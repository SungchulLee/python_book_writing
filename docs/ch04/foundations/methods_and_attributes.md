# Methods and Attributes

In Python, an **attribute** is a property or value linked to an object, while a **method** is a callable function bound to an object. Since everything in Python is an object, even primitive types like `int`, `float`, and `str` have methods and attributes.

!!! tip "Mental Model"
    Every Python object carries a bag of named references called attributes. Some of those references point to callable objects -- those are methods. Use `dir()` to peek inside the bag and `help()` to read the label on any item.

---

## Discovering Methods and Attributes

Use `dir()` to see all methods and attributes of any object:

```python
print(dir(float))
print(dir(int))
print(dir(str))
```

Use `help()` for documentation:

```python
help(str.upper)
```

---

## `float` Type

### Storage: IEEE 754

Python floats are 64-bit double-precision (IEEE 754):

| Component | Bits |
|-----------|------|
| Sign | 1 |
| Exponent | 11 |
| Mantissa | 52 |
| **Total** | **64** |

```python
mantissa_bits = 52
exponent_bits = 11
sign_bit = 1
total = mantissa_bits + exponent_bits + sign_bit
print(f"Float size: {total} bits")  # 64 bits
```

### Precision Limitations

Floats have finite precision:

```python
print(0.1 + 0.2)        # 0.30000000000000004 (not 0.3!)
print(0.1 + 0.2 == 0.3) # False
```

For exact decimals, use `decimal.Decimal`:

```python
from decimal import Decimal
print(Decimal('0.1') + Decimal('0.2'))  # 0.3
```

### Float Methods

```python
x = 3.14

x.is_integer()          # False (not a whole number)
(4.0).is_integer()      # True

x.as_integer_ratio()    # (7070651414971679, 2251799813685248)

x.hex()                 # '0x1.91eb851eb851fp+1'
```

### Float Attributes

```python
x = 3.14
print(x.real)           # 3.14 (real part)
print(x.imag)           # 0.0 (imaginary part)
```

### Comparing Floats

Use tolerance for comparison:

```python
a = 0.1 + 0.2
b = 0.3

# Wrong
print(a == b)                   # False

# Correct
print(abs(a - b) < 1e-9)        # True

# Or use math.isclose
import math
print(math.isclose(a, b))       # True
```

---

## `int` Type

### Storage: Arbitrary Precision

Python integers have **no size limit** — they grow as needed:

```python
big = 31415926535897932384626433832795028841971693993751058209749445923078164062
print(big)
print(type(big))        # <class 'int'>
```

No overflow errors like in C/Java.

### Integer Methods

```python
n = 42

n.bit_length()          # 6 (bits needed to represent 42)
n.bit_count()           # 3 (number of 1s in binary: 101010)

(255).to_bytes(2, 'big')    # b'\x00\xff'
int.from_bytes(b'\x00\xff', 'big')  # 255
```

### Integer Attributes

```python
n = 42
print(n.real)           # 42
print(n.imag)           # 0
print(n.numerator)      # 42
print(n.denominator)    # 1
```

### Integer Operations

```python
print(10 // 3)          # 3 (floor division)
print(10 % 3)           # 1 (modulus)
print(divmod(10, 3))    # (3, 1) (quotient, remainder)
print(2 ** 10)          # 1024 (exponentiation)
```

---

## `str` Type

### Storage: UTF-8 Encoding

Python strings are Unicode, encoded as UTF-8:

| Character Type | Bytes | Example |
|----------------|-------|---------|
| ASCII | 1 | `A`, `9`, `!` |
| Latin Extended | 2 | `é`, `ß`, `ø` |
| CJK (Korean, Chinese, Japanese) | 3 | `안`, `你`, `日` |
| Emoji | 4 | `😊`, `🚀` |

```python
# ASCII string
a = "Hello"
print(len(a))                       # 5 characters
print(len(a.encode('utf-8')))       # 5 bytes

# Korean string
b = "안녕"
print(len(b))                       # 2 characters
print(len(b.encode('utf-8')))       # 6 bytes (3 per character)

# Emoji
c = "😊"
print(len(c))                       # 1 character
print(len(c.encode('utf-8')))       # 4 bytes
```

### String Methods (Selection)

```python
s = "Hello World"

# Case methods
s.upper()               # 'HELLO WORLD'
s.lower()               # 'hello world'
s.title()               # 'Hello World'
s.capitalize()          # 'Hello world'

# Search methods
s.find('World')         # 6 (index)
s.count('l')            # 3
s.startswith('Hello')   # True
s.endswith('World')     # True

# Modify methods
s.replace('World', 'Python')  # 'Hello Python'
s.strip()               # Remove whitespace
s.split()               # ['Hello', 'World']

# Check methods
'hello'.isalpha()       # True
'123'.isdigit()         # True
'hello123'.isalnum()    # True
```

### String Formatting

```python
name = "Alice"
age = 30

# f-string (recommended)
f"Name: {name}, Age: {age}"

# format method
"Name: {}, Age: {}".format(name, age)

# % formatting (old style)
"Name: %s, Age: %d" % (name, age)
```

---

## Summary: How Types are Stored

