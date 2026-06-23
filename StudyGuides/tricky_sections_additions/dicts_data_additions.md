# Dictionary and Data Additions from the Chart PDF

These questions are new angles from `introduction-to-programming-with-chart`, not replacements for the existing dictionary/set/chart drills.

## [HIGH] 1. Counter methods vs Counter arithmetic

Source: chart PDF pp. 7-9.

Trace this exactly:

```python
from collections import Counter

c1 = Counter("abracadabra")
c2 = Counter("barb")

print(c1.most_common(3))
print(list(c2.elements()))
print(c1 - c2)
print(c1.subtract(c2))
print(c1)
print(list(c1.elements()))
print(+c1)
```

Answer:

```text
[('a', 5), ('b', 2), ('r', 2)]
['b', 'b', 'a', 'r']
Counter({'a': 4, 'r': 1, 'c': 1, 'd': 1})
None
Counter({'a': 4, 'r': 1, 'c': 1, 'd': 1, 'b': 0})
['a', 'a', 'a', 'a', 'r', 'c', 'd']
Counter({'a': 4, 'r': 1, 'c': 1, 'd': 1})
```

Why: `c1 - c2` returns a new Counter and drops zero/negative counts. `subtract` mutates in place and returns `None`. `elements()` repeats only positive-count elements. `most_common(3)` uses count order, with ties following first-seen order.

## [HIGH] 2. Dict comprehension for nth primes

Source: chart PDF p. 14.

Implement `first_k_prime_map(k)` so it returns `{1: 2, 2: 3, 3: 5, ...}` for the first `k` primes, and the final dictionary construction must be a dictionary comprehension. `k` is already given and must not be requested inside the comprehension.

Answer:

```python
def is_prime(n):
    if n < 2:
        return False
    for factor in range(2, int(n ** 0.5) + 1):
        if n % factor == 0:
            return False
    return True


def first_k_prime_map(k):
    primes = []
    candidate = 2
    while len(primes) < k:
        if is_prime(candidate):
            primes.append(candidate)
        candidate += 1
    return {index + 1: prime for index, prime in enumerate(primes)}
```

Check:

```python
print(first_k_prime_map(6))
```

```text
{1: 2, 2: 3, 3: 5, 4: 7, 5: 11, 6: 13}
```

Why: the comprehension maps an index to an already-computed prime. Do not hide an input call or an unbounded prime search inside the comprehension.

## [MID] 3. OrderedDict vs normal dict: what is the real reason?

Source: chart PDF pp. 13-14.

Explain which data structure you would choose for each case:

1. A Python 3.11 script builds `interval_counts` in order and immediately calls `plt.bar(interval_counts.keys(), interval_counts.values())`.
2. A library must preserve insertion order on older Python versions too.
3. You need to move a recently used key to the end after lookup.

Answer:

1. Use a normal `dict`. Modern Python preserves insertion order, and keys/values views iterate in the same dictionary order.
2. Use `collections.OrderedDict` if old-version compatibility is a requirement.
3. Use `OrderedDict` because it has order-manipulation methods such as `move_to_end`.

Why: `OrderedDict` is not just "a dict that remembers order" anymore. In modern Python, normal dicts remember insertion order too; `OrderedDict` matters when compatibility or explicit order operations are part of the requirement.

## [HIGH] 4. `**kwargs`, `list(c.items())`, and a tuple key

Source: chart PDF pp. 17-19.

Trace this:

```python
def z(a, *b, **c):
    print(type(a), type(b), type(c))
    print(a, b[1], c, sep="\n")
    print(len(c), list(c.items()))
    g = list(c.items())
    c[g[0]] = 156
    print(list(c.items()))
    d = [i for i in c.keys()]
    print(c[d[0]])
    print(c[list(c)[0]])
    for i in iter(c):
        print(i)

z(12, 3, 4, 5, k=87, l=19)
```

Answer:

```text
<class 'int'> <class 'tuple'> <class 'dict'>
12
4
{'k': 87, 'l': 19}
2 [('k', 87), ('l', 19)]
[('k', 87), ('l', 19), (('k', 87), 156)]
87
87
k
l
('k', 87)
```

Why: `*b` captures extra positional arguments as a tuple, and `**c` captures keyword arguments as a dict. `g[0]` is the tuple `('k', 87)`, which is hashable, so it can become a new key in `c`. Iterating over a dict gives keys.

## [HIGH] 5. Scrabble signature dictionary

Source: chart PDF pp. 20-22.

Implement the core dictionary for a six-letter Scrabble descrambler. Given a list of words, build a dictionary where the key is the sorted-letter signature and the value is a list of all words with that signature. Then return matches for a rack.

```python
words = ["REACTN", "CRETAN", "TRANCE", "PYTHON", "THINGY"]
print(signature("ACENRT"))
print(build_scrabble_dict(words))
print(find_words("ACENRT", words))
```

