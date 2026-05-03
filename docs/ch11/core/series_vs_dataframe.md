# Series vs DataFrame

Understanding the relationship between Series and DataFrame is fundamental to working effectively with pandas. This document clarifies when to use each and how they interact.

!!! tip "Mental Model"
    A Series is one column; a DataFrame is a collection of columns sharing the same row index. Selecting a single column from a DataFrame returns a Series, and combining multiple Series side-by-side creates a DataFrame. The two types are not separate worlds -- they are the 1D and 2D faces of the same design.

## Structural Comparison

```
┌─────────────────────────────────────────────────────────────┐
│                        DataFrame                             │
│  ┌─────────┬─────────┬─────────┬─────────┐                  │
│  │ Series  │ Series  │ Series  │ Series  │  ← Columns       │
│  │ (col A) │ (col B) │ (col C) │ (col D) │                  │
│  ├─────────┼─────────┼─────────┼─────────┤                  │
│  │   1.0   │  'foo'  │  True   │  100    │  ← Row 0        │
│  │   2.0   │  'bar'  │  False  │  200    │  ← Row 1        │
│  │   3.0   │  'baz'  │  True   │  300    │  ← Row 2        │
│  └─────────┴─────────┴─────────┴─────────┘                  │
│      ↑          ↑          ↑          ↑                      │
│   float64    object      bool      int64    ← dtype per col │
└─────────────────────────────────────────────────────────────┘
```

| Aspect | Series | DataFrame |
|--------|--------|-----------|
| Dimensions | 1D (single column) | 2D (multiple columns) |
| Data types | Single dtype | Different dtype per column |
| Analogy | Excel column | Excel spreadsheet |
| NumPy equivalent | 1D array | 2D array (but heterogeneous) |

## Type Transitions

Understanding how operations change the type is crucial.

### DataFrame to Series

```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

# Single column selection -> Series
col_a = df['A']
print(type(col_a))  # <class 'pandas.core.series.Series'>

# Single row selection -> Series
row_0 = df.iloc[0]
print(type(row_0))  # <class 'pandas.core.series.Series'>

# Aggregation -> Series
col_means = df.mean()
print(type(col_means))  # <class 'pandas.core.series.Series'>
```

### Preserving DataFrame Type

```python
# Double brackets preserve DataFrame
col_a_df = df[['A']]
print(type(col_a_df))  # <class 'pandas.core.frame.DataFrame'>
print(col_a_df.shape)  # (3, 1)

# Multiple column selection -> DataFrame
subset = df[['A', 'B']]
print(type(subset))  # <class 'pandas.core.frame.DataFrame'>
```

### Series to DataFrame

```python
s = pd.Series([1, 2, 3], name='values')

# to_frame() method
df = s.to_frame()
print(type(df))  # <class 'pandas.core.frame.DataFrame'>

# reset_index() also creates DataFrame
df = s.reset_index()
print(df.columns)  # Index(['index', 'values'])
```

## Shape Differences

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Full DataFrame
print(df.shape)                  # (891, 12)

# Multiple columns -> DataFrame
print(df[["Survived", "Sex"]].shape)  # (891, 2)

# Single column with double brackets -> DataFrame
print(df[["Survived"]].shape)    # (891, 1)

# Single column with single brackets -> Series
print(df["Survived"].shape)      # (891,) - Note: 1D tuple
```

## Access Patterns

### Equivalent Operations

| Operation | DataFrame Syntax | Series Syntax |
|-----------|------------------|---------------|
| Get element | `df.loc[row, col]` | `s[label]` or `s.loc[label]` |
| Get by position | `df.iloc[i, j]` | `s.iloc[i]` |
| Boolean filter | `df[df['A'] > 0]` | `s[s > 0]` |
| Get values | `df.values` | `s.values` |

### Column-wise vs Element-wise

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# DataFrame aggregation is column-wise by default
print(df.sum())
# A     6
# B    15
# dtype: int64

s = pd.Series([1, 2, 3])

# Series aggregation is element-wise
print(s.sum())  # 6
```

## Method Behavior Differences

### Aggregations

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
s = pd.Series([1, 2, 3])

