# nonlocal and Mutation

클로저에서 외부 변수를 수정하는 방법입니다.

!!! tip "Mental Model"
    A closure can freely mutate a captured mutable object (like appending to a list), but it cannot rebind the name without `nonlocal`. Think of `nonlocal` as a permission slip that says "when I write `x = ...`, update the existing name in the enclosing scope instead of creating a new local one."

## Rebinding vs Mutation

### The Core Difference

```python
def outer():
    x = [1, 2, 3]
    
    def rebind():
        x = [4, 5, 6]  # Creates NEW local variable!
    
    def mutate():
        x.append(4)  # Modifies SAME object
    
    rebind()
    print(x)  # [1, 2, 3] — unchanged
    
    mutate()
    print(x)  # [1, 2, 3, 4] — modified

outer()
```

| Operation | What Happens | Works Without nonlocal? |
|-----------|--------------|------------------------|
| `x = value` | Creates new binding | ❌ No |
| `x.method()` | Mutates existing object | ✅ Yes |
| `x[i] = v` | Mutates existing object | ✅ Yes |

### Why?

- **Assignment** (`=`) creates a new local variable
- **Method calls** operate on the looked-up object

---

## The nonlocal Keyword

`nonlocal`은 내부 함수가 외부 변수를 **재바인딩**할 수 있게 합니다:

```python
def outer():
    count = 0
    
    def increment():
        nonlocal count  # Required for rebinding
        count += 1
        return count
    
    return increment

counter = increment()
print(counter())  # 1
print(counter())  # 2
```

### Without nonlocal — Error

```python
def outer():
    count = 0
    
    def increment():
        count += 1  # UnboundLocalError!
        return count
    
    return increment
```

`count += 1`은 `count = count + 1`이므로, assignment가 `count`를 로컬로 만들어버립니다.

---

## nonlocal Resolution

`nonlocal`은 가장 가까운 enclosing scope의 변수를 찾습니다:

```python
def level1():
    x = 1
    
    def level2():
        x = 2
        
        def level3():
            nonlocal x  # Modifies level2's x (closest)
            x = 3
        
        level3()
        print(f"level2: {x}")  # 3
    
    level2()
    print(f"level1: {x}")  # 1 (unchanged)

level1()
```

---

## Augmented Assignment Operators

### With Mutable Objects (Works)

```python
def outer():
    items = [1, 2, 3]
    
    def extend():
        items += [4, 5]  # Calls __iadd__, mutates in place
    
    extend()
    print(items)  # [1, 2, 3, 4, 5]

outer()
```

### With Immutable Objects (Fails)

```python
def outer():
    count = 0
    
    def increment():
        count += 1  # Rebinding! Error without nonlocal
    
    # increment()  # UnboundLocalError

outer()
```

---

## Cell Sharing

여러 내부 함수가 같은 cell을 공유합니다:

```python
def outer():
    x = 0
    
    def inc():
        nonlocal x
        x += 1
        return x
    
    def dec():
        nonlocal x
        x -= 1
        return x
    
    def get():
        return x
    
    return inc, dec, get

inc, dec, get = outer()

print(inc())  # 1
print(inc())  # 2
print(dec())  # 1
print(get())  # 1
```

### Verify Same Cell

```python
def outer():
    x = 10
    f1 = lambda: x
    f2 = lambda: x
    return f1, f2

a, b = outer()
print(a.__closure__[0] is b.__closure__[0])  # True — same cell
```

---

## Workarounds Without nonlocal

### Using Mutable Container

```python
def outer():
    count = [0]  # Mutable container
    
    def increment():
        count[0] += 1  # Mutation, not rebinding
        return count[0]
    
    return increment

counter = outer()
print(counter())  # 1
print(counter())  # 2
```

### Using Object Attribute

```python
def outer():
    class State:
        count = 0
    
    def increment():
        State.count += 1
        return State.count
    
    return increment
```

### Using Function Attribute

```python
def counter():
    def inner():
        inner.count += 1
        return inner.count
    inner.count = 0
    return inner

c = counter()
print(c())  # 1
print(c())  # 2
```

---

## Best Practices

### When to Use nonlocal

✅ Simple state management in closures:

```python
def make_counter(start=0):
    count = start
    
    def increment():
        nonlocal count
        count += 1
        return count
    
    return increment
```

### When to Avoid nonlocal

❌ Complex state → Use a class instead:

```python
# Instead of multiple nonlocal variables
class Counter:
    def __init__(self, start=0):
        self.count = start
    
    def increment(self):
        self.count += 1
        return self.count
```

---

## Summary

| Concept | Description |
|---------|-------------|
| Rebinding | `x = value` creates new variable; needs `nonlocal` |
| Mutation | `x.method()` modifies object; works without `nonlocal` |
| `nonlocal` | Allows rebinding of enclosing scope variable |
| Cell sharing | Multiple closures from same function share cells |
| Workaround | Use mutable container `[value]` if avoiding `nonlocal` |

---

## Runnable Example: `closure_mutable_state_example.py`

```python
"""
Closures with Mutable State - Using Free Variables for Stateful Computation
This tutorial demonstrates how closures can maintain mutable state
by capturing variables from their enclosing scope.
Run this file to see closures with state in action!
"""

if __name__ == "__main__":

    print("=" * 70)
    print("CLOSURES WITH MUTABLE STATE - EXAMPLES")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: Understanding Closure State
    # ============================================================================
    print("\n1. UNDERSTANDING CLOSURE STATE")
    print("-" * 70)

    print("\nFrom the previous closure tutorial, we learned:")
    print("- Closures capture variables from their enclosing scope")
    print("- These captured variables are called FREE VARIABLES")
    print("- Free variables are stored in the closure object")
    print("\nBut can we use mutable objects (lists, dicts) in closures?")
    print("YES! And this lets us build stateful functions!\n")

    # ============================================================================
    # EXAMPLE 2: Simple Closure - Constant Free Variable
    # ============================================================================
    print("\n2. SIMPLE CLOSURE - CONSTANT FREE VARIABLE")
    print("-" * 70)

    def make_multiplier(factor):
        """Create a function that multiplies by a factor."""
        def multiply(x):
            return x * factor
        return multiply

    times3 = make_multiplier(3)
    times5 = make_multiplier(5)

    print("\nDefined make_multiplier(factor)")
    print("Created: times3 = make_multiplier(3)")
    print("Created: times5 = make_multiplier(5)\n")

    print(f"times3(10) = {times3(10)}")
    print(f"times5(10) = {times5(10)}")

    print("\nThese closures captured 'factor' as a free variable")
    print("But factor is immutable (int), so it never changes")

    # ============================================================================
    # EXAMPLE 3: Closure with Mutable State - The Accumulator
    # ============================================================================
    print("\n3. CLOSURE WITH MUTABLE STATE - THE ACCUMULATOR")
    print("-" * 70)

    def make_accumulator():
        """
        Create a function that accumulates values.

        The accumulator function maintains its own total,
        which persists between calls!
        """
        total = 0  # This variable is captured by the closure

        def accumulate(value):
            nonlocal total  # Declare that we're using the outer 'total'
            total += value  # Modify the captured variable!
            return total

        return accumulate

    print("\nDefined make_accumulator()")
    print("Key: uses 'nonlocal total' to modify the captured variable\n")

    acc = make_accumulator()

    print("Created: acc = make_accumulator()\n")

    print("Calling acc() multiple times:")
    print(f"  acc(1) = {acc(1)}")
    print(f"  acc(2) = {acc(2)}")
    print(f"  acc(5) = {acc(5)}")
    print(f"  acc(3) = {acc(3)}")

    print("\nNOTICE: The total PERSISTS between calls!")
    print("- Each call modifies the same 'total' variable")
    print("- This is stateful behavior without a class!")

    # ============================================================================
    # EXAMPLE 4: Understanding 'nonlocal'
    # ============================================================================
    print("\n4. UNDERSTANDING 'nonlocal'")
    print("-" * 70)

    print("\nThe 'nonlocal' keyword is crucial for modifying captured variables!\n")

    print("Without 'nonlocal':")
    print("""
    def make_acc_broken():
        total = 0
        def accumulate(value):
            total += value  # ERROR! total is local, not the outer one!
            return total
        return accumulate
    """)

    print("\nWith 'nonlocal':")
    print("""
    def make_accumulator():
        total = 0
        def accumulate(value):
            nonlocal total  # OK! Use the outer total
            total += value  # Modifies the outer total
            return total
        return accumulate
    """)

    print("\nWITHOUT 'nonlocal':")
    print("- Python thinks 'total' is a NEW local variable")
    print("- 'total += value' tries to read total before assigning")
    print("- UnboundLocalError!")

    print("\nWITH 'nonlocal':")
    print("- Python knows 'total' refers to the outer variable")
    print("- 'total += value' modifies the captured variable")
    print("- State persists across calls!")

    # ============================================================================
    # EXAMPLE 5: Closure with Mutable Container - The Running Average
    # ============================================================================
    print("\n5. CLOSURE WITH MUTABLE STATE - RUNNING AVERAGE")
    print("-" * 70)

    def make_averager():
        """
        Create a function that computes running average.

        Each call appends to a list and computes the average.
        The list is a MUTABLE object captured by the closure.
        """
        series = []  # Mutable list captured by closure

        def averager(new_value):
            series.append(new_value)  # Modify the mutable list
            total = sum(series)
            return total / len(series)

        return averager

    print("\nDefined make_averager()")
    print("Uses a mutable list to store all values\n")

    avg = make_averager()

    print("Created: avg = make_averager()\n")

    print("Computing running average:")
    result1 = avg(10)
    print(f"  avg(10) = {result1}")
    print(f"    All values so far: [10]")
    print(f"    Average: 10 / 1 = {result1}")

    result2 = avg(11)
    print(f"\n  avg(11) = {result2}")
    print(f"    All values so far: [10, 11]")
    print(f"    Average: (10 + 11) / 2 = {result2}")

    result3 = avg(12)
    print(f"\n  avg(12) = {result3}")
    print(f"    All values so far: [10, 11, 12]")
    print(f"    Average: (10 + 11 + 12) / 3 = {result3}")

    print("\nKEY INSIGHT:")
    print("- The list 'series' is MUTABLE")
    print("- We don't need 'nonlocal' because we're not reassigning it")
    print("- We're just modifying its contents with append()")
    print("- The list PERSISTS between calls!")

    # ============================================================================
    # EXAMPLE 6: Inspecting Closure Objects
    # ============================================================================
    print("\n6. INSPECTING CLOSURE OBJECTS")
    print("-" * 70)

    print("\nWe can inspect the closure to see captured variables!\n")

    print("For avg = make_averager():\n")

    print(f"avg.__code__.co_varnames = {avg.__code__.co_varnames}")
    print("  ^ Local variables in averager() function")

    print(f"\navg.__code__.co_freevars = {avg.__code__.co_freevars}")
    print("  ^ Names of free variables (captured from outer scope)")

    print(f"\navg.__closure__ = {avg.__closure__}")
    print("  ^ Tuple of cell objects holding the free variables")

    print(f"\nNumber of cells: {len(avg.__closure__)}")
    print(f"Contents of the 'series' cell:")
    print(f"  avg.__closure__[0].cell_contents = {avg.__closure__[0].cell_contents}")

    print("\nBEFORE MAKING CALLS: series is empty")
    print(f"AFTER calling avg(10), avg(11), avg(12):")
    print(f"  series still contains: {avg.__closure__[0].cell_contents}")

    # ============================================================================
    # EXAMPLE 7: Multiple Closures - Independent State
    # ============================================================================
    print("\n7. MULTIPLE CLOSURES - INDEPENDENT STATE")
    print("-" * 70)

    avg1 = make_averager()
    avg2 = make_averager()

    print("\nCreated: avg1 = make_averager()")
    print("Created: avg2 = make_averager()\n")

    print("They have SEPARATE series lists!\n")

    print("avg1(10):", avg1(10))
    print("avg1(20):", avg1(20))

    print("\navg2(100):", avg2(100))
    print("avg2(200):", avg2(200))

    print("\nEach closure has its own state:")
    print(f"avg1's series: {avg1.__closure__[0].cell_contents}")
    print(f"avg2's series: {avg2.__closure__[0].cell_contents}")

    print("\nMULTIPLE INSTANCES:")
    print("- Each call to make_averager() creates NEW variables")
    print("- Each returned function captures its OWN series list")
    print("- State is independent!")

    # ============================================================================
    # EXAMPLE 8: Practical Example - Event Logger with State
    # ============================================================================
    print("\n8. PRACTICAL EXAMPLE - EVENT LOGGER")
    print("-" * 70)

    def make_event_logger(name):
        """
        Create a function that logs events with timestamps.

        The logger maintains a list of events.
        """
        events = []

        def log_event(message):
            import time
            timestamp = time.strftime("%H:%M:%S")
            event = f"[{timestamp}] {message}"
            events.append(event)
            print(f"{name}: {event}")
            return len(events)

        def get_events():
            return events.copy()

        log_event.get_events = get_events  # Attach method to function
        return log_event

    print("\nDefined make_event_logger(name)")
    print("This creates a logger that maintains state\n")

    logger1 = make_event_logger("APP")
    logger2 = make_event_logger("AUTH")

    print("Created: logger1 = make_event_logger('APP')")
    print("Created: logger2 = make_event_logger('AUTH')\n")

    logger1("System started")
    logger1("Processing request")
    logger2("User login attempt")
    logger1("Request completed")
    logger2("User logged in")

    print("\nAll events logged by logger1:")
    for event in logger1.get_events():
        print(f"  {event}")

    print("\nAll events logged by logger2:")
    for event in logger2.get_events():
        print(f"  {event}")

    print("\nSEPARATE STATE:")
    print("- Each logger has its own events list")
    print("- Loggers are independent")
    print("- State persists across calls")

    # ============================================================================
    # SUMMARY: Closures with Mutable State
    # ============================================================================
    print("\n" + "=" * 70)
    print("SUMMARY - CLOSURES WITH MUTABLE STATE")
    print("=" * 70)

    print("""
    IMMUTABLE FREE VARIABLES:
      - Captured at closure creation time
      - Can read them, but can't reassign without 'nonlocal'
      - Example: factor in make_multiplier()

    IMMUTABLE FREE VARIABLES WITH 'nonlocal':
      - Can reassign using 'nonlocal' keyword
      - Example: total in make_accumulator()

    MUTABLE FREE VARIABLES:
      - Lists, dicts, objects, etc.
      - Can modify contents (append, add keys, etc.)
      - No 'nonlocal' needed for modifications!
      - Only need 'nonlocal' if reassigning the variable

    WHEN TO USE CLOSURES VS CLASSES:

    Use closures for:
      - Simple functions with minimal state
      - Lightweight stateful callbacks
      - Higher-order functions

    Use classes for:
      - Multiple methods on the same state
      - Complex state management
      - When inheritance is useful
      - Public API (classes are more explicit)

    CLOSURES ARE POWERFUL:
      - Maintain state without classes
      - Create factory functions
      - Implement decorators
      - Enable functional programming style

    KEY POINTS:
    - Free variables enable closures to have state
    - 'nonlocal' allows reassigning captured variables
    - Each closure instance has its own captured variables
    - Mutable objects can be modified without 'nonlocal'
    - Inspecting __code__ and __closure__ shows what's captured
    """)
```

