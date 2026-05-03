# Matrix Square Root

The matrix square root $X$ satisfies $X^2 = A$.

!!! tip "Mental Model"
    The matrix square root finds $X$ such that multiplying $X$ by itself recovers the original matrix $A$. Unlike the scalar case, a matrix can have multiple square roots (or none at all for certain singular matrices). SciPy computes the principal square root via the Schur decomposition, which is numerically stable and works even when eigenvalues are complex.

## linalg.sqrtm

### 1. Basic Usage

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 0],
                  [0, 9]])
    
    sqrt_A = linalg.sqrtm(A)
    
    print("A =")
    print(A)
    print()
    print("sqrt(A) =")
    print(sqrt_A)

if __name__ == "__main__":
    main()
```

### 2. Verify X² = A

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2],
                  [2, 3]])
    
    X = linalg.sqrtm(A)
    
    print("sqrt(A) =")
    print(X)
    print()
    print("sqrt(A) @ sqrt(A) =")
    print((X @ X).round(10))
    print()
    print("Original A =")
    print(A)

if __name__ == "__main__":
    main()
```

### 3. Non-Unique

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 0],
                  [0, 4]])
    
    # Principal square root
    X1 = linalg.sqrtm(A)
    
    # Another square root
    X2 = -X1  # (-X)² = X² = A
    
    print("Principal sqrt(A):")
    print(X1)
    print()
    print("Another sqrt(A):")
    print(X2)
    print()
    print("Both satisfy X² = A:")
    print(f"X1² = A: {np.allclose(X1 @ X1, A)}")
    print(f"X2² = A: {np.allclose(X2 @ X2, A)}")

if __name__ == "__main__":
    main()
```

## Properties

### 1. Positive Definite Input

```python
import numpy as np
from scipy import linalg

def main():
    # Positive definite -> real square root
    A = np.array([[4, 2],
                  [2, 5]])
    
    X = linalg.sqrtm(A)
    
    print("A is positive definite")
    print("sqrt(A) is real:")
    print(X.real.round(6))

if __name__ == "__main__":
    main()
```

### 2. Negative Eigenvalues

```python
import numpy as np
from scipy import linalg

def main():
    # Negative eigenvalues -> complex square root
    A = np.array([[-1, 0],
                  [0, 4]])
    
    X = linalg.sqrtm(A)
    
    print("A has negative eigenvalue:")
    print(A)
    print()
    print("sqrt(A) is complex:")
    print(X)

if __name__ == "__main__":
    main()
```

## Applications

### 1. Whitening Transform

```python
import numpy as np
from scipy import linalg

def main():
    np.random.seed(42)
    
    # Covariance matrix
    Sigma = np.array([[2, 1],
                      [1, 2]])
    
    # Whitening: W = Sigma^{-1/2}
    Sigma_sqrt = linalg.sqrtm(Sigma)
    W = np.linalg.inv(Sigma_sqrt)
    
    # Generate correlated data
    data = np.random.randn(1000, 2) @ linalg.sqrtm(Sigma)
    
    # Whiten
    whitened = data @ W
    
    print("Original covariance:")
    print(np.cov(data.T).round(2))
    print()
    print("Whitened covariance:")
    print(np.cov(whitened.T).round(2))

if __name__ == "__main__":
    main()
```

### 2. Geometric Mean

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 0],
                  [0, 9]])
    B = np.array([[1, 0],
                  [0, 4]])
    
    # Matrix geometric mean: A#B = A^{1/2} (A^{-1/2} B A^{-1/2})^{1/2} A^{1/2}
    A_sqrt = linalg.sqrtm(A)
    A_inv_sqrt = linalg.sqrtm(np.linalg.inv(A))
    
    inner = A_inv_sqrt @ B @ A_inv_sqrt
    geo_mean = A_sqrt @ linalg.sqrtm(inner) @ A_sqrt
    
    print("Geometric mean A#B:")
    print(geo_mean.real.round(6))

if __name__ == "__main__":
    main()
```

## Summary

| Function | Description |
|:---------|:------------|
| `linalg.sqrtm(A)` | Principal matrix square root |

Key: Returns principal square root. May be complex if A has negative eigenvalues.

---

## Exercises

**Exercise 1.**
Compute the matrix square root of $A = \begin{pmatrix} 5 & 2 \\ 2 & 8 \end{pmatrix}$ and verify that $X^2 = A$ by checking $\|X^2 - A\|_F < 10^{-12}$. Also verify that the square root is real (since $A$ is positive definite).

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        A = np.array([[5, 2],
                       [2, 8]], dtype=float)

        X = linalg.sqrtm(A)
        error = np.linalg.norm(X @ X - A)
        is_real = np.allclose(X.imag, 0) if np.iscomplexobj(X) else True

        print(f"sqrt(A) =\n{X.real.round(6)}")
        print(f"X^2 - A error: {error:.2e}")
        print(f"Result is real: {is_real}")

---

**Exercise 2.**
Implement the whitening transform for the covariance matrix $\Sigma = \begin{pmatrix} 4 & 2 \\ 2 & 3 \end{pmatrix}$. Compute $W = \Sigma^{-1/2}$ using `sqrtm` and `np.linalg.inv`. Generate 1000 correlated samples from $N(0, \Sigma)$, apply the whitening transform, and verify that the sample covariance of the whitened data is approximately the identity.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        np.random.seed(0)
        Sigma = np.array([[4, 2],
                           [2, 3]], dtype=float)

        Sigma_sqrt = linalg.sqrtm(Sigma)
        W = np.linalg.inv(Sigma_sqrt.real)

        # Generate correlated samples
        samples = np.random.randn(1000, 2) @ Sigma_sqrt.real

        # Whiten
        whitened = samples @ W
        cov_whitened = np.cov(whitened.T)

        print(f"Whitened covariance:\n{cov_whitened.round(2)}")
        print(f"Close to identity: {np.allclose(cov_whitened, np.eye(2), atol=0.15)}")

---

**Exercise 3.**
Compute the matrix geometric mean of $A = \begin{pmatrix} 4 & 1 \\ 1 & 3 \end{pmatrix}$ and $B = \begin{pmatrix} 2 & 0 \\ 0 & 5 \end{pmatrix}$ using the formula $A \# B = A^{1/2} (A^{-1/2} B A^{-1/2})^{1/2} A^{1/2}$. Verify that the result is symmetric and its eigenvalues lie between those of $A$ and $B$.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        A = np.array([[4, 1],
                       [1, 3]], dtype=float)
        B = np.array([[2, 0],
                       [0, 5]], dtype=float)

        A_sqrt = linalg.sqrtm(A).real
        A_inv_sqrt = linalg.sqrtm(np.linalg.inv(A)).real

        inner = A_inv_sqrt @ B @ A_inv_sqrt
        geo_mean = A_sqrt @ linalg.sqrtm(inner).real @ A_sqrt

        print(f"Geometric mean A#B:\n{geo_mean.round(6)}")
        print(f"Symmetric: {np.allclose(geo_mean, geo_mean.T)}")

        eig_geo = np.sort(np.linalg.eigvalsh(geo_mean))
        eig_A = np.sort(np.linalg.eigvalsh(A))
        eig_B = np.sort(np.linalg.eigvalsh(B))
        print(f"Eigenvalues of A: {eig_A}")
        print(f"Eigenvalues of A#B: {eig_geo.round(6)}")
        print(f"Eigenvalues of B: {eig_B}")
