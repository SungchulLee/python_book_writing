# Practical Decorator Patterns

Common real-world decorator patterns for timing, caching, validation, and more.

!!! tip "Mental Model"
    Decorators shine as cross-cutting concerns -- behavior you want to inject into many functions without modifying any of them. Timing, logging, caching, access control, and retry logic all follow the same shape: do something before/after/around the original call. Once you see a decorator as a reusable "before-and-after" sandwich, every pattern here becomes a variation of filling.

## Timing Decorator

Measure function execution time without modifying the original code.

```python
import time
from functools import wraps

def timer(func):
    """Measure and print execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(0.5)
    return "done"

slow_function()  # slow_function took 0.5012 seconds
```

### Comparing Algorithms

```python
@timer
def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

@timer
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

data = list(range(1000, 0, -1))
bubble_sort(data)  # bubble_sort took 0.0892 seconds
quick_sort(data)   # quick_sort took 0.0023 seconds
```

---

## Trace Decorator

Visualize recursive function calls with indentation.

```python
def trace(func):
    """Trace recursive function calls."""
    trace.depth = 0
    
    @wraps(func)
    def wrapper(*args):
        indent = '│  ' * trace.depth
        print(f"{indent}├─ {func.__name__}{args}")
        trace.depth += 1
        result = func(*args)
        trace.depth -= 1
        print(f"{indent}├─ return {result}")
        return result
    return wrapper

@trace
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

factorial(4)
```

Output:
```
├─ factorial(4,)
│  ├─ factorial(3,)
│  │  ├─ factorial(2,)
│  │  │  ├─ factorial(1,)
│  │  │  ├─ return 1
│  │  ├─ return 2
│  ├─ return 6
├─ return 24
```

---

## Logger Decorator

Log function calls with arguments and return values.

```python
from functools import wraps
import logging

logging.basicConfig(level=logging.DEBUG)

def logger(func):
    """Log function calls."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.debug(f"Calling {func.__name__}")
        logging.debug(f"  args: {args}")
        logging.debug(f"  kwargs: {kwargs}")
        result = func(*args, **kwargs)
        logging.debug(f"  returned: {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(3, 5)
```

---

## Memoization (Caching)

Cache function results for repeated calls.

### Simple Memoization

```python
def memoize(func):
    """Cache function results."""
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    
    wrapper.cache = cache
    wrapper.cache_clear = lambda: cache.clear()
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Fast due to caching
```

### Using Built-in `lru_cache`

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))
print(fibonacci.cache_info())  # CacheInfo(hits=98, misses=101, ...)
```

---

## Retry Decorator

Automatically retry failed operations.

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    """Retry failed function calls."""
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
                        print(f"Attempt {attempt} failed: {e}. Retrying...")
                        time.sleep(delay)
            raise last_exception
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5, exceptions=(ConnectionError,))
def fetch_data(url):
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return "Data"
```

---

## Validation Decorator

Validate function arguments.

### Type Validation

```python
from functools import wraps

def validate_types(*types):
    """Validate argument types."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg, expected in zip(args, types):
                if not isinstance(arg, expected):
                    raise TypeError(
                        f"Expected {expected.__name__}, got {type(arg).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(int, int)
def add(a, b):
    return a + b

add(2, 3)      # Works: 5
add("2", 3)    # TypeError
```

### Range Validation

```python
def validate_range(min_val=None, max_val=None):
    """Validate numeric arguments are within range."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for arg in args:
                if isinstance(arg, (int, float)):
                    if min_val is not None and arg < min_val:
                        raise ValueError(f"Value {arg} below minimum {min_val}")
                    if max_val is not None and arg > max_val:
                        raise ValueError(f"Value {arg} above maximum {max_val}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_range(min_val=0, max_val=100)
def set_percentage(value):
    return value

set_percentage(50)   # Works
set_percentage(150)  # ValueError
```

---

## Rate Limiting

Limit how often a function can be called.

