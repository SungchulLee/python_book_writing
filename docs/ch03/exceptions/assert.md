# assert Statement

The `assert` statement is a debugging aid that tests a condition and raises `AssertionError` if the condition is `False`. It helps verify assumptions during development.

!!! tip "Mental Model"
    An `assert` is a contract with your future self: "at this point in the code, this condition must be true." It is a development-time safety net, not a runtime error handler. Python silently removes all `assert` statements when you run with `-O` (optimize), so never use them for input validation or security checks.

## Basic Syntax

```python
assert condition, message
```

- `condition`: Expression that should evaluate to `True`
- `message`: Optional error message if assertion fails

```python
x = 10
assert x > 0, "x must be positive"  # Passes silently

y = -5
assert y > 0, "y must be positive"  # Raises AssertionError
```


## Simple Assertions

Assertions without a message raise a bare `AssertionError`.

```python
x = 5
assert x == 5      # Passes
assert x == 10     # AssertionError
```


## Assertions with Messages

Provide context when the assertion fails.

```python
def divide(a, b):
    assert b != 0, "Division by zero is not allowed"
    return a / b

result = divide(10, 2)
print(result)  # 5.0

result = divide(10, 0)  # AssertionError: Division by zero is not allowed
```


## Practical Example

Validate function inputs during development.

```python
def calculate_average(numbers):
    assert len(numbers) > 0, "List cannot be empty"
    assert all(isinstance(n, (int, float)) for n in numbers), \
        "All elements must be numbers"
    return sum(numbers) / len(numbers)

print(calculate_average([1, 2, 3, 4, 5]))  # 3.0
print(calculate_average([]))  # AssertionError: List cannot be empty
```


## Assert vs Exception Handling

Use `assert` for debugging, not for production error handling.

```python
# Good: assert for internal consistency checks
def process_data(data):
    assert data is not None, "Bug: data should never be None here"
    # ... processing logic

# Bad: assert for user input validation
def get_age(age):
    assert age > 0  # Don't do this!
    return age

# Good: exceptions for user input validation
def get_age(age):
    if age <= 0:
        raise ValueError("Age must be positive")
    return age
```


## When to Use assert

**Do use assert for:**

- Internal consistency checks
- Verifying programmer assumptions
- Development and testing
- Documenting invariants

**Don't use assert for:**

- Validating user input
- Checking conditions that might legitimately fail
- Production error handling
- Security checks


## Assertions Can Be Disabled

Assertions are removed when Python runs with optimization (`-O` flag).

```bash
python -O script.py  # Assertions are ignored
```

This is why you should never use `assert` for critical checks.

```python
# WRONG: Security check with assert
assert user.is_authenticated, "User must be logged in"

# CORRECT: Proper security check
if not user.is_authenticated:
    raise PermissionError("User must be logged in")
```


## Multiple Conditions

Check multiple conditions in one assertion.

```python
def set_coordinates(x, y):
    assert 0 <= x <= 100 and 0 <= y <= 100, \
        f"Coordinates ({x}, {y}) out of bounds"
    print(f"Position set to ({x}, {y})")

set_coordinates(50, 50)   # Position set to (50, 50)
set_coordinates(150, 50)  # AssertionError: Coordinates (150, 50) out of bounds
```

---

## Exercises


**Exercise 1.**
Write a function `calculate_average(numbers)` that uses `assert` to ensure the input list is not empty before computing the average. Test it with both a valid list and an empty list.

??? success "Solution to Exercise 1"

        ```python
        def calculate_average(numbers):
            assert len(numbers) > 0, "Cannot compute average of empty list"
            return sum(numbers) / len(numbers)

        print(calculate_average([10, 20, 30]))  # 20.0

        try:
            calculate_average([])
        except AssertionError as e:
            print(f"Error: {e}")  # Cannot compute average of empty list
        ```

    The `assert` statement raises `AssertionError` with the custom message when the condition is `False`.

---

**Exercise 2.**
Explain why `assert` should not be used for input validation in production code. What happens when Python is run with the `-O` (optimize) flag?

??? success "Solution to Exercise 2"

    `assert` statements are removed entirely when Python is run with `-O` (optimize) flag:

        ```bash
        python -O script.py
        ```

    This means any validation done via `assert` will be silently skipped in optimized mode. For input validation, always use explicit `if`/`raise`:

        ```python
        # Bad: silently skipped with -O
        assert user_input > 0

        # Good: always runs
        if user_input <= 0:
            raise ValueError("Input must be positive")
        ```

    Use `assert` only for internal consistency checks during development, not for validating external input.

---

**Exercise 3.**
Write a function `validate_age(age)` that uses `assert` with a custom error message to check that `age` is between 0 and 150. Then rewrite it using a proper `if`/`raise` pattern that works even with optimization enabled.

??? success "Solution to Exercise 3"

        ```python
        # Using assert (development only)
        def validate_age_assert(age):
            assert 0 <= age <= 150, f"Invalid age: {age}"
            return age

        # Using if/raise (production safe)
        def validate_age(age):
            if not (0 <= age <= 150):
                raise ValueError(f"Invalid age: {age}")
            return age

        print(validate_age(25))  # 25

        try:
            validate_age(-5)
        except ValueError as e:
            print(f"Error: {e}")  # Invalid age: -5
        ```

    The `if`/`raise` version works regardless of optimization flags and raises a more appropriate `ValueError` instead of `AssertionError`.
