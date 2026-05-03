# `super()` Mechanics

The `super()` function enables cooperative multiple inheritance by following the [Method Resolution Order (MRO)](mro.md). Together with [C3 linearization](c3_linearization.md), it forms the core of Python's method dispatch: C3 computes the order, the MRO stores it, and `super()` walks it.

!!! tip "Mental Model"
    `super()` does not mean "call my parent." It means "call the next class in the MRO." In single inheritance the next class *is* the parent, so the distinction is invisible. In multiple inheritance, `super()` may call a sibling class you never directly inherited from. This cooperative chain is what makes diamond inheritance work correctly.

---

## What `super()` Does

### 1. Not Just Parent

`super()` doesn't call the "parent" class—it calls the **next class in MRO**. The simplest correct mental model: `super()` means **"continue the chain."**

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        super().method()
        print("B")
```

### 2. MRO-Aware

```python
class D(B, C):
    def method(self):
        super().method()  # follows MRO, not just B
```

### 3. Dynamic Dispatch

`super()` is internally bound to a **(class, instance) pair**. The "class" is the class where `super()` appears in the source code, and the "instance" is the actual object. Python uses this pair to find the current position in the instance's MRO and dispatch to the next class. This is why the same `super()` call in `B` may dispatch to different classes depending on whether the instance is a `B` or a `D(B, C)`.

!!! note "How super() Works Internally"

    `super()` returns a **proxy object**, not a class. When you call a method on this proxy, Python:

    1. Finds the current class (where `super()` appears) in the instance's MRO
    2. Moves to the **next** class in the MRO
    3. Looks up the method name on that class
    4. Binds the method to the original instance
    5. Returns the bound method (which you then call)

    This is why `super()` is MRO-aware and not simply "call my parent" — step 2 uses the full MRO of the actual instance, which may include classes the current class knows nothing about.

!!! warning "Do Not Pass `self` to `super().method()`"

    Because step 4 above **binds** the method to the instance, `super().method()` is already a bound method call — `self` is supplied automatically. Writing `super().method(self)` passes `self` **twice**, which typically raises `TypeError` due to an extra argument.

    ```python
    # ✅ Correct — self is bound automatically
    super().method()

    # ❌ Wrong — self passed twice
    super().method(self)
    ```

    This is the same reason you write `self.method()` and not `self.method(self)` — method binding handles it for you.

---

## Cooperative Inheritance

### 1. All Use `super()`

```python
class A:
    def __init__(self):
        print("A init")
        super().__init__()

class B(A):
    def __init__(self):
        print("B init")
        super().__init__()

class C(A):
    def __init__(self):
        print("C init")
        super().__init__()
```

### 2. Diamond Pattern

```python
class D(B, C):
    def __init__(self):
        print("D init")
        super().__init__()

d = D()
# Output:
# D init
# B init
# C init
# A init
```

### 3. Each Called Once

`super()` ensures each class in MRO is called exactly once.

---

## `super()` Syntax

### 1. Python 3 (Preferred)

```python
class Child(Parent):
    def method(self):
        super().method()  # automatic
```

### 2. Python 2 (Legacy)

```python
class Child(Parent):
    def method(self):
        super(Child, self).method()
```

### 3. No `self` Argument

```python
# Wrong
super().__init__(self, x, y)

# Correct
super().__init__(x, y)
```

---

## When to Use `super()`

### 1. Always in Hierarchies

Use `super()` in any inheritance hierarchy.

### 2. Multiple Inheritance

Essential for cooperative multiple inheritance.

### 3. Framework Design

Critical when designing extensible frameworks.

---

## Common Pitfalls

### 1. Forgetting `super()`

```python
class B(A):
    def __init__(self):
        # forgot super().__init__()
        self.b = "value"
```

Breaks the chain—`A.__init__` never runs.

### 2. Mixing Styles

```python
class B(A):
    def __init__(self):
        A.__init__(self)  # don't mix with super()
```

Use `super()` consistently throughout hierarchy.

### 3. Assuming Parent

```python
# super() calls next in MRO, not necessarily parent
class D(B, C):
    def method(self):
        super().method()  # might call C, not B!
```

---

## Advanced: MRO Flow

### 1. Simple Chain

```python
class A: pass
class B(A): pass
class C(B): pass

# MRO: C → B → A → object
```

### 2. Multiple Inheritance

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

# MRO: D → B → C → A → object
```

### 3. `super()` Follows MRO

At each step, `super()` moves to the next class in this order.

---

## Key Takeaways

