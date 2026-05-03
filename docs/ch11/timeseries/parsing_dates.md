# Parsing Dates

Parsing dates involves converting string representations of dates and times into datetime objects. This is essential for time series analysis and date-based operations in pandas.

!!! tip "Mental Model"
    A date string like `"2024-01-15"` is just text -- you cannot add days or extract the month from it. `pd.to_datetime()` parses the string into a Timestamp object that understands calendar logic. Always parse date columns at load time (`parse_dates` in `read_csv`) rather than after, so every downstream operation benefits from proper datetime dtype.

## Understanding Date Parsing

### String vs Datetime

```python
import pandas as pd

# String - limited operations
date_str = "2024-01-15"
print(type(date_str))  # <class 'str'>

# Datetime - full date operations
date_dt = pd.to_datetime(date_str)
print(type(date_dt))   # <class 'pandas._libs.tslibs.timestamps.Timestamp'>
print(date_dt.year)    # 2024
print(date_dt.month)   # 1
print(date_dt.day)     # 15
```

### Why Parse Dates?

1. **Date arithmetic**: Add/subtract time periods
2. **Component extraction**: Get year, month, day, etc.
3. **Filtering**: Select date ranges
4. **Resampling**: Aggregate by time periods
5. **Sorting**: Chronological ordering

## pd.to_datetime()

The primary function for converting to datetime.

### Basic Usage

```python
# Single value
date = pd.to_datetime('2024-01-15')
print(date)  # 2024-01-15 00:00:00

# Series
s = pd.Series(['2024-01-15', '2024-01-16', '2024-01-17'])
dates = pd.to_datetime(s)
print(dates)
```

```
0   2024-01-15
1   2024-01-16
2   2024-01-17
dtype: datetime64[ns]
```

### Automatic Format Detection

pandas can often infer the date format automatically:

```python
# Various formats - all parsed correctly
formats = [
    '2024-01-15',       # ISO format
    '01/15/2024',       # US format
    '15-01-2024',       # European format
    'January 15, 2024', # Written format
    '2024/01/15',       # Slash format
]

for f in formats:
    print(f"{f:20} -> {pd.to_datetime(f)}")
```

### Specifying Format

For faster parsing or ambiguous formats, specify the format explicitly.

```python
# Explicit format
s = pd.Series(['01/15/2024', '02/20/2024', '03/25/2024'])

# Without format (slower, may be ambiguous)
dates = pd.to_datetime(s)

# With format (faster, unambiguous)
dates = pd.to_datetime(s, format='%m/%d/%Y')
```

### Common Format Codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | 2024 |
| `%y` | 2-digit year | 24 |
| `%m` | Month (01-12) | 01 |
| `%d` | Day (01-31) | 15 |
| `%H` | Hour (00-23) | 14 |
| `%I` | Hour (01-12) | 02 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%f` | Microsecond | 000000 |
| `%p` | AM/PM | PM |
| `%B` | Full month name | January |
| `%b` | Abbreviated month | Jan |
| `%A` | Full weekday | Monday |
| `%a` | Abbreviated weekday | Mon |

### Handling Errors

```python
s = pd.Series(['2024-01-15', 'invalid', '2024-01-17'])

# Default: raises error
# pd.to_datetime(s)  # ValueError

# errors='coerce': invalid dates become NaT (Not a Time)
dates = pd.to_datetime(s, errors='coerce')
print(dates)
```

```
0   2024-01-15
1          NaT
2   2024-01-17
dtype: datetime64[ns]
```

```python
# errors='ignore': return original input unchanged
dates = pd.to_datetime(s, errors='ignore')
print(dates)
```

```
0    2024-01-15
1       invalid
2    2024-01-17
dtype: object
```

### Unix Timestamps

```python
# Unix timestamps (seconds since 1970-01-01)
timestamps = pd.Series([1705276800, 1705363200, 1705449600])
dates = pd.to_datetime(timestamps, unit='s')
print(dates)
```

```
0   2024-01-15
1   2024-01-16
2   2024-01-17
dtype: datetime64[ns]
```

| Unit | Description |
|------|-------------|
| `'D'` | Days |
| `'s'` | Seconds |
| `'ms'` | Milliseconds |
| `'us'` | Microseconds |
| `'ns'` | Nanoseconds |

## Parsing in pd.read_csv()

### parse_dates Parameter

```python
url = 'https://raw.githubusercontent.com/srivatsan88/YouTubeLI/master/dataset/electricity_consumption.csv'

# Without parsing - dates are strings
df = pd.read_csv(url)
print(df['Bill_Date'].dtype)  # object

# With parse_dates=True - attempt to parse index
df = pd.read_csv(url, index_col='Bill_Date', parse_dates=True)
print(df.index.dtype)  # datetime64[ns]

