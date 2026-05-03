# 09 — Modules & Packages

## What it is

A **module** is simply a `.py` file containing Python code you can reuse. A **package** is a folder of modules with an `__init__.py` file. As projects grow, splitting code into modules keeps things organized, testable, and reusable — exactly what production data pipelines require.

---

## Key Concepts

- **`import`** — bring a module into scope
- **`from ... import`** — import specific names
- **`as`** — alias for a module
- **`__init__.py`** — makes a folder a package
- **Standard library** — built-in modules (no install needed)
- **Third-party packages** — installed via `pip`
- **`__name__ == "__main__"`** — run code only when script is executed directly
- **Virtual environments** — isolated Python environments per project
- **`requirements.txt`** — list of project dependencies

---

## Code Examples

```python
# --- Importing modules ---
import os
import sys
import math
import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter

# --- Using standard library ---
print(os.getcwd())                    # current directory
print(sys.version)                    # Python version
print(math.sqrt(144))                 # 12.0
print(datetime.now())                 # current datetime
print(datetime.now() - timedelta(days=7))  # 7 days ago

# --- from ... import ---
from math import sqrt, pi
print(sqrt(16))   # 4.0
print(pi)         # 3.14159...

# --- Aliases ---
import numpy as np
import pandas as pd
from datetime import datetime as dt

# --- Creating your own module ---
# utils.py
def clean_string(s: str) -> str:
    return s.strip().lower()

def to_snake_case(s: str) -> str:
    return s.strip().lower().replace(" ", "_")

# main.py
from utils import clean_string, to_snake_case
print(clean_string("  Hello World  "))  # hello world
print(to_snake_case("Sales ETL"))       # sales_etl

# --- __name__ == "__main__" ---
# This block only runs when the file is executed directly,
# not when it's imported as a module

def main():
    print("Running pipeline...")

if __name__ == "__main__":
    main()

# --- Package structure ---
# my_pipeline/
# ├── __init__.py
# ├── extract.py
# ├── transform.py
# ├── load.py
# └── utils/
#     ├── __init__.py
#     ├── logging.py
#     └── validation.py

# extract.py
def extract_from_blob(container: str, blob: str) -> list[dict]:
    print(f"Extracting {blob} from {container}")
    return []

# __init__.py (expose public interface)
from .extract import extract_from_blob
from .transform import transform_data
from .load import load_to_snowflake

# Using the package
from my_pipeline import extract_from_blob
data = extract_from_blob("raw", "sales.csv")

# --- Useful standard library modules for data engineering ---
import os
import sys
import json
import csv
import logging
import argparse
import datetime
from pathlib import Path
from collections import defaultdict, Counter, OrderedDict
from itertools import chain, islice, groupby
from functools import reduce, partial, lru_cache

# defaultdict — dict with default values
word_count = defaultdict(int)
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
for word in words:
    word_count[word] += 1
print(dict(word_count))  # {'apple': 3, 'banana': 2, 'cherry': 1}

# Counter
counter = Counter(words)
print(counter.most_common(2))  # [('apple', 3), ('banana', 2)]

# lru_cache — memoization
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    print(f"Computing for {n}...")
    return n ** 2

print(expensive_computation(5))  # computes
print(expensive_computation(5))  # from cache — no print

# argparse — command line arguments
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run ETL pipeline")
    parser.add_argument("--source", required=True, help="Source name")
    parser.add_argument("--env", default="prod", choices=["dev", "staging", "prod"])
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()

# Run: python pipeline.py --source sales --env dev --dry-run
```

---

## Exercises

### Exercise 1 — Standard library
Use the `collections.Counter` to count word frequencies in a sentence, then print the top 3 most common words.

```python
sentence = "the quick brown fox jumps over the lazy dog the fox"
```

<details>
<summary>Solution</summary>

```python
from collections import Counter

sentence = "the quick brown fox jumps over the lazy dog the fox"
words = sentence.split()
counter = Counter(words)
print(counter.most_common(3))
```
</details>

---

### Exercise 2 — Create a module
Create a file `string_utils.py` with three functions:
- `clean(s)` — strips and lowercases
- `to_snake_case(s)` — replaces spaces with underscores and lowercases
- `truncate(s, max_len)` — returns the string truncated to `max_len` characters

Then import and use them in a main script.

<details>
<summary>Solution</summary>

```python
# string_utils.py
def clean(s: str) -> str:
    return s.strip().lower()

def to_snake_case(s: str) -> str:
    return s.strip().lower().replace(" ", "_")

def truncate(s: str, max_len: int) -> str:
    return s[:max_len] if len(s) > max_len else s

# main.py
from string_utils import clean, to_snake_case, truncate

print(clean("  Hello World  "))
print(to_snake_case("Sales ETL Pipeline"))
print(truncate("This is a very long string", 10))
```
</details>

---

### Exercise 3 — __name__ == "__main__"
Write a module `calculator.py` with functions `add`, `subtract`, `multiply`, `divide`. At the bottom, add a `__main__` block that runs a quick demo of all four functions.

<details>
<summary>Solution</summary>

```python
# calculator.py
def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == "__main__":
    print(add(10, 5))
    print(subtract(10, 5))
    print(multiply(10, 5))
    print(divide(10, 5))
```
</details>

---

### Exercise 4 — defaultdict
Given a list of log entries, use `defaultdict(list)` to group them by log level.

```python
logs = [
    ("INFO", "Pipeline started"),
    ("ERROR", "Connection failed"),
    ("INFO", "Reading data"),
    ("WARNING", "Slow query"),
    ("ERROR", "Schema mismatch"),
    ("INFO", "Pipeline complete"),
]
```

<details>
<summary>Solution</summary>

```python
from collections import defaultdict

logs = [
    ("INFO", "Pipeline started"),
    ("ERROR", "Connection failed"),
    ("INFO", "Reading data"),
    ("WARNING", "Slow query"),
    ("ERROR", "Schema mismatch"),
    ("INFO", "Pipeline complete"),
]

grouped = defaultdict(list)
for level, message in logs:
    grouped[level].append(message)

for level, messages in grouped.items():
    print(f"{level}: {messages}")
```
</details>

---

## Common Mistakes

```python
# ❌ Circular imports — module A imports B, B imports A
# solution: restructure or use lazy imports inside functions

# ❌ Polluting namespace with wildcard imports
from math import *   # imports everything — unclear what's available

# ✅ Import explicitly
from math import sqrt, pi

# ❌ Shadowing built-in names
list = [1, 2, 3]       # overrides built-in list
print = "hello"        # overrides print function

# ❌ Not using __main__ guard — code runs on import
# pipeline.py
run_pipeline()  # runs when imported, not just when executed

# ✅
if __name__ == "__main__":
    run_pipeline()
```

---

## Resources

- [Python modules — official docs](https://docs.python.org/3/tutorial/modules.html)
- [Python standard library](https://docs.python.org/3/library/)
- [Real Python — packages](https://realpython.com/python-modules-packages/)
