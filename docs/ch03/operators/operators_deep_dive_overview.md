# Operators Overview

Operators are special symbols that perform operations on values (operands). Python provides several categories of operators.

!!! tip "Mental Model"
    Every Python operator is syntactic sugar for a method call: `a + b` calls `a.__add__(b)`, `a == b` calls `a.__eq__(b)`, and so on. This means operators work with any type that defines the right dunder method. Understanding this connection explains why `+` can add numbers, concatenate strings, and merge lists -- each type defines its own `__add__`.

## Operators and Operands

```python
result = 10 + 5
#        ^  ^ ^
#        |  | operand
#        |  operator
#        operand
```

- **Operator**: Symbol that performs an operation (`+`, `-`, `*`, etc.)
- **Operand**: Value the operator acts upon


## Operator Categories

| Category | Operators | Example |
|----------|-----------|---------|
| Arithmetic | `+`, `-`, `*`, `/`, `//`, `%`, `**` | `3 + 2` |
| Comparison | `==`, `!=`, `<`, `>`, `<=`, `>=` | `3 > 2` |
| Logical | `and`, `or`, `not` | `True and False` |
| Assignment | `=`, `+=`, `-=`, `*=`, etc. | `x += 1` |
| Bitwise | `&`, `\|`, `^`, `~`, `<<`, `>>` | `5 & 3` |
| Identity | `is`, `is not` | `x is None` |
| Membership | `in`, `not in` | `'a' in 'cat'` |


## Quick Examples

```python
# Arithmetic
print(10 + 3)   # 13
print(10 / 3)   # 3.333...
print(10 // 3)  # 3 (floor division)
print(10 % 3)   # 1 (remainder)
print(2 ** 3)   # 8 (power)

# Comparison
print(5 > 3)    # True
print(5 == 5)   # True

# Logical
print(True and False)  # False
print(True or False)   # True
print(not True)        # False

# Identity
x = [1, 2]
y = [1, 2]
print(x == y)   # True (same value)
print(x is y)   # False (different objects)

# Membership
print('a' in 'cat')     # True
print(3 in [1, 2, 3])   # True
```


## Operator Behavior Depends on Types

The same operator can behave differently based on operand types:

```python
# + with numbers: addition
print(3 + 2)        # 5

# + with strings: concatenation
print("Hello" + " World")  # "Hello World"

# + with lists: concatenation
print([1, 2] + [3, 4])     # [1, 2, 3, 4]

# * with number and string: repetition
print("ab" * 3)     # "ababab"

# * with number and list: repetition
print([1, 2] * 2)   # [1, 2, 1, 2]
```


## Summary

- Operators perform operations on operands
- Python has 7 main operator categories
- Operator behavior can vary by operand type
- See specific pages for details on each category


---

## Exercises


**Exercise 1.**
For the `+` operator, show three different behaviors depending on the operand types: with two integers, with two strings, and with two lists. What determines which behavior is used?

??? success "Solution to Exercise 1"

    ```python
    # Integers: arithmetic addition
    print(3 + 2)              # 5

    # Strings: concatenation
    print("Hello" + " World") # Hello World

    # Lists: concatenation
    print([1, 2] + [3, 4])    # [1, 2, 3, 4]
    ```

    The `+` operator dispatches to the `__add__` method of the left operand. Each type implements `__add__` differently, so behavior depends on the operand's type.

---

**Exercise 2.**
Write a function `type_aware_multiply(a, b)` that checks the types of its arguments and returns a meaningful result: numeric multiplication for numbers, string repetition for `str * int`, and raises `TypeError` for unsupported combinations.

??? success "Solution to Exercise 2"

    ```python
    def type_aware_multiply(a, b):
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return a * b
        elif isinstance(a, str) and isinstance(b, int):
            return a * b
        elif isinstance(a, int) and isinstance(b, str):
            return b * a
        else:
            raise TypeError(f"Cannot multiply {type(a).__name__} and {type(b).__name__}")

    print(type_aware_multiply(3, 4))       # 12
    print(type_aware_multiply("ab", 3))    # ababab
    print(type_aware_multiply(3, "ab"))    # ababab
    ```

    The function uses `isinstance()` to check operand types and delegates to the appropriate behavior.

---

**Exercise 3.**
List all seven Python operator categories and give one example of each. For the membership category, show how `in` works differently with a `list` versus a `dict`.

??? success "Solution to Exercise 3"

    ```python
    # 1. Arithmetic
    print(10 + 3)             # 13

    # 2. Comparison
    print(5 > 3)              # True

    # 3. Logical
    print(True and False)     # False

    # 4. Assignment
    x = 10
    x += 5                    # 15

    # 5. Bitwise
    print(5 & 3)              # 1

    # 6. Identity
    print(None is None)       # True

    # 7. Membership
    print(3 in [1, 2, 3])    # True (checks elements)
    d = {'a': 1, 'b': 2}
    print('a' in d)           # True (checks keys, not values)
    ```

    For lists, `in` checks if the value is an element. For dicts, `in` checks if the value is a key.
