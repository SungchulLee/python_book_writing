# Method Resolution Order

The **Method Resolution Order (MRO)** defines how Python resolves methods in inheritance hierarchies, especially with multiple inheritance. The MRO, [C3 linearization](c3_linearization.md), and [`super()`](super.md) form a unified system: C3 computes the order, the MRO stores it, and `super()` walks it at runtime.

!!! note "MRO Governs All Attribute Lookup"

    Despite its name, the Method Resolution Order is not limited to methods. It defines the search order for **all** attribute access on an object. When you write `obj.attr`, Python searches the instance `__dict__` first, then walks the class hierarchy in MRO order looking for `attr` in each class's `__dict__`. Methods, class variables, descriptors, and properties are all found through this same mechanism. Methods are simply attributes that happen to be callable.

---

## Why MRO Exists

### 1. Ambiguity Problem

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

d = D()
d.method()  # Which method?
```

### 2. Diamond Problem

```python
    A
   / \
  B   C
   \ /
    D
```

When `D` inherits from both `B` and `C`, which inherit from `A`, how should methods resolve?

### 3. Deterministic Order

MRO provides a consistent, predictable resolution order.

---

## Inspecting MRO

### 1. Using `.mro()`

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.mro())
# [<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]
```

### 2. Using `__mro__`

```python
print(D.__mro__)
# Same output as .mro()
```

### 3. Reading the Order

Attributes are searched through this list from left to right. However, the full lookup is: **data descriptors → instance `__dict__` → class hierarchy (MRO) → `__getattr__`**. The MRO governs the class hierarchy part of this chain. See the [descriptor section](../descriptors/descriptor_intro.md) for the complete picture.

---

## MRO Principles

### 1. Child First

The class itself is always first in MRO.

### 2. Left-to-Right (Subject to C3 Constraints)

Parents are generally searched in declaration order, but this rule is subject to the constraints imposed by [C3 linearization](c3_linearization.md). "Left-to-right" is a useful simplification for most cases, but the full algorithm also preserves monotonicity and parent MRO consistency.

```python
class D(B, C):  # B before C
    pass
```

### 3. Parents Before Ancestors

A parent appears before its own parents.

```python
# D → B → C → A
# B appears before A
# C appears before A
```

---

## C3 Linearization

### 1. Algorithm Used

Python uses [C3 linearization](c3_linearization.md) to compute MRO. Unlike naïve depth-first or breadth-first traversals, C3 guarantees a consistent ordering or rejects the hierarchy.

### 2. Three Properties

- Preserves local precedence order
- Maintains parent MRO consistency
- Ensures monotonicity

### 3. Consistency

Guarantees a consistent resolution order or raises an error. See [C3 Linearization](c3_linearization.md) for the full merge algorithm and worked examples.

---

## MRO and `super()`

### 1. `super()` Follows MRO

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        super().method()  # calls next in MRO
        print("B")
```

### 2. Cooperative Calls

```python
class D(B, C):
    def method(self):
        super().method()  # calls B.method
        # B.method calls super() → C.method
        # C.method calls super() → A.method
```

### 3. Each Class Once

Even in diamond inheritance, each class is called exactly once.

---

## Invalid MRO

### 1. Inconsistent Hierarchy

```python
class X: pass
class Y: pass

class A(X, Y): pass
class B(Y, X): pass  # reversed order

