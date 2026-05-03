# __delattr__

`__delattr__` is the least commonly overridden of the four attribute hooks. In most
codebases, the default behavior (remove the attribute from `__dict__`) is sufficient.
Override it only when you need to **protect** attributes from deletion, **clean up**
associated resources, or **audit** deletions. For simple cases, a `@property` deleter
on a specific attribute is usually clearer.

!!! tip "Mental Model"
    `__delattr__` is the gatekeeper for `del obj.attr`. Every attribute deletion passes through it, giving you a single choke point to block protected attributes, log deletions, or cascade cleanup. Like `__setattr__`, always call `super().__delattr__(name)` for attributes you do want to actually remove -- otherwise the deletion never happens.

## Fundamentals

### 1. Definition

The `__delattr__` method is called **whenever you delete an attribute** on an object:

```python
del obj.attr  # Triggers obj.__delattr__('attr')
delattr(obj, 'attr')  # Also triggers __delattr__
```

### 2. Method Signature

```python
def __delattr__(self, name):
    # name: attribute name to delete (string)
    pass
```

### 3. Universal Deletion Hook

Every attribute deletion goes through `__delattr__`:

```python
del self.x      # Calls __delattr__('x')
del self.name   # Calls __delattr__('name')
del self.data   # Calls __delattr__('data')
```

!!! note "Attribute Operations Symmetry"

    `__delattr__` completes the three-operation system for attribute mutation:

    ```text
    obj.attr        → __getattribute__  (read)
    obj.attr = val  → __setattr__       (write)
    del obj.attr    → __delattr__        (delete)
    ```

    Like `__setattr__`, `__delattr__` runs unconditionally for every deletion — there is no "fallback" variant. Together, these three hooks give you complete control over the attribute lifecycle. Override only the hooks you need; the defaults (inherited from `object`) handle the common cases correctly.

## Basic Implementation

### 1. Simple Override

```python
class MyClass:
    def __init__(self):
        self.x = 42
        self.y = 100
    
    def __delattr__(self, name):
        print(f"Deleting attribute: {name}")
        super().__delattr__(name)

obj = MyClass()
del obj.x
# Output: Deleting attribute: x

print(hasattr(obj, 'x'))  # False
```

### 2. Without super()

```python
class MyClass:
    def __delattr__(self, name):
        print(f"Deleting {name}")
        object.__delattr__(self, name)
```

### 3. Must Actually Delete

```python
# ❌ BAD - doesn't actually delete
def __delattr__(self, name):
    print(f"Deleting {name}")
    # Forgot to actually delete it!

# ✅ GOOD
def __delattr__(self, name):
    print(f"Deleting {name}")
    super().__delattr__(name)
```

## Preventing Deletion

### 1. Protecting Attributes

```python
class ProtectedAttributes:
    def __init__(self):
        self.id = 123
        self.name = "Alice"
        self.value = 42
    
    def __delattr__(self, name):
        if name == 'id':
            raise AttributeError("Cannot delete 'id' attribute")
        super().__delattr__(name)

obj = ProtectedAttributes()
del obj.name    # ✅ OK
del obj.value   # ✅ OK
# del obj.id    # ❌ AttributeError
```

### 2. Read-Only Class

```python
class ImmutableAfterInit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._initialized = True
    
    def __delattr__(self, name):
        if hasattr(self, '_initialized'):
            raise AttributeError("Cannot delete attributes after initialization")
        super().__delattr__(name)

obj = ImmutableAfterInit(10, 20)
# del obj.x  # ❌ AttributeError
```

### 3. Conditional Protection

```python
class Document:
    def __init__(self):
        self._locked = False
        self.content = "Draft"
    
    def lock(self):
        self._locked = True
    
    def __delattr__(self, name):
        if self._locked and name != '_locked':
            raise AttributeError("Document is locked")
        super().__delattr__(name)

doc = Document()
del doc.content  # ✅ OK (before lock)
doc.lock()
# del doc.content  # ❌ AttributeError (after lock)
```

## Cleanup Actions

### 1. Resource Cleanup

```python
class DatabaseConnection:
    def __init__(self):
        self.connection = self._create_connection()
    
    def _create_connection(self):
        print("Opening database connection")
        return {"status": "connected"}
    
    def __delattr__(self, name):
        if name == 'connection':
            print("Closing database connection")
            # Cleanup code here
            self.connection['status'] = 'closed'
        super().__delattr__(name)

obj = DatabaseConnection()
del obj.connection
# Output: Closing database connection
```

### 2. Cascade Deletion

