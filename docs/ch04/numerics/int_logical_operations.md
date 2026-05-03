# Logical Operations

Python's logical operators `or`, `and`, and `not` can work with integers because non-zero integers are **truthy** and `0` is **falsy**.

!!! tip "Mental Model"
    Python's `and`/`or` are not Boolean gates -- they are short-circuit selectors that return one of their operands. `or` returns the first truthy value (or the last), `and` returns the first falsy value (or the last). Once you see them as "pick the deciding operand," their behavior with any type becomes predictable.

---

## Truthiness

Integers are treated as Boolean values in logical operations.

### 1. Truthy vs Falsy

- **Non-zero integer** = truthy (True)
- **Zero (0)** = falsy (False)

This allows logical operators to manipulate integer values directly.

---

## The or Operator

The `or` operator returns the first truthy value or the last value if all are falsy.

### 1. Evaluation Rules

$$\begin{array}{clccccccccccccccc}
\text{a}&&&\text{a or b}\\
\text{True}&\text{(a or b) is True due to a}&\Rightarrow&\text{returns a}\\
\text{False}&\text{(a or b) depends on b}&\Rightarrow&\text{returns b}\\
\end{array}$$

### 2. Non-zero First

```python
def main():
    a = 156
    b = 52
    c = a or b
    print(c)  # Output: 156

if __name__ == "__main__":
    main()
```

### 3. Zero First

```python
def main():
    a = 0
    b = 52
    c = a or b
    print(c)  # Output: 52

if __name__ == "__main__":
    main()
```

### 4. Basic Example

Since `a` is non-zero (truthy), the `or` operator immediately returns `a`:

```python
a = 5  # Non-zero, evaluates to True
b = 0  # Zero, evaluates to False

result = a or b  # Since 'a' is truthy, 'a' is returned
print(result)  # Output: 5
```

If both operands are zero:

```python
a = 0  # Falsy
b = 0  # Falsy

result = a or b  # Both falsy, so returns 'b'
print(result)  # Output: 0
```

**Key Takeaway:** The `or` operator returns the first non-zero value, or the last value if all are zero.

---

## The and Operator

The `and` operator returns the second operand if both are truthy, otherwise returns the first falsy operand.

### 1. Evaluation Rules

$$\begin{array}{clccccccccccccccc}
\text{a}&&&\text{a and b}\\
\text{True}&\text{(a and b) depends on b}&\Rightarrow&\text{returns b}\\
\text{False}&\text{(a and b) is False due to a}&\Rightarrow&\text{returns a}\\
\end{array}$$

### 2. Both Non-zero

```python
def main():
    a = 156
    b = 52
    print(a and b)  # Output: 52

if __name__ == "__main__":
    main()
```

### 3. First Zero

```python
def main():
    a = 0
    b = 52
    print(a and b)  # Output: 0

if __name__ == "__main__":
    main()
```

### 4. Basic Example

Both `a` and `b` are truthy, so `b` is returned:

```python
a = 5  # Non-zero, evaluates to True
b = 3  # Non-zero, evaluates to True

result = a and b  # Both truthy, so 'b' is returned
print(result)  # Output: 3
```

If the first operand is zero:

```python
a = 0  # Falsy
b = 10  # Non-zero, evaluates to True

result = a and b  # Since 'a' is falsy, result is 'a' (0)
print(result)  # Output: 0
```

**Key Takeaway:** The `and` operator returns the second operand if both are non-zero; otherwise, it returns the first operand.

---

## The not Operator

The `not` operator inverts the truthiness of a value.

### 1. Evaluation Rules

$$\begin{array}{clccccccccccccccc}
\text{a}&&&\text{not a}\\
\text{True}&\text{(not a) is False}&\Rightarrow&\text{returns False}\\
\text{False}&\text{(not a) is True}&\Rightarrow&\text{returns True}\\
\end{array}$$

### 2. Non-zero Input

```python
def main():
    a = 3
    print(not a)  # Output: False

if __name__ == "__main__":
    main()
```

### 3. Zero Input

```python
def main():
    a = 0
    print(not a)  # Output: True

if __name__ == "__main__":
    main()
```

### 4. Basic Example

```python
a = 5  # Non-zero, evaluates to True

result = not a  # Inverts truthiness
print(result)  # Output: False
```

For zero:

```python
b = 0  # Falsy

result = not b  # Inverts truthiness
print(result)  # Output: True
```

**Key Takeaway:** `not` inverts the truthiness—non-zero integers become `False`, and zero becomes `True`.

---

## Combined Operations

Logical operators can be combined for complex expressions.

### 1. or and and

```python
a = 0
b = 3
c = 5

result = a or (b and c)  # 'b and c' returns 5, then 'a or 5' returns 5
print(result)  # Output: 5
```

