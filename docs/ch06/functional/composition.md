# Composition Pattern

!!! tip "Mental Model"
    Composition means an object *owns* its parts and controls their lifetime -- when the owner dies, the parts die with it. Think of a car and its engine: the engine is created inside the car and has no independent existence. This tight ownership distinguishes composition from looser forms of association like aggregation.

## Strong Has-a

### 1. Definition

**Composition** is a strong form of association where:

- One class **owns** instances of another class
- The **lifetime** of the component is tied to the container
- When the container is destroyed, components are destroyed
- Models **whole-part** relationships

### 2. Ownership Model

The container **creates and controls** its components:

```python
class Engine:
    def start(self):
        return "Engine running"

class Car:
    def __init__(self):
        self.engine = Engine()  # Created here, owned by Car
    
    def start(self):
        return self.engine.start()

car = Car()  # Creates Engine
del car      # Destroys Engine too
```

### 3. Key Principle

Components **cannot exist meaningfully** outside their container.

## Implementation

### 1. Basic Pattern

```python
class Heart:
    def beat(self):
        return "Beating"

class Brain:
    def think(self):
        return "Thinking"

class Human:
    def __init__(self, name):
        self.name = name
        self.heart = Heart()    # Composed
        self.brain = Brain()    # Composed
    
    def live(self):
        return f"{self.heart.beat()}, {self.brain.think()}"

person = Human("Alice")
print(person.live())  # Beating, Thinking
```

### 2. Multiple Components

```python
class CPU:
    def __init__(self, cores):
        self.cores = cores
    
    def process(self):
        return f"Processing on {self.cores} cores"

class RAM:
    def __init__(self, size):
        self.size = size
    
    def store(self):
        return f"Storing in {self.size}GB RAM"

class Computer:
    def __init__(self, cpu_cores, ram_size):
        self.cpu = CPU(cpu_cores)      # Composed
        self.ram = RAM(ram_size)       # Composed
        self.storage = []              # Composed
    
    def specs(self):
        return f"{self.cpu.process()}, {self.ram.store()}"

pc = Computer(8, 16)
print(pc.specs())  # Processing on 8 cores, Storing in 16GB RAM
```

### 3. Nested Composition

```python
class Wheel:
    def __init__(self, size):
        self.size = size

class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

class Chassis:
    def __init__(self):
        self.wheels = [Wheel(18) for _ in range(4)]

class Car:
    def __init__(self):
        self.chassis = Chassis()     # Composed
        self.engine = Engine(200)    # Composed
```

## Benefits

### 1. Modularity

Break complex systems into manageable parts:

```python
class DisplayController:
    def render(self):
        return "Rendering display"

class InputController:
    def handle_input(self):
        return "Handling input"

class AudioController:
    def play_sound(self):
        return "Playing sound"

class GameConsole:
    def __init__(self):
        self.display = DisplayController()
        self.input = InputController()
        self.audio = AudioController()
    
    def run(self):
        return f"{self.display.render()}, {self.input.handle_input()}"
```

### 2. Encapsulation

Hide implementation details:

```python
class Database:
    def query(self, sql):
        # Complex database logic
        return "Query result"

class Cache:
    def get(self, key):
        return "Cached value"

class DataService:
    def __init__(self):
        self._database = Database()  # Hidden implementation
        self._cache = Cache()        # Hidden implementation
    
    def get_data(self, id):
        # Client doesn't know about DB or Cache
        cached = self._cache.get(id)
        if cached:
            return cached
        return self._database.query(f"SELECT * FROM table WHERE id={id}")
```

### 3. Flexibility

Swap implementations without changing interface:

```python
class EmailSender:
    def send(self, message):
        return f"Email sent: {message}"

class SMSSender:
    def send(self, message):
        return f"SMS sent: {message}"

class NotificationService:
    def __init__(self, sender):
        self.sender = sender
    
    def notify(self, message):
        return self.sender.send(message)

# Flexible composition
email_service = NotificationService(EmailSender())
sms_service = NotificationService(SMSSender())
```

## Lifetime Control

### 1. Container Controls

The container manages component lifecycle:

```python
class Connection:
    def __init__(self):
        print("Connection opened")
    
    def close(self):
        print("Connection closed")

class DatabaseSession:
    def __init__(self):
        self.connection = Connection()  # Created
    
    def __del__(self):
        self.connection.close()  # Destroyed with container

session = DatabaseSession()  # Connection opened
del session                  # Connection closed
```

