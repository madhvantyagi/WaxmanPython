# Generator Design Additions

These questions are from the generators PDF only and avoid repeating the existing lazy-execution, one-use, `send`, mutation, and `return` drills already in `generators.md`.

## [HIGH] 1. Finite even-number generator with no global state

Source: generators PDF pp. 2-5.

Implement a generator that produces the positive even integers less than 10. Then trace the exact behavior below.

```python
def evens_under_10():
    # fill in
    pass

g = evens_under_10()
print(next(g))
print(next(g))
print(list(g))
try:
    print(next(g))
except StopIteration:
    print("done")
```

Answer:

```python
def evens_under_10():
    n = 2
    while n < 10:
        yield n
        n += 2
```

Exact output:

```text
2
4
[6, 8]
done
```

Why: `n` is a local variable stored inside the suspended generator frame. No global variable is needed. `list(g)` consumes the remaining values until `StopIteration`, catches that exception internally, and returns `[6, 8]`. A later manual `next(g)` exposes the exhaustion as `StopIteration`.

## [HIGH] 2. Infinite prime generator and `i -> ith prime` dictionary

Source: generators PDF pp. 5-6.

Write `gen_primes()` so each `next()` returns the next prime. Then implement `prime_dict(n)` so `d[i]` maps to the ith prime for `i` from `1` to `n`.

```python
def gen_primes():
    # fill in
    pass

def prime_dict(n):
    # fill in using a dictionary comprehension
    pass

print(prime_dict(6))
```

Answer:

```python
def is_prime(x):
    if x < 2:
        return False
    d = 2
    while d * d <= x:
        if x % d == 0:
            return False
        d += 1
    return True

def gen_primes():
    candidate = 2
    while True:
        if is_prime(candidate):
            yield candidate
        candidate += 1

def prime_dict(n):
    primes = gen_primes()
    return {i: next(primes) for i in range(1, n + 1)}
```

Exact output:

```text
{1: 2, 2: 3, 3: 5, 4: 7, 5: 11, 6: 13}
```

Why: the dictionary comprehension is the consumer. Each iteration calls `next(primes)` exactly once, so one shared generator object advances through the prime stream. Do not call `gen_primes()` inside the comprehension value, or every key would start from the first prime again.

## [HIGH] 3. Sensor monitor with warning and exact `return` behavior

Source: generators PDF pp. 8-12.

Modify `sensor_monitor(states, n)` so it yields the gap every time a `1` arrives, but if the gap becomes larger than `n`, it returns `"WARNING"`. Trace the exact output.

```python
def sensor_monitor(states, n):
    # fill in
    pass

g = sensor_monitor([1, 0, 0, 1, 0, 0, 0, 1], 2)
try:
    while True:
        print(next(g))
except StopIteration as e:
    print("stopped:", e.value)
```

Answer:

```python
def sensor_monitor(states, n):
    gap = 0
    for state in states:
        if state == 1:
            yield gap
            gap = 0
        else:
            gap += 1
            if gap > n:
                return "WARNING"
```

Exact output:

```text
0
2
stopped: WARNING
```

Why: the first `1` yields `0`. The next two zeros make `gap == 2`; the next `1` yields `2` and resets. Then three zeros make `gap == 3`, which is larger than `n`, so the generator returns. Manual `next()` sees that return value as `StopIteration.value`; a `for` loop or `list()` would hide it.

## [MID] 4. Leap-year generator: implement and trace partial consumption

Source: generators PDF p. 6.

Write a generator that yields leap years starting at a given year. Use the standard rule: divisible by 4, except divisible by 100 unless also divisible by 400.

```python
def leap_years(start):
    # fill in
    pass

g = leap_years(1896)
print([next(g) for _ in range(5)])
print(next(g))
```

Answer:

```python
def is_leap(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def leap_years(start):
    year = start
    while True:
        if is_leap(year):
            yield year
        year += 1
```

Exact output:

```text
[1896, 1904, 1908, 1912, 1916]
1920
```

Why: `1900` is skipped because it is divisible by `100` but not by `400`. The list comprehension is a consumer that calls `next(g)` five times and leaves the same generator positioned after `1916`.

