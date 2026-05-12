# \_\_init_subclass\_\_

`__init_subclass__` (Python 3.6+) is a hook that runs whenever a class is subclassed. It provides a simpler alternative to metaclasses for many common use cases — but it has hard limits.

!!! tip "Mental Model"
    `__init_subclass__` is a parent class's callback that fires every time someone writes `class Child(Parent)`. Think of it as a registration desk: the parent inspects each new child at birth, can enforce rules (require certain methods), inject behavior (auto-register plugins), or reject the child entirely. It covers 80% of metaclass use cases with none of the complexity.

!!! warning "Hard Limits — what `__init_subclass__` cannot do"
    `__init_subclass__` runs **after** the class object already exists. It cannot:

    - Modify the class namespace **before** creation (use `__prepare__` in a metaclass)
    - Affect method resolution order (MRO)
    - Intercept or control **instance** creation (use `__call__` in a metaclass)

    ```text
    class statement → metaclass.__new__ → class object exists → __init_subclass__
    ```

    If you need to act *before* the class is fully formed, you need a metaclass.

!!! tip "The `super()` rule"
    Always call `super().__init_subclass__(**kwargs)` in your implementation. This
    ensures cooperative multiple inheritance works correctly — without it, sibling
    hooks in the MRO chain will be silently skipped.

```python
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Called when any class inherits from Base
```

---

## Basic Usage

```python
class Plugin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"New plugin registered: {cls.__name__}")

class AudioPlugin(Plugin):
    pass
# Output: New plugin registered: AudioPlugin

class VideoPlugin(Plugin):
    pass
# Output: New plugin registered: VideoPlugin
```

---

## How It Works

When you define a subclass:

```python
class Child(Parent):
    pass
```

Python automatically calls:

```python
Parent.__init_subclass__(Child)
```

The hook receives:

- `cls`: The newly created subclass (not the parent)
- `**kwargs`: Any keyword arguments from the class definition

---

## Passing Arguments

You can pass arguments in the class definition:

```python
class Serializable:
    def __init_subclass__(cls, format="json", **kwargs):
        super().__init_subclass__(**kwargs)
        cls._format = format
        print(f"{cls.__name__} uses {format} format")

class User(Serializable, format="xml"):
    pass
# Output: User uses xml format

class Product(Serializable):  # Uses default
    pass
# Output: Product uses json format

print(User._format)     # xml
print(Product._format)  # json
```

---

## Practical Examples

### Plugin Registration

```python
class Plugin:
    _registry = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # Register plugin by name
        Plugin._registry[cls.__name__] = cls
    
    @classmethod
    def get_plugin(cls, name):
        return cls._registry.get(name)

class ImageProcessor(Plugin):
    def process(self, data):
        return f"Processing image: {data}"

class TextProcessor(Plugin):
    def process(self, data):
        return f"Processing text: {data}"

# Access registered plugins
print(Plugin._registry)
# {'ImageProcessor': <class 'ImageProcessor'>, 'TextProcessor': <class 'TextProcessor'>}

processor = Plugin.get_plugin("ImageProcessor")()
print(processor.process("photo.jpg"))
```

### Validation

```python
class ValidatedModel:
    required_fields = []
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # Check that required fields are defined
        for field in cls.required_fields:
            if not hasattr(cls, field):
                raise TypeError(
                    f"{cls.__name__} must define '{field}'"
                )

class UserModel(ValidatedModel):
    required_fields = ['name', 'email']
    name = str
    email = str
    # ✓ Valid - has both required fields

# class InvalidModel(ValidatedModel):
#     required_fields = ['name', 'email']
#     name = str
#     # TypeError: InvalidModel must define 'email'
```

### Automatic Method Addition

!!! note "Illustrative example — not production-safe"
    The `AutoRepr` pattern below inspects `__init__` parameters via `inspect.signature`.
    This breaks with inheritance (picks up the wrong `__init__`), does not handle
    `*args`/`**kwargs`, and ignores dataclasses, slots, and descriptors. For production
    use, prefer `@dataclass` (which generates `__repr__` correctly) or write an explicit
    `__repr__`.

