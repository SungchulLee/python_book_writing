# \_\_slots\_\_

By default, Python stores instance attributes in a dictionary (`__dict__`). The `__slots__` declaration lets you explicitly define which attributes an instance can have, resulting in significant memory savings and faster attribute access.

!!! tip "Mental Model"
    Without `__slots__`, every instance carries a full dictionary -- like giving each person a filing cabinet when they only need two index cards. Declaring `__slots__` replaces that cabinet with fixed-size slots, saving memory per instance and making attribute lookup faster through direct offset access.

---

## The Problem: Memory Overhead

Every Python object with instance attributes carries a `__dict__`:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.__dict__)  # {'x': 1, 'y': 2}
```

This dictionary:

- Consumes memory (empty dict ~64 bytes, plus key storage)
- Allows dynamic attribute creation
- Has hash table overhead for attribute lookup

For millions of small objects, this overhead adds up significantly.

---

## The Solution: \_\_slots\_\_

Declare `__slots__` to use a fixed, memory-efficient storage:

```python
class Point:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(p.x, p.y)    # 1 2
# print(p.__dict__)  # AttributeError: 'Point' object has no attribute '__dict__'
```

---

## Memory Comparison

```python
import sys

class RegularPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SlottedPoint:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

regular = RegularPoint(1, 2)
slotted = SlottedPoint(1, 2)

print(sys.getsizeof(regular))           # ~48 bytes (object only)
print(sys.getsizeof(regular.__dict__))  # ~104 bytes (dict overhead)
print(sys.getsizeof(slotted))           # ~48 bytes (no dict!)

# Total memory per instance:
# Regular: ~152 bytes
# Slotted: ~48 bytes (68% reduction!)
```

### At Scale

```python
# Creating 1 million points
regular_points = [RegularPoint(i, i) for i in range(1_000_000)]
# Memory: ~152 MB

slotted_points = [SlottedPoint(i, i) for i in range(1_000_000)]
# Memory: ~48 MB

# Savings: ~104 MB (68% reduction)
```

---

## Syntax Variations

### Tuple of Strings

```python
class Point:
    __slots__ = ('x', 'y')
```

### List of Strings

```python
class Point:
    __slots__ = ['x', 'y']
```

### Single Attribute

```python
class Counter:
    __slots__ = ('count',)  # Note: tuple needs comma
    # or
    __slots__ = ['count']
    # or
    __slots__ = 'count'     # Single string works too
```

---

## Behavior Changes

### No Dynamic Attributes

```python
class SlottedPoint:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = SlottedPoint(1, 2)
p.z = 3  # AttributeError: 'SlottedPoint' object has no attribute 'z'
```

### No \_\_dict\_\_ by Default

```python
p = SlottedPoint(1, 2)
p.__dict__  # AttributeError: 'SlottedPoint' object has no attribute '__dict__'
```

### Can Add \_\_dict\_\_ to Slots

```python
class Hybrid:
    __slots__ = ('x', 'y', '__dict__')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

h = Hybrid(1, 2)
h.z = 3       # Works! Stored in __dict__
print(h.z)    # 3
print(h.x)    # 1 (stored in slot)
```

---

## Inheritance

### Slotted Parent, No Slots in Child

```python
class Parent:
    __slots__ = ('x',)

class Child(Parent):
    pass  # Gets __dict__ automatically

c = Child()
c.x = 1    # Uses inherited slot
c.y = 2    # Uses __dict__
print(c.__dict__)  # {'y': 2}
```

### Both Parent and Child Slotted

```python
class Parent:
    __slots__ = ('x',)

class Child(Parent):
    __slots__ = ('y',)  # Don't repeat 'x'!

c = Child()
c.x = 1
c.y = 2
# c.__dict__  # AttributeError - no dict
```

### Warning: Don't Repeat Slots

```python
class Parent:
    __slots__ = ('x',)

class Child(Parent):
    __slots__ = ('x', 'y')  # BAD: 'x' repeated
    # This wastes memory and can cause issues
```

---

## With \_\_weakref\_\_

By default, slotted objects cannot be weakly referenced:

```python
import weakref

class Slotted:
    __slots__ = ('x',)

s = Slotted()
weakref.ref(s)  # TypeError: cannot create weak reference to 'Slotted' object
```

Add `__weakref__` to slots to enable weak references:

```python
class Slotted:
    __slots__ = ('x', '__weakref__')

s = Slotted()
ref = weakref.ref(s)  # Works!
```

---

## Performance Benefits

### Faster Attribute Access

```python
import timeit

class Regular:
    def __init__(self):
        self.x = 0

class Slotted:
    __slots__ = ('x',)
    def __init__(self):
        self.x = 0

r = Regular()
s = Slotted()

# Attribute access is faster with slots
timeit.timeit('r.x', globals={'r': r}, number=10_000_000)  # ~0.35s
timeit.timeit('s.x', globals={'s': s}, number=10_000_000)  # ~0.30s
# ~15% faster
```

---

## When to Use \_\_slots\_\_

### Good Use Cases

```python
# 1. Many instances of simple data classes
class Coordinate:
    __slots__ = ('lat', 'lon')

# 2. Performance-critical inner loops
class Node:
    __slots__ = ('value', 'left', 'right')

# 3. Memory-constrained environments
class SensorReading:
    __slots__ = ('timestamp', 'value', 'sensor_id')
```

### When NOT to Use

```python
# 1. Need dynamic attributes
class FlexibleConfig:
    pass  # Users may add arbitrary attributes

# 2. Using __dict__ for introspection
class Debuggable:
    pass  # Need vars() or __dict__ access

