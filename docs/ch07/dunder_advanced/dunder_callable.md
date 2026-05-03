# Callable Objects

In Python, any object with a `__call__` method is considered callable — you can invoke it with parentheses just like a function. This is one of Python's core **protocols**: Python doesn't care *what type* your object is, only *whether it implements `__call__`*. The same protocol-based approach drives [containers](dunder_containers.md), [iteration](dunder_iterables.md), and [context managers](dunder_context.md).

Callable objects are powerful because, unlike plain functions, they can carry state between invocations. Whenever you need a function that remembers configuration or accumulates results, a callable object is a natural fit.

!!! tip "Mental Model"
    A callable object is a function that remembers. Where a plain function is stateless (or relies on closures), a callable object stores configuration in `self` and uses `__call__` as its entry point. Think of it as upgrading a function to a class whenever you need persistent state between calls.

## Making Objects Callable

### 1. The __call__ Method

When you define `__call__` on a class, instances of that class become callable. Conceptually, writing `obj(args)` is translated by Python into `type(obj).__call__(obj, args)` — Python looks up `__call__` on the **class**, not the instance. (The actual C-level call path is more complex, but this model is accurate for understanding behavior.) This is the same descriptor-based lookup used by all dunder methods.

!!! note "Class Lookup, Not Instance Lookup"
    `obj()` does **not** call `obj.__call__()` via instance attribute lookup. It calls `type(obj).__call__(obj)`, which means `__call__` must be defined on the class (or a superclass), not assigned to the instance. This is consistent with how all Python protocols work: the method is looked up on the type, not on the object itself.

### 2. Use Cases

Callable objects are useful in several common scenarios:

- **Function-like objects**: create reusable operations that carry configuration state, such as a multiplier with a fixed factor.
- **Decorators**: implement decorators as classes when you need to maintain state across decorated function calls.
- **State machines**: encode transitions and current state inside the object, and trigger transitions by calling it.

### 3. Example

The following class creates a callable that multiplies its argument by a fixed factor set at initialization.

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, x):
        return x * self.factor

double = Multiplier(2)
print(double(5))   # 10
print(double(12))  # 24
```

The `double` object carries the factor `2` as internal state. Each call to `double(x)` multiplies `x` by that stored factor, producing the same behavior as a function but with the flexibility to change the factor or add methods later.

## Callable Objects vs Closures

Closures can also carry state, so when should you use a callable object instead?

```python
# Closure approach
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

# Callable object approach
class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    def __call__(self, x):
        return x * self.factor
```

Use a **closure** when the state is simple and read-only. Use a **callable object** when you need mutable state, multiple methods, inheritance, or introspection (`isinstance` checks, attribute access).

## Summary

- Defining `__call__` on a class makes its instances callable with the same syntax as a regular function.
- Callable objects combine the convenience of function call syntax with the ability to store and update internal state.
- Prefer closures for simple stateless or read-only-state cases; prefer callable objects when you need mutability, methods, or introspection.
- Common applications include configurable operations (strategy pattern), stateful decorators, and state machines.
- Callable objects are widely used in libraries like PyTorch (`nn.Module.__call__`), scikit-learn (transformers), and TensorFlow (layers) — any framework where objects need to behave like functions while carrying learned state.

!!! warning "When NOT to Use __call__"
    Don't implement `__call__` when its meaning would be ambiguous. A `User()` object that is callable — what does calling it do? If the answer is not immediately obvious, use a named method instead. Protocols should make code **more readable**, not clever.

---

## Runnable Example: `hash_digest_callable_example.py`

```python
"""
Callable Objects: Stream Hasher with __call__

Demonstrates the __call__ magic method by creating a callable class
that computes file hash digests. The object acts like a function but
maintains internal state (algorithm, buffer size).

Topics covered:
- __call__ to make instances callable
- hashlib for cryptographic hash functions
- Dynamic module/attribute loading with __import__ and getattr
- Iterator pattern with iter(callable, sentinel)

Based on concepts from Python-100-Days example07 and ch06/dunder_advanced materials.
"""

