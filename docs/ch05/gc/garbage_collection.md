# Garbage Collection

순환 참조를 처리하는 Python의 가비지 컬렉터입니다.

!!! tip "Mental Model"
    Reference counting handles most cleanup instantly, but it cannot break cycles where objects point to each other. The garbage collector is the backup janitor that periodically walks through objects, finds groups that reference only each other with no outside connections, and reclaims them.

## Generational GC

Python은 세대별 가비지 컬렉션을 사용합니다. "대부분의 객체는 일찍 죽는다"는 약한 세대 가설(Weak Generational Hypothesis)에 기반합니다.

### Three Generations

```python
import gc

# (gen0_count, gen1_count, gen2_count)
print(gc.get_count())
```

| Generation | Description | Collection Frequency |
|------------|-------------|---------------------|
| Gen 0 | Young objects | Most frequent |
| Gen 1 | Survived 1 collection | Less frequent |
| Gen 2 | Long-lived objects | Rare |

### Promotion

```python
# Object created → Gen 0
# Survives collection → Gen 1
# Survives again → Gen 2
```

### Thresholds

```python
import gc

# (threshold0, threshold1, threshold2)
print(gc.get_threshold())  # Default: (700, 10, 10)

# Gen 0: every 700 allocations
# Gen 1: every 10 gen-0 collections
# Gen 2: every 10 gen-1 collections
```

---

## gc Module

### Enable/Disable

```python
import gc

gc.disable()  # Turn off
# Critical section
gc.enable()   # Turn on
```

### Force Collection

```python
import gc

# Collect all generations
collected = gc.collect()
print(f"Collected {collected} objects")

# Collect specific generation
gc.collect(0)  # Gen 0 only
gc.collect(1)  # Gen 0 and 1
gc.collect(2)  # All generations
```

### Inspect Objects

```python
import gc

# All tracked objects
objects = gc.get_objects()
print(len(objects))

# Count by type
from collections import Counter

types = Counter(type(obj).__name__ for obj in gc.get_objects())
for name, count in types.most_common(10):
    print(f"{name}: {count}")
```

### Adjust Thresholds

```python
import gc

# Get current thresholds
print(gc.get_threshold())  # (700, 10, 10)

# Set new thresholds
gc.set_threshold(1000, 15, 15)
```

### Generation Statistics

```python
import gc

stats = gc.get_stats()
for i, stat in enumerate(stats):
    print(f"Gen {i}: {stat}")
```

---

## Debugging

### Debug Flags

```python
import gc

# Enable debug output
gc.set_debug(gc.DEBUG_STATS | gc.DEBUG_LEAK)
```

| Flag | Description |
|------|-------------|
| `DEBUG_STATS` | Print collection statistics |
| `DEBUG_COLLECTABLE` | Print collectable objects |
| `DEBUG_UNCOLLECTABLE` | Print uncollectable objects |
| `DEBUG_LEAK` | Debug leaks (COLLECTABLE + UNCOLLECTABLE) |

### Find Uncollectable Objects

```python
import gc

gc.collect()

# Get garbage (uncollectable)
garbage = gc.garbage
print(f"Uncollectable: {len(garbage)}")
```

---

## Cycle Detection Example

```python
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

# Create cycle
a = Node('a')
b = Node('b')
a.ref = b
b.ref = a

# Delete references
del a, b

# Objects still exist (cycle)
print(f"Before: {gc.get_count()}")

# Force collection
collected = gc.collect()
print(f"Collected: {collected}")

print(f"After: {gc.get_count()}")
```

## Summary

| Feature | Description |
|---------|-------------|
| Algorithm | Mark-and-sweep with generations |
| Generations | 3 (young, middle, old) |
| Trigger | Allocation threshold |
| Control | `gc.enable()`, `gc.disable()`, `gc.collect()` |
| Tuning | `gc.set_threshold()` |

---

## Runnable Example: `memory_management_tutorial.py`

---

## Exercises

