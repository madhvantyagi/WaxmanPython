# Part 1: Introduction to Python & Core Concepts

## 1. Compiled vs. Interpreted Languages
Before we dive into writing code, it is crucial to understand *how* Python operates under the hood. Programming languages generally fall into two categories: **Compiled** and **Interpreted**.

### Compiled Languages (e.g., C, C++)
- **Process**: The entire source code is translated into machine code (binary) by a compiler *before* the program is executed.
- **Speed**: Very fast because the code runs directly on the hardware's CPU.
- **Memory**: Variables are assigned specific memory locations (e.g., 32 bits for an integer), and the actual data is stored there. If you declare a variable as an integer, it **must** remain an integer.
- **Security**: The source code is secure because users only get the compiled binary executable, making intellectual property hard to steal.

### Interpreted Languages (e.g., Python)
- **Process**: Code is executed line-by-line by an interpreter. Specifically, Python translates your code into intermediate *bytecode*, which is then executed by the Python Virtual Machine (PVM).
- **Speed**: Generally slower than compiled languages because of the translation overhead during runtime.
- **Flexibility**: Highly flexible. You can run Python on any OS that has the Python interpreter installed. 

### Just-In-Time (JIT) Compilation
Some Python implementations (like PyPy) use Just-In-Time compiling. This means the interpreter compiles parts of the code as it runs to speed up execution, sitting somewhere between a pure interpreter and a pure compiler. However, standard Python (CPython) remains heavily interpreted.

---

## 2. Variables and Memory in Python
One of the most profound differences between C++ and Python is how variables and memory are handled.

### Variables as Pointers (References)
In C++, a statement like `int x = 10;` physically reserves a block of memory, labels it `x`, and places the binary value of `10` inside it. 

In Python, a statement like `x = 10` works entirely differently:
1. Python creates an **integer object** containing the value `10` somewhere in memory (the heap).
2. The variable `x` is simply a **name (or pointer/reference)** that gets attached to that object.
3. **Data types live with the object, not the variable.** The object knows it is an integer. The variable `x` does not care; it is just a tag.

Because of this, you can do:
```python
x = 10       # x points to an integer object
x = "Hello"  # Now x points to a string object
```
This is called **Dynamic Typing**. It provides immense flexibility but sacrifices the raw speed of statically typed languages.

---

## 3. Input and Output (`print` and `input`)

### The `print()` Function
The `print()` function pushes output to a stream (usually the standard output, your screen).
```python
print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)
```

**Key Arguments:**
- `sep`: The separator between items. Defaults to a single space.
- `end`: What to print at the very end. Defaults to a newline (`\n`).
- `file`: The output stream. You can write output directly to a file by changing this.
- `flush`: Forces the output buffer to flush immediately.

**Examples:**
```python
print("Hello", "World", sep="***") 
# Output: Hello***World

print("Stay", end=" ")
print("Here")
# Output: Stay Here
```

### The `input()` Function
The `input()` function pauses execution and waits for the user to type something and press Enter. 

**CRITICAL RULE:** `input()` **ALWAYS** returns a **String**. 
```python
age = input("Enter your age: ") 
# If the user types 25, age holds the string "25", NOT the integer 25.
```

If you try to add strings together, they **concatenate**:
```python
first = input("First number: ")   # User types 3
second = input("Second number: ") # User types 5
print(first + second)             # Output: 35 (String concatenation!)
```

To perform mathematical arithmetic, you must convert (cast) the string objects to integer objects using **Conversion Constructors** like `int()` or `float()`.
```python
first = int(input("First number: "))   # User types 3
second = int(input("Second number: ")) # User types 5
print(first + second)                  # Output: 8
```

---

## 4. Loops and Iterators

### The `for` Loop and `range()`
A `for` loop in Python iterates over an **iterable** sequence. The `range()` function generates a sequence of numbers (a `range` object).

```python
range(start, stop, step)
```
- `start`: Inclusive starting point (default is 0).
- `stop`: Exclusive stopping point (required).
- `step`: How much to increment by (default is 1).

**Example:**
```python
for i in range(5):
    print(i)
# Prints 0, 1, 2, 3, 4
```

Python uses **indentation** to define code blocks (unlike Java or C++ which use `{}`). Everything indented beneath the `for` statement belongs to that loop.

### The `while` Loop
A `while` loop continues to run as long as a specified condition is `True`.

```python
x = "continue"
while x != "done":
    print("Running...")
    x = input("Type 'done' to stop: ")
```

---

## 5. Turtle Graphics
Turtle is a built-in module in Python that provides a virtual canvas and a "turtle" (a pen) to draw graphics using Cartesian coordinates.

### Basic Commands
```python
from turtle import *

forward(100) # Move forward 100 pixels
right(90)    # Turn right 90 degrees
left(45)     # Turn left 45 degrees
penup()      # Lift pen (moving won't leave a trace)
pendown()    # Drop pen (moving leaves a trace)
```

### Drawing Polygons
To draw regular polygons, use loops. The turtle must trace out the perimeter. When the turtle reaches a corner, it must turn by the **exterior angle** of the polygon.

**Formulas for an n-sided regular polygon:**
- Sum of Interior Angles: `(n - 2) * 180`
- Single Interior Angle: `((n - 2) * 180) / n`
- **Exterior Angle (Turn Angle):** `360 / n`

**Example: Drawing a Hexagon (6 sides)**
```python
from turtle import *
for i in range(6):
    forward(100)
    left(360 / 6) # Turns 60 degrees left at each corner
```

**Drawing a Circle:**
A circle can be approximated as a polygon with 360 sides.
```python
from turtle import *
for i in range(360):
    forward(1)
    right(1)
```

---

