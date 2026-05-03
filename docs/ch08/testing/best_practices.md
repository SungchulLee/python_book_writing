# Test Organization and Best Practices

Guidelines for writing maintainable and effective tests.

!!! tip "Mental Model"
    Good tests follow the AAA pattern: *Arrange* (set up inputs), *Act* (call the code), *Assert* (check the result). Keep each test focused on one behavior, name it after what it verifies, and organize test files to mirror your source tree. Tests that are easy to read and run are tests that actually get maintained.

## Test Organization

Structure tests logically.

```python
# Project structure:
# project/
#   src/
#     my_module.py
#   tests/
#     test_my_module.py
#     conftest.py (shared fixtures)

import pytest

def function_to_test(x):
    return x * 2

class TestMyModule:
    def test_double(self):
        assert function_to_test(5) == 10
    
    def test_zero(self):
        assert function_to_test(0) == 0

# Run: pytest tests/ -v
print("Tests organized by module")
```

```
Tests organized by module
```

## Naming Conventions and Best Practices

Follow testing best practices.

```python
import pytest

# Good test names describe what is being tested
def test_add_positive_numbers():
    assert 2 + 3 == 5

def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_string_length():
    assert len("hello") == 5

# Arrange-Act-Assert pattern
def test_user_registration():
    # Arrange
    username = "alice"
    password = "secure"
    
    # Act
    registered = register_user(username, password)
    
    # Assert
    assert registered is True

def register_user(username, password):
    return True

print("Best practices applied")
```

```
Best practices applied
```

---

## Exercises

**Exercise 1.**
Refactor the following test to follow the Arrange-Act-Assert pattern. The test checks that a shopping cart correctly calculates the total: items are `[("apple", 1.50), ("banana", 0.75)]` and the expected total is `2.25`. Write both the function and the test.

??? success "Solution to Exercise 1"

    ```python
    def cart_total(items):
        return sum(price for _, price in items)

    def test_cart_total_with_multiple_items():
        # Arrange
        items = [("apple", 1.50), ("banana", 0.75)]
        expected = 2.25

        # Act
        result = cart_total(items)

        # Assert
        assert result == expected
    ```

---

**Exercise 2.**
Write a test class `TestStringUtils` with three well-named test methods for a function `capitalize_words(text)` that capitalizes the first letter of each word. Test normal input, empty string, and already-capitalized input. Use descriptive test names.

??? success "Solution to Exercise 2"

    ```python
    def capitalize_words(text):
        return text.title()

    class TestStringUtils:
        def test_capitalize_words_normal_input(self):
            assert capitalize_words("hello world") == "Hello World"

        def test_capitalize_words_empty_string(self):
            assert capitalize_words("") == ""

        def test_capitalize_words_already_capitalized(self):
            assert capitalize_words("Hello World") == "Hello World"
    ```

---

**Exercise 3.**
Create a test file structure for a project with `src/calculator.py` and `tests/test_calculator.py`. Write the test file with a `conftest.py` that provides a `calculator` fixture. Include at least three tests in a `TestCalculator` class.

??? success "Solution to Exercise 3"

    ```python
    # conftest.py
    import pytest

    class Calculator:
        def add(self, a, b):
            return a + b
        def subtract(self, a, b):
            return a - b
        def multiply(self, a, b):
            return a * b

    @pytest.fixture
    def calculator():
        return Calculator()

    # test_calculator.py
    class TestCalculator:
        def test_add_positive_numbers(self, calculator):
            assert calculator.add(2, 3) == 5

        def test_subtract_returns_negative(self, calculator):
            assert calculator.subtract(3, 5) == -2

        def test_multiply_by_zero(self, calculator):
            assert calculator.multiply(5, 0) == 0
    ```
