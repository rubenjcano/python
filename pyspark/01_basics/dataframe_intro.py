from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper, lit

spark = SparkSession.builder \
    .appName("DataFrame Intro") \
    .master("local[*]") \
    .getOrCreate()

# Create a DataFrame from a list of tuples
data = [
    ("Alice", 30, "Engineering"),
    ("Bob", 25, "Marketing"),
    ("Carol", 35, "Engineering"),
    ("David", 28, "HR"),
    ("Eve", 32, "Marketing"),
]
columns = ["name", "age", "department"]

df = spark.createDataFrame(data, columns)

# Inspect the DataFrame
df.show()
df.printSchema()
print("Row count:", df.count())

# Select specific columns
df.select("name", "department").show()

# Filter rows
df.filter(col("age") > 28).show()

# Add a new column
df.withColumn("name_upper", upper(col("name"))) \
  .withColumn("country", lit("Spain")) \
  .show()

# Drop a column
df.drop("department").show()

# Rename a column
df.withColumnRenamed("age", "years_old").show()

# Sort
df.orderBy("age", ascending=False).show()

spark.stop()