# transform Method

The `transform()` method applies a function to each group and returns a result with the same shape as the original DataFrame.

!!! tip "Mental Model"
    `transform` is the shape-preserving counterpart to `agg`. While `agg` collapses each group to one row, `transform` broadcasts the group result back to every row of that group. This is how you create columns like "each value minus its group mean" -- the group statistic is repeated to match the original row count.

## Basic Concept

Transform preserves the original index.

### 1. Difference from agg

```python
import pandas as pd

df = pd.DataFrame({
    'group': ['A', 'A', 'B', 'B'],
    'value': [1, 2, 3, 4]
})

# agg: returns one value per group
df.groupby('group')['value'].mean()
# group
# A    1.5
# B    3.5

# transform: returns same-length Series
df.groupby('group')['value'].transform('mean')
# 0    1.5
# 1    1.5
# 2    3.5
# 3    3.5
```

### 2. Same Shape Output

Transform output aligns with original DataFrame.

### 3. Broadcast Group Values

Each row gets its group's aggregated value.

## LeetCode Example: First Activity Date

Find each player's first login date.

### 1. Sample Data

```python
activity = pd.DataFrame({
    'player_id': [1, 1, 2, 2],
    'event_date': pd.to_datetime([
        '2024-01-01', '2024-01-02',
        '2024-01-03', '2024-01-04'
    ])
})
```

### 2. Transform with min

```python
activity["first"] = activity.groupby("player_id")["event_date"].transform('min')
print(activity)
```

```
   player_id event_date      first
0          1 2024-01-01 2024-01-01
1          1 2024-01-02 2024-01-01
2          2 2024-01-03 2024-01-03
3          2 2024-01-04 2024-01-03
```

### 3. Each Row Gets Group Min

Every row for player 1 shows their first date.

## Common Use Cases

Typical transform applications.

### 1. Group Normalization

```python
df['normalized'] = df.groupby('group')['value'].transform(
    lambda x: (x - x.mean()) / x.std()
)
```

### 2. Percent of Group Total

```python
df['pct_of_group'] = df.groupby('group')['value'].transform(
    lambda x: x / x.sum()
)
```

### 3. Rank Within Group

```python
df['group_rank'] = df.groupby('group')['value'].transform('rank')
```

## transform vs apply

Key differences between methods.

### 1. Output Shape

```python
# transform: must return same shape
# apply: can return any shape
```

### 2. Function Requirements

```python
# transform: function must return same-length Series
# apply: more flexible
```

### 3. Performance

```python
# transform: often faster for built-in functions
# apply: more flexible but potentially slower
```

## Multiple Columns

Transform multiple columns at once.

### 1. Same Function

```python
df[['value1', 'value2']] = df.groupby('group')[['value1', 'value2']].transform('mean')
```

### 2. Different Functions

```python
# Use apply for different functions per column
```

### 3. Preserving Original

```python
# Create new columns instead of overwriting
df['value_mean'] = df.groupby('group')['value'].transform('mean')
```

---

## Exercises

**Exercise 1.**
Given a DataFrame with `'department'` and `'salary'` columns, use `groupby().transform('mean')` to add a new column `'dept_avg_salary'` that shows each department's average salary on every row.

??? success "Solution to Exercise 1"
    Use `transform('mean')` to broadcast the group mean to every row.

        import pandas as pd

        df = pd.DataFrame({
            'department': ['IT', 'IT', 'HR', 'HR', 'IT'],
            'salary': [70000, 65000, 50000, 55000, 72000]
        })
        df['dept_avg_salary'] = df.groupby('department')['salary'].transform('mean')
        print(df)

---

**Exercise 2.**
Use `transform` to normalize values within each group: for each group, compute `(x - mean) / std`. Add the result as a `'normalized'` column.

??? success "Solution to Exercise 2"
    Apply a lambda that computes z-scores within each group.

        import pandas as pd

        df = pd.DataFrame({
            'group': ['A', 'A', 'A', 'B', 'B', 'B'],
            'value': [10, 20, 30, 100, 200, 300]
        })
        df['normalized'] = df.groupby('group')['value'].transform(
            lambda x: (x - x.mean()) / x.std()
        )
        print(df)

---

**Exercise 3.**
Use `transform('sum')` to compute each row's value as a percentage of its group total. Add a column `'pct_of_group'` that shows what fraction each row contributes to its group's total.

??? success "Solution to Exercise 3"
    Divide each value by the group sum using transform.

        import pandas as pd

        df = pd.DataFrame({
            'region': ['East', 'East', 'West', 'West'],
            'sales': [100, 300, 200, 200]
        })
        df['pct_of_group'] = df['sales'] / df.groupby('region')['sales'].transform('sum')
        print(df)
