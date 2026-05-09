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
| Java (JDK) | 11 or 17 |

> **Tip:** Spark requires Java under the hood even when using Python. Make sure `JAVA_HOME` is set correctly.

### Install PySpark

```bash
pip install pyspark
```

Or if using a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install pyspark
```

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
