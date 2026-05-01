# Descriptor Introduction

## What Is a Descriptor?

!!! tip "Mental Model"
    Think of descriptors as **hooks inserted into the attribute access pipeline**. When Python encounters a descriptor during attribute lookup, it hands control to the descriptor's methods instead of returning the object directly.

### 1. Definition

A **descriptor** is any object that defines at least one of these three special methods:

- `__get__(self, instance, owner)` - controls **getting** an attribute
- `__set__(self, instance, value)` - controls **setting** an attribute
- `__delete__(self, instance)` - controls **deleting** an attribute

### 2. Key Concept

Descriptors are objects that **live on classes** but manage attribute access for **instances**.

```python
class MyDescriptor:
    def __get__(self, instance, owner):
        return "descriptor value"

class MyClass:
    attr = MyDescriptor()  # Descriptor lives here (class level)

obj = MyClass()
print(obj.attr)  # "descriptor value" (accessed on instance)
```

### 3. Descriptors ARE Python OOP

Everything in Python OOP is built on descriptors:

- `@property` — is a descriptor
- Methods — become bound methods via descriptors
- `classmethod` and `staticmethod` — are descriptors
- ORM fields (Django, SQLAlchemy) — use descriptors

### 4. The Three Rules of Attribute Lookup

Attribute lookup is a **priority competition**. Remember these three rules and everything else follows:

1. **Data descriptor wins** — if the class (via MRO) has a data descriptor for that name, it intercepts the access.
2. **Instance `__dict__` wins** — if there is no data descriptor, the instance's own dictionary is checked.
3. **Non-data descriptor / class attribute runs** — if nothing is found on the instance, non-data descriptors and plain class attributes are consulted.

See [Attribute Access and Lookup](attribute_access_lookup.md) for the full pipeline and [Data vs Non-Data](descriptor_types.md) for why the distinction matters.

### 5. Three Layers of the System

This section covers three layers, each building on the previous:

```text
Layer 1: Attribute system
    __getattribute__, __getattr__, __setattr__, __delattr__

Layer 2: Descriptor protocol
    __get__, __set__, __delete__

Layer 3: Applications
    properties, methods, ORM, caching
```

Layer 1 defines *when* the hooks run. Layer 2 defines *what* the hooks do. Layer 3 is what you build with them.

If you understand descriptors, you understand Python's attribute access system.

## How Python Uses Descriptors

Descriptors plug into Python's attribute lookup pipeline. When you access `obj.attr`, data descriptors are checked before the instance `__dict__`, while non-data descriptors are checked after. See [Attribute Access and Lookup](attribute_access_lookup.md) for the complete resolution order.

### Descriptor Lives on Class, Manages Instance Access

```python
class Descriptor:
    def __get__(self, instance, owner):
        if instance is None:
            return self  # Accessed from class
        return f"Value for {instance}"  # Accessed from instance

class MyClass:
    attr = Descriptor()  # Lives in class namespace

# Accessing from class — instance is None
print(MyClass.attr)    # <Descriptor object>

# Accessing from instance — instance is the object
obj = MyClass()
print(obj.attr)        # "Value for <MyClass object>"
```

## Simple Example

### 1. Basic Descriptor

```python
class SimpleDescriptor:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        print(f"Getting {self.name}")
        return instance.__dict__.get(self.name, None)
    
    def __set__(self, instance, value):
        print(f"Setting {self.name} = {value}")
        instance.__dict__[self.name] = value

class MyClass:
    x = SimpleDescriptor('x')
    y = SimpleDescriptor('y')

obj = MyClass()
obj.x = 10  # Setting x = 10
print(obj.x)  # Getting x → 10

obj.y = 20  # Setting y = 20
print(obj.y)  # Getting y → 20
```

### 2. Why Use This?

Instead of:
```python
class MyClass:
    def get_x(self):
        return self._x
    
    def set_x(self, value):
        self._x = value
```

You can:
```python
class MyClass:
    x = ManagedAttribute('x')
```

### 3. Benefits

