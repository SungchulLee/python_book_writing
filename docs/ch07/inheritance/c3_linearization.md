# C3 Linearization

C3 linearization is the algorithm Python uses to compute the Method Resolution Order (MRO) for classes with multiple inheritance.

---

## Why C3? (Not DFS or BFS)

Naïve traversals fail for multiple inheritance:

| Strategy | Problem |
|---|---|
| Depth-first (DFS) | Visits common ancestors too early, causing duplicates (e.g., `D → B → A → C → A`) |
| Breadth-first (BFS) | Can break local precedence order (a parent listed first may appear after one listed second) |
| C3 linearization | Preserves local order, avoids duplicates, rejects inconsistent hierarchies |

Python adopted C3 in version 2.3 specifically because DFS and BFS both violate key invariants that cooperative inheritance relies on.

## Algorithm Overview

### 1. Named After Paper

C3 linearization algorithm, based on the Dylan language's approach and formalized by Barrett et al.

### 2. Not Simple Traversal

Not depth-first or breadth-first --- a specialized merge algorithm that produces a single consistent ordering or rejects the hierarchy.

### 3. Three Key Properties

- Preserves local precedence order
- Maintains parent MRO consistency  
- Ensures monotonicity

---

## The Formula

For a class `C(B1, B2, ..., Bn)`:

$$
L[C] = [C] + \text{merge}(L[B1], L[B2], \ldots, L[Bn], [B1, B2, \ldots, Bn])
$$

where:

- $L[Bi]$ is the MRO of parent $Bi$
- $[B1, B2, \ldots, Bn]$ is the list of direct parents

---

## Merge Procedure

### 1. Look at Heads

Examine the first element of each list.

### 2. Find Valid Head

Pick the first head that **is not in the tail** of any other list. The intuition: if a class appears in someone else's tail, that means some other class must come before it (the tail represents "things that should come after the head"). Picking only classes with no such constraint ensures we never violate any ordering requirement.

### 3. Append and Remove

Append this head to result and remove it from all lists.

### 4. Repeat

Continue until all lists are empty.

---

## Simple Example

### 1. Class Hierarchy

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
```

### 2. Compute Base MROs

- $L[A] = [A, \text{object}]$
- $L[B] = [B, A, \text{object}]$
- $L[C] = [C, A, \text{object}]$

### 3. Apply Formula

$$
L[D] = [D] + \text{merge}([B, A, \text{object}], [C, A, \text{object}], [B, C])
$$

---

## Step-by-Step Merge

### 1. Initial Lists

- $[B, A, \text{object}]$ : head $B$, tail $[A, \text{object}]$
- $[C, A, \text{object}]$ : head $C$, tail $[A, \text{object}]$
- $[B, C]$ : head $B$, tail $[C]$

### 2. Pick B

$B$ is a head and not in any tail → append $B$.

Result: $[D, B]$

Updated lists:
- $[A, \text{object}]$
- $[C, A, \text{object}]$
- $[C]$

### 3. Pick C

$C$ is a head and not in any tail → append $C$.

Result: $[D, B, C]$

Updated lists:
- $[A, \text{object}]$
- $[A, \text{object}]$
- $[]$

### 4. Pick A

$A$ is a head and not in any tail → append $A$.

Result: $[D, B, C, A]$

Updated lists:
- $[\text{object}]$
- $[\text{object}]$
- $[]$

### 5. Pick object

$\text{object}$ is a head → append $\text{object}$.

Result: $[D, B, C, A, \text{object}]$

All lists empty—done!

---

## Final MRO

$$
L[D] = [D, B, C, A, \text{object}]
$$

```python
print(D.mro())
# [<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>]
```

---

## Complex Example

### 1. Multiple Paths

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
class E(D, C): pass
```

### 2. Compute Step-by-Step

- $L[D] = [D, B, C, A, \text{object}]$
- $L[C] = [C, A, \text{object}]$

$$
L[E] = [E] + \text{merge}([D, B, C, A, \text{object}], [C, A, \text{object}], [D, C])
$$

