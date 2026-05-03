
# int Type Conversion

Python provides the `int()` function to convert values into integers.

This is one of the most common type conversions in Python, especially when working with:

- user input
- strings containing digits
- floating-point values
- boolean values

```mermaid
flowchart TD
    A[value]
    A --> B[int()]
    B --> C[integer result]
````

!!! tip "Mental Model"
    `int()` strips away everything that is not a whole number. For floats, it truncates toward zero (dropping the decimal part). For strings, it parses the text as a number. If the conversion is impossible---like `int("hello")`---Python raises a `ValueError` rather than guessing. This makes `int()` both a converter and a validator.

---

## 1. Basic Syntax

```python
int(x)
```

The function attempts to convert `x` into an integer.

Example:

```python
print(int("42"))
print(int(3.9))
print(int(True))
```

Output:

```text
42
3
1
```

---

## 2. Converting from Strings

A string containing digits can be converted to an integer.

```python
x = "123"
y = int(x)

print(y)
print(type(y))
```

Output:

```text
123
<class 'int'>
```

### Negative numbers

```python
print(int("-25"))
```

Output:

```text
-25
```

---

## 3. Converting from Floats

When converting a float to an integer, Python **truncates toward zero**.

```python
print(int(3.9))
print(int(3.1))
print(int(-3.9))
```

Output:

```text
3
3
-3
```

This is not rounding. It is truncation.

```mermaid
flowchart LR
    A[3.9] --> B[int()] --> C[3]
    D[-3.9] --> E[int()] --> F[-3]
```

---

## 4. Converting from Booleans

Because `bool` is a subclass of `int`, Boolean values convert naturally.

```python
print(int(True))
print(int(False))
```

Output:

```text
1
0
```

---

## 5. Base Conversion from Strings

`int()` can also interpret strings written in different bases.

Syntax:

```python
int(string, base)
```

Example:

```python
print(int("1010", 2))
print(int("52", 8))
print(int("2A", 16))
```

Output:

```text
10
42
42
```

This is useful when reading binary, octal, or hexadecimal values.

---

## 6. Invalid Conversions

Some conversions fail and raise `ValueError`.

```python
int("hello")
int("3.14")
```

These fail because the strings do not represent valid integers in base 10.

Example:

```python
try:
    print(int("hello"))
except ValueError:
    print("Cannot convert")
```

---

## 7. User Input Pattern

A common pattern is converting input strings into integers.

```python
age = int(input("Enter your age: "))
print(age + 1)
```

This works because `input()` always returns a string.

---

## 8. Worked Examples

### Example 1: converting input

```python
text = "45"
number = int(text)

print(number * 2)
```

Output:

```text
90
```

### Example 2: converting a float

```python
price = 19.99
whole = int(price)

print(whole)
```

Output:

```text
19
```

### Example 3: binary string to integer

```python
bits = "1101"
value = int(bits, 2)

print(value)
```

Output:

```text
13
```

---

## 9. Common Pitfalls

### Assuming `int()` rounds

```python
print(int(3.9))
```

This gives `3`, not `4`.

### Forgetting base when needed

```python
int("1010")
```

This is interpreted as decimal `1010`, not binary `10`.

---


## 10. Summary

Key ideas:

* `int()` converts compatible values into integers
* float conversion truncates toward zero
* strings can be converted when they contain valid integer text
* `int(string, base)` supports other number bases
* invalid conversions raise `ValueError`

Understanding `int()` is essential for handling input and performing exact numeric operations.


## Exercises

**Exercise 1.**
`int()` truncates toward zero, but `int("3.14")` raises `ValueError` even though `int(3.14)` works fine. Explain why Python treats these two cases differently. What is the correct way to convert the string `"3.14"` to the integer `3`?

??? success "Solution to Exercise 1"
    `int(3.14)` works because `3.14` is already a float object in memory -- Python simply truncates the fractional part to produce `3`. The conversion from float to int is a well-defined numeric operation.

    `int("3.14")` fails because `int()` parses the string as a **direct integer representation**. The string `"3.14"` contains a decimal point, which is not valid in an integer literal. `int()` does not first parse the string as a float and then truncate -- it expects the string to represent an integer directly.

    The correct way to convert `"3.14"` to `3`:

    ```python
    result = int(float("3.14"))  # First parse as float, then truncate
    ```

    This two-step conversion is explicit about what is happening: parse the string as a float, then convert the float to an integer.

---

**Exercise 2.**
The `int(string, base)` form interprets strings in different bases. Predict the output:

```python
print(int("ff", 16))
print(int("77", 8))
print(int("11111111", 2))
print(int("10", 3))
print(int("10", 0))
```

What does base `0` mean? Why does Python require a string (not a number) as the first argument when specifying a base?

??? success "Solution to Exercise 2"
    Output:

    ```text
    255
    63
    255
    3
    ```

    The last one (`int("10", 0)`) requires explanation. Base `0` means **auto-detect the base from the string prefix**:

    - `"0b..."` or `"0B..."` = binary
    - `"0o..."` or `"0O..."` = octal
    - `"0x..."` or `"0X..."` = hexadecimal
    - Otherwise = decimal

    So `int("10", 0)` treats `"10"` as decimal (no prefix), giving `10`. But `int("0xff", 0)` would give `255`.

    Python requires a string (not a number) when specifying a base because bases only make sense for **textual representations**. The integer `10` is just a number -- it has no inherent base. But the string `"10"` can mean ten (decimal), two (binary), eight (octal), or sixteen (hex) depending on interpretation. Bases describe how digits in text map to numeric values.

---

**Exercise 3.**
A programmer wants to convert user input to an integer safely:

```python
user_input = "  42  "
print(int(user_input))

user_input2 = "42.0"
print(int(user_input2))

user_input3 = ""
print(int(user_input3))
```

Predict which conversions succeed and which raise errors. Explain the results, and write a robust function that converts a string to an integer, handling leading/trailing whitespace, float strings, and empty strings gracefully.

??? success "Solution to Exercise 3"
    Results:

    - `int("  42  ")` **succeeds**, returns `42`. `int()` strips leading and trailing whitespace automatically.
    - `int("42.0")` **raises `ValueError`**. The decimal point is not valid in an integer string, even if the fractional part is zero.
    - `int("")` **raises `ValueError`**. An empty string does not represent any integer.

    A robust conversion function:

    ```python
    def safe_int(s, default=0):
        s = s.strip()
        if not s:
            return default
        try:
            return int(s)
        except ValueError:
            try:
                return int(float(s))
            except (ValueError, OverflowError):
                return default
    ```

    This handles whitespace (via `strip()`), empty strings (returns default), pure integer strings (first `try`), float-like strings like `"42.0"` (nested `try` with `int(float(s))`), and completely invalid strings (returns default).
