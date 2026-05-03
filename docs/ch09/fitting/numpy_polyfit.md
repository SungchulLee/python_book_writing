# Polynomial Fitting: polyfit and poly1d

NumPy provides tools for fitting polynomials to data and working with polynomial objects.

!!! tip "Mental Model"
    `polyfit` finds the best polynomial curve through your data points by minimizing squared errors, and `poly1d` wraps those coefficients into a callable object. Think of `polyfit` as the fitting step and `poly1d` as the evaluation step -- together they give you a smooth function you can evaluate anywhere.

    Under the hood, `polyfit` builds a Vandermonde matrix from your x-values and
    solves $V\mathbf{c} \approx \mathbf{y}$ via QR decomposition — the same
    [least squares](least_squares.md) machinery described in the previous page.
    Understanding this connection explains why high-degree fits on wide x-ranges
    become unstable (the Vandermonde matrix becomes ill-conditioned) and why the
    modern `Polynomial.fit` API, which scales x to $[-1, 1]$, is more reliable.

```python
import numpy as np
```

---

## np.polyfit() — Fit Polynomial to Data

Fit a polynomial of specified degree to data points using least squares:

```python
# Data points
x = np.array([0, 1, 2, 3, 4])
y = np.array([1, 3, 7, 13, 21])

# Fit quadratic (degree 2): y = ax² + bx + c
coefficients = np.polyfit(x, y, deg=2)
print(coefficients)  # [1. 1. 1.] → y = x² + x + 1
```

### Understanding the Output

```python
# coefficients are in descending order of power
# [a, b, c] for ax² + bx + c

x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 3.9, 6.2, 7.8, 10.1])

# Linear fit (degree 1)
m, b = np.polyfit(x, y, 1)
print(f"Slope: {m:.2f}, Intercept: {b:.2f}")
# Slope: 2.00, Intercept: 0.02
```

---

## np.poly1d() — Polynomial Object

Create a polynomial object from coefficients for easy evaluation:

```python
# Create polynomial: x² + 2x + 3
p = np.poly1d([1, 2, 3])
print(p)
#    2
# 1 x + 2 x + 3

# Evaluate at x = 2
print(p(2))  # 1*4 + 2*2 + 3 = 11

# Evaluate at multiple points
x_vals = np.array([0, 1, 2, 3])
print(p(x_vals))  # [ 3  6 11 18]
```

### Combining polyfit and poly1d

```python
x = np.array([0, 1, 2, 3, 4])
y = np.array([1, 2.1, 4.9, 9.2, 16.1])

# Fit and create polynomial object
coeffs = np.polyfit(x, y, 2)
p = np.poly1d(coeffs)

# Evaluate fitted polynomial
y_fitted = p(x)
print(y_fitted)  # [1.02 2.04 4.98 9.84 16.62]

# Evaluate at new points
x_new = np.linspace(0, 5, 100)
y_new = p(x_new)
```

---

## Polynomial Operations

### Arithmetic

```python
p1 = np.poly1d([1, 2])    # x + 2
p2 = np.poly1d([1, 0, 1]) # x² + 1

# Addition
print(p1 + p2)  # x² + x + 3

# Multiplication
print(p1 * p2)  # x³ + 2x² + x + 2

# Power
print(p1 ** 2)  # x² + 4x + 4
```

### Derivative and Integral

```python
p = np.poly1d([1, -2, 1])  # x² - 2x + 1
print(p)
#    2
# 1 x - 2 x + 1

# Derivative
dp = p.deriv()
print(dp)  # 2x - 2

# Second derivative
d2p = p.deriv(2)
print(d2p)  # 2

# Integral (with constant of integration)
ip = p.integ()
print(ip)  # 0.3333 x³ - x² + x

# Integral with specific constant
ip = p.integ(k=5)  # constant = 5
```

### Roots

```python
p = np.poly1d([1, -5, 6])  # x² - 5x + 6

# Find roots
roots = p.r
print(roots)  # [3. 2.]

# Verify: (x-2)(x-3) = x² - 5x + 6
```

---

## Practical Examples

### Linear Regression

