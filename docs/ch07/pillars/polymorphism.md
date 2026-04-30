# Polymorphism

Polymorphism allows objects of different types to be treated through a common interface, with each type implementing behavior in its own way. At its core, polymorphism replaces conditional branching (`if/elif` on types) with **dispatch** --- the right method is called automatically based on the object's type. Polymorphism works alongside [encapsulation](encapsulation.md) (protecting state), [abstraction](abstraction.md) (defining interfaces), and [inheritance](inheritance.md) (sharing structure).

---

## What is Polymorphism

### 1. Many Forms

"Polymorphism" means "many forms"—same interface, different implementations.

### 2. Common Interface

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"
```

### 3. Uniform Treatment

```python
animals = [Dog("Buddy"), Cat("Whiskers")]
for animal in animals:
    print(animal.speak())
```

Don't care about the specific type—just call the method.

---

## Interface Definition

### 1. Placeholder Method

```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass  # placeholder
```

Signals that all subclasses should implement `speak`.

### 2. Method Override

```python
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"
```

Each subclass provides its own implementation.

### 3. Type Consistency

All `Animal` objects have a `speak` method.

---

## Duck Typing

### 1. No Type Declaration

```python
def make_speak(animal):
    print(animal.speak())
```

No need to declare `animal` is an `Animal`.

### 2. Interface Matters

```python
class Robot:
    def speak(self):
        return "Beep boop!"

make_speak(Robot())  # Works!
```

If it has `speak()`, it works.

### 3. Runtime Check

```python
if hasattr(obj, 'speak'):
    obj.speak()
```

---

## Types of Polymorphism

Python supports several forms of polymorphism:

| Type | Mechanism | Example |
|---|---|---|
| Subtype (inheritance) | Method overriding via class hierarchy | `Dog(Animal).speak()` |
| Duck typing (structural) | Any object with the right methods | `Robot().speak()` works without inheriting `Animal` |
| Operator overloading | Special methods (`__add__`, `__eq__`, ...) | `Vector(1,2) + Vector(3,4)` |
| Parametric (generics) | Type parameters (Python 3.12+ syntax) | `list[int]`, `dict[str, float]` |

In Python, **duck typing is the dominant form** --- inheritance-based polymorphism is available but not required. This is a key difference from languages like Java or C++ where subtype polymorphism is the primary mechanism.

---

## Method Overriding

### 1. Replace Behavior

```python
class Parent:
    def greet(self):
        return "Hello from Parent"

class Child(Parent):
    def greet(self):
        return "Hello from Child"
```

### 2. Extend Behavior

```python
class Child(Parent):
    def greet(self):
        parent_msg = super().greet()
        return f"{parent_msg} and Child"
```

### 3. Selective Override

```python
class Parent:
    def method_a(self):
        return "A"
    
    def method_b(self):
        return "B"

class Child(Parent):
    def method_a(self):  # override only this
        return "A from Child"
    # method_b inherited
```

---

## Operator Overloading

### 1. Special Methods

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
```

### 2. String Representation

```python
def __str__(self):
    return f"Vector({self.x}, {self.y})"

def __repr__(self):
    return f"Vector(x={self.x}, y={self.y})"
```

### 3. Comparison

```python
def __eq__(self, other):
    return self.x == other.x and self.y == other.y

def __lt__(self, other):
    return self.x < other.x
```

---

## Real-World Example

### 1. SciPy Distributions

```python
from scipy import stats

# Different distributions, same interface
obj = stats.norm()    # Normal
# obj = stats.uniform() # Uniform
# obj = stats.expon()  # Exponential

x = obj.rvs(10_000)  # All have rvs()
```

### 2. Common Methods

```python
samples = obj.rvs(n)     # random samples
density = obj.pdf(x)     # probability density
cumulative = obj.cdf(x)  # cumulative distribution
```

### 3. Interchangeable

Can swap distributions without changing code.

---

## Polymorphic Functions

### 1. Generic Processing

```python
def process_shapes(shapes):
    total_area = 0
    for shape in shapes:
        total_area += shape.area()
    return total_area
```

### 2. Mixed Types