## 🎯 Practice Problems: Part 1

**Problem 1.1: Memory Models**
Explain in your own words what happens in Python's memory when the following two lines of code are executed:
```python
a = 100
a = "Python"
```
*How does this differ from C++?*

**Problem 1.2: Formatting Output**
Write a single `print` statement that takes the strings `"Red"`, `"Green"`, and `"Blue"` and outputs them exactly like this:
`Red-->Green-->Blue!!!`
*Hint: Use `sep` and `end` arguments.*

**Problem 1.3: Type Casting & Arithmetic**
Write a short script that asks the user for the base and height of a triangle. Ensure you account for decimal inputs. Output the area of the triangle formatted as a string. (Area = 0.5 * base * height).

**Problem 1.4: Polygon Calculations**
You need to draw a regular **Nonagon (9-sided polygon)** using the turtle module.
1. What is the sum of the interior angles?
2. What is the value of a single interior angle?
3. What is the turning angle (exterior angle) the turtle must make?
4. Write the `for` loop required to draw it with side length `50`.

**Problem 1.5: Nested Triangles**
Using the turtle module, write a script that draws 10 triangles. The first triangle should have a side length of 10. The second triangle should have a side length of 20. The third should have a side length of 30, and so on up to 100.
*Hint: Use `for i in range(1, 11):` and multiply your forward movement by `i`.*

**Problem 1.6: Validating User Input**
Write a `while` loop that continuously asks the user for a magic word. If the user types anything other than `"abracadabra"`, print `"Wrong, try again."`. If they type the magic word, print `"Access Granted"` and terminate the loop.
# Part 2: Data Types, Logic, and String Formatting

## 1. Deep Dive into Data Types

Python's built-in scalar data types include `int`, `float`, `str`, and `bool`.

### Integers (`int`)
Unlike C++ or Java where integers are strictly tied to hardware architectures (e.g., 32-bit limits causing integer overflow at large values), Python simulates integer arithmetic using internal software objects. 
- **Result:** Python integers can be **arbitrarily large**, limited only by your computer's available memory. You will rarely encounter an "integer overflow" error in plain Python.
- **Large Numbers:** You cannot use commas for thousands separators (e.g., `1,000,000`), because commas define Tuples. However, you can use underscores for readability: `1_000_000`.

### Floats (`float`)
Floating-point numbers (decimals) in Python **are** represented directly using the underlying hardware (usually standard 64-bit IEEE 754 precision). 
- **Result:** Because they rely on hardware, floating-point numbers **can** overflow and are subject to traditional precision errors.

### Strings (`str`)
In Python, there is no separate "character" (`char`) data type as seen in C++. A single letter like `'A'` is simply a string of length 1.
- Everything inside single `''` or double `""` quotes is a string.

### Division Operators
Python offers two kinds of division:
1. **True Division (`/`)**: Always returns a `float`. E.g., `5 / 2 = 2.5`.
2. **Truncated / Floor Division (`//`)**: Throws away the fractional part and returns the largest floor value. E.g., `5 // 2 = 2`.

---

## 2. Advanced String Operations & Formatting

### Multiplication of Strings
Just as `3 * 5` means adding five three times (`5 + 5 + 5`), multiplying a string by an integer means string concatenation:
```python
print(3 * "Hello ") 
# Output: Hello Hello Hello 
```

### Relational Comparisons
Strings are compared **lexicographically** (dictionary order) character by character using their underlying ASCII values.
```python
print("ABC" < "DEF")  # True
print("apple" < "Zebra") # False (Uppercase letters have lower ASCII values than lowercase)
```

### Chained Comparisons
A unique feature of Python is the ability to write mathematical chains normally reserved for algebra:
```python
x = 5
print(1 <= x < 10)  # Valid Python! Evaluates to True.
```

---

## 3. String Formatting (`.format()` and F-strings)

When building applications, printing ugly output like `You earned $ 50.0 ` is unacceptable. We need to format our strings cleanly.

### The `.format()` Method
This calls the `__format__` dunder method on String objects to interpolate variables.
```python
hours = 5
rate = 10.5
print("You earned ${:.2f}".format(hours * rate))
# Output: You earned $52.50
```
- `{:.2f}`: The `:` indicates format specifier mode. `.2f` means "Float rounded to 2 decimal places".
- `{:<20}`: Left-align within a 20-character width field.
- `{:>20}`: Right-align within a 20-character width field.
- `{:^20}`: Center within a 20-character width field.
- `{:0>5}`: Right-align within 5 characters, fill empty space with zeros.

### F-Strings (Formatted String Literals)
Introduced in Python 3.6, these are the modern standard for printing. You prepend the string with an `f` or `F`.
```python
name = "Alice"
age = 30
print(f"Name: {name}, Age: {age:^10}")
```

### Debugging with `!r` and `!s`
Variables inside f-strings look for their string representation. 
- By default, Python calls `str()`, giving a human-readable string.
- Appending `!r` will force Python to call `repr()`, which prints the internal representation. This is excellent for debugging hidden characters.
```python
msg = "Hello\nWorld"
print(f"Normal: {msg}")      # Prints on two lines
print(f"Debug: {msg!r}")     # Prints 'Hello\nWorld' literally
```

---

## 4. Boolean Logic and Short-Circuiting

Boolean values are always capitalized: `True` and `False`.
Python uses logical English words: `and`, `or`, `not`.

### Truthy and Falsy
In Python, anything that evaluates to "empty" or zero is `False`. Everything else is `True`.
- **Falsy**: `0`, `0.0`, `""` (empty string), `None`, `[]` (empty list).
- **Truthy**: `5`, `-3`, `"Hello"`, `" "` (space).

