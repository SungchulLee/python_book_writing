# Index Misalignment

pandas aligns operations by **index labels**, not by position. This powerful feature can also cause subtle bugs when indices don't match as expected.

!!! tip "Mental Model"
    Pandas always aligns by label before operating. If two Series have different index labels, unmatched labels produce NaN -- even if both Series have the same length. This is a feature, not a bug: it prevents accidental position-based mismatches. Use `.reset_index(drop=True)` or `.values` when you intentionally want position-based alignment.

## The Alignment Behavior

```python
import pandas as pd

s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([4, 5, 6], index=['b', 'c', 'a'])

print("s1:")
print(s1)
print("\ns2:")
print(s2)
print("\ns1 + s2:")
print(s1 + s2)
```

```
s1:
a    1
b    2
c    3

s2:
b    4
c    5
a    6

s1 + s2:
a    7    # 1 + 6 (matched by label 'a')
b    6    # 2 + 4 (matched by label 'b')
c    8    # 3 + 5 (matched by label 'c')
dtype: int64
```

**pandas matched by index labels, not positions!**

## When Alignment Causes Problems

### Problem 1: Unexpected Order

```python
# You expect position-based addition
returns_1 = pd.Series([0.01, 0.02, 0.03], index=[0, 1, 2])
returns_2 = pd.Series([0.04, 0.05, 0.06], index=[2, 1, 0])

# But you get label-based addition
combined = returns_1 + returns_2
print(combined)
```

```
0    0.07    # 0.01 + 0.06 (both at index 0)
1    0.07    # 0.02 + 0.05 (both at index 1)
2    0.07    # 0.03 + 0.04 (both at index 2)
dtype: float64
```

You might have expected `[0.05, 0.07, 0.09]` if thinking positionally.

### Problem 2: NaN from Missing Labels

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([4, 5, 6], index=['b', 'c', 'd'])

print(s1 + s2)
```

```
a    NaN    # 'a' only in s1
b    6.0    # matched
c    8.0    # matched
d    NaN    # 'd' only in s2
dtype: float64
```

### Problem 3: DataFrame Column Alignment

```python
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'B': [5, 6], 'A': [7, 8]})

print(df1 + df2)
```

```
    A   B
0   8   8    # A+A, B+B (by column name)
1  10  10
```

Columns aligned by name, not position.

## Solutions

### Solution 1: Reset Index for Position-Based Operations

```python
s1 = pd.Series([0.01, 0.02, 0.03], index=['x', 'y', 'z'])
s2 = pd.Series([0.04, 0.05, 0.06], index=['a', 'b', 'c'])

# Position-based addition
result = s1.reset_index(drop=True) + s2.reset_index(drop=True)
print(result)
```

```
0    0.05
1    0.07
2    0.09
dtype: float64
```

### Solution 2: Use .values for NumPy Operations

```python
# Bypass pandas alignment entirely
result = pd.Series(s1.values + s2.values)
print(result)
```

### Solution 3: Explicit reindex

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([4, 5], index=['a', 'b'])

# Make s2 have same index as s1
s2_aligned = s2.reindex(s1.index, fill_value=0)
print(s1 + s2_aligned)
```

```
a    5
b    7
c    3    # 3 + 0 (filled)
dtype: int64
```

### Solution 4: Verify Alignment Before Operations

```python
def safe_add(s1, s2):
    """Add two series, warning if indices don't match."""
    if not s1.index.equals(s2.index):
        print("Warning: Indices don't match!")
        print(f"s1 index: {s1.index.tolist()}")
        print(f"s2 index: {s2.index.tolist()}")
    return s1 + s2

s1 = pd.Series([1, 2], index=['a', 'b'])
s2 = pd.Series([3, 4], index=['b', 'c'])

result = safe_add(s1, s2)
```

## DataFrame Alignment Issues

### Row and Column Alignment

```python
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]}, index=['x', 'y'])
df2 = pd.DataFrame({'B': [5, 6], 'C': [7, 8]}, index=['y', 'z'])

print(df1 + df2)
```

```
     A    B    C
x  NaN  NaN  NaN
y  NaN  9.0  NaN
z  NaN  NaN  NaN
```

Only 'y' row and 'B' column exist in both.

### Solution: Explicit Alignment

```python
# Fill missing with 0
result = df1.add(df2, fill_value=0)
print(result)
```

```
     A     B    C
x  1.0   3.0  0.0
y  2.0  10.0  8.0
z  0.0   6.0  8.0
```

## Common Scenarios

### After Filtering

```python
df = pd.DataFrame({'A': [1, 2, 3, 4, 5]})

# Filter creates non-contiguous index
filtered = df[df['A'] > 2]
print(filtered.index)  # Int64Index([2, 3, 4])

# Another operation with different index
other = pd.Series([10, 20, 30], index=[0, 1, 2])

# Alignment produces mostly NaN
print(filtered['A'] + other)
```

```
0    NaN
1    NaN
2    13.0    # Only index 2 matches
3    NaN
4    NaN
dtype: float64
```

### After Sorting

```python
df = pd.DataFrame({'A': [3, 1, 2]}, index=['c', 'a', 'b'])
df_sorted = df.sort_values('A')

print(f"Original index: {df.index.tolist()}")
print(f"Sorted index: {df_sorted.index.tolist()}")

# Index is preserved after sort!
# Operations still align by original labels
```

### After GroupBy

```python
df = pd.DataFrame({
    'group': ['A', 'A', 'B', 'B'],
    'value': [1, 2, 3, 4]
})

means = df.groupby('group')['value'].mean()
print(means)  # Index is ['A', 'B'], not [0, 1]
```

## Best Practices

1. **Check indices before operations**
   ```python
   assert s1.index.equals(s2.index), "Index mismatch!"
   ```

2. **Reset index for position-based operations**
   ```python
   result = s1.reset_index(drop=True) + s2.reset_index(drop=True)
   ```

3. **Use explicit alignment**
   ```python
   s2_aligned = s2.reindex_like(s1)
   ```

4. **Sort index if order matters**
   ```python
   s1 = s1.sort_index()
   s2 = s2.sort_index()
   ```

5. **Document expected indices**
   ```python
   # Input: daily returns indexed by date
   # Both series must have identical DatetimeIndex
   ```

## Summary

| Issue | Solution |
|-------|----------|
| Order doesn't match | `reset_index(drop=True)` |
| Missing labels | `reindex(fill_value=0)` |
| Need position-based | Use `.values` for NumPy |
| Unknown alignment | Check `.index.equals()` |
| After groupby | Be aware new index is group keys |


---

## Exercises

**Exercise 1.** Create two Series with different indices and add them. Explain why some results are `NaN`.

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

**Exercise 2.** Write code that demonstrates index alignment in DataFrame arithmetic. Show what happens when indices don't match.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Explain how to use `reindex()` or `reset_index()` to fix index misalignment issues.

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

**Exercise 4.** Write code showing the difference between `df1 + df2` (which aligns by index) and `df1.values + df2.values` (which does not).

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
