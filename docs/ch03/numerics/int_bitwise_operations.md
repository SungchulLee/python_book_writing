# Bitwise Operations

Since integers are stored in binary, Python allows bitwise operations to manipulate individual bits.

!!! tip "Mental Model"
    Bitwise operators treat an integer as a row of independent on/off switches. `&` keeps a switch on only if both inputs are on, `|` turns it on if either is, `^` toggles it when the inputs differ, and `~` flips every switch. Shifts (`<<`, `>>`) slide the entire row left or right, which is equivalent to multiplying or dividing by powers of two.

---

## Basic Operators

Python provides six bitwise operators for bit-level manipulation.

### 1. AND (&)

Sets each bit to 1 if both bits are 1.

```python
x = 5  # 0b0101
y = 3  # 0b0011

print(x & y)  # Bitwise AND: 1 (0b0101 & 0b0011 = 0b0001)
```

Example: `5 & 3` results in `1` (binary `101 & 011` is `001`).

### 2. OR (|)

Sets each bit to 1 if one of the bits is 1.

```python
x = 5  # 0b0101
y = 3  # 0b0011

print(x | y)  # Bitwise OR: 7  (0b0101 | 0b0011 = 0b0111)
```

Example: `5 | 3` results in `7` (binary `101 | 011` is `111`).

### 3. XOR (^)

Sets each bit to 1 if only one of the bits is 1.

```python
x = 5  # 0b0101
y = 3  # 0b0011

print(x ^ y)  # Bitwise XOR: 6 (0b0101 ^ 0b0011 = 0b0110)
```

Example: `5 ^ 3` results in `6` (binary `101 ^ 011` is `110`).

### 4. NOT (~)

Inverts all the bits.

```python
x = 5  # 0b0101

print(~x)  # Bitwise NOT: -6
```

