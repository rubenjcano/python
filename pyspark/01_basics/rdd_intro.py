from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("RDD Intro") \
    .master("local[*]") \
    .getOrCreate()

sc = spark.sparkContext

# Create an RDD from a list
numbers = sc.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Basic transformations (lazy — nothing runs yet)
evens = numbers.filter(lambda x: x % 2 == 0)
squared = evens.map(lambda x: x ** 2)

# Action — this triggers the actual computation
result = squared.collect()
print("Even numbers squared:", result)

# Other useful actions
print("Sum:", numbers.reduce(lambda a, b: a + b))
print("Count:", numbers.count())
print("First:", numbers.first())
print("Take 3:", numbers.take(3))

# Word count — the classic Spark example
text = sc.parallelize([
    "spark is fast",
    "spark is easy",
    "spark is powerful"
])

word_counts = text \
    .flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .sortBy(lambda x: x[1], ascending=False)

print("\nWord counts:")
for word, count in word_counts.collect():
    print(f"  {word}: {count}")

spark.stop()