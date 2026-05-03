# Multi-Index Joins

Real-world datasets often have composite keys — for example, (date, ticker) for financial data or (year, quarter, region) for sales data. Pandas represents composite keys as a MultiIndex, and joining DataFrames on these multi-level indices requires understanding how index levels are matched. This page covers the mechanics of joining and merging when one or both DataFrames have a MultiIndex.

!!! tip "Mental Model"
    A MultiIndex join matches on all shared index levels simultaneously -- like a SQL join on a composite primary key. If one DataFrame has levels `(date, ticker)` and the other has only `(ticker)`, pandas matches on the shared level and broadcasts across the unshared one. Keeping level names consistent across DataFrames is the key to making these joins work seamlessly.

```python
import pandas as pd
import numpy as np
```

---

## Joining on a Shared MultiIndex

When both DataFrames have the same MultiIndex structure, `DataFrame.join` matches on all levels automatically.

```python
index = pd.MultiIndex.from_tuples(
    [("2023", "Q1"), ("2023", "Q2"), ("2024", "Q1")],
    names=["year", "quarter"]
)

revenue = pd.DataFrame({"revenue": [100, 200, 150]}, index=index)
costs = pd.DataFrame({"cost": [80, 160, 120]}, index=index)

result = revenue.join(costs)
print(result)
```

```
               revenue  cost
year quarter
2023 Q1            100    80
     Q2            200   160
2024 Q1            150   120
```

Both DataFrames share the same (year, quarter) MultiIndex, so the join matches all levels.

---

## Joining MultiIndex with Single Index

When the left DataFrame has a MultiIndex and the right has a single index that matches **one level** of the MultiIndex, pandas does not automatically align them. You need to specify which level to join on.

### Using merge with Left Level

```python
sales = pd.DataFrame(
    {"revenue": [100, 200, 150, 250]},
    index=pd.MultiIndex.from_tuples(
        [("East", "Q1"), ("East", "Q2"), ("West", "Q1"), ("West", "Q2")],
        names=["region", "quarter"]
    )
)

targets = pd.DataFrame(
    {"target": [180, 300]},
    index=pd.Index(["East", "West"], name="region")
)

# Merge on the "region" level of sales' MultiIndex
result = pd.merge(
    sales, targets,
    left_on="region", right_index=True
)
print(result)
```

```
                revenue  target
region quarter
East   Q1           100     180
       Q2           200     180
West   Q1           150     300
       Q2           250     300
```

### Using join with on Parameter

Alternatively, reset the relevant level to a column and use `on`.

```python
sales_reset = sales.reset_index(level="region")

result = sales_reset.join(targets, on="region")
print(result)
```

```
        region  revenue  target
quarter
Q1        East      100     180
Q2        East      200     180
Q1        West      150     300
Q2        West      300     300
```

---

## Merging on MultiIndex Levels

`pd.merge` supports joining on specific index levels using `left_on` and `right_on` with level names.

```python
df1 = pd.DataFrame(
    {"val1": [1, 2, 3, 4]},
    index=pd.MultiIndex.from_tuples(
        [("A", 1), ("A", 2), ("B", 1), ("B", 2)],
        names=["group", "id"]
    )
)

df2 = pd.DataFrame(
    {"val2": [10, 20]},
    index=pd.Index(["A", "B"], name="group")
)

# Join on the "group" level
result = pd.merge(df1, df2, left_on="group", right_index=True)
print(result)
```

```
          val1  val2
group id
A     1      1    10
      2      2    10
B     1      3    20
      2      4    20
```

---

## Both Sides with MultiIndex

When both DataFrames have a MultiIndex, `pd.merge` can join on specific levels from each side.

```python
left = pd.DataFrame(
    {"value": [10, 20, 30]},
    index=pd.MultiIndex.from_tuples(
        [("A", "x"), ("A", "y"), ("B", "x")],
        names=["key1", "key2"]
    )
)

right = pd.DataFrame(
    {"label": ["alpha", "beta"]},
    index=pd.MultiIndex.from_tuples(
        [("A", 100), ("B", 200)],
        names=["key1", "code"]
    )
)

# Join on the shared "key1" level
result = pd.merge(left, right, left_on="key1", right_on="key1")
print(result)
```

```
               value  label
key1 key2 code
A    x    100     10  alpha
     y    100     20  alpha
B    x    200     30   beta
```

---

## Joining Columns to a MultiIndex

A common pattern is joining a flat DataFrame (with regular columns) to a DataFrame with a MultiIndex, where the flat columns correspond to index levels.

