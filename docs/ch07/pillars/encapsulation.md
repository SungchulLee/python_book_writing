# Encapsulation

Encapsulation controls how an object's state can be accessed and modified, ensuring that all mutations go through well-defined interfaces. The goal is not merely to hide data, but to **protect invariants** --- making invalid states impossible. Encapsulation works alongside [abstraction](abstraction.md) (defining stable interfaces), [inheritance](inheritance.md) (sharing structure), and [polymorphism](polymorphism.md) (enabling flexibility).

---

## What is Encapsulation

Encapsulation is the mechanism of restricting access to certain details and controlling access to an object's data.

### 1. Bundling Data

```python
class Person:
    def __init__(self, name, age):
        self.__name = name  # private
        self.__age = age    # private
```

Data and methods are bundled into a single unit.

### 2. Controlled Access

```python
def get_name(self):
    return self.__name

def set_age(self, age):
    if 0 < age < 120:
        self.__age = age
```

Access is controlled through public methods.

### 3. Information Hiding

Internal implementation details are hidden from the outside.

---

## Access Levels

### 1. Public Attributes

```python
class Hello:
    def __init__(self):
        self.a = 1  # public
```

Accessible from anywhere.

### 2. Weak Private (`_`)

```python
class Hello:
    def __init__(self):
        self._b = 2  # weak private
```

Convention: internal use only, but still accessible.

### 3. Private (`__`)

```python
class Hello:
    def __init__(self):
        self.__c = 3  # private
```

Name mangling prevents direct external access.

---

## Name Mangling (`__`)

### 1. Not Truly Private

Python has no true access control like Java or C++. Double-underscore attributes are **name-mangled**, not locked. `self.__name` becomes `self._ClassName__name` internally, which discourages accidental access but does not prevent it.

```python
class Person:
    def __init__(self, name):
        self.__name = name

person = Person("John")
# person.__name             # AttributeError (mangled name)
print(person._Person__name)  # "John" — still accessible
```

### 2. Use Getter Methods

```python
class Person:
    def __init__(self, name):
        self.__name = name
    
    def get_name(self):
        return self.__name

person = Person("John")
print(person.get_name())  # Works
```

### 3. Use Setter Methods

```python
def set_age(self, age):
    if 0 < age < 120:
        self.__age = age
    else:
        raise ValueError("Invalid age")
```

Setters enable validation logic.

---

## Private Methods

Name mangling applies to methods exactly the same way as attributes --- `__method` becomes `_ClassName__method`.

### 1. Internal Logic

```python
class Hello:
    def __print_c(self):  # name-mangled method
        print(self.__c)
```

Intended for internal use only, but not truly hidden.

### 2. Mangled, Not Inaccessible

```python
m = Hello()
m.__print_c()            # AttributeError (mangled name)
m._Hello__print_c()      # Works — same mangling as attributes
```

### 3. Expose via Public

```python
def print_c(self):  # public method
    self.__print_c()

m.print_c()  # Works
```

---

## Getters and Setters

### 1. Basic Pattern

```python
class Person:
    def __init__(self, age):
        self.__age = age
    
    def get_age(self):
        return self.__age
    
    def set_age(self, age):
        self.__age = age
```

### 2. With Validation

```python
def set_age(self, age):
    if 0 < age < 120:
        self.__age = age
    else:
        raise ValueError("Invalid age")
```

### 3. Read-Only Attributes

```python
def get_name(self):
    return self.__name
# No setter - read-only
```

---

## Idiomatic Python: `@property`

Java-style `get_x()` / `set_x()` methods work but are not idiomatic in Python. The Pythonic approach is to start with direct attribute access and add `@property` only when validation or computation is needed --- the external API stays the same either way.