class C(A, B): pass  # Error!
```

### 2. TypeError Raised

```plaintext
TypeError: Cannot create a consistent method resolution order (MRO)
```

### 3. Fix the Design

Rearrange inheritance to be consistent.

---

## Practical Advice

### 1. Single Inheritance

Prefer single inheritance when possible—simpler MRO.

### 2. Understand Your MRO

Always check `.mro()` in complex hierarchies.

### 3. Use `super()` Consistently

Design all classes to work cooperatively.

### 4. Avoid Deep Hierarchies

Keep inheritance shallow for maintainability.

---

## Key Takeaways

- MRO defines method lookup order.
- Python uses C3 linearization algorithm.
- `.mro()` reveals the resolution order.
- `super()` follows MRO, not just parent.
- Invalid hierarchies raise `TypeError`.

---

## Runnable Example: `diamond_problem.py`

```python
"""
03_diamond_problem.py

INTERMEDIATE LEVEL: The Diamond Problem and Python's Solution

This file explains the classic "diamond problem" in multiple inheritance
and demonstrates how Python's MRO (using C3 linearization) solves it elegantly.

The diamond problem occurs when a class inherits from two classes that both
inherit from a common base class, creating a diamond-shaped inheritance graph.

Learning Objectives:
- Understand what the diamond problem is
- See how Python prevents the diamond problem
- Learn about duplicate base class prevention
- Understand why C3 linearization is important
"""

# ============================================================================
# SECTION 1: What is the Diamond Problem?
# ============================================================================

