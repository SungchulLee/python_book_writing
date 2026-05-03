# Decorator Fundamentals

A decorator is a function that takes another function as input and returns a modified version of it. Decorators provide a clean syntax for wrapping functions with additional behavior.

!!! tip "Mental Model"
    Think of a decorator as gift-wrapping a function: the original function is still inside, but the wrapper adds behavior before and after each call. The `@decorator` syntax is just shorthand for `func = decorator(func)` -- it replaces the name with the wrapped version.

## Basic Syntax

### The `@` Syntax

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before")
        result = func(*args, **kwargs)
        print("After")
        return result
    return wrapper

@decorator
def greet():
    print("Hello")

# Equivalent to:
# greet = decorator(greet)
```

The `@decorator` syntax is syntactic sugar—it automatically passes the function to the decorator and reassigns the result.

### Calling Decorated Functions

```python
greet()
# Output:
# Before
# Hello
# After
```

---

## The Wrapper Pattern

### Basic Structure

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        # Before logic (pre-processing)
        result = func(*args, **kwargs)
        # After logic (post-processing)
        return result
    return wrapper
```

**Key elements**:
- `func`: The original function being decorated
- `wrapper`: The new function that wraps the original
- `*args, **kwargs`: Accepts any arguments to pass through
- `return result`: Preserves the original return value

### Why `*args, **kwargs`?

```python
def decorator(func):
    def wrapper(*args, **kwargs):  # Accept ANY arguments
        return func(*args, **kwargs)  # Pass them through
    return wrapper

@decorator
def add(a, b):
    return a + b

@decorator
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# Both work with the same decorator
add(2, 3)           # 5
greet("Alice")      # "Hello, Alice!"
```

---

## Execution Time

### Decorators Run at Definition Time

```python
def decorator(func):
    print(f"Decorating {func.__name__}")  # Runs immediately!
    return func

@decorator  # Prints "Decorating function" when this line executes
def function():
    pass

# The decorator has already run before we call function()
```

This is important: the decorator itself runs when Python loads the module, not when you call the decorated function.

---

## Preserving Function Metadata

### The Problem

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def greet():
    """Say hello."""
    print("Hello")

print(greet.__name__)  # 'wrapper' — Wrong!
print(greet.__doc__)   # None — Lost!
```

### The Solution: `functools.wraps`

```python
from functools import wraps

def decorator(func):
    @wraps(func)  # Copies metadata from func to wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def greet():
    """Say hello."""
    print("Hello")

print(greet.__name__)  # 'greet' — Correct!
print(greet.__doc__)   # 'Say hello.' — Preserved!
```

**Always use `@wraps`**—it preserves:
- `__name__`: Function name
- `__doc__`: Docstring
- `__module__`: Module name
- `__annotations__`: Type hints
- `__dict__`: Function attributes

---

## State in Decorators

### Using Closure Variables

```python
from functools import wraps

def count_calls(func):
    count = 0
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(f"Call #{count}")
        return func(*args, **kwargs)
    
    return wrapper

@count_calls
def greet():
    print("Hello")

greet()  # Call #1, Hello
greet()  # Call #2, Hello
```

### Using Function Attributes

```python
from functools import wraps

def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)
    
    wrapper.calls = 0
    return wrapper

@count_calls
def greet():
    print("Hello")

greet()
greet()
print(greet.calls)  # 2 — Accessible from outside
```

---

## Closures vs Decorators

### Closure

A function that **retains access to variables** from its enclosing scope:

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor  # 'factor' captured from enclosing scope
    return multiply

times3 = make_multiplier(3)
print(times3(10))  # 30
```

### Decorator

A function that **takes another function as input** and **returns a new function**:

```python
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### Relationship

**Decorators are built on closures.** The `wrapper` function inside a decorator is a closure—it captures `func` from the enclosing scope.

### Comparison

| Feature | Closure | Decorator |
|---------|---------|-----------|
| **Purpose** | Retain state from outer function | Modify/enhance function behavior |
| **Returns** | A nested function | A new function wrapping the original |
| **Captures** | Variables from enclosing scope | The decorated function |
| **Used for** | Function factories, stateful functions | Logging, timing, caching, validation |

### When to Use Each

**Closures** for function factories:

```python
def make_power(exp):
    def power(base):
        return base ** exp
    return power

