# Attribute Access and Lookup

Understanding Python's attribute access system—including the lookup hierarchy, descriptor protocol, and access hooks—is essential for advanced OOP.

!!! tip "Mental Model"
    Think of attribute access as a **pipeline**: every time you write `obj.attr`, Python walks a chain of checks—data descriptors, instance dictionaries, non-data descriptors, class hierarchies, and fallback hooks—before returning a value. Without a descriptor, Python returns the stored value directly. With a descriptor, Python calls its `__get__` — the descriptor decides what to return.

---

## Attribute Resolution Order

When you access `obj.attr`, Python searches in this order:

1. **Data descriptors** — search each class's `__dict__` in MRO order for a data descriptor
2. **Instance attributes** — check `obj.__dict__`
3. **Non-data descriptors and class attributes** — search MRO again for non-data descriptors or plain attributes
4. **`__getattr__`** — called only if nothing was found above

!!! warning "Phases, Not Per-Class Loops"
    A common misconception is that Python runs steps 1–3 per class before moving to the next class in MRO. It does **not**. Each step is a **phase across the entire MRO**:

    - Phase 1 scans **all** classes in MRO for data descriptors
    - Phase 2 checks the instance `__dict__`
    - Phase 3 scans **all** classes in MRO again for non-data descriptors / plain attributes

    This is why a data descriptor in a parent class overrides an instance attribute — Python finds it in phase 1, before ever reaching phase 2.

    **Performance:** this sounds expensive, but CPython optimizes heavily — cached attribute lookups, type version tags, fast paths in `LOAD_ATTR` bytecode. Most MROs are short (2–3 classes), so even the logical search is small. The lookup rules are designed for correctness first; CPython then optimizes the common cases.

### Visual Flow

```
obj.attr
    ↓
__getattribute__ called
    ↓
[1] Search MRO for data descriptor → call __get__
    ↓
[2] Check instance __dict__
    ↓
[3] Search MRO for non-data descriptor / plain attribute
    ↓
[4] __getattr__ (if defined)
    ↓
AttributeError
```

### Key Principle

**Data descriptors override instance attributes**, while **non-data descriptors defer to instance attributes**.

---

## Data vs Non-Data Descriptors

The key distinction affecting lookup priority:

| Type | Methods | Priority |
|------|---------|----------|
| **Data descriptor** | `__get__` + `__set__` or `__delete__` | Before instance `__dict__` |
| **Non-data descriptor** | Only `__get__` | After instance `__dict__` |

See [Data vs Non-Data Descriptors](descriptor_types.md) for detailed examples, priority demonstrations, and patterns.

---

## The Four Access Hooks

Python provides four attribute access hooks:

| Method | Called When | Fallback |
|--------|-------------|----------|
| `__getattribute__` | **Every** attribute read | None |
| `__getattr__` | **Missing** attribute only | None |
| `__setattr__` | **Every** attribute write | None |
| `__delattr__` | **Every** attribute deletion | None |

### Relationship Diagram

```
Attribute Read: obj.x
    ↓
__getattribute__('x')
    ↓
Found? → Return value
    ↓
Not found? → AttributeError
    ↓
__getattr__('x') if defined
    ↓
Return value or raise AttributeError

Attribute Write: obj.x = value
    ↓
__setattr__('x', value)
    ↓
Store in __dict__ or descriptor

Attribute Delete: del obj.x
    ↓
__delattr__('x')
    ↓
Remove from __dict__ or descriptor
```

---

## Combined Implementation

### All Methods Together

```python
class FullControl:
    def __init__(self, value):
        # Careful: __setattr__ is active here!
        super().__setattr__('_data', {})
        self.value = value  # Uses __setattr__
    
    def __getattribute__(self, name):
        print(f"[GET] {name}")
        return super().__getattribute__(name)
    
    def __getattr__(self, name):
        print(f"[MISSING] {name}")
        return f"Default for {name}"
    
    def __setattr__(self, name, value):
        print(f"[SET] {name} = {value}")
        super().__setattr__(name, value)
    
    def __delattr__(self, name):
        print(f"[DEL] {name}")
        super().__delattr__(name)

obj = FullControl(42)
# [SET] value = 42

print(obj.value)
# [GET] value
# 42

print(obj.missing)
# [GET] missing
# [MISSING] missing
# Default for missing
```

### With Properties

