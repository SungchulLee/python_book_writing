# Enum Methods and Customization

Add methods to enums and customize their behavior to create powerful, expressive types.

!!! tip "Mental Model"
    An enum is not just a bag of constants -- it is a class, and its members are instances. This means you can add methods, properties, and even `__init__` to give each member domain-specific behavior. Instead of scattering `if status == ...` checks across your codebase, put the logic on the enum itself: `status.next_state()`.

---

## Adding Methods to Enums

```python
from enum import Enum

class Size(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3
    XLARGE = 4
    
    def get_next_size(self):
        '''Get the next larger size'''
        members = list(Size)
        idx = members.index(self)
        if idx < len(members) - 1:
            return members[idx + 1]
        return self
    
    def get_price_multiplier(self):
        '''Get price multiplier for this size'''
        multipliers = {
            Size.SMALL: 1.0,
            Size.MEDIUM: 1.25,
            Size.LARGE: 1.5,
            Size.XLARGE: 1.75
        }
        return multipliers[self]

small = Size.SMALL
print(small.get_next_size())        # Size.MEDIUM
print(small.get_price_multiplier()) # 1.0
```

!!! note "Closed Polymorphism"
    Enums with methods are a form of **closed polymorphism** — the set of variants is fixed at definition time, and each member can carry its own behavior. This is similar to algebraic data types in functional languages. Unlike open polymorphism (class inheritance, where anyone can add new subclasses), enum polymorphism is **exhaustive** — you can handle every case and be certain you haven't missed one. This makes enums ideal for state machines, command patterns, and any domain where the set of options is known and complete.

## Properties in Enums

```python
from enum import Enum
from functools import cached_property

class UserRole(Enum):
    GUEST = "guest"
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    
    @property
    def can_delete_posts(self):
        '''Check if role can delete posts'''
        return self in (UserRole.MODERATOR, UserRole.ADMIN)
    
    @property
    def can_ban_users(self):
        '''Check if role can ban users'''
        return self == UserRole.ADMIN
    
    @property
    def display_name(self):
        '''Human-readable role name'''
        return self.value.capitalize()

role = UserRole.MODERATOR
print(f"Role: {role.display_name}")          # Role: Moderator
print(f"Can delete posts: {role.can_delete_posts}")  # True
print(f"Can ban users: {role.can_ban_users}")        # False
```

## Class Methods in Enums

```python
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    
    @classmethod
    def from_string(cls, value: str):
        '''Create from string, case-insensitive'''
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        raise ValueError(f"Unknown environment: {value}")
    
    @classmethod
    def is_production(cls, env):
        '''Check if environment is production'''
        return env == cls.PRODUCTION

env = Environment.from_string("PRODUCTION")
print(env)                                  # Environment.PRODUCTION
print(Environment.is_production(env))       # True
```

## Custom Enum with __str__

```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    
    def __str__(self):
        '''Custom string representation'''
        symbols = {
            Status.PENDING: "⏳",
            Status.RUNNING: "▶️",
            Status.COMPLETED: "✅",
            Status.FAILED: "❌"
        }
        return f"{symbols[self]} {self.value}"

status = Status.RUNNING
print(status)           # ▶️ running
print(str(status))      # ▶️ running
```

## Enum with __repr__

```python
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    
    def __repr__(self):
        '''Detailed representation'''
        return f"<Priority: {self.name} (level {self.value})>"

priority = Priority.HIGH
print(repr(priority))   # <Priority: HIGH (level 3)>
```

## Computed Enum Values

```python
from enum import Enum
from datetime import datetime

class LogLevel(Enum):
    DEBUG = (1, "DEBUG", "🔍")
    INFO = (2, "INFO", "ℹ️")
    WARNING = (3, "WARNING", "⚠️")
    ERROR = (4, "ERROR", "❌")
    CRITICAL = (5, "CRITICAL", "🔴")
    
    def __init__(self, level, name_str, symbol):
        self.level = level
        self.name_str = name_str
        self.symbol = symbol
    
    def format_message(self, message: str) -> str:
        '''Format log message'''
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {self.symbol} {self.name_str}: {message}"

log = LogLevel.ERROR
print(log.format_message("Database connection failed"))
```

## Customizing Lookup

```python
from enum import Enum

class ErrorCode(Enum):
    NOT_FOUND = 404
    FORBIDDEN = 403
    SERVER_ERROR = 500
    
    def __init__(self, code):
        self.code = code
    
    @classmethod
    def from_http_status(cls, status_code: int):
        '''Look up by HTTP status code'''
        for member in cls:
            if member.code == status_code:
                return member
        raise ValueError(f"No enum for status code: {status_code}")
    
    def get_message(self) -> str:
        '''Get friendly error message'''
        messages = {
            404: "Resource not found",
            403: "Access forbidden",
            500: "Internal server error"
        }
        return messages.get(self.code, "Unknown error")

error = ErrorCode.from_http_status(404)
print(f"{error.code}: {error.get_message()}")  # 404: Resource not found
```

## When to Add Methods

- Validation logic
- Conversion operations
- Related computations
- Display formatting
- Lookup functionality

!!! warning "When NOT to Add Methods"
    Enums with methods are powerful, but not every enum needs them. Avoid adding methods when:

    - The logic doesn't depend on the enum member itself — use a standalone function instead.
    - The method grows complex enough to warrant its own class — this is a sign you need a full class hierarchy, not a method-heavy enum.
    - The enum is used purely as a set of constants (e.g., configuration keys) — methods add complexity without value.

    A good rule of thumb: if your enum has more method lines than member definitions, consider whether a class with an enum attribute would be clearer.

