# Float Python vs C

Python and C handle floating-point numbers differently. Understanding these differences explains performance characteristics and memory usage patterns.

!!! tip "Mental Model"
    Both Python and C use the same IEEE 754 double-precision format for floats, so they agree on precision. The difference is overhead: C's `double` is a bare 8-byte value on the stack, while Python's `float` is a heap-allocated object with a type pointer and reference count, making it roughly 3x larger and slower to allocate.

## Introductory Example

A surprising result from floating-point arithmetic.

### 1. The Classic Problem

Adding 0.1 twice doesn't always equal 0.2.

```python
def main():
    a = 0.1
    b = 0.1
    c = a + b
    print(c == 0.2)  # True

if __name__ == "__main__":
    main()
```

### 2. A Surprising Failure

But 0.1 + 1.1 doesn't equal 1.2.

```python
def main():
    a = 0.1
    b = 1.1
    c = a + b
    print(c == 1.2)  # False

if __name__ == "__main__":
    main()

# Why? Check the actual values
print(f"{0.1 + 1.1:.20f}")  # 1.20000000000000017764
print(f"{1.2:.20f}")        # 1.19999999999999995559
```

### 3. Binary Representation Cause

Both languages share this issue due to IEEE 754.

```python
# Neither 0.1 nor 1.1 are exactly representable
print(f"{0.1:.20f}")   # 0.10000000000000000555
print(f"{1.1:.20f}")   # 1.10000000000000008882
print(f"{1.2:.20f}")   # 1.19999999999999995559

# The sum accumulates errors differently
print(f"{0.1 + 1.1:.20f}")  # 1.20000000000000017764
```

## Python Float Implementation

How CPython stores floating-point numbers.

### 1. PyFloatObject Structure

Python floats are full objects with metadata.

```c
// CPython internal structure (simplified)
typedef struct {
    PyObject_HEAD          // Reference count + type pointer
    double ob_fval;        // 64-bit IEEE 754 value
} PyFloatObject;
```

```python
# Every float is an object
x = 3.14
print(type(x))  # <class 'float'>

# Has object identity
print(id(x))    # Memory address
```

### 2. Memory Overhead

Python floats consume more memory than the raw value.

```python
import sys

# Single float object size
x = 3.14
print(sys.getsizeof(x))  # 24 bytes

# Compare: the actual value is only 8 bytes (64-bit double)
# Extra 16 bytes for:
#   - Reference count (8 bytes)
#   - Type pointer (8 bytes)
```

### 3. Dynamic Typing Cost

Type determined at runtime, not compile time.

```python
def add_floats(a, b):
    return a + b  # Type check happens at runtime

# Python must:
# 1. Check type of a
# 2. Check type of b
# 3. Look up __add__ method
# 4. Perform addition
# 5. Create new float object for result

result = add_floats(1.5, 2.5)
```

## C Float Implementation

How C stores floating-point numbers.

### 1. Direct Memory Storage

C floats are raw binary values without metadata.

```c
#include <stdio.h>

int main() {
    float a = 3.14f;   // 32-bit IEEE 754
    double b = 3.14;   // 64-bit IEEE 754
    
    printf("float: %f\n", a);
    printf("double: %lf\n", b);
    
    return 0;
}
```

### 2. Fixed Size

Size determined at compile time.

```c
#include <stdio.h>

int main() {
    printf("sizeof(float): %zu bytes\n", sizeof(float));   // 4 bytes
    printf("sizeof(double): %zu bytes\n", sizeof(double)); // 8 bytes
    
    return 0;
}
```

### 3. Static Typing

Type known at compile time enables optimization.

```c
double add_doubles(double a, double b) {
    return a + b;  // Single CPU instruction
}

// Compiler knows exact types
// No runtime type checking
// Direct floating-point addition
```

## Key Differences

Side-by-side comparison of Python and C floats.

### 1. Comparison Table

| Feature | Python `float` | C `float` / `double` |
|---------|---------------|---------------------|
| Typing | Dynamic | Static |
| Size | 24 bytes (object) | 4 / 8 bytes |
| Storage | Heap with metadata | Stack or heap directly |
| Performance | Slower (overhead) | Faster (direct access) |
| Precision | 64-bit (always) | 32-bit or 64-bit |
| Overflow | Returns `inf` / `-inf` | Undefined behavior |

### 2. Memory Layout Visualization

```python
# Python float memory layout (24 bytes total)
# +------------------+
# | Reference Count  |  8 bytes
# +------------------+
# | Type Pointer     |  8 bytes  -> points to float type
# +------------------+
# | ob_fval (double) |  8 bytes  -> actual IEEE 754 value
# +------------------+

# C double memory layout (8 bytes total)
# +------------------+
# | IEEE 754 value   |  8 bytes  -> that's it!
# +------------------+
```

### 3. Array Memory Comparison