# DataFrame.mean() returns Series (one value per column)
print(df.mean())
# A    2.0
# B    5.0
# dtype: float64

# Series.mean() returns scalar
print(s.mean())  # 2.0
```

### Apply Behavior

```python
# DataFrame apply works on columns (axis=0) or rows (axis=1)
df.apply(sum, axis=0)  # Sum each column
df.apply(sum, axis=1)  # Sum each row

# Series apply works element-wise
s.apply(lambda x: x ** 2)  # Square each element
```

## Common Conversion Patterns

### Aggregation Results

```python
# groupby returns Series by default
result = df.groupby('category')['value'].sum()
print(type(result))  # Series

# Convert to DataFrame with reset_index
result_df = df.groupby('category')['value'].sum().reset_index()
print(type(result_df))  # DataFrame

# Or use to_frame with custom column name
result_df = df.groupby('category')['value'].sum().to_frame(name='total')
```

### Value Counts

```python
s = pd.Series(['a', 'b', 'a', 'c', 'a', 'b'])

# value_counts returns Series
counts = s.value_counts()
print(type(counts))  # Series

# Convert to DataFrame
counts_df = s.value_counts().reset_index()
counts_df.columns = ['value', 'count']
```

## Practical Guidelines

### When to Use Series

1. Working with a single variable
2. Time series of one measurement
3. Result of column extraction
4. Input to plotting functions expecting 1D data

```python
# Time series analysis
prices = df['Close']  # Series
returns = prices.pct_change()
rolling_mean = prices.rolling(20).mean()
```

### When to Use DataFrame

1. Multiple variables that should stay aligned
2. Tabular data with different column types
3. Data requiring row-wise operations
4. Input/output for file operations

```python
# Multi-asset analysis
portfolio = df[['AAPL', 'MSFT', 'GOOGL']]  # DataFrame
correlations = portfolio.corr()
portfolio_returns = portfolio.pct_change()
```

### Avoiding Common Mistakes

```python
# WRONG: Expecting DataFrame, getting Series
col = df['price']  # This is a Series!
col.columns  # AttributeError: 'Series' object has no attribute 'columns'

# RIGHT: Keep as DataFrame if needed
col = df[['price']]  # This is a DataFrame
col.columns  # Index(['price'], dtype='object')

# WRONG: Chained assignment warning
df[df['A'] > 0]['B'] = 1  # May not work as expected

# RIGHT: Use loc for assignment
df.loc[df['A'] > 0, 'B'] = 1
```

## Performance Considerations

| Operation | Series | DataFrame |
|-----------|--------|-----------|
| Memory | Lower (single dtype) | Higher (metadata per column) |
| Iteration | Faster | Slower |
| Vectorized ops | Optimal | Optimal |
| Type consistency | Guaranteed | Per-column |

For large-scale numerical operations, extracting to NumPy arrays may provide additional performance benefits:

```python
# Extract for numerical operations
arr = df['price'].values  # NumPy array
result = np.sqrt(arr)     # Fast NumPy operation

# Put back into pandas if needed
df['price_sqrt'] = result
```

---

## Runnable Example: `python_numpy_pandas_comparison.py`

```python
"""
Three Ways: Pure Python vs NumPy vs Pandas for Data Analysis

This tutorial solves the same sales data analysis problem three ways,
showing why NumPy and Pandas exist and how they simplify data work.

Problem: Analyze monthly sales data across 5 regions.
Tasks:
1. Monthly total sales
2. Month-over-month growth rate
3. Annual sales by region (sorted)
4. Find peak sales (month + region)
5. Find most volatile region (variance)

Based on Python-100-Days Day66-80 day01.ipynb cells.
"""

import numpy as np
import pandas as pd


# =============================================================================
# Setup: Sales Data (12 months x 5 regions, in millions)
# =============================================================================

months = [f'{i:>2d}' for i in range(1, 13)]
regions = ['East', 'West', 'North', 'South', 'Central']
sales_data = [
    [32, 17, 12, 20, 28],
    [41, 30, 17, 15, 35],
    [35, 18, 13, 11, 24],
    [12, 42, 44, 21, 34],
    [29, 11, 42, 32, 50],
    [10, 15, 11, 12, 26],
    [16, 28, 48, 22, 28],
    [31, 40, 45, 30, 39],
    [25, 41, 47, 42, 47],
    [47, 21, 13, 49, 48],
    [41, 36, 17, 36, 22],
    [22, 25, 15, 20, 37],
]


