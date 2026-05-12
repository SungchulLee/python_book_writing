# Performance Implications of Broadcasting

Broadcasting is not just a syntactic convenience. It has real consequences for execution speed and memory consumption. In the best case, broadcasting eliminates both Python-level loops and unnecessary data copies, yielding orders-of-magnitude speedups. In the worst case, a broadcasted operation can silently allocate a temporary array far larger than either input. This page examines both sides so that the reader can use broadcasting effectively.

!!! tip "Mental Model"
    Broadcasting gives you C-level speed by avoiding Python loops, but the output array can be much larger than either input. A `(10000, 1)` array broadcast against `(1, 10000)` silently creates a 100-million-element result. Always check the resulting shape mentally before running a broadcasted operation on large data.

---

## Speed vs Python Loops

Broadcasting replaces Python-level iteration with optimized C code inside NumPy.

### 1. Loop Baseline

```python
import numpy as np
import time

def add_loop(M, v):
    result = np.empty_like(M)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            result[i, j] = M[i, j] + v[j]
    return result

def main():
    M = np.random.randn(1000, 1000)
    v = np.random.randn(1000)

    start = time.perf_counter()
    result = add_loop(M, v)
    elapsed = time.perf_counter() - start
    print(f"Loop time: {elapsed:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Broadcasting Baseline

```python
import numpy as np
import time

def main():
    M = np.random.randn(1000, 1000)
    v = np.random.randn(1000)

    start = time.perf_counter()
    result = M + v
    elapsed = time.perf_counter() - start
    print(f"Broadcast time: {elapsed:.6f} sec")

if __name__ == "__main__":
    main()
```

### 3. Comparison

```python
import numpy as np
import time

def add_loop(M, v):
    result = np.empty_like(M)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            result[i, j] = M[i, j] + v[j]
    return result

def main():
    np.random.seed(42)
    M = np.random.randn(1000, 1000)
    v = np.random.randn(1000)

    start = time.perf_counter()
    r1 = add_loop(M, v)
    loop_time = time.perf_counter() - start

    start = time.perf_counter()
    r2 = M + v
    bc_time = time.perf_counter() - start

    assert np.allclose(r1, r2)
    print(f"Loop:      {loop_time:.4f} sec")
    print(f"Broadcast: {bc_time:.6f} sec")
    print(f"Speedup:   {loop_time / bc_time:.0f}x")

if __name__ == "__main__":
    main()
```

Typical output:

```
Loop:      0.3500 sec
Broadcast: 0.001200 sec
Speedup:   292x
```


## Memory Efficiency

Broadcasting avoids duplicating data when possible through NumPy's stride mechanism.

### 1. No-Copy Expansion

When NumPy broadcasts, it sets the stride to 0 along the expanded axis. The data is read repeatedly without being copied.

```python
import numpy as np

def main():
    v = np.array([1, 2, 3])
    expanded = np.broadcast_to(v, (1000, 3))
    print(f"Original size:  {v.nbytes} bytes")
    print(f"Broadcast size: {expanded.nbytes} bytes")
    print(f"Actual memory:  {v.nbytes} bytes (shared)")
    print(f"Strides: {expanded.strides}")  # (0, 8) — stride 0 on axis 0

if __name__ == "__main__":
    main()
```

Output:

```
Original size:  24 bytes
Broadcast size: 24000 bytes
Actual memory:  24 bytes (shared)
Strides: (0, 8)
```

### 2. When Copies Happen

The zero-stride trick only works for read access. Any arithmetic operation that produces output allocates a new result array at the full broadcast size:

```python
import numpy as np

def main():
    M = np.ones((10000, 10000))                   # 800 MB
    v = np.array([1.0])                             # 8 bytes
    result = M + v  # allocates another 800 MB for output
    print(f"M memory:      {M.nbytes / 1e6:.0f} MB")
    print(f"result memory: {result.nbytes / 1e6:.0f} MB")

