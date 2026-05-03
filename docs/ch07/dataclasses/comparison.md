# Dataclass vs NamedTuple vs attrs

Python offers multiple ways to create structured data classes — `dataclass`, `NamedTuple`, and `attrs` — each with distinct tradeoffs around mutability, performance, and validation. Choosing the right one depends on whether your data needs to change after creation, how many instances you will create, and whether you need built-in validation.

!!! tip "Mental Model"
    Picture three containers: `NamedTuple` is a sealed envelope (immutable, lightweight, tuple-compatible), `dataclass` is a labeled box (mutable by default, standard-library, no dependencies), and `attrs` is a box with a built-in inspector (validation, converters, slots by default). Pick the container whose built-in constraints match your data's requirements.

---

## Dataclasses

```python
from dataclasses import dataclass

@dataclass
class PersonDataclass:
    name: str
    age: int
    city: str = "Unknown"

person = PersonDataclass("Alice", 30)
person.age = 31  # Mutable
print(person)    # PersonDataclass(name='Alice', age=31, city='Unknown')
```

## NamedTuple

```python
from typing import NamedTuple

class PersonNamedTuple(NamedTuple):
    name: str
    age: int
    city: str = "Unknown"

person = PersonNamedTuple("Bob", 25)
print(person)       # PersonNamedTuple(name='Bob', age=25, city='Unknown')
print(person[0])    # 'Bob' (tuple indexing works)
# person.age = 26   # Error: immutable
```

## attrs Library

```python
# pip install attrs
import attrs

@attrs.define
class PersonAttrs:
    name: str
    age: int
    city: str = "Unknown"

person = PersonAttrs("Charlie", 28)
person.age = 29  # Mutable
print(person)    # PersonAttrs(name='Charlie', age=29, city='Unknown')
```

## Comparison

```python
from dataclasses import dataclass
from typing import NamedTuple

@dataclass
class DataclassPerson:
    name: str
    age: int = 0

class NamedTuplePerson(NamedTuple):
    name: str
    age: int = 0

# Mutability
dc_person = DataclassPerson("Alice")
dc_person.age = 30  # Works

nt_person = NamedTuplePerson("Bob")
# nt_person.age = 30  # Error

# Tuple unpacking (NamedTuple only)
name, age = nt_person
print(f"{name}: {age}")

# Hashing
dc_frozen = DataclassPerson("Charlie")
dc_dict = {dc_frozen: "value"}  # Error without frozen=True

nt_dict = {nt_person: "value"}  # Works automatically
```

## Performance Comparison

```python
import timeit
from dataclasses import dataclass
from typing import NamedTuple

@dataclass
class DC:
    x: int
    y: int

class NT(NamedTuple):
    x: int
    y: int

# Creation time similar
# NamedTuple slightly faster for creation
# Dataclass more flexible

time_dc = timeit.timeit(lambda: DC(1, 2), number=100000)
time_nt = timeit.timeit(lambda: NT(1, 2), number=100000)

print(f"Dataclass: {time_dc:.4f}s")
print(f"NamedTuple: {time_nt:.4f}s")
```

## Decision Guide

Use this decision tree when choosing between the three approaches:

```text
Need immutability + hashing?
├── Yes, and need tuple unpacking → NamedTuple
├── Yes, but no unpacking needed  → frozen dataclass
└── No
    ├── Need built-in validation or converters → attrs
    ├── Need standard library only             → dataclass
    └── Need slots by default + validators     → attrs
```

**Dataclasses** are the right default when you need a general-purpose mutable data container
in the standard library. They become the clear winner when you need `__post_init__` hooks,
`field()` customization, or inheritance — features that NamedTuple handles poorly or not at all.

**NamedTuple** wins when you need an immutable, lightweight record that participates in tuple
protocols (indexing, unpacking, iteration). Because instances are actual tuples, they use less
memory and are hashable without configuration. The tradeoff is no mutability and limited
inheritance support.

**attrs** is the strongest choice for production models that need built-in validators,
converters, and rich field metadata. It generates `__slots__` by default (via `@attrs.define`),
provides `attrs.validators` for declarative validation, and supports `converter` arguments
that auto-coerce inputs. The tradeoff is an external dependency.

