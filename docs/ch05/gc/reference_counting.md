# Reference Counting

CPython의 기본 메모리 관리 메커니즘입니다.

!!! tip "Mental Model"
    Every Python object carries a hidden counter that tracks how many names or containers point to it. Each new reference increments the counter; each deleted reference decrements it. The instant the counter hits zero, the object is freed immediately -- no waiting, no scanning. This is why most Python memory cleanup is instantaneous and predictable.

## CPython Mechanism

### 1. Every Object Has a Reference Count

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # 2 (x + getrefcount's arg)
```

### 2. Increment/Decrement

```python
x = [1, 2, 3]  # refcount = 1
y = x          # refcount = 2
del y          # refcount = 1
del x          # refcount = 0 → freed
```

## Automatic Management

### 1. No Manual Memory Management

```python
def function():
    x = [1, 2, 3]
    # Automatically freed when function returns
    return

# No memory leak
```

## Advantages

### 1. Immediate Deallocation

```python
x = [1, 2, 3]
del x
# Memory freed immediately (deterministic)
```

### 2. Predictable

메모리가 언제 해제되는지 예측 가능합니다.

---

## Limitation: Circular References

참조 카운팅만으로는 순환 참조를 해제할 수 없습니다.

### The Problem

```python
class Node:
    def __init__(self):
        self.ref = None

a = Node()
b = Node()
a.ref = b
b.ref = a
# Cycle: a → b → a
```

```
     ┌──────────┐
     │  a       │
     │ refcount │──────┐
     │   = 1    │      │
     └──────────┘      ▼
          ▲       ┌──────────┐
          │       │  b       │
          │       │ refcount │
          └───────│   = 1    │
                  └──────────┘
```

`del a, b` 후에도 각 객체의 refcount는 1로 남아있습니다.

### Detection with GC

```python
import gc

# GC finds cycles
gc.collect()
```

### Manual Prevention

```python
# Break cycle manually
a.ref = None
b.ref = None
del a, b  # Now freed
```

## Summary

| Feature | Reference Counting |
|---------|-------------------|
| Speed | Immediate |
| Deterministic | Yes |
| Cycles | Cannot handle |
| Overhead | Per-operation |

---


## Runnable Example: `object_lifecycle.py`

```python
"""
06_advanced_object_lifecycle.py

TOPIC: Object Lifecycle and Memory Internals
LEVEL: Advanced
DURATION: 75-90 minutes

LEARNING OBJECTIVES:
1. Understand complete object lifecycle from creation to destruction
2. Learn about __new__, __init__, and __del__ methods
3. Explore object memory layout and PyObject structure
4. Master memory profiling tools and techniques
5. Understand CPython implementation details

KEY CONCEPTS:
- Object creation: __new__ and __init__
- Object destruction: __del__ and garbage collection
- PyObject structure and overhead
- Memory interning and optimization
- Context managers for resource management
- Memory profiling with memory_profiler
"""

import sys
import gc
import weakref
from ctypes import py_object, c_void_p, cast

