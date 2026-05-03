# functools.total_ordering

The `@total_ordering` class decorator auto-generates missing comparison methods. Define `__eq__` and **one** of `__lt__`, `__le__`, `__gt__`, or `__gt__`, and `total_ordering` fills in the remaining four.

!!! tip "Mental Model"
    If you can test equality and one ordering direction, the other comparisons are logically derivable. `@total_ordering` does that derivation for you: define `__eq__` plus any one of `__lt__`/`__le__`/`__gt__`/`__ge__`, and the decorator fills in the rest. It trades a small runtime cost for eliminating four boilerplate methods.

```python
from functools import total_ordering
```

---

## The Problem

Python's comparison operators each map to a separate dunder method:

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other):
        return self.celsius == other.celsius

    def __lt__(self, other):
        return self.celsius < other.celsius

    def __le__(self, other):
        return self.celsius <= other.celsius

    def __gt__(self, other):
        return self.celsius > other.celsius

    def __ge__(self, other):
        return self.celsius >= other.celsius

# 5 methods for 6 operators (__ne__ auto-derives from __eq__)
# This is tedious and error-prone
```

---

## The Solution

```python
from functools import total_ordering

@total_ordering
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other):
        return self.celsius == other.celsius

    def __lt__(self, other):
        return self.celsius < other.celsius

# All six comparisons now work
t1 = Temperature(20)
t2 = Temperature(25)

print(t1 < t2)   # True  (defined)
print(t1 <= t2)  # True  (auto-generated)
print(t1 > t2)   # False (auto-generated)
print(t1 >= t2)  # False (auto-generated)
print(t1 == t2)  # False (defined)
print(t1 != t2)  # True  (auto from __eq__)
```

---

## Requirements

You must define exactly:

1. `__eq__` — always required
2. **One** of: `__lt__`, `__le__`, `__gt__`, `__ge__`

```python
from functools import total_ordering

# Any one of these works with __eq__:

@total_ordering
class A:
    def __eq__(self, other): ...
    def __lt__(self, other): ...  # Option 1 (most common)

@total_ordering
class B:
    def __eq__(self, other): ...
    def __le__(self, other): ...  # Option 2

@total_ordering
class C:
    def __eq__(self, other): ...
    def __gt__(self, other): ...  # Option 3

@total_ordering
class D:
    def __eq__(self, other): ...
    def __ge__(self, other): ...  # Option 4
```

### Missing __eq__ Raises Error

```python
from functools import total_ordering

@total_ordering
class Bad:
    def __lt__(self, other): ...

# ValueError: must have at least one ordering operation defined
```

---

## How Auto-Generation Works

Given `__eq__` and `__lt__`, the decorator derives:

| Method | Derived As |
|--------|-----------|
| `__le__(a, b)` | `a < b or a == b` |
| `__gt__(a, b)` | `not (a < b or a == b)` |
| `__ge__(a, b)` | `not (a < b)` |

```python
# Conceptually equivalent to:
def __le__(self, other):
    return self.__lt__(other) or self.__eq__(other)

def __gt__(self, other):
    return not self.__le__(other)

def __ge__(self, other):
    return not self.__lt__(other)
```

---

## Practical Examples

### Version Comparison

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, version_string):
        self.parts = tuple(int(p) for p in version_string.split('.'))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

    def __repr__(self):
        return f"Version({'.'.join(map(str, self.parts))})"

versions = [Version("2.0"), Version("1.10"), Version("1.2"), Version("3.0")]
print(sorted(versions))
# [Version(1.2), Version(1.10), Version(2.0), Version(3.0)]

print(Version("1.2") < Version("1.10"))   # True
print(Version("2.0") >= Version("1.10"))  # True
```

### Money Type

```python
from functools import total_ordering

@total_ordering
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other):
        if self.currency != other.currency:
            return NotImplemented
        return self.amount == other.amount

    def __lt__(self, other):
        if self.currency != other.currency:
            return NotImplemented
        return self.amount < other.amount

    def __repr__(self):
        return f"Money({self.amount}, '{self.currency}')"

m1 = Money(100)
m2 = Money(200)
m3 = Money(100, "EUR")

print(m1 < m2)   # True
print(m1 >= m2)  # False
print(sorted([m2, m1]))  # [Money(100, 'USD'), Money(200, 'USD')]

# Different currencies: returns NotImplemented → TypeError
# print(m1 < m3)  # TypeError
```

