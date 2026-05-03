# Matrix Multiplication

Sparse matrix-matrix multiplication and its considerations.

!!! tip "Mental Model"
    Sparse matrix multiplication skips all the zero-times-anything work, making it dramatically faster than dense multiplication when both matrices are sparse. However, the product of two sparse matrices can be much denser than either input -- each nonzero can contribute to multiple output entries. Always check the output sparsity to avoid unexpected memory blowup.

## Sparse @ Sparse

### 1. Basic Usage

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 0], [0, 2]])
    B = sparse.csr_matrix([[1, 2], [3, 4]])
    
    C = A @ B
    
    print("A @ B =")
    print(C.toarray())
    print(f"Result type: {type(C)}")

if __name__ == "__main__":
    main()
```

### 2. Using .dot()

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 2], [3, 4]])
    B = sparse.csr_matrix([[5, 6], [7, 8]])
    
    C = A.dot(B)
    
    print("A.dot(B) =")
    print(C.toarray())

if __name__ == "__main__":
    main()
```

## Fill-in

### 1. Sparsity Can Decrease

```python
from scipy import sparse

def main():
    n = 100
    A = sparse.random(n, n, density=0.1, format='csr')
    B = sparse.random(n, n, density=0.1, format='csr')
    
    C = A @ B
    
    print(f"A density: {A.nnz / n**2:.2%}")
    print(f"B density: {B.nnz / n**2:.2%}")
    print(f"C = A@B density: {C.nnz / n**2:.2%}")

if __name__ == "__main__":
    main()
```

### 2. Structured Sparsity

```python
from scipy import sparse

def main():
    # Banded matrices preserve structure better
    n = 100
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    
    C = A @ A
    
    print(f"A bandwidth: 1")
    print(f"A@A bandwidth: {max(abs(C.nonzero()[0] - C.nonzero()[1]))}")

if __name__ == "__main__":
    main()
```

## Sparse @ Dense

### 1. Matrix-Matrix

```python
import numpy as np
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 0], [0, 2]])
    B = np.array([[1, 2], [3, 4]])
    
    C = A @ B  # Result is dense
    
    print("Sparse @ Dense =")
    print(C)
    print(f"Result type: {type(C)}")

if __name__ == "__main__":
    main()
```

## Performance Tips

### 1. CSR for Row-based Multiply

```python
from scipy import sparse
import time

def main():
    n = 1000
    A_csr = sparse.random(n, n, density=0.01, format='csr')
    A_csc = A_csr.tocsc()
    B = sparse.random(n, n, density=0.01, format='csr')
    
    # CSR @ CSR
    start = time.perf_counter()
    C = A_csr @ B
    csr_time = time.perf_counter() - start
    
    # CSC @ CSR
    start = time.perf_counter()
    C = A_csc @ B
    csc_time = time.perf_counter() - start
    
    print(f"CSR @ CSR: {csr_time:.4f} sec")
    print(f"CSC @ CSR: {csc_time:.4f} sec")

if __name__ == "__main__":
    main()
```

## Summary

- `A @ B` returns sparse if both sparse
- Fill-in can increase density of result
- Use CSR format for efficient multiplication
- Result density depends on sparsity patterns

---

## Exercises

**Exercise 1.**
Create two $100 \times 100$ sparse random matrices $A$ and $B$ with density 0.05 each (use `np.random.seed(6)`). Compute their product $C = A \cdot B$ and print the density of $A$, $B$, and $C$. Observe the fill-in effect: $C$ should be denser than either input.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        np.random.seed(6)
        n = 100
        A = sparse.random(n, n, density=0.05, format='csr')
        B = sparse.random(n, n, density=0.05, format='csr')

        C = A @ B

        print(f"A density: {A.nnz / n**2:.4f}")
        print(f"B density: {B.nnz / n**2:.4f}")
        print(f"C density: {C.nnz / n**2:.4f}")

---

**Exercise 2.**
Build a $200 \times 200$ sparse tridiagonal matrix $A$ (2 on diagonal, -1 on off-diagonals). Compute $A^2 = A \cdot A$ and $A^3 = A^2 \cdot A$. Print the bandwidth (maximum $|i - j|$ for nonzero entries) of $A$, $A^2$, and $A^3$. Verify the bandwidth increases with each multiplication.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse

        n = 200
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')

        A2 = A @ A
        A3 = A2 @ A

        def bandwidth(M):
            rows, cols = M.nonzero()
            return max(abs(rows - cols)) if len(rows) > 0 else 0

        print(f"A  bandwidth: {bandwidth(A)}")
        print(f"A^2 bandwidth: {bandwidth(A2)}")
        print(f"A^3 bandwidth: {bandwidth(A3)}")

---

**Exercise 3.**
Multiply a $5000 \times 5000$ sparse CSR matrix (density 0.001, `np.random.seed(0)`) by a dense $5000 \times 10$ matrix. Measure the time for the sparse-dense product and compare with converting the sparse matrix to dense first and then multiplying. Print both times.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        import time

        np.random.seed(0)
        n = 5000
        A_sparse = sparse.random(n, n, density=0.001, format='csr')
        B_dense = np.random.randn(n, 10)

        # Sparse @ dense
        start = time.perf_counter()
        C1 = A_sparse @ B_dense
        t_sparse = time.perf_counter() - start

        # Dense @ dense
        A_dense = A_sparse.toarray()
        start = time.perf_counter()
        C2 = A_dense @ B_dense
        t_dense = time.perf_counter() - start

        print(f"Sparse @ dense: {t_sparse:.4f} sec")
        print(f"Dense @ dense:  {t_dense:.4f} sec")
        print(f"Results match: {np.allclose(C1, C2)}")
