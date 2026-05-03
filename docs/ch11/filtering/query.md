# query Method

The `query()` method filters DataFrames using a string expression, providing cleaner syntax for complex conditions.

!!! tip "Mental Model"
    `query()` lets you write filter conditions as a readable string instead of bracket-heavy boolean expressions. `df.query("age > 30 and city == 'NY'")` replaces `df[(df['age'] > 30) & (df['city'] == 'NY')]`. The result is identical, but the string form is closer to how you think about the condition in plain English.

## Basic Usage

Filter with string expressions.

### 1. Simple Condition

```python
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'Salary': [50000, 60000, 70000, 80000]
})

# Equivalent operations
result1 = df[df['Age'] < 35]          # Boolean indexing
result2 = df.query('Age < 35')         # Query method

print(result2)
```

```
      Name  Age  Salary
0    Alice   25   50000
1      Bob   30   60000
```

### 2. Cleaner Syntax

Query avoids repeated DataFrame references.

### 3. Column Names

Use column names directly in the query string.

## Multiple Conditions

Combine conditions with and/or.

### 1. AND Condition

```python
# Boolean indexing
df[(df['Age'] > 25) & (df['Salary'] > 50000)]

# Query method
df.query('Age > 25 and Salary > 50000')
```

### 2. OR Condition

```python
df.query('Age > 35 or Salary < 55000')
```

### 3. Complex Conditions

```python
df.query('(Age > 30 and Salary > 60000) or Name == "Alice"')
```

## Column Comparisons

Compare columns against each other.

### 1. Column vs Column

```python
df = pd.DataFrame({
    'Subscribers': [760, 366, 1660, 171],
    'Age': [40, 50, 25, 35]
})

# Subscribers > 10 * Age
df.query('Subscribers > 10 * Age')
```

### 2. Arithmetic Expressions

```python
df.query('Salary / 1000 > Age')
```

### 3. Multiple Columns

```python
df.query('High > Open and Close > Open')
```

## External Variables

Reference variables with @ prefix.

### 1. Variable Reference

```python
limit = 500

# Boolean indexing
df[df['Subscribers'] > limit]

# Query method
df.query('Subscribers > @limit')
```

### 2. Multiple Variables

```python
min_age = 25
max_age = 40
df.query('@min_age <= Age <= @max_age')
```

### 3. List Variables

```python
valid_names = ['Alice', 'Bob']
df.query('Name in @valid_names')
```

## String Operations

Query with string conditions.

### 1. Equality

```python
df.query('Name == "Alice"')
```

### 2. In List

```python
df.query('Name in ["Alice", "Bob"]')
```

### 3. Not In

```python
df.query('Name not in ["Charlie", "David"]')
```

## Detecting NaN

Special handling for missing values.

### 1. NaN Detection

```python
# NaN != NaN is True
df.query('Subscribers != Subscribers')  # Finds NaN rows
```

### 2. Not NaN

```python
df.query('Subscribers == Subscribers')  # Non-NaN rows
```

### 3. Alternative

```python
# More readable alternatives
df[df['Subscribers'].isna()]
df[df['Subscribers'].notna()]
```

## Date Queries

Filter by date ranges.

### 1. Date Range

```python
df.query('request_at >= "2013-10-01" and request_at <= "2013-10-03"')
```

### 2. Year Filter

```python
df.query('sale_date.dt.year == 2019')
```

### 3. Month Filter

```python
df.query('sale_date.dt.month in [1, 2, 3]')
```

## LeetCode Example: Sales Analysis

Filter sales by date.

### 1. Sample Data

```python
sales = pd.DataFrame({
    'sale_date': pd.to_datetime(['2019-01-15', '2019-04-10', '2018-12-25']),
    'product_id': [1, 2, 3]
})
```

### 2. Filter Q1 2019

```python
q1_sales = sales.query('sale_date.dt.year == 2019 and sale_date.dt.month in [1, 2, 3]')
```

### 3. Exclude Q1 2019

```python
not_q1 = sales.query('sale_date.dt.year != 2019 or sale_date.dt.month not in [1, 2, 3]')
```

## Spaces in Column Names

Handle column names with spaces.

### 1. Backticks

```python
df = pd.DataFrame({'First Name': ['Alice', 'Bob']})
df.query('`First Name` == "Alice"')
```

### 2. Rename Columns

```python
# Better to avoid spaces in column names
df.columns = df.columns.str.replace(' ', '_')
```

### 3. Alternative

```python
df[df['First Name'] == 'Alice']  # Boolean indexing works
```

## Performance

When to use query.

### 1. Large DataFrames

Query can be faster for large DataFrames.

### 2. Complex Conditions

Query is cleaner for multiple conditions.

### 3. Simple Filters

Boolean indexing is fine for simple filters.

## Query vs Boolean Indexing

Comparison of approaches.

### 1. Query Advantages

- Cleaner syntax for complex conditions
- No repeated DataFrame name
- More readable

### 2. Boolean Indexing Advantages

- More flexible
- Works with any expression
- No string parsing

### 3. Choose Based On

- Readability needs
- Condition complexity
- Personal preference

---

## Exercises

**Exercise 1.**
Create a DataFrame with columns `'product'`, `'price'`, and `'quantity'`. Use `.query()` to find products where `price > 20` and `quantity < 100`. Compare the readability with equivalent boolean indexing.

??? success "Solution to Exercise 1"
    Use `.query()` with a readable string expression.

        import pandas as pd

        df = pd.DataFrame({
            'product': ['Widget', 'Gadget', 'Gizmo', 'Tool'],
            'price': [15, 25, 30, 10],
            'quantity': [200, 50, 80, 150]
        })
        result = df.query('price > 20 and quantity < 100')
        print(result)

---

**Exercise 2.**
Use `.query()` with the `@` syntax to reference a Python variable. Given a variable `min_salary = 60000`, write a query that filters employees with `salary >= @min_salary`.

??? success "Solution to Exercise 2"
    Reference external variables with `@` inside query strings.

        import pandas as pd

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Carol'],
            'salary': [55000, 65000, 72000]
        })
        min_salary = 60000
        result = df.query('salary >= @min_salary')
        print(result)

---

**Exercise 3.**
Use `.query()` with string methods by filtering a DataFrame where the `'name'` column starts with the letter `'A'`. Use the backtick syntax if the column name contains spaces.

??? success "Solution to Exercise 3"
    Use string methods inside `.query()`.

        import pandas as pd

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Anna', 'Charlie'],
            'score': [85, 90, 78, 92]
        })
        result = df.query('name.str.startswith("A")', engine='python')
        print(result)
