

# Bits and Bytes

!!! tip "Mental Model"
    A bit is a single yes-or-no answer; a byte is a group of eight such answers bundled together. Every piece of data a computer handles -- numbers, text, images, programs -- is just a pattern of bits given meaning by context. Understanding bits and bytes is understanding the alphabet that all digital information is written in.

All information in a computer—numbers, text, images, sound, and programs—is ultimately represented as patterns of **bits**. To understand how computers store and process information, we begin with the most basic building blocks: **bits** and **bytes**.

This section explains what bits and bytes are, how binary numbers work, how negative integers are represented, how bitwise operations manipulate data, and how multi-byte values are laid out in memory.

---

## 1. Bits: the smallest unit of digital information

A **bit** (*binary digit*) is the smallest unit of information in a digital system. A bit has only two possible values:

```text
0 or 1
```

Those two values correspond to two reliably distinguishable physical states in hardware, such as low vs. high voltage, off vs. on, or absence vs. presence of magnetization.

The key idea is simple:

> computers work with physical systems that can reliably distinguish between two states, so information is encoded in binary.

### Visual intuition

```mermaid
flowchart LR
    A[Physical state A] --> B[Bit 0]
    C[Physical state B] --> D[Bit 1]
```

A single bit carries very little information, but many bits together can represent rich and complex data.

---

## 2. Bytes: groups of 8 bits

A **byte** is a group of **8 bits**.

```text
1 byte = 8 bits
```

Since each bit can be either 0 or 1, a byte can represent:

[
2^8 = 256
]

distinct patterns.

So an unsigned byte can store values from:

```text
0 to 255
```

### Why 8 bits?

The 8-bit byte became standard largely through the influence of **IBM System/360 (1964)**. Earlier machines used other sizes such as 6-bit or 9-bit units, but 8 bits proved especially practical because it:

* fits naturally with powers of two
* works well for memory addressing
* provides enough patterns for small integers and character encodings
* aligns neatly with hexadecimal notation

Most modern general-purpose computers are **byte-addressable**, meaning each memory address refers to one byte.

### Byte as a container

```mermaid
flowchart LR
    b7[bit 7] --> BYTE[1 byte]
    b6[bit 6] --> BYTE
    b5[bit 5] --> BYTE
    b4[bit 4] --> BYTE
    b3[bit 3] --> BYTE
    b2[bit 2] --> BYTE
    b1[bit 1] --> BYTE
    b0[bit 0] --> BYTE
```

---

## 3. Binary numbers

A byte is not just a sequence of symbols. Each bit position has a **place value**.

For an 8-bit number:

| Bit position |   7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
| ------------ | --: | -: | -: | -: | -: | -: | -: | -: |
| Value        | 128 | 64 | 32 | 16 |  8 |  4 |  2 |  1 |

The rightmost bit is the **least significant bit (LSB)**.
The leftmost bit is the **most significant bit (MSB)**.

### Example: interpreting a byte

Consider:

```text
10110110
```

This means:

[
1\cdot128 + 0\cdot64 + 1\cdot32 + 1\cdot16 + 0\cdot8 + 1\cdot4 + 1\cdot2 + 0\cdot1
]

[
= 128 + 32 + 16 + 4 + 2 = 182
]

### Visualization

```mermaid
flowchart TD
    A["10110110"] --> B["1×128"]
    A --> C["0×64"]
    A --> D["1×32"]
    A --> E["1×16"]
    A --> F["0×8"]
    A --> G["1×4"]
    A --> H["1×2"]
    A --> I["0×1"]
    B --> J["182"]
    C --> J
    D --> J
    E --> J
    F --> J
    G --> J
    H --> J
    I --> J
```

### Another example

```text
00101101
```

[
0\cdot128 + 0\cdot64 + 1\cdot32 + 0\cdot16 + 1\cdot8 + 1\cdot4 + 0\cdot2 + 1\cdot1
]

