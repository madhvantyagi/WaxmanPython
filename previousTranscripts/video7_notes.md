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
