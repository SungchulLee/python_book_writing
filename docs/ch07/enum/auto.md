# auto() Function

The `auto()` function automatically assigns values to enum members, eliminating tedious manual assignment.

!!! tip "Mental Model"
    `auto()` tells Python "I care about the names, not the values -- just number them for me." This is the right choice when member identity matters more than the underlying value. If you persist enum values externally (databases, APIs), prefer explicit values, because reordering members silently changes what `auto()` assigns.

!!! warning "Order Sensitivity"
    When using `auto()` with default integer values, the assigned values depend on **member declaration order**. Reordering members changes their values. If your code persists enum values (databases, APIs, config files), prefer explicit values to avoid silent breakage when members are reordered.

---

## Basic auto() Usage

```python
from enum import Enum, auto

class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()

print(Color.RED)        # Color.RED
print(Color.RED.value)  # 1
print(Color.GREEN.value)  # 2
print(Color.BLUE.value)   # 3

# Values are auto-incremented starting from 1
for color in Color:
    print(f"{color.name} = {color.value}")
```

## auto() with Flag

```python
from enum import Flag, auto

class Permission(Flag):
    READ = auto()      # 1
    WRITE = auto()     # 2
    EXECUTE = auto()   # 4

# Flag auto() uses powers of 2
for perm in Permission:
    print(f"{perm.name} = {perm.value}")

# Allows bitwise operations
user_perms = Permission.READ | Permission.WRITE
print(user_perms)  # Permission.READ|WRITE
```

## Customizing auto() Behavior

Override `_generate_next_value_` to control what `auto()` produces. This static method is called once per member during class creation and receives four arguments:

| Parameter | Meaning |
|---|---|
| `name` | The member's Python name (e.g., `"LOW"`) |
| `start` | The start value (default `1`, rarely changed) |
| `count` | How many members have been created so far |
| `last_values` | List of all previously assigned values |

The return value becomes the member's `.value`.

```python
from enum import Enum, auto

class Priority(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()
    
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

print(Priority.LOW.value)        # 'low'
print(Priority.CRITICAL.value)   # 'critical'
```

## auto() with Strings

```python
from enum import Enum, auto

class HttpMethod(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.upper()
    
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    PATCH = auto()

print(HttpMethod.GET.value)     # 'GET'
print(HttpMethod.DELETE.value)  # 'DELETE'
```

## Mixing auto() and Manual Values

```python
from enum import Enum, auto

class Status(Enum):
    PENDING = auto()      # 1
    APPROVED = auto()     # 2
    CUSTOM = "special"    # manual value
    REJECTED = auto()     # 3
    ARCHIVED = auto()     # 4

for status in Status:
    print(f"{status.name}: {status.value}")
```

## auto() with IntEnum

```python
from enum import IntEnum, auto

class HttpStatus(IntEnum):
    # Custom auto for specific patterns
    def _generate_next_value_(name, start, count, last_values):
        if count == 0:
            return 100
        elif count < 3:
            return 100 + (count - 1) * 10 + 1
        elif count < 6:
            return 200 + (count - 3) * 100
        else:
            return 400 + (count - 6) * 50
    
    CONTINUE = auto()          # 100
    SWITCHING = auto()         # 101
    PROCESSING = auto()        # 102
    OK = auto()                # 200
    CREATED = auto()           # 300
    BAD_REQUEST = auto()       # 400

print(HttpStatus.CONTINUE.value)     # 100
print(HttpStatus.OK.value)           # 200
print(HttpStatus.BAD_REQUEST.value)  # 400
```

## auto() for String Slugs

```python
from enum import Enum, auto

class ContentType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower().replace('_', '-')
    
    PLAIN_TEXT = auto()
    RICH_TEXT = auto()
    HTML_PAGE = auto()
    JSON_DATA = auto()

print(ContentType.PLAIN_TEXT.value)   # 'plain-text'
print(ContentType.HTML_PAGE.value)    # 'html-page'
print(ContentType.JSON_DATA.value)    # 'json-data'
```

## When to Use auto()

- Ordering matters but exact value doesn't
- Avoiding manual typos in value assignment
- Natural progression (1, 2, 3, ...)
- Combined with custom `_generate_next_value_` for domain-specific values

!!! warning "When to Avoid auto()"
    Use `auto()` only when values are **not externally visible**. If enum values are stored in databases, sent over APIs, or written to configuration files, use explicit values instead. With `auto()`, reordering members or inserting new ones silently changes the assigned values, which can corrupt persisted data.

---

## Exercises

**Exercise 1.**
Create a `Direction` enum using `auto()` for values. Then create a `LogLevel` enum that uses a custom `_generate_next_value_` to set values as the lowercase member name (e.g., `DEBUG` gets value `"debug"`). Print all members and their values for both enums.