[
= 32 + 8 + 4 + 1 = 45
]

---

## 4. From binary to hexadecimal

Binary is fundamental, but long binary strings are hard to read. **Hexadecimal** provides a compact way to write bit patterns.

Each hexadecimal digit corresponds to **4 bits**:

| Binary | Hex |
| ------ | --- |
| 0000   | 0   |
| 0001   | 1   |
| 0010   | 2   |
| 0011   | 3   |
| 0100   | 4   |
| 0101   | 5   |
| 0110   | 6   |
| 0111   | 7   |
| 1000   | 8   |
| 1001   | 9   |
| 1010   | A   |
| 1011   | B   |
| 1100   | C   |
| 1101   | D   |
| 1110   | E   |
| 1111   | F   |

Since a byte has 8 bits, one byte equals **two hexadecimal digits**.

Example:

```text
10110110 = B6
```

because:

```text
1011 = B
0110 = 6
```

### Visualization

```mermaid
flowchart LR
    A["10110110"] --> B["1011"]
    A --> C["0110"]
    B --> D["B"]
    C --> E["6"]
    D --> F["B6"]
    E --> F
```

Hexadecimal is widely used in systems programming, debugging, memory inspection, and networking because it is much shorter than binary while still closely matching bit structure.

---

## 5. Unsigned and signed integers

So far, we have treated a byte as an **unsigned** quantity, meaning all 256 patterns represent nonnegative values:

[
0 \text{ to } 255
]

But computers must also represent **negative integers**.

### 5.1 Unsigned integers

With (n) bits, an unsigned integer can represent:

[
0 \text{ to } 2^n - 1
]

For 8 bits:

[
0 \text{ to } 255
]

---

## 5.2 Signed integers and two’s complement

Most modern systems represent signed integers using **two’s complement**.

For an 8-bit signed integer, the range is:

[
-128 \text{ to } 127
]

### Why two’s complement?

It has a major engineering advantage:

> addition and subtraction can be implemented using the same underlying binary hardware.

### Examples

| Binary   | Value |
| -------- | ----: |
| 00000000 |     0 |
| 00000001 |     1 |
| 00000010 |     2 |
| 01111111 |   127 |
| 10000000 |  -128 |
| 11111111 |    -1 |
| 11111110 |    -2 |

### Intuition

In two’s complement:

* positive numbers look mostly familiar
* negative numbers occupy the upper half of the bit-pattern space
* the MSB contributes a negative weight

For 8 bits, the place values are effectively:

| Bit position |    7 |  6 |  5 |  4 |  3 |  2 |  1 |  0 |
| ------------ | ---: | -: | -: | -: | -: | -: | -: | -: |
| Value        | -128 | 64 | 32 | 16 |  8 |  4 |  2 |  1 |

So:

```text
11111111
```

means:

[
-128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = -1
]

### How to form the negative of a number

A common rule for fixed-width two’s complement is:

1. write the positive number in binary
2. flip all bits
3. add 1

Example: represent (-5) in 8 bits.

```text
  5  = 00000101
flip = 11111010
+ 1  = 11111011
```

So:

```text
-5 = 11111011
```

### Visualization

```mermaid
flowchart TD
    A["+5 = 00000101"] --> B["flip bits"]
    B --> C["11111010"]
    C --> D["+1"]
    D --> E["11111011 = -5"]
```

---

## 6. Binary arithmetic

Binary arithmetic follows the same structural rules as decimal arithmetic, but each digit is either 0 or 1.

---

### 6.1 Binary addition

The basic addition rules are:

```text
0 + 0 = 0
0 + 1 = 1
1 + 0 = 1
1 + 1 = 10   (write 0, carry 1)
```

#### Example: (5 + 3)

```text
  0101
+ 0011
------
  1000
```

This equals:

[
5 + 3 = 8
]

### Visualization of carries

```mermaid
flowchart TB
    A["0101"] --> C["add bit by bit"]
    B["0011"] --> C
    C --> D["1+1 creates carry"]
    D --> E["1000"]
```

