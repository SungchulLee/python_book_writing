# Dynamic vs Static

Programming languages differ fundamentally in when they check types. Statically typed languages like Java and C++ verify types at compile time and require every attribute to be declared before use. Python, by contrast, is dynamically typed: objects can receive new attributes at any point during execution without prior declaration. Python is also **strongly typed**, meaning it does not silently coerce between unrelated types — for example, `"3" + 5` raises a `TypeError` rather than guessing what the programmer intended. This flexibility is a core part of Python's design, but it requires discipline to avoid runtime errors from typos or unexpected attribute additions.

!!! tip "Mental Model"
    Static typing is a pre-flight checklist -- the compiler verifies everything before takeoff. Dynamic typing is an in-flight adjustment -- Python figures out types as the code runs. Python is dynamically typed but strongly typed: you can attach any attribute at any time, but `"3" + 5` is still a `TypeError`. The freedom is in *when* types are checked, not in *whether* they are enforced.

## Dynamic Typing

### 1. Python

In a dynamically typed language like Python, you can add attributes to an object at any time. There is no requirement to declare them in the class body or in `__init__` — the interpreter simply creates the attribute when you assign to it.

```python
class Dog:
    pass

# Can add attributes anytime
dog = Dog()
dog.name = "Rex"  # OK
dog.age = 5       # OK
```

### 2. Duck Typing

Python's dynamic type system embraces **duck typing**: "if it walks like a duck and quacks like a duck, it's a duck." Instead of checking an object's declared type, Python code simply calls the methods or accesses the attributes it needs. If the object provides them, it works — regardless of its class.

```python
class Duck:
    def quack(self):
        return "Quack!"

class Person:
    def quack(self):
        return "I can quack too!"

def make_it_quack(thing):
    # No type check — just call the method
    print(thing.quack())

make_it_quack(Duck())    # Quack!
make_it_quack(Person())  # I can quack too!
```

Duck typing is one of the most powerful consequences of dynamic typing. The function `make_it_quack` never inspects the type of `thing` — it only cares that the object has a `quack` method. This makes code naturally polymorphic without requiring inheritance hierarchies or shared interfaces.

!!! info "Duck Typing vs Explicit Type Checks"

    Idiomatic Python avoids `isinstance()` checks when duck typing suffices. Checking types explicitly couples your code to specific classes, while duck typing keeps it open to any object that satisfies the required interface. The `collections.abc` module and `typing.Protocol` formalize duck typing for static analysis.

## Static Typing

### 1. Other Languages

In statically typed languages, all attributes must be declared in the class definition. The compiler checks every attribute access at compile time and rejects any reference to an undeclared field.

```java
// Java - static
class Dog {
    String name;  // Must declare
}
```

Attempting to assign `dog.age` without declaring `age` in the class would cause a compilation error in Java, whereas Python would silently create the attribute.

!!! note "The Static–Dynamic Spectrum"

    The divide between static and dynamic typing is a **spectrum**, not a binary. Many "static" languages support dynamic features: Java has reflection, Kotlin and Rust have type inference that reduces annotation burden, and TypeScript offers gradual typing where you can opt in or out file by file. Conversely, Python's type hints bring static-analysis capabilities into a dynamic language. When comparing languages, think in terms of **how much** type information is checked at compile time versus runtime, rather than placing each language into a rigid category.

## Type Hints

### 1. Optional

Python introduced type hints as an optional middle ground between full dynamic freedom and static enforcement. You can annotate parameter and attribute types for documentation and for use with static analysis tools like mypy, without sacrificing Python's runtime flexibility.

```python
class Dog:
    def __init__(self, name: str):
        self.name: str = name

# Type hints are not enforced at runtime
```

Type hints make code more readable and allow tools to catch type errors before the program runs, but the Python interpreter itself does not enforce them.

### 2. Static Analysis with mypy

While Python ignores type hints at runtime, **mypy** is a static analysis tool that reads your annotations and catches type errors before you run the program — giving you compile-time-like safety in a dynamic language.

```python
# mypy catches this at analysis time
def greet(name: str) -> str:
    return "Hello, " + name

greet(42)  # mypy error: Argument 1 has incompatible type "int"; expected "str"
```

Running `mypy your_file.py` reports the error without executing any code. This bridges the gap between dynamic flexibility and static safety: you write Python as usual, but mypy acts as a compile-time checker for the portions of code you have annotated.

```bash
$ mypy your_file.py
your_file.py:5: error: Argument 1 to "greet" has incompatible type "int"; expected "str"
```

### 3. Managing Dynamic Typing Safely

Dynamic typing gives you freedom, but freedom without discipline leads to bugs that only appear at runtime. The Python ecosystem provides several tools and patterns to manage this tradeoff.

