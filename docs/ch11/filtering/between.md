# between Method

The `between()` method filters values within a range, inclusive of both endpoints.

!!! tip "Mental Model"
    `between(a, b)` is shorthand for `(x >= a) & (x <= b)`. It returns a boolean mask that is True for values inside the interval. Use it whenever you need a range filter -- it is cleaner than a double inequality and supports an `inclusive` parameter for open or half-open ranges.

## Basic Usage

Filter values in a range.

### 1. Numeric Range

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'age': [22, 28, 35, 42, 55]
})

# Filter age between 25 and 40
result = df[df['age'].between(25, 40)]
print(result)
```

```
      name  age
1      Bob   28
2  Charlie   35
```

### 2. Inclusive by Default

Both endpoints are included (25 and 40).

### 3. Boolean Result

```python
mask = df['age'].between(25, 40)
print(mask)
```

```
0    False
1     True
2     True
3    False
4    False
Name: age, dtype: bool
```

## inclusive Parameter

Control endpoint inclusion.

### 1. Both Endpoints (Default)

```python
df['age'].between(25, 40, inclusive='both')
# Includes 25 and 40
```

### 2. Neither Endpoint

```python
df['age'].between(25, 40, inclusive='neither')
# Excludes 25 and 40
```

### 3. Left or Right Only

```python
df['age'].between(25, 40, inclusive='left')   # Includes 25 only
df['age'].between(25, 40, inclusive='right')  # Includes 40 only
```

## Date Ranges

Filter dates within a period.

### 1. Date between

```python
activity = pd.DataFrame({
    'activity_date': pd.to_datetime([
        '2019-06-27', '2019-06-28', '2019-07-01',
        '2019-07-27', '2019-07-28'
    ]),
    'user_id': [1, 2, 3, 4, 5]
})

# Filter 30-day period
result = activity[
    activity['activity_date'].between('2019-06-28', '2019-07-27')
]
print(result)
```

```
  activity_date  user_id
1    2019-06-28        2
2    2019-07-01        3
3    2019-07-27        4
```

### 2. String Dates

Pandas automatically converts string dates.

### 3. Datetime Objects

```python
from datetime import datetime

start = datetime(2019, 6, 28)
end = datetime(2019, 7, 27)
result = activity[activity['activity_date'].between(start, end)]
```

## LeetCode Example: User Activity

Filter activity within date range.

### 1. Sample Data

```python
activity = pd.DataFrame({
    'activity_date': pd.to_datetime([
        '2019-06-27', '2019-06-28', '2019-07-01',
        '2019-07-15', '2019-07-27', '2019-07-28', '2019-08-01'
    ]),
    'user_id': [1, 2, 3, 4, 5, 6, 7]
})
```

### 2. Filter with between

```python
filtered = activity[
    activity['activity_date'].between('2019-06-28', '2019-07-27')
]
```

### 3. Count Unique Users

```python
active_users = filtered['user_id'].nunique()
```

## vs Comparison Operators

Equivalent operations.

### 1. between Syntax

```python
df[df['age'].between(25, 40)]
```

### 2. Comparison Syntax

```python
df[(df['age'] >= 25) & (df['age'] <= 40)]
```

### 3. Advantages

- between: cleaner, more readable
- Comparison: more flexible (exclusive bounds, etc.)

## String Ranges

Filter string values alphabetically.

### 1. Alphabetic Range

```python
df = pd.DataFrame({'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']})
result = df[df['name'].between('B', 'D')]
print(result)
```

```
     name
1     Bob
2  Charlie
```

### 2. Lexicographic Order

Strings are compared lexicographically.

### 3. Case Sensitivity

```python
# Uppercase letters come before lowercase in ASCII
# 'A' < 'Z' < 'a' < 'z'
```

## Numeric Precision

Handling float comparisons.

### 1. Float Range

```python
df = pd.DataFrame({'value': [0.1, 0.5, 1.0, 1.5, 2.0]})
result = df[df['value'].between(0.5, 1.5)]
```

### 2. Precision Issues

```python
# Be aware of floating point precision
# 0.1 + 0.2 != 0.3 in floating point
```

### 3. Round First

```python
df['value_rounded'] = df['value'].round(2)
result = df[df['value_rounded'].between(0.5, 1.5)]
```

## Combining with Other Filters

Use between with additional conditions.

### 1. AND Condition

```python
result = df[
    (df['age'].between(25, 40)) & 
    (df['city'] == 'NY')
]
```

### 2. OR Condition

```python
result = df[
    (df['age'].between(25, 40)) | 
    (df['salary'] > 100000)
]
```

### 3. Multiple between

```python
result = df[
    (df['age'].between(25, 40)) & 
    (df['salary'].between(50000, 80000))
]
```

---

## Exercises

**Exercise 1.**
Create a Series of daily temperatures and use `.between(15, 25)` to find days with comfortable temperatures. Print the filtered Series and the count of comfortable days.

??? success "Solution to Exercise 1"
    Use `.between()` to create a boolean mask for range filtering.

        import pandas as pd

        temps = pd.Series([10, 18, 22, 30, 15, 25, 8], name='temp')
        comfortable = temps[temps.between(15, 25)]
        print(comfortable)
        print(f"Comfortable days: {len(comfortable)}")

---

**Exercise 2.**
Given a DataFrame with a `'date'` column, use `.between()` to filter rows where dates fall in Q1 2024 (January 1 to March 31). Demonstrate that `between` works with string dates.

??? success "Solution to Exercise 2"
    The `.between()` method works with date strings.

        import pandas as pd

        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=120),
            'value': range(120)
        })
        q1 = df[df['date'].between('2024-01-01', '2024-03-31')]
        print(f"Q1 rows: {len(q1)}")
        print(q1.head())

---

**Exercise 3.**
Use `.between()` with `inclusive='neither'` to find stock prices strictly between two thresholds (excluding the boundaries). Compare the result count with `inclusive='both'` (the default).

??? success "Solution to Exercise 3"
    Compare `inclusive` parameter options.

        import pandas as pd

        prices = pd.Series([95, 100, 105, 110, 115, 120, 125])
        both = prices[prices.between(100, 120, inclusive='both')]
        neither = prices[prices.between(100, 120, inclusive='neither')]
        print(f"inclusive='both': {len(both)} values")
        print(f"inclusive='neither': {len(neither)} values")
