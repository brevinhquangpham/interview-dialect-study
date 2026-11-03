# Run this with: python generate_dialects.py data/sample_responses.csv data/dialect_variants.csv

import argparse
import json
import os
import re
import warnings
import zlib
from collections import Counter

os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd

# dialects used
DIALECTS = {
    "SAE": None,
    "IndianEnglish": "IndianDialect",
    "SingaporeanEnglish": "ColloquialSingaporeDialect",
    "AAE": "AfricanAmericanVernacular",
}
DEFAULT_DIALECTS = ["SAE", "IndianEnglish"]

DEFAULT_EXCLUDED_FEATURES = [
    "negative_concord",
    "no_preverbal_negator",
    "never_negator",
]

MANUAL_COLUMNS = ["reviewer", "meaning_preserved", "natural", "revised_text"]
REQUIRED_COLUMNS = ["response_id", "question_id", "correctness", "text"]

# Technical content protection
# this is just a mask to prevent technical content from possibly being overwritten and replaced
CODE_SPAN = r"```.*?```|`[^`\n]+`"
BIG_O = r"\bO\([^()\n]*\)"


# Protection Written by Claude
def protect(text, extra_terms=()):
    """Replace code spans, Big-O expressions and listed terms with placeholders.

    Multi-VALUE would otherwise inflect or drop pieces of identifiers. Returns the
    masked text and {placeholder: original}.
    """
    parts = [CODE_SPAN, BIG_O]
    terms = sorted({t for t in extra_terms if t}, key=len, reverse=True)
    if terms:
        parts.append(r"(?<!\w)(?:" + "|".join(re.escape(t) for t in terms) + r")(?!\w)")
    mapping = {}

    def mask(match):
        n, letters = len(mapping), ""
        while True:
            n, r = divmod(n, 26)
            letters += chr(ord("a") + r)
            if not n:
                break
        key = f"Zq{letters}qz"
        mapping[key] = match.group(0)
        return key

    return re.sub("|".join(parts), mask, text, flags=re.DOTALL), mapping


def unprotect(text, mapping):
    for key, original in mapping.items():
        text = text.replace(key, original)
    return text


# Automatic meaning-preservation checks

NEGATION = re.compile(
    r"\b(?:not|no|never|none|nothing|neither|nor|cannot|ain't|aint|dont|doesnt|didnt|isnt|arent|"
    r"wasnt|werent|cant|wont|couldnt|shouldnt|wouldnt|hasnt|havent|hadnt)\b|n't\b"
)
STOPWORDS = set(
    "that this with from have been were they them their there then than when what which while "
    "will would could should about into over also just only some such each very more most does "
    "doesn".split()
)
# Short function words that carry the logic of an answer; losing one ("If two keys
CONNECTIVES = (
    "if",
    "because",
    "unless",
    "until",
    "but",
    "so",
    "or",
    "than",
    "only",
    "all",
    "every",
    "before",
    "after",
    "while",
    "since",
    "then",
)
MIN_CONTENT_OVERLAP = 0.8
LENGTH_RATIO_RANGE = (0.6, 1.4)


def _norm(text):
    return text.replace("’", "'").lower()


def _count_word(text, word):
    return len(re.findall(rf"\b{word}\b", text))


def _stems(text):
    """4-letter prefixes of content words; crude, but survives inflection changes."""
    return [
        w[:4]
        for w in re.findall(r"[a-z]+", _norm(text))
        if len(w) >= 4 and w not in STOPWORDS
    ]


def run_checks(source, variant, protected):
    """Return {check_name: bool, ...}; True means the check passed."""
    src_n, var_n = _norm(source), _norm(variant)
    stems = _stems(source)
    variant_stems = set(_stems(variant))
    overlap = sum(s in variant_stems for s in stems) / len(stems) if stems else 1.0
    ratio = len(variant) / max(len(source), 1)
    return {
        "protected_intact": all(variant.count(p) >= source.count(p) for p in protected),
        "numbers_preserved": Counter(re.findall(r"\d+", src_n))
        == Counter(re.findall(r"\d+", var_n)),
        "negation_preserved": len(NEGATION.findall(src_n))
        == len(NEGATION.findall(var_n)),
        "connectives_preserved": all(
            _count_word(var_n, w) >= _count_word(src_n, w) for w in CONNECTIVES
        ),
        "content_overlap_ok": overlap >= MIN_CONTENT_OVERLAP,
        "length_ratio_ok": LENGTH_RATIO_RANGE[0] <= ratio <= LENGTH_RATIO_RANGE[1],
    }


# Transformation (where MValue is actually rewriting text)


def load_dialect(name, excluded_features):
    from multivalue import Dialects

    dialect = getattr(Dialects, DIALECTS[name])()
    for feature in excluded_features:
        dialect.morphosyntax_transforms.pop(feature, None)
    return dialect


def seed_for(response_id, dialect_name, base_seed, attempt):
    return (
        zlib.crc32(f"{response_id}|{dialect_name}".encode()) + base_seed + attempt
    ) % 2**32


def transform_once(dialect, masked_text, mapping, seed):
    import random

    random.seed(seed)
    out = dialect.convert_sae_to_dialect(masked_text)
    rules = [
        {"type": r["type"], "value": unprotect(r["value"], mapping)}
        for _, r in sorted(dialect.executed_rules.items())
    ]
    return unprotect(out, mapping), rules


