
# help() and dir()

These are **introspection tools**---they let you examine Python objects at runtime. `help()` displays an object's documentation; `dir()` lists its available attributes and methods. They are especially useful when working with unfamiliar objects or libraries, allowing you to explore without leaving the interpreter.

!!! tip "Mental Model"
    `dir()` is the table of contents---it shows what an object can do. `help()` is the manual---it explains how each capability works. When you encounter an unfamiliar object, use `dir()` to discover its interface and `help()` to understand the details.

## help()

Displays the built-in documentation for any Python object, including functions, modules, and classes.

```python
help(print)
```

## dir()

Lists all attributes and methods available on a given object or type.

```python
dir(str)
```

This returns a list of all string methods and attributes:

```
['capitalize', 'count', 'encode', 'find', 'lower', ...]
```

## Practical Example

```python
x = "Python"

print(dir(x))
```

These tools help developers **discover available functionality**.

---

## Practical Example

```python
# Exploring an unfamiliar library
import math

print(dir(math))          # discover available functions
help(math.sqrt)           # learn how sqrt works
```

---

## Exercises

**Exercise 1.**
`dir()` reveals more than user-defined attributes. Predict the output:

```python
x = 42
print("__add__" in dir(x))
print("__len__" in dir(x))
print("bit_length" in dir(x))
```

Why does an integer have `__add__` but not `__len__`? What do the double-underscore ("dunder") methods represent?

??? success "Solution to Exercise 1"
    Output:

    ```text
    True
    False
    True
    ```

    `__add__` is present because `+` on integers calls `int.__add__`. The dunder (double-underscore) methods are Python's **data model methods** -- they implement operators and built-in function behavior. `+` calls `__add__`, `len()` calls `__len__`, `str()` calls `__str__`, etc.

    `__len__` is absent because integers are not containers -- they have no length. `len(42)` raises `TypeError`. Only sequences and containers (lists, strings, dicts, etc.) define `__len__`.

    `bit_length` is a regular method specific to `int` that returns the number of bits needed to represent the integer.

---

**Exercise 2.**
`dir()` with no arguments shows the current namespace. Predict the output:

```python
x = 10
y = 20
names = dir()
print("x" in names)
print("y" in names)
print("__name__" in names)
```

Why does `__name__` appear in `dir()` even though you did not define it? Where does it come from?

??? success "Solution to Exercise 2"
    Output:

    ```text
    True
    True
    True
    ```

    `dir()` with no arguments returns the names in the current scope. At module level, this includes all variables you defined (`x`, `y`) plus built-in module attributes like `__name__`, `__doc__`, `__builtins__`, etc.

    `__name__` is automatically set by Python for every module. When a script runs directly, `__name__` is `"__main__"`. When imported, it is the module's name. These automatic attributes are part of the module namespace, visible via `dir()`.

---

**Exercise 3.**
`help()` retrieves the docstring of an object. Predict the output:

```python
def greet(name):
    """Say hello to someone."""
    return f"Hello, {name}!"

print(greet.__doc__)
print(type(greet.__doc__))
```

Why is the docstring stored as `__doc__`? How does `help()` use this attribute to generate its output?

??? success "Solution to Exercise 3"
    Output:

    ```text
    Say hello to someone.
    <class 'str'>
    ```

    The first string literal in a function body is stored as the function's `__doc__` attribute. `help(greet)` reads `greet.__doc__` and formats it along with the function signature.

    `__doc__` is a regular string attribute that is writable -- you can even change it at runtime with `greet.__doc__ = "new docs"`. This is Python's convention for attaching documentation directly to objects, making it accessible programmatically (not just in source comments).
