# Determinant and Inverse

Compute matrix determinants and inverses using `np.linalg`.

!!! tip "Mental Model"
    The determinant measures how a matrix scales volume -- zero means the matrix is singular and has no inverse. `np.linalg.inv` computes the inverse, but in practice you should almost always use `np.linalg.solve` instead, because solving a system directly is faster and more numerically stable than inverting first and multiplying.

    The sharper insight: $\det(A) = 0$ means **information collapse** — the
    transformation $A$ maps some directions to zero, making it impossible to
    recover the original input. A near-zero determinant (ill-conditioned matrix)
    means the collapse is almost happening, and numerical results become unreliable.

## np.linalg.det

### 1. Basic Usage

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    det = np.linalg.det(A)
    
    print("A =")
    print(A)
    print(f"det(A) = {det}")

if __name__ == "__main__":
    main()
```

**Output:**

```
A =
[[1 2]
 [3 4]]
det(A) = -2.0
```

### 2. Mathematical Form

For 2×2 matrix:

$$\det\begin{pmatrix} a & b \\ c & d \end{pmatrix} = ad - bc$$

```python
import numpy as np

def main():
    a, b, c, d = 1, 2, 3, 4
    A = np.array([[a, b],
                  [c, d]])
    
    det_numpy = np.linalg.det(A)
    det_manual = a * d - b * c
    
    print(f"NumPy det:  {det_numpy}")
    print(f"Manual det: {det_manual}")

if __name__ == "__main__":
    main()
```

### 3. Larger Matrices

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 10]])
    
    det = np.linalg.det(A)
    
    print("A =")
    print(A)
    print(f"det(A) = {det:.4f}")

if __name__ == "__main__":
    main()
```

## Singular Matrices

### 1. Zero Determinant

```python
import numpy as np

def main():
    # Singular matrix (rows are linearly dependent)
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    det = np.linalg.det(A)
    
    print("A =")
    print(A)
    print(f"det(A) = {det:.2e}")  # Essentially zero

if __name__ == "__main__":
    main()
```

### 2. Numerical Precision

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    det = np.linalg.det(A)
    
    # Check if "essentially zero"
    is_singular = np.abs(det) < 1e-10
    
    print(f"det(A) = {det:.2e}")
    print(f"Is singular: {is_singular}")

if __name__ == "__main__":
    main()
```

### 3. Condition Number

Better way to check near-singularity.

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9.0001]])  # Nearly singular
    
    cond = np.linalg.cond(A)
    
    print(f"Condition number: {cond:.2e}")
    print("High condition number indicates near-singularity")

if __name__ == "__main__":
    main()
```

## np.linalg.inv

### 1. Basic Usage

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    A_inv = np.linalg.inv(A)
    
    print("A =")
    print(A)
    print()
    print("A^(-1) =")
    print(A_inv)

if __name__ == "__main__":
    main()
```

### 2. Verify Inverse

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    A_inv = np.linalg.inv(A)
    
    # A @ A^(-1) should be identity
    product = A @ A_inv
    
    print("A @ A^(-1) =")
    print(product)
    print()
    print("Close to identity:", np.allclose(product, np.eye(2)))

if __name__ == "__main__":
    main()
```

### 3. Singular Matrix Error

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [2, 4]])  # Singular (row 2 = 2 * row 1)
    
    try:
        A_inv = np.linalg.inv(A)
    except np.linalg.LinAlgError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## np.linalg.pinv

### 1. Pseudo-Inverse

Moore-Penrose pseudo-inverse for non-square or singular matrices.

```python
import numpy as np

def main():
    # Non-square matrix
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    A_pinv = np.linalg.pinv(A)
    
    print(f"A shape: {A.shape}")
    print(f"A+ shape: {A_pinv.shape}")
    print()
    print("A+ =")
    print(A_pinv)

if __name__ == "__main__":
    main()
```

### 2. Least Squares

Pseudo-inverse gives least squares solution.

```python
import numpy as np

def main():
    # Overdetermined system
    A = np.array([[1, 1],
                  [1, 2],
                  [1, 3]])
    b = np.array([1, 2, 2])
    
    # Least squares via pinv
    x = np.linalg.pinv(A) @ b
    
    print(f"x = {x}")
    print(f"Residual: {np.linalg.norm(A @ x - b):.4f}")

if __name__ == "__main__":
    main()
```

### 3. Singular Matrix

```python
import numpy as np

def main():
    # Singular matrix
    A = np.array([[1, 2],
                  [2, 4]])
    
    # inv fails, pinv works
    A_pinv = np.linalg.pinv(A)
    
    print("A (singular) =")
    print(A)
    print()
    print("A+ =")
    print(A_pinv)

if __name__ == "__main__":
    main()
```

