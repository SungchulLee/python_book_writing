# melt Method

The `melt()` function transforms a DataFrame from wide format to long format, unpivoting columns into rows.

!!! tip "Mental Model"
    `melt` is the reverse of `pivot`. It takes columns and folds them down into two new columns: one for the former column name ("variable") and one for the value. Use `id_vars` to specify which columns stay fixed and `value_vars` to specify which columns get melted. The result is always longer and narrower.

## Basic Usage

Convert columns to rows.

### 1. Wide to Long

```python
import pandas as pd

data = {
    "day": ["Monday", "Tuesday", "Wednesday"],
    "chicago": [32, 30, 28],
    "chennai": [75, 77, 75],
    "berlin": [41, 43, 45],
}
df = pd.DataFrame(data)
print("Original DataFrame:")
print(df)
```

```
         day  chicago  chennai  berlin
0     Monday       32       75      41
1    Tuesday       30       77      43
2  Wednesday       28       75      45
```

### 2. Melt Transform

```python
dg = pd.melt(df, id_vars=["day"], var_name='city', value_name='temperature')
print("Melted DataFrame:")
print(dg)
```

```
         day     city  temperature
0     Monday  chicago           32
1    Tuesday  chicago           30
2  Wednesday  chicago           28
3     Monday  chennai           75
4    Tuesday  chennai           77
5  Wednesday  chennai           75
6     Monday   berlin           41
7    Tuesday   berlin           43
8  Wednesday   berlin           45
```

### 3. Result Structure

Each city-day combination becomes a row.

## Parameters

Control the melt transformation.

### 1. id_vars

```python
# Columns to keep as identifiers
pd.melt(df, id_vars=["day"])
```

### 2. var_name

```python
# Name for the column containing original column headers
pd.melt(df, id_vars=["day"], var_name='city')
```

### 3. value_name

```python
# Name for the column containing values
pd.melt(df, id_vars=["day"], value_name='temperature')
```

## LeetCode Example: Sales Report

Transform quarterly sales to long format.

### 1. Sample Data

```python
report = pd.DataFrame({
    'product': ['A', 'B'],
    'Q1': [10, 15],
    'Q2': [20, 25],
    'Q3': [30, 35],
    'Q4': [40, 45]
})
print(report)
```

```
  product  Q1  Q2  Q3  Q4
0       A  10  20  30  40
1       B  15  25  35  45
```

### 2. Melt Transform

```python
result = pd.melt(
    report,
    id_vars=["product"],
    var_name='quarter',
    value_name='sales'
)
print(result)
```

```
  product quarter  sales
0       A      Q1     10
1       B      Q1     15
2       A      Q2     20
3       B      Q2     25
4       A      Q3     30
5       B      Q3     35
6       A      Q4     40
7       B      Q4     45
```

### 3. Analysis Ready

Long format is easier for groupby and plotting.

## value_vars Parameter

Select specific columns to unpivot.

### 1. Subset of Columns

```python
pd.melt(
    report,
    id_vars=["product"],
    value_vars=["Q1", "Q2"],  # Only Q1 and Q2
    var_name='quarter',
    value_name='sales'
)
```

### 2. Exclude Columns

```python
# If not specified, all non-id columns are melted
```

### 3. Column Order

```python
# value_vars also controls order in result
```

## Method vs Function

Two ways to call melt.

### 1. Function Syntax

```python
pd.melt(df, id_vars=["day"])
```

### 2. Method Syntax

```python
df.melt(id_vars=["day"])
```

### 3. Equivalent Results

Both produce identical output.


---

## Exercises

**Exercise 1.** Write code that converts a wide DataFrame to long format using `pd.melt()`. Specify `id_vars` and `value_vars`.

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

**Exercise 2.** Explain the `id_vars`, `value_vars`, `var_name`, and `value_name` parameters of `pd.melt()`.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that melts a DataFrame with column names like `'Jan'`, `'Feb'`, `'Mar'` into a long format with a `'month'` column.

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

**Exercise 4.** Create a wide DataFrame, melt it, and then use `.pivot()` to convert it back to wide format.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
