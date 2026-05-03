# Companion Matrix

Finding the roots of a polynomial is equivalent to finding the eigenvalues of a particular matrix constructed from the polynomial's coefficients. This matrix is called the companion matrix, and it converts root-finding into an eigenvalue problem — which is how `np.roots` works internally. SciPy provides `linalg.companion` to construct this matrix directly.

!!! tip "Mental Model"
    The companion matrix bridges polynomials and linear algebra: its eigenvalues are exactly the roots of the polynomial. This is not just a theoretical curiosity -- it is how numerical root-finders like `np.roots` actually work under the hood, converting an algebraic problem into a well-studied eigenvalue problem.

```python
import numpy as np
from scipy import linalg
```

---

## Definition

Given a monic polynomial of degree $n$

$$
p(x) = x^n + c_{n-1}x^{n-1} + \cdots + c_1 x + c_0
$$

its companion matrix is the $n \times n$ matrix

$$
C = \begin{pmatrix} 0 & 0 & \cdots & 0 & -c_0 \\ 1 & 0 & \cdots & 0 & -c_1 \\ 0 & 1 & \cdots & 0 & -c_2 \\ \vdots & \vdots & \ddots & \vdots & \vdots \\ 0 & 0 & \cdots & 1 & -c_{n-1} \end{pmatrix}
$$

The matrix has 1's on the sub-diagonal and the negated coefficients (excluding the leading 1) in the last column. The key property is that the characteristic polynomial of $C$ equals $p(x)$, so the eigenvalues of $C$ are exactly the roots of $p$.

---

## scipy.linalg.companion

`linalg.companion` takes a 1-D array of polynomial coefficients in **descending** power order (same convention as `np.poly1d`) and returns the companion matrix.

```python
def main():
    # p(x) = x³ - 6x² + 11x - 6 = (x-1)(x-2)(x-3)
    coeffs = [1, -6, 11, -6]

    C = linalg.companion(coeffs)
    print("Companion matrix:")
    print(C)

    # Eigenvalues are polynomial roots
    roots = np.linalg.eigvals(C)
    print(f"Roots: {roots.real}")

if __name__ == "__main__":
    main()
```

```
Companion matrix:
[[ 6. -11.   6.]
 [ 1.   0.   0.]
 [ 0.   1.   0.]]
Roots: [1. 2. 3.]
```

The roots 1, 2, and 3 match the factored form $(x-1)(x-2)(x-3)$.

!!! note "Coefficient Convention"
    `linalg.companion` expects the leading coefficient (highest power) to be first and to be nonzero. For a non-monic polynomial, the function normalizes by dividing all coefficients by the leading one.

---

## Why Eigenvalues Equal Roots

The characteristic polynomial of $C$ is defined as $\det(\lambda I - C)$. By expanding this determinant along the last column, one can show that

$$
\det(\lambda I - C) = \lambda^n + c_{n-1}\lambda^{n-1} + \cdots + c_1\lambda + c_0 = p(\lambda)
$$

Since eigenvalues are the roots of the characteristic polynomial, and the characteristic polynomial of $C$ is exactly $p$, the eigenvalues of $C$ are the roots of $p$.

---

## Practical Example

Use the companion matrix approach to find roots and verify them.

```python
# p(x) = x⁴ - 10x³ + 35x² - 50x + 24 = (x-1)(x-2)(x-3)(x-4)
coeffs = [1, -10, 35, -50, 24]

C = linalg.companion(coeffs)
roots = np.sort(np.linalg.eigvals(C).real)
print(f"Roots: {roots}")  # [1. 2. 3. 4.]

# Verify: evaluate polynomial at each root
poly = np.poly1d(coeffs)
print(f"p(roots) ≈ {poly(roots)}")  # Close to [0. 0. 0. 0.]
```

---

## Summary

| Function | Input | Output |
|----------|-------|--------|
| `scipy.linalg.companion(c)` | Polynomial coefficients (descending order) | Companion matrix (NumPy array) |
| `np.linalg.eigvals(C)` | Companion matrix | Polynomial roots |

**Key Takeaways**:

- The companion matrix encodes polynomial coefficients so that its eigenvalues are the polynomial's roots
- `scipy.linalg.companion` expects coefficients in descending power order (highest power first)
- This eigenvalue-based approach is how `np.roots` computes polynomial roots internally
- The characteristic polynomial of the companion matrix equals the original polynomial

---

## Exercises

**Exercise 1.**
Use `linalg.companion` to find the roots of the polynomial $p(x) = x^3 + 2x^2 - 5x - 6$. Verify that the roots are $-3, -1, 2$ by evaluating the polynomial at each root (should be approximately zero).

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import linalg

        coeffs = [1, 2, -5, -6]
        C = linalg.companion(coeffs)
        roots = np.sort(np.linalg.eigvals(C).real)

        print(f"Roots: {roots.round(10)}")

        poly = np.poly1d(coeffs)
        print(f"p(roots) = {poly(roots).round(10)}")
        print(f"Expected roots: [-3, -1, 2]")

---

**Exercise 2.**
Create the companion matrix for $p(x) = x^5 - 15x^4 + 85x^3 - 225x^2 + 274x - 120$, which factors as $(x-1)(x-2)(x-3)(x-4)(x-5)$. Compute its eigenvalues and verify they are the integers 1 through 5. Print the maximum absolute error from the expected roots.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import linalg

        coeffs = [1, -15, 85, -225, 274, -120]
        C = linalg.companion(coeffs)
        roots = np.sort(np.linalg.eigvals(C).real)

        expected = np.array([1, 2, 3, 4, 5], dtype=float)
        max_error = np.max(np.abs(roots - expected))
        print(f"Roots: {roots.round(10)}")
        print(f"Max error from integers: {max_error:.2e}")

---

**Exercise 3.**
Generate a polynomial with known roots $[0.5, 1.5, 2.5, 3.5]$ using `np.poly`. Construct its companion matrix, compute the eigenvalues, sort them, and verify they match the original roots. Also verify that `np.roots` gives the same result as the companion matrix eigenvalue approach.

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import linalg

        original_roots = [0.5, 1.5, 2.5, 3.5]
        coeffs = np.poly(original_roots)

        C = linalg.companion(coeffs)
        eig_roots = np.sort(np.linalg.eigvals(C).real)
        np_roots = np.sort(np.roots(coeffs).real)

        print(f"Original roots:   {sorted(original_roots)}")
        print(f"Companion roots:  {eig_roots.round(10)}")
        print(f"np.roots:         {np_roots.round(10)}")
        print(f"Match: {np.allclose(eig_roots, np_roots)}")
