# Composition Pattern

Composition models a "has-a" relationship where one object owns another as an integral part. The owner creates the part during its own initialization, and the part's lifetime is tied to the owner. When the owner is destroyed, its parts go with it. Composition is often preferred over inheritance for building flexible, modular systems because it avoids the tight coupling that deep class hierarchies introduce.

!!! tip "Mental Model"
    Think of composition as building with LEGO bricks that are glued together -- the whole creates its parts, owns them exclusively, and when you break the whole, the parts go with it. The owner delegates work to its parts rather than inheriting behavior, which keeps each piece simple and replaceable.

## What Is Composition

### 1. Has-A Relationship

In composition, the container creates its parts internally during initialization. This establishes exclusive ownership: no outside code holds a reference to the part before the container exists.

```python
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()  # Composition

    def start(self):
        return self.engine.start()

car = Car()
print(car.start())  # Engine started
```

The `Car` creates its own `Engine` inside `__init__`. Outside code interacts with the engine only through the `Car` interface, which encapsulates the internal part.

## Ownership

### 1. Strong Relationship

Strong ownership means the part's lifetime is tied to the container. The part is created when the container is created, and it becomes **unreachable** when the container becomes unreachable — at which point Python's garbage collector reclaims it. There is no need for manual cleanup.

```python
class Car:
    def __init__(self):
        self.engine = Engine()  # Engine created with Car

# When car becomes unreachable (no more references), the Engine
# also becomes unreachable and is eventually garbage-collected.
car = Car()
del car  # Removes the last reference; Engine is now unreachable
```

!!! note "GC Nuance"
    Python does not guarantee *when* an unreachable object is destroyed — only that it will be collected eventually. In CPython (the standard interpreter), reference counting usually reclaims objects immediately when the last reference is removed, but this is an implementation detail, not a language guarantee. The important design point is that the part **cannot be accessed** once the container is gone, because no external reference to it exists.

Because the `Engine` was created inside `Car.__init__` and no external variable holds a reference to it, deleting the `Car` removes the last reference to the `Engine`, making it unreachable.

## When Composition Goes Too Far

Composition is not free of costs. Over-decomposing into many tiny objects can **increase indirection** and hurt readability:

```python
# Over-composition: every concept is its own class
class NameValidator:
    def validate(self, name): ...

class NameFormatter:
    def format(self, name): ...

class NameStorage:
    def store(self, name): ...

class NameManager:
    def __init__(self):
        self._validator = NameValidator()
        self._formatter = NameFormatter()
        self._storage = NameStorage()
```

When a few lines of code inside one class would suffice, creating separate objects for each responsibility adds complexity without benefit. Composition should simplify your design, not multiply your classes.

## Summary

- Composition establishes a has-a relationship where the container creates and owns its parts.
- The owned component shares the lifetime of its container and is destroyed when the container is destroyed.
- This strong coupling between the whole and its parts means the part cannot exist independently.
- Composition promotes modular design by encapsulating implementation details behind the container's interface.
- **Avoid over-composition** --- don't create micro-objects for every concept when simpler inline code would suffice.

---

## Exercises

**Exercise 1.**
Create a `Computer` class that creates a `CPU` and `Memory` object inside its `__init__` (composition). Each component should have a `specs()` method returning a string. Add a `describe()` method to `Computer` that combines specs from all components. Demonstrate that the parts are created and owned by the computer.

??? success "Solution to Exercise 1"

        class CPU:
            def __init__(self, model):
                self.model = model

            def specs(self):
                return f"CPU: {self.model}"

        class Memory:
            def __init__(self, size_gb):
                self.size_gb = size_gb

            def specs(self):
                return f"Memory: {self.size_gb}GB"

        class Computer:
            def __init__(self, cpu_model, memory_gb):
                self._cpu = CPU(cpu_model)        # Composition
                self._memory = Memory(memory_gb)  # Composition

            def describe(self):
                return f"{self._cpu.specs()}, {self._memory.specs()}"

        pc = Computer("Intel i7", 16)
        print(pc.describe())  # CPU: Intel i7, Memory: 16GB

---

**Exercise 2.**
Build a `House` class that composes a `Room` list internally. The `House.__init__` takes a list of room names (strings) and creates `Room` objects from them. `Room` has a `name` and `area` attribute. Show that deleting the `House` removes all references to the rooms (no external variable holds them).

