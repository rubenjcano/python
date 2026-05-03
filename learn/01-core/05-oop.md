# 05 — Object-Oriented Programming (OOP)

## What it is

OOP is a programming paradigm where you model real-world concepts as **objects** — bundles of data (attributes) and behaviour (methods). In Python, everything is an object. OOP helps you write code that is reusable, organized, and easier to maintain as projects grow.

---

## Key Concepts

- **Class** — a blueprint for creating objects
- **Object / Instance** — a specific realization of a class
- **`__init__`** — constructor method, runs when an object is created
- **`self`** — reference to the current instance
- **Attributes** — data stored on an object
- **Methods** — functions defined inside a class
- **Inheritance** — a class can extend another class
- **`super()`** — call a parent class method
- **Encapsulation** — hiding internal details (using `_` or `__`)
- **Dunder methods** — special methods like `__str__`, `__repr__`, `__len__`
- **Class vs instance attributes** — class attributes are shared, instance attributes are per object
- **`@classmethod`** and `@staticmethod` — alternative constructors and utility methods
- **`@property`** — controlled access to attributes

---

## Code Examples

```python
# --- Basic class ---
class DataPipeline:
    # Class attribute (shared by all instances)
    version = "1.0"

    def __init__(self, name, source, destination):
        # Instance attributes
        self.name = name
        self.source = source
        self.destination = destination
        self.is_active = False
        self._run_count = 0  # convention: "private" (don't touch directly)

    def run(self):
        self.is_active = True
        self._run_count += 1
        print(f"Running pipeline: {self.name}")

    def stop(self):
        self.is_active = False
        print(f"Stopped pipeline: {self.name}")

    def status(self):
        state = "active" if self.is_active else "stopped"
        return f"{self.name} ({state}) — runs: {self._run_count}"

    # --- Dunder methods ---
    def __str__(self):
        return f"Pipeline({self.name}: {self.source} → {self.destination})"

    def __repr__(self):
        return f"DataPipeline(name={self.name!r}, source={self.source!r}, destination={self.destination!r})"

    def __eq__(self, other):
        return self.name == other.name

# Create instances
p1 = DataPipeline("sales_etl", "Azure Blob", "Snowflake")
p2 = DataPipeline("orders_etl", "SQL Server", "Databricks")

p1.run()
p1.run()
print(p1.status())   # sales_etl (active) — runs: 2
print(p1)            # Pipeline(sales_etl: Azure Blob → Snowflake)
print(repr(p1))
print(DataPipeline.version)  # class attribute

# --- @classmethod (alternative constructor) ---
class DataPipeline:
    def __init__(self, name, source, destination):
        self.name = name
        self.source = source
        self.destination = destination

    @classmethod
    def from_dict(cls, config: dict):
        return cls(config["name"], config["source"], config["destination"])

    @staticmethod
    def validate_name(name: str) -> bool:
        return name.replace("_", "").isalnum()

config = {"name": "sales_etl", "source": "blob", "destination": "snowflake"}
p = DataPipeline.from_dict(config)
print(DataPipeline.validate_name("sales_etl"))  # True

# --- @property ---
class DataPipeline:
    def __init__(self, name, source, destination):
        self.name = name
        self.source = source
        self.destination = destination
        self._schedule = "daily"

    @property
    def schedule(self):
        return self._schedule

    @schedule.setter
    def schedule(self, value):
        allowed = ["hourly", "daily", "weekly"]
        if value not in allowed:
            raise ValueError(f"Schedule must be one of {allowed}")
        self._schedule = value

p = DataPipeline("sales_etl", "blob", "snowflake")
p.schedule = "hourly"    # goes through setter
print(p.schedule)        # hourly

# --- Inheritance ---
class BatchPipeline(DataPipeline):
    def __init__(self, name, source, destination, batch_size):
        super().__init__(name, source, destination)
        self.batch_size = batch_size

    def run(self):
        print(f"Running batch pipeline with size {self.batch_size}")
        super().run()  # call parent run

class StreamingPipeline(DataPipeline):
    def __init__(self, name, source, destination, window_seconds):
        super().__init__(name, source, destination)
        self.window_seconds = window_seconds

    def run(self):
        print(f"Running streaming pipeline with {self.window_seconds}s window")
        super().run()

batch = BatchPipeline("sales_batch", "blob", "snowflake", batch_size=1000)
stream = StreamingPipeline("events_stream", "event_hub", "adls", window_seconds=60)

batch.run()
stream.run()

# isinstance checks
print(isinstance(batch, DataPipeline))    # True
print(isinstance(batch, BatchPipeline))   # True
print(isinstance(batch, StreamingPipeline))  # False
```

