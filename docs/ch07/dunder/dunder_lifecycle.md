# Object Lifecycle

Lifecycle dunder methods control how objects are created, initialized, and destroyed.

!!! tip "Mental Model"
    Object creation is a two-phase process: `__new__` allocates the blank object (like pouring a foundation), and `__init__` furnishes it with state (like moving in the furniture). Destruction via `__del__` is unreliable -- think of it as a "maybe" cleanup. For deterministic resource management, use context managers instead.

## Overview: Object Creation Flow

```
MyClass(args)
    ↓
MyClass.__new__(cls, args)   → Creates instance
    ↓
MyClass.__init__(self, args) → Initializes instance
    ↓
(object used)
    ↓
MyClass.__del__(self)        → Called before destruction (unreliable)
```

## `__new__`: Object Creation

`__new__` is a static method that creates and returns a new instance.

### Basic __new__

```python
class MyClass:
    def __new__(cls, *args, **kwargs):
        print(f"Creating instance of {cls.__name__}")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, value):
        print(f"Initializing with value={value}")
        self.value = value

obj = MyClass(42)
# Output:
# Creating instance of MyClass
# Initializing with value=42
```

### When to Use __new__

`__new__` is rarely needed, but useful for:

1. **Subclassing immutable types** (str, int, tuple)
2. **Implementing singletons**
3. **Object caching/flyweight pattern**
4. **Custom metaclasses**

## Subclassing Immutable Types

Immutable types must be modified in `__new__` because `__init__` is too late.

```python
class UpperStr(str):
    """String that's always uppercase."""
    
    def __new__(cls, value):
        # Must modify in __new__ - str is immutable
        instance = super().__new__(cls, value.upper())
        return instance

s = UpperStr("hello")
print(s)         # HELLO
print(type(s))   # <class '__main__.UpperStr'>
```

```python
class EvenInt(int):
    """Integer that rounds to nearest even number."""
    
    def __new__(cls, value):
        # Round to nearest even
        rounded = round(value / 2) * 2
        return super().__new__(cls, rounded)

print(EvenInt(3))   # 4
print(EvenInt(4))   # 4
print(EvenInt(5))   # 6
```

```python
class NamedTuple(tuple):
    """Simple named tuple implementation."""
    
    def __new__(cls, name, values):
        instance = super().__new__(cls, values)
        instance.name = name  # Can add attributes after creation
        return instance

point = NamedTuple("origin", (0, 0))
print(point)        # (0, 0)
print(point.name)   # origin
```

## Singleton Pattern

Ensure only one instance of a class exists.

```python
class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, value=None):
        # Note: __init__ runs every time!
        if value is not None:
            self.value = value

a = Singleton(1)
b = Singleton(2)

print(a is b)      # True
print(a.value)     # 2 (overwritten by second __init__)
print(id(a), id(b))  # Same id
```

!!! warning "__init__ Runs Every Time"

    A common singleton bug: `__init__` runs **every time** you call the class, even when `__new__` returns the existing instance. In the example above, `Singleton(2)` does not create a new object, but it still executes `__init__`, overwriting `value` from `1` to `2`. The `BetterSingleton` pattern below guards against this with an `_initialized` flag. Always consider whether repeated `__init__` calls could corrupt your singleton's state.

### Singleton with Init Guard

```python
class BetterSingleton:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, value):
        if not BetterSingleton._initialized:
            self.value = value
            BetterSingleton._initialized = True

a = BetterSingleton(1)
b = BetterSingleton(2)

print(a.value)  # 1 (preserved)
print(b.value)  # 1 (same object)
```

## Object Caching / Flyweight Pattern

Reuse existing objects for identical values.

```python
class CachedInt:
    _cache = {}
    
    def __new__(cls, value):
        if value in cls._cache:
            return cls._cache[value]
        
        instance = super().__new__(cls)
        instance.value = value
        cls._cache[value] = instance
        return instance
    
    def __init__(self, value):
        pass  # Already initialized in __new__
    
    def __repr__(self):
        return f"CachedInt({self.value})"

a = CachedInt(5)
b = CachedInt(5)
c = CachedInt(10)

print(a is b)  # True (same cached object)
print(a is c)  # False (different value)
```

### LRU Cache for Limited Memory

