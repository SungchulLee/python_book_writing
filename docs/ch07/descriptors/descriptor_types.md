# Data vs Non-Data

!!! tip "Mental Model"
    The key question is: **does the descriptor control writes?** If it defines `__set__` or `__delete__`, it is a *data* descriptor and wins over instance `__dict__`. If it only defines `__get__`, it is *non-data* and instance `__dict__` can shadow it. This single distinction — write control — determines lookup priority.

## Two Types

### 1. Definitions

**Data Descriptor:**

- Defines `__set__` and/or `__delete__` (at least one)
- Takes **priority** over instance `__dict__`

**Non-Data Descriptor:**

- Defines **only** `__get__`
- **Defers** to instance `__dict__` if it exists

### 2. Key Difference

```python
# Data descriptor - has __set__
class DataDesc:
    def __get__(self, instance, owner):
        return "data descriptor"
    
    def __set__(self, instance, value):
        pass  # Even empty __set__ makes it data descriptor

# Non-data descriptor - only __get__
class NonDataDesc:
    def __get__(self, instance, owner):
        return "non-data descriptor"
```

### 3. Priority Table

| Lookup Order | What Python Checks |
|--------------|-------------------|
| 1st | Data descriptors from class (MRO search) |
| 2nd | Instance `__dict__` |
| 3rd | Non-data descriptors and plain class attributes (MRO search) |
| 4th | `__getattr__` if defined |

See [Attribute Access and Lookup](attribute_access_lookup.md) for the full resolution pipeline including `__getattribute__` and MRO.

## Priority Demonstration

### 1. Data Descriptor Wins

```python
class DataDescriptor:
    def __get__(self, instance, owner):
        return "from data descriptor"
    
    def __set__(self, instance, value):
        print(f"Setting via descriptor: {value}")

class MyClass:
    attr = DataDescriptor()

obj = MyClass()

# Try to set in instance dict
obj.__dict__['attr'] = "instance value"

# Data descriptor wins!
print(obj.attr)  # "from data descriptor"
```

### 2. Instance Dict Wins

```python
class NonDataDescriptor:
    def __get__(self, instance, owner):
        return "from non-data descriptor"

class MyClass:
    attr = NonDataDescriptor()

obj = MyClass()

# Set in instance dict
obj.__dict__['attr'] = "instance value"

# Instance dict wins!
print(obj.attr)  # "instance value"
```

### 3. Side-by-Side Comparison

```python
class DataDesc:
    def __get__(self, instance, owner):
        return "data"
    def __set__(self, instance, value):
        pass

class NonDataDesc:
    def __get__(self, instance, owner):
        return "non-data"

class Example:
    data_attr = DataDesc()
    nondata_attr = NonDataDesc()

obj = Example()

# Set in instance __dict__
obj.__dict__['data_attr'] = "instance data"
obj.__dict__['nondata_attr'] = "instance non-data"

print(obj.data_attr)     # "data" (descriptor wins)
print(obj.nondata_attr)  # "instance non-data" (instance wins)
```

## Real-World Examples

### 1. Property is Data Descriptor

```python
class Example:
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        self._value = val

obj = Example()

# Property has both __get__ and __set__
print(hasattr(type(obj).__dict__['value'], '__get__'))  # True
print(hasattr(type(obj).__dict__['value'], '__set__'))  # True

# Try to override in instance dict
obj.__dict__['value'] = 999

# Property still wins!
obj.value = 42
print(obj.value)  # 42 (not 999)
```

### 2. Methods are Non-Data

```python
class Example:
    def method(self):
        return "original method"

obj = Example()

# Methods only have __get__ (non-data descriptor)
print(hasattr(type(obj).__dict__['method'], '__get__'))  # True
print(hasattr(type(obj).__dict__['method'], '__set__'))  # False

# Can override in instance dict!
obj.__dict__['method'] = lambda: "overridden"
print(obj.method())  # "overridden"
```

### 3. Read-Only Property

```python
class ReadOnlyProperty:
    """Non-data descriptor (no __set__)"""
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.func(instance)

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @ReadOnlyProperty
    def area(self):
        from math import pi
        return pi * self.radius ** 2

c = Circle(5)
print(c.area)  # 78.54...

# Can override because it's non-data!
c.__dict__['area'] = 100
print(c.area)  # 100
```

## Why This Matters

### 1. Property Behavior

