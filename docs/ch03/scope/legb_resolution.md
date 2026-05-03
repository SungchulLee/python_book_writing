# LEGB Resolution

!!! tip "Mental Model"
    When Python encounters a name, it searches four scopes in order: Local, Enclosing, Global, Built-in -- the LEGB rule. The first match wins. Reading follows LEGB automatically, but writing always targets the local scope unless you explicitly declare `global` or `nonlocal`.

## Four Scopes

### 1. Local (L)

```python
def function():
    x = 10  # Local
```

### 2. Enclosing (E)

```python
def outer():
    x = 10  # Enclosing for inner
    def inner():
        print(x)
```

### 3. Global (G)

```python
x = 10  # Global

def function():
    print(x)
```

### 4. Built-in (B)

```python
# Always available
print(len([1, 2, 3]))
```

## Lookup Order

Searches: L → E → G → B


## Accessing Namespaces

### 1. `globals()`

Returns the global namespace dictionary:

```python
x = 42
print(globals()['x'])  # 42
```

### 2. `locals()`

Returns the local namespace dictionary:

```python
def f():
    a = 10
    b = 20
    print(locals())  # {'a': 10, 'b': 20}
```

### 3. `__builtins__`

Contains built-in names:

```python
import builtins
print(dir(builtins))  # ['abs', 'all', 'any', ...]
```

### 4. No `enclosings()` Function

There is no built-in to access enclosing scope directly. Enclosing variables are captured in closures via `__closure__`:

```python
def outer():
    x = 10
    def inner():
        return x
    return inner

f = outer()
print(f.__closure__[0].cell_contents)  # 10
```


## Namespace Summary

| Namespace | Access Method | Modifiable? |
|-----------|---------------|-------------|
| Local | `locals()` | No (snapshot) |
| Enclosing | `__closure__` | Via `nonlocal` |
| Global | `globals()` | Yes |
| Built-in | `builtins` module | Not recommended |


## Summary

- Four scope levels
- Specific lookup order
- First match wins

---

## Runnable Example: `legb_examples.py`

