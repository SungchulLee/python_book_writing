# Why Sparse Matrices

Sparse matrices efficiently represent matrices with mostly zero entries.

!!! tip "Mental Model"
    A 10,000 x 10,000 matrix has 100 million entries, but if only 0.1% are nonzero, storing all of them wastes 99.9% of your memory. Sparse formats store only the nonzero values and their positions, collapsing storage from $O(n^2)$ to $O(\text{nnz})$. The speedup follows the same logic: algorithms that skip zero entries can be orders of magnitude faster.

## Memory Efficiency

### 1. Dense vs Sparse Storage

```python
import numpy as np
from scipy import sparse
import sys

def main():
    n = 10000
    density = 0.001  # 0.1% nonzero
    
    # Dense storage
    A_dense = np.zeros((n, n))
    k = int(n * n * density)
    rows = np.random.randint(0, n, k)
    cols = np.random.randint(0, n, k)
    A_dense[rows, cols] = np.random.randn(k)
    
    # Sparse storage
    A_sparse = sparse.csr_matrix(A_dense)
    
    dense_size = A_dense.nbytes
    sparse_size = A_sparse.data.nbytes + A_sparse.indices.nbytes + A_sparse.indptr.nbytes
    
    print(f"Matrix size: {n} x {n}")
    print(f"Nonzeros: {k} ({density*100}%)")
    print(f"Dense storage:  {dense_size / 1e6:.1f} MB")
    print(f"Sparse storage: {sparse_size / 1e6:.3f} MB")
    print(f"Compression: {dense_size / sparse_size:.0f}x")

if __name__ == "__main__":
    main()
```

### 2. Complexity Analysis

| Storage | Memory |
|:--------|:-------|
| Dense | $O(mn)$ |
| Sparse | $O(k)$ where $k$ = nonzeros |

### 3. When Sparse Wins

```python
import numpy as np
from scipy import sparse

def main():
    n = 1000
    
    for density in [0.001, 0.01, 0.1, 0.5]:
        k = int(n * n * density)
        
        dense_mem = n * n * 8  # 8 bytes per float64
        sparse_mem = k * 8 + k * 4 + (n + 1) * 4  # data + indices + indptr
        
        ratio = dense_mem / sparse_mem
        winner = "Sparse" if ratio > 1 else "Dense"
        
        print(f"Density {density*100:5.1f}%: {winner} wins ({ratio:.1f}x)")

if __name__ == "__main__":
    main()
```

## Computational Efficiency

### 1. Matrix-Vector Multiply

```python
import numpy as np
from scipy import sparse
import time

def main():
    n = 5000
    density = 0.01
    
    # Create sparse matrix
    A_sparse = sparse.random(n, n, density=density, format='csr')
    A_dense = A_sparse.toarray()
    x = np.random.randn(n)
    
    # Dense multiplication
    start = time.perf_counter()
    for _ in range(10):
        y_dense = A_dense @ x
    dense_time = time.perf_counter() - start
    
    # Sparse multiplication
    start = time.perf_counter()
    for _ in range(10):
        y_sparse = A_sparse @ x
    sparse_time = time.perf_counter() - start
    
    print(f"Dense:  {dense_time:.4f} sec")
    print(f"Sparse: {sparse_time:.4f} sec")
    print(f"Speedup: {dense_time/sparse_time:.1f}x")

if __name__ == "__main__":
    main()
```

### 2. Operation Complexity

| Operation | Dense | Sparse |
|:----------|:------|:-------|
| $Ax$ (matrix-vector) | $O(n^2)$ | $O(k)$ |
| $A + B$ | $O(n^2)$ | $O(k_A + k_B)$ |
| Memory | $O(n^2)$ | $O(k)$ |

## Where Sparse Matrices Arise

### 1. PDEs (Finite Differences)

```python
import numpy as np
from scipy import sparse

def main():
    # 1D Laplacian: tridiagonal
    n = 100
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n))
    
    print(f"1D Laplacian ({n}x{n})")
    print(f"Nonzeros: {A.nnz}")
    print(f"Density: {A.nnz / (n*n) * 100:.2f}%")

if __name__ == "__main__":
    main()
```

### 2. Graphs (Adjacency)