The `property` type always defines `__set__` and `__delete__`, making every property a data descriptor — even without an explicit setter. A read-only property's `__set__` raises `AttributeError`, which prevents instance `__dict__` from shadowing it:

```python
class Person:
    @property
    def name(self):
        return self._name

p = Person()
p._name = "Alice"

# Cannot shadow — property is a data descriptor regardless of setter
p.__dict__['name'] = "override"
print(p.name)  # "Alice" — property wins
```

### 2. Method Rebinding

Methods can be overridden per-instance:

```python
class Example:
    def method(self):
        return "class method"

obj1 = Example()
obj2 = Example()

# Override just for obj1
obj1.method = lambda: "custom method"

print(obj1.method())  # "custom method"
print(obj2.method())  # "class method"
```

### 3. Caching Pattern

Non-data descriptors enable caching:

```python
class cached_property:
    """Computes once, then replaces itself"""
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Compute value
        value = self.func(instance)
        # Replace descriptor with value in instance dict
        instance.__dict__[self.func.__name__] = value
        return value

class Expensive:
    @cached_property
    def data(self):
        print("Computing...")
        return [1, 2, 3, 4, 5]

obj = Expensive()
print(obj.data)  # Computing... [1, 2, 3, 4, 5]
print(obj.data)  # [1, 2, 3, 4, 5] (from __dict__, no computing)
```

## Making Descriptors Data

### 1. Add Empty __set__

```python
class BecomeData:
    def __get__(self, instance, owner):
        return "value"
    
    def __set__(self, instance, value):
        # Even if empty, makes it data descriptor
        raise AttributeError("Read-only")

class Example:
    attr = BecomeData()

obj = Example()
obj.__dict__['attr'] = "won't work"
print(obj.attr)  # "value" (descriptor wins)
```

### 2. Add __delete__

```python
class AlsoData:
    def __get__(self, instance, owner):
        return "value"
    
    def __delete__(self, instance):
        # Having __delete__ also makes it data descriptor
        raise AttributeError("Cannot delete")
```

### 3. Comparison

```python
# Non-data (only __get__)
class NonData:
    def __get__(self, instance, owner):
        return "non-data"

# Data (__get__ + __set__)
class Data1:
    def __get__(self, instance, owner):
        return "data"
    def __set__(self, instance, value):
        pass

# Data (__get__ + __delete__)
class Data2:
    def __get__(self, instance, owner):
        return "data"
    def __delete__(self, instance):
        pass

# Data (__get__ + __set__ + __delete__)
class Data3:
    def __get__(self, instance, owner):
        return "data"
    def __set__(self, instance, value):
        pass
    def __delete__(self, instance):
        pass
```

## Practical Implications

### 1. Validation Requires Data

```python
class ValidatedAge:
    """Must be data descriptor to validate"""
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get('_age', 0)
    
    def __set__(self, instance, value):
        if not 0 <= value <= 150:
            raise ValueError("Invalid age")
        instance.__dict__['_age'] = value

class Person:
    age = ValidatedAge()

p = Person()
p.age = 30  # ✅ Validated
# p.__dict__['_age'] = 200  # ⚠️ Bypasses validation!
# But: p.age still goes through descriptor
```

### 2. Computed Without Caching

```python
class AlwaysComputed:
    """Data descriptor - always computes"""
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.func(instance)
    
    def __set__(self, instance, value):
        raise AttributeError("Read-only computed property")

class Rectangle:
    @AlwaysComputed
    def area(self):
        print("Computing area")
        return self.width * self.height

# Computes every time
r = Rectangle()
r.width, r.height = 5, 10
print(r.area)  # Computing area... 50
print(r.area)  # Computing area... 50 (not cached)
```

### 3. Cached with Non-Data

```python
class CachedProperty:
    """Non-data descriptor - caches by self-replacement"""
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.func(instance)
        # Store in instance dict - becomes regular attribute
        setattr(instance, self.func.__name__, value)
        return value

class Rectangle:
    @CachedProperty
    def area(self):
        print("Computing area")
        return self.width * self.height

r = Rectangle()
r.width, r.height = 5, 10
print(r.area)  # Computing area... 50
print(r.area)  # 50 (from __dict__, cached)
```

## Testing Descriptor Type

### 1. Check Methods

