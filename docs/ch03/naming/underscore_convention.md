# Underscore Convention

!!! tip "Mental Model"
    Underscores in Python names are signals with increasing strength: `_x` means "internal, please don't touch," `__x` triggers name mangling to avoid subclass collisions, `__x__` is reserved for Python's own special methods, and a bare `_` means "I don't care about this value." Memorize these four patterns and you can read any Python naming convention at a glance.

## Single Leading

### 1. Throwaway Variable

```python
# Loop without using variable
for _ in range(5):
    print("Hello")

# Unpacking ignored values
_, status_code, _ = ("HTTP", 200, "OK")

# With star
first, *_, last = range(10)
```

### 2. Weak Private

Suggests internal use:

```python
# Module-level
_internal_cache = {}
_helper = lambda x: x * 2

# Class attribute  
class MyClass:
    def __init__(self):
        self._internal = 42
```

## Double Leading

### 1. Name Mangling

Triggers name mangling in classes:

```python
class MyClass:
    def __init__(self):
        self.__private = 42  # Mangled

obj = MyClass()
# obj.__private  # AttributeError
print(obj._MyClass__private)  # 42
```

### 2. Prevents Override

```python
class Base:
    def __init__(self):
        self.__setup()  # Calls Base.__setup
    
    def __setup(self):
        print("Base setup")

class Derived(Base):
    def __setup(self):  # Different method
        print("Derived setup")

obj = Derived()  # Prints: Base setup
```

## Dunder Methods

### 1. Magic Methods

Double leading AND trailing:

```python
class MyClass:
    def __init__(self):
        pass
    
    def __str__(self):
        return "MyClass instance"
    
    def __len__(self):
        return 42
```

### 2. Don't Create Own

```python
# Don't do this!
# def __my_method__(self):
#     pass

# Reserved for Python
```

## Trailing Underscore

### 1. Avoid Keywords

```python
# Avoid keyword collision
class_ = "MyClass"
type_ = "custom"
from_ = "source"

def process(type_=None):
    if type_ is None:
        type_ = "default"
    return type_
```

## Summary Table

| Pattern | Use Case | Example |
|---------|----------|---------|
| `_var` | Internal/throwaway | `_cache`, `_` |
| `__var` | Strong private | `__password` |
| `__method__` | Magic | `__init__` |
| `var_` | Avoid keyword | `class_` |

---

## Exercises


**Exercise 1.**
Explain the meaning of each underscore convention: `_var`, `var_`, `__var`, `__var__`, and `_`. Give an example use case for each.

??? success "Solution to Exercise 1"

    | Convention | Meaning | Example |
    |-----------|---------|---------|
    | `_var` | Internal/private by convention | `_helper_function()` |
    | `var_` | Avoids conflict with keyword | `class_`, `type_` |
    | `__var` | Name mangling in classes | `self.__balance` |
    | `__var__` | Dunder/magic methods | `__init__`, `__str__` |
    | `_` | Throwaway variable | `for _ in range(5)` |

---

**Exercise 2.**
Demonstrate Python's name mangling for `__var` inside a class. Create a class with a `__secret` attribute and show how to access it from outside the class.

??? success "Solution to Exercise 2"

        ```python
        class BankAccount:
            def __init__(self, balance):
                self.__balance = balance  # Name-mangled

            def get_balance(self):
                return self.__balance

        acc = BankAccount(100)
        # print(acc.__balance)           # AttributeError
        print(acc._BankAccount__balance)  # 100 (mangled name)
        print(acc.get_balance())          # 100
        ```

    Python mangles `__balance` to `_BankAccount__balance` to avoid accidental overrides in subclasses.

---

**Exercise 3.**
Write a loop that uses `_` as a throwaway variable and a function that uses `_` in the interactive interpreter convention.

??? success "Solution to Exercise 3"

        ```python
        # Throwaway variable in loop
        for _ in range(3):
            print("Hello")

        # Ignoring values in unpacking
        name, _, age = ("Alice", "ignored", 30)
        print(f"{name}, {age}")  # Alice, 30
        ```

    `_` signals to readers that the value is intentionally unused.