```python
shapes = [
    Rectangle(3, 4),
    Circle(5),
    Triangle(3, 4)
]
print(process_shapes(shapes))
```

### 3. No Type Checks

Don't need to check `isinstance()`—just call the method.

---

## Benefits

### 1. Code Reusability

Write once, works for many types.

### 2. Extensibility

Add new types without changing existing code.

### 3. Clean Design

No complex conditional logic based on type.

---

## Polymorphism vs Abstraction

### 1. Polymorphism (Informal)

```python
class Animal:
    def speak(self):
        pass  # no enforcement
```

Trust that subclasses implement correctly.

### 2. Abstraction (Formal)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass  # enforced!
```

Forces subclasses to implement.

### 3. Key Difference

Polymorphism = same interface, different behaviors (the runtime mechanism).
[Abstraction](abstraction.md) = enforced contract with ABC (the design-time guarantee).

Polymorphism can work without abstraction (via duck typing), and abstraction without polymorphism is just a contract with one implementation. They are most powerful together.

---

## Key Takeaways

- Polymorphism enables uniform interfaces.
- Different types implement methods differently.
- Duck typing: if it quacks, it's a duck.
- Method overriding enables custom behavior.
- Operator overloading uses special methods.

---

## Runnable Example: `polymorphism_demo.py`

```python
"""
Example 05: Polymorphism

Polymorphism means "many forms". It allows objects of different classes
to be treated as objects of a common parent class, and the correct method
is called based on the object's actual type.
"""

# ============================================================================
# Example 1: Basic Polymorphism
class PaymentMethod:
    def __init__(self, name):
        self.name = name
    
    def process_payment(self, amount):
        raise NotImplementedError("Subclass must implement this method")
    
    def get_receipt(self, amount):
        return f"Payment of ${amount:.2f} via {self.name}"


class CreditCard(PaymentMethod):
    def __init__(self, card_number, cvv):
        super().__init__("Credit Card")
        self.card_number = card_number[-4:]  # Store only last 4 digits
        self.cvv = cvv
    
    def process_payment(self, amount):
        return f"Processing ${amount:.2f} on card ending in {self.card_number}"


class PayPal(PaymentMethod):
    def __init__(self, email):
        super().__init__("PayPal")
        self.email = email
    
    def process_payment(self, amount):
        return f"Processing ${amount:.2f} via PayPal account {self.email}"


class Bitcoin(PaymentMethod):
    def __init__(self, wallet_address):
        super().__init__("Bitcoin")
        self.wallet_address = wallet_address
    
    def process_payment(self, amount):
        btc_amount = amount / 30000  # Simplified conversion
        return f"Processing {btc_amount:.6f} BTC to wallet {self.wallet_address[:8]}..."


# ============================================================================
# Example 2: Polymorphism with Different Return Types
class DataProcessor:
    def process(self, data):
        raise NotImplementedError


class TextProcessor(DataProcessor):
    def process(self, data):
        # Returns uppercase text
        return data.upper()


class NumberProcessor(DataProcessor):
    def process(self, data):
        # Returns sum of numbers
        return sum(data)


class ListProcessor(DataProcessor):
    def process(self, data):
        # Returns sorted list
        return sorted(data)


# ============================================================================
# Example 3: Duck Typing (Python's Polymorphism)
class Duck:
    def speak(self):
        return "Quack!"
    
    def swim(self):
        return "Duck is swimming"


class Person:
    def speak(self):
        return "Hello!"
    
    def swim(self):
        return "Person is swimming"


class Robot:
    def speak(self):
        return "Beep boop!"
    
    def swim(self):
        return "Robot cannot swim (error: water damage)"


def make_it_speak_and_swim(entity):
    """
    Duck typing: If it walks like a duck and quacks like a duck, it's a duck.
    We don't check the type, we just try to call the methods.
    """
    print(entity.speak())
    print(entity.swim())


# ============================================================================
# Example 4: Polymorphism in Action - File System
class FileSystemItem:
    def __init__(self, name):
        self.name = name
    
    def get_size(self):
        raise NotImplementedError
    
    def display(self, indent=0):
        raise NotImplementedError