# With parse_dates=['column'] - parse specific columns
df = pd.read_csv(url, parse_dates=['Bill_Date'])
print(df['Bill_Date'].dtype)  # datetime64[ns]
```

### date_format Parameter

Specify the format for date columns:

```python
# When date format is known
df = pd.read_csv(url, parse_dates=['Bill_Date'], date_format='%m/%d/%Y')
```

### Multiple Date Columns

```python
# Parse multiple columns
df = pd.read_csv(filename, parse_dates=['start_date', 'end_date'])

# Combine columns into single datetime
df = pd.read_csv(filename, parse_dates={'datetime': ['date', 'time']})
```

## strptime vs strftime

Understanding the difference between parsing and formatting:

### strptime (String Parse Time)

**String → Datetime Object**

```python
from datetime import datetime

date_string = "2024-01-15 14:30:00"
format_string = "%Y-%m-%d %H:%M:%S"

# Parse string to datetime
dt = datetime.strptime(date_string, format_string)
print(dt)  # 2024-01-15 14:30:00
print(type(dt))  # <class 'datetime.datetime'>
```

### strftime (String From Time)

**Datetime Object → String**

```python
from datetime import datetime

dt = datetime(2024, 1, 15, 14, 30, 0)

# Format datetime to string
date_string = dt.strftime("%B %d, %Y at %I:%M %p")
print(date_string)  # January 15, 2024 at 02:30 PM
```

### In pandas

```python
# Parsing (strptime equivalent)
s = pd.Series(['2024-01-15', '2024-01-16'])
dates = pd.to_datetime(s, format='%Y-%m-%d')

# Formatting (strftime)
formatted = dates.dt.strftime('%B %d, %Y')
print(formatted)
# January 15, 2024
# January 16, 2024
```

## Timezone-Aware Parsing

### Parsing with Timezone

```python
# String with timezone
s = pd.Series(['2024-01-15 12:00:00+00:00', '2024-01-15 07:00:00-05:00'])
dates = pd.to_datetime(s)
print(dates)
```

### Adding Timezone After Parsing

```python
# Parse first (naive)
dates = pd.to_datetime(['2024-01-15', '2024-01-16'])

# Then localize
dates_utc = dates.tz_localize('UTC')
print(dates_utc)
```

## Performance Considerations

### Use format Parameter

```python
import time

s = pd.Series(['01/15/2024'] * 100000)

# Without format (slower)
start = time.time()
pd.to_datetime(s)
print(f"Without format: {time.time() - start:.3f}s")

# With format (faster)
start = time.time()
pd.to_datetime(s, format='%m/%d/%Y')
print(f"With format: {time.time() - start:.3f}s")
```

### infer_datetime_format (deprecated)

In older pandas versions, `infer_datetime_format=True` could speed up parsing. This is now the default behavior and the parameter is deprecated.

## Practical Examples

### Financial Data

```python
# Stock data with various date formats
df = pd.DataFrame({
    'date_str': ['2024-01-15', '2024-01-16', '2024-01-17'],
    'close': [150.0, 151.5, 149.8]
})

# Parse and set as index
df['date'] = pd.to_datetime(df['date_str'])
df = df.set_index('date').drop('date_str', axis=1)
print(df)
```

### Mixed Date Formats

```python
# Handle mixed formats with errors='coerce'
mixed_dates = pd.Series([
    '2024-01-15',
    '01/16/2024',
    'January 17, 2024',
    'invalid'
])

dates = pd.to_datetime(mixed_dates, errors='coerce')
print(dates)
```

### Creating DatetimeIndex for Time Series

```python
# Create proper time series
prices = pd.Series(
    [100, 101, 102, 103, 104],
    index=pd.to_datetime(['2024-01-15', '2024-01-16', '2024-01-17', 
                          '2024-01-18', '2024-01-19']),
    name='price'
)

# Now can use time series operations
print(prices['2024-01-16':'2024-01-18'])  # Date slicing
print(prices.resample('2D').mean())        # Resampling
```

## Summary

| Task | Method |
|------|--------|
| Parse strings to datetime | `pd.to_datetime()` |
| Parse during CSV read | `parse_dates` parameter |
| Format datetime to string | `dt.strftime()` |
| Handle invalid dates | `errors='coerce'` |
| Parse Unix timestamps | `unit='s'` parameter |
| Specify date format | `format` parameter |


---

## Exercises

**Exercise 1.** Write code that converts a string column to datetime using `pd.to_datetime()`. Handle a custom format like `'15-Mar-2024'`.

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

**Exercise 2.** Explain the `format` parameter in `pd.to_datetime()`. Why is specifying the format faster than letting Pandas infer it?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that handles parsing errors using `errors='coerce'` in `pd.to_datetime()`. Show what happens to unparseable values.

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

**Exercise 4.** Create a DataFrame with a date string column and set it as the index after converting to datetime.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
