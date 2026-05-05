# Properties as a Unified Abstraction

!!! tip "Mental Model"
    A property is not three separate features. It is **one concept** --- a gatekeeper object that sits on a class and intercepts attribute access through up to three hooks: **get**, **set**, and **delete**. The caller writes `obj.x` and has no idea whether they are reading a stored value or triggering a method. Start with a plain attribute; add a property later when you need validation, computation, or access control --- without changing the public API.

!!! note "One Descriptor, Three Hooks"
    Each `@property` creates a single descriptor object with up to three callables (`fget`, `fset`, `fdel`). The `@prop.setter` and `@prop.deleter` decorators attach additional hooks to the **same** descriptor. They are not independent features.

---

## What Are Properties?

A **property** lets you define methods that behave like attributes. It is declared using the `@property` decorator and optionally `@<name>.setter` and `@<name>.deleter`.

Use properties to:

- Expose **computed values** as attributes
- Add **getter/setter logic** without changing the external API
- Enforce **validation** or **read-only** access
- Keep internal representation private while providing a clean interface

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        from math import pi
        return pi * self._radius ** 2

c = Circle(3)
print(c.area)   # attribute-like access, but computed
# c.area = 50   # AttributeError: no setter defined
```

!!! tip "Core Rule"
    `@property` = **controlled attribute access**. It lets you compute, validate, or restrict without changing how callers access the attribute. The caller writes `obj.attr` --- they never know whether it is a stored value or a method call.

---

## Why Properties Exist

Start with a plain attribute:

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

c = Circle(5)
print(c.radius)    # 5
c.radius = 10      # direct access
```

Later, you need validation. You have two choices.

**Option 1: Introduce a method** --- breaks existing code:

```python
# Old code: c.radius = 10       <-- breaks
# New code: c.set_radius(10)    <-- different API
```

Every caller that wrote `c.radius` must be rewritten.

**Option 2: Use `@property`** --- old code still works:

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius        # triggers setter

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("must be positive")
        self._radius = value

c = Circle(5)
c.radius = 10      # still works -- setter validates silently
print(c.radius)     # still works -- getter returns value
```

Callers see no change. Validation was added without touching the interface.

!!! tip "The Design Principle"
    `@property` separates **what users see** (`obj.radius`) from **how it works** (validation, computation, storage). This lets you evolve implementation without breaking existing code --- the same principle Java solves with boilerplate getters/setters, but without the boilerplate.

| Approach | Read Syntax | Write Syntax | Pythonic |
|----------|-------------|--------------|----------|
| Explicit methods | `p.get_name()` | `p.set_name("Bob")` | No |
| Property | `p.name` | `p.name = "Bob"` | Yes |

---

## The Three Hooks: Getter, Setter, Deleter

### Getter

The `@property` decorator turns a method into a readable attribute.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius
```

### Setter

The `@<name>.setter` decorator defines what happens on assignment.

```python
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Negative radius")
        self._radius = value
```

### Deleter

The `@<name>.deleter` decorator defines what happens on `del obj.attr`.

```python
    @radius.deleter
    def radius(self):
        del self._radius
```

Most properties do not need a deleter. Common uses include invalidating caches, closing resources, and resetting state.

!!! warning "Name Matching Requirement"
    The setter and deleter method names **must** be identical to the property name --- `@radius.setter def radius(self, value)`. A mismatched name silently creates a separate property instead of attaching a hook to the existing one.

---

## Read-Only Properties

A read-only property is a `@property` with no setter. Any attempt to assign to it raises `AttributeError`.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        from math import pi
        return pi * self._radius ** 2

c = Circle(5)
print(c.area)    # 78.54...
# c.area = 100  # AttributeError: can't set attribute
```

Use read-only properties when:

- The value is derived from other state (area from radius)
- External modification would break invariants
- You want to express immutability at the language level

### Immutable Objects

Making all attributes read-only produces an immutable object:

```python
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def magnitude(self):
        return (self._x ** 2 + self._y ** 2) ** 0.5

    def move(self, dx, dy):
        """Return a new Point -- the original is unchanged."""
        return Point(self._x + dx, self._y + dy)
