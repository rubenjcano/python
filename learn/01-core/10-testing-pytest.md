# 10 — Testing with pytest

## What it is

Testing is writing code that verifies your code works correctly. **pytest** is the standard Python testing framework — simple to write, powerful to run. In data engineering, tests catch bugs before they corrupt production data, and give you confidence when refactoring pipelines.

---

## Key Concepts

- **Unit test** — tests a single function in isolation
- **`assert`** — verifies a condition is True, fails the test if not
- **Test function naming** — must start with `test_`
- **Test file naming** — must start with `test_` or end with `_test.py`
- **`pytest.raises`** — test that an exception is raised
- **Fixtures** — reusable setup code shared across tests
- **Parametrize** — run the same test with multiple inputs
- **Mocking** — replace real dependencies with fake ones (`unittest.mock`)
- **Coverage** — measure what % of code is tested

---

## Code Examples

```python
# --- The code being tested: utils.py ---
def clean_string(s: str) -> str:
    return s.strip().lower()

def calculate_average(numbers: list[float]) -> float:
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)

def parse_record(row: dict) -> dict:
    return {
        "id": int(row["id"]),
        "name": row["name"].strip(),
        "amount": float(row["amount"]),
    }

# --- Basic test file: test_utils.py ---
import pytest
from utils import clean_string, calculate_average, parse_record

def test_clean_string_strips_whitespace():
    assert clean_string("  hello  ") == "hello"

def test_clean_string_lowercases():
    assert clean_string("HELLO") == "hello"

def test_clean_string_handles_empty():
    assert clean_string("") == ""

def test_calculate_average_basic():
    assert calculate_average([1, 2, 3, 4, 5]) == 3.0

def test_calculate_average_single_value():
    assert calculate_average([42]) == 42.0

def test_calculate_average_raises_on_empty():
    with pytest.raises(ValueError, match="Cannot calculate average"):
        calculate_average([])

def test_parse_record():
    row = {"id": "1", "name": "  Alice  ", "amount": "1200.50"}
    result = parse_record(row)
    assert result == {"id": 1, "name": "Alice", "amount": 1200.50}

# --- Parametrize: same test, multiple inputs ---
@pytest.mark.parametrize("input_str, expected", [
    ("  hello  ", "hello"),
    ("WORLD", "world"),
    ("  Mixed Case  ", "mixed case"),
    ("", ""),
])
def test_clean_string_parametrized(input_str, expected):
    assert clean_string(input_str) == expected

@pytest.mark.parametrize("numbers, expected", [
    ([1, 2, 3], 2.0),
    ([10, 20], 15.0),
    ([5], 5.0),
    ([0, 0, 0], 0.0),
])
def test_calculate_average_parametrized(numbers, expected):
    assert calculate_average(numbers) == expected

# --- Fixtures: reusable test setup ---
@pytest.fixture
def sample_records():
    return [
        {"id": "1", "name": "Alice", "amount": "1200"},
        {"id": "2", "name": "Bob", "amount": "950"},
        {"id": "3", "name": "Charlie", "amount": "1500"},
    ]

def test_parse_multiple_records(sample_records):
    results = [parse_record(row) for row in sample_records]
    assert len(results) == 3
    assert results[0]["id"] == 1
    assert results[1]["name"] == "Bob"
    assert results[2]["amount"] == 1500.0

# --- Mocking: replace external dependencies ---
from unittest.mock import patch, MagicMock

# The function we want to test
def fetch_data_from_api(url: str) -> dict:
    import requests
    response = requests.get(url)
    return response.json()

# Test without actually calling the API
def test_fetch_data_from_api():
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "ok", "count": 42}

    with patch("requests.get", return_value=mock_response):
        result = fetch_data_from_api("https://api.example.com/data")

    assert result["status"] == "ok"
    assert result["count"] == 42

# --- Testing file I/O with tmp_path fixture ---
def write_pipeline_names(filepath: str, names: list[str]) -> None:
    with open(filepath, "w") as f:
        for name in names:
            f.write(name + "\n")

def test_write_pipeline_names(tmp_path):
    output_file = tmp_path / "pipelines.txt"
    names = ["sales_etl", "orders_etl", "customers_sync"]
    write_pipeline_names(str(output_file), names)

    content = output_file.read_text()
    assert "sales_etl\n" in content
    assert "orders_etl\n" in content
    assert len(content.strip().split("\n")) == 3
```

