# 05. Decorators and OOP - Last-Hour Review

## Decorators: mental model

Always translate:

```python
@deco
def f(x):
    return x + 1
```

into:

```python
def f(x):
    return x + 1

f = deco(f)
```

- The original function object is created first.
- The decorator runs at definition time, right after the `def`.
- The decorator's return value is rebound to the original name.
- Usually the returned value is `wrapper`.
- Later, `f(...)` calls `wrapper(...)`; the wrapper calls the original through a closure.

Definition-time vs call-time trace:

```python
def deco(func):
    print("decorate", func.__name__)
    def wrapper(*args, **kwargs):
        print("call")
        return func(*args, **kwargs)
    return wrapper

@deco
def f():
    print("body")

print("ready")
f()
```

Output:

```text
decorate f
ready
call
body
```

## Correct wrapper shape

```python
import functools

def deco(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper
```

What each part prevents:

- `return wrapper`: otherwise the decorated name becomes `None`.
- `*args, **kwargs`: otherwise decorated calls with arguments can fail at the wrapper.
- `return func(...)` or `return result`: otherwise the decorated function returns `None`.
- `functools.wraps(func)`: otherwise metadata looks like the wrapper.

Return-value bug:

```python
def noisy(func):
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
    return wrapper

@noisy
def add(x, y):
    return x + y

print(add(2, 3))
```

Output:

```text
before
after
None
```

If code does `add(2, 3) * 10`, the error is:

```text
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

Argument-forwarding bug:

```python
def deco(func):
    def wrapper():
        return func()
    return wrapper

@deco
def mult(x, y):
    return x * y

mult(2, 3)
```

The call is really `wrapper(2, 3)`, so the wrapper signature fails before `mult` runs.

## `functools.wraps` and `__wrapped__`

Without `wraps`, the decorated name points to the wrapper, so metadata is wrapper metadata:

```python
def plain(func):
    def wrapper():
        """wrapper doc"""
        return func()
    return wrapper

@plain
def f():
    """f doc"""
    return 1

print(f.__name__, f.__doc__)  # wrapper wrapper doc
```

With `@functools.wraps(func)`:

- `__name__` and `__doc__` look like the original.
- `__wrapped__` points to the undecorated original.
- `f(...)` still runs the wrapper.
- `f.__wrapped__(...)` bypasses the wrapper.

```python
def deco(func):
    @functools.wraps(func)
    def wrapper(x):
        print("wrap")
        return func(x) + 1
    return wrapper

@deco
def inc(x):
    """inc doc"""
    return x + 1

print(inc.__name__, inc.__doc__)
print(inc(4))
print(inc.__wrapped__(4))
```

Output:

```text
inc inc doc
wrap
6
5
```

## Decorator factories and shared dictionaries

A decorator factory returns the real decorator:

```python
def countcalls(calldict):
    def decorator(func):
        def wrapper(*args, **kwargs):
            calldict[func.__name__] = calldict.get(func.__name__, 0) + 1
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

This:

```python
@countcalls(calls)
def add(x, y):
    return x + y
```

means:

```python
add = countcalls(calls)(add)
```

Order:

1. `countcalls(calls)` runs at definition time and returns `decorator`.
2. `decorator(add)` runs at definition time and returns `wrapper`.
3. `add(...)` later runs `wrapper(...)`.

Shared dictionary trap:

```python
calls = {}

@countcalls(calls)
def a():
    return "A"

@countcalls(calls)
def b():
    return a()

print(b())
print(calls)
```

Output:

```text
A
{'b': 1, 'a': 1}
```

Both wrappers close over the same `calls` object. Inside original `b`, the name `a` already means the wrapper for `a`.

## Stacking order

```python
@d2
@d1
def f():
    ...
```

means:

```python
f = d2(d1(f))
```

- Applied bottom-up: `d1`, then `d2`.
- Called top-down: `d2` wrapper, then `d1` wrapper, then original body.

Typical output shape:

```text
make d1
make d2
run d2
run d1
body
```

## Timing decorators

`time.time()` pattern:

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        return end - start, value
    return wrapper
```

- `time.time()` gives current seconds; use `end - start` around bigger work.
- `timeit.timeit(callable, number=n)` runs code repeatedly in a controlled way; better for small benchmark snippets.
- A timer often changes the return shape from `value` to `(runtime, value)`.

Recursive return-shape trap:

```python
@timer
def total(n):
    if n == 0:
        return 0
    return n + total(n - 1)
