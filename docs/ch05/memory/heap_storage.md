# Heap Storage

!!! tip "Mental Model"
    The heap is a big warehouse where every Python object lives -- integers, strings, lists, everything. Unlike the organized call stack, heap objects are scattered wherever space is available. Python's memory allocator and garbage collector manage this warehouse for you, placing new objects in free spots and reclaiming space when objects are no longer needed.

## Object Allocation

### 1. All Objects

Everything on heap:

```python
x = 42              # int on heap
s = "hello"         # str on heap
lst = [1, 2, 3]     # list on heap
```

### 2. Dynamic Growth

```python
# Heap grows as needed
data = []
for i in range(1000000):
    data.append(i)  # Heap expands
```

## Object Layout

### 1. Continuous Memory

```python
# List items contiguous
lst = [1, 2, 3, 4, 5]

# In memory:
# [header][ptr1][ptr2][ptr3][ptr4][ptr5]
```

### 2. Scattered Objects

```python
# Objects anywhere on heap
a = [1, 2]
b = "hello"
c = {'key': 'value'}

# Memory not sequential
```

## Memory Pools

### 1. Small Objects

Python uses memory pools:

```python
# Small objects (< 512 bytes)
# Allocated from pools
# Faster than malloc

x = 42              # From pool
s = "hi"            # From pool
```

### 2. Large Objects

```python
# Large objects
# Direct malloc
big = [0] * 1000000
```

## Fragmentation

### 1. Can Occur

```python
# Create many objects
data = [[] for _ in range(1000)]

# Delete some
for i in range(0, 1000, 2):
    del data[i]

# Holes in memory
```

### 2. GC Helps

```python
import gc

# Force collection
gc.collect()

# Helps reduce fragmentation
```

## Object Sizes

### 1. Check Size

```python
import sys

print(sys.getsizeof(42))        # Small
print(sys.getsizeof([1, 2, 3])) # Larger
print(sys.getsizeof("hello"))   # String
```

### 2. Container Overhead

```python
# List overhead
empty_list = []
print(sys.getsizeof(empty_list))  # ~56 bytes

# Plus items
lst = [1, 2, 3]
print(sys.getsizeof(lst))  # ~80 bytes
```

## Lifetime

### 1. Until GC'd

```python
x = [1, 2, 3]       # Created
# Lives on heap
del x               # Reference removed
# Eventually GC'd
```

### 2. Reference Counting

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # 2

y = x
print(sys.getrefcount(x))  # 3

del y
print(sys.getrefcount(x))  # 2
```

## Heap vs Stack

### 1. Comparison

```python
def function():
    # Local name on stack
    x = [1, 2, 3]   # Object on heap
    
    # x removed from stack at return
    # Object stays until GC'd
    return x
```

## Summary

### 1. Heap

- All objects stored here
- Dynamic size
- Slower than stack
- Manual/GC management

### 2. Memory Management

- Pools for small objects
- Direct allocation for large
- Fragmentation possible
- GC handles cleanup

---


## Runnable Example: `mutable_types.py`

```python
"""
03_intermediate_mutable_types.py

TOPIC: Mutable Types and Reference Behavior
LEVEL: Intermediate
DURATION: 60-75 minutes

LEARNING OBJECTIVES:
1. Understand mutable types (list, dict, set) and their memory behavior
2. Learn about reference semantics and aliasing
3. Explore the dangers of unintended sharing
4. Master the difference between mutation and reassignment
5. Understand how mutable types behave as function parameters

KEY CONCEPTS:
- Mutable objects can be changed in-place
- Multiple variables can reference the same mutable object (aliasing)
- Mutations affect all references to the same object
- Mutable types: list, dict, set, bytearray, custom objects
- Mutable default arguments (common pitfall)
"""