### 1. Clean Syntax

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value
```

### 2. Transparent to Callers

```python
t = Temperature(25)
t.celsius = 100      # looks like direct access, but runs validation
print(t.celsius)     # 100
```

### 3. When to Use

- Start with public attributes (`self.x`)
- Add `@property` later if you need validation, computation, or read-only access
- No need to pre-emptively wrap everything in getters/setters

---

## Why Encapsulation

### 1. Data Protection

Prevents accidental modification of internal state.

### 2. Controlled Interface

Changes to internal implementation don't break external code.

### 3. Validation Logic

Setters can enforce business rules and constraints.

---

## Inheritance and Name Mangling

### 1. Mangled Names Do Not Inherit Transparently

Name mangling is per-class: `self.__width` in `Polygon` becomes `self._Polygon__width`, which a subclass cannot access as `self.__width` (that would look for `self._Rectangle__width`).

```python
class Polygon:
    def set_values(self, width, height):
        self.__width = width
        self.__height = height

class Rectangle(Polygon):
    def compute_area(self):
        return self.__width * self.__height  # AttributeError!
```

For attributes that subclasses need, use single-underscore convention (`self._width`) instead.

### 2. Use Public or Protected Methods

```python
class Polygon:
    def set_values(self, width, height):
        self.__width = width
        self.__height = height
    
    def get_width(self):
        return self.__width
    
    def get_height(self):
        return self.__height

class Rectangle(Polygon):
    def compute_area(self):
        return self.get_width() * self.get_height()
```

---

## Key Takeaways

- Encapsulation protects invariants and controls how state changes.
- `_` (single underscore) is the preferred convention for internal attributes.
- `__` (double underscore) triggers name mangling --- discourages access but does not enforce true privacy.
- Use `@property` for idiomatic validation instead of Java-style getters/setters.
- Python relies on **convention and design**, not language-enforced access control.

---

## Runnable Example: `encapsulation_examples.py`

```python
"""
Example 01: Basic Encapsulation

Encapsulation is the concept of bundling data and methods that work on that data
within a class, while controlling access to prevent misuse.
"""

# BAD EXAMPLE - No Encapsulation

# =============================================================================
# Definitions
# =============================================================================

class BankAccountBad:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance  # Anyone can modify this!


