# pytest Basics

Introduction to pytest, a simpler and more powerful testing framework.

!!! tip "Mental Model"
    pytest strips testing down to plain `assert` statements and free functions — no class boilerplate, no `self.assertEqual`. Write a function whose name starts with `test_`, use `assert` to check results, and run `pytest`. Its automatic test discovery, rich failure messages, and plugin ecosystem make it the de facto standard for Python testing.

## Simple pytest Tests

Write tests without unittest boilerplate.

```python
# test_math.py - pytest style
def add(a, b):
    return a + b

def test_addition():
    assert add(2, 3) == 5

def test_negative():
    assert add(-1, 1) == 0

def test_string_concat():
    assert add("hello", " world") == "hello world"

# Run with: pytest test_math.py -v
```

```
test_math.py::test_addition PASSED
test_math.py::test_negative PASSED
test_math.py::test_string_concat PASSED
```

## pytest Markers and Organization

Organize tests with markers and fixtures.

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    import time
    time.sleep(0.1)
    assert True

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0)
])
def test_add(a, b, expected):
    assert a + b == expected

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

# Run with: pytest -v -m "not slow"
print("pytest organization example")
```

```
pytest organization example
```

---

## Runnable Example: `pytest_basics_tutorial.py`

```python
"""
08_pytest_basics.py - Introduction to pytest
===========================================
Modern, powerful testing with pytest framework.
"""
# pytest uses simple functions, not classes (though classes work too)
# No need to import unittest or inherit from TestCase

# =============================================================================
# Definitions
# =============================================================================

def add(a, b):
    """Add two numbers."""
    return a + b

def test_add_positive_numbers():
    """Test adding positive numbers."""
    assert add(2, 3) == 5

def test_add_negative_numbers():
    """Test adding negative numbers."""
    assert add(-1, -1) == -2

def test_add_zero():
    """Test adding zero."""
    assert add(5, 0) == 5

# pytest provides better assertion introspection than unittest
def test_list_operations():
    """pytest shows detailed failure information."""
    my_list = [1, 2, 3]
    assert 3 in my_list
    assert len(my_list) == 3

def test_dict_operations():
    """Test dictionary operations."""
    my_dict = {'name': 'Alice', 'age': 30}
    assert my_dict['name'] == 'Alice'
    assert 'age' in my_dict

# pytest fixtures (simple version)
import pytest


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    @pytest.fixture
    def sample_list():
        """Fixture that provides a sample list."""
        return [1, 2, 3, 4, 5]

    def test_with_fixture(sample_list):
        """Test using a fixture."""
        assert len(sample_list) == 5
        assert sum(sample_list) == 15

    # Testing exceptions with pytest
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def test_divide_by_zero():
        """Test that division by zero raises ValueError."""
        with pytest.raises(ValueError):
            divide(10, 0)

    def test_divide_by_zero_message():
        """Test exception message."""
        with pytest.raises(ValueError, match="Cannot divide"):
            divide(10, 0)

    # Run with: pytest 08_pytest_basics.py -v
```

---

## Exercises

**Exercise 1.** Write a function `fizzbuzz(n)` that returns `"Fizz"` if `n` is divisible by 3, `"Buzz"` if divisible by 5, `"FizzBuzz"` if divisible by both, and `str(n)` otherwise. Write pytest tests for all four cases.

??? success "Solution to Exercise 1"
    ```python
    def fizzbuzz(n):
        if n % 15 == 0:
            return "FizzBuzz"
        if n % 3 == 0:
            return "Fizz"
        if n % 5 == 0:
            return "Buzz"
        return str(n)

    def test_fizz():
        assert fizzbuzz(9) == "Fizz"

    def test_buzz():
        assert fizzbuzz(10) == "Buzz"

    def test_fizzbuzz():
        assert fizzbuzz(15) == "FizzBuzz"

    def test_number():
        assert fizzbuzz(7) == "7"
    ```

---

**Exercise 2.** Predict the output of running `pytest -v` on this file:

```python
def test_truthy():
    assert [1, 2, 3]

def test_falsy():
    assert []
```

??? success "Solution to Exercise 2"
    `test_truthy` passes because a non-empty list is truthy. `test_falsy` fails because an empty list is falsy, and `assert []` evaluates to `assert False`.

---

**Exercise 3.** Write a function `parse_int(s)` that converts a string to an integer or raises `ValueError`. Use `pytest.raises` to test the error case.

??? success "Solution to Exercise 3"
    ```python
    import pytest

    def parse_int(s):
        return int(s)

    def test_valid():
        assert parse_int("42") == 42

    def test_invalid():
        with pytest.raises(ValueError):
            parse_int("abc")
    ```

---

**Exercise 4.** Use `@pytest.mark.parametrize` to test a `square(n)` function with at least five different inputs, including negative numbers and zero.

??? success "Solution to Exercise 4"
    ```python
    import pytest

    def square(n):
        return n * n

    @pytest.mark.parametrize("n,expected", [
        (0, 0),
        (1, 1),
        (5, 25),
        (-3, 9),
        (100, 10000),
    ])
    def test_square(n, expected):
        assert square(n) == expected
    ```
