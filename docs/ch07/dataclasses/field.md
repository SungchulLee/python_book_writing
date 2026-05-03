# field() Function

The `field()` function provides fine-grained control over how individual fields are handled in dataclasses, including default values, factory functions, and metadata.

!!! tip "Mental Model"
    If `@dataclass` is the architect drawing the blueprint, `field()` is the fine print on each room's spec sheet. It lets you say "this room has a default size", "this room is not shown on the tour", or "this room builds its own furniture on move-in" -- per-field customization that the decorator alone cannot express.

!!! tip "Quick Guide — when to reach for each parameter"
    | Parameter | Use when |
    |-----------|----------|
    | `default_factory` | Mutable defaults (lists, dicts, sets) |
    | `compare=False` | Cache fields, internal state that should not affect equality |
    | `repr=False` | Secrets (passwords, tokens) or noisy fields (large data) |
    | `init=False` | Derived/computed fields set in `__post_init__` |
    | `kw_only=True` | Preventing positional-argument mix-ups on a per-field basis |
    | `metadata` | Serialization hints, ORM column mapping, documentation |

---

## Basic field() Usage

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class Person:
    name: str
    age: int = field(default=0)  # With default
    hobbies: List[str] = field(default_factory=list)  # Mutable default

person1 = Person("Alice")
person2 = Person("Bob", age=30)
person3 = Person("Charlie", age=25, hobbies=["reading"])

print(person1)  # Person(name='Alice', age=0, hobbies=[])
print(person2)  # Person(name='Bob', age=30, hobbies=[])
```

## default_factory for Mutable Objects

```python
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Config:
    name: str
    options: Dict[str, int] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

config1 = Config("api")
config2 = Config("database")

# Each gets its own dictionary and list
config1.options['timeout'] = 30
config1.tags.append('important')

print(config1)  # Config(name='api', options={'timeout': 30}, tags=['important'])
print(config2)  # Config(name='database', options={}, tags=[])
```

## Field Metadata and Exclusion

```python
from dataclasses import dataclass, field, asdict

@dataclass
class User:
    name: str
    password: str = field(repr=False)  # Don't show in repr
    email: str = field(compare=False)  # Don't use in comparisons

user1 = User("alice", "secret123", "alice@example.com")
user2 = User("alice", "different", "alice@different.com")

print(user1)           # User(name='alice', email='alice@example.com')
print(user1 == user2)  # True (email not compared, password excluded)
```

## Custom Metadata

Metadata is an arbitrary mapping attached to a field. The dataclass machinery itself ignores
it, but external tools read it — serialization libraries use metadata to map field names to
JSON keys or database columns, and ORM layers use it for column constraints.

```python
from dataclasses import dataclass, field, fields

@dataclass
class Product:
    name: str = field(metadata={'description': 'Product name'})
    price: float = field(metadata={'currency': 'USD', 'min': 0.0})
    quantity: int = field(default=0, metadata={'unit': 'items'})

# Access metadata
for f in fields(Product):
    print(f"{f.name}: {f.metadata}")
```

In a real serialization framework, metadata might drive JSON key renaming:

```python
@dataclass
class APIUser:
    user_name: str = field(metadata={"json": "userName"})
    email_addr: str = field(metadata={"json": "email"})
```

## Initialization Order and Init

```python
from dataclasses import dataclass, field

@dataclass
class Example:
    required: str
    optional: str = field(default="default_value")
    # Fields with init=False aren't included in __init__
    computed: str = field(init=False)
    
    def __post_init__(self):
        self.computed = f"{self.required}_{self.optional}"

example = Example("test")
print(example)  # Example(required='test', optional='default_value', computed='test_default_value')
```

## Compare and Hash Control

!!! warning "`compare=False` can silently break equality logic"
    Excluding a field from comparisons means two instances with different values
    for that field will compare as equal. This is intentional for caches and
    internal state, but it can mask bugs if applied to semantically meaningful
    fields. Always document **why** a field is excluded.

```python
from dataclasses import dataclass, field

@dataclass
class Item:
    id: int
    name: str = field(compare=True)
    internal_state: dict = field(compare=False, repr=False)

item1 = Item(1, "widget", {})
item2 = Item(1, "widget", {'processed': True})

print(item1 == item2)  # True (internal_state not compared)
print(hash(item1))     # Works with hashable fields
```

---

## Runnable Example: `dataclass_fields_and_defaults.py`

```python
"""
TUTORIAL: Dataclass Fields and Defaults - Understanding Type Annotations
=========================================================================

In this tutorial, you'll learn the difference between three types of attributes
in a dataclass:

  1. Typed fields with no default: REQUIRED when creating instances
  2. Typed fields with default values: OPTIONAL when creating instances
  3. Class attributes without type hints: NOT dataclass fields

This distinction is crucial. Dataclasses use type hints to identify which
attributes should be instance fields managed by the generated __init__ method.
Attributes without type hints are treated as class attributes instead.

Understanding this hierarchy prevents confusing bugs where you accidentally
forget to make something a field or misunderstand why something behaves
differently than expected.
"""

