# dropna Keywords

The `dropna()` method accepts several keyword arguments to control which rows or columns are dropped.

!!! tip "Mental Model"
    The keywords fine-tune which rows survive. `how='any'` drops a row if even one cell is NaN; `how='all'` drops only if every cell is NaN. `subset` limits the NaN check to specific columns. `thresh` sets a minimum count of non-NaN values required to keep the row. Together they let you express nuanced "how much missing is too much" policies.

## how Keyword

Specify when to drop a row or column.

### 1. how='any' (Default)

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, np.nan, 3],
    'B': [4, np.nan, np.nan],
    'C': [7, 8, 9]
})

df.dropna(how='any')
# Drops row if ANY value is NaN
```

### 2. how='all'

```python
url = "https://raw.githubusercontent.com/codebasics/py/master/pandas/5_handling_missing_data_fillna_dropna_interpolate/weather_data.csv"
df = pd.read_csv(url, index_col='day', parse_dates=True)

dg = df.dropna(how='all')
print(dg)
```

Only drops rows where ALL values are NaN.

### 3. Comparison

```python
# how='any': Drop if at least one NaN
# how='all': Drop only if entire row is NaN
```

## subset Keyword

Specify columns to consider for NaN detection.

### 1. Single Column

```python
students = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', None, 'Bob'],
    'grade': ['A', 'B', None]
})

students.dropna(subset=['name'])
# Only checks 'name' column
```

### 2. Multiple Columns

```python
students.dropna(subset=['name', 'grade'])
# Drops if NaN in name OR grade
```

### 3. Selective Cleaning

```python
# Keep rows even if other columns have NaN
# Only require specific columns to be non-null
df.dropna(subset=['critical_column'])
```

## thresh Keyword

Require minimum number of non-NaN values.

### 1. Basic Usage

```python
url = "https://raw.githubusercontent.com/codebasics/py/master/pandas/5_handling_missing_data_fillna_dropna_interpolate/weather_data.csv"
df = pd.read_csv(url, index_col='day', parse_dates=True)

dg = df.dropna(thresh=2)
print(dg)
```

Keeps rows with at least 2 non-NaN values.

### 2. Calculate Threshold

```python
# Keep rows with at least 50% non-null values
threshold = int(len(df.columns) * 0.5)
df.dropna(thresh=threshold)
```

### 3. Cannot Combine with how

```python
# thresh cannot be used with how parameter
# df.dropna(how='any', thresh=2)  # Error
```

## axis Keyword

Drop rows or columns.

### 1. axis=0 (Default)

```python
df.dropna(axis=0)  # Drop rows
df.dropna()        # Same as axis=0
```

### 2. axis=1

```python
df.dropna(axis=1)  # Drop columns with NaN
```

### 3. Column Cleaning

```python
# Remove columns with more than 50% missing
threshold = int(len(df) * 0.5)
df.dropna(axis=1, thresh=threshold)
```

## Combined Keywords

Use multiple keywords for precise control.

### 1. Subset with Threshold

```python
# Keep rows with at least 2 non-null values
# in the specified columns
df.dropna(subset=['col1', 'col2', 'col3'], thresh=2)
```

### 2. Axis with how

```python
# Drop columns where all values are NaN
df.dropna(axis=1, how='all')
```

### 3. Practical Pipeline

```python
df_clean = (df
    .dropna(how='all')           # Remove empty rows
    .dropna(axis=1, how='all')   # Remove empty columns
    .dropna(subset=['key_col'])  # Require key column
)
```

## inplace Keyword

Modify DataFrame in place.

### 1. Without inplace

```python
dg = df.dropna()  # Returns new DataFrame
```

### 2. With inplace

```python
df.dropna(inplace=True)  # Modifies df directly
```

### 3. Prefer Reassignment

```python
df = df.dropna()  # More explicit than inplace
```

---

## Exercises

**Exercise 1.**
Create a DataFrame where one row is entirely `NaN`. Use `dropna(how='all')` to drop only that row. Verify that rows with partial `NaN` values are kept.

??? success "Solution to Exercise 1"
    Drop only rows where all values are NaN.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'A': [1, np.nan, 3],
            'B': [np.nan, np.nan, 6],
            'C': [7, np.nan, 9]
        })
        result = df.dropna(how='all')
        print(result)
        print(f"Rows kept: {len(result)}")

---

**Exercise 2.**
Create a DataFrame and use `dropna(thresh=2)` to keep only rows that have at least 2 non-null values. Count how many rows are dropped.

??? success "Solution to Exercise 2"
    Use thresh to require a minimum number of non-null values.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'A': [1, np.nan, np.nan, 4],
            'B': [np.nan, np.nan, 3, 4],
            'C': [1, np.nan, np.nan, 4]
        })
        before = len(df)
        result = df.dropna(thresh=2)
        print(result)
        print(f"Dropped: {before - len(result)} rows")

---

**Exercise 3.**
Create a DataFrame with 4 columns and use `dropna(subset=['col1', 'col2'])` to drop rows only when `col1` or `col2` has `NaN`, ignoring `NaN` in other columns.

??? success "Solution to Exercise 3"
    Drop based on specific column subset.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'col1': [1, np.nan, 3, 4],
            'col2': [5, 6, np.nan, 8],
            'col3': [np.nan, np.nan, np.nan, 12],
            'col4': [13, 14, 15, 16]
        })
        result = df.dropna(subset=['col1', 'col2'])
        print(result)
        # NaN in col3 does not trigger row removal
