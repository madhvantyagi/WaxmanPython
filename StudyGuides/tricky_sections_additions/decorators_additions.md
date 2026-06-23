# Decorators Additions: PDF-Only Gap Drills

These are new high-value practice questions from the decorators PDF. They avoid repeating the main drill's basic decorator-definition, simple metadata, stacking, and recursive-timer examples.

## Questions

### [HIGH] 1. Implement a metadata-safe logging decorator

Source: decorators PDF pages 3-6.

Write `log_function_call` so this code preserves the return value, forwards any positional/keyword arguments, and keeps the decorated function's metadata.

```python
import functools

def log_function_call(func):
    # fill this in
    pass

@log_function_call
def add_numbers(x, y):
    """add two numbers"""
    return x + y

print(add_numbers(2, 3))
print(add_numbers.__name__)
print(add_numbers.__doc__)
print(add_numbers.__wrapped__(2, 3))
```

One correct solution:

```python
def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finished calling function {func.__name__}")
        return result
    return wrapper
```

Exact output:

```text
Calling function add_numbers
Finished calling function add_numbers
5
add_numbers
add two numbers
5
```

Why: `*args, **kwargs` makes the wrapper work for any call shape. `return result` preserves the original function's value. `functools.wraps(func)` copies metadata and creates `__wrapped__`.

### [HIGH] 2. Fix the silent return-value bug before it becomes an exact error

Source: decorators PDF pages 3-5.

What is the exact output/error, and what one line fixes it?

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

print(add(2, 3) * 10)
```

Exact output/error:

```text
before
after
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
```

Fix:

```python
return result
```

Why: the original `add` returns `5`, but the wrapper discards it. A function with no explicit return returns `None`, so the final line becomes `None * 10`.

### [HIGH] 3. Exact error when the wrapper forgets `*args, **kwargs`

Source: decorators PDF pages 3, 4, and 6.

What exact error is raised?

```python
def deco(func):
    def wrapper():
        return func()
    return wrapper

@deco
def mult(x, y):
    return x * y

print(mult(2, 3))
```

Exact error:

```text
TypeError: deco.<locals>.wrapper() takes 0 positional arguments but 2 were given
```

Why: after decoration, `mult` means `wrapper`. Python tries to pass `2, 3` into `wrapper`, but `wrapper` was defined with no parameters. The general decorator shape is `def wrapper(*args, **kwargs): return func(*args, **kwargs)`.

### [HIGH] 4. Decorator factory with arguments and shared dictionary state

Source: decorators PDF pages 12-13.

Fill in `countcalls` so the dictionary is shared across all decorated functions.

```python
def countcalls(calldict):
    # fill this in
    pass

calls = {}

@countcalls(calls)
def add(x, y):
    return x + y

@countcalls(calls)
def mult(x, y):
    return x * y

print(add(2, 3))
print(mult(2, y=4))
print(calls)
```

One correct solution:

```python
def countcalls(calldict):
    def decorator(func):
        def wrapper(*args, **kwargs):
            calldict[func.__name__] = calldict.get(func.__name__, 0) + 1
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

Exact output:

```text
5
8
{'add': 1, 'mult': 1}
```

Why: `countcalls(calls)` runs first and returns the real decorator. Both wrappers close over the same `calls` dictionary, so updates made by different functions accumulate in one shared object.

### [MID] 5. When does the decorator factory run in a definition-only file?

Source: decorators PDF pages 7-8 and 12-13.

This file never calls `add` or `mult`. What is the exact output?

```python
def countcalls(calldict):
    print("factory")
    def decorator(func):
        print("decorate", func.__name__)
        def wrapper(*args, **kwargs):
            print("call", func.__name__)
            calldict[func.__name__] = calldict.get(func.__name__, 0) + 1
            return func(*args, **kwargs)
        return wrapper
    return decorator

calls = {}

@countcalls(calls)
def add(x, y):
    return x + y

@countcalls(calls)
def mult(x, y):
    return x * y
```

Exact output:

```text
factory
decorate add
factory
decorate mult
```

Why: `countcalls(calls)` and then `decorator(original_function)` run immediately after each `def`. The wrapper body does not run because neither decorated function is called.

### [HIGH] 6. Store the original function on the wrapper

Source: decorators PDF pages 10-11.

Give the exact output.

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("decorated")
        return func(*args, **kwargs)
    wrapper.original = func
    return wrapper

@my_decorator
def add(x, y):
    print("body", x, y)
    return x + y

print(add(1, 2))
print(add.original(1, 2))
print(add is add.original)
```

Exact output:

```text
decorated
body 1 2
3
body 1 2
3
False
```

Why: `add` is the decorated wrapper, so `add(1, 2)` prints the extra decorator line. `add.original` is the undecorated function object saved on the wrapper, so it skips the wrapper. They are different function objects.

### [HIGH] 7. `functools.wraps` plus `__wrapped__` changes what you can inspect and call

Source: decorators PDF pages 5-6.

Give the exact output.

```python
import functools

def deco(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("wrap")
        return func(*args, **kwargs) + 1
    return wrapper

@deco
def inc(x):
    """inc doc"""
    return x + 1

print(inc.__name__, inc.__doc__)
print(inc(4))
print(inc.__wrapped__(4))
```

Exact output:

```text
inc inc doc
wrap
6
5
```

Why: `wraps` makes the wrapper look like `inc` for metadata. Calling `inc(4)` runs the wrapper, which adds one after the original result. Calling `inc.__wrapped__(4)` calls the original function directly, so it returns only `5`.

### [HIGH] 8. Recursive decorated function that deliberately bypasses wrapped recursion

Source: decorators PDF pages 10, 17, and 18.

Give the exact output and explain why only one timing line prints.

```python
def timer(func):
    def wrapper(n):
        print("time", n)
        value = func(n)
        return "T" + str(n), value
    wrapper.original = func
    return wrapper

@timer
def fact(n):
    if n == 0:
        return 1
    return n * fact.original(n - 1)

print(fact(3))
```

Exact output:

```text
time 3
('T3', 6)
```

Why: the outer call `fact(3)` goes through the wrapper. Inside the original function body, the recursive call uses `fact.original`, so the recursion bypasses the wrapper and returns plain integers. This is the same kind of return-shape control needed when a timer decorator returns `(runtime, value)`.

