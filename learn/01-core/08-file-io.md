# 08 — File I/O

## What it is

File I/O (Input/Output) is how Python reads from and writes to files. As a data engineer, you'll constantly work with CSV files, JSON configs, log files, and more. Python makes this clean and safe with context managers (`with` statement).

---

## Key Concepts

- **`open()`** — open a file, returns a file object
- **Modes** — `"r"` read, `"w"` write, `"a"` append, `"rb"` / `"wb"` binary
- **Context manager** — `with open(...) as f` — automatically closes the file
- **`read()`** — read entire file as a string
- **`readlines()`** — read all lines as a list
- **`write()`** — write a string to a file
- **`csv` module** — reading and writing CSV files properly
- **`json` module** — reading and writing JSON files
- **`pathlib`** — modern, object-oriented file path handling

---

## Code Examples

```python
import csv
import json
from pathlib import Path

# --- Reading a text file ---
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()          # entire file as string
    print(content)

with open("data.txt", "r") as f:
    lines = f.readlines()       # list of lines (includes \n)

with open("data.txt", "r") as f:
    for line in f:              # memory-efficient line-by-line
        print(line.strip())

# --- Writing a text file ---
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")

# --- Appending to a file ---
with open("log.txt", "a") as f:
    f.write("New log entry\n")

# --- CSV reading ---
with open("sales.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)  # each row is a dict: {"date": "2024-01-01", "amount": "500"}

# --- CSV writing ---
data = [
    {"name": "Alice", "sales": 1200},
    {"name": "Bob", "sales": 950},
    {"name": "Charlie", "sales": 1500},
]

with open("results.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "sales"])
    writer.writeheader()
    writer.writerows(data)

# --- JSON reading ---
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)  # dict
    print(config["pipeline_name"])

# --- JSON writing ---
pipeline_config = {
    "name": "sales_etl",
    "source": "Azure Blob",
    "destination": "Snowflake",
    "schedule": "daily"
}

with open("pipeline_config.json", "w", encoding="utf-8") as f:
    json.dump(pipeline_config, f, indent=2)

# --- JSON from/to string ---
json_string = json.dumps(pipeline_config, indent=2)
parsed = json.loads(json_string)

# --- pathlib (modern path handling) ---
from pathlib import Path

# Create path objects
data_dir = Path("data")
file_path = data_dir / "sales.csv"

# Check existence
print(file_path.exists())
print(file_path.is_file())
print(data_dir.is_dir())

# Create directories
data_dir.mkdir(parents=True, exist_ok=True)

# File info
print(file_path.name)      # sales.csv
print(file_path.stem)      # sales
print(file_path.suffix)    # .csv
print(file_path.parent)    # data

# List files in a directory
for f in data_dir.glob("*.csv"):
    print(f)

# Read / write with pathlib
text = file_path.read_text(encoding="utf-8")
file_path.write_text("new content", encoding="utf-8")

# --- Practical: process all CSV files in a folder ---
def process_csv_folder(folder: str) -> list[dict]:
    results = []
    folder_path = Path(folder)

    for csv_file in folder_path.glob("*.csv"):
        with open(csv_file, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["source_file"] = csv_file.name
                results.append(row)

    print(f"Processed {len(results)} rows from {folder}")
    return results
```

---

## Exercises

### Exercise 1 — Write and read a file
Write a list of 5 pipeline names to a file `pipelines.txt` (one per line), then read it back and print each name.

<details>
<summary>Solution</summary>

```python
pipelines = ["sales_etl", "orders_etl", "customers_sync", "products_load", "events_stream"]

with open("pipelines.txt", "w") as f:
    for pipeline in pipelines:
        f.write(pipeline + "\n")

with open("pipelines.txt", "r") as f:
    for line in f:
        print(line.strip())
```
</details>

---

### Exercise 2 — CSV write and read
Create a list of 3 employee dicts with keys `name`, `role`, `department`. Write them to `employees.csv`, then read them back and print each row.

<details>
<summary>Solution</summary>

```python
import csv

employees = [
    {"name": "Alice", "role": "Data Engineer", "department": "Data"},
    {"name": "Bob", "role": "Data Analyst", "department": "BI"},
    {"name": "Charlie", "role": "ML Engineer", "department": "AI"},
]

with open("employees.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "role", "department"])
    writer.writeheader()
    writer.writerows(employees)

with open("employees.csv", "r", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```
</details>

---

### Exercise 3 — JSON config
Write a pipeline config dict to `config.json` with keys: `name`, `source`, `destination`, `schedule`, `retries`. Read it back and print only the `name` and `schedule`.

<details>
<summary>Solution</summary>

```python
import json

config = {
    "name": "sales_etl",
    "source": "azure_blob",
    "destination": "snowflake",
    "schedule": "daily",
    "retries": 3
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)

with open("config.json", "r") as f:
    loaded = json.load(f)
    print(f"Pipeline: {loaded['name']}, Schedule: {loaded['schedule']}")
```
</details>

---

### Exercise 4 — pathlib
Use `pathlib` to: check if a folder `output/` exists, create it if not, list all `.json` files in the current directory, and print the name and size of each.

<details>
<summary>Solution</summary>

```python
from pathlib import Path

output_dir = Path("output")
if not output_dir.exists():
    output_dir.mkdir(parents=True)
    print("Created output/ folder")

for json_file in Path(".").glob("*.json"):
    size = json_file.stat().st_size
    print(f"{json_file.name}: {size} bytes")
```
</details>

---

### Exercise 5 — Log writer
Write a function `log(message, level="INFO", filepath="pipeline.log")` that appends a log entry to a file in the format `"[LEVEL] YYYY-MM-DD HH:MM:SS — message"`. Test it with INFO and ERROR messages.

<details>
<summary>Solution</summary>

```python
from datetime import datetime

def log(message: str, level: str = "INFO", filepath: str = "pipeline.log") -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{level}] {timestamp} — {message}\n"
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(entry)

log("Pipeline started")
log("Connection timeout", level="ERROR")
log("Pipeline completed")
```
</details>

---

## Common Mistakes

```python
# ❌ Not using context manager — file may not close properly
f = open("data.txt", "r")
content = f.read()
# if an error occurs here, f.close() is never called

# ✅ Always use with
with open("data.txt", "r") as f:
    content = f.read()

# ❌ Forgetting newline="" when writing CSV — causes extra blank lines on Windows
with open("data.csv", "w") as f:  # missing newline=""
    writer = csv.writer(f)

# ✅
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

# ❌ Reading a large file entirely into memory
with open("huge_file.csv") as f:
    all_lines = f.readlines()  # loads everything into RAM

# ✅ Iterate line by line
with open("huge_file.csv") as f:
    for line in f:
        process(line)

# ❌ Hardcoding path separators
path = "data\\sales.csv"   # breaks on Mac/Linux

# ✅ Use pathlib
from pathlib import Path
path = Path("data") / "sales.csv"
```

---

## Resources

- [Python file I/O — official docs](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Python csv module](https://docs.python.org/3/library/csv.html)
- [Python json module](https://docs.python.org/3/library/json.html)
- [Real Python — pathlib](https://realpython.com/python-pathlib/)