```

Benefits: thread-safe by design, usable as dictionary keys (with `__hash__`), easier to reason about.

### Caveat: `__dict__` Override

Writing directly to `obj.__dict__['area'] = 100` bypasses the descriptor. The shadowed value is never returned because data descriptors take priority, but it can cause confusion. Avoid manipulating `__dict__` directly for property-controlled attributes. For more, see [Properties as Descriptors](property_descriptor_connection.md).

---

## Internal Mechanism

### The Plain-English Version

When you write `@property` above a method, Python creates a **gatekeeper object** that sits on the class and watches for anyone trying to read, write, or delete that attribute name.

- **Read** `obj.name` --- the gatekeeper calls your getter and returns the result.
- **Write** `obj.name = value` --- the gatekeeper calls your setter (or raises an error if none exists).
- **Delete** `del obj.name` --- the gatekeeper calls your deleter.

The gatekeeper always runs before Python checks the instance's own dictionary, so it cannot be bypassed by accident. This is why properties can enforce validation --- the gatekeeper intercepts every access.

### The Technical Details

`@property` creates a **descriptor object** of type `property` that implements `__get__`, `__set__`, and `__delete__`. It lives in the class's namespace (`Circle.__dict__`). Because it defines both `__get__` and `__set__`, it is a **data descriptor** --- it takes priority over instance `__dict__` entries during attribute lookup.

```python
print(type(Circle.area))             # <class 'property'>
print(isinstance(Circle.area, property))  # True
```

Every `property` object stores three function references internally:

- **`fget`** --- the **getter** function. Called when you read the attribute (`obj.x`). This is the method you decorate with `@property`.
- **`fset`** --- the **setter** function. Called when you assign to the attribute (`obj.x = value`). This is the method you decorate with `@x.setter`. If `None`, assignment raises `AttributeError`.
- **`fdel`** --- the **deleter** function. Called when you delete the attribute (`del obj.x`). This is the method you decorate with `@x.deleter`. If `None`, deletion raises `AttributeError`.

You can inspect them directly:

```python
Circle.area.fget   # <function Circle.area at 0x...>
Circle.area.fset   # None (read-only — no setter defined)
Circle.area.fdel   # None (no deleter defined)
```

These are **two layers** of the same mechanism — just like `a + b` is actually `a.__add__(b)`, attribute access is actually a descriptor call:

| Syntax | Python desugars to | Which calls |
|---|---|---|
| `obj.x` (read) | `type(obj).__dict__['x'].__get__(obj, type(obj))` | `fget(obj)` |
| `obj.x = v` (write) | `type(obj).__dict__['x'].__set__(obj, v)` | `fset(obj, v)` |
| `del obj.x` (delete) | `type(obj).__dict__['x'].__delete__(obj)` | `fdel(obj)` |

And the mapping from your decorators to what gets stored:

| Your code | Stored in property as | Descriptor method that calls it |
|---|---|---|
| `@property def x` | `fget` | `__get__` |
| `@x.setter def x` | `fset` | `__set__` |
| `@x.deleter def x` | `fdel` | `__delete__` |

`fget/fset/fdel` = **what to do** (your functions). `__get__/__set__/__delete__` = **when Python does it** (descriptor protocol, triggered by attribute access). The `property` object connects the two: `property.__get__(obj, cls)` internally calls `fget(obj)`.

!!! warning "Why Properties Enforce Control"
    Properties work because they are **data descriptors** --- they define both `__get__` and `__set__` (even if the setter raises `AttributeError`). Data descriptors are checked **before** the instance `__dict__` during attribute lookup. Without this mechanism, any assignment would bypass property logic entirely.

For the full descriptor mechanics, see [Properties as Descriptors](property_descriptor_connection.md).

---

## Common Patterns

### Computed Values

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        return self.width * self.height

    @property
    def perimeter(self):
        return 2 * (self.width + self.height)

    @property
    def diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** 0.5
```

### Derived Attributes

```python
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        return f"{self.first_name[0]}.{self.last_name[0]}."
```

### Lazy Evaluation

Defer expensive work until the value is actually needed. This is a manual version of a cached property. For a reusable descriptor-based implementation, see [Cached Properties](cached_property.md).

