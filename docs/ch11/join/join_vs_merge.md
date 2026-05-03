# join vs merge

Pandas provides two overlapping methods for combining DataFrames by matching key values: `DataFrame.join` and `pd.merge` (or equivalently `DataFrame.merge`). Both perform database-style joins, but they differ in their defaults and typical use cases. Understanding the distinction avoids confusion when choosing between them.

!!! tip "Mental Model"
    `join` defaults to index-on-index with a left join; `merge` defaults to column-on-column with an inner join. Both produce the same result when configured identically. Use `join` when your keys live in the index, and `merge` when they live in columns.

```python
import pandas as pd
```

---

## Quick Comparison

| Feature | `DataFrame.join` | `pd.merge` / `DataFrame.merge` |
|---------|-----------------|-------------------------------|
| Default join key | Caller's index + other's index | Common column names |
| Default join type | Left join | Inner join |
| Column overlap handling | `lsuffix` / `rsuffix` parameters | `suffixes` parameter |
| Joining on columns | Requires `on` parameter | Default behavior |
| Multiple DataFrames | Supports list of DataFrames | Two DataFrames only |
| Typical use | Index-aligned joins | Column-based joins |

---

## DataFrame.join — Index-Based by Default

`DataFrame.join` joins the caller with another DataFrame (or list of DataFrames) using the **index** of the other DataFrame as the join key. The caller's index is used by default, or a column can be specified via `on`.

```python
df_left = pd.DataFrame(
    {"revenue": [100, 200, 300]},
    index=["store_A", "store_B", "store_C"]
)

df_right = pd.DataFrame(
    {"region": ["East", "West", "East"]},
    index=["store_A", "store_B", "store_D"]
)

# join uses the index of both DataFrames
result = df_left.join(df_right)
print(result)
```

```
         revenue region
store_A      100   East
store_B      200   West
store_C      300    NaN
```

The default is a **left join**: all rows from the left DataFrame are kept, and non-matching rows get `NaN`.

---

## pd.merge — Column-Based by Default

`pd.merge` joins two DataFrames on **column values** by default. It finds columns with the same name in both DataFrames and uses them as join keys.

```python
df_orders = pd.DataFrame({
    "store": ["store_A", "store_B", "store_C"],
    "revenue": [100, 200, 300]
})

df_regions = pd.DataFrame({
    "store": ["store_A", "store_B", "store_D"],
    "region": ["East", "West", "East"]
})

# merge uses shared column "store" as the join key
result = pd.merge(df_orders, df_regions)
print(result)
```

```
     store  revenue region
0  store_A      100   East
1  store_B      200   West
```

The default is an **inner join**: only rows with matching keys in both DataFrames are kept.

---

## Same Result, Different Syntax

The two methods can produce identical results. The following example demonstrates how to achieve the same left join using both approaches.

### Using join

```python
df_left = pd.DataFrame(
    {"value": [1, 2, 3]},
    index=["a", "b", "c"]
)

df_right = pd.DataFrame(
    {"label": ["X", "Y"]},
    index=["a", "b"]
)

result_join = df_left.join(df_right, how="left")
print(result_join)
```

```
   value label
a      1     X
b      2     Y
c      3   NaN
```

### Using merge

```python
result_merge = pd.merge(
    df_left, df_right,
    left_index=True, right_index=True,
    how="left"
)
print(result_merge)
```

```
   value label
a      1     X
b      2     Y
c      3   NaN
```

Both produce the same output. The `join` version is shorter when joining on indices; the `merge` version requires explicit `left_index=True, right_index=True`.

---

## Handling Column Name Overlaps

When both DataFrames share a column name that is not a join key, the two methods use different parameter names for suffixes.

### join: lsuffix and rsuffix

```python
df1 = pd.DataFrame({"val": [1, 2]}, index=["a", "b"])
df2 = pd.DataFrame({"val": [3, 4]}, index=["a", "b"])

result = df1.join(df2, lsuffix="_left", rsuffix="_right")
print(result)
```

```
   val_left  val_right
a         1          3
b         2          4
```

### merge: suffixes

