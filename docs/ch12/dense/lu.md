# LU Decomposition

LU decomposition factors a matrix into lower and upper triangular matrices.

!!! tip "Mental Model"
    LU decomposition is Gaussian elimination captured in matrix form: factor $A = PLU$ once, then solve $Ax = b$ cheaply for any right-hand side by forward and back substitution. The upfront factorization cost pays for itself whenever you need to solve the same system with multiple different $b$ vectors.

## Basic LU Factorization

### 1. linalg.lu

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1, 1],
                  [4, 3, 3],
                  [8, 7, 9]])
    
    P, L, U = linalg.lu(A)
    
    print("P (permutation matrix):")
    print(P)
    print()
    print("L (lower triangular):")
    print(L)
    print()
    print("U (upper triangular):")
    print(U)
    print()
    print("Verify P @ L @ U:")
    print(P @ L @ U)

if __name__ == "__main__":
    main()
```

### 2. Mathematical Form

$$A = PLU$$

where:

- $P$ is a permutation matrix
- $L$ is lower triangular with ones on diagonal
- $U$ is upper triangular

### 3. Permutation Purpose

```python
import numpy as np
from scipy import linalg

def main():
    # Without permutation, LU can fail or be unstable
    A = np.array([[0, 1],
                  [1, 1]])
    
    P, L, U = linalg.lu(A)
    
    print("A has zero on diagonal:")
    print(A)
    print()
    print("P swaps rows:")
    print(P)
    print()
    print("Result: P @ L @ U =")
    print(P @ L @ U)

if __name__ == "__main__":
    main()
```

## LU Factor for Solving

### 1. linalg.lu_factor

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1, 1],
                  [4, 3, 3],
                  [8, 7, 9]])
    b = np.array([4, 10, 24])
    
    # Factor once
    lu, piv = linalg.lu_factor(A)
    
    # Solve using factorization
    x = linalg.lu_solve((lu, piv), b)
    
    print(f"Solution: x = {x}")
    print(f"Verify A @ x = {A @ x}")

if __name__ == "__main__":
    main()
```

### 2. Multiple Right-Hand Sides

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1],
                  [1, 3]])
    
    # Factor once
    lu, piv = linalg.lu_factor(A)
    
    # Solve for multiple b vectors
    b1 = np.array([3, 4])
    b2 = np.array([1, 2])
    b3 = np.array([5, 5])
    
    x1 = linalg.lu_solve((lu, piv), b1)
    x2 = linalg.lu_solve((lu, piv), b2)
    x3 = linalg.lu_solve((lu, piv), b3)
    
    print(f"x1 = {x1}")
    print(f"x2 = {x2}")
    print(f"x3 = {x3}")

if __name__ == "__main__":
    main()
```

### 3. Performance Benefit

```python
import numpy as np
from scipy import linalg
import time

def main():
    n = 1000
    A = np.random.randn(n, n)
    
    # Multiple solves without factorization
    start = time.perf_counter()
    for _ in range(10):
        b = np.random.randn(n)
        x = linalg.solve(A, b)
    no_factor_time = time.perf_counter() - start
    
    # Factor once, solve multiple times
    start = time.perf_counter()
    lu, piv = linalg.lu_factor(A)
    for _ in range(10):
        b = np.random.randn(n)
        x = linalg.lu_solve((lu, piv), b)
    factor_time = time.perf_counter() - start
    
    print(f"Without pre-factoring: {no_factor_time:.4f} sec")
    print(f"With pre-factoring:    {factor_time:.4f} sec")

if __name__ == "__main__":
    main()
```

## Packed Format

### 1. Understanding lu_factor Output

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1, 1],
                  [4, 3, 3],
                  [8, 7, 9]])
    
    # lu_factor returns packed format
    lu, piv = linalg.lu_factor(A)
    
    print("Packed LU matrix:")
    print(lu)
    print()
    print("Pivot indices:")
    print(piv)
    print()
    
    # Compare with full decomposition
    P, L, U = linalg.lu(A)
    print("L from full decomposition:")
    print(L)
    print()
    print("U from full decomposition:")
    print(U)

if __name__ == "__main__":
    main()
```

### 2. Extract L and U

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1, 1],
                  [4, 3, 3],
                  [8, 7, 9]])
    
    lu, piv = linalg.lu_factor(A)
    
    # Extract L (lower part + unit diagonal)
    L = np.tril(lu, k=-1) + np.eye(len(A))
    
    # Extract U (upper part including diagonal)
    U = np.triu(lu)
    
    print("Extracted L:")
    print(L)
    print()
    print("Extracted U:")
    print(U)

if __name__ == "__main__":
    main()
```

## Determinant via LU

### 1. Compute Determinant

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1, 1],
                  [4, 3, 3],
                  [8, 7, 9]])
    
    # Determinant = product of U diagonal * sign from permutation
    P, L, U = linalg.lu(A)
    
    det_U = np.prod(np.diag(U))
    det_P = np.linalg.det(P)  # +1 or -1
    
    det_A = det_P * det_U
    
    print(f"det(A) via LU: {det_A}")
    print(f"det(A) direct: {np.linalg.det(A)}")

if __name__ == "__main__":
    main()
```

