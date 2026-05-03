# Keyword - indicator

The `indicator` parameter adds a column showing the source of each row, useful for debugging and understanding merge results.

!!! tip "Mental Model"
    `indicator=True` adds a `_merge` column with values `left_only`, `right_only`, or `both`, revealing exactly which table contributed each row. It is the best debugging tool for merges -- use it to verify that an inner join did not silently drop rows or that an outer join introduced expected NaN rows.

## Basic Usage

Add a column indicating merge source.

### 1. Enable Indicator

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

df = pd.merge(df1, df2, on='city', how='outer', indicator=True)
print(df)
```

```
  city  temperature  humidity      _merge
0   NY         21.0      68.0        both
1   SF         14.0      65.0        both
2   LA         35.0       NaN   left_only
3  ICN          NaN      75.0  right_only
```

### 2. Indicator Values

- `both`: Key exists in both DataFrames
- `left_only`: Key exists only in left DataFrame
- `right_only`: Key exists only in right DataFrame

### 3. Column Name

Default column name is `_merge`.

## Custom Column Name

Specify indicator column name.

### 1. String Value

```python
df = pd.merge(
    df1, df2,
    on='city',
    how='outer',
    indicator='source'
)
print(df['source'])
```

```
0          both
1          both
2     left_only
3    right_only
Name: source, dtype: object
```

### 2. Descriptive Name

```python
df = pd.merge(
    df1, df2,
    on='city',
    how='outer',
    indicator='merge_status'
)
```

### 3. Avoid Conflicts

```python
# Name must not conflict with existing columns
```

## Filtering by Indicator

Use indicator to filter results.

### 1. Find Unmatched Left

```python
df = pd.merge(df1, df2, on='city', how='outer', indicator=True)
unmatched_left = df[df['_merge'] == 'left_only']
print(unmatched_left)
```

```
  city  temperature  humidity     _merge
2   LA         35.0       NaN  left_only
```

### 2. Find Unmatched Right

```python
unmatched_right = df[df['_merge'] == 'right_only']
```

### 3. Find Matched Only

```python
matched = df[df['_merge'] == 'both']
```

## Data Quality Checks

Use indicator for merge validation.

### 1. Count Match Types

```python
df = pd.merge(df1, df2, on='key', how='outer', indicator=True)
print(df['_merge'].value_counts())
```

```
both          100
left_only      15
right_only     20
Name: _merge, dtype: int64
```

### 2. Validate Complete Match

```python
unmatched = df[df['_merge'] != 'both']
if len(unmatched) > 0:
    print(f"Warning: {len(unmatched)} unmatched rows")
```

### 3. Data Reconciliation

```python
# Identify missing records in each source
missing_in_right = df[df['_merge'] == 'left_only']['key']
missing_in_left = df[df['_merge'] == 'right_only']['key']
```

## Drop Indicator Column

Remove indicator after use.

### 1. Drop Column

```python
df = pd.merge(df1, df2, on='city', how='outer', indicator=True)
# Use indicator for filtering
matched_df = df[df['_merge'] == 'both'].drop('_merge', axis=1)
```

### 2. Chain Operations

```python
matched_df = (
    pd.merge(df1, df2, on='city', how='outer', indicator=True)
    .query("_merge == 'both'")
    .drop('_merge', axis=1)
)
```

### 3. Select Columns

```python
result = df[['city', 'temperature', 'humidity']]
```

## Practical Applications

Real-world uses for indicator.

### 1. Find New Records

```python
# Find records added since last sync
new_records = merged[merged['_merge'] == 'right_only']
```

### 2. Find Deleted Records

```python
# Find records removed since last sync
deleted_records = merged[merged['_merge'] == 'left_only']
```

### 3. Debug Merge Issues

```python
# Understand why rows are missing
if merged['_merge'].value_counts().get('left_only', 0) > expected:
    print("Investigate: too many unmatched left rows")
```

---

## Exercises

**Exercise 1.**
Create two DataFrames and perform an outer merge with `indicator=True`. Filter the result to show only rows that appear in the left DataFrame but not the right (i.e., `_merge == 'left_only'`).

??? success "Solution to Exercise 1"
    Find left-only rows using the indicator column.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'val1': [1, 2, 3]})
        df2 = pd.DataFrame({'key': ['b', 'c', 'd'], 'val2': [4, 5, 6]})
        result = pd.merge(df1, df2, on='key', how='outer', indicator=True)
        left_only = result[result['_merge'] == 'left_only']
        print(left_only)

---

**Exercise 2.**
Use `indicator=True` with an inner merge. Verify that all rows in the result have `_merge == 'both'` (since inner join only keeps matches).

??? success "Solution to Exercise 2"
    Verify inner merge indicator values are all 'both'.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'val1': [1, 2, 3]})
        df2 = pd.DataFrame({'key': ['b', 'c', 'd'], 'val2': [4, 5, 6]})
        result = pd.merge(df1, df2, on='key', how='inner', indicator=True)
        assert (result['_merge'] == 'both').all()
        print("All inner join rows are 'both'.")

---

**Exercise 3.**
Use `indicator='source'` (custom column name) in an outer merge. Use `value_counts()` on the indicator column to summarize how many rows came from each source.

??? success "Solution to Exercise 3"
    Use a custom indicator column name and summarize.

        import pandas as pd

        df1 = pd.DataFrame({'id': [1, 2, 3], 'name': ['A', 'B', 'C']})
        df2 = pd.DataFrame({'id': [2, 3, 4], 'score': [80, 90, 70]})
        result = pd.merge(df1, df2, on='id', how='outer', indicator='source')
        print(result['source'].value_counts())