---

### 6.2 Another addition example

```text
  0110   (6)
+ 0101   (5)
------
  1011   (11)
```

Column by column:

* (0 + 1 = 1)
* (1 + 0 = 1)
* (1 + 1 = 10): write 0, carry 1
* (0 + 0 + 1 = 1)

---

### 6.3 Binary subtraction

Binary subtraction also uses borrowing, but in real hardware subtraction is often implemented as:

[
a - b = a + (-b)
]

That is, subtraction can be performed by adding the two’s complement of the subtrahend.

#### Example: (7 - 3)

```text
  0111   (7)
- 0011   (3)
------
  0100   (4)
```

#### Using two’s complement

```text
3      = 00000011
flip   = 11111100
+1     = 11111101   (-3)

7      = 00000111
-3     = 11111101
----------------
sum    = 00000100   (ignore carry out)
```

### Visualization

```mermaid
flowchart TD
    A["3 = 00000011"] --> B["flip bits"]
    B --> C["11111100"]
    C --> D["+1"]
    D --> E["11111101 = -3"]
    E --> F["add to 7"]
    G["7 = 00000111"] --> F
    F --> H["00000100 = 4"]
```

---

## 7. Overflow in fixed-width arithmetic

Real machine integers have a fixed width: 8 bits, 16 bits, 32 bits, 64 bits, and so on. This means there is a maximum and minimum representable value.

When a computation exceeds that range, **overflow** occurs.

### Unsigned overflow example

With 8-bit unsigned integers:

```text
255 = 11111111
```

Now add 1:

```text
  11111111
+ 00000001
----------
1 00000000
```

If only 8 bits are kept, the leading carry is discarded:

```text
00000000
```

So the result wraps around from 255 to 0.

### Signed overflow example

For 8-bit signed integers:

```text
  01111111   (127)
+ 00000001   (1)
----------
  10000000   (-128 in two's complement)
```

The bit pattern is valid, but the mathematical result (128) is outside the representable range. This is signed overflow.

### Visualization

```mermaid
flowchart LR
    A["01111111 (127)"] --> B["+ 1"]
    B --> C["10000000"]
    C --> D["bit pattern valid"]
    D --> E["mathematical overflow"]
```

---

## 8. Bitwise operations

A computer often needs to manipulate individual bits directly. This is the purpose of **bitwise operations**.

| Operation   | Symbol | Meaning                                 |                                          |
| ----------- | ------ | --------------------------------------- | ---------------------------------------- |
| AND         | `&`    | result bit is 1 only if both bits are 1 |                                          |
| OR          | `      | `                                       | result bit is 1 if at least one bit is 1 |
| XOR         | `^`    | result bit is 1 if the bits differ      |                                          |
| NOT         | `~`    | inverts each bit                        |                                          |
| left shift  | `<<`   | moves bits left                         |                                          |
| right shift | `>>`   | moves bits right                        |                                          |

---

### 8.1 AND

```text
  1100
& 1010
------
  1000
```

Only positions where both inputs are 1 remain 1.

---

### 8.2 OR

```text
  1100
| 1010
------
  1110
```

If either input has a 1, the result has a 1.

---

### 8.3 XOR

```text
  1100
^ 1010
------
  0110
```

A result bit is 1 when the two input bits are different.

XOR is useful for toggling bits, parity checks, and low-level algorithms.

---

### 8.4 NOT

For a fixed-width value, NOT flips every bit.

```text
~00001111 = 11110000
```

In Python, integers are not fixed-width, so `~x` behaves as:

[
\sim x = -(x+1)
]

because Python models integers as if they had infinite two’s-complement sign extension.

---

### 8.5 Shifts

A left shift moves all bits left:

```text
00000001 << 3 = 00001000
```

For unsigned integers, left shift by (n) positions corresponds to multiplication by (2^n), assuming no overflow.