### 2. Why This Works

$$\det(A) = \det(P)\det(L)\det(U) = \det(P) \cdot 1 \cdot \prod_{i} U_{ii}$$

## Inverse via LU

### 1. Compute Inverse

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1],
                  [1, 3]])
    
    # Factor
    lu, piv = linalg.lu_factor(A)
    
    # Solve A @ X = I for inverse
    I = np.eye(len(A))
    A_inv = linalg.lu_solve((lu, piv), I)
    
    print("A inverse via LU:")
    print(A_inv)
    print()
    print("Verify A @ A_inv:")
    print(A @ A_inv)

if __name__ == "__main__":
    main()
```

## Applications

### 1. System of Equations

```python
import numpy as np
from scipy import linalg

def main():
    # Economic model: supply-demand equilibrium
    # 2p1 + p2 = 10
    # p1 + 3p2 = 15
    
    A = np.array([[2, 1],
                  [1, 3]])
    b = np.array([10, 15])
    
    lu, piv = linalg.lu_factor(A)
    prices = linalg.lu_solve((lu, piv), b)
    
    print(f"Equilibrium prices: {prices}")

if __name__ == "__main__":
    main()
```

### 2. Circuit Analysis

```python
import numpy as np
from scipy import linalg

def main():
    # Kirchhoff's laws
    R = np.array([[10, -5, 0],
                  [-5, 15, -10],
                  [0, -10, 20]])
    V = np.array([10, 0, 0])
    
    lu, piv = linalg.lu_factor(R)
    currents = linalg.lu_solve((lu, piv), V)
    
    print(f"Branch currents: {currents}")

if __name__ == "__main__":
    main()
```

## Summary

### 1. Functions

| Function | Description |
|:---------|:------------|
| `linalg.lu(A)` | Full P, L, U matrices |
| `linalg.lu_factor(A)` | Packed format for solving |
| `linalg.lu_solve((lu, piv), b)` | Solve using factorization |

### 2. Complexity

- Factorization: $O(n^3)$
- Each solve: $O(n^2)$
- Pre-factor when solving multiple systems with same $A$

---

## Exercises

**Exercise 1.**
Use `linalg.lu` to decompose the matrix $A = \begin{pmatrix} 0 & 2 & 1 \\ 1 & 1 & 0 \\ 2 & 0 & 3 \end{pmatrix}$ into $P$, $L$, $U$. Verify the decomposition by checking that $\|PLU - A\|_F < 10^{-12}$. Also confirm that $L$ has ones on the diagonal and $U$ is upper triangular.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        A = np.array([[0, 2, 1],
                       [1, 1, 0],
                       [2, 0, 3]])
        P, L, U = linalg.lu(A)

        recon_error = np.linalg.norm(P @ L @ U - A)
        print(f"Reconstruction error: {recon_error:.2e}")
        print(f"L diagonal all ones: {np.allclose(np.diag(L), 1)}")
        print(f"U is upper triangular: {np.allclose(U, np.triu(U))}")

---

**Exercise 2.**
Factor a random $100 \times 100$ matrix (using `np.random.seed(5)`) with `lu_factor`, then solve the system $Ax = b$ for 20 different random right-hand sides using `lu_solve`. Measure and print the total time for the 20 solves. Then repeat without pre-factoring (calling `linalg.solve` each time) and compare the total times.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg
        import time

        np.random.seed(5)
        n = 100
        A = np.random.randn(n, n)

        # With pre-factoring
        start = time.perf_counter()
        lu, piv = linalg.lu_factor(A)
        for _ in range(20):
            b = np.random.randn(n)
            x = linalg.lu_solve((lu, piv), b)
        time_prefactor = time.perf_counter() - start

        # Without pre-factoring
        start = time.perf_counter()
        for _ in range(20):
            b = np.random.randn(n)
            x = linalg.solve(A, b)
        time_nofactor = time.perf_counter() - start

        print(f"With pre-factoring:    {time_prefactor:.4f} sec")
        print(f"Without pre-factoring: {time_nofactor:.4f} sec")

---

**Exercise 3.**
Compute the determinant of $A = \begin{pmatrix} 3 & 1 & 4 \\ 1 & 5 & 9 \\ 2 & 6 & 5 \end{pmatrix}$ using the LU decomposition: $\det(A) = \det(P) \cdot \prod_i U_{ii}$. Compare with `np.linalg.det(A)` and verify they agree to within $10^{-10}$.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        A = np.array([[3, 1, 4],
                       [1, 5, 9],
                       [2, 6, 5]])
        P, L, U = linalg.lu(A)

        det_P = np.linalg.det(P)
        det_U = np.prod(np.diag(U))
        det_lu = det_P * det_U

        det_direct = np.linalg.det(A)
        print(f"det(A) via LU:     {det_lu:.10f}")
        print(f"det(A) via np:     {det_direct:.10f}")
        print(f"Difference:        {abs(det_lu - det_direct):.2e}")
        assert abs(det_lu - det_direct) < 1e-10
