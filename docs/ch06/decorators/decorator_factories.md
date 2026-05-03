# Decorator Factories

Decorator factories create parameterized decorators, allowing you to customize decorator behavior.

!!! tip "Mental Model"
    A decorator factory is a function that returns a decorator -- it adds one extra layer of nesting so you can pass configuration arguments. When you write `@repeat(3)`, Python first calls `repeat(3)` to get a decorator, then applies that decorator to your function. Three nested functions, three distinct jobs: configure, wrap, execute.

## Basic Factory Pattern

A decorator factory is a function that returns a decorator:

```python
from functools import wraps

def repeat(times):
    """Decorator factory that repeats function execution."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet():
    print("Hello")

greet()  # Prints "Hello" 3 times
```

### Three Levels of Nesting

```python
def factory(param):           # Level 1: Factory (accepts parameters)
    def decorator(func):      # Level 2: Decorator (accepts function)
        @wraps(func)
        def wrapper(*args):   # Level 3: Wrapper (accepts call arguments)
            # Use param, func, and args
            return func(*args)
        return wrapper
    return decorator
```

---

## Multiple Parameters

### Configuration Decorator

```python
from functools import wraps

def log(level="INFO", prefix=""):
    """Configurable logging decorator."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] {prefix}{func.__name__} called")
            result = func(*args, **kwargs)
            print(f"[{level}] {prefix}{func.__name__} returned {result}")
            return result
        return wrapper
    return decorator

@log(level="DEBUG", prefix=">> ")
def add(a, b):
    return a + b

add(2, 3)
# [DEBUG] >> add called
# [DEBUG] >> add returned 5
```

### Retry with Configuration

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Retry decorator with configurable attempts and delay."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        print(f"Attempt {attempt} failed, retrying in {delay}s...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
def fetch_data():
    # May fail occasionally
    pass
```

---

## Preserving Metadata with `functools.wraps`

### The Problem

Without `@wraps`, the wrapper replaces the original function's metadata:

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def greet():
    """Say hello."""
    pass

print(greet.__name__)  # 'wrapper' — Lost!
print(greet.__doc__)   # None — Lost!
```

### The Solution

```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def greet():
    """Say hello."""
    pass

print(greet.__name__)  # 'greet' — Preserved!
print(greet.__doc__)   # 'Say hello.' — Preserved!
```

### What `@wraps` Preserves

| Attribute | Description |
|-----------|-------------|
| `__name__` | Function name |
| `__doc__` | Docstring |
| `__module__` | Module where defined |
| `__annotations__` | Type hints |
| `__qualname__` | Qualified name |
| `__dict__` | Function attributes |
| `__wrapped__` | Reference to original function |

### Accessing the Original Function

```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorator
def greet():
    """Say hello."""
    print("Hello")

# Access the original unwrapped function
original = greet.__wrapped__
```

---

## Optional Parameters Pattern

Create decorators that work with or without parentheses:

```python
from functools import wraps

def log(func=None, *, level="INFO"):
    """Decorator that works with or without arguments."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Calling {fn.__name__}")
            return fn(*args, **kwargs)
        return wrapper
    
    if func is not None:
        # Called without arguments: @log
        return decorator(func)
    # Called with arguments: @log(level="DEBUG")
    return decorator

# Both work:
@log
def func1():
    pass

@log(level="DEBUG")
def func2():
    pass
```

---

## Factory with Validation

```python
from functools import wraps

def validate_types(*types):
    """Validate argument types."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg, expected_type in zip(args, types):
                if not isinstance(arg, expected_type):
                    raise TypeError(
                        f"Expected {expected_type.__name__}, got {type(arg).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(int, int)
def add(a, b):
    return a + b

add(2, 3)       # Works: 5
add("2", 3)     # TypeError: Expected int, got str
```

---

## Summary

| Concept | Description |
|---------|-------------|
| Decorator factory | Function that returns a decorator |
| Three levels | Factory → Decorator → Wrapper |
| `@wraps(func)` | Preserves original function metadata |
| Optional params | Support both `@deco` and `@deco()` |

