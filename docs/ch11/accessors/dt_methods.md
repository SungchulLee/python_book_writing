# Datetime Methods Reference

Complete reference for all datetime methods and properties available through the pandas `dt` accessor.

!!! tip "Mental Model"
    Every datetime value is a structured object with nested fields -- year, month, day, hour, and so on. The `dt` methods are extractors and formatters that pull out or reshape these fields across an entire Series at once. If you can describe it on a calendar or a clock, `dt` has a property for it.

## Date Component Properties

| Property | Description | Return Type |
|----------|-------------|-------------|
| `dt.year` | Year | int |
| `dt.month` | Month (1-12) | int |
| `dt.day` | Day of month (1-31) | int |
| `dt.quarter` | Quarter (1-4) | int |
| `dt.dayofweek` | Day of week (0=Monday, 6=Sunday) | int |
| `dt.weekday` | Same as dayofweek | int |
| `dt.dayofyear` | Day of year (1-366) | int |
| `dt.days_in_month` | Number of days in month | int |

```python
import pandas as pd

dates = pd.Series(pd.date_range('2024-03-15', periods=3))

print(dates.dt.year)          # 2024, 2024, 2024
print(dates.dt.month)         # 3, 3, 3
print(dates.dt.day)           # 15, 16, 17
print(dates.dt.quarter)       # 1, 1, 1
print(dates.dt.dayofweek)     # 4, 5, 6 (Fri, Sat, Sun)
print(dates.dt.dayofyear)     # 75, 76, 77
print(dates.dt.days_in_month) # 31, 31, 31
```

## Time Component Properties

| Property | Description | Return Type |
|----------|-------------|-------------|
| `dt.hour` | Hour (0-23) | int |
| `dt.minute` | Minute (0-59) | int |
| `dt.second` | Second (0-59) | int |
| `dt.microsecond` | Microsecond (0-999999) | int |
| `dt.nanosecond` | Nanosecond (0-999999999) | int |

```python
times = pd.Series(pd.to_datetime(['2024-01-15 14:30:45.123456']))

print(times.dt.hour)        # 14
print(times.dt.minute)      # 30
print(times.dt.second)      # 45
print(times.dt.microsecond) # 123456
print(times.dt.nanosecond)  # 0
```

## Date/Time Extraction Properties

| Property | Description | Return Type |
|----------|-------------|-------------|
| `dt.date` | Date component | datetime.date |
| `dt.time` | Time component | datetime.time |

```python
times = pd.Series(pd.to_datetime(['2024-01-15 14:30:45']))

print(times.dt.date)  # 2024-01-15
print(times.dt.time)  # 14:30:45
```

## Name Methods

| Method | Description | Return Type |
|--------|-------------|-------------|
| `dt.day_name()` | Full day name | str |
| `dt.month_name()` | Full month name | str |

```python
dates = pd.Series(pd.date_range('2024-01-15', periods=3))

print(dates.dt.day_name())
# Monday, Tuesday, Wednesday

print(dates.dt.month_name())
# January, January, January

# With locale (if supported)
print(dates.dt.day_name(locale='de_DE'))
# Montag, Dienstag, Mittwoch
```

## Boolean Properties

| Property | Description |
|----------|-------------|
| `dt.is_month_start` | First day of month |
| `dt.is_month_end` | Last day of month |
| `dt.is_quarter_start` | First day of quarter |
| `dt.is_quarter_end` | Last day of quarter |
| `dt.is_year_start` | First day of year |
| `dt.is_year_end` | Last day of year |
| `dt.is_leap_year` | Is a leap year |

```python
dates = pd.Series(pd.to_datetime([
    '2024-01-01',  # Year start, Q1 start, month start
    '2024-03-31',  # Q1 end, month end
    '2024-06-15',  # Mid-quarter
    '2024-12-31'   # Year end, Q4 end, month end
]))

print(dates.dt.is_month_start)   # True, False, False, False
print(dates.dt.is_month_end)     # False, True, False, True
print(dates.dt.is_quarter_start) # True, False, False, False
print(dates.dt.is_quarter_end)   # False, True, False, True
print(dates.dt.is_year_start)    # True, False, False, False
print(dates.dt.is_year_end)      # False, False, False, True
print(dates.dt.is_leap_year)     # True, True, True, True
```

## Week Methods

| Method | Description |
|--------|-------------|
| `dt.isocalendar()` | Returns DataFrame with year, week, day |

```python
dates = pd.Series(pd.date_range('2024-01-01', periods=5))

iso = dates.dt.isocalendar()
print(iso)
#    year  week  day
# 0  2024     1    1
# 1  2024     1    2
# ...

# Access individual components
print(dates.dt.isocalendar().week)  # Week numbers
```

