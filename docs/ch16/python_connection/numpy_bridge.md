# How NumPy Bridges the Gap

!!! tip "Mental Model"
    NumPy lets you write one line of Python that triggers millions of operations in optimized C. The trick is contiguous, typed memory: instead of a Python list of boxed objects scattered across the heap, NumPy stores raw numbers side by side, enabling cache-friendly access and SIMD vectorization. You describe what to compute; NumPy handles how.

## The NumPy Strategy

NumPy achieves C-like performance while staying in Python by:

1. Storing data in contiguous, typed arrays (like C)
2. Implementing operations in compiled C code
3. Minimizing Python overhead by operating on whole arrays

```
The NumPy Bridge:

Python World                          C World
┌─────────────────────┐              ┌─────────────────────┐
│                     │              │                     │
│  arr = np.array()   │───creates──▶│  Raw memory block   │
│  arr * 2            │───calls────▶│  Compiled C loop    │
│  np.sum(arr)        │───calls────▶│  Optimized routine  │
│                     │              │                     │
│  Easy syntax        │              │  Fast execution     │
└─────────────────────┘              └─────────────────────┘
```

## Memory Layout Comparison

### Python List

```python
# Python list of integers
py_list = [1, 2, 3, 4, 5]
```

```
Memory Layout (scattered):

py_list object ──▶ [ref1, ref2, ref3, ref4, ref5]
                      │      │      │      │      │
                      ▼      ▼      ▼      ▼      ▼
                   PyInt  PyInt  PyInt  PyInt  PyInt
                   (28B)  (28B)  (28B)  (28B)  (28B)
                   at     at     at     at     at
                   0x100  0x250  0x180  0x300  0x220
                   
Total: 80 bytes (list) + 5×28 bytes (ints) = 220 bytes
Plus: pointer chasing, poor cache locality
```

### NumPy Array

```python
# NumPy array of integers
np_arr = np.array([1, 2, 3, 4, 5], dtype=np.int64)
```

```
Memory Layout (contiguous):

np_arr object ──▶ metadata (dtype, shape, strides)
                      │
                      ▼
                  ┌───┬───┬───┬───┬───┐
                  │ 1 │ 2 │ 3 │ 4 │ 5 │  Raw values
                  └───┴───┴───┴───┴───┘
                  8B   8B   8B   8B   8B
                  
                  Contiguous block at 0x100
                  
Total: ~100 bytes (metadata) + 5×8 bytes (data) = 140 bytes
Plus: Sequential access, excellent cache locality
```

## How NumPy Operations Work

### Element-wise Operations

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = a * 2  # Element-wise multiplication
```

What happens:

```
Python level:
  b = a * 2
       │
       ▼
  a.__mul__(2)
       │
       ▼
  numpy.multiply(a, 2)

C level:
┌────────────────────────────────────────────────────────┐
│  for (i = 0; i < n; i++) {                            │
│      result[i] = data[i] * 2;                         │
│  }                                                     │
│                                                        │
│  - No type checking per element                        │
│  - No object creation per element                      │
│  - Contiguous memory access                            │
│  - SIMD vectorization possible                         │
└────────────────────────────────────────────────────────┘
```

### The BLAS/LAPACK Backend

For linear algebra, NumPy uses highly optimized libraries:

```python
import numpy as np

A = np.random.rand(1000, 1000)
B = np.random.rand(1000, 1000)
C = A @ B  # Matrix multiplication
```

```
Execution path:

np.matmul(A, B)
      │
      ▼
NumPy wrapper
      │
      ▼
BLAS library (OpenBLAS, MKL, or ATLAS)
      │
      ▼
┌────────────────────────────────────────────────────────┐
│  Highly optimized matrix multiplication:               │
│  - Cache-blocked algorithms                            │
│  - SIMD instructions (AVX2, AVX512)                   │
│  - Multi-threaded (parallel)                          │
│  - CPU-specific tuning                                │
└────────────────────────────────────────────────────────┘
```

## Vectorization

NumPy's key concept: **operate on arrays, not elements**.

### Slow: Python Loop

```python
# Element-by-element in Python
def slow_magnitude(x, y):
    result = []
    for i in range(len(x)):
        result.append(math.sqrt(x[i]**2 + y[i]**2))
    return result
```

### Fast: NumPy Vectorized

```python
# Whole-array operation in C
def fast_magnitude(x, y):
    return np.sqrt(x**2 + y**2)
```

### Performance Comparison

```python
import numpy as np
import time

n = 1_000_000
x = np.random.rand(n)
y = np.random.rand(n)

# Python loop
x_list, y_list = x.tolist(), y.tolist()
start = time.perf_counter()
result = [math.sqrt(x_list[i]**2 + y_list[i]**2) for i in range(n)]
python_time = time.perf_counter() - start

# NumPy vectorized
start = time.perf_counter()
result = np.sqrt(x**2 + y**2)
numpy_time = time.perf_counter() - start

