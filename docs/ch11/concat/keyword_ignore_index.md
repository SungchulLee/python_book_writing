# Keyword - ignore_index

The `ignore_index` parameter resets the index of the concatenated result to a new RangeIndex.

!!! tip "Mental Model"
    When you stack two DataFrames, their original indices tag along, often producing duplicates like `[0, 1, 0, 1]`. Setting `ignore_index=True` throws away those old labels and renumbers from scratch -- `[0, 1, 2, 3]`. Use it whenever the original index values carry no meaning.

## Default Behavior

By default, original indices are preserved.

### 1. Preserved Indices

```python
import pandas as pd

df1 = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))

df = pd.concat([df1, df2])
print("ignore_index = False (default)")
print(df)
```

```
   A  B
0  1  2
1  3  4
0  5  6
1  7  8
```

### 2. Duplicate Indices

Notice indices 0 and 1 appear twice.

### 3. Potential Issues

Duplicate indices can cause problems with `loc`.

## ignore_index=True

Create a new sequential index.

### 1. Reset Index

```python
dg = pd.concat([df1, df2], ignore_index=True)
print("ignore_index = True")
print(dg)
```

```
   A  B
0  1  2
1  3  4
2  5  6
3  7  8
```

### 2. Unique Indices

New RangeIndex from 0 to n-1.

### 3. Clean Result

No duplicate indices; easier to work with.

## When to Use

Guidelines for ignore_index.

### 1. Use ignore_index=True When

```python
# Original index is meaningless (like auto-generated)
# Combining data from multiple files
# Need unique indices
# Index will be reset anyway
```

### 2. Keep Original Index When

```python
# Index has meaning (dates, IDs)
# Need to trace data back to source
# Using keys parameter instead
```

### 3. Common Pattern

```python
# Combine CSVs with ignore_index
all_data = pd.concat([
    pd.read_csv('data_2023.csv'),
    pd.read_csv('data_2024.csv')
], ignore_index=True)
```

## axis=1 Behavior

ignore_index works on both axes.

### 1. Reset Column Names

```python
df1 = pd.DataFrame([[1, 2]], columns=['A', 'B'])
df2 = pd.DataFrame([[3, 4]], columns=['C', 'D'])

result = pd.concat([df1, df2], axis=1, ignore_index=True)
print(result)
```

```
   0  1  2  3
0  1  2  3  4
```

### 2. Column Names Lost

Columns become 0, 1, 2, 3 instead of A, B, C, D.

### 3. Usually Not Wanted

For axis=1, typically keep column names.

## Comparison with reset_index

Two ways to achieve clean indices.

### 1. concat with ignore_index

```python
result = pd.concat([df1, df2], ignore_index=True)
```

### 2. reset_index After

```python
result = pd.concat([df1, df2]).reset_index(drop=True)
```

### 3. Equivalent Results

Both produce the same output; ignore_index is cleaner.


---

## Exercises

**Exercise 1.** Write code that concatenates two DataFrames and shows the difference between `ignore_index=False` (default) and `ignore_index=True`.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    result = pd.concat([df1, df2], ignore_index=True)
    print(result)
    ```

---

**Exercise 2.** Explain when `ignore_index=True` is useful. What problem does it solve?

??? success "Solution to Exercise 2"
    See the explanation in the main content. The key concept involves understanding how `pd.concat()` aligns data along the specified axis and handles mismatched indices or columns.

---

**Exercise 3.** Create two DataFrames with custom indices (e.g., starting from 100). Concatenate them with and without `ignore_index` and compare the index.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'C': [7, 8]})
    result = pd.concat([df1, df2], axis=0)
    print(result)
    ```

---

**Exercise 4.** Write code that concatenates DataFrames along `axis=1` with `ignore_index=True`. What gets reset in this case?

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2]}, index=[0, 1])
    df2 = pd.DataFrame({'A': [3, 4]}, index=[2, 3])
    result = pd.concat([df1, df2])
    print(result)
    ```
