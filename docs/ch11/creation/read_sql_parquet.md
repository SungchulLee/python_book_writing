# Reading SQL and Parquet Files

pandas supports reading data from SQL databases and Parquet files, which are common in enterprise and big data environments.

!!! tip "Mental Model"
    `read_sql` treats a database query result as a DataFrame -- the SQL engine does the heavy filtering, and pandas receives the final table. `read_parquet` loads columnar binary files that preserve dtypes exactly, making round-trips lossless and fast. Both skip the parsing overhead of text formats like CSV.

## pd.read_sql - Database Connectivity

### Basic Setup

```python
import pandas as pd
import sqlite3

# Create a SQLite connection (example)
conn = sqlite3.connect('database.db')

# For other databases, use appropriate drivers:
# PostgreSQL: psycopg2
# MySQL: pymysql or mysql-connector-python
# SQL Server: pyodbc
# Oracle: cx_Oracle
```

### Reading with SQL Query

```python
# Execute a SQL query and load results into DataFrame
query = "SELECT * FROM employees WHERE department = 'Sales'"
df = pd.read_sql(query, conn)
print(df)
```

### Reading Entire Table

```python
# Load an entire table
df = pd.read_sql_table('employees', conn)

# Or using read_sql with table name
df = pd.read_sql('employees', conn)
```

### Connection Strings

```python
# SQLAlchemy connection string format (recommended)
from sqlalchemy import create_engine

# SQLite
engine = create_engine('sqlite:///database.db')

# PostgreSQL
engine = create_engine('postgresql://user:password@localhost:5432/dbname')

# MySQL
engine = create_engine('mysql+pymysql://user:password@localhost:3306/dbname')

# SQL Server
engine = create_engine('mssql+pyodbc://user:password@server/dbname?driver=ODBC+Driver+17+for+SQL+Server')

# Read using engine
df = pd.read_sql("SELECT * FROM table_name", engine)
```

### Parameterized Queries

```python
# Safe parameter passing (prevents SQL injection)
query = "SELECT * FROM employees WHERE salary > :min_salary"
df = pd.read_sql(query, conn, params={'min_salary': 50000})

# With SQLite positional parameters
query = "SELECT * FROM employees WHERE department = ?"
df = pd.read_sql(query, conn, params=['Sales'])
```

### Chunked Reading for Large Tables

```python
# Read in chunks for memory efficiency
chunks = pd.read_sql(
    "SELECT * FROM large_table",
    conn,
    chunksize=10000
)

# Process chunks
for chunk in chunks:
    process(chunk)
    
# Or concatenate all chunks
df = pd.concat(chunks, ignore_index=True)
```

### Setting Index from Column

```python
# Use a column as the DataFrame index
df = pd.read_sql(
    "SELECT id, name, value FROM table",
    conn,
    index_col='id'
)
```

### Parsing Dates

```python
# Auto-parse date columns
df = pd.read_sql(
    "SELECT * FROM orders",
    conn,
    parse_dates=['order_date', 'ship_date']
)

# With custom format
df = pd.read_sql(
    "SELECT * FROM orders",
    conn,
    parse_dates={'order_date': '%Y-%m-%d'}
)
```

### Key Parameters for read_sql

| Parameter | Description | Default |
|-----------|-------------|---------|
| `sql` | SQL query or table name | Required |
| `con` | Database connection | Required |
| `index_col` | Column to use as index | None |
| `coerce_float` | Convert decimal to float | True |
| `params` | Query parameters | None |
| `parse_dates` | Columns to parse as dates | None |
| `chunksize` | Rows per chunk | None |

## pd.read_parquet - Columnar File Format

Parquet is a columnar storage format optimized for analytical queries.

### Why Parquet?

| Feature | CSV | Parquet |
|---------|-----|---------|
| Compression | None/External | Built-in (snappy, gzip, zstd) |
| Schema | None | Embedded |
| Read speed | Row-by-row | Column-oriented |
| Partial read | No | Column selection |
| File size | Large | 2-10x smaller |
| Type preservation | No | Yes |

### Basic Reading

```python
# Read entire parquet file
df = pd.read_parquet('data.parquet')

# Read from URL
df = pd.read_parquet('https://example.com/data.parquet')

# Read from S3 (requires s3fs)
df = pd.read_parquet('s3://bucket/data.parquet')
```

### Column Selection

One of Parquet's key advantages is reading only needed columns.

```python
# Read only specific columns (much faster for wide tables)
df = pd.read_parquet('data.parquet', columns=['id', 'name', 'value'])

# Compare performance
import time

start = time.time()
df_all = pd.read_parquet('wide_table.parquet')  # 100 columns
print(f"All columns: {time.time() - start:.2f}s")

start = time.time()
df_subset = pd.read_parquet('wide_table.parquet', columns=['col1', 'col2'])
print(f"2 columns: {time.time() - start:.2f}s")
```

