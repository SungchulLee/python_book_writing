# explode Method

The `explode()` method transforms list-like elements in a column into separate rows, duplicating the index for each element. This is essential for normalizing nested data structures.

!!! tip "Mental Model"
    `explode` is the inverse of `groupby(...).agg(list)`. If a cell contains a list like `[a, b, c]`, explode creates three rows -- one per element -- duplicating the values in all other columns. It normalizes nested data into a flat, one-value-per-row format suitable for standard pandas operations.

## Basic Usage

### Exploding a Single Column

```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'hobbies': [['reading', 'chess'], ['hiking'], ['painting', 'music', 'cooking']]
})

print("Original:")
print(df)

exploded = df.explode('hobbies')
print("\nExploded:")
print(exploded)
```

```
Original:
    name                      hobbies
0  Alice             [reading, chess]
1    Bob                     [hiking]
2  Carol  [painting, music, cooking]

Exploded:
    name   hobbies
0  Alice   reading
0  Alice     chess
1    Bob    hiking
2  Carol  painting
2  Carol     music
2  Carol   cooking
```

### Index Preservation

Notice that the index is preserved and duplicated. This maintains the relationship to the original row.

```python
# To get a fresh sequential index
exploded_reset = df.explode('hobbies').reset_index(drop=True)
print(exploded_reset)
```

## Handling Empty Lists and NaN

### Empty Lists Become NaN

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'items': [['a', 'b'], [], ['c']]
})

exploded = df.explode('items')
print(exploded)
```

```
    name items
0  Alice     a
0  Alice     b
1    Bob   NaN
2  Carol     c
```

### NaN Values Stay NaN

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob'],
    'items': [['a', 'b'], None]
})

exploded = df.explode('items')
print(exploded)
```

```
    name items
0  Alice     a
0  Alice     b
1    Bob  None
```

## Exploding Multiple Columns

### Synchronized Explosion (pandas 1.3+)

When two columns have lists of the same length, you can explode them together.

```python
df = pd.DataFrame({
    'id': [1, 2],
    'keys': [['a', 'b'], ['c', 'd', 'e']],
    'values': [[10, 20], [30, 40, 50]]
})

# Explode both columns together
exploded = df.explode(['keys', 'values'])
print(exploded)
```

```
   id keys  values
0   1    a      10
0   1    b      20
1   2    c      30
1   2    d      40
1   2    e      50
```

### Mismatched Lengths Cause Errors

```python
df = pd.DataFrame({
    'id': [1],
    'keys': [['a', 'b']],
    'values': [[10, 20, 30]]  # Length mismatch!
})

# This will raise ValueError
# df.explode(['keys', 'values'])
```

## Practical Examples

### 1. Normalizing JSON Data

```python
# Data from an API with nested structure
data = pd.DataFrame({
    'user_id': [1, 2, 3],
    'username': ['alice', 'bob', 'carol'],
    'tags': [
        ['python', 'data'],
        ['javascript', 'react', 'node'],
        ['python', 'ml', 'deep-learning']
    ]
})

# Normalize to one tag per row
normalized = data.explode('tags')

# Count tag frequency
tag_counts = normalized['tags'].value_counts()
print(tag_counts)
```

### 2. Stock Holdings Breakdown

```python
# Portfolio with multiple holdings per account
portfolio = pd.DataFrame({
    'account': ['IRA', 'Brokerage'],
    'tickers': [['AAPL', 'GOOGL', 'MSFT'], ['VTI', 'BND']],
    'shares': [[100, 50, 75], [500, 200]]
})

# Explode to individual holdings
holdings = portfolio.explode(['tickers', 'shares'])
print(holdings)
```

```
     account tickers shares
0        IRA    AAPL    100
0        IRA   GOOGL     50
0        IRA    MSFT     75
1  Brokerage     VTI    500
1  Brokerage     BND    200
```

### 3. Email Recipients

```python
emails = pd.DataFrame({
    'subject': ['Meeting', 'Report', 'Update'],
    'recipients': [
        ['alice@company.com', 'bob@company.com'],
        ['carol@company.com'],
        ['alice@company.com', 'bob@company.com', 'carol@company.com']
    ],
    'sent_date': ['2024-01-15', '2024-01-16', '2024-01-17']
})

# One row per recipient
expanded = emails.explode('recipients')

# Count emails per recipient
print(expanded['recipients'].value_counts())
```

### 4. Processing Survey Responses

