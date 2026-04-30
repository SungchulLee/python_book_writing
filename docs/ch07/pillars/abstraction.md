# Abstraction

Abstraction is the practice of defining stable interfaces that hide volatile implementation details, allowing components to change independently. It is a **design concept** --- not just a Python module. While the `abc` module provides one enforcement mechanism, abstraction also happens through duck typing, protocols, and simple function signatures. Abstraction works alongside [encapsulation](encapsulation.md) (protecting state), [inheritance](inheritance.md) (sharing structure), and [polymorphism](polymorphism.md) (enabling flexibility).

---

## What is Abstraction

### 1. Define Stable Boundaries

Show only essential features while hiding implementation details that may change.

### 2. High-Level Interface

Users interact with objects at a high level without understanding internals.

### 3. Design for Change

Focus on **what** an object does, not **how** it does it --- so that implementations can evolve without breaking consumers.

---

## Abstract Base Classes

### 1. Using ABC Module

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
```

Defines a contract that subclasses must follow.

### 2. Cannot Instantiate

```python
shape = Shape()  # TypeError!
```

Abstract classes cannot be instantiated directly.

### 3. Must Implement

```python
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):  # Must implement
        return self.width * self.height
```

---

## `@abstractmethod`

### 1. Required Methods

```python
class MyBase(ABC):
    @abstractmethod
    def must_override(self):
        pass
```

Subclasses **must** implement this method.

### 2. Enforcement

```python
class Incomplete(MyBase):
    pass

obj = Incomplete()  # TypeError!
```

Python prevents instantiation if abstract methods aren't implemented.

### 3. Complete Implementation

```python
class Complete(MyBase):
    def must_override(self):
        return "Implemented!"

obj = Complete()  # Works
```

---

## Abstract vs Optional

### 1. Required Methods

```python
class Dataset(ABC):
    @abstractmethod
    def __getitem__(self, index):
        pass  # Must override
    
    @abstractmethod
    def __len__(self):
        pass  # Must override
```

### 2. Optional Methods

```python
def __add__(self, other):
    return ConcatDataset([self, other])
```

No `@abstractmethod` = optional to override.

### 3. Mixed Approach

```python
class MyDataset(Dataset):
    def __getitem__(self, index):  # Required
        return self.data[index]
    
    def __len__(self):  # Required
        return len(self.data)
    
    # __add__ inherited - optional
```

---

## Abstract Decorators

### 1. Abstract Class Method

```python
class MyBase(ABC):
    @classmethod
    @abstractmethod
    def create(cls):
        pass
```

### 2. Abstract Static Method

```python
class MyBase(ABC):
    @staticmethod
    @abstractmethod
    def validate(data):
        pass
```

### 3. Abstract Property

```python
class MyBase(ABC):
    @property
    @abstractmethod
    def name(self):
        pass
```

---

## Abstraction Without ABC (Duck Typing)

You do not always need `ABC` to achieve abstraction in Python. Thanks to duck typing, any object that implements the expected methods can serve as an implementation --- no formal inheritance required.

### 1. Implicit Interface

```python
def process_payment(processor, amount):
    processor.process(amount)
```

Any object with a `process(amount)` method works --- no base class needed.

### 2. When to Use ABC vs Duck Typing

- **Use ABC** when you want Python to enforce the contract at instantiation time (failing fast if methods are missing).
- **Use duck typing** when flexibility matters more than compile-time safety, or when you are working with third-party classes you cannot modify.

### 3. Trade-off

Duck typing is more flexible but offers no enforcement. ABCs are more rigid but catch missing methods earlier. Both are valid forms of abstraction.

---

## Real-World Example

### 1. Shape Hierarchy

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
```

### 2. Concrete Shapes

```python
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius
```

### 3. Polymorphic Use

```python
shapes = [Rectangle(3, 4), Circle(5)]
for shape in shapes:
    print(f"Area: {shape.area()}")
```