```python
import time
from functools import wraps

def rate_limit(calls_per_second=1):
    """Limit function call rate."""
    min_interval = 1.0 / calls_per_second
    last_call = [0.0]  # Mutable container for closure
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_second=2)
def api_call():
    print(f"Called at {time.time():.2f}")

# Will be limited to 2 calls per second
for _ in range(5):
    api_call()
```

---

## Deprecation Warning

Warn when deprecated functions are used.

```python
import warnings
from functools import wraps

def deprecated(message=""):
    """Mark a function as deprecated."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} is deprecated. {message}",
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@deprecated("Use new_function() instead")
def old_function():
    return "old"

old_function()  # DeprecationWarning: old_function is deprecated. Use new_function() instead
```

---

## Summary

| Decorator | Purpose | Key Feature |
|-----------|---------|-------------|
| `@timer` | Measure execution time | Performance profiling |
| `@trace` | Visualize call stack | Debugging recursion |
| `@logger` | Log function calls | Debugging, audit trail |
| `@memoize` | Cache results | Performance optimization |
| `@retry` | Retry on failure | Resilience |
| `@validate` | Validate arguments | Input safety |
| `@rate_limit` | Limit call frequency | API protection |
| `@deprecated` | Warn about old functions | Migration support |

**Key Benefits**:

- Keep original functions clean
- Reusable across many functions
- Easy to enable/disable
- Separate concerns (single responsibility)
---

## Runnable Example: `timing_decorator_professional.py`

