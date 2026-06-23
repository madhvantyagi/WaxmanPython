# Tricky Python Exam Drill: Iterators and Generators

Core rule: an iterable can produce an iterator. An iterator remembers where it is. `next(it)` asks for one value. When no value remains, Python raises `StopIteration`. A generator function is a shortcut for writing an iterator: it runs only when consumed, pauses at `yield`, and keeps its local variables alive between pauses.

## 1. Calling a generator does not run the body

```python
def countdown(n):
    print("start", n)
    while n > 0:
        print("before yield", n)
        yield n
        print("after yield", n)
        n -= 1

c = countdown(2)
print("made")
print(next(c))
print(next(c))
try:
    print(next(c))
except StopIteration:
    print("StopIteration")
```

Exact output:

```text
made
start 2
before yield 2
2
after yield 2
before yield 1
1
after yield 1
StopIteration
```

Behind the scenes: `c = countdown(2)` creates a generator object only. The body starts at the first `next(c)`. Each `yield n` returns `n` and freezes the frame. The next `next(c)` resumes immediately after the paused `yield`, so `"after yield"` prints before `n` changes.

## 2. A generator object is one-use

```python
def pair():
    yield "A"
    yield "B"

g = pair()
print(list(g))
print(list(g))
try:
    print(next(g))
except StopIteration:
    print("StopIteration")
```

Exact output:

```text
['A', 'B']
[]
StopIteration
```

Behind the scenes: `list(g)` repeatedly calls `next(g)` until `StopIteration`. After the first `list(g)`, the same generator object is exhausted. Calling `list(g)` again does not restart it. Manual `next(g)` exposes the end as `StopIteration`.

## 3. List comprehension now, generator expression later

```python
nums = [1, 2, 3]

lst = [x * 10 for x in nums if x % 2 == 1]
gen = (x * 10 for x in nums if x % 2 == 1)

nums.append(5)

print(lst)
print(list(gen))
```

Exact output:

```text
[10, 30]
[10, 30, 50]
```

Behind the scenes: the list comprehension runs immediately and stores `[10, 30]`. The generator expression is lazy. It has not pulled values yet, so when `list(gen)` consumes it, the appended `5` is also seen by the list iterator and becomes `50`.

## 4. Lazy generator expressions with side effects

```python
def noisy(x):
    print("call", x)
    return x * 2

g = (noisy(x) for x in range(3))

print("made")
print(next(g))
print(sum(g))
```

Exact output:

```text
made
call 0
0
call 1
call 2
6
```

Behind the scenes: making `g` does not call `noisy`. The first `next(g)` calls `noisy(0)` and yields `0`. Then `sum(g)` consumes the remaining values by calling `next(g)` until exhaustion, so `noisy(1)` and `noisy(2)` run before `sum` prints `2 + 4 = 6`.

## 5. `send` resumes at the paused `yield`

```python
def watch():
    total = 0
    while True:
        value = (yield total)
        if value is None:
            total -= 1
        else:
            total += value

m = watch()
print(next(m))
print(m.send(3))
print(m.send(None))
print(m.send(2))
```

Exact output:

```text
0
3
2
4
```

Behind the scenes: `next(m)` primes the generator and pauses at `(yield total)`, yielding `0`. `m.send(3)` resumes that exact yield expression, so `value` becomes `3`; then the loop yields the new `total`. Sending `None` is still a value: here it triggers `total -= 1`.

## 6. Sending too early is an error

```python
def watch():
    total = 0
    while True:
        value = (yield total)
        total += value

m = watch()
try:
    print(m.send(3))
except TypeError as e:
    print(type(e).__name__ + ": " + str(e))
```

Exact output:

```text
TypeError: can't send non-None value to a just-started generator
```

Behind the scenes: a new generator has not reached a `yield` yet. There is no paused `yield` expression where `3` can be assigned. Prime it first with `next(m)` or `m.send(None)`.

## 7. Modifying a list during iteration changes what the iterator sees

