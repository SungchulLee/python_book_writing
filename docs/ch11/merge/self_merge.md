# Self Merge

A self merge joins a DataFrame with itself, useful for comparing rows within the same table or representing hierarchical relationships.

!!! tip "Mental Model"
    A self merge treats the same table as both left and right, matching different columns against each other. The classic example is an employee table where `manager_id` references another row's `id`. By merging the table on `manager_id = id`, each employee row gains its manager's details -- a pattern that models any tree or graph stored in a flat table.

## Basic Concept

Merge a DataFrame with itself using different columns.

### 1. Employee-Manager Example

```python
import pandas as pd

employee = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['John', 'Doe', 'Jane', 'Smith'],
    'salary': [50000, 40000, 60000, 30000],
    'managerId': [None, 1, 1, 2]
})
print(employee)
```

```
   id   name  salary  managerId
0   1   John   50000        NaN
1   2    Doe   40000        1.0
2   3   Jane   60000        1.0
3   4  Smith   30000        2.0
```

### 2. Self Merge

```python
merged = pd.merge(
    left=employee,
    right=employee,
    left_on='managerId',
    right_on='id',
    how='inner',
    suffixes=('_employee', '_manager')
)
print(merged)
```

### 3. Result Interpretation

Each row pairs an employee with their manager.

## LeetCode Example: Higher Salary than Manager

Find employees earning more than their managers.

### 1. Self Merge

```python
merged = pd.merge(
    left=employee,
    right=employee,
    left_on='managerId',
    right_on='id',
    how='inner',
    suffixes=('_employee', '_manager')
)
```

### 2. Filter Condition

```python
higher_earners = merged[
    merged['salary_employee'] > merged['salary_manager']
]
```

### 3. Select Result

```python
result = higher_earners[['name_employee']].rename(
    columns={'name_employee': 'Employee'}
)
```

## Hierarchical Relationships

Self merge for parent-child relationships.

### 1. Category Hierarchy

```python
categories = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'name': ['Electronics', 'Phones', 'Laptops', 'iPhone', 'MacBook'],
    'parent_id': [None, 1, 1, 2, 3]
})
```

### 2. Join Parent Info

```python
with_parent = pd.merge(
    categories,
    categories[['id', 'name']],
    left_on='parent_id',
    right_on='id',
    how='left',
    suffixes=('', '_parent')
)
```

### 3. Result

```python
# Shows each category with its parent category name
```

## Comparing Consecutive Rows

Self merge to compare rows.

### 1. Stock Data

```python
stock = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=5),
    'price': [100, 102, 101, 105, 103]
})
stock['row_num'] = range(len(stock))
```

### 2. Join Consecutive Rows

```python
stock_comparison = pd.merge(
    stock,
    stock,
    left_on='row_num',
    right_on=stock['row_num'] + 1,
    suffixes=('_today', '_yesterday')
)
```

### 3. Calculate Change

```python
stock_comparison['change'] = (
    stock_comparison['price_today'] - stock_comparison['price_yesterday']
)
```

## Join Types in Self Merge

Choose appropriate join type.

### 1. Inner Join

```python
# Only rows with valid relationship
pd.merge(df, df, left_on='parent_id', right_on='id', how='inner')
# Excludes rows without parent (root nodes)
```

### 2. Left Join

```python
# Keep all original rows
pd.merge(df, df, left_on='parent_id', right_on='id', how='left')
# Root nodes have NaN for parent info
```

### 3. Use Case Selection

```python
# Inner: When relationship is required
# Left: When preserving all original rows matters
```

## Performance Considerations

Self merge creates more rows.

### 1. Cartesian Product Warning

```python
# Without proper keys, self merge creates N×N rows
# Always specify join columns carefully
```

### 2. Large DataFrames

```python
# Self merge can be memory-intensive
# Consider filtering before merge
```

### 3. Alternative Approaches

```python
# For simple comparisons, consider:
df['prev_value'] = df['value'].shift(1)
```

---

## Exercises

**Exercise 1.**
Create an `employees` DataFrame with `'id'`, `'name'`, and `'manager_id'` columns. Perform a self merge to add each employee's manager name as a new column.

??? success "Solution to Exercise 1"
    Self merge to find each employee's manager name.

        import pandas as pd

        employees = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Alice', 'Bob', 'Carol', 'Dave'],
            'manager_id': [None, 1, 1, 2]
        })
        result = pd.merge(
            employees, employees[['id', 'name']],
            left_on='manager_id', right_on='id',
            suffixes=('', '_manager'), how='left'
        )
        print(result[['name', 'name_manager']])

---

**Exercise 2.**
Create a `flights` DataFrame with `'origin'` and `'destination'` airport codes. Perform a self merge to find all pairs of flights that can be connected (where the destination of one flight matches the origin of another).

??? success "Solution to Exercise 2"
    Find connecting flights via self merge.

        import pandas as pd

        flights = pd.DataFrame({
            'flight': ['F1', 'F2', 'F3'],
            'origin': ['NYC', 'CHI', 'LAX'],
            'destination': ['CHI', 'LAX', 'NYC']
        })
        connections = pd.merge(
            flights, flights,
            left_on='destination', right_on='origin',
            suffixes=('_first', '_second')
        )
        print(connections[['flight_first', 'origin_first', 'destination_first', 'flight_second', 'destination_second']])

---

**Exercise 3.**
Create a table of parent-child relationships. Use a self merge to find all grandparent-grandchild pairs (merge twice: child to parent, then parent to grandparent).

??? success "Solution to Exercise 3"
    Find grandparent-grandchild pairs with two self merges.

        import pandas as pd

        family = pd.DataFrame({
            'person': ['Alice', 'Bob', 'Carol', 'Dave'],
            'parent': ['Bob', 'Carol', None, 'Carol']
        })
        # First merge: person -> parent
        step1 = pd.merge(family, family[['person', 'parent']], left_on='parent', right_on='person', suffixes=('', '_gp'))
        # parent_gp is the grandparent
        grandparents = step1[step1['parent_gp'].notna()][['person', 'parent_gp']]
        grandparents.columns = ['grandchild', 'grandparent']
        print(grandparents)
