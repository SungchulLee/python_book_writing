# Metaclasses Introduction

A metaclass is a class whose instances are classes. Just as a class defines how instances behave, a metaclass defines how classes behave. Every class in Python is created by a metaclass — if you don't specify one, Python uses `type` as the default. You are always using a metaclass, even when you don't say so explicitly.

!!! note "Mental Model"
    A metaclass is a **class factory + behavior controller**. It builds the class
    object (via `__new__`), initializes it (via `__init__`), and controls how that
    class creates its own instances (via `__call__`).

    ```text
    Metaclass → builds classes
    Class     → builds instances
    ABC       → constrains class design
    ```

    A metaclass is **not** responsible for constructing instances — that is the class's job. The metaclass constructs the class itself.

---

## Understanding the Concept

### Everything is an Object

In Python, **classes are objects too**:

```python
class MyClass:
    pass

# MyClass is an object
print(type(MyClass))  # <class 'type'>

# Just like instances are objects
obj = MyClass()
print(type(obj))      # <class '__main__.MyClass'>
```

### The type() Function

`type` has two uses:

```python
# 1. Get the type of an object
print(type(42))        # <class 'int'>
print(type("hello"))   # <class 'str'>
print(type([1, 2]))    # <class 'list'>

# 2. Create a new class dynamically
MyClass = type('MyClass', (), {'x': 10})
print(MyClass.x)       # 10
```

### type is the Default Metaclass

```python
class MyClass:
    pass

# These are equivalent:
# 1. Using class statement
class MyClass:
    x = 10

# 2. Using type() directly
MyClass = type('MyClass', (), {'x': 10})
```

---

## The Class Creation Process

When Python sees a class definition:

```python
class MyClass(BaseClass):
    x = 10
    def method(self):
        pass
```

It executes roughly:

```python
# 1. Collect class body into a namespace dict
namespace = {'x': 10, 'method': method_function}

# 2. Determine metaclass (default: type)
metaclass = type

# 3. Call metaclass to create class
MyClass = metaclass('MyClass', (BaseClass,), namespace)
```

---

## Creating a Metaclass

### Basic Metaclass

```python
class MyMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class: {name}")
        # Create the class using type.__new__
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

class MyClass(metaclass=MyMeta):
    pass
# Output: Creating class: MyClass
```

### __new__ vs __init__ in Metaclass

The key difference: `__new__` can **replace** the class object entirely (by returning
a different object), while `__init__` receives the already-created class and can only
modify it in place. Use `__new__` when you need to intercept or transform the class
before it exists; use `__init__` for post-creation setup.

```python
class MyMeta(type):
    def __new__(mcs, name, bases, namespace):
        """Called to CREATE the class object.
        Can modify namespace or return a completely different class."""
        print(f"__new__: Creating {name}")
        return super().__new__(mcs, name, bases, namespace)
    
    def __init__(cls, name, bases, namespace):
        """Called to INITIALIZE the class object.
        The class already exists — can only modify it, not replace it."""
        print(f"__init__: Initializing {name}")
        super().__init__(name, bases, namespace)

class MyClass(metaclass=MyMeta):
    pass
# __new__: Creating MyClass
# __init__: Initializing MyClass
```

### __call__ in Metaclass

Controls instance creation:

```python
class SingletonMeta(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """Called when MyClass() is invoked."""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    pass

a = Singleton()
b = Singleton()
print(a is b)  # True
```

!!! warning "Singleton caveat: first initialization wins"
    After the first instance is created, all subsequent calls return that same
    instance — **any new arguments are silently ignored**. This can hide bugs:

    ```python
    db1 = Database("postgres")  # Creates instance with postgres
    db2 = Database("mysql")     # Returns db1 — "mysql" is ignored!
    print(db2.url)              # "postgres"
    ```

    Document this behavior clearly, or raise an error on re-initialization.

---

## Practical Examples

### Automatic Registration

