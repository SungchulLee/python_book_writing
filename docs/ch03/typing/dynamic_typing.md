# Dynamic Typing

!!! tip "Mental Model"
    In Python, variables do not have types -- objects do. A variable is just a name tag that can be moved from one object to another at any time. Type checking happens at runtime when an operation is attempted, not at compile time. This is why `x = 42` followed by `x = "hello"` is perfectly legal.

## Overview

### 1. No Type Declarations

```python
# No type needed
x = 42
x = "hello"  # Can change type
x = [1, 2, 3]  # Again
```

## Runtime Type Checking

### 1. Type Determined at Runtime

```python
def process(data):
    # Type checked when executed
    return data * 2

print(process(5))      # 10
print(process("hi"))   # "hihi"
```

## Duck Typing

### 1. If It Walks Like Duck

```python
class Duck:
    def quack(self):
        return "Quack!"

class Person:
    def quack(self):
        return "I'm quacking!"

def make_it_quack(thing):
    return thing.quack()

# Both work
print(make_it_quack(Duck()))
print(make_it_quack(Person()))
```

## Summary

- Types determined at runtime
- No explicit declarations
- Duck typing philosophy
- Flexible but needs care


---

## Exercises


**Exercise 1.**
Write a function `double(x)` that returns `x * 2`. Show that it works with an integer, a string, and a list, producing different behavior for each type.

??? success "Solution to Exercise 1"

    ```python
    def double(x):
        return x * 2

    print(double(5))         # 10
    print(double("hi"))      # hihi
    print(double([1, 2]))    # [1, 2, 1, 2]
    ```

    The `*` operator behaves differently depending on the type: arithmetic multiplication for numbers, repetition for strings and lists.

---

**Exercise 2.**
Create two classes, `Cat` and `Robot`, each with a `speak()` method. Write a function `make_speak(thing)` that calls `thing.speak()` without checking the type. Demonstrate duck typing.

??? success "Solution to Exercise 2"

    ```python
    class Cat:
        def speak(self):
            return "Meow!"

    class Robot:
        def speak(self):
            return "Beep boop!"

    def make_speak(thing):
        return thing.speak()

    print(make_speak(Cat()))    # Meow!
    print(make_speak(Robot()))  # Beep boop!
    ```

    `make_speak()` does not check the type of its argument. It only requires that the object has a `speak()` method. This is duck typing in action.

---

**Exercise 3.**
Show what happens when duck typing fails by calling `len()` on an integer. Catch the `TypeError` and print a meaningful error message.

??? success "Solution to Exercise 3"

    ```python
    try:
        result = len(42)
    except TypeError as e:
        print(f"TypeError: {e}")
        # TypeError: object of type 'int' has no len()
    ```

    Duck typing fails when the object does not support the required operation. Integers have no `__len__` method, so `len(42)` raises a `TypeError`.
