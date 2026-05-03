# getattr setattr delattr

!!! tip "Mental Model"
    `getattr`, `setattr`, and `delattr` are Python's way of turning attribute names into variables. Instead of hardcoding `obj.name`, you pass the attribute name as a string: `getattr(obj, "name")`. This lets you write generic code -- serializers, ORMs, and frameworks -- that works with any attribute on any object without knowing the class at coding time.

## Built-In Functions

### 1. Overview

Python provides three powerful built-in functions to dynamically interact with object attributes:

- `getattr(obj, name[, default])` - retrieve attribute value
- `setattr(obj, name, value)` - set attribute value  
- `delattr(obj, name)` - delete attribute

### 2. Why Dynamic Access?

**Dynamic** means determined at **runtime**, not hardcoded:

```python
# Static (fixed) access
person.name = "Alice"

# Dynamic access
attr = "name"
setattr(person, attr, "Alice")
```

### 3. Key Use Cases

- Generic code that works with any attribute
- Frameworks that don't know class structure ahead of time
- Serialization/deserialization systems
- Configuration-driven applications
- Reflection and metaprogramming

## getattr Function

### 1. Basic Syntax

```python
value = getattr(obj, 'attr_name')
value = getattr(obj, 'attr_name', default_value)
```

### 2. Simple Example

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)

# Static access
print(p.name)  # "Alice"

# Dynamic access
print(getattr(p, 'name'))  # "Alice"
print(getattr(p, 'age'))   # 30
```

### 3. With Default Value

```python
# Attribute exists
print(getattr(p, 'name', 'Unknown'))  # "Alice"

# Attribute missing - returns default
print(getattr(p, 'email', 'no-email'))  # "no-email"

# Without default - raises AttributeError
# print(getattr(p, 'email'))  # ❌ AttributeError
```

!!! note "getattr Follows the Full Lookup Chain"

    `getattr(obj, name)` is not a simple dictionary lookup on `obj.__dict__`. It follows
    the full attribute lookup chain: it calls `type(obj).__getattribute__(obj, name)`,
    which checks data descriptors, instance `__dict__`, non-data descriptors, and finally
    `__getattr__` if defined. This means accessing a property via `getattr` executes the
    property's getter, and accessing a class-level descriptor invokes its `__get__` method.
    Be aware of this when using `getattr` on objects with complex attribute access logic.

## setattr Function

### 1. Basic Syntax

```python
setattr(obj, 'attr_name', value)
```

Equivalent to:
```python
obj.attr_name = value
```

### 2. Simple Example

```python
class Person:
    pass

p = Person()

# Static assignment
p.name = "Alice"

# Dynamic assignment
setattr(p, 'age', 30)
setattr(p, 'city', 'New York')

print(p.name)  # "Alice"
print(p.age)   # 30
print(p.city)  # "New York"
```

### 3. Dynamic Attribute Names

```python
person = Person()

# Set multiple attributes from dictionary
data = {'name': 'Bob', 'age': 25, 'city': 'Boston'}
for key, value in data.items():
    setattr(person, key, value)

print(person.name)  # "Bob"
print(person.age)   # 25
```

## delattr Function

### 1. Basic Syntax

```python
delattr(obj, 'attr_name')
```

Equivalent to:
```python
del obj.attr_name
```

### 2. Simple Example

```python
class Person:
    def __init__(self):
        self.name = "Alice"
        self.age = 30

p = Person()
print(p.name)  # "Alice"

# Delete attribute
delattr(p, 'name')

# Now accessing raises error
# print(p.name)  # ❌ AttributeError
```

### 3. Conditional Deletion

```python
def remove_attribute(obj, attr):
    if hasattr(obj, attr):
        delattr(obj, attr)
        print(f"Deleted {attr}")
    else:
        print(f"{attr} doesn't exist")

remove_attribute(p, 'age')    # Deleted age
remove_attribute(p, 'email')  # email doesn't exist
```

## Practical Examples

### 1. Configuration Loading

```python
class Config:
    pass

def load_config(filename):
    config = Config()
    with open(filename) as f:
        for line in f:
            key, value = line.strip().split('=')
            setattr(config, key, value)
    return config

# config.txt:
# host=localhost
# port=8080
# debug=true

config = load_config('config.txt')
print(config.host)   # "localhost"
print(config.port)   # "8080"
```

### 2. Dynamic Method Calls

```python
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
    
    def multiply(self, a, b):
        return a * b

calc = Calculator()
operation = 'add'  # from user input

# Get method dynamically
method = getattr(calc, operation)
result = method(5, 3)  # 8
```

### 3. Object Serialization

```python
def to_dict(obj):
    """Convert object attributes to dictionary"""
    return {k: v for k, v in vars(obj).items() if not k.startswith('_')}

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(to_dict(p))  # {'age': 30, 'name': 'Alice'}
```

## hasattr Helper

### 1. Check Existence

`hasattr(obj, name)` checks if attribute exists:

```python
class Person:
    def __init__(self, name):
        self.name = name

p = Person("Alice")

print(hasattr(p, 'name'))   # True
print(hasattr(p, 'age'))    # False
```

### 2. Safe Access Pattern

```python
# Instead of try/except
value = getattr(obj, 'attr', None)

# Or check first
if hasattr(obj, 'attr'):
    value = getattr(obj, 'attr')
