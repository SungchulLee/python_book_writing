# Keyword - suffixes

The `suffixes` parameter specifies strings to append to overlapping column names when both DataFrames have columns with the same name.

!!! tip "Mental Model"
    When both tables have a column with the same name (and it is not the join key), pandas must disambiguate. `suffixes=('_left', '_right')` appends these tags to the conflicting names. Choose descriptive suffixes like `('_2023', '_2024')` so the resulting columns are self-documenting.

## Default Suffixes

Default suffixes are `_x` and `_y`.

### 1. Overlapping Columns

```python
import pandas as pd

df1 = pd.DataFrame({
    'city': ['NY', 'SF', 'LA'],
    'temperature': [21, 14, 35]
})

df2 = pd.DataFrame({
    'city': ['SF', 'NY', 'ICN'],
    'temperature': [22, 15, 30],
    'humidity': [65, 68, 75]
})

df = pd.merge(df1, df2, on='city')
print(df)
```

```
  city  temperature_x  temperature_y  humidity
0   NY             21             15        68
1   SF             14             22        65
```

### 2. Default Values

```python
# Default: suffixes=('_x', '_y')
```

### 3. Join Column Not Suffixed

The `on` column appears only once without suffix.

## Custom Suffixes

Specify meaningful suffix names.

### 1. Descriptive Names

```python
df = pd.merge(
    df1, df2,
    on='city',
    suffixes=['_left', '_right']
)
print(df)
```

```
  city  temperature_left  temperature_right  humidity
0   NY                21                 15        68
1   SF                14                 22        65
```

### 2. Source Identification

```python
df = pd.merge(
    df1, df2,
    on='city',
    suffixes=['_2023', '_2024']
)
```

### 3. Table Names

```python
df = pd.merge(
    orders, products,
    on='product_id',
    suffixes=['_order', '_product']
)
```

## Empty String Suffix

Use empty string to keep one column unchanged.

### 1. Keep Left Original

```python
df = pd.merge(
    df1, df2,
    on='city',
    suffixes=['', '_new']
)
# temperature (from df1)
# temperature_new (from df2)
```

### 2. Keep Right Original

```python
df = pd.merge(
    df1, df2,
    on='city',
    suffixes=['_old', '']
)
```

### 3. Avoid Both Empty

```python
# Both empty strings cause column name collision
# suffixes=['', '']  # Will raise error
```

## LeetCode Example: Employee Manager Comparison

Self-join with suffixes for clarity.

### 1. Sample Data

```python
employee = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['John', 'Doe', 'Jane', 'Smith'],
    'salary': [50000, 40000, 60000, 30000],
    'managerId': [None, 1, 1, 2]
})
```

### 2. Self Merge with Suffixes

```python
merged = pd.merge(
    left=employee,
    right=employee,
    left_on='managerId',
    right_on='id',
    how='inner',
    suffixes=('_employee', '_manager')
)
```

### 3. Clear Column Names

```python
# Columns: id_employee, name_employee, salary_employee, ...
#          id_manager, name_manager, salary_manager, ...
```

## Handling Multiple Overlaps

Suffixes apply to all overlapping columns.

### 1. Multiple Columns

```python
df1 = pd.DataFrame({
    'key': ['A', 'B'],
    'value1': [1, 2],
    'value2': [3, 4]
})

df2 = pd.DataFrame({
    'key': ['A', 'B'],
    'value1': [10, 20],
    'value2': [30, 40]
})

df = pd.merge(df1, df2, on='key', suffixes=['_v1', '_v2'])
# value1_v1, value1_v2, value2_v1, value2_v2
```

### 2. Consistent Naming

All overlapping columns get the same suffixes.

### 3. Post-merge Rename

```python
# Rename specific columns after merge
df = df.rename(columns={
    'value1_v1': 'value1_original',
    'value1_v2': 'value1_updated'
})
```

---

## Exercises

**Exercise 1.**
Create two DataFrames with a shared `'date'` key and a shared `'price'` column. Merge them on `'date'` with `suffixes=('_stock1', '_stock2')`. Compute the price difference between the two stocks.

??? success "Solution to Exercise 1"
    Merge with custom suffixes and compute a difference.

        import pandas as pd

        df1 = pd.DataFrame({'date': ['2024-01-01', '2024-01-02'], 'price': [100, 105]})
        df2 = pd.DataFrame({'date': ['2024-01-01', '2024-01-02'], 'price': [200, 210]})
        result = pd.merge(df1, df2, on='date', suffixes=('_stock1', '_stock2'))
        result['price_diff'] = result['price_stock2'] - result['price_stock1']
        print(result)

---

**Exercise 2.**
Merge two DataFrames and use `suffixes=('', '_new')` so that the left DataFrame's columns keep their original names while only the right's overlapping columns get suffixed.

??? success "Solution to Exercise 2"
    Keep left columns unchanged with empty suffix.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b'], 'val': [1, 2]})
        df2 = pd.DataFrame({'key': ['a', 'b'], 'val': [3, 4]})
        result = pd.merge(df1, df2, on='key', suffixes=('', '_new'))
        print(result)
        assert 'val' in result.columns
        assert 'val_new' in result.columns

---

**Exercise 3.**
Merge two DataFrames with multiple overlapping column names. Verify that all overlapping columns (except the key) receive the specified suffixes, while non-overlapping columns remain unchanged.

??? success "Solution to Exercise 3"
    Verify suffix behavior with multiple overlapping columns.

        import pandas as pd

        df1 = pd.DataFrame({'id': [1, 2], 'score': [85, 90], 'rank': [2, 1]})
        df2 = pd.DataFrame({'id': [1, 2], 'score': [88, 92], 'rank': [3, 1], 'extra': ['x', 'y']})
        result = pd.merge(df1, df2, on='id', suffixes=('_L', '_R'))
        print(result.columns.tolist())
        # score_L, score_R, rank_L, rank_R get suffixes; extra stays unchanged
