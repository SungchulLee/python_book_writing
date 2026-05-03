# Cholesky Decomposition

Cholesky decomposition factors symmetric positive definite matrices.

!!! tip "Mental Model"
    Think of Cholesky as taking the "square root" of a symmetric positive definite matrix: it finds a lower triangular $L$ such that $A = LL^T$. Because it exploits symmetry, Cholesky is roughly twice as fast as LU and is the go-to factorization whenever your matrix is symmetric positive definite.

## Basic Decomposition

### 1. linalg.cholesky

```python
import numpy as np
from scipy import linalg

def main():
    # Symmetric positive definite matrix
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    
    L = linalg.cholesky(A, lower=True)
    
    print("A =")
    print(A)
    print()
    print("L (lower Cholesky factor):")
    print(L)
    print()
    print("Verify L @ L.T:")
    print(L @ L.T)

if __name__ == "__main__":
    main()
```

### 2. Mathematical Form

$$A = LL^T$$

where $L$ is lower triangular with positive diagonal entries.

### 3. Upper Form

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    
    # Upper triangular form: A = U.T @ U
    U = linalg.cholesky(A, lower=False)
    
    print("U (upper Cholesky factor):")
    print(U)
    print()
    print("Verify U.T @ U:")
    print(U.T @ U)

if __name__ == "__main__":
    main()
```

## Requirements

### 1. Symmetric Positive Definite

```python
import numpy as np
from scipy import linalg

def main():
    # Check if matrix is SPD
    A = np.array([[4, 2],
                  [2, 3]])
    
    # Method 1: Check eigenvalues
    eigvals = np.linalg.eigvalsh(A)
    print(f"Eigenvalues: {eigvals}")
    print(f"All positive: {np.all(eigvals > 0)}")
    print()
    
    # Method 2: Try Cholesky (fails if not SPD)
    try:
        L = linalg.cholesky(A, lower=True)
        print("Cholesky succeeded - matrix is SPD")
    except linalg.LinAlgError:
        print("Cholesky failed - matrix is not SPD")

if __name__ == "__main__":
    main()
```

### 2. Non-SPD Matrix

```python
import numpy as np
from scipy import linalg

def main():
    # Not positive definite
    A = np.array([[1, 2],
                  [2, 1]])  # Has negative eigenvalue
    
    print(f"Eigenvalues: {np.linalg.eigvalsh(A)}")
    
    try:
        L = linalg.cholesky(A, lower=True)
    except linalg.LinAlgError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### 3. Creating SPD Matrices

```python
import numpy as np
from scipy import linalg

def main():
    # Method 1: A @ A.T is always SPD (if A has full row rank)
    B = np.random.randn(3, 5)
    A1 = B @ B.T
    
    # Method 2: Covariance matrix
    data = np.random.randn(100, 3)
    A2 = np.cov(data.T)
    
    # Method 3: Add to diagonal for numerical stability
    C = np.random.randn(3, 3)
    A3 = C @ C.T + 0.1 * np.eye(3)
    
    # All should work
    for i, A in enumerate([A1, A2, A3], 1):
        L = linalg.cholesky(A, lower=True)
        print(f"Matrix {i}: Cholesky succeeded")

if __name__ == "__main__":
    main()
```

## Solving Linear Systems

### 1. cho_factor and cho_solve

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    b = np.array([7, 9, 9])
    
    # Factor
    c, low = linalg.cho_factor(A)
    
    # Solve
    x = linalg.cho_solve((c, low), b)
    
    print(f"Solution: x = {x}")
    print(f"Verify A @ x = {A @ x}")

if __name__ == "__main__":
    main()
```

### 2. Multiple Solves

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2],
                  [2, 3]])
    
    # Factor once
    c, low = linalg.cho_factor(A)
    
    # Solve multiple systems
    for b in [[6, 5], [4, 3], [2, 1]]:
        b = np.array(b)
        x = linalg.cho_solve((c, low), b)
        print(f"b = {b} -> x = {x}")

if __name__ == "__main__":
    main()
```

### 3. vs LU Performance

```python
import numpy as np
from scipy import linalg
import time

def main():
    n = 1000
    A = np.random.randn(n, n)
    A = A @ A.T + n * np.eye(n)  # SPD
    b = np.random.randn(n)
    
    # LU solve
    start = time.perf_counter()
    lu, piv = linalg.lu_factor(A)
    x1 = linalg.lu_solve((lu, piv), b)
    lu_time = time.perf_counter() - start
    
    # Cholesky solve
    start = time.perf_counter()
    c, low = linalg.cho_factor(A)
    x2 = linalg.cho_solve((c, low), b)
    cho_time = time.perf_counter() - start
    
    print(f"LU time:       {lu_time:.4f} sec")
    print(f"Cholesky time: {cho_time:.4f} sec")
    print(f"Speedup:       {lu_time/cho_time:.2f}x")

if __name__ == "__main__":
    main()
```

## Determinant and Log-Determinant

### 1. Determinant via Cholesky

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    
    L = linalg.cholesky(A, lower=True)
    
    # det(A) = det(L)^2 = (prod of diagonal)^2
    det_L = np.prod(np.diag(L))
    det_A = det_L ** 2
    
    print(f"det(A) via Cholesky: {det_A}")
    print(f"det(A) direct:       {np.linalg.det(A)}")

if __name__ == "__main__":
    main()
```

### 2. Log-Determinant (Numerically Stable)

```python
import numpy as np
from scipy import linalg

