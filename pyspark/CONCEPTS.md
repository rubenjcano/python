# Spark Concepts 🧠

A conceptual overview of Apache Spark — what it is, how it works, and what libraries it provides. Read this before diving into the code examples.

---

## What is Spark?

Spark is an engine that analyzes data in a **distributed fashion**. It really shines when streaming or running analytics on very large datasets — the kind that wouldn't fit or would be too slow on a single machine.

---

## Core Architecture

Spark is built around four main components:

| Component | Role |
|---|---|
| **Master Node** | Receives user applications and communicates with the cluster manager |
| **Cluster Manager** | Distributes computation across worker nodes (you don't interact with this directly) |
| **Worker Node** | Executes the actual computation assigned to it |
| **Application** | Your code — written in Python, Scala, Java, or R — that uses the Spark API |

### How they connect

```
Your Application
      ↓
  Master Node
      ↓
Cluster Manager
      ↓
Worker Nodes (do the actual work)
```

The cluster manager handles distributing work efficiently and transparently. Worker nodes are configured with a set amount of resources and execute whatever they are assigned.

---

## General Workflow (standalone cluster)

```bash
# 1. Start the master node
./sbin/start-master.sh

# 2. Start one or more worker nodes (use the URL printed by the master)
./sbin/start-slave.sh <master-node-URL>

# 3. Check the Spark UI
open http://localhost:8080

# 4. Submit your application
spark-submit your_app.py
```

The **Spark UI** at `localhost:8080` is very useful — it lets you monitor running applications, resource usage, and job progress in real time.

---

## RDD — Resilient Distributed Dataset

An RDD is the **fundamental data structure of Spark**. Everything else (DataFrames, Datasets) is built on top of it.

### What it is

An RDD is an immutable, distributed collection of objects spread across the nodes of a cluster. Breaking down the name:

| Word | Meaning |
|---|---|
| **Resilient** | Fault-tolerant — if a partition is lost, Spark can recompute it from the original data |
| **Distributed** | Data is split into partitions and spread across worker nodes |
| **Dataset** | A collection of records (can be anything — strings, tuples, objects) |

### How it works

When you create an RDD, Spark splits the data into **partitions** and assigns each partition to a worker node. Operations run in parallel across all partitions.

```
RDD
├── Partition 1  →  Worker Node 1
├── Partition 2  →  Worker Node 2
└── Partition 3  →  Worker Node 3
```

### Transformations vs Actions

This is one of the most important concepts in Spark — operations on RDDs are either **lazy transformations** or **eager actions**.

**Transformations** — define a new RDD, but do nothing yet:
- `map()` — apply a function to each element
- `filter()` — keep elements matching a condition
- `flatMap()` — like map, but flattens the result
- `reduceByKey()` — group by key and reduce values

**Actions** — trigger the actual computation:
- `collect()` — return all elements to the driver
- `count()` — return the number of elements
- `first()` — return the first element
- `take(n)` — return the first n elements
- `saveAsTextFile()` — write to disk

```python
rdd = sc.parallelize([1, 2, 3, 4, 5])

# Transformations — nothing runs yet
evens = rdd.filter(lambda x: x % 2 == 0)
squared = evens.map(lambda x: x ** 2)

# Action — this triggers everything above
result = squared.collect()  # [4, 16]
```

### RDD vs DataFrame

In modern PySpark you will mostly use **DataFrames**, not RDDs directly. Here's why:

| | RDD | DataFrame |
|---|---|---|
| Structure | Unstructured (any Python object) | Structured (rows and columns with schema) |
| Optimization | Manual | Automatic via Catalyst optimizer |
| Performance | Slower (no optimization) | Faster |
| API | Functional (`map`, `filter`) | SQL-like (`select`, `groupBy`) |
| When to use | Custom objects, complex logic, legacy code | Almost everything else |

> RDDs are still important to understand because DataFrames are built on top of them, and knowing RDDs helps you reason about what Spark is doing under the hood.

---

## The Four Spark Libraries

### 1. Spark Streaming
For processing **real-time data streams**. Supports sources like HDFS, Kafka, Flume, and Twitter. The key power: you can combine streaming with batch processing, SQL queries, and even ML — all in one pipeline.

### 2. Spark SQL
For processing **structured data** using SQL-like syntax. Available in Python, Scala, Java, and R. Works great with JSON, Parquet, CSV, and databases. Can be combined with Spark Streaming to query structured data as it arrives.

```python
df.createOrReplaceTempView("sales")
spark.sql("SELECT region, SUM(revenue) FROM sales GROUP BY region").show()
```

### 3. MLlib
Spark's built-in **machine learning library**. Includes classification, regression, clustering, collaborative filtering, and more — all running distributed across the cluster.

### 4. GraphX
For **graph-based computation and analysis** — think social networks, recommendation graphs, or any dataset where relationships between entities matter. Extends Spark SQL with graph processing capabilities.

---

## Why Spark over traditional tools?

- **Speed** — in-memory processing, much faster than Hadoop MapReduce
- **Unified** — one engine for batch, streaming, SQL, ML, and graph
- **Multi-language** — Python, Scala, Java, R all supported
- **Fault-tolerant** — if a worker node fails, Spark recovers automatically
- **Scalable** — runs on a laptop locally or across thousands of nodes in the cloud

---

## Where PySpark fits

PySpark is simply the Python API for Spark. When you write PySpark, your Python code talks to the Spark engine running on the JVM. Thanks to **Apache Arrow**, data transfer between Python and the JVM is now highly efficient — making PySpark a production-grade choice for most data engineering workloads.

> See the examples in this repo to start applying these concepts hands-on.