```python
class AutoRepr:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # Add __repr__ based on __init__ parameters
        if hasattr(cls, '__init__'):
            import inspect
            sig = inspect.signature(cls.__init__)
            params = [p for p in sig.parameters if p != 'self']
            
            def __repr__(self):
                values = ', '.join(
                    f"{p}={getattr(self, p)!r}" 
                    for p in params 
                    if hasattr(self, p)
                )
                return f"{self.__class__.__name__}({values})"
            
            cls.__repr__ = __repr__

class Person(AutoRepr):
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(p)  # Person(name='Alice', age=30)
```

### Configuration Inheritance

```python
class Configurable:
    _config = {}
    
    def __init_subclass__(cls, **config):
        super().__init_subclass__()
        # Inherit parent config and update with new values
        cls._config = {**cls._config, **config}

class BaseService(Configurable, timeout=30, retries=3):
    pass

class DatabaseService(BaseService, timeout=60):
    pass

class CacheService(BaseService, retries=5):
    pass

print(BaseService._config)     # {'timeout': 30, 'retries': 3}
print(DatabaseService._config) # {'timeout': 60, 'retries': 3}
print(CacheService._config)    # {'timeout': 30, 'retries': 5}
```

### Enforcing Abstract Methods

```python
class Interface:
    _required_methods = []
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        
        # Skip abstract classes
        if getattr(cls, '_abstract', False):
            return
        
        # Check all required methods are implemented
        missing = []
        for method in cls._required_methods:
            if not callable(getattr(cls, method, None)):
                missing.append(method)
        
        if missing:
            raise TypeError(
                f"{cls.__name__} must implement: {', '.join(missing)}"
            )

class Repository(Interface):
    _abstract = True
    _required_methods = ['get', 'save', 'delete']

class UserRepository(Repository):
    def get(self, id):
        return {"id": id}
    
    def save(self, entity):
        pass
    
    def delete(self, id):
        pass
# ✓ Valid

# class BadRepository(Repository):
#     def get(self, id):
#         return {"id": id}
# TypeError: BadRepository must implement: save, delete
```

---

## With Multiple Inheritance

```python
class A:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"A.__init_subclass__ for {cls.__name__}")

class B:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"B.__init_subclass__ for {cls.__name__}")

class C(A, B):
    pass
# Output:
# B.__init_subclass__ for C
# A.__init_subclass__ for C
```

Note how the MRO determines the order: `B.__init_subclass__` runs before
`A.__init_subclass__` because Python traverses the MRO from right to left when
calling cooperative `super()` chains.

---

## __init_subclass__ vs Metaclass

| Feature | `__init_subclass__` | Metaclass |
|---------|---------------------|-----------|
| Complexity | Simple | Complex |
| Called when | Class is subclassed | Class is created |
| Access to | Subclass only | Full creation process |
| Modify namespace | No | Yes (via `__prepare__`) |
| Control instantiation | No | Yes (via `__call__`) |
| Use case | Registration, validation | DSLs, ORMs |

!!! tip "Decision Rule"

    Use `__init_subclass__` when you only need the **finished class** — registration,
    validation, adding attributes. Use a metaclass when you need to control **how the
    class is built** — custom namespace (`__prepare__`), intercepting instance creation
    (`__call__`), or transforming the class body before the class object exists.

### When to Use __init_subclass__

- Registering subclasses
- Validating class definitions
- Adding methods or attributes
- Simple class customization

### When to Use Metaclass

- Modifying class before creation
- Controlling instance creation
- Custom namespace handling
- Complex framework behavior

---

## Common Patterns

### Optional Hook

```python
class OptionalHook:
    def __init_subclass__(cls, register=True, **kwargs):
        super().__init_subclass__(**kwargs)
        if register:
            cls._registered = True
        else:
            cls._registered = False

class Registered(OptionalHook):
    pass

class NotRegistered(OptionalHook, register=False):
    pass

print(Registered._registered)     # True
print(NotRegistered._registered)  # False
```

### Chained Hooks

```python
class Logger:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"[LOG] Created: {cls.__name__}")

class Validator:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        print(f"[VALIDATE] Checking: {cls.__name__}")

class MyClass(Logger, Validator):
    pass
# [VALIDATE] Checking: MyClass
# [LOG] Created: MyClass
```