def main():
    # Large SPD matrix
    n = 100
    A = np.random.randn(n, n)
    A = A @ A.T + n * np.eye(n)
    
    L = linalg.cholesky(A, lower=True)
    
    # log|A| = 2 * sum(log(diag(L)))
    log_det = 2 * np.sum(np.log(np.diag(L)))
    
    print(f"log|A| via Cholesky: {log_det:.4f}")
    print(f"log|A| via slogdet:  {np.linalg.slogdet(A)[1]:.4f}")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Multivariate Normal Sampling

```python
import numpy as np
from scipy import linalg

def main():
    # Sample from N(mu, Sigma)
    mu = np.array([1, 2])
    Sigma = np.array([[1.0, 0.5],
                      [0.5, 1.0]])
    
    L = linalg.cholesky(Sigma, lower=True)
    
    # Generate samples: x = mu + L @ z, where z ~ N(0, I)
    n_samples = 1000
    z = np.random.randn(n_samples, 2)
    samples = mu + z @ L.T
    
    print(f"Sample mean: {samples.mean(axis=0)}")
    print(f"Sample cov:\n{np.cov(samples.T)}")

if __name__ == "__main__":
    main()
```

### 2. Gaussian Process Regression

```python
import numpy as np
from scipy import linalg

def main():
    # Kernel matrix (must be SPD)
    X = np.linspace(0, 1, 10).reshape(-1, 1)
    K = np.exp(-0.5 * ((X - X.T) ** 2) / 0.1)
    K += 1e-6 * np.eye(len(X))  # Numerical stability
    
    y = np.sin(2 * np.pi * X.flatten()) + 0.1 * np.random.randn(10)
    
    # Solve K @ alpha = y using Cholesky
    L = linalg.cholesky(K, lower=True)
    alpha = linalg.cho_solve((L, True), y)
    
    print(f"Coefficients: {alpha[:5]}...")

if __name__ == "__main__":
    main()
```

### 3. Portfolio Optimization

```python
import numpy as np
from scipy import linalg

def main():
    # Covariance matrix of returns
    Sigma = np.array([[0.04, 0.01, 0.02],
                      [0.01, 0.09, 0.03],
                      [0.02, 0.03, 0.16]])
    
    # Check it's valid covariance (SPD)
    L = linalg.cholesky(Sigma, lower=True)
    print("Valid covariance matrix")
    print()
    
    # Simulate correlated returns
    n_days = 252
    z = np.random.randn(n_days, 3)
    returns = z @ L.T
    
    print(f"Simulated correlation:\n{np.corrcoef(returns.T).round(2)}")

if __name__ == "__main__":
    main()
```

## Summary

### 1. Functions

| Function | Description |
|:---------|:------------|
| `linalg.cholesky(A, lower=True)` | Compute L where A = LL^T |
| `linalg.cho_factor(A)` | Factor for solving |
| `linalg.cho_solve((c, low), b)` | Solve using factorization |

### 2. Key Properties

- Requires symmetric positive definite matrix
- About 2x faster than LU for SPD matrices
- Numerically stable for SPD systems
- Half the storage of LU (only L needed)

---

## Exercises

**Exercise 1.**
Generate a random $5 \times 5$ symmetric positive definite matrix by creating a random matrix $B$ with `np.random.seed(42)` and computing $A = B^T B + 5I$. Perform Cholesky decomposition to obtain $L$, then verify that $\|A - LL^T\|_F < 10^{-12}$ using `np.linalg.norm`.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        np.random.seed(42)
        B = np.random.randn(5, 5)
        A = B.T @ B + 5 * np.eye(5)

        L = linalg.cholesky(A, lower=True)
        error = np.linalg.norm(A - L @ L.T)
        print(f"Reconstruction error: {error:.2e}")
        assert error < 1e-12, "Reconstruction error too large"

---

**Exercise 2.**
Using `cho_factor` and `cho_solve`, solve the system $Ax = b$ for $A = \begin{pmatrix} 10 & 3 & 1 \\ 3 & 8 & 2 \\ 1 & 2 & 6 \end{pmatrix}$ and three different right-hand sides $b_1 = (1, 0, 0)^T$, $b_2 = (0, 1, 0)^T$, $b_3 = (0, 0, 1)^T$. Stack the three solutions as columns and verify that the result approximates $A^{-1}$.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        A = np.array([[10, 3, 1],
                       [3, 8, 2],
                       [1, 2, 6]])
        c, low = linalg.cho_factor(A)

        solutions = []
        for b in [np.array([1, 0, 0]), np.array([0, 1, 0]), np.array([0, 0, 1])]:
            x = linalg.cho_solve((c, low), b)
            solutions.append(x)

        A_inv_cholesky = np.column_stack(solutions)
        A_inv_direct = np.linalg.inv(A)
        print("A^{-1} via Cholesky solves:")
        print(A_inv_cholesky)
        print(f"Match: {np.allclose(A_inv_cholesky, A_inv_direct)}")

---

**Exercise 3.**
Create a $200 \times 200$ SPD matrix and compute its log-determinant using both the Cholesky-based formula $\log|A| = 2\sum_i \log L_{ii}$ and `np.linalg.slogdet`. Print the absolute difference between the two results and confirm it is below $10^{-8}$.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        np.random.seed(0)
        n = 200
        B = np.random.randn(n, n)
        A = B @ B.T + n * np.eye(n)

        L = linalg.cholesky(A, lower=True)
        log_det_chol = 2 * np.sum(np.log(np.diag(L)))

        sign, log_det_np = np.linalg.slogdet(A)
        diff = abs(log_det_chol - log_det_np)
        print(f"Cholesky log-det: {log_det_chol:.6f}")
        print(f"slogdet log-det:  {log_det_np:.6f}")
        print(f"Difference:       {diff:.2e}")
        assert diff < 1e-8
