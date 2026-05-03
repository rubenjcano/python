# 07 — Type Hints

## What it is

Type hints let you annotate variables, function parameters, and return values with their expected types. Python doesn't enforce them at runtime — they're for documentation, tooling (IDEs, linters), and static analysis tools like **mypy**. In data engineering, type hints make pipelines much easier to understand and debug.

---

## Key Concepts

- **Basic annotations** — `int`, `str`, `float`, `bool`, `None`
- **`Optional`** — value can be a type or `None`
- **`Union`** — value can be one of several types
- **`list`, `dict`, `tuple`, `set`** — with type parameters
- **`Any`** — disables type checking for that value
- **`Callable`** — a function type
- **`TypeVar`** — generic types
- **`dataclass`** — type-hinted data containers
- **mypy** — static type checker for Python

---

## Code Examples

```python
from typing import Optional, Union, Any, Callable
from collections.abc import Iterator

# --- Basic annotations ---
name: str = "Ruben"
age: int = 28
salary: float = 45000.0
is_active: bool = True

# --- Function annotations ---
def greet(name: str) -> str:
    return f"Hello, {name}!"

def calculate_average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

def get_user(user_id: int) -> dict[str, Any]:
    return {"id": user_id, "name": "Ruben"}

# --- Optional (value or None) ---
def find_user(user_id: int) -> Optional[dict]:
    if user_id == 1:
        return {"id": 1, "name": "Ruben"}
    return None

# Python 3.10+ shorthand
def find_user(user_id: int) -> dict | None:
    ...

# --- Union (multiple types allowed) ---
def process_id(user_id: Union[int, str]) -> str:
    return str(user_id)

# Python 3.10+ shorthand
def process_id(user_id: int | str) -> str:
    return str(user_id)

# --- List, Dict, Tuple, Set with types ---
def get_names(ids: list[int]) -> list[str]:
    return [str(i) for i in ids]

def build_config(keys: list[str], values: list[Any]) -> dict[str, Any]:
    return dict(zip(keys, values))

def get_coordinates() -> tuple[float, float]:
    return 41.3874, 2.1686

def get_unique_tags(items: list[str]) -> set[str]:
    return set(items)

# --- Callable ---
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

def double(x: int) -> int:
    return x * 2

print(apply(double, 5))  # 10

# --- Iterator / Generator ---
def even_numbers(limit: int) -> Iterator[int]:
    for n in range(0, limit + 1, 2):
        yield n

# --- dataclass (structured, typed data containers) ---
from dataclasses import dataclass, field

@dataclass
class Pipeline:
    name: str
    source: str
    destination: str
    schedule: str = "daily"
    is_active: bool = True
    tags: list[str] = field(default_factory=list)

    def run(self) -> None:
        print(f"Running {self.name}")

p = Pipeline(
    name="sales_etl",
    source="Azure Blob",
    destination="Snowflake",
    tags=["finance", "daily"]
)
print(p)
print(p.name)

# Dataclasses auto-generate __init__, __repr__, __eq__

# --- TypedDict (typed dictionaries) ---
from typing import TypedDict

class PipelineConfig(TypedDict):
    name: str
    source: str
    destination: str
    schedule: str

config: PipelineConfig = {
    "name": "sales_etl",
    "source": "blob",
    "destination": "snowflake",
    "schedule": "daily"
}

# --- Practical: typed pipeline function ---
from typing import Callable

def run_pipeline(
    name: str,
    extract: Callable[[], list[dict]],
    transform: Callable[[list[dict]], list[dict]],
    load: Callable[[list[dict]], None]
) -> bool:
    try:
        data = extract()
        transformed = transform(data)
        load(transformed)
        return True
    except Exception as e:
        print(f"Pipeline {name} failed: {e}")
        return False
```

---

## Exercises

### Exercise 1 — Annotate functions
Add type hints to these functions:

```python
def add(a, b):
    return a + b

def get_initials(full_name):
    return "".join(word[0].upper() for word in full_name.split())

def find_max(numbers):
    return max(numbers) if numbers else None
```

<details>
<summary>Solution</summary>

```python
def add(a: int | float, b: int | float) -> int | float:
    return a + b

def get_initials(full_name: str) -> str:
    return "".join(word[0].upper() for word in full_name.split())

def find_max(numbers: list[int | float]) -> int | float | None:
    return max(numbers) if numbers else None
```
</details>

---

### Exercise 2 — dataclass
Create a `DataSource` dataclass with fields: `name: str`, `type: str`, `host: str`, `port: int`, `database: str`, `is_secure: bool = True`. Add a method `connection_string() -> str` that returns `"{type}://{host}:{port}/{database}"`.

<details>
<summary>Solution</summary>

```python
from dataclasses import dataclass

@dataclass
class DataSource:
    name: str
    type: str
    host: str
    port: int
    database: str
    is_secure: bool = True

    def connection_string(self) -> str:
        return f"{self.type}://{self.host}:{self.port}/{self.database}"

ds = DataSource("prod_db", "postgresql", "localhost", 5432, "sales")
print(ds.connection_string())
```
</details>

---

### Exercise 3 — Optional return
Write a function `parse_int(value: str) -> int | None` that tries to convert a string to int, returning `None` if it fails.

<details>
<summary>Solution</summary>

```python
def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None

print(parse_int("42"))    # 42
print(parse_int("hello")) # None
```
</details>

---

### Exercise 4 — TypedDict
Create a `LogEntry` TypedDict with fields: `timestamp: str`, `level: str`, `message: str`, `pipeline: str`. Write a function `format_log(entry: LogEntry) -> str` that returns `"[{level}] {timestamp} — {pipeline}: {message}"`.

<details>
<summary>Solution</summary>

```python
from typing import TypedDict

class LogEntry(TypedDict):
    timestamp: str
    level: str
    message: str
    pipeline: str

def format_log(entry: LogEntry) -> str:
    return f"[{entry['level']}] {entry['timestamp']} — {entry['pipeline']}: {entry['message']}"

log: LogEntry = {
    "timestamp": "2025-01-01 10:00:00",
    "level": "ERROR",
    "message": "Connection timeout",
    "pipeline": "sales_etl"
}

print(format_log(log))
```
</details>

---

## Common Mistakes

```python
# ❌ Using type hints as runtime validation (they don't enforce)
def add(a: int, b: int) -> int:
    return a + b

add("hello", "world")  # runs fine — no error at runtime

# ✅ Use isinstance() if you need runtime checks
def add(a: int, b: int) -> int:
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers")
    return a + b

# ❌ Old-style typing for built-in types (Python 3.9+)
from typing import List, Dict, Tuple  # no longer needed

def get_names(ids: List[int]) -> List[str]: ...  # outdated

# ✅ Use built-in types directly
def get_names(ids: list[int]) -> list[str]: ...

# ❌ Using Any everywhere — defeats the purpose
def process(data: Any) -> Any: ...
```

---

## Resources

- [Python typing — official docs](https://docs.python.org/3/library/typing.html)
- [Real Python — type hints](https://realpython.com/python-type-checking/)
- [mypy — static type checker](https://mypy.readthedocs.io/)
- [Python dataclasses — official docs](https://docs.python.org/3/library/dataclasses.html)
