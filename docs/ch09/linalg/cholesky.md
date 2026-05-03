# Cholesky Decomposition

Decompose positive definite matrices as $A = LL^T$.

!!! tip "Mental Model"
    Cholesky is a "square root" for positive definite matrices -- it splits $A$ into a lower-triangular matrix $L$ times its own transpose. It is roughly twice as fast as a general LU decomposition and serves as the workhorse for sampling multivariate normals, solving symmetric systems, and testing positive definiteness.

!!! note "Connection to Solving Systems"
    When $A$ is symmetric positive definite, Cholesky gives the fastest path to
    solving $Ax = b$: factor $A = LL^T$ once, then solve two triangular systems
    ($Ly = b$, then $L^T x = y$) via `scipy.linalg.cho_solve`. This is roughly 2x
    faster than the general `np.linalg.solve` (which uses LU) and exploits the
    structure that `solve` cannot assume. Covariance matrices in statistics and
    kernel matrices in ML are always SPD, making Cholesky the natural choice.

## np.linalg.cholesky

### 1. Basic Usage

```python
import numpy as np

def main():
    # Symmetric positive definite matrix
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    
    L = np.linalg.cholesky(A)
    
    print("A =")
    print(A)
    print()
    print("L (lower triangular) =")
    print(L.round(4))

if __name__ == "__main__":
    main()
```

### 2. Mathematical Form

$$A = LL^T$$

where $L$ is lower triangular.

### 3. Verify Result

```python
import numpy as np

def main():
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    
    L = np.linalg.cholesky(A)
    
    # Reconstruct
    A_reconstructed = L @ L.T
    
    print("Original A:")
    print(A)
    print()
    print("L @ L^T:")
    print(A_reconstructed.round(10))
    print()
    print(f"Match: {np.allclose(A, A_reconstructed)}")

if __name__ == "__main__":
    main()
```

## Requirements

### 1. Symmetric Matrix

```python
import numpy as np

def main():
    A = np.array([[4, 2],
                  [2, 3]])
    
    is_symmetric = np.allclose(A, A.T)
    print(f"A is symmetric: {is_symmetric}")
    
    L = np.linalg.cholesky(A)
    print(f"Cholesky succeeded: L =\n{L}")

if __name__ == "__main__":
    main()
```

### 2. Positive Definite

All eigenvalues must be positive.

```python
import numpy as np

def main():
    A = np.array([[4, 2],
                  [2, 3]])
    
    eigenvalues = np.linalg.eigvalsh(A)
    is_positive_definite = np.all(eigenvalues > 0)
    
    print(f"Eigenvalues: {eigenvalues}")
    print(f"Positive definite: {is_positive_definite}")

if __name__ == "__main__":
    main()
```

### 3. Error for Non-PD

```python
import numpy as np

def main():
    # Not positive definite (negative eigenvalue)
    A = np.array([[1, 2],
                  [2, 1]])
    
    print(f"Eigenvalues: {np.linalg.eigvalsh(A)}")
    
    try:
        L = np.linalg.cholesky(A)
    except np.linalg.LinAlgError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## Creating PD Matrices

### 1. From Random Matrix

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Random matrix
    B = np.random.randn(3, 3)
    
    # A = B @ B^T is positive semi-definite
    A = B @ B.T
    
    # Add small diagonal for strict positive definite
    A = A + 0.01 * np.eye(3)
    
    print("A =")
    print(A.round(3))
    print()
    print(f"Eigenvalues: {np.linalg.eigvalsh(A).round(4)}")
    
    L = np.linalg.cholesky(A)
    print("Cholesky succeeded!")

if __name__ == "__main__":
    main()
```

### 2. Covariance Matrix

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Sample data
    X = np.random.randn(100, 3)
    
    # Sample covariance (symmetric, typically PD)
    cov = np.cov(X.T)
    
    print("Covariance matrix:")
    print(cov.round(3))
    print()
    
    L = np.linalg.cholesky(cov)
    print("Cholesky factor:")
    print(L.round(3))

if __name__ == "__main__":
    main()
```

### 3. Regularization

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Nearly singular covariance
    X = np.random.randn(10, 5)
    cov = np.cov(X.T)
    
    # Add regularization
    reg = 1e-6
    cov_reg = cov + reg * np.eye(cov.shape[0])
    
    L = np.linalg.cholesky(cov_reg)
    print("Regularized Cholesky succeeded!")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Solving Linear Systems

Faster than general solve for PD matrices.

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    b = np.array([1, 2, 3])
    
    # Method 1: Standard solve
    x1 = np.linalg.solve(A, b)
    
    # Method 2: Cholesky-based solve
    L = np.linalg.cholesky(A)
    # Solve L @ y = b
    y = linalg.solve_triangular(L, b, lower=True)
    # Solve L^T @ x = y
    x2 = linalg.solve_triangular(L.T, y, lower=False)
    
    print(f"Standard solve: {x1}")
    print(f"Cholesky solve: {x2}")
    print(f"Match: {np.allclose(x1, x2)}")

if __name__ == "__main__":
    main()
```

### 2. Multivariate Normal