```python
from collections import OrderedDict

class LRUCachedObject:
    _cache = OrderedDict()
    _max_size = 100
    
    def __new__(cls, key):
        if key in cls._cache:
            # Move to end (most recently used)
            cls._cache.move_to_end(key)
            return cls._cache[key]
        
        instance = super().__new__(cls)
        instance.key = key
        
        cls._cache[key] = instance
        if len(cls._cache) > cls._max_size:
            cls._cache.popitem(last=False)  # Remove oldest
        
        return instance
```

## `__init__`: Object Initialization

`__init__` initializes an already-created instance.

### Basic __init__

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self._validate()
    
    def _validate(self):
        if self.age < 0:
            raise ValueError("Age cannot be negative")

p = Person("Alice", 30)
print(p.name)  # Alice
```

### __init__ Must Return None

```python
class Wrong:
    def __init__(self, value):
        self.value = value
        return self  # TypeError!

# TypeError: __init__() should return None, not 'Wrong'
```

### Flexible Initialization

```python
class Connection:
    def __init__(self, host=None, port=None, *, url=None):
        if url:
            # Parse URL
            self.host, self.port = self._parse_url(url)
        else:
            self.host = host or 'localhost'
            self.port = port or 8080
    
    def _parse_url(self, url):
        # Simplified parsing
        parts = url.replace('://', ':').split(':')
        return parts[1], int(parts[2])
    
    def __repr__(self):
        return f"Connection({self.host}:{self.port})"

# Multiple initialization patterns
c1 = Connection('example.com', 443)
c2 = Connection(url='https://api.example.com:8443')
c3 = Connection()  # defaults

print(c1)  # Connection(example.com:443)
print(c2)  # Connection(api.example.com:8443)
print(c3)  # Connection(localhost:8080)
```

## `__del__`: Object Destruction

`__del__` is called when an object is about to be garbage-collected. **Avoid `__del__` in real code** unless you have a thorough understanding of Python's garbage collector. Its timing is unpredictable, it may never run (circular references, interpreter shutdown), and exceptions raised inside it are silently ignored. Use context managers (`with` statements) for reliable cleanup instead.

### Basic __del__

```python
class Resource:
    def __init__(self, name):
        self.name = name
        print(f"Acquiring {name}")
    
    def __del__(self):
        print(f"Releasing {self.name}")

r = Resource("database connection")
# Acquiring database connection
del r
# Releasing database connection
```

### Why __del__ is Unreliable

```python
# Problem 1: Timing is unpredictable
class Unreliable:
    def __del__(self):
        print("Destructor called")

obj = Unreliable()
obj = None  # May or may not trigger __del__ immediately

# Problem 2: Circular references may prevent __del__
class Node:
    def __init__(self):
        self.ref = None
    
    def __del__(self):
        print("Node destroyed")

a = Node()
b = Node()
a.ref = b
b.ref = a  # Circular reference
del a, b   # __del__ may never be called!

# Problem 3: Exceptions in __del__ are ignored
class BadDestructor:
    def __del__(self):
        raise RuntimeError("Oops!")  # Silently ignored

obj = BadDestructor()
del obj  # No exception raised, just a warning
```

### Better Alternative: Context Managers

```python
class Resource:
    def __init__(self, name):
        self.name = name
    
    def __enter__(self):
        print(f"Acquiring {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing {self.name}")
        return False
    
    def use(self):
        print(f"Using {self.name}")

# Guaranteed cleanup with context manager
with Resource("database") as r:
    r.use()
# Releasing happens even if exception occurs
```

## Complete Lifecycle Example

```python
class TrackedObject:
    _count = 0
    
    def __new__(cls, name):
        print(f"1. __new__: Creating instance of {cls.__name__}")
        instance = super().__new__(cls)
        return instance
    
    def __init__(self, name):
        print(f"2. __init__: Initializing with name={name}")
        self.name = name
        TrackedObject._count += 1
        self.id = TrackedObject._count
    
    def __repr__(self):
        return f"TrackedObject(name={self.name!r}, id={self.id})"
    
    def __del__(self):
        print(f"3. __del__: Destroying {self.name} (id={self.id})")

print("Creating object:")
obj = TrackedObject("test")
print(f"Object: {obj}")
print("\nDeleting object:")
del obj
print("Done")