if __name__ == "__main__":

    """
    The Diamond Problem:

            A
           / \
          B   C
           \ /
            D

    Class D inherits from B and C
    Classes B and C both inherit from A

    Questions that arise:
    1. Which version of A's methods does D get?
    2. Is A's __init__ called once or twice?
    3. In what order are methods searched?
    4. How do we prevent conflicts and ambiguity?

    Python solves this using C3 Linearization algorithm, which ensures:
    - Each class appears only ONCE in the MRO
    - The MRO is consistent and predictable
    - Child classes come before parent classes
    - Parent order is preserved from the class definition
    """


    # ============================================================================
    # SECTION 2: Classic Diamond Problem Example
    # ============================================================================

    class A:
        """
        Base class at the top of the diamond.
        This is the common ancestor.
        """

        def __init__(self):
            print("A.__init__ called")
            self.value_a = "From A"

        def method(self):
            return "Method from A"

        def show_mro(self):
            """Helper method to show where method is called from."""
            return "show_mro from A"


    class B(A):
        """
        Left branch of the diamond.
        Inherits from A.
        """

        def __init__(self):
            print("B.__init__ called")
            super().__init__()  # Call A.__init__
            self.value_b = "From B"

        def method(self):
            return "Method from B"

        def method_b(self):
            return "Specific to B"


    class C(A):
        """
        Right branch of the diamond.
        Also inherits from A.
        """

        def __init__(self):
            print("C.__init__ called")
            super().__init__()  # Call A.__init__
            self.value_c = "From C"

        def method(self):
            return "Method from C"

        def method_c(self):
            return "Specific to C"


    class D(B, C):
        """
        Bottom of the diamond.
        Inherits from both B and C, which both inherit from A.

        This creates the diamond:
               A
              / \
             B   C
              \ /
               D

        Python's MRO: D -> B -> C -> A -> object

        Notice: A appears only ONCE at the end, not twice!
        This is Python's solution to the diamond problem.
        """

        def __init__(self):
            print("D.__init__ called")
            super().__init__()  # This will call the next class in MRO
            self.value_d = "From D"


    print("="*70)
    print("CLASSIC DIAMOND PROBLEM")
    print("="*70)

    # Create an instance of D
    print("\nCreating instance of D:")
    d = D()
    # Notice: A.__init__ is called only ONCE, not twice!

    # View the MRO
    print("\nMRO for class D:")
    for i, cls in enumerate(D.__mro__, 1):
        print(f"{i}. {cls.__name__}")
    # Output:
    # 1. D
    # 2. B
    # 3. C
    # 4. A      <- A appears only once!
    # 5. object

    # Method resolution follows this MRO
    print(f"\nCalling d.method(): {d.method()}")  # Finds in B (first in MRO after D)
    print(f"Calling d.method_b(): {d.method_b()}")  # Finds in B
    print(f"Calling d.method_c(): {d.method_c()}")  # Finds in C
    print(f"Calling d.show_mro(): {d.show_mro()}")  # Finds in A


    # ============================================================================
    # SECTION 3: Understanding super() in Diamond Inheritance
    # ============================================================================

    """
    The key to Python's diamond problem solution is super().

    super() doesn't just call the parent class - it calls the NEXT class in MRO!

    This ensures:
    1. Each class's __init__ is called exactly once
    2. The MRO is followed correctly
    3. No duplicate initialization
    """


    class Animal:
        """Base animal class."""

        def __init__(self, name):
            print(f"Animal.__init__ called for {name}")
            self.name = name


    class Mammal(Animal):
        """Mammal branch."""

        def __init__(self, name, warm_blooded=True):
            print(f"Mammal.__init__ called for {name}")
            super().__init__(name)  # Calls next in MRO, not necessarily Animal!
            self.warm_blooded = warm_blooded


    class Winged(Animal):
        """Winged branch."""

        def __init__(self, name, can_fly=True):
            print(f"Winged.__init__ called for {name}")
            super().__init__(name)  # Calls next in MRO
            self.can_fly = can_fly


    class Bat(Mammal, Winged):
        """
        Bat is both a mammal and winged.

        Diamond structure:
               Animal
               /    \
          Mammal  Winged
               \    /
                Bat

        MRO: Bat -> Mammal -> Winged -> Animal -> object
        """

        def __init__(self, name):
            print(f"Bat.__init__ called for {name}")
            # super().__init__ will call Mammal.__init__ (next in MRO)
            # Mammal's super().__init__ will call Winged.__init__ (next in MRO)
            # Winged's super().__init__ will call Animal.__init__ (next in MRO)
            super().__init__(name, warm_blooded=True)
            self.nocturnal = True


    print("\n" + "="*70)
    print("SUPER() IN DIAMOND INHERITANCE")
    print("="*70)

    print("\nCreating a Bat instance:")
    print("Watch the order of __init__ calls:\n")
    bruce = Bat("Bruce")

    print("\nMRO for Bat:")
    for i, cls in enumerate(Bat.__mro__, 1):
        print(f"{i}. {cls.__name__}")

    print(f"\nBat attributes:")
    print(f"  Name: {bruce.name}")
    print(f"  Warm-blooded: {bruce.warm_blooded}")
    print(f"  Nocturnal: {bruce.nocturnal}")
    # Note: can_fly is not set because we didn't pass it to Mammal.__init__


    # ============================================================================
    # SECTION 4: Proper Diamond Pattern with Keyword Arguments
    # ============================================================================

    """
    To properly handle diamond inheritance with different parameters,
    use **kwargs to pass arguments through the MRO chain.
    """


    class Shape:
        """Base shape class."""

        def __init__(self, color="black", **kwargs):
            print(f"Shape.__init__ called with color={color}")
            super().__init__(**kwargs)  # Pass remaining kwargs up the chain
            self.color = color


    class Rectangle(Shape):
        """Rectangle shape."""

        def __init__(self, width=0, height=0, **kwargs):
            print(f"Rectangle.__init__ called with width={width}, height={height}")
            super().__init__(**kwargs)
            self.width = width
            self.height = height

        def area(self):
            return self.width * self.height


    class Border(Shape):
        """Border mixin."""

        def __init__(self, border_width=1, **kwargs):
            print(f"Border.__init__ called with border_width={border_width}")
            super().__init__(**kwargs)
            self.border_width = border_width


    class BorderedRectangle(Rectangle, Border):
        """
        Rectangle with a border.

        Diamond structure:
               Shape
               /    \
        Rectangle  Border
               \    /
         BorderedRectangle

        MRO: BorderedRectangle -> Rectangle -> Border -> Shape -> object
        """

        def __init__(self, width=0, height=0, border_width=1, color="black"):
            print(f"BorderedRectangle.__init__ called")
            super().__init__(
                width=width,
                height=height,
                border_width=border_width,
                color=color
            )

        def total_area(self):
            """Calculate total area including border."""
            inner_area = self.width * self.height
            border_area = (self.width + 2*self.border_width) * (self.height + 2*self.border_width)
            return border_area


    print("\n" + "="*70)
    print("PROPER DIAMOND PATTERN WITH KWARGS")
    print("="*70)

    print("\nCreating a BorderedRectangle:")
    print("Watch how arguments flow through the MRO:\n")
    rect = BorderedRectangle(width=10, height=5, border_width=2, color="red")

    print("\nMRO for BorderedRectangle:")
    for i, cls in enumerate(BorderedRectangle.__mro__, 1):
        print(f"{i}. {cls.__name__}")

    print(f"\nBorderedRectangle attributes:")
    print(f"  Width: {rect.width}")
    print(f"  Height: {rect.height}")
    print(f"  Border width: {rect.border_width}")
    print(f"  Color: {rect.color}")
    print(f"  Inner area: {rect.area()}")
    print(f"  Total area: {rect.total_area()}")


    # ============================================================================
    # SECTION 5: Invalid MRO - When Diamond Goes Wrong
    # ============================================================================

    """
    Not all inheritance patterns are valid. Python will raise TypeError
    if the MRO cannot be computed consistently using C3 linearization.
    """


    class X:
        pass


    class Y:
        pass


    class A(X, Y):
        """A inherits from X, then Y."""
        pass


    class B(Y, X):
        """B inherits from Y, then X - opposite order!"""
        pass


    # This would create an inconsistent MRO and raise TypeError:
    # class C(A, B):
    #     """
    #     C inherits from A and B.
    #     A says: X before Y
    #     B says: Y before X
    #     This is inconsistent - Python cannot resolve this!
    #     """
    #     pass

    print("\n" + "="*70)
    print("INVALID MRO EXAMPLE")
    print("="*70)

    print("\nTrying to create an inconsistent MRO:")
    print("class A(X, Y): pass  # A says X before Y")
    print("class B(Y, X): pass  # B says Y before X")
    print("class C(A, B): pass  # C cannot resolve: X before Y or Y before X?")
    print("\nThis would raise: TypeError: Cannot create a consistent MRO")


    # Uncomment to see the actual error:
    # try:
    #     class C(A, B):
    #         pass
    # except TypeError as e:
    #     print(f"\nActual error: {e}")


    # ============================================================================
    # SECTION 6: Real-World Diamond Example - GUI Components
    # ============================================================================

    """
    A practical example: GUI components that share common functionality.
    """


    class Widget:
        """Base widget class."""

        def __init__(self, id="widget", **kwargs):
            super().__init__(**kwargs)
            print(f"Widget.__init__: creating {id}")
            self.id = id
            self.visible = True

        def show(self):
            self.visible = True
            return f"{self.id} is now visible"

        def hide(self):
            self.visible = False
            return f"{self.id} is now hidden"


    class Clickable(Widget):
        """Mixin for clickable widgets."""

        def __init__(self, on_click=None, **kwargs):
            super().__init__(**kwargs)
            print(f"Clickable.__init__: setting up click handler")
            self.on_click = on_click
            self.click_count = 0

        def click(self):
            self.click_count += 1
            result = f"Clicked {self.id} (count: {self.click_count})"
            if self.on_click:
                self.on_click()
            return result


    class Hoverable(Widget):
        """Mixin for hoverable widgets."""

        def __init__(self, on_hover=None, **kwargs):
            super().__init__(**kwargs)
            print(f"Hoverable.__init__: setting up hover handler")
            self.on_hover = on_hover
            self.is_hovered = False

        def hover(self):
            self.is_hovered = True
            result = f"Hovering over {self.id}"
            if self.on_hover:
                self.on_hover()
            return result


    class Button(Clickable, Hoverable):
        """
        Button widget that is both clickable and hoverable.

        Diamond structure:
               Widget
               /    \
        Clickable  Hoverable
               \    /
               Button

        MRO: Button -> Clickable -> Hoverable -> Widget -> object
        """

        def __init__(self, id="button", label="Click me", **kwargs):
            super().__init__(id=id, **kwargs)
            print(f"Button.__init__: creating button with label '{label}'")
            self.label = label

        def render(self):
            """Render the button."""
            state = "visible" if self.visible else "hidden"
            hover = " (hovered)" if self.is_hovered else ""
            return f"[Button '{self.label}' - {state}{hover} - clicks: {self.click_count}]"


    print("\n" + "="*70)
    print("REAL-WORLD EXAMPLE: GUI BUTTON")
    print("="*70)

    print("\nCreating a Button:")
    print("Initialization order follows MRO:\n")

    def click_handler():
        print("  -> Click handler executed!")

    def hover_handler():
        print("  -> Hover handler executed!")

    submit_btn = Button(
        id="submit_button",
        label="Submit Form",
        on_click=click_handler,
        on_hover=hover_handler
    )

    print("\nMRO for Button:")
    for i, cls in enumerate(Button.__mro__, 1):
        print(f"{i}. {cls.__name__}")

    print(f"\nButton operations:")
    print(submit_btn.render())
    print(submit_btn.click())
    print(submit_btn.hover())
    print(submit_btn.render())
    print(submit_btn.click())
    print(submit_btn.render())


    # ============================================================================
    # SECTION 7: Key Takeaways
    # ============================================================================

    """
    KEY POINTS ABOUT THE DIAMOND PROBLEM:

    1. Diamond Problem Structure:
               A
              / \
             B   C
              \ /
               D
       D inherits from B and C, both inherit from A

    2. Python's Solution:
       - C3 Linearization algorithm
       - Each class appears ONLY ONCE in MRO
       - Preserves order of parent classes
       - Ensures consistent, predictable method resolution

    3. super() is the Key:
       - super() calls the NEXT class in MRO, not the parent
       - This prevents duplicate initialization
       - Always use super() in cooperative inheritance

    4. Use **kwargs:
       - Pass parameters through the MRO chain
       - Each class takes what it needs
       - Passes the rest to super().__init__()

    5. Invalid MROs:
       - Some inheritance patterns are inconsistent
       - Python raises TypeError for invalid MRO
       - Different parent orders can create conflicts

    6. Practical Uses:
       - Mixin classes (Clickable, Hoverable, etc.)
       - Shared functionality across hierarchies
       - Plugin architectures
       - Framework base classes

    7. Best Practices:
       - Document your MRO intentions
       - Use super() consistently
       - Design parent classes to be "cooperative"
       - Test complex hierarchies thoroughly
       - Consider composition for very complex scenarios
    """

    print("\n" + "="*70)
    print("END OF DIAMOND PROBLEM TUTORIAL")
    print("="*70)
    print("\nNext: Learn about super() and its relationship with MRO!")
