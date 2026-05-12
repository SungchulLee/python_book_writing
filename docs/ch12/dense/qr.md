# QR Decomposition

QR decomposition factors a matrix into orthogonal and upper triangular components.

!!! tip "Mental Model"
    QR decomposition is the matrix version of Gram-Schmidt orthogonalization: it factors $A = QR$ where $Q$ has orthonormal columns and $R$ is upper triangular. Because orthogonal transformations preserve lengths and angles, QR is numerically more stable than LU for least-squares problems and is the backbone of modern eigenvalue algorithms.

## Basic Decomposition

### 1. linalg.qr

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    Q, R = linalg.qr(A)
    
    print("A =")
    print(A)
    print()
    print("Q (orthogonal):")
    print(Q)
    print()
    print("R (upper triangular):")
    print(R)
    print()
    print("Verify Q @ R:")
    print(Q @ R)

if __name__ == "__main__":
    main()
```

### 2. Mathematical Form

$$A = QR$$

where:

- $Q$ is orthogonal ($Q^TQ = I$)
- $R$ is upper triangular

### 3. Orthogonality Check

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    Q, R = linalg.qr(A)
    
    print("Q.T @ Q (should be identity):")
    print((Q.T @ Q).round(10))

if __name__ == "__main__":
    main()
```

## Mode Options

### 1. Full vs Reduced

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])  # 3x2
    
    # Full QR (default)
    Q_full, R_full = linalg.qr(A, mode='full')
    print(f"Full: Q shape {Q_full.shape}, R shape {R_full.shape}")
    
    # Economic/reduced QR
    Q_econ, R_econ = linalg.qr(A, mode='economic')
    print(f"Economic: Q shape {Q_econ.shape}, R shape {R_econ.shape}")

if __name__ == "__main__":
    main()
```

### 2. R Only

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    # Only compute R (faster)
    R = linalg.qr(A, mode='r')
    
    print("R only:")
    print(R)

if __name__ == "__main__":
    main()
```

### 3. Pivoting

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    # QR with column pivoting: A @ P = Q @ R
    Q, R, P = linalg.qr(A, pivoting=True)
    
    print("Permutation P:")
    print(P)
    print()
    print("R (reveals rank):")
    print(R.round(10))

if __name__ == "__main__":
    main()
```

## Solving Least Squares

### 1. QR for Overdetermined Systems

```python
import numpy as np
from scipy import linalg

def main():
    # Overdetermined: more equations than unknowns
    A = np.array([[1, 1],
                  [1, 2],
                  [1, 3]])
    b = np.array([1, 2, 2])
    
    Q, R = linalg.qr(A, mode='economic')
    
    # Solve R @ x = Q.T @ b
    x = linalg.solve_triangular(R, Q.T @ b)
    
    print(f"Least squares solution: x = {x}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.4f}")

if __name__ == "__main__":
    main()
```

### 2. Comparison with lstsq

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 1],
                  [1, 2],
                  [1, 3],
                  [1, 4]])
    b = np.array([1, 2, 2, 3])
    
    # Method 1: QR
    Q, R = linalg.qr(A, mode='economic')
    x_qr = linalg.solve_triangular(R, Q.T @ b)
    
    # Method 2: lstsq
    x_lstsq, *_ = np.linalg.lstsq(A, b, rcond=None)
    
    print(f"QR solution:    {x_qr}")
    print(f"lstsq solution: {x_lstsq}")

if __name__ == "__main__":
    main()
```

## Gram-Schmidt Connection

### 1. QR as Orthonormalization

```python
import numpy as np
from scipy import linalg

def main():
    # Columns of A
    A = np.array([[1, 1],
                  [1, 0],
                  [0, 1]])
    
    Q, R = linalg.qr(A, mode='economic')
    
    print("Original columns (A):")
    print(A)
    print()
    print("Orthonormal columns (Q):")
    print(Q)
    print()
    print("Column norms:")
    for i in range(Q.shape[1]):
        print(f"  ||q{i+1}|| = {np.linalg.norm(Q[:, i]):.4f}")
    print()
    print("Dot product q1 · q2:", np.dot(Q[:, 0], Q[:, 1]).round(10))

if __name__ == "__main__":
    main()
```

### 2. R Contains Projections

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[3, 1],
                  [4, 0],
                  [0, 2]])
    
    Q, R = linalg.qr(A, mode='economic')
    
    print("R diagonal = column norms of original (after orthogonalization):")
    print(f"R[0,0] = {R[0,0]:.4f}")
    print(f"R[1,1] = {R[1,1]:.4f}")

if __name__ == "__main__":
    main()
```

## Matrix Rank

### 1. Rank from QR

```python
import numpy as np
from scipy import linalg

def main():
    # Rank-deficient matrix
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])  # Rank 2
    
    Q, R, P = linalg.qr(A, pivoting=True)
    
    print("R diagonal:")
    print(np.diag(R))
    print()
    
    # Count non-negligible diagonal entries
    tol = 1e-10
    rank = np.sum(np.abs(np.diag(R)) > tol)
    print(f"Numerical rank: {rank}")

