# agg with Multiple Functions

The `agg()` method excels at applying multiple aggregation functions simultaneously, producing comprehensive summary statistics.

!!! tip "Mental Model"
    Passing a list of functions to `agg()` is like asking multiple analysts to summarize the same column -- each returns one number, and the results stack into a multi-row or multi-column table. A dict of `{column: [functions]}` extends this to different questions per column, all computed in one call.

## Multiple Functions per Column

Apply several functions to each column.

### 1. List of Functions

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50]
})

result = df.agg(['mean', 'std', 'min', 'max'])
print(result)
```

```
             A          B
mean  3.000000  30.000000
std   1.581139  15.811388
min   1.000000  10.000000
max   5.000000  50.000000
```

### 2. With Custom Functions

```python
def range_func(x):
    return x.max() - x.min()

result = df.agg(['mean', 'std', range_func])
print(result)
```

### 3. Lambda Functions

```python
result = df.agg([
    'mean',
    'std',
    lambda x: x.max() - x.min()
])
```

## LeetCode Example: Monthly Transactions

Aggregate multiple metrics by group.

### 1. Sample Data

```python
transactions = pd.DataFrame({
    'month': ['2023-01', '2023-01', '2023-02', '2023-02', '2023-03'],
    'country': ['USA', 'USA', 'UK', 'UK', 'Canada'],
    'id': [1, 2, 3, 4, 5],
    'state': [1, 0, 1, 1, 0],  # 1=approved, 0=declined
    'amount': [50, 20, 70, 30, 40],
    'approved_amount': [50, 0, 70, 30, 0]
})
```

### 2. Multi-metric Aggregation

```python
aggregated = transactions.groupby(
    ['month', 'country'],
    dropna=False
).agg({
    'id': 'count',
    'state': 'sum',
    'amount': 'sum',
    'approved_amount': 'sum'
}).reset_index()

print(aggregated)
```

### 3. Renaming Columns

```python
aggregated.columns = [
    'month', 'country', 'trans_count',
    'approved_count', 'total_amount', 'approved_total'
]
```

## LeetCode Example: Employee Reports

Count and average with named aggregations.

### 1. Sample Data

```python
employees = pd.DataFrame({
    'employee_id': [1, 2, 3, 4, 5],
    'reports_to': [0, 1, 1, 2, 2],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [45, 30, 28, 35, 40]
})
```

### 2. Named Aggregations

```python
result = employees.groupby('reports_to', as_index=False).agg(
    reports_count=('employee_id', 'size'),
    average_age=('age', 'mean')
)
print(result)
```

### 3. Result

```
   reports_to  reports_count  average_age
0           0              1         45.0
1           1              2         29.0
2           2              2         37.5
```

## Hierarchical Column Output

Multiple functions create MultiIndex columns.

### 1. MultiIndex Columns

```python
result = df.agg({
    'A': ['mean', 'std'],
    'B': ['min', 'max']
})
print(result)
print(result.columns)
```

### 2. Flatten Columns

```python
result.columns = ['_'.join(col) for col in result.columns]
```

### 3. Access Specific Results

```python
result['A']['mean']  # Access mean of column A
result[('A', 'mean')]  # Alternative syntax
```

## Combining with GroupBy

agg is most powerful with groupby.

### 1. Grouped Aggregation

```python
df = pd.DataFrame({
    'Group': ['A', 'A', 'B', 'B'],
    'Value': [1, 2, 3, 4],
    'Other': [10, 20, 30, 40]
})

df.groupby('Group').agg({
    'Value': ['sum', 'mean'],
    'Other': ['min', 'max']
})
```

### 2. Different Functions per Column

```python
df.groupby('Group').agg({
    'Value': 'sum',
    'Other': 'mean'
})
```

### 3. Named Aggregations

```python
df.groupby('Group').agg(
    value_total=('Value', 'sum'),
    value_avg=('Value', 'mean'),
    other_range=('Other', lambda x: x.max() - x.min())
)
```

## Best Practices

Guidelines for effective aggregation.

### 1. Use Named Aggregations

```python
# Clear and readable
df.groupby('Group').agg(
    total=('Value', 'sum'),
    average=('Value', 'mean')
)
```

### 2. Reset Index When Needed

```python
result = df.groupby('Group').agg('sum').reset_index()
```

### 3. Handle Missing Values

```python
df.groupby('Group', dropna=False).agg('mean')
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with columns `'department'`, `'salary'`, and `'bonus'`. Use `groupby('department').agg()` with named aggregations to compute `total_salary=('salary', 'sum')`, `avg_bonus=('bonus', 'mean')`, and `headcount=('salary', 'count')`.

??? success "Solution to Exercise 1"
    Use named aggregation syntax for readable column names.

        import pandas as pd

        df = pd.DataFrame({
            'department': ['HR', 'HR', 'IT', 'IT', 'Sales'],
            'salary': [50000, 55000, 70000, 65000, 60000],
            'bonus': [5000, 6000, 8000, 7500, 5500]
        })
        result = df.groupby('department').agg(
            total_salary=('salary', 'sum'),
            avg_bonus=('bonus', 'mean'),
            headcount=('salary', 'count')
        )
        print(result)

---

**Exercise 2.**
Apply multiple aggregation functions `['min', 'max', 'mean']` to two numeric columns simultaneously using `.agg()`. Then flatten the resulting MultiIndex columns into single-level column names using a list comprehension.

??? success "Solution to Exercise 2"
    Apply multiple functions and flatten the MultiIndex.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'group': ['A', 'A', 'B', 'B'],
            'x': [10, 20, 30, 40],
            'y': [1.5, 2.5, 3.5, 4.5]
        })
        result = df.groupby('group')[['x', 'y']].agg(['min', 'max', 'mean'])
        result.columns = ['_'.join(col) for col in result.columns]
        print(result)

---

**Exercise 3.**
Group a sales DataFrame by `'region'` and apply a lambda function inside `.agg()` that computes the coefficient of variation (std / mean) for the `'sales'` column. Name the result `'cv'`.

??? success "Solution to Exercise 3"
    Use a lambda for coefficient of variation inside `.agg()`.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'region': ['East', 'East', 'West', 'West', 'West'],
            'sales': [100, 150, 200, 180, 220]
        })
        result = df.groupby('region').agg(
            cv=('sales', lambda x: x.std() / x.mean())
        )
        print(result)