```python
items = [1, 2, 3]

for x in items:
    print(x)
    if x == 2:
        items.append(4)

print(items)
```

Exact output:

```text
1
2
3
4
[1, 2, 3, 4]
```

Behind the scenes: a list iterator is not a frozen copy. It keeps an index into the same list object. When `4` is appended before the iterator reaches the end, the iterator can see it. This is legal but exam-dangerous because removing items can also skip values.

## 8. Modifying a dictionary during iteration is different

```python
d = {"a": 1, "b": 2}

try:
    for k in d:
        print(k)
        d["c"] = 3
except RuntimeError as e:
    print(type(e).__name__ + ": " + str(e))
```

Exact output:

```text
a
RuntimeError: dictionary changed size during iteration
```

Behind the scenes: dictionary iterators detect size changes. The loop starts with key `"a"` because dictionaries preserve insertion order. After adding `"c"`, the next attempt to advance the dictionary iterator raises `RuntimeError`.

## 9. `enumerate` is also a one-pass iterator

```python
e = enumerate(["x", "y", "z"])

print(next(e))
print(list(e))
print(list(e))
```

Exact output:

```text
(0, 'x')
[(1, 'y'), (2, 'z')]
[]
```

Behind the scenes: `enumerate` stores an index and an underlying iterator. The first `next(e)` consumes index `0` and value `"x"`. The first `list(e)` consumes the rest. The second `list(e)` gets nothing because `e` is already exhausted.

## 10. `zip`, `map`, and `filter` all consume one pass

```python
nums = [1, 2, 3, 4]
z = zip(
    nums,
    map(lambda x: x * 10, nums),
    filter(lambda x: x % 2 == 0, nums)
)

print(next(z))
print(list(z))
print(list(z))
```

Exact output:

```text
(1, 10, 2)
[(2, 20, 4)]
[]
```

Behind the scenes: `zip` asks each input iterator for one value. The plain `nums` iterator gives `1`; the `map` iterator gives `10`; the `filter` iterator skips `1` and yields `2`. On the next row, they give `2`, `20`, and `4`. After that, `filter` is exhausted, so `zip` stops. The same `z` cannot be reused.

## 11. `return` inside a generator ends it

```python
def g():
    yield 1
    return "done"
    yield 2

x = g()
print(next(x))
try:
    print(next(x))
except StopIteration as e:
    print("StopIteration value:", e.value)
```

Exact output:

```text
1
StopIteration value: done
```

Behind the scenes: after yielding `1`, the generator resumes and hits `return "done"`. That ends the generator. The later `yield 2` is unreachable. In a manual `next`, the return value is stored on the `StopIteration` exception as `e.value`; a normal `for` loop would hide the exception.

## 12. `iter(generator)` does not restart it

```python
def small():
    yield 1
    yield 2

a = small()
print(next(a))
b = iter(a)
print(a is b)
print(list(b))
print(list(a))
```

Exact output:

```text
1
True
[2]
[]
```

Behind the scenes: a generator object is its own iterator, so `iter(a)` returns `a`, not a fresh object. Since `1` was already consumed, `list(b)` gets only `2`. Then the same generator is exhausted, so `list(a)` is empty.

## Trap checklist

- A generator function call creates a generator object; the body starts only on `next`, a `for` loop, `list`, `sum`, `zip`, or another consumer.
- `yield` returns one value and pauses. The next resume starts immediately after that `yield`.
- A generator object is one-use. Call the generator function again if you need a fresh stream.
- `for` loops hide `StopIteration`; manual `next` shows it.
- `list(g)` and `sum(g)` consume `g`. They do not peek.
- List comprehensions run immediately; generator expressions run lazily.
- `enumerate`, `zip`, `map`, and `filter` are one-pass iterator-style tools in Python 3.
- Mutating a list during iteration may affect the loop; mutating a dictionary size during iteration raises `RuntimeError`.
- `send(value)` needs a paused `yield`; prime first with `next(g)` or `g.send(None)`.
- Same printed values can hide different memory behavior: list stores values, generator streams them.
