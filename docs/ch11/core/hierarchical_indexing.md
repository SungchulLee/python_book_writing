# Hierarchical Indexing

Hierarchical indexing (also called MultiIndex) enables you to store and manipulate data with multiple levels of indexing. This is essential for working with higher-dimensional data in a 2D DataFrame structure.

!!! tip "Mental Model"
    A MultiIndex is a tree of labels on the row (or column) axis. Instead of a flat list like `[0, 1, 2]`, you get nested levels like `(country, city)`. This lets a 2D DataFrame represent 3D or higher-dimensional data by encoding extra dimensions into the index, without needing separate tables.

## Conceptual Overview

```
                        temperature  humidity
country  city                                
india    mumbai               32        70
         delhi                45        60
us       new york             21        68
         chicago              14        65
         ↑          ↑
      Level 0   Level 1
```

Hierarchical indexing allows you to:

- Represent 3D+ data in a 2D structure
- Perform grouped operations efficiently
- Select data at different levels of granularity

## Creating Hierarchical Indexes

### Using pd.concat with keys

```python
import pandas as pd

# Create separate DataFrames
india = pd.DataFrame({
    "city": ["mumbai", "delhi"],
    "temperature": [32, 45],
    "humidity": [70, 60],
}).set_index('city')

us = pd.DataFrame({
    "city": ["new york", "chicago"],
    "temperature": [21, 14],
    "humidity": [68, 65],
}).set_index('city')

# Concatenate with hierarchical keys
df = pd.concat([india, us], keys=["india", "us"])
print(df)
```

```
                  temperature  humidity
india mumbai              32        70
      delhi               45        60
us    new york            21        68
      chicago             14        65
```

### Using MultiIndex.from_tuples

```python
index = pd.MultiIndex.from_tuples([
    ('india', 'mumbai'),
    ('india', 'delhi'),
    ('us', 'new york'),
    ('us', 'chicago')
], names=['country', 'city'])

df = pd.DataFrame({
    'temperature': [32, 45, 21, 14],
    'humidity': [70, 60, 68, 65]
}, index=index)
```

### Using MultiIndex.from_product

Creates a MultiIndex from the Cartesian product of iterables.

```python
countries = ['india', 'us']
metrics = ['temperature', 'humidity']

index = pd.MultiIndex.from_product(
    [countries, metrics],
    names=['country', 'metric']
)
print(index)
```

```
MultiIndex([('india', 'temperature'),
            ('india', 'humidity'),
            ('us', 'temperature'),
            ('us', 'humidity')],
           names=['country', 'metric'])
```

### Using MultiIndex.from_arrays

```python
arrays = [
    ['india', 'india', 'us', 'us'],
    ['mumbai', 'delhi', 'new york', 'chicago']
]

index = pd.MultiIndex.from_arrays(arrays, names=['country', 'city'])
```

## Selecting Data with MultiIndex

### Using loc with Tuples (Recommended)

```python
df = pd.concat([india, us], keys=["india", "us"])

# Select specific country and city
print(df.loc[("us", "new york")])
```

```
temperature    21
humidity       68
Name: (us, new york), dtype: int64
```

### Selecting an Entire Level

```python
# Select all cities in 'us'
print(df.loc["us"])
```

```
          temperature  humidity
city                           
new york           21        68
chicago            14        65
```

### Avoid Chained Indexing

```python
# NOT RECOMMENDED - Chained indexing
df.loc["us"].loc["new york"]

# RECOMMENDED - Single tuple access
df.loc[("us", "new york")]
```

**Why avoid chained indexing?**

- `df.loc["us"]` creates an intermediate DataFrame
- pandas treats these as separate operations
- Can lead to unpredictable behavior with assignments
- Single tuple access is faster and clearer

## Hierarchical Columns

MultiIndex can also be applied to columns.

```python
df = pd.DataFrame(
    [[1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12]],
    columns=pd.MultiIndex.from_product(
        [['one', 'two'], ['first', 'second']]
    )
)
print(df)
```

```
  one        two       
  first second first second
0     1      2     3      4
1     5      6     7      8
2     9     10    11     12
```

### Accessing Hierarchical Columns

```python
# Select top-level column group
print(df['one'])
```

```
   first  second
0      1       2
1      5       6
2      9      10
```

```python
# Select specific nested column - use tuple
print(df[('one', 'second')])
```

```
0     2
1     6
2    10
Name: (one, second), dtype: int64
```

### Avoid Chained Column Access

```python
# NOT RECOMMENDED
df['one']['second']

# RECOMMENDED
df.loc[:, ('one', 'second')]
```

## MultiIndex Operations

### Swapping Levels

```python
df = pd.concat([india, us], keys=["india", "us"])

# Swap the order of index levels
df_swapped = df.swaplevel()
print(df_swapped)
```

