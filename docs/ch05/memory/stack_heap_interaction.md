# Stack-Heap Interaction

!!! tip "Mental Model"
    The stack holds names (variables), and the heap holds the actual objects. A variable on the stack is just an arrow pointing to its object on the heap. Multiple names can point to the same object, which is why aliasing works -- and why mutating through one name affects all names that share that arrow.

## Name-Object Binding

### 1. Names on Stack

```python
def function():
    x = [1, 2, 3]   # x on stack
                    # [1,2,3] on heap
```

**Memory:**
```
Stack:          Heap:
[frame]
  x -------->  [1, 2, 3]
```

### 2. Multiple Names

```python
def function():
    x = [1, 2, 3]
    y = x
    z = x
```

**Memory:**
```
Stack:          Heap:
[frame]
  x -------->
  y -------->  [1, 2, 3]
  z -------->
```

## Function Calls

### 1. Parameter Passing

```python
def process(lst):
    lst.append(4)

data = [1, 2, 3]
process(data)
```

**Memory:**
```
Stack:              Heap:
[main]
  data -------->
                    [1, 2, 3]
[process]
  lst -------->
```

### 2. Return Values

```python
def create():
    x = [1, 2, 3]
    return x

result = create()
```

**After return:**
```
Stack:          Heap:
[main]
  result ----> [1, 2, 3]
```

## Scope Impact

### 1. Local Scope

```python
def outer():
    x = [1, 2, 3]   # x in outer frame
    
    def inner():
        y = x       # y in inner frame
                    # Both point to heap
    inner()
```

### 2. Global Scope

```python
GLOBAL = [1, 2, 3]  # Global frame

def function():
    local = GLOBAL   # Local frame
                     # Both point to heap
```

## Object Lifetime

### 1. Outlives Frame

```python
def create():
    x = [1, 2, 3]
    return x
    # x removed from stack
    # Object stays on heap

result = create()
# Object still accessible
```

### 2. Multiple References

```python
def function():
    x = [1, 2, 3]
    global GLOBAL
    GLOBAL = x
    # x removed at return
    # Object kept by GLOBAL
```

## Closures

### 1. Captured Variables

```python
def outer():
    x = [1, 2, 3]   # Heap object
    
    def inner():
        return x    # Captures reference
    
    return inner

f = outer()
# outer frame gone
# x kept for closure
```

## Memory Efficiency

### 1. Sharing Objects

```python
# Efficient: one object
data = [1, 2, 3]
refs = [data] * 100

# 100 stack entries
# 1 heap object
```

### 2. Copying Objects

```python
# Inefficient: many objects
refs = [
    [1, 2, 3].copy()
    for _ in range(100)
]

# 100 stack entries
# 100 heap objects
```

## Summary

### 1. Interaction

- Names on stack
- Objects on heap
- Names point to objects
- Multiple names → one object

### 2. Lifetime

- Stack: function scope
- Heap: until GC'd
- Objects outlive frames

---


## Runnable Example: `variables_and_memory.py`

