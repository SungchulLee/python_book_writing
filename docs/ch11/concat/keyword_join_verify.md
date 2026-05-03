# Keyword - join and verify_integrity

When concatenating DataFrames with `pd.concat`, mismatched columns can silently introduce `NaN` values, and duplicate index labels can go undetected. The `join` parameter controls how columns (or indices) that do not appear in all DataFrames are handled, while `verify_integrity` provides a safety check against duplicate index values in the result.

!!! tip "Mental Model"
    `join="outer"` keeps every column from every DataFrame, filling gaps with NaN. `join="inner"` keeps only the columns that appear in all DataFrames. `verify_integrity=True` is a safety net that raises an error if the resulting index has duplicates -- useful for catching accidental double-stacking.

```python
import pandas as pd
```

---

## join Parameter

The `join` parameter determines what happens to columns that exist in some DataFrames but not others. It accepts two values: `"outer"` (the default) and `"inner"`.

### Outer Join (Default)

With `join="outer"`, the result includes **all** columns from every DataFrame. Missing values are filled with `NaN`.

```python
df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"B": [5, 6], "C": [7, 8]})

result = pd.concat([df1, df2], join="outer", ignore_index=True)
print(result)
```

```
     A  B    C
0  1.0  3  NaN
1  2.0  4  NaN
2  NaN  5  7.0
3  NaN  6  8.0
```

Columns `A` and `C` appear in only one DataFrame, so the other gets `NaN` in those positions.

### Inner Join

With `join="inner"`, the result keeps **only** columns that appear in every DataFrame. No `NaN` values are introduced from column mismatch.

```python
result = pd.concat([df1, df2], join="inner", ignore_index=True)
print(result)
```

```
   B
0  3
1  4
2  5
3  6
```

Only column `B` is common to both DataFrames, so `A` and `C` are dropped.

### When to Use Each

| Situation | Recommended `join` |
|-----------|-------------------|
| DataFrames share all columns | Either (same result) |
| Some columns differ, keep all data | `"outer"` (default) |
| Some columns differ, keep only shared | `"inner"` |

!!! warning "Silent NaN Introduction"
    The default `join="outer"` can introduce `NaN` values without warning when DataFrames have different columns. If your downstream code does not handle `NaN`, consider using `join="inner"` or explicitly checking columns before concatenation.

---

## verify_integrity Parameter

Setting `verify_integrity=True` causes `pd.concat` to raise a `ValueError` if the resulting index contains duplicate values. This is useful as a sanity check when duplicate indices would indicate a data problem.

### Default Behavior (No Checking)

By default, `pd.concat` allows duplicate index values.

```python
df1 = pd.DataFrame({"A": [1, 2]}, index=[0, 1])
df2 = pd.DataFrame({"A": [3, 4]}, index=[0, 1])

result = pd.concat([df1, df2])
print(result)
```

```
   A
0  1
1  2
0  3
1  4
```

The result has duplicate index values (0 and 1 each appear twice), which is allowed by default.

### Enabling Integrity Check

```python
try:
    result = pd.concat([df1, df2], verify_integrity=True)
except ValueError as e:
    print(e)
# Indexes have overlapping values: Int64Index([0, 1], dtype='int64')
```

The call raises a `ValueError` because indices 0 and 1 appear in both DataFrames.

### Fixing Duplicate Indices

Two common approaches to resolve duplicate indices before or during concatenation:

```python
# Option 1: Reset indices with ignore_index
result = pd.concat([df1, df2], ignore_index=True)
print(result)
```

```
   A
0  1
1  2
2  3
3  4
```

```python
# Option 2: Use keys to create a hierarchical index
result = pd.concat([df1, df2], keys=["first", "second"])
print(result)
```

```
            A
first  0    1
       1    2
second 0    3
       1    4
```

Both approaches produce a result with unique index values.

---

## Combining join and verify_integrity

The two parameters work independently and can be used together.

```python
df1 = pd.DataFrame({"A": [1], "B": [2]}, index=["x"])
df2 = pd.DataFrame({"B": [3], "C": [4]}, index=["y"])

# Inner join + integrity check
result = pd.concat(
    [df1, df2],
    join="inner",
    verify_integrity=True
)
print(result)
```

```
   B
x  2
y  3
```

Here `join="inner"` keeps only column `B`, and `verify_integrity=True` confirms no duplicate indices exist.

---

## Summary

| Parameter | Values | Purpose |
|-----------|--------|---------|
| `join` | `"outer"` (default), `"inner"` | Controls column handling for mismatched DataFrames |
| `verify_integrity` | `False` (default), `True` | Raises error on duplicate index values |

**Key Takeaways**:

- `join="outer"` keeps all columns but may introduce `NaN`; `join="inner"` keeps only shared columns
- `verify_integrity=True` is a safety net that raises `ValueError` on duplicate indices
- Use `ignore_index=True` or `keys` to resolve duplicate indices before they cause problems
- These parameters apply to `pd.concat` only, not to `pd.merge` (which has its own join logic)


---

## Exercises

**Exercise 1.** Write code that concatenates two DataFrames with different columns using `join='inner'` and `join='outer'`. Compare the results.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    result = pd.concat([df1, df2], ignore_index=True)
    print(result)
    ```

---

**Exercise 2.** Explain what the `verify_integrity` parameter does in `pd.concat()`. What happens if there are duplicate index values?

??? success "Solution to Exercise 2"
    See the explanation in the main content. The key concept involves understanding how `pd.concat()` aligns data along the specified axis and handles mismatched indices or columns.

---

**Exercise 3.** Create two DataFrames with partially overlapping columns. Concatenate with `join='inner'` and show that only common columns are kept.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'C': [7, 8]})
    result = pd.concat([df1, df2], axis=0)
    print(result)
    ```

---

**Exercise 4.** Write code demonstrating that `pd.concat([df1, df2], verify_integrity=True)` raises an error when index values are duplicated.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2]}, index=[0, 1])
    df2 = pd.DataFrame({'A': [3, 4]}, index=[2, 3])
    result = pd.concat([df1, df2])
    print(result)
    ```
