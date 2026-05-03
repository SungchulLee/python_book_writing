# unittest Basics

Introduction to Python's built-in unittest framework.

!!! tip "Mental Model"
    `unittest` follows the xUnit pattern: you subclass `TestCase`, write methods named `test_*`, use `self.assert*` to check results, and run them with a test runner. `setUp` runs before each test, `tearDown` after. It is more verbose than pytest but ships with Python and is well-suited for teams already familiar with JUnit or NUnit from other languages.

## Creating Test Cases

Write test classes with unittest.

```python
import unittest

def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_add_negative(self):
        self.assertEqual(add(-1, -1), -2)
    
    def test_add_zero(self):
        self.assertEqual(add(0, 5), 5)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False, verbosity=2)
```

```
test_add_negative (__main__.TestMath) ... ok
test_add_positive (__main__.TestMath) ... ok
test_add_zero (__main__.TestMath) ... ok
```

## setUp and tearDown

Use setUp and tearDown for test initialization and cleanup.

```python
import unittest

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Run before each test
        self.db = {}
        print("Setting up test database")
    
    def tearDown(self):
        # Run after each test
        self.db.clear()
        print("Cleaning up database")
    
    def test_insert(self):
        self.db['user1'] = 'Alice'
        self.assertEqual(self.db['user1'], 'Alice')
    
    def test_delete(self):
        self.db['user1'] = 'Bob'
        del self.db['user1']
        self.assertNotIn('user1', self.db)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False, verbosity=2)
```

```
Setting up test database
test_delete (__main__.TestDatabase) ... ok
Cleaning up database
test_insert (__main__.TestDatabase) ... ok
```

---

## Runnable Example: `unittest_basics_tutorial.py`

