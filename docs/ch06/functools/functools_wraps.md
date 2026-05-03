# functools.wraps

When writing decorators, `functools.wraps` preserves the original function's metadata. Without it, decorated functions lose their name, docstring, and other attributes.

!!! tip "Mental Model"
    A decorator replaces your function with a wrapper, and that wrapper has its own `__name__`, `__doc__`, and other attributes. `@wraps(func)` copies the original's metadata onto the wrapper so the outside world still sees the original identity. Think of it as a name tag transfer -- the wrapper wears the original's badge.

```python
from functools import wraps
```

---

## The Problem

### Without wraps

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        print("Before call")
        result = func(*args, **kwargs)
        print("After call")
        return result
    return wrapper

@my_decorator
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

# Metadata is lost!
print(greet.__name__)  # 'wrapper' — Wrong!
print(greet.__doc__)   # 'Wrapper function.' — Wrong!
```

The decorated function looks like `wrapper`, not `greet`.

---

## The Solution

### With wraps

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)  # Preserves func's metadata
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        print("Before call")
        result = func(*args, **kwargs)
        print("After call")
        return result
    return wrapper

@my_decorator
def greet(name):
    """Return a greeting message."""
    return f"Hello, {name}!"

# Metadata preserved!
print(greet.__name__)  # 'greet' — Correct!
print(greet.__doc__)   # 'Return a greeting message.' — Correct!
```

---

## What wraps Preserves

`wraps` copies these attributes from the original function:

| Attribute | Description |
|-----------|-------------|
| `__name__` | Function name |
| `__doc__` | Docstring |
| `__module__` | Module where defined |
| `__qualname__` | Qualified name (includes class) |
| `__annotations__` | Type hints |
| `__dict__` | Function's attribute dictionary |

It also sets:

| Attribute | Description |
|-----------|-------------|
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
def original():
    """Original docstring."""
    pass

# Access the unwrapped function
print(original.__wrapped__)  # <function original at 0x...>
print(original.__wrapped__.__name__)  # 'original'
```

---

## Decorator Templates

### Basic Decorator

```python
from functools import wraps

def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Before
        result = func(*args, **kwargs)
        # After
        return result
    return wrapper
```

### Decorator with Arguments

```python
from functools import wraps