### Short-Circuit Evaluation
Python evaluates compound Boolean expressions from left to right and stops reading as soon as the outcome is guaranteed. This returns the *last evaluated value*.

```python
x = True and 6
# Step 1: Python sees True. But it's an 'and', so it MUST check the right side.
# Step 2: It evaluates 6. Since 6 is truthy, the expression is True, but Python returns the actual object 6.
print(x) # Output: 6

y = 5 or 0
# Step 1: Python sees 5. Since an 'or' needs only one True, the whole expression is guaranteed True.
# Step 2: It immediately returns 5 without even looking at the 0.
print(y) # Output: 5
```

---

## 5. Mathematical Flow Control (No `if` Statements)

Suppose you want to print `"Even"` if a number is even, and `"Odd"` if odd, without using an `if` statement. You can combine Booleans and string multiplication!

```python
x = int(input("Enter number: "))
# (x % 2 == 0) gets converted to 1 (True) or 0 (False)
ans = ("Even" * (x % 2 == 0)) + ("Odd" * (x % 2 != 0))
print(ans)
```
If `x = 4`:
- `(4 % 2 == 0)` is True (1). `"Even" * 1 = "Even"`
- `(4 % 2 != 0)` is False (0). `"Odd" * 0 = ""`
- `"Even" + ""` = `"Even"`.

---

## 6. Variables and Operations

### The Walrus Operator (`:=`)
In Python, the standard assignment statement `x = 5` **does not** return a value. 
If you want an assignment to return a value (often to save space in loop headers), use the Walrus operator (Python 3.8+):
```python
# Instead of doing:
# n = input()
# while n != "done":

while (n := input("Type 'done': ")) != "done":
    print(f"You typed {n}")
```

### Unpacking & Swapping Variables
Most languages require a temporary variable to swap two values. Python can swap values cleanly using Tuple Unpacking.
```python
a = 10
b = 20
a, b = b, a   # Python evaluates the right side entirely, then unpacks into the left!
```

### Banker's Rounding
The built-in `round()` function does not perform mathematical half-up rounding (i.e., `.5` always rounding up) to minimize statistical bias in large datasets. It uses **Banker's Algorithm**, rounding precisely half values (`.5`) to the **nearest even integer**.

```python
print(round(1.5)) # Output: 2
print(round(2.5)) # Output: 2
print(round(3.5)) # Output: 4
```
To calculate old-school rounding manually: `int(x + 0.5)` for positive numbers.

---

## 🎯 Practice Problems: Part 2

**Problem 2.1: Division and Arithmetic**
Write a Python program that takes two integer inputs from a user, `A` and `B`. Print:
1. `A` true-divided by `B`
2. `A` floor-divided by `B`
3. The remainder of `A` divided by `B`

**Problem 2.2: Short-Circuit Logic Tracing**
Evaluate the final value returned by each of the following expressions in Python, without running them. Explain *why* Python chose that value based on short-circuiting rules.
1. `var1 = "Hello" or ""`
2. `var2 = "" and "World"`
3. `var3 = 0 or 7 or 10`
4. `var4 = 5 and 10 and 15`

**Problem 2.3: The F-string Receipt**
Ask a user for an item name, a price, and a quantity. Calculate the total cost (price * quantity). Using an f-string, print a perfectly aligned receipt.
- Item Name (left aligned, 15 characters)
- Quantity (centered, 5 characters)
- Total Cost (right aligned, 10 characters, formatted strictly to 2 decimal places with a $).

**Problem 2.4: Tuple Swap Validation**
Write a script that initializes `x = 100`, `y = 200`, `z = 300`.
In a single statement using tuple unpacking, rotate the values so that `x` gets `y`'s value, `y` gets `z`'s value, and `z` gets `x`'s value. Print them out to confirm.

**Problem 2.5: Advanced Boolean String Math**
Without using `if`, `elif`, or `else`, write an expression that evaluates a user integer `N`.
- If `N` is divisible by 3, the result string must contain `"Fizz"`.
- If `N` is divisible by 5, the result string must contain `"Buzz"`.
- If `N` is divisible by 15, the result string is `"FizzBuzz"`.
*Hint: Build on the string multiplication trick.*

**Problem 2.6: Banker's Rounding Verification**
Write a loop that iterates from `0.5` through `5.5` in steps of `1`. For each number, print out its value, the value when `round()` is called, and the value when `int(num + 0.5)` is called. Note where the outputs differ.
# Part 3: Algorithmic Problem Solving and Control Structures

## 1. Using `eval()`
The built-in `eval()` function is a powerful (yet dangerous) tool that takes a string and evaluates it as if it were a valid Python expression.
```python
x = eval("5 + 10")
print(x) # Output: 15
```
It is often used when taking user inputs dynamically, but it poses security risks in production because users can type malicious Python code.

## 2. Floating Point Precision in Financial Software
When dealing with money, never use pure floating points (decimals like `0.53`). You will quickly encounter floating point precision loss, resulting in bugs like `0.5300000000000001`.

### The "Pennies" Technique
Standard practice in Fintech is to convert all user values to integers directly after input. So instead of storing `$1.25` as `1.25`, multiply it by `100` and `round()` it to store `125` pennies. Perform all division and math on the integer `125`.

### Python's `decimal` Module
For environments requiring perfect precision (e.g., banking), Python provides a built-in `decimal` module that handles extremely precise fractional math manually.

---

## 3. Advanced Math-driven Logic (Without `if`)

Before exploring `if` statements, it is healthy to understand how boolean matrices and multipliers can execute branching algorithms linearly.

### Problem: Overtime Calculator
Imagine an employee works `H` hours. They receive `$10/hr` for their first 40 hours. Any hours worked above 40 are given "time and a half" (`$15/hr`). You must write this without an `if` statement.

