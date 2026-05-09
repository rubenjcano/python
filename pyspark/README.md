# pyspark 🐍⚡

A personal learning folder for exploring **Apache Spark with Python (PySpark)** — from core concepts to real-world data processing patterns.

---

## 📋 Table of Contents

- [About](#about)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Folder Structure](#folder-structure)
- [Topics Covered](#topics-covered)
- [Running the Examples](#running-the-examples)
- [Resources](#resources)

---

## About

> 💡 New to Spark? Read [CONCEPTS.md](./CONCEPTS.md) first for a high-level overview of the architecture and libraries.

This folder is a hands-on sandbox for learning PySpark progressively. The goal is to build solid foundations in:

- Spark core concepts (RDDs, DataFrames, Datasets)
- Spark SQL and querying
- Reading and writing data (CSV, Parquet, JSON, Delta)
- Transformations, actions, and lazy evaluation
- Pandas UDFs with Apache Arrow
- Performance tuning basics (partitioning, caching, broadcast joins)

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | 3.9+ |
| PySpark | 3.4+ |
| Java (JDK) | 17 |
| Winutils | hadoop-3.3.5 (Windows only) |

---

## Setup & Installation (Windows)

### Step 1 — Install Python

Download the installer from 👉 https://www.python.org/downloads/

During installation, make sure to check **"Add Python to PATH"** before clicking Install.

Verify:

```powershell
python --version
```

### Step 2 — Install Java (JDK 17)

Download the `.msi` installer from 👉 https://adoptium.net

Choose **Windows x64 .msi** and run the installer.

Verify:

```powershell
java -version
```

Then set `JAVA_HOME`:

1. Search for **"Edit the system environment variables"** in the Start menu
2. Click **Environment Variables**
3. Under **System variables** → **New**:
   - Variable name: `JAVA_HOME`
   - Variable value: `C:\Program Files\Eclipse Adoptium\jdk-17.x.x` (adjust to your install path)
4. Find the `Path` variable → **Edit** → **New** → add `%JAVA_HOME%\bin`
5. Restart your terminal

### Step 3 — Install Winutils

Spark requires Winutils to run on Windows. Download it from 👉 https://github.com/cdarlint/winutils

Download `winutils.exe` from the `hadoop-3.3.5/bin/` folder and save it to `C:\hadoop\bin`.

Then add a new system environment variable:
- Variable name: `HADOOP_HOME`
- Variable value: `C:\hadoop`

### Step 4 — Install PySpark

```powershell
pip install pyspark
```

### Step 5 — Verify everything works

```powershell
python -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.master('local').getOrCreate(); print('OK')"
```

If you see `OK` you are ready to run the scripts.

---

## Folder Structure

```
pyspark/
├── 01_basics/
│   ├── rdd_intro.py              # RDD creation and basic operations
│   ├── dataframe_intro.py        # DataFrame API fundamentals
│   └── lazy_evaluation.py        # Understanding transformations vs actions
├── 02_spark_sql/
│   ├── sql_queries.py            # Running SQL on DataFrames
│   └── temp_views.py             # Creating and querying temp views
├── 03_io/
│   ├── read_csv.py               # Reading CSV files
│   ├── read_parquet.py           # Reading Parquet files
│   └── write_partitioned.py      # Writing partitioned data
├── 04_transformations/
│   ├── joins.py                  # Inner, left, broadcast joins
│   ├── aggregations.py           # groupBy, agg, window functions
│   └── udfs.py                   # Python UDFs and pandas UDFs (Arrow)
├── 05_performance/
│   ├── caching.py                # persist() and cache()
│   ├── partitioning.py           # repartition vs coalesce
│   └── broadcast_joins.py        # When and how to broadcast
├── data/
│   ├── input/                    # Sample data files
│   └── output/                   # Generated output (git-ignored)
└── README.md
```

---

## Topics Covered

### 1. Basics

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MyApp") \
    .master("local[*]") \
    .getOrCreate()

# Create a DataFrame from a list
data = [("Alice", 30), ("Bob", 25), ("Carol", 35)]
df = spark.createDataFrame(data, ["name", "age"])

df.show()
df.printSchema()
```

### 2. Spark SQL

```python
df.createOrReplaceTempView("people")

result = spark.sql("""
    SELECT name, age
    FROM people
    WHERE age > 28
    ORDER BY age DESC
""")

result.show()
```

### 3. Aggregations

```python
from pyspark.sql.functions import sum, avg, count, desc

df.groupBy("category") \
  .agg(
      sum("revenue").alias("total_revenue"),
      avg("revenue").alias("avg_revenue"),
      count("*").alias("num_records")
  ) \
  .orderBy(desc("total_revenue")) \
  .show()
```

### 4. Pandas UDFs (with Arrow)

```python
from pyspark.sql.functions import pandas_udf
import pandas as pd

# Enable Arrow for faster data transfer
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

@pandas_udf("double")
def normalize(col: pd.Series) -> pd.Series:
    return (col - col.mean()) / col.std()

df.withColumn("normalized", normalize(df["value"])).show()
```

### 5. Window Functions

```python
from pyspark.sql.functions import rank
from pyspark.sql.window import Window

window = Window.partitionBy("department").orderBy(desc("salary"))

df.withColumn("rank", rank().over(window)).show()
```

---

## Running the Examples

```bash
# Run any script directly
python 01_basics/dataframe_intro.py

# Or via spark-submit
spark-submit 01_basics/dataframe_intro.py
```

> For local development, `master("local[*]")` in the SparkSession is enough — no cluster needed.

---

## Resources

- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Spark by Examples (Python)](https://sparkbyexamples.com/pyspark-tutorial/)
- [Apache Arrow + PySpark](https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html)
- [Learning Spark 2nd Edition (O'Reilly)](https://www.oreilly.com/library/view/learning-spark-2nd/9781492050032/)
- [Databricks Community Edition](https://community.cloud.databricks.com/) — free cluster to practice

---

## License

MIT — free to use, fork, and learn from.