```python
def is_data_descriptor(obj):
    """Check if object is a data descriptor"""
    return (hasattr(obj, '__set__') or hasattr(obj, '__delete__'))

def is_non_data_descriptor(obj):
    """Check if object is non-data descriptor"""
    return hasattr(obj, '__get__') and not is_data_descriptor(obj)

# Test
class DataDesc:
    def __get__(self, instance, owner): pass
    def __set__(self, instance, value): pass

class NonDataDesc:
    def __get__(self, instance, owner): pass

print(is_data_descriptor(DataDesc()))      # True
print(is_non_data_descriptor(NonDataDesc()))  # True
```

### 2. Inspect Property

```python
class Example:
    @property
    def read_only(self):
        return 42
    
    @property
    def read_write(self):
        return self._value
    
    @read_write.setter
    def read_write(self, value):
        self._value = value

# Check types
ro = type(Example.read_only)
rw = type(Example.read_write)

print(hasattr(Example.read_only, '__set__'))    # True (property always has __set__)
print(hasattr(Example.read_write, '__set__'))   # True (data)
```

## Summary Table

### 1. Type Characteristics

| Type | Has __get__ | Has __set__ or __delete__ | Priority |
|------|-------------|--------------------------|----------|
| Data | Yes | Yes | Before instance dict |
| Non-data | Yes | No | After instance dict |

### 2. Common Examples

| Example | Type | Reason |
|---------|------|--------|
| `@property` with setter | Data | Has `__set__` |
| `@property` without setter | Data | Has `__set__` (raises `AttributeError`) |
| Methods | Non-data | Only `__get__` |
| `@classmethod` | Non-data | Only `__get__` |
| `@staticmethod` | Non-data | Only `__get__` |
| `@functools.cached_property` | Non-data | Only `__get__` |

### 3. Use Cases

| Need | Use |
|------|-----|
| Validation | Data descriptor |
| Computed property | Either (depends on caching) |
| Caching with replacement | Non-data descriptor |
| Always compute fresh | Data descriptor |
| Method-like behavior | Non-data descriptor |

!!! tip "Rule of Thumb"
    **Need control?** → data descriptor (intercepts every access)
    **Need override/caching?** → non-data descriptor (instance `__dict__` can take over)

---

## Runnable Example: `descriptor_kinds_demo.py`