??? success "Solution to Exercise 2"

        class Room:
            def __init__(self, name, area=20.0):
                self.name = name
                self.area = area

            def __repr__(self):
                return f"Room('{self.name}', {self.area})"

        class House:
            def __init__(self, room_names):
                # Rooms created inside — composition
                self._rooms = [Room(name) for name in room_names]

            def list_rooms(self):
                return [r.name for r in self._rooms]

        house = House(["Kitchen", "Bedroom", "Bathroom"])
        print(house.list_rooms())  # ['Kitchen', 'Bedroom', 'Bathroom']

        del house
        # No external references to Room objects — they are garbage collected

---

**Exercise 3.**
Design a `Document` class that owns a `Header`, `Body`, and `Footer` (all created inside `Document.__init__`). Each part has a `render()` method. `Document` has a `render()` method that concatenates all parts. Demonstrate that changing a part requires going through the `Document` interface, since no external references to the parts exist.

??? success "Solution to Exercise 3"

        class Header:
            def __init__(self, title):
                self.title = title

            def render(self):
                return f"=== {self.title} ==="

        class Body:
            def __init__(self, content):
                self.content = content

            def render(self):
                return self.content

        class Footer:
            def __init__(self, text):
                self.text = text

            def render(self):
                return f"--- {self.text} ---"

        class Document:
            def __init__(self, title, content, footer_text):
                self._header = Header(title)
                self._body = Body(content)
                self._footer = Footer(footer_text)

            def render(self):
                parts = [self._header.render(), self._body.render(), self._footer.render()]
                return "\n".join(parts)

            def update_body(self, new_content):
                self._body.content = new_content

        doc = Document("Report", "Main content here.", "Page 1")
        print(doc.render())
        doc.update_body("Updated content.")
        print(doc.render())

---

**Exercise 4.**
Explain why the following design is **over-composition** and refactor it into a simpler version that keeps the same functionality. What is the rule of thumb for when composition adds complexity without benefit?

```python
class NameValidator:
    def validate(self, name):
        return len(name) > 0

class NameFormatter:
    def format(self, name):
        return name.strip().title()

class NameProcessor:
    def __init__(self):
        self._validator = NameValidator()
        self._formatter = NameFormatter()

    def process(self, name):
        if self._validator.validate(name):
            return self._formatter.format(name)
        raise ValueError("Invalid name")
```

??? success "Solution to Exercise 4"

    This is over-composition because `NameValidator` and `NameFormatter` each contain a single trivial method that will never be reused or swapped. Creating separate classes for one-line operations adds indirection without benefit.

    **Refactored:**

        class NameProcessor:
            def process(self, name):
                if not name:
                    raise ValueError("Invalid name")
                return name.strip().title()

    **Rule of thumb:** don't create a class for something that a function (or even a single expression) can handle. Composition should simplify your design by separating *genuinely independent* concerns — not by wrapping every line of code in its own object. If the "component" has no state, no alternative implementations, and no independent tests, it doesn't need to be a class.

---

**Exercise 5.**
A `Logger` class composes a `Formatter` and a `Writer`. The `Formatter` formats the message, and the `Writer` writes it to output. Show how this composition design connects to real-world patterns like dependency injection: make `Logger.__init__` accept formatter and writer as parameters (instead of creating them internally), so that tests can inject mocks and production code can inject real implementations.

??? success "Solution to Exercise 5"

        class Formatter:
            def format(self, message):
                from datetime import datetime
                return f"[{datetime.now():%H:%M:%S}] {message}"

        class ConsoleWriter:
            def write(self, text):
                print(text)

        class FileWriter:
            def __init__(self, path):
                self.path = path

            def write(self, text):
                print(f"(would write to {self.path}: {text})")

        class Logger:
            def __init__(self, formatter, writer):
                self._formatter = formatter  # Injected — not created here
                self._writer = writer

            def log(self, message):
                self._writer.write(self._formatter.format(message))

        # Production usage
        logger = Logger(Formatter(), FileWriter("app.log"))
        logger.log("Server started")

        # Test usage — inject mocks
        class MockWriter:
            def __init__(self):
                self.messages = []

            def write(self, text):
                self.messages.append(text)

        mock = MockWriter()
        test_logger = Logger(Formatter(), mock)
        test_logger.log("test message")
        assert len(mock.messages) == 1

    This is **dependency injection** — the `Logger` declares what it needs (a formatter and a writer) but does not decide which specific implementations to use. The caller makes that choice. This is composition at its most powerful: the `Logger` is fully testable, the components are interchangeable, and no subclass is needed to change behavior.
