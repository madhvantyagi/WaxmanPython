# Final Hour Priority Map

Use this as a triage sheet, not a lecture. In the last hour, review the traps
that change exact output, exact errors, or hidden object state.

## How To Trace Any Question

Before guessing output, track three things:

```text
name      points to / value      changed how?
```

Ask after each line:

- Did this rebind a name or mutate an existing object?
- Did this call return a value or `None`?
- Is this container shallow, shared, live, or one-use?
- Did this code run now, or only create something that runs later?

## 60-Minute Review Order

### 1. First 12 minutes: aliases, mutation, copies

Most important if a question has lists, dicts, rows, objects, or function
parameters.

- `b = a` aliases. `a[:]`, `list(a)`, `.copy()` copy only the outer container.
- `copy.deepcopy(a)` copies nested mutable objects too.
- `append`, `extend`, `insert`, `remove`, `sort`, `reverse`, `clear` mutate and
  usually return `None`.
- `sorted(a)` returns a new list. `a.sort()` mutates and returns `None`.
- `a = a + [...]` rebinds. `a += [...]` usually mutates a list in place.
- Parameters are local names. Mutating a passed object affects the caller;
  rebinding the parameter does not.
- `[[0] * n] * m` shares rows. Use a comprehension for independent rows.
- Returning `matrix[i]` returns a row alias; returning a comprehension gives a
  new list.

### 2. Next 10 minutes: functions, scope, signatures

- Arguments evaluate left to right before the function body starts.
- `def` creates a function object; the body runs only when called.
- Assignment inside a function makes that name local unless declared `global` or
  `nonlocal`.
- `nonlocal` must target an enclosing function variable, not a global.
- Default arguments are created once when `def` runs.
- `*args` and `**kwargs` collect extras; `*seq` and `**dict` in a call still must
  match the signature.
- `/` means positional-only before it. `*` means keyword-only after it.
- Builtins can be shadowed: `sum = 0` breaks `sum(...)`.
- Annotations and docstrings are metadata, not runtime type checks.
- `exec` runs statements and returns `None`; `eval` handles one expression.

### 3. Next 10 minutes: dicts, sets, Counter, defaultdict, groupby

Highest value for counting, grouping, charts, files, and inverted index problems.

- Dict membership checks keys, not values.
- Missing `d[k]` raises `KeyError`; `get` and `pop(default)` are safer.
- Dict/set keys or elements must be hashable.
- `d["IBM", "date"]` is one tuple key.
- `d.keys()`, `d.values()`, and `d.items()` are live views.
- `list(d)` and `list(d.items())` are snapshots.
- Duplicate dict keys overwrite earlier values.
- `{}` is an empty dict; `set()` is an empty set.
- Set output order is not exam evidence; sort if exact output matters.
- `remove` raises if absent; `discard` does not.
- `Counter["missing"]` is `0`; normal dict missing lookup is an error.
- `Counter.subtract()` mutates and can leave zero/negative counts.
- `c1 - c2` returns a new Counter and drops nonpositive counts.
- `defaultdict` can create a key just by reading `d[key]`.
- `groupby` groups adjacent runs only. Sort first if equal keys must combine.
- Inverted index shape: `word -> {"count": n, "lines": [(line, count), ...]}`.

### 4. Next 10 minutes: iterators and generators

- Iterable can produce an iterator. Iterator remembers position.
- Manual `next(it)` can raise `StopIteration`.
- `for`, `list`, `sum`, `set`, and `dict` consume until exhaustion and hide
  `StopIteration`.
- Calling a generator function does not run the body.
- The body starts when the generator is consumed.
- `yield` returns a value and pauses the frame; the next `next(g)` resumes after
  that `yield`.
- A generator object is one-use. `list(g)` once can exhaust it.
- `range` is reusable; generator objects are not.
- Generator expressions are lazy; list comprehensions run immediately.
- Later list mutations can affect a not-yet-consumed generator expression.
- `send(x)` needs a paused `yield`; prime first with `next(g)` or `g.send(None)`.
- `return value` inside a generator is visible only as `StopIteration.value` in
  manual handling.

### 5. Next 10 minutes: decorators and OOP

- Translate `@deco` into `f = deco(f)`.
- Decorator/factory code runs at definition time.
- Wrapper code runs when the decorated name is called.
- Correct wrapper shape: `def wrapper(*args, **kwargs): return func(*args, **kwargs)`.
- Missing `return wrapper` makes the decorated name become `None`.
- Missing `return result` makes the decorated function return `None`.
- Missing `*args, **kwargs` makes calls fail at the wrapper.
- `functools.wraps` fixes metadata and creates `__wrapped__`; it does not remove
  the wrapper.