**Best Practices**:
- Always use `@wraps(func)` in wrappers
- Use keyword-only arguments for clarity
- Document factory parameters
- Consider optional parameter pattern for flexibility
---

## Runnable Example: `decorator_factory_strategy_example.py`

```python
"""
Decorator Factory with Strategy Pattern

This example demonstrates a decorator factory that accepts different
output strategies (console, file) for recording function execution.
This combines decorator factories with the strategy design pattern.

Topics covered:
- Decorator factories (decorators that accept parameters)
- Strategy pattern (swappable behavior via function arguments)
- functools.wraps for preserving function metadata
- Timing function execution

Based on concepts from Python-100-Days example09 and ch05/decorators materials.
"""

from functools import wraps
from time import time, sleep


# =============================================================================
# Example 1: Output Strategy Functions
# =============================================================================

def output_to_console(func_name: str, duration: float) -> None:
    """Strategy: print timing info to console."""
    print(f'  [{func_name}] completed in {duration:.3f}s')


def output_to_file(func_name: str, duration: float,
                   filename: str = 'timing_log.txt') -> None:
    """Strategy: append timing info to a log file."""
    with open(filename, 'a') as f:
        f.write(f'{func_name}: {duration:.3f}s\n')
    print(f'  [{func_name}] logged to {filename}')


# =============================================================================
# Example 2: Decorator Factory with Strategy Parameter
# =============================================================================

def record(output_strategy):
    """Decorator factory: create a timing decorator with a given output strategy.

    This is a three-level nesting pattern:
    1. record(strategy) -> returns the actual decorator
    2. decorator(func) -> wraps the target function
    3. wrapper(*args, **kwargs) -> executes and times the function

    Usage:
        @record(output_to_console)
        def my_function():
            ...
    """
    def decorator(func):
        @wraps(func)  # Preserve original function's __name__, __doc__, etc.
        def wrapper(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            duration = time() - start
            output_strategy(func.__name__, duration)
            return result
        return wrapper
    return decorator


# =============================================================================
# Example 3: Using the Decorator Factory
# =============================================================================

@record(output_to_console)
def simulate_api_call(endpoint: str, delay: float = 0.1) -> str:
    """Simulate an API call with artificial delay."""
    sleep(delay)
    return f"Response from {endpoint}"


@record(output_to_file)
def simulate_db_query(query: str, delay: float = 0.05) -> list:
    """Simulate a database query with artificial delay."""
    sleep(delay)
    return [{"id": 1, "data": query}]


# =============================================================================
# Example 4: Flexible Strategy with Lambda
# =============================================================================

@record(lambda name, dur: print(f'  >>> {name} took {dur*1000:.1f}ms'))
def quick_operation():
    """A fast operation with inline strategy."""
    return sum(range(10000))


# =============================================================================
# Example 5: Accessing __wrapped__ to Bypass Decorator
# =============================================================================

def demo_unwrap():
    """functools.wraps adds __wrapped__ attribute for accessing the original."""
    print("\n=== Bypassing Decorator ===")
    print(f"Decorated name: {simulate_api_call.__name__}")

    # Access original function without timing
    original = simulate_api_call.__wrapped__
    result = original("/api/test", delay=0.01)
    print(f"  Direct call (no timing): {result}")


# =============================================================================
# Example 6: Configurable Decorator Factory
# =============================================================================

def timed(*, threshold: float = 0.0, label: str = ""):
    """Decorator factory that only reports when execution exceeds threshold.

    This is a more practical version showing how decorator factories
    can accept keyword arguments for configuration.

    Usage:
        @timed(threshold=0.5, label="SLOW")
        def my_function():
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            duration = time() - start
            if duration >= threshold:
                tag = f" [{label}]" if label else ""
                print(f"  {func.__name__}{tag}: {duration:.3f}s "
                      f"(threshold: {threshold:.3f}s)")
            return result
        return wrapper
    return decorator


@timed(threshold=0.1, label="SLOW")
def fast_function():
    """This function is fast, so timing won't be reported."""
    return sum(range(100))


@timed(threshold=0.01, label="DB")
def slow_function():
    """This function is slow, so timing will be reported."""
    sleep(0.05)
    return "done"


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    print("=== Decorator Factory with Strategy Pattern ===\n")

    print("--- Console Strategy ---")
    result = simulate_api_call("/api/users", delay=0.1)
    print(f"  Result: {result}")

    print("\n--- File Strategy ---")
    result = simulate_db_query("SELECT * FROM users")
    print(f"  Result: {result}")

    print("\n--- Lambda Strategy ---")
    result = quick_operation()
    print(f"  Result: {result}")

    demo_unwrap()

    print("\n=== Configurable Threshold Decorator ===")
    fast_function()   # Won't print (under threshold)
    slow_function()   # Will print (over threshold)
    print("  fast_function: no output (under threshold)")
```