```python
#!/usr/bin/env python3
"""
LEGB Rule - Practical Examples
==============================

This file contains 15 practical examples demonstrating Python's LEGB rule.
Run this file to see all examples in action.

Usage: python 02_legb_examples.py
"""

if __name__ == "__main__":

    print("=" * 70)
    print("PYTHON LEGB RULE - 15 PRACTICAL EXAMPLES")
    print("=" * 70)
    print()

    # ============================================================================
    # EXAMPLE 1: Basic LEGB Demonstration
    # ============================================================================

    print("Example 1: Basic LEGB Demonstration")
    print("-" * 70)

    x = "Global X"  # Global scope

    def outer():
        x = "Enclosing X"  # Enclosing scope

        def inner():
            x = "Local X"  # Local scope
            print(f"Inside inner(): {x}")

        inner()
        print(f"Inside outer(): {x}")

    outer()
    print(f"In global scope: {x}")

    print("\nExplanation:")
    print("• Each scope has its own 'x' variable")
    print("• inner() uses Local x")
    print("• outer() uses Enclosing x")
    print("• Global scope uses Global x")
    print()

    # ============================================================================
    # EXAMPLE 2: Searching Up the Chain
    # ============================================================================

    print("=" * 70)
    print("Example 2: Searching Up the Chain")
    print("-" * 70)

    message = "Global message"

    def outer():
        # No 'message' in enclosing scope

        def inner():
            # No 'message' in local scope
            # Python searches: Local → Enclosing → Global (found!)
            print(f"Message: {message}")

        inner()

    outer()

    print("\nExplanation:")
    print("• inner() has no local 'message'")
    print("• outer() has no enclosing 'message'")
    print("• Python finds 'message' in global scope")
    print()

    # ============================================================================
    # EXAMPLE 3: Built-in Scope
    # ============================================================================

    print("=" * 70)
    print("Example 3: Built-in Scope")
    print("-" * 70)

    def use_builtins():
        # No local/enclosing/global definitions of these
        # Python uses built-in scope
        data = [1, 2, 3, 4, 5]
        print(f"Length: {len(data)}")  # Built-in len()
        print(f"Max: {max(data)}")     # Built-in max()
        print(f"Sum: {sum(data)}")     # Built-in sum()

    use_builtins()

    print("\nExplanation:")
    print("• len, max, sum are built-in functions")
    print("• Available everywhere without import")
    print("• Last resort in LEGB chain")
    print()

    # ============================================================================
    # EXAMPLE 4: Shadowing Variables
    # ============================================================================

    print("=" * 70)
    print("Example 4: Shadowing Variables (Not Recommended)")
    print("-" * 70)

    x = 100  # Global

    def func1():
        x = 200  # Shadows global (creates local)
        print(f"func1 - Local x: {x}")

    def func2():
        print(f"func2 - Global x: {x}")

    func1()
    func2()
    print(f"Global x unchanged: {x}")

    print("\nExplanation:")
    print("• func1 creates a local 'x' (shadows global)")
    print("• func2 reads the global 'x'")
    print("• Global x is never modified")
    print()

    # ============================================================================
    # EXAMPLE 5: Reading Global (No Keyword Needed)
    # ============================================================================

    print("=" * 70)
    print("Example 5: Reading Global Variables")
    print("-" * 70)

    PI = 3.14159
    APP_NAME = "MyApp"
    VERSION = "1.0"

    def show_constants():
        # Can read globals without 'global' keyword
        print(f"π = {PI}")
        print(f"App: {APP_NAME} v{VERSION}")

    show_constants()

    print("\nExplanation:")
    print("• Reading global variables requires no keyword")
    print("• Only assignment needs 'global' keyword")
    print()

    # ============================================================================
    # EXAMPLE 6: The global Keyword
    # ============================================================================

    print("=" * 70)
    print("Example 6: Using global Keyword")
    print("-" * 70)

    counter = 0  # Global

    def increment():
        global counter  # Tell Python to use global counter
        counter += 1
        print(f"Counter incremented to: {counter}")

    print(f"Initial counter: {counter}")
    increment()
    increment()
    increment()
    print(f"Final counter: {counter}")

    print("\nExplanation:")
    print("• 'global' keyword tells Python to use global variable")
    print("• Without 'global', would create local variable")
    print("• Allows function to modify global state")
    print()

    # ============================================================================
    # EXAMPLE 7: UnboundLocalError Example
    # ============================================================================

    print("=" * 70)
    print("Example 7: Common Mistake - UnboundLocalError")
    print("-" * 70)

    x = 10

    def problematic_function():
        try:
            print(x)  # Trying to read x
            x = 20    # But assignment makes x local!
        except UnboundLocalError as e:
            print(f"Error: {e}")
            print("Problem: x is treated as local because of assignment below")

    problematic_function()

    print("\nExplanation:")
    print("• Python sees 'x = 20' and makes x local")
    print("• Trying to print x before assignment fails")
    print("• Solution: Use 'global x' or rename variable")
    print()

    # ============================================================================
    # EXAMPLE 8: Multiple Enclosing Scopes
    # ============================================================================

    print("=" * 70)
    print("Example 8: Multiple Enclosing Scopes")
    print("-" * 70)

    def level1():
        x = "Level 1"
        print(f"Level 1: x = '{x}'")

        def level2():
            y = "Level 2"
            print(f"Level 2: y = '{y}', x = '{x}' (from level1)")

            def level3():
                z = "Level 3"
                print(f"Level 3: z = '{z}', y = '{y}' (from level2), x = '{x}' (from level1)")

            level3()

        level2()

    level1()

    print("\nExplanation:")
    print("• Inner functions can access all outer scopes")
    print("• Python searches each enclosing scope in order")
    print("• Can have multiple levels of nesting")
    print()

    # ============================================================================
    # EXAMPLE 9: The nonlocal Keyword
    # ============================================================================

    print("=" * 70)
    print("Example 9: Using nonlocal Keyword")
    print("-" * 70)

    def outer():
        count = 0  # Enclosing variable

        def increment():
            nonlocal count  # Access enclosing count
            count += 1
            return count

        print(f"Initial count: {count}")
        print(f"After 1st increment: {increment()}")
        print(f"After 2nd increment: {increment()}")
        print(f"After 3rd increment: {increment()}")
        print(f"Final count in outer: {count}")

    outer()

    print("\nExplanation:")
    print("• 'nonlocal' allows modifying enclosing scope")
    print("• Without 'nonlocal', would create local variable")
    print("• Only works with enclosing scope, not global")
    print()

    # ============================================================================
    # EXAMPLE 10: Closure Example
    # ============================================================================

    print("=" * 70)
    print("Example 10: Closures - Functions that Remember")
    print("-" * 70)

    def make_multiplier(n):
        def multiply(x):
            return x * n  # Captures 'n' from enclosing scope
        return multiply

    times_2 = make_multiplier(2)
    times_3 = make_multiplier(3)
    times_10 = make_multiplier(10)

    print(f"times_2(5) = {times_2(5)}")
    print(f"times_3(5) = {times_3(5)}")
    print(f"times_10(5) = {times_10(5)}")

    print("\nExplanation:")
    print("• Inner function 'multiply' captures 'n' from outer scope")
    print("• Each returned function remembers its own 'n'")
    print("• This is called a 'closure'")
    print()

    # ============================================================================
    # EXAMPLE 11: Namespace Inspection
    # ============================================================================

    print("=" * 70)
    print("Example 11: Inspecting Namespaces")
    print("-" * 70)

    global_var = "I'm global"

    def outer():
        enclosing_var = "I'm enclosing"

        def inner():
            local_var = "I'm local"
            print("Local namespace:", locals())
            print("\nGlobal namespace (first 5 items):")
            for key in list(globals().keys())[:5]:
                print(f"  {key}")

        inner()

    outer()

    print("\nExplanation:")
    print("• locals() returns current scope's variables")
    print("• globals() returns module-level variables")
    print("• Useful for debugging scope issues")
    print()

    # ============================================================================
    # EXAMPLE 12: Shadowing Built-ins (Bad Practice!)
    # ============================================================================

    print("=" * 70)
    print("Example 12: Shadowing Built-ins (Don't Do This!)")
    print("-" * 70)

    def bad_practice():
        # Shadowing built-in 'list'
        list = [1, 2, 3]  # Now 'list' is a variable, not the class
        print(f"My list: {list}")

        # Can't use list() constructor anymore!
        try:
            new_list = list("abc")  # Trying to convert string to list
        except TypeError as e:
            print(f"Error: {e}")
            print("Problem: 'list' now refers to [1,2,3], not list class")

    bad_practice()

    # After function, built-in 'list' works again
    print(f"\nOutside function, list('xyz') = {list('xyz')}")

    print("\nExplanation:")
    print("• Variable name 'list' shadows built-in 'list' class")
    print("• Always use different names to avoid this")
    print("• Good alternatives: items, values, data, etc.")
    print()

    # ============================================================================
    # EXAMPLE 13: global vs. nonlocal
    # ============================================================================

    print("=" * 70)
    print("Example 13: global vs. nonlocal")
    print("-" * 70)

    x = "I'm global"

    def outer():
        x = "I'm enclosing"

        def use_nonlocal():
            nonlocal x
            print(f"nonlocal sees: '{x}' (enclosing)")

        def use_global():
            global x
            print(f"global sees: '{x}' (global)")

        use_nonlocal()
        use_global()

    outer()

    print("\nExplanation:")
    print("• 'nonlocal' accesses enclosing scope")
    print("• 'global' accesses global scope")
    print("• Both skip local scope")
    print()

    # ============================================================================
    # EXAMPLE 14: Practical Closure - Counter Factory
    # ============================================================================

    print("=" * 70)
    print("Example 14: Practical Closure - Counter Factory")
    print("-" * 70)

    def make_counter(start=0, step=1):
        count = start

        def increment():
            nonlocal count
            count += step
            return count

        def decrement():
            nonlocal count
            count -= step
            return count

        def reset():
            nonlocal count
            count = start

        def get_value():
            return count

        return increment, decrement, reset, get_value

    # Create two independent counters
    inc1, dec1, reset1, get1 = make_counter(0, 1)
    inc2, dec2, reset2, get2 = make_counter(100, 10)

    print("Counter 1:")
    print(f"  Start: {get1()}")
    print(f"  +1: {inc1()}")
    print(f"  +1: {inc1()}")
    print(f"  -1: {dec1()}")

    print("\nCounter 2:")
    print(f"  Start: {get2()}")
    print(f"  +10: {inc2()}")
    print(f"  +10: {inc2()}")
    print(f"  -10: {dec2()}")

    print("\nExplanation:")
    print("• Each counter maintains its own state")
    print("• State is preserved across function calls")
    print("• Closures provide encapsulation")
    print()

    # ============================================================================
    # EXAMPLE 15: LEGB in Classes
    # ============================================================================

    print("=" * 70)
    print("Example 15: LEGB with Classes")
    print("-" * 70)

    class_var = "I'm a module variable"

    class MyClass:
        class_attr = "I'm a class attribute"

        def method(self):
            local_var = "I'm local to method"

            # Can access all scopes
            print(f"Local: {local_var}")
            print(f"Class attribute: {self.class_attr}")
            print(f"Module variable: {class_var}")
            print(f"Built-in: {len([1, 2, 3])}")

    obj = MyClass()
    obj.method()

    print("\nExplanation:")
    print("• Class methods have access to all scopes")
    print("• self.attr accesses instance/class attributes")
    print("• LEGB still applies for regular variables")
    print()

    # ============================================================================
    # SUMMARY
    # ============================================================================

    print("=" * 70)
    print("SUMMARY - LEGB RULE")
    print("=" * 70)
    print("""
    Key Takeaways:

    1. Search Order: Local → Enclosing → Global → Built-in

    2. Reading is easy: Can read outer scopes automatically

    3. Writing requires keywords:
       • global: For modifying global variables
       • nonlocal: For modifying enclosing variables

    4. Shadowing: Inner scope can hide outer scope names

    5. Closures: Inner functions can capture outer variables

    6. Best Practice: Minimize global/nonlocal usage, prefer parameters

    Remember: When Python can't find a name in any scope, you get NameError!
    """)

    print("=" * 70)
    print("Next: Practice with exercises in 03_legb_exercises.py")
    print("=" * 70)
```