- Stacked decorators apply bottom-up and execute top-down.
- Timer decorators can change recursive return shape.
- `obj.method()` supplies `self`; `Class.method()` does not.
- `obj.attr = value` writes to the instance; `obj.attr.append(...)` mutates the
  found object, possibly shared class state.
- Mutable class attributes and mutable default arguments are shared.
- Containers display elements with `repr`, not `str`.
- `is` checks identity; `==` checks equality.
- Python does not overload `__init__`; a later definition replaces an earlier one.

### 6. Final 8 minutes: strings, files, CSV, matrices

- Strings are immutable; string methods return new strings or lists.
- `split()` groups whitespace and drops empties. `split(",")` keeps empties.
- `strip(chars)` removes any listed character from the ends, not a suffix.
- `find` returns `-1`; `index` raises.
- `join` is called on the separator and needs strings.
- File reads advance position; a second `read()` at EOF returns `""`.
- `readline()` usually includes the newline.
- `csv.reader` returns rows as strings; convert numbers yourself.
- Use `newline=""` when writing CSV.
- Matrix is `x[row][col]`.
- Column `j`: `[x[i][j] for i in range(len(x))]`.
- Main diagonal: `x[i][i]`.
- Anti-diagonal: `x[i][len(x) - 1 - i]`.
- `zip(*B)` transposes into tuples and stops at the shortest row.
- Matrix multiply is row dot column, not element-by-element multiply.
- Robot paths table: top row and left column are `1`; inside is above plus left.

## Common Exam Traps

### If output is `None`

- In-place list/set/dict method.
- Function mutates but does not return.
- Decorator wrapper forgot to return the original result.
- `Counter.subtract()`.
- `exec(code)`.

### If an object changed unexpectedly

- Assignment alias.
- Shallow copy shared a nested object.
- Mutable default argument.
- Shared class attribute.
- `dict.fromkeys(keys, [])` reused one list.
- 2D row multiplication reused one row.
- Live dict view.
- List mutated while an iterator was walking it.

### If an error appears

- `UnboundLocalError`: assignment made the name local.
- `KeyError`: missing dict key.
- `ValueError`: missing `remove/index` value or bad strided slice assignment.
- `IndexError`: bad list index or empty `pop`.
- `TypeError`: unhashable key, shadowed callable, bad wrapper signature, missing
  `self`, or sending to a fresh generator.

### If counts, groups, or charts are wrong

- Dict membership checked keys only.
- Duplicate dict keys overwrote earlier values.
- Set or set comprehension removed duplicates.
- `dict(zip(...))` stopped at the shortest input.
- `groupby` was used before sorting.
- `defaultdict` created a key while reading.
- Chart labels were sorted but values came from old dict order.

### If recursion/decorators/generators are weird

- Decorated recursive name points to the wrapper.
- Timer changed return value into `(runtime, value)`.
- Generator body has not started yet.
- Generator already got consumed.
- Generator `return` is hidden unless catching `StopIteration`.
- Closure state lives in the returned inner function's captured environment.

## Do Not Forget Checklist

- Assignment binds names; mutation changes objects.
- Aliases see mutation, not rebinding.
- Shallow copy copies the outer container only.
- In-place methods usually return `None`.
- `append` adds one object; `extend` opens an iterable.
- Do not remove from the front of a list while looping forward.
- Default arguments are evaluated once.
- Function arguments evaluate before the function body starts.
- LEGB: local, enclosing, global, builtins.
- Dict membership checks keys.
- Dict views are live.
- Generator objects are one-use.
- Generator expressions are lazy.
- `groupby` groups adjacent runs only.
- `defaultdict` can create keys on read.
- `@deco` means `f = deco(f)`.
- Decorators run now; wrappers run later.
- `wraps` preserves metadata but keeps the wrapper.
- `obj.method()` supplies `self`.
- Mutable class attributes are shared.
- Containers use `repr`.
- `is` is identity; `==` is equality.
- Strings are immutable.
- File reads advance position.
- CSV rows are strings.
- `zip(*B)` is transpose.
- Anti-diagonal index is `len(x) - 1 - i`.

If time is almost gone, skip explanations and simulate the code line by line.