Example: `~5` results in `-6` (binary `~00000101` is `11111010` in two's complement).

### 5. Left Shift (<<)

Shifts the bits to the left, adding zeros on the right.

```python
x = 5  # 0b0101

print(x << 1)  # Left shift: 10 (0b0101 << 1 = 0b1010)
```

Example: `5 << 1` results in `10` (binary `101` becomes `1010`).

### 6. Right Shift (>>)

Shifts the bits to the right, discarding bits shifted off.

```python
x = 5  # 0b0101

print(x >> 1)  # Right shift: 2 (0b0101 >> 1 = 0b0010)
```

Example: `5 >> 1` results in `2` (binary `101` becomes `010`).

---

## Practical Usage

Bitwise operations are useful for bit-level manipulations and optimizations.

### 1. Set Bit

```python
# Set bit at position pos
n |= (1 << pos)
```

### 2. Clear Bit

```python
# Clear bit at position pos
n &= ~(1 << pos)
```

### 3. Toggle Bit

```python
# Toggle bit at position pos
n ^= (1 << pos)
```

### 4. Check Bit

```python
# Check if bit at position pos is set
is_set = n & (1 << pos) != 0
```

### 5. Masking

```python
# Extract the lower 4 bits
lower_4_bits = n & 0b1111
```

---

## AND Examples

Bitwise AND with positive and negative integers.

### 1. Positive AND

What is the output?

```python
print(f"{10 & 5 = }")
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&1010_2&10_{10}\\
\text{b}&101_2&5_{10}\\\hline
\text{a \& b}&0_2&0_{10}\\
\end{array}$$

```python
print(f"{10 & 5 = }")  # Output: 10 & 5 = 0
```

### 2. Negative AND

What is the output?

```python
print(f"{10 & -5 = }")
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&1010_2&10_{10}\\
\text{5_{10} without sign bit}&101_2&5_{10}\\
\text{5_{10} with sign bit}&00101_2&5_{10}\\
\text{one's complement}&11010_2&\\
\text{b}&11011_2&-5_{10}\\
\hline
\text{a \& b}&01010_2&10_{10}\\
\end{array}$$

```python
print(f"{10 & -5 = }")  # Output: 10 & -5 = 10
```

---

## OR Examples

Bitwise OR with positive and negative integers.

### 1. Positive OR

What is the output?

```python
print(f"{10 | 5 = }")
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&1010_2&10_{10}\\
\text{b}&101_2&5_{10}\\\hline
\text{a | b}&1111_2&15_{10}\\
\end{array}$$

```python
print(f"{10 | 5 = }")  # Output: 10 | 5 = 15
```

### 2. Negative OR

What is the output?

```python
print(f"{10 | -5 = }")
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&1010_2&10_{10}\\
\text{b}&11011_2&-5_{10}\\
\hline
\text{a | b}&11011_2&-5_{10}\\
\end{array}$$

```python
print(f"{10 | -5 = }")  # Output: 10 | -5 = -5
```

---

## XOR Examples

Bitwise XOR with positive and negative integers.

### 1. Positive XOR

What is the output?

```python
print(f"{10 ^ 5 = }")
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&1010_2&10_{10}\\
\text{b}&101_2&5_{10}\\\hline
\text{a \^ b}&1111_2&15_{10}\\
\end{array}$$

```python
print(f"{10 ^ 5  = }")  # Output: 10 ^ 5 = 15
```

### 2. Negative XOR

What is the output?

```python
print(f"{10 ^ -5 = }")
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&1010_2&10_{10}\\
\text{b}&11011_2&-5_{10}\\\hline
\text{a \^ b}&10001_2&-15_{10}\\
\end{array}$$

```python
print(f"{10 ^ -5  = }")  # Output: 10 ^ -5 = -15
```

---

## NOT Examples

Bitwise NOT with different integer types.

### 1. Regular NOT

What is the output?

```python
print(f"{~ 10 = }")
```

**Solution:**

$$\begin{array}{ccr}
\text{Expression}&\text{Binary with Sign Bit}&\text{Decimal}\\
\text{a}&01010_2&10_{10}\\\hline
\text{~ a}&10101_2&-11_{10}\\
\end{array}$$

```python
print(f"{~ 10 = }")  # Output: ~ 10 = -11
```

### 2. NumPy uint8

What is the output?

```python
print(f"{~ np.array(10, dtype=np.uint8) = }")
```

**Solution:**

$$\begin{array}{ccr}
\text{Expression}&\text{Binary with np.uint8}&\text{Decimal}\\
\text{a}&00001010_2&10_{10}\\\hline
\text{~ a}&11110101_2&245_{10}\\
\end{array}$$

```python
print(f"{~ np.array(10, dtype=np.uint8) = }")  # Output: 245
```

### 3. NumPy uint16

What is the output?

```python
print(f"{~ np.array(10, dtype=np.uint16) = }")
```

**Solution:**

$$\begin{array}{ccr}
\text{Expression}&\text{Binary with np.uint16}&\text{Decimal}\\
\text{a}&0000000000001010_2&10_{10}\\\hline
\text{~ a}&1111111111110101_2&65525_{10}\\
\end{array}$$

```python
print(f"{~ np.array(10, dtype=np.uint16) = }")  # Output: 65525
```

---

## Right Shift

Right shift discards bits shifted off the right end.

### 1. Positive Shift

What is the output?

```python
print(5 >> 1)
print(5 >> 2)
print(5 >> 3)
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&101_2&5_{10}\\
\hline
\text{a >> 1}&10_2&2_{10}\\
\text{a >> 2}&1_2&1_{10}\\
\text{a >> 3}&0_2&0_{10}\\
\end{array}$$

```python
print(5 >> 1)  # Output: 2
print(5 >> 2)  # Output: 1
print(5 >> 3)  # Output: 0
```

### 2. Negative Shift

What is the output?

```python
print(-5 >> 1)
print(-5 >> 2)
print(-5 >> 3)
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&11011_2&-5_{10}\\
\hline
\text{a >> 1}&11101_2&-3_{10}\\
\text{a >> 2}&11110_2&-2_{10}\\
\text{a >> 3}&11111_2&-1_{10}\\
\end{array}$$

```python
print(-5 >> 1)  # Output: -3
print(-5 >> 2)  # Output: -2
print(-5 >> 3)  # Output: -1
```

---

## Left Shift

Left shift adds zeros on the right, effectively multiplying by powers of 2.

### 1. Positive Shift

What is the output?

```python
print(5 << 1)
print(5 << 2)
print(5 << 3)
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&101_2&5_{10}\\
\hline
\text{a << 1}&1010_2&10_{10}\\
\text{a << 2}&10100_2&20_{10}\\
\text{a << 3}&101000_2&40_{10}\\
\end{array}$$

```python
print(5 << 1)  # Output: 10
print(5 << 2)  # Output: 20
print(5 << 3)  # Output: 40
```

### 2. Negative Shift

What is the output?

```python
print(-5 << 1)
print(-5 << 2)
print(-5 << 3)
```

**Solution:**

$$\begin{array}{crr}
\text{Expression}&\text{Binary}&\text{Decimal}\\
\text{a}&11011_2&-5_{10}\\
\hline
\text{a << 1}&110110_2&-10_{10}\\
\text{a << 2}&1101100_2&-20_{10}\\
\text{a << 3}&11011000_2&-30_{10}\\
\end{array}$$

```python
print(-5 << 1)  # Output: -10
print(-5 << 2)  # Output: -20
print(-5 << 3)  # Output: -30
```

---

## Practical Examples

Real-world applications of bitwise operations.

### 1. Array Sizing

```python
def main():
    for n in range(4):
        memo = [-1] * (1 << (n+1))
        print(memo)

if __name__ == "__main__":
    main()
```

### 2. XOR Swap

Swap two variables without a temporary variable.

What is the output?

```python
a = 4
b = 3
print(f"{a = }, {b = }")

a = a ^ b
b = a ^ b
a = a ^ b
print(f"{a = }, {b = }")
```

**Solution:**

```python
def main():
    a = 4
    b = 3
    print(f"{a = }, {b = }")

    a = a ^ b
    b = a ^ b
    a = a ^ b
    print(f"{a = }, {b = }")

if __name__ == "__main__":
    main()
```

### 3. Count Bits

Count the number of bits in an integer.

What is the output?

```python
def func(num):
    count = 0
    while num:
        count += 1
        num >>= 1
    return count

def main():
    print(f"{func(435)}")

if __name__ == "__main__":
    main()   
```

**Solution:**

```python
def func(num):
    count = 0
    while num:
        count += 1
        num >>= 1
    return count

def main():
    print(f"{func(435)}")  # Output: 9

if __name__ == "__main__":
    main()
```

---

## Conclusion

Understanding bitwise operations is essential for low-level programming, optimizing performance, and working with hardware and embedded systems. These operations provide efficient ways to manipulate individual bits for tasks like setting flags, masking, and performing fast arithmetic.


---

## Exercises


**Exercise 1.**
Write a function `is_power_of_two(n)` that uses bitwise operations to check whether a positive integer is a power of two. Hint: a power of two has exactly one bit set.

??? success "Solution to Exercise 1"

    ```python
    def is_power_of_two(n):
        return n > 0 and (n & (n - 1)) == 0

    print(is_power_of_two(1))    # True  (2^0)
    print(is_power_of_two(16))   # True  (2^4)
    print(is_power_of_two(18))   # False
    print(is_power_of_two(1024)) # True  (2^10)
    ```

    A power of two in binary is `100...0`. Subtracting 1 flips all bits below the set bit to `011...1`. The AND of these two values is zero only for powers of two.

---

**Exercise 2.**
Without using multiplication, write a function `multiply_by_eight(n)` that multiplies an integer by 8 using only bitwise shift operators.

??? success "Solution to Exercise 2"

    ```python
    def multiply_by_eight(n):
        return n << 3

    print(multiply_by_eight(5))   # 40
    print(multiply_by_eight(10))  # 80
    print(multiply_by_eight(-3))  # -24
    ```

    Left-shifting by `k` positions multiplies by `2^k`. Shifting by 3 multiplies by `2^3 = 8`.

---

**Exercise 3.**
Write a function `swap_bits(n, i, j)` that swaps the bits at positions `i` and `j` in the integer `n`. Test with `n = 0b1010`, `i = 1`, `j = 3`.

??? success "Solution to Exercise 3"

    ```python
    def swap_bits(n, i, j):
        # Extract bits at positions i and j
        bit_i = (n >> i) & 1
        bit_j = (n >> j) & 1
        # If bits differ, flip both using XOR
        if bit_i != bit_j:
            n ^= (1 << i) | (1 << j)
        return n

    result = swap_bits(0b1010, 1, 3)
    print(f"{result:#06b}")  # 0b0010 -> 0b0010
    print(result)            # 2
    ```

    If the two bits are different, XOR with a mask that has 1s at both positions flips them, effectively swapping. If they are the same, no change is needed.