```python
survey = pd.DataFrame({
    'respondent_id': [1, 2, 3],
    'selected_options': [
        ['Option A', 'Option C'],
        ['Option B'],
        ['Option A', 'Option B', 'Option C', 'Option D']
    ]
})

# Expand to analyze individual selections
expanded = survey.explode('selected_options')

# Cross-tabulation
print(pd.crosstab(expanded['respondent_id'], expanded['selected_options']))
```

### 5. Time Series with Multiple Events

```python
events = pd.DataFrame({
    'date': pd.to_datetime(['2024-01-01', '2024-01-02']),
    'events': [
        ['login', 'purchase', 'logout'],
        ['login', 'browse']
    ],
    'timestamps': [
        ['09:00', '10:30', '11:00'],
        ['14:00', '14:15']
    ]
})

# Expand events with their timestamps
expanded = events.explode(['events', 'timestamps'])
print(expanded)
```

## Working with String Data

If your "list" is actually a string representation, you need to convert it first.

### String to List Conversion

```python
df = pd.DataFrame({
    'id': [1, 2],
    'tags': ['["python", "data"]', '["ml", "ai"]']  # String, not list!
})

# Check type
print(type(df['tags'].iloc[0]))  # <class 'str'>

# Convert string to list using ast.literal_eval
import ast
df['tags'] = df['tags'].apply(ast.literal_eval)

# Now explode works
exploded = df.explode('tags')
print(exploded)
```

### Comma-Separated Strings

```python
df = pd.DataFrame({
    'id': [1, 2],
    'tags': ['python,data,ml', 'javascript,react']
})

# Split string into list, then explode
df['tags'] = df['tags'].str.split(',')
exploded = df.explode('tags')
print(exploded)
```

## Inverse Operation: Aggregating Back

To reverse an explode operation, use groupby with a list aggregation.

```python
# Exploded data
exploded = pd.DataFrame({
    'name': ['Alice', 'Alice', 'Bob', 'Bob', 'Bob'],
    'hobby': ['reading', 'chess', 'hiking', 'camping', 'fishing']
})

# Aggregate back to lists
aggregated = exploded.groupby('name')['hobby'].agg(list).reset_index()
print(aggregated)
```

```
    name                        hobby
0  Alice              [reading, chess]
1    Bob  [hiking, camping, fishing]
```

## Performance Considerations

### Memory Impact

Exploding creates many new rows, which can significantly increase memory usage.

```python
# Original: 1000 rows, average 10 items per list = 10,000 rows after explode
df = pd.DataFrame({
    'id': range(1000),
    'items': [list(range(10)) for _ in range(1000)]
})

print(f"Original rows: {len(df)}")
exploded = df.explode('items')
print(f"Exploded rows: {len(exploded)}")
```

### Processing Large Datasets

For very large datasets, consider processing in chunks:

```python
def explode_in_chunks(df, column, chunk_size=10000):
    """Explode a large DataFrame in chunks."""
    chunks = []
    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start:start + chunk_size]
        chunks.append(chunk.explode(column))
    return pd.concat(chunks, ignore_index=True)
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `column` | Column(s) to explode | Required |
| `ignore_index` | Reset index to sequential integers | False |

## Common Pitfalls

### 1. Expecting Original Index After reset_index

```python
exploded = df.explode('items')
# Index is duplicated (0, 0, 1, 1, 2, 2, ...)

# Use reset_index for sequential index
exploded = df.explode('items').reset_index(drop=True)
# Now index is (0, 1, 2, 3, 4, 5, ...)
```

### 2. Scalar Values Don't Explode

```python
df = pd.DataFrame({
    'id': [1, 2],
    'value': [10, 20]  # Scalars, not lists
})

exploded = df.explode('value')
print(exploded)  # No change - scalars stay as is
```

### 3. Nested Lists Stay Nested

```python
df = pd.DataFrame({
    'id': [1],
    'nested': [[['a', 'b'], ['c', 'd']]]  # List of lists
})

exploded = df.explode('nested')
print(exploded)
```

```
   id  nested
0   1  [a, b]
0   1  [c, d]
```

To fully flatten, you need multiple explode calls or a custom approach.


---

## Exercises

**Exercise 1.** Write code that uses `df.explode('col')` to convert a column containing lists into separate rows.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd
    import numpy as np

    # Solution for the specific exercise
    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10)})
    print(df.head())
    ```

---

**Exercise 2.** Explain when `explode()` is useful. Give a real-world example of data that would benefit from it.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Create a DataFrame where one column contains comma-separated strings. Split them into lists with `.str.split(',')` and then use `explode()`.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(20), 'B': np.random.randn(20)})
    result = df.describe()
    print(result)
    ```

---

**Exercise 4.** Write code showing that `explode()` preserves the original index. How can you reset it?

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
