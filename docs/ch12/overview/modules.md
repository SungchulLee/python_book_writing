# Module Organization

SciPy provides linear algebra functionality across multiple modules.

!!! tip "Mental Model"
    SciPy's linear algebra lives in three places: `scipy.linalg` for dense matrices, `scipy.sparse` for sparse matrix classes, and `scipy.sparse.linalg` for sparse solvers. Knowing which module to import is half the battle -- dense operations assume the full matrix fits in memory, while sparse operations work only with the nonzero entries.

## Core Modules

### 1. scipy.linalg

Dense matrix operations and decompositions.

```python
from scipy import linalg

# Key functions
# linalg.lu, linalg.qr, linalg.svd
# linalg.eig, linalg.eigh
# linalg.solve, linalg.inv
# linalg.expm, linalg.logm
```

### 2. scipy.sparse

Sparse matrix classes and construction.

```python
from scipy import sparse

# Sparse matrix formats
# sparse.csr_matrix, sparse.csc_matrix
# sparse.coo_matrix, sparse.lil_matrix
# sparse.dia_matrix, sparse.dok_matrix
```

### 3. scipy.sparse.linalg

Sparse linear algebra operations.

```python
from scipy.sparse import linalg as splinalg

# Sparse solvers
# splinalg.spsolve, splinalg.splu
# splinalg.cg, splinalg.gmres
# splinalg.eigs, splinalg.eigsh
```

## Module Overview

### 1. Hierarchy

```
scipy
├── linalg           # Dense operations
│   ├── decompositions (lu, qr, svd, cholesky, schur)
│   ├── eigenvalues (eig, eigh, eigvals)
│   ├── solvers (solve, solve_triangular, solve_banded)
│   ├── matrix functions (expm, logm, sqrtm)
│   └── special matrices (toeplitz, circulant, companion)
│
├── sparse           # Sparse matrix classes
│   ├── csr_matrix, csc_matrix
│   ├── coo_matrix, lil_matrix
│   └── construction functions
│
└── sparse.linalg    # Sparse operations
    ├── direct solvers (spsolve, splu)
    ├── iterative solvers (cg, gmres, bicg)
    └── eigensolvers (eigs, eigsh)
```

### 2. Import Patterns

```python
import numpy as np
from scipy import linalg
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    # Dense matrix
    A_dense = np.array([[4, 1], [1, 3]])
    
    # Dense operations via scipy.linalg
    L = linalg.cholesky(A_dense, lower=True)
    print("Cholesky L:")
    print(L)
    print()
    
    # Sparse matrix
    A_sparse = sparse.csr_matrix(A_dense)
    
    # Sparse operations via scipy.sparse.linalg
    b = np.array([1, 2])
    x = splinalg.spsolve(A_sparse, b)
    print(f"Sparse solve: x = {x}")

if __name__ == "__main__":
    main()
```

## Function Categories

### 1. Decompositions

| Function | Module | Description |
|:---------|:-------|:------------|
| `lu` | `linalg` | LU factorization |
| `qr` | `linalg` | QR factorization |
| `svd` | `linalg` | Singular value decomposition |
| `cholesky` | `linalg` | Cholesky decomposition |
| `schur` | `linalg` | Schur decomposition |
| `hessenberg` | `linalg` | Hessenberg form |

### 2. Eigenvalue Problems

| Function | Module | Description |
|:---------|:-------|:------------|
| `eig` | `linalg` | General eigenvalues |
| `eigh` | `linalg` | Hermitian eigenvalues |
| `eigvals` | `linalg` | Eigenvalues only |
| `eigs` | `sparse.linalg` | Sparse eigenvalues |
| `eigsh` | `sparse.linalg` | Sparse Hermitian eigenvalues |

### 3. Linear Solvers

| Function | Module | Description |
|:---------|:-------|:------------|
| `solve` | `linalg` | Dense system solver |
| `solve_triangular` | `linalg` | Triangular solver |
| `solve_banded` | `linalg` | Banded matrix solver |
| `spsolve` | `sparse.linalg` | Sparse direct solver |
| `cg` | `sparse.linalg` | Conjugate gradient |
| `gmres` | `sparse.linalg` | GMRES iterative |

### 4. Matrix Functions

| Function | Module | Description |
|:---------|:-------|:------------|
| `expm` | `linalg` | Matrix exponential |
| `logm` | `linalg` | Matrix logarithm |
| `sqrtm` | `linalg` | Matrix square root |
| `funm` | `linalg` | General matrix function |

