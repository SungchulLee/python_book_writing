# __getattribute__

## Fundamentals

### 1. Definition

The `__getattribute__` method is automatically called by Python **for every attribute access** on an object:

```python
obj.attr  # Triggers obj.__getattribute__('attr')
getattr(obj, 'attr')  # Also triggers obj.__getattribute__('attr')
```

### 2. Method Signature

```python
def __getattribute__(self, name):
    # name is a string
    # Must return a value or raise AttributeError
    pass
```

### 3. Universal Hook

**Key characteristic**: `__getattribute__` is called for **every** attribute access, even:

- Instance attributes
- Class attributes
- Methods
- Properties
- Dunder methods (like `__dict__`)

!!! tip "Core Idea"
    `__getattribute__` intercepts **every** attribute read — existing, missing, methods, properties, even `__dict__` itself. It is the single entry point for all attribute access in Python. If you only need to handle *missing* attributes, use [`__getattr__`](dunder_getattr.md) instead.

## Attribute Lifecycle — Unified Mental Model

All four attribute dunder methods fit into a single lifecycle:

```text
READ:   obj.attr  →  __getattribute__  →  (AttributeError?)  →  __getattr__
WRITE:  obj.attr = val  →  __setattr__
DELETE: del obj.attr    →  __delattr__
```

`__getattribute__` is the only hook that runs on **every** read — it is the entry
point. `__getattr__` is the fallback that fires only when `__getattribute__` raises
`AttributeError`. `__setattr__` and `__delattr__` each handle their respective
operations unconditionally.

| Goal | Use |
|------|-----|
| Handle missing attributes | `__getattr__` |
| Intercept every read | `__getattribute__` |
| Validate / transform writes | `__setattr__` |
| Control deletion | `__delattr__` |
| Control a single named attribute | `@property` |

## Basic Implementation

### 1. Simple Override

```python
class MyClass:
    def __init__(self):
        self.value = 42
    
    def __getattribute__(self, name):
        print(f"Accessing attribute: {name}")
        return super().__getattribute__(name)

obj = MyClass()
x = obj.value
# Output: Accessing attribute: value
# Returns: 42
```

### 2. Without super()

```python
class MyClass:
    def __getattribute__(self, name):
        print(f"Getting: {name}")
        return object.__getattribute__(self, name)
```

### 3. Must Return or Raise

```python
def __getattribute__(self, name):
    if name == 'secret':
        raise AttributeError("Access denied")
    return super().__getattribute__(name)
```

!!! note "What super().__getattribute__ Does Internally"
    When you call `super().__getattribute__(name)`, Python's default implementation follows a precise lookup order:

    1. **Data descriptors** on the class (via MRO) — e.g., `@property`, `__slots__`
    2. **Instance `__dict__`** — the object's own namespace
    3. **Non-data descriptors and class attributes** (via MRO) — e.g., methods, class variables
    4. If none found → raise `AttributeError` → triggers `__getattr__` (if defined)

    This is the same [attribute lookup chain](../descriptors/attribute_access_lookup.md) described earlier. `__getattribute__` is the entry point; the descriptor protocol governs what happens inside it.

## Avoiding Recursion

### 1. The Problem

```python
class Broken:
    def __getattribute__(self, name):
        # ❌ INFINITE RECURSION!
        return self.name  # Calls __getattribute__ again!
```

### 2. Correct Approaches

**Use `super()`:**
```python
class Correct:
    def __getattribute__(self, name):
        return super().__getattribute__(name)
```

**Use `object.__getattribute__`:**
```python
class Correct:
    def __getattribute__(self, name):
        return object.__getattribute__(self, name)
```

**Direct dict access:**
```python
class Correct:
    def __getattribute__(self, name):
        return object.__getattribute__(self, '__dict__')[name]
```

### 3. Why Recursion Happens

```python
def __getattribute__(self, name):
    value = self.something  # Calls __getattribute__('something')
    # Which calls __getattribute__('something')
    # Which calls __getattribute__('something')
    # ... forever!
```

