# __getattr__

!!! tip "Mental Model"
    `__getattr__` is the safety net at the bottom of Python's attribute lookup chain -- it only fires when every other lookup mechanism has failed. This makes it perfect for lazy defaults, proxy delegation, and deprecated-attribute warnings, without the performance or recursion risks of intercepting every access via `__getattribute__`.

!!! tip "Core Idea"
    `__getattr__` is the **fallback of last resort** — called only when the attribute was not found by the normal lookup chain ([`__getattribute__`](dunder_getattribute.md) → instance `__dict__` → class/MRO → descriptors). It is cheaper and safer than `__getattribute__` because it never fires for existing attributes.

## Fundamentals

### 1. Definition

The `__getattr__` method is called **only when regular attribute lookup fails**:

```python
obj.missing_attr  # Triggers __getattr__ if 'missing_attr' not found
```

### 2. Method Signature

```python
def __getattr__(self, name):
    # Called only for missing attributes
    # Can return a value or raise AttributeError
    pass
```

### 3. Fallback Mechanism

```python
obj.attr
    ↓
__getattribute__('attr') called
    ↓
Attribute found? → Return it
    ↓
Not found? → AttributeError
    ↓
__getattr__('attr') called (if defined)
    ↓
Return value or raise AttributeError
```

## Basic Implementation

### 1. Simple Example

```python
class MyClass:
    def __init__(self):
        self.existing = "I exist"
    
    def __getattr__(self, name):
        return f"Default value for {name}"

obj = MyClass()
print(obj.existing)     # "I exist" (normal lookup)
print(obj.missing)      # "Default value for missing" (__getattr__)
print(obj.anything)     # "Default value for anything" (__getattr__)
```

### 2. Providing Defaults

```python
class Config:
    def __init__(self):
        self.host = "localhost"
    
    def __getattr__(self, name):
        defaults = {
            'port': 8080,
            'debug': False,
            'timeout': 30
        }
        if name in defaults:
            return defaults[name]
        raise AttributeError(f"No attribute: {name}")

config = Config()
print(config.host)    # "localhost" (exists)
print(config.port)    # 8080 (from __getattr__)
print(config.debug)   # False (from __getattr__)
```

### 3. Raising Errors

```python
def __getattr__(self, name):
    raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
```

## Only for Missing Attributes

### 1. Comparison

```python
class Example:
    def __init__(self):
        self.exists = "value"
    
    def __getattr__(self, name):
        print(f"__getattr__ called for: {name}")
        return "default"

obj = Example()
print(obj.exists)   # "value" (__getattr__ NOT called)
print(obj.missing)  # "default" (__getattr__ IS called)
```

### 2. When It Fires (and When It Does Not)

`__getattr__` is the **fallback of last resort**. It fires only when every other
lookup mechanism has failed — the instance `__dict__`, class and parent descriptors,
and `__getattribute__` itself have all come up empty (i.e., raised `AttributeError`).
If the attribute exists anywhere in the normal chain, `__getattr__` is never called.

!!! tip "Interaction with `__dir__`"
    If your `__getattr__` synthesizes attributes dynamically, also override `__dir__`
    to list them. Tools like `dir()`, tab completion, and `help()` rely on `__dir__`
    and will not discover dynamically generated attributes otherwise.

!!! danger "Interaction with `hasattr` — Common Source of Bugs"
    `hasattr(obj, name)` works by calling `getattr(obj, name)` and returning `False`
    only if `AttributeError` is raised. If your `__getattr__` returns a default value
    (like `None`) instead of raising `AttributeError` for unknown names, then
    `hasattr()` will return `True` for **every** attribute name — even nonsensical ones
    like `hasattr(obj, 'asdfgh')`. This breaks duck-typing checks, confuses
    serialization libraries, and makes debugging extremely difficult.

    **Rule:** always raise `AttributeError` for names you do not explicitly handle.
    Never use a catch-all `return None` unless you genuinely intend every possible
    attribute name to be valid.