```

Inside the original body, `total` is the decorated global name. So recursive calls return `(runtime, value)`, not a plain number. `n + tuple` fails. Fix by unpacking:

```python
_, previous = total(n - 1)
return n + previous
```

or save the original:

```python
wrapper.original = func
```

and call `total.original(n - 1)` when recursion should bypass the wrapper.

## OOP: object and method model

- An instance stores its own attributes in `obj.__dict__`.
- `self` is the instance parameter. The name is a convention, but the first argument is required.
- `obj.method()` automatically passes `obj` as `self`.
- `Class.method(obj)` passes `self` manually.
- `Class.method()` is missing `self`.

Typical error:

```text
TypeError: show() missing 1 required positional argument: 'self'
```

`b.show` is a bound method and remembers `b`. `Box.show` is the raw function stored on the class.

## Class vs instance attributes

Lookup for `obj.x`:

1. Instance attribute.
2. Class attribute.

Assignment to `obj.x` writes to the instance:

```python
class Counter:
    total = 0

    def __init__(self):
        self.total += 1
```

`self.total += 1` reads `Counter.total`, then writes `self.total`. It does not update `Counter.total`.

Use `Counter.total += 1` when you mean shared class state.

## Mutable class attrs and mutable defaults

Shared class list:

```python
class Bag:
    items = []

    def add(self, x):
        self.items.append(x)
```

If no instance has its own `items`, every instance mutates the same class list.

Shared default list:

```python
class Weird:
    def __init__(self, values=[]):
        self.values = values
```

The default list is created once when the function is defined, not once per object. Safer:

```python
def __init__(self, values=None):
    if values is None:
        values = []
    self.values = values
```

## Properties and data hiding

Python has conventions, not strict C++ privacy:

- `_x`: intended internal attribute.
- `__x`: name-mangled; harder to access accidentally.
- Both can still be bypassed.

Property setter:

```python
class Rat:
    def __init__(self, n=0, d=1):
        self.n = n
        self.d = d

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, value):
        if value == 0:
            raise ValueError("zero denominator")
        self._d = value
```

`self.d = d` inside `__init__` calls the setter. It does not directly create `self.d`.

But this bypasses the setter:

```python
r._d = 0
print(r.d)  # 0
```

## `__str__` and `__repr__`

- `print(obj)` uses `str(obj)`, which calls `__str__`.
- `repr(obj)` calls `__repr__`.
- Lists and dictionaries display elements with `repr`, not `str`.

```python
class MiniRat:
    def __str__(self):
        return "1/2"
    def __repr__(self):
        return "MiniRat(1, 2)"

r = MiniRat()
print(r)    # 1/2
print([r])  # [MiniRat(1, 2)]
```

For exact output inside containers, check `__repr__`.

## Identity vs equality

- `is`: same object identity.
- `==`: value equality, usually through `__eq__`.

```python
class Card:
    def __init__(self, rank):
        self.rank = rank
    def __eq__(self, other):
        return isinstance(other, Card) and self.rank == other.rank

a = Card(7)
b = Card(7)
c = a
```

Results:

```python
a == b  # True
a is b  # False
a == c  # True
a is c  # True
```

## Constructors

Python does not overload `__init__` by signature. A second definition replaces the first:

```python
class Build:
    def __init__(self):
        self.kind = "empty"

    def __init__(self, x):
        self.kind = "one"
        self.x = x
```

Only the second constructor remains. `Build()` fails because `x` is required.

Replacement options:

- Use defaults: `def __init__(self, n=0, d=1): ...`
- Use `*args` carefully for multiple construction shapes.
- Use class methods for named constructors:

```python
@classmethod
def from_string(cls, s):
    n, d = s.split("/")
    return cls(int(n), int(d))
```

`cls(...)` preserves subclasses. Hard-coding `Rat(...)` does not.

## Copying object state

Assignment does not copy:

```python
b = a  # a is b
```

Shallow copy creates a new outer object but can share nested mutable objects. A custom `__copy__` must preserve every important field:

```python
def __copy__(self):
    cp = SA(self.low, self.high)
    cp.data = self.data.copy()
    return cp
```

Bad pattern:

```python
cp = SA(self.high - self.low + 1)
cp.data = self.data.copy()
```

This copies values but resets bounds to `0..size-1`, so part of the object state is wrong.

## Final traps

- Decorator assignment form first: `name = deco(original_name)`.
- Decoration-time code runs before normal code below the `def`.
- Wrapper body runs only when the decorated name is called.
- `return wrapper`, `*args/**kwargs`, and `return result` are the three common decorator failures.
- `wraps` fixes metadata and gives `__wrapped__`; it does not remove the wrapper.
- Factory order is factory, decorator, wrapper.
- Stacked decorators apply bottom-up and execute top-down.
- Timer decorators can make recursive functions return tuples inside themselves.
- `obj.method()` supplies `self`; `Class.method()` does not.
- `obj.attr = value` writes to the instance; `obj.attr.append(...)` mutates the found object.
- Mutable class attributes and mutable default arguments are shared.
- Properties run setters, but underscore storage can still be modified directly.
- Containers use `repr`.
- `is` is identity; `==` is equality.
- A later `__init__` replaces an earlier one.
- Good copies preserve all state, not just list contents.