---

## Summary

| Feature | Example |
|---------|---------|
| Basic hook | `def __init_subclass__(cls, **kwargs):` |
| With arguments | `class Child(Parent, arg=value):` |
| Always call super | `super().__init_subclass__(**kwargs)` |
| Access subclass | `cls` parameter |

**Key Takeaways**:

- `__init_subclass__` is called when a class is subclassed
- Simpler alternative to metaclasses for many use cases
- Always call `super().__init_subclass__(**kwargs)`
- Can receive keyword arguments from class definition
- Use for registration, validation, and automatic setup
- Prefer over metaclasses unless you need `__prepare__` or `__call__`

---

## Runnable Example: `singleton_metaclass_example.py`

```python
"""
Metaclass Example: Thread-Safe Singleton

A metaclass is a "class of a class" - it controls how classes
are created and how instances are constructed.

This tutorial implements a singleton pattern using a metaclass,
where __call__ on the metaclass intercepts instance creation.

Topics covered:
- Custom metaclass (inheriting from type)
- __init__ on metaclass (called when class is defined)
- __call__ on metaclass (called when class() is invoked)
- Thread-safe double-checked locking
- Comparison with decorator approach

Based on concepts from Python-100-Days example18 and ch06/metaclasses materials.
"""

import threading


# =============================================================================
# Example 1: Singleton Metaclass
# =============================================================================

class SingletonMeta(type):
    """Metaclass that makes any class using it a singleton.

    How it works:
    1. When the class is DEFINED (class Foo(metaclass=SingletonMeta):),
       SingletonMeta.__init__ runs, initializing _instance and _lock.
    2. When Foo() is CALLED to create an instance,
       SingletonMeta.__call__ runs instead of the normal type.__call__.
    3. __call__ checks if an instance already exists (thread-safely).
    """

    def __init__(cls, *args, **kwargs):
        """Called when the class is first defined (not when instantiated)."""
        cls._instance = None
        cls._lock = threading.Lock()
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        """Called every time cls() is invoked (instead of creating new instance).

        Uses double-checked locking for thread safety:
        1. Fast check without lock (avoids lock overhead after first creation)
        2. Acquire lock and check again (prevents race condition)
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


# =============================================================================
# Example 2: Using the Singleton Metaclass
# =============================================================================

class DatabaseConnection(metaclass=SingletonMeta):
    """Database connection that should only exist once.

    Using metaclass=SingletonMeta ensures that DatabaseConnection()
    always returns the same instance.
    """

    def __init__(self, host: str = "localhost", port: int = 5432):
        self.host = host
        self.port = port
        self.connected = True

    def __str__(self):
        return f"DB({self.host}:{self.port})"


class AppLogger(metaclass=SingletonMeta):
    """Application logger (separate singleton from DatabaseConnection)."""

    def __init__(self, name: str = "app"):
        self.name = name
        self.entries: list[str] = []

    def log(self, message: str):
        self.entries.append(message)

    def __str__(self):
        return f"Logger('{self.name}', {len(self.entries)} entries)"


# =============================================================================
# Example 3: Demonstrating Singleton Behavior
# =============================================================================

def demo_singleton():
    """Show that the metaclass enforces singleton behavior."""
    print("=== Singleton Metaclass Demo ===")

    # First call creates the instance
    db1 = DatabaseConnection("postgres.example.com", 5432)
    # Second call returns the SAME instance (args ignored)
    db2 = DatabaseConnection("mysql.example.com", 3306)
    # Even __call__ returns the same instance
    db3 = DatabaseConnection.__call__("oracle.example.com", 1521)

    print(f"db1: {db1}")
    print(f"db2: {db2}")
    print(f"db3: {db3}")
    print(f"db1 is db2: {db1 is db2}")
    print(f"db1 is db3: {db1 is db3}")
    print()

    # Different classes have independent singletons
    logger = AppLogger("main")
    print(f"logger: {logger}")
    print(f"logger is db1: {logger is db1}")
    print()


# =============================================================================
# Example 4: isinstance() Works (Unlike Decorator Approach)
# =============================================================================

def demo_isinstance():
    """Show that isinstance works correctly with metaclass singleton."""
    print("=== isinstance() Works Correctly ===")

    db = DatabaseConnection()

    print(f"isinstance(db, DatabaseConnection): {isinstance(db, DatabaseConnection)}")
    print(f"type(db): {type(db).__name__}")
    print(f"type(DatabaseConnection): {type(DatabaseConnection).__name__}")
    print()

    print("Note: With a decorator singleton, isinstance() would fail")
    print("because the decorator replaces the class with a function.")
    print("The metaclass approach preserves the class identity.")
    print()


# =============================================================================
# Example 5: The Metaclass Chain
# =============================================================================

def demo_metaclass_chain():
    """Visualize the metaclass relationship."""
    print("=== Metaclass Chain ===")
    print("""
    Normal chain:    instance -> class -> type (default metaclass)
    Singleton chain: instance -> class -> SingletonMeta -> type

    The chain:
    - db = DatabaseConnection()     # db is an instance
    - type(db) is DatabaseConnection  # class of db
    - type(DatabaseConnection) is SingletonMeta  # metaclass
    - type(SingletonMeta) is type     # meta-metaclass (always type)
    """)

    db = DatabaseConnection()
    print(f"Instance:  {db}")
    print(f"Class:     {type(db).__name__}")
    print(f"Metaclass: {type(type(db)).__name__}")
    print(f"Meta-meta: {type(type(type(db))).__name__}")


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    demo_singleton()
    demo_isinstance()
    demo_metaclass_chain()
```

