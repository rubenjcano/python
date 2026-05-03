# 01 — Data Types

## What it is

Python has built-in data types that define what kind of value a variable holds and what operations you can perform on it. Unlike some languages, Python is dynamically typed — you don't declare types explicitly, Python figures it out at runtime.

---

## Key Concepts

### Primitive types

| Type | Example | Description |
|---|---|---|
| `int` | `42` | Whole numbers |
| `float` | `3.14` | Decimal numbers |
| `str` | `"hello"` | Text |
| `bool` | `True / False` | Boolean values |
| `NoneType` | `None` | Absence of value |

### Collection types

| Type | Example | Ordered | Mutable | Duplicates |
|---|---|---|---|---|
| `list` | `[1, 2, 3]` | ✅ | ✅ | ✅ |
| `tuple` | `(1, 2, 3)` | ✅ | ❌ | ✅ |
| `set` | `{1, 2, 3}` | ❌ | ✅ | ❌ |
| `dict` | `{"a": 1}` | ✅ (Python 3.7+) | ✅ | Keys: ❌ |

---

## Code Examples

```python
# --- Primitives ---
age = 28
price = 9.99
name = "Ruben"
is_active = True
result = None

print(type(age))       # <class 'int'>
print(type(price))     # <class 'float'>
print(type(name))      # <class 'str'>

# --- String operations ---
greeting = "hello world"
print(greeting.upper())          # HELLO WORLD
print(greeting.replace("hello", "hi"))  # hi world
print(greeting.split(" "))       # ['hello', 'world']
print(f"Name: {name}, Age: {age}")  # f-strings

# --- List ---
fruits = ["apple", "banana", "cherry"]
fruits.append("mango")
fruits.remove("banana")
print(fruits[0])       # apple
print(fruits[-1])      # mango
print(fruits[1:3])     # slicing

# --- Tuple (immutable) ---
coordinates = (40.7128, -74.0060)
lat, lon = coordinates  # unpacking
print(lat)             # 40.7128

# --- Set (unique values only) ---
tags = {"python", "azure", "python"}
print(tags)            # {'python', 'azure'} — no duplicates

# --- Dict ---
person = {"name": "Ruben", "age": 28, "city": "Barcelona"}
print(person["name"])          # Ruben
print(person.get("country", "unknown"))  # safe access with default
person["role"] = "Data Engineer"  # add key
for key, value in person.items():
    print(f"{key}: {value}")

# --- Type conversion ---
num_str = "42"
num_int = int(num_str)
num_float = float(num_str)
back_to_str = str(num_int)

# --- Checking types ---
print(isinstance(age, int))    # True
print(isinstance(name, str))   # True
```

---

## Exercises

### Exercise 1 — Basic types
Create variables for your name, age, city, and whether you are a data engineer. Print them all using an f-string.

<details>
<summary>Solution</summary>

```python
name = "Ruben"
age = 28
city = "Barcelona"
is_data_engineer = True

print(f"Name: {name}, Age: {age}, City: {city}, Data Engineer: {is_data_engineer}")
```
</details>

---

### Exercise 2 — List operations
Given the list `numbers = [5, 3, 8, 1, 9, 2, 7]`:
- Sort it in ascending order
- Get the first 3 elements
- Get the last element
- Add the number `10` to the end
- Remove the number `3`

<details>
<summary>Solution</summary>

```python
numbers = [5, 3, 8, 1, 9, 2, 7]

numbers.sort()
print(numbers)         # [1, 2, 3, 5, 7, 8, 9]
print(numbers[:3])     # [1, 2, 3]
print(numbers[-1])     # 9
numbers.append(10)
numbers.remove(3)
print(numbers)         # [1, 2, 5, 7, 8, 9, 10]
```
</details>

---

### Exercise 3 — Dict operations
Create a dictionary representing a data pipeline with keys: `name`, `source`, `destination`, `is_active`. Then:
- Print the pipeline name
- Add a `schedule` key with value `"daily"`
- Loop through all key-value pairs and print them

<details>
<summary>Solution</summary>

```python
pipeline = {
    "name": "sales_etl",
    "source": "Azure Blob Storage",
    "destination": "Snowflake",
    "is_active": True
}

print(pipeline["name"])

pipeline["schedule"] = "daily"

for key, value in pipeline.items():
    print(f"{key}: {value}")
```
</details>

---

### Exercise 4 — Sets
Given two lists of tags:
```python
tags_project_a = ["python", "azure", "etl", "sql"]
tags_project_b = ["python", "databricks", "sql", "spark"]
```
Find: the tags in common, the tags unique to project A, and all unique tags combined.

<details>
<summary>Solution</summary>

```python
tags_project_a = {"python", "azure", "etl", "sql"}
tags_project_b = {"python", "databricks", "sql", "spark"}

print(tags_project_a & tags_project_b)  # intersection: {'python', 'sql'}
print(tags_project_a - tags_project_b)  # difference: {'azure', 'etl'}
print(tags_project_a | tags_project_b)  # union: all unique tags
```
</details>

---

### Exercise 5 — Type conversion
You receive data as strings from a CSV file: `"42"`, `"3.14"`, `"True"`. Convert them to their correct Python types and print the type of each result.

<details>
<summary>Solution</summary>

```python
raw_int = "42"
raw_float = "3.14"
raw_bool = "True"

converted_int = int(raw_int)
converted_float = float(raw_float)
converted_bool = raw_bool == "True"  # string comparison

print(converted_int, type(converted_int))     # 42 <class 'int'>
print(converted_float, type(converted_float)) # 3.14 <class 'float'>
print(converted_bool, type(converted_bool))   # True <class 'bool'>
```
</details>

---

## Common Mistakes

```python
# ❌ Mutable default argument in functions (covered more in functions.md)
def add_item(item, my_list=[]):
    my_list.append(item)
    return my_list

# ❌ Modifying a list while iterating over it
numbers = [1, 2, 3, 4, 5]
for n in numbers:
    if n % 2 == 0:
        numbers.remove(n)  # skips elements — use list comprehension instead

# ✅ Correct way
numbers = [n for n in numbers if n % 2 != 0]

# ❌ Using == to compare with None
if result == None:  # works but not idiomatic
    pass

# ✅ Correct way
if result is None:
    pass
```

---

## Resources

- [Python built-in types — official docs](https://docs.python.org/3/library/stdtypes.html)
- [Real Python — Lists and Tuples](https://realpython.com/python-lists-tuples/)
- [Real Python — Dictionaries](https://realpython.com/python-dicts/)
