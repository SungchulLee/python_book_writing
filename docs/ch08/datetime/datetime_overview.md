# datetime Overview

The `datetime` module provides classes for manipulating dates and times, including date, time, datetime, timedelta, and timezone support.

!!! tip "Mental Model"
    The `datetime` module gives you a small family of types: points in time (`date`, `time`, `datetime`) and durations between them (`timedelta`). You create a point, do arithmetic with durations, and format results as strings. Nearly all date/time work in Python starts here before reaching for third-party libraries.

## Core Classes

The datetime module provides several core classes for date and time manipulation.

```python
from datetime import date, time, datetime, timedelta

# Current date
today = date.today()
print(f"Today: {today}")

# Create specific date
birthday = date(1990, 5, 15)
print(f"Birthday: {birthday}")

# Current time
now = datetime.now()
print(f"Now: {now}")
```

```
Today: 2026-02-12
Birthday: 1990-05-15
Now: 2026-02-12 12:34:56.789123
```

## Parsing and Formatting

Convert between datetime objects and strings.

```python
from datetime import datetime

# Parse string to datetime
date_str = "2024-12-25"
parsed = datetime.strptime(date_str, "%Y-%m-%d")
print(f"Parsed: {parsed}")

# Format datetime to string
formatted = parsed.strftime("%A, %B %d, %Y")
print(f"Formatted: {formatted}")
```

```
Parsed: 2024-12-25 00:00:00
Formatted: Wednesday, December 25, 2024
```

---

## Exercises

**Exercise 1.**
Write a function `days_in_year` that takes a year (int) and returns the total number of days in that year by computing the difference between January 1 of that year and January 1 of the next year. For example, `days_in_year(2024)` should return `366`.

??? success "Solution to Exercise 1"

    ```python
    from datetime import date

    def days_in_year(year):
        start = date(year, 1, 1)
        end = date(year + 1, 1, 1)
        return (end - start).days

    # Test
    print(days_in_year(2024))  # 366 (leap year)
    print(days_in_year(2025))  # 365
    ```

---

**Exercise 2.**
Write a function `parse_multiple_formats` that takes a date string and tries to parse it against a list of common formats (`"%Y-%m-%d"`, `"%d/%m/%Y"`, `"%B %d, %Y"`, `"%m-%d-%Y"`). Return the parsed `datetime` for the first format that succeeds, or `None` if none match.

??? success "Solution to Exercise 2"

    ```python
    from datetime import datetime

    def parse_multiple_formats(date_str):
        formats = ["%Y-%m-%d", "%d/%m/%Y", "%B %d, %Y", "%m-%d-%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    # Test
    print(parse_multiple_formats("2024-12-25"))
    # 2024-12-25 00:00:00
    print(parse_multiple_formats("25/12/2024"))
    # 2024-12-25 00:00:00
    print(parse_multiple_formats("December 25, 2024"))
    # 2024-12-25 00:00:00
    print(parse_multiple_formats("not a date"))
    # None
    ```

---

**Exercise 3.**
Write a function `weekday_name` that takes a date string in `"YYYY-MM-DD"` format and returns the full name of the day of the week (e.g., `"Monday"`). For example, `weekday_name("2024-12-25")` should return `"Wednesday"`.

??? success "Solution to Exercise 3"

    ```python
    from datetime import datetime

    def weekday_name(date_str):
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.strftime("%A")

    # Test
    print(weekday_name("2024-12-25"))  # Wednesday
    print(weekday_name("2024-01-01"))  # Monday
    ```
