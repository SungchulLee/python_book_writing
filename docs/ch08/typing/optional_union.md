# Optional and Union

`Optional` represents values that can be None, while `Union` represents a value that can be one of several types.

!!! tip "Mental Model"
    `Optional[X]` is shorthand for `Union[X, None]` — it says "this value is either an X or None." `Union[X, Y]` says "this value is either an X or a Y." In Python 3.10+ you can write `X | Y` instead, which reads more naturally. These annotations make nullable and multi-type values explicit so type checkers can warn you when you forget a None check.

## Optional - Nullable Types

Use `Optional[T]` when a value can be of type T or None.

```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

print(find_user(1))  # Alice
print(find_user(99))  # None
```

```
Alice
None
```

## Union - Multiple Possible Types

Use `Union[T1, T2]` when a value can be one of several types.

```python
from typing import Union

def process_id(value: Union[int, str]) -> str:
    if isinstance(value, int):
        return f"Integer ID: {value}"
    else:
        return f"String ID: {value}"

print(process_id(123))
print(process_id("ABC"))
```

```
Integer ID: 123
String ID: ABC
```

## Modern Syntax with |

Python 3.10+ allows using | instead of Union.

```python
# Python 3.10+ syntax
def process_data(value: int | str) -> str:
    return f"Got: {value}"

# Optional is equivalent to T | None
def find_item(item_id: int) -> str | None:
    items = {1: "Item A"}
    return items.get(item_id)

print(process_data(42))
print(find_item(1))
print(find_item(99))
```

```
Got: 42
Item A
None
```

---

## Runnable Example: `optional_union_tutorial.py`

