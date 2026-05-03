# __get__ __set__ __delete__

!!! tip "Mental Model"
    The three descriptor methods are **interceptors on the attribute access pipeline**. `__get__` intercepts reads, `__set__` intercepts writes, `__delete__` intercepts deletions. Each gives the descriptor full control over what happens — it can validate, transform, compute, cache, or deny the operation entirely.

## The Three Methods

### 1. Method Signatures

```python
class Descriptor:
    def __get__(self, instance, owner):
        """Called on attribute read"""
        pass
    
    def __set__(self, instance, value):
        """Called on attribute write"""
        pass
    
    def __delete__(self, instance):
        """Called on attribute deletion"""
        pass
```

### 2. Parameters

**`__get__(self, instance, owner)`:**
- `self` - the descriptor object itself
- `instance` - the instance being accessed (`None` if accessed from class)
- `owner` - the class that owns the descriptor

**`__set__(self, instance, value)`:**
- `self` - the descriptor object itself
- `instance` - the instance being modified
- `value` - the value being assigned

**`__delete__(self, instance)`:**
- `self` - the descriptor object itself
- `instance` - the instance where attribute is being deleted

### 3. When They're Called

```python
obj.attr        # → __get__(descriptor, obj, type(obj))
obj.attr = val  # → __set__(descriptor, obj, val)
del obj.attr    # → __delete__(descriptor, obj)

Class.attr      # → __get__(descriptor, None, Class)
```

## __get__ Method

### 1. Basic Implementation

```python
class GetDescriptor:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        print(f"__get__ called")
        print(f"  self = {self}")
        print(f"  instance = {instance}")
        print(f"  owner = {owner}")
        
        if instance is None:
            return self  # Accessed from class
        
        return instance.__dict__.get(self.name, "default")

class MyClass:
    attr = GetDescriptor('attr')

# Access from class
print(MyClass.attr)
# __get__ called
#   self = <GetDescriptor object>
#   instance = None
#   owner = <class 'MyClass'>

# Access from instance
obj = MyClass()
obj.attr = 42
print(obj.attr)
# __get__ called
#   self = <GetDescriptor object>
#   instance = <MyClass object>
#   owner = <class 'MyClass'>
# 42
```

### 2. Handling Class vs Instance

```python
class SmartGetter:
    def __init__(self, value):
        self.value = value
    
    def __get__(self, instance, owner):
        if instance is None:
            # Accessed from class - return descriptor
            return self
        # Accessed from instance - return value
        return self.value

class Example:
    x = SmartGetter(42)

print(Example.x)      # <SmartGetter object>
print(Example().x)    # 42
```

### 3. Computed Values

```python
class ComputedProperty:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.func(instance)

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @ComputedProperty
    def area(self):
        from math import pi
        return pi * self.radius ** 2

c = Circle(5)
print(c.area)  # 78.54... (computed each time)
```

## __set__ Method

### 1. Basic Implementation

```python
class SetDescriptor:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        print(f"__set__ called")
        print(f"  self = {self}")
        print(f"  instance = {instance}")
        print(f"  value = {value}")
        
        instance.__dict__[self.name] = value

class MyClass:
    attr = SetDescriptor('attr')

obj = MyClass()
obj.attr = 42
# __set__ called
#   self = <SetDescriptor object>
#   instance = <MyClass object>
#   value = 42
```

### 2. Validation

```python
class ValidatedDescriptor:
    def __init__(self, name, validator):
        self.name = name
        self.validator = validator
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        instance.__dict__[self.name] = value

class Person:
    age = ValidatedDescriptor('age', lambda x: 0 <= x <= 150)
    name = ValidatedDescriptor('name', lambda x: len(x) > 0)

p = Person()
p.age = 30      # ✅ OK
# p.age = 200   # ❌ ValueError
p.name = "Alice"  # ✅ OK
# p.name = ""   # ❌ ValueError
```

### 3. Type Enforcement

```python
class TypedDescriptor:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        instance.__dict__[self.name] = value

class Product:
    name = TypedDescriptor('name', str)
    price = TypedDescriptor('price', (int, float))
    quantity = TypedDescriptor('quantity', int)

prod = Product()
prod.name = "Widget"   # ✅ OK
prod.price = 19.99     # ✅ OK
# prod.name = 123      # ❌ TypeError
```

## __delete__ Method

### 1. Basic Implementation

