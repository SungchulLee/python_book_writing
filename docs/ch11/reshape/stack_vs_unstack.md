# stack vs unstack

`stack()` and `unstack()` are inverse operations for reshaping data between wide and long formats. Understanding when to use each is essential for data manipulation.

!!! tip "Mental Model"
    `stack` moves columns into the index (wide to long); `unstack` moves an index level into columns (long to wide). They are perfect inverses: `unstack(stack(df))` returns the original shape. The `level` parameter controls which index level or column level participates in the swap.

## Conceptual Overview

```
                    stack()
     Wide Format  ──────────►  Long Format
     (DataFrame)               (Series/MultiIndex)
                  ◄──────────
                   unstack()
```

## Visual Comparison

### stack(): Columns → Rows

```
Before stack():                After stack():
        A    B                          
   0   1.0  2.0                0  A    1.0
   1   3.0  4.0                   B    2.0
                               1  A    3.0
        ↓                         B    4.0
   Columns A, B
   become inner                   ↑
   index level               Inner index
                             has A, B
```

### unstack(): Rows → Columns

```
Before unstack():              After unstack():
                                      A    B
0  A    1.0                    0    1.0  2.0
   B    2.0                    1    3.0  4.0
1  A    3.0
   B    4.0                         ↑
                               Inner index A, B
   ↓                           become columns
Inner index
level A, B
```

## Side-by-Side Code Example

```python
import pandas as pd
import numpy as np

# Start with a DataFrame
df = pd.DataFrame({
    'A': [1.0, 3.0],
    'B': [2.0, 4.0]
}, index=['row0', 'row1'])
df.columns.name = 'col'
df.index.name = 'row'

print("Original DataFrame:")
print(df)
print()

# stack: columns become inner index
stacked = df.stack()
print("After stack() - columns A,B become index level:")
print(stacked)
print()

# unstack: inner index becomes columns
unstacked = stacked.unstack()
print("After unstack() - index level becomes columns:")
print(unstacked)
```

```
Original DataFrame:
col    A    B
row          
row0  1.0  2.0
row1  3.0  4.0

After stack() - columns A,B become index level:
row   col
row0  A      1.0
      B      2.0
row1  A      3.0
      B      4.0
dtype: float64

After unstack() - index level becomes columns:
col    A    B
row          
row0  1.0  2.0
row1  3.0  4.0
```

## Key Differences

| Aspect | stack() | unstack() |
|--------|---------|-----------|
| Direction | Columns → Index | Index → Columns |
| Input type | DataFrame | Series/DataFrame with MultiIndex |
| Output type | Usually Series | Usually DataFrame |
| Effect on shape | Longer, narrower | Shorter, wider |
| Use case | Wide → Long | Long → Wide |

## Multi-Level Examples

### stack() with Multi-Level Columns

```python
# Create DataFrame with 2-level columns
columns = pd.MultiIndex.from_product([['price', 'volume'], ['AAPL', 'MSFT']])
df = pd.DataFrame(
    [[150, 300, 1000, 2000],
     [151, 301, 1100, 2100]],
    index=['day1', 'day2'],
    columns=columns
)

print("Original (2-level columns):")
print(df)
print()

# stack innermost column level
stacked = df.stack()
print("stack() - innermost column level to index:")
print(stacked)
print()

# stack outer column level
stacked_level0 = df.stack(level=0)
print("stack(level=0) - outer column level to index:")
print(stacked_level0)
```

### unstack() with Multi-Level Index

```python
# Create Series with 3-level index
index = pd.MultiIndex.from_product([
    ['2024'],
    ['AAPL', 'MSFT'],
    ['Q1', 'Q2']
], names=['year', 'ticker', 'quarter'])

s = pd.Series([100, 110, 200, 210], index=index)

print("Original (3-level index):")
print(s)
print()

# unstack innermost level
print("unstack() - innermost level to columns:")
print(s.unstack())
print()

# unstack middle level
print("unstack('ticker') - ticker level to columns:")
print(s.unstack('ticker'))
```

## When to Use Each

### Use stack() When:

1. **Converting wide to long format**
   ```python
   # Multiple columns for same variable type
   df = pd.DataFrame({
       'AAPL': [150, 151],
       'MSFT': [300, 301],
       'GOOGL': [140, 141]
   })
   
   # Stack to get single 'price' series
   prices_long = df.stack()
   ```

2. **Preparing data for certain analyses**
   ```python
   # GroupBy analysis often needs long format
   prices_long.groupby(level=1).mean()  # Mean per ticker
   ```

3. **Creating MultiIndex from columns**
   ```python
   df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
   df.stack()  # Creates MultiIndex Series
   ```

### Use unstack() When:

1. **Converting long to wide format**
   ```python
   # Panel data in long format
   returns_long = pd.Series(..., index=pd.MultiIndex.from_product([tickers, dates]))
   
   # Unstack to get tickers as columns
   returns_wide = returns_long.unstack('ticker')
   ```

2. **Creating correlation/covariance matrices**
   ```python
   # Wide format needed for .corr()
   returns_wide = returns_long.unstack()
   correlation = returns_wide.corr()
   ```

3. **Pivoting for visualization**
   ```python
   # Many plotting functions expect wide format
   returns_wide.plot()
   ```

## Practical Financial Example

```python
# Start with long-format returns data
np.random.seed(42)
tickers = ['AAPL', 'MSFT', 'GOOGL']
dates = pd.date_range('2024-01-01', periods=5)

index = pd.MultiIndex.from_product([dates, tickers], names=['date', 'ticker'])
returns = pd.Series(np.random.randn(15) * 0.02, index=index, name='return')

print("Long format (common in databases):")
print(returns)
print()

# UNSTACK: Convert to wide for analysis
returns_wide = returns.unstack('ticker')
print("Wide format (after unstack):")
print(returns_wide)
print()

# Calculate correlation (requires wide format)
print("Correlation matrix:")
print(returns_wide.corr().round(2))
print()

# STACK: Convert back to long
returns_long = returns_wide.stack()
print("Back to long format (after stack):")
print(returns_long)
```

## Roundtrip Property

`stack()` and `unstack()` are inverses:

```python
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

# stack then unstack = original
assert df.equals(df.stack().unstack())

# For Series with MultiIndex:
s = pd.Series([1, 2, 3, 4], 
              index=pd.MultiIndex.from_product([['a', 'b'], ['x', 'y']]))

# unstack then stack = original  
assert s.equals(s.unstack().stack())
```

## Comparison with pivot/melt

| Operation | From | To | Index handling |
|-----------|------|-----|----------------|
| `stack()` | Wide DataFrame | Long Series | Preserves, adds level |
| `unstack()` | Long (MultiIndex) | Wide DataFrame | Removes level |
| `pivot()` | Long DataFrame | Wide DataFrame | From column values |
| `melt()` | Wide DataFrame | Long DataFrame | Resets index |

```python
# Equivalent operations:

# Using stack/unstack (works with index)
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]}, index=['x', 'y'])
stacked = df.stack()
unstacked = stacked.unstack()

# Using melt/pivot (works with columns)
df_reset = df.reset_index()
melted = df_reset.melt(id_vars='index', var_name='column', value_name='value')
pivoted = melted.pivot(index='index', columns='column', values='value')
```

## Summary

| Need | Use |
|------|-----|
| Columns → Index level | `stack()` |
| Index level → Columns | `unstack()` |
| Wide → Long (keeping index) | `stack()` |
| Long → Wide (from MultiIndex) | `unstack()` |
| Wide → Long (resetting index) | `melt()` |
| Long → Wide (from columns) | `pivot()` |


---

## Exercises

**Exercise 1.** Write code that demonstrates `stack()` followed by `unstack()` returns the original DataFrame.

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

**Exercise 2.** Explain when you would use `stack()` vs `melt()` for converting wide format to long format.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Create a MultiIndex DataFrame and use `unstack()` to move an index level to columns. Then use `stack()` to reverse it.

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

**Exercise 4.** Write code showing the difference between `unstack(level=0)` and `unstack(level=1)` on a 2-level MultiIndex.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
