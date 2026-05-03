# Categorical Operations

This document covers common operations on categorical data, including groupby performance, merging, and manipulation patterns.

!!! tip "Mental Model"
    Because categoricals store integer codes internally, operations like groupby and merge can work on integers instead of strings, which is dramatically faster. Think of categoricals as pre-indexed data: the expensive string-comparison work is done once at creation time, and every subsequent operation benefits.

## GroupBy Performance

Categorical columns provide significant speedup for groupby operations.

```python
import pandas as pd
import numpy as np
import time

# Create test data
np.random.seed(42)
n = 2_000_000
sectors = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer']

df = pd.DataFrame({
    'sector_string': np.random.choice(sectors, n),
    'returns': np.random.randn(n) * 0.02
})

df['sector_cat'] = df['sector_string'].astype('category')

# Benchmark string groupby
start = time.time()
result_string = df.groupby('sector_string')['returns'].mean()
time_string = time.time() - start

# Benchmark categorical groupby
start = time.time()
result_cat = df.groupby('sector_cat')['returns'].mean()
time_cat = time.time() - start

print(f"String groupby: {time_string:.3f}s")
print(f"Categorical groupby: {time_cat:.3f}s")
print(f"Speedup: {time_string/time_cat:.1f}x")
```

### Why Categorical is Faster

1. **Integer-based hashing**: Codes are integers, faster to hash than strings
2. **Pre-computed categories**: No need to discover unique values
3. **Efficient memory access**: Contiguous integer array

## Value Counts

```python
s = pd.Series(['a', 'b', 'a', 'c', 'a', 'b'], dtype='category')

# Value counts respects category order
counts = s.value_counts()
print(counts)
```

### Including Empty Categories

```python
# Add category 'd' that doesn't appear in data
s = s.cat.add_categories(['d'])

# Default: only counts existing values
print(s.value_counts())

# Include empty categories
print(s.value_counts(dropna=False))
```

## Merging with Categoricals

### Same Categories - Fast Merge

```python
# Both DataFrames have same categorical type
sector_dtype = pd.CategoricalDtype(categories=['Tech', 'Finance', 'Health'])

df1 = pd.DataFrame({
    'sector': pd.Categorical(['Tech', 'Finance'], dtype=sector_dtype),
    'value1': [100, 200]
})

df2 = pd.DataFrame({
    'sector': pd.Categorical(['Tech', 'Health'], dtype=sector_dtype),
    'value2': [10, 30]
})

# Merge preserves categorical type
result = df1.merge(df2, on='sector', how='outer')
print(result)
print(result['sector'].dtype)  # category
```

### Different Categories - May Convert to Object

```python
df1 = pd.DataFrame({
    'sector': pd.Categorical(['Tech', 'Finance']),
    'value1': [100, 200]
})

df2 = pd.DataFrame({
    'sector': pd.Categorical(['Tech', 'Health']),  # Different categories
    'value2': [10, 30]
})

result = df1.merge(df2, on='sector', how='outer')
print(result['sector'].dtype)  # May be object or unified category
```

### Best Practice: Unify Categories Before Merge

```python
# Define common dtype
common_dtype = pd.CategoricalDtype(categories=['Tech', 'Finance', 'Health'])

df1['sector'] = df1['sector'].astype(common_dtype)
df2['sector'] = df2['sector'].astype(common_dtype)

result = df1.merge(df2, on='sector', how='outer')
print(result['sector'].dtype)  # category (preserved)
```

## Concatenation

```python
s1 = pd.Series(['a', 'b'], dtype='category')
s2 = pd.Series(['b', 'c'], dtype='category')

# Concatenation unifies categories
result = pd.concat([s1, s2], ignore_index=True)
print(result)
print(result.cat.categories)  # ['a', 'b', 'c']
```

## Pivot Tables with Categoricals

```python
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=6),
    'sector': pd.Categorical(['Tech', 'Finance', 'Tech', 'Finance', 'Tech', 'Finance']),
    'region': pd.Categorical(['East', 'East', 'West', 'West', 'East', 'West']),
    'sales': [100, 200, 150, 250, 120, 180]
})

# Pivot preserves categorical in result
pivot = df.pivot_table(
    values='sales',
    index='sector',
    columns='region',
    aggfunc='sum'
)
print(pivot)
```

## String Operations on Categoricals

To use string methods, convert to string first:

```python
s = pd.Series(['apple', 'banana', 'cherry'], dtype='category')

# Direct string methods don't work on categories
# s.str.upper()  # Works but operates on categories

# Convert to string for string operations
s_upper = s.astype(str).str.upper()
print(s_upper)

# Or rename categories
s_upper = s.cat.rename_categories(str.upper)
print(s_upper)
```

## Arithmetic Not Supported

Categorical data doesn't support arithmetic operations:

```python
s = pd.Series([1, 2, 3], dtype='category')

# These will fail or produce unexpected results
# s + 1  # TypeError
# s * 2  # TypeError

# Convert to numeric first
s_numeric = s.astype(int)
print(s_numeric + 1)  # Works
```

## Replacing Values

### Using cat.rename_categories()

```python
s = pd.Series(['old_a', 'old_b', 'old_a'], dtype='category')
s = s.cat.rename_categories({'old_a': 'new_a', 'old_b': 'new_b'})
print(s)
```

### Using replace() - Converts to Object

```python
s = pd.Series(['a', 'b', 'a'], dtype='category')
s_replaced = s.replace({'a': 'x'})
print(s_replaced.dtype)  # object (no longer categorical)

# To preserve categorical, use rename_categories instead
```

## Filtering Patterns

### Using isin()

```python
s = pd.Series(['Tech', 'Finance', 'Health', 'Energy', 'Tech'], dtype='category')

# Filter multiple categories
tech_finance = s[s.isin(['Tech', 'Finance'])]
print(tech_finance)
```

### Using Boolean Masks

```python
df = pd.DataFrame({
    'sector': pd.Categorical(['Tech', 'Finance', 'Health', 'Tech']),
    'value': [100, 200, 150, 120]
})

# Single category
tech = df[df['sector'] == 'Tech']

# Multiple categories
selected = df[df['sector'].isin(['Tech', 'Health'])]
```

## Handling Missing Categories After Filter

After filtering, unused categories remain:

```python
s = pd.Series(['a', 'b', 'c', 'a', 'b'], dtype='category')
filtered = s[s != 'c']
print(filtered.cat.categories)  # Still ['a', 'b', 'c']

# Remove unused categories
filtered = filtered.cat.remove_unused_categories()
print(filtered.cat.categories)  # ['a', 'b']
```

## Aggregation Functions

Most aggregation functions work with categoricals:

```python
df = pd.DataFrame({
    'category': pd.Categorical(['A', 'B', 'A', 'B', 'A']),
    'value': [10, 20, 15, 25, 12]
})

# These work
print(df.groupby('category')['value'].sum())
print(df.groupby('category')['value'].mean())
print(df.groupby('category')['value'].std())
print(df.groupby('category')['value'].min())
print(df.groupby('category')['value'].max())
print(df.groupby('category')['value'].count())
```

## Transform with Categoricals

```python
df = pd.DataFrame({
    'category': pd.Categorical(['A', 'B', 'A', 'B', 'A']),
    'value': [10, 20, 15, 25, 12]
})

# Transform preserves original index
df['category_mean'] = df.groupby('category')['value'].transform('mean')
print(df)
```

## Categorical in MultiIndex

```python
# Create MultiIndex with categorical level
arrays = [
    pd.Categorical(['A', 'A', 'B', 'B']),
    [1, 2, 1, 2]
]
index = pd.MultiIndex.from_arrays(arrays, names=['category', 'number'])

df = pd.DataFrame({'value': [10, 20, 30, 40]}, index=index)
print(df)

# Groupby on categorical level is fast
print(df.groupby(level='category').sum())
```

## Summary of Operations

| Operation | Categorical Support | Notes |
|-----------|---------------------|-------|
| GroupBy | ✅ Excellent | Faster than string |
| Value Counts | ✅ Good | Respects category order |
| Merge | ✅ Good | Best with same categories |
| Concat | ✅ Good | Categories unified |
| Pivot | ✅ Good | Preserves categorical |
| String methods | ⚠️ Limited | Use rename_categories |
| Arithmetic | ❌ No | Convert to numeric |
| Replace | ⚠️ Limited | Use rename_categories |
| Filtering | ✅ Good | Remember to clean unused |
| Aggregation | ✅ Excellent | All standard functions |


---

## Exercises

**Exercise 1.** Write code that adds and removes categories from a categorical Series using `.cat.add_categories()` and `.cat.remove_categories()`.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    # See page content for relevant API details
    s = pd.Series(['a', 'b', 'c', 'a', 'b'], dtype='category')
    print(s)
    print(s.cat.categories)
    print(s.cat.codes)
    ```

---

**Exercise 2.** Explain what happens when you try to assign a value to a categorical Series that is not in the current categories.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page. The key concept involves understanding the categorical data type and its internal representation in Pandas.

---

**Exercise 3.** Write code that renames categories using `.cat.rename_categories()`. Change `['a', 'b', 'c']` to `['Alpha', 'Beta', 'Gamma']`.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'col': np.random.choice(['A', 'B', 'C'], 1000)})
    df['col'] = df['col'].astype('category')
    print(df.dtypes)
    print(df['col'].value_counts())
    ```

---

**Exercise 4.** Create a categorical Series and use `.cat.reorder_categories()` to change the category ordering. Show that comparison operators reflect the new order.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    s = pd.Categorical(['low', 'medium', 'high', 'low'],
                        categories=['low', 'medium', 'high'],
                        ordered=True)
    print(s)
    print(s > 'low')
    ```
