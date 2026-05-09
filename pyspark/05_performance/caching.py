from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark import StorageLevel

spark = SparkSession.builder \
    .appName("Caching") \
    .master("local[*]") \
    .getOrCreate()

data = [(i, i * 2, i % 5) for i in range(1, 101)]
df = spark.createDataFrame(data, ["id", "value", "group"])

# -----------------------------------------------------------
# Without caching — Spark recomputes the transformation
# every time an action is called
# -----------------------------------------------------------
filtered = df.filter(col("value") > 50)

filtered.count()   # computes
filtered.show()    # computes again from scratch

# -----------------------------------------------------------
# cache() — stores in memory (default)
# Best for DataFrames you reuse multiple times in the same job
# -----------------------------------------------------------
filtered_cached = df.filter(col("value") > 50).cache()

filtered_cached.count()   # computes and caches
filtered_cached.show()    # reads from cache — fast

# -----------------------------------------------------------
# persist() — lets you control the storage level
# -----------------------------------------------------------
df.persist(StorageLevel.MEMORY_AND_DISK)
# MEMORY_ONLY          → RAM only, recomputes if evicted
# MEMORY_AND_DISK      → RAM first, spills to disk
# DISK_ONLY            → disk only (slower, saves RAM)
# MEMORY_ONLY_SER      → serialized in RAM (less memory, more CPU)

# Always unpersist when done to free memory
filtered_cached.unpersist()
df.unpersist()

# -----------------------------------------------------------
# When to cache:
# ✅ DataFrame used in multiple actions in the same job
# ✅ Iterative algorithms (ML training loops)
# ❌ DataFrame used only once
# ❌ Very large DataFrames that don't fit in memory
# -----------------------------------------------------------

spark.stop()