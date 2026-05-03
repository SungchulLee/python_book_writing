# typing Overview

Python is dynamically typed — variables can hold any type, and type errors only surface at runtime. As codebases grow, this flexibility becomes a liability: a function may receive an unexpected type and fail deep in its execution. The `typing` module lets you declare expected types so that tools like `mypy` can catch mismatches before the code runs, while Python itself remains dynamically typed.

!!! tip "Mental Model"
    Type hints are a contract layer on top of dynamic Python. You write annotations that say "this function takes a `str` and returns an `int`," and a static checker like mypy verifies the contract at analysis time — without slowing down your program at runtime. Think of them as machine-readable documentation that catches bugs before the code ever runs.

## What is Type Hinting?

Type hints annotate the expected types of variables, function parameters, and return values. Python does not enforce these annotations at runtime — passing the wrong type will not raise a `TypeError` from the hint itself. Instead, type hints serve as machine-readable documentation that static analysis tools can verify.

```python
# Type hints for function parameters and return types
def greet(name: str, age: int) -> str:
    return f"{name} is {age} years old"

result = greet("Alice", 30)
print(result)

# Type hints work with any types
numbers: list[int] = [1, 2, 3]
config: dict[str, str] = {"host": "localhost"}
print(numbers, config)
```

```text
Alice is 30 years old
[1, 2, 3] {'host': 'localhost'}
```

## Benefits of Type Hints

Beyond documentation, type hints unlock three practical benefits. First, IDEs like VS Code and PyCharm use them for autocomplete and inline error detection. Second, static checkers like `mypy` can flag type mismatches before you run the code. Third, type-annotated code is easier for collaborators to read, since the function signature alone reveals the expected data shapes.

```python
# Clear intent for complex types using built-in generics (Python 3.9+)
def process_users(users: list[dict[str, str]]) -> int:
    return len(users)

data = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com"}
]
print(f"Processed {process_users(data)} users")
```

```text
Processed 2 users
```

---

## Runnable Example: `basic_type_hints_tutorial.py`