```python
"""
TUTORIAL: Professional Timing Decorator Using functools.wraps

This tutorial covers how to write a PRODUCTION-QUALITY decorator that measures
function execution time.

The Key Concept: Decorators wrap functions to add behavior. But wrapping hides
the original function's metadata. The functools.wraps decorator solves this by
copying the wrapped function's metadata (__name__, __doc__, etc.) to the wrapper.

This tutorial demonstrates the CLOCK DECORATOR, which times function execution
and prints detailed information about calls, including arguments and results.
This is based on the clockdeco examples from Fluent Python.

Professional decorator pattern:
1. Use functools.wraps to preserve metadata
2. Handle *args and **kwargs for flexibility
3. Format output clearly
4. Don't hide function signature
5. Use functools.wraps ALWAYS
"""

import time
import functools

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Professional Timing Decorator with functools.wraps")
    print("=" * 70)

    # ============ EXAMPLE 1: The Problem Without functools.wraps
    print("\n# ============ EXAMPLE 1: The Problem Without functools.wraps")
    print("Why functools.wraps is essential:\n")


    def bad_timer(func):
        """A timer decorator WITHOUT functools.wraps"""
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"[{elapsed:.4f}s] Function executed")
            return result
        return wrapper


    @bad_timer
    def slow_function(n):
        """Compute factorial - this docstring will be lost!"""
        time.sleep(0.1)
        return n * (n - 1)


    print("Function with bad_timer decorator:")
    print(f"Function name: {slow_function.__name__}")
    print(f"Expected: slow_function")
    print(f"Actual: wrapper <- WRONG! We lost the original name!")
    print()

    print(f"Function docstring: {slow_function.__doc__}")
    print(f"Expected: 'Compute factorial - this docstring will be lost!'")
    print(f"Actual: {slow_function.__doc__} <- LOST!")
    print()

    print("""
    PROBLEM: When a decorator returns a wrapper function, it replaces
    the original function's metadata. The wrapper function has its own
    name, docstring, etc. This breaks:
      - help() documentation
      - __name__ inspection
      - __doc__ access
      - IDE autocomplete
      - Type stubs and type hints
    """)

    # ============ EXAMPLE 2: The Solution - functools.wraps
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 2: The Solution - functools.wraps")
    print("Using functools.wraps preserves original metadata:\n")


    def good_timer(func):
        """A timer decorator WITH functools.wraps"""
        @functools.wraps(func)  # This is the KEY line!
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            print(f"[{elapsed:.4f}s] Function executed")
            return result
        return wrapper


    @good_timer
    def factorial(n):
        """Compute factorial of n"""
        time.sleep(0.05)
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


    print("Function with good_timer decorator (using functools.wraps):")
    print(f"Function name: {factorial.__name__}")
    print(f"Expected: factorial")
    print(f"Actual: factorial <- CORRECT!")
    print()

    print(f"Function docstring: {factorial.__doc__}")
    print(f"Expected: 'Compute factorial of n'")
    print(f"Actual: {factorial.__doc__} <- CORRECT!")
    print()

    print("Calling the function:")
    result = factorial(5)
    print(f"Result: {result}\n")

    # ============ EXAMPLE 3: What functools.wraps Does
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 3: What functools.wraps Does")
    print("Understanding the metadata that gets preserved:\n")

    print("""
    @functools.wraps(func) copies these attributes from the original function:
      - __name__:      Function name
      - __doc__:       Docstring
      - __module__:    Module where defined
      - __qualname__:  Qualified name
      - __annotations__: Type hints
      - __dict__:      Function attributes
      - __wrapped__:   Reference to original function (for introspection!)

    EXAMPLE: Before functools.wraps
      wrapper.__name__ = 'wrapper'
      wrapper.__doc__ = None
      wrapper.__module__ = '__main__'

    AFTER functools.wraps(original_func)
      wrapper.__name__ = original_func.__name__
      wrapper.__doc__ = original_func.__doc__
      wrapper.__module__ = original_func.__module__
      wrapper.__wrapped__ = original_func  <- Can access original!
    """)

    # ============ EXAMPLE 4: The Clock Decorator - Professional Implementation
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 4: The Clock Decorator - Professional Implementation")
    print("A production-quality timing decorator:\n")


    def clock(func):
        """
        Decorator to time function execution and print details.

        Shows:
        - Elapsed time
        - Function name
        - All arguments (args and kwargs)
        - Return value

        Uses functools.wraps to preserve original function metadata.
        """
        @functools.wraps(func)
        def clocked(*args, **kwargs):
            # Record the start time
            t0 = time.perf_counter()

            # Call the original function
            result = func(*args, **kwargs)

            # Calculate elapsed time
            elapsed = time.perf_counter() - t0

            # Get function name
            name = func.__name__

            # Format arguments
            arg_lst = [repr(arg) for arg in args]
            arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
            arg_str = ', '.join(arg_lst)

            # Print the result in a nice format
            print(f'[{elapsed:0.8f}s] {name}({arg_str}) -> {result!r}')

            return result

        return clocked


    print("Define some test functions with the @clock decorator:\n")


    @clock
    def factorial_fast(n):
        """Compute n!"""
        if n < 2:
            return 1
        return n * factorial_fast(n - 1)


    @clock
    def fibonacci(n):
        """Compute Fibonacci number at position n"""
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)


    @clock
    def greet(name, greeting="Hello"):
        """Greet someone with a custom greeting"""
        time.sleep(0.01)
        return f"{greeting}, {name}!"


    print("Test 1: Simple function with one argument")
    result = factorial_fast(5)
    print()

    print("Test 2: Recursive function")
    result = fibonacci(5)
    print()

    print("Test 3: Function with keyword arguments")
    result = greet("Alice", greeting="Hi")
    print()

    print("Test 4: Function with positional and keyword args")
    result = greet("Bob")
    print()

    # ============ EXAMPLE 5: Accessing the Original Function
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 5: Accessing the Original Function")
    print("functools.wraps provides __wrapped__ for introspection:\n")

    print("Decorated function still accessible via __wrapped__:")
    print(f"factorial_fast.__wrapped__ = {factorial_fast.__wrapped__}")
    print(f"factorial_fast.__wrapped__ is the original function")

    print("\nYou can call the original function directly (bypassing decoration):")
    # This calls the original without timing
    original_result = factorial_fast.__wrapped__(5)
    print(f"Result: {original_result}\n")

    print(f"Compare metadata:")
    print(f"  factorial_fast.__name__ = {factorial_fast.__name__}")
    print(f"  factorial_fast.__doc__ = {factorial_fast.__doc__}")
    print(f"  factorial_fast.__wrapped__ = {factorial_fast.__wrapped__}")

    # ============ EXAMPLE 6: Comparing Decorated vs Non-Decorated
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 6: Comparing Decorated vs Non-Decorated")
    print("Timing the same function with and without decoration:\n")


    def undecorated_calculation(n):
        """Calculate something without timing"""
        return sum(range(n))


    @clock
    def decorated_calculation(n):
        """Calculate something with timing"""
        return sum(range(n))


    print("Calling undecorated version:")
    result1 = undecorated_calculation(1000000)
    print(f"Result: {result1}\n")

    print("Calling decorated version (note the timing output):")
    result2 = decorated_calculation(1000000)
    print(f"Result: {result2}")
    print("(Notice how the decorated version prints timing info)\n")

    # ============ EXAMPLE 7: Customizing the Clock Decorator
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 7: Customizing the Clock Decorator")
    print("Create a parameterized version that shows/hides details:\n")


    def clock_with_options(precision=8, show_args=True, show_result=True):
        """
        Decorator factory that creates customized timing decorators.

        Args:
            precision: Decimal places for elapsed time (default: 8)
            show_args: Whether to show arguments (default: True)
            show_result: Whether to show return value (default: True)
        """
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                t0 = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - t0

                name = func.__name__

                # Build output string based on options
                if show_args:
                    arg_lst = [repr(arg) for arg in args]
                    arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
                    arg_str = ', '.join(arg_lst)
                    parts = [f'{name}({arg_str})']
                else:
                    parts = [f'{name}()']

                if show_result:
                    parts.append(f'-> {result!r}')

                output = ' '.join(parts)
                format_str = f'[{{:0.{precision}f}}s] {{}}'
                print(format_str.format(elapsed, output))

                return result
            return wrapper
        return decorator


    @clock_with_options()
    def func_full_info(x):
        """Shows everything"""
        time.sleep(0.01)
        return x * 2


    @clock_with_options(show_args=False, show_result=False)
    def func_minimal_info(x):
        """Shows only timing and function name"""
        time.sleep(0.01)
        return x * 2


    @clock_with_options(precision=3, show_result=False)
    def func_moderate_info(x):
        """Shows timing, name, and args, but not result"""
        time.sleep(0.01)
        return x * 2


    print("Full info (shows everything):")
    func_full_info(42)

    print("\nMinimal info (only timing and name):")
    func_minimal_info(42)

    print("\nModerate info (timing, name, args, but not result):")
    func_moderate_info(42)

    # ============ EXAMPLE 8: Multiple Decorators with functools.wraps
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 8: Multiple Decorators with functools.wraps")
    print("Stacking decorators while preserving metadata:\n")


    def trace(func):
        """Decorator that shows when functions enter/exit"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  >> Entering {func.__name__}")
            result = func(*args, **kwargs)
            print(f"  << Exiting {func.__name__}")
            return result
        return wrapper


    @clock
    @trace
    def with_both_decorators(n):
        """Function with both decorators"""
        time.sleep(0.02)
        return n ** 2


    print("Function with @clock and @trace decorators:")
    print(f"Name: {with_both_decorators.__name__}")
    print(f"Doc: {with_both_decorators.__doc__}\n")

    print("Calling the function:")
    result = with_both_decorators(5)
    print(f"Result: {result}")

    # ============ EXAMPLE 9: Real-World Use Cases
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 9: Real-World Use Cases")
    print("Practical applications of timing decorators:\n")


    @clock
    def api_call(endpoint):
        """Simulate an API call"""
        time.sleep(0.1)
        return f"Data from {endpoint}"


    @clock
    def database_query(table, limit=10):
        """Simulate a database query"""
        time.sleep(0.05)
        return f"Fetched {limit} rows from {table}"


    @clock
    def process_data(data):
        """Process some data"""
        time.sleep(0.02)
        return f"Processed: {data}"


    print("API call timing:")
    api_call('/users')

    print("\nDatabase query timing:")
    database_query('users', limit=100)

    print("\nData processing timing:")
    process_data([1, 2, 3, 4, 5])

    # ============ EXAMPLE 10: Best Practices for Decorators
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 10: Best Practices for Decorators")
    print("Guidelines for writing professional decorators:\n")

    print("""
    BEST PRACTICES FOR DECORATORS:

    1. ALWAYS USE functools.wraps
       @functools.wraps(func)
       def wrapper(*args, **kwargs):
           ...

       This preserves:
       - Function name
       - Docstring
       - Type hints
       - __wrapped__ reference

    2. USE *args AND **kwargs FOR FLEXIBILITY
       def wrapper(*args, **kwargs):
           ...

       This allows the decorator to work with any function signature.

    3. PRESERVE RETURN VALUE
       Always return the result from calling the wrapped function.
       return func(*args, **kwargs)

    4. HANDLE EXCEPTIONS PROPERLY
       If you need to catch exceptions, re-raise them after cleanup.
       try:
           result = func(*args, **kwargs)
       finally:
           # cleanup

    5. DOCUMENT WHAT THE DECORATOR DOES
       Clearly explain:
       - What behavior is added
       - What performance impact it has
       - Any side effects
       - Usage examples

    6. FOR PARAMETERIZED DECORATORS, USE FACTORIES
       def decorator_factory(param1, param2):
           def decorator(func):
               @functools.wraps(func)
               def wrapper(*args, **kwargs):
                   ...
               return wrapper
           return decorator

       Usage: @decorator_factory(param1=value)

    7. CONSIDER DECORATOR ORDER
       - @clock above @trace means clock wraps trace
       - Execution order: clock -> trace -> original
       - Be aware of decorator stacking

    8. AVOID MODIFYING FUNCTION SIGNATURE
       - Decorator shouldn't change what parameters function accepts
       - Use *args, **kwargs to be transparent

    9. TEST THAT METADATA IS PRESERVED
       assert decorated_func.__name__ == original_func.__name__
       assert decorated_func.__doc__ == original_func.__doc__

    10. DOCUMENT PERFORMANCE IMPACT
        Decorators add overhead. If significant, document it.
        Consider making timing/tracing optional.
    """)

    # ============ EXAMPLE 11: Common Pitfalls and Solutions
    print("\n" + "=" * 70)
    print("# ============ EXAMPLE 11: Common Pitfalls and Solutions")
    print("Mistakes to avoid:\n")

    print("""
    PITFALL 1: Forgetting functools.wraps
    WRONG:
        def timer(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper

    RIGHT:
        def timer(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper


    PITFALL 2: Not preserving return value
    WRONG:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                func(*args, **kwargs)  # Return value lost!
                return None
            return wrapper

    RIGHT:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)  # Preserve return!
            return wrapper


    PITFALL 3: Changing function signature
    WRONG:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(x):  # Only works for single arg!
                return func(x)
            return wrapper

    RIGHT:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):  # Works for any signature
                return func(*args, **kwargs)
            return wrapper


    PITFALL 4: Swallowing exceptions
    WRONG:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    pass  # Silent failure!
            return wrapper

    RIGHT:
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Error: {e}")
                    raise  # Re-raise the exception!
            return wrapper
    """)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("""
    KEY TAKEAWAYS:

    1. FUNCTOOLS.WRAPS IS ESSENTIAL
       @functools.wraps(func) preserves the original function's metadata.
       Never write a decorator without it!

    2. BASIC PATTERN:
       import functools

       def decorator(func):
           @functools.wraps(func)
           def wrapper(*args, **kwargs):
               # Do something before
               result = func(*args, **kwargs)
               # Do something after
               return result
           return wrapper

    3. WHAT functools.wraps PRESERVES:
       - __name__: Function name
       - __doc__: Docstring
       - __module__: Module name
       - __wrapped__: Original function (for introspection)
       - __annotations__: Type hints
       - __dict__: Custom attributes

    4. USE *args, **kwargs ALWAYS
       Allows decorator to work with any function signature.

    5. ALWAYS RETURN THE RESULT
       return func(*args, **kwargs)

    6. CLOCK DECORATOR EXAMPLE:
       Times function execution and prints:
       - Elapsed time with 8 decimal places
       - Function name
       - All arguments (args and kwargs)
       - Return value

    7. FOR PARAMETERS, USE DECORATOR FACTORIES:
       @decorator_factory(param=value)
       Requires an extra level of nesting.

    8. STACKING DECORATORS:
       @clock
       @trace
       def func():
           ...

       Decorators applied bottom-up.
       clock wraps trace wraps func.

    9. REAL-WORLD USES:
       - Timing and performance monitoring
       - Logging and tracing
       - Authentication and authorization
       - Caching and memoization
       - Input validation
       - Retry logic

    10. REMEMBER:
        - Always use functools.wraps
        - Use *args and **kwargs
        - Return the result
        - Handle exceptions properly
        - Document the decorator's behavior
        - Test that metadata is preserved
    """)
```

