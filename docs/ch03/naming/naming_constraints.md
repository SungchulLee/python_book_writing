# Naming Constraints

Python identifiers (variable names, function names, class names) must follow specific rules.

!!! tip "Mental Model"
    A valid Python name starts with a letter or underscore, followed by any combination of letters, digits, and underscores. No spaces, no hyphens, no leading digits. Python 3 extends "letter" to include Unicode, so `cafe` and `nombre` are valid, but sticking to ASCII keeps code portable and readable.

## Basic Rules

### First Character

Valid first characters:

- Letters: `A-Z`, `a-z`
- Underscore: `_`

Invalid first characters:

- Digits: `0-9`

```python
# Valid
name = "Alice"
_private = 42
Name = "Bob"

# Invalid
# 2speed = 60      # SyntaxError
# 123var = "data"  # SyntaxError
# 1st_place = True # SyntaxError
```


### Subsequent Characters

After the first character, you can use:

- Letters: `A-Z`, `a-z`
- Digits: `0-9`
- Underscore: `_`

Not allowed anywhere:

- Spaces
- Hyphens: `-`
- Special characters: `@`, `#`, `$`, etc.

```python
# Valid
user123 = "Alice"
data_2024 = [1, 2, 3]
my_var_123 = True

# Invalid
# user-name = "Alice"  # SyntaxError
# user name = "Bob"    # SyntaxError
# user@host = "data"   # SyntaxError
# price$ = 100         # SyntaxError
```


## Case Sensitivity

Python distinguishes between uppercase and lowercase.

```python
Data = 100
data = 200
DATA = 300

print(f"{Data = }")  # Data = 100
print(f"{data = }")  # data = 200
print(f"{DATA = }")  # DATA = 300
```

Common mistake:

```python
name = "Alice"
# Later...
print(Name)  # NameError: name 'Name' is not defined
```


## Reserved Keywords

Python keywords cannot be used as identifiers.

```python
import keyword
print(keyword.kwlist)
```

Common keywords:

- Control flow: `if`, `else`, `elif`, `for`, `while`, `break`, `continue`
- Functions: `def`, `return`, `lambda`, `yield`
- Classes: `class`, `pass`
- Logic: `and`, `or`, `not`, `in`, `is`
- Constants: `True`, `False`, `None`
- Exceptions: `try`, `except`, `finally`, `raise`
- Imports: `import`, `from`, `as`
- Context: `with`, `async`, `await`

```python
# All invalid - SyntaxError
# class = "MyClass"
# def = 42
# for = [1, 2, 3]
# None = 10
# True = False
```


## Special Patterns

### Single Underscore

Used for throwaway variables.

```python
# Loop counter you don't need
for _ in range(5):
    print("Hello")

# Unpacking values you don't need
_, status, _ = ("GET", 200, "OK")
```


### Leading Underscore

Convention for private/internal names.

```python
_private = 42
_internal_helper = lambda x: x * 2
```


### Double Leading Underscore

Triggers name mangling in classes.

```python
class MyClass:
    def __init__(self):
        self.__private = 42  # Becomes _MyClass__private
```


### Dunder (Double Underscore Both Sides)

Reserved for special methods.

```python
class MyClass:
    def __init__(self):
        pass
    
    def __str__(self):
        return "MyClass instance"
    
    def __len__(self):
        return 0
```


## Edge Cases

### Looks Invalid But Valid

```python
# All underscores - valid
_ = 42
__ = "data"
___ = [1, 2, 3]
___private___ = True
```


### Looks Valid But Reserved

```python
# These look like valid names but are keywords
# None = 10     # SyntaxError
# True = False  # SyntaxError
# pass = 42     # SyntaxError
```


## Validating Identifiers

### Using `isidentifier()`

```python
print("valid_name".isidentifier())   # True
print("2invalid".isidentifier())     # False
print("user-name".isidentifier())    # False
print("class".isidentifier())        # True (but reserved!)
```

Note: `isidentifier()` returns `True` for keywords, so additional checking is needed.


### Checking for Keywords

```python
import keyword

name = "class"
if keyword.iskeyword(name):
    print(f"'{name}' is a reserved keyword!")
```


### Complete Validation

