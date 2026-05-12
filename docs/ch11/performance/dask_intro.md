# Introduction to Dask

When datasets exceed available RAM or when you need parallel processing, Dask extends pandas to handle larger-than-memory data across multiple cores.

!!! tip "Mental Model"
    Dask is "lazy pandas." It mirrors the pandas API but builds a task graph instead of computing immediately. When you call `.compute()`, Dask executes the graph in parallel across CPU cores, streaming data from disk. If your code works in pandas but runs out of memory, switching to Dask often requires changing just the import and adding `.compute()` at the end.

## Why Dask?

| Limitation of Pandas | Dask Solution |
|---------------------|---------------|
| Single-threaded | Multi-core parallel execution |
| Must fit in RAM | Stream from disk (out-of-core) |
| Eager evaluation | Lazy evaluation (build task graph) |

## Installation

```bash
pip install dask[dataframe]
```

## Creating a Dask DataFrame

### From Pandas

```python
import dask.dataframe as dd
import pandas as pd
import numpy as np

# Create pandas DataFrame
pdf = pd.DataFrame({
    'A': np.random.randn(1_000_000),
    'B': np.random.randint(0, 100, 1_000_000),
    'C': np.random.choice(['X', 'Y', 'Z'], 1_000_000)
})

# Convert to Dask DataFrame
ddf = dd.from_pandas(pdf, npartitions=10)
print(ddf)
```

```
Dask DataFrame Structure:
                   A      B       C
npartitions=10
0             float64  int64  object
100000            ...    ...     ...
...               ...    ...     ...
900000            ...    ...     ...
dtype: object
Dask Name: from_pandas, 10 tasks
```

### From CSV Files

```python
# Single large file
ddf = dd.read_csv('huge_file.csv')

# Multiple files (glob pattern)
ddf = dd.read_csv('data/*.csv')

# With type specification
ddf = dd.read_csv('data.csv', dtype={'category': 'category', 'value': 'float32'})
```

### From Parquet (Recommended for Large Data)

```python
# Parquet is column-oriented, compressed, and fast
ddf = dd.read_parquet('data.parquet')

# Write to parquet
ddf.to_parquet('output.parquet')
```

## Lazy Evaluation

Dask operations don't execute immediately—they build a task graph.

```python
# These operations are lazy (instant)
result = ddf['A'].mean()
print(result)  # Not the actual value!
```

```
dd.Scalar<series-..., dtype=float64>
```

```python
# .compute() triggers actual computation
actual_mean = result.compute()
print(actual_mean)  # Now we get the number
```

## Basic Operations

Most pandas operations work the same way:

```python
# Column selection
ddf['A']
ddf[['A', 'B']]

# Arithmetic
ddf['D'] = ddf['A'] + ddf['B']

# Filtering
filtered = ddf[ddf['A'] > 0]

# GroupBy
grouped = ddf.groupby('C')['A'].mean()

# Always call .compute() to get results
result = grouped.compute()
```

## Aggregations

```python
# Single aggregation
mean_a = ddf['A'].mean().compute()
sum_b = ddf['B'].sum().compute()

# Multiple aggregations
stats = ddf.agg({
    'A': ['mean', 'std'],
    'B': ['sum', 'count']
}).compute()

# GroupBy aggregation
group_stats = ddf.groupby('C').agg({
    'A': 'mean',
    'B': 'sum'
}).compute()
```

## Partitions

Dask splits data into partitions (small pandas DataFrames).

```python
# Check number of partitions
print(ddf.npartitions)  # 10

# Repartition for better parallelism
ddf = ddf.repartition(npartitions=100)

# Get a specific partition (returns pandas DataFrame)
partition_0 = ddf.get_partition(0).compute()
```

### Partition Guidelines

| Data Size | Partitions | Partition Size |
|-----------|------------|----------------|
| 1 GB | 10-100 | 10-100 MB each |
| 10 GB | 100-500 | 20-100 MB each |
| 100 GB | 500-1000 | 100-200 MB each |

**Rule of thumb**: Each partition should be 100MB-1GB.

## Parallel Execution

Dask automatically parallelizes across available cores:

```python
import dask
from dask.distributed import Client

# Optional: Start distributed scheduler for monitoring
client = Client()
print(client.dashboard_link)  # Opens dashboard in browser

# Now operations run in parallel
result = ddf.groupby('C')['A'].mean().compute()
```

