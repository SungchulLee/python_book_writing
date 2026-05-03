# Einsum Operations

`np.einsum` provides a powerful notation for tensor contractions and array operations.

!!! tip "Mental Model"
    `einsum` uses Einstein summation convention: label each axis with a letter, and any letter that appears in the inputs but not the output is summed over. `'ij,jk->ik'` is matrix multiplication, `'ii->'` is a trace, `'ij->ji'` is a transpose. Once you learn the notation, `einsum` can express almost any array operation in a single, readable call.

## Basic Syntax

### 1. Subscript Notation

```python
import numpy as np

def main():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    # Matrix multiplication: C_ik = sum_j A_ij * B_jk
    C = np.einsum('ij,jk->ik', A, B)
    
    print("A @ B via einsum:")
    print(C)
    print()
    print("Verify with @:")
    print(A @ B)

if __name__ == "__main__":
    main()
```

### 2. Index Convention

- Repeated indices are summed (contracted)
- Output indices appear after `->`
- Free indices remain in result

### 3. Implicit vs Explicit

```python
import numpy as np

def main():
    A = np.array([[1, 2], [3, 4]])
    
    # Explicit output
    trace1 = np.einsum('ii->', A)
    
    # Implicit (same result)
    trace2 = np.einsum('ii', A)
    
    print(f"Trace (explicit): {trace1}")
    print(f"Trace (implicit): {trace2}")

if __name__ == "__main__":
    main()
```

## Common Operations

### 1. Matrix Transpose

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    # Transpose: swap indices
    AT = np.einsum('ij->ji', A)
    
    print("Original:")
    print(A)
    print()
    print("Transposed:")
    print(AT)

if __name__ == "__main__":
    main()
```

### 2. Matrix Trace

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    # Trace: sum of diagonal
    trace = np.einsum('ii->', A)
    
    print(f"einsum trace: {trace}")
    print(f"np.trace:     {np.trace(A)}")

if __name__ == "__main__":
    main()
```

### 3. Matrix Diagonal

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    # Extract diagonal
    diag = np.einsum('ii->i', A)
    
    print(f"einsum diag: {diag}")
    print(f"np.diag:     {np.diag(A)}")

if __name__ == "__main__":
    main()
```

## Vector Operations

### 1. Dot Product

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # Dot product: sum_i a_i * b_i
    dot = np.einsum('i,i->', a, b)
    
    print(f"einsum dot: {dot}")
    print(f"np.dot:     {np.dot(a, b)}")

if __name__ == "__main__":
    main()
```

### 2. Outer Product

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5])
    
    # Outer product: C_ij = a_i * b_j
    outer = np.einsum('i,j->ij', a, b)
    
    print("einsum outer:")
    print(outer)
    print()
    print("np.outer:")
    print(np.outer(a, b))

if __name__ == "__main__":
    main()
```

### 3. Element-wise Product

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # Hadamard product: c_i = a_i * b_i
    hadamard = np.einsum('i,i->i', a, b)
    
    print(f"einsum:  {hadamard}")
    print(f"a * b:   {a * b}")

if __name__ == "__main__":
    main()
```

## Matrix Operations

### 1. Matrix Multiply

```python
import numpy as np

def main():
    A = np.random.randn(3, 4)
    B = np.random.randn(4, 5)
    
    # C_ik = sum_j A_ij * B_jk
    C = np.einsum('ij,jk->ik', A, B)
    
    print(f"Shape: {C.shape}")
    print(f"Matches A @ B: {np.allclose(C, A @ B)}")

if __name__ == "__main__":
    main()
```

### 2. Batch Matrix Multiply

```python
import numpy as np

def main():
    # Batch of matrices: (batch, rows, cols)
    A = np.random.randn(10, 3, 4)
    B = np.random.randn(10, 4, 5)
    
    # Batch matmul: C_bij = sum_k A_bik * B_bkj
    C = np.einsum('bik,bkj->bij', A, B)
    
    print(f"A shape: {A.shape}")
    print(f"B shape: {B.shape}")
    print(f"C shape: {C.shape}")

if __name__ == "__main__":
    main()
```

### 3. Matrix-Vector Product

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6]])
    x = np.array([1, 2, 3])
    
    # y_i = sum_j A_ij * x_j
    y = np.einsum('ij,j->i', A, x)
    
    print(f"einsum: {y}")
    print(f"A @ x:  {A @ x}")

if __name__ == "__main__":
    main()
```

## Tensor Contractions

### 1. 3D Tensor Sum

```python
import numpy as np

def main():
    T = np.random.randn(3, 4, 5)
    
    # Sum over all indices
    total = np.einsum('ijk->', T)
    
    print(f"einsum sum: {total:.4f}")
    print(f"np.sum:     {np.sum(T):.4f}")

if __name__ == "__main__":
    main()
```

### 2. Partial Contraction

```python
import numpy as np

def main():
    T = np.random.randn(3, 4, 5)
    
    # Sum over middle index: R_ik = sum_j T_ijk
    R = np.einsum('ijk->ik', T)
    
    print(f"Original shape: {T.shape}")
    print(f"Result shape:   {R.shape}")
    print(f"Matches sum:    {np.allclose(R, T.sum(axis=1))}")