import hashlib
import io


# =============================================================================
# Example 1: Stream Hasher (Callable Class)
# =============================================================================

class StreamHasher:
    """A callable object that computes hash digests of data streams.

    By implementing __call__, instances can be used like functions:
        hasher = StreamHasher('sha256')
        digest = hasher(file_stream)  # Calls hasher.__call__(file_stream)

    This is more flexible than a plain function because the object
    retains configuration (algorithm, buffer size) as state.
    """

    SUPPORTED = ('md5', 'sha1', 'sha256', 'sha512')

    def __init__(self, algorithm: str = 'md5', buffer_size: int = 4096):
        """Initialize with hash algorithm and buffer size.

        Args:
            algorithm: Hash algorithm name (md5, sha1, sha256, sha512).
            buffer_size: Bytes to read per chunk.
        """
        if algorithm.lower() not in self.SUPPORTED:
            raise ValueError(
                f"Unsupported algorithm '{algorithm}'. "
                f"Choose from: {self.SUPPORTED}"
            )
        self.algorithm = algorithm.lower()
        self.buffer_size = buffer_size

    def digest(self, data_stream) -> str:
        """Compute hexadecimal hash digest from a data stream.

        Uses iter(callable, sentinel) pattern to read chunks:
        - callable: lambda that reads buffer_size bytes
        - sentinel: b'' (empty bytes = end of stream)
        """
        hasher = hashlib.new(self.algorithm)
        for chunk in iter(lambda: data_stream.read(self.buffer_size), b''):
            hasher.update(chunk)
        return hasher.hexdigest()

    def __call__(self, data_stream) -> str:
        """Make instances callable: hasher(stream) == hasher.digest(stream)."""
        return self.digest(data_stream)

    def __repr__(self):
        return f"StreamHasher('{self.algorithm}', buffer_size={self.buffer_size})"


# =============================================================================
# Example 2: Using Callable Objects
# =============================================================================

def demo_callable():
    """Demonstrate callable objects with hash computation."""
    print("=== Callable Object Demo ===")

    # Create hashers for different algorithms
    md5_hasher = StreamHasher('md5')
    sha256_hasher = StreamHasher('sha256')

    # Hash some data using BytesIO as a stream
    data = b"Hello, World! This is a test of the callable hasher."

    stream1 = io.BytesIO(data)
    stream2 = io.BytesIO(data)

    # Both calling styles work:
    md5_digest = md5_hasher(stream1)           # Using __call__
    sha256_digest = sha256_hasher.digest(stream2)  # Using method directly

    print(f"Data: {data.decode()!r}")
    print(f"MD5:    {md5_digest}")
    print(f"SHA256: {sha256_digest}")
    print()

    # Verify callable() built-in
    print(f"callable(md5_hasher): {callable(md5_hasher)}")
    print(f"callable('string'):   {callable('string')}")
    print()


# =============================================================================
# Example 3: Callable vs Function
# =============================================================================

def simple_md5(data: bytes) -> str:
    """Plain function alternative to callable class."""
    return hashlib.md5(data).hexdigest()


def demo_callable_vs_function():
    """Compare callable class vs plain function."""
    print("=== Callable Class vs Function ===")

    data = b"test data"

    # Function: simple but no configuration
    result1 = simple_md5(data)
    print(f"Function:        {result1}")

    # Callable object: configurable and stateful
    hasher = StreamHasher('md5', buffer_size=2)
    result2 = hasher(io.BytesIO(data))
    print(f"Callable object: {result2}")
    print(f"Same result:     {result1 == result2}")

    print()
    print("When to use callable classes:")
    print("  - Need configurable behavior (algorithm, buffer size)")
    print("  - Want to maintain state between calls")
    print("  - Implementing strategy/command patterns")
    print("  - Need both function-call and method-call interfaces")
    print()


