# Sorting by Index and Values

pandas provides methods to sort DataFrames and Series by their index labels or column values.

!!! tip "Mental Model"
    `sort_values` reorders rows by the data in one or more columns -- like clicking a column header in a spreadsheet. `sort_index` reorders rows by their index labels. Both return a new DataFrame by default and support `ascending=False` for descending order.

## sort_index Method

Sort by row or column labels.

### 1. Sort Rows by Index

```python
import pandas as pd

df = pd.DataFrame({
    'A': [3, 1, 2],
    'B': [6, 4, 5]
}, index=['c', 'a', 'b'])

df.sort_index()
```

```
   A  B
a  1  4
b  2  5
c  3  6
```

### 2. Descending Order

```python
df.sort_index(ascending=False)
```

```
   A  B
c  3  6
b  2  5
a  1  4
```

### 3. Sort Columns

```python
df = pd.DataFrame({
    'C': [1, 2],
    'A': [3, 4],
    'B': [5, 6]
})

df.sort_index(axis=1)  # Sort columns alphabetically
```

## sort_values Method

Sort by values in specified columns.

### 1. Single Column

```python
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Carol'],
    'Age': [30, 25, 35]
})

df.sort_values(by='Age')
```

```
    Name  Age
1    Bob   25
0  Alice   30
2  Carol   35
```

### 2. Multiple Columns

```python
df = pd.DataFrame({
    'Dept': ['A', 'B', 'A', 'B'],
    'Name': ['Alice', 'Bob', 'Carol', 'Dave'],
    'Salary': [50000, 60000, 55000, 60000]
})

df.sort_values(by=['Dept', 'Salary'])
```

### 3. Mixed Order

```python
df.sort_values(
    by=['Dept', 'Salary'],
    ascending=[True, False]  # Dept ascending, Salary descending
)
```

## Series Sorting

Sort Series by index or values.

### 1. Sort by Values

```python
s = pd.Series([3, 1, 4, 1, 5], index=['a', 'b', 'c', 'd', 'e'])
s.sort_values()
```

```
b    1
d    1
a    3
c    4
e    5
dtype: int64
```

### 2. Sort by Index

```python
s.sort_index()
```

### 3. Get Sorted Index

```python
s.argsort()  # Returns positions for sorting
```

## Handling NaN

Control how missing values are sorted.

### 1. NaN at End (Default)

```python
df = pd.DataFrame({
    'A': [3, None, 1, 2]
})

df.sort_values(by='A')  # NaN at end
```

### 2. NaN at Beginning

```python
df.sort_values(by='A', na_position='first')
```

### 3. Drop NaN Before Sorting

```python
df.dropna().sort_values(by='A')
```

## Ranking

Assign ranks to values.

### 1. Basic Ranking

```python
df = pd.DataFrame({
    'Score': [85, 90, 85, 95]
})

df['Rank'] = df['Score'].rank(ascending=False)
```

### 2. Ranking Methods

```python
# method='average' (default): average rank for ties
# method='min': lowest rank for ties
# method='max': highest rank for ties
# method='first': ranks by order of appearance
# method='dense': like 'min', but ranks always increase by 1
```

### 3. Dense Ranking Example

```python
df['DenseRank'] = df['Score'].rank(ascending=False, method='dense')
```

## Practical Examples

Common sorting scenarios.

### 1. Top N Values with nlargest

The `nlargest()` method is more efficient than `sort_values().head()` for finding top N values.

```python
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Carol', 'David', 'Eve'],
    'Salary': [75000, 60000, 90000, 55000, 85000],
    'Experience': [5, 3, 8, 2, 6]
})

# Get top 3 highest salaries
top_earners = df.nlargest(3, 'Salary')
print(top_earners)
```

```
    Name  Salary  Experience
2  Carol   90000           8
4    Eve   85000           6
0  Alice   75000           5
```

### 2. Bottom N Values with nsmallest

```python
# Get 3 employees with least experience
newest = df.nsmallest(3, 'Experience')
print(newest)
```

```
    Name  Salary  Experience
3  David   55000           2
1    Bob   60000           3
0  Alice   75000           5
```

### 3. Multiple Columns in nlargest/nsmallest

```python
# Top 3 by salary, then by experience (tie-breaker)
df.nlargest(3, ['Salary', 'Experience'])

# Equivalent to sorting by multiple columns
df.sort_values(['Salary', 'Experience'], ascending=[False, False]).head(3)
```

### 4. Performance Comparison

```python
import time
import numpy as np

# Large DataFrame
large_df = pd.DataFrame({
    'value': np.random.randn(1_000_000)
})

# Method 1: sort_values + head (slower)
start = time.time()
result1 = large_df.sort_values('value', ascending=False).head(10)
sort_time = time.time() - start

# Method 2: nlargest (faster)
start = time.time()
result2 = large_df.nlargest(10, 'value')
nlargest_time = time.time() - start

print(f"sort_values + head: {sort_time:.3f}s")
print(f"nlargest: {nlargest_time:.3f}s")
print(f"Speedup: {sort_time/nlargest_time:.1f}x")
```

