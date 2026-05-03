# Iterative Solvers

Iterative methods for large sparse linear systems.

!!! tip "Mental Model"
    Iterative solvers never factor the matrix -- they only need to multiply it by vectors, refining an approximate solution at each step. This makes them ideal for very large sparse systems where even the factorization would be too expensive. The tradeoff is that convergence depends on the matrix's condition number, and a poor condition number may require preconditioning to get a useful answer.

## Conjugate Gradient (CG)

### 1. For SPD Matrices

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 1000
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    b = np.ones(n)
    
    x, info = splinalg.cg(A, b)
    
    print(f"Converged: {info == 0}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

### 2. With Tolerance

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 1000
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    b = np.ones(n)
    
    x, info = splinalg.cg(A, b, tol=1e-10, maxiter=500)
    
    print(f"Info: {info}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

## GMRES

### 1. For General Matrices

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 500
    A = sparse.random(n, n, density=0.01, format='csr')
    A = A + sparse.eye(n) * 10  # Make diagonally dominant
    b = np.ones(n)
    
    x, info = splinalg.gmres(A, b)
    
    print(f"Converged: {info == 0}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

## BiCGSTAB

### 1. Another Option for Non-symmetric

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 500
    A = sparse.random(n, n, density=0.01, format='csr')
    A = A + sparse.eye(n) * 10
    b = np.ones(n)
    
    x, info = splinalg.bicgstab(A, b)
    
    print(f"Converged: {info == 0}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

## Callback for Monitoring

### 1. Track Convergence

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 500
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    b = np.ones(n)
    
    residuals = []
    def callback(xk):
        r = np.linalg.norm(A @ xk - b)
        residuals.append(r)
    
    x, info = splinalg.cg(A, b, callback=callback)
    
    print(f"Iterations: {len(residuals)}")
    print(f"Final residual: {residuals[-1]:.2e}")

if __name__ == "__main__":
    main()
```

## Method Selection

| Method | Matrix Type | Memory |
|:-------|:------------|:-------|
| CG | SPD | Low |
| GMRES | General | High (grows) |
| BiCGSTAB | General | Low |
| MINRES | Symmetric | Low |

## Summary

| Function | Use Case |
|:---------|:---------|
| `cg(A, b)` | Symmetric positive definite |
| `gmres(A, b)` | General (non-symmetric) |
| `bicgstab(A, b)` | General, memory-efficient |
| `minres(A, b)` | Symmetric indefinite |

---

## Exercises

**Exercise 1.**
Create a $2000 \times 2000$ sparse SPD tridiagonal matrix (3 on diagonal, -1 on off-diagonals). Solve $Ax = b$ where $b$ is a vector of ones using CG with tolerance $10^{-12}$. Use a callback to count the number of iterations. Print the iteration count and final residual.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 2000
        A = sparse.diags([-1, 3, -1], [-1, 0, 1], shape=(n, n), format='csr')
        b = np.ones(n)

        count = [0]
        def callback(xk):
            count[0] += 1

        x, info = splinalg.cg(A, b, tol=1e-12, callback=callback)
        residual = np.linalg.norm(A @ x - b)

        print(f"Iterations: {count[0]}")
        print(f"Converged: {info == 0}")
        print(f"Residual: {residual:.2e}")

---

**Exercise 2.**
Build a $500 \times 500$ sparse non-symmetric matrix by adding `sparse.eye(500) * 10` to a random sparse matrix with density 0.02 (use `np.random.seed(4)`). Solve $Ax = b$ with $b = \mathbf{1}$ using both GMRES and BiCGSTAB. Compare the residual norms and convergence status.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        np.random.seed(4)
        n = 500
        A = sparse.random(n, n, density=0.02, format='csr') + sparse.eye(n) * 10
        b = np.ones(n)

        x_gmres, info_gmres = splinalg.gmres(A, b)
        r_gmres = np.linalg.norm(A @ x_gmres - b)

        x_bicg, info_bicg = splinalg.bicgstab(A, b)
        r_bicg = np.linalg.norm(A @ x_bicg - b)

        print(f"GMRES:    converged={info_gmres == 0}, residual={r_gmres:.2e}")
        print(f"BiCGSTAB: converged={info_bicg == 0}, residual={r_bicg:.2e}")

---

**Exercise 3.**
For a $1000 \times 1000$ sparse SPD tridiagonal matrix, solve $Ax = b$ using CG both with and without a Jacobi (diagonal) preconditioner. Count iterations for each approach and print the speedup in iteration count from preconditioning.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 1000
        A = sparse.diags([-1, 3, -1], [-1, 0, 1], shape=(n, n), format='csr')
        b = np.ones(n)

        # Without preconditioner
        count_no = [0]
        def cb_no(xk):
            count_no[0] += 1
        splinalg.cg(A, b, tol=1e-10, callback=cb_no)

        # With Jacobi preconditioner
        diag_A = A.diagonal()
        M = splinalg.LinearOperator(A.shape, lambda x: x / diag_A)
        count_pre = [0]
        def cb_pre(xk):
            count_pre[0] += 1
        splinalg.cg(A, b, M=M, tol=1e-10, callback=cb_pre)

        print(f"Without precond: {count_no[0]} iterations")
        print(f"With Jacobi:     {count_pre[0]} iterations")
        if count_pre[0] > 0:
            print(f"Speedup: {count_no[0] / count_pre[0]:.1f}x")
