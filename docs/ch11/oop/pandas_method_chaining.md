# Method Chaining

!!! tip "Mental Model"
    Method chaining works because most pandas methods return a new DataFrame or Series. Each call in the chain takes the output of the previous call as input, forming a pipeline: `read -> clean -> filter -> transform -> aggregate`. This fluent style eliminates intermediate variables and makes the data flow read like a recipe.

## Fluent Interface

### 1. Concept

Method chaining returns self or new object:

```python
import pandas as pd

df = (pd.read_csv('data.csv')
      .dropna()
      .query('age > 25')
      .sort_values('name')
      .reset_index(drop=True))
```

### 2. Benefits

- Readable pipeline
- No intermediate variables
- Functional style

### 3. Design Pattern

Methods return DataFrame/Series:

```python
class DataFrame:
    def dropna(self):
        # ... operation
        return new_dataframe
```

## Common Chains

### 1. Cleaning Pipeline

```python
df_clean = (df
    .drop_duplicates()
    .dropna(subset=['key_column'])
    .replace({'old': 'new'})
    .reset_index(drop=True))
```

### 2. Transformation

```python
result = (df
    .assign(total=lambda x: x['a'] + x['b'])
    .pipe(lambda x: x[x['total'] > 10])
    .groupby('category')['total']
    .mean())
```

### 3. Aggregation

```python
summary = (df
    .groupby(['year', 'month'])
    .agg({'sales': 'sum', 'profit': 'mean'})
    .round(2))
```

## Pipe Method

The `pipe()` method enables clean functional programming with DataFrames by allowing any function to be called in a method chain.

### 1. Basic Syntax

```python
# Without pipe
result = custom_function(df)

# With pipe (chainable)
result = df.pipe(custom_function)
```

### 2. Custom Functions with pipe

```python
def remove_outliers(df, column, n_std=2):
    """Remove rows where column value is beyond n standard deviations."""
    mean = df[column].mean()
    std = df[column].std()
    return df[abs(df[column] - mean) < n_std * std]

def add_calculated_columns(df):
    """Add derived columns."""
    return df.assign(
        total=df['quantity'] * df['price'],
        tax=df['quantity'] * df['price'] * 0.1
    )

def format_currency(df, columns):
    """Format columns as currency strings."""
    df = df.copy()
    for col in columns:
        df[col] = df[col].apply(lambda x: f"${x:,.2f}")
    return df

# Use in a pipeline
result = (df
    .pipe(remove_outliers, 'price', n_std=3)
    .pipe(add_calculated_columns)
    .pipe(format_currency, ['total', 'tax']))
```

### 3. Passing Arguments to pipe

```python
# Function with multiple arguments
def filter_by_date_range(df, start, end, date_col='date'):
    mask = (df[date_col] >= start) & (df[date_col] <= end)
    return df[mask]

# Pass keyword arguments
result = df.pipe(filter_by_date_range, '2024-01-01', '2024-12-31')

# With explicit date column
result = df.pipe(filter_by_date_range, '2024-01-01', '2024-12-31', date_col='order_date')
```

### 4. Lambda Functions

```python
result = (df
    .pipe(lambda x: x[x['age'] > 18])
    .pipe(lambda x: x.assign(adult=True))
    .pipe(lambda x: x.sort_values('name')))
```

### 5. Alternative Syntax with Tuple

When your DataFrame is not the first argument:

```python
def merge_with_lookup(lookup_df, main_df, key):
    return main_df.merge(lookup_df, on=key)

# Using tuple: (function, arg_name_for_df)
result = df.pipe((merge_with_lookup, 'main_df'), lookup_table, key='id')
```

### 6. Debugging with pipe

```python
def debug_step(df, message=''):
    """Print debug info without modifying DataFrame."""
    print(f"{message}")
    print(f"  Shape: {df.shape}")
    print(f"  Columns: {list(df.columns)}")
    print(f"  Memory: {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
    return df

result = (df
    .pipe(debug_step, 'After loading')
    .query('value > 0')
    .pipe(debug_step, 'After filtering')
    .groupby('category').sum()
    .pipe(debug_step, 'After aggregation'))
```

### 7. Method Injection

