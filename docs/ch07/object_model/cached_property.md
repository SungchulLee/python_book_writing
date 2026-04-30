# Cached Properties

## Concept

### 1. What Is Caching?

A **cached property** computes its value **once** on first access, stores the result inside the instance (usually in `__dict__`), and on future accesses, just returns the cached value — skipping recomputation.

### 2. When to Use

Use cached properties when:

- Computation is expensive (database queries, heavy calculations)
- Result doesn't change after first computation
- Want to trade memory for speed
- Need lazy evaluation

### 3. Built-in vs Custom

- **Python ≥ 3.8**: `@functools.cached_property`
- **Custom**: Build your own using descriptors

!!! note "Relationship to property"
    `cached_property` is a **non-data descriptor** — it defines `__get__` but not `__set__`. On first access, `__get__` computes the value and stores it directly in the instance's `__dict__`. On subsequent accesses, the instance `__dict__` entry is found before the descriptor (because non-data descriptors have lower priority), so the cached value is returned without calling `__get__` again. This is the opposite of `@property`, which is a **data descriptor** that always intercepts access.

## Custom Implementation

### 1. Descriptor Class

```python
class CachedProperty:
    def __init__(self, func):
        self.func = func
        self.__doc__ = func.__doc__
        self.name = func.__name__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.name not in instance.__dict__:
            print(f"Computing and caching: {self.name}")
            instance.__dict__[self.name] = self.func(instance)
        else:
            print(f"Using cached value: {self.name}")
        return instance.__dict__[self.name]
```

### 2. Using Custom Descriptor

```python
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @CachedProperty
    def area(self):
        print("Calculating area...")
        return math.pi * self.radius ** 2

    @CachedProperty
    def perimeter(self):
        print("Calculating perimeter...")
        return 2 * math.pi * self.radius
```

### 3. Behavior Example

```python
c = Circle(10)

print(c.area)      # → Calculates and caches
# Output: Computing and caching: area
#         Calculating area...
#         314.159...

print(c.area)      # → Uses cached value
# Output: Using cached value: area
#         314.159...
```

## How It Works

### 1. Initialization

When you decorate:

```python
@CachedProperty
def area(self):
    ...
```

You are doing at class definition time:

```python
Circle.area = CachedProperty(area)
```

The `CachedProperty.__init__` stores:
- `self.func = area` → original method
- `self.__doc__ = area.__doc__` → docstring
- `self.name = 'area'` → attribute name

### 2. First Access

When you do `c.area`, Python calls:

```python
Circle.area.__get__(c, Circle)
```

Inside `__get__`:

1. Check if `instance is None` (class access) → return descriptor
2. Check if `'area'` in `instance.__dict__` → not yet
3. Compute: `instance.__dict__['area'] = self.func(instance)`
4. Return cached value

### 3. Subsequent Access

When you do `c.area` again:

1. Check if `instance is None` → no
2. Check if `'area'` in `instance.__dict__` → **yes, found!**
3. Skip computation, return cached value directly

After the first access, the descriptor is no longer involved. The value is returned directly from `instance.__dict__` because instance `__dict__` entries take priority over non-data descriptors in Python's attribute lookup. Deleting the cached attribute (`del c.area`) removes the `__dict__` entry, causing the descriptor to run again on next access.

## Built-in Version

### 1. Using functools

Python 3.8+ provides built-in cached property:

```python
from functools import cached_property

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @cached_property
    def area(self):
        print("Computing area...")
        return math.pi * self.radius ** 2
```

### 2. Behavior

```python
c = Circle(10)
print(c.area)  # Computing area... 314.159...
print(c.area)  # 314.159... (no recomputation)
```

### 3. Clearing Cache

To clear cached value:

```python
del c.area  # Remove from instance.__dict__
print(c.area)  # Recomputes
```

## Practical Examples

### 1. Database Query

```python
class User:
    def __init__(self, user_id):
        self.user_id = user_id
    
    @cached_property
    def profile(self):
        print(f"Fetching profile for user {self.user_id}...")
        # Expensive database query
        return db.query(f"SELECT * FROM users WHERE id={self.user_id}")
```

### 2. File Reading

```python
class ConfigFile:
    def __init__(self, path):
        self.path = path
    
    @cached_property
    def data(self):
        print(f"Reading {self.path}...")
        with open(self.path) as f:
            return f.read()
```

### 3. Complex Computation

```python
class Matrix:
    def __init__(self, data):
        self.data = data
    
    @cached_property
    def determinant(self):
        print("Computing determinant...")
        # Expensive calculation
        return self._compute_determinant()
```

## Comparison Table

### 1. Property vs Cached Property

| Feature | `@property` | `@cached_property` |
|---------|-------------|-------------------|
| Computation | Every access | Once on first access |
| Storage | Not stored | Stored in `__dict__` |
| Speed | Slower | Faster after first |
| Memory | Less | More |
| Use case | Dynamic values | Static expensive values |

### 2. When to Choose

**Use `@property` when:**
- Value changes over time
- Computation is cheap
- Need fresh value each time