```python
"""
Tutorial 01: Basic Type Hints in Python
========================================

Level: Beginner

This tutorial introduces the fundamental concepts of type hints in Python,
starting with Python 3.5+. Type hints improve code readability, enable
better IDE support, and help catch bugs early with static type checkers.

Learning Objectives:
- Understand what type hints are and why they're useful
- Learn basic built-in types (int, str, float, bool)
- Apply type hints to variables
- Understand the relationship between type hints and runtime behavior

Prerequisites:
- Basic Python knowledge (variables, functions)
- Python 3.5 or higher
"""

# =============================================================================
# SECTION 1: Introduction to Type Hints
# =============================================================================

"""
Type hints are annotations that specify the expected type of variables,
function parameters, and return values. They were introduced in PEP 484
(Python 3.5) and have been enhanced in subsequent versions.

Key Points:
1. Type hints are OPTIONAL - Python remains dynamically typed
2. Type hints don't affect runtime behavior
3. Type hints are checked by external tools (mypy, pyright, etc.)
4. Type hints improve code documentation and IDE support
"""

# Example 1: Variable without type hint (traditional Python)
age = 25

# Example 2: Variable with type hint (Python 3.5+)
age_with_hint: int = 25

# Both variables behave identically at runtime
# The type hint is metadata that tools can use for static analysis


# =============================================================================
# SECTION 2: Basic Built-in Types
# =============================================================================

"""
Python provides several built-in types that can be used as type hints:
- int: Integer numbers
- float: Floating-point numbers
- str: String (text) data
- bool: Boolean values (True/False)
- bytes: Byte strings
- None: The None type
"""

# Integer type hint
student_count: int = 30
year: int = 2024

# Float type hint
temperature: float = 98.6
pi: float = 3.14159

# String type hint
name: str = "Alice"
greeting: str = "Hello, World!"

# Boolean type hint
is_active: bool = True
has_permission: bool = False

# Bytes type hint
data: bytes = b"binary data"

# None type hint (for variables that will be assigned later)
result: None = None


# =============================================================================
# SECTION 3: Type Hints with Simple Functions
# =============================================================================

"""
Functions can have type hints for parameters and return values.
Syntax: def function_name(param: type) -> return_type:
"""

def greet(name: str) -> str:
    """
    Simple function with type hints.
    
    Parameters:
    - name (str): The name to greet
    
    Returns:
    - str: A greeting message
    """
    return f"Hello, {name}!"


def add(a: int, b: int) -> int:
    """
    Add two integers.
    
    Parameters:
    - a (int): First integer
    - b (int): Second integer
    
    Returns:
    - int: Sum of a and b
    """
    return a + b


def calculate_area(width: float, height: float) -> float:
    """
    Calculate the area of a rectangle.
    
    Parameters:
    - width (float): Width of the rectangle
    - height (float): Height of the rectangle
    
    Returns:
    - float: Area of the rectangle
    """
    return width * height


def is_even(number: int) -> bool:
    """
    Check if a number is even.
    
    Parameters:
    - number (int): The number to check
    
    Returns:
    - bool: True if even, False otherwise
    """
    return number % 2 == 0


# =============================================================================
# SECTION 4: Understanding Runtime Behavior
# =============================================================================

"""
IMPORTANT: Type hints do NOT enforce type checking at runtime.
Python will not raise an error if you pass the wrong type.
"""

def multiply(x: int, y: int) -> int:
    """Multiply two integers."""
    return x * y


# This works at runtime, even though the types are wrong!
result_1 = multiply(2, 3)        # Correct: 6
result_2 = multiply(2.5, 3.5)    # Also works at runtime: 8.75
result_3 = multiply("Hi", 3)     # Also works: "HiHiHi"

# To catch these errors, you need to use a static type checker like mypy:
# $ mypy 01_basic_type_hints.py


# =============================================================================
# SECTION 5: Benefits of Type Hints
# =============================================================================

"""
Benefits of using type hints:

1. IMPROVED READABILITY
   - Code is self-documenting
   - Clear expectations for function inputs/outputs

2. BETTER IDE SUPPORT
   - Autocomplete suggestions
   - Type checking in real-time
   - Refactoring assistance

3. EARLY BUG DETECTION
   - Static type checkers find type errors before runtime
   - Catch bugs during development

4. EASIER MAINTENANCE
   - Understand code faster when returning to it
   - Safer refactoring

5. BETTER COLLABORATION
   - Clear contracts between functions
   - Less confusion about expected types
"""

def calculate_discount(price: float, discount_percent: int) -> float:
    """
    Calculate discounted price.
    
    With type hints, it's immediately clear that:
    - price should be a floating-point number
    - discount_percent should be an integer
    - The function returns a floating-point number
    
    Without type hints, you'd need to read documentation or code
    to understand these expectations.
    """
    discount_amount = price * (discount_percent / 100)
    return price - discount_amount


# =============================================================================
# SECTION 6: Common Mistakes and Best Practices
# =============================================================================

"""
MISTAKE 1: Thinking type hints are enforced at runtime
"""

def square(n: int) -> int:
    return n * n

# This will work at runtime but is incorrect according to type hints
x = square("5")  # No runtime error, but type checker would complain


"""
MISTAKE 2: Being inconsistent with type hints
"""

# BAD: Mixing typed and untyped code in the same function
def bad_example(a: int, b) -> int:  # 'b' has no type hint
    return a + b

# GOOD: Be consistent - either type everything or nothing
def good_example(a: int, b: int) -> int:
    return a + b


"""
BEST PRACTICE 1: Start with function signatures
"""

# Type hints are most valuable for function signatures
# They document the contract between the function and its callers
def process_data(input_data: str, max_length: int) -> str:
    """Process and truncate input data."""
    return input_data[:max_length]


"""
BEST PRACTICE 2: Use type hints for public APIs
"""

# Always use type hints for functions that other code will call
def public_function(user_id: int, username: str) -> bool:
    """Public function with clear type contract."""
    # Implementation details...
    return True


# =============================================================================
# SECTION 7: Practical Examples
# =============================================================================

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate Body Mass Index.
    
    Parameters:
    - weight_kg (float): Weight in kilograms
    - height_m (float): Height in meters
    
    Returns:
    - float: BMI value
    """
    return weight_kg / (height_m ** 2)


def format_currency(amount: float, currency_symbol: str) -> str:
    """
    Format a number as currency.
    
    Parameters:
    - amount (float): The monetary amount
    - currency_symbol (str): Symbol to use (e.g., "$", "€")
    
    Returns:
    - str: Formatted currency string
    """
    return f"{currency_symbol}{amount:.2f}"


def is_valid_age(age: int) -> bool:
    """
    Check if an age value is valid (between 0 and 150).
    
    Parameters:
    - age (int): Age to validate
    
    Returns:
    - bool: True if valid, False otherwise
    """
    return 0 <= age <= 150


def count_vowels(text: str) -> int:
    """
    Count the number of vowels in a string.
    
    Parameters:
    - text (str): Input string
    
    Returns:
    - int: Number of vowels
    """
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)


# =============================================================================
# SECTION 8: Testing and Verification
# =============================================================================

if __name__ == "__main__":
    # Test basic functions
    print("=== Basic Type Hints Examples ===\n")
    
    print(f"greet('Bob'): {greet('Bob')}")
    print(f"add(5, 3): {add(5, 3)}")
    print(f"calculate_area(4.5, 3.2): {calculate_area(4.5, 3.2)}")
    print(f"is_even(7): {is_even(7)}")
    print()
    
    # Test practical examples
    print("=== Practical Examples ===\n")
    
    bmi = calculate_bmi(70.0, 1.75)
    print(f"BMI for 70kg, 1.75m: {bmi:.2f}")
    
    price = format_currency(42.50, "$")
    print(f"Formatted price: {price}")
    
    print(f"Is age 25 valid? {is_valid_age(25)}")
    print(f"Is age 200 valid? {is_valid_age(200)}")
    
    print(f"Vowels in 'Hello World': {count_vowels('Hello World')}")
    
    print("\n=== Type Checking Notes ===")
    print("To check types with mypy, run: mypy 01_basic_type_hints.py")
    print("Type hints improve code quality but don't affect runtime behavior!")
```

