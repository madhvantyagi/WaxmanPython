# Part 2: Advanced Data Types, Logic, and Internal Mechanics

This module moves beyond basic syntax to understand *why* Python behaves the way it does, heavily contrasting Python's internal design with compiled languages like C++ and Java.

## 1. Deep Dive into Data Types & Memory

### Integers (`int`)
- **Internal Simulation:** In C++/Java, integers are directly bound to hardware architecture (e.g., 32-bit registers limits), which causes "integer overflow" when numbers get too large. Python **simulates integer arithmetic internally** in software.
- **Arbitrarily Large:** As a result, Python integers can be exponentially large, limited only by your runtime memory (RAM).
- **Readability:** You cannot use commas (e.g., `1,000,000`) because commas define a `Tuple`. Use underscores for human readability: `123_456_789`.

### Floats (`float`)
- Unlike integers, floating-point numbers **are represented directly using the underlying hardware** (IEEE 754 precision).
- Thus, floats *can* run into traditional hardware limits, precision errors, overflow, and underflow, exactly as they do in C++.

### Strings (`str`)
- **No `Char` Type:** In C++, single quotes specify a `char` (a single 1-byte integer mapping to ASCII) and double quotes specify a `string` (a sequence of characters ending with a null terminator `\0`).
- **Python's Approach:** Python has **no character type**. A single letter like `'A'` is just a string of length 1. Both single (`''`) and double (`""`) quotes act identically.
- **Relational Operations:** Strings are compared **lexicographically** based on underlying ASCII values. `ABC < DEF` is `True`. In chained comparisons, `x <= y < z` is valid math notation in Python.
- **Multiplication**: `3 * "Hello"` concatenates the string multiple times, mathematically resolving repetition.

### Booleans (`bool`)
- `True` and `False` (capitalized).
- Internally, `True` is treated as `1` and `False` as `0`.
- Because Python attempts to be helpful with data types, you can perform math on booleans:
  - `True * 6` evaluates to `6` (because `1 * 6 = 6`).
  - `False or 6` yields short-circuit resolution.
  - Relational operations (`>`, `<`, `==`) don't operate *on* booleans mathematically, they *yield* generic booleans. E.g., `7 > 5 * 6` returns `False` (which internally equates to `0`).

---

## 2. Variables and the Nature of Assignment

### The Runtime Stack (Pointers vs Registers)
In C++, `int I = 3` creates a specific labeled box in memory named `I` holding the binary string for `3`.
In Python, **everything is an object**. A variable `I` is merely a pointer inside a runtime stack frame referencing an object `3` in memory.

### The Assignment Statement (Python) vs Expression (C++)
- **C++ Assignment:** `I = 3` is an *expression* that returns the left-hand side reference. Hence, `cout << (I = 3);` assigns `3` to `I`, returns `I`, and prints `3`. It has both a side effect (assignment) and a return value.
- **Python Assignment:** `I = 3` is strictly a *statement*, returning absolutely **nothing**.
  - Trying to run `print(x = 5)` results in a TypeError: `x` is interpreted as an invalid keyword argument.
- **The Walrus Operator (`:=`):** Introduced in Python 3.8, it acts exactly like an assignment expression. `print(x := 5)` assigns `5` to `x` and effectively returns `5` to the `print` function.

### Extended Assignment and Tuples
- `X = Y = Z = 5` creates one object `5` and three pointers all directly referencing it.
- **Tuple Unpacking:** You can assign multiple variables simultaneously: `X, Y, Z = 1, 2, 3`. This mechanism naturally unpacks a Tuple. Functions natively return Tuples, allowing extremely clean multiple-variable returns.
- **Variable Swapping:** `a, b = b, a`. In most languages, you require a temporary variable to hold `a`. In Python, the tuple unpacking behaves efficiently via byte-code registers under the hood, seamlessly swapping values without a manual temporary variable block in RAM.

---

## 3. Advanced Boolean Logic and Short-Circuiting

Python's `and` / `or` logic evaluation behaves uniquely. They don't strictly return `True` or `False`; they return the **actual object** that ultimately resolved the conditional!

### Short-Circuit Evaluation: `and`
- Python evaluates from left to right.
- `True and 6`: Python sees `True`. Because it's an `and` operator, it *must* check the right side. It evaluates `6` (which is truthy). Since the whole expression is complete, **it returns the object `6`**.

