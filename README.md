```
██╗    ██╗ █████╗ ██╗  ██╗███╗   ███╗ █████╗ ███╗   ██╗
██║    ██║██╔══██╗╚██╗██╔╝████╗ ████║██╔══██╗████╗  ██║
██║ █╗ ██║███████║ ╚███╔╝ ██╔████╔██║███████║██╔██╗ ██║
██║███╗██║██╔══██║ ██╔██╗ ██║╚██╔╝██║██╔══██║██║╚██╗██║
╚███╔███╔╝██║  ██║██╔╝ ██╗██║ ╚═╝ ██║██║  ██║██║ ╚████║
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝

    ██████╗ ██╗   ██╗████████╗██╗  ██╗ ██████╗ ███╗   ██╗
    ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔═══██╗████╗  ██║
    ██████╔╝ ╚████╔╝    ██║   ███████║██║   ██║██╔██╗ ██║
    ██╔═══╝   ╚██╔╝     ██║   ██╔══██║██║   ██║██║╚██╗██║
    ██║        ██║      ██║   ██║  ██║╚██████╔╝██║ ╚████║
    ╚═╝        ╚═╝      ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
```

> **"Sleep is for the weak. Python is for the based."**

---

```
  ╔══════════════════════════════════════════════════════╗
  ║   🌙  ONE NIGHT. ONE EXAM. ONE REPO TO RULE THEM.   ║
  ╚══════════════════════════════════════════════════════╝
```

This is the **Waxman Python 1-Nighter** — everything you need to survive (and crush) your intro Python exam, distilled into one repo built at 2am with caffeine and spite.

No fluff. No 4-hour lecture rewatches. Just the good stuff.

---

## 🗂 What's Inside

```
  WaxmanPython/
  │
  ├── 📁 Classes PDF/          ← The actual lecture slides
  │     ├── OOP
  │     ├── Decorators
  │     ├── Generators
  │     ├── Part 4 (Lists, Runtime)
  │     └── Part 5 (Functions, Sets, Matrices)
  │
  ├── 📁 StudyGuides/          ← THE GOODS. Start here.
  │     ├── final_review_sections/   ← Organized last-hour cramming
  │     ├── tricky_sections/         ← The stuff that trips people up
  │     └── *.html                   ← Open in browser for clean reading
  │
  ├── 📁 Practice/             ← Code-along videos (video1–6.py)
  │
  ├── 📁 Questions/            ← Exam practice + midterm 2024
  │
  ├── 📁 extracted_pdf_text/   ← Raw text from all PDFs (searchable)
  │
  ├── 🔥 Python_Final_Last_Hour_Review.html   ← OPEN THIS FIRST
  ├── 🔥 build_last_hour_review.py
  ├── 🔥 build_tricky_exam_sheet.py
  └── 🔥 fetch_youtube_transcript.py
```

---

## ⚡ The 1-Night Game Plan

```
  Hour 1 ──► Open Python_Final_Last_Hour_Review.html
             Read: 00_priority_last_hour.md
             Vibe check: do you know lists & runtime?

  Hour 2 ──► Hit the tricky sections:
              ├── part4_lists_runtime.md
              ├── part5_functions_references.md
              └── dicts_sets_charts.md

  Hour 3 ──► The spicy stuff:
              ├── generators.md
              ├── decorators.md
              └── oop.md

  Hour 4 ──► GRIND:
              ├── Questions/ExamPractice.py
              └── Questions/Midterm2024.py

  Hour 5 ──► Panic review the tricky_sections_additions/
             Sleep (optional)
             Eat something (mandatory)
```

---

## 🧠 Topics Covered

```
  ┌─────────────────────────────────────────────────────┐
  │  ✅  Lists & Runtime Complexity   O(n)? O(1)? Know it │
  │  ✅  Functions, Scope & Modules   global? nonlocal?   │
  │  ✅  Dicts, Sets & Comprehensions  { } gang           │
  │  ✅  Iterators & Generators        yield gang         │
  │  ✅  Decorators                    @wrapper magic     │
  │  ✅  OOP (Classes, Inheritance)    __init__ life      │
  │  ✅  Strings, Files, CSV           open() everything  │
  │  ✅  Matrices & Nested Loops       pain & growth      │
  └─────────────────────────────────────────────────────┘
```

---

## 🔥 Must-Read Files (In Order)

| Priority | File | Why |
|----------|------|-----|
| 🚨 #1 | `Python_Final_Last_Hour_Review.html` | The whole exam in one page |
| 🚨 #2 | `StudyGuides/final_review_sections/00_priority_last_hour.md` | What to hit first |
| 🔥 #3 | `StudyGuides/tricky-python-final-exam-drill.html` | The curveball killer |
| 📖 #4 | `Questions/ExamPractice.py` | Write code, don't just read it |
| 📖 #5 | `Questions/Midterm2024.py` | Real exam, real format |

---

## 🐍 Quick Python Survival Cheatsheet

```python
# List comprehension  →  [expr for x in iterable if cond]
squares = [x**2 for x in range(10) if x % 2 == 0]

# Generator           →  same but lazy (use yield or ())
def gen():
    yield 1; yield 2; yield 3

# Decorator           →  wrap a function, extend behavior
def my_dec(func):
    def wrapper(*args, **kwargs):
        print("before")
        return func(*args, **kwargs)
    return wrapper

# OOP basics
class Animal:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return f"{self.name} says something"

class Dog(Animal):
    def speak(self):           # override
        return f"{self.name} says woof"

# Dict tricks
d = {"a": 1, "b": 2}
d.get("c", 0)                  # safe access, returns 0
{k: v for k, v in d.items()}   # dict comprehension

# File I/O
with open("file.csv", "r") as f:
    for line in f:
        print(line.strip())
```

---

## 💀 Common Exam Traps

```
  ⚠️  Mutable default args:  def f(x=[]) ← DON'T
  ⚠️  is vs ==               (identity vs equality)
  ⚠️  list.sort() vs sorted()  (in-place vs new list)
  ⚠️  generator exhaustion    (you can only iterate once)
  ⚠️  scope: LEGB             (Local → Enclosing → Global → Built-in)
  ⚠️  __str__ vs __repr__     (for humans vs for devs)
  ⚠️  shallow vs deep copy    (copy.copy vs copy.deepcopy)
```

---

## 🛠 Scripts in This Repo

| Script | What it does |
|--------|-------------|
| `build_last_hour_review.py` | Generates the HTML last-hour review |
| `build_tricky_exam_sheet.py` | Builds the tricky exam drill sheet |
| `extract_class_pdfs.py` | Pulls text from all lecture PDFs |
| `fetch_youtube_transcript.py` | Grabs transcripts from lecture videos |

---

```
  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │    You got this. The exam is just Python.               │
  │    Python is just reading and writing lists.            │
  │    You've been doing that your whole life.              │
  │                                                         │
  │         now go get that A                               │
  │                         🐍                             │
  └─────────────────────────────────────────────────────────┘
```

---

*Built in one night. Powered by caffeine. Dedicated to everyone who opened their textbook at 11pm.*