**Boundary rule**: if data crosses a system boundary (user input, API responses, config
files), prefer **pydantic** or **attrs** — they validate at the edge. If the data is
internal (passed between your own functions/classes), a plain `@dataclass` is sufficient.

```python
# attrs validator + converter example
import attrs

@attrs.define
class Temperature:
    celsius: float = attrs.field(converter=float)

    @celsius.validator
    def _check_range(self, attribute, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")

t = Temperature("36.6")   # converter coerces str → float
print(t.celsius)           # 36.6
```

---

## Runnable Example: `namedtuple_basic_example.py`

```python
"""
TUTORIAL: NamedTuple Basics - Typed Named Tuples vs Dataclasses
================================================================

In this tutorial, you'll learn about NamedTuple, Python's typed alternative
to the regular tuple. NamedTuple provides:

  - Named fields for accessing data (e.g., person.name instead of person[0])
  - Type hints for clarity and IDE support
  - Immutability (tuples cannot be modified after creation)
  - Unpacking capability (like regular tuples)
  - Smaller memory footprint than dataclasses

The main difference from @dataclass:
  - NamedTuple is immutable by default (dataclass is mutable by default)
  - NamedTuple is a tuple subclass (dataclass is not)
  - NamedTuple has smaller memory overhead
  - Dataclass offers more flexibility with the frozen= parameter

In this file, we show the basic NamedTuple syntax and compare it to the
equivalent dataclass version. Notice the three types of attributes:
  1. Typed fields with no default: REQUIRED
  2. Typed fields with defaults: OPTIONAL
  3. Class attributes without type hints: NOT fields
"""

import typing


# ============ Example 1: Basic NamedTuple Definition ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Defining a basic NamedTuple")
    print("=" * 70)

    class DemoNTClass(typing.NamedTuple):
        """A NamedTuple with three attributes following the same pattern as dataclass.

        Attributes:
            a (int): Required field - must provide when creating instances.
                     Has type hint, so it's a named tuple field.

            b (float): Optional field with default value.
                       If not provided, instances will use 1.1.
                       Has type hint, so it's a named tuple field.

            c: Class attribute without type hint.
               Not treated as a field, unlike 'a' and 'b'.
        """
        # Field 1: Required - has type hint, no default
        a: int           # <1> Required when creating instance

        # Field 2: Optional - has type hint and default value
        b: float = 1.1   # <2> Optional, defaults to 1.1

        # Not a field - no type hint, so treated as class attribute
        c = 'spam'       # <3> Class attribute, not field


    print(f"\nNamedTuple definition complete.\n")


    # ============ Example 2: Creating NamedTuple Instances ============
    print("=" * 70)
    print("EXAMPLE 2: Creating instances and accessing fields")
    print("=" * 70)

    # Create with required field only
    instance1 = DemoNTClass(42)
    print(f"\ninstance1 = DemoNTClass(42)")
    print(f"  instance1.a = {instance1.a}")
    print(f"  instance1.b = {instance1.b}  (uses default)")
    print(f"  Accessing by name: instance1.a (more readable than instance1[0])")

    # Create with both fields
    instance2 = DemoNTClass(100, 2.5)
    print(f"\ninstance2 = DemoNTClass(100, 2.5)")
    print(f"  instance2.a = {instance2.a}")
    print(f"  instance2.b = {instance2.b}")

    # Create using keyword arguments
    instance3 = DemoNTClass(a=50, b=1.5)
    print(f"\ninstance3 = DemoNTClass(a=50, b=1.5)  (using keyword arguments)")
    print(f"  instance3.a = {instance3.a}")
    print(f"  instance3.b = {instance3.b}")


    # ============ Example 3: NamedTuple vs Regular Tuple ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: NamedTuple advantages over regular tuple")
    print("=" * 70)

    # Regular tuple - unclear what each value represents
    regular_tuple = (100, 2.5)
    print(f"\nRegular tuple:")
    print(f"  my_tuple = (100, 2.5)")
    print(f"  my_tuple[0] = {regular_tuple[0]}  (What is this? Need documentation)")
    print(f"  my_tuple[1] = {regular_tuple[1]}  (What is this? Need documentation)")

    # NamedTuple - clear field names
    named_tuple = DemoNTClass(100, 2.5)
    print(f"\nNamedTuple:")
    print(f"  my_tuple = DemoNTClass(100, 2.5)")
    print(f"  my_tuple.a = {named_tuple.a}  (Clear: this is 'a')")
    print(f"  my_tuple.b = {named_tuple.b}  (Clear: this is 'b')")

    print(f"\nWhy NamedTuple is better:")
    print(f"  1. Names make code self-documenting")
    print(f"  2. IDE autocomplete works with named fields")
    print(f"  3. Type hints help catch errors before runtime")
    print(f"  4. Still has tuple efficiency and immutability")


    # ============ Example 4: Immutability - NamedTuples Cannot Be Modified ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: NamedTuples are immutable by default")
    print("=" * 70)

    print(f"\nAttempting to modify a NamedTuple:")
    print(f"  instance1.a = 50  # Try to change field 'a'")

    try:
        instance1.a = 50
        print(f"  ERROR: This should not succeed!")
    except AttributeError as e:
        print(f"  Result: AttributeError: {e}")
        print(f"  WHY? NamedTuples are immutable (like regular tuples)")

    print(f"\nThis is a key difference from mutable dataclasses:")
    print(f"  - NamedTuple: Immutable by default (like tuple)")
    print(f"  - Dataclass: Mutable by default (can use frozen=True)")


    # ============ Example 5: Tuple Operations Still Work ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: NamedTuple still supports tuple operations")
    print("=" * 70)

    # Indexing
    print(f"\nIndexing (like a regular tuple):")
    print(f"  instance2[0] = {instance2[0]}  (first field: a)")
    print(f"  instance2[1] = {instance2[1]}  (second field: b)")

    # Unpacking
    print(f"\nUnpacking (like a regular tuple):")
    a_val, b_val = instance2
    print(f"  a_val, b_val = instance2")
    print(f"  a_val = {a_val}, b_val = {b_val}")

    # Iteration
    print(f"\nIteration (like a regular tuple):")
    print(f"  for value in instance2:")
    for value in instance2:
        print(f"    {value}")

    # Length
    print(f"\nLength:")
    print(f"  len(instance2) = {len(instance2)}")

    # String representation
    print(f"\nString representation:")
    print(f"  str(instance2) = {str(instance2)}")
    print(f"  repr(instance2) = {repr(instance2)}")


    # ============ Example 6: Class Attributes in NamedTuple ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Class attributes without type hints")
    print("=" * 70)

    print(f"\nThe 'c' attribute is a class attribute (like in dataclass):")
    print(f"  DemoNTClass.c = '{DemoNTClass.c}'")
    print(f"  instance1.c = '{instance1.c}'")
    print(f"  instance2.c = '{instance2.c}'")

    print(f"\nIt's shared across all instances:")
    print(f"  (Accessing it through instances shows the class-level value)")

    print(f"\nIt's NOT in the NamedTuple fields:")
    print(f"  len(instance2) = {len(instance2)}  (only a and b, not c)")


    # ============ Example 7: NamedTuple vs Dataclass Comparison ============
    print("\n" + "=" * 70)
    print("EXAMPLE 7: NamedTuple vs Dataclass")
    print("=" * 70)

    print(f"\nNamedTuple advantages:")
    print(f"  1. Immutable by default (safer for dict keys/sets)")
    print(f"  2. Lighter memory footprint (still a tuple)")
    print(f"  3. Compatible with any tuple operation")
    print(f"  4. Great for simple data structures")

    print(f"\nDataclass advantages:")
    print(f"  1. Mutable by default (easier to work with)")
    print(f"  2. More flexible (add methods, use field())")
    print(f"  3. order=True generates comparison methods")
    print(f"  4. Better for complex data structures")

    print(f"\nChoose NamedTuple when:")
    print(f"  - You need immutability")
    print(f"  - You want tuple-like behavior")
    print(f"  - Memory efficiency matters")
    print(f"  - Your data is simple (few fields, no methods)")

    print(f"\nChoose Dataclass when:")
    print(f"  - You need mutability")
    print(f"  - You want to add methods to your data structure")
    print(f"  - You need customizable initialization or comparison")
    print(f"  - You need field validation")

    print(f"\n" + "=" * 70)
```


