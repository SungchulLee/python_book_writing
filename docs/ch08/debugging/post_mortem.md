# Post-Mortem Debugging

Debug a program after it crashes using post-mortem debugging.

!!! tip "Mental Model"
    Post-mortem debugging is an autopsy for crashed programs. Instead of adding breakpoints and re-running, you examine the program's state at the exact moment it died — the exception, the call stack, and every local variable in each frame. It is invaluable when a bug is hard to reproduce or occurs deep in a call chain.

## Post-Mortem Debugging with pdb

Debug exceptions after they occur.

```python
import pdb
import traceback

def buggy_function():
    x = 10
    y = 0
    return x / y  # This will raise ZeroDivisionError

try:
    result = buggy_function()
except Exception:
    # Start debugging at the point of exception
    traceback.print_exc()
    pdb.post_mortem()
    # Now you can inspect the call stack and variables
```

```
Traceback (most recent call last):
  File "script.py", line 9, in <module>
    result = buggy_function()
  File "script.py", line 5, in buggy_function
    return x / y
ZeroDivisionError: division by zero
```

## Debugging Exceptions

Inspect exceptions and their context.

```python
import sys
import pdb

def analyze_error():
    items = [1, 2, 3]
    try:
        result = items[10]  # IndexError
    except IndexError:
        # Get exception info
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(f"Exception: {exc_type.__name__}")
        print(f"Message: {exc_value}")
        print(f"Traceback present: {exc_tb is not None}")
        
        # Use traceback to understand the error
        import traceback
        traceback.print_tb(exc_tb)

analyze_error()
```

```
Exception: IndexError
Message: list index out of range
Traceback present: True
```

---

## Exercises

**Exercise 1.**
Write a function `safe_divide_all` that takes a list of `(numerator, denominator)` tuples and returns a list of results. Use a try/except block to catch `ZeroDivisionError`. In the except block, use `sys.exc_info()` to capture and print the exception type and message, then append `None` for that entry. For example, `safe_divide_all([(10, 2), (5, 0), (8, 4)])` should return `[5.0, None, 2.0]`.

??? success "Solution to Exercise 1"

    ```python
    import sys

    def safe_divide_all(pairs):
        results = []
        for num, denom in pairs:
            try:
                results.append(num / denom)
            except ZeroDivisionError:
                exc_type, exc_value, _ = sys.exc_info()
                print(f"{exc_type.__name__}: {exc_value}")
                results.append(None)
        return results

    # Test
    result = safe_divide_all([(10, 2), (5, 0), (8, 4)])
    print(result)  # [5.0, None, 2.0]
    ```

---

**Exercise 2.**
Write a function `debug_key_access` that takes a dictionary and a list of keys, and returns the values for those keys. Use a try/except around each key access. If a `KeyError` occurs, use `traceback.format_exc()` to capture the traceback as a string and add it to an errors list. Return both the values and the errors.

??? success "Solution to Exercise 2"

    ```python
    import traceback

    def debug_key_access(data, keys):
        values = []
        errors = []
        for key in keys:
            try:
                values.append(data[key])
            except KeyError:
                tb_str = traceback.format_exc()
                errors.append(tb_str)
                values.append(None)
        return values, errors

    # Test
    d = {"a": 1, "b": 2}
    values, errors = debug_key_access(d, ["a", "c", "b"])
    print(values)  # [1, None, 2]
    print(f"Errors found: {len(errors)}")  # 1
    ```

---

**Exercise 3.**
Write a decorator `post_mortem_on_error` that wraps a function so that if it raises any exception, the decorator prints the full traceback using `traceback.print_exc()` and returns `None` instead of crashing. Apply it to a function that deliberately raises a `ValueError`.

??? success "Solution to Exercise 3"

    ```python
    import traceback

    def post_mortem_on_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                traceback.print_exc()
                return None
        return wrapper

    @post_mortem_on_error
    def risky_function(x):
        if x < 0:
            raise ValueError(f"Negative value: {x}")
        return x ** 2

    # Test
    print(risky_function(5))   # 25
    print(risky_function(-3))  # Prints traceback, returns None
    ```
