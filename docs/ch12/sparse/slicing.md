# Slicing and Indexing

Accessing elements and submatrices in sparse matrices.

!!! tip "Mental Model"
    Slicing a sparse matrix is format-dependent: CSR makes row slicing fast because rows are stored contiguously, while CSC makes column slicing fast for the same reason. Single-element access is slow in any format because it requires a search through compressed indices. If you need to read many individual elements, convert to dense first or restructure your algorithm to use row/column slices.

## Element Access

### 1. Single Element

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 0, 2],
                           [0, 3, 0],
                           [4, 0, 5]])
    
    print(f"A[0, 0] = {A[0, 0]}")
    print(f"A[0, 2] = {A[0, 2]}")
    print(f"A[1, 0] = {A[1, 0]}")  # Zero element

if __name__ == "__main__":
    main()
```

## Row and Column Slicing

### 1. Row Slicing (CSR efficient)

```python
from scipy import sparse

def main():
    A = sparse.csr_matrix([[1, 0, 2],
                           [0, 3, 0],
                           [4, 0, 5]])
    
    row_0 = A[0, :]
    rows_0_1 = A[0:2, :]
    
    print("Row 0:")
    print(row_0.toarray())
    print()
    print("Rows 0-1:")
    print(rows_0_1.toarray())

if __name__ == "__main__":
    main()
```

### 2. Column Slicing (CSC efficient)

```python
from scipy import sparse

def main():
    A = sparse.csc_matrix([[1, 0, 2],
                           [0, 3, 0],
                           [4, 0, 5]])
    
    col_0 = A[:, 0]
    cols_0_1 = A[:, 0:2]
    
    print("Column 0:")
    print(col_0.toarray())

if __name__ == "__main__":
    main()
```

## Fancy Indexing

### 1. Row Selection

```python
from scipy import sparse
import numpy as np

def main():
    A = sparse.csr_matrix([[1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 9],
                           [10, 11, 12]])
    
    rows = [0, 2, 3]
    B = A[rows, :]
    
    print("Selected rows [0, 2, 3]:")
    print(B.toarray())

if __name__ == "__main__":
    main()
```

### 2. Boolean Indexing

```python
from scipy import sparse
import numpy as np

def main():
    A = sparse.csr_matrix([[1, 2], [3, 4], [5, 6]])
    
    mask = np.array([True, False, True])
    B = A[mask, :]
    
    print("Boolean selected rows:")
    print(B.toarray())

if __name__ == "__main__":
    main()
```

## Modifying Elements

### 1. Set Single Element

```python
from scipy import sparse

def main():
    A = sparse.lil_matrix((3, 3))
    
    A[0, 0] = 1
    A[1, 1] = 2
    A[2, 2] = 3
    
    print(A.toarray())

if __name__ == "__main__":
    main()
```

### 2. LIL for Modification

```python
from scipy import sparse

def main():
    # CSR is inefficient for element-by-element modification
    # Use LIL, then convert
    
    lil = sparse.lil_matrix((5, 5))
    for i in range(5):
        lil[i, i] = i + 1
    
    csr = lil.tocsr()
    print(csr.toarray())

if __name__ == "__main__":
    main()
```

## Performance

### 1. Format Matters

| Operation | CSR | CSC | COO |
|:----------|:----|:----|:----|
| Row slice | Fast | Slow | Slow |
| Col slice | Slow | Fast | Slow |
| Element access | Medium | Medium | Slow |
| Modification | Slow | Slow | Fast |

## Summary

- Use CSR for row operations
- Use CSC for column operations  
- Use LIL for building/modifying
- Avoid element-by-element access on CSR/CSC

---

## Exercises

**Exercise 1.**
Create a $10 \times 10$ sparse CSR matrix from the dense matrix where entry $(i, j) = i \cdot 10 + j$ if $|i - j| \leq 1$, and 0 otherwise. Extract rows 3 through 6 using slicing and print the result as a dense array. Also extract the single element at position $(5, 4)$.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        n = 10
        dense = np.zeros((n, n))
        for i in range(n):
            for j in range(max(0, i - 1), min(n, i + 2)):
                dense[i, j] = i * 10 + j

        A = sparse.csr_matrix(dense)

        rows_3_6 = A[3:7, :]
        print("Rows 3-6:")
        print(rows_3_6.toarray())

        element = A[5, 4]
        print(f"\nA[5, 4] = {element}")

---

**Exercise 2.**
Build a $100 \times 100$ sparse random matrix in CSR format (density 0.1, `np.random.seed(7)`). Use fancy indexing to select rows `[0, 10, 20, 50, 99]` and print the resulting submatrix shape and number of nonzeros. Then use boolean indexing to select all rows whose row sum exceeds 5.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse

        np.random.seed(7)
        A = sparse.random(100, 100, density=0.1, format='csr')

        # Fancy indexing
        selected_rows = A[[0, 10, 20, 50, 99], :]
        print(f"Selected rows shape: {selected_rows.shape}")
        print(f"Selected rows nnz: {selected_rows.nnz}")

        # Boolean indexing
        row_sums = np.array(A.sum(axis=1)).flatten()
        mask = row_sums > 5
        filtered = A[mask, :]
        print(f"\nRows with sum > 5: {mask.sum()}")
        print(f"Filtered shape: {filtered.shape}")

---

**Exercise 3.**
Create a $50 \times 50$ sparse matrix using LIL format. Set the diagonal entries to their row index (0 through 49), then set entries $(i, i+5)$ to -1 for valid indices. Convert to CSR, extract column 10 using CSC format (convert first), and print the nonzero entries of that column.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse

        n = 50
        lil = sparse.lil_matrix((n, n))
        for i in range(n):
            lil[i, i] = i
            if i + 5 < n:
                lil[i, i + 5] = -1

        csr = lil.tocsr()
        csc = csr.tocsc()

        col_10 = csc[:, 10]
        nz_rows = col_10.nonzero()[0]
        print("Column 10 nonzero entries:")
        for r in nz_rows:
            print(f"  Row {r}: {col_10[r, 0]}")
