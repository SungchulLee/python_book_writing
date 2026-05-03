# Keyword - on and lsuffix/rsuffix

By default, `DataFrame.join` matches rows using the index of both DataFrames. The `on` parameter overrides this by specifying a column from the calling DataFrame to use as the join key instead. When both DataFrames share non-key column names, the `lsuffix` and `rsuffix` parameters add distinguishing suffixes to avoid name collisions.

!!! tip "Mental Model"
    `on` shifts the left side's join key from the index to a named column, while the right side still matches on its index. `lsuffix` and `rsuffix` are disambiguation labels: when both DataFrames share a column name, pandas appends these suffixes so you can tell `value_left` from `value_right` in the result.

```python
import pandas as pd
```

---

## on Parameter

The `on` parameter specifies one or more columns from the **calling** DataFrame to join on. The **other** DataFrame is still matched by its index.

### Default Behavior (No on)

Without `on`, both DataFrames are matched by their indices.

```python
df_left = pd.DataFrame(
    {"value": [10, 20, 30]},
    index=["a", "b", "c"]
)

df_right = pd.DataFrame(
    {"label": ["X", "Y"]},
    index=["a", "b"]
)

result = df_left.join(df_right)
print(result)
```

```
   value label
a     10     X
b     20     Y
c     30   NaN
```

### Using on to Join on a Column

When the caller has a column that matches the other DataFrame's index, use `on` to specify it.

```python
employees = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "dept_id": ["D1", "D2", "D1"]
})

departments = pd.DataFrame(
    {"dept_name": ["Engineering", "Sales"]},
    index=["D1", "D2"]
)

# Join on the "dept_id" column of employees, matched to departments' index
result = employees.join(departments, on="dept_id")
print(result)
```

```
    name dept_id    dept_name
0  Alice      D1  Engineering
1    Bob      D2        Sales
2  Carol      D1  Engineering
```

The `dept_id` column values in `employees` are matched against the index of `departments`.

### on with Multiple Columns

When the other DataFrame has a MultiIndex, pass a list of column names.

```python
data = pd.DataFrame({
    "year": [2023, 2023, 2024],
    "quarter": ["Q1", "Q2", "Q1"],
    "revenue": [100, 200, 150]
})

targets = pd.DataFrame(
    {"target": [120, 180, 160]},
    index=pd.MultiIndex.from_tuples(
        [(2023, "Q1"), (2023, "Q2"), (2024, "Q1")],
        names=["year", "quarter"]
    )
)

result = data.join(targets, on=["year", "quarter"])
print(result)
```

```
   year quarter  revenue  target
0  2023      Q1      100     120
1  2023      Q2      200     180
2  2024      Q1      150     160
```

---

## lsuffix and rsuffix Parameters

When both DataFrames have columns with the same name (excluding the join key), `join` raises a `ValueError` unless you specify suffixes to distinguish them.

### The Problem

```python
df1 = pd.DataFrame({"val": [1, 2]}, index=["a", "b"])
df2 = pd.DataFrame({"val": [3, 4]}, index=["a", "b"])

try:
    result = df1.join(df2)
except ValueError as e:
    print(e)
# columns overlap but no suffix specified: Index(['val'], dtype='object')
```

### The Fix

```python
result = df1.join(df2, lsuffix="_left", rsuffix="_right")
print(result)
```

```
   val_left  val_right
a         1          3
b         2          4
```

- `lsuffix` is appended to overlapping column names from the **left** (calling) DataFrame
- `rsuffix` is appended to overlapping column names from the **right** (other) DataFrame

### Non-Overlapping Columns Are Unchanged

Suffixes are applied only to columns that conflict. Columns unique to one DataFrame keep their original names.

```python
df1 = pd.DataFrame({"val": [1, 2], "extra": [5, 6]}, index=["a", "b"])
df2 = pd.DataFrame({"val": [3, 4], "info": [7, 8]}, index=["a", "b"])

result = df1.join(df2, lsuffix="_L", rsuffix="_R")
print(result)
```

```
   val_L  extra  val_R  info
a      1      5      3     7
b      2      6      4     8
```

Only the `val` column (present in both) gets suffixes. `extra` and `info` remain unchanged.