```python
import sys

# Python list of floats
py_list = [1.0, 2.0, 3.0, 4.0, 5.0]
list_size = sys.getsizeof(py_list)
objects_size = sum(sys.getsizeof(x) for x in py_list)
print(f"Python list: {list_size} + {objects_size} = {list_size + objects_size} bytes")

# NumPy array (C-style storage)
import numpy as np
np_array = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
print(f"NumPy array: {np_array.nbytes} bytes (data only)")
print(f"NumPy total: {sys.getsizeof(np_array)} bytes (with overhead)")
```

## Performance Implications

How implementation affects speed.

### 1. Operation Overhead

Python has significant per-operation cost.

```python
import time

# Python float operations
def python_sum(n):
    total = 0.0
    for i in range(n):
        total += 0.1
    return total

start = time.perf_counter()
result = python_sum(1_000_000)
elapsed = time.perf_counter() - start
print(f"Python loop: {elapsed:.4f} seconds")
```

### 2. NumPy Speedup

NumPy uses C-style operations internally.

```python
import numpy as np
import time

# NumPy vectorized operations
def numpy_sum(n):
    arr = np.full(n, 0.1)
    return np.sum(arr)

start = time.perf_counter()
result = numpy_sum(1_000_000)
elapsed = time.perf_counter() - start
print(f"NumPy sum: {elapsed:.4f} seconds")

# Typically 10-100x faster than Python loop
```

### 3. Benchmark Comparison

```python
import numpy as np
import time

n = 1_000_000

# Method 1: Python loop
start = time.perf_counter()
total = 0.0
for _ in range(n):
    total += 0.1
python_time = time.perf_counter() - start

# Method 2: NumPy
start = time.perf_counter()
total = np.sum(np.full(n, 0.1))
numpy_time = time.perf_counter() - start

print(f"Python: {python_time:.4f}s")
print(f"NumPy:  {numpy_time:.4f}s")
print(f"Speedup: {python_time/numpy_time:.1f}x")
```

## Precision Differences

Both use IEEE 754, but with different defaults.

### 1. Python Always Uses Double

Python `float` is always 64-bit.

```python
import sys

# No way to create 32-bit float in pure Python
x = 3.14
print(f"Mantissa digits: {sys.float_info.mant_dig}")  # 53
print(f"Decimal digits: {sys.float_info.dig}")        # 15
```

### 2. C Offers Both Precisions

C provides 32-bit and 64-bit options.

```c
#include <stdio.h>
#include <float.h>

int main() {
    // 32-bit float
    printf("float digits: %d\n", FLT_DIG);        // 6
    printf("float mantissa: %d\n", FLT_MANT_DIG); // 24
    
    // 64-bit double
    printf("double digits: %d\n", DBL_DIG);       // 15
    printf("double mantissa: %d\n", DBL_MANT_DIG);// 53
    
    return 0;
}
```

### 3. NumPy Provides Both

Use NumPy for 32-bit floats in Python.

```python
import numpy as np

# 32-bit float
f32 = np.float32(3.14159265358979)
print(f"float32: {f32}")  # 3.1415927 (lost precision)

# 64-bit float
f64 = np.float64(3.14159265358979)
print(f"float64: {f64}")  # 3.14159265358979

# Check precision
print(f"float32 eps: {np.finfo(np.float32).eps:.2e}")  # ~1.2e-07
print(f"float64 eps: {np.finfo(np.float64).eps:.2e}")  # ~2.2e-16
```

## Overflow Handling

Python and C handle extreme values differently.

### 1. Python Graceful Overflow

Python converts to infinity without crashing.

```python
import sys

# Approach maximum
large = sys.float_info.max
print(f"Max float: {large}")  # ~1.8e308

# Overflow to infinity
overflow = large * 2
print(f"Overflow: {overflow}")  # inf

# Operations continue
print(overflow + 1)    # inf
print(overflow * -1)   # -inf
print(1 / overflow)    # 0.0
```

### 2. C Silent Overflow

C may produce undefined behavior.

```c
#include <stdio.h>
#include <float.h>

int main() {
    float large = FLT_MAX;
    printf("Max float: %e\n", large);
    
    // Overflow - behavior is implementation-defined
    float overflow = large * 2.0f;
    printf("Overflow: %e\n", overflow);  // May be inf or garbage
    
    return 0;
}
```

### 3. Safe Overflow Detection

Check for infinity in both languages.

```python
import math

def safe_multiply(a, b):
    """Multiply with overflow detection."""
    result = a * b
    if math.isinf(result):
        raise OverflowError(f"Overflow: {a} * {b}")
    return result

try:
    x = safe_multiply(1e200, 1e200)
except OverflowError as e:
    print(e)  # Overflow: 1e+200 * 1e+200
```

## Underflow Handling

Very small values approaching zero.

### 1. Python Gradual Underflow

Python supports subnormal numbers.

```python
import sys

# Approach minimum
small = sys.float_info.min
print(f"Min positive: {small}")  # ~2.2e-308

# Gradual underflow (subnormal)
tiny = small / 1e10
print(f"Subnormal: {tiny}")  # ~2.2e-318

# Complete underflow to zero
zero = small / 1e308
print(f"Underflow: {zero}")  # 0.0
```