## Applications

### 1. Linear Transformation

```python
import numpy as np

def main():
    # Transform points
    A = np.array([[2, 0],
                  [0, 3]])
    
    points = np.array([[1, 0],
                       [0, 1],
                       [1, 1]])
    
    # Forward transform
    transformed = (A @ points.T).T
    
    # Inverse transform
    A_inv = np.linalg.inv(A)
    recovered = (A_inv @ transformed.T).T
    
    print("Original points:")
    print(points)
    print()
    print("Transformed:")
    print(transformed)
    print()
    print("Recovered:")
    print(recovered)

if __name__ == "__main__":
    main()
```

### 2. Covariance Inverse

```python
import numpy as np

def main():
    # Sample covariance matrix
    np.random.seed(42)
    X = np.random.randn(100, 3)
    cov = np.cov(X.T)
    
    # Precision matrix (inverse covariance)
    precision = np.linalg.inv(cov)
    
    print("Covariance:")
    print(cov.round(3))
    print()
    print("Precision:")
    print(precision.round(3))

if __name__ == "__main__":
    main()
```

### 3. Matrix Equation

Solve $AXB = C$ for $X$.

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    B = np.array([[5, 6],
                  [7, 8]])
    C = np.array([[10, 20],
                  [30, 40]])
    
    # X = A^(-1) @ C @ B^(-1)
    X = np.linalg.inv(A) @ C @ np.linalg.inv(B)
    
    # Verify
    print("X =")
    print(X)
    print()
    print("A @ X @ B =")
    print(A @ X @ B)

if __name__ == "__main__":
    main()
```

## Best Practices

### 1. Avoid Inverse

Prefer `np.linalg.solve` over computing inverse explicitly.

```python
import numpy as np

def main():
    A = np.random.randn(100, 100)
    b = np.random.randn(100)
    
    # Bad: compute inverse
    x_bad = np.linalg.inv(A) @ b
    
    # Good: solve directly
    x_good = np.linalg.solve(A, b)
    
    print(f"Results close: {np.allclose(x_bad, x_good)}")

if __name__ == "__main__":
    main()
```

### 2. Check Condition

Always check condition number for numerical stability.

### 3. Use pinv for Robustness

When matrix may be singular or non-square, use `pinv`.

---

## Exercises

**Exercise 1.**
Create a 3x3 matrix `A` and compute its determinant. Then compute the determinant of `2 * A` and verify that `det(2A) = 2^3 * det(A)` (the scaling property of determinants for an nxn matrix).

??? success "Solution to Exercise 1"

        import numpy as np

        A = np.array([[1, 2, 3], [0, 4, 5], [1, 0, 6]], dtype=float)
        det_A = np.linalg.det(A)
        det_2A = np.linalg.det(2 * A)
        print(f"det(A) = {det_A:.4f}")
        print(f"det(2A) = {det_2A:.4f}")
        print(f"2^3 * det(A) = {8 * det_A:.4f}")
        print(f"Match: {np.allclose(det_2A, 8 * det_A)}")

---

**Exercise 2.**
Compute the inverse of `A = np.array([[1, 2], [3, 4]])` and verify that `A @ A_inv` and `A_inv @ A` both equal the identity matrix (within floating-point tolerance).

??? success "Solution to Exercise 2"

        import numpy as np

        A = np.array([[1, 2], [3, 4]], dtype=float)
        A_inv = np.linalg.inv(A)
        print(f"A @ A_inv = \n{(A @ A_inv).round(10)}")
        print(f"Identity: {np.allclose(A @ A_inv, np.eye(2))}")
        print(f"Identity: {np.allclose(A_inv @ A, np.eye(2))}")

---

**Exercise 3.**
Create a singular matrix `A = np.array([[1, 2], [2, 4]])` (rows are linearly dependent). Show that `np.linalg.det(A)` returns approximately zero and that `np.linalg.inv(A)` either raises a `LinAlgError` or returns a matrix with very large elements.

??? success "Solution to Exercise 3"

        import numpy as np

        A = np.array([[1, 2], [2, 4]], dtype=float)
        det = np.linalg.det(A)
        print(f"det(A) = {det:.2e}")  # ~0

        try:
            A_inv = np.linalg.inv(A)
            print(f"Inverse has large values: {np.max(np.abs(A_inv)):.2e}")
        except np.linalg.LinAlgError as e:
            print(f"Error: {e}")