# =============================================================================
# Example 4: iter(callable, sentinel) Pattern
# =============================================================================

def demo_iter_sentinel():
    """Demonstrate the iter(callable, sentinel) pattern used in StreamHasher."""
    print("=== iter(callable, sentinel) Pattern ===")

    # iter() with two args: calls the callable until it returns sentinel
    data = io.BytesIO(b"Hello World")

    print("Reading 3 bytes at a time until empty:")
    chunks = list(iter(lambda: data.read(3), b''))
    print(f"  Chunks: {chunks}")
    print()

    print("This is equivalent to:")
    print("  while True:")
    print("      chunk = stream.read(3)")
    print("      if chunk == b'':  # sentinel")
    print("          break")
    print("      process(chunk)")
    print()


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    demo_callable()
    demo_callable_vs_function()
    demo_iter_sentinel()
```


---

## Runnable Example: `callable_and_context_tutorial.py`

```python
"""
Example 5: Callable Objects and Context Managers
Demonstrates: __call__, __enter__, __exit__
"""

import time


class Multiplier:
    """A callable class that multiplies by a factor."""
    
    def __init__(self, factor):
        self.factor = factor
    
    def __call__(self, x):
        """Make the object callable."""
        return x * self.factor
    
    def __repr__(self):
        return f"Multiplier({self.factor})"


class Counter:
    """A callable counter that increments each time it's called."""
    
    def __init__(self, start=0):
        self.count = start
    
    def __call__(self):
        """Increment and return the count."""
        self.count += 1
        return self.count
    
    def reset(self):
        """Reset the counter."""
        self.count = 0
    
    def __repr__(self):
        return f"Counter(current={self.count})"


class Timer:
    """A context manager that times code execution."""
    
    def __init__(self, name="Code block"):
        self.name = name
        self.start_time = None
        self.elapsed_time = None
    
    def __enter__(self):
        """Start the timer when entering the context."""
        print(f"Starting timer for: {self.name}")
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop the timer when exiting the context."""
        self.elapsed_time = time.time() - self.start_time
        print(f"Finished: {self.name}")
        print(f"Time elapsed: {self.elapsed_time:.4f} seconds")
        
        # Return False to propagate any exceptions
        # Return True to suppress exceptions
        return False


class FileWriter:
    """A context manager for safe file writing."""
    
    def __init__(self, filename):
        self.filename = filename
        self.file = None
    
    def __enter__(self):
        """Open the file when entering the context."""
        print(f"Opening file: {self.filename}")
        self.file = open(self.filename, 'w')
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the file when exiting the context."""
        if self.file:
            print(f"Closing file: {self.filename}")
            self.file.close()
        
        # Handle exceptions
        if exc_type is not None:
            print(f"An error occurred: {exc_val}")
        
        return False  # Don't suppress exceptions