```python
import numpy as np
from scipy import sparse

def main():
    # Social network: each person has ~150 connections
    n_people = 1_000_000
    avg_connections = 150
    
    # Theoretical storage
    dense_gb = n_people * n_people * 8 / 1e9
    sparse_gb = n_people * avg_connections * 12 / 1e9  # data + indices
    
    print(f"Network: {n_people:,} people, {avg_connections} avg connections")
    print(f"Dense storage:  {dense_gb:,.0f} GB (impossible)")
    print(f"Sparse storage: {sparse_gb:.2f} GB (feasible)")

if __name__ == "__main__":
    main()
```

### 3. Machine Learning (Features)

```python
import numpy as np
from scipy import sparse

def main():
    # Text classification: bag of words
    n_documents = 100_000
    vocabulary = 50_000
    avg_words_per_doc = 200
    
    # Feature matrix
    dense_gb = n_documents * vocabulary * 8 / 1e9
    sparse_gb = n_documents * avg_words_per_doc * 12 / 1e9
    
    print(f"Documents: {n_documents:,}")
    print(f"Vocabulary: {vocabulary:,}")
    print(f"Dense:  {dense_gb:.1f} GB")
    print(f"Sparse: {sparse_gb:.2f} GB")

if __name__ == "__main__":
    main()
```

## Summary

### 1. Use Sparse When

- Most entries are zero (density < 10%)
- Matrix is too large for dense storage
- Structure enables sparse operations

### 2. Use Dense When

- Matrix is small
- High density (> 30%)
- Need all dense operations

---

## Exercises

**Exercise 1.**
Create a $5000 \times 5000$ sparse matrix with density 0.002 and its dense equivalent (use `np.random.seed(0)`). Compare the memory usage of both representations by computing the byte sizes of the internal arrays. Print the compression ratio (dense bytes / sparse bytes).

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        np.random.seed(0)
        n = 5000
        A_sparse = sparse.random(n, n, density=0.002, format='csr')
        A_dense = A_sparse.toarray()

        dense_bytes = A_dense.nbytes
        sparse_bytes = (A_sparse.data.nbytes + A_sparse.indices.nbytes

                        + A_sparse.indptr.nbytes)

        print(f"Dense memory:  {dense_bytes / 1e6:.1f} MB")
        print(f"Sparse memory: {sparse_bytes / 1e6:.3f} MB")
        print(f"Compression ratio: {dense_bytes / sparse_bytes:.0f}x")

---

**Exercise 2.**
Benchmark sparse vs. dense matrix-vector multiplication for a $3000 \times 3000$ matrix with density 0.01 (use `np.random.seed(1)`). Perform 50 multiplications with each representation and print the total time for each. Compute the speedup factor.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse
        import time

        np.random.seed(1)
        n = 3000
        A_sparse = sparse.random(n, n, density=0.01, format='csr')
        A_dense = A_sparse.toarray()
        x = np.random.randn(n)

        start = time.perf_counter()
        for _ in range(50):
            y = A_dense @ x
        t_dense = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(50):
            y = A_sparse @ x
        t_sparse = time.perf_counter() - start

        print(f"Dense (50 matvecs):  {t_dense:.4f} sec")
        print(f"Sparse (50 matvecs): {t_sparse:.4f} sec")
        print(f"Speedup: {t_dense / t_sparse:.1f}x")

---

**Exercise 3.**
Investigate the crossover density at which sparse storage becomes more expensive than dense. For a $500 \times 500$ matrix, compute the theoretical memory for CSR format and dense format at densities 0.01, 0.05, 0.1, 0.2, 0.3, and 0.5. Print a table showing the density, dense memory, sparse memory, and which is smaller.

??? success "Solution to Exercise 3"
        import numpy as np

        n = 500
        print(f"{'Density':>8} {'Dense (KB)':>10} {'Sparse (KB)':>12} {'Winner':>8}")
        print("-" * 42)

        for density in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5]:
            k = int(n * n * density)
            dense_mem = n * n * 8  # float64
            sparse_mem = k * 8 + k * 4 + (n + 1) * 4  # data + indices + indptr
            winner = "Sparse" if sparse_mem < dense_mem else "Dense"
            print(f"{density:>8.2f} {dense_mem/1024:>10.0f} "
                  f"{sparse_mem/1024:>12.0f} {winner:>8}")
