# Comprehensions and Remaining Risk Drills

These questions cover a gap found after re-auditing the extracted PDFs: comprehensions are not just syntax. They are often used to test memory behavior, duplicate removal, dictionary overwrites, nested-loop order, and whether a result is built now or streamed later.

## [HIGH] 1. Loop to list comprehension: expression, loop, filter order

Source: Part 5 pp. 114-115.

Question type: convert and trace.

Rewrite the loop as one list comprehension, then give the output.

```python
z = [13, 14, 7, 12, 11, 3, 18]
out = []
for i in range(len(z)):
    if z[i] % 2 == 0:
        out.append((i, z[i]))
print(out)
```

Answer:

```python
out = [(i, z[i]) for i in range(len(z)) if z[i] % 2 == 0]
```

Output:

```text
[(1, 14), (3, 12), (6, 18)]
```

Why: a comprehension reads left to right like the loop: choose `i`, test the `if`, then build the expression `(i, z[i])`. The expression is not the loop variable; it is the value appended to the new list.

## [HIGH] 2. Comprehension reassignment does not mutate the caller's list

Source: Part 4 p. 101.

Question type: output and memory explanation.

```python
def square_rebind(items):
    items = [x * x for x in items]
    print("inside", items)

def square_mutate(items):
    for i, x in enumerate(items):
        items[i] = x * x
    print("inside", items)

a = [1, 2, 3]
square_rebind(a)
print("after rebind", a)
square_mutate(a)
print("after mutate", a)
```

Answer:

```text
inside [1, 4, 9]
after rebind [1, 2, 3]
inside [1, 4, 9]
after mutate [1, 4, 9]
```

Why: the comprehension creates a new list object and local name `items` is rebound to it. The caller's list is not changed. The second function writes into the original list object by index, so the caller sees the mutation.

## [HIGH] 3. Set comprehension removes duplicates, but order is not the point

Source: Part 5 pp. 111, 121; eight-queens diagonal test.

Question type: exact concept and possible output.

```python
nums = [1, 2, 2, 3, 3, 3]
squares = {x * x for x in nums}
print(len(squares))
print(4 in squares)
```

Answer:

```text
3
True
```

Why: `{x * x for x in nums}` is a set comprehension. The duplicate `2`s all produce `4`, but a set stores one copy. Do not depend on printed set order for exam reasoning unless the question asks only membership or length.

## [HIGH] 4. Generator expression passed to set is still consumed immediately by set

Source: Part 5 p. 121; Generators pp. 1-2.

Question type: explain syntax and trace.

```python
vec = (0, 2, 4)
col = [0, 1, 2]

a = {vec[i] + i for i in col}
b = set(vec[i] - i for i in col)

print(a)
print(b)
print(len(a), len(b))
```

Answer:

```text
{0, 3, 6}
{0, 1, 2}
3 3
```

Why: `a` uses a set comprehension. `b` passes a generator expression into `set(...)`. The generator expression is lazy by itself, but `set(...)` immediately consumes it to build a set. In the eight-queens test, this is used to check whether all diagonal values are unique.

## [HIGH] 5. Dict comprehension with duplicate keys overwrites earlier values

Source: Chart/dictionaries pp. 133, 141.

Question type: output and data-structure reasoning.

```python
portfolio = [
    ("IBM", 75),
    ("ACME", 50),
    ("IBM", 25),
]

d = {name: shares for name, shares in portfolio}
totals = {name: 0 for name, shares in portfolio}
for name, shares in portfolio:
    totals[name] += shares

print(d)
print(totals)
```

Answer:

```text
{'IBM': 25, 'ACME': 50}
{'IBM': 100, 'ACME': 50}
```

Why: dictionary keys are unique. In `d`, the second `"IBM"` overwrites the first `"IBM"`. In `totals`, the comprehension only initializes each key to `0`; the following loop accumulates both IBM rows.

## [HIGH] 6. Nested list comprehension loop order

Source: Part 5 pp. 119, 129.

Question type: trace and fill-in.

```python
pairs = [(i, j) for i in range(2) for j in range(3)]
print(pairs)
```

Answer:

```text
[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
```

Why: the comprehension is equivalent to:

```python
pairs = []
for i in range(2):
    for j in range(3):
        pairs.append((i, j))
```

The leftmost `for` is the outer loop. This matters in matrix code like `[[dot(ri, cj) for cj in zip(*B)] for ri in A]`.

## [HIGH] 7. Matrix multiplication comprehension: what is each loop doing?

