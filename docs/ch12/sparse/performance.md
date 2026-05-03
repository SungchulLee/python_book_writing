# Performance Tips

Best practices for sparse matrix performance.

!!! tip "Mental Model"
    Sparse performance boils down to three rules: convert to the right format once up front, never access individual elements in a loop, and avoid operations that destroy sparsity. Most performance problems come from repeatedly converting formats inside loops or from treating sparse matrices like dense NumPy arrays with element-wise access.

## 1. Convert Once

```python
from scipy import sparse

# Bad: repeated conversion
for i in range(100):
    csr = coo.tocsr()
    result = csr @ x

# Good: convert once
csr = coo.tocsr()
for i in range(100):
    result = csr @ x
```

## 2. Use Right Format

| Operation | Best Format |
|:----------|:------------|
| A @ x | CSR |
| A[:, j] | CSC |
| A[i, :] | CSR |
| Build | LIL, COO |

## 3. Avoid Element Access

```python
# Bad: element-by-element
for i in range(n):
    for j in range(n):
        A[i, j] = func(i, j)

# Good: build with COO
rows, cols, data = [], [], []
for i in range(n):
    for j in range(n):
        if (val := func(i, j)) != 0:
            rows.append(i)
            cols.append(j)
            data.append(val)
A = sparse.coo_matrix((data, (rows, cols)))
```

## 4. Preallocate When Possible

Use `lil_matrix` for incremental builds, then convert.

## 5. Monitor Fill-in

Matrix products can dramatically increase density.

---

## Exercises

**Exercise 1.**
Create a $500 \times 500$ sparse matrix using COO format (density 0.02, `np.random.seed(9)`). Measure the time for 200 matrix-vector products when: (a) converting COO to CSR once and reusing, versus (b) converting COO to CSR in every iteration. Print both times and the speedup factor.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse
        import time

        np.random.seed(9)
        coo = sparse.random(500, 500, density=0.02, format='coo')
        x = np.random.randn(500)

        # (a) Convert once
        csr = coo.tocsr()
        start = time.perf_counter()
        for _ in range(200):
            y = csr @ x
        t_once = time.perf_counter() - start

        # (b) Convert every time
        start = time.perf_counter()
        for _ in range(200):
            csr_temp = coo.tocsr()
            y = csr_temp @ x
        t_every = time.perf_counter() - start

        print(f"Convert once:       {t_once:.4f} sec")
        print(f"Convert every time: {t_every:.4f} sec")
        print(f"Speedup: {t_every / t_once:.1f}x")

---

**Exercise 2.**
Compare two approaches for building a $1000 \times 1000$ tridiagonal matrix: (a) element-by-element insertion in a CSR matrix, (b) building with `sparse.diags`. Time both methods and print the results. Explain why approach (b) is faster.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse
        import time

        n = 1000

        # (a) Element-by-element with LIL (CSR is worse for insertion)
        start = time.perf_counter()
        lil = sparse.lil_matrix((n, n))
        for i in range(n):
            lil[i, i] = 2
            if i > 0:
                lil[i, i - 1] = -1
            if i < n - 1:
                lil[i, i + 1] = -1
        A1 = lil.tocsr()
        t_loop = time.perf_counter() - start

        # (b) Using sparse.diags
        start = time.perf_counter()
        A2 = sparse.diags([-1, 2, -1], [-1, 0, 1],
                           shape=(n, n), format='csr')
        t_diags = time.perf_counter() - start

        print(f"Element-by-element: {t_loop:.4f} sec")
        print(f"sparse.diags:       {t_diags:.4f} sec")
        print(f"Speedup: {t_loop / t_diags:.1f}x")

---

**Exercise 3.**
Create a $2000 \times 2000$ sparse matrix with density 0.005 (use `np.random.seed(1)`). Compute $A^T A$ (a common operation in least squares). Measure the time and print the density of both $A$ and $A^T A$. Suggest when it would be better to use the normal equations versus QR factorization based on the fill-in observed.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        import time

        np.random.seed(1)
        n = 2000
        A = sparse.random(n, n, density=0.005, format='csr')

        start = time.perf_counter()
        ATA = A.T @ A
        elapsed = time.perf_counter() - start

        print(f"A density:     {A.nnz / n**2:.4%}")
        print(f"A^T A density: {ATA.nnz / n**2:.4%}")
        print(f"Time for A^T A: {elapsed:.4f} sec")
        print(f"Fill-in factor: {ATA.nnz / A.nnz:.1f}x")
