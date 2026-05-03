# Flag and IntFlag

Flag and IntFlag are specialized enums for bit flags, supporting bitwise operations like OR, AND, and NOT.

!!! tip "Mental Model"
    A regular `Enum` is a radio button -- exactly one option selected at a time. A `Flag` is a row of checkboxes -- multiple options can be active simultaneously. Each flag member occupies a unique bit position, so combining them with `|` and testing them with `in` is fast, unambiguous, and type-safe.

!!! note "Flag vs Enum"
    A regular `Enum` represents **one value at a time** — a status is either `PENDING` or `ACTIVE`, never both. A `Flag` represents a **combination of values** (a bitmask) — a user can have `READ` and `WRITE` and `EXECUTE` permissions simultaneously. Use `Flag` when multiple options can be active at the same time; use `Enum` when exactly one option is selected.

!!! tip "Why Powers of 2?"
    Each flag member must be a distinct power of 2 (`1, 2, 4, 8, ...`). This works because in binary, each power of 2 sets exactly **one unique bit**:

    ```
    READ    = 1  →  001
    WRITE   = 2  →  010
    EXECUTE = 4  →  100
    ```

    Combining flags with `|` (OR) sets multiple bits: `READ | WRITE = 011 = 3`. Testing with `in` (AND) checks whether a specific bit is set. If you used consecutive integers (1, 2, 3) instead, the bit patterns would overlap and combinations would be ambiguous — `3` could mean "EXECUTE" or "READ + WRITE."

---

## Flag Basics

```python
from enum import Flag, auto

class Permission(Flag):
    READ = auto()      # 1
    WRITE = auto()     # 2
    EXECUTE = auto()   # 4

# Single permission
user1_perms = Permission.READ
print(user1_perms)              # Permission.READ

# Multiple permissions with bitwise OR
user2_perms = Permission.READ | Permission.WRITE
print(user2_perms)              # Permission.READ|WRITE

# Check if permission is set
print(Permission.READ in user2_perms)     # True
print(Permission.EXECUTE in user2_perms)  # False
```

## Practical Flag Example

```python
from enum import Flag, auto

class FileMode(Flag):
    READABLE = auto()    # 1
    WRITABLE = auto()    # 2
    EXECUTABLE = auto()  # 4

def check_permissions(mode: FileMode, required: FileMode) -> bool:
    return required in mode

file_mode = FileMode.READABLE | FileMode.WRITABLE

# Check single permission
print(check_permissions(file_mode, FileMode.READABLE))    # True
print(check_permissions(file_mode, FileMode.EXECUTABLE))  # False

# Check multiple permissions
can_read_write = FileMode.READABLE | FileMode.WRITABLE
print(can_read_write in file_mode)  # True
```

## IntFlag

```python
from enum import IntFlag, auto

class Status(IntFlag):
    RUNNING = auto()     # 1
    PAUSED = auto()      # 2
    STOPPED = auto()     # 4
    ERROR = auto()       # 8

# IntFlag can also use arithmetic
status = Status.RUNNING | Status.ERROR
print(status)           # Status.RUNNING|ERROR
print(status.value)     # 9 (1 + 8)

# Can mix with integers
combined = status | 0x10  # Add raw bits
print(combined.value)     # 25

# Bitwise operations work
print(status & Status.RUNNING)  # Status.RUNNING
print(status & Status.PAUSED)   # Status(0) - empty
```

## Flag Iteration and Checking

```python
from enum import Flag, auto

class Feature(Flag):
    FEATURE_A = auto()
    FEATURE_B = auto()
    FEATURE_C = auto()
    FEATURE_D = auto()

enabled_features = Feature.FEATURE_A | Feature.FEATURE_C

# Iterate over enabled features
print("Enabled features:")
for feature in Feature:
    if feature in enabled_features:
        print(f"  - {feature.name}")

# Count enabled features
count = bin(enabled_features.value).count('1')
print(f"Total enabled: {count}")
```

## Combining Flags

```python
from enum import Flag, auto

class DatabaseOption(Flag):
    CACHE = auto()           # 1
    REPLICATE = auto()       # 2
    COMPRESS = auto()        # 4
    ENCRYPT = auto()         # 8
    VALIDATE = auto()        # 16

def create_connection(options: DatabaseOption):
    if DatabaseOption.ENCRYPT in options:
        print("Enabling encryption")
    if DatabaseOption.CACHE in options:
        print("Enabling cache")
    if DatabaseOption.REPLICATE in options:
        print("Enabling replication")

# Create options combination
conn_options = (DatabaseOption.ENCRYPT | 
                DatabaseOption.CACHE | 
                DatabaseOption.REPLICATE)

create_connection(conn_options)
```

## Removing Flags

```python
from enum import Flag, auto

class Permission(Flag):
    READ = auto()
    WRITE = auto()
    DELETE = auto()
    ADMIN = auto()

# Start with multiple permissions
perms = Permission.READ | Permission.WRITE | Permission.DELETE

# Remove a permission
perms = perms & ~Permission.DELETE  # Bitwise NOT and AND
print(perms)                        # Permission.READ|WRITE

# Check it's gone
print(Permission.DELETE in perms)   # False
```

## IntFlag Arithmetic