```python
"""
04_unittest_basics.py

UNITTEST FRAMEWORK BASICS
==========================

Introduction to Python's built-in unittest framework for structured testing.

Learning Objectives:
- Understand unittest.TestCase class
- Write test methods and test classes  
- Run tests with unittest.main()
- Use basic unittest assertions
- Organize tests in test classes

Target: Intermediate Level - Week 3
Prerequisites: 01-03 completed
"""

import unittest


# ============================================================================
# PART 1: INTRODUCTION TO UNITTEST
# ============================================================================

"""
unittest is Python's built-in testing framework, inspired by JUnit (Java).

KEY FEATURES:
- Test organization in classes
- Rich set of assertion methods
- Test fixtures (setUp/tearDown)
- Test discovery
- Test runners
- Built into Python (no installation needed)

BASIC STRUCTURE:
1. Import unittest
2. Create class inheriting from unittest.TestCase
3. Write test methods starting with test_
4. Use self.assert* methods
5. Run with unittest.main()
"""


# ============================================================================
# PART 2: FIRST UNITTEST TEST CASE
# ============================================================================

# Functions to test
def add(a, b):
    """Add two numbers."""
    return a + b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


# Test class inheriting from unittest.TestCase
class TestBasicMath(unittest.TestCase):
    """Test basic mathematical operations."""
    
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        result = add(2, 3)
        self.assertEqual(result, 5)
    
    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        result = add(-2, -3)
        self.assertEqual(result, -5)
    
    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        result = multiply(3, 4)
        self.assertEqual(result, 12)
    
    def test_multiply_by_zero(self):
        """Test multiplying by zero returns zero."""
        result = multiply(5, 0)
        self.assertEqual(result, 0)


# ============================================================================
# PART 3: COMMON UNITTEST ASSERTIONS
# ============================================================================

class TestUnittestAssertions(unittest.TestCase):
    """Demonstrate common unittest assertion methods."""
    
    def test_assertEqual(self):
        """Test assertEqual: checks if two values are equal."""
        self.assertEqual(1 + 1, 2)
        self.assertEqual("hello", "hello")
        self.assertEqual([1, 2, 3], [1, 2, 3])
    
    def test_assertNotEqual(self):
        """Test assertNotEqual: checks if two values are different."""
        self.assertNotEqual(1, 2)
        self.assertNotEqual("hello", "world")
    
    def test_assertTrue_assertFalse(self):
        """Test assertTrue and assertFalse: check boolean values."""
        self.assertTrue(True)
        self.assertTrue(1 == 1)
        self.assertFalse(False)
        self.assertFalse(1 == 2)
    
    def test_assertIs_assertIsNot(self):
        """Test assertIs and assertIsNot: check object identity."""
        a = [1, 2, 3]
        b = a  # Same object
        c = [1, 2, 3]  # Different object, same value
        
        self.assertIs(a, b)  # Same object
        self.assertIsNot(a, c)  # Different objects
    
    def test_assertIsNone_assertIsNotNone(self):
        """Test assertIsNone and assertIsNotNone: check for None."""
        value = None
        self.assertIsNone(value)
        
        value = "something"
        self.assertIsNotNone(value)
    
    def test_assertIn_assertNotIn(self):
        """Test assertIn and assertNotIn: check membership."""
        self.assertIn(3, [1, 2, 3, 4])
        self.assertIn("apple", ["apple", "banana"])
        self.assertNotIn(5, [1, 2, 3, 4])
    
    def test_assertIsInstance(self):
        """Test assertIsInstance: check type."""
        self.assertIsInstance(42, int)
        self.assertIsInstance("hello", str)
        self.assertIsInstance([1, 2], list)


# ============================================================================
# PART 4: TESTING WITH MULTIPLE TEST CLASSES
# ============================================================================

class Calculator:
    """Simple calculator for demonstration."""
    
    def __init__(self):
        self.history = []
    
    def add(self, a, b):
        """Add two numbers and record in history."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """Subtract b from a and record in history."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()


class TestCalculatorOperations(unittest.TestCase):
    """Test calculator arithmetic operations."""
    
    def test_addition(self):
        """Test calculator addition."""
        calc = Calculator()
        self.assertEqual(calc.add(2, 3), 5)
        self.assertEqual(calc.add(10, 20), 30)
    
    def test_subtraction(self):
        """Test calculator subtraction."""
        calc = Calculator()
        self.assertEqual(calc.subtract(5, 3), 2)
        self.assertEqual(calc.subtract(10, 20), -10)


class TestCalculatorHistory(unittest.TestCase):
    """Test calculator history functionality."""
    
    def test_history_records_operations(self):
        """Test that operations are recorded in history."""
        calc = Calculator()
        calc.add(2, 3)
        calc.subtract(10, 5)
        
        self.assertEqual(len(calc.history), 2)
        self.assertIn("2 + 3 = 5", calc.history)
        self.assertIn("10 - 5 = 5", calc.history)
    
    def test_clear_history_empties_list(self):
        """Test that clear_history empties the history list."""
        calc = Calculator()
        calc.add(1, 1)
        calc.clear_history()
        
        self.assertEqual(len(calc.history), 0)


# ============================================================================
# PART 5: TEST METHOD NAMING AND ORGANIZATION
# ============================================================================

"""
TEST METHOD REQUIREMENTS:
- Must start with 'test_'
- Should have descriptive names
- One test, one concept
- Can have docstrings

GOOD TEST NAMES:
✓ test_add_positive_numbers()
✓ test_empty_list_returns_zero()
✓ test_invalid_email_raises_error()

BAD TEST NAMES:
✗ test1()  # Not descriptive
✗ testAddition()  # Wrong naming convention (camelCase)
✗ check_addition()  # Doesn't start with 'test_'
"""


class TestNamingExamples(unittest.TestCase):
    """Examples of good test naming."""
    
    def test_empty_string_has_zero_length(self):
        """Test that empty string has length of zero."""
        self.assertEqual(len(""), 0)
    
    def test_list_append_increases_length(self):
        """Test that append increases list length by one."""
        my_list = [1, 2, 3]
        my_list.append(4)
        self.assertEqual(len(my_list), 4)
    
    def test_dict_get_returns_none_for_missing_key(self):
        """Test that dict.get() returns None for missing keys."""
        my_dict = {"a": 1}
        self.assertIsNone(my_dict.get("b"))


# ============================================================================
# PART 6: RUNNING UNITTEST TESTS
# ============================================================================

"""
WAYS TO RUN UNITTEST TESTS:

1. MODULE EXECUTION (using if __name__ == "__main__")
   python 04_unittest_basics.py

2. COMMAND LINE - SINGLE FILE
   python -m unittest 04_unittest_basics.py

3. COMMAND LINE - SPECIFIC CLASS
   python -m unittest 04_unittest_basics.TestBasicMath

4. COMMAND LINE - SPECIFIC TEST
   python -m unittest 04_unittest_basics.TestBasicMath.test_add_positive_numbers

5. TEST DISCOVERY (all test files)
   python -m unittest discover

6. VERBOSE OUTPUT
   python -m unittest -v 04_unittest_basics.py
"""


# ============================================================================
# PART 7: PRACTICAL EXAMPLE - STRING UTILITIES
# ============================================================================

class StringUtils:
    """Utility functions for string manipulation."""
    
    @staticmethod
    def reverse(text):
        """Reverse a string."""
        return text[::-1]
    
    @staticmethod
    def is_palindrome(text):
        """Check if text is a palindrome."""
        clean = text.lower().replace(" ", "")
        return clean == clean[::-1]
    
    @staticmethod
    def count_vowels(text):
        """Count vowels in text."""
        vowels = "aeiouAEIOU"
        return sum(1 for char in text if char in vowels)


class TestStringUtils(unittest.TestCase):
    """Test StringUtils class methods."""
    
    def test_reverse_simple_string(self):
        """Test reversing a simple string."""
        result = StringUtils.reverse("hello")
        self.assertEqual(result, "olleh")
    
    def test_reverse_empty_string(self):
        """Test reversing empty string returns empty string."""
        result = StringUtils.reverse("")
        self.assertEqual(result, "")
    
    def test_is_palindrome_true_case(self):
        """Test palindrome detection with actual palindrome."""
        self.assertTrue(StringUtils.is_palindrome("racecar"))
        self.assertTrue(StringUtils.is_palindrome("A man a plan a canal Panama"))
    
    def test_is_palindrome_false_case(self):
        """Test palindrome detection with non-palindrome."""
        self.assertFalse(StringUtils.is_palindrome("hello"))
        self.assertFalse(StringUtils.is_palindrome("world"))
    
    def test_count_vowels_simple_string(self):
        """Test counting vowels in a simple string."""
        count = StringUtils.count_vowels("hello")
        self.assertEqual(count, 2)  # 'e' and 'o'
    
    def test_count_vowels_no_vowels(self):
        """Test counting vowels in string with no vowels."""
        count = StringUtils.count_vowels("gym")
        self.assertEqual(count, 0)


# ============================================================================
# PART 8: UNITTEST BEST PRACTICES
# ============================================================================

"""
UNITTEST BEST PRACTICES:

1. ONE CONCEPT PER TEST
   ✓ test_add_positive_numbers()
   ✗ test_all_calculator_functions()  # Too broad

2. USE DESCRIPTIVE NAMES
   ✓ test_empty_list_returns_zero_length()
   ✗ test1()

3. TEST ONE THING AT A TIME
   - Each test should verify one specific behavior
   - Easier to identify failures

4. INDEPENDENT TESTS
   - Tests should not depend on each other
   - Should work in any order

5. FAST TESTS
   - Unit tests should be fast (milliseconds)
   - Slow tests reduce test frequency

6. USE SELF.ASSERT* METHODS
   ✓ self.assertEqual(a, b)
   ✗ assert a == b  # Don't use raw assert in unittest

7. CLEAR ERROR MESSAGES
   - Add msg parameter to assertions when helpful
   - self.assertEqual(result, expected, "Addition failed")
"""


class TestBestPracticesExample(unittest.TestCase):
    """Example of following best practices."""
    
    def test_single_concept(self):
        """Each test checks one specific thing."""
        result = add(2, 3)
        self.assertEqual(result, 5, "2 + 3 should equal 5")
    
    def test_is_independent(self):
        """This test doesn't depend on any other test."""
        # Create fresh test data
        numbers = [1, 2, 3]
        # Test one specific behavior
        self.assertEqual(len(numbers), 3)


# ============================================================================
# SUMMARY
# ============================================================================

"""
KEY TAKEAWAYS:

1. unittest provides structured testing framework
2. Tests are organized in classes inheriting from TestCase
3. Test methods must start with 'test_'
4. Use self.assert* methods, not raw assert
5. Multiple test classes can test different aspects
6. Tests should be independent and focused
7. Run with python -m unittest or unittest.main()

UNITTEST vs PLAIN ASSERTIONS:
Plain:  assert result == expected
unittest: self.assertEqual(result, expected)

ADVANTAGES OF UNITTEST:
- Better error messages
- Test organization and grouping
- Test fixtures (setUp/tearDown)
- Test discovery and runners
- Integration with CI/CD systems

NEXT STEPS:
- Learn more assertion methods (05_unittest_assertions.py)
- Master test fixtures (06_test_fixtures.py)
- Explore test suites (07_test_suites.py)
"""


if __name__ == "__main__":
    # Run all tests in this module
    unittest.main(verbosity=2)
```

