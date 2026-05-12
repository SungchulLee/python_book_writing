# LeetCode DataFrame Problems

This document covers common LeetCode patterns involving pandas DataFrame operations including groupby, merge, pivot, and multi-table manipulations.

!!! tip "Mental Model"
    LeetCode DataFrame problems are SQL queries in disguise. Each problem maps to a chain of pandas verbs: `groupby` for GROUP BY, `merge` for JOIN, `query` for WHERE. Recognizing the SQL pattern first, then translating to pandas, is the fastest path to a solution.

## Pattern 1: GroupBy and Aggregation

### LeetCode 586: Customer Placing the Largest Number of Orders

**Problem**: Find the customer who placed the most orders.

```python
def largest_orders(orders: pd.DataFrame) -> pd.DataFrame:
    # Group by customer and count orders
    order_counts = orders.groupby('customer_number')['order_number'].count()
    
    # Find customer with max orders
    max_customer = order_counts.idxmax()
    
    return pd.DataFrame({'customer_number': [max_customer]})
```

**With reset_index**:

```python
def largest_orders(orders: pd.DataFrame) -> pd.DataFrame:
    counts = orders.groupby('customer_number')['order_number'].count().reset_index()
    counts.columns = ['customer_number', 'order_count']
    
    max_count = counts['order_count'].max()
    return counts[counts['order_count'] == max_count][['customer_number']]
```

### LeetCode 182: Duplicate Emails

**Problem**: Find emails that appear more than once.

```python
def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    # Group by email and count
    email_counts = person.groupby('email')['id'].count().reset_index(name='count')
    
    # Filter duplicates
    duplicates = email_counts[email_counts['count'] > 1]
    
    return duplicates[['email']].rename(columns={'email': 'Email'})
```

## Pattern 2: Merge Operations

### LeetCode 175: Combine Two Tables

**Problem**: Left join person and address tables.

```python
def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    result = person.merge(
        address,
        on='personId',
        how='left'
    )
    return result[['firstName', 'lastName', 'city', 'state']]
```

### LeetCode 577: Employee Bonus

**Problem**: Find employees with bonus < 1000 or no bonus.

```python
def employee_bonus(employee: pd.DataFrame, bonus: pd.DataFrame) -> pd.DataFrame:
    # Left merge to include employees without bonus
    merged = employee.merge(bonus, on='empId', how='left')
    
    # Filter: bonus < 1000 OR bonus is null
    result = merged[(merged['bonus'] < 1000) | (merged['bonus'].isnull())]
    
    return result[['name', 'bonus']]
```

**Key Concepts**:

- Left join preserves all employees
- `isnull()` catches employees without bonus records

### LeetCode 181: Employees Earning More Than Their Managers

**Problem**: Self-join to compare employee and manager salaries.

```python
def employees_earning_more(employee: pd.DataFrame) -> pd.DataFrame:
    # Self merge: join employee with their manager
    merged = employee.merge(
        employee,
        left_on='managerId',
        right_on='id',
        suffixes=('_emp', '_mgr')
    )
    
    # Filter where employee earns more
    result = merged[merged['salary_emp'] > merged['salary_mgr']]
    
    return result[['name_emp']].rename(columns={'name_emp': 'Employee'})
```

## Pattern 3: Pivot and Reshape

### LeetCode 1179: Reformat Department Table

**Problem**: Pivot monthly revenue by department.

```python
def reformat_table(department: pd.DataFrame) -> pd.DataFrame:
    # Pivot: rows=id, columns=month, values=revenue
    pivoted = department.pivot(
        index='id',
        columns='month',
        values='revenue'
    ).reset_index()
    
    # Ensure all months present
    all_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Add revenue suffix to column names
    pivoted.columns = ['id'] + [f'{m}_Revenue' for m in all_months 
                                if m in pivoted.columns]
    
    # Reindex to include missing months
    for month in all_months:
        col = f'{month}_Revenue'
        if col not in pivoted.columns:
            pivoted[col] = None
    
    return pivoted
```

### LeetCode 626: Exchange Seats

**Problem**: Swap adjacent seat IDs.

