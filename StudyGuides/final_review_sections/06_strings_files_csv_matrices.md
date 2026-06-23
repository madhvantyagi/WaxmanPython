# 06 - Strings, Files, CSV, Matrices

Last-hour goal: know the exact return values, what mutates, what stays an iterator,
and the one-line formulas for rows, columns, diagonals, transpose, and matrix multiply.

## Strings

Strings are immutable. Every string method below returns a new string/list; it does
not change the original.

```python
s = "cat"
# s[0] = "b"        # TypeError
s = "b" + s[1:]     # "bat"
```

### Split family

```python
"  a  b  ".split()       # ["a", "b"]        whitespace grouped
"1,,2".split(",")        # ["1", "", "2"]   explicit sep keeps empties
"a=b=c".split("=", 1)    # ["a", "b=c"]
"".split(",")            # [""]
"   ".split()            # []
```

`splitlines()` breaks on `\n`, `\r`, and `\r\n`.

```python
"a\nb\r\nc".splitlines()       # ["a", "b", "c"]
"a\nb".splitlines(True)        # ["a\n", "b"]
```

### Strip family

`strip(chars)` removes any combination of those characters from the ends. `chars`
is not a suffix.

```python
"...cat,;".strip(".,;")     # "cat"
"...cat,;".lstrip(".,;")    # "cat,;"
"...cat,;".rstrip(".,;")    # "...cat"
"mississippi".strip("im")   # "ssissipp"
```

Punctuation cleanup:

```python
words = ["cat,", ".dog;", "b;ir,d"]
[w.rstrip(".,;") for w in words]                 # end only
[w.strip(".,;") for w in words]                  # both ends
["".join(ch for ch in w if ch not in ".,;") for w in words]  # anywhere
```

### Search, count, replace, join

```python
s = "banana"
s.find("na")          # 2
s.find("x")           # -1
s.count("na")         # 2, non-overlapping
s.replace("na", "NA", 1)  # "baNAna"
",".join(["a", "b"])  # "a,b"
"".join(reversed("abc"))  # "cba"
```

`join` is called on the separator, and every item must already be a string.

```python
"-".join(map(str, [1, 2, 3]))   # "1-2-3"
```

### Reversing strings

```python
def rev1(s):
    return s[::-1]

def rev2(s):
    out = ""
    for ch in s:
        out = ch + out
    return out

def rev3(s):
    return "".join(reversed(s))
```

## Files

Use `with open(...) as f:` so the file closes automatically.

```python
with open("data.txt") as f:
    for line in f:
        print(line, end="")   # line already usually has "\n"
```

### Read methods

```python
f.read()        # whole remaining file as one string; "" at EOF
f.read(100)     # next 100 chars, or fewer at EOF
f.readline()    # next line as string, usually including "\n"
f.readlines()   # list of remaining lines, each usually with "\n"
for line in f:  # memory-friendly line iteration
    ...
```

File objects remember their position.

```python
with open("data.txt") as f:
    a = f.read()
    b = f.read()     # "" because already at EOF
    f.seek(0)
    c = f.readline()
```

Newline traps:

```python
line = "Bob 78 90\n"
line.split()          # ["Bob", "78", "90"]  removes whitespace
line.rstrip("\n")     # "Bob 78 90"
"a\nb\n".splitlines() # ["a", "b"]
```

Writing:

```python
with open("out.txt", "w") as out:
    print("hello", file=out)
    out.write("bye\n")
```

## CSV

`csv.reader` returns rows as lists of strings. Convert numbers yourself.

```python
import csv

with open("scores.csv", newline="") as f:
    rows = csv.reader(f)
    next(rows)              # skip header
    for row in rows:
        name = row[0]
        scores = [float(x) for x in row[1:] if x]
        print(name, sum(scores) / len(scores))
```

Tiny grade-bin pattern:

```python
grades = ["10", "", "0", "10.5", "100"]
positive = [float(g) for g in grades if g and float(g) > 0]

for lo in range(1, 101, 10):
    count = sum(1 for x in positive if lo <= x < lo + 10)
    if count:
        print(f"{lo}-{lo + 9}: {count}")
```

