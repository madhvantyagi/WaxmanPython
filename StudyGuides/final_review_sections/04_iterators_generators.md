# 04. Iterators and Generators - Last-Hour Review

## Core model

- **Iterable**: object you can loop over. Examples: `list`, `tuple`, `str`, `dict`, `set`, `range`, files, and classes with `__iter__`.
- **Iterator**: object that remembers a current position. It has `__iter__()` and `__next__()`.
- `iter(obj)` asks an iterable for an iterator.
- `next(it)` asks an iterator for one value.
- When no values remain, `next(it)` raises `StopIteration`.
- `for x in obj:` is basically:

```python
it = iter(obj)
while True:
    try:
        x = next(it)
    except StopIteration:
        break
```

Manual `next()` exposes `StopIteration`; `for`, `list`, `sum`, `set`, and `dict` hide it by stopping normally.

## Iterable vs iterator

```python
nums = [10, 20]
a = iter(nums)
b = iter(nums)
print(next(a))      # 10
print(next(a))      # 20
print(next(b))      # 10, fresh list iterator
```

The list is reusable because each `iter(nums)` creates a new iterator.

```python
g = (x for x in [10, 20])
print(iter(g) is g) # True
```

A generator object is its own iterator. `iter(g)` does not restart it.

## Generator function basics

```python
def countdown(n):
    print("start")
    while n > 0:
        yield n
        n -= 1

g = countdown(2)
print("made")
print(next(g))
print(next(g))
```

Output:

```text
made
start
2
1
```

Calling `countdown(2)` does not run the body. It only creates a generator object. The body starts on the first consumer: `next(g)`, a `for` loop, `list(g)`, `sum(g)`, etc.

## `yield` pause/resume

- `yield value` returns `value` to the caller and freezes the function frame.
- Local variables stay alive.
- The next `next(g)` resumes immediately after the paused `yield`.
- If the function ends or hits `return`, the generator raises `StopIteration`.
- `return "done"` inside a generator stores `"done"` in `StopIteration.value` only for manual `next()` handling.

## One-use rule

```python
def pair():
    yield "A"
    yield "B"

g = pair()
print(list(g))  # ['A', 'B']
print(list(g))  # []
```

The same generator object is one-use. To restart, call the generator function again: `pair()`.

## `range` is reusable

```python
r = range(3)
print(list(r))  # [0, 1, 2]
print(list(r))  # [0, 1, 2]
```

`range` is an iterable that can create a fresh iterator each time. A generator object cannot.

## Generator expression is lazy

```python
nums = [1, 2, 3]
g = (x * 10 for x in nums if x % 2 == 1)
nums.append(5)
print(list(g))  # [10, 30, 50]
```

The generator expression does not compute when created. It computes when consumed, so later list changes can matter.

## Consumers

These consume an iterator until `StopIteration`:

- `list(g)`: stores every yielded value.
- `sum(g)`: adds values and keeps a running total.
- `set(g)`: stores unique yielded values.
- `dict(g)`: expects yielded `(key, value)` pairs and builds a dictionary.
- Comprehensions can also consume with `next(g)` inside them.

After a consumer finishes a generator, the generator is exhausted.

```python
g = (x for x in [1, 2, 3])
print(next(g))  # 1
print(sum(g))   # 5, consumes 2 and 3
print(list(g))  # []
```

## Memory differences

```python
print(sum([1, 2, 3, 4, 5]))
print(sum(range(1, 6)))
print(sum(i for i in range(1, 6)))
```

All print `15`, but the memory model is different:

- List: stores all values before `sum` starts.
- `range`: compact reusable object; does not store the whole list of integers.
- Generator expression: streams one value at a time and is one-use.

Use generators when values can be processed one at a time or the sequence is huge.

## `send` and priming

`send(value)` resumes a generator at the paused `yield` expression. The sent value becomes the result of that `yield` expression.

```python
def watch():
    total = 0
    while True:
        value = (yield total)
        total += value

g = watch()
print(next(g))   # 0, primes to first yield
print(g.send(3)) # 3
print(g.send(2)) # 5
```

You cannot send a non-`None` value to a just-started generator:

```python
g = watch()
g.send(3)  # TypeError
```

Prime first with `next(g)` or `g.send(None)`.

## `sensor_monitor` pattern

Finite input version:

```python
def sensor_monitor(states):
    gap = 0
    for state in states:
        if state == 1:
            yield gap
            gap = 0
        else:
            gap += 1

runs = [1, 1, 0, 1, 0, 0, 1]
print(list(sensor_monitor(runs)))  # [0, 0, 1, 2]
```

`list(...)` is the consumer. It repeatedly calls `next()` until the generator ends.

Coroutine version with `send`:

```python
def sensor_monitor():
    gap = 0
    while True:
        state = (yield gap)
        if state == 1:
            gap = 0
        else:
            gap += 1

m = sensor_monitor()
next(m)           # prime
print(m.send(0)) # 1
print(m.send(0)) # 2
print(m.send(1)) # 0
```

Use this when the generator should receive one new sensor value each time.

## Custom iterable / iterator class

Restartable iterable using `__iter__` as a generator:

```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

c = Countdown(3)
print(list(c))  # [3, 2, 1]
print(list(c))  # [3, 2, 1]
```

Each `iter(c)` calls `__iter__` and creates a fresh generator.

Manual one-pass iterator class:

```python
class CountDownIterator:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
```

Here `__iter__` returns `self`, so the object stores its own position and is one-pass unless you create a new object.

## Exam traps

- Generator call does not execute the body.
- `yield` pauses; next resume starts after that `yield`.
- `list(g)`, `sum(g)`, `set(g)`, and `dict(g)` consume. They do not peek.
- A generator object is one-use.
- `range` is reusable; generator objects are not.
- `iter(g) is g` for a generator.
- Manual `next(g)` can raise `StopIteration`; loops and constructors hide it.
- Generator expressions are lazy; list comprehensions run immediately.
- `send(x)` needs a paused `yield`; prime first.
- Same output can hide different memory behavior.