A right shift moves bits right:

```text
00001000 >> 2 = 00000010
```

For nonnegative integers, right shift by (n) positions corresponds to integer division by (2^n).

### Shift visualization

```mermaid
flowchart LR
    A["00000001"] --> B["<< 1"]
    B --> C["00000010"]
    C --> D["<< 1"]
    D --> E["00000100"]
    E --> F["<< 1"]
    F --> G["00001000"]
```

---

## 9. Bitmasks and flags

A powerful use of bits is to store many boolean conditions inside one integer. This is called using **bit flags** or a **bitmask**.

Suppose we define:

```python
READ    = 0b100
WRITE   = 0b010
EXECUTE = 0b001
```

Then:

```python
perms = READ | WRITE   # 0b110
```

means the value stores both read and write permission.

### Common operations

Check whether a flag is present:

```python
bool(perms & READ)
```

Add a flag:

```python
perms |= EXECUTE
```

Remove a flag:

```python
perms &= ~WRITE
```

### Visualization

```mermaid
flowchart TD
    A["READ = 100"] --> D["permissions"]
    B["WRITE = 010"] --> D
    C["EXECUTE = 001"] --> D
    D --> E["110 means READ + WRITE"]
```

Bitmasks are common in operating systems, graphics APIs, networking code, file permissions, and embedded systems.

---

## 10. Endianness: byte order in memory

When a value uses more than one byte, the computer must decide how to arrange those bytes in memory.

This is called **endianness**.

Consider the 32-bit hexadecimal value:

```text
0x12345678
```

This occupies four bytes:

```text
12 34 56 78
```

But there are two possible memory orders.

### Big-endian

The **most significant byte** comes first.

```text
12 34 56 78
```

### Little-endian

The **least significant byte** comes first.

```text
78 56 34 12
```

### Memory-layout diagram

```mermaid
flowchart TB
    subgraph Big_endian
        A1["Address 0: 12"]
        A2["Address 1: 34"]
        A3["Address 2: 56"]
        A4["Address 3: 78"]
    end

    subgraph Little_endian
        B1["Address 0: 78"]
        B2["Address 1: 56"]
        B3["Address 2: 34"]
        B4["Address 3: 12"]
    end
```

Most modern desktop and mobile CPUs are little-endian. Network protocols traditionally use big-endian, which is why big-endian is often called **network byte order**.

### Why endianness matters

Endianness becomes important when:

* reading raw binary files
* sending data over networks
* working with memory dumps
* interfacing between different machines or languages
* using serialization formats

---

## 11. Bytes, words, and memory units

A **byte** is 8 bits, but computers also operate on larger chunks of data.

A **word** is the natural unit of data a CPU processes efficiently. On a 32-bit system, a word is often 32 bits. On a 64-bit system, it is often 64 bits.

Common sizes:

| Unit     | Size                       |
| -------- | -------------------------- |
| nibble   | 4 bits                     |
| byte     | 8 bits                     |
| word     | architecture-dependent     |
| kilobyte | roughly one thousand bytes |
| megabyte | roughly one million bytes  |
| gigabyte | roughly one billion bytes  |

### Decimal vs binary prefixes

There are two standards for storage units.

#### SI prefixes (decimal)

Used by drive manufacturers:

* 1 KB = 1000 bytes
* 1 MB = 1000 KB
* 1 GB = 1000 MB

#### IEC prefixes (binary)

Used in many operating-system contexts:

* 1 KiB = 1024 bytes
* 1 MiB = 1024 KiB
* 1 GiB = 1024 MiB

This is why a “1 TB” drive may appear as about **931 GiB** when viewed by the operating system.

---

## 12. Python examples

These examples reinforce the concepts above.

### Bitwise operations

```python
a = 0b1100  # 12
b = 0b1010  # 10

print(a & b)       # 8
print(bin(a & b))  # 0b1000

print(a | b)       # 14
print(bin(a | b))  # 0b1110

print(a ^ b)       # 6
print(bin(a ^ b))  # 0b0110
```