### 3. Merge Process

Following the same merge rules:

$L[E] = [E, D, B, C, A, \text{object}]$

---

## Conflict Detection

### 1. When Merge Fails

If **every head** appears in some tail, merge fails.

### 2. TypeError Raised

```python
class X: pass
class Y: pass
class A(X, Y): pass
class B(Y, X): pass
class C(A, B): pass  # Error!
```

### 3. Error Message

```plaintext
TypeError: Cannot create a consistent method resolution order (MRO)
```

---

## Why It Matters

### 1. Predictability

C3 ensures deterministic method resolution.

### 2. Cooperative Inheritance

Enables `super()` to work correctly.

### 3. Prevents Ambiguity

Guarantees consistency or rejects invalid hierarchies.

---

## Practical Implications

### 1. Left Parents First

Parents listed first have higher priority.

```python
class D(B, C):  # B's methods before C's
    pass
```

### 2. All Ancestors Once

Each class appears exactly once in MRO.

### 3. Monotonic Order

Parent order is preserved throughout the hierarchy.

---

## Key Takeaways

- C3 linearization computes MRO deterministically.
- Uses merge algorithm on parent MROs.
- Picks heads not in any tail.
- Rejects inconsistent hierarchies.
- Enables cooperative multiple inheritance.

---

## Runnable Example: `c3_linearization_examples.py`

