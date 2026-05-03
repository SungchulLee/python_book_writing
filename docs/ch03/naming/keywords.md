# Reserved Keywords

!!! tip "Mental Model"
    Keywords are names the parser has claimed for itself -- `if`, `def`, `class`, `return`, and about 30 others. Unlike built-in names, keywords cannot be used as variable names at all; attempting to do so is a `SyntaxError`. Use `keyword.kwlist` to see the full list and `keyword.iskeyword()` to check any name.

## View Keywords

### 1. List All

```python
import keyword

# Get all keywords
print(keyword.kwlist)

# Count
print(len(keyword.kwlist))
```

### 2. Check Keyword

```python
import keyword

print(keyword.iskeyword('class'))   # True
print(keyword.iskeyword('myvar'))   # False
```

## Control Flow

### 1. Conditionals

```python
# if, elif, else
if x > 0:
    pass
elif x == 0:
    pass
else:
    pass

# Cannot use
# if = 5      # SyntaxError
```

### 2. Loops

```python
# for, while, break, continue
for i in range(10):
    if i == 5:
        break
    if i % 2:
        continue

# Cannot use
# for = 10     # SyntaxError
# while = 5    # SyntaxError
```

## Functions

### 1. Definition

```python
# def, class, return
def my_function():
    return 42

class MyClass:
    pass

# Cannot use
# def = 5      # SyntaxError  
# class = 10   # SyntaxError
```

### 2. Lambda

```python
# lambda
square = lambda x: x**2

# Cannot use
# lambda = 5  # SyntaxError
```

## Boolean

### 1. Values

```python
# True, False, None
is_valid = True
result = None

# Cannot reassign
# True = 1   # SyntaxError
# None = 0   # SyntaxError
```

### 2. Operators

```python
# and, or, not
if x > 0 and x < 10:
    pass

if not is_empty:
    pass

# Cannot use
# and = True   # SyntaxError
```

## Exception Handling

### 1. Try Block

```python
# try, except, finally, raise
try:
    risky_operation()
except ValueError:
    handle_error()
finally:
    cleanup()
```

### 2. Assert

```python
# assert
assert x > 0, "Must be positive"

# Cannot use
# assert = True  # SyntaxError
```

## Import

### 1. Statements

```python
# import, from, as
import math
from os import path
import numpy as np

# Cannot use
# import = 1   # SyntaxError
```

## Scope

### 1. Global/Nonlocal

```python
# global
count = 0

def increment():
    global count
    count += 1

# nonlocal
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 1
```

## Complete List

### 1. All Keywords

```
False      await      else       import     pass
None       break      except     in         raise
True       class      finally    is         return
and        continue   for        lambda     try
as         def        from       nonlocal   while
assert     del        global     not        with
async      elif       if         or         yield
```

## Workarounds

### 1. Trailing Underscore

```python
# Use trailing underscore
class_ = "MyClass"
type_ = "data"
from_ = "source"
```

### 2. Different Word

```python
# Instead of 'class'
klass = MyClass
cls = MyClass

# Instead of 'type'
data_type = "string"
kind = "integer"
```

---

## Exercises


**Exercise 1.**
Write code that lists all Python keywords using the `keyword` module. How many are there in your Python version?

??? success "Solution to Exercise 1"

        ```python
        import keyword

        print(keyword.kwlist)
        print(f"Total keywords: {len(keyword.kwlist)}")
        ```

    Python 3.12 has 35 keywords. The exact number may vary by version.

---

**Exercise 2.**
What happens when you try to use `class`, `return`, or `for` as a variable name? Demonstrate the error.

??? success "Solution to Exercise 2"

        ```python
        # All of these cause SyntaxError:
        # class = 5
        # return = 10
        # for = "hello"

        # SyntaxError: invalid syntax
        ```

    Keywords are reserved by the parser. Using them as identifiers causes `SyntaxError` at compile time.

---

**Exercise 3.**
Some words that look like keywords are actually built-in names (e.g., `True`, `False`, `None`). Verify which of these are keywords using `keyword.iskeyword()` and which are just built-in constants.

??? success "Solution to Exercise 3"

        ```python
        import keyword

        for name in ["True", "False", "None", "print", "len"]:
            is_kw = keyword.iskeyword(name)
            print(f"{name:>6}: keyword={is_kw}")
        ```

    `True`, `False`, and `None` are keywords (since Python 3). `print` and `len` are built-in names, not keywords -- they can be reassigned (though doing so is not recommended).
