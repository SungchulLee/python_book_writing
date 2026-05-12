# Code Quality

Best practices for writing correct, maintainable, and well-styled Python code.

!!! tip "Mental Model"
    Good Python code makes the object model work for you rather than against you. Use immutable defaults, compare with `==` instead of `is`, and let Python's built-in idioms (context managers, unpacking, comprehensions) express intent clearly. Correctness comes from respecting how names, scopes, and mutability actually behave.

## Correctness

### Avoid Mutable Default Arguments

```python
# WRONG: Default list is shared between calls
def add_item(item, lst=[]):
    lst.append(item)
    return lst

# RIGHT: Use None as default
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### Fix Late Binding in Closures

```python
# WRONG: All functions return the last value of i
funcs = [lambda: i for i in range(3)]

# RIGHT: Capture i as default argument
funcs = [lambda x=i: x for i in range(3)]
```

### Use `is` Correctly

```python
# WRONG: Using is for value comparison
if x is 1000:  # May fail!
    pass

# RIGHT: Use == for values
if x == 1000:
    pass

# RIGHT: Use is for None, True, False
if result is None:
    pass
```

### Handle Exceptions Properly

```python
# WRONG: Bare except catches everything
try:
    risky_operation()
except:
    pass

# RIGHT: Catch specific exceptions
try:
    risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
except (TypeError, KeyError) as e:
    logger.error(f"Type or key error: {e}")
```

### Write Tests

```python
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_negative_numbers(self):
        self.assertEqual(add(-1, -1), -2)
    
    def test_mixed_numbers(self):
        self.assertEqual(add(-1, 1), 0)

if __name__ == '__main__':
    unittest.main()
```

---

## Maintainability

### Use Descriptive Names

```python
# BAD: Cryptic names
def p(d, n):
    return d * (1 + r) ** n

# GOOD: Clear, descriptive names
def calculate_compound_interest(principal, years, rate=0.05):
    return principal * (1 + rate) ** years

# BAD: Single-letter variables
n = len(users)

# GOOD: Meaningful names
user_count = len(users)
active_user_count = len([u for u in users if u.is_active])
```

### Keep Functions Small

```python
# BAD: One function doing too much
def process_user_data(user):
    # Validate
    if not user.email:
        raise ValueError("No email")
    # Transform
    user.name = user.name.title()
    # Save
    db.save(user)
    # Notify
    send_email(user.email, "Welcome!")

# GOOD: Single responsibility
def validate_user(user):
    if not user.email:
        raise ValueError("No email")

def normalize_user(user):
    user.name = user.name.title()

def save_user(user):
    db.save(user)

def notify_user(user):
    send_email(user.email, "Welcome!")

def process_user(user):
    validate_user(user)
    normalize_user(user)
    save_user(user)
    notify_user(user)