### Short-Circuit Evaluation: `or`
- `True or 6`: Python sees `True`. Because it's an `or` operator, the expression is already guaranteed `True`. It exits instantly and **returns the object `True`**, ignoring the `6`.
- `False or 6`: Python sees `False`. It *must* evaluate the right side. It sees `6` and returns `6`.
- `6 or True`: Returns `6` immediately.

### Mathematical Flow Control (Boolean Cohesion Trick)
Leveraging Boolean-to-Integer coercion (`True=1`), you can execute logic without `if` statements:
```python
x = 4
# Only the true condition survives the string multiplication
ans = ("Even" * (x % 2 == 0)) + ("Odd" * (x % 2 != 0))
# "Even" * 1 + "Odd" * 0 = "Even"
```

---

## 4. String Formatting & Dunder Methods

### Under the Hood: The `.format()` Function
Whenever you format a string, Python internally invokes the object's `__format__` method (often called a "Dunder" method, for *Double Under*).
- Syntax: `{value:specifier}`. E.g., `"{:<20}".format("ABC")` means "Left align within a 20-character field".

### F-Strings and Expression Execution
F-strings directly interpolate variables and expressions: `f"The total is {2 * 5:10f}"`.
- Append `=` to print the literal expression variable: `f"{x=}"` yields `"x=5"`.

### Human Readable (`str`) vs Programmer Debug (`repr`)
By default, variables inside formatted strings call the `str()` constructor, which provides friendly output.
But you can force Python to use its internal representation using `!r` (which calls `repr()`).
```python
msg = "Hello\nWorld"
print(f"Normal: {msg}")      # Prints across two lines
print(f"Debug: {msg!r}")     # Exact trace output: 'Hello\nWorld'
```
This is essential for finding hidden line breaks or bad encodings.

---

## 5. Mathematical Operations and Rounding

### Two Kinds of Division
1. **True Division (`/`):** Always returns a float (`3 / 2 = 1.5`).
2. **Floor Division (`//`):** Performs truncated value drop (`3 // 2 = 1`).

### Banker's Rounding
The standard rounding computational trick is `int(x + 0.5)`, rounding everything exactly at `.5` up.
However, Python's built-in `round()` function actively mitigates statistical bias from continuously rounding `.5` upwards.
- It uses the "Banker's Algorithm": it rounds exact half values (`.5`) to the **nearest even integer**.
- `round(1.5)` = `2`
- `round(2.5)` = `2` (Even)
- `round(3.5)` = `4` (Even)
- `round(-1.5)` = `-2`
This ensures mass-aggregated financial datasets don't artificially drift towards higher totals.

---

## 🎯 Practice Problems: Part 2

**Problem 2.1: The Walrus Expression**
Rewrite the following typical early programming loop using a single line evaluation block utilizing the Walrus Operator `:=`:
```python
val = input("Enter a positive number or 'stop': ")
while val != 'stop':
    print(f"You entered {val}")
    val = input("Enter a positive number or 'stop': ")
```

**Problem 2.2: Deep Short-Circuit Logic**
Without running the code, dictate exactly what each variable will hold and *why* based on the python runtime stack.
1. `val1 = 0 and "Python"`
2. `val2 = "Apple" or "Banana"`
3. `val3 = "" or [] or 10`
4. `val4 = 6 and True and "Code"`

**Problem 2.3: Mathematical Boolean Logic (No `if` statements)**
Ask a user for an integer `N`.
- If `N` is divisible by 3, output string must contain `"Fizz"`.
- If `N` is divisible by 5, output string must contain `"Buzz"`.
- If `N` is divisible by 15, output string is `"FizzBuzz"`.
*(Hint: Use string-integer multiplication concatenation.)*

**Problem 2.4: Dunder Strings and Representations**
Initialize a hidden string literal variable `secret = "Line1\tLine2\nLine3"`.
Print the string using default f-strings, and again using explicit `!r` formatting to debug the hidden tab and newline characters.

**Problem 2.5: Formatting and Swapping Challenge**
1. Initialize variables `employee = "Jane"`, `hours = 40.5`, `rate = 25`.
2. Compute `salary = hours * rate`.
3. Use a single F-string to print:
   - `employee` centered in a 15-width field with empty spaces replaced by asterisks `*` via `fill` format.
   - `salary` mapped strictly to two decimal points explicitly printing commas for thousands.