def decorator_with_args(arg1, arg2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Use arg1, arg2 here
            print(f"Args: {arg1}, {arg2}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@decorator_with_args("hello", 42)
def my_function():
    """My function docstring."""
    pass

print(my_function.__name__)  # 'my_function'
```

### Optional Arguments Decorator

```python
from functools import wraps

def decorator(func=None, *, option1=None, option2=None):
    """Decorator that works with or without arguments."""
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Options: {option1}, {option2}")
            return func(*args, **kwargs)
        return wrapper
    
    if func is None:
        # Called with arguments: @decorator(option1="x")
        return actual_decorator
    else:
        # Called without arguments: @decorator
        return actual_decorator(func)

# Both work:
@decorator
def func1(): pass

@decorator(option1="custom")
def func2(): pass
```

---

## Practical Examples

### Logging Decorator

```python
from functools import wraps
import logging

def log_calls(func):
    """Log function calls with arguments and return values."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Calling {func.__name__} with {args}, {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} returned {result}")
        return result
    return wrapper

@log_calls
def add(a, b):
    """Add two numbers."""
    return a + b
```

### Timing Decorator

```python
from functools import wraps
import time

def timer(func):
    """Measure function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    """A slow function."""
    time.sleep(1)
    return "done"
```

### Retry Decorator

```python
from functools import wraps
import time

def retry(max_attempts=3, delay=1):
    """Retry function on exception."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    print(f"{func.__name__} failed (attempt {attempt + 1})")
                    time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unreliable_api_call():
    """Call an unreliable API."""
    pass
```

### Validation Decorator

```python
from functools import wraps

def validate_types(**type_hints):
    """Validate argument types."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check keyword arguments
            for name, expected_type in type_hints.items():
                if name in kwargs:
                    value = kwargs[name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{name} must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def create_user(name, age):
    """Create a user with validated types."""
    return {"name": name, "age": age}
```

---

## Why Metadata Matters

### Help and Documentation

```python
# Without wraps: help shows wrapper info
help(greet)  # Shows "wrapper function" docs

# With wraps: help shows original info
help(greet)  # Shows "Return a greeting message."
```

### Debugging and Logging

```python
# Without wraps: confusing stack traces
# Error in wrapper at line 5...

# With wraps: clear stack traces
# Error in greet at line 20...
```

### Introspection Tools

```python
# Frameworks and tools rely on __name__
import inspect

# Without wraps
inspect.signature(greet)  # Shows wrapper's signature

# With wraps
inspect.signature(greet)  # Shows greet's signature
```

### Testing

```python
# Test frameworks use function names
def test_greet():
    assert greet.__name__ == "greet"  # Fails without wraps!
```

---

## Common Mistakes

### Forgetting wraps

```python
# Bad: loses metadata
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper  # Missing @wraps(func)!

# Good: preserves metadata
def good_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Wrong Placement

```python
# Wrong: wraps on outer function
@wraps(func)  # This doesn't work!
def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# Right: wraps on inner function
def decorator(func):
    @wraps(func)  # Correct placement
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Class-Based Decorators

```python
from functools import wraps, update_wrapper

class Decorator:
    """Class-based decorator with proper metadata."""
    
    def __init__(self, func):
        self.func = func
        update_wrapper(self, func)  # Use update_wrapper for classes
    
    def __call__(self, *args, **kwargs):
        print("Before")
        result = self.func(*args, **kwargs)
        print("After")
        return result

@Decorator
def my_func():
    """My function."""
    pass

print(my_func.__name__)  # 'my_func'
```

---

## Summary

| Without `@wraps` | With `@wraps` |
|------------------|---------------|
| `__name__` = 'wrapper' | `__name__` = original name |
| `__doc__` = wrapper's doc | `__doc__` = original doc |
| No `__wrapped__` | `__wrapped__` = original func |
| Confusing debugging | Clear stack traces |
| Broken introspection | Tools work correctly |

**Key Takeaways**:

- Always use `@wraps(func)` when writing decorators
- Place `@wraps` on the inner wrapper function
- Use `update_wrapper()` for class-based decorators
- `__wrapped__` provides access to the original function
- Proper metadata enables debugging, documentation, and testing

---

## Exercises

**Exercise 1.**
Write a `@timer` decorator without `@wraps` and one with `@wraps`. Apply each to a function with a docstring. Print `__name__` and `__doc__` for both decorated functions to demonstrate the difference.

??? success "Solution to Exercise 1"

        from functools import wraps

        def timer_bad(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        def timer_good(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

        @timer_bad
        def add_bad(a, b):
            """Add two numbers."""
            return a + b

        @timer_good
        def add_good(a, b):
            """Add two numbers."""
            return a + b

        print(f"Without wraps: name={add_bad.__name__}, doc={add_bad.__doc__}")
        # Without wraps: name=wrapper, doc=None

        print(f"With wraps:    name={add_good.__name__}, doc={add_good.__doc__}")
        # With wraps:    name=add_good, doc=Add two numbers.

---

**Exercise 2.**
Write a decorator `@logged` that uses `@wraps` and prints a message before calling the function. After decorating a function, access `__wrapped__` to call the original function directly (bypassing the decorator). Verify no log message is printed when calling via `__wrapped__`.

??? success "Solution to Exercise 2"

        from functools import wraps

        def logged(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(f"LOG: calling {func.__name__}")
                return func(*args, **kwargs)
            return wrapper

        @logged
        def multiply(a, b):
            """Multiply two numbers."""
            return a * b

        print(multiply(3, 4))       # LOG: calling multiply \n 12

        # Bypass the decorator via __wrapped__
        original = multiply.__wrapped__
        print(original(3, 4))       # 12 (no LOG message)

---

**Exercise 3.**
Create a class-based decorator `CallTracker` that counts calls. Use `functools.update_wrapper` in `__init__` to preserve metadata. Decorate a function, call it three times, then verify that `__name__`, `__doc__`, and the `count` attribute all work correctly.

??? success "Solution to Exercise 3"

        import functools

        class CallTracker:
            def __init__(self, func):
                functools.update_wrapper(self, func)
                self.func = func
                self.count = 0

            def __call__(self, *args, **kwargs):
                self.count += 1
                return self.func(*args, **kwargs)

        @CallTracker
        def greet(name):
            """Greet someone by name."""
            return f"Hello, {name}!"

        greet("Alice")
        greet("Bob")
        greet("Charlie")

        print(greet.__name__)  # greet
        print(greet.__doc__)   # Greet someone by name.
        print(greet.count)     # 3
