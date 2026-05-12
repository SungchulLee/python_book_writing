# namedtuple

A **namedtuple** is a tuple subclass with named fields. It combines the immutability of tuples with the readability of classes.

!!! tip "Mental Model"
    A `namedtuple` is a lightweight, immutable record — like a `struct` in C or a row in a spreadsheet. You get the memory efficiency and hashability of a tuple, but you access fields by name (`point.x`) instead of by cryptic index (`point[0]`). Use it whenever you need a simple data container without the overhead of a full class.

---

## Creating Named Tuples

```python
from collections import namedtuple

# Define the type
Scientist = namedtuple('Scientist', ['name', 'field', 'born', 'nobel'])

# Create instances
marie = Scientist('Marie Curie', 'physics', 1867, True)
einstein = Scientist(name='Albert Einstein', field='physics', born=1879, nobel=True)
```

### Alternative Field Definitions

```python
# Space-separated string
Point = namedtuple('Point', 'x y z')

# Comma-separated string
RGB = namedtuple('RGB', 'red, green, blue')

# List of strings
Person = namedtuple('Person', ['name', 'age', 'city'])
```

---

## Accessing Fields

### By Name (like class)

```python
Scientist = namedtuple('Scientist', ['name', 'field', 'born', 'nobel'])
s = Scientist('Marie Curie', 'physics', 1867, True)

print(s.name)       # Marie Curie
print(s.field)      # physics
print(s.born)       # 1867
print(s.nobel)      # True
```

### By Index (like tuple)

```python
print(s[0])         # Marie Curie
print(s[1])         # physics
print(s[-1])        # True
```

### Slicing

```python
print(s[:2])        # ('Marie Curie', 'physics')
print(s[1:3])       # ('physics', 1867)
```

---

## Immutability

Named tuples are **immutable** like regular tuples:

```python
s = Scientist('Marie Curie', 'physics', 1867, True)

s.name = 'M Curie'  # AttributeError: can't set attribute
s[0] = 'M Curie'    # TypeError: 'Scientist' object does not support item assignment
```

### Creating Modified Copies

Use `_replace()` to create a new instance with some fields changed:

```python
s = Scientist('Marie Curie', 'physics', 1867, True)
s2 = s._replace(name='M. Curie', born=1867)
print(s2)           # Scientist(name='M. Curie', field='physics', born=1867, nobel=True)
print(s)            # Original unchanged
```

---

## Comparison with Regular Class

### Regular Class (Mutable)

```python
class Scientist:
    def __init__(self, name, field, born, nobel):
        self.name = name
        self.field = field
        self.born = born
        self.nobel = nobel

s = Scientist('Marie Curie', 'physics', 1867, True)
s.name = 'M Curie'  # Works! (mutable)
```

### namedtuple (Immutable)

```python
from collections import namedtuple
Scientist = namedtuple('Scientist', ['name', 'field', 'born', 'nobel'])

s = Scientist('Marie Curie', 'physics', 1867, True)
s.name = 'M Curie'  # AttributeError (immutable)
```

---

## Utility Methods

Named tuples provide special methods (prefixed with `_`):

### `_fields`

```python
print(Scientist._fields)    # ('name', 'field', 'born', 'nobel')
```

### `_asdict()`

```python
s = Scientist('Marie Curie', 'physics', 1867, True)
print(s._asdict())
# {'name': 'Marie Curie', 'field': 'physics', 'born': 1867, 'nobel': True}
```

### `_make(iterable)`

```python
data = ['Albert Einstein', 'physics', 1879, True]
einstein = Scientist._make(data)
print(einstein)     # Scientist(name='Albert Einstein', ...)
```

---

## Default Values

Use `defaults` parameter (Python 3.7+):

```python
Scientist = namedtuple('Scientist', ['name', 'field', 'born', 'nobel'], 
                       defaults=[None, False])

# 'born' defaults to None, 'nobel' defaults to False
s = Scientist('Marie Curie', 'physics')
print(s)            # Scientist(name='Marie Curie', field='physics', born=None, nobel=False)
```

---

## Use Cases

### Function Return Values

```python
def get_user_info(user_id):
    UserInfo = namedtuple('UserInfo', ['name', 'email', 'active'])
    return UserInfo('Alice', 'alice@example.com', True)

info = get_user_info(123)
print(info.name)    # Alice (more readable than info[0])
```

