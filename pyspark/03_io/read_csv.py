from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

spark = SparkSession.builder \
    .appName("Read CSV") \
    .master("local[*]") \
    .getOrCreate()

# -----------------------------------------------------------
# Option 1: infer schema automatically (convenient, slower)
# -----------------------------------------------------------
df_inferred = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("data/input/sales.csv")

df_inferred.show()
df_inferred.printSchema()

# -----------------------------------------------------------
# Option 2: define schema manually (recommended for production)
# Faster and avoids type surprises
# -----------------------------------------------------------
schema = StructType([
    StructField("date", StringType(), True),
    StructField("product", StringType(), True),
    StructField("category", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("revenue", DoubleType(), True),
])

df_typed = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv("data/input/sales.csv")

df_typed.show()
df_typed.printSchema()

# -----------------------------------------------------------
# Useful read options
# -----------------------------------------------------------
# .option("sep", ";")           → different delimiter
# .option("nullValue", "N/A")   → treat "N/A" as null
# .option("dateFormat", "yyyy-MM-dd")
# .option("multiLine", "true")  → for multiline fields

spark.stop()