# Storage Formats

SciPy provides multiple sparse matrix formats optimized for different operations.

!!! tip "Mental Model"
    A sparse format answers: "How do I store only the nonzero entries and still know where they belong?" Each format encodes position differently -- CSR groups by row, CSC by column, COO stores explicit (row, col, value) triplets. The storage scheme determines which operations are fast and which are slow, so understanding the internal arrays is key to predicting performance.

## CSR (Compressed Sparse Row)

### 1. Structure

```python
import numpy as np
from scipy import sparse

def main():
    A = np.array([[1, 0, 2],
                  [0, 0, 3],
                  [4, 5, 6]])
    
    csr = sparse.csr_matrix(A)
    
    print("Dense matrix:")
    print(A)
    print()
    print("CSR representation:")
    print(f"data:    {csr.data}")      # Nonzero values
    print(f"indices: {csr.indices}")   # Column indices
    print(f"indptr:  {csr.indptr}")    # Row pointers

if __name__ == "__main__":
    main()
```

### 2. Best For

- Fast row slicing
- Fast matrix-vector products
- Efficient arithmetic operations

### 3. Row Access

```python
import numpy as np
from scipy import sparse

def main():
    A = sparse.random(1000, 1000, density=0.01, format='csr')
    
    # Fast row slicing
    row_5 = A[5, :]
    rows_10_20 = A[10:20, :]
    
    print(f"Row 5 nonzeros: {row_5.nnz}")
    print(f"Rows 10-20 shape: {rows_10_20.shape}")

if __name__ == "__main__":
    main()
```

## CSC (Compressed Sparse Column)

### 1. Structure

```python
import numpy as np
from scipy import sparse

def main():
    A = np.array([[1, 0, 2],
                  [0, 0, 3],
                  [4, 5, 6]])
    
    csc = sparse.csc_matrix(A)
    
    print("CSC representation:")
    print(f"data:    {csc.data}")      # Nonzero values
    print(f"indices: {csc.indices}")   # Row indices
    print(f"indptr:  {csc.indptr}")    # Column pointers

if __name__ == "__main__":
    main()
```

### 2. Best For

- Fast column slicing
- Efficient column operations
- Some sparse solvers

### 3. Column Access

```python
import numpy as np
from scipy import sparse

def main():
    A = sparse.random(1000, 1000, density=0.01, format='csc')
    
    # Fast column slicing
    col_5 = A[:, 5]
    cols_10_20 = A[:, 10:20]
    
    print(f"Column 5 nonzeros: {col_5.nnz}")
    print(f"Columns 10-20 shape: {cols_10_20.shape}")

if __name__ == "__main__":
    main()
```

## COO (Coordinate)

### 1. Structure

```python
import numpy as np
from scipy import sparse

def main():
    A = np.array([[1, 0, 2],
                  [0, 0, 3],
                  [4, 5, 6]])
    
    coo = sparse.coo_matrix(A)
    
    print("COO representation:")
    print(f"data: {coo.data}")
    print(f"row:  {coo.row}")
    print(f"col:  {coo.col}")

if __name__ == "__main__":
    main()
```

### 2. Best For

- Fast construction
- Converting between formats
- Adding entries incrementally

### 3. Building Matrices

```python
import numpy as np
from scipy import sparse

def main():
    # Build from triplets
    row = np.array([0, 0, 1, 2, 2, 2])
    col = np.array([0, 2, 2, 0, 1, 2])
    data = np.array([1, 2, 3, 4, 5, 6])
    
    coo = sparse.coo_matrix((data, (row, col)), shape=(3, 3))
    
    print("Built from triplets:")
    print(coo.toarray())

if __name__ == "__main__":
    main()
```

## LIL (List of Lists)

### 1. Structure

```python
import numpy as np
from scipy import sparse

def main():
    lil = sparse.lil_matrix((3, 3))
    lil[0, 0] = 1
    lil[0, 2] = 2
    lil[1, 2] = 3
    lil[2, :] = [4, 5, 6]
    
    print("LIL matrix:")
    print(lil.toarray())
    print()
    print("Internal rows:", lil.rows)
    print("Internal data:", lil.data)

if __name__ == "__main__":
    main()
```

### 2. Best For

- Incremental construction
- Modifying sparsity pattern
- Building row by row

## DIA (Diagonal)

### 1. Structure

```python
import numpy as np
from scipy import sparse

def main():
    # Tridiagonal matrix
    diags = [[-1, -1, -1, -1],
             [2, 2, 2, 2, 2],
             [-1, -1, -1, -1]]
    offsets = [-1, 0, 1]
    
    dia = sparse.diags(diags, offsets, shape=(5, 5), format='dia')
    
    print("Diagonal matrix:")
    print(dia.toarray())

if __name__ == "__main__":
    main()
```

