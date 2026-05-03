# Memory Preallocation

Preallocate arrays before iterative population to avoid dynamic allocation overhead.

!!! tip "Mental Model"
    Growing an array inside a loop (via `np.append` or `np.concatenate`) copies the entire array on every iteration, turning O(n) work into O(n^2). Preallocating with `np.empty` or `np.zeros` and filling by index keeps work at O(n). Always allocate first, then fill.


## The Problem

Dynamic allocation in loops causes catastrophic inefficiency.

### 1. Bad Pattern

```python
import numpy as np

def build_array_bad(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return np.array(result)
```

### 2. Why It's Slow

- Each `append` may trigger reallocation
- Memory fragmentation increases
- Type conversion at the end adds overhead

### 3. Hidden Cost

Python lists store pointers, not contiguous data.


## Preallocation Solution

Allocate the full array before the loop.

### 1. Good Pattern

```python
import numpy as np

def build_array_good(n):
    result = np.empty(n, dtype=np.float64)
    for i in range(n):
        result[i] = i ** 2
    return result
```

### 2. Why It's Fast

- Single allocation upfront
- Contiguous memory access
- No type conversion needed

### 3. Best Pattern

```python
import numpy as np

def build_array_best(n):
    return np.arange(n) ** 2  # Fully vectorized
```


## Timing Comparison

Measure the performance difference.

### 1. Benchmark Code

```python
import numpy as np
import time

def with_append(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return np.array(result)

def with_prealloc(n):
    result = np.empty(n, dtype=np.int64)
    for i in range(n):
        result[i] = i ** 2
    return result

def main():
    n = 100_000
    
    start = time.perf_counter()
    _ = with_append(n)
    append_time = time.perf_counter() - start
    
    start = time.perf_counter()
    _ = with_prealloc(n)
    prealloc_time = time.perf_counter() - start
    
    print(f"Append time:     {append_time:.4f} sec")
    print(f"Prealloc time:   {prealloc_time:.4f} sec")
    print(f"Speedup:         {append_time / prealloc_time:.1f}x")

if __name__ == "__main__":
    main()
```

### 2. Typical Results

```
Append time:     0.0450 sec
Prealloc time:   0.0120 sec
Speedup:         3.8x
```


## Allocation Functions

Choose the right function for preallocation.

### 1. np.empty

```python
import numpy as np

arr = np.empty((1000, 1000))  # Fastest, uninitialized
```

No initialization; use when you'll overwrite all values.

### 2. np.zeros

```python
import numpy as np

arr = np.zeros((1000, 1000))  # Initialized to zero
```

Safe default when partial filling is possible.

### 3. np.empty_like

```python
import numpy as np

template = np.random.randn(100, 100)
arr = np.empty_like(template)  # Match shape and dtype
```


## 2D Preallocation

Apply preallocation to multi-dimensional arrays.

### 1. Matrix Building

```python
import numpy as np

def build_matrix(rows, cols):
    result = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        for j in range(cols):
            result[i, j] = i * cols + j
    return result
```

### 2. Row-wise Building

```python
import numpy as np

def build_by_rows(rows, cols):
    result = np.empty((rows, cols), dtype=np.float64)
    for i in range(rows):
        result[i, :] = np.arange(cols) + i * cols
    return result
```

### 3. Fully Vectorized

```python
import numpy as np

def build_vectorized(rows, cols):
    return np.arange(rows * cols).reshape(rows, cols)
```


## Best Practices

Guidelines for effective preallocation.

### 1. Know Final Size

Preallocation requires knowing dimensions upfront.

### 2. Specify dtype

Always specify dtype to avoid implicit conversions.

### 3. Prefer Vectorization

Preallocation helps loops, but vectorization eliminates them.

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