**Solution Approach**:
- Isolate the Regular Hours: It is `H` if `H < 40`, and `40` if `H >= 40`.
- Isolate the Overtime Hours: It is `0` if `H < 40`, and `H - 40` if `H >= 40`.

```python
hours = int(input("Total hours worked: "))

# Booleans convert to 1 (True) or 0 (False)
reg_hours = (hours * (hours <= 40)) + (40 * (hours > 40))
ot_hours = ((hours - 40) * (hours > 40))

reg_pay = reg_hours * 10
ot_pay = ot_hours * 15
print(f"Total: ${reg_pay + ot_pay}")
```

---

## 4. Control Structures (`if`, `elif`, `else`)

Control structures allow programs to break purely linear execution and execute blocks of code only if exact conditions are met.

### Basic Syntax
```python
x = 5
if x > 3:
    print("Greater than 3")
elif x == 3:
    print("Exactly 3")
else:
    print("Less than 3")
```
- A colon `:` is mathematically required at the end of the condition.
- A block of code is dictated strictly by **indentation** (standard is 4 spaces).

### The "Dangling Else" Problem
In languages like C++ or Java that rely on curly braces `{}`, developers often nest `if` statements but forget braces, resulting in a syntax ambiguity: "Which `if` does this loose `else` attach to?"
- **The Global C++ Rule:** The `else` attaches to the closest preceding `if` that does not already have an `else`.

Python entirely dodges the "Dangling Else" problem. Because Python is strictly indentation-based, an `else` statement attaches exactly to whichever `if` shares its vertical indentation column.

### Default Assumption Pattern
A very common programming trick to simplify branching is to set a "Default Assumption" variable, and only run an `if` statement to correct yourself if the assumption was wrong. This eliminates the need for `else`!

```python
num = 5
ans = "Even"       # Make an assumption
if num % 2 != 0:   # Test for the opposite condition
    ans = "Odd"    # Correct the assumption 
print(ans)         # Prints "Odd"
```

### Checking Range Syntaxes
Instead of checking individual conditions (`if score >= 0 and score <= 100:`), Python lets you chain them naturally:
```python
score = 85
if 0 <= score <= 100:
    print("Valid score.")
```

---

## 5. Algorithmic Breakdown: Palindrome Integer checking

Consider a prompt: *Ask the user for a 4-digit ID number. Verify that it is exactly 4-digits using ranges, and check if it is a Palindrome (reads the same backward and forward) purely using integer arithmetic—no strings allowed!*

**Step 1: Get Input and Verify bounds**
```python
num = int(input("Enter a 4-digit number: "))
if 1000 <= num <= 9999: # Ensures exactly 4 digits without strings
    pass
else:
    print("Error: Must be 4 digits.")
```

**Step 2: Math Breakdown (Given `1221`)**
To break a number apart, we use `//` (floor divide to shave from the right) and `%` (mod by 10 to extract the far right digit).
- `d4 (thousands) = num // 1000` -> `1`
- `temp = num % 1000` -> `221`
- `d3 (hundreds) = temp // 100` -> `2`
- `temp = temp % 100` -> `21`
- `d2 (tens) = temp // 10` -> `2`
- `d1 (ones) = temp % 10` -> `1`

**Step 3: Verification**
```python
if (d4 == d1) and (d3 == d2):
    print("Palindrome!")
```

---

## 🎯 Practice Problems: Part 3

**Problem 3.1: The Secure Coin Exchange**
A user provides a dollar amount (e.g., `4.86`). Write an algorithm that takes this float, cleanly converts it to an integer of pennies to avoid precision defects, and calculates the minimum number of Half Dollars (50¢), Quarters (25¢), Dimes (10¢), Nickels (5¢), and Pennies (1¢) to return. Provide the output organized.

**Problem 3.2: Grading Rubric Evaluation**
Write a Python script that takes a number grade from 0-100. Write the `if/elif/else` chain using Python's combined range syntaxes (e.g., `90 <= grade <= 100`) to assign `"A"`, `"B"`, `"C"`, `"D"`, or `"F"`. Ensure negative values and values over 100 trigger an `"Invalid Scope"` alert.

**Problem 3.3: Finding Max using "Default Assumption"**
Initialize 5 variables to random integers. Create a variable `maximum` and use the "Default Assumption" trick along with a chain of simple `if` statements (no `elif` or `else`) to determine and print the largest distinct value.

**Problem 3.4: Leap Year Math Logic**
Write a system that asks for a year. It must correctly output `True` if it is a leap year, and `False` otherwise.
- Rule 1: A leap year is divisible by 4.
- Rule 2: Exception! If it is divisible by 100, it is NOT a leap year.
- Rule 3: Exception Exception! If it is divisible by 400, it IS a leap year.
Implement this using chained `if/elif` statements.

**Problem 3.5: No-String Palindrome Checking! (5-digit)**
Modify the integer breakdown logic shown in the lesson. Write a script that strictly accepts a 5-digit number (using the correct range boundaries) and mathematically peels off `d5`, `d4`, `d3`, `d2`, `d1` to verify if it is a palindrome entirely using the modulo `%` and floor division `//` operations.
# Part 4: Iteration, Loops, and Advanced Integer Manipulation

## 1. Introduction to Iteration (Loops)
When we need to execute a block of code multiple times, we use loops. Python provides two main loop structures: `while` loops and `for` loops.

### The `while` Loop
A `while` loop runs endlessly as long as its Boolean condition evaluates to `True`.
```python
x = 5
while x > 0:
    print(x)
    x -= 1  # Crucial! Without this, the loop goes to infinity
```