### Reading with Filters (Row Groups)

```python
# PyArrow filters (if using pyarrow engine)
# This filters at read time, reducing memory usage
df = pd.read_parquet(
    'data.parquet',
    filters=[
        ('year', '>=', 2020),
        ('category', '==', 'A')
    ]
)
```

### Partitioned Parquet Files

Parquet files can be partitioned by column values (like Hive-style partitioning).

```
data/
├── year=2023/
│   ├── month=01/
│   │   └── data.parquet
│   └── month=02/
│       └── data.parquet
└── year=2024/
    └── month=01/
        └── data.parquet
```

```python
# Read entire partitioned dataset
df = pd.read_parquet('data/')

# Partition columns are added automatically
print(df.columns)  # [...original columns..., 'year', 'month']

# With filters on partition columns (very efficient)
df = pd.read_parquet(
    'data/',
    filters=[('year', '==', 2024)]
)
```

### Choosing Parquet Engine

```python
# PyArrow (default, recommended)
df = pd.read_parquet('data.parquet', engine='pyarrow')

# fastparquet (alternative)
df = pd.read_parquet('data.parquet', engine='fastparquet')
```

### Writing Parquet Files

```python
# Basic write
df.to_parquet('output.parquet')

# With compression
df.to_parquet('output.parquet', compression='snappy')  # Fast, moderate compression
df.to_parquet('output.parquet', compression='gzip')    # Slower, better compression
df.to_parquet('output.parquet', compression='zstd')    # Best balance

# Partitioned write
df.to_parquet('output/', partition_cols=['year', 'month'])
```

### Key Parameters for read_parquet

| Parameter | Description | Default |
|-----------|-------------|---------|
| `path` | File path or URL | Required |
| `engine` | 'pyarrow' or 'fastparquet' | 'auto' |
| `columns` | Columns to read | None (all) |
| `filters` | Row group filters | None |
| `use_nullable_dtypes` | Use nullable dtypes | False |

## Practical Examples

### 1. Database to DataFrame Workflow

```python
from sqlalchemy import create_engine
import pandas as pd

# Connect to PostgreSQL
engine = create_engine('postgresql://user:pass@localhost/sales_db')

# Load recent orders
query = """
    SELECT 
        o.order_id,
        o.order_date,
        c.customer_name,
        p.product_name,
        o.quantity,
        o.total_price
    FROM orders o
    JOIN customers c ON o.customer_id = c.id
    JOIN products p ON o.product_id = p.id
    WHERE o.order_date >= '2024-01-01'
"""

df = pd.read_sql(query, engine, parse_dates=['order_date'])

# Analysis
daily_sales = df.groupby(df['order_date'].dt.date)['total_price'].sum()
print(daily_sales)
```

### 2. Large Dataset with Parquet

```python
# Read large dataset efficiently
df = pd.read_parquet(
    'transactions.parquet',
    columns=['date', 'amount', 'category'],
    filters=[('date', '>=', '2024-01-01')]
)

# Aggregate
summary = df.groupby('category')['amount'].agg(['sum', 'mean', 'count'])
print(summary)
```

### 3. ETL Pipeline: SQL to Parquet

```python
# Extract from database
df = pd.read_sql(
    "SELECT * FROM large_table WHERE updated_at > :last_run",
    engine,
    params={'last_run': '2024-01-01'},
    chunksize=100000
)

# Transform and load to Parquet
for i, chunk in enumerate(df):
    # Transform
    chunk = chunk.dropna()
    chunk['processed_at'] = pd.Timestamp.now()
    
    # Load to partitioned Parquet
    chunk.to_parquet(
        f'output/batch_{i}.parquet',
        compression='snappy'
    )
```

### 4. Financial Data Storage

```python
import yfinance as yf

# Get historical data
tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN']
data = {}

for ticker in tickers:
    data[ticker] = yf.Ticker(ticker).history(period='5y')

# Combine into panel format
df = pd.concat(data, names=['ticker', 'date'])
df = df.reset_index()

# Save as partitioned Parquet (efficient for queries by ticker)
df.to_parquet('stock_data/', partition_cols=['ticker'])

# Read specific ticker efficiently
aapl = pd.read_parquet('stock_data/', filters=[('ticker', '==', 'AAPL')])
```

## Performance Comparison