```python
# Simple linear regression
x = np.array([1, 2, 3, 4, 5])
y = np.array([2.2, 4.1, 5.9, 8.1, 9.8])

# Fit line
slope, intercept = np.polyfit(x, y, 1)
print(f"y = {slope:.2f}x + {intercept:.2f}")
# y = 1.94x + 0.28

# Create polynomial for predictions
line = np.poly1d([slope, intercept])

# Predict new values
x_new = np.array([6, 7, 8])
y_pred = line(x_new)
print(y_pred)  # [11.92 13.86 15.80]
```

### Quadratic Fit

```python
# Projectile motion data
t = np.array([0, 0.5, 1.0, 1.5, 2.0])  # time
h = np.array([0, 11.4, 15.2, 11.5, 0.1])  # height

# Fit quadratic: h = at² + bt + c
a, b, c = np.polyfit(t, h, 2)
print(f"h = {a:.2f}t² + {b:.2f}t + {c:.2f}")
# h ≈ -9.8t² + 19.6t + 0.1

# Find maximum height
trajectory = np.poly1d([a, b, c])
t_max = -b / (2*a)  # vertex of parabola
h_max = trajectory(t_max)
print(f"Max height: {h_max:.2f} at t={t_max:.2f}")
```

### Polynomial Interpolation

```python
# Given points
x = np.array([0, 1, 2, 3])
y = np.array([1, 2, 1, 2])

# Fit polynomial passing through all points
# Need degree = n_points - 1 for exact fit
coeffs = np.polyfit(x, y, 3)
p = np.poly1d(coeffs)

# Verify: polynomial passes through all points
print(p(x))  # [1. 2. 1. 2.]
```

### Trend Removal

```python
# Time series with trend
t = np.arange(100)
signal = 0.5 * t + 10 + np.random.randn(100) * 2

# Fit and remove trend
trend_coeffs = np.polyfit(t, signal, 1)
trend = np.poly1d(trend_coeffs)
detrended = signal - trend(t)

# detrended now has mean ≈ 0
```

---

## Goodness of Fit

### R-squared Calculation

```python
def r_squared(y_true, y_pred):
    """Calculate R² (coefficient of determination)."""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return 1 - (ss_res / ss_tot)

x = np.array([1, 2, 3, 4, 5])
y = np.array([2.1, 4.0, 5.9, 8.1, 10.0])

# Fit and evaluate
p = np.poly1d(np.polyfit(x, y, 1))
y_pred = p(x)
r2 = r_squared(y, y_pred)
print(f"R² = {r2:.4f}")  # R² ≈ 0.9988
```

### Residual Covariance

```python
# polyfit can return residuals and other info
coeffs, residuals, rank, sv, rcond = np.polyfit(
    x, y, 1, full=True
)
print(f"Residual sum of squares: {residuals[0]:.4f}")
```

### Choosing Polynomial Degree

```python
x = np.linspace(0, 10, 50)
y = np.sin(x) + np.random.randn(50) * 0.1

# Compare different degrees
for deg in [1, 3, 5, 10]:
    p = np.poly1d(np.polyfit(x, y, deg))
    y_pred = p(x)
    r2 = r_squared(y, y_pred)
    print(f"Degree {deg:2d}: R² = {r2:.4f}")
    
# Higher degree → better fit, but risk overfitting
```

---

!!! warning "Legacy API — Know the Limits"
    `polyfit`/`poly1d` are fine for quick, low-degree fits with moderate x-ranges. **Avoid** for:

    - High-degree polynomials (degree > 10) — numerical instability
    - Large x-ranges (e.g., `[0, 10000]`) — Vandermonde conditioning blows up
    - Production code — prefer `Polynomial.fit` from the modern `np.polynomial` module

    See [Least Squares Connection](least_squares.md) for *why* conditioning matters, and [np.polynomial Module](numpy_polynomial.md) for the stable alternative.

## Modern Alternative: np.polynomial

NumPy's newer `polynomial` module offers improved numerical stability:

```python
from numpy.polynomial import polynomial as P

x = np.array([0, 1, 2, 3, 4])
y = np.array([1, 3, 7, 13, 21])

# Fit polynomial (coefficients in ascending order!)
coeffs = P.polyfit(x, y, 2)
print(coeffs)  # [1. 1. 1.] → 1 + x + x²

# Evaluate
y_fit = P.polyval(x, coeffs)
```

