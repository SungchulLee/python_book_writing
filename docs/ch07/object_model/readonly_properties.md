# Read-Only Properties

## Creating Read-Only

### 1. Property Without Setter

The simplest way to create a read-only property is to define only the getter:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def area(self):
        from math import pi
        return pi * self._radius ** 2
```

### 2. Attempting to Write

```python
c = Circle(5)
print(c.area)  # ✅ Works: 78.54...
c.area = 100   # ❌ AttributeError: can't set attribute
```

### 3. Why Use Read-Only

- Prevent accidental modification of computed values
- Enforce immutability for specific attributes
- Maintain data consistency
- Express design intent clearly

### 4. Caveat: `__dict__` Override

Because `property` is a data descriptor, assigning `obj.area = 100` triggers the setter (or raises `AttributeError` if there is none). However, writing directly to `obj.__dict__['area'] = 100` bypasses the descriptor entirely and creates an instance attribute. This shadowed value is never returned because the data descriptor takes priority, but it can cause confusion. Avoid manipulating `__dict__` directly for property-controlled attributes. For more on how this works, see [Properties as Descriptors](property_descriptor_connection.md).

!!! warning "Why Properties Enforce Control"
    Properties work because they are **data descriptors** — they define both `__get__` and `__set__` (even if the setter raises `AttributeError`). Data descriptors are checked **before** the instance `__dict__` during attribute lookup. This is why `obj.area = 100` triggers the property's setter instead of creating an instance attribute — the descriptor intercepts the write at a higher priority level. Without this mechanism, any assignment would bypass property logic entirely.

## Common Patterns

### 1. Computed Values

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

### 2. Derived Attributes

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

### 3. Configuration Values

```python
class Config:
    def __init__(self):
        self._api_key = "secret123"
    
    @property
    def api_endpoint(self):
        return "https://api.example.com/v1"
    
    @property
    def max_retries(self):
        return 3
```

## Protecting Internal State

### 1. Private Attribute Pattern

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance
    
    @property
    def balance(self):
        """Read-only access to balance"""
        return self._balance
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
    
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
```

### 2. Why This Works

- `_balance` is private (convention)
- `balance` property provides read-only access
- Modifications only through controlled methods
- Maintains invariants

### 3. Usage Example

```python
account = BankAccount(1000)
print(account.balance)  # ✅ 1000
account.deposit(500)    # ✅ Works
# account.balance = 5000  # ❌ Can't set attribute
```

## Immutable Objects

### 1. Full Immutability

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
```

### 2. Benefits

- Thread-safe by design
- Can be used as dictionary keys
- Easier to reason about
- Prevents bugs from state mutation

### 3. Creating New Instances

```python
class Point:
    # ... (properties as above)
    
    def move(self, dx, dy):
        """Returns new Point with offset"""
        return Point(self._x + dx, self._y + dy)
```

## Advanced Patterns

### 1. Conditional Read-Only

Make property read-only based on state:

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

### 2. Lazy Evaluation

This is a manual version of a cached property. For a reusable descriptor-based implementation, see [Cached Properties](cached_property.md).

```python
class ExpensiveCalculation:
    def __init__(self, data):
        self._data = data
        self._result = None
    
    @property
    def result(self):
        """Computed once, then cached"""
        if self._result is None:
            print("Computing...")
            self._result = sum(x**2 for x in self._data)
        return self._result
```

### 3. Type Conversion

```python
class DataRecord:
    def __init__(self, timestamp_str):
        self._timestamp_str = timestamp_str
    
    @property
    def timestamp(self):
        """Always returns datetime object"""
        from datetime import datetime
        return datetime.fromisoformat(self._timestamp_str)
```

## Comparison

### 1. Read-Only vs Writable

| Aspect | Read-Only Property | Writable Property |
|--------|-------------------|-------------------|
| Setter | Not defined | Defined |
| Assignment | Raises error | Allowed |
| Use case | Computed/protected values | Validated attributes |
| Mutability | Immutable | Mutable |

### 2. Enforcement Levels

| Method | Enforcement | Access |
|--------|-------------|--------|
| Public attribute | None | `obj.x = 5` works |
| `_private` convention | Social | `obj._x = 5` discouraged |
| Read-only property | Strong | `obj.x = 5` raises error |

### 3. Design Principles

**Use read-only properties when:**
- Value is derived from other state
- External modification would break invariants
- Expressing configuration or constants
- Implementing immutable data structures

---

## Exercises

**Exercise 1.** Create an immutable `Point` class with read-only `x` and `y` properties and a read-only `distance_from_origin` property that computes $\sqrt{x^2 + y^2}$. Show that attempting to set `x` or `y` raises an error.

??? success "Solution to Exercise 1"
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

**Exercise 2.** Predict the output of the following code:

```python
class Config:
    @property
    def max_retries(self):
        return 3

c = Config()
print(c.max_retries)

try:
    c.max_retries = 5
except AttributeError:
    print("Cannot modify")
```

??? success "Solution to Exercise 2"
    The output is:

    ```
    3
    Cannot modify
    ```

    `max_retries` is a read-only property (no setter defined). Reading it returns `3`. Attempting to assign a new value raises `AttributeError`.

---

**Exercise 3.** Write a `Student` class with `first_name` and `last_name` as regular attributes, and read-only properties `full_name` and `email` (computed as `first_last@school.edu` in lowercase). Show that changing `first_name` automatically updates both derived properties.

??? success "Solution to Exercise 3"
    ```python
    class Student:
        def __init__(self, first_name, last_name):
            self.first_name = first_name
            self.last_name = last_name

        @property
        def full_name(self):
            return f"{self.first_name} {self.last_name}"

        @property
        def email(self):
            return f"{self.first_name}_{self.last_name}@school.edu".lower()

    s = Student("Alice", "Smith")
    print(s.full_name)  # Alice Smith
    print(s.email)      # alice_smith@school.edu

    s.first_name = "Bob"
    print(s.full_name)  # Bob Smith
    print(s.email)      # bob_smith@school.edu
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

**Exercise 5.** Create an `ExpensiveResult` class with a lazy read-only property `result` that computes the sum of squares from 1 to 100,000 on first access and caches it. Show that the computation runs only once.

??? success "Solution to Exercise 5"
    ```python
    class ExpensiveResult:
        def __init__(self):
            self._result = None

        @property
        def result(self):
            if self._result is None:
                print("Computing...")
                self._result = sum(i ** 2 for i in range(1, 100_001))
            return self._result

    er = ExpensiveResult()
    print(er.result)  # Computing... 333338333350000
    print(er.result)  # 333338333350000 (no recomputation)
    ```
