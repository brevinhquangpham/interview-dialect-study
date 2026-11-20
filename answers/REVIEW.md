# SAE answer bank: draft for review

> **Draft, not final.** 90 answers = 15 questions × 3 correctness levels × 2 variants. Every correctness label needs a human check before we generate dialect versions. The *Why this label* line says what makes it correct, partial or incorrect; argue with it if you disagree.

Levels: **correct** = accurate and covers what the question asks. **partial** = right core idea but missing a part the question asks for, or one notable error. **incorrect** = a confident answer built on a real misconception.

Within each question, the three levels are kept close in length so that length can't give away correctness.

## Q1 · Python · Easy

**What is the difference between a list and a tuple in Python, and when would you use each?**

**Q1-C1**: `correct` · 83 words

> The main difference is that a list is mutable and a tuple is immutable. Because tuples are immutable, they are hashable as long as their elements are hashable, so I can use them as dictionary keys or put them in a set, which I cannot do with a list. I would use a list for a collection that changes, like items in a shopping cart, and a tuple for a fixed record, like a coordinate pair or several values returned from a function.

*Why this label:* Mutability, hashability, and a fitting use case for each.

**Q1-C2**: `correct` · 93 words

> A list can be modified in place, so I can append, insert, or delete items, while a tuple cannot be changed once it is built. That immutability is useful because it signals that the data should stay the same, and it lets a tuple be used as a key in a dictionary if everything inside it is also immutable. So I reach for a list when I am collecting or updating items, and a tuple when I have a fixed group of related values, like a date stored as year, month, and day.

*Why this label:* Same points as C1 in different words.

**Q1-P1**: `partial` · 88 words

> A list uses square brackets and a tuple uses parentheses. The other difference is that a tuple cannot be changed after you create it, while a list can be changed whenever you want. In practice I almost always just use lists, because they are more flexible and you can do more with them, like appending or sorting. I think tuples are mostly there for older code, so I do not really see a reason to choose them in a new project unless someone else's code already uses them.

*Why this label:* Mutability is right, but there is no real use case for tuples and it wrongly calls them legacy.

**Q1-P2**: `partial` · 87 words

> Lists are mutable and tuples are immutable, so you can change a list after creating it but not a tuple. Since tuples are immutable, any tuple can be used as a dictionary key, no matter what it contains, which makes them handy for lookups. I would use a list when the data needs to grow or change, like a list of user names that I keep adding to, and a tuple when the values belong together and should stay the same, like a latitude and longitude pair.

*Why this label:* Mostly right, but 'any tuple can be a key' is false: a tuple holding a list is not hashable.

**Q1-I1**: `incorrect` · 89 words

> The main difference is that a tuple can only hold one type of data, while a list can mix types, like numbers and strings together. Tuples are also kept sorted automatically, which is why lookups in a tuple are faster than in a list. So I would use a tuple when I have a group of numbers that I want to keep in order, like test scores, and a list when I need to store mixed information, like a user's name, age, and email address in the same place.

*Why this label:* Wrong: tuples can hold mixed types and are not kept sorted. Misses mutability entirely.

**Q1-I2**: `incorrect` · 85 words

> A tuple is basically a faster version of a list. You can still append items to a tuple and change its values, but you cannot sort it or reverse it, which is the tradeoff for the extra speed. Lists have more built in methods, so they are slower. I would use a tuple whenever performance matters, like inside a loop that runs many times, and a list when I need to sort the data or use one of the extra methods that only lists have.

*Why this label:* Wrong: tuples cannot be appended to or changed; the speed framing is a misconception.

## Q2 · Python · Medium

**Explain the difference between a shallow copy and a deep copy in Python. Give an example of when this matters.**

**Q2-C1**: `correct` · 89 words · protected: copy.copy, copy.deepcopy

> A shallow copy creates a new outer object, but the elements inside it are still references to the same objects as the original. A deep copy recursively copies everything, so the nested objects are new as well. This matters with nested data. For example, if I have a list of lists representing a game board and I make a shallow copy with copy.copy, then change a cell in one of the inner lists, the original board changes too. If I use copy.deepcopy instead, the two boards are completely independent.

*Why this label:* Correct definitions plus a nested-list example showing the difference.

**Q2-C2**: `correct` · 92 words

> With a shallow copy, Python builds a new container but fills it with the same inner objects, so the copy and the original share anything nested. A deep copy walks through the whole structure and duplicates every nested object. It matters when the data has mutable objects inside. Say I copy a dictionary of settings where each value is a list. If I shallow copy it and append to one of those lists, the original settings change as well. A deep copy avoids that, at the cost of more time and memory.

*Why this label:* Same concept with a settings-dictionary example and the cost tradeoff.

**Q2-P1**: `partial` · 82 words

> A shallow copy only copies the top level of an object, and a deep copy copies the object and everything inside it. So a deep copy is more complete than a shallow copy. In Python you can make a deep copy with the copy module. It matters when you want to be sure your copy is fully separate from the original, so you would usually use a deep copy if you are not sure which one you need, just to be safe.

*Why this label:* Definitions are right but there is no concrete example of when it matters, as the question asks.

**Q2-P2**: `partial` · 81 words

> A shallow copy makes a new object but shares the inner objects with the original, while a deep copy duplicates the inner objects too. For example, if I shallow copy a list of integers and then change one number in the copy, the original list changes as well, because the integers are shared. With a deep copy that would not happen. So any time I copy a list and plan to modify it, I make a deep copy to stay safe.

*Why this label:* Definitions right, but the example is wrong: reassigning an int in a shallow-copied flat list does not affect the original.

**Q2-I1**: `incorrect` · 86 words