```python
class DeleteDescriptor:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        print(f"__delete__ called")
        print(f"  self = {self}")
        print(f"  instance = {instance}")
        
        del instance.__dict__[self.name]

class MyClass:
    attr = DeleteDescriptor('attr')

obj = MyClass()
obj.attr = 42
del obj.attr
# __delete__ called
#   self = <DeleteDescriptor object>
#   instance = <MyClass object>
```

### 2. Protected Deletion

```python
class ProtectedDescriptor:
    def __init__(self, name, deletable=True):
        self.name = name
        self.deletable = deletable
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        if not self.deletable:
            raise AttributeError(f"Cannot delete {self.name}")
        del instance.__dict__[self.name]

class Person:
    id = ProtectedDescriptor('id', deletable=False)
    name = ProtectedDescriptor('name', deletable=True)

p = Person()
p.id = 123
p.name = "Alice"

del p.name  # ✅ OK
# del p.id  # ❌ AttributeError
```

### 3. Cleanup on Delete

```python
class ResourceDescriptor:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        resource = instance.__dict__.get(self.name)
        if resource and hasattr(resource, 'close'):
            print(f"Closing resource: {self.name}")
            resource.close()
        del instance.__dict__[self.name]

class FileHandler:
    file = ResourceDescriptor('file')

handler = FileHandler()
handler.file = open('test.txt', 'w')
del handler.file  # Closes file before deleting
```

## Complete Example

### 1. Full Descriptor

```python
class ManagedAttribute:
    def __init__(self, name, validator=None, default=None):
        self.name = name
        self.validator = validator
        self.default = default
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, self.default)
    
    def __set__(self, instance, value):
        if self.validator and not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

class Person:
    name = ManagedAttribute(
        'name',
        validator=lambda x: isinstance(x, str) and len(x) > 0
    )
    age = ManagedAttribute(
        'age',
        validator=lambda x: isinstance(x, int) and 0 <= x <= 150,
        default=0
    )

p = Person()
p.name = "Alice"
p.age = 30
print(p.name, p.age)  # Alice 30

del p.age
print(p.age)  # 0 (default)
```

### 2. With Logging

```python
class LoggedDescriptor:
    def __init__(self, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = instance.__dict__.get(self.name)
        print(f"[GET] {self.name} = {value}")
        return value
    
    def __set__(self, instance, value):
        print(f"[SET] {self.name} = {value}")
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        print(f"[DEL] {self.name}")
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]

class Example:
    x = LoggedDescriptor('x')
    y = LoggedDescriptor('y')

obj = Example()
obj.x = 10      # [SET] x = 10
print(obj.x)    # [GET] x = 10
del obj.x       # [DEL] x
```

### 3. With Caching

```python
class CachedDescriptor:
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Check cache
        cache_name = f'_cached_{self.name}'
        if cache_name not in instance.__dict__:
            # Compute and cache
            value = self.func(instance)
            instance.__dict__[cache_name] = value
        
        return instance.__dict__[cache_name]
    
    def __set__(self, instance, value):
        raise AttributeError("Cannot set computed property")
    
    def __delete__(self, instance):
        # Clear cache
        cache_name = f'_cached_{self.name}'
        if cache_name in instance.__dict__:
            del instance.__dict__[cache_name]

class ExpensiveCalculation:
    def __init__(self, data):
        self.data = data
    
    @CachedDescriptor
    def result(self):
        print("Computing...")
        return sum(x**2 for x in self.data)

obj = ExpensiveCalculation([1, 2, 3, 4, 5])
print(obj.result)  # Computing... 55
print(obj.result)  # 55 (from cache)
del obj.result     # Clear cache
print(obj.result)  # Computing... 55
```

## Method Interaction

### 1. All Three Together

When all three methods are defined, they work together:

```python
obj.attr        # → __get__
obj.attr = val  # → __set__
del obj.attr    # → __delete__
```

### 2. Only Some Defined

You don't need all three:

```python
# Read-only descriptor (no __set__)
class ReadOnly:
    def __get__(self, instance, owner):
        return "constant"

# Write-only descriptor (unusual, but possible)
class WriteOnly:
    def __set__(self, instance, value):
        instance.__dict__['_value'] = value
```

### 3. Call Order

```python
class TrackedDescriptor:
    def __get__(self, instance, owner):
        print("1. __get__")
        return instance.__dict__.get('value', 0)
    
    def __set__(self, instance, value):
        print("2. __set__")
        instance.__dict__['value'] = value
    
    def __delete__(self, instance):
        print("3. __delete__")
        del instance.__dict__['value']

class Example:
    attr = TrackedDescriptor()

obj = Example()
obj.attr = 10   # 2. __set__
x = obj.attr    # 1. __get__
del obj.attr    # 3. __delete__
```

