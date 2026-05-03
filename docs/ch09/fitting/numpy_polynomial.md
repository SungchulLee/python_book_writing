# np.polynomial Module (Modern API)

NumPy's legacy functions `np.polyfit` and `np.poly1d` represent polynomials with coefficients in descending power order, which can cause numerical instability for high-degree fits. The `np.polynomial` module provides a modern replacement that stores coefficients in ascending order, supports fitting over shifted and scaled domains, and offers multiple polynomial bases beyond the standard power basis. This page covers the modern API and highlights the practical differences from the legacy interface.

!!! tip "Mental Model"
    The modern `Polynomial` class fixes the two biggest problems with the legacy API: coefficient order is ascending (constant term first, matching math convention), and fitting automatically maps data to a `[-1, 1]` window for numerical stability. If you are starting new code, prefer `numpy.polynomial.Polynomial` over `np.polyfit`/`np.poly1d`.

```python
import numpy as np
from numpy.polynomial import Polynomial
```

---

## Polynomial Class Basics

The `Polynomial` class is the central object in the modern API. Unlike `np.poly1d`, it stores coefficients in **ascending** order of power.

```python
# Create polynomial: 3 + 2x + x²
# Coefficients in ascending order: [constant, x^1, x^2, ...]
p = Polynomial([3, 2, 1])
print(p)
# 3.0 + 2.0·x + 1.0·x²
```

### Evaluation

```python
# Evaluate at a single point
print(p(2))  # 3 + 2*2 + 1*4 = 11.0

# Evaluate at multiple points
x = np.array([0, 1, 2, 3])
print(p(x))  # [ 3.  6. 11. 18.]
```

### Coefficient Access

```python
p = Polynomial([3, 2, 1])

# Coefficients (ascending order)
print(p.coef)    # [3. 2. 1.]

# Degree
print(p.degree())  # 2

# Domain and window (used for fitting)
print(p.domain)  # [-1  1]
print(p.window)  # [-1  1]
```

---

## Fitting Data with Polynomial.fit

The class method `Polynomial.fit` performs least-squares fitting. A key advantage over `np.polyfit` is that it automatically maps the data domain to $[-1, 1]$ before fitting, which improves numerical conditioning for large or unevenly spaced $x$ values.

```python
x = np.array([0, 1, 2, 3, 4])
y = np.array([1, 3, 7, 13, 21])

# Fit a degree-2 polynomial
p_fit = Polynomial.fit(x, y, deg=2)
print(p_fit)
# Displays the polynomial in the mapped domain
```

### Domain Mapping

When `Polynomial.fit` receives data with domain $[a, b]$, it internally maps $x$ to $[-1, 1]$ via

$$
u = \frac{2x - (a + b)}{b - a}
$$

and fits the polynomial in $u$. This avoids the large powers of $x$ that cause numerical issues with `np.polyfit` for high degrees or wide data ranges.

```python
# The fitted polynomial remembers its domain
print(p_fit.domain)  # [0. 4.]

# Convert to standard power-basis coefficients
p_standard = p_fit.convert()
print(p_standard.coef)  # [1. 1. 1.] → 1 + x + x²
```

### Evaluation in Original Domain

The fitted polynomial evaluates correctly in the original domain without manual conversion.

```python
# Evaluate at the original data points
print(p_fit(x))  # [1. 3. 7. 13. 21.]

# Predict at new points
x_new = np.array([5, 6])
print(p_fit(x_new))  # [31. 43.]
```

---

## Arithmetic Operations

`Polynomial` objects support standard arithmetic. All operations return new `Polynomial` objects.

```python
p1 = Polynomial([1, 2])       # 1 + 2x
p2 = Polynomial([3, 0, 1])    # 3 + x²

# Addition
print(p1 + p2)  # 4.0 + 2.0·x + 1.0·x²

# Subtraction
print(p1 - p2)  # -2.0 + 2.0·x - 1.0·x²

# Multiplication
print(p1 * p2)  # 3.0 + 6.0·x + 1.0·x² + 2.0·x³

# Scalar multiplication
print(3 * p1)   # 3.0 + 6.0·x

# Power
print(p1 ** 2)  # 1.0 + 4.0·x + 4.0·x²
```

---

## Calculus Operations

### Derivative

```python
p = Polynomial([1, -2, 3])  # 1 - 2x + 3x²

# First derivative: -2 + 6x
dp = p.deriv()
print(dp.coef)  # [-2.  6.]

# Second derivative: 6
d2p = p.deriv(2)
print(d2p.coef)  # [6.]
```

