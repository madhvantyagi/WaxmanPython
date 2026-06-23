# Part 4 Runtime Additions

These are extra Part 4 questions for gaps not already covered in `part4_lists_runtime.md` or the merged drill sheet.

## Questions

### [HIGH] 1. Import Style and Name Collision

Source: Part 4 pp. 73-75, 138.

Question type: output/trace.

```python
import math
from math import sqrt

sqrt = "not a function"
print(math.sqrt(16))
print(sqrt(16))
```

Answer:

```text
4.0
TypeError: 'str' object is not callable
```

Why: `import math` binds the module name, so `math.sqrt` still reaches the function inside the module. `from math import sqrt` binds the name `sqrt` directly in the current namespace, and the later assignment shadows that imported function.

### [HIGH] 2. Builtins Are Not Reserved Names

Source: Part 4 p. 84.

Question type: exact error and fix-the-bug.

```python
sum = 0
for i in range(4):
    sum += i

print(sum)
print(sum([10, 20, 30]))
```

Answer:

```text
6
TypeError: 'int' object is not callable
```

Fix:

```python
total = 0
for i in range(4):
    total += i

print(total)
print(sum([10, 20, 30]))
```

Why: Python searches globals before builtins. The global name `sum` now points to the integer `6`, so `sum(...)` tries to call an integer.

### [HIGH] 3. Function Attributes Are Not Local Variables

Source: Part 4 pp. 91-92.

Question type: output/trace.

```python
def tracker(x):
    tracker.calls += 1
    return x * 2

tracker.calls = 0
print(tracker.__dict__)
print(tracker(3), tracker(4))
print(tracker.__dict__)
```

Answer:

```text
{'calls': 0}
6 8
{'calls': 2}
```

Why: user-defined functions are objects and can store custom attributes. `tracker.calls` lives in `tracker.__dict__`; it is not a local variable inside the function call frame.

Follow-up: Why would this fail?

```python
print.calls = 0
```

Answer: built-in functions do not allow arbitrary attribute assignment, so this raises `AttributeError`.

```text
AttributeError: 'builtin_function_or_method' object has no attribute 'calls' and no __dict__ for setting new attributes
```

### [HIGH] 4. `def` Creates a Function Object Before Any Call

Source: Part 4 pp. 79, 105-109.

Question type: output/trace plus explain concept.

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

Answer:

```text
A
D
B
add
C
15
```

Why: executing the outer `def` parses/compiles the body, creates a function object, and binds `make_adder`; it does not run the body yet. `B` prints only when `make_adder(10)` is called. The inner `def add` runs during that call and creates another function object. `C` prints only when `f(5)` calls that returned function.

### [HIGH] 5. Positional-Only and Keyword-Only Parameters

Source: Part 4 pp. 96-99.

Question type: exact error.

```python
def after(seconds, func, /, *args, **kwargs):
    return func(*args, **kwargs)

def duration(*, seconds, minutes=0, hours=0):
    return seconds + 60 * minutes + 3600 * hours

print(after(0, duration, seconds=20, minutes=1))
print(duration(20))
```

Answer:

```text
80
TypeError: duration() takes 0 positional arguments but 1 was given
```

Why: in `after(seconds, func, /, ...)`, `seconds` and `func` must be supplied positionally to `after`. In `duration(*, seconds, ...)`, everything after `*` must be supplied by keyword, so `duration(20)` is illegal.

### [HIGH] 6. `*` and `**` Unpacking Still Must Match the Signature

Source: Part 4 p. 102.

Question type: output/trace and exact error.

```python
def f(a, b, c=0, *, scale=1):
    return (a + b + c) * scale

args = [1, 2]
opts = {"c": 3, "scale": 10}

print(f(*args, **opts))
print(f(1, *[2], b=9))
```

Answer:

```text
60
TypeError: f() got multiple values for argument 'b'
```

Why: `*args` fills `a=1` and `b=2`; `**opts` fills `c=3` and keyword-only `scale=10`. The second call also fills `b` positionally from `*[2]`, then tries to fill `b` again by keyword.

### [MID] 7. Annotations and Docstrings Are Metadata, Not Runtime Checks

Source: Part 4 pp. 99-100.

Question type: output/trace and explain concept.

```python
def twice(x: int) -> int:
    """Return x twice."""
    return x + x

print(twice("ha"))
print(twice.__annotations__)
print(twice.__doc__)
```

Answer:

```text
haha
{'x': <class 'int'>, 'return': <class 'int'>}
Return x twice.
```

Why: annotations are stored in `__annotations__`; the docstring is stored in `__doc__`. Python does not use either one to enforce argument types during normal execution.

### [MID] 8. Named Tuple Return Values

Source: Part 4 pp. 103-104.

Question type: implement small function.

Implement `parse_value(text)` so all three uses below work.

```python
from typing import NamedTuple

class ParseResult(NamedTuple):
    name: str
    value: str

def parse_value(text):
    # your code here
    pass

r = parse_value("url = http://example.com")
print(r.name)
print(r[1])
name, value = r
print(name, value)
```

Answer:

```python
def parse_value(text):
    name, value = text.split("=", 1)
    return ParseResult(name.strip(), value.strip())
```

Output:

```text
url
http://example.com
url http://example.com
```

Why: a named tuple behaves like a tuple for unpacking and indexing, but it also exposes named fields such as `r.name` and `r.value`.

### [MID] 9. AST, Bytecode, and the Call Stack

Source: Part 4 pp. 105-112.

Question type: explain concept.

Put these events in the correct order for this code, and say which event runs the body.

```python
def add(a, b):
    return a + b

result = add(2, 3)
```

Events:

```text
A. Python creates a new execution frame for the call.
B. Python parses the function definition into an AST.
C. Python binds the name add to a function object.
D. Python compiles the function body into bytecode.
E. Bytecode instructions load a and b, add them, and return the value.
```

Answer:

```text
B, D, C, A, E
```

Why: the `def` statement prepares the function first: parse to AST, compile to bytecode, create/bind the function object. The body does not execute until the call `add(2, 3)`, when Python creates a call frame and runs the bytecode using its stack-based virtual machine.

### [HIGH] 10. `exec`, `eval`, and `__name__ == "__main__"`

Source: Part 4 pp. 115-119.

Question type: exact error plus explain concept.

Part A:

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

Answer:

```text
None
12
15
SyntaxError: invalid syntax
```

Why: `exec` runs statements and can create names such as `triple`, but it returns `None`. `eval` evaluates one expression and returns its value; assignment is a statement, not an expression.

Part B:

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

If you run `python module.py`, output is:

```text
loading __main__
direct
foo
```

If you run `python app.py`, output is:

```text
loading module
foo
```

Why: when a file is executed directly, Python sets its `__name__` to `"__main__"`. When the same file is imported, `__name__` is the module name, so the guarded script block does not run.