---

## Exercises

**Exercise 1.** Write a function `is_palindrome(s)` that returns `True` if the string reads the same forwards and backwards (case-insensitive). Then write a `unittest.TestCase` class with at least four test methods covering normal palindromes, non-palindromes, empty strings, and single characters.

??? success "Solution to Exercise 1"
    ```python
    import unittest

    def is_palindrome(s):
        s = s.lower()
        return s == s[::-1]

    class TestPalindrome(unittest.TestCase):
        def test_palindrome(self):
            self.assertTrue(is_palindrome("racecar"))

        def test_not_palindrome(self):
            self.assertFalse(is_palindrome("hello"))

        def test_empty_string(self):
            self.assertTrue(is_palindrome(""))

        def test_single_char(self):
            self.assertTrue(is_palindrome("a"))

        def test_case_insensitive(self):
            self.assertTrue(is_palindrome("Madam"))

    if __name__ == "__main__":
        unittest.main()
    ```

---

**Exercise 2.** Predict what happens when you run this test class. Will the test pass or fail, and why?

```python
import unittest

class TestListMethods(unittest.TestCase):
    def test_append(self):
        lst = [1, 2, 3]
        lst.append(4)
        self.assertEqual(lst, [1, 2, 3, 4])
        self.assertIn(4, lst)

    def test_remove_nonexistent(self):
        lst = [1, 2, 3]
        lst.remove(5)
```