# Output:
# Creating object:
# 1. __new__: Creating instance of TrackedObject
# 2. __init__: Initializing with name=test
# Object: TrackedObject(name='test', id=1)
#
# Deleting object:
# 3. __del__: Destroying test (id=1)
# Done
```

## Factory Methods Using __new__

```python
class Shape:
    def __new__(cls, shape_type, *args):
        if cls is not Shape:
            # Called on subclass, proceed normally
            return super().__new__(cls)
        
        # Factory: create appropriate subclass
        if shape_type == 'circle':
            return Circle.__new__(Circle)
        elif shape_type == 'square':
            return Square.__new__(Square)
        else:
            raise ValueError(f"Unknown shape: {shape_type}")

class Circle(Shape):
    def __init__(self, shape_type, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

class Square(Shape):
    def __init__(self, shape_type, side):
        self.side = side
    
    def area(self):
        return self.side ** 2

# Factory usage
c = Shape('circle', 5)
s = Shape('square', 4)
print(type(c))    # <class '__main__.Circle'>
print(c.area())   # 78.53975
print(type(s))    # <class '__main__.Square'>
print(s.area())   # 16
```

## __init_subclass__: Customizing Subclass Creation

Python 3.6+ provides `__init_subclass__` for customizing subclass behavior.

```python
class Plugin:
    _registry = {}
    
    def __init_subclass__(cls, name=None, **kwargs):
        super().__init_subclass__(**kwargs)
        plugin_name = name or cls.__name__.lower()
        Plugin._registry[plugin_name] = cls
        print(f"Registered plugin: {plugin_name}")
    
    @classmethod
    def get_plugin(cls, name):
        return cls._registry.get(name)

class AudioPlugin(Plugin, name='audio'):
    pass

class VideoPlugin(Plugin):  # Uses class name
    pass

# Output:
# Registered plugin: audio
# Registered plugin: videoplugin

print(Plugin._registry)
# {'audio': <class 'AudioPlugin'>, 'videoplugin': <class 'VideoPlugin'>}
```

## Key Takeaways

- `__new__` creates instances; use for immutables, singletons, caching
- `__init__` initializes instances; most common place for setup
- `__del__` is unreliable; prefer context managers for cleanup
- `__new__` receives class, `__init__` receives instance
- `__new__` must return an instance; `__init__` must return `None`
- For reliable cleanup, use `with` statements and `__enter__`/`__exit__`
- Use `__init_subclass__` to customize subclass creation (Python 3.6+)

---

## Runnable Example: `sequence_protocol_example.py`

```python
"""
TUTORIAL: The Sequence Protocol - Making Custom Objects Behave Like Lists

This tutorial teaches you how to implement __len__ and __getitem__ dunder methods
to make a custom class support the sequence protocol. We'll build a FrenchDeck class
that behaves like a sequence - you can call len() on it, index into it, and slice it,
just like with built-in lists and tuples.

Key Learning Goals:
  - Understand why dunder methods make Python more intuitive
  - Learn how __len__ and __getitem__ enable sequence behavior
  - See how minimal code enables powerful functionality
"""

import collections

if __name__ == "__main__":

    print("=" * 70)
    print("TUTORIAL: The Sequence Protocol - Custom Sequence Objects")
    print("=" * 70)

    # ============ EXAMPLE 1: Understanding Namedtuples ============
    print("\n# Example 1: Creating a Card with namedtuple")
    print("=" * 70)

    Card = collections.namedtuple('Card', ['rank', 'suit'])

    # A namedtuple is a lightweight data structure. It's perfect for simple objects
    # that need readable field names instead of just index positions.
    card1 = Card('7', 'hearts')
    card2 = Card('A', 'spades')

    print(f"Card 1: {card1}")
    print(f"Card 2: {card2}")
    print(f"Accessing card1.rank: {card1.rank}")
    print(f"Accessing card1.suit: {card1.suit}")
    print("""
    WHY: A namedtuple is perfect here because a card is just two pieces of data.
    It's more readable than Card(7, 'hearts') and faster than a full class.
    """)

    # ============ EXAMPLE 2: Building the FrenchDeck Class ============
    print("\n# Example 2: Implementing the Sequence Protocol")
    print("=" * 70)

    class FrenchDeck:
        """
        A standard 52-card French deck that implements the sequence protocol.

        By implementing __len__ and __getitem__, instances can be used wherever
        Python expects a sequence (like lists or tuples). This is a powerful example
        of "duck typing" - if it walks like a sequence and quacks like a sequence,
        Python will treat it as one.
        """

        # Class attributes: these are defined once and shared by all instances
        ranks = [str(n) for n in range(2, 11)] + list('JQKA')  # 2-10, J, Q, K, A
        suits = 'spades diamonds clubs hearts'.split()

        def __init__(self):
            """
            Initialize the deck with all 52 cards.

            We create cards by combining each suit with each rank.
            The order matters: suits loop on the outside, ranks on the inside.
            This creates: [Card(2, spades), Card(3, spades), ..., Card(A, hearts)]
            """
            self._cards = [Card(rank, suit)
                           for suit in self.suits
                           for rank in self.ranks]

        def __len__(self):
            """
            Return the number of cards in the deck.

            By implementing __len__, our deck now supports:
              - len(deck)  # returns 52
              - if deck:   # works as a boolean (empty deck = False)
              - for loop iteration works better

            This is a tiny method but incredibly powerful. Python now treats
            FrenchDeck as a sequence!
            """
            return len(self._cards)

        def __getitem__(self, position):
            """
            Return a card at a specific position or a slice of cards.

            By implementing __getitem__, our deck now supports:
              - deck[0]        # get first card
              - deck[-1]       # get last card
              - deck[1:3]      # slice operations work automatically!
              - for card in deck:  # iteration works too

            This is the key to making our class behave like a real sequence.
            We don't need separate slicing logic - Python handles it for us
            because __getitem__ can receive slice objects.
            """
            return self._cards[position]


    # ============ EXAMPLE 3: Creating and Using a Deck ============
    print("\n# Example 3: Creating a FrenchDeck")
    print("=" * 70)

    deck = FrenchDeck()

    print(f"Number of cards in deck: {len(deck)}")
    print(f"First card: {deck[0]}")
    print(f"Last card: {deck[-1]}")
    print(f"""
    WHY: We don't need to write special methods for these operations.
    By implementing __getitem__ with a list inside, Python automatically
    gives us indexing, negative indexing, and even slicing!
    """)

    # ============ EXAMPLE 4: Slicing Works Automatically ============
    print("\n# Example 4: Slicing Operations (Free From __getitem__)")
    print("=" * 70)

    first_three = deck[0:3]
    print(f"First three cards: {first_three}")

    last_five = deck[-5:]
    print(f"Last five cards: {last_five}")

    every_nth = deck[::13]  # Every 13th card (one from each suit, roughly)
    print(f"Every 13th card (samples): {every_nth}")
    print("""
    WHY: Slicing is automatic! When you write deck[0:3], Python calls
    __getitem__ with a slice(0, 3) object, and that gets passed to our
    internal list's __getitem__, which already knows how to handle slices.
    """)

    # ============ EXAMPLE 5: Iteration Works Automatically ============
    print("\n# Example 5: Iteration (Also Free From __getitem__)")
    print("=" * 70)

    print("First 5 cards when iterating:")
    for i, card in enumerate(deck):
        if i < 5:
            print(f"  Card {i}: {card}")
        else:
            break
    print("  ...")
    print(f"Total cards iterated: {len(deck)}")
    print("""
    WHY: For loops work because Python falls back to __getitem__ when __iter__
    isn't defined. It starts at index 0 and keeps incrementing until it gets
    an IndexError. This is how iteration works on sequences!
    """)

    # ============ EXAMPLE 6: Boolean Context (Free From __len__) ============
    print("\n# Example 6: Using Deck in Boolean Context")
    print("=" * 70)

    non_empty_deck = FrenchDeck()
    empty_list = []

    print(f"if deck: {bool(non_empty_deck)} (deck has {len(non_empty_deck)} cards)")
    print(f"if empty_list: {bool(empty_list)} (list is empty)")
    print("""
    WHY: Python uses __len__ to determine truthiness. Any object with a
    non-zero length is truthy. By implementing __len__, we get free boolean
    behavior!
    """)

    # ============ EXAMPLE 7: The Complete Picture ============
    print("\n# Example 7: What We Get With Just Two Methods")
    print("=" * 70)

    print("""
    By implementing just __len__ and __getitem__, FrenchDeck gets:

      ✓ len(deck)           - calls __len__
      ✓ deck[i]             - calls __getitem__
      ✓ deck[i:j]           - calls __getitem__ with slice object
      ✓ deck[-1]            - negative indexing
      ✓ for card in deck:   - iteration
      ✓ if deck: ...        - boolean context
      ✓ reversed(deck)      - calls __getitem__ with negative indices
      ✓ list(deck)          - conversion to list
      ✓ print(deck[0])      - card representation

    This is the power of the sequence protocol. Python recognizes the pattern
    and automatically enables a whole family of operations.

    KEY INSIGHT: By following Python's protocols (implementing the right dunder
    methods), we write less code and users can interact with our objects using
    all the standard Python operations they already know.
    """)

    # ============ EXAMPLE 8: Practical Use Case ============
    print("\n# Example 8: Practical Code with Our Deck")
    print("=" * 70)

    # Because we implemented the sequence protocol, we can use standard Python tools
    import random

    small_hand = random.sample(deck, 5)
    print(f"Random hand of 5 cards: {small_hand}")

    # Convert to list if needed (though it's already sequence-like)
    as_list = list(deck[:3])
    print(f"First 3 cards as list: {as_list}")

    # Use in any place that expects sequences
    def show_first_card(sequence):
        """Works with any sequence"""
        if sequence:
            return sequence[0]
        return None

    print(f"Works with functions expecting sequences: {show_first_card(deck)}")

    print("""
    WHY: Because we implemented the sequence protocol correctly, FrenchDeck
    instances work seamlessly with all standard Python tools and functions
    that expect sequences. This is duck typing in action.
    """)

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)
    print("""
    1. DUNDER METHODS ARE PROTOCOLS: Implementing __len__ and __getitem__
       is not about those specific methods - it's about implementing the
       sequence protocol, which tells Python "I'm sequence-like."

    2. MINIMAL CODE, MAXIMUM POWER: With just two methods, we unlocked
       indexing, slicing, iteration, boolean context, and more.

    3. DUCK TYPING: We don't inherit from list, we don't have a special base
       class - we just implement the right methods. Python doesn't care about
       our type, only our behavior.

    4. USERS GET FAMILIAR PYTHON: Since our deck behaves like a sequence,
       users can use all the standard Python operations they already know.
       No learning curve required.
    """)