---

## Runnable Example: `method_as_descriptor.py`

```python
"""
TUTORIAL: Methods as Descriptors - Understanding the Descriptor Protocol

This tutorial reveals the magic behind Python methods. Every time you access
a method on an object, Python's descriptor protocol is at work. Functions
are actually non-data descriptors that use __get__ to bind 'self'.

Understanding this explains fundamental Python behavior: why methods work,
why 'self' is implicit, and how you can manipulate methods if needed.

Key Learning Goals:
  - See methods as descriptors (functions with __get__)
  - Understand how 'self' gets bound automatically
  - Learn the difference between bound and unbound methods
  - Understand access via instance vs class
  - See practical uses of this knowledge
"""

import collections

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: Methods as Descriptors - The Function Protocol")
    print("=" * 70)

    # ============ EXAMPLE 1: Functions Are Descriptors ============
    print("\n# Example 1: Functions Implement the Descriptor Protocol")
    print("=" * 70)

    class MyClass:
        """Simple class with a method."""

        def method(self):
            """A simple method."""
            return "method result"


    print("A function object is a descriptor:")
    print(f"type(MyClass.method) = {type(MyClass.method)}")
    print(f"hasattr(function, '__get__') = {hasattr(MyClass.method, '__get__')}")
    print()

    print("When you access via instance, __get__ is called:")
    obj = MyClass()
    print(f"obj.method = {obj.method}")
    print(f"type(obj.method) = {type(obj.method)}")
    print()

    print("When you access via class:")
    print(f"MyClass.method = {MyClass.method}")
    print(f"type(MyClass.method) = {type(MyClass.method)}")
    print()

    print("""
    Functions are non-data descriptors: they have __get__ but not __set__.
    Via instance, __get__ creates a bound method; via class, it returns
    the function itself.
    """)

    # ============ EXAMPLE 2: The Bound Method ============
    print("\n# Example 2: Accessing Methods Creates Bound Methods")
    print("=" * 70)

    class Text(collections.UserString):
        """Text class with a reverse method."""

        def __repr__(self):
            return 'Text({!r})'.format(self.data)

        def reverse(self):
            """Return text reversed."""
            return self[::-1]


    word = Text('forward')

    print(f"Original: {word}")
    print()

    # Access method via instance
    print("Access method via instance:")
    method = word.reverse
    print(f"  word.reverse = {method}")
    print(f"  type = {type(method)}")
    print()

    # Call it
    result = method()
    print(f"  word.reverse() = {result}")
    print()

    # Access method via class
    print("Access method via class:")
    func = Text.reverse
    print(f"  Text.reverse = {func}")
    print(f"  type = {type(func)}")
    print()

    # Call it with instance as argument
    result = func(word)
    print(f"  Text.reverse(word) = {result}")

    print("""
    Bound method (obj.method): carries both function and instance,
    passes instance as 'self' automatically.

    Unbound function (Class.method): just the function — you must
    pass the instance explicitly.
    """)

    # ============ EXAMPLE 3: How __get__ Works ============
    print("\n# Example 3: Calling __get__ Directly")
    print("=" * 70)

    class Demo:
        def method(self):
            return f"method called on {self}"


    obj = Demo()

    print("The __get__ method creates the bound method:")
    print(f"Demo.method.__get__(obj, Demo) = {Demo.method.__get__(obj, Demo)}")
    print()

    print("Calling __get__ with None instance returns unbound:")
    print(f"Demo.method.__get__(None, Demo) = {Demo.method.__get__(None, Demo)}")
    print()

    print("The bound method carries references to function and instance:")
    bound = obj.method
    print(f"bound.__func__ = {bound.__func__}")
    print(f"bound.__self__ = {bound.__self__}")
    print(f"bound.__func__ is Demo.method = {bound.__func__ is Demo.method}")
    print(f"bound.__self__ is obj = {bound.__self__ is obj}")
    print()

    print("You can call the bound method:")
    print(f"bound() = {bound()}")

    print("""
    __func__ holds the actual function, __self__ holds the bound instance.
    Calling the bound method passes __self__ as the first argument.
    """)

    # ============ EXAMPLE 4: Shadowing Methods ============
    print("\n# Example 4: Instance Attributes Shadow Methods")
    print("=" * 70)

    class Shadowing:
        def method(self):
            return "class method"


    obj = Shadowing()

    print("Initially, call the class method:")
    print(f"  obj.method() = {obj.method()}")
    print()

    print("Shadow it with an instance attribute:")
    obj.method = lambda: "instance lambda"
    print(f"  obj.method = {obj.method}")
    print()

    print("Now it calls the instance attribute:")
    print(f"  obj.method() = {obj.method()}")
    print()

    print("Class still has the original:")
    print(f"  Shadowing.method = {Shadowing.method}")
    print(f"  Shadowing.method(obj) = {Shadowing.method(obj)}")
    print()

    print("Delete the instance attribute to restore:")
    del obj.method
    print(f"  obj.method() = {obj.method()}")

    print("""
    Methods are non-data descriptors, so instance __dict__ can shadow them.
    Unlike @property (data descriptor), which always intercepts access.
    """)

    # ============ EXAMPLE 5: Bound Method Equality ============
    print("\n# Example 5: Bound Methods and Equality")
    print("=" * 70)

    class Data:
        def check(self):
            return True


    obj1 = Data()
    obj2 = Data()

    print("Getting the same bound method twice:")
    m1 = obj1.check
    m2 = obj1.check
    print(f"  m1 = obj1.check")
    print(f"  m2 = obj1.check")
    print(f"  m1 == m2 = {m1 == m2}")
    print(f"  m1 is m2 = {m1 is m2}")  # Different objects!
    print()

    print("Bound methods from different instances:")
    m3 = obj1.check
    m4 = obj2.check
    print(f"  m3 = obj1.check")
    print(f"  m4 = obj2.check")
    print(f"  m3 == m4 = {m3 == m4}")
    print(f"  m3.__self__ is m4.__self__ = {m3.__self__ is m4.__self__}")

    print("""
    Bound methods are created fresh on each access via __get__. They compare
    equal if same function + instance, but are not identical objects.
    """)

    # ============ EXAMPLE 6: Using map With Methods ============
    print("\n# Example 6: Practical Use - Applying Methods Across Objects")
    print("=" * 70)

    class Number:
        def __init__(self, value):
            self.value = value

        def squared(self):
            return self.value ** 2

        def __repr__(self):
            return f"Number({self.value})"


    numbers = [Number(1), Number(2), Number(3)]

    print("Using map with a method:")
    print(f"numbers = {numbers}")
    print()

    print("Apply squared() to all:")
    # This works because the unbound method can take any instance
    results = list(map(Number.squared, numbers))
    print(f"map(Number.squared, numbers) = {results}")
    print()

    print("""
    WHY: This works because:
        - Number.squared is the unbound function
        - map passes each number as the first argument
        - The function is called as Number.squared(number)

    You could also do:
        results = [num.squared() for num in numbers]

    But using the unbound method is more elegant in some cases.
    """)

    # ============ EXAMPLE 7: Staticmethod and Classmethod ============
    print("\n# Example 7: Other Descriptor Types - staticmethod and classmethod")
    print("=" * 70)

    class Demo:
        @staticmethod
        def static():
            """Static methods don't get 'self' or 'cls' binding."""
            return "static result"

        @classmethod
        def cls_method(cls):
            """Class methods get 'cls' as first argument."""
            return f"class method from {cls.__name__}"

        def instance_method(self):
            """Normal methods get 'self'."""
            return "instance method"


    print("Instance method (normal):")
    print(f"  Demo.instance_method = {Demo.instance_method}")
    print()

    print("Class method (bound to class):")
    print(f"  Demo.cls_method = {Demo.cls_method}")
    print(f"  Demo.cls_method() = {Demo.cls_method()}")
    print()

    print("Static method (no binding):")
    print(f"  Demo.static = {Demo.static}")
    print(f"  Demo.static() = {Demo.static()}")
    print()

    print("All are descriptors but work differently:")
    obj = Demo()
    print(f"obj.instance_method() = {obj.instance_method()}")
    print(f"obj.cls_method() = {obj.cls_method()}")
    print(f"obj.static() = {obj.static()}")

    print("""
    Three method types, all using the descriptor protocol:
      Instance method: __get__ binds self
      Class method:    __get__ binds cls
      Static method:   wraps function, no binding
    """)

    # ============ EXAMPLE 8: Custom Descriptor Mimicking Methods ============
    print("\n# Example 8: Building a Method-Like Descriptor")
    print("=" * 70)

    class MethodLike:
        """Descriptor that mimics method behavior."""

        def __init__(self, func):
            self.func = func

        def __get__(self, obj, objtype=None):
            if obj is None:
                return self.func  # Accessed from class
            # Create a bound method-like object
            return lambda *args, **kwargs: self.func(obj, *args, **kwargs)


    class MyClass:
        @MethodLike
        def my_method(self):
            return f"Called on {self}"


    obj = MyClass()

    print("Using the descriptor:")
    print(f"MyClass.my_method = {MyClass.my_method}")
    print(f"obj.my_method = {obj.my_method}")
    print()

    print("Calling the bound version:")
    result = obj.my_method()
    print(f"obj.my_method() = {result}")
    print()

    print("""
    This shows how __get__ can return different things based on context.
    In practice, use regular methods — this is for understanding the mechanism.
    """)

    # ============ EXAMPLE 9: Summary ============
    print("\n# Example 9: How Methods Work — Summary")
    print("=" * 70)

    print("""
    THE METHOD MECHANISM:

    obj.method access:
      1. Look up 'method' in obj.__dict__ (not found)
      2. Find function in class.__dict__
      3. Call function.__get__(obj, MyClass) — creates bound method
      4. Bound method passes obj as 'self' when called

    KEY POINTS:
      - Functions are non-data descriptors (have __get__, not __set__)
      - Instance __dict__ can shadow methods
      - Same mechanism powers @property, @staticmethod, @classmethod
      - Each access creates a fresh bound method (Python optimizes this)
    """)
```

