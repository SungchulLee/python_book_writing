# Comparison Operators

Comparison operators compare values and return `True` or `False`.

!!! tip "Mental Model"
    Comparisons answer yes/no questions about values: equal, not equal, greater, less. Python allows chaining (`1 < x < 10`) which reads like mathematical notation and is evaluated as `1 < x and x < 10` without computing `x` twice. Remember that `==` compares values while `is` compares identity -- two different questions.

## Operator Summary

| Operator | Description | Example | Result |
|----------|-------------|---------|--------|
| `==` | Equal to | `3 == 3` | `True` |
| `!=` | Not equal to | `3 != 2` | `True` |
| `<` | Less than | `3 < 5` | `True` |
| `>` | Greater than | `3 > 5` | `False` |
| `<=` | Less than or equal | `3 <= 3` | `True` |
| `>=` | Greater than or equal | `5 >= 3` | `True` |


## Numeric Comparison

```python
print(5 > 3)    # True
print(5 < 3)    # False
print(5 >= 5)   # True
print(5 <= 4)   # False
print(5 == 5)   # True
print(5 != 5)   # False
```

### Integer and Float

Python handles mixed numeric types:

```python
print(1 == 1.0)   # True
print(1 < 1.0)    # False
print(1 <= 1.0)   # True
```


## Boolean Comparison

Booleans can be compared:

```python
print(True == True)    # True
print(True == False)   # False
print(True != False)   # True
```


## Chained Comparisons

Python allows chaining comparisons:

```python
print(1 < 2 < 3)           # True
print(1 < 2 < 3 < 4 < 5)   # True
print(1 < 5 > 3)           # True (1 < 5 and 5 > 3)
```

This is equivalent to:

```python
print(1 < 2 and 2 < 3)     # True
```

### Practical Example

```python
age = 25
if 18 <= age <= 65:
    print("Working age")
```


## Comparison Gotchas

### Floating-Point Precision

```python
print(0.1 + 0.2 == 0.3)   # False!
print(0.1 + 0.2)          # 0.30000000000000004
```

Use approximate comparison:

```python
import math
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

### Comparison Order

```python
# These are equivalent
print(10 <= 20 == 30 > 40)
print((10 <= 20) and (20 == 30) and (30 > 40))  # False
```


## Equality vs Identity

| Operator | Compares | Example |
|----------|----------|---------|
| `==` | Values | `[1,2] == [1,2]` → `True` |
| `is` | Identity | `[1,2] is [1,2]` → `False` |

See [Identity Operators](identity.md) for details.


## Comparison with Different Types

### Numeric Types Mix

```python
print(1 == 1.0 == True)  # True (True is 1)
print(0 == False)         # True
```

### String vs Number

```python
# Python 3: Cannot compare
print("5" > 3)  # TypeError
```

### None Comparison

```python
print(None == None)  # True
print(None is None)  # True (preferred)
```


## Use in Control Flow

```python
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
else:
    grade = 'F'
```


## Summary

- `==` compares values, `is` compares identity
- Chained comparisons: `a < b < c` means `a < b and b < c`
- Be careful with float comparison (use `math.isclose`)
- Cannot compare incompatible types in Python 3


---

## Exercises


**Exercise 1.**
Write a function `clamp(value, low, high)` that uses chained comparisons to check if `value` is within the range `[low, high]`. Return `low` if below, `high` if above, or `value` if within range.

??? success "Solution to Exercise 1"

    ```python
    def clamp(value, low, high):
        if low <= value <= high:
            return value
        elif value < low:
            return low
        else:
            return high

    print(clamp(5, 0, 10))   # 5
    print(clamp(-3, 0, 10))  # 0
    print(clamp(15, 0, 10))  # 10
    ```

    The chained comparison `low <= value <= high` is equivalent to `low <= value and value <= high` but more readable.

---

**Exercise 2.**
Demonstrate the floating-point comparison gotcha with `0.1 + 0.2 == 0.3`. Then fix the comparison using `math.isclose()` with both default and custom tolerances.

??? success "Solution to Exercise 2"

    ```python
    import math

    # The gotcha
    print(0.1 + 0.2 == 0.3)   # False
    print(f"{0.1 + 0.2:.20f}")  # 0.30000000000000004441

    # Fix with math.isclose (default tolerance)
    print(math.isclose(0.1 + 0.2, 0.3))  # True

    # Custom tolerance
    print(math.isclose(0.1 + 0.2, 0.3, rel_tol=1e-9, abs_tol=1e-12))  # True
    ```

    `math.isclose()` uses a relative tolerance (default `1e-9`) to account for floating-point representation errors.

---

**Exercise 3.**
Explain the difference between `==` and `is` by creating two lists with the same contents. Show that `==` returns `True` but `is` returns `False`, and explain when to use each.

??? success "Solution to Exercise 3"

    ```python
    a = [1, 2, 3]
    b = [1, 2, 3]

    print(a == b)   # True  (same values)
    print(a is b)   # False (different objects)

    c = a
    print(a is c)   # True  (same object)
    ```

    Use `==` to compare values. Use `is` only for singleton comparisons (`None`, `True`, `False`). Two separately created lists are equal in value but are distinct objects in memory.
