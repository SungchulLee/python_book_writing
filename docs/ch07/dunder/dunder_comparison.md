# Comparison Operators

Comparison dunder methods enable custom comparison logic and sorting for your objects.

## Basic Comparison Methods

### Equality: `__eq__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)

print(p1 == p2)  # True
print(p1 == p3)  # False
print(p1 == "not a point")  # False (NotImplemented → False)
```

### All Comparison Methods

| Method | Operator | Example |
|--------|----------|---------|
| `__eq__` | `==` | `a == b` |
| `__ne__` | `!=` | `a != b` |
| `__lt__` | `<` | `a < b` |
| `__le__` | `<=` | `a <= b` |
| `__gt__` | `>` | `a > b` |
| `__ge__` | `>=` | `a >= b` |

### Complete Implementation

```python
class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch
    
    def _to_tuple(self):
        return (self.major, self.minor, self.patch)
    
    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._to_tuple() == other._to_tuple()
    
    # __ne__ is NOT needed — Python automatically derives it from __eq__
    
    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._to_tuple() < other._to_tuple()
    
    def __le__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._to_tuple() <= other._to_tuple()
    
    def __gt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._to_tuple() > other._to_tuple()
    
    def __ge__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._to_tuple() >= other._to_tuple()
    
    def __repr__(self):
        return f"Version({self.major}, {self.minor}, {self.patch})"

v1 = Version(1, 0, 0)
v2 = Version(2, 0, 0)
v3 = Version(1, 5, 0)

print(v1 < v2)   # True
print(v1 < v3)   # True
print(v2 > v3)   # True
print(sorted([v2, v1, v3]))  # [Version(1, 0, 0), Version(1, 5, 0), Version(2, 0, 0)]
```

## Using @total_ordering

The `functools.total_ordering` decorator reduces boilerplate by deriving missing comparison methods from `__eq__` and one ordering method.

```python
from functools import total_ordering

@total_ordering
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade == other.grade
    
    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade < other.grade
    
    def __repr__(self):
        return f"Student({self.name!r}, {self.grade})"

# All comparisons work!
alice = Student("Alice", 90)
bob = Student("Bob", 85)
charlie = Student("Charlie", 90)

print(alice > bob)    # True  (derived from __lt__)
print(alice >= bob)   # True  (derived from __lt__ and __eq__)
print(alice <= bob)   # False (derived from __lt__ and __eq__)
print(alice == charlie)  # True
print(alice != bob)   # True  (derived from __eq__)
```

### How @total_ordering Works

You provide `__eq__` + one of (`__lt__`, `__le__`, `__gt__`, `__ge__`), and it derives the rest:

| You Implement | Decorator Derives |
|---------------|-------------------|
| `__eq__` + `__lt__` | `__le__`, `__gt__`, `__ge__` |
| `__eq__` + `__le__` | `__lt__`, `__gt__`, `__ge__` |
| `__eq__` + `__gt__` | `__lt__`, `__le__`, `__ge__` |
| `__eq__` + `__ge__` | `__lt__`, `__le__`, `__gt__` |

### Performance Note

```python
# @total_ordering has slight performance overhead
# For performance-critical code, implement all methods manually

# Or use __slots__ with manual implementation
class FastPoint:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
    
    def __le__(self, other):
        return (self.x, self.y) <= (other.x, other.y)
    
    def __gt__(self, other):
        return (self.x, self.y) > (other.x, other.y)
    
    def __ge__(self, other):
        return (self.x, self.y) >= (other.x, other.y)
```

!!! tip "Practical Advice"

    In practice, use `@total_ordering` unless you have a specific reason not to. Manual implementation of all six comparison methods is rarely needed — the two main exceptions are: (1) performance-critical code where the decorator's overhead matters (it wraps each derived method in an extra function call), and (2) non-standard comparison semantics where the derived methods would produce incorrect results. For the vast majority of classes, `__eq__` + `__lt__` + `@total_ordering` is the right choice.

## Hashing and Equality

Objects that compare equal **must** have equal hashes. Defining `__eq__` without `__hash__` is one of the most common dunder-method mistakes --- Python will set `__hash__` to `None`, making your objects unhashable (they cannot be used in sets or as dictionary keys). Always pair the two.

```python
class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    
    def __eq__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return (self.r, self.g, self.b) == (other.r, other.g, other.b)
    
    def __hash__(self):
        return hash((self.r, self.g, self.b))
    
    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"

