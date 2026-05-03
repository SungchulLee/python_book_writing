# Initialization Patterns

When a child class defines its own `__init__`, Python does not automatically call the parent's initializer. If the parent sets up important attributes or performs setup logic, those steps are silently skipped unless the child explicitly invokes them. The `super()` function provides a clean, MRO-aware way to call parent initializers, and using it correctly is essential for both single and multiple inheritance.

!!! tip "Mental Model"
    Python's rule is simple: defining `__init__` in a child class replaces the parent's -- it does not extend it. If the parent's setup matters, the child must explicitly call `super().__init__()`. Think of it as relaying a baton: if you do not pass it, the next runner never starts. In multiple inheritance, `super()` follows the MRO, so every class in the chain gets its turn.

## Parent __init__

### 1. Call super()

A child class should call `super().__init__()` to ensure the parent's initialization logic runs. Any arguments the parent expects must be passed through explicitly.

```python
class Parent:
    def __init__(self, x):
        self.x = x

class Child(Parent):
    def __init__(self, x, y):
        super().__init__(x)
        self.y = y

obj = Child(10, 20)
print(obj.x, obj.y)  # 10 20
```

Without the `super().__init__(x)` call, `obj.x` would never be set, and accessing it would raise an `AttributeError`.

## Multiple Inheritance

### 1. MRO Order

With multiple inheritance, `super()` follows the [Method Resolution Order (MRO)](mro.md). Python uses [C3 linearization](c3_linearization.md) to determine a consistent order in which classes are visited. Each `super()` call passes control to the next class in the MRO chain, not necessarily the direct parent.

**Key invariant**: for cooperative multiple inheritance to work, all classes in the hierarchy must accept compatible signatures. The standard pattern is to use `**kwargs` to absorb and forward unknown arguments:

```python
class Base:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class Left(Base):
    def __init__(self, left_val, **kwargs):
        super().__init__(**kwargs)
        self.left_val = left_val
```

Without `**kwargs`, the chain breaks:

- Arguments meant for downstream classes are **lost** or cause `TypeError`
- Adding a new class to the hierarchy **breaks** existing `__init__` calls
- In large hierarchies, these failures appear far from the actual bug, making them hard to debug

```python
class A:
    def __init__(self):
        print("A")
        super().__init__()

class B:
    def __init__(self):
        print("B")
        super().__init__()

class C(A, B):
    def __init__(self):
        print("C")
        super().__init__()

obj = C()
# Prints: C, A, B
```

The MRO for `C` is `[C, A, B, object]`. When `C.__init__` calls `super().__init__()`, control passes to `A`. When `A` calls `super().__init__()`, control passes to `B` (the next in the MRO), not to `object`. Finally, `B` calls `super().__init__()`, which reaches `object.__init__()` and the chain completes.

## When Not to Call `super()`

!!! tip "Default Rule"
    Use `super()` in cooperative hierarchies — this is the right choice in the vast majority of cases.

There are two legitimate exceptions:

- **Non-cooperative third-party classes** that don't call `super()` themselves --- inserting a `super()` call may cause unexpected double-initialization or argument errors.
- **Deliberately terminating the chain** --- a class designed to be the final base in an MRO may intentionally omit `super().__init__()`.

When in doubt, call `super()`. But inspect the MRO and parent signatures first in complex hierarchies.

## Summary

- Call `super().__init__()` in child classes to ensure the parent's initialization logic executes.
- Use `**kwargs` in cooperative hierarchies so that arguments pass cleanly through the MRO chain.
- The [Method Resolution Order (MRO)](mro.md) determines the sequence in which `super()` dispatches calls.
- In multiple inheritance, every cooperative class should call `super().__init__(**kwargs)` so that all initializers run exactly once in MRO order.

---

## Runnable Example: `mixin_pattern.py`

