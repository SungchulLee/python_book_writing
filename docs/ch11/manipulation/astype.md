# Type Conversion with astype

The `astype()` method converts Series or DataFrame columns to a specified data type. This is essential for data cleaning, memory optimization, and ensuring correct operations.

!!! tip "Mental Model"
    `astype()` is an explicit type cast for an entire column. It tells pandas "reinterpret every value under this new dtype." Common uses include converting strings to numbers after cleaning, shrinking int64 to int8 for memory savings, and switching to categorical. If a value cannot be converted, it raises an error -- use `pd.to_numeric(errors='coerce')` for graceful handling.

## Basic Usage

### Series Conversion

```python
import pandas as pd

s = pd.Series([1, 2, 3])
print(f"Original dtype: {s.dtype}")  # int64

# Convert to float
s_float = s.astype('float64')
print(f"Converted dtype: {s_float.dtype}")  # float64
print(s_float)
```

```
0    1.0
1    2.0
2    3.0
dtype: float64
```

### DataFrame Column Conversion

```python
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['4', '5', '6']
})

# Convert single column
df['B'] = df['B'].astype(int)
print(df.dtypes)
```

```
A    int64
B    int64
dtype: object
```

### Multiple Columns at Once

```python
df = pd.DataFrame({
    'A': ['1', '2', '3'],
    'B': ['4.0', '5.0', '6.0'],
    'C': ['True', 'False', 'True']
})

# Convert multiple columns using a dictionary
df = df.astype({
    'A': 'int64',
    'B': 'float64'
})
print(df.dtypes)
```

## Common Type Conversions

### String to Numeric

```python
s = pd.Series(['1', '2', '3'])
s_int = s.astype(int)
s_float = s.astype(float)
```

### Numeric to String

```python
s = pd.Series([1, 2, 3])
s_str = s.astype(str)
print(s_str)
```

```
0    1
1    2
2    3
dtype: object
```

### To Boolean

```python
s = pd.Series([0, 1, 0, 1])
s_bool = s.astype(bool)
print(s_bool)
```

```
0    False
1     True
2    False
3     True
dtype: bool
```

### To Category

```python
s = pd.Series(['low', 'medium', 'high', 'low', 'medium'])
s_cat = s.astype('category')
print(s_cat)
print(f"Categories: {s_cat.cat.categories.tolist()}")
```

```
0       low
1    medium
2      high
3       low
4    medium
dtype: category
Categories (3, object): ['high', 'low', 'medium']
```

## Practical Example: Trip Status Encoding

From LeetCode 262: Convert trip status to binary for cancellation rate calculation.

```python
trips = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'status': ['completed', 'cancelled_by_driver', 'completed', 
               'cancelled_by_client', 'completed']
})

# Step 1: Replace status strings with integers
status_encoded = trips['status'].replace({
    'cancelled_by_driver': 1,
    'cancelled_by_client': 1,
    'completed': 0
})
print(status_encoded)
```

```
0    0
1    1
2    0
3    1
4    0
Name: status, dtype: int64
```

```python
# Step 2: Ensure integer type (important after replace)
status_encoded = status_encoded.astype(int)

# Calculate cancellation rate
cancellation_rate = status_encoded.sum() / len(status_encoded)
print(f"Cancellation rate: {cancellation_rate:.2%}")  # 40.00%
```

### Why astype(int) After Replace?

The `replace()` method may return mixed types if not all values are replaced. Using `astype(int)` ensures consistent integer type for calculations.

```python
# Example where replace might leave mixed types
df = pd.DataFrame({
    'status': ['completed', 'cancelled_by_driver', 'in_progress']
})

# 'in_progress' is not in the mapping, remains as string
result = df['status'].replace({
    'cancelled_by_driver': 1,
    'completed': 0
})
print(result.dtype)  # object (mixed)

# Force to numeric (will error if truly invalid)
# result.astype(int)  # Would raise ValueError
```

## Handling Conversion Errors

### errors Parameter

```python
s = pd.Series(['1', '2', 'three', '4'])

# Default: raises error
# s.astype(int)  # ValueError

# With pd.to_numeric for error handling
s_numeric = pd.to_numeric(s, errors='coerce')
print(s_numeric)
```

```
0    1.0
1    2.0
2    NaN
3    4.0
dtype: float64
```

### Safe Conversion Pattern

```python
def safe_convert(series, dtype):
    """Safely convert series to dtype, returning None on failure."""
    try:
        return series.astype(dtype)
    except (ValueError, TypeError) as e:
        print(f"Conversion failed: {e}")
        return None

s = pd.Series(['1', '2', 'invalid'])
result = safe_convert(s, int)  # Conversion failed
```

## Memory Optimization

### Downcasting Integers

```python
# Default int64 uses 8 bytes per value
s = pd.Series([1, 2, 3, 4, 5])
print(f"int64 memory: {s.memory_usage()} bytes")

# Downcast to int8 (1 byte) for small integers
s_small = s.astype('int8')
print(f"int8 memory: {s_small.memory_usage()} bytes")
```

### Integer Types and Their Ranges

| Type | Bytes | Range |
|------|-------|-------|
| int8 | 1 | -128 to 127 |
| int16 | 2 | -32,768 to 32,767 |
| int32 | 4 | -2B to 2B |
| int64 | 8 | -9×10¹⁸ to 9×10¹⁸ |
| uint8 | 1 | 0 to 255 |

### Using pd.to_numeric with Downcast