```
                  temperature  humidity
mumbai   india             32        70
delhi    india             45        60
new york us                21        68
chicago  us                14        65
```

### Reordering Levels

For MultiIndex with more than 2 levels, use `reorder_levels()`.

```python
# Create 3-level MultiIndex
index = pd.MultiIndex.from_tuples([
    ('2024', 'Q1', 'Jan'),
    ('2024', 'Q1', 'Feb'),
    ('2024', 'Q2', 'Apr'),
    ('2024', 'Q2', 'May')
], names=['year', 'quarter', 'month'])

df = pd.DataFrame({'value': [10, 20, 30, 40]}, index=index)
print(df)
```

```
                        value
year quarter month           
2024 Q1      Jan          10
             Feb          20
     Q2      Apr          30
             May          40
```

```python
# Reorder to: month, year, quarter
df_reordered = df.reorder_levels(['month', 'year', 'quarter'])
print(df_reordered)
```

```
                        value
month year quarter           
Jan   2024 Q1             10
Feb   2024 Q1             20
Apr   2024 Q2             30
May   2024 Q2             40
```

```python
# Use integer positions
df_reordered = df.reorder_levels([2, 0, 1])  # Same result

# Sort after reordering for proper order
df_reordered = df.reorder_levels(['month', 'year', 'quarter']).sort_index()
```

### Sorting by Index

```python
# Sort by all levels
df_sorted = df.sort_index()

# Sort by specific level
df_sorted = df.sort_index(level='city')
```

### Resetting Index

```python
# Convert MultiIndex to columns
df_reset = df.reset_index()
print(df_reset)
```

```
  level_0    level_1  temperature  humidity
0   india     mumbai           32        70
1   india      delhi           45        60
2      us   new york           21        68
3      us    chicago           14        65
```

### Setting MultiIndex from Columns

```python
df_reset.set_index(['level_0', 'level_1'], inplace=True)
df_reset.index.names = ['country', 'city']
```

## Cross-Section Selection with xs

The `xs` method provides a convenient way to select data at a particular level.

```python
df = pd.concat([india, us], keys=["india", "us"])

# Select all rows where level 0 is 'india'
print(df.xs('india', level=0))
```

```
        temperature  humidity
city                         
mumbai           32        70
delhi            45        60
```

```python
# Select all rows where city is 'delhi' (level 1)
print(df.xs('delhi', level=1))
```

```
         temperature  humidity
country                       
india             45        60
```

## Aggregation with MultiIndex

### GroupBy on Index Levels

```python
# Aggregate by country (level 0)
print(df.groupby(level=0).mean())
```

```
         temperature  humidity
country                       
india           38.5      65.0
us              17.5      66.5
```

### Using level parameter in aggregations

```python
# Sum across level 0
print(df.sum(level=0))  # Deprecated in newer pandas

# Modern approach
print(df.groupby(level=0).sum())
```

## Financial Example: Multi-Asset Time Series

```python
import pandas as pd
import numpy as np

# Create multi-asset price data
dates = pd.date_range('2024-01-01', periods=5)
assets = ['AAPL', 'MSFT']
metrics = ['open', 'high', 'low', 'close']

# Create MultiIndex columns
columns = pd.MultiIndex.from_product([assets, metrics])

# Random price data
np.random.seed(42)
data = np.random.randn(5, 8).cumsum(axis=0) + 100

df = pd.DataFrame(data, index=dates, columns=columns)
print(df.round(2))
```

```
            AAPL                          MSFT                        
            open   high    low  close     open   high    low  close
2024-01-01 100.50 100.86 101.51 103.02  100.31  99.85  99.38 100.95
2024-01-02 101.27 100.58 101.99 103.81  100.82 100.00  99.97 101.12
...
```

### Selecting Asset Data

```python
# Get all AAPL data
aapl_data = df['AAPL']

# Get close prices for all assets
close_prices = df.xs('close', level=1, axis=1)
print(close_prices)
```

## Index Attributes

### names

```python
df = pd.concat([india, us], keys=["india", "us"])
print(df.index.names)  # [None, 'city']

# Set names
df.index.names = ['country', 'city']
```

### levels

```python
print(df.index.levels)
# FrozenList([['india', 'us'], ['chicago', 'delhi', 'mumbai', 'new york']])
```

### nlevels

```python
print(df.index.nlevels)  # 2
```

## Best Practices

1. **Use tuple indexing** instead of chained indexing for clarity and performance
2. **Name your index levels** for self-documenting code
3. **Sort the index** after creation for better performance with `loc`
4. **Consider alternatives** - sometimes separate columns are clearer than MultiIndex
5. **Use xs()** for cleaner cross-section selection

```python
# Good: Clear, named, sorted MultiIndex
df.index.names = ['country', 'city']
df = df.sort_index()
result = df.loc[('us', 'chicago'), 'temperature']

# Avoid: Unnamed, unsorted, chained access
result = df.loc['us'].loc['chicago']['temperature']
```