---

## Exercises

**Exercise 1.**
Create a `Season` enum with a method `is_warm()` that returns `True` for `SUMMER` and `SPRING`. Add a `__str__` override that returns a formatted string like `"Season: Spring"`. Iterate over all seasons and print which are warm.

??? success "Solution to Exercise 1"

        from enum import Enum

        class Season(Enum):
            SPRING = 1
            SUMMER = 2
            AUTUMN = 3
            WINTER = 4

            def is_warm(self):
                return self in (Season.SPRING, Season.SUMMER)

            def __str__(self):
                return f"Season: {self.name.capitalize()}"

        for s in Season:
            warm = "warm" if s.is_warm() else "cold"
            print(f"{s} ({warm})")

---

**Exercise 2.**
Define a `Coin` enum with `PENNY = 1`, `NICKEL = 5`, `DIME = 10`, `QUARTER = 25`. Add a `dollar_value` property that returns the value in dollars (e.g., `0.25` for QUARTER). Add a class method `total(coins)` that returns the total dollar value of a list of coins.

??? success "Solution to Exercise 2"

        from enum import Enum

        class Coin(Enum):
            PENNY = 1
            NICKEL = 5
            DIME = 10
            QUARTER = 25

            @property
            def dollar_value(self):
                return self.value / 100

            @classmethod
            def total(cls, coins):
                return sum(c.dollar_value for c in coins)

        coins = [Coin.QUARTER, Coin.DIME, Coin.NICKEL, Coin.PENNY]
        print(f"Total: ${Coin.total(coins):.2f}")  # Total: $0.41

---

**Exercise 3.**
Create a `Direction` enum with a `opposite` property that returns the opposite direction (NORTH returns SOUTH, etc.). Also add a `rotate(steps)` method that rotates clockwise by the given number of 90-degree steps. Demonstrate both features.

??? success "Solution to Exercise 3"

        from enum import Enum

        class Direction(Enum):
            NORTH = 0
            EAST = 1
            SOUTH = 2
            WEST = 3

            @property
            def opposite(self):
                return Direction((self.value + 2) % 4)

            def rotate(self, steps=1):
                return Direction((self.value + steps) % 4)

        print(Direction.NORTH.opposite)    # Direction.SOUTH
        print(Direction.EAST.opposite)     # Direction.WEST
        print(Direction.NORTH.rotate(1))   # Direction.EAST
        print(Direction.NORTH.rotate(3))   # Direction.WEST

---

**Exercise 4.**
An enum has grown to include a complex `process()` method with 20+ lines of logic. A colleague argues this is fine because "enums can have methods." Explain why this is a design smell and propose a refactored design that keeps the enum simple. Illustrate with a before/after sketch.

??? success "Solution to Exercise 4"

    **Why it's a smell:** Enums are meant to be lightweight symbolic constants. When methods grow complex, the enum takes on responsibilities that belong to a separate class. This makes the enum harder to test, harder to extend, and harder to read.

    **Before (design smell):**

        class TaskStatus(Enum):
            PENDING = "pending"
            RUNNING = "running"
            DONE = "done"

            def process(self, task, db, logger, notifier):
                if self == TaskStatus.PENDING:
                    # 20 lines of scheduling logic...
                    pass
                elif self == TaskStatus.RUNNING:
                    # 20 lines of monitoring logic...
                    pass
                elif self == TaskStatus.DONE:
                    # 20 lines of cleanup logic...
                    pass

    **After (clean separation):**

        class TaskStatus(Enum):
            PENDING = "pending"
            RUNNING = "running"
            DONE = "done"

        class TaskProcessor:
            def process(self, status: TaskStatus, task):
                handler = {
                    TaskStatus.PENDING: self._schedule,
                    TaskStatus.RUNNING: self._monitor,
                    TaskStatus.DONE: self._cleanup,
                }
                return handler[status](task)

    **Rule of thumb:** if a method needs dependencies beyond `self` (databases, loggers, external services), it belongs in a service class, not the enum.

---

**Exercise 5.**
Create a `Temperature` enum with members `FREEZING = 0`, `COLD = 10`, `WARM = 20`, `HOT = 30` (values in Celsius). Add a `to_fahrenheit` property, a `__str__` that shows both units, and a class method `from_celsius(temp)` that returns the closest matching member. Demonstrate all three.

??? success "Solution to Exercise 5"

        from enum import Enum

        class Temperature(Enum):
            FREEZING = 0
            COLD = 10
            WARM = 20
            HOT = 30

            @property
            def to_fahrenheit(self):
                return self.value * 9 / 5 + 32

            def __str__(self):
                return f"{self.name}: {self.value}°C / {self.to_fahrenheit:.0f}°F"

            @classmethod
            def from_celsius(cls, temp):
                return min(cls, key=lambda m: abs(m.value - temp))

        # Property
        print(Temperature.FREEZING.to_fahrenheit)  # 32.0

        # __str__
        print(Temperature.HOT)  # HOT: 30°C / 86°F

        # Class method
        print(Temperature.from_celsius(15))  # Temperature.COLD (closest to 15)
        print(Temperature.from_celsius(28))  # Temperature.HOT (closest to 28)