---

## Exercises

**Exercise 1.** Add type annotations to the following unannotated function:

```python
def count_words(text):
    words = text.split()
    counts = {}
    for w in words:
        counts[w] = counts.get(w, 0) + 1
    return counts
```

??? success "Solution to Exercise 1"
    ```python
    def count_words(text: str) -> dict[str, int]:
        words: list[str] = text.split()
        counts: dict[str, int] = {}
        for w in words:
            counts[w] = counts.get(w, 0) + 1
        return counts

    print(count_words("the cat sat on the mat"))
    ```

---

**Exercise 2.** Explain the difference between Python's runtime behavior and `mypy`'s static analysis. If you annotate `x: int = "hello"`, will Python raise an error at runtime? Will `mypy`?

??? success "Solution to Exercise 2"
    Python does not enforce type annotations at runtime. `x: int = "hello"` runs without error — annotations are metadata only. However, `mypy` (a static type checker) reports: `Incompatible types in assignment (expression has type "str", variable has type "int")`. The annotations serve as documentation and are checked by external tools, not by Python itself.

---

**Exercise 3.** Write a fully annotated function `safe_get(d: dict[str, T], key: str, default: T) -> T` using `TypeVar`. Test it with both `int` and `str` value types.

??? success "Solution to Exercise 3"
    ```python
    from typing import TypeVar

    T = TypeVar("T")

    def safe_get(d: dict[str, T], key: str, default: T) -> T:
        return d.get(key, default)

    print(safe_get({"a": 1, "b": 2}, "c", 0))         # 0
    print(safe_get({"x": "hello"}, "y", "default"))     # "default"
    ```

---

**Exercise 4.** List three benefits and one potential drawback of adding type hints to a Python project. Provide a concrete example of each benefit.

??? success "Solution to Exercise 4"
    **Benefits:**

    1. **Catch bugs early**: `mypy` flags `len(42)` before you run the code.
    2. **Self-documenting**: `def connect(host: str, port: int) -> Socket` is clearer than an unannotated version.
    3. **IDE support**: Editors provide better autocomplete and refactoring when types are known.

    **Drawback:**

    1. **Added verbosity**: Complex annotations like `dict[str, list[tuple[int, ...]]]` can reduce readability. Type aliases help mitigate this.