```python
"""
TUTORIAL: Data vs Non-Data Descriptors - The Descriptor Protocol

This advanced tutorial teaches you about Python's descriptor protocol using
__get__ and __set__ dunder methods. Descriptors are the mechanism behind
properties, methods, and other magical attribute access in Python.

You'll learn the difference between data descriptors (with __set__) and
non-data descriptors (only __get__), and how Python's attribute lookup
order works.

This is advanced but essential for understanding Python's internals.

Key Learning Goals:
  - Understand the descriptor protocol (__get__ and __set__)
  - Learn the difference between data and non-data descriptors
  - Understand attribute lookup order in Python
  - See how methods work as non-data descriptors
  - Know when to use descriptors
"""

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Descriptors - Data vs Non-Data Descriptors")
    print("=" * 70)

    # ============ EXAMPLE 1: What Are Descriptors? ============
    print("\n# Example 1: Introduction to Descriptors")
    print("=" * 70)

    print("""
    DEFINITION: A descriptor is an object that implements __get__ and/or __set__
    and/or __delete__ dunder methods. When you access an attribute, Python
    checks if it's a descriptor and calls the appropriate method.

    SIMPLE EXAMPLE:
        class Descriptor:
            def __get__(self, obj, objtype=None):
                print("__get__ called!")
                return "descriptor value"

        class MyClass:
            x = Descriptor()

        obj = MyClass()
        obj.x  # Calls Descriptor.__get__()

    IMPORTANT DISTINCTION:

        DATA DESCRIPTOR: Has __set__ (and/or __delete__)
            - Takes priority over instance __dict__
            - Even if instance has an attribute with the same name

        NON-DATA DESCRIPTOR: Only has __get__
            - Instance __dict__ can "shadow" it
            - Instance attribute takes priority
            - Methods are non-data descriptors

    This is why you can't accidentally override instance attributes when
    properties (data descriptors) are used - the property always intercepts.
    """)

    # ============ EXAMPLE 2: Attribute Lookup Order ============
    print("\n# Example 2: Python's Attribute Lookup Order")
    print("=" * 70)

    print("""
    When you access obj.name, Python looks in this order:

        1. DATA DESCRIPTOR on the class and its bases
           (descriptor with __set__)
        2. Instance __dict__
           (attributes specific to this object)
        3. NON-DATA DESCRIPTOR on the class and its bases
           (descriptor with only __get__)
        4. Class attributes that aren't descriptors
        5. __getattr__() if defined

    This order is why data descriptors (like @property) override instance
    attributes. They're checked first!

    Example:
        class Managed:
            x = DataDescriptor()
            y = NonDataDescriptor()
            z = "plain_attribute"

        obj = Managed()
        obj.__dict__['x'] = "instance"
        obj.__dict__['y'] = "instance"
        obj.__dict__['z'] = "instance"

        obj.x  # DataDescriptor (lookup #1)
        obj.y  # "instance" (lookup #2 - instance dict wins!)
        obj.z  # "instance" (lookup #2)
    """)

    # ============ EXAMPLE 3: Data Descriptor (with __set__) ============
    print("\n# Example 3: Data Descriptor - Taking Priority")
    print("=" * 70)

    # Helper functions for display
    def cls_name(obj_or_cls):
        cls = type(obj_or_cls)
        if cls is type:
            cls = obj_or_cls
        return cls.__name__.split('.')[-1]


    def display(obj):
        cls = type(obj)
        if cls is type:
            return f'<class {obj.__name__}>'
        elif cls in [type(None), int]:
            return repr(obj)
        else:
            return f'<{cls_name(obj)} object>'


    def print_args(name, *args):
        pseudo_args = ', '.join(display(x) for x in args)
        print(f'-> {cls_name(args[0])}.__{name}__({pseudo_args})')


    class Overriding:
        """
        A data descriptor (has __set__).

        This is a "data descriptor" because it defines __set__.
        It overrides instance attributes - always takes priority.
        """

        def __get__(self, instance, owner):
            print_args('get', self, instance, owner)

        def __set__(self, instance, value):
            print_args('set', self, instance, value)


    class Managed:
        over = Overriding()


    obj = Managed()

    print("Accessing via instance (calls __get__):")
    obj.over
    print()

    print("Accessing via class (calls __get__ with instance=None):")
    Managed.over
    print()

    print("Setting via instance (calls __set__):")
    obj.over = 7
    print()

    print("Accessing again (still calls __get__, not the stored value!):")
    obj.over
    print()

    print("Even if we force a value into __dict__:")
    obj.__dict__['over'] = 8
    print(f"Instance __dict__: {obj.__dict__}")
    print()

    print("The descriptor still wins:")
    obj.over  # Still calls __get__!

    print("""
    WHY: Data descriptors (with __set__) are checked FIRST in attribute
    lookup. They take priority even over instance __dict__. This is how
    @property works - it's a data descriptor.

    Use case: When you want to ensure code always runs (properties,
    validators, computed attributes).
    """)

    # ============ EXAMPLE 4: Non-Data Descriptor (only __get__) ============
    print("\n# Example 4: Non-Data Descriptor - Instance Dict Wins")
    print("=" * 70)


    class NonOverriding:
        """
        A non-data descriptor (only __get__, no __set__).

        Instance __dict__ can "shadow" this descriptor.
        Instance attributes take priority.
        """

        def __get__(self, instance, owner):
            print_args('get', self, instance, owner)


    class Managed:
        non_over = NonOverriding()


    obj = Managed()

    print("Accessing via instance (calls __get__):")
    obj.non_over
    print()

    print("Setting an instance attribute (stores in __dict__):")
    obj.non_over = 7
    print()

    print("Now accessing returns the instance value (no __get__):")
    print(f"obj.non_over = {obj.non_over}")
    print()

    print("Accessing via class still calls __get__:")
    Managed.non_over
    print()

    print("Delete the instance attribute:")
    del obj.non_over
    print()

    print("Now __get__ is called again:")
    obj.non_over

    print("""
    WHY: Non-data descriptors (only __get__) are checked AFTER instance
    __dict__. If instance has an attribute, it wins.

    Use case: Methods are non-data descriptors. That's why you can store
    a different object in instance.__dict__ with the same name.
    """)

    # ============ EXAMPLE 5: Methods Are Non-Data Descriptors ============
    print("\n# Example 5: Methods - The Most Important Non-Data Descriptor")
    print("=" * 70)


    class Demo:
        def method(self):
            print(f"  method() called on {self}")


    obj = Demo()

    print("Accessing a method via instance:")
    print(f"obj.method = {obj.method}")
    print()

    print("Accessing via class:")
    print(f"Demo.method = {Demo.method}")
    print()

    print("Notice the difference:")
    print(f"  obj.method is a BOUND method")
    print(f"  Demo.method is a FUNCTION")
    print()

    print("The function's __get__ descriptor creates the bound method:")
    bound_method = Demo.method.__get__(obj, Demo)
    print(f"Demo.method.__get__(obj, Demo) = {bound_method}")
    print()

    print("Call the bound method:")
    bound_method()
    print()

    print("Call the unbound method via class:")
    print("Demo.method(obj):")
    Demo.method(obj)
    print()

    print("You can override the method in instance __dict__:")
    obj.method = lambda: print("  Overridden method!")
    print(f"obj.method = {obj.method}")
    obj.method()
    print()

    print("""
    WHY: Methods are non-data descriptors. The function object's __get__
    method binds 'self' to create a callable method.

    When you do obj.method, Python:
        1. Looks in instance __dict__ (finds the lambda)
        2. Returns it directly (no descriptor protocol)

    If you hadn't overridden in instance __dict__:
        1. Looks in class (finds the function)
        2. Calls function.__get__(obj, Demo)
        3. Returns a bound method

    This is why you can shadow methods with instance attributes!
    """)

    # ============ EXAMPLE 6: Practical Data Descriptor - Validator ============
    print("\n# Example 6: Practical Use - Validator Descriptor")
    print("=" * 70)


    class ValidatedAttribute:
        """
        A data descriptor that validates values.

        Practical example of when you'd use __get__ and __set__.
        """

        def __init__(self, name, validator=None):
            self.name = name
            self.validator = validator or (lambda x: True)

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self  # Accessed from class, return descriptor itself
            return obj.__dict__.get(self.name, None)

        def __set__(self, obj, value):
            if not self.validator(value):
                raise ValueError(f"{self.name} validation failed for {value}")
            obj.__dict__[self.name] = value


    class User:
        # Use descriptors for validated attributes
        name = ValidatedAttribute('name', lambda x: isinstance(x, str) and len(x) > 0)
        age = ValidatedAttribute('age', lambda x: isinstance(x, int) and 0 <= x <= 150)


    user = User()

    print("Setting valid values:")
    user.name = "Alice"
    user.age = 30
    print(f"user.name = {user.name}")
    print(f"user.age = {user.age}")
    print()

    print("Trying invalid value:")
    try:
        user.age = 200
    except ValueError as e:
        print(f"Error: {e}")

    print()
    print("""
    WHY: Data descriptors like ValidatedAttribute let you:
        - Run code on every attribute access
        - Validate values transparently
        - Store computed properties
        - Enforce constraints

    This is the foundation for ORM frameworks (SQLAlchemy, Django ORM).
    They use descriptors to track column values and changes.
    """)

    # ============ EXAMPLE 7: Summary ============
    print("\n# Example 7: Descriptor Hierarchy Summary")
    print("=" * 70)

    print("""
    DATA DESCRIPTOR (has __set__ and/or __delete__):
      - Priority: before instance __dict__
      - Examples: @property with setter, validators
      - obj.__dict__['x'] = 5 gets ignored — descriptor wins

    NON-DATA DESCRIPTOR (only __get__):
      - Priority: after instance __dict__
      - Examples: methods, lazy-loading
      - obj.__dict__['method'] = func — instance wins

    LOOKUP ORDER: data descriptor > instance __dict__ > non-data descriptor
    """)

    # ============ EXAMPLE 8: Advanced Pattern - Lazy Loading ============
    print("\n# Example 8: Advanced Pattern - Lazy Loading with Descriptors")
    print("=" * 70)


    class LazyAttribute:
        """
        Descriptor that loads a value only on first access.

        Useful for expensive computations or resources.
        """

        def __init__(self, loader_func):
            self.loader_func = loader_func

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self
            # First access: compute and store
            # Subsequent: return stored value
            name = self.loader_func.__name__
            value = obj.__dict__.get(name)
            if value is None:
                print(f"  [Loading {name}...]")
                value = self.loader_func(obj)
                obj.__dict__[name] = value
            return value


    class WebPage:
        def __init__(self, url):
            self.url = url

        @LazyAttribute
        def content(self):
            """Simulate downloading page content."""
            print(f"    Downloading from {self.url}")
            return f"Content from {self.url}"


    page = WebPage("https://example.com")

    print("First access (loads):")
    print(page.content)
    print()

    print("Second access (cached):")
    print(page.content)

    print("""
    WHY: Lazy-loading with descriptors:
        - Defers expensive work until needed
        - Transparent to caller (looks like normal attribute)
        - Works seamlessly with ORM frameworks
        - More efficient than computing everything upfront
    """)

    # ============ EXAMPLE 9: Quick Reference ============
    print("\n# Example 9: Quick Reference")
    print("=" * 70)

    print("""
    PROTOCOL METHODS:
      __get__(self, instance, owner)  — attribute read
      __set__(self, instance, value)  — attribute write (makes it data)
      __delete__(self, instance)      — attribute delete (makes it data)

    WHEN TO USE DESCRIPTORS:
      DO:  validation, computed/cached properties, ORM mappings, lazy-loading
      DON'T: simple getter/setter (use @property), performance-critical loops
    """)

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
    1. Data descriptors (__set__) override instance __dict__; non-data don't.
    2. Properties, methods, classmethod, staticmethod — all use descriptors.
    3. The lookup order (data desc > instance > non-data desc) explains why
       properties can't be shadowed but methods can.
    4. Use @property for simple cases; write custom descriptors for reusable
       validation, caching, or ORM-style patterns.
    """)
```

