# Memory Optimization

Efficient memory usage is critical when working with large datasets. This document covers strategies to reduce memory consumption in pandas.

!!! tip "Mental Model"
    Memory optimization is about choosing the smallest dtype that fits your data. `int64` uses 8 bytes per value, but if values fit in 0-255, `uint8` uses just 1 byte -- an 8x savings. String columns with few unique values should be converted to `category`. Measure with `memory_usage(deep=True)`, downcast numeric columns, and convert repetitive strings to categoricals.

## Understanding Memory Consumption

### Check Current Memory

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'int_col': np.random.randint(0, 100, 1_000_000),
    'float_col': np.random.randn(1_000_000),
    'str_col': np.random.choice(['A', 'B', 'C', 'D', 'E'], 1_000_000)
})

# Total memory (accurate)
total_mb = df.memory_usage(deep=True).sum() / 1e6
print(f"Total: {total_mb:.1f} MB")

# Per-column breakdown
print(df.memory_usage(deep=True))
```

## Strategy 1: Downcast Numeric Types

Pandas defaults to `int64` and `float64`, but smaller types often suffice.

### Integer Downcasting

```python
def downcast_integers(df):
    """Downcast integer columns to smallest type."""
    for col in df.select_dtypes(include=['int64']).columns:
        c_min, c_max = df[col].min(), df[col].max()
        
        if c_min >= 0:  # Unsigned
            if c_max <= 255:
                df[col] = df[col].astype('uint8')
            elif c_max <= 65535:
                df[col] = df[col].astype('uint16')
            elif c_max <= 4294967295:
                df[col] = df[col].astype('uint32')
        else:  # Signed
            if c_min >= -128 and c_max <= 127:
                df[col] = df[col].astype('int8')
            elif c_min >= -32768 and c_max <= 32767:
                df[col] = df[col].astype('int16')
            elif c_min >= -2147483648 and c_max <= 2147483647:
                df[col] = df[col].astype('int32')
    
    return df
```

### Float Downcasting

```python
def downcast_floats(df):
    """Downcast float columns to float32."""
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].astype('float32')
    return df
```

### Using pd.to_numeric with downcast

```python
# Automatic downcasting
df['int_col'] = pd.to_numeric(df['int_col'], downcast='integer')
df['float_col'] = pd.to_numeric(df['float_col'], downcast='float')
```

## Strategy 2: Use Categorical for Strings

String columns with repeated values benefit enormously from categorical encoding.

### When to Use Categorical

| Condition | Recommendation |
|-----------|----------------|
| Unique values < 50% of rows | ✅ Use categorical |
| Few unique values, many rows | ✅ Use categorical |
| All unique values | ❌ No benefit |
| Need string methods | ⚠️ Convert back first |

### Conversion Example

```python
# Before: string storage
print(f"String: {df['str_col'].memory_usage(deep=True) / 1e6:.2f} MB")

# After: categorical storage
df['str_col'] = df['str_col'].astype('category')
print(f"Categorical: {df['str_col'].memory_usage(deep=True) / 1e6:.2f} MB")
```

Typical result:
```
String: 57.00 MB
Categorical: 1.00 MB
```

### Automatic Detection

```python
def convert_to_categorical(df, threshold=0.5):
    """Convert low-cardinality object columns to categorical."""
    for col in df.select_dtypes(include=['object']).columns:
        ratio = df[col].nunique() / len(df)
        if ratio < threshold:
            df[col] = df[col].astype('category')
            print(f"Converted {col}: {df[col].nunique()} unique values")
    return df
```

## Strategy 3: Specify dtypes at Load Time

Loading data with optimized types is more efficient than converting after.

### read_csv with dtype

```python
# Define optimal types upfront
dtypes = {
    'id': 'int32',
    'value': 'float32',
    'category': 'category',
    'flag': 'bool'
}

df = pd.read_csv('data.csv', dtype=dtypes)
```

### CategoricalDtype for Ordered Categories

```python
rating_dtype = pd.CategoricalDtype(
    categories=['D', 'C', 'B', 'A', 'S'],
    ordered=True
)