---

## Runnable Example: `namedtuple_typed_with_methods.py`

```python
"""
TUTORIAL: Typed NamedTuple with Custom Methods - Adding Behavior to Tuples
===========================================================================

In this tutorial, you'll learn how to add custom methods to NamedTuple classes.
NamedTuple is immutable by default, but you can override methods like __str__
to customize how instances are displayed.

Key insight: NamedTuple is both a tuple AND a class. You can:
  - Keep immutability (for safety and hashability)
  - Add custom methods (for behavior and presentation)
  - Use all tuple operations (indexing, unpacking, iteration)

In this example, we override __str__ to display geographic coordinates in
human-readable format (e.g., "51.5°N, 0.1°W") while keeping the technical
__repr__ for debugging.

Why add methods to NamedTuple?
  - Custom __str__ for user-friendly output
  - Custom __repr__ for debugging information
  - Helper methods for common operations on the data
  - Validation or transformation methods
"""

from typing import NamedTuple


# ============ Example 1: NamedTuple with Custom __str__ ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Defining a NamedTuple with custom __str__ method")
    print("=" * 70)

    class Coordinate(NamedTuple):
        """A geographic coordinate with latitude and longitude.

        This NamedTuple extends the basic tuple with:
        - Named fields for clarity (lat, lon instead of [0], [1])
        - Type hints for documentation and IDE support
        - Custom __str__ for readable geographic format
        - Immutability for safety and hashability

        The __str__ method converts:
          (51.5074, -0.1278) → "51.5°N, 0.1°W"
        """
        lat: float
        lon: float

        def __str__(self):
            """Return a user-friendly string representation of the coordinate.

            This converts raw coordinates to geographic format:
            - 'N' for positive latitude (North), 'S' for negative (South)
            - 'E' for positive longitude (East), 'W' for negative (West)
            - One decimal place for readability

            Returns:
                str: Coordinate in "latitude°direction, longitude°direction" format
            """
            # Determine hemisphere indicators
            ns = 'N' if self.lat >= 0 else 'S'  # North or South
            we = 'E' if self.lon >= 0 else 'W'  # East or West

            # Format with absolute values and one decimal place
            return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'


    # Create coordinate instances
    london = Coordinate(51.5074, -0.1278)
    sydney = Coordinate(-33.8688, 151.2093)
    tokyo = Coordinate(35.6762, 139.6503)

    print(f"\nCoordinates created:")
    print(f"  london = Coordinate(51.5074, -0.1278)")
    print(f"  sydney = Coordinate(-33.8688, 151.2093)")
    print(f"  tokyo = Coordinate(35.6762, 139.6503)")


    # ============ Example 2: __str__ vs __repr__ ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Comparing __str__ (user-friendly) vs __repr__ (technical)")
    print("=" * 70)

    print(f"\nUsing str() - our custom __str__ method:")
    print(f"  str(london) = {str(london)}")
    print(f"  str(sydney) = {str(sydney)}")
    print(f"  str(tokyo) = {str(tokyo)}")

    print(f"\nUsing repr() - automatic NamedTuple __repr__:")
    print(f"  repr(london) = {repr(london)}")
    print(f"  repr(sydney) = {repr(sydney)}")

    print(f"\nWhy both?")
    print(f"  - __str__(): For humans (e.g., print output, user interfaces)")
    print(f"  - __repr__(): For developers (e.g., debugging, interactive shell)")
    print(f"  - print() calls __str__() if it exists, otherwise __repr__()")


    # ============ Example 3: Using in print Statements ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Using coordinates in print statements")
    print("=" * 70)

    print(f"\nSimple print statements use __str__:")
    print(f"  print(london) outputs: {london}")
    print(f"  print(sydney) outputs: {sydney}")

    print(f"\nYou can format them in strings:")
    message = f"Meeting in London at {london}"
    print(f"  message = f'Meeting in London at {{london}}'")
    print(f"  Result: {message}")

    locations = [london, sydney, tokyo]
    print(f"\nPrinting a list of locations:")
    for name, loc in [('London', london), ('Sydney', sydney), ('Tokyo', tokyo)]:
        print(f"  {name}: {loc}")


    # ============ Example 4: NamedTuple Operations Still Work ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: NamedTuple is still a tuple - indexing and unpacking work")
    print("=" * 70)

    print(f"\nAccessing by field name (more readable):")
    print(f"  london.lat = {london.lat}")
    print(f"  london.lon = {london.lon}")

    print(f"\nAccessing by index (like regular tuple):")
    print(f"  london[0] = {london[0]}  (latitude)")
    print(f"  london[1] = {london[1]}  (longitude)")

    print(f"\nUnpacking:")
    lat, lon = london
    print(f"  lat, lon = london")
    print(f"  lat = {lat}, lon = {lon}")

    print(f"\nIteration:")
    print(f"  for value in london:")
    for value in london:
        print(f"    {value}")

    print(f"\nLength:")
    print(f"  len(london) = {len(london)}")


    # ============ Example 5: Immutability ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: NamedTuple instances are immutable")
    print("=" * 70)

    print(f"\nAttempting to modify: london.lat = 50.0")
    try:
        london.lat = 50.0
        print(f"  ERROR: This should have failed!")
    except AttributeError as e:
        print(f"  Result: AttributeError")
        print(f"  WHY? NamedTuple is immutable (inherits from tuple)")

    print(f"\nAttempting to add new attribute: london.city = 'London'")
    try:
        london.city = 'London'
        print(f"  ERROR: This should have failed!")
    except AttributeError as e:
        print(f"  Result: AttributeError")
        print(f"  WHY? Tuples don't support arbitrary attribute assignment")


    # ============ Example 6: Using as Dictionary Keys ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Hashable - can use as dictionary keys")
    print("=" * 70)

    # Create a dictionary with coordinates as keys
    cities = {
        london: 'London, UK',
        sydney: 'Sydney, Australia',
        tokyo: 'Tokyo, Japan',
    }

    print(f"\nUsing coordinates as dictionary keys:")
    print(f"  cities = {{")
    for coord, name in cities.items():
        print(f"    {coord}: '{name}',")
    print(f"  }}")

    print(f"\nLooking up cities:")
    print(f"  cities[london] = '{cities[london]}'")
    print(f"  cities[sydney] = '{cities[sydney]}'")

    print(f"\nWhy is this possible?")
    print(f"  - Dictionary keys must be hashable (immutable)")
    print(f"  - NamedTuple is immutable by default")
    print(f"  - Both __str__ and immutability make it a perfect key type")


    # ============ Example 7: Adding More Methods ============
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Adding additional helper methods")
    print("=" * 70)

    class EnhancedCoordinate(NamedTuple):
        """Coordinate with additional helper methods."""
        lat: float
        lon: float

        def __str__(self):
            """User-friendly geographic format."""
            ns = 'N' if self.lat >= 0 else 'S'
            we = 'E' if self.lon >= 0 else 'W'
            return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'

        def is_northern_hemisphere(self):
            """Check if coordinate is in Northern Hemisphere."""
            return self.lat > 0

        def is_equator(self):
            """Check if coordinate is on the equator."""
            return abs(self.lat) < 0.01  # Within 0.01 degrees

        def distance_from_prime_meridian(self):
            """Calculate absolute distance from prime meridian (0° longitude)."""
            return abs(self.lon)


    # Use the enhanced coordinate
    location = EnhancedCoordinate(51.5, 0.1)
    print(f"\nlocation = EnhancedCoordinate(51.5, 0.1)")
    print(f"  str(location) = {str(location)}")
    print(f"  location.is_northern_hemisphere() = {location.is_northern_hemisphere()}")
    print(f"  location.is_equator() = {location.is_equator()}")
    print(f"  location.distance_from_prime_meridian() = {location.distance_from_prime_meridian()}")

    equator_loc = EnhancedCoordinate(0.0, 30.0)
    print(f"\nequator_loc = EnhancedCoordinate(0.0, 30.0)")
    print(f"  str(equator_loc) = {str(equator_loc)}")
    print(f"  equator_loc.is_equator() = {equator_loc.is_equator()}")
    print(f"  equator_loc.is_northern_hemisphere() = {equator_loc.is_northern_hemisphere()}")


    # ============ Example 8: Summary - NamedTuple with Methods ============
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Key benefits of NamedTuple with methods")
    print("=" * 70)

    print(f"\nNamedTuple combines the best of both worlds:")
    print(f"  1. Tuple benefits:")
    print(f"     - Immutable and hashable")
    print(f"     - Lightweight (lower memory than dataclass)")
    print(f"     - Can use in sets and as dict keys")
    print(f"     - Compatible with tuple unpacking/indexing")

    print(f"  2. Class benefits:")
    print(f"     - Named fields (self.lat instead of self[0])")
    print(f"     - Type hints for clarity and IDE support")
    print(f"     - Custom methods (__str__, __repr__, helpers)")
    print(f"     - Self-documenting code")

    print(f"\nWhen to use:")
    print(f"  - Small, immutable data structures")
    print(f"  - Need tuple-like operations (unpacking, iteration)")
    print(f"  - Want hashability (dict keys, set members)")
    print(f"  - Performance matters (lighter than dataclass)")

    print(f"\nWhen NOT to use:")
    print(f"  - Need mutability")
    print(f"  - Building complex objects with many methods")
    print(f"  - Want inheritance (NamedTuple has limitations)")

    print(f"\n" + "=" * 70)
```