class DatabaseConnection:
    """A context manager simulating a database connection."""
    
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False
    
    def __enter__(self):
        """Establish connection when entering context."""
        print(f"Connecting to database: {self.db_name}")
        self.connected = True
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close connection when exiting context."""
        print(f"Disconnecting from database: {self.db_name}")
        self.connected = False
        return False
    
    def execute(self, query):
        """Simulate executing a query."""
        if not self.connected:
            raise RuntimeError("Not connected to database")
        print(f"Executing query: {query}")
        return f"Result of: {query}"


# Examples
if __name__ == "__main__":

    # ============================================================================
    print("=== Callable Objects: Multiplier ===")
    double = Multiplier(2)
    triple = Multiplier(3)
    
    print(f"double: {double}")
    print(f"double(5) = {double(5)}")
    print(f"double(10) = {double(10)}")
    
    print(f"\ntriple: {triple}")
    print(f"triple(5) = {triple(5)}")
    print(f"triple(10) = {triple(10)}")
    
    # Use in map
    numbers = [1, 2, 3, 4, 5]
    doubled = list(map(double, numbers))
    print(f"\nOriginal: {numbers}")
    print(f"Doubled: {doubled}")
    
    print("\n\n=== Callable Objects: Counter ===")
    counter = Counter()
    print(f"Counter: {counter}")
    
    print(f"Call 1: {counter()}")
    print(f"Call 2: {counter()}")
    print(f"Call 3: {counter()}")
    print(f"Current state: {counter}")
    
    counter.reset()
    print(f"After reset: {counter}")
    print(f"Next call: {counter()}")
    
    print("\n\n=== Context Manager: Timer ===")
    with Timer("Example computation"):
        # Simulate some work
        total = 0
        for i in range(1000000):
            total += i
        print(f"Sum calculated: {total}")
    
    print("\n=== Context Manager: Timer with Variable ===")
    with Timer("Another task") as timer:
        time.sleep(0.1)  # Sleep for 100ms
    print(f"Recorded time: {timer.elapsed_time:.4f} seconds")
    
    print("\n\n=== Context Manager: FileWriter ===")
    # Note: In this example, we won't actually create a file
    # but show how it would work
    print("Example of file writing (demonstration):")
    print("with FileWriter('output.txt') as f:")
    print("    f.write('Hello, World!')")
    print("    f.write('This is a test.')")
    
    print("\n\n=== Context Manager: DatabaseConnection ===")
    with DatabaseConnection("mydb") as db:
        result1 = db.execute("SELECT * FROM users")
        print(f"Result: {result1}")
        
        result2 = db.execute("INSERT INTO users VALUES (1, 'Alice')")
        print(f"Result: {result2}")
    
    print("\n=== Multiple Context Managers ===")
    with Timer("Database operations"), DatabaseConnection("testdb") as db:
        db.execute("SELECT * FROM products")
        db.execute("UPDATE products SET price = 99.99")
    
    print("\n=== Combining Callable and Context Manager ===")
    
    class CallableTimer:
        """A class that's both callable and a context manager."""
        
        def __init__(self):
            self.times = []
        
        def __call__(self, duration):
            """Record a time when called."""
            self.times.append(duration)
            print(f"Recorded time: {duration:.4f}s")
        
        def __enter__(self):
            """Start timing."""
            self.start = time.time()
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            """Calculate and record elapsed time."""
            elapsed = time.time() - self.start
            self(elapsed)  # Use __call__ to record
            return False
        
        def average(self):
            """Calculate average time."""
            return sum(self.times) / len(self.times) if self.times else 0
    
    timer_recorder = CallableTimer()
    
    # Use as context manager
    with timer_recorder:
        time.sleep(0.05)
    
    with timer_recorder:
        time.sleep(0.08)

    print(f"\nAverage time: {timer_recorder.average():.4f}s")
