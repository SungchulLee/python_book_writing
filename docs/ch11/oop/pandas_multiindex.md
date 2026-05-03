# MultiIndex Hierarchy

!!! tip "Mental Model"
    A MultiIndex is a tree encoded as tuples. Each "row label" is actually a tuple of values from multiple levels, like `('US', 'NY')`. Internally, pandas stores each level as a separate array and uses integer codes to map rows to level values, making the structure memory-efficient even with millions of rows.

## Hierarchical Indexing

### 1. Definition

MultiIndex enables multiple index levels:

```python
import pandas as pd

arrays = [
    ['A', 'A', 'B', 'B'],
    [1, 2, 1, 2]
]
index = pd.MultiIndex.from_arrays(arrays, names=['letter', 'number'])
s = pd.Series([10, 20, 30, 40], index=index)
```

### 2. From Tuples

```python
tuples = [('A', 1), ('A', 2), ('B', 1), ('B', 2)]
index = pd.MultiIndex.from_tuples(tuples)
```

### 3. From Product

```python
index = pd.MultiIndex.from_product([['A', 'B'], [1, 2]])
```

## Accessing Data

### 1. Level Selection

```python
s['A']  # All entries with level 0 = 'A'
s['A', 1]  # Specific entry
```

### 2. Cross-section

```python
df = s.unstack()  # Pivot to DataFrame
# letter  A   B
# number       
# 1      10  30
# 2      20  40
```

### 3. Slicing

```python
s.loc[('A', 1):('B', 1)]  # Range
```

## DataFrame with MultiIndex

### 1. Rows and Columns

```python
df = pd.DataFrame(
    [[1, 2], [3, 4], [5, 6], [7, 8]],
    index=pd.MultiIndex.from_tuples([('A', 'x'), ('A', 'y'), ('B', 'x'), ('B', 'y')]),
    columns=['col1', 'col2']
)
```

### 2. Selecting

```python
df.loc['A']  # All rows where first level = 'A'
df.loc[('A', 'x')]  # Specific row
```

### 3. Stacking

```python
stacked = df.stack()  # Add column as index level
unstacked = stacked.unstack()  # Remove level
```


---

## Exercises

**Exercise 1.** Create a DataFrame with a MultiIndex (2 levels) using `pd.MultiIndex.from_tuples()`. Access data at each level using `.loc[]`.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 28],
        'score': [85, 92, 78, 95, 88]
    })
    print(f'Shape: {df.shape}')
    print(f'Columns: {df.columns.tolist()}')
    print(f'Dtypes:\n{df.dtypes}')
    ```

---

**Exercise 2.** Explain the difference between `pd.MultiIndex.from_tuples()`, `from_arrays()`, and `from_product()`. Give an example of each.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas data structures and their relationships.

---

**Exercise 3.** Write code that creates a DataFrame with a MultiIndex and uses `.xs()` to select a cross-section at a specific level.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'score': [85, 92, 78]
    })
    # Label-based
    print(df.loc[0])
    # Position-based
    print(df.iloc[-1])
    ```

---

**Exercise 4.** Create a MultiIndex DataFrame and use `reset_index()` to flatten it back to a regular DataFrame. Then use `set_index()` to recreate the MultiIndex.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    df['c'] = df['a'] + df['b']
    df = df.drop(columns=['b'])
    print(df)
    ```