if __name__ == "__main__":
    main()
```

### 3. In-Place Operations Save Memory

```python
import numpy as np

def main():
    M = np.ones((5000, 5000))
    v = np.array([1, 2, 3, 4, 5] * 1000)  # (5000,)
    M += v  # in-place: no new array allocated
    print(f"M.shape = {M.shape}")

if __name__ == "__main__":
    main()
```


## Temporary Array Explosion

Broadcasting can create unexpectedly large intermediate arrays.

### 1. Pairwise Distance Anti-Pattern

```python
import numpy as np

def main():
    n = 10000
    d = 3
    X = np.random.randn(n, d)

    # This creates a (10000, 10000, 3) intermediate — 2.4 GB!
    # diff = X[:, np.newaxis, :] - X[np.newaxis, :, :]

    # For large n, use scipy instead
    from scipy.spatial.distance import cdist
    dist = cdist(X, X)
    print(f"dist.shape = {dist.shape}")
    print(f"dist memory: {dist.nbytes / 1e6:.0f} MB")

if __name__ == "__main__":
    main()
```

### 2. Estimating Temporary Size

Before running a broadcast, estimate the result size:

```python
import numpy as np

def main():
    shape_a = (1000, 1, 500)
    shape_b = (1, 2000, 500)
    result_shape = np.broadcast_shapes(shape_a, shape_b)
    n_elements = np.prod(result_shape)
    memory_bytes = n_elements * 8  # float64
    print(f"Result shape: {result_shape}")
    print(f"Memory: {memory_bytes / 1e9:.2f} GB")

if __name__ == "__main__":
    main()
```

Output:

```
Result shape: (1000, 2000, 500)
Memory: 8.00 GB
```

### 3. Chunked Processing

When the broadcast result is too large, process in chunks:

```python
import numpy as np

def main():
    A = np.random.randn(10000, 100)
    B = np.random.randn(10000, 100)

    # Instead of one giant operation, process in chunks
    chunk_size = 1000
    results = []
    for i in range(0, len(A), chunk_size):
        chunk_a = A[i:i + chunk_size, np.newaxis, :]
        diff = chunk_a - B[np.newaxis, :, :]
        dist_chunk = np.sqrt((diff ** 2).sum(axis=2))
        results.append(dist_chunk)
    # Each chunk is (1000, 10000) instead of (10000, 10000)

if __name__ == "__main__":
    main()
```


## Contiguous Memory and Cache Effects

Array memory layout affects broadcasting speed.

### 1. C-Order vs Fortran-Order

```python
import numpy as np
import time

