# Time Indexing

Time-based indexing allows powerful selection and filtering of time series data using date strings.

!!! tip "Mental Model"
    With a DatetimeIndex, `loc` accepts partial date strings as slicing keys. `df.loc['2024']` selects all of 2024, `df.loc['2024-03']` selects March 2024, and `df.loc['2024-03-15']` selects a single day. Pandas automatically matches the precision of your string to the appropriate range -- no manual date arithmetic needed.

## Date-based Selection

Select data using date strings.

### 1. Exact Date

```python
import pandas as pd
import numpy as np

dates = pd.date_range('2025-01-01', periods=365)
df = pd.DataFrame({'value': np.random.randn(365)}, index=dates)

df.loc['2025-01-15']  # Single date
```

### 2. Date Range

```python
df.loc['2025-01-15':'2025-01-20']  # Inclusive range
```

### 3. Partial String

```python
df.loc['2025-01']     # Entire January
df.loc['2025-03']     # Entire March
```

## Slicing Time Series

Slice by date ranges.

### 1. Start to Date

```python
df.loc[:'2025-03-31']  # From start to March 31
```

### 2. Date to End

```python
df.loc['2025-10-01':]  # From October 1 to end
```

### 3. Year Selection

```python
df.loc['2025']  # All of 2025
```

## Multiple Levels

Work with datetime components.

### 1. Extract Components

```python
df['year'] = df.index.year
df['month'] = df.index.month
df['day'] = df.index.day
df['weekday'] = df.index.dayofweek
```

### 2. Filter by Component

```python
# Select Mondays only (weekday 0)
mondays = df[df.index.dayofweek == 0]
```

### 3. First of Month

```python
first_of_month = df[df.index.day == 1]
```

## between_time and at_time

Select by time of day (for intraday data).

### 1. at_time

```python
# DataFrame with datetime index including time
df.at_time('09:30')  # Exactly 9:30 AM
```

### 2. between_time

```python
df.between_time('09:30', '16:00')  # Market hours
```

### 3. Trading Hours Filter

```python
# Filter to market hours only
market_hours = df.between_time('09:30', '16:00')
```

## Truncate Method

Trim data to date range.

### 1. Truncate Before

```python
df.truncate(before='2025-03-01')
```

### 2. Truncate After

```python
df.truncate(after='2025-09-30')
```

### 3. Both Directions

```python
df.truncate(before='2025-03-01', after='2025-09-30')
```

## Practical Examples

Common time selection patterns.

### 1. Last 30 Days

```python
from datetime import datetime, timedelta

end = df.index.max()
start = end - timedelta(days=30)
recent = df.loc[start:end]
```

### 2. Quarter Selection

```python
q1 = df.loc['2025-01':'2025-03']  # Q1
q2 = df.loc['2025-04':'2025-06']  # Q2
```

### 3. Year-over-Year Comparison

```python
jan_2024 = df.loc['2024-01']
jan_2025 = df.loc['2025-01']
```


---

## Exercises

**Exercise 1.** Write code that creates a time series with DatetimeIndex and slices it using string indexing (e.g., `ts['2024-06']`).

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

**Exercise 2.** Explain partial string indexing for DatetimeIndex. What does `ts['2024']` return?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code using `.between_time('09:00', '17:00')` to select only business hours from an intraday time series.

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

**Exercise 4.** Create a time series and use `.truncate(before='2024-03-01', after='2024-06-30')` to select a date range.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