```python
s = pd.Series([1, 2, 3, 100, 200])

# Automatically choose smallest integer type
s_downcast = pd.to_numeric(s, downcast='integer')
print(f"Downcast dtype: {s_downcast.dtype}")  # int8
```

## Nullable Integer Types

pandas supports nullable integers that can hold NaN values.

```python
# Standard int64 cannot hold NaN
s = pd.Series([1, 2, None])
print(s.dtype)  # float64 (upcasted)

# Nullable integer preserves integer nature
s = pd.Series([1, 2, None], dtype='Int64')
print(s)
```

```
0       1
1       2
2    <NA>
dtype: Int64
```

### Converting to Nullable

```python
s = pd.Series([1.0, 2.0, float('nan')])
s_nullable = s.astype('Int64')
print(s_nullable)
```

```
0       1
1       2
2    <NA>
dtype: Int64
```

## Datetime Conversions

### String to Datetime

```python
s = pd.Series(['2024-01-01', '2024-01-02', '2024-01-03'])

# Using astype
s_datetime = s.astype('datetime64[ns]')

# Better: using pd.to_datetime for more control
s_datetime = pd.to_datetime(s)
print(s_datetime)
```

### Datetime to String

```python
dates = pd.Series(pd.date_range('2024-01-01', periods=3))
dates_str = dates.astype(str)
print(dates_str)
```

```
0    2024-01-01
1    2024-01-02
2    2024-01-03
dtype: object
```

## Practical Example: Data Cleaning Pipeline

```python
# Raw data with mixed types
raw_data = pd.DataFrame({
    'user_id': ['1', '2', '3', '4'],
    'age': ['25', '30', '28', 'unknown'],
    'premium': ['1', '0', '1', '1'],
    'signup_date': ['2024-01-01', '2024-01-15', '2024-02-01', '2024-02-15']
})

# Clean and convert types
cleaned = raw_data.copy()

# Convert user_id to int
cleaned['user_id'] = cleaned['user_id'].astype(int)

# Convert age to numeric, coercing errors
cleaned['age'] = pd.to_numeric(cleaned['age'], errors='coerce')

# Convert premium to boolean
cleaned['premium'] = cleaned['premium'].astype(int).astype(bool)

# Convert signup_date to datetime
cleaned['signup_date'] = pd.to_datetime(cleaned['signup_date'])

print(cleaned.dtypes)
```

```
user_id                  int64
age                    float64
premium                   bool
signup_date    datetime64[ns]
dtype: object
```

## Financial Example: Portfolio Data Types

```python
portfolio = pd.DataFrame({
    'ticker': ['AAPL', 'MSFT', 'GOOGL'],
    'shares': ['100', '150', '50'],
    'price': ['150.25', '350.50', '140.75'],
    'sector': ['Tech', 'Tech', 'Tech']
})

# Convert to appropriate types
portfolio = portfolio.astype({
    'shares': 'int64',
    'price': 'float64',
    'sector': 'category'
})

# Calculate position values
portfolio['value'] = portfolio['shares'] * portfolio['price']
print(portfolio)
print(f"\nData types:\n{portfolio.dtypes}")
```

## Summary of Type Conversions

| From | To | Method |
|------|-----|--------|
| str → int | `s.astype(int)` | Direct conversion |
| str → float | `s.astype(float)` | Direct conversion |
| str → datetime | `pd.to_datetime(s)` | Preferred for dates |
| int → str | `s.astype(str)` | Direct conversion |
| float → int | `s.astype(int)` | Truncates decimals |
| object → category | `s.astype('category')` | Memory efficient |
| int64 → Int64 | `s.astype('Int64')` | Nullable integer |

---

## Exercises

**Exercise 1.**
Create a DataFrame with a column of string numbers (e.g., `['1', '2', '3']`). Convert it to `int` using `.astype(int)`. Then convert it to `float64` and verify the dtype changed.

??? success "Solution to Exercise 1"
    Convert string numbers to int then float.

        import pandas as pd

        df = pd.DataFrame({'nums': ['1', '2', '3']})
        print("Original dtype:", df['nums'].dtype)
        df['nums'] = df['nums'].astype(int)
        print("After int:", df['nums'].dtype)
        df['nums'] = df['nums'].astype('float64')
        print("After float64:", df['nums'].dtype)

---

**Exercise 2.**
Create a DataFrame with an `int64` column where values range from 0 to 100. Convert it to `int8` using `.astype('int8')` to save memory. Use `.memory_usage()` to compare memory before and after.

??? success "Solution to Exercise 2"
    Downcast int64 to int8 and compare memory.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({'values': np.random.randint(0, 101, 10000).astype('int64')})
        mem_before = df['values'].memory_usage(deep=True)
        df['values'] = df['values'].astype('int8')
        mem_after = df['values'].memory_usage(deep=True)
        print(f"Before: {mem_before} bytes")
        print(f"After:  {mem_after} bytes")

---

**Exercise 3.**
Create a DataFrame with a column containing mixed values including some that cannot be converted to numeric (e.g., `'N/A'`). Demonstrate that `.astype(float)` raises an error, then use `pd.to_numeric()` with `errors='coerce'` as an alternative to convert valid values and set invalid ones to `NaN`.

??? success "Solution to Exercise 3"
    Handle conversion errors with pd.to_numeric.

        import pandas as pd

        df = pd.DataFrame({'col': ['1.5', '2.0', 'N/A', '4.0']})
        try:
            df['col'].astype(float)
        except ValueError as e:
            print(f"astype error: {e}")

        df['col'] = pd.to_numeric(df['col'], errors='coerce')
        print(df)
        print(df.dtypes)
