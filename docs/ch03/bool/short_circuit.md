# Short-Circuit Evaluation

Python's and and or operators use short-circuit evaluation, stopping evaluation as soon as the result is determined. This behavior is crucial for writing efficient code and preventing errors from evaluating unnecessary expressions.

!!! tip "Mental Model"
    Think of `and`/`or` as lazy gatekeepers. `and` stops at the first failure because one `False` makes the whole expression `False`. `or` stops at the first success because one `True` makes the whole expression `True`. This laziness is not just an optimization -- it lets you write guard patterns like `x and x.method()` that safely skip the second part when the first is falsy.

---

## and Short-Circuiting

### Early Termination with and

```python
def test_value(x):
    print(f"Testing {x}")
    return x > 5

result = False and test_value(10)
print(f"Result: {result}")
```

Output:
```
Result: False
```

Notice that test_value was never called because the first operand is False.

### Practical Usage

```python
user = {"name": "Alice", "age": 30}

if user and user.get("name") and len(user.get("name")) > 0:
    print(f"Valid user: {user['name']}")
```

Output:
```
Valid user: Alice
```

## or Short-Circuiting

### Early Termination with or

```python
def get_default():
    print("Getting default")
    return "default"

result = "custom" or get_default()
print(f"Result: {result}")
```

Output:
```
custom
```

The get_default function is never called because "custom" is truthy.

### Default Value Pattern

```python
username = None
fallback = "guest"

displayed_name = username or fallback
print(f"Username: {displayed_name}")
```

Output:
```
Username: guest
```

## Efficiency Implications

### Avoiding Expensive Operations

```python
import time

def expensive_check():
    time.sleep(0.1)
    return True

# Short-circuits immediately
result = False and expensive_check()
print(f"Instant result: {result}")

# This would wait for expensive_check
result2 = True and expensive_check()
print(f"Takes time: {result2}")
```

Output:
```
Instant result: False
Takes time: True
```

## Complex Expressions

### Order Matters

```python
def check_condition(n, label):
    print(f"Checking {label}")
    return n > 5

# Only first is checked
result = check_condition(3, "A") and check_condition(10, "B")
print(f"Result: {result}\n")

# Both are checked
result = check_condition(10, "A") and check_condition(3, "B")
print(f"Result: {result}")
```

Output:
```
Checking A
Result: False

Checking A
Checking B
Result: False
```

---

## Exercises


**Exercise 1.**
Without running the code, predict which functions get called and what the final output is.

```python
def a():
    print("a called")
    return True

def b():
    print("b called")
    return False

def c():
    print("c called")
    return True

result = a() or b() or c()
print(f"Result: {result}")
```

??? success "Solution to Exercise 1"

        ```
        a called
        Result: True
        ```

    `a()` returns `True`. Since `or` short-circuits on the first truthy value, `b()` and `c()` are never called. The result is `True` (the return value of `a()`).

---

**Exercise 2.**
Write a function `safe_divide(a, b)` that returns `a / b` if `b` is not zero, or `"undefined"` otherwise. Use short-circuit evaluation with `and`/`or` in a single expression (no `if` statement).

??? success "Solution to Exercise 2"

        ```python
        def safe_divide(a, b):
            return b and a / b or "undefined"

        # Caution: this fails if a/b is 0 (falsy). A safer version:
        def safe_divide(a, b):
            return a / b if b else "undefined"

        print(safe_divide(10, 2))   # 5.0
        print(safe_divide(10, 0))   # "undefined"
        ```

    The `and`/`or` approach works for most cases but has an edge case: if `a / b` evaluates to `0` or `0.0` (falsy), it would incorrectly return `"undefined"`. The conditional expression version is safer and more readable.

---

**Exercise 3.**
Explain why the following code does not raise a `ZeroDivisionError` even though `b` is 0.

```python
b = 0
result = b != 0 and 10 / b > 2
print(result)
```

??? success "Solution to Exercise 3"

    Short-circuit evaluation prevents the division from executing. `b != 0` evaluates to `False`, so `and` immediately returns `False` without evaluating the right operand `10 / b > 2`.

        ```python
        b = 0
        result = b != 0 and 10 / b > 2
        print(result)  # False
        ```

    `and` stops at the first falsy operand. Since `b != 0` is `False`, Python never evaluates `10 / b`, avoiding the `ZeroDivisionError`.
