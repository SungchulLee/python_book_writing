# sys.getsizeof()

The `sys.getsizeof()` function returns the size of an object in bytes. It's essential for understanding Python's memory usage and optimizing memory-critical applications.

!!! tip "Mental Model"
    `sys.getsizeof()` is like weighing a shipping box on a scale -- it tells you the weight of the box itself, but not the weight of the items packed inside it. For containers like lists and dicts, you get the shallow size of the container structure, not the total size including all referenced objects.

```python
import sys
```

---

## Basic Usage

```python
import sys

# Integers
print(sys.getsizeof(0))        # 24 bytes (small int)
print(sys.getsizeof(1))        # 28 bytes
print(sys.getsizeof(2**30))    # 32 bytes (larger int)
print(sys.getsizeof(2**100))   # 44 bytes (arbitrary precision)

# Strings
print(sys.getsizeof(""))       # 49 bytes (empty string overhead)
print(sys.getsizeof("a"))      # 50 bytes
print(sys.getsizeof("hello"))  # 54 bytes

# Collections
print(sys.getsizeof([]))       # 56 bytes (empty list)
print(sys.getsizeof({}))       # 64 bytes (empty dict)
print(sys.getsizeof(set()))    # 216 bytes (empty set)
```

---

## Important Limitation: Shallow Size Only

`getsizeof()` returns the **shallow** size—it doesn't include the size of objects that the container references:

```python
import sys

# List with integers
lst = [1, 2, 3, 4, 5]
print(sys.getsizeof(lst))  # ~96 bytes (just the list structure)
# Does NOT include the size of integers 1, 2, 3, 4, 5!

# List with strings
strings = ["hello", "world"]
print(sys.getsizeof(strings))  # ~72 bytes (just the list)
# Does NOT include the size of "hello" and "world"!
```

### Visual Explanation

```
sys.getsizeof(lst) measures this:
┌─────────────────────────────────┐
│ List object (header + pointers) │  ← Measured
├─────────────────────────────────┤
│ ptr → 1                         │  ← NOT measured
│ ptr → 2                         │  ← NOT measured
│ ptr → 3                         │  ← NOT measured
└─────────────────────────────────┘
```

---

## Calculating Deep Size

To get the total memory including referenced objects, use recursion:

### Simple Deep Size Function

```python
import sys

def deep_getsizeof(obj, seen=None):
    """Recursively calculate total size of object and its contents."""
    if seen is None:
        seen = set()
    
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    
    size = sys.getsizeof(obj)
    
    if isinstance(obj, dict):
        size += sum(deep_getsizeof(k, seen) + deep_getsizeof(v, seen) 
                    for k, v in obj.items())
    elif isinstance(obj, (list, tuple, set, frozenset)):
        size += sum(deep_getsizeof(item, seen) for item in obj)
    elif hasattr(obj, '__dict__'):
        size += deep_getsizeof(obj.__dict__, seen)
    elif hasattr(obj, '__slots__'):
        size += sum(deep_getsizeof(getattr(obj, slot), seen) 
                    for slot in obj.__slots__ if hasattr(obj, slot))
    
    return size

# Usage
data = {'name': 'Alice', 'scores': [95, 87, 92]}
print(sys.getsizeof(data))       # ~232 bytes (shallow)
print(deep_getsizeof(data))      # ~450 bytes (deep)
```

### Using pympler Library

For production use, consider the `pympler` library:

```python
from pympler import asizeof

data = {'name': 'Alice', 'scores': [95, 87, 92]}
print(asizeof.asizeof(data))  # Total deep size
```

---

## Size of Built-in Types

### Integers

Python integers have variable size based on magnitude:

```python
import sys

# Small integers (CPython caches -5 to 256)
print(sys.getsizeof(0))         # 24 bytes
print(sys.getsizeof(1))         # 28 bytes
print(sys.getsizeof(256))       # 28 bytes

# Larger integers grow
print(sys.getsizeof(2**30))     # 32 bytes
print(sys.getsizeof(2**60))     # 36 bytes
print(sys.getsizeof(2**100))    # 44 bytes
print(sys.getsizeof(2**1000))   # 160 bytes
```

### Floats

Floats have fixed size (64-bit IEEE 754):

```python
print(sys.getsizeof(0.0))       # 24 bytes
print(sys.getsizeof(3.14159))   # 24 bytes
print(sys.getsizeof(1e308))     # 24 bytes (always same)
```

### Strings

String size depends on content and encoding:

```python
# ASCII strings (1 byte per char + overhead)
print(sys.getsizeof(""))        # 49 bytes (overhead)
print(sys.getsizeof("a"))       # 50 bytes
print(sys.getsizeof("hello"))   # 54 bytes

# Unicode strings may use more bytes per char
print(sys.getsizeof("é"))       # 74 bytes (Latin-1)
print(sys.getsizeof("中"))      # 76 bytes (UCS-2)
print(sys.getsizeof("🐍"))      # 80 bytes (UCS-4)
```

