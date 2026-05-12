# Series Creation

This document covers all methods for creating pandas Series objects, from basic list conversion to extracting columns from DataFrames.

!!! tip "Mental Model"
    A Series is created by pairing values with an index. Pass a list and you get auto-numbered labels `[0, 1, 2, ...]`. Pass a dict and the keys become the index. Extract a DataFrame column and you inherit that DataFrame's index. Every creation method is just a different way to specify the value-label pairs.

## From a List

The simplest way to create a Series is from a Python list.

### Basic Creation

```python
import pandas as pd

# Default integer index (0, 1, 2, ...)
s = pd.Series([3, 9, 1])
print(s)
```

```
0    3
1    9
2    1
dtype: int64
```

### With Custom Index

```python
s = pd.Series([3, 9, 1], index=['a', 'b', 'c'])
print(s)
```

```
a    3
b    9
c    1
dtype: int64
```

### With Name

```python
s = pd.Series([3, 9, 1], name='values')
print(s)
```

```
0    3
1    9
2    1
Name: values, dtype: int64
```

### With DatetimeIndex

```python
data = [3, 9, 1]
name = "daily_values"
index = pd.date_range(start='2019-09-01', end='2019-09-03')

s = pd.Series(data, name=name, index=index)
print(s)
```

```
2019-09-01    3
2019-09-02    9
2019-09-03    1
Freq: D, Name: daily_values, dtype: int64
```

### Specifying dtype

```python
# Force float type
s = pd.Series([1, 2, 3], dtype='float64')
print(s)
```

```
0    1.0
1    2.0
2    3.0
dtype: float64
```

## From a Dictionary

When creating from a dictionary, keys become index labels.

### Basic Dictionary Creation

```python
data = {'a': 10, 'b': 20, 'c': 30}
s = pd.Series(data)
print(s)
```

```
a    10
b    20
c    30
dtype: int64
```

### With Date String Keys

```python
data_dict = {
    '2019-09-01': 3,
    '2019-09-02': 9,
    '2019-09-03': 1
}
s = pd.Series(data_dict, name="data")
print(s)
```

```
2019-09-01    3
2019-09-02    9
2019-09-03    1
Name: data, dtype: int64
```

### Reordering with Index Parameter

```python
data = {'a': 10, 'b': 20, 'c': 30}

# Reorder and potentially add NaN for missing keys
s = pd.Series(data, index=['c', 'b', 'a', 'd'])
print(s)
```

```
c    30.0
b    20.0
a    10.0
d     NaN
dtype: float64
```

## From a DataFrame Column

Extracting a column from a DataFrame returns a Series.

### Bracket Notation (Recommended)

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Single brackets return a Series
survived = df["Survived"]
print(type(survived))  # <class 'pandas.core.series.Series'>
print(survived.head())
```

```
0    0
1    1
2    1
3    1
4    0
Name: Survived, dtype: int64
```

### Dot Notation (Use Cautiously)

```python
# Works for simple column names
survived = df.Survived
print(type(survived))  # <class 'pandas.core.series.Series'>
```

**Limitations of dot notation:**

- Fails if column name contains spaces
- Fails if column name starts with a number
- Fails if column name conflicts with DataFrame methods

```python
# These will NOT work with dot notation:
# df.Passenger Id  # Syntax error (space)
# df.1st_class     # Syntax error (starts with number)
# df.count         # Returns method, not column
```

### Preserving DataFrame Type

```python
# Double brackets return a DataFrame, not a Series
survived_df = df[["Survived"]]
print(type(survived_df))  # <class 'pandas.core.frame.DataFrame'>
print(survived_df.shape)  # (891, 1)

# Single brackets return a Series
survived_series = df["Survived"]
print(survived_series.shape)  # (891,)
```

## From a NumPy Array

```python
import numpy as np

arr = np.array([1.5, 2.5, 3.5])
s = pd.Series(arr)
print(s)
```

```
0    1.5
1    2.5
2    3.5
dtype: float64
```

### With Shared Memory

By default, the Series may share memory with the original array:

```python
arr = np.array([1, 2, 3])
s = pd.Series(arr)

arr[0] = 999
print(s[0])  # May be 999 (shared memory)

