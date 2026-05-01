# Enum Basics

Enums represent a fixed set of values, providing type safety and code clarity. Before enums, Python developers used plain constants (`STATUS_ACTIVE = 1`), strings (`"active"`), or class attributes — all of which are error-prone because nothing prevents typos, invalid values, or accidental comparisons between unrelated constants. Enums solve this by creating **singleton symbolic constants with identity semantics**: each member is a unique object, not just a value.

Enums rest on three core ideas:

- **Identity** — each member is a singleton object, not just a number or string. `Status.ACTIVE is Status.ACTIVE` is always `True`.
- **Restriction** — the set of valid values is closed and fixed at definition time. You cannot add or remove members at runtime.
- **Clarity** — `Status.ACTIVE` is self-documenting; `1` is not.

Everything else in this section — [variants](int_str_enum.md), [`auto()` generation](auto.md), [flags](flag.md), [methods](methods_customization.md), [patterns](practical_patterns.md) — builds on these three ideas.

!!! tip "Mental Model: Name, Value, and Identity"
    Every enum member has three aspects:

    - **Name** — the Python identifier (e.g., `Color.RED`). Used in code.
    - **Value** — the underlying data (e.g., `1` or `"red"`). Used for serialization and lookups.
    - **Identity** — enum members are singletons. `Color.RED is Color.RED` is always `True`, and `Color.RED == 1` is always `False` (unless using `IntEnum`).

    The most common beginner mistake is confusing value comparison with identity comparison. `Color.RED == 1` is `False` even if `Color.RED.value == 1` is `True`.

!!! note "Enum Members Are Objects"
    Each enum member is a **singleton instance** of its enum class. `Color.RED` is an instance of `Color`, just like any other Python object:

    ```python
    isinstance(Color.RED, Color)  # True
    type(Color.RED)               # <enum 'Color'>
    ```

    This means enum members can have methods, participate in attribute lookup, and behave like any other object. The only difference is that they are created at class definition time and cannot be instantiated afterward.

---

## Creating Basic Enums

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

class Size(Enum):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    XLARGE = "XL"

# Access members
print(Color.RED)          # Color.RED
print(Color.RED.name)     # 'RED'
print(Color.RED.value)    # 1

print(Size.MEDIUM)        # Size.MEDIUM
print(Size.MEDIUM.value)  # 'M'
```

## Enum Iteration

```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

# Iterate over all members
for status in Status:
    print(f"{status.name}: {status.value}")

# Get all values
values = [s.value for s in Status]
print(values)  # ['pending', 'running', 'completed', 'failed']

# Get all names
names = [s.name for s in Status]
print(names)   # ['PENDING', 'RUNNING', 'COMPLETED', 'FAILED']
```

## Accessing Enum Members

```python
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

# By name
priority1 = Priority['HIGH']        # Priority.HIGH
priority2 = Priority.HIGH           # Priority.HIGH

# By value
priority3 = Priority(3)             # Priority.HIGH

# Comparison
print(Priority.HIGH == Priority.HIGH)      # True
print(Priority.HIGH == Priority.MEDIUM)    # False
print(Priority.HIGH.value == 3)            # True
```

## Type Checking with Enums

```python
from enum import Enum
from typing import Union

class Environment(Enum):
    DEVELOPMENT = "dev"
    STAGING = "staging"
    PRODUCTION = "prod"

def deploy(env: Environment):
    if env == Environment.PRODUCTION:
        print("⚠️ Deploying to PRODUCTION")
    elif env == Environment.STAGING:
        print("Deploying to staging")
    else:
        print("Deploying to development")

deploy(Environment.PRODUCTION)
# deploy("production")  # Type error - caught by linters
```

## Enum Membership Testing

```python
from enum import Enum

class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"

def handle_request(method: str):
    try:
        http_method = HTTPMethod[method.upper()]
        print(f"Handling {http_method.value} request")
    except KeyError:
        print(f"Unknown HTTP method: {method}")

handle_request("GET")      # Works
handle_request("TRACE")    # Unknown HTTP method: TRACE
```

## Enum Comparison and Ordering

```python
from enum import Enum

class Grade(Enum):
    F = 1
    D = 2
    C = 3
    B = 4
    A = 5

grade1 = Grade.A
grade2 = Grade.C

