# select_dtypes Method

The `select_dtypes()` method filters DataFrame columns based on their data types. This is essential for applying type-specific operations and preparing data for analysis.

!!! tip "Mental Model"
    `select_dtypes` is a column filter based on type, not name. Pass `include='number'` to grab all numeric columns, or `exclude='object'` to drop all string columns. It is the first step in any pipeline that needs to treat numeric and categorical columns differently, such as scaling or encoding.

## Basic Usage

### Selecting Numeric Columns

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'age': [25, 30, 35],
    'salary': [50000.0, 60000.0, 70000.0],
    'department': pd.Categorical(['Sales', 'IT', 'HR']),
    'hire_date': pd.to_datetime(['2020-01-15', '2019-06-01', '2021-03-20']),
    'active': [True, True, False]
})

# Select numeric columns only
numeric_df = df.select_dtypes(include='number')
print(numeric_df)
```

```
   age    salary
0   25   50000.0
1   30   60000.0
2   35   70000.0
```

### Selecting by Multiple Types

```python
# Include multiple types
num_and_bool = df.select_dtypes(include=['number', 'bool'])
print(num_and_bool.columns.tolist())
# ['age', 'salary', 'active']
```

## Include vs Exclude

### Using include

```python
# Only string/object columns
strings = df.select_dtypes(include='object')
print(strings.columns.tolist())  # ['name']

# Only datetime columns
dates = df.select_dtypes(include='datetime')
print(dates.columns.tolist())  # ['hire_date']

# Only categorical columns
cats = df.select_dtypes(include='category')
print(cats.columns.tolist())  # ['department']
```

### Using exclude

```python
# Everything except objects and categories
non_categorical = df.select_dtypes(exclude=['object', 'category'])
print(non_categorical.columns.tolist())
# ['age', 'salary', 'hire_date', 'active']
```

### Combining include and exclude

```python
# Numeric but not integers
floats_only = df.select_dtypes(include='number', exclude='int')
print(floats_only.columns.tolist())  # ['salary']
```

## Common Type Selectors

| Selector | Matches |
|----------|---------|
| `'number'` | int64, float64, int32, etc. |
| `'int'` or `'int64'` | Integer types |
| `'float'` or `'float64'` | Float types |
| `'bool'` | Boolean |
| `'object'` | Strings and mixed types |
| `'category'` | Categorical |
| `'datetime'` or `'datetime64'` | Datetime |
| `'timedelta'` | Timedelta |
| `np.number` | All numeric types |
| `np.object_` | Object dtype |

## Practical Examples

### 1. Automatic Summary Statistics

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol'],
    'age': [25, 30, 35],
    'salary': [50000.0, 60000.0, 70000.0],
    'department': ['Sales', 'IT', 'HR']
})

# Describe only numeric columns (automatic with describe, but explicit here)
numeric_cols = df.select_dtypes(include='number')
print(numeric_cols.describe())

# Count unique values for non-numeric
non_numeric = df.select_dtypes(exclude='number')
print(non_numeric.nunique())
```

### 2. Preprocessing for Machine Learning

```python
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Separate numeric and categorical for different preprocessing
numeric_features = df.select_dtypes(include='number')
categorical_features = df.select_dtypes(include=['object', 'category'])

# Scale numeric features
scaler = StandardScaler()
df_numeric_scaled = pd.DataFrame(
    scaler.fit_transform(numeric_features),
    columns=numeric_features.columns
)

# Encode categorical features
df_categorical_encoded = categorical_features.apply(LabelEncoder().fit_transform)

# Combine
df_processed = pd.concat([df_numeric_scaled, df_categorical_encoded], axis=1)
print(df_processed)
```

### 3. Data Quality Report

```python
def data_quality_report(df):
    """Generate a data quality report by data type."""
    report = {}
    
    # Numeric columns
    numeric = df.select_dtypes(include='number')
    if not numeric.empty:
        report['numeric'] = {
            'columns': numeric.columns.tolist(),
            'missing': numeric.isnull().sum().to_dict(),
            'zeros': (numeric == 0).sum().to_dict()
        }
    
    # Categorical/Object columns
    categorical = df.select_dtypes(include=['object', 'category'])
    if not categorical.empty:
        report['categorical'] = {
            'columns': categorical.columns.tolist(),
            'unique_counts': categorical.nunique().to_dict(),
            'missing': categorical.isnull().sum().to_dict()
        }
    
    # Datetime columns
    datetime_cols = df.select_dtypes(include='datetime')
    if not datetime_cols.empty:
        report['datetime'] = {
            'columns': datetime_cols.columns.tolist(),
            'min': datetime_cols.min().to_dict(),
            'max': datetime_cols.max().to_dict()
        }
    
    return report

# Usage
report = data_quality_report(df)
print(report)
```

### 4. Memory Optimization by Downcasting

```python
def optimize_dtypes(df):
    """Downcast numeric types to save memory."""
    df_optimized = df.copy()
    
    # Downcast integers
    int_cols = df_optimized.select_dtypes(include='int').columns
    for col in int_cols:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
    
    # Downcast floats
    float_cols = df_optimized.select_dtypes(include='float').columns
    for col in float_cols:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='float')
    
    # Convert low-cardinality strings to category
    obj_cols = df_optimized.select_dtypes(include='object').columns
    for col in obj_cols:
        if df_optimized[col].nunique() / len(df_optimized) < 0.5:
            df_optimized[col] = df_optimized[col].astype('category')
    
    return df_optimized

# Compare memory usage
print(f"Original: {df.memory_usage(deep=True).sum()} bytes")
df_opt = optimize_dtypes(df)
print(f"Optimized: {df_opt.memory_usage(deep=True).sum()} bytes")
```