```

### Write Docstrings

```python
def calculate_discount(price, discount_percent):
    """
    Calculate the discounted price.
    
    Args:
        price: Original price in dollars.
        discount_percent: Discount percentage (0-100).
    
    Returns:
        The discounted price.
    
    Raises:
        ValueError: If discount_percent is not between 0 and 100.
    
    Example:
        >>> calculate_discount(100, 20)
        80.0
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount must be between 0 and 100")
    return price * (1 - discount_percent / 100)
```

### Use Type Hints

```python
from typing import List, Optional, Dict

def find_user(user_id: int) -> Optional[Dict[str, str]]:
    """Find user by ID, return None if not found."""
    pass

def get_active_users(users: List[Dict]) -> List[Dict]:
    """Filter and return only active users."""
    return [u for u in users if u.get('active')]
```

---

## Style Guide (PEP 8)

### Naming Conventions

```python
# Variables and functions: snake_case
user_name = "Alice"
def calculate_total():
    pass

# Classes: PascalCase
class UserAccount:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# Private: leading underscore
_internal_cache = {}
def _helper_function():
    pass

# "Private" (name mangling): double underscore
class MyClass:
    def __init__(self):
        self.__private_attr = 42
```

### Spacing and Formatting

```python
# Spaces around operators
x = 1 + 2
y = x * 3

# No space before colon in slices
items[1:3]
items[::2]

# Spaces after commas
func(a, b, c)
data = [1, 2, 3]

# Two blank lines between top-level definitions
def function_one():
    pass


def function_two():
    pass


class MyClass:
    pass
```

### Import Organization

```python
# Standard library imports
import os
import sys
from collections import defaultdict

# Third-party imports
import numpy as np
import pandas as pd

# Local imports
from mypackage import mymodule
from mypackage.utils import helper
```

### Line Length

```python
# Keep lines under 79-88 characters
# Break long lines appropriately

# Long function call
result = some_function(
    argument_one,
    argument_two,
    argument_three,
)

# Long string
message = (
    "This is a very long message that needs to be "
    "split across multiple lines for readability."
)

# Long condition
if (condition_one
        and condition_two
        and condition_three):
    do_something()
```

---

## Code Review Checklist

### Correctness
- [ ] No mutable default arguments
- [ ] Closures capture variables correctly
- [ ] Exceptions handled appropriately
- [ ] Edge cases considered
- [ ] Tests written and passing

### Maintainability
- [ ] Functions are small and focused
- [ ] Names are descriptive
- [ ] Docstrings present for public APIs
- [ ] Type hints used where helpful
- [ ] No code duplication

### Style
- [ ] Follows PEP 8 conventions
- [ ] Imports organized properly
- [ ] Consistent formatting
- [ ] Line length reasonable
- [ ] Comments explain "why", not "what"

---

## Summary

| Aspect | Key Points |
|--------|------------|
| Correctness | Avoid mutable defaults, fix late binding, handle exceptions |
| Maintainability | Descriptive names, small functions, good documentation |
| Style | Follow PEP 8, consistent formatting, organized imports |

Key principles:

- Code is read more than written--optimize for readability
- Test your code thoroughly
- Follow established conventions
- Keep functions focused and small
- Document public APIs

---

## Exercises

**Exercise 1.**
Mutable default arguments are a common source of bugs. Predict the output:

```python
def add_item(item, lst=[]):
    lst.append(item)
    return lst

r1 = add_item("a")
r2 = add_item("b")
r3 = add_item("c", [])

print(r1)
print(r2)
print(r3)
print(r1 is r2)
```

Why does `r2` contain both `"a"` and `"b"`? Why is `r1 is r2` `True`? Write the corrected version of this function.

??? success "Solution to Exercise 1"
    Output:

    ```text
    ['a', 'b']
    ['a', 'b']
    ['c']
    True
    ```

    The default argument `lst=[]` is evaluated **once** at function definition time, not on each call. Every call that uses the default shares the **same list object**. `add_item("a")` appends to this shared list, and `add_item("b")` appends to the same list. `r1` and `r2` are the same object (`r1 is r2` is `True`).

    `r3` gets a fresh list because `[]` was passed explicitly, bypassing the default.

    Corrected version:

    ```python
    def add_item(item, lst=None):
        if lst is None:
            lst = []
        lst.append(item)
        return lst
    ```

    Using `None` as a sentinel and creating a new list inside the function body ensures each call gets its own list.

---

**Exercise 2.**
Late binding in closures created inside loops is a classic Python pitfall. Predict the output:

```python
funcs = [lambda: i for i in range(4)]
print([f() for f in funcs])

funcs2 = [lambda i=i: i for i in range(4)]
print([f() for f in funcs2])
```

Why do all functions in `funcs` return `3`? How does the default argument trick in `funcs2` fix the problem? What is the underlying mechanism?

??? success "Solution to Exercise 2"
    Output:

    ```text
    [3, 3, 3, 3]
    [0, 1, 2, 3]
    ```

    All lambdas in `funcs` capture the **variable** `i` by reference, not its value. By the time any lambda is called, the loop has finished and `i` is `3`. All four functions look up the same `i` and find `3`.

    `lambda i=i: i` fixes this by capturing the **current value** of `i` as a default argument. Default arguments are evaluated at function definition time (during each loop iteration), so each lambda gets a snapshot: `i=0`, `i=1`, `i=2`, `i=3`.

    The underlying mechanism: closures hold references to **cell objects** (shared mutable containers), while default arguments store **values** directly in the function object's `__defaults__` tuple.

---

**Exercise 3.**
Exception handling has subtleties around variable scope. Predict the output:

```python
try:
    x = 1 / 0
except ZeroDivisionError as e:
    error = e
    print(type(error))

try:
    print(e)
except NameError:
    print("e is gone")

print(error)
```

Why is `e` deleted after the `except` block but `error` survives? What Python design decision explains this behavior?

??? success "Solution to Exercise 3"
    Output:

    ```text
    <class 'ZeroDivisionError'>
    e is gone
    division by zero
    ```

    Python **deletes** the exception variable `e` at the end of the `except` block. This is by design (PEP 3110): exception objects hold references to the traceback, which holds references to all local variables in the stack frames. If `e` survived, it would create a reference cycle preventing garbage collection of those frames.

    However, `error = e` creates a separate binding to the same exception object. Since `error` is a normal variable (not the `as` target), Python does not delete it. The exception object itself survives as long as `error` references it.

    This is equivalent to Python implicitly running `del e` at the end of the `except` block.