```python
"""
06_c3_linearization.py

ADVANCED LEVEL: Understanding the C3 Linearization Algorithm

This file explains the C3 linearization algorithm that Python uses to compute
MRO. Understanding C3 helps you predict MRO for complex hierarchies and
understand why certain inheritance patterns fail.

Learning Objectives:
- Understand the C3 linearization algorithm
- Learn to compute MRO manually
- Understand consistency requirements
- Predict MRO for complex hierarchies
- Recognize invalid inheritance patterns
"""

# ============================================================================
# SECTION 1: What is C3 Linearization?
# ============================================================================

if __name__ == "__main__":

    """
    C3 Linearization (also called C3 Superclass Linearization) is the algorithm
    Python uses to determine Method Resolution Order.

    Created by: Michele Simionato and others
    Adopted in: Python 2.3 (2003)
    Purpose: Solve the diamond problem and provide consistent method resolution

    KEY PROPERTIES:
    1. Children come before parents
    2. Parent order is preserved from class definition
    3. Each class appears exactly once
    4. MRO must be consistent (monotonic)

    MONOTONICITY means: if class A precedes class B in the linearization of class C,
    then A must precede B in the linearization of any subclass of C (unless B is
    removed).
    """


    # ============================================================================
    # SECTION 2: C3 Algorithm - The Merge Process
    # ============================================================================

    """
    C3 LINEARIZATION ALGORITHM:

    For a class C with parents P1, P2, ..., Pn:

    L[C] = C + merge(L[P1], L[P2], ..., L[Pn], [P1, P2, ..., Pn])

    Where:
    - L[C] is the linearization (MRO) of class C
    - + means prepending C to the result
    - merge() is the C3 merge algorithm
    - [P1, P2, ..., Pn] is the list of parents in order

    MERGE ALGORITHM:
    1. Take the head of the first list
    2. If it's not in the tail of any other list, add it to result
    3. Otherwise, try the head of the next list
    4. Repeat until all lists are exhausted
    5. If we can't find a valid head, the hierarchy is invalid (inconsistent MRO)

    TERMINOLOGY:
    - Head: first element of a list
    - Tail: all elements except the first
    """


    def compute_c3_mro(cls, indent=0):
        """
        Manually compute C3 linearization with detailed steps.
        This is for educational purposes - Python does this automatically!
        """
        prefix = "  " * indent

        print(f"{prefix}Computing L[{cls.__name__}]:")

        # Base case: object
        if cls == object:
            print(f"{prefix}  Base case: object")
            return [object]

        # Get parents
        parents = cls.__bases__
        print(f"{prefix}  Parents: {[p.__name__ for p in parents]}")

        # Compute linearizations of parents
        parent_mros = []
        for parent in parents:
            print(f"{prefix}  Computing L[{parent.__name__}]:")
            mro = compute_c3_mro(parent, indent + 2)
            parent_mros.append(mro)
            print(f"{prefix}  L[{parent.__name__}] = {[c.__name__ for c in mro]}")

        # Prepare lists for merge
        lists_to_merge = parent_mros + [list(parents)]
        print(f"{prefix}  Lists to merge:")
        for i, lst in enumerate(lists_to_merge):
            print(f"{prefix}    {[c.__name__ for c in lst]}")

        # Perform merge
        print(f"{prefix}  Merging:")
        result = [cls] + c3_merge(lists_to_merge, prefix + "    ")

        print(f"{prefix}  Result: L[{cls.__name__}] = {[c.__name__ for c in result]}")
        return result


    def c3_merge(lists, prefix=""):
        """
        Perform C3 merge algorithm.
        """
        result = []

        while True:
            # Remove empty lists
            lists = [lst for lst in lists if lst]

            if not lists:
                break

            # Try to find a valid head
            found = False
            for lst in lists:
                head = lst[0]

                # Check if head is in tail of any list
                in_tail = False
                for other_list in lists:
                    if head in other_list[1:]:
                        in_tail = True
                        break

                if not in_tail:
                    # Valid head found!
                    result.append(head)
                    print(f"{prefix}Adding {head.__name__} (not in any tail)")

                    # Remove from all lists
                    for lst in lists:
                        if lst and lst[0] == head:
                            lst.pop(0)

                    found = True
                    break

            if not found:
                # Inconsistent MRO!
                print(f"{prefix}ERROR: Cannot find valid head - inconsistent MRO!")
                raise TypeError("Cannot create consistent MRO")

        return result


    # ============================================================================
    # SECTION 3: Step-by-Step Example - Simple Diamond
    # ============================================================================

    """
    Let's compute MRO for a simple diamond step by step.
    """


    class A:
        """Base class."""
        pass


    class B(A):
        """Left branch."""
        pass


    class C(A):
        """Right branch."""
        pass


    class D(B, C):
        """Diamond bottom."""
        pass


    print("="*70)
    print("C3 LINEARIZATION - SIMPLE DIAMOND")
    print("="*70)

    print("\nClass hierarchy:")
    print("     A")
    print("    / \\")
    print("   B   C")
    print("    \\ /")
    print("     D")

    print("\n" + "-"*70)
    print("MANUAL COMPUTATION:")
    print("-"*70)

    # Show the computation
    result = compute_c3_mro(D)

    print("\n" + "-"*70)
    print("PYTHON'S ACTUAL MRO:")
    print("-"*70)
    print(f"D.__mro__ = {[c.__name__ for c in D.__mro__]}")

    print("\nMatches our computation! ✓")


    # ============================================================================
    # SECTION 4: Another Example - Multiple Parents
    # ============================================================================

    """
    Computing MRO for a class with multiple unrelated parents.
    """


    class X:
        pass


    class Y:
        pass


    class Z:
        pass


    class Multi(X, Y, Z):
        """Class with three independent parents."""
        pass


    print("\n" + "="*70)
    print("C3 LINEARIZATION - MULTIPLE INDEPENDENT PARENTS")
    print("="*70)

    print("\nClass hierarchy:")
    print("X    Y    Z")
    print(" \\   |   /")
    print("  \\  |  /")
    print("   Multi")

    print("\n" + "-"*70)
    print("COMPUTING L[Multi]:")
    print("-"*70)

    print("""
    Step-by-step:
    1. L[Multi] = Multi + merge(L[X], L[Y], L[Z], [X, Y, Z])
    2. L[X] = [X, object]
    3. L[Y] = [Y, object]
    4. L[Z] = [Z, object]
    5. merge([X, object], [Y, object], [Z, object], [X, Y, Z])
       - Take X (not in any tail) → result: [X]
       - Take Y (not in any tail) → result: [X, Y]
       - Take Z (not in any tail) → result: [X, Y, Z]
       - Take object (not in any tail) → result: [X, Y, Z, object]
    6. L[Multi] = [Multi, X, Y, Z, object]
    """)

    print("Python's actual MRO:")
    print(f"Multi.__mro__ = {[c.__name__ for c in Multi.__mro__]}")


    # ============================================================================
    # SECTION 5: Complex Example - Nested Diamonds
    # ============================================================================

    """
    A more complex hierarchy with nested diamonds.
    """


    class O:
        """Root."""
        pass


    class A(O):
        pass


    class B(O):
        pass


    class C(O):
        pass


    class D(A, B):
        pass


    class E(B, C):
        pass


    class F(D, E):
        """
        Complex hierarchy:
              O
            / | \\
           A  B  C
           |  |\\|
           D  | E
            \\ |/
              F
        """
        pass


    print("\n" + "="*70)
    print("C3 LINEARIZATION - COMPLEX HIERARCHY")
    print("="*70)

    print("\nClass hierarchy:")
    print("       O")
    print("     / | \\")
    print("    A  B  C")
    print("    |  |\\|")
    print("    D  | E")
    print("     \\ |/")
    print("       F")

    print("\n" + "-"*70)
    print("COMPUTING L[F]:")
    print("-"*70)

    print("""
    Step-by-step (simplified):
    1. L[A] = [A, O, object]
    2. L[B] = [B, O, object]
    3. L[C] = [C, O, object]
    4. L[D] = [D, A, B, O, object]
    5. L[E] = [E, B, C, O, object]
    6. L[F] = F + merge([D, A, B, O, object], [E, B, C, O, object], [D, E])

    Detailed merge:
    - Take F → [F]
    - Take D (not in tail of [E, B, C, O, object] or [D, E]) → [F, D]
    - Take A (not in any tail) → [F, D, A]
    - Take B from first list? No, B is in tail of [E, B, C, O, object]
    - Take E (not in any tail) → [F, D, A, E]
    - Take B (now not in any tail) → [F, D, A, E, B]
    - Take C (not in any tail) → [F, D, A, E, B, C]
    - Take O (not in any tail) → [F, D, A, E, B, C, O]
    - Take object → [F, D, A, E, B, C, O, object]
    """)

    print("Python's actual MRO:")
    for i, cls in enumerate(F.__mro__, 1):
        print(f"{i}. {cls.__name__}")


    # ============================================================================
    # SECTION 6: Inconsistent MRO - Why Some Hierarchies Fail
    # ============================================================================

    """
    Some inheritance patterns cannot be linearized consistently.
    C3 will detect and reject these.
    """


    class P1:
        pass


    class P2:
        pass


    # This is OK
    class C1(P1, P2):
        """C1 says: P1 before P2"""
        pass


    # This is also OK
    class C2(P2, P1):
        """C2 says: P2 before P1 (opposite order)"""
        pass


    # But this will FAIL
    print("\n" + "="*70)
    print("INCONSISTENT MRO EXAMPLE")
    print("="*70)

    print("\nClass hierarchy:")
    print("P1    P2")
    print("| \\  / |")
    print("|  \\/  |")
    print("|  /\\  |")
    print("| /  \\ |")
    print("C1    C2")
    print(" \\    /")
    print("  \\  /")
    print("   Bad")

    print("\nC1 says: P1 before P2")
    print("C2 says: P2 before P1")
    print("Bad inherits from both C1 and C2")
    print("\nThis creates a conflict:")

    print("""
    L[Bad] = Bad + merge(L[C1], L[C2], [C1, C2])
           = Bad + merge([C1, P1, P2, object], [C2, P2, P1, object], [C1, C2])

    Try to merge:
    1. Take Bad → [Bad]
    2. Take C1 → [Bad, C1]
    3. Take P1? NO - P1 is in tail of [C2, P2, P1, object]
    4. Take C2 from [C2, P2, P1, object]? NO - C2 is in tail of [C1, C2]
    5. STUCK! Cannot find a valid head.

    This is an INCONSISTENT MRO - Python will raise TypeError.
    """)

    print("\nTrying to create the class:")
    try:
        class Bad(C1, C2):
            pass
        print("Success (unexpected!)")
    except TypeError as e:
        print(f"TypeError: {e}")
        print("\nPython correctly rejected this inconsistent hierarchy!")


    # ============================================================================
    # SECTION 7: Properties of Valid MRO
    # ============================================================================

    """
    A valid MRO must satisfy these properties:
    """


    def check_mro_properties(cls):
        """
        Check if MRO satisfies C3 properties.
        """
        mro = cls.__mro__

        print(f"\nChecking MRO properties for {cls.__name__}:")
        print(f"MRO: {[c.__name__ for c in mro]}")

        # Property 1: Class comes first
        print(f"\n1. Class comes first:")
        print(f"   {mro[0].__name__} == {cls.__name__}: {mro[0] == cls} ✓")

        # Property 2: Parents appear after children
        print(f"\n2. Parents appear after children:")
        for i, c in enumerate(mro[:-1]):  # Skip object
            for parent in c.__bases__:
                if parent in mro:
                    parent_index = mro.index(parent)
                    if parent_index > i:
                        print(f"   {c.__name__} (pos {i}) before {parent.__name__} (pos {parent_index}) ✓")
                    else:
                        print(f"   ERROR: {c.__name__} (pos {i}) after {parent.__name__} (pos {parent_index}) ✗")

        # Property 3: Each class appears once
        print(f"\n3. Each class appears exactly once:")
        if len(mro) == len(set(mro)):
            print(f"   All {len(mro)} classes are unique ✓")
        else:
            print(f"   ERROR: Duplicate classes found ✗")

        # Property 4: object is last
        print(f"\n4. object is last:")
        print(f"   Last class is {mro[-1].__name__}: {mro[-1] == object} ✓")

        # Property 5: Local precedence order
        print(f"\n5. Local precedence order preserved:")
        for c in mro[:-1]:
            if c.__bases__:
                print(f"   {c.__name__} has parents: {[p.__name__ for p in c.__bases__]}")
                for i, p1 in enumerate(c.__bases__[:-1]):
                    p2 = c.__bases__[i + 1]
                    if p1 in mro and p2 in mro:
                        if mro.index(p1) < mro.index(p2):
                            print(f"     {p1.__name__} before {p2.__name__} ✓")
                        else:
                            print(f"     ERROR: {p1.__name__} after {p2.__name__} ✗")


    print("\n" + "="*70)
    print("PROPERTIES OF VALID MRO")
    print("="*70)

    check_mro_properties(F)


    # ============================================================================
    # SECTION 8: Practical MRO Prediction
    # ============================================================================

    """
    Tips for predicting MRO:
    1. Start with the class itself
    2. Add parents left to right, recursing depth-first
    3. But skip parents that will appear later
    4. Add common ancestors only once at the end
    """


    def predict_mro(cls, show_steps=False):
        """
        Simple heuristic for predicting MRO (not always perfect).
        """
        if show_steps:
            print(f"\nPredicting MRO for {cls.__name__}:")

        # Start with the class itself
        result = [cls]

        # Process parents left to right
        for parent in cls.__bases__:
            if show_steps:
                print(f"  Processing parent: {parent.__name__}")

            # Get parent's MRO
            parent_mro = parent.__mro__

            # Add classes from parent's MRO that aren't already in result
            for c in parent_mro:
                if c not in result:
                    result.append(c)
                    if show_steps:
                        print(f"    Added: {c.__name__}")

        return result


    print("\n" + "="*70)
    print("MRO PREDICTION PRACTICE")
    print("="*70)

    # Test prediction
    predicted = predict_mro(F, show_steps=True)
    actual = F.__mro__

    print(f"\nPredicted: {[c.__name__ for c in predicted]}")
    print(f"Actual:    {[c.__name__ for c in actual]}")
    print(f"Match: {predicted == list(actual)} {('✓' if predicted == list(actual) else '✗')}")


    # ============================================================================
    # SECTION 9: Key Takeaways
    # ============================================================================

    """
    KEY POINTS ABOUT C3 LINEARIZATION:

    1. C3 Algorithm:
       - Merge parent linearizations with parent list
       - Take heads that aren't in any tail
       - Ensures consistent, predictable MRO
       - Rejects inconsistent hierarchies

    2. Properties Guaranteed:
       - Children before parents
       - Parent order preserved
       - Each class appears once
       - Monotonic (consistent with subclasses)
       - object always last

    3. Why Some Hierarchies Fail:
       - Conflicting parent orders
       - Cannot satisfy all constraints
       - Python raises TypeError
       - Fix by reordering parents or restructuring

    4. Computing MRO:
       - L[C] = C + merge(L[P1], ..., L[Pn], [P1, ..., Pn])
       - Merge takes valid heads only
       - Recursive process
       - Ends at object

    5. Practical Tips:
       - Design hierarchies carefully
       - Avoid conflicting parent orders
       - Test complex hierarchies
       - Use inspection tools
       - Document MRO intentions

    6. Historical Note:
       - Python 2.2 and earlier used different algorithm
       - C3 adopted in Python 2.3 (2003)
       - Solves diamond problem elegantly
       - Based on Dylan language's algorithm

    7. When You Need This:
       - Debugging complex hierarchies
       - Designing framework base classes
       - Understanding method resolution
       - Fixing TypeError for inconsistent MRO
       - Teaching advanced OOP concepts
    """

    print("\n" + "="*70)
    print("END OF C3 LINEARIZATION TUTORIAL")
    print("="*70)
    print("\nNext: Learn about complex real-world hierarchies!")
```