---

## Running Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest

# Run a specific file
pytest test_utils.py

# Run a specific test function
pytest test_utils.py::test_calculate_average_basic

# Run with verbose output
pytest -v

# Run and show print statements
pytest -s

# Run with coverage report
pytest --cov=utils --cov-report=term-missing

# Run only tests matching a keyword
pytest -k "average"
```

---

## Exercises

### Exercise 1 — Write basic tests
Given this function:
```python
def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]
```
Write at least 4 tests — valid emails, invalid emails, edge cases.

<details>
<summary>Solution</summary>

```python
import pytest
from utils import is_valid_email

def test_valid_email():
    assert is_valid_email("ruben@gmail.com") is True

def test_valid_email_with_subdomain():
    assert is_valid_email("ruben@mail.company.com") is True

def test_invalid_email_no_at():
    assert is_valid_email("rubengmail.com") is False

def test_invalid_email_no_dot():
    assert is_valid_email("ruben@gmailcom") is False

def test_empty_string():
    assert is_valid_email("") is False
```
</details>

---

### Exercise 2 — Test exceptions
Given:
```python
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
```
Write a test that verifies the exception is raised with the correct message.

<details>
<summary>Solution</summary>

```python
def test_divide_by_zero_raises():
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)

def test_divide_normal():
    assert divide(10, 2) == 5.0
```
</details>

---

### Exercise 3 — Parametrize
Write a parametrized test for a `to_snake_case(s)` function with at least 5 input/output pairs.

<details>
<summary>Solution</summary>

```python
@pytest.mark.parametrize("input_str, expected", [
    ("Sales ETL", "sales_etl"),
    ("Orders Pipeline", "orders_pipeline"),
    ("already_snake", "already_snake"),
    ("  Extra Spaces  ", "extra_spaces"),
    ("ONE", "one"),
])
def test_to_snake_case(input_str, expected):
    assert to_snake_case(input_str) == expected
```
</details>

---

### Exercise 4 — Fixture
Create a fixture `pipeline_config` that returns a sample pipeline config dict. Write 3 tests that use it to verify different fields.

<details>
<summary>Solution</summary>

```python
@pytest.fixture
def pipeline_config():
    return {
        "name": "sales_etl",
        "source": "azure_blob",
        "destination": "snowflake",
        "schedule": "daily",
        "retries": 3,
        "is_active": True
    }

def test_pipeline_has_name(pipeline_config):
    assert pipeline_config["name"] == "sales_etl"

def test_pipeline_is_active(pipeline_config):
    assert pipeline_config["is_active"] is True

def test_pipeline_retries_positive(pipeline_config):
    assert pipeline_config["retries"] > 0
```
</details>

---

## Common Mistakes

```python
# ❌ Test that doesn't actually test anything
def test_something():
    result = calculate_average([1, 2, 3])
    print(result)  # no assert — always passes

# ✅ Always assert
def test_something():
    result = calculate_average([1, 2, 3])
    assert result == 2.0

# ❌ One giant test that tests everything
def test_pipeline():
    # 50 lines testing extract, transform, load, logging...

# ✅ Small, focused tests — one concept per test
def test_extract_returns_list(): ...
def test_transform_cleans_nulls(): ...
def test_load_writes_correct_rows(): ...

# ❌ Tests that depend on each other or on external state
def test_b():
    # assumes test_a ran first and set some global variable

# ✅ Each test is independent and self-contained

# ❌ Not testing edge cases
def test_calculate_average():
    assert calculate_average([1, 2, 3]) == 2.0
    # missing: empty list, single element, negative numbers, floats
```

---

## Resources

- [pytest — official docs](https://docs.pytest.org/)
- [Real Python — pytest](https://realpython.com/pytest-python-testing/)
- [Real Python — mocking](https://realpython.com/python-mock-library/)
