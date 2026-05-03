# 06 — Error Handling

## What it is

Errors are inevitable in real programs — files don't exist, APIs fail, data is malformed. Error handling lets you anticipate these situations and respond gracefully instead of crashing. In Python, errors are **exceptions** — objects that represent something going wrong.

---

## Key Concepts

- **Exception** — an error that disrupts normal program flow
- **`try / except`** — attempt code, catch errors if they occur
- **`else`** — runs if no exception was raised
- **`finally`** — always runs, regardless of exception (cleanup)
- **`raise`** — manually trigger an exception
- **Custom exceptions** — your own exception classes
- **Exception hierarchy** — all exceptions inherit from `BaseException`
- **`as e`** — capture the exception object for inspection

---

## Code Examples

```python
# --- Basic try/except ---
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")

# --- Catching multiple exceptions ---
def parse_value(raw):
    try:
        return int(raw)
    except ValueError:
        print(f"Cannot convert '{raw}' to int")
        return None
    except TypeError:
        print("Input must be a string or number")
        return None

# --- Catching any exception (use sparingly) ---
try:
    risky_operation()
except Exception as e:
    print(f"Something went wrong: {e}")
    print(f"Error type: {type(e).__name__}")

# --- else and finally ---
def read_file(filepath):
    try:
        f = open(filepath, "r")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    else:
        content = f.read()  # runs only if no exception
        return content
    finally:
        print("Attempted to read file")  # always runs

# --- Context manager (preferred for resources) ---
def read_file(filepath):
    try:
        with open(filepath, "r") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None

# --- raise ---
def calculate_average(numbers):
    if not numbers:
        raise ValueError("Cannot calculate average of an empty list")
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise TypeError("All values must be numeric")
    return sum(numbers) / len(numbers)

try:
    print(calculate_average([]))
except ValueError as e:
    print(f"Error: {e}")

# --- Re-raising exceptions ---
def load_data(filepath):
    try:
        with open(filepath) as f:
            return f.read()
    except FileNotFoundError as e:
        print("Logging error...")
        raise  # re-raises the original exception

# --- Custom exceptions ---
class PipelineError(Exception):
    """Base exception for pipeline errors."""
    pass

class ConnectionError(PipelineError):
    """Raised when a pipeline cannot connect to a source."""
    def __init__(self, source, message="Connection failed"):
        self.source = source
        self.message = message
        super().__init__(f"{message}: {source}")

class SchemaError(PipelineError):
    """Raised when data doesn't match the expected schema."""
    pass

# Using custom exceptions
def connect_to_source(source):
    if source == "unreachable_db":
        raise ConnectionError(source)
    print(f"Connected to {source}")

try:
    connect_to_source("unreachable_db")
except ConnectionError as e:
    print(f"Pipeline failed — {e}")
    print(f"Source: {e.source}")
except PipelineError as e:
    print(f"General pipeline error: {e}")

# --- Exception chaining ---
def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        raise PipelineError("Could not load pipeline config") from e

# --- Practical pattern: pipeline with error handling ---
import logging

logging.basicConfig(level=logging.INFO)

def run_pipeline(name, steps):
    logging.info(f"Starting pipeline: {name}")
    for step in steps:
        try:
            step()
            logging.info(f"Step {step.__name__} completed")
        except Exception as e:
            logging.error(f"Step {step.__name__} failed: {e}")
            raise PipelineError(f"Pipeline {name} failed at {step.__name__}") from e
    logging.info(f"Pipeline {name} completed successfully")
```

---

## Exercises

### Exercise 1 — Basic exception handling
Write a function `safe_divide(a, b)` that returns `a / b` but handles `ZeroDivisionError` and `TypeError`, returning `None` in both cases and printing a helpful message.

