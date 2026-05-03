# replace Method

The `replace()` method substitutes values in a DataFrame or Series. It is more general than `fillna()` and can replace any value, not just NaN.

!!! tip "Mental Model"
    `replace()` is find-and-replace for DataFrames. Unlike `fillna` which only targets NaN, `replace` swaps any value for any other value. Pass a dict of `{old: new}` pairs, a list of values to replace, or even a regex pattern. It is the right tool for cleaning up sentinel values like -999, "N/A", or typos.

## Basic Usage

Replace specific values with new values.

### 1. Replace NaN

```python
import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/codebasics/py/master/pandas/5_handling_missing_data_fillna_dropna_interpolate/weather_data.csv"
df = pd.read_csv(url, index_col='day', parse_dates=True)
print(df)

dg = df.replace(to_replace=np.nan, value=0)
print(dg)
```

### 2. Replace Single Value

```python
df.replace(to_replace=-999, value=np.nan)
```

### 3. Shorthand Syntax

```python
df.replace(-999, np.nan)  # Positional arguments
```

## Dictionary Replacement

Use dictionaries for multiple replacements.

### 1. Simple Dictionary

```python
df.replace({'old_value': 'new_value'})
```

### 2. Multiple Replacements

```python
df.replace({
    -999: np.nan,
    -1: 0,
    'N/A': np.nan
})
```

### 3. Column-specific

```python
df.replace({
    'column_A': {0: 100},
    'column_B': {'x': 'y'}
})
```

## List Replacement

Replace multiple values with a single value.

### 1. List to Scalar

```python
df.replace([np.nan, -999, 'NA'], 0)
```

### 2. List to List

```python
df.replace(
    to_replace=['low', 'medium', 'high'],
    value=[1, 2, 3]
)
```

### 3. Order Matters

```python
# Lists must have same length for one-to-one mapping
```

## Regex Replacement

Use regular expressions for pattern matching.

### 1. Enable Regex

```python
df['text'].replace(
    to_replace=r'^ba.$',
    value='new',
    regex=True
)
```

### 2. Pattern Replacement

```python
# Replace all strings starting with 'test'
df.replace(r'^test.*', 'replaced', regex=True)
```

### 3. Capture Groups

```python
df['col'].replace(
    r'(\d+)-(\d+)',
    r'\2-\1',
    regex=True
)  # Swap groups
```

## Comparison with fillna

When to use replace vs fillna.

### 1. fillna for NaN Only

```python
df.fillna(0)  # Only replaces NaN
```

### 2. replace for Any Value

```python
df.replace(-999, np.nan)  # Replaces any value
df.replace(np.nan, 0)     # Also replaces NaN
```

### 3. Use Case Guidance

```python
# Use fillna when specifically handling missing values
# Use replace when substituting specific values
```

## Practical Examples

Common replacement scenarios.

### 1. Clean Sentinel Values

```python
# Replace common missing value indicators
df.replace([-999, -1, 'NA', 'N/A', ''], np.nan)
```

### 2. Standardize Categories

```python
df['status'].replace({
    'Y': 'Yes', 'y': 'Yes', 'YES': 'Yes',
    'N': 'No', 'n': 'No', 'NO': 'No'
})
```

### 3. Fix Data Entry Errors

```python
df['country'].replace({
    'USA': 'United States',
    'U.S.A.': 'United States',
    'US': 'United States'
})
```

## Method Parameters

Additional parameters for replace.

### 1. inplace

```python
df.replace(-999, np.nan, inplace=True)
```

### 2. limit

```python
df.replace(-999, np.nan, limit=10)  # Max 10 replacements
```

### 3. method (Deprecated)

```python
# method parameter was used for forward/backward fill
# Now deprecated; use fillna instead
```

---

## Exercises

**Exercise 1.**
Create a DataFrame where `-999` is used as a sentinel for missing data. Use `.replace(-999, np.nan)` to convert these to proper `NaN` values. Then count the resulting `NaN` values.

??? success "Solution to Exercise 1"
    Replace sentinel values with NaN.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'temp': [21, -999, 25, -999],
            'humidity': [65, 68, -999, 75]
        })
        df = df.replace(-999, np.nan)
        print(df)
        print(f"Total NaN: {df.isna().sum().sum()}")

---

**Exercise 2.**
Create a Series with inconsistent string values (e.g., `'yes'`, `'Yes'`, `'YES'`, `'no'`, `'No'`). Use `.replace()` with a dictionary to standardize them to `'Yes'` and `'No'`.

??? success "Solution to Exercise 2"
    Standardize inconsistent string values.

        import pandas as pd

        s = pd.Series(['yes', 'Yes', 'YES', 'no', 'No', 'NO'])
        s = s.replace({'yes': 'Yes', 'YES': 'Yes', 'no': 'No', 'NO': 'No'})
        print(s)
        print(s.value_counts())

---

**Exercise 3.**
Create a DataFrame and use `.replace()` with `regex=True` to replace all strings matching a pattern (e.g., replace any value starting with `'old_'` with `'new_'`).

??? success "Solution to Exercise 3"
    Use regex replacement to transform matching values.

        import pandas as pd

        df = pd.DataFrame({
            'code': ['old_abc', 'old_def', 'new_ghi', 'old_jkl']
        })
        df['code'] = df['code'].replace(r'^old_', 'new_', regex=True)
        print(df)
