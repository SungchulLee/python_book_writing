# Number Systems

Python supports multiple number system representations for integers.

!!! tip "Mental Model"
    An integer is just a number -- the base you write it in is a display choice, not a different type. `0b1010`, `0o12`, `10`, and `0xa` are all the same `int` object (ten). Python provides literal prefixes for binary, octal, and hex, plus `bin()`, `oct()`, and `hex()` to convert back to string representations.

---

## Representations

Four different ways to represent integers in Python.

### 1. Representation Table

||Format Specifier|Key Word|Example|
|:---|:---:|:---|:---|
|Decimal (10)|d||10|
|Binary (2)|b|0b or 0B|0b10 or 0B10|
|Octal (8)|o|0o or 0O|0o10 or 0O10|
|Hexadecimal (16)|x or X|0x or 0X|0x10 or 0X10|

---

## Decimal

Decimal is the default representation (base 10).

### 1. Decimal Example

```python
def main():
    a = 10
    print(a, type(a))
    print(f"{a = }")
    print(f"{a = :d}") # Decimal Representation
    print(f"{a = :b}") # Binary Representation
    print(f"{a = :o}") # Octal Representation
    print(f"{a = :x}") # Hexadecimal Representation

if __name__ == "__main__":
    main()
```

---

## Binary

Binary representation uses base 2 with prefix `0b` or `0B`.

### 1. Binary Literals

```python
def main():
    a = 0b10
    print(a, type(a))
    print(f"{a = }")
    print(f"{a = :d}") # Decimal Representation
    print(f"{a = :b}") # Binary Representation
    print(f"{a = :o}") # Octal Representation
    print(f"{a = :x}") # Hexadecimal Representation

if __name__ == "__main__":
    main()
```

### 2. Capital Prefix

```python
def main():
    a = 0B10
    print(a, type(a))
    print(f"{a = }")
    print(f"{a = :d}") # Decimal Representation
    print(f"{a = :b}") # Binary Representation
    print(f"{a = :o}") # Octal Representation
    print(f"{a = :x}") # Hexadecimal Representation

if __name__ == "__main__":
    main()
```

### 3. Decimal to Binary

```python
def main():
    a = 17

    b = bin(a)
    print(b, type(b))  # Output: 0b10001 <class 'str'>

    c = format(a,"b")
    print(c, type(c))  # Output: 10001 <class 'str'>

if __name__ == "__main__":
    main()
```

### 4. Negative Binary

```python
def main():
    a = -17
    b = bin(a)
    print(b, type(b))  # Output: -0b10001 <class 'str'>

if __name__ == "__main__":
    main()
```

### 5. Binary to Decimal

```python
def main():
    a = 0b10001
    b = int(a)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = 0B10001
    b = int(a)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = "0b10001"
    b = int(a[2:], 2)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = "0B10001"
    b = int(a[2:], 2)
    print(b, type(b))  # Output: 17 <class 'int'>

if __name__ == "__main__":
    main()
```

### 6. Negative Conversion

```python
def main():
    a = -0b10001
    b = int(a)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = -0B10001
    b = int(a)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = "-0b10001"
    b = -int(a[3:], 2)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = "-0B10001"
    b = -int(a[3:], 2)
    print(b, type(b))  # Output: -17 <class 'int'>

if __name__ == "__main__":
    main()
```

---

## Octal

Octal representation uses base 8 with prefix `0o` or `0O`.

### 1. Octal Literals

```python
def main():
    a = 0o10
    print(a, type(a))
    print(f"{a = }")
    print(f"{a = :d}") # Decimal Representation
    print(f"{a = :b}") # Binary Representation
    print(f"{a = :o}") # Octal Representation
    print(f"{a = :x}") # Hexadecimal Representation

if __name__ == "__main__":
    main()
```

### 2. Capital Prefix

```python
def main():
    a = 0O10
    print(a, type(a))
    print(f"{a = }")
    print(f"{a = :d}") # Decimal Representation
    print(f"{a = :b}") # Binary Representation
    print(f"{a = :o}") # Octal Representation
    print(f"{a = :x}") # Hexadecimal Representation

if __name__ == "__main__":
    main()
```

### 3. Decimal to Octal

```python
def main():
    a = 17
    b = oct(17)
    print(b, type(b))  # Output: 0o21 <class 'str'>

if __name__ == "__main__":
    main()
```

### 4. Negative Octal

```python
def main():
    a = -17
    b = oct(17)
    print(b, type(b))  # Output: 0o21 <class 'str'>

if __name__ == "__main__":
    main()
```

### 5. Octal to Decimal

```python
def main():
    a = 0o21
    b = int(a)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = 0O21
    b = int(a)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = "0o21"
    b = int(a[2:], 8)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = "0O21"
    b = int(a[2:], 8)
    print(b, type(b))  # Output: 17 <class 'int'>

if __name__ == "__main__":
    main()
```