<details>
<summary>Solution</summary>

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero")
        return None
    except TypeError:
        print(f"Error: Cannot divide {type(a).__name__} by {type(b).__name__}")
        return None

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))    # None
print(safe_divide(10, "2"))  # None
```
</details>

---

### Exercise 2 — File handling
Write a function `load_csv(filepath)` that opens a file, reads all lines, and returns them as a list. Handle `FileNotFoundError` and `PermissionError` with meaningful messages.

<details>
<summary>Solution</summary>

```python
def load_csv(filepath):
    try:
        with open(filepath, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return []
    except PermissionError:
        print(f"Permission denied: {filepath}")
        return []

lines = load_csv("data.csv")
```
</details>

---

### Exercise 3 — Custom exception
Create a `ValidationError` custom exception. Write a function `validate_age(age)` that raises `ValidationError` if age is not an integer, is negative, or is over 150.

<details>
<summary>Solution</summary>

```python
class ValidationError(Exception):
    pass

def validate_age(age):
    if not isinstance(age, int):
        raise ValidationError(f"Age must be an integer, got {type(age).__name__}")
    if age < 0:
        raise ValidationError(f"Age cannot be negative: {age}")
    if age > 150:
        raise ValidationError(f"Age is unrealistically high: {age}")
    return True

for test in [25, -5, 200, "old"]:
    try:
        validate_age(test)
        print(f"{test} is valid")
    except ValidationError as e:
        print(f"Invalid: {e}")
```
</details>

---

### Exercise 4 — finally for cleanup
Write a function `process_file(filepath)` that opens a file, processes it, and always prints "Processing complete" at the end whether or not an error occurred.

<details>
<summary>Solution</summary>

```python
def process_file(filepath):
    try:
        with open(filepath, "r") as f:
            data = f.read()
            print(f"Processed {len(data)} characters")
            return data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    finally:
        print("Processing complete")

process_file("existing.txt")
process_file("missing.txt")
```
</details>

---

### Exercise 5 — Pipeline error handling
Write a `run_etl(source, destination)` function that:
- Raises `ConnectionError` if source is `"offline"`
- Raises `SchemaError` if destination is `"incompatible"`
- Prints success otherwise
- Catches both with appropriate messages

<details>
<summary>Solution</summary>

```python
class PipelineError(Exception):
    pass

class ConnectionError(PipelineError):
    pass

class SchemaError(PipelineError):
    pass

def run_etl(source, destination):
    try:
        if source == "offline":
            raise ConnectionError(f"Cannot connect to source: {source}")
        if destination == "incompatible":
            raise SchemaError(f"Schema mismatch at destination: {destination}")
        print(f"ETL from {source} to {destination} completed successfully")
    except ConnectionError as e:
        print(f"Connection failed: {e}")
    except SchemaError as e:
        print(f"Schema error: {e}")

run_etl("azure_blob", "snowflake")
run_etl("offline", "snowflake")
run_etl("azure_blob", "incompatible")
```
</details>

---

## Common Mistakes

```python
# ❌ Catching all exceptions silently — hides bugs
try:
    risky_code()
except:
    pass  # never do this

# ❌ Catching Exception too broadly
try:
    result = int(user_input)
except Exception:
    print("Something went wrong")  # not helpful

# ✅ Catch specific exceptions
try:
    result = int(user_input)
except ValueError:
    print(f"'{user_input}' is not a valid number")

# ❌ Using exceptions for control flow
try:
    value = my_dict["key"]
except KeyError:
    value = "default"

# ✅ Use .get() instead
value = my_dict.get("key", "default")

# ❌ Losing the original exception
try:
    risky()
except Exception as e:
    raise RuntimeError("Failed") # loses original traceback

# ✅ Chain it
raise RuntimeError("Failed") from e
```

---

## Resources

- [Python exceptions — official docs](https://docs.python.org/3/tutorial/errors.html)
- [Real Python — exceptions](https://realpython.com/python-exceptions/)
- [Real Python — custom exceptions](https://realpython.com/python-custom-exceptions/)
