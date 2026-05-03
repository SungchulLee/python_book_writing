# Solving Linear Systems

Solve systems of linear equations $Ax = b$ using `np.linalg`.

!!! tip "Mental Model"
    `np.linalg.solve(A, b)` finds the vector $x$ such that $Ax = b$, using LU decomposition internally. Always prefer `solve` over computing `inv(A) @ b` -- it is both faster and more numerically accurate. For overdetermined systems (more equations than unknowns), use `np.linalg.lstsq` instead.

    At the deepest level, almost every numerical linear algebra problem reduces to
    some form of $Ax = b$: regression is $Ax \approx b$ (least squares), eigenvalue
    problems become $(A - \lambda I)x = 0$, and matrix factorizations are tools for
    solving $Ax = b$ efficiently under different structural assumptions.

## np.linalg.solve

### 1. Basic Usage

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    b = np.array([5, 6])
    
    x = np.linalg.solve(A, b)
    
    print(f"x = {x}")
    print(f"Verify A @ x = {A @ x}")

if __name__ == "__main__":
    main()
```

**Output:**

```
x = [-4.   4.5]
Verify A @ x = [5. 6.]
```

### 2. Mathematical Form

Solve:

$$\begin{cases} 1x_1 + 2x_2 = 5 \\ 3x_1 + 4x_2 = 6 \end{cases}$$

### 3. Multiple Right-Hand Sides

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    B = np.array([[5, 1],
                  [6, 2]])  # Two RHS vectors as columns
    
    X = np.linalg.solve(A, B)
    
    print("X =")
    print(X)
    print()
    print("Verify A @ X =")
    print(A @ X)

if __name__ == "__main__":
    main()
```

## Why Not Inverse?

### 1. Numerical Stability

```python
import numpy as np

def main():
    np.random.seed(42)
    n = 100
    
    A = np.random.randn(n, n)
    b = np.random.randn(n)
    
    # Method 1: Using inverse (less stable)
    x1 = np.linalg.inv(A) @ b
    
    # Method 2: Using solve (more stable)
    x2 = np.linalg.solve(A, b)
    
    # Both give similar results for well-conditioned A
    print(f"Max difference: {np.max(np.abs(x1 - x2)):.2e}")

if __name__ == "__main__":
    main()
```

### 2. Performance

```python
import numpy as np
import time

def main():
    n = 1000
    A = np.random.randn(n, n)
    b = np.random.randn(n)
    
    # Using inverse
    start = time.perf_counter()
    x1 = np.linalg.inv(A) @ b
    inv_time = time.perf_counter() - start
    
    # Using solve
    start = time.perf_counter()
    x2 = np.linalg.solve(A, b)
    solve_time = time.perf_counter() - start
    
    print(f"Inverse time: {inv_time:.4f} sec")
    print(f"Solve time:   {solve_time:.4f} sec")

if __name__ == "__main__":
    main()
```

### 3. Rule of Thumb

Always use `solve` instead of computing inverse explicitly.

## Solution Cases

Linear systems $Ax = b$ have three possible outcomes depending on the matrix $A$.

### 1. Unique Solution

Full rank square matrix has exactly one solution.

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    b = np.array([[5],
                  [11]])
    
    # Method 1: inverse (not recommended)
    x1 = np.linalg.inv(A) @ b
    print("Using inv:")
    print(x1)
    print()
    
    # Method 2: solve (not recommended for general case)
    x2 = np.linalg.solve(A, b)
    print("Using solve:")
    print(x2)
    print()
    
    # Method 3: lstsq (recommended - handles all cases)
    x3, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    print("Using lstsq:")
    print(x3)
    print(f"Rank: {rank}")

if __name__ == "__main__":
    main()
```

### 2. Infinitely Many Solutions

Dependent rows (rank < n) with consistent equations.

```python
import numpy as np

def main():
    # Rows are linearly dependent (row2 = row1)
    A = np.array([[1, 2],
                  [1, 2]])
    b = np.array([[5],
                  [5]])
    
    # inv and solve will fail
    # lstsq returns minimum norm solution
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    
    print("Minimum norm solution:")
    print(x)
    print(f"Rank: {rank}")
    print()
    
    # Verify: any x where x1 + 2*x2 = 5 is valid
    print(f"A @ x = {(A @ x).flatten()}")

if __name__ == "__main__":
    main()
```

### 3. No Solution

Inconsistent equations (overdetermined or contradictory).

```python
import numpy as np