### Shifting

```python
print(1 << 3)        # 8
print(bin(1 << 3))   # 0b1000

print(8 >> 2)        # 2
print(bin(8 >> 2))   # 0b10
```

### Endianness

```python
import sys

print(sys.byteorder)  # often 'little'

x = 0x12345678
print(x.to_bytes(4, "big"))     # b'\x12\x34\x56\x78'
print(x.to_bytes(4, "little"))  # b'\x78\x56\x34\x12'
```

### Bit flags

```python
READ    = 0b100
WRITE   = 0b010
EXECUTE = 0b001

perms = READ | WRITE
print(bin(perms))               # 0b110

print(bool(perms & READ))       # True
print(bool(perms & EXECUTE))    # False

perms |= EXECUTE
print(bin(perms))               # 0b111

perms &= ~WRITE
print(bin(perms))               # 0b101
```

---

## 13. Worked examples

### Worked Example 1: convert binary to decimal

Convert `11010101` to decimal.

[
1\cdot128 + 1\cdot64 + 0\cdot32 + 1\cdot16 + 0\cdot8 + 1\cdot4 + 0\cdot2 + 1\cdot1
]

[
= 128 + 64 + 16 + 4 + 1 = 213
]

---

### Worked Example 2: convert decimal to binary

Convert (45) to binary.

Break 45 into powers of two:

[
45 = 32 + 8 + 4 + 1
]

So the bits for (32, 8, 4,) and (1) are 1:

```text
00101101
```

---

### Worked Example 3: interpret a signed 8-bit value

Interpret `11111011` as a signed 8-bit integer.

Use two’s complement weights:

[
-128 + 64 + 32 + 16 + 8 + 0 + 2 + 1 = -5
]

So:

```text
11111011 = -5
```

---

## 14. Common pitfalls

### Confusing bits and bytes

A byte is not one bit. A byte contains **8 bits**.

### Assuming all large storage units are powers of 1024

Manufacturers typically use powers of 1000, while operating systems often display powers of 1024.

### Forgetting fixed width

Bitwise reasoning often depends on how many bits are being used. `11111111` can mean 255 as an unsigned value or -1 as an 8-bit signed value.

### Ignoring endianness

A multi-byte value has no single memory layout without specifying byte order.

### Overgeneralizing shifts

Left shift behaves like multiplication by (2^n) only when overflow is not an issue.

---

## 15. Exercises

### Concept checks

1. How many distinct values can be represented with 12 bits?
2. What decimal value does `00110110` represent?
3. Write 91 in 8-bit binary.
4. Convert `11110000` to hexadecimal.
5. What is the 8-bit two’s complement representation of `-3`?
6. Compute:

   * `0b1101 & 0b1011`
   * `0b1101 | 0b1011`
   * `0b1101 ^ 0b1011`
7. What value results from `1 << 5`?
8. On an 8-bit unsigned system, what happens when `255 + 1` is computed?
9. Why can `0x12345678` have two different byte layouts in memory?
10. Why does Python’s `~x` not simply “flip a fixed number of bits”?

---

### Practice problems

1. Convert `10101100` to decimal.
2. Convert 156 to 8-bit binary.
3. Convert `11001010` to hexadecimal.
4. Interpret `10000001` as:

   * an unsigned 8-bit integer
   * a signed 8-bit integer
5. Use two’s complement to represent `-18` in 8 bits.
6. Show the binary addition of 13 and 6.
7. Show the binary subtraction of 9 and 4 using two’s complement.
8. A permission system uses:

   * READ = `0b1000`
   * WRITE = `0b0100`
   * EXECUTE = `0b0010`
   * DELETE = `0b0001`

   If a file has permissions `0b1101`:

   * which permissions are enabled?
   * how would you remove WRITE?
   * how would you test EXECUTE?

---

## 16. Short answers

### Concept checks

