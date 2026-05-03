# Frozen Dataclasses

The `frozen=True` parameter makes a dataclass immutable, preventing modifications after creation. Frozen dataclasses can be hashed and used in sets/dicts.

!!! tip "Mental Model"
    A frozen dataclass is like a notarized document -- once signed, no field can be altered. This guarantee makes instances safe to use as dictionary keys and set members, because their hash can never change. When you need to "modify" a frozen instance, you create a new one with `replace()`, leaving the original untouched.

---

## Creating Frozen Dataclasses

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: float
    y: float

point = Point(1.0, 2.0)
print(point)  # Point(x=1.0, y=2.0)

# Attempt to modify raises FrozenInstanceError
try:
    point.x = 5.0
except AttributeError as e:
    print(f"Error: {e}")
```

## Using Frozen Dataclasses as Dictionary Keys

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

# Frozen dataclasses are hashable
coords = {
    Coordinate(0, 0): "origin",
    Coordinate(1, 1): "diagonal",
    Coordinate(-1, 1): "northwest"
}

print(coords[Coordinate(0, 0)])    # "origin"
print(Coordinate(1, 1) in coords)  # True
```

## Using Frozen Dataclasses in Sets

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Color:
    red: int
    green: int
    blue: int

colors = {
    Color(255, 0, 0),     # Red
    Color(0, 255, 0),     # Green
    Color(0, 0, 255),     # Blue
    Color(255, 0, 0)      # Duplicate red (ignored)
}

print(len(colors))  # 3 (unique colors only)
print(Color(255, 0, 0) in colors)  # True
```

## Frozen vs Mutable

```python
from dataclasses import dataclass

# Mutable (default)
@dataclass
class MutablePoint:
    x: float
    y: float

# Frozen
@dataclass(frozen=True)
class FrozenPoint:
    x: float
    y: float

# Mutable can be modified
mut_point = MutablePoint(1, 2)
mut_point.x = 3

# Frozen cannot
frozen_point = FrozenPoint(1, 2)
try:
    frozen_point.x = 3
except AttributeError as e:
    print(f"Cannot modify frozen: {e}")

# Frozen can be hashed (used as dict key)
point_map = {frozen_point: "initial"}
print(point_map[frozen_point])  # "initial"
```

## Performance Implications

```python
from dataclasses import dataclass
import timeit

@dataclass
class Mutable:
    x: int
    y: int

@dataclass(frozen=True)
class Frozen:
    x: int
    y: int

# Frozen dataclasses have hash cached
frozen = Frozen(1, 2)
print(hash(frozen))

# Creation time is similar
# But hashing is faster for frozen (cached)
```

## Updating Frozen Instances with replace()

Since frozen instances cannot be modified, use `dataclasses.replace()` to create a
new instance with selected fields changed — a "copy and modify" pattern:

```python
from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Config:
    host: str
    port: int
    debug: bool = False

prod = Config("db.example.com", 5432)
dev = replace(prod, debug=True, port=5433)

print(prod)  # Config(host='db.example.com', port=5432, debug=False)
print(dev)   # Config(host='db.example.com', port=5433, debug=True)
```

!!! warning "Frozen does not mean deeply immutable"
    `frozen=True` prevents reassignment of fields, but if a field holds a mutable
    object (e.g., a list), the contents of that object can still be modified:

    ```python
    @dataclass(frozen=True)
    class Team:
        name: str
        members: list

    t = Team("Alpha", ["Alice", "Bob"])
    # t.name = "Beta"        # FrozenInstanceError
    t.members.append("Eve")  # Works! The list itself is mutable
    print(t.members)          # ['Alice', 'Bob', 'Eve']
    ```

    For true deep immutability, use tuples or frozensets for collection fields.

## When to Use Frozen

Frozen dataclasses are **value objects** — their identity is defined entirely by
their field values, not by an `id` or reference. Two frozen instances with the same
fields are equal, hashable, and safely shareable across threads or data structures.

- Use when data should be immutable (coordinates, colors, config snapshots)
- Use when storing in sets or as dictionary keys
- Use for function parameters that shouldn't be modified
- Use for thread-safe data sharing
- **Tradeoff**: frozen instances have a small performance overhead on creation (the
  generated `__init__` uses `object.__setattr__` instead of direct assignment), and
  every "update" requires creating a new object via `replace()`

---

## Runnable Example: `dataclass_immutable_with_methods.py`

```python
"""
TUTORIAL: Frozen Dataclass with Custom Methods - Immutability and __str__
=========================================================================

In this tutorial, you'll learn how to create immutable dataclasses using the
frozen=True parameter. Immutable objects cannot be modified after creation,
which is useful for:

  - Data that should never change (like coordinates or dates)
  - Using instances as dictionary keys (requires immutability)
  - Thread-safe code where no synchronization is needed
  - Making intent clear: "this data is final"

We'll also override the __str__ method to create a custom string representation.
Unlike __repr__ (which shows the internal structure), __str__ shows a user-friendly
format. For geographic coordinates, we'll display them as "latitude degrees
direction, longitude degrees direction" format (e.g., "51.5°N, 0.1°W").

Why override __str__ in a frozen dataclass? Even though @dataclass generates
__repr__, you can provide a more readable __str__ for end users while keeping
the technical __repr__ for debugging.
"""

