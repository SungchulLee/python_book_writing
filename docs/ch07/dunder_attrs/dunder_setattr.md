# __setattr__

!!! tip "Mental Model"
    `__setattr__` intercepts every `obj.attr = value` assignment -- including those inside `__init__`. This makes it a universal validation and logging hook, but it also means you must use `super().__setattr__()` or direct `__dict__` writes internally to avoid infinite recursion. Think of it as a customs checkpoint: everything passes through, so your inspection logic must know which shipments to wave through.

## Fundamentals

### 1. Definition

The `__setattr__` method is called **whenever you assign to an attribute** on an object:

```python
obj.attr = value  # Triggers obj.__setattr__('attr', value)
setattr(obj, 'attr', value)  # Also triggers __setattr__
```

### 2. Method Signature

```python
def __setattr__(self, name, value):
    # name: attribute name (string)
    # value: value being assigned
    pass
```

### 3. Universal Assignment Hook

Every attribute assignment goes through `__setattr__`:

```python
self.x = 10       # Calls __setattr__('x', 10)
self.name = "hi"  # Calls __setattr__('name', "hi")
self.data = []    # Calls __setattr__('data', [])
```

!!! note "Symmetry with Other Attribute Hooks"

    The three attribute-mutation hooks form a symmetric system:

    | Operation | Syntax | Hook |
    |---|---|---|
    | Read | `obj.attr` | `__getattribute__` → `__getattr__` (fallback) |
    | Write | `obj.attr = val` | `__setattr__` (always) |
    | Delete | `del obj.attr` | `__delattr__` (always) |

    Reading has a two-stage fallback (`__getattribute__` first, then `__getattr__` if not found). Writing and deletion each have a single hook that runs unconditionally. This asymmetry exists because reads need a "not found" fallback while writes and deletes always know their target.

## Basic Implementation

### 1. Simple Override

```python
class MyClass:
    def __setattr__(self, name, value):
        print(f"Setting {name} = {value}")
        super().__setattr__(name, value)

obj = MyClass()
obj.x = 42
# Output: Setting x = 42

obj.name = "Alice"
# Output: Setting name = Alice
```

### 2. Without super()

```python
class MyClass:
    def __setattr__(self, name, value):
        print(f"Setting {name} = {value}")
        object.__setattr__(self, name, value)
```

### 3. Must Actually Store

```python
# ❌ BAD - doesn't actually store anything
def __setattr__(self, name, value):
    print(f"Setting {name}")
    # Forgot to actually set it!

# ✅ GOOD
def __setattr__(self, name, value):
    print(f"Setting {name}")
    super().__setattr__(name, value)
```

## Avoiding Recursion

### 1. The Problem

```python
class Broken:
    def __setattr__(self, name, value):
        # ❌ INFINITE RECURSION!
        self.name = value  # Calls __setattr__ again!
```

### 2. Correct Approaches

**Use `super()`:**
```python
class Correct:
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
```

**Use `object.__setattr__`:**
```python
class Correct:
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
```

**Direct `__dict__` access:**
```python
class Correct:
    def __setattr__(self, name, value):
        self.__dict__[name] = value
```

### 3. In `__init__`

Be careful in constructors:

```python
class Example:
    def __init__(self, value):
        self.value = value  # ✅ Calls __setattr__
    
    def __setattr__(self, name, value):
        print(f"Setting {name}")
        super().__setattr__(name, value)

obj = Example(42)
# Output: Setting value
```

## Practical Examples

### 1. Validation

```python
class Person:
    def __setattr__(self, name, value):
        if name == 'age':
            if not isinstance(value, int):
                raise TypeError("Age must be integer")
            if value < 0 or value > 150:
                raise ValueError("Invalid age range")
        elif name == 'name':
            if not isinstance(value, str):
                raise TypeError("Name must be string")
            if not value.strip():
                raise ValueError("Name cannot be empty")
        
        super().__setattr__(name, value)

person = Person()
person.name = "Alice"  # ✅ OK
person.age = 30        # ✅ OK
# person.age = -5      # ❌ ValueError
# person.name = ""     # ❌ ValueError
```

### 2. Type Coercion

```python
class TypedAttributes:
    def __setattr__(self, name, value):
        if name == 'count':
            value = int(value)  # Convert to int
        elif name == 'price':
            value = float(value)  # Convert to float
        elif name == 'name':
            value = str(value).strip()  # Convert to string
        
        super().__setattr__(name, value)

obj = TypedAttributes()
obj.count = "42"      # Stored as int(42)
obj.price = "19.99"   # Stored as float(19.99)
obj.name = "  hi  "   # Stored as "hi"
```