```python
data = pd.DataFrame({
    "year": [2023, 2023, 2024],
    "quarter": ["Q1", "Q2", "Q1"],
    "revenue": [100, 200, 150]
})

targets = pd.DataFrame(
    {"target": [120, 180, 160]},
    index=pd.MultiIndex.from_tuples(
        [(2023, "Q1"), (2023, "Q2"), (2024, "Q1")],
        names=["year", "quarter"]
    )
)

# Merge flat columns against MultiIndex
result = pd.merge(
    data, targets,
    left_on=["year", "quarter"],
    right_index=True
)
print(result)
```

```
   year quarter  revenue  target
0  2023      Q1      100     120
1  2023      Q2      200     180
2  2024      Q1      150     160
```

---

## Common Pitfalls

!!! warning "Level Name Mismatch"
    When using `left_on` or `right_on` with index level names, the level names must match exactly. A typo or case mismatch produces a `KeyError`.

!!! warning "Duplicate Level Values"
    If the MultiIndex has duplicate values at the matched level, the join produces a Cartesian product for those duplicates, potentially creating more rows than expected. Check with `df.index.get_level_values(level).is_unique`.

---

## Summary

| Scenario | Recommended Approach |
|----------|---------------------|
| Both share same MultiIndex | `df1.join(df2)` |
| MultiIndex left, single index right | `pd.merge(left, right, left_on=level_name, right_index=True)` |
| Both have MultiIndex, shared level | `pd.merge(left, right, left_on=level, right_on=level)` |
| Flat columns to MultiIndex | `pd.merge(flat, multi, left_on=[cols], right_index=True)` |

**Key Takeaways**:

- When both DataFrames share the same MultiIndex, `join` matches all levels automatically
- Use `left_on` with index level names and `right_index=True` to match a single level against another DataFrame's index
- Flat column values can be matched against MultiIndex levels using `left_on=[col1, col2]` with `right_index=True`
- Watch for Cartesian products when joining on non-unique index levels
- Level names must match exactly — check with `df.index.names` before joining

---

## Exercises

**Exercise 1.**
Create two DataFrames that share the same `(year, quarter)` MultiIndex. Use `.join()` to combine them. Verify the result has the same MultiIndex and no `NaN` values.

??? success "Solution to Exercise 1"
    Join two DataFrames on a shared MultiIndex.

        import pandas as pd

        idx = pd.MultiIndex.from_tuples(
            [(2023, 'Q1'), (2023, 'Q2'), (2024, 'Q1')],
            names=['year', 'quarter']
        )
        revenue = pd.DataFrame({'revenue': [100, 200, 150]}, index=idx)
        costs = pd.DataFrame({'cost': [80, 160, 120]}, index=idx)
        result = revenue.join(costs)
        print(result)
        assert result.isna().sum().sum() == 0
        print("No NaN values.")

---

**Exercise 2.**
Create a DataFrame with a `(region, quarter)` MultiIndex and a second DataFrame with a single `'region'` index. Use `pd.merge()` with `left_on='region'` and `right_index=True` to join them. Verify that each region's target is broadcast to all its quarters.

??? success "Solution to Exercise 2"
    Merge MultiIndex with single index on one level.

        import pandas as pd

        sales = pd.DataFrame(
            {'revenue': [100, 200, 150, 250]},
            index=pd.MultiIndex.from_tuples(
                [('East', 'Q1'), ('East', 'Q2'), ('West', 'Q1'), ('West', 'Q2')],
                names=['region', 'quarter']
            )
        )
        targets = pd.DataFrame(
            {'target': [180, 300]},
            index=pd.Index(['East', 'West'], name='region')
        )
        result = pd.merge(sales, targets, left_on='region', right_index=True)
        print(result)
        # Each region's target is broadcast to all its quarters

---

**Exercise 3.**
Create a flat DataFrame with `'dept'` and `'team'` columns and a targets DataFrame with a `(dept, team)` MultiIndex. Use `pd.merge()` with `left_on=['dept', 'team']` and `right_index=True` to look up targets for each row.

??? success "Solution to Exercise 3"
    Merge flat columns against a MultiIndex.

        import pandas as pd

        data = pd.DataFrame({
            'dept': ['Eng', 'Eng', 'Sales'],
            'team': ['Backend', 'Frontend', 'East'],
            'headcount': [10, 8, 15]
        })
        targets = pd.DataFrame(
            {'target': [12, 10, 18]},
            index=pd.MultiIndex.from_tuples(
                [('Eng', 'Backend'), ('Eng', 'Frontend'), ('Sales', 'East')],
                names=['dept', 'team']
            )
        )
        result = pd.merge(data, targets, left_on=['dept', 'team'], right_index=True)
        print(result)