---

## Benefits

### 1. Contract Enforcement

Guarantees subclasses implement required methods.

### 2. Clear Interface

Defines what operations are available.

### 3. Design Consistency

All implementations follow the same structure.

---

## Common Patterns

### 1. Template Method

```python
class Algorithm(ABC):
    @abstractmethod
    def step_one(self):
        pass
    
    @abstractmethod
    def step_two(self):
        pass
    
    def execute(self):  # Template
        self.step_one()
        self.step_two()
```

### 2. Strategy Pattern

```python
class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass
```

### 3. Factory Pattern

```python
class Creator(ABC):
    @abstractmethod
    def create_product(self):
        pass
```

---

## When Abstraction Goes Wrong

### 1. Leaky Abstraction

When the interface exposes implementation details (e.g., requiring a specific SQL dialect), the abstraction fails to isolate consumers from change.

### 2. Over-Abstraction

Too many abstract layers slow development and obscure intent. Not every function needs an abstract base class.

---

## Key Takeaways

- Abstraction defines stable interfaces that hide implementation details.
- ABC module enforces contracts; duck typing offers a lighter alternative.
- `@abstractmethod` marks required methods.
- Cannot instantiate abstract classes.
- Enables [polymorphic](polymorphism.md) designs.
- Beware leaky or excessive abstraction.

---

## Runnable Example: `abstract_base_classes_examples.py`

```python
"""Abstract Base Classes (ABC) - Defining contracts"""
from abc import ABC, abstractmethod

# =============================================================================
# Definitions
# =============================================================================

class PaymentProcessor(ABC):
    """Abstract interface for payment processing"""
    
    @abstractmethod
    def process_payment(self, amount):
        """All processors must implement this"""
        pass
    
    @abstractmethod
    def refund(self, transaction_id):
        """All processors must implement this"""
        pass
    
    def log_transaction(self, details):
        """Common implementation for all"""
        print(f"Logged: {details}")

class StripeProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing ${amount} via Stripe")
        self.log_transaction(f"Stripe: ${amount}")
    
    def refund(self, transaction_id):
        print(f"Refunding Stripe transaction {transaction_id}")

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing ${amount} via PayPal")
        self.log_transaction(f"PayPal: ${amount}")
    
    def refund(self, transaction_id):
        print(f"Refunding PayPal transaction {transaction_id}")

# Polymorphism with abstraction
def process_order(processor: PaymentProcessor, amount):
    processor.process_payment(amount)

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    stripe = StripeProcessor()
    paypal = PayPalProcessor()
    
    process_order(stripe, 100)
    process_order(paypal, 50)
```

---

## Exercises

**Exercise 1.** Define an abstract base class `Vehicle` with abstract methods `start_engine()` and `stop_engine()`. Then create two concrete subclasses, `Car` and `Motorcycle`, each providing its own implementation. Instantiate both and call their methods.

??? success "Solution to Exercise 1"
    ```python
    from abc import ABC, abstractmethod

    class Vehicle(ABC):
        @abstractmethod
        def start_engine(self):
            pass

        @abstractmethod
        def stop_engine(self):
            pass

    class Car(Vehicle):
        def start_engine(self):
            print("Car engine started: vroom!")

        def stop_engine(self):
            print("Car engine stopped.")

    class Motorcycle(Vehicle):
        def start_engine(self):
            print("Motorcycle engine started: braaap!")

        def stop_engine(self):
            print("Motorcycle engine stopped.")

    car = Car()
    car.start_engine()    # Car engine started: vroom!
    car.stop_engine()     # Car engine stopped.

    moto = Motorcycle()
    moto.start_engine()   # Motorcycle engine started: braaap!
    moto.stop_engine()    # Motorcycle engine stopped.
    ```

---

**Exercise 2.** Predict the output of the following code. Explain why it behaves the way it does.

