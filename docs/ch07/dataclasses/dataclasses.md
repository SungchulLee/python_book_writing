# dataclasses

The `dataclasses` module (Python 3.7+) automatically generates boilerplate code for classes that primarily store data. It reduces repetitive `__init__`, `__repr__`, `__eq__`, and other methods.

!!! tip "Dataclass Design Workflow"
    ```text
    1. Start with @dataclass
    2. Decide mutability     → immutable? add frozen=True
    3. Handle defaults       → mutable default? use field(default_factory=...)
    4. Add validation        → use __post_init__
    5. Need performance?     → add slots=True
    6. Need API safety?      → add kw_only=True
    7. Complex validation?   → consider attrs or pydantic instead
    ```

```python
from dataclasses import dataclass, field
```

---

## The Problem: Boilerplate

Without dataclasses, simple data containers require lots of repetitive code:

```python
# Traditional approach - verbose!
class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, z={self.z})"
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
```

---

## The Solution: @dataclass

!!! note "Mental Model"
    Think of a dataclass as **fields + generated methods + optional constraints**.
    You declare the data; the decorator writes the boilerplate. Every other feature
    (`frozen`, `order`, `slots`, `field()`, `__post_init__`) layers on top of this
    core idea.

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0

# All of this is auto-generated:
p = Point(1.0, 2.0)
print(p)              # Point(x=1.0, y=2.0, z=0.0)
print(p == Point(1.0, 2.0))  # True
```

---

## Basic Usage

### Defining Fields

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int
    email: str = ""  # Default value

# Positional or keyword arguments
p1 = Person("Alice", 30)
p2 = Person(name="Bob", age=25, email="bob@example.com")

print(p1)  # Person(name='Alice', age=30, email='')
```

### Type Hints are Required

```python
@dataclass
class Item:
    name: str        # Required
    price: float     # Required
    quantity: int = 1  # Optional with default
    
    # Without type hint - NOT a field!
    category = "general"  # Class attribute, not instance field
```

### Field Ordering

Fields with defaults must come after fields without defaults:

```python
@dataclass
class Product:
    name: str          # No default - must be first
    id: int            # No default
    price: float = 0.0  # Has default - must be after
    stock: int = 0      # Has default
```

---

## Decorator Parameters

```python
@dataclass(
    init=True,       # Generate __init__
    repr=True,       # Generate __repr__
    eq=True,         # Generate __eq__
    order=False,     # Generate __lt__, __le__, __gt__, __ge__
    unsafe_hash=False,  # Force __hash__ generation
    frozen=False,    # Make instances immutable
    match_args=True, # Enable pattern matching (3.10+)
    kw_only=False,   # All fields keyword-only (3.10+)
    slots=False,     # Use __slots__ (3.10+)
)
class MyClass:
    ...
```

### Common Configurations

```python
# Immutable (like a named tuple)
@dataclass(frozen=True)
class ImmutablePoint:
    x: float
    y: float

p = ImmutablePoint(1.0, 2.0)
# p.x = 3.0  # FrozenInstanceError!

# Sortable
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int = 0

versions = [Version(2, 0), Version(1, 5), Version(1, 10)]
print(sorted(versions))
# [Version(major=1, minor=5, patch=0), Version(major=1, minor=10, patch=0), ...]

# Memory efficient (Python 3.10+)
@dataclass(slots=True)
class EfficientPoint:
    x: float
    y: float
```

---

## The field() Function

For advanced field configuration:

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    name: str
    tags: list = field(default_factory=list)  # Mutable default
    _id: int = field(default=0, repr=False)   # Hidden from repr
    computed: str = field(init=False)          # Not in __init__
    
    def __post_init__(self):
        self.computed = f"{self.name}-{self._id}"
```

### field() Parameters

| Parameter | Description |
|-----------|-------------|
| `default` | Default value (for immutables) |
| `default_factory` | Callable for mutable defaults |
| `repr` | Include in `__repr__` |
| `hash` | Include in `__hash__` |
| `compare` | Include in comparisons |
| `init` | Include in `__init__` |
| `kw_only` | Keyword-only argument (3.10+) |

### Mutable Default Values

**Never use mutable defaults directly!**

```python
# ✗ WRONG - shared mutable default
@dataclass
class Bad:
    items: list = []  # All instances share same list!

# ✓ CORRECT - factory function
@dataclass
class Good:
    items: list = field(default_factory=list)