1. (2^{12} = 4096)
2. 54
3. `01011011`
4. `F0`
5. `11111101`
6. * `1001`
   * `1111`
   * `0110`
7. 32
8. It wraps to 0 if only 8 bits are kept.
9. Because endianness determines byte order.
10. Because Python integers are not fixed-width.

---

## 17. Looking ahead

Bits and bytes are only the beginning of data representation. Once these ideas are clear, the next natural questions are:

* How are larger integers represented?
* How are floating-point numbers stored?
* How are characters encoded as bytes?
* How are images and sound reduced to binary data?
* How do programs and machine instructions become bit patterns?

Those topics build directly on the ideas introduced here: place value, fixed-width representation, bit manipulation, and memory layout.

---


## 18. Summary

* A **bit** is the smallest unit of digital information and has value 0 or 1.
* A **byte** is 8 bits and can represent 256 distinct patterns.
* Binary numbers use powers of two for place value.
* Hexadecimal provides a compact notation for binary data.
* Signed integers are usually represented with **two’s complement**.
* Binary arithmetic follows the same structural rules as decimal arithmetic, but with base 2.
* **Overflow** occurs when a value exceeds the range of a fixed-width representation.
* **Bitwise operations** manipulate individual bits efficiently.
* **Bitmasks** store multiple boolean flags inside a single integer.
* **Endianness** determines byte order in multi-byte memory representations.

A solid understanding of bits and bytes is the foundation for understanding data types, memory, machine arithmetic, and low-level programming.


## Exercises

**Exercise 1.**
Write a Python function `twos_complement(value, bits)` that takes a signed integer and a bit width and returns the two's complement binary string (zero-padded to the specified width). Test it with `twos_complement(-42, 8)`, `twos_complement(42, 8)`, and `twos_complement(-1, 16)`. Verify your results by converting back using the two's complement weight formula.

??? success "Solution to Exercise 1"
    ```python
    def twos_complement(value, bits):
        if value >= 0:
            return format(value, f'0{bits}b')
        else:
            # Two's complement: (2^bits) + value
            unsigned = (1 << bits) + value
            return format(unsigned, f'0{bits}b')

    # Tests
    tests = [(-42, 8), (42, 8), (-1, 16)]
    for val, bits in tests:
        binary = twos_complement(val, bits)
        print(f"twos_complement({val:>4}, {bits:>2}) = {binary}")

    # Verification: convert 11010110 back to signed 8-bit
    # MSB weight is -128
    b = "11010110"
    weights = [-128, 64, 32, 16, 8, 4, 2, 1]
    result = sum(int(bit) * w for bit, w in zip(b, weights))
    print(f"Verify {b} = {result}")  # should be -42
    ```

    Output:

    ```text
    twos_complement( -42,  8) = 11010110
    twos_complement(  42,  8) = 00101010
    twos_complement(  -1, 16) = 1111111111111111
    Verify 11010110 = -42
    ```

---

**Exercise 2.**
Write a Python script that demonstrates endianness by storing the 32-bit integer `0xDEADBEEF` in both big-endian and little-endian byte order using `int.to_bytes()`. Print the resulting byte sequences in hexadecimal. Then read them back using `int.from_bytes()` and verify that the original value is recovered.

??? success "Solution to Exercise 2"
    ```python
    value = 0xDEADBEEF

    big = value.to_bytes(4, byteorder="big")
    little = value.to_bytes(4, byteorder="little")

    print(f"Original:     0x{value:08X}")
    print(f"Big-endian:   {big.hex(' ')}")
    print(f"Little-endian: {little.hex(' ')}")

    # Read back
    recovered_big = int.from_bytes(big, byteorder="big")
    recovered_little = int.from_bytes(little, byteorder="little")

    print(f"Recovered (big):    0x{recovered_big:08X}")
    print(f"Recovered (little): 0x{recovered_little:08X}")
    print(f"Both match: {recovered_big == value == recovered_little}")
    ```

    Output:

    ```text
    Original:     0xDEADBEEF
    Big-endian:   de ad be ef
    Little-endian: ef be ad de
    Recovered (big):    0xDEADBEEF
    Recovered (little): 0xDEADBEEF
    Both match: True
    ```

