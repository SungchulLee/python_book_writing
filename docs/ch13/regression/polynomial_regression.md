# Polynomial Regression

Many real-world relationships are not well described by a straight line. A
chemical reaction rate might rise and then plateau, or a projectile's height
follows a parabolic arc. Polynomial regression captures these curved
relationships by adding powers of the predictor to the model. Despite the
nonlinear shape of the fitted curve, polynomial regression is a special case
of multiple linear regression, so the entire OLS machinery applies unchanged.

!!! tip "Mental Model"
    Polynomial regression fits a curve by treating $x, x^2, x^3, \ldots$ as separate predictors and running ordinary linear regression on them. The curve looks nonlinear in $x$, but the math is identical to multiple regression. The danger is overfitting: a degree-$n$ polynomial passes through $n+1$ points exactly, so high-degree models memorize noise instead of learning the trend.

---

## The Polynomial Model

A polynomial regression of degree $d$ models the response as

$$
y_i = \beta_0 + \beta_1 x_i + \beta_2 x_i^2 + \cdots + \beta_d x_i^d + \varepsilon_i
$$

This is equivalent to multiple regression with derived predictors
$z_1 = x$, $z_2 = x^2$, $\dots$, $z_d = x^d$. The design matrix becomes
the Vandermonde matrix

$$
\mathbf{X} = \begin{pmatrix} 1 & x_1 & x_1^2 & \cdots & x_1^d \\ 1 & x_2 & x_2^2 & \cdots & x_2^d \\ \vdots & \vdots & \vdots & \ddots & \vdots \\ 1 & x_n & x_n^2 & \cdots & x_n^d \end{pmatrix}
$$

The OLS estimator is the same as in multiple regression:

$$
\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{y}
$$

## Fitting with NumPy

NumPy provides `numpy.polyfit` for polynomial fitting and `numpy.polynomial.polynomial.polyfit`
for the same task with a different coefficient ordering convention.

```python
import numpy as np

# Sample data with a quadratic relationship
x = np.array([1, 2, 3, 4, 5, 6, 7, 8])
y = np.array([2.5, 6.2, 11.0, 17.1, 24.8, 33.9, 44.2, 56.1])

# Fit degree-2 polynomial: y = c2*x^2 + c1*x + c0
coeffs = np.polyfit(x, y, deg=2)
print(f"Coefficients (highest to lowest degree): {coeffs}")

# Evaluate the fitted polynomial
p = np.poly1d(coeffs)
y_hat = p(x)
```

!!! tip "Vandermonde matrix approach"
    For explicit control, construct the design matrix with `numpy.vander`
    and solve via `numpy.linalg.lstsq`:
    ```python
    V = np.vander(x, N=3, increasing=True)
    beta, _, _, _ = np.linalg.lstsq(V, y, rcond=None)
    ```

## Degree Selection and Overfitting

Choosing the polynomial degree $d$ involves a bias-variance trade-off:

- **Too low** ($d$ small): underfitting. The model cannot capture the true
  curvature, leading to high bias.
- **Too high** ($d$ large): overfitting. The model fits noise in the training
  data, leading to high variance and poor generalization.

A polynomial of degree $n - 1$ passes exactly through all $n$ data points
(interpolation), but this perfect fit almost always generalizes poorly.

Practical criteria for selecting $d$ include:

- **Adjusted $R^2$**: penalizes additional parameters
- **Cross-validation**: evaluates prediction error on held-out data
- **Information criteria**: AIC and BIC balance fit quality against model complexity

## Numerical Conditioning

As the degree increases, the columns of the Vandermonde matrix become
increasingly correlated, making $\mathbf{X}^\top\mathbf{X}$ ill-conditioned.
The condition number grows rapidly with $d$, causing numerical instability
in the OLS solution.

Two remedies are common:

1. **Centering and scaling**: replace $x$ with $(x - \bar{x})/s_x$ before
   forming the powers. This reduces correlation among columns.
