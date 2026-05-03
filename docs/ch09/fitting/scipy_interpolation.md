# scipy.interpolate — Spline Interpolation

While NumPy's `polyfit` fits a single polynomial to data, `scipy.interpolate` provides piecewise spline interpolation that avoids the oscillation problems of high-degree polynomials. Spline interpolation is essential in financial mathematics for constructing smooth yield curves, volatility surfaces, and forward rate curves from discrete market data.

!!! tip "Mental Model"
    Instead of one global polynomial that oscillates wildly at the edges, spline interpolation stitches together many low-degree polynomials -- one per interval between data points -- and enforces smoothness at the joints. The result passes exactly through your data while staying well-behaved between points.

    The key distinction from `polyfit` / `Polynomial.fit`: those are **global
    approximation** (one polynomial for the entire domain), while splines are
    **local approximation** (many small polynomials, each responsible for one
    interval). Global fitting minimizes overall error but can oscillate; local
    fitting trades global optimality for guaranteed smoothness.

---

!!! warning "Why Not Just Use a High-Degree Polynomial?"
    A single high-degree polynomial through $n$ points tends to **oscillate wildly** between the data points, especially near the edges. This is the **Runge phenomenon** — the very reason splines exist. Splines avoid it by using many low-degree (typically cubic) pieces joined smoothly, keeping the curve well-behaved everywhere.

## interp1d — 1D Interpolation

The `interp1d` function creates a callable interpolant from discrete $(x, y)$ data:

```python
import numpy as np
from scipy.interpolate import interp1d

x = np.array([0.1, 0.5, 1.0, 2.0, 5.0, 10.0])
y = np.array([0.0, 0.109, 0.212, 0.274, 0.147, 0.002])

f_linear = interp1d(x, y, kind='linear')
f_cubic = interp1d(x, y, kind='cubic')

# Evaluate at any point within the data range
x_fine = np.linspace(x.min(), x.max(), 200)
y_linear = f_linear(x_fine)
y_cubic = f_cubic(x_fine)
```

The `kind` parameter selects the interpolation method: `'linear'` (default), `'quadratic'`, `'cubic'`, or an integer specifying the spline order.

### Combining Interpolation with Integration

A powerful pattern is to interpolate discrete data and then integrate the smooth interpolant. This computes quantities like the expected value of an empirical distribution:

```python
from scipy.integrate import quad

x = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.55, 0.662, 0.8, 1., 1.25,
              1.5, 2., 3., 4., 5., 6., 8., 10.])
y = np.array([0., 0.032, 0.06, 0.086, 0.109, 0.131, 0.151, 0.185,
              0.212, 0.238, 0.257, 0.274, 0.256, 0.205, 0.147, 0.096, 0.029, 0.002])

f = interp1d(x, y, 'cubic')

numerator = quad(lambda t: t * f(t), x.min(), x.max())[0]
denominator = quad(f, x.min(), x.max())[0]
mean = numerator / denominator  # ≈ 3.38
```

### Interpolation for ODE Solving

Tabulated data can be converted into smooth functions for use as coefficients in differential equations:

```python
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp

t_data = np.array([0., 0.25, 0.5, 0.75, 1.])
m_data = np.array([1., 0.99912, 0.97188, 0.78643, 0.1])

m = interp1d(t_data, m_data, 'cubic')
m_prime = m._spline.derivative(nu=1)

a, b = 0.78, 0.1
def dvdt(t, v):
    return -a - b * v**2 / m(t) - m_prime(t) / m(t)

sol = solve_ivp(dvdt, [1e-4, 1], y0=[0], t_eval=np.linspace(1e-4, 1, 1000))
```

## interp2d — 2D Surface Interpolation

For data defined on a 2D grid, `interp2d` constructs a smooth surface interpolant:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# Scattered data on a 5×5 grid
x = np.array([0., 0.25, 0.5, 0.75, 1.] * 5)
y = np.repeat([0., 0.25, 0.5, 0.75, 1.], 5)
z = x**2 + y**2  # z = x² + y²

f = interp2d(x, y, z, kind='cubic')

# Evaluate on a fine grid
x_fine = np.linspace(0, 1, 100)
y_fine = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x_fine, y_fine)
Z = f(x_fine, y_fine)

fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, alpha=0.8)
for xx, yy, zz in zip(x, y, z):
    ax.plot(xx, yy, zz, 'or')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
```

### Financial Application

2D interpolation is used extensively in quantitative finance for constructing volatility surfaces from discrete option market data (strike × maturity grid), interpolating yield curve surfaces across tenors and dates, and building smooth forward rate surfaces for interest rate modeling.

## Summary

`scipy.interpolate` provides spline-based interpolation that complements NumPy's polynomial fitting. Use `interp1d` for 1D curve interpolation and `interp2d` for 2D surface construction. The resulting callable objects integrate seamlessly with `scipy.integrate.quad` and `scipy.integrate.solve_ivp`.

---

## Runnable Example: `scipy_interpolation_2d.py`

```python
"""
2D Surface Interpolation with scipy.interpolate
================================================
Level: Intermediate
Topics: interp2d, 3D surface plots, grid interpolation,
        meshgrid, surface visualization

This module demonstrates 2D interpolation for constructing smooth
surfaces from scattered data points — applicable to volatility
surfaces and yield curve grids in financial mathematics.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d

# =============================================================================
# SECTION 1: Create Sample Data on a Regular Grid
# =============================================================================

if __name__ == "__main__":
    """
    In practice, market data often comes on a discrete grid:
    - Options: strike prices × maturities
    - Bonds: tenors × dates
    - Rates: maturities × currencies

    Here we use z = x² + y² as a known function to verify interpolation.
    """

    # 5×5 grid of known data points
    x = np.array([0., 0.25, 0.5, 0.75, 1.,
                  0., 0.25, 0.5, 0.75, 1.,
                  0., 0.25, 0.5, 0.75, 1.,
                  0., 0.25, 0.5, 0.75, 1.,
                  0., 0.25, 0.5, 0.75, 1.])

    y = np.array([0., 0., 0., 0., 0.,
                  0.25, 0.25, 0.25, 0.25, 0.25,
                  0.5, 0.5, 0.5, 0.5, 0.5,
                  0.75, 0.75, 0.75, 0.75, 0.75,
                  1., 1., 1., 1., 1.])

    z = np.array([0., 0.0625, 0.25, 0.5625, 1.,
                  0.0625, 0.125, 0.3125, 0.625, 1.0625,
                  0.25, 0.3125, 0.5, 0.8125, 1.25,
                  0.5625, 0.625, 0.8125, 1.125, 1.5625,
                  1., 1.0625, 1.25, 1.5625, 2.])

    print("=" * 60)
    print("2D Surface Interpolation")
    print("=" * 60)
    print(f"Data points: {len(x)}")
    print(f"Grid: 5×5 = 25 points")
    print()

    # =============================================================================
    # SECTION 2: Build the Interpolant
    # =============================================================================

    f = interp2d(x, y, z, kind='cubic')

    # =============================================================================
    # SECTION 3: Evaluate on Fine Grid
    # =============================================================================

    x_fine = np.linspace(0, 1, 100)
    y_fine = np.linspace(0, 1, 100)
    X, Y = np.meshgrid(x_fine, y_fine)
    Z = f(x_fine, y_fine)  # Returns (100, 100) array

    print(f"Fine grid: {Z.shape[0]}×{Z.shape[1]} = {Z.size} points")
    print(f"Interpolation range: x=[{x_fine.min():.1f}, {x_fine.max():.1f}], "
          f"y=[{y_fine.min():.1f}, {y_fine.max():.1f}]")
    print()

    # =============================================================================
    # SECTION 4: Verify Against Known Function
    # =============================================================================

    Z_exact = X**2 + Y**2
    max_error = np.max(np.abs(Z - Z_exact))
    print(f"Maximum interpolation error: {max_error:.6e}")
    print()

    # =============================================================================
    # SECTION 5: 3D Visualization
    # =============================================================================

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})

    # Interpolated surface
    ax.plot_surface(X, Y, Z, alpha=0.8, cmap='viridis')

    # Original data points
    for xx, yy, zz in zip(x, y, z):
        ax.plot(xx, yy, zz, 'or', markersize=5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('2D Cubic Interpolation: Surface from 25 Data Points')
    plt.tight_layout()
    plt.show()

    # =============================================================================
    # SECTION 6: Financial Application — Volatility Surface
    # =============================================================================
    """
    In practice, a volatility surface is constructed from
    implied volatilities at discrete (strike, maturity) pairs.
    The interp2d function fills in the gaps, producing a smooth
    surface that can be queried at any (strike, maturity) combination.

    Example: If we have implied vols at strikes [90, 95, 100, 105, 110]
    and maturities [1M, 3M, 6M, 1Y], interp2d gives us vols at
    any intermediate strike and maturity.
    """

    print("=" * 60)
    print("Application: Volatility Surface (Simulated)")
    print("=" * 60)

    # Simulated implied volatility data
    strikes = np.array([90, 95, 100, 105, 110])
    maturities = np.array([0.083, 0.25, 0.5, 1.0])  # In years

    # Simulated smile: higher vol at extremes, lower at ATM
    S, M = np.meshgrid(strikes, maturities)
    vol_data = 0.20 + 0.001 * (S - 100)**2 + 0.05 / np.sqrt(M)

    # Build interpolant
    vol_surface = interp2d(S.ravel(), M.ravel(), vol_data.ravel(), kind='cubic')

    # Query at non-grid points
    strike_query = 97.5
    maturity_query = 0.375
    vol_interp = vol_surface(strike_query, maturity_query)[0]
    print(f"Implied vol at K={strike_query}, T={maturity_query}Y: {vol_interp:.4f}")

    print("\nDone!")
```

---

## Exercises

**Exercise 1.**
Create sample data `x = [0, 1, 2, 3, 4, 5]` and `y = [0, 0.8, 0.9, 0.1, -0.8, -1.0]`. Build both a linear and a cubic `interp1d` interpolant. Evaluate both at `x_fine = np.linspace(0, 5, 100)` and print the maximum difference between the linear and cubic interpolations.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy.interpolate import interp1d

        x = np.array([0, 1, 2, 3, 4, 5], dtype=float)
        y = np.array([0, 0.8, 0.9, 0.1, -0.8, -1.0])

        f_linear = interp1d(x, y, kind='linear')
        f_cubic = interp1d(x, y, kind='cubic')

        x_fine = np.linspace(0, 5, 100)
        y_linear = f_linear(x_fine)
        y_cubic = f_cubic(x_fine)

        max_diff = np.max(np.abs(y_linear - y_cubic))
        print(f"Max difference between linear and cubic: {max_diff:.4f}")

---

**Exercise 2.**
Given tabulated data representing a probability density, use `interp1d` with `kind='cubic'` and `scipy.integrate.quad` to compute the mean of the distribution:

```python
x = np.array([0, 1, 2, 3, 4, 5])
pdf = np.array([0.0, 0.2, 0.5, 0.2, 0.1, 0.0])
```

Compute `mean = integral(x * f(x)) / integral(f(x))` over `[0, 5]`.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy.interpolate import interp1d
        from scipy.integrate import quad

        x = np.array([0, 1, 2, 3, 4, 5], dtype=float)
        pdf = np.array([0.0, 0.2, 0.5, 0.2, 0.1, 0.0])

        f = interp1d(x, pdf, kind='cubic')

        numerator = quad(lambda t: t * f(t), 0, 5)[0]
        denominator = quad(f, 0, 5)[0]
        mean = numerator / denominator
        print(f"Mean of distribution: {mean:.4f}")

---

**Exercise 3.**
Create a 5x5 grid of data points for `z = sin(x) * cos(y)` on `[0, pi] x [0, pi]`. Use `interp2d` with `kind='cubic'` to interpolate onto a 50x50 fine grid. Compute the maximum interpolation error by comparing with the true function values on the fine grid.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy.interpolate import interp2d

        x = np.linspace(0, np.pi, 5)
        y = np.linspace(0, np.pi, 5)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)

        f = interp2d(x, y, Z, kind='cubic')

        x_fine = np.linspace(0, np.pi, 50)
        y_fine = np.linspace(0, np.pi, 50)
        Z_interp = f(x_fine, y_fine)

        Xf, Yf = np.meshgrid(x_fine, y_fine)
        Z_exact = np.sin(Xf) * np.cos(Yf)

        max_error = np.max(np.abs(Z_interp - Z_exact))
        print(f"Max interpolation error: {max_error:.6f}")
