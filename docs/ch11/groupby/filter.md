# filter Method

The `filter()` method removes groups that do not satisfy a condition, keeping or excluding entire groups.

!!! tip "Mental Model"
    `filter()` is a group-level WHERE clause: it tests a condition on each group as a whole and keeps or drops the entire group. Unlike boolean indexing which tests row by row, `filter` asks "does this group meet the criterion?" and returns all rows of qualifying groups unchanged.

## Basic Usage

Filter groups based on a condition.

### 1. Filter by Group Size

```python
import pandas as pd

df = pd.DataFrame({
    'group': ['A', 'A', 'A', 'B', 'B', 'C'],
    'value': [1, 2, 3, 4, 5, 6]
})

# Keep only groups with more than 2 members
result = df.groupby('group').filter(lambda x: len(x) > 2)
print(result)
```

```
  group  value
0     A      1
1     A      2
2     A      3
```

### 2. Filter Function

The function receives each group DataFrame and returns True/False.

### 3. All or Nothing

If condition is True, entire group is kept; otherwise, entire group is removed.

## Common Filtering Patterns

Typical filter conditions.

### 1. Minimum Group Size

```python
df.groupby('group').filter(lambda x: len(x) >= 5)
```

### 2. Value Threshold

```python
# Keep groups where mean exceeds threshold
df.groupby('group').filter(lambda x: x['value'].mean() > 10)
```

### 3. All Values Meet Condition

```python
# Keep groups where all values are positive
df.groupby('group').filter(lambda x: (x['value'] > 0).all())
```

## LeetCode Example: Classes with Students

Find classes with at least 5 students.

### 1. Sample Data

```python
courses = pd.DataFrame({
    'class': ['Math', 'Math', 'Math', 'Math', 'Math',
              'Art', 'Art', 'Music', 'Music', 'Music'],
    'student': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
})
```

### 2. Filter Large Classes

```python
large_classes = courses.groupby('class').filter(lambda x: len(x) >= 5)
print(large_classes)
```

### 3. Get Class Names

```python
# Get unique class names
classes = large_classes['class'].unique()
```

## Filter vs Boolean Indexing

Compare approaches.

### 1. Boolean Indexing

```python
# Filter individual rows
df[df['value'] > 5]
```

### 2. GroupBy Filter

```python
# Filter entire groups
df.groupby('group').filter(lambda x: x['value'].mean() > 5)
```

### 3. Key Difference

Boolean indexing filters rows; filter removes groups.

## dropna Parameter

Handle groups with missing values.

### 1. Default Behavior

```python
# dropna=True (default): ignore groups with NA
```

### 2. Include NA Groups

```python
df.groupby('group', dropna=False).filter(lambda x: len(x) > 1)
```

### 3. Filter NA Groups

```python
df.groupby('group').filter(lambda x: x['value'].notna().all())
```

## Performance Considerations

Optimize filter operations.

### 1. Simple Conditions First

```python
# Pre-filter when possible
valid_groups = df.groupby('group').size() >= 5
valid_group_names = valid_groups[valid_groups].index
df[df['group'].isin(valid_group_names)]
```

### 2. Avoid Lambda When Possible

```python
# Faster alternative for size filter
group_sizes = df.groupby('group').size()
valid = group_sizes[group_sizes >= 5].index
df[df['group'].isin(valid)]
```

### 3. Use Built-in Methods

Built-in aggregations are faster than custom lambdas.

---

## Exercises

**Exercise 1.**
Group a DataFrame by `'city'` and use `.filter()` to keep only cities that have more than 3 records in the dataset.

??? success "Solution to Exercise 1"
    Filter groups by size using `len(x)`.

        import pandas as pd

        df = pd.DataFrame({
            'city': ['NY', 'NY', 'NY', 'NY', 'LA', 'LA', 'SF'],
            'value': [10, 20, 30, 40, 50, 60, 70]
        })
        result = df.groupby('city').filter(lambda x: len(x) > 3)
        print(result)

---

**Exercise 2.**
Use `.filter()` to keep groups where the mean of the `'score'` column exceeds 80. Print the entire filtered DataFrame (not just the group summaries).

??? success "Solution to Exercise 2"
    Filter groups by mean score threshold.

        import pandas as pd

        df = pd.DataFrame({
            'class': ['A', 'A', 'B', 'B', 'C', 'C'],
            'score': [85, 90, 70, 75, 95, 88]
        })
        result = df.groupby('class').filter(lambda x: x['score'].mean() > 80)
        print(result)

---

**Exercise 3.**
Compare the performance of using `.filter(lambda x: len(x) >= 5)` versus the manual approach of computing group sizes, finding valid groups, and using `.isin()`. Time both approaches on a larger DataFrame.

??? success "Solution to Exercise 3"
    Compare filter with manual isin approach.

        import pandas as pd
        import numpy as np
        import time

        np.random.seed(42)
        df = pd.DataFrame({
            'group': np.random.choice(list('ABCDEFGHIJ'), 10000),
            'value': np.random.randn(10000)
        })

        start = time.time()
        r1 = df.groupby('group').filter(lambda x: len(x) >= 900)
        t1 = time.time() - start

        start = time.time()
        sizes = df.groupby('group').size()
        valid = sizes[sizes >= 900].index
        r2 = df[df['group'].isin(valid)]
        t2 = time.time() - start

        print(f"filter(): {t1:.4f}s, isin(): {t2:.4f}s")