**Exercise 1.**
Write a script that creates 500 circular reference pairs (two objects referencing each other). Use `gc.get_count()` before and after creation, then call `gc.collect()` and print how many objects were collected. Verify that the count in generation 0 decreases after collection.

??? success "Solution to Exercise 1"
        ```python
        import gc

        class Node:
            def __init__(self):
                self.ref = None

        gc.collect()
        before = gc.get_count()
        print(f"Before: {before}")

        pairs = []
        for _ in range(500):
            a, b = Node(), Node()
            a.ref = b
            b.ref = a
            pairs.append((a, b))

        after_create = gc.get_count()
        print(f"After creation: {after_create}")

        del pairs
        collected = gc.collect()
        after_gc = gc.get_count()

        print(f"Collected: {collected} objects")
        print(f"After gc.collect(): {after_gc}")
        ```

---

**Exercise 2.**
Write a function `monitor_gc_stats()` that saves `gc.get_stats()` before and after running a function that creates 10,000 short-lived lists. Print the number of collections that occurred in each generation during the function's execution.

??? success "Solution to Exercise 2"
        ```python
        import gc

        def monitor_gc_stats(func):
            gc.collect()
            before = gc.get_stats()
            func()
            after = gc.get_stats()

            for i in range(3):
                delta = after[i]['collections'] - before[i]['collections']
                print(f"Gen {i}: {delta} collections during execution")

        def create_short_lived():
            for _ in range(10_000):
                _ = [0] * 100

        monitor_gc_stats(create_short_lived)
        ```

---

**Exercise 3.**
Experiment with GC thresholds: set thresholds to `(100, 5, 5)` using `gc.set_threshold()`, then create 200 circular references in a loop. After each batch of 50, print `gc.get_count()`. Reset thresholds to the defaults at the end. Observe how lower thresholds trigger more frequent collections.

??? success "Solution to Exercise 3"
        ```python
        import gc

        class Node:
            def __init__(self):
                self.ref = None

        default = gc.get_threshold()
        gc.set_threshold(100, 5, 5)
        print(f"Thresholds set to: {gc.get_threshold()}")

        gc.collect()
        for batch in range(4):
            for _ in range(50):
                a, b = Node(), Node()
                a.ref = b
                b.ref = a
            print(f"After batch {batch + 1} (50 pairs): gc.get_count() = {gc.get_count()}")

        gc.set_threshold(*default)
        print(f"Thresholds restored to: {gc.get_threshold()}")
        ```

