# SciPy vs NumPy Linalg

SciPy's `scipy.linalg` extends NumPy's linear algebra capabilities.

!!! tip "Mental Model"
    NumPy provides the essentials -- determinants, eigenvalues, SVD, and basic solves. SciPy's `linalg` is a strict superset that adds specialized decompositions (LU, QR, Schur, Hessenberg), matrix functions (expm, logm), and LAPACK-level control over algorithm parameters. When in doubt, import from `scipy.linalg` -- it covers everything NumPy does and more.

## Module Comparison

### 1. Basic Import

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2], [3, 4]])
    
    # Both modules provide similar functions
    det_np = np.linalg.det(A)
    det_sp = linalg.det(A)
    
    print(f"NumPy det: {det_np}")
    print(f"SciPy det: {det_sp}")

if __name__ == "__main__":
    main()
```

### 2. Key Differences

| Feature | `numpy.linalg` | `scipy.linalg` |
|:--------|:---------------|:---------------|
| Scope | Core operations | Comprehensive |
| Decompositions | Basic (SVD, QR, Cholesky) | Extended (LU, Schur, Hessenberg) |
| Matrix functions | None | expm, logm, sqrtm |
| Special matrices | Limited | Extensive |
| LAPACK access | Indirect | Direct |
| Sparse support | No | Via `scipy.sparse.linalg` |

### 3. When to Use Which

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2], [2, 5]])
    
    # NumPy: simple operations
    eigvals_np = np.linalg.eigvals(A)
    print(f"NumPy eigvals: {eigvals_np}")
    
    # SciPy: more control and options
    eigvals_sp = linalg.eigvals(A)
    print(f"SciPy eigvals: {eigvals_sp}")

if __name__ == "__main__":
    main()
```

## Extended Functionality

### 1. Decompositions

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 10]])
    
    # LU decomposition (SciPy only)
    P, L, U = linalg.lu(A)
    
    print("P (permutation):")
    print(P)
    print()
    print("L (lower):")
    print(L)
    print()
    print("U (upper):")
    print(U)

if __name__ == "__main__":
    main()
```

### 2. Matrix Functions

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2], [0, 1]])
    
    # Matrix exponential (SciPy only)
    exp_A = linalg.expm(A)
    
    print("A =")
    print(A)
    print()
    print("exp(A) =")
    print(exp_A)

if __name__ == "__main__":
    main()
```

### 3. Special Solvers

```python
import numpy as np
from scipy import linalg

def main():
    # Triangular system (SciPy provides specialized solver)
    U = np.array([[2, 1, 3],
                  [0, 4, 2],
                  [0, 0, 5]])
    b = np.array([10, 14, 15])
    
    # Specialized triangular solver
    x = linalg.solve_triangular(U, b)
    
    print(f"x = {x}")
    print(f"Verify U @ x = {U @ x}")

if __name__ == "__main__":
    main()
```

## LAPACK and BLAS Access

### 1. Low-Level Routines

```python
import numpy as np
from scipy import linalg

def main():
    # Access LAPACK routines directly
    A = np.array([[1, 2], [3, 4]], dtype=float)
    
    # Get LAPACK function for LU factorization
    getrf = linalg.get_lapack_funcs('getrf', (A,))
    
    lu, piv, info = getrf(A)
    print(f"LU result:\n{lu}")
    print(f"Pivot indices: {piv}")
    print(f"Info: {info}")

if __name__ == "__main__":
    main()
```

### 2. BLAS Operations

```python
import numpy as np
from scipy import linalg

def main():
    # Access BLAS for optimized operations
    x = np.array([1, 2, 3], dtype=float)
    y = np.array([4, 5, 6], dtype=float)
    
    # Get BLAS dot product function
    ddot = linalg.get_blas_funcs('dot', (x, y))
    
    result = ddot(x, y)
    print(f"BLAS dot product: {result}")
    print(f"NumPy dot product: {np.dot(x, y)}")

if __name__ == "__main__":
    main()
```

## Recommendation

### 1. Use NumPy When

- Basic operations (det, inv, solve, eig)
- Minimizing dependencies
- Simple scripts

### 2. Use SciPy When

- Advanced decompositions (LU, Schur, Hessenberg)
- Matrix functions (expm, logm, sqrtm)
- Specialized solvers (triangular, banded)
- Maximum performance via LAPACK

### 3. General Advice

```python
# Recommended import pattern
import numpy as np
from scipy import linalg

# Use scipy.linalg as default for comprehensive functionality
```

---

## Exercises

**Exercise 1.**
Solve the upper triangular system $Ux = b$ where $U = \begin{pmatrix} 3 & 1 & 2 \\ 0 & 5 & 4 \\ 0 & 0 & 2 \end{pmatrix}$ and $b = (10, 13, 4)^T$ using `scipy.linalg.solve_triangular`. Verify the solution by comparing with `np.linalg.solve`. The specialized solver should give the same result but is more efficient for triangular systems.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        U = np.array([[3, 1, 2],
                       [0, 5, 4],
                       [0, 0, 2]], dtype=float)
        b = np.array([10, 13, 4], dtype=float)

        x_tri = linalg.solve_triangular(U, b)
        x_gen = np.linalg.solve(U, b)

        print(f"Triangular solver: {x_tri}")
        print(f"General solver:    {x_gen}")
        print(f"Match: {np.allclose(x_tri, x_gen)}")

---

**Exercise 2.**
Compare the eigenvalue computation of a $100 \times 100$ symmetric matrix using both `np.linalg.eigh` and `scipy.linalg.eigh` (use `np.random.seed(15)` to create $A + A^T$). Verify that both return the same eigenvalues (up to $10^{-10}$) and measure the execution time of each.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg
        import time

        np.random.seed(15)
        B = np.random.randn(100, 100)
        A = B + B.T

        start = time.perf_counter()
        vals_np = np.linalg.eigh(A)[0]
        time_np = time.perf_counter() - start

        start = time.perf_counter()
        vals_sp = linalg.eigh(A)[0]
        time_sp = time.perf_counter() - start

        diff = np.max(np.abs(vals_np - vals_sp))
        print(f"Max eigenvalue difference: {diff:.2e}")
        print(f"NumPy time:  {time_np:.4f} sec")
        print(f"SciPy time:  {time_sp:.4f} sec")

---

**Exercise 3.**
Demonstrate a function available only in SciPy: compute the matrix exponential `expm` and the Schur decomposition of a $4 \times 4$ random matrix (use `np.random.seed(20)`). Print the Schur form $T$ and verify that `expm(A)` can be computed as $Z \cdot \text{expm}(T) \cdot Z^H$.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        np.random.seed(20)
        A = np.random.randn(4, 4)

        # Schur decomposition (SciPy only)
        T, Z = linalg.schur(A, output='complex')
        print(f"Schur form T:\n{T.round(4)}")

        # Matrix exponential (SciPy only)
        exp_A_direct = linalg.expm(A)
        exp_A_schur = Z @ linalg.expm(T) @ Z.conj().T

        error = np.linalg.norm(exp_A_direct - exp_A_schur.real)
        print(f"\nexpm(A) via Schur matches direct: {error:.2e}")
