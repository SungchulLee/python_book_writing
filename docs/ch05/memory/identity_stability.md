# Identity Stability

!!! tip "Mental Model"
    An object's identity (`id()`) is its fixed address in memory -- like a house number that never changes as long as the house exists. Mutating the contents (repainting walls) keeps the same address, but reassigning the variable (moving to a new house) gives you a different address. This is why `is` checks identity while `==` checks content.

## Object Identity

### 1. Constant ID

```python
x = [1, 2, 3]
original_id = id(x)

# Modify object
x.append(4)
x.extend([5, 6])
x[0] = 100

# ID unchanged
print(id(x) == original_id)  # True
```

### 2. New Object

```python
x = [1, 2, 3]
original_id = id(x)

# Create new object
x = [1, 2, 3]

# Different ID
print(id(x) != original_id)  # True
```

## Mutation

### 1. Preserves Identity

```python
lst = [1, 2, 3]
id1 = id(lst)

# All preserve identity
lst.append(4)
lst.extend([5, 6])
lst.insert(0, 0)
lst.remove(2)
lst.pop()
lst.sort()
lst.reverse()

print(id(lst) == id1)  # True
```

### 2. Immutables

```python
x = "hello"
id1 = id(x)

# Must create new
x = x + " world"

print(id(x) != id1)  # True
```

## References

### 1. Shared Identity

```python
a = [1, 2, 3]
b = a
c = a

# All same ID
print(id(a) == id(b) == id(c))  # True
```

### 2. Independent IDs

```python
a = [1, 2, 3]
b = [1, 2, 3]

# Different IDs
print(id(a) != id(b))  # True
```

## Guarantees

### 1. Language Level

```python
# Guaranteed: identity stable
x = [1, 2, 3]
x.append(4)
# Same object

# Guaranteed: mutation visible
y = x
x.append(5)
# y sees change
```

## Summary

### 1. Identity

- Unique per object
- Never changes
- Check with `is`

### 2. Operations

- Mutation: same ID
- Assignment: new ID
- Immutables: always new

---


## Runnable Example: `immutable_types.py`