```python
"""
TUTORIAL: Mixin Pattern - Adding Functionality Through Multiple Inheritance
============================================================================

In this tutorial, you'll learn about the Mixin Pattern, a powerful technique
for adding functionality to classes without using traditional inheritance.

What is a Mixin?
  - A class designed to provide a specific piece of functionality
  - Not meant to stand alone (doesn't define the core behavior)
  - Combined with other classes through multiple inheritance
  - Provides methods that enhance or modify the behavior of other classes

Key characteristics:
  1. Mixins are combined in specific positions in the inheritance order
  2. They typically override specific methods to add functionality
  3. They use super() to allow chaining with other mixins
  4. They're small, focused, and reusable across different classes

In this example:
  - UpperCaseMixin overrides key methods (__setitem__, __getitem__, get, etc.)
  - These methods transform string keys to uppercase
  - UpperDict combines the mixin with dict functionality
  - UpperCounter combines the mixin with Counter functionality

The power: With ONE mixin class, we enhance TWO different collection types!
"""

import collections


# ============ Example 1: The UpperCaseMixin ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Defining UpperCaseMixin - case-insensitive string keys")
    print("=" * 70)

    def _upper(key):
        """Helper function to uppercase a key if it's a string.

        This function safely handles non-string keys (like integers)
        by returning them unchanged if they don't support .upper().

        Args:
            key: Any value, could be a string or something else.

        Returns:
            The uppercased key (if string) or the original key.
        """
        try:
            return key.upper()
        except AttributeError:
            # Not a string (e.g., int, tuple) - return as-is
            return key


    class UpperCaseMixin:
        """Mixin that makes string keys case-insensitive by uppercasing them.

        This mixin overrides four key methods to uppercase all string keys:
        1. __setitem__: When setting items (d[key] = value)
        2. __getitem__: When getting items (d[key])
        3. get: When using .get(key, default)
        4. __contains__: When checking membership (key in d)

        Why a mixin?
        - We want to add this behavior to multiple collection types
        - Instead of creating two separate subclasses, one mixin handles both
        - UpperDict and UpperCounter both benefit from the same mixin code

        How it works:
        - All methods call _upper(key) before calling super()
        - super() passes the uppercased key to the actual implementation
        - This lets dict and Counter handle the uppercased keys normally
        """

        def __setitem__(self, key, item):
            """Store item with uppercased key.

            When you do: d['hello'] = value
            Internally: super().__setitem__('HELLO', value)

            Args:
                key: The key to store under (will be uppercased if string).
                item: The value to store.
            """
            super().__setitem__(_upper(key), item)

        def __getitem__(self, key):
            """Retrieve item by uppercased key.

            When you do: value = d['hello']
            Internally: super().__getitem__('HELLO')

            Args:
                key: The key to look up (will be uppercased if string).

            Returns:
                The value associated with the uppercased key.
            """
            return super().__getitem__(_upper(key))

        def get(self, key, default=None):
            """Get item with optional default.

            When you do: d.get('hello', 'default')
            Internally: super().get('HELLO', 'default')

            Args:
                key: The key to look up (will be uppercased if string).
                default: Value returned if key not found.

            Returns:
                The value associated with the uppercased key, or default.
            """
            return super().get(_upper(key), default)

        def __contains__(self, key):
            """Check if key exists (case-insensitive).

            When you do: 'hello' in d
            Internally: super().__contains__('HELLO')

            Args:
                key: The key to check (will be uppercased if string).

            Returns:
                True if the uppercased key exists, False otherwise.
            """
            return super().__contains__(_upper(key))


    print(f"\nUpperCaseMixin defined with:")
    print(f"  - __setitem__: Uppercases key before storing")
    print(f"  - __getitem__: Uppercases key before retrieving")
    print(f"  - get: Uppercases key before looking up")
    print(f"  - __contains__: Uppercases key before checking membership")


    # ============ Example 2: UpperDict - Mixin + UserDict ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: UpperDict - Combining mixin with UserDict")
    print("=" * 70)

    class UpperDict(UpperCaseMixin, collections.UserDict):
        """A dict-like object with case-insensitive string keys.

        Inheritance order:
        1. UpperCaseMixin (provides case-insensitive behavior)
        2. UserDict (provides dict functionality)

        When a method like __setitem__ is called:
        1. Python looks in UpperDict (not found)
        2. Then UpperCaseMixin (found!)
        3. UpperCaseMixin.super().__setitem__ calls UserDict.__setitem__
        4. UserDict stores the item normally

        Why UserDict instead of dict?
        - dict doesn't allow method overriding (implemented in C)
        - UserDict is a pure Python wrapper that allows subclassing
        """
        pass


    print(f"\nUpperDict created: UpperCaseMixin + UserDict")
    print(f"Result: Dict with case-insensitive string keys")

    # Create and use an UpperDict
    d = UpperDict([('a', 'letter A'), (2, 'digit two')])

    print(f"\nd = UpperDict([('a', 'letter A'), (2, 'digit two')])")
    print(f"  Keys stored: {list(d.keys())}")

    print(f"\nSetting items (case-insensitive):")
    print(f"  d['b'] = 'letter B'")
    d['b'] = 'letter B'

    print(f"\nChecking membership (case-insensitive):")
    print(f"  'b' in d = {('b' in d)}  # lowercase works")
    print(f"  'B' in d = {('B' in d)}  # uppercase works")
    print(f"  'z' in d = {('z' in d)}  # not in dict")

    print(f"\nRetrieving values (case-insensitive):")
    print(f"  d['a'] = '{d['a']}'  # lowercase works")
    print(f"  d['A'] = '{d['A']}'  # uppercase works")

    print(f"\nUsing get() (case-insensitive):")
    print(f"  d.get('A') = '{d.get('A')}'")
    print(f"  d.get('B') = '{d.get('B')}'")
    print(f"  d.get('z', 'not found') = '{d.get('z', 'not found')}'")

    print(f"\nInteger keys are unaffected:")
    print(f"  d[2] = '{d[2]}'  (integers don't get uppercased)")
    print(f"  Keys now: {list(d.keys())}")


    # ============ Example 3: UpperCounter - Same Mixin, Different Class ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: UpperCounter - Same mixin, different parent class")
    print("=" * 70)

    class UpperCounter(UpperCaseMixin, collections.Counter):
        """A Counter with case-insensitive string keys.

        Same UpperCaseMixin, but combined with Counter instead of UserDict!
        This demonstrates the power of mixins: one mixin, multiple uses.

        Counter counts occurrences of items. With the mixin, it counts
        case-insensitively, treating 'a' and 'A' as the same key.
        """
        pass


    print(f"\nUpperCounter created: UpperCaseMixin + Counter")
    print(f"Result: Counter with case-insensitive string keys")

    # Create and use an UpperCounter
    c = UpperCounter('BaNanA')

    print(f"\nc = UpperCounter('BaNanA')")
    print(f"  Internal storage (all uppercase): {dict(c)}")

    print(f"\nmost_common():")
    print(f"  c.most_common() = {c.most_common()}")
    print(f"  A=3, N=2, B=1 (case-insensitive counting)")

    print(f"\nAccessing counts (case-insensitive):")
    print(f"  c['a'] = {c['a']}  (lowercase works)")
    print(f"  c['A'] = {c['A']}  (uppercase works)")
    print(f"  c['b'] = {c['b']}  (lowercase)")

    print(f"\nAdding items (case-insensitive):")
    c['a'] += 1
    print(f"  c['a'] += 1")
    print(f"  c.most_common() = {c.most_common()}")
    print(f"  'A' count is now 4 (merged with 'a')")


    # ============ Example 4: How Mixin Methods Work ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Understanding how mixin method delegation works")
    print("=" * 70)

    print(f"\nExecution flow for d['hello'] = 'world':")
    print(f"  1. User code: d['hello'] = 'world'")
    print(f"  2. Python calls: UpperDict.__setitem__(d, 'hello', 'world')")
    print(f"  3. Not in UpperDict, check MRO:")
    print(f"     UpperDict.__mro__ = {UpperDict.__mro__}")
    print(f"  4. Found in UpperCaseMixin:")
    print(f"     def __setitem__(self, key, item):")
    print(f"         super().__setitem__(_upper(key), item)")
    print(f"  5. _upper('hello') → 'HELLO'")
    print(f"  6. super().__setitem__('HELLO', 'world')")
    print(f"     (super() refers to next in MRO: UserDict)")
    print(f"  7. UserDict.__setitem__ stores key='HELLO', value='world'")

    print(f"\nExecution flow for value = d['hello']:")
    print(f"  1. User code: value = d['hello']")
    print(f"  2. Python calls: UpperDict.__getitem__(d, 'hello')")
    print(f"  3. Found in UpperCaseMixin:")
    print(f"     return super().__getitem__(_upper(key))")
    print(f"  4. _upper('hello') → 'HELLO'")
    print(f"  5. super().__getitem__('HELLO')")
    print(f"  6. UserDict.__getitem__ retrieves and returns 'world'")


    # ============ Example 5: Mixin Benefits ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Benefits of the Mixin Pattern")
    print("=" * 70)

    print(f"\nDRY (Don't Repeat Yourself):")
    print(f"  - Without mixin: would need two classes")
    print(f"    class UpperDict(dict): ... (with all 4 methods)")
    print(f"    class UpperCounter(Counter): ... (with same 4 methods)")
    print(f"  - With mixin: write once, use twice")
    print(f"    UpperCaseMixin (1 definition)")
    print(f"    UpperDict = UpperCaseMixin + UserDict")
    print(f"    UpperCounter = UpperCaseMixin + Counter")

    print(f"\nComposability:")
    print(f"  - Could create UpperSet = UpperCaseMixin + set")
    print(f"  - Could create UpperDefaultDict = UpperCaseMixin + defaultdict")
    print(f"  - Single mixin works with any dict-like class")

    print(f"\nSeparation of Concerns:")
    print(f"  - UpperCaseMixin: handles key transformation")
    print(f"  - UserDict/Counter: handles storage")
    print(f"  - Each class has a single responsibility")

    print(f"\nFlexibility:")
    print(f"  - Can be combined with other mixins too")
    print(f"  - Can be used with future collection types")


    # ============ Example 6: Mixin Pattern in Real Code ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Real-world mixin example")
    print("=" * 70)

    class ReprMixin:
        """Mixin that adds a nice string representation."""
        def __repr__(self):
            items = ', '.join(f'{k}={v!r}' for k, v in self.items())
            return f'{self.__class__.__name__}({{{items}}})'

    class CaselessDict(UpperCaseMixin, ReprMixin, collections.UserDict):
        """UserDict with case-insensitive keys AND nice repr!"""
        pass

    cd = CaselessDict([('Name', 'Alice'), ('AGE', 30)])
    print(f"\ncd = CaselessDict([('Name', 'Alice'), ('AGE', 30)])")
    print(f"  repr(cd) = {repr(cd)}")
    print(f"  cd['name'] = '{cd['name']}'  (case-insensitive)")
    print(f"  cd['age'] = {cd['age']}  (case-insensitive)")

    print(f"\nWe combined TWO mixins:")
    print(f"  - UpperCaseMixin: case-insensitive access")
    print(f"  - ReprMixin: nice string representation")
    print(f"  - Result: a fully-featured case-insensitive dict")


    # ============ Example 7: When to Use Mixins ============
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Mixin Pattern Best Practices")
    print("=" * 70)

    print(f"\nUse mixins when:")
    print(f"  1. Adding functionality to multiple unrelated classes")
    print(f"  2. The functionality is orthogonal (doesn't create hierarchy)")
    print(f"  3. Code would be duplicated across classes")
    print(f"  4. You want composition over inheritance")

    print(f"\nDon't use mixins when:")
    print(f"  1. Creating a primary class hierarchy (use inheritance)")
    print(f"  2. The mixin would be used alone (needs a main class)")
    print(f"  3. Mixing in creates unclear code or confusing MRO")

    print(f"\nMixin naming convention:")
    print(f"  - Typically end with 'Mixin' (UpperCaseMixin, ReprMixin)")
    print(f"  - Or end with descriptor (TimestampedMixin, ValidatedMixin)")
    print(f"  - Helps readers understand they're not primary classes")

    print(f"\nMixin placement in inheritance:")
    print(f"  - Usually: YourMixin, BaseClass")
    print(f"  - Mixin comes FIRST so its methods are found first")
    print(f"  - super() in mixin calls the next class in MRO")

    print(f"\n" + "=" * 70)
```