### 3. Change Tracking

```python
class TrackedObject:
    def __init__(self):
        super().__setattr__('_changes', {})
    
    def __setattr__(self, name, value):
        if name != '_changes':
            # Track old value
            if hasattr(self, name):
                old_value = super().__getattribute__(name)
            else:
                old_value = None
            
            # Record change — use a list to preserve full history
            changes = super().__getattribute__('_changes')
            changes.setdefault(name, []).append((old_value, value))
        
        super().__setattr__(name, value)

obj = TrackedObject()
obj.x = 10
obj.x = 20
obj.y = 30
print(obj._changes)
# {'x': [(None, 10), (10, 20)], 'y': [(None, 30)]}
```

## Read-Only Attributes

### 1. Protecting Attributes

```python
class ReadOnlyAttrs:
    def __init__(self):
        super().__setattr__('_locked', False)
        self.value = 42
        super().__setattr__('_locked', True)
    
    def __setattr__(self, name, value):
        if super().__getattribute__('_locked'):
            raise AttributeError("Attributes are read-only")
        super().__setattr__(name, value)

obj = ReadOnlyAttrs()
print(obj.value)      # 42
# obj.value = 100     # ❌ AttributeError
# obj.new_attr = 5    # ❌ AttributeError
```

### 2. Protecting Specific Attributes

```python
class ProtectedID:
    def __init__(self, id_value):
        self._id = id_value
        self.name = ""
    
    def __setattr__(self, name, value):
        if name == '_id' and hasattr(self, '_id'):
            raise AttributeError("Cannot modify ID after initialization")
        super().__setattr__(name, value)

obj = ProtectedID(123)
obj.name = "Alice"   # ✅ OK
# obj._id = 456      # ❌ AttributeError
```

### 3. Conditional Write Protection

```python
class Document:
    def __init__(self):
        self._finalized = False
        self.content = ""
    
    def finalize(self):
        self._finalized = True
    
    def __setattr__(self, name, value):
        if name != '_finalized':
            if hasattr(self, '_finalized') and self._finalized:
                raise AttributeError("Document is finalized")
        super().__setattr__(name, value)

doc = Document()
doc.content = "Draft"  # ✅ OK
doc.finalize()
# doc.content = "New"  # ❌ AttributeError
```

## Logging and Debugging

```python
from datetime import datetime

class AuditedObject:
    """Logs every attribute write with a timestamp."""
    def __init__(self):
        super().__setattr__('_history', [])
    
    def __setattr__(self, name, value):
        if name != '_history':
            history = super().__getattribute__('_history')
            history.append({
                'attr': name,
                'value': value,
                'time': datetime.now()
            })
            print(f"[SET] {name} = {value} (type: {type(value).__name__})")
        super().__setattr__(name, value)

obj = AuditedObject()
obj.x = 42
# [SET] x = 42 (type: int)
print(obj._history)
# [{'attr': 'x', 'value': 42, 'time': datetime(...)}]
```

## __setattr__ vs @property Setters

Both `__setattr__` and `@property` setters intercept attribute writes, but they
serve different purposes:

| Concern | `__setattr__` | `@property` setter |
|---------|--------------|-------------------|
| Scope | **All** attributes | **One** named attribute |
| Use when | You need blanket validation, logging, or type enforcement across many attributes | You need custom logic for a specific attribute |
| Performance | Runs on every assignment (including `__init__`) | Runs only for the decorated name |
| Complexity | Higher — must avoid recursion, handle internal attrs | Lower — self-contained |

**Rule of thumb**: if you only need to control one or two attributes, use
`@property`. Reach for `__setattr__` when the policy applies to all (or most)
attributes uniformly.

## Interaction with Properties

### 1. Properties Take Priority

```python
class Example:
    def __init__(self):
        self._value = 0
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        print("Property setter")
        self._value = val
    
    def __setattr__(self, name, value):
        print(f"__setattr__: {name}")
        super().__setattr__(name, value)

obj = Example()
obj.value = 42
# Output:
# __setattr__: _value
# __setattr__: value
# Property setter
# __setattr__: _value
```

### 2. Call Order

```python
obj.value = 42
    ↓
__setattr__('value', 42) called
    ↓
super().__setattr__('value', 42)
    ↓
Finds property descriptor in class
    ↓
Calls property's __set__ method
    ↓
Inside setter: self._value = val
    ↓
__setattr__('_value', val) called again
```