# Now Color can be used in sets and as dict keys
red = Color(255, 0, 0)
also_red = Color(255, 0, 0)

colors = {red, also_red}
print(len(colors))  # 1 (same hash and equal)

color_names = {red: "red", Color(0, 255, 0): "green"}
print(color_names[also_red])  # "red"
```

### Hash Rules

```python
# Rule 1: Equal objects must have equal hashes
a == b  →  hash(a) == hash(b)

# Rule 2: Unequal objects CAN have equal hashes (collisions are OK)
hash(a) == hash(b)  ↛  a == b

# Rule 3: Mutable objects should not be hashable
# (their hash could change, breaking dict/set invariants)
```

### Making Objects Unhashable

```python
class MutablePoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if not isinstance(other, MutablePoint):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    # Explicitly make unhashable
    __hash__ = None

p = MutablePoint(1, 2)
# hash(p)  # TypeError: unhashable type: 'MutablePoint'
# {p}      # TypeError: unhashable type: 'MutablePoint'
```

## Identity vs Equality

```python
class Box:
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        if not isinstance(other, Box):
            return NotImplemented
        return self.value == other.value

a = Box(42)
b = Box(42)
c = a

# Equality (==) uses __eq__
print(a == b)  # True (same value)
print(a == c)  # True (same value)

# Identity (is) compares memory addresses
print(a is b)  # False (different objects)
print(a is c)  # True (same object)
```

## Comparing with None

```python
class OptionalValue:
    def __init__(self, value=None):
        self.value = value
    
    def __eq__(self, other):
        # Handle None comparison
        if other is None:
            return self.value is None
        if not isinstance(other, OptionalValue):
            return NotImplemented
        return self.value == other.value

empty = OptionalValue()
filled = OptionalValue(42)

print(empty == None)   # True
print(filled == None)  # False
```

## Comparison with Different Types

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    
    def __eq__(self, other):
        if isinstance(other, Temperature):
            return self.celsius == other.celsius
        if isinstance(other, (int, float)):
            return self.celsius == other
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Temperature):
            return self.celsius < other.celsius
        if isinstance(other, (int, float)):
            return self.celsius < other
        return NotImplemented

t = Temperature(20)
print(t == 20)              # True
print(t == Temperature(20)) # True
print(t < 25)               # True
print(t > Temperature(15))  # True
```

## Chained Comparisons

Python's chained comparisons (like `a < b < c`) work automatically:

```python
from functools import total_ordering

@total_ordering
class Score:
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        if not isinstance(other, Score):
            return NotImplemented
        return self.value == other.value
    
    def __lt__(self, other):
        if not isinstance(other, Score):
            return NotImplemented
        return self.value < other.value

low = Score(10)
mid = Score(50)
high = Score(90)

# Chained comparison
print(low < mid < high)  # True
# Equivalent to: low < mid and mid < high
```

## Practical Example: Priority Queue Item

```python
from functools import total_ordering

@total_ordering
class PriorityItem:
    """Item for priority queue with (priority, data) comparison."""
    
    _counter = 0  # Tie-breaker for equal priorities
    
    def __init__(self, priority, data):
        self.priority = priority
        self.data = data
        PriorityItem._counter += 1
        self._order = PriorityItem._counter
    
    def __eq__(self, other):
        if not isinstance(other, PriorityItem):
            return NotImplemented
        return (self.priority, self._order) == (other.priority, other._order)
    
    def __lt__(self, other):
        if not isinstance(other, PriorityItem):
            return NotImplemented
        # Lower priority number = higher priority
        # Earlier insertion = higher priority (for ties)
        return (self.priority, self._order) < (other.priority, other._order)
    
    def __repr__(self):
        return f"PriorityItem({self.priority}, {self.data!r})"

import heapq

tasks = []
heapq.heappush(tasks, PriorityItem(2, "low priority"))
heapq.heappush(tasks, PriorityItem(1, "high priority"))
heapq.heappush(tasks, PriorityItem(1, "also high priority"))

while tasks:
    item = heapq.heappop(tasks)
    print(item)

# Output:
# PriorityItem(1, 'high priority')
# PriorityItem(1, 'also high priority')
# PriorityItem(2, 'low priority')
```

## Sorting Custom Objects