### 2. not and and

```python
a = 0
b = 5

result = not (a and b)  # 'a and b' is 0, so 'not 0' is True
print(result)  # Output: True
```

### 3. Nested Logic

```python
x = 5
y = 0
z = 10

result = not x and (y or z)  # 'not x' is False, 'y or z' is 10, False and 10 is False
print(result)  # Output: False
```

---

## Short-Circuit

Python uses short-circuit evaluation for efficiency.

### 1. Short-Circuit or

The `or` operator stops evaluating once it finds a truthy value.

```python
a = 5
b = expensive_function()  # Not called if a is truthy

result = a or b  # b is never evaluated because a is truthy
```

### 2. Short-Circuit and

The `and` operator stops evaluating once it finds a falsy value.

```python
a = 0
b = expensive_function()  # Not called if a is falsy

result = a and b  # b is never evaluated because a is falsy
```

---

## Conclusion

In Python, logical operations with integers leverage implicit truthiness conversion. The `or` operator returns the first truthy value, `and` checks if both are truthy, and `not` inverts truthiness. These operations are essential for making decisions and controlling logic flow, all while using Python's treatment of integers as Boolean values.

---

## Exercises

**Exercise 1.**
`and` and `or` return one of their operands, not necessarily `True`/`False`. `not` always returns a `bool`. Predict the output:

```python
print(type(5 or 0))
print(type(5 and 0))
print(type(not 5))

print([] or {} or 0 or "hello" or None)
print(1 and 2 and 3)
print(1 and 0 and 3)
```

Why do `or` and `and` return an operand while `not` returns a `bool`? What practical use does this enable?

??? success "Solution to Exercise 1"
    Output:

    ```text
    <class 'int'>
    <class 'int'>
    <class 'bool'>
    hello
    3
    0
    ```

    `or` returns the **first truthy operand** (or the last operand if all are falsy). `and` returns the **first falsy operand** (or the last operand if all are truthy). Both return the actual operand object, preserving its type.

    `not` is different: it always returns `True` or `False` because its purpose is logical negation, not value selection.

    The practical use: `or` provides default values (`name = user_input or "Anonymous"`), and `and` provides guard patterns (`x and x[0]` returns `x` if empty, otherwise the first element).

---

**Exercise 2.**
Short-circuit evaluation means the second operand may never be evaluated. Predict the output:

```python
def explode():
    raise RuntimeError("boom!")

print(True or explode())
print(False and explode())
print(0 or 0 or 42 or explode())
```

What happens if you change the first line to `print(False or explode())`? Why is short-circuiting more than just a performance optimization -- how does it enable safe guard patterns like `x != 0 and y / x`?

??? success "Solution to Exercise 2"
    Output:

    ```text
    True
    False
    42
    ```

    `explode()` is never called in any of these cases. `True or explode()`: `or` finds `True` and stops. `False and explode()`: `and` finds `False` and stops. `0 or 0 or 42 or explode()`: `or` finds `42` (truthy) and stops.

    `False or explode()` would raise `RuntimeError` because `or` must evaluate the second operand when the first is falsy.

    Short-circuiting enables **safe guard patterns**: `x != 0 and y / x` never divides by zero because if `x == 0`, the `and` short-circuits before evaluating `y / x`. Similarly, `lst and lst[0]` safely handles empty lists. Without short-circuiting, both operands would always be evaluated, making such patterns impossible.

---

**Exercise 3.**
Operator precedence: `not` binds tighter than `and`, which binds tighter than `or`. Predict the output:

```python
print(not 0 or 1)
print(not (0 or 1))

print(1 or 2 and 3)
print((1 or 2) and 3)

print(not 0 and not 0)
print(not (0 and not 0))
```

Why does `not 0 or 1` differ from `not (0 or 1)`? Trace the evaluation step by step.

??? success "Solution to Exercise 3"
    Output:

    ```text
    True
    False
    1
    3
    True
    True
    ```

    `not 0 or 1`: Precedence is `(not 0) or 1` = `True or 1` = `True`. The `not` binds to `0` first, giving `True`, then `True or 1` short-circuits to `True`.

    `not (0 or 1)`: Parentheses force `0 or 1` = `1` first, then `not 1` = `False`.

    `1 or 2 and 3`: `and` binds tighter, so `(1 or (2 and 3))` = `1 or 3` = `1`. But `or` short-circuits: since `1` is truthy, `2 and 3` is never evaluated.

    `(1 or 2) and 3`: `1 or 2` = `1`, then `1 and 3` = `3`.

    The precedence order `not > and > or` matches mathematical logic where NOT > AND > OR.
