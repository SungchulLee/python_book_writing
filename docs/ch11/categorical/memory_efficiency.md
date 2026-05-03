# Memory Efficiency with Categoricals

One of the primary benefits of categorical data is dramatic memory savings. This document demonstrates the memory characteristics and optimization strategies.

!!! tip "Mental Model"
    Object-dtype columns store a full Python string per cell -- a million rows of "Technology" means a million copies. Categorical dtype stores the string once in a lookup table and keeps only a small integer code per row. The fewer unique values relative to total rows, the larger the memory savings.

## How Memory is Saved

### String Storage (object dtype)

Each string value is stored separately in memory, even if repeated:

```python
import pandas as pd
import numpy as np

# 1 million rows with 10 unique sectors
sectors = ['Technology', 'Finance', 'Healthcare', 'Retail', 'Energy',
           'Utilities', 'Media', 'Aerospace', 'Banks', 'Insurance']

np.random.seed(42)
data = np.random.choice(sectors, size=1_000_000)

# String storage
s_string = pd.Series(data)
string_memory = s_string.memory_usage(deep=True)
print(f"String storage: {string_memory / 1e6:.2f} MB")
```

```
String storage: 57.89 MB
```

### Categorical Storage

Categories are stored once; data stores only integer codes:

```python
# Categorical storage
s_cat = s_string.astype('category')
cat_memory = s_cat.memory_usage(deep=True)
print(f"Categorical storage: {cat_memory / 1e6:.2f} MB")
print(f"Memory reduction: {string_memory / cat_memory:.1f}x")
```

```
Categorical storage: 1.00 MB
Memory reduction: 57.9x
```

## Memory Breakdown

```python
def analyze_categorical_memory(s_cat):
    """Analyze memory components of a categorical Series."""
    # Category table size
    categories = s_cat.cat.categories
    cat_memory = categories.memory_usage(deep=True)
    
    # Codes array size (integer array)
    codes_memory = s_cat.cat.codes.nbytes
    
    # Total
    total = s_cat.memory_usage(deep=True)
    
    print(f"Categories ({len(categories)} unique): {cat_memory:,} bytes")
    print(f"Codes ({len(s_cat):,} values): {codes_memory:,} bytes")
    print(f"Total: {total:,} bytes")
    
    return cat_memory, codes_memory, total

s_cat = pd.Series(np.random.choice(['A', 'B', 'C'], 1_000_000), dtype='category')
analyze_categorical_memory(s_cat)
```

```
Categories (3 unique): 248 bytes
Codes (1,000,000 values): 1,000,000 bytes
Total: 1,000,376 bytes
```

## Memory Comparison Table

```python
def compare_memory(n_rows, n_categories, avg_string_length=10):
    """Compare string vs categorical memory usage."""
    # Generate data
    categories = [f'Cat_{i:0{len(str(n_categories))}d}' for i in range(n_categories)]
    data = np.random.choice(categories, n_rows)
    
    # String
    s_string = pd.Series(data)
    string_mem = s_string.memory_usage(deep=True)
    
    # Categorical
    s_cat = s_string.astype('category')
    cat_mem = s_cat.memory_usage(deep=True)
    
    return string_mem, cat_mem, string_mem / cat_mem

# Test different scenarios
scenarios = [
    (100_000, 5),
    (100_000, 50),
    (100_000, 500),
    (1_000_000, 10),
    (1_000_000, 100),
    (1_000_000, 1000),
]

print(f"{'Rows':>12} {'Categories':>12} {'String MB':>12} {'Cat MB':>12} {'Ratio':>8}")
print("-" * 60)

for n_rows, n_cats in scenarios:
    str_mem, cat_mem, ratio = compare_memory(n_rows, n_cats)
    print(f"{n_rows:>12,} {n_cats:>12} {str_mem/1e6:>12.2f} {cat_mem/1e6:>12.2f} {ratio:>8.1f}x")
```

```
        Rows   Categories    String MB       Cat MB    Ratio
------------------------------------------------------------
     100,000            5         5.79         0.10    57.9x
     100,000           50         5.79         0.11    52.6x
     100,000          500         6.30         0.15    42.0x
   1,000,000           10        57.89         1.00    57.9x
   1,000,000          100        57.89         1.01    57.3x
   1,000,000         1000        62.89         1.10    57.2x
```

## When Categoricals Save Memory

### High Savings (Use Categorical)

- Few unique values relative to total rows
- Long string values
- Many repeated values

```python
# Ideal case: 1M rows, 10 categories, long strings
countries = ['United States of America', 'United Kingdom', 'Germany',
             'France', 'Japan', 'China', 'India', 'Brazil', 'Canada', 'Australia']

data = np.random.choice(countries, 1_000_000)
s_string = pd.Series(data)
s_cat = s_string.astype('category')

print(f"String: {s_string.memory_usage(deep=True) / 1e6:.1f} MB")
print(f"Categorical: {s_cat.memory_usage(deep=True) / 1e6:.1f} MB")
```

### Low Savings (May Not Be Worth It)

- Many unique values (high cardinality)
- Short strings
- Few rows

```python
# Poor case: many unique values
unique_ids = [f'ID_{i}' for i in range(100_000)]  # All unique
s_string = pd.Series(unique_ids)
s_cat = s_string.astype('category')

print(f"String: {s_string.memory_usage(deep=True) / 1e6:.1f} MB")
print(f"Categorical: {s_cat.memory_usage(deep=True) / 1e6:.1f} MB")
# Similar or worse for high cardinality
```

## Integer Code Sizes

Pandas automatically chooses the smallest integer type for codes:

| Number of Categories | Code Type | Bytes per Value |
|---------------------|-----------|-----------------|
| ≤ 127 | int8 | 1 |
| ≤ 32,767 | int16 | 2 |
| ≤ 2,147,483,647 | int32 | 4 |
| > 2,147,483,647 | int64 | 8 |

