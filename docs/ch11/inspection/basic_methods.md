# Basic DataFrame Methods

Essential methods for inspecting and exploring DataFrame contents.

!!! tip "Mental Model"
    Inspection methods are your data microscope. `head()` and `tail()` show the edges, `info()` gives a structural summary with dtypes and null counts, and `describe()` computes column-wise statistics. Run these three right after loading any new dataset to build a mental picture before writing analysis code.

## head and tail

View first or last rows.

### 1. head Method

```python
import pandas as pd
import yfinance as yf

df = yf.Ticker('WMT').history(start='2020-01-01', end='2020-12-31')
print(df.head())      # First 5 rows (default)
print(df.head(3))     # First 3 rows
```

### 2. tail Method

```python
print(df.tail())      # Last 5 rows (default)
print(df.tail(3))     # Last 3 rows
```

### 3. Quick Preview

```python
# Combine for overview
print(df.head(2))
print('...')
print(df.tail(2))
```

## info

Display DataFrame summary.

### 1. Basic Info

```python
print(df.info())
```

```
<class 'pandas.core.frame.DataFrame'>
DatetimeIndex: 253 entries, 2020-01-02 to 2020-12-31
Data columns (total 7 columns):
 #   Column        Non-Null Count  Dtype  
---  ------        --------------  -----  
 0   Open          253 non-null    float64
 1   High          253 non-null    float64
...
```

### 2. Information Provided

- Index type and range
- Column count
- Column names and dtypes
- Non-null counts
- Memory usage

### 3. Memory Details

```python
df.info(memory_usage='deep')
```

## describe

Generate descriptive statistics.

### 1. Numeric Columns

```python
print(df.describe())
```

```
              Open         High          Low        Close
count   253.000000   253.000000   253.000000   253.000000
mean    120.456789   121.234567   119.876543   120.567890
std       8.123456     8.234567     8.012345     8.156789
min     102.345678   103.456789   101.234567   102.456789
25%     114.567890   115.678901   113.456789   114.678901
50%     120.123456   121.234567   119.012345   120.234567
75%     126.789012   127.890123   125.678901   126.890123
max     138.901234   140.012345   137.890123   139.012345
```

### 2. Include All Columns

```python
print(df.describe(include='all'))
```

### 3. Returns DataFrame

```python
stats = df.describe()
print(type(stats))  # DataFrame
print(stats.loc['mean', 'Close'])  # Access specific stat
```

## copy

Create a deep copy of DataFrame.

### 1. Deep Copy

```python
df_copy = df.copy()
```

### 2. Why Copy Matters

```python
# Without copy, changes affect original
df_view = df
df_view.iloc[0, 0] = 9999
print(df.iloc[0, 0])  # 9999 - original changed!

# With copy, original is safe
df_copy = df.copy()
df_copy.iloc[0, 0] = 9999
print(df.iloc[0, 0])  # Original unchanged
```

### 3. Deep vs Shallow

```python
df_deep = df.copy(deep=True)   # Default
df_shallow = df.copy(deep=False)
```

## isna and isnull

Check for missing values.

### 1. Check Missing

```python
import numpy as np

df.iloc[1, 1] = np.nan
df.iloc[2, 2] = np.nan

print(df.isna().head(3))
```

### 2. isna vs isnull

```python
# They are identical
print(df.isna().equals(df.isnull()))  # True
```

### 3. Count Missing

```python
print(df.isnull().sum())  # Missing per column
```

## iterrows

Iterate over rows as (index, Series) pairs.

### 1. Basic Iteration

```python
for date, row in df.iterrows():
    print(date)
    print(row)
    print('-' * 40)
    break  # Just show first
```

### 2. Access Values

```python
for idx, row in df.iterrows():
    print(f"Date: {idx}, Close: {row['Close']}")
```

### 3. Performance Warning

```python
# iterrows is slow for large DataFrames
# Prefer vectorized operations when possible
```

## itertuples

Faster iteration with named tuples.

### 1. Basic Usage

```python
for row in df.itertuples():
    print(row.Index, row.Close)
```

### 2. Faster than iterrows

```python
# itertuples is faster than iterrows
```

### 3. Access by Name

```python
for row in df.itertuples(index=False):
    print(row.Open, row.Close)
```

## sample

Random sample of rows.

### 1. Random Rows

```python
print(df.sample(5))  # 5 random rows
```

### 2. Reproducible Sample

```python
print(df.sample(5, random_state=42))
```

### 3. Fraction Sample

```python
print(df.sample(frac=0.1))  # 10% of rows
```

## min and max

Find minimum and maximum values.

### 1. Column Min/Max

```python
print(df['Close'].min())
print(df['Close'].max())
```

### 2. All Columns

```python
print(df.min())  # Min of each column
print(df.max())  # Max of each column
```

### 3. With Index

```python
print(df['Close'].idxmin())  # Index of min
print(df['Close'].idxmax())  # Index of max
```

## count

Count non-null values.

### 1. Per Column

```python
print(df.count())
```

### 2. Single Column

```python
print(df['Close'].count())
```

### 3. vs len()

```python
print(len(df))       # Total rows
print(df.count())    # Non-null per column
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with 100 rows of random data. Use `.head(10)` and `.tail(10)` to view the first and last 10 rows. Then use `.sample(5, random_state=0)` to get a reproducible random sample.

??? success "Solution to Exercise 1"
    Use head, tail, and sample for quick inspection.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        df = pd.DataFrame(np.random.randn(100, 3), columns=['A', 'B', 'C'])
        print(df.head(10))
        print(df.tail(10))
        print(df.sample(5, random_state=0))

---

**Exercise 2.**
Create a DataFrame with some `NaN` values. Use `.info()` to inspect the non-null counts per column, then use `.isna().sum()` to confirm the count of missing values in each column.

??? success "Solution to Exercise 2"
    Use info and isna to inspect missing data.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', None, 'Dave'],
            'age': [25, np.nan, 35, np.nan],
            'score': [90, 85, 88, 92]
        })
        df.info()
        print("\nMissing values per column:")
        print(df.isna().sum())

---

**Exercise 3.**
Create a DataFrame with a `'price'` column. Use `.min()`, `.max()`, `.idxmin()`, and `.idxmax()` to find the minimum and maximum prices along with their row indices. Verify that `df.loc[df['price'].idxmax(), 'price'] == df['price'].max()`.

??? success "Solution to Exercise 3"
    Find min/max values and their indices.

        import pandas as pd

        df = pd.DataFrame({
            'product': ['A', 'B', 'C', 'D', 'E'],
            'price': [19.99, 5.49, 42.00, 12.75, 35.50]
        })
        print("Min price:", df['price'].min(), "at index", df['price'].idxmin())
        print("Max price:", df['price'].max(), "at index", df['price'].idxmax())
        assert df.loc[df['price'].idxmax(), 'price'] == df['price'].max()
        print("Verification passed.")
