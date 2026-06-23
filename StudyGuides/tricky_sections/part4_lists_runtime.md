# Part 4 Tricky Drill: Lists, References, Runtime, and Output Tracing

Use this section for professor-style output prediction. The main rule: names point to objects. Assignment changes a name binding; mutation changes the object.

## Trap Checklist

- `b = a` makes an alias, not a copy.
- `a[:]`, `list(a)`, and `copy.copy(a)` copy the outer list only.
- `copy.deepcopy(a)` copies nested mutable objects too.
- `list.sort()` and `list.reverse()` mutate and return `None`; `sorted(a)` returns a new list.
- `append(x)` adds one object; `extend(x)` iterates over `x` and adds each element.
- A `for` loop over a list keeps using the same list object even if you mutate it.
- Removing while iterating can skip elements because later items shift left.
- Appending while iterating can make the loop visit appended items.
- `del name` deletes a name; `del a[i]` deletes a list element; `a.clear()` mutates the list object.
- `[[0] * n] * m` repeats the same row reference.
- Normal slice assignment can change length; strided slice assignment must match the exact number of selected positions.
- Mutable default arguments are created once, when `def` runs.
- If a function assigns to a name anywhere in its body, that name is local unless declared `global` or `nonlocal`.
- Function call arguments are evaluated before the function body runs.
- Tuple assignment like `a, b = b, a` loads the right side before storing the left side.

## Questions

### 1. Mutate, Alias, Then Rebind

```python
def touch(x):
    x.append(4)
    y = x
    x = x + [5]
    y[0] = 99
    print("inside", x, y)

a = [1, 2, 3]
touch(a)
print("outside", a)
```

Output:

```text
inside [1, 2, 3, 4, 5] [99, 2, 3, 4]
outside [99, 2, 3, 4]
```

Behind the scenes: `x` first points to the same list as `a`, so `append(4)` mutates `a`'s list. `y = x` makes another alias. `x = x + [5]` creates a new list and rebinds only local name `x`. `y[0] = 99` mutates the original list, so `a` sees it.

### 2. Shallow Copy and Wrapper List

```python
a = [[1], [2]]
b = a[:]
c = [a]
b[0].append(10)
b.append([3])
a[1] = ["X"]
print(a)
print(b)
print(c)
```

Output:

```text
[[1, 10], ['X']]
[[1, 10], [2], [3]]
[[[1, 10], ['X']]]
```

Behind the scenes: `b = a[:]` makes a new outer list but shares the original inner lists. `b[0].append(10)` mutates the shared inner list. `b.append([3])` changes only `b`'s outer list. `a[1] = ["X"]` replaces an element in `a`'s outer list; `b` still points to the old `[2]`. `c = [a]` stores a reference to the whole `a` list, so it reflects `a`'s current outer contents.

### 3. 2D List Multiplication Alias

```python
grid = [[0] * 3] * 3
grid[0].append(5)
grid[1][0] = 9
print(grid)
print(grid[0] is grid[2])
```

Output:

```text
[[9, 0, 0, 5], [9, 0, 0, 5], [9, 0, 0, 5]]
True
```

Behind the scenes: `[0] * 3` creates one row. The outer `* 3` repeats that same row reference three times. Appending through row 0 and assigning through row 1 both mutate the same row object.

### 4. Strided Slice Assignment

```python
a = [0, 1, 2, 3, 4, 5]
a[1:5:2] = ["a", "b"]
print(a)
a[::2] = [7, 8]
print(a)
```

Error after the first print:

```text
[0, 'a', 2, 'b', 4, 5]
ValueError: attempt to assign sequence of size 2 to extended slice of size 3
```

Behind the scenes: `a[1:5:2]` selects indices 1 and 3, so two replacement values are allowed. After that, `a[::2]` selects indices 0, 2, and 4. A strided slice cannot change length, so two replacement values for three slots raises `ValueError`.

### 5. Loop Variable Is Only a Name

```python
a = [[1], [2], [3]]
for row in a:
    row.append(0)
    row = ["gone"]
print(a)

for row in a:
    del row
print(a)
```

Output:

```text
[[1, 0], [2, 0], [3, 0]]
[[1, 0], [2, 0], [3, 0]]
```

Behind the scenes: during each iteration, `row` is a temporary name pointing at one inner list. `row.append(0)` mutates that inner list. `row = ["gone"]` only rebinds the loop variable. `del row` deletes the loop variable name, not the element stored inside `a`.

### 6. Removing While Iterating

```python
nums = [1, 2, 2, 2, 3]
for x in nums:
    if x == 2:
        nums.remove(x)
print(nums)
```

Output:

```text
[1, 2, 3]
```

Behind the scenes: the loop has an internal index. When the first `2` is removed, later elements shift left, but the loop advances to the next index. That skips over a `2`. The same skip happens again, leaving one `2`.