| Type | Storage Format | Size | Precision |
|------|----------------|------|-----------|
| `float` | IEEE 754 double | 64 bits | ~15-17 decimal digits |
| `int` | Variable-length binary | Dynamic | Unlimited |
| `str` | UTF-8 Unicode | 1-4 bytes/char | N/A |

---

## Method Types in Classes

Python distinguishes three method types:

### Instance Methods

Operate on specific instances:

```python
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):             # Instance method
        return f"{self.name} says woof!"

dog = Dog("Buddy")
dog.bark()                      # "Buddy says woof!"
```

### Class Methods

Operate on the class itself:

```python
class Dog:
    count = 0
    
    def __init__(self, name):
        self.name = name
        Dog.count += 1
    
    @classmethod
    def get_count(cls):         # Class method
        return cls.count

Dog("Buddy")
Dog("Max")
Dog.get_count()                 # 2
```

### Static Methods

Don't depend on instance or class:

```python
class Math:
    @staticmethod
    def add(a, b):              # Static method
        return a + b

Math.add(2, 3)                  # 5
```

---


## Key Takeaways

- **Attributes**: Properties/values (`x.real`, `x.imag`)
- **Methods**: Callable functions (`x.is_integer()`, `s.upper()`)
- `dir(obj)` shows all methods and attributes
- `float`: 64-bit IEEE 754, finite precision, use `Decimal` for exactness
- `int`: Arbitrary precision, no overflow
- `str`: UTF-8 encoded, 1-4 bytes per character
- Python has instance methods, class methods (`@classmethod`), and static methods (`@staticmethod`)


## Exercises

**Exercise 1.**
Even "primitive" types have methods and attributes in Python. Predict the output:

```python
x = 7
print(x.bit_length())
print((255).bit_length())
print((0).bit_length())

y = 3.14
print(y.is_integer())
print((4.0).is_integer())
print(y.as_integer_ratio())
```

Why can you call methods on integer and float literals? What does this reveal about how Python treats "primitive" types compared to languages like C or Java?

??? success "Solution to Exercise 1"
    Output:

    ```text
    3
    8
    0
    False
    True
    (7070651414971679, 2251799813685248)
    ```

    In Python, integers, floats, and strings are all **full objects** with methods and attributes. There are no "primitives" in the C/Java sense. `7` is an instance of `int`, and `int` is a class with methods like `.bit_length()`, `.to_bytes()`, etc.

    You can call methods on literals because the literal syntax creates an object just like `int(7)` would. `(255).bit_length()` returns 8 because 255 = 11111111 in binary (8 bits). `(0).bit_length()` returns 0 because zero needs zero bits.

    `as_integer_ratio()` returns the exact numerator and denominator that represent the float's stored value. For `3.14`, this is not `314/100` but the exact binary fraction, revealing floating-point representation.

---

**Exercise 2.**
`dir()` reveals the full method set of any object. Predict the output:

```python
print("__add__" in dir(int))
print("__add__" in dir(str))
print("__add__" in dir(list))

print(int.__add__(5, 3))
print(str.__add__("hello", " world"))
```

Why do `int`, `str`, and `list` all have `__add__`? What is the relationship between the `+` operator and the `__add__` method? How does Python use these "dunder" methods to implement operators?

??? success "Solution to Exercise 2"
    Output:

    ```text
    True
    True
    True
    8
    hello world
    ```

    `int`, `str`, and `list` all define `__add__` because the `+` operator is syntactic sugar for calling `__add__`. When Python evaluates `5 + 3`, it calls `(5).__add__(3)`. When it evaluates `"hello" + " world"`, it calls `"hello".__add__(" world")`.

    This is Python's **operator overloading** via the **data model** (also called the "dunder protocol"). Every operator maps to a dunder method: `+` → `__add__`, `-` → `__sub__`, `*` → `__mul__`, `[]` → `__getitem__`, `len()` → `__len__`, etc. This is why custom classes can support `+` by defining `__add__`.

---

**Exercise 3.**
Instance methods, class methods, and static methods receive different first arguments. Predict the output:

```python
class Demo:
    class_var = "shared"

    def instance_method(self):
        return type(self).__name__

    @classmethod
    def class_method(cls):
        return cls.class_var

    @staticmethod
    def static_method():
        return "no self, no cls"

d = Demo()
print(d.instance_method())
print(Demo.class_method())
print(Demo.static_method())
print(d.class_method())
print(d.static_method())
```

Why can you call `class_method` and `static_method` on both the class and the instance? What does each decorator actually do to the function?

??? success "Solution to Exercise 3"
    Output:

    ```text
    Demo
    shared
    no self, no cls
    shared
    no self, no cls
    ```

    All three method types can be called on instances. The difference is what gets passed as the first argument:

    - **Instance method**: Python automatically passes the instance as `self`. Must be called on an instance (or explicitly: `Demo.instance_method(d)`).
    - **Class method** (`@classmethod`): Python automatically passes the **class** as `cls`, regardless of whether called on the class or an instance. Useful for alternative constructors.
    - **Static method** (`@staticmethod`): Python passes **nothing** automatically. It is a plain function that lives inside the class namespace for organizational purposes.

    `@classmethod` and `@staticmethod` are **descriptors** -- they wrap the function and intercept the attribute access to modify how arguments are passed. This is part of Python's descriptor protocol.
