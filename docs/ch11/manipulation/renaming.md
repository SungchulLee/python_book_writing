# Renaming Axes

The `rename()` method changes labels of axes (columns or index). Clear, descriptive names improve code readability and data understanding.

!!! tip "Mental Model"
    `rename()` swaps out axis labels without touching the data. Pass a dict of `{old_name: new_name}` pairs to selectively rename columns or index labels. It is a metadata-only operation -- the underlying arrays stay in place, only the labels change.

## Column Renaming

Rename DataFrame columns.

### 1. Dictionary Mapping

```python
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30]
})

df.rename(columns={'Name': 'First Name'}, inplace=True)
print(df)
```

```
  First Name  Age
0      Alice   25
1        Bob   30
```

### 2. Multiple Columns

```python
df.rename(columns={
    'col_a': 'Column A',
    'col_b': 'Column B',
    'col_c': 'Column C'
})
```

### 3. Function Mapping

```python
df.rename(columns=str.upper)      # All uppercase
df.rename(columns=str.lower)      # All lowercase
df.rename(columns=lambda x: x.strip())  # Remove whitespace
```

## Index Renaming

Rename row labels.

### 1. Dictionary Mapping

```python
df = pd.DataFrame({
    'A': [1, 2, 3]
}, index=['row1', 'row2', 'row3'])

df.rename(index={'row1': 'first_row'})
```

### 2. Function Mapping

```python
df.rename(index=str.upper)
```

### 3. Both Axes

```python
df.rename(
    columns={'A': 'Column A'},
    index={'row1': 'Row 1'}
)
```

## set_axis Method

Replace all labels at once.

### 1. Replace Columns

```python
df.set_axis(['new_col1', 'new_col2'], axis=1)
```

### 2. Replace Index

```python
df.set_axis(['a', 'b', 'c'], axis=0)
```

### 3. Must Match Length

```python
# Number of new labels must equal existing labels
```

## columns Property

Direct assignment to columns attribute.

### 1. Replace All Columns

```python
df.columns = ['new_name1', 'new_name2']
```

### 2. List Comprehension

```python
df.columns = [col.replace(' ', '_') for col in df.columns]
```

### 3. Prefix and Suffix

```python
df.columns = ['prefix_' + col for col in df.columns]
df.columns = [col + '_suffix' for col in df.columns]
```

## add_prefix and add_suffix

Add text to all column names.

### 1. Add Prefix

```python
df.add_prefix('2024_')
```

```
   2024_A  2024_B
0       1       4
1       2       5
```

### 2. Add Suffix

```python
df.add_suffix('_value')
```

### 3. Chaining

```python
df.add_prefix('raw_').add_suffix('_v1')
```

## Practical Examples

Common renaming scenarios.

### 1. Clean Column Names

```python
def clean_column_name(name):
    return (name
        .lower()
        .strip()
        .replace(' ', '_')
        .replace('-', '_'))

df.rename(columns=clean_column_name)
```

### 2. Financial Data

```python
df.rename(columns={
    'Open': 'open_price',
    'High': 'high_price',
    'Low': 'low_price',
    'Close': 'close_price',
    'Volume': 'trading_volume'
})
```

### 3. Multi-source Merge

```python
# Add source identifier before merge
df1.add_suffix('_source1')
df2.add_suffix('_source2')
pd.merge(df1, df2, left_index=True, right_index=True)
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with columns `'col_a'`, `'col_b'`, `'col_c'`. Rename them to `'Column A'`, `'Column B'`, `'Column C'` using a dictionary with `rename(columns=...)`.

??? success "Solution to Exercise 1"
    Rename columns using a dictionary.

        import pandas as pd

        df = pd.DataFrame({'col_a': [1], 'col_b': [2], 'col_c': [3]})
        df = df.rename(columns={'col_a': 'Column A', 'col_b': 'Column B', 'col_c': 'Column C'})
        print(df.columns.tolist())

---

**Exercise 2.**
Given a DataFrame with uppercase column names, use `rename(columns=str.lower)` to convert all column names to lowercase. Then use a lambda to replace spaces with underscores.

??? success "Solution to Exercise 2"
    Use functions to transform column names.

        import pandas as pd

        df = pd.DataFrame({'FIRST NAME': [1], 'LAST NAME': [2], 'AGE GROUP': [3]})
        df = df.rename(columns=str.lower)
        print(df.columns.tolist())
        df = df.rename(columns=lambda x: x.replace(' ', '_'))
        print(df.columns.tolist())

---

**Exercise 3.**
Create a DataFrame with a default `RangeIndex`. Use `rename(index=...)` with a dictionary to rename specific row indices (e.g., `{0: 'first', 1: 'second'}`). Verify the index changed for those rows.

??? success "Solution to Exercise 3"
    Rename specific index labels using a dictionary.

        import pandas as pd

        df = pd.DataFrame({'A': [10, 20, 30]})
        df = df.rename(index={0: 'first', 1: 'second'})
        print(df)
        assert df.index[0] == 'first'
        assert df.index[1] == 'second'
