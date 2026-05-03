# concat Method

The `concat()` function concatenates pandas objects along a particular axis, stacking DataFrames vertically or horizontally.

!!! tip "Mental Model"
    `pd.concat` is like stacking blocks. With `axis=0` (default) you stack vertically -- more rows. With `axis=1` you stack horizontally -- more columns. No key matching happens; DataFrames are simply glued along the chosen axis, and pandas aligns by index labels to decide where NaN fills appear.

## Basic Usage

Concatenate DataFrames vertically.

### 1. Vertical Concatenation

```python
import pandas as pd

df1 = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
print(df1)

df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
print(df2)

df = pd.concat([df1, df2])
print(df)
```

```
   A  B
0  1  2
1  3  4
0  5  6
1  7  8
```

### 2. List of DataFrames

```python
pd.concat([df1, df2, df3, df4])
```

### 3. Index Preserved

Original indices are kept (may have duplicates).

## LeetCode Example: Friend Requests

Concatenate two columns into one Series.

### 1. Sample Data

```python
request_accepted = pd.DataFrame({
    'requester_id': [1, 2, 3, 4, 1, 2],
    'accepter_id': [2, 3, 4, 1, 3, 4]
})
```

### 2. Concatenate Columns

```python
combined_ids = pd.concat([
    request_accepted['requester_id'],
    request_accepted['accepter_id']
])
print(combined_ids)
```

```
0    1
1    2
2    3
3    4
4    1
5    2
0    2
1    3
2    4
3    1
4    3
5    4
dtype: int64
```

### 3. Count Occurrences

```python
friend_counts = combined_ids.value_counts()
```

## Horizontal Concatenation

Stack DataFrames side by side.

### 1. axis=1

```python
df1 = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('CD'))

dg = pd.concat([df1, df2], axis=1)
print(dg)
```

```
   A  B  C  D
0  1  2  5  6
1  3  4  7  8
```

### 2. Index Alignment

```python
# When indices differ, NaN fills missing values
```

### 3. Use join Parameter

```python
pd.concat([df1, df2], axis=1, join='inner')  # Only matching indices
```

## Handling Mismatched Columns

Concat with different column structures.

### 1. Union of Columns

```python
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'B': [5, 6], 'C': [7, 8]})

result = pd.concat([df1, df2])
# Columns: A, B, C with NaN where missing
```

### 2. join='inner'

```python
result = pd.concat([df1, df2], join='inner')
# Only column B (common to both)
```

### 3. Specify Columns

```python
# Ensure same columns before concat
df2 = df2.reindex(columns=df1.columns)
```

## keys Parameter

Add hierarchical index to identify sources.

### 1. Label Sources

```python
result = pd.concat([df1, df2], keys=['first', 'second'])
```

### 2. MultiIndex Result

```python
print(result.index)
# MultiIndex([('first', 0), ('first', 1), ...])
```

### 3. Access by Key

```python
result.loc['first']  # Get first DataFrame's rows
```


---

## Exercises

**Exercise 1.** Write code that creates two DataFrames with the same columns and concatenates them vertically using `pd.concat()`. Reset the index with `ignore_index=True`.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    result = pd.concat([df1, df2], ignore_index=True)
    print(result)
    ```

---

**Exercise 2.** Explain the difference between `pd.concat()` with `axis=0` and `axis=1`. What does each produce?

??? success "Solution to Exercise 2"
    See the explanation in the main content. The key concept involves understanding how `pd.concat()` aligns data along the specified axis and handles mismatched indices or columns.

---

**Exercise 3.** Write code that concatenates three DataFrames and uses the `keys` parameter to create a hierarchical index identifying the source of each row.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'C': [7, 8]})
    result = pd.concat([df1, df2], axis=0)
    print(result)
    ```

---

**Exercise 4.** Create two DataFrames with overlapping and non-overlapping columns. Concatenate them and show what happens to the non-matching columns.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2]}, index=[0, 1])
    df2 = pd.DataFrame({'A': [3, 4]}, index=[2, 3])
    result = pd.concat([df1, df2])
    print(result)
    ```