### 2. C Underflow Behavior

C behavior depends on compiler settings.

```c
#include <stdio.h>
#include <float.h>

int main() {
    double small = DBL_MIN;
    printf("Min positive: %e\n", small);
    
    // May underflow to zero or subnormal
    double tiny = small / 1e10;
    printf("Tiny: %e\n", tiny);
    
    return 0;
}
```

## Practical Recommendations

When to use each approach.

### 1. Use Python Floats For

General-purpose scripting and prototyping.

```python
# Quick calculations
price = 19.99
tax_rate = 0.0825
total = price * (1 + tax_rate)
print(f"Total: ${total:.2f}")

# Readability over performance
def calculate_interest(principal, rate, years):
    return principal * (1 + rate) ** years
```

### 2. Use NumPy For

Performance-critical numerical work.

```python
import numpy as np

# Large-scale computation
data = np.random.randn(1_000_000)
mean = np.mean(data)
std = np.std(data)

# Matrix operations
A = np.random.randn(1000, 1000)
B = np.random.randn(1000, 1000)
C = A @ B  # Fast matrix multiplication
```

### 3. Use C/Cython For

Maximum performance requirements.

```python
# When even NumPy isn't fast enough:
# 1. Write critical code in C
# 2. Use Cython for C-like speed with Python syntax
# 3. Use Numba JIT compilation

from numba import jit

@jit(nopython=True)
def fast_sum(arr):
    total = 0.0
    for x in arr:
        total += x
    return total
```

## Summary Table

Quick reference for Python vs C floats.

### 1. When to Choose What

| Use Case | Recommendation |
|----------|----------------|
| Scripting | Python `float` |
| Data science | NumPy arrays |
| Real-time systems | C `double` |
| Embedded systems | C `float` (32-bit) |
| Financial | Python `Decimal` |
| Scientific computing | NumPy + SciPy |

### 2. Memory Rule of Thumb

```python
import sys
import numpy as np

# Single value
print(f"Python float: {sys.getsizeof(1.0)} bytes")  # 24
print(f"NumPy float64: {np.float64(1.0).nbytes} bytes")  # 8

# Array of 1000 floats
py_list = [1.0] * 1000
np_arr = np.ones(1000, dtype=np.float64)

py_size = sys.getsizeof(py_list) + sum(sys.getsizeof(x) for x in py_list)
np_size = np_arr.nbytes

print(f"Python list: ~{py_size} bytes")   # ~32,000
print(f"NumPy array: {np_size} bytes")    # 8,000
print(f"Ratio: {py_size/np_size:.1f}x")   # ~4x more memory
```


---

## Exercises


**Exercise 1.**
Use `sys.getsizeof()` to compare the memory used by a single Python `float`, a Python `int`, and a Python `str` of `"3.14"`. Explain why a Python float uses more memory than the 8 bytes needed for the IEEE 754 value.

??? success "Solution to Exercise 1"

    ```python
    import sys

    f = 3.14
    i = 3
    s = "3.14"

    print(f"float: {sys.getsizeof(f)} bytes")  # 24
    print(f"int:   {sys.getsizeof(i)} bytes")   # 28
    print(f"str:   {sys.getsizeof(s)} bytes")   # 53

    # Python float uses 24 bytes:
    #   8 bytes for reference count
    #   8 bytes for type pointer
    #   8 bytes for the actual IEEE 754 double value
    ```

    Every Python object carries metadata (reference count and type pointer), adding 16 bytes of overhead on top of the 8-byte double value.

---

**Exercise 2.**
Write a timing comparison that sums one million `0.1` values using (a) a Python `for` loop and (b) `sum()` with a generator expression. Report the times and explain the difference.

??? success "Solution to Exercise 2"

    ```python
    import time

    n = 1_000_000

    # Method 1: for loop
    start = time.perf_counter()
    total = 0.0
    for _ in range(n):
        total += 0.1
    loop_time = time.perf_counter() - start

    # Method 2: sum with generator
    start = time.perf_counter()
    total = sum(0.1 for _ in range(n))
    sum_time = time.perf_counter() - start

    print(f"for loop: {loop_time:.4f}s")
    print(f"sum():    {sum_time:.4f}s")
    ```

    `sum()` is implemented in C and avoids Python bytecode overhead for each addition, making it faster than an explicit loop.

---

**Exercise 3.**
Demonstrate that `0.1 + 0.2 != 0.3` in Python and show two different ways to correctly compare floating-point values for approximate equality.

??? success "Solution to Exercise 3"

    ```python
    import math

    # The problem
    print(0.1 + 0.2 == 0.3)  # False

    # Solution 1: math.isclose
    print(math.isclose(0.1 + 0.2, 0.3))  # True

    # Solution 2: absolute tolerance
    epsilon = 1e-9
    print(abs((0.1 + 0.2) - 0.3) < epsilon)  # True
    ```

    Floating-point representation errors mean `0.1 + 0.2` produces `0.30000000000000004`. Use `math.isclose()` or an explicit tolerance for comparisons.
