# Vectorization Basics

Vectorization replaces explicit loops with bulk array operations optimized in C.

!!! tip "Mental Model"
    Vectorization means expressing your computation as operations on whole arrays instead of looping over individual elements. The mental shift is from "process one item at a time" to "describe the transformation on the entire collection." NumPy then runs the work in compiled C, bypassing Python's per-element overhead entirely.

!!! note "Performance Model — The Optimization Hierarchy"
    Efficient NumPy code is not about writing faster loops — it is about
    transforming computations into forms the system can execute efficiently.
    This transformation follows a hierarchy, from most to least impactful:

    ```text
    1. Mathematical simplification  → closed-form beats any loop
    2. Vectorization                → array ops in C (this page)
    3. Memory optimization          → in-place ops, preallocation
    4. Loop optimization            → hoisting invariants
    5. Measurement                  → profiling to find the real bottleneck
    ```

    The goal at every level is the same: **move computation from Python-level
    interpretation to optimized low-level execution**:

    ```text
    Python loop → NumPy vectorization → compiled C → CPU/SIMD → GPU/distributed
    ```

    Always start at the top of the hierarchy — a closed-form formula beats even
    the best-vectorized loop. When NumPy alone is not enough, [acceleration
    libraries](acceleration_libs.md) extend the pipeline further toward hardware.


## Core Principle

Suppress Python-level loops for orders-of-magnitude speedup.

### 1. Loop Approach

```python
import numpy as np

def square_with_loop(arr):
    result = np.empty_like(arr)
    for i in range(len(arr)):
        result[i] = arr[i] ** 2
    return result
```

### 2. Vectorized Approach

```python
import numpy as np

def square_vectorized(arr):
    return arr ** 2
```

### 3. Key Difference

Vectorized code executes in optimized C; loops execute in slow Python.


## Performance Gain

Vectorization yields dramatic speedups.

### 1. Timing Comparison

```python
import numpy as np
import time

def main():
    arr = np.random.randn(1_000_000)
    
    # Loop timing
    start = time.perf_counter()
    result_loop = np.empty_like(arr)
    for i in range(len(arr)):
        result_loop[i] = arr[i] ** 2
    loop_time = time.perf_counter() - start
    
    # Vectorized timing
    start = time.perf_counter()
    result_vec = arr ** 2
    vec_time = time.perf_counter() - start
    
    print(f"Loop time:       {loop_time:.4f} sec")
    print(f"Vectorized time: {vec_time:.6f} sec")
    print(f"Speedup:         {loop_time / vec_time:.0f}x")

if __name__ == "__main__":
    main()
```

### 2. Typical Results

```
Loop time:       0.3200 sec
Vectorized time: 0.001500 sec
Speedup:         213x
```

### 3. Scale Matters

Speedup increases with array size.


## Common Patterns

Recognize loop patterns that can be vectorized.

### 1. Element-wise Math

```python
import numpy as np

# Loop
for i in range(len(arr)):
    result[i] = np.sin(arr[i])

# Vectorized
result = np.sin(arr)
```

### 2. Conditional Logic

```python
import numpy as np

# Loop
for i in range(len(arr)):
    if arr[i] > 0:
        result[i] = arr[i]
    else:
        result[i] = 0

# Vectorized
result = np.where(arr > 0, arr, 0)
```

### 3. Aggregation

```python
import numpy as np

# Loop
total = 0
for i in range(len(arr)):
    total += arr[i]

# Vectorized
total = np.sum(arr)
```


## Universal Functions

NumPy ufuncs are inherently vectorized.

### 1. Math Functions

```python
import numpy as np

arr = np.array([1, 2, 3, 4])
print(np.sqrt(arr))   # [1.  1.41 1.73 2.]
print(np.exp(arr))    # [2.71 7.38 20.08 54.59]
print(np.log(arr))    # [0.  0.69 1.09 1.38]
```

### 2. Comparison Functions

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([2, 2, 2])
print(np.maximum(a, b))  # [2 2 3]
print(np.minimum(a, b))  # [1 2 2]
```

### 3. Custom ufuncs

Use `np.vectorize` for custom functions (convenience, not performance).


## When Loops Are OK

Some situations still require explicit loops.

### 1. Sequential Dependence

When iteration `i` depends on result of `i-1`.

### 2. Complex Logic

When vectorization would be unreadable or impossible.

### 3. Small Arrays

Overhead matters less for tiny arrays.

---

## Runnable Example: `norm_optimization_progression.py`

```python
"""
Vector Norm Computation: Pure Python vs NumPy Vectorization

This tutorial demonstrates how vectorizing mathematical operations can lead to
dramatic performance improvements. We'll compute the L2 norm (Euclidean norm) of
a vector using two approaches:

1. Pure Python with explicit loops
2. NumPy with vectorized array operations

The key insight: NumPy operations are implemented in C and operate on entire
arrays at once, while pure Python loops iterate element-by-element, incurring
function call overhead for each iteration.

Learning Goals:
- Understand what vectorization means in practice
- See how NumPy leverages compiled code for speed
- Recognize patterns in your code that could be vectorized
- Measure the real-world performance difference
"""

