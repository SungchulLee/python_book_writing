# isin Method

The `isin()` method filters rows where column values are in a specified list or set.

!!! tip "Mental Model"
    `isin()` is the pandas equivalent of SQL's `IN` clause. It checks each value against a set of allowed values and returns a boolean mask. Instead of chaining `(x == 'a') | (x == 'b') | (x == 'c')`, write `x.isin(['a', 'b', 'c'])` -- cleaner, faster, and scales to any number of values.

## Basic Usage

Check membership in a list.

### 1. Simple isin

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie', 'David'],
    'city': ['NY', 'LA', 'SF', 'NY']
})

# Filter where city is in list
result = df[df['city'].isin(['NY', 'SF'])]
print(result)
```

```
      name city
0    Alice   NY
2  Charlie   SF
3    David   NY
```

### 2. Boolean Result

```python
mask = df['city'].isin(['NY', 'SF'])
print(mask)
```

```
0     True
1    False
2     True
3     True
Name: city, dtype: bool
```

### 3. Apply Filter

```python
result = df[mask]
```

## NOT isin

Filter values NOT in list.

### 1. Negate with ~

```python
# Cities NOT in list
result = df[~df['city'].isin(['NY', 'SF'])]
print(result)
```

```
  name city
1  Bob   LA
```

### 2. Common Pattern

```python
# Find customers who never ordered
customers[~customers['id'].isin(orders['customerId'])]
```

### 3. Exclude Values

```python
# Remove specific categories
df[~df['category'].isin(['Deprecated', 'Deleted'])]
```

## LeetCode Example: Customers Who Never Order

Find customers not in orders.

### 1. Sample Data

```python
customers = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Alice', 'Bob', 'Charlie', 'David']
})

orders = pd.DataFrame({
    'customerId': [1, 3, 1]
})
```

### 2. Filter Not In

```python
result = customers[~customers['id'].isin(orders['customerId'])]
print(result)
```

```
   id   name
1   2    Bob
3   4  David
```

### 3. Select Column

```python
result = result[['name']].rename(columns={'name': 'Customers'})
```

## isin with Series

Use another column or Series as the list.

### 1. Column as List

```python
valid_ids = orders['customerId'].unique()
result = customers[customers['id'].isin(valid_ids)]
```

### 2. From Another DataFrame

```python
# Products sold in Q1
q1_products = q1_sales['product_id']
products_sold = products[products['id'].isin(q1_products)]
```

### 3. Dynamic Lists

```python
# Filter based on computed values
top_cities = df.groupby('city')['sales'].sum().nlargest(5).index
top_city_data = df[df['city'].isin(top_cities)]
```

## isin with Dictionary

Check multiple columns simultaneously.

### 1. Dict Syntax

```python
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['x', 'y', 'z']
})

# Check if values are in respective lists
mask = df.isin({'A': [1, 3], 'B': ['x', 'z']})
print(mask)
```

```
       A      B
0   True   True
1  False  False
2   True   True
```

### 2. Row Filter

```python
# Rows where ALL columns match
result = df[mask.all(axis=1)]

# Rows where ANY column matches
result = df[mask.any(axis=1)]
```

### 3. Use Case

```python
# Valid combinations
valid = {
    'department': ['Sales', 'Marketing'],
    'level': ['Senior', 'Manager']
}
filtered = df[df.isin(valid).all(axis=1)]
```

## Numeric isin

Filter numeric values.

### 1. Integer List

```python
df = pd.DataFrame({'id': [1, 2, 3, 4, 5]})
result = df[df['id'].isin([1, 3, 5])]
```

### 2. Float Values

```python
# Be careful with float precision
df[df['value'].isin([1.0, 2.0, 3.0])]
```

### 3. Range Alternative

```python
# For ranges, use comparison operators
df[(df['id'] >= 1) & (df['id'] <= 5)]
```

## Date isin

Filter specific dates.

### 1. Date List

```python
dates = pd.to_datetime(['2024-01-01', '2024-01-15', '2024-02-01'])
result = df[df['date'].isin(dates)]
```

### 2. Month Filter

```python
# Q1 months
result = df[df['date'].dt.month.isin([1, 2, 3])]
```

### 3. Year Filter

```python
result = df[df['date'].dt.year.isin([2023, 2024])]
```

## Performance

isin optimization.

### 1. Set for Large Lists

```python
# Convert to set for faster lookup
large_list = set(range(10000))
df[df['id'].isin(large_list)]
```

### 2. vs Multiple OR

```python
# isin is faster than multiple OR conditions
# Good
df[df['city'].isin(['NY', 'LA', 'SF'])]

# Slower
df[(df['city'] == 'NY') | (df['city'] == 'LA') | (df['city'] == 'SF')]
```

### 3. Merge Alternative

```python
# For very large lookups, merge can be faster
lookup = pd.DataFrame({'city': ['NY', 'LA', 'SF']})
result = df.merge(lookup, on='city')
```

---

## Exercises

**Exercise 1.**
Create a DataFrame of orders with a `'status'` column. Use `.isin()` to filter rows where the status is either `'shipped'` or `'delivered'`, excluding `'pending'` and `'cancelled'` orders.

??? success "Solution to Exercise 1"
    Pass a list of target values to `.isin()`.

        import pandas as pd

        df = pd.DataFrame({
            'order_id': [1, 2, 3, 4, 5],
            'status': ['shipped', 'pending', 'delivered', 'cancelled', 'shipped']
        })
        active = df[df['status'].isin(['shipped', 'delivered'])]
        print(active)

---

**Exercise 2.**
Use the negation of `.isin()` (with `~`) to find all employees whose department is NOT in the list `['HR', 'Finance']`. Print the filtered result.

??? success "Solution to Exercise 2"
    Negate the isin mask with `~`.

        import pandas as pd

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Carol', 'Dave'],
            'department': ['IT', 'HR', 'Finance', 'IT']
        })
        result = df[~df['department'].isin(['HR', 'Finance'])]
        print(result)

---

**Exercise 3.**
Given a DataFrame with `'ticker'` and `'sector'` columns, use `.isin()` on two columns simultaneously: filter rows where the ticker is in a watchlist AND the sector is in an approved sectors list.

??? success "Solution to Exercise 3"
    Combine two `.isin()` conditions with `&`.

        import pandas as pd

        df = pd.DataFrame({
            'ticker': ['AAPL', 'JPM', 'MSFT', 'XOM', 'GOOGL'],
            'sector': ['Tech', 'Finance', 'Tech', 'Energy', 'Tech']
        })
        watchlist = ['AAPL', 'MSFT', 'GOOGL']
        approved = ['Tech', 'Energy']
        result = df[df['ticker'].isin(watchlist) & df['sector'].isin(approved)]
        print(result)
