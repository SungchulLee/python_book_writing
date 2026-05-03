# Formatting (strftime) and Parsing (strptime)

`strftime()` formats datetime objects as strings, while `strptime()` parses strings into datetime objects.

!!! tip "Mental Model"
    Think of `strftime` as "string **f**rom time" — it turns a datetime object into a human-readable string. `strptime` is "string **p**arse time" — it reads a string and builds a datetime object. The same format codes (`%Y`, `%m`, `%d`, etc.) drive both directions, so learning the codes once covers formatting and parsing alike.

## strftime - Format Datetime to String

Use format codes to create human-readable date strings.

```python
from datetime import datetime

now = datetime(2024, 12, 25, 14, 30, 45)

# Common format codes
formats = {
    "%Y-%m-%d": now.strftime("%Y-%m-%d"),
    "%d/%m/%Y": now.strftime("%d/%m/%Y"),
    "%A, %B %d, %Y": now.strftime("%A, %B %d, %Y"),
    "%I:%M %p": now.strftime("%I:%M %p"),
    "%H:%M:%S": now.strftime("%H:%M:%S"),
}

for pattern, result in formats.items():
    print(f"{pattern}: {result}")
```

```
%Y-%m-%d: 2024-12-25
%d/%m/%Y: 25/12/2024
%A, %B %d, %Y: Wednesday, December 25, 2024
%I:%M %p: 02:30 PM
%H:%M:%S: 14:30:45
```

## strptime - Parse String to Datetime

Parse date strings using format codes.

```python
from datetime import datetime

# Parse various date formats
dates = [
    ("2024-12-25", "%Y-%m-%d"),
    ("25/12/2024", "%d/%m/%Y"),
    ("December 25, 2024", "%B %d, %Y"),
    ("02:30 PM", "%I:%M %p"),
]

for date_str, fmt in dates:
    parsed = datetime.strptime(date_str, fmt)
    print(f"'{date_str}' -> {parsed}")
```

```
'2024-12-25' -> 2024-12-25 00:00:00
'25/12/2024' -> 2024-12-25 00:00:00
'December 25, 2024' -> 2024-12-25 00:00:00
'02:30 PM' -> 1900-01-01 14:30:00
```

---

## Exercises

**Exercise 1.**
Write a function `reformat_date` that takes a date string in `"MM/DD/YYYY"` format and returns it in `"YYYY-MM-DD"` format. For example, `reformat_date("12/25/2024")` should return `"2024-12-25"`.

??? success "Solution to Exercise 1"

    ```python
    from datetime import datetime

    def reformat_date(date_str):
        dt = datetime.strptime(date_str, "%m/%d/%Y")
        return dt.strftime("%Y-%m-%d")

    # Test
    print(reformat_date("12/25/2024"))  # 2024-12-25
    print(reformat_date("01/01/2025"))  # 2025-01-01
    ```

---

**Exercise 2.**
Write a function `format_log_timestamp` that takes a `datetime` object and returns a string in the format `"[YYYY-MM-DD HH:MM:SS]"` suitable for log files. For example, `format_log_timestamp(datetime(2024, 12, 25, 14, 30, 45))` should return `"[2024-12-25 14:30:45]"`.

??? success "Solution to Exercise 2"

    ```python
    from datetime import datetime

    def format_log_timestamp(dt):
        return dt.strftime("[%Y-%m-%d %H:%M:%S]")

    # Test
    dt = datetime(2024, 12, 25, 14, 30, 45)
    print(format_log_timestamp(dt))  # [2024-12-25 14:30:45]
    print(format_log_timestamp(datetime.now()))
    ```

---

**Exercise 3.**
Write a function `parse_and_add_days` that takes a date string in `"%B %d, %Y"` format and an integer number of days, and returns the resulting date as a string in `"%Y-%m-%d"` format. For example, `parse_and_add_days("December 25, 2024", 7)` should return `"2025-01-01"`.

??? success "Solution to Exercise 3"

    ```python
    from datetime import datetime, timedelta

    def parse_and_add_days(date_str, days):
        dt = datetime.strptime(date_str, "%B %d, %Y")
        result = dt + timedelta(days=days)
        return result.strftime("%Y-%m-%d")

    # Test
    print(parse_and_add_days("December 25, 2024", 7))
    # 2025-01-01
    print(parse_and_add_days("February 28, 2024", 1))
    # 2024-02-29 (leap year)
    ```
