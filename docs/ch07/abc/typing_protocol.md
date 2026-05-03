# typing.Protocol — Structural Subtyping

`Protocol` (Python 3.8+) enables structural subtyping (static duck typing). Classes don't need to inherit from a Protocol — they just need to implement the required methods. Think of Protocol as **"duck typing with guardrails"**: you get the flexibility of duck typing (no inheritance required) combined with the safety of static type checking (your editor and `mypy` verify that the right methods exist before you run the code).

!!! tip "Mental Model"
    An ABC says "you must be in the family to sit at the table" (nominal typing). A Protocol says "anyone who can hold a fork and use a napkin may sit down" (structural typing). The class never needs to know the Protocol exists -- it just needs to have the right shape, and the type checker confirms it at compile time.

!!! warning "Protocol requires a type checker to be useful"
    Protocol is a **static typing** construct. Without a type checker like `mypy` or
    `pyright`, Protocol definitions are just documentation — Python itself performs
    no verification at runtime (unless you add `@runtime_checkable`, which only
    checks method existence, not signatures). If your project does not use a type
    checker, Protocol offers no safety beyond what plain duck typing provides.

```python
from typing import Protocol
```

---

## Nominal vs Structural Typing

### Nominal Typing (ABC)

Classes must explicitly inherit:

```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self) -> str:
        pass

# Must inherit from Drawable
class Circle(Drawable):
    def draw(self) -> str:
        return "○"

# This class has draw() but ISN'T Drawable
class Square:
    def draw(self) -> str:
        return "□"

def render(shape: Drawable):
    print(shape.draw())

render(Circle())  # ✓ OK
render(Square())  # ✗ Type error (doesn't inherit Drawable)
```

### Structural Typing (Protocol)

Classes just need matching methods:

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str:
        ...

# No inheritance needed!
class Circle:
    def draw(self) -> str:
        return "○"

class Square:
    def draw(self) -> str:
        return "□"

def render(shape: Drawable):
    print(shape.draw())

render(Circle())  # ✓ OK
render(Square())  # ✓ OK - has draw(), so it's Drawable!
```

---

## Defining Protocols

### Basic Protocol

```python
from typing import Protocol

class Greeter(Protocol):
    def greet(self, name: str) -> str:
        ...  # Use ... or pass

# Any class with greet(name: str) -> str works
class FormalGreeter:
    def greet(self, name: str) -> str:
        return f"Good day, {name}."

class CasualGreeter:
    def greet(self, name: str) -> str:
        return f"Hey {name}!"

def say_hello(greeter: Greeter, name: str):
    print(greeter.greet(name))

say_hello(FormalGreeter(), "Alice")  # "Good day, Alice."
say_hello(CasualGreeter(), "Bob")    # "Hey Bob!"
```

### Protocol with Multiple Methods

```python
from typing import Protocol

class Database(Protocol):
    def connect(self) -> None:
        ...
    
    def execute(self, query: str) -> list:
        ...
    
    def close(self) -> None:
        ...

# Must implement ALL methods to be compatible
class PostgresDB:
    def connect(self) -> None:
        print("Connecting to Postgres...")
    
    def execute(self, query: str) -> list:
        return [{"id": 1}]
    
    def close(self) -> None:
        print("Closing connection")

def run_query(db: Database, query: str) -> list:
    db.connect()
    result = db.execute(query)
    db.close()
    return result
```

### Protocol with Properties

```python
from typing import Protocol

class Named(Protocol):
    @property
    def name(self) -> str:
        ...

class Person:
    def __init__(self, name: str):
        self._name = name
    
    @property
    def name(self) -> str:
        return self._name

class Company:
    name: str  # Class attribute also satisfies protocol
    
    def __init__(self, name: str):
        self.name = name

def display(obj: Named):
    print(f"Name: {obj.name}")

display(Person("Alice"))    # ✓
display(Company("Acme"))    # ✓
```

### Protocol with Class Variables

```python
from typing import Protocol, ClassVar

class Configurable(Protocol):
    config_key: ClassVar[str]
    
    def configure(self) -> None:
        ...

class DatabaseConfig:
    config_key: ClassVar[str] = "database"
    
    def configure(self) -> None:
        print(f"Configuring {self.config_key}")
```

---

## Runtime Checking

By default, Protocols only work for static type checking. For runtime `isinstance()` checks:

### @runtime_checkable

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Closeable(Protocol):
    def close(self) -> None:
        ...

class File:
    def close(self) -> None:
        print("File closed")

class Connection:
    def close(self) -> None:
        print("Connection closed")

f = File()
print(isinstance(f, Closeable))  # True

# Works with any object that has close()
import io
buffer = io.StringIO()
print(isinstance(buffer, Closeable))  # True
```

