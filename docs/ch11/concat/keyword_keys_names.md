# Keyword - keys and names

After concatenating multiple DataFrames, it is often necessary to trace which original DataFrame each row came from. The `keys` parameter of `pd.concat` creates a hierarchical MultiIndex that labels each group, while the `names` parameter assigns meaningful names to the MultiIndex levels. Together, they provide structured provenance tracking in the concatenated result.

!!! tip "Mental Model"
    `keys` stamps each source DataFrame with a label before stacking, creating a MultiIndex that preserves provenance. `names` then gives that outer index level a meaningful column-like name. Together they answer "which original table did this row come from?" at any point downstream.

```python
import pandas as pd
```

---

## keys Parameter

Passing a list of labels to `keys` creates a MultiIndex on the concatenation axis, with the outer level identifying the source DataFrame.

### Basic Usage

```python
df1 = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
df2 = pd.DataFrame({"A": [5, 6], "B": [7, 8]})

result = pd.concat([df1, df2], keys=["first", "second"])
print(result)
```

```
          A  B
first  0  1  3
       1  2  4
second 0  5  7
       1  6  8
```

The result has a two-level index. The outer level contains the key labels (`"first"`, `"second"`), and the inner level preserves the original DataFrame indices.

### Selecting by Key

The hierarchical index enables selection of individual groups using `.loc`.

```python
# Select all rows from the "first" group
print(result.loc["first"])
```

```
   A  B
0  1  3
1  2  4
```

```python
# Select a specific row: group "second", original index 1
print(result.loc[("second", 1)])
```

```
A    6
B    8
Name: (second, 1), dtype: int64
```

### Keys with Column Concatenation

When concatenating along `axis=1`, `keys` label the outer level of a MultiIndex on columns.

```python
df1 = pd.DataFrame({"val": [1, 2]}, index=["x", "y"])
df2 = pd.DataFrame({"val": [3, 4]}, index=["x", "y"])

result = pd.concat([df1, df2], axis=1, keys=["source_A", "source_B"])
print(result)
```

```
  source_A source_B
       val      val
x        1        3
y        2        4
```

---

## names Parameter

The `names` parameter assigns labels to the levels of the MultiIndex created by `keys`. Without `names`, the levels are unnamed.

### Adding Level Names

```python
result = pd.concat(
    [df1, df2],
    keys=["first", "second"],
    names=["group", "row"]
)
print(result)
```

```
            A  B
group  row
first  0    1  3
       1    2  4
second 0    5  7
       1    6  8
```

The index levels are now labeled `"group"` and `"row"`, which makes the structure self-documenting.

### Accessing Level Names

```python
print(result.index.names)  # ['group', 'row']

# Reset specific level to a column
reset = result.reset_index(level="group")
print(reset)
```

```
      group  A  B
row
0     first  1  3
1     first  2  4
0    second  5  7
1    second  6  8
```

---

## Practical Example

A common use case is combining data from multiple files or time periods while preserving the source information.

```python
# Simulating data from three quarters
q1 = pd.DataFrame({"revenue": [100, 200], "cost": [80, 150]})
q2 = pd.DataFrame({"revenue": [120, 220], "cost": [90, 160]})
q3 = pd.DataFrame({"revenue": [130, 250], "cost": [95, 170]})

annual = pd.concat(
    [q1, q2, q3],
    keys=["Q1", "Q2", "Q3"],
    names=["quarter", "store"]
)
print(annual)
```

```
               revenue  cost
quarter store
Q1      0          100    80
        1          200   150
Q2      0          120    90
        1          220   160
Q3      0          130    95
        1          250   170
```

```python
# Compute total revenue per quarter
print(annual.groupby(level="quarter")["revenue"].sum())
```

```
quarter
Q1    300
Q2    340
Q3    380
Name: revenue, dtype: int64
```

---

## keys Without names

If only `keys` is provided, the MultiIndex levels have `None` as their names. This still works but makes downstream code less readable.

```python
result = pd.concat([df1, df2], keys=["first", "second"])
print(result.index.names)  # [None, None]

# Compare with named levels
result = pd.concat(
    [df1, df2],
    keys=["first", "second"],
    names=["source", "idx"]
)
print(result.index.names)  # ['source', 'idx']
```

!!! tip "Always Name Your Levels"
    Specifying `names` alongside `keys` costs nothing and makes the resulting DataFrame easier to work with in `groupby`, `reset_index`, and `.loc` operations.

---

## Summary

| Parameter | Purpose | Default |
|-----------|---------|---------|
| `keys` | Create MultiIndex with group labels on the concatenation axis | `None` (no hierarchical index) |
| `names` | Assign names to the MultiIndex levels | `None` (unnamed levels) |

**Key Takeaways**:

- `keys` adds a hierarchical MultiIndex that identifies which source DataFrame each row (or column) came from
- `names` labels the MultiIndex levels for readability and downstream operations
- Use `.loc` with tuple indexing to select specific groups or rows from the keyed result
- When concatenating along `axis=1`, `keys` and `names` apply to the column MultiIndex instead
- Always pair `keys` with `names` to keep the result self-documenting


---

## Exercises

**Exercise 1.** Write code that uses `keys=['source_a', 'source_b']` in `pd.concat()` to create a MultiIndex identifying the origin of each row.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    result = pd.concat([df1, df2], ignore_index=True)
    print(result)
    ```

---

**Exercise 2.** Explain the purpose of the `names` parameter in `pd.concat()`. How does it relate to `keys`?

??? success "Solution to Exercise 2"
    See the explanation in the main content. The key concept involves understanding how `pd.concat()` aligns data along the specified axis and handles mismatched indices or columns.

---

**Exercise 3.** Concatenate three DataFrames with `keys` and `names` parameters. Show how to select all rows from a specific source using `.loc`.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'C': [7, 8]})
    result = pd.concat([df1, df2], axis=0)
    print(result)
    ```

---

**Exercise 4.** Write code that concatenates along `axis=1` with `keys` to create a MultiIndex for columns instead of rows.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df1 = pd.DataFrame({'A': [1, 2]}, index=[0, 1])
    df2 = pd.DataFrame({'A': [3, 4]}, index=[2, 3])
    result = pd.concat([df1, df2])
    print(result)
    ```