```python
from functools import total_ordering

@total_ordering
class Employee:
    def __init__(self, name, salary, years):
        self.name = name
        self.salary = salary
        self.years = years
    
    def __eq__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        return (self.salary, self.years) == (other.salary, other.years)
    
    def __lt__(self, other):
        if not isinstance(other, Employee):
            return NotImplemented
        # Sort by salary (desc), then years (desc)
        return (-self.salary, -self.years) < (-other.salary, -other.years)
    
    def __repr__(self):
        return f"Employee({self.name!r}, ${self.salary}, {self.years}y)"

employees = [
    Employee("Alice", 75000, 5),
    Employee("Bob", 80000, 3),
    Employee("Charlie", 75000, 8),
]

# Using default sort (uses __lt__)
for emp in sorted(employees):
    print(emp)

# Output:
# Employee('Bob', \$80000, 3y)
# Employee('Charlie', \$75000, 8y)
# Employee('Alice', \$75000, 5y)
```

## Key Takeaways

- Implement `__eq__` for equality; Python provides `__ne__` automatically
- Use `@total_ordering` to avoid boilerplate—just implement `__eq__` and one of `__lt__`, `__le__`, `__gt__`, `__ge__`
- Return `NotImplemented` (not `False`) for unsupported types
- If you define `__eq__`, also define `__hash__` for hashable objects
- Set `__hash__ = None` for mutable objects that shouldn't be hashable
- Tuple comparison is a clean way to implement multi-field comparisons
- Identity (`is`) and equality (`==`) are different concepts

---

## Runnable Example: `comparison_operators_tutorial.py`

```python
"""
Example 2: Comparison Operators
Demonstrates: __eq__, __ne__, __lt__, __le__, __gt__, __ge__
"""


class Student:
    """A student with grade-based comparisons."""
    
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade
    
    def __repr__(self):
        return f"Student('{self.name}', {self.grade})"
    
    def __eq__(self, other):
        """Check if two students have the same grade."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade == other.grade
    
    def __ne__(self, other):
        """Check if two students have different grades."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade != other.grade
    
    def __lt__(self, other):
        """Check if this student's grade is less than another's."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade < other.grade
    
    def __le__(self, other):
        """Check if this student's grade is less than or equal to another's."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade <= other.grade
    
    def __gt__(self, other):
        """Check if this student's grade is greater than another's."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade > other.grade
    
    def __ge__(self, other):
        """Check if this student's grade is greater than or equal to another's."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.grade >= other.grade


class Version:
    """A version class that can be compared (e.g., 1.2.3)."""
    
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch
    
    def __repr__(self):
        return f"Version({self.major}, {self.minor}, {self.patch})"
    
    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"
    
    def _as_tuple(self):
        """Convert to tuple for easy comparison."""
        return (self.major, self.minor, self.patch)
    
    def __eq__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._as_tuple() == other._as_tuple()
    
    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._as_tuple() < other._as_tuple()
    
    def __le__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._as_tuple() <= other._as_tuple()
    
    def __gt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._as_tuple() > other._as_tuple()
    
    def __ge__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        return self._as_tuple() >= other._as_tuple()


# Examples
if __name__ == "__main__":

    # ============================================================================
    print("=== Student Comparison Examples ===")
    alice = Student("Alice", 85)
    bob = Student("Bob", 92)
    charlie = Student("Charlie", 85)
    
    print(f"{alice.name}: {alice.grade}")
    print(f"{bob.name}: {bob.grade}")
    print(f"{charlie.name}: {charlie.grade}")
    
    print(f"\nAlice == Charlie: {alice == charlie}")
    print(f"Alice == Bob: {alice == bob}")
    print(f"Alice < Bob: {alice < bob}")
    print(f"Bob > Alice: {bob > alice}")
    print(f"Alice <= Charlie: {alice <= charlie}")
    
    # Sorting students by grade
    students = [bob, alice, charlie, Student("David", 78), Student("Eve", 95)]
    print("\n=== Sorting Students ===")
    print("Original:", students)
    sorted_students = sorted(students)
    print("Sorted by grade:", sorted_students)
    
    print("\n\n=== Version Comparison Examples ===")
    v1 = Version(1, 2, 3)
    v2 = Version(1, 2, 4)
    v3 = Version(2, 0, 0)
    v4 = Version(1, 2, 3)
    
    print(f"v1: {v1}")
    print(f"v2: {v2}")
    print(f"v3: {v3}")
    print(f"v4: {v4}")
    
    print(f"\nv1 == v4: {v1 == v4}")
    print(f"v1 < v2: {v1 < v2}")
    print(f"v2 < v3: {v2 < v3}")
    print(f"v3 > v1: {v3 > v1}")
    
    versions = [v3, v1, v2, Version(0, 9, 5)]
    print("\n=== Sorting Versions ===")
    print("Original:", versions)
    print("Sorted:", sorted(versions))
```


