# Acceleration Libraries

External libraries provide additional speedups beyond pure NumPy.

!!! tip "Mental Model"
    When NumPy alone is not fast enough, acceleration libraries extend the
    [optimization hierarchy](vectorization_basics.md) with a **scaling layer** that
    pushes computation closer to hardware. Each library targets a different
    bottleneck in the execution pipeline:

    ```text
    Python loop → NumPy (C loops) → Acceleration
                                        │
                                ┌───────┼───────┐
                            Numba    numexpr    CuPy / Dask
                           compile    fuse      offload
                           loops    expressions  to GPU/cluster
    ```

!!! note "Decision Framework — When to Use Which"
    | Bottleneck | Tool | What it does |
    |-----------|------|-------------|
    | Python loops that resist vectorization | **Numba** | JIT-compiles Python to machine code |
    | Large expressions with temporaries | **numexpr** | Fuses element-wise ops, avoids intermediate arrays |
    | Data too large for one CPU | **Dask** | Parallelizes across cores or a cluster |
    | Need GPU acceleration | **CuPy** | Drop-in NumPy replacement on NVIDIA GPUs |
    | Already vectorized, still slow | **Profile first** | The bottleneck may be I/O or algorithm, not execution |

## numexpr

Optimized evaluation of array expressions.

### 1. Installation

```bash
pip install numexpr
```

### 2. Basic Usage

```python
import numpy as np
import numexpr as ne

def main():
    a = np.random.randn(1_000_000)
    b = np.random.randn(1_000_000)
    
    # NumPy (creates temporaries)
    result_np = 2 * a + 3 * b ** 2
    
    # numexpr (avoids temporaries)
    result_ne = ne.evaluate("2 * a + 3 * b ** 2")

if __name__ == "__main__":
    main()
```

### 3. Why It's Faster

- Avoids intermediate array allocations
- Uses multiple CPU cores automatically
- Optimizes memory access patterns

## numexpr Benchmark

Compare numexpr vs pure NumPy.

### 1. Timing Code

```python
import numpy as np
import numexpr as ne
import time

def main():
    n = 10_000_000
    a = np.random.randn(n)
    b = np.random.randn(n)
    
    # NumPy timing
    start = time.perf_counter()
    for _ in range(10):
        result = 2 * a + 3 * b ** 2
    np_time = time.perf_counter() - start
    
    # numexpr timing
    start = time.perf_counter()
    for _ in range(10):
        result = ne.evaluate("2 * a + 3 * b ** 2")
    ne_time = time.perf_counter() - start
    
    print(f"NumPy time:   {np_time:.4f} sec")
    print(f"numexpr time: {ne_time:.4f} sec")
    print(f"Speedup:      {np_time/ne_time:.1f}x")

if __name__ == "__main__":
    main()
```

### 2. Typical Speedup

2-10x faster for complex expressions with large arrays.

## Numba

Just-in-time compilation for Python functions.

### 1. Installation

```bash
pip install numba
```

### 2. Basic JIT

```python
import numpy as np
from numba import jit

@jit(nopython=True)
def sum_squares(arr):
    total = 0.0
    for i in range(len(arr)):
        total += arr[i] ** 2
    return total

def main():
    arr = np.random.randn(1_000_000)
    result = sum_squares(arr)  # First call compiles
    result = sum_squares(arr)  # Subsequent calls fast

if __name__ == "__main__":
    main()
```

### 3. nopython Mode

`nopython=True` ensures full compilation without Python fallback.

## Numba Parallel

Automatic parallelization with Numba.

### 1. Parallel Loop

```python
import numpy as np
from numba import jit, prange

@jit(nopython=True, parallel=True)
def parallel_sum(arr):
    total = 0.0
    for i in prange(len(arr)):
        total += arr[i] ** 2
    return total

def main():
    arr = np.random.randn(10_000_000)
    result = parallel_sum(arr)

if __name__ == "__main__":
    main()
```

### 2. prange

Use `prange` instead of `range` for parallel iteration.

### 3. Multi-core Speedup

Automatically distributes work across CPU cores.

## Cython

Static typing and C compilation for Python code.

### 1. Installation

```bash
pip install cython
```

### 2. Cython File (.pyx)

```cython
# sum_squares.pyx
import numpy as np
cimport numpy as np

def sum_squares_cy(np.ndarray[np.float64_t, ndim=1] arr):
    cdef double total = 0.0
    cdef int i
    cdef int n = arr.shape[0]
    
    for i in range(n):
        total += arr[i] ** 2
    
    return total
```

### 3. Compilation

Requires setup.py or build configuration to compile.

## Dask

Parallel computing for larger-than-memory datasets.

### 1. Installation

```bash
pip install dask[array]
```

### 2. Basic Usage

```python
import numpy as np
import dask.array as da

def main():
    # Create Dask array from NumPy
    x_np = np.random.randn(10000, 10000)
    x_dask = da.from_array(x_np, chunks=(1000, 1000))
    
    # Operations are lazy
    result = (x_dask ** 2).sum()
    
    # Compute triggers execution
    print(f"Result: {result.compute():.4f}")

if __name__ == "__main__":
    main()
```