---

## Runnable Example: `mro_mixin_setonce_example.py`

```python
"""
Multiple Inheritance: MRO, Diamond Problem, and Mixins

When a class inherits from multiple parents, Python uses the C3
Linearization algorithm to determine Method Resolution Order (MRO).

Topics covered:
- Diamond inheritance problem
- C3 Linearization (MRO)
- Mixin pattern for composable behavior
- SetOnceMixin: preventing key overwrites

Based on concepts from Python-100-Days example17 and ch06/inheritance materials.
"""


# =============================================================================
# Example 1: Diamond Problem and MRO
# =============================================================================

class A:
    def greet(self):
        return 'Hello from A'


class B(A):
    pass  # Inherits A.greet


class C(A):
    def greet(self):
        return 'Hello from C'


class D(B, C):
    pass  # Which greet() does D inherit?


def demo_diamond():
    """Demonstrate the diamond problem and C3 linearization."""
    print("=== Diamond Problem ===")
    print("""
    Class hierarchy:
        A           (defines greet)
       / \\
      B   C         (C overrides greet)
       \\ /
        D           (inherits from both B and C)
    """)

    d = D()
    print(f"D().greet() = '{d.greet()}'")
    print()

    # MRO determines the search order
    print("Method Resolution Order (C3 Linearization):")
    print(f"  D.mro() = {[cls.__name__ for cls in D.mro()]}")
    print()

    print("Python 3 uses C3 algorithm (breadth-first-like):")
    print("  D -> B -> C -> A -> object")
    print("  So D.greet() calls C.greet() because C comes before A in MRO")
    print()


# =============================================================================
# Example 2: SetOnce Mixin
# =============================================================================

class SetOnceMixin:
    """Mixin that prevents overwriting existing keys.

    A mixin is a class designed to be combined with other classes
    via multiple inheritance. It adds a single focused behavior.

    This mixin overrides __setitem__ to raise KeyError if the key
    already exists, enforcing write-once semantics.
    """
    __slots__ = ()  # Mixins typically don't add instance attributes

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Key '{key}' already set (write-once policy)")
        return super().__setitem__(key, value)


class SetOnceDict(SetOnceMixin, dict):
    """A dictionary where keys can only be set once.

    MRO: SetOnceDict -> SetOnceMixin -> dict -> object
    When setting a key, SetOnceMixin.__setitem__ runs first,
    then delegates to dict.__setitem__ via super().
    """
    pass


def demo_setonce():
    """Demonstrate the SetOnce mixin."""
    print("=== SetOnce Mixin ===")
    print(f"SetOnceDict MRO: {[c.__name__ for c in SetOnceDict.__mro__]}")
    print()

    config = SetOnceDict()
    config['database'] = 'postgres'
    config['port'] = 5432
    print(f"Config: {config}")

    try:
        config['database'] = 'mysql'  # Raises KeyError
    except KeyError as e:
        print(f"KeyError: {e}")
    print()


# =============================================================================
# Example 3: Composable Mixins
# =============================================================================

class LoggingMixin:
    """Mixin that logs all item assignments."""
    __slots__ = ()

    def __setitem__(self, key, value):
        print(f"  [LOG] Setting '{key}' = {value!r}")
        super().__setitem__(key, value)


class ValidatingMixin:
    """Mixin that validates keys are strings."""
    __slots__ = ()

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise TypeError(f"Key must be str, got {type(key).__name__}")
        super().__setitem__(key, value)


class StrictDict(ValidatingMixin, LoggingMixin, SetOnceMixin, dict):
    """A dict with validation, logging, and write-once behavior.

    MRO: StrictDict -> ValidatingMixin -> LoggingMixin
         -> SetOnceMixin -> dict -> object

    Each mixin's __setitem__ calls super().__setitem__(),
    creating a chain of responsibility.
    """
    pass


def demo_composable():
    """Show how multiple mixins compose together."""
    print("=== Composable Mixins ===")
    print(f"StrictDict MRO: {[c.__name__ for c in StrictDict.__mro__]}")
    print()

    d = StrictDict()

    # Normal operation: validation -> logging -> set-once -> dict
    d['name'] = 'Alice'
    print(f"Result: {d}")
    print()

    # Try non-string key (ValidatingMixin catches it)
    print("Trying integer key:")
    try:
        d[42] = 'invalid'
    except TypeError as e:
        print(f"  TypeError: {e}")
    print()

    # Try duplicate key (SetOnceMixin catches it)
    print("Trying duplicate key:")
    try:
        d['name'] = 'Bob'
    except KeyError as e:
        print(f"  KeyError: {e}")
    print()


# =============================================================================
# Example 4: Mixin Best Practices
# =============================================================================

def demo_best_practices():
    """Summarize mixin design guidelines."""
    print("=== Mixin Best Practices ===")
    print("""
    1. Single Responsibility: Each mixin adds ONE behavior
    2. No __init__: Mixins should not define __init__
    3. Use __slots__ = (): Mixins shouldn't add instance attributes
    4. Always call super(): Enable cooperative multiple inheritance
    5. Name with 'Mixin' suffix: Makes intent clear
    6. Keep mixins focused and composable
    7. Document MRO expectations
    """)


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    demo_diamond()
    demo_setonce()
    demo_composable()
    demo_best_practices()
```