```python
class ExpensiveCalculation:
    def __init__(self, data):
        self._data = data
        self._result = None

    @property
    def result(self):
        if self._result is None:
            self._result = sum(x ** 2 for x in self._data)
        return self._result
```

### Conditional Read-Only

Make a property writable until some condition locks it:

```python
class Document:
    def __init__(self):
        self._content = ""
        self._locked = False

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._locked:
            raise AttributeError("Document is locked")
        self._content = value

    def lock(self):
        self._locked = True
```

### Type Conversion

```python
class DataRecord:
    def __init__(self, timestamp_str):
        self._timestamp_str = timestamp_str

    @property
    def timestamp(self):
        """Always returns a datetime object."""
        from datetime import datetime
        return datetime.fromisoformat(self._timestamp_str)
```

---

## Properties vs Methods

Use `@property` when the access **looks like reading an attribute**: the name is a noun, the computation is fast, and there are no side effects beyond the computation itself.

Use a **method** when the operation is a verb, is expensive, has side effects, takes parameters, or might involve I/O.

| Criterion | Property | Method |
|-----------|----------|--------|
| Name | Noun (`area`, `name`) | Verb (`save`, `fetch`) |
| Speed | Fast / cached | May be slow |
| Side effects | None | Allowed |
| Parameters | None (beyond `self`) | Accepted |
| Example | `circle.area` | `db.query(sql)` |

```python
# Property -- noun, fast, pure computation
class Circle:
    @property
    def area(self):
        import math
        return math.pi * self.radius ** 2

# Method -- verb, expensive, I/O
class Database:
    def query(self, sql):
        return self.execute(sql)
```

---

## Best Practices

1. **Start with plain attributes.** Add `@property` only when you need validation, computation, or read-only access.
2. **Keep properties fast.** Users expect `obj.x` and `obj.x = val` to be near-instant. Use methods for expensive operations.
3. **Prefer immutability.** Omit the setter to make an attribute read-only when external modification would break invariants.
4. **Don't write trivial properties.** A getter that returns `self._x` with no validation or computation adds noise, not value. Use a plain attribute instead.
5. **Document your properties.** The getter's docstring becomes the property's `__doc__`.
6. **Use lazy loading for expensive computations.** Cache the result in a private attribute so work is done at most once.

---

## Runnable Example: `property_decorator_basic.py`

