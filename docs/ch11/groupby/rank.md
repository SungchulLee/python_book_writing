# rank Method

The `rank()` method assigns ranks to values within each group, useful for identifying top performers or creating rankings.

!!! tip "Mental Model"
    `rank()` inside a groupby is SQL's `RANK() OVER (PARTITION BY ...)`. Each group gets its own independent ranking -- the top value in group A is rank 1 regardless of values in group B. The result has the same shape as the original DataFrame, with rank numbers replacing the original values.

## Basic Ranking

Rank values within groups.

### 1. Simple Rank

```python
import pandas as pd

df = pd.DataFrame({
    'dept': ['A', 'A', 'A', 'B', 'B', 'B'],
    'employee': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank'],
    'salary': [5000, 6000, 4000, 4500, 5500, 4500]
})

df['rank'] = df.groupby('dept')['salary'].rank(ascending=False)
print(df)
```

```
  dept employee  salary  rank
0    A    Alice    5000   2.0
1    A      Bob    6000   1.0
2    A    Carol    4000   3.0
3    B     Dave    4500   2.5
4    B      Eve    5500   1.0
5    B    Frank    4500   2.5
```

### 2. ascending Parameter

```python
# ascending=False: highest value gets rank 1
# ascending=True: lowest value gets rank 1
```

### 3. Tie Handling

Default: tied values get average rank (2.5 for Dave and Frank).

## LeetCode Example: Department Top Salaries

Find top 3 salaries per department.

### 1. Sample Data

```python
employee = pd.DataFrame({
    'departmentId': [1, 1, 1, 2, 2, 2],
    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank'],
    'salary': [5000, 6000, 4000, 4500, 5500, 4500]
})
```

### 2. Dense Ranking

```python
employee['rank'] = employee.groupby('departmentId')['salary'].rank(
    ascending=False,
    method='dense'
)
print(employee)
```

### 3. Filter Top 3

```python
top_3 = employee[employee['rank'] <= 3]
```

## method Parameter

Control how ties are handled.

### 1. method='average' (Default)

```python
# Ties get average of ranks they would occupy
# [100, 100, 80] → [1.5, 1.5, 3.0]
```

### 2. method='min'

```python
# Ties get lowest rank
# [100, 100, 80] → [1, 1, 3]
```

### 3. method='dense'

```python
# Ties get same rank, next rank is consecutive
# [100, 100, 80] → [1, 1, 2]
```

## Ranking Examples

Common ranking patterns.

### 1. Percentile Rank

```python
df['percentile'] = df.groupby('dept')['salary'].rank(pct=True)
```

### 2. Row Number

```python
df['row_num'] = df.groupby('dept').cumcount() + 1
```

### 3. First/Last in Group

```python
df['is_top'] = df.groupby('dept')['salary'].rank(ascending=False) == 1
```

## Comparison with SQL

Equivalent SQL window functions.

### 1. RANK()

```python
df.groupby('dept')['salary'].rank(method='min', ascending=False)
```

### 2. DENSE_RANK()

```python
df.groupby('dept')['salary'].rank(method='dense', ascending=False)
```

### 3. ROW_NUMBER()

```python
df.groupby('dept').cumcount() + 1
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with `'department'` and `'salary'` columns. Use `groupby('department')['salary'].rank(method='dense', ascending=False)` to assign dense rankings within each department. Show the top earner per department.

??? success "Solution to Exercise 1"
    Dense ranking within groups to find top earners.

        import pandas as pd

        df = pd.DataFrame({
            'department': ['IT', 'IT', 'IT', 'HR', 'HR'],
            'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],
            'salary': [70000, 65000, 72000, 50000, 55000]
        })
        df['rank'] = df.groupby('department')['salary'].rank(
            method='dense', ascending=False
        )
        top = df[df['rank'] == 1]
        print(top)

---

**Exercise 2.**
Compare three ranking methods (`'average'`, `'min'`, `'dense'`) on the same data that contains ties. Create a DataFrame showing the original values alongside all three ranking columns.

??? success "Solution to Exercise 2"
    Compare average, min, and dense ranking on tied data.

        import pandas as pd

        df = pd.DataFrame({
            'value': [100, 200, 200, 300, 300, 300]
        })
        df['rank_avg'] = df['value'].rank(method='average')
        df['rank_min'] = df['value'].rank(method='min')
        df['rank_dense'] = df['value'].rank(method='dense')
        print(df)

---

**Exercise 3.**
Use `.rank(pct=True)` to compute percentile ranks within groups. Given student scores grouped by class, compute the percentile rank and identify students in the top 25% of their class.

??? success "Solution to Exercise 3"
    Use percentile ranking to find top performers.

        import pandas as pd

        df = pd.DataFrame({
            'class': ['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'],
            'student': ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8'],
            'score': [85, 92, 78, 95, 88, 76, 91, 84]
        })
        df['pct_rank'] = df.groupby('class')['score'].rank(pct=True)
        top_25 = df[df['pct_rank'] >= 0.75]
        print("Top 25% per class:")
        print(top_25)
