from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Partitioning") \
    .master("local[*]") \
    .getOrCreate()

data = [(i, i % 10) for i in range(1, 201)]
df = spark.createDataFrame(data, ["id", "group"])

# Check current number of partitions
print("Default partitions:", df.rdd.getNumPartitions())

# -----------------------------------------------------------
# repartition(n)
# - Reshuffles ALL data across the network (full shuffle)
# - Can increase OR decrease partitions
# - Use when: you need more parallelism or want to partition by column
# -----------------------------------------------------------
df_repartitioned = df.repartition(4)
print("After repartition(4):", df_repartitioned.rdd.getNumPartitions())

# Repartition by column — useful before writing partitioned data
df_by_group = df.repartition(col("group"))
print("After repartition by column:", df_by_group.rdd.getNumPartitions())

# -----------------------------------------------------------
# coalesce(n)
# - Reduces partitions with minimal data movement (no full shuffle)
# - Can ONLY decrease partitions
# - Use when: you want fewer output files when writing
# -----------------------------------------------------------
df_coalesced = df.coalesce(2)
print("After coalesce(2):", df_coalesced.rdd.getNumPartitions())

# -----------------------------------------------------------
# Rule of thumb:
# repartition → increase partitions or repartition by column
# coalesce    → decrease partitions (e.g. before writing to disk)
#
# Ideal partition size: 100MB–200MB per partition
# Too many small partitions → scheduling overhead
# Too few large partitions  → not enough parallelism
# -----------------------------------------------------------

# Write with coalesce to avoid many tiny files
df_coalesced.write \
  .mode("overwrite") \
  .parquet("data/output/partitioned_out")

spark.stop()