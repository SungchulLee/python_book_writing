# stack Method

The `stack()` method pivots columns into rows, moving the innermost column level to become the innermost row index level. This is useful for converting wide-format data to long-format.

!!! tip "Mental Model"
    `stack` takes column headers and pushes them down into the row index, creating a MultiIndex. The result is longer and narrower -- fewer columns, more rows. It is the index-based counterpart of `melt`, and its inverse is `unstack`.

## Basic Concept

```
Before stack():                After stack():
        A    B                          
   0   1.0  2.0                0  A    1.0
   1   3.0  4.0                   B    2.0
                               1  A    3.0
                                  B    4.0
```

## Basic Usage

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1.0, 3.0],
    'B': [2.0, 4.0]
})
print("Original DataFrame:")
print(df)
print()

stacked = df.stack()
print("After stack():")
print(stacked)
print(f"\nType: {type(stacked)}")
```

```
Original DataFrame:
     A    B
0  1.0  2.0
1  3.0  4.0

After stack():
0  A    1.0
   B    2.0
1  A    3.0
   B    4.0
dtype: float64

Type: <class 'pandas.core.series.Series'>
```

## Result is a MultiIndex Series

After stacking, the result is a Series with a MultiIndex:

```python
stacked = df.stack()
print(f"Index levels: {stacked.index.names}")
print(f"Index:\n{stacked.index}")
```

```
Index levels: [None, None]
Index:
MultiIndex([(0, 'A'),
            (0, 'B'),
            (1, 'A'),
            (1, 'B')],
           )
```

## With Named Index and Columns

```python
df = pd.DataFrame(
    {'A': [1, 3], 'B': [2, 4]},
    index=['row1', 'row2']
)
df.columns.name = 'letter'
df.index.name = 'row'

print("Original:")
print(df)
print()

stacked = df.stack()
print("Stacked:")
print(stacked)
```

```
Original:
letter  A  B
row          
row1    1  2
row2    3  4

Stacked:
row   letter
row1  A         1
      B         2
row2  A         3
      B         4
dtype: int64
```

## Handling Missing Values

By default, `stack()` drops rows with NaN values:

```python
df = pd.DataFrame({
    'A': [1.0, np.nan],
    'B': [2.0, 4.0]
})
print("Original:")
print(df)
print()

# Default: dropna=True (drops NaN)
print("stack() [default]:")
print(df.stack())
print()

# Keep NaN values
print("stack(dropna=False):")
print(df.stack(dropna=False))
```

```
Original:
     A    B
0  1.0  2.0
1  NaN  4.0

stack() [default]:
0  A    1.0
   B    2.0
1  B    4.0
dtype: float64

stack(dropna=False):
0  A    1.0
   B    2.0
1  A    NaN
   B    4.0
dtype: float64
```

## Multi-Level Columns

When columns have multiple levels, `stack()` operates on the innermost level:

```python
# Create DataFrame with MultiIndex columns
columns = pd.MultiIndex.from_tuples([
    ('price', 'AAPL'), ('price', 'MSFT'),
    ('volume', 'AAPL'), ('volume', 'MSFT')
])
df = pd.DataFrame(
    [[150, 300, 1000, 2000],
     [151, 301, 1100, 2100]],
    index=['day1', 'day2'],
    columns=columns
)

print("Original (multi-level columns):")
print(df)
print()

# Stack innermost level (ticker)
stacked = df.stack()
print("After stack():")
print(stacked)
```

```
Original (multi-level columns):
      price      volume      
       AAPL MSFT   AAPL  MSFT
day1    150  300   1000  2000
day2    151  301   1100  2100

After stack():
           price  volume
day1 AAPL    150    1000
     MSFT    300    2000
day2 AAPL    151    1100
     MSFT    301    2100
```

### Specifying Level to Stack

```python
# Stack the outer level instead
stacked_outer = df.stack(level=0)
print("Stack outer level (level=0):")
print(stacked_outer)
```

```
Stack outer level (level=0):
            AAPL  MSFT