---

## Exercises

**Exercise 1.**
Create a data descriptor `Validated` (implements both `__get__` and `__set__`) and a non-data descriptor `DefaultValue` (implements only `__get__`). Apply both to a class. Show that the data descriptor takes priority over instance `__dict__`, while the non-data descriptor can be overridden by an instance attribute.

??? success "Solution to Exercise 1"

        class Validated:  # Data descriptor
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return obj.__dict__.get(self.name, 0)

            def __set__(self, obj, value):
                if value < 0:
                    raise ValueError("Must be non-negative")
                obj.__dict__[self.name] = value

        class DefaultValue:  # Non-data descriptor
            def __init__(self, default):
                self.default = default

            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return obj.__dict__.get(self.name, self.default)

        class Demo:
            score = Validated()
            label = DefaultValue("unknown")

        d = Demo()
        d.score = 10
        print(d.score)  # 10 — data descriptor intercepts

        d.__dict__['score'] = -5  # Bypass descriptor
        print(d.score)  # -5? No: data descriptor __get__ reads from __dict__
        # Actually returns -5 since our __get__ reads __dict__

        d.__dict__['label'] = "custom"
        print(d.label)  # "custom" — instance overrides non-data descriptor

---

**Exercise 2.**
Write a non-data descriptor `LazyProperty` that computes a value on first access and stores it in the instance `__dict__` so subsequent accesses bypass the descriptor. Compare this behavior with a data descriptor that always intercepts access. Show the difference in access counts.

