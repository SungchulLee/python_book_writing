# Stack & Heap Overview

!!! tip "Mental Model"
    Python's runtime uses two memory regions with different personalities. The stack is fast, organized, and automatic -- it grows and shrinks with function calls, holding local variable names. The heap is large, flexible, and managed by the garbage collector -- it stores every actual Python object. Names on the stack point to objects on the heap.

## Two Memory Areas

### 1. Stack

Function call frames and local names:

```python
def function():
    x = 10          # Name on stack
    y = 20          # Name on stack
    return x + y

# Stack grows/shrinks with calls
```

### 2. Heap

Objects storage:

```python
x = [1, 2, 3]       # Object on heap
y = "hello"         # Object on heap
z = 42              # Object on heap
```

## Stack Properties

### 1. Fast Access

```python
def compute():
    a = 10          # Fast stack access
    b = 20
    return a + b
```

### 2. Automatic Management

```python
def f():
    x = 10          # Stack allocated
    return x
    # x deallocated when f returns
```

### 3. Limited Size

```python
def recursive(n):
    if n == 0:
        return
    return recursive(n - 1)

# Too deep causes stack overflow
```

## Heap Properties

### 1. Dynamic Size

```python
# Can grow as needed
lst = []
for i in range(1000000):
    lst.append(i)   # Heap grows
```

### 2. Manual Management

```python
x = [1, 2, 3]       # Heap allocated
# Stays until GC'd
del x               # Remove reference
```

### 3. Slower Access

```python
# Heap access slower than stack
# But necessary for objects
```

## What Goes Where

### 1. Stack

- Function frames
- Local name bindings
- Return addresses
- Parameters

### 2. Heap

- All Python objects
- Lists, dicts, strings
- Integers, floats
- User-defined objects

## Memory Visualization

### 1. Example

```python
def process():
    x = [1, 2, 3]
    y = x
    return y
```

**Memory:**
```
Stack:
  [process frame]
    x -----> 
    y -----> [1, 2, 3] (Heap)
    
Heap:
  [1, 2, 3] object
```

### 2. Multiple Frames

```python
def outer():
    a = [1, 2]
    return inner(a)

def inner(param):
    b = param
    return b
```

**Stack:**
```
[outer frame]
  a -----> [1, 2] (Heap)
  
[inner frame]  
  param -----> [1, 2] (Heap)
  b -----> [1, 2] (Heap)
```

## Frame Objects

### 1. Stack Frame

```python
import inspect

def example():
    frame = inspect.currentframe()
    print(frame.f_locals)

example()
```

### 2. Frame Info

```python
def show_frame():
    frame = inspect.currentframe()
    print(f"Function: {frame.f_code.co_name}")
    print(f"Line: {frame.f_lineno}")
    
show_frame()
```

## Summary

### 1. Stack

- Fast, limited size
- Function frames
- Name bindings
- Auto management

### 2. Heap

- Slower, dynamic size
- All objects
- Manual/GC management
- Longer lifetime

---


## Runnable Example: `stack_vs_heap.py`

```python
"""
01_stack_vs_heap.py - Stack vs Heap Memory (Conceptual Foundation)
Topic #23: Memory and Namespace
"""

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("STACK VS HEAP MEMORY")
    print("=" * 70)

    print("""
    COMPUTER MEMORY (RAM) IS DIVIDED INTO:

    STACK                          HEAP
    - Organized (frames)          - Unorganized (flexible)
    - Automatic management        - Requires GC
    - Fixed size per frame        - Variable size allocations
    - Very fast                   - Slower
    - LIFO structure              - Random access
    - Function calls              - All Python objects
    - Local variable NAMES        - Everything is an object!

    KEY INSIGHT:
    Variable NAMES live on stack
    Variable OBJECTS live on heap
    """)

    # Simple example
    x = 42
    name = "Alice"
    numbers = [1, 2, 3]

    print(f"\nCreated: x={x}, name='{name}', numbers={numbers}")

    print("""
    MEMORY MODEL:

    STACK:                  HEAP:
    ┌──────────┐           ┌─────────────┐
    │ x    ────┼──────────→│ int: 42     │
    │ name ────┼──────────→│ str: "Alice"│
    │ numbers ─┼──────────→│ list: [...]│
    └──────────┘           └─────────────┘

    Stack holds NAMES (references)
    Heap holds OBJECTS (actual data)
    """)

    # Function call stack
    def outer():
        print("  → outer() called")
        inner()
        print("  ← outer() returns")

    def inner():
        print("    → inner() called")
        x = 100
        print(f"    x = {x}")
        print("    ← inner() returns")

    print("\nFunction call stack demonstration:")
    outer()

    print("""
    STACK FRAMES:

    Start:           [global]
    Call outer():    [outer] [global]
    Call inner():    [inner] [outer] [global]  ← Stack grows
    inner returns:   [outer] [global]
    outer returns:   [global]                  ← Stack shrinks

    Each function gets its own frame!
    """)

    print("\nKey takeaways:")
    print("1. Stack: Fast, automatic, organized")
    print("2. Heap: Flexible, requires GC, all objects")
    print("3. Names on stack point to objects on heap")
    print("4. Understanding this helps debug memory issues")

    print("\nSee exercises.py for practice!")
```


## Exercises

**Exercise 1.**
Write a script that creates 5 nested function calls (a calls b calls c calls d calls e). In function `e`, use `inspect.stack()` to print the entire call stack, showing each frame's function name and line number. Explain in comments which parts are on the stack vs the heap.

??? success "Solution to Exercise 1"
        ```python
        import inspect

        def a():
            b()

        def b():
            c()

        def c():
            d()

        def d():
            e()

        def e():
            # Stack frames are on the stack; the frame objects
            # and their local namespaces are Python objects on the heap
            print("Call stack (innermost first):")
            for info in inspect.stack():
                print(f"  {info.function}() at line {info.lineno}")

        a()
        ```

---

**Exercise 2.**
Demonstrate that objects outlive their creating frame: write a function `create_data()` that creates a list, stores a `weakref.ref` to it in a global variable, and returns the list. After the function returns, verify that the weak reference is still alive (because the caller holds a strong reference to the returned value).

??? success "Solution to Exercise 2"
        ```python
        import weakref

        global_ref = None

        def create_data():
            global global_ref
            data = list(range(1000))
            global_ref = weakref.ref(data)
            return data

        result = create_data()
        print(f"Weak ref alive: {global_ref() is not None}")  # True
        print(f"Same object: {global_ref() is result}")        # True

        del result
        print(f"After del: {global_ref() is not None}")        # False
        ```

---

**Exercise 3.**
Write a function that creates a local variable referencing a large list, then reassigns that variable to `None`. Use `tracemalloc` snapshots before and after the reassignment to show that the heap memory is freed even though the stack frame is still active.

??? success "Solution to Exercise 3"
        ```python
        import tracemalloc

        def free_in_scope():
            tracemalloc.start()
            snap1 = tracemalloc.take_snapshot()

            data = list(range(500_000))  # Allocate on heap

            snap2 = tracemalloc.take_snapshot()
            growth = snap2.compare_to(snap1, 'lineno')
            alloc = sum(s.size_diff for s in growth if s.size_diff > 0)
            print(f"After allocation: +{alloc / 1024:.1f} KB")

            data = None  # Free the heap object

            snap3 = tracemalloc.take_snapshot()
            shrink = snap3.compare_to(snap2, 'lineno')
            freed = sum(s.size_diff for s in shrink if s.size_diff < 0)
            print(f"After reassignment: {freed / 1024:.1f} KB freed")

            tracemalloc.stop()

        free_in_scope()
        ```

---
