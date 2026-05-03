# Matrix Exponential

The matrix exponential $e^A$ is fundamental in solving differential equations.

!!! tip "Mental Model"
    Just as the scalar exponential $e^{at}$ solves $\dot{x} = ax$, the matrix exponential $e^{At}$ solves the system $\dot{\mathbf{x}} = A\mathbf{x}$. It is not computed element-wise -- SciPy uses scaling-and-squaring with Pade approximants to evaluate the infinite series $I + A + A^2/2! + \cdots$ accurately and efficiently.

## linalg.expm

### 1. Basic Usage

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [0, 3]])
    
    exp_A = linalg.expm(A)
    
    print("A =")
    print(A)
    print()
    print("exp(A) =")
    print(exp_A)

if __name__ == "__main__":
    main()
```

### 2. Definition

$$e^A = \sum_{k=0}^{\infty} \frac{A^k}{k!} = I + A + \frac{A^2}{2!} + \frac{A^3}{3!} + \cdots$$

### 3. Diagonal Matrix

```python
import numpy as np
from scipy import linalg

def main():
    # For diagonal matrices: exp(D) has exp on diagonal
    D = np.diag([1, 2, 3])
    
    exp_D = linalg.expm(D)
    
    print("exp(D) =")
    print(exp_D)
    print()
    print("Diagonal elements:", np.diag(exp_D))
    print("Expected:", np.exp([1, 2, 3]))

if __name__ == "__main__":
    main()
```

## Properties

### 1. exp(0) = I

```python
import numpy as np
from scipy import linalg

def main():
    n = 3
    Z = np.zeros((n, n))
    
    print("exp(0) =")
    print(linalg.expm(Z))

if __name__ == "__main__":
    main()
```

### 2. exp(A) exp(-A) = I

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    exp_A = linalg.expm(A)
    exp_neg_A = linalg.expm(-A)
    
    print("exp(A) @ exp(-A) =")
    print((exp_A @ exp_neg_A).round(10))

if __name__ == "__main__":
    main()
```

### 3. Commuting Matrices

```python
import numpy as np
from scipy import linalg

def main():
    # If AB = BA, then exp(A+B) = exp(A) exp(B)
    A = np.diag([1, 2])
    B = np.diag([3, 4])
    
    exp_ApB = linalg.expm(A + B)
    exp_A_exp_B = linalg.expm(A) @ linalg.expm(B)
    
    print("exp(A+B) =")
    print(exp_ApB)
    print()
    print("exp(A) @ exp(B) =")
    print(exp_A_exp_B)

if __name__ == "__main__":
    main()
```

## Applications

### 1. Linear ODE Solution

```python
import numpy as np
from scipy import linalg

def main():
    # dx/dt = Ax, x(0) = x0
    # Solution: x(t) = exp(At) @ x0
    
    A = np.array([[-1, 1],
                  [0, -2]])
    x0 = np.array([1, 1])
    
    # Solution at t = 1
    t = 1
    x_t = linalg.expm(A * t) @ x0
    
    print(f"x(0) = {x0}")
    print(f"x({t}) = {x_t}")

if __name__ == "__main__":
    main()
```

### 2. State Transition Matrix

```python
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt

def main():
    A = np.array([[-0.5, 1],
                  [-1, -0.5]])
    x0 = np.array([1, 0])
    
    times = np.linspace(0, 10, 100)
    trajectory = np.array([linalg.expm(A * t) @ x0 for t in times])
    
    fig, ax = plt.subplots()
    ax.plot(trajectory[:, 0], trajectory[:, 1])
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_title('System Trajectory')
    ax.axis('equal')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Rotation Matrix

```python
import numpy as np
from scipy import linalg

def main():
    # Skew-symmetric matrix generates rotation
    theta = np.pi / 4
    A = np.array([[0, -theta],
                  [theta, 0]])
    
    R = linalg.expm(A)
    
    print(f"Rotation by {np.degrees(theta)} degrees:")
    print(R)
    print()
    print("Expected:")
    print(np.array([[np.cos(theta), -np.sin(theta)],
                    [np.sin(theta), np.cos(theta)]]))

if __name__ == "__main__":
    main()
```

## Summary

| Function | Description |
|:---------|:------------|
| `linalg.expm(A)` | Matrix exponential |
| `linalg.expm_frechet(A, E)` | Frechet derivative |

Key: $e^A \neq$ element-wise exp. Use `np.exp(A)` for element-wise.

---

## Exercises

**Exercise 1.**
Compute the matrix exponential of $A = \begin{pmatrix} 0 & -\pi/2 \\ \pi/2 & 0 \end{pmatrix}$ (a skew-symmetric matrix). Verify that the result is a rotation matrix by checking that $R^TR = I$ and $\det(R) = 1$. What rotation angle does this correspond to?

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        A = np.array([[0, -np.pi / 2],
                       [np.pi / 2, 0]])
        R = linalg.expm(A)

        print(f"exp(A) =\n{R.round(10)}")
        print(f"R^T R = I: {np.allclose(R.T @ R, np.eye(2))}")
        print(f"det(R) = {np.linalg.det(R):.10f}")
        angle = np.arctan2(R[1, 0], R[0, 0])
        print(f"Rotation angle: {np.degrees(angle):.1f} degrees")

---

**Exercise 2.**
Solve the linear ODE system $\frac{dx}{dt} = Ax$ with $A = \begin{pmatrix} -1 & 2 \\ 0 & -3 \end{pmatrix}$ and initial condition $x(0) = (1, 1)^T$. Compute the solution $x(t) = e^{At} x_0$ at times $t = 0, 0.5, 1, 2, 5$ and print the state vector at each time.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        A = np.array([[-1, 2],
                       [0, -3]])
        x0 = np.array([1, 1])

        for t in [0, 0.5, 1, 2, 5]:
            x_t = linalg.expm(A * t) @ x0
            print(f"x({t}) = {x_t}")

---

**Exercise 3.**
Verify that `expm(A) @ expm(-A)` equals the identity matrix for a random $4 \times 4$ matrix (use `np.random.seed(50)`). Compute the Frobenius norm of the difference from identity and confirm it is below $10^{-12}$.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        np.random.seed(50)
        A = np.random.randn(4, 4)

        product = linalg.expm(A) @ linalg.expm(-A)
        error = np.linalg.norm(product - np.eye(4))
        print(f"expm(A) @ expm(-A) =\n{product.round(12)}")
        print(f"Error from identity: {error:.2e}")
        assert error < 1e-12