```python
"""
02_beginner_immutable_types.py

TOPIC: Immutable Types and Memory Behavior
LEVEL: Beginner
DURATION: 45-60 minutes

LEARNING OBJECTIVES:
1. Understand what immutability means in Python
2. Learn which types are immutable (int, float, str, tuple, frozenset, bytes)
3. Explore how immutable types behave with assignment and modification
4. Understand why immutability matters for memory and performance
5. Learn about string interning and integer caching

KEY CONCEPTS:
- Immutable objects cannot be changed after creation
- "Modification" creates new objects
- Immutable types: int, float, str, tuple, bool, frozenset, bytes, None
- String interning for memory optimization
- Integer caching for small integers (-5 to 256)
"""

# ============================================================================
# SECTION 1: What is Immutability?
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("SECTION 1: Understanding Immutability")
    print("=" * 70)

    # IMMUTABLE means "cannot be changed"
    # Once an immutable object is created, its VALUE cannot be modified
    # Any "modification" creates a NEW object

    # Let's demonstrate with integers:
    x = 10
    print(f"Initial: x = {x}, id(x) = {id(x)}")

    # What happens when we "change" x?
    original_id = id(x)
    x = x + 5  # This looks like modification, but...

    print(f"After x = x + 5: x = {x}, id(x) = {id(x)}")
    print(f"Did the object change? {original_id == id(x)}")
    print(f"No! A NEW object was created and x now references it.")

    # MEMORY MODEL:
    # BEFORE x = x + 5:         AFTER x = x + 5:
    # STACK     HEAP            STACK     HEAP
    # ┌───┐    ┌──────┐       ┌───┐    ┌──────┐
    # │ x─┼───>│  10  │       │ x─┼───>│  15  │  (new object)
    # └───┘    └──────┘       └───┘    └──────┘
    #                                   ┌──────┐
    #                                   │  10  │  (old object, may be GC'd)
    #                                   └──────┘

    # ============================================================================
    # SECTION 2: Common Immutable Types in Python
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 2: Immutable Types in Python")
    print("=" * 70)

    # Python's immutable built-in types:
    immutable_examples = {
        "int": 42,
        "float": 3.14,
        "str": "Hello",
        "tuple": (1, 2, 3),
        "bool": True,
        "frozenset": frozenset([1, 2, 3]),
        "bytes": b"hello",
        "NoneType": None,
    }

    print("\nDemonstrating immutable types:")
    for type_name, value in immutable_examples.items():
        print(f"  {type_name:12} : {value} (type: {type(value).__name__})")

    # ============================================================================
    # SECTION 3: Integers and Immutability
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 3: Integer Immutability")
    print("=" * 70)

    # Integers are immutable - you cannot change an integer object's value
    a = 100
    b = a  # b references the same object as a

    print(f"Initially:")
    print(f"  a = {a}, id(a) = {id(a)}")
    print(f"  b = {b}, id(b) = {id(b)}")
    print(f"  a is b: {a is b}")

    # Now "modify" a
    a = a + 1

    print(f"\nAfter a = a + 1:")
    print(f"  a = {a}, id(a) = {id(a)}")
    print(f"  b = {b}, id(b) = {id(b)}")
    print(f"  a is b: {a is b}")

    # Key insight: b is unchanged! a now references a different object
    # This is different from mutable types (we'll see this in the next file)

    # ============================================================================
    # SECTION 4: Integer Caching (Optimization)
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 4: Integer Caching (-5 to 256)")
    print("=" * 70)

    # Python pre-creates and caches integer objects from -5 to 256
    # This is a performance optimization for commonly used integers

    # Cached integers (same object):
    x1 = 100
    x2 = 100
    print(f"Cached integers:")
    print(f"  x1 = {x1}, id(x1) = {id(x1)}")
    print(f"  x2 = {x2}, id(x2) = {id(x2)}")
    print(f"  x1 is x2: {x1 is x2}")  # True! Same object

    # Non-cached integers (different objects, usually):
    y1 = 1000
    y2 = 1000
    print(f"\nNon-cached integers:")
    print(f"  y1 = {y1}, id(y1) = {id(y1)}")
    print(f"  y2 = {y2}, id(y2) = {id(y2)}")
    print(f"  y1 is y2: {y1 is y2}")  # May be False (implementation dependent)

    # WHY DOES THIS MATTER?
    # - Memory efficiency: Small integers are shared
    # - Performance: No need to allocate new objects repeatedly
    # - BUT: Never rely on 'is' for numeric comparisons - always use '=='

    print("\nIMPORTANT: Always use == for value comparison, not 'is'")
    print(f"  y1 == y2: {y1 == y2}")  # Always True if values are equal

    # ============================================================================
    # SECTION 5: Strings and Immutability
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 5: String Immutability")
    print("=" * 70)

    # Strings are immutable sequences of characters
    s = "Hello"
    print(f"Original string: s = '{s}', id(s) = {id(s)}")

    # Attempt to "modify" the string
    original_id = id(s)
    s = s + " World"  # Concatenation creates a NEW string object

    print(f"After concatenation: s = '{s}', id(s) = {id(s)}")
    print(f"Same object? {original_id == id(s)}")

    # String "methods" that seem to modify actually return new strings:
    text = "python"
    print(f"\nOriginal: text = '{text}', id = {id(text)}")

    upper_text = text.upper()
    print(f"text.upper() = '{upper_text}', id = {id(upper_text)}")
    print(f"Original text unchanged: '{text}', id = {id(text)}")

    # IMPORTANT: Strings cannot be modified in place
    # This won't work: text[0] = 'P'  # TypeError: 'str' object does not support item assignment

    # ============================================================================
    # SECTION 6: String Interning (Optimization)
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 6: String Interning")
    print("=" * 70)

    # Python "interns" some strings to save memory
    # Interning means reusing the same string object for identical values

    # Automatically interned: identifiers and short strings
    s1 = "hello"
    s2 = "hello"
    print(f"Short strings:")
    print(f"  s1 = '{s1}', id = {id(s1)}")
    print(f"  s2 = '{s2}', id = {id(s2)}")
    print(f"  s1 is s2: {s1 is s2}")  # Often True

    # Strings with spaces or special characters may not be interned:
    s3 = "hello world"
    s4 = "hello world"
    print(f"\nStrings with spaces:")
    print(f"  s3 = '{s3}', id = {id(s3)}")
    print(f"  s4 = '{s4}', id = {id(s4)}")
    print(f"  s3 is s4: {s3 is s4}")  # May be True or False

    # Explicit interning using sys.intern():
    import sys
    s5 = sys.intern("hello world")
    s6 = sys.intern("hello world")
    print(f"\nExplicitly interned strings:")
    print(f"  s5 = '{s5}', id = {id(s5)}")
    print(f"  s6 = '{s6}', id = {id(s6)}")
    print(f"  s5 is s6: {s5 is s6}")  # Always True

    # WHY STRING INTERNING MATTERS:
    # - Memory savings when you have many identical strings
    # - Faster string comparison (identity check instead of character comparison)
    # - Useful for dictionary keys and identifiers

    # ============================================================================
    # SECTION 7: Tuples and Immutability
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 7: Tuple Immutability")
    print("=" * 70)

    # Tuples are immutable sequences
    t = (1, 2, 3)
    print(f"Original tuple: t = {t}, id = {id(t)}")

    # Cannot modify tuple elements:
    # t[0] = 10  # TypeError: 'tuple' object does not support item assignment

    # "Modifying" a tuple creates a new one:
    original_id = id(t)
    t = t + (4, 5)
    print(f"After concatenation: t = {t}, id = {id(t)}")
    print(f"Same object? {original_id == id(t)}")

    # ============================================================================
    # SECTION 8: Nested Immutability - Important Gotcha!
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 8: Tuples with Mutable Elements (GOTCHA!)")
    print("=" * 70)

    # IMPORTANT: A tuple itself is immutable, but it can contain mutable objects!
    tuple_with_list = (1, 2, [3, 4])
    print(f"Tuple with list: {tuple_with_list}")
    print(f"  Tuple id: {id(tuple_with_list)}")
    print(f"  List id: {id(tuple_with_list[2])}")

    # We CANNOT change which objects the tuple references:
    # tuple_with_list[2] = [5, 6]  # TypeError

    # BUT we CAN modify the mutable object (list) inside the tuple:
    tuple_with_list[2].append(5)
    print(f"\nAfter modifying the list inside:")
    print(f"  Tuple: {tuple_with_list}")
    print(f"  Tuple id: {id(tuple_with_list)} (unchanged)")
    print(f"  List id: {id(tuple_with_list[2])} (unchanged)")

    # MEMORY MODEL:
    # The tuple still references the same list object
    # The list object's contents changed, but the list object itself is the same
    #
    # ┌─────────────────┐
    # │  Tuple (1,2,L)  │ (immutable - references can't change)
    # └────────┬────────┘
    #          │ 
    #          ├──> int: 1
    #          ├──> int: 2
    #          └──> ┌───────────┐
    #               │ List [3,4,5]│ (mutable - contents can change)
    #               └───────────┘

    # ============================================================================
    # SECTION 9: Immutability and Function Parameters
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 9: Immutability in Functions")
    print("=" * 70)

    def try_to_modify_int(x):
        """
        This function tries to modify an integer parameter
        """
        print(f"  Inside function before: x = {x}, id = {id(x)}")
        x = x + 10  # This creates a new object and rebinds local x
        print(f"  Inside function after: x = {x}, id = {id(x)}")
        return x

    def try_to_modify_string(s):
        """
        This function tries to modify a string parameter
        """
        print(f"  Inside function before: s = '{s}', id = {id(s)}")
        s = s + " World"  # Creates new string, rebinds local s
        print(f"  Inside function after: s = '{s}', id = {id(s)}")
        return s

    # Test with integer
    num = 5
    print(f"Before function call: num = {num}, id = {id(num)}")
    result = try_to_modify_int(num)
    print(f"After function call: num = {num}, id = {id(num)}")
    print(f"Returned value: result = {result}")

    print()

    # Test with string
    text = "Hello"
    print(f"Before function call: text = '{text}', id = {id(text)}")
    result = try_to_modify_string(text)
    print(f"After function call: text = '{text}', id = {id(text)}")
    print(f"Returned value: result = '{result}'")

    # KEY INSIGHT: Immutable objects passed to functions cannot be modified
    # by the function. The function can only create new objects.

    # ============================================================================
    # SECTION 10: Why Immutability Matters
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 10: Benefits of Immutability")
    print("=" * 70)

    print("""
    WHY IMMUTABILITY IS IMPORTANT:

    1. THREAD SAFETY
       - Immutable objects can be safely shared between threads
       - No risk of concurrent modification issues

    2. HASHABILITY
       - Immutable objects can be used as dictionary keys
       - Immutable objects can be added to sets
       - Hash values remain constant

    3. PREDICTABILITY
       - Functions can't unexpectedly modify immutable arguments
       - Easier to reason about code behavior

    4. MEMORY OPTIMIZATION
       - Python can reuse immutable objects (caching, interning)
       - Reduces memory allocation overhead

    5. SECURITY
       - Prevents accidental modification of important data
       - Safer for use as constants or configuration values
    """)

    # Demonstrating hashability:
    # Immutable objects can be dictionary keys
    immutable_key = (1, 2, 3)  # Tuple
    my_dict = {immutable_key: "value"}
    print(f"Dictionary with tuple key: {my_dict}")

    # Mutable objects cannot be dictionary keys:
    # mutable_key = [1, 2, 3]  # List
    # my_dict = {mutable_key: "value"}  # TypeError: unhashable type: 'list'

    # ============================================================================
    # SECTION 11: Performance Implications
    # ============================================================================

    print("\n" + "=" * 70)
    print("SECTION 11: Performance Considerations")
    print("=" * 70)

    import time

    # String concatenation creates many intermediate objects
    # This is inefficient for large-scale operations
    def inefficient_string_building():
        result = ""
        for i in range(1000):
            result = result + str(i)  # Creates new string each iteration!
        return result

    # Better approach: use join() which creates only one final string
    def efficient_string_building():
        parts = []
        for i in range(1000):
            parts.append(str(i))
        return "".join(parts)

    # Measure performance
    start = time.time()
    s1 = inefficient_string_building()
    time1 = time.time() - start

    start = time.time()
    s2 = efficient_string_building()
    time2 = time.time() - start

    print(f"Inefficient string concatenation: {time1:.4f} seconds")
    print(f"Efficient join method: {time2:.4f} seconds")
    print(f"Speedup: {time1/time2:.2f}x faster")

    # ============================================================================
    # SECTION 12: Key Takeaways
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    print("""
    1. Immutable types: int, float, str, tuple, bool, frozenset, bytes, None
    2. Immutable objects cannot be changed; "modification" creates new objects
    3. Python optimizes memory by caching small integers (-5 to 256)
    4. Python interns some strings to save memory
    5. Immutable objects are thread-safe and hashable (can be dict keys)
    6. Tuples are immutable, but can contain mutable objects
    7. Function parameters that are immutable cannot be modified by the function
    8. String concatenation in loops is inefficient; use join() instead
    9. Use == for value comparison, not 'is' (identity comparison)
    10. Understanding immutability is crucial for writing correct Python code
    """)

    # ============================================================================
    # PRACTICE EXERCISES
    # ============================================================================

    print("\n" + "=" * 70)
    print("PRACTICE EXERCISES")
    print("=" * 70)

    print("""
    Try these exercises to reinforce your understanding:

    1. Create a function that tries to modify a tuple parameter. What happens?

    2. Investigate integer caching by checking 'is' for various integer values.
       Find the exact range where caching occurs.

    3. Create a tuple containing a list. Try to modify the list. What happens
       to the tuple's id?

    4. Write two functions to concatenate 10,000 strings: one using += and
       one using join(). Compare their performance.

    5. Explain why immutable objects can be dictionary keys but mutable objects
       cannot. Create examples demonstrating this.

    6. Investigate string interning with various strings (with/without spaces,
       special characters, etc.). When does interning occur?

    See exercises_01_beginner.py for complete practice problems!
    """)
```