## Formatting Methods

### strftime(format)

Format datetime as string using format codes.

```python
dates = pd.Series(pd.date_range('2024-01-15', periods=3))

print(dates.dt.strftime('%Y-%m-%d'))
# 2024-01-15, 2024-01-16, 2024-01-17

print(dates.dt.strftime('%d/%m/%Y'))
# 15/01/2024, 16/01/2024, 17/01/2024

print(dates.dt.strftime('%B %d, %Y'))
# January 15, 2024, January 16, 2024, January 17, 2024

print(dates.dt.strftime('%A, %B %d'))
# Monday, January 15, Tuesday, January 16, Wednesday, January 17
```

### Format Code Reference

| Code | Description | Example |
|------|-------------|---------|
| `%Y` | 4-digit year | 2024 |
| `%y` | 2-digit year | 24 |
| `%m` | Month (01-12) | 01 |
| `%B` | Full month name | January |
| `%b` | Abbreviated month | Jan |
| `%d` | Day (01-31) | 15 |
| `%j` | Day of year (001-366) | 015 |
| `%H` | Hour 24-hour (00-23) | 14 |
| `%I` | Hour 12-hour (01-12) | 02 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |
| `%f` | Microsecond | 000000 |
| `%A` | Full weekday | Monday |
| `%a` | Abbreviated weekday | Mon |
| `%w` | Weekday number (0=Sunday) | 1 |
| `%p` | AM/PM | PM |
| `%Z` | Timezone name | UTC |
| `%z` | UTC offset | +0000 |

## Rounding Methods

| Method | Description |
|--------|-------------|
| `dt.round(freq)` | Round to nearest frequency |
| `dt.floor(freq)` | Round down |
| `dt.ceil(freq)` | Round up |

```python
times = pd.Series(pd.to_datetime([
    '2024-01-15 09:37:45',
    '2024-01-15 14:22:30',
    '2024-01-15 18:45:15'
]))

# Round to hour
print(times.dt.round('H'))
# 10:00, 14:00, 19:00

# Floor to hour
print(times.dt.floor('H'))
# 09:00, 14:00, 18:00

# Ceil to hour
print(times.dt.ceil('H'))
# 10:00, 15:00, 19:00

# Round to 15 minutes
print(times.dt.round('15T'))
# 09:30, 14:30, 18:45

# Round to day
print(times.dt.round('D'))
# 2024-01-16, 2024-01-15, 2024-01-16
```

### Frequency Strings

| String | Description |
|--------|-------------|
| `'D'` | Day |
| `'H'` | Hour |
| `'T'` or `'min'` | Minute |
| `'S'` | Second |
| `'L'` or `'ms'` | Millisecond |
| `'U'` or `'us'` | Microsecond |
| `'N'` | Nanosecond |
| `'W'` | Week |
| `'M'` | Month end |
| `'MS'` | Month start |
| `'Q'` | Quarter end |
| `'QS'` | Quarter start |
| `'A'` or `'Y'` | Year end |
| `'AS'` or `'YS'` | Year start |

## Timezone Methods

| Method | Description |
|--------|-------------|
| `dt.tz_localize(tz)` | Assign timezone to naive datetime |
| `dt.tz_convert(tz)` | Convert to different timezone |
| `dt.tz` | Get timezone (property) |

```python
# Create naive datetime
dates = pd.Series(pd.date_range('2024-01-15 12:00', periods=3, freq='H'))

# Localize to UTC
dates_utc = dates.dt.tz_localize('UTC')
print(dates_utc)
# 2024-01-15 12:00:00+00:00, ...

# Convert to US Eastern
dates_eastern = dates_utc.dt.tz_convert('US/Eastern')
print(dates_eastern)
# 2024-01-15 07:00:00-05:00, ...

# Get timezone
print(dates_utc.dt.tz)  # UTC
print(dates_eastern.dt.tz)  # US/Eastern
```

### Common Timezone Strings

| String | Description |
|--------|-------------|
| `'UTC'` | Coordinated Universal Time |
| `'US/Eastern'` | Eastern Time (US) |
| `'US/Pacific'` | Pacific Time (US) |
| `'US/Central'` | Central Time (US) |
| `'US/Mountain'` | Mountain Time (US) |
| `'Europe/London'` | UK Time |
| `'Europe/Paris'` | Central European Time |
| `'Europe/Berlin'` | Central European Time |
| `'Asia/Tokyo'` | Japan Time |
| `'Asia/Shanghai'` | China Time |
| `'Asia/Kolkata'` | India Time |
| `'Australia/Sydney'` | Australian Eastern Time |