### Database Records

```python
Row = namedtuple('Row', ['id', 'name', 'price'])
products = [
    Row(1, 'Apple', 1.50),
    Row(2, 'Banana', 0.75),
]
for p in products:
    print(f"{p.name}: ${p.price}")
```

### Coordinates and Points

```python
Point = namedtuple('Point', ['x', 'y'])
p1 = Point(3, 4)
p2 = Point(0, 0)
distance = ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5
```

---

## namedtuple vs typing.NamedTuple

For type hints, use `typing.NamedTuple`:

```python
from typing import NamedTuple

class Scientist(NamedTuple):
    name: str
    field: str
    born: int
    nobel: bool = False     # Default value

s = Scientist('Marie Curie', 'physics', 1867)
print(s.nobel)              # False
```

---

## Summary

| Feature | tuple | namedtuple | class |
|---------|-------|------------|-------|
| Access by index | ✅ | ✅ | ❌ |
| Access by name | ❌ | ✅ | ✅ |
| Mutable | ❌ | ❌ | ✅ |
| Hashable | ✅ | ✅ | Depends |
| Memory | Low | Low | Higher |

**Use namedtuple when:**

- You need readable field names
- Immutability is desired
- Memory efficiency matters
- Simple data container without methods

---

## Exercises

**Exercise 1.**
Define a `Color` namedtuple with fields `name`, `hex_code`, and `rgb` (a tuple of three ints). Create a list of at least three colors and write a function `find_by_name` that takes the list and a color name string and returns the matching `Color` or `None`. For example, `find_by_name(colors, "red")` should return the red Color instance.

??? success "Solution to Exercise 1"

    ```python
    from collections import namedtuple

    Color = namedtuple('Color', ['name', 'hex_code', 'rgb'])

    colors = [
        Color('red', '#FF0000', (255, 0, 0)),
        Color('green', '#00FF00', (0, 255, 0)),
        Color('blue', '#0000FF', (0, 0, 255)),
    ]

    def find_by_name(color_list, name):
        for color in color_list:
            if color.name == name:
                return color
        return None

    # Test
    print(find_by_name(colors, "red"))
    # Color(name='red', hex_code='#FF0000', rgb=(255, 0, 0))
    print(find_by_name(colors, "yellow"))
    # None
    ```

---

**Exercise 2.**
Write a function `csv_to_namedtuples` that takes a CSV-formatted string (with a header row) and returns a list of namedtuples, where the namedtuple type is created dynamically from the header. For example, given `"name,age\nAlice,30\nBob,25"`, it should return a list of `Row(name='Alice', age='30')` and `Row(name='Bob', age='25')`.

??? success "Solution to Exercise 2"

    ```python
    from collections import namedtuple

    def csv_to_namedtuples(csv_string):
        lines = csv_string.strip().split('\n')
        headers = lines[0].split(',')
        Row = namedtuple('Row', headers)
        result = []
        for line in lines[1:]:
            values = line.split(',')
            result.append(Row._make(values))
        return result

    # Test
    csv_data = "name,age\nAlice,30\nBob,25"
    rows = csv_to_namedtuples(csv_data)
    for row in rows:
        print(row)
    # Row(name='Alice', age='30')
    # Row(name='Bob', age='25')
    print(rows[0].name)  # Alice
    ```

---

**Exercise 3.**
Define a `Point` namedtuple with fields `x` and `y`. Write a function `translate` that takes a `Point` and two offsets `dx` and `dy`, and returns a new `Point` shifted by those offsets using `_replace()`. Then write a function `distance` that takes two `Point` instances and returns the Euclidean distance between them.

??? success "Solution to Exercise 3"

    ```python
    from collections import namedtuple
    import math

    Point = namedtuple('Point', ['x', 'y'])

    def translate(point, dx, dy):
        return point._replace(x=point.x + dx, y=point.y + dy)

    def distance(p1, p2):
        return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    # Test
    p = Point(3, 4)
    moved = translate(p, 1, -2)
    print(moved)  # Point(x=4, y=2)

    origin = Point(0, 0)
    print(distance(p, origin))  # 5.0
    ```
