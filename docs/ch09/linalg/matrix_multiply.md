# Matrix Multiplication

NumPy provides multiple ways to perform matrix multiplication.

!!! tip "Mental Model"
    The `@` operator is the standard way to do matrix multiplication in NumPy -- `A @ B` means "dot rows of A with columns of B." Remember that `*` is element-wise multiplication, not matrix multiplication. For 1D arrays, `@` computes the dot product; for higher dimensions, it broadcasts the matrix multiply over batch axes.

    Conceptually, matrix multiplication is **composition of linear transformations**:
    if $A$ maps space one way and $B$ maps it another, $A @ B$ applies $B$ first, then
    $A$. This geometric view is why matrix multiply is not commutative ($AB \neq BA$)
    and why the inner dimensions must match.

!!! note "Matrix Computation System"
    All linear algebra operations in this section fall into three categories:

    ```text
    Matrix A
        │
        ├── 1. Transformations
        │       A @ x  (matrix multiply)
        │
        ├── 2. Solvers
        │       Ax = b  (solve, lstsq, Cholesky-solve, QR-solve)
        │
        └── 3. Decompositions
                Factor A into simpler components:
                ├── LU       → general solve
                ├── QR       → least squares, eigenvalue algorithms
                ├── LLᵀ      → symmetric positive definite (Cholesky)
                ├── VΛV⁻¹    → eigen decomposition (square)
                └── UΣVᵀ     → most general (SVD)
    ```

    Each decomposition reveals different structure:

    - **Cholesky** → positive definiteness (fast SPD solve, sampling)
    - **QR** → orthogonality (stable least squares)
    - **Eigen** → intrinsic directions (PCA, stability, oscillation modes)
    - **SVD** → full geometry and rank (compression, pseudoinverse, ML)

    The decompositions form a hierarchy of generality:
    Cholesky $\subset$ QR $\subset$ SVD (each works on a broader class of matrices).

    **Which method to use?**

    | Problem | Method |
    |---------|--------|
    | Square system $Ax = b$ | `np.linalg.solve` (LU internally) |
    | Overdetermined system | `np.linalg.lstsq` or QR |
    | Symmetric positive definite | Cholesky (2x faster than LU) |
    | Need eigenstructure | `eig` / `eigh` |
    | Need robustness / rank analysis | SVD |
    | Any matrix, maximum generality | SVD |

## The @ Operator

### 1. Basic Usage

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    B = np.array([[5, 6],
                  [7, 8]])
    
    C = A @ B
    
    print("A @ B =")
    print(C)

if __name__ == "__main__":
    main()
```

**Output:**

```
A @ B =
[[19 22]
 [43 50]]
```

### 2. Mathematical Form

$$C_{ij} = \sum_k A_{ik} B_{kj}$$

### 3. Shape Requirements

Inner dimensions must match: `(m, n) @ (n, p) -> (m, p)`.

```python
import numpy as np

def main():
    A = np.random.randn(3, 4)
    B = np.random.randn(4, 5)
    
    C = A @ B
    
    print(f"A shape: {A.shape}")
    print(f"B shape: {B.shape}")
    print(f"C shape: {C.shape}")

if __name__ == "__main__":
    main()
```

## np.matmul

### 1. Equivalent to @

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    B = np.array([[5, 6],
                  [7, 8]])
    
    C1 = A @ B
    C2 = np.matmul(A, B)
    
    print(f"Results equal: {np.array_equal(C1, C2)}")

if __name__ == "__main__":
    main()
```

### 2. Batch Multiplication

Both `@` and `np.matmul` support batch dimensions.

```python
import numpy as np

def main():
    # Batch of 10 matrices
    A = np.random.randn(10, 3, 4)
    B = np.random.randn(10, 4, 5)
    
    C = A @ B  # or np.matmul(A, B)
    
    print(f"A shape: {A.shape}")
    print(f"B shape: {B.shape}")
    print(f"C shape: {C.shape}")

if __name__ == "__main__":
    main()
```

### 3. Broadcasting

```python
import numpy as np

def main():
    # Single matrix times batch
    A = np.random.randn(3, 4)
    B = np.random.randn(10, 4, 5)
    
    C = A @ B
    
    print(f"A shape: {A.shape}")
    print(f"B shape: {B.shape}")
    print(f"C shape: {C.shape}")

if __name__ == "__main__":
    main()
```

## np.dot

### 1. Vector Dot Product

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    dot = np.dot(a, b)
    
    print(f"a · b = {dot}")
    print(f"Manual: {1*4 + 2*5 + 3*6}")

if __name__ == "__main__":
    main()
```

### 2. Matrix Multiplication

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    B = np.array([[5, 6],
                  [7, 8]])
    
    C = np.dot(A, B)
    
    print("np.dot(A, B) =")
    print(C)

if __name__ == "__main__":
    main()
```

### 3. Difference from @

`np.dot` and `@` differ for higher-dimensional arrays.