# To avoid shared memory, use copy=True
s = pd.Series(arr, copy=True)
```

## From a Scalar Value

A scalar is broadcast to fill all index positions.

```python
s = pd.Series(5, index=['a', 'b', 'c'])
print(s)
```

```
a    5
b    5
c    5
dtype: int64
```

## From a Range

```python
s = pd.Series(range(5))
print(s)
```

```
0    0
1    1
2    2
3    3
4    4
dtype: int64
```

## dtype Inference and Upcasting

pandas automatically infers the appropriate dtype and performs upcasting when needed.

### String Data → object

```python
s = pd.Series(['Boat', 'Car', 'Bike'])
print(f"{s.dtype = }")  # s.dtype = dtype('O')
```

### Integer Data → int64

```python
s = pd.Series([1, 55, 99])
print(f"{s.dtype = }")  # s.dtype = dtype('int64')
```

### Float Data → float64

```python
s = pd.Series([1., 55., 99.])
print(f"{s.dtype = }")  # s.dtype = dtype('float64')
```

### Mixed int/float → Upcasted to float64

```python
s = pd.Series([1., 55, 99])  # Mixed float and int
print(f"{s.dtype = }")  # s.dtype = dtype('float64')
```

### With Missing Values → float64

```python
s = pd.Series([1, 2, None])
print(f"{s.dtype = }")  # s.dtype = dtype('float64')
print(s)
```

```
0    1.0
1    2.0
2    NaN
dtype: float64
```

### Nullable Integer Type

```python
# Use nullable integer type to preserve integers with NaN
s = pd.Series([1, 2, None], dtype='Int64')
print(s)
```

```
0       1
1       2
2    <NA>
dtype: Int64
```

## Financial Examples

### Stock Prices

```python
import yfinance as yf

# Download and extract close prices as Series
ticker = 'AAPL'
df = yf.Ticker(ticker).history(start='2024-01-01', end='2024-06-30')

close_prices = df['Close']
print(type(close_prices))  # <class 'pandas.core.series.Series'>
print(close_prices.head())
```

### Portfolio Weights

```python
weights = pd.Series({
    'AAPL': 0.30,
    'MSFT': 0.25,
    'GOOGL': 0.20,
    'AMZN': 0.15,
    'META': 0.10
}, name='weight')

print(weights)
print(f"Total: {weights.sum()}")  # 1.0
```

### Daily Returns

```python
# Create returns Series from prices
prices = pd.Series(
    [100, 102, 101, 105, 103],
    index=pd.date_range('2024-01-01', periods=5),
    name='AAPL'
)

returns = prices.pct_change()
print(returns)
```

```
2024-01-01         NaN
2024-01-02    0.020000
2024-01-03   -0.009804
2024-01-04    0.039604
2024-01-05   -0.019048
Freq: D, Name: AAPL, dtype: float64
```

## Creation Method Summary

| Method | Use Case | Example |
|--------|----------|---------|
| From list | Simple data | `pd.Series([1, 2, 3])` |
| From dict | Labeled data | `pd.Series({'a': 1, 'b': 2})` |
| From DataFrame | Column extraction | `df['column']` |
| From NumPy | Numerical computing | `pd.Series(np.array([...]))` |
| From scalar | Constant fill | `pd.Series(0, index=[...])` |
| From range | Sequential integers | `pd.Series(range(10))` |

---

## Exercises

**Exercise 1.**
Create a pandas Series from a dictionary where the keys are stock tickers `'AAPL'`, `'MSFT'`, `'GOOGL'` and the values are their closing prices `150.0`, `350.0`, `140.0`. Name the Series `'close_price'`. Print the Series and verify its `dtype` is `float64`.

??? success "Solution to Exercise 1"
    Create the Series from a dictionary and assign a name.

        import pandas as pd

        data = {'AAPL': 150.0, 'MSFT': 350.0, 'GOOGL': 140.0}
        s = pd.Series(data, name='close_price')
        print(s)
        print(f"dtype: {s.dtype}")  # float64

---

**Exercise 2.**
Create a Series of five daily portfolio values `[10000, 10250, 10100, 10400, 10350]` with a `DatetimeIndex` starting from `'2024-06-01'`. Name the Series `'portfolio_value'`. Then compute the daily percentage change using `pct_change()` and print it.

??? success "Solution to Exercise 2"
    Use `pd.date_range` for the index and `pct_change()` for returns.

        import pandas as pd

        values = [10000, 10250, 10100, 10400, 10350]
        index = pd.date_range(start='2024-06-01', periods=5)
        s = pd.Series(values, index=index, name='portfolio_value')
        print(s)
        print(s.pct_change())

---

**Exercise 3.**
Create a Series from the list `[10, 20, None, 40, 50]` using the nullable integer type `'Int64'`. Confirm that the dtype is `Int64` (not `float64`) and that the missing value displays as `<NA>` rather than `NaN`.

??? success "Solution to Exercise 3"
    Use the capital-I `'Int64'` nullable integer dtype.

        import pandas as pd

        s = pd.Series([10, 20, None, 40, 50], dtype='Int64')
        print(s)
        print(f"dtype: {s.dtype}")  # Int64
        print(f"Missing value: {s[2]}")  # <NA>