> A shallow copy is when you assign one variable to another, like b equals a, so both names point to the same list. A deep copy is when you call the copy method on the list, which makes a brand new list with brand new elements inside, so nothing is shared. This matters because if you only assign the variable and then modify b, you will also modify a. So whenever I need a separate version, I just call the copy method and I am safe.

*Why this label:* Wrong: assignment is not a copy at all, and list.copy() is a shallow copy, not deep.

**Q2-I2**: `incorrect` · 84 words

> The difference is about what gets copied. A deep copy copies both the data and the methods of the object, while a shallow copy only copies the data, which is why a shallow copy is faster. In both cases the copy is fully independent, so changing the copy will never affect the original object. It matters mostly for performance, so for large objects I would use a shallow copy to save time, and a deep copy only when I need the methods as well.

*Why this label:* Wrong: methods are not copied per object, and shallow copies do share nested objects.

## Q3 · Python · Hard

**How does Python's Global Interpreter Lock (GIL) affect multithreaded programs, and when would multiprocessing be preferable?**

**Q3-C1**: `correct` · 95 words · protected: GIL, CPython, I/O

> In CPython, the Global Interpreter Lock is a mutex that allows only one thread to execute Python bytecode at a time. For CPU bound work, this means multiple threads do not run in parallel, so adding threads gives little or no speedup. For I/O bound work, threads still help, because the GIL is released while a thread waits on I/O. When the work is CPU bound, I would use multiprocessing, since each process has its own interpreter and its own GIL, at the cost of more memory and the overhead of passing data between processes.

*Why this label:* CPU-bound vs I/O-bound distinction, why multiprocessing helps, and its cost.

**Q3-C2**: `correct` · 94 words · protected: GIL, CPython

> The GIL is a lock inside the standard CPython interpreter that lets only one thread run Python code at any moment. Threads can still take turns, so they are fine for tasks that spend most of their time waiting, because a waiting thread releases the lock. But for tasks that keep the processor busy, threads end up running one after another instead of in parallel. In that case multiprocessing is better, because separate processes each get their own GIL and can use multiple cores, although starting processes and sharing data between them costs more.

*Why this label:* Same points with different examples.

**Q3-P1**: `partial` · 81 words · protected: GIL

> The GIL is a lock that makes sure only one thread runs Python code at a time. Because of that, threads in Python can never run in parallel, so multithreading basically does not help performance in Python at all. That is why I would always use multiprocessing instead of threads whenever I want a program to run faster, since each process gets its own interpreter and can run on its own core. Threads are mostly useful just for keeping code organized.

*Why this label:* Definition is right, but it misses that threads still help with I/O-bound work.

**Q3-P2**: `partial` · 85 words · protected: GIL, CPython

> The Global Interpreter Lock is a lock in CPython that only lets one thread execute Python bytecode at a time, even on a machine with many cores. The interpreter switches between threads, so it can look like they are running together, but only one is actually executing Python code at any moment. This was done to make memory management simpler and safer inside the interpreter. Because of the GIL, multithreaded Python programs behave differently from multithreaded programs in languages like Java or C plus plus.

*Why this label:* Accurate description but never says when multiprocessing is preferable.

**Q3-I1**: `incorrect` · 83 words · protected: GIL

> The GIL is a lock on global variables. It stops two threads from changing the same global variable at the same time, which makes Python programs thread safe automatically. Because of that, you do not need to add your own locks in Python the way you would in Java. It does not really slow down multithreaded programs. I would only use multiprocessing if the program needs more memory than one process is allowed to use, since each process gets its own memory space.

*Why this label:* Wrong: the GIL is not about global variables and does not make user code thread-safe.

**Q3-I2**: `incorrect` · 86 words · protected: GIL, I/O

> The GIL limits how Python threads run, so the rule of thumb is to use threads for CPU bound work and multiprocessing for I/O bound work. Threads share memory, so they are good for heavy calculations where all the threads need the same data. Processes are better for things like downloading files or waiting on a database, because each process can wait on its own without blocking the others. So for a web scraper I would use multiprocessing, and for matrix math I would use threads.

*Why this label:* Wrong: the recommendation is reversed for CPU-bound vs I/O-bound work.

## Q4 · Data Structures · Easy

**What is the difference between a stack and a queue? Give a practical example of each.**

**Q4-C1**: `correct` · 89 words

> A stack is last in, first out, so the most recently added item is the first one removed. A queue is first in, first out, so items are removed in the same order they were added, with new items going in at the back and leaving from the front. A practical example of a stack is the undo feature in a text editor, where the latest change is undone first. A practical example of a queue is a printer queue, where documents print in the order they were sent.

*Why this label:* LIFO vs FIFO, operations, and a correct example of each.

**Q4-C2**: `correct` · 92 words

> The difference is the order in which items come out. A stack follows last in, first out, like a pile of plates where you take the top plate first. A queue follows first in, first out, like a line at a coffee shop where the first person in line is served first. In software, the browser back button behaves like a stack, because it returns you to the page you visited most recently. A task scheduler that handles requests in arrival order, or breadth first search in a graph, uses a queue.

*Why this label:* Same concept with different examples.

**Q4-P1**: `partial` · 92 words

> A stack is last in, first out, and a queue is first in, first out. So with a stack the newest item is removed first, and with a queue the oldest item is removed first. Both of them are ways to store a collection of items in a certain order, and you can build either one using a list or an array. A practical example of a stack would be the call stack when a program runs functions, and a queue is also used in a lot of different places in programming.

*Why this label:* Definitions right, but the queue example is missing.

**Q4-P2**: `partial` · 88 words

> A stack is last in, first out, and a queue is first in, first out. With a stack you push and pop items from the same end, and with a queue you add at one end and remove from the other. A practical example of a stack is the undo history in an editor, since the last change is undone first. A practical example of a queue is the browser back button, since it takes you back through the pages you visited in the order you saw them.