```python
import time
import pandas as pd
import numpy as np

# Create sample data
n_rows = 1_000_000
df = pd.DataFrame({
    'id': range(n_rows),
    'value': np.random.randn(n_rows),
    'category': np.random.choice(['A', 'B', 'C'], n_rows),
    'date': pd.date_range('2020-01-01', periods=n_rows, freq='s')
})

# Save in different formats
df.to_csv('data.csv', index=False)
df.to_parquet('data.parquet')

# Compare read times
start = time.time()
df_csv = pd.read_csv('data.csv')
csv_time = time.time() - start

start = time.time()
df_parquet = pd.read_parquet('data.parquet')
parquet_time = time.time() - start

print(f"CSV read time: {csv_time:.2f}s")
print(f"Parquet read time: {parquet_time:.2f}s")
print(f"Speedup: {csv_time/parquet_time:.1f}x")

# File sizes
import os
print(f"\nCSV size: {os.path.getsize('data.csv') / 1e6:.1f} MB")
print(f"Parquet size: {os.path.getsize('data.parquet') / 1e6:.1f} MB")
```

Typical results:
- Parquet is 5-10x faster to read than CSV
- Parquet files are 2-10x smaller than CSV
- Column selection in Parquet provides additional speedup

## Common Pitfalls (SQL)

### 1. Database Connection Not Closed

```python
# Bad: Connection stays open
df = pd.read_sql("SELECT * FROM table", conn)

# Good: Use context manager
with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM table", conn)
# Connection automatically closed
```

### 2. SQL Injection Vulnerability

```python
# DANGEROUS: String formatting
user_input = "Sales'; DROP TABLE employees;--"
query = f"SELECT * FROM emp WHERE dept = '{user_input}'"

# SAFE: Use parameterized queries
query = "SELECT * FROM emp WHERE dept = :dept"
df = pd.read_sql(query, conn, params={'dept': user_input})
```

### 3. Parquet Type Preservation

```python
# Categorical and nullable types may need explicit handling
df = pd.read_parquet('data.parquet')

# Convert categorical back if needed
df['category'] = df['category'].astype('category')
```

---

## Exercises

**Exercise 1.**
Using SQLite and `pd.read_sql`, create an in-memory database with a table named `products` that has columns `id`, `name`, and `price`. Insert three rows, then read the table into a DataFrame using a parameterized query that selects only products with `price > 10`.

??? success "Solution to Exercise 1"
    Create an in-memory SQLite database, insert rows, and query with parameters.

        import pandas as pd
        import sqlite3

        conn = sqlite3.connect(':memory:')
        conn.execute('''
            CREATE TABLE products (id INTEGER, name TEXT, price REAL)
        ''')
        conn.executemany(
            'INSERT INTO products VALUES (?, ?, ?)',
            [(1, 'Widget', 9.99), (2, 'Gadget', 19.99), (3, 'Gizmo', 14.99)]
        )
        conn.commit()

        query = "SELECT * FROM products WHERE price > ?"
        df = pd.read_sql(query, conn, params=[10])
        print(df)
        conn.close()

---

**Exercise 2.**
Create a DataFrame with columns `'date'`, `'ticker'`, and `'close'`. Save it to a Parquet file. Then read back only the `'ticker'` and `'close'` columns (without loading `'date'`) and verify the result has exactly two columns.

??? success "Solution to Exercise 2"
    Use the `columns` parameter of `read_parquet` to select specific columns.

        import pandas as pd

        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=5),
            'ticker': ['AAPL'] * 5,
            'close': [150.0, 151.0, 149.0, 152.0, 153.0]
        })
        df.to_parquet('stock_data.parquet', index=False)

        df_subset = pd.read_parquet('stock_data.parquet', columns=['ticker', 'close'])
        print(df_subset)
        print(f"Number of columns: {len(df_subset.columns)}")  # 2

---

**Exercise 3.**
Create a DataFrame with 10,000 rows. Save it as both CSV and Parquet. Read both files back and compare the read times using `time.time()`. Print the speedup factor.

??? success "Solution to Exercise 3"
    Time the read operations and compute the speedup ratio.

        import pandas as pd
        import numpy as np
        import time

        np.random.seed(42)
        df = pd.DataFrame({
            'id': range(10000),
            'value': np.random.randn(10000),
            'category': np.random.choice(['A', 'B', 'C', 'D'], 10000)
        })

        df.to_csv('bench.csv', index=False)
        df.to_parquet('bench.parquet')

        start = time.time()
        _ = pd.read_csv('bench.csv')
        csv_time = time.time() - start

        start = time.time()
        _ = pd.read_parquet('bench.parquet')
        parquet_time = time.time() - start

        print(f"CSV read: {csv_time:.4f}s")
        print(f"Parquet read: {parquet_time:.4f}s")
        print(f"Speedup: {csv_time / parquet_time:.1f}x")