---

## Exercises

**Exercise 1.**
Create a descriptor `ValidatedString` that implements `__get__`, `__set__`, and `__delete__`. On `__set__`, ensure the value is a non-empty string. On `__delete__`, set the value to `None` instead of removing it. Use `__set_name__` to store the attribute name automatically. Demonstrate all three operations.

??? success "Solution to Exercise 1"

        class ValidatedString:
            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return obj.__dict__.get(self.name)

            def __set__(self, obj, value):
                if not isinstance(value, str) or not value:
                    raise ValueError(f"{self.name} must be a non-empty string")
                obj.__dict__[self.name] = value

            def __delete__(self, obj):
                obj.__dict__[self.name] = None

        class Profile:
            bio = ValidatedString()

            def __init__(self, bio):
                self.bio = bio

        p = Profile("Hello world")
        print(p.bio)  # Hello world

        del p.bio
        print(p.bio)  # None (not removed, just set to None)

        try:
            p.bio = ""
        except ValueError as e:
            print(f"Error: {e}")

---

**Exercise 2.**
Write a descriptor `Counter` that tracks how many times an attribute has been set. Implement `__get__` to return a tuple of `(current_value, set_count)`. Implement `__set__` to update the value and increment the count. Apply it to a `Sensor` class with a `reading` field. Show the count increasing with each assignment.