```python
"""
TUTORIAL: The @property Decorator - Computed Attributes

This tutorial teaches you how to use the @property decorator to create
computed attributes that look like simple instance attributes but actually
run custom code. Properties let you write foo.bar instead of foo.get_bar()
while still controlling access, validation, and computation.

This is one of Python's most useful and commonly used features.

Key Learning Goals:
  - Understand why properties are useful
  - Implement basic properties with getters and setters
  - Learn property documentation and introspection
  - See how properties enforce encapsulation without boilerplate
  - Understand performance implications
"""

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: The @property Decorator - Computed Attributes")
    print("=" * 70)

    # ============ EXAMPLE 1: The Problem - Boilerplate Without Properties ============
    print("\n# Example 1: Without Properties - The Verbose Way")
    print("=" * 70)

    class BankAccountBad:
        """
        Bank account WITHOUT properties (the verbose, non-Pythonic way).

        This is how you might write code in Java or C#. Not in Python!
        """

        def __init__(self, name, balance):
            self._name = name
            self._balance = balance

        def get_name(self):
            """Get the account holder name."""
            return self._name

        def set_name(self, value):
            """Set the account holder name."""
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Name must be non-empty string")
            self._name = value

        def get_balance(self):
            """Get the current balance."""
            return self._balance

        def set_balance(self, value):
            """Set the balance (with validation)."""
            if value < 0:
                raise ValueError("Balance cannot be negative")
            self._balance = value


    print("Without properties, you write:")
    account = BankAccountBad("Alice", 1000)
    print(f"Name: {account.get_name()}")
    print(f"Balance: {account.get_balance()}")
    print()

    print("This is verbose and repetitive!")
    print("Users have to remember: get_name(), get_balance(), etc.")
    print("And we lost the nice attribute syntax: account.name")
    print("""
    WHY THIS IS BAD:
        - Too much boilerplate (get_/set_ methods)
        - Ugly syntax: account.get_name() vs account.name
        - Hard to add validation later (breaks API)
        - Not Pythonic (Python prefers simple attribute access)
    """)

    # ============ EXAMPLE 2: Basic Property - Read-Only ============
    print("\n# Example 2: Basic Property - Read-Only Access")
    print("=" * 70)

    class Person:
        """
        Person class with a read-only name property.

        The @property decorator turns a method into a readable attribute.
        """

        def __init__(self, name):
            self._name = name  # Private attribute (convention: leading underscore)

        @property
        def name(self):
            """
            The name property.

            After @property decorator, you access this as person.name
            (attribute syntax) not person.name() (method syntax).

            The method becomes a property getter.
            """
            print(f"  [Getting name: {self._name}]")  # Show that code runs
            return self._name


    person = Person("Bob")

    print(f"Accessing person.name (attribute syntax, not method):")
    name = person.name
    print(f"Got: {name}")
    print()

    print("Try to set it:")
    try:
        person.name = "Charlie"
    except AttributeError as e:
        print(f"  Error: {e}")

    print("""
    WHY: The @property decorator makes the method look like an attribute.
    You write person.name not person.name(). Clean and intuitive!

    Since we only have @property (getter), the attribute is read-only.
    Attempting to set it raises AttributeError.
    """)

    # ============ EXAMPLE 3: Property with Setter ============
    print("\n# Example 3: Property with Getter and Setter")
    print("=" * 70)

    class Rectangle:
        """
        Rectangle with width and height properties that allow getting and setting.

        Use @property for the getter, @name.setter for the setter.
        Both run custom code (like validation).
        """

        def __init__(self, width, height):
            self._width = width
            self._height = height

        @property
        def width(self):
            """Get the width."""
            return self._width

        @width.setter
        def width(self, value):
            """
            Set the width with validation.

            The setter method name must match the property name.
            The decorator is @name.setter, not @property.
            """
            if not isinstance(value, (int, float)):
                raise TypeError("Width must be a number")
            if value <= 0:
                raise ValueError("Width must be positive")
            print(f"  [Setting width to {value}]")
            self._width = value

        @property
        def height(self):
            """Get the height."""
            return self._height

        @height.setter
        def height(self, value):
            """Set the height with validation."""
            if not isinstance(value, (int, float)):
                raise TypeError("Height must be a number")
            if value <= 0:
                raise ValueError("Height must be positive")
            print(f"  [Setting height to {value}]")
            self._height = value

        @property
        def area(self):
            """
            Computed property: area is calculated, not stored.

            This is read-only (no setter) - it's always computed from width/height.
            """
            return self._width * self._height


    rect = Rectangle(3, 4)

    print(f"Width: {rect.width}, Height: {rect.height}")
    print(f"Area: {rect.area} (computed, not stored)")
    print()

    print("Setting width to 5:")
    rect.width = 5
    print(f"New area: {rect.area}")
    print()

    print("Validation works:")
    try:
        rect.width = -10
    except ValueError as e:
        print(f"  Error: {e}")

    try:
        rect.height = "invalid"
    except TypeError as e:
        print(f"  Error: {e}")

    print("""
    WHY: Properties let you:
        1. Use attribute syntax (rect.width not rect.get_width())
        2. Run validation code transparently
        3. Compute values on-the-fly (rect.area)
        4. Control access (read-only, write-only, or both)
        5. Change implementation without breaking the API

    If you later want to add validation or computation, users don't know
    or care - they still use attribute syntax.
    """)

    # ============ EXAMPLE 4: Property Documentation ============
    print("\n# Example 4: Property Documentation and Introspection")
    print("=" * 70)

    class Foo:
        """Example class with documented properties."""

        @property
        def bar(self):
            """
            The bar attribute.

            This docstring becomes the property's documentation.
            Visible via help() and IDE tooltips.
            """
            return self.__dict__.get('bar', 'default')

        @bar.setter
        def bar(self, value):
            self.__dict__['bar'] = value


    # Access property documentation
    print("Property documentation:")
    print(f"  Foo.bar.__doc__ = {repr(Foo.bar.__doc__)}")
    print()

    foo = foo_instance = Foo()

    # Inspect properties
    print("Introspection:")
    print(f"  type(Foo.bar) = {type(Foo.bar)}")
    print(f"  isinstance(Foo.bar, property) = {isinstance(Foo.bar, property)}")
    print()

    # Help on property
    print("Help for property:")
    print(f"  Foo.bar.fget = {Foo.bar.fget}")  # getter function
    print(f"  Foo.bar.fset = {Foo.bar.fset}")  # setter function
    print(f"  Foo.bar.fdel = {Foo.bar.fdel}")  # deleter function (None if not defined)

    print("""
    WHY: Properties have introspectable metadata:
        - __doc__: The docstring
        - fget, fset, fdel: The getter, setter, deleter functions
        - You can check isinstance(attr, property) to detect properties

    This is useful for frameworks and tools that need to understand
    your class structure.
    """)

    # ============ EXAMPLE 5: Using __dict__ Directly (Storage Pattern) ============
    print("\n# Example 5: Storing in __dict__ (Instance Dictionary)")
    print("=" * 70)

    class Thermostat:
        """
        Thermostat with temperature property that stores in __dict__.

        The common pattern: store attributes in self.__dict__ instead of
        private attributes like self._temp.
        """

        @property
        def celsius(self):
            """
            Get temperature in Celsius.

            This gets/sets directly in the __dict__ dictionary.
            """
            return self.__dict__.get('celsius', 20)  # default 20 degrees

        @celsius.setter
        def celsius(self, value):
            """Set temperature with bounds checking."""
            if not -50 <= value <= 50:
                raise ValueError("Temperature must be between -50 and 50 Celsius")
            self.__dict__['celsius'] = value

        @property
        def fahrenheit(self):
            """Get temperature in Fahrenheit (computed)."""
            return (self.celsius * 9/5) + 32

        @fahrenheit.setter
        def fahrenheit(self, value):
            """Set temperature from Fahrenheit."""
            self.celsius = (value - 32) * 5/9


    thermo = Thermostat()

    print(f"Default temperature: {thermo.celsius}C = {thermo.fahrenheit}F")
    print()

    print("Setting to 25C:")
    thermo.celsius = 25
    print(f"  {thermo.celsius}C = {thermo.fahrenheit}F")
    print()

    print("Setting to 68F:")
    thermo.fahrenheit = 68
    print(f"  {thermo.celsius:.1f}C = {thermo.fahrenheit:.1f}F")
    print()

    print("Instance __dict__:")
    print(f"  {thermo.__dict__}")

    print("""
    WHY: Using __dict__ directly is clean and idiomatic Python.
    You don't need separate private attributes when properties manage
    access to __dict__.

    PATTERN:
        @property
        def attr(self):
            return self.__dict__.get('attr', default)

        @attr.setter
        def attr(self, value):
            self.__dict__['attr'] = value
    """)

    # ============ EXAMPLE 6: Common Anti-Pattern - Avoid This ============
    print("\n# Example 6: Anti-Pattern - Storing in Private Attribute")
    print("=" * 70)

    class BadDesign:
        """Example of property anti-pattern (stores in _attr for no reason)."""

        def __init__(self):
            self._value = None

        @property
        def value(self):
            # Unnecessary indirection!
            return self._value

        @value.setter
        def value(self, x):
            self._value = x  # Just copying to self._value. Why?


    print("This is an anti-pattern - the property adds no value:")
    print("  - No validation")
    print("  - No computation")
    print("  - Just stores in _value")
    print()

    print("""
    BETTER: Just use self.value = x directly

    If you later need validation:
        @property
        def value(self):
            return self.__dict__.get('value')

        @value.setter
        def value(self, x):
            if not validate(x):
                raise ValueError("Invalid")
            self.__dict__['value'] = x

    Only use @property when you need custom behavior (validation,
    computation, access control). Don't use it for trivial getters/setters.
    """)

    # ============ EXAMPLE 7: Deleter and Other Tricks ============
    print("\n# Example 7: Property Deleter - Handling Deletion")
    print("=" * 70)

    class Cache:
        """
        Cache with a value property that can be deleted.

        @name.deleter defines what happens when you delete the property.
        """

        def __init__(self):
            self._value = None
            self._cached = False

        @property
        def value(self):
            """Get the cached value."""
            return self._value

        @value.setter
        def value(self, x):
            """Set and mark as cached."""
            self._value = x
            self._cached = True

        @value.deleter
        def value(self):
            """Delete and invalidate cache."""
            print("  [Cache invalidated]")
            self._value = None
            self._cached = False


    cache = Cache()

    print("Setting cache value:")
    cache.value = "important data"
    print(f"  Value: {cache.value}, Cached: {cache._cached}")
    print()

    print("Deleting cache:")
    del cache.value
    print(f"  Value: {cache.value}, Cached: {cache._cached}")

    print("""
    WHY: The deleter lets you handle del obj.property.

    COMMON USES:
        - Invalidate caches
        - Close resources
        - Reset state
        - Trigger cleanup

    Most properties don't need deleters, but they're there when needed.
    """)

    # ============ EXAMPLE 8: Lazy Evaluation with Properties ============
    print("\n# Example 8: Lazy Evaluation - Compute Only When Needed")
    print("=" * 70)

    class ExpensiveComputation:
        """
        Properties for lazy evaluation: compute only when accessed.

        This pattern defers expensive work until the value is actually needed.
        """

        def __init__(self, name):
            self.name = name
            self._result = None  # None means "not computed yet"

        @property
        def result(self):
            """
            Compute expensive result, but only on first access.

            Subsequent accesses return the cached result.
            """
            if self._result is None:
                print(f"  [Computing result for {self.name}...]")
                import time
                time.sleep(0.1)  # Simulate expensive work
                self._result = f"Result of {self.name}"
            else:
                print(f"  [Using cached result for {self.name}]")
            return self._result


    obj = ExpensiveComputation("task")

    print("First access (computes):")
    r1 = obj.result
    print(f"  Got: {r1}")
    print()

    print("Second access (cached):")
    r2 = obj.result
    print(f"  Got: {r2}")

    print("""
    WHY: Lazy evaluation defers expensive computations:
        - If the result is never accessed, work isn't done
        - If accessed multiple times, work is done once
        - Client code uses simple property access

    PATTERN:
        @property
        def expensive_attr(self):
            if self._cached_value is None:
                self._cached_value = do_expensive_work()
            return self._cached_value
    """)

    # ============ EXAMPLE 9: Properties vs Methods ============
    print("\n# Example 9: Choosing Between Properties and Methods")
    print("=" * 70)

    print("""
    USE @property WHEN:
        - Value looks like an attribute (singular noun)
        - Access is fast (cached or simple computation)
        - Logically feels like an attribute (name, age, area)
        - No side effects beyond computation
        - You might want to change to simple attribute later

    USE A METHOD WHEN:
        - Operation name is a verb (get_user(), save())
        - Computation is expensive (database query)
        - Has side effects (I/O, modifies state)
        - Takes parameters (get(key), find(pattern))
        - Might take variable time (network request)

    EXAMPLES:

    PROPERTY:
        class Circle:
            @property
            def area(self):  # Noun, fast, pure computation
                return math.pi * self.radius ** 2

    METHOD:
        class Database:
            def query(self, sql):  # Verb, expensive, I/O
                return self.execute(sql)

        class User:
            def save(self):  # Verb, side effects
                self.db.insert(self)

    PROPERTY:
        class Point:
            @property
            def magnitude(self):  # Noun, fast, pure
                return math.hypot(self.x, self.y)

    METHOD:
        class API:
            def fetch(self, url):  # Verb, expensive, I/O
                return requests.get(url)
    """)

    # ============ EXAMPLE 10: Summary ============
    print("\n# Example 10: Property Implementation Checklist")
    print("=" * 70)

    class CompleteExample:
        """Example showing all property features together."""

        def __init__(self, name):
            self._name = name
            self._active = True

        @property
        def name(self):
            """
            Get the name.

            Always include documentation for properties!
            """
            return self._name

        @name.setter
        def name(self, value):
            """Set name with validation."""
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Name must be non-empty string")
            self._name = value

        @name.deleter
        def name(self):
            """Deleting name disables the object."""
            self._active = False

        @property
        def is_active(self):
            """Read-only property (no setter)."""
            return self._active


    print("Complete example:")
    obj = CompleteExample("Alice")
    print(f"Name: {obj.name}")
    print(f"Active: {obj.is_active}")
    print()

    obj.name = "Bob"
    print(f"After setting name: {obj.name}")
    print()

    del obj.name
    print(f"After deleting name: {obj.is_active}")

    print("""
    PROPERTY CHECKLIST:
        - Use @property for getter
        - Use @name.setter for setter (if needed)
        - Use @name.deleter for deleter (rarely needed)
        - Store in __dict__ or private attribute
        - Validate in setter
        - Include docstring
        - Handle None defaults gracefully
        - Make computation fast or lazy-load
        - Don't use for expensive I/O (use methods instead)
        - Document return type in docstring

    PERFORMANCE:
        - Properties have slightly more overhead than attributes
        - But far less than method calls
        - Use lazy-loading for expensive computations
        - Cache results when appropriate
    """)

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
    1. PROPERTIES LOOK LIKE ATTRIBUTES: @property makes methods look like
       simple attributes. You write obj.name not obj.name().

    2. POWERFUL ENCAPSULATION: Properties let you validate, compute, or
       control access without breaking the API.

    3. CHANGE IMPLEMENTATION WITHOUT BREAKING CODE: Start with simple
       attributes. Add @property later if you need custom behavior.

    4. FOLLOW NAMING CONVENTIONS: Name properties like nouns (name, area,
       is_active) and methods like verbs (get_data(), save()).

    5. USE __dict__ STORAGE: Store properties in self.__dict__ directly
       for a clean, idiomatic pattern.

    6. DOCUMENT YOUR PROPERTIES: Include docstrings explaining what the
       property does, its type, and any constraints.

    7. LAZY-LOAD EXPENSIVE COMPUTATIONS: Cache results to avoid recomputing
       on every access.

    8. DON'T OVERUSE PROPERTIES: Only use them when you need custom behavior.
       Simple attributes are fine as-is.

    9. PROPERTIES ARE PYTHONIC: They're one of Python's most elegant features.
       Used everywhere in professional code.

    10. COMBINATION WITH OTHER FEATURES: Properties work great with
        descriptors, metaclasses, and other advanced features - but you
        usually don't need them.
    """)
```

