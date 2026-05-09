from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder \
    .appName("Read Parquet") \
    .master("local[*]") \
    .getOrCreate()

# -----------------------------------------------------------
# Why Parquet?
# - Columnar format → only reads the columns you need
# - Compressed → smaller files on disk
# - Schema embedded → no need to define or infer
# - The standard format in most data lakes
# -----------------------------------------------------------

# Read a single Parquet file
df = spark.read.parquet("data/input/sales.parquet")

df.show()
df.printSchema()

# Read a partitioned Parquet dataset (folder with partition subfolders)
# e.g. data/input/sales_partitioned/year=2024/month=01/part-0000.parquet
df_partitioned = spark.read.parquet("data/input/sales_partitioned/")

# Partition columns are automatically added to the schema
df_partitioned.show()

# Predicate pushdown — Spark will skip partitions that don't match
df_partitioned.filter(col("year") == 2024).show()

# Write back to Parquet (for reference)
df.write \
  .mode("overwrite") \
  .parquet("data/output/sales_out.parquet")

spark.stop()