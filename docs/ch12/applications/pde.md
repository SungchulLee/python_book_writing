# PDE Discretization

Sparse matrices from discretizing PDEs.

!!! tip "Mental Model"
    Discretizing a PDE on a grid turns it into a linear system where each grid point only interacts with its immediate neighbors. The resulting matrix is extremely sparse -- a 1000-point grid produces a matrix with a million entries but only a few thousand nonzeros. Sparse solvers exploit this structure to solve PDE systems that would be impossible with dense methods.

## 1D Laplacian

```python
import numpy as np
from scipy import sparse
from scipy.sparse import linalg as splinalg

def main():
    n = 100
    h = 1 / (n + 1)
    
    # Tridiagonal Laplacian
    A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n)) / h**2
    
    # Solve -u'' = f with u(0) = u(1) = 0
    x = np.linspace(h, 1-h, n)
    f = np.sin(np.pi * x)
    
    u = splinalg.spsolve(A.tocsr(), f)
    
    print(f"Solution at midpoint: {u[n//2]:.6f}")
    print(f"Exact: {np.sin(np.pi * 0.5) / np.pi**2:.6f}")

if __name__ == "__main__":
    main()
```

## 2D Laplacian

```python
import numpy as np
from scipy import sparse

def main():
    n = 10  # Grid points per dimension
    N = n * n  # Total unknowns
    
    # 5-point stencil
    diag = 4 * np.ones(N)
    off1 = -np.ones(N - 1)
    off1[n-1::n] = 0  # No wrap at row boundaries
    offn = -np.ones(N - n)
    
    A = sparse.diags([offn, off1, diag, off1, offn], 
                     [-n, -1, 0, 1, n], format='csr')
    
    print(f"2D Laplacian: {A.shape}")
    print(f"Nonzeros: {A.nnz}")
    print(f"Density: {A.nnz / N**2:.4%}")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Construct the 1D Laplacian matrix for $n = 50$ interior grid points with grid spacing $h = 1/(n+1)$. Solve the Poisson equation $-u'' = \pi^2 \sin(\pi x)$ with homogeneous Dirichlet boundary conditions. Compare the numerical solution at the midpoint with the exact solution $u(x) = \sin(\pi x)$ and print the absolute error.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 50
        h = 1 / (n + 1)
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n)) / h**2

        x = np.linspace(h, 1 - h, n)
        f = np.pi**2 * np.sin(np.pi * x)

        u = splinalg.spsolve(A.tocsr(), f)

        mid = n // 2
        exact = np.sin(np.pi * x[mid])
        error = abs(u[mid] - exact)
        print(f"Numerical at midpoint: {u[mid]:.8f}")
        print(f"Exact at midpoint:     {exact:.8f}")
        print(f"Absolute error:        {error:.2e}")

---

**Exercise 2.**
Build the 2D Laplacian using the 5-point stencil for a $20 \times 20$ interior grid. Print the matrix shape, the number of nonzeros, and the sparsity (percentage of zero entries). Verify that the matrix is symmetric by checking that `(A - A.T).nnz == 0`.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse

        n = 20
        N = n * n

        diag = 4 * np.ones(N)
        off1 = -np.ones(N - 1)
        off1[n - 1::n] = 0  # no wrap at row boundaries
        offn = -np.ones(N - n)

        A = sparse.diags([offn, off1, diag, off1, offn],
                         [-n, -1, 0, 1, n], format='csr')

        print(f"Shape: {A.shape}")
        print(f"Nonzeros: {A.nnz}")
        sparsity = 1 - A.nnz / (N * N)
        print(f"Sparsity: {sparsity:.4%}")
        print(f"Symmetric: {(A - A.T).nnz == 0}")

---

**Exercise 3.**
For the 1D Laplacian with $n = 200$, compute the 5 smallest eigenvalues using `scipy.sparse.linalg.eigsh`. Compare them with the exact eigenvalues $\lambda_k = \frac{4}{h^2}\sin^2\!\bigl(\frac{k\pi h}{2}\bigr)$ for $k = 1, \ldots, 5$ and print the maximum absolute error.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse
        from scipy.sparse import linalg as splinalg

        n = 200
        h = 1 / (n + 1)
        A = sparse.diags([-1, 2, -1], [-1, 0, 1], shape=(n, n)) / h**2

        vals, _ = splinalg.eigsh(A.tocsr(), k=5, which='SM')
        vals = np.sort(vals)

        exact = np.array([4 / h**2 * np.sin(k * np.pi * h / 2)**2
                          for k in range(1, 6)])
        max_error = np.max(np.abs(vals - exact))
        print(f"Numerical eigenvalues: {vals}")
        print(f"Exact eigenvalues:     {exact}")
        print(f"Max absolute error:    {max_error:.2e}")
