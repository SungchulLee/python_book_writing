# Memory Usage

Understanding memory consumption is essential when working with large datasets. Pandas provides `memory_usage()` and `info()` methods for profiling DataFrame memory.

!!! tip "Mental Model"
    Each column occupies a contiguous block of memory whose size depends on dtype and row count. `memory_usage(deep=True)` measures the true footprint, including the actual string contents of object columns. The key insight: object columns often dominate memory because each cell is a separate Python object, while numeric columns are compact arrays.

## memory_usage() Method

Returns the memory consumption of each column in bytes.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'int_col': np.random.randint(0, 100, 100000),
    'float_col': np.random.randn(100000),
    'str_col': ['category_' + str(i % 10) for i in range(100000)],
    'bool_col': np.random.choice([True, False], 100000)
})

print(df.memory_usage())
```

```
Index          128
int_col     800000
float_col   800000
str_col     800000
bool_col    100000
dtype: int64
```

### The deep Parameter

By default, `memory_usage()` underestimates memory for object columns (strings). Use `deep=True` for accurate measurement:

```python
# Without deep: underestimates string memory
print(f"Shallow: {df.memory_usage().sum() / 1e6:.2f} MB")

# With deep: accurate measurement
print(f"Deep: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
```

```
Shallow: 2.50 MB
Deep: 6.89 MB
```

### Why deep=True Matters

Object dtype columns store pointers to Python objects. Without `deep=True`, only pointer size is counted:

```python
# String column memory comparison
s_string = pd.Series(['hello world'] * 100000)

print(f"Shallow: {s_string.memory_usage() / 1e6:.2f} MB")      # Just pointers
print(f"Deep: {s_string.memory_usage(deep=True) / 1e6:.2f} MB") # Actual strings
```

### index Parameter

Control whether to include index memory:

```python
# Include index (default)
print(df.memory_usage(index=True))

# Exclude index
print(df.memory_usage(index=False))
```

## info() Method

Provides a comprehensive summary including memory usage.

```python
df.info()
```

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 100000 entries, 0 to 99999
Data columns (total 4 columns):
 #   Column     Non-Null Count   Dtype  
---  ------     --------------   -----  
 0   int_col    100000 non-null  int64  
 1   float_col  100000 non-null  float64
 2   str_col    100000 non-null  object 
 3   bool_col   100000 non-null  bool   
dtypes: bool(1), float64(1), int64(1), object(1)
memory usage: 2.4 MB
```

### memory_usage Parameter

```python
# Accurate memory with deep calculation
df.info(memory_usage='deep')
```

```
memory usage: 6.8 MB
```

### verbose Parameter

Control column detail display:

```python
# Suppress column details for wide DataFrames
df.info(verbose=False)
```

## Memory by Data Type

Different dtypes consume different amounts of memory:

| Dtype | Bytes per Value | Notes |
|-------|-----------------|-------|
| `bool` | 1 | Most efficient for True/False |
| `int8` | 1 | Range: -128 to 127 |
| `int16` | 2 | Range: -32,768 to 32,767 |
| `int32` | 4 | Range: ±2.1 billion |
| `int64` | 8 | Default integer type |
| `float16` | 2 | Limited precision |
| `float32` | 4 | Single precision |
| `float64` | 8 | Default float type |
| `object` | 8+ | Pointer + actual object |
| `category` | 1-8 | Depends on category count |

```python
# Compare memory for same data, different types
n = 1_000_000

df_compare = pd.DataFrame({
    'int64': np.array([1, 2, 3, 4, 5] * (n // 5), dtype='int64'),
    'int32': np.array([1, 2, 3, 4, 5] * (n // 5), dtype='int32'),
    'int16': np.array([1, 2, 3, 4, 5] * (n // 5), dtype='int16'),
    'int8': np.array([1, 2, 3, 4, 5] * (n // 5), dtype='int8'),
})

print(df_compare.memory_usage(deep=True))
```

```
Index      128
int64    8000000
int32    4000000
int16    2000000
int8     1000000
dtype: int64
```

## Analyzing Memory Distribution

```python
def memory_report(df):
    """Generate a detailed memory report."""
    mem = df.memory_usage(deep=True)
    total = mem.sum()
    
    print(f"Total Memory: {total / 1e6:.2f} MB\n")
    print(f"{'Column':<20} {'Type':<12} {'Memory':>12} {'Percent':>8}")
    print("-" * 54)
    
    for col in df.columns:
        col_mem = mem[col]
        pct = col_mem / total * 100
        dtype = str(df[col].dtype)
        print(f"{col:<20} {dtype:<12} {col_mem/1e6:>10.2f} MB {pct:>7.1f}%")

memory_report(df)
```

```
Total Memory: 6.89 MB

Column               Type              Memory  Percent
------------------------------------------------------
int_col              int64             0.80 MB   11.6%
float_col            float64           0.80 MB   11.6%
str_col              object            5.19 MB   75.3%
bool_col             bool              0.10 MB    1.5%
```

## Monitoring Memory Growth

Track memory during transformations:

```python
def track_memory(df, operation_name):
    """Print memory after an operation."""
    mem_mb = df.memory_usage(deep=True).sum() / 1e6
    print(f"{operation_name}: {mem_mb:.2f} MB")

# Initial
track_memory(df, "Initial")

# After adding column
df['new_col'] = df['int_col'] * 2
track_memory(df, "After adding column")

# After type conversion
df['str_col'] = df['str_col'].astype('category')
track_memory(df, "After categorical conversion")
```

## Practical Example: Optimizing a DataFrame

```python
def optimize_dtypes(df, verbose=True):
    """Optimize DataFrame memory by downcasting types."""
    initial_mem = df.memory_usage(deep=True).sum()
    
    for col in df.columns:
        col_type = df[col].dtype
        
        # Optimize integers
        if col_type == 'int64':
            c_min, c_max = df[col].min(), df[col].max()
            if c_min >= -128 and c_max <= 127:
                df[col] = df[col].astype('int8')
            elif c_min >= -32768 and c_max <= 32767:
                df[col] = df[col].astype('int16')
            elif c_min >= -2147483648 and c_max <= 2147483647:
                df[col] = df[col].astype('int32')
        
        # Optimize floats
        elif col_type == 'float64':
            df[col] = df[col].astype('float32')
        
        # Convert low-cardinality strings to categorical
        elif col_type == 'object':
            n_unique = df[col].nunique()
            if n_unique / len(df) < 0.5:  # Less than 50% unique
                df[col] = df[col].astype('category')
    
    final_mem = df.memory_usage(deep=True).sum()
    
    if verbose:
        print(f"Memory: {initial_mem/1e6:.1f} MB → {final_mem/1e6:.1f} MB")
        print(f"Reduction: {(1 - final_mem/initial_mem)*100:.1f}%")
    
    return df

df_optimized = optimize_dtypes(df.copy())
```

## Summary

| Method | Purpose | Key Parameter |
|--------|---------|---------------|
| `memory_usage()` | Per-column memory | `deep=True` for accuracy |
| `info()` | Overall summary | `memory_usage='deep'` |

Best practices:
- Always use `deep=True` for object columns
- Monitor memory after each major transformation
- Optimize dtypes for large datasets
- Convert string columns to categorical when appropriate

---

## Exercises

**Exercise 1.**
Create a DataFrame with 100,000 rows containing an `int64` column, a `float64` column, and a `string` (object) column. Use `.memory_usage(deep=True)` to find the total memory. Compare it with `.memory_usage()` (without `deep=True`) to see the difference for object columns.

??? success "Solution to Exercise 1"
    Compare shallow vs deep memory measurement.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'ints': np.random.randint(0, 100, 100000),
            'floats': np.random.randn(100000),
            'strings': ['item_' + str(i % 10) for i in range(100000)]
        })
        shallow = df.memory_usage().sum()
        deep = df.memory_usage(deep=True).sum()
        print(f"Shallow: {shallow / 1e6:.2f} MB")
        print(f"Deep:    {deep / 1e6:.2f} MB")
        print(f"Difference: {(deep - shallow) / 1e6:.2f} MB")

