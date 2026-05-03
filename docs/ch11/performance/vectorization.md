# Vectorization

Vectorization is the practice of applying operations to entire arrays at once, rather than iterating through elements. Vectorized operations in pandas are typically 10-100x faster than loops.

!!! tip "Mental Model"
    A Python `for` loop processes one value per iteration with full interpreter overhead. A vectorized operation hands the entire array to a compiled C/Fortran routine that processes all values in a tight, optimized loop. The rule is simple: if you can express the operation without a Python loop, do so -- the speedup is typically 10-100x.

## Why Vectorization Matters

### The Problem with Loops

```python
import pandas as pd
import numpy as np
import time

df = pd.DataFrame({
    'A': np.random.randn(100000),
    'B': np.random.randn(100000)
})

# Slow: iterating with a loop
def slow_sum(df):
    result = []
    for i in range(len(df)):
        result.append(df.iloc[i]['A'] + df.iloc[i]['B'])
    return result

# Even slower: iterrows
def slower_sum(df):
    result = []
    for idx, row in df.iterrows():
        result.append(row['A'] + row['B'])
    return result
```

### The Vectorized Solution

```python
# Fast: vectorized operation
df['C'] = df['A'] + df['B']
```

## Performance Comparison

```python
n = 100000
df = pd.DataFrame({
    'A': np.random.randn(n),
    'B': np.random.randn(n)
})

# Method 1: iterrows (slowest)
start = time.time()
result = []
for idx, row in df.iterrows():
    result.append(row['A'] + row['B'])
iterrows_time = time.time() - start

# Method 2: apply (slow)
start = time.time()
result = df.apply(lambda row: row['A'] + row['B'], axis=1)
apply_time = time.time() - start

# Method 3: vectorized (fast)
start = time.time()
result = df['A'] + df['B']
vector_time = time.time() - start

print(f"iterrows: {iterrows_time:.3f}s")
print(f"apply:    {apply_time:.3f}s")
print(f"vectorized: {vector_time:.6f}s")
```

Typical results:
```
iterrows: 4.521s
apply:    1.234s
vectorized: 0.001s
```

## Common Vectorized Operations

### Arithmetic

```python
# Element-wise operations
df['sum'] = df['A'] + df['B']
df['diff'] = df['A'] - df['B']
df['product'] = df['A'] * df['B']
df['ratio'] = df['A'] / df['B']
df['power'] = df['A'] ** 2
```

### Comparisons

```python
# Returns boolean Series
mask = df['A'] > 0
mask = df['A'] >= df['B']
mask = (df['A'] > 0) & (df['B'] < 0)
mask = (df['A'] > 0) | (df['B'] > 0)
```

### String Operations (with .str accessor)

```python
df = pd.DataFrame({'text': ['hello', 'world', 'python']})

# Vectorized string operations
df['upper'] = df['text'].str.upper()
df['length'] = df['text'].str.len()
df['contains_o'] = df['text'].str.contains('o')
```

### Datetime Operations (with .dt accessor)

```python
df = pd.DataFrame({'date': pd.date_range('2024-01-01', periods=100)})

# Vectorized datetime operations
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.dayofweek
```

## Replacing Loops with Vectorization

### Conditional Assignment

```python
# Instead of:
for i in range(len(df)):
    if df.loc[i, 'A'] > 0:
        df.loc[i, 'result'] = 'positive'
    else:
        df.loc[i, 'result'] = 'negative'

# Use:
df['result'] = np.where(df['A'] > 0, 'positive', 'negative')
```

### Multiple Conditions

```python
# Instead of complex if-elif-else in loop:
conditions = [
    df['A'] > 1,
    df['A'] > 0,
    df['A'] > -1
]
choices = ['high', 'medium', 'low']
df['category'] = np.select(conditions, choices, default='very_low')
```

### Cumulative Operations

```python
# Instead of loop with running total:
df['cumsum'] = df['A'].cumsum()
df['cumprod'] = df['A'].cumprod()
df['cummax'] = df['A'].cummax()
df['cummin'] = df['A'].cummin()
```

### Shifting and Differencing

```python
# Instead of loop comparing to previous row:
df['prev_A'] = df['A'].shift(1)
df['change'] = df['A'].diff()
df['pct_change'] = df['A'].pct_change()
```

### Rolling Operations

