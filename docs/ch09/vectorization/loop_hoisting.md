# Loop Hoisting

Loop hoisting moves invariant computations outside inner loops for better performance.

!!! tip "Mental Model"
    If a computation inside a loop produces the same result every iteration, compute it once before the loop starts. This "hoisting" technique is simple but high-impact: it turns O(n) redundant work into O(1). In NumPy code, hoisting often means precomputing arrays or constants that are reused across iterations.

    In the [optimization hierarchy](vectorization_basics.md), hoisting is a **loop
    optimization step that precedes full vectorization**. When you cannot eliminate
    a loop entirely, hoisting invariants out of it is the next best thing — it
    reduces the cost per iteration, making the remaining loop as cheap as possible
    before you attempt to replace it with array operations.

## Concept

### 1. What is Hoisting

Moving calculations that don't depend on the loop variable outside the loop.

### 2. Why It Helps

Avoids redundant recomputation on every iteration.

### 3. Common Pattern

```python
# Before hoisting
for i in range(n):
    for j in range(m):
        val = expensive(i)  # Doesn't depend on j
        result[i, j] = val + something(j)

# After hoisting
for i in range(n):
    val = expensive(i)  # Computed once per i
    for j in range(m):
        result[i, j] = val + something(j)
```

## Image Normalization

### 1. Problem Setup

Normalize each row of an image by its mean and standard deviation.

```python
import numpy as np

def main():
    # Simulated image: (height, width, channels)
    img = np.random.randint(0, 256, size=(100, 150, 3), dtype=np.uint8)
    print(f"Image shape: {img.shape}")

if __name__ == "__main__":
    main()
```

### 2. Normalization Formula

For each pixel $(i, j)$:

$$\text{normalized}_{i,j} = \frac{\text{pixel}_{i,j} - \mu_i}{\sigma_i + \epsilon}$$

where $\mu_i$ and $\sigma_i$ are the mean and std of row $i$.

### 3. Key Observation

Row statistics $\mu_i$ and $\sigma_i$ don't depend on column $j$.

## Naive Implementation

### 1. Code

```python
import numpy as np
import time

def main():
    np.random.seed(42)
    img = np.random.randint(0, 256, size=(400, 600, 3), dtype=np.uint8)
    img_float = img.astype(np.float64)
    result = np.empty_like(img_float)
    
    ep = 1e-6
    
    tic = time.time()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            row_mean = np.mean(img[i, :, :], axis=0)  # Recomputed!
            row_std = np.std(img[i, :, :], axis=0)   # Recomputed!
            result[i, j, :] = (img_float[i, j, :] - row_mean) / (row_std + ep)
    toc = time.time()
    
    print(f"Naive Time: {toc - tic:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Problem

`row_mean` and `row_std` are recalculated for every pixel in the row.

### 3. Redundant Work

For a 400×600 image, statistics are computed 600× more than necessary per row.

## Loop Hoisting

### 1. Code

```python
import numpy as np
import time

def main():
    np.random.seed(42)
    img = np.random.randint(0, 256, size=(400, 600, 3), dtype=np.uint8)
    img_float = img.astype(np.float64)
    result = np.empty_like(img_float)
    
    ep = 1e-6
    
    tic = time.time()
    for i in range(img.shape[0]):
        row_mean = np.mean(img[i, :, :], axis=0)  # Hoisted!
        row_std = np.std(img[i, :, :], axis=0)   # Hoisted!
        for j in range(img.shape[1]):
            result[i, j, :] = (img_float[i, j, :] - row_mean) / (row_std + ep)
    toc = time.time()
    
    print(f"Hoisted Time: {toc - tic:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Improvement

Statistics computed once per row, not once per pixel.

### 3. Typical Speedup

5-10× faster than naive implementation.

## Full Vectorization

### 1. Code

```python
import numpy as np
import time

def main():
    np.random.seed(42)
    img = np.random.randint(0, 256, size=(400, 600, 3), dtype=np.uint8)
    img_float = img.astype(np.float64)
    
    ep = 1e-6
    
    tic = time.time()
    # keepdims=True enables broadcasting
    mean = np.mean(img_float, axis=1, keepdims=True)  # (400, 1, 3)
    std = np.std(img_float, axis=1, keepdims=True)    # (400, 1, 3)
    result = (img_float - mean) / (std + ep)
    toc = time.time()
    
    print(f"Vectorized Time: {toc - tic:.6f} sec")
    print(f"mean shape: {mean.shape}")
    print(f"std shape: {std.shape}")

if __name__ == "__main__":
    main()
```

### 2. Key Technique

`keepdims=True` preserves dimensions for broadcasting.

### 3. Typical Speedup

100-1000× faster than naive, 10-100× faster than hoisted.

## Comparison

### 1. Full Benchmark

```python
import numpy as np
import time

def main():
    np.random.seed(42)
    img = np.random.randint(0, 256, size=(200, 300, 3), dtype=np.uint8)
    img_float = img.astype(np.float64)
    ep = 1e-6
    
    # Naive
    result1 = np.empty_like(img_float)
    tic = time.time()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            row_mean = np.mean(img[i, :, :], axis=0)
            row_std = np.std(img[i, :, :], axis=0)
            result1[i, j, :] = (img_float[i, j, :] - row_mean) / (row_std + ep)
    naive_time = time.time() - tic
    
    # Hoisted
    result2 = np.empty_like(img_float)
    tic = time.time()
    for i in range(img.shape[0]):
        row_mean = np.mean(img[i, :, :], axis=0)
        row_std = np.std(img[i, :, :], axis=0)
        for j in range(img.shape[1]):
            result2[i, j, :] = (img_float[i, j, :] - row_mean) / (row_std + ep)
    hoisted_time = time.time() - tic
    
    # Vectorized
    tic = time.time()
    mean = np.mean(img_float, axis=1, keepdims=True)
    std = np.std(img_float, axis=1, keepdims=True)
    result3 = (img_float - mean) / (std + ep)
    vec_time = time.time() - tic
    
    print(f"Naive:      {naive_time:.4f} sec")
    print(f"Hoisted:    {hoisted_time:.4f} sec (×{naive_time/hoisted_time:.1f})")
    print(f"Vectorized: {vec_time:.6f} sec (×{naive_time/vec_time:.0f})")
    
    # Verify results match
    print(f"\nResults match: {np.allclose(result1, result3)}")

if __name__ == "__main__":
    main()
```

### 2. Sample Output

```
Naive:      8.2341 sec
Hoisted:    1.0234 sec (×8.0)
Vectorized: 0.0089 sec (×925)

Results match: True
```

### 3. Lessons Learned

- Loop hoisting: Easy optimization, moderate speedup
- Full vectorization: Best performance, requires rethinking the problem

## General Strategy

### 1. Identify Invariants

Find computations that don't depend on inner loop variables.

### 2. Hoist First

Move invariants outside inner loops as a quick win.

### 3. Vectorize Fully

Eliminate loops entirely using NumPy broadcasting and `keepdims`.

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