```

---

## Exercises

**Exercise 1.**
Create a `Multiplier` callable class. Its `__init__` takes a `factor`, and calling the instance multiplies the argument by that factor. For example, `double = Multiplier(2); double(5)` returns `10`. Also make it work with `map()`: `list(map(Multiplier(3), [1, 2, 3]))` returns `[3, 6, 9]`.

??? success "Solution to Exercise 1"

        class Multiplier:
            def __init__(self, factor):
                self.factor = factor

            def __call__(self, x):
                return x * self.factor

        double = Multiplier(2)
        print(double(5))   # 10
        print(double(100)) # 200

        triple = Multiplier(3)
        print(list(map(triple, [1, 2, 3])))  # [3, 6, 9]

---

**Exercise 2.**
Write a `CallCounter` callable class that wraps any function. Each time the instance is called, it forwards arguments to the wrapped function and increments a `count` attribute. Demonstrate by wrapping a `square` function and showing the call count after several invocations.

??? success "Solution to Exercise 2"

        class CallCounter:
            def __init__(self, func):
                self.func = func
                self.count = 0

            def __call__(self, *args, **kwargs):
                self.count += 1
                return self.func(*args, **kwargs)

        def square(x):
            return x ** 2

        counted_square = CallCounter(square)
        print(counted_square(5))  # 25
        print(counted_square(3))  # 9
        print(counted_square(7))  # 49
        print(f"Called {counted_square.count} times")  # Called 3 times

---

**Exercise 3.**
Build a `Pipeline` callable class that chains multiple functions together. Its `__init__` takes a list of functions. Calling the instance with a value passes it through each function in sequence. For example, `Pipeline([str.strip, str.lower, str.title])("  hello WORLD  ")` returns `"Hello World"`.

??? success "Solution to Exercise 3"

        class Pipeline:
            def __init__(self, functions):
                self.functions = functions

            def __call__(self, value):
                result = value
                for func in self.functions:
                    result = func(result)
                return result

        clean = Pipeline([str.strip, str.lower, str.title])
        print(clean("  hello WORLD  "))  # Hello World

        math_pipe = Pipeline([abs, float, lambda x: x ** 2])
        print(math_pipe(-5))  # 25.0

---

**Exercise 4.**
Explain why the following code does not make the instance callable, even though `__call__` is assigned as an instance attribute. What does this reveal about how Python looks up dunder methods?

```python
class Foo:
    pass

f = Foo()
f.__call__ = lambda: "called!"
f()  # TypeError: 'Foo' object is not callable
```

??? success "Solution to Exercise 4"

    Python looks up dunder methods on the **class** (via `type(obj)`), not on the instance. When you write `f()`, Python does `type(f).__call__(f)`, which looks for `__call__` on `Foo`, not on `f` itself. Since `Foo` doesn't define `__call__`, the call fails with `TypeError`.

    The instance attribute `f.__call__` exists but is never consulted by the call machinery. To make it work, you must define `__call__` on the class:

        class Foo:
            def __call__(self):
                return "called!"

        f = Foo()
        f()  # "called!" — works because __call__ is on the class

    This class-based lookup rule applies to all dunder methods (`__len__`, `__iter__`, `__enter__`, etc.) and is part of Python's data model. It exists so that metaclasses and type behavior remain consistent — the class defines the behavior, not individual instances.

---

**Exercise 5.**
Compare a closure and a callable class for implementing a rate limiter that allows at most `n` calls per `interval` seconds. Implement both approaches. Then explain which is easier to extend if you later need to add a `reset()` method and track the total number of rejected calls.

??? success "Solution to Exercise 5"

        import time

        # Closure approach
        def make_rate_limiter(max_calls, interval):
            timestamps = []

            def limiter():
                now = time.time()
                # Remove expired timestamps
                while timestamps and now - timestamps[0] > interval:
                    timestamps.pop(0)
                if len(timestamps) < max_calls:
                    timestamps.append(now)
                    return True
                return False

            return limiter

        # Callable class approach
        class RateLimiter:
            def __init__(self, max_calls, interval):
                self.max_calls = max_calls
                self.interval = interval
                self._timestamps = []
                self.rejected = 0

            def __call__(self):
                now = time.time()
                while self._timestamps and now - self._timestamps[0] > self.interval:
                    self._timestamps.pop(0)
                if len(self._timestamps) < self.max_calls:
                    self._timestamps.append(now)
                    return True
                self.rejected += 1
                return False

            def reset(self):
                self._timestamps.clear()
                self.rejected = 0

        # Usage
        limiter = RateLimiter(max_calls=3, interval=1.0)
        print(limiter())  # True
        print(limiter())  # True
        print(limiter())  # True
        print(limiter())  # False — rate limited
        print(f"Rejected: {limiter.rejected}")  # 1

    The closure works but cannot easily gain a `reset()` method or a `rejected` counter without resorting to mutable containers (e.g., a `dict`) shared between inner functions — which is awkward. The callable class naturally supports additional methods and attributes, making it the better choice when the "function" needs to grow beyond simple state.
