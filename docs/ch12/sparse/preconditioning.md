# Preconditioning

Preconditioners accelerate iterative solver convergence.

!!! tip "Mental Model"
    A preconditioner transforms a hard-to-solve system into an easier one that an iterative solver can crack quickly. Instead of solving $Ax = b$ directly, you solve $M^{-1}Ax = M^{-1}b$ where $M$ approximates $A$ but is cheap to invert. The better $M$ approximates $A$, the fewer iterations you need -- but a more accurate $M$ costs more to build, so there is always a tradeoff.

## Why Precondition

### 1. Condition Number Effect

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 500
    # Ill-conditioned system
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    A = A + sparse.diags([0.01], [n//2], shape=(n, n))
    b = np.ones(n)
    
    # Without preconditioning
    x1, info1 = splinalg.cg(A, b, maxiter=1000)
    
    # With ILU preconditioning
    M = splinalg.spilu(A.tocsc())
    M_op = splinalg.LinearOperator(A.shape, M.solve)
    x2, info2 = splinalg.cg(A, b, M=M_op, maxiter=1000)
    
    print(f"Without precond: info={info1}")
    print(f"With ILU precond: info={info2}")

if __name__ == "__main__":
    main()
```

## ILU Preconditioner

### 1. Incomplete LU

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 1000
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csc')
    b = np.ones(n)
    
    # Create ILU preconditioner
    ilu = splinalg.spilu(A)
    M = splinalg.LinearOperator(A.shape, ilu.solve)
    
    # Solve with preconditioning
    x, info = splinalg.cg(A.tocsr(), b, M=M)
    
    print(f"Residual: {np.linalg.norm(A @ x - b):.2e}")

if __name__ == "__main__":
    main()
```

## Diagonal Preconditioner

### 1. Jacobi Preconditioner

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 500
    A = sparse.diags([-1, 4, -1], [-1, 0, 1], shape=(n, n), format='csr')
    b = np.ones(n)
    
    # Jacobi: M = diag(A)
    diag_A = A.diagonal()
    M = splinalg.LinearOperator(A.shape, lambda x: x / diag_A)
    
    x, info = splinalg.cg(A, b, M=M)
    
    print(f"Converged: {info == 0}")

if __name__ == "__main__":
    main()
```

## Performance Comparison

### 1. Iteration Count

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 1000
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
    b = np.ones(n)
    
    def count_iterations(M=None):
        count = [0]
        def callback(xk):
            count[0] += 1
        splinalg.cg(A, b, M=M, callback=callback, tol=1e-10)
        return count[0]
    
    # No preconditioning
    iters_none = count_iterations()
    
    # ILU preconditioning
    ilu = splinalg.spilu(A.tocsc())
    M_ilu = splinalg.LinearOperator(A.shape, ilu.solve)
    iters_ilu = count_iterations(M_ilu)
    
    print(f"No precond:  {iters_none} iterations")
    print(f"ILU precond: {iters_ilu} iterations")

if __name__ == "__main__":
    main()
```

## Summary

| Preconditioner | Cost | Effectiveness |
|:---------------|:-----|:--------------|
| Jacobi (diagonal) | Low | Moderate |
| ILU | Medium | Good |
| Sparse Cholesky | High | Excellent |

Key: Choose preconditioner based on cost vs. iteration reduction trade-off.

---

## Exercises

**Exercise 1.**
Create a $500 \times 500$ sparse SPD matrix: start with a tridiagonal matrix (2 on diagonal, -1 on off-diagonals) and add a small random perturbation to make it less well-conditioned (use `np.random.seed(3)`). Solve $Ax = b$ with CG both with and without a Jacobi (diagonal) preconditioner. Print the iteration counts for both and the residuals.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        np.random.seed(3)
        n = 500
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
        A = A + sparse.random(n, n, density=0.001, format='csr')
        A = (A + A.T) / 2 + 3 * sparse.eye(n)  # ensure SPD
        b = np.ones(n)

        # Without preconditioner
        count_no = [0]
        def cb1(xk): count_no[0] += 1
        x1, info1 = splinalg.cg(A, b, tol=1e-10, callback=cb1)

        # Jacobi preconditioner
        diag_A = A.diagonal()
        M = splinalg.LinearOperator(A.shape, lambda x: x / diag_A)
        count_pre = [0]
        def cb2(xk): count_pre[0] += 1
        x2, info2 = splinalg.cg(A, b, M=M, tol=1e-10, callback=cb2)

        print(f"No precond: {count_no[0]} iters, residual={np.linalg.norm(A@x1-b):.2e}")
        print(f"Jacobi:     {count_pre[0]} iters, residual={np.linalg.norm(A@x2-b):.2e}")

---

**Exercise 2.**
Build a $1000 \times 1000$ sparse SPD tridiagonal matrix. Create an ILU preconditioner using `spilu` and wrap it as a `LinearOperator`. Solve $Ax = b$ using CG with this preconditioner and compare the iteration count to unpreconditioned CG. Print both iteration counts.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 1000
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
        b = np.ones(n)

        # No preconditioner
        count_no = [0]
        def cb1(xk): count_no[0] += 1
        splinalg.cg(A, b, tol=1e-10, callback=cb1)

        # ILU preconditioner
        ilu = splinalg.spilu(A.tocsc())
        M = splinalg.LinearOperator(A.shape, ilu.solve)
        count_ilu = [0]
        def cb2(xk): count_ilu[0] += 1
        splinalg.cg(A, b, M=M, tol=1e-10, callback=cb2)

        print(f"No preconditioner: {count_no[0]} iterations")
        print(f"ILU preconditioner: {count_ilu[0]} iterations")

---

**Exercise 3.**
Demonstrate the effect of condition number on convergence. Create two $500 \times 500$ SPD tridiagonal matrices: one well-conditioned (diagonal = 10, off-diagonal = -1) and one ill-conditioned (diagonal = 2, off-diagonal = -1). Solve both with CG (no preconditioner) and print the iteration counts. Then apply ILU preconditioning to the ill-conditioned system and print the new iteration count.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 500
        b = np.ones(n)

        # Well-conditioned
        A_good = sparse.diags([-1, 10, -1], [-1, 0, 1], shape=(n, n), format='csr')
        count_good = [0]
        def cb1(xk): count_good[0] += 1
        splinalg.cg(A_good, b, tol=1e-10, callback=cb1)

        # Ill-conditioned
        A_bad = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n), format='csr')
        count_bad = [0]
        def cb2(xk): count_bad[0] += 1
        splinalg.cg(A_bad, b, tol=1e-10, callback=cb2)

        # Ill-conditioned with ILU
        ilu = splinalg.spilu(A_bad.tocsc())
        M = splinalg.LinearOperator(A_bad.shape, ilu.solve)
        count_ilu = [0]
        def cb3(xk): count_ilu[0] += 1
        splinalg.cg(A_bad, b, M=M, tol=1e-10, callback=cb3)

        print(f"Well-conditioned (no precond): {count_good[0]} iterations")
        print(f"Ill-conditioned (no precond):  {count_bad[0]} iterations")
        print(f"Ill-conditioned (ILU precond): {count_ilu[0]} iterations")
