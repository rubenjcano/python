from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Write Partitioned") \
    .master("local[*]") \
    .getOrCreate()

data = [
    ("2024-01-01", "Laptop", "Electronics", 1200.0),
    ("2024-01-15", "Phone", "Electronics", 800.0),
    ("2024-02-10", "Desk", "Furniture", 350.0),
    ("2024-02-20", "Chair", "Furniture", 200.0),
    ("2024-03-05", "Monitor", "Electronics", 500.0),
]
columns = ["date", "product", "category", "revenue"]

df = spark.createDataFrame(data, columns)

# -----------------------------------------------------------
# Write partitioned by category
# Creates subfolders: category=Electronics/, category=Furniture/
# Queries filtering on category will skip irrelevant partitions
# -----------------------------------------------------------
df.write \
  .mode("overwrite") \
  .partitionBy("category") \
  .parquet("data/output/sales_by_category")

# Write as CSV (useful for sharing/debugging)
df.write \
  .mode("overwrite") \
  .option("header", "true") \
  .csv("data/output/sales_csv")

# Write modes:
# "overwrite"  → replace existing data
# "append"     → add to existing data
# "ignore"     → do nothing if data exists
# "error"      → raise error if data exists (default)

print("Write complete. Check data/output/")

spark.stop()