*Why this label:* Definitions right, but the back-button example is a stack, not a queue.

**Q4-I1**: `incorrect` · 89 words

> A stack is first in, first out, and a queue is last in, first out. With a stack, the first item you put in is the first one to come out, kind of like people waiting in a line. With a queue, the newest item comes out first, like a pile of books where you grab the one on top. So a practical example of a stack is a printer handling documents in order, and a practical example of a queue is the undo button in a text editor.

*Why this label:* Wrong: LIFO and FIFO are swapped, so both examples are swapped too.

**Q4-I2**: `incorrect` · 88 words

> The difference is mostly about how they are stored in memory. A stack is stored in one continuous block of memory, while a queue is always stored as a linked list spread around memory. That is why stacks are faster to access than queues. Otherwise they work the same way, since both let you add and remove items from either end. I would use a stack when speed matters, like in a game loop, and a queue when I do not know how many items there will be.

*Why this label:* Wrong: the defining difference is removal order (LIFO vs FIFO), not memory layout.

## Q5 · Data Structures · Medium

**How does a hash table work, and what happens when two keys produce the same hash index?**

**Q5-C1**: `correct` · 93 words

> A hash table stores key value pairs in an array of buckets. A hash function turns each key into a bucket index, so on average inserts and lookups take constant time. When two keys map to the same index, that is a collision. One common fix is separate chaining, where each bucket holds a small list of entries. Another is open addressing, where we probe for the next free slot. As the table fills up, it resizes and rehashes to keep collisions rare, because with many collisions lookups can degrade to linear time.

*Why this label:* Hashing to an index, two collision strategies, resizing, and the worst case.

**Q5-C2**: `correct` · 94 words

> A hash table uses a hash function to convert a key into an index in an underlying array, so it can jump straight to where the value should be. That gives average constant time lookups. Two different keys can still land on the same index, which is called a collision. The table handles it either by keeping a linked list in each slot and searching that list, or by probing other slots until it finds an empty one. Keeping the load factor low by growing the array prevents long chains and keeps operations fast.

*Why this label:* Same concept; mentions load factor and resizing.

**Q5-P1**: `partial` · 87 words

> A hash table uses a hash function to turn a key into an index in an array, and then it stores the value at that index. When two keys produce the same index, which is called a collision, the table stores both entries in a linked list at that slot and searches the list. Because of the hash function, lookups in a hash table are always constant time, even when there are collisions, which is why hash tables are faster than every other data structure for searching.

*Why this label:* Mechanism and chaining are right, but 'always constant time even with collisions' is false.

**Q5-P2**: `partial` · 91 words

> A hash table takes a key, runs it through a hash function, and uses the result to decide where to store the value in an array. This makes finding values quick, because you do not have to look through every item. Sometimes two keys get the same index, and that is called a collision. When that happens, the hash table has a built in way of dealing with it so that both values can still be stored and found later, so it is not something you usually need to worry about.

*Why this label:* Hashing is explained, but collision handling is left vague with no actual strategy.

**Q5-I1**: `incorrect` · 85 words

> A hash table uses a hash function to turn each key into an index in an array, and the value is stored there. When two keys produce the same index, the second key overwrites the first one, because each index can only hold one value. That is the reason keys in a dictionary have to be unique. To avoid losing data, you have to choose keys that will not produce the same hash, which is why most people use numbers or short strings as keys.

*Why this label:* Wrong: colliding keys do not overwrite each other; collisions are resolved by chaining or probing.

**Q5-I2**: `incorrect` · 83 words · protected: log n

> A hash table works by sorting all the keys when they are inserted, so that it can use binary search to find any key quickly. The hash part refers to how the keys are compressed to save memory. When two keys produce the same hash, the table just compares the original keys during the binary search to tell them apart. This is why lookups in a hash table take log n time, which is still much faster than searching through an unsorted list.

*Why this label:* Wrong: hash tables do not sort keys or use binary search.

## Q6 · Data Structures · Hard

**Explain how a self-balancing binary search tree maintains efficient operations and why balancing is necessary.**

**Q6-C1**: `correct` · 93 words · protected: O of log n

> In a binary search tree, search, insert, and delete all take time proportional to the height of the tree. If keys arrive in sorted order, a plain tree turns into something like a linked list, and those operations become linear. A self balancing tree, such as an AVL tree or a red black tree, checks a balance rule after every insert or delete, and if the rule is broken it fixes the shape with rotations. This keeps the height logarithmic, so every operation stays O of log n even in the worst case.

*Why this label:* Why height matters, the sorted-input failure case, rotations, and the guarantee.

**Q6-C2**: `correct` · 96 words · protected: log n

> The efficiency of a binary search tree depends on its height, because each operation walks one path from the root. Without balancing, inserting already sorted data makes every new node go to the same side, so the tree becomes a long chain and searching is linear. Self balancing trees prevent that. A red black tree, for example, colors nodes and enforces rules about those colors, and after each insertion or deletion it recolors nodes and performs rotations to restore the rules. That guarantees the height stays around log n, so search, insert, and delete stay fast.

*Why this label:* Same concept using red-black trees.

**Q6-P1**: `partial` · 78 words · protected: O of log n

> A self balancing binary search tree keeps itself balanced so that operations like search and insert stay at O of log n. Trees like AVL trees use rotations to move nodes around and keep the left and right sides even. Balancing is necessary because a balanced tree is faster than an unbalanced one, and it also uses memory more efficiently. Without balancing, the tree would still work correctly, but it would be slower and take up more space.

*Why this label:* Rotations and O(log n) are right, but it never explains how a tree becomes unbalanced; 'takes more space' is wrong.

**Q6-P2**: `partial` · 83 words · protected: log n

