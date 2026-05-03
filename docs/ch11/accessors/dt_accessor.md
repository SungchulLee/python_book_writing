# Datetime Accessor (dt)

The `dt` accessor in pandas provides vectorized datetime operations on Series containing datetime values. This allows you to extract date components, perform datetime arithmetic, and format dates without explicit loops.

!!! tip "Mental Model"
    Picture each datetime value as a clock face with year, month, day, hour dials. The `.dt` accessor lets you read any dial across an entire column at once -- no loop needed. It turns one column of timestamps into many columns of components, all in a single vectorized call.

## Overview

```python
import pandas as pd

dates = pd.Series(pd.date_range('2024-01-01', periods=5))

# Access datetime methods via .dt accessor
print(dates.dt.year)
```

```
0    2024
1    2024
2    2024
3    2024
4    2024
dtype: int32
```

## Prerequisites

The `dt` accessor requires datetime-like data. Convert strings to datetime first:

```python
# String column
s = pd.Series(['2024-01-01', '2024-01-02', '2024-01-03'])
print(s.dtype)  # object

# Convert to datetime
s = pd.to_datetime(s)
print(s.dtype)  # datetime64[ns]

# Now dt accessor works
print(s.dt.day)  # 1, 2, 3
```

## Extracting Date Components

### Year, Month, Day

```python
dates = pd.Series(pd.date_range('2024-03-15', periods=3))

print(dates.dt.year)   # 2024, 2024, 2024
print(dates.dt.month)  # 3, 3, 3
print(dates.dt.day)    # 15, 16, 17
```

### Quarter and Week

```python
dates = pd.Series(pd.to_datetime(['2024-01-15', '2024-04-15', '2024-07-15', '2024-10-15']))

print(dates.dt.quarter)      # 1, 2, 3, 4
print(dates.dt.isocalendar().week)  # ISO week number
```

### Day of Week

```python
dates = pd.Series(pd.date_range('2024-01-01', periods=7))

print(dates.dt.dayofweek)    # 0=Monday, 6=Sunday
print(dates.dt.day_name())   # Monday, Tuesday, ...
print(dates.dt.weekday)      # Same as dayofweek
```

### Day of Year

```python
dates = pd.Series(pd.to_datetime(['2024-01-01', '2024-06-15', '2024-12-31']))
print(dates.dt.dayofyear)  # 1, 167, 366
```

## Extracting Time Components

### Hour, Minute, Second

```python
times = pd.Series(pd.to_datetime(['2024-01-01 09:30:45', '2024-01-01 14:15:30']))

print(times.dt.hour)        # 9, 14
print(times.dt.minute)      # 30, 15
print(times.dt.second)      # 45, 30
print(times.dt.microsecond) # 0, 0
print(times.dt.nanosecond)  # 0, 0
```

### Time Component

Extract just the time portion:

```python
times = pd.Series(pd.to_datetime(['2024-01-01 09:30:45', '2024-01-01 14:15:30']))
print(times.dt.time)
```

```
0    09:30:45
1    14:15:30
dtype: object
```

### Date Component

Extract just the date portion:

```python
print(times.dt.date)
```

```
0    2024-01-01
1    2024-01-01
dtype: object
```

## Boolean Properties

### Checking Date Characteristics

```python
dates = pd.Series(pd.to_datetime([
    '2024-01-01', '2024-01-31', '2024-02-29', '2024-12-31'
]))

print(dates.dt.is_month_start)  # True, False, False, False
print(dates.dt.is_month_end)    # False, True, False, True
print(dates.dt.is_quarter_start) # True, False, False, False
print(dates.dt.is_quarter_end)   # False, False, False, True
print(dates.dt.is_year_start)    # True, False, False, False
print(dates.dt.is_year_end)      # False, False, False, True
print(dates.dt.is_leap_year)     # True, True, True, True (2024 is leap year)
```

## Formatting Dates

### strftime()

Format datetime to string using format codes.