Generate correlated random samples.

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    np.random.seed(42)
    
    # Mean and covariance
    mean = np.array([0, 0])
    cov = np.array([[1, 0.8],
                    [0.8, 1]])
    
    # Cholesky factor
    L = np.linalg.cholesky(cov)
    
    # Generate samples: x = mean + L @ z
    n_samples = 1000
    z = np.random.randn(2, n_samples)
    samples = mean.reshape(-1, 1) + L @ z
    
    fig, ax = plt.subplots()
    ax.scatter(samples[0], samples[1], alpha=0.3, s=10)
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_title('Correlated Normal Samples via Cholesky')
    ax.set_aspect('equal')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Log Determinant

Numerically stable computation.

```python
import numpy as np

def main():
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    
    L = np.linalg.cholesky(A)
    
    # log|A| = 2 * sum(log(diag(L)))
    log_det_cholesky = 2 * np.sum(np.log(np.diag(L)))
    
    # Direct computation
    sign, log_det_direct = np.linalg.slogdet(A)
    
    print(f"Log det (Cholesky): {log_det_cholesky:.6f}")
    print(f"Log det (slogdet):  {log_det_direct:.6f}")

if __name__ == "__main__":
    main()
```

## scipy.linalg

### 1. Lower and Upper

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2],
                  [2, 3]])
    
    # Lower triangular (default)
    L = linalg.cholesky(A, lower=True)
    print("Lower Cholesky:")
    print(L)
    print()
    
    # Upper triangular
    U = linalg.cholesky(A, lower=False)
    print("Upper Cholesky:")
    print(U)
    print()
    
    # Verify: A = L @ L^T = U^T @ U
    print(f"L @ L^T matches A: {np.allclose(L @ L.T, A)}")
    print(f"U^T @ U matches A: {np.allclose(U.T @ U, A)}")

if __name__ == "__main__":
    main()
```

### 2. Cholesky Solve

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    b = np.array([1, 2, 3])
    
    # Direct Cholesky solve
    L = linalg.cholesky(A, lower=True)
    x = linalg.cho_solve((L, True), b)
    
    print(f"Solution: {x}")
    print(f"Verify A @ x = {A @ x}")

if __name__ == "__main__":
    main()
```

### 3. Check for PD

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2],
                  [2, 3]])
    
    try:
        L = linalg.cholesky(A, lower=True, check_finite=True)
        print("Matrix is positive definite")
    except linalg.LinAlgError:
        print("Matrix is NOT positive definite")

if __name__ == "__main__":
    main()
```

## Performance

### 1. Efficiency

Cholesky is ~2x faster than LU decomposition for PD matrices.

```python
import numpy as np
import time

def main():
    n = 1000
    
    # Create PD matrix
    B = np.random.randn(n, n)
    A = B @ B.T + np.eye(n)
    
    # Cholesky timing
    start = time.perf_counter()
    L = np.linalg.cholesky(A)
    cholesky_time = time.perf_counter() - start
    
    # General solve timing (uses LU)
    b = np.random.randn(n)
    start = time.perf_counter()
    x = np.linalg.solve(A, b)
    solve_time = time.perf_counter() - start
    
    print(f"Cholesky decomposition: {cholesky_time:.4f} sec")
    print(f"General solve: {solve_time:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Memory

Lower triangular storage uses half the memory.

### 3. Numerical Stability

Cholesky is numerically stable for PD matrices.

---

## Exercises

**Exercise 1.**
Create a 3x3 symmetric positive definite matrix by computing `A = B.T @ B + np.eye(3)` where `B = np.random.randn(3, 3)`. Compute the Cholesky decomposition `L` and verify that `L @ L.T` reconstructs `A` within floating-point tolerance.

??? success "Solution to Exercise 1"

        import numpy as np

        np.random.seed(42)
        B = np.random.randn(3, 3)
        A = B.T @ B + np.eye(3)
        L = np.linalg.cholesky(A)
        reconstructed = L @ L.T
        print(f"Match: {np.allclose(A, reconstructed)}")

---

**Exercise 2.**
Use Cholesky decomposition to solve the system `A @ x = b` where `A` is a symmetric positive definite matrix. First compute `L = np.linalg.cholesky(A)`, then solve `L @ y = b` followed by `L.T @ x = y` using `np.linalg.solve`. Verify the result matches `np.linalg.solve(A, b)`.

??? success "Solution to Exercise 2"

        import numpy as np

        A = np.array([[4, 2, 1], [2, 5, 2], [1, 2, 6]], dtype=float)
        b = np.array([1, 2, 3], dtype=float)

        L = np.linalg.cholesky(A)
        y = np.linalg.solve(L, b)
        x_chol = np.linalg.solve(L.T, y)

        x_direct = np.linalg.solve(A, b)
        print(f"Cholesky: {x_chol}")
        print(f"Direct:   {x_direct}")
        print(f"Match: {np.allclose(x_chol, x_direct)}")

---

**Exercise 3.**
Given a matrix that is symmetric but NOT positive definite (e.g., `A = np.array([[1, 2], [2, 1]])`), show that `np.linalg.cholesky` raises a `LinAlgError`. Catch the exception and print the error message. Then verify the matrix is not positive definite by checking that it has a negative eigenvalue.

??? success "Solution to Exercise 3"

        import numpy as np

        A = np.array([[1, 2], [2, 1]], dtype=float)
        try:
            L = np.linalg.cholesky(A)
        except np.linalg.LinAlgError as e:
            print(f"Error: {e}")

        eigvals = np.linalg.eigvalsh(A)
        print(f"Eigenvalues: {eigvals}")
        print(f"Has negative eigenvalue: {np.any(eigvals < 0)}")