```python
import numpy as np

def main():
    A = np.random.randn(2, 3, 4)
    B = np.random.randn(2, 4, 5)
    
    # @ treats as batch matmul
    C_matmul = A @ B
    print(f"A @ B shape: {C_matmul.shape}")
    
    # np.dot sums over last axis of A and second-to-last of B
    # Result shape differs!

if __name__ == "__main__":
    main()
```

## Matrix-Vector Product

### 1. Ax = b Style

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6]])
    x = np.array([1, 2, 3])
    
    b = A @ x
    
    print(f"A shape: {A.shape}")
    print(f"x shape: {x.shape}")
    print(f"b shape: {b.shape}")
    print(f"b = {b}")

if __name__ == "__main__":
    main()
```

### 2. Row Vector

```python
import numpy as np

def main():
    x = np.array([1, 2])
    A = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    b = x @ A
    
    print(f"x shape: {x.shape}")
    print(f"A shape: {A.shape}")
    print(f"b shape: {b.shape}")
    print(f"b = {b}")

if __name__ == "__main__":
    main()
```

### 3. Explicit Shapes

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    x = np.array([[1],
                  [2]])  # Column vector
    
    b = A @ x
    
    print(f"A shape: {A.shape}")
    print(f"x shape: {x.shape}")
    print(f"b shape: {b.shape}")
    print("b =")
    print(b)

if __name__ == "__main__":
    main()
```

## Performance

### 1. BLAS Backend

NumPy uses optimized BLAS libraries (OpenBLAS, MKL).

```python
import numpy as np

def main():
    print(np.show_config())

if __name__ == "__main__":
    main()
```

### 2. Large Matrix Timing

```python
import numpy as np
import time

def main():
    n = 1000
    A = np.random.randn(n, n)
    B = np.random.randn(n, n)
    
    start = time.perf_counter()
    C = A @ B
    elapsed = time.perf_counter() - start
    
    print(f"Matrix size: {n}x{n}")
    print(f"Time: {elapsed:.4f} sec")
    print(f"GFLOPS: {2*n**3/elapsed/1e9:.1f}")

if __name__ == "__main__":
    main()
```

### 3. Contiguous Memory

Ensure arrays are contiguous for best performance.

```python
import numpy as np
import time

def main():
    n = 1000
    A = np.random.randn(n, n)
    
    # Contiguous
    B = np.ascontiguousarray(A.T)
    
    start = time.perf_counter()
    C = B @ B
    t1 = time.perf_counter() - start
    
    # Non-contiguous (transposed view)
    start = time.perf_counter()
    C = A.T @ A.T
    t2 = time.perf_counter() - start
    
    print(f"Contiguous:     {t1:.4f} sec")
    print(f"Non-contiguous: {t2:.4f} sec")

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Use @ Operator

Prefer `@` for readability; it's equivalent to `np.matmul`.

### 2. Check Shapes

Verify shapes before multiplication to avoid broadcasting surprises.

### 3. Batch Operations

Use batch matmul instead of loops for multiple matrix multiplications.

---

## Exercises

**Exercise 1.**
Create two matrices `A` of shape `(3, 4)` and `B` of shape `(4, 2)`. Compute their product using both `A @ B` and `np.matmul(A, B)`. Verify both produce the same result and the output shape is `(3, 2)`.

??? success "Solution to Exercise 1"

        import numpy as np

        A = np.random.randn(3, 4)
        B = np.random.randn(4, 2)
        result1 = A @ B
        result2 = np.matmul(A, B)
        print(f"Shape: {result1.shape}")  # (3, 2)
        print(f"Match: {np.allclose(result1, result2)}")

---

**Exercise 2.**
Demonstrate the difference between element-wise multiplication (`A * B`) and matrix multiplication (`A @ B`) for two 3x3 matrices. Show that the results are different and explain when each is appropriate.

??? success "Solution to Exercise 2"

        import numpy as np

        A = np.array([[1, 2], [3, 4]])
        B = np.array([[5, 6], [7, 8]])
        print(f"Element-wise A * B:\n{A * B}")
        print(f"Matrix A @ B:\n{A @ B}")
        # Element-wise: each (i,j) = A[i,j] * B[i,j]
        # Matrix: row-column dot products

---

**Exercise 3.**
Compute the matrix-vector product `A @ v` where `A = np.array([[1, 2, 3], [4, 5, 6]])` and `v = np.array([1, 0, -1])`. Then compute the same result using `np.dot` and `np.einsum('ij,j->i', A, v)`. Verify all three produce the same output.

??? success "Solution to Exercise 3"

        import numpy as np

        A = np.array([[1, 2, 3], [4, 5, 6]])
        v = np.array([1, 0, -1])

        r1 = A @ v
        r2 = np.dot(A, v)
        r3 = np.einsum('ij,j->i', A, v)

        print(f"A @ v:    {r1}")
        print(f"np.dot:   {r2}")
        print(f"einsum:   {r3}")
        print(f"All match: {np.allclose(r1, r2) and np.allclose(r1, r3)}")