---

## Exercises

**Exercise 1.**
Write a decorator factory `tag(tag_name)` that wraps the string return value of a function in an HTML tag. For example, `@tag("b")` applied to a function returning `"hello"` should produce `"<b>hello</b>"`. Use `@wraps` to preserve metadata.

??? success "Solution to Exercise 1"

        from functools import wraps

        def tag(tag_name):
            """Decorator factory that wraps return value in an HTML tag."""
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    return f"<{tag_name}>{result}</{tag_name}>"
                return wrapper
            return decorator

        @tag("b")
        def greet(name):
            """Return a greeting."""
            return f"Hello, {name}"

        print(greet("Alice"))       # <b>Hello, Alice</b>
        print(greet.__name__)       # greet
        print(greet.__doc__)        # Return a greeting.

---

**Exercise 2.**
Create a decorator factory `enforce_types` that reads a function's type annotations and raises a `TypeError` if any argument does not match its annotation at call time. It should silently ignore parameters without annotations. Demonstrate it on a function `def greet(name: str, times: int) -> str`.

??? success "Solution to Exercise 2"

        from functools import wraps
        import inspect

        def enforce_types(func):
            """Decorator that enforces type annotations at call time."""
            hints = func.__annotations__
            sig = inspect.signature(func)

            @wraps(func)
            def wrapper(*args, **kwargs):
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                for name, value in bound.arguments.items():
                    if name in hints and name != 'return':
                        expected = hints[name]
                        if not isinstance(value, expected):
                            raise TypeError(
                                f"Argument '{name}' must be {expected.__name__}, "
                                f"got {type(value).__name__}"
                            )
                return func(*args, **kwargs)
            return wrapper

        @enforce_types
        def greet(name: str, times: int) -> str:
            return (name + "! ") * times

        print(greet("Alice", 3))     # Alice! Alice! Alice!
        try:
            greet("Alice", "three")  # TypeError
        except TypeError as e:
            print(e)

---

**Exercise 3.**
Write an optional-parameter decorator factory `debug(func=None, *, show_args=True, show_result=True)` that works both as `@debug` and `@debug(show_result=False)`. When `show_args` is `True`, print the arguments before the call. When `show_result` is `True`, print the return value after the call.

??? success "Solution to Exercise 3"

        from functools import wraps

        def debug(func=None, *, show_args=True, show_result=True):
            """Debug decorator that works with or without arguments."""
            def decorator(fn):
                @wraps(fn)
                def wrapper(*args, **kwargs):
                    if show_args:
                        print(f"Calling {fn.__name__}({args}, {kwargs})")
                    result = fn(*args, **kwargs)
                    if show_result:
                        print(f"{fn.__name__} returned {result!r}")
                    return result
                return wrapper

            if func is not None:
                return decorator(func)
            return decorator

        @debug
        def add(a, b):
            return a + b

        @debug(show_result=False)
        def multiply(a, b):
            return a * b

        add(2, 3)        # prints args and result
        multiply(4, 5)   # prints args only
