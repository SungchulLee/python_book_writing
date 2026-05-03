# merge vs join

pandas provides two methods for combining DataFrames: `merge()` and `join()`. Understanding their differences is essential for data wrangling.

!!! tip "Mental Model"
    `merge` and `join` do the same thing under the hood -- they differ in defaults. `merge` matches on columns (inner join). `join` matches on the index (left join). Pick whichever matches where your keys live: columns for `merge`, index for `join`.

## Key Differences

merge and join serve different purposes.

### 1. merge Uses Columns

```python
import pandas as pd

df1 = pd.DataFrame({
    'key': ['A', 'B', 'C'],
    'value1': [1, 2, 3]
})

df2 = pd.DataFrame({
    'key': ['A', 'B', 'D'],
    'value2': [4, 5, 6]
})

# merge on column
pd.merge(df1, df2, on='key')
```

### 2. join Uses Index

```python
df1 = pd.DataFrame({
    'value1': [1, 2, 3]
}, index=['A', 'B', 'C'])

df2 = pd.DataFrame({
    'value2': [4, 5, 6]
}, index=['A', 'B', 'D'])

# join on index
df1.join(df2)
```

### 3. Comparison Table

| Feature | merge | join |
|---------|-------|------|
| Join key | Column values | Index labels |
| Syntax | `pd.merge(df1, df2)` | `df1.join(df2)` |
| Default | Inner join | Left join |
| Flexibility | More options | Simpler API |

## When to Use merge

Choose merge for column-based joins.

### 1. Foreign Key Relationships

```python
orders = pd.DataFrame({
    'order_id': [1, 2, 3],
    'customer_id': [101, 102, 101],
    'amount': [100, 200, 150]
})

customers = pd.DataFrame({
    'customer_id': [101, 102, 103],
    'name': ['Alice', 'Bob', 'Carol']
})

pd.merge(orders, customers, on='customer_id')
```

### 2. Different Column Names

```python
pd.merge(df1, df2, left_on='id', right_on='customer_id')
```

### 3. Multiple Join Keys

```python
pd.merge(df1, df2, on=['key1', 'key2'])
```

## When to Use join

Choose join for index-based operations.

### 1. Time Series Alignment

```python
import yfinance as yf

aapl = yf.Ticker('AAPL').history(period='1y')[['Close']].rename(
    columns={'Close': 'AAPL'}
)
msft = yf.Ticker('MSFT').history(period='1y')[['Close']].rename(
    columns={'Close': 'MSFT'}
)

portfolio = aapl.join(msft, how='inner')
```

### 2. Multiple DataFrames

```python
# Join multiple DataFrames by index
df1.join([df2, df3, df4])
```

### 3. Suffix Handling

```python
df1.join(df2, lsuffix='_left', rsuffix='_right')
```

## Four Join Types

Both methods support the same join types.

### 1. Inner Join

```python
pd.merge(df1, df2, on='key', how='inner')  # Only matching
df1.join(df2, how='inner')
```

### 2. Left Join

```python
pd.merge(df1, df2, on='key', how='left')   # All from left
df1.join(df2, how='left')  # Default for join
```

### 3. Right Join

```python
pd.merge(df1, df2, on='key', how='right')  # All from right
df1.join(df2, how='right')
```

### 4. Outer Join

```python
pd.merge(df1, df2, on='key', how='outer')  # All rows
df1.join(df2, how='outer')
```

## Visual Comparison

Four ways of combining two DataFrames.

### 1. Sample DataFrames

```python
df1 = pd.DataFrame({'city': ['NY', 'SF', 'LA'], 'temp': [21, 14, 35]})
df2 = pd.DataFrame({'city': ['SF', 'NY', 'ICN'], 'humidity': [65, 68, 75]})
```

### 2. Inner (Intersection)

```python
pd.merge(df1, df2, on='city', how='inner')
# Only NY and SF
```

### 3. Outer (Union)

```python
pd.merge(df1, df2, on='city', how='outer')
# NY, SF, LA, ICN (with NaN for missing)
```

## Practical Guidelines

Choose the right method for your use case.

### 1. Use merge When

- Joining on column values (foreign keys)
- Column names differ between DataFrames
- Need fine-grained control over join

### 2. Use join When

- DataFrames share a meaningful index
- Combining time series data
- Simple index-based combination

### 3. Performance

Both methods have similar performance; choose based on data structure.

---

## Exercises

**Exercise 1.**
Create two DataFrames with a shared column `'key'`. Combine them using `pd.merge()`. Then set `'key'` as the index of both and use `.join()` to achieve the same result. Compare the outputs.

??? success "Solution to Exercise 1"
    Achieve the same result with merge and join.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'val1': [1, 2, 3]})
        df2 = pd.DataFrame({'key': ['a', 'b', 'c'], 'val2': [4, 5, 6]})
        result_merge = pd.merge(df1, df2, on='key')
        result_join = df1.set_index('key').join(df2.set_index('key'))
        print("merge:\n", result_merge)
        print("join:\n", result_join)

---

**Exercise 2.**
Demonstrate the different default behaviors: show that `pd.merge()` defaults to an inner join while `.join()` defaults to a left join, using the same pair of DataFrames.

??? success "Solution to Exercise 2"
    Show different default join types.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'v1': [1, 2, 3]})
        df2 = pd.DataFrame({'key': ['a', 'b', 'd'], 'v2': [4, 5, 6]})
        print("merge (default inner):")
        print(pd.merge(df1, df2, on='key'))
        print("\njoin (default left):")
        print(df1.set_index('key').join(df2.set_index('key')))

---

**Exercise 3.**
Identify a scenario where `pd.merge()` is clearly better than `.join()` (e.g., joining on columns with different names) and another where `.join()` is clearly better (e.g., joining multiple DataFrames by index). Implement both.

??? success "Solution to Exercise 3"
    Show when merge is better and when join is better.

        import pandas as pd

        # merge is better: different key column names
        df1 = pd.DataFrame({'emp_id': [1, 2], 'name': ['Alice', 'Bob']})
        df2 = pd.DataFrame({'employee_id': [1, 2], 'dept': ['HR', 'IT']})
        print("merge with different key names:")
        print(pd.merge(df1, df2, left_on='emp_id', right_on='employee_id'))

        # join is better: multiple DataFrames by index
        a = pd.DataFrame({'A': [1, 2]}, index=['x', 'y'])
        b = pd.DataFrame({'B': [3, 4]}, index=['x', 'y'])
        c = pd.DataFrame({'C': [5, 6]}, index=['x', 'y'])
        print("\njoin multiple DataFrames:")
        print(a.join([b, c]))
