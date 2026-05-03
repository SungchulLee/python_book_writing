# Memory Optimization

Techniques for reducing memory usage and tools for profiling memory consumption.

!!! tip "Mental Model"
    Memory optimization is about choosing the right container for the job. A generator is a faucet (produces water on demand), while a list is a water tank (stores everything at once). Use `__slots__` to swap a flexible dictionary for a compact fixed-size struct, and prefer lazy iteration whenever you don't need all items simultaneously.

## Optimization Techniques

### Use `__slots__`

Eliminate per-instance `__dict__` overhead:

```python
class Point:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Saves ~100+ bytes per instance
points = [Point(i, i) for i in range(1000000)]
```

### Prefer Generators Over Lists

Generators produce values on-demand without storing all in memory:

```python
# Bad: entire list in memory
def get_numbers_list():
    return [x ** 2 for x in range(1000000)]

# Good: generator yields one at a time
def get_numbers_gen():
    return (x ** 2 for x in range(1000000))

# Or generator function
def get_numbers():
    for x in range(1000000):
        yield x ** 2
```

### Use `itertools` for Memory Efficiency

```python
import itertools

# Process without loading all data
for item in itertools.islice(huge_iterator, 100):
    process(item)

# Chain iterators without concatenating
for item in itertools.chain(iter1, iter2, iter3):
    process(item)

# Filter without creating intermediate list
for item in itertools.filterfalse(is_bad, data):
    process(item)
```

### Use Appropriate Data Structures

```python
# For many small integers, use array
import array
arr = array.array('i', range(1000000))  # Much smaller than list

# For boolean flags, use bitarray or integers
flags = 0
flags |= (1 << 0)  # Set flag 0
flags |= (1 << 3)  # Set flag 3

# For sparse data, use dict instead of list
sparse_data = {0: 'a', 1000000: 'b'}  # Not [0]*1000001
```

### Avoid Unnecessary Copies

```python
# Bad: creates copy
def process(data):
    data = list(data)  # Unnecessary copy
    return sum(data)

# Good: work with original
def process(data):
    return sum(data)

# Use slices carefully
big_list = list(range(1000000))
# Bad: creates copy
subset = big_list[100:200]
# Consider: itertools.islice for iteration
```

### Delete Unused Large Objects

```python
def process_large_file():
    data = load_huge_file()  # 1GB in memory
    result = compute(data)
    del data  # Free memory immediately
    return result
```

---

## Memory Profiling

### `sys.getsizeof()`

Get the size of a single object:

```python
import sys

x = [1, 2, 3]
print(sys.getsizeof(x))  # ~88 bytes (list object itself)

# Note: doesn't include referenced objects
nested = [[1, 2], [3, 4]]
print(sys.getsizeof(nested))  # Only the outer list size
```

### Deep Size Calculation

```python
import sys

def deep_getsizeof(obj, seen=None):
    """Recursively calculate size of objects."""
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
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes)):
        size += sum(deep_getsizeof(i, seen) for i in obj)
    
    return size

nested = [[1, 2], [3, 4], {'a': [5, 6]}]
print(deep_getsizeof(nested))  # Total size including contents
```

### `tracemalloc` Module

Track memory allocations:

```python
import tracemalloc

tracemalloc.start()

# ... your code ...
data = [x ** 2 for x in range(100000)]

current, peak = tracemalloc.get_traced_memory()
print(f"Current: {current / 1024 / 1024:.2f} MB")
print(f"Peak: {peak / 1024 / 1024:.2f} MB")

tracemalloc.stop()
```

### Finding Memory Hogs

```python
import tracemalloc

tracemalloc.start()

# Your code here
data = load_data()
process(data)

# Take snapshot
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

print("Top 10 memory allocations:")
for stat in top_stats[:10]:
    print(stat)
```

### Comparing Snapshots

```python
import tracemalloc

tracemalloc.start()

snapshot1 = tracemalloc.take_snapshot()

# Code that might leak
data = create_large_data()

snapshot2 = tracemalloc.take_snapshot()

# Compare
top_stats = snapshot2.compare_to(snapshot1, 'lineno')

print("Memory changes:")
for stat in top_stats[:10]:
    print(stat)
```

### Memory Profiler Package

For line-by-line profiling (install: `pip install memory-profiler`):

```python
from memory_profiler import profile

@profile
def my_function():
    a = [1] * 1000000
    b = [2] * 2000000
    del b
    return a

my_function()
```

Output:
```
Line #    Mem usage    Increment   Line Contents
================================================
     3     38.0 MiB     38.0 MiB   @profile
     4                             def my_function():
     5     45.6 MiB      7.6 MiB       a = [1] * 1000000
     6     61.0 MiB     15.3 MiB       b = [2] * 2000000
     7     45.6 MiB    -15.3 MiB       del b
     8     45.6 MiB      0.0 MiB       return a
```