### Student Grades

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa

    def __eq__(self, other):
        return self.gpa == other.gpa

    def __lt__(self, other):
        return self.gpa < other.gpa

    def __repr__(self):
        return f"{self.name}({self.gpa})"

students = [Student("Alice", 3.8), Student("Bob", 3.5), Student("Charlie", 3.9)]
print(sorted(students))
# [Bob(3.5), Alice(3.8), Charlie(3.9)]
print(max(students))
# Charlie(3.9)
```

### Priority Queue Item

```python
from functools import total_ordering

@total_ordering
class Task:
    def __init__(self, priority, description):
        self.priority = priority
        self.description = description

    def __eq__(self, other):
        return self.priority == other.priority

    def __lt__(self, other):
        # Lower number = higher priority
        return self.priority < other.priority

    def __repr__(self):
        return f"Task(p={self.priority}, '{self.description}')"

tasks = [Task(3, "Low"), Task(1, "Critical"), Task(2, "Normal")]
print(sorted(tasks))
# [Task(p=1, 'Critical'), Task(p=2, 'Normal'), Task(p=3, 'Low')]
```

---

## Returning NotImplemented

When comparing incompatible types, return `NotImplemented` to let Python try the reflected operation:

```python
from functools import total_ordering

@total_ordering
class Celsius:
    def __init__(self, temp):
        self.temp = temp

    def __eq__(self, other):
        if not isinstance(other, Celsius):
            return NotImplemented
        return self.temp == other.temp

    def __lt__(self, other):
        if not isinstance(other, Celsius):
            return NotImplemented
        return self.temp < other.temp

c = Celsius(100)
print(c == Celsius(100))  # True
print(c == "100")         # False (Python handles NotImplemented)
print(c < Celsius(200))   # True
# print(c < "200")        # TypeError (no reflected operation available)
```

---

## Performance Considerations

Auto-generated methods involve an extra function call and boolean logic:

```python
# Hand-written __le__ (1 comparison):
def __le__(self, other):
    return self.celsius <= other.celsius

# Auto-generated __le__ (2 comparisons):
# Effectively: self.__lt__(other) or self.__eq__(other)
```

For most applications, this overhead is negligible. For **performance-critical** sorting of millions of objects, consider defining all methods manually:

```python
# Performance-critical: define all methods
class FastTemperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def __eq__(self, other): return self.celsius == other.celsius
    def __ne__(self, other): return self.celsius != other.celsius
    def __lt__(self, other): return self.celsius < other.celsius
    def __le__(self, other): return self.celsius <= other.celsius
    def __gt__(self, other): return self.celsius > other.celsius
    def __ge__(self, other): return self.celsius >= other.celsius
```

---

## total_ordering vs Manual Implementation

| Aspect | `@total_ordering` | Manual |
|--------|-------------------|--------|
| Code | 2 methods | 5-6 methods |
| Consistency | Guaranteed | Possible bugs |
| Performance | Slight overhead | Optimal |
| Maintenance | Easy | Must update all methods |
| Best for | Most classes | Performance-critical sorting |

---

## Relationship to __lt__ and sorted()

Python's `sorted()` and `list.sort()` use `__lt__` by default:

```python
from functools import total_ordering

@total_ordering
class Item:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

# sorted() works because __lt__ is defined
items = [Item(3), Item(1), Item(2)]
sorted(items)  # Uses __lt__ internally
```

If you only need sorting (not general comparisons), defining just `__lt__` is sufficient without `@total_ordering`.

---

## Common Pitfalls

### Inconsistent Equality and Ordering

```python
from functools import total_ordering

@total_ordering
class Bad:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x  # Compares only x

    def __lt__(self, other):
        return self.y < other.y   # Orders by y

# Contradictory: a == b but a < b is possible!
a = Bad(1, 10)
b = Bad(1, 5)
print(a == b)  # True (same x)
print(a < b)   # False (a.y > b.y) — contradicts equality!
```

**Rule**: `__eq__` and `__lt__` should use the same attributes.

### Forgetting __hash__

If you define `__eq__`, Python sets `__hash__` to `None`, making instances unhashable:

```python
@total_ordering
class Item:
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        return self.value == other.value
    def __lt__(self, other):
        return self.value < other.value