### 6. Negative Conversion

```python
def main():
    a = -0o21
    b = int(a)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = -0O21
    b = int(a)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = "-0o21"
    b = -int(a[3:], 8)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = "-0O21"
    b = -int(a[3:], 8)
    print(b, type(b))  # Output: -17 <class 'int'>

if __name__ == "__main__":
    main()
```

---

## Hexadecimal

Hexadecimal representation uses base 16 with prefix `0x` or `0X`.

### 1. Hex Literals

```python
def main():
    a = 0x1f
    print(a, type(a))
    print(f"{a = }")
    print(f"{a = :d}") # Decimal Representation
    print(f"{a = :b}") # Binary Representation
    print(f"{a = :o}") # Octal Representation
    print(f"{a = :x}") # Hexadecimal Representation

if __name__ == "__main__":
    main()
```

### 2. Capital Prefix

```python
def main():
    a = 0X1f
    print(a, type(a))
    print(f"{a = }")
    print(f"{a = :d}") # Decimal Representation
    print(f"{a = :b}") # Binary Representation
    print(f"{a = :o}") # Octal Representation
    print(f"{a = :x}") # Hexadecimal Representation

if __name__ == "__main__":
    main()
```

### 3. Decimal to Hex

```python
def main():
    a = 1117
    b = hex(a)
    print(b, type(b))  # Output: 0x45d <class 'str'>

if __name__ == "__main__":
    main()
```

### 4. Negative Hex

```python
def main():
    a = -17
    b = hex(a)
    print(b, type(b))  # Output: -0x11 <class 'str'>

if __name__ == "__main__":
    main()
```

### 5. Hex to Decimal

```python
def main():
    a = 0x11
    b = int(a)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = 0X11
    b = int(a)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = "0x11"
    b = int(a[2:],16)
    print(b, type(b))  # Output: 17 <class 'int'>

    a = "0X11"
    b = int(a[2:],16)
    print(b, type(b))  # Output: 17 <class 'int'>

if __name__ == "__main__":
    main()
```

### 6. Negative Conversion

```python
def main():
    a = -0x11
    b = int(a)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = -0X11
    b = int(a)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = "-0x11"
    b = -int(a[3:],16)
    print(b, type(b))  # Output: -17 <class 'int'>

    a = "-0X11"
    b = -int(a[3:],16)
    print(b, type(b))  # Output: -17 <class 'int'>

if __name__ == "__main__":
    main()
```

---

## Conclusion

Python's support for multiple number systems makes it easy to work with different bases. Understanding these representations is essential for low-level programming, bit manipulation, and working with hardware interfaces.


---

## Exercises


**Exercise 1.**
Write a function `convert_all_bases(n)` that takes a decimal integer and returns a dictionary with keys `"bin"`, `"oct"`, and `"hex"`, each holding the string representation (with prefix) of `n` in that base.

??? success "Solution to Exercise 1"

    ```python
    def convert_all_bases(n):
        return {
            "bin": bin(n),
            "oct": oct(n),
            "hex": hex(n),
        }

    result = convert_all_bases(255)
    print(result)
    # {'bin': '0b11111111', 'oct': '0o377', 'hex': '0xff'}
    ```

    `bin()`, `oct()`, and `hex()` return string representations with the appropriate prefix.

---

**Exercise 2.**
Given the string `"0b11010110"`, convert it to its decimal, octal, and hexadecimal string representations without using `int()` with a base argument more than once. Print all three results.

??? success "Solution to Exercise 2"

    ```python
    s = "0b11010110"
    decimal_val = int(s, 2)          # Use int() once with base 2
    print(f"Decimal: {decimal_val}")  # 214
    print(f"Octal: {oct(decimal_val)}")  # 0o326
    print(f"Hex: {hex(decimal_val)}")    # 0xd6
    ```

    `int(s, 2)` parses a binary string. From the integer, `oct()` and `hex()` produce the other representations.

---

**Exercise 3.**
Write a function `base_to_decimal(s)` that accepts a string with a prefix (`"0b"`, `"0o"`, or `"0x"`) and returns the decimal integer. If the prefix is unrecognized, raise a `ValueError`.

??? success "Solution to Exercise 3"

    ```python
    def base_to_decimal(s):
        prefix = s[:2].lower()
        if prefix == "0b":
            return int(s, 2)
        elif prefix == "0o":
            return int(s, 8)
        elif prefix == "0x":
            return int(s, 16)
        else:
            raise ValueError(f"Unrecognized prefix in '{s}'")

    print(base_to_decimal("0b1010"))   # 10
    print(base_to_decimal("0o17"))     # 15
    print(base_to_decimal("0xFF"))     # 255
    ```

    The function inspects the first two characters to determine the base, then delegates to `int()` with the appropriate base argument.
