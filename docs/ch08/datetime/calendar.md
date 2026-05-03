# calendar Module

The `calendar` module provides functions for calendar-related operations and generating formatted calendars.

!!! tip "Mental Model"
    The `calendar` module is a virtual wall calendar you can query programmatically. Ask it which day of the week a date falls on, whether a year is a leap year, or print an entire month grid. It handles the tedious arithmetic of varying month lengths and weekday offsets so you don't have to.

## Basic Calendar Operations

Get calendar information for dates.

```python
import calendar
from datetime import date

# Day of week for a specific date
d = date(2024, 12, 25)
day_name = calendar.day_name[d.weekday()]
print(f"2024-12-25 is a {day_name}")

# Check if leap year
print(f"2024 is leap year: {calendar.isleap(2024)}")
print(f"2025 is leap year: {calendar.isleap(2025)}")

# Days in month
days = calendar.monthrange(2024, 2)
print(f"Feb 2024 has {days[1]} days")
```

```
2024-12-25 is a Wednesday
2024 is leap year: True
2025 is leap year: False
Feb 2024 has 29 days
```

## Print Calendars

Generate and display formatted calendars.

```python
import calendar

# Print a month
print("December 2024:")
print(calendar.month(2024, 12))

# Print a year (just first 3 months for brevity)
cal = calendar.TextCalendar()
for month in range(1, 4):
    print(calendar.month(2024, month))
```

```
December 2024:
   December 2024
Mo Tu We Th Fr Sa Su
                   1
 2  3  4  5  6  7  8
 9 10 11 12 13 14 15
16 17 18 19 20 21 22
23 24 25 26 27 28 29
30 31
```

---

## Exercises

**Exercise 1.**
Write a function `count_leap_years` that takes a start year and an end year (inclusive) and returns the number of leap years in that range. Use `calendar.isleap()`. For example, `count_leap_years(2000, 2024)` should return `7`.

??? success "Solution to Exercise 1"

    ```python
    import calendar

    def count_leap_years(start, end):
        return sum(1 for year in range(start, end + 1)
                   if calendar.isleap(year))

    # Test
    print(count_leap_years(2000, 2024))  # 7
    print(count_leap_years(1900, 1900))  # 0 (1900 is not a leap year)
    print(count_leap_years(2000, 2000))  # 1
    ```

---

**Exercise 2.**
Write a function `fridays_in_month` that takes a year and month and returns the number of Fridays in that month. Use `calendar.monthcalendar()` to get the weeks. For example, `fridays_in_month(2024, 11)` should return `5`.

??? success "Solution to Exercise 2"

    ```python
    import calendar

    def fridays_in_month(year, month):
        count = 0
        for week in calendar.monthcalendar(year, month):
            if week[calendar.FRIDAY] != 0:
                count += 1
        return count

    # Test
    print(fridays_in_month(2024, 11))  # 5
    print(fridays_in_month(2024, 12))  # 4
    ```

---

**Exercise 3.**
Write a function `last_day_of_month` that takes a year and month and returns the last day of that month as a `date` object. Use `calendar.monthrange()`. For example, `last_day_of_month(2024, 2)` should return `date(2024, 2, 29)`.

??? success "Solution to Exercise 3"

    ```python
    import calendar
    from datetime import date

    def last_day_of_month(year, month):
        _, last_day = calendar.monthrange(year, month)
        return date(year, month, last_day)

    # Test
    print(last_day_of_month(2024, 2))   # 2024-02-29
    print(last_day_of_month(2025, 2))   # 2025-02-28
    print(last_day_of_month(2024, 12))  # 2024-12-31
    ```