??? success "Solution to Exercise 1"

        from enum import Enum, auto

        class Direction(Enum):
            NORTH = auto()
            SOUTH = auto()
            EAST = auto()
            WEST = auto()

        for d in Direction:
            print(f"{d.name} = {d.value}")
        # NORTH = 1, SOUTH = 2, EAST = 3, WEST = 4

        class LogLevel(Enum):
            def _generate_next_value_(name, start, count, last_values):
                return name.lower()

            DEBUG = auto()
            INFO = auto()
            WARNING = auto()
            ERROR = auto()

        for level in LogLevel:
            print(f"{level.name} = {level.value!r}")
        # DEBUG = 'debug', INFO = 'info', etc.

---

**Exercise 2.**
Define a `Permission` Flag enum using `auto()`. Members should be `READ`, `WRITE`, `EXECUTE`, and `ADMIN`. Demonstrate combining permissions with `|`, checking with `in`, and removing a permission with `& ~`. Show that `auto()` assigns powers of 2 for Flag.

??? success "Solution to Exercise 2"

        from enum import Flag, auto

        class Permission(Flag):
            READ = auto()      # 1
            WRITE = auto()     # 2
            EXECUTE = auto()   # 4
            ADMIN = auto()     # 8

        # Combine
        user_perms = Permission.READ | Permission.WRITE
        print(user_perms)  # Permission.READ|WRITE

        # Check
        print(Permission.READ in user_perms)     # True
        print(Permission.ADMIN in user_perms)    # False

        # Remove
        user_perms = user_perms & ~Permission.WRITE
        print(user_perms)  # Permission.READ

---

**Exercise 3.**
Create a `APIEndpoint` enum with a custom `_generate_next_value_` that converts member names to URL-style slugs (e.g., `USER_PROFILE` becomes `"/user-profile"`). Add members `HOME`, `USER_PROFILE`, `SETTINGS_PAGE`, and `API_DOCS`. Print each member's value to verify the slug conversion.

??? success "Solution to Exercise 3"

        from enum import Enum, auto

        class APIEndpoint(Enum):
            def _generate_next_value_(name, start, count, last_values):
                return "/" + name.lower().replace("_", "-")

            HOME = auto()
            USER_PROFILE = auto()
            SETTINGS_PAGE = auto()
            API_DOCS = auto()

        for endpoint in APIEndpoint:
            print(f"{endpoint.name}: {endpoint.value}")
        # HOME: /home
        # USER_PROFILE: /user-profile
        # SETTINGS_PAGE: /settings-page
        # API_DOCS: /api-docs

---

**Exercise 4.**
A developer stores `auto()`-generated integer values in a database. Later, they reorder the enum members and add a new one in the middle. Explain what goes wrong and how to prevent it. Write a short example showing the before and after to illustrate the problem.

??? success "Solution to Exercise 4"

    With `auto()`, values are assigned by declaration order starting from 1. Reordering members or inserting new ones changes the values assigned to existing members:

        # BEFORE
        class Status(Enum):
            PENDING = auto()    # 1
            ACTIVE = auto()     # 2
            ARCHIVED = auto()   # 3

        # AFTER — added REVIEW in the middle
        class Status(Enum):
            PENDING = auto()    # 1
            REVIEW = auto()     # 2  ← new
            ACTIVE = auto()     # 3  ← was 2!
            ARCHIVED = auto()   # 4  ← was 3!

    Any database rows that stored `2` for `ACTIVE` now map to `REVIEW` instead — a silent data corruption bug.

    **Prevention:** When values are persisted externally, always use explicit values:

        class Status(Enum):
            PENDING = 1
            REVIEW = 4     # New members get new explicit values
            ACTIVE = 2
            ARCHIVED = 3

    Use `auto()` only when the specific value does not matter (e.g., internal-only enums where only identity is compared).

---

**Exercise 5.**
Write a `_generate_next_value_` override that assigns values as `"{name}:{count}"` — for example, the first member `ALPHA` gets value `"ALPHA:0"`, the second member `BETA` gets `"BETA:1"`. Create an enum `Tag` with members `ALPHA`, `BETA`, `GAMMA` and verify the values. Then explain which of the four parameters you used and which you ignored.

??? success "Solution to Exercise 5"

        from enum import Enum, auto

        class Tag(Enum):
            def _generate_next_value_(name, start, count, last_values):
                return f"{name}:{count}"

            ALPHA = auto()
            BETA = auto()
            GAMMA = auto()

        for t in Tag:
            print(f"{t.name} = {t.value!r}")
        # ALPHA = 'ALPHA:0'
        # BETA = 'BETA:1'
        # GAMMA = 'GAMMA:2'

    **Parameters used:** `name` (the member's Python name) and `count` (how many members have been defined before this one, starting from 0).

    **Parameters ignored:** `start` (the default starting integer, only relevant for numeric sequences) and `last_values` (the list of previously assigned values — useful when each value depends on the previous one, e.g., doubling).
