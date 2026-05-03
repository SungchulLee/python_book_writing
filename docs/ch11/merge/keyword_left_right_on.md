# Keyword - left_on right_on

The `left_on` and `right_on` parameters specify join columns when they have different names in each DataFrame.

!!! tip "Mental Model"
    `left_on` and `right_on` solve the "same concept, different name" problem. When the left table calls it `city` and the right calls it `town`, you tell pandas to match `city` against `town`. Both columns survive in the result, so you may want to drop the redundant one afterward.

## Basic Usage

Join DataFrames with differently named columns.

### 1. Different Column Names

```python
import pandas as pd

df1 = pd.DataFrame({
    'city': ['NY', 'SF', 'LA'],
    'temperature': [21, 14, 35]
})

df2 = pd.DataFrame({
    'CITY': ['SF', 'NY', 'ICN'],
    'humidity': [65, 68, 75]
})

df = pd.merge(df1, df2, left_on='city', right_on='CITY')
print(df)
```

```
  city  temperature CITY  humidity
0   NY           21   NY        68
1   SF           14   SF        65
```

### 2. Both Columns Kept

```python
# Both join columns appear in result
# Use drop to remove duplicate
df = df.drop('CITY', axis=1)
```

### 3. Cannot Use with on

```python
# left_on/right_on and on are mutually exclusive
# pd.merge(df1, df2, on='city', left_on='city')  # Error
```

## Multiple Columns

Specify multiple columns for each side.

### 1. List of Columns

```python
df1 = pd.DataFrame({
    'year': [2023, 2024],
    'qtr': [1, 1],
    'sales': [100, 200]
})

df2 = pd.DataFrame({
    'fiscal_year': [2023, 2024],
    'quarter': [1, 1],
    'expenses': [80, 120]
})

df = pd.merge(
    df1, df2,
    left_on=['year', 'qtr'],
    right_on=['fiscal_year', 'quarter']
)
```

### 2. Lists Must Match Length

```python
# left_on and right_on must have same number of columns
```

### 3. Order Matters

```python
# First column in left_on matches first in right_on
left_on=['a', 'b']
right_on=['x', 'y']  # a matches x, b matches y
```

## Index as Join Key

Use index instead of columns.

### 1. left_index and right_index

```python
df1 = pd.DataFrame({'value': [1, 2]}, index=['A', 'B'])
df2 = pd.DataFrame({'other': [3, 4]}, index=['A', 'C'])

pd.merge(df1, df2, left_index=True, right_index=True)
```

### 2. Column to Index

```python
# Join df1's column with df2's index
pd.merge(df1, df2, left_on='key', right_index=True)
```

### 3. Index to Column

```python
# Join df1's index with df2's column
pd.merge(df1, df2, left_index=True, right_on='key')
```

## LeetCode Example: Employees and Managers

Self-join with different column references.

### 1. Sample Data

```python
employee = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['John', 'Doe', 'Jane', 'Smith'],
    'salary': [50000, 40000, 60000, 30000],
    'managerId': [None, 1, 1, 2]
})
```

### 2. Self Merge

```python
merged = pd.merge(
    left=employee,
    right=employee,
    left_on='managerId',
    right_on='id',
    how='inner',
    suffixes=('_employee', '_manager')
)
print(merged)
```

### 3. Result

```
   id_employee name_employee  salary_employee  managerId_employee  id_manager name_manager  salary_manager  managerId_manager
0            2           Doe            40000                 1.0           1         John           50000                NaN
1            3          Jane            60000                 1.0           1         John           50000                NaN
2            4         Smith            30000                 2.0           2          Doe           40000                1.0
```

## Cleanup After Merge

Remove redundant columns after merge.

### 1. Drop Duplicate Column

```python
df = pd.merge(df1, df2, left_on='city', right_on='CITY')
df = df.drop('CITY', axis=1)
```

### 2. Rename Columns

```python
df = df.rename(columns={'city': 'location'})
```

### 3. Select Columns

```python
df = df[['city', 'temperature', 'humidity']]
```

---

## Exercises

**Exercise 1.**
Create two DataFrames where the key column is named `'emp_id'` in one and `'employee_id'` in the other. Use `left_on` and `right_on` to merge them. Drop the duplicate key column afterward.

??? success "Solution to Exercise 1"
    Merge on differently named key columns.

        import pandas as pd

        df1 = pd.DataFrame({'emp_id': [1, 2, 3], 'salary': [50000, 60000, 70000]})
        df2 = pd.DataFrame({'employee_id': [1, 2, 3], 'dept': ['HR', 'IT', 'Sales']})
        result = pd.merge(df1, df2, left_on='emp_id', right_on='employee_id')
        result = result.drop(columns='employee_id')
        print(result)

---

**Exercise 2.**
Create a DataFrame with a `'manager_id'` column and another with `'id'` and `'name'`. Use `left_on='manager_id'` and `right_on='id'` to look up each person's manager name.

??? success "Solution to Exercise 2"
    Look up manager names via left_on and right_on.

        import pandas as pd

        employees = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Carol'],
            'manager_id': [None, 1, 1]
        })
        result = pd.merge(
            employees, employees[['id', 'name']],
            left_on='manager_id', right_on='id',
            suffixes=('', '_manager'), how='left'
        )
        print(result[['name', 'name_manager']])

---

**Exercise 3.**
Merge two DataFrames where one has the key in a column and the other has the key as its index. Use `left_on='key_col'` and `right_index=True` to perform the merge.

??? success "Solution to Exercise 3"
    Merge column key against index key.

        import pandas as pd

        orders = pd.DataFrame({'order_id': [1, 2, 3], 'product_id': [101, 102, 101]})
        products = pd.DataFrame(
            {'product_name': ['Widget', 'Gadget']},
            index=pd.Index([101, 102], name='product_id')
        )
        result = pd.merge(orders, products, left_on='product_id', right_index=True)
        print(result)
