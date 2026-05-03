# Recursion & Stack

!!! tip "Mental Model"
    Every recursive call adds a new frame to the call stack, like stacking plates. Python enforces a default limit of about 1,000 plates to prevent the program from consuming unbounded memory. If your recursion is too deep, either add a base case, increase the limit with caution, or rewrite the algorithm iteratively.

## Stack Depth

### 1. Recursion Limit

```python
import sys

# Default limit
print(sys.getrecursionlimit())  # Usually 1000
```

### 2. Stack Overflow

```python
def infinite():
    return infinite()

try:
    infinite()
except RecursionError as e:
    print("Stack overflow!")
```

## Recursive Frames

### 1. Frame Per Call

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# factorial(5) creates 5 frames
```

**Stack:**
```
[factorial(5)]
[factorial(4)]
[factorial(3)]
[factorial(2)]
[factorial(1)]  # Base case
```

### 2. Memory Growth

```python
def deep_recursion(n):
    if n == 0:
        return
    return deep_recursion(n - 1)

# Each call adds frame to stack
deep_recursion(100)  # 100 frames
```

## Tail Recursion

### 1. Not Optimized

Python doesn't optimize tail calls:

```python
def factorial(n, acc=1):
    if n <= 1:
        return acc
    return factorial(n - 1, n * acc)

# Still creates frames
```

### 2. Use Iteration

```python
# Better: iterative
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# No stack growth
```

## Adjust Limit

### 1. Increase Limit

```python
import sys

# Increase (carefully!)
sys.setrecursionlimit(2000)

# Now can recurse deeper
```

### 2. Dangers

```python
# Too high risks:
# - Stack overflow crash
# - Memory exhaustion
# - System instability

# Use with caution!
```

## Deep Recursion

### 1. Problem

```python
def tree_depth(node):
    if not node:
        return 0
    left = tree_depth(node.left)
    right = tree_depth(node.right)
    return 1 + max(left, right)

# Deep tree → stack overflow
```

### 2. Solution

```python
# Use iteration + explicit stack
def tree_depth(root):
    if not root:
        return 0
        
    stack = [(root, 1)]
    max_depth = 0
    
    while stack:
        node, depth = stack.pop()
        max_depth = max(max_depth, depth)
        
        if node.left:
            stack.append((node.left, depth + 1))
        if node.right:
            stack.append((node.right, depth + 1))
    
    return max_depth
```

## Stack Trace

### 1. View Stack

```python
import traceback

def a():
    b()

def b():
    c()
    
def c():
    traceback.print_stack()

a()
# Shows full call chain
```

### 2. Exception Stack

```python
def outer():
    middle()

def middle():
    inner()
    
def inner():
    raise ValueError("Error!")

try:
    outer()
except ValueError:
    traceback.print_exc()
    # Shows: inner -> middle -> outer
```

## Summary

### 1. Recursion

- Each call adds frame
- Limited by stack size
- Not tail-optimized
- Use iteration when deep

### 2. Stack Management

- Check recursion limit
- Increase carefully
- Prefer iteration
- Use explicit stack

---


## Runnable Example: `aliasing_and_copying.py`

```python
"""
04_intermediate_aliasing_copying.py

TOPIC: Aliasing, Shallow Copy, and Deep Copy
LEVEL: Intermediate  
DURATION: 60-75 minutes

LEARNING OBJECTIVES:
1. Master the concept of aliasing and its implications
2. Understand shallow copy vs deep copy
3. Learn different ways to copy objects in Python
4. Recognize when to use each copying strategy
5. Debug common issues related to object sharing

KEY CONCEPTS:
- Aliasing: multiple names for the same object
- Shallow copy: copies the structure but not nested objects
- Deep copy: recursively copies all nested objects
- copy module: copy.copy() and copy.deepcopy()
- List/dict comprehensions and slicing for copying
"""

import copy
import sys