### Limitations of Runtime Checking

`@runtime_checkable` only checks method **existence**, not signatures:

```python
@runtime_checkable
class Adder(Protocol):
    def add(self, x: int, y: int) -> int:
        ...

class BadAdder:
    def add(self):  # Wrong signature!
        return 42

# Runtime check passes (only checks if 'add' exists)
print(isinstance(BadAdder(), Adder))  # True!

# But type checker would catch this
```

---

## Inheriting from Protocol

### Extending Protocols

```python
from typing import Protocol

class Reader(Protocol):
    def read(self) -> str:
        ...

class Writer(Protocol):
    def write(self, data: str) -> None:
        ...

class ReadWriter(Reader, Writer, Protocol):
    """Combines Reader and Writer."""
    pass

# Must implement both read() and write()
class File:
    def read(self) -> str:
        return "data"
    
    def write(self, data: str) -> None:
        print(f"Writing: {data}")

def process(rw: ReadWriter):
    data = rw.read()
    rw.write(data.upper())

process(File())  # ✓
```

### Adding Methods to Extended Protocol

```python
from typing import Protocol

class Identifiable(Protocol):
    @property
    def id(self) -> int:
        ...

class Timestamped(Protocol):
    @property
    def created_at(self) -> str:
        ...

class Entity(Identifiable, Timestamped, Protocol):
    @property
    def updated_at(self) -> str:
        ...
```

---

## Generic Protocols

```python
from typing import Protocol, TypeVar

T = TypeVar('T')

class Container(Protocol[T]):
    def get(self) -> T:
        ...
    
    def set(self, value: T) -> None:
        ...

class Box:
    def __init__(self, value: int):
        self._value = value
    
    def get(self) -> int:
        return self._value
    
    def set(self, value: int) -> None:
        self._value = value

def double_value(container: Container[int]) -> None:
    container.set(container.get() * 2)

box = Box(5)
double_value(box)
print(box.get())  # 10
```

### Covariant and Contravariant

Variance describes how subtyping of the type parameter relates to subtyping of the
generic Protocol. The intuition:

- **Covariant** (`T_co`): the Protocol only *produces* values of type `T`. A
  `Readable[Dog]` can be used where `Readable[Animal]` is expected (because a `Dog`
  is an `Animal`).
- **Contravariant** (`T_contra`): the Protocol only *consumes* values of type `T`. A
  `Writable[Animal]` can be used where `Writable[Dog]` is expected (because it can
  accept any `Animal`, including `Dog`).

```python
from typing import Protocol, TypeVar

T_co = TypeVar('T_co', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)

class Readable(Protocol[T_co]):
    def read(self) -> T_co:
        ...

class Writable(Protocol[T_contra]):
    def write(self, value: T_contra) -> None:
        ...
```

---

## Practical Examples

### Callback Protocol

```python
from typing import Protocol

class EventHandler(Protocol):
    def __call__(self, event: str, data: dict) -> None:
        ...

def on_click(event: str, data: dict) -> None:
    print(f"Clicked: {event}, {data}")

class ClickLogger:
    def __call__(self, event: str, data: dict) -> None:
        print(f"[LOG] {event}: {data}")

def register_handler(handler: EventHandler):
    handler("click", {"x": 10, "y": 20})

register_handler(on_click)      # Function ✓
register_handler(ClickLogger()) # Callable object ✓
```

### Iterator Protocol

```python
from typing import Protocol, TypeVar, Iterator

T = TypeVar('T')

class SupportsIter(Protocol[T]):
    def __iter__(self) -> Iterator[T]:
        ...

def first_item(items: SupportsIter[T]) -> T:
    return next(iter(items))

# Works with any iterable
print(first_item([1, 2, 3]))        # 1
print(first_item({4, 5, 6}))        # 4 (or 5 or 6)
print(first_item("hello"))          # 'h'
```

### Comparable Protocol

```python
from typing import Protocol, TypeVar

T = TypeVar('T')

class Comparable(Protocol):
    def __lt__(self, other: 'Comparable') -> bool:
        ...
    
    def __eq__(self, other: object) -> bool:
        ...

def min_value(a: Comparable, b: Comparable) -> Comparable:
    return a if a < b else b

# Works with any comparable
print(min_value(3, 7))          # 3
print(min_value("apple", "banana"))  # "apple"
```