!!! warning "Risk of unintended side effects"
    Cascade deletion can silently destroy attributes the caller did not intend to
    remove. Use this pattern only when the relationship between attributes is
    well-documented and callers expect the cascade. Prefer explicit cleanup methods
    (e.g., `obj.reset()`) over implicit magic in `__delattr__`.

```python
class Parent:
    def __init__(self):
        self.child1 = "value1"
        self.child2 = "value2"
        self.child3 = "value3"
    
    def __delattr__(self, name):
        if name == 'child1':
            # Cascade delete related attributes
            print("Cascading deletion of related attributes")
            if hasattr(self, 'child2'):
                super().__delattr__('child2')
            if hasattr(self, 'child3'):
                super().__delattr__('child3')
        super().__delattr__(name)

obj = Parent()
del obj.child1
# Deletes child1, child2, and child3
```

### 3. Logging Deletions

```python
from datetime import datetime

class AuditedDeletion:
    def __init__(self):
        self._deletion_log = []
        self.value = 42
    
    def __delattr__(self, name):
        if name != '_deletion_log':
            self._deletion_log.append({
                'attr': name,
                'time': datetime.now()
            })
        super().__delattr__(name)

obj = AuditedDeletion()
del obj.value
print(obj._deletion_log)
# [{'attr': 'value', 'time': datetime(...)}]
```

## Interaction with Properties

### 1. Properties with Deleters

```python
class Example:
    def __init__(self):
        self._value = 42
    
    @property
    def value(self):
        return self._value
    
    @value.deleter
    def value(self):
        print("Property deleter called")
        del self._value
    
    def __delattr__(self, name):
        print(f"__delattr__: {name}")
        super().__delattr__(name)

obj = Example()
del obj.value
# Output:
# __delattr__: value
# Property deleter called
# __delattr__: _value
```

### 2. Call Order

```python
del obj.value
    ↓
__delattr__('value') called
    ↓
super().__delattr__('value')
    ↓
Finds property descriptor in class
    ↓
Calls property's __delete__ method
    ↓
Inside deleter: del self._value
    ↓
__delattr__('_value') called again
```

### 3. Bypassing Property Deleter

```python
def __delattr__(self, name):
    if name == 'special':
        # Bypass property deleter
        del self.__dict__[name]
    else:
        super().__delattr__(name)
```

## Practical Examples

### 1. Cache Invalidation

```python
class CachedComputation:
    def __init__(self):
        self.data = [1, 2, 3, 4, 5]
        self._cache = {}
    
    @property
    def sum_cached(self):
        if 'sum' not in self._cache:
            self._cache['sum'] = sum(self.data)
        return self._cache['sum']
    
    def __delattr__(self, name):
        if name == 'data':
            # Invalidate cache when data is deleted
            self._cache.clear()
        super().__delattr__(name)

obj = CachedComputation()
print(obj.sum_cached)  # 15
del obj.data
# Cache is cleared
```

### 2. Dependency Management

```python
class ConfigManager:
    def __init__(self):
        self.database_host = "localhost"
        self.database_port = 5432
        self._connection = None
    
    def __delattr__(self, name):
        if name in ('database_host', 'database_port'):
            # Close connection when config changes
            if self._connection:
                print("Closing connection due to config change")
                self._connection = None
        super().__delattr__(name)

config = ConfigManager()
del config.database_host
# Output: Closing connection due to config change
```

### 3. Notification System

```python
class Observable:
    def __init__(self):
        self._observers = []
        self.value = 42
    
    def attach(self, observer):
        self._observers.append(observer)
    
    def __delattr__(self, name):
        if name not in ('_observers',):
            # Notify observers
            for observer in self._observers:
                observer.on_delete(name)
        super().__delattr__(name)

class Observer:
    def on_delete(self, attr_name):
        print(f"Attribute {attr_name} was deleted")

obj = Observable()
obs = Observer()
obj.attach(obs)
del obj.value
# Output: Attribute value was deleted
```

## Error Handling

### 1. Checking Existence

```python
class SafeDelete:
    def __delattr__(self, name):
        if not hasattr(self, name):
            raise AttributeError(f"Attribute '{name}' does not exist")
        super().__delattr__(name)

obj = SafeDelete()
obj.x = 10
del obj.x       # ✅ OK
# del obj.x     # ❌ AttributeError (already deleted)
```

### 2. Custom Error Messages

```python
class InformativeErrors:
    def __delattr__(self, name):
        protected = ['id', '_internal']
        if name in protected:
            raise AttributeError(
                f"Cannot delete protected attribute '{name}'. "
                f"Protected attributes: {protected}"
            )
        if not hasattr(self, name):
            available = [k for k in self.__dict__ if not k.startswith('_')]
            raise AttributeError(
                f"Attribute '{name}' not found. "
                f"Available attributes: {available}"
            )
        super().__delattr__(name)
```