> A self balancing tree is a binary search tree that keeps its height small so that searching stays fast. If a tree gets unbalanced, for example when you insert values in sorted order, it can end up looking like a linked list and searching becomes slow. To avoid this, the tree rearranges its nodes whenever it notices that one side has gotten too deep. That way it keeps operations efficient, usually around log n time, no matter what order the data comes in.

*Why this label:* Explains why balancing is needed, but the mechanism (rotations, balance rules) is vague.

**Q6-I1**: `incorrect` · 79 words

> A self balancing tree keeps the same number of nodes on every level. After each insert, it copies all the values into an array, sorts them, and rebuilds the tree from the middle out, so it stays perfectly balanced. Because the tree is rebuilt in sorted order, insertion is constant time and search is constant time too. Balancing is necessary because otherwise the tree would not be sorted, and you would not be able to search it at all.

*Why this label:* Wrong: balancing uses local rotations rather than full rebuilds, and the operations are O(log n), not constant time.

**Q6-I2**: `incorrect` · 79 words

> Balancing means making sure the left subtree and the right subtree of the root always have exactly the same values in them, mirrored on each side. Because both sides match, the tree can check the left side and right side at the same time, which makes search constant time. It is necessary because an unbalanced tree cannot do this parallel search. Trees like AVL trees do this by duplicating nodes when one side has fewer values than the other.

*Why this label:* Wrong: balance is about height, not mirrored values; it gives O(log n), not constant time.

## Q7 · Algorithms · Easy

**What is the difference between linear search and binary search? When can binary search be used?**

**Q7-C1**: `correct` · 95 words · protected: O of n, O of log n

> Linear search checks each element one by one from the start until it finds the target or reaches the end, so it takes O of n time but works on any list. Binary search only works when the data is sorted and you can access elements by index. It looks at the middle element, and if the target is smaller it continues in the left half, otherwise in the right half, cutting the search space in half each time. That gives O of log n time, so it is much faster on large sorted arrays.

*Why this label:* Both algorithms, their complexity, and the sorted-plus-random-access requirement.

**Q7-C2**: `correct` · 94 words

> With linear search you scan the items in order and compare each one to what you are looking for, which is simple and works on unsorted data, but in the worst case you look at every element. Binary search requires the collection to be sorted. You compare the target with the middle item and throw away the half where it cannot be, and you repeat until you find it or run out of items. Because the range halves each step, a million sorted items take about twenty comparisons instead of up to a million.

*Why this label:* Same points with a concrete comparison count.

**Q7-P1**: `partial` · 87 words · protected: O of n, O of log n

> Linear search goes through the list one element at a time until it finds the value, so it can take a long time on a big list. Binary search is faster because it starts in the middle of the list and decides whether to go left or right, cutting the list in half each time. So binary search takes O of log n time instead of O of n. You can use binary search whenever you have a large list and you want to find something quickly.

*Why this label:* Algorithms are right, but it misses that binary search requires sorted data, which the question asks.

**Q7-P2**: `partial` · 78 words · protected: O of n divided by two

> Linear search checks every element in order until it finds the target. Binary search can only be used on a sorted list. It checks the middle element and then only searches the half where the target could be. Because it skips half of the remaining elements each time, binary search runs in O of n divided by two time, which is about twice as fast as linear search, and that is why it is preferred for sorted data.

*Why this label:* The sorted requirement is right, but the complexity is wrong: binary search is O(log n).

**Q7-I1**: `incorrect` · 79 words

> Linear search starts at the beginning and goes to the end, while binary search checks two elements at a time, one from the front and one from the back, and moves toward the middle. That is why it is called binary, because it looks at two positions at once. This makes binary search twice as fast as linear search. Binary search can be used on any list, sorted or not, as long as it has at least two elements.

*Why this label:* Wrong: binary search halves a sorted range; it does not scan from both ends, and it requires sorted data.

**Q7-I2**: `incorrect` · 88 words

> Linear search is used for normal data like numbers and strings, and binary search is used for binary data, like ones and zeros or data stored in binary files. Binary search is also the search used inside binary trees, which is where the name comes from. So the main question is what kind of data you have. If you are searching text or a regular list, you would use linear search, and if you are working with binary values or a binary tree, you would use binary search.

*Why this label:* Wrong: binary search refers to halving a sorted range, not to binary data.

## Q8 · Algorithms · Medium

**Explain how merge sort works and describe its time and space complexity.**

**Q8-C1**: `correct` · 89 words · protected: O of n log n, O of n, log n

> Merge sort is a divide and conquer algorithm. It splits the array into two halves, recursively sorts each half, and then merges the two sorted halves by repeatedly taking the smaller of the two front elements. There are about log n levels of splitting, and each level does O of n work during merging, so the time complexity is O of n log n in the best, average, and worst case. The standard array version needs O of n extra space for merging, and it is a stable sort.

*Why this label:* Split, recurse, merge; O(n log n) in all cases; O(n) extra space.

**Q8-C2**: `correct` · 92 words · protected: O of n log n, O of n, log n

> Merge sort keeps dividing the list in half until each piece has one element. Then it builds the answer back up by merging pairs of sorted pieces, comparing the first element of each piece and moving the smaller one into a new list until both pieces are used up. Every level of merging touches all n elements, and there are log n levels, so it always runs in O of n log n time. The drawback is memory, since merging needs a temporary array, so it uses O of n additional space.

*Why this label:* Same content, explained bottom-up.

**Q8-P1**: `partial` · 85 words · protected: O of n log n, O of 1, log n

> Merge sort splits the array into halves over and over until each part has one element, and then it merges the parts back together in sorted order by comparing their elements. Since the array is split in half log n times and each merge step goes through all the elements, the time complexity is O of n log n. Merge sort also sorts the array in place, so its space complexity is O of 1, which makes it a good choice when memory is limited.

