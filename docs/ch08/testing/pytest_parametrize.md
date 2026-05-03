# pytest Parametrize

Use parametrize to test multiple input/output combinations efficiently.

!!! tip "Mental Model"
    `@pytest.mark.parametrize` turns one test function into many — each set of arguments becomes a separate test case with its own pass/fail status. Instead of copying the same test with different inputs, you list the cases in a table and let pytest expand them. It keeps your test suite DRY while making every edge case individually visible in the output.

## Basic Parametrization

Test multiple inputs with a single test function.

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5),
    (9, 3, 3),
    (8, 4, 2),
    (0, 5, 0),
])
def test_divide(a, b, expected):
    assert divide(a, b) == expected

# Run with: pytest -v test_divide.py
print("Parametrization test")
```

```
Parametrization test
```

## Parametrizing with pytest.param

Use pytest.param for complex parametrization.

```python
import pytest

def is_palindrome(text):
    return text == text[::-1]

@pytest.mark.parametrize("word,is_palindrome_expected", [
    ("racecar", True),
    ("hello", False),
    ("noon", True),
    ("a", True),
    pytest.param("", True, marks=pytest.mark.skip),
])
def test_palindrome(word, is_palindrome_expected):
    assert is_palindrome(word) == is_palindrome_expected

print("pytest.param allows custom marking")
```

```
pytest.param allows custom marking
```


---

## Exercises

**Exercise 1.** Write a function `is_even(n)` and use `@pytest.mark.parametrize` to test it with at least six values (a mix of even, odd, zero, and negative numbers).

??? success "Solution to Exercise 1"
    ```python
    import pytest

    def is_even(n):
        return n % 2 == 0

    @pytest.mark.parametrize("n,expected", [
        (0, True),
        (1, False),
        (2, True),
        (-3, False),
        (-4, True),
        (100, True),
    ])
    def test_is_even(n, expected):
        assert is_even(n) == expected
    ```

---

**Exercise 2.** Use `@pytest.mark.parametrize` with multiple parameters to test a `max_of_three(a, b, c)` function with at least four test cases.

??? success "Solution to Exercise 2"
    ```python
    import pytest

    def max_of_three(a, b, c):
        return max(a, b, c)

    @pytest.mark.parametrize("a,b,c,expected", [
        (1, 2, 3, 3),
        (3, 2, 1, 3),
        (1, 1, 1, 1),
        (-5, -2, -8, -2),
    ])
    def test_max_of_three(a, b, c, expected):
        assert max_of_three(a, b, c) == expected
    ```

---

**Exercise 3.** Use `pytest.param` with `marks=pytest.mark.xfail` to include a test case that you expect to fail. Write a parametrized test for a `divide(a, b)` function where one case divides by zero.

??? success "Solution to Exercise 3"
    ```python
    import pytest

    def divide(a, b):
        return a / b

    @pytest.mark.parametrize("a,b,expected", [
        (10, 2, 5.0),
        (9, 3, 3.0),
        pytest.param(10, 0, None, marks=pytest.mark.xfail(raises=ZeroDivisionError)),
    ])
    def test_divide(a, b, expected):
        assert divide(a, b) == expected
    ```

---

**Exercise 4.** Stack two `@pytest.mark.parametrize` decorators to test all combinations of inputs. For example, test `multiply(a, b)` where `a` comes from `[1, 2, 3]` and `b` comes from `[10, 20]`.

??? success "Solution to Exercise 4"
    ```python
    import pytest

    def multiply(a, b):
        return a * b

    @pytest.mark.parametrize("a", [1, 2, 3])
    @pytest.mark.parametrize("b", [10, 20])
    def test_multiply(a, b):
        assert multiply(a, b) == a * b
    ```