## Practical Examples

### 1. Logging Access

```python
class LoggedAccess:
    def __init__(self):
        self.data = {'x': 1, 'y': 2}
    
    def __getattribute__(self, name):
        print(f"[LOG] Accessing: {name}")
        return super().__getattribute__(name)

obj = LoggedAccess()
print(obj.data)
# [LOG] Accessing: data
# {'x': 1, 'y': 2}
```

### 2. Access Control

```python
class Restricted:
    def __init__(self):
        self._private = "secret"
        self.public = "visible"
    
    def __getattribute__(self, name):
        if name.startswith('_') and not name.startswith('__'):
            raise AttributeError(f"Cannot access private attribute: {name}")
        return super().__getattribute__(name)

obj = Restricted()
print(obj.public)   # ✅ "visible"
# print(obj._private)  # ❌ AttributeError
```

### 3. Lazy Loading

```python
class LazyLoader:
    def __init__(self):
        self._loaded = False
        self._data = None
    
    def __getattribute__(self, name):
        if name == 'data':
            loaded = super().__getattribute__('_loaded')
            if not loaded:
                print("Loading data...")
                object.__setattr__(self, '_data', [1, 2, 3, 4, 5])
                object.__setattr__(self, '_loaded', True)
            return super().__getattribute__('_data')
        return super().__getattribute__(name)

obj = LazyLoader()
print(obj.data)  # Loading data... [1, 2, 3, 4, 5]
print(obj.data)  # [1, 2, 3, 4, 5] (no loading)
```

## Interaction with Properties

### 1. Properties Still Work

```python
class Example:
    def __init__(self):
        self._value = 42
    
    @property
    def value(self):
        return self._value * 2
    
    def __getattribute__(self, name):
        print(f"Intercepting: {name}")
        return super().__getattribute__(name)

obj = Example()
print(obj.value)
# Intercepting: value
# 84 (property getter was called)
```

### 2. Order of Operations

```python
obj.value
    ↓
__getattribute__('value') called
    ↓
super().__getattribute__('value')
    ↓
Finds property descriptor in class
    ↓
Calls property's __get__ method
    ↓
Returns result
```

### 3. Blocking Properties

```python
class BlockProperty:
    @property
    def value(self):
        return 42
    
    def __getattribute__(self, name):
        if name == 'value':
            return 100  # Bypass property!
        return super().__getattribute__(name)

obj = BlockProperty()
print(obj.value)  # 100 (property never called)
```

## Advanced Patterns

### 1. Attribute Proxy

```python
class Proxy:
    def __init__(self, obj):
        object.__setattr__(self, '_obj', obj)
    
    def __getattribute__(self, name):
        if name == '_obj':
            return object.__getattribute__(self, name)
        obj = object.__getattribute__(self, '_obj')
        return getattr(obj, name)

class Target:
    def __init__(self):
        self.value = 42

proxy = Proxy(Target())
print(proxy.value)  # 42
```

### 2. Attribute Mapping

```python
class AttributeMapper:
    def __init__(self):
        self._mapping = {
            'old_name': 'new_name',
            'deprecated': 'current'
        }
        self.new_name = "value"
        self.current = "data"
    
    def __getattribute__(self, name):
        mapping = super().__getattribute__('_mapping')
        if name in mapping:
            name = mapping[name]
        return super().__getattribute__(name)

obj = AttributeMapper()
print(obj.old_name)    # "value"
print(obj.deprecated)  # "data"
```

### 3. Counting Access

```python
class AccessCounter:
    def __init__(self):
        object.__setattr__(self, '_counts', {})
        self.data = [1, 2, 3]
    
    def __getattribute__(self, name):
        if name not in ('_counts', '__dict__', '__class__'):
            counts = object.__getattribute__(self, '_counts')
            counts[name] = counts.get(name, 0) + 1
        return super().__getattribute__(name)
    
    def get_counts(self):
        return self._counts

obj = AccessCounter()
obj.data
obj.data
obj.data
print(obj.get_counts())  # {'data': 3}
```

