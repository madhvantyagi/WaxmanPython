# Decorators and Closures: Tricky Exam Drill

Core rule: `@deco` runs when the function is defined. The returned object is bound to the original function name. Usually that returned object is `wrapper`. Later, calling the function name calls `wrapper`, and `wrapper` reaches the original function through a closure cell.

## Questions

### 1. Definition time vs call time

```python
def deco(func):
    print("make", func.__name__)

    def wrapper():
        print("before")
        func()
        print("after")

    print("return wrapper")
    return wrapper

@deco
def f():
    print("body")

print("between")
f()
```

Exact output:

```text
make f
return wrapper
between
before
body
after
```

Behind the scenes: Python creates the original `f`, immediately calls `deco(f)`, and rebinds `f` to `wrapper`. That is why `make f` and `return wrapper` print before `between`. The wrapper body waits until `f()` is called.

### 2. Passing the function result instead of the function

```python
def deco(func):
    def wrapper():
        return func()
    return wrapper

def f():
    print("body")
    return 10

f = deco(f())
print("ready")
f()
```

Exact output/error:

```text
body
ready
TypeError: 'int' object is not callable
```

Behind the scenes: `f()` runs before decoration and returns `10`. So `deco` stores `10` in its closure as `func`. Later `wrapper` tries `func()`, meaning `10()`, which is illegal.

### 3. Wrapper returned function and closure cell

```python
def deco(func):
    def wrapper():
        return func()
    return wrapper

@deco
def greet():
    return "hi"

print(greet.__name__)
print(greet.__closure__[0].cell_contents.__name__)
print(greet())
```

Exact output:

```text
wrapper
greet
hi
```

Behind the scenes: after decoration, the name `greet` points to `wrapper`, so `greet.__name__` is `wrapper`. But `wrapper` has a closure cell holding the original function object, whose name is still `greet`.

### 4. Missing `return result` from the wrapper

```python
def deco(func):
    def wrapper(*args, **kwargs):
        print("start")
        result = func(*args, **kwargs)
        print("end")
        # no return result
    return wrapper

@deco
def add(x, y):
    return x + y

print(add(2, 3))
```

Exact output:

```text
start
end
None
```

Behind the scenes: `add` is really `wrapper`. The original `add` returns `5`, but `wrapper` does not return that value. A Python function with no explicit return returns `None`.

### 5. `nonlocal` mutates the closure cell

```python
def count_calls(func):
    count = 0

    def wrapper():
        nonlocal count
        count += 1
        print("count", count)
        return func()

    return wrapper

@count_calls
def ping():
    print("ping")

ping()
ping()
```

Exact output:

```text
count 1
ping
count 2
ping
```

Behind the scenes: `count` lives in the enclosing `count_calls` frame through a closure cell. `nonlocal count` tells `wrapper` to update that cell instead of creating a new local variable.

### 6. `global` does not mean enclosing decorator scope

```python
count = 100

def deco(func):
    count = 0

    def wrapper():
        global count
        count += 1
        print("count", count)
        return func()

    return wrapper

@deco
def f():
    print("body")

f()
print("module count", count)
```

Exact output:

```text
count 101
body
module count 101
```

Behind the scenes: the `count = 0` inside `deco` is an enclosing local, but `global count` skips it and binds to the module-level `count`. Use `nonlocal` for the enclosing decorator variable.

### 7. Nested decorated calls with a shared dictionary

```python
def countcalls(d):
    def decorator(func):
        def wrapper(*args, **kwargs):
            d[func.__name__] = d.get(func.__name__, 0) + 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

calls = {}

@countcalls(calls)
def a():
    print("A")
    return "done"

@countcalls(calls)
def b():
    print("B")
    return a()

print(b())
print(calls)
```

Exact output:

```text
B
A
done
{'b': 1, 'a': 1}
```

Behind the scenes: `b()` calls the wrapper for `b`, which increments `b`. Inside the original `b`, the name `a` now points to the wrapper for `a`, so calling `a()` increments `a` before running the original `a`.

### 8. Metadata/name surprise, without and with `functools.wraps`

```python
import functools

def plain(func):
    def wrapper():
        """wrapper doc"""
        return func()
    return wrapper

def fixed(func):
    @functools.wraps(func)
    def wrapper():
        """wrapper doc"""
        return func()
    return wrapper

@plain
def a():
    """a doc"""
    return 1

@fixed
def b():
    """b doc"""
    return 2

print(a.__name__, a.__doc__)
print(b.__name__, b.__doc__)
```

Exact output:

```text
wrapper wrapper doc
b b doc
```

Behind the scenes: without `wraps`, the visible function is the wrapper, so its metadata is shown. `functools.wraps(func)` copies the original function metadata onto the wrapper and stores the original in `__wrapped__`.

### 9. Decorator stacking: application order vs call order

```python
def d1(func):
    print("make d1")

    def wrapper():
        print("run d1")
        return func()

    return wrapper

def d2(func):
    print("make d2")

    def wrapper():
        print("run d2")
        return func()

    return wrapper

@d2
@d1
def f():
    print("body")

f()
```

Exact output:

```text
make d1
make d2
run d2
run d1
body
```

Behind the scenes: the binding is `f = d2(d1(f))`. The decorator closest to the function, `d1`, is applied first. But the outermost wrapper, from `d2`, runs first when `f()` is called.

### 10. Timer wrapper changes recursive return values

```python
def timer(func):
    def wrapper(n):
        print("time", n)
        value = func(n)
        return "T" + str(n), value
    return wrapper

@timer
def fact(n):
    if n == 0:
        return 1
    _, previous = fact(n - 1)
    return n * previous

print(fact(3))
```

Exact output:

```text
time 3
time 2
time 1
time 0
('T3', 6)
```

Behind the scenes: after decoration, the global name `fact` points to `wrapper`. Recursive calls inside the original body also go through `wrapper`, so they return `("T...", value)`. The unpacking ignores the timer label and keeps the numeric value.

### 11. Recursive timing wrapper without unpacking

```python
def timer(func):
    def wrapper(n):
        print("time", n)
        value = func(n)
        return 0.0, value
    return wrapper

@timer
def total(n):
    if n == 0:
        return 0
    return n + total(n - 1)

print(total(2))
```

Exact output/error:

```text
time 2
time 1
time 0
TypeError: unsupported operand type(s) for +: 'int' and 'tuple'
```

Behind the scenes: `total(0)` returns `(0.0, 0)` because the name `total` means the wrapper. Then the original body for `n == 1` tries `1 + (0.0, 0)`, causing the error.

## Trap Checklist

- Translate `@deco` as `name = deco(original_name)`.
- Decoration-time code runs immediately after the original function object is created.
- Call-time code is the body of the returned wrapper.
- The original function name is usually rebound to `wrapper`.
- A wrapper can still call the original through a closure cell named `func`.
- `wrapper.original = func` preserves manual access to the undecorated function.
- Forgetting `return wrapper` makes the decorated name become `None`.
- Forgetting `return result` inside `wrapper` makes the decorated function return `None`.
- Use `*args, **kwargs` in a general wrapper, then forward them into `func`.
- `nonlocal` updates the enclosing decorator variable; `global` updates the module variable.
- Stacked decorators apply bottom-up but execute top-down.
- Without `functools.wraps`, `__name__` and `__doc__` usually belong to `wrapper`.
- Timing decorators often change the return type, for example from `value` to `(runtime, value)`.
- Recursive decorated functions call the decorated global name unless you deliberately call an undecorated reference.
