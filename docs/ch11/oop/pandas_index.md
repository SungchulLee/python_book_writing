# Index Objects

!!! tip "Mental Model"
    An Index is an immutable, hashable array that provides O(1) label lookups via an internal hash table. It is shared between a DataFrame and its columns, ensuring that label-based access and alignment are always consistent. Immutability guarantees that the hash table stays valid throughout the object's lifetime.

## Index Purpose

### 1. Label Container

Index provides axis labels:

```python
import pandas as pd

idx = pd.Index(['a', 'b', 'c', 'd'])
s = pd.Series([10, 20, 30, 40], index=idx)
```

### 2. Immutability

Indexes are immutable:

```python
idx = pd.Index(['a', 'b', 'c'])
# idx[0] = 'x'  # TypeError
```

### 3. Types

```python
pd.Index        # Generic
pd.RangeIndex   # Efficient range
pd.DatetimeIndex  # Datetime labels
pd.MultiIndex   # Hierarchical
```

## Index Operations

### 1. Set Operations

```python
idx1 = pd.Index(['a', 'b', 'c'])
idx2 = pd.Index(['b', 'c', 'd'])

print(idx1.union(idx2))  # ['a', 'b', 'c', 'd']
print(idx1.intersection(idx2))  # ['b', 'c']
print(idx1.difference(idx2))  # ['a']
```

### 2. Alignment

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([10, 20], index=['b', 'c'])
result = s1 + s2  # Aligns on index
```

### 3. Reindexing

```python
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s_new = s.reindex(['a', 'b', 'c', 'd'], fill_value=0)
```

## Datetime Index

### 1. Creation

```python
dates = pd.date_range('2023-01-01', periods=5)
s = pd.Series([10, 20, 30, 40, 50], index=dates)
```

### 2. Selection

```python
s['2023-01-01']  # Single date
s['2023-01-02':'2023-01-04']  # Range
```

### 3. Frequency

```python
dates = pd.date_range('2023-01-01', periods=10, freq='D')
```


---

## Exercises

**Exercise 1.** Create a DataFrame with a custom index using string labels. Demonstrate accessing rows by label with `.loc[]`.

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

**Exercise 2.** Explain the difference between `RangeIndex`, `Int64Index`, and custom string indices. When would you use each?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas data structures and their relationships.

---

**Exercise 3.** Write code that resets the index of a DataFrame with `reset_index()` and sets a column as the new index with `set_index()`.

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

**Exercise 4.** Create two DataFrames with different indices and show how Pandas aligns data by index during arithmetic operations.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    df['c'] = df['a'] + df['b']
    df = df.drop(columns=['b'])
    print(df)
    ```