---

## Exercises

### Exercise 1 — Basic class
Create a `DatabaseConnection` class with attributes: `host`, `port`, `database`, `is_connected`. Add methods:
- `connect()` — sets `is_connected = True` and prints a message
- `disconnect()` — sets `is_connected = False`
- `__str__` — returns `"Connected to {database} on {host}:{port}"`

<details>
<summary>Solution</summary>

```python
class DatabaseConnection:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.is_connected = False

    def connect(self):
        self.is_connected = True
        print(f"Connected to {self.database} on {self.host}:{self.port}")

    def disconnect(self):
        self.is_connected = False
        print(f"Disconnected from {self.database}")

    def __str__(self):
        return f"Connected to {self.database} on {self.host}:{self.port}"

db = DatabaseConnection("localhost", 5432, "sales_db")
db.connect()
print(db)
db.disconnect()
```
</details>

---

### Exercise 2 — Class method
Add a `@classmethod` called `from_connection_string` to `DatabaseConnection` that parses a connection string like `"localhost:5432/sales_db"` and returns an instance.

<details>
<summary>Solution</summary>

```python
@classmethod
def from_connection_string(cls, conn_str):
    host_port, database = conn_str.split("/")
    host, port = host_port.split(":")
    return cls(host, int(port), database)

db = DatabaseConnection.from_connection_string("localhost:5432/sales_db")
print(db.host, db.port, db.database)
```
</details>

---

### Exercise 3 — Property with validation
Add a `@property` called `port` that validates the value is between 1 and 65535. Raise a `ValueError` if not.

<details>
<summary>Solution</summary>

```python
@property
def port(self):
    return self._port

@port.setter
def port(self, value):
    if not 1 <= value <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    self._port = value
```
</details>

---

### Exercise 4 — Inheritance
Create a `CloudDatabaseConnection` that extends `DatabaseConnection` and adds a `cloud_provider` attribute. Override `connect()` to print `"Connecting to {cloud_provider} cloud database..."` before calling the parent method.

<details>
<summary>Solution</summary>

```python
class CloudDatabaseConnection(DatabaseConnection):
    def __init__(self, host, port, database, cloud_provider):
        super().__init__(host, port, database)
        self.cloud_provider = cloud_provider

    def connect(self):
        print(f"Connecting to {self.cloud_provider} cloud database...")
        super().connect()

cloud_db = CloudDatabaseConnection("sql.azure.com", 1433, "analytics", "Azure")
cloud_db.connect()
```
</details>

---

### Exercise 5 — Dunder methods
Create a `Pipeline` class with a `__len__` method that returns the number of steps, a `__contains__` method to check if a step name is in the pipeline, and a `__iter__` to iterate over steps.

<details>
<summary>Solution</summary>

```python
class Pipeline:
    def __init__(self, name, steps):
        self.name = name
        self.steps = steps

    def __len__(self):
        return len(self.steps)

    def __contains__(self, step):
        return step in self.steps

    def __iter__(self):
        return iter(self.steps)

    def __str__(self):
        return f"Pipeline({self.name}): {' → '.join(self.steps)}"

p = Pipeline("sales_etl", ["extract", "validate", "transform", "load"])
print(len(p))              # 4
print("transform" in p)    # True
print("clean" in p)        # False
for step in p:
    print(step)
print(p)
```
</details>

---

## Common Mistakes

```python
# ❌ Forgetting self in method definition
class MyClass:
    def my_method():   # missing self
        pass

# ❌ Modifying class attributes through an instance
class Pipeline:
    count = 0

p = Pipeline()
p.count = 5   # creates an instance attribute, doesn't modify class attribute
print(Pipeline.count)  # still 0!

# ✅ Modify class attributes through the class
Pipeline.count = 5

# ❌ Not calling super().__init__() in child class
class Child(Parent):
    def __init__(self, x, y):
        self.y = y  # parent attributes not initialized!

# ✅
class Child(Parent):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y
```

---

## Resources

- [Python OOP — official docs](https://docs.python.org/3/tutorial/classes.html)
- [Real Python — OOP](https://realpython.com/python3-object-oriented-programming/)
- [Real Python — dunder methods](https://realpython.com/python-magic-methods/)
