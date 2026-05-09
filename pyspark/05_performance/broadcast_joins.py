from pyspark.sql import SparkSession
from pyspark.sql.functions import broadcast, col

spark = SparkSession.builder \
    .appName("Broadcast Joins") \
    .master("local[*]") \
    .getOrCreate()

# Large table (imagine millions of rows)
orders = spark.createDataFrame(
    [(i, i % 5 + 1, float(i * 10)) for i in range(1, 101)],
    ["order_id", "product_id", "amount"]
)

# Small lookup table (categories, configs, mappings...)
products = spark.createDataFrame([
    (1, "Laptop", "Electronics"),
    (2, "Chair", "Furniture"),
    (3, "Phone", "Electronics"),
    (4, "Desk", "Furniture"),
    (5, "Headphones", "Electronics"),
], ["product_id", "product_name", "category"])

# -----------------------------------------------------------
# Regular join — Spark shuffles BOTH tables across the network
# Expensive when one table is large
# -----------------------------------------------------------
print("=== Regular Join ===")
orders.join(products, on="product_id").show(5)

# -----------------------------------------------------------
# Broadcast join — the small table is sent to every worker
# No shuffle of the large table → much faster
# Use when one table fits in memory (typically < 10MB)
# -----------------------------------------------------------
print("=== Broadcast Join ===")
orders.join(broadcast(products), on="product_id").show(5)

# -----------------------------------------------------------
# Auto broadcast
# Spark will broadcast automatically if the table is smaller
# than spark.sql.autoBroadcastJoinThreshold (default: 10MB)
# -----------------------------------------------------------
print("Threshold:", spark.conf.get("spark.sql.autoBroadcastJoinThreshold"))

# Increase threshold (in bytes)
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", 50 * 1024 * 1024)  # 50MB

# Disable auto broadcast
# spark.conf.set("spark.sql.autoBroadcastJoinThreshold", -1)

spark.stop()