### The `for` Loop and `range()`
Unlike other languages where `for` loops are just syntactic sugar over `while` loops (e.g., `for (int i=0; i<10; i++)`), Python's `for` loop is specifically a "for-in" structure. It iterates over a sequence of items.

The built-in `range()` function generates an iterable sequence of integers:
- `range(stop)`: 0 up to (but not including) `stop`.
- `range(start, stop)`: `start` up to (but not including) `stop`.
- `range(start, stop, step)`: Jumps by `step`.

```python
# Prints 2, 4, 6, 8
for i in range(2, 10, 2):
    print(i)
```

---

## 2. Advanced Integer Reversal (Without Strings)
In previous sections, we learned how to strip digits from an integer using `%` and `//`. Consider how you would construct a completely new integer reversed (e.g., taking `123` and building the pure integer `321`).

**The Algorithm (The Math Trick):**
To build an integer backward, start with an empty accumulator `n = 0`.
Every time you extract a right-most digit from your original variable `x`, you multiply `n` by 10 (shifting all current digits to the left) and add the pulled digit.

```python
x = int(input("Enter number: ")) # e.g., 123
n = 0

while x > 0:
    digit = x % 10     # Extract the far right digit
    n = (n * 10) + digit # Shift 'n' left by multiplying by 10, then add digit
    x = x // 10        # Chop off the far right digit from 'x'
    
print(f"Reversed: {n}")
```
*Trace for 123:*
1. `x = 123`, `digit = 3`, `n = 0 * 10 + 3 = 3`, `x //= 10 = 12`
2. `x = 12`, `digit = 2`, `n = 3 * 10 + 2 = 32`, `x //= 10 = 1`
3. `x = 1`, `digit = 1`, `n = 32 * 10 + 1 = 321`, `x //= 10 = 0`. End of loop.

---

## 3. Name Shadowing Bugs
A major pitfall in Python is that built-in functions behave like variables holding pointers to code. If you define a variable with the exact same name as a built-in function, Python severs the link to the function and assigns the name to your data.

**Example BUG:**
```python
list_of_nums = [1, 2, 3, 4, 5]
sum = 0
for i in list_of_nums:
    sum += i

# Later in your program...
total = sum([10, 20]) # ERROR: 'int' object is not callable!
```
By assigning `sum = 0`, the student destroyed the native `sum()` function. The computer thinks you are typing `0([10, 20])`, which makes no sense. *Never name your variables `sum`, `max`, `min`, `list`, or `str`.*

---

## 4. `break` and the `while...else` Construct

### The `break` Keyword
If you are inside a loop and realize you have immediately found your answer, continuing the loop wastes processing power. The `break` keyword instantly aborts the nearest enclosing loop.

### The Strange `else` in Loops
Python has a very unique idiom: connecting an `else` block to a `while` or `for` loop, rather than an `if` statement!
- **Rule:** The loop's `else` block triggers ONLY if the loop finishes entirely naturally (i.e., its condition naturally becomes `False`). If the loop is forcefully exited via a `break` statement, the `else` block is strictly skipped.

### Practical Application: Prime Number Checking
A prime number is only divisible by `1` and itself. To mathematically check if `x` is prime, loop `i` from `2` up to `x/2`. If `x % i == 0`, it is NOT prime, and we should `break` to avoid wasting time.
If we manage to finish the *entire* loop without breaking, then it MUST be a prime number!

```python
num = int(input("Check Prime: "))
if num <= 1:
    print("Not Prime")
else:
    i = 2
    while i <= num // 2:
        if num % i == 0:
            print("Not Prime")
            break  # Instantly exit the while loop!
        i += 1
    else: 
        # Triggered ONLY if the while loop finished naturally without a break
        print("Prime!")
```

---

## 🎯 Practice Problems: Part 4

**Problem 4.1: Password Gateway**
Write a script that prompts the user for a 4-digit PIN. You have 3 attempts.
1. Use a `while` loop that allows up to 3 tries.
2. Inside the loop, verify the input is both exactly 4 digits, and all digits must be Even.
3. If they enter a valid pin, print "Access Granted" and `break`.
4. If they use all 3 attempts without success, use the `while...else` construct to print "Intruder Alert. System Locked."

**Problem 4.2: Triangle Printer**
Write a script that asks a user for a positive integer `rows`.
Use a `for` loop and string multiplication to print an ascending triangle of stars (`*`), then immediately follow it with a descending triangle.
```
Enter rows: 3
*
**
***
**
*
```

**Problem 4.3: Optimal Odd Summation**
Suppose you need to sum every Odd integer up to `N` where `1 <= N <= 1,000,000`. Writing `if i % 2 != 0: total += i` evaluates a million modulo checks. Write a highly optimized `for` loop using the `range` step argument that loops *exactly* `N/2` times, performing zero `if` checks.

**Problem 4.4: Integer Base Conversion (Binary to Decimal)**
Do not use Python's built-in `int(x, 2)`.
Ask the user for a binary number consisting only of `1`s and `0`s (e.g. `1011`). Read it as a pure integer. Use a `while` loop, `% 10`, and `// 10` to strip digits backward. Mathematically construct the decimal equivalent by utilizing `powers_of_2` increasing incrementally during the loop.

**Problem 4.5: Name Shadowing Diagnostics**
Analyze the following buggy code without running it. Explain what Python error it throws and exactly why.
```python
max = 100
scores = [45, 88, 92, 12, 105]
for s in scores:
    if s > max:
        print("New high score!")

highest = max(scores)
print(f"The highest score was {highest}")
```
# Part 5: Nested Loops, Functions, Closures, and Decorators