## When to Use

### 1. Good Use Cases

✅ **Debugging and logging** - Track all attribute access
✅ **Proxies and wrappers** - Delegate to another object
✅ **Access control** - Enforce security policies
✅ **Attribute translation** - Map old names to new names

### 2. Avoid When

❌ **Simple attribute access** — Use normal attributes
❌ **Validation only** — Use `@property` instead
❌ **Missing attributes** — Use `__getattr__` instead (cheaper, safer)
❌ **Performance-critical paths** — Every attribute read passes through this hook,
including internal accesses like `self.x` inside other methods. In tight loops this
overhead is measurable.

!!! warning "Performance cost"
    `__getattribute__` is called for **every** attribute access — not just the ones
    you care about. A class with 5 attributes accessed in a method body triggers 5
    calls per invocation. In contrast, `__getattr__` is **free** for existing
    attributes (it is never called). Prefer `__getattr__` or `@property` unless you
    genuinely need to intercept all reads (proxies, frameworks).

!!! tip "The Master Insight"
    Everything in Python is built on attribute access. Even a method call like `obj.method()` is actually:

    1. `type(obj).__getattribute__(obj, 'method')` — finds the function
    2. `function.__get__(obj, type(obj))` — descriptor produces a bound method
    3. The bound method is then called

    This means **all Python behavior starts with attribute lookup**. Descriptors, methods, properties, and protocols all flow through `__getattribute__`. Understanding this single hook is the key to understanding the entire Python object model.

## Common Mistakes

### 1. Infinite Recursion

```python
# ❌ BAD
def __getattribute__(self, name):
    if self.ready:  # Calls __getattribute__!
        return self.value
```

**Fix:**
```python
# ✅ GOOD
def __getattribute__(self, name):
    ready = super().__getattribute__('ready')
    if ready:
        return super().__getattribute__('value')
```

### 2. Forgetting to Return

```python
# ❌ BAD
def __getattribute__(self, name):
    print(f"Accessing {name}")
    # Forgot to return!

# Returns None for everything!
```

### 3. Breaking Built-ins

```python
# ❌ BAD
def __getattribute__(self, name):
    return "always this"  # Breaks __dict__, __class__, etc.
```

---

## Exercises

**Exercise 1.**
Create a class `AccessLogger` that overrides `__getattribute__` to print a message every time ANY attribute is accessed (including methods). Use `super().__getattribute__()` to avoid infinite recursion. Demonstrate with a class that has both data attributes and methods.

??? success "Solution to Exercise 1"

        class AccessLogger:
            def __init__(self, x, y):
                self.x = x
                self.y = y

            def __getattribute__(self, name):
                print(f"Accessing: {name}")
                return super().__getattribute__(name)

            def sum(self):
                return self.x + self.y

        obj = AccessLogger(10, 20)
        print(obj.x)      # Accessing: x -> 10
        print(obj.sum())   # Accessing: sum, Accessing: x, Accessing: y -> 30

---

**Exercise 2.**
Write a class `CaseInsensitiveAccess` where `__getattribute__` converts attribute names to lowercase before looking them up. Set attributes with mixed case in `__init__` (using `object.__setattr__` with lowercase keys). Show that `obj.Name`, `obj.NAME`, and `obj.name` all return the same value.

??? success "Solution to Exercise 2"

        class CaseInsensitiveAccess:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    object.__setattr__(self, k.lower(), v)

            def __getattribute__(self, name):
                return super().__getattribute__(name.lower())

        obj = CaseInsensitiveAccess(Name="Alice", Age=30)
        print(obj.name)   # Alice
        print(obj.NAME)   # Alice
        print(obj.Name)   # Alice
        print(obj.AGE)    # 30

---

