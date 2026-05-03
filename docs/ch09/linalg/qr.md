# QR Decomposition

Decompose a matrix into orthogonal and triangular components.

!!! tip "Mental Model"
    QR splits any matrix into an orthogonal matrix $Q$ (whose columns are perpendicular unit vectors) and an upper-triangular matrix $R$. This is the numerically stable way to solve least-squares problems: instead of forming the normal equations, factor $A = QR$ and back-substitute. It is also the foundation of the QR algorithm for eigenvalues.

    In the [factorization landscape](matrix_multiply.md), QR occupies the
    middle ground: more general than Cholesky (works on any matrix, not just SPD)
    but more structured than SVD (faster when you only need least squares, not
    rank analysis).

## np.linalg.qr

### 1. Basic Usage

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    Q, R = np.linalg.qr(A)
    
    print("A =")
    print(A)
    print()
    print("Q (orthogonal) =")
    print(Q.round(4))
    print()
    print("R (upper triangular) =")
    print(R.round(4))

if __name__ == "__main__":
    main()
```

### 2. Mathematical Form

$$A = QR$$

- $Q$: Orthogonal matrix ($Q^TQ = I$)
- $R$: Upper triangular matrix

### 3. Verify Result

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    Q, R = np.linalg.qr(A)
    
    # Q @ R should equal A
    A_reconstructed = Q @ R
    
    print("A =")
    print(A)
    print()
    print("Q @ R =")
    print(A_reconstructed.round(10))
    print()
    print(f"Match: {np.allclose(A, A_reconstructed)}")

if __name__ == "__main__":
    main()
```

## Properties

### 1. Q is Orthogonal

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    Q, R = np.linalg.qr(A)
    
    # Q^T @ Q should be identity
    QtQ = Q.T @ Q
    
    print("Q^T @ Q =")
    print(QtQ.round(10))
    print()
    print(f"Is identity: {np.allclose(QtQ, np.eye(QtQ.shape[0]))}")

if __name__ == "__main__":
    main()
```

### 2. R is Upper Triangular

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 10]])
    
    Q, R = np.linalg.qr(A)
    
    print("R =")
    print(R.round(4))
    print()
    
    # Check lower triangle is zero
    lower = np.tril(R, k=-1)
    print("Lower triangle (should be zeros):")
    print(lower.round(10))

if __name__ == "__main__":
    main()
```

### 3. Orthonormal Columns

```python
import numpy as np

def main():
    A = np.random.randn(5, 3)
    
    Q, R = np.linalg.qr(A)
    
    # Check column norms are 1
    col_norms = np.linalg.norm(Q, axis=0)
    print(f"Column norms: {col_norms}")
    
    # Check columns are orthogonal
    for i in range(Q.shape[1]):
        for j in range(i + 1, Q.shape[1]):
            dot = Q[:, i] @ Q[:, j]
            print(f"Q[:, {i}] · Q[:, {j}] = {dot:.10f}")

if __name__ == "__main__":
    main()
```

## Mode Options

### 1. Reduced QR (default)

```python
import numpy as np

def main():
    A = np.random.randn(5, 3)
    
    Q, R = np.linalg.qr(A, mode='reduced')
    
    print(f"A shape: {A.shape}")
    print(f"Q shape: {Q.shape}")
    print(f"R shape: {R.shape}")

if __name__ == "__main__":
    main()
```

### 2. Full QR

```python
import numpy as np

def main():
    A = np.random.randn(5, 3)
    
    Q, R = np.linalg.qr(A, mode='complete')
    
    print(f"A shape: {A.shape}")
    print(f"Q shape: {Q.shape}")  # Square
    print(f"R shape: {R.shape}")

if __name__ == "__main__":
    main()
```

### 3. R Only

```python
import numpy as np

def main():
    A = np.random.randn(5, 3)
    
    R = np.linalg.qr(A, mode='r')
    
    print(f"A shape: {A.shape}")
    print(f"R shape: {R.shape}")
    print()
    print("R =")
    print(R.round(4))

if __name__ == "__main__":
    main()
```

## Least Squares

### 1. QR Solution

```python
import numpy as np
from scipy import linalg

def main():
    # Overdetermined system
    A = np.array([[1, 1],
                  [1, 2],
                  [1, 3]])
    b = np.array([1, 2, 2])
    
    Q, R = np.linalg.qr(A)
    
    # Solve R @ x = Q^T @ b
    x = linalg.solve_triangular(R, Q.T @ b)
    
    print(f"Least squares solution: {x}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.4f}")

if __name__ == "__main__":
    main()
```

### 2. Compare with lstsq

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 1],
                  [1, 2],
                  [1, 3],
                  [1, 4]])
    b = np.array([1, 2.1, 2.9, 4.2])
    
    # QR method
    Q, R = np.linalg.qr(A)
    x_qr = linalg.solve_triangular(R, Q.T @ b)
    
    # lstsq method
    x_lstsq, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
    
    print(f"QR solution:    {x_qr}")
    print(f"lstsq solution: {x_lstsq}")
    print(f"Match: {np.allclose(x_qr, x_lstsq)}")

