# DataFrame Architecture

!!! tip "Mental Model"
    Under the hood, a DataFrame is not a 2D array -- it is a collection of 1D arrays (one per column) managed by a BlockManager. Each column can have a different dtype, and operations like adding or dropping columns rearrange pointers rather than copying data. Understanding this columnar layout explains why column operations are fast and row iterations are slow.

## Columnar Design

### 1. Structure

DataFrame is a dict-like container of Series:

```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4.0, 5.0, 6.0],
    'C': ['x', 'y', 'z']
})
```

### 2. Columns as Series

```python
col_a = df['A']
print(type(col_a))  # Series
print(col_a.dtype)  # int64

col_c = df['C']
print(col_c.dtype)  # object
```

### 3. Heterogeneous Types

Each column has its own dtype:

```python
print(df.dtypes)
# A     int64
# B   float64
# C    object
```

## Construction

### 1. From Dict

```python
data = {
    'name': ['Alice', 'Bob'],
    'age': [25, 30],
    'salary': [50000, 60000]
}
df = pd.DataFrame(data)
```

### 2. From Lists

```python
data = [
    [1, 4, 'x'],
    [2, 5, 'y'],
    [3, 6, 'z']
]
df = pd.DataFrame(data, columns=['A', 'B', 'C'])
```

### 3. From Records

```python
df = pd.DataFrame([
    {'name': 'Alice', 'age': 25},
    {'name': 'Bob', 'age': 30}
])
```

## Indexing

### 1. Column Selection

```python
df['A']          # Single column (Series)
df[['A', 'B']]   # Multiple columns (DataFrame)
```

### 2. Row Selection

```python
df.loc[0]        # By label
df.iloc[0]       # By position
df.loc[0:2]      # Slice by label
```

### 3. Boolean Indexing

```python
df[df['age'] > 25]  # Filter rows
```

## Operations

### 1. Column-wise

```python
df['D'] = df['A'] + df['B']  # New column
df.drop('D', axis=1, inplace=True)  # Remove column
```

### 2. Row-wise

```python
df.loc[3] = [4, 7, 'w']  # Add row
df = df.drop(3)  # Remove row
```

### 3. Aggregation

```python
df.sum()      # Sum each column
df.mean()     # Mean each column
df.describe() # Summary statistics
```


---

## Exercises

**Exercise 1.** Create a DataFrame from a dictionary with three columns and five rows. Print its shape, columns, and dtypes.

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

**Exercise 2.** Explain the relationship between a DataFrame and its constituent Series objects. How do you extract a single column as a Series?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas data structures and their relationships.

---

**Exercise 3.** Write code that creates a DataFrame and accesses rows using `.loc[]` (label-based) and `.iloc[]` (position-based). Show the difference.

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

**Exercise 4.** Create a DataFrame and add a new column computed from existing columns. Then delete a column using `del` or `.drop()`.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    df['c'] = df['a'] + df['b']
    df = df.drop(columns=['b'])
    print(df)
    ```