*Why this label:* Process and time are right, but the space claim is wrong: standard merge sort needs O(n) extra space.

**Q8-P2**: `partial` · 84 words · protected: O of n log n

> Merge sort is a divide and conquer algorithm. It divides the array into two halves, sorts each half, and then merges the halves together into one sorted array, taking the smaller front element each time. It keeps dividing until the pieces are small enough to be trivially sorted. Its time complexity is O of n log n, which makes it faster than simple algorithms like bubble sort or insertion sort on large inputs, and it performs consistently regardless of how the data starts out.

*Why this label:* Process and time are right, but space complexity, which the question asks for, is never mentioned.

**Q8-I1**: `incorrect` · 89 words · protected: O of n log n, O of n squared, O of 1

> Merge sort picks one element as a pivot and moves everything smaller to its left and everything larger to its right. Then it does the same thing on the left side and the right side until everything is in order, and finally it merges the sides back together. On average it takes O of n log n time, but if you keep choosing a bad pivot, like the smallest element, it becomes O of n squared. It does not need extra memory, so the space is O of 1.

*Why this label:* Wrong: this describes quicksort, not merge sort, including the wrong worst case and space.

**Q8-I2**: `incorrect` · 82 words · protected: O of n

> Merge sort works by merging adjacent elements. It goes through the array once, and whenever two neighbors are out of order it merges them into the right order, like combining two cards in your hand. Since it only passes through the array a single time, the time complexity is O of n, which is the fastest possible for sorting. It also does not create any new arrays, so its space complexity is constant, which is why many languages use it by default.

*Why this label:* Wrong: merge sort is not one pass, it is not O(n), and it uses O(n) extra space.

## Q9 · Algorithms · Hard

**Explain how Dijkstra's algorithm finds shortest paths and why negative edge weights are problematic.**

**Q9-C1**: `correct` · 92 words · protected: Bellman Ford

> Dijkstra's algorithm sets the source distance to zero and every other node to infinity. It keeps a priority queue of nodes ordered by their current best distance. Each step, it removes the node with the smallest distance, which is now final, and relaxes its edges. This greedy choice is correct because, with non negative weights, no later path can get back to a finished node more cheaply. With a negative edge that is no longer true, a finished node could later get a shorter path, so we would use Bellman Ford instead.

*Why this label:* Initialization, priority queue, relaxation, why greedy works, and why negative edges break it.

**Q9-C2**: `correct` · 89 words

> Dijkstra's algorithm grows a set of nodes whose shortest distance from the source is known. It always picks the unvisited node with the smallest tentative distance, usually using a min heap, marks it as done, and then checks each of its neighbors to see if the path through it is shorter than what we had. The algorithm assumes that once a node is done, its distance cannot improve. Negative edge weights break that assumption, because a path that looks longer at first could become shorter after a negative edge.

*Why this label:* Same content, described as growing a set of finished nodes.

**Q9-P1**: `partial` · 80 words

> Dijkstra's algorithm starts at the source with distance zero and uses a priority queue to always visit the closest unvisited node next. For that node, it updates the distances of its neighbors if it finds a shorter path through it, and it repeats until every node has been visited. Negative edge weights are a problem because they create cycles where the distance keeps going down forever, so the algorithm would get stuck in an infinite loop and never finish running.

*Why this label:* The algorithm is right, but it confuses negative edges with negative cycles; Dijkstra gives wrong answers, not an infinite loop.

**Q9-P2**: `partial` · 80 words

> Dijkstra's algorithm finds the shortest path from one starting node to all the other nodes in a weighted graph. It sets the start to zero and everything else to infinity, then repeatedly takes the unvisited node with the lowest distance from a priority queue and updates its neighbors if it finds a cheaper path. It continues until all the nodes are visited. Dijkstra's algorithm does not support negative edge weights, so for those graphs you would need a different algorithm.

*Why this label:* The algorithm is right, but it never explains why negative weights are a problem.

**Q9-I1**: `incorrect` · 83 words

> Dijkstra's algorithm explores every possible path from the source to each node using depth first search, adds up the weights along each path, and then keeps the path with the smallest total. That is why it always finds the shortest path. Negative edge weights are problematic because the priority queue used by Dijkstra's algorithm can only store positive numbers, so the program throws an error when it sees a negative weight. That is also why Dijkstra can be slow on very large graphs.

*Why this label:* Wrong: Dijkstra does not enumerate all paths with DFS, and the negative-weight explanation is invented.

**Q9-I2**: `incorrect` · 81 words

> Dijkstra's algorithm works by starting at the source and always moving along the shortest edge from the node it is currently on, then continuing from the next node in the same way until it reaches the destination. Because it always takes the cheapest edge available, the total path ends up being the shortest. Negative edge weights are a problem because the algorithm would always pick the negative edge first, which might send it in the wrong direction away from the destination.

*Why this label:* Wrong: this is a nearest-neighbor walk; Dijkstra picks the closest unvisited node by total distance from the source.

## Q10 · Operating Systems · Easy

**What is the difference between a process and a thread?**

**Q10-C1**: `correct` · 92 words

> A process is an instance of a running program with its own address space, memory, and resources like open files. A thread is a unit of execution inside a process. Threads in the same process share the heap, global data, and open files, but each thread has its own stack, registers, and program counter. Because they share memory, threads are cheaper to create and switch between and can communicate easily, but they need synchronization to avoid conflicts. Processes are isolated from each other, so one crashing usually does not bring down another.

*Why this label:* Separate vs shared address space, what each thread owns, and the cost and isolation tradeoffs.

**Q10-C2**: `correct` · 94 words