## Practical Examples

### 1. Dynamic Attributes

```python
class DynamicObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __getattr__(self, name):
        return f"No attribute '{name}' - returning None"

obj = DynamicObject(name="Alice", age=30)
print(obj.name)     # "Alice"
print(obj.age)      # 30
print(obj.email)    # "No attribute 'email' - returning None"
```

### 2. Lazy Loading

```python
class LazyLoader:
    def __init__(self):
        self._cache = {}
    
    def __getattr__(self, name):
        if name.startswith('data_'):
            print(f"Loading {name}...")
            # Simulate expensive operation
            data = f"Loaded data for {name}"
            # Cache it
            self._cache[name] = data
            setattr(self, name, data)  # Store in __dict__
            return data
        raise AttributeError(f"No attribute: {name}")

loader = LazyLoader()
print(loader.data_users)      # Loading data_users... Loaded data for data_users
print(loader.data_users)      # Loaded data for data_users (from __dict__, __getattr__ not called)
```

### 3. Attribute Delegation

```python
class Wrapper:
    def __init__(self, wrapped_object):
        self._wrapped = wrapped_object
    
    def __getattr__(self, name):
        # Delegate to wrapped object
        return getattr(self._wrapped, name)

class Target:
    def __init__(self):
        self.value = 42
    
    def method(self):
        return "method called"

wrapper = Wrapper(Target())
print(wrapper.value)     # 42 (delegated)
print(wrapper.method())  # "method called" (delegated)
```

## vs __getattribute__

### 1. Key Differences

| Aspect | `__getattribute__` | `__getattr__` |
|--------|-------------------|---------------|
| When called | **Every** attribute access | **Only** missing attributes |
| Frequency | Always | Rarely (only on failure) |
| Use case | Universal interception | Graceful fallback |
| Complexity | High (easy to break) | Low (safer) |
| Performance | Slower (always runs) | Faster (rarely runs) |

### 2. Example

```python
class Comparison:
    def __init__(self):
        self.exists = "value"
    
    def __getattribute__(self, name):
        print(f"__getattribute__: {name}")
        return super().__getattribute__(name)
    
    def __getattr__(self, name):
        print(f"__getattr__: {name}")
        return "default"

obj = Comparison()
print("=" * 40)
print(obj.exists)
# __getattribute__: exists
# value

print("=" * 40)
print(obj.missing)
# __getattribute__: missing
# __getattr__: missing
# default
```

### 3. When to Choose

**Use `__getattr__`:**

- Providing default values
- Delegating to another object
- Lazy loading attributes
- Backward compatibility (old attribute names)

**Use `__getattribute__`:**

- Logging all access
- Proxying everything
- Universal access control
- Complete attribute control

## Advanced Patterns

### 1. Database-Backed Attributes

```python
class DatabaseModel:
    def __init__(self, record_id):
        self.id = record_id
        self._cache = {}
    
    def __getattr__(self, name):
        # Check cache first
        if name in self._cache:
            return self._cache[name]
        
        # Query database
        print(f"Querying database for {name}...")
        value = f"DB value for {name}"
        
        # Cache result
        self._cache[name] = value
        return value

model = DatabaseModel(123)
print(model.name)      # Querying database for name... DB value for name
print(model.name)      # DB value for name (from cache)
print(model.email)     # Querying database for email... DB value for email
```

### 2. Method Generation

```python
class DynamicMethods:
    def __getattr__(self, name):
        if name.startswith('get_'):
            field = name[4:]  # Remove 'get_' prefix
            return lambda: f"Getting {field}"
        elif name.startswith('set_'):
            field = name[4:]  # Remove 'set_' prefix
            return lambda value: f"Setting {field} to {value}"
        raise AttributeError(f"No attribute: {name}")

obj = DynamicMethods()
print(obj.get_name())         # "Getting name"
print(obj.set_age(30))        # "Setting age to 30"
```