## 1. Algorithmic Optimization: The Square Root Prime Check
In earlier sections, we checked if a number `N` was prime by dividing it by every number up to `N // 2`. We can mathematically optimize this.
Factors always come in pairs (e.g., for `N = 100`, factors are `2 * 50`, `4 * 25`, `10 * 10`).
The highest possible "first half" factor pair will occur at the square root of `N`. If you check up to `int(square_root(N))` and find no divisors, you have proven the number is prime without checking the other half. It is a massive performance boost for large numbers.

---

## 2. Nested Loops and `continue`
You can run a loop inside another loop. 
- The inner loop finishes all its cycles *before* the outer loop increments by one.
- The `continue` keyword instantly skips the rest of the *current cycle* of the enclosing loop and jumps back to the top condition.

*Example:*
```python
for outer in range(1, 4):
    for inner in range(1, 4):
        if outer == inner:
            continue # Skips matching numbers
        print(f"X:{outer}, Y:{inner}")
```

---

## 3. Iterables vs. Counters
Python's `for` loop technically does not count. It iterates over a sequence (an iterable) item by item:
- **Strings:** `for letter in "hello":`
- **Lists:** `for item in [10, 20, 30]:`
- **Dictionaries:** `for key in my_dict:`
- **Files:** `for line in my_file:`

---

## 4. Modules and Built-in Libraries
Python comes with built-in modules (libraries) like `math`.
There are several ways to import logic:
1. `import math`: Safest way. Must type `math.sqrt(9)`. It prevents "namespace pollution".
2. `from math import sqrt`: Imports just one tool. You can type `sqrt(9)`.
3. `from math import *`: Imports everything directly into your file. Risky, as you might overwrite existing variables!

You can explore a module using:
- `dir(math)`: Shows you every function available in the math module.
- `help(math.tan)`: Opens the official documentation explaining how the tangent function works.

### Dunder Methods (Magic Methods)
When you type `dir()`, you will see weird properties with double-underscores (e.g., `__add__`). These "dunder" methods are built-in hooks that allow Python objects to interact with standard operators (like using the `+` sign using `__add__`).

---

## 5. Functions
Functions allow you to reuse blocks of code, accept arguments, and calculate returned results.
Definitions begin with the `def` keyword.
- If a function lacks a `return` statement naturally, Python implicitly returns `None`.

