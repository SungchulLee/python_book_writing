# Memory Management

Understanding copy semantics, memory views, and `__slots__` for efficient memory usage.

!!! tip "Mental Model"
    Shallow copy is like photocopying a page of links -- you get a new page, but the links still point to the same websites. Deep copy recreates the entire website tree. Choose shallow when shared sub-objects are fine; choose deep when each copy must be fully independent.

## Copy vs Deepcopy

### Shallow Copy

A shallow copy creates a new container but references the same nested objects:

```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)

# Top level is copied
print(shallow is original)  # False

# Nested objects are shared
print(shallow[0] is original[0])  # True
```

**Mutation affects both:**

```python
shallow[0].append(3)

print(original)  # [[1, 2, 3], [3, 4]]
print(shallow)   # [[1, 2, 3], [3, 4]]
# Both changed!
```

### Deep Copy

A deep copy recursively copies all nested objects:

```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

# Everything is copied
print(deep is original)  # False
print(deep[0] is original[0])  # False
```

**Changes are independent:**

```python
deep[0].append(3)

print(original)  # [[1, 2], [3, 4]]
print(deep)      # [[1, 2, 3], [3, 4]]
# Only deep changed
```

### When to Use Each

| Situation | Use | Example |
|-----------|-----|---------|
| Flat data | Shallow | `[1, 2, 3].copy()` |
| Nested mutable | Deep | `copy.deepcopy(nested)` |
| Performance critical | Shallow | Large data, no nesting |
| Complete independence | Deep | Complex structures |

```python
# Shallow: fast, less memory
data = [1, 2, 3]
backup = data.copy()

# Deep: slow, more memory, but safe
nested = [[1, 2], {'a': [3, 4]}]
backup = copy.deepcopy(nested)
```

---

## Memory Views

Memory views provide zero-copy access to buffer data.

### Creating Memory Views

```python
data = bytearray(b'Hello World')
view = memoryview(data)

# Access without copying
print(view[0])  # 72 (ASCII for 'H')
print(bytes(view[0:5]))  # b'Hello'
```

### Zero-Copy Slicing

```python
data = bytearray(range(100))
view = memoryview(data)

# Slice creates a view, not a copy
slice_view = view[10:20]
print(bytes(slice_view))  # b'\n\x0b\x0c...'

# Verify no copy
slice_view[0] = 255
print(data[10])  # 255 (original modified)
```

### Use Cases

**Large Data Processing:**

```python
import array

arr = array.array('i', range(1000000))
view = memoryview(arr)

# Process in chunks without copying
for i in range(0, len(view), 1000):
    chunk = view[i:i+1000]
    process(chunk)
```

**Network Buffers:**

```python
buffer = bytearray(4096)
view = memoryview(buffer)

# Receive directly into buffer
bytes_received = socket.recv_into(view)

# Process without copying
data = view[:bytes_received]
```

**In-Place Modification:**

```python
data = bytearray(b'Hello')
view = memoryview(data)

view[0] = ord('J')
print(data)  # bytearray(b'Jello')
```

### Memory View Properties

```python
view = memoryview(bytearray(100))

print(view.nbytes)    # Total bytes
print(view.readonly)  # False for bytearray
print(view.format)    # 'B' (unsigned char)
print(view.itemsize)  # 1 byte per item
```

---

## `__slots__`

`__slots__` reduces memory usage by eliminating the instance `__dict__`.

### Without Slots (Default)

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(10, 20)
print(p.__dict__)  # {'x': 10, 'y': 20}
```

### With Slots

```python
class Point:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(10, 20)
# p.__dict__  # AttributeError: no __dict__
print(p.x, p.y)  # 10 20
```

### Memory Comparison

```python
import sys

class WithDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class WithSlots:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

d = WithDict(1, 2)
s = WithSlots(1, 2)

print(sys.getsizeof(d))  # ~48 bytes (+ dict ~104)
print(sys.getsizeof(s))  # ~48 bytes (no dict overhead)
```

### Restrictions

**No Dynamic Attributes:**

```python
class Point:
    __slots__ = ['x', 'y']
    
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(10, 20)
# p.z = 30  # AttributeError: 'Point' has no attribute 'z'
```

**Inheritance Considerations:**

```python
class Point:
    __slots__ = ['x', 'y']

class Point3D(Point):
    __slots__ = ['z']  # Only add new slots
    
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
```

**Enabling Weak References:**

```python
class Point:
    __slots__ = ['x', 'y', '__weakref__']  # Add __weakref__
```

### When to Use `__slots__`

```python
# Good: millions of instances
class Particle:
    __slots__ = ['x', 'y', 'vx', 'vy', 'mass']

particles = [Particle() for _ in range(1000000)]
# Saves significant memory