??? success "Solution to Exercise 2"

        class Counter:
            def __set_name__(self, owner, name):
                self.name = name
                self.count_name = f"_{name}_count"

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                value = obj.__dict__.get(self.name)
                count = obj.__dict__.get(self.count_name, 0)
                return (value, count)

            def __set__(self, obj, value):
                obj.__dict__[self.name] = value
                obj.__dict__[self.count_name] = obj.__dict__.get(self.count_name, 0) + 1

        class Sensor:
            reading = Counter()

            def __init__(self, initial):
                self.reading = initial

        s = Sensor(10.5)
        print(s.reading)  # (10.5, 1)

        s.reading = 20.3
        print(s.reading)  # (20.3, 2)

        s.reading = 15.0
        print(s.reading)  # (15.0, 3)

---

**Exercise 3.**
Implement a `Transformer` descriptor that accepts a transform function in its `__init__`. On `__set__`, it applies the transform before storing. On `__get__`, it returns the stored value. Create a `Record` class using `Transformer(str.strip)` for `name` and `Transformer(float)` for `value`. Show that values are automatically transformed on assignment.

??? success "Solution to Exercise 3"

        class Transformer:
            def __init__(self, func):
                self.func = func

            def __set_name__(self, owner, name):
                self.name = name

            def __get__(self, obj, objtype=None):
                if obj is None:
                    return self
                return obj.__dict__.get(self.name)

            def __set__(self, obj, value):
                obj.__dict__[self.name] = self.func(value)

        class Record:
            name = Transformer(str.strip)
            value = Transformer(float)

            def __init__(self, name, value):
                self.name = name
                self.value = value

        r = Record("  Alice  ", "42")
        print(r.name)   # "Alice" (stripped)
        print(r.value)  # 42.0 (converted to float)

        r.value = "99.5"
        print(r.value)  # 99.5
