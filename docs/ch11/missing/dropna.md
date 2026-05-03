# dropna Method

The `dropna()` method removes rows or columns containing missing values. It is useful when missing data cannot be reliably imputed.

!!! tip "Mental Model"
    `dropna()` is the "delete the problem" strategy for missing data. It removes entire rows (or columns) that contain NaN. It is safe when missing values are few and random, but dangerous when data is missing systematically -- dropping those rows could introduce bias. Always check how much data you are losing before committing.

## Basic Usage

Drop rows with any missing values.

### 1. Drop Rows

```python
import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/codebasics/py/master/pandas/5_handling_missing_data_fillna_dropna_interpolate/weather_data.csv"
df = pd.read_csv(url, index_col='day', parse_dates=True)
print(df)

dg = df.dropna()
print(dg)
```

### 2. Drop Columns

```python
df.dropna(axis=1)  # Drop columns with any NaN
```

### 3. Return Copy

```python
# dropna returns a new DataFrame
dg = df.dropna()
# Original df is unchanged
```

## LeetCode Example: Student Names

Drop students with missing names.

### 1. Problem Data

```python
students = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'name': ['Alice', None, 'Bob', None, 'Charlie'],
    'grade': ['A', 'B', 'B+', 'A-', 'C']
})
```

### 2. Drop Missing Names

```python
result = students.dropna(subset=['name'])
print(result)
```

### 3. Result

```
   id     name grade
0   1    Alice     A
2   3      Bob    B+
4   5  Charlie     C
```

## LeetCode Example: Employee Data

Drop employees with any missing values.

### 1. Problem Data

```python
filtered_employees = pd.DataFrame({
    'employee_id': [1, 2, 3, 4, 5],
    'manager_id': [2.0, None, None, 2.0, 3.0],
    'salary': [25000, 35000, 28000, None, 32000]
})
```

### 2. Drop All NaN Rows

```python
cleaned_employees = filtered_employees.dropna()
print(cleaned_employees)
```

### 3. Result

Only rows with complete data remain:

```
   employee_id  manager_id  salary
0            1         2.0   25000
4            5         3.0   32000
```

## Practical Considerations

When to use dropna vs fillna.

### 1. Use dropna When

- Missing data is random and limited
- Filling would introduce bias
- Sufficient data remains after dropping

### 2. Avoid dropna When

- Missing data is systematic
- Dropping loses too much information
- Missing values can be reasonably estimated

### 3. Check Impact

```python
print(f"Before: {len(df)} rows")
print(f"After: {len(df.dropna())} rows")
print(f"Dropped: {len(df) - len(df.dropna())} rows")
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with `NaN` values in different positions. Use `.dropna()` to drop rows with any missing values. Compare the number of rows before and after.

??? success "Solution to Exercise 1"
    Drop rows with any NaN and compare counts.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'A': [1, np.nan, 3, 4],
            'B': [5, 6, np.nan, 8],
            'C': [9, 10, 11, 12]
        })
        print(f"Before: {len(df)} rows")
        result = df.dropna()
        print(f"After: {len(result)} rows")

---

**Exercise 2.**
Create a DataFrame where one column is entirely `NaN`. Use `.dropna(axis=1)` to drop columns with any missing values. Verify the all-NaN column is removed.

??? success "Solution to Exercise 2"
    Drop all-NaN columns with axis=1.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'A': [1, 2, 3],
            'B': [np.nan, np.nan, np.nan],
            'C': [4, np.nan, 6]
        })
        result = df.dropna(axis=1)
        print(result.columns.tolist())
        assert 'B' not in result.columns

---

**Exercise 3.**
Create a DataFrame and use `.dropna(subset=['col_name'])` to drop rows only where a specific column has missing values, leaving other columns' NaN values intact.

??? success "Solution to Exercise 3"
    Drop rows based on a specific column's missing values.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'name': ['Alice', None, 'Carol', 'Dave'],
            'score': [90, 85, np.nan, 88]
        })
        result = df.dropna(subset=['name'])
        print(result)
        # Row with None name is dropped, but NaN in score is kept