```python
"""
01_beginner_variables_and_memory.py

TOPIC: Introduction to Variables and Memory in Python
LEVEL: Beginner
DURATION: 45-60 minutes

LEARNING OBJECTIVES:
1. Understand what variables are in Python (names that reference objects)
2. Learn the difference between stack and heap memory
3. Explore Python's object model
4. Use id() to inspect memory addresses
5. Understand the concept of "everything is an object"

KEY CONCEPTS:
- Variables are names, not containers
- Objects live in heap memory
- Variable names are stored in namespaces (on the stack)
- id() returns the memory address of an object
- Python uses "pass by object reference" semantics
"""

# ============================================================================
# SECTION 1: Understanding Variables as References
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: Variables as References to Objects")
    print("=" * 70)

    # In Python, variables are NOT boxes that contain values.
    # Instead, variables are NAMES that REFERENCE objects in memory.

    # When we write this:
    x = 42

    # What actually happens:
    # 1. Python creates an integer object with value 42 in HEAP memory
    # 2. Python creates a name 'x' in the current namespace (STACK memory)
    # 3. Python makes 'x' REFERENCE (point to) the integer object

    # We can see WHERE in memory the object lives using id():
    print(f"\nVariable x references value: {x}")
    print(f"Memory address (id) of object: {id(x)}")
    print(f"Type of object: {type(x)}")

    # The id() function returns a unique identifier for an object
    # In CPython (the standard Python implementation), this is the memory address

    # ============================================================================
    # SECTION 2: Multiple Variables Can Reference the Same Object
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: Multiple Names for the Same Object")
    print("=" * 70)

    # Let's create another variable that references the same object
    y = x

    print(f"\nx = {x}, id(x) = {id(x)}")
    print(f"y = {y}, id(y) = {id(y)}")

    # Notice: id(x) and id(y) are THE SAME!
    # This means x and y are TWO NAMES for the SAME object in memory
    print(f"\nAre x and y the same object? {id(x) == id(y)}")

    # We can also use the 'is' operator to test object identity
    print(f"Using 'is' operator: x is y = {x is y}")

    # MEMORY MODEL:
    #
    # STACK (Namespace)          HEAP (Objects)
    # ┌──────────────┐           ┌──────────────┐
    # │ x  ───────────┼──────────>│   int: 42    │
    # │ y  ───────────┼──────────>│              │
    # └──────────────┘           └──────────────┘
    #
    # Both x and y point to the same integer object in heap memory

    # ============================================================================
    # SECTION 3: Assignment Creates New References, Not New Objects (Sometimes)
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: Understanding Assignment")
    print("=" * 70)

    # For small integers, Python uses a technique called "integer interning"
    # This means Python REUSES objects for common integers (-5 to 256)

    a = 100
    b = 100

    print(f"\na = {a}, id(a) = {id(a)}")
    print(f"b = {b}, id(b) = {id(b)}")
    print(f"Are a and b the same object? {a is b}")

    # For larger integers, Python creates separate objects
    # (Note: This behavior can vary based on how integers are created)

    large_a = 1000
    large_b = 1000

    print(f"\nlarge_a = {large_a}, id(large_a) = {id(large_a)}")
    print(f"large_b = {large_b}, id(large_b) = {id(large_b)}")
    print(f"Are large_a and large_b the same object? {large_a is large_b}")

    # IMPORTANT: This shows that Python optimizes memory for common values!

    # ============================================================================
    # SECTION 4: Reassignment Changes What a Variable References
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: Reassignment")
    print("=" * 70)

    # Let's start with a variable
    num = 10
    print(f"Initially: num = {num}, id = {id(num)}")

    # Now reassign it
    old_id = id(num)
    num = 20
    new_id = id(num)

    print(f"After reassignment: num = {num}, id = {id(num)}")
    print(f"Did the id change? {old_id != new_id}")

    # WHAT HAPPENED:
    # 1. num originally referenced an int object with value 10
    # 2. Assignment num = 20 makes num reference a DIFFERENT int object (value 20)
    # 3. The original object (10) might be garbage collected if nothing else references it
    #
    # MEMORY MODEL BEFORE:          MEMORY MODEL AFTER:
    # STACK      HEAP               STACK      HEAP
    # ┌────┐    ┌────────┐         ┌────┐    ┌────────┐
    # │num─┼───>│ int:10 │         │num─┼───>│ int:20 │
    # └────┘    └────────┘         └────┘    └────────┘
    #                                         ┌────────┐
    #                                         │ int:10 │ (may be garbage collected)
    #                                         └────────┘

    # ============================================================================
    # SECTION 5: Stack vs Heap Memory in Python
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: Stack vs Heap Memory")
    print("=" * 70)

    # STACK MEMORY:
    # - Stores function call information (call stack)
    # - Stores local variable NAMES (references)
    # - Stores function parameters
    # - Fixed size, automatically managed
    # - Very fast access
    # - Small in size

    # HEAP MEMORY:
    # - Stores all OBJECTS (integers, strings, lists, custom objects, etc.)
    # - Dynamically allocated
    # - Managed by Python's memory manager and garbage collector
    # - Slower than stack but more flexible
    # - Much larger than stack

    def demonstrate_stack_heap():
        """
        Function to demonstrate stack and heap usage
        """
        # When this function is called:
        # 1. A new frame is pushed onto the CALL STACK
        # 2. Local variable names are stored in this frame's namespace (STACK)
        # 3. Objects are created in HEAP memory

        local_var = "Hello"  # 'local_var' name on stack, string object in heap

        print(f"\nInside function:")
        print(f"  local_var = {local_var}")
        print(f"  id(local_var) = {id(local_var)}")

        return local_var  # Returns the reference, not the object itself

    result = demonstrate_stack_heap()
    print(f"\nOutside function:")
    print(f"  result = {result}")
    print(f"  id(result) = {id(result)}")

    # Notice: The id is the same! The string object is in heap memory,
    # and both local_var and result are just names that reference it.

    # When demonstrate_stack_heap() finishes:
    # - The function's stack frame is removed
    # - local_var name no longer exists
    # - But the string object STAYS in heap (because 'result' references it)

    # ============================================================================
    # SECTION 6: Everything is an Object in Python
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: Everything is an Object")
    print("=" * 70)

    # In Python, EVERYTHING is an object, including:
    # - Numbers
    # - Strings
    # - Functions
    # - Classes
    # - Modules
    # - Even types themselves!

    # Let's verify this:
    items = [
        42,                    # Integer
        3.14,                  # Float
        "Hello",              # String
        [1, 2, 3],           # List
        demonstrate_stack_heap, # Function
        int,                  # Type
    ]

    print("\nDemonstrating that everything has an id (memory address):")
    for item in items:
        print(f"  {str(item):30} -> id: {id(item)}, type: {type(item).__name__}")

    # ============================================================================
    # SECTION 7: The Difference Between '==' and 'is'
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 7: Equality vs Identity")
    print("=" * 70)

    # == compares VALUES (calls the __eq__ method)
    # is compares IDENTITY (checks if same object in memory)

    list1 = [1, 2, 3]
    list2 = [1, 2, 3]
    list3 = list1

    print(f"\nlist1 = {list1}, id = {id(list1)}")
    print(f"list2 = {list2}, id = {id(list2)}")
    print(f"list3 = {list3}, id = {id(list3)}")

    print(f"\nlist1 == list2: {list1 == list2}  # Same values")
    print(f"list1 is list2: {list1 is list2}  # Different objects")

    print(f"\nlist1 == list3: {list1 == list3}  # Same values")
    print(f"list1 is list3: {list1 is list3}  # Same object")

    # MEMORY MODEL:
    # STACK           HEAP
    # ┌──────┐       ┌──────────────┐
    # │list1─┼──────>│ [1, 2, 3]    │
    # │list3─┼──────>│              │
    # └──────┘       └──────────────┘
    # ┌──────┐       ┌──────────────┐
    # │list2─┼──────>│ [1, 2, 3]    │
    # └──────┘       └──────────────┘

    # ============================================================================
    # SECTION 8: Understanding sys.getsizeof()
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 8: Object Size in Memory")
    print("=" * 70)

    import sys

    # sys.getsizeof() tells us how many bytes an object occupies in memory

    objects = [
        42,
        "Hello",
        [1, 2, 3],
        {"key": "value"},
    ]

    print("\nMemory sizes of different objects:")
    for obj in objects:
        print(f"  {str(obj):30} -> {sys.getsizeof(obj)} bytes")

    # Notice:
    # - Even simple integers take up memory (28 bytes on most systems)
    # - This is because Python stores additional information:
    #   * Reference count
    #   * Type information
    #   * Object header

    # ============================================================================
    # SECTION 9: Key Takeaways
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    print("""
    1. Variables are NAMES that REFERENCE objects, not containers
    2. Objects live in HEAP memory
    3. Variable names are stored in STACK memory (in namespaces)
    4. Multiple variables can reference the same object
    5. id() gives us the memory address (identity) of an object
    6. 'is' checks object identity, '==' checks value equality
    7. Everything in Python is an object (has id, type, and value)
    8. Assignment creates new references, not necessarily new objects
    9. Python optimizes memory by reusing objects for common values
    10. Understanding memory is crucial for writing efficient code
    """)

    # ============================================================================
    # EXERCISES TO TRY:
    # ============================================================================

    print("\n" + "=" * 70)
    print("PRACTICE EXERCISES")
    print("=" * 70)

    print("""
    Try these exercises to test your understanding:

    1. Create two variables with the same string value and check if they're
       the same object using 'is'. Try with short strings and long strings.

    2. Create a list and assign it to two different variables. Modify the list
       through one variable and observe what happens to the other.

    3. Use id() to track what happens to an object when you reassign a variable.

    4. Write a function that takes a parameter and prints its id before and
       after reassigning the parameter inside the function.

    5. Compare the memory size (using sys.getsizeof()) of an empty list,
       a list with 10 elements, and a list with 100 elements.

    See exercises_01_beginner.py for complete practice problems!
    """)
```


