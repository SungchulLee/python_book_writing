# Enum Members and Values

Access and manipulate enum members and their values. Understand the differences between names, values, and member objects. For everyday use, you only need `member.name`, `member.value`, `EnumClass(value)`, and `EnumClass['NAME']`. The internal attributes (`_member_map_`, `_value2member_map_`) shown later in this page are advanced — useful for introspection and metaprogramming, but not needed for typical enum usage.

!!! tip "Mental Model"
    An enum member is a triple: the **member object** itself (e.g., `Fruit.APPLE`), its **name** (the string `"APPLE"`), and its **value** (whatever you assigned, like `"apple"`). Access goes both ways: `EnumClass['NAME']` for name-to-member and `EnumClass(value)` for value-to-member. The member is the identity; the name and value are just labels attached to it.

---

## Accessing Names and Values

```python
from enum import Enum

class Fruit(Enum):
    APPLE = "apple"
    BANANA = "banana"
    ORANGE = "orange"

# Get member object
apple = Fruit.APPLE
print(apple)              # Fruit.APPLE
print(type(apple))        # <enum 'Fruit'>

# Access name and value separately
print(apple.name)         # 'APPLE'
print(apple.value)        # 'apple'

# Both directions
print(Fruit['APPLE'])     # Fruit.APPLE
print(Fruit('apple'))     # Fruit.APPLE
```

## Listing All Members

```python
from enum import Enum

class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

# Access _member_names_ (tuple) — ADVANCED: internal API
print(Day._member_names_)  # ('MONDAY', 'TUESDAY', ...)

# Access _member_map_ (dict name -> member) — ADVANCED: internal API
print(Day._member_map_['FRIDAY'])  # Day.FRIDAY

# Access _value2member_map_ (dict value -> member) — ADVANCED: internal API
print(Day._value2member_map_[5])   # Day.FRIDAY

# Iterate
for day in Day:
    print(f"{day.name}: {day.value}")
```

## Creating Enums with Complex Values

```python
from enum import Enum
from dataclasses import dataclass

@dataclass
class Config:
    code: str
    description: str

class ErrorType(Enum):
    NOT_FOUND = Config("404", "Resource not found")
    FORBIDDEN = Config("403", "Access denied")
    SERVER_ERROR = Config("500", "Internal server error")

error = ErrorType.NOT_FOUND
print(f"{error.value.code}: {error.value.description}")
# Output: 404: Resource not found
```

## Alias Members

```python
from enum import Enum

class Status(Enum):
    ACTIVE = 1
    INACTIVE = 2
    PENDING = 3
    # Aliases - multiple names for same value
    WAITING = 3
    ON_HOLD = 3

# Aliases are hidden in iteration
for status in Status:
    print(status)
# Output: Status.ACTIVE, Status.INACTIVE, Status.PENDING

# Access by alias
print(Status.WAITING)           # Status.PENDING (canonical member)
print(Status.WAITING.name)      # 'PENDING'
print(Status.WAITING == Status.PENDING)  # True

# Canonical and aliases have same object
print(Status.PENDING is Status.WAITING)  # True
```

!!! note "Aliases Share Identity"

    Aliases are not copies — they are the **exact same object**. `Status.WAITING is Status.PENDING` is `True` because they share identity, not just equality. This means aliases don't appear in iteration (only the canonical name does), and any method called on an alias behaves identically to the original member.

## Conditional Access

```python
from enum import Enum

class PaymentMethod(Enum):
    CREDIT_CARD = "cc"
    DEBIT_CARD = "dc"
    BANK_TRANSFER = "bt"
    PAYPAL = "pp"
    CRYPTOCURRENCY = "crypto"

def get_fee_percentage(method: PaymentMethod) -> float:
    fee_map = {
        PaymentMethod.CREDIT_CARD: 2.9,
        PaymentMethod.DEBIT_CARD: 0.5,
        PaymentMethod.BANK_TRANSFER: 0.0,
        PaymentMethod.PAYPAL: 3.49,
        PaymentMethod.CRYPTOCURRENCY: 1.0
    }
    return fee_map.get(method, 0)

fee = get_fee_percentage(PaymentMethod.CREDIT_CARD)
print(f"Fee: {fee}%")
```

## Serialization

```python
from enum import Enum
import json

class Color(Enum):
    RED = "#FF0000"
    GREEN = "#00FF00"
    BLUE = "#0000FF"

# Serialize by value
color = Color.RED
json_str = json.dumps({'color': color.value})
print(json_str)  # {'color': '#FF0000'}

# Deserialize back
data = json.loads(json_str)
restored_color = Color(data['color'])
print(restored_color)  # Color.RED
```

## Safe Member Access

```python
from enum import Enum

class Status(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"

def safe_get_status(value: str) -> Status:
    try:
        return Status(value)
    except ValueError:
        return Status.PENDING  # Default

status = safe_get_status("unknown")
print(status)  # Status.PENDING
```

---

## Exercises

**Exercise 1.**
Create a `Planet` enum with members and tuple values containing `(mass, radius)`. Access a planet's mass and radius via `planet.value[0]` and `planet.value[1]`. Write a function `heaviest(planets)` that returns the planet with the greatest mass from a list of `Planet` members.