# ============================================================================
# SECTION 1: Aliasing Recap
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: Understanding Aliasing")
    print("=" * 70)

    # Aliasing: When two or more variables reference the same object
    original = [1, 2, 3, 4, 5]
    alias = original  # alias points to the SAME object

    print(f"original = {original}, id = {id(original)}")
    print(f"alias = {alias}, id = {id(alias)}")
    print(f"Are they the same object? {original is alias}")

    # Modifying through alias affects original:
    alias.append(6)
    print(f"\nAfter alias.append(6):")
    print(f"original = {original}")
    print(f"alias = {alias}")

    # MEMORY MODEL:
    # ┌──────────┐     ┌────────────────────┐
    # │ original ├────>│  [1, 2, 3, 4, 5, 6]│
    # │ alias    ├────>│                    │
    # └──────────┘     └────────────────────┘

    # ============================================================================
    # SECTION 2: Creating Independent Copies
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: Why We Need Copies")
    print("=" * 70)

    # Sometimes we want an INDEPENDENT copy, not an alias
    # Question: How do we create a true copy?

    # Let's try the wrong way first (aliasing):
    list1 = [1, 2, 3]
    list2 = list1  # This is aliasing, not copying!

    list1.append(4)
    print(f"list1 = {list1}")
    print(f"list2 = {list2}  # Oops! Changed too")

    # ============================================================================
    # SECTION 3: Shallow Copy - Method 1: Slicing
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: Shallow Copy Using Slicing")
    print("=" * 70)

    # For lists, slicing creates a new list
    original = [1, 2, 3, 4, 5]
    copy_by_slice = original[:]  # [:] creates a shallow copy

    print(f"original = {original}, id = {id(original)}")
    print(f"copy_by_slice = {copy_by_slice}, id = {id(copy_by_slice)}")
    print(f"Are they the same object? {original is copy_by_slice}")

    # Now modifications are independent:
    copy_by_slice.append(6)
    print(f"\nAfter copy_by_slice.append(6):")
    print(f"original = {original} (unchanged)")
    print(f"copy_by_slice = {copy_by_slice} (changed)")

    # MEMORY MODEL:
    # ┌──────────┐     ┌───────────────┐
    # │ original ├────>│ [1, 2, 3, 4, 5]│
    # └──────────┘     └───────────────┘
    # ┌──────────────┐ ┌─────────────────┐
    # │copy_by_slice ├>│ [1, 2, 3, 4, 5, 6]│
    # └──────────────┘ └─────────────────┘

    # ============================================================================
    # SECTION 4: Shallow Copy - Method 2: list() Constructor
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: Shallow Copy Using Constructor")
    print("=" * 70)

    # Using type constructors also creates shallow copies
    original = [1, 2, 3]
    copy_by_constructor = list(original)

    print(f"original = {original}, id = {id(original)}")
    print(f"copy_by_constructor = {copy_by_constructor}, id = {id(copy_by_constructor)}")
    print(f"Same object? {original is copy_by_constructor}")

    # Works for other types too:
    original_dict = {"a": 1, "b": 2}
    copy_dict = dict(original_dict)
    print(f"\nDict copy: {original_dict is copy_dict} (False - different objects)")

    original_set = {1, 2, 3}
    copy_set = set(original_set)
    print(f"Set copy: {original_set is copy_set} (False - different objects)")

    # ============================================================================
    # SECTION 5: Shallow Copy - Method 3: copy.copy()
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: Shallow Copy Using copy.copy()")
    print("=" * 70)

    # The copy module provides a general-purpose shallow copy function
    original = [1, 2, 3, 4]
    shallow_copy = copy.copy(original)

    print(f"original = {original}, id = {id(original)}")
    print(f"shallow_copy = {shallow_copy}, id = {id(shallow_copy)}")
    print(f"Same object? {original is shallow_copy}")

    # copy.copy() works with any object:
    original_dict = {"x": 10, "y": 20}
    shallow_copy_dict = copy.copy(original_dict)
    print(f"\nDict: original is copy? {original_dict is shallow_copy_dict}")

    # ============================================================================
    # SECTION 6: The Problem with Shallow Copies
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: Shallow Copy Limitation - Nested Objects")
    print("=" * 70)

    # SHALLOW COPY creates a new outer container
    # BUT nested objects are still SHARED (aliased)!

    original = [[1, 2], [3, 4], [5, 6]]
    shallow = original[:]  # Shallow copy

    print("Original and shallow copy:")
    print(f"original = {original}, id = {id(original)}")
    print(f"shallow = {shallow}, id = {id(shallow)}")
    print(f"Different objects? {original is not shallow}")

    # Check nested lists:
    print(f"\nAre nested lists the same?")
    print(f"original[0] is shallow[0]? {original[0] is shallow[0]}")  # True!
    print(f"original[1] is shallow[1]? {original[1] is shallow[1]}")  # True!

    # Modify a nested list:
    shallow[0].append(99)

    print(f"\nAfter shallow[0].append(99):")
    print(f"original = {original}  # Changed!")
    print(f"shallow = {shallow}   # Changed!")

    print("\nWHY? The outer lists are different, but they share nested lists!")

    # MEMORY MODEL:
    # ┌──────────┐     ┌─────────┐     ┌──────────┐
    # │ original ├────>│ List A  ├────>│ [1, 2, 99]│<─┐
    # └──────────┘     │ (outer) │  ┌─>│ [3, 4]    │<─┼─┐
    #                  └─────────┘  │  │ [5, 6]    │<─┼─┼─┐
    #                               │  └──────────┘  │ │ │
    # ┌──────────┐     ┌─────────┐ │                │ │ │
    # │ shallow  ├────>│ List B  ├─┘                │ │ │
    # └──────────┘     │ (outer) │──────────────────┘ │ │
    #                  │         │────────────────────┘ │
    #                  └─────────┘──────────────────────┘
    #
    # Lists A and B are different (shallow copy worked for outer list)
    # BUT they share the same nested lists (shallow copy limitation)

    # ============================================================================
    # SECTION 7: Deep Copy - The Solution
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 7: Deep Copy Using copy.deepcopy()")
    print("=" * 70)

    # DEEP COPY recursively copies ALL objects, including nested ones
    original = [[1, 2], [3, 4], [5, 6]]
    deep = copy.deepcopy(original)

    print("Original and deep copy:")
    print(f"original = {original}, id = {id(original)}")
    print(f"deep = {deep}, id = {id(deep)}")
    print(f"Different outer objects? {original is not deep}")

    # Check nested lists:
    print(f"\nAre nested lists the same?")
    print(f"original[0] is deep[0]? {original[0] is deep[0]}")  # False!
    print(f"original[1] is deep[1]? {original[1] is deep[1]}")  # False!

    # Now modifications are truly independent:
    deep[0].append(99)

    print(f"\nAfter deep[0].append(99):")
    print(f"original = {original}  # Unchanged!")
    print(f"deep = {deep}        # Changed!")

    # MEMORY MODEL:
    # ┌──────────┐     ┌─────────┐     ┌──────────┐
    # │ original ├────>│ List A  ├────>│ [1, 2]   │
    # └──────────┘     │         │     │ [3, 4]   │
    #                  └─────────┘     │ [5, 6]   │
    #                                  └──────────┘
    # ┌──────────┐     ┌─────────┐     ┌──────────┐
    # │ deep     ├────>│ List B  ├────>│ [1, 2, 99]│
    # └──────────┘     │         │     │ [3, 4]    │
    #                  └─────────┘     │ [5, 6]    │
    #                                  └──────────┘
    # Everything is copied - complete independence!

    # ============================================================================
    # SECTION 8: Shallow vs Deep Copy - Side by Side Comparison
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 8: Shallow vs Deep Copy Comparison")
    print("=" * 70)

    # Create a nested structure
    original = {
        "name": "Alice",
        "scores": [95, 87, 92],
        "metadata": {"grade": "A", "year": 2024}
    }

    shallow = copy.copy(original)
    deep = copy.deepcopy(original)

    print("Testing modifications:\n")

    # 1. Modify top-level value (immutable string):
    shallow["name"] = "Bob"
    print("After shallow['name'] = 'Bob':")
    print(f"  original['name'] = {original['name']} (unchanged)")
    print(f"  shallow['name'] = {shallow['name']} (changed)")
    print("  Reason: Reassignment creates new reference\n")

    # 2. Modify nested list through shallow copy:
    shallow["scores"].append(100)
    print("After shallow['scores'].append(100):")
    print(f"  original['scores'] = {original['scores']} (CHANGED!)")
    print(f"  shallow['scores'] = {shallow['scores']} (changed)")
    print("  Reason: Nested list is shared (shallow copy)\n")

    # 3. Modify nested list through deep copy:
    deep["scores"].append(200)
    print("After deep['scores'].append(200):")
    print(f"  original['scores'] = {original['scores']} (unchanged)")
    print(f"  deep['scores'] = {deep['scores']} (changed)")
    print("  Reason: Nested list is independent (deep copy)\n")

    # ============================================================================
    # SECTION 9: When to Use Each Copying Method
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 9: Choosing the Right Copy Method")
    print("=" * 70)

    print("""
    ALIASING (no copy):
      original = my_list

      When to use:
      - You WANT shared state
      - Passing to functions that should modify original
      - Memory efficiency is critical
      - You want changes to propagate

    SHALLOW COPY:
      copy = my_list[:] 
      copy = list(my_list)
      copy = copy.copy(my_list)

      When to use:
      - Simple structures (no nested mutable objects)
      - You want to modify top-level independently
      - Nested objects can be shared
      - Performance matters (faster than deep copy)

    DEEP COPY:
      copy = copy.deepcopy(my_list)

      When to use:
      - Complex nested structures
      - Complete independence required
      - Nested mutable objects (lists, dicts)
      - Safety over performance
    """)

    # ============================================================================
    # SECTION 10: Performance Comparison
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 10: Performance Comparison")
    print("=" * 70)

    import time

    # Create a nested structure
    nested_list = [[i for i in range(100)] for j in range(100)]

    # Measure aliasing (no copy):
    start = time.time()
    for _ in range(1000):
        alias = nested_list
    alias_time = time.time() - start

    # Measure shallow copy:
    start = time.time()
    for _ in range(1000):
        shallow = nested_list[:]
    shallow_time = time.time() - start

    # Measure deep copy:
    start = time.time()
    for _ in range(1000):
        deep = copy.deepcopy(nested_list)
    deep_time = time.time() - start

    print(f"Aliasing:     {alias_time:.6f} seconds (fastest)")
    print(f"Shallow copy: {shallow_time:.6f} seconds (medium)")
    print(f"Deep copy:    {deep_time:.6f} seconds (slowest)")
    print(f"\nDeep copy is {deep_time/shallow_time:.1f}x slower than shallow copy")

    # ============================================================================
    # SECTION 11: Copying Different Data Structures
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 11: Copying Various Data Structures")
    print("=" * 70)

    # LISTS:
    print("Lists:")
    orig_list = [1, 2, [3, 4]]
    print(f"  Shallow: {orig_list[:] is orig_list} (different)")
    print(f"  Deep: {copy.deepcopy(orig_list) is orig_list} (different)")

    # DICTIONARIES:
    print("\nDictionaries:")
    orig_dict = {"a": 1, "b": [2, 3]}
    print(f"  Shallow: {orig_dict.copy() is orig_dict} (different)")
    print(f"  Deep: {copy.deepcopy(orig_dict) is orig_dict} (different)")

    # SETS:
    print("\nSets:")
    orig_set = {1, 2, 3}
    print(f"  Shallow: {orig_set.copy() is orig_set} (different)")
    print(f"  Deep: {copy.deepcopy(orig_set) is orig_set} (different)")

    # TUPLES (interesting case!):
    print("\nTuples:")
    orig_tuple = (1, 2, [3, 4])
    shallow_tuple = copy.copy(orig_tuple)
    deep_tuple = copy.deepcopy(orig_tuple)

    print(f"  Shallow: {shallow_tuple is orig_tuple} (SAME!)")
    print(f"  Deep: {deep_tuple is orig_tuple} (different)")
    print("  Note: Shallow copy of tuple returns the same object (immutable)")
    print("  But nested list is still shared!")

    # ============================================================================
    # SECTION 12: Custom Objects and Copying
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 12: Copying Custom Objects")
    print("=" * 70)

    class Person:
        def __init__(self, name, friends):
            self.name = name
            self.friends = friends  # list of friend names

        def __repr__(self):
            return f"Person('{self.name}', {self.friends})"

    # Create original
    alice = Person("Alice", ["Bob", "Charlie"])
    print(f"Original: {alice}, id = {id(alice)}")

    # Shallow copy
    alice_shallow = copy.copy(alice)
    print(f"Shallow: {alice_shallow}, id = {id(alice_shallow)}")
    print(f"Different objects? {alice is not alice_shallow}")
    print(f"Share friends list? {alice.friends is alice_shallow.friends}")

    # Modify friends through shallow copy:
    alice_shallow.friends.append("Dave")
    print(f"\nAfter alice_shallow.friends.append('Dave'):")
    print(f"  alice.friends: {alice.friends}  # Changed!")
    print(f"  alice_shallow.friends: {alice_shallow.friends}")

    # Deep copy
    alice_deep = copy.deepcopy(alice)
    print(f"\nDeep: {alice_deep}, id = {id(alice_deep)}")
    print(f"Different objects? {alice is not alice_deep}")
    print(f"Share friends list? {alice.friends is alice_deep.friends}")

    alice_deep.friends.append("Eve")
    print(f"\nAfter alice_deep.friends.append('Eve'):")
    print(f"  alice.friends: {alice.friends}  # Unchanged")
    print(f"  alice_deep.friends: {alice_deep.friends}")

    # ============================================================================
    # SECTION 13: Common Pitfalls and Debugging
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 13: Common Pitfalls")
    print("=" * 70)

    print("""
    PITFALL 1: Thinking = creates a copy
      wrong = original  # This is aliasing!
      correct = copy.copy(original)

    PITFALL 2: Using shallow copy for nested structures
      nested = [[1, 2], [3, 4]]
      copy = nested[:]  # Nested lists still shared!
      Use: copy = copy.deepcopy(nested)

    PITFALL 3: Forgetting that tuple copying returns same object
      t = (1, 2, 3)
      t_copy = copy.copy(t)  # t_copy is t!

    PITFALL 4: Deep copying when not needed (performance cost)
      simple = [1, 2, 3, 4]  # No nested structures
      copy = copy.deepcopy(simple)  # Overkill! Use simple[:]

    DEBUGGING TIP:
      Use 'is' to check if objects are shared:
      print(f"Shared? {obj1 is obj2}")

      Use id() to track objects:
      print(f"obj1 id: {id(obj1)}")
      print(f"obj2 id: {id(obj2)}")
    """)

    # ============================================================================
    # SECTION 14: Key Takeaways
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    print("""
    1. Aliasing: = creates a reference, not a copy
    2. Shallow copy: Creates new outer object, shares nested objects
    3. Deep copy: Recursively copies all objects
    4. Shallow copy methods: [:], list(), dict.copy(), copy.copy()
    5. Deep copy method: copy.deepcopy()
    6. Shallow copy is faster but limited for nested structures
    7. Deep copy provides complete independence but is slower
    8. Always use 'is' to check if objects are shared
    9. Tuples are special: shallow copy returns the same object
    10. Choose copying strategy based on structure and requirements

    DECISION TREE:
    - Need shared state? → Use aliasing (=)
    - Simple structure? → Use shallow copy ([:], .copy())
    - Nested mutable objects? → Use deep copy (deepcopy())
    - Unsure? → Use deep copy (safer)
    """)

    # ============================================================================
    # PRACTICE EXERCISES
    # ============================================================================

    print("\n" + "=" * 70)
    print("PRACTICE EXERCISES")
    print("=" * 70)

    print("""
    Master copying with these exercises:

    1. Create a 3-level nested list. Show that shallow copy fails but
       deep copy succeeds in creating independence.

    2. Create a custom class with nested attributes. Demonstrate the
       difference between shallow and deep copy.

    3. Write a function that takes a list and returns a modified copy
       without changing the original. Test with nested lists.

    4. Measure the performance difference between shallow and deep copy
       for various structure sizes (10x10, 100x100, 1000x1000).

    5. Create a dictionary with nested lists and dicts. Show what happens
       with aliasing, shallow copy, and deep copy when you modify values.

    6. Debug a piece of code where unwanted aliasing causes bugs.

    See exercises_02_intermediate.py for complete practice problems!
    """)