```

---

## __post_init__

Called after `__init__` for additional initialization:

```python
from dataclasses import dataclass, field

@dataclass
class Rectangle:
    width: float
    height: float
    area: float = field(init=False)
    
    def __post_init__(self):
        self.area = self.width * self.height

r = Rectangle(5, 10)
print(r.area)  # 50.0
```

### Validation in __post_init__

```python
@dataclass
class Person:
    name: str
    age: int
    
    def __post_init__(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")
        if not self.name:
            raise ValueError("Name cannot be empty")
```

---

## Inheritance

```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str
    age: int

@dataclass
class Dog(Animal):
    breed: str
    
dog = Dog("Buddy", 3, "Labrador")
print(dog)  # Dog(name='Buddy', age=3, breed='Labrador')
```

### Field Ordering with Inheritance

```python
@dataclass
class Base:
    x: int
    y: int = 0  # Has default

@dataclass
class Child(Base):
    z: int  # No default - ERROR! Would come after y
    
# Fix: Give z a default too
@dataclass
class Child(Base):
    z: int = 0  # Now valid
```

---

## Conversion Methods

### asdict() and astuple()

```python
from dataclasses import dataclass, asdict, astuple

@dataclass
class Point:
    x: float
    y: float
    z: float = 0.0

p = Point(1.0, 2.0, 3.0)

# Convert to dict
d = asdict(p)
print(d)  # {'x': 1.0, 'y': 2.0, 'z': 3.0}

# Convert to tuple
t = astuple(p)
print(t)  # (1.0, 2.0, 3.0)
```

### Nested Dataclasses

```python
@dataclass
class Address:
    city: str
    zip_code: str

@dataclass
class Person:
    name: str
    address: Address

p = Person("Alice", Address("NYC", "10001"))

# asdict converts nested dataclasses too
d = asdict(p)
print(d)
# {'name': 'Alice', 'address': {'city': 'NYC', 'zip_code': '10001'}}
```

---

## Practical Examples

### Configuration Object

```python
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "mydb"
    user: str = "admin"
    password: str = field(default="", repr=False)  # Hide password
    pool_size: int = 5
    
    @property
    def connection_string(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
```

### API Response Model

```python
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    roles: List[str] = field(default_factory=list)
    profile: Optional[dict] = None

# JSON-like creation
user = User(
    id=1,
    username="alice",
    email="alice@example.com",
    roles=["admin", "user"]
)
```

### Immutable Value Object

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "USD"
    
    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)

m1 = Money(100, "USD")
m2 = Money(50, "USD")
m3 = m1 + m2  # Money(amount=150, currency='USD')

# Can be used in sets and as dict keys (hashable)
prices = {Money(100, "USD"), Money(200, "EUR")}
```

### With Validation

```python
from dataclasses import dataclass, field

@dataclass
class Email:
    address: str
    
    def __post_init__(self):
        if "@" not in self.address:
            raise ValueError(f"Invalid email: {self.address}")

@dataclass
class User:
    name: str
    email: Email
    age: int = field(default=0)
    
    def __post_init__(self):
        if isinstance(self.email, str):
            self.email = Email(self.email)  # Auto-convert
        if self.age < 0:
            raise ValueError("Age cannot be negative")
```

---

## Comparison with Alternatives

| Feature | dataclass | NamedTuple | Regular Class |
|---------|-----------|------------|---------------|
| Mutable | ✓ (default) | ✗ | ✓ |
| Type hints | Required | Optional | Optional |
| Inheritance | ✓ | Limited | ✓ |
| Default values | ✓ | ✓ | ✓ |
| Methods | ✓ | ✓ | ✓ |
| `__slots__` | ✓ (3.10+) | Automatic | Manual |
| Memory | Normal | Efficient | Normal |
| Boilerplate | Minimal | Minimal | High |

---

## Summary

| Feature | Syntax |
|---------|--------|
| Basic dataclass | `@dataclass` |
| Immutable | `@dataclass(frozen=True)` |
| Sortable | `@dataclass(order=True)` |
| With slots | `@dataclass(slots=True)` |
| Mutable default | `field(default_factory=list)` |
| Hidden from repr | `field(repr=False)` |
| Not in __init__ | `field(init=False)` |
| Post-init logic | `def __post_init__(self)` |
| To dict | `asdict(instance)` |
| To tuple | `astuple(instance)` |

**Key Takeaways**:

- Use `@dataclass` for classes that primarily store data
- Type hints are required for all fields
- Use `field(default_factory=...)` for mutable defaults (lists, dicts)
- Use `frozen=True` for immutable objects (hashable, safe)
- Use `__post_init__` for validation and computed fields
- Python 3.10+ adds `slots=True` for memory efficiency
- `asdict()` and `astuple()` for easy serialization

!!! warning "Common Mistakes"

    - **Mutable defaults**: Writing `items: list = []` shares one list across all
      instances. Always use `field(default_factory=list)`.
    - **Forgetting field ordering**: Fields with defaults must come after fields
      without defaults — this also applies across inheritance hierarchies.
    - **Assuming `frozen` means deeply immutable**: A frozen dataclass prevents
      reassignment of its fields, but mutable objects inside those fields (lists,
      dicts) can still be modified in place.

---

## Runnable Example: `dataclass_basics_tutorial.py`

```python
"""
TUTORIAL: Dataclass Basics - @dataclass Decorator with Ordering Support
========================================================================

In this tutorial, you'll learn how to use the @dataclass decorator to create
simple data-holding classes automatically. We'll explore the @dataclass(order=True)
parameter which automatically generates comparison methods like __lt__, __le__,
__gt__, and __ge__.

Why use @dataclass? Before dataclasses, you had to manually write __init__,
__repr__, __eq__, and other methods. Dataclasses generate these for you,
reducing boilerplate while keeping code readable and maintainable.

The order=True parameter is particularly useful when you need to sort instances
or compare them using <, <=, >, >= operators. Without it, you'd get a TypeError
when trying to compare instances.
"""

from dataclasses import dataclass


# ============ Example 1: Basic Dataclass with Ordering ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Creating a Card dataclass with order=True")
    print("=" * 70)

    @dataclass(order=True)
    class Card:
        """A playing card with rank and suit.

        The order=True parameter tells @dataclass to generate comparison methods.
        Python will compare cards by rank first, then by suit (in the order you
        define the fields). This makes it easy to sort cards programmatically.
        """
        rank: str
        suit: str

        # Class attributes (not dataclass fields since they lack type hints)
        ranks = [str(n) for n in range(2, 10)] + list('JQKA')
        suits = 'spades diamonds clubs hearts'.split()


    # Create some card instances
    card1 = Card('2', 'spades')
    card2 = Card('K', 'hearts')
    card3 = Card('5', 'clubs')

    print(f"\nCards created:")
    print(f"  card1 = {card1}")
    print(f"  card2 = {card2}")
    print(f"  card3 = {card3}")

    # Demonstrate automatic __repr__ (generated by @dataclass)
    print(f"\nAutomatic __repr__ (generated by @dataclass):")
    print(f"  repr(card1) = {repr(card1)}")


    # ============ Example 2: Comparison Operations ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Comparing cards using order=True")
    print("=" * 70)

    # The order=True parameter generates these comparison methods
    print(f"\nComparison results (comparing cards by rank first, then suit):")
    print(f"  Card('2', 'spades') < Card('K', 'hearts'): {card1 < card2}")
    print(f"    WHY? '2' comes before 'K' in the ranks list")

    print(f"\n  Card('5', 'clubs') > Card('2', 'spades'): {card3 > card1}")
    print(f"    WHY? '5' comes after '2' in the ranks list")

    # These operators would fail without order=True
    print(f"\n  Card('2', 'spades') <= Card('2', 'spades'): {card1 <= Card('2', 'spades')}")
    print(f"    WHY? Equality is also generated by @dataclass")


    # ============ Example 3: Sorting Cards ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Sorting cards using the generated comparison methods")
    print("=" * 70)

    cards = [
        Card('K', 'hearts'),
        Card('2', 'spades'),
        Card('5', 'clubs'),
        Card('A', 'diamonds'),
        Card('5', 'hearts'),
    ]

    print(f"\nUnsorted cards:")
    for card in cards:
        print(f"  {card}")

    sorted_cards = sorted(cards)

    print(f"\nSorted cards (order=True generates the comparison logic):")
    for card in sorted_cards:
        print(f"  {card}")

    print(f"\nWhy this order? Fields are compared left to right:")
    print(f"  First by rank: 2 < 5 < 5 < A < K")
    print(f"  For ties (5 = 5), then by suit: clubs < hearts")


    # ============ Example 4: Class Attributes vs Instance Attributes ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Understanding class vs instance attributes")
    print("=" * 70)

    print(f"\nClass attributes (shared across all instances):")
    print(f"  Card.ranks = {Card.ranks}")
    print(f"  Card.suits = {Card.suits}")

    print(f"\nInstance attributes (unique to each instance):")
    print(f"  card1.rank = '{card1.rank}', card1.suit = '{card1.suit}'")
    print(f"  card2.rank = '{card2.rank}', card2.suit = '{card2.suit}'")

    print(f"\nWhy separate them?")
    print(f"  - Dataclass fields (with type hints) → instance attributes")
    print(f"  - Class-level assignments without type hints → class attributes")
    print(f"  - This keeps your code clear and prevents accidental mutations")


    # ============ Example 5: What @dataclass(order=True) Generates ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Behind the scenes - what @dataclass generates")
    print("=" * 70)

    print(f"\nThe @dataclass decorator automatically creates:")
    print(f"  1. __init__() - initializes rank and suit from arguments")
    print(f"  2. __repr__() - shows Card(rank='K', suit='hearts')")
    print(f"  3. __eq__() - checks if two cards are identical")
    print(f"  4. __lt__() - checks if one card < another (order=True)")
    print(f"  5. __le__() - checks if one card <= another (order=True)")
    print(f"  6. __gt__() - checks if one card > another (order=True)")
    print(f"  7. __ge__() - checks if one card >= another (order=True)")

    print(f"\nWithout @dataclass, you'd write all of this manually!")
    print(f"Without order=True, comparison methods wouldn't exist.")

    print(f"\n" + "=" * 70)
```

---

## Exercises

**Exercise 1.**
Create a `Book` dataclass with fields `title` (str), `author` (str), `pages` (int), and `price` (float with default `9.99`). Create several instances, print them (using the auto-generated `__repr__`), and test equality between two books with identical fields.

??? success "Solution to Exercise 1"

        from dataclasses import dataclass

        @dataclass
        class Book:
            title: str
            author: str
            pages: int
            price: float = 9.99

        b1 = Book("Python 101", "Author A", 300)
        b2 = Book("Python 101", "Author A", 300)
        b3 = Book("Data Science", "Author B", 450, 29.99)

        print(b1)  # Book(title='Python 101', author='Author A', pages=300, price=9.99)
        print(b1 == b2)  # True — auto-generated __eq__
        print(b1 == b3)  # False

---

**Exercise 2.**
Define a `Temperature` dataclass with a single field `celsius` (float). Add a method `to_fahrenheit()` that returns the converted value. Use `order=True` so temperatures can be sorted. Create a list of temperatures and sort them.

??? success "Solution to Exercise 2"

        from dataclasses import dataclass

        @dataclass(order=True)
        class Temperature:
            celsius: float

            def to_fahrenheit(self):
                return self.celsius * 9 / 5 + 32

        temps = [Temperature(100), Temperature(0), Temperature(37), Temperature(-40)]
        print(sorted(temps))
        # [Temperature(celsius=-40), Temperature(celsius=0),
        #  Temperature(celsius=37), Temperature(celsius=100)]

        for t in sorted(temps):
            print(f"{t.celsius}C = {t.to_fahrenheit()}F")

---

**Exercise 3.**
Build an `Inventory` dataclass with fields `item_name` (str), `quantity` (int, default `0`), and `unit_price` (float, default `0.0`). Add a `total_value` property that returns `quantity * unit_price`. Create several inventory items, calculate total values, and find the most valuable item using `max()` with a key function.

??? success "Solution to Exercise 3"

        from dataclasses import dataclass

        @dataclass
        class Inventory:
            item_name: str
            quantity: int = 0
            unit_price: float = 0.0

            @property
            def total_value(self):
                return self.quantity * self.unit_price

        items = [
            Inventory("Widget", 100, 2.50),
            Inventory("Gadget", 50, 15.00),
            Inventory("Doohickey", 200, 1.25),
        ]

        for item in items:
            print(f"{item.item_name}: ${item.total_value:.2f}")
        # Widget: $250.00, Gadget: $750.00, Doohickey: $250.00

        most_valuable = max(items, key=lambda i: i.total_value)
        print(f"Most valuable: {most_valuable.item_name}")