### 3. Graceful Degradation

```python
class GracefulDelete:
    def __delattr__(self, name):
        try:
            super().__delattr__(name)
        except AttributeError:
            print(f"Warning: Could not delete '{name}' (not found)")
            # Don't raise, just warn
```

## Advanced Patterns

### 1. Soft Delete

!!! warning "Breaks caller expectations"
    Soft delete makes `del obj.attr` appear to work while secretly keeping the data.
    This violates the principle of least surprise — code that checks `hasattr()` or
    catches `AttributeError` after deletion may behave incorrectly. Reserve this
    pattern for audit/compliance scenarios where data retention is an explicit
    requirement, and document the behavior prominently.

```python
class SoftDelete:
    def __init__(self):
        self._deleted = set()
        self.value = 42
    
    def __delattr__(self, name):
        # Don't actually delete, just mark as deleted
        if name != '_deleted':
            self._deleted.add(name)
    
    def __getattribute__(self, name):
        deleted = object.__getattribute__(self, '_deleted')
        if name in deleted:
            raise AttributeError(f"Attribute '{name}' has been deleted")
        return super().__getattribute__(name)

obj = SoftDelete()
del obj.value
# print(obj.value)  # ❌ AttributeError (appears deleted)
print(obj.__dict__)  # {'_deleted': {'value'}, 'value': 42}
```

### 2. Undo Functionality

```python
class UndoableDelete:
    def __init__(self):
        self._deleted_attrs = {}
        self.value = 42
    
    def __delattr__(self, name):
        if name != '_deleted_attrs':
            # Save value before deleting
            self._deleted_attrs[name] = getattr(self, name)
        super().__delattr__(name)
    
    def undo_delete(self, name):
        if name in self._deleted_attrs:
            setattr(self, name, self._deleted_attrs[name])
            del self._deleted_attrs[name]

obj = UndoableDelete()
del obj.value
obj.undo_delete('value')
print(obj.value)  # 42 (restored)
```

### 3. Reference Counting

```python
class RefCounted:
    _ref_counts = {}
    
    def __setattr__(self, name, value):
        if name not in ('_ref_counts',):
            RefCounted._ref_counts[name] = RefCounted._ref_counts.get(name, 0) + 1
        super().__setattr__(name, value)
    
    def __delattr__(self, name):
        if name in RefCounted._ref_counts:
            RefCounted._ref_counts[name] -= 1
            if RefCounted._ref_counts[name] == 0:
                print(f"Last reference to '{name}' deleted")
        super().__delattr__(name)
```

## When NOT to Use __delattr__

!!! warning "Avoid When"
    - **Controlling deletion of a specific named attribute** — use a `@property` deleter instead. It is self-contained and easier to understand.
    - **The default behavior is sufficient** — if you just want `del obj.attr` to remove the attribute from `__dict__`, you don't need to override anything.
    - **You are tempted to add cascade deletes** — prefer an explicit `reset()` or `clear()` method that makes the intent visible to the caller.

    Override `__delattr__` only when you need a **blanket policy** (protect all underscore attributes, audit all deletions, enforce immutability across the board).

## Common Mistakes

### 1. Not Actually Deleting

```python
# ❌ BAD - logs but doesn't delete
def __delattr__(self, name):
    print(f"Deleting {name}")
    # Forgot to call super().__delattr__!

# ✅ GOOD
def __delattr__(self, name):
    print(f"Deleting {name}")
    super().__delattr__(name)
```

### 2. Deleting Non-Existent Attributes

```python
# ❌ BAD - assumes attribute exists
def __delattr__(self, name):
    value = self.__dict__[name]  # KeyError if not exists!
    super().__delattr__(name)

# ✅ GOOD
def __delattr__(self, name):
    if hasattr(self, name):
        super().__delattr__(name)
```

### 3. Circular Dependencies

```python
# ❌ BAD
def __delattr__(self, name):
    if name == 'x':
        del self.y  # If y's deletion tries to delete x... infinite loop!
    super().__delattr__(name)
```

---

## Exercises

**Exercise 1.**
Create a class `ProtectedAttributes` that prevents deletion of attributes whose names start with an underscore. Override `__delattr__` to raise `AttributeError` for protected attributes while allowing deletion of others. Demonstrate both cases.

??? success "Solution to Exercise 1"

        class ProtectedAttributes:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    object.__setattr__(self, k, v)

            def __delattr__(self, name):
                if name.startswith("_"):
                    raise AttributeError(f"Cannot delete protected attribute '{name}'")
                super().__delattr__(name)

        obj = ProtectedAttributes(_secret="hidden", public="visible")

        del obj.public  # Works
        try:
            del obj._secret
        except AttributeError as e:
            print(f"Error: {e}")
            # Error: Cannot delete protected attribute '_secret'

