# General Eigenvalues

SciPy provides eigenvalue solvers for general (non-symmetric) matrices.

!!! tip "Mental Model"
    An eigenvalue tells you the factor by which a matrix stretches along a particular direction (the eigenvector). For non-symmetric matrices, eigenvalues can be complex even when the matrix is real, so `linalg.eig` always returns complex arrays. If your matrix is symmetric, use `eigh` instead for guaranteed real eigenvalues and faster computation.

## linalg.eig

### 1. Basic Usage

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    eigenvalues, eigenvectors = linalg.eig(A)
    
    print("Eigenvalues:")
    print(eigenvalues)
    print()
    print("Eigenvectors (columns):")
    print(eigenvectors)

if __name__ == "__main__":
    main()
```

### 2. Verify Av = λv

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    eigenvalues, eigenvectors = linalg.eig(A)
    
    for i in range(len(eigenvalues)):
        lam = eigenvalues[i]
        v = eigenvectors[:, i]
        
        Av = A @ v
        lam_v = lam * v
        
        print(f"Eigenvalue {i}: λ = {lam:.4f}")
        print(f"  A @ v  = {Av}")
        print(f"  λ * v  = {lam_v}")
        print(f"  Match: {np.allclose(Av, lam_v)}")
        print()

if __name__ == "__main__":
    main()
```

### 3. Complex Eigenvalues

```python
import numpy as np
from scipy import linalg

def main():
    # Rotation matrix has complex eigenvalues
    theta = np.pi / 4
    A = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])
    
    eigenvalues, eigenvectors = linalg.eig(A)
    
    print("Rotation matrix eigenvalues:")
    print(eigenvalues)
    print()
    print("Magnitude:", np.abs(eigenvalues))

if __name__ == "__main__":
    main()
```

## linalg.eigvals

### 1. Eigenvalues Only

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    # Only eigenvalues (faster if eigenvectors not needed)
    eigenvalues = linalg.eigvals(A)
    
    print("Eigenvalues:")
    print(eigenvalues)

if __name__ == "__main__":
    main()
```

### 2. Performance Comparison

```python
import numpy as np
from scipy import linalg
import time

def main():
    n = 500
    A = np.random.randn(n, n)
    
    # With eigenvectors
    start = time.perf_counter()
    vals, vecs = linalg.eig(A)
    eig_time = time.perf_counter() - start
    
    # Without eigenvectors
    start = time.perf_counter()
    vals_only = linalg.eigvals(A)
    eigvals_time = time.perf_counter() - start
    
    print(f"eig (with vectors):    {eig_time:.4f} sec")
    print(f"eigvals (values only): {eigvals_time:.4f} sec")

if __name__ == "__main__":
    main()
```

## Left Eigenvectors

### 1. Right vs Left

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    # Right eigenvectors: A @ v = λ * v
    eigenvalues, right_vecs = linalg.eig(A)
    
    # Left eigenvectors: w.H @ A = λ * w.H
    _, left_vecs = linalg.eig(A, left=True, right=False)
    
    print("Right eigenvectors:")
    print(right_vecs)
    print()
    print("Left eigenvectors:")
    print(left_vecs)

if __name__ == "__main__":
    main()
```

### 2. Both Left and Right

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    eigenvalues, left_vecs, right_vecs = linalg.eig(A, left=True, right=True)
    
    print("Eigenvalues:", eigenvalues)
    print()
    
    # Verify left: w.H @ A = λ * w.H
    for i in range(len(eigenvalues)):
        w = left_vecs[:, i]
        lam = eigenvalues[i]
        print(f"Left check {i}: {np.allclose(w.conj() @ A, lam * w.conj())}")

if __name__ == "__main__":
    main()
```

## Special Cases

### 1. Defective Matrices

```python
import numpy as np
from scipy import linalg

def main():
    # Defective matrix: eigenvalue 1 has algebraic multiplicity 2
    # but geometric multiplicity 1
    A = np.array([[1, 1],
                  [0, 1]])
    
    eigenvalues, eigenvectors = linalg.eig(A)
    
    print("Eigenvalues:")
    print(eigenvalues)
    print()
    print("Eigenvectors:")
    print(eigenvectors)
    print()
    print("Note: Only one linearly independent eigenvector")

if __name__ == "__main__":
    main()
```

### 2. Numerical Sensitivity

```python
import numpy as np
from scipy import linalg

def main():
    # Nearly defective matrix
    eps = 1e-10
    A = np.array([[1, 1],
                  [eps, 1]])
    
    eigenvalues, eigenvectors = linalg.eig(A)
    
    print(f"Eigenvalues (eps={eps}):")
    print(eigenvalues)
    print()
    
    # Condition number for eigenvalues
    cond = np.linalg.cond(eigenvectors)
    print(f"Eigenvector matrix condition number: {cond:.2e}")

if __name__ == "__main__":
    main()
```

## Spectral Decomposition

### 1. Diagonalization

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 1],
                  [2, 3]])
    
    eigenvalues, V = linalg.eig(A)
    
    # A = V @ D @ V^{-1}
    D = np.diag(eigenvalues)
    V_inv = np.linalg.inv(V)
    
    print("A = V @ D @ V^{-1}:")
    print((V @ D @ V_inv).real.round(6))
    print()
    print("Original A:")
    print(A)

if __name__ == "__main__":
    main()
```

### 2. Matrix Power via Eigendecomposition

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1],
                  [1, 2]])
    
    eigenvalues, V = linalg.eig(A)
    V_inv = np.linalg.inv(V)
    
    # A^n = V @ D^n @ V^{-1}
    n = 10
    D_n = np.diag(eigenvalues ** n)
    A_n = V @ D_n @ V_inv
    
    print(f"A^{n} via eigendecomposition:")
    print(A_n.real.round(2))
    print()
    print(f"A^{n} via matrix_power:")
    print(np.linalg.matrix_power(A, n))