### 2. Initialization Order

Components initialize in order:

```python
class Logger:
    def __init__(self):
        print("Logger initialized")

class Config:
    def __init__(self):
        print("Config initialized")

class Application:
    def __init__(self):
        self.config = Config()    # First
        self.logger = Logger()    # Second
        print("Application ready")

app = Application()
# Output:
# Config initialized
# Logger initialized
# Application ready
```

### 3. Cleanup Guarantee

Container ensures cleanup:

```python
class TempFile:
    def __init__(self, name):
        self.name = name
        print(f"Created {name}")
    
    def cleanup(self):
        print(f"Deleted {name}")

class FileProcessor:
    def __init__(self):
        self.temp_files = [TempFile(f"temp_{i}") for i in range(3)]
    
    def __del__(self):
        for f in self.temp_files:
            f.cleanup()

processor = FileProcessor()
# Created temp_0, temp_1, temp_2
del processor
# Deleted temp_0, temp_1, temp_2
```

## Design Patterns

### 1. Builder Pattern

```python
class Burger:
    def __init__(self):
        self.bun = None
        self.patty = None
        self.toppings = []

class BurgerBuilder:
    def __init__(self):
        self.burger = Burger()
    
    def add_bun(self, bun_type):
        self.burger.bun = bun_type
        return self
    
    def add_patty(self, patty_type):
        self.burger.patty = patty_type
        return self
    
    def add_topping(self, topping):
        self.burger.toppings.append(topping)
        return self
    
    def build(self):
        return self.burger

burger = (BurgerBuilder()
    .add_bun("sesame")
    .add_patty("beef")
    .add_topping("lettuce")
    .add_topping("tomato")
    .build())
```

### 2. Facade Pattern

```python
class VideoFile:
    def load(self):
        return "Video loaded"

class AudioFile:
    def load(self):
        return "Audio loaded"

class Codec:
    def decode(self):
        return "Decoded"

class MediaPlayer:
    """Facade that composes subsystems"""
    def __init__(self):
        self.video = VideoFile()
        self.audio = AudioFile()
        self.codec = Codec()
    
    def play(self, filename):
        video = self.video.load()
        audio = self.audio.load()
        decoded = self.codec.decode()
        return f"{video}, {audio}, {decoded}"

player = MediaPlayer()
player.play("movie.mp4")  # Simple interface, complex composition
```

### 3. Composite Pattern

```python
class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
    
    def get_size(self):
        return self.size

class Directory:
    def __init__(self, name):
        self.name = name
        self.children = []
    
    def add(self, item):
        self.children.append(item)
    
    def get_size(self):
        return sum(child.get_size() for child in self.children)

root = Directory("root")
root.add(File("file1.txt", 100))
root.add(File("file2.txt", 200))

subdir = Directory("subdir")
subdir.add(File("file3.txt", 150))
root.add(subdir)

print(root.get_size())  # 450
```

## Common Use Cases

### 1. Document Structure

```python
class Paragraph:
    def __init__(self, text):
        self.text = text

class Image:
    def __init__(self, url):
        self.url = url

class Section:
    def __init__(self, title):
        self.title = title
        self.paragraphs = []
        self.images = []

class Document:
    def __init__(self, title):
        self.title = title
        self.sections = []
    
    def add_section(self, section):
        self.sections.append(section)
```

### 2. UI Components

```python
class Label:
    def __init__(self, text):
        self.text = text

class Button:
    def __init__(self, label):
        self.label = label

class TextInput:
    def __init__(self, placeholder):
        self.placeholder = placeholder

class Form:
    def __init__(self):
        self.inputs = []
        self.buttons = []
        self.labels = []
    
    def add_input(self, input_field):
        self.inputs.append(input_field)
```

### 3. Game Objects

```python
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Sprite:
    def __init__(self, image):
        self.image = image

class Collider:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class GameObject:
    def __init__(self):
        self.position = Position(0, 0)
        self.sprite = Sprite("default.png")
        self.collider = Collider(32, 32)
```

## Best Practices

### 1. Single Responsibility

Each component has one job:

```python
class Validator:
    def validate(self, data):
        return True

class Parser:
    def parse(self, text):
        return {"parsed": text}

class Processor:
    def __init__(self):
        self.validator = Validator()
        self.parser = Parser()
    
    def process(self, text):
        if self.validator.validate(text):
            return self.parser.parse(text)
```

### 2. Dependency Injection