def main():
    # Inconsistent: row2 = 2*row1 but b2 != 2*b1
    A = np.array([[1, 2],
                  [2, 4]])
    b = np.array([[5],
                  [11]])  # Should be 10 for consistency
    
    # lstsq returns least squares solution
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    
    print("Least squares solution:")
    print(x)
    print(f"Rank: {rank}")
    print()
    
    # Check residual (non-zero means no exact solution)
    actual = A @ x
    print(f"A @ x = {actual.flatten()}")
    print(f"b = {b.flatten()}")
    print(f"Residual norm: {np.linalg.norm(actual - b):.4f}")

if __name__ == "__main__":
    main()
```

## Overdetermined Systems

### 1. More Equations Than Unknowns

```python
import numpy as np

def main():
    # 3 equations, 2 unknowns
    A = np.array([[1, 2],
                  [3, 4],
                  [4, 6]])
    b = np.array([[5],
                  [11],
                  [15]])
    
    # lstsq finds best fit
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    
    print("Least squares solution:")
    print(x)
    print(f"Rank: {rank}")
    print()
    print(f"A @ x =")
    print(A @ x)
    print()
    print(f"b =")
    print(b)

if __name__ == "__main__":
    main()
```

### 2. Method Comparison

| Method | Unique | Many | None | Overdetermined |
|:-------|:------:|:----:|:----:|:--------------:|
| `inv(A) @ b` | ✓ | ✗ | ✗ | ✗ |
| `solve(A, b)` | ✓ | ✗ | ✗ | ✗ |
| `lstsq(A, b)` | ✓ | ✓ | ✓ | ✓ |

### 3. Recommendation

Use `np.linalg.lstsq` for robustness across all cases.

### 1. Error Handling

```python
import numpy as np

def main():
    # Singular matrix
    A = np.array([[1, 2],
                  [2, 4]])
    b = np.array([3, 6])
    
    try:
        x = np.linalg.solve(A, b)
    except np.linalg.LinAlgError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### 2. Check Before Solving

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [2, 4]])
    b = np.array([3, 6])
    
    det = np.linalg.det(A)
    
    if np.abs(det) < 1e-10:
        print("Matrix is singular or near-singular")
        print("Using least squares instead")
        x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
        print(f"x = {x}")
    else:
        x = np.linalg.solve(A, b)

if __name__ == "__main__":
    main()
```

### 3. Condition Number

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [2, 4.0001]])  # Nearly singular
    b = np.array([3, 6])
    
    cond = np.linalg.cond(A)
    print(f"Condition number: {cond:.2e}")
    
    if cond > 1e10:
        print("Warning: Ill-conditioned system")
    
    x = np.linalg.solve(A, b)
    print(f"x = {x}")

if __name__ == "__main__":
    main()
```

## np.linalg.lstsq

### 1. Overdetermined Systems

More equations than unknowns.

```python
import numpy as np

def main():
    # 3 equations, 2 unknowns
    A = np.array([[1, 1],
                  [1, 2],
                  [1, 3]])
    b = np.array([1, 2, 2])
    
    x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    
    print(f"Least squares solution: x = {x}")
    print(f"Residual sum of squares: {residuals}")
    print(f"Matrix rank: {rank}")

if __name__ == "__main__":
    main()
```

### 2. Linear Regression

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Data points
    x_data = np.array([0, 1, 2, 3, 4])
    y_data = np.array([1, 2.1, 2.9, 4.2, 4.8])
    
    # Design matrix [1, x]
    A = np.column_stack([np.ones_like(x_data), x_data])
    
    # Least squares fit
    coeffs, residuals, rank, s = np.linalg.lstsq(A, y_data, rcond=None)
    
    intercept, slope = coeffs
    print(f"y = {slope:.3f}x + {intercept:.3f}")
    
    # Plot
    fig, ax = plt.subplots()
    ax.scatter(x_data, y_data, label='Data')
    ax.plot(x_data, A @ coeffs, 'r-', label='Fit')
    ax.legend()
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Polynomial Fitting

```python
import numpy as np

def main():
    # Data
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([1, 1, 2, 4, 7])
    
    # Quadratic fit: y = a + bx + cx^2
    A = np.column_stack([np.ones_like(x), x, x**2])
    
    coeffs, residuals, rank, s = np.linalg.lstsq(A, y, rcond=None)
    
    a, b, c = coeffs
    print(f"y = {c:.3f}x² + {b:.3f}x + {a:.3f}")

if __name__ == "__main__":
    main()
```

