# Storage & Two's Complement

Understanding how integers are stored in memory and how negative numbers are represented.

!!! tip "Mental Model"
    Python integers have unlimited precision -- they grow as needed. But hardware (and C) uses fixed-width two's complement, where flipping all bits and adding one turns a positive number into its negative. Understanding this fixed-width encoding explains overflow, bitwise operator behavior, and why Python must simulate it for negative numbers.

---

## Python Storage

Python integers are stored differently from languages like C.

### 1. Dynamic Typing

Python integers are dynamically typed with no fixed size.

### 2. Arbitrary Precision

Python's `int` type uses a variable-length structure (Big Integer implementation).

### 3. Memory Structure

Python's integer contains:

- Reference count
- Type information
- Actual integer value

In CPython, an `int` is represented as a C struct:

```c
struct _longobject {
    PyObject_VAR_HEAD
    digit ob_digit[1];
};
```

- `PyObject_VAR_HEAD`: Metadata (reference count, type)
- `ob_digit`: Array storing the actual value

---

## C Storage

C integers use fixed-size storage.

### 1. Static Typing

`int` in C is of fixed size, typically **4 bytes (32-bit)** or **8 bytes (64-bit)**.

### 2. Raw Memory

Stored directly in memory without extra overhead.

### 3. C Example

```c
int a = 10; // Typically occupies 4 bytes in memory
```

Stored as binary: `00000000 00000000 00000000 00001010`

---

## Key Differences

Comparison of Python and C integer implementations.

### 1. Comparison Table

| Feature           | Python `int`  | C `int` |
|------------------|--------------|---------|
| **Typing** | Dynamically typed | Statically typed |
| **Size** | Variable-length (arbitrary precision) | Fixed-length (e.g., 4 bytes) |
| **Storage** | Heap-allocated with metadata | Stack/heap-allocated as raw binary |
| **Performance** | Slower due to dynamic handling | Faster due to direct operations |
| **Overflow Handling** | No overflow (can grow infinitely) | Can overflow (limited by size) |
| **Memory Usage** | More overhead (object structure) | Minimal overhead |

### 2. Memory Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys

# Define a range of large integer values
large_int_values = [10**i for i in range(1, 20)]

# Memory usage for Python int (variable size)
large_python_memory_usage = [sys.getsizeof(i) for i in large_int_values]

# Memory usage for C int (assuming 4 bytes)
large_c_memory_usage = [4] * len(large_int_values)

# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 5))

# Plot memory usage
ax.plot(large_int_values, large_c_memory_usage, label="C int (4 bytes)", marker="o", linestyle="--")
ax.plot(large_int_values, large_python_memory_usage, label="Python int (variable size)", marker="s", linestyle="-")

# Set log scale for x-axis only
ax.set_xscale("log")

# Set linear scale for y-axis
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_formatter(ticker.ScalarFormatter())

# Labels and title
ax.set_xlabel("Integer Value")
ax.set_ylabel("Memory Usage (bytes)")
ax.set_title("Memory Usage of int in Python vs. C")

ax.set_ylim( (0, 38) )
ax.legend()

plt.show()
```

---

## Consequences

Understanding the practical implications of these differences.

### 1. Performance Overhead

Python's `int` operations are slower because they involve:

- Memory allocation
- Reference counting
- Dynamic type checking

### 2. Overflow Safety

**Python:** Avoids overflow by automatically expanding size.

```python
a = 2147483647
b = a + 1
print(b)  # No overflow, outputs 2147483648
```

**C:** Fixed size can cause overflow.

```c
#include <stdio.h>

int main() {
    int a = 2147483647; // Maximum 32-bit int
    int b = a + 1; // Causes overflow
    printf("%d\n", b); // Undefined behavior
    return 0;
}
```

### 3. Memory Usage

- **C** is much more memory-efficient (stores only the raw value)
- **Python** requires more memory due to object overhead

### 4. Use Cases

- **C**: Performance-critical applications (system programming, embedded systems)
- **Python**: Large numbers, dynamic typing beneficial (scientific computing, cryptography)

---

## Two's Complement

Two's complement is the standard method for representing signed integers in binary.

### 1. Definition

In an **N-bit** system:

- **Most significant bit (MSB)** is the sign bit:
  - `0` = positive
  - `1` = negative
- Positive numbers: standard binary
- Negative numbers: invert all bits and add 1

### 2. Example (8-bit)

**Positive Number (5):**

```
00000101  (Binary for 5)
```

**Negative Number (-5):**

1. Binary of `5`: `00000101`
2. Invert bits: `11111010`
3. Add `1`: `11111011`

Thus, `11111011` represents `-5` in two's complement.

### 3. Logic Behind MSB

The MSB contributes a large negative weight.

In 8-bit:

- MSB in `11111011` has weight `-128`
- Remaining bits: `64 + 32 + 16 + 8 + 2 + 1 = 123`
- Total: `-128 + 123 = -5`

### 4. Range (N-bit)

For an N-bit system:

$$
-2^{(N-1)} \text{ to } 2^{(N-1)} - 1
$$

For 8-bit:

$$
-128 \text{ to } 127
$$

---

## Python Representation

Python does not use two's complement internally.

### 1. Sign-Magnitude

Python uses sign-magnitude with arbitrary-length representation, not two's complement.

### 2. Comparison

| Feature | Two's Complement | Python's Integer |
|---------|----------------|--------------------|
| Fixed Bit-Length | Yes (e.g., 8-bit, 16-bit) | No (arbitrary precision) |
| Negative Representation | MSB indicates sign, bitwise inversion + 1 | Sign-magnitude with arbitrary-length |
| Overflow | Yes (limited by bit-width) | No (expands dynamically) |
| Arithmetic Simplicity | Simple addition/subtraction | Slightly more overhead |

### 3. Does Python Use Two's Complement?

**Answer:** No, Python does not use two's complement for representing negative integers. Python uses a sign-magnitude representation.

**Sign-magnitude representation:**

- Leftmost bit indicates sign: `0` for positive, `1` for negative
- Remaining bits represent the magnitude

Example with 8-bit integers:

- Positive 5: `00000101`
- Negative 5: `10000101`

**Two's complement (used in C/C++):**

- Negative numbers are represented by inverting bits and adding 1
- Simplifies arithmetic operations
- No separate sign bit needed

Python's approach maintains human-readability and avoids hardware-level complexities, though two's complement remains crucial for low-level systems.

[ChatGPT](https://openai.com/blog/chatgpt)

---

## Pros and Cons

Evaluating the trade-offs of each representation.

### 1. Two's Complement

**Pros:**

- Simple arithmetic operations
- Efficient in hardware with fixed bit-width
- Single representation for zero

**Cons:**

- Overflow issues due to fixed bit-width
- Limited range of values

### 2. Python's Approach

**Pros:**

- No overflow due to dynamic sizing
- Handles very large numbers

**Cons:**

- Slightly higher memory usage
- More computational overhead

---

## Conclusion

**C `int`** is faster and memory-efficient but suffers from fixed size and overflow issues.

**Python `int`** is slower and consumes more memory but is safe from overflow and supports arbitrary precision.

**Trade-off:** C is better for efficiency, while Python is better for flexibility and safety.

Two's complement remains crucial for low-level systems and embedded computing, while Python's approach is advantageous for applications requiring precision without fixed bit-width constraints.

---

## Exercises

**Exercise 1.**
Python integers have no fixed size, so they never overflow. Predict the output:

```python
import sys