from dataclasses import dataclass


# ============ Example 1: Declaring Dataclass Fields ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Three types of attributes in a dataclass")
    print("=" * 70)

    @dataclass
    class DemoDataClass:
        """Demonstrates the three ways to define attributes in a dataclass.

        Attributes:
            a (int): A required field - MUST be provided when creating an instance.
                     Has a type hint, so @dataclass treats it as an instance field.

            b (float): An optional field - Has a default value (1.1).
                       If not provided, instances will use the default.
                       @dataclass treats this as an instance field because it has
                       a type hint.

            c: NOT a dataclass field - This class attribute lacks a type hint.
               @dataclass ignores it. It's a regular class attribute shared by all
               instances, like a constant or helper attribute.
        """
        # Field 1: Required - has type hint, no default
        a: int           # <1> Required when creating instance

        # Field 2: Optional - has type hint and default value
        b: float = 1.1   # <2> Optional, defaults to 1.1

        # Not a field - no type hint, so treated as class attribute
        c = 'spam'       # <3> Class attribute, not instance field


    print(f"\nClass definition complete. Let's see what @dataclass generates:\n")


    # ============ Example 2: Creating Instances with Required Fields ============
    print("=" * 70)
    print("EXAMPLE 2: Creating instances - mixing required and optional fields")
    print("=" * 70)

    # Create instance with only required field
    instance1 = DemoDataClass(a=42)
    print(f"\ninstance1 = DemoDataClass(a=42)")
    print(f"  instance1.a = {instance1.a}")
    print(f"  instance1.b = {instance1.b}  (uses default)")
    print(f"  WHY? 'b' has default value 1.1, so it's optional")

    # Create instance with both fields
    instance2 = DemoDataClass(a=100, b=2.5)
    print(f"\ninstance2 = DemoDataClass(a=100, b=2.5)")
    print(f"  instance2.a = {instance2.a}")
    print(f"  instance2.b = {instance2.b}")

    # Try creating instance without required field
    print(f"\nAttempting: DemoDataClass(b=3.0)  # Missing required 'a'")
    try:
        broken = DemoDataClass(b=3.0)
        print(f"  ERROR: This should have failed!")
    except TypeError as e:
        print(f"  Result: TypeError: {e}")
        print(f"  WHY? 'a' has no default value, so it's required")


    # ============ Example 3: Class Attributes vs Instance Attributes ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Understanding class attribute 'c' vs instance fields")
    print("=" * 70)

    print(f"\nThe 'c' attribute is NOT an instance field:")
    print(f"  - It lacks a type hint")
    print(f"  - @dataclass ignores it")
    print(f"  - It becomes a class attribute")

    # Class attribute - shared by all instances
    print(f"\nClass attribute (shared by all instances):")
    print(f"  DemoDataClass.c = '{DemoDataClass.c}'")

    # But you can still access it through instances
    print(f"\nAccessing class attribute through instances:")
    print(f"  instance1.c = '{instance1.c}'")
    print(f"  instance2.c = '{instance2.c}'")

    print(f"\nModifying the class attribute affects ALL instances:")
    original_c = DemoDataClass.c
    DemoDataClass.c = 'eggs'
    print(f"  DemoDataClass.c = 'eggs'  # Changed class attribute")
    print(f"  instance1.c = '{instance1.c}'  (reflected immediately)")
    print(f"  instance2.c = '{instance2.c}'  (reflected immediately)")

    # Restore for clean output
    DemoDataClass.c = original_c
    print(f"  DemoDataClass.c = '{original_c}'  # Restored")

    print(f"\nWhy not make 'c' a dataclass field?")
    print(f"  - Without type hint, @dataclass doesn't know it's a field")
    print(f"  - This is intentional: class attributes are class-level constants")
    print(f"  - If you want instance field, add type hint: c: str = 'spam'")


    # ============ Example 4: Comparing with Proper Type Hints ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: What happens if we add a type hint to 'c'")
    print("=" * 70)

    @dataclass
    class ImprovedDemo:
        """Same as DemoDataClass but with 'c' as a proper typed field."""
        a: int
        b: float = 1.1
        c: str = 'spam'  # Now it has a type hint!


    instance3 = ImprovedDemo(a=50)
    print(f"\ninstance3 = ImprovedDemo(a=50)")
    print(f"  instance3.a = {instance3.a}")
    print(f"  instance3.b = {instance3.b}  (uses default 1.1)")
    print(f"  instance3.c = '{instance3.c}'  (uses default 'spam')")

    instance4 = ImprovedDemo(a=60, b=3.3, c='ham')
    print(f"\ninstance4 = ImprovedDemo(a=60, b=3.3, c='ham')")
    print(f"  instance4.a = {instance4.a}")
    print(f"  instance4.b = {instance4.b}")
    print(f"  instance4.c = '{instance4.c}'")

    print(f"\nNow 'c' is a real instance field:")
    print(f"  - Each instance has its own 'c' value")
    print(f"  - You can provide 'c' when creating instances")
    print(f"  - Changing instance4.c doesn't affect instance3.c")

    instance4.c = 'turkey'
    print(f"\ninstance4.c = 'turkey'")
    print(f"  instance4.c = '{instance4.c}'")
    print(f"  instance3.c = '{instance3.c}'  (unchanged)")


    # ============ Example 5: Generated __init__ Signature ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: The __init__ method @dataclass generates")
    print("=" * 70)

    import inspect

    print(f"\nDemoDataClass.__init__ signature:")
    sig = inspect.signature(DemoDataClass.__init__)
    print(f"  {sig}")
    print(f"\nExplanation:")
    print(f"  - self: Always first parameter")
    print(f"  - a: int - REQUIRED (no default shown)")
    print(f"  - b: float = 1.1 - OPTIONAL (default shown)")
    print(f"  - Note: 'c' is NOT in the signature (it's not a field)")

    print(f"\nImprovedDemo.__init__ signature:")
    sig2 = inspect.signature(ImprovedDemo.__init__)
    print(f"  {sig2}")
    print(f"\nNow 'c' appears in the signature because we added a type hint!")


    # ============ Example 6: Field Order Matters ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Important - fields with defaults must come after required")
    print("=" * 70)

    print(f"\nDataclass rule: Required fields must come BEFORE optional fields")
    print(f"\nThis is valid:")
    @dataclass
    class ValidOrder:
        required_field: int          # No default
        optional_field: str = 'default'  # Has default

    print(f"  class ValidOrder:")
    print(f"      required_field: int")
    print(f"      optional_field: str = 'default'")

    print(f"\nThis would be INVALID:")
    print(f"  class BadOrder:")
    print(f"      optional_field: str = 'default'  # Has default")
    print(f"      required_field: int              # No default (ERROR!)")
    print(f"\nWhy? Python's parameter rules require defaults after non-defaults")

    print(f"\n" + "=" * 70)
