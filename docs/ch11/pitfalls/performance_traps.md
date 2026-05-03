# Performance Traps

pandas is built for **vectorized operations**. Using Python loops or incorrect patterns can make code orders of magnitude slower.

!!! tip "Mental Model"
    The performance hierarchy is: vectorized ops > `apply()` > `itertuples()` > `iterrows()` > Python loops. Every time you write a loop over DataFrame rows, ask "can I express this as a column operation instead?" Other common traps include growing a DataFrame row-by-row (use a list of dicts then construct once) and calling `.apply()` when a built-in method exists.

## The Golden Rule

**Vectorized operations > apply() > itertuples() > iterrows() > for loops**

## Trap 1: Row-by-Row Iteration

### The Problem

```python
import pandas as pd
import numpy as np
import time

# Create test data
n = 100_000
df = pd.DataFrame({
    'A': np.random.randn(n),
    'B': np.random.randn(n)
})

# SLOW: Using iterrows
def slow_sum():
    result = []
    for idx, row in df.iterrows():
        result.append(row['A'] + row['B'])
    return pd.Series(result)

start = time.time()
slow_result = slow_sum()
print(f"iterrows: {time.time() - start:.2f}s")
```

### The Solution: Vectorize

```python
# FAST: Vectorized
start = time.time()
fast_result = df['A'] + df['B']
print(f"Vectorized: {time.time() - start:.4f}s")
```

**Speedup: 100-1000x faster**

## Trap 2: Growing DataFrames in a Loop

### The Problem

```python
# SLOW: Appending in a loop
df = pd.DataFrame(columns=['A', 'B'])

for i in range(10000):
    df = pd.concat([df, pd.DataFrame({'A': [i], 'B': [i*2]})])
    # Each concat creates a new DataFrame!
```

### The Solution: Build List, Then DataFrame

```python
# FAST: Collect data, then create DataFrame
data = []
for i in range(10000):
    data.append({'A': i, 'B': i*2})

df = pd.DataFrame(data)
```

**Speedup: 100x+ faster**

## Trap 3: Using apply() When Vectorized Option Exists

### The Problem

```python
# SLOW: Using apply
df['C'] = df['A'].apply(lambda x: x ** 2)

# SLOW: Row-wise apply
df['D'] = df.apply(lambda row: row['A'] + row['B'], axis=1)
```

### The Solution: Use Built-in Vectorized Operations

```python
# FAST: Vectorized
df['C'] = df['A'] ** 2

# FAST: Vectorized
df['D'] = df['A'] + df['B']
```

**Speedup: 10-100x faster**

## Trap 4: String Operations in Loops

### The Problem

```python
df = pd.DataFrame({'text': ['hello', 'world', 'python'] * 10000})

# SLOW: Loop
result = []
for text in df['text']:
    result.append(text.upper())
df['upper'] = result
```

### The Solution: Use str Accessor

```python
# FAST: Vectorized string operation
df['upper'] = df['text'].str.upper()
```

## Trap 5: Conditional Assignment in Loops

### The Problem

```python
df = pd.DataFrame({'value': np.random.randn(100000)})

# SLOW: Loop with condition
for idx in df.index:
    if df.loc[idx, 'value'] > 0:
        df.loc[idx, 'category'] = 'positive'
    else:
        df.loc[idx, 'category'] = 'negative'
```

### The Solution: Vectorized Conditional

```python
# FAST: np.where
df['category'] = np.where(df['value'] > 0, 'positive', 'negative')

# FAST: .loc with boolean indexing
df.loc[df['value'] > 0, 'category'] = 'positive'
df.loc[df['value'] <= 0, 'category'] = 'negative'
```

## Trap 6: Using Object Dtype for Numbers

### The Problem

```python
# Accidental object dtype
df = pd.DataFrame({'values': ['1', '2', '3', '4', '5']})
print(df['values'].dtype)  # object

# Operations on object dtype are slow
df['values'].astype(float).sum()  # Conversion on every operation
```

### The Solution: Use Correct Dtypes