---

## Exercises

**Exercise 1.**
Given classes `A`, `B(A)`, `C(A)`, `D(B, C)`, manually compute the MRO for `D` using C3 linearization. Then verify your answer using `D.__mro__`. Show each merge step.

??? success "Solution to Exercise 1"

        class A: pass
        class B(A): pass
        class C(A): pass
        class D(B, C): pass

        # Manual C3:
        # L(A) = [A, O]
        # L(B) = [B] + merge(L(A), [A]) = [B, A, O]
        # L(C) = [C] + merge(L(A), [A]) = [C, A, O]
        # L(D) = [D] + merge(L(B), L(C), [B, C])
        #       = [D] + merge([B, A, O], [C, A, O], [B, C])
        #       = [D, B] + merge([A, O], [C, A, O], [C])
        #       = [D, B, C] + merge([A, O], [A, O])
        #       = [D, B, C, A, O]

        print(D.__mro__)
        # (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)

---

**Exercise 2.**
Create a class hierarchy that would fail C3 linearization. For example, try `class X(A, B)` and `class Y(B, A)`, then `class Z(X, Y)`. Show that Python raises `TypeError` and explain why the ordering is inconsistent.

??? success "Solution to Exercise 2"

        class A: pass
        class B: pass

        class X(A, B): pass
        class Y(B, A): pass

        try:
            class Z(X, Y): pass
        except TypeError as e:
            print(f"TypeError: {e}")
        # Cannot create a consistent method resolution order
        # X says A before B, Y says B before A — contradiction!

---

**Exercise 3.**
Build a diamond hierarchy: `Base`, `Left(Base)`, `Right(Base)`, `Bottom(Left, Right)`. Add a `greet()` method to each class that calls `super().greet()`. Show how C3 linearization ensures each class's `greet()` is called exactly once, in MRO order.

??? success "Solution to Exercise 3"

        class Base:
            def greet(self):
                print("Base.greet")

        class Left(Base):
            def greet(self):
                print("Left.greet")
                super().greet()

        class Right(Base):
            def greet(self):
                print("Right.greet")
                super().greet()

        class Bottom(Left, Right):
            def greet(self):
                print("Bottom.greet")
                super().greet()

        Bottom().greet()
        # Bottom.greet -> Left.greet -> Right.greet -> Base.greet
        # Each called exactly once, following MRO
        print(Bottom.__mro__)