```

---

## Exercises

**Exercise 1.**
Create a `UserProfile` dataclass where `username` is a regular field, `tags` uses `field(default_factory=list)`, and `created_at` uses `field(default_factory=datetime.now)` (import `datetime`). Show that each instance gets its own list and timestamp. Demonstrate the mutable default problem by explaining what would happen without `default_factory`.

??? success "Solution to Exercise 1"

        from dataclasses import dataclass, field
        from datetime import datetime

        @dataclass
        class UserProfile:
            username: str
            tags: list = field(default_factory=list)
            created_at: datetime = field(default_factory=datetime.now)

        u1 = UserProfile("alice")
        u2 = UserProfile("bob")

        u1.tags.append("admin")
        print(u1.tags)  # ['admin']
        print(u2.tags)  # [] — independent list

        print(u1.created_at)
        print(u2.created_at)  # Different timestamps

        # Without default_factory, tags=[] would be shared:
        # All instances would reference the SAME list object

---

**Exercise 2.**
Define a `Product` dataclass with fields `name`, `price`, and `internal_id`. Use `field(repr=False)` on `internal_id` so it does not appear in the repr output. Add a `metadata` field using `field(metadata={"unit": "USD"})`. Print the repr and access the metadata.

??? success "Solution to Exercise 2"

        from dataclasses import dataclass, field, fields

        @dataclass
        class Product:
            name: str
            price: float
            internal_id: int = field(repr=False)
            metadata: dict = field(
                default_factory=lambda: {"unit": "USD"},
                metadata={"unit": "USD"}
            )

        p = Product("Widget", 9.99, 12345)
        print(p)  # Product(name='Widget', price=9.99, metadata={'unit': 'USD'})
        # internal_id not shown in repr

        # Access field metadata
        for f in fields(p):
            if f.metadata:
                print(f"{f.name}: metadata={f.metadata}")

---

**Exercise 3.**
Create a `Matrix` dataclass with a `rows` field (int), `cols` field (int), and `data` field that uses `field(default_factory=list, compare=False)`. The `data` field should not be used in equality comparisons. Create two matrices with the same dimensions but different data and show they compare as equal. Then create two with different dimensions and show they compare as unequal.

??? success "Solution to Exercise 3"

        from dataclasses import dataclass, field

        @dataclass
        class Matrix:
            rows: int
            cols: int
            data: list = field(default_factory=list, compare=False)

        m1 = Matrix(3, 3, [1, 2, 3])
        m2 = Matrix(3, 3, [4, 5, 6])
        m3 = Matrix(2, 4, [1, 2, 3])

        print(m1 == m2)  # True — data excluded from comparison
        print(m1 == m3)  # False — different dimensions
