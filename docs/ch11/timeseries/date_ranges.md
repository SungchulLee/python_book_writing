# Creating Date Ranges

The `pd.date_range()` function generates sequences of dates with various frequencies and options.

!!! tip "Mental Model"
    `pd.date_range` is `range()` for dates. Specify any two of three: start, end, and periods, plus a frequency string like `'D'` (daily), `'B'` (business days), `'M'` (month-end), or `'H'` (hourly). The result is a DatetimeIndex ready to serve as a DataFrame index for time series data.

## Basic date_range

Generate date sequences.

### 1. With Periods

```python
import pandas as pd

dates = pd.date_range('2025-01-01', periods=6)
print(dates)
```

```
DatetimeIndex(['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04',
               '2025-01-05', '2025-01-06'],
              dtype='datetime64[ns]', freq='D')
```

### 2. With End Date

```python
dates = pd.date_range(start='2025-01-01', end='2025-01-10')
```

### 3. Specify Start and Periods

```python
dates = pd.date_range(start='2025-01-01', periods=10, freq='D')
```

## Frequency Options

Control the interval between dates.

### 1. Common Frequencies

```python
pd.date_range('2025-01-01', periods=5, freq='D')   # Daily
pd.date_range('2025-01-01', periods=5, freq='W')   # Weekly
pd.date_range('2025-01-01', periods=5, freq='M')   # Month end
pd.date_range('2025-01-01', periods=5, freq='Y')   # Year end
```

### 2. Business Frequencies

```python
pd.date_range('2025-01-01', periods=5, freq='B')   # Business days
pd.date_range('2025-01-01', periods=5, freq='BM')  # Business month end
pd.date_range('2025-01-01', periods=5, freq='BQ')  # Business quarter end
```

### 3. Intraday Frequencies

```python
pd.date_range('2025-01-01', periods=5, freq='H')   # Hourly
pd.date_range('2025-01-01', periods=5, freq='T')   # Minute
pd.date_range('2025-01-01', periods=5, freq='S')   # Second
```

## Using with DataFrames

Create time-indexed DataFrames.

### 1. As Index

```python
import numpy as np

dates = pd.date_range('2025-01-01', periods=6)
df = pd.DataFrame(
    np.random.randn(6, 4),
    index=dates,
    columns=list('ABCD')
)
print(df)
```

### 2. As Column

```python
df = pd.DataFrame({
    'date': pd.date_range('2025-01-01', periods=5),
    'value': [100, 101, 102, 103, 104]
})
```

### 3. Set as Index

```python
df = df.set_index('date')
```

## Period Ranges

Alternative to DatetimeIndex for periods.

### 1. period_range

```python
periods = pd.period_range('2025-01', periods=6, freq='M')
print(periods)
```

```
PeriodIndex(['2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06'],
            dtype='period[M]')
```

### 2. Month Periods

```python
months = pd.period_range('2025-01', '2025-12', freq='M')
```

### 3. Quarter Periods

```python
quarters = pd.period_range('2025Q1', periods=4, freq='Q')
```

## Practical Examples

Common date range patterns.

### 1. Trading Days

```python
# US trading days for 2025
trading_days = pd.date_range('2025-01-01', '2025-12-31', freq='B')
```

### 2. Monthly Data Points

```python
# End of each month
month_ends = pd.date_range('2025-01-31', periods=12, freq='M')
```

### 3. Specific Time Intervals

```python
# Every 6 hours
timestamps = pd.date_range('2025-01-01', periods=24, freq='6H')
```


---

## Exercises

**Exercise 1.** Write code that creates a DatetimeIndex using `pd.date_range()` with 30 business days starting from `'2024-01-01'`.

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

**Exercise 2.** Explain the `freq` parameter in `pd.date_range()`. List five common frequency strings (e.g., `'D'`, `'M'`, `'B'`).

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that creates a monthly date range for all of 2024 using `freq='MS'` (month start) and `freq='ME'` (month end).

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

**Exercise 4.** Create a DataFrame with a DatetimeIndex and demonstrate slicing by date string (e.g., `df['2024-03']`).

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
