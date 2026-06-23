# Part 5 Additions: Sets, Matrix Logic, DP, and Unpacking

These are new Part 5 practice questions meant to fill gaps not already covered by the current functions/references drill. Source page references use the Part 5 PDF's printed page number when visible, with the extracted page in parentheses.

## Questions

### [HIGH] 1. Set methods: exact output and exact errors

Source: Part 5 PDF p. 111 (extracted page 2).

```python
s = {1, 2, 3}
t = {3, 4}
print(sorted(s & t))
print(sorted(s | t))
print(sorted(s - t))
print(s.remove(2))
print(2 in s, len(s))
print(s.discard(9))
print(9 in s, len(s))
s.remove(9)
print("done")
```

What is the exact output/error? Then answer: if the last `remove` is replaced by `s.pop()` after `s.clear()`, what error is raised?

Answer:

```text
[3]
[1, 2, 3, 4]
[1, 2]
None
False 2
None
False 2
KeyError: 9
```

After `s.clear(); s.pop()`, Python raises:

```text
KeyError: 'pop from an empty set'
```

Set algebra creates new sets: `&` is intersection, `|` is union, and `-` is difference. `remove` requires the element to exist. `discard` is silent when the element is absent. `pop` removes an arbitrary element, so only use it when any element is acceptable; on an empty set it raises `KeyError`.

### [HIGH] 2. Unique random table: choose the correct version

Source: Part 5 PDF pp. 110-112 (extracted pages 1-3).

We need an `n` by `m` table filled with `n*m` unique random integers in `1..k`, and `k > n*m`. Which version is correct?

```python
# A
x = []
seen = set()
for i in range(n):
    row = []
    for j in range(m):
        r = randint(1, k)
        while r in seen:
            r = randint(1, k)
        seen.add(r)
        row.append(r)
    x.append(row)

# B
x = []
seen = set()
for i in range(n):
    row = []
    for j in range(m):
        r = randint(1, k)
        if r not in seen:
            seen.add(r)
            row.append(r)
    x.append(row)
```

Answer: A is correct. B can make short rows because a duplicate simply gets skipped and the inner `for` still moves to the next column.

Performance note: A is usually fine when `k` is much larger than `n*m`, but slows as the set fills because collisions cause repeated random draws. A deterministic high-performance version is:

```python
nums = list(range(1, k + 1))
shuffle(nums)
x = [nums[i*m:(i+1)*m] for i in range(n)]
```

That uses more memory for `nums`, but it avoids repeated rejection attempts.

### [HIGH] 3. Matrix list comprehensions: column, diagonals, and dot product

Source: Part 5 PDF pp. 113-118 (extracted pages 4-8).

Trace the output.

```python
x = [
    [3, 1, 4],
    [1, 5, 9],
    [2, 6, 5],
]

col1 = [x[j][1] for j in range(len(x))]
d1 = sum(x[i][i] for i in range(len(x)))
d2 = sum(x[i][len(x) - 1 - i] for i in range(len(x)))
dot = sum(x[0][i] * col1[i] for i in range(len(x)))

print(col1)
print(d1, d2, d1 - d2)
print(dot)
```

Answer:

```text
[1, 5, 6]
13 11 2
32
```

The anti-diagonal index is `len(x) - 1 - i`, not `len(x) - i`. The dot product pairs positions: `3*1 + 1*5 + 4*6`.

### [HIGH] 4. Digit-list integers: implement `make_int` and trace `int_add`

Source: Part 5 PDF pp. 118-119 (extracted pages 8-9).

Implement `make_int(x)` so `"907"` becomes `[9, 0, 7]`. Then trace the output of this addition logic:

```python
def make_int(x):
    return [int(ch) for ch in x]

def int_add(x, y):
    if len(x) < len(y):
        x = [0] * (len(y) - len(x)) + x
    if len(y) < len(x):
        y = [0] * (len(x) - len(y)) + y

    carry = 0
    out = []
    for i in range(len(x) - 1, -1, -1):
        total = x[i] + y[i] + carry
        out.append(total % 10)
        carry = total // 10
    if carry:
        out.append(carry)
    return out[::-1]

a = make_int("999")
b = make_int("7")
print(a, b)
print(int_add(a, b))
print(a, b)
```

Answer:

```text
[9, 9, 9] [7]
[1, 0, 0, 6]
[9, 9, 9] [7]
```

The shorter list is padded by rebinding local names `x` or `y`, not by mutating `a` or `b`. The result grows by one digit because the final carry remains after the leftmost column.

### [HIGH] 5. Matrix multiply: choose the correct design

Source: Part 5 PDF pp. 119, 128-131 (extracted pages 9, 20-23).

First, implement `matrix_add(X, Y)` for same-size square matrices. Then choose which `matrix_mult` implementation matches the definition "row of A dot column of B".

Answer for addition:

```python
def matrix_add(X, Y):
    return [[X[i][j] + Y[i][j] for j in range(len(X))]
            for i in range(len(X))]
```