---

**Exercise 2.**
Write a class `AuditLog` where `__delattr__` logs every attribute deletion (printing the attribute name and its value before deletion) and then proceeds with the deletion using `super().__delattr__()`. Show the audit output for several deletions.

??? success "Solution to Exercise 2"

        class AuditLog:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    object.__setattr__(self, k, v)

            def __delattr__(self, name):
                value = getattr(self, name, "<not found>")
                print(f"AUDIT: Deleting '{name}' (was: {value!r})")
                super().__delattr__(name)

        obj = AuditLog(x=10, y="hello", z=[1, 2, 3])
        del obj.x  # AUDIT: Deleting 'x' (was: 10)
        del obj.y  # AUDIT: Deleting 'y' (was: 'hello')

---

**Exercise 3.**
Build a class `Immutable` where `__delattr__` always raises `AttributeError` with the message "Cannot delete attributes from immutable object". Set attributes in `__init__` using `object.__setattr__`. Show that attributes exist and can be read but never deleted.

??? success "Solution to Exercise 3"

        class Immutable:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    object.__setattr__(self, k, v)

            def __delattr__(self, name):
                raise AttributeError("Cannot delete attributes from immutable object")

            def __setattr__(self, name, value):
                raise AttributeError("Cannot modify attributes of immutable object")

        obj = Immutable(x=10, y=20)
        print(obj.x)  # 10
        print(obj.y)  # 20

        try:
            del obj.x
        except AttributeError as e:
            print(f"Error: {e}")
            # Error: Cannot delete attributes from immutable object

---

**Exercise 4.**
Explain why you would use a `@property` deleter instead of `__delattr__` for controlling deletion of a single attribute. Implement a `User` class with a `session` property that, when deleted, also prints a logout message. Then show what the equivalent `__delattr__` implementation would look like and explain why the property version is simpler.

??? success "Solution to Exercise 4"

        # Property deleter — simple, self-contained
        class UserProperty:
            def __init__(self, name):
                self.name = name
                self._session = None

            @property
            def session(self):
                return self._session

            @session.setter
            def session(self, value):
                self._session = value

            @session.deleter
            def session(self):
                print(f"Logging out {self.name}")
                self._session = None

        u = UserProperty("Alice")
        u.session = "token_abc"
        del u.session  # Logging out Alice

        # __delattr__ equivalent — more complex
        class UserDelattr:
            def __init__(self, name):
                self.name = name
                self._session = None

            def __delattr__(self, name):
                if name == "session":
                    print(f"Logging out {self.name}")
                    object.__setattr__(self, '_session', None)
                    return  # Don't actually delete the property
                super().__delattr__(name)

    The property version is simpler because: (1) the logic is co-located with the getter and setter, (2) no risk of accidentally affecting other attribute deletions, and (3) no need to handle the asymmetry between `session` (the property name) and `_session` (the backing attribute). `__delattr__` is the right tool when you need a blanket policy across many attributes.

---

**Exercise 5.**
Build a `ResourceManager` class that holds `connection`, `cache`, and `logger` attributes. Override `__delattr__` so that deleting any of these three prints a cleanup message and calls a corresponding private `_close_*` method before deletion. Deleting any other attribute should work normally. Demonstrate deleting each resource.

??? success "Solution to Exercise 5"

        class ResourceManager:
            def __init__(self):
                self.connection = "db://localhost"
                self.cache = {"key": "value"}
                self.logger = "file_logger"
                self.name = "manager_1"  # Non-resource attribute

            def _close_connection(self):
                print(f"  Closing connection: {self.connection}")

            def _close_cache(self):
                print(f"  Clearing cache: {len(self.cache)} entries")

            def _close_logger(self):
                print(f"  Shutting down logger: {self.logger}")

            def __delattr__(self, name):
                cleanups = {
                    "connection": self._close_connection,
                    "cache": self._close_cache,
                    "logger": self._close_logger,
                }
                if name in cleanups:
                    print(f"Cleaning up '{name}':")
                    cleanups[name]()
                super().__delattr__(name)

        rm = ResourceManager()

        del rm.connection
        # Cleaning up 'connection':
        #   Closing connection: db://localhost

        del rm.cache
        # Cleaning up 'cache':
        #   Clearing cache: 1 entries

        del rm.name  # No cleanup — just deleted normally

        print(hasattr(rm, "connection"))  # False
        print(hasattr(rm, "name"))        # False
        print(hasattr(rm, "logger"))      # True — not deleted yet