### 3. Nested Attribute Access

```python
class NestedAccess:
    def __init__(self, data):
        self._data = data
    
    def __getattr__(self, name):
        if '.' in name:
            # Handle nested access like 'user.profile.email'
            parts = name.split('.')
            value = self._data
            for part in parts:
                value = value.get(part)
                if value is None:
                    raise AttributeError(f"No nested attribute: {name}")
            return value
        
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No attribute: {name}")

data = {
    'user': {
        'profile': {
            'email': 'alice@example.com'
        }
    }
}
obj = NestedAccess(data)
print(obj.user)  # {'profile': {'email': 'alice@example.com'}}
```

## Common Pitfalls

### 1. Forgetting to Raise

```python
# ❌ BAD - returns None for everything missing
def __getattr__(self, name):
    if name in self.valid_attrs:
        return self.valid_attrs[name]
    # Forgot to raise AttributeError!

# ✅ GOOD
def __getattr__(self, name):
    if name in self.valid_attrs:
        return self.valid_attrs[name]
    raise AttributeError(f"No attribute: {name}")
```

### 2. Infinite Recursion

```python
# ❌ BAD
def __getattr__(self, name):
    return self.default_value  # If 'default_value' missing, infinite loop!

# ✅ GOOD
def __getattr__(self, name):
    return object.__getattribute__(self, 'default_value')
```

### 3. Not Storing Loaded Values

```python
# ❌ BAD - reloads every time
def __getattr__(self, name):
    return self._load_from_db(name)  # Always hits database!

# ✅ GOOD - cache after loading
def __getattr__(self, name):
    value = self._load_from_db(name)
    setattr(self, name, value)  # Store in __dict__
    return value
```

## Best Practices

### 1. Clear Error Messages

```python
def __getattr__(self, name):
    valid = ', '.join(self._valid_attributes)
    raise AttributeError(
        f"'{type(self).__name__}' has no attribute '{name}'. "
        f"Valid attributes: {valid}"
    )
```

### 2. Document Behavior

```python
class DynamicAPI:
    """
    Provides dynamic attribute access.
    
    Any attribute access will query the API endpoint
    with the same name. Results are cached.
    
    Example:
        api.users  # Calls /api/users
        api.posts  # Calls /api/posts
    """
    def __getattr__(self, name):
        return self._fetch_endpoint(name)
```

### 3. Limit Scope

```python
def __getattr__(self, name):
    # Only handle specific pattern
    if not name.startswith('dynamic_'):
        raise AttributeError(f"No attribute: {name}")
    
    # Handle dynamic attributes
    return self._handle_dynamic(name)
```

---

## Exercises

**Exercise 1.**
Create a `FlexibleConfig` class that uses `__getattr__` to return a default value of `None` for any attribute that has not been explicitly set. Set a few attributes in `__init__` and show that existing attributes return their values while missing attributes return `None` without raising `AttributeError`.

??? success "Solution to Exercise 1"

        class FlexibleConfig:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    self.__dict__[k] = v

            def __getattr__(self, name):
                return None  # Default for missing attributes

        cfg = FlexibleConfig(host="localhost", port=8080)
        print(cfg.host)    # localhost
        print(cfg.port)    # 8080
        print(cfg.debug)   # None — missing, no error
        print(cfg.timeout) # None

---

**Exercise 2.**
Write a `Proxy` class that wraps another object. Use `__getattr__` to forward any attribute access to the wrapped object. Demonstrate by wrapping a list and accessing methods like `append`, `pop`, and `__len__` through the proxy.

??? success "Solution to Exercise 2"

        class Proxy:
            def __init__(self, wrapped):
                object.__setattr__(self, '_wrapped', wrapped)

            def __getattr__(self, name):
                return getattr(self._wrapped, name)

        proxy = Proxy([1, 2, 3])
        proxy.append(4)
        print(proxy.pop())     # 4
        print(len(proxy))      # 3 — __len__ forwarded
        print(list(proxy))     # [1, 2, 3]