### Context Manager Protocol

```python
from typing import Protocol, TypeVar

T = TypeVar('T')

class ContextManager(Protocol[T]):
    def __enter__(self) -> T:
        ...
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        ...

class Timer:
    def __enter__(self) -> 'Timer':
        import time
        self.start = time.time()
        return self
    
    def __exit__(self, *args) -> bool:
        import time
        self.elapsed = time.time() - self.start
        return False

def timed_operation(cm: ContextManager[Timer]):
    with cm as timer:
        pass
    return timer.elapsed
```

---

## Protocol vs ABC Comparison

| Feature | Protocol | ABC |
|---------|----------|-----|
| Inheritance required | No | Yes |
| Static type checking | ✓ | ✓ |
| Runtime isinstance() | With `@runtime_checkable` | Always |
| Method implementation | Not enforced | Enforced |
| Signature checking (runtime) | No | No |
| Use case | Duck typing, interfaces | Contracts, mixins |

### When to Use Each

**Use Protocol when:**
- You want duck typing with type hints
- Working with external code you can't modify
- Defining interfaces for callbacks
- Type checking without requiring inheritance

**Use ABC when:**
- You need runtime enforcement
- You want to share implementation (concrete methods)
- Building class hierarchies
- Need `isinstance()` checks without decorator

!!! note "What happens without a type checker?"
    Without `mypy` or `pyright`, a function typed as `def f(x: Drawable)` accepts
    **any** argument at runtime — Python does not enforce type hints. A class missing
    the `draw()` method will only fail when `draw()` is actually called, just like
    plain duck typing. This is why Protocol is most valuable in projects that run a
    type checker as part of their CI pipeline.

    Example `mypy` error for a missing method:

    ```text
    error: Argument 1 to "render" has incompatible type "Triangle";
           expected "Drawable"
    note:  "Triangle" is missing following "Drawable" protocol member:
    note:      draw
    ```

---

## Summary

| Feature | Syntax |
|---------|--------|
| Define Protocol | `class MyProtocol(Protocol):` |
| Runtime checkable | `@runtime_checkable` |
| Method stub | `def method(self) -> None: ...` |
| Property | `@property` + `...` |
| Extend Protocol | `class Extended(Proto1, Proto2, Protocol):` |
| Generic Protocol | `class Container(Protocol[T]):` |

**Key Takeaways**:

- Protocols enable structural subtyping (static duck typing)
- No inheritance required—just implement the methods
- Use `@runtime_checkable` for `isinstance()` support
- Runtime checks only verify method existence, not signatures
- Protocols are ideal for type hints without tight coupling
- Prefer Protocol for interfaces, ABC for enforced contracts

---

## Exercises

**Exercise 1.**
Define a `Measurable` Protocol with a `length()` method that returns a `float`. Then create three classes---`Rope`, `River`, and `Road`---each with a `length()` method returning different values. Write a function `total_length(items: list[Measurable]) -> float` that sums the lengths. None of the classes should inherit from `Measurable`.

??? success "Solution to Exercise 1"

        from typing import Protocol

        class Measurable(Protocol):
            def length(self) -> float:
                ...

        class Rope:
            def __init__(self, meters: float):
                self._meters = meters

            def length(self) -> float:
                return self._meters

        class River:
            def __init__(self, km: float):
                self._km = km

            def length(self) -> float:
                return self._km * 1000

        class Road:
            def __init__(self, miles: float):
                self._miles = miles

            def length(self) -> float:
                return self._miles * 1609.34

        def total_length(items: list[Measurable]) -> float:
            return sum(item.length() for item in items)

        items = [Rope(5.0), River(2.5), Road(1.0)]
        print(f"Total length: {total_length(items):.2f} meters")
        # Total length: 4114.34 meters

---

**Exercise 2.**
Create a `Loggable` Protocol with two methods: `log(message: str) -> None` and a `name` property returning `str`. Mark it with `@runtime_checkable`. Implement two classes that satisfy the protocol (`ConsoleLogger` and `FileLogger`). Demonstrate that `isinstance()` checks pass for both, and also show a class that is missing the `name` property fails the `isinstance()` check.

