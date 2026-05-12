# LeetCode Series Problems

This document covers common LeetCode patterns involving pandas Series operations. These problems demonstrate practical applications of Series methods for data manipulation and analysis.

!!! tip "Mental Model"
    Series-level LeetCode problems focus on single-column transformations: mapping values, filtering with boolean masks, and computing rolling or cumulative statistics. The key insight is that almost every operation stays within one Series and returns another Series of the same length, keeping the solution vectorized and loop-free.

## Pattern 1: Value Replacement with astype

### LeetCode 262: Trips and Users

**Problem**: Calculate cancellation rate by converting status strings to binary values.

```python
def trips_and_users(trips: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    # Filter unbanned users
    banned_users = users[users['banned'] == 'Yes']['users_id']
    filtered_trips = trips[
        ~trips['client_id'].isin(banned_users) & 
        ~trips['driver_id'].isin(banned_users)
    ]
    
    # Convert status to binary: cancelled=1, completed=0
    cancelled = filtered_trips['status'].replace({
        'cancelled_by_driver': 1,
        'cancelled_by_client': 1,
        'completed': 0
    }).astype(int)
    
    # Calculate cancellation rate
    cancellation_rate = cancelled.sum() / len(cancelled)
    return cancellation_rate
```

**Key Concepts**:

- `replace()` maps categorical values to numeric
- `astype(int)` ensures consistent integer type
- Series arithmetic for rate calculation

## Pattern 2: Boolean Filtering with isin

### LeetCode 183: Customers Who Never Order

**Problem**: Find customers not present in orders table.

```python
def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    # Find customers whose id is NOT in orders
    no_orders = customers[~customers['id'].isin(orders['customerId'])]
    return no_orders[['name']].rename(columns={'name': 'Customers'})
```

**Key Concepts**:

- `isin()` checks membership in another Series
- `~` negates boolean Series
- Boolean indexing filters DataFrame

### Step-by-Step Breakdown

```python
# Sample data
customers = pd.DataFrame({
    'id': [1, 2, 3],
    'name': ['Alice', 'Bob', 'Charlie']
})
orders = pd.DataFrame({'customerId': [1, 3]})

# Step 1: Check membership
mask = customers['id'].isin(orders['customerId'])
print(mask)  # True, False, True

# Step 2: Negate to find non-members
mask = ~mask
print(mask)  # False, True, False

# Step 3: Filter
result = customers[mask]
print(result)  # Bob (id=2)
```

## Pattern 3: Missing Value Detection with isna/isnull

### LeetCode 608: Tree Node

**Problem**: Classify tree nodes as Root, Inner, or Leaf.

```python
def tree_node(tree: pd.DataFrame) -> pd.DataFrame:
    # Root: p_id is null
    tree.loc[tree['p_id'].isna(), 'type'] = 'Root'
    
    # Inner: has parent AND has children
    has_children = tree['id'].isin(tree['p_id'])
    tree.loc[has_children & tree['p_id'].notna(), 'type'] = 'Inner'
    
    # Leaf: has parent but no children
    tree.loc[~has_children & tree['p_id'].notna(), 'type'] = 'Leaf'
    
    return tree[['id', 'type']]
```

**Key Concepts**:

- `isna()` detects missing values
- `notna()` detects non-missing values
- `.loc[]` for conditional assignment

### LeetCode 1965: Employees With Missing Information

**Problem**: Find employees with incomplete records.

```python
def employees_with_missing_info(
    employees: pd.DataFrame, 
    salaries: pd.DataFrame
) -> pd.DataFrame:
    # Merge with outer join
    merged = employees.merge(salaries, on='employee_id', how='outer')
    
    # Find rows with any missing value
    missing = merged[merged.isna().any(axis=1)]
    
    return missing[['employee_id']].sort_values('employee_id')
```

**Key Concepts**:

- `isna()` returns boolean DataFrame
- `any(axis=1)` checks if any column is True per row
- Boolean indexing on aggregated condition

## Pattern 4: Counting with value_counts and nunique

### LeetCode 570: Managers with 5+ Direct Reports

**Problem**: Find managers who have at least 5 direct reports.

```python
def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    # Count direct reports per manager
    manager_counts = employee['managerId'].value_counts()
    
    # Filter managers with 5+ reports
    qualified = manager_counts[manager_counts >= 5].index
    
    # Get manager names
    return employee[employee['id'].isin(qualified)][['name']]
```

**Key Concepts**:

- `value_counts()` counts occurrences
- Index contains unique values
- Filter on count threshold

### LeetCode 550: Game Play Analysis IV

**Problem**: Calculate fraction of players who logged in on consecutive days.

```python
def game_play_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    # Get first login date per player
    first_login = activity.groupby('player_id')['event_date'].min()
    
    # Count total unique players
    total_players = activity['player_id'].nunique()
    
    # Check for next-day login
    activity['first_date'] = activity['player_id'].map(first_login)
    activity['next_day'] = activity['first_date'] + pd.Timedelta(days=1)
    
    # Count players with next-day login
    next_day_logins = activity[
        activity['event_date'] == activity['next_day']
    ]['player_id'].nunique()
    
    fraction = next_day_logins / total_players
    return pd.DataFrame({'fraction': [round(fraction, 2)]})
```

**Key Concepts**:

- `nunique()` counts unique values
- `groupby().min()` finds first occurrence
- Date arithmetic with Timedelta

## Pattern 5: String Operations

### LeetCode 1667: Fix Names in a Table