---

## Runnable Example: `hash_eq_slots_example.py`

```python
"""
Magic Methods: __hash__, __eq__, and __slots__

When using custom objects in sets or as dict keys, Python needs:
- __hash__() to compute a hash code (for bucket placement)
- __eq__() to check if two objects are "equal"

Rule: Objects that compare equal MUST have the same hash.
      Same hash does NOT mean equal (hash collisions exist).

Topics covered:
- __hash__ and __eq__ for hashable objects
- __slots__ for memory-efficient classes
- __setitem__ and __getitem__ for container-like classes

Based on concepts from Python-100-Days example16 and ch06/dunder materials.
"""


# =============================================================================
# Example 1: Making Objects Hashable
# =============================================================================

class Student:
    """A student that can be used in sets and as dict keys.

    __slots__ restricts attributes to save memory.
    __hash__ and __eq__ make instances hashable.

    >>> s1 = Student(1001, 'Alice')
    >>> s2 = Student(1001, 'Alice')
    >>> s1 == s2
    True
    >>> hash(s1) == hash(s2)
    True
    >>> s1 is s2  # Different objects
    False
    """
    __slots__ = ('student_id', 'name', 'grade')

    def __init__(self, student_id: int, name: str):
        self.student_id = student_id
        self.name = name

    def __hash__(self) -> int:
        """Hash based on student_id and name.

        Must be consistent with __eq__: if a == b, then hash(a) == hash(b).
        Using tuple hashing is a clean pattern.
        """
        return hash((self.student_id, self.name))

    def __eq__(self, other) -> bool:
        """Two students are equal if they have the same ID and name."""
        if not isinstance(other, Student):
            return NotImplemented
        return (self.student_id == other.student_id and
                self.name == other.name)

    def __str__(self):
        return f'{self.student_id}: {self.name}'

    def __repr__(self):
        return f'Student({self.student_id}, {self.name!r})'


def demo_hashable():
    """Demonstrate hashable objects in sets and dicts."""
    print("=== Hashable Objects in Sets ===")

    students = set()
    students.add(Student(1001, 'Alice'))
    students.add(Student(1001, 'Alice'))  # Duplicate - won't be added
    students.add(Student(1002, 'Bob'))

    print(f"Set size: {len(students)} (added 3, but 2 unique)")
    print(f"Students: {students}")
    print()


# =============================================================================
# Example 2: __slots__ for Memory Efficiency
# =============================================================================

def demo_slots():
    """Demonstrate __slots__ behavior."""
    print("=== __slots__ Behavior ===")

    stu = Student(1234, 'Charlie')
    stu.grade = 'A'  # OK - 'grade' is in __slots__
    print(f"Student: {stu}, Grade: {stu.grade}")

    try:
        stu.email = 'charlie@example.com'  # Error - not in __slots__
    except AttributeError as e:
        print(f"AttributeError: {e}")

    print(f"Allowed attributes: {Student.__slots__}")
    print(f"Has __dict__: {hasattr(stu, '__dict__')}")  # False with __slots__
    print()


# =============================================================================
# Example 3: Container-Like Class with __setitem__ and __getitem__
# =============================================================================

class Registry:
    """A registry that stores items by key using dict-like syntax.

    Implements __setitem__ and __getitem__ so you can use
    bracket notation: registry[key] = value
    """

    def __init__(self, name: str):
        self.name = name
        self._items: dict = {}

    def __setitem__(self, key, value):
        """Enable registry[key] = value syntax."""
        self._items[key] = value

    def __getitem__(self, key):
        """Enable registry[key] syntax."""
        return self._items[key]

    def __contains__(self, key) -> bool:
        """Enable 'key in registry' syntax."""
        return key in self._items

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self):
        return f"Registry('{self.name}', {len(self)} items)"


def demo_container():
    """Demonstrate container-like class usage."""
    print("=== Container Protocol (__setitem__, __getitem__) ===")

    school = Registry('Python Academy')
    school[1001] = Student(1001, 'Alice')
    school[1002] = Student(1002, 'Bob')
    school[1003] = Student(1003, 'Charlie')

    print(f"Registry: {school}")
    print(f"school[1002] = {school[1002]}")
    print(f"1003 in school: {1003 in school}")
    print(f"9999 in school: {9999 in school}")
    print()


# =============================================================================
# Example 4: Why Both __hash__ and __eq__ Matter
# =============================================================================

def demo_hash_eq_relationship():
    """Explain the relationship between __hash__ and __eq__."""
    print("=== Hash and Equality Relationship ===")

    s1 = Student(1001, 'Alice')
    s2 = Student(1001, 'Alice')
    s3 = Student(1001, 'Bob')

    print(f"s1 = {s1!r}")
    print(f"s2 = {s2!r}")
    print(f"s3 = {s3!r}")
    print()

    print(f"s1 == s2: {s1 == s2}  (same id and name)")
    print(f"s1 is s2: {s1 is s2}  (different objects)")
    print(f"hash(s1) == hash(s2): {hash(s1) == hash(s2)}  (equal -> same hash)")
    print()

    print(f"s1 == s3: {s1 == s3}  (different name)")
    print(f"hash(s1) == hash(s3): {hash(s1) == hash(s3)}  (may differ)")

    print()
    print("Rules:")
    print("  1. Equal objects MUST have the same hash")
    print("  2. Same hash does NOT mean equal (collisions)")
    print("  3. If you define __eq__, define __hash__ too")
    print("  4. Mutable objects generally should NOT be hashable")


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    demo_hashable()
    demo_slots()
    demo_container()
    demo_hash_eq_relationship()
```

