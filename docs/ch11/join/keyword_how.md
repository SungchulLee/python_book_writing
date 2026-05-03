# Keyword - how

The `how` parameter in `join()` specifies the type of join, controlling which rows are included based on index matching.

!!! tip "Mental Model"
    `how` answers "which rows survive the join?" Left keeps all rows from the caller, right keeps all from the other, inner keeps only matches, and outer keeps everything. Unmatched cells are filled with NaN. Visualize two overlapping circles: `how` controls which parts of the Venn diagram you keep.

## Left Join (Default)

Keep all rows from the calling DataFrame.

### 1. Default Behavior

```python
import pandas as pd
import yfinance as yf

def download(ticker):
    return yf.Ticker(ticker).history(period="max")

tickers = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOG']

for i, ticker in enumerate(tickers):
    if i == 0:
        df = download(ticker).rename(columns={'Close': ticker})[[ticker]]
    else:
        dg = download(ticker).rename(columns={'Close': ticker})[[ticker]]
        df = df.join(dg, how="left")  # Default

print(df.head(3))
```

### 2. Preserves Left Index

All dates from the first stock are kept.

### 3. NaN for Missing

Stocks without data for certain dates have NaN.

## Right Join

Keep all rows from the passed DataFrame.

### 1. Right Join Example

```python
for i, ticker in enumerate(tickers):
    if i == 0:
        df = download(ticker).rename(columns={'Close': ticker})[[ticker]]
    else:
        dg = download(ticker).rename(columns={'Close': ticker})[[ticker]]
        df = df.join(dg, how="right")

print(df.head(3))
```

### 2. Preserves Right Index

All dates from the joined stock are kept.

### 3. Use Case

When the right DataFrame has the authoritative index.

## Inner Join

Keep only rows with matching indices.

### 1. Inner Join Example

```python
for i, ticker in enumerate(tickers):
    if i == 0:
        df = download(ticker).rename(columns={'Close': ticker})[[ticker]]
    else:
        dg = download(ticker).rename(columns={'Close': ticker})[[ticker]]
        df = df.join(dg, how="inner")

print(df.head(3))
print(df.tail(3))
```

### 2. Intersection of Indices

Only dates present in all stocks.

### 3. No Missing Values

Inner join produces complete data without NaN.

## Outer Join

Keep all rows from both DataFrames.

### 1. Outer Join Example

```python
for i, ticker in enumerate(tickers):
    if i == 0:
        df = download(ticker).rename(columns={'Close': ticker})[[ticker]]
    else:
        dg = download(ticker).rename(columns={'Close': ticker})[[ticker]]
        df = df.join(dg, how="outer")

print(df.head(3))
print(df.tail(3))
```

### 2. Union of Indices

All dates from any stock are included.

### 3. Most Missing Values

Outer join may have many NaN values.

## Comparison

Summary of join types.

### 1. Row Counts

```python
# Given df1 (100 dates) and df2 (80 dates) with 60 overlap:
# how='left':  100 rows (all from df1)
# how='right':  80 rows (all from df2)
# how='inner':  60 rows (intersection)
# how='outer': 120 rows (union)
```

### 2. Best Practices

```python
# Inner: When you need complete data
# Left: When preserving primary DataFrame structure
# Outer: When you need all dates for analysis
```

### 3. Financial Context

```python
# Inner join for synchronized analysis
# Outer join for data completeness check
# Left join for preserving benchmark dates
```

---

## Exercises

**Exercise 1.**
Create two DataFrames with partially overlapping indices (e.g., 5 indices each with 3 in common). Perform all four join types (`left`, `right`, `inner`, `outer`) and print the row count of each result. Verify that inner gives the fewest rows and outer gives the most.

??? success "Solution to Exercise 1"
    Compare row counts across all four join types.

        import pandas as pd

        df1 = pd.DataFrame({'A': range(5)}, index=['a', 'b', 'c', 'd', 'e'])
        df2 = pd.DataFrame({'B': range(5)}, index=['c', 'd', 'e', 'f', 'g'])
        for how in ['left', 'right', 'inner', 'outer']:
            result = df1.join(df2, how=how)
            print(f"{how}: {len(result)} rows")

---

**Exercise 2.**
Create two DataFrames representing monthly sales data for different regions, where some months are missing in each. Use an inner join to get only the months with data in both regions. Confirm there are no `NaN` values in the result.

??? success "Solution to Exercise 2"
    Inner join to get months with data in both regions.

        import pandas as pd

        region_a = pd.DataFrame(
            {'sales_a': [100, 200, 300]},
            index=pd.Index(['Jan', 'Feb', 'Mar'], name='month')
        )
        region_b = pd.DataFrame(
            {'sales_b': [150, 250, 350]},
            index=pd.Index(['Feb', 'Mar', 'Apr'], name='month')
        )
        result = region_a.join(region_b, how='inner')
        print(result)
        assert result.isna().sum().sum() == 0
        print("No NaN values in inner join result.")

---

**Exercise 3.**
Using the same two DataFrames from Exercise 2, perform an outer join. Count the `NaN` values per column and use `.fillna(0)` to replace them. Print the result before and after filling.

??? success "Solution to Exercise 3"
    Outer join with NaN counting and filling.

        import pandas as pd

        region_a = pd.DataFrame(
            {'sales_a': [100, 200, 300]},
            index=pd.Index(['Jan', 'Feb', 'Mar'], name='month')
        )
        region_b = pd.DataFrame(
            {'sales_b': [150, 250, 350]},
            index=pd.Index(['Feb', 'Mar', 'Apr'], name='month')
        )
        result = region_a.join(region_b, how='outer')
        print("Before fillna:")
        print(result)
        print("\nNaN per column:", result.isna().sum().to_dict())
        result = result.fillna(0)
        print("\nAfter fillna:")
        print(result)