**Problem**: Capitalize first letter, lowercase rest.

```python
def fix_names(users: pd.DataFrame) -> pd.DataFrame:
    users['name'] = users['name'].str.capitalize()
    return users.sort_values('user_id')
```

### LeetCode 1683: Invalid Tweets

**Problem**: Find tweets with content > 15 characters.

```python
def invalid_tweets(tweets: pd.DataFrame) -> pd.DataFrame:
    return tweets[tweets['content'].str.len() > 15][['tweet_id']]
```

### LeetCode 1873: Calculate Special Bonus

**Problem**: Bonus for employees with odd ID and name not starting with 'M'.

```python
def calculate_special_bonus(employees: pd.DataFrame) -> pd.DataFrame:
    # Condition: odd ID AND name doesn't start with M
    condition = (
        (employees['employee_id'] % 2 != 0) & 
        (~employees['name'].str.startswith('M'))
    )
    
    # Assign bonus
    employees['bonus'] = 0
    employees.loc[condition, 'bonus'] = employees.loc[condition, 'salary']
    
    return employees[['employee_id', 'bonus']].sort_values('employee_id')
```

### LeetCode 1517: Find Users With Valid E-Mails

**Problem**: Filter users with valid email format.

```python
def valid_emails(users: pd.DataFrame) -> pd.DataFrame:
    pattern = r'^[A-Za-z][A-Za-z0-9_.\-]*@leetcode\.com$'
    valid = users[users['mail'].str.match(pattern)]
    return valid
```

### LeetCode 620: Not Boring Movies

**Problem**: Find movies with odd ID and description not containing "boring".

```python
def not_boring_movies(cinema: pd.DataFrame) -> pd.DataFrame:
    condition = (
        (cinema['id'] % 2 != 0) & 
        (~cinema['description'].str.contains('boring', case=False))
    )
    return cinema[condition].sort_values('rating', ascending=False)
```

## Pattern 6: Value Replacement

### LeetCode 627: Swap Salary

**Problem**: Swap 'm' and 'f' values in sex column.

```python
def swap_salary(salary: pd.DataFrame) -> pd.DataFrame:
    salary['sex'] = salary['sex'].replace({'m': 'f', 'f': 'm'})
    return salary
```

**Key Concepts**:

- `replace()` with dictionary for bidirectional swap
- In-place modification of column

## Pattern 7: Rolling Window

### LeetCode 1321: Restaurant Growth

**Problem**: Calculate 7-day rolling sum of amounts.

```python
def restaurant_growth(customer: pd.DataFrame) -> pd.DataFrame:
    # Group by date and sum amounts
    daily = customer.groupby('visited_on')['amount'].sum().reset_index()
    
    # Set date as index for rolling
    daily = daily.set_index('visited_on').sort_index()
    
    # Calculate 7-day rolling sum
    daily['rolling_sum'] = daily['amount'].rolling('7D').sum()
    
    # Filter to rows with full 7-day window
    # (at least 7 days from first date)
    min_date = daily.index.min() + pd.Timedelta(days=6)
    result = daily[daily.index >= min_date].reset_index()
    
    return result[['visited_on', 'rolling_sum']]
```

**Key Concepts**:

- `rolling('7D')` creates time-based window
- Requires DatetimeIndex
- `.sum()` aggregates within window

## Pattern 8: Aggregation to DataFrame

### LeetCode 619: Biggest Single Number

**Problem**: Find the largest number that appears only once.

```python
def biggest_single_number(my_numbers: pd.DataFrame) -> pd.DataFrame:
    # Find numbers appearing exactly once
    counts = my_numbers['num'].value_counts()
    unique = counts[counts == 1].index
    
    # Get max or None
    if len(unique) > 0:
        result = my_numbers[my_numbers['num'].isin(unique)]['num'].max()
    else:
        result = None
    
    return pd.DataFrame({'num': [result]})
```

**Alternative using to_frame()**:

```python
def biggest_single_number(my_numbers: pd.DataFrame) -> pd.DataFrame:
    unique = my_numbers.drop_duplicates(keep=False)
    return unique['num'].max().to_frame(name='num') if len(unique) > 0 \
           else pd.DataFrame({'num': [None]})
```

## Pattern Summary

| Pattern | Methods Used | Common Use Case |
|---------|-------------|-----------------|
| Value Replacement | `replace()`, `astype()` | Encoding categories |
| Boolean Filtering | `isin()`, `~` | Set membership |
| Missing Detection | `isna()`, `notna()`, `any()` | Data quality |
| Counting | `value_counts()`, `nunique()` | Frequency analysis |
| String Operations | `str.capitalize()`, `str.contains()` | Text processing |
| Rolling Windows | `rolling()`, `sum()` | Time series |
| Aggregation | `to_frame()`, `reset_index()` | Result formatting |


---

## Exercises

**Exercise 1.** Create a Series of integers and write code to find all values that appear more than once using `value_counts()`.

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

**Exercise 2.** Write code to find the second-highest value in a Series without sorting the entire Series.

??? success "Solution to Exercise 2"
    See the main content for the relevant patterns and API calls. The solution involves understanding how to combine Pandas operations to solve data manipulation problems.

---

**Exercise 3.** Create a Series of strings and write code to find all entries longer than 5 characters using `.str.len()`.

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

**Exercise 4.** Write code that replaces all negative values in a Series with 0 using boolean indexing.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    s = pd.Series(np.random.randn(100))
    s_clean = s.clip(lower=0)
    print(s_clean.describe())
    ```
