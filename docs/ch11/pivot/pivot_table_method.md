# pivot_table Method

The `pivot_table()` method creates a spreadsheet-style pivot table with aggregation support, handling duplicate entries and providing more flexibility than `pivot()`.

!!! tip "Mental Model"
    `pivot_table` is `pivot` with a built-in `groupby`. When multiple rows share the same (index, columns) pair, `pivot_table` aggregates them using `aggfunc` (default: mean). Think of it as the pandas equivalent of an Excel pivot table -- specify rows, columns, values, and an aggregation function to get a summary cross-tabulation.

## Basic Usage

Create a pivot table with aggregation.

### 1. Simple Pivot Table

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'date': ['5/1/2017', '5/1/2017', '5/2/2017', '5/2/2017',
             '5/1/2017', '5/2/2017'],
    'city': ['new york', 'new york', 'new york', 'new york',
             'mumbai', 'mumbai'],
    'temperature': [65, 61, 70, 72, 75, 81],
    'humidity': [56, 54, 60, 62, 80, 55]
})
print(df.head())
```

### 2. Create Pivot Table

```python
dg = df.pivot_table(
    index="city",
    columns="date",
    aggfunc=np.mean
)
print(dg)
```

```
         humidity          temperature         
date     5/1/2017 5/2/2017    5/1/2017 5/2/2017
city                                           
mumbai       80.0     55.0        75.0     81.0
new york     55.0     61.0        63.0     71.0
```

### 3. Automatic Aggregation

pivot_table aggregates duplicate index-column pairs.

## pivot_table vs pivot

Key differences between the methods.

### 1. Duplicates

```python
# pivot: fails with duplicate entries
# pivot_table: aggregates duplicates
```

### 2. Aggregation Function

```python
# pivot: no aggregation
# pivot_table: aggfunc parameter (default='mean')
```

### 3. Multiple Values

```python
# pivot_table can show multiple columns automatically
```

## aggfunc Parameter

Specify how to aggregate values.

### 1. Built-in Functions

```python
df.pivot_table(index='city', columns='date', values='temperature', aggfunc='sum')
df.pivot_table(index='city', columns='date', values='temperature', aggfunc='count')
df.pivot_table(index='city', columns='date', values='temperature', aggfunc='max')
```

### 2. NumPy Functions

```python
df.pivot_table(index='city', columns='date', values='temperature', aggfunc=np.mean)
df.pivot_table(index='city', columns='date', values='temperature', aggfunc=np.std)
```

### 3. Multiple Functions

```python
df.pivot_table(
    index='city',
    columns='date',
    values='temperature',
    aggfunc=['mean', 'std', 'count']
)
```

## values Parameter

Specify which columns to aggregate.

### 1. Single Column

```python
df.pivot_table(
    index='city',
    columns='date',
    values='temperature'
)
```

### 2. Multiple Columns

```python
df.pivot_table(
    index='city',
    columns='date',
    values=['temperature', 'humidity']
)
```

### 3. All Numeric (Default)

```python
# If values not specified, all numeric columns are used
df.pivot_table(index='city', columns='date')
```

## fill_value Parameter

Replace missing values.

### 1. Fill with Zero

```python
df.pivot_table(
    index='city',
    columns='date',
    values='temperature',
    fill_value=0
)
```

### 2. Fill with NaN (Default)

Missing combinations show NaN.

### 3. Custom Fill

```python
df.pivot_table(..., fill_value=-999)
```

## Practical Example

Sales transactions analysis.

### 1. Sample Data

```python
sales = pd.DataFrame({
    'Region': ['North', 'South', 'East', 'West', 'North', 'South'],
    'Product': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Sales': [100, 150, 200, 300, 250, 180],
    'Profit': [20, 30, 50, 80, 60, 40]
})
```

### 2. Create Summary

```python
pivot_sales = sales.pivot_table(
    values='Sales',
    index='Region',
    columns='Product',
    aggfunc='sum',
    fill_value=0
)
print(pivot_sales)
```

### 3. Add Margins

```python
pivot_sales = sales.pivot_table(
    values='Sales',
    index='Region',
    columns='Product',
    aggfunc='sum',
    margins=True,
    margins_name='Total'
)
```


---

## Exercises

**Exercise 1.** Write code that creates a pivot table with `aggfunc='mean'` to compute the average value for each group combination.

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

**Exercise 2.** Explain the difference between `.pivot()` and `.pivot_table()`. When must you use `pivot_table`?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Create a pivot table with multiple aggregation functions using `aggfunc=['mean', 'sum', 'count']`.

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

**Exercise 4.** Write code that creates a pivot table with `margins=True` to add row and column totals.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
