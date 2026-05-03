# 03 — Functions

## What it is

A function is a reusable block of code that performs a specific task. Instead of repeating the same logic multiple times, you define it once and call it whenever needed. Good functions do one thing, do it well, and have a clear name.

---

## Key Concepts

- **def** — define a function
- **return** — send a value back to the caller
- **Parameters vs arguments** — parameters are in the definition, arguments are what you pass
- **Default parameters** — fallback values if no argument is given
- **\*args** — variable number of positional arguments
- **\*\*kwargs** — variable number of keyword arguments
- **Lambda** — anonymous one-line function
- **Docstrings** — documentation inside the function
- **First-class functions** — functions can be passed as arguments and returned

---

## Code Examples

```python
# --- Basic function ---
def greet(name):
    return f"Hello, {name}!"

print(greet("Ruben"))  # Hello, Ruben!

# --- Default parameters ---
def greet(name, role="Data Engineer"):
    return f"Hello, {name}! You are a {role}."

print(greet("Ruben"))                        # uses default
print(greet("Ruben", role="Data Analyst"))   # overrides default

# --- Multiple return values ---
def min_max(numbers):
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 9, 5, 7])
print(low, high)  # 1 9

# --- *args (variable positional arguments) ---
def total(*numbers):
    return sum(numbers)

print(total(1, 2, 3))       # 6
print(total(10, 20, 30, 40)) # 100

# --- **kwargs (variable keyword arguments) ---
def log_event(**details):
    for key, value in details.items():
        print(f"{key}: {value}")

log_event(pipeline="sales_etl", status="success", duration_s=42)

# --- Combining all parameter types ---
def pipeline_run(name, *tables, env="prod", **metadata):
    print(f"Running {name} in {env}")
    print(f"Tables: {tables}")
    print(f"Metadata: {metadata}")

pipeline_run("sales_etl", "orders", "customers", env="dev", team="data")

# --- Lambda (anonymous function) ---
square = lambda x: x ** 2
print(square(5))  # 25

# Used with sorted, map, filter
numbers = [5, 2, 8, 1, 9]
sorted_numbers = sorted(numbers, key=lambda x: -x)  # descending
print(sorted_numbers)  # [9, 8, 5, 2, 1]

# --- map and filter ---
doubled = list(map(lambda x: x * 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))

# --- Docstrings ---
def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers: A list of numeric values.

    Returns:
        The arithmetic mean as a float.

    Raises:
        ValueError: If the list is empty.
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)

# --- Functions as first-class objects ---
def apply(func, value):
    return func(value)

def double(x):
    return x * 2

print(apply(double, 5))   # 10
print(apply(square, 5))   # 25

# --- Returning a function (closure) ---
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

triple = multiplier(3)
print(triple(7))   # 21
```

---

## Exercises

### Exercise 1 — Basic function
Write a function `celsius_to_fahrenheit(celsius)` that converts a temperature. Formula: `F = (C × 9/5) + 32`. Test it with 0, 100, and 37.

<details>
<summary>Solution</summary>

```python
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

for temp in [0, 100, 37]:
    print(f"{temp}°C = {celsius_to_fahrenheit(temp)}°F")
```
</details>

---

### Exercise 2 — Default parameters
Write a function `create_pipeline(name, source, destination, schedule="daily", is_active=True)` that returns a dict with all those values.

<details>
<summary>Solution</summary>

```python
def create_pipeline(name, source, destination, schedule="daily", is_active=True):
    return {
        "name": name,
        "source": source,
        "destination": destination,
        "schedule": schedule,
        "is_active": is_active
    }

p = create_pipeline("sales_etl", "Azure Blob", "Snowflake")
print(p)

p2 = create_pipeline("orders_etl", "SQL Server", "Databricks", schedule="hourly")
print(p2)
```
</details>

---

### Exercise 3 — *args
Write a function `summarize(*values)` that returns a dict with the count, sum, min, max, and average of the values passed.

<details>
<summary>Solution</summary>

```python
def summarize(*values):
    return {
        "count": len(values),
        "sum": sum(values),
        "min": min(values),
        "max": max(values),
        "average": sum(values) / len(values)
    }

print(summarize(10, 20, 30, 40, 50))
```
</details>

---

### Exercise 4 — Lambda + sorted
Given a list of pipeline dicts, sort them by `duration_s` in descending order using a lambda.

```python
pipelines = [
    {"name": "sales_etl", "duration_s": 120},
    {"name": "orders_etl", "duration_s": 45},
    {"name": "products_etl", "duration_s": 300},
    {"name": "customers_etl", "duration_s": 90},
]
```

<details>
<summary>Solution</summary>

```python
sorted_pipelines = sorted(pipelines, key=lambda p: p["duration_s"], reverse=True)
for p in sorted_pipelines:
    print(f"{p['name']}: {p['duration_s']}s")
```
</details>

---

### Exercise 5 — Closure
Write a function `make_multiplier(n)` that returns a function which multiplies its input by `n`. Use it to create a `double` and a `triple` function.

<details>
<summary>Solution</summary>

```python
def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```
</details>

---

## Common Mistakes

```python
# ❌ Mutable default argument — shared across all calls
def add_item(item, my_list=[]):
    my_list.append(item)
    return my_list

add_item("a")  # ['a']
add_item("b")  # ['a', 'b'] ← bug! list persists between calls

# ✅ Use None as default
def add_item(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list

# ❌ Forgetting to return
def double(x):
    x * 2  # calculates but returns None

# ❌ Too many responsibilities in one function
def process_data(data):
    # reads, cleans, transforms, writes, sends email — too much!
    pass

# ✅ One function, one responsibility
def clean_data(data): ...
def transform_data(data): ...
def write_data(data): ...
```

---

## Resources

- [Python functions — official docs](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Real Python — functions](https://realpython.com/defining-your-own-python-function/)
- [Real Python — lambda](https://realpython.com/python-lambda/)