### 3. Bypassing Properties

```python
def __setattr__(self, name, value):
    if name == 'special':
        # Bypass property, set directly
        self.__dict__[name] = value
    else:
        super().__setattr__(name, value)
```

## Advanced Patterns

### 1. Attribute Registry

```python
class RegisteredAttributes:
    _registry = {}
    
    def __setattr__(self, name, value):
        # Register all attributes
        RegisteredAttributes._registry[id(self), name] = value
        super().__setattr__(name, value)
    
    @classmethod
    def get_all_values(cls):
        return list(cls._registry.values())
```

### 2. Proxy Pattern

```python
class Proxy:
    def __init__(self, obj):
        object.__setattr__(self, '_obj', obj)
    
    def __setattr__(self, name, value):
        if name == '_obj':
            object.__setattr__(self, name, value)
        else:
            setattr(object.__getattribute__(self, '_obj'), name, value)

class Target:
    def __init__(self):
        self.value = 0

proxy = Proxy(Target())
proxy.value = 42
```

### 3. Slots Enforcement

```python
class StrictSlots:
    __slots__ = ['x', 'y']
    
    def __setattr__(self, name, value):
        if name not in self.__slots__:
            raise AttributeError(f"'{name}' not in __slots__")
        super().__setattr__(name, value)

obj = StrictSlots()
obj.x = 10  # ✅ OK
# obj.z = 20  # ❌ AttributeError
```

## When NOT to Use __setattr__

!!! warning "Avoid When"

    - **Validating only one or two attributes** — use `@property` setters instead. `__setattr__` intercepts *every* assignment, including internal ones in `__init__`, which adds complexity for no benefit when only one field needs validation.
    - **Simple logging of one attribute** — a property setter with a `print` is far simpler.
    - **Performance-sensitive code** — `__setattr__` runs on every assignment, including `self.x = ...` inside methods. In tight loops this overhead is measurable.

    Use `__setattr__` only when the policy applies to **all or most** attributes uniformly (type enforcement, change tracking, freezing). For per-attribute control, `@property` is the right tool.

## Common Mistakes

### 1. Infinite Recursion

```python
# ❌ BAD
def __setattr__(self, name, value):
    self.name = value  # Recursion!

# ✅ GOOD
def __setattr__(self, name, value):
    super().__setattr__(name, value)
```

### 2. Not Storing Values

```python
# ❌ BAD - validation but no storage
def __setattr__(self, name, value):
    if isinstance(value, int):
        print("Valid")
    # Value is never stored!

# ✅ GOOD
def __setattr__(self, name, value):
    if isinstance(value, int):
        print("Valid")
    super().__setattr__(name, value)
```

### 3. Breaking `__init__`

```python
# ❌ BAD
def __setattr__(self, name, value):
    if hasattr(self, 'initialized'):
        # Logic here
        pass
    # Can't set 'initialized' in __init__!

# ✅ GOOD
def __setattr__(self, name, value):
    if name == 'initialized' or not hasattr(self, 'initialized'):
        super().__setattr__(name, value)
    else:
        # Logic here
        super().__setattr__(name, value)
```

---

## Exercises

**Exercise 1.**
Create a class `TypeEnforced` that uses `__setattr__` to enforce types based on a class-level `_types` dictionary. For example, `_types = {"name": str, "age": int}` means `name` must always be a string and `age` must always be an int. Raise `TypeError` on violation. Allow attributes not in `_types` to be set freely.

??? success "Solution to Exercise 1"

        class TypeEnforced:
            _types = {"name": str, "age": int}

            def __setattr__(self, name, value):
                if name in self._types:
                    expected = self._types[name]
                    if not isinstance(value, expected):
                        raise TypeError(
                            f"'{name}' must be {expected.__name__}, got {type(value).__name__}"
                        )
                super().__setattr__(name, value)

        obj = TypeEnforced()
        obj.name = "Alice"  # OK
        obj.age = 30        # OK
        obj.other = [1, 2]  # OK — not in _types

        try:
            obj.age = "thirty"
        except TypeError as e:
            print(f"Error: {e}")
            # Error: 'age' must be int, got str

---

**Exercise 2.**
Write a class `HistoryTracked` where `__setattr__` keeps a history of all values assigned to each attribute. Store the history in a `_history` dictionary. Provide a `get_history(attr_name)` method that returns the list of past values. Use `object.__setattr__` to avoid recursion.