```python
import keyword

def is_valid_identifier(name):
    """Check if name is a valid, non-reserved identifier."""
    return name.isidentifier() and not keyword.iskeyword(name)

# Test
print(is_valid_identifier("valid_name"))  # True
print(is_valid_identifier("class"))       # False (keyword)
print(is_valid_identifier("2bad"))        # False (starts with digit)
print(is_valid_identifier("user-name"))   # False (contains hyphen)
```


### Batch Testing

```python
import keyword

tests = [
    "valid_name",
    "_private",
    "__dunder__",
    "var123",
    "2invalid",
    "user-name",
    "class",
    "None",
]

for name in tests:
    valid = name.isidentifier()
    is_kw = keyword.iskeyword(name)
    
    if is_kw:
        status = "❌ Reserved keyword"
    elif valid:
        status = "✅ Valid"
    else:
        status = "❌ Invalid syntax"
    
    print(f"{name:15} {status}")
```

Output:
```
valid_name      ✅ Valid
_private        ✅ Valid
__dunder__      ✅ Valid
var123          ✅ Valid
2invalid        ❌ Invalid syntax
user-name       ❌ Invalid syntax
class           ❌ Reserved keyword
None            ❌ Reserved keyword
```


## Quick Reference

| Pattern | Valid? | Reason |
|---------|--------|--------|
| `name` | ✅ | Standard identifier |
| `_name` | ✅ | Private convention |
| `__name` | ✅ | Name mangling |
| `__name__` | ✅ | Dunder/magic |
| `Name` | ✅ | Capitalized |
| `NAME` | ✅ | Constant convention |
| `name123` | ✅ | Digits after first char |
| `name_var` | ✅ | Underscore separator |
| `2name` | ❌ | Starts with digit |
| `name-var` | ❌ | Contains hyphen |
| `name var` | ❌ | Contains space |
| `name@host` | ❌ | Contains special char |
| `class` | ❌ | Reserved keyword |
| `None` | ❌ | Reserved keyword |


## Best Practices

1. **Keep names readable** - Under 30 characters
   ```python
   # Too long
   this_is_an_extremely_long_variable_name = 42
   
   # Better
   max_timeout = 30
   ```

2. **Use snake_case for variables and functions**
   ```python
   user_name = "Alice"
   def calculate_total():
       pass
   ```

3. **Use UPPER_CASE for constants**
   ```python
   MAX_SIZE = 100
   DEFAULT_TIMEOUT = 30
   PI = 3.14159
   ```

4. **Use PascalCase for classes**
   ```python
   class UserAccount:
       pass
   ```

---

## Exercises


**Exercise 1.**
Which of the following are valid Python identifiers? Test each with `str.isidentifier()`.

```python
names = ["my_var", "2things", "_private", "__dunder__", "class", "my-var", "café"]
```

??? success "Solution to Exercise 1"

        ```python
        names = ["my_var", "2things", "_private", "__dunder__", "class", "my-var", "café"]

        for name in names:
            print(f"{name:>12}: {name.isidentifier()}")
        ```

    `my_var`, `_private`, `__dunder__`, `class`, and `café` are valid identifiers. `2things` (starts with digit) and `my-var` (contains hyphen) are not. Note that `class` is a valid identifier but is a reserved keyword.

---

**Exercise 2.**
Explain the rules for valid Python identifiers: what characters can they start with, and what characters can follow?

??? success "Solution to Exercise 2"

    Python identifiers must:

    - Start with a letter (a-z, A-Z) or underscore (`_`)
    - Followed by zero or more letters, digits (0-9), or underscores
    - Not be a keyword (though `isidentifier()` returns `True` for keywords)
    - Unicode letters are allowed (e.g., `café`, `变量`)

---

**Exercise 3.**
Write a function `sanitize_name(s)` that converts an arbitrary string into a valid Python identifier by replacing invalid characters with underscores and prepending `_` if it starts with a digit.

??? success "Solution to Exercise 3"

        ```python
        import keyword

        def sanitize_name(s):
            result = ""
            for i, ch in enumerate(s):
                if i == 0 and ch.isdigit():
                    result += "_" + ch
                elif ch.isalnum() or ch == "_":
                    result += ch
                else:
                    result += "_"
            if not result:
                result = "_"
            if keyword.iskeyword(result):
                result += "_"
            return result

        print(sanitize_name("2things"))    # _2things
        print(sanitize_name("my-var"))     # my_var
        print(sanitize_name("class"))      # class_
        ```