```python
df.pipe(print)  # Debug intermediate state

# Log to file
def log_to_file(df, filename):
    with open(filename, 'a') as f:
        f.write(f"Shape: {df.shape}, Columns: {list(df.columns)}\n")
    return df

result = df.pipe(log_to_file, 'pipeline.log').query('x > 0')
```

### 8. Reusable Pipeline Functions

```python
def standard_cleaning_pipeline(df):
    """Standard data cleaning operations."""
    return (df
        .drop_duplicates()
        .dropna(subset=['id'])
        .assign(
            created_at=lambda x: pd.to_datetime(x['created_at']),
            updated_at=lambda x: pd.to_datetime(x['updated_at'])
        )
        .sort_values('created_at')
        .reset_index(drop=True))

# Apply to any DataFrame
clean_df = raw_df.pipe(standard_cleaning_pipeline)
```

### 9. Conditional Operations with pipe

```python
def maybe_filter(df, condition, column, threshold):
    """Conditionally apply filter."""
    if condition:
        return df[df[column] > threshold]
    return df

# Apply filter only if flag is True
result = df.pipe(maybe_filter, apply_filter, 'value', 100)
```

### 10. Financial Example

```python
def calculate_returns(df, price_col='close'):
    """Add return columns."""
    return df.assign(
        daily_return=df[price_col].pct_change(),
        cumulative_return=(1 + df[price_col].pct_change()).cumprod() - 1
    )

def add_moving_averages(df, windows=[20, 50], price_col='close'):
    """Add moving average columns."""
    for w in windows:
        df = df.assign(**{f'ma_{w}': df[price_col].rolling(w).mean()})
    return df

def flag_signals(df):
    """Add trading signals."""
    return df.assign(
        golden_cross=(df['ma_20'] > df['ma_50']) & (df['ma_20'].shift(1) <= df['ma_50'].shift(1)),
        death_cross=(df['ma_20'] < df['ma_50']) & (df['ma_20'].shift(1) >= df['ma_50'].shift(1))
    )

# Complete analysis pipeline
analysis = (stock_df
    .pipe(calculate_returns)
    .pipe(add_moving_averages, [20, 50, 200])
    .pipe(flag_signals)
    .dropna())
```

## Why Use pipe?

| Without pipe | With pipe |
|--------------|-----------|
| Nested function calls | Flat, readable chain |
| `f3(f2(f1(df)))` | `df.pipe(f1).pipe(f2).pipe(f3)` |
| Hard to debug | Easy to insert debug steps |
| Difficult to reorder | Simple to rearrange |

### Best Practices

1. **Keep functions pure**: Return new DataFrames, don't modify in place
2. **Single responsibility**: Each pipe function does one thing
3. **Document functions**: Add docstrings for complex operations
4. **Test independently**: Functions can be unit tested separately
5. **Use for clarity**: Don't pipe trivial operations

```python
# Good: Complex, reusable operation
df.pipe(standardize_column_names)

# Not needed: Simple operation
df.pipe(lambda x: x.head())  # Just use df.head()
```


---

## Exercises

**Exercise 1.** Write a method chain that: (1) reads/creates a DataFrame, (2) filters rows, (3) selects columns, and (4) sorts the result. Do it in a single expression.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'age': [25, 30, 35, 40, 28],
        'score': [85, 92, 78, 95, 88]
    })
    print(f'Shape: {df.shape}')
    print(f'Columns: {df.columns.tolist()}')
    print(f'Dtypes:\n{df.dtypes}')
    ```

---

**Exercise 2.** Explain the advantage of method chaining over step-by-step variable assignment. When might chaining be inappropriate?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas data structures and their relationships.

---

**Exercise 3.** Write code that uses `.pipe()` to include a custom function in a method chain.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'score': [85, 92, 78]
    })
    # Label-based
    print(df.loc[0])
    # Position-based
    print(df.iloc[-1])
    ```

---

**Exercise 4.** Rewrite the following step-by-step code as a method chain: filter rows where `age > 25`, select `name` and `salary` columns, sort by salary descending.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
    df['c'] = df['a'] + df['b']
    df = df.drop(columns=['b'])
    print(df)
    ```
