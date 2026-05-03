# timedelta Arithmetic

`timedelta` represents a duration and enables arithmetic operations on dates and times.

!!! tip "Mental Model"
    A `timedelta` is a ruler on the timeline — it measures the gap between two points in time. Add a `timedelta` to a `datetime` to move forward, subtract to move backward, and subtract two `datetime` objects to get the `timedelta` between them. Internally it stores only days, seconds, and microseconds, normalizing everything else into those three fields.

## Creating and Using timedelta

Create timedelta objects to represent durations.

```python
from datetime import datetime, timedelta

# Create timedelta
delta = timedelta(days=5, hours=2, minutes=30)
print(f"Delta: {delta}")

# Access components
print(f"Days: {delta.days}, Seconds: {delta.seconds}")

# Arithmetic with dates
today = datetime.now()
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(weeks=1)

print(f"Today: {today.date()}")
print(f"Tomorrow: {tomorrow.date()}")
print(f"Next week: {next_week.date()}")
```

```
Delta: 5 days, 2:30:00
Days: 5, Seconds: 9000
Today: 2026-02-12
Tomorrow: 2026-02-13
Next week: 2026-02-19
```

## Date Differences

Calculate the duration between two dates.

```python
from datetime import date

start = date(2024, 1, 1)
end = date(2024, 12, 31)

difference = end - start
print(f"Days between: {difference.days}")

# Calculate age
from datetime import date
birth_date = date(1990, 5, 15)
today = date.today()
age_delta = today - birth_date
age_years = age_delta.days // 365
print(f"Age (approximate): {age_years} years")
```

```
Days between: 364
Age (approximate): 35 years
```

---

## Exercises

**Exercise 1.**
Write a function `total_hours` that takes a `timedelta` object and returns the total number of hours as a float (including fractional hours from minutes and seconds). For example, `total_hours(timedelta(days=1, hours=6, minutes=30))` should return `30.5`.

??? success "Solution to Exercise 1"

    ```python
    from datetime import timedelta

    def total_hours(delta):
        return delta.total_seconds() / 3600

    # Test
    print(total_hours(timedelta(days=1, hours=6, minutes=30)))
    # 30.5
    print(total_hours(timedelta(hours=2, minutes=15)))
    # 2.25
    ```

---

**Exercise 2.**
Write a function `add_business_days` that takes a `date` and an integer `n`, and returns the date that is `n` business days (Monday-Friday) later. For example, adding 3 business days to Friday 2024-12-20 should return Wednesday 2024-12-25.

??? success "Solution to Exercise 2"

    ```python
    from datetime import date, timedelta

    def add_business_days(start_date, n):
        current = start_date
        added = 0
        while added < n:
            current += timedelta(days=1)
            if current.weekday() < 5:  # Monday-Friday
                added += 1
        return current

    # Test
    # Friday Dec 20 + 3 business days = Wed Dec 25
    print(add_business_days(date(2024, 12, 20), 3))
    # 2024-12-25
    print(add_business_days(date(2024, 12, 20), 5))
    # 2024-12-27
    ```

---

**Exercise 3.**
Write a function `format_duration` that takes a `timedelta` and returns a human-readable string like `"2 days, 3 hours, 15 minutes"`. Omit components that are zero. For example, `format_duration(timedelta(hours=5))` should return `"5 hours"`.

??? success "Solution to Exercise 3"

    ```python
    from datetime import timedelta

    def format_duration(delta):
        total_seconds = int(delta.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60

        parts = []
        if days:
            parts.append(f"{days} day{'s' if days != 1 else ''}")
        if hours:
            parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
        if minutes:
            parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")

        return ", ".join(parts) if parts else "0 minutes"

    # Test
    print(format_duration(timedelta(days=2, hours=3, minutes=15)))
    # 2 days, 3 hours, 15 minutes
    print(format_duration(timedelta(hours=5)))
    # 5 hours
    print(format_duration(timedelta(minutes=1)))
    # 1 minute
    ```