### 2. Best For

- Banded matrices
- PDE discretizations
- Memory-efficient for diagonals

## Format Comparison

### 1. Summary Table

| Format | Construction | Arithmetic | Row Slice | Col Slice |
|:-------|:-------------|:-----------|:----------|:----------|
| CSR | Slow | Fast | Fast | Slow |
| CSC | Slow | Fast | Slow | Fast |
| COO | Fast | Slow | Slow | Slow |
| LIL | Fast | Slow | Fast | Slow |
| DIA | Fast | Fast | Slow | Slow |

### 2. Typical Workflow

```python
import numpy as np
from scipy import sparse

def main():
    n = 1000
    
    # 1. Build with LIL or COO
    lil = sparse.lil_matrix((n, n))
    for i in range(n):
        lil[i, i] = 2
        if i > 0:
            lil[i, i-1] = -1
        if i < n-1:
            lil[i, i+1] = -1
    
    # 2. Convert to CSR for computation
    csr = lil.tocsr()
    
    # 3. Use for matrix operations
    x = np.ones(n)
    y = csr @ x
    
    print(f"Built {n}x{n} matrix")
    print(f"Nonzeros: {csr.nnz}")

if __name__ == "__main__":
    main()
```

## Summary

| Format | Use Case |
|:-------|:---------|
| CSR | General computation, row operations |
| CSC | Column operations, some solvers |
| COO | Building matrices, format conversion |
| LIL | Incremental construction |
| DIA | Banded/diagonal matrices |

---

## Exercises

**Exercise 1.**
Create the same $4 \times 4$ matrix $A = \begin{pmatrix} 1 & 0 & 2 & 0 \\ 0 & 3 & 0 & 0 \\ 0 & 0 & 4 & 5 \\ 6 & 0 & 0 & 7 \end{pmatrix}$ in CSR, CSC, and COO formats. For each format, print the internal storage arrays (e.g., `data`, `indices`, `indptr` for CSR; `data`, `row`, `col` for COO). Verify all three produce the same dense array.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        A = np.array([[1, 0, 2, 0],
                       [0, 3, 0, 0],
                       [0, 0, 4, 5],
                       [6, 0, 0, 7]])

        csr = sparse.csr_matrix(A)
        csc = sparse.csc_matrix(A)
        coo = sparse.coo_matrix(A)

        print("CSR: data={}, indices={}, indptr={}".format(
            csr.data, csr.indices, csr.indptr))
        print("CSC: data={}, indices={}, indptr={}".format(
            csc.data, csc.indices, csc.indptr))
        print("COO: data={}, row={}, col={}".format(
            coo.data, coo.row, coo.col))

        assert np.allclose(csr.toarray(), csc.toarray())
        assert np.allclose(csr.toarray(), coo.toarray())
        print("All formats match.")

---

**Exercise 2.**
Build a $6 \times 6$ sparse matrix using LIL format where entry $(i, j)$ equals $10i + j$ for positions on the main diagonal and the two adjacent diagonals. Convert to CSR and DIA formats. Compare the number of stored elements in each format.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse

        n = 6
        lil = sparse.lil_matrix((n, n))
        for i in range(n):
            for j in range(max(0, i - 1), min(n, i + 2)):
                lil[i, j] = 10 * i + j

        csr = lil.tocsr()
        dia = lil.todia()

        print("Matrix:")
        print(csr.toarray())
        print(f"CSR stored elements: {csr.nnz}")
        print(f"DIA stored elements: {dia.data.size}")

---

**Exercise 3.**
Create a $1000 \times 1000$ sparse random matrix with density 0.01 (use `np.random.seed(11)`). Convert it to all five formats (CSR, CSC, COO, LIL, DIA). For each format, measure the memory used by the internal arrays and print a comparison table. Which format uses the least memory for this matrix?

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse

        np.random.seed(11)
        A = sparse.random(1000, 1000, density=0.01, format='coo')

        formats = {
            'CSR': A.tocsr(),
            'CSC': A.tocsc(),
            'COO': A,
            'LIL': A.tolil(),
        }

        print(f"{'Format':<6} {'Memory (KB)':>12}")
        print("-" * 20)
        for name, mat in formats.items():
            if name == 'CSR' or name == 'CSC':
                mem = mat.data.nbytes + mat.indices.nbytes + mat.indptr.nbytes
            elif name == 'COO':
                mem = mat.data.nbytes + mat.row.nbytes + mat.col.nbytes
            elif name == 'LIL':
                mem = sum(sum(len(r) for r in mat.rows) * 8,
                          sum(len(d) for d in mat.data) * 8)
            print(f"{name:<6} {mem / 1024:>12.1f}")