```python
class PluginMeta(type):
    plugins = {}
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # Don't register the base class itself
        if bases:  # Has parent classes
            mcs.plugins[name] = cls
        return cls

class Plugin(metaclass=PluginMeta):
    """Base class for plugins."""
    pass

class AudioPlugin(Plugin):
    pass

class VideoPlugin(Plugin):
    pass

print(PluginMeta.plugins)
# {'AudioPlugin': <class 'AudioPlugin'>, 'VideoPlugin': <class 'VideoPlugin'>}
```

### Attribute Validation

```python
class ValidatedMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Check that required attributes exist
        if bases:  # Not the base class
            if 'required_field' not in namespace:
                raise TypeError(f"{name} must define 'required_field'")
        return super().__new__(mcs, name, bases, namespace)

class Base(metaclass=ValidatedMeta):
    pass

class Valid(Base):
    required_field = "I exist"

# class Invalid(Base):  # TypeError: Invalid must define 'required_field'
#     pass
```

### Method Wrapping

```python
import functools

class LoggedMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Wrap all methods with logging
        for key, value in namespace.items():
            if callable(value) and not key.startswith('_'):
                namespace[key] = mcs.log_call(value)
        return super().__new__(mcs, name, bases, namespace)
    
    @staticmethod
    def log_call(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper

class MyClass(metaclass=LoggedMeta):
    def method1(self):
        return "result1"
    
    def method2(self, x):
        return x * 2

obj = MyClass()
obj.method1()  # Calling method1
obj.method2(5) # Calling method2
```

### Interface Enforcement

```python
class InterfaceMeta(type):
    required_methods = []
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        
        # Skip check for base class
        if bases and mcs.required_methods:
            for method in mcs.required_methods:
                if method not in namespace:
                    raise TypeError(
                        f"{name} must implement {method}()"
                    )
        return cls

class ServiceMeta(InterfaceMeta):
    required_methods = ['start', 'stop', 'status']

class Service(metaclass=ServiceMeta):
    """Base service class."""
    def start(self): pass
    def stop(self): pass
    def status(self): pass

class DatabaseService(Service):
    def start(self):
        print("DB starting")
    
    def stop(self):
        print("DB stopping")
    
    def status(self):
        return "running"
```

---

## Metaclass vs Alternatives

### When NOT to Use Metaclasses

Most use cases have simpler alternatives:

| Need | Alternative |
|------|-------------|
| Modify class creation | `__init_subclass__` |
| Add methods | Class decorators |
| Validate attributes | Descriptors |
| Singleton pattern | Module-level instance |
| Registration | Class decorators |

### __init_subclass__ (Python 3.6+)

Simpler alternative for many cases:

```python
class Plugin:
    plugins = {}
    
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.plugins[cls.__name__] = cls

class AudioPlugin(Plugin):
    pass

class VideoPlugin(Plugin):
    pass

print(Plugin.plugins)
# {'AudioPlugin': <class 'AudioPlugin'>, 'VideoPlugin': <class 'VideoPlugin'>}
```

### Class Decorators

```python
def register(cls):
    registry[cls.__name__] = cls
    return cls

def add_method(cls):
    cls.new_method = lambda self: "added"
    return cls

@register
@add_method
class MyClass:
    pass
```

---

## Class Creation Timeline

The full pipeline, showing where each hook fires and how `__init_subclass__` fits in:

```text
class MyClass(Base, metaclass=MyMeta):
    ...

Step 1:  MyMeta.__prepare__('MyClass', (Base,))   → namespace dict
Step 2:  Execute class body in that namespace
Step 3:  MyMeta.__new__(mcs, 'MyClass', ...)       → class object created
Step 4:  MyMeta.__init__(cls, 'MyClass', ...)       → class object initialized
Step 5:  Base.__init_subclass__(MyClass)            → parent's subclass hook
```

`__init_subclass__` runs **after** the metaclass has finished creating the class.
This is why it cannot modify the namespace or replace the class — it only sees the
finished product.