??? success "Solution to Exercise 2"

        class HistoryTracked:
            def __init__(self, **kwargs):
                object.__setattr__(self, '_history', {})
                for k, v in kwargs.items():
                    setattr(self, k, v)

            def __setattr__(self, name, value):
                history = object.__getattribute__(self, '_history')
                if name not in history:
                    history[name] = []
                history[name].append(value)
                object.__setattr__(self, name, value)

            def get_history(self, attr_name):
                return self._history.get(attr_name, [])

        obj = HistoryTracked(x=1)
        obj.x = 2
        obj.x = 3
        print(obj.x)               # 3
        print(obj.get_history("x")) # [1, 2, 3]

---

**Exercise 3.**
Build a class `WriteOnce` where `__setattr__` allows an attribute to be set only if it does not already exist. If the attribute already exists, raise `AttributeError`. Use this to create objects whose attributes can be set in `__init__` but never changed afterward.

??? success "Solution to Exercise 3"

        class WriteOnce:
            def __setattr__(self, name, value):
                if hasattr(self, name):
                    raise AttributeError(f"'{name}' already set and cannot be changed")
                super().__setattr__(name, value)

        obj = WriteOnce()
        obj.name = "Alice"
        obj.age = 30
        print(obj.name)  # Alice

        try:
            obj.name = "Bob"
        except AttributeError as e:
            print(f"Error: {e}")
            # Error: 'name' already set and cannot be changed

---

**Exercise 4.**
Explain why the following `__init__` triggers `__setattr__` three times, even though the developer only intends to set two user-visible attributes. Trace each `__setattr__` call with the attribute name and value.

```python
class Traced:
    def __init__(self, x, y):
        self._internal = []
        self.x = x
        self.y = y

    def __setattr__(self, name, value):
        print(f"__setattr__({name!r}, {value!r})")
        super().__setattr__(name, value)

obj = Traced(10, 20)
```

??? success "Solution to Exercise 4"

    Output:

        __setattr__('_internal', [])
        __setattr__('x', 10)
        __setattr__('y', 20)

    `__setattr__` runs for **every** assignment, including `self._internal = []` inside `__init__`. This is often surprising — developers assume `__setattr__` only fires for "user" assignments, but Python makes no distinction.

    This is why `__setattr__` implementations must handle internal attributes carefully:

    - **Option 1:** Check `if name == '_internal'` and skip validation.
    - **Option 2:** Use `object.__setattr__(self, '_internal', [])` in `__init__` to bypass the custom hook for internal setup.
    - **Option 3:** Use a flag like `_initialized` (set via `object.__setattr__`) and only apply validation after initialization is complete.

    The takeaway: `__setattr__` has no concept of "internal" vs "external" — all assignments are equal.

---

**Exercise 5.**
Compare `__setattr__` and `@property` for the following scenario: a `Temperature` class where `celsius` must always be a non-negative number. Implement both approaches. Then explain which you would choose if the class also needs `fahrenheit` and `kelvin` attributes with similar validation.

??? success "Solution to Exercise 5"

        # Approach 1: @property (per-attribute)
        class TempProperty:
            def __init__(self, celsius):
                self.celsius = celsius

            @property
            def celsius(self):
                return self._celsius

            @celsius.setter
            def celsius(self, value):
                if not isinstance(value, (int, float)) or value < 0:
                    raise ValueError("celsius must be a non-negative number")
                self._celsius = value

        # Approach 2: __setattr__ (blanket policy)
        class TempSetattr:
            _numeric_fields = {"celsius", "fahrenheit", "kelvin"}

            def __init__(self, celsius):
                self.celsius = celsius

            def __setattr__(self, name, value):
                if name in self._numeric_fields:
                    if not isinstance(value, (int, float)) or value < 0:
                        raise ValueError(f"{name} must be a non-negative number")
                super().__setattr__(name, value)

        # Both work for one attribute
        t1 = TempProperty(100)
        t2 = TempSetattr(100)

    **For one attribute:** `@property` is simpler — it's self-contained, no recursion risk, and the validation logic is co-located with the getter.

    **For three attributes with identical rules:** `__setattr__` is better — writing three `@property` blocks with identical validation logic is repetitive. `__setattr__` applies the rule once to all fields in `_numeric_fields`.

    **Rule of thumb:** use `@property` when each attribute has unique validation logic. Use `__setattr__` when the same rule applies uniformly to multiple attributes.
