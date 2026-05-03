# Partial Application

!!! tip "Mental Model"
    Partial application freezes some arguments of a function, producing a new function that needs fewer arguments. Think of it as pre-filling a form: you lock in the fields you already know, and the resulting simpler form only asks for what's left. The original function stays unchanged.

## functools.partial

### 1. Fix Arguments

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))  # 25
print(cube(5))    # 125
```

## Use Cases

### 1. Configure Functions

```python
from functools import partial

def greet(greeting, name):
    return f"{greeting}, {name}!"

say_hello = partial(greet, "Hello")
say_hi = partial(greet, "Hi")

print(say_hello("Alice"))  # Hello, Alice!
print(say_hi("Bob"))       # Hi, Bob!
```

### 2. Callbacks

```python
def log(level, message):
    print(f"[{level}] {message}")

info = partial(log, "INFO")
error = partial(log, "ERROR")

info("Starting")   # [INFO] Starting
error("Failed")    # [ERROR] Failed
```

## Summary

- Fix some arguments
- Create specialized functions
- Useful for callbacks
- Built-in with functools

---

## Exercises

**Exercise 1.**
Use `functools.partial` to create a `print_line` function from `print` that always ends with `"\n---"` (using the `end` parameter). Demonstrate by calling `print_line("Hello")` and `print_line("World")`.

??? success "Solution to Exercise 1"

        from functools import partial

        print_line = partial(print, end="\n---\n")

        print_line("Hello")
        print_line("World")

---

**Exercise 2.**
Write a `multiply(a, b)` function. Use `partial` to create `double` (multiplies by 2) and `triple` (multiplies by 3). Print the `func`, `args`, and `keywords` attributes of one of the partial objects to show how `partial` stores its configuration.

??? success "Solution to Exercise 2"

        from functools import partial

        def multiply(a, b):
            return a * b

        double = partial(multiply, 2)
        triple = partial(multiply, 3)

        print(double(5))   # 10
        print(triple(5))   # 15

        # Inspecting the partial object
        print(double.func)       # <function multiply at ...>
        print(double.args)       # (2,)
        print(double.keywords)   # {}

---

**Exercise 3.**
Create a list of partial functions that each add a different value (1 through 5) to their argument. Use a loop with `partial` to build the list, then apply all five functions to the number 10 and print the results. Explain why this avoids the late-binding closure bug that a lambda loop would cause.

??? success "Solution to Exercise 3"

        from functools import partial

        def add(a, b):
            return a + b

        adders = [partial(add, i) for i in range(1, 6)]

        results = [f(10) for f in adders]
        print(results)  # [11, 12, 13, 14, 15]

        # partial captures the value of i at creation time,
        # unlike a lambda which captures the variable by reference.
        # A lambda version would give [15, 15, 15, 15, 15] without
        # the default-argument fix.
