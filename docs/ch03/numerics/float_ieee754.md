# IEEE 754 Standard

The IEEE 754 floating-point standard defines how computers represent real numbers in binary. Understanding this representation explains why certain decimal values cannot be stored exactly and why floating-point arithmetic behaves unexpectedly.

!!! tip "Mental Model"
    A 64-bit float packs three fields into 8 bytes: a sign bit, an 11-bit exponent, and a 52-bit mantissa. This is binary scientific notation -- the mantissa gives precision and the exponent gives range. Because the mantissa has only 52 bits, most decimal fractions (like 0.1) cannot be represented exactly, which is the root cause of floating-point surprises.

## Binary Scientific Notation

Floating-point numbers use binary scientific notation, analogous to decimal scientific notation.

### 1. Decimal vs Binary

In decimal, we write $1234.5 = 1.2345 \times 10^3$. Binary follows the same pattern.

```python
# Decimal scientific notation
print(f"{1234.5:.4e}")  # 1.2345e+03

# Binary representation of 5.75
# 5.75 = 4 + 1 + 0.5 + 0.25 = 2^2 + 2^0 + 2^-1 + 2^-2
# Binary: 101.11 = 1.0111 × 2^2
print(5.75)  # 5.75

# Verify
print(4 + 1 + 0.5 + 0.25)  # 5.75
```

### 2. Floating-Point Formula

IEEE 754 encodes numbers as:

$$x = (-1)^s \times (1 + m) \times 2^{e-\text{bias}}$$

Where:
- $s$ is the sign bit (0 = positive, 1 = negative)
- $m$ is the mantissa (fractional part after the implicit 1)
- $e$ is the biased exponent
- bias = 1023 for double precision, 127 for single precision

```python
import struct

def float_to_binary(x):
    """Show IEEE 754 binary representation."""
    # Pack as double, unpack as 8 bytes
    packed = struct.pack('>d', x)
    # Convert to binary string
    bits = ''.join(f'{byte:08b}' for byte in packed)
    
    sign = bits[0]
    exponent = bits[1:12]
    mantissa = bits[12:]
    
    return sign, exponent, mantissa

# Example: 5.75
s, e, m = float_to_binary(5.75)
print(f"Sign:     {s}")
print(f"Exponent: {e} = {int(e, 2)} (biased)")
print(f"Mantissa: {m[:20]}...")

# Decode
bias = 1023
exp_val = int(e, 2) - bias
print(f"\nActual exponent: {int(e, 2)} - {bias} = {exp_val}")
```

## Double Precision Format

Python's `float` uses IEEE 754 double precision (64 bits).

### 1. Bit Layout

The 64-bit double precision format allocates bits as follows:

| Component | Bits | Range |
|-----------|------|-------|
| Sign | 1 bit | 0 or 1 |
| Exponent | 11 bits | 0–2047 (biased) |
| Mantissa | 52 bits | Fraction after implicit 1 |

```python
import sys

# Python float info
print(f"Max float:        {sys.float_info.max:.6e}")
print(f"Min positive:     {sys.float_info.min:.6e}")
print(f"Mantissa digits:  {sys.float_info.mant_dig}")
print(f"Max exponent:     {sys.float_info.max_exp}")
print(f"Min exponent:     {sys.float_info.min_exp}")
```

### 2. Precision Limits

52 mantissa bits provide approximately 15–17 significant decimal digits.

```python
# 52 bits of precision
# 2^52 ≈ 4.5 × 10^15

# Numbers up to 2^52 are exact integers
print(2**52)           # 4503599627370496 (exact)
print(2**52 + 1)       # 4503599627370497 (exact)
print(float(2**52))    # 4503599627370496.0 (exact)

# Beyond 2^53, not all integers are representable
print(2**53)           # 9007199254740992
print(2**53 + 1)       # 9007199254740993
print(float(2**53 + 1))# 9007199254740992.0 (lost precision!)
```

### 3. Exponent Range

The 11-bit exponent allows magnitudes from $10^{-308}$ to $10^{308}$.

```python
import sys

# Exponent limits
print(f"Largest:  {sys.float_info.max:.6e}")   # ~1.8e+308
print(f"Smallest: {sys.float_info.min:.6e}")   # ~2.2e-308

# Overflow to infinity
print(1e308 * 10)   # inf

# Underflow to zero (gradual)
print(1e-323)       # 1e-323 (subnormal)
print(1e-324)       # 0.0 (underflow)
```

## Single Precision

NumPy provides single precision (32-bit) floats.

### 1. Bit Layout

Single precision uses fewer bits:

| Component | Bits | Range |
|-----------|------|-------|
| Sign | 1 bit | 0 or 1 |
| Exponent | 8 bits | 0–255 (biased) |
| Mantissa | 23 bits | Fraction after implicit 1 |

```python
import numpy as np

# Single precision info
info = np.finfo(np.float32)
print(f"Max:        {info.max:.6e}")
print(f"Min:        {info.min:.6e}")
print(f"Precision:  {info.precision} decimal digits")
print(f"Epsilon:    {info.eps:.6e}")
```

### 2. Double vs Single

Compare precision between formats.

```python
import numpy as np

# Same value in different precisions
val = 1.23456789012345

d = np.float64(val)
s = np.float32(val)

print(f"Original:  {val}")
print(f"float64:   {d}")
print(f"float32:   {s}")  # Lost digits!

# Precision difference
print(f"\nfloat64 epsilon: {np.finfo(np.float64).eps:.2e}")
print(f"float32 epsilon: {np.finfo(np.float32).eps:.2e}")
```

## Decimal Fractions Problem

Many common decimal fractions have infinite binary representations.

### 1. Why 0.1 Is Inexact

The decimal 0.1 cannot be represented exactly in binary.

$$0.1_{10} = 0.0\overline{0011}_{2}$$

The binary expansion repeats infinitely.

```python
# 0.1 is not exactly representable
print(f"{0.1:.20f}")  # 0.10000000000000000555...

# Show the actual stored value
from decimal import Decimal
print(Decimal(0.1))
# 0.1000000000000000055511151231257827021181583404541015625

# Compare with true 0.1
true_01 = Decimal('0.1')
stored_01 = Decimal(0.1)
print(f"Error: {stored_01 - true_01:.2e}")
```

### 2. Exact Representations

Numbers that are sums of powers of 2 are exact.

```python
# Powers of 2 are exact
print(f"{0.5:.20f}")   # 0.50000000000000000000 (exact: 2^-1)
print(f"{0.25:.20f}")  # 0.25000000000000000000 (exact: 2^-2)
print(f"{0.125:.20f}") # 0.12500000000000000000 (exact: 2^-3)

# Sums of powers of 2 are exact
print(f"{0.75:.20f}")  # 0.75000000000000000000 (2^-1 + 2^-2)

# But 0.1, 0.2, 0.3 are not
print(f"{0.1:.20f}")   # Error in last digits
print(f"{0.2:.20f}")   # Error in last digits
print(f"{0.3:.20f}")   # Error in last digits
```

### 3. Common Inexact Values

| Decimal | Binary (approximate) | Exact? |
|---------|---------------------|--------|
| 0.5 | 0.1 | ✓ |
| 0.25 | 0.01 | ✓ |
| 0.1 | 0.0001100110011... | ✗ |
| 0.2 | 0.0011001100110... | ✗ |
| 0.3 | 0.0100110011001... | ✗ |

```python
# Quick test for exact representation
def is_exact_binary(x, tol=1e-16):
    """Check if x can be represented exactly."""
    from decimal import Decimal
    stored = Decimal(x)
    intended = Decimal(str(x))
    return abs(stored - intended) < Decimal(str(tol))

print(f"0.5 exact: {is_exact_binary(0.5)}")   # True
print(f"0.1 exact: {is_exact_binary(0.1)}")   # False
print(f"0.125 exact: {is_exact_binary(0.125)}")  # True
```

## Rounding Modes

IEEE 754 defines rounding modes for operations.

### 1. Round to Nearest Even

Default mode—rounds to nearest, ties go to even.

```python
# Python's round() uses banker's rounding (round half to even)
print(round(0.5))   # 0 (tie goes to even)
print(round(1.5))   # 2 (tie goes to even)
print(round(2.5))   # 2 (tie goes to even)
print(round(3.5))   # 4 (tie goes to even)

# Contrast with away-from-zero rounding
import math
print(math.floor(2.5 + 0.5))  # 3 (traditional rounding)
```

### 2. Directed Rounding

Other rounding directions available via `math` module.

```python
import math

x = 2.7

print(f"floor({x}):   {math.floor(x)}")   # 2 (toward -∞)
print(f"ceil({x}):    {math.ceil(x)}")    # 3 (toward +∞)
print(f"trunc({x}):   {math.trunc(x)}")   # 2 (toward 0)

# Negative numbers show the difference
y = -2.7
print(f"\nfloor({y}):  {math.floor(y)}")  # -3
print(f"ceil({y}):   {math.ceil(y)}")     # -2
print(f"trunc({y}):  {math.trunc(y)}")    # -2
```

