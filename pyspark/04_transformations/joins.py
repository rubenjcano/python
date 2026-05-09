from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast

spark = SparkSession.builder \
    .appName("Joins") \
    .master("local[*]") \
    .getOrCreate()

orders = spark.createDataFrame([
    (1, 101, 250.0),
    (2, 102, 180.0),
    (3, 101, 90.0),
    (4, 103, 400.0),
    (5, 999, 50.0),   # customer 999 doesn't exist in customers
], ["order_id", "customer_id", "amount"])

customers = spark.createDataFrame([
    (101, "Alice", "Barcelona"),
    (102, "Bob", "Madrid"),
    (103, "Carol", "Valencia"),
    (104, "David", "Seville"),  # customer with no orders
], ["customer_id", "name", "city"])

# Inner join — only matching rows
print("=== Inner Join ===")
orders.join(customers, on="customer_id", how="inner").show()

# Left join — all orders, nulls for unmatched customers
print("=== Left Join ===")
orders.join(customers, on="customer_id", how="left").show()

# Right join — all customers, nulls for those with no orders
print("=== Right Join ===")
orders.join(customers, on="customer_id", how="right").show()

# Full outer join
print("=== Full Outer Join ===")
orders.join(customers, on="customer_id", how="outer").show()

# Broadcast join — use when one table is small
# Sends the small table to every worker, avoids shuffle
print("=== Broadcast Join ===")
orders.join(broadcast(customers), on="customer_id", how="inner").show()

spark.stop()