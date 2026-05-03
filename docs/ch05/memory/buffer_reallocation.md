# Buffer Reallocation

!!! tip "Mental Model"
    A Python list is like a row of seats in a theater. When you run out of seats, you cannot just add one -- you move everyone to a bigger row with extra empty seats. This over-allocation strategy means most `append` calls are instant (an empty seat is waiting), and the occasional move is amortized across many appends, giving O(1) average cost.

## List Growth

### 1. Dynamic Arrays

Lists grow dynamically:

```python
lst = []
for i in range(100):
    lst.append(i)
    # May trigger reallocation
```

### 2. Capacity

```python
import sys

lst = []
print(sys.getsizeof(lst))  # Initial

lst.append(1)
print(sys.getsizeof(lst))  # Grew

# Over-allocates for efficiency
```

## Growth Strategy

### 1. Exponential

```python
# CPython strategy:
# new_capacity = old_capacity + (old_capacity >> 3) + 6

# Example progression:
# 0 -> 4 -> 8 -> 16 -> 25 -> 35 -> ...
```

### 2. Amortized O(1)

```python
# Average append is O(1)
# Occasional reallocation is O(n)
# Amortized: O(1)

lst = []
for i in range(1000):
    lst.append(i)  # Fast on average
```

## Pre-allocation

### 1. If Known Size

```python
# Inefficient
lst = []
for i in range(1000):
    lst.append(i)

# Better: pre-allocate
lst = [0] * 1000
for i in range(1000):
    lst[i] = i
```

### 2. List Comprehension

```python
# Also pre-allocates
lst = [i for i in range(1000)]
```

## Memory Impact

### 1. Over-allocation

```python
import sys

lst = [1, 2, 3]
print(sys.getsizeof(lst))  # e.g., 80

# Has extra capacity
# Not just 3 items worth
```

### 2. Shrinking

```python
# Doesn't automatically shrink
lst = list(range(1000))
size1 = sys.getsizeof(lst)

del lst[100:]
size2 = sys.getsizeof(lst)

# size2 may equal size1
```

## Summary

### 1. Dynamic Growth

- Lists grow automatically
- Exponential strategy
- Over-allocates
- Amortized O(1) append

### 2. Optimization

- Pre-allocate when possible
- Use comprehensions
- Avoid many appends

---


## Runnable Example: `defensive_copying_pattern.py`

