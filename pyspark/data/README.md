# Sample Data

This folder contains sample input files used by the scripts in this repo.

| File | Used by | Description |
|---|---|---|
| `sales.csv` | `03_io/read_csv.py`, `03_io/write_partitioned.py` | Monthly sales records by product and category |
| `sales.parquet` | `03_io/read_parquet.py` | Same sales data in Parquet format |
| `employees.csv` | `02_spark_sql/sql_queries.py`, `04_transformations/aggregations.py` | Employee records with department and salary |
| `orders.csv` | `04_transformations/joins.py` | Customer orders linked to products |
| `products.csv` | `04_transformations/joins.py` | Product catalog with category and price |

> `data/output/` is git-ignored — it gets populated when you run the scripts.