if __name__ == "__main__":
    main()
```

### 3. Why Use QR

- More numerically stable than normal equations
- Efficient for multiple right-hand sides

## Applications

### 1. Orthonormal Basis

```python
import numpy as np

def main():
    # Linearly independent vectors (as columns)
    A = np.array([[1, 1],
                  [1, 2],
                  [0, 1]])
    
    Q, R = np.linalg.qr(A)
    
    print("Original columns (not orthogonal):")
    print(A)
    print()
    print("Orthonormal basis for column space:")
    print(Q.round(4))

if __name__ == "__main__":
    main()
```

### 2. Projection Matrix

```python
import numpy as np

def main():
    # Subspace spanned by columns of A
    A = np.array([[1, 0],
                  [1, 1],
                  [0, 1]])
    
    Q, R = np.linalg.qr(A)
    
    # Projection matrix: P = Q @ Q^T
    P = Q @ Q.T
    
    print("Projection matrix:")
    print(P.round(4))
    print()
    
    # Project a vector
    v = np.array([1, 1, 1])
    v_proj = P @ v
    print(f"v = {v}")
    print(f"Projection of v: {v_proj.round(4)}")

if __name__ == "__main__":
    main()
```

### 3. Matrix Rank

```python
import numpy as np

def main():
    # Rank-deficient matrix
    A = np.array([[1, 2, 3],
                  [2, 4, 6],
                  [1, 1, 1]])
    
    Q, R = np.linalg.qr(A)
    
    # Rank = number of non-zero diagonal elements in R
    diag_R = np.abs(np.diag(R))
    rank_qr = np.sum(diag_R > 1e-10)
    
    print("R diagonal:", diag_R.round(4))
    print(f"Rank via QR: {rank_qr}")
    print(f"np.linalg.matrix_rank: {np.linalg.matrix_rank(A)}")

if __name__ == "__main__":
    main()
```

## scipy.linalg.qr

### 1. Pivoting

Column pivoting for better numerical stability.

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    # QR with column pivoting
    Q, R, P = linalg.qr(A, pivoting=True)
    
    print(f"Permutation: {P}")
    print()
    print("R diagonal:", np.diag(R).round(4))

if __name__ == "__main__":
    main()
```

### 2. Economic Mode

```python
import numpy as np
from scipy import linalg

def main():
    A = np.random.randn(100, 10)
    
    # Economic QR (like NumPy's reduced)
    Q, R = linalg.qr(A, mode='economic')
    
    print(f"A shape: {A.shape}")
    print(f"Q shape: {Q.shape}")
    print(f"R shape: {R.shape}")

if __name__ == "__main__":
    main()
```

### 3. Raw Mode

Returns Householder reflectors for advanced use.

## Best Practices

### 1. Use for Least Squares

QR is the recommended method for solving least squares problems.

### 2. Reduced by Default

Use reduced (economic) mode unless you need the full Q.

### 3. Pivoting for Rank

Use pivoted QR when rank determination is important.

---

## Exercises

**Exercise 1.**
Compute the QR decomposition of `A = np.array([[1, 2], [3, 4], [5, 6]])`. Verify that `Q @ R` reconstructs `A` and that `Q` has orthonormal columns (`Q.T @ Q` is the identity).

??? success "Solution to Exercise 1"

        import numpy as np

        A = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
        Q, R = np.linalg.qr(A)
        print(f"Q @ R matches A: {np.allclose(Q @ R, A)}")
        print(f"Q orthonormal: {np.allclose(Q.T @ Q, np.eye(2))}")

---

**Exercise 2.**
Use QR decomposition to solve the least squares problem `A @ x = b` where `A = np.array([[1, 1], [1, 2], [1, 3]])` and `b = np.array([1, 2, 2])`. Compute `Q, R = np.linalg.qr(A)` then solve `R @ x = Q.T @ b`. Compare with `np.linalg.lstsq`.

??? success "Solution to Exercise 2"

        import numpy as np

        A = np.array([[1, 1], [1, 2], [1, 3]], dtype=float)
        b = np.array([1, 2, 2], dtype=float)

        Q, R = np.linalg.qr(A)
        x_qr = np.linalg.solve(R, Q.T @ b)
        x_lstsq, _, _, _ = np.linalg.lstsq(A, b, rcond=None)

        print(f"QR solution:    {x_qr}")
        print(f"lstsq solution: {x_lstsq}")
        print(f"Match: {np.allclose(x_qr, x_lstsq)}")

---

**Exercise 3.**
Generate a random 5x3 matrix and compute its QR decomposition. Verify that `Q` has shape `(5, 3)` and `R` has shape `(3, 3)`. Check that `R` is upper triangular by verifying all elements below the diagonal are zero.

??? success "Solution to Exercise 3"

        import numpy as np

        A = np.random.randn(5, 3)
        Q, R = np.linalg.qr(A)
        print(f"Q shape: {Q.shape}")  # (5, 3)
        print(f"R shape: {R.shape}")  # (3, 3)

        # Check upper triangular
        is_upper = np.allclose(R, np.triu(R))
        print(f"R is upper triangular: {is_upper}")