## Advanced: __prepare__

Control the namespace dict used during class creation:

```python
from collections import OrderedDict

class OrderedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        # Return custom namespace (must be dict-like)
        return OrderedDict()
    
    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, dict(namespace))
        cls._field_order = list(namespace.keys())
        return cls

class Record(metaclass=OrderedMeta):
    first = 1
    second = 2
    third = 3

print(Record._field_order)
# ['__module__', '__qualname__', 'first', 'second', 'third']
```

---

## When to Use Metaclasses

**Use metaclasses when you need to:**

- Modify class creation before the class exists
- Automatically register all subclasses
- Enforce class-level invariants
- Create DSLs (Domain Specific Languages)
- Build frameworks (ORMs, serializers)

**Famous examples:**

- Django models (`ModelBase`)
- SQLAlchemy ORM (`DeclarativeMeta`)
- ABC module (`ABCMeta`)
- Enum (`EnumMeta`)

### Metaclass vs ABC (Common Confusion)

Metaclasses and abstract base classes (ABCs) both "control class behavior" but at different levels:

| Aspect | Metaclass | ABC |
|---|---|---|
| Level | Class **creation** | Class **usage** (instantiation) |
| When it runs | Class definition time | Instance creation time |
| Purpose | Modify/build the class object | Enforce an interface contract |
| Complexity | Very high | Moderate |

The relationship: ABC is **implemented using** a metaclass. Writing `class Shape(ABC)` is equivalent to `class Shape(metaclass=ABCMeta)`. The metaclass is the underlying mechanism; ABC is a practical tool built on top of it.

---

## Summary

```python
# Class hierarchy
object  # Base of all objects
   ↑
 type   # Metaclass - creates classes (type is its own metaclass)
   ↑
MyMeta  # Custom metaclass
   ↓
MyClass # Regular class (instance of MyMeta)
   ↓
  obj   # Instance of MyClass
```

| Hook | Called When | Use For |
|------|-------------|---------|
| `__new__` | Creating class | Modify namespace, validate |
| `__init__` | Initializing class | Post-creation setup |
| `__call__` | Creating instance | Singleton, pooling |
| `__prepare__` | Before body execution | Custom namespace |

!!! note "Mental Compression"

    A metaclass is to a class what a class is to an instance:

    | Relationship | Factory | Product |
    |---|---|---|
    | Class → Instance | `MyClass()` calls `type.__call__` | instance object |
    | Metaclass → Class | `class MyClass:` calls `MyMeta.__new__` + `MyMeta.__init__` | class object |

    The three metaclass hooks map directly to this:

    - `__new__` — **builds** the class (like `__new__` builds an instance)
    - `__init__` — **configures** the class after creation
    - `__call__` — controls what happens when the class **creates instances**

**Key Takeaways**:

- Classes are instances of metaclasses
- `type` is the default metaclass for all classes
- Metaclasses control class creation and behavior
- Use `__init_subclass__` or decorators when possible
- Reserve metaclasses for framework-level code
- "If you wonder whether you need metaclasses, you don't" — Tim Peters

!!! tip "The Unifying Insight"

    Python is built on just **two fundamental operations**:

    1. **Attribute access**: `obj.attr` → resolved via `__getattribute__`, descriptors, and MRO
    2. **Call**: `obj(...)` → resolved via `__call__`

    Everything else is built on these two:

    - `obj.method()` → attribute lookup + call
    - `MyClass()` → `type.__call__(MyClass)` → `MyClass.__new__` + `MyClass.__init__`
    - `class MyClass:` → `metaclass(name, bases, namespace)` → another call
    - `super().method()` → modified attribute lookup + call

    Once you see this, the entire object model — classes, metaclasses, descriptors, MRO, `super()` — reduces to attribute access and calls, composed in different ways.

---

## Runnable Example: `class_factory_type.py`

