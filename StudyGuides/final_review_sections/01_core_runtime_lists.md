# Core Runtime + Lists: Last-Hour Review

Use this as a memory checklist. Most exam traps reduce to one question:
did this line rebind a name, or mutate an existing object?

## 1. Names, References, Mutation

| Code shape | What happens | Remember |
|---|---|---|
| `b = a` | `b` and `a` point to the same object | Alias, not copy |
| `a = a + [4]` | New list, name `a` rebound | Old aliases do not see it |
| `a += [4]` | Usually mutates list in place | Aliases see it |
| `a.append(4)` | Mutates same list | Returns `None` |
| `a[0] = 9` | Mutates same list | Aliases see it |
| `del a` | Deletes the name `a` | Object may still exist |
| `del a[0]` | Deletes list item | Later items shift left |
| `a.clear()` | Empties the same list object | Aliases see `[]` |

Tiny trace:

```python
a = [1, 2]
b = a
a.append(3)
a = [9]
print(b)   # [1, 2, 3]
```

Function parameters are local names bound to the passed objects. Mutating the
object affects the caller; rebinding the parameter does not.

```python
def f(x):
    x.append(4)   # caller sees this
    x = [0]       # only local x changes
```

## 2. List Methods: Return Values and Errors

| Method | Mutates list? | Return value | Trap |
|---|---:|---|---|
| `s.append(x)` | Yes | `None` | Adds `x` as one object |
| `s.extend(t)` | Yes | `None` | Iterates through `t` and adds each item |
| `s.insert(i, x)` | Yes | `None` | Inserts before index `i` |
| `s.remove(x)` | Yes | `None` | Removes first equal value; `ValueError` if absent |
| `s.pop()` | Yes | Removed last item | `IndexError` if empty |
| `s.pop(i)` | Yes | Removed item at `i` | Later items shift left |
| `s.index(x)` | No | First index of `x` | `ValueError` if absent |
| `s.count(x)` | No | Number of matches | Safe if absent, returns `0` |
| `s.reverse()` | Yes | `None` | In-place |
| `s.sort()` | Yes | `None` | In-place, stable |
| `sorted(s)` | No | New sorted list | Works on any iterable |
| `list(s)` | No | New outer list | Shallow copy if `s` has nested mutables |

Never write:

```python
x = [3, 1, 2]
y = x.sort()
print(y)       # None
```

## 3. Append vs Extend

| Code | Result |
|---|---|
| `a = [1]; a.append([2, 3])` | `[1, [2, 3]]` |
| `a = [1]; a.extend([2, 3])` | `[1, 2, 3]` |
| `a = [1]; a += [2, 3]` | `[1, 2, 3]` |
| `a = [1]; a.append("hi")` | `[1, "hi"]` |
| `a = [1]; a.extend("hi")` | `[1, "h", "i"]` |

`+` needs two lists. `extend()` accepts any iterable.

## 4. Slicing and Slice Mutation

| Form | Meaning |
|---|---|
| `s[i:j]` | New list from `i` up to, not including, `j` |
| `s[:j]` | From start to `j` |
| `s[i:]` | From `i` to end |
| `s[:]` | Shallow copy of outer list |
| `s[i:j:k]` | Extended slice with stride `k` |
| `s[i:j] = t` | Replace that slice; length may change |
| `s[i:j:k] = t` | Strided replacement; lengths must match |
| `del s[i:j]` | Delete a slice |
| `del s[i:j:k]` | Delete strided positions |

Tiny examples:

```python
a = [0, 1, 2, 3, 4]
a[1:3] = ["x", "y", "z"]
print(a)        # [0, 'x', 'y', 'z', 3, 4]

b = [0, 1, 2, 3, 4, 5]
b[::2] = [9, 8, 7]
print(b)        # [9, 1, 8, 3, 7, 5]
```

This fails because `b[::2]` selects 3 positions but the right side has 2:

```python
b[::2] = [9, 8]     # ValueError
```

Deleting positions shifts later elements left. This matters inside loops.

## 5. Loops While Mutating Lists

The `for` loop walks the same list object by index. It does not copy the list.

| Mutation during loop | Risk |
|---|---|
| `remove`, `pop`, `del` | Items shift left; loop may skip elements |
| `append` | New items may be visited |
| Rebinding loop variable | Does not change the list |
| Mutating object referenced by loop variable | Changes the nested object |

Classic skip:

```python
nums = [1, 2, 2, 2, 3]
for x in nums:
    if x == 2:
        nums.remove(x)
print(nums)     # [1, 2, 3]
```

Safer patterns:

```python
# build a new list
nums = [x for x in nums if x != 2]

# or mutate by index from right to left
for i in range(len(nums) - 1, -1, -1):
    if nums[i] == 2:
        del nums[i]
```

Loop variable trap:

```python
rows = [[1], [2]]
for row in rows:
    row.append(0)   # mutates inner list
    row = []        # only rebinds local loop name
print(rows)         # [[1, 0], [2, 0]]
```

## 6. Copying: Alias, Shallow, Deep

| Code | New outer object? | Nested objects copied? |
|---|---:|---:|
| `b = a` | No | No |
| `b = a[:]` | Yes | No |
| `b = list(a)` | Yes | No |
| `b = a.copy()` | Yes | No |
| `copy.copy(a)` | Yes | No |
| `copy.deepcopy(a)` | Yes | Yes |

Tiny trace:

```python
import copy

a = [[1], [2]]
b = a[:]
c = copy.deepcopy(a)
b[0].append(9)
c[1].append(8)
print(a)   # [[1, 9], [2]]
print(b)   # [[1, 9], [2]]
print(c)   # [[1], [2, 8]]
```

2D list multiplication trap:

```python
grid = [[0] * 3] * 3
grid[0][0] = 9
print(grid)  # all rows changed
```

Correct pattern:

```python
grid = [[0] * 3 for _ in range(3)]
```

## 7. Sorting Reminders

| Need | Use |
|---|---|
| Change the list itself | `a.sort()` |
| Keep original list | `sorted(a)` |
| Reverse order | `reverse=True` |
| Case-insensitive strings | `key=str.lower` |
| Sort records by field | `key=lambda row: row[2]` or `itemgetter(2)` |

Facts to remember:

- `list.sort()` and `sorted()` are stable.
- Stable means equal keys keep their original relative order.
- Python uses Timsort: adaptive, stable, good on partially sorted data.
- The `key` function is called once per item and returns the comparison key.

Manual sort sketches:

| Sort | Core idea | Exam reminder |
|---|---|---|
| Selection sort | Repeatedly find min in unsorted suffix and swap to front | Usually in-place, simple, `O(n^2)` |
| Insertion sort | Insert each new item into already-sorted prefix | Stable if equal items are not moved past each other |
| Merge sort | Split, sort halves, merge | Stable, `O(n log n)`, needs extra space |

Selection-sort pattern:

```python
for i in range(len(a) - 1):
    pos = i
    for j in range(i, len(a)):
        if a[j] < a[pos]:
            pos = j
    a[i], a[pos] = a[pos], a[i]
```

## 8. Random, Sieve, Monte Carlo

Random basics:

| Function | Returns |
|---|---|
| `random()` | Float `0.0 <= x < 1.0` |
| `randint(a, b)` | Integer `a <= x <= b` |

Use `from random import random, randint` or `import random`, but remember name
collisions: assigning `random = 5` shadows the imported function name.

Sieve of Eratosthenes:

```python
n = 101
sieve = [True] * n
sieve[0] = sieve[1] = False

for i in range(2, int(n ** 0.5) + 1):
    if sieve[i]:
        for j in range(i * i, n, i):
            sieve[j] = False

primes = [i for i in range(n) if sieve[i]]
```

Must remember:

- Boolean list says whether each index is still possibly prime.
- Set `0` and `1` to `False`.
- Only need outer loop through `sqrt(n)`.
- Start crossing off at `i*i`; smaller multiples were handled earlier.

Monte Carlo pi:

```python
from math import sqrt
from random import random

count = 0
trials = 1000000
for _ in range(trials):
    x = random()
    y = random()
    if sqrt(x * x + y * y) < 1:
        count += 1

print(4 * count / trials)
```

Why it works: random points in the unit square; the quarter circle area is
`pi / 4`, so the inside fraction times `4` estimates `pi`.

## 9. Last-Minute Traps

- Draw arrows: names point to objects.
- Assignment rebinds names; list methods usually mutate objects.
- If a method mutates in place, expect return value `None`.
- `append` adds one object; `extend` opens an iterable.
- `index` and `remove` fail if the value is absent; check `x in s` first.
- `pop` returns the removed value; `remove` does not.
- `a[:]` copies only the outer list.
- Slice assignment without stride can change length.
- Strided slice assignment must replace exactly the selected count.
- Do not delete from the front of a list while looping forward through it.
- `[[0] * n] * m` shares one row; use a comprehension for 2D lists.
- `sorted(a)` returns a new list; `a.sort()` mutates and returns `None`.
- Builtin names are not reserved: `sum = 0` breaks later `sum(...)`.