---

## Exercises

**Exercise 1.** Create a class `BankAccount` with a private `_balance` attribute. Use `@property` to provide read-only access to the balance. Add `deposit(amount)` and `withdraw(amount)` methods that modify `_balance` with validation (no negative deposits, no overdrafts). Show that assigning to `account.balance` raises an error.

??? success "Solution to Exercise 1"
    ```python
    class BankAccount:
        def __init__(self, initial_balance=0):
            self._balance = initial_balance

        @property
        def balance(self):
            return self._balance

        def deposit(self, amount):
            if amount <= 0:
                raise ValueError("Deposit must be positive")
            self._balance += amount

        def withdraw(self, amount):
            if amount <= 0:
                raise ValueError("Withdrawal must be positive")
            if amount > self._balance:
                raise ValueError("Insufficient funds")
            self._balance -= amount

    account = BankAccount(1000)
    print(account.balance)    # 1000
    account.deposit(500)
    print(account.balance)    # 1500
    account.withdraw(200)
    print(account.balance)    # 1300

    try:
        account.balance = 9999
    except AttributeError as e:
        print(e)  # property 'balance' of 'BankAccount' object has no setter
    ```

---

**Exercise 2.** Write a `Temperature` class with a `celsius` property that has a getter, setter, and deleter. The setter should reject values below $-273.15$. The deleter should reset the temperature to `0`. Demonstrate all three operations.

