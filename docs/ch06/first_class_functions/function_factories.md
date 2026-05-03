# Function Factories

A function factory is a function that creates and returns another function. This pattern leverages closures to generate specialized functions dynamically.

!!! tip "Mental Model"
    A function factory is a template with blanks: you call it with configuration values, and it hands back a new function with those values baked in via a closure. Each call produces an independent function that remembers its own captured state, like stamping out custom tools from the same mold.

## Basic Pattern

A function factory returns an inner function that captures variables from the enclosing scope:

```python
def make_multiplier(n: int):  # returns a function: int -> int
    def multiply(x: int) -> int:
        return x * n
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

Each call to `make_multiplier` creates a new function with its own captured value of `n`.

## How Closures Work

The inner function `multiply` remembers the value of `n` even after `make_multiplier` has finished executing. This combination of a function and the variables it captures from its enclosing scope is called a **closure**.

```python
def make_adder(n: int):  # returns a function: int -> int
    def add(x: int) -> int:
        return x + n
    return add

add_10 = make_adder(10)
add_100 = make_adder(100)

print(add_10(5))    # 15
print(add_100(5))   # 105
```

`add_10` and `add_100` are independent closures — each holds its own copy of `n`.

## Practical Examples

### Validators

```python
def make_range_validator(min_val: float, max_val: float):  # returns a function: float -> bool
    def validate(x: float) -> bool:
        return min_val <= x <= max_val
    return validate

valid_percentage = make_range_validator(0, 100)
valid_age = make_range_validator(0, 150)

print(valid_percentage(50))   # True
print(valid_percentage(150))  # False
print(valid_age(25))          # True
```

### Greeting Functions

```python
def make_greeter(greeting: str):  # returns a function: str -> str
    def greet(name: str) -> str:
        return f"{greeting}, {name}!"
    return greet

say_hello = make_greeter("Hello")
say_hi = make_greeter("Hi")

print(say_hello("Alice"))  # Hello, Alice!
print(say_hi("Bob"))       # Hi, Bob!
```

### Formatters

```python
def make_formatter(prefix: str, suffix: str = ""):  # returns a function: value -> str
    def format_value(value) -> str:
        return f"{prefix}{value}{suffix}"
    return format_value

format_currency = make_formatter("\$", " USD")
format_percent = make_formatter("", "%")

print(format_currency(100))   # $100 USD
print(format_percent(85.5))   # 85.5%
```

### Power Functions

```python
def make_power(exp: int):  # returns a function: float -> float
    def power(base: float) -> float:
        return base ** exp
    return power

square = make_power(2)
cube = make_power(3)

print(square(4))  # 16
print(cube(4))    # 64
```

## Modifying Captured Variables with nonlocal

A closure can read captured variables freely, but to **modify** them it needs the `nonlocal` keyword. Without `nonlocal`, an assignment inside the inner function would create a new local variable instead of updating the captured one.

```python
def make_counter(start: int = 0, step: int = 1):  # returns a function: () -> int
    count = start
    def counter() -> int:
        nonlocal count
        current = count
        count += step
        return current
    return counter

counter = make_counter()
print(counter())  # 0
print(counter())  # 1
print(counter())  # 2

by_tens = make_counter(start=10, step=10)
print(by_tens())  # 10
print(by_tens())  # 20
```

## Late Binding in Loops

Creating closures inside a loop is a common source of bugs. Because closures capture variables **by reference** (not by value), all the closures share the same variable — and see its final value after the loop ends.

```python
# Bug: all functions capture the same variable i
funcs = []
for i in range(3):
    funcs.append(lambda x: x + i)

print(funcs[0](10))  # 12 (not 10!)
print(funcs[1](10))  # 12 (not 11!)

# Fix: capture the current value with a default parameter
funcs = []
for i in range(3):
    funcs.append(lambda x, i=i: x + i)

print(funcs[0](10))  # 10
print(funcs[1](10))  # 11
```

## Key Ideas

Function factories produce specialized functions from a common template. The inner function captures variables from the enclosing scope, forming a closure that remembers those values across calls. This is useful whenever you need a family of related functions that differ only in their configuration — validators, formatters, converters, and similar patterns.

When the inner function needs to *modify* a captured variable (not just read it), use `nonlocal`. When your factory grows complex enough to need multiple methods or shared mutable state, consider using a class instead.

For more on the decorator pattern — a close relative of function factories — see the decorators chapter.

---

## Exercises

**Exercise 1.**
Write a function factory `make_validator(min_val, max_val)` that returns a function accepting a single number and returning `True` if it is within the range `[min_val, max_val]`, or `False` otherwise. Create validators for percentages (0--100) and temperatures (-40--50) and test them.

??? success "Solution to Exercise 1"

        def make_validator(min_val, max_val):
            def validate(value):
                return min_val <= value <= max_val
            return validate

        is_percentage = make_validator(0, 100)
        is_temperature = make_validator(-40, 50)

        print(is_percentage(50))     # True
        print(is_percentage(150))    # False
        print(is_temperature(-30))   # True
        print(is_temperature(60))    # False

---

**Exercise 2.**
Create a `make_counter(start=0)` factory that returns a function. Each call to the returned function increments the counter by 1 and returns the new value. Use `nonlocal` to update the captured variable. Demonstrate that two counters created from the factory maintain independent state.

??? success "Solution to Exercise 2"

        def make_counter(start=0):
            count = start
            def counter():
                nonlocal count
                count += 1
                return count
            return counter

        counter_a = make_counter()
        counter_b = make_counter(10)

        print(counter_a())  # 1
        print(counter_a())  # 2
        print(counter_b())  # 11
        print(counter_b())  # 12
        print(counter_a())  # 3  (independent from counter_b)

---

**Exercise 3.**
Write a factory `make_formatter(template)` that accepts a format string with a single `{}` placeholder and returns a function that inserts its argument into the template. For example, `make_formatter("Hello, {}!")("Alice")` should return `"Hello, Alice!"`. Then demonstrate the late-binding pitfall by creating formatters in a loop and show how to fix it with a default argument.

??? success "Solution to Exercise 3"

        def make_formatter(template):
            def formatter(value):
                return template.format(value)
            return formatter

        hello = make_formatter("Hello, {}!")
        print(hello("Alice"))  # Hello, Alice!

        # Late-binding pitfall
        formatters_buggy = []
        for prefix in ["INFO", "WARN", "ERROR"]:
            formatters_buggy.append(lambda msg: f"[{prefix}] {msg}")

        # All use "ERROR" because prefix is captured by reference
        print(formatters_buggy[0]("test"))  # [ERROR] test  (bug!)

        # Fix with default argument
        formatters_fixed = []
        for prefix in ["INFO", "WARN", "ERROR"]:
            formatters_fixed.append(lambda msg, p=prefix: f"[{p}] {msg}")

        print(formatters_fixed[0]("test"))  # [INFO] test
        print(formatters_fixed[1]("test"))  # [WARN] test
        print(formatters_fixed[2]("test"))  # [ERROR] test