## Practical Implications

Understanding IEEE 754 helps write correct numerical code.

### 1. Integer Range in Floats

Floats can store integers exactly up to $2^{53}$.

```python
# Safe integer range for floats
MAX_SAFE_INT = 2**53

print(f"Max safe integer: {MAX_SAFE_INT:,}")

# Within range: exact
a = float(MAX_SAFE_INT - 1)
print(a == MAX_SAFE_INT - 1)  # True

# Beyond range: may lose precision
b = float(MAX_SAFE_INT + 1)
print(b == MAX_SAFE_INT + 1)  # False!
print(f"Stored: {b:.0f}, Expected: {MAX_SAFE_INT + 1}")
```

### 2. Format String Precision

Avoid false precision in output.

```python
x = 1/3

# Too many digits suggests false precision
print(f"{x:.20f}")  # 0.33333333333333331483

# Match actual precision (~15-17 digits)
print(f"{x:.15f}")  # 0.333333333333333
print(f"{x:.6f}")   # 0.333333 (reasonable for display)

# General rule: 15-16 significant digits max
import sys
print(f"Reliable digits: {sys.float_info.dig}")  # 15
```

### 3. Hexadecimal Float Literal

Python supports exact hexadecimal float representation.

```python
# Hexadecimal float literals (exact representation)
x = 0x1.999999999999ap-4  # Exact representation of ~0.1
print(x)  # 0.1

# Get hex representation of any float
print((0.1).hex())  # 0x1.999999999999ap-4
print((0.5).hex())  # 0x1.0000000000000p-1

# Round-trip without precision loss
original = 3.141592653589793
hex_rep = original.hex()
recovered = float.fromhex(hex_rep)
print(original == recovered)  # True
```


---

## Exercises


**Exercise 1.**
Use Python's `struct` module to extract the sign, exponent, and mantissa bits of the float `−6.5`. Verify your result by reconstructing the value from the extracted components.

??? success "Solution to Exercise 1"

    ```python
    import struct

    def float_parts(x):
        packed = struct.pack('>d', x)
        bits = ''.join(f'{b:08b}' for b in packed)
        sign = int(bits[0])
        exponent = int(bits[1:12], 2)
        mantissa = bits[12:]
        return sign, exponent, mantissa

    s, e, m = float_parts(-6.5)
    print(f"Sign: {s}")       # 1 (negative)
    print(f"Exponent: {e}")   # 1025
    print(f"Mantissa: {m[:10]}...")

    # Reconstruct: (-1)^1 * (1 + mantissa_fraction) * 2^(1025-1023)
    # = -1 * 1.625 * 4 = -6.5
    bias = 1023
    mantissa_val = int(m, 2) / (2**52)
    reconstructed = ((-1)**s) * (1 + mantissa_val) * (2**(e - bias))
    print(f"Reconstructed: {reconstructed}")  # -6.5
    ```

    The sign bit is 1 (negative), the biased exponent gives an actual exponent of 2, and the mantissa encodes the fraction 0.625, so the value is `-(1.625) * 4 = -6.5`.

---

**Exercise 2.**
Demonstrate that `float(2**53 + 1) == float(2**53)` is `True`. Explain why this happens in terms of IEEE 754 mantissa bits.

??? success "Solution to Exercise 2"

    ```python
    a = 2**53
    b = 2**53 + 1

    print(float(a) == float(b))  # True
    print(f"2^53     = {a}")
    print(f"2^53 + 1 = {b}")
    print(f"float(2^53)     = {float(a):.1f}")
    print(f"float(2^53 + 1) = {float(b):.1f}")
    ```

    IEEE 754 double precision has 52 mantissa bits (plus one implicit bit), so it can represent integers exactly up to `2^53`. Beyond that, consecutive floats are spaced 2 apart, and `2^53 + 1` rounds down to `2^53`.

---

**Exercise 3.**
Write a function `is_exact_float(x)` that checks whether a decimal string like `"0.375"` can be represented exactly as a Python float. Test it with `"0.5"`, `"0.1"`, and `"0.375"`.

??? success "Solution to Exercise 3"

    ```python
    from decimal import Decimal

    def is_exact_float(s):
        float_val = float(s)
        return Decimal(float_val) == Decimal(s)

    print(is_exact_float("0.5"))    # True
    print(is_exact_float("0.1"))    # False
    print(is_exact_float("0.375"))  # True
    ```

    Values that are sums of powers of 2 (like 0.5 = 2^-1 and 0.375 = 2^-2 + 2^-3) are exact. Values like 0.1 have infinite binary expansions and cannot be stored exactly.