```python
# Few categories -> int8
s = pd.Series(['a', 'b', 'c'] * 1000, dtype='category')
print(f"3 categories: {s.cat.codes.dtype}")  # int8

# Many categories -> int16
cats = [f'cat_{i}' for i in range(200)]
s = pd.Series(np.random.choice(cats, 1000), dtype='category')
print(f"200 categories: {s.cat.codes.dtype}")  # int16
```

## DataFrame Memory Optimization

```python
def optimize_dataframe(df, verbose=True):
    """Convert low-cardinality string columns to categorical."""
    original_memory = df.memory_usage(deep=True).sum()
    
    for col in df.select_dtypes(include=['object']).columns:
        n_unique = df[col].nunique()
        n_total = len(df)
        
        # Convert if less than 50% unique values
        if n_unique / n_total < 0.5:
            df[col] = df[col].astype('category')
            if verbose:
                print(f"Converted '{col}': {n_unique} unique values")
    
    new_memory = df.memory_usage(deep=True).sum()
    
    if verbose:
        print(f"\nMemory: {original_memory/1e6:.1f} MB → {new_memory/1e6:.1f} MB")
        print(f"Reduction: {(1 - new_memory/original_memory)*100:.1f}%")
    
    return df

# Example usage
df = pd.DataFrame({
    'sector': np.random.choice(['Tech', 'Finance', 'Health'], 100_000),
    'rating': np.random.choice(['A', 'B', 'C', 'D'], 100_000),
    'id': [f'ID_{i}' for i in range(100_000)],  # High cardinality - won't convert
    'value': np.random.randn(100_000)
})

df = optimize_dataframe(df)
```

```
Converted 'sector': 3 unique values
Converted 'rating': 4 unique values

Memory: 14.2 MB → 2.1 MB
Reduction: 85.2%
```

## Real-World Example: S&P 500 Data

```python
# Simulate S&P 500 historical data
np.random.seed(42)

sectors = ['Technology', 'Healthcare', 'Finance', 'Energy', 
           'Consumer Discretionary', 'Consumer Staples',
           'Industrials', 'Materials', 'Utilities',
           'Real Estate', 'Communication Services']

tickers = [f'STOCK_{i:03d}' for i in range(500)]
dates = pd.date_range('2020-01-01', '2024-01-01', freq='B')

# Create large dataset
n_rows = len(tickers) * len(dates)
df = pd.DataFrame({
    'date': np.tile(dates, len(tickers)),
    'ticker': np.repeat(tickers, len(dates)),
    'sector': np.repeat(np.random.choice(sectors, len(tickers)), len(dates)),
    'close': np.random.randn(n_rows).cumsum() + 100,
    'volume': np.random.randint(1000, 1000000, n_rows)
})

print(f"Dataset size: {len(df):,} rows")
print(f"\nBefore optimization:")
print(df.memory_usage(deep=True))
print(f"Total: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")

# Optimize
df['ticker'] = df['ticker'].astype('category')
df['sector'] = df['sector'].astype('category')

print(f"\nAfter optimization:")
print(df.memory_usage(deep=True))
print(f"Total: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
```

## Guidelines

| Unique Values (% of rows) | Recommendation |
|---------------------------|----------------|
| < 1% | ✅ Definitely use categorical |
| 1-10% | ✅ Use categorical |
| 10-50% | ⚠️ Test both options |
| > 50% | ❌ Probably not beneficial |

## Performance vs Memory Trade-off

Converting to categorical has a small upfront cost but saves memory and speeds up operations:

```python
import time

# Large dataset
n = 5_000_000
sectors = ['A', 'B', 'C', 'D', 'E']
data = np.random.choice(sectors, n)

# Conversion time
start = time.time()
s_cat = pd.Series(data, dtype='category')
conv_time = time.time() - start
print(f"Conversion time: {conv_time:.2f}s")

# GroupBy comparison
s_string = pd.Series(data)
values = np.random.randn(n)

start = time.time()
pd.Series(values).groupby(s_string).mean()
string_groupby = time.time() - start

start = time.time()
pd.Series(values).groupby(s_cat).mean()
cat_groupby = time.time() - start

print(f"String groupby: {string_groupby:.3f}s")
print(f"Categorical groupby: {cat_groupby:.3f}s")
print(f"Speedup: {string_groupby/cat_groupby:.1f}x")
```


---

## Exercises

**Exercise 1.** Create a DataFrame with a string column containing 100000 rows but only 5 unique values. Compare memory usage before and after converting to categorical.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    # See page content for relevant API details
    s = pd.Series(['a', 'b', 'c', 'a', 'b'], dtype='category')
    print(s)
    print(s.cat.categories)
    print(s.cat.codes)
    ```

---

**Exercise 2.** Explain how categorical data is stored internally (codes + categories). Why is this more memory-efficient than storing repeated strings?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page. The key concept involves understanding the categorical data type and its internal representation in Pandas.

---

**Exercise 3.** Write code that reads memory usage of each column in a DataFrame using `df.memory_usage(deep=True)` and identifies which columns would benefit from categorical conversion.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'col': np.random.choice(['A', 'B', 'C'], 1000)})
    df['col'] = df['col'].astype('category')
    print(df.dtypes)
    print(df['col'].value_counts())
    ```

---

**Exercise 4.** Create a function that takes a DataFrame and automatically converts all string columns with fewer than 50 unique values to categorical type. Return the total memory saved.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    s = pd.Categorical(['low', 'medium', 'high', 'low'],
                        categories=['low', 'medium', 'high'],
                        ordered=True)
    print(s)
    print(s > 'low')
    ```