Answer:

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


def find_words(rack, words):
    d = build_scrabble_dict(words)
    return d.get(signature(rack), [])
```

Exact output:

```text
ACENRT
{'ACENRT': ['REACTN', 'CRETAN', 'TRANCE'], 'HNOPTY': ['PYTHON'], 'GHINTY': ['THINGY']}
['REACTN', 'CRETAN', 'TRANCE']
```

Why: anagrams share the same sorted-letter signature. The dictionary key should be the signature, not the original word.

## [MID] 6. Pickle dump/load modes and object reconstruction

Source: chart PDF pp. 21-22.

Fix the bug and explain what gets reconstructed:

```python
import pickle

d = {"ACENRT": ["CRETAN", "TRANCE"]}

with open("slwords", "w") as f:
    pickle.dump(d, f)

with open("slwords", "r") as f:
    restored = pickle.load(f)
```

Answer:

```python
import pickle

d = {"ACENRT": ["CRETAN", "TRANCE"]}

with open("slwords", "wb") as f:
    pickle.dump(d, f)

with open("slwords", "rb") as f:
    restored = pickle.load(f)
```

Why: pickle uses a binary format, so the file must be opened with `wb` for dumping and `rb` for loading. `pickle.load` reconstructs a new Python object with the same nested structure and values. It is not the same object identity as the original in memory.

Exact identity check:

```python
print(restored == d)
print(restored is d)
```

```text
True
False
```

## [HIGH] 7. Inverted index with defaultdict and squish

Source: chart PDF pp. 23-28.

Implement an inverted index for these lines. The value for each word should store total count and squished line numbers as `(line, count_on_that_line)` pairs.

```python
lines = [
    "Cat cat dog",
    "dog bird",
    "cat dog dog",
]
print(build_inverted_index(lines)["cat"])
print(build_inverted_index(lines)["dog"])
```

Answer:

```python
from collections import defaultdict


def clean(text):
    exclude = {".", ",", "-"}
    return "".join(ch for ch in text.lower() if ch not in exclude)


def squish(nums):
    if not nums:
        return []
    result = []
    current = nums[0]
    count = 1
    for number in nums[1:] + [None]:
        if number == current:
            count += 1
        else:
            result.append((current, count))
            current = number
            count = 1
    return result


def build_inverted_index(lines):
    index = defaultdict(lambda: {"count": 0, "lines": []})
    for line_number, line in enumerate(lines, 1):
        for word in clean(line).split():
            entry = index[word]
            entry["count"] += 1
            entry["lines"].append(line_number)
    for data in index.values():
        data["lines"] = squish(sorted(data["lines"]))
    return index
```

Exact output:

```text
{'count': 3, 'lines': [(1, 2), (3, 1)]}
{'count': 4, 'lines': [(1, 1), (2, 1), (3, 2)]}
```

Why: `defaultdict` removes the repeated "if word not in index" setup. `squish` compresses repeated line numbers after sorting, so multiple occurrences on one line become one `(line, count)` pair.

## [MID] 8. `groupby` squish bug when input is unsorted

Source: chart PDF pp. 24-25 and pp. 33-34.

Trace the bug and then fix it:

```python
from itertools import groupby

def squish_with_groupby(nums):
    return [(key, len(list(group))) for key, group in groupby(nums)]

line_numbers = [4, 6, 4, 4, 6, 8, 8]
print(squish_with_groupby(line_numbers))
print(squish_with_groupby(sorted(line_numbers)))
```

Answer:

```text
[(4, 1), (6, 1), (4, 2), (6, 1), (8, 2)]
[(4, 3), (6, 2), (8, 2)]
```

Why: `groupby` only groups consecutive equal values. For an inverted index, if line numbers might arrive out of order, sort first. For already sequential file reading, repeated line numbers for a word usually appear in line-number order, but the safe general rule is: sort before `groupby` when you want all equal keys combined.

## [MID] 9. Chart labels and values can silently misalign

Source: chart PDF pp. 31-34.

Fix the bug. The labels are sorted, but the bar heights still come from the original insertion order.

```python
interval_counts = {"91-100": 2, "1-10": 1, "11-20": 3}

labels = sorted(interval_counts)
heights = list(interval_counts.values())

print(labels)
print(heights)
```

Buggy output:

```text
['1-10', '11-20', '91-100']
[2, 1, 3]
```

Correct answer:

```python
labels = sorted(interval_counts, key=lambda label: int(label.split("-")[0]))
heights = [interval_counts[label] for label in labels]

print(labels)
print(heights)
```

Correct output:

```text
['1-10', '11-20', '91-100']
[1, 3, 2]
```

Why: `dict.keys()` and `dict.values()` line up only when both views come from the same dictionary order. Once you sort or otherwise reorder the keys, build values from those exact labels.