def main():
    n = 5000
    C_arr = np.ones((n, n), order='C')   # row-major
    F_arr = np.ones((n, n), order='F')   # column-major
    v = np.ones(n)

    # Row broadcast: v has shape (n,) — aligns with last axis
    start = time.perf_counter()
    for _ in range(10):
        _ = C_arr + v
    c_time = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(10):
        _ = F_arr + v
    f_time = time.perf_counter() - start

    print(f"C-order:       {c_time:.4f} sec")
    print(f"Fortran-order: {f_time:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Why Layout Matters

Broadcasting along the last axis reads contiguous memory in C-order arrays, which is cache-friendly. Fortran-order arrays store data column-major, so the same operation accesses memory with larger strides.

### 3. Check Array Flags

```python
import numpy as np

def main():
    A = np.ones((3, 4))
    print(f"C_CONTIGUOUS: {A.flags['C_CONTIGUOUS']}")
    print(f"F_CONTIGUOUS: {A.flags['F_CONTIGUOUS']}")
    print(f"Strides: {A.strides}")

if __name__ == "__main__":
    main()
```


## When to Avoid Broadcasting

Broadcasting is not always the best approach.

### 1. Very Large Temporaries

If the broadcast result exceeds available memory, use `scipy` functions or chunked processing instead of raw broadcasting.

### 2. Repeated Operations

For repeated broadcasts of the same shape, pre-allocating with `np.empty` and using the `out` parameter avoids repeated allocation:

```python
import numpy as np

def main():
    M = np.random.randn(1000, 1000)
    v = np.random.randn(1000)
    out = np.empty_like(M)

    for _ in range(100):
        np.add(M, v, out=out)  # reuses pre-allocated output

    print(f"out.shape = {out.shape}")

if __name__ == "__main__":
    main()
```

### 3. Sparse Data

If most values are zero, sparse matrices (`scipy.sparse`) are more memory-efficient than dense broadcasting.


## Rules of Thumb

!!! tip "Performance Quick Reference"

    1. **Broadcasting vs loops:** expect 100-1000x speedup over Python `for` loops on arrays larger than ~1000 elements.
    2. **Memory check first:** before broadcasting, estimate `np.prod(result_shape) * 8` bytes. If it exceeds ~25% of RAM, chunk or use `scipy`.
    3. **In-place when possible:** `M += v` avoids allocating a new array; `np.add(M, v, out=M)` does the same.
    4. **C-order + last-axis broadcast** is fastest — this is the default and cache-friendly layout.
    5. **Avoid giant intermediates:** pairwise distance on 10k points creates a 2.4 GB temporary. Use `scipy.spatial.distance.cdist` instead.
    6. **Pre-allocate for loops:** if you broadcast repeatedly in a loop, create `out = np.empty(...)` once and reuse via the `out` parameter.

## Summary

Broadcasting provides substantial speedups (100-1000x over Python loops) and avoids unnecessary data copies through zero-stride expansion. The main performance risk is temporary array explosion, where an intermediate result is far larger than either input. Estimate output sizes before broadcasting, use in-place operations when possible, and fall back to chunked processing or specialized libraries for very large pairwise computations.

---

## Exercises

**Exercise 1.**
Use `np.broadcast_shapes` and `np.prod` to estimate the memory in megabytes of the result of broadcasting arrays with shapes `(500, 1, 200)` and `(1, 300, 200)` assuming `float64` dtype. Would this fit in 1 GB of RAM?

??? success "Solution to Exercise 1"

        import numpy as np

        shape = np.broadcast_shapes((500, 1, 200), (1, 300, 200))
        n_elements = np.prod(shape)
        memory_bytes = n_elements * 8  # float64
        memory_mb = memory_bytes / 1e6
        print(f"Result shape: {shape}")            # (500, 300, 200)
        print(f"Memory: {memory_mb:.1f} MB")       # 240.0 MB
        print(f"Fits in 1 GB: {memory_mb < 1000}") # True

---

**Exercise 2.**
Given `M = np.random.randn(5000, 5000)` and `v = np.random.randn(5000)`, compare the memory usage of `M + v` (which allocates a new array) versus `M += v` (in-place). Measure the wall-clock time of each approach over 5 repetitions and print the speedup factor.

??? success "Solution to Exercise 2"

        import numpy as np
        import time

        M = np.random.randn(5000, 5000)
        v = np.random.randn(5000)

        # Out-of-place
        start = time.perf_counter()
        for _ in range(5):
            result = M + v
        t_copy = time.perf_counter() - start

        # In-place
        M2 = M.copy()
        start = time.perf_counter()
        for _ in range(5):
            M2 += v
        t_inplace = time.perf_counter() - start

        print(f"Out-of-place: {t_copy:.4f} sec")
        print(f"In-place:     {t_inplace:.4f} sec")
        print(f"Speedup:      {t_copy / t_inplace:.2f}x")

---

**Exercise 3.**
Implement a chunked pairwise Euclidean distance computation for `X = np.random.randn(5000, 3)` using chunks of size 500 along axis 0. Concatenate the chunks vertically to form the full `(5000, 5000)` distance matrix. Print the total memory saved compared to creating the full `(5000, 5000, 3)` intermediate in one step.

??? success "Solution to Exercise 3"

        import numpy as np

        X = np.random.randn(5000, 3)
        chunk_size = 500
        n = len(X)

        chunks = []
        for i in range(0, n, chunk_size):
            diff = X[i:i+chunk_size, np.newaxis, :] - X[np.newaxis, :, :]
            dist_chunk = np.sqrt((diff ** 2).sum(axis=2))
            chunks.append(dist_chunk)

        dist_full = np.concatenate(chunks, axis=0)
        print(f"Distance matrix shape: {dist_full.shape}")  # (5000, 5000)

        # Memory comparison
        full_intermediate = 5000 * 5000 * 3 * 8  # bytes
        chunk_intermediate = chunk_size * 5000 * 3 * 8
        saved_bytes = full_intermediate - chunk_intermediate
        print(f"Full intermediate:  {full_intermediate / 1e6:.1f} MB")
        print(f"Chunk intermediate: {chunk_intermediate / 1e6:.1f} MB")
        print(f"Memory saved:       {saved_bytes / 1e6:.1f} MB")

---

**Exercise 4.**
Compare `np.add(M, v, out=M)` versus `M = M + v` in a loop of 100 iterations for `M` of shape `(2000, 2000)`. Measure wall-clock time for each approach and explain why the `out` parameter version is faster.

??? success "Solution to Exercise 4"

        import numpy as np
        import time

        M_orig = np.random.randn(2000, 2000)
        v = np.random.randn(2000)

        # Approach 1: M = M + v (allocates new array each iteration)
        M1 = M_orig.copy()
        start = time.perf_counter()
        for _ in range(100):
            M1 = M1 + v
        t_alloc = time.perf_counter() - start

        # Approach 2: np.add with out (reuses same array)
        M2 = M_orig.copy()
        start = time.perf_counter()
        for _ in range(100):
            np.add(M2, v, out=M2)
        t_out = time.perf_counter() - start

        print(f"New array each time: {t_alloc:.4f} sec")
        print(f"Reuse via out:       {t_out:.4f} sec")
        print(f"Speedup:             {t_alloc / t_out:.2f}x")

        # The `out` version is faster because:
        # 1. No memory allocation per iteration (allocation is expensive)
        # 2. Better cache locality (same memory region reused)
        # 3. No garbage collection pressure from temporary arrays

---

**Exercise 5.**
Estimate whether the following pairwise operation will fit in 16 GB of RAM: `X[:, None, :] - X[None, :, :]` where `X` has shape `(20000, 50)` and dtype `float64`. Calculate the intermediate size in GB. If it does not fit, implement a chunked version that processes 1000 rows at a time.

??? success "Solution to Exercise 5"

        import numpy as np

        n, d = 20000, 50

        # Intermediate shape: (20000, 20000, 50)
        n_elements = n * n * d
        memory_gb = n_elements * 8 / 1e9
        print(f"Intermediate: ({n}, {n}, {d})")
        print(f"Memory: {memory_gb:.1f} GB")  # 160.0 GB — does NOT fit!

        # Chunked version
        X = np.random.randn(n, d)
        chunk_size = 1000
        dist_rows = []

        for i in range(0, n, chunk_size):
            chunk = X[i:i+chunk_size]  # (1000, 50)
            diff = chunk[:, None, :] - X[None, :, :]  # (1000, 20000, 50)
            dist_chunk = np.sqrt((diff ** 2).sum(axis=2))  # (1000, 20000)
            dist_rows.append(dist_chunk)
            # Each chunk uses: 1000 * 20000 * 50 * 8 = 8 GB — marginal
            # Reduce chunk_size to 500 for safer memory

        # For this problem, scipy.spatial.distance.cdist is the practical choice:
        # from scipy.spatial.distance import cdist
        # dist = cdist(X, X)  # memory-efficient, uses (20000, 20000) only