Pass dependencies rather than create:

```python
# ✅ GOOD - Flexible
class Service:
    def __init__(self, logger, database):
        self.logger = logger
        self.database = database

# ❌ BAD - Rigid
class Service:
    def __init__(self):
        self.logger = Logger()      # Hard-coded
        self.database = Database()  # Hard-coded
```

### 3. Interface Segregation

Depend on abstractions:

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, data):
        pass

class FileStorage(Storage):
    def save(self, data):
        # Save to file
        pass

class DataManager:
    def __init__(self, storage: Storage):
        self.storage = storage  # Depends on interface
```

## Testing

### 1. Easy Mocking

Composition enables easy testing:

```python
class MockDatabase:
    def query(self, sql):
        return {"mock": "data"}

class DataService:
    def __init__(self, database):
        self.database = database
    
    def get_user(self, id):
        return self.database.query(f"SELECT * FROM users WHERE id={id}")

# Easy to test
service = DataService(MockDatabase())
assert service.get_user(1) == {"mock": "data"}
```

### 2. Isolated Testing

Test components independently:

```python
class Calculator:
    def add(self, a, b):
        return a + b

class Display:
    def show(self, value):
        return f"Result: {value}"

class CalculatorApp:
    def __init__(self):
        self.calc = Calculator()
        self.display = Display()

# Test Calculator alone
assert Calculator().add(2, 3) == 5

# Test Display alone
assert Display().show(5) == "Result: 5"
```

### 3. Integration Testing

Test composed system:

```python
app = CalculatorApp()
result = app.calc.add(2, 3)
output = app.display.show(result)
assert output == "Result: 5"
```

---

## Exercises

**Exercise 1.**
Create a `Computer` class that owns an `CPU` and a `Memory` component (composition). The `CPU` has a `process(data)` method, and `Memory` has `read()` and `write(data)` methods. The `Computer`'s `run(data)` method should write data to memory, process it with the CPU, and return the result. Demonstrate that the components do not exist independently.

??? success "Solution to Exercise 1"

        class CPU:
            def process(self, data):
                return data * 2

        class Memory:
            def __init__(self):
                self._data = None

            def write(self, data):
                self._data = data

            def read(self):
                return self._data

        class Computer:
            def __init__(self):
                self.cpu = CPU()       # Composition: Computer owns CPU
                self.memory = Memory() # Composition: Computer owns Memory

            def run(self, data):
                self.memory.write(data)
                stored = self.memory.read()
                return self.cpu.process(stored)

        pc = Computer()
        print(pc.run(21))  # 42

---

**Exercise 2.**
Implement a `House` class that is composed of `Room` objects. Each `Room` has a `name` and `area`. The `House` should provide a `total_area()` method that sums all room areas, and an `add_room(name, area)` method. Demonstrate that rooms are created by the house and cannot outlive it.

??? success "Solution to Exercise 2"

        class Room:
            def __init__(self, name, area):
                self.name = name
                self.area = area

        class House:
            def __init__(self):
                self._rooms = []

            def add_room(self, name, area):
                room = Room(name, area)  # House creates the Room
                self._rooms.append(room)

            def total_area(self):
                return sum(r.area for r in self._rooms)

        house = House()
        house.add_room("Kitchen", 20)
        house.add_room("Bedroom", 15)
        house.add_room("Living Room", 30)
        print(f"Total area: {house.total_area()} sqm")  # 65

---

**Exercise 3.**
Build a `ReportBuilder` using the builder pattern with composition. The `ReportBuilder` should have `add_title(text)`, `add_paragraph(text)`, and `build()` methods. Each call to `add_title` or `add_paragraph` stores a component internally. `build()` returns the full report as a single string with titles in uppercase and paragraphs as-is, separated by newlines.

??? success "Solution to Exercise 3"

        class ReportBuilder:
            def __init__(self):
                self._parts = []

            def add_title(self, text):
                self._parts.append(("title", text))
                return self

            def add_paragraph(self, text):
                self._parts.append(("paragraph", text))
                return self

            def build(self):
                lines = []
                for kind, text in self._parts:
                    if kind == "title":
                        lines.append(text.upper())
                    else:
                        lines.append(text)
                return "\n".join(lines)

        report = (
            ReportBuilder()
            .add_title("Introduction")
            .add_paragraph("This is the first paragraph.")
            .add_title("Conclusion")
            .add_paragraph("This wraps up the report.")
            .build()
        )
        print(report)