import time
import numpy as np

if __name__ == "__main__":


    print("=" * 70)
    print("VECTOR NORM COMPUTATION: PURE PYTHON vs NUMPY VECTORIZATION")
    print("=" * 70)


    # ============ EXAMPLE 1: Pure Python Implementation ============
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Pure Python with Explicit Loops")
    print("=" * 70)

    def norm_square_python(vector):
        """
        Compute the squared L2 norm using pure Python.

        The L2 norm (Euclidean norm) of a vector is: sqrt(sum(v_i^2))
        We compute the squared norm (without the sqrt) since sqrt is expensive
        and we often only care about relative magnitudes.

        Why this is slow:
        - Each iteration calls Python operations (addition, multiplication)
        - Python must interpret each operation
        - No knowledge of what comes next, so can't optimize
        """
        norm = 0
        for v in vector:
            norm += v * v
        return norm


    # Create a test vector
    test_vector_python = list(range(10000))

    # Show what the function returns
    result_python = norm_square_python(test_vector_python)
    print(f"\nSquared norm of vector [0, 1, 2, ..., 9999]: {result_python}")
    print(f"This equals: sum(i^2 for i in 0..9999) = 0^2 + 1^2 + 2^2 + ... + 9999^2")

    # Time the pure Python version
    num_iterations = 5
    times_python = []
    test_size = 1000000

    test_vector_python = list(range(test_size))
    print(f"\nTiming pure Python with vector of {test_size:,} elements ({num_iterations} runs):")

    for i in range(num_iterations):
        start = time.time()
        norm_square_python(test_vector_python)
        elapsed = time.time() - start
        times_python.append(elapsed)
        print(f"  Run {i+1}: {elapsed:.6f}s")

    min_time_python = min(times_python)
    print(f"\nBest pure Python time: {min_time_python:.6f}s")


    # ============ EXAMPLE 2: NumPy Vectorized Implementation ============
    print("\n" + "=" * 70)
    print("EXAMPLE 2: NumPy Vectorized Operations")
    print("=" * 70)

    def norm_square_numpy(vector):
        """
        Compute the squared L2 norm using NumPy.

        Why this is fast:
        - vector * vector: element-wise multiplication on entire array at once
        - np.sum(): single function call to sum all elements
        - Both operations are implemented in optimized C code
        - NumPy can use SIMD (Single Instruction Multiple Data) on modern CPUs
        - No Python loop overhead!

        The key vectorization principle:
        Instead of: for v in vector: norm += v * v
        Do this:   np.sum(vector * vector)
        """
        return np.sum(vector * vector)


    # Create a test vector using NumPy
    test_vector_numpy = np.arange(10000)

    # Show what the function returns
    result_numpy = norm_square_numpy(test_vector_numpy)
    print(f"\nSquared norm of vector [0, 1, 2, ..., 9999]: {result_numpy}")
    print(f"Note: Same result as pure Python (both should be {int(result_python)})")

    # Time the NumPy version
    times_numpy = []
    test_vector_numpy = np.arange(test_size)
    print(f"\nTiming NumPy with vector of {test_size:,} elements ({num_iterations} runs):")

    for i in range(num_iterations):
        start = time.time()
        norm_square_numpy(test_vector_numpy)
        elapsed = time.time() - start
        times_numpy.append(elapsed)
        print(f"  Run {i+1}: {elapsed:.6f}s")

    min_time_numpy = min(times_numpy)
    print(f"\nBest NumPy time: {min_time_numpy:.6f}s")


    # ============ EXAMPLE 3: Performance Comparison ============
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Performance Comparison & Speedup Analysis")
    print("=" * 70)

    speedup = min_time_python / min_time_numpy
    print(f"\nResults for {test_size:,}-element vector:")
    print(f"  Pure Python: {min_time_python:.6f}s")
    print(f"  NumPy:       {min_time_numpy:.6f}s")
    print(f"  Speedup:     {speedup:.1f}x faster with NumPy")

    print(f"\n{'*' * 70}")
    print("WHY IS VECTORIZATION SO POWERFUL?")
    print("{'*' * 70}")

    print("""
    1. ELIMINATION OF PYTHON LOOP OVERHEAD
       - Pure Python: 1,000,000 iterations through Python's interpreter
       - NumPy: One C function call that processes all data

    2. COMPILED C IMPLEMENTATION
       - NumPy operations (*, sum) are written in C
       - C is orders of magnitude faster than interpreted Python
       - Direct memory access without Python's dynamic type checking

    3. SIMD VECTORIZATION
       - Modern CPUs have instructions to process multiple values in one step
       - NumPy can use these (AVX, SSE) for additional speedup
       - Python loops cannot take advantage of this

    4. MEMORY LAYOUT AWARENESS
       - NumPy arrays store data in continuous memory blocks
       - CPU caches work optimally with this layout
       - Python lists are scattered pointers, poor cache behavior

    5. ALGORITHMIC OPTIMIZATION
       - NumPy's internals are battle-tested and optimized
       - Authors have spent years perfecting these algorithms
       - Your hand-written loops can't compete
    """)


    # ============ EXAMPLE 4: Correct NumPy Norm Using Built-in ============
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Using NumPy's Built-in Norm Function")
    print("=" * 70)

    print("""
    In real code, you'd use NumPy's norm function:
      norm = np.linalg.norm(vector)  # Computes sqrt(sum(v_i^2))

    This is even more optimized and handles edge cases properly.
    """)

    # Demonstrate
    vector_example = np.array([3.0, 4.0])
    norm_result = np.linalg.norm(vector_example)
    print(f"Example: norm([3, 4]) = {norm_result} (should be 5.0)")
    print(f"  Verification: sqrt(3^2 + 4^2) = sqrt(9 + 16) = sqrt(25) = 5.0")


    # ============ EXAMPLE 5: The Vectorization Pattern ============
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Recognizing Vectorization Opportunities")
    print("=" * 70)

    print("""
    When you see this pattern in Python:

        result = initial_value
        for element in collection:
            result = operation(result, element)

    Consider if you can vectorize it with NumPy:

        1. Convert to NumPy array
        2. Use element-wise operations (*, +, etc.)
        3. Use aggregation functions (sum, mean, max, etc.)

    Example transformations:

    BEFORE (Pure Python):
        total = 0
        for x in values:
            total += x * x

    AFTER (Vectorized):
        total = np.sum(values * values)

    BEFORE (Pure Python):
        result = []
        for i, val in enumerate(my_list):
            result.append(val * 2)

    AFTER (Vectorized):
        result = np.array(my_list) * 2

    The principle: Avoid Python loops over numeric data when possible.
    """)


    print("\n" + "=" * 70)
    print("KEY TAKEAWAY")
    print("=" * 70)
    print(f"""
    Vectorization with NumPy can provide {speedup:.0f}x+ speedup for numerical
    operations. The main idea is to let compiled libraries (NumPy, using C code)
    handle the iteration instead of Python's interpreter.

    This is one of the most important optimization techniques for data-heavy
    Python code. As a rule of thumb:
    - Numerical operations on large arrays → Use NumPy
    - File I/O or string processing → Optimize differently
    - When speed matters, measure and vectorize
    """)
