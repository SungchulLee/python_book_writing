# Precedence and Associativity

Operator precedence determines which operations are performed first. Associativity determines the order when operators have the same precedence.

!!! tip "Mental Model"
    Precedence is the invisible parentheses Python adds to your expression. `2 + 3 * 4` becomes `2 + (3 * 4)` because `*` binds tighter than `+`. When in doubt, add explicit parentheses -- they cost nothing at runtime and make intent unambiguous. The one surprise: `**` is right-associative, so `2 ** 3 ** 2` means `2 ** (3 ** 2) = 512`, not `(2 ** 3) ** 2 = 64`.

## Precedence Table

From **highest** to **lowest** precedence:

| Precedence | Operator | Description |
|------------|----------|-------------|
| Highest | `()`, `[]`, `{}` | Parentheses, indexing |
| | `x[i]`, `x[i:j]` | Indexing, slicing |
| | `**` | Exponentiation |
| | `+x`, `-x`, `~x` | Unary plus, minus, bitwise NOT |
| | `*`, `/`, `//`, `%` | Multiplication, division, modulo |
| | `+`, `-` | Addition, subtraction |
| | `<<`, `>>` | Bitwise shifts |
| | `&` | Bitwise AND |
| | `^` | Bitwise XOR |
| | `\|` | Bitwise OR |
| | `<`, `<=`, `>`, `>=`, `!=`, `==` | Comparisons |
| | `is`, `is not` | Identity |
| | `in`, `not in` | Membership |
| | `not` | Logical NOT |
| | `and` | Logical AND |
| | `or` | Logical OR |
| | `if else` | Conditional expression |
| | `lambda` | Lambda expression |
| Lowest | `=`, `+=`, `-=`, etc. | Assignment |


## Precedence Examples

### Arithmetic

Multiplication before addition:

```python
print(2 + 3 * 4)      # 14, not 20
print((2 + 3) * 4)    # 20

print(2 + 3 * 2)      # 8
print((2 + 3) * 2)    # 10
```

### Exponentiation

Highest among arithmetic operators:

```python
print(2 * 3 ** 2)     # 18 (3**2 first, then *2)
print((2 * 3) ** 2)   # 36
```

### Comparison and Logical

```python
print(3 > 2 and 5 < 10)   # True
# Evaluated as: (3 > 2) and (5 < 10)

print(not 3 > 2)          # False
# Evaluated as: not (3 > 2)
```


## Associativity

When operators have the **same precedence**, associativity determines order.

### Left-to-Right (Most Operators)

```python
print(10 / 2 * 5)     # 25.0
# Evaluated as: (10 / 2) * 5

print(10 - 5 - 2)     # 3
# Evaluated as: (10 - 5) - 2
```

### Right-to-Left (Exponentiation)

```python
print(2 ** 3 ** 2)    # 512
# Evaluated as: 2 ** (3 ** 2) = 2 ** 9

print((2 ** 3) ** 2)  # 64
```

### Right-to-Left (Assignment)

```python
a = b = c = 5
# Evaluated as: a = (b = (c = 5))
print(a, b, c)  # 5 5 5
```


## Common Pitfalls

### Comparison Chaining

Python evaluates chained comparisons specially:

```python
print(10 <= 20 == 30 > 40)
# Evaluated as: (10 <= 20) and (20 == 30) and (30 > 40)
# Result: False

print(1 < 2 < 3)      # True
# Evaluated as: (1 < 2) and (2 < 3)
```

### Bitwise vs Comparison

Comparison has higher precedence than bitwise:

```python
print(5 & 3 == 1)     # False
# Evaluated as: 5 & (3 == 1) = 5 & False = 0

print((5 & 3) == 1)   # True
```

### Logical Operators

`not` has higher precedence than `and` and `or`:

```python
print(not True or False)   # False
# Evaluated as: (not True) or False

print(not (True or False)) # False
```


## Best Practices

### Use Parentheses for Clarity

```python
# Unclear
result = a + b * c / d - e

# Clear
result = a + ((b * c) / d) - e
```

### Avoid Complex Expressions

```python
# Hard to read
x = a and b or c and not d or e

# Better
condition1 = a and b
condition2 = c and not d
x = condition1 or condition2 or e
```


## Summary

| Rule | Example |
|------|---------|
| `**` before `*`, `/` | `2 * 3 ** 2 = 18` |
| `*`, `/` before `+`, `-` | `2 + 3 * 4 = 14` |
| Comparison before logical | `3 > 2 and 5 < 10` |
| `not` before `and` before `or` | `not a or b` |
| Left-to-right for most | `10 / 2 * 5 = 25` |
| Right-to-left for `**` | `2 ** 3 ** 2 = 512` |

**When in doubt, use parentheses!**


---

## Exercises


**Exercise 1.**
Without running the code, evaluate the following expression step by step and give the final result:

```python
result = 2 + 3 * 4 ** 2 / 8 - 1
```

??? success "Solution to Exercise 1"

    ```python
    # Step by step:
    # 1. 4 ** 2 = 16         (exponentiation first)
    # 2. 3 * 16 = 48         (multiplication)
    # 3. 48 / 8 = 6.0        (division)
    # 4. 2 + 6.0 = 8.0       (addition)
    # 5. 8.0 - 1 = 7.0       (subtraction)

    result = 2 + 3 * 4 ** 2 / 8 - 1
    print(result)  # 7.0
    ```

    Exponentiation has the highest precedence among arithmetic operators, followed by multiplication/division (left to right), then addition/subtraction.

---

**Exercise 2.**
Explain why `5 & 3 == 1` evaluates to `False` and how adding parentheses fixes it to `True`. What precedence rule causes this?

??? success "Solution to Exercise 2"

    ```python
    # Without parentheses
    print(5 & 3 == 1)     # False
    # Evaluated as: 5 & (3 == 1) = 5 & False = 0

    # With parentheses
    print((5 & 3) == 1)   # True
    # Evaluated as: (5 & 3) = 1, then 1 == 1 = True
    ```

    Comparison operators (`==`) have higher precedence than bitwise operators (`&`). So `3 == 1` is evaluated first, yielding `False`, and then `5 & False` gives `0`.

---

**Exercise 3.**
Rewrite the following expression using parentheses to make the evaluation order explicit and unambiguous:

```python
x = not a or b and c > d + e * f
```

??? success "Solution to Exercise 3"

    ```python
    # Original: not a or b and c > d + e * f
    # Fully parenthesized:
    x = (not a) or (b and (c > (d + (e * f))))
    ```

    The precedence order is: `*` > `+` > `>` > `not` > `and` > `or`. Multiplication is evaluated first, then addition, then the comparison, then logical operators from highest to lowest precedence.