# =============================================================================
# Way 1: Pure Python (loops and comprehensions)
# =============================================================================

def pure_python_analysis():
    """Analyze sales data using only Python builtins."""
    print("=" * 50)
    print("WAY 1: Pure Python")
    print("=" * 50)

    # Task 1: Monthly totals
    monthly_totals = [sum(row) for row in sales_data]
    print("\n--- Monthly Totals ---")
    for m, total in zip(months, monthly_totals):
        print(f"  Month {m}: {total}M")

    # Task 2: Month-over-month growth
    print("\n--- Month-over-Month Growth ---")
    for i in range(1, len(monthly_totals)):
        growth = (monthly_totals[i] - monthly_totals[i-1]) / monthly_totals[i-1]
        print(f"  Month {months[i]}: {growth:>+.2%}")

    # Task 3: Annual sales by region (sorted)
    region_totals = {}
    for j, region in enumerate(regions):
        region_totals[region] = sum(sales_data[i][j] for i in range(12))
    sorted_regions = sorted(region_totals, key=lambda r: region_totals[r], reverse=True)
    print("\n--- Annual Sales by Region (sorted) ---")
    for r in sorted_regions:
        print(f"  {r}: {region_totals[r]}M")

    # Task 4: Peak sales
    max_val, max_month, max_region = 0, 0, 0
    for i in range(len(months)):
        for j in range(len(regions)):
            if sales_data[i][j] > max_val:
                max_val = sales_data[i][j]
                max_month, max_region = i, j
    print(f"\n--- Peak Sales ---")
    print(f"  Month {months[max_month]}, {regions[max_region]}: {max_val}M")

    # Task 5: Most volatile region (population variance)
    print("\n--- Most Volatile Region ---")
    max_var, most_volatile = 0, ""
    for j, region in enumerate(regions):
        values = [sales_data[i][j] for i in range(12)]
        avg = sum(values) / len(values)
        var = sum((x - avg) ** 2 for x in values) / len(values)
        if var > max_var:
            max_var, most_volatile = var, region
    print(f"  {most_volatile} (variance: {max_var:.1f})")
    print()


# =============================================================================
# Way 2: NumPy (vectorized operations with axis)
# =============================================================================

def numpy_analysis():
    """Same analysis using NumPy - vectorized, no loops."""
    print("=" * 50)
    print("WAY 2: NumPy")
    print("=" * 50)

    data = np.array(sales_data)
    print(f"\nArray shape: {data.shape}  (12 months x 5 regions)")

    # Task 1: Monthly totals - sum along axis=1 (columns)
    monthly_totals = data.sum(axis=1)
    print(f"\n--- Monthly Totals (axis=1) ---")
    print(f"  {monthly_totals}")

    # Task 2: Month-over-month growth
    mom = np.diff(monthly_totals) / monthly_totals[:-1]
    print(f"\n--- MoM Growth ---")
    print(f"  {np.round(mom * 100, 1)}%")

    # Task 3: Annual by region - sum along axis=0 (rows)
    region_totals = data.sum(axis=0)
    sorted_idx = np.argsort(region_totals)[::-1]
    print(f"\n--- Annual Sales by Region (sorted) ---")
    for idx in sorted_idx:
        print(f"  {regions[idx]}: {region_totals[idx]}M")

    # Task 4: Peak sales - argmax on flattened then unravel
    flat_idx = data.argmax()
    peak_month, peak_region = np.unravel_index(flat_idx, data.shape)
    print(f"\n--- Peak Sales ---")
    print(f"  Month {months[peak_month]}, {regions[peak_region]}: "
          f"{data[peak_month, peak_region]}M")

    # Task 5: Most volatile - variance along axis=0
    variances = data.var(axis=0)
    most_volatile = np.argmax(variances)
    print(f"\n--- Most Volatile Region ---")
    print(f"  {regions[most_volatile]} (variance: {variances[most_volatile]:.1f})")
    print(f"  All variances: {np.round(variances, 1)}")
    print()