# {Item(1)}  # TypeError: unhashable type
# Fix: define __hash__
    def __hash__(self):
        return hash(self.value)
```

---

## Summary

| Feature | Details |
|---------|---------|
| Import | `from functools import total_ordering` |
| Requires | `__eq__` + one of `__lt__`, `__le__`, `__gt__`, `__ge__` |
| Generates | The remaining 3 comparison methods |
| Performance | Slight overhead vs manual implementation |
| Use case | Any class that needs full comparison support |

**Key Takeaways**:

- `@total_ordering` eliminates boilerplate: define 2 methods, get 6 comparisons
- Always define `__eq__` and `__lt__` (most common and expected pair)
- Use the same attributes in `__eq__` and `__lt__` to avoid contradictions
- Return `NotImplemented` for incompatible types
- Define `__hash__` if instances need to go in sets or dict keys
- For performance-critical sorting of millions of objects, define all methods manually
- If you only need `sorted()` support, `__lt__` alone suffices without `@total_ordering`

---

## Exercises

**Exercise 1.**
Create a `Temperature` class with a `celsius` attribute. Use `@total_ordering` and define only `__eq__` and `__lt__`. Verify that all six comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`) work between two `Temperature` instances.

??? success "Solution to Exercise 1"

        from functools import total_ordering

        @total_ordering
        class Temperature:
            def __init__(self, celsius):
                self.celsius = celsius

            def __eq__(self, other):
                if not isinstance(other, Temperature):
                    return NotImplemented
                return self.celsius == other.celsius

            def __lt__(self, other):
                if not isinstance(other, Temperature):
                    return NotImplemented
                return self.celsius < other.celsius

            def __repr__(self):
                return f"Temperature({self.celsius})"

        t1 = Temperature(20)
        t2 = Temperature(30)

        print(t1 == t2)   # False
        print(t1 != t2)   # True
        print(t1 < t2)    # True
        print(t1 <= t2)   # True
        print(t1 > t2)    # False
        print(t1 >= t2)   # False

---

**Exercise 2.**
Build a `Version` class that represents semantic versions (e.g., `Version(1, 2, 3)` for `1.2.3`). Use `@total_ordering` with `__eq__` and `__lt__` comparing `(major, minor, patch)` tuples. Sort a list of versions and verify the order.

??? success "Solution to Exercise 2"

        from functools import total_ordering

        @total_ordering
        class Version:
            def __init__(self, major, minor, patch):
                self.major = major
                self.minor = minor
                self.patch = patch

            def _key(self):
                return (self.major, self.minor, self.patch)

            def __eq__(self, other):
                if not isinstance(other, Version):
                    return NotImplemented
                return self._key() == other._key()

            def __lt__(self, other):
                if not isinstance(other, Version):
                    return NotImplemented
                return self._key() < other._key()

            def __repr__(self):
                return f"{self.major}.{self.minor}.{self.patch}"

        versions = [Version(2, 0, 0), Version(1, 9, 1), Version(1, 10, 0), Version(1, 9, 0)]
        print(sorted(versions))
        # [1.9.0, 1.9.1, 1.10.0, 2.0.0]

---

**Exercise 3.**
Create a `Student` class with `name` and `gpa` attributes. Use `@total_ordering`, comparing by `gpa`. Define `__hash__` based on `name` so students can be stored in a set. Demonstrate sorting a list of students and adding them to a set.

??? success "Solution to Exercise 3"

        from functools import total_ordering

        @total_ordering
        class Student:
            def __init__(self, name, gpa):
                self.name = name
                self.gpa = gpa

            def __eq__(self, other):
                if not isinstance(other, Student):
                    return NotImplemented
                return self.gpa == other.gpa

            def __lt__(self, other):
                if not isinstance(other, Student):
                    return NotImplemented
                return self.gpa < other.gpa

            def __hash__(self):
                return hash(self.name)

            def __repr__(self):
                return f"Student({self.name!r}, {self.gpa})"

        students = [Student("Alice", 3.8), Student("Bob", 3.5), Student("Charlie", 3.9)]
        print(sorted(students))
        # [Student('Bob', 3.5), Student('Alice', 3.8), Student('Charlie', 3.9)]

        student_set = set(students)
        print(student_set)  # All three (unique names)