```python
def exchange_seats(seat: pd.DataFrame) -> pd.DataFrame:
    n = len(seat)
    
    # Create new id column
    seat['new_id'] = seat['id'].apply(
        lambda x: x + 1 if x % 2 == 1 and x < n 
                  else x - 1 if x % 2 == 0 
                  else x
    )
    
    # Sort by new_id and reset
    result = seat.sort_values('new_id').reset_index(drop=True)
    result['id'] = result['new_id']
    
    return result[['id', 'student']]
```

## Pattern 4: Ranking and Window Functions

### LeetCode 176: Second Highest Salary

**Problem**: Find the second highest distinct salary.

```python
def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    # Get unique salaries sorted descending
    unique_salaries = employee['salary'].drop_duplicates().sort_values(ascending=False)
    
    # Get second highest or None
    if len(unique_salaries) >= 2:
        second = unique_salaries.iloc[1]
    else:
        second = None
    
    return pd.DataFrame({'SecondHighestSalary': [second]})
```

### LeetCode 178: Rank Scores

**Problem**: Rank scores with dense ranking.

```python
def rank_scores(scores: pd.DataFrame) -> pd.DataFrame:
    # Dense rank: no gaps in ranking
    scores['rank'] = scores['score'].rank(method='dense', ascending=False)
    
    return scores[['score', 'rank']].sort_values('score', ascending=False)
```

### LeetCode 184: Department Highest Salary

**Problem**: Find highest paid employee(s) per department.

```python
def department_highest_salary(
    employee: pd.DataFrame, 
    department: pd.DataFrame
) -> pd.DataFrame:
    # Merge to get department names
    merged = employee.merge(department, left_on='departmentId', right_on='id')
    
    # Find max salary per department
    max_salaries = merged.groupby('departmentId')['salary'].transform('max')
    
    # Filter employees with max salary
    result = merged[merged['salary'] == max_salaries]
    
    return result[['name_y', 'name_x', 'salary']].rename(
        columns={'name_y': 'Department', 'name_x': 'Employee', 'salary': 'Salary'}
    )
```

## Pattern 5: Date Operations

### LeetCode 197: Rising Temperature

**Problem**: Find dates where temperature was higher than previous day.

```python
def rising_temperature(weather: pd.DataFrame) -> pd.DataFrame:
    # Sort by date
    weather = weather.sort_values('recordDate')
    
    # Self merge on consecutive dates
    weather['prev_date'] = weather['recordDate'] - pd.Timedelta(days=1)
    
    merged = weather.merge(
        weather,
        left_on='prev_date',
        right_on='recordDate',
        suffixes=('', '_prev')
    )
    
    # Filter where temperature increased
    rising = merged[merged['temperature'] > merged['temperature_prev']]
    
    return rising[['id']]
```

**Alternative with shift**:

```python
def rising_temperature(weather: pd.DataFrame) -> pd.DataFrame:
    weather = weather.sort_values('recordDate')
    
    # Check for consecutive dates
    weather['prev_temp'] = weather['temperature'].shift(1)
    weather['prev_date'] = weather['recordDate'].shift(1)
    weather['is_consecutive'] = (
        weather['recordDate'] - weather['prev_date']
    ) == pd.Timedelta(days=1)
    
    # Filter rising and consecutive
    result = weather[
        (weather['temperature'] > weather['prev_temp']) & 
        weather['is_consecutive']
    ]
    
    return result[['id']]
```

## Pattern 6: Multiple Aggregations

### LeetCode 1193: Monthly Transactions I

**Problem**: Aggregate transaction counts and amounts by month and country.

```python
def monthly_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    # Extract month
    transactions['month'] = transactions['trans_date'].dt.strftime('%Y-%m')
    
    # Aggregate
    result = transactions.groupby(['month', 'country']).agg(
        trans_count=('id', 'count'),
        approved_count=('state', lambda x: (x == 'approved').sum()),
        trans_total_amount=('amount', 'sum'),
        approved_total_amount=('amount', lambda x: x[transactions.loc[x.index, 'state'] == 'approved'].sum())
    ).reset_index()
    
    return result
```