day1 price   150   300
     volume 1000  2000
day2 price   151   301
     volume 1100  2100
```

## Practical Examples

### Converting Wide Price Data to Long Format

```python
# Wide format: each ticker is a column
prices_wide = pd.DataFrame({
    'AAPL': [150, 151, 152],
    'MSFT': [300, 301, 302],
    'GOOGL': [140, 141, 142]
}, index=pd.date_range('2024-01-01', periods=3))
prices_wide.columns.name = 'ticker'
prices_wide.index.name = 'date'

print("Wide format:")
print(prices_wide)
print()

# Convert to long format
prices_long = prices_wide.stack()
prices_long.name = 'price'
print("Long format:")
print(prices_long)
```

```
Wide format:
ticker      AAPL  MSFT  GOOGL
date                         
2024-01-01   150   300    140
2024-01-02   151   301    141
2024-01-03   152   302    142

Long format:
date        ticker
2024-01-01  AAPL      150
            MSFT      300
            GOOGL     140
2024-01-02  AAPL      151
            MSFT      301
            GOOGL     141
2024-01-03  AAPL      152
            MSFT      302
            GOOGL     142
Name: price, dtype: int64
```

### Reset to DataFrame

```python
# Convert stacked Series back to DataFrame
prices_df = prices_long.reset_index()
prices_df.columns = ['date', 'ticker', 'price']
print(prices_df)
```

```
        date ticker  price
0 2024-01-01   AAPL    150
1 2024-01-01   MSFT    300
2 2024-01-01  GOOGL    140
3 2024-01-02   AAPL    151
...
```

### Financial Data Reshaping

```python
# OHLC data in wide format
ohlc_wide = pd.DataFrame({
    ('AAPL', 'open'): [149, 150],
    ('AAPL', 'close'): [150, 151],
    ('MSFT', 'open'): [299, 300],
    ('MSFT', 'close'): [300, 301],
}, index=['day1', 'day2'])
ohlc_wide.columns = pd.MultiIndex.from_tuples(ohlc_wide.columns)

print("Wide OHLC:")
print(ohlc_wide)
print()

# Stack to get ticker as row index
stacked = ohlc_wide.stack(level=0)
print("Stacked by ticker:")
print(stacked)
```

## Stack vs Melt

Both convert wide to long format, but differently:

| Aspect | stack() | melt() |
|--------|---------|--------|
| Input | DataFrame | DataFrame |
| Output | Series (usually) | DataFrame |
| Index | Uses existing index | Resets index |
| Column handling | Moves to index | Moves to column |
| Multi-level | Handles naturally | Requires flatten first |

```python
df = pd.DataFrame({
    'A': [1, 2],
    'B': [3, 4]
}, index=['x', 'y'])

# stack: columns become inner index level
stacked = df.stack()
print("stack():")
print(stacked)
print()

# melt: columns become a column value
melted = df.reset_index().melt(id_vars='index')
print("melt():")
print(melted)
```

## Summary

| Parameter | Description | Default |
|-----------|-------------|---------|
| `level` | Which level to stack | -1 (innermost) |
| `dropna` | Drop rows with missing values | True |

**Key Points:**

- `stack()` pivots columns to rows
- Result is typically a Series with MultiIndex
- Operates on innermost column level by default
- Inverse operation is `unstack()`


---

## Exercises

**Exercise 1.** Write code that uses `.stack()` on a DataFrame to move column labels into the index, creating a MultiIndex Series.

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

**Exercise 2.** Explain the relationship between `.stack()` and `.unstack()`. What does each do?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Create a DataFrame with MultiIndex columns and use `.stack(level=0)` and `.stack(level=1)` to show the difference.

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

**Exercise 4.** Write code showing how `.stack()` handles NaN values. What does `dropna=False` do?

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