a = 2 ** 63 - 1
b = a + 1
print(b)
print(type(b))
print(sys.getsizeof(a))
print(sys.getsizeof(b))
print(sys.getsizeof(2 ** 1000))
```

Why does `sys.getsizeof` return different values for `a` and `b`? How does Python's memory layout for integers differ from C's fixed 4-byte or 8-byte representation?

??? success "Solution to Exercise 1"
    Output (sizes may vary by platform):

    ```text
    9223372036854775808
    <class 'int'>
    36
    36
    172
    ```

    (Exact `getsizeof` values depend on CPython version and platform, but `b` will be equal to or larger than `a`, and `2 ** 1000` will be much larger.)

    Python integers are objects with a variable-length array of "digits" (30-bit or 15-bit chunks in CPython). When a number exceeds the capacity of the current digit array, Python allocates more digits. The `getsizeof` reflects the object header (reference count, type pointer) plus the digit array.

    C stores integers in a fixed number of bytes (typically 4 or 8), regardless of the value. Python trades memory efficiency and speed for the guarantee that integers never overflow and can grow to arbitrary size.

---

**Exercise 2.**
Python simulates two's complement for bitwise operations on negative numbers. Predict the output:

```python
print(bin(5))
print(bin(-5))
print(bin(~5))

print(-5 & 0xFF)
print(bin(-5 & 0xFF))
```

Why does `bin(-5)` show `-0b101` instead of the two's complement bit pattern? Why does `-5 & 0xFF` give `251`? What is Python doing internally to make bitwise operations on negative numbers consistent with two's complement?

??? success "Solution to Exercise 2"
    Output:

    ```text
    0b101
    -0b101
    -0b110
    251
    0b11111011
    ```

    `bin(-5)` shows `-0b101` because Python displays negative integers with a minus sign followed by the magnitude in binary. Internally, Python uses sign-magnitude, not two's complement.

    However, for **bitwise operations**, Python behaves **as if** negative numbers are stored in two's complement with infinite width. `-5` is treated as `...11111011` (infinite leading 1s). When you mask with `0xFF`, you extract the low 8 bits: `11111011` = 251.

    `~5` (bitwise NOT) gives `-6` because in infinite-width two's complement, flipping all bits of `...00000101` gives `...11111010` = -6.

    Python maintains two's complement semantics for bitwise operations while using sign-magnitude for storage -- a design choice that gives correct low-level behavior without fixed bit widths.

---

**Exercise 3.**
In C, signed integer overflow is undefined behavior. Predict what happens in Python vs. what would happen in a 32-bit C `int`:

```python
# Python
a = 2147483647  # 2^31 - 1 (max 32-bit signed int)
b = a + 1
c = a * a
print(b)
print(c)
print(len(str(c)))
```

Why does Python handle this correctly while C produces undefined behavior? What is the trade-off Python makes for this safety?

??? success "Solution to Exercise 3"
    Output:

    ```text
    2147483648
    4611686014132420609
    19
    ```

    Python produces mathematically correct results because its integers automatically expand. `b` = 2^31, which exceeds the 32-bit signed range but is perfectly representable in Python. `c` = (2^31 - 1)^2, a 19-digit number.

    In C with 32-bit signed `int`, `a + 1` would overflow. The C standard says signed integer overflow is **undefined behavior** -- the compiler can produce any result, crash, or even optimize away code that depends on overflow. In practice, most systems using two's complement would wrap to `-2147483648`, but this is not guaranteed.

    The trade-off: Python pays for this safety with slower arithmetic (every operation must check for potential reallocation) and higher memory usage (object overhead per integer). C gets raw speed by operating directly on fixed-size hardware registers.