```python
"""
TUTORIAL: Class Factory Using type() - Creating Classes Dynamically
===================================================================

In this tutorial, you'll learn how to create classes dynamically using the
type() builtin. Normally, type(obj) returns the type of an object, but type()
has another mode: creating new classes!

Normal usage: type(obj) → returns the class

Dynamic creation: type(name, bases, dict) → creates a NEW class

The three arguments to type():
  1. name (str): The name of the new class
  2. bases (tuple): Parent classes (can be empty for object)
  3. dict (dict): Class attributes and methods

Why create classes dynamically?
  - Build flexible frameworks where classes are generated at runtime
  - Reduce boilerplate when creating many similar classes
  - Generate specialized classes based on data or configuration
  - Create classes from strings (parsing, serialization)

In this example:
  - record_factory() creates classes dynamically using type()
  - These classes are tuples with named fields and custom methods
  - They demonstrate the full power of runtime class creation

Key insight: Classes are objects too! You can create them, modify them,
and pass them around just like any other Python object.
"""

from typing import Union, Any
from collections.abc import Iterable, Iterator


# ============ Example 1: Understanding type() for Class Creation ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Creating classes with type()")
    print("=" * 70)

    # The type() builtin has two modes:
    print(f"\nMode 1: type(obj) returns the class of obj")
    print(f"  type(42) = {type(42)}")
    print(f"  type('hello') = {type('hello')}")
    print(f"  type([1, 2, 3]) = {type([1, 2, 3])}")

    print(f"\nMode 2: type(name, bases, dict) creates a NEW class")
    print(f"  MyClass = type('MyClass', (), {{}})")
    print(f"  Creates: a class named MyClass with no parents and no attributes")

    # Create a simple class dynamically
    MyClass = type('MyClass', (), {})
    print(f"\nMyClass = {MyClass}")
    print(f"  Type: {type(MyClass)}")
    print(f"  Instance: {MyClass()}")


    # ============ Example 2: Adding Attributes and Methods ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Adding methods to dynamically created classes")
    print("=" * 70)

    def say_hello(self):
        """A method to add to the class."""
        return f'Hello from {self.__class__.__name__}'

    def __init__(self, name):
        """An initializer for the class."""
        self.name = name

    def __repr__(self):
        """String representation."""
        return f'{self.__class__.__name__}(name={self.name!r})'

    # Create a class with methods
    Greeter = type('Greeter',
                   (),
                   {'__init__': __init__,
                    'say_hello': say_hello,
                    '__repr__': __repr__,
                    'class_var': 'I am a class variable'})

    print(f"\nGreeter = type('Greeter', (), {{'__init__': ..., 'say_hello': ..., ...}})")
    print(f"\nCreated class: {Greeter}")
    print(f"Class variable: {Greeter.class_var}")

    greeter = Greeter('Alice')
    print(f"\ngreeter = Greeter('Alice')")
    print(f"  greeter.name = '{greeter.name}'")
    print(f"  repr(greeter) = {repr(greeter)}")
    print(f"  greeter.say_hello() = '{greeter.say_hello()}'")


    # ============ Example 3: The record_factory() Function ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Practical example - record_factory()")
    print("=" * 70)

    FieldNames = Union[str, Iterable[str]]

    def record_factory(cls_name: str, field_names: FieldNames) -> type[tuple]:
        """Create a class for holding data, like a namedtuple.

        This factory function dynamically creates classes that:
        1. Store data efficiently using __slots__
        2. Support unpacking (for x, y in records)
        3. Have a nice __repr__ for debugging
        4. Accept both positional and keyword arguments

        Args:
            cls_name: The name for the new class.
            field_names: Field names as a string ('name age') or iterable.

        Returns:
            A new class that can be instantiated with the given fields.
        """

        slots = parse_identifiers(field_names)

        def __init__(self, *args, **kwargs) -> None:
            """Initialize instance, accepting positional and keyword args."""
            attrs = dict(zip(self.__slots__, args))
            attrs.update(kwargs)
            for name, value in attrs.items():
                setattr(self, name, value)

        def __iter__(self) -> Iterator[Any]:
            """Allow unpacking of the instance (for x, y in instances)."""
            for name in self.__slots__:
                yield getattr(self, name)

        def __repr__(self):
            """Return a nice representation like: Dog(name='Rex', weight=30)."""
            values = ', '.join(f'{name}={value!r}'
                for name, value in zip(self.__slots__, self))
            cls_name_local = self.__class__.__name__
            return f'{cls_name_local}({values})'

        # Prepare the class attributes dictionary
        cls_attrs = dict(
            __slots__=slots,
            __init__=__init__,
            __iter__=__iter__,
            __repr__=__repr__,
        )

        # Create and return the class using type()
        return type(cls_name, (object,), cls_attrs)


    def parse_identifiers(names: FieldNames) -> tuple[str, ...]:
        """Parse field names from string or iterable.

        Args:
            names: Either a string like 'name age weight' or a list/tuple.

        Returns:
            Tuple of validated identifier strings.

        Raises:
            ValueError: If any name is not a valid Python identifier.
        """
        if isinstance(names, str):
            names = names.replace(',', ' ').split()
        if not all(s.isidentifier() for s in names):
            raise ValueError('names must all be valid identifiers')
        return tuple(names)


    print(f"\nrecord_factory() creates data classes using type()")
    print(f"\nSignature: record_factory(cls_name, field_names) -> class")
    print(f"\nExample: Dog = record_factory('Dog', 'name weight owner')")


    # ============ Example 4: Using the Created Classes ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Creating and using classes from record_factory()")
    print("=" * 70)

    # Create a Dog class
    Dog = record_factory('Dog', 'name weight owner')

    print(f"\nDog = record_factory('Dog', 'name weight owner')")
    print(f"  Created: {Dog}")
    print(f"  Fields (__slots__): {Dog.__slots__}")

    # Create instances
    rex = Dog('Rex', 30, 'Bob')
    buddy = Dog('Buddy', 25, 'Alice')

    print(f"\nrex = Dog('Rex', 30, 'Bob')")
    print(f"  repr(rex) = {repr(rex)}")

    print(f"\nbuddy = Dog('Buddy', 25, 'Alice')")
    print(f"  repr(buddy) = {repr(buddy)}")

    print(f"\nAccessing attributes:")
    print(f"  rex.name = '{rex.name}'")
    print(f"  rex.weight = {rex.weight}")
    print(f"  rex.owner = '{rex.owner}'")


    # ============ Example 5: Unpacking and Iteration ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Unpacking and iteration support")
    print("=" * 70)

    print(f"\nUnpacking (like tuple unpacking):")
    name, weight, owner = rex
    print(f"  name, weight, owner = rex")
    print(f"  name = '{name}', weight = {weight}, owner = '{owner}'")

    print(f"\nIndexing (like tuple indexing):")
    print(f"  rex[0] = '{rex[0]}'  (name)")
    print(f"  rex[1] = {rex[1]}  (weight)")
    print(f"  rex[2] = '{rex[2]}'  (owner)")

    print(f"\nFormatting with unpacking:")
    message = "{2}'s dog {0} weighs {1}kg"
    print(f"  message = \"{message}\"")
    print(f"  message.format(*rex) = '{message.format(*rex)}'")

    print(f"\nIteration:")
    print(f"  for value in rex:")
    for i, value in enumerate(rex):
        print(f"    [{i}] = {value!r}")


    # ============ Example 6: Modifying Instance Attributes ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Instances are mutable (can be modified)")
    print("=" * 70)

    print(f"\nOriginal: rex = {repr(rex)}")

    rex.weight = 32
    print(f"  rex.weight = 32")
    print(f"  Modified: rex = {repr(rex)}")

    print(f"\nThis is different from namedtuples (immutable)")
    print(f"  - record_factory classes are mutable")
    print(f"  - namedtuples are immutable")
    print(f"  - Both are efficient with __slots__")


    # ============ Example 7: Creating with String or List ============
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Flexible field name input")
    print("=" * 70)

    # Create with string
    Person = record_factory('Person', 'name age city')
    print(f"\nPerson = record_factory('Person', 'name age city')")
    print(f"  Fields: {Person.__slots__}")

    alice = Person('Alice', 30, 'NYC')
    print(f"  alice = Person('Alice', 30, 'NYC')")
    print(f"  repr(alice) = {repr(alice)}")

    # Create with list
    Product = record_factory('Product', ['id', 'name', 'price'])
    print(f"\nProduct = record_factory('Product', ['id', 'name', 'price'])")
    print(f"  Fields: {Product.__slots__}")

    item = Product(1, 'Laptop', 999.99)
    print(f"  item = Product(1, 'Laptop', 999.99)")
    print(f"  repr(item) = {repr(item)}")

    # Create with comma-separated string
    Coordinate = record_factory('Coordinate', 'x,y,z')
    print(f"\nCoordinate = record_factory('Coordinate', 'x,y,z')")
    print(f"  Fields: {Coordinate.__slots__}")

    point = Coordinate(10, 20, 30)
    print(f"  point = Coordinate(10, 20, 30)")
    print(f"  repr(point) = {repr(point)}")


    # ============ Example 8: Keyword Arguments ============
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Creating instances with keyword arguments")
    print("=" * 70)

    # Using positional arguments
    dog1 = Dog('Max', 28, 'Charlie')
    print(f"\ndog1 = Dog('Max', 28, 'Charlie')")
    print(f"  {repr(dog1)}")

    # Using keyword arguments
    dog2 = Dog(name='Lucy', weight=24, owner='Diana')
    print(f"\ndog2 = Dog(name='Lucy', weight=24, owner='Diana')")
    print(f"  {repr(dog2)}")

    # Using mixed positional and keyword
    dog3 = Dog('Buddy', owner='Eve', weight=26)
    print(f"\ndog3 = Dog('Buddy', owner='Eve', weight=26)")
    print(f"  {repr(dog3)}")


    # ============ Example 9: Why Use type() for Class Creation ============
    print("\n" + "=" * 70)
    print("EXAMPLE 9: Why dynamically create classes with type()")
    print("=" * 70)

    print(f"\nBenefits of type()-based class creation:")
    print(f"  1. Reduce boilerplate - don't repeat similar classes")
    print(f"  2. Generate from data - create classes from strings, configs")
    print(f"  3. Framework design - base frameworks on runtime class generation")
    print(f"  4. Meta-programming - inspect and modify classes at runtime")

    print(f"\nUse cases:")
    print(f"  - ORM systems (database mapping): create model classes dynamically")
    print(f"  - Data validation: generate validators from schemas")
    print(f"  - API clients: generate resource classes from API specs")
    print(f"  - Configuration: create classes based on config files")

    print(f"\nAlternatives to type():")
    print(f"  - dataclass: for data-holding classes with less boilerplate")
    print(f"  - namedtuple: for immutable tuple-like classes")
    print(f"  - type(): for maximum flexibility and runtime creation")


    # ============ Example 10: Class Hierarchy ============
    print("\n" + "=" * 70)
    print("EXAMPLE 10: Classes created with type() in the hierarchy")
    print("=" * 70)

    print(f"\nDog.__mro__ (method resolution order):")
    print(f"  {Dog.__mro__}")

    print(f"\nDog class details:")
    print(f"  Dog.__name__ = '{Dog.__name__}'")
    print(f"  Dog.__bases__ = {Dog.__bases__}")
    print(f"  Dog.__dict__ keys = {list(Dog.__dict__.keys())}")

    print(f"\nInstance details:")
    print(f"  rex.__class__.__name__ = '{rex.__class__.__name__}'")
    print(f"  isinstance(rex, Dog) = {isinstance(rex, Dog)}")
    print(f"  type(rex) = {type(rex)}")
    print(f"  type(type(rex)) = {type(type(rex))}")

    print(f"\nThe full chain:")
    print(f"  rex is an instance of Dog")
    print(f"  Dog is an instance of type (it's a class)")
    print(f"  type is an instance of type (it's a metaclass)")


    # ============ Example 11: Summary - Dynamic Class Creation ============
    print("\n" + "=" * 70)
    print("EXAMPLE 11: Summary - When and How to Use type()")
    print("=" * 70)

    print(f"\nThe type() function has three jobs:")
    print(f"  1. type(obj) - returns the type of an object")
    print(f"  2. type(name, bases, dict) - creates a new class")
    print(f"  3. type as a metaclass - controls class creation")

    print(f"\nCreating classes with type():")
    print(f"  Syntax: NewClass = type(name, bases, attributes_dict)")
    print(f"  name: String name for the class")
    print(f"  bases: Tuple of parent classes (or () for object)")
    print(f"  attributes_dict: Dict of methods and class variables")

    print(f"\nKey benefits:")
    print(f"  - Powerful for framework and library design")
    print(f"  - Can generate many similar classes from data")
    print(f"  - Allows runtime inspection and modification")

    print(f"\nImportant notes:")
    print(f"  - Classes created with type() are normal classes")
    print(f"  - They work with inheritance, isinstance(), etc.")
    print(f"  - __slots__ makes them memory-efficient")
    print(f"  - Custom methods work just like normal classes")

    print(f"\n" + "=" * 70)
```

