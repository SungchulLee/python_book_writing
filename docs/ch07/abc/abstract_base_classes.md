# Abstract Base Classes (ABC)

Abstract Base Classes define interfaces that subclasses must implement. They provide a way to enforce contracts and enable polymorphism with explicit structure. While Python's duck typing is flexible, it offers no guarantee that a class actually implements the methods a caller expects. ABCs fill this gap by letting you declare required methods up front and catching missing implementations at instantiation time rather than deep in a call stack.

!!! note "Mental Model"
    **ABC = nominal contract + optional shared implementation.** A class must
    explicitly inherit from the ABC (nominal typing), implement every abstract
    method, and optionally reuse concrete methods the ABC provides. This stands in
    contrast to `typing.Protocol`, which uses structural typing — no inheritance
    required, just matching method signatures.

```python
from abc import ABC, abstractmethod
```

---

## Why Use ABCs?

### The Problem: Duck Typing Limitations

Duck typing ("if it quacks like a duck...") is flexible but has issues:

```python
# Duck typing - no enforcement
class Duck:
    def quack(self):
        print("Quack!")

class Person:
    def quack(self):
        print("I'm pretending to be a duck!")

# Both work, but Person isn't really a duck
def make_it_quack(thing):
    thing.quack()  # Works for both, but is Person valid?
```

### The Solution: ABCs

ABCs explicitly define what methods a class must have:

```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def fly(self):
        """All birds must implement fly()"""
        pass
    
    @abstractmethod
    def make_sound(self):
        """All birds must implement make_sound()"""
        pass

# Cannot instantiate abstract class
# bird = Bird()  # TypeError!

class Sparrow(Bird):
    def fly(self):
        return "Sparrow flies short distances"
    
    def make_sound(self):
        return "Chirp!"

# Can instantiate concrete class
sparrow = Sparrow()  # ✓ OK
```

---

## Basic ABC Definition