> A process is a program the operating system is running, and it gets its own protected memory space. A thread is a path of execution within a process, and one process can contain many threads. All the threads of a process share its memory and resources, while each keeps its own stack and set of registers. That makes threads lightweight and good for doing several things at once inside one application, like a browser tab loading images while responding to clicks. Processes are heavier but safer, because they cannot directly corrupt each other's memory.

*Why this label:* Same points with a browser example.

**Q10-P1**: `partial` · 76 words

> A process is a program that is running, and a thread is a smaller part of a process that runs inside it. A process can have multiple threads. The threads inside a process share memory with each other, while separate processes do not share memory. So threads are basically lighter weight versions of processes that can work together on the same task inside one program. A web browser, for example, might use several threads at once.

*Why this label:* Correct but thin: nothing about per-thread stacks and registers, or the cost and isolation tradeoffs.

**Q10-P2**: `partial` · 80 words

> A process is an independent running program with its own memory space, while a thread is a unit of execution inside a process. Each thread has its own heap and its own stack, but threads in the same process can share global variables. Threads are faster to create than processes and are good for doing several tasks at the same time in one program. Processes are more isolated, so a problem in one process does not usually affect another one.

*Why this label:* Mostly right, but threads share the heap; they do not each have their own.

**Q10-I1**: `incorrect` · 86 words

> A process is the physical core in the CPU, and a thread is the software that runs on that core. So a computer with eight cores can run eight processes, and each process can run two threads at a time because of hyperthreading. The operating system decides which thread goes on which process. That is why adding more processes to a program only helps if the computer has more cores available. This is also why a phone with fewer cores can only run a few apps.

*Why this label:* Wrong: confuses processes with CPU cores; a process is a running program, not hardware.

**Q10-I2**: `incorrect` · 89 words

> A thread is just a small process. Every thread always runs on its own separate CPU core, and threads do not share any memory with each other, which is what makes them safe to use. A process is the bigger program that starts the threads, and once the threads are running the process has no more work to do. The main difference is size, since threads are small and processes are big. So creating more threads always makes a program faster, as long as the computer has enough cores.

*Why this label:* Wrong: threads share their process's memory and do not get a dedicated core.

## Q11 · Operating Systems · Medium

**What is a race condition, and how can a mutex prevent it?**

**Q11-C1**: `correct` · 91 words

> A race condition happens when two or more threads access shared data at the same time, at least one of them writes, and the result depends on the timing. A classic example is two threads incrementing the same counter. If their read, add, and write steps interleave, both can read the same old value, so one increment is lost. A mutex prevents this by making that read, update, and write a critical section. A thread must acquire the lock before entering, only one thread can hold it, and the others wait.

*Why this label:* Definition, the lost-update counter example, and how a mutex enforces exclusive access.

**Q11-C2**: `correct` · 93 words

> A race condition is a bug where the outcome of a program depends on the unpredictable order in which threads run, usually because they share data without coordination. For example, two threads checking a bank balance and both withdrawing money could each see enough funds and overdraw the account. A mutex, short for mutual exclusion, is a lock that only one thread can hold at a time. If we lock the mutex before checking and updating the balance and unlock it afterward, the two operations cannot overlap, so the update is effectively atomic.

*Why this label:* Same concept with a bank-balance example.

**Q11-P1**: `partial` · 79 words

> A race condition is when two threads try to use the same data at the same time and the result depends on which one gets there first. A mutex is a lock that prevents this by only allowing one thread at a time to access the data. Using a mutex also makes the program run faster, because the threads no longer have to compete with each other for the data and can just take turns in an organized way.

*Why this label:* Definitions right, but no example, and the 'faster' claim is wrong: locking adds overhead.

**Q11-P2**: `partial` · 77 words

> A race condition happens when multiple threads read and write shared data at the same time and the final result depends on the timing, like two threads incrementing the same counter and losing an update. A mutex fixes this by letting only one thread enter the critical section at a time. Once you protect shared data with mutexes, your program is safe from all concurrency problems, including deadlocks, because threads can never interfere with each other again.

*Why this label:* Race and mutex are right, but mutexes do not prevent deadlocks; using them can cause deadlocks.

**Q11-I1**: `incorrect` · 81 words

> A race condition is when several threads compete for the CPU, and the operating system kills the slowest thread so the others can finish. A mutex prevents this by giving each thread a priority, so the important threads always win the race and none of them gets killed. That is why you should mark your most important threads with a mutex, so the scheduler knows to run them first. This is common in games, where the rendering thread must always win.

*Why this label:* Wrong: a race condition is about unsynchronized shared data, and a mutex is a lock, not a priority.

**Q11-I2**: `incorrect` · 81 words

> A race condition can only happen on computers with more than one core, because on a single core only one thread runs at a time. A mutex prevents it by giving each thread its own private copy of the shared variable, so they never actually touch the same memory. When the threads are done, the copies are combined. This way the threads never have to wait for each other. That is why mutexes are mainly used on servers with many cores.

*Why this label:* Wrong: races also happen on one core through preemption, and a mutex locks shared data rather than copying it.

## Q12 · Operating Systems · Hard

**What are the four necessary conditions for deadlock, and how can an operating system prevent deadlocks?**

**Q12-C1**: `correct` · 97 words

> The four Coffman conditions are mutual exclusion, where a resource can only be used by one process at a time; hold and wait, where a process holds one resource while waiting for another; no preemption, where resources cannot be taken away; and circular wait, where there is a cycle of processes each waiting for the next. A deadlock needs all four, so prevention means breaking one. For example, we can impose a global order on locks so circular wait cannot happen, or require a process to request all its resources at once to remove hold and wait.

*Why this label:* All four conditions, correctly defined, and prevention by breaking one of them.

**Q12-C2**: `correct` · 95 words