# ============================================================================
# SECTION 1: Introduction to Mutable Types
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: Understanding Mutability")
    print("=" * 70)

    # MUTABLE means "can be changed"
    # Mutable objects can be modified IN-PLACE without creating a new object

    # Let's demonstrate with a list:
    my_list = [1, 2, 3]
    print(f"Initial list: {my_list}, id = {id(my_list)}")

    # Modify the list in-place
    original_id = id(my_list)
    my_list.append(4)  # Modifies the SAME object

    print(f"After append: {my_list}, id = {id(my_list)}")
    print(f"Same object? {original_id == id(my_list)}")
    print("Yes! The object was modified, not replaced.")

    # CONTRAST with immutable types:
    my_int = 10
    original_id = id(my_int)
    my_int = my_int + 1  # Creates a NEW object

    print(f"\nFor immutable int, same object? {original_id == id(my_int)}")
    print("No! A new object was created.")

    # ============================================================================
    # SECTION 2: Common Mutable Types
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: Mutable Types in Python")
    print("=" * 70)

    # Python's mutable built-in types:
    mutable_examples = {
        "list": [1, 2, 3],
        "dict": {"key": "value"},
        "set": {1, 2, 3},
        "bytearray": bytearray(b"hello"),
    }

    print("\nDemonstrating mutable types:")
    for type_name, value in mutable_examples.items():
        print(f"  {type_name:12} : {value} (type: {type(value).__name__})")

    # All of these can be modified in-place!

    # ============================================================================
    # SECTION 3: Aliasing - Multiple Names for the Same Object
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: Aliasing with Mutable Objects")
    print("=" * 70)

    # Aliasing occurs when multiple variables reference the same object
    # This is CRUCIAL to understand with mutable types!

    list1 = [1, 2, 3]
    list2 = list1  # list2 is an ALIAS for list1 (same object!)

    print(f"list1 = {list1}, id = {id(list1)}")
    print(f"list2 = {list2}, id = {id(list2)}")
    print(f"Are they the same object? {list1 is list2}")

    # Now modify through list1:
    list1.append(4)

    print(f"\nAfter list1.append(4):")
    print(f"list1 = {list1}")
    print(f"list2 = {list2}")  # list2 also changed!

    print("\nIMPORTANT: Both variables reference the same object!")
    print("Modifying through one affects the other.")

    # MEMORY MODEL:
    # STACK           HEAP
    # ┌───────┐      ┌─────────────┐
    # │ list1─┼─────>│ [1, 2, 3, 4]│
    # │ list2─┼─────>│             │
    # └───────┘      └─────────────┘

    # ============================================================================
    # SECTION 4: Mutation vs. Reassignment
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: Mutation vs. Reassignment")
    print("=" * 70)

    # MUTATION: Changing the object in-place
    # REASSIGNMENT: Making a variable reference a different object

    # Setup:
    list_a = [1, 2, 3]
    list_b = list_a

    print("Initial state:")
    print(f"  list_a = {list_a}, id = {id(list_a)}")
    print(f"  list_b = {list_b}, id = {id(list_b)}")

    # MUTATION: Modifies the shared object
    list_a.append(4)
    print("\nAfter MUTATION (list_a.append(4)):")
    print(f"  list_a = {list_a}, id = {id(list_a)}")
    print(f"  list_b = {list_b}, id = {id(list_b)}")
    print("  Both changed! (same object)")

    # REASSIGNMENT: Changes what list_a references
    list_a = [10, 20, 30]
    print("\nAfter REASSIGNMENT (list_a = [10, 20, 30]):")
    print(f"  list_a = {list_a}, id = {id(list_a)}")
    print(f"  list_b = {list_b}, id = {id(list_b)}")
    print("  Only list_a changed! (different objects now)")

    # ============================================================================
    # SECTION 5: Lists - In-Place Modifications
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: List Mutation Methods")
    print("=" * 70)

    # Methods that MUTATE the list (modify in-place):
    nums = [3, 1, 4, 1, 5]
    print(f"Original: nums = {nums}, id = {id(nums)}")

    original_id = id(nums)

    # Mutating operations:
    nums.append(9)          # Add to end
    print(f"After append(9): {nums}, same object? {id(nums) == original_id}")

    nums.extend([2, 6])     # Add multiple elements
    print(f"After extend([2,6]): {nums}, same object? {id(nums) == original_id}")

    nums.insert(0, 0)       # Insert at index
    print(f"After insert(0,0): {nums}, same object? {id(nums) == original_id}")

    nums.remove(1)          # Remove first occurrence
    print(f"After remove(1): {nums}, same object? {id(nums) == original_id}")

    nums.sort()             # Sort in-place
    print(f"After sort(): {nums}, same object? {id(nums) == original_id}")

    nums.reverse()          # Reverse in-place
    print(f"After reverse(): {nums}, same object? {id(nums) == original_id}")

    print("\nAll operations modified the SAME object!")

    # ============================================================================
    # SECTION 6: Dictionaries - In-Place Modifications
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: Dictionary Mutation")
    print("=" * 70)

    person = {"name": "Alice", "age": 30}
    print(f"Original: person = {person}, id = {id(person)}")

    original_id = id(person)

    # Mutating operations:
    person["city"] = "NYC"                    # Add new key
    print(f"After adding key: {person}, same object? {id(person) == original_id}")

    person["age"] = 31                        # Modify existing key
    print(f"After modifying: {person}, same object? {id(person) == original_id}")

    person.update({"country": "USA"})         # Update with dict
    print(f"After update(): {person}, same object? {id(person) == original_id}")

    del person["city"]                        # Delete key
    print(f"After del: {person}, same object? {id(person) == original_id}")

    person.pop("country")                     # Pop key
    print(f"After pop(): {person}, same object? {id(person) == original_id}")

    print("\nAll operations modified the SAME dictionary object!")

    # ============================================================================
    # SECTION 7: Sets - In-Place Modifications
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 7: Set Mutation")
    print("=" * 70)

    numbers = {1, 2, 3}
    print(f"Original: numbers = {numbers}, id = {id(numbers)}")

    original_id = id(numbers)

    # Mutating operations:
    numbers.add(4)                           # Add element
    print(f"After add(4): {numbers}, same object? {id(numbers) == original_id}")

    numbers.update({5, 6})                   # Add multiple elements
    print(f"After update: {numbers}, same object? {id(numbers) == original_id}")

    numbers.remove(1)                        # Remove element (error if not present)
    print(f"After remove(1): {numbers}, same object? {id(numbers) == original_id}")

    numbers.discard(2)                       # Remove element (no error if absent)
    print(f"After discard(2): {numbers}, same object? {id(numbers) == original_id}")

    print("\nAll operations modified the SAME set object!")

    # ============================================================================
    # SECTION 8: Mutable Objects as Function Parameters
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 8: Mutable Parameters in Functions")
    print("=" * 70)

    def modify_list(lst):
        """
        This function modifies the list parameter in-place
        """
        print(f"  Inside function, before: lst = {lst}, id = {id(lst)}")
        lst.append(100)  # Mutates the SAME object
        print(f"  Inside function, after: lst = {lst}, id = {id(lst)}")

    def reassign_list(lst):
        """
        This function reassigns the local parameter
        """
        print(f"  Inside function, before: lst = {lst}, id = {id(lst)}")
        lst = [100, 200, 300]  # Creates NEW object, rebinds local lst
        print(f"  Inside function, after: lst = {lst}, id = {id(lst)}")

    # Test mutation:
    my_list = [1, 2, 3]
    print(f"Before modify_list(): my_list = {my_list}, id = {id(my_list)}")
    modify_list(my_list)
    print(f"After modify_list(): my_list = {my_list}, id = {id(my_list)}")
    print("The original list was MODIFIED!")

    print()

    # Test reassignment:
    my_list = [1, 2, 3]
    print(f"Before reassign_list(): my_list = {my_list}, id = {id(my_list)}")
    reassign_list(my_list)
    print(f"After reassign_list(): my_list = {my_list}, id = {id(my_list)}")
    print("The original list was NOT affected (local reassignment only)!")

    # ============================================================================
    # SECTION 9: Mutable Default Arguments - DANGEROUS PITFALL!
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 9: Mutable Default Arguments (COMMON BUG!)")
    print("=" * 70)

    # WRONG WAY - DON'T DO THIS:
    def append_to_list_wrong(item, my_list=[]):  # BAD! Mutable default
        """
        BUGGY FUNCTION: Uses mutable default argument
        """
        my_list.append(item)
        return my_list

    # The default list is created ONCE when the function is defined
    # It's shared across all calls that use the default!

    print("Calling with mutable default argument:")
    result1 = append_to_list_wrong(1)
    print(f"  First call: {result1}, id = {id(result1)}")

    result2 = append_to_list_wrong(2)
    print(f"  Second call: {result2}, id = {id(result2)}")

    result3 = append_to_list_wrong(3)
    print(f"  Third call: {result3}, id = {id(result3)}")

    print("\nAll calls share the SAME default list object!")
    print(f"result1 is result2 is result3: {result1 is result2 is result3}")

    # CORRECT WAY:
    def append_to_list_correct(item, my_list=None):  # GOOD! Use None as default
        """
        CORRECT FUNCTION: Uses None as default, creates new list each time
        """
        if my_list is None:
            my_list = []  # Create NEW list each time
        my_list.append(item)
        return my_list

    print("\nCalling with None default and creating new list:")
    result1 = append_to_list_correct(1)
    print(f"  First call: {result1}, id = {id(result1)}")

    result2 = append_to_list_correct(2)
    print(f"  Second call: {result2}, id = {id(result2)}")

    result3 = append_to_list_correct(3)
    print(f"  Third call: {result3}, id = {id(result3)}")

    print("\nEach call gets a NEW list object!")

    # ============================================================================
    # SECTION 10: Nested Mutable Structures
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 10: Nested Mutable Structures")
    print("=" * 70)

    # Lists can contain lists - nested mutable structures
    matrix = [[1, 2], [3, 4], [5, 6]]
    print(f"Original matrix: {matrix}")

    # What if we try to create a copy by aliasing?
    matrix_alias = matrix
    matrix_alias[0][0] = 999  # Modify nested element

    print(f"After modifying through alias:")
    print(f"  matrix = {matrix}")
    print(f"  matrix_alias = {matrix_alias}")
    print("Both changed! They reference the same nested structure.")

    # Even modifying a nested element affects all aliases:
    row = matrix[0]  # Get reference to first row
    print(f"\nrow = {row}, id = {id(row)}")
    print(f"matrix[0] id = {id(matrix[0])}")
    print(f"Same object? {row is matrix[0]}")

    row.append(100)
    print(f"After row.append(100):")
    print(f"  matrix = {matrix}")

    # ============================================================================
    # SECTION 11: Comparing Mutable vs Immutable Behavior
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 11: Side-by-Side Comparison")
    print("=" * 70)

    print("IMMUTABLE (tuple):")
    t1 = (1, 2, 3)
    t2 = t1
    print(f"  t1 = {t1}, id = {id(t1)}")
    print(f"  t2 = {t2}, id = {id(t2)}")
    t1 = t1 + (4,)  # Creates new tuple
    print(f"  After t1 = t1 + (4,):")
    print(f"  t1 = {t1}, id = {id(t1)} (NEW object)")
    print(f"  t2 = {t2}, id = {id(t2)} (unchanged)")

    print("\nMUTABLE (list):")
    l1 = [1, 2, 3]
    l2 = l1
    print(f"  l1 = {l1}, id = {id(l1)}")
    print(f"  l2 = {l2}, id = {id(l2)}")
    l1.append(4)  # Mutates existing list
    print(f"  After l1.append(4):")
    print(f"  l1 = {l1}, id = {id(l1)} (SAME object)")
    print(f"  l2 = {l2}, id = {id(l2)} (CHANGED!)")

    # ============================================================================
    # SECTION 12: When Mutable Types Behave Like Immutable
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 12: Operations That Return New Objects")
    print("=" * 70)

    # Some operations on mutable types return NEW objects instead of mutating

    original_list = [1, 2, 3]
    print(f"Original: {original_list}, id = {id(original_list)}")

    # These create NEW lists:
    sorted_list = sorted(original_list)  # sorted() returns new list
    print(f"sorted(list): {sorted_list}, id = {id(sorted_list)} (NEW)")

    concatenated = original_list + [4, 5]  # + creates new list
    print(f"list + [4,5]: {concatenated}, id = {id(concatenated)} (NEW)")

    sliced = original_list[:]  # Slicing creates new list
    print(f"list[:]: {sliced}, id = {id(sliced)} (NEW)")

    print(f"\nOriginal unchanged: {original_list}, id = {id(original_list)}")

    # Compare to in-place methods:
    original_list.sort()  # Mutates in place
    print(f"After .sort(): {original_list}, id = {id(original_list)} (SAME)")

    # ============================================================================
    # SECTION 13: Practical Implications
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 13: Real-World Implications")
    print("=" * 70)

    print("""
    WHEN MUTABILITY CAUSES PROBLEMS:

    1. Unexpected Shared State:
       - Function modifies a list you passed
       - Multiple parts of code share the same object
       - Debugging becomes difficult

    2. Mutable Default Arguments:
       - Default list/dict is shared across function calls
       - Leads to subtle bugs that are hard to track

    3. Concurrent Programming:
       - Mutable objects are not thread-safe
       - Need locks or synchronization

    WHEN MUTABILITY IS USEFUL:

    1. Performance:
       - In-place modification is faster
       - Avoids creating many intermediate objects

    2. Shared State (intentional):
       - Multiple parts of code need access to same data
       - Caching mechanisms

    3. Data Structures:
       - Stacks, queues, graphs often need mutation
       - Building complex structures incrementally
    """)

    # ============================================================================
    # SECTION 14: Key Takeaways
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    print("""
    1. Mutable types: list, dict, set, bytearray, custom objects
    2. Mutable objects can be modified in-place
    3. Multiple variables can reference the same mutable object (aliasing)
    4. Mutations affect all references to the object
    5. Mutation ≠ Reassignment (different operations!)
    6. Mutable objects passed to functions can be modified by the function
    7. NEVER use mutable default arguments (use None instead)
    8. Some operations return new objects (sorted, +, [:])
    9. Other operations mutate in-place (.sort(), .append(), etc.)
    10. Understanding mutability prevents many common bugs!

    GOLDEN RULE: 
    When in doubt, check if id() changes after an operation!
    """)

    # ============================================================================
    # PRACTICE EXERCISES
    # ============================================================================

    print("\n" + "=" * 70)
    print("PRACTICE EXERCISES")
    print("=" * 70)

    print("""
    Try these exercises to master mutable types:

    1. Create a function that accidentally modifies a list argument.
       Then fix it to avoid the modification.

    2. Demonstrate the mutable default argument bug with a dictionary.

    3. Create a 3x3 matrix (list of lists). Create an alias and modify
       one element. What happens to both references?

    4. Write a function that takes a list and returns a modified version
       WITHOUT changing the original list.

    5. Compare the performance of in-place sort (.sort()) vs. creating
       a new sorted list (sorted()) for a large list.

    6. Create a scenario where aliasing is INTENTIONAL and beneficial.

    See exercises_02_intermediate.py for complete practice problems!
    """)