if __name__ == "__main__":
    main()
```

## Applications

### 1. Stability Analysis

```python
import numpy as np
from scipy import linalg

def main():
    # Linear system dx/dt = Ax
    A = np.array([[-1, 1],
                  [0, -2]])
    
    eigenvalues = linalg.eigvals(A)
    
    print("System eigenvalues:")
    print(eigenvalues)
    print()
    
    if np.all(eigenvalues.real < 0):
        print("System is asymptotically stable")
    elif np.all(eigenvalues.real <= 0):
        print("System is marginally stable")
    else:
        print("System is unstable")

if __name__ == "__main__":
    main()
```

### 2. Markov Chain

```python
import numpy as np
from scipy import linalg

def main():
    # Transition matrix
    P = np.array([[0.7, 0.3],
                  [0.4, 0.6]])
    
    eigenvalues, eigenvectors = linalg.eig(P.T)  # Left eigenvectors of P
    
    # Stationary distribution: eigenvector for λ=1
    idx = np.argmin(np.abs(eigenvalues - 1))
    stationary = eigenvectors[:, idx].real
    stationary = stationary / stationary.sum()
    
    print("Eigenvalues:", eigenvalues)
    print()
    print("Stationary distribution:", stationary)

if __name__ == "__main__":
    main()
```

### 3. PageRank

```python
import numpy as np
from scipy import linalg

def main():
    # Adjacency matrix (simplified web graph)
    # Page 0 -> 1, 2
    # Page 1 -> 0
    # Page 2 -> 0, 1
    
    G = np.array([[0, 1, 1],
                  [1, 0, 1],
                  [0, 0, 0]])
    
    # Normalize columns
    col_sums = G.sum(axis=0)
    col_sums[col_sums == 0] = 1  # Handle dangling nodes
    M = G / col_sums
    
    # Damping factor
    d = 0.85
    n = len(G)
    A = d * M + (1 - d) / n * np.ones((n, n))
    
    # PageRank = dominant eigenvector
    eigenvalues, eigenvectors = linalg.eig(A)
    idx = np.argmax(np.abs(eigenvalues))
    pagerank = np.abs(eigenvectors[:, idx])
    pagerank = pagerank / pagerank.sum()
    
    print("PageRank scores:", pagerank.round(4))

if __name__ == "__main__":
    main()
```

## Summary

### 1. Functions

| Function | Description |
|:---------|:------------|
| `linalg.eig(A)` | Eigenvalues and eigenvectors |
| `linalg.eigvals(A)` | Eigenvalues only |
| `linalg.eig(A, left=True)` | Include left eigenvectors |

### 2. Key Points

- Eigenvalues may be complex even for real matrices
- Use `eigvals` when eigenvectors not needed
- Defective matrices have fewer eigenvectors than eigenvalues
- Left eigenvectors satisfy $w^H A = \lambda w^H$

---

## Exercises

**Exercise 1.**
Compute the eigenvalues and eigenvectors of $A = \begin{pmatrix} 0 & 1 \\ -2 & -3 \end{pmatrix}$. Verify the eigendecomposition by checking that $Av_i = \lambda_i v_i$ for each eigenpair. Print the eigenvalues and whether they are real or complex.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        A = np.array([[0, 1],
                       [-2, -3]])
        eigenvalues, eigenvectors = linalg.eig(A)

        for i in range(len(eigenvalues)):
            lam = eigenvalues[i]
            v = eigenvectors[:, i]
            match = np.allclose(A @ v, lam * v)
            print(f"lambda_{i} = {lam}, real={np.isreal(lam)}, Av=lv: {match}")

---

**Exercise 2.**
Create the transition matrix for a 3-state Markov chain: $P = \begin{pmatrix} 0.5 & 0.4 & 0.1 \\ 0.3 & 0.4 & 0.3 \\ 0.2 & 0.3 & 0.5 \end{pmatrix}$. Find the stationary distribution by computing the left eigenvector corresponding to eigenvalue 1 (use `linalg.eig(P.T)` and normalize so the entries sum to 1).

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        P = np.array([[0.5, 0.4, 0.1],
                       [0.3, 0.4, 0.3],
                       [0.2, 0.3, 0.5]])

        eigenvalues, eigenvectors = linalg.eig(P.T)
        idx = np.argmin(np.abs(eigenvalues - 1))
        stationary = eigenvectors[:, idx].real
        stationary = stationary / stationary.sum()

        print(f"Eigenvalues: {eigenvalues}")
        print(f"Stationary distribution: {stationary}")
        print(f"Sum = {stationary.sum():.6f}")

---

**Exercise 3.**
Use eigendecomposition to compute $A^{20}$ for $A = \begin{pmatrix} 1 & 1 \\ 0 & 2 \end{pmatrix}$ via $A^{20} = V D^{20} V^{-1}$. Verify the result against `np.linalg.matrix_power(A, 20)`.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        A = np.array([[1, 1],
                       [0, 2]], dtype=float)

        eigenvalues, V = linalg.eig(A)
        V_inv = np.linalg.inv(V)

        D_20 = np.diag(eigenvalues ** 20)
        A_20_eig = (V @ D_20 @ V_inv).real

        A_20_direct = np.linalg.matrix_power(A, 20)
        print(f"A^20 via eigendecomposition:\n{A_20_eig.round(2)}")
        print(f"A^20 via matrix_power:\n{A_20_direct}")
        print(f"Match: {np.allclose(A_20_eig, A_20_direct)}")