> Deadlock requires four conditions at the same time: mutual exclusion, hold and wait, no preemption, and circular wait. If any one of them is missing, deadlock cannot happen. Mutual exclusion is often impossible to remove, so systems usually attack the others. Resources can be numbered, and processes always acquire them in increasing order, which rules out a circular wait. Or the system can let a resource be preempted from a waiting process. There are also approaches beyond prevention, like the banker's algorithm for avoidance, or detecting a deadlock and then recovering by killing a process.

*Why this label:* All four conditions, two prevention strategies, plus avoidance and detection.

**Q12-P1**: `partial` · 79 words

> The conditions for deadlock are mutual exclusion, where only one process can use a resource at a time; hold and wait, where a process keeps a resource while waiting for another one; and circular wait, where processes are waiting for each other in a loop. To prevent deadlock, the operating system can make processes request resources in a fixed order, which breaks the circular wait, so the processes can never end up waiting on each other in a cycle.

*Why this label:* Prevention is right, but it lists only three conditions and misses no preemption.

**Q12-P2**: `partial` · 81 words

> The four conditions for deadlock are mutual exclusion, hold and wait, no preemption, and circular wait. When all four are true, processes can get stuck forever waiting on each other. To prevent deadlocks, the simplest thing is to add timeouts, so that if a process has been waiting too long, it just gives up and tries again later. That way nothing stays stuck permanently, and the system can keep making progress over time. Most databases and operating systems use this approach.

*Why this label:* All four conditions named, but prevention is only timeouts, which can livelock, with no condition-breaking strategy.

**Q12-I1**: `incorrect` · 77 words

> The four conditions for deadlock are starvation, race conditions, livelock, and priority inversion. When all four happen together, the system freezes. The operating system prevents deadlock by giving every process the same priority, so no process gets starved, and by running processes one at a time whenever it detects a race condition. Doing that removes the conditions, so the processes can keep running without getting stuck. This is why most operating systems use a round robin scheduler.

*Why this label:* Wrong: these are other concurrency problems, not the Coffman conditions.

**Q12-I2**: `incorrect` · 84 words

> Deadlock happens when there are more processes than CPU cores, the system runs out of memory, a process takes too long, and too many threads are created. The way an operating system prevents deadlock is by adding more cores or more memory, so that every process has its own resources. That is why deadlocks are mostly a problem on older or cheaper computers and are rare on modern servers with plenty of hardware. The way the software is written has little effect on it.

*Why this label:* Wrong: deadlock is caused by circular waiting on locked resources, not by a hardware shortage.

## Q13 · Databases · Easy

**What is the difference between a primary key and a foreign key in a relational database?**

**Q13-C1**: `correct` · 89 words · protected: customer id

> A primary key uniquely identifies each row in a table, so its values must be unique and not null, and a table has only one primary key. A foreign key is a column in one table that references the primary key of another table, and it links the two tables together. The database uses it to enforce referential integrity. For example, an orders table has a customer id foreign key pointing to the id primary key in the customers table, and many orders can share the same customer id.

*Why this label:* Uniqueness and not-null, the reference to another table, referential integrity, and an example.

**Q13-C2**: `correct` · 93 words

> The primary key is the column, or set of columns, that identifies each record in a table, and the database guarantees that it is unique and never empty. A foreign key is how one table points to another: it stores values that must match a primary key in the referenced table. Unlike a primary key, a foreign key can repeat, which is how we model one to many relationships, like many employees belonging to one department. The foreign key constraint stops us from inserting an employee with a department that does not exist.

*Why this label:* Same concept with an employees and departments example.

**Q13-P1**: `partial` · 79 words

> A primary key is a column that uniquely identifies each row in a table, like a student id. A foreign key is a column in another table that refers to that primary key, which connects the two tables together. Just like the primary key, the foreign key also has to be unique in its table, so that each row in the second table points to a different row in the first table, and you can always join them correctly.

*Why this label:* The definitions are right, but foreign keys do not have to be unique; one-to-many relies on repeats.

**Q13-P2**: `partial` · 86 words

> A primary key is the main identifier for each row in a table. It has to be unique so that no two rows are the same. A foreign key is a key that connects one table to another table by referring to a key in that other table. Both of them are important for relational databases, because they help organize the data and make it possible to combine information from different tables when you write queries. For example, they are used in almost every web application.

*Why this label:* Basically right but vague: no not-null, no referential integrity, no example.

**Q13-I1**: `incorrect` · 87 words

> A primary key is just the first column of a table, which is why it is called primary, and the database uses it to sort the table. A foreign key is a key that comes from outside the database, like an id from an external system or an API. You use a foreign key when you import data from another company or service, so you can keep track of where the data originally came from. Foreign keys are also how two databases share data with each other.

*Why this label:* Wrong: a primary key is not defined by position, and a foreign key references another table in the same database.

**Q13-I2**: `incorrect` · 81 words

> A table can have many primary keys, one for every column that you search by often, because primary keys make searching faster. A foreign key is the opposite: it is a column that is not indexed and is not used for searching. So the difference is really about performance. You mark important columns as primary keys and everything else as foreign keys, which tells the database which columns to optimize. This is why most tables end up with several primary keys.

*Why this label:* Wrong: a table has one primary key, and foreign keys are about references, not indexing.

## Q14 · Databases · Medium

**What is a database index, and how does it affect query performance and write operations?**

**Q14-C1**: `correct` · 90 words · protected: B tree

> A database index is a separate data structure, usually a B tree, that lets the database find matching rows without scanning the whole table. With an index, a lookup or range query on that column takes roughly logarithmic time instead of linear. The tradeoff is on writes. Every insert, update, or delete has to update the index too, so writes get slower, and the index takes extra storage. So I would index columns that are frequently used in where clauses or joins, and avoid adding indexes that are rarely used.