```


## Exercises

**Exercise 1.**
Write both a recursive and an iterative version of a function that computes the sum 1 + 2 + ... + n. Test both with n = 500 and n = 5000. Show that the recursive version fails with a `RecursionError` for large n (if the limit is 1000) while the iterative version succeeds.

??? success "Solution to Exercise 1"
        ```python
        import sys

        def sum_recursive(n):
            if n <= 0:
                return 0
            return n + sum_recursive(n - 1)

        def sum_iterative(n):
            total = 0
            for i in range(1, n + 1):
                total += i
            return total

        # Test with n = 500 (within default limit)
        print(f"Recursive sum(500): {sum_recursive(500)}")
        print(f"Iterative sum(500): {sum_iterative(500)}")

        # Test with n = 5000 (exceeds default limit)
        print(f"Iterative sum(5000): {sum_iterative(5000)}")

        try:
            sum_recursive(5000)
        except RecursionError:
            print("Recursive sum(5000): RecursionError!")
        ```

---

**Exercise 2.**
Write a recursive Fibonacci function that prints the current recursion depth (pass it as a parameter). Call it with n = 10 and observe the maximum depth reached. Then rewrite it using an explicit stack (a list) to avoid recursion, and show it produces the same result.

??? success "Solution to Exercise 2"
        ```python
        max_depth = 0

        def fib_recursive(n, depth=0):
            global max_depth
            max_depth = max(max_depth, depth)
            if n <= 1:
                return n
            return (fib_recursive(n - 1, depth + 1)
                    + fib_recursive(n - 2, depth + 1))

        def fib_stack(n):
            if n <= 1:
                return n
            stack = [(n, False, 0, 0)]
            result = 0
            while stack:
                num, has_left, left_val, right_val = stack[-1]
                if num <= 1:
                    stack.pop()
                    result = num
                    if stack:
                        top = stack[-1]
                        if not top[1]:
                            stack[-1] = (top[0], True, num, 0)
                        else:
                            stack.pop()
                            result = top[2] + num
                            if stack:
                                top2 = stack[-1]
                                if not top2[1]:
                                    stack[-1] = (top2[0], True, result, 0)
                                else:
                                    stack.pop()
                                    result = top2[2] + result
                elif not has_left:
                    stack.append((num - 1, False, 0, 0))
                else:
                    stack.pop()
                    stack.append((num, True, left_val, 0))
                    stack.append((num - 2, False, 0, 0))
            return result

        # Simpler iterative approach:
        def fib_iterative(n):
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

        r1 = fib_recursive(10)
        print(f"Recursive fib(10) = {r1}, max depth = {max_depth}")

        r2 = fib_iterative(10)
        print(f"Iterative fib(10) = {r2}")
        print(f"Results match: {r1 == r2}")
        ```

---

**Exercise 3.**
Write a script that measures the memory cost of deep recursion using `tracemalloc`. Create a recursive function that descends to depth 500, taking a snapshot at the deepest level and at the top level. Compare the two snapshots and print the memory consumed by the stack frames.

??? success "Solution to Exercise 3"
        ```python
        import tracemalloc

        tracemalloc.start()

        top_snapshot = None
        deep_snapshot = None

        def recurse(depth, target):
            global deep_snapshot
            if depth == target:
                deep_snapshot = tracemalloc.take_snapshot()
                return
            recurse(depth + 1, target)

        top_snapshot = tracemalloc.take_snapshot()
        recurse(0, 500)

        diff = deep_snapshot.compare_to(top_snapshot, 'filename')
        total_growth = sum(s.size_diff for s in diff if s.size_diff > 0)

        print(f"Memory used by 500 stack frames: "
              f"{total_growth / 1024:.1f} KB")

        tracemalloc.stop()
        ```

---
