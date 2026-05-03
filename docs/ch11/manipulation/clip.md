# clip Method

The `clip()` method constrains values to a specified range.

!!! tip "Mental Model"
    `clip(lower, upper)` is a guardrail: any value below `lower` is raised to `lower`, any value above `upper` is capped at `upper`, and everything in between is untouched. It is the vectorized equivalent of `max(lower, min(x, upper))` applied to every element at once.

## Basic Usage

### Clipping with Lower and Upper Bounds

```python
import pandas as pd

s = pd.Series([1, 5, 10, 15, 20, 25])

# Clip values to range [5, 20]
clipped = s.clip(lower=5, upper=20)
print(clipped)
```

```
0     5
1     5
2    10
3    15
4    20
5    20
dtype: int64
```

### Only Lower or Upper Bound

```python
s.clip(lower=10)  # Values below 10 become 10
s.clip(upper=15)  # Values above 15 become 15
```

## DataFrame Clipping

### Clip All Columns

```python
df = pd.DataFrame({
    'A': [1, 5, 10, 15, 20],
    'B': [2, 8, 14, 22, 30]
})

clipped = df.clip(lower=5, upper=20)
print(clipped)
```

### Per-Column Clipping

```python
df = pd.DataFrame({'A': [1, 50, 100], 'B': [10, 500, 1000]})

# Different bounds for each column
clipped = df.clip(lower=[0, 100], upper=[80, 800], axis=1)
```

## Practical Examples

### 1. Outlier Capping

```python
def cap_outliers(df, columns):
    """Cap outliers at 1st and 99th percentiles."""
    df_capped = df.copy()
    for col in columns:
        lower = df[col].quantile(0.01)
        upper = df[col].quantile(0.99)
        df_capped[col] = df[col].clip(lower=lower, upper=upper)
    return df_capped
```

### 2. Normalizing to Range

```python
# Clip values to valid range before processing
scores = pd.Series([95, 105, 88, -5, 72])
valid_scores = scores.clip(lower=0, upper=100)
```

### 3. Financial Position Limits

```python
positions = pd.DataFrame({
    'ticker': ['AAPL', 'GOOGL', 'MSFT'],
    'weight': [0.45, 0.35, 0.20]
})

# Enforce max 40% position limit
positions['weight_capped'] = positions['weight'].clip(upper=0.40)
```

### 4. Signal Processing

```python
# Clip noisy sensor readings
readings = pd.Series([98, 102, 150, 95, 99, -10, 101])
clean_readings = readings.clip(lower=90, upper=110)
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `lower` | Minimum allowed value | None |
| `upper` | Maximum allowed value | None |
| `axis` | Align bounds along axis (0 or 1) | None |
| `inplace` | Modify in place | False |

## Notes

- At least one of `lower` or `upper` must be specified
- NaN values are not clipped (they remain NaN)
- Works with both Series and DataFrame
- Original data is not modified unless `inplace=True`

---

## Exercises

**Exercise 1.**
Create a Series with values ranging from -10 to 10. Use `.clip(lower=0, upper=5)` to constrain all values to the range [0, 5]. Verify that no values fall outside this range.

??? success "Solution to Exercise 1"
    Clip a Series to a specific range.

        import pandas as pd

        s = pd.Series(range(-10, 11))
        clipped = s.clip(lower=0, upper=5)
        print(clipped)
        assert clipped.min() >= 0
        assert clipped.max() <= 5
        print("All values within [0, 5].")

---

**Exercise 2.**
Create a DataFrame with two numeric columns. Use `.clip(lower=0)` to replace all negative values with 0 (no upper bound). Count how many values were clipped by comparing with the original.

??? success "Solution to Exercise 2"
    Clip negative values to zero and count changes.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'A': [1, -3, 5, -7, 2],
            'B': [-1, 4, -6, 8, -2]
        })
        clipped = df.clip(lower=0)
        n_clipped = (df < 0).sum().sum()
        print(clipped)
        print(f"Values clipped: {n_clipped}")

---

**Exercise 3.**
Given a DataFrame of daily stock returns (some extreme outliers), use `.clip()` to cap returns at +/- 5%. Print the number of values that were clipped on each side (above 5% and below -5%).

??? success "Solution to Exercise 3"
    Cap extreme stock returns at +/- 5%.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        returns = pd.DataFrame({
            'AAPL': np.random.randn(100) * 0.03,
            'MSFT': np.random.randn(100) * 0.03
        })
        above = (returns > 0.05).sum().sum()
        below = (returns < -0.05).sum().sum()
        clipped = returns.clip(lower=-0.05, upper=0.05)
        print(f"Clipped above 5%: {above}")
        print(f"Clipped below -5%: {below}")
        print(clipped.describe())
