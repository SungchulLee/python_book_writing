# Hessenberg Form

Hessenberg form reduces a matrix to almost-triangular form.

!!! tip "Mental Model"
    Hessenberg form is a halfway house between a full matrix and a triangular one -- it has zeros below the first subdiagonal. This near-triangular structure makes subsequent eigenvalue iterations converge much faster, which is why eigenvalue algorithms almost always start by reducing to Hessenberg form.

## Basic Decomposition

### 1. linalg.hessenberg

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2, 3, 4],
                  [5, 6, 7, 8],
                  [9, 10, 11, 12],
                  [13, 14, 15, 16]])
    
    H = linalg.hessenberg(A)
    
    print("A =")
    print(A)
    print()
    print("H (upper Hessenberg):")
    print(H.round(6))

if __name__ == "__main__":
    main()
```

### 2. Mathematical Form

$$A = QHQ^H$$

where:
- $Q$ is unitary
- $H$ is upper Hessenberg (zero below first subdiagonal)

### 3. Structure

```
Upper Hessenberg:
[* * * *]
[* * * *]
[0 * * *]
[0 0 * *]
```

## With Transformation Matrix

### 1. Return Q

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    H, Q = linalg.hessenberg(A, calc_q=True)
    
    print("H (Hessenberg form):")
    print(H.round(6))
    print()
    print("Q (unitary):")
    print(Q.round(6))
    print()
    print("Verify Q @ H @ Q.T:")
    print((Q @ H @ Q.T).round(6))

if __name__ == "__main__":
    main()
```

### 2. Verify Orthogonality

```python
import numpy as np
from scipy import linalg

def main():
    A = np.random.randn(4, 4)
    
    H, Q = linalg.hessenberg(A, calc_q=True)
    
    print("Q.T @ Q (should be identity):")
    print((Q.T @ Q).round(10))

if __name__ == "__main__":
    main()
```

## Eigenvalue Computation

### 1. Why Hessenberg

```python
import numpy as np
from scipy import linalg

def main():
    n = 5
    A = np.random.randn(n, n)
    
    # Eigenvalue algorithms work faster on Hessenberg form
    # QR iteration on H: O(n^2) per iteration vs O(n^3) on A
    
    H = linalg.hessenberg(A)
    
    # Eigenvalues are preserved
    eig_A = np.sort(np.linalg.eigvals(A))
    eig_H = np.sort(np.linalg.eigvals(H))
    
    print("Eigenvalues of A:")
    print(eig_A.round(6))
    print()
    print("Eigenvalues of H:")
    print(eig_H.round(6))

if __name__ == "__main__":
    main()
```

### 2. QR Iteration on Hessenberg

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 1, 0],
                  [1, 3, 1],
                  [0, 1, 2]])
    
    # Reduce to Hessenberg first
    H = linalg.hessenberg(A)
    
    # QR iteration (faster on Hessenberg)
    Hk = H.copy()
    for _ in range(30):
        Q, R = np.linalg.qr(Hk)
        Hk = R @ Q
    
    print("Converged to quasi-triangular:")
    print(Hk.round(6))
    print()
    print("Eigenvalues (diagonal):")
    print(np.diag(Hk).round(6))

if __name__ == "__main__":
    main()
```

## Symmetric Case

### 1. Tridiagonal Form

```python
import numpy as np
from scipy import linalg

def main():
    # Symmetric matrix
    A = np.array([[4, 1, 0, 0],
                  [1, 4, 1, 0],
                  [0, 1, 4, 1],
                  [0, 0, 1, 4]])
    
    H = linalg.hessenberg(A)
    
    print("H for symmetric A (tridiagonal):")
    print(H.round(6))

if __name__ == "__main__":
    main()
```

### 2. Why Tridiagonal

For symmetric matrices, Hessenberg form becomes tridiagonal, enabling even faster algorithms.

## Computational Cost

### 1. Complexity Analysis

```python
import numpy as np
from scipy import linalg
import time

def main():
    sizes = [100, 200, 400, 800]
    
    print("Hessenberg reduction times:")
    print(f"{'n':>6} | {'Time (sec)':>12}")
    print("-" * 22)
    
    for n in sizes:
        A = np.random.randn(n, n)
        
        start = time.perf_counter()
        H = linalg.hessenberg(A)
        elapsed = time.perf_counter() - start
        
        print(f"{n:6d} | {elapsed:12.4f}")

if __name__ == "__main__":
    main()
```

### 2. Reduction is O(n³)

Initial reduction: $O(n^3)$

Each QR step on H: $O(n^2)$ instead of $O(n^3)$

## Applications

### 1. Polynomial Eigenvalues

```python
import numpy as np
from scipy import linalg

