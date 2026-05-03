# Format Conversion

Converting between sparse matrix formats.

!!! tip "Mental Model"
    Different sparse formats excel at different tasks, so a typical workflow converts between them: build in COO or LIL (easy to assemble), then convert to CSR for row-oriented computation or CSC for column-oriented solvers. Conversion itself is cheap compared to the operations that follow, so convert once up front and reuse the result.

## Conversion Methods

### 1. To CSR

```python
from scipy import sparse

def main():
    coo = sparse.random(5, 5, density=0.3, format='coo')
    csr = coo.tocsr()
    print(f"Converted to CSR: {type(csr)}")

if __name__ == "__main__":
    main()
```

### 2. To CSC

```python
from scipy import sparse

def main():
    csr = sparse.random(5, 5, density=0.3, format='csr')
    csc = csr.tocsc()
    print(f"Converted to CSC: {type(csc)}")

if __name__ == "__main__":
    main()
```

### 3. To Dense

```python
from scipy import sparse

def main():
    csr = sparse.random(5, 5, density=0.3, format='csr')
    
    # Method 1
    dense1 = csr.toarray()
    
    # Method 2
    dense2 = csr.todense()  # Returns matrix
    
    print(type(dense1))  # ndarray
    print(type(dense2))  # matrix

if __name__ == "__main__":
    main()
```

## Conversion Table

| From/To | `.tocsr()` | `.tocsc()` | `.tocoo()` | `.tolil()` | `.toarray()` |
|:--------|:-----------|:-----------|:-----------|:-----------|:-------------|
| CSR | - | Fast | Fast | Slow | Fast |
| CSC | Fast | - | Fast | Slow | Fast |
| COO | Fast | Fast | - | Fast | Fast |
| LIL | Fast | Fast | Fast | - | Fast |

## Best Practices

### 1. Build then Convert

```python
from scipy import sparse

def main():
    # Build with LIL
    lil = sparse.lil_matrix((1000, 1000))
    for i in range(1000):
        lil[i, i] = 2
        if i > 0:
            lil[i, i-1] = -1
    
    # Convert once for computation
    csr = lil.tocsr()
    
    # Use CSR for all operations
    x = csr @ [1]*1000
    print(f"Result norm: {sum(x)}")

if __name__ == "__main__":
    main()
```

### 2. Avoid Repeated Conversion

```python
from scipy import sparse
import time

def main():
    A = sparse.random(1000, 1000, density=0.01, format='coo')
    
    # Bad: convert every iteration
    start = time.perf_counter()
    for _ in range(100):
        csr = A.tocsr()
        _ = csr.sum()
    bad_time = time.perf_counter() - start
    
    # Good: convert once
    start = time.perf_counter()
    csr = A.tocsr()
    for _ in range(100):
        _ = csr.sum()
    good_time = time.perf_counter() - start
    
    print(f"Bad (repeated): {bad_time:.4f} sec")
    print(f"Good (once):    {good_time:.4f} sec")

if __name__ == "__main__":
    main()
```

## Summary

- Use `.tocsr()` for row operations and general arithmetic
- Use `.tocsc()` for column operations
- Use `.toarray()` only for small matrices or visualization
- Convert once, use many times

---

## Exercises

**Exercise 1.**
Create a $100 \times 100$ sparse random matrix in COO format with density 0.05 (use `np.random.seed(3)`). Convert it to CSR, CSC, and LIL formats. Print the type of each and verify that all four representations produce the same dense array (using `toarray()`).

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        np.random.seed(3)
        coo = sparse.random(100, 100, density=0.05, format='coo')

        csr = coo.tocsr()
        csc = coo.tocsc()
        lil = coo.tolil()

        print(f"COO: {type(coo)}")
        print(f"CSR: {type(csr)}")
        print(f"CSC: {type(csc)}")
        print(f"LIL: {type(lil)}")

        dense_ref = coo.toarray()
        assert np.allclose(dense_ref, csr.toarray())
        assert np.allclose(dense_ref, csc.toarray())
        assert np.allclose(dense_ref, lil.toarray())
        print("All formats produce identical dense arrays.")

---

**Exercise 2.**
Build a $500 \times 500$ tridiagonal matrix using `sparse.lil_matrix` (set the diagonal to 4 and the off-diagonals to -1 in a loop). Convert to CSR and compute a matrix-vector product with a random vector. Measure the time for 100 matrix-vector products in CSR format and print it.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse
        import time

        n = 500
        lil = sparse.lil_matrix((n, n))
        for i in range(n):
            lil[i, i] = 4
            if i > 0:
                lil[i, i - 1] = -1
            if i < n - 1:
                lil[i, i + 1] = -1

        csr = lil.tocsr()
        x = np.random.randn(n)

        start = time.perf_counter()
        for _ in range(100):
            y = csr @ x
        elapsed = time.perf_counter() - start
        print(f"100 matvecs in CSR: {elapsed:.4f} sec")

---

**Exercise 3.**
Start with a COO matrix built from triplets: `row = [0, 0, 1, 1, 2]`, `col = [0, 2, 1, 2, 0]`, `data = [1, 2, 3, 4, 5]` with shape $(3, 3)$. Convert to CSR and examine the internal arrays (`data`, `indices`, `indptr`). Print all three arrays and explain how `indptr` encodes the row boundaries.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse

        row = [0, 0, 1, 1, 2]
        col = [0, 2, 1, 2, 0]
        data = [1, 2, 3, 4, 5]

        coo = sparse.coo_matrix((data, (row, col)), shape=(3, 3))
        csr = coo.tocsr()

        print(f"data:    {csr.data}")
        print(f"indices: {csr.indices}")
        print(f"indptr:  {csr.indptr}")
        print(f"\nDense:\n{csr.toarray()}")
        print("\nindptr[i]:indptr[i+1] gives the slice of data/indices for row i")
