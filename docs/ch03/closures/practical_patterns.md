# Practical Patterns

클로저의 실용적인 활용 패턴과 디버깅 방법입니다.

!!! tip "Mental Model"
    Closures are lightweight alternatives to classes when you need a function bundled with a small amount of private state. Factories produce customized functions, decorators wrap behavior around existing functions, and callback registries remember context. If you find yourself writing a class with only `__init__` and one method, a closure is usually simpler.

## Factory Functions

### Basic Factory

```python
def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

### Configuration Factory

```python
def make_formatter(prefix, suffix=""):
    def format(value):
        return f"{prefix}{value}{suffix}"
    return format

currency = make_formatter("$", " USD")
percent = make_formatter("", "%")

print(currency(100))  # \$100 USD
print(percent(75))    # 75%
```

### Validator Factory

```python
def make_validator(min_val, max_val):
    def validate(value):
        if min_val <= value <= max_val:
            return True
        raise ValueError(f"Value must be between {min_val} and {max_val}")
    return validate

validate_age = make_validator(0, 150)
validate_percent = make_validator(0, 100)
```

---

## Decorators with State

### Call Counter

```python
def count_calls(func):
    count = 0
    
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"Call #{count}")
        return func(*args, **kwargs)
    
    wrapper.get_count = lambda: count
    return wrapper

@count_calls
def greet(name):
    return f"Hello, {name}!"

greet("Alice")  # Call #1
greet("Bob")    # Call #2
print(greet.get_count())  # 2
```

### Memoization

```python
def memoize(func):
    cache = {}
    
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    wrapper.cache = cache
    wrapper.clear = lambda: cache.clear()
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(100))  # Fast!
```

### Rate Limiter

```python
import time

def rate_limit(max_calls, period):
    calls = []
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls
            while calls and calls[0] < now - period:
                calls.pop(0)
            
            if len(calls) >= max_calls:
                raise Exception("Rate limit exceeded")
            
            calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=3, period=60)
def api_call():
    return "Response"
```

---

## functools.partial

기존 함수의 인자를 고정합니다:

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125
```

### partial vs Closure

```python
# Using closure
def make_power(exp):
    return lambda x: x ** exp

# Using partial
from functools import partial
def power(x, exp):
    return x ** exp

square_closure = make_power(2)
square_partial = partial(power, exp=2)

# Both work the same
print(square_closure(5))  # 25
print(square_partial(5))  # 25
```

| Approach | Pros | Cons |
|----------|------|------|
| Closure | Full control, custom logic | More verbose |
| `partial` | Concise, preserves metadata | Only fixes arguments |

---

## Callback Patterns

### Event Handler Factory

```python
def make_handler(event_name, callback):
    def handler(data):
        print(f"[{event_name}] Processing...")
        return callback(data)
    return handler

def process_click(data):
    return f"Clicked at {data['x']}, {data['y']}"

click_handler = make_handler("CLICK", process_click)
print(click_handler({'x': 100, 'y': 200}))
```

### Retry Logic

```python
import time

def with_retry(max_attempts, delay):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

@with_retry(max_attempts=3, delay=1)
def unstable_api_call():
    # Might fail
    pass
```

---

## Debugging Tools

### Inspect Closure Contents

```python
def outer():
    x = 10
    y = "hello"
    return lambda: (x, y)

f = outer()

# View closure
print(f.__closure__)  # (<cell ...>, <cell ...>)

# View free variable names
print(f.__code__.co_freevars)  # ('x', 'y')

# View cell contents
for var, cell in zip(f.__code__.co_freevars, f.__closure__):
    print(f"{var} = {cell.cell_contents}")
# x = 10
# y = hello
```

### Debug Helper Function

```python
def inspect_closure(func):
    """Print closure details for debugging."""
    print(f"Function: {func.__name__}")
    
    if func.__closure__ is None:
        print("  No closure")
        return
    
    freevars = func.__code__.co_freevars
    for var, cell in zip(freevars, func.__closure__):
        print(f"  {var} = {cell.cell_contents!r}")

# Usage
def make_adder(n):
    return lambda x: x + n

add5 = make_adder(5)
inspect_closure(add5)
# Function: <lambda>
#   n = 5
```