2. **Orthogonal polynomials**: use a basis of orthogonal polynomials (e.g.,
   Legendre or Chebyshev) so that $\mathbf{X}^\top\mathbf{X}$ is diagonal
   or nearly so.

```python
# Centering and scaling before polynomial fit
x_centered = (x - x.mean()) / x.std()
coeffs_stable = np.polyfit(x_centered, y, deg=4)
```

!!! warning "High-degree polynomial pitfalls"
    Polynomials of degree $d \geq 5$ often exhibit Runge's phenomenon: large
    oscillations near the boundaries of the data range. Piecewise polynomials
    (splines) are generally preferred for flexible curve fitting.

## Comparison with Multiple Regression

| Aspect                  | Multiple Regression           | Polynomial Regression              |
|-------------------------|-------------------------------|------------------------------------|
| Predictors              | Multiple independent variables | Powers of a single variable        |
| Design matrix           | Observed features              | Vandermonde matrix                 |
| Interpretation          | Each coefficient = partial effect | Coefficients lack simple interpretation |
| Multicollinearity risk  | Depends on data                | Inherent (powers are correlated)   |

## Summary

Polynomial regression extends simple linear regression by including powers of
the predictor as additional features. The model remains linear in the parameters,
so OLS applies directly. The key challenge is choosing the polynomial degree:
too low produces underfitting, too high produces overfitting and numerical
instability. Centering, scaling, and orthogonal polynomial bases help manage
conditioning issues.

---

## Exercises

**Exercise 1.**
Fit polynomials of degree 1, 2, and 3 to the data $x = [1,...,10]$, $y = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]$ (which is $x^2$). Compare the coefficients and identify which degree recovers the true relationship.

??? success "Solution to Exercise 1"

        import numpy as np

        x = np.arange(1, 11, dtype=float)
        y = x ** 2

        for deg in [1, 2, 3]:
            coeffs = np.polyfit(x, y, deg)
            print(f"Degree {deg}: {np.round(coeffs, 4)}")

---

**Exercise 2.**
Demonstrate overfitting: generate 10 noisy samples from $y = \sin(x)$ and fit polynomials of degree 2, 5, and 9. Plot each fit and show how the degree-9 polynomial passes through all points but oscillates wildly.

??? success "Solution to Exercise 2"

        import numpy as np
        import matplotlib.pyplot as plt

        np.random.seed(42)
        x = np.linspace(0, 2*np.pi, 10)
        y = np.sin(x) + np.random.normal(0, 0.2, 10)
        x_fine = np.linspace(0, 2*np.pi, 200)

        for deg in [2, 5, 9]:
            p = np.polyfit(x, y, deg)
            plt.plot(x_fine, np.polyval(p, x_fine), label=f'deg {deg}')
        plt.scatter(x, y, c='black', zorder=5)
        plt.legend()
        plt.title('Polynomial Overfitting')
        plt.show()

---

**Exercise 3.**
Fit a degree-3 polynomial to 50 samples from $y = 2x - 0.5x^2 + 0.1x^3 + \varepsilon$ with $\varepsilon \sim N(0, 3)$. Compare fitted coefficients with true values. Compute $R^2$ for degree 1, 2, 3, and 4 fits.

??? success "Solution to Exercise 3"

        import numpy as np

        np.random.seed(42)
        x = np.random.uniform(0, 5, 50)
        y = 2*x - 0.5*x**2 + 0.1*x**3 + np.random.normal(0, 3, 50)

        coeffs = np.polyfit(x, y, 3)
        print(f"Fitted: {np.round(coeffs, 4)}")
        print(f"True:   [0.1, -0.5, 2.0, 0.0]")

        for deg in [1, 2, 3, 4]:
            p = np.polyfit(x, y, deg)
            yhat = np.polyval(p, x)
            r2 = 1 - np.sum((y - yhat)**2) / np.sum((y - y.mean())**2)
            print(f"Degree {deg}: R2 = {r2:.4f}")