---

## Exercises


**Exercise 1.**
Write a closure `make_counter()` that returns three functions: `increment`, `decrement`, and `get_value`. The counter should start at 0. Use `nonlocal` to modify the shared state.

??? success "Solution to Exercise 1"

        ```python
        def make_counter():
            value = 0
            def increment():
                nonlocal value
                value += 1
            def decrement():
                nonlocal value
                value -= 1
            def get_value():
                return value
            return increment, decrement, get_value

        inc, dec, get = make_counter()
        inc(); inc(); inc()
        print(get())  # 3
        dec()
        print(get())  # 2
        ```

    All three functions share the same `value` variable from the enclosing scope, modified via `nonlocal`.

---

**Exercise 2.**
Explain why the following code raises `UnboundLocalError`. Fix it using `nonlocal`.

```python
def outer():
    count = 0
    def inner():
        count += 1
        return count
    return inner
```

??? success "Solution to Exercise 2"

    The assignment `count += 1` makes `count` a local variable in `inner`. Python detects this at compile time, so reading `count` before assignment raises `UnboundLocalError`.

        ```python
        def outer():
            count = 0
            def inner():
                nonlocal count
                count += 1
                return count
            return inner

        f = outer()
        print(f())  # 1
        print(f())  # 2
        ```

    `nonlocal count` tells Python that `count` refers to the variable in the enclosing scope, not a new local variable.

---

**Exercise 3.**
Write a closure `make_toggle()` that returns a function. Each call toggles between `True` and `False`, starting with `True` on the first call.

??? success "Solution to Exercise 3"

        ```python
        def make_toggle():
            state = False
            def toggle():
                nonlocal state
                state = not state
                return state
            return toggle

        t = make_toggle()
        print(t())  # True
        print(t())  # False
        print(t())  # True
        ```

    The state starts as `False` and flips on each call. The first call returns `True`.