??? success "Solution to Exercise 2"

        from typing import Protocol, runtime_checkable

        @runtime_checkable
        class Loggable(Protocol):
            @property
            def name(self) -> str:
                ...

            def log(self, message: str) -> None:
                ...

        class ConsoleLogger:
            @property
            def name(self) -> str:
                return "console"

            def log(self, message: str) -> None:
                print(f"[{self.name}] {message}")

        class FileLogger:
            @property
            def name(self) -> str:
                return "file"

            def log(self, message: str) -> None:
                print(f"[{self.name}] Writing to file: {message}")

        class IncompleteLogger:
            def log(self, message: str) -> None:
                print(message)
            # Missing 'name' property

        print(isinstance(ConsoleLogger(), Loggable))     # True
        print(isinstance(FileLogger(), Loggable))        # True
        print(isinstance(IncompleteLogger(), Loggable))  # False

---

**Exercise 3.**
Define two Protocols: `Readable` with a `read() -> str` method, and `Writable` with a `write(data: str) -> None` method. Combine them into a `ReadWritable` Protocol. Create a `StringBuffer` class that satisfies `ReadWritable` without inheriting from any Protocol. Write a function that accepts a `ReadWritable` parameter and demonstrate that `StringBuffer` is compatible.

??? success "Solution to Exercise 3"

        from typing import Protocol

        class Readable(Protocol):
            def read(self) -> str:
                ...

        class Writable(Protocol):
            def write(self, data: str) -> None:
                ...

        class ReadWritable(Readable, Writable, Protocol):
            pass

        class StringBuffer:
            def __init__(self):
                self._buffer = ""

            def read(self) -> str:
                return self._buffer

            def write(self, data: str) -> None:
                self._buffer += data

        def process(rw: ReadWritable) -> str:
            rw.write("Hello, ")
            rw.write("World!")
            return rw.read()

        buf = StringBuffer()
        result = process(buf)
        print(result)  # Hello, World!

---

**Exercise 4.**
Explain the difference between these two approaches to defining a `Closeable` interface. Which one requires the implementing class to inherit? Which one would catch a missing `close()` method at type-checking time without `@runtime_checkable`? When would you choose one over the other?

```python
# Approach A
from abc import ABC, abstractmethod

class CloseableABC(ABC):
    @abstractmethod
    def close(self) -> None:
        pass

# Approach B
from typing import Protocol

class CloseableProtocol(Protocol):
    def close(self) -> None:
        ...
```

??? success "Solution to Exercise 4"

    **Approach A (ABC)** requires explicit inheritance. Any class that wants to be `CloseableABC` must write `class MyClass(CloseableABC):`. If `close()` is missing, Python raises `TypeError` at instantiation time — no type checker needed.

    **Approach B (Protocol)** does **not** require inheritance. Any class with a `close(self) -> None` method is structurally compatible. A type checker like `mypy` will flag a missing or mismatched `close()` at analysis time. Without `@runtime_checkable`, `isinstance()` checks will not work.

    **When to choose each:**

    - Use **ABC** when you need runtime enforcement, want to share concrete method implementations, or are building a class hierarchy you fully control.
    - Use **Protocol** when working with code you cannot modify (third-party libraries), when you want lightweight interfaces without coupling, or when structural compatibility is more important than a strict hierarchy.

    In modern Python, Protocol is the default choice for defining interfaces. Reserve ABCs for cases where you need concrete shared methods or runtime `isinstance()` enforcement without decorators.

---

**Exercise 5.**
A colleague argues that `@runtime_checkable` makes Protocol equivalent to ABC for runtime safety. Write a concrete example that disproves this claim: define a `@runtime_checkable` Protocol with a method `process(self, data: list) -> dict`, create a class whose `process` method has an incompatible signature (e.g., takes no arguments), and show that `isinstance()` still returns `True`. What does this tell you about the guarantees of `@runtime_checkable`?

??? success "Solution to Exercise 5"

        from typing import Protocol, runtime_checkable

        @runtime_checkable
        class Processor(Protocol):
            def process(self, data: list) -> dict:
                ...

        class BadProcessor:
            def process(self):  # Wrong signature: missing 'data' parameter
                return 42       # Wrong return type too

        bp = BadProcessor()
        print(isinstance(bp, Processor))  # True!

        # But calling it as expected fails:
        try:
            bp.process([1, 2, 3])
        except TypeError as e:
            print(e)
        # TypeError: BadProcessor.process() takes 1 positional argument but 2 were given

    `@runtime_checkable` only verifies that an attribute with the name `process` **exists** — it does not check the number of parameters, their types, or the return type. This means `isinstance()` can return `True` for a class that will fail at call time.

    The takeaway: `@runtime_checkable` is a quick structural check, not a behavioral guarantee. For full signature verification, rely on a static type checker like `mypy`. ABCs, by contrast, at least enforce that the method is *overridden* (though they also do not check signatures).