```

---

## Exercises

**Exercise 1.** Write a vectorized NumPy solution and a pure Python loop solution for the same computation. Measure and compare their performance using `time.perf_counter()`.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    data = np.random.default_rng(42).random(n)

    # Python loop
    start = time.perf_counter()
    result_py = [x ** 2 for x in data]
    py_time = time.perf_counter() - start

    # NumPy vectorized
    start = time.perf_counter()
    result_np = data ** 2
    np_time = time.perf_counter() - start

    print(f"Python: {py_time:.4f}s, NumPy: {np_time:.6f}s")
    print(f"Speedup: {py_time / np_time:.0f}x")
    ```

---

**Exercise 2.** Identify a potential performance pitfall in the following code and rewrite it using NumPy vectorization:

```python
result = []
for i in range(len(data)):
    result.append(data[i] ** 2 + 2 * data[i] + 1)
```

??? success "Solution to Exercise 2"
    ```python
    import numpy as np

    data = np.random.default_rng(42).random(100000)

    # Vectorized (fast)
    result = data ** 2 + 2 * data + 1
    ```

    The loop version creates Python objects for each element and calls `append` repeatedly. The vectorized version computes everything in compiled C code on contiguous memory.

---

**Exercise 3.** Explain why NumPy vectorized operations are faster than Python loops. Reference memory layout, type checking overhead, and SIMD instructions in your answer.

??? success "Solution to Exercise 3"
    NumPy vectorized operations are faster because:

    1. **Contiguous memory**: NumPy arrays store elements in a contiguous block, enabling efficient CPU cache usage.
    2. **No type checking**: Python loops check types at each iteration; NumPy knows the dtype in advance.
    3. **Compiled C loops**: The actual computation runs in compiled C/Fortran code, not interpreted Python.
    4. **SIMD instructions**: Modern CPUs can process multiple array elements simultaneously using SIMD (Single Instruction, Multiple Data).

---

**Exercise 4.** Apply the concepts from this page to a practical problem: given a large array of temperatures in Celsius, convert them all to Fahrenheit and find the maximum. Compare vectorized and loop approaches.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    rng = np.random.default_rng(42)
    celsius = rng.uniform(-40, 50, 1_000_000)

    # Vectorized
    start = time.perf_counter()
    fahrenheit = celsius * 9/5 + 32
    max_f = fahrenheit.max()
    vec_time = time.perf_counter() - start

    # Loop
    start = time.perf_counter()
    max_f_loop = max(c * 9/5 + 32 for c in celsius)
    loop_time = time.perf_counter() - start

    print(f"Vectorized: {vec_time:.6f}s, max={max_f:.1f}F")
    print(f"Loop: {loop_time:.4f}s, max={max_f_loop:.1f}F")
    ```