??? success "Solution to Exercise 2"

        class LazyProperty:
            """Non-data descriptor that caches on first access."""
            def __init__(self, func):
                self.func = func

            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                print(f"Computing {self.name}...")
                value = self.func(obj)
                obj.__dict__[self.name] = value  # Cache in instance
                return value

        class Circle:
            def __init__(self, radius):
                self.radius = radius

            @LazyProperty
            def area(self):
                import math
                return math.pi * self.radius ** 2

        c = Circle(5)
        print(c.area)  # "Computing area..." then 78.54
        print(c.area)  # 78.54 — cached, no "Computing" message

---

**Exercise 3.**
Demonstrate the lookup priority by creating a class with: (a) a data descriptor `x`, (b) an instance attribute `x` (set via `__dict__`), and (c) a non-data descriptor `y` and instance attribute `y`. Show that `obj.x` returns the data descriptor's value (not the instance attribute) while `obj.y` returns the instance attribute (not the non-data descriptor's value).

??? success "Solution to Exercise 3"

        class DataDesc:
            """Data descriptor — has __get__ and __set__."""
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return f"data_descriptor({self.name})"

            def __set__(self, obj, value):
                pass  # Intercepts but does nothing

        class NonDataDesc:
            """Non-data descriptor — has only __get__."""
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return f"non_data_descriptor({self.name})"

        class Demo:
            x = DataDesc()
            y = NonDataDesc()

        d = Demo()
        d.__dict__['x'] = "instance_x"
        d.__dict__['y'] = "instance_y"

        print(d.x)  # "data_descriptor(x)" — data descriptor wins
        print(d.y)  # "instance_y" — instance wins over non-data descriptor