## Structured Matrices

### 1. Triangular Systems

```python
import numpy as np
from scipy import linalg

def main():
    # Upper triangular
    U = np.array([[2, 1, 3],
                  [0, 4, 2],
                  [0, 0, 5]])
    b = np.array([10, 14, 15])
    
    # Specialized solver (faster)
    x = linalg.solve_triangular(U, b)
    
    print(f"x = {x}")
    print(f"Verify U @ x = {U @ x}")

if __name__ == "__main__":
    main()
```

### 2. Symmetric Positive Definite

```python
import numpy as np
from scipy import linalg

def main():
    # Symmetric positive definite
    A = np.array([[4, 2, 1],
                  [2, 5, 2],
                  [1, 2, 6]])
    b = np.array([1, 2, 3])
    
    # Cholesky-based solve
    x = linalg.solve(A, b, assume_a='pos')
    
    print(f"x = {x}")
    print(f"Verify A @ x = {A @ x}")

if __name__ == "__main__":
    main()
```

### 3. Banded Matrices

```python
import numpy as np
from scipy import linalg

def main():
    # Tridiagonal matrix
    n = 5
    diag = 4 * np.ones(n)
    off_diag = -np.ones(n - 1)
    
    A = np.diag(diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1)
    b = np.ones(n)
    
    x = np.linalg.solve(A, b)
    
    print("A =")
    print(A)
    print(f"x = {x}")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Circuit Analysis

```python
import numpy as np

def main():
    # Kirchhoff's laws: RI = V
    R = np.array([[10, -5, 0],
                  [-5, 15, -10],
                  [0, -10, 20]])
    V = np.array([10, 0, 0])
    
    I = np.linalg.solve(R, V)
    
    print(f"Currents: {I}")

if __name__ == "__main__":
    main()
```

### 2. Equilibrium Prices

```python
import numpy as np

def main():
    # Supply-demand equilibrium
    A = np.array([[2, -1],
                  [1, 1]])
    b = np.array([1, 3])
    
    prices = np.linalg.solve(A, b)
    
    print(f"Equilibrium prices: {prices}")

if __name__ == "__main__":
    main()
```

### 3. Heat Distribution

```python
import numpy as np

def main():
    # Steady-state heat equation (finite differences)
    n = 5
    
    # Laplacian matrix
    A = -2 * np.eye(n) + np.eye(n, k=1) + np.eye(n, k=-1)
    
    # Boundary conditions
    b = np.zeros(n)
    b[0] = -100   # Left boundary at 100
    b[-1] = -50   # Right boundary at 50
    
    T = np.linalg.solve(A, b)
    
    print(f"Temperature profile: {T}")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Solve the system `2x + y = 5` and `x + 3y = 7` using `np.linalg.solve`. Verify the solution by substituting back into both equations.

??? success "Solution to Exercise 1"

        import numpy as np

        A = np.array([[2, 1], [1, 3]], dtype=float)
        b = np.array([5, 7], dtype=float)
        x = np.linalg.solve(A, b)
        print(f"Solution: x={x[0]:.4f}, y={x[1]:.4f}")
        print(f"Verify: {np.allclose(A @ x, b)}")

---

**Exercise 2.**
Create a 4x4 random matrix `A` and a random vector `b` of length 4. Solve `A @ x = b` using both `np.linalg.solve` and `np.linalg.inv(A) @ b`. Verify both give the same answer, and explain why `solve` is preferred over computing the inverse.

??? success "Solution to Exercise 2"

        import numpy as np

        np.random.seed(42)
        A = np.random.randn(4, 4)
        b = np.random.randn(4)

        x_solve = np.linalg.solve(A, b)
        x_inv = np.linalg.inv(A) @ b

        print(f"solve:  {x_solve}")
        print(f"inv@b:  {x_inv}")
        print(f"Match: {np.allclose(x_solve, x_inv)}")
        # solve is preferred because it is faster and more
        # numerically stable than computing the full inverse.

---

**Exercise 3.**
Solve a system with multiple right-hand sides: `A @ X = B` where `A` is 3x3 and `B` is 3x2 (two right-hand side vectors). Use `np.linalg.solve(A, B)` and verify the result shape is `(3, 2)`.

??? success "Solution to Exercise 3"

        import numpy as np

        A = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 10]], dtype=float)
        B = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
        X = np.linalg.solve(A, B)
        print(f"X shape: {X.shape}")  # (3, 2)
        print(f"Verify: {np.allclose(A @ X, B)}")