---

## Exercises

**Exercise 1.**
Use `type()` as a function to dynamically create a class `Dog` with a `bark` method and a `species` class attribute. Create an instance and call `bark()`. Show that the dynamically created class behaves identically to one defined with the `class` keyword.

??? success "Solution to Exercise 1"

        def bark(self):
            return f"{self.name} says Woof!"

        Dog = type('Dog', (), {
            'species': 'Canis familiaris',
            'bark': bark,
            '__init__': lambda self, name: setattr(self, 'name', name),
        })

        d = Dog("Buddy")
        print(d.bark())      # Buddy says Woof!
        print(Dog.species)   # Canis familiaris
        print(type(d))       # <class 'Dog'>

---

**Exercise 2.**
Write a metaclass `SingletonMeta` where `__call__` ensures only one instance of any class using this metaclass can exist. If an instance already exists, return it. Apply the metaclass to a `Database` class and show that multiple calls to `Database()` return the same object.

??? success "Solution to Exercise 2"

        class SingletonMeta(type):
            _instances = {}

            def __call__(cls, *args, **kwargs):
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
                return cls._instances[cls]

        class Database(metaclass=SingletonMeta):
            def __init__(self, url="default"):
                self.url = url

        db1 = Database("postgres://localhost")
        db2 = Database("mysql://localhost")

        print(db1 is db2)  # True — same instance
        print(db1.url)     # postgres://localhost (first call wins)

---

**Exercise 3.**
Create a metaclass `AutoReprMeta` that automatically adds a `__repr__` method to any class that uses it. The auto-generated `__repr__` should list all instance attributes. Apply it to a `Point` class with `x` and `y` attributes and show the auto-generated repr.

??? success "Solution to Exercise 3"

        class AutoReprMeta(type):
            def __new__(mcs, name, bases, namespace):
                cls = super().__new__(mcs, name, bases, namespace)
                if '__repr__' not in namespace:
                    def auto_repr(self):
                        attrs = ', '.join(f'{k}={v!r}' for k, v in vars(self).items())
                        return f"{name}({attrs})"
                    cls.__repr__ = auto_repr
                return cls

        class Point(metaclass=AutoReprMeta):
            def __init__(self, x, y):
                self.x = x
                self.y = y

        p = Point(3, 4)
        print(repr(p))  # Point(x=3, y=4)