```python
from enum import IntFlag, auto

class Level(IntFlag):
    BASIC = auto()         # 1
    INTERMEDIATE = auto()  # 2
    ADVANCED = auto()      # 4

level = Level.INTERMEDIATE
print(level.value)        # 2

# IntFlag supports arithmetic
next_level = level | Level.ADVANCED
print(next_level.value)   # 6

# Can extract individual flags
remaining = next_level & ~Level.INTERMEDIATE
print(remaining)          # Level.ADVANCED
```

## When to Use Flag

- Permissions and capabilities
- Feature toggles
- Configuration options
- Combination of boolean settings
- Need bitwise operations

---

## Exercises

**Exercise 1.**
Create a `FilePermission` Flag with `READ`, `WRITE`, `EXECUTE`. Write a function `check_access(user_perms, required_perms)` that returns `True` if the user has all required permissions. Test with various combinations.

??? success "Solution to Exercise 1"

        from enum import Flag, auto

        class FilePermission(Flag):
            READ = auto()
            WRITE = auto()
            EXECUTE = auto()

        def check_access(user_perms, required_perms):
            return required_perms in user_perms

        user = FilePermission.READ | FilePermission.WRITE
        print(check_access(user, FilePermission.READ))                # True
        print(check_access(user, FilePermission.EXECUTE))             # False
        print(check_access(user, FilePermission.READ | FilePermission.WRITE))  # True

---

**Exercise 2.**
Define a `Feature` Flag with `DARK_MODE`, `NOTIFICATIONS`, `ANALYTICS`, `BETA`. Write a function `toggle_feature(current, feature)` that flips a feature on or off (using XOR `^`). Start with no features enabled and toggle several features on and off.

??? success "Solution to Exercise 2"

        from enum import Flag, auto

        class Feature(Flag):
            DARK_MODE = auto()
            NOTIFICATIONS = auto()
            ANALYTICS = auto()
            BETA = auto()

        def toggle_feature(current, feature):
            return current ^ feature

        features = Feature(0)  # No features
        features = toggle_feature(features, Feature.DARK_MODE)
        print(features)  # Feature.DARK_MODE

        features = toggle_feature(features, Feature.NOTIFICATIONS)
        print(features)  # Feature.DARK_MODE|NOTIFICATIONS

        features = toggle_feature(features, Feature.DARK_MODE)  # Toggle off
        print(features)  # Feature.NOTIFICATIONS

---

**Exercise 3.**
Create an `IntFlag` called `StatusCode` with `RUNNING = 1`, `PAUSED = 2`, `ERROR = 4`, `MAINTENANCE = 8`. Demonstrate that `IntFlag` values can be combined with plain integers using `|`. Show that `status.value` returns the numeric sum and that individual flags can be extracted using `&`.

??? success "Solution to Exercise 3"

        from enum import IntFlag, auto

        class StatusCode(IntFlag):
            RUNNING = 1
            PAUSED = 2
            ERROR = 4
            MAINTENANCE = 8

        status = StatusCode.RUNNING | StatusCode.ERROR
        print(status)         # StatusCode.RUNNING|ERROR
        print(status.value)   # 5 (1 + 4)

        # Can mix with integers
        combined = status | 0x10
        print(combined.value)  # 21

        # Extract individual flags
        print(status & StatusCode.RUNNING)  # StatusCode.RUNNING
        print(status & StatusCode.PAUSED)   # StatusCode(0) — not set

---

**Exercise 4.**
Explain why the following `Flag` definition is broken. What value does `ADMIN` get, and why does combining `READ | WRITE` produce an ambiguous result?

```python
from enum import Flag

class BadPermission(Flag):
    READ = 1
    WRITE = 2
    EXECUTE = 3   # NOT a power of 2!
    ADMIN = 4
```

??? success "Solution to Exercise 4"

    `EXECUTE = 3` is `011` in binary — the same bit pattern as `READ | WRITE` (`001 | 010 = 011`). This means there is no way to tell whether a combined value of `3` means "EXECUTE alone" or "READ + WRITE together."

    `ADMIN = 4` (`100`) is fine because it is a power of 2 and occupies its own unique bit.

    The fix is to use powers of 2 for every member:

        class Permission(Flag):
            READ = 1       # 001
            WRITE = 2      # 010
            EXECUTE = 4    # 100
            ADMIN = 8      # 1000

    Alternatively, use `auto()` which assigns powers of 2 automatically for `Flag` enums. The rule is simple: every flag member must set **exactly one bit** that no other member sets.

---

**Exercise 5.**
Create a `Flag` enum `Weekday` with members for each day of the week (MON through SUN). Define composite members `WEEKDAYS = MON | TUE | WED | THU | FRI` and `WEEKEND = SAT | SUN`. Write a function `is_workday(day: Weekday) -> bool` that checks whether a single day is in `WEEKDAYS`. Demonstrate with several days.

??? success "Solution to Exercise 5"

        from enum import Flag, auto

        class Weekday(Flag):
            MON = auto()
            TUE = auto()
            WED = auto()
            THU = auto()
            FRI = auto()
            SAT = auto()
            SUN = auto()
            WEEKDAYS = MON | TUE | WED | THU | FRI
            WEEKEND = SAT | SUN

        def is_workday(day: Weekday) -> bool:
            return day in Weekday.WEEKDAYS

        print(is_workday(Weekday.MON))  # True
        print(is_workday(Weekday.SAT))  # False
        print(is_workday(Weekday.FRI))  # True
        print(is_workday(Weekday.SUN))  # False

        # Composite members work too
        print(Weekday.WEEKEND)  # Weekday.SAT|SUN