### Integration

```python
p = Polynomial([2, 3])  # 2 + 3x

# Indefinite integral: C + 2x + 1.5x²
ip = p.integ()
print(ip.coef)  # [0.  2.  1.5]

# With specific constant of integration
ip = p.integ(k=5)
print(ip.coef)  # [5.  2.  1.5]
```

### Roots

```python
p = Polynomial([6, -5, 1])  # 6 - 5x + x² = (x-2)(x-3)
print(p.roots())  # [2. 3.]
```

---

## Module-Level Functions

The `numpy.polynomial.polynomial` submodule provides standalone functions that work with plain coefficient arrays instead of `Polynomial` objects.

```python
from numpy.polynomial import polynomial as P

x = np.array([0, 1, 2, 3, 4])
y = np.array([1, 3, 7, 13, 21])

# Fit polynomial — returns coefficient array (ascending order)
coeffs = P.polyfit(x, y, 2)
print(coeffs)  # [1. 1. 1.] → 1 + x + x²

# Evaluate polynomial from coefficient array
y_fit = P.polyval(x, coeffs)
print(y_fit)  # [ 1.  3.  7. 13. 21.]
```

### Available Functions

| Function | Purpose |
|----------|---------|
| `P.polyfit(x, y, deg)` | Least-squares fit, returns coefficient array |
| `P.polyval(x, c)` | Evaluate polynomial at $x$ given coefficients $c$ |
| `P.polyadd(c1, c2)` | Add two polynomials (coefficient arrays) |
| `P.polymul(c1, c2)` | Multiply two polynomials |
| `P.polyder(c)` | Derivative (returns coefficient array) |
| `P.polyint(c)` | Integral (returns coefficient array) |
| `P.polyroots(c)` | Roots of polynomial |

---

## Comparison with Legacy API

The modern `np.polynomial` module differs from the legacy `np.polyfit` / `np.poly1d` interface in several ways.

| Feature | Legacy (`np.polyfit` / `np.poly1d`) | Modern (`np.polynomial`) |
|---------|-------------------------------------|--------------------------|
| Coefficient order | Descending (highest power first) | Ascending (constant first) |
| Domain mapping | None (fits raw $x$ values) | Automatic $[-1, 1]$ mapping |
| Numerical stability | Degrades for high degree | Better conditioned |
| Multiple bases | Power basis only | Chebyshev, Legendre, Hermite, Laguerre |
| Status | Legacy (not deprecated) | Recommended for new code |

```python
# Legacy: descending coefficients
legacy_coeffs = np.polyfit(x, y, 2)
print(legacy_coeffs)  # [1. 1. 1.] → 1·x² + 1·x + 1

# Modern: ascending coefficients
modern_coeffs = P.polyfit(x, y, 2)
print(modern_coeffs)  # [1. 1. 1.] → 1 + 1·x + 1·x²
# Same numbers here, but the order convention is reversed!
```

!!! warning "Coefficient Order Matters"
    The legacy and modern APIs use **opposite** coefficient orderings. Passing legacy coefficients to modern functions (or vice versa) produces wrong results. Always check which convention a function expects.

---

## When polyfit Fails but Polynomial.fit Works

Large x-ranges cause `polyfit` to produce garbage while `Polynomial.fit` handles them gracefully thanks to automatic domain mapping:

```python
import numpy as np
from numpy.polynomial import Polynomial

x = np.linspace(0, 10000, 50)
y = np.sin(x / 1000)

# Legacy — ill-conditioned, coefficients are unreliable
legacy_coeffs = np.polyfit(x, y, 8)
legacy_pred = np.polyval(legacy_coeffs, x)
print(f"polyfit max error:        {np.max(np.abs(legacy_pred - y)):.2e}")

# Modern — automatic domain mapping keeps it stable
p_modern = Polynomial.fit(x, y, 8)
print(f"Polynomial.fit max error: {np.max(np.abs(p_modern(x) - y)):.2e}")
```

---

## Other Polynomial Bases

The `np.polynomial` module supports polynomial bases beyond the standard power basis. Each basis has its own class and submodule with the same interface.

```python
from numpy.polynomial import Chebyshev, Legendre

# Fit using Chebyshev polynomials
x = np.linspace(-1, 1, 50)
y = np.exp(x)

cheb_fit = Chebyshev.fit(x, y, deg=5)
print(cheb_fit(0.5))  # Close to np.exp(0.5)

# Fit using Legendre polynomials
leg_fit = Legendre.fit(x, y, deg=5)
print(leg_fit(0.5))   # Close to np.exp(0.5)
```