---

**Exercise 3.**
Build a `DeprecatedAttributes` class where `__getattr__` checks a mapping of old attribute names to new ones. If a deprecated name is accessed, print a warning and return the value from the new attribute. If the name is not in the mapping, raise `AttributeError`. Demonstrate the deprecation warning.

??? success "Solution to Exercise 3"

        class DeprecatedAttributes:
            _deprecated = {
                "colour": "color",
                "favourite": "favorite",
            }

            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    self.__dict__[k] = v

            def __getattr__(self, name):
                if name in self._deprecated:
                    new_name = self._deprecated[name]
                    print(f"Warning: '{name}' is deprecated, use '{new_name}'")
                    return getattr(self, new_name)
                raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        obj = DeprecatedAttributes(color="red", favorite="pizza")
        print(obj.colour)    # Warning: 'colour' is deprecated... -> red
        print(obj.favorite)  # pizza (direct access, no warning)

        try:
            obj.unknown
        except AttributeError as e:
            print(f"Error: {e}")

---

**Exercise 4.**
Demonstrate the `hasattr` trap. Create a class `BadDefault` whose `__getattr__` returns `None` for any missing attribute. Show that `hasattr(obj, 'nonexistent_xyz')` returns `True`. Then fix it by creating `SafeDefault` that returns defaults only for a known set of attribute names and raises `AttributeError` for everything else.

??? success "Solution to Exercise 4"

        # BAD — hasattr always returns True
        class BadDefault:
            def __getattr__(self, name):
                return None

        obj = BadDefault()
        print(hasattr(obj, "nonexistent_xyz"))  # True — broken!
        print(hasattr(obj, "literally_anything"))  # True — broken!

        # FIXED — only known defaults
        class SafeDefault:
            _defaults = {"timeout": 30, "retries": 3, "debug": False}

            def __getattr__(self, name):
                if name in self._defaults:
                    return self._defaults[name]
                raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        obj = SafeDefault()
        print(obj.timeout)  # 30
        print(hasattr(obj, "timeout"))  # True
        print(hasattr(obj, "nonexistent_xyz"))  # False — correct!

    The fix is simple: explicitly list which attributes have defaults. Raise `AttributeError` for everything else so that `hasattr()`, duck-typing checks, and serialization libraries all work correctly.

---

**Exercise 5.**
Build a `LazyProperties` class where `__getattr__` computes expensive attributes on first access and caches the result in `__dict__` so that subsequent accesses bypass `__getattr__` entirely. The class should have a `_lazy_specs` dictionary mapping attribute names to zero-argument factory functions. Demonstrate that the factory runs once, then show that the second access goes straight to `__dict__` (no `__getattr__` call).

??? success "Solution to Exercise 5"

        class LazyProperties:
            _lazy_specs = {
                "squares": lambda: [x ** 2 for x in range(1000)],
                "greeting": lambda: "Hello, World!",
            }

            def __getattr__(self, name):
                if name in self._lazy_specs:
                    print(f"Computing '{name}' for the first time...")
                    value = self._lazy_specs[name]()
                    # Store in __dict__ — future reads won't trigger __getattr__
                    self.__dict__[name] = value
                    return value
                raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

        obj = LazyProperties()

        # First access — __getattr__ runs, factory computes value
        print(len(obj.squares))  # Computing 'squares'... 1000

        # Second access — reads from __dict__, __getattr__ NOT called
        print(len(obj.squares))  # 1000 (no "Computing" message)

        # Verify it's in __dict__
        print("squares" in obj.__dict__)  # True

    This is the **lazy loading pattern**: `__getattr__` fires only for missing attributes, so storing the result in `__dict__` ensures the computation runs exactly once. This is simpler and cheaper than using `__getattribute__` for the same purpose.
