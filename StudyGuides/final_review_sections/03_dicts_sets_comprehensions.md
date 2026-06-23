# Dicts, Sets, Comprehensions: Last-Hour Review

Use this as a memory checklist. Most traps here reduce to:

1. Is Python checking keys, values, or items?
2. Is this a live view, shallow copy, or new container?
3. Are duplicates being kept, removed, or overwritten?
4. Did you sort before `groupby` or chart alignment?

## 1. Dict Basics and Methods

Dicts map hashable keys to values. Membership checks keys only.

```python
prices = {"IBM": 91.5}
print("IBM" in prices)       # True
print(91.5 in prices)        # False
print(prices["GOOG"])        # KeyError: 'GOOG'
```

| Operation | Meaning | Missing-key behavior | Return |
|---|---|---|---|
| `d[k]` | Lookup | `KeyError` | Value |
| `d[k] = v` | Insert or replace | No error | None |
| `d.get(k)` | Safe lookup | `None` | Value or `None` |
| `d.get(k, default)` | Safe lookup | `default` | Value or default |
| `d.pop(k)` | Remove key | `KeyError` | Removed value |
| `d.pop(k, default)` | Remove if present | `default` | Removed value or default |
| `del d[k]` | Delete key/value pair | `KeyError` | No return |
| `d.clear()` | Empty same dict object | No key lookup | `None` |
| `d.copy()` | Shallow copy outer dict | No key lookup | New dict |

Memory warning: `copy()` is shallow.

```python
d = {"a": [1], "b": 2}
e = d.copy()
e["a"].append(9)
e["b"] = 20
print(d)       # {'a': [1, 9], 'b': 2}
print(e)       # {'a': [1, 9], 'b': 20}
```

## 2. Keys, Tuple Keys, Views, Order

Keys must be hashable. Strings, numbers, and tuples of hashable objects are OK.
Lists, sets, and dicts are not OK as keys.

```python
d = {}
d["IBM", "2015-02-04"] = 91.42
print(list(d))                         # [('IBM', '2015-02-04')]
print(d[("IBM", "2015-02-04")])        # 91.42
print("IBM" in d)                      # False
d[[1, 2]] = "bad"                      # TypeError
```

Memory warning: commas can make one tuple key. Membership checks the whole key,
not pieces inside it.

Dict views are live:

| Form | What it is | Trap |
|---|---|---|
| `d.keys()` | Live key view | Updates when dict changes |
| `d.values()` | Live value view | Same dict order as keys/items |
| `d.items()` | Live `(key, value)` view | Values update live |
| `list(d)` | Snapshot list of keys | Frozen at that moment |
| `list(d.items())` | Snapshot list of pairs | Still shallow for nested values |

```python
d = {"a": 1, "b": 2}
keys = d.keys()
snap = list(d)
d["c"] = 3
del d["a"]
print(list(keys))      # ['b', 'c']
print(snap)            # ['a', 'b']
```

Modern dicts preserve insertion order. Keys and values line up only if they
come from the same order:

```python
counts = {"91-100": 2, "1-10": 1, "11-20": 3}
labels = sorted(counts, key=lambda s: int(s.split("-")[0]))
heights = [counts[label] for label in labels]
print(labels)      # ['1-10', '11-20', '91-100']
print(heights)     # [1, 3, 2]
```

Memory warning: after sorting labels, do not use `list(counts.values())`.

## 3. Comprehensions

| Form | Builds | Eager/lazy | Duplicate behavior | Exam warning |
|---|---|---|---|---|
| `[expr for x in it if test]` | List | Eager | Keeps duplicates | Builds new list |
| `{expr for x in it if test}` | Set | Eager | Collapses duplicates | Order not the point |
| `{k: v for x in it if test}` | Dict | Eager | Duplicate keys overwrite | Last key wins |
| `(expr for x in it if test)` | Generator | Lazy | Yields produced values | One-pass iterator |

Comprehensions read like nested loops from left to right:

```python
z = [13, 14, 7, 12, 11, 3, 18]
out = [(i, z[i]) for i in range(len(z)) if z[i] % 2 == 0]
print(out)       # [(1, 14), (3, 12), (6, 18)]

print([(i, j) for i in range(2) for j in range(3)])
# [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
```

Duplicate behavior:

```python
nums = [1, 2, 2, 3]
print([x * x for x in nums])       # [1, 4, 4, 9]
print({x * x for x in nums})       # {1, 4, 9}, order not the point

portfolio = [("IBM", 75), ("ACME", 50), ("IBM", 25)]
print({name: shares for name, shares in portfolio})
# {'IBM': 25, 'ACME': 50}
```

Memory warning: a comprehension builds a new container. Rebinding a local name
to that new container does not mutate the caller's object.

## 4. Sets

A set stores unique hashable elements. Use sets for membership and duplicate
removal, not indexing or order.

### Set Core Rules

| Idea | Tiny code | Result / warning |
|---|---|---|
| Empty set | `s = set()` | Correct empty set |
| Empty dict | `x = {}` | Dict, not set |
| Uniqueness | `set([1, 1, 2])` | `{1, 2}` |
| Membership | `2 in s` | Checks element presence |
| No indexing | `s[0]` | `TypeError` |
| Hashable item | `s.add((1, 2))` | Tuple OK if contents hashable |
| Unhashable item | `s.add([1, 2])` | `TypeError` |

### Set Methods

| Method / operation | Meaning | Return | Trap |
|---|---|---|---|
| `s.add(x)` | Add one element | `None` | Duplicate changes nothing |
| `s.remove(x)` | Remove existing element | `None` | `KeyError` if absent |
| `s.discard(x)` | Remove if present | `None` | Silent if absent |
| `s.pop()` | Remove arbitrary element | Removed element | `KeyError` if empty |
| `s.clear()` | Empty same set object | `None` | Aliases see empty set |
| `x in s` | Membership test | Boolean | No position/index |
| `len(s)` | Count unique elements | Integer | Duplicates already collapsed |

```python
s = {1, 2, 2, 3}
print(len(s))         # 3
print(2 in s)         # True
print(s.add(3))       # None
print(s.remove(2))    # None
print(s.discard(9))   # None
s.remove(9)           # KeyError: 9
```

`pop()` is arbitrary:

```python
s = {"a", "b"}
x = s.pop()           # do not predict which element
```

Set algebra and set comprehension:

```python
s = {1, 2, 3}
t = {3, 4}
print(s & t)      # {3}
print(s | t)      # {1, 2, 3, 4}
print(s - t)      # {1, 2}

nums = [1, 2, 2, 3]
squares = {x * x for x in nums}
print(len(squares), 4 in squares)      # 3 True
```

Memory warning: printed set order is not exam evidence. Use `len`, membership,
or `sorted(s)` when exact output order matters.

## 5. `Counter`, `defaultdict`, `OrderedDict`

`Counter` is a dict-like class for counts. Missing keys act like `0`.

```python
from collections import Counter

c = Counter("banana")
print(c["a"])              # 3
print(c["z"])              # 0
print(c.most_common(2))    # [('a', 3), ('n', 2)]
```

Counter arithmetic warning:

```python
c1 = Counter("abracadabra")
c2 = Counter("barb")
print(c1 - c2)             # new Counter, drops zero/negative counts
print(c1.subtract(c2))     # None, mutates c1
print(+c1)                 # drops zero/negative counts in result
```

`defaultdict(factory)` creates missing values on bracket lookup:

```python
from collections import defaultdict

d = defaultdict(list)
d["cat"].append(1)
print(d["dog"])        # []
print(list(d))         # ['cat', 'dog']
```

Memory warning: reading `d["missing"]` on a `defaultdict` can create that key.

`OrderedDict` is mainly for old Python order compatibility or order operations:

```python
from collections import OrderedDict
od = OrderedDict([("a", 1), ("b", 2)])
od.move_to_end("a")
print(list(od))        # ['b', 'a']
```

## 6. `groupby`, Inverted Index, `squish`

`itertools.groupby` groups consecutive runs only. Sort first if you want all
equal values grouped together.