??? success "Solution to Exercise 2"
    The first test (`test_append`) passes. The second test (`test_remove_nonexistent`) fails with a `ValueError` because `5` is not in the list. Since the test does not use `assertRaises`, the unhandled `ValueError` causes the test to fail.

---

**Exercise 3.** Write a `Calculator` class with methods `add`, `subtract`, `multiply`, and `divide`. The `divide` method should raise `ZeroDivisionError` for division by zero. Write a `unittest.TestCase` that tests all four operations and uses `assertRaises` for the error case.

??? success "Solution to Exercise 3"
    ```python
    import unittest

    class Calculator:
        def add(self, a, b):
            return a + b
        def subtract(self, a, b):
            return a - b
        def multiply(self, a, b):
            return a * b
        def divide(self, a, b):
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            return a / b

    class TestCalculator(unittest.TestCase):
        def setUp(self):
            self.calc = Calculator()

        def test_add(self):
            self.assertEqual(self.calc.add(2, 3), 5)

        def test_subtract(self):
            self.assertEqual(self.calc.subtract(10, 4), 6)

        def test_multiply(self):
            self.assertEqual(self.calc.multiply(3, 7), 21)

        def test_divide(self):
            self.assertAlmostEqual(self.calc.divide(10, 3), 3.3333, places=3)

        def test_divide_by_zero(self):
            with self.assertRaises(ZeroDivisionError):
                self.calc.divide(10, 0)

    if __name__ == "__main__":
        unittest.main()
    ```

---

**Exercise 4.** Write a test class that uses `setUp` and `tearDown` to create and clean up a temporary list. In `setUp`, create a list `[1, 2, 3]`. Write two tests: one that appends an element and checks the length, and another that pops an element and checks the result. Verify that each test starts with a fresh list.

??? success "Solution to Exercise 4"
    ```python
    import unittest

    class TestWithSetUp(unittest.TestCase):
        def setUp(self):
            self.data = [1, 2, 3]

        def tearDown(self):
            self.data = None

        def test_append(self):
            self.data.append(4)
            self.assertEqual(len(self.data), 4)
            self.assertIn(4, self.data)

        def test_pop(self):
            result = self.data.pop()
            self.assertEqual(result, 3)
            self.assertEqual(len(self.data), 2)
            # data still has [1, 2, 3] at the start of each test
            # because setUp creates a fresh list

    if __name__ == "__main__":
        unittest.main()
    ```