### Function Arguments
- **Positional args:** Values match based on position order.
- **Keyword args (Default args):** Parameters can have defaults (e.g., `def greet(name="User"):`). Keyword arguments must be specified at the end of the argument list.
- **Arbitrary args (`*args` // `**kwargs`):** Adding a `*` to an argument (like `*args`) allows the user to pass an infinite number of arguments in, packaged as a Tuple inside the function.

### Pass-by-Value vs. Pass-by-Reference
- Basic datatypes (Integers, Floats, Strings, Booleans) are IMMUTABLE. When passed into a function, they are "Passed by Value". If you modify them inside the function, the original variable outside is untouched.
- Complex datatypes (Lists, Dictionaries) are MUTABLE. When passed into a function, they are "Passed by Reference". If you append a value to a list inside a function, the original list outside the function changes!

---

## 6. Inner Functions, Closures, and Decorators

### Inner Functions and Closures
Unlike languages like C++, Python allows you to define a `def` inside another `def`. Furthermore, the inner function "remembers" the variables of the outer function even after the outer function finishes executing. This captured snapshot of the environment is called a **Closure**.

### Decorators
A decorator is a concept where you pass a function into *another function* to temporarily change its behavior (like strapping a stopwatch around it) without permanently editing its original source code.

```python
# A Timer Decorator
def my_decorator(func_to_decorate):
    def wrapper():
        print("Starting Timer...")
        func_to_decorate()      # Executes the original function
        print("Stopping Timer...")
    return wrapper

def say_hello():
    print("HELLO!")

# We execute it:
decorated_hello = my_decorator(say_hello)
decorated_hello() 
```
Python eventually gives us `@syntactic_sugar` to easily wrap these around our codes.

---

## 🎯 Practice Problems: Part 5

**Problem 5.1: Nested Triangle Pattern**
Write a script using nested loops `for outer in range(1, rows)` and `for inner in range(...)` to print the classic right-aligned descending number grid. (Do not use string multiplication).
```
1
12
123
1234
```

**Problem 5.2: Maximum Divisors Competition**
Using the square root principle from Section 1, write a function `math_check(start, end)` that finds which integer between `start` and `end` (inclusive) has the highest number of factors. Instead of checking up to N/2, optimize the counting of divisors mathematically limiting to the square root.

**Problem 5.3: Immutability Diagnostic Tool**
Write a function `diagnostic_tool(a_number, a_list)`:
1. Adds `100` to `a_number`.
2. Appends `100` to `a_list`.
3. Returns `None`.
Below the function, declare `x = 5` and `y = [5]`. Run `diagnostic_tool(x, y)`. Print `x` and `y`. Observe and write an inline comment explaining why `x` did not change but `y` did.

**Problem 5.4: Custom "Max" Rewrite**
Python has `max()` built-in. Do not use it.
Write your own function `def custom_max(*args):` (noticing the arbitrary star).
Given any number of integers separated by commas `custom_max(4, 9, 21, 3, 10)`, iterate over `args` and return the highest integer. Return `None` if zero integers are passed.

**Problem 5.5: Function Wrapper / Closure**
Write an outer function called `salutation_maker(greeting)` that returns an inner function called `person_greeter`.
The inner function should accept a `name`.
The inner function should print `f"{greeting}, {name}"`.
Usage should look like:
```python
french_greeting = salutation_maker("Bonjour")
french_greeting("Alice")  # Output: Bonjour, Alice

texan_greeting = salutation_maker("Howdy")
texan_greeting("Bob")     # Output: Howdy, Bob
```
# Part 6: Advanced Scoping, Function Properties, and Arguments

## 1. Output Formatting (Grids)
When generating streams of numbers (like primes), printing one per line is messy. You can create a grid by using a `counter`. If the counter hits max column size (e.g., `5`), reset the counter and print an empty string to generate a new line. Using `\t` (Tab) keeps columns perfectly aligned.
```python
counter = 0
for i in range(1, 20):
    print(i, end="\t")
    counter += 1
    if counter == 5:
        print()      # Carriage return
        counter = 0  # Reset
```

## 2. The `pass` Keyword
Python expects indented code blocks after structure statements (`if`, `while`, `def`, `for`). If you are drafting a program and want to leave a block empty temporarily without crashing your program with an `IndentationError`, place the `pass` keyword. It is a "no-op" (does absolutely nothing).

---

## 3. Variable Scoping Rules (LEGB)
When you ask for a variable named `x`, Python searches an exact hierarchy to find it called LEGB:
1. **L - Local:** Inside the current function `def`.
2. **E - Enclosing:** Inside any wrapping outer functions.
3. **G - Global:** Defined at the very top of the script.
4. **B - Built-in:** Native Python names (like `sum`, `len`, `max`).

You can dynamically investigate everything Python sees at the Local or Global levels by calling the `locals()` and `globals()` functions, which return a Dictionary.

### Mutating Outer Scopes
If you want a function to simply *read* a global variable, it finds it automatically. However, if you attempt to *change* it (`x += 1`), Python strictly assumes you want to create a brand brand-new Local variable and throws an `UnboundLocalError`.
- To mutate a **Global** variable inside a function, explicitly declare: `global x` at the top of the function.
- To mutate an **Enclosing** variable inside a nested function, explicitly declare: `nonlocal x`.

---

## 4. Under the Hood: Closures and Cell Objects
Recall that inner functions remember variables from their parent functions even after the parent function closes. Where is this stored if the parent is dead? 
Python physically stores these captured variables inside a special **"Cell Object"**. You can inspect this manually by printing the function's internal attribute: `print(my_function.__closure__)`.

### Dynamic Function Attributes
Because functions in Python are entirely Objects, they have property dictionaries just like classes do. You can completely arbitrarily strap variables onto the outside of a function for storage!
```python
def my_func():
    return "Hello"

my_func.run_count = 0  # Creating a custom attribute on the fly!
my_func.run_count += 1
print(my_func.run_count)
```

---

## 5. The Mutable Default Argument Trap 
This is the most common interview trap in Python.
**Default arguments are evaluated exactly ONCE at the moment the function is defined, NOT every time it is called!**

*The Trap:*
```python
def add_to_list(val, my_list=[]):
    my_list.append(val)
    return my_list

print(add_to_list(1)) # [1]
print(add_to_list(2)) # [1, 2] -- WAIT! We didn't pass [1] in!
```
Because `[]` is mutable, the same physical list persists forever in memory. 
*The Solution:* Use `None`, which is an immutable Singleton.
```python
def add_to_list(val, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(val)
    return my_list
```

---

## 6. Variadic Arguments (`*args`)
Sometimes you don't know exactly how many arguments a user will pass. By placing a `*` before an argument name (standardly `*args`), Python collects all overflowing positional arguments and hands them to you as a Tuple.
Because Tuples are iterable, you can loop through `args` easily.

```python
def product(first_num, *args):
    result = first_num
    for num in args:
        result *= num
    return result

print(product(2, 3, 4, 5)) # Outputs 120
```

---

## 🎯 Practice Problems: Part 6

**Problem 6.1: Advanced Base Conversion Engine (Arithmetic only)**
Write a function `convert_base(number, base_start, base_target)`.
Do not use binary strings or `int(num, base)`.
Assume `number` is a pure integer representation.
1. Use the algorithm `modulo base_start` and multiplying by increasing powers of `base_start` to mathematically convert `number` into Base 10.
2. Use the algorithm `modulo base_target` and floor division `// base_target` building backward to convert the Base 10 number into `base_target`.
Return the mathematical integer. (Example: converting octal `17` base-8 to base-2).

**Problem 6.2: Global vs. Local Diagnostic**
Write a script with a global variable `bank_balance = 500`.
Write a function `deposit(amount)` that correctly mutates the global variable to add the amount.
Write a second buggy function `bad_withdrawal(amount)` that tries to subtract the amount without using the `global` keyword.
Below the definitions, write a multi-line comment explaining the exact error Python will throw when calling `bad_withdrawal` and why.

**Problem 6.3: The Mutable Default Fix**
You inherited buggy code:
```python
def employee_logger(name, log_sheet=[]):
    log_sheet.append(name)
    print(f"Logged today: {log_sheet}")
```
Rewrite this function to properly handle default arguments using the `None` pattern, ensuring that if no list is passed, a fresh empty list is created for every single distinct call.

**Problem 6.4: Variadic Statistics (`*args`)**
Write a function `analyze_numbers(name, *args)`.
If `args` is empty, return `f"{name}: No data"`.
Otherwise, iterate through `args` without using built-in `sum()`, `max()`, or `min()`.
Calculate the sum, the maximum, and the average, and return a formatted string.

**Problem 6.5: Function Attribute Counter**
Create an empty function `def do_nothing(): pass`.
Directly below it, dynamically attach a `.calls` attribute and set it to `0`.
Write a `for` loop that runs 5 times. Inside the loop, run `do_nothing()` and increment `do_nothing.calls` by 1. Print the final count from the function's attribute to prove it tracked the state outside the function's inner logic.
# Part 7: Memory Management, Lists, and Advanced Execution

## 1. Positional-Only and Keyword-Only Arguments
When designing robust functions, you can strictly enforce how users pass arguments:
- `/` (Slash): Forces all arguments **before** it to be positional-only. (The user cannot use `name=value`).
- `*` (Star): Forces all arguments **after** it to be keyword-only. (The user *must* use `name=value`).

*Example:* `def my_func(a, b, /, *, c, d):` dictates `a` and `b` must be positional, and `c` and `d` must be keyword.

---

## 2. Unpacking and Variadic Keyword Arguments (`**kwargs`)
Just like `*args` packs unknown positional arguments into a Tuple, `**kwargs` packs unknown keyword arguments into a Dictionary.
You can iterate through them using standard dictionary methods.
```python
def make_table(data, **kwargs):
    print(data)
    for key, val in kwargs.items():
        print(f"{key} is set to {val}")

make_table("MyData", color="red", width=500)
```

Furthermore, Python allows returning multiple values simply by wrapping them in a comma structure. It implicitly builds a Tuple and "unpacks" it on the receiving end:
```python
def get_coordinates():
    return 10, -5  # Returns the tuple (10, -5)

x, y = get_coordinates() # Unpacks perfectly into two variables
```

---

## 3. Dynamic Execution (`eval` vs `exec`)
Python can compile and run code dynamically at runtime.
- `eval(expression_string)`: Evaluates a single mathematical or standard expression and **returns** its mathematical/evaluative result.
- `exec(code_block_string)`: Compiles and fully executes a multi-line string of raw python code (including `def`, `loops`, etc.) inside the current environment. Very powerful but extremely dangerous if accepting untrusted text.

---

## 4. Scripts vs Modules (`if __name__ == '__main__':`)
Python files can be run directly (as a script) or imported (as a module toolset).
When a file runs directly from the terminal, Python secretly assigns the string `__main__` to its `__name__` property.
When a file is *imported* by another file, its `__name__` becomes its actual filename.
Using `if __name__ == '__main__':` at the bottom of a file creates a sandbox where application logic only runs if the user executed the file directly, allowing the file to still be cleanly imported by others.

---

## 5. Sequence Types and List Basics
A sequence is any set of objects indexed by non-negative integers. Lists, Tuples, and Strings are all sequences.
Unlike arrays in C++, Python lists are heterogeneous (you can mix Strings, Ints, and inner Lists together). In memory, a List is essentially a contiguous block of pointers pointing to various objects scattered around the heap.

Differences in Addition:
- `append(item)` takes exactly one object and glues it to the end of the list as a single element. If you append a list `[1,2]`, the outer list gets `[1,2]` as one slot.
- `extend(iterable)` takes a sequence, breaks it open, and appends the inner items one by one.

---

## 6. Memory: Reference Counting and Interned Objects
Python tracks almost everything using built-in Reference Counters. If 5 variables point to the same string, the string's reference count is 5. If you call `del variable`, Python breaks the pointer and decreases the count to 4. When it drops to 0, a Garbage Collector deletes the underlying object.

### The Small Integer Cache (Interning)
To save memory, upon boot-up Python instantiates static Singleton objects for all integers between `-5` and `256`. Therefore, if you write `x = 5; y = 5`, they will physically point to the exact same memory id. However, if you write `x = 9000; y = 9000`, Python creates two completely different objects in memory.

---

## 7. The Loop-Deleter Trap
A massive source of logical errors comes from attempting to delete items from a list while looping forward through it using an index or iterator.
*The Problem:* When you delete index 2, the list shifts left immediately. Index 3 slides into index 2. The loop increments its counter to check index 3 next... successfully skipping the item that just slid into slot 2.

*The Solution:* If you must delete by index, iterate **backwards** through the list.
```python
for i in range(len(my_list) - 1, -1, -1):
    if my_list[i] == "Bad":
        del my_list[i] 
```

---

## 🎯 Practice Problems: Part 7

**Problem 7.1: Strict Configuration Engine**
Create a function `database_config(ip, port, /, *, user, password)` that prints out the variables.
1. Write a function call that executes properly.
2. Underneath, write a comment explaining exactly why `database_config(ip="127.0.0.1", port=80, user="a", password="b")` will crash the Python interpreter.

**Problem 7.2: Dictionary Keyword Unpacker**
Write a function `process_transaction(action, **kwargs)`.
If `action` is "deposit", iterate through the `kwargs` to total up all numerical values passed in and print the total sum.
Example usage: `process_transaction("deposit", checking=50, savings=100, crypto=40)` -> Should print 190.

**Problem 7.3: The Safe Deleter**
You are given `corrupted_data = [10, "ERROR", 20, 30, "ERROR", "ERROR", 40]`.
Write a backwards `for` loop tracking the index `for i in range(....):` that looks at the indexed position, checks if the value is the string `"ERROR"`, and uses `del corrupted_data[i]` to scrub the list cleanly. After the loop, print the list to confirm all numbers slid down safely.

**Problem 7.4: Identity Verification Proof**
Write a python test using the `is` operator to mathematically prove that Python uses "Interned" Singleton objects for small integers but not large integers. (Compare identity mapping of `a=100` and `b=100` vs `x=5000` and `y=5000`).

**Problem 7.5: Extending vs Appending Sandbox**
Initialize `L = [10, 20]`.
Initialize `M = [30, 40]`.
Write two steps:
1. First, `append` `M` directly to `L`. Print the length of `L`. (Pause to think: What should it be?)
2. Now clear `L` back to `[10, 20]`. Use `extend` to merge `M` into `L`. Print the length of `L`. (What is it now?). 
Write a code comment beside each print explaining the length variance.