```

---

## Exercises

**Exercise 1.**
Create a class `TrackedObject` that prints a message in `__init__` when created and in `__del__` when destroyed. Create an instance, assign it to a second variable, then delete the first variable. Observe that `__del__` is NOT called until all references are gone.

??? success "Solution to Exercise 1"

        class TrackedObject:
            def __init__(self, name):
                self.name = name
                print(f"Created: {self.name}")

            def __del__(self):
                print(f"Destroyed: {self.name}")

        obj = TrackedObject("alpha")  # Created: alpha
        ref = obj  # Second reference

        del obj
        print("obj deleted, ref still exists")
        # __del__ NOT called yet

        del ref
        # Now __del__ is called: Destroyed: alpha

---

**Exercise 2.**
Write a `Singleton` class where `__new__` ensures only one instance is ever created. If an instance already exists, `__new__` returns the existing one. Demonstrate that creating multiple instances all return the same object (same `id()`).

??? success "Solution to Exercise 2"

        class Singleton:
            _instance = None

            def __new__(cls, *args, **kwargs):
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                return cls._instance

            def __init__(self, value=None):
                self.value = value

        a = Singleton("first")
        b = Singleton("second")

        print(a is b)          # True
        print(id(a) == id(b))  # True
        print(a.value)         # "second" — __init__ ran again

---

**Exercise 3.**
Build a `Connection` class that uses `__init__` to open a simulated connection and `__del__` to close it. Also implement `__enter__` and `__exit__` so it works as a context manager. Demonstrate both usage patterns and explain why the context manager approach is preferred.

??? success "Solution to Exercise 3"

        class Connection:
            def __init__(self, url):
                self.url = url
                self.connected = True
                print(f"Connected to {url}")

            def __del__(self):
                if self.connected:
                    self.close()

            def close(self):
                self.connected = False
                print(f"Disconnected from {self.url}")

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                self.close()
                return False

        # Context manager (preferred — deterministic cleanup)
        with Connection("https://api.example.com") as conn:
            print(f"Using: {conn.connected}")
        # Automatically disconnected
