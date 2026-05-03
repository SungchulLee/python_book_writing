# Python vs C Memory

!!! tip "Mental Model"
    In C, a variable is a named box that directly holds a value -- an `int` lives right there on the stack. In Python, a variable is a name tag attached to an object that always lives on the heap. Python trades the raw speed of direct stack storage for safety and flexibility: no manual `malloc`/`free`, no dangling pointers, but more memory overhead per value.

## Memory Model

### 1. Python

Everything on heap:

```python
x = 42              # Heap
s = "hello"         # Heap
lst = [1, 2, 3]     # Heap
```

### 2. C

Variables on stack:

```c
int x = 42;         // Stack
char s[] = "hello"; // Stack
```

## Allocation

### 1. Python Auto

```python
# Automatic allocation
x = [1, 2, 3]

# Automatic deallocation
del x
# GC handles it
```

### 2. C Manual

```c
// Manual allocation
int *x = malloc(sizeof(int) * 3);

// Manual deallocation
free(x);  // Must remember!
```

## References

### 1. Python

All names are references:

```python
a = [1, 2, 3]
b = a           # Both point to same

b.append(4)
print(a)        # [1, 2, 3, 4]
```

### 2. C

Explicit pointers:

```c
int x = 42;
int *p = &x;    // Explicit pointer
int y = x;      // Copy value
```

## Type Safety

### 1. Python Dynamic

```python
x = 42
x = "hello"     # OK
x = [1, 2, 3]   # OK
```

### 2. C Static

```c
int x = 42;
x = "hello";    // Error!
```

## Memory Overhead

### 1. Python

Every object has overhead:

```python
import sys

x = 1
print(sys.getsizeof(x))  # ~28 bytes!
```

### 2. C

Minimal overhead:

```c
int x = 1;  // 4 bytes only
```

## Performance

### 1. Python

- Auto management
- More overhead
- Slower allocation

### 2. C

- Manual control
- Less overhead
- Faster allocation
- More error-prone

## Summary

| Aspect | Python | C |
|--------|--------|---|
| Location | Heap | Stack/Heap |
| Management | Auto | Manual |
| References | All refs | Explicit |
| Overhead | High | Low |
| Safety | Safe | Unsafe |

---


## Runnable Example: `mutable_default_arguments_gotcha.py`