- `super()` follows MRO, not just parent.
- Use `super()` consistently in hierarchies.
- Never pass `self` to `super()`.
- Cooperative inheritance requires all classes use `super()`.

---

## Runnable Example: `super_and_mro.py`

```python
"""
04_super_and_mro.py

INTERMEDIATE LEVEL: Understanding super() and its Relationship with MRO

This file provides a deep dive into how super() works with MRO in Python.
The super() function is essential for cooperative multiple inheritance and
understanding it is key to mastering MRO.

Learning Objectives:
- Understand what super() really does
- Learn the difference between super() and direct parent calls
- Master cooperative inheritance patterns
- Handle initialization chains correctly
- Debug super() issues
"""

# ============================================================================
# SECTION 1: What super() Actually Does
# ============================================================================

if __name__ == "__main__":

    """
    COMMON MISCONCEPTION:
    super() calls the parent class

    REALITY:
    super() calls the NEXT CLASS in the MRO, not necessarily the parent!

    This is crucial for understanding cooperative multiple inheritance.

    super() returns a proxy object that delegates method calls to the next
    class in the MRO chain, starting after the current class.
    """


    # ============================================================================
    # SECTION 2: super() vs Direct Parent Call
    # ============================================================================

    class Parent:
        """Simple parent class."""

        def __init__(self):
            print("Parent.__init__ called")
            self.parent_value = "from parent"

        def method(self):
            return "Parent method"


    class ChildWithSuper(Parent):
        """Child using super() - recommended way."""

        def __init__(self):
            print("ChildWithSuper.__init__ called")
            super().__init__()  # Calls next in MRO
            self.child_value = "from child"

        def method(self):
            # super() calls the next class's method in MRO
            parent_result = super().method()
            return f"Child method (parent says: {parent_result})"


    class ChildDirect(Parent):
        """Child using direct parent call."""

        def __init__(self):
            print("ChildDirect.__init__ called")
            Parent.__init__(self)  # Directly calls Parent
            self.child_value = "from child"

        def method(self):
            # Direct call to parent method
            parent_result = Parent.method(self)
            return f"Child method (parent says: {parent_result})"


    print("="*70)
    print("SUPER() VS DIRECT PARENT CALL")
    print("="*70)

    print("\nUsing super():")
    child1 = ChildWithSuper()
    print(f"Result: {child1.method()}")

    print("\nUsing direct parent call:")
    child2 = ChildDirect()
    print(f"Result: {child2.method()}")

    print("\nBoth work the same for single inheritance!")
    print("But super() is better for multiple inheritance...")


    # ============================================================================
    # SECTION 3: Why super() Matters - Diamond Problem Example
    # ============================================================================

    class Base:
        """Common base class."""

        def __init__(self):
            print("Base.__init__ called")
            self.base_value = "base"


    class LeftWithSuper(Base):
        """Left branch using super()."""

        def __init__(self):
            print("LeftWithSuper.__init__ called")
            super().__init__()  # Calls NEXT in MRO, not Base!
            self.left_value = "left"


    class RightWithSuper(Base):
        """Right branch using super()."""

        def __init__(self):
            print("RightWithSuper.__init__ called")
            super().__init__()  # Calls NEXT in MRO, not Base!
            self.right_value = "right"


    class DiamondWithSuper(LeftWithSuper, RightWithSuper):
        """
        Diamond inheritance using super().

        MRO: DiamondWithSuper -> LeftWithSuper -> RightWithSuper -> Base -> object
        """

        def __init__(self):
            print("DiamondWithSuper.__init__ called")
            super().__init__()  # Starts the MRO chain


    # Now compare with direct parent calls:

    class LeftDirect(Base):
        """Left branch using direct call."""

        def __init__(self):
            print("LeftDirect.__init__ called")
            Base.__init__(self)  # Directly calls Base
            self.left_value = "left"


    class RightDirect(Base):
        """Right branch using direct call."""

        def __init__(self):
            print("RightDirect.__init__ called")
            Base.__init__(self)  # Directly calls Base
            self.right_value = "right"


    class DiamondDirect(LeftDirect, RightDirect):
        """
        Diamond inheritance using direct calls.
        This will call Base.__init__ TWICE!
        """

        def __init__(self):
            print("DiamondDirect.__init__ called")
            LeftDirect.__init__(self)   # Calls Base.__init__
            RightDirect.__init__(self)  # Calls Base.__init__ AGAIN!


    print("\n" + "="*70)
    print("SUPER() IN DIAMOND INHERITANCE")
    print("="*70)

    print("\nUsing super() - Base.__init__ called ONCE:")
    d1 = DiamondWithSuper()

    print("\nMRO for DiamondWithSuper:")
    for i, cls in enumerate(DiamondWithSuper.__mro__, 1):
        print(f"{i}. {cls.__name__}")

    print("\n" + "-"*70)

    print("\nUsing direct calls - Base.__init__ called TWICE:")
    d2 = DiamondDirect()

    print("\nThis can cause bugs! Base is initialized twice.")


    # ============================================================================
    # SECTION 4: How super() Follows MRO
    # ============================================================================

    """
    super() uses the MRO to determine which class to call next.
    Let's trace through the MRO step by step.
    """


    class A:
        def __init__(self):
            print(f"  A.__init__ called (MRO position: {A.__mro__.index(A) + 1})")
            print(f"  A: next in MRO would be object")
            super().__init__()  # Calls object.__init__


    class B(A):
        def __init__(self):
            print(f"  B.__init__ called (MRO position: {B.__mro__.index(B) + 1})")
            print(f"  B: next in MRO is {B.__mro__[B.__mro__.index(B) + 1].__name__}")
            super().__init__()  # Calls A.__init__


    class C(A):
        def __init__(self):
            print(f"  C.__init__ called (MRO position: variable - depends on final class)")
            print(f"  C: calls super().__init__()")
            super().__init__()  # Calls next in MRO (might not be A!)


    class D(B, C):
        """
        Diamond with detailed tracing.

        MRO: D -> B -> C -> A -> object
        """

        def __init__(self):
            print(f"  D.__init__ called (MRO position: 1)")
            print(f"  D: next in MRO is {D.__mro__[1].__name__}")
            super().__init__()  # Calls B.__init__


    print("\n" + "="*70)
    print("TRACING SUPER() THROUGH MRO")
    print("="*70)

    print("\nMRO for D:")
    for i, cls in enumerate(D.__mro__, 1):
        print(f"{i}. {cls.__name__}")

    print("\nCreating D instance and tracing super() calls:")
    d = D()

    print("\nNotice:")
    print("- Each class calls super().__init__()")
    print("- super() in B calls C, not A (following MRO)")
    print("- super() in C calls A (following MRO)")
    print("- A's __init__ is called only once at the end")


    # ============================================================================
    # SECTION 5: Cooperative Inheritance Pattern
    # ============================================================================

    """
    Cooperative inheritance: all classes in the hierarchy cooperate by:
    1. Taking their own parameters
    2. Passing remaining parameters to super()
    3. Ensuring all classes get properly initialized
    """


    class Logger:
        """Base class for logging functionality."""

        def __init__(self, log_level="INFO", **kwargs):
            # Take our parameter
            print(f"Logger.__init__: log_level={log_level}")
            self.log_level = log_level

            # Pass remaining kwargs to next in MRO
            super().__init__(**kwargs)

        def log(self, message):
            return f"[{self.log_level}] {message}"


    class Timestamped:
        """Mixin to add timestamps."""

        def __init__(self, include_timestamp=True, **kwargs):
            print(f"Timestamped.__init__: include_timestamp={include_timestamp}")
            self.include_timestamp = include_timestamp

            super().__init__(**kwargs)

        def get_timestamp(self):
            from datetime import datetime
            if self.include_timestamp:
                return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return ""


    class FileHandler(Logger, Timestamped):
        """
        Handles file operations with logging and timestamps.

        MRO: FileHandler -> Logger -> Timestamped -> object

        Both Logger and Timestamped use cooperative inheritance,
        so all __init__ methods are called correctly.
        """

        def __init__(self, filename, log_level="INFO", include_timestamp=True):
            print(f"FileHandler.__init__: filename={filename}")
            self.filename = filename

            # Pass parameters to cooperative parent classes
            super().__init__(
                log_level=log_level,
                include_timestamp=include_timestamp
            )

        def write(self, data):
            """Write data to file with logging and timestamp."""
            timestamp = self.get_timestamp()
            prefix = f"{timestamp} " if timestamp else ""
            message = f"{prefix}Writing to {self.filename}: {data}"
            return self.log(message)


    print("\n" + "="*70)
    print("COOPERATIVE INHERITANCE PATTERN")
    print("="*70)

    print("\nCreating FileHandler:")
    handler = FileHandler(
        filename="data.txt",
        log_level="DEBUG",
        include_timestamp=True
    )

    print("\nMRO for FileHandler:")
    for i, cls in enumerate(FileHandler.__mro__, 1):
        print(f"{i}. {cls.__name__}")

    print(f"\nUsing FileHandler:")
    print(handler.write("Hello, World!"))


    # ============================================================================
    # SECTION 6: Common super() Pitfalls
    # ============================================================================

    """
    Common mistakes when using super():
    1. Mixing super() and direct calls
    2. Not passing **kwargs
    3. Incorrect parameter handling
    4. Forgetting to call super()
    """


    # PITFALL 1: Mixing super() and direct calls
    class Bad1A:
        def __init__(self):
            print("Bad1A.__init__")


    class Bad1B(Bad1A):
        def __init__(self):
            print("Bad1B.__init__")
            super().__init__()  # Uses super()


    class Bad1C(Bad1A):
        def __init__(self):
            print("Bad1C.__init__")
            Bad1A.__init__(self)  # Direct call!


    class Bad1D(Bad1B, Bad1C):
        """
        This might work but is fragile and unpredictable.
        Bad1A.__init__ gets called twice!
        """

        def __init__(self):
            print("Bad1D.__init__")
            super().__init__()


    # PITFALL 2: Not passing **kwargs
    class Good2A:
        def __init__(self, a=None, **kwargs):
            print(f"Good2A: a={a}")
            super().__init__(**kwargs)  # Passes remaining kwargs


    class Bad2B(Good2A):
        def __init__(self, b=None, **kwargs):
            print(f"Bad2B: b={b}")
            super().__init__()  # Doesn't pass kwargs!
            # This breaks the chain!


    class Good2C(Good2A):
        def __init__(self, c=None, **kwargs):
            print(f"Good2C: c={c}")
            super().__init__(**kwargs)  # Correctly passes kwargs


    print("\n" + "="*70)
    print("COMMON SUPER() PITFALLS")
    print("="*70)

    print("\nPitfall 1 - Mixing super() and direct calls:")
    print("Bad1D might work but is unpredictable:")
    # bad1d = Bad1D()  # Bad1A.__init__ called twice

    print("\nPitfall 2 - Not passing **kwargs:")
    print("This breaks the cooperative chain")
    # If we had: class Bad2D(Bad2B, Good2C): pass
    # Good2C's parameters wouldn't be passed through Bad2B


    # ============================================================================
    # SECTION 7: super() with Arguments
    # ============================================================================

    """
    super() can take arguments: super(Class, instance)
    This is rarely needed but useful for understanding how super() works.
    """


    class Base7:
        def method(self):
            return "Base7"


    class Child7(Base7):
        def method(self):
            # These are equivalent:
            result1 = super().method()  # Modern way
            result2 = super(Child7, self).method()  # Explicit way

            return f"Child7 (base: {result1})"


    class GrandChild7(Child7):
        def method(self):
            # Can skip a class in MRO if needed (rare!)
            result = super(Child7, self).method()  # Skip Child7, go to Base7
            return f"GrandChild7 (skipped to: {result})"


    print("\n" + "="*70)
    print("SUPER() WITH ARGUMENTS")
    print("="*70)

    child = Child7()
    print(f"child.method(): {child.method()}")

    grandchild = GrandChild7()
    print(f"grandchild.method() - normal: {super(GrandChild7, grandchild).method()}")
    print(f"grandchild.method() - skip: {super(Child7, grandchild).method()}")


    # ============================================================================
    # SECTION 8: Debugging super() and MRO
    # ============================================================================

    """
    Tips for debugging super() issues:
    1. Print the MRO
    2. Trace __init__ calls
    3. Check for consistent use of super()
    4. Verify **kwargs are passed correctly
    """


    class DebugMixin:
        """Mixin to help debug MRO and super() issues."""

        def print_mro(self):
            """Print the MRO in a readable format."""
            print(f"\nMRO for {self.__class__.__name__}:")
            for i, cls in enumerate(self.__class__.__mro__, 1):
                print(f"  {i}. {cls.__name__}")

        def trace_method(self, method_name):
            """Trace which class provides a method."""
            print(f"\nTracing method '{method_name}':")
            for cls in self.__class__.__mro__:
                if method_name in cls.__dict__:
                    print(f"  Found in: {cls.__name__}")
                    break
            else:
                print(f"  Not found in MRO")


    class DebugA(DebugMixin):
        def method_a(self):
            return "from A"


    class DebugB(DebugMixin):
        def method_b(self):
            return "from B"


    class DebugC(DebugA, DebugB):
        def method_c(self):
            return "from C"


    print("\n" + "="*70)
    print("DEBUGGING TOOLS")
    print("="*70)

    debug = DebugC()
    debug.print_mro()
    debug.trace_method("method_a")
    debug.trace_method("method_b")
    debug.trace_method("method_c")
    debug.trace_method("nonexistent")


    # ============================================================================
    # SECTION 9: Key Takeaways
    # ============================================================================

    """
    KEY POINTS ABOUT SUPER():

    1. What super() Does:
       - Returns a proxy that calls the NEXT class in MRO
       - NOT the same as calling the parent class directly
       - Essential for cooperative multiple inheritance

    2. Why Use super():
       - Prevents duplicate initialization in diamond inheritance
       - Enables cooperative inheritance patterns
       - More maintainable and flexible code
       - Respects the MRO

    3. Cooperative Inheritance Pattern:
       - Each class takes its own parameters
       - Pass remaining parameters using **kwargs
       - Always call super().__init__(**kwargs)
       - Document your MRO intentions

    4. Common Pitfalls:
       - Mixing super() and direct parent calls
       - Not passing **kwargs through the chain
       - Inconsistent use of super() across hierarchy
       - Forgetting to call super() at all

    5. Best Practices:
       - Use super() consistently in all classes
       - Pass **kwargs to handle unknown parameters
       - Document complex MRO chains
       - Test diamond inheritance scenarios
       - Use debugging tools to trace MRO

    6. When NOT to Use super():
       - When you specifically need to call one parent
       - When you're not doing cooperative inheritance
       - Simple single inheritance (but super() still works!)

    7. Python 2 vs Python 3:
       - Python 2: super(ClassName, self).method()
       - Python 3: super().method() (simpler!)
       - This course uses Python 3 syntax
    """

    print("\n" + "="*70)
    print("END OF SUPER() AND MRO TUTORIAL")
    print("="*70)
    print("\nNext: Learn MRO inspection tools and techniques!")
```