## [MID] 5. Octal-string generator without using `oct()`

Source: generators PDF p. 7.

Implement `get_oct()` so it yields `"0"`, `"1"`, ..., `"7"`, `"10"`, ..., `"20"` as strings. Do not use Python's `oct()` function.

```python
def get_oct():
    # fill in
    pass

g = get_oct()
for _ in range(17):
    value = next(g)
print(value)
print(next(g))
```

Answer:

```python
def to_octal_string(n):
    if n == 0:
        return "0"
    digits = ""
    while n > 0:
        digits = str(n % 8) + digits
        n //= 8
    return digits

def get_oct():
    n = 0
    while True:
        yield to_octal_string(n)
        n += 1
```

Exact output:

```text
20
21
```

Why: the loop calls `next(g)` 17 times, so `value` ends as the octal representation of decimal `16`, which is `"20"`. The following `next(g)` advances to decimal `17`, which is `"21"`.

## [MID] 6. Fibonacci generator state bug fix

Source: generators PDF p. 7.

The intended output is `0, 1, 1, 2, 3, 5`. What is wrong, and how should it be fixed?

```python
def fib():
    a = 0
    b = 1
    while True:
        yield a
        a = b
        b = a + b

g = fib()
print([next(g) for _ in range(6)])
```

Answer:

```python
def fib():
    a = 0
    b = 1
    while True:
        yield a
        a, b = b, a + b
```

Exact output:

```text
[0, 1, 1, 2, 3, 5]
```

Why: in the broken version, `a = b` runs before `b = a + b`, so the second assignment uses the already-changed `a`. Tuple assignment computes the right side first from the old values, then updates both names together.

## [HIGH] 7. Iterator protocol class versus generator function

Source: generators PDF pp. 2-4, 13-14.

Build a restartable countdown object. Each new `for` loop over the same object should start again from the original number.

```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        # fill in
        pass

c = Countdown(3)
print(list(c))
print(list(c))
```

Answer:

```python
class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1
```

Exact output:

```text
[3, 2, 1]
[3, 2, 1]
```

Why: `Countdown` is an iterable. Its `__iter__` method creates a fresh generator each time iteration starts. That is different from a generator object, whose `__iter__()` returns itself and therefore cannot restart after exhaustion. If writing a manual iterator instead, `__iter__` returns `self` and `__next__` must either return the next value or raise `StopIteration`.

## [MID] 8. Same sum, different memory model

Source: generators PDF pp. 1-2, 9-10.

All three lines print `15`. Explain what each one stores or streams, and identify which object consumes the values.

```python
print(sum([1, 2, 3, 4, 5]))
print(sum(range(1, 6)))
print(sum(i for i in range(1, 6)))
```

Answer:

```text
15
15
15
```

Memory model:

- `[1, 2, 3, 4, 5]` builds a list object containing all five integers before `sum` starts.
- `range(1, 6)` builds a compact range object that can produce the integers without storing a list of them.
- `(i for i in range(1, 6))` builds a generator object. It asks the range iterator for one value at a time and yields one value at a time.

Consumer rule: `sum(...)` is the consumer in all three cases. Like `list(...)`, it repeatedly calls `next()` on the iterable's iterator until `StopIteration`. The difference is that `list(...)` stores all produced values, while `sum(...)` combines them and keeps only the running total.

## [LOW] 9. Serial-number generator boundary trace

Source: generators PDF p. 7.

Implement a generator for serial numbers from `AA00000000` through `ZZ99999999`. Then trace the boundary around the first prefix change.

```python
def serial_numbers():
    # fill in
    pass

g = serial_numbers()
last = None
for _ in range(100000001):
    last = next(g)
print(last)
print(next(g))
```

Answer:

```python
def serial_numbers():
    for first in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        for second in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            prefix = first + second
            for number in range(100000000):
                yield prefix + str(number).zfill(8)
```

Exact output:

```text
AB00000000
AB00000001
```

Why: the first `100000000` values are `AA00000000` through `AA99999999`. The `100000001`st call returns the first `AB` value, so `last` is `AB00000000`; the next call returns `AB00000001`. The generator does not build all serial numbers in memory.