---

## Exercises

**Exercise 1.**
Create `Animal` with `name` in `__init__`. Create `Pet(Animal)` that adds `owner`. Show what happens if `Pet.__init__` forgets to call `super().__init__()` (the `name` attribute is missing). Then fix it.

??? success "Solution to Exercise 1"

        class Animal:
            def __init__(self, name):
                self.name = name

        # Broken: forgets super()
        class PetBroken(Animal):
            def __init__(self, name, owner):
                self.owner = owner
                # Forgot super().__init__(name)

        try:
            p = PetBroken("Buddy", "Alice")
            print(p.name)
        except AttributeError as e:
            print(f"Error: {e}")  # 'PetBroken' has no attribute 'name'

        # Fixed
        class Pet(Animal):
            def __init__(self, name, owner):
                super().__init__(name)
                self.owner = owner

        p = Pet("Buddy", "Alice")
        print(p.name)   # Buddy
        print(p.owner)  # Alice

---

**Exercise 2.**
Build a mixin pattern: `TimestampMixin` (adds `created_at` in `__init__`), `LogMixin` (adds a `log(msg)` method), and `Document(TimestampMixin, LogMixin)` with a `title`. All `__init__` methods should use `super().__init__(**kwargs)` for cooperative initialization. Show that all attributes are correctly set.