## Exercises

**Exercise 1.**
Write a script that starts with a list `lst = [3, 1, 4, 1, 5]` and applies every mutating method (append, extend, insert, remove, pop, sort, reverse) in sequence. After each operation, assert that `id(lst)` has not changed. Print the list after each step and the final confirmation message.

??? success "Solution to Exercise 1"
        ```python
        lst = [3, 1, 4, 1, 5]
        original_id = id(lst)

        lst.append(9)
        print(f"After append:  {lst}")
        assert id(lst) == original_id

        lst.extend([2, 6])
        print(f"After extend:  {lst}")
        assert id(lst) == original_id

        lst.insert(0, 0)
        print(f"After insert:  {lst}")
        assert id(lst) == original_id

        lst.remove(1)
        print(f"After remove:  {lst}")
        assert id(lst) == original_id

        lst.pop()
        print(f"After pop:     {lst}")
        assert id(lst) == original_id

        lst.sort()
        print(f"After sort:    {lst}")
        assert id(lst) == original_id

        lst.reverse()
        print(f"After reverse: {lst}")
        assert id(lst) == original_id

        print("\nAll mutations preserved identity!")
        ```

---

**Exercise 2.**
Demonstrate identity instability with strings: create a string `s`, record its `id`, then perform concatenation (`s = s + " world"`), a method call (`s = s.upper()`), and an f-string rebuild (`s = f"{s}!"`). Print the `id` after each step and count how many new objects were created.

