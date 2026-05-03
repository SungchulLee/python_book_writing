# Creating Sparse Matrices

Methods for constructing sparse matrices in SciPy.

!!! tip "Mental Model"
    There are two main paths to building a sparse matrix: convert from dense (convenient but defeats the purpose for large matrices) or construct directly from coordinate data (row indices, column indices, values). For incremental construction, use LIL or DOK format; for batch construction from known coordinates, use COO format -- then convert to CSR/CSC for computation.

## From Dense Array

### 1. Direct Conversion

```python
import numpy as np
from scipy import sparse

def main():
    A = np.array([[1, 0, 2],
                  [0, 0, 3],
                  [4, 5, 6]])
    
    csr = sparse.csr_matrix(A)
    csc = sparse.csc_matrix(A)
    coo = sparse.coo_matrix(A)
    
    print(f"CSR: {csr.nnz} nonzeros")
    print(f"CSC: {csc.nnz} nonzeros")
    print(f"COO: {coo.nnz} nonzeros")

if __name__ == "__main__":
    main()
```

## From Triplets

### 1. COO Format

```python
import numpy as np
from scipy import sparse

def main():
    row = np.array([0, 0, 1, 2, 2])
    col = np.array([0, 2, 2, 0, 1])
    data = np.array([1, 2, 3, 4, 5])
    
    A = sparse.coo_matrix((data, (row, col)), shape=(3, 3))
    
    print(A.toarray())

if __name__ == "__main__":
    main()
```

## Diagonal Matrices

### 1. sparse.diags

```python
import numpy as np
from scipy import sparse

def main():
    # Tridiagonal
    n = 5
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n))
    
    print(A.toarray())

if __name__ == "__main__":
    main()
```

### 2. Multiple Diagonals

```python
import numpy as np
from scipy import sparse

def main():
    diagonals = [np.ones(4), 2*np.ones(5), np.ones(4)]
    A = sparse.diags(diagonals, [-1, 0, 1])
    
    print(A.toarray())

if __name__ == "__main__":
    main()
```

## Special Matrices

### 1. Identity

```python
from scipy import sparse

def main():
    I = sparse.eye(5)
    print(I.toarray())

if __name__ == "__main__":
    main()
```

### 2. Random Sparse

```python
from scipy import sparse

def main():
    A = sparse.random(5, 5, density=0.3, format='csr')
    print(f"Density: {A.nnz / 25:.2f}")
    print(A.toarray().round(2))

if __name__ == "__main__":
    main()
```

## Incremental Building

### 1. LIL Matrix

```python
from scipy import sparse

def main():
    lil = sparse.lil_matrix((5, 5))
    
    # Add entries one by one
    lil[0, 0] = 1
    lil[1, 1] = 2
    lil[2, 2] = 3
    lil[0, 4] = 4
    
    # Convert for computation
    csr = lil.tocsr()
    print(csr.toarray())

if __name__ == "__main__":
    main()
```

## Summary

| Method | Use Case |
|:-------|:---------|
| `csr_matrix(A)` | From dense array |
| `coo_matrix((data, (row, col)))` | From triplets |
| `diags(d, offsets)` | Diagonal/banded |
| `eye(n)` | Identity matrix |
| `random(m, n, density)` | Random sparse |
| `lil_matrix((m, n))` | Incremental build |

---

## Exercises

**Exercise 1.**
Create a $7 \times 7$ pentadiagonal matrix using `sparse.diags` with values: -1 on offsets -2 and +2, 4 on offsets -1 and +1, and 10 on the main diagonal. Print the dense representation and verify the number of nonzeros.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        n = 7
        A = sparse.diags([-1, 4, 10, 4, -1], [-2, -1, 0, 1, 2],
                          shape=(n, n))

        print("Pentadiagonal matrix:")
        print(A.toarray())
        print(f"Nonzeros: {A.nnz}")

---

**Exercise 2.**
Build a $100 \times 100$ sparse matrix using COO triplet format where entry $(i, j) = i + j$ for all pairs where $|i - j| \leq 1$ (i.e., a tridiagonal pattern). Convert to CSR and print the shape, number of nonzeros, and the first 5 rows as a dense array.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse

        n = 100
        rows, cols, data = [], [], []
        for i in range(n):
            for j in range(max(0, i - 1), min(n, i + 2)):
                rows.append(i)
                cols.append(j)
                data.append(i + j)

        A = sparse.coo_matrix((data, (rows, cols)), shape=(n, n)).tocsr()
        print(f"Shape: {A.shape}")
        print(f"Nonzeros: {A.nnz}")
        print(f"First 5 rows:\n{A[:5].toarray()}")

---

**Exercise 3.**
Use `sparse.lil_matrix` to incrementally construct a $50 \times 50$ lower triangular matrix where entry $(i, j) = 1/(i - j + 1)$ for $j \leq i$. Convert to CSR, print the number of nonzeros, and verify the result by checking that all entries above the diagonal are zero.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse

        n = 50
        lil = sparse.lil_matrix((n, n))
        for i in range(n):
            for j in range(i + 1):
                lil[i, j] = 1.0 / (i - j + 1)

        csr = lil.tocsr()
        print(f"Nonzeros: {csr.nnz}")

        dense = csr.toarray()
        upper_sum = np.sum(np.abs(np.triu(dense, k=1)))
        print(f"Sum of upper triangle: {upper_sum}")
        assert upper_sum == 0, "Should be lower triangular"