---

## Exercises

**Exercise 1.**
Create `Shape` with an `area()` method returning `0`. Create `Rectangle(Shape)` that overrides `area()`. Then create `ColoredRectangle(Rectangle)` that adds a `color` attribute but reuses `Rectangle.area()` via `super()`. Show that `super()` skips to the correct parent.

??? success "Solution to Exercise 1"

        class Shape:
            def area(self):
                return 0

        class Rectangle(Shape):
            def __init__(self, width, height):
                self.width = width
                self.height = height

            def area(self):
                return self.width * self.height

        class ColoredRectangle(Rectangle):
            def __init__(self, width, height, color):
                super().__init__(width, height)
                self.color = color

            # area() not overridden — uses Rectangle's via super()

        cr = ColoredRectangle(5, 3, "red")
        print(cr.area())   # 15 — from Rectangle
        print(cr.color)    # red

---

**Exercise 2.**
Build a cooperative diamond: `Base` has `setup()` that prints "Base". `Mixin1(Base)` and `Mixin2(Base)` each override `setup()`, print their name, and call `super().setup()`. `Combined(Mixin1, Mixin2)` overrides `setup()` and calls `super().setup()`. Show that each `setup()` is called exactly once in MRO order.

??? success "Solution to Exercise 2"

        class Base:
            def setup(self):
                print("Base.setup")

        class Mixin1(Base):
            def setup(self):
                print("Mixin1.setup")
                super().setup()

        class Mixin2(Base):
            def setup(self):
                print("Mixin2.setup")
                super().setup()

        class Combined(Mixin1, Mixin2):
            def setup(self):
                print("Combined.setup")
                super().setup()

        Combined().setup()
        # Combined.setup -> Mixin1.setup -> Mixin2.setup -> Base.setup
        # Each called exactly once

---

**Exercise 3.**
Demonstrate a `super()` pitfall: create `Parent` with `__init__(self, x)` and `Child(Parent)` with `__init__(self, x, y)`. Show that `super().__init__(x)` works, but calling `super().__init__(x, y)` fails because `Parent.__init__` does not accept `y`. Then fix it using `**kwargs` for forward compatibility.

??? success "Solution to Exercise 3"

        # Broken version
        class Parent:
            def __init__(self, x):
                self.x = x

        class Child(Parent):
            def __init__(self, x, y):
                super().__init__(x)  # Works
                self.y = y

        c = Child(1, 2)
        print(c.x, c.y)  # 1 2

        # Fixed version with **kwargs
        class ParentFixed:
            def __init__(self, x, **kwargs):
                super().__init__(**kwargs)
                self.x = x

        class ChildFixed(ParentFixed):
            def __init__(self, x, y, **kwargs):
                super().__init__(x=x, **kwargs)
                self.y = y

        cf = ChildFixed(x=1, y=2)
        print(cf.x, cf.y)  # 1 2