# ============================================================================
# SECTION 1: Object Creation Lifecycle
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: Object Creation - __new__ and __init__")
    print("=" * 70)

    # Object creation is a TWO-STEP process in Python:
    # 1. __new__: Allocates memory and creates the object
    # 2. __init__: Initializes the object's state

    class LifecycleDemo:
        """Demonstrates the complete object creation lifecycle"""

        def __new__(cls, value):
            """
            __new__ is called FIRST
            - It's a static method (takes cls, not self)
            - Allocates memory for the object
            - Returns the new instance
            """
            print(f"  1. __new__ called with value={value}")
            print(f"     Allocating memory...")
            instance = super().__new__(cls)
            print(f"     Object created at id={id(instance)}")
            return instance

        def __init__(self, value):
            """
            __init__ is called SECOND
            - Receives the object created by __new__
            - Initializes object attributes
            - Returns None
            """
            print(f"  2. __init__ called")
            print(f"     Initializing object with value={value}")
            self.value = value
            print(f"     Initialization complete")

    print("Creating object:")
    obj = LifecycleDemo(42)
    print(f"\nFinal object: {obj.value} at id={id(obj)}")

    print("""
    LIFECYCLE STAGES:

    1. ALLOCATION (__new__):
       - Memory allocated on heap
       - PyObject structure created
       - Reference count initialized to 0

    2. INITIALIZATION (__init__):
       - Object attributes set
       - Object becomes usable
       - Reference count increased to 1

    3. USAGE:
       - Object referenced by variables
       - Reference count increases/decreases
       - Object may be passed to functions

    4. CLEANUP (__del__ if defined):
       - Called when refcount reaches 0
       - Allows cleanup of resources
       - Should not be relied upon for critical cleanup

    5. DEALLOCATION:
       - Memory returned to Python's memory pool
       - Object no longer exists
    """)

    # ============================================================================
    # SECTION 2: Object Destruction - __del__
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: Object Destruction - __del__")
    print("=" * 70)

    class TrackedObject:
        """Object that tracks its lifecycle"""

        count = 0  # Class variable to track instances

        def __init__(self, name):
            TrackedObject.count += 1
            self.name = name
            print(f"  Created {self.name} (total: {TrackedObject.count})")

        def __del__(self):
            """
            __del__ is called when object is about to be destroyed
            - Reference count has reached 0
            - Object is being garbage collected
            """
            TrackedObject.count -= 1
            print(f"  Destroying {self.name} (remaining: {TrackedObject.count})")

    print("Creating objects:")
    obj1 = TrackedObject("Object1")
    obj2 = TrackedObject("Object2")
    obj3 = TrackedObject("Object3")

    print(f"\nCurrent count: {TrackedObject.count}")

    print("\nDeleting obj1:")
    del obj1  # __del__ called immediately (refcount = 0)

    print("\nCreating alias for obj2:")
    obj2_alias = obj2  # Both obj2 and obj2_alias reference same object

    print("\nDeleting obj2:")
    del obj2  # __del__ NOT called yet (obj2_alias still references it)

    print(f"Object still alive! Refcount: {sys.getrefcount(obj2_alias)}")

    print("\nDeleting obj2_alias:")
    del obj2_alias  # NOW __del__ is called (refcount = 0)

    print("\nDeleting obj3:")
    del obj3

    print("""
    __del__ CAUTIONS:

    1. DON'T RELY ON __del__ for critical cleanup:
       - Timing is unpredictable
       - May not be called in some situations
       - Can be called at interpreter shutdown

    2. BETTER ALTERNATIVES:
       - Use context managers (with statement)
       - Explicitly call cleanup methods
       - Use try/finally blocks

    3. CYCLIC REFERENCES:
       - __del__ can prevent garbage collection of cycles
       - May cause memory leaks

    4. EXCEPTIONS IN __del__:
       - Are printed but otherwise ignored
       - Don't propagate to caller
    """)

    # ============================================================================
    # SECTION 3: PyObject Structure and Memory Layout
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: PyObject Structure and Memory Overhead")
    print("=" * 70)

    # Every Python object has overhead from the PyObject structure:
    # - ob_refcnt: Reference count (8 bytes on 64-bit)
    # - ob_type: Pointer to type object (8 bytes on 64-bit)
    # - + actual object data

    print("Memory sizes of Python objects:\n")

    # Integers
    print("INTEGERS:")
    for val in [0, 1, 100, 10000, 10**100]:
        size = sys.getsizeof(val)
        print(f"  {str(val):20} : {size} bytes")

    # The first few integers (usually -5 to 256) are pre-allocated
    # Larger integers take more space

    print("\nSTRINGS:")
    strings = ["", "a", "hello", "a" * 100]
    for s in strings:
        size = sys.getsizeof(s)
        print(f"  {repr(s[:20]):22} : {size} bytes")

    print("\nLISTS:")
    lists = [[], [1], [1]*10, [1]*100]
    for lst in lists:
        size = sys.getsizeof(lst)
        print(f"  {len(lst):3} elements : {size} bytes")

    print("\nDICTIONARIES:")
    dicts = [{}, {"a": 1}, {f"k{i}": i for i in range(10)}]
    for d in dicts:
        size = sys.getsizeof(d)
        print(f"  {len(d):3} items : {size} bytes")

    print("""
    MEMORY OVERHEAD BREAKDOWN:

    For most objects on 64-bit Python:
    - PyObject header: 16 bytes (refcount + type pointer)
    - Object-specific data varies by type

    Examples:
    - int: 28 bytes minimum (header + value)
    - str: 49+ bytes (header + length + hash + chars)
    - list: 56 bytes empty + 8 bytes per element (for pointers)
    - dict: 64 bytes empty + overhead per key-value pair

    IMPLICATIONS:
    - Small objects have high overhead ratio
    - Lists of integers: each int is a separate object!
    - array.array or numpy can be more memory-efficient
    """)

    # ============================================================================
    # SECTION 4: Object Identity and Equality
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: Object Identity vs Equality")
    print("=" * 70)

    # Identity: Same object in memory (id)
    # Equality: Same value (__eq__)

    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a

    print("Three variables:")
    print(f"a = {a}, id = {id(a)}")
    print(f"b = {b}, id = {id(b)}")
    print(f"c = {c}, id = {id(c)}")

    print("\nIdentity (is operator):")
    print(f"  a is b: {a is b}  # Different objects")
    print(f"  a is c: {a is c}  # Same object")

    print("\nEquality (== operator):")
    print(f"  a == b: {a == b}  # Same values")
    print(f"  a == c: {a == c}  # Same values")

    # The 'is' operator is implemented as:
    # a is b  ⟺  id(a) == id(b)

    print("\nChecking with id():")
    print(f"  id(a) == id(b): {id(a) == id(b)}")
    print(f"  id(a) == id(c): {id(a) == id(c)}")

    # ============================================================================
    # SECTION 5: Context Managers and Resource Management
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: Context Managers (Better than __del__)")
    print("=" * 70)

    class ResourceManager:
        """Demonstrates proper resource management using context manager"""

        def __init__(self, name):
            self.name = name

        def __enter__(self):
            """Called when entering 'with' block"""
            print(f"  Acquiring resource: {self.name}")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            """Called when exiting 'with' block (GUARANTEED)"""
            print(f"  Releasing resource: {self.name}")
            # Return False to propagate exceptions, True to suppress
            return False

        def use(self):
            print(f"  Using resource: {self.name}")

    print("Using context manager:")
    with ResourceManager("Database Connection") as resource:
        resource.use()
        print("  Doing work...")
        # __exit__ will be called even if exception occurs!
    print("Outside with block - resource released\n")

    # Compare to manual cleanup (error-prone):
    print("Manual cleanup (DON'T DO THIS):")
    resource = ResourceManager("File Handle")
    resource.__enter__()
    resource.use()
    # What if exception occurs here? Resource won't be released!
    resource.__exit__(None, None, None)

    print("""
    CONTEXT MANAGER BENEFITS:

    1. GUARANTEED CLEANUP:
       - __exit__ always called
       - Even if exception occurs
       - Even if return statement executed

    2. EXPLICIT SCOPE:
       - Clear where resource is acquired/released
       - Easy to reason about resource lifetime

    3. PYTHONIC:
       - with statement is idiomatic Python
       - Widely understood pattern

    4. COMPOSABLE:
       - Can use multiple context managers
       - with open('a') as f1, open('b') as f2:
    """)

    # ============================================================================
    # SECTION 6: Memory Profiling in Detail
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: Advanced Memory Profiling")
    print("=" * 70)

    def memory_intensive_function():
        """Function that allocates significant memory"""
        # Create large data structures
        data = []
        for i in range(1000):
            data.append([i] * 100)
        return data

    # Using tracemalloc for detailed profiling
    import tracemalloc

    tracemalloc.start()

    # Get baseline
    snapshot_before = tracemalloc.take_snapshot()

    # Run memory-intensive code
    result = memory_intensive_function()

    # Get snapshot after
    snapshot_after = tracemalloc.take_snapshot()

    # Analyze differences
    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')

    print("Top memory allocations:")
    for i, stat in enumerate(top_stats[:5], 1):
        print(f"\n#{i}: {stat}")
        for line in stat.traceback.format():
            print(f"  {line}")

    # Overall memory usage
    current, peak = tracemalloc.get_traced_memory()
    print(f"\nCurrent memory: {current / 1024:.1f} KB")
    print(f"Peak memory: {peak / 1024:.1f} KB")

    tracemalloc.stop()

    # Clean up
    del result

    # ============================================================================
    # SECTION 7: Debugging Memory Issues
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 7: Debugging Memory Problems")
    print("=" * 70)

    # Finding objects that keep other objects alive
    class Container:
        def __init__(self, name):
            self.name = name
            self.items = []

    # Create structure
    container = Container("MyContainer")
    item = [1, 2, 3]
    container.items.append(item)

    print(f"item refcount: {sys.getrefcount(item)}")

    # Find what's referencing an object
    referrers = gc.get_referrers(item)
    print(f"\nObjects referencing item: {len(referrers)}")
    for ref in referrers:
        print(f"  {type(ref).__name__}: {ref if len(str(ref)) < 50 else str(ref)[:50]+'...'}")

    # Find what an object references
    referents = gc.get_referents(container)
    print(f"\nObjects referenced by container: {len(referents)}")
    for ref in referents[:5]:  # Limit output
        print(f"  {type(ref).__name__}")

    # ============================================================================
    # SECTION 8: Object Interning and Caching
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 8: Object Interning and Caching")
    print("=" * 70)

    # Python caches small integers
    print("INTEGER CACHING:")
    a = 256
    b = 256
    print(f"256: a is b = {a is b}  # Cached")

    a = 257
    b = 257
    print(f"257: a is b = {a is b}  # Not cached (usually)")

    # String interning
    print("\nSTRING INTERNING:")
    s1 = "hello"
    s2 = "hello"
    print(f"'hello': s1 is s2 = {s1 is s2}  # Interned")

    s1 = "hello world"
    s2 = "hello world"
    print(f"'hello world': s1 is s2 = {s1 is s2}  # May or may not be interned")

    # Explicit interning
    s1 = sys.intern("hello world")
    s2 = sys.intern("hello world")
    print(f"sys.intern('hello world'): s1 is s2 = {s1 is s2}  # Explicitly interned")

    print("""
    INTERNING BENEFITS:

    1. MEMORY SAVINGS:
       - One copy of string instead of many
       - Useful for large codebases with repeated strings

    2. FASTER COMPARISONS:
       - Identity check (is) instead of value check (==)
       - O(1) instead of O(n)

    3. AUTOMATIC FOR:
       - Python identifiers (variable names, function names)
       - Small integers (-5 to 256)
       - Some strings (compile-time constants)

    WHEN TO USE sys.intern():
       - Dictionary keys used repeatedly
       - Configuration strings
       - Strings from large datasets with repetition
    """)

    # ============================================================================
    # SECTION 9: Memory-Efficient Data Structures
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 9: Memory-Efficient Alternatives")
    print("=" * 70)

    import array

    # Compare list vs array.array
    print("STORING 1000 INTEGERS:\n")

    # Using list (each int is a separate PyObject)
    int_list = list(range(1000))
    list_size = sys.getsizeof(int_list)
    list_item_size = sum(sys.getsizeof(i) for i in int_list[:10])  # Sample
    print(f"List:")
    print(f"  Container: {list_size} bytes")
    print(f"  10 items: {list_item_size} bytes (~{list_item_size/10:.0f} bytes each)")
    print(f"  Total (estimated): {list_size + 1000 * (list_item_size/10):.0f} bytes")

    # Using array.array (compact storage)
    int_array = array.array('i', range(1000))
    array_size = sys.getsizeof(int_array)
    print(f"\nArray:")
    print(f"  Total: {array_size} bytes")
    print(f"  Savings: {(1 - array_size / (list_size + 1000 * (list_item_size/10))) * 100:.1f}%")

    print("""
    MEMORY-EFFICIENT CHOICES:

    1. FOR NUMERIC DATA:
       - array.array: Compact, homogeneous types
       - numpy.ndarray: Best for scientific computing
       - struct: Binary data packing

    2. FOR STRINGS:
       - str: Use for text
       - bytes: Use for binary data (more compact)
       - bytearray: Mutable bytes

    3. FOR COLLECTIONS:
       - tuple instead of list (if immutable)
       - set for membership testing
       - collections.deque for queues
       - dict for key-value (optimized in Python 3.6+)

    4. FOR CLASSES:
       - __slots__: Reduces per-instance overhead
       - namedtuple: Immutable, lightweight
       - dataclass: Convenient, reasonable overhead
    """)

    # ============================================================================
    # SECTION 10: Key Takeaways
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    print("""
    1. Object creation: __new__ (allocate) then __init__ (initialize)
    2. Object destruction: refcount → 0, then __del__ (if defined), then deallocate
    3. Use context managers (with) instead of __del__ for cleanup
    4. Every Python object has 16-byte overhead (64-bit systems)
    5. Integer caching: -5 to 256 pre-allocated
    6. String interning: automatic for identifiers, manual with sys.intern()
    7. Use tracemalloc and gc.get_referrers() for debugging
    8. Choose appropriate data structures for memory efficiency
    9. array.array and __slots__ can save significant memory
    10. Profile before optimizing - measure actual memory usage!

    BEST PRACTICES:
    - Use 'with' for resource management
    - Prefer array.array for numeric data
    - Use __slots__ for classes with many instances
    - Profile with tracemalloc before optimizing
    - Explicitly del large objects when done
    - Use generators for large sequences
    - Consider namedtuple or dataclass over dict
    """)

    # ============================================================================
    # PRACTICE EXERCISES
    # ============================================================================

    print("\n" + "=" * 70)
    print("PRACTICE EXERCISES")
    print("=" * 70)

    print("""
    Master object lifecycle with these exercises:

    1. Create a class that implements __new__, __init__, and __del__.
       Track the complete lifecycle of instances.

    2. Implement a context manager for a database connection simulator.
       Ensure cleanup happens even with exceptions.

    3. Use tracemalloc to profile memory usage of list vs array.array
       for storing 1 million integers.

    4. Create a class without __slots__, then add __slots__. 
       Create 100,000 instances and compare memory usage.

    5. Write a decorator that profiles memory usage of a function
       and reports allocations and peak usage.

    6. Create a circular reference and use gc.get_referrers() to
       debug what's keeping objects alive.

    See exercises_03_advanced.py for complete practice problems!
    """)