```python
# A
def matrix_mult(A, B):
    dot = lambda r, c: sum(r[i] * c[i] for i in range(len(r)))
    return [[dot(ri, cj) for cj in zip(*B)] for ri in A]

# B
def matrix_mult(A, B):
    return [[A[i][j] * B[i][j] for j in range(len(B[0]))]
            for i in range(len(A))]
```

Then trace version A:

```python
A = [[1, 2, 3],
     [4, 5, 6]]
B = [[7, 8],
     [9, 10],
     [11, 12]]
print(matrix_mult(A, B))
print(list(zip(*B)))
```

Answer:

```text
[[58, 64], [139, 154]]
[(7, 9, 11), (8, 10, 12)]
```

A is correct. B is element-by-element multiplication, not matrix multiplication. `zip(*B)` turns B's columns into tuples, so each output cell is one dot product.

### [MID] 6. Saddle point: implement and explain the scan

Source: Part 5 PDF p. 119 (extracted page 10).

A saddle point is the minimum in its row and maximum in its column. Implement `saddle(x)` returning `(value, row, col)` or `"not found"`. Then give the result for the table below.

```python
x = [
    [4, 2, 5],
    [3, 1, 6],
    [7, 0, 8],
]
```

Answer:

```python
def saddle(x):
    n = len(x)
    for i in range(n):
        row_min = min(x[i])
        for j in range(n):
            if x[i][j] == row_min:
                col = [x[r][j] for r in range(n)]
                if x[i][j] == max(col):
                    return (x[i][j], i, j)
    return "not found"
```

Result:

```text
(2, 0, 1)
```

`2` is the smallest value in row `0`, and column `1` is `[2, 1, 0]`, so `2` is also the largest value in that column.

### [HIGH] 7. Robot paths: DP table versus recursion

Source: Part 5 PDF pp. 120-121 (extracted page 11).

For an `n` by `n` grid, a robot starts at upper left and can only move right or down. Trace the printed table and result for `n = 4`.

```python
n = 4
a = [[0] * n for _ in range(n)]
for i in range(n):
    a[i][0] = 1
    a[0][i] = 1
for i in range(1, n):
    for j in range(1, n):
        a[i][j] = a[i - 1][j] + a[i][j - 1]
print(a)
print(a[n - 1][n - 1])
```

Answer:

```text
[[1, 1, 1, 1], [1, 2, 3, 4], [1, 3, 6, 10], [1, 4, 10, 20]]
20
```

Each cell counts paths from above plus paths from the left. The plain recursive version computes the same recurrence, but repeats subproblems many times. The DP table stores each subproblem once, so it is much faster and also shows the intermediate counts.

### [HIGH] 8. Base-8 generation, permutations, and diagonal sets

Source: Part 5 PDF pp. 120-122 (extracted pages 12-14).

Part A: Write `get_num(n)` returning the 8-digit base-8 representation of decimal `n` as a list of digits. Trace `get_num(65)`.

Part B: Explain why this eight queens test finds diagonal conflicts:

```python
col = [0,1,2,3,4,5,6,7]
8 == len(set(vec[i] + i for i in col)) == len(set(vec[i] - i for i in col))
```

Answer:

```python
def get_num(n):
    out = [0] * 8
    for i in range(7, -1, -1):
        out[i] = n % 8
        n //= 8
    return out
```

```text
get_num(65) -> [0, 0, 0, 0, 0, 1, 0, 1]
```

For queens, a permutation already guarantees one queen per row and one per column if `i` is the row and `vec[i]` is the column. Queens share one diagonal when `row + col` matches, and they share the other diagonal when `col - row` matches. The two sets must both have length `8`; any duplicate means a diagonal conflict.

### [MID] 9. Starred and nested unpacking: trace and exact error

Source: Part 5 PDF pp. 123-126 (extracted pages 15-18).

Trace the output/error.

```python
a, *body, c = range(5)
print(a, body, c)

record = ("Tokyo", "JP", 36.933, (35.689722, 139.691667))
name, _, pop, (lat, lon) = record
print(name, pop, round(lon, 2))

x, *mid, y, z = [10, 20]
print(x, mid, y, z)
```

Answer:

```text
0 [1, 2, 3] 4
Tokyo 36.933 139.69
ValueError: not enough values to unpack (expected at least 3, got 2)
```

The starred target collects excess items into a list, but the non-starred targets still need enough values. In the last assignment, `x`, `y`, and `z` require three values before `mid` can collect extras.

### [MID] 10. `zip(*B)` transpose and `dict(zip(keys, values))`

Source: Part 5 PDF pp. 127-129 (extracted pages 19-21).

Trace the output.

```python
B = [[1, 2, 3],
     [4, 5, 6]]
print(list(zip(*B)))
print([list(group) for group in zip(*B)])

keys = ["a", "b", "c"]
values = [10, 20]
print(dict(zip(keys, values)))
```

Answer:

```text
[(1, 4), (2, 5), (3, 6)]
[[1, 4], [2, 5], [3, 6]]
{'a': 10, 'b': 20}
```

`zip(*B)` passes each row as a separate argument to `zip`, so it groups column positions. `zip` produces tuples and stops at the shortest input; that is why key `"c"` is dropped when building the dictionary.