# Not needed: few instances
class Config:
    def __init__(self):
        self.debug = False
        self.verbose = True
# Only one instance, slots unnecessary
```

---

## Summary

| Technique | Purpose | Use When |
|-----------|---------|----------|
| Shallow copy | Quick duplicate | Flat structures |
| Deep copy | Full independence | Nested mutables |
| Memory views | Zero-copy access | Large buffers |
| `__slots__` | Reduce memory | Many instances |

Key points:
- Understand shallow vs deep copy to avoid aliasing bugs
- Use memory views for efficient buffer manipulation
- Use `__slots__` when creating many instances of a class
- `__slots__` prevents dynamic attribute addition
- Always profile before optimizing

---


## Runnable Example: `list_internals.py`

```python
"""
01_list_internals.py

TOPIC: Python List Implementation Internals
LEVEL: Advanced
DURATION: 60-75 minutes

PREREQUISITES:
- Topic #24: Memory Deep Dive (mutable types, references, memory management)

LEARNING OBJECTIVES:
1. Understand list memory layout
2. Learn about over-allocation strategy
3. Explore capacity vs length
4. Understand why lists are fast for certain operations

This is ADVANCED implementation details - builds on memory concepts from #24
"""

import sys

if __name__ == "__main__":

    print("=" * 70)
    print("PYTHON LIST INTERNALS")
    print("=" * 70)

    # ============================================================================
    # SECTION 1: List Memory Layout
    # ============================================================================

    print("\nSECTION 1: How Lists Are Structured")
    print("-" * 70)

    print("""
    PYTHON LIST STRUCTURE (CPython):

    ┌─────────────────────────────────────────┐
    │ PyListObject                            │
    ├─────────────────────────────────────────┤
    │ ob_refcnt: reference count              │
    │ ob_type: pointer to list type           │
    │ ob_size: number of elements (LENGTH)    │  ← What len() returns
    │ allocated: capacity (slots)             │  ← Total allocated space
    │ ob_item: pointer to array of pointers   │  ← Points to actual data
    └─────────────────────────────────────────┘
               │
               ↓
        ┌──────────────────────┐
        │ Array of Pointers    │
        ├──────────────────────┤
        │ [0] → Object 1       │
        │ [1] → Object 2       │
        │ [2] → Object 3       │
        │ [3] → Object 4       │
        │ [4] → (unused)       │  ← OVER-ALLOCATION
        │ [5] → (unused)       │  ← Extra capacity
        └──────────────────────┘

    KEY INSIGHT:
    - Lists store POINTERS to objects, not objects themselves
    - ob_size (length) ≤ allocated (capacity)
    - Extra capacity allows fast appends!
    """)

    # ============================================================================
    # SECTION 2: Length vs Capacity
    # ============================================================================

    print("\nSECTION 2: Length vs Capacity")
    print("-" * 70)

    # Create empty list
    my_list = []
    print(f"Empty list: {my_list}")
    print(f"  len() = {len(my_list)}")  # ob_size
    print(f"  sys.getsizeof() = {sys.getsizeof(my_list)} bytes")  # includes allocated capacity

    # Add one element
    my_list.append(1)
    print(f"\nAfter append(1): {my_list}")
    print(f"  len() = {len(my_list)}")
    print(f"  sys.getsizeof() = {sys.getsizeof(my_list)} bytes")

    # Add more elements
    sizes = [sys.getsizeof([])]
    for i in range(2, 20):
        my_list.append(i)
        size = sys.getsizeof(my_list)
        if size > sizes[-1]:
            print(f"\nAfter append({i}): len={len(my_list)}, size={size} bytes (RESIZED!)")
            sizes.append(size)
        else:
            print(f"After append({i}): len={len(my_list)}, size={size} bytes")

    print("""
    OBSERVATIONS:
    - Size doesn't increase with EVERY append
    - Size increases in JUMPS (when capacity is exceeded)
    - This is OVER-ALLOCATION strategy
    - Trade-off: waste some memory for faster appends
    """)

    # ============================================================================
    # SECTION 3: Over-Allocation Strategy
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: Why Over-Allocation?")
    print("-" * 70)

    print("""
    WITHOUT OVER-ALLOCATION (naive approach):
    ───────────────────────────────────────
    lst = []           # Allocate 0 slots
    lst.append(1)      # Allocate 1 slot, copy 0 items
    lst.append(2)      # Allocate 2 slots, copy 1 item
    lst.append(3)      # Allocate 3 slots, copy 2 items
    lst.append(4)      # Allocate 4 slots, copy 3 items
    ...
    lst.append(n)      # Allocate n slots, copy n-1 items

    Total copies: 0 + 1 + 2 + ... + (n-1) = O(n²)  ← TERRIBLE!

    WITH OVER-ALLOCATION (Python's approach):
    ───────────────────────────────────────
    lst = []           # Allocate 0 slots
    lst.append(1)      # Allocate 4 slots (over-allocate!)
    lst.append(2)      # Use existing capacity
    lst.append(3)      # Use existing capacity
    lst.append(4)      # Use existing capacity
    lst.append(5)      # Allocate 8 slots, copy 4 items
    lst.append(6)      # Use existing capacity
    ...

    Total copies: Much fewer! = O(n)  ← MUCH BETTER!

    GROWTH PATTERN (approximately):
    0, 4, 8, 16, 25, 35, 46, 58, 72, 88, ...

    Formula (approximately): new_capacity = old_capacity + (old_capacity >> 3) + 6
    Which is roughly: new_capacity ≈ 1.125 * old_capacity + 6
    """)

    # ============================================================================
    # SECTION 4: Performance Implications
    # ============================================================================

    print("\nSECTION 4: Performance Analysis")
    print("-" * 70)

    print("""
    OPERATION PERFORMANCE:

    FAST (O(1) amortized):
    ✓ append() - usually fits in capacity
    ✓ Access by index: lst[i]
    ✓ Modify by index: lst[i] = x
    ✓ len(lst)
    ✓ pop() - remove last element

    SLOW (O(n)):
    ✗ insert(0, x) - shift all elements right
    ✗ pop(0) - shift all elements left
    ✗ remove(x) - search then shift
    ✗ Concatenation: lst1 + lst2

    WHY append() is O(1) amortized:
    - Most appends use existing capacity: O(1)
    - Occasional resize: O(n)
    - But resizes become increasingly rare
    - Average over many operations: O(1)
    """)

    # Demonstrate fast append
    import time

    n = 100000
    start = time.time()
    test_list = []
    for i in range(n):
        test_list.append(i)
    append_time = time.time() - start

    print(f"\nAppending {n} elements: {append_time:.4f} seconds")
    print(f"Average per append: {append_time/n*1000000:.2f} microseconds")

    # ============================================================================
    # SECTION 5: Memory Trade-offs
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: Memory Trade-offs")
    print("-" * 70)

    # Show wasted space
    test_list = list(range(100))
    actual_size = sys.getsizeof(test_list)
    ptr_size = 8  # 64-bit system
    base_size = sys.getsizeof([])
    used_size = base_size + (100 * ptr_size)

    print(f"List with 100 elements:")
    print(f"  Total memory: {actual_size} bytes")
    print(f"  Base overhead: {base_size} bytes")
    print(f"  Used for data: {100 * ptr_size} bytes (100 pointers × 8 bytes)")
    print(f"  Estimated waste: {actual_size - used_size} bytes (~{(actual_size-used_size)/actual_size*100:.1f}%)")

    print("""
    TRADE-OFF:
    - Waste ~10-30% of memory (varies with size)
    - Gain O(1) amortized append performance
    - For most applications: speed > memory

    WHEN TO CARE:
    - Creating MANY small lists → use tuples if immutable
    - Memory-constrained environments
    - Lists that rarely grow after creation
    """)

    # ============================================================================
    # SECTION 6: Practical Implications
    # ============================================================================

    print("\nSECTION 6: Practical Programming Implications")
    print("-" * 70)

    print("""
    BEST PRACTICES:

    1. Pre-allocate if you know size:
       ✓ lst = [None] * 1000  # Better than 1000 appends

    2. Use list comprehensions:
       ✓ [x**2 for x in range(1000)]  # Optimized

    3. Avoid repeated insertions at beginning:
       ✗ for x in data: lst.insert(0, x)  # O(n²)
       ✓ Use collections.deque for queue operations

    4. Don't pre-allocate unnecessarily:
       ✗ lst = [None] * 1000000  # Wastes memory if not all used

    5. Concatenation alternatives:
       ✗ result = []
          for lst in many_lists:
              result = result + lst  # Creates new list each time!
       ✓ result = []
          for lst in many_lists:
              result.extend(lst)  # Modifies in place
    """)

    # ============================================================================
    # SECTION 7: Comparison to Other Data Structures
    # ============================================================================

    print("\nSECTION 7: When NOT to Use Lists")
    print("-" * 70)

    print("""
    USE THESE INSTEAD:

    collections.deque:
    - Fast O(1) operations at both ends
    - Use for queues, stacks
    - Slower random access

    array.array:
    - Compact storage for numeric data
    - No over-allocation waste
    - Only homogeneous types

    numpy.ndarray:
    - Multi-dimensional arrays
    - Vectorized operations
    - Scientific computing

    tuple:
    - Immutable, no over-allocation
    - Slightly faster, less memory
    - Use when size fixed
    """)

    # ============================================================================
    # SECTION 8: Key Takeaways
    # ============================================================================

    print("\nKEY TAKEAWAYS")
    print("-" * 70)

    print("""
    1. Lists use OVER-ALLOCATION for performance
    2. Length (ob_size) ≤ Capacity (allocated)
    3. append() is O(1) amortized due to over-allocation
    4. Occasional resize operations are O(n)
    5. Growth pattern: ~1.125x + constant
    6. Trades memory (10-30% waste) for speed
    7. insert(0) and pop(0) are O(n) - avoid for queues
    8. Pre-allocate if size known
    9. Use deque for queue operations
    10. Understanding internals helps choose right data structure

    CONNECTS TO #24 MEMORY CONCEPTS:
    - Mutable type behavior
    - Reference storage
    - Memory allocation patterns
    - Performance vs memory trade-offs
    """)

    print("\nSee exercises.py for practice!")