from dataclasses import dataclass


# ============ Example 1: Creating a Frozen Dataclass ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Defining a frozen (immutable) Coordinate dataclass")
    print("=" * 70)

    @dataclass(frozen=True)
    class Coordinate:
        """A geographic coordinate with latitude and longitude.

        The frozen=True parameter makes instances immutable. You cannot modify
        lat or lon after the Coordinate is created. Python will raise a
        FrozenInstanceError if you try.

        This class also overrides __str__ to display coordinates in a
        human-readable format (e.g., "51.5°N, 0.1°W").
        """
        lat: float
        lon: float

        def __str__(self):
            """Return a user-friendly string representation of the coordinate.

            We override __str__ to provide a geographic format:
            - Convert latitude to absolute value with N/S hemisphere indicator
            - Convert longitude to absolute value with E/W hemisphere indicator
            - Format with one decimal place for readability
            """
            # 'N' for positive latitude (North), 'S' for negative (South)
            ns = 'N' if self.lat >= 0 else 'S'
            # 'E' for positive longitude (East), 'W' for negative (West)
            we = 'E' if self.lon >= 0 else 'W'
            # Return formatted string with absolute values and direction indicators
            return f'{abs(self.lat):.1f}°{ns}, {abs(self.lon):.1f}°{we}'


    # Create some coordinate instances
    london = Coordinate(51.5074, -0.1278)
    sydney = Coordinate(-33.8688, 151.2093)
    equator = Coordinate(0.0, 0.0)

    print(f"\nCoordinates created:")
    print(f"  london = Coordinate(51.5074, -0.1278)")
    print(f"  sydney = Coordinate(-33.8688, 151.2093)")
    print(f"  equator = Coordinate(0.0, 0.0)")


    # ============ Example 2: __str__ vs __repr__ ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Understanding __str__ vs __repr__")
    print("=" * 70)

    print(f"\nUsing str() - our custom __str__ method (user-friendly):")
    print(f"  str(london) = {str(london)}")
    print(f"  str(sydney) = {str(sydney)}")
    print(f"  str(equator) = {str(equator)}")

    print(f"\nUsing repr() - dataclass-generated __repr__ (technical):")
    print(f"  repr(london) = {repr(london)}")
    print(f"  repr(sydney) = {repr(sydney)}")

    print(f"\nWhy both?")
    print(f"  - __str__(): For humans reading output")
    print(f"  - __repr__(): For developers debugging code")
    print(f"  - str() calls __str__() if it exists")
    print(f"  - repr() calls __repr__() and shows the 'official' representation")


    # ============ Example 3: Immutability - Trying to Modify ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Testing immutability - frozen=True prevents changes")
    print("=" * 70)

    print(f"\nAttempting to modify a frozen dataclass:")
    print(f"  london.lat = 50.0  # Try to change latitude")

    try:
        london.lat = 50.0
        print(f"  ERROR: This should not succeed!")
    except Exception as e:
        print(f"  Result: {type(e).__name__}: {e}")
        print(f"  WHY? frozen=True makes the instance immutable")

    print(f"\nAttempting to add a new attribute:")
    print(f"  london.name = 'London'  # Try to add new attribute")

    try:
        london.name = 'London'
        print(f"  ERROR: This should not succeed!")
    except Exception as e:
        print(f"  Result: {type(e).__name__}: {e}")
        print(f"  WHY? frozen=True prevents any attribute modification")


    # ============ Example 4: Using Frozen Dataclasses as Dictionary Keys ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Frozen dataclasses are hashable - use as dict keys")
    print("=" * 70)

    # Immutable objects can be used as dictionary keys
    print(f"\nCreating a dictionary with coordinates as keys:")
    cities = {
        london: 'London, UK',
        sydney: 'Sydney, Australia',
        equator: 'Null Island',
    }

    print(f"  cities = {{")
    for coord, name in cities.items():
        print(f"    {coord}: '{name}',")
    print(f"  }}")

    print(f"\nLooking up cities by coordinate:")
    print(f"  cities[london] = '{cities[london]}'")
    print(f"  cities[sydney] = '{cities[sydney]}'")

    print(f"\nWhy is this only possible with frozen=True?")
    print(f"  - Dictionary keys must be hashable (immutable)")
    print(f"  - Mutable objects change after insertion, breaking the dictionary")
    print(f"  - frozen=True makes Coordinate instances hashable")


    # ============ Example 5: Hemisphere Direction Logic ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Understanding the geographic direction logic")
    print("=" * 70)

    # Test coordinates in all four hemispheres
    north_east = Coordinate(45.0, 90.0)
    north_west = Coordinate(45.0, -90.0)
    south_east = Coordinate(-45.0, 90.0)
    south_west = Coordinate(-45.0, -90.0)

    print(f"\nCoordinates in all four hemispheres:")
    print(f"  North/East: lat=45.0, lon=90.0   →  {north_east}")
    print(f"  North/West: lat=45.0, lon=-90.0  →  {north_west}")
    print(f"  South/East: lat=-45.0, lon=90.0  →  {south_east}")
    print(f"  South/West: lat=-45.0, lon=-90.0 →  {south_west}")

    print(f"\nHow the __str__ method works:")
    print(f"  1. Check lat >= 0 → 'N' (North) or 'S' (South)")
    print(f"  2. Check lon >= 0 → 'E' (East) or 'W' (West)")
    print(f"  3. Use abs() to get positive values")
    print(f"  4. Format with .1f for one decimal place")


    # ============ Example 6: Summary of Frozen Dataclass Benefits ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Key benefits of frozen dataclasses")
    print("=" * 70)

    print(f"\nFrozen dataclasses provide:")
    print(f"  1. Immutability: Values never change after creation")
    print(f"  2. Hashability: Can be used as dictionary keys or in sets")
    print(f"  3. Safety: Accidental modifications are caught as errors")
    print(f"  4. Intent clarity: Frozen = 'this data is final and safe'")

    print(f"\nCustom __str__ method provides:")
    print(f"  1. User-friendly output (geographic format, not raw numbers)")
    print(f"  2. Domain-specific representation")
    print(f"  3. Cleaner print() output for end users")

    print(f"\n" + "=" * 70)
