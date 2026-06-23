# OOP Edge Cases: Final Exam Drill

Use this section for trace-the-output questions. The main rule is simple: names point to objects, attributes point to objects, and method calls are just function calls with one argument filled in for you.

## 1. Bound method vs unbound function

```python
class Box:
    def __init__(self, name):
        self.name = name

    def show(self):
        print(self.name)

b = Box("red")
f = b.show
g = Box.show

f()
g(b)
g()
```

Exact output/error:

```text
red
red
TypeError: show() missing 1 required positional argument: 'self'
```

Behind the scenes: `b.show` is a bound method, so it remembers `b` as `self`. `Box.show` is the raw function stored on the class, so you must pass the object yourself. `g()` fails because no object was supplied for `self`.

## 2. Class variable shadowed by instance assignment

```python
class Counter:
    total = 0

    def __init__(self):
        self.total += 1

a = Counter()
b = Counter()
print(Counter.total, a.total, b.total)
print(a.__dict__)

Counter.total = 10
c = Counter()
print(Counter.total, a.total, b.total, c.total)
print(c.__dict__)
```

Exact output:

```text
0 1 1
{'total': 1}
10 1 1 11
{'total': 11}
```

Behind the scenes: `self.total += 1` first reads `total` by lookup. If the instance does not have `total`, Python finds `Counter.total`. But the assignment part writes back to the instance, creating `self.__dict__["total"]`. The class variable never increments.

## 3. Shared mutable class attribute

```python
class Bag:
    items = []

    def add(self, x):
        self.items.append(x)

a = Bag()
b = Bag()
a.add("A")
b.add("B")

print(a.items)
print(b.items)
print(a.items is b.items)
```

Exact output:

```text
['A', 'B']
['A', 'B']
True
```

Behind the scenes: neither `a` nor `b` has an instance attribute named `items`, so lookup finds the one list stored on the class. `append` mutates that shared list. No assignment creates a new instance attribute here.

## 4. Object alias plus list alias

```python
class Holder:
    def __init__(self):
        self.data = [0, 0]

a = Holder()
b = a
c = Holder()
lst = a.data

b.data[0] = 7
lst.append(9)

print(a.data, b.data, c.data)
print(a is b, a.data is lst, a is c)
```

Exact output:

```text
[7, 0, 9] [7, 0, 9] [0, 0]
True True False
```

Behind the scenes: `b = a` does not make a second `Holder`; it gives the same object another name. `lst = a.data` gives the internal list another name. Mutating through `b.data` or `lst` changes the same list inside `a`.

## 5. Mutable default argument inside objects

```python
class Weird:
    def __init__(self, values=[]):
        self.values = values

    def add(self, x):
        self.values.append(x)

a = Weird()
b = Weird()
c = Weird([])

a.add(1)
b.add(2)
c.add(3)

print(a.values)
print(b.values)
print(c.values)
print(a.values is b.values, a.values is c.values)
```

Exact output:

```text
[1, 2]
[1, 2]
[3]
True False
```

Behind the scenes: the default list is created once when the function is defined, not once per call. Both `a` and `b` store references to that same default list. `c` gets a fresh list because `[]` was passed explicitly.

## 6. Constructor goes through a property setter

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

try:
    bad = Rat(1, 0)
except Exception as e:
    print(type(e).__name__ + ": " + str(e))

r = Rat(1, 2)
r._d = 0
print(r.d)
```

Exact output:

```text
ValueError: zero denominator
0
```

Behind the scenes: `self.d = d` does not directly put `d` in `__dict__`; the property setter runs and rejects zero. But `_d` is just a normal attribute by convention. Writing `r._d = 0` bypasses the setter and breaks the invariant.

## 7. `__str__`, `__repr__`, and containers

```python
class MiniRat:
    def __init__(self, n, d):
        self.n = n
        self.d = d

    def __str__(self):
        return str(self.n) + "/" + str(self.d)

    def __repr__(self):
        return "MiniRat(" + str(self.n) + ", " + str(self.d) + ")"

r = MiniRat(1, 2)
print(r)
print(repr(r))
print([r])
```

Exact output:

```text
1/2
MiniRat(1, 2)
[MiniRat(1, 2)]
```

Behind the scenes: `print(r)` uses `str(r)`, which calls `__str__`. `repr(r)` calls `__repr__`. A list uses each element's `repr`, not its `str`, so containers usually need `__repr__` if you want clean trace output.

## 8. Equality vs identity

```python
class Card:
    def __init__(self, rank):
        self.rank = rank

    def __eq__(self, other):
        return isinstance(other, Card) and self.rank == other.rank

a = Card(7)
b = Card(7)
c = a

