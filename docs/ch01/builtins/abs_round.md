
# abs() and round()

These are **value transformations**---they take a single number and produce a new number. Unlike collection operations (`len`, `sum`) or iteration tools (`enumerate`, `zip`), these operate on individual numeric values.

Both normalize numbers toward a simpler or more useful form: `abs()` strips the sign, `round()` reduces precision.

!!! tip "Mental Model"
    Think of `abs()` and `round()` as lenses that simplify a number. `abs()` removes direction (keeping only magnitude), while `round()` removes excess precision (keeping only the detail you need). Both take a raw number and return a cleaner version of it.

## abs()

Returns the absolute value of a number---its distance from zero on the number line.

```python
print(abs(-5))
```

Output:

```
5
```

## round()

Rounds numbers to a specified precision.

```python
print(round(3.14159,2))
```

Output:

```
3.14
```

## Rounding to the Nearest Integer

```python
print(round(5.7))
```

Output:

```
6
```

---

## Practical Example

```python
# Round prices for display
prices = [19.995, 5.555, 3.333]
formatted = [round(p, 2) for p in prices]
print(formatted)   # [20.0, 5.56, 3.33]

# Distance from zero (error magnitude)
errors = [-0.2, 0.5, -1.3]
magnitudes = [abs(e) for e in errors]
print(magnitudes)  # [0.2, 0.5, 1.3]
```

## Exercises

**Exercise 1.**
`round()` uses banker's rounding (round half to even). Predict the output:

```python
print(round(0.5))
print(round(1.5))
print(round(2.5))
print(round(3.5))
print(round(4.5))
```

Why does `round(0.5)` return `0` instead of `1`? What is banker's rounding and why does Python use it?

??? success "Solution to Exercise 1"
    Output:

    ```text
    0
    2
    2
    4
    4
    ```

    Python uses **banker's rounding** (round half to even): when a value is exactly halfway between two integers, it rounds to the nearest **even** number. `0.5` rounds to `0` (even), `1.5` rounds to `2` (even), `2.5` rounds to `2` (even), `3.5` rounds to `4` (even).

    Banker's rounding reduces systematic bias. If you always round 0.5 up (as taught in school), then averaging many rounded values produces a slight upward bias. Rounding to even distributes the rounding error equally between up and down, making it statistically unbiased. This is the IEEE 754 default rounding mode.

---

**Exercise 2.**
`abs()` works with different numeric types. Predict the output:

```python
print(abs(-5))
print(abs(3.14))
print(abs(-0.0))
print(abs(3 + 4j))
print(type(abs(3 + 4j)))
```

Why does `abs(3 + 4j)` return `5.0` instead of a complex number? What mathematical operation does `abs()` perform on complex numbers?

??? success "Solution to Exercise 2"
    Output:

    ```text
    5
    3.14
    0.0
    5.0
    <class 'float'>
    ```

    For real numbers, `abs()` returns the distance from zero (negating negatives). For complex numbers, `abs()` returns the **magnitude** (modulus): $|a + bi| = \sqrt{a^2 + b^2}$. So `abs(3 + 4j)` = $\sqrt{9 + 16}$ = $\sqrt{25}$ = `5.0`.

    The result is a `float`, not a complex number, because magnitude is always a non-negative real number. Note `abs(-0.0)` returns `0.0` (positive zero), not `-0.0`.

---

**Exercise 3.**
`round()` with negative `ndigits` rounds to powers of 10. Predict the output:

```python
print(round(1234, -1))
print(round(1234, -2))
print(round(1250, -2))
print(round(1350, -2))
print(round(1234, 0))
print(type(round(1234, 0)))
```

What type does `round(1234, 0)` return? How does this compare to `round(1234)` (without `ndigits`)? What is the rule for the return type?

??? success "Solution to Exercise 3"
    Output:

    ```text
    1230
    1200
    1200
    1400
    1234
    <class 'int'>
    ```

    Negative `ndigits` rounds to the left of the decimal point: `-1` rounds to tens, `-2` rounds to hundreds. Banker's rounding still applies: `1250` is halfway between `1200` and `1300`, so it rounds to `1200` (even hundreds).

    **Return type behavior:**

    - `round(x)` (no `ndigits`) always returns an `int`
    - `round(x, ndigits)` returns a number whose type matches the input type

    ```python
    round(1234)        # int → 1234
    round(1234, 0)     # int → 1234
    round(1234.0, 0)   # float → 1234.0
    ```

    If `ndigits` is omitted, the result is always `int`. If `ndigits` is provided, the result matches the input type (`int` in → `int` out, `float` in → `float` out). This distinction matters when the return type is used in further calculations.