## Practical Usage

### 1. Dense Workflow

```python
import numpy as np
from scipy import linalg

def main():
    A = np.random.randn(100, 100)
    A = A @ A.T  # Make symmetric positive definite
    b = np.random.randn(100)
    
    # Solve using Cholesky
    c, low = linalg.cho_factor(A)
    x = linalg.cho_solve((c, low), b)
    
    print(f"Solution norm: {np.linalg.norm(x):.4f}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

### 2. Sparse Workflow

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    # Create sparse matrix
    n = 1000
    diags = [-np.ones(n-1), 2*np.ones(n), -np.ones(n-1)]
    A = sparse.diags(diags, [-1, 0, 1], format='csr')
    
    b = np.ones(n)
    
    # Solve sparse system
    x = splinalg.spsolve(A, b)
    
    print(f"Solution norm: {np.linalg.norm(x):.4f}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

## Summary

### 1. Quick Reference

| Task | Module |
|:-----|:-------|
| Dense decompositions | `scipy.linalg` |
| Dense solvers | `scipy.linalg` |
| Matrix functions | `scipy.linalg` |
| Sparse matrices | `scipy.sparse` |
| Sparse solvers | `scipy.sparse.linalg` |
| Sparse eigenvalues | `scipy.sparse.linalg` |

---

## Exercises

**Exercise 1.**
Write a script that imports `scipy.linalg`, `scipy.sparse`, and `scipy.sparse.linalg`. Create a $5 \times 5$ dense SPD matrix, solve $Ax = b$ using `linalg.cho_factor` and `linalg.cho_solve`. Then convert $A$ to a sparse CSR matrix and solve the same system with `splinalg.spsolve`. Verify both solutions agree (norm of difference below $10^{-12}$).

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg, sparse
        from scipy.sparse import linalg as splinalg

        np.random.seed(0)
        B = np.random.randn(5, 5)
        A = B @ B.T + 5 * np.eye(5)
        b = np.random.randn(5)

        # Dense Cholesky solve
        c, low = linalg.cho_factor(A)
        x_dense = linalg.cho_solve((c, low), b)

        # Sparse solve
        A_sparse = sparse.csr_matrix(A)
        x_sparse = splinalg.spsolve(A_sparse, b)

        diff = np.linalg.norm(x_dense - x_sparse)
        print(f"Dense solution:  {x_dense}")
        print(f"Sparse solution: {x_sparse}")
        print(f"Difference norm: {diff:.2e}")

---

**Exercise 2.**
Use `scipy.linalg` functions to perform the following pipeline on a random $6 \times 6$ matrix (use `np.random.seed(8)`): (1) compute the LU decomposition, (2) compute the QR decomposition, (3) compute the eigenvalues. Print the shapes of all decomposition outputs and the eigenvalues.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        np.random.seed(8)
        A = np.random.randn(6, 6)

        # LU decomposition
        P, L, U = linalg.lu(A)
        print(f"LU: P {P.shape}, L {L.shape}, U {U.shape}")

        # QR decomposition
        Q, R = linalg.qr(A)
        print(f"QR: Q {Q.shape}, R {R.shape}")

        # Eigenvalues
        eigenvalues = linalg.eigvals(A)
        print(f"Eigenvalues: {eigenvalues}")

---

**Exercise 3.**
Create a $500 \times 500$ sparse tridiagonal matrix using `scipy.sparse.diags`. Solve $Ax = b$ with $b = \mathbf{1}$ using three different approaches: `splinalg.spsolve`, `splinalg.cg`, and dense `linalg.solve` (after converting to dense). Print the residual norm for each method and compare.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg, sparse
        from scipy.sparse import linalg as splinalg

        n = 500
        A_sparse = sparse.diags([-1, 2, -1], [-1, 0, 1],
                                 shape=(n, n), format='csr')
        b = np.ones(n)

        # Method 1: spsolve
        x1 = splinalg.spsolve(A_sparse, b)
        r1 = np.linalg.norm(A_sparse @ x1 - b)

        # Method 2: CG
        x2, info = splinalg.cg(A_sparse, b)
        r2 = np.linalg.norm(A_sparse @ x2 - b)

        # Method 3: dense solve
        A_dense = A_sparse.toarray()
        x3 = linalg.solve(A_dense, b)
        r3 = np.linalg.norm(A_dense @ x3 - b)

        print(f"spsolve residual: {r1:.2e}")
        print(f"CG residual:      {r2:.2e}")
        print(f"Dense residual:   {r3:.2e}")