??? success "Solution to Exercise 2"
    ```python
    class Temperature:
        def __init__(self, celsius=0):
            self.celsius = celsius

        @property
        def celsius(self):
            return self._celsius

        @celsius.setter
        def celsius(self, value):
            if value < -273.15:
                raise ValueError("Below absolute zero")
            self._celsius = value

        @celsius.deleter
        def celsius(self):
            self._celsius = 0

    t = Temperature(100)
    print(t.celsius)       # 100

    t.celsius = -10
    print(t.celsius)       # -10

    del t.celsius
    print(t.celsius)       # 0

    try:
        t.celsius = -300
    except ValueError as e:
        print(e)           # Below absolute zero
    ```

---

**Exercise 3.** Create an immutable `Point` class with read-only `x` and `y` properties and a read-only `distance_from_origin` property that computes $\sqrt{x^2 + y^2}$. Show that attempting to set `x` or `y` raises an error.

??? success "Solution to Exercise 3"
    ```python
    import math

    class Point:
        def __init__(self, x, y):
            self._x = x
            self._y = y

        @property
        def x(self):
            return self._x

        @property
        def y(self):
            return self._y

        @property
        def distance_from_origin(self):
            return math.sqrt(self._x ** 2 + self._y ** 2)

    p = Point(3, 4)
    print(p.x)                      # 3
    print(p.y)                      # 4
    print(p.distance_from_origin)   # 5.0

    try:
        p.x = 10
    except AttributeError:
        print("Cannot set x")  # Cannot set x
    ```

