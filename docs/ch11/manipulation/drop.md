# drop Method

The `drop()` method removes specified rows or columns from a DataFrame.

!!! tip "Mental Model"
    `drop()` removes by label, not by condition. Pass column names with `axis=1` to remove columns, or index labels with `axis=0` to remove rows. It returns a new DataFrame by default -- the original is unchanged unless you set `inplace=True`.

## Drop Columns

Remove columns by name.

### 1. Single Column

```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
})

result = df.drop('B', axis=1)
print(result)
```

```
   A  C
0  1  7
1  2  8
2  3  9
```

### 2. Multiple Columns

```python
result = df.drop(['B', 'C'], axis=1)
```

### 3. columns Parameter

```python
result = df.drop(columns=['B', 'C'])
# More explicit than axis=1
```

## Drop Rows

Remove rows by index.

### 1. Single Row

```python
result = df.drop(0)  # axis=0 is default
print(result)
```

```
   A  B  C
1  2  5  8
2  3  6  9
```

### 2. Multiple Rows

```python
result = df.drop([0, 2])
```

### 3. index Parameter

```python
result = df.drop(index=[0, 2])
```

## inplace Parameter

Modify DataFrame directly.

### 1. Without inplace

```python
result = df.drop(columns=['B'])
# df unchanged, result has change
```

### 2. With inplace

```python
df.drop(columns=['B'], inplace=True)
# df modified directly, returns None
```

### 3. Best Practice

```python
# Prefer reassignment over inplace
df = df.drop(columns=['B'])
```

## LeetCode Example: Tree Node

Drop unnecessary columns.

### 1. Sample Data

```python
tree = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'p_id': [None, 1, 1, 2, 2],
    'type': ['Root', 'Inner', 'Inner', 'Leaf', 'Leaf']
})
```

### 2. Drop Column

```python
result = tree.drop(columns='p_id')
print(result)
```

```
   id   type
0   1   Root
1   2  Inner
2   3  Inner
3   4   Leaf
4   5   Leaf
```

### 3. axis=1 Syntax

```python
result = tree.drop('p_id', axis=1)
```

## LeetCode Example: Top Travellers

Drop ID column from rides.

### 1. Sample Data

```python
rides = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'user_id': [1, 1, 2, 3],
    'distance': [10, 15, 20, 25]
})
```

### 2. Drop ID

```python
result = rides.drop('id', axis=1)
```

### 3. Result

```python
print(result)
```

```
   user_id  distance
0        1        10
1        1        15
2        2        20
3        3        25
```

## Drop by Condition

Remove rows based on conditions.

### 1. Drop NaN Rows

```python
# Use dropna instead
df = df.dropna()
```

### 2. Drop Specific Values

```python
# Filter instead of drop
df = df[df['status'] != 'Deleted']
```

### 3. Get Index Then Drop

```python
# Find rows to drop
to_drop = df[df['value'] < 0].index
df = df.drop(to_drop)
```

## errors Parameter

Handle missing labels.

### 1. Default (raise)

```python
# Raises KeyError if column doesn't exist
df.drop(columns=['NonExistent'])  # Error!
```

### 2. Ignore Errors

```python
df.drop(columns=['NonExistent'], errors='ignore')
# No error, returns df unchanged
```

### 3. Safe Drop

```python
# Drop if exists
columns_to_drop = ['B', 'NonExistent']
df.drop(columns=columns_to_drop, errors='ignore')
```

## Drop Duplicates Context

Use drop_duplicates for duplicate removal.

### 1. drop vs drop_duplicates

```python
# drop: remove by label
df.drop(index=[0, 1])

# drop_duplicates: remove duplicate rows
df.drop_duplicates()
```

### 2. Different Purposes

```python
# drop: known indices/columns
# drop_duplicates: based on values
```

### 3. See drop_duplicates

Refer to drop_duplicates.md for duplicate removal.

## Method Chaining

drop in pipelines.

### 1. Chain Operations

```python
result = (
    df
    .drop(columns=['temp_col'])
    .drop(index=[0])
    .reset_index(drop=True)
)
```

### 2. With Other Methods

```python
result = (
    df
    .assign(calculated=df['a'] + df['b'])
    .drop(columns=['a', 'b'])
    .rename(columns={'calculated': 'sum'})
)
```

### 3. Clean Pipeline

```python
result = (
    raw_df
    .dropna()
    .drop(columns=['unnecessary_col'])
    .reset_index(drop=True)
)
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with 5 columns. Drop two columns using `drop(columns=[...])`. Verify the resulting DataFrame has 3 columns.

??? success "Solution to Exercise 1"
    Drop columns and verify the result.

        import pandas as pd

        df = pd.DataFrame({
            'A': [1], 'B': [2], 'C': [3], 'D': [4], 'E': [5]
        })
        result = df.drop(columns=['B', 'D'])
        print(result.columns.tolist())
        assert len(result.columns) == 3

---

**Exercise 2.**
Create a DataFrame with rows indexed `[0, 1, 2, 3, 4]`. Drop rows at indices 1 and 3 using `drop([1, 3])`. Verify the remaining indices are `[0, 2, 4]`.

??? success "Solution to Exercise 2"
    Drop rows by index label.

        import pandas as pd

        df = pd.DataFrame({'val': [10, 20, 30, 40, 50]})
        result = df.drop([1, 3])
        print(result)
        assert result.index.tolist() == [0, 2, 4]

---

**Exercise 3.**
Create a DataFrame and attempt to drop a non-existent column. Use the `errors='ignore'` parameter to suppress the `KeyError`. Then drop the column without `errors='ignore'` to see the error.

??? success "Solution to Exercise 3"
    Use errors='ignore' to handle missing labels gracefully.

        import pandas as pd

        df = pd.DataFrame({'A': [1], 'B': [2]})
        result = df.drop(columns=['C'], errors='ignore')
        print(result)  # No error, df unchanged

        try:
            df.drop(columns=['C'])
        except KeyError as e:
            print(f"KeyError: {e}")