```python
"""
05_advanced_memory_management.py

TOPIC: Memory Management and Garbage Collection
LEVEL: Advanced
DURATION: 75-90 minutes

LEARNING OBJECTIVES:
1. Understand Python's memory management architecture
2. Learn about reference counting mechanism
3. Explore garbage collection and cyclic reference detection
4. Master memory profiling techniques
5. Apply memory optimization strategies

KEY CONCEPTS:
- Reference counting: primary memory management strategy
- Garbage collector: handles cyclic references
- Memory pools and arenas
- Memory profiling with tracemalloc and memory_profiler
- Memory optimization techniques
- sys.getrefcount() and gc module
"""

import sys
import gc
import weakref
import tracemalloc

# ============================================================================
# SECTION 1: Python's Memory Management Architecture
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: Memory Management Architecture")
    print("=" * 70)

    print("""
    PYTHON'S MEMORY MANAGEMENT LAYERS:

    1. OPERATING SYSTEM LAYER:
       - Provides raw memory to Python
       - Manages virtual memory and physical RAM

    2. PYTHON'S MEMORY MANAGER (pymalloc):
       - Private heap for Python objects
       - Organized into pools and arenas
       - Optimized for small objects (<= 512 bytes)

    3. OBJECT-SPECIFIC ALLOCATORS:
       - Integer pool (small integers cached)
       - String pool (interning)
       - List/dict/tuple allocators

    4. AUTOMATIC MEMORY MANAGEMENT:
       - Reference counting (primary)
       - Garbage collection (backup for cycles)

    MEMORY HIERARCHY:
    ┌──────────────────────────────────────┐
    │  Operating System (OS Memory)        │
    └────────────┬─────────────────────────┘
                 │
    ┌────────────▼─────────────────────────┐
    │  Python Memory Manager (pymalloc)    │
    │  ┌──────────────────────────────┐   │
    │  │  Arenas (256KB blocks)       │   │
    │  │  ┌────────────────────────┐  │   │
    │  │  │  Pools (4KB blocks)    │  │   │
    │  │  │  ┌──────────────────┐  │  │   │
    │  │  │  │  Objects         │  │  │   │
    │  │  │  └──────────────────┘  │  │   │
    │  │  └────────────────────────┘  │   │
    │  └──────────────────────────────┘   │
    └──────────────────────────────────────┘
    """)

    # ============================================================================
    # SECTION 2: Reference Counting Mechanism
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: Reference Counting")
    print("=" * 70)

    # Python uses REFERENCE COUNTING as its primary memory management strategy
    # Every object has a reference count that tracks how many names point to it

    # Create an object and check its reference count
    x = [1, 2, 3]
    print(f"Created list: x = {x}")
    print(f"Reference count: {sys.getrefcount(x)}")
    print("(Note: getrefcount() adds 1 temporary reference)")

    # When we create more references, the count increases
    y = x
    print(f"\nAfter y = x:")
    print(f"Reference count of x: {sys.getrefcount(x)}")

    z = x
    print(f"\nAfter z = x:")
    print(f"Reference count of x: {sys.getrefcount(x)}")

    # When references are deleted, the count decreases
    del y
    print(f"\nAfter del y:")
    print(f"Reference count of x: {sys.getrefcount(x)}")

    del z
    print(f"\nAfter del z:")
    print(f"Reference count of x: {sys.getrefcount(x)}")

    print("""
    REFERENCE COUNTING RULES:
    - Count increases when:
      * Variable assigned to object
      * Object passed to function
      * Object added to container

    - Count decreases when:
      * Variable reassigned
      * Variable deleted (del)
      * Variable goes out of scope
      * Container holding object is deleted

    - When count reaches 0:
      * Object memory is immediately reclaimed
      * No waiting for garbage collection!
    """)

    # ============================================================================
    # SECTION 3: Demonstrating Reference Counting in Action
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: Reference Counting in Different Scenarios")
    print("=" * 70)

    # Scenario 1: Function calls
    def process_list(lst):
        print(f"  Inside function: refcount = {sys.getrefcount(lst)}")
        # Function parameter adds a reference
        return len(lst)

    my_list = [1, 2, 3, 4, 5]
    print(f"Before function call: refcount = {sys.getrefcount(my_list)}")
    result = process_list(my_list)
    print(f"After function call: refcount = {sys.getrefcount(my_list)}")

    # Scenario 2: Containers
    print("\nReference counts with containers:")
    obj = [1, 2, 3]
    print(f"Initial: refcount = {sys.getrefcount(obj)}")

    container = [obj, obj, obj]  # Same object referenced 3 times
    print(f"After adding to container 3 times: refcount = {sys.getrefcount(obj)}")

    container.clear()
    print(f"After container.clear(): refcount = {sys.getrefcount(obj)}")

    # Scenario 3: Dictionary values
    print("\nReference counts with dictionary:")
    data = {"list": obj}
    print(f"After adding to dict: refcount = {sys.getrefcount(obj)}")

    del data["list"]
    print(f"After removing from dict: refcount = {sys.getrefcount(obj)}")

    # ============================================================================
    # SECTION 4: The Problem with Reference Counting - Cycles
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: Cyclic References Problem")
    print("=" * 70)

    # Reference counting FAILS with cyclic references
    # Two objects that reference each other will never reach refcount 0

    class Node:
        def __init__(self, value):
            self.value = value
            self.next = None

        def __repr__(self):
            return f"Node({self.value})"

    # Create a cycle
    node1 = Node(1)
    node2 = Node(2)

    print(f"node1 refcount: {sys.getrefcount(node1)}")
    print(f"node2 refcount: {sys.getrefcount(node2)}")

    # Create cycle: node1 -> node2 -> node1
    node1.next = node2
    node2.next = node1

    print(f"\nAfter creating cycle:")
    print(f"node1 refcount: {sys.getrefcount(node1)}")
    print(f"node2 refcount: {sys.getrefcount(node2)}")

    # Even if we delete the variables, objects still reference each other!
    print(f"\nDeleting variables...")
    del node1, node2

    # These objects are now UNREACHABLE but have refcount > 0
    # This is where the garbage collector comes in!

    print("""
    THE CYCLE PROBLEM:
    ┌────────┐        ┌────────┐
    │ Node 1 │───────>│ Node 2 │
    │        │<───────│        │
    └────────┘        └────────┘

    Even after deleting variables:
    - Both nodes reference each other (refcount >= 1)
    - Objects are unreachable from program
    - Reference counting alone cannot free them
    - Solution: Garbage Collector!
    """)

    # ============================================================================
    # SECTION 5: The Garbage Collector
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: Garbage Collection for Cycles")
    print("=" * 70)

    # Python's garbage collector (gc module) detects and collects cyclic references
    print(f"Garbage collector enabled? {gc.isenabled()}")
    print(f"Current thresholds: {gc.get_threshold()}")
    print(f"Number of tracked objects: {len(gc.get_objects())}")

    # Get garbage collection statistics
    print(f"\nGC stats: {gc.get_stats()}")

    # Create many cyclic structures
    print("\nCreating cyclic structures...")
    for i in range(100):
        node_a = Node(f"A{i}")
        node_b = Node(f"B{i}")
        node_a.next = node_b
        node_b.next = node_a
        # Variables go out of scope, creating garbage

    # Force garbage collection
    print(f"\nCollecting garbage...")
    collected = gc.collect()
    print(f"Objects collected: {collected}")

    print("""
    GARBAGE COLLECTION GENERATIONS:

    Python uses GENERATIONAL GC with 3 generations:

    Generation 0: Young objects (most recently created)
      - Checked most frequently
      - Most objects die young (short-lived)

    Generation 1: Middle-aged objects
      - Survived one GC cycle
      - Checked less frequently

    Generation 2: Old objects
      - Survived multiple GC cycles
      - Checked least frequently
      - Most likely to survive

    THRESHOLD SYSTEM:
    - (threshold0, threshold1, threshold2)
    - When gen0 count > threshold0, collect gen0
    - When gen1 count > threshold1, collect gen1
    - When gen2 count > threshold2, collect gen2

    This generational approach is efficient because:
    - Most objects are short-lived
    - Checking old objects repeatedly is wasteful
    """)

    # ============================================================================
    # SECTION 6: Controlling Garbage Collection
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: Controlling the Garbage Collector")
    print("=" * 70)

    # Get current GC statistics
    print("Current GC statistics:")
    for i, stat in enumerate(gc.get_stats()):
        print(f"  Generation {i}: {stat['collections']} collections")

    # Get generation counts
    print(f"\nCurrent counts per generation: {gc.get_count()}")

    # Manually trigger collection
    print("\nManually triggering garbage collection...")
    collected = gc.collect(generation=0)  # Collect generation 0
    print(f"Generation 0 collected: {collected} objects")

    collected = gc.collect()  # Collect all generations
    print(f"All generations collected: {collected} objects")

    # Disable/enable GC
    print(f"\nGC enabled: {gc.isenabled()}")
    gc.disable()
    print(f"After gc.disable(): {gc.isenabled()}")
    gc.enable()
    print(f"After gc.enable(): {gc.isenabled()}")

    # Adjust thresholds (advanced usage)
    default_thresholds = gc.get_threshold()
    print(f"\nDefault thresholds: {default_thresholds}")

    # Example: Make GC less aggressive (check less frequently)
    # gc.set_threshold(1000, 15, 15)
    # Example: Make GC more aggressive (check more frequently)
    # gc.set_threshold(500, 5, 5)

    # ============================================================================
    # SECTION 7: Memory Profiling with tracemalloc
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 7: Memory Profiling with tracemalloc")
    print("=" * 70)

    # tracemalloc: Python's built-in memory profiler
    # It tracks memory allocations and helps find memory leaks

    # Start tracking
    tracemalloc.start()

    # Take a snapshot before allocation
    snapshot1 = tracemalloc.take_snapshot()

    # Allocate some memory
    large_list = [i for i in range(100000)]
    large_dict = {i: i**2 for i in range(10000)}

    # Take a snapshot after allocation
    snapshot2 = tracemalloc.take_snapshot()

    # Compare snapshots
    top_stats = snapshot2.compare_to(snapshot1, 'lineno')

    print("\nTop 3 memory allocations:")
    for stat in top_stats[:3]:
        print(f"  {stat}")

    # Get current memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"\nCurrent memory usage: {current / 1024 / 1024:.2f} MB")
    print(f"Peak memory usage: {peak / 1024 / 1024:.2f} MB")

    # Stop tracking
    tracemalloc.stop()

    # Clean up
    del large_list, large_dict

    # ============================================================================
    # SECTION 8: Finding Memory Leaks
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 8: Detecting Memory Leaks")
    print("=" * 70)

    # Memory leaks occur when objects are unintentionally kept alive
    # Common causes: global variables, caches, closures, cycles

    # Example of a memory leak (simplified):
    class LeakyCache:
        """A cache that never releases objects - memory leak!"""
        def __init__(self):
            self.cache = {}

        def store(self, key, value):
            self.cache[key] = value  # Never removed!

        def size(self):
            return len(self.cache)

    # Create leak
    cache = LeakyCache()
    for i in range(1000):
        cache.store(i, [0] * 1000)  # Each entry is ~8KB

    print(f"Cache size: {cache.size()} entries")
    print(f"Approximate memory: {cache.size() * 8} KB")

    # To detect leaks:
    # 1. Use tracemalloc to track allocations
    # 2. Use gc.get_objects() to see all objects
    # 3. Look for unexpected growth in object counts

    print(f"\nNumber of dict objects in memory: {sum(1 for obj in gc.get_objects() if type(obj) == dict)}")

    # Clean up
    del cache

    # ============================================================================
    # SECTION 9: Weak References
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 9: Weak References")
    print("=" * 70)

    # Weak references don't increase reference count
    # Useful for caches and avoiding cycles

    # Normal reference:
    obj = [1, 2, 3]
    ref = obj  # Strong reference, increases refcount
    print(f"Object: {obj}")
    print(f"Strong refcount: {sys.getrefcount(obj)}")

    # Weak reference:
    obj2 = [4, 5, 6]
    weak_ref = weakref.ref(obj2)  # Weak reference, doesn't increase refcount
    print(f"\nObject: {obj2}")
    print(f"Weak refcount: {sys.getrefcount(obj2)}")
    print(f"Access through weak ref: {weak_ref()}")

    # If we delete the object, weak reference becomes invalid
    del obj2
    print(f"After del obj2, weak ref: {weak_ref()}")

    # Weak references are useful for caches:
    class BetterCache:
        """Cache using weak references - no memory leak!"""
        def __init__(self):
            self.cache = weakref.WeakValueDictionary()

        def store(self, key, value):
            self.cache[key] = value

        def get(self, key):
            return self.cache.get(key)

        def size(self):
            return len(self.cache)

    # Objects are automatically removed when no strong references exist
    cache = BetterCache()
    temp_obj = [1, 2, 3]
    cache.store("key1", temp_obj)
    print(f"\nCache with object: {cache.get('key1')}")

    del temp_obj  # Object can be garbage collected
    gc.collect()  # Force collection
    print(f"After deleting object: {cache.get('key1')}")

    # ============================================================================
    # SECTION 10: Memory Optimization Strategies
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 10: Memory Optimization Techniques")
    print("=" * 70)

    print("""
    MEMORY OPTIMIZATION STRATEGIES:

    1. USE GENERATORS INSTEAD OF LISTS:
       - List: [x for x in range(1000000)]  # 8+ MB
       - Generator: (x for x in range(1000000))  # ~200 bytes

    2. USE __SLOTS__ IN CLASSES:
       - Prevents __dict__ creation
       - Reduces memory per instance by ~40%

    3. USE APPROPRIATE DATA STRUCTURES:
       - array.array() for numeric data (more compact than list)
       - collections.deque for queues (more efficient than list)
       - set() for membership testing (O(1) vs O(n))

    4. AVOID GLOBAL VARIABLES:
       - Kept alive for program duration
       - Use local variables or context managers

    5. USE WEAK REFERENCES FOR CACHES:
       - Allows automatic cleanup
       - Prevents memory leaks

    6. EXPLICITLY DELETE LARGE OBJECTS:
       - Use 'del' when done with large data
       - Helps reclaim memory immediately

    7. USE STRING INTERNING JUDICIOUSLY:
       - sys.intern() for frequently used strings
       - Saves memory for repeated strings

    8. PROFILE MEMORY USAGE:
       - Use tracemalloc or memory_profiler
       - Identify hot spots
       - Measure before and after optimization
    """)

    # Demonstrate __slots__:
    class WithoutSlots:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    class WithSlots:
        __slots__ = ['x', 'y']
        def __init__(self, x, y):
            self.x = x
            self.y = y

    # Compare memory usage
    obj_no_slots = WithoutSlots(1, 2)
    obj_with_slots = WithSlots(1, 2)

    print(f"\nMemory usage comparison:")
    print(f"Without __slots__: {sys.getsizeof(obj_no_slots)} + {sys.getsizeof(obj_no_slots.__dict__)} bytes")
    print(f"With __slots__: {sys.getsizeof(obj_with_slots)} bytes")

    # ============================================================================
    # SECTION 11: Monitoring Memory in Practice
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 11: Practical Memory Monitoring")
    print("=" * 70)

    import os
    import psutil  # Note: May need to install: pip install psutil

    # Get current process
    process = psutil.Process(os.getpid())

    # Memory info
    mem_info = process.memory_info()
    print(f"RSS (Resident Set Size): {mem_info.rss / 1024 / 1024:.2f} MB")
    print(f"VMS (Virtual Memory Size): {mem_info.vms / 1024 / 1024:.2f} MB")

    # Memory percent
    print(f"Memory usage: {process.memory_percent():.2f}%")

    # ============================================================================
    # SECTION 12: Key Takeaways
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    print("""
    1. Python uses reference counting as primary memory management
    2. Reference count tracks how many names point to an object
    3. When refcount reaches 0, memory is immediately reclaimed
    4. Garbage collector handles cyclic references
    5. GC uses generational approach (gen 0, 1, 2)
    6. tracemalloc helps profile memory usage
    7. Weak references prevent increasing refcount
    8. __slots__ reduces memory usage in classes
    9. Generators are more memory-efficient than lists
    10. Always profile before optimizing!

    BEST PRACTICES:
    - Use sys.getrefcount() to debug reference issues
    - Use gc.collect() to force cleanup when needed
    - Use tracemalloc to find memory leaks
    - Use weak references for caches
    - Delete large objects explicitly when done
    - Profile memory before and after optimization
    """)

    # ============================================================================
    # PRACTICE EXERCISES
    # ============================================================================

    print("\n" + "=" * 70)
    print("PRACTICE EXERCISES")
    print("=" * 70)

    print("""
    Master memory management with these exercises:

    1. Create a cyclic data structure and verify it's collected by gc.
       Use gc.get_objects() before and after collection.

    2. Use tracemalloc to profile memory usage of different data structures
       (list vs array vs numpy array).

    3. Create a class with and without __slots__. Create 10,000 instances
       of each and compare total memory usage.

    4. Implement a cache using WeakValueDictionary and verify that objects
       are automatically removed when no longer referenced.

    5. Write a context manager that tracks memory usage for a code block
       and reports allocation/deallocation.

    6. Create a memory leak intentionally, then use gc.get_referrers()
       to find what's keeping objects alive.

    See exercises_03_advanced.py for complete practice problems!
    """)
```