---

**Exercise 4.** Implement a `Document` class whose `content` property starts as writable but becomes read-only after calling `lock()`. Demonstrate both the writable and locked states.

??? success "Solution to Exercise 4"
    ```python
    class Document:
        def __init__(self, content=""):
            self._content = content
            self._locked = False

        @property
        def content(self):
            return self._content

        @content.setter
        def content(self, value):
            if self._locked:
                raise AttributeError("Document is locked")
            self._content = value

        def lock(self):
            self._locked = True

    doc = Document()
    doc.content = "Hello, world!"
    print(doc.content)  # Hello, world!

    doc.lock()
    try:
        doc.content = "New text"
    except AttributeError as e:
        print(e)  # Document is locked
    ```

---

**Exercise 5.** A `Student` class has `name` and an optional `id_num`. The tuition `price` should be 7000 if the student has an ID number, and 8000 otherwise. A junior developer stores `price` as a plain attribute set in `__init__`. Explain why a `@property` is a better design, then implement it. Show that the same class produces different prices for different students without any explicit assignment to `price`.

```python
# Junior version (plain attribute)
class Student:
    def __init__(self, name, id_num=None):
        self.name = name
        self.id_num = id_num
        if id_num is not None:
            self.price = 7000
        else:
            self.price = 8000
```