```


## Exercises

**Exercise 1.**
Write a script that creates a list object, then creates three additional references to it (by assigning it to new variables). After each assignment, print the reference count using `sys.getrefcount()`. Then delete the references one by one, printing the count each time. Explain in a comment why the count never reaches the value you might naively expect.

??? success "Solution to Exercise 1"
        ```python
        import sys

        obj = [1, 2, 3]
        print(f"Initial: {sys.getrefcount(obj)}")  # 2 (obj + getrefcount arg)

        a = obj
        print(f"After a = obj: {sys.getrefcount(obj)}")  # 3

        b = obj
        print(f"After b = obj: {sys.getrefcount(obj)}")  # 4

        c = obj
        print(f"After c = obj: {sys.getrefcount(obj)}")  # 5

        del c
        print(f"After del c: {sys.getrefcount(obj)}")  # 4

        del b
        print(f"After del b: {sys.getrefcount(obj)}")  # 3

        del a
        print(f"After del a: {sys.getrefcount(obj)}")  # 2

        # getrefcount() always adds 1 because passing the object
        # as an argument creates a temporary reference
        ```

---

**Exercise 2.**
Create two classes `A` and `B` where each instance stores a reference to an instance of the other (circular reference). After deleting both variables, show that `gc.get_objects()` still contains the instances. Then call `gc.collect()` and verify the objects have been collected by checking the count again.

??? success "Solution to Exercise 2"
        ```python
        import gc

        class A:
            def __init__(self):
                self.ref = None

        class B:
            def __init__(self):
                self.ref = None

        a = A()
        b = B()
        a.ref = b
        b.ref = a

        del a, b

        # Count A and B instances still alive
        before = sum(1 for obj in gc.get_objects()
                     if isinstance(obj, (A, B)))
        print(f"Before gc.collect(): {before} objects")  # 2

        collected = gc.collect()
        print(f"Collected: {collected}")

        after = sum(1 for obj in gc.get_objects()
                    if isinstance(obj, (A, B)))
        print(f"After gc.collect(): {after} objects")  # 0
        ```

---

**Exercise 3.**
Write a function `break_cycle_demo()` that (a) creates a circular reference between two objects, (b) manually breaks the cycle by setting the cross-references to `None`, and (c) deletes the objects. Use `weakref.ref` to verify that the objects are freed immediately upon `del` (without needing `gc.collect()`).

??? success "Solution to Exercise 3"
        ```python
        import weakref
        import gc

        def break_cycle_demo():
            class Node:
                def __init__(self, name):
                    self.name = name
                    self.ref = None

            a = Node("A")
            b = Node("B")
            a.ref = b
            b.ref = a

            weak_a = weakref.ref(a)
            weak_b = weakref.ref(b)

            # Break cycle manually
            a.ref = None
            b.ref = None

            del a, b

            # No gc.collect() needed — freed by refcount
            print(f"a alive: {weak_a() is not None}")  # False
            print(f"b alive: {weak_b() is not None}")  # False

        break_cycle_demo()
        ```

---