---

## Exercises

**Exercise 1.**
Create a base class `Plugin` that uses `__init_subclass__` to automatically register all subclasses into a class-level `_registry` dictionary (mapping the class name to the class). Create three plugin subclasses and print the registry without any manual registration code.

??? success "Solution to Exercise 1"

        class Plugin:
            _registry = {}

            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__(**kwargs)
                Plugin._registry[cls.__name__] = cls

        class AuthPlugin(Plugin):
            pass

        class CachePlugin(Plugin):
            pass

        class LogPlugin(Plugin):
            pass

        print(Plugin._registry)
        # {'AuthPlugin': <class 'AuthPlugin'>, 'CachePlugin': ..., 'LogPlugin': ...}

---

**Exercise 2.**
Write a base class `ValidatedModel` where `__init_subclass__` checks that every subclass defines a `required_fields` class attribute (a list of strings). If missing, raise `TypeError`. Create a valid subclass and an invalid one to demonstrate the validation.

??? success "Solution to Exercise 2"

        class ValidatedModel:
            def __init_subclass__(cls, **kwargs):
                super().__init_subclass__(**kwargs)
                if not hasattr(cls, 'required_fields'):
                    raise TypeError(f"{cls.__name__} must define 'required_fields'")

        class User(ValidatedModel):
            required_fields = ["name", "email"]

        print(User.required_fields)  # ['name', 'email']

        try:
            class BadModel(ValidatedModel):
                pass  # Missing required_fields
        except TypeError as e:
            print(f"Error: {e}")
            # Error: BadModel must define 'required_fields'

---

**Exercise 3.**
Build a `Serializable` base class where `__init_subclass__` accepts a `format` keyword argument (e.g., `class MyData(Serializable, format="json")`). Store the format on the subclass as `_format`. Add a `serialize()` method that prints the format. Show that different subclasses can declare different formats.

??? success "Solution to Exercise 3"

        class Serializable:
            def __init_subclass__(cls, format="text", **kwargs):
                super().__init_subclass__(**kwargs)
                cls._format = format

            def serialize(self):
                print(f"Serializing {self.__class__.__name__} as {self._format}")

        class JsonData(Serializable, format="json"):
            pass

        class XmlData(Serializable, format="xml"):
            pass

        class PlainData(Serializable):  # Uses default "text"
            pass

        JsonData().serialize()   # Serializing JsonData as json
        XmlData().serialize()    # Serializing XmlData as xml
        PlainData().serialize()  # Serializing PlainData as text
