from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, pandas_udf, col
from pyspark.sql.types import StringType, DoubleType
import pandas as pd

spark = SparkSession.builder \
    .appName("UDFs") \
    .master("local[*]") \
    .getOrCreate()

# Enable Arrow for faster pandas UDF execution
spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")

data = [
    ("alice smith", 70000.0),
    ("bob jones", 50000.0),
    ("carol white", 90000.0),
]
df = spark.createDataFrame(data, ["name", "salary"])

# -----------------------------------------------------------
# Regular Python UDF
# Processed row by row — simple but slower
# Use when logic is complex and pandas vectorization isn't easy
# -----------------------------------------------------------
def title_case(name: str) -> str:
    return name.title() if name else name

title_udf = udf(title_case, StringType())

print("=== Regular UDF ===")
df.withColumn("name_formatted", title_udf(col("name"))).show()

# -----------------------------------------------------------
# Pandas UDF (vectorized)
# Processes entire columns as pandas Series — much faster
# Powered by Apache Arrow under the hood
# -----------------------------------------------------------
@pandas_udf(DoubleType())
def normalize_salary(salary: pd.Series) -> pd.Series:
    return (salary - salary.mean()) / salary.std()

@pandas_udf(StringType())
def add_currency(salary: pd.Series) -> pd.Series:
    return salary.apply(lambda x: f"€{x:,.0f}")

print("=== Pandas UDF ===")
df.withColumn("salary_normalized", normalize_salary(col("salary"))) \
  .withColumn("salary_display", add_currency(col("salary"))) \
  .show()

# -----------------------------------------------------------
# When to use which:
# Regular UDF  → complex logic, string parsing, external libs
# Pandas UDF   → math, stats, anything pandas does well
# Built-in SQL functions (col, when, etc.) → always prefer these first
# -----------------------------------------------------------

spark.stop()