### Using ABC Base Class

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """Calculate the area of the shape."""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate the perimeter of the shape."""
        pass

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
        from math import pi
        return pi * self.radius ** 2
    
    def perimeter(self):
        from math import pi
        return 2 * pi * self.radius
```

### Using ABCMeta Metaclass

Alternative syntax (equivalent to inheriting from ABC). In practice, `class MyABC(ABC)` is the preferred modern form — `ABCMeta` is shown here because you will encounter it in older codebases:

```python
from abc import ABCMeta, abstractmethod

class Shape(metaclass=ABCMeta):
    @abstractmethod
    def area(self):
        pass
```

---

## Abstract Methods

### @abstractmethod

Must be implemented by all concrete subclasses:

```python
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def connect(self):
        """Establish connection to database."""
        pass
    
    @abstractmethod
    def execute(self, query):
        """Execute a query."""
        pass
    
    @abstractmethod
    def close(self):
        """Close the connection."""
        pass
```

### Abstract Properties

```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def max_speed(self):
        """Maximum speed in km/h."""
        pass
    
    @property
    @abstractmethod
    def fuel_type(self):
        """Type of fuel used."""
        pass

class Car(Vehicle):
    @property
    def max_speed(self):
        return 200
    
    @property
    def fuel_type(self):
        return "gasoline"
```

### Abstract Class Methods

```python
from abc import ABC, abstractmethod

class Serializable(ABC):
    @classmethod
    @abstractmethod
    def from_json(cls, json_str):
        """Create instance from JSON string."""
        pass
    
    @abstractmethod
    def to_json(self):
        """Convert instance to JSON string."""
        pass
```

### Abstract Static Methods

```python
from abc import ABC, abstractmethod

class Validator(ABC):
    @staticmethod
    @abstractmethod
    def validate(value):
        """Validate the given value."""
        pass
```

---

## Concrete Methods in ABCs

ABCs can have concrete (implemented) methods:

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def speak(self):
        """Must be implemented by subclass."""
        pass
    
    # Concrete method - inherited as-is
    def introduce(self):
        return f"I am {self.name} and I say: {self.speak()}"

class Dog(Animal):
    def speak(self):
        return "Woof!"

dog = Dog("Buddy")
print(dog.introduce())  # "I am Buddy and I say: Woof!"
```

---

## Default Implementation

Abstract methods can have a body that serves as a default implementation. Subclasses must still override the method (it is still abstract), but they can call `super()` to reuse the default logic:

```python
from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message):
        """Log a message. Subclasses should call super()."""
        # This body is a *default* — subclasses MUST still override,
        # but can call super().log() to reuse this logic.
        print(f"[{self.__class__.__name__}] {message}")

class FileLogger(Logger):
    def log(self, message):
        super().log(message)  # Call default implementation
        # Additional file-specific logging
        with open("log.txt", "a") as f:
            f.write(message + "\n")
```

!!! warning "Abstract methods with bodies must still be overridden"
    Even though `Logger.log` has a full method body, the `@abstractmethod` decorator
    still prevents direct instantiation of `Logger`. Subclasses **must** override
    the method — the body is purely opt-in for subclasses that choose to call
    `super()`. This surprises many developers who expect a body to make the method
    concrete.

---

## Checking Implementation

### isinstance() and issubclass()

```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Drawable):
    def draw(self):
        return "Drawing circle"

circle = Circle()

print(isinstance(circle, Drawable))  # True
print(issubclass(Circle, Drawable))  # True
```

### __subclasshook__

Customize isinstance/issubclass behavior:

```python
from abc import ABC, abstractmethod

class Iterable(ABC):
    @abstractmethod
    def __iter__(self):
        pass
    
    @classmethod
    def __subclasshook__(cls, C):
        if cls is Iterable:
            if hasattr(C, '__iter__'):
                return True
        return NotImplemented

# Now any class with __iter__ is considered Iterable
class MyContainer:
    def __iter__(self):
        return iter([1, 2, 3])

print(isinstance(MyContainer(), Iterable))  # True
```

---

## Built-in ABCs

Python's `collections.abc` module provides many useful ABCs:

```python
from collections.abc import (
    Iterable,      # Has __iter__
    Iterator,      # Has __iter__ and __next__
    Sequence,      # Has __getitem__ and __len__
    MutableSequence,  # Sequence + __setitem__, __delitem__, insert
    Mapping,       # Has __getitem__, __iter__, __len__
    MutableMapping,   # Mapping + __setitem__, __delitem__
    Set,           # Has __contains__, __iter__, __len__
    Callable,      # Has __call__
    Hashable,      # Has __hash__
)

# Check if something is iterable
from collections.abc import Iterable
print(isinstance([1, 2, 3], Iterable))  # True
print(isinstance(42, Iterable))          # False
```

### Implementing Collection ABCs

```python
from collections.abc import Sequence

class MyList(Sequence):
    def __init__(self, data):
        self._data = list(data)
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __len__(self):
        return len(self._data)
    
    # Sequence provides: __contains__, __iter__, __reversed__,
    # index(), count() for free!

ml = MyList([1, 2, 3, 4, 5])
print(3 in ml)      # True (uses inherited __contains__)
print(ml.count(3))  # 1 (uses inherited count())
```

---

## Practical Examples

### Plugin System

```python
from abc import ABC, abstractmethod

class Plugin(ABC):
    @property
    @abstractmethod
    def name(self):
        """Plugin name."""
        pass
    
    @abstractmethod
    def execute(self, data):
        """Process data."""
        pass
    
    def __repr__(self):
        return f"<Plugin: {self.name}>"

class UppercasePlugin(Plugin):
    @property
    def name(self):
        return "uppercase"
    
    def execute(self, data):
        return data.upper()

class ReversePlugin(Plugin):
    @property
    def name(self):
        return "reverse"
    
    def execute(self, data):
        return data[::-1]

# Plugin manager
class PluginManager:
    def __init__(self):
        self.plugins = {}
    
    def register(self, plugin: Plugin):
        self.plugins[plugin.name] = plugin
    
    def process(self, name, data):
        return self.plugins[name].execute(data)
```

### Repository Pattern

```python
from abc import ABC, abstractmethod
from typing import List, Optional

class Repository(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[dict]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[dict]:
        pass
    
    @abstractmethod
    def add(self, entity: dict) -> int:
        pass
    
    @abstractmethod
    def update(self, id: int, entity: dict) -> bool:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self._data = {}
        self._next_id = 1
    
    def get(self, id: int) -> Optional[dict]:
        return self._data.get(id)
    
    def get_all(self) -> List[dict]:
        return list(self._data.values())
    
    def add(self, entity: dict) -> int:
        id = self._next_id
        self._data[id] = {**entity, 'id': id}
        self._next_id += 1
        return id
    
    def update(self, id: int, entity: dict) -> bool:
        if id in self._data:
            self._data[id] = {**entity, 'id': id}
            return True
        return False
    
    def delete(self, id: int) -> bool:
        if id in self._data:
            del self._data[id]
            return True
        return False
```

### Strategy Pattern

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with credit card {self.card_number[-4:]}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via PayPal ({self.email})"

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy: PaymentStrategy = None
    
    def set_payment(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        total = sum(item['price'] for item in self.items)
        return self.payment_strategy.pay(total)
```

---

## When to Use (and Not Use) ABCs

!!! tip "Decision Framework"
    ```text
    Use ABC when:
    - You control the class hierarchy
    - You want shared implementation (concrete methods)
    - You want runtime enforcement (TypeError at instantiation)

    Use Protocol when:
    - You don't control implementations (third-party code)
    - You want loose coupling without inheritance
    - You rely on static type checking (mypy / pyright)

    Use collections.abc when:
    - Building container-like types (Sequence, Mapping, Set)

    Use register() when:
    - Adapting legacy or third-party code to an existing ABC — only
    ```
    Don't use ABC for small projects or one-off classes — it adds ceremony without proportional benefit. Plain duck typing is fine when the interface is obvious.

!!! warning "ABC ≠ Full Runtime Safety"
    ABCs enforce that abstract methods are *defined* in subclasses, but they do not verify argument types, return values, or behavioral contracts. A subclass can implement `def area(self): return "not a number"` and Python will not complain. For richer validation, combine ABCs with type checkers like `mypy`.

---

## ABC vs Protocol

| Feature | ABC | Protocol (typing) |
|---------|-----|-------------------|
| Type | Nominal (explicit inheritance) | Structural (implicit) |
| Runtime check | `isinstance()` works | Requires `@runtime_checkable` |
| Inheritance | Required | Not required |
| Use case | Enforce implementation | Type hints, duck typing |

```python
from abc import ABC, abstractmethod
from typing import Protocol

# ABC - must inherit
class DrawableABC(ABC):
    @abstractmethod
    def draw(self): pass

class Circle(DrawableABC):  # Must inherit
    def draw(self): return "circle"

# Protocol - just implement method
class DrawableProtocol(Protocol):
    def draw(self) -> str: ...

class Square:  # No inheritance needed
    def draw(self): return "square"

# Square is compatible with DrawableProtocol
def render(shape: DrawableProtocol):
    print(shape.draw())

render(Square())  # Works!
```

---

## Summary

| Feature | Syntax |
|---------|--------|
| Define ABC | `class MyABC(ABC):` |
| Abstract method | `@abstractmethod` |
| Abstract property | `@property` + `@abstractmethod` |
| Abstract classmethod | `@classmethod` + `@abstractmethod` |
| Concrete method | Regular method in ABC |
| Check instance | `isinstance(obj, MyABC)` |

**Key Takeaways**:

- ABCs define interfaces that subclasses must implement
- Cannot instantiate a class with unimplemented abstract methods
- Use `@abstractmethod` decorator for required methods
- ABCs can have concrete methods with shared implementation
- `collections.abc` provides useful built-in ABCs
- Choose ABC for strict contracts, Protocol for structural typing

---

## Runnable Example: `abstract_base_class_example.py`

```python
"""
TUTORIAL: Abstract Base Classes (ABC) - Defining Contracts for Subclasses
==========================================================================

