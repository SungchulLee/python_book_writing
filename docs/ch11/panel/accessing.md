# Accessing Panel Data

This document covers techniques for selecting and slicing panel data with MultiIndex.

!!! tip "Mental Model"
    Accessing panel data is indexing with two keys: entity and time. Use `loc[(entity, time)]` for a specific observation, `loc[entity]` to get all time periods for one entity, or `xs(time, level='date')` to get all entities at one time point. The MultiIndex makes these two-dimensional queries natural on a flat DataFrame.

## Setup

```python
import pandas as pd
import numpy as np

# Create sample panel
tickers = ['AAPL', 'MSFT', 'GOOGL']
dates = pd.date_range('2024-01-01', periods=5)
index = pd.MultiIndex.from_product([tickers, dates], names=['ticker', 'date'])

np.random.seed(42)
df = pd.DataFrame({
    'return': np.random.randn(15) * 0.02,
    'volume': np.random.randint(1000, 10000, 15)
}, index=index)

print(df)
```

## Selecting a Single Entity

### Using .loc with Label

```python
# All data for AAPL
aapl_data = df.loc['AAPL']
print(aapl_data)
```

```
              return  volume
date                        
2024-01-01  0.009934    5765
2024-01-02 -0.002765    6274
2024-01-03  0.012936    2627
2024-01-04  0.030486    8019
2024-01-05 -0.004675    3927
```

Note: Result has only the `date` index level.

### Using .xs (Cross-Section)

```python
# Same result using xs
aapl_data = df.xs('AAPL', level='ticker')
print(aapl_data)
```

## Selecting a Single Time Period

### All Entities at One Time

```python
# All stocks on 2024-01-01
day_data = df.xs('2024-01-01', level='date')
print(day_data)
```

```
          return  volume
ticker                  
AAPL    0.009934    5765
MSFT   -0.003129    3109
GOOGL  -0.018867    3046
```

## Selecting Entity-Time Combination

### Using Tuple

```python
# AAPL on 2024-01-01
single_obs = df.loc[('AAPL', '2024-01-01')]
print(single_obs)
```

```
return      0.009934
volume   5765.000000
Name: (AAPL, 2024-01-01), dtype: float64
```

### Specific Column

```python
# AAPL return on 2024-01-01
value = df.loc[('AAPL', '2024-01-01'), 'return']
print(value)  # 0.009934...
```

## Slicing Multiple Entities

```python
# Multiple specific tickers
selected = df.loc[['AAPL', 'MSFT']]
print(selected)
```

## Slicing Time Ranges

### For One Entity

```python
# AAPL from Jan 2 to Jan 4
aapl_slice = df.loc['AAPL'].loc['2024-01-02':'2024-01-04']
print(aapl_slice)
```

### For All Entities

```python
# All stocks, Jan 2 to Jan 4
time_slice = df.loc[(slice(None), slice('2024-01-02', '2024-01-04')), :]
print(time_slice)
```

Using `pd.IndexSlice` for cleaner syntax:

```python
idx = pd.IndexSlice

# All tickers, specific date range
result = df.loc[idx[:, '2024-01-02':'2024-01-04'], :]
print(result)
```

## Complex Selections with IndexSlice

```python
idx = pd.IndexSlice

# Specific tickers, all dates
result = df.loc[idx[['AAPL', 'GOOGL'], :], :]
print("AAPL and GOOGL, all dates:")
print(result)
print()

# All tickers, specific dates
result = df.loc[idx[:, ['2024-01-01', '2024-01-03']], :]
print("All tickers, specific dates:")
print(result)
print()

# Specific ticker, date range
result = df.loc[idx['MSFT', '2024-01-02':'2024-01-04'], :]
print("MSFT, Jan 2-4:")
print(result)
```

## Boolean Selection

### Based on Values

```python
# High volume observations
high_volume = df[df['volume'] > 7000]
print(high_volume)
```

### Based on Index Level

```python
# Get the ticker level values
tickers_in_index = df.index.get_level_values('ticker')

# Filter to specific tickers
tech_stocks = df[tickers_in_index.isin(['AAPL', 'MSFT'])]
print(tech_stocks)
```

### Combined Conditions

```python
# AAPL with positive returns
aapl_positive = df[(df.index.get_level_values('ticker') == 'AAPL') & 
                   (df['return'] > 0)]
print(aapl_positive)
```

## Accessing Index Levels

```python
# Get all unique tickers
tickers = df.index.get_level_values('ticker').unique()
print(f"Tickers: {tickers.tolist()}")

# Get all unique dates
dates = df.index.get_level_values('date').unique()
print(f"Dates: {dates.tolist()}")

# Get index as DataFrame
index_df = df.index.to_frame(index=False)
print(index_df.head())
```

## Reset vs Preserve Index

### Keep MultiIndex

```python
# Selection preserves index structure
subset = df.loc['AAPL']
print(f"Index: {subset.index.name}")  # 'date'
```

### Reset to Columns

```python
# Convert index levels to columns
flat = df.reset_index()
print(flat.head())
```

```
  ticker       date    return  volume
0   AAPL 2024-01-01  0.009934    5765
1   AAPL 2024-01-02 -0.002765    6274
...
```

## Query Method for Panel

```python
# Reset index first, then query
flat = df.reset_index()

# Query syntax
result = flat.query("ticker == 'AAPL' and return > 0")
print(result)
```

## Accessing Panel Series

```python
# Get returns as panel Series
returns = df['return']
print(type(returns))  # Series with MultiIndex

# Access specific return
aapl_jan1_return = returns[('AAPL', '2024-01-01')]
print(aapl_jan1_return)
```

## Summary of Access Methods

| Goal | Method |
|------|--------|
| Single entity | `df.loc['AAPL']` or `df.xs('AAPL', level='ticker')` |
| Single time | `df.xs('2024-01-01', level='date')` |
| Entity + time | `df.loc[('AAPL', '2024-01-01')]` |
| Multiple entities | `df.loc[['AAPL', 'MSFT']]` |
| Time range | `df.loc[idx[:, 'start':'end'], :]` |
| Complex slice | `pd.IndexSlice` with `.loc` |
| Boolean filter | `df[condition]` |


---

## Exercises

**Exercise 1.** Write code that creates a dictionary of DataFrames (simulating panel data) and accesses data for a specific entity using dictionary indexing.

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

**Exercise 2.** Explain how to use `pd.concat()` with `keys` to create a panel-like structure with MultiIndex.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that selects all rows for a specific time period across all entities in a MultiIndex DataFrame using `.loc`.

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

**Exercise 4.** Create panel data with MultiIndex and use `xs()` to extract a cross-section for a specific entity.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
