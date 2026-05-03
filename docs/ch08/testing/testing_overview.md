# Testing Overview

Introduction to testing frameworks and strategies for writing reliable tests.

!!! tip "Mental Model"
    Automated tests are a safety net for change. Every test encodes one fact about how your code should behave; when you modify the code, the test suite instantly tells you which facts still hold and which broke. Python offers `unittest` (built-in, class-based) and `pytest` (third-party, function-based) — both achieve the same goal with different ergonomics.

## Why Test?

Benefits of automated testing.

```python
# Testing benefits:
# - Catch bugs early
# - Document expected behavior
# - Enable refactoring safely
# - Improve code quality
# - Reduce manual testing

def add(a, b):
    return a + b

# Simple test
assert add(2, 3) == 5, "Addition failed"
assert add(-1, 1) == 0, "Zero test failed"
print("All tests passed!")
```

```
All tests passed!
```

## Testing Frameworks

Popular testing frameworks in Python.

```python
# unittest - built-in testing framework
import unittest

class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 3, 5)

# pytest - simpler, more powerful
# pip install pytest
# def test_addition():
#     assert 2 + 3 == 5

# Running tests:
# unittest: python -m unittest test_module
# pytest: pytest test_file.py

print("Testing frameworks overview")
```

```
Testing frameworks overview
```

## Exercises

**Exercise 1.** Summarize the key concepts introduced in this overview in your own words. Identify which concept you find most important and explain why.

??? success "Solution to Exercise 1"
    Answers will vary. A strong response should demonstrate understanding of the main ideas and articulate a clear reason for prioritizing one concept, connecting it to practical programming tasks.

---

**Exercise 2.** For each concept introduced in this overview, write a short code snippet (2-5 lines) that demonstrates it in action.

??? success "Solution to Exercise 2"
    Answers will vary based on the specific overview content. Each snippet should be self-contained and clearly illustrate the concept it targets.

