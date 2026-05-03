# fillna Keywords

The `fillna()` method accepts several keyword arguments that control how missing values are filled.

!!! tip "Mental Model"
    `method='ffill'` carries the last known value forward; `method='bfill'` pulls the next known value backward. `limit` caps how many consecutive NaN cells get filled. These keywords turn `fillna` from a simple constant-fill into a directional propagation tool, ideal for time series where "no new data means the old value still holds."

## method Keyword

Propagate non-null values forward or backward.

### 1. Forward Fill (ffill)

```python
import pandas as pd

url = "https://raw.githubusercontent.com/codebasics/py/master/pandas/5_handling_missing_data_fillna_dropna_interpolate/weather_data.csv"
df = pd.read_csv(url, index_col='day', parse_dates=True)
print(df)

dg = df.fillna(method='ffill')
print(dg)
```

Forward fill propagates the last valid observation forward.

### 2. Backward Fill (bfill)

```python
dg = df.fillna(method='bfill')
print(dg)
```

Backward fill uses the next valid observation to fill gaps.

### 3. pad Alias

```python
df.fillna(method='pad')    # Same as ffill
df.fillna(method='backfill')  # Same as bfill
```

## axis Keyword

Specify the axis along which to fill missing values.

### 1. Fill Along Rows (axis=0)

```python
dg = df.fillna(method='ffill', axis=0)
print(dg)
```

Default behavior: fill down columns.

### 2. Fill Along Columns (axis=1)

```python
dg = df.fillna(method='ffill', axis=1)
print(dg)
```

Fill across rows from left to right.

### 3. Numeric vs String Columns

When filling along axis=1, be aware that mixed types may cause issues.

## limit Keyword

Limit the number of consecutive NaN values to fill.

### 1. Limit Forward Fill

```python
dg = df.fillna(method='ffill', limit=1)
print(dg)
```

Only fills up to 1 consecutive NaN value.

### 2. Preventing Over-filling

```python
# If there are 3 consecutive NaNs and limit=2
# Only the first 2 will be filled
```

### 3. Use Case

```python
# In time series, limit prevents filling across
# long gaps where forward fill may be inappropriate
df['price'].fillna(method='ffill', limit=5)
```

## Combined Keywords

Use multiple keywords together for precise control.

### 1. Forward Fill with Limit

```python
df.fillna(method='ffill', axis=0, limit=2)
```

### 2. Backward Fill with Limit

```python
df.fillna(method='bfill', axis=0, limit=1)
```

### 3. Fill Strategy

```python
# First forward fill, then backward fill remaining
df_filled = df.fillna(method='ffill').fillna(method='bfill')
```

## Modern Syntax

In recent pandas versions, prefer explicit methods over the `method` keyword.

### 1. ffill Method

```python
df.ffill()           # Forward fill
df.ffill(limit=2)    # With limit
```

### 2. bfill Method

```python
df.bfill()           # Backward fill
df.bfill(limit=1)    # With limit
```

### 3. Deprecation Note

The `method` parameter in `fillna` is deprecated in newer pandas versions:

```python
# Deprecated
df.fillna(method='ffill')

# Preferred
df.ffill()
```

---

## Exercises

**Exercise 1.**
Create a Series with multiple consecutive `NaN` values. Use `fillna(method='ffill', limit=1)` to forward-fill only one step. Verify that the second consecutive `NaN` remains unfilled.

??? success "Solution to Exercise 1"
    Forward fill with a limit of 1.

        import pandas as pd
        import numpy as np

        s = pd.Series([1, np.nan, np.nan, np.nan, 5])
        result = s.fillna(method='ffill', limit=1)
        print(result)
        # Index 1 gets filled (1.0), index 2 and 3 stay NaN

---

**Exercise 2.**
Create a DataFrame and use `fillna()` with a dictionary to apply different fill strategies per column (e.g., column A gets 0, column B gets the column mean).

??? success "Solution to Exercise 2"
    Per-column fill strategies using a dictionary.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'A': [1, np.nan, 3],
            'B': [np.nan, 5, np.nan]
        })
        fill_values = {'A': 0, 'B': df['B'].mean()}
        result = df.fillna(fill_values)
        print(result)

---

**Exercise 3.**
Create a DataFrame with `NaN` values. Compare the results of `fillna(method='ffill')` and `fillna(method='bfill')` when the first or last row has `NaN`. Identify which positions remain unfilled by each method.

??? success "Solution to Exercise 3"
    Compare ffill and bfill at edges.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({'val': [np.nan, 2, np.nan, 4, np.nan]})
        ffilled = df.fillna(method='ffill')
        bfilled = df.fillna(method='bfill')
        print("ffill:\n", ffilled)
        print("\nbfill:\n", bfilled)
        # ffill cannot fill the first row; bfill cannot fill the last row
