# Performance vs Loops

Vectorization is the single most important performance concept in NumPy.

!!! tip "Mental Model"
    Every Python `for` loop iteration pays a fixed overhead for type checking, reference counting, and interpreter dispatch. Vectorized NumPy operations pay that overhead once for the entire array and then run a tight C loop internally. The speedup is typically 10-100x, growing with array size because the per-element overhead vanishes.

## Python Loop Cost

### 1. Loop Overhead

A pure Python loop incurs significant overhead.

```python
import numpy as np

def add_with_loop(a, b):
    res = []
    for i in range(len(a)):
        res.append(a[i] + b[i])
    return res
```

### 2. Sources of Slowdown

Each iteration involves:

- Interpreter overhead
- Repeated attribute lookups
- Python object creation
- Type checking

### 3. Accumulating Cost

For large arrays, these costs multiply dramatically.

## Vectorized NumPy

### 1. Single Expression

```python
import numpy as np

def add_vectorized(a, b):
    return a + b
```

### 2. Under the Hood

This executes:

- In optimized C loops
- With contiguous memory access
- Without Python-level iteration

### 3. Hardware Benefits

Vectorized code can leverage:

- CPU cache prefetching
- SIMD instructions
- Memory locality

## Speedup Magnitude

### 1. Typical Speedups

Vectorization typically provides:

- 10×–100× faster for small arrays
- 100×–1000× faster for large arrays

### 2. Array Size Effect

```python
import numpy as np
import time

def main():
    for n in [1_000, 100_000, 10_000_000]:
        a = np.random.randn(n)
        
        # Loop
        start = time.perf_counter()
        result = [x ** 2 for x in a]
        loop_time = time.perf_counter() - start
        
        # Vectorized
        start = time.perf_counter()
        result = a ** 2
        vec_time = time.perf_counter() - start
        
        print(f"n={n:>10}: {loop_time/vec_time:>6.0f}x speedup")

if __name__ == "__main__":
    main()
```

### 3. Why Essential

This is why NumPy is essential for numerical work.

## Memory Tradeoffs

### 1. Temporary Arrays

Vectorization may allocate temporary arrays.

```python
import numpy as np

# Creates temporary for (a + b) before multiplying
result = (a + b) * c
```

### 2. Peak Memory

Large operations increase peak memory usage.

### 3. In-Place Operations

Use in-place operations when appropriate:

```python
import numpy as np

def main():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    
    a += b  # Modifies a in place
    print(a)

if __name__ == "__main__":
    main()
```

## Practical Guidance

### 1. Avoid Python Loops

Never loop over array elements when vectorization is possible.

### 2. Think in Arrays

Reformulate problems as array operations.

### 3. Profile First

Measure before micro-optimizing.

```python
import numpy as np
import time

def main():
    arr = np.random.randn(1_000_000)
    
    start = time.perf_counter()
    result = np.sum(arr ** 2)
    elapsed = time.perf_counter() - start
    
    print(f"Time: {elapsed:.6f} sec")

if __name__ == "__main__":
    main()
```

---

## Runnable Example: `performance_tutorial.py`

```python
"""
01_performance.py - Writing Fast NumPy Code

Key: Vectorization eliminates Python loops!
"""

import numpy as np
import time

if __name__ == "__main__":

    print("="*80)
    print("PERFORMANCE OPTIMIZATION")
    print("="*80)

    # ============================================================================
    # Vectorization Example
    # ============================================================================

    print("\nVectorization: Eliminate Loops!")
    print("="*80)

    n = 1000000
    arr = np.random.rand(n)

    # SLOW: Python loop
    print(f"\nProcessing {n:,} elements...")
    start = time.time()
    result = np.zeros(n)
    for i in range(n):
        result[i] = arr[i] ** 2 + 2 * arr[i] + 1
    slow_time = time.time() - start

    # FAST: Vectorized
    start = time.time()
    result_fast = arr**2 + 2*arr + 1
    fast_time = time.time() - start

    print(f"Python loop: {slow_time*1000:.0f} ms")
    print(f"Vectorized:  {fast_time*1000:.0f} ms")
    print(f"Speedup: {slow_time/fast_time:.0f}x faster!")

    print("""
    \nWhy vectorized is faster:
    1. NumPy uses CPU SIMD instructions
    2. No Python interpreter overhead per element
    3. Contiguous memory (cache friendly)
    4. Optimized C code underneath
    """)

    # ============================================================================
    # Memory Efficiency
    # ============================================================================

    print("\n" + "="*80)
    print("Memory Efficiency (Topic #24)")
    print("="*80)

    # Use appropriate dtype
    arr_default = np.arange(1000)
    arr_int16 = np.arange(1000, dtype=np.int16)

    print(f"Default int: {arr_default.nbytes:,} bytes")
    print(f"int16: {arr_int16.nbytes:,} bytes")
    print(f"Savings: {100*(1 - arr_int16.nbytes/arr_default.nbytes):.0f}%")

    # Reuse arrays instead of creating new ones
    print("\nReuse arrays (avoid allocations):")
    result = np.zeros(1000)
    for i in range(100):
        result[:] = np.random.rand(1000) * 2  # Reuse memory!
    print("  Use arr[:] = ... to reuse memory")

    print("""
    \n🎯 PERFORMANCE TIPS:
    1. Use vectorization (eliminate loops!)
    2. Choose appropriate dtype
    3. Reuse arrays when possible
    4. Use views instead of copies
    5. Profile before optimizing!
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