---

## Exercises

**Exercise 1.**
Create the same `Point` class three ways: as a `dataclass`, as a `NamedTuple`, and as a regular class. Each should have `x` and `y` fields. Compare them by testing equality (`==`), immutability (can you change `x`?), and whether they can be used as dictionary keys.

??? success "Solution to Exercise 1"

        from dataclasses import dataclass
        from typing import NamedTuple

        # Dataclass
        @dataclass
        class PointDC:
            x: float
            y: float

        # NamedTuple
        class PointNT(NamedTuple):
            x: float
            y: float

        # Regular class
        class PointReg:
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def __eq__(self, other):
                return self.x == other.x and self.y == other.y

        # Equality
        print(PointDC(1, 2) == PointDC(1, 2))    # True
        print(PointNT(1, 2) == PointNT(1, 2))    # True
        print(PointReg(1, 2) == PointReg(1, 2))   # True

        # Immutability
        dc = PointDC(1, 2)
        dc.x = 10  # Works — mutable by default

        nt = PointNT(1, 2)
        # nt.x = 10  # AttributeError — immutable

        # Dictionary keys
        # print({PointDC(1, 2): "a"})  # TypeError — not hashable
        print({PointNT(1, 2): "a"})    # Works — immutable and hashable

---

**Exercise 2.**
Model a `Config` object with fields `host`, `port`, and `debug`. Implement it as both a `NamedTuple` and a `frozen=True` dataclass. Compare: which supports default values more naturally? Which supports inheritance? Show the differences in practice.