---

**Exercise 3.**
Implement a simple permission system using bitmasks. Define four flags: `READ = 0b1000`, `WRITE = 0b0100`, `EXECUTE = 0b0010`, `DELETE = 0b0001`. Write functions `set_permission(perms, flag)`, `remove_permission(perms, flag)`, `has_permission(perms, flag)`, and `display_permissions(perms)` that prints the names of all active flags. Test by creating a permission value with READ and WRITE, then adding EXECUTE, then removing WRITE.

??? success "Solution to Exercise 3"
    ```python
    READ    = 0b1000
    WRITE   = 0b0100
    EXECUTE = 0b0010
    DELETE  = 0b0001

    FLAG_NAMES = {READ: "READ", WRITE: "WRITE",
                  EXECUTE: "EXECUTE", DELETE: "DELETE"}

    def set_permission(perms, flag):
        return perms | flag

    def remove_permission(perms, flag):
        return perms & ~flag

    def has_permission(perms, flag):
        return bool(perms & flag)

    def display_permissions(perms):
        active = [name for flag, name in FLAG_NAMES.items()
                  if has_permission(perms, flag)]
        print(f"  {bin(perms):>8} -> {', '.join(active)}")

    # Test
    perms = set_permission(0, READ)
    perms = set_permission(perms, WRITE)
    print("After setting READ and WRITE:")
    display_permissions(perms)

    perms = set_permission(perms, EXECUTE)
    print("After adding EXECUTE:")
    display_permissions(perms)

    perms = remove_permission(perms, WRITE)
    print("After removing WRITE:")
    display_permissions(perms)
    ```

    Output:

    ```text
    After setting READ and WRITE:
      0b1100 -> READ, WRITE
    After adding EXECUTE:
      0b1110 -> READ, WRITE, EXECUTE
    After removing WRITE:
      0b1010 -> READ, EXECUTE
    ```

---

**Exercise 4.**
Two's complement uses the same binary addition circuitry for both signed and unsigned integers. Explain why this is a profound engineering advantage. Specifically: if a CPU ALU has a single ADD instruction, why does two's complement allow it to work correctly regardless of whether the programmer interprets the bit pattern as signed or unsigned? Give a concrete 8-bit example where the same binary addition produces the correct result under both interpretations.

??? success "Solution to Exercise 4"
    Two's complement is designed so that binary addition modulo $2^n$ produces the correct result whether the operands are interpreted as signed or unsigned. This means the CPU needs only one ADD circuit -- it performs the same bit-level operation regardless of signedness.

    **8-bit example:** Consider adding 250 (unsigned) or -6 (signed, same bit pattern `11111010`) to 10 (`00001010`):

    ```
      11111010   (250 unsigned, or -6 signed)
    + 00001010   (10)
    ----------
    1 00000100   (result: 260 unsigned mod 256 = 4, or -6 + 10 = 4 signed)
    ```

    The carry out of bit 7 is discarded (modular arithmetic). The 8-bit result `00000100` = 4 is correct under **both** interpretations:

    - Unsigned: 250 + 10 = 260 mod 256 = 4
    - Signed: -6 + 10 = 4

    This works because two's complement defines $-x$ as $2^n - x$, so signed arithmetic is just unsigned arithmetic modulo $2^n$. The ALU does not need to know whether it is doing signed or unsigned addition -- the same circuit handles both. This halves the hardware complexity for addition and subtraction.

---

**Exercise 5.**
Python integers have arbitrary precision (no fixed bit width), while C and NumPy integers have fixed widths (8, 16, 32, or 64 bits). Explain what overflow means in the context of fixed-width arithmetic and why Python integers can never overflow. What is the trade-off? Why would anyone choose fixed-width integers if Python's arbitrary-precision integers are "safer"? Think in terms of memory layout, CPU instructions, and performance.