??? success "Solution to Exercise 5"
    The plain-attribute version works, but the price logic is buried in `__init__` and can be overridden by accident (`a.price = 0`). A `@property` makes the rule explicit, computed, and read-only:

    ```python
    class Student:
        def __init__(self, name, id_num=None):
            self.name = name
            self.id_num = id_num

        @property
        def price(self):
            if self.id_num is not None:
                return 7000
            else:
                return 8000

    a = Student("Kim", 12345)
    print(a.price)  # 7000

    b = Student("Lee")
    print(b.price)  # 8000

    # a.price = 0  # AttributeError -- cannot override the rule
    ```

    The `@property` version is better because: (1) the pricing rule lives in one place, not scattered in `__init__`, (2) it is read-only --- external code cannot accidentally set `price` to an invalid value, and (3) if the rule changes later (e.g., different tiers), you modify one method instead of hunting through constructors.

---

**Exercise 6.** Write a `Person` class where `name` is a property with both a getter and setter. The setter should strip leading/trailing whitespace and raise `ValueError` if the name is empty after stripping. Add a read-only `full_name` property using `first_name` and `last_name` stored internally. Demonstrate both valid and invalid usage.

??? success "Solution to Exercise 6"
    ```python
    class Person:
        def __init__(self, name):
            self.name = name  # uses the setter

        @property
        def name(self):
            return f"{self._first} {self._last}"

        @name.setter
        def name(self, value):
            cleaned = value.strip()
            if not cleaned:
                raise ValueError("Name cannot be empty")
            parts = cleaned.split(maxsplit=1)
            self._first = parts[0]
            self._last = parts[1] if len(parts) > 1 else ""

    p = Person("  Alice Smith  ")
    print(p.name)  # Alice Smith

    p.name = "Bob Jones"
    print(p.name)  # Bob Jones

    try:
        p.name = "   "
    except ValueError as e:
        print(e)  # Name cannot be empty
    ```
