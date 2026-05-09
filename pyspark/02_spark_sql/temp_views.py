from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Temp Views") \
    .master("local[*]") \
    .getOrCreate()

employees = spark.createDataFrame([
    (1, "Alice", 10),
    (2, "Bob", 20),
    (3, "Carol", 10),
], ["id", "name", "dept_id"])

departments = spark.createDataFrame([
    (10, "Engineering"),
    (20, "Marketing"),
], ["dept_id", "dept_name"])

# createOrReplaceTempView → session-scoped (disappears when session ends)
employees.createOrReplaceTempView("employees")
departments.createOrReplaceTempView("departments")

# Join across views using SQL
spark.sql("""
    SELECT e.name, d.dept_name
    FROM employees e
    JOIN departments d ON e.dept_id = d.dept_id
""").show()

# createGlobalTempView → accessible across sessions (global_temp schema)
employees.createGlobalTempView("employees_global")

spark.sql("SELECT * FROM global_temp.employees_global").show()

# List available views
print("Available views:")
spark.catalog.listTables()

spark.stop()