??? success "Solution to Exercise 5"
    **Overflow** in fixed-width arithmetic occurs when the mathematical result of an operation exceeds the range representable in the given number of bits. For 8-bit signed integers, the range is [-128, 127], so 127 + 1 wraps to -128.

    Python integers cannot overflow because they have no fixed bit width. Python's `int` internally stores the number using as many machine words as needed, dynamically allocating more memory for larger values. `2 ** 1000` works correctly because Python allocates enough memory to hold all the digits.

    **The trade-off:**

    1. **Memory**: A Python integer `42` uses 28 bytes (object header, reference count, type pointer, value). A C `int32` uses 4 bytes. A NumPy array of 1 million `int64` values uses 8 MB; a Python list of 1 million integers uses ~28 MB (plus 8 MB for the pointer array).

    2. **CPU instructions**: Fixed-width integers map directly to CPU hardware. `a + b` for two `int64` values is one machine instruction (`ADD`). For Python integers, `a + b` requires type checking, method dispatch, multi-word arithmetic if the numbers are large, and memory allocation for the result.

    3. **SIMD**: Fixed-width integers enable vectorized operations (one instruction adding 4 or 8 integers at once). Python's variable-width integers cannot be packed into SIMD registers.

    Fixed-width integers are chosen when maximum performance is needed and the programmer can guarantee values stay within range. Python's arbitrary-precision integers are chosen when correctness and convenience matter more than raw speed.

---

**Exercise 6.**
Bitwise operations like AND, OR, XOR, and shift work on individual bits. Explain why `x << 1` is equivalent to multiplying `x` by 2, and `x >> 1` is equivalent to integer division by 2 (for non-negative `x`). Use the positional value system ($d_i \cdot 2^i$) to prove this algebraically. Then explain why right-shifting a negative two's complement number is more subtle than simply dividing by 2 -- what is "arithmetic shift" versus "logical shift"?

??? success "Solution to Exercise 6"
    A binary number is represented as:

    $$
    x = d_{n-1} \cdot 2^{n-1} + d_{n-2} \cdot 2^{n-2} + \cdots + d_1 \cdot 2^1 + d_0 \cdot 2^0
    $$

    **Left shift** (`x << 1`): Each bit $d_i$ moves to position $i+1$, and a 0 is inserted at position 0:

    $$
    x \ll 1 = d_{n-1} \cdot 2^n + d_{n-2} \cdot 2^{n-1} + \cdots + d_0 \cdot 2^1 + 0 \cdot 2^0 = 2x
    $$

    Every term is multiplied by 2, so the result is $2x$.

    **Right shift** (`x >> 1`): Each bit $d_i$ moves to position $i-1$, and the lowest bit $d_0$ is discarded:

    $$
    x \gg 1 = d_{n-1} \cdot 2^{n-2} + \cdots + d_1 \cdot 2^0 = \lfloor x/2 \rfloor
    $$

    Every term is divided by 2, giving $\lfloor x/2 \rfloor$ (the floor division discards the lost bit $d_0$).

    **Negative numbers and arithmetic vs. logical shift:**

    - **Logical shift right** inserts a 0 in the most significant bit. For the two's complement representation of -2 (`11111110` in 8-bit), logical right shift gives `01111111` = 127, which is wrong as a division by 2.
    - **Arithmetic shift right** copies the sign bit (MSB) into the vacated position. For -2 (`11111110`), arithmetic right shift gives `11111111` = -1, which is the correct $\lfloor -2/2 \rfloor = -1$.

    Python uses arithmetic right shift for negative numbers (`-2 >> 1 == -1`), which preserves the floor-division semantics. The distinction matters because the sign bit has a negative weight ($-2^{n-1}$) in two's complement, so inserting a 0 there dramatically changes the value.