```python
# Convert once, use many times
df['values'] = pd.to_numeric(df['values'])
print(df['values'].dtype)  # int64 or float64

# Operations are now fast
df['values'].sum()
```

## Trap 7: Inefficient GroupBy

### The Problem

```python
# SLOW: Multiple separate groupby calls
mean_by_group = df.groupby('group')['value'].mean()
std_by_group = df.groupby('group')['value'].std()
count_by_group = df.groupby('group')['value'].count()
```

### The Solution: Single GroupBy with agg

```python
# FAST: Single groupby with multiple aggregations
stats = df.groupby('group')['value'].agg(['mean', 'std', 'count'])
```

## Trap 8: Large DataFrame Copies

### The Problem

```python
# SLOW: Unnecessary copies
df_copy = df.copy()
df_copy['new_col'] = df_copy['A'] * 2
# Then only use df_copy briefly
```

### The Solution: Modify In-Place or Use Views

```python
# Option 1: Modify original if appropriate
df['new_col'] = df['A'] * 2

# Option 2: Use assign for method chaining (creates copy only when needed)
result = df.assign(new_col=lambda x: x['A'] * 2)
```

## Trap 9: Using Python max/min/sum

### The Problem

```python
# SLOW: Python built-ins
result = sum(df['A'])  # Python sum, iterates one by one
result = max(df['A'])  # Python max
```

### The Solution: Use pandas/NumPy Methods

```python
# FAST: pandas methods
result = df['A'].sum()  # Vectorized
result = df['A'].max()  # Vectorized
```

## Benchmarking Your Code

```python
import time

def benchmark(func, name, n_runs=3):
    """Simple benchmarking function."""
    times = []
    for _ in range(n_runs):
        start = time.time()
        func()
        times.append(time.time() - start)
    avg_time = sum(times) / n_runs
    print(f"{name}: {avg_time:.4f}s (avg of {n_runs} runs)")
    return avg_time

# Compare approaches
df = pd.DataFrame({'A': np.random.randn(100000)})

benchmark(lambda: df['A'].apply(lambda x: x**2), "apply")
benchmark(lambda: df['A'] ** 2, "vectorized")
```

## When apply() is Acceptable

Sometimes `apply()` is necessary:

```python
# Complex logic that can't be vectorized
def complex_business_logic(row):
    if row['status'] == 'A' and row['value'] > 100:
        return row['value'] * 1.1
    elif row['status'] == 'B':
        return row['value'] * 0.9
    else:
        return row['value']

# This is acceptable (but try to vectorize if possible)
df['adjusted'] = df.apply(complex_business_logic, axis=1)
```

**Better alternative with np.select:**

```python
conditions = [
    (df['status'] == 'A') & (df['value'] > 100),
    df['status'] == 'B'
]
choices = [
    df['value'] * 1.1,
    df['value'] * 0.9
]
df['adjusted'] = np.select(conditions, choices, default=df['value'])
```

## Summary: Performance Hierarchy

| Approach | Relative Speed | Use When |
|----------|---------------|----------|
| Vectorized (NumPy/pandas) | 1x (baseline) | Always prefer |
| Boolean indexing | ~1x | Conditional assignment |
| str/dt accessor | ~2-5x slower | String/datetime ops |
| apply() on column | ~10-100x slower | Last resort for complex logic |
| apply() on rows (axis=1) | ~100-500x slower | Very last resort |
| itertuples() | ~50-200x slower | Need row access, can't vectorize |
| iterrows() | ~500-2000x slower | Avoid |
| Python for loop | ~1000-5000x slower | Never for data ops |


---

## Exercises

**Exercise 1.** Explain why growing a DataFrame row-by-row in a loop with `pd.concat()` inside the loop is slow. What is the correct alternative?

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

**Exercise 2.** Write code showing the performance difference between `iterrows()` and vectorized operations for computing a column.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Explain why `apply()` with a Python function is slower than using built-in Pandas/NumPy vectorized methods.

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

**Exercise 4.** Write code that collects results in a list and creates a DataFrame at the end, instead of appending to a DataFrame in a loop.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