---

## Memory Considerations

### Problem: Large Captures

```python
# Bad: captures entire large_data
def make_handler():
    large_data = [0] * 1_000_000
    
    def handler():
        return len(large_data)  # Only needs length
    
    return handler  # Keeps 1M integers alive!
```

### Solution: Capture Only What's Needed

```python
# Good: captures only the length
def make_handler():
    large_data = [0] * 1_000_000
    data_len = len(large_data)
    
    def handler():
        return data_len
    
    return handler  # large_data can be garbage collected
```

### Avoid Circular References

```python
# Potential issue
def outer():
    x = []
    def inner():
        return x
    x.append(inner)  # Cycle: inner → x → inner
    return inner

# Better: use weakref if needed
import weakref

def outer():
    x = []
    def inner():
        return x
    # Don't create cycles, or use weak references
    return inner
```

---

## Summary

| Pattern | Use Case | Key Technique |
|---------|----------|---------------|
| Factory | Create configured functions | Return inner function |
| Decorator | Add behavior to functions | `nonlocal` for state |
| `partial` | Fix function arguments | `functools.partial` |
| Callback | Event handling | Capture context |
| Memoization | Cache results | Dict in closure |

**Debugging Checklist:**

1. `func.__closure__` — Cell objects
2. `func.__code__.co_freevars` — Variable names
3. `cell.cell_contents` — Actual values

---

## Runnable Example: `closure_vs_class_comparison.py`