# GOOD EXAMPLE - With Encapsulation
class BankAccountGood:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private attribute (name mangling)
    
    def deposit(self, amount):
        """Controlled way to add money"""
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        """Controlled way to remove money"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self):
        """Controlled way to view balance"""
        return self.__balance


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    # BAD EXAMPLE - No encapsulation (problem with no encapsulation)
    bad_account = BankAccountBad("John", 1000)
    print(f"Initial balance: ${bad_account.balance}")

    # Direct access allows invalid operations
    bad_account.balance = -5000  # Negative balance? No validation!
    print(f"After direct modification: ${bad_account.balance}")  # This is bad!

    print("\n" + "=" * 60)
    print("ENCAPSULATION DEMONSTRATION")
    print("=" * 60)

    # GOOD EXAMPLE - Using encapsulated class
    good_account = BankAccountGood("Jane", 1000)
    print(f"\nInitial balance: ${good_account.get_balance()}")
    
    # Must use methods to modify balance
    good_account.deposit(500)
    print(f"After deposit: ${good_account.get_balance()}")
    
    good_account.withdraw(200)
    print(f"After withdrawal: ${good_account.get_balance()}")
    
    # Try invalid operations
    print("\n--- Testing validation ---")
    if not good_account.deposit(-100):
        print("❌ Cannot deposit negative amount")
    
    if not good_account.withdraw(5000):
        print("❌ Cannot withdraw more than balance")
    
    # Try to access private attribute directly
    print("\n--- Testing encapsulation ---")
    try:
        print(good_account.__balance)  # This will fail!
    except AttributeError as e:
        print(f"❌ Cannot access private attribute: {e}")
    
    # Python's name mangling allows this (but you shouldn't do it!)
    print(f"\nName mangled attribute: {good_account._BankAccountGood__balance}")
    print("⚠️  But you shouldn't access it this way!")

"""
KEY TAKEAWAYS:
1. Encapsulation protects data from invalid modifications
2. Use private attributes (double underscore) for internal data
3. Provide public methods for controlled access
4. Validation happens in methods, not everywhere in your code
5. Name mangling makes attributes harder (but not impossible) to access
6. Encapsulation makes code safer and more maintainable
"""
```

---

## Exercises

**Exercise 1.** Create a class `Password` that stores a password in a private attribute `__password`. Provide a `set_password(new_pw)` method that only accepts passwords of at least 8 characters and a `check_password(pw)` method that returns `True` if the given password matches. Do not provide a getter that reveals the stored password.

??? success "Solution to Exercise 1"
    ```python
    class Password:
        def __init__(self, password):
            self.__password = None
            self.set_password(password)

        def set_password(self, new_pw):
            if len(new_pw) < 8:
                raise ValueError("Password must be at least 8 characters")
            self.__password = new_pw

        def check_password(self, pw):
            return pw == self.__password

    p = Password("secure123")
    print(p.check_password("secure123"))  # True
    print(p.check_password("wrong"))      # False

    try:
        p.set_password("short")
    except ValueError as e:
        print(e)  # Password must be at least 8 characters
    ```

---

**Exercise 2.** Predict the output of the following code. Explain how name mangling works.

```python
class Secret:
    def __init__(self):
        self.__value = 42

s = Secret()
print(hasattr(s, '__value'))
print(hasattr(s, '_Secret__value'))
print(s._Secret__value)
```

??? success "Solution to Exercise 2"
    The output is:

    ```
    False
    True
    42
    ```

    Python's name mangling transforms any attribute starting with double underscores (e.g., `__value`) into `_ClassName__value`. Therefore `s.__value` does not exist as a direct attribute (so `hasattr` returns `False`), but `s._Secret__value` does exist. This mechanism discourages accidental access to private attributes but does not make them truly inaccessible.

---

**Exercise 3.** Write a class `Temperature` with a private attribute `__celsius`. Provide a `set_celsius(value)` method that rejects values below absolute zero ($-273.15$). Add a `get_fahrenheit()` method that computes and returns the equivalent Fahrenheit temperature using the formula $F = C \times 9/5 + 32$.

??? success "Solution to Exercise 3"
    ```python
    class Temperature:
        def __init__(self, celsius):
            self.__celsius = None
            self.set_celsius(celsius)

        def set_celsius(self, value):
            if value < -273.15:
                raise ValueError("Temperature below absolute zero")
            self.__celsius = value

        def get_fahrenheit(self):
            return self.__celsius * 9 / 5 + 32

    t = Temperature(100)
    print(t.get_fahrenheit())  # 212.0

    try:
        t.set_celsius(-300)
    except ValueError as e:
        print(e)  # Temperature below absolute zero
    ```

---

**Exercise 4.** A developer writes the following class and claims it uses encapsulation. Identify the flaw and rewrite the class with proper encapsulation.

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
```

??? success "Solution to Exercise 4"
    The flaw is that `self.count` is a public attribute, so any external code can set it to an arbitrary value (e.g., `c.count = -100`), bypassing any validation. A properly encapsulated version uses a private attribute and controlled methods:

    ```python
    class Counter:
        def __init__(self):
            self.__count = 0

        def increment(self):
            self.__count += 1

        def get_count(self):
            return self.__count

    c = Counter()
    c.increment()
    c.increment()
    print(c.get_count())  # 2
    # c.__count = -100  # AttributeError — cannot access directly
    ```

---

**Exercise 5.** Create a class `ReadOnlyList` that wraps a regular Python list in a private attribute. Expose `get(index)` and `length()` methods but do not provide any way to modify the list after construction. Demonstrate that external code cannot add or remove elements.

??? success "Solution to Exercise 5"
    ```python
    class ReadOnlyList:
        def __init__(self, items):
            self.__items = list(items)  # defensive copy

        def get(self, index):
            return self.__items[index]

        def length(self):
            return len(self.__items)

    rol = ReadOnlyList([10, 20, 30])
    print(rol.get(0))     # 10
    print(rol.length())   # 3

    # No way to modify:
    try:
        rol.__items.append(40)
    except AttributeError:
        print("Cannot access private attribute")

    # Even the returned values don't expose the internal list
    ```
