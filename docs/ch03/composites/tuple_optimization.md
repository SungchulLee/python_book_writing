# tuple Optimization

Tuples are optimized in CPython through tuple interning and caching, making them faster for hashable collections and reducing memory usage. Understanding these optimizations explains why tuples are preferred for immutable sequences and dictionary keys.

!!! tip "Mental Model"
    Because tuples are immutable, CPython can cache and reuse them aggressively. Small tuples with constant elements may be interned (shared across your program), and freed tuples are recycled from a free list instead of being garbage-collected. This makes tuple creation and destruction significantly cheaper than list equivalents.

---

## Tuple Interning

### Small Tuple Caching

```python
a = (1, 2, 3)
b = (1, 2, 3)
print(f"Same object: {a is b}")

c = tuple([1, 2, 3])
print(f"Constructed tuple same: {a is c}")
```

Output:
```
Same object: True
Constructed tuple same: False
```

### String Tuple Interning

```python
t1 = ("hello", "world")
t2 = ("hello", "world")
print(f"String tuples same: {t1 is t2}")
```

Output:
```
String tuples same: True
```

## Memory Efficiency

### Tuple vs List Comparison

```python
import sys

t = (1, 2, 3, 4, 5)
l = [1, 2, 3, 4, 5]

print(f"Tuple size: {sys.getsizeof(t)} bytes")
print(f"List size: {sys.getsizeof(l)} bytes")
```

Output:
```
Tuple size: 56 bytes
List size: 64 bytes
```

## Tuple Unpacking Optimization

### Fast Unpacking

```python
def swap(a, b):
    return b, a

x = 1
y = 2
x, y = swap(x, y)
print(f"Swapped: x={x}, y={y}")
```

Output:
```
Swapped: x=2, y=1
```

## Practical Advantages

### Hashable for Dictionaries

```python
# Tuples can be dict keys
coordinates = {
    (0, 0): "origin",
    (1, 0): "right",
    (0, 1): "up"
}

print(coordinates[(1, 0)])
```

Output:
```
right
```

### Function Return Optimization

```python
def get_coordinates():
    return 10, 20

x, y = get_coordinates()
print(f"Coordinates: ({x}, {y})")
```

Output:
```
Coordinates: (10, 20)
```

---

## Exercises


**Exercise 1.**
Compare the memory usage of a tuple and a list containing the same 1000 integers using `sys.getsizeof()`. Which uses less memory and why?

??? success "Solution to Exercise 1"

        ```python
        import sys

        data = list(range(1000))
        t = tuple(data)
        l = list(data)

        print(f"Tuple: {sys.getsizeof(t)} bytes")
        print(f"List:  {sys.getsizeof(l)} bytes")
        ```

    Tuples use less memory because they are fixed-size and do not need to store extra capacity for potential growth. Lists allocate extra space to support efficient appending.

---

**Exercise 2.**
Demonstrate that tuples are hashable (and can be used as dictionary keys) while lists are not. Create a dictionary that maps (x, y) coordinate tuples to city names.

??? success "Solution to Exercise 2"

        ```python
        cities = {
            (37.5665, 126.9780): "Seoul",
            (35.6762, 139.6503): "Tokyo",
            (40.7128, -74.0060): "New York",
        }

        print(cities[(37.5665, 126.9780)])  # Seoul

        try:
            bad = {[37.5665, 126.9780]: "Seoul"}
        except TypeError as e:
            print(f"Error: {e}")  # unhashable type: 'list'
        ```

    Tuples are immutable and hashable, making them valid dictionary keys. Lists are mutable and unhashable.

---

**Exercise 3.**
Explain what tuple packing and unpacking are. Write an example that uses both in a function that returns multiple values.

??? success "Solution to Exercise 3"

        ```python
        # Tuple packing: multiple values packed into a tuple
        coordinates = 37.5665, 126.9780  # packing
        print(type(coordinates))  # <class 'tuple'>

        # Tuple unpacking: extracting values from a tuple
        lat, lon = coordinates  # unpacking
        print(f"Latitude: {lat}, Longitude: {lon}")

        # Common pattern: function returning multiple values
        def min_max(numbers):
            return min(numbers), max(numbers)  # packing

        lo, hi = min_max([3, 1, 4, 1, 5, 9])  # unpacking
        print(f"Min: {lo}, Max: {hi}")  # Min: 1, Max: 9
        ```

    Packing creates a tuple from comma-separated values. Unpacking assigns tuple elements to individual variables.