### Lists

Lists have base overhead plus pointer storage:

```python
# Empty list
print(sys.getsizeof([]))        # 56 bytes

# Lists grow in chunks (over-allocation)
for n in range(10):
    lst = list(range(n))
    print(f"{n} items: {sys.getsizeof(lst)} bytes")

# Output shows growth pattern:
# 0 items: 56 bytes
# 1 items: 64 bytes
# 2 items: 72 bytes
# 3 items: 80 bytes
# 4 items: 88 bytes
# 5 items: 96 bytes  (may jump)
# ...
```

### Dictionaries

```python
print(sys.getsizeof({}))                    # 64 bytes
print(sys.getsizeof({'a': 1}))              # 184 bytes
print(sys.getsizeof({'a': 1, 'b': 2}))      # 184 bytes (same bucket)
print(sys.getsizeof({i: i for i in range(10)}))  # 352 bytes
```

### Sets

```python
print(sys.getsizeof(set()))                 # 216 bytes
print(sys.getsizeof({1}))                   # 216 bytes
print(sys.getsizeof({1, 2, 3}))             # 216 bytes
print(sys.getsizeof(set(range(10))))        # 728 bytes
```

### Tuples

Tuples are more memory-efficient than lists:

```python
print(sys.getsizeof(()))                    # 40 bytes
print(sys.getsizeof((1,)))                  # 48 bytes
print(sys.getsizeof((1, 2, 3)))             # 64 bytes

# Compare with list
print(sys.getsizeof([1, 2, 3]))             # 80+ bytes
```

---

## Object Size Comparison

```python
import sys

def show_size(name, obj):
    print(f"{name:20} {sys.getsizeof(obj):>8} bytes")

show_size("None", None)
show_size("True", True)
show_size("int 0", 0)
show_size("int 1", 1)
show_size("float", 3.14)
show_size("str ''", "")
show_size("str 'hello'", "hello")
show_size("bytes b''", b"")
show_size("list []", [])
show_size("list [1,2,3]", [1,2,3])
show_size("tuple ()", ())
show_size("tuple (1,2,3)", (1,2,3))
show_size("dict {}", {})
show_size("set()", set())
show_size("frozenset()", frozenset())
```

Output (approximate, varies by Python version):
```
None                       16 bytes
True                       28 bytes
int 0                      24 bytes
int 1                      28 bytes
float                      24 bytes
str ''                     49 bytes
str 'hello'                54 bytes
bytes b''                  33 bytes
list []                    56 bytes
list [1,2,3]               80 bytes
tuple ()                   40 bytes
tuple (1,2,3)              64 bytes
dict {}                    64 bytes
set()                     216 bytes
frozenset()               216 bytes
```

---

## Custom Objects

### With \_\_dict\_\_

```python
class Regular:
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = Regular(1, 2)
print(sys.getsizeof(obj))           # ~48 bytes (object)
print(sys.getsizeof(obj.__dict__))  # ~104 bytes (attribute dict)
# Total: ~152 bytes per instance
```

### With \_\_slots\_\_

```python
class Slotted:
    __slots__ = ('x', 'y')
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

obj = Slotted(1, 2)
print(sys.getsizeof(obj))  # ~48 bytes (no __dict__)
```

---

## Practical Examples

### Compare Data Structure Efficiency

```python
import sys

data = list(range(1000))

# Different representations
as_list = list(data)
as_tuple = tuple(data)
as_set = set(data)
as_frozenset = frozenset(data)

print(f"list:      {sys.getsizeof(as_list):,} bytes")
print(f"tuple:     {sys.getsizeof(as_tuple):,} bytes")
print(f"set:       {sys.getsizeof(as_set):,} bytes")
print(f"frozenset: {sys.getsizeof(as_frozenset):,} bytes")
```

### Memory Budget Check

```python
import sys

def check_memory_budget(obj, max_bytes):
    """Check if object fits within memory budget."""
    size = sys.getsizeof(obj)
    if size > max_bytes:
        raise MemoryError(
            f"Object size {size:,} bytes exceeds budget {max_bytes:,} bytes"
        )
    return size

# Usage
cache = {}
check_memory_budget(cache, max_bytes=1024)
```

### Profile Class Instances

```python
import sys

def instance_memory_report(cls, *args, **kwargs):
    """Report memory usage of a class instance."""
    obj = cls(*args, **kwargs)
    
    base_size = sys.getsizeof(obj)
    dict_size = sys.getsizeof(obj.__dict__) if hasattr(obj, '__dict__') else 0
    
    print(f"Class: {cls.__name__}")
    print(f"  Base object: {base_size} bytes")
    print(f"  __dict__:    {dict_size} bytes")
    print(f"  Total:       {base_size + dict_size} bytes")
    
    return obj

class MyClass:
    def __init__(self, name, values):
        self.name = name
        self.values = values

instance_memory_report(MyClass, "test", [1, 2, 3])
```

---

## Summary

