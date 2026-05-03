# Format Selection Guide

Choose the right sparse format for your use case.

!!! tip "Mental Model"
    Choosing a sparse format is like choosing the right data structure: COO and LIL are for building, CSR is for row-wise operations and matrix-vector products, CSC is for column-wise access and direct solvers, and DIA is for banded matrices. Pick the format that matches your dominant operation, and convert only once.

## Decision Tree

### 1. Building a Matrix?
- Use **LIL** or **COO** for construction
- Convert to CSR/CSC before computation

### 2. Row Operations?
- Use **CSR** for row slicing and matvec

### 3. Column Operations?
- Use **CSC** for column slicing

### 4. Banded Matrix?
- Use **DIA** for diagonal/banded structures

### 5. Solving Linear Systems?
- Use **CSC** for direct solvers
- Use **CSR** for iterative solvers

## Quick Reference

| Task | Recommended Format |
|:-----|:-------------------|
| Build incrementally | LIL, COO |
| Matrix-vector product | CSR |
| Row slicing | CSR |
| Column slicing | CSC |
| Direct solve (splu) | CSC |
| Iterative solve (cg) | CSR |
| Banded matrices | DIA |
| Format conversion | COO |

## Workflow

```python
from scipy import sparse

def main():
    # 1. Build with LIL
    lil = sparse.lil_matrix((1000, 1000))
    # ... add entries ...
    
    # 2. Convert to CSR for computation
    csr = lil.tocsr()
    
    # 3. Use CSR for all operations
    # ... matrix operations ...

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
You have a banded matrix with 5 diagonals. Create it using `sparse.diags` in DIA format, then convert it to CSR for matrix-vector products and to CSC for a direct solve. Print the format type at each stage and verify the dense representations are identical.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        n = 50
        dia = sparse.diags([1, -2, 6, -2, 1], [-2, -1, 0, 1, 2],
                            shape=(n, n), format='dia')
        print(f"DIA format: {type(dia)}")

        csr = dia.tocsr()
        print(f"CSR format: {type(csr)}")

        csc = dia.tocsc()
        print(f"CSC format: {type(csc)}")

        assert np.allclose(dia.toarray(), csr.toarray())
        assert np.allclose(dia.toarray(), csc.toarray())
        print("All formats produce identical dense arrays.")

---

**Exercise 2.**
Build a $200 \times 200$ sparse matrix incrementally: for each row $i$, set $A[i, i] = 10$ and $A[i, j] = -1$ for $j$ in a random subset of 3 other columns (use `np.random.seed(5)`). Use LIL format for construction, then convert to CSR. Print the total nonzeros and verify the matrix is diagonally dominant.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse

        np.random.seed(5)
        n = 200
        lil = sparse.lil_matrix((n, n))
        for i in range(n):
            lil[i, i] = 10
            others = np.random.choice([j for j in range(n) if j != i],
                                       size=3, replace=False)
            for j in others:
                lil[i, j] = -1

        csr = lil.tocsr()
        print(f"Nonzeros: {csr.nnz}")

        # Check diagonal dominance
        dense = csr.toarray()
        diag_dominant = True
        for i in range(n):
            if abs(dense[i, i]) <= np.sum(np.abs(dense[i, :])) - abs(dense[i, i]):
                diag_dominant = False
                break
        print(f"Diagonally dominant: {diag_dominant}")

---

**Exercise 3.**
Create a $1000 \times 1000$ sparse matrix in COO format from random triplets (use `np.random.seed(0)`, 5000 entries). Convert to CSR and CSC. Measure the time for 100 row slices `A[i, :]` using CSR versus CSC, and 100 column slices `A[:, j]` using CSR versus CSC. Print the times to demonstrate which format is faster for each operation.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        import time

        np.random.seed(0)
        n = 1000
        rows = np.random.randint(0, n, 5000)
        cols = np.random.randint(0, n, 5000)
        data = np.random.randn(5000)
        coo = sparse.coo_matrix((data, (rows, cols)), shape=(n, n))

        csr = coo.tocsr()
        csc = coo.tocsc()

        # Row slicing
        start = time.perf_counter()
        for i in range(100):
            _ = csr[i, :]
        t_row_csr = time.perf_counter() - start

        start = time.perf_counter()
        for i in range(100):
            _ = csc[i, :]
        t_row_csc = time.perf_counter() - start

        # Column slicing
        start = time.perf_counter()
        for j in range(100):
            _ = csr[:, j]
        t_col_csr = time.perf_counter() - start

        start = time.perf_counter()
        for j in range(100):
            _ = csc[:, j]
        t_col_csc = time.perf_counter() - start

        print(f"Row slice:  CSR={t_row_csr:.4f}s, CSC={t_row_csc:.4f}s")
        print(f"Col slice:  CSR={t_col_csr:.4f}s, CSC={t_col_csc:.4f}s")
