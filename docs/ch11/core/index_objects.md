# Index Objects

Index objects provide axis labels for pandas data structures. Understanding indexes is fundamental to effective pandas usage.

!!! tip "Mental Model"
    An Index is an immutable array of labels attached to an axis. It serves two roles: it is the lookup key for label-based selection (`loc`), and it is the alignment mechanism that makes arithmetic between mismatched Series "just work." Every pandas operation begins by consulting the Index.

## Index Purpose

Index serves as an immutable container for axis labels.

### 1. Label Container

```python
import pandas as pd

idx = pd.Index(['a', 'b', 'c', 'd'])
s = pd.Series([10, 20, 30, 40], index=idx)
print(s)
```

```
a    10
b    20
c    30
d    40
dtype: int64
```

### 2. Immutability

Indexes cannot be modified in place:

```python
idx = pd.Index(['a', 'b', 'c'])
# idx[0] = 'x'  # TypeError: Index does not support mutable operations
```

### 3. Index Types

```python
pd.Index         # Generic index
pd.RangeIndex    # Memory-efficient integer range
pd.DatetimeIndex # Datetime labels
pd.MultiIndex    # Hierarchical index
pd.CategoricalIndex  # Categorical data
```

## Index Operations

Index supports set-like operations for data alignment.

### 1. Set Union

```python
idx1 = pd.Index(['a', 'b', 'c'])
idx2 = pd.Index(['b', 'c', 'd'])

print(idx1.union(idx2))
# Index(['a', 'b', 'c', 'd'], dtype='object')
```

### 2. Set Intersection

```python
print(idx1.intersection(idx2))
# Index(['b', 'c'], dtype='object')
```

### 3. Set Difference

```python
print(idx1.difference(idx2))
# Index(['a'], dtype='object')
```

## Automatic Alignment

pandas automatically aligns data based on index labels during operations.

### 1. Series Alignment

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([10, 20], index=['b', 'c'])
result = s1 + s2
print(result)
```

```
a     NaN
b    12.0
c    23.0
dtype: float64
```

### 2. DataFrame Alignment

```python
df1 = pd.DataFrame({'A': [1, 2]}, index=['x', 'y'])
df2 = pd.DataFrame({'A': [10, 20]}, index=['y', 'z'])
print(df1 + df2)
```

### 3. Fill Value

```python
result = s1.add(s2, fill_value=0)
```

## Reindexing

Change the index of a Series or DataFrame with `reindex`.

### 1. Basic Reindexing

```python
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s_new = s.reindex(['a', 'b', 'c', 'd'])
print(s_new)
```

```
a    1.0
b    2.0
c    3.0
d    NaN
dtype: float64
```

### 2. Fill Missing Values

```python
s_new = s.reindex(['a', 'b', 'c', 'd'], fill_value=0)
```

### 3. Forward Fill

```python
s_new = s.reindex(['a', 'b', 'c', 'd'], method='ffill')
```

## RangeIndex

Default integer index optimized for memory efficiency.

### 1. Automatic Creation

```python
s = pd.Series([10, 20, 30])
print(s.index)
# RangeIndex(start=0, stop=3, step=1)
```

### 2. Reset Index

```python
df = pd.DataFrame({'A': [1, 2, 3]}, index=['x', 'y', 'z'])
df_reset = df.reset_index(drop=True)
print(df_reset.index)
# RangeIndex(start=0, stop=3, step=1)
```

### 3. Memory Efficiency

RangeIndex stores only start, stop, and step, not individual values.

---

## Exercises

**Exercise 1.**
Create a `pd.Index` from a list of strings. Demonstrate that the Index is immutable by attempting to modify an element (it should raise a `TypeError`).

??? success "Solution to Exercise 1"
    Verify Index immutability.

        import pandas as pd

        idx = pd.Index(['a', 'b', 'c'])
        print(idx)
        try:
            idx[0] = 'z'
        except TypeError as e:
            print(f"TypeError: {e}")

---

**Exercise 2.**
Create two Index objects with overlapping values. Use `.intersection()`, `.union()`, and `.difference()` to perform set operations on them.

??? success "Solution to Exercise 2"
    Perform set operations on Index objects.

        import pandas as pd

        idx1 = pd.Index([1, 2, 3, 4])
        idx2 = pd.Index([3, 4, 5, 6])
        print("Intersection:", idx1.intersection(idx2).tolist())
        print("Union:", idx1.union(idx2).tolist())
        print("Difference:", idx1.difference(idx2).tolist())

---

**Exercise 3.**
Create a DataFrame and use `.set_index()` to set a column as the index. Then use `.reset_index()` to move the index back to a column. Verify the DataFrame is the same as the original.

??? success "Solution to Exercise 3"
    Round-trip set_index and reset_index.

        import pandas as pd

        df = pd.DataFrame({'id': [1, 2, 3], 'val': [10, 20, 30]})
        df_indexed = df.set_index('id')
        print("Indexed:\n", df_indexed)
        df_reset = df_indexed.reset_index()
        print("Reset:\n", df_reset)
        assert df.equals(df_reset)