```python
"""
Tutorial 04: Optional and Union Types
======================================

Level: Intermediate

This tutorial covers Optional and Union types, which allow you to specify
that a variable or parameter can be one of multiple types. These are
essential for handling None values and creating flexible type signatures.

Learning Objectives:
- Master the Optional type for nullable values
- Use Union types for multiple possible types
- Understand the difference between Optional and Union
- Handle None values safely in type-checked code
- Use type narrowing with isinstance checks

Prerequisites:
- Tutorial 01: Basic Type Hints
- Tutorial 02: Function Annotations
- Tutorial 03: Collection Type Hints
"""

from typing import Optional, Union, List, Dict

# =============================================================================
# SECTION 1: The Optional Type
# =============================================================================

"""
Optional[X] is equivalent to Union[X, None].
It indicates that a value can be either type X or None.

Use Optional when:
- A parameter has a default value of None
- A function might return None in some cases
- A variable might not be initialized immediately

Syntax:
- Optional[type] is shorthand for Union[type, None]
"""

def find_user(user_id: int) -> Optional[str]:
    """
    Find a user by ID, return None if not found.
    
    Parameters:
    - user_id (int): User ID to search for
    
    Returns:
    - Optional[str]: Username if found, None otherwise
    """
    # Simulated database lookup
    users = {1: "alice", 2: "bob", 3: "charlie"}
    return users.get(user_id)  # Returns None if key not found


def greet_user(name: Optional[str] = None) -> str:
    """
    Greet a user, with optional name parameter.
    
    Parameters:
    - name (Optional[str]): User's name, or None for generic greeting
    
    Returns:
    - str: Greeting message
    """
    if name is None:
        return "Hello, guest!"
    return f"Hello, {name}!"


def parse_int(value: str) -> Optional[int]:
    """
    Parse a string to an integer, return None if invalid.
    
    Parameters:
    - value (str): String to parse
    
    Returns:
    - Optional[int]: Parsed integer or None if parsing fails
    """
    try:
        return int(value)
    except ValueError:
        return None


# Optional with collections
def get_first_element(items: List[int]) -> Optional[int]:
    """
    Get the first element of a list, or None if list is empty.
    
    Parameters:
    - items (List[int]): List of integers
    
    Returns:
    - Optional[int]: First element or None
    """
    if items:
        return items[0]
    return None


def find_max(numbers: List[float]) -> Optional[float]:
    """
    Find maximum value in a list, return None if list is empty.
    
    Parameters:
    - numbers (List[float]): List of numbers
    
    Returns:
    - Optional[float]: Maximum value or None
    """
    if not numbers:
        return None
    return max(numbers)


# =============================================================================
# SECTION 2: Working with Optional Values
# =============================================================================

"""
When working with Optional values, you should check for None before using
the value. This is called "type narrowing" - the type checker understands
that after a None check, the value is no longer Optional.
"""

def process_optional_string(text: Optional[str]) -> int:
    """
    Process a string that might be None.
    
    Demonstrates proper handling of Optional values.
    
    Parameters:
    - text (Optional[str]): String to process, or None
    
    Returns:
    - int: Length of string, or 0 if None
    """
    # Check for None before using the value
    if text is None:
        return 0
    
    # After the None check, text is known to be str (not Optional[str])
    return len(text)  # Type checker knows text is str here


def get_initials(name: Optional[str]) -> str:
    """
    Get initials from a name, return empty string if name is None.
    
    Parameters:
    - name (Optional[str]): Full name or None
    
    Returns:
    - str: Initials or empty string
    """
    if name is None:
        return ""
    
    words = name.split()
    if not words:
        return ""
    
    return "".join(word[0].upper() for word in words)


def double_if_present(value: Optional[int]) -> Optional[int]:
    """
    Double a number if present, otherwise return None.
    
    Parameters:
    - value (Optional[int]): Number to double, or None
    
    Returns:
    - Optional[int]: Doubled value or None
    """
    if value is not None:
        return value * 2
    return None


# =============================================================================
# SECTION 3: The Union Type
# =============================================================================

"""
Union[X, Y] indicates that a value can be either type X or type Y (or both).
Union can include more than two types.

Use Union when:
- A value can legitimately be one of several types
- Different return types are possible based on input
- An API accepts multiple input types

Syntax: Union[type1, type2, ...]
"""

def process_id(user_id: Union[int, str]) -> str:
    """
    Process a user ID that can be either int or str.
    
    Parameters:
    - user_id (Union[int, str]): User ID as integer or string
    
    Returns:
    - str: Formatted user ID
    """
    # Use isinstance to check which type we have
    if isinstance(user_id, int):
        return f"ID-{user_id:06d}"
    else:  # user_id is str
        return f"ID-{user_id}"


def add_numbers(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers that can be int or float.
    
    Parameters:
    - a (Union[int, float]): First number
    - b (Union[int, float]): Second number
    
    Returns:
    - Union[int, float]: Sum (int if both are int, otherwise float)
    """
    result = a + b
    # If both inputs are int, result is int; otherwise float
    if isinstance(a, int) and isinstance(b, int):
        return result
    return float(result)


def format_value(value: Union[int, float, str]) -> str:
    """
    Format a value that can be int, float, or str.
    
    Parameters:
    - value (Union[int, float, str]): Value to format
    
    Returns:
    - str: Formatted string
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, int):
        return f"{value}"
    else:  # float
        return f"{value:.2f}"


# Union with None (equivalent to Optional)
def divide(a: float, b: float) -> Union[float, None]:
    """
    Divide two numbers, return None if division by zero.
    
    This is equivalent to: -> Optional[float]
    
    Parameters:
    - a (float): Numerator
    - b (float): Denominator
    
    Returns:
    - Union[float, None]: Result or None if b is zero
    """
    if b == 0:
        return None
    return a / b


# =============================================================================
# SECTION 4: Type Narrowing with isinstance
# =============================================================================

"""
When working with Union types, use isinstance() to narrow the type.
Type checkers understand isinstance checks and treat the variable as
the specific type in each branch.
"""

def process_data(data: Union[List[int], Dict[str, int]]) -> int:
    """
    Process data that can be either a list or a dictionary.
    
    Parameters:
    - data (Union[List[int], Dict[str, int]]): Input data
    
    Returns:
    - int: Sum of all values
    """
    if isinstance(data, list):
        # Type checker knows data is List[int] here
        return sum(data)
    else:
        # Type checker knows data is Dict[str, int] here
        return sum(data.values())


def get_length(obj: Union[str, List[int], Dict[str, int]]) -> int:
    """
    Get the length of various objects.
    
    Parameters:
    - obj (Union[str, List[int], Dict[str, int]]): Object to measure
    
    Returns:
    - int: Length of the object
    """
    # isinstance works with all these types
    return len(obj)


def stringify(value: Union[int, float, bool, None]) -> str:
    """
    Convert various types to string with specific formatting.
    
    Parameters:
    - value (Union[int, float, bool, None]): Value to convert
    
    Returns:
    - str: String representation
    """
    if value is None:
        return "null"
    elif isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, int):
        return str(value)
    else:  # float
        return f"{value:.2f}"


# =============================================================================
# SECTION 5: Complex Optional and Union Patterns
# =============================================================================

"""
Optional and Union can be combined with collections and other types
to create complex type signatures.
"""

# Optional collection
def get_tags(item_id: int) -> Optional[List[str]]:
    """
    Get tags for an item, return None if item doesn't exist.
    
    Parameters:
    - item_id (int): Item ID
    
    Returns:
    - Optional[List[str]]: List of tags or None if item not found
    """
    # Simulated database lookup
    items = {
        1: ["python", "programming"],
        2: ["web", "javascript"]
    }
    return items.get(item_id)


# List of optional values
def parse_numbers(values: List[str]) -> List[Optional[int]]:
    """
    Parse a list of strings to integers, None for invalid strings.
    
    Parameters:
    - values (List[str]): Strings to parse
    
    Returns:
    - List[Optional[int]]: List of parsed integers (None for invalid)
    """
    result: List[Optional[int]] = []
    for value in values:
        try:
            result.append(int(value))
        except ValueError:
            result.append(None)
    return result


# Union of collections
def process_input(data: Union[List[int], Dict[str, int], int]) -> int:
    """
    Process input that can be a list, dict, or single integer.
    
    Parameters:
    - data (Union[List[int], Dict[str, int], int]): Input data
    
    Returns:
    - int: Processed result
    """
    if isinstance(data, int):
        return data
    elif isinstance(data, list):
        return sum(data)
    else:  # Dict[str, int]
        return sum(data.values())


# Optional with Union
def flexible_lookup(key: Union[int, str]) -> Optional[str]:
    """
    Lookup that accepts multiple key types and might return None.
    
    Parameters:
    - key (Union[int, str]): Lookup key
    
    Returns:
    - Optional[str]: Found value or None
    """
    int_map = {1: "one", 2: "two", 3: "three"}
    str_map = {"a": "alpha", "b": "beta", "c": "gamma"}
    
    if isinstance(key, int):
        return int_map.get(key)
    else:
        return str_map.get(key)


# =============================================================================
# SECTION 6: Best Practices
# =============================================================================

"""
PRACTICE 1: Prefer Optional over Union[X, None]
"""

# GOOD: Clear and concise
def find_item(item_id: int) -> Optional[str]:
    pass

# OKAY: More verbose but equivalent
def find_item_verbose(item_id: int) -> Union[str, None]:
    pass


"""
PRACTICE 2: Always check for None before using Optional values
"""

def safe_processing(value: Optional[str]) -> str:
    # GOOD: Check before use
    if value is None:
        return "default"
    return value.upper()


"""
PRACTICE 3: Use Union sparingly - consider if a common interface would work
"""

# Sometimes Union indicates a design problem
# Consider if these could share a common interface instead
def process_mixed(data: Union[List[int], Dict[str, int]]) -> int:
    # Needs isinstance checks throughout
    if isinstance(data, list):
        return sum(data)
    return sum(data.values())


"""
PRACTICE 4: Document what None means
"""

def search(query: str, max_results: Optional[int] = None) -> List[str]:
    """
    Search for items matching query.
    
    Parameters:
    - query (str): Search query
    - max_results (Optional[int]): Maximum results to return.
                                    None means no limit.
    
    Returns:
    - List[str]: Search results
    """
    # Implementation would use max_results appropriately
    return []


# =============================================================================
# SECTION 7: Practical Examples
# =============================================================================

def safe_divide(a: float, b: float, default: Optional[float] = None) -> Optional[float]:
    """
    Safely divide two numbers.
    
    Parameters:
    - a (float): Numerator
    - b (float): Denominator
    - default (Optional[float]): Default value for division by zero
    
    Returns:
    - Optional[float]: Result or default or None
    """
    if b == 0:
        return default
    return a / b


def extract_numbers(text: str) -> List[Union[int, float]]:
    """
    Extract all numbers (int or float) from text.
    
    Parameters:
    - text (str): Input text
    
    Returns:
    - List[Union[int, float]]: Extracted numbers
    """
    numbers: List[Union[int, float]] = []
    for word in text.split():
        try:
            if '.' in word:
                numbers.append(float(word))
            else:
                numbers.append(int(word))
        except ValueError:
            continue
    return numbers


def merge_configs(
    default: Dict[str, Union[str, int]],
    override: Optional[Dict[str, Union[str, int]]] = None
) -> Dict[str, Union[str, int]]:
    """
    Merge configuration dictionaries.
    
    Parameters:
    - default (Dict[str, Union[str, int]]): Default configuration
    - override (Optional[Dict[str, Union[str, int]]]): Override values
    
    Returns:
    - Dict[str, Union[str, int]]: Merged configuration
    """
    result = default.copy()
    if override is not None:
        result.update(override)
    return result


def calculate_average(numbers: List[Union[int, float]]) -> Optional[float]:
    """
    Calculate average of numbers, return None if list is empty.
    
    Parameters:
    - numbers (List[Union[int, float]]): List of numbers
    
    Returns:
    - Optional[float]: Average or None
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


# =============================================================================
# SECTION 8: Testing and Examples
# =============================================================================

if __name__ == "__main__":
    print("=== Optional and Union Types Examples ===\n")
    
    # Optional examples
    print("Optional Types:")
    print(f"  Find user 1: {find_user(1)}")
    print(f"  Find user 999: {find_user(999)}")
    print(f"  Greet with name: {greet_user('Alice')}")
    print(f"  Greet without name: {greet_user()}")
    print(f"  Parse '123': {parse_int('123')}")
    print(f"  Parse 'abc': {parse_int('abc')}")
    print()
    
    # Union examples
    print("Union Types:")
    print(f"  Process ID (int): {process_id(42)}")
    print(f"  Process ID (str): {process_id('user-abc')}")
    print(f"  Add 2 + 3: {add_numbers(2, 3)}")
    print(f"  Add 2.5 + 3.5: {add_numbers(2.5, 3.5)}")
    print(f"  Format int: {format_value(42)}")
    print(f"  Format float: {format_value(3.14159)}")
    print(f"  Format str: {format_value('hello')}")
    print()
    
    # Type narrowing
    print("Type Narrowing:")
    print(f"  Process list: {process_data([1, 2, 3, 4])}")
    print(f"  Process dict: {process_data({'a': 1, 'b': 2})}")
    print()
    
    # Complex patterns
    print("Complex Patterns:")
    print(f"  Get tags (exists): {get_tags(1)}")
    print(f"  Get tags (missing): {get_tags(3)}")
    parsed = parse_numbers(["1", "2", "abc", "3"])
    print(f"  Parse numbers: {parsed}")
    print()
    
    # Practical examples
    print("Practical Examples:")
    print(f"  Safe divide 10/2: {safe_divide(10, 2)}")
    print(f"  Safe divide 10/0: {safe_divide(10, 0)}")
    print(f"  Safe divide 10/0 (default 0): {safe_divide(10, 0, 0.0)}")
    nums = extract_numbers("I have 3 apples and 2.5 oranges")
    print(f"  Extract numbers: {nums}")
    avg = calculate_average([1, 2.5, 3, 4.5])
    print(f"  Average: {avg}")
```