```python
class WithProperties:
    def __init__(self):
        self._value = 0
    
    @property
    def value(self):
        print("[PROPERTY GET]")
        return self._value
    
    @value.setter
    def value(self, val):
        print("[PROPERTY SET]")
        self._value = val
    
    def __getattribute__(self, name):
        print(f"[__getattribute__] {name}")
        return super().__getattribute__(name)
    
    def __setattr__(self, name, value):
        print(f"[__setattr__] {name}")
        super().__setattr__(name, value)

obj = WithProperties()
# [__setattr__] _value

obj.value = 42
# [__setattr__] value
# [PROPERTY SET]
# [__setattr__] _value

print(obj.value)
# [__getattribute__] value
# [PROPERTY GET]
# [__getattribute__] _value
# 42
```

---

## MRO and Inheritance

### Method Resolution Order

For inherited classes, Python follows the **MRO**:

```python
class A:
    x = "A"

class B(A):
    pass

class C(A):
    x = "C"

class D(B, C):
    pass

print(D.mro())
# [D, B, C, A, object]

print(D.x)  # "C" (found in C before A)
```

### Searching Through MRO

```python
class Base:
    def method(self):
        return "Base"

class Child(Base):
    pass

obj = Child()
# Searches: Child → Base → object
print(obj.method())  # "Base"
```

---

## Descriptor Protocol

Descriptors integrate directly into this lookup pipeline. Without a descriptor, Python returns the stored value directly. With a descriptor, Python calls its `__get__` method — the descriptor decides what to return:

```python
# Python internally does:
type(obj).__dict__['attr'].__get__(obj, type(obj))
```

See [Descriptor Introduction](descriptor_intro.md) for what descriptors are and when to use them, and [Descriptor Methods](descriptor_methods.md) for the full `__get__`, `__set__`, `__delete__` protocol.

---

## Practical Patterns

### Read-Only After Init

```python
class ReadOnlyAfterInit:
    def __init__(self):
        super().__setattr__('_locked', False)
        self.value = 42
        super().__setattr__('_locked', True)
    
    def __setattr__(self, name, value):
        if super().__getattribute__('_locked'):
            raise AttributeError("Object is read-only")
        super().__setattr__(name, value)
    
    def __delattr__(self, name):
        if super().__getattribute__('_locked'):
            raise AttributeError("Object is read-only")
        super().__delattr__(name)
```

### Lazy Loading with Caching

```python
class LazyCache:
    def __init__(self):
        super().__setattr__('_cache', {})
        super().__setattr__('_loaders', {})
    
    def register_loader(self, attr, loader_func):
        self._loaders[attr] = loader_func
    
    def __getattr__(self, name):
        # Called only for missing attributes
        loaders = super().__getattribute__('_loaders')
        cache = super().__getattribute__('_cache')
        
        if name in loaders:
            print(f"[LOADING] {name}")
            value = loaders[name]()
            cache[name] = value
            setattr(self, name, value)  # Cache in __dict__
            return value
        raise AttributeError(f"No attribute: {name}")

obj = LazyCache()
obj.register_loader('data', lambda: [1, 2, 3, 4, 5])

print(obj.data)  # [LOADING] data → [1, 2, 3, 4, 5]
print(obj.data)  # [1, 2, 3, 4, 5] (from __dict__, no loading)
```

### Validation System

```python
class ValidatedObject:
    _validators = {}
    
    def __setattr__(self, name, value):
        if name in self._validators:
            if not self._validators[name](value):
                raise ValueError(f"Validation failed for {name}")
        super().__setattr__(name, value)
    
    @classmethod
    def add_validator(cls, attr, validator):
        cls._validators[attr] = validator

ValidatedObject.add_validator('age', lambda x: 0 <= x <= 150)

obj = ValidatedObject()
obj.age = 30   # ✓ OK
# obj.age = 200  # ✗ ValueError
```

---

## Debugging Attribute Access

!!! tip "Debugging Rule"
    If `obj.attr` behaves unexpectedly, check in this order:

    1. Is it a **property or descriptor**? → Check `type(type(obj).__dict__.get('attr'))`
    2. Is it in **`obj.__dict__`**? → Check `obj.__dict__`
    3. Is it in the **class**? → Check `type(obj).__dict__`
    4. Is **`__getattr__`** involved? → Check if the class defines `__getattr__`

---

## Common Pitfalls

### Forgetting super()

```python
# ✗ BAD - doesn't actually store value
def __setattr__(self, name, value):
    print(f"Setting {name}")
    # Forgot super().__setattr__!

# ✓ GOOD
def __setattr__(self, name, value):
    print(f"Setting {name}")
    super().__setattr__(name, value)
```

### Infinite Recursion

