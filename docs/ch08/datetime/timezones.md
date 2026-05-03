# Timezone Handling (timezone, zoneinfo)

Handle timezones with `timezone` for fixed offsets and `zoneinfo` for named timezones.

!!! tip "Mental Model"
    A "naive" datetime is like a clock with no label — you know the time, but not *where*. Attaching a timezone makes it "aware," anchoring it to a specific point on Earth. Use `timezone` for simple fixed offsets (UTC+5) and `zoneinfo` for real-world zones (America/New_York) that handle daylight saving automatically.

## Fixed Timezones with timezone

Create fixed timezone offsets.

```python
from datetime import datetime, timezone, timedelta

# UTC timezone
utc = timezone.utc
now_utc = datetime.now(utc)
print(f"UTC: {now_utc}")

# Custom offset (EST is UTC-5)
est = timezone(timedelta(hours=-5))
now_est = datetime.now(est)
print(f"EST: {now_est}")

# Convert between timezones
print(f"UTC: {now_utc}")
print(f"EST: {now_utc.astimezone(est)}")
```

```
UTC: 2026-02-12 20:00:00+00:00
EST: 2026-02-12 15:00:00-05:00
UTC: 2026-02-12 20:00:00+00:00
EST: 2026-02-12 15:00:00-05:00
```

## Named Timezones with zoneinfo

Use named timezone identifiers from the IANA database.

```python
from datetime import datetime
from zoneinfo import ZoneInfo

# Get current time in different timezones
timezones = ["UTC", "America/New_York", "Europe/London", "Asia/Tokyo"]

now = datetime.now()
for tz_name in timezones:
    tz = ZoneInfo(tz_name)
    local_time = now.astimezone(tz)
    print(f"{tz_name}: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}
```

```
UTC: 2026-02-12 20:00:00 UTC
America/New_York: 2026-02-12 15:00:00 EST
Europe/London: 2026-02-12 20:00:00 GMT
Asia/Tokyo: 2026-02-13 05:00:00 JST
```

---

## Exercises

**Exercise 1.**
Write a function `utc_to_local` that takes a naive `datetime` (assumed UTC) and a timezone name string (e.g., `"America/New_York"`) and returns the corresponding aware `datetime` in that timezone. Use `zoneinfo.ZoneInfo`.

??? success "Solution to Exercise 1"

    ```python
    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo

    def utc_to_local(naive_dt, tz_name):
        utc_dt = naive_dt.replace(tzinfo=timezone.utc)
        local_tz = ZoneInfo(tz_name)
        return utc_dt.astimezone(local_tz)

    # Test
    utc_time = datetime(2024, 12, 25, 14, 0, 0)
    ny_time = utc_to_local(utc_time, "America/New_York")
    print(ny_time)  # 2024-12-25 09:00:00-05:00
    ```

---

**Exercise 2.**
Write a function `time_difference_hours` that takes two timezone name strings and returns the current time difference in hours between them. For example, `time_difference_hours("America/New_York", "Asia/Tokyo")` should return `14` (or `13` depending on DST).

??? success "Solution to Exercise 2"

    ```python
    from datetime import datetime
    from zoneinfo import ZoneInfo

    def time_difference_hours(tz1_name, tz2_name):
        now = datetime.now(ZoneInfo("UTC"))
        time1 = now.astimezone(ZoneInfo(tz1_name))
        time2 = now.astimezone(ZoneInfo(tz2_name))
        offset1 = time1.utcoffset().total_seconds() / 3600
        offset2 = time2.utcoffset().total_seconds() / 3600
        return abs(offset2 - offset1)

    # Test
    diff = time_difference_hours("America/New_York", "Asia/Tokyo")
    print(f"Difference: {diff} hours")  # 14.0 (or 13.0 with DST)
    ```

---

**Exercise 3.**
Write a function `meeting_time` that takes a `datetime` in one timezone and converts it to a list of `(timezone_name, local_time_string)` tuples for a list of attendee timezones. Format each time as `"HH:MM AM/PM"`. For example, a meeting at 2 PM UTC should show the corresponding local times for New York, London, and Tokyo.

??? success "Solution to Exercise 3"

    ```python
    from datetime import datetime
    from zoneinfo import ZoneInfo

    def meeting_time(dt, attendee_timezones):
        results = []
        for tz_name in attendee_timezones:
            local = dt.astimezone(ZoneInfo(tz_name))
            time_str = local.strftime("%I:%M %p")
            results.append((tz_name, time_str))
        return results

    # Test
    meeting = datetime(2024, 12, 25, 14, 0, tzinfo=ZoneInfo("UTC"))
    zones = ["America/New_York", "Europe/London", "Asia/Tokyo"]
    for tz, time_str in meeting_time(meeting, zones):
        print(f"{tz}: {time_str}")
    # America/New_York: 09:00 AM
    # Europe/London: 02:00 PM
    # Asia/Tokyo: 11:00 PM
    ```
