# Composition Pattern

Composition models a "has-a" relationship where one object owns another as an integral part. The owner creates the part during its own initialization, and the part's lifetime is tied to the owner. When the owner is destroyed, its parts go with it. Composition is often preferred over inheritance for building flexible, modular systems because it avoids the tight coupling that deep class hierarchies introduce.

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

Strong ownership means the part's lifetime is tied to the container. The part is created when the container is created, and Python's garbage collector automatically destroys the part when the container is collected. There is no need for manual cleanup.

```python
class Car:
    def __init__(self):
        self.engine = Engine()  # Engine created with Car

# When car goes out of scope and is garbage-collected,
# the Engine is also collected automatically because
# no other references to it exist.
car = Car()
del car  # Engine is cleaned up along with Car
```

Because the `Engine` was created inside `Car.__init__` and no external variable holds a reference to it, deleting the `Car` removes the last reference to the `Engine`, and Python's garbage collector reclaims it.

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