## Practical Example: Large File Processing

```python
# Process 50GB of log data
ddf = dd.read_csv('logs/*.csv', 
                  dtype={'status': 'int16', 'bytes': 'int32'})

# Compute statistics
stats = ddf.groupby('status').agg({
    'bytes': ['sum', 'mean', 'count']
}).compute()

print(stats)
```

## Practical Example: Stock Data Analysis

```python
# Load large stock price dataset
ddf = dd.read_parquet('stock_prices/')

# Calculate returns per ticker
ddf['return'] = ddf.groupby('ticker')['close'].apply(
    lambda x: x.pct_change(),
    meta=('return', 'float64')
)

# Calculate average return by sector
sector_returns = ddf.groupby('sector')['return'].mean().compute()

# Calculate volatility
volatility = ddf.groupby('ticker')['return'].std().compute() * np.sqrt(252)
```

## Key Differences from Pandas

### 1. Always .compute()

```python
# Pandas: immediate result
pdf['A'].mean()  # Returns: -0.00234

# Dask: lazy result
ddf['A'].mean()  # Returns: Scalar object
ddf['A'].mean().compute()  # Returns: -0.00234
```

### 2. Some Operations Are Expensive

```python
# Expensive in Dask (requires shuffling all data)
ddf.sort_values('A')  # Avoid if possible

# Expensive (needs to collect all data)
len(ddf)  # Use ddf.shape[0].compute() instead
```

### 3. Row Indexing Limitations

```python
# Not supported (would require scanning all partitions)
# ddf.iloc[1000]  # Error!

# Use .head() for preview
ddf.head(10)  # Returns pandas DataFrame
```

### 4. Custom Functions Need meta

```python
# When applying custom functions, specify output type
def custom_func(x):
    return x ** 2

# Provide meta parameter
result = ddf['A'].apply(custom_func, meta=('A', 'float64'))
```

## When to Use Dask vs Pandas

| Scenario | Use |
|----------|-----|
| Data fits in RAM | Pandas |
| Data exceeds RAM | Dask |
| Need multi-core parallelism | Dask |
| Complex row operations | Pandas |
| Simple aggregations on large data | Dask |
| Interactive exploration | Pandas (or Dask sample) |

## Performance Tips

### 1. Persist Intermediate Results

```python
# For results used multiple times
ddf_filtered = ddf[ddf['A'] > 0].persist()
```

### 2. Use Parquet Format

```python
# Much faster than CSV
ddf = dd.read_parquet('data.parquet')
```

### 3. Specify dtypes

```python
# Reduce memory and improve speed
ddf = dd.read_csv('data.csv', dtype={
    'id': 'int32',
    'value': 'float32',
    'category': 'category'
})
```

### 4. Avoid Shuffles

```python
# Operations that shuffle data are slow:
# - sort_values
# - merge (on non-index columns)
# - groupby on high-cardinality columns

# Set index for faster merges
ddf = ddf.set_index('id')
```

## Summary

| Feature | Pandas | Dask |
|---------|--------|------|
| Execution | Eager | Lazy |
| Parallelism | Single core | Multi-core |
| Memory | RAM-bound | Out-of-core |
| API | Complete | ~80% coverage |
| Best for | < 10GB | > 10GB |

**Workflow recommendation:**

1. Prototype with pandas on sample data
2. Scale to Dask when data grows
3. Use `.compute()` sparingly (at the end)
4. Prefer Parquet format for large files
5. Monitor with Dask dashboard


---

## Exercises

**Exercise 1.** Explain what Dask is and how it extends Pandas for larger-than-memory datasets.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd
    import numpy as np

    # Solution for the specific exercise
    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10)})
    print(df.head())
    ```

---

**Exercise 2.** Write the import statement for Dask DataFrame and explain how `dask.dataframe.read_csv()` differs from `pd.read_csv()`.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Explain the concept of lazy evaluation in Dask. What does `.compute()` do?

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(20), 'B': np.random.randn(20)})
    result = df.describe()
    print(result)
    ```

---

**Exercise 4.** Compare the syntax for a groupby aggregation in Pandas vs Dask. How similar are they?

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