| Type | Empty Size | Notes |
|------|------------|-------|
| `None` | 16 bytes | Singleton |
| `int` (small) | 24-28 bytes | Grows with magnitude |
| `float` | 24 bytes | Fixed (64-bit) |
| `str` | 49+ bytes | Varies by encoding |
| `list` | 56+ bytes | Over-allocates |
| `tuple` | 40+ bytes | More compact than list |
| `dict` | 64+ bytes | Hash table overhead |
| `set` | 216+ bytes | Hash table overhead |
| `object` | ~48 bytes | Plus `__dict__` (~104 bytes) |

**Key Takeaways**:

- `sys.getsizeof()` returns **shallow** size only
- Use recursive functions or `pympler` for deep size
- Empty containers have significant overhead
- `tuple` is more memory-efficient than `list`
- `__slots__` reduces instance size by ~60-70%
- String size depends on character encoding
- Integer size grows with magnitude (arbitrary precision)

---

## Exercises

**Exercise 1.**
Write a function `compare_container_overhead()` that creates an empty `list`, `tuple`, `dict`, `set`, and `frozenset`, then prints each container's overhead (in bytes) using `sys.getsizeof()`. Next, populate each with 100 integers (0 through 99) and print the sizes again. Calculate and display the per-element cost for each container type.

??? success "Solution to Exercise 1"
        ```python
        import sys

        containers = {
            "list": (list, list(range(100))),
            "tuple": (tuple, tuple(range(100))),
            "dict": (dict, {i: i for i in range(100)}),
            "set": (set, set(range(100))),
            "frozenset": (frozenset, frozenset(range(100))),
        }

        for name, (cls, filled) in containers.items():
            empty_size = sys.getsizeof(cls())
            filled_size = sys.getsizeof(filled)
            per_element = (filled_size - empty_size) / 100
            print(f"{name:>10}: empty={empty_size:>6}B, "
                  f"filled={filled_size:>6}B, "
                  f"per-element={per_element:.1f}B")
        ```

---

**Exercise 2.**
Implement the `deep_getsizeof(obj, seen=None)` function from the chapter. Use it to measure the total memory of a dictionary `{"users": [{"name": "Alice", "scores": [95, 87]}, {"name": "Bob", "scores": [72, 88]}]}`. Print both the shallow size (`sys.getsizeof`) and the deep size, and explain in a comment why they differ.

??? success "Solution to Exercise 2"
        ```python
        import sys

        def deep_getsizeof(obj, seen=None):
            if seen is None:
                seen = set()
            obj_id = id(obj)
            if obj_id in seen:
                return 0
            seen.add(obj_id)

            size = sys.getsizeof(obj)

            if isinstance(obj, dict):
                size += sum(deep_getsizeof(k, seen) + deep_getsizeof(v, seen)
                            for k, v in obj.items())
            elif isinstance(obj, (list, tuple, set, frozenset)):
                size += sum(deep_getsizeof(item, seen) for item in obj)
            elif hasattr(obj, '__dict__'):
                size += deep_getsizeof(obj.__dict__, seen)

            return size

        data = {
            "users": [
                {"name": "Alice", "scores": [95, 87]},
                {"name": "Bob", "scores": [72, 88]},
            ]
        }

        shallow = sys.getsizeof(data)
        deep = deep_getsizeof(data)
        print(f"Shallow size: {shallow} bytes")
        print(f"Deep size:    {deep} bytes")
        # The shallow size only measures the outer dict structure.
        # The deep size includes all nested dicts, lists, strings, and ints.
        ```

---

**Exercise 3.**
Create two classes: `RegularPoint` with attributes `x`, `y`, `z` and `SlottedPoint` with `__slots__ = ('x', 'y', 'z')`. Instantiate 100,000 of each and use `sys.getsizeof()` to compare per-instance memory. Print the total estimated memory for each approach and the percentage saved by using `__slots__`.

??? success "Solution to Exercise 3"
        ```python
        import sys

        class RegularPoint:
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        class SlottedPoint:
            __slots__ = ('x', 'y', 'z')
            def __init__(self, x, y, z):
                self.x = x
                self.y = y
                self.z = z

        r = RegularPoint(1, 2, 3)
        s = SlottedPoint(1, 2, 3)

        regular_size = sys.getsizeof(r) + sys.getsizeof(r.__dict__)
        slotted_size = sys.getsizeof(s)

        n = 100_000
        total_regular = regular_size * n
        total_slotted = slotted_size * n
        savings = (1 - total_slotted / total_regular) * 100

        print(f"Per instance - Regular: {regular_size}B, Slotted: {slotted_size}B")
        print(f"Total for {n:,} instances:")
        print(f"  Regular: {total_regular:,} bytes ({total_regular/1024/1024:.1f} MB)")
        print(f"  Slotted: {total_slotted:,} bytes ({total_slotted/1024/1024:.1f} MB)")
        print(f"  Savings: {savings:.1f}%")
        ```