```


## Exercises

**Exercise 1.**
Write a script that demonstrates the difference between shallow and deep copy for a nested structure: a list of dictionaries where each dictionary contains a list. Modify a deeply nested value through the shallow copy and show that the original is affected. Then do the same with a deep copy and show independence.

??? success "Solution to Exercise 1"
        ```python
        import copy

        original = [
            {"name": "Alice", "scores": [90, 85]},
            {"name": "Bob", "scores": [78, 92]},
        ]

        shallow = copy.copy(original)
        shallow[0]["scores"].append(100)
        print("After shallow copy modification:")
        print(f"  original[0]['scores'] = {original[0]['scores']}")  # [90, 85, 100]
        print(f"  shallow[0]['scores']  = {shallow[0]['scores']}")   # [90, 85, 100]
        print("  Original was affected!\n")

        original[0]["scores"].pop()  # restore

        deep = copy.deepcopy(original)
        deep[0]["scores"].append(200)
        print("After deep copy modification:")
        print(f"  original[0]['scores'] = {original[0]['scores']}")  # [90, 85]
        print(f"  deep[0]['scores']     = {deep[0]['scores']}")      # [90, 85, 200]
        print("  Original is independent!")
        ```

---

**Exercise 2.**
Create a `bytearray` of 1000 bytes, then obtain a `memoryview` of it. Slice the memory view to get bytes 100 through 199 and modify the first byte of the slice to `0xFF`. Print the original `bytearray` at index 100 to prove that memory views provide zero-copy access. Measure and print the size of the slice versus creating an actual `bytes` copy of the same range.

??? success "Solution to Exercise 2"
        ```python
        import sys

        data = bytearray(1000)
        view = memoryview(data)

        slice_view = view[100:200]
        slice_view[0] = 0xFF

        print(f"data[100] = {data[100]:#04x}")  # 0xff — zero-copy confirmed

        copy_bytes = bytes(data[100:200])
        print(f"memoryview slice size: {sys.getsizeof(slice_view)} bytes")
        print(f"bytes copy size:       {sys.getsizeof(copy_bytes)} bytes")
        ```

---

**Exercise 3.**
Define a class `Sensor` with `__slots__ = ('id', 'value', 'timestamp')` and a class `SensorNoSlots` with the same attributes but no `__slots__`. Create 50,000 instances of each, then use `sys.getsizeof()` to compare per-instance sizes. Also use `tracemalloc` to measure the total memory consumed by each batch.

??? success "Solution to Exercise 3"
        ```python
        import sys
        import tracemalloc

        class Sensor:
            __slots__ = ('id', 'value', 'timestamp')
            def __init__(self, id, value, timestamp):
                self.id = id
                self.value = value
                self.timestamp = timestamp

        class SensorNoSlots:
            def __init__(self, id, value, timestamp):
                self.id = id
                self.value = value
                self.timestamp = timestamp

        s = Sensor(1, 2.0, 3)
        ns = SensorNoSlots(1, 2.0, 3)
        print(f"With slots:    {sys.getsizeof(s)} bytes/instance")
        print(f"Without slots: {sys.getsizeof(ns) + sys.getsizeof(ns.__dict__)} bytes/instance")

        n = 50_000

        tracemalloc.start()
        slots_list = [Sensor(i, float(i), i) for i in range(n)]
        _, slots_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tracemalloc.start()
        noslots_list = [SensorNoSlots(i, float(i), i) for i in range(n)]
        _, noslots_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"\n{n:,} instances peak memory:")
        print(f"  With slots:    {slots_peak / 1024 / 1024:.2f} MB")
        print(f"  Without slots: {noslots_peak / 1024 / 1024:.2f} MB")
        ```

---
