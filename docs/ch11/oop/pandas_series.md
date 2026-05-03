# Series Object

!!! tip "Mental Model"
    A Series is a thin wrapper around a NumPy array plus an Index. The array holds the data, the Index provides labels, and the `name` attribute identifies which column it came from. When you do arithmetic between two Series, pandas aligns them by Index labels first -- this automatic alignment is the defining feature that separates Series from a plain array.

## Core Structure

### 1. Definition

A Series is a 1D labeled array:

```python
import pandas as pd

s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(type(s))  # <class 'pandas.core.series.Series'>
```

### 2. Components

```python
print(s.values)  # NumPy array [10 20 30]
print(s.index)   # Index(['a', 'b', 'c'])
print(s.dtype)   # dtype('int64')
```

### 3. vs NumPy Array

Series = Values (ndarray) + Index + Name

## Construction

### 1. From List

```python
s = pd.Series([1, 2, 3, 4])
print(s.index)  # RangeIndex(0, 4)
```

### 2. From Dict

```python
data = {'a': 10, 'b': 20, 'c': 30}
s = pd.Series(data)
```

### 3. From Scalar

```python
s = pd.Series(5, index=['a', 'b', 'c'])
# a    5
# b    5
# c    5
```

## Indexing

### 1. Label-based

```python
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
print(s['a'])  # 10
print(s[['a', 'c']])  # Multiple labels
```

### 2. Position-based

```python
print(s.iloc[0])  # 10
print(s.iloc[0:2])  # First two
```

### 3. Boolean Indexing

```python
print(s[s > 15])  # Elements > 15
```

## Operations

### 1. Arithmetic

```python
s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
s2 = pd.Series([10, 20, 30], index=['a', 'b', 'd'])
result = s1 + s2
# Aligns on index, NaN for 'c' and 'd'
```

### 2. Methods

```python
s = pd.Series([1, 2, 3, 4, 5])
print(s.mean())  # 3.0
print(s.std())   # 1.58
print(s.sum())   # 15
```

### 3. String Methods

```python
s = pd.Series(['hello', 'world', 'pandas'])
print(s.str.upper())
print(s.str.len())
```


---

## Exercises

**Exercise 1.** Create a Pandas Series from a list and from a dictionary. Print the values, index, and dtype of each.

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

**Exercise 2.** Explain the difference between a Pandas Series and a NumPy array. What does the index add?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas data structures and their relationships.

---

**Exercise 3.** Write code that performs element-wise arithmetic between two Series with different indices. What happens with non-matching indices?

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

**Exercise 4.** Create a Series and demonstrate three different ways to select elements: by label (`.loc`), by position (`.iloc`), and by boolean mask.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    df['c'] = df['a'] + df['b']
    df = df.drop(columns=['b'])
    print(df)
    ```