```python
# Instead of loop calculating moving average:
df['rolling_mean'] = df['A'].rolling(window=5).mean()
df['rolling_std'] = df['A'].rolling(window=5).std()
df['rolling_sum'] = df['A'].rolling(window=5).sum()
```

## When apply() Is Acceptable

Sometimes `apply()` is necessary, but optimize the function:

```python
# Slow: complex logic in apply
def complex_calculation(row):
    if row['A'] > 0 and row['B'] > 0:
        return row['A'] * row['B']
    elif row['A'] < 0 and row['B'] < 0:
        return -row['A'] * row['B']
    else:
        return 0

# Faster: vectorize the logic
mask1 = (df['A'] > 0) & (df['B'] > 0)
mask2 = (df['A'] < 0) & (df['B'] < 0)

df['result'] = 0  # default
df.loc[mask1, 'result'] = df.loc[mask1, 'A'] * df.loc[mask1, 'B']
df.loc[mask2, 'result'] = -df.loc[mask2, 'A'] * df.loc[mask2, 'B']
```

## Using NumPy Functions

NumPy functions work directly on pandas objects:

```python
# Math functions
df['abs_A'] = np.abs(df['A'])
df['sqrt_abs'] = np.sqrt(np.abs(df['A']))
df['log_abs'] = np.log(np.abs(df['A']) + 1)
df['exp_A'] = np.exp(df['A'])

# Trigonometric
df['sin_A'] = np.sin(df['A'])
df['cos_A'] = np.cos(df['A'])

# Rounding
df['floor'] = np.floor(df['A'])
df['ceil'] = np.ceil(df['A'])
df['round'] = np.round(df['A'], 2)
```

## Practical Example: Financial Calculations

```python
# Stock price data
np.random.seed(42)
prices = pd.DataFrame({
    'close': 100 + np.cumsum(np.random.randn(10000) * 0.5)
})

# All vectorized calculations
prices['return'] = prices['close'].pct_change()
prices['log_return'] = np.log(prices['close'] / prices['close'].shift(1))
prices['sma_20'] = prices['close'].rolling(20).mean()
prices['sma_50'] = prices['close'].rolling(50).mean()
prices['std_20'] = prices['return'].rolling(20).std()
prices['upper_band'] = prices['sma_20'] + 2 * prices['std_20'] * prices['close']
prices['lower_band'] = prices['sma_20'] - 2 * prices['std_20'] * prices['close']
prices['signal'] = np.where(prices['sma_20'] > prices['sma_50'], 1, -1)
```

## Performance Tips

### 1. Avoid iterrows()

```python
# Never do this for large DataFrames
for idx, row in df.iterrows():
    # process row
    pass
```

### 2. Minimize apply()

```python
# Try to replace apply with vectorized operations
# Bad
df['result'] = df.apply(lambda x: x['A'] + x['B'], axis=1)

# Good
df['result'] = df['A'] + df['B']
```

### 3. Use eval() for Complex Expressions

```python
# For complex arithmetic on large DataFrames
df.eval('result = (A + B) * (C - D) / E', inplace=True)
```

### 4. Batch Operations

```python
# Instead of multiple separate operations
df['A'] = df['A'] * 2
df['B'] = df['B'] + 1
df['C'] = df['A'] + df['B']

# Consider eval for batch
df.eval('''
    A = A * 2
    B = B + 1
    C = A + B
''', inplace=True)
```

## Summary

| Method | Speed | Use Case |
|--------|-------|----------|
| Vectorized ops | ⚡ Fastest | Arithmetic, comparisons |
| NumPy functions | ⚡ Fast | Math operations |
| eval() | ⚡ Fast | Complex expressions |
| apply(axis=0) | 🔶 Moderate | Column-wise operations |
| apply(axis=1) | 🔴 Slow | Row-wise operations |
| iterrows() | 🔴 Slowest | Avoid if possible |

**Rule of thumb**: If you're writing a loop over DataFrame rows, there's almost always a vectorized alternative.

---

## Runnable Example: `performance_tutorial.py`