print(a == b, a is b)
print(a == c, a is c)
b.rank = 8
print(a == b, a is b)
```

Exact output:

```text
True False
True True
False False
```

Behind the scenes: `==` asks the objects whether their values are equal by calling `__eq__`. `is` checks whether two names point to the exact same object. `a` and `b` start with equal state, but they are separate objects. `c` is an alias for `a`.

## 9. `cls` preserves subclass construction

```python
class Rat:
    def __init__(self, n=0, d=1):
        self.n = n
        self.d = d

    @classmethod
    def from_string(cls, s):
        n, d = s.split("/")
        return cls(int(n), int(d))

    @classmethod
    def bad_from_string(cls, s):
        n, d = s.split("/")
        return Rat(int(n), int(d))

class LoudRat(Rat):
    pass

x = LoudRat.from_string("3/4")
y = LoudRat.bad_from_string("5/6")

print(type(x).__name__, x.n, x.d)
print(type(y).__name__, y.n, y.d)
```

Exact output:

```text
LoudRat 3 4
Rat 5 6
```

Behind the scenes: in a class method, `cls` is the class used in the call. `LoudRat.from_string` passes `LoudRat` as `cls`, so `cls(...)` builds a `LoudRat`. Hard-coding `Rat(...)` ignores the subclass.

## 10. Copying an object but not preserving all object state

```python
import copy

class SA:
    def __init__(self, *args):
        if len(args) == 1:
            self.low = 0
            self.high = args[0] - 1
            self.data = [0] * args[0]
        elif len(args) == 2:
            self.low, self.high = args
            self.data = [0] * (self.high - self.low + 1)

    def __copy__(self):
        cp = SA(self.high - self.low + 1)
        cp.data = self.data.copy()
        return cp

    def __getitem__(self, index):
        if index < self.low or index > self.high:
            raise IndexError("index " + str(index) + " out of range")
        return self.data[index - self.low]

    def __setitem__(self, index, value):
        if index < self.low or index > self.high:
            raise IndexError("index " + str(index) + " out of range")
        self.data[index - self.low] = value

sa = SA(10, 12)
sa[10] = 5
sa[12] = 9
cp = copy.copy(sa)

print(sa.low, sa.high, sa.data)
print(cp.low, cp.high, cp.data)

try:
    print(cp[10])
except Exception as e:
    print(type(e).__name__ + ": " + str(e))
```

Exact output:

```text
10 12 [5, 0, 9]
0 2 [5, 0, 9]
IndexError: index 10 out of range
```

Behind the scenes: `copy.copy(sa)` calls `sa.__copy__()`. This version copies the internal list, but it constructs the new array with `SA(size)`, so the copied bounds become `0..2` instead of `10..12`. The values moved, but part of the object state did not.

## 11. Nested list alias inside an object

```python
class Grid:
    def __init__(self):
        self.rows = [[0] * 2] * 2

g = Grid()
h = g

g.rows[0][1] = 7
h.rows.append([9, 9])

print(g.rows)
print(g.rows[0] is g.rows[1])
print(g is h)
```

Exact output:

```text
[[0, 7], [0, 7], [9, 9]]
True
True
```

Behind the scenes: `[[0] * 2] * 2` repeats a reference to the same inner list. Changing `g.rows[0][1]` also changes `g.rows[1][1]`. Also, `h = g` aliases the whole `Grid` object, so appending through `h.rows` changes `g.rows`.

## 12. Two `__init__` definitions do not overload constructors

```python
class Build:
    def __init__(self):
        self.kind = "empty"

    def __init__(self, x):
        self.kind = "one"
        self.x = x

try:
    a = Build()
except Exception as e:
    print(type(e).__name__ + ": " + str(e))

b = Build(4)
print(b.__dict__)
```

Exact output:

```text
TypeError: __init__() missing 1 required positional argument: 'x'
{'kind': 'one', 'x': 4}
```

Behind the scenes: Python does not overload constructors by signature. The second `def __init__` replaces the first one in the class dictionary. `Build()` fails because the only remaining constructor requires `x`.

## Trap Checklist

- `self` is not magic syntax, but normal instance calls automatically pass the object as the first argument.
- `Class.method(obj)` and `obj.method()` can call the same function; the difference is who supplies `self`.
- `x = y` never copies an object. It binds another name to the same object.
- `obj.attr = value` can create or replace an instance attribute, even if the class has an attribute with the same name.
- Mutating a shared list changes the list object; assigning a new list changes which list a name or attribute references.
- Class attributes that are mutable, like lists or dictionaries, are shared until an instance shadows them.
- Default mutable arguments are created once, so object constructors can accidentally share lists.
- `__str__` controls `print(obj)`. `__repr__` controls `repr(obj)` and how the object appears inside lists and dictionaries.
- `==` can be customized with `__eq__`; `is` only checks whether two references point to the same object.
- `@staticmethod` gets no automatic `self` or `cls`. `@classmethod` gets `cls`.
- A property setter can run inside `__init__` when the constructor assigns `self.prop = value`.
- Shallow copy copies the outer container or object shell; nested mutable objects may still be shared unless copied too.