**Exercise 3.**
Build a class `CountedAccess` that tracks how many times each attribute has been accessed. Override `__getattribute__` to increment a counter (stored in a dictionary) each time an attribute is read. Provide a method `access_counts()` that returns the counts. Be careful to avoid recursion when accessing the counter dict itself.

??? success "Solution to Exercise 3"

        class CountedAccess:
            def __init__(self, **kwargs):
                object.__setattr__(self, '_counts', {})
                for k, v in kwargs.items():
                    object.__setattr__(self, k, v)

            def __getattribute__(self, name):
                if name in ('_counts', 'access_counts'):
                    return super().__getattribute__(name)
                counts = super().__getattribute__('_counts')
                counts[name] = counts.get(name, 0) + 1
                return super().__getattribute__(name)

            def access_counts(self):
                return dict(self._counts)

        obj = CountedAccess(x=10, y=20)
        _ = obj.x
        _ = obj.x
        _ = obj.y
        print(obj.access_counts())  # {'x': 2, 'y': 1}

---

**Exercise 4.**
Explain why the following code produces infinite recursion. Trace the first three calls step by step. Then fix it using two different approaches: `super().__getattribute__()` and `object.__getattribute__()`.

```python
class Broken:
    def __init__(self):
        self.data = [1, 2, 3]

    def __getattribute__(self, name):
        print(f"Getting {name}")
        if name == "data":
            return self.data  # Intended to return self.data
        return super().__getattribute__(name)
```

??? success "Solution to Exercise 4"

    **Trace of the recursion:**

    1. `obj.data` → calls `__getattribute__("data")`
    2. Inside, `self.data` → calls `__getattribute__("data")` again
    3. Inside, `self.data` → calls `__getattribute__("data")` again
    4. ... infinite recursion → `RecursionError`

    The problem is that `self.data` inside `__getattribute__` triggers another call to `__getattribute__`, creating a loop.

    **Fix 1 — `super()`:**

        def __getattribute__(self, name):
            print(f"Getting {name}")
            return super().__getattribute__(name)

    **Fix 2 — `object.__getattribute__`:**

        def __getattribute__(self, name):
            print(f"Getting {name}")
            return object.__getattribute__(self, name)

    Both bypass the custom `__getattribute__` and go directly to the default implementation, which reads from `__dict__` and the class hierarchy without recursion. The rule: **never use `self.anything` inside `__getattribute__`** — always use `super()` or `object.__getattribute__`.

---

**Exercise 5.**
A class uses `__getattribute__` to block access to attributes whose names start with `_`. A colleague points out that this also blocks `__dict__`, `__class__`, and `__repr__`, breaking basic Python functionality. Explain why, and write a version that blocks single-underscore attributes (like `_secret`) while allowing dunder attributes (like `__dict__`).

??? success "Solution to Exercise 5"

    Dunder attributes (`__dict__`, `__class__`, `__repr__`) also start with `_`, so a blanket check `name.startswith('_')` blocks them too. Without `__dict__`, `vars(obj)` fails. Without `__class__`, `type(obj)` and `isinstance()` fail. Without `__repr__`, printing the object fails.

    **Fixed version:**

        class SafeRestricted:
            def __init__(self):
                self._secret = "hidden"
                self.public = "visible"

            def __getattribute__(self, name):
                # Allow dunder attributes (start AND end with __)
                if name.startswith('__') and name.endswith('__'):
                    return super().__getattribute__(name)
                # Block single-underscore private attributes
                if name.startswith('_'):
                    raise AttributeError(f"Access denied: {name}")
                return super().__getattribute__(name)

        obj = SafeRestricted()
        print(obj.public)       # "visible" — allowed
        print(type(obj))        # <class 'SafeRestricted'> — __class__ allowed
        print(vars(obj))        # works — __dict__ allowed

        try:
            obj._secret
        except AttributeError as e:
            print(e)  # Access denied: _secret

    The key insight: dunder names (`__x__`) are Python infrastructure — they must always be accessible. Single-underscore names (`_x`) are the convention for "internal" attributes.