```python
dates = pd.Series(pd.date_range('2024-01-15', periods=3))

# Various formats
print(dates.dt.strftime('%Y-%m-%d'))    # 2024-01-15, 2024-01-16, ...
print(dates.dt.strftime('%d/%m/%Y'))    # 15/01/2024, 16/01/2024, ...
print(dates.dt.strftime('%B %d, %Y'))   # January 15, 2024, ...
print(dates.dt.strftime('%A'))          # Monday, Tuesday, ...
```

### Common Format Codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | Year (4-digit) | 2024 |
| `%y` | Year (2-digit) | 24 |
| `%m` | Month (zero-padded) | 01-12 |
| `%B` | Month name (full) | January |
| `%b` | Month name (abbr) | Jan |
| `%d` | Day (zero-padded) | 01-31 |
| `%H` | Hour (24-hour) | 00-23 |
| `%I` | Hour (12-hour) | 01-12 |
| `%M` | Minute | 00-59 |
| `%S` | Second | 00-59 |
| `%A` | Weekday (full) | Monday |
| `%a` | Weekday (abbr) | Mon |
| `%p` | AM/PM | AM, PM |

## Rounding Operations

### floor(), ceil(), round()

```python
times = pd.Series(pd.to_datetime([
    '2024-01-15 09:37:45',
    '2024-01-15 14:22:30'
]))

# Round to nearest hour
print(times.dt.round('H'))
# 2024-01-15 10:00:00, 2024-01-15 14:00:00

# Floor to hour
print(times.dt.floor('H'))
# 2024-01-15 09:00:00, 2024-01-15 14:00:00

# Ceil to hour
print(times.dt.ceil('H'))
# 2024-01-15 10:00:00, 2024-01-15 15:00:00
```

### Common Frequency Strings

| String | Meaning |
|--------|---------|
| `'D'` | Day |
| `'H'` | Hour |
| `'T'` or `'min'` | Minute |
| `'S'` | Second |
| `'W'` | Week |
| `'M'` | Month end |
| `'MS'` | Month start |
| `'Q'` | Quarter end |

## Timezone Operations

### tz_localize()

Assign timezone to naive datetime.

```python
dates = pd.Series(pd.date_range('2024-01-15', periods=3))

# Localize to UTC
dates_utc = dates.dt.tz_localize('UTC')
print(dates_utc)
```

### tz_convert()

Convert between timezones.

```python
dates_utc = pd.Series(pd.date_range('2024-01-15', periods=3, tz='UTC'))

# Convert to US Eastern
dates_eastern = dates_utc.dt.tz_convert('US/Eastern')
print(dates_eastern)
```

### tz

Access timezone information.

```python
dates = pd.Series(pd.date_range('2024-01-15', periods=3, tz='US/Eastern'))
print(dates.dt.tz)  # US/Eastern
```

## Normalization

### normalize()

Set time component to midnight.

```python
times = pd.Series(pd.to_datetime([
    '2024-01-15 09:30:00',
    '2024-01-15 14:45:00'
]))

print(times.dt.normalize())
# 2024-01-15, 2024-01-15 (at midnight)
```

## Practical Examples

### Filtering by Date Components

```python
# Create sample data
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=100, freq='D'),
    'sales': range(100)
})

# Filter weekends
weekends = df[df['date'].dt.dayofweek >= 5]
print(f"Weekend days: {len(weekends)}")

# Filter specific month
january = df[df['date'].dt.month == 1]

# Filter Q1
q1 = df[df['date'].dt.quarter == 1]
```

### Grouping by Time Period

```python
# Daily sales data
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=365, freq='D'),
    'sales': range(365)
})

# Monthly totals
monthly = df.groupby(df['date'].dt.month)['sales'].sum()

# Day of week analysis
dow_avg = df.groupby(df['date'].dt.dayofweek)['sales'].mean()
dow_avg.index = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
print(dow_avg)
```

### Financial Example: Trading Days

```python
import pandas as pd
import numpy as np

# Stock price data
dates = pd.bdate_range('2024-01-01', '2024-03-31')  # Business days only
prices = pd.DataFrame({
    'date': dates,
    'close': 100 + np.cumsum(np.random.randn(len(dates)))
})

# Extract date features
prices['year'] = prices['date'].dt.year
prices['month'] = prices['date'].dt.month
prices['day_name'] = prices['date'].dt.day_name()
prices['is_month_end'] = prices['date'].dt.is_month_end

# Month-end prices
month_end_prices = prices[prices['is_month_end']]
print(month_end_prices[['date', 'close']])
```

