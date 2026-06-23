# Functions, Scope, Modules: Last-Hour Review

Use this as a memory checklist for function and module traps. Most exam
problems here reduce to three checks:

1. When was this name bound?
2. Which namespace is Python searching?
3. Did this line call the function, or only create/pass/store it?

## 1. Imports, Modules, and Name Collisions

| Style | What gets bound in your file | Collision risk |
|---|---|---|
| `import math` | name `math` points to the module object | Low; use `math.sqrt()` |
| `import math as m` | name `m` points to the module object | Low, but `m` can still be rebound |
| `from math import sqrt` | name `sqrt` points directly to the function | Higher; easy to shadow |
| `from math import *` | many names copied into current namespace | Highest; avoid for tracing |

Trace:

```python
import math
from math import sqrt

sqrt = "not a function"
print(math.sqrt(16))   # 4.0
print(sqrt(16))        # TypeError: 'str' object is not callable
```

Why: `math.sqrt` still looks inside the module object. Plain `sqrt` now means
the local/global name `sqrt`, which was rebound to a string.

Name lookup reminder:

```text
Local -> Enclosing -> Global/module -> Builtins
```

The first matching name wins. Python does not care that the old meaning was
important.

## 2. Builtins Can Be Shadowed

Builtins are not reserved words. You can accidentally replace them in your
namespace.

```python
sum = 0
for i in range(4):
    sum += i

print(sum)                 # 6
print(sum([10, 20, 30]))   # TypeError: 'int' object is not callable
```

Common names not to use as variables:

| Avoid | Why |
|---|---|
| `sum` | Shadows `sum(...)` |
| `list` | Shadows `list(...)` |
| `str` | Shadows `str(...)` |
| `dict` | Shadows `dict(...)` |
| `set` | Shadows `set(...)` |
| `input` | Shadows `input(...)` |
| `file` | Confusing file variable name |

Fix by using real variable names:

```python
total = 0
items = [1, 2, 3]
text = "abc"
```

## 3. Functions Are Objects

Functions are first-class objects. That means a function can be:

- assigned to a variable
- passed as an argument
- returned from another function
- stored in a list or dictionary
- given attributes if it is a normal user-defined function

```python
def shout(text):
    return text.upper()

def run(func, value):
    return func(value)

f = shout
print(run(f, "hi"))        # HI
print(f is shout)          # True
```

User-defined function attributes live on the function object, not in the call
frame.

```python
def tracker(x):
    tracker.calls += 1
    return x * 2

tracker.calls = 0
print(tracker.__dict__)        # {'calls': 0}
print(tracker(3), tracker(4))  # 6 8
print(tracker.__dict__)        # {'calls': 2}
```

Built-in functions usually do not allow custom attributes:

```python
print.calls = 0        # AttributeError
```

## 4. `def` Creates a Function Object

Executing a `def` statement creates a function object and binds its name. It
does not run the function body.

```python
print("A")

def make_adder(n):
    print("B")
    def add(x):
        print("C")
        return x + n
    return add

print("D")
f = make_adder(10)
print(f.__name__)
print(f(5))
```

Output:

```text
A
D
B
add
C
15
```

Order to remember:

```text
parse function body -> compile bytecode -> create function object -> bind name
call later -> create call frame -> run body
```

Inner `def` statements run only when execution reaches them.

## 5. Argument Evaluation Before the Call

Python evaluates all argument expressions before the function body starts.
Evaluation is left to right.

```python
def bump(a):
    a.append(len(a))
    return len(a)

def show(x, y, z):
    print(x, y, z)

nums = [0]
show(bump(nums), bump(nums), nums)
```

Output:

```text
2 3 [0, 1, 2]
```

Why: the first `bump(nums)` mutates `nums`; the second sees the already-mutated
list. Only after both calls finish does `show(...)` start.

## 6. Parameters, Defaults, `*args`, and `**kwargs`

Parameters are local names bound to the objects passed in.

```python
def f(x):
    x.append(4)   # mutates caller's list
    x = [9]       # only rebinds local x

a = [1, 2]
f(a)
print(a)          # [1, 2, 4]
```

If a function has no useful return, it returns `None`.

```python
def add_item(a):
    a.append(3)

items = [1, 2]
r = add_item(items)
print(items)      # [1, 2, 3]
print(r)          # None
```

Default arguments are evaluated once, when `def` runs.

```python
def add_item(x, box=[]):
    box.append(x)
    return box

print(add_item("a"))       # ['a']
print(add_item("b"))       # ['a', 'b']
print(add_item("c", []))   # ['c']
print(add_item("d"))       # ['a', 'b', 'd']
```

Safe pattern:

```python
def add_item(x, box=None):
    if box is None:
        box = []
    box.append(x)
    return box
```

Packing in a function header:

```python
def f(a, b, *args, **kwargs):
    print(a, b)
    print(args)      # extra positional arguments as a tuple
    print(kwargs)    # extra keyword arguments as a dict

f(1, 2, 3, 4, x=5)
```