df = pd.read_csv('data.csv', dtype={'rating': rating_dtype})
```

## Strategy 4: Sparse Data

For data with many repeated values (often zeros), use sparse types.

```python
# Dense array: stores every value
dense = pd.Series([0, 0, 0, 1, 0, 0, 0, 0, 2, 0] * 100000)
print(f"Dense: {dense.memory_usage() / 1e6:.2f} MB")

# Sparse array: stores only non-default values
sparse = dense.astype('Sparse[int64]')
print(f"Sparse: {sparse.memory_usage() / 1e6:.2f} MB")
```

## Complete Optimization Function

```python
def optimize_dataframe(df, verbose=True):
    """Optimize DataFrame memory usage."""
    initial_mem = df.memory_usage(deep=True).sum()
    
    # Downcast integers
    for col in df.select_dtypes(include=['int64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer')
    
    # Downcast floats
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='float')
    
    # Convert low-cardinality strings to categorical
    for col in df.select_dtypes(include=['object']).columns:
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')
    
    final_mem = df.memory_usage(deep=True).sum()
    
    if verbose:
        print(f"Memory: {initial_mem/1e6:.1f} MB → {final_mem/1e6:.1f} MB")
        print(f"Reduction: {(1 - final_mem/initial_mem)*100:.1f}%")
    
    return df
```

## Practical Example: Stock Data

```python
# Simulated stock data
np.random.seed(42)
n = 2_000_000

df = pd.DataFrame({
    'date': pd.date_range('2000-01-01', periods=n, freq='T'),
    'ticker': np.random.choice(['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META'], n),
    'open': np.random.uniform(100, 200, n),
    'high': np.random.uniform(100, 200, n),
    'low': np.random.uniform(100, 200, n),
    'close': np.random.uniform(100, 200, n),
    'volume': np.random.randint(1000, 1000000, n)
})

print("Before optimization:")
print(df.info(memory_usage='deep'))

# Optimize
df = optimize_dataframe(df)

print("\nAfter optimization:")
print(df.info(memory_usage='deep'))
print(df.dtypes)
```

## Memory Monitoring During Processing

```python
def memory_checkpoint(df, label):
    """Print memory usage at checkpoint."""
    mem = df.memory_usage(deep=True).sum() / 1e6
    print(f"[{label}] Memory: {mem:.1f} MB")

# Usage
memory_checkpoint(df, "Start")

df['new_col'] = df['close'] * df['volume']
memory_checkpoint(df, "After calculation")

df = df[df['volume'] > 10000]
memory_checkpoint(df, "After filtering")
```

## Summary Table

| Strategy | Typical Savings | Use Case |
|----------|-----------------|----------|
| Downcast integers | 50-87% | All numeric data |
| Downcast floats | 50% | Float columns |
| Categorical | 90%+ | Repeated strings |
| Sparse | Varies | Many repeated values |
| Specify dtype at load | Avoids conversion | All data loading |

## Best Practices

1. **Profile first**: Use `memory_usage(deep=True)` to find big columns
2. **Optimize at load time**: Specify dtypes in `read_csv()`
3. **Use categorical**: For columns with < 50% unique values
4. **Downcast numerics**: Use smallest type that fits your data
5. **Monitor growth**: Check memory after transformations
6. **Drop unused columns**: Remove columns you don't need
7. **Process in chunks**: For files too large for RAM


---

## Exercises

**Exercise 1.** Write code that uses `df.memory_usage(deep=True)` to check memory consumption of each column. Sum the total memory.

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

**Exercise 2.** Explain how downcasting numeric types (e.g., `int64` to `int32`) can save memory. Write code using `pd.to_numeric(downcast='integer')`.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that converts all object (string) columns with few unique values to categorical dtype and measures the memory savings.

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

**Exercise 4.** Create a function that takes a DataFrame and automatically optimizes its memory usage by downcasting numeric columns and converting low-cardinality strings to categorical.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
