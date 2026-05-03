# Iteration with GroupBy

GroupBy objects support iteration, allowing you to process each group individually.

!!! tip "Mental Model"
    Iterating over a GroupBy yields `(key, sub_dataframe)` pairs, one per group. It is the escape hatch for custom logic that does not fit into `agg`, `transform`, or `filter`. Use it sparingly -- vectorized group operations are faster -- but it is invaluable for debugging or applying complex per-group logic.

## Basic Iteration

Iterate through groups as (name, group) pairs.

### 1. For Loop

```python
import pandas as pd

data = {
    'day': ['1/1/20', '1/2/20', '1/1/20', '1/2/20', '1/1/20', '1/2/20'],
    'city': ['NY', 'NY', 'SF', 'SF', 'LA', 'LA'],
    'temperature': [21, 14, 25, 32, 36, 42],
    'humidity': [31, 15, 36, 22, 16, 29],
}
df = pd.DataFrame(data)

for city, df_city in df.groupby("city"):
    print(city)
    print(df_city)
    print()
```

### 2. Tuple Unpacking

```python
# city: group key (string)
# df_city: DataFrame for that group
```

### 3. Output

```
LA
      day city  temperature  humidity
4  1/1/20   LA           36        16
5  1/2/20   LA           42        29

NY
      day city  temperature  humidity
0  1/1/20   NY           21        31
1  1/2/20   NY           14        15

SF
      day city  temperature  humidity
2  1/1/20   SF           25        36
3  1/2/20   SF           32        22
```

## Multiple Group Keys

Iterate with multiple grouping columns.

### 1. Tuple Keys

```python
for (city, day), group in df.groupby(['city', 'day']):
    print(f"City: {city}, Day: {day}")
    print(group)
    print()
```

### 2. Named Tuple

```python
# Keys are returned as tuple (city, day)
```

### 3. Access Individual Keys

```python
for keys, group in df.groupby(['city', 'day']):
    city, day = keys
    print(f"Processing {city} on {day}")
```

## Custom Processing

Apply custom logic to each group.

### 1. Compute Statistics

```python
results = []
for city, group in df.groupby('city'):
    results.append({
        'city': city,
        'mean_temp': group['temperature'].mean(),
        'max_temp': group['temperature'].max()
    })

summary = pd.DataFrame(results)
```

### 2. Conditional Logic

```python
for city, group in df.groupby('city'):
    if group['temperature'].mean() > 30:
        print(f"{city} is hot!")
```

### 3. Save to Files

```python
for city, group in df.groupby('city'):
    group.to_csv(f'{city}_data.csv', index=False)
```

## When to Use Iteration

Guidelines for choosing iteration vs aggregation.

### 1. Prefer Built-in Methods

```python
# Fast and optimized
df.groupby('city')['temperature'].mean()
```

### 2. Use Iteration When

```python
# Complex custom logic
# Need to output multiple files
# Debugging group contents
```

### 3. Performance

```python
# Built-in aggregations are much faster
# Iteration is slower but more flexible
```

---

## Exercises

**Exercise 1.**
Iterate over a GroupBy object and print each group name and the number of rows in that group. Use tuple unpacking in the for loop.

??? success "Solution to Exercise 1"
    Unpack group name and DataFrame in the for loop.

        import pandas as pd

        df = pd.DataFrame({
            'city': ['NY', 'NY', 'LA', 'SF', 'SF', 'SF'],
            'value': [10, 20, 30, 40, 50, 60]
        })
        for city, group in df.groupby('city'):
            print(f"{city}: {len(group)} rows")

---

**Exercise 2.**
Group a sales DataFrame by `'region'` and iterate to build a list of dictionaries, each containing the region name, total sales, and average order value. Convert the list to a DataFrame.

??? success "Solution to Exercise 2"
    Build summary statistics via iteration.

        import pandas as pd

        df = pd.DataFrame({
            'region': ['East', 'East', 'West', 'West', 'North'],
            'sales': [100, 200, 150, 250, 300]
        })
        results = []
        for region, group in df.groupby('region'):
            results.append({
                'region': region,
                'total_sales': group['sales'].sum(),
                'avg_order': group['sales'].mean()
            })
        summary = pd.DataFrame(results)
        print(summary)

---

**Exercise 3.**
Group by `['year', 'quarter']` and iterate using tuple unpacking for the composite key. Print each (year, quarter) combination along with the group's row count.

??? success "Solution to Exercise 3"
    Unpack composite keys from multi-column groupby.

        import pandas as pd

        df = pd.DataFrame({
            'year': [2023, 2023, 2023, 2024, 2024],
            'quarter': ['Q1', 'Q2', 'Q1', 'Q1', 'Q2'],
            'revenue': [100, 200, 150, 180, 220]
        })
        for (year, quarter), group in df.groupby(['year', 'quarter']):
            print(f"{year}-{quarter}: {len(group)} rows")