```python
"""
TUTORIAL: Mutable Default Arguments Gotcha

This tutorial covers one of Python's most famous gotchas: using mutable objects
as default argument values. It seems innocent, but it's a CLASSIC BUG that catches
even experienced Python developers.

The Problem: Default arguments are evaluated ONCE when the function is defined,
not every time it's called. If that default is a mutable object, it becomes
SHARED across all function calls!

The Haunted Bus Example from Fluent Python demonstrates this perfectly.
We'll see how "ghost passengers" mysteriously appear due to this behavior.
"""

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Mutable Default Arguments Gotcha")
    print("=" * 70)

    # ============ EXAMPLE 1: The Infamous Mutable Default Bug
    print("\n# ============ EXAMPLE 1: The Infamous Mutable Default Bug")
    print("See how a mutable default creates shared state across instances:\n")


    class HauntedBus:
        """A bus where 'ghost passengers' mysteriously appear (ANTI-PATTERN!)"""

        def __init__(self, passengers=[]):
            # THIS IS THE BUG! passengers=[] is evaluated ONCE at function definition time.
            # Every instance that doesn't provide its own list SHARES this same default list!
            self.passengers = passengers

        def pick(self, name):
            """Add a passenger"""
            self.passengers.append(name)

        def drop(self, name):
            """Remove a passenger"""
            self.passengers.remove(name)


    print("Creating bus1 with explicit passenger list:")
    bus1 = HauntedBus(['Alice', 'Bill'])
    print(f"bus1.passengers = {bus1.passengers}")

    print("\nAdding 'Charlie' to bus1:")
    bus1.pick('Charlie')
    print(f"bus1.passengers = {bus1.passengers}")

    print("\nRemoving 'Alice' from bus1:")
    bus1.drop('Alice')
    print(f"bus1.passengers = {bus1.passengers}")

    print("\n" + "-" * 70)
    print("Now create bus2 WITHOUT providing a passenger list...")
    print("We expect an empty bus, right?")
    print("-" * 70)

    bus2 = HauntedBus()
    print(f"\nbus2.passengers = {bus2.passengers}")
    print("WAIT! Where did 'Carrie' come from? We just created bus2!")

    print("\nLet's add 'Carrie' to bus2:")
    bus2.pick('Carrie')
    print(f"bus2.passengers = {bus2.passengers}")

    print("\nNow create bus3 WITHOUT providing a passenger list...")
    bus3 = HauntedBus()
    print(f"bus3.passengers = {bus3.passengers}")
    print("BUS3 HAS THE SAME PASSENGERS AS BUS2!")

    print("\nLet's add 'Dave' to bus2:")
    bus2.pick('Dave')
    print(f"bus2.passengers = {bus2.passengers}")

    print("\nCheck bus3 again:")
    print(f"bus3.passengers = {bus3.passengers}")
    print("GHOST PASSENGERS! bus3 now has passengers we never added to it!")

    # ============ EXAMPLE 2: Understanding the Root Cause
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 2: Understanding the Root Cause")
    print("Why does this happen? Let's look at the function's __defaults__:\n")

    print("The __init__ method stores its default arguments in __defaults__:")
    print(f"HauntedBus.__init__.__defaults__ = {HauntedBus.__init__.__defaults__}")

    print("\nThis is a TUPLE containing the default value:")
    default_list = HauntedBus.__init__.__defaults__[0]
    print(f"default_list = {default_list}")

    print("\nNow check if bus2 and bus3 use the SAME list object:")
    print(f"bus2.passengers is default_list: {bus2.passengers is default_list}")
    print(f"bus3.passengers is default_list: {bus3.passengers is default_list}")
    print("bus2.passengers is bus3.passengers: {bus2.passengers is bus3.passengers}")

    print("""
    THIS IS THE KEY INSIGHT:
    - bus2.passengers, bus3.passengers, and the default list are ALL THE SAME OBJECT
    - When you modify bus2.passengers, you're modifying the default argument
    - This affects all future instances that use the default!
    """)

    # ============ EXAMPLE 3: The Correct Pattern (Using None)
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 3: The Correct Pattern (Using None)")
    print("The safe way to handle optional mutable arguments:\n")


    class SafeBus:
        """A bus that does it the RIGHT way!"""

        def __init__(self, passengers=None):
            # CORRECT: Use None as the default, then create a new list if needed
            # This way, each instance gets its OWN list
            if passengers is None:
                self.passengers = []
            else:
                self.passengers = list(passengers)  # Also make a defensive copy!

        def pick(self, name):
            self.passengers.append(name)

        def drop(self, name):
            self.passengers.remove(name)


    print("Creating safe_bus1 with explicit list:")
    safe_bus1 = SafeBus(['Alice', 'Bill'])
    print(f"safe_bus1.passengers = {safe_bus1.passengers}")
    safe_bus1.pick('Charlie')
    print(f"After pick: {safe_bus1.passengers}")

    print("\nCreating safe_bus2 without arguments:")
    safe_bus2 = SafeBus()
    print(f"safe_bus2.passengers = {safe_bus2.passengers}")
    print("-> Empty as expected!")

    print("\nAdding passengers to safe_bus2:")
    safe_bus2.pick('Diana')
    safe_bus2.pick('Eve')
    print(f"safe_bus2.passengers = {safe_bus2.passengers}")

    print("\nCreating safe_bus3 without arguments:")
    safe_bus3 = SafeBus()
    print(f"safe_bus3.passengers = {safe_bus3.passengers}")
    print("-> Empty! No ghost passengers!")

    print("\nModifying safe_bus2 doesn't affect safe_bus3:")
    safe_bus2.pick('Frank')
    print(f"safe_bus2.passengers = {safe_bus2.passengers}")
    print(f"safe_bus3.passengers = {safe_bus3.passengers}")
    print("-> They have completely independent lists!")

    # ============ EXAMPLE 4: Why This Happens (Python Internals)
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 4: Why This Happens (Python Internals)")
    print("Understanding when default arguments are evaluated:\n")

    print("""
    WHEN ARE DEFAULTS EVALUATED?

    In Python, default argument values are evaluated at FUNCTION DEFINITION TIME,
    not at CALL TIME.

    Example timeline:
    1. def func(x=[]):     <- [] is created and stored in func.__defaults__
    2. func()              <- Uses the list created in step 1
    3. func()              <- Still uses the SAME list from step 1
    4. func([1])           <- Creates and uses a different list

    This works fine for immutable defaults (strings, numbers, tuples):
    """)


    def count_calls(name="guest"):
        # Immutable default - no problem!
        print(f"Guest: {name}")


    count_calls()  # Uses default "guest"
    count_calls()  # Uses default "guest" again - no shared state
    count_calls("Alice")  # Uses provided value


    print("\nBut it's DANGEROUS for mutable defaults:")


    def add_item_bad(item, items=[]):
        # DANGER: items=[] is created once and shared!
        items.append(item)
        return items


    print("Calling add_item_bad with 'apple':")
    result1 = add_item_bad('apple')
    print(f"Result: {result1}")

    print("\nCalling add_item_bad with 'banana' (new call):")
    result2 = add_item_bad('banana')
    print(f"Result: {result2}")
    print("BOTH ITEMS THERE! The list was shared!")

    # ============ EXAMPLE 5: Common Mutable Types as Defaults
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 5: Common Mutable Types as Defaults")
    print("All these are dangerous as default arguments:\n")

    print("""
    DANGEROUS DEFAULTS:
      - list:  def func(items=[]):           NEVER DO THIS!
      - dict:  def func(config={}):          NEVER DO THIS!
      - set:   def func(seen=set()):         NEVER DO THIS!

    WHY? Because each parameter shares the same object across all calls.

    SAFE PATTERN: Use None, then create a new object if needed:
      - list:  if items is None: items = []
      - dict:  if config is None: config = {}
      - set:   if seen is None: seen = set()

    IMMUTABLE DEFAULTS (SAFE):
      - tuple: def func(coords=(0, 0)):      SAFE
      - str:   def func(name=""):            SAFE
      - int:   def func(count=0):            SAFE
      - None:  def func(value=None):         SAFE
    """)

    # ============ EXAMPLE 6: Real-World Examples of the Bug
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 6: Real-World Examples of the Bug")
    print("Places where this bug commonly appears:\n")


    # BUGGY VERSION
    class BuggyCache:
        """Cache implementation with mutable default bug"""

        def __init__(self, initial_data={}):
            # BUG: This dict is shared across all instances!
            self.data = initial_data

        def add(self, key, value):
            self.data[key] = value

        def show(self):
            return self.data


    print("Creating cache1 and adding data:")
    cache1 = BuggyCache()
    cache1.add('user_1', 'Alice')
    print(f"cache1.data = {cache1.show()}")

    print("\nCreating cache2 (new instance):")
    cache2 = BuggyCache()
    print(f"cache2.data = {cache2.show()}")
    print("-> cache2 has user_1 from cache1! The dict was shared!")

    print("\nAdding to cache2:")
    cache2.add('user_2', 'Bob')
    print(f"cache2.data = {cache2.show()}")

    print("\nChecking cache1 again:")
    print(f"cache1.data = {cache1.show()}")
    print("-> cache1 now has user_2 added by cache2! Contaminated!")

    # Now the CORRECT version
    print("\n" + "-" * 70)
    print("Corrected version:")
    print("-" * 70)


    class CorrectCache:
        """Cache implementation done RIGHT"""

        def __init__(self, initial_data=None):
            if initial_data is None:
                self.data = {}
            else:
                self.data = dict(initial_data)  # Defensive copy!

        def add(self, key, value):
            self.data[key] = value

        def show(self):
            return self.data


    print("\nCreating correct_cache1 and adding data:")
    correct_cache1 = CorrectCache()
    correct_cache1.add('user_1', 'Alice')
    print(f"correct_cache1.data = {correct_cache1.show()}")

    print("\nCreating correct_cache2 (new instance):")
    correct_cache2 = CorrectCache()
    print(f"correct_cache2.data = {correct_cache2.show()}")
    print("-> correct_cache2 is empty! Separate instance!")

    print("\nAdding to correct_cache2:")
    correct_cache2.add('user_2', 'Bob')
    print(f"correct_cache2.data = {correct_cache2.show()}")

    print("\nChecking correct_cache1 again:")
    print(f"correct_cache1.data = {correct_cache1.show()}")
    print("-> correct_cache1 still only has user_1! No contamination!")

    # ============ EXAMPLE 7: Detecting the Gotcha in Your Code
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 7: Detecting the Gotcha in Your Code")
    print("How to identify if you have this bug:\n")

    print("""
    RED FLAGS - Look for these patterns:

    1. def func(items=[]):
       def func(config={}):
       def func(data=set()):
       -> Mutable defaults - DANGER!

    2. Class attributes that are mutable and modified:
       def method(self, items=[]):
       -> Especially in methods called multiple times

    3. Behavior that seems wrong:
       "Why does my cache have data from a different instance?"
       "Why are passengers appearing without being added?"
       "Why is my list growing between function calls?"
       -> Could be the mutable default gotcha!

    HOW TO CHECK:
       print(function.__defaults__)
       -> Look for mutable objects (lists, dicts, sets)

    HOW TO FIX:
       1. Use None as the default
       2. Create new mutable objects when None is passed
       3. Optionally make defensive copies
    """)

    # ============ EXAMPLE 8: Mutable Defaults in Practice
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 8: Mutable Defaults in Practice")
    print("Best practices summary:\n")


    def process_data_wrong(items=[]):
        """WRONG: Mutable default"""
        items.append('processed')
        return items


    def process_data_right(items=None):
        """RIGHT: Using None"""
        if items is None:
            items = []
        items.append('processed')
        return items


    print("Calling process_data_wrong multiple times:")
    print(f"Call 1: {process_data_wrong()}")
    print(f"Call 2: {process_data_wrong()}")
    print(f"Call 3: {process_data_wrong()}")
    print("-> List grows each time! SHARED STATE!")

    print("\nCalling process_data_right multiple times:")
    print(f"Call 1: {process_data_right()}")
    print(f"Call 2: {process_data_right()}")
    print(f"Call 3: {process_data_right()}")
    print("-> Fresh list each time! NO SHARED STATE!")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    KEY TAKEAWAYS:

    1. DEFAULT ARGS ARE EVALUATED AT DEFINITION TIME
       Default values are created once when the function is defined,
       then reused for every call. This is a feature for immutables,
       a bug for mutables.

    2. NEVER USE MUTABLE DEFAULTS
       - WRONG: def __init__(self, items=[]):
       - WRONG: def __init__(self, config={}):
       - WRONG: def method(self, data=set()):

    3. USE NONE INSTEAD
       - RIGHT: def __init__(self, items=None):
       - Then: if items is None: items = []

    4. WHY THIS MATTERS
       - Bug is hard to spot (looks innocent!)
       - Causes shared state across instances
       - Data corruption and mysterious bugs
       - One of Python's most famous gotchas

    5. THE RULE
       "If your default value is mutable, you're doing it wrong!"
    """)
```


