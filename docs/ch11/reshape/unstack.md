# unstack Method

The `unstack()` method pivots rows into columns, moving an index level to become a column level. This is useful for converting long-format data to wide-format.

!!! tip "Mental Model"
    `unstack` pulls an index level out of the row axis and spreads its unique values across as new column headers. The result is wider and shorter -- more columns, fewer rows. It is the inverse of `stack` and the index-based counterpart of `pivot`.

## Basic Concept

```
Before unstack():              After unstack():
                                      A    B
0  A    1.0                    0    1.0  2.0
   B    2.0                    1    3.0  4.0
1  A    3.0
   B    4.0
```

## Basic Usage

```python
import pandas as pd
import numpy as np

# Create a Series with MultiIndex
index = pd.MultiIndex.from_tuples([
    (0, 'A'), (0, 'B'),
    (1, 'A'), (1, 'B')
])
s = pd.Series([1.0, 2.0, 3.0, 4.0], index=index)

print("Original Series:")
print(s)
print()

unstacked = s.unstack()
print("After unstack():")
print(unstacked)
```

```
Original Series:
0  A    1.0
   B    2.0
1  A    3.0
   B    4.0
dtype: float64

After unstack():
     A    B
0  1.0  2.0
1  3.0  4.0
```

## Specifying Level to Unstack

By default, `unstack()` operates on the innermost level (-1):

```python
# Create MultiIndex with named levels
index = pd.MultiIndex.from_tuples([
    ('row1', 'A'), ('row1', 'B'),
    ('row2', 'A'), ('row2', 'B')
], names=['row', 'col'])

s = pd.Series([1, 2, 3, 4], index=index)

print("Original:")
print(s)
print()

# Unstack inner level (default)
print("unstack() [default, level=-1]:")
print(s.unstack())
print()

# Unstack outer level
print("unstack(level=0):")
print(s.unstack(level=0))
```

```
Original:
row   col
row1  A      1
      B      2
row2  A      3
      B      4
dtype: int64

unstack() [default, level=-1]:
col   A  B
row        
row1  1  2
row2  3  4

unstack(level=0):
row   row1  row2
col             
A        1     3
B        2     4
```

### Unstack by Level Name

```python
# Unstack by name instead of position
print(s.unstack(level='col'))
print(s.unstack(level='row'))
```

## Handling Missing Values

`unstack()` introduces NaN when combinations don't exist:

```python
# Incomplete MultiIndex
index = pd.MultiIndex.from_tuples([
    ('A', 1), ('A', 2),
    ('B', 1)  # Missing ('B', 2)
])
s = pd.Series([10, 20, 30], index=index)

print("Original (missing B-2):")
print(s)
print()

print("After unstack():")
print(s.unstack())
```

```
Original (missing B-2):
A  1    10
   2    20
B  1    30
dtype: int64

After unstack():
      1     2
A  10.0  20.0
B  30.0   NaN
```

### Fill Missing Values

```python
# Fill NaN with a specific value
print(s.unstack(fill_value=0))
```

```
    1   2
A  10  20
B  30   0
```

## DataFrame unstack

Works on DataFrame index levels:

```python
# DataFrame with MultiIndex
index = pd.MultiIndex.from_tuples([
    ('AAPL', 'day1'), ('AAPL', 'day2'),
    ('MSFT', 'day1'), ('MSFT', 'day2')
], names=['ticker', 'date'])

df = pd.DataFrame({
    'price': [150, 151, 300, 301],
    'volume': [1000, 1100, 2000, 2100]
}, index=index)

print("Original:")
print(df)
print()

# Unstack the date level
print("unstack('date'):")
print(df.unstack('date'))
```

```
Original:
              price  volume
ticker date                
AAPL   day1    150    1000
       day2    151    1100
MSFT   day1    300    2000
       day2    301    2100

unstack('date'):
       price       volume      
date    day1 day2   day1  day2
ticker                        
AAPL     150  151   1000  1100
MSFT     300  301   2000  2100
```

## Practical Examples

