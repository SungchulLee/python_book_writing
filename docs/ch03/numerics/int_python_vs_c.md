# `int`: Python vs C

Python integers (`int`) differ fundamentally from integers in low-level languages like C. Understanding this difference prevents many bugs and misconceptions.

!!! tip "Mental Model"
    C integers are fixed-width registers (32 or 64 bits) that silently overflow. Python integers are arbitrary-precision: they grow as large as memory allows, with no overflow. The trade-off is that Python integers are heap-allocated objects with higher memory overhead and slower arithmetic than raw machine integers.

---

## Fixed-size vs

### 1. C integers
- Fixed size (e.g. 32-bit or 64-bit)
- Overflow wraps around or is undefined

```c
int x = INT_MAX;
x = x + 1;   // overflow
```

### 2. Python integers
- Arbitrary precision
- No overflow (memory grows as needed)

```python
x = 10**100
print(x)
```

---

## Memory

- C `int`: stored directly in a fixed number of bits
- Python `int`: object containing
  - sign
  - length
  - array of machine words

This makes Python `int`:
- slower than C `int`
- but mathematically safe

---

## Semantics

Python integers obey **mathematical integer semantics**:
- exact arithmetic
- no overflow surprises

This is crucial for:
- financial calculations
- cryptography
- symbolic computation

---

## Performance

Because Python `int` is an object:
- arithmetic is slower than in C
- large integers cost more memory

For heavy numerical work, libraries like NumPy use fixed-size types internally.

---

## Key takeaways

- Python `int` has arbitrary precision.
- No overflow, but higher memory and CPU cost.
- Safer semantics than C for finance and math.


---

## Exercises


**Exercise 1.**
Compute `2 ** 1000` in Python and print the number of digits. Explain why this works in Python but would overflow in C.

??? success "Solution to Exercise 1"

    ```python
    result = 2 ** 1000
    num_digits = len(str(result))
    print(f"2^1000 has {num_digits} digits")  # 302 digits
    ```

    Python integers have arbitrary precision -- they grow as needed. In C, a 64-bit `long` can hold at most about 19 digits before overflowing.

---

**Exercise 2.**
Use `sys.getsizeof()` to compare the memory usage of the integers `0`, `1`, `2**30`, and `2**1000`. Explain the pattern.

??? success "Solution to Exercise 2"

    ```python
    import sys

    for val in [0, 1, 2**30, 2**1000]:
        size = sys.getsizeof(val)
        print(f"getsizeof({str(val)[:20]:>20s}...) = {size} bytes")
    ```

    Small integers use a fixed base size. As the value grows, Python allocates additional machine words to store the extra digits, so `2**1000` uses significantly more memory than `1`.

---

**Exercise 3.**
Write a function `factorial_digits(n)` that computes `n!` and returns the number of decimal digits in the result. Test with `n = 100`. Explain why Python can handle this while C `int` or `long` cannot.

??? success "Solution to Exercise 3"

    ```python
    import math

    def factorial_digits(n):
        result = math.factorial(n)
        return len(str(result))

    print(f"100! has {factorial_digits(100)} digits")  # 158 digits
    ```

    `100!` is a 158-digit number. Python handles this naturally because `int` has arbitrary precision. A C `unsigned long long` (64 bits) overflows at about `20!`.