```

---

## Exercises

**Exercise 1.**
Create a frozen dataclass `Coordinate` with `latitude` and `longitude` fields. Show that attempting to modify a field raises `FrozenInstanceError`. Then demonstrate that a `Coordinate` can be used as a dictionary key and stored in a set.

??? success "Solution to Exercise 1"

        from dataclasses import dataclass

        @dataclass(frozen=True)
        class Coordinate:
            latitude: float
            longitude: float

        c = Coordinate(37.7749, -122.4194)

        try:
            c.latitude = 0.0
        except AttributeError as e:
            print(f"Cannot modify: {e}")

        # Use as dictionary key
        locations = {c: "San Francisco"}
        print(locations[Coordinate(37.7749, -122.4194)])  # San Francisco

        # Use in a set
        coords = {Coordinate(0, 0), Coordinate(1, 1), Coordinate(0, 0)}
        print(len(coords))  # 2 — duplicate removed

---

**Exercise 2.**
Define a frozen dataclass `Color` with `r`, `g`, `b` (int) fields. Add a method `hex()` that returns the color as a hex string (e.g., `"#FF0000"`). Create a set of colors and demonstrate deduplication (adding the same color twice results in only one entry).

??? success "Solution to Exercise 2"

        from dataclasses import dataclass

        @dataclass(frozen=True)
        class Color:
            r: int
            g: int
            b: int

            def hex(self):
                return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

        red = Color(255, 0, 0)
        green = Color(0, 255, 0)
        print(red.hex())    # #FF0000
        print(green.hex())  # #00FF00

        colors = {Color(255, 0, 0), Color(0, 255, 0), Color(255, 0, 0)}
        print(len(colors))  # 2 — red deduplicated

---

**Exercise 3.**
Create a frozen dataclass `AppConfig` with fields `db_host`, `db_port`, and `debug`. Demonstrate the "copy and modify" pattern: use `dataclasses.replace()` to create a new config with `debug=True` while keeping the original unchanged. Show that the original and modified configs are different objects.

??? success "Solution to Exercise 3"

        from dataclasses import dataclass, replace

        @dataclass(frozen=True)
        class AppConfig:
            db_host: str
            db_port: int
            debug: bool

        prod = AppConfig("db.example.com", 5432, False)
        dev = replace(prod, debug=True)

        print(prod)  # AppConfig(db_host='db.example.com', db_port=5432, debug=False)
        print(dev)   # AppConfig(db_host='db.example.com', db_port=5432, debug=True)
        print(prod is dev)    # False — different objects
        print(prod == dev)    # False — debug differs