??? success "Solution to Exercise 2"

        from datetime import datetime

        class TimestampMixin:
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.created_at = datetime.now()

        class LogMixin:
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self._logs = []

            def log(self, msg):
                self._logs.append(msg)

        class Document(TimestampMixin, LogMixin):
            def __init__(self, title, **kwargs):
                super().__init__(**kwargs)
                self.title = title

        doc = Document("Report")
        doc.log("Created")
        print(doc.title)       # Report
        print(doc.created_at)  # timestamp
        print(doc._logs)       # ['Created']

---

**Exercise 3.**
Create a diamond: `Base(__init__(self, value, **kwargs))`, `Left(Base)` and `Right(Base)` each add their own attribute, and `Bottom(Left, Right)`. Use `super().__init__(**kwargs)` everywhere. Show that `Bottom(value=1, left_attr="L", right_attr="R")` correctly initializes all attributes by passing `**kwargs` up the MRO.

??? success "Solution to Exercise 3"

        class Base:
            def __init__(self, value, **kwargs):
                super().__init__(**kwargs)
                self.value = value

        class Left(Base):
            def __init__(self, left_attr="", **kwargs):
                super().__init__(**kwargs)
                self.left_attr = left_attr

        class Right(Base):
            def __init__(self, right_attr="", **kwargs):
                super().__init__(**kwargs)
                self.right_attr = right_attr

        class Bottom(Left, Right):
            pass

        b = Bottom(value=1, left_attr="L", right_attr="R")
        print(b.value)       # 1
        print(b.left_attr)   # L
        print(b.right_attr)  # R
