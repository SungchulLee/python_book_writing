# Keyword - on

The `on` parameter specifies which column(s) to use as the join key when both DataFrames share the same column name.

!!! tip "Mental Model"
    `on` is the explicit key selector for merge. Without it, pandas merges on all shared column names, which can produce surprising results if tables share incidental columns. Always specify `on` to make the join key unambiguous and self-documenting.

## Single Column

Join on a single shared column.

### 1. Basic Usage

```python
import pandas as pd

df1 = pd.DataFrame({
    'city': ['NY', 'SF', 'LA'],
    'temperature': [21, 14, 35]
})

df2 = pd.DataFrame({
    'city': ['SF', 'NY', 'ICN'],
    'humidity': [65, 68, 75]
})

df = pd.merge(df1, df2, on='city')
print(df)
```

```
  city  temperature  humidity
0   NY           21        68
1   SF           14        65
```

### 2. Column Must Exist

```python
# Column must exist in both DataFrames
# pd.merge(df1, df2, on='nonexistent')  # KeyError
```

### 3. Case Sensitive

```python
# Column names are case-sensitive
# 'City' != 'city'
```

## Multiple Columns

Join on multiple columns.

### 1. List of Columns

```python
df1 = pd.DataFrame({
    'year': [2023, 2023, 2024],
    'month': [1, 2, 1],
    'sales': [100, 150, 200]
})

df2 = pd.DataFrame({
    'year': [2023, 2023, 2024],
    'month': [1, 2, 1],
    'expenses': [80, 90, 120]
})

df = pd.merge(df1, df2, on=['year', 'month'])
print(df)
```

### 2. All Keys Must Match

```python
# A row matches only if ALL specified columns match
```

### 3. Order Independence

```python
# on=['year', 'month'] same as on=['month', 'year']
```

## LeetCode Example: Student Examinations

Join on multiple columns for student-subject pairs.

### 1. Sample Data

```python
student_subject = pd.DataFrame({
    'student_id': [1, 1, 2, 2],
    'student_name': ['Alice', 'Alice', 'Bob', 'Bob'],
    'subject_name': ['Math', 'Science', 'Math', 'Science']
})

examination_count = pd.DataFrame({
    'student_id': [1, 1, 2],
    'subject_name': ['Math', 'Science', 'Math'],
    'attended_exams': [2, 1, 3]
})
```

### 2. Multi-column Join

```python
result = pd.merge(
    student_subject,
    examination_count,
    on=['student_id', 'subject_name'],
    how='left'
)
print(result)
```

### 3. Result

```
   student_id student_name subject_name  attended_exams
0           1        Alice         Math             2.0
1           1        Alice      Science             1.0
2           2          Bob         Math             3.0
3           2          Bob      Science             NaN
```

## Default Behavior

When `on=None`, merge auto-detects common columns.

### 1. Auto Detection

```python
# Finds all columns with same name in both DataFrames
pd.merge(df1, df2)  # Uses all common columns
```

### 2. Explicit is Better

```python
# Prefer explicit on parameter for clarity
pd.merge(df1, df2, on='common_column')
```

### 3. Avoid Surprises

```python
# Auto-detection may join on unintended columns
# Always specify on for production code
```

## Error Handling

Common issues with the `on` parameter.

### 1. Column Not Found

```python
# KeyError if column doesn't exist in both
try:
    pd.merge(df1, df2, on='missing_col')
except KeyError as e:
    print(f"Error: {e}")
```

### 2. No Common Columns

```python
# MergeError if on=None and no common columns
# Solution: use left_on and right_on
```

### 3. Type Mismatch

```python
# Columns should have compatible types
# int and float usually work
# str and int will not match
```

---

## Exercises

**Exercise 1.**
Create two DataFrames that share two columns: `'year'` and `'month'`. Merge them on both columns simultaneously using `on=['year', 'month']`.

??? success "Solution to Exercise 1"
    Merge on multiple shared columns.

        import pandas as pd

        sales = pd.DataFrame({'year': [2023, 2023, 2024], 'month': [1, 2, 1], 'revenue': [100, 200, 150]})
        targets = pd.DataFrame({'year': [2023, 2023, 2024], 'month': [1, 2, 1], 'target': [120, 180, 160]})
        result = pd.merge(sales, targets, on=['year', 'month'])
        print(result)

---

**Exercise 2.**
Create two DataFrames with one shared column name. Merge using `on` to specify the key explicitly, even though pandas would auto-detect it. Verify the result is the same as merging without the `on` parameter.

??? success "Solution to Exercise 2"
    Compare explicit on vs auto-detected key.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'val1': [1, 2, 3]})
        df2 = pd.DataFrame({'key': ['a', 'b', 'd'], 'val2': [4, 5, 6]})
        explicit = pd.merge(df1, df2, on='key')
        auto = pd.merge(df1, df2)
        assert explicit.equals(auto)
        print("Explicit on= gives same result as auto-detect.")

---

**Exercise 3.**
Create two DataFrames that share a column name `'id'` but also have other overlapping column names. Merge on `'id'` and observe how the overlapping non-key columns get suffixed with `_x` and `_y`.

??? success "Solution to Exercise 3"
    Observe suffix behavior for overlapping non-key columns.

        import pandas as pd

        df1 = pd.DataFrame({'id': [1, 2], 'score': [85, 90], 'grade': ['B', 'A']})
        df2 = pd.DataFrame({'id': [1, 2], 'score': [88, 92], 'comment': ['good', 'great']})
        result = pd.merge(df1, df2, on='id')
        print(result)
        print("Columns:", result.columns.tolist())