```python
# ✗ BAD - infinite recursion
def __getattribute__(self, name):
    if self.ready:  # Calls __getattribute__ again!
        return self.value

# ✓ GOOD
def __getattribute__(self, name):
    ready = super().__getattribute__('ready')
    if ready:
        return super().__getattribute__('value')
    return super().__getattribute__(name)
```

### Shadowing Class Attributes

```python
class Counter:
    count = 0
    
    def increment(self):
        self.count += 1  # ✗ Creates instance attribute!

c1 = Counter()
c1.increment()
print(c1.count)        # 1 (instance)
print(Counter.count)   # 0 (class unchanged)

# ✓ Fix: modify class attribute directly
def increment(self):
    Counter.count += 1
```

### Understanding `__dict__`

```python
class Example:
    class_var = "class"

obj = Example()
obj.instance_var = "instance"

print(obj.__dict__)        # {'instance_var': 'instance'}
print(Example.__dict__)    # {..., 'class_var': 'class', ...}
```

---

## When to Use Each Method

| Method | Use When |
|--------|----------|
| `__getattribute__` | Need to intercept **all** reads (logging, proxies) |
| `__getattr__` | Need **default values** for missing attributes |
| `__setattr__` | Need to **validate** or **transform** all writes |
| `__delattr__` | Need to **protect** or **cleanup** on deletion |

### Best Practices

- **Use the minimum necessary** — Don't override all four if you don't need to
- **Call super()** — Always delegate to parent implementation
- **Avoid recursion** — Never access `self.x` inside `__getattribute__`
- **Consider properties first** — They're simpler for specific attributes
- **Document behavior** — Make it clear which attributes are special

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Resolution order | Data descriptors (MRO) → instance `__dict__` → non-data / class attrs (MRO) → `__getattr__` |
| Data descriptor | Has `__set__` or `__delete__`, overrides instance |
| Non-data descriptor | Only `__get__`, defers to instance |
| `__getattribute__` | Called for every attribute access |
| `__getattr__` | Fallback for missing attributes only |
| MRO | C3 linearization determines search order |

**Key Takeaways**:

- Attribute lookup follows a strict hierarchy
- Data descriptors have highest priority (e.g., properties with setters)
- Always use `super().__getattribute__()` inside `__getattribute__` to avoid recursion
- `__getattr__` is only called when attribute is not found normally
- Properties are simpler than `__getattribute__` for specific attributes

---

## Exercises

**Exercise 1.**
Create a class `LoggedAccess` that implements `__getattribute__` to print a message every time any attribute is accessed. Use `super().__getattribute__()` to avoid infinite recursion. Demonstrate it with a simple class that has `name` and `value` attributes.

??? success "Solution to Exercise 1"

        class LoggedAccess:
            def __getattribute__(self, name):
                print(f"Accessing attribute: {name}")
                return super().__getattribute__(name)

        class Item(LoggedAccess):
            def __init__(self, name, value):
                self.name = name
                self.value = value

        item = Item("widget", 42)
        print(item.name)   # prints "Accessing attribute: name" then "widget"
        print(item.value)  # prints "Accessing attribute: value" then "42"

---

**Exercise 2.**
Write a class `DefaultDict` that uses `__getattr__` to return a default value (`"N/A"`) for any attribute that does not exist, instead of raising `AttributeError`. Set a few attributes in `__init__` and show that existing attributes return their values while missing attributes return the default.

??? success "Solution to Exercise 2"

        class DefaultDict:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    self.__dict__[k] = v

            def __getattr__(self, name):
                return "N/A"  # Default for missing attributes

        d = DefaultDict(name="Alice", age=30)
        print(d.name)      # Alice
        print(d.age)       # 30
        print(d.email)     # N/A — does not exist
        print(d.phone)     # N/A — does not exist

---

**Exercise 3.**
Build a class `Frozen` that allows attributes to be set in `__init__` but prevents any attribute modification after initialization. Use a flag `_initialized` and override `__setattr__` to raise `AttributeError` if `_initialized` is `True`. Demonstrate that attributes can be set during construction but not after.

??? success "Solution to Exercise 3"

        class Frozen:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    object.__setattr__(self, k, v)
                object.__setattr__(self, '_initialized', True)

            def __setattr__(self, name, value):
                if getattr(self, '_initialized', False):
                    raise AttributeError(f"Cannot modify attribute '{name}' on frozen object")
                super().__setattr__(name, value)

        f = Frozen(x=10, y=20)
        print(f.x)  # 10
        print(f.y)  # 20

        try:
            f.x = 99
        except AttributeError as e:
            print(f"Error: {e}")
            # Error: Cannot modify attribute 'x' on frozen object
