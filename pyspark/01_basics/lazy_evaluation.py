from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Lazy Evaluation") \
    .master("local[*]") \
    .getOrCreate()

# -----------------------------------------------------------
# KEY CONCEPT: Spark is lazy.
# Transformations do NOT run immediately — they build a plan.
# Actions trigger the actual execution.
# -----------------------------------------------------------

data = [(i,) for i in range(1, 11)]
df = spark.createDataFrame(data, ["number"])

# These are TRANSFORMATIONS — nothing runs yet
filtered = df.filter(col("number") > 5)
doubled = filtered.withColumn("doubled", col("number") * 2)

# You can inspect the execution plan without running it
print("=== Execution Plan ===")
doubled.explain()

# This is an ACTION — this triggers the computation
print("\n=== Result ===")
doubled.show()

# Other common actions:
# .count()      → returns the number of rows
# .collect()    → returns all rows as a Python list
# .first()      → returns the first row
# .take(n)      → returns the first n rows
# .write        → saves data to disk

print("Count:", doubled.count())
print("First row:", doubled.first())

spark.stop()