---

## Exercises


**Exercise 1.**
Write a nested function example that demonstrates all four LEGB scopes. Define a variable with the same name at each level and print which value is seen from the innermost function.

??? success "Solution to Exercise 1"

    ```python
    x = "global"

    def outer():
        x = "enclosing"

        def inner():
            x = "local"
            print(f"inner sees: {x}")  # local

        inner()
        print(f"outer sees: {x}")  # enclosing

    outer()
    print(f"module sees: {x}")  # global
    print(f"built-in example: {len([1,2,3])}")  # 3 (built-in)
    ```

    Python searches Local first, then Enclosing, then Global, then Built-in. The first match wins.

---

**Exercise 2.**
Use `locals()` and `globals()` inside a function to inspect the available namespaces. Define some local variables and print both dictionaries to see the difference.

??? success "Solution to Exercise 2"

    ```python
    module_var = "I am global"

    def example():
        local_var = "I am local"
        another = 42
        print("Locals:", locals())
        print("Globals contain 'module_var':", 'module_var' in globals())

    example()
    ```

    `locals()` returns a snapshot of the local namespace. `globals()` returns the module-level namespace dictionary, which can be modified directly.

---

**Exercise 3.**
Create a closure where the inner function captures a variable from the enclosing scope. After calling the outer function, use `__closure__` to inspect the captured value.

??? success "Solution to Exercise 3"

    ```python
    def outer(value):
        def inner():
            return value
        return inner

    closure = outer(42)
    print(closure())  # 42
    print(closure.__closure__[0].cell_contents)  # 42
    ```

    The inner function captures `value` from the enclosing scope. The `__closure__` attribute contains cell objects holding the captured values.