??? success "Solution to Exercise 1"

        from enum import Enum

        class Planet(Enum):
            MERCURY = (3.303e+23, 2.4397e6)
            VENUS = (4.869e+24, 6.0518e6)
            EARTH = (5.976e+24, 6.37814e6)
            MARS = (6.421e+23, 3.3972e6)

        earth = Planet.EARTH
        print(f"Mass: {earth.value[0]:.2e}")    # Mass: 5.98e+24
        print(f"Radius: {earth.value[1]:.2e}")  # Radius: 6.38e+06

        def heaviest(planets):
            return max(planets, key=lambda p: p.value[0])

        print(heaviest(list(Planet)))  # Planet.EARTH

---

**Exercise 2.**
Define a `Status` enum with an alias: `ACTIVE = 1`, `ENABLED = 1` (alias), `INACTIVE = 2`, `DISABLED = 2` (alias). Show how to iterate over only canonical members (using `Status.__members__`) vs all members. Demonstrate that `Status.ACTIVE is Status.ENABLED`.

??? success "Solution to Exercise 2"

        from enum import Enum

        class Status(Enum):
            ACTIVE = 1
            ENABLED = 1   # Alias for ACTIVE
            INACTIVE = 2
            DISABLED = 2  # Alias for INACTIVE

        # Canonical members only (no aliases)
        for s in Status:
            print(s.name, s.value)
        # ACTIVE 1, INACTIVE 2

        # All members including aliases
        for name, member in Status.__members__.items():
            print(f"{name} -> {member.name}")
        # ACTIVE -> ACTIVE, ENABLED -> ACTIVE, ...

        print(Status.ACTIVE is Status.ENABLED)  # True

---

**Exercise 3.**
Create a `Currency` enum with values as 3-letter codes. Write a `from_value(value)` class method that converts a string value to the enum member (using `Currency(value)`). Handle invalid values by raising `ValueError` with a helpful message listing all valid values.

??? success "Solution to Exercise 3"

        from enum import Enum

        class Currency(Enum):
            USD = "USD"
            EUR = "EUR"
            GBP = "GBP"
            JPY = "JPY"

            @classmethod
            def from_value(cls, value):
                try:
                    return cls(value)
                except ValueError:
                    valid = [m.value for m in cls]
                    raise ValueError(f"Invalid currency '{value}'. Valid: {valid}")

        print(Currency.from_value("EUR"))  # Currency.EUR

        try:
            Currency.from_value("XYZ")
        except ValueError as e:
            print(f"Error: {e}")

---

**Exercise 4.**
Explain the difference between iterating over an enum class directly (`for s in Status`) and iterating over `Status.__members__.items()`. Create a `Status` enum with aliases (`ENABLED = 1`, `ACTIVE = 1`, `DISABLED = 2`, `INACTIVE = 2`) and show the output of both iteration approaches. Why does Python hide aliases from the default iterator?

??? success "Solution to Exercise 4"

        from enum import Enum

        class Status(Enum):
            ENABLED = 1
            ACTIVE = 1    # alias for ENABLED
            DISABLED = 2
            INACTIVE = 2  # alias for DISABLED

        # Default iteration — canonical members only
        print("Default iteration:")
        for s in Status:
            print(f"  {s.name} = {s.value}")
        # ENABLED = 1
        # DISABLED = 2

        # __members__ — includes aliases
        print("\n__members__ iteration:")
        for name, member in Status.__members__.items():
            canonical = "alias" if name != member.name else "canonical"
            print(f"  {name} -> {member.name} ({canonical})")
        # ENABLED -> ENABLED (canonical)
        # ACTIVE -> ENABLED (alias)
        # DISABLED -> DISABLED (canonical)
        # INACTIVE -> DISABLED (alias)

    Python hides aliases from the default iterator to prevent duplicate processing. When you iterate to build a menu, populate a dropdown, or map values, you typically want each *distinct value* once — not multiple names pointing to the same member. The `__members__` dict is available when you explicitly need to see aliases (e.g., for documentation or migration tools).

---

**Exercise 5.**
Write a generic function `enum_to_dict(enum_class)` that takes any `Enum` subclass and returns a dictionary mapping member names to values. Then write the reverse: `dict_to_enum(name, mapping)` that dynamically creates an `Enum` class from a dictionary using the functional API (`Enum(name, mapping)`). Demonstrate round-tripping: create an enum, convert to dict, recreate from dict, and verify the members match.

??? success "Solution to Exercise 5"

        from enum import Enum

        def enum_to_dict(enum_class):
            return {member.name: member.value for member in enum_class}

        def dict_to_enum(name, mapping):
            return Enum(name, mapping)

        # Original enum
        class Color(Enum):
            RED = 1
            GREEN = 2
            BLUE = 3

        # Convert to dict
        color_dict = enum_to_dict(Color)
        print(color_dict)  # {'RED': 1, 'GREEN': 2, 'BLUE': 3}

        # Recreate from dict
        Color2 = dict_to_enum("Color2", color_dict)

        # Verify members match
        for member in Color2:
            original = Color[member.name]
            print(f"{member.name}: {member.value} == {original.value} -> {member.value == original.value}")
        # RED: 1 == 1 -> True
        # GREEN: 2 == 2 -> True
        # BLUE: 3 == 3 -> True

    Note: `Color2.RED is not Color.RED` — they are different enum classes with the same names and values. The functional API `Enum(name, mapping)` is useful for creating enums from external data (configuration files, database schemas), but the resulting classes are not interchangeable with statically defined ones.
