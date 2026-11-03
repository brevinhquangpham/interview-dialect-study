# Dialect generation pipeline

Turns SAE interview responses into dialect variants with Multi-VALUE, with
meaning-preservation checks and a manual-review hook.

## Setup (Python 3.11)

    uv venv --python 3.11 .venv && uv pip install --python .venv/bin/python -r requirements.txt
    .venv/bin/python -m spacy download en_core_web_sm
    .venv/bin/python -c "import nltk; [nltk.download(p) for p in ('wordnet','omw-1.4','cmudict')]"

The first Multi-VALUE run also downloads Stanza models.

## Run

    .venv/bin/python generate_dialects.py data/sample_responses.csv data/dialect_variants.csv \
        --dialects SAE IndianEnglish            # also: SingaporeanEnglish AAE
    .venv/bin/python -m unittest discover -s tests -t .

Input CSV columns: `response_id` (unique), `question_id`, `correctness`, `text`, and
optionally `protected_terms` (`|`-separated terms that must survive verbatim).
`data/sample_responses.csv` is placeholder content for testing only.

## Output (`dialect_variants.csv`)

One row per response x dialect (SAE is the unchanged baseline). Includes the rules
that fired (`features`, `rules`), the `seed`, `attempts`, per-check results
(`failed_checks`, `needs_review`), blank manual columns (`reviewer`,
`meaning_preserved`, `natural`, `revised_text`), and `final_text` = the manual
revision if present, otherwise the automatic variant. Re-running with `--force`
keeps manual columns for rows whose automatic text did not change.

## How it works

1. Code spans, `O(...)` expressions and `protected_terms` are masked with placeholders.
2. Up to `--max-attempts` seeded Multi-VALUE candidates are generated (deterministic).
3. The first candidate that changes the text and passes every check is kept; otherwise
   the least-bad one is kept and flagged. Checks: protected spans, numbers, negation
   count, logical connectives (if/because/but/...), content-word overlap, length ratio.
4. Negative-concord features are disabled by default (`--exclude-features`).

The checks are heuristics and cannot detect ungrammatical output; every variant
still needs human review.
