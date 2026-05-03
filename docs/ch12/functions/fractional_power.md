# Matrix Power

Compute arbitrary matrix powers $A^p$ including fractional exponents.

!!! tip "Mental Model"
    Fractional matrix powers generalize the idea of "square root of a matrix" to arbitrary exponents. If $A = V \Lambda V^{-1}$, then $A^p = V \Lambda^p V^{-1}$ -- each eigenvalue is raised to the power $p$. This lets you smoothly interpolate between the identity ($A^0$) and the matrix itself ($A^1$), which is useful in diffusion processes, interpolation, and numerical methods.

## linalg.fractional_matrix_power

### 1. Basic Usage

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[4, 0],
                  [0, 9]])
    
    # A^{0.5} = sqrt(A)
    A_half = linalg.fractional_matrix_power(A, 0.5)
    
    print("A =")
    print(A)
    print()
    print("A^{0.5} =")
    print(A_half)

if __name__ == "__main__":
    main()
```

### 2. Various Powers

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1],
                  [0, 3]])
    
    powers = [-1, -0.5, 0, 0.5, 1, 2]
    
    for p in powers:
        A_p = linalg.fractional_matrix_power(A, p)
        print(f"A^{p:4.1f} =")
        print(A_p.real.round(4))
        print()

if __name__ == "__main__":
    main()
```

### 3. Verify A^p @ A^q = A^{p+q}

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1],
                  [1, 2]])
    
    p, q = 0.3, 0.7
    
    A_p = linalg.fractional_matrix_power(A, p)
    A_q = linalg.fractional_matrix_power(A, q)
    A_pq = linalg.fractional_matrix_power(A, p + q)
    
    print(f"A^{p} @ A^{q} =")
    print((A_p @ A_q).real.round(6))
    print()
    print(f"A^{p+q} =")
    print(A_pq.real.round(6))

if __name__ == "__main__":
    main()
```

## Special Cases

### 1. Integer Powers

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    # Integer power via fractional_matrix_power
    A_3 = linalg.fractional_matrix_power(A, 3)
    
    # Direct computation
    A_3_direct = A @ A @ A
    
    print("A³ via fractional_matrix_power:")
    print(A_3.real.round(6))
    print()
    print("A³ direct:")
    print(A_3_direct)

if __name__ == "__main__":
    main()
```

### 2. Negative Powers

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[2, 1],
                  [1, 2]])
    
    # A^{-1}
    A_inv = linalg.fractional_matrix_power(A, -1)
    
    # Verify
    print("A^{-1} @ A =")
    print((A_inv @ A).real.round(10))

if __name__ == "__main__":
    main()
```

### 3. Zero Power

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 2],
                  [3, 4]])
    
    # A^0 = I
    A_0 = linalg.fractional_matrix_power(A, 0)
    
    print("A^0 =")
    print(A_0.real.round(10))

if __name__ == "__main__":
    main()
```

## Applications

### 1. Matrix Interpolation

```python
import numpy as np
from scipy import linalg

def main():
    A = np.array([[1, 0],
                  [0, 1]])
    B = np.array([[4, 0],
                  [0, 9]])
    
    # Interpolate: C(t) = A^{1-t} @ B^t
    for t in [0, 0.25, 0.5, 0.75, 1.0]:
        A_1mt = linalg.fractional_matrix_power(A, 1-t)
        B_t = linalg.fractional_matrix_power(B, t)
        C_t = A_1mt @ B_t
        print(f"t={t}: diag = {np.diag(C_t.real).round(2)}")

if __name__ == "__main__":
    main()
```

### 2. Diffusion Process

```python
import numpy as np
from scipy import linalg

def main():
    # Transition matrix
    P = np.array([[0.7, 0.3],
                  [0.4, 0.6]])
    
    # Fractional steps
    for t in [0.5, 1, 2, 10]:
        P_t = linalg.fractional_matrix_power(P, t)
        print(f"P^{t} =")
        print(P_t.real.round(4))
        print()

if __name__ == "__main__":
    main()
```

## Summary

| Function | Description |
|:---------|:------------|
| `linalg.fractional_matrix_power(A, p)` | Compute $A^p$ |

Key: Works for any real $p$. Uses principal branch for non-integer powers.

---

## Exercises

**Exercise 1.**
Compute $A^{1/3}$ (the cube root) for $A = \begin{pmatrix} 8 & 0 \\ 0 & 27 \end{pmatrix}$ using `fractional_matrix_power`. Verify the result by cubing it: check that $(A^{1/3})^3 \approx A$ with Frobenius norm error below $10^{-10}$.

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        A = np.array([[8, 0],
                       [0, 27]], dtype=float)

        A_third = linalg.fractional_matrix_power(A, 1/3)
        A_cubed = A_third @ A_third @ A_third

        error = np.linalg.norm(A_cubed.real - A)
        print(f"A^(1/3) =\n{A_third.real.round(6)}")
        print(f"(A^(1/3))^3 =\n{A_cubed.real.round(6)}")
        print(f"Error: {error:.2e}")
        assert error < 1e-10

---

**Exercise 2.**
For the matrix $A = \begin{pmatrix} 2 & 1 \\ 1 & 3 \end{pmatrix}$, verify the power law $A^p \cdot A^q = A^{p+q}$ for $p = 0.4$ and $q = 0.6$. Print the Frobenius norm of the difference between the two sides.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        A = np.array([[2, 1],
                       [1, 3]], dtype=float)
        p, q = 0.4, 0.6

        Ap = linalg.fractional_matrix_power(A, p)
        Aq = linalg.fractional_matrix_power(A, q)
        Apq = linalg.fractional_matrix_power(A, p + q)

        product = Ap @ Aq
        error = np.linalg.norm(product.real - Apq.real)
        print(f"A^{p} @ A^{q} =\n{product.real.round(8)}")
        print(f"A^{p+q} =\n{Apq.real.round(8)}")
        print(f"Difference norm: {error:.2e}")

---

**Exercise 3.**
Create a $3 \times 3$ transition matrix $P = \begin{pmatrix} 0.8 & 0.1 & 0.1 \\ 0.2 & 0.7 & 0.1 \\ 0.1 & 0.2 & 0.7 \end{pmatrix}$. Compute $P^{0.5}$ (the "half-step" transition matrix) and verify that each row sums to 1 and all entries are non-negative (a valid stochastic matrix).

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        P = np.array([[0.8, 0.1, 0.1],
                       [0.2, 0.7, 0.1],
                       [0.1, 0.2, 0.7]])

        P_half = linalg.fractional_matrix_power(P, 0.5).real

        row_sums = P_half.sum(axis=1)
        all_nonneg = np.all(P_half >= -1e-10)
        print(f"P^0.5 =\n{P_half.round(6)}")
        print(f"Row sums: {row_sums.round(10)}")
        print(f"All rows sum to 1: {np.allclose(row_sums, 1)}")
        print(f"All entries non-negative: {all_nonneg}")