**Use `@cached_property` when:**
- Value is constant after creation
- Computation is expensive
- Multiple accesses expected

### 3. When NOT to Use `@cached_property`

- **Mutable underlying state**: if the attributes the cached property depends on can change after construction (e.g., `self.radius` is modified), the cached value becomes stale and silently wrong.
- **Thread safety**: `functools.cached_property` is **not thread-safe**. If multiple threads access the property simultaneously before it is cached, the computation may run multiple times. Use `threading.Lock` if this matters.
- **Side effects**: avoid caching properties that perform I/O or modify external state --- the user expects repeated access to be harmless.

---

## Exercises

**Exercise 1.** Write a `DataSet` class that accepts a list of numbers. Add a `@cached_property` called `stats` that returns a dictionary with `"mean"`, `"min"`, and `"max"`. Verify that the computation runs only once across multiple accesses.

??? success "Solution to Exercise 1"
    ```python
    from functools import cached_property

    class DataSet:
        def __init__(self, numbers):
            self.numbers = numbers

        @cached_property
        def stats(self):
            print("Computing stats...")
            return {
                "mean": sum(self.numbers) / len(self.numbers),
                "min": min(self.numbers),
                "max": max(self.numbers),
            }

    ds = DataSet([10, 20, 30, 40, 50])
    print(ds.stats)  # Computing stats... {'mean': 30.0, 'min': 10, 'max': 50}
    print(ds.stats)  # {'mean': 30.0, 'min': 10, 'max': 50} (no recomputation)
    ```

---

**Exercise 2.** Predict the output of the following code:

```python
from functools import cached_property

class Greeter:
    def __init__(self, name):
        self.name = name

    @cached_property
    def message(self):
        print("Computing message")
        return f"Hello, {self.name}!"

g = Greeter("Alice")
print(g.message)
g.name = "Bob"
print(g.message)
```

??? success "Solution to Exercise 2"
    The output is:

    ```
    Computing message
    Hello, Alice!
    Hello, Alice!
    ```

    The `message` cached property computes once on first access using `name = "Alice"`. Even though `name` is later changed to `"Bob"`, the cached value is never recomputed. `cached_property` stores the result in the instance's `__dict__`, and subsequent accesses return the cached string. This is a key difference from `@property`, which would recompute each time.

---

**Exercise 3.** Implement a custom `CachedProperty` descriptor class (without using `functools.cached_property`). It should compute the value on first access, store it in the instance's `__dict__`, and return the cached value on subsequent accesses. Test it with a class that computes the factorial of a stored number.

??? success "Solution to Exercise 3"
    ```python
    import math

    class CachedProperty:
        def __init__(self, func):
            self.func = func
            self.name = func.__name__

        def __get__(self, instance, owner):
            if instance is None:
                return self
            if self.name not in instance.__dict__:
                instance.__dict__[self.name] = self.func(instance)
            return instance.__dict__[self.name]

    class FactorialComputer:
        def __init__(self, n):
            self.n = n

        @CachedProperty
        def factorial(self):
            print(f"Computing {self.n}!")
            return math.factorial(self.n)

    fc = FactorialComputer(10)
    print(fc.factorial)  # Computing 10! -> 3628800
    print(fc.factorial)  # 3628800 (cached)
    ```

---

**Exercise 4.** Using `functools.cached_property`, create a `FileAnalyzer` class that takes a file path and has cached properties `line_count` and `word_count`. Demonstrate that deleting the cached property forces recomputation on next access.

??? success "Solution to Exercise 4"
    ```python
    from functools import cached_property

    class FileAnalyzer:
        def __init__(self, path):
            self.path = path

        @cached_property
        def line_count(self):
            print("Counting lines...")
            with open(self.path) as f:
                return sum(1 for _ in f)

        @cached_property
        def word_count(self):
            print("Counting words...")
            with open(self.path) as f:
                return sum(len(line.split()) for line in f)

    # Demonstration (assuming a file exists):
    # fa = FileAnalyzer("example.txt")
    # print(fa.line_count)    # Counting lines... 42
    # print(fa.line_count)    # 42 (cached)
    # del fa.line_count       # Clear cache
    # print(fa.line_count)    # Counting lines... 42 (recomputed)
    ```

---

**Exercise 5.** Explain the key difference between `@property` and `@cached_property` in terms of when computation happens. Give a concrete example of when using `@property` would be more appropriate than `@cached_property`.

??? success "Solution to Exercise 5"
    `@property` recomputes the value every time the attribute is accessed. `@cached_property` computes the value once on first access and caches it in the instance's `__dict__`.

    Use `@property` when the value depends on mutable state that may change between accesses:

    ```python
    class Rectangle:
        def __init__(self, width, height):
            self.width = width
            self.height = height

        @property
        def area(self):
            return self.width * self.height

    r = Rectangle(3, 4)
    print(r.area)     # 12
    r.width = 10
    print(r.area)     # 40 (correctly recomputed)
    ```

    If `area` were a `@cached_property`, it would still return `12` after changing `width`, which would be incorrect. Use `@cached_property` only when the underlying data is immutable after construction.
