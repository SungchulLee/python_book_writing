# Docstrings

While type hints describe the structure of data, docstrings describe its **meaning and intent**. A docstring is a string literal placed as the first statement in a function body, documenting what the function does and why.

```python
def celsius_to_fahrenheit(c: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32
```

Python stores the docstring on the function object and makes it available at runtime. Type hints say *what* the types are; the docstring says *why* the function exists and what it does.

!!! tip "Mental Model"
    A docstring is a built-in user manual attached to every function. Python stores it as the `__doc__` attribute, so `help()` can display it at runtime. Type hints tell the reader *what goes in and out*; the docstring tells the reader *why the function exists and how to use it*.

## Single-Line Docstrings

Use a single line for simple functions. The string sits on one line, inside triple quotes:

```python
def square(x: int) -> int:
    """Return the square of x."""
    return x * x

def is_even(n: int) -> bool:
    """Return True if n is even, False otherwise."""
    return n % 2 == 0
```

Write the docstring as an imperative sentence — *"Return ..."*, *"Compute ..."*, *"Check ..."* — not *"Returns ..."* or *"This function returns ..."*.

## Multi-Line Docstrings

Use multiple lines when the function needs more explanation. The first line is a short summary; a blank line separates it from the rest:

```python
def describe_point(x: float, y: float) -> str:
    """Return a formatted string describing a 2D point.

    The output uses the format '(x, y)' with two decimal places.
    Negative coordinates are shown with a minus sign.
    """
    return f"({x:.2f}, {y:.2f})"
```

## Accessing Docstrings

Python stores the docstring in the `__doc__` attribute:

```python
def greet(name: str) -> None:
    """Print a welcome message for the given name."""
    print(f"Welcome, {name}!")

print(greet.__doc__)   # Print a welcome message for the given name.
```

`help()` displays it in a formatted view — useful in an interactive session:

```python
help(greet)
```

Output:

```text
Help on function greet in module __main__:

greet(name: str) -> None
    Print a welcome message for the given name.
```

## Docstrings and Type Hints Together

Type hints and docstrings complement each other. Type hints handle the *what*; the docstring handles the *why* and *how*:

```python
def calculate_bmi(weight: float, height: float) -> float:
    """Return the Body Mass Index for the given weight and height.

    weight is in kilograms, height is in metres.
    A result below 18.5 is underweight; above 25.0 is overweight.
    """
    return weight / height ** 2
```

The type hints tell a reader (and static analysis tools) that both arguments are floats. The docstring explains the units and what the result means — information that types alone cannot convey.

## Key Ideas

A docstring is the first string in a function body. It is stored on `__doc__` and displayed by `help()`.
Single-line docstrings suit simple functions; multi-line docstrings add detail when needed.
Write docstrings as imperative sentences and use them to explain intent, units, and constraints — the things type hints cannot express.

---

## Exercises

**Exercise 1.**
A programmer writes three different forms of documentation:

```python
def version_a(x):
    # Return the square of x
    return x * x

def version_b(x):
    """Return the square of x."""
    return x * x

def version_c(x):
    return x * x  # Return the square of x
```

For each version, what does `func.__doc__` return? Which form is accessible at runtime, and why? What makes a docstring fundamentally different from a comment?

??? success "Solution to Exercise 1"
    - `version_a.__doc__` returns `None` -- the comment `# Return the square of x` is stripped by the parser and has no runtime existence.
    - `version_b.__doc__` returns `"Return the square of x."` -- the string literal as the first statement is stored as the docstring.
    - `version_c.__doc__` returns `None` -- the comment after `return` is not a docstring; `return x * x` is the first statement, and it is not a string literal.

    A docstring is fundamentally different from a comment because it is a **string object** stored in memory at runtime, accessible via `__doc__` and `help()`. A comment is text for the human reader of the source code -- it is completely removed during parsing and has zero runtime existence. Docstrings bridge the gap between source code and runtime introspection.

---

**Exercise 2.**
Docstrings can contain additional sections. Explain the purpose of each section in this multi-line docstring:

```python
def connect(host: str, port: int, timeout: float = 30.0) -> bool:
    """Establish a TCP connection to the given host and port.

    Args:
        host: The hostname or IP address.
        port: The port number (1-65535).
        timeout: Maximum seconds to wait. Defaults to 30.

    Returns:
        True if the connection succeeds, False otherwise.

    Raises:
        ValueError: If port is out of range.
    """
    ...
```

Why is this level of documentation useful even when type hints are present? What information does the docstring provide that type hints cannot?

??? success "Solution to Exercise 2"
    - **Summary line** ("Establish a TCP connection..."): a one-sentence description, readable in `help()` listings.
    - **Args**: documents each parameter's meaning, constraints (port range), and defaults. Type hints say `port: int` but not "must be 1-65535."
    - **Returns**: describes the meaning of the return value. `-> bool` says the type, but not that `True` means success.
    - **Raises**: lists exceptions the function may raise and when. This information cannot be expressed in type hints at all.

    Type hints and docstrings serve complementary roles: hints express **types** (machine-readable), docstrings express **semantics** (human-readable). The docstring explains units, valid ranges, default behaviors, error conditions, and the relationship between inputs and outputs -- none of which type hints can convey.

---

**Exercise 3.**
Python stores docstrings on `__doc__`, but they can also be overwritten. Predict the output:

```python
def greet():
    """Say hello."""
    print("Hello!")

print(greet.__doc__)
greet.__doc__ = "Modified docstring"
print(greet.__doc__)
help(greet)
```

Why does Python allow modifying `__doc__`? Is the docstring part of the function's code, or part of its metadata?

??? success "Solution to Exercise 3"
    Output:

    ```text
    Say hello.
    Modified docstring
    ```

    Then `help(greet)` displays `Modified docstring` as the documentation.

    Python allows modifying `__doc__` because the docstring is **metadata** stored as an attribute on the function object -- it is not part of the compiled bytecode. Functions are objects, and `__doc__` is just one of their attributes (like `__name__`, `__module__`, etc.).

    This can be useful in practice: decorators sometimes modify `__doc__` to combine the wrapper's documentation with the original function's documentation. `functools.wraps` preserves the original `__doc__` when wrapping a function.

Next: [Runtime Model (Call Stack)](call_stack.md).