# =============================================================================
# Way 3: Pandas (labeled data, built-in methods)
# =============================================================================

def pandas_analysis():
    """Same analysis using Pandas - labeled, expressive, chainable."""
    print("=" * 50)
    print("WAY 3: Pandas")
    print("=" * 50)

    df = pd.DataFrame(sales_data, columns=regions,
                      index=[f'Month {m}' for m in months])
    print(f"\n{df}\n")

    # Task 1: Monthly totals
    print("--- Monthly Totals (df.sum(axis=1)) ---")
    print(df.sum(axis=1))
    print()

    # Task 2: Month-over-month with pct_change()
    print("--- MoM Growth (pct_change()) ---")
    print(df.sum(axis=1).pct_change().dropna().map('{:.2%}'.format))
    print()

    # Task 3: Annual by region (sorted)
    print("--- Annual Sales by Region (sorted) ---")
    print(df.sum().sort_values(ascending=False))
    print()

    # Task 4: Peak sales with idxmax on stacked DataFrame
    stacked = df.stack()
    peak_idx = stacked.idxmax()
    print(f"--- Peak Sales ---")
    print(f"  {peak_idx[0]}, {peak_idx[1]}: {stacked[peak_idx]}M")
    print()

    # Task 5: Most volatile
    print("--- Most Volatile Region (var()) ---")
    variances = df.var(ddof=0)
    print(f"  {variances.idxmax()} (variance: {variances.max():.1f})")
    print(f"  All variances:\n{variances.round(1)}")
    print()


# =============================================================================
# Comparison Summary
# =============================================================================

def comparison_summary():
    """Compare the three approaches."""
    print("=" * 50)
    print("COMPARISON SUMMARY")
    print("=" * 50)
    print("""
    Pure Python:
      + No dependencies
      + Easy to understand
      - Verbose (many loops)
      - Slow on large data

    NumPy:
      + Fast (vectorized C operations)
      + Concise (axis-based operations)
      - Integer indexing only (no labels)
      - Homogeneous dtype

    Pandas:
      + Labeled data (named rows/columns)
      + Rich methods (pct_change, describe, groupby)
      + Handles mixed types and missing values
      + Great for tabular data
      - More memory overhead
      - Learning curve for API
    """)


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    pure_python_analysis()
    numpy_analysis()
    pandas_analysis()
    comparison_summary()
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with 3 columns. Extract one column as a Series using `df['col']` and as a single-column DataFrame using `df[['col']]`. Print the type and shape of each.

??? success "Solution to Exercise 1"
    Compare Series vs single-column DataFrame.

        import pandas as pd

        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'C': [5, 6]})
        series = df['A']
        dataframe = df[['A']]
        print(f"Series type: {type(series)}, shape: {series.shape}")
        print(f"DataFrame type: {type(dataframe)}, shape: {dataframe.shape}")

---

**Exercise 2.**
Create a Series and convert it to a DataFrame using `.to_frame()`. Then create a DataFrame and extract a row as a Series using `.loc[]`. Observe how the index of the resulting Series corresponds to the column names.

??? success "Solution to Exercise 2"
    Convert between Series and DataFrame.

        import pandas as pd

        s = pd.Series([10, 20, 30], index=['a', 'b', 'c'], name='values')
        df_from_series = s.to_frame()
        print(type(df_from_series))

        df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]}, index=['row0', 'row1'])
        row_series = df.loc['row0']
        print(row_series)
        print("Index of row Series:", row_series.index.tolist())

---

**Exercise 3.**
Demonstrate that a DataFrame can hold columns of different dtypes (int, float, string) while a Series has a single dtype. Create both and use `.dtypes` (DataFrame) and `.dtype` (Series) to verify.

??? success "Solution to Exercise 3"
    Compare dtypes in DataFrame vs dtype in Series.

        import pandas as pd

        df = pd.DataFrame({'ints': [1, 2], 'floats': [1.5, 2.5], 'strings': ['a', 'b']})
        print("DataFrame dtypes:\n", df.dtypes)
        s = df['ints']
        print(f"\nSeries dtype: {s.dtype}")