- ✅ Cleaner syntax
- ✅ Reusable attribute logic
- ✅ Attribute-style access with method-level control
- ✅ DRY (Don't Repeat Yourself)

## Where Descriptors Shine

### 1. Validation

```python
class TypedDescriptor:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}"
            )
        instance.__dict__[self.name] = value
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

class Person:
    name = TypedDescriptor('name', str)
    age = TypedDescriptor('age', int)

p = Person()
p.name = "Alice"  # ✅ OK
p.age = 30        # ✅ OK
# p.age = "30"    # ❌ TypeError
```

### 2. Lazy Loading

```python
class LazyProperty:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.func(instance)
        # Cache by replacing descriptor with value
        setattr(instance, self.func.__name__, value)
        return value

class DataLoader:
    @LazyProperty
    def data(self):
        print("Loading data...")
        return [1, 2, 3, 4, 5]

obj = DataLoader()
print(obj.data)  # Loading data... [1, 2, 3, 4, 5]
print(obj.data)  # [1, 2, 3, 4, 5] (no loading)
```

### 3. Computed Properties

```python
class Quantity:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, 0)
    
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        instance.__dict__[self.name] = value

class Product:
    price = Quantity('price')
    quantity = Quantity('quantity')
    
    @property
    def total(self):
        return self.price * self.quantity

prod = Product()
prod.price = 10
prod.quantity = 5
print(prod.total)  # 50
```

## Descriptor vs Property

### 1. Property Is a Descriptor

```python
# Using property
class Example:
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

# Property is actually a descriptor!
print(type(Example.__dict__['x']))  # <class 'property'>
```

### 2. When to Use Each

**Use `@property` when:**
- One-off attribute with custom logic
- Simple getter/setter/deleter
- Specific to one class

**Use descriptor when:**
- Reusable across multiple classes
- Complex attribute management
- Need to share logic

### 3. Comparison

```python
# Property - specific to one attribute
class Circle:
    @property
    def area(self):
        return 3.14 * self.radius ** 2

# Descriptor - reusable pattern
class PositiveNumber:
    def __init__(self, name):
        self.name = name
    
    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("Must be positive")
        instance.__dict__[self.name] = value
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, 1)

class Rectangle:
    width = PositiveNumber('width')
    height = PositiveNumber('height')

class Circle:
    radius = PositiveNumber('radius')
```

## Why Descriptors Matter

Descriptors enable **reusable attribute logic** — write validation, type checking, or access control once and apply it across many classes:

```python
# Define once
class NonNegative:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        if value < 0:
            raise ValueError("Must be non-negative")
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, 0)

# Use everywhere
class BankAccount:
    balance = NonNegative()

class ShoppingCart:
    total = NonNegative()

class Inventory:
    quantity = NonNegative()
```

Frameworks like Django and SQLAlchemy use descriptors extensively — every ORM field is a descriptor that handles database storage and retrieval. See [Descriptor Use Cases](descriptor_applications.md) for validation, ORM, caching, and access control patterns.

---

## Exercises

**Exercise 1.**
Create a simple descriptor `Uppercase` that, when a string value is set, automatically converts it to uppercase. Use `__set_name__`, `__get__`, and `__set__`. Apply it to a `User` class with a `username` field. Show that `user.username = "alice"` stores `"ALICE"`.

??? success "Solution to Exercise 1"

        class Uppercase:
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return obj.__dict__.get(self.name)

            def __set__(self, obj, value):
                obj.__dict__[self.name] = value.upper()

        class User:
            username = Uppercase()

            def __init__(self, username):
                self.username = username

        u = User("alice")
        print(u.username)  # ALICE

        u.username = "bob"
        print(u.username)  # BOB

---

**Exercise 2.**
Write a `ReadOnly` descriptor that allows a value to be set once (in `__init__`) but raises `AttributeError` on any subsequent assignment. Use it in a `Product` class for the `sku` field. Show that the SKU can be set during construction but not changed afterward.

??? success "Solution to Exercise 2"

        class ReadOnly:
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return obj.__dict__.get(self.name)

            def __set__(self, obj, value):
                if self.name in obj.__dict__:
                    raise AttributeError(f"'{self.name}' is read-only")
                obj.__dict__[self.name] = value

        class Product:
            sku = ReadOnly()

            def __init__(self, sku, name):
                self.sku = sku
                self.name = name

        p = Product("ABC-123", "Widget")
        print(p.sku)  # ABC-123

        try:
            p.sku = "NEW-456"
        except AttributeError as e:
            print(f"Error: {e}")  # Error: 'sku' is read-only

---

**Exercise 3.**
Build a `Logged` descriptor that prints a message every time a value is set or accessed. Include the attribute name, old value, and new value in set messages. Apply it to a `Settings` class with `theme` and `language` fields. Demonstrate the logging output.

??? success "Solution to Exercise 3"

        class Logged:
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                value = obj.__dict__.get(self.name)
                print(f"GET {self.name} -> {value!r}")
                return value

            def __set__(self, obj, value):
                old = obj.__dict__.get(self.name, "<unset>")
                print(f"SET {self.name}: {old!r} -> {value!r}")
                obj.__dict__[self.name] = value

        class Settings:
            theme = Logged()
            language = Logged()

            def __init__(self, theme, language):
                self.theme = theme
                self.language = language

        s = Settings("dark", "en")
        # SET theme: '<unset>' -> 'dark'
        # SET language: '<unset>' -> 'en'
        s.theme
        # GET theme -> 'dark'
        s.theme = "light"
        # SET theme: 'dark' -> 'light'