*Why this label:* The structure, faster reads, slower writes, storage cost, and when to index.

**Q14-C2**: `correct` · 95 words

> An index is like the index at the back of a book. Instead of reading every page, the database looks up the value in a sorted structure that points directly to the rows. That makes queries that filter, sort, or join on the indexed column much faster. But the index has to be kept in sync with the data, so every time a row is inserted, updated, or deleted, the database also changes the index, which slows down writes and uses more disk space. Good indexing is about choosing the columns your queries actually use.

*Why this label:* Same points using the book analogy.

**Q14-P1**: `partial` · 80 words

> A database index is a data structure that helps the database find rows faster, similar to an index in a book. Without an index, the database has to scan every row to find what you are looking for, but with an index it can jump directly to the right rows. This makes select queries with where clauses much faster, especially on large tables, so it is a good idea to add indexes on the columns you search by most often.

*Why this label:* Read speed-up is right, but it skips the write cost, which the question asks about.

**Q14-P2**: `partial` · 84 words

> A database index helps queries find rows faster by avoiding a full table scan. The way it works is that the database stores a complete sorted copy of the whole table for every index you create, so it can search that copy quickly. This makes reads faster, but it slows down inserts and updates, because the database has to change every copy of the table, and it takes a lot of extra storage space. So you should only index the columns you query often.

*Why this label:* Read and write tradeoffs are right, but an index is not a full copy of the table; it stores keys and row pointers.

**Q14-I1**: `incorrect` · 79 words

> A database index makes both reads and writes faster. Reads are faster because the database knows where each row is, and writes are faster because the index tells the database exactly where to put each new row, so it does not have to search for free space. There is really no downside besides the time it takes to create the index at first, so it is a good practice to add an index on every column of every table.

*Why this label:* Wrong: indexes slow down writes and cost storage; indexing every column is bad practice.

**Q14-I2**: `incorrect` · 80 words

> A database index is the row number of each record in a table. When you add an index to a table, the database renumbers all the rows starting from one, so that you can ask for row fifty directly. This makes queries that ask for a specific row number faster. It does not change write speed, but if you delete a row, the database has to renumber all the rows after it. Most databases do this automatically for every table.

*Why this label:* Wrong: an index is a lookup structure on column values, not row numbering.

## Q15 · Databases · Hard

**Explain the ACID properties of database transactions and why isolation levels matter when multiple transactions execute concurrently.**

**Q15-C1**: `correct` · 91 words · protected: ACID

> ACID stands for atomicity, consistency, isolation, and durability. Atomicity means a transaction happens completely or not at all. Consistency means a transaction moves the database from one valid state to another. Isolation means concurrent transactions do not see each other's partial work. Durability means once a transaction commits, it survives a crash. Isolation levels matter because full isolation is expensive. Read uncommitted allows dirty reads, read committed prevents those but allows non repeatable reads, repeatable read prevents those too, and serializable is the strictest but adds the most locking or aborts.

*Why this label:* All four properties defined, plus the isolation levels and the anomalies each one allows.

**Q15-C2**: `correct` · 84 words

> Atomicity guarantees that all the steps in a transaction succeed or none of them do. Consistency guarantees the data still follows all the rules after the transaction. Isolation guarantees that transactions running at the same time do not interfere with each other. Durability guarantees that committed changes are saved even if the server crashes. Isolation levels let us trade correctness for performance. Lower levels like read committed allow anomalies such as non repeatable reads or phantom rows, while serializable prevents them but reduces concurrency.

*Why this label:* Same content with named anomalies.

**Q15-P1**: `partial` · 82 words · protected: ACID

> ACID stands for atomicity, consistency, isolation, and durability. Atomicity means a transaction is all or nothing, consistency means the database stays valid, isolation means transactions do not interfere with each other, and durability means committed data is not lost. Isolation levels matter because higher levels are safer but slower, and lower levels are faster but less safe, so you have to choose the right level for your application. For example, a bank might pick a higher level than a social media app.

*Why this label:* ACID is right, but isolation levels are hand-waved with no anomalies or examples.

**Q15-P2**: `partial` · 84 words · protected: ACID

> ACID stands for atomicity, consistency, isolation, and durability. Atomicity means a transaction either fully completes or fully rolls back. Consistency means every copy of the database on different servers always has the same data. Isolation means running transactions do not see each other's uncommitted changes, and durability means committed data survives crashes. Isolation levels matter because weaker levels like read committed allow problems like non repeatable reads, while serializable prevents them but is slower. This is why picking the right level matters in practice.

*Why this label:* Mostly right, but it defines consistency as replica consistency, which is the distributed-systems meaning, not ACID's.

**Q15-I1**: `incorrect` · 83 words · protected: ACID

> ACID stands for availability, concurrency, integrity, and distribution. Availability means the database is always online, concurrency means many users can use it at once, integrity means the data is encrypted, and distribution means the data is spread across servers. Isolation levels matter because they decide how many servers a transaction is copied to, so higher isolation levels are safer because more servers keep a copy of the data. Most banks use the highest isolation level for this reason, even though it is slower.

*Why this label:* Wrong: the acronym and every definition are wrong, and so is the isolation-level explanation.

**Q15-I2**: `incorrect` · 84 words · protected: ACID

> ACID stands for atomicity, consistency, isolation, and durability. Isolation means each transaction runs on its own separate database server, so they physically cannot touch each other. Isolation levels control how many servers are used, so the highest level gives every transaction its own machine. This matters because if two transactions run on the same server, they will always corrupt each other's data, which is why banks use the highest isolation level. It is also the most expensive option, since it needs the most hardware.

*Why this label:* The acronym is right, but isolation and isolation levels are completely misdefined.