## Normalization Method

### normalize()

Set time component to midnight.

```python
times = pd.Series(pd.to_datetime([
    '2024-01-15 09:30:00',
    '2024-01-15 14:45:00',
    '2024-01-16 23:59:59'
]))

print(times.dt.normalize())
# 2024-01-15, 2024-01-15, 2024-01-16 (all at 00:00:00)
```

## Timedelta Properties

For Series with timedelta64 dtype:

| Property | Description |
|----------|-------------|
| `dt.days` | Number of days |
| `dt.seconds` | Seconds (0-86399) |
| `dt.microseconds` | Microseconds (0-999999) |
| `dt.nanoseconds` | Nanoseconds (0-999999999) |
| `dt.total_seconds()` | Total duration in seconds |
| `dt.components` | DataFrame of components |

```python
# Create timedelta Series
durations = pd.Series([
    pd.Timedelta(days=1, hours=2, minutes=30),
    pd.Timedelta(hours=5, minutes=45),
    pd.Timedelta(days=2, seconds=3600)
])

print(durations.dt.days)           # 1, 0, 2
print(durations.dt.total_seconds())  # 95400.0, 20700.0, 176400.0
print(durations.dt.components)
#    days  hours  minutes  seconds  milliseconds  microseconds  nanoseconds
# 0     1      2       30        0             0             0            0
# 1     0      5       45        0             0             0            0
# 2     2      1        0        0             0             0            0
```

## Period Properties

For Series with Period dtype:

| Property | Description |
|----------|-------------|
| `dt.start_time` | Start of period |
| `dt.end_time` | End of period |
| `dt.freq` | Frequency of period |

```python
# Create period Series
periods = pd.Series(pd.period_range('2024-01', periods=3, freq='M'))

print(periods.dt.start_time)  # Start of each month
print(periods.dt.end_time)    # End of each month
print(periods.dt.freq)        # <MonthEnd>
```

## Method Summary

| Category | Methods/Properties |
|----------|-------------------|
| **Date Components** | `year`, `month`, `day`, `quarter`, `dayofweek`, `dayofyear` |
| **Time Components** | `hour`, `minute`, `second`, `microsecond`, `nanosecond` |
| **Extraction** | `date`, `time` |
| **Names** | `day_name()`, `month_name()` |
| **Boolean Checks** | `is_month_start`, `is_month_end`, `is_year_start`, `is_year_end`, `is_leap_year` |
| **Rounding** | `round()`, `floor()`, `ceil()` |
| **Timezone** | `tz_localize()`, `tz_convert()`, `tz` |
| **Formatting** | `strftime()` |
| **Normalization** | `normalize()` |
| **Week Info** | `isocalendar()` |

---

## Exercises

**Exercise 1.**
Create a Series of 12 monthly timestamps for the year 2024. Use `.dt.month_name()` to get the month names and `.dt.is_quarter_start` to identify which months are quarter starts.

??? success "Solution to Exercise 1"
    Use `pd.date_range` with monthly frequency.

        import pandas as pd

        months = pd.Series(pd.date_range('2024-01-01', periods=12, freq='MS'))
        print(months.dt.month_name())
        print("Quarter starts:")
        print(months[months.dt.is_quarter_start])

---

**Exercise 2.**
Given a Series of timestamps in UTC, use `.dt.tz_localize('UTC')` and then `.dt.tz_convert('US/Eastern')` to convert them to Eastern time. Print the resulting timestamps and confirm the timezone offset.

??? success "Solution to Exercise 2"
    Localize to UTC first, then convert to Eastern.

        import pandas as pd

        timestamps = pd.Series(pd.to_datetime([
            '2024-06-15 18:00:00',
            '2024-12-15 18:00:00'
        ]))
        utc = timestamps.dt.tz_localize('UTC')
        eastern = utc.dt.tz_convert('US/Eastern')
        print(eastern)

---

**Exercise 3.**
Create a Series of timestamps with different times of day. Use `.dt.strftime('%Y/%m/%d %I:%M %p')` to format them in 12-hour format with AM/PM. Then use `.dt.normalize()` to strip the time component and keep only dates.

??? success "Solution to Exercise 3"
    Format with `strftime` and normalize to midnight.

        import pandas as pd

        ts = pd.Series(pd.to_datetime([
            '2024-01-15 09:30:00',
            '2024-01-15 14:45:00',
            '2024-01-15 21:00:00'
        ]))
        formatted = ts.dt.strftime('%Y/%m/%d %I:%M %p')
        print("Formatted:\n", formatted)

        normalized = ts.dt.normalize()
        print("Normalized:\n", normalized)