---

**Exercise 2.**
Take a DataFrame with a string column that has low cardinality (few unique values). Convert it to `'category'` dtype using `.astype('category')`. Compare memory usage before and after the conversion using `.memory_usage(deep=True)`.

??? success "Solution to Exercise 2"
    Convert low-cardinality string column to categorical.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'status': np.random.choice(['active', 'inactive', 'pending'], 100000)
        })
        before = df.memory_usage(deep=True).sum()
        df['status'] = df['status'].astype('category')
        after = df.memory_usage(deep=True).sum()
        print(f"Before: {before / 1e6:.2f} MB")
        print(f"After:  {after / 1e6:.2f} MB")
        print(f"Reduction: {(1 - after / before) * 100:.1f}%")

---

**Exercise 3.**
Create a DataFrame with an `int64` column where all values fit in `int8` range (-128 to 127). Downcast it to `int8` using `.astype('int8')`. Measure the memory reduction and verify the values are unchanged.

??? success "Solution to Exercise 3"
    Downcast int64 to int8 and verify values.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({'values': np.random.randint(-128, 128, 100000).astype('int64')})
        before = df.memory_usage(deep=True).sum()
        original_values = df['values'].copy()
        df['values'] = df['values'].astype('int8')
        after = df.memory_usage(deep=True).sum()
        print(f"Before: {before / 1e6:.2f} MB")
        print(f"After:  {after / 1e6:.2f} MB")
        print(f"Reduction: {(1 - after / before) * 100:.1f}%")
        assert (df['values'] == original_values).all()
        print("Values unchanged after downcast: True")