```python
"""
TUTORIAL: Defensive Copying Pattern in __init__

In this tutorial, you'll learn how to avoid one of Python's most insidious bugs:
ALIASING. When you accept a mutable object (like a list) as a parameter, you need
to be careful: if you assign it directly to an instance variable, you and the caller
share the SAME list. Any changes to it affects both!

The solution is DEFENSIVE COPYING: make a copy of mutable arguments in __init__.
This ensures your object owns its own data and can't be corrupted by external changes.

This is based on the Bus example from Fluent Python by Luciano Ramalho.
"""

import copy

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Defensive Copying Pattern")
    print("=" * 70)

    # ============ EXAMPLE 1: The Correct Bus Class (with defensive copying)
    print("\n# ============ EXAMPLE 1: The Correct Bus Class")
    print("Define a Bus class that makes defensive copies of the passenger list")
    print("so external changes can't corrupt our data:\n")


    class Bus:
        """A bus with its own copy of the passenger list"""

        def __init__(self, passengers=None):
            # WHY defensive copying? If passengers is provided, we DON'T assign it
            # directly. Instead, we create a NEW list with list(passengers).
            # This means our self.passengers is independent from the original list.
            if passengers is None:
                self.passengers = []
            else:
                # Make a defensive copy! This is the KEY difference.
                self.passengers = list(passengers)

        def pick(self, name):
            """Add a passenger to the bus"""
            self.passengers.append(name)

        def drop(self, name):
            """Remove a passenger from the bus"""
            self.passengers.remove(name)


    # Test 1: Create buses with initial passengers
    print("Creating bus1 with ['Alice', 'Bill', 'Claire', 'David']")
    bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
    print(f"bus1.passengers = {bus1.passengers}")

    print("\nCreating bus2 as a shallow copy of bus1 (copy.copy)")
    bus2 = copy.copy(bus1)
    print(f"bus2.passengers = {bus2.passengers}")

    print("\nCreating bus3 as a deep copy of bus1 (copy.deepcopy)")
    bus3 = copy.deepcopy(bus1)
    print(f"bus3.passengers = {bus3.passengers}")

    # Now drop a passenger from bus1
    print("\nDropping 'Bill' from bus1...")
    bus1.drop('Bill')
    print(f"bus1.passengers = {bus1.passengers}")

    # Check bus2 - it was a SHALLOW copy, so it shares the same passenger list
    print(f"bus2.passengers = {bus2.passengers}")
    print("-> bus2 also changed because shallow copy shares the list object!")

    # Check bus3 - it was a DEEP copy, so it has its own completely independent copy
    print(f"bus3.passengers = {bus3.passengers}")
    print("-> bus3 remains unchanged because deep copy made independent copies!")

    # ============ EXAMPLE 2: Why Defensive Copying Matters in __init__
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 2: Why Defensive Copying Matters in __init__")
    print("Demonstrate what happens WITHOUT defensive copying:\n")


    class UnsafeBus:
        """A bus that doesn't make defensive copies (ANTI-PATTERN)"""

        def __init__(self, passengers=None):
            # WRONG: Direct assignment creates an alias!
            # If passengers is a list, self.passengers now points to THE SAME list
            if passengers is None:
                self.passengers = []
            else:
                self.passengers = passengers  # ALIASING! Shared reference!

        def pick(self, name):
            self.passengers.append(name)

        def drop(self, name):
            self.passengers.remove(name)


    print("Creating a passenger list we'll reuse:")
    original_passengers = ['Alice', 'Bill', 'Claire']
    print(f"original_passengers = {original_passengers}")

    print("\nCreating unsafe_bus with this list...")
    unsafe_bus = UnsafeBus(original_passengers)
    print(f"unsafe_bus.passengers = {unsafe_bus.passengers}")

    print("\nNow drop 'Bill' from the bus...")
    unsafe_bus.drop('Bill')
    print(f"unsafe_bus.passengers = {unsafe_bus.passengers}")

    print("\nBUT LOOK - the original list was also modified!")
    print(f"original_passengers = {original_passengers}")
    print("-> This is the ALIASING BUG! Both variables point to the same list.")
    print("-> Modifying one affects the other - data corruption!")

    # ============ EXAMPLE 3: Comparing Safe vs Unsafe
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 3: Comparing Safe vs Unsafe")
    print("Side-by-side comparison of defensive vs non-defensive copying:\n")

    print("Scenario: We have a list of guests and create two buses")
    guests = ['Eve', 'Frank', 'Grace']
    print(f"guests = {guests}")

    print("\nSafe Bus (with defensive copying):")
    safe_bus = Bus(guests)
    print(f"safe_bus.passengers = {safe_bus.passengers}")
    safe_bus.drop('Frank')
    print(f"After dropping 'Frank': safe_bus.passengers = {safe_bus.passengers}")
    print(f"Original list unchanged: guests = {guests}")
    print("-> Our bus can't corrupt external data!")

    guests = ['Eve', 'Frank', 'Grace']  # Reset
    print("\nUnsafe Bus (without defensive copying):")
    unsafe_bus = UnsafeBus(guests)
    print(f"unsafe_bus.passengers = {unsafe_bus.passengers}")
    unsafe_bus.drop('Frank')
    print(f"After dropping 'Frank': unsafe_bus.passengers = {unsafe_bus.passengers}")
    print(f"Original list corrupted: guests = {guests}")
    print("-> The bus corrupted the external data!")

    # ============ EXAMPLE 4: Understanding What list() Does
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 4: Understanding What list() Does")
    print("The list() constructor creates a new list with the same elements:\n")

    original = [1, 2, 3]
    copy1 = list(original)

    print(f"original = {original}")
    print(f"copy1 = list(original) = {copy1}")
    print(f"copy1 == original: {copy1 == original}  (same contents)")
    print(f"copy1 is original: {copy1 is original}  (different objects)")

    print("\nModifying copy1 doesn't affect original:")
    copy1.append(4)
    print(f"After copy1.append(4):")
    print(f"original = {original}")
    print(f"copy1 = {copy1}")
    print("-> They're completely independent!")

    # ============ EXAMPLE 5: When to Use Defensive Copying
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 5: When to Use Defensive Copying")
    print("Best practices for defensive copying:\n")

    print("""
    RULE 1: If a parameter is a MUTABLE collection (list, dict, set),
            and you store it as an instance variable, make a copy.

    RULE 2: Use list(param) for lists, dict(param) for dicts, set(param) for sets.
            These are shallow copies - good enough for most cases.

    RULE 3: Only use copy.deepcopy() if your collections contain mutable objects
            that also need to be protected from external modification.

    WHY? Because Python objects are references. Without copying, you create
    an ALIAS - two variables pointing to the same object. Changes through
    one variable affect what the other sees.

    WHEN? Defensive copying is mainly for:
      - __init__ methods (protect your instance variables)
      - Public methods that accept mutable parameters
      - Any time you store a parameter as instance state

    NOT NEEDED for:
      - Immutable objects (strings, tuples, numbers)
      - When you process and discard the parameter (not storing it)
      - When aliasing is intentional and documented
    """)

    # ============ EXAMPLE 6: Defensive Copying with Different Collections
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 6: Defensive Copying with Different Collections")
    print("Different collection types need different copy approaches:\n")


    class Config:
        """Configuration class demonstrating defensive copying for different types"""

        def __init__(self, names=None, settings=None, allowed_tags=None):
            # Copy each mutable parameter appropriately
            self.names = list(names) if names is not None else []
            self.settings = dict(settings) if settings is not None else {}
            self.allowed_tags = set(allowed_tags) if allowed_tags is not None else set()


    print("Creating initial data:")
    names = ['Alice', 'Bob']
    settings = {'theme': 'dark', 'lang': 'en'}
    tags = {'python', 'tutorial'}

    config = Config(names, settings, tags)
    print(f"config.names = {config.names}")
    print(f"config.settings = {config.settings}")
    print(f"config.allowed_tags = {config.allowed_tags}")

    print("\nModifying original data:")
    names.append('Charlie')
    settings['theme'] = 'light'
    tags.add('advanced')

    print(f"names = {names}, config.names = {config.names} (unchanged)")
    print(f"settings = {settings}, config.settings = {config.settings} (unchanged)")
    print(f"tags = {tags}, config.allowed_tags = {config.allowed_tags} (unchanged)")
    print("-> All config data protected by defensive copying!")

    # ============ EXAMPLE 7: The Cost of Defensive Copying
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 7: The Cost of Defensive Copying")
    print("Defensive copying uses memory - but it's almost always worth it:\n")

    print("""
    MEMORY: Copying uses extra memory proportional to the data size
    SPEED:  list(param) is very fast - typically negligible overhead

    TRADE-OFF: A tiny bit of memory and CPU to prevent BUGS and DATA CORRUPTION
               This is almost always the right choice!

    EXCEPTION: In rare high-performance scenarios with huge lists where you
               KNOW aliasing is safe, you might skip defensive copying.
               But document it clearly!

    PRINCIPLE: Be DEFENSIVE. Assume users will modify their data.
               Protect your instance variables by copying mutable inputs.
    """)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    KEY TAKEAWAYS:

    1. ALIASING: In Python, assignment creates references, not copies.
       Multiple variables can point to the same mutable object.

    2. DEFENSIVE COPYING: In __init__, copy mutable parameters using:
       - list(param) for lists
       - dict(param) for dicts
       - set(param) for sets

    3. WHY: This prevents external code from corrupting your object's data
            through the original reference they passed in.

    4. COST: Minimal - it's a shallow copy, very fast for most cases.

    5. BEST PRACTICE: Always use defensive copying for mutable parameters
                      unless there's a documented reason not to.
    """)
```


