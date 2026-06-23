# Dictionaries, Sets, Counter, Defaultdict, Views, and Chart Data Traps

These are final-exam style trace questions. The point is not memorizing method names; it is knowing when Python is using a hash table, when a view is live, when a nested object is shared, and when a grouping/chart result depends on order.

## 1. Missing key: `get` vs bracket lookup

```python
prices = {'IBM': 91.5, 'MSFT': 52.13}
print(prices.get('GOOG', 0.0))
print(prices['GOOG'])
```

Exact output/error:

```text
0.0
KeyError: 'GOOG'
```

Behind the scenes: a dict is a hash table. Python hashes the key and looks for it. `get` handles a missing key by returning the default. Bracket lookup requires the key to exist, so the missing hash-table entry raises `KeyError`.

## 2. Tuple key hidden by commas

```python
d = {}
d['IBM', '2015-02-04'] = 91.42
print(list(d.keys()))
print(d[('IBM', '2015-02-04')])
print('IBM' in d)
```

Exact output:

```text
[('IBM', '2015-02-04')]
91.42
False
```

Behind the scenes: the comma creates one tuple key: `('IBM', '2015-02-04')`. The string `'IBM'` is not a separate key inside the dictionary. Membership in a dict checks whole keys, not pieces of tuple keys and not values.

## 3. Unhashable key error

```python
d = {}
d[[1, 2]] = 'bad key'
print(d)
```

Exact error:

```text
TypeError: unhashable type: 'list'
```

Behind the scenes: dictionary keys must have a stable hash. Lists are mutable, so their contents can change after insertion. Python refuses to use them as keys. A tuple like `(1, 2)` works only because its contents are hashable.

## 4. Live key view vs frozen list snapshot

```python
d = {'a': 1, 'b': 2}
keys_view = d.keys()
keys_list = list(d)
d['c'] = 3
del d['a']
print(list(keys_view))
print(keys_list)
print(sorted(keys_view & {'b', 'c', 'x'}))
```

Exact output:

```text
['b', 'c']
['a', 'b']
['b', 'c']
```

Behind the scenes: `d.keys()` is a live view into the same dictionary. It does not copy the keys. `list(d)` creates a real list at that moment, so later dictionary mutations do not change it. A keys view can also do set-style operations because dict keys are unique and hashable; `sorted` is used here so the printed set result has a predictable order.

## 5. Mutating dictionary size during iteration

```python
d = {'a': 1, 'b': 2}
for key in d:
    print(key)
    d['c'] = 3
```

Exact output/error:

```text
a
RuntimeError: dictionary changed size during iteration
```

Behind the scenes: iterating over a dict walks its current hash-table structure. Adding or deleting keys changes the table size while the iterator is using it, so Python stops with `RuntimeError`. Safe version: iterate over `list(d)` if you need to add or delete keys.

## 6. `items()` view changes live too

```python
d = {'x': 1, 'y': 2}
pairs = d.items()
print(list(pairs))
d['x'] = 10
d['z'] = 3
print(list(pairs))
```

Exact output:

```text
[('x', 1), ('y', 2)]
[('x', 10), ('y', 2), ('z', 3)]
```

Behind the scenes: `items()` returns a `dict_items` view, not a copied list. The view keeps pointing at the same dictionary, so changed values and new keys appear when you convert it to a list later.

## 7. Shallow copy vs alias

```python
a = {'nums': [1, 2], 'flag': True}
b = a
c = a.copy()
b['flag'] = False
c['nums'].append(3)
print(a)
print(c)
print(a is b, a is c, a['nums'] is c['nums'])
```

Exact output:

```text
{'nums': [1, 2, 3], 'flag': False}
{'nums': [1, 2, 3], 'flag': True}
True False True
```

Behind the scenes: `b = a` is an alias, so both names point to the same outer dict. `a.copy()` makes a new outer dict, so `c['flag']` stays `True`. But the copy is shallow: the nested list is still the exact same list object, so appending through `c` changes the list seen from `a`.

## 8. `dict.fromkeys` with a shared mutable value