!!! tip "Practical Tools for Taming Dynamic Typing"

    - **Use type hints consistently.** Annotate function signatures, return types, and important variables. Even partial coverage helps readers and tools understand your intent.
    - **Run mypy in CI.** Integrate `mypy --strict` into your continuous integration pipeline so type errors are caught before code is merged.
    - **Prefer `dataclasses` or `pydantic` for structured data.** These enforce a fixed set of fields with declared types, preventing silent attribute creation and providing validation.
    - **Use `__slots__` when attribute sets are fixed.** This prevents accidental attribute creation via typos and reduces memory usage.
    - **Leverage linters.** Tools like `pylint` and `pyright` catch common mistakes, enforce coding standards, and complement type checking.

## Connection to the Attribute System

Dynamic typing is not an abstract philosophy — it is a direct consequence of how Python resolves attributes at runtime:

```
obj.attr  →  type(obj).__getattribute__(obj, "attr")
              →  descriptors / instance __dict__ / __getattr__
```

Because this resolution happens at runtime (not compile time), you can add attributes on the fly, swap methods, and use objects based on behavior rather than type. The built-in functions [`getattr`/`setattr`/`delattr`](builtin_attr_functions.md) provide programmatic access to this same mechanism. Everything you learned about [attribute lookup](../object_model/attribute_lookup.md) and [descriptors](../object_model/attribute_lookup.md) is the machinery that makes dynamic typing work.

## Summary

- Python is **dynamically typed** (types are checked at runtime) and **strongly typed** (no silent coercion between unrelated types like `str + int`).
- Python embraces **duck typing**: objects are used based on the methods and attributes they provide, not their declared type.
- Statically typed languages require all attributes to be declared in advance and enforce this at compile time, but the static-vs-dynamic divide is a **spectrum** — many static languages support reflection, type inference, or gradual typing.
- **Type hints** provide an optional way to document expected types and enable static analysis without changing Python's dynamic runtime behavior.
- **mypy** and similar tools bring compile-time-like checking to Python by analyzing type annotations before runtime.
- Dynamic typing offers flexibility but demands careful discipline. Tools like `dataclasses`, `pydantic`, `__slots__`, and linters help manage the tradeoff between freedom and safety.

---

## Exercises

**Exercise 1.**
Create a class `Point` without type hints. Show that you can add arbitrary attributes (like `color`, `label`) at runtime. Then create a `TypedPoint` with type hints and `__slots__`. Show the difference: `TypedPoint` prevents dynamic attribute addition while `Point` allows it.

??? success "Solution to Exercise 1"

        class Point:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        p = Point(1, 2)
        p.color = "red"   # Dynamic — works fine
        p.label = "A"     # Also fine
        print(vars(p))    # {'x': 1, 'y': 2, 'color': 'red', 'label': 'A'}

        class TypedPoint:
            __slots__ = ('x', 'y')

            def __init__(self, x: float, y: float):
                self.x = x
                self.y = y

        tp = TypedPoint(1, 2)
        try:
            tp.color = "red"
        except AttributeError as e:
            print(f"Error: {e}")
            # Error: 'TypedPoint' object has no attribute 'color'

---

**Exercise 2.**
Write a function that takes an object and a list of expected attribute names. It should check whether the object has all expected attributes using `hasattr()` and return a report dictionary mapping each name to `True`/`False`. Demonstrate with a duck-typing scenario where two different classes satisfy the same interface check.

??? success "Solution to Exercise 2"

        def check_interface(obj, expected):
            return {name: hasattr(obj, name) for name in expected}

        class Duck:
            def quack(self):
                return "Quack!"
            def swim(self):
                return "Swimming"

        class Person:
            def quack(self):
                return "I'm quacking!"
            def swim(self):
                return "I'm swimming!"

        expected = ["quack", "swim", "fly"]
        print(check_interface(Duck(), expected))
        # {'quack': True, 'swim': True, 'fly': False}
        print(check_interface(Person(), expected))
        # {'quack': True, 'swim': True, 'fly': False}

---

**Exercise 3.**
Demonstrate the "typo bug" problem in dynamic typing: create a class `Account` with a `balance` attribute. Accidentally write `self.balence = 100` (typo). Show that Python silently creates a new attribute. Then show how `__slots__` prevents this problem by raising `AttributeError` on the typo.

??? success "Solution to Exercise 3"

        # Dynamic typing — typo creates silent bug
        class Account:
            def __init__(self, balance):
                self.balance = balance

        acc = Account(1000)
        acc.balence = 500  # Typo! Creates new attribute silently
        print(acc.balance)   # 1000 — original unchanged
        print(acc.balence)   # 500 — typo attribute

        # Slots prevent this
        class SafeAccount:
            __slots__ = ('balance',)

            def __init__(self, balance):
                self.balance = balance

        safe = SafeAccount(1000)
        try:
            safe.balence = 500  # Typo caught!
        except AttributeError as e:
            print(f"Caught typo: {e}")