---

## Combining on with lsuffix/rsuffix

Both parameters work together when joining on a column and facing name collisions.

```python
orders = pd.DataFrame({
    "product_id": ["P1", "P2", "P1"],
    "quantity": [10, 5, 8]
})

products = pd.DataFrame(
    {"quantity": [100, 50]},  # "quantity" here means stock quantity
    index=["P1", "P2"]
)

result = orders.join(
    products,
    on="product_id",
    lsuffix="_ordered",
    rsuffix="_in_stock"
)
print(result)
```

```
  product_id  quantity_ordered  quantity_in_stock
0         P1               10                100
1         P2                5                 50
2         P1                8                100
```

!!! warning "Suffixes Are Required for Overlapping Names"
    Unlike `pd.merge` which has default suffixes (`_x` and `_y`), `DataFrame.join` raises an error if overlapping column names exist and no suffixes are provided. Always specify `lsuffix` and `rsuffix` when name collisions are possible.

---

## Summary

| Parameter | Purpose | Default |
|-----------|---------|---------|
| `on` | Column(s) from the caller to use as join key | `None` (use index) |
| `lsuffix` | Suffix for overlapping columns from the left DataFrame | `""` (empty — raises error on overlap) |
| `rsuffix` | Suffix for overlapping columns from the right DataFrame | `""` (empty — raises error on overlap) |

**Key Takeaways**:

- `on` redirects the join key from the caller's index to one of its columns; the other DataFrame is still matched by its index
- `lsuffix` and `rsuffix` resolve column name collisions by appending suffixes to the conflicting names
- Non-overlapping columns are never modified by suffix parameters
- Unlike `pd.merge`, `DataFrame.join` does not provide default suffixes — they must be specified explicitly when overlaps exist
- Use `on` with a list of column names when the other DataFrame has a MultiIndex

---

## Exercises

**Exercise 1.**
Create an `employees` DataFrame with columns `'name'` and `'dept_id'`, and a `departments` DataFrame indexed by department ID with a `'dept_name'` column. Use `.join()` with `on='dept_id'` to look up each employee's department name.

??? success "Solution to Exercise 1"
    Use the on parameter to join a column to an index.

        import pandas as pd

        employees = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Carol'],
            'dept_id': ['D1', 'D2', 'D1']
        })
        departments = pd.DataFrame(
            {'dept_name': ['Engineering', 'Sales']},
            index=['D1', 'D2']
        )
        result = employees.join(departments, on='dept_id')
        print(result)

---

**Exercise 2.**
Create two DataFrames that both have a column named `'score'`. Join them by index using `lsuffix='_exam1'` and `rsuffix='_exam2'`. Then compute a new column `'avg_score'` as the mean of the two score columns.

??? success "Solution to Exercise 2"
    Resolve overlapping column names and compute an average.

        import pandas as pd

        df1 = pd.DataFrame({'score': [85, 90, 78]}, index=['Alice', 'Bob', 'Carol'])
        df2 = pd.DataFrame({'score': [88, 92, 80]}, index=['Alice', 'Bob', 'Carol'])
        result = df1.join(df2, lsuffix='_exam1', rsuffix='_exam2')
        result['avg_score'] = (result['score_exam1'] + result['score_exam2']) / 2
        print(result)

---

**Exercise 3.**
Create a flat DataFrame with `'year'` and `'quarter'` columns, and a targets DataFrame with a MultiIndex of (year, quarter). Use `.join()` with `on=['year', 'quarter']` to combine them. Verify the target values are correctly aligned.

??? success "Solution to Exercise 3"
    Join flat columns against a MultiIndex using on.

        import pandas as pd

        data = pd.DataFrame({
            'year': [2023, 2023, 2024],
            'quarter': ['Q1', 'Q2', 'Q1'],
            'revenue': [100, 200, 150]
        })
        targets = pd.DataFrame(
            {'target': [120, 180, 160]},
            index=pd.MultiIndex.from_tuples(
                [(2023, 'Q1'), (2023, 'Q2'), (2024, 'Q1')],
                names=['year', 'quarter']
            )
        )
        result = data.join(targets, on=['year', 'quarter'])
        print(result)
