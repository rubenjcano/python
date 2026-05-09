from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Spark SQL") \
    .master("local[*]") \
    .getOrCreate()

data = [
    ("Alice", 30, "Engineering", 70000),
    ("Bob", 25, "Marketing", 50000),
    ("Carol", 35, "Engineering", 90000),
    ("David", 28, "HR", 55000),
    ("Eve", 32, "Marketing", 62000),
    ("Frank", 40, "Engineering", 95000),
]
columns = ["name", "age", "department", "salary"]

df = spark.createDataFrame(data, columns)

# Register the DataFrame as a temporary SQL view
df.createOrReplaceTempView("employees")

# Basic SELECT
spark.sql("SELECT * FROM employees").show()

# Filtering
spark.sql("""
    SELECT name, salary
    FROM employees
    WHERE salary > 60000
    ORDER BY salary DESC
""").show()

# Aggregation
spark.sql("""
    SELECT
        department,
        COUNT(*) AS num_employees,
        AVG(salary) AS avg_salary,
        MAX(salary) AS max_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""").show()

# Subquery
spark.sql("""
    SELECT name, department, salary
    FROM employees
    WHERE salary > (SELECT AVG(salary) FROM employees)
""").show()

spark.stop()