```


---

## Runnable Example: `mro_diamond_problem.py`

```python
"""
TUTORIAL: Method Resolution Order (MRO) - Understanding the Diamond Problem
===========================================================================

In this tutorial, you'll learn how Python's Method Resolution Order (MRO)
handles the "diamond problem" in multiple inheritance.

The Diamond Problem:
  A class (Leaf) inherits from two classes (A and B) which both inherit from
  a common parent (Root). When you call a method on Leaf, which version runs?
  This is the diamond problem.

Python uses C3 Linearization to solve this:
  1. Each class is visited in a specific order
  2. Each class appears only once in the order
  3. A class never appears before its parents
  4. The order respects the order in which parents are listed

Key Insight: super() uses MRO to call the next method in the chain.
This allows cooperative multiple inheritance where methods can be properly
delegated up the inheritance hierarchy.

In this example, we see:
  - How print(ClassName.__mro__) shows the resolution order
  - How super() uses MRO to call methods
  - Which methods get called from which classes
  - Why the order matters
"""


# ============ Example 1: Defining the Diamond Inheritance Hierarchy ============

if __name__ == "__main__":
    print("=" * 70)
    print("EXAMPLE 1: Diamond inheritance - Root > A, B > Leaf")
    print("=" * 70)

    class Root:
        """The common parent at the top of the diamond.

        Both A and B inherit from Root. Methods here are called when
        neither A, B, nor Leaf override them.
        """
        def ping(self):
            print(f'{self}.ping() in Root')

        def pong(self):
            print(f'{self}.pong() in Root')

        def __repr__(self):
            cls_name = type(self).__name__
            return f'<instance of {cls_name}>'


    class A(Root):
        """Left side of the diamond.

        Inherits from Root. Both ping() and pong() use super() to call
        the parent implementation, continuing the method chain.
        """
        def ping(self):
            print(f'{self}.ping() in A')
            super().ping()

        def pong(self):
            print(f'{self}.pong() in A')
            super().pong()


    class B(Root):
        """Right side of the diamond.

        Inherits from Root. ping() calls super(), but pong() does NOT.
        This demonstrates how different classes can handle the chain differently.
        """
        def ping(self):
            print(f'{self}.ping() in B')
            super().ping()

        def pong(self):
            print(f'{self}.pong() in B')
            # Note: No super().pong() call - chain stops here


    class Leaf(A, B):
        """Bottom of the diamond - inherits from both A and B.

        Leaf specifies inheritance order: A first, then B.
        This order affects the MRO.
        """
        def ping(self):
            print(f'{self}.ping() in Leaf')
            super().ping()


    print(f"\nDiamond hierarchy defined:")
    print(f"         Root")
    print(f"        /    \\")
    print(f"       A      B")
    print(f"        \\    /")
    print(f"         Leaf")
    print(f"\nClass definitions:")
    print(f"  class Root: ping(), pong()")
    print(f"  class A(Root): ping() with super(), pong() with super()")
    print(f"  class B(Root): ping() with super(), pong() WITHOUT super()")
    print(f"  class Leaf(A, B): ping() with super()")


    # ============ Example 2: Understanding the Method Resolution Order ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Method Resolution Order (MRO)")
    print("=" * 70)

    print(f"\nLeaf.__mro__ shows the order methods are looked up:")
    mro = Leaf.__mro__
    print(f"  {Leaf.__mro__}")

    print(f"\nBreaking it down:")
    for i, cls in enumerate(mro):
        print(f"  {i}. {cls}")

    print(f"\nWhat this means:")
    print(f"  - When Leaf.method() is called, Python looks in Leaf first")
    print(f"  - Then A (from Leaf(A, B) left-to-right order)")
    print(f"  - Then B")
    print(f"  - Then Root")
    print(f"  - Finally object (implicit parent of all classes)")

    print(f"\nWhy this order?")
    print(f"  1. Leaf inherits from A first, so A has priority")
    print(f"  2. A and B both inherit from Root, but Root comes after both")
    print(f"  3. This respects the inheritance hierarchy")
    print(f"  4. C3 Linearization ensures consistency")


    # ============ Example 3: Calling ping() - Method Chain with super() ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Calling ping() - tracing the super() chain")
    print("=" * 70)

    leaf1 = Leaf()
    print(f"\nleaf1 = Leaf()")
    print(f"leaf1.ping()  # Trace the method chain:")
    print()
    leaf1.ping()

    print(f"\nExplanation of ping() call chain:")
    print(f"  1. Leaf.ping() called")
    print(f"     - Prints: '<instance of Leaf>.ping() in Leaf'")
    print(f"     - Calls: super().ping()")
    print(f"     - super() uses MRO: next class after Leaf is A")
    print(f"\n  2. A.ping() called via super()")
    print(f"     - Prints: '<instance of Leaf>.ping() in A'")
    print(f"     - Calls: super().ping()")
    print(f"     - super() uses MRO: next class after A is B")
    print(f"\n  3. B.ping() called via super()")
    print(f"     - Prints: '<instance of Leaf>.ping() in B'")
    print(f"     - Calls: super().ping()")
    print(f"     - super() uses MRO: next class after B is Root")
    print(f"\n  4. Root.ping() called via super()")
    print(f"     - Prints: '<instance of Leaf>.ping() in Root'")
    print(f"     - No super() call, chain ends")


    # ============ Example 4: Calling pong() - Super Chain Stops Early ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Calling pong() - where the super() chain stops")
    print("=" * 70)

    print(f"\nleaf1.pong()  # Trace the pong() chain:")
    print()
    leaf1.pong()

    print(f"\nExplanation of pong() call chain:")
    print(f"  1. Leaf doesn't override pong(), so MRO looks further")
    print(f"     - Next class with pong() is A")
    print(f"\n  2. A.pong() called")
    print(f"     - Prints: '<instance of Leaf>.pong() in A'")
    print(f"     - Calls: super().pong()")
    print(f"     - super() uses MRO: next class is B")
    print(f"\n  3. B.pong() called via super()")
    print(f"     - Prints: '<instance of Leaf>.pong() in B'")
    print(f"     - NOTE: No super().pong() call!")
    print(f"     - Chain STOPS here, Root.pong() is never called!")

    print(f"\nKey insight:")
    print(f"  - A calls super(), so chain continues to B")
    print(f"  - B does NOT call super(), so chain stops")
    print(f"  - Root.pong() is never reached")
    print(f"  - This is a design choice - B can intentionally end the chain")


    # ============ Example 5: MRO Affects Behavior ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: MRO affects which implementation runs")
    print("=" * 70)

    print(f"\nWhat if we changed Leaf(A, B) to Leaf(B, A)?")
    print(f"  class Leaf(B, A):  # B first, then A")
    print(f"      def ping(self):")
    print(f"          print(f'{{self}}.ping() in Leaf')")
    print(f"          super().ping()")

    class LeafReversed(B, A):
        """Same as Leaf but with inheritance order reversed."""
        def ping(self):
            print(f'{self}.ping() in LeafReversed')
            super().ping()

    print(f"\nLeafReversed.__mro__:")
    print(f"  {LeafReversed.__mro__}")

    print(f"\nNotice: B comes before A now!")
    print(f"  (because Leaf(B, A) puts B first)")

    leaf2 = LeafReversed()
    print(f"\nleaf2 = LeafReversed()")
    print(f"leaf2.ping():")
    print()
    leaf2.ping()


    # ============ Example 6: Multiple Inheritance with Shared Methods ============
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Why super() is better than explicit parent calls")
    print("=" * 70)

    print(f"\nWithout super() (explicit parent calls):")
    print(f"  class A(Root):")
    print(f"      def ping(self):")
    print(f"          print('ping in A')")
    print(f"          Root.ping(self)  # EXPLICIT call")

    print(f"\nProblem: If we change inheritance (Leaf inherits from B, A),")
    print(f"A still calls Root directly, skipping B in the chain!")

    print(f"\nWith super() (uses MRO):")
    print(f"  class A(Root):")
    print(f"      def ping(self):")
    print(f"          print('ping in A')")
    print(f"          super().ping()  # Uses MRO")

    print(f"\nAdvantage: super() automatically uses the MRO,")
    print(f"so it works correctly regardless of inheritance order!")

    print(f"\nIn Leaf(A, B): super() in A calls B (correct chain)")
    print(f"In LeafReversed(B, A): super() in A calls Root (still correct)")


    # ============ Example 7: Real-World MRO Example ============
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Practical example - Mixin classes with MRO")
    print("=" * 70)

    class TimestampMixin:
        """A mixin that adds timestamp capability."""
        def get_info(self):
            return f'{super().get_info()} [timestamped]'

    class SerializableMixin:
        """A mixin that adds serialization capability."""
        def get_info(self):
            return f'{super().get_info()} [serializable]'

    class DataObject:
        """Base class for data objects."""
        def get_info(self):
            return 'DataObject'

    class Document(TimestampMixin, SerializableMixin, DataObject):
        """Document with multiple capabilities via mixins."""
        pass

    print(f"\nDocument.__mro__:")
    print(f"  {Document.__mro__}")

    doc = Document()
    print(f"\ndoc = Document()")
    print(f"doc.get_info() = '{doc.get_info()}'")

    print(f"\nMethod chain:")
    print(f"  1. Document.get_info() → not found, use MRO")
    print(f"  2. TimestampMixin.get_info() → adds '[timestamped]'")
    print(f"     → calls super().get_info()")
    print(f"  3. SerializableMixin.get_info() → adds '[serializable]'")
    print(f"     → calls super().get_info()")
    print(f"  4. DataObject.get_info() → returns 'DataObject'")


    # ============ Example 8: Summary - MRO Best Practices ============
    print("\n" + "=" * 70)
    print("EXAMPLE 8: Summary - MRO Best Practices")
    print("=" * 70)

    print(f"\nRules for MRO (C3 Linearization):")
    print(f"  1. Child classes come before parents")
    print(f"  2. Parents are listed in inheritance order")
    print(f"  3. Each class appears only once")

    print(f"\nUsing super() effectively:")
    print(f"  1. Always use super() instead of explicit parent calls")
    print(f"  2. super() respects MRO and works with multiple inheritance")
    print(f"  3. Mixins should always use super() to continue the chain")
    print(f"  4. Remember: super() doesn't call the parent - it calls the NEXT class in MRO")

    print(f"\nDebugging MRO:")
    print(f"  1. Print ClassName.__mro__ to see the resolution order")
    print(f"  2. Use print() statements to trace method chains")
    print(f"  3. Remember that inheritance order matters!")

    print(f"\nCommon mistakes:")
    print(f"  1. Forgetting super() in a cooperative hierarchy")
    print(f"  2. Not understanding that inheritance order affects MRO")
    print(f"  3. Calling parent explicitly instead of using super()")

    print(f"\n" + "=" * 70)
