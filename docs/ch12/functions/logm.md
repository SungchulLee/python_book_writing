# Matrix Logarithm

The matrix logarithm is the inverse of matrix exponential.

!!! tip "Mental Model"
    If the matrix exponential answers "where does this system end up after time $t$?", the matrix logarithm asks the reverse: "what generator produced this transformation?" Given a matrix $M$, its logarithm $L = \log(M)$ satisfies $e^L = M$. This is essential in control theory and Lie group computations where you need to recover continuous-time dynamics from a discrete-time transition matrix.

## linalg.logm

### 1. Basic Usage

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 0],
                  [0, 3]])
    
    log_A = linalg.logm(A)
    
    print("A =")
    print(A)
    print()
    print("log(A) =")
    print(log_A)

if __name__ == "__main__":
    main()
```

### 2. Inverse Relationship

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 0.5],
                  [0, 2]])
    
    # log(exp(A)) = A
    exp_A = linalg.expm(A)
    log_exp_A = linalg.logm(exp_A)
    
    print("A =")
    print(A)
    print()
    print("log(exp(A)) =")
    print(log_exp_A.real.round(10))

if __name__ == "__main__":
    main()
```

### 3. exp(log(A)) = A

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1],
                  [0, 3]])
    
    log_A = linalg.logm(A)
    exp_log_A = linalg.expm(log_A)
    
    print("A =")
    print(A)
    print()
    print("exp(log(A)) =")
    print(exp_log_A.real.round(10))

if __name__ == "__main__":
    main()
```

## Requirements

### 1. No Negative Eigenvalues

```python
import numpy as np
from scipy import linalg

def main():
    # Matrix with negative eigenvalue
    A = np.array([[-1, 0],
                  [0, 2]])
    
    # logm may return complex result
    log_A = linalg.logm(A)
    
    print("A eigenvalues:", np.linalg.eigvals(A))
    print()
    print("log(A) (complex):")
    print(log_A)

if __name__ == "__main__":
    main()
```

### 2. Nonsingular Matrix

```python
import numpy as np
from scipy import linalg

def main():
    # Singular matrix - logarithm undefined
    A = np.array([[1, 0],
                  [0, 0]])
    
    try:
        log_A = linalg.logm(A)
        print(log_A)
    except Exception as e:
        print(f"Error: log undefined for singular matrix")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Rotation Interpolation

```python
import numpy as np
from scipy import linalg

def main():
    # Interpolate between rotations
    theta1, theta2 = 0, np.pi/2
    
    R1 = np.array([[np.cos(theta1), -np.sin(theta1)],
                   [np.sin(theta1), np.cos(theta1)]])
    R2 = np.array([[np.cos(theta2), -np.sin(theta2)],
                   [np.sin(theta2), np.cos(theta2)]])
    
    # Interpolation: R(t) = R1 @ exp(t * log(R1.T @ R2))
    log_diff = linalg.logm(R1.T @ R2)
    
    for t in [0, 0.25, 0.5, 0.75, 1.0]:
        R_t = R1 @ linalg.expm(t * log_diff)
        angle = np.arctan2(R_t[1, 0], R_t[0, 0])
        print(f"t={t}: angle = {np.degrees(angle):.1f}°")

if __name__ == "__main__":
    main()
```

### 2. Principal Logarithm

```python
import numpy as np
from scipy import linalg

def main():
    # For positive definite matrix, log is real
    A = np.array([[4, 2],
                  [2, 3]])
    
    log_A = linalg.logm(A)
    
    print("Symmetric positive definite A:")
    print(A)
    print()
    print("log(A) (real):")
    print(log_A.real.round(6))

if __name__ == "__main__":
    main()
```

## Summary

| Function | Description |
|:---------|:------------|
| `linalg.logm(A)` | Matrix logarithm |

Key: Requires nonsingular A. May be complex for matrices with negative eigenvalues.

---

## Exercises

**Exercise 1.**
Compute the matrix logarithm of the identity matrix $I_3$. Verify that `logm(I)` returns the zero matrix (all entries below $10^{-14}$ in absolute value).

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        I = np.eye(3)
        log_I = linalg.logm(I)

        print(f"logm(I) =\n{log_I}")
        print(f"All entries ~ 0: {np.all(np.abs(log_I) < 1e-14)}")

---

**Exercise 2.**
For the SPD matrix $A = \begin{pmatrix} 3 & 1 \\ 1 & 2 \end{pmatrix}$, verify the round-trip property: compute `logm(A)`, then `expm(logm(A))`, and check that the result matches $A$ with Frobenius norm error below $10^{-12}$.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        A = np.array([[3, 1],
                       [1, 2]], dtype=float)

        log_A = linalg.logm(A)
        exp_log_A = linalg.expm(log_A)

        error = np.linalg.norm(exp_log_A.real - A)
        print(f"logm(A) =\n{log_A.real.round(8)}")
        print(f"expm(logm(A)) =\n{exp_log_A.real.round(10)}")
        print(f"Round-trip error: {error:.2e}")
        assert error < 1e-12

---

**Exercise 3.**
Create two rotation matrices $R_1$ (30 degrees) and $R_2$ (75 degrees). Use the matrix logarithm to interpolate between them at $t = 0.5$: compute $R(t) = R_1 \cdot \exp\bigl(t \cdot \log(R_1^T R_2)\bigr)$. Verify that the interpolated rotation angle is approximately 52.5 degrees (the midpoint).

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        def rotation_matrix(deg):
            rad = np.radians(deg)
            return np.array([[np.cos(rad), -np.sin(rad)],
                              [np.sin(rad), np.cos(rad)]])

        R1 = rotation_matrix(30)
        R2 = rotation_matrix(75)

        log_diff = linalg.logm(R1.T @ R2)
        t = 0.5
        R_mid = R1 @ linalg.expm(t * log_diff)

        angle = np.degrees(np.arctan2(R_mid[1, 0].real, R_mid[0, 0].real))
        print(f"Interpolated rotation matrix:\n{R_mid.real.round(6)}")
        print(f"Interpolated angle: {angle:.1f} degrees")
        print(f"Expected: 52.5 degrees")