### Creating Date Features for Analysis

```python
df = pd.DataFrame({
    'transaction_date': pd.date_range('2023-01-01', periods=1000, freq='H')
})

# Extract multiple features at once
df['year'] = df['transaction_date'].dt.year
df['month'] = df['transaction_date'].dt.month
df['day'] = df['transaction_date'].dt.day
df['hour'] = df['transaction_date'].dt.hour
df['dayofweek'] = df['transaction_date'].dt.dayofweek
df['is_weekend'] = df['transaction_date'].dt.dayofweek >= 5
df['quarter'] = df['transaction_date'].dt.quarter

print(df.head(10))
```

## Timedelta Operations

For TimedeltaIndex or timedelta64 dtype, similar accessor methods are available:

```python
# Calculate time differences
df = pd.DataFrame({
    'start': pd.to_datetime(['2024-01-01 09:00', '2024-01-02 10:30']),
    'end': pd.to_datetime(['2024-01-01 17:30', '2024-01-02 18:00'])
})

df['duration'] = df['end'] - df['start']

# Access timedelta components
print(df['duration'].dt.total_seconds())  # Total seconds
print(df['duration'].dt.components)       # Days, hours, minutes, etc.
```

## Summary of Key Properties

| Property | Returns | Example |
|----------|---------|---------|
| `dt.year` | Year | 2024 |
| `dt.month` | Month (1-12) | 1 |
| `dt.day` | Day (1-31) | 15 |
| `dt.hour` | Hour (0-23) | 14 |
| `dt.minute` | Minute (0-59) | 30 |
| `dt.second` | Second (0-59) | 45 |
| `dt.dayofweek` | Day of week (0=Mon) | 0 |
| `dt.dayofyear` | Day of year (1-366) | 15 |
| `dt.quarter` | Quarter (1-4) | 1 |
| `dt.is_month_end` | Boolean | True/False |
| `dt.date` | Date only | 2024-01-15 |
| `dt.time` | Time only | 14:30:45 |

---

## Exercises

**Exercise 1.**
Create a DataFrame with a `'date'` column containing 90 consecutive dates starting from `'2024-01-01'`. Add a new column `'day_name'` using the `.dt.day_name()` method. Then count how many rows fall on each day of the week using `value_counts()`.

??? success "Solution to Exercise 1"
    Use `.dt.day_name()` and `value_counts()`.

        import pandas as pd

        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=90)
        })
        df['day_name'] = df['date'].dt.day_name()
        print(df['day_name'].value_counts())

---

**Exercise 2.**
Given a Series of datetime values spanning multiple years, use the `.dt` accessor to extract the year and quarter. Create a new string column in the format `'2024-Q1'` by combining these extracted components.

??? success "Solution to Exercise 2"
    Combine `.dt.year` and `.dt.quarter` with string formatting.

        import pandas as pd

        dates = pd.Series(pd.date_range('2023-01-15', periods=8, freq='2ME'))
        year_quarter = dates.dt.year.astype(str) + '-Q' + dates.dt.quarter.astype(str)
        print(year_quarter)

---

**Exercise 3.**
Create a Series of timestamps at irregular intervals. Use `.dt.floor('h')` to round all timestamps down to the nearest hour. Then verify that all resulting timestamps have zero minutes and seconds.

??? success "Solution to Exercise 3"
    Use `.dt.floor('h')` and check minutes/seconds are zero.

        import pandas as pd

        timestamps = pd.Series(pd.to_datetime([
            '2024-01-01 10:23:45',
            '2024-01-01 14:59:01',
            '2024-01-01 08:00:30'
        ]))
        floored = timestamps.dt.floor('h')
        print(floored)
        assert (floored.dt.minute == 0).all()
        assert (floored.dt.second == 0).all()
        print("All timestamps rounded to the hour.")
