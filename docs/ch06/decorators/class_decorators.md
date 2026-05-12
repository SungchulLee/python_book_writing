# Class Decorators

Decorators can be applied to classes, and classes can be used as decorators.

!!! tip "Mental Model"
    A class decorator intercepts a class at creation time, modifies or wraps it, and hands it back -- just like a function decorator, but the input is a class object instead of a function. Think of it as a factory inspector who stamps extra features onto each class as it rolls off the assembly line.

## Decorating Classes

A class decorator receives a class and returns a modified class.

### Adding Methods

```python
def add_repr(cls):
    """Add a __repr__ method to a class."""
    def __repr__(self):
        attrs = ', '.join(f'{k}={v!r}' for k, v in vars(self).items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p)  # Point(x=3, y=4)
```

### Adding Class Attributes

```python
def singleton(cls):
    """Make a class a singleton."""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Connecting to database...")

db1 = Database()  # Prints message
db2 = Database()  # No message (same instance)
print(db1 is db2)  # True
```

### Registering Classes

```python
registry = {}

def register(cls):
    """Register a class in the global registry."""
    registry[cls.__name__] = cls
    return cls

@register
class Handler:
    pass

@register
class Processor:
    pass

print(registry)  # {'Handler': <class 'Handler'>, 'Processor': <class 'Processor'>}
```

---

## Classes as Decorators

A class can act as a decorator by implementing `__init__` and `__call__`.

### Basic Pattern

```python
class CountCalls:
    """Decorator class that counts function calls."""
    
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call {self.count} of {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Call 1 of greet, Hello, Alice!
greet("Bob")    # Call 2 of greet, Hello, Bob!
print(greet.count)  # 2
```

### With Parameters (Factory Pattern)

```python
class Repeat:
    """Decorator class with parameters."""
    
    def __init__(self, times):
        self.times = times
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for _ in range(self.times):
                result = func(*args, **kwargs)
            return result
        return wrapper

@Repeat(3)
def say_hello():
    print("Hello!")

say_hello()  # Prints "Hello!" 3 times
```

### Stateful Decorator Class

```python
class Memoize:
    """Caching decorator implemented as a class."""
    
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]
    
    def clear_cache(self):
        self.cache.clear()

@Memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(100))  # Fast due to caching
print(fibonacci.cache)  # View cached values
fibonacci.clear_cache()  # Clear the cache
```

---

## Preserving Method Behavior

When decorating methods, use `__get__` to handle the descriptor protocol:

```python
from functools import wraps

class Logger:
    """Decorator that works with both functions and methods."""
    
    def __init__(self, func):
        self.func = func
        wraps(func)(self)
    
    def __call__(self, *args, **kwargs):
        print(f"Calling {self.func.__name__}")
        return self.func(*args, **kwargs)
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Return a bound method
        from functools import partial
        return partial(self.__call__, obj)

class MyClass:
    @Logger
    def method(self, x):
        return x * 2

obj = MyClass()
print(obj.method(5))  # Works correctly with self
```

---

## Comparison: Function vs Class Decorators

| Aspect | Function Decorator | Class Decorator |
|--------|-------------------|-----------------|
| State | Closure variables | Instance attributes |
| Methods | Not applicable | Can add helper methods |
| Readability | Simpler for basic cases | Better for complex state |
| Instance check | Not applicable | `isinstance(decorated, DecoratorClass)` |

### When to Use Class Decorators

- Need complex state management
- Want to expose additional methods
- Need to work with the descriptor protocol
- Want cleaner organization for complex decorators

### When to Use Function Decorators

- Simple transformations
- No complex state needed
- Prefer functional style
- Need to work with `functools.wraps` easily

---

## Practical Examples

### Timing Decorator Class

```python
import time

class Timer:
    """Time function execution with statistics."""
    
    def __init__(self, func):
        self.func = func
        self.times = []
    
    def __call__(self, *args, **kwargs):
        start = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        self.times.append(elapsed)
        return result
    
    @property
    def average_time(self):
        return sum(self.times) / len(self.times) if self.times else 0
    
    @property
    def total_time(self):
        return sum(self.times)

@Timer
def slow_function():
    time.sleep(0.1)

for _ in range(5):
    slow_function()

print(f"Average: {slow_function.average_time:.3f}s")
print(f"Total: {slow_function.total_time:.3f}s")
```

