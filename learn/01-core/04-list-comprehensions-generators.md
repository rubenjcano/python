# 04 — List Comprehensions & Generators

## What it is

**List comprehensions** are a concise way to create lists from existing sequences, replacing many `for` loops with a single readable line.

**Generators** are like list comprehensions but they don't create the full list in memory — they produce values one at a time, making them far more efficient for large datasets.

---

## Key Concepts

- **List comprehension** — `[expression for item in iterable if condition]`
- **Dict comprehension** — `{key: value for item in iterable}`
- **Set comprehension** — `{expression for item in iterable}`
- **Generator expression** — `(expression for item in iterable)` — lazy, memory-efficient
- **`yield`** — turns a function into a generator
- **`next()`** — get the next value from a generator
- **Lazy evaluation** — values are computed only when needed

---

## Code Examples

```python
# --- List comprehension ---
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Traditional for loop
squares = []
for n in numbers:
    squares.append(n ** 2)

# List comprehension — same result, cleaner
squares = [n ** 2 for n in numbers]
print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# --- With condition (filter) ---
evens = [n for n in numbers if n % 2 == 0]
print(evens)  # [2, 4, 6, 8, 10]

even_squares = [n ** 2 for n in numbers if n % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]

# --- Transforming strings ---
names = ["alice", "bob", "charlie"]
upper_names = [name.upper() for name in names]
print(upper_names)  # ['ALICE', 'BOB', 'CHARLIE']

# --- Flattening a nested list ---
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# --- Dict comprehension ---
prices = {"apple": 1.2, "banana": 0.5, "cherry": 2.0}

# Apply a 10% discount
discounted = {item: round(price * 0.9, 2) for item, price in prices.items()}
print(discounted)

# Filter items over €1
expensive = {item: price for item, price in prices.items() if price > 1.0}
print(expensive)

# --- Set comprehension ---
words = ["hello", "world", "hello", "python", "world"]
unique_words = {word for word in words}
print(unique_words)  # {'hello', 'world', 'python'}

# --- Generator expression ---
# Like a list comprehension but uses () and is lazy
gen = (n ** 2 for n in range(1_000_000))  # no memory allocated yet

print(next(gen))  # 0 — computes first value
print(next(gen))  # 1 — computes second value

# Sum without building a list
total = sum(n ** 2 for n in range(1_000_000))  # memory efficient

# --- Generator function with yield ---
def even_numbers(limit):
    """Yields even numbers up to limit one at a time."""
    for n in range(2, limit + 1, 2):
        yield n

for num in even_numbers(10):
    print(num)  # 2, 4, 6, 8, 10

# Reading a large file line by line with a generator
def read_large_file(filepath):
    with open(filepath, "r") as f:
        for line in f:
            yield line.strip()

# --- Chaining generators (pipeline pattern) ---
def read_numbers(data):
    for n in data:
        yield n

def filter_evens(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n

def square(numbers):
    for n in numbers:
        yield n ** 2

data = range(1, 11)
pipeline = square(filter_evens(read_numbers(data)))
print(list(pipeline))  # [4, 16, 36, 64, 100]
```

---

## Exercises

### Exercise 1 — Basic list comprehension
Given `numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`:
- Create a list of cubes of all odd numbers
- Create a list of strings like `"number_1"`, `"number_2"`, etc.

<details>
<summary>Solution</summary>

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

odd_cubes = [n ** 3 for n in numbers if n % 2 != 0]
print(odd_cubes)  # [1, 27, 125, 343, 729]

labels = [f"number_{n}" for n in numbers]
print(labels)
```
</details>

---

### Exercise 2 — Dict comprehension
Given a list of pipeline names, create a dict where each name maps to its length (number of characters).

```python
pipelines = ["sales_etl", "orders_pipeline", "customers_sync", "products_load"]
```

<details>
<summary>Solution</summary>

```python
pipelines = ["sales_etl", "orders_pipeline", "customers_sync", "products_load"]
name_lengths = {name: len(name) for name in pipelines}
print(name_lengths)
```
</details>

---

### Exercise 3 — Filtering with comprehension
Given a list of log entries, use a list comprehension to extract only the `"ERROR"` entries and return just the message part.

```python
logs = [
    "INFO: Pipeline started",
    "ERROR: Connection timeout",
    "INFO: Reading data",
    "ERROR: Schema mismatch",
    "INFO: Pipeline finished",
]
```

<details>
<summary>Solution</summary>

```python
errors = [log.replace("ERROR: ", "") for log in logs if log.startswith("ERROR")]
print(errors)  # ['Connection timeout', 'Schema mismatch']
```
</details>

---

### Exercise 4 — Generator function
Write a generator `fibonacci(n)` that yields the first `n` Fibonacci numbers.

<details>
<summary>Solution</summary>

```python
def fibonacci(n):
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

print(list(fibonacci(10)))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```
</details>

---

### Exercise 5 — Generator pipeline
Write a generator pipeline that:
1. Takes a list of raw strings (simulating CSV rows)
2. Strips whitespace
3. Filters out empty rows
4. Splits each row by comma

```python
raw_rows = ["  Alice, 28, Barcelona  ", "  ", "Bob, 35, Madrid", "", "  Charlie, 22, Valencia  "]
```

<details>
<summary>Solution</summary>

```python
raw_rows = ["  Alice, 28, Barcelona  ", "  ", "Bob, 35, Madrid", "", "  Charlie, 22, Valencia  "]

def strip_rows(rows):
    for row in rows:
        yield row.strip()

def filter_empty(rows):
    for row in rows:
        if row:
            yield row

def split_rows(rows):
    for row in rows:
        yield [field.strip() for field in row.split(",")]

pipeline = split_rows(filter_empty(strip_rows(raw_rows)))
for row in pipeline:
    print(row)
```
</details>

---

## Common Mistakes

```python
# ❌ Over-complicated comprehension — hard to read
result = [x * y for x in range(10) for y in range(10) if x != y if x % 2 == 0]
# Use a regular for loop when logic is complex

# ❌ Using a list comprehension when you only need to iterate (waste of memory)
[print(n) for n in range(10)]  # creates a list of None values
# ✅
for n in range(10):
    print(n)

# ❌ Consuming a generator twice
gen = (n for n in range(5))
print(list(gen))  # [0, 1, 2, 3, 4]
print(list(gen))  # [] — generator is exhausted!

# ✅ Re-create the generator or use a list if you need to iterate multiple times
```

---

## Resources

- [Python list comprehensions — official docs](https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions)
- [Real Python — list comprehensions](https://realpython.com/list-comprehension-python/)
- [Real Python — generators](https://realpython.com/introduction-to-python-generators/)