def main():
    # Roots of p(x) = x^3 - 6x^2 + 11x - 6
    # Are eigenvalues of companion matrix
    
    coeffs = [1, -6, 11, -6]  # x^3 - 6x^2 + 11x - 6
    
    # Companion matrix is already Hessenberg
    C = np.array([[6, -11, 6],
                  [1, 0, 0],
                  [0, 1, 0]])
    
    roots = np.linalg.eigvals(C)
    
    print("Polynomial roots:")
    print(np.sort(roots.real).round(6))
    print()
    print("Verify: (x-1)(x-2)(x-3) = x^3 - 6x^2 + 11x - 6")

if __name__ == "__main__":
    main()
```

### 2. Transfer Function Analysis

```python
import numpy as np
from scipy import linalg

def main():
    # State-space system: dx/dt = Ax
    A = np.array([[0, 1, 0],
                  [0, 0, 1],
                  [-6, -11, -6]])
    
    H, Q = linalg.hessenberg(A, calc_q=True)
    
    print("System in Hessenberg form:")
    print(H.round(6))
    print()
    
    # Eigenvalues determine stability
    eigs = np.linalg.eigvals(H)
    print("Poles (eigenvalues):")
    print(eigs.round(6))

if __name__ == "__main__":
    main()
```

### 3. Matrix Exponential Preprocessing

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    # Hessenberg reduction can accelerate exp(A) computation
    H, Q = linalg.hessenberg(A, calc_q=True)
    
    # exp(A) = Q @ exp(H) @ Q.T
    exp_H = linalg.expm(H)
    exp_A = Q @ exp_H @ Q.T
    
    print("exp(A) via Hessenberg:")
    print(exp_A.round(6))
    print()
    print("exp(A) direct:")
    print(linalg.expm(A).round(6))

if __name__ == "__main__":
    main()
```

## Summary

### 1. Functions

| Function | Description |
|:---------|:------------|
| `linalg.hessenberg(A)` | Hessenberg form |
| `linalg.hessenberg(A, calc_q=True)` | With transformation Q |

### 2. Key Properties

- $H$ is upper Hessenberg (zeros below subdiagonal)
- Preserves eigenvalues
- Symmetric A → Tridiagonal H
- Speeds up QR iteration: $O(n^2)$ vs $O(n^3)$ per step

---

## Exercises

**Exercise 1.**
Create a random $6 \times 6$ matrix with `np.random.seed(10)`. Compute its Hessenberg form $H$ with the transformation matrix $Q$. Verify that $Q$ is orthogonal (i.e., $\|Q^TQ - I\|_F < 10^{-12}$) and that $\|QHQ^T - A\|_F < 10^{-12}$.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        np.random.seed(10)
        A = np.random.randn(6, 6)

        H, Q = linalg.hessenberg(A, calc_q=True)

        orth_error = np.linalg.norm(Q.T @ Q - np.eye(6))
        recon_error = np.linalg.norm(Q @ H @ Q.T - A)
        print(f"Orthogonality error: {orth_error:.2e}")
        print(f"Reconstruction error: {recon_error:.2e}")
        assert orth_error < 1e-12
        assert recon_error < 1e-12

---

**Exercise 2.**
Construct a $5 \times 5$ symmetric tridiagonal matrix with 4 on the diagonal and 1 on the sub/super-diagonals. Compute its Hessenberg form and verify that the result is tridiagonal (all entries below the first subdiagonal are effectively zero, i.e., below $10^{-12}$ in absolute value).

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        A = np.diag([4]*5) + np.diag([1]*4, 1) + np.diag([1]*4, -1)
        H = linalg.hessenberg(A)

        # Check entries below first subdiagonal
        is_tridiagonal = True
        for i in range(2, 5):
            for j in range(0, i - 1):
                if abs(H[i, j]) > 1e-12:
                    is_tridiagonal = False

        print("Hessenberg of symmetric matrix:")
        print(H.round(10))
        print(f"Is tridiagonal: {is_tridiagonal}")

---

**Exercise 3.**
Generate a random $8 \times 8$ matrix with `np.random.seed(7)`. Reduce it to Hessenberg form $H$, then run 50 iterations of the QR algorithm on $H$ (at each step compute $Q, R = $ QR of $H_k$, then set $H_{k+1} = RQ$). Compare the diagonal of the final matrix with the eigenvalues from `np.linalg.eigvals` and print the maximum absolute error after sorting by real part.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        np.random.seed(7)
        A = np.random.randn(8, 8)

        H = linalg.hessenberg(A)
        Hk = H.copy()
        for _ in range(50):
            Q, R = np.linalg.qr(Hk)
            Hk = R @ Q

        qr_eigs = np.sort_complex(np.diag(Hk))
        true_eigs = np.sort_complex(np.linalg.eigvals(A))

        # Sort by real part for comparison
        qr_sorted = sorted(qr_eigs, key=lambda x: (x.real, x.imag))
        true_sorted = sorted(true_eigs, key=lambda x: (x.real, x.imag))
        max_error = max(abs(a - b) for a, b in zip(qr_sorted, true_sorted))
        print(f"Max eigenvalue error: {max_error:.6f}")