## Exercises

**Exercise 1.**
Write a function `demonstrate_sharing()` that creates a list, passes it to three other functions (each of which appends an element), and then prints the final list back in the caller. Use `id()` to prove that all four functions operated on the same heap object.

??? success "Solution to Exercise 1"
        ```python
        def add_a(lst):
            print(f"  add_a sees id: {id(lst)}")
            lst.append("a")

        def add_b(lst):
            print(f"  add_b sees id: {id(lst)}")
            lst.append("b")

        def add_c(lst):
            print(f"  add_c sees id: {id(lst)}")
            lst.append("c")

        def demonstrate_sharing():
            data = [0]
            print(f"  caller id: {id(data)}")
            add_a(data)
            add_b(data)
            add_c(data)
            print(f"  Final list: {data}")

        demonstrate_sharing()
        ```

---

**Exercise 2.**
Write a function `closure_keeps_alive()` that creates a large list inside a local scope, returns a closure that references the list, and then verifies (using `weakref.ref`) that the list stays alive as long as the closure exists. Delete the closure and verify the list is collected.

??? success "Solution to Exercise 2"
        ```python
        import weakref
        import gc

        def closure_keeps_alive():
            data = list(range(10_000))
            ref = weakref.ref(data)

            def getter():
                return data[0]

            return getter, ref

        getter, ref = closure_keeps_alive()
        gc.collect()
        print(f"Closure alive -> list alive: {ref() is not None}")  # True

        del getter
        gc.collect()
        print(f"Closure deleted -> list alive: {ref() is not None}")  # False
        ```

---

**Exercise 3.**
Create a function `show_stack_heap(depth)` that recurses to the given depth. At each level, it creates a local list and prints `id()` of that list and the current depth. After the recursion completes, show that none of the local lists exist anymore by checking weak references created at each level.

??? success "Solution to Exercise 3"
        ```python
        import weakref
        import gc

        refs = []

        def show_stack_heap(depth, current=0):
            local_list = [current]
            refs.append(weakref.ref(local_list))
            print(f"  depth={current}, id={id(local_list)}")
            if current < depth:
                show_stack_heap(depth, current + 1)

        show_stack_heap(5)
        gc.collect()

        alive = sum(1 for r in refs if r() is not None)
        print(f"\nAfter recursion: {alive} of {len(refs)} lists still alive")
        # Should be 0 — all local lists were freed when frames unwound
        ```

---
