# Direct Solvers

Direct methods for solving sparse linear systems.

!!! tip "Mental Model"
    Direct sparse solvers factor the matrix exactly (like LU), then solve by substitution. They give you the answer in a predictable amount of time with no convergence worries, but the factorization can create "fill-in" -- new nonzeros that weren't in the original matrix. For moderate-sized sparse systems, direct solvers are the reliable default; for very large systems, consider iterative methods instead.

## spsolve

### 1. Basic Usage

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    A = sparse.csr_matrix([[4, 1, 0],
                           [1, 4, 1],
                           [0, 1, 4]])
    b = np.array([1, 2, 1])
    
    x = splinalg.spsolve(A, b)
    
    print(f"Solution: x = {x}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

## splu - Sparse LU

### 1. Factor Once, Solve Multiple

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 1000
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csc')
    
    # Factor once
    lu = splinalg.splu(A)
    
    # Solve multiple systems
    for i in range(3):
        b = np.random.randn(n)
        x = lu.solve(b)
        print(f"System {i}: residual = {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

### 2. Fill-in Management

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 100
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csc')
    
    lu = splinalg.splu(A)
    
    print(f"Original nnz: {A.nnz}")
    print(f"L nnz: {lu.L.nnz}")
    print(f"U nnz: {lu.U.nnz}")

if __name__ == "__main__":
    main()
```

## spilu - Incomplete LU

### 1. Preconditioner

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 100
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csc')
    
    # Incomplete LU (for preconditioning)
    ilu = splinalg.spilu(A)
    
    print(f"Original nnz: {A.nnz}")
    print(f"ILU L nnz: {ilu.L.nnz}")
    print(f"ILU U nnz: {ilu.U.nnz}")

if __name__ == "__main__":
    main()
```

## Performance

### 1. Sparse vs Dense

```python
import numpy as np
from scipy import sparse, linalg
from scipy.sparse import linalg as splinalg
import time

def main():
    n = 2000
    A_sparse = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csc')
    A_dense = A_sparse.toarray()
    b = np.random.randn(n)
    
    # Dense solve
    start = time.perf_counter()
    x_dense = linalg.solve(A_dense, b)
    dense_time = time.perf_counter() - start
    
    # Sparse solve
    start = time.perf_counter()
    x_sparse = splinalg.spsolve(A_sparse, b)
    sparse_time = time.perf_counter() - start
    
    print(f"Dense solve:  {dense_time:.4f} sec")
    print(f"Sparse solve: {sparse_time:.4f} sec")
    print(f"Speedup: {dense_time/sparse_time:.1f}x")

if __name__ == "__main__":
    main()
```

## Summary

| Function | Description |
|:---------|:------------|
| `spsolve(A, b)` | Direct sparse solve |
| `splu(A)` | Sparse LU factorization |
| `spilu(A)` | Incomplete LU (preconditioner) |

Use CSC format for direct solvers.

---

## Exercises

**Exercise 1.**
Create a $500 \times 500$ sparse tridiagonal SPD matrix (2 on diagonal, -1 on off-diagonals) and a random right-hand side vector. Solve the system using `spsolve` and verify the residual norm is below $10^{-10}$.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 500
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
        b = np.random.randn(n)

        x = splinalg.spsolve(A, b)
        residual = np.linalg.norm(A @ x - b)
        print(f"Residual norm: {residual:.2e}")
        assert residual < 1e-10

---

**Exercise 2.**
Use `splu` to factor a $1000 \times 1000$ sparse tridiagonal matrix (in CSC format). Solve the system for 10 different random right-hand sides using the pre-computed factorization. Print the average residual norm across all 10 solves.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 1000
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csc')
        lu = splinalg.splu(A)

        residuals = []
        for _ in range(10):
            b = np.random.randn(n)
            x = lu.solve(b)
            residuals.append(np.linalg.norm(A @ x - b))

        avg_residual = np.mean(residuals)
        print(f"Average residual norm: {avg_residual:.2e}")

---

**Exercise 3.**
Compare `spsolve` and `splu` + `lu.solve` for a $2000 \times 2000$ sparse tridiagonal system. Factor the matrix once with `splu`, then solve for 5 right-hand sides with both approaches. Measure and print the total time for each approach (including the factorization time for `splu`).

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg
        import time

        n = 2000
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csc')
        bs = [np.random.randn(n) for _ in range(5)]

        # spsolve approach
        start = time.perf_counter()
        for b in bs:
            x = splinalg.spsolve(A, b)
        time_spsolve = time.perf_counter() - start

        # splu approach
        start = time.perf_counter()
        lu = splinalg.splu(A)
        for b in bs:
            x = lu.solve(b)
        time_splu = time.perf_counter() - start

        print(f"spsolve (5 solves):     {time_spsolve:.4f} sec")
        print(f"splu + solve (5 solves): {time_splu:.4f} sec")
