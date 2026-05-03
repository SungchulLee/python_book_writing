# date, time, datetime Objects

These three classes represent dates, times, and the combination of both, forming the foundation of datetime operations.

!!! tip "Mental Model"
    Think of `date` as a calendar page (year-month-day), `time` as a clock face (hour-minute-second), and `datetime` as both stapled together. Most real-world timestamps need `datetime` because events happen at a specific date *and* time. The split into three classes lets you work with whichever dimension matters for your task.

## date Class

The date class represents a calendar date (year, month, day).

```python
from datetime import date

# Today's date
today = date.today()
print(f"Today: {today}")

# Create specific date
d = date(2024, 12, 25)
print(f"Date: {d}")

# Access components
print(f"Year: {d.year}, Month: {d.month}, Day: {d.day}")

# Day of week (0=Monday)
print(f"Weekday: {d.weekday()}")
print(f"ISO Weekday: {d.isoweekday()}")
```

```
Today: 2026-02-12
Date: 2024-12-25
Year: 2024, Month: 12, Day: 25
Weekday: 2
ISO Weekday: 3
```

## time Class

The time class represents time (hour, minute, second, microsecond).

```python
from datetime import time

# Create time
t = time(14, 30, 45)
print(f"Time: {t}")

# Access components
print(f"Hour: {t.hour}, Minute: {t.minute}, Second: {t.second}")

# Midnight, noon
midnight = time(0, 0, 0)
noon = time(12, 0, 0)
print(f"Midnight: {midnight}, Noon: {noon}")
```

```
Time: 14:30:45
Hour: 14, Minute: 30, Second: 45
Midnight: 00:00:00, Noon: 12:00:00
```

## datetime Class

The datetime class combines date and time.

```python
from datetime import datetime

# Current datetime
now = datetime.now()
print(f"Now: {now}")

# Create specific datetime
dt = datetime(2024, 12, 25, 14, 30, 0)
print(f"DateTime: {dt}")

# Combine date and time
from datetime import date, time
d = date(2024, 12, 25)
t = time(14, 30)
combined = datetime.combine(d, t)
print(f"Combined: {combined}")
```

```
Now: 2026-02-12 14:30:45.123456
DateTime: 2024-12-25 14:30:00
Combined: 2024-12-25 14:30:00
```

---

## Exercises

**Exercise 1.**
Write a function `days_until_birthday` that takes a `date` object representing a birthday and returns the number of days until the next occurrence of that birthday (from today). If the birthday is today, return `0`. For example, if today is 2026-02-12 and the birthday is `date(1990, 7, 4)`, it should return the number of days until 2026-07-04.

??? success "Solution to Exercise 1"

    ```python
    from datetime import date

    def days_until_birthday(birthday):
        today = date.today()
        next_birthday = birthday.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    # Test
    bday = date(1990, 7, 4)
    print(f"Days until birthday: {days_until_birthday(bday)}")
    # Depends on current date
    ```

---

**Exercise 2.**
Write a function `is_business_hours` that takes a `datetime` object and returns `True` if it falls on a weekday (Monday-Friday) between 9:00 AM and 5:00 PM (inclusive of 9:00, exclusive of 17:00). For example, `datetime(2024, 12, 25, 10, 30)` (a Wednesday) should return `True`.

??? success "Solution to Exercise 2"

    ```python
    from datetime import datetime, time

    def is_business_hours(dt):
        # Monday=0, Friday=4
        if dt.weekday() > 4:
            return False
        start = time(9, 0)
        end = time(17, 0)
        return start <= dt.time() < end

    # Test
    print(is_business_hours(datetime(2024, 12, 25, 10, 30)))  # True (Wed)
    print(is_business_hours(datetime(2024, 12, 25, 18, 0)))   # False (after 5pm)
    print(is_business_hours(datetime(2024, 12, 22, 10, 0)))   # False (Sunday)
    ```

---

**Exercise 3.**
Write a function `combine_and_format` that takes a `date`, a `time`, and a format string, combines the date and time into a `datetime`, and returns the formatted string. For example, `combine_and_format(date(2024, 12, 25), time(14, 30), "%B %d, %Y at %I:%M %p")` should return `"December 25, 2024 at 02:30 PM"`.

??? success "Solution to Exercise 3"

    ```python
    from datetime import date, time, datetime

    def combine_and_format(d, t, fmt):
        dt = datetime.combine(d, t)
        return dt.strftime(fmt)

    # Test
    result = combine_and_format(
        date(2024, 12, 25),
        time(14, 30),
        "%B %d, %Y at %I:%M %p"
    )
    print(result)  # December 25, 2024 at 02:30 PM
    ```