Output:

```text
1-10: 2
91-100: 1
```

Reason: intervals are half-open. `1 <= x < 11`, so `10.5` is still in `1-10`.

When writing CSV on Windows/macOS/Linux, use `newline=""`.

```python
with open("out.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "score"])
```

## Matrices

A matrix is a list of row lists: `x[row][col]`.

```python
x = [
    [3, 1, 4],
    [1, 5, 9],
    [2, 6, 5],
]
```

### Row, column, diagonals

```python
row0 = x[0]                               # reference to original row
row0_copy = [x[0][j] for j in range(len(x[0]))]
col1 = [x[i][1] for i in range(len(x))]   # [1, 5, 6]

d1 = sum(x[i][i] for i in range(len(x)))              # main diagonal
d2 = sum(x[i][len(x) - 1 - i] for i in range(len(x))) # anti-diagonal
```

Trap: anti-diagonal index is `len(x) - 1 - i`, not `len(x) - i`.

### Dot product

```python
def dot(a, b):
    return sum(a[i] * b[i] for i in range(len(a)))

dot([1, 2, 3], [10, 11, 12])  # 68
```

### Transpose with zip

```python
B = [[1, 2, 3],
     [4, 5, 6]]

list(zip(*B))                         # [(1, 4), (2, 5), (3, 6)]
[list(col) for col in zip(*B)]        # [[1, 4], [2, 5], [3, 6]]
```

`zip` returns tuples and stops at the shortest input.

### Matrix add and multiply

```python
def matrix_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))]
            for i in range(len(A))]

def matrix_mult(A, B):
    def dot(r, c):
        return sum(r[i] * c[i] for i in range(len(r)))
    return [[dot(row, col) for col in zip(*B)] for row in A]
```

Trace:

```python
A = [[1, 2, 3],
     [4, 5, 6]]
B = [[7, 8],
     [9, 10],
     [11, 12]]

matrix_mult(A, B)   # [[58, 64], [139, 154]]
list(zip(*B))       # [(7, 9, 11), (8, 10, 12)]
```

Matrix multiplication is row dot column. Element-by-element multiplication is not
matrix multiplication.

## Classic Review Problems

### Saddle point

A saddle point is minimum in its row and maximum in its column.

```python
def saddle(x):
    for i in range(len(x)):
        row_min = min(x[i])
        for j in range(len(x[i])):
            if x[i][j] == row_min:
                col = [x[r][j] for r in range(len(x))]
                if x[i][j] == max(col):
                    return (x[i][j], i, j)
    return "not found"
```

```python
saddle([[4, 2, 5],
        [3, 1, 6],
        [7, 0, 8]])    # (2, 0, 1)
```

### Robot paths

Moves allowed: right or down. Boundary cells are `1`; inside cells are above plus
left.

```python
n = 4
a = [[0] * n for _ in range(n)]
for i in range(n):
    a[i][0] = 1
    a[0][i] = 1
for i in range(1, n):
    for j in range(1, n):
        a[i][j] = a[i - 1][j] + a[i][j - 1]

a[n - 1][n - 1]   # 20
```

The table for `n = 4`:

```text
[[1, 1, 1, 1],
 [1, 2, 3, 4],
 [1, 3, 6, 10],
 [1, 4, 10, 20]]
```

### Base-8 digit list

```python
def get_num(n):
    out = [0] * 8
    for i in range(7, -1, -1):
        out[i] = n % 8
        n //= 8
    return out

get_num(65)   # [0, 0, 0, 0, 0, 1, 0, 1]
```

### Eight queens diagonal test

Use permutations for columns: one queen per row and one per column is already
guaranteed. Only diagonals remain.

```python
from itertools import permutations

col = list(range(8))
for vec in permutations(col):
    if (8 == len(set(vec[i] + i for i in col))
            == len(set(vec[i] - i for i in col))):
        print(vec)
```

Why it works:

```text
same row + col  => same down-left/up-right diagonal
same col - row  => same down-right/up-left diagonal
duplicate in either set => diagonal conflict
```