### Validation Decorator Class

```python
class ValidateArgs:
    """Validate function arguments against type specifications."""
    
    def __init__(self, **type_specs):
        self.type_specs = type_specs
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            # Validate keyword arguments
            for name, expected_type in self.type_specs.items():
                if name in kwargs:
                    if not isinstance(kwargs[name], expected_type):
                        raise TypeError(
                            f"{name} must be {expected_type.__name__}"
                        )
            return func(*args, **kwargs)
        return wrapper

@ValidateArgs(name=str, age=int)
def create_user(name, age):
    return {'name': name, 'age': age}

create_user(name="Alice", age=30)  # Works
create_user(name="Bob", age="30")  # TypeError
```

---

## Summary

| Pattern | Description |
|---------|-------------|
| Class decorator | Decorator applied to a class |
| Decorator class | Class that acts as a decorator |
| `__init__` | Receives the function/parameters |
| `__call__` | Called when decorated function is invoked |
| `__get__` | For method decoration (descriptor protocol) |

**Key Points**:

- Class decorators modify or enhance classes
- Decorator classes provide stateful decorators
- Use `__get__` for method compatibility
- Choose based on complexity and state requirements
---

## Runnable Example: `singleton_decorator_example.py`

```python
"""
Singleton Pattern: Decorator vs Metaclass Approaches

The singleton pattern ensures a class has only one instance.
This tutorial shows how to implement it using a class decorator
with thread-safety via double-checked locking.

Topics covered:
- Class decorators (decorators applied to classes)
- Singleton pattern implementation
- Thread safety with threading.Lock
- functools.wraps on classes
- Comparison: decorator vs metaclass singleton

Based on concepts from Python-100-Days examples 10 & 18, and ch05/decorators materials.
"""

import threading
from functools import wraps


# =============================================================================
# Example 1: Thread-Safe Singleton Decorator
# =============================================================================

def singleton(cls):
    """Decorator that makes a class a singleton (only one instance ever created).

    Uses double-checked locking for thread safety:
    1. First check without lock (fast path for existing instance)
    2. Acquire lock and check again (prevent race condition)

    >>> @singleton
    ... class Database:
    ...     def __init__(self, url):
    ...         self.url = url
    >>> db1 = Database("localhost:5432")
    >>> db2 = Database("localhost:3306")  # Returns same instance!
    >>> db1 is db2
    True
    """
    instances = {}
    lock = threading.Lock()

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:          # Fast check (no lock)
            with lock:                     # Acquire lock
                if cls not in instances:   # Double-check under lock
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


# =============================================================================
# Example 2: Singleton in Action
# =============================================================================

@singleton
class AppConfig:
    """Application configuration (should only exist once)."""

    def __init__(self, debug=False, db_url="sqlite:///app.db"):
        self.debug = debug
        self.db_url = db_url

    def __str__(self):
        return f"AppConfig(debug={self.debug}, db_url='{self.db_url}')"


def demo_singleton():
    """Demonstrate that singleton always returns the same instance."""
    print("=== Singleton Decorator Demo ===")

    config1 = AppConfig(debug=True, db_url="postgres://localhost/mydb")
    config2 = AppConfig(debug=False, db_url="mysql://localhost/other")

    print(f"config1: {config1}")
    print(f"config2: {config2}")
    print(f"Same object? {config1 is config2}")  # True
    print(f"Class name preserved: {AppConfig.__name__}")
    print()


# =============================================================================
# Example 3: Thread-Safety Verification
# =============================================================================

@singleton
class Counter:
    """Thread-safe singleton counter."""

    def __init__(self):
        self.count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self.count += 1


def demo_thread_safety():
    """Verify singleton works correctly under concurrent access."""
    print("=== Thread Safety Verification ===")

    def worker():
        c = Counter()  # Always gets the same instance
        for _ in range(1000):
            c.increment()

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    counter = Counter()
    print(f"Expected count: 10000")
    print(f"Actual count:   {counter.count}")
    print(f"Thread safe:    {counter.count == 10000}")
    print()


# =============================================================================
# Example 4: Metaclass Alternative (for comparison)
# =============================================================================

class SingletonMeta(type):
    """Metaclass approach to singleton pattern.

    Instead of decorating the class, we use a custom metaclass that
    intercepts instance creation via __call__.
    """

    def __init__(cls, *args, **kwargs):
        cls._instance = None
        cls._lock = threading.Lock()
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Logger(metaclass=SingletonMeta):
    """Logger using metaclass singleton."""

    def __init__(self, name="default"):
        self.name = name
        self.messages = []

    def log(self, message):
        self.messages.append(message)

    def __str__(self):
        return f"Logger('{self.name}', {len(self.messages)} messages)"


def demo_metaclass_singleton():
    """Compare metaclass singleton with decorator singleton."""
    print("=== Metaclass Singleton Comparison ===")

    log1 = Logger("app")
    log1.log("Started")
    log2 = Logger("other")  # Returns same instance
    log2.log("Continued")

    print(f"log1: {log1}")
    print(f"log2: {log2}")
    print(f"Same object? {log1 is log2}")

    print()
    print("Decorator singleton:")
    print("  + Simple to apply (@singleton)")
    print("  + Works with functools.wraps")
    print("  - isinstance() won't work (returns function)")
    print()
    print("Metaclass singleton:")
    print("  + isinstance() works correctly")
    print("  + More 'proper' OOP approach")
    print("  - More complex to understand")
    print("  - Can't combine with other metaclasses easily")


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    demo_singleton()
    demo_thread_safety()
    demo_metaclass_singleton()
```

