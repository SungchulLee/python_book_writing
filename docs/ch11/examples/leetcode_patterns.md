# LeetCode Patterns

Common pandas patterns from LeetCode SQL problems, demonstrating practical data manipulation techniques.

!!! tip "Mental Model"
    Most LeetCode pandas problems reduce to a small set of recurring patterns: group-and-count, self-merge for comparisons, rank within groups, and boolean masking for conditional filters. Learn to recognize which pattern a problem uses, and the solution becomes a templated one-liner or short chain.

## GroupBy Count Pattern

Count occurrences within groups.

### 1. Duplicate Emails (LeetCode 182)

```python
import pandas as pd

person = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'email': ['a@ex.com', 'b@ex.com', 'a@ex.com', 'b@ex.com', 'c@ex.com']
})

# Count emails and find duplicates
email_counts = person.groupby('email')['id'].count().reset_index(name='count')
duplicates = email_counts[email_counts['count'] > 1]['email']
```

### 2. Customer Orders (LeetCode 586)

```python
orders = pd.DataFrame({
    'order_number': [101, 102, 103, 104, 105],
    'customer_number': [1, 1, 2, 3, 2]
})

# Find customer with most orders
order_counts = orders.groupby('customer_number')['order_number'].count()
top_customer = order_counts.idxmax()
```

### 3. Classes with Students (LeetCode 596)

```python
courses = pd.DataFrame({
    'class': ['Math', 'Math', 'Math', 'Math', 'Math', 'Art', 'Art'],
    'student': ['A', 'B', 'C', 'D', 'E', 'F', 'G']
})

# Classes with at least 5 students
class_counts = courses.groupby('class')['student'].apply(len)
large_classes = class_counts[class_counts >= 5].index.tolist()
```

## Merge Pattern

Combine tables using merge.

### 1. Person and Address (LeetCode 175)

```python
person = pd.DataFrame({
    'personId': [1, 2, 3],
    'firstName': ['John', 'Jane', 'Jake'],
    'lastName': ['Doe', 'Smith', 'Brown']
})

address = pd.DataFrame({
    'personId': [1, 3],
    'city': ['New York', 'Los Angeles'],
    'state': ['NY', 'CA']
})

# Left join to keep all persons
result = person.merge(address, on='personId', how='left')
```

### 2. Employee Manager (LeetCode 181)

```python
employee = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['John', 'Doe', 'Jane', 'Smith'],
    'salary': [50000, 40000, 60000, 30000],
    'managerId': [None, 1, 1, 2]
})

# Self merge to compare with manager
merged = pd.merge(
    employee, employee,
    left_on='managerId', right_on='id',
    suffixes=('_emp', '_mgr')
)

# Find employees earning more than manager
higher = merged[merged['salary_emp'] > merged['salary_mgr']]
```

### 3. Project Employees (LeetCode 1075)

```python
project = pd.DataFrame({'project_id': [1, 2], 'name': ['P1', 'P2']})
employee = pd.DataFrame({
    'employee_id': [1, 2, 3],
    'project_id': [1, 1, 2],
    'experience': [5, 3, 7]
})

# Average experience per project
merged = pd.merge(project, employee, on='project_id')
avg_exp = merged.groupby('project_id')['experience'].mean()
```

## Transform Pattern

Apply group calculations back to rows.

### 1. First Activity (LeetCode 550)

```python
activity = pd.DataFrame({
    'player_id': [1, 1, 2, 2],
    'event_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04'])
})

# Get first activity date per player
activity['first'] = activity.groupby('player_id')['event_date'].transform('min')
```

### 2. Rank in Department (LeetCode 185)

```python
employee = pd.DataFrame({
    'departmentId': [1, 1, 1, 2, 2],
    'name': ['A', 'B', 'C', 'D', 'E'],
    'salary': [100, 90, 80, 95, 85]
})

# Dense rank within department
employee['rank'] = employee.groupby('departmentId')['salary'].rank(
    ascending=False, method='dense'
)

# Top 3 salaries per department
top_3 = employee[employee['rank'] <= 3]
```

### 3. Percent of Total

```python
sales = pd.DataFrame({
    'region': ['A', 'A', 'B', 'B'],
    'amount': [100, 200, 150, 250]
})

# Percent of region total
sales['pct'] = sales.groupby('region')['amount'].transform(
    lambda x: x / x.sum() * 100
)
```

## Apply Pattern

Custom logic per group.

### 1. Weighted Average (LeetCode 1251)

```python
def weighted_mean(df, value_col, weight_col):
    return (df[value_col] * df[weight_col]).sum() / df[weight_col].sum()

sold = pd.DataFrame({
    'product_id': [1, 1, 2],
    'price': [100, 120, 200],
    'units': [10, 5, 8]
})

avg_price = sold.groupby('product_id').apply(
    weighted_mean, 'price', 'units'
).rename('avg_price')
```

### 2. Quality Metrics (LeetCode 1211)

```python
queries = pd.DataFrame({
    'query_name': ['Q1', 'Q1', 'Q2'],
    'rating': [5, 4, 3],
    'position': [2, 1, 3]
})

queries['quality'] = queries['rating'] / queries['position']
result = queries.groupby('query_name')['quality'].mean().round(2)
```

### 3. Special Bonus (LeetCode 1873)

```python
employees = pd.DataFrame({
    'employee_id': [1, 2, 3],
    'name': ['Alice', 'Mike', 'Eve'],
    'salary': [50000, 60000, 70000]
})

# Bonus if odd ID and name doesn't start with M
employees['bonus'] = employees.apply(
    lambda row: row['salary'] if (row['employee_id'] % 2 != 0 and 
                                   not row['name'].startswith('M')) else 0,
    axis=1
)
```


---

## Exercises

**Exercise 1.** Write code that performs a self-join on a DataFrame to find all pairs where one employee earns more than another in the same department.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'salary': [70000, 80000, 60000, 90000],
        'department': ['IT', 'IT', 'HR', 'HR']
    })
    result = df.groupby('department')['salary'].max()
    print(result)
    ```

---

**Exercise 2.** Explain how to use `pd.merge()` to find rows in one DataFrame that have no matching entry in another (anti-join pattern).

??? success "Solution to Exercise 2"
    See the main content for the relevant patterns and API calls. The solution involves understanding how to combine Pandas operations to solve data manipulation problems.

---

**Exercise 3.** Write code that uses `groupby().transform()` to add a column showing each employee's salary as a percentage of their department's total salary.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({
        'value': np.random.randint(0, 100, 20),
        'group': np.random.choice(['A', 'B'], 20)
    })
    result = df.groupby('group')['value'].transform('sum')
    print(result)
    ```

---

**Exercise 4.** Create a DataFrame and use `nlargest()` to find the top 3 salaries in each department.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    s = pd.Series(np.random.randn(100))
    s_clean = s.clip(lower=0)
    print(s_clean.describe())
    ```