### Key Differences

| Feature | `np.polyfit` | `np.polynomial.polynomial` |
|---------|--------------|---------------------------|
| Coefficient order | Descending (highest first) | Ascending (constant first) |
| Numerical stability | Can have issues | Better conditioning |
| Polynomial object | `np.poly1d` | `Polynomial` class |

```python
from numpy.polynomial import Polynomial

# Create polynomial: 1 + 2x + 3x²
p = Polynomial([1, 2, 3])  # ascending order!

# Fit from data
p_fit = Polynomial.fit(x, y, deg=2)
```

---

## Summary

| Function | Purpose |
|----------|---------|
| `np.polyfit(x, y, deg)` | Fit polynomial of degree `deg` |
| `np.poly1d(coeffs)` | Create polynomial object |
| `p(x)` | Evaluate polynomial at x |
| `p.deriv()` | Derivative of polynomial |
| `p.integ()` | Integral of polynomial |
| `p.r` | Roots of polynomial |

**Key Takeaways**:

- `polyfit` returns coefficients in **descending** order of power
- `poly1d` creates callable polynomial objects
- Degree = n_points - 1 for exact interpolation
- Higher degree risks overfitting
- Check fit quality with R² or residuals
- For numerical stability, consider `np.polynomial` module
- Use `deriv()` and `integ()` for calculus operations

---

## Exercises

**Exercise 1.**
Fit a quadratic polynomial to the projectile data `t = [0, 0.5, 1.0, 1.5, 2.0]` and `h = [0, 11.4, 15.2, 11.5, 0.1]`. Use the fitted `poly1d` to find the time at which the maximum height occurs and the value of that maximum height.

??? success "Solution to Exercise 1"

        import numpy as np

        t = np.array([0, 0.5, 1.0, 1.5, 2.0])
        h = np.array([0, 11.4, 15.2, 11.5, 0.1])

        coeffs = np.polyfit(t, h, 2)
        trajectory = np.poly1d(coeffs)

        # Maximum at vertex: t = -b / (2a)
        a, b, c = coeffs
        t_max = -b / (2 * a)
        h_max = trajectory(t_max)
        print(f"Polynomial: {a:.2f}t^2 + {b:.2f}t + {c:.2f}")
        print(f"Max height: {h_max:.2f} at t = {t_max:.2f}")

---

**Exercise 2.**
Generate 100 points from `y = sin(x)` on `[0, 2*pi]` with Gaussian noise (`sigma=0.1`). Fit polynomials of degrees 3, 5, 7, and 9. Compute the R-squared value for each and print which degree gives the best fit without overfitting (hint: the R-squared should plateau).

??? success "Solution to Exercise 2"

        import numpy as np

        np.random.seed(42)
        x = np.linspace(0, 2*np.pi, 100)
        y = np.sin(x) + 0.1 * np.random.randn(100)

        def r_squared(y_true, y_pred):
            ss_res = np.sum((y_true - y_pred)**2)
            ss_tot = np.sum((y_true - y_true.mean())**2)
            return 1 - ss_res / ss_tot

        for deg in [3, 5, 7, 9]:
            p = np.poly1d(np.polyfit(x, y, deg))
            r2 = r_squared(y, p(x))
            print(f"Degree {deg}: R^2 = {r2:.6f}")

---

**Exercise 3.**
Create a time series with a quadratic trend: `signal = 0.01*t**2 + 0.5*t + 10 + noise` for `t = np.arange(200)`. Use `np.polyfit` and `np.poly1d` to fit and remove the quadratic trend. Verify that the detrended signal has approximately zero mean and no visible trend.

??? success "Solution to Exercise 3"

        import numpy as np

        np.random.seed(42)
        t = np.arange(200, dtype=float)
        noise = np.random.randn(200) * 2
        signal = 0.01*t**2 + 0.5*t + 10 + noise

        # Fit and remove quadratic trend
        trend_coeffs = np.polyfit(t, signal, 2)
        trend = np.poly1d(trend_coeffs)
        detrended = signal - trend(t)

        print(f"Detrended mean: {detrended.mean():.4f}")
        print(f"Detrended std:  {detrended.std():.4f}")
