# Multi-Level Grouping

Group by multiple columns to create hierarchical aggregations.

!!! tip "Mental Model"
    Grouping by multiple columns creates a cross-tabulation: each unique combination of values forms one group. The result has a MultiIndex with one level per grouping column. Think of it as nested folders -- region, then city -- where each leaf folder contains the rows for that specific combination.

## Basic Multi-Level

Group by multiple columns.

### 1. Two-Level Grouping

```python
import pandas as pd

df = pd.DataFrame({
    'region': ['East', 'East', 'West', 'West'],
    'product': ['A', 'B', 'A', 'B'],
    'sales': [100, 150, 200, 250]
})

result = df.groupby(['region', 'product'])['sales'].sum()
print(result)
```

```
region  product
East    A          100
        B          150
West    A          200
        B          250
Name: sales, dtype: int64
```

### 2. MultiIndex Result

The result has a hierarchical index.

### 3. Access Levels

```python
result['East']      # All products in East
result['East', 'A']  # Specific combination
```

## reset_index

Flatten the hierarchical result.

### 1. Convert to DataFrame

```python
result = df.groupby(['region', 'product'])['sales'].sum().reset_index()
print(result)
```

```
  region product  sales
0   East       A    100
1   East       B    150
2   West       A    200
3   West       B    250
```

### 2. as_index=False

```python
df.groupby(['region', 'product'], as_index=False)['sales'].sum()
```

### 3. Equivalent Results

Both approaches produce a flat DataFrame.

## Aggregations with Multiple Columns

Apply aggregations to grouped data.

### 1. Single Aggregation

```python
df.groupby(['region', 'product']).agg({'sales': 'sum'})
```

### 2. Multiple Aggregations

```python
df.groupby(['region', 'product']).agg({
    'sales': ['sum', 'mean', 'count']
})
```

### 3. Named Aggregations

```python
df.groupby(['region', 'product']).agg(
    total_sales=('sales', 'sum'),
    avg_sales=('sales', 'mean')
)
```

## unstack Method

Reshape grouped results.

### 1. Basic unstack

```python
result = df.groupby(['region', 'product'])['sales'].sum().unstack()
print(result)
```

```
product    A    B
region           
East     100  150
West     200  250
```

### 2. Pivot-like Output

unstack moves inner index level to columns.

### 3. Fill Missing

```python
result.unstack(fill_value=0)
```

## Practical Example

Financial sector analysis.

### 1. Sample Data

```python
df = pd.DataFrame({
    'sector': ['Tech', 'Tech', 'Finance', 'Finance'],
    'ticker': ['AAPL', 'MSFT', 'JPM', 'GS'],
    'per': [25.5, 30.2, 12.1, 10.8],
    'market_cap': [2800, 2400, 450, 120]
})
```

### 2. Grouped Statistics

```python
stats = df.groupby('sector').agg({
    'per': ['mean', 'min', 'max'],
    'market_cap': 'sum'
})
print(stats)
```

### 3. Reset and Flatten

```python
stats.columns = ['_'.join(col) for col in stats.columns]
stats = stats.reset_index()
```

---

## Exercises

**Exercise 1.**
Group a DataFrame by `['region', 'product']` and compute the sum of `'sales'`. Then use `.unstack()` to reshape the result into a pivot-like table with regions as rows and products as columns.

??? success "Solution to Exercise 1"
    Group, aggregate, and unstack for a pivot-like view.

        import pandas as pd

        df = pd.DataFrame({
            'region': ['East', 'East', 'West', 'West'],
            'product': ['A', 'B', 'A', 'B'],
            'sales': [100, 150, 200, 250]
        })
        result = df.groupby(['region', 'product'])['sales'].sum().unstack()
        print(result)

---

**Exercise 2.**
Apply named aggregations with multi-level grouping: group by `['sector', 'ticker']` and compute `total_volume=('volume', 'sum')` and `avg_price=('price', 'mean')`. Flatten the column index and reset the row index.

??? success "Solution to Exercise 2"
    Named aggregations with multi-level grouping.

        import pandas as pd

        df = pd.DataFrame({
            'sector': ['Tech', 'Tech', 'Finance', 'Finance'],
            'ticker': ['AAPL', 'MSFT', 'JPM', 'GS'],
            'volume': [1000, 800, 500, 300],
            'price': [150.0, 350.0, 180.0, 380.0]
        })
        result = df.groupby(['sector', 'ticker']).agg(
            total_volume=('volume', 'sum'),
            avg_price=('price', 'mean')
        ).reset_index()
        print(result)

---

**Exercise 3.**
Group by two columns and access a specific sub-group using bracket indexing on the resulting MultiIndex Series: `result['East']` to get all products in the East region, and `result['East', 'A']` for a specific combination.

??? success "Solution to Exercise 3"
    Access sub-groups in a MultiIndex result.

        import pandas as pd

        df = pd.DataFrame({
            'region': ['East', 'East', 'West', 'West'],
            'product': ['A', 'B', 'A', 'B'],
            'sales': [100, 150, 200, 250]
        })
        result = df.groupby(['region', 'product'])['sales'].sum()
        print("All East:", result['East'])
        print("East-A:", result['East', 'A'])