Output:

```text
1 2
(3, 4)
{'x': 5}
```

Unpacking in a call:

```python
def total(a, b, c=0, *, scale=1):
    return (a + b + c) * scale

args = [1, 2]
opts = {"c": 3, "scale": 10}
print(total(*args, **opts))        # 60
```

The final signature still must match:

```python
total(1, *[2], b=9)    # TypeError: got multiple values for argument 'b'
```

## 7. Positional-Only and Keyword-Only

`/` means everything before it must be positional. `*` means everything after it
must be keyword-only.

```python
def after(seconds, func, /, *args, **kwargs):
    return func(*args, **kwargs)

def duration(*, seconds, minutes=0, hours=0):
    return seconds + 60 * minutes + 3600 * hours

print(after(0, duration, seconds=20, minutes=1))  # 80
print(duration(20))                               # TypeError
```

Signature map:

```python
def f(pos_only, /, normal, *args, key_only, **kwargs):
    ...
```

| Parameter | Can be passed how |
|---|---|
| `pos_only` | positional only |
| `normal` | positional or keyword |
| `*args` | collects extra positional |
| `key_only` | keyword only |
| `**kwargs` | collects extra keyword |

## 8. Local, Global, Nonlocal, and Closures

If a name is assigned anywhere inside a function, Python treats it as local for
that whole function unless declared `global` or `nonlocal`.

```python
x = 5

def f():
    print(x)
    x = 6

f()       # UnboundLocalError
```

Why: `x = 6` makes `x` local inside `f`, so `print(x)` reads a local variable
before it has a value.

`global` means the module-level name:

```python
x = [1]

def f():
    global x
    x = x + [2]

f()
print(x)      # [1, 2]
```

`nonlocal` means the nearest enclosing function scope:

```python
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
        return count
    return inner

inc = outer()
print(inc())        # 1
print(inc())        # 2
print(outer()())    # 1
```

Closure rule: a returned inner function can remember variables from the outer
function. Each call to the outer function creates a fresh captured environment.

Invalid `nonlocal`:

```python
def f():
    nonlocal x      # SyntaxError: no binding for nonlocal 'x' found
    x = 3
```

`nonlocal` cannot target a global name. It must target an enclosing function
variable.

## 9. Named Tuples

A named tuple is still a tuple, but fields also have names.

```python
from typing import NamedTuple

class ParseResult(NamedTuple):
    name: str
    value: str

def parse_value(text):
    name, value = text.split("=", 1)
    return ParseResult(name.strip(), value.strip())

r = parse_value("url = http://example.com")
print(r.name)       # url
print(r[1])         # http://example.com
name, value = r
print(name, value)  # url http://example.com
```

Remember:

- supports indexing like a tuple
- supports unpacking like a tuple
- supports field names like `r.name`
- is immutable like a tuple

## 10. Annotations and Docstrings Are Metadata

Annotations do not enforce runtime types in normal Python.

```python
def twice(x: int) -> int:
    """Return x twice."""
    return x + x

print(twice("ha"))          # haha
print(twice.__annotations__)
print(twice.__doc__)
```

Output:

```text
haha
{'x': <class 'int'>, 'return': <class 'int'>}
Return x twice.
```

Metadata to know:

| Attribute | Meaning |
|---|---|
| `func.__name__` | function name |
| `func.__doc__` | docstring, or `None` |
| `func.__annotations__` | annotation dictionary |
| `func.__dict__` | custom attributes for user-defined functions |
| `func.__closure__` | closure cells, if any |

## 11. `__main__`: Script vs Module

Same `.py` file, two possible roles:

| Situation | `__name__` becomes |
|---|---|
| `python module.py` | `"__main__"` |
| `import module` | `"module"` |

Pattern:

```python
# module.py
print("loading", __name__)

def foo():
    print("foo")

if __name__ == "__main__":
    print("direct")
    foo()
```

```python
# app.py
import module
module.foo()
```

Run directly:

```text
loading __main__
direct
foo
```

Imported:

```text
loading module
foo
```

Use the guard to keep test/demo/script code from running during import.

## 12. `exec` and `eval`

Both run code from strings. Treat them as dangerous with untrusted input.

| Tool | Input kind | Return value | Can define names? |
|---|---|---|---|
| `exec(code)` | statements or blocks | `None` | Yes |
| `eval(expr)` | one expression | expression value | Not for statements |

Trace:

```python
code = "def triple(x):\n    return x * 3"

print(exec(code))
print(triple(4))
print(eval("triple(5)"))
try:
    print(eval("x = 3"))
except SyntaxError as e:
    print(type(e).__name__ + ": " + e.msg)
```

Output:

```text
None
12
15
SyntaxError: invalid syntax
```

Exam warnings:

- `exec` can create or modify names in a namespace.
- `eval` only evaluates an expression, not an assignment or loop.
- Never pass user input into `exec` or `eval` unless the problem is explicitly
  about dynamic execution and safety.