if __name__ == "__main__":
    main()
```

### 3. Tensor Product

```python
import numpy as np

def main():
    A = np.random.randn(2, 3)
    B = np.random.randn(4, 5)
    
    # Tensor (Kronecker-like) product
    C = np.einsum('ij,kl->ijkl', A, B)
    
    print(f"A shape: {A.shape}")
    print(f"B shape: {B.shape}")
    print(f"C shape: {C.shape}")

if __name__ == "__main__":
    main()
```

## Performance

### 1. Optimize Flag

```python
import numpy as np
import time

def main():
    A = np.random.randn(100, 100)
    B = np.random.randn(100, 100)
    C = np.random.randn(100, 100)
    
    # Without optimization
    start = time.perf_counter()
    for _ in range(100):
        D = np.einsum('ij,jk,kl->il', A, B, C)
    time1 = time.perf_counter() - start
    
    # With optimization
    start = time.perf_counter()
    for _ in range(100):
        D = np.einsum('ij,jk,kl->il', A, B, C, optimize=True)
    time2 = time.perf_counter() - start
    
    print(f"Without optimize: {time1:.4f} sec")
    print(f"With optimize:    {time2:.4f} sec")
    print(f"Speedup:          {time1/time2:.1f}x")

if __name__ == "__main__":
    main()
```

### 2. Path Optimization

```python
import numpy as np

def main():
    A = np.random.randn(10, 20)
    B = np.random.randn(20, 30)
    C = np.random.randn(30, 40)
    
    # Get optimized contraction path
    path, info = np.einsum_path('ij,jk,kl->il', A, B, C, optimize='optimal')
    
    print("Contraction path:")
    print(path)
    print()
    print(info)

if __name__ == "__main__":
    main()
```

### 3. vs Native Operations

```python
import numpy as np
import time

def main():
    A = np.random.randn(1000, 1000)
    B = np.random.randn(1000, 1000)
    
    # einsum
    start = time.perf_counter()
    C1 = np.einsum('ij,jk->ik', A, B, optimize=True)
    einsum_time = time.perf_counter() - start
    
    # Native matmul
    start = time.perf_counter()
    C2 = A @ B
    matmul_time = time.perf_counter() - start
    
    print(f"einsum time: {einsum_time:.4f} sec")
    print(f"matmul time: {matmul_time:.4f} sec")
    print(f"Results match: {np.allclose(C1, C2)}")

if __name__ == "__main__":
    main()
```

## Practical Examples

### 1. Attention Scores

```python
import numpy as np

def main():
    # Query, Key, Value matrices
    batch, seq_len, d_model = 2, 10, 64
    
    Q = np.random.randn(batch, seq_len, d_model)
    K = np.random.randn(batch, seq_len, d_model)
    
    # Attention scores: S_bij = sum_k Q_bik * K_bjk
    scores = np.einsum('bik,bjk->bij', Q, K)
    
    print(f"Q shape:      {Q.shape}")
    print(f"K shape:      {K.shape}")
    print(f"Scores shape: {scores.shape}")

if __name__ == "__main__":
    main()
```

### 2. Bilinear Form

```python
import numpy as np

def main():
    # x^T A y
    x = np.array([1, 2, 3])
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    y = np.array([1, 1, 1])
    
    # Bilinear: sum_ij x_i * A_ij * y_j
    result = np.einsum('i,ij,j->', x, A, y)
    
    print(f"einsum:     {result}")
    print(f"x @ A @ y:  {x @ A @ y}")

if __name__ == "__main__":
    main()
```

### 3. Covariance Matrix

```python
import numpy as np

def main():
    # Data matrix: (samples, features)
    X = np.random.randn(100, 5)
    X_centered = X - X.mean(axis=0)
    
    # Covariance: C_ij = (1/n) sum_k X_ki * X_kj
    n = X.shape[0]
    cov_einsum = np.einsum('ki,kj->ij', X_centered, X_centered) / n
    
    print("einsum covariance:")
    print(cov_einsum)
    print()
    print("np.cov (transposed input):")
    print(np.cov(X.T, bias=True))

if __name__ == "__main__":
    main()
```

## Summary Table

### 1. Quick Reference

| Operation | einsum | Equivalent |
|:----------|:-------|:-----------|
| Transpose | `'ij->ji'` | `A.T` |
| Trace | `'ii->'` | `np.trace(A)` |
| Diagonal | `'ii->i'` | `np.diag(A)` |
| Dot product | `'i,i->'` | `np.dot(a, b)` |
| Outer product | `'i,j->ij'` | `np.outer(a, b)` |
| Matrix multiply | `'ij,jk->ik'` | `A @ B` |
| Batch matmul | `'bij,bjk->bik'` | `np.matmul(A, B)` |

### 2. When to Use einsum

- Complex tensor contractions
- Multiple simultaneous operations
- Non-standard axis combinations

### 3. When to Avoid

- Simple operations with native equivalents
- When readability is paramount

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