print(grade1 == Grade.A)        # True
print(grade1 != grade2)         # True
# Can't use <, >, <=, >= on regular Enums
```

## Common Pitfalls

!!! danger "Pitfall: Comparing Enum Members with Raw Values"
    ```python
    class Status(Enum):
        ACTIVE = 1

    # WRONG — always False for regular Enum
    if status == 1:
        ...

    # CORRECT
    if status == Status.ACTIVE:
        ...
    ```

    Regular `Enum` members do **not** compare equal to their values. Use `status.value == 1` if you need a value comparison, or use `IntEnum`/`StrEnum` if you genuinely need transparent interop.

!!! danger "Pitfall: Serialization Surprises"
    `json.dumps(Status.ACTIVE)` raises `TypeError` because enum members are not JSON-serializable by default. Always serialize via `.value` or `.name`:

    ```python
    json.dumps({"status": Status.ACTIVE.value})  # OK
    ```

## Best Practices

- Use Enums for fixed sets of values
- Provide descriptive names (not `E1`, `E2`, etc.)
- Keep enum definitions at module level
- Use type hints with Enum types
- Document what each member represents

!!! tip "When NOT to Use Enums"
    Enums are for **fixed, known-at-definition-time** sets. Avoid them when:

    - Values come from user input, databases, or configuration files at runtime — use a dictionary or data class instead.
    - The set of values changes frequently — adding/removing enum members requires code changes and redeployment.
    - You need a large number of members (hundreds+) — enums add per-member overhead and are not designed as data containers.

---

## Exercises

**Exercise 1.**
Create a `Season` enum with members `SPRING`, `SUMMER`, `AUTUMN`, `WINTER` and string values (`"spring"`, etc.). Write a function `describe_season(season: Season)` that returns a description. Iterate over all seasons and print name, value, and description.

??? success "Solution to Exercise 1"

        from enum import Enum

        class Season(Enum):
            SPRING = "spring"
            SUMMER = "summer"
            AUTUMN = "autumn"
            WINTER = "winter"

        def describe_season(season: Season):
            descriptions = {
                Season.SPRING: "Flowers bloom",
                Season.SUMMER: "Hot and sunny",
                Season.AUTUMN: "Leaves fall",
                Season.WINTER: "Cold and snowy",
            }
            return descriptions[season]

        for s in Season:
            print(f"{s.name} ({s.value}): {describe_season(s)}")

---

**Exercise 2.**
Define a `HTTPMethod` enum with members `GET`, `POST`, `PUT`, `DELETE`. Write a function that accepts a string (like `"get"`) and returns the corresponding enum member using bracket notation (`HTTPMethod[...]`). Handle invalid input with a try/except that catches `KeyError`.

??? success "Solution to Exercise 2"

        from enum import Enum

        class HTTPMethod(Enum):
            GET = "GET"
            POST = "POST"
            PUT = "PUT"
            DELETE = "DELETE"

        def parse_method(method_str):
            try:
                return HTTPMethod[method_str.upper()]
            except KeyError:
                print(f"Unknown method: {method_str}")
                return None

        print(parse_method("get"))     # HTTPMethod.GET
        print(parse_method("post"))    # HTTPMethod.POST
        print(parse_method("PATCH"))   # Unknown method: PATCH -> None

---

**Exercise 3.**
Create a `Priority` enum with members `LOW = 1`, `MEDIUM = 2`, `HIGH = 3`, `CRITICAL = 4`. Write a function `filter_by_priority(tasks, min_priority)` where each task is a tuple of `(name, Priority)`. It should return only tasks with priority >= `min_priority` by comparing `.value`. Demonstrate with a list of tasks.

??? success "Solution to Exercise 3"

        from enum import Enum

        class Priority(Enum):
            LOW = 1
            MEDIUM = 2
            HIGH = 3
            CRITICAL = 4

        def filter_by_priority(tasks, min_priority):
            return [(name, p) for name, p in tasks if p.value >= min_priority.value]

        tasks = [
            ("Fix typo", Priority.LOW),
            ("Update docs", Priority.MEDIUM),
            ("Security patch", Priority.CRITICAL),
            ("New feature", Priority.HIGH),
        ]

        urgent = filter_by_priority(tasks, Priority.HIGH)
        for name, p in urgent:
            print(f"[{p.name}] {name}")
        # [CRITICAL] Security patch
        # [HIGH] New feature

---

**Exercise 4.**
Explain why the following comparison returns `False`, even though the enum member's value is `1`. What would you change to make the comparison return `True` without using `.value`?

```python
from enum import Enum

class Status(Enum):
    ACTIVE = 1

print(Status.ACTIVE == 1)  # False — why?
```

??? success "Solution to Exercise 4"

    Regular `Enum` members use **identity-based comparison**, not value-based. `Status.ACTIVE` is an `Enum` object, not the integer `1`, so `Status.ACTIVE == 1` is `False` even though `Status.ACTIVE.value == 1` is `True`.

    Two ways to make the comparison work:

    1. **Compare values explicitly:** `Status.ACTIVE.value == 1` — keeps type safety, makes intent clear.
    2. **Use `IntEnum`:** `class Status(IntEnum): ACTIVE = 1` — now `Status.ACTIVE == 1` is `True`, but you lose the type safety guarantee that prevents accidental comparisons with unrelated integers.

    The `Enum` behavior is intentional: it forces you to compare `Status.ACTIVE == Status.ACTIVE` (clear intent) rather than `Status.ACTIVE == 1` (ambiguous — does `1` mean "active" or is it a count?).

---

**Exercise 5.**
A colleague stores enum values in a JSON config file and reads them back. The following code raises an error. Explain why and show two ways to fix it.

```python
from enum import Enum
import json

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

data = {"color": Color.RED}
json.dumps(data)  # TypeError!
```

??? success "Solution to Exercise 5"

    `json.dumps` does not know how to serialize `Enum` objects — they are not one of JSON's native types (`str`, `int`, `float`, `bool`, `None`, `list`, `dict`).

    **Fix 1 — Serialize the value manually:**

        data = {"color": Color.RED.value}
        json_str = json.dumps(data)          # '{"color": 1}'
        restored = Color(json.loads(json_str)["color"])  # Color.RED

    **Fix 2 — Custom JSON encoder:**

        class EnumEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, Enum):
                    return obj.value
                return super().default(obj)

        json_str = json.dumps({"color": Color.RED}, cls=EnumEncoder)
        # '{"color": 1}'

    The first approach is simpler and explicit. The second is useful when enum members appear in many places and you want a consistent serialization strategy.