---

## Exercises

**Exercise 1.**
Write a `@timer` decorator that measures and prints the execution time of any function. Store the last measured duration as a `last_elapsed` attribute on the wrapper. Use `@wraps` to preserve metadata. Demonstrate it on a function that sorts a large list.

??? success "Solution to Exercise 1"

        import time
        from functools import wraps

        def timer(func):
            """Decorator that measures execution time."""
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                result = func(*args, **kwargs)
                wrapper.last_elapsed = time.perf_counter() - start
                print(f"{func.__name__} took {wrapper.last_elapsed:.4f}s")
                return result
            wrapper.last_elapsed = 0.0
            return wrapper

        @timer
        def sort_numbers(n):
            """Sort a list of n random numbers."""
            import random
            data = [random.randint(0, n) for _ in range(n)]
            return sorted(data)

        sort_numbers(100_000)
        print(f"Last elapsed: {sort_numbers.last_elapsed:.4f}s")

---

**Exercise 2.**
Create a `@retry(max_attempts, delay)` decorator factory that retries a function when it raises an exception. After all attempts are exhausted, re-raise the last exception. Demonstrate it with a function that simulates intermittent `ConnectionError` failures.

??? success "Solution to Exercise 2"

        import time
        from functools import wraps

        def retry(max_attempts=3, delay=1.0):
            """Decorator factory that retries on exception."""
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    last_exc = None
                    for attempt in range(1, max_attempts + 1):
                        try:
                            return func(*args, **kwargs)
                        except Exception as e:
                            last_exc = e
                            if attempt < max_attempts:
                                print(f"Attempt {attempt} failed: {e}. Retrying...")
                                time.sleep(delay)
                    raise last_exc
                return wrapper
            return decorator

        call_count = 0

        @retry(max_attempts=3, delay=0.1)
        def fetch_data():
            global call_count
            call_count += 1
            if call_count < 3:
                raise ConnectionError("Server unreachable")
            return {"status": "ok"}

        result = fetch_data()
        print(result)  # {"status": "ok"}

---

**Exercise 3.**
Write a `@validate_return(expected_type)` decorator factory that checks whether the return value of the decorated function is an instance of `expected_type`. If not, raise a `TypeError` with a descriptive message. Demonstrate it by decorating a function that should return a `dict` but sometimes returns `None`.

??? success "Solution to Exercise 3"

        from functools import wraps

        def validate_return(expected_type):
            """Decorator factory that validates return type."""
            def decorator(func):
                @wraps(func)
                def wrapper(*args, **kwargs):
                    result = func(*args, **kwargs)
                    if not isinstance(result, expected_type):
                        raise TypeError(
                            f"{func.__name__} must return {expected_type.__name__}, "
                            f"got {type(result).__name__}"
                        )
                    return result
                return wrapper
            return decorator

        @validate_return(dict)
        def get_config(use_default=True):
            if use_default:
                return {"debug": False}
            return None  # Bug: should return a dict

        print(get_config())            # {'debug': False}
        try:
            get_config(use_default=False)  # TypeError
        except TypeError as e:
            print(e)