??? success "Solution to Exercise 2"
        ```python
        s = "hello"
        ids = [id(s)]

        s = s + " world"
        ids.append(id(s))

        s = s.upper()
        ids.append(id(s))

        s = f"{s}!"
        ids.append(id(s))

        new_objects = sum(1 for i in range(1, len(ids))
                         if ids[i] != ids[i - 1])

        for i, addr in enumerate(ids):
            label = ["initial", "concat", "upper", "f-string"][i]
            print(f"  {label:>10}: id = {addr}")

        print(f"\nNew objects created: {new_objects}")
        ```

---

**Exercise 3.**
Write a function `track_identity(obj, operations)` that takes a mutable object and a list of callables. For each callable, it applies the operation to the object and records whether the `id` changed. Return a list of booleans indicating identity stability for each operation. Test it with a dictionary and operations like `update`, `pop`, `clear`, and reassignment.

??? success "Solution to Exercise 3"
        ```python
        def track_identity(obj, operations):
            results = []
            for op in operations:
                old_id = id(obj)
                obj = op(obj)
                results.append(id(obj) == old_id)
            return results

        d = {"a": 1, "b": 2, "c": 3}

        ops = [
            lambda d: (d.update({"d": 4}), d)[1],   # update (mutates)
            lambda d: (d.pop("a"), d)[1],             # pop (mutates)
            lambda d: (d.clear(), d)[1],              # clear (mutates)
            lambda d: {"x": 99},                      # reassignment (new obj)
        ]

        labels = ["update", "pop", "clear", "reassign"]
        results = track_identity(d, ops)

        for label, stable in zip(labels, results):
            print(f"  {label:>10}: identity stable = {stable}")
        ```

---