| Class | Basis | Typical Use |
|-------|-------|-------------|
| `Polynomial` | Power basis $\{1, x, x^2, \ldots\}$ | General-purpose fitting |
| `Chebyshev` | Chebyshev $\{T_0, T_1, T_2, \ldots\}$ | Approximation on $[-1, 1]$ |
| `Legendre` | Legendre $\{P_0, P_1, P_2, \ldots\}$ | Numerical integration weights |
| `Hermite` | Hermite $\{H_0, H_1, H_2, \ldots\}$ | Gaussian-weighted problems |
| `Laguerre` | Laguerre $\{L_0, L_1, L_2, \ldots\}$ | Semi-infinite domains |

---

## Summary

| Feature | Function / Method |
|---------|-------------------|
| Create polynomial | `Polynomial([c0, c1, c2])` (ascending order) |
| Fit from data | `Polynomial.fit(x, y, deg)` |
| Evaluate | `p(x)` |
| Derivative | `p.deriv(n)` |
| Integral | `p.integ(k=0)` |
| Roots | `p.roots()` |
| Convert to standard form | `p.convert()` |
| Coefficient array fit | `P.polyfit(x, y, deg)` |
| Coefficient array eval | `P.polyval(x, c)` |

**Key Takeaways**:

- The modern `np.polynomial` module stores coefficients in **ascending** order
- `Polynomial.fit` automatically maps data to $[-1, 1]$ for better numerical stability
- Multiple polynomial bases (Chebyshev, Legendre, etc.) share the same interface
- Use `p.convert()` to get standard power-basis coefficients from a fitted polynomial
- The legacy `np.polyfit` / `np.poly1d` functions still work but the modern API is preferred for new code

---

## Exercises

**Exercise 1.**
Using `Polynomial.fit`, fit a degree-3 polynomial to `x = np.linspace(0, 10, 50)` and `y = np.sin(x)`. Convert the fitted polynomial to standard form with `.convert()` and print the ascending-order coefficients. Evaluate the fit at `x = 5.0` and compare with `np.sin(5.0)`.

??? success "Solution to Exercise 1"

        import numpy as np
        from numpy.polynomial import Polynomial

        x = np.linspace(0, 10, 50)
        y = np.sin(x)
        p = Polynomial.fit(x, y, deg=3)

        p_std = p.convert()
        print(f"Coefficients (ascending): {p_std.coef}")
        print(f"Fit at x=5:    {p(5.0):.6f}")
        print(f"sin(5):        {np.sin(5.0):.6f}")
        print(f"Error:         {abs(p(5.0) - np.sin(5.0)):.6f}")

---

**Exercise 2.**
Create two `Polynomial` objects: `p1 = 1 + 2x` and `p2 = 3 - x + x^2`. Compute their product, the derivative of the product, and the roots of the derivative. Verify by hand that the roots are correct critical points.

??? success "Solution to Exercise 2"

        import numpy as np
        from numpy.polynomial import Polynomial

        p1 = Polynomial([1, 2])       # 1 + 2x
        p2 = Polynomial([3, -1, 1])   # 3 - x + x^2

        product = p1 * p2
        print(f"Product: {product}")

        dp = product.deriv()
        print(f"Derivative: {dp}")

        roots = dp.roots()
        print(f"Critical points: {roots}")

---

**Exercise 3.**
Fit `y = exp(x)` on `[-1, 1]` using both `Polynomial.fit` (power basis, degree 5) and `Chebyshev.fit` (Chebyshev basis, degree 5). Evaluate both fits at 50 equally spaced points and print the maximum absolute error for each. Explain which basis gives a better approximation and why.

??? success "Solution to Exercise 3"

        import numpy as np
        from numpy.polynomial import Polynomial, Chebyshev

        x = np.linspace(-1, 1, 50)
        y = np.exp(x)

        p_fit = Polynomial.fit(x, y, deg=5)
        c_fit = Chebyshev.fit(x, y, deg=5)

        err_poly = np.max(np.abs(p_fit(x) - y))
        err_cheb = np.max(np.abs(c_fit(x) - y))

        print(f"Polynomial max error: {err_poly:.2e}")
        print(f"Chebyshev max error:  {err_cheb:.2e}")
        # Chebyshev typically gives a better approximation on [-1, 1]
        # because Chebyshev polynomials minimize the maximum error
        # (near-optimal minimax approximation).
