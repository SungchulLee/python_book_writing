# Dataclass Inheritance

Dataclasses support inheritance with automatic handling of parent and child fields. Understanding field ordering rules is important.

!!! tip "Mental Model"
    When a child dataclass inherits from a parent, Python concatenates the parent's fields before the child's fields to build `__init__`. This means a parent field with a default followed by a child field without one creates an illegal signature (positional after keyword). Think of it as stacking cards: the parent's cards go on the bottom, the child's on top, and the resulting deck must follow Python's argument-ordering rules.

---

## Basic Inheritance

```python
from dataclasses import dataclass

@dataclass
class Animal:
    name: str
    age: int

@dataclass
class Dog(Animal):
    breed: str

dog = Dog("Buddy", 3, "Golden Retriever")
print(dog)  # Dog(name='Buddy', age=3, breed='Golden Retriever')
```

## Field Ordering in Inheritance

```python
from dataclasses import dataclass, field

@dataclass
class Base:
    x: int
    y: int = 10

# Fields with defaults must come after fields without defaults
@dataclass
class Derived(Base):
    z: int = 20  # Must have default since parent has default field

derived = Derived(1)
print(derived)  # Derived(x=1, y=10, z=20)

# This would fail: fields without defaults after those with defaults
# @dataclass
# class BadDerived(Base):
#     z: int  # Error: non-default field after default field
```

## Overriding Parent Fields

```python
from dataclasses import dataclass, field

@dataclass
class Vehicle:
    wheels: int = 4
    color: str = "white"

@dataclass
class Car(Vehicle):
    # Override with different default
    wheels: int = 4  # Explicitly set
    color: str = "silver"  # Different default
    doors: int = 4

car = Car()
print(car)  # Car(wheels=4, color='silver', doors=4)
```

## Multiple Inheritance

```python
from dataclasses import dataclass

@dataclass
class TimestampMixin:
    created_at: str = "2024-01-01"

@dataclass
class NameMixin:
    name: str

@dataclass
class Document(NameMixin, TimestampMixin):
    content: str = ""

doc = Document(name="Report", content="Summary")
print(doc)  # Document(name='Report', created_at='2024-01-01', content='Summary')
```

## Initialization Behavior

```python
from dataclasses import dataclass

@dataclass
class Parent:
    x: int
    
    def __post_init__(self):
        print(f"Parent init: x={self.x}")

@dataclass
class Child(Parent):
    y: int = 0
    
    def __post_init__(self):
        super().__post_init__()  # Call parent
        print(f"Child init: y={self.y}")

child = Child(1, 2)
# Output:
# Parent init: x=1
# Child init: y=2
```

## Inheritance with Mutable Defaults

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class BaseCollection:
    items: List[str] = field(default_factory=list)

@dataclass
class ExtendedCollection(BaseCollection):
    metadata: dict = field(default_factory=dict)

col1 = ExtendedCollection()
col2 = ExtendedCollection()

col1.items.append("item1")
col1.metadata['type'] = 'test'

print(col1)  # ExtendedCollection(items=['item1'], metadata={'type': 'test'})
print(col2)  # ExtendedCollection(items=[], metadata={})  # Independent
```

## Best Practices

- Keep parent dataclasses simple
- Place required fields in parent, optional in child
- Call `super().__post_init__()` when overriding
- Consider composition over inheritance for complex cases

!!! warning "Dataclass inheritance is convenient but brittle"
    Keep hierarchies shallow (one level of inheritance is ideal). Beyond two levels,
    field ordering constraints compound, defaults become hard to manage, and
    `__post_init__` chaining grows fragile. If you find yourself fighting the
    framework, flatten the hierarchy or switch to composition.

!!! tip "When NOT to use inheritance"
    Dataclass inheritance works well for shallow, "is-a" hierarchies (e.g., `Dog`
    is an `Animal`). Prefer **composition** when:

    - Behavior differs significantly between parent and child — you end up
      overriding most methods, defeating the purpose of reuse.
    - The hierarchy grows deeper than two levels — field ordering constraints
      compound and defaults become hard to manage.
    - You need to mix capabilities from multiple unrelated sources — multiple
      inheritance with dataclasses can produce surprising MRO and field-order issues.

    ```python
    # Composition instead of deep inheritance
    @dataclass
    class Engine:
        horsepower: int
        fuel_type: str

    @dataclass
    class Car:
        make: str
        engine: Engine  # has-a, not is-a
    ```

---

## Exercises

**Exercise 1.**
Create a parent dataclass `Vehicle` with fields `make` (str) and `year` (int). Create a child dataclass `Car` that adds `doors` (int, default `4`) and `electric` (bool, default `False`). Create instances of both and print them. Show that `Car` inherits fields from `Vehicle`.

??? success "Solution to Exercise 1"

        from dataclasses import dataclass

        @dataclass
        class Vehicle:
            make: str
            year: int

        @dataclass
        class Car(Vehicle):
            doors: int = 4
            electric: bool = False

        v = Vehicle("Toyota", 2023)
        c = Car("Tesla", 2024, doors=4, electric=True)

        print(v)  # Vehicle(make='Toyota', year=2023)
        print(c)  # Car(make='Tesla', year=2024, doors=4, electric=True)
        print(c.make)  # Tesla — inherited from Vehicle

---

**Exercise 2.**
Define a base dataclass `Shape` with a `color` field (str, default `"black"`). Create child dataclasses `Circle` (adds `radius`) and `Rectangle` (adds `width` and `height`). Add `area()` methods to each child. Be careful with field ordering: required fields must come before fields with defaults. Show a working solution.

??? success "Solution to Exercise 2"

        from dataclasses import dataclass
        import math

        @dataclass
        class Shape:
            color: str = "black"

        @dataclass
        class Circle(Shape):
            radius: float = 1.0  # Must have default (parent has default)

            def area(self):
                return math.pi * self.radius ** 2

        @dataclass
        class Rectangle(Shape):
            width: float = 1.0
            height: float = 1.0

            def area(self):
                return self.width * self.height

        c = Circle(color="red", radius=5)
        r = Rectangle(color="blue", width=3, height=4)

        print(f"{c} -> area={c.area():.2f}")
        # Circle(color='red', radius=5) -> area=78.54
        print(f"{r} -> area={r.area():.2f}")
        # Rectangle(color='blue', width=3, height=4) -> area=12.00

---

**Exercise 3.**
Create a parent dataclass `Employee` with `name` (str) and `department` (str). Create a child `Manager` that adds `team_size` (int) and overrides `__post_init__` to validate that `team_size` is positive (calling `super().__post_init__()` if the parent has one). Demonstrate that creating a `Manager` with `team_size=0` raises a `ValueError`.

??? success "Solution to Exercise 3"

        from dataclasses import dataclass

        @dataclass
        class Employee:
            name: str
            department: str

            def __post_init__(self):
                if not self.name:
                    raise ValueError("Name cannot be empty")

        @dataclass
        class Manager(Employee):
            team_size: int = 1

            def __post_init__(self):
                super().__post_init__()
                if self.team_size <= 0:
                    raise ValueError(f"team_size must be positive, got {self.team_size}")

        m = Manager("Alice", "Engineering", team_size=5)
        print(m)  # Manager(name='Alice', department='Engineering', team_size=5)

        try:
            bad = Manager("Bob", "Sales", team_size=0)
        except ValueError as e:
            print(f"Error: {e}")
            # Error: team_size must be positive, got 0