```python
"""
Closures vs Classes - Comparing Two Approaches to Stateful Objects
This tutorial compares implementing the same functionality using
closures and classes, showing when to use each approach.
Run this file to see the comparison in action!
"""

if __name__ == "__main__":

    print("=" * 70)
    print("CLOSURES VS CLASSES - COMPARISON")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: Understanding the Problem
    # ============================================================================
    print("\n1. THE PROBLEM - HOW TO MAINTAIN STATE?")
    print("-" * 70)

    print("""
    We want to compute a running average of numbers.

    Each call should:
    - Accept a new number
    - Remember all previous numbers
    - Return the average of all numbers seen so far

    We can solve this two ways:
    1. Using a CLOSURE with captured mutable state
    2. Using a CLASS with instance variables

    Let's compare both approaches!
    """)

    # ============================================================================
    # EXAMPLE 2: The Closure Approach
    # ============================================================================
    print("\n2. THE CLOSURE APPROACH")
    print("-" * 70)

    def make_averager_closure():
        """
        Factory function that returns a closure.

        The returned function captures a list from the enclosing scope.
        """
        series = []  # Captured by the closure

        def averager(new_value):
            series.append(new_value)
            total = sum(series)
            return total / len(series)

        return averager

    print("\nDefined make_averager_closure():\n")

    print("""
    def make_averager_closure():
        series = []  # Captured variable

        def averager(new_value):
            series.append(new_value)
            total = sum(series)
            return total / len(series)

        return averager
    """)

    print("How it works:")
    print("1. make_averager_closure() creates a new 'series' list")
    print("2. It returns the inner 'averager' function")
    print("3. averager captures 'series' in its closure")
    print("4. Each call to averager modifies the captured list")
    print("5. State persists between calls!\n")

    avg_closure = make_averager_closure()
    print("Created: avg_closure = make_averager_closure()\n")

    print("Using the closure:")
    print(f"  avg_closure(10) = {avg_closure(10)}")
    print(f"  avg_closure(11) = {avg_closure(11)}")
    print(f"  avg_closure(12) = {avg_closure(12)}")

    # ============================================================================
    # EXAMPLE 3: The Class Approach
    # ============================================================================
    print("\n3. THE CLASS APPROACH")
    print("-" * 70)

    class Averager:
        """
        A class to compute running average.

        Uses an instance variable to maintain state.
        """

        def __init__(self):
            """Initialize with an empty series list."""
            self.series = []

        def __call__(self, new_value):
            """
            Make instances callable using __call__.

            This allows instances to be used like functions!
            """
            self.series.append(new_value)
            total = sum(self.series)
            return total / len(self.series)

    print("\nDefined Averager class:\n")

    print("""
    class Averager:
        def __init__(self):
            self.series = []

        def __call__(self, new_value):
            self.series.append(new_value)
            total = sum(self.series)
            return total / len(self.series)
    """)

    print("How it works:")
    print("1. __init__ creates an empty series list as instance variable")
    print("2. __call__ makes instances callable like functions")
    print("3. Each call modifies self.series")
    print("4. State persists between calls!\n")

    avg_class = Averager()
    print("Created: avg_class = Averager()\n")

    print("Using the instance (called like a function):")
    print(f"  avg_class(10) = {avg_class(10)}")
    print(f"  avg_class(11) = {avg_class(11)}")
    print(f"  avg_class(12) = {avg_class(12)}")

    # ============================================================================
    # EXAMPLE 4: They Do the Same Thing
    # ============================================================================
    print("\n4. THEY PRODUCE THE SAME RESULTS")
    print("-" * 70)

    print("\nBoth approaches compute the exact same average!\n")

    avg_c = make_averager_closure()
    avg_o = Averager()

    values = [10, 11, 12]

    print("Using closure approach:")
    closure_results = []
    for val in values:
        result = avg_c(val)
        closure_results.append(result)
        print(f"  {val} -> {result}")

    print("\nUsing class approach:")
    class_results = []
    for val in values:
        result = avg_o(val)
        class_results.append(result)
        print(f"  {val} -> {result}")

    print(f"\nResults match: {closure_results == class_results}")

    # ============================================================================
    # EXAMPLE 5: Differences in Syntax
    # ============================================================================
    print("\n5. DIFFERENCES IN SYNTAX AND USAGE")
    print("-" * 70)

    print("""
    CLOSURE:
      avg = make_averager_closure()
      result = avg(10)  # Function call

    CLASS:
      avg = Averager()
      result = avg(10)  # Also works with __call__

    At the call site, they look the same!
    But the implementation is different.
    """)

    # ============================================================================
    # EXAMPLE 6: Accessing State
    # ============================================================================
    print("\n6. ACCESSING AND INSPECTING STATE")
    print("-" * 70)

    avg_c = make_averager_closure()
    avg_o = Averager()

    # Make some calls
    for val in [10, 11, 12]:
        avg_c(val)
        avg_o(val)

    print("Accessing state from CLOSURE:\n")

    print("Direct access: NOT POSSIBLE")
    print("  avg_c.series -> AttributeError!")
    print("  You can't directly access captured variables\n")

    print("But we can inspect the closure:")
    print(f"  avg_c.__closure__ = {avg_c.__closure__}")
    print(f"  avg_c.__closure__[0].cell_contents = {avg_c.__closure__[0].cell_contents}\n")

    print("Accessing state from CLASS:\n")

    print("Direct access: POSSIBLE!")
    print(f"  avg_o.series = {avg_o.series}")
    print(f"  You can read and modify instance variables directly!\n")

    print("WHY THIS MATTERS:")
    print("- Class state is directly accessible and inspectable")
    print("- Closure state is hidden (encapsulation)")
    print("- For debugging, classes are easier to work with")

    # ============================================================================
    # EXAMPLE 7: Adding Methods
    # ============================================================================
    print("\n7. ADDING MORE METHODS")
    print("-" * 70)

    print("\nWhat if we want to add a method to get all values?\n")

    print("CLOSURE APPROACH:")
    print("Need to return multiple functions or attach methods:\n")

    def make_averager_extended():
        """Extended closure with multiple operations."""
        series = []

        def averager(new_value):
            series.append(new_value)
            total = sum(series)
            return total / len(series)

        def get_series():
            """Get a copy of all values."""
            return series.copy()

        # Attach method to function
        averager.get_series = get_series
        return averager

    avg_ext = make_averager_extended()
    print(f"avg_ext(10) = {avg_ext(10)}")
    print(f"avg_ext(11) = {avg_ext(11)}")
    print(f"avg_ext.get_series() = {avg_ext.get_series()}\n")

    print("CLASS APPROACH:")
    print("Just add another method:\n")

    class AveragerExtended:
        """Extended class with multiple methods."""

        def __init__(self):
            self.series = []

        def __call__(self, new_value):
            self.series.append(new_value)
            total = sum(self.series)
            return total / len(self.series)

        def get_series(self):
            """Get a copy of all values."""
            return self.series.copy()

    avg_ext = AveragerExtended()
    print(f"avg_ext(10) = {avg_ext(10)}")
    print(f"avg_ext(11) = {avg_ext(11)}")
    print(f"avg_ext.get_series() = {avg_ext.get_series()}\n")

    print("COMPARISON:")
    print("- Closure: Awkward to add multiple operations")
    print("- Class: Natural way to add methods")

    # ============================================================================
    # EXAMPLE 8: When to Use Each Approach
    # ============================================================================
    print("\n8. WHEN TO USE CLOSURES VS CLASSES")
    print("-" * 70)

    print("""
    USE CLOSURES WHEN:
    ✓ The object has ONE main operation (is essentially a function)
    ✓ State is simple and minimal
    ✓ You want to hide internal state (encapsulation)
    ✓ The function is returned from a factory (higher-order functions)
    ✓ You're implementing decorators
    ✓ You want a lightweight, minimal memory footprint

    Examples:
      - Running average calculator
      - Event listener callback
      - Decorator functions
      - Filter/transform functions

    USE CLASSES WHEN:
    ✓ The object has MULTIPLE methods
    ✓ State is complex and needs multiple operations
    ✓ You need to inherit from other classes
    ✓ You want a clear, explicit public API
    ✓ You need to introspect the object
    ✓ Other developers need to understand the code quickly

    Examples:
      - Bank account (deposit, withdraw, balance, etc.)
      - File reader (read, seek, tell, close)
      - Request handler (validate, process, respond)
      - Game character (move, attack, defend, heal)

    HYBRID APPROACH:
    Some objects use both:
      - Class with __call__ makes it callable like a function
      - But it has multiple methods for different operations
      - Best of both worlds!
    """)

    # ============================================================================
    # EXAMPLE 9: Readability and Maintenance
    # ============================================================================
    print("\n9. READABILITY AND MAINTENANCE")
    print("-" * 70)

    print("""
    CLOSURE READABILITY:
    - Compact, minimal code
    - Good for simple cases
    - Harder to debug (hidden state)
    - Hard to introspect

    CLASS READABILITY:
    - More explicit, self-documenting
    - Clear what methods are available
    - Easy to debug (visible state)
    - Easy to introspect and understand
    - Familiar to most programmers

    QUOTE FROM PEP 20 (Zen of Python):
    "Explicit is better than implicit."

    Classes are usually more explicit!
    """)

    # ============================================================================
    # EXAMPLE 10: Performance Comparison
    # ============================================================================
    print("\n10. PERFORMANCE COMPARISON")
    print("-" * 70)

    import timeit

    # Closure version
    def make_avg_c():
        series = []
        def avg(val):
            series.append(val)
            return sum(series) / len(series)
        return avg

    # Class version
    class AvgClass:
        def __init__(self):
            self.series = []
        def __call__(self, val):
            self.series.append(val)
            return sum(self.series) / len(self.series)

    avg_c = make_avg_c()
    avg_o = AvgClass()

    print("\nPerformance test (100,000 calls with value 42):\n")

    closure_time = timeit.timeit(lambda: avg_c(42), number=100000)
    print(f"Closure approach: {closure_time:.6f} seconds")

    class_time = timeit.timeit(lambda: avg_o(42), number=100000)
    print(f"Class approach:   {class_time:.6f} seconds")

    print(f"\nDifference: {abs(closure_time - class_time):.6f} seconds")
    print("(Difference is negligible for most applications)")

    print("\nCONCLUSION:")
    print("- Performance is essentially the same")
    print("- Choose based on design, not performance")
    print("- Readability matters more than micro-optimizations")

    # ============================================================================
    # SUMMARY: Making the Choice
    # ============================================================================
    print("\n" + "=" * 70)
    print("SUMMARY - CHOOSING BETWEEN CLOSURES AND CLASSES")
    print("=" * 70)

    print("""
    DECISION FLOWCHART:

    1. Does the object have only ONE callable operation?
       -> Use closure (simpler, less code)

    2. Does the object have MULTIPLE methods?
       -> Use class (clearer, more maintainable)

    3. Is state complex or needs introspection?
       -> Use class (easier to debug)

    4. Is this a factory function returning callables?
       -> Use closure (natural pattern)

    5. Is this a decorator?
       -> Use closure (standard pattern)

    6. Do you need inheritance?
       -> Use class (required)

    DEFAULT RECOMMENDATION:
    - Start with a class for clarity
    - Use closures only when the closure approach is clearly better
    - Don't over-engineer simple cases with classes
    - Don't hide complexity in closures

    PYTHONIC APPROACH:
    "Explicit is better than implicit." - Zen of Python

    Classes make intent explicit.
    Classes are the default choice for most scenarios.
    Use closures for specific patterns where they shine:
      - Decorators
      - Factory functions
      - Event handlers
      - Simple callbacks

    BOTH ARE VALID:
    There's no single "right" answer.
    Choose based on:
      - Clarity and readability
      - Maintenance considerations
      - Team preferences
      - Specific use case requirements

    The best code is the code that's easiest to understand,
    maintain, and modify by your team!
    """)
```

