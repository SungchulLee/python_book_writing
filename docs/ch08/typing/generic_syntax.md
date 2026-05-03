# List[int] vs list[int] - Generic Types

Generic types can be specified using either typing module classes (List[int]) or built-in types (list[int], available in Python 3.9+).

!!! tip "Mental Model"
    Before Python 3.9, you had to import capitalized generics from `typing` (`List[int]`, `Dict[str, int]`). From 3.9 onward, the built-in types themselves accept subscripts (`list[int]`, `dict[str, int]`). The two forms mean exactly the same thing — prefer the lowercase built-in syntax in new code and use the `typing` imports only when supporting older Python versions.

## Legacy Typing Module Syntax

Before Python 3.9, use types from the typing module for generic annotations.

```python
from typing import List, Dict, Set, Tuple

# Pre-3.9 style using typing module
numbers: List[int] = [1, 2, 3]
mapping: Dict[str, int] = {"a": 1, "b": 2}
unique: Set[str] = {"x", "y", "z"}
pair: Tuple[int, str] = (1, "one")

print(numbers, mapping, unique, pair)
```

```
[1, 2, 3] {'a': 1, 'b': 2} {'x', 'y', 'z'} (1, 'one')
```

## Modern Built-in Syntax (Python 3.9+)

Starting with Python 3.9, use built-in types directly for generics.

```python
# Python 3.9+ style using built-in types
numbers: list[int] = [1, 2, 3]
mapping: dict[str, int] = {"a": 1, "b": 2}
unique: set[str] = {"x", "y", "z"}
pair: tuple[int, str] = (1, "one")

print(numbers, mapping, unique, pair)
```

```
[1, 2, 3] {'a': 1, 'b': 2} {'x', 'y', 'z'} (1, 'one')
```

## When to Use Each Style

Choose based on your Python version and codebase consistency.

```python
# New code with Python 3.9+: prefer built-in syntax
def process(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

result = process(["cat", "elephant", "dog"])
print(result)

# Use typing module for complex types
from typing import Callable
callback: Callable[[int], str] = str
print(callback(42))
```

```
{'cat': 3, 'elephant': 8, 'dog': 3}
42
```


---

## Exercises

**Exercise 1.** Rewrite the following annotation using the modern `list[int]` syntax instead of `List[int]`:

```python
from typing import List, Dict, Tuple
def process(data: List[int]) -> Dict[str, Tuple[int, ...]]:
    pass
```

??? success "Solution to Exercise 1"
    ```python
    def process(data: list[int]) -> dict[str, tuple[int, ...]]:
        pass
    ```

---

**Exercise 2.** Write a function `first_element(items: list[str]) -> str` that returns the first element. What Python version is required to use `list[str]` instead of `List[str]`?

??? success "Solution to Exercise 2"
    ```python
    def first_element(items: list[str]) -> str:
        return items[0]

    print(first_element(["a", "b", "c"]))  # "a"
    ```

    Python 3.9+ is required. In 3.8 and earlier, you must use `from typing import List` and write `List[str]`.

---

**Exercise 3.** Predict whether the following code works in Python 3.9+ and in Python 3.8:

```python
def keys_and_values(d: dict[str, int]) -> tuple[list[str], list[int]]:
    return list(d.keys()), list(d.values())
```

??? success "Solution to Exercise 3"
    In Python 3.9+, this works perfectly. In Python 3.8, it raises a `TypeError` at runtime because built-in types like `dict` and `tuple` do not support subscript syntax for type hints. To make it work in 3.8, use `from __future__ import annotations` or import from `typing`.

---

**Exercise 4.** Explain the purpose of `from __future__ import annotations` and how it allows using modern syntax in older Python versions.

??? success "Solution to Exercise 4"
    `from __future__ import annotations` (PEP 563) makes all annotations lazy — they are stored as strings and not evaluated at runtime. This means you can use `list[int]`, `dict[str, int]`, etc., even in Python 3.7+, because the subscript expression is never actually executed. The annotations are only evaluated when a tool like `mypy` or `typing.get_type_hints()` processes them.