```python
d = dict.fromkeys(['red', 'blue'], [])
d['red'].append(1)
print(d)
print(d['red'] is d['blue'])
```

Exact output:

```text
{'red': [1], 'blue': [1]}
True
```

Behind the scenes: `fromkeys` assigns the same value object to every key. There are two hash-table keys, but both values reference one shared list. Use a loop or comprehension if each key needs its own list.

## 9. Counter negative counts and cleanup

```python
from collections import Counter

c = Counter('mississippi')
c.subtract('sipzzz')
print(c['z'])
print(c)
print(+c)
```

Exact output:

```text
-3
Counter({'i': 3, 's': 3, 'm': 1, 'p': 1, 'z': -3})
Counter({'i': 3, 's': 3, 'm': 1, 'p': 1})
```

Behind the scenes: `Counter` is a dict subclass for counts. Missing keys start at `0`, so subtracting `'z'` three times creates `-3`. Unary plus removes zero and negative counts; it does not mutate the original unless assigned back.

## 10. Defaultdict creates keys by reading them

```python
from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)
print(dict(d))
print(d['b'])
print(list(d.keys()))
```

Exact output:

```text
{'a': [1]}
[]
['a', 'b']
```

Behind the scenes: `defaultdict(list)` calls `list()` when a missing key is accessed. Reading `d['b']` creates key `'b'` with a new empty list. This is useful for grouping, but it can accidentally add keys.

## 11. `groupby` groups consecutive values only

```python
from itertools import groupby

grades = [95, 12, 18, 91, 17]

def interval_key(grade):
    return f"{int((grade - 1) // 10) * 10 + 1}-{int((grade - 1) // 10) * 10 + 10}"

for key, group in groupby(grades, interval_key):
    print(key, list(group))
```

Exact output:

```text
91-100 [95]
11-20 [12, 18]
91-100 [91]
11-20 [17]
```

Behind the scenes: `groupby` does not search the whole list for matching keys. It streams left to right and starts a new group whenever the key changes. Sort by the same key first if all matching intervals must combine.

## 12. CSV strings, positive filtering, and chart bins

```python
import csv
from io import StringIO

data = "name,score\nAnn,10\nBo,\nCy,0\nDi,10.5\nEli,100\n"
rows = csv.reader(StringIO(data))
next(rows)

grades = [row[1] for row in rows]
positive = [float(g) for g in grades if g and float(g) > 0]

print(grades)
print(positive)
for interval in range(1, 101, 10):
    count = sum(1 for num in positive if interval <= num < interval + 10)
    if count:
        print(f"{interval}-{interval + 9}: {count}")
```

Exact output:

```text
['10', '', '0', '10.5', '100']
[10.0, 10.5, 100.0]
1-10: 2
91-100: 1
```

Behind the scenes: CSV gives strings, not numbers. The blank string is skipped, and `'0'` is removed by `float(g) > 0`. The interval test is half-open: `1 <= num < 11`, so `10.5` still belongs in `1-10`. Chart code like `plt.bar(counts.keys(), counts.values())` depends on dictionary insertion order so labels and bar heights line up.

## Trap Checklist

- `{}` creates an empty dict. Empty set is `set()`.
- `key in d` checks keys, not values.
- `d[key]` can raise `KeyError`; `d.get(key, default)` does not insert the key.
- Dict keys must be hashable; lists, sets, and dicts cannot be keys.
- Set print order is not the point on exams; use `sorted(s)` if exact order matters.
- Plain `for x in d` iterates keys. Use `d.items()` for `(key, value)` pairs.
- `keys()`, `values()`, and `items()` are live views.
- Do not add or delete dict keys while iterating over the dict itself.
- Assignment aliases the same object. `copy()` is shallow. Nested mutable values stay shared.
- `Counter.subtract()` can leave negative counts; `c1 - c2` discards nonpositive counts.
- `defaultdict` can create a key just by reading `d[key]`.
- `groupby` groups adjacent runs only; sort first when needed.
- CSV fields are strings until converted, and chart bins often fail at boundaries like `10`, `10.5`, `11`, and `100`.
