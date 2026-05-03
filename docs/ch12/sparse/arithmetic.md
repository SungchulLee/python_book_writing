# Arithmetic Operations

Sparse matrices support efficient arithmetic operations.

!!! tip "Mental Model"
    Sparse arithmetic only touches nonzero entries, so adding two sparse matrices with $k$ nonzeros each costs $O(k)$ rather than $O(n^2)$. However, beware of operations that destroy sparsity -- adding a scalar to a sparse matrix fills in every entry, turning your efficient sparse matrix into a dense one in disguise.

## Addition and Subtraction

### 1. Sparse + Sparse

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 0], [0, 2]])
    B = sparse.csr_matrix([[0, 3], [4, 0]])
    
    C = A + B
    
    print("A + B =")
    print(C.toarray())

if __name__ == "__main__":
    main()
```

### 2. Sparse + Scalar

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 0], [0, 2]])
    
    # Note: adds to ALL entries (converts to dense pattern)
    B = A + 1
    
    print("A + 1 =")
    print(B.toarray())

if __name__ == "__main__":
    main()
```

## Scalar Multiplication

### 1. Scale Matrix

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 0, 2], [0, 3, 0]])
    
    B = 2 * A
    C = A * 0.5
    
    print("2 * A =")
    print(B.toarray())

if __name__ == "__main__":
    main()
```

## Matrix-Vector Product

### 1. Sparse @ Dense

```python
import numpy as np
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 0, 2],
                           [0, 3, 0],
                           [4, 0, 5]])
    x = np.array([1, 2, 3])
    
    y = A @ x
    
    print(f"A @ x = {y}")

if __name__ == "__main__":
    main()
```

### 2. Performance

```python
import numpy as np
from scipy import sparse
import time

def main():
    n = 10000
    A = sparse.random(n, n, density=0.001, format='csr')
    x = np.random.randn(n)
    
    start = time.perf_counter()
    for _ in range(100):
        y = A @ x
    elapsed = time.perf_counter() - start
    
    print(f"100 sparse matvecs: {elapsed:.4f} sec")

if __name__ == "__main__":
    main()
```

## Element-wise Operations

### 1. Hadamard Product

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 2], [3, 4]])
    B = sparse.csr_matrix([[1, 0], [0, 1]])
    
    # Element-wise multiplication
    C = A.multiply(B)
    
    print("A ⊙ B =")
    print(C.toarray())

if __name__ == "__main__":
    main()
```

### 2. Power

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 2], [3, 4]])
    
    # Element-wise power
    B = A.power(2)
    
    print("A.^2 =")
    print(B.toarray())

if __name__ == "__main__":
    main()
```

## Summary

| Operation | Method | Preserves Sparsity |
|:----------|:-------|:-------------------|
| A + B | `A + B` | Yes |
| A + scalar | `A + c` | No (fills matrix) |
| c * A | `c * A` | Yes |
| A @ x | `A @ x` | N/A (returns dense) |
| A ⊙ B | `A.multiply(B)` | Yes |

---

## Exercises

**Exercise 1.**
Create two sparse CSR matrices: $A = \begin{pmatrix} 1 & 0 & 2 \\ 0 & 3 & 0 \end{pmatrix}$ and $B = \begin{pmatrix} 0 & 4 & 0 \\ 5 & 0 & 6 \end{pmatrix}$. Compute $C = 3A + 2B$ and verify the result by converting to dense. Check that $C$ is still sparse and print its number of nonzeros.

??? success "Solution to Exercise 1"
        from scipy import sparse

        A = sparse.csr_matrix([[1, 0, 2], [0, 3, 0]])
        B = sparse.csr_matrix([[0, 4, 0], [5, 0, 6]])

        C = 3 * A + 2 * B
        print("C = 3A + 2B:")
        print(C.toarray())
        print(f"C is sparse: {sparse.issparse(C)}")
        print(f"Nonzeros: {C.nnz}")

---

**Exercise 2.**
Create a $1000 \times 1000$ sparse random matrix with density 0.005 in CSR format (use `np.random.seed(2)`). Compute the matrix-vector product $y = Ax$ where $x$ is a vector of ones. Print the first 5 entries of $y$ and verify they match the row sums of $A$.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse

        np.random.seed(2)
        A = sparse.random(1000, 1000, density=0.005, format='csr')
        x = np.ones(1000)

        y = A @ x
        row_sums = np.array(A.sum(axis=1)).flatten()

        print(f"First 5 entries of A @ ones: {y[:5]}")
        print(f"First 5 row sums:            {row_sums[:5]}")
        print(f"Match: {np.allclose(y, row_sums)}")

---

**Exercise 3.**
Given $A = \text{sparse.csr\_matrix}([[1, 2, 3], [4, 5, 6]])$ and $B = \text{sparse.csr\_matrix}([[1, 0, 1], [0, 1, 0]])$, compute the element-wise (Hadamard) product using `.multiply()`, the element-wise square using `.power(2)`, and print both results as dense arrays. Verify that the Hadamard product preserves the sparsity pattern of $B$.

??? success "Solution to Exercise 3"
        from scipy import sparse

        A = sparse.csr_matrix([[1, 2, 3], [4, 5, 6]])
        B = sparse.csr_matrix([[1, 0, 1], [0, 1, 0]])

        hadamard = A.multiply(B)
        squared = A.power(2)

        print("Hadamard product A*B:")
        print(hadamard.toarray())
        print(f"Hadamard nnz: {hadamard.nnz}, B nnz: {B.nnz}")

        print("\nElement-wise square A.^2:")
        print(squared.toarray())