```python
result = pd.merge(
    df1, df2,
    left_index=True, right_index=True,
    suffixes=("_left", "_right")
)
print(result)
```

```
   val_left  val_right
a         1          3
b         2          4
```

---

## When to Use Each

Use the following decision guide.

1. **Join on index values** — prefer `DataFrame.join` (shorter syntax, left join default)
2. **Join on column values** — prefer `pd.merge` (designed for column-based keys)
3. **Join multiple DataFrames at once** — use `DataFrame.join` with a list
4. **Need full SQL-style control** (left_on, right_on, indicator) — use `pd.merge`

!!! tip "Rule of Thumb"
    If the join key is in the index, use `join`. If the join key is in a column, use `merge`.

---

## Summary

| Aspect | `DataFrame.join` | `pd.merge` |
|--------|-----------------|-----------|
| Default key | Index | Shared column names |
| Default how | `"left"` | `"inner"` |
| Suffix params | `lsuffix`, `rsuffix` | `suffixes` |
| Multiple inputs | Yes (list) | No (two only) |
| Best for | Index-based joins | Column-based joins |

**Key Takeaways**:

- `join` defaults to index-based left joins; `merge` defaults to column-based inner joins
- Both can produce identical results, but the syntax differs
- `join` is more concise for index joins; `merge` is more flexible for column joins
- Use `lsuffix`/`rsuffix` with `join` and `suffixes` with `merge` to handle overlapping column names
- `join` accepts a list of DataFrames; `merge` only works with two at a time

---

## Exercises

**Exercise 1.**
Create two DataFrames with a shared column `'key'`. Combine them using `pd.merge()` (the default inner join). Then achieve the same result using `.join()` by first setting `'key'` as the index of both DataFrames.

??? success "Solution to Exercise 1"
    Achieve the same result with merge and join.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'val1': [1, 2, 3]})
        df2 = pd.DataFrame({'key': ['a', 'b', 'd'], 'val2': [4, 5, 6]})

        # Using merge (default inner join on shared column)
        result_merge = pd.merge(df1, df2, on='key')
        print("merge:\n", result_merge)

        # Using join (set key as index first)
        result_join = df1.set_index('key').join(df2.set_index('key'), how='inner')
        print("join:\n", result_join)

---

**Exercise 2.**
Create two DataFrames with overlapping column names. Demonstrate how `.join()` uses `lsuffix`/`rsuffix` while `pd.merge()` uses the `suffixes` parameter. Verify both approaches produce the same result.

??? success "Solution to Exercise 2"
    Compare suffix handling between join and merge.

        import pandas as pd

        df1 = pd.DataFrame({'val': [1, 2]}, index=['a', 'b'])
        df2 = pd.DataFrame({'val': [3, 4]}, index=['a', 'b'])

        result_join = df1.join(df2, lsuffix='_L', rsuffix='_R')
        result_merge = pd.merge(df1, df2, left_index=True, right_index=True, suffixes=('_L', '_R'))
        print("join:\n", result_join)
        print("merge:\n", result_merge)
        assert result_join.equals(result_merge)
        print("Results are identical.")

---

**Exercise 3.**
Create three DataFrames with a common index. Use `.join()` with a list to combine all three in one call. Then replicate the same result using sequential `pd.merge()` calls with `left_index=True` and `right_index=True`. Compare the outputs.

??? success "Solution to Exercise 3"
    Join three DataFrames using join list vs sequential merge.

        import pandas as pd

        df1 = pd.DataFrame({'A': [1, 2, 3]}, index=['x', 'y', 'z'])
        df2 = pd.DataFrame({'B': [4, 5, 6]}, index=['x', 'y', 'z'])
        df3 = pd.DataFrame({'C': [7, 8, 9]}, index=['x', 'y', 'z'])

        result_join = df1.join([df2, df3])
        result_merge = pd.merge(
            pd.merge(df1, df2, left_index=True, right_index=True),
            df3, left_index=True, right_index=True
        )
        print("join:\n", result_join)
        print("merge:\n", result_merge)
        assert result_join.equals(result_merge)
        print("Results are identical.")