print(f"Python: {python_time:.3f}s")
print(f"NumPy:  {numpy_time:.3f}s")
print(f"Speedup: {python_time/numpy_time:.0f}x")
```

Typical output:
```
Python: 0.450s
NumPy:  0.005s
Speedup: 90x
```

## Universal Functions (ufuncs)

NumPy's `ufuncs` are C-compiled functions that operate element-wise:

```python
# These are all ufuncs - implemented in C
np.add(a, b)       # Addition
np.multiply(a, b)  # Multiplication
np.sin(a)          # Trigonometry
np.exp(a)          # Exponential
np.log(a)          # Logarithm
np.maximum(a, b)   # Element-wise max
```

### ufunc Features

```python
# Broadcasting - different shapes work together
a = np.array([[1], [2], [3]])  # Shape (3, 1)
b = np.array([10, 20, 30])     # Shape (3,)
c = a + b                       # Shape (3, 3)!

# Output array - avoid allocation
out = np.empty_like(a)
np.multiply(a, 2, out=out)  # Result stored in pre-allocated array

# Reduction - aggregate operations
np.add.reduce([1, 2, 3, 4])  # 10 (sum)
np.multiply.reduce([1, 2, 3, 4])  # 24 (product)
```

## View vs Copy

NumPy avoids copying data when possible:

```python
a = np.arange(10)

# View - shares memory (fast)
b = a[::2]  # Every other element
b[0] = 99   # Modifies 'a' too!

# Copy - new memory (slower but independent)
c = a[::2].copy()
c[0] = 99   # Doesn't affect 'a'
```

```
View (no copy):
a: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
     ↑     ↑     ↑     ↑     ↑
b:   └─────┴─────┴─────┴─────┘  (same memory, different stride)

Copy (new memory):
a: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

c: [0, 2, 4, 6, 8]  (separate memory)
```

## NumPy + Cache Efficiency

```python
import numpy as np
import time

n = 10000

# Row-major array (default)
a = np.random.rand(n, n)

# Row-wise sum (cache-friendly)
start = time.perf_counter()
row_sums = np.sum(a, axis=1)
row_time = time.perf_counter() - start

# Column-wise sum (cache-unfriendly for C-order)
start = time.perf_counter()
col_sums = np.sum(a, axis=0)
col_time = time.perf_counter() - start

print(f"Row-wise: {row_time:.4f}s")
print(f"Col-wise: {col_time:.4f}s")
```

## When NumPy Isn't Enough

### Numba: JIT Compilation

```python
from numba import jit
import numpy as np

@jit(nopython=True)
def custom_operation(arr):
    """JIT-compiled to machine code."""
    result = 0.0
    for i in range(len(arr)):
        result += arr[i] ** 2 + np.sin(arr[i])
    return result

# First call: compiles
# Subsequent calls: fast as C
```

### Cython: Static Typing

```python
# In .pyx file
cimport numpy as np
import numpy as np

def fast_operation(np.ndarray[np.float64_t, ndim=1] arr):
    cdef int i
    cdef double result = 0.0
    for i in range(arr.shape[0]):
        result += arr[i] ** 2
    return result
```

## Summary

| Technique | How It Helps |
|-----------|--------------|
| **Contiguous memory** | Cache efficiency, SIMD possible |
| **Typed arrays** | No per-element type checking |
| **C implementation** | No interpreter overhead |
| **Vectorization** | One Python call → millions of C operations |
| **BLAS/LAPACK** | Decades of optimization for linear algebra |
| **Views** | Avoid copying data |

The NumPy pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  Python: Describe WHAT to compute                          │
│          (high-level, readable, flexible)                  │
│                                                             │
│  NumPy:  Handle HOW to compute                             │
│          (low-level, optimized, parallel)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

One line of NumPy = thousands of optimized C operations
```


---

## Exercises

**Exercise 1.** Explain how NumPy achieves near-C performance despite being called from Python. What role do compiled C libraries play?

??? success "Solution to Exercise 1"
    ```python
    # Conceptual solution - see page content for details
    import sys
    import platform

    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    ```

---

**Exercise 2.** Write Python code that compares the performance of a pure Python loop versus a NumPy vectorized operation for computing the sum of squares of 1 million numbers.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Explain what the 'Python overhead' means when calling NumPy functions on very small arrays. Why might a Python loop be faster for arrays of size 5?

??? success "Solution to Exercise 3"
    ```python
    import time

    # Simple benchmark
    n = 10_000_000
    start = time.perf_counter()
    total = sum(range(n))
    elapsed = time.perf_counter() - start
    print(f"Sum of {n} integers: {total}")
    print(f"Time: {elapsed:.4f} seconds")
    ```

---

**Exercise 4.** Write code that demonstrates the memory layout difference between a Python list and a NumPy array using `sys.getsizeof()`.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    # Python loop
    start = time.perf_counter()
    result_py = sum(i * i for i in range(n))
    time_py = time.perf_counter() - start

    # NumPy vectorized
    arr = np.arange(n)
    start = time.perf_counter()
    result_np = np.sum(arr * arr)
    time_np = time.perf_counter() - start

    print(f"Python: {time_py:.4f}s, NumPy: {time_np:.4f}s")
    print(f"Speedup: {time_py / time_np:.1f}x")
    ```
