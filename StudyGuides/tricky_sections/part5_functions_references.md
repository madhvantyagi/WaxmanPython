# Part 5 Tricky Drill: Functions, References, and Scope

Use this section for final-exam tracing. The main rule: draw stack frames, then draw objects. Names live in frames; lists and tuples live as objects; assignment rebinds a name; list methods and item assignment mutate an existing list object.

## Trap Checklist

- Function arguments are object references. The parameter name starts as another name for the same object.
- `x = ...` inside a function rebinds local name `x`; it does not change the caller's name.
- `x.append(...)`, `x[i] = ...`, and `x.clear()` mutate the list object, so all aliases see it.
- Returning `x[i]` from a 2D list returns a row alias. Returning a comprehension or slice usually returns a new list.
- `n * [inner]` repeats references to the same `inner` list.
- Tuples are immutable as containers, but a tuple can contain a mutable list.
- If a function assigns to a name anywhere in its body, Python treats that name as local unless `global` or `nonlocal` says otherwise.
- Mutable default arguments are created once when the function is defined, not once per call.
- Each recursive call has its own frame and local names.

## Questions

### 1. Parameter alias plus local rebinding

```python
def f(a):
    a.append(4)
    a = [9, 9]
    a.append(10)
    print("inside", a)

x = [1, 2, 3]
f(x)
print("outside", x)
```

Exact output:

```text
inside [9, 9, 10]
outside [1, 2, 3, 4]
```

Behind the scenes: when `f(x)` starts, local name `a` and global name `x` point to the same list. `a.append(4)` mutates that shared list. Then `a = [9, 9]` rebinds only the local name `a` to a new list, so the later append affects only the new local list.

### 2. Row copy versus row reference

```python
def row_copy(m, i):
    return [m[i][j] for j in range(len(m[i]))]

def row_ref(m, i):
    return m[i]

grid = [[1, 2], [3, 4]]
a = row_copy(grid, 0)
b = row_ref(grid, 0)
a[0] = 99
b[1] = 88
print(a)
print(b)
print(grid)
```

Exact output:

```text
[99, 2]
[1, 88]
[[1, 88], [3, 4]]
```

Behind the scenes: `row_copy` builds a new list object, so `a` is separate from `grid[0]`. `row_ref` returns the exact row object stored in `grid[0]`, so `b[1] = 88` mutates the matrix.

### 3. Bad 2D-list construction

```python
rows = 3 * [[0, 0]]
rows[0][1] = 7
print(rows)
print(rows[0] is rows[1])
```

Exact output:

```text
[[0, 7], [0, 7], [0, 7]]
True
```

Behind the scenes: the outer multiplication copied references, not rows. There are three slots in the outer list, but all three slots point to the same inner list object.

### 4. Returning an alias from a function

```python
def first_row(m):
    return m[0]

def change(v):
    v[0] = "X"
    return v

table = [["a", "b"], ["c", "d"]]
r = first_row(table)
s = change(r)
print(r)
print(s)
print(table)
print(r is table[0], s is r)
```

Exact output:

```text
['X', 'b']
['X', 'b']
[['X', 'b'], ['c', 'd']]
True True
```

Behind the scenes: `first_row` returns the row object itself. `r`, `s`, and `table[0]` are three names/paths to the same list. `change` mutates that object and returns another reference to it.

### 5. Mutable default argument

```python
def add_item(x, box=[]):
    box.append(x)
    return box

print(add_item("a"))
print(add_item("b"))
print(add_item("c", []))
print(add_item("d"))
```

Exact output:

```text
['a']
['a', 'b']
['c']
['a', 'b', 'd']
```

Behind the scenes: the default list for `box` is created once when Python defines the function. Calls that omit `box` reuse the same list object. The call with `[]` passes a fresh list only for that one call.

### 6. Local scope error from assignment

```python
x = 5

def f():
    print(x)
    x = 6

f()
```

Exact error:

```text
UnboundLocalError: local variable 'x' referenced before assignment
```

Behind the scenes: because `x = 6` appears inside `f`, Python decides `x` is a local name for the whole function body. The `print(x)` tries to read local `x` before the local frame has a value for it.

### 7. Global rebinding

```python
x = [1]

def f():
    global x
    x = x + [2]
    print("inside", x)

f()
print("outside", x)
```

Exact output:

```text
inside [1, 2]
outside [1, 2]
```

Behind the scenes: `global x` makes assignments to `x` target the module/global frame. `x + [2]` creates a new list, and the global name `x` is rebound to that new list.

### 8. Nonlocal closure state

```python
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
        return count
    return inner

inc = outer()
print(inc())
print(inc())
print(outer()())
```

Exact output:

```text
1
2
1
```

Behind the scenes: `outer()` creates a frame with `count`. The returned `inner` function keeps access to that variable. `nonlocal count` rebinding changes the captured `count`, not a new local one. The last line calls a fresh `outer()`, so it gets a fresh `count`.

### 9. Invalid nonlocal

```python
def f():
    nonlocal x
    x = 3
```

Exact error:

```text
SyntaxError: no binding for nonlocal 'x' found
```

Behind the scenes: `nonlocal` must refer to a name in an enclosing function scope. A global name is not enough, and here there is no enclosing function variable named `x`.

### 10. Tuple container versus list inside tuple

```python
t = ([1, 2], 3)
t[0].append(4)
print(t)
t[0] = [9]
```

Exact output before the error:

```text
([1, 2, 4], 3)
```

Exact error:

```text
TypeError: 'tuple' object does not support item assignment
```

Behind the scenes: the tuple's slots cannot be rebound, so `t[0] = [9]` fails. But slot `0` points to a list object, and that list object can still be mutated with `append`.

### 11. Recursion frame tracing

```python
def mystery(n, acc):
    print("enter", n, acc)
    if n == 0:
        return acc
    ans = mystery(n - 1, acc + [n])
    print("leave", n, ans)
    return ans

print(mystery(3, []))
```

Exact output:

```text
enter 3 []
enter 2 [3]
enter 1 [3, 2]
enter 0 [3, 2, 1]
leave 1 [3, 2, 1]
leave 2 [3, 2, 1]
leave 3 [3, 2, 1]
[3, 2, 1]
```

Behind the scenes: each call has its own `n`, `acc`, and later `ans`. `acc + [n]` creates a new list on each call, so the previous frame's `acc` is not mutated. Returns move back up the stack from `n == 0` to `n == 3`.

### 12. Recursion with shared mutation

```python
def collect(n, acc):
    if n == 0:
        return acc
    acc.append(n)
    ans = collect(n - 1, acc)
    acc.append(-n)
    return ans

x = []
y = collect(3, x)
print(x)
print(y)
print(x is y)
```

Exact output:

```text
[3, 2, 1, -1, -2, -3]
[3, 2, 1, -1, -2, -3]
True
```

Behind the scenes: every recursive frame receives a parameter name `acc` pointing to the same list object. The appends before and after the recursive call all mutate that one shared list. The base case returns the same object, so `x` and `y` are aliases.

### 13. Print tracing with identity and equality

```python
def make_pair(a):
    b = a[:]
    c = a
    b.append(3)
    c.append(4)
    return b, c

nums = [1, 2]
p, q = make_pair(nums)
print(p)
print(q)
print(nums)
print(p == q)
print(q is nums)
```

Exact output:

```text
[1, 2, 3]
[1, 2, 4]
[1, 2, 4]
False
True
```

Behind the scenes: `b = a[:]` makes a shallow copy of the outer list. `c = a` makes another name for the original list. Mutating `b` does not touch `nums`; mutating `c` does. `==` compares contents, while `is` compares object identity.