## Exercises

**Exercise 1.**
Write a script that appends elements to an empty list one at a time (up to 100 elements) and records `sys.getsizeof(lst)` after each append. Print each step where the size changes (indicating a reallocation). Count the total number of reallocations.

??? success "Solution to Exercise 1"
        ```python
        import sys

        lst = []
        prev_size = sys.getsizeof(lst)
        reallocs = 0

        for i in range(100):
            lst.append(i)
            curr_size = sys.getsizeof(lst)
            if curr_size != prev_size:
                reallocs += 1
                print(f"  Realloc at len={len(lst)}: "
                      f"{prev_size} -> {curr_size} bytes")
                prev_size = curr_size

        print(f"\nTotal reallocations: {reallocs}")
        ```

---

**Exercise 2.**
Compare the total memory used (via `sys.getsizeof`) by three approaches to creating a list of 10,000 integers: (a) appending in a loop, (b) pre-allocating with `[0] * 10000` and assigning by index, and (c) using a list comprehension. Print the final size for each and explain any differences.

??? success "Solution to Exercise 2"
        ```python
        import sys

        # (a) Append loop
        lst_a = []
        for i in range(10_000):
            lst_a.append(i)
        size_a = sys.getsizeof(lst_a)

        # (b) Pre-allocate
        lst_b = [0] * 10_000
        for i in range(10_000):
            lst_b[i] = i
        size_b = sys.getsizeof(lst_b)

        # (c) List comprehension
        lst_c = [i for i in range(10_000)]
        size_c = sys.getsizeof(lst_c)

        print(f"Append loop:        {size_a:,} bytes")
        print(f"Pre-allocate:       {size_b:,} bytes")
        print(f"List comprehension: {size_c:,} bytes")

        # Append loop over-allocates; pre-allocate and
        # comprehension allocate exactly what is needed.
        ```

---

**Exercise 3.**
Demonstrate that deleting elements from a list does not shrink its allocated buffer. Create a list of 10,000 elements, record its size, delete all but the first 10 elements using `del lst[10:]`, and record the size again. Then show that creating a new list from the remaining elements (`list(lst)`) reclaims the wasted space.

??? success "Solution to Exercise 3"
        ```python
        import sys

        lst = list(range(10_000))
        size_full = sys.getsizeof(lst)
        print(f"Full list ({len(lst)} items): {size_full:,} bytes")

        del lst[10:]
        size_after_del = sys.getsizeof(lst)
        print(f"After del lst[10:] ({len(lst)} items): "
              f"{size_after_del:,} bytes")
        print(f"Buffer shrunk? {size_after_del < size_full}")

        # Reclaim space by creating a new list
        lst = list(lst)
        size_new = sys.getsizeof(lst)
        print(f"New list ({len(lst)} items): {size_new:,} bytes")
        print(f"Space reclaimed: {size_after_del - size_new:,} bytes")
        ```

---