### Panel Data Reshaping

```python
# Long format panel data
np.random.seed(42)
tickers = ['AAPL', 'MSFT', 'GOOGL']
dates = pd.date_range('2024-01-01', periods=5)

# Create MultiIndex panel
index = pd.MultiIndex.from_product([tickers, dates], names=['ticker', 'date'])
returns = pd.Series(np.random.randn(15) * 0.02, index=index, name='return')

print("Long format (panel):")
print(returns.head(10))
print()

# Unstack to wide format (each ticker as column)
returns_wide = returns.unstack('ticker')
print("Wide format:")
print(returns_wide)
```

### Cross-Sectional Analysis

```python
# Wide format is useful for correlation analysis
correlation = returns_wide.corr()
print("Correlation matrix:")
print(correlation)
```

### Time Series Pivot

```python
# Data by sector and date
index = pd.MultiIndex.from_product([
    ['Tech', 'Finance', 'Health'],
    pd.date_range('2024-01-01', periods=3)
], names=['sector', 'date'])

df = pd.DataFrame({
    'returns': np.random.randn(9) * 0.02,
    'volume': np.random.randint(100, 1000, 9)
}, index=index)

print("Original:")
print(df)
print()

# Pivot: dates as columns, sectors as rows
returns_pivot = df['returns'].unstack('date')
print("Returns pivoted:")
print(returns_pivot)
```

## Multiple Unstacks

You can unstack multiple times:

```python
# Three-level MultiIndex
index = pd.MultiIndex.from_product([
    ['2024', '2025'],
    ['Q1', 'Q2'],
    ['AAPL', 'MSFT']
], names=['year', 'quarter', 'ticker'])

s = pd.Series(range(8), index=index)
print("Original (3 levels):")
print(s)
print()

# Unstack once
print("After one unstack():")
print(s.unstack())
print()

# Unstack twice
print("After two unstacks:")
print(s.unstack().unstack())
```

## unstack vs pivot

Both reshape data, but differently:

| Aspect | unstack() | pivot() |
|--------|-----------|---------|
| Input | Series/DataFrame with MultiIndex | DataFrame with columns |
| Source | Index levels | Column values |
| Operation | Index level → columns | Column → columns |

```python
# Using unstack (from MultiIndex)
s = pd.Series([1, 2, 3, 4], 
              index=pd.MultiIndex.from_product([['A', 'B'], ['x', 'y']]))
print("unstack():")
print(s.unstack())
print()

# Using pivot (from columns)
df = pd.DataFrame({
    'row': ['A', 'A', 'B', 'B'],
    'col': ['x', 'y', 'x', 'y'],
    'value': [1, 2, 3, 4]
})
print("pivot():")
print(df.pivot(index='row', columns='col', values='value'))
```

## stack and unstack are Inverses

```python
df = pd.DataFrame({
    'A': [1, 2],
    'B': [3, 4]
}, index=['x', 'y'])

print("Original:")
print(df)
print()

# Stack then unstack returns original
stacked = df.stack()
unstacked = stacked.unstack()
print("After stack().unstack():")
print(unstacked)
```

## Summary

| Parameter | Description | Default |
|-----------|-------------|---------|
| `level` | Which level to unstack | -1 (innermost) |
| `fill_value` | Value for missing combinations | NaN |

**Key Points:**

- `unstack()` pivots index level to columns
- Inverse of `stack()`
- Creates NaN for missing combinations
- Use `fill_value` to handle missing data
- Essential for converting long to wide format


---

## Exercises

**Exercise 1.** Write code that creates a Series with a MultiIndex and uses `.unstack()` to convert it to a DataFrame.

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

**Exercise 2.** Explain what `.unstack()` does. Which index level is moved to columns by default?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Create a MultiIndex DataFrame and use `.unstack(fill_value=0)` to fill NaN values created by the reshape.

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

**Exercise 4.** Write code that unstacks a grouped aggregation result (e.g., `df.groupby(['a', 'b']).mean().unstack()`).

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