In this tutorial, you'll learn how to use Python's abc module to create
Abstract Base Classes. An ABC is a blueprint that enforces what methods
subclasses MUST implement.

Key concepts:
  1. ABC: A class that cannot be instantiated directly
  2. @abstractmethod: Marks methods that subclasses MUST override
  3. Concrete methods: Can provide default implementation in the ABC
  4. Inheritance: Subclasses must implement all abstract methods

Why use ABC?
  - Enforce a consistent interface across subclasses
  - Prevent accidental incomplete implementations
  - Document what subclasses must do
  - Catch errors at class definition time, not runtime

In this example, we define a Tombola (lottery machine) ABC with:
  - Abstract methods: load() and pick() that subclasses must implement
  - Concrete methods: loaded() and inspect() that use the abstract methods

This demonstrates how abstract methods serve as hooks that concrete methods
depend on, creating a reusable pattern for subclasses.
"""

import abc


# ============ Example 1: Defining an Abstract Base Class ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Creating the Tombola ABC")
    print("=" * 70)

    class Tombola(abc.ABC):
        """Abstract Base Class for a lottery machine (tombola).

        A Tombola must be able to:
        - load() items from an iterable
        - pick() random items and remove them
        - report loaded() status
        - inspect() current contents

        Subclasses MUST implement load() and pick().
        The load() and inspect() methods depend on these abstract methods
        to provide complete functionality.
        """

        @abc.abstractmethod
        def load(self, iterable):
            """Add items from an iterable to the tombola.

            This is an abstract method. Every subclass MUST override it
            with its own implementation. Without it, you cannot instantiate
            the subclass.

            Args:
                iterable: A collection of items to add to the tombola.
            """

        @abc.abstractmethod
        def pick(self):
            """Remove item at random from the tombola, returning it.

            This is an abstract method. Every subclass MUST override it
            with its own implementation.

            Returns:
                A randomly selected item from the tombola.

            Raises:
                LookupError: When the tombola is empty.
            """

        def loaded(self):
            """Return True if there's at least 1 item, False otherwise.

            This is a concrete method. It provides a default implementation
            that uses the abstract method pick() as a hook.

            Note: This method works with ANY subclass that implements
            load() and pick(), making it reusable across all subclasses.
            """
            return bool(self.inspect())

        def inspect(self):
            """Return a sorted tuple with the items currently inside.

            This is a concrete method that uses the abstract methods:
            1. Calls pick() repeatedly to get all items
            2. Calls load() to restore the items after inspection

            This demonstrates how concrete methods can depend on
            abstract methods to provide sophisticated behavior.

            Returns:
                tuple: Sorted tuple of all items in the tombola.
            """
            items = []
            while True:
                try:
                    # Keep picking items until empty
                    items.append(self.pick())
                except LookupError:
                    # Empty - break the loop
                    break

            # Restore the items we removed
            self.load(items)

            # Return sorted tuple of contents
            return tuple(items)


    print(f"\nTombola ABC defined with:")
    print(f"  - Abstract methods: load(), pick()")
    print(f"  - Concrete methods: loaded(), inspect()")
    print(f"\nTrying to instantiate Tombola directly...")

    try:
        tombola = Tombola()
        print(f"  ERROR: This should have failed!")
    except TypeError as e:
        print(f"  Result: TypeError")
        print(f"  Message: {e}")
        print(f"  WHY? ABC classes cannot be instantiated directly")


    # ============ Example 2: Creating a Concrete Subclass ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Implementing a concrete subclass (BingoTombola)")
    print("=" * 70)

    import random

    class BingoTombola(Tombola):
        """A Tombola implementation using a list to store items.

        This concrete subclass implements the two abstract methods
        that Tombola requires.
        """

        def __init__(self):
            """Initialize an empty bingo tombola."""
            self._items = []

        def load(self, iterable):
            """Load items from an iterable into the list.

            Args:
                iterable: Items to add to the tombola.
            """
            self._items.extend(iterable)

        def pick(self):
            """Remove and return a random item.

            Returns:
                A random item from _items.

            Raises:
                LookupError: When the list is empty.
            """
            try:
                position = random.randrange(len(self._items))
            except ValueError:
                raise LookupError('pick from empty Tombola') from None
            return self._items.pop(position)

        def __call__(self):
            """Return self for compatibility."""
            return self


    print(f"\nBingoTombola created - a concrete subclass of Tombola")
    print(f"It implements both abstract methods:")
    print(f"  - load(iterable): Stores items in self._items")
    print(f"  - pick(): Removes and returns a random item")

    # Create an instance
    bingo = BingoTombola()
    print(f"\nbingo = BingoTombola()")
    print(f"  Instance created successfully (it's a proper subclass)")


    # ============ Example 3: Using the Concrete Subclass ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Using BingoTombola - load and inspect")
    print("=" * 70)

    # Load some items
    numbers = range(1, 7)
    bingo.load(numbers)

    print(f"\nbingo.load(range(1, 7))  # Load numbers 1-6")
    print(f"  Items loaded into tombola")

    # Check if loaded
    print(f"\nbingo.loaded()  # Check if anything is loaded")
    print(f"  Result: {bingo.loaded()}")
    print(f"  WHY? inspect() called pick() and found items")

    # Inspect contents
    contents = bingo.inspect()
    print(f"\nbingo.inspect()  # Get all items without modifying")
    print(f"  Result: {contents}")
    print(f"  Note: Still loaded after inspect (load() restored items)")


    # ============ Example 4: Picking Items and Emptying ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Picking items one at a time")
    print("=" * 70)

    bingo2 = BingoTombola()
    bingo2.load(['a', 'b', 'c', 'd', 'e'])

    print(f"\nbingo2.load(['a', 'b', 'c', 'd', 'e'])")
    print(f"bingo2.loaded() = {bingo2.loaded()}")

    print(f"\nPicking 3 items:")
    for i in range(3):
        item = bingo2.pick()
        print(f"  Pick {i+1}: {item}")

    print(f"\nRemaining items via inspect():")
    print(f"  bingo2.inspect() = {bingo2.inspect()}")

    print(f"\nbingo2.loaded() = {bingo2.loaded()}")
    print(f"  Still has items")

    # Pick remaining items
    print(f"\nPicking remaining items until empty:")
    try:
        while True:
            item = bingo2.pick()
            print(f"  Picked: {item}")
    except LookupError as e:
        print(f"  LookupError: {e}")
        print(f"  WHY? No more items in tombola")

    print(f"\nbingo2.loaded() = {bingo2.loaded()}")
    print(f"  Now empty after all picks")


    # ============ Example 5: Why Abstract Methods Matter ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Attempted incomplete subclass - this would fail")
    print("=" * 70)

    print(f"\nAttempting to create incomplete subclass:")
    print(f"  class IncompleteTombola(Tombola):")
    print(f"      def load(self, iterable): pass")
    print(f"      # Missing pick() implementation\n")

    try:
        class IncompleteTombola(Tombola):
            def load(self, iterable):
                pass
            # Forgot to implement pick()

        incomplete = IncompleteTombola()
        print(f"  ERROR: This should have failed!")
    except TypeError as e:
        print(f"  Result: TypeError")
        print(f"  Message: {e}")
        print(f"  WHY? Class definition fails if not all abstract methods")
        print(f"       are implemented. This catches errors early!")


    # ============ Example 6: How Concrete Methods Depend on Abstract Methods ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Concrete methods using abstract method hooks")
    print("=" * 70)

    print(f"\nThe inspect() method is elegant because:")
    print(f"  1. It's defined once in the ABC")
    print(f"  2. It works for ANY concrete subclass")
    print(f"  3. It 'hooks' into pick() and load()")

    print(f"\nFlow of inspect() for BingoTombola:")
    print(f"  1. Loop: bingo.pick() [abstract hook]")
    print(f"     - Removes items from _items list")
    print(f"     - Raises LookupError when empty")
    print(f"  2. Collect all items into a list")
    print(f"  3. Restore: bingo.load(items) [abstract hook]")
    print(f"     - Puts items back without modification")
    print(f"  4. Return tuple(items)")

    print(f"\nBecause load() and pick() are abstract hooks,")
    print(f"each subclass can have different storage mechanisms")
    print(f"but inspect() works the same way for all of them!")


    # ============ Example 7: Another Subclass - Different Implementation ============
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Alternative subclass with different storage (LotteryTombola)")
    print("=" * 70)

    class LotteryTombola(Tombola):
        """A Tombola implementation using a set instead of a list.

        This shows that different implementations can use different
        internal data structures while satisfying the same interface.
        """

        def __init__(self):
            """Initialize an empty lottery tombola."""
            self._numbers = set()

        def load(self, iterable):
            """Add numbers to the set.

            Args:
                iterable: Numbers to add.
            """
            self._numbers.update(iterable)

        def pick(self):
            """Remove and return a random number.

            Returns:
                A random number from the set.

            Raises:
                LookupError: When the set is empty.
            """
            if not self._numbers:
                raise LookupError('pick from empty LotteryTombola')
            # Convert to list, pick random, remove from set
            value = random.choice(list(self._numbers))
            self._numbers.discard(value)
            return value


    lottery = LotteryTombola()
    lottery.load([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    print(f"\nlottery = LotteryTombola()")
    print(f"lottery.load(range(1, 11))")

    print(f"\nlottery.loaded() = {lottery.loaded()}")
    print(f"lottery.inspect() = {lottery.inspect()}")

    print(f"\nLotteryTombola uses a different storage mechanism (set)")
    print(f"but provides the SAME interface as BingoTombola!")
    print(f"This is the power of ABC - enforcing a contract.")


    # ============ Example 8: Summary - Why Use ABC? ============
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Summary - Benefits of Abstract Base Classes")
    print("=" * 70)

    print(f"\nBenefits of ABC:")
    print(f"  1. CONTRACT: Forces subclasses to implement required methods")
    print(f"     - TypeError raised at class definition if incomplete")
    print(f"     - Errors caught early, not at runtime")

    print(f"  2. REUSABILITY: Concrete methods work for all subclasses")
    print(f"     - inspect() works the same for BingoTombola and LotteryTombola")
    print(f"     - Hooks (load, pick) allow customization")

    print(f"  3. DOCUMENTATION: Clear what subclasses must do")
    print(f"     - Docstrings on abstract methods guide implementers")
    print(f"     - Self-documenting code")

    print(f"  4. CONSISTENCY: All subclasses have same interface")
    print(f"     - Users know what methods exist")
    print(f"     - Polymorphism works correctly")

    print(f"\nWhen to use ABC:")
    print(f"  - Designing a framework or library")
    print(f"  - Multiple related classes should follow same interface")
    print(f"  - Want to prevent incomplete implementations")
    print(f"  - Need polymorphic behavior")

    print(f"\n" + "=" * 70)
```

---

## Exercises

**Exercise 1.**
Define an abstract base class `Exporter` with two abstract methods: `export(data)` and `file_extension()` (as an abstract property). Then create two concrete subclasses, `CSVExporter` and `JSONExporter`, each implementing both abstract methods. Demonstrate that `Exporter` cannot be instantiated directly, but both concrete subclasses can.

??? success "Solution to Exercise 1"

        from abc import ABC, abstractmethod

        class Exporter(ABC):
            @abstractmethod
            def export(self, data):
                """Export data in a specific format."""
                pass

            @property
            @abstractmethod
            def file_extension(self):
                """Return the file extension for this format."""
                pass

        class CSVExporter(Exporter):
            @property
            def file_extension(self):
                return ".csv"

            def export(self, data):
                header = ",".join(data[0].keys())
                rows = [",".join(str(v) for v in row.values()) for row in data]
                return header + "\n" + "\n".join(rows)

        class JSONExporter(Exporter):
            @property
            def file_extension(self):
                return ".json"

            def export(self, data):
                import json
                return json.dumps(data, indent=2)

        # Exporter cannot be instantiated
        try:
            e = Exporter()
        except TypeError as err:
            print(f"Cannot instantiate Exporter: {err}")

        # Concrete subclasses work
        data = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
        csv_exp = CSVExporter()
        print(csv_exp.file_extension)  # .csv
        print(csv_exp.export(data))

        json_exp = JSONExporter()
        print(json_exp.file_extension)  # .json
        print(json_exp.export(data))

---

**Exercise 2.**
Create an ABC called `Validator` with an abstract method `validate(value)` that returns `True` or `False`, and a concrete method `validate_many(values)` that applies `validate` to each item in a list and returns a list of booleans. Implement `EmailValidator` (checks for `@` in the string) and `PositiveNumberValidator` (checks that a number is greater than zero). Show that the concrete method works correctly for both subclasses without being overridden.

??? success "Solution to Exercise 2"

        from abc import ABC, abstractmethod

        class Validator(ABC):
            @abstractmethod
            def validate(self, value):
                """Return True if value is valid, False otherwise."""
                pass

            def validate_many(self, values):
                """Apply validate to each item and return list of booleans."""
                return [self.validate(v) for v in values]

        class EmailValidator(Validator):
            def validate(self, value):
                return isinstance(value, str) and "@" in value

        class PositiveNumberValidator(Validator):
            def validate(self, value):
                return isinstance(value, (int, float)) and value > 0

        email_v = EmailValidator()
        print(email_v.validate_many(["a@b.com", "invalid", "x@y"]))
        # [True, False, True]

        num_v = PositiveNumberValidator()
        print(num_v.validate_many([10, -3, 0, 5.5]))
        # [True, False, False, True]

---

**Exercise 3.**
Write an ABC `NotificationSender` with abstract methods `send(recipient, message)` and `validate_recipient(recipient)`. Create a concrete subclass `EmailSender` that validates email format and simulates sending. Then create a separate class `SMSSender` (without inheriting from `NotificationSender`) that has the same methods, and use `NotificationSender.register(SMSSender)` to make it a virtual subclass. Verify that `isinstance` checks pass for both classes.

??? success "Solution to Exercise 3"

        from abc import ABC, abstractmethod

        class NotificationSender(ABC):
            @abstractmethod
            def send(self, recipient, message):
                pass

            @abstractmethod
            def validate_recipient(self, recipient):
                pass

        class EmailSender(NotificationSender):
            def validate_recipient(self, recipient):
                return isinstance(recipient, str) and "@" in recipient

            def send(self, recipient, message):
                if not self.validate_recipient(recipient):
                    raise ValueError(f"Invalid email: {recipient}")
                print(f"Email sent to {recipient}: {message}")

        class SMSSender:
            def validate_recipient(self, recipient):
                return isinstance(recipient, str) and recipient.isdigit() and len(recipient) >= 10

            def send(self, recipient, message):
                if not self.validate_recipient(recipient):
                    raise ValueError(f"Invalid phone: {recipient}")
                print(f"SMS sent to {recipient}: {message}")

        # Register SMSSender as virtual subclass
        NotificationSender.register(SMSSender)

        email = EmailSender()
        sms = SMSSender()

        print(isinstance(email, NotificationSender))  # True
        print(isinstance(sms, NotificationSender))    # True

        email.send("alice@example.com", "Hello!")
        sms.send("1234567890", "Hi there!")

---

**Exercise 4.**
Explain why the following code raises a `TypeError` at instantiation, even though `PartialShape` defines `area()`. What must be done to fix it?

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

class PartialShape(Shape):
    def area(self):
        return 0

shape = PartialShape()
```

??? success "Solution to Exercise 4"

    `PartialShape` implements `area()` but does **not** implement `perimeter()`. Python's ABC machinery tracks all abstract methods and prevents instantiation unless **every** one is overridden. The error message will be:

        TypeError: Can't instantiate abstract class PartialShape with abstract method perimeter

    To fix it, add the missing method:

        class PartialShape(Shape):
            def area(self):
                return 0

            def perimeter(self):
                return 0

    This illustrates the core value of ABCs: incomplete implementations are caught at instantiation time, not when `perimeter()` is eventually called deep inside another method.

---

**Exercise 5.**
Consider the `Logger` ABC shown in the Default Implementation section. Describe what happens if `FileLogger` does **not** call `super().log(message)`. Does `FileLogger` still satisfy the ABC contract? Under what circumstances would omitting `super()` be a design mistake versus an intentional choice?

??? success "Solution to Exercise 5"

    Yes, `FileLogger` still satisfies the ABC contract — it overrides the abstract `log()` method, which is all that `@abstractmethod` requires. The `super().log()` call is entirely optional.

    **Omitting `super()` is intentional** when the subclass provides a completely different implementation that does not need the parent's behavior. For example, a `NullLogger` that silently discards messages would have no reason to call `super()`.

    **Omitting `super()` is a mistake** when the ABC's default implementation provides shared setup logic that all subclasses should run (e.g., timestamp formatting, log-level filtering). In that case, forgetting `super()` silently skips that shared logic, leading to inconsistent behavior across subclasses.

    This highlights a limitation of ABCs: they can enforce that a method *exists*, but they cannot enforce that it *calls `super()`*. When the default implementation is load-bearing, document the expectation clearly in the docstring.
