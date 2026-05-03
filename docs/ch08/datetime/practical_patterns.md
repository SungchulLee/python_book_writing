# Practical Patterns for datetime

Common patterns and best practices for working with dates and times in real-world applications.

!!! tip "Mental Model"
    Real-world datetime code revolves around a handful of recurring patterns: computing "time ago" labels, finding business-day boundaries, generating date ranges, and converting between timezones. Mastering these recipes means you rarely need to reinvent the wheel — most datetime tasks are a variation of one of these patterns.

## Human-Readable Relative Times

Display times relative to now (e.g., '2 hours ago').

```python
from datetime import datetime, timedelta

def time_ago(dt):
    now = datetime.now()
    delta = now - dt
    
    if delta.days > 0:
        return f"{delta.days} days ago"
    elif delta.seconds > 3600:
        return f"{delta.seconds // 3600} hours ago"
    elif delta.seconds > 60:
        return f"{delta.seconds // 60} minutes ago"
    else:
        return "just now"

past = datetime.now() - timedelta(hours=2)
print(time_ago(past))
```

```
2 hours ago
```

## Date Range Iteration

Iterate through a range of dates.

```python
from datetime import date, timedelta

def date_range(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)

start = date(2024, 12, 23)
end = date(2024, 12, 26)

for d in date_range(start, end):
    print(d)
```

```
2024-12-23
2024-12-24
2024-12-25
2024-12-26
```

## Scheduling and Cron-like Logic

Check if a task should run based on schedule.

```python
from datetime import datetime, timedelta

class Task:
    def __init__(self, name, interval_hours):
        self.name = name
        self.interval = timedelta(hours=interval_hours)
        self.last_run = None
    
    def should_run(self):
        if self.last_run is None:
            return True
        return datetime.now() >= self.last_run + self.interval
    
    def run(self):
        print(f"Running {self.name}")
        self.last_run = datetime.now()

task = Task("cleanup", 24)
print(f"Should run: {task.should_run()}")
task.run()
print(f"Should run again: {task.should_run()}")
```

```
Should run: True
Running cleanup
Should run again: False
```

---

## Exercises

**Exercise 1.**
Write an improved `time_ago` function that also handles weeks and months (approximate, 30 days). It should return strings like `"3 weeks ago"` or `"2 months ago"` for longer durations. Test it with various `timedelta` offsets.

??? success "Solution to Exercise 1"

    ```python
    from datetime import datetime, timedelta

    def time_ago(dt):
        now = datetime.now()
        delta = now - dt

        if delta.days >= 30:
            months = delta.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
        elif delta.days >= 7:
            weeks = delta.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        elif delta.days > 0:
            return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
        elif delta.seconds >= 3600:
            hours = delta.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif delta.seconds >= 60:
            minutes = delta.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "just now"

    # Test
    print(time_ago(datetime.now() - timedelta(days=45)))   # 1 month ago
    print(time_ago(datetime.now() - timedelta(days=14)))   # 2 weeks ago
    print(time_ago(datetime.now() - timedelta(hours=3)))   # 3 hours ago
    print(time_ago(datetime.now() - timedelta(seconds=30)))  # just now
    ```

---

**Exercise 2.**
Write a function `business_days_between` that takes two `date` objects and returns the number of business days (Monday-Friday) between them, exclusive of both endpoints. For example, between Monday 2024-12-23 and Friday 2024-12-27, there are 3 business days (Tue, Wed, Thu).

??? success "Solution to Exercise 2"

    ```python
    from datetime import date, timedelta

    def business_days_between(start, end):
        if start > end:
            start, end = end, start
        count = 0
        current = start + timedelta(days=1)
        while current < end:
            if current.weekday() < 5:  # Monday=0 to Friday=4
                count += 1
            current += timedelta(days=1)
        return count

    # Test
    # Mon Dec 23 to Fri Dec 27: Tue, Wed, Thu = 3
    print(business_days_between(date(2024, 12, 23), date(2024, 12, 27)))
    # 3
    ```

---

**Exercise 3.**
Write a class `Countdown` that takes a target `datetime` and provides a method `remaining()` that returns a human-readable string of the time remaining (days, hours, minutes). If the target has passed, return `"Event has passed"`.

??? success "Solution to Exercise 3"

    ```python
    from datetime import datetime

    class Countdown:
        def __init__(self, target):
            self.target = target

        def remaining(self):
            now = datetime.now()
            if now >= self.target:
                return "Event has passed"
            delta = self.target - now
            days = delta.days
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            return f"{days} days, {hours} hours, {minutes} minutes"

    # Test
    from datetime import timedelta
    future = datetime.now() + timedelta(days=10, hours=5, minutes=30)
    cd = Countdown(future)
    print(cd.remaining())  # ~10 days, 5 hours, 30 minutes

    past = datetime.now() - timedelta(days=1)
    cd2 = Countdown(past)
    print(cd2.remaining())  # Event has passed
    ```
