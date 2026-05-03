# 02 — Control Flow

## What it is

Control flow is how you direct the order in which Python executes code. Instead of running every line top to bottom, you can make decisions (`if/elif/else`), repeat actions (`for`, `while`), and jump out of loops (`break`, `continue`).

---

## Key Concepts

- **if / elif / else** — conditional branching
- **for loop** — iterate over a sequence
- **while loop** — repeat while a condition is True
- **break** — exit a loop early
- **continue** — skip to the next iteration
- **pass** — placeholder, does nothing
- **match / case** — structural pattern matching (Python 3.10+)

---

## Code Examples

```python
# --- if / elif / else ---
score = 85

if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "F"

print(grade)  # B

# --- Ternary (one-line if) ---
status = "active" if score >= 60 else "inactive"

# --- for loop ---
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# --- range ---
for i in range(5):         # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 10, 2):  # 2, 4, 6, 8
    print(i)

# --- enumerate (index + value) ---
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# --- zip (iterate two lists together) ---
names = ["Alice", "Bob", "Charlie"]
scores = [90, 75, 88]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# --- while loop ---
count = 0
while count < 5:
    print(count)
    count += 1

# --- break and continue ---
for i in range(10):
    if i == 3:
        continue   # skip 3
    if i == 7:
        break      # stop at 7
    print(i)       # prints 0, 1, 2, 4, 5, 6

# --- loop over dict ---
person = {"name": "Ruben", "city": "Barcelona", "role": "Data Engineer"}
for key, value in person.items():
    print(f"{key}: {value}")

# --- match / case (Python 3.10+) ---
status_code = 404

match status_code:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case 500:
        print("Server Error")
    case _:
        print("Unknown")
```

---

## Exercises

### Exercise 1 — Grading system
Write a function that takes a score (0–100) and returns the grade:
- 90–100 → "A"
- 75–89 → "B"
- 60–74 → "C"
- Below 60 → "F"

Test it with scores: 95, 80, 65, 45.

<details>
<summary>Solution</summary>

```python
def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "F"

for score in [95, 80, 65, 45]:
    print(f"{score} → {get_grade(score)}")
```
</details>

---

### Exercise 2 — FizzBuzz
Print numbers from 1 to 30. For multiples of 3 print "Fizz", for multiples of 5 print "Buzz", for multiples of both print "FizzBuzz", otherwise print the number.

<details>
<summary>Solution</summary>

```python
for i in range(1, 31):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```
</details>

---

### Exercise 3 — Loop with break
You have a list of pipeline statuses: `["success", "success", "failed", "success", "success"]`. Loop through them and stop as soon as you find a `"failed"` status. Print how many ran before it failed.

<details>
<summary>Solution</summary>

```python
statuses = ["success", "success", "failed", "success", "success"]

count = 0
for status in statuses:
    if status == "failed":
        print(f"Pipeline failed after {count} successful runs")
        break
    count += 1
```
</details>

---

### Exercise 4 — Nested loops
You have a list of tables and a list of operations. Print every combination of table + operation.

```python
tables = ["sales", "customers", "products"]
operations = ["INSERT", "UPDATE", "DELETE"]
```

<details>
<summary>Solution</summary>

```python
tables = ["sales", "customers", "products"]
operations = ["INSERT", "UPDATE", "DELETE"]

for table in tables:
    for operation in operations:
        print(f"{operation} on {table}")
```
</details>

---

### Exercise 5 — While with user input simulation
Simulate a retry loop: a pipeline fails on the first 2 attempts and succeeds on the 3rd. Use a while loop with a counter and print the attempt number each time.

<details>
<summary>Solution</summary>

```python
attempt = 0
max_attempts = 5
success_on = 3

while attempt < max_attempts:
    attempt += 1
    print(f"Attempt {attempt}...")
    if attempt == success_on:
        print("Pipeline succeeded!")
        break
else:
    print("All attempts failed.")
```
</details>

---

## Common Mistakes

```python
# ❌ Using = instead of == in conditions
if x = 5:   # SyntaxError
    pass

# ❌ Infinite while loop (forgetting to update the condition)
count = 0
while count < 5:
    print(count)
    # forgot count += 1 → runs forever

# ❌ Comparing with wrong types
if "5" == 5:    # False — string vs int
    pass

# ✅ Convert first
if int("5") == 5:
    pass

# ❌ range is not a list
r = range(5)
print(r[0])    # works, but r is not a list
print(list(r)) # [0, 1, 2, 3, 4]
```

---

## Resources

- [Python control flow — official docs](https://docs.python.org/3/tutorial/controlflow.html)
- [Real Python — for loops](https://realpython.com/python-for-loop/)
- [Real Python — while loops](https://realpython.com/python-while-loop/)