---

## Common Memory Issues

### Circular References

```python
# Problem: circular reference
class Node:
    def __init__(self):
        self.parent = None
        self.children = []

parent = Node()
child = Node()
parent.children.append(child)
child.parent = parent  # Circular!

# Solution: use weak references
import weakref

class Node:
    def __init__(self):
        self._parent = None
        self.children = []
    
    @property
    def parent(self):
        return self._parent() if self._parent else None
    
    @parent.setter
    def parent(self, value):
        self._parent = weakref.ref(value) if value else None
```

### Growing Caches

```python
# Problem: unbounded cache
cache = {}

def get_data(key):
    if key not in cache:
        cache[key] = expensive_compute(key)
    return cache[key]

# Solution: bounded cache
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_data(key):
    return expensive_compute(key)
```

---

## Summary

| Technique | Memory Saving | Complexity |
|-----------|--------------|------------|
| `__slots__` | ~100 bytes/instance | Low |
| Generators | Significant | Low |
| `array.array` | 4-8x for numbers | Low |
| Memory views | Avoids copies | Medium |
| Object pools | Reduces allocations | Medium |

Profiling tools:
- `sys.getsizeof()`: Quick object size
- `tracemalloc`: Detailed allocation tracking
- `memory_profiler`: Line-by-line analysis

Key points:
- Profile before optimizing
- Use generators for large sequences
- Choose appropriate data structures
- Watch for memory leaks and circular references
- Delete large objects when no longer needed

---

## Exercises

**Exercise 1.**
Write two functions that each produce the sum of squares for numbers 0 through 999,999: one using a list comprehension and one using a generator expression. Use `tracemalloc` to measure peak memory for each approach and print the results. Verify that both return the same answer.

??? success "Solution to Exercise 1"
        ```python
        import tracemalloc

        def sum_squares_list():
            return sum([x ** 2 for x in range(1_000_000)])

        def sum_squares_gen():
            return sum(x ** 2 for x in range(1_000_000))

        tracemalloc.start()
        result1 = sum_squares_list()
        _, peak1 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        result2 = sum_squares_gen()
        _, peak2 = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"List comprehension: result={result1}, peak={peak1 / 1024:.1f} KB")
        print(f"Generator:          result={result2}, peak={peak2 / 1024:.1f} KB")
        print(f"Same result: {result1 == result2}")
        print(f"Memory saved: {(peak1 - peak2) / 1024:.1f} KB")
        ```

---

**Exercise 2.**
Create a class `Record` with five attributes (`a`, `b`, `c`, `d`, `e`) using `__slots__`, and an equivalent `RecordDict` without slots. Instantiate 200,000 of each. Use `tracemalloc` to compare total memory, then print per-instance savings and total savings in MB.

??? success "Solution to Exercise 2"
        ```python
        import tracemalloc

        class Record:
            __slots__ = ('a', 'b', 'c', 'd', 'e')
            def __init__(self, a, b, c, d, e):
                self.a = a
                self.b = b
                self.c = c
                self.d = d
                self.e = e

        class RecordDict:
            def __init__(self, a, b, c, d, e):
                self.a = a
                self.b = b
                self.c = c
                self.d = d
                self.e = e

        n = 200_000

        tracemalloc.start()
        slots_list = [Record(i, i+1, i+2, i+3, i+4) for i in range(n)]
        _, peak_slots = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        dict_list = [RecordDict(i, i+1, i+2, i+3, i+4) for i in range(n)]
        _, peak_dict = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"With __slots__:    {peak_slots / 1024 / 1024:.2f} MB")
        print(f"Without __slots__: {peak_dict / 1024 / 1024:.2f} MB")
        print(f"Savings: {(peak_dict - peak_slots) / 1024 / 1024:.2f} MB "
              f"({(1 - peak_slots / peak_dict) * 100:.1f}%)")
        ```

---

**Exercise 3.**
Write a function `find_memory_hog()` that uses `tracemalloc` snapshots to identify the top 3 memory-consuming lines in a block of code. The block should create a list of 100,000 random strings, a dictionary mapping integers to their squares (50,000 entries), and a set of 80,000 floats. Print the top 3 allocations with file, line number, and size.

??? success "Solution to Exercise 3"
        ```python
        import tracemalloc
        import random
        import string

        def find_memory_hog():
            tracemalloc.start()

            strings = [''.join(random.choices(string.ascii_letters, k=20))
                       for _ in range(100_000)]
            squares = {i: i ** 2 for i in range(50_000)}
            floats = {random.random() for _ in range(80_000)}

            snapshot = tracemalloc.take_snapshot()
            top_stats = snapshot.statistics('lineno')

            print("Top 3 memory allocations:")
            for stat in top_stats[:3]:
                print(f"  {stat}")

            tracemalloc.stop()

        find_memory_hog()
        ```