### 7. Appending While Iterating

```python
nums = [1, 2, 3]
for x in nums:
    print(x)
    if x < 3:
        nums.append(x + 10)
print(nums)
```

Output:

```text
1
2
3
11
12
[1, 2, 3, 11, 12]
```

Behind the scenes: the loop is walking the same list object. Values appended before the loop reaches the end can also be visited. The guard `x < 3` prevents an infinite pattern here because `11` and `12` do not append more values.

### 8. Mutable Default Value

```python
def add_tag(tag, bucket=[]):
    bucket.append([tag])
    return bucket

x = add_tag("a")
y = add_tag("b")
y[0].append("A")
z = add_tag("c", [])
print(x)
print(y)
print(z)
```

Output:

```text
[['a', 'A'], ['b']]
[['a', 'A'], ['b']]
[['c']]
```

Behind the scenes: the default `bucket` list is created once when Python executes the `def`. Calls that omit `bucket` share it, so `x` and `y` point to the same default list. The explicit `[]` in the third call is a fresh list.

### 9. Scope: Assignment Makes the Name Local

```python
xs = [1, 2]

def f():
    xs.append(3)
    xs = [9]
    return xs

f()
print(xs)
```

Error:

```text
UnboundLocalError: local variable 'xs' referenced before assignment
```

Behind the scenes: because `xs = [9]` appears inside `f`, Python treats `xs` as a local variable for the whole function. The earlier `xs.append(3)` tries to read that local before it has been assigned. The global `xs` is not used.

### 10. `sorted()` vs `sort()`

```python
words = ["bbb", "A", "cc"]
r1 = sorted(words, key=len)
r2 = words.sort(key=str.lower)
print(r1)
print(words)
print(r2)
```

Output:

```text
['A', 'cc', 'bbb']
['A', 'bbb', 'cc']
None
```

Behind the scenes: `sorted(words, key=len)` returns a new list and leaves `words` alone. `words.sort(key=str.lower)` mutates `words` in place and returns `None`. The key function controls comparison, not the values returned in the list.

### 11. Nested Loop 2D Trace

```python
mat = [[1, 2, 3], [4, 5], [6, 7, 8]]
diag = []
for i in range(len(mat)):
    for j in range(len(mat[i])):
        if i == j:
            diag.append(mat[i][j])
print(diag)
print(sum(diag))
```

Output:

```text
[1, 5, 8]
14
```

Behind the scenes: `len(mat[i])` uses the current row length, so uneven row sizes are handled. The diagonal condition `i == j` selects `mat[0][0]`, `mat[1][1]`, and `mat[2][2]`. `diag` stores those integer objects, and `sum(diag)` adds them.

### 12. Function Arguments Evaluate Before the Call Finishes

```python
def bump(L):
    L.append(len(L))
    return L[-1]

a = [10]
print(bump(a), bump(a), a)
```

Output:

```text
1 2 [10, 1, 2]
```

Behind the scenes: `print` arguments are evaluated left to right. The first `bump(a)` sees length 1, appends `1`, and returns `1`. The second sees the already-mutated list length 2, appends `2`, and returns `2`. Then `print` receives the final same list object.

### 13. Tuple Assignment and the Runtime Stack

```python
a = [1]
b = [2]
a, b = b, a
a.append(9)
print(a)
print(b)
```

Output:

```text
[2, 9]
[1]
```

Behind the scenes: for `a, b = b, a`, Python loads the right-side object references before storing into the left-side names. No source-level temporary variable is needed because the runtime stack temporarily holds the old references. After the swap, `a` points to the old `[2]` list and `b` points to the old `[1]` list.

### 14. `del` Name vs `clear()` Object

```python
a = [1, 2]
b = a
c = [a, a[:]]
del a
b.clear()
print(b)
print(c)
```

Output:

```text
[]
[[], [1, 2]]
```

Behind the scenes: `del a` removes only the name `a`; the original list still exists because `b` and `c[0]` reference it. `b.clear()` mutates that original list to empty. `a[:]` made a separate outer list copy for `c[1]`, so it remains `[1, 2]`.

### 15. Shallow Copy vs Deep Copy

```python
import copy

original = [[1], {"k": [2]}]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow[0].append(9)
shallow[1]["k"].append(3)
deep[0].append(8)
deep[1]["k"].append(4)

print(original)
print(shallow)
print(deep)
```

Output:

```text
[[1, 9], {'k': [2, 3]}]
[[1, 9], {'k': [2, 3]}]
[[1, 8], {'k': [2, 4]}]
```

Behind the scenes: `copy.copy(original)` creates a new outer list but shares the inner list and dictionary, including the dictionary's inner list. Mutating through `shallow` affects `original`. `copy.deepcopy(original)` recursively copies the nested mutable objects, so mutations through `deep` stay separate.
