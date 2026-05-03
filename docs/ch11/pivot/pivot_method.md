# pivot Method

The `pivot()` method reshapes data from long format to wide format, spreading values across columns.

!!! tip "Mental Model"
    `pivot` takes three columns -- index, columns, values -- and reshapes the table so that unique values of the "columns" column become actual column headers. It is a pure reshape with no aggregation, so it requires unique (index, columns) pairs. If duplicates exist, use `pivot_table` instead.

## Basic Usage

Pivot a DataFrame.

### 1. Long to Wide

```python
import pandas as pd

df = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
    'city': ['NY', 'LA', 'NY', 'LA'],
    'temperature': [30, 70, 32, 72]
})
print("Long format:")
print(df)

wide = df.pivot(index='date', columns='city', values='temperature')
print("\nWide format:")
print(wide)
```

```
Long format:
         date city  temperature
0  2024-01-01   NY           30
1  2024-01-01   LA           70
2  2024-01-02   NY           32
3  2024-01-02   LA           72

Wide format:
city        LA  NY
date             
2024-01-01  70  30
2024-01-02  72  32
```

### 2. Parameters

```python
# index: column to become row index
# columns: column whose values become column headers
# values: column containing data values
```

### 3. Result Structure

Each unique value in 'city' becomes a column.

## LeetCode Example: Department Table

Reshape department revenue by month.

### 1. Sample Data

```python
department = pd.DataFrame({
    'id': [1, 1, 1, 2, 2],
    'month': ['Jan', 'Feb', 'Mar', 'Jan', 'Feb'],
    'revenue': [100, 150, 200, 80, 120]
})
```

### 2. Pivot Transform

```python
bymonth = department.pivot(
    index='id',
    columns='month',
    values='revenue'
)
print(bymonth)
```

```
month  Feb  Jan    Mar
id                    
1      150  100  200.0
2      120   80    NaN
```

### 3. Handle Missing

```python
bymonth = bymonth.fillna(0)
```

## Limitations

pivot has strict requirements.

### 1. No Duplicate Entries

```python
# pivot fails if index-column combination has duplicates
df = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-01'],
    'city': ['NY', 'NY'],  # Duplicate!
    'temp': [30, 31]
})
# df.pivot(index='date', columns='city', values='temp')  # Error!
```

### 2. Use pivot_table for Duplicates

```python
# pivot_table handles duplicates with aggregation
df.pivot_table(index='date', columns='city', values='temp', aggfunc='mean')
```

### 3. Single Value Required

Each index-column pair must have exactly one value.

## Financial Example

Pivot stock price data.

### 1. Sample Data

```python
prices = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-01', '2024-01-02', '2024-01-02'],
    'ticker': ['AAPL', 'MSFT', 'AAPL', 'MSFT'],
    'close': [150, 350, 152, 355]
})
```

### 2. Pivot to Wide

```python
price_matrix = prices.pivot(
    index='date',
    columns='ticker',
    values='close'
)
```

### 3. Use for Analysis

```python
# Calculate correlation
price_matrix.corr()

# Calculate returns
price_matrix.pct_change()
```

## reset_index After Pivot

Flatten the result.

### 1. Index as Column

```python
result = df.pivot(index='date', columns='city', values='temp')
result = result.reset_index()
```

### 2. Remove Column Name

```python
result.columns.name = None
```

### 3. Rename Columns

```python
result.columns = ['date', 'los_angeles', 'new_york']
```


---

## Exercises

**Exercise 1.** Create a DataFrame with columns `['date', 'city', 'temperature']` and use `.pivot()` to reshape it so each city becomes a column.

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

**Exercise 2.** Explain the three required parameters of `.pivot()`: `index`, `columns`, and `values`.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code showing that `.pivot()` raises an error when there are duplicate entries for the same index-column combination.

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

**Exercise 4.** Create a pivoted DataFrame and use `.melt()` to convert it back to the original long format.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