def generate_variant(dialect, name, row, base_seed, max_attempts):
    source = row["text"]
    extra = [t.strip() for t in str(row.get("protected_terms", "") or "").split("|")]
    masked, mapping = protect(source, extra)
    protected = list(mapping.values())

    best = None
    for attempt in range(max_attempts):
        seed = seed_for(row["response_id"], name, base_seed, attempt)
        text, rules = transform_once(dialect, masked, mapping, seed)
        changed = text.strip() != source.strip()
        checks = run_checks(source, text, protected)
        failed = sum(not ok for ok in checks.values())
        candidate = dict(
            text=text,
            rules=rules,
            changed=changed,
            checks=checks,
            seed=seed,
            attempts=attempt + 1,
        )
        if changed and not failed:
            return candidate
        # we prefer changed candidates, then fewest failed checks, then most rules.
        rank = (not changed, failed, -len(rules))
        if best is None or rank < best[0]:
            best = (rank, candidate)
    candidate = best[1]
    candidate["attempts"] = max_attempts
    return candidate


def build_rows(df, dialect_names, excluded_features, base_seed, max_attempts):
    loaded = {
        n: load_dialect(n, excluded_features) for n in dialect_names if DIALECTS[n]
    }
    rows = []
    for _, row in df.iterrows():
        for name in dialect_names:
            base = dict(
                response_id=row["response_id"],
                question_id=row["question_id"],
                correctness=row["correctness"],
                dialect=name,
                source_text=row["text"],
            )
            if DIALECTS[name] is None:
                rows.append(
                    {
                        **base,
                        "variant_text": row["text"],
                        "changed": False,
                        "n_rules": 0,
                        "features": "{}",
                        "rules": "[]",
                        "seed": "",
                        "attempts": 0,
                        "checks_passed": True,
                        "failed_checks": "",
                        "needs_review": False,
                    }
                )
                continue
            c = generate_variant(loaded[name], name, row, base_seed, max_attempts)
            failed = [k for k, ok in c["checks"].items() if not ok]
            if not c["changed"]:
                failed.append("unchanged")
            rows.append(
                {
                    **base,
                    "variant_text": c["text"],
                    "changed": c["changed"],
                    "n_rules": len(c["rules"]),
                    "features": json.dumps(
                        dict(Counter(r["type"] for r in c["rules"]))
                    ),
                    "rules": json.dumps(c["rules"]),
                    "seed": c["seed"],
                    "attempts": c["attempts"],
                    "checks_passed": not failed,
                    "failed_checks": ";".join(failed),
                    "needs_review": bool(failed),
                }
            )
    out = pd.DataFrame(rows)
    for col in MANUAL_COLUMNS:
        out[col] = ""
    return out


# Outputs hnadling


def carry_over_manual_work(new, path):
    """Keep reviewers' columns from an existing output file when the auto text is
    unchanged; warn about rows whose variant changed underneath a review."""
    old = pd.read_csv(path, dtype=str, keep_default_na=False)
    keys = ["response_id", "dialect"]
    merged = new.drop(columns=MANUAL_COLUMNS).merge(
        old[keys + ["variant_text"] + MANUAL_COLUMNS],
        on=keys,
        how="left",
        suffixes=("", "_old"),
    )
    same = merged["variant_text"] == merged["variant_text_old"]
    stale = (~same) & merged[MANUAL_COLUMNS].fillna("").ne("").any(axis=1)
    for col in MANUAL_COLUMNS:
        merged[col] = merged[col].where(same, "").fillna("")
    if stale.any():
        print(
            f"WARNING: {int(stale.sum())} reviewed row(s) now have different auto text; their manual columns "
            f"were cleared: {merged.loc[stale, 'response_id'].tolist()}"
        )
    return merged.drop(columns=["variant_text_old"])


def finalize(df):
    df["final_text"] = df["revised_text"].where(
        df["revised_text"].ne(""), df["variant_text"]
    )
    return df


def print_summary(df):
    sub = df[df["dialect"] != "SAE"]
    if sub.empty:
        return
    g = sub.groupby("dialect")
    summary = pd.DataFrame(
        {
            "n": g.size(),
            "changed_%": (g["changed"].mean() * 100).round(0),
            "mean_rules": g["n_rules"].mean().round(1),
            "needs_review_%": (g["needs_review"].mean() * 100).round(0),
        }
    )
    print("\n" + summary.to_string())
    failures = Counter(f for s in sub["failed_checks"] for f in s.split(";") if f)
    if failures:
        print("failed checks:", dict(failures))


def main():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument(
        "input",
        help="CSV with columns: " + ", ".join(REQUIRED_COLUMNS) + " [protected_terms]",
    )
    p.add_argument("output", help="CSV to write")
    p.add_argument(
        "--dialects", nargs="+", default=DEFAULT_DIALECTS, choices=list(DIALECTS)
    )
    p.add_argument("--seed", type=int, default=0, help="base seed (default 0)")
    p.add_argument(
        "--max-attempts",
        type=int,
        default=10,
        help="seeded candidates tried per variant",
    )
    p.add_argument(
        "--exclude-features",
        nargs="*",
        default=DEFAULT_EXCLUDED_FEATURES,
        help="Multi-VALUE features to disable; pass with no values to disable none",
    )
    p.add_argument(
        "--force", action="store_true", help="overwrite an existing output file"
    )
    args = p.parse_args()

    df = pd.read_csv(args.input, dtype=str, keep_default_na=False)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        p.error(f"input is missing columns: {missing}")
    if df["response_id"].duplicated().any():
        p.error("response_id must be unique")
    if os.path.exists(args.output) and not args.force:
        p.error(
            f"{args.output} exists; pass --force to regenerate (manual review columns are preserved)"
        )

    out = build_rows(
        df, args.dialects, args.exclude_features, args.seed, args.max_attempts
    )
    if os.path.exists(args.output):
        out = carry_over_manual_work(out, args.output)
    out = finalize(out)
    out.to_csv(args.output, index=False)
    print(f"wrote {len(out)} rows to {args.output}")
    print_summary(out)


if __name__ == "__main__":
    main()