Typical result: `nlargest` is 5-10x faster for large DataFrames with small N.

### 5. Series nlargest and nsmallest

```python
s = pd.Series([3, 1, 4, 1, 5, 9, 2, 6], index=list('abcdefgh'))

# Top 3 values
print(s.nlargest(3))
```

```
f    9
h    6
e    5
dtype: int64
```

```python
# Bottom 3 values
print(s.nsmallest(3))
```

```
b    1
d    1
g    2
dtype: int64
```

### 6. Financial Example: Top Performers

```python
import yfinance as yf

# Get stock data
tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META', 'NVDA', 'TSLA']
returns = {}

for ticker in tickers:
    data = yf.Ticker(ticker).history(period='1y')
    returns[ticker] = (data['Close'].iloc[-1] / data['Close'].iloc[0]) - 1

returns_df = pd.DataFrame({
    'Ticker': list(returns.keys()),
    'Annual_Return': list(returns.values())
})

# Top 3 performers
print("Top 3 Performers:")
print(returns_df.nlargest(3, 'Annual_Return'))

# Bottom 3 performers
print("\nBottom 3 Performers:")
print(returns_df.nsmallest(3, 'Annual_Return'))
```

### 7. Keep Parameter (Handling Duplicates)

```python
df = pd.DataFrame({
    'name': ['A', 'B', 'C', 'D'],
    'value': [10, 20, 20, 30]  # B and C have same value
})

# 'first' (default): keep first occurrence
print(df.nlargest(3, 'value', keep='first'))

# 'last': keep last occurrence
print(df.nlargest(3, 'value', keep='last'))

# 'all': keep all duplicates (may return more than n rows)
print(df.nlargest(3, 'value', keep='all'))
```

### 8. Combining with groupby

```python
df = pd.DataFrame({
    'department': ['Sales', 'Sales', 'IT', 'IT', 'HR', 'HR'],
    'employee': ['A', 'B', 'C', 'D', 'E', 'F'],
    'salary': [50000, 55000, 70000, 65000, 45000, 48000]
})

# Top 1 earner per department
top_per_dept = df.groupby('department').apply(
    lambda x: x.nlargest(1, 'salary')
).reset_index(drop=True)
print(top_per_dept)
```

### 9. Reset Index After Sort

```python
df_sorted = df.sort_values('Age').reset_index(drop=True)
```

## Key Parameter

Custom sort using a key function.

### 1. Case-insensitive Sort

```python
df.sort_values(by='Name', key=lambda x: x.str.lower())
```

### 2. String Length Sort

```python
df.sort_values(by='Name', key=lambda x: x.str.len())
```

### 3. Custom Transform

```python
df.sort_values(by='Value', key=lambda x: abs(x))
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with columns `'name'`, `'age'`, and `'score'`. Sort by `'score'` in descending order using `sort_values()`. Then sort by `'age'` ascending and `'score'` descending simultaneously.

??? success "Solution to Exercise 1"
    Sort by one or multiple columns.

        import pandas as pd

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Carol', 'Dave'],
            'age': [30, 25, 30, 25],
            'score': [85, 90, 78, 92]
        })
        print(df.sort_values('score', ascending=False))
        print(df.sort_values(['age', 'score'], ascending=[True, False]))

---

**Exercise 2.**
Create a DataFrame with a non-sequential index (e.g., `[5, 2, 8, 1, 3]`). Use `sort_index()` to sort rows by the index. Then sort the columns alphabetically using `sort_index(axis=1)`.

??? success "Solution to Exercise 2"
    Sort by index and by columns.

        import pandas as pd

        df = pd.DataFrame(
            {'C': [1, 2, 3, 4, 5], 'A': [6, 7, 8, 9, 10], 'B': [11, 12, 13, 14, 15]},
            index=[5, 2, 8, 1, 3]
        )
        print("Sort by index:")
        print(df.sort_index())
        print("\nSort columns:")
        print(df.sort_index(axis=1))

---

**Exercise 3.**
Create a DataFrame with some `NaN` values in a column. Use `sort_values()` with `na_position='first'` to place `NaN` rows at the top, then with `na_position='last'` to place them at the bottom. Compare the two results.

??? success "Solution to Exercise 3"
    Control NaN position in sorted output.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Carol', 'Dave'],
            'score': [85, np.nan, 78, np.nan]
        })
        print("NaN first:")
        print(df.sort_values('score', na_position='first'))
        print("\nNaN last:")
        print(df.sort_values('score', na_position='last'))