---

## Exercises

**Exercise 1.**
Create a `Version` class with `major`, `minor`, and `patch` fields. Implement `__eq__`, `__lt__`, and use `functools.total_ordering` to get the remaining comparison operators. Show that versions can be sorted: `Version(2, 0, 0) > Version(1, 9, 9)`.

??? success "Solution to Exercise 1"

        from functools import total_ordering

        @total_ordering
        class Version:
            def __init__(self, major, minor, patch):
                self.major = major
                self.minor = minor
                self.patch = patch

            def __eq__(self, other):
                return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

            def __lt__(self, other):
                return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

            def __repr__(self):
                return f"Version({self.major}, {self.minor}, {self.patch})"

        versions = [Version(2, 0, 0), Version(1, 9, 9), Version(1, 10, 0), Version(2, 0, 1)]
        print(sorted(versions))
        # [Version(1, 9, 9), Version(1, 10, 0), Version(2, 0, 0), Version(2, 0, 1)]
        print(Version(2, 0, 0) > Version(1, 9, 9))  # True

---

**Exercise 2.**
Write a `Student` class with `name` and `gpa`. Implement `__eq__` (comparing by name and gpa) and `__hash__` (so students can be stored in sets). Also implement `__lt__` based on gpa for sorting. Show students in a sorted list and a set with duplicates removed.

??? success "Solution to Exercise 2"

        class Student:
            def __init__(self, name, gpa):
                self.name = name
                self.gpa = gpa

            def __eq__(self, other):
                return self.name == other.name and self.gpa == other.gpa

            def __hash__(self):
                return hash((self.name, self.gpa))

            def __lt__(self, other):
                return self.gpa < other.gpa

            def __repr__(self):
                return f"Student('{self.name}', {self.gpa})"

        students = [Student("Alice", 3.8), Student("Bob", 3.5),
                     Student("Alice", 3.8), Student("Charlie", 3.9)]
        print(sorted(students))
        unique = set(students)
        print(len(unique))  # 3 — duplicate Alice removed

---

**Exercise 3.**
Build a `Temperature` class with a `value` and `scale` ("C" or "F"). Implement comparison operators that convert to a common scale before comparing. For example, `Temperature(32, "F") == Temperature(0, "C")` should be `True`. Use `functools.total_ordering`.

??? success "Solution to Exercise 3"

        from functools import total_ordering

        @total_ordering
        class Temperature:
            def __init__(self, value, scale="C"):
                self.value = value
                self.scale = scale

            def _to_celsius(self):
                if self.scale == "C":
                    return self.value
                return (self.value - 32) * 5 / 9

            def __eq__(self, other):
                return abs(self._to_celsius() - other._to_celsius()) < 1e-9

            def __lt__(self, other):
                return self._to_celsius() < other._to_celsius()

            def __repr__(self):
                return f"Temperature({self.value}, '{self.scale}')"

        print(Temperature(32, "F") == Temperature(0, "C"))   # True
        print(Temperature(212, "F") == Temperature(100, "C")) # True
        print(Temperature(100, "C") > Temperature(200, "F"))  # True