---

## Exercises

**Exercise 1.**
Write a class decorator `add_str` that adds a `__str__` method to any class. The generated `__str__` should return the class name followed by all instance attributes in `key=value` format. Apply it to a `Book` class with `title` and `author` attributes and verify the output.

??? success "Solution to Exercise 1"

        def add_str(cls):
            """Add a __str__ method that shows all instance attributes."""
            def __str__(self):
                attrs = ', '.join(f'{k}={v!r}' for k, v in vars(self).items())
                return f"{cls.__name__}({attrs})"
            cls.__str__ = __str__
            return cls

        @add_str
        class Book:
            def __init__(self, title, author):
                self.title = title
                self.author = author

        b = Book("1984", "Orwell")
        print(b)  # Book(title='1984', author='Orwell')

---

**Exercise 2.**
Create a decorator class `RateLimiter` that limits how many times a decorated function can be called within a given number of seconds. The constructor should accept a `max_calls` parameter (default 3). If the function is called more than `max_calls` times within one second, raise a `RuntimeError`. Expose a `reset()` method to clear the call history.

??? success "Solution to Exercise 2"

        import time

        class RateLimiter:
            """Decorator class that limits function call frequency."""

            def __init__(self, max_calls=3):
                self.max_calls = max_calls
                self.call_times = []

            def __call__(self, func):
                def wrapper(*args, **kwargs):
                    now = time.time()
                    # Keep only calls within the last second
                    self.call_times = [t for t in self.call_times if now - t < 1.0]
                    if len(self.call_times) >= self.max_calls:
                        raise RuntimeError(
                            f"Rate limit exceeded: {self.max_calls} calls per second"
                        )
                    self.call_times.append(now)
                    return func(*args, **kwargs)
                wrapper.reset = self.reset
                return wrapper

            def reset(self):
                self.call_times.clear()

        @RateLimiter(max_calls=2)
        def ping():
            return "pong"

        print(ping())  # pong
        print(ping())  # pong
        try:
            ping()  # RuntimeError
        except RuntimeError as e:
            print(e)

---

**Exercise 3.**
Write a class decorator `track_instances` that adds instance tracking to any class. The decorated class should gain a class-level `instances` list that holds weak references (or plain references) to every object created, and a class method `get_instance_count()` that returns the current number of tracked instances. Demonstrate it with a `Player` class.

??? success "Solution to Exercise 3"

        def track_instances(cls):
            """Class decorator that tracks all created instances."""
            original_init = cls.__init__
            cls.instances = []

            def new_init(self, *args, **kwargs):
                original_init(self, *args, **kwargs)
                cls.instances.append(self)

            cls.__init__ = new_init

            @classmethod
            def get_instance_count(klass):
                return len(klass.instances)

            cls.get_instance_count = get_instance_count
            return cls

        @track_instances
        class Player:
            def __init__(self, name):
                self.name = name

        p1 = Player("Alice")
        p2 = Player("Bob")
        p3 = Player("Charlie")
        print(Player.get_instance_count())  # 3