# 3. Multiple inheritance with different slots
# Can get complicated quickly
```

---

## Slots with Dataclasses (Python 3.10+)

Python 3.10 added `slots=True` to dataclasses:

```python
from dataclasses import dataclass

@dataclass(slots=True)
class Point:
    x: float
    y: float

p = Point(1.0, 2.0)
# p.z = 3  # AttributeError
```

This is the cleanest way to use slots with modern Python.

---

## Slots with NamedTuple

`NamedTuple` already uses slots internally:

```python
from typing import NamedTuple

class Point(NamedTuple):
    x: float
    y: float

p = Point(1.0, 2.0)
# Already memory-efficient, but immutable
```

---

## Common Pitfalls

### Forgetting Inherited Slots

```python
class Parent:
    __slots__ = ('x',)

class Child(Parent):
    __slots__ = ('y',)
    
    def __init__(self):
        self.x = 1  # From parent
        self.y = 2  # From child
        self.z = 3  # AttributeError! No slot for 'z'
```

### Class Attributes vs Instance Slots

```python
class Example:
    __slots__ = ('x',)
    y = 10  # Class attribute - works fine
    
    def __init__(self):
        self.x = 1   # Instance slot
        # self.z = 3  # AttributeError

e = Example()
print(e.x)  # 1 (instance)
print(e.y)  # 10 (class attribute)
```

### Default Values

```python
# This doesn't work as expected:
class Wrong:
    __slots__ = ('x',)
    x = 10  # This becomes a class attribute, shadows the slot!

# Do this instead:
class Right:
    __slots__ = ('x',)
    
    def __init__(self, x=10):
        self.x = x
```

---

## Summary

| Aspect | With `__dict__` | With `__slots__` |
|--------|-----------------|------------------|
| Memory per instance | Higher (~152 bytes) | Lower (~48 bytes) |
| Attribute access | Hash lookup | Direct offset |
| Dynamic attributes | Yes | No (unless `__dict__` in slots) |
| Weak references | Yes | Only if `__weakref__` in slots |
| Introspection | `vars(obj)` works | Limited |

**Key Takeaways**:

- `__slots__` eliminates per-instance `__dict__` overhead
- Use for classes with many instances and fixed attributes
- Memory savings of 50-70% typical
- Slight performance improvement for attribute access
- Don't repeat parent slots in child classes
- Add `__weakref__` if weak references needed
- Python 3.10+ dataclasses support `slots=True`

---

## Exercises

**Exercise 1.**
Create a slotted class `Vector3D` with attributes `x`, `y`, `z` and `__weakref__`. Verify that (a) setting a dynamic attribute like `w` raises `AttributeError`, (b) you can create a `weakref.ref` to an instance, and (c) print the instance's size using `sys.getsizeof()`.

??? success "Solution to Exercise 1"
        ```python
        import sys
        import weakref

        class Vector3D:
            __slots__ = ('x', 'y', 'z', '__weakref__')

            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        v = Vector3D(1.0, 2.0, 3.0)

        # (a) Dynamic attribute blocked
        try:
            v.w = 4.0
        except AttributeError as e:
            print(f"AttributeError: {e}")

        # (b) Weak reference works
        ref = weakref.ref(v)
        print(f"Weak ref alive: {ref() is not None}")

        # (c) Instance size
        print(f"Size: {sys.getsizeof(v)} bytes")
        ```

---

**Exercise 2.**
Define a parent class `Shape` with `__slots__ = ('color',)` and a child class `Circle` with `__slots__ = ('radius',)`. Create a `Circle` instance, set both `color` and `radius`, then demonstrate that attempting to set an unlisted attribute raises `AttributeError`. Also show that `Circle` does not have a `__dict__`.

??? success "Solution to Exercise 2"
        ```python
        class Shape:
            __slots__ = ('color',)

        class Circle(Shape):
            __slots__ = ('radius',)

            def __init__(self, color, radius):
                self.color = color
                self.radius = radius

        c = Circle('red', 5.0)
        print(f"color={c.color}, radius={c.radius}")

        # No dynamic attributes
        try:
            c.area = 78.5
        except AttributeError as e:
            print(f"AttributeError: {e}")

        # No __dict__
        print(f"Has __dict__: {hasattr(c, '__dict__')}")
        ```

---

**Exercise 3.**
Use `timeit` to compare attribute read/write speed between a slotted class and a regular class. Each class should have one attribute `x`. Run 10 million reads and 10 million writes for each and print the times and the percentage speedup from slots.

??? success "Solution to Exercise 3"
        ```python
        import timeit

        class Regular:
            def __init__(self):
                self.x = 0

        class Slotted:
            __slots__ = ('x',)
            def __init__(self):
                self.x = 0

        r = Regular()
        s = Slotted()
        n = 10_000_000

        # Read benchmark
        t_read_regular = timeit.timeit('r.x', globals={'r': r}, number=n)
        t_read_slotted = timeit.timeit('s.x', globals={'s': s}, number=n)

        # Write benchmark
        t_write_regular = timeit.timeit('r.x = 1', globals={'r': r}, number=n)
        t_write_slotted = timeit.timeit('s.x = 1', globals={'s': s}, number=n)

        print(f"Read  - Regular: {t_read_regular:.3f}s, Slotted: {t_read_slotted:.3f}s "
              f"({(1 - t_read_slotted / t_read_regular) * 100:.1f}% faster)")
        print(f"Write - Regular: {t_write_regular:.3f}s, Slotted: {t_write_slotted:.3f}s "
              f"({(1 - t_write_slotted / t_write_regular) * 100:.1f}% faster)")
        ```