### 3. Chunked Processing

```python
import dask.array as da

def main():
    # Create large array directly
    x = da.random.random((50000, 50000), chunks=(5000, 5000))
    
    print(f"Array shape: {x.shape}")
    print(f"Chunk shape: {x.chunksize}")
    
    # Compute mean (processes in chunks)
    mean = x.mean().compute()
    print(f"Mean: {mean:.6f}")

if __name__ == "__main__":
    main()
```

## Dask Benefits

### 1. Out-of-Core Computing

Process data larger than RAM by working in chunks.

```python
import dask.array as da

def main():
    # 100GB array (doesn't fit in memory)
    x = da.random.random((100000, 100000), chunks=(10000, 10000))
    
    # Still computable via chunking
    result = x.mean().compute()
    print(f"Mean of 100GB array: {result:.6f}")

if __name__ == "__main__":
    main()
```

### 2. Parallel Execution

```python
import dask.array as da
from dask.distributed import Client

def main():
    # Start local cluster
    client = Client()
    print(f"Dashboard: {client.dashboard_link}")
    
    x = da.random.random((20000, 20000), chunks=(2000, 2000))
    result = (x @ x.T).mean().compute()
    
    print(f"Result: {result:.4f}")

if __name__ == "__main__":
    main()
```

### 3. NumPy API Compatibility

Most NumPy operations work seamlessly with Dask arrays.

## CuPy

GPU-accelerated NumPy-compatible arrays.

### 1. Installation

```bash
pip install cupy-cuda11x  # Match your CUDA version
```

### 2. Basic Usage

```python
import numpy as np
import cupy as cp

def main():
    # Create array on GPU
    x_gpu = cp.random.randn(10000, 10000)
    
    # Operations run on GPU
    result_gpu = x_gpu @ x_gpu.T
    
    # Transfer back to CPU if needed
    result_cpu = cp.asnumpy(result_gpu)
    
    print(f"Result shape: {result_cpu.shape}")

if __name__ == "__main__":
    main()
```

### 3. NumPy to CuPy

```python
import numpy as np
import cupy as cp

def main():
    # NumPy array on CPU
    x_np = np.random.randn(5000, 5000)
    
    # Transfer to GPU
    x_gpu = cp.asarray(x_np)
    
    # Compute on GPU
    result_gpu = cp.linalg.svd(x_gpu, full_matrices=False)
    
    # Transfer result back
    U, s, Vt = [cp.asnumpy(arr) for arr in result_gpu]
    
    print(f"Singular values shape: {s.shape}")

if __name__ == "__main__":
    main()
```

## CuPy Benchmark

### 1. Matrix Multiply

```python
import numpy as np
import cupy as cp
import time

def main():
    n = 5000
    
    # CPU (NumPy)
    a_np = np.random.randn(n, n).astype(np.float32)
    b_np = np.random.randn(n, n).astype(np.float32)
    
    start = time.perf_counter()
    c_np = a_np @ b_np
    cpu_time = time.perf_counter() - start
    
    # GPU (CuPy)
    a_gpu = cp.asarray(a_np)
    b_gpu = cp.asarray(b_np)
    
    # Warm-up
    _ = a_gpu @ b_gpu
    cp.cuda.Stream.null.synchronize()
    
    start = time.perf_counter()
    c_gpu = a_gpu @ b_gpu
    cp.cuda.Stream.null.synchronize()
    gpu_time = time.perf_counter() - start
    
    print(f"CPU time: {cpu_time:.4f} sec")
    print(f"GPU time: {gpu_time:.4f} sec")
    print(f"Speedup:  {cpu_time/gpu_time:.1f}x")

if __name__ == "__main__":
    main()
```

### 2. Typical Speedup

10-100x faster for large matrix operations on modern GPUs.

### 3. Memory Considerations

GPU memory is limited; check available memory with `cp.cuda.runtime.memGetInfo()`.

## Comparison Table

Choose the right tool for your needs.

### 1. Summary

| Library | Use Case | Speedup | Hardware |
|:--------|:---------|:--------|:---------|
| numexpr | Array expressions | 2-10x | CPU |
| Numba | Numerical loops | 10-100x | CPU |
| Cython | General Python | 10-100x | CPU |
| Dask | Large datasets | Parallel | CPU cluster |
| CuPy | Matrix operations | 10-100x | GPU |

### 2. Decision Guide

- **Small data, complex expressions**: numexpr
- **Loops that can't vectorize**: Numba
- **Data larger than RAM**: Dask
- **Large matrices, have GPU**: CuPy

### 3. Combinations

Libraries can be combined (e.g., Dask + CuPy for distributed GPU).

## Best Practices

Guidelines for using acceleration libraries.

### 1. Profile First

Identify bottlenecks before adding dependencies.

### 2. Start Simple

Try numexpr before Numba; try Numba before Cython.

### 3. Test Correctness

Verify results match original implementation.

### 4. Consider Trade-offs

- CuPy: Requires NVIDIA GPU
- Dask: Adds complexity for small data
- Numba: First call has compilation overhead

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
