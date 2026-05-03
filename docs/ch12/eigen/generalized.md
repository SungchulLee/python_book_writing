# Generalized Eigenvalues

Generalized eigenvalue problems solve $Av = \lambda Bv$.

!!! tip "Mental Model"
    The standard eigenvalue problem asks "which vectors does $A$ merely scale?" The generalized problem asks "which vectors does $A$ scale relative to $B$?" This arises naturally in physics and engineering when the mass matrix $B$ and stiffness matrix $A$ define vibration modes, and in statistics where it underpins Fisher's discriminant analysis.

## linalg.eig with Two Matrices

### 1. Basic Usage

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    B = np.array([[5, 6],
                  [7, 8]])
    
    # Solve A @ v = λ @ B @ v
    eigenvalues, eigenvectors = linalg.eig(A, B)
    
    print("Generalized eigenvalues:")
    print(eigenvalues)
    print()
    print("Generalized eigenvectors:")
    print(eigenvectors)

if __name__ == "__main__":
    main()
```

### 2. Verify Solution

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2],
                  [2, 3]])
    B = np.array([[2, 0],
                  [0, 1]])
    
    eigenvalues, eigenvectors = linalg.eig(A, B)
    
    for i in range(len(eigenvalues)):
        lam = eigenvalues[i]
        v = eigenvectors[:, i]
        
        Av = A @ v
        lam_Bv = lam * B @ v
        
        print(f"Eigenvalue {i}: λ = {lam:.4f}")
        print(f"  Match: {np.allclose(Av, lam_Bv)}")

if __name__ == "__main__":
    main()
```

## Symmetric Generalized Problem

### 1. linalg.eigh with B

```python
import numpy as np
from scipy import linalg

def main():
    # Both A and B symmetric, B positive definite
    A = np.array([[4, 2],
                  [2, 3]])
    B = np.array([[2, 0.5],
                  [0.5, 1]])
    
    eigenvalues, eigenvectors = linalg.eigh(A, B)
    
    print("Eigenvalues (real, sorted):")
    print(eigenvalues)

if __name__ == "__main__":
    main()
```

### 2. B-Orthogonality

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 2],
                  [2, 3]])
    B = np.array([[2, 0],
                  [0, 1]])
    
    eigenvalues, V = linalg.eigh(A, B)
    
    # Eigenvectors are B-orthonormal: V.T @ B @ V = I
    print("V.T @ B @ V:")
    print((V.T @ B @ V).round(10))

if __name__ == "__main__":
    main()
```

## Applications

### 1. Vibration Analysis

```python
import numpy as np
from scipy import linalg

def main():
    # Mass-spring system: K @ x = ω² @ M @ x
    K = np.array([[3, -1, 0],
                  [-1, 2, -1],
                  [0, -1, 1]])
    M = np.array([[2, 0, 0],
                  [0, 1, 0],
                  [0, 0, 1]])
    
    eigenvalues, modes = linalg.eigh(K, M)
    
    print("Natural frequencies (ω):")
    print(np.sqrt(eigenvalues))

if __name__ == "__main__":
    main()
```

### 2. Fisher's Linear Discriminant

```python
import numpy as np
from scipy import linalg

def main():
    np.random.seed(42)
    
    class1 = np.random.randn(50, 3) + [0, 0, 0]
    class2 = np.random.randn(50, 3) + [2, 1, 1]
    
    S_W = np.cov(class1.T) + np.cov(class2.T)
    m1, m2 = class1.mean(axis=0), class2.mean(axis=0)
    diff = (m1 - m2).reshape(-1, 1)
    S_B = diff @ diff.T
    
    eigenvalues, eigenvectors = linalg.eig(S_B, S_W)
    idx = np.argmax(eigenvalues.real)
    w = eigenvectors[:, idx].real
    
    print("Optimal projection:")
    print(w / np.linalg.norm(w))

if __name__ == "__main__":
    main()
```

## Summary

| Function | Description |
|:---------|:------------|
| `linalg.eig(A, B)` | General Av = λBv |
| `linalg.eigh(A, B)` | Symmetric A, SPD B |
| `linalg.qz(A, B)` | QZ decomposition |

---

## Exercises

**Exercise 1.**
Solve the generalized eigenvalue problem $Av = \lambda Bv$ for $A = \begin{pmatrix} 6 & 2 \\ 2 & 4 \end{pmatrix}$ and $B = \begin{pmatrix} 2 & 0 \\ 0 & 1 \end{pmatrix}$ using `linalg.eigh(A, B)`. Verify that $V^T B V = I$ (B-orthogonality) and that $Av_i = \lambda_i B v_i$ for each eigenpair.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        A = np.array([[6, 2],
                       [2, 4]])
        B = np.array([[2, 0],
                       [0, 1]])

        eigenvalues, V = linalg.eigh(A, B)

        # B-orthogonality
        b_orth = V.T @ B @ V
        print(f"V^T B V:\n{b_orth.round(10)}")
        print(f"B-orthogonal: {np.allclose(b_orth, np.eye(2))}")

        # Verify Av = lambda Bv
        for i in range(len(eigenvalues)):
            lam = eigenvalues[i]
            v = V[:, i]
            print(f"lambda={lam:.4f}, Av=lBv: {np.allclose(A @ v, lam * B @ v)}")

---

**Exercise 2.**
Model a 3-mass spring system with stiffness matrix $K = \begin{pmatrix} 5 & -2 & 0 \\ -2 & 4 & -2 \\ 0 & -2 & 3 \end{pmatrix}$ and mass matrix $M = \begin{pmatrix} 1 & 0 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 1 \end{pmatrix}$. Find the natural frequencies $\omega_i = \sqrt{\lambda_i}$ by solving the generalized eigenvalue problem $Kx = \lambda M x$.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        K = np.array([[5, -2, 0],
                       [-2, 4, -2],
                       [0, -2, 3]])
        M = np.array([[1, 0, 0],
                       [0, 2, 0],
                       [0, 0, 1]])

        eigenvalues, modes = linalg.eigh(K, M)
        frequencies = np.sqrt(eigenvalues)

        print("Eigenvalues (omega^2):", eigenvalues)
        print("Natural frequencies (omega):", frequencies)

---

**Exercise 3.**
Generate two random $4 \times 4$ matrices with `np.random.seed(42)`. Make $A$ symmetric ($A = B_1 + B_1^T$) and $B$ symmetric positive definite ($B = B_2^T B_2 + 4I$). Solve the generalized problem with `linalg.eigh(A, B)` and verify the result by checking $\|A V - B V \Lambda\|_F < 10^{-10}$ where $\Lambda = \text{diag}(\lambda)$.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        np.random.seed(42)
        B1 = np.random.randn(4, 4)
        B2 = np.random.randn(4, 4)
        A = B1 + B1.T
        B = B2.T @ B2 + 4 * np.eye(4)

        eigenvalues, V = linalg.eigh(A, B)
        Lambda = np.diag(eigenvalues)

        error = np.linalg.norm(A @ V - B @ V @ Lambda)
        print(f"Eigenvalues: {eigenvalues}")
        print(f"Verification error: {error:.2e}")
        assert error < 1e-10