```

---

## Exercises

**Exercise 1.**
Create a hierarchy: `A`, `B(A)`, `C(A)`, `D(B, C)`. Print `D.__mro__` and `D.mro()`. Add a `who_am_i()` method to each class. Call `D().who_am_i()` and predict which version runs. Then override only in `C` and call again --- predict which version runs based on MRO.

??? success "Solution to Exercise 1"

        class A:
            def who_am_i(self):
                return "A"

        class B(A):
            def who_am_i(self):
                return "B"

        class C(A):
            def who_am_i(self):
                return "C"

        class D(B, C):
            pass

        print(D.__mro__)
        # D -> B -> C -> A -> object

        print(D().who_am_i())  # "B" — first in MRO after D

        # Override only in C, remove from B
        class B2(A):
            pass

        class D2(B2, C):
            pass

        print(D2().who_am_i())  # "C" — B2 doesn't have it, falls to C

---

**Exercise 2.**
Create a diamond hierarchy where each class has a `describe()` method that returns its class name. In each `describe()`, also call `super().describe()` and concatenate the results. Show the full chain of method calls by printing the result of `Bottom().describe()`.

??? success "Solution to Exercise 2"

        class Base:
            def describe(self):
                return "Base"

        class Left(Base):
            def describe(self):
                return f"Left -> {super().describe()}"

        class Right(Base):
            def describe(self):
                return f"Right -> {super().describe()}"

        class Bottom(Left, Right):
            def describe(self):
                return f"Bottom -> {super().describe()}"

        print(Bottom().describe())
        # Bottom -> Left -> Right -> Base

---

**Exercise 3.**
Write a function `show_mro(cls)` that takes a class and prints its MRO in a formatted way, showing each class and its module. Use `cls.__mro__` to iterate. Test it with Python's built-in `bool` class to see its full MRO chain (`bool -> int -> object`).

??? success "Solution to Exercise 3"

        def show_mro(cls):
            print(f"MRO for {cls.__name__}:")
            for i, c in enumerate(cls.__mro__):
                module = c.__module__
                print(f"  {i}: {module}.{c.__name__}")

        show_mro(bool)
        # MRO for bool:
        #   0: builtins.bool
        #   1: builtins.int
        #   2: builtins.object