---

## Exercises

**Exercise 1.** Write a function `find_user(user_id: int) -> Optional[str]` that returns a name if the user exists or `None` otherwise. Simulate with a dictionary lookup.

??? success "Solution to Exercise 1"
    ```python
    from typing import Optional

    USERS = {1: "Alice", 2: "Bob"}

    def find_user(user_id: int) -> Optional[str]:
        return USERS.get(user_id)

    print(find_user(1))  # Alice
    print(find_user(99)) # None
    ```

---

**Exercise 2.** Rewrite `Union[int, float, str]` using the modern `|` syntax (Python 3.10+). Then write a function `stringify(value: int | float | str) -> str` that converts any of those types to a string.

??? success "Solution to Exercise 2"
    ```python
    def stringify(value: int | float | str) -> str:
        return str(value)

    print(stringify(42))      # "42"
    print(stringify(3.14))    # "3.14"
    print(stringify("hello")) # "hello"
    ```

---

**Exercise 3.** Predict whether `mypy` reports an error:

```python
from typing import Optional

def greet(name: Optional[str]) -> str:
    return "Hello, " + name
```

??? success "Solution to Exercise 3"
    Yes, `mypy` reports an error. `name` has type `Optional[str]` (i.e., `str | None`), so concatenating with `+` could fail if `name` is `None`. The fix is to check for `None` first:

    ```python
    def greet(name: Optional[str]) -> str:
        if name is None:
            return "Hello, stranger"
        return "Hello, " + name
    ```

---

**Exercise 4.** Write a function `safe_divide(a: float, b: float) -> float | None` that returns `None` instead of raising `ZeroDivisionError`. Annotate it properly and write a caller that handles the `None` case.

??? success "Solution to Exercise 4"
    ```python
    def safe_divide(a: float, b: float) -> float | None:
        if b == 0:
            return None
        return a / b

    result = safe_divide(10, 3)
    if result is not None:
        print(f"Result: {result:.2f}")
    else:
        print("Cannot divide by zero")
    ```