```python
from itertools import groupby

nums = [4, 6, 4, 4, 6, 8, 8]
print([(k, len(list(g))) for k, g in groupby(nums)])
# [(4, 1), (6, 1), (4, 2), (6, 1), (8, 2)]

print([(k, len(list(g))) for k, g in groupby(sorted(nums))])
# [(4, 3), (6, 2), (8, 2)]
```

Inverted index shape:

```text
word -> {'count': total_count, 'lines': [(line_number, count_on_line), ...]}
```

Core pattern:

```python
from collections import defaultdict
from itertools import groupby

def squish(nums):
    return [(line, len(list(group))) for line, group in groupby(sorted(nums))]

index = defaultdict(lambda: {"count": 0, "lines": []})
for line_no, line in enumerate(lines, 1):
    for word in line.lower().split():
        index[word]["count"] += 1
        index[word]["lines"].append(line_no)

for data in index.values():
    data["lines"] = squish(data["lines"])
```

Tiny trace:

```python
lines = ["cat cat dog", "dog", "cat dog dog"]
# cat -> {'count': 3, 'lines': [(1, 2), (3, 1)]}
# dog -> {'count': 4, 'lines': [(1, 1), (2, 1), (3, 2)]}
```

Memory warning: `groupby` gives a one-use group iterator. Convert it once if
you need length or contents.

## 7. Chart Bins, `dict(zip)`, Scrabble Signature

CSV grades are strings. Guard blanks before `float`.

```python
grades = ["10", "", "0", "10.5", "100"]
positive = [float(g) for g in grades if g and float(g) > 0]
print(positive)        # [10.0, 10.5, 100.0]
```

Chart-bin pattern:

```python
counts = {}
for start in range(1, 101, 10):
    counts[f"{start}-{start + 9}"] = sum(
        1 for grade in positive if start <= grade < start + 10
    )
```

Boundary warning: `1-10` means `1 <= grade < 11`, so `10.5` belongs in
`1-10`; `100` belongs in `91-100`.

`dict(zip(keys, values))` stops at the shortest input, then duplicate keys
overwrite:

```python
print(dict(zip(["a", "b", "c"], [10, 20])))    # {'a': 10, 'b': 20}
print(dict(zip(["a", "a"], [1, 2])))           # {'a': 2}
```

Scrabble signature dictionary:

```python
def signature(word):
    return "".join(sorted(word.upper()))

def build_scrabble_dict(words):
    d = {}
    for word in words:
        sig = signature(word)
        if sig not in d:
            d[sig] = []
        d[sig].append(word)
    return d

words = ["REACTN", "CRETAN", "TRANCE", "PYTHON"]
d = build_scrabble_dict(words)
print(signature("ACENRT"))       # ACENRT
print(d["ACENRT"])               # ['REACTN', 'CRETAN', 'TRANCE']
```

Memory warning: the Scrabble key is the sorted signature, not the original word.
The value is a list because many words can share one signature.

## 8. Fast Final Checks

- Dict membership checks keys only.
- Dict keys must be hashable; tuple keys are valid if their contents are hashable.
- `d.keys()`, `d.values()`, and `d.items()` are live views.
- Dict duplicate keys overwrite older values.
- `list(d)` is a snapshot of keys.
- `copy()` is shallow.
- `{}` is an empty dict; `set()` is an empty set.
- Set duplicate elements collapse into one element.
- `remove` raises when absent; `discard` does not.
- `pop` returns and removes; `clear` mutates and returns `None`.
- List comprehensions keep duplicates; set comprehensions remove duplicates.
- Dict comprehensions overwrite duplicate keys.
- Generator expressions are lazy one-pass iterators.
- `Counter["missing"]` is `0`; normal `dict["missing"]` is `KeyError`.
- `defaultdict` can create a key just by reading `d[key]`.
- Modern dicts preserve insertion order; `OrderedDict` is for compatibility or order moves.
- `groupby` groups consecutive items only.
- Chart labels and heights must come from the same order.
- `dict(zip(keys, values))` stops at the shortest iterable.