```


## Exercises

**Exercise 1.**
Write a script that creates 10 different types of Python objects (int, float, str, list, dict, set, tuple, bool, bytes, bytearray) and prints `sys.getsizeof()` for each. Sort and display them from smallest to largest, demonstrating the per-object overhead on the heap.

??? success "Solution to Exercise 1"
        ```python
        import sys

        objects = [
            ("int", 42),
            ("float", 3.14),
            ("str", "hello"),
            ("list", [1, 2, 3]),
            ("dict", {"a": 1}),
            ("set", {1, 2, 3}),
            ("tuple", (1, 2, 3)),
            ("bool", True),
            ("bytes", b"hello"),
            ("bytearray", bytearray(b"hello")),
        ]

        sizes = [(name, sys.getsizeof(obj)) for name, obj in objects]
        sizes.sort(key=lambda x: x[1])

        print(f"{'Type':<12} {'Size (bytes)':>12}")
        print("-" * 26)
        for name, size in sizes:
            print(f"{name:<12} {size:>12}")
        ```

---

**Exercise 2.**
Demonstrate memory pool reuse for small objects by creating and deleting 1,000 small lists (each containing a single integer), then creating 1,000 more. Use `id()` to show that some of the new objects reuse the same memory addresses as the deleted ones. Print the number of reused addresses.

??? success "Solution to Exercise 2"
        ```python
        # Phase 1: create and record IDs, then delete
        old_ids = set()
        temp = []
        for i in range(1_000):
            obj = [i]
            old_ids.add(id(obj))
            temp.append(obj)
        del temp  # Free all

        # Phase 2: create new objects and check for reused addresses
        reused = 0
        for i in range(1_000):
            obj = [i]
            if id(obj) in old_ids:
                reused += 1

        print(f"Reused addresses: {reused} out of 1,000")
        ```

---

**Exercise 3.**
Compare heap fragmentation effects: (a) create a list of 10,000 small lists, delete every other one, then measure total tracked memory with `tracemalloc`; (b) repeat but delete all at once instead. Print peak and current memory for both scenarios and explain the difference.

??? success "Solution to Exercise 3"
        ```python
        import tracemalloc
        import gc

        # Scenario (a): delete every other one
        tracemalloc.start()
        items = [[i] for i in range(10_000)]
        for i in range(0, 10_000, 2):
            items[i] = None
        gc.collect()
        curr_a, peak_a = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Scenario (b): delete all at once
        tracemalloc.start()
        items = [[i] for i in range(10_000)]
        items.clear()
        gc.collect()
        curr_b, peak_b = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"Alternating delete - Current: {curr_a/1024:.1f} KB, "
              f"Peak: {peak_a/1024:.1f} KB")
        print(f"Bulk delete        - Current: {curr_b/1024:.1f} KB, "
              f"Peak: {peak_b/1024:.1f} KB")
        ```

---