## Exercises

**Exercise 1.**
Write a script that compares the memory overhead of storing 1,000 integers in Python vs the theoretical cost in C. For Python, sum `sys.getsizeof(i)` for each integer plus the container overhead. For C, compute `1000 * 4` bytes (assuming 4-byte `int`). Print both values and the overhead ratio.

??? success "Solution to Exercise 1"
        ```python
        import sys

        n = 1_000
        python_item_bytes = sum(sys.getsizeof(i) for i in range(n))
        python_container = sys.getsizeof(list(range(n)))
        python_total = python_item_bytes + python_container

        c_total = n * 4  # 4 bytes per int in C

        print(f"Python total: {python_total:,} bytes")
        print(f"C total:      {c_total:,} bytes")
        print(f"Overhead ratio: {python_total / c_total:.1f}x")
        ```

---

**Exercise 2.**
Demonstrate Python's automatic memory management by writing a function that creates a large list inside a local scope, returns only a summary (e.g., the sum), and show using `tracemalloc` that the memory is freed after the function returns and `gc.collect()` is called.

??? success "Solution to Exercise 2"
        ```python
        import tracemalloc
        import gc

        def compute_sum(n):
            data = list(range(n))
            return sum(data)

        tracemalloc.start()
        snap1 = tracemalloc.take_snapshot()

        result = compute_sum(500_000)

        gc.collect()
        snap2 = tracemalloc.take_snapshot()

        diff = snap2.compare_to(snap1, 'lineno')
        total_change = sum(s.size_diff for s in diff)

        print(f"Result: {result}")
        print(f"Memory change after function return: "
              f"{total_change / 1024:.1f} KB")
        print("Memory was freed (small or negative change)")
        tracemalloc.stop()
        ```

---

**Exercise 3.**
Compare `array.array('i', ...)` vs a regular Python list for storing 100,000 integers. Print `sys.getsizeof()` for both containers and compute the per-element cost for each. Show the memory savings as a percentage.

??? success "Solution to Exercise 3"
        ```python
        import sys
        import array

        n = 100_000

        lst = list(range(n))
        arr = array.array('i', range(n))

        lst_size = sys.getsizeof(lst)
        arr_size = sys.getsizeof(arr)

        lst_per_elem = lst_size / n
        arr_per_elem = arr_size / n

        savings = (1 - arr_size / lst_size) * 100

        print(f"List:  {lst_size:>10,} bytes ({lst_per_elem:.1f} bytes/elem)")
        print(f"Array: {arr_size:>10,} bytes ({arr_per_elem:.1f} bytes/elem)")
        print(f"Savings: {savings:.1f}%")
        ```

---
