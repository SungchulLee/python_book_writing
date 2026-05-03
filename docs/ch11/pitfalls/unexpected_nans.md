# Unexpected NaNs

NaN (Not a Number) values can appear unexpectedly in pandas operations. Understanding the common causes helps prevent and debug data quality issues.

!!! tip "Mental Model"
    NaN is pandas' way of saying "I do not have a value here." It appears in three main situations: outer joins with missing keys, arithmetic between misaligned indices, and type coercion of non-numeric strings. Whenever NaN appears unexpectedly, check these three sources first -- the root cause is almost always an alignment or key-matching issue.

## Common Sources of Unexpected NaN

### 1. Merge/Join with Missing Keys

```python
import pandas as pd

df1 = pd.DataFrame({
    'key': ['A', 'B', 'C'],
    'value1': [1, 2, 3]
})

df2 = pd.DataFrame({
    'key': ['B', 'C', 'D'],
    'value2': [4, 5, 6]
})

# Outer merge introduces NaN for non-matching keys
result = pd.merge(df1, df2, on='key', how='outer')
print(result)
```

```
  key  value1  value2
0   A     1.0     NaN    # A only in df1
1   B     2.0     4.0
2   C     3.0     5.0
3   D     NaN     6.0    # D only in df2
```

### 2. Left/Right Join Missing Matches

```python
# Left join: NaN when right table has no match
result = pd.merge(df1, df2, on='key', how='left')
print(result)
```

```
  key  value1  value2
0   A       1     NaN    # No match for A in df2
1   B       2     4.0
2   C       3     5.0
```

### 3. Index Misalignment in Operations

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([4, 5, 6], index=['b', 'c', 'd'])

print(s1 + s2)
```

```
a    NaN    # 'a' only in s1
b    6.0
c    8.0
d    NaN    # 'd' only in s2
dtype: float64
```

### 4. Reindex with New Labels

```python
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s_reindexed = s.reindex(['a', 'b', 'c', 'd', 'e'])
print(s_reindexed)
```

```
a    1.0
b    2.0
c    3.0
d    NaN    # New label, no value
e    NaN    # New label, no value
dtype: float64
```

### 5. Division by Zero

```python
df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 0, 1]})
df['ratio'] = df['a'] / df['b']
print(df)
```

```
   a  b  ratio
0  1  1    1.0
1  2  0    inf    # or NaN in some cases
2  3  1    3.0
```

### 6. GroupBy with Missing Groups

```python
df = pd.DataFrame({
    'group': pd.Categorical(['A', 'B', 'A'], categories=['A', 'B', 'C']),
    'value': [1, 2, 3]
})

# GroupBy includes all categories
print(df.groupby('group', observed=False)['value'].sum())
```

```
group
A    4
B    2
C    0    # or NaN depending on operation
Name: value, dtype: int64
```

### 7. shift() Creates NaN

```python
s = pd.Series([1, 2, 3, 4, 5])
print(s.shift(1))
```

```
0    NaN    # First value becomes NaN
1    1.0
2    2.0
3    3.0
4    4.0
dtype: float64
```

### 8. pct_change() First Value

```python
s = pd.Series([100, 102, 101, 105])
print(s.pct_change())
```

```
0         NaN    # No previous value to compare
1    0.020000
2   -0.009804
3    0.039604
dtype: float64
```

### 9. Rolling Window Not Full

```python
s = pd.Series([1, 2, 3, 4, 5])
print(s.rolling(3).mean())
```

```
0    NaN    # Window not full
1    NaN    # Window not full
2    2.0
3    3.0
4    4.0
dtype: float64
```

## Detecting Unexpected NaN

### After Merge/Join

```python
# Always check for NaN after merge
result = pd.merge(df1, df2, on='key', how='outer')

# Count NaN per column
nan_counts = result.isnull().sum()
print("NaN counts after merge:")
print(nan_counts)

# Rows with any NaN
rows_with_nan = result[result.isnull().any(axis=1)]
print(f"\nRows with NaN: {len(rows_with_nan)}")
```

### After Arithmetic Operations

```python
# Check for NaN introduction
before_nan = df.isnull().sum().sum()
result = df['a'] / df['b']
after_nan = result.isnull().sum()

if after_nan > before_nan:
    print(f"Warning: {after_nan - before_nan} new NaN values!")
```

## Solutions

### 1. Use indicator in Merge

```python
result = pd.merge(df1, df2, on='key', how='outer', indicator=True)
print(result)
```

```
  key  value1  value2      _merge
0   A     1.0     NaN   left_only
1   B     2.0     4.0        both
2   C     3.0     5.0        both
3   D     NaN     6.0  right_only
```

### 2. Fill NaN with Default Value

```python
# During merge
result = pd.merge(df1, df2, on='key', how='outer').fillna(0)

# During reindex
s_reindexed = s.reindex(['a', 'b', 'c', 'd'], fill_value=0)
```

### 3. Use min_periods for Rolling

```python
s = pd.Series([1, 2, 3, 4, 5])
print(s.rolling(3, min_periods=1).mean())
```

```
0    1.0    # Only 1 value available
1    1.5    # 2 values available
2    2.0    # Full window
3    3.0
4    4.0
dtype: float64
```

### 4. Fill shift/pct_change NaN

```python
s = pd.Series([1, 2, 3, 4, 5])

# Forward fill first value
s_shifted = s.shift(1).fillna(method='bfill')

# Or use fill_value parameter
s_shifted = s.shift(1, fill_value=s.iloc[0])
```

### 5. Handle Division by Zero

```python
df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 0, 1]})

# Replace 0 before division
df['ratio'] = df['a'] / df['b'].replace(0, np.nan)

# Or use np.where
import numpy as np
df['ratio'] = np.where(df['b'] != 0, df['a'] / df['b'], 0)
```

## Validation Pattern

```python
def validate_no_new_nan(df_before, df_after, operation_name):
    """Check that operation didn't introduce unexpected NaN."""
    nan_before = df_before.isnull().sum().sum()
    nan_after = df_after.isnull().sum().sum()
    
    if nan_after > nan_before:
        new_nan = nan_after - nan_before
        print(f"Warning: {operation_name} introduced {new_nan} NaN values")
        
        # Show which columns
        for col in df_after.columns:
            before = df_before[col].isnull().sum() if col in df_before else 0
            after = df_after[col].isnull().sum()
            if after > before:
                print(f"  - {col}: {after - before} new NaN")
        
        return False
    return True

# Usage
result = pd.merge(df1, df2, on='key', how='outer')
validate_no_new_nan(df1, result, "merge")
```

## Summary

| Source | Solution |
|--------|----------|
| Merge mismatch | Use `indicator=True`, check after merge |
| Index mismatch | `reindex` with `fill_value` |
| Division by zero | Replace zeros or use `np.where` |
| Rolling window | Use `min_periods=1` |
| shift/pct_change | Fill or handle first values |
| Reindex new labels | Provide `fill_value` |


---

## Exercises

**Exercise 1.** Create two Series with mismatched indices and perform arithmetic. Explain why NaN values appear in the result.

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

**Exercise 2.** Write code that demonstrates how `merge()` with `how='left'` can introduce NaN values. How do you handle them?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Explain three common sources of unexpected NaN values in Pandas operations.

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

**Exercise 4.** Write code that uses `fillna()` and `dropna()` to handle NaN values introduced by index misalignment.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