---

## Runnable Example: `multiindex_tutorial.py`

```python
"""
Pandas Tutorial: Multi-Index (Hierarchical Indexing).

Covers creating and working with multi-level indices.
"""

import pandas as pd
import numpy as np

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("="*70)
    print("MULTI-INDEX (HIERARCHICAL INDEXING)")
    print("="*70)

    # Create multi-index DataFrame
    np.random.seed(42)
    index = pd.MultiIndex.from_product([
        ['Store1', 'Store2', 'Store3'],
        ['Product A', 'Product B']
    ], names=['Store', 'Product'])

    df = pd.DataFrame({
        'Sales': np.random.randint(100, 1000, 6),
        'Quantity': np.random.randint(10, 100, 6)
    }, index=index)

    print("\nMulti-Index DataFrame:")
    print(df)

    # Selecting with multi-index
    print("\n1. Select by outer index (Store1):")
    print(df.loc['Store1'])

    print("\n2. Select by both indices (Store1, Product A):")
    print(df.loc[('Store1', 'Product A')])

    print("\n3. Select using slice:")
    print(df.loc[('Store1', slice(None)), :])

    # Stack/Unstack
    print("\n4. Unstack (inner index to columns):")
    unstacked = df.unstack()
    print(unstacked)

    print("\n5. Stack back:")
    stacked = unstacked.stack()
    print(stacked)

    # Swap levels
    print("\n6. Swap index levels:")
    swapped = df.swaplevel()
    print(swapped)

    # Sort by index
    print("\n7. Sort by index:")
    sorted_df = swapped.sort_index()
    print(sorted_df)

    # Reset index
    print("\n8. Reset multi-index to columns:")
    reset = df.reset_index()
    print(reset)

    # Set multi-index from columns
    print("\n9. Create multi-index from columns:")
    df_flat = pd.DataFrame({
        'Store': ['A', 'A', 'B', 'B'],
        'Product': ['X', 'Y', 'X', 'Y'],
        'Sales': [100, 200, 150, 250]
    })
    print("Flat DataFrame:")
    print(df_flat)

    df_multi = df_flat.set_index(['Store', 'Product'])
    print("\nWith Multi-Index:")
    print(df_multi)

    # Aggregation with multi-index
    print("\n10. Aggregation by level:")
    print("Sum by Store:")
    print(df.sum(level='Store'))

    print("\nMean by Product:")
    print(df.mean(level='Product'))

    print("\nKEY TAKEAWAYS:")
    print("- MultiIndex: Hierarchical row/column indices")
    print("- Create with from_product(), from_tuples(), from_arrays()")
    print("- Select with loc[] using tuples")
    print("- unstack(): Move index level to columns")
    print("- stack(): Move column level to index")
    print("- swaplevel(): Swap index levels")
    print("- Aggregate by specific levels")
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with a MultiIndex from tuples (e.g., `('US', 'NYC')`, `('US', 'LA')`, `('UK', 'London')`). Use `.loc[]` to select all rows for a specific level-0 value (e.g., `'US'`).

??? success "Solution to Exercise 1"
    Select from a MultiIndex using loc.

        import pandas as pd

        idx = pd.MultiIndex.from_tuples([
            ('US', 'NYC'), ('US', 'LA'), ('UK', 'London'), ('UK', 'Manchester')
        ], names=['country', 'city'])
        df = pd.DataFrame({'pop': [8, 4, 9, 3]}, index=idx)
        print(df.loc['US'])

---

**Exercise 2.**
Create a MultiIndex DataFrame and use `.xs()` (cross-section) to select data at a specific level. Compare `.xs('US', level=0)` with `.loc['US']`.

??? success "Solution to Exercise 2"
    Use xs for cross-section selection.

        import pandas as pd

        idx = pd.MultiIndex.from_tuples([
            ('US', 'NYC'), ('US', 'LA'), ('UK', 'London')
        ], names=['country', 'city'])
        df = pd.DataFrame({'val': [100, 200, 300]}, index=idx)
        print(df.xs('US', level='country'))
        print(df.loc['US'])

---

**Exercise 3.**
Create a DataFrame with a MultiIndex. Use `.unstack()` to pivot one level of the index into columns, then `.stack()` to reverse the operation. Verify you get back the original structure.

??? success "Solution to Exercise 3"
    Stack and unstack a MultiIndex DataFrame.

        import pandas as pd

        idx = pd.MultiIndex.from_tuples([
            ('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y')
        ], names=['group', 'sub'])
        df = pd.DataFrame({'val': [1, 2, 3, 4]}, index=idx)
        unstacked = df.unstack()
        print("Unstacked:\n", unstacked)
        restacked = unstacked.stack()
        print("\nRestacked:\n", restacked)