```python
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message):
        pass

class FileLogger(Logger):
    pass

try:
    f = FileLogger()
except TypeError as e:
    print(e)
```

??? success "Solution to Exercise 2"
    The output is:

    ```
    Can't instantiate abstract class FileLogger without an implementation for abstract method 'log'
    ```

    `FileLogger` inherits from `Logger` but does not implement the abstract method `log`. Python enforces that all abstract methods must be implemented before a class can be instantiated. Attempting to create an instance of `FileLogger` raises a `TypeError` because the `log` method is still abstract.

---

**Exercise 3.** Create an abstract class `Converter` with an abstract class method `from_string(cls, s)` and an abstract property `unit`. Write a concrete subclass `TemperatureConverter` that implements both. The `from_string` method should parse a string like `"100C"` and return an instance, and the `unit` property should return `"Celsius"`.

??? success "Solution to Exercise 3"
    ```python
    from abc import ABC, abstractmethod

    class Converter(ABC):
        @classmethod
        @abstractmethod
        def from_string(cls, s):
            pass

        @property
        @abstractmethod
        def unit(self):
            pass

    class TemperatureConverter(Converter):
        def __init__(self, value):
            self._value = value

        @classmethod
        def from_string(cls, s):
            # Parse string like "100C"
            numeric = float(s.rstrip("CcFf"))
            return cls(numeric)

        @property
        def unit(self):
            return "Celsius"

    tc = TemperatureConverter.from_string("100C")
    print(tc._value)  # 100.0
    print(tc.unit)    # Celsius
    ```

---

**Exercise 4.** Using the Template Method pattern, create an abstract class `DataPipeline` with abstract methods `extract()`, `transform(data)`, and `load(data)`, plus a concrete `run()` method that calls them in order. Implement a `CSVPipeline` subclass that prints a message at each step.

??? success "Solution to Exercise 4"
    ```python
    from abc import ABC, abstractmethod

    class DataPipeline(ABC):
        @abstractmethod
        def extract(self):
            pass

        @abstractmethod
        def transform(self, data):
            pass

        @abstractmethod
        def load(self, data):
            pass

        def run(self):
            raw = self.extract()
            cleaned = self.transform(raw)
            self.load(cleaned)

    class CSVPipeline(DataPipeline):
        def extract(self):
            print("Extracting data from CSV file...")
            return ["Alice,30", "Bob,25"]

        def transform(self, data):
            print("Transforming CSV rows into dictionaries...")
            result = []
            for row in data:
                name, age = row.split(",")
                result.append({"name": name, "age": int(age)})
            return result

        def load(self, data):
            print(f"Loading {len(data)} records into database...")
            for record in data:
                print(f"  Inserted: {record}")

    pipeline = CSVPipeline()
    pipeline.run()
    ```

---

**Exercise 5.** Write a function `total_area(shapes)` that takes a list of objects and returns the sum of their areas. Use an abstract base class `Shape` with an abstract `area()` method. Create at least three different shape classes and demonstrate polymorphic behavior by passing a mixed list to your function.

??? success "Solution to Exercise 5"
    ```python
    from abc import ABC, abstractmethod
    import math

    class Shape(ABC):
        @abstractmethod
        def area(self):
            pass

    class Circle(Shape):
        def __init__(self, radius):
            self.radius = radius
        def area(self):
            return math.pi * self.radius ** 2

    class Rectangle(Shape):
        def __init__(self, width, height):
            self.width = width
            self.height = height
        def area(self):
            return self.width * self.height

    class Triangle(Shape):
        def __init__(self, base, height):
            self.base = base
            self.height = height
        def area(self):
            return 0.5 * self.base * self.height

    def total_area(shapes):
        return sum(s.area() for s in shapes)

    shapes = [Circle(5), Rectangle(3, 4), Triangle(6, 8)]
    print(f"Total area: {total_area(shapes):.2f}")
    # Total area: 78.54 + 12 + 24 = 114.54
    ```
