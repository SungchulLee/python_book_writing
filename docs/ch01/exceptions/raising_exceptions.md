
# Raising Exceptions

Raising exceptions defines the **contract** of a function. It specifies what inputs are valid, what conditions are unacceptable, and how violations are communicated to the caller. Instead of returning error codes, functions raise exceptions to signal failure clearly.

Python programs can **raise exceptions explicitly** using the `raise` statement.

```mermaid
flowchart LR
    A[Function detects problem]
    A --> B[raise exception]
    B --> C[Caller handles exception]
````

!!! tip "Mental Model"
    `raise` is how a function says "I cannot do what you asked." Instead of returning a special error value that callers might ignore, raising an exception forces the issue---execution stops immediately and unwinds the call stack until something handles it. This makes failures impossible to silently overlook.

---

## 1. Basic raise

```python
raise ValueError("Invalid value")
```

This immediately stops execution and raises the specified exception.

---

## 2. Raising Exceptions in Functions

```python
def divide(a, b):
    if b == 0:
        raise ValueError("b cannot be zero")
    return a / b
```

Example:

```python
print(divide(10, 2))
print(divide(10, 0))
```

---

## 3. Custom Error Checking

Raising exceptions helps enforce constraints.

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds")
    return balance - amount
```

---

## 4. Re-raising Exceptions

Sometimes a function catches an exception but wants to propagate it upward.

```python
try:
    x = int("abc")
except ValueError:
    print("Conversion error")
    raise
```

This re-raises the same exception.

---

## 5. Custom Exception Classes

Programs may define their own exception types.

```python
class NegativeNumberError(Exception):
    pass
```

Example:

```python
def sqrt(x):
    if x < 0:
        raise NegativeNumberError("Negative value")
```

Custom exceptions help express domain-specific errors.

---

## 6. Worked Examples

### Example 1

```python
def check_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative")
```

### Example 2

```python
def temperature(c):
    if c < -273.15:
        raise ValueError("Below absolute zero")
```

---

## 7. When to Raise Exceptions

Raising exceptions is appropriate when:

* inputs violate assumptions
* an operation cannot be completed
* continuing would produce incorrect results

Do **not** raise exceptions for normal control flow---use `if/else` or `return` instead.

---


## 8. Summary

Key ideas:

* `raise` explicitly signals errors
* functions can validate inputs and raise exceptions
* exceptions propagate up the call stack
* custom exception classes can represent domain-specific problems

Raising exceptions allows programs to enforce correctness and communicate errors clearly.

---

## Putting It Together

Exceptions provide a complete system for handling failure:

- exception types describe **what went wrong**
- `try/except` defines **how to respond**
- `raise` communicates **failure to callers**

Together, control flow and exceptions describe all possible execution paths in a program: what happens when operations succeed, and what happens when they fail.


## Exercises

**Exercise 1.**
A programmer raises `ValueError` for invalid input but is unsure when to use `TypeError` instead. For each scenario, state which exception is more appropriate and why:

```python
def set_age(age):
    # age is "hello" -- should this raise TypeError or ValueError?
    # age is -5 -- should this raise TypeError or ValueError?
    # age is [25] -- should this raise TypeError or ValueError?
    pass
```

??? success "Solution to Exercise 1"
    - `age = "hello"`: **`TypeError`**. The type is wrong -- `set_age` expects a number, not a string. No string value could be a valid age.
    - `age = -5`: **`ValueError`**. The type is correct (integer), but the specific value is invalid (ages cannot be negative).
    - `age = [25]`: **`TypeError`**. A list is the wrong type for an age parameter, regardless of its contents.

    The rule: `TypeError` means "this type of object is fundamentally incompatible with this operation." `ValueError` means "this type is correct, but this particular value is outside the valid range."

    In practice:

    ```python
    def set_age(age):
        if not isinstance(age, (int, float)):
            raise TypeError(f"Expected number, got {type(age).__name__}")
        if age < 0 or age > 150:
            raise ValueError(f"Age must be 0-150, got {age}")
    ```

---

**Exercise 2.**
The bare `raise` re-raises the current exception. Predict the output:

```python
def process():
    try:
        return int("hello")
    except ValueError:
        print("Logging error...")
        raise

try:
    process()
except ValueError as e:
    print(f"Caught: {e}")
```

Why is `raise` (without arguments) preferable to `raise ValueError(...)` in the `except` block? What information would be lost if you raised a new exception instead?

??? success "Solution to Exercise 2"
    Output:

    ```text
    Logging error...
    Caught: invalid literal for int() with base 10: 'hello'
    ```

    Bare `raise` re-raises the **exact same exception object**, preserving the original traceback. If you instead wrote `raise ValueError("conversion failed")`, you would create a new exception object with a new traceback -- the original location of the error (inside `int()`) would be lost.

    Bare `raise` is preferable in "catch, log, re-raise" patterns because:
    1. The original traceback is preserved, showing where the error actually occurred.
    2. The original error message is preserved.
    3. Any custom attributes on the original exception are preserved.

    Python 3 also supports `raise NewError() from original_error` for exception chaining, which preserves the original exception as the `__cause__` of the new one.

---

**Exercise 3.**
Custom exceptions help organize error handling. Explain why this pattern is useful:

```python
class AppError(Exception):
    pass

class DatabaseError(AppError):
    pass

class AuthError(AppError):
    pass
```

How does this hierarchy let a caller handle all application errors with one `except` clause while still being able to handle specific errors differently? What advantage does this have over raising built-in exceptions like `RuntimeError`?

??? success "Solution to Exercise 3"
    The hierarchy lets callers choose their level of specificity:

    ```python
    # Handle all application errors the same way
    try:
        do_something()
    except AppError:
        print("Application error occurred")

    # Handle specific errors differently
    try:
        do_something()
    except DatabaseError:
        print("Database problem -- retry")
    except AuthError:
        print("Authentication failed -- re-login")
    except AppError:
        print("Other application error")
    ```

    `except AppError` catches `DatabaseError` and `AuthError` (because they inherit from `AppError`), but the more specific `except` clauses handle them individually when listed first.

    Advantages over using built-in exceptions like `RuntimeError`:
    1. **Clarity**: `except DatabaseError` is self-documenting; `except RuntimeError` could mean anything.
    2. **Specificity**: you can catch only your application's errors without accidentally catching unrelated `RuntimeError`s from libraries.
    3. **Organization**: the hierarchy mirrors your application's error categories, making error handling logic match your domain model.