```

!!! warning "hasattr Internally Calls getattr"

    `hasattr(obj, name)` works by calling `getattr(obj, name)` and returning `False` if an
    `AttributeError` is raised. This means it triggers the full attribute lookup chain,
    including `__getattr__`, `__getattribute__`, and property getters. If any of these have
    side effects (logging, database queries, lazy initialization), `hasattr` will execute
    them. Avoid using `hasattr` on objects where attribute access is expensive or has
    side effects.

### 3. Combined Example

```python
def safe_get(obj, attr, default=None):
    """Safely get attribute with default"""
    if hasattr(obj, attr):
        return getattr(obj, attr)
    return default

age = safe_get(person, 'age', 0)
```

## The Unified Attribute System

The three functions form a symmetric system that maps directly to Python's dunder methods:

| Operation | Built-in | Dunder Method | Syntax Equivalent |
|---|---|---|---|
| Read | `getattr(obj, name)` | `__getattribute__` → `__getattr__` (fallback) | `obj.name` |
| Write | `setattr(obj, name, val)` | `__setattr__` | `obj.name = val` |
| Delete | `delattr(obj, name)` | `__delattr__` | `del obj.name` |

Both static access (`obj.attr`) and dynamic access (`getattr(obj, "attr")`) trigger the **same** underlying mechanism. The only difference is whether the attribute name is known at coding time or determined at runtime.

!!! note "Bound Methods via getattr"

    When `getattr(obj, "method")` retrieves a method, it returns a **bound method**, not the raw function. This happens because functions are descriptors: `getattr` triggers `function.__get__(obj, type(obj))`, which binds the instance as the first argument. This is the same descriptor mechanism described in the [Attribute Lookup](../object_model/attribute_lookup.md) chapter.

## Comparison

### 1. Static vs Dynamic

| Aspect | Static Access | Dynamic Access |
|--------|---------------|----------------|
| Syntax | `obj.attr` | `getattr(obj, 'attr')` |
| Speed | Faster | Slightly slower |
| Flexibility | Fixed at write time | Determined at runtime |
| Use case | Known attributes | Generic/framework code |

### 2. When to Use Each

**Use static access (`obj.attr`) when:**
- You know the attribute name at coding time
- Performance is critical
- Code clarity is priority

**Use dynamic access (`getattr/setattr`) when:**
- Attribute name comes from user input, config, or database
- Writing generic utilities or frameworks
- Need to iterate over arbitrary attributes
- Implementing serialization/deserialization

!!! warning "Prefer Static Access by Default"

    Dynamic attribute access should be used sparingly in production code. Overuse leads to
    code that is hard to debug, resistant to refactoring, and invisible to static analysis
    tools like mypy. When attribute names are known at coding time, always prefer static
    access (`obj.attr`). Reserve `getattr`/`setattr`/`delattr` for genuinely dynamic
    scenarios such as frameworks, serialization, and configuration-driven code.

!!! tip "Connection to Dunder Methods"

    `getattr(obj, name)` calls `type(obj).__getattribute__(obj, name)` internally. If
    `__getattribute__` raises `AttributeError` and the class defines `__getattr__`, Python
    falls back to `obj.__getattr__(name)`. Similarly, `setattr` invokes `__setattr__` and
    `delattr` invokes `__delattr__`. Understanding this link between built-in functions and
    dunder methods is key for Chapter 7's descriptor and attribute access topics.

---

## Exercises

**Exercise 1.**
Write a function `copy_attributes(source, target, names)` that uses `getattr` and `setattr` to copy the named attributes from `source` to `target`. If an attribute does not exist on `source`, skip it using `hasattr`. Demonstrate with two simple objects.

??? success "Solution to Exercise 1"

        class Source:
            def __init__(self):
                self.name = "Alice"
                self.age = 30
                self.email = "alice@example.com"

        class Target:
            pass

        def copy_attributes(source, target, names):
            for name in names:
                if hasattr(source, name):
                    setattr(target, name, getattr(source, name))

        src = Source()
        tgt = Target()
        copy_attributes(src, tgt, ["name", "age", "phone"])  # phone skipped
        print(vars(tgt))  # {'name': 'Alice', 'age': 30}

---

**Exercise 2.**
Create a `DynamicConfig` class with a `from_dict(data)` class method that uses `setattr` to set attributes from dictionary keys. Also add a `to_dict()` method that uses `vars()` to return the instance attributes as a dictionary. Demonstrate round-tripping: create from dict, modify, convert back.

??? success "Solution to Exercise 2"

        class DynamicConfig:
            @classmethod
            def from_dict(cls, data):
                obj = cls()
                for key, value in data.items():
                    setattr(obj, key, value)
                return obj

            def to_dict(self):
                return vars(self).copy()

        config = DynamicConfig.from_dict({"host": "localhost", "port": 8080, "debug": True})
        print(config.host)       # localhost
        config.port = 9090       # Modify
        print(config.to_dict())  # {'host': 'localhost', 'port': 9090, 'debug': True}

---

**Exercise 3.**
Build a function `reset_attributes(obj, defaults)` where `defaults` is a dictionary of attribute names to default values. For each key, use `delattr` to remove the attribute if it exists, then use `setattr` to set it to the default value. Show before and after states using `vars()`.

??? success "Solution to Exercise 3"

        def reset_attributes(obj, defaults):
            for name, default in defaults.items():
                if hasattr(obj, name):
                    delattr(obj, name)
                setattr(obj, name, default)

        class Settings:
            def __init__(self):
                self.theme = "dark"
                self.font_size = 14
                self.language = "en"

        s = Settings()
        s.theme = "custom"
        s.font_size = 20
        print("Before:", vars(s))

        reset_attributes(s, {"theme": "light", "font_size": 12, "language": "en"})
        print("After:", vars(s))