---

## Exercises


**Exercise 1.**
Write a memoization closure `make_memoized(func)` that caches results of a single-argument function. The closure should store results in a dictionary and return cached values for repeated arguments.

??? success "Solution to Exercise 1"

        ```python
        def make_memoized(func):
            cache = {}
            def wrapper(arg):
                if arg not in cache:
                    cache[arg] = func(arg)
                return cache[arg]
            return wrapper

        @make_memoized
        def square(x):
            print(f"Computing {x}^2")
            return x ** 2

        print(square(4))  # Computing 4^2 -> 16
        print(square(4))  # 16 (cached, no print)
        print(square(5))  # Computing 5^2 -> 25
        ```

    The closure captures `cache` (a dict) and `func`. Results are stored on first call and returned from cache on subsequent calls.

---

**Exercise 2.**
Write a closure `make_rate_limiter(max_calls, period)` that returns a function wrapper. The wrapper should allow at most `max_calls` calls within `period` seconds, raising a `RuntimeError` if the limit is exceeded. Use `time.time()` and a list to track call timestamps.

??? success "Solution to Exercise 2"

        ```python
        import time

        def make_rate_limiter(max_calls, period):
            timestamps = []
            def wrapper(func):
                def limited(*args, **kwargs):
                    now = time.time()
                    timestamps[:] = [t for t in timestamps if now - t < period]
                    if len(timestamps) >= max_calls:
                        raise RuntimeError("Rate limit exceeded")
                    timestamps.append(now)
                    return func(*args, **kwargs)
                return limited
            return wrapper

        @make_rate_limiter(3, 1.0)
        def api_call():
            return "success"

        print(api_call())  # success
        print(api_call())  # success
        print(api_call())  # success
        # api_call()       # RuntimeError: Rate limit exceeded
        ```

    The closure maintains a list of timestamps. Old timestamps outside the period are removed before each check.

---

**Exercise 3.**
Write a closure `make_validator(min_val, max_val)` that returns a function. The returned function takes a value and returns `True` if it is between `min_val` and `max_val` (inclusive), `False` otherwise.

??? success "Solution to Exercise 3"

        ```python
        def make_validator(min_val, max_val):
            def validate(value):
                return min_val <= value <= max_val
            return validate

        is_valid_age = make_validator(0, 120)
        print(is_valid_age(25))   # True
        print(is_valid_age(-5))   # False
        print(is_valid_age(150))  # False
        ```

    The closure captures `min_val` and `max_val` and uses Python's chained comparison.