```python
"""
Pandas Tutorial: Performance Optimization.

Covers techniques for faster data processing.
"""

import pandas as pd
import numpy as np
import time

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("="*70)
    print("PERFORMANCE OPTIMIZATION")
    print("="*70)

    # Create large dataset
    n = 100000
    np.random.seed(42)
    df = pd.DataFrame({
        'A': np.random.randint(0, 100, n),
        'B': np.random.randint(0, 100, n),
        'C': np.random.choice(['X', 'Y', 'Z'], n),
        'D': np.random.random(n)
    })

    print(f"\nDataFrame with {len(df):,} rows")
    print(df.head())

    # 1. Vectorized operations vs loops
    print("\n1. Vectorized operations vs loops:")

    # Loop (slow)
    start = time.time()
    result_loop = []
    for val in df['A']:
        result_loop.append(val * 2)
    loop_time = time.time() - start

    # Vectorized (fast)
    start = time.time()
    result_vec = df['A'] * 2
    vec_time = time.time() - start

    print(f"Loop time: {loop_time:.4f}s")
    print(f"Vectorized time: {vec_time:.4f}s")
    print(f"Speedup: {loop_time/vec_time:.2f}x")

    # 2. Use categorical for repeated strings
    print("\n2. Memory optimization with categorical:")
    print(f"Original memory: {df['C'].memory_usage(deep=True):,} bytes")
    df['C_cat'] = df['C'].astype('category')
    print(f"Categorical memory: {df['C_cat'].memory_usage(deep=True):,} bytes")

    # 3. Query method (faster than boolean indexing for large datasets)
    print("\n3. Query method:")
    start = time.time()
    result1 = df[(df['A'] > 50) & (df['B'] < 30)]
    bool_time = time.time() - start

    start = time.time()
    result2 = df.query('A > 50 and B < 30')
    query_time = time.time() - start

    print(f"Boolean indexing: {bool_time:.4f}s")
    print(f"Query method: {query_time:.4f}s")

    # 4. Use appropriate dtypes
    print("\n4. Optimize data types:")
    df_types = pd.DataFrame({
        'int_col': [1, 2, 3, 4, 5] * 20000,
        'float_col': [1.5, 2.5, 3.5] * 33334
    })

    print("\nBefore optimization:")
    print(df_types.dtypes)
    print(f"Memory: {df_types.memory_usage(deep=True).sum():,} bytes")

    # Downcast to smaller types
    df_types['int_col'] = pd.to_numeric(df_types['int_col'], downcast='integer')
    df_types['float_col'] = pd.to_numeric(df_types['float_col'], downcast='float')

    print("\nAfter optimization:")
    print(df_types.dtypes)
    print(f"Memory: {df_types.memory_usage(deep=True).sum():,} bytes")

    # 5. Avoid chained indexing
    print("\n5. Avoid chained indexing:")
    print("❌ Bad: df[df['A'] > 50]['B'] = 100  (chained)")
    print("✅ Good: df.loc[df['A'] > 50, 'B'] = 100")

    # 6. Use inplace when appropriate (though not always faster)
    print("\n6. Inplace operations:")
    df_temp = df.copy()
    start = time.time()
    df_temp = df_temp.drop(columns=['D'])
    drop_time = time.time() - start

    df_temp2 = df.copy()
    start = time.time()
    df_temp2.drop(columns=['D'], inplace=True)
    inplace_time = time.time() - start

    print(f"Regular drop: {drop_time:.4f}s")
    print(f"Inplace drop: {inplace_time:.4f}s")

    print("\nKEY TAKEAWAYS:")
    print("1. Use vectorized operations instead of loops")
    print("2. Convert repeated strings to categorical")
    print("3. Use query() for complex boolean indexing")
    print("4. Optimize data types (downcast integers/floats)")
    print("5. Avoid chained indexing - use loc/iloc")
    print("6. Consider chunking for very large files")
    print("7. Use eval() for complex expressions")
    print("8. Avoid apply() when vectorization is possible")
```


---

## Exercises

**Exercise 1.** Write code that computes a new column using vectorized operations (e.g., `df['c'] = df['a'] + df['b']`) and compare the timing with a for-loop approach using `%%timeit` or `time`.

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

**Exercise 2.** Explain why vectorized operations are faster than iterating with `iterrows()` in Pandas.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that replaces a `for` loop that applies a conditional transformation with a vectorized `np.where()` call.

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

**Exercise 4.** Demonstrate the performance difference between `df.apply(func)` and a vectorized alternative for a simple mathematical operation.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