### 5. Financial Data Processing

```python
import yfinance as yf

# Get stock data
stock = yf.Ticker('AAPL').history(period='1mo')

# Identify column types
print("Numeric columns:", stock.select_dtypes(include='number').columns.tolist())
print("Other columns:", stock.select_dtypes(exclude='number').columns.tolist())

# Apply percentage formatting to numeric columns
numeric_cols = stock.select_dtypes(include='number').columns
stock_pct = stock.copy()
stock_pct[numeric_cols] = stock[numeric_cols].pct_change()
```

### 6. Correlation Matrix for Numeric Only

```python
# Calculate correlation only for numeric columns
numeric_df = df.select_dtypes(include='number')
correlation_matrix = numeric_df.corr()
print(correlation_matrix)
```

## Working with Nullable Types

pandas nullable types (Int64, Float64, boolean, string) are handled correctly.

```python
df = pd.DataFrame({
    'int_nullable': pd.array([1, 2, None], dtype='Int64'),
    'float_nullable': pd.array([1.0, None, 3.0], dtype='Float64'),
    'string_nullable': pd.array(['a', 'b', None], dtype='string'),
    'bool_nullable': pd.array([True, None, False], dtype='boolean')
})

# Numeric includes nullable integer and float
print(df.select_dtypes(include='number').columns.tolist())
# ['int_nullable', 'float_nullable']
```

## Combining with Other Operations

### Apply Function to Selected Types

```python
# Apply standardization only to numeric columns
def standardize(x):
    return (x - x.mean()) / x.std()

df[df.select_dtypes(include='number').columns] = (
    df.select_dtypes(include='number').apply(standardize)
)
```

### Filter Columns for Analysis

```python
# Get column names for specific analysis
numeric_cols = df.select_dtypes(include='number').columns.tolist()
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

# Use in groupby or analysis
for cat_col in categorical_cols:
    print(f"\n{cat_col}:")
    print(df.groupby(cat_col)[numeric_cols].mean())
```

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `include` | dtypes to include (str, type, or list) |
| `exclude` | dtypes to exclude (str, type, or list) |

**Note:** At least one of `include` or `exclude` must be provided.

## Common Pitfalls

### 1. Mixed Types in Object Columns

```python
df = pd.DataFrame({
    'mixed': [1, 'two', 3.0, None]  # Mixed types
})

print(df['mixed'].dtype)  # object
# This appears in object selection, not numeric!
selected = df.select_dtypes(include='object')
print(selected.columns.tolist())  # ['mixed']
```

### 2. Category vs Object

```python
df = pd.DataFrame({
    'cat': pd.Categorical(['a', 'b', 'c']),
    'obj': ['a', 'b', 'c']
})

print(df.select_dtypes(include='object').columns.tolist())  # ['obj']
print(df.select_dtypes(include='category').columns.tolist())  # ['cat']
# They're different types!
```

### 3. Boolean Treated Separately

```python
df = pd.DataFrame({
    'num': [1, 2, 3],
    'flag': [True, False, True]
})

# Boolean is NOT included in 'number'
print(df.select_dtypes(include='number').columns.tolist())  # ['num']
print(df.select_dtypes(include='bool').columns.tolist())  # ['flag']

# To include both:
print(df.select_dtypes(include=['number', 'bool']).columns.tolist())  # ['num', 'flag']
```

### 4. Empty Selection Returns Empty DataFrame

```python
df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})

# No datetime columns
result = df.select_dtypes(include='datetime')
print(result.empty)  # True
print(result.columns.tolist())  # []
```

---

## Exercises

**Exercise 1.**
Create a mixed-type DataFrame with integer, float, string, and boolean columns. Use `select_dtypes(include='number')` to select only numeric columns and print their column names.

??? success "Solution to Exercise 1"
    Use `include='number'` to get all numeric columns.

        import pandas as pd

        df = pd.DataFrame({
            'id': [1, 2, 3],
            'price': [9.99, 19.99, 29.99],
            'name': ['A', 'B', 'C'],
            'active': [True, False, True]
        })
        numeric_df = df.select_dtypes(include='number')
        print("Numeric columns:", numeric_df.columns.tolist())

---

**Exercise 2.**
Use `select_dtypes(exclude='object')` to remove all string columns from a DataFrame. Then compute `.describe()` on the resulting numeric-only DataFrame.

??? success "Solution to Exercise 2"
    Exclude object dtype to keep only non-string columns.

        import pandas as pd

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Carol'],
            'age': [25, 30, 35],
            'salary': [50000.0, 60000.0, 70000.0],
            'dept': ['HR', 'IT', 'Sales']
        })
        non_string = df.select_dtypes(exclude='object')
        print(non_string.describe())

---

**Exercise 3.**
Given a DataFrame with datetime, categorical, and numeric columns, use `select_dtypes` to select only `'datetime64'` columns. Print the selected column names and their dtypes.

??? success "Solution to Exercise 3"
    Select datetime columns by specifying the dtype.

        import pandas as pd

        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=3),
            'category': pd.Categorical(['A', 'B', 'A']),
            'value': [10, 20, 30]
        })
        datetime_cols = df.select_dtypes(include='datetime64')
        print("Datetime columns:", datetime_cols.columns.tolist())
        print(datetime_cols.dtypes)