Source: Part 5 pp. 128-129.

Question type: choose-correct-version.

Which version computes matrix multiplication?

```python
A = [[1, 2], [3, 4]]
B = [[10, 20], [30, 40]]

def version1(A, B):
    dot = lambda r, c: sum(r[i] * c[i] for i in range(len(r)))
    return [[dot(ri, cj) for cj in zip(*B)] for ri in A]

def version2(A, B):
    return [[A[i][j] * B[i][j] for j in range(len(B[0]))]
            for i in range(len(A))]

print(version1(A, B))
print(version2(A, B))
```

Answer:

```text
[[70, 100], [150, 220]]
[[10, 40], [90, 160]]
```

Why: matrix multiplication uses row-column dot products, so `version1` is correct. `zip(*B)` turns B's columns into tuples. `version2` only multiplies matching positions element-by-element.

## [MID] 8. List comprehension can hide an IndexError

Source: Part 5 pp. 113-118.

Question type: exact error and fix.

```python
x = [[1, 2], [3, 4], [5]]
col1 = [row[1] for row in x]
print(col1)
```

Answer:

```text
IndexError: list index out of range
```

Fix if you only want rows that have column 1:

```python
col1 = [row[1] for row in x if len(row) > 1]
```

Why: the comprehension is still normal indexing. It does not skip bad rows unless you explicitly add an `if` filter.

## [HIGH] 9. Comprehension scope does not leak the loop variable

Source: Part 4 scoping pp. 84-87; Part 5 comprehension syntax.

Question type: output and scope explanation.

```python
i = 100
nums = [i * 2 for i in range(3)]
print(nums)
print(i)
```

Answer in Python 3:

```text
[0, 2, 4]
100
```

Why: in Python 3, the comprehension's loop variable has its own local comprehension scope. It does not overwrite the outer `i`. This is still LEGB thinking: names are resolved by scope, not indentation alone.

## [MID] 10. Deep-copy logic with list, dict, and set comprehensions

Source: Part 4 pp. 87-88.

Question type: implement and explain.

Complete the recursive copy function so lists, dicts, and sets do not share nested mutable objects.

```python
def deep_copy(obj):
    if isinstance(obj, list):
        return __________________________
    if isinstance(obj, dict):
        return __________________________
    if isinstance(obj, set):
        return __________________________
    return obj

data = {"a": [[1]], "b": {2, 3}}
copy_data = deep_copy(data)
copy_data["a"][0].append(99)
copy_data["b"].add(4)
print(data)
print(copy_data)
```

Answer:

```python
def deep_copy(obj):
    if isinstance(obj, list):
        return [deep_copy(item) for item in obj]
    if isinstance(obj, dict):
        return {deep_copy(key): deep_copy(value) for key, value in obj.items()}
    if isinstance(obj, set):
        return {deep_copy(item) for item in obj}
    return obj
```

Output:

```text
{'a': [[1]], 'b': {2, 3}}
{'a': [[1, 99]], 'b': {2, 3, 4}}
```

Why: each comprehension builds a new container. Recursing into each element prevents nested lists/dicts/sets from being shared.

## [MID] 11. Decorated calls inside a comprehension still call the wrapper each time

Source: Decorators pp. 7-10; countcalls dictionary.

Question type: output/state trace.

```python
calls = {}

def countcalls(d):
    def deco(func):
        def wrapper(*args, **kwargs):
            d[func.__name__] = d.get(func.__name__, 0) + 1
            return func(*args, **kwargs)
        return wrapper
    return deco

@countcalls(calls)
def add(a, b):
    return a + b

values = [add(i, i) for i in range(3)]
print(values)
print(calls)
```

Answer:

```text
[0, 2, 4]
{'add': 3}
```

Why: the list comprehension calls `add(i, i)` three times. The name `add` points to the wrapper, so the wrapper updates the shared dictionary on every iteration.

## [LOW] 12. Comprehension vs map/filter is mostly style here

Source: Part 5 list comprehension intro; chart data cleaning.

Question type: choose clearer version.

```python
words = ["cat,", "dog.", "bird"]
a = [w.strip(".,;") for w in words]
b = list(map(lambda w: w.strip(".,;"), words))
print(a)
print(b)
```

Answer:

```text
['cat', 'dog', 'bird']
['cat', 'dog', 'bird']
```

Why: both produce the same list. For this class, the comprehension is usually clearer because the expression, loop source, and optional filter are visible in one place.