??? success "Solution to Exercise 2"

        from dataclasses import dataclass
        from typing import NamedTuple

        class ConfigNT(NamedTuple):
            host: str = "localhost"
            port: int = 8080
            debug: bool = False

        @dataclass(frozen=True)
        class ConfigDC:
            host: str = "localhost"
            port: int = 8080
            debug: bool = False

        # Both support defaults
        nt = ConfigNT()
        dc = ConfigDC()
        print(nt)  # ConfigNT(host='localhost', port=8080, debug=False)
        print(dc)  # ConfigDC(host='localhost', port=8080, debug=False)

        # Dataclass supports inheritance; NamedTuple has limitations
        @dataclass(frozen=True)
        class ProdConfig(ConfigDC):
            ssl: bool = True

        print(ProdConfig())
        # ProdConfig(host='localhost', port=8080, debug=False, ssl=True)

---

**Exercise 3.**
Create a `Student` with `name`, `grade`, and `gpa` fields using all three approaches (regular class, NamedTuple, dataclass). For each, add a method `is_honors()` that returns `True` if `gpa >= 3.5`. Discuss which approach makes adding methods easiest and which produces the cleanest code.

??? success "Solution to Exercise 3"

        from dataclasses import dataclass
        from typing import NamedTuple

        # Regular class
        class StudentReg:
            def __init__(self, name, grade, gpa):
                self.name = name
                self.grade = grade
                self.gpa = gpa

            def is_honors(self):
                return self.gpa >= 3.5

        # NamedTuple
        class StudentNT(NamedTuple):
            name: str
            grade: int
            gpa: float

            def is_honors(self):
                return self.gpa >= 3.5

        # Dataclass
        @dataclass
        class StudentDC:
            name: str
            grade: int
            gpa: float

            def is_honors(self):
                return self.gpa >= 3.5

        for cls in [StudentReg, StudentNT, StudentDC]:
            s = cls("Alice", 12, 3.8)
            print(f"{cls.__name__}: is_honors={s.is_honors()}")
        # Dataclass is cleanest: no boilerplate, easy to add methods
