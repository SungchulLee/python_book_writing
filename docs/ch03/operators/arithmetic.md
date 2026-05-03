# Arithmetic Operators

Arithmetic operators perform mathematical operations on numeric values.

!!! tip "Mental Model"
    Python has two division operators: `/` always returns a float (true division), while `//` always rounds toward negative infinity (floor division). The modulo `%` follows floor division's sign convention. These three operators -- `/`, `//`, `%` -- form a consistent trio governed by the invariant `a == (a // b) * b + (a % b)`.

## Operator Summary

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `3 + 2` | `5` |
| `-` | Subtraction | `3 - 2` | `1` |
| `*` | Multiplication | `3 * 2` | `6` |
| `/` | Division | `7 / 2` | `3.5` |
| `//` | Floor Division | `7 // 2` | `3` |
| `%` | Modulo | `7 % 2` | `1` |
| `**` | Exponentiation | `3 ** 2` | `9` |


## Basic Operations

```python
a = 10
b = 3

print(a + b)   # 13 (addition)
print(a - b)   # 7  (subtraction)
print(a * b)   # 30 (multiplication)
print(a / b)   # 3.333... (true division)
print(a // b)  # 3  (floor division)
print(a % b)   # 1  (remainder)
print(a ** b)  # 1000 (10^3)
```


## Division Types

### True Division (`/`)

Always returns a float:

```python
print(10 / 2)   # 5.0
print(7 / 2)    # 3.5
print(1 / 3)    # 0.333...
```

### Floor Division (`//`)

Returns the largest integer less than or equal to the result:

```python
print(7 // 2)    # 3
print(10 // 3)   # 3
print(-7 // 2)   # -4 (rounds toward negative infinity)
```

### Modulo (`%`)

Returns the remainder after division:

```python
print(7 % 2)     # 1
print(10 % 3)    # 1
print(15 % 5)    # 0
```


## Unary Operators

```python
x = 5
print(+x)   # 5  (unary plus)
print(-x)   # -5 (unary minus)
```


## Exponentiation

```python
print(2 ** 3)    # 8
print(2 ** 0.5)  # 1.414... (square root)
print(10 ** -2)  # 0.01

# Right-to-left associativity
print(2 ** 3 ** 2)   # 512 (2^9, not 8^2)
```


## Assignment Operators

Combine assignment with arithmetic:

| Operator | Example | Equivalent To |
|----------|---------|---------------|
| `+=` | `x += 2` | `x = x + 2` |
| `-=` | `x -= 2` | `x = x - 2` |
| `*=` | `x *= 2` | `x = x * 2` |
| `/=` | `x /= 2` | `x = x / 2` |
| `//=` | `x //= 2` | `x = x // 2` |
| `%=` | `x %= 2` | `x = x % 2` |
| `**=` | `x **= 2` | `x = x ** 2` |

```python
x = 10
x += 5   # x = 15
x *= 2   # x = 30
x //= 4  # x = 7
```


## Type Behavior

### Integer Operations

```python
print(5 + 3)     # 8 (int)
print(5 * 3)     # 15 (int)
print(5 // 3)    # 1 (int)
print(5 / 3)     # 1.666... (float, always)
```

### Float Operations

```python
print(5.0 + 3)   # 8.0 (float)
print(5 * 3.0)   # 15.0 (float)
```

### Complex Operations

```python
print((1+2j) + (3+4j))  # (4+6j)
print((1+2j) * (3+4j))  # (-5+10j)
```


## Common Use Cases

### Check Even/Odd

```python
if n % 2 == 0:
    print("Even")
else:
    print("Odd")
```

### Wrap Around (Circular)

```python
# Cycle through 0-9
index = (index + 1) % 10
```

### Integer Division with Remainder

```python
quotient, remainder = divmod(17, 5)
print(quotient, remainder)  # 3, 2
```


## Summary

- `/` always returns float
- `//` returns floor (rounds toward negative infinity)
- `%` returns remainder
- `**` is right-associative
- Use `divmod()` for both quotient and remainder


---

## Exercises


**Exercise 1.**
Explain the difference between `/` and `//` for both positive and negative numbers. Show examples where `-7 / 2` and `-7 // 2` give different results and explain why.

??? success "Solution to Exercise 1"

    ```python
    # True division always returns float
    print(-7 / 2)    # -3.5

    # Floor division rounds toward negative infinity
    print(-7 // 2)   # -4 (not -3!)

    # For positive numbers
    print(7 / 2)     # 3.5
    print(7 // 2)    # 3
    ```

    `/` performs true division and returns a float. `//` performs floor division, rounding toward negative infinity. For `-7 // 2`, the mathematical result is `-3.5`, and the floor of `-3.5` is `-4`.

---

**Exercise 2.**
Using only `divmod()`, write a function `time_breakdown(total_seconds)` that converts a number of seconds into hours, minutes, and remaining seconds.

??? success "Solution to Exercise 2"

    ```python
    def time_breakdown(total_seconds):
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds

    h, m, s = time_breakdown(3725)
    print(f"{h}h {m}m {s}s")  # 1h 2m 5s
    ```

    `divmod(a, b)` returns `(a // b, a % b)` in one call, which is both cleaner and slightly faster than computing quotient and remainder separately.

---

**Exercise 3.**
Demonstrate that `**` is right-associative by showing that `2 ** 3 ** 2` equals `2 ** 9` (not `8 ** 2`). Then use parentheses to get the left-associative result.

??? success "Solution to Exercise 3"

    ```python
    # Right-associative (default)
    print(2 ** 3 ** 2)    # 512 (2 ** 9)

    # Left-associative (with parentheses)
    print((2 ** 3) ** 2)  # 64 (8 ** 2)

    # Verify
    print(2 ** 9)         # 512
    print(8 ** 2)         # 64
    ```

    Without parentheses, `2 ** 3 ** 2` is evaluated as `2 ** (3 ** 2) = 2 ** 9 = 512`. This right-to-left associativity matches mathematical convention for exponentiation.
