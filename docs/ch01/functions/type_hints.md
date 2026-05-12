# Type Hints

Type hints define a function's expected interface, forming a contract between the function and its callers. They make the expected types of inputs and outputs explicit.

!!! tip "Mental Model"
    Type hints are labels on a function's inputs and outputs. Python does not enforce them at runtime---they are documentation that tools like `mypy` can check statically. Think of them as a contract: "I expect a `float` in and promise a `float` out." They make code self-documenting and catch type mismatches before the program runs.

## The Problem

Consider this function:

```python
def area(length, width):
    return length * width
```

What types are `length` and `width`?
Are they integers, floats, or something else?

Without additional context, the reader cannot tell.

## The Solution

Type hints make the expected types explicit.

```python
def area(length: float, width: float) -> float:
    return length * width
```

A reader can immediately see the intended types.

## Syntax

Type hints appear after parameter names and after the function arrow.

```python
def add(a: int, b: int) -> int:
    return a + b
```

Here:

- `a: int` means `a` should be an integer
- `b: int` means `b` should be an integer
- `-> int` means the function returns an integer

A slightly richer example:

```python
def average(a: float, b: float) -> float:
    return (a + b) / 2

result = average(3.0, 7.0)
print(result)
```

Output

```text
5.0
```

## Returning None

Functions that do not return a value can be annotated with `-> None`.

```python
def greet(name: str) -> None:
    print("Welcome,", name)
```

This tells the reader — and any analysis tool — that `greet` is called for its side effect (printing), not for a return value.

## Type Hints Are Optional

Python does **not enforce type hints at runtime**.

This means the following will still run without error:

```python
def add(a: int, b: int) -> int:
    return a + b

print(add("2", "3"))
```

Output

```text
23
```

The function was annotated for `int`, but Python happily accepted two strings and concatenated them.
The result `"23"` is valid Python but almost certainly not what the caller intended.

Static analysis tools such as mypy or pyright can examine the code without running it and warn about mismatches like this before they cause bugs.

## Key Ideas

Type hints document the expected types of parameters (`: type`) and return values (`-> type`).
Python does not enforce them at runtime, but they make code easier to read and allow static analysis tools to catch type errors early.
For functions that only perform side effects and return nothing, use `-> None`.

---



---

## Notebook Examples

```python
def celsius_to_fahrenheit(c: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32

print(help(celsius_to_fahrenheit))
```

```python
def convert_celsius_to_fahrenheit(c: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return (c * 9 / 5) + 32

print(help(convert_celsius_to_fahrenheit))
```

---

## Exercises

**Exercise 1.**
Type hints are NOT enforced at runtime. Predict the output:

```python
def add(a: int, b: int) -> int:
    return a + b

print(add(3, 4))
print(add("hello", " world"))
print(add([1], [2]))
```

All three calls succeed. Why does Python not enforce type hints? What tool would catch the last two calls as errors? What is the benefit of type hints if they are not enforced?

??? success "Solution to Exercise 1"
    Output:

    ```text
    7
    hello world
    [1, 2]
    ```

    All three succeed because Python ignores type hints at runtime. The hints are **metadata** stored on the function object (`add.__annotations__`), but Python's interpreter does not check them when the function is called.

    A **static type checker** like `mypy` or `pyright` would flag the last two calls as errors: `add("hello", " world")` passes `str` where `int` is expected.

    The benefits of type hints without enforcement:

    1. **Documentation**: readers immediately see expected types.
    2. **IDE support**: autocompletion, refactoring, and inline error highlighting.
    3. **Static analysis**: tools catch type errors before runtime, during development.
    4. **Gradual adoption**: existing code works without changes; hints can be added incrementally.

---

**Exercise 2.**
A programmer annotates a function incorrectly:

```python
def divide(a: int, b: int) -> int:
    return a / b

result = divide(7, 2)
print(result, type(result))
```

What does the function actually return? Does the type hint `-> int` change the return type? What should the correct annotation be?

??? success "Solution to Exercise 2"
    Output:

    ```text
    3.5 <class 'float'>
    ```

    The `/` operator always returns `float` in Python 3, regardless of the operand types. The type hint `-> int` does NOT change the actual return type -- it is just a claim by the programmer, and in this case, the claim is **wrong**.

    The correct annotation should be `-> float`:

    ```python
    def divide(a: int, b: int) -> float:
        return a / b
    ```

    Or, if integer division is intended:

    ```python
    def divide(a: int, b: int) -> int:
        return a // b
    ```

    This illustrates an important point: type hints are only as correct as the programmer makes them. A wrong hint is worse than no hint because it misleads readers and tools.

---

**Exercise 3.**
Type hints can express complex types using `typing` module constructs. Explain what each annotation means:

```python
from typing import Optional, Union

def find(items: list[int], target: int) -> Optional[int]:
    ...

def process(value: Union[str, int]) -> str:
    ...

def transform(data: list[tuple[str, int]]) -> dict[str, int]:
    ...
```

What is the difference between `Optional[int]` and `Union[int, None]`? Why is expressing these types in hints useful even though Python does not check them?

??? success "Solution to Exercise 3"

    - `find(items: list[int], target: int) -> Optional[int]`: takes a list of integers and an integer target. Returns either an `int` (the found value/index) or `None` (if not found).

    - `process(value: Union[str, int]) -> str`: accepts either a string or an integer. Returns a string.

    - `transform(data: list[tuple[str, int]]) -> dict[str, int]`: takes a list of (string, integer) tuples. Returns a dictionary mapping strings to integers.

    `Optional[int]` is exactly equivalent to `Union[int, None]` -- it means "int or None." `Optional` is just syntactic sugar for the common pattern of "this value might be None." In Python 3.10+, you can write `int | None` instead.

    Expressing these types is useful because it communicates the **contract** of the function: what it accepts and what it returns, including edge cases like `None`. This helps other developers use the function correctly and helps static analysis tools verify that callers handle all possible return types (e.g., checking for `None` before using the result).

Next: [Docstrings](docstrings.md).