square = make_power(2)
cube = make_power(3)
```

**Decorators** for cross-cutting concerns:

```python
@timer
def slow_function():
    ...

@cache
def expensive_computation(x):
    ...
```

---

## Common Decorator Template

```python
from functools import wraps

def decorator_name(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # === BEFORE the original function ===
        # Pre-processing, validation, logging, etc.
        
        # === CALL the original function ===
        result = func(*args, **kwargs)
        
        # === AFTER the original function ===
        # Post-processing, cleanup, etc.
        
        return result
    return wrapper
```

---

## Summary

| Concept | Description |
|---------|-------------|
| `@decorator` | Syntactic sugar for `func = decorator(func)` |
| Wrapper pattern | Inner function that wraps the original |
| `*args, **kwargs` | Accept and pass through any arguments |
| `@wraps(func)` | Preserve original function's metadata |
| Execution time | Decorator runs at definition, wrapper runs at call |
| Closure | Function + captured environment |

**Key Takeaways**:
- Decorators are functions that transform functions
- Always use `@wraps` to preserve metadata
- The wrapper pattern is the foundation of most decorators
- Decorators run at definition time, not call time
- Decorators use closures internally
---

## Runnable Example: `decorator_examples.py`

```python
"""
Python Decorators - Practical Examples
This file contains various practical examples of decorators in Python.
Run this file to see decorators in action!
"""

import time
import functools

if __name__ == "__main__":

    print("=" * 70)
    print("PYTHON DECORATORS - EXAMPLES")
    print("=" * 70)

    # ============================================================================
    # EXAMPLE 1: Basic Decorator
    # ============================================================================
    print("\n1. BASIC DECORATOR")
    print("-" * 70)

    def simple_decorator(func):
        @functools.wraps(func)
        def wrapper():
            print("Before function call")
            result = func()
            print("After function call")
            return result
        return wrapper

    @simple_decorator
    def say_hello():
        print("Hello, World!")
        return "Greeting complete"

    result = say_hello()
    print(f"Return value: {result}")

    # ============================================================================
    # EXAMPLE 2: Decorator with Function Arguments
    # ============================================================================
    print("\n\n2. DECORATOR WITH FUNCTION ARGUMENTS")
    print("-" * 70)

    def logger(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__} with:")
            print(f"  args: {args}")
            print(f"  kwargs: {kwargs}")
            result = func(*args, **kwargs)
            print(f"  result: {result}")
            return result
        return wrapper

    @logger
    def add(a, b):
        return a + b

    @logger
    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    add(5, 3)
    print()
    greet("Alice", greeting="Hi")

    # ============================================================================
    # EXAMPLE 3: Timing Decorator
    # ============================================================================
    print("\n\n3. TIMING DECORATOR")
    print("-" * 70)

    def timer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            print(f"{func.__name__} executed in {end - start:.4f} seconds")
            return result
        return wrapper

    @timer
    def fast_function():
        return sum(range(100))

    @timer
    def slow_function():
        time.sleep(0.5)
        return sum(range(1000000))

    print(f"Fast function result: {fast_function()}")
    print(f"Slow function result: {slow_function()}")

    # ============================================================================
    # EXAMPLE 4: Decorator with Parameters
    # ============================================================================
    print("\n\n4. DECORATOR WITH PARAMETERS")
    print("-" * 70)

    def repeat(times):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                results = []
                for i in range(times):
                    print(f"  Execution {i+1}/{times}:")
                    result = func(*args, **kwargs)
                    results.append(result)
                return results
            return wrapper
        return decorator

    @repeat(times=3)
    def greet(name):
        greeting = f"Hello, {name}!"
        print(f"    {greeting}")
        return greeting

    print("Calling decorated function:")
    results = greet("Bob")
    print(f"All results: {results}")

    # ============================================================================
    # EXAMPLE 5: Multiple Decorators (Stacking)
    # ============================================================================
    print("\n\n5. STACKING MULTIPLE DECORATORS")
    print("-" * 70)

    def uppercase(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result.upper()
        return wrapper

    def exclaim(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return result + "!!!"
        return wrapper

    def quote(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return f'"{result}"'
        return wrapper

    @quote
    @uppercase
    @exclaim
    def greet(name):
        return f"hello, {name}"

    print(greet("Alice"))
    print("Note: Decorators are applied bottom-to-top")

    # ============================================================================
    # EXAMPLE 6: Caching/Memoization Decorator
    # ============================================================================
    print("\n\n6. CACHING/MEMOIZATION DECORATOR")
    print("-" * 70)

    def memoize(func):
        cache = {}
        @functools.wraps(func)
        def wrapper(*args):
            if args in cache:
                print(f"  Returning cached result for {args}")
                return cache[args]
            print(f"  Computing result for {args}")
            result = func(*args)
            cache[args] = result
            return result
        return wrapper

    @memoize
    def fibonacci(n):
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)

    print("Calculating fibonacci(5):")
    print(f"Result: {fibonacci(5)}")
    print("\nCalculating fibonacci(5) again:")
    print(f"Result: {fibonacci(5)}")

    # ============================================================================
    # EXAMPLE 7: Authentication/Authorization Decorator
    # ============================================================================
    print("\n\n7. AUTHENTICATION DECORATOR")
    print("-" * 70)

    # Simulated user system
    current_user = {"name": "Alice", "role": "admin"}

    def require_auth(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if current_user is None:
                print("Access denied: Not logged in")
                return None
            return func(*args, **kwargs)
        return wrapper

    def require_role(role):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if current_user.get("role") != role:
                    print(f"Access denied: Requires '{role}' role")
                    return None
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @require_auth
    def view_profile():
        return f"Viewing profile for {current_user['name']}"

    @require_role("admin")
    def delete_user(username):
        return f"User {username} deleted by {current_user['name']}"

    print(view_profile())
    print(delete_user("Bob"))

    # Change user role
    current_user["role"] = "user"
    print("\nAfter changing role to 'user':")
    print(delete_user("Bob"))

    # ============================================================================
    # EXAMPLE 8: Validation Decorator
    # ============================================================================
    print("\n\n8. VALIDATION DECORATOR")
    print("-" * 70)

    def validate_positive(func):
        @functools.wraps(func)
        def wrapper(n):
            if n < 0:
                raise ValueError(f"Argument must be positive, got {n}")
            return func(n)
        return wrapper

    def validate_range(min_val, max_val):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(n):
                if not (min_val <= n <= max_val):
                    raise ValueError(f"Argument must be between {min_val} and {max_val}")
                return func(n)
            return wrapper
        return decorator

    @validate_positive
    def square_root(n):
        return n ** 0.5

    @validate_range(0, 100)
    def percentage_to_grade(score):
        if score >= 90: return "A"
        if score >= 80: return "B"
        if score >= 70: return "C"
        return "F"

    print(f"Square root of 16: {square_root(16)}")
    print(f"Grade for 85: {percentage_to_grade(85)}")

    print("\nTrying invalid inputs:")
    try:
        square_root(-4)
    except ValueError as e:
        print(f"  Error: {e}")

    try:
        percentage_to_grade(150)
    except ValueError as e:
        print(f"  Error: {e}")

    # ============================================================================
    # EXAMPLE 9: Retry Decorator
    # ============================================================================
    print("\n\n9. RETRY DECORATOR")
    print("-" * 70)

    def retry(max_attempts=3, delay=0.5):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                attempts = 0
                while attempts < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        if attempts == max_attempts:
                            print(f"  Failed after {max_attempts} attempts")
                            raise
                        print(f"  Attempt {attempts} failed: {e}. Retrying...")
                        time.sleep(delay)
            return wrapper
        return decorator

    # Simulate unreliable function
    call_count = 0

    @retry(max_attempts=3, delay=0.1)
    def unreliable_function():
        global call_count
        call_count += 1
        print(f"  Attempt {call_count}")
        if call_count < 2:
            raise ConnectionError("Network error")
        return "Success!"

    print("Calling unreliable function:")
    result = unreliable_function()
    print(f"Final result: {result}")

    # ============================================================================
    # EXAMPLE 10: Class-Based Decorator
    # ============================================================================
    print("\n\n10. CLASS-BASED DECORATOR")
    print("-" * 70)

    class CountCalls:
        def __init__(self, func):
            functools.update_wrapper(self, func)
            self.func = func
            self.count = 0

        def __call__(self, *args, **kwargs):
            self.count += 1
            print(f"Call #{self.count} to {self.func.__name__}")
            return self.func(*args, **kwargs)

    @CountCalls
    def say_hello(name):
        return f"Hello, {name}!"

    print(say_hello("Alice"))
    print(say_hello("Bob"))
    print(say_hello("Charlie"))
    print(f"\nTotal calls: {say_hello.count}")

    # ============================================================================
    # EXAMPLE 11: Debug Decorator
    # ============================================================================
    print("\n\n11. DEBUG DECORATOR")
    print("-" * 70)

    def debug(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            print(f"Calling {func.__name__}({signature})")
            result = func(*args, **kwargs)
            print(f"{func.__name__!r} returned {result!r}")
            return result
        return wrapper

    @debug
    def calculate(x, y, operation="+"):
        if operation == "+":
            return x + y
        elif operation == "*":
            return x * y
        return None

    calculate(5, 3, operation="+")
    calculate(5, 3, operation="*")

    # ============================================================================
    # EXAMPLE 12: Rate Limiting Decorator
    # ============================================================================
    print("\n\n12. RATE LIMITING DECORATOR")
    print("-" * 70)

    def rate_limit(max_calls, time_period):
        """Limit function calls to max_calls per time_period seconds"""
        def decorator(func):
            calls = []

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                now = time.time()
                # Remove old calls outside the time window
                calls[:] = [call for call in calls if now - call < time_period]

                if len(calls) >= max_calls:
                    wait_time = time_period - (now - calls[0])
                    print(f"  Rate limit reached. Wait {wait_time:.2f}s")
                    return None

                calls.append(now)
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @rate_limit(max_calls=3, time_period=2)
    def api_call(endpoint):
        return f"Calling {endpoint}"

    print("Making API calls (max 3 per 2 seconds):")
    for i in range(5):
        result = api_call(f"endpoint_{i}")
        if result:
            print(f"  {result}")
        time.sleep(0.3)

    print("\n" + "=" * 70)
    print("END OF EXAMPLES")
    print("=" * 70)
```

---

## Exercises

**Exercise 1.**
Write a decorator `uppercase_result` that converts the return value of a function to uppercase. Use `@wraps` to preserve metadata. Apply it to a function `def greet(name: str) -> str` that returns `f"hello, {name}"` and verify the output.

??? success "Solution to Exercise 1"

        from functools import wraps

        def uppercase_result(func):
            """Decorator that converts the return value to uppercase."""
            @wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                return result.upper()
            return wrapper

        @uppercase_result
        def greet(name: str) -> str:
            """Return a greeting."""
            return f"hello, {name}"

        print(greet("alice"))       # HELLO, ALICE
        print(greet.__name__)       # greet
        print(greet.__doc__)        # Return a greeting.

---

**Exercise 2.**
Create a decorator `call_counter` that tracks how many times a function has been called. Store the count as a function attribute `calls` on the wrapper so it can be inspected from outside. Demonstrate that calling the decorated function three times sets `func.calls` to `3`.

??? success "Solution to Exercise 2"

        from functools import wraps

        def call_counter(func):
            """Decorator that counts how many times the function is called."""
            @wraps(func)
            def wrapper(*args, **kwargs):
                wrapper.calls += 1
                return func(*args, **kwargs)
            wrapper.calls = 0
            return wrapper

        @call_counter
        def say_hi():
            print("Hi!")

        say_hi()
        say_hi()
        say_hi()
        print(say_hi.calls)  # 3

---

**Exercise 3.**
Write a decorator `require_positive` that inspects all positional arguments before calling the original function and raises a `ValueError` if any argument is a negative number. Non-numeric arguments should be ignored. Apply it to a function `def area(width, height)` and test with both valid and invalid inputs.

??? success "Solution to Exercise 3"

        from functools import wraps

        def require_positive(func):
            """Decorator that rejects negative numeric arguments."""
            @wraps(func)
            def wrapper(*args, **kwargs):
                for arg in args:
                    if isinstance(arg, (int, float)) and arg < 0:
                        raise ValueError(
                            f"Negative argument not allowed: {arg}"
                        )
                return func(*args, **kwargs)
            return wrapper

        @require_positive
        def area(width, height):
            return width * height

        print(area(5, 10))   # 50
        try:
            area(-3, 10)     # ValueError
        except ValueError as e:
            print(e)