if __name__ == "__main__":
    main()
```

### 2. Rank Estimation

```python
import numpy as np
from scipy import linalg

def main():
    # Create rank-3 matrix of size 5x4
    np.random.seed(42)
    U = np.random.randn(5, 3)
    V = np.random.randn(3, 4)
    A = U @ V  # Rank at most 3
    
    Q, R, P = linalg.qr(A, pivoting=True)
    
    print("R diagonal (magnitude indicates rank):")
    print(np.abs(np.diag(R)))

if __name__ == "__main__":
    main()
```

## Applications

### 1. Linear Regression

```python
import numpy as np
from scipy import linalg

def main():
    # Data
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([1, 2.1, 2.9, 4.2, 4.8])
    
    # Design matrix
    A = np.column_stack([np.ones_like(x), x])
    
    # QR solve
    Q, R = linalg.qr(A, mode='economic')
    coeffs = linalg.solve_triangular(R, Q.T @ y)
    
    intercept, slope = coeffs
    print(f"y = {slope:.3f}x + {intercept:.3f}")

if __name__ == "__main__":
    main()
```

### 2. Orthonormal Basis

```python
import numpy as np
from scipy import linalg

def main():
    # Find orthonormal basis for column space
    A = np.array([[1, 2, 3],
                  [1, 0, 1],
                  [0, 1, 1],
                  [1, 1, 2]])
    
    Q, R = linalg.qr(A, mode='economic')
    
    print("Orthonormal basis for column space of A:")
    print(Q)

if __name__ == "__main__":
    main()
```

### 3. QR Iteration (Eigenvalues)

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 1, 0],
                  [1, 3, 1],
                  [0, 1, 2]])
    
    # Simple QR iteration
    Ak = A.copy()
    for _ in range(30):
        Q, R = linalg.qr(Ak)
        Ak = R @ Q
    
    print("Eigenvalues (QR iteration):")
    print(np.diag(Ak))
    print()
    print("Eigenvalues (direct):")
    print(np.sort(np.linalg.eigvalsh(A))[::-1])

if __name__ == "__main__":
    main()
```

## Summary

### 1. Functions

| Function | Description |
|:---------|:------------|
| `linalg.qr(A)` | Full QR decomposition |
| `linalg.qr(A, mode='economic')` | Reduced QR |
| `linalg.qr(A, mode='r')` | R only |
| `linalg.qr(A, pivoting=True)` | With column pivoting |

### 2. Key Properties

- $Q^TQ = I$ (orthogonal)
- $R$ is upper triangular
- Numerically stable for least squares
- Column pivoting reveals rank

---

## Exercises

**Exercise 1.**
Generate a random $8 \times 4$ matrix with `np.random.seed(3)`. Compute its economic QR decomposition, then verify that $Q^TQ = I_4$ (up to tolerance $10^{-12}$) and that $\|QR - A\|_F < 10^{-12}$.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        np.random.seed(3)
        A = np.random.randn(8, 4)

        Q, R = linalg.qr(A, mode='economic')

        orth_error = np.linalg.norm(Q.T @ Q - np.eye(4))
        recon_error = np.linalg.norm(Q @ R - A)
        print(f"Q shape: {Q.shape}, R shape: {R.shape}")
        print(f"Orthogonality error: {orth_error:.2e}")
        print(f"Reconstruction error: {recon_error:.2e}")

---

**Exercise 2.**
Fit a degree-3 polynomial $y = c_0 + c_1 x + c_2 x^2 + c_3 x^3$ to the data points $x = [0, 1, 2, 3, 4, 5]$, $y = [1.0, 2.7, 5.8, 6.6, 7.5, 9.9]$ using QR decomposition. Build the Vandermonde design matrix, solve via `linalg.qr` (economic) and `linalg.solve_triangular`, and print the four coefficients.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        x = np.array([0, 1, 2, 3, 4, 5], dtype=float)
        y = np.array([1.0, 2.7, 5.8, 6.6, 7.5, 9.9])

        # Vandermonde design matrix
        A = np.column_stack([x**k for k in range(4)])

        Q, R = linalg.qr(A, mode='economic')
        coeffs = linalg.solve_triangular(R, Q.T @ y)

        print("Polynomial coefficients (c0, c1, c2, c3):")
        print(coeffs)

---

**Exercise 3.**
Create a $6 \times 6$ rank-4 matrix by computing `A = U @ V` where $U$ is $6 \times 4$ and $V$ is $4 \times 6$ (use `np.random.seed(1)`). Use QR decomposition with column pivoting to estimate the rank of $A$. Print the diagonal of $R$ and the estimated rank (count of diagonal entries with absolute value above $10^{-10}$).

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        np.random.seed(1)
        U = np.random.randn(6, 4)
        V = np.random.randn(4, 6)
        A = U @ V  # rank at most 4

        Q, R, P = linalg.qr(A, pivoting=True)

        diag_R = np.abs(np.diag(R))
        rank = np.sum(diag_R > 1e-10)
        print(f"Diagonal of R: {diag_R}")
        print(f"Estimated rank: {rank}")
