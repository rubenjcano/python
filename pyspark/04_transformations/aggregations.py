from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, avg, count, max, min, desc, rank, lag, round
from pyspark.sql.window import Window

spark = SparkSession.builder \
    .appName("Aggregations") \
    .master("local[*]") \
    .getOrCreate()

data = [
    ("Alice", "Engineering", 70000),
    ("Bob", "Marketing", 50000),
    ("Carol", "Engineering", 90000),
    ("David", "HR", 55000),
    ("Eve", "Marketing", 62000),
    ("Frank", "Engineering", 95000),
    ("Grace", "HR", 48000),
]
df = spark.createDataFrame(data, ["name", "department", "salary"])

# -----------------------------------------------------------
# Basic aggregations with groupBy
# -----------------------------------------------------------
print("=== Department Summary ===")
df.groupBy("department") \
  .agg(
      count("*").alias("headcount"),
      round(avg("salary"), 2).alias("avg_salary"),
      max("salary").alias("max_salary"),
      min("salary").alias("min_salary"),
      sum("salary").alias("total_salary")
  ) \
  .orderBy(desc("avg_salary")) \
  .show()

# -----------------------------------------------------------
# Window functions — calculations across related rows
# -----------------------------------------------------------

# Rank employees by salary within each department
window_dept = Window.partitionBy("department").orderBy(desc("salary"))

print("=== Salary Rank per Department ===")
df.withColumn("rank", rank().over(window_dept)).show()

# Compare each employee's salary to the previous one (ordered globally)
window_global = Window.orderBy("salary")

print("=== Salary vs Previous Employee ===")
df.withColumn("prev_salary", lag("salary", 1).over(window_global)) \
  .withColumn("diff", df["salary"] - lag("salary", 1).over(window_global)) \
  .show()

spark.stop()