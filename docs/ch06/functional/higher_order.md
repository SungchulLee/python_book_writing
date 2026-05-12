# Higher-Order Functions

!!! tip "Mental Model"
    A higher-order function treats other functions as data -- it either accepts a function as an argument, returns a function, or both. This is the gateway to functional programming: once functions can flow in and out of other functions, you can build powerful abstractions like `map`, `filter`, decorators, and pipelines.

## Definition

Functions that:

1. Take functions as arguments
2. Return functions

## Take Functions

### 1. Apply Function

```python
def apply_twice(func, value):
    return func(func(value))

def add_one(x):
    return x + 1

print(apply_twice(add_one, 5))  # 7
```

## Return Functions

### 1. Function Factory

```python
def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

## Built-in Examples

### 1. map, filter

```python
# map takes function
squared = map(lambda x: x**2, [1, 2, 3])

# filter takes function
evens = filter(lambda x: x % 2 == 0, range(10))
```

## Summary

- Take functions as args
- Return functions
- Enable abstraction
- Powerful pattern

---

## Exercises

**Exercise 1.**
Write a higher-order function `apply_n(func, value, n)` that applies `func` to `value` exactly `n` times. For example, `apply_n(lambda x: x + 1, 0, 5)` returns `5`. Test with several functions and counts.

??? success "Solution to Exercise 1"

        def apply_n(func, value, n):
            for _ in range(n):
                value = func(value)
            return value

        print(apply_n(lambda x: x + 1, 0, 5))     # 5
        print(apply_n(lambda x: x * 2, 1, 10))     # 1024
        print(apply_n(str.upper, "hello", 1))       # HELLO

---

**Exercise 2.**
Write a higher-order function `make_repeater(func, n)` that returns a new function. The returned function takes a value and applies `func` to it `n` times. For example, `doubler = make_repeater(lambda x: x * 2, 3)` creates a function that doubles three times, so `doubler(5)` returns `40`.

??? success "Solution to Exercise 2"

        def make_repeater(func, n):
            def repeated(value):
                for _ in range(n):
                    value = func(value)
                return value
            return repeated

        doubler = make_repeater(lambda x: x * 2, 3)
        print(doubler(5))   # 40
        print(doubler(1))   # 8

        increment_5 = make_repeater(lambda x: x + 1, 5)
        print(increment_5(0))  # 5

---

**Exercise 3.**
Write a higher-order function `compose(f, g)` that returns a new function representing the composition `f(g(x))`. Then use `compose` to build a pipeline that first squares a number and then adds 10. Verify with several inputs.

??? success "Solution to Exercise 3"

        def compose(f, g):
            def composed(x):
                return f(g(x))
            return composed

        square = lambda x: x ** 2
        add_ten = lambda x: x + 10

        square_then_add = compose(add_ten, square)
        print(square_then_add(3))    # 19 (3² + 10)
        print(square_then_add(5))    # 35 (5² + 10)
        print(square_then_add(0))    # 10 (0² + 10)