class File(FileSystemItem):
    def __init__(self, name, size_kb):
        super().__init__(name)
        self.size_kb = size_kb
    
    def get_size(self):
        return self.size_kb
    
    def display(self, indent=0):
        return "  " * indent + f"📄 {self.name} ({self.size_kb} KB)"


class Folder(FileSystemItem):
    def __init__(self, name):
        super().__init__(name)
        self.items = []
    
    def add_item(self, item):
        self.items.append(item)
    
    def get_size(self):
        # Polymorphism: call get_size() on different types
        return sum(item.get_size() for item in self.items)
    
    def display(self, indent=0):
        result = "  " * indent + f"📁 {self.name}/\n"
        for item in self.items:
            result += item.display(indent + 1) + "\n"
        return result.rstrip()


# Testing Polymorphism
if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: PAYMENT PROCESSING POLYMORPHISM")
    print("=" * 70)
    
    # Different payment methods, same interface
    payment_methods = [
        CreditCard("1234-5678-9012-3456", "123"),
        PayPal("user@email.com"),
        Bitcoin("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
    ]
    
    total = 99.99
    for payment in payment_methods:
        print(f"\n{payment.name}:")
        print(payment.process_payment(total))
        print(payment.get_receipt(total))
    
    print("\n" + "=" * 70)
    print("EXAMPLE 2: DATA PROCESSING POLYMORPHISM")
    print("=" * 70)
    
    processors = [
        (TextProcessor(), "hello world"),
        (NumberProcessor(), [1, 2, 3, 4, 5]),
        (ListProcessor(), [5, 2, 8, 1, 9])
    ]
    
    for processor, data in processors:
        print(f"\n{processor.__class__.__name__}:")
        print(f"  Input: {data}")
        print(f"  Output: {processor.process(data)}")
    
    print("\n" + "=" * 70)
    print("EXAMPLE 3: DUCK TYPING")
    print("=" * 70)
    
    entities = [Duck(), Person(), Robot()]
    for entity in entities:
        print(f"\n{entity.__class__.__name__}:")
        make_it_speak_and_swim(entity)
    
    print("\n" + "=" * 70)
    print("EXAMPLE 4: FILE SYSTEM POLYMORPHISM")
    print("=" * 70)
    
    # Create file system structure
    root = Folder("root")
    
    docs = Folder("documents")
    docs.add_item(File("report.pdf", 250))
    docs.add_item(File("notes.txt", 15))
    
    images = Folder("images")
    images.add_item(File("photo1.jpg", 1200))
    images.add_item(File("photo2.jpg", 1500))
    
    root.add_item(docs)
    root.add_item(images)
    root.add_item(File("readme.md", 8))
    
    # Polymorphism in action: both File and Folder have get_size() and display()
    print(root.display())
    print(f"\nTotal size: {root.get_size()} KB")

"""
KEY TAKEAWAYS:
1. Polymorphism allows treating different objects through a common interface
2. Different classes can implement the same method differently
3. The correct method is called based on the object's actual type (runtime)
4. Python uses "duck typing" - if it has the method, you can call it
5. Polymorphism makes code more flexible and maintainable
6. Common parent classes define the interface

BENEFITS OF POLYMORPHISM:
1. Flexibility: Easy to add new types without changing existing code
2. Maintainability: Changes to one class don't affect others
3. Extensibility: New classes can be added that work with existing code
4. Code Reusability: Same function/loop works with multiple types
5. Abstraction: Hide implementation details behind common interface

REAL-WORLD USES:
- Payment processing (multiple payment methods)
- File handling (different file types)
- Database connections (MySQL, PostgreSQL, MongoDB)
- UI components (buttons, inputs, dropdowns)
- Game entities (players, enemies, NPCs)
- Notification systems (email, SMS, push notifications)
"""
```

---

## Exercises

**Exercise 1.** Write three classes `Dog`, `Cat`, and `Duck`, each with a `speak()` method that returns a species-appropriate string. Then write a function `animal_chorus(animals)` that iterates over a list and prints each animal's sound. Demonstrate duck typing by adding a `RobotDog` class that is not related by inheritance but has a `speak()` method.

??? success "Solution to Exercise 1"
    ```python
    class Dog:
        def speak(self):
            return "Woof!"

    class Cat:
        def speak(self):
            return "Meow!"

    class Duck:
        def speak(self):
            return "Quack!"

    class RobotDog:
        def speak(self):
            return "Beep-boop-bark!"

    def animal_chorus(animals):
        for animal in animals:
            print(animal.speak())

    animals = [Dog(), Cat(), Duck(), RobotDog()]
    animal_chorus(animals)
    # Woof!
    # Meow!
    # Quack!
    # Beep-boop-bark!
    ```

    `RobotDog` has no inheritance relationship with the other classes, but the function works because Python only cares that the object has a `speak()` method (duck typing).

---

**Exercise 2.** Predict the output of the following code.

```python
class Base:
    def identify(self):
        return "Base"

class ChildA(Base):
    def identify(self):
        return "ChildA"

class ChildB(Base):
    pass

items = [Base(), ChildA(), ChildB()]
for item in items:
    print(item.identify())
```

??? success "Solution to Exercise 2"
    The output is:

    ```
    Base
    ChildA
    Base
    ```

    `Base().identify()` calls the `Base` version. `ChildA().identify()` calls the overridden version in `ChildA`. `ChildB` does not override `identify()`, so it inherits the `Base` version and prints `"Base"`.

---

**Exercise 3.** Create a `Vector` class that supports addition (`+`), subtraction (`-`), equality (`==`), and string representation (`str()`). Each vector has two components `x` and `y`. Demonstrate operator overloading by computing `Vector(1, 2) + Vector(3, 4)`.

??? success "Solution to Exercise 3"
    ```python
    class Vector:
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __add__(self, other):
            return Vector(self.x + other.x, self.y + other.y)

        def __sub__(self, other):
            return Vector(self.x - other.x, self.y - other.y)

        def __eq__(self, other):
            return self.x == other.x and self.y == other.y

        def __str__(self):
            return f"Vector({self.x}, {self.y})"

        def __repr__(self):
            return f"Vector({self.x}, {self.y})"

    v1 = Vector(1, 2)
    v2 = Vector(3, 4)

    print(v1 + v2)        # Vector(4, 6)
    print(v2 - v1)        # Vector(2, 2)
    print(v1 == Vector(1, 2))  # True
    ```

---

**Exercise 4.** Write a polymorphic function `describe_all(items)` that calls `describe()` on each element. Create three unrelated classes (`Book`, `Movie`, `Song`) that each implement `describe()`. This exercise illustrates that Python polymorphism does not require a shared base class.

??? success "Solution to Exercise 4"
    ```python
    class Book:
        def __init__(self, title):
            self.title = title
        def describe(self):
            return f"Book: {self.title}"

    class Movie:
        def __init__(self, title):
            self.title = title
        def describe(self):
            return f"Movie: {self.title}"

    class Song:
        def __init__(self, title):
            self.title = title
        def describe(self):
            return f"Song: {self.title}"

    def describe_all(items):
        for item in items:
            print(item.describe())

    media = [Book("1984"), Movie("Inception"), Song("Bohemian Rhapsody")]
    describe_all(media)
    # Book: 1984
    # Movie: Inception
    # Song: Bohemian Rhapsody
    ```

---

**Exercise 5.** Explain the difference between polymorphism through inheritance and Python's duck typing. Write a short code example that shows the same function working with objects from completely unrelated class hierarchies, and explain why it works.

??? success "Solution to Exercise 5"
    **Inheritance-based polymorphism** requires classes to share a common parent. A function accepts a base type, and each subclass provides its own implementation of the same method.

    **Duck typing** does not require any shared base class. Python only checks at runtime whether the object has the required method. If it does, the call succeeds regardless of the object's type.

    ```python
    class Printer:
        def output(self):
            return "Printing a document"

    class Speaker:
        def output(self):
            return "Playing audio"

    class Monitor:
        def output(self):
            return "Displaying image"

    def activate(device):
        # No type checking — just calls .output()
        print(device.output())

    # These classes share no base class, yet the function works
    activate(Printer())   # Printing a document
    activate(Speaker())   # Playing audio
    activate(Monitor())   # Displaying image
    ```

    This works because Python follows the principle "if it has the right method, use it." No `isinstance` check or shared base class is needed.