**Alternative approach**:

```python
def monthly_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    transactions['month'] = transactions['trans_date'].dt.strftime('%Y-%m')
    transactions['is_approved'] = transactions['state'] == 'approved'
    transactions['approved_amount'] = transactions['amount'] * transactions['is_approved']
    
    result = transactions.groupby(['month', 'country']).agg({
        'id': 'count',
        'is_approved': 'sum',
        'amount': 'sum',
        'approved_amount': 'sum'
    }).reset_index()
    
    result.columns = ['month', 'country', 'trans_count', 'approved_count',
                      'trans_total_amount', 'approved_total_amount']
    
    return result
```

## Pattern 7: Conditional Updates with loc

### LeetCode 1873: Calculate Special Bonus

**Problem**: Assign bonus based on conditions.

```python
def calculate_special_bonus(employees: pd.DataFrame) -> pd.DataFrame:
    # Initialize bonus to 0
    employees['bonus'] = 0
    
    # Condition: odd employee_id AND name doesn't start with 'M'
    mask = (
        (employees['employee_id'] % 2 == 1) & 
        (~employees['name'].str.startswith('M'))
    )
    
    # Assign salary as bonus where condition is met
    employees.loc[mask, 'bonus'] = employees.loc[mask, 'salary']
    
    return employees[['employee_id', 'bonus']].sort_values('employee_id')
```

## Pattern 8: Outer Joins for Finding Missing Data

### LeetCode 1148: Article Views I

**Problem**: Find authors who viewed their own articles.

```python
def article_views(views: pd.DataFrame) -> pd.DataFrame:
    # Filter where author == viewer
    self_views = views[views['author_id'] == views['viewer_id']]
    
    # Get unique authors
    result = self_views[['author_id']].drop_duplicates()
    result.columns = ['id']
    
    return result.sort_values('id')
```

## Pattern Summary

| Pattern | Methods Used | Common Use Case |
|---------|-------------|-----------------|
| GroupBy Aggregation | `groupby()`, `count()`, `sum()` | Counting, totaling |
| Merge/Join | `merge()`, `how='left/inner/outer'` | Combining tables |
| Self Merge | `merge()` with same DataFrame | Comparing rows |
| Pivot | `pivot()`, `pivot_table()` | Reshaping data |
| Ranking | `rank()`, `nlargest()` | Finding top N |
| Date Operations | `dt` accessor, `shift()`, `Timedelta` | Time comparisons |
| Conditional Update | `loc[]` with mask | Row-wise assignment |
| Multiple Aggregations | `agg()` with dict | Complex summaries |

## Common DataFrame Operations Quick Reference

```python
# GroupBy with multiple aggregations
df.groupby('col').agg({
    'value': ['sum', 'mean', 'count'],
    'other': 'max'
})

# Merge with different keys
df1.merge(df2, left_on='id1', right_on='id2', how='left')

# Self merge
df.merge(df, left_on='parent_id', right_on='id', suffixes=('', '_parent'))

# Conditional column
df['new_col'] = np.where(condition, value_if_true, value_if_false)

# Transform (broadcast aggregation back)
df['group_mean'] = df.groupby('group')['value'].transform('mean')

# Rank within groups
df['rank'] = df.groupby('group')['value'].rank(method='dense', ascending=False)
```


---

## Exercises

**Exercise 1.** Create a DataFrame with columns `'name'`, `'salary'`, and `'department'`. Write code to find the highest salary in each department.

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

**Exercise 2.** Write code to find all duplicate rows in a DataFrame based on a specific column using `duplicated()`.

??? success "Solution to Exercise 2"
    See the main content for the relevant patterns and API calls. The solution involves understanding how to combine Pandas operations to solve data manipulation problems.

---

**Exercise 3.** Create a DataFrame and write code to rank employees by salary within each department using `groupby()` and `rank()`.

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

**Exercise 4.** Write code that deletes rows where a specific column has null values, then resets the index.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    s = pd.Series(np.random.randn(100))
    s_clean = s.clip(lower=0)
    print(s_clean.describe())
    ```
