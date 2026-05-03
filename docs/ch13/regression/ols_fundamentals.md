# Ordinary Least Squares Fundamentals

Ordinary least squares (OLS) is the most widely used method for estimating the
parameters of a linear regression model. The idea is intuitive: choose the
parameter values that make the fitted line as close as possible to the observed
data, where "closeness" is measured by the sum of squared vertical distances
from the data points to the line. This page develops the OLS framework from the
optimization problem through the solution, its statistical properties, and
practical computation.

!!! tip "Mental Model"
    OLS draws the line that minimizes the total squared vertical distance from each data point to the line. Squaring the distances penalizes large errors disproportionately and yields a smooth, differentiable objective with a unique closed-form solution. Under Gaussian errors, OLS is also the maximum likelihood estimator.

---

## The OLS Objective

Given $n$ observations $\{(x_i, y_i)\}_{i=1}^n$ and the model
$y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$, OLS seeks the values
$\hat{\beta}_0$ and $\hat{\beta}_1$ that minimize

$$
S(\beta_0, \beta_1) = \sum_{i=1}^{n} (y_i - \beta_0 - \beta_1 x_i)^2 = \sum_{i=1}^{n} e_i^2
$$

where $e_i = y_i - \beta_0 - \beta_1 x_i$ is the residual for the $i$-th
observation.

The choice of squared residuals (rather than absolute residuals) is not
arbitrary: it leads to a smooth, differentiable objective with a unique
closed-form solution and connects directly to maximum likelihood estimation
under Gaussian errors.

## Deriving the OLS Estimators

Setting the partial derivatives to zero yields two equations:

$$
\frac{\partial S}{\partial \beta_0} = -2\sum_{i=1}^{n}(y_i - \beta_0 - \beta_1 x_i) = 0
$$

$$
\frac{\partial S}{\partial \beta_1} = -2\sum_{i=1}^{n} x_i(y_i - \beta_0 - \beta_1 x_i) = 0
$$

From the first equation, $\hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}$.
Substituting into the second and solving for $\hat{\beta}_1$ gives

$$
\hat{\beta}_1 = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n}(x_i - \bar{x})^2}
$$

$$
\hat{\beta}_0 = \bar{y} - \hat{\beta}_1 \bar{x}
$$

The fitted line always passes through the point $(\bar{x}, \bar{y})$.

## Matrix Formulation

For $p$ predictors, the model in matrix form is $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$
and the OLS objective becomes

$$
S(\boldsymbol{\beta}) = (\mathbf{y} - \mathbf{X}\boldsymbol{\beta})^\top(\mathbf{y} - \mathbf{X}\boldsymbol{\beta})
$$

Taking the gradient and setting it to zero yields the normal equations

$$
\mathbf{X}^\top \mathbf{X} \hat{\boldsymbol{\beta}} = \mathbf{X}^\top \mathbf{y}
$$

with solution

$$
\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{y}
$$

provided $\mathbf{X}^\top \mathbf{X}$ is invertible (i.e., $\mathbf{X}$ has full
column rank).

## Statistical Properties

Under the Gauss-Markov conditions -- (1) linearity, (2) strict exogeneity
$\mathbb{E}[\varepsilon_i \mid \mathbf{X}] = 0$, (3) homoscedasticity, and
(4) no perfect multicollinearity -- the OLS estimator has the following properties.

**Unbiasedness.** The OLS estimator is unbiased:

$$
\mathbb{E}[\hat{\boldsymbol{\beta}}] = \boldsymbol{\beta}
$$

**Variance.** The covariance matrix of the OLS estimator is

$$
\operatorname{Cov}(\hat{\boldsymbol{\beta}}) = \sigma^2 (\mathbf{X}^\top \mathbf{X})^{-1}
$$

**Gauss-Markov Theorem.** Among all linear unbiased estimators of $\boldsymbol{\beta}$,
the OLS estimator has the smallest variance. That is, OLS is the Best Linear Unbiased
Estimator (BLUE).

!!! note "BLUE does not mean best overall"
    The Gauss-Markov theorem restricts the comparison to *linear* and *unbiased*
    estimators. Biased estimators such as Ridge regression can achieve lower
    mean squared error by trading a small bias for a larger reduction in variance.

## Residual Variance Estimator

The residual variance $\sigma^2$ is estimated by

$$
\hat{\sigma}^2 = \frac{1}{n - p - 1} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2 = \frac{\text{RSS}}{n - p - 1}
$$

where RSS is the residual sum of squares and $n - p - 1$ are the degrees of
freedom ($n$ observations minus $p + 1$ estimated parameters). The divisor
$n - p - 1$ instead of $n$ ensures unbiasedness of $\hat{\sigma}^2$.

## Computing OLS in Python

```python
import numpy as np
from scipy import stats

# Simple linear regression via linregress
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
y = np.array([2.1, 4.3, 5.8, 8.2, 9.7, 12.1, 13.8, 16.2])

result = stats.linregress(x, y)
print(f"Slope:     {result.slope:.4f}")
print(f"Intercept: {result.intercept:.4f}")

# Verify with the normal equations
X = np.column_stack([np.ones_like(x), x])
beta_hat = np.linalg.solve(X.T @ X, X.T @ y)
print(f"Normal equations: intercept={beta_hat[0]:.4f}, slope={beta_hat[1]:.4f}")
```

!!! tip "Numerical stability"
    The normal equations require inverting $\mathbf{X}^\top\mathbf{X}$, which
    amplifies round-off errors when predictors are correlated. In practice,
    use `numpy.linalg.lstsq` or a QR decomposition, which solve the least
    squares problem without forming the cross-product matrix.

## Geometric Interpretation

The fitted values $\hat{\mathbf{y}} = \mathbf{H}\mathbf{y}$ are the orthogonal
projection of $\mathbf{y}$ onto the column space of $\mathbf{X}$. The hat matrix

$$
\mathbf{H} = \mathbf{X}(\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top
$$

is an idempotent projection matrix ($\mathbf{H}^2 = \mathbf{H}$). The residual
vector $\hat{\boldsymbol{\varepsilon}} = (\mathbf{I} - \mathbf{H})\mathbf{y}$ is
orthogonal to the column space of $\mathbf{X}$, which means

$$
\mathbf{X}^\top \hat{\boldsymbol{\varepsilon}} = \mathbf{0}
$$

This orthogonality condition is equivalent to the normal equations and provides
the geometric justification for OLS: the residual vector is perpendicular to
every column of the design matrix.

## Summary

OLS minimizes the sum of squared residuals and produces the Best Linear Unbiased
Estimator under the Gauss-Markov conditions. The closed-form solution via the
normal equations generalizes to multiple predictors through the matrix formula
$\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$.
The geometric view reveals that OLS computes an orthogonal projection of the
response onto the column space of the design matrix.

---

## Exercises

**Exercise 1.**
Verify the OLS normal equations numerically: for data $x = [1, 2, 3, 4, 5]$ and $y = [2.3, 4.1, 5.8, 8.2, 9.9]$, construct the design matrix $\mathbf{X}$, compute $\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$, and verify that $\mathbf{X}^\top\hat{\boldsymbol{\varepsilon}} = \mathbf{0}$.

??? success "Solution to Exercise 1"

        import numpy as np

        x = np.array([1, 2, 3, 4, 5], dtype=float)
        y = np.array([2.3, 4.1, 5.8, 8.2, 9.9])
        X = np.column_stack([np.ones_like(x), x])
        beta = np.linalg.solve(X.T @ X, X.T @ y)
        residuals = y - X @ beta
        print(f"beta: {beta}")
        print(f"X'e = {X.T @ residuals}")

---

**Exercise 2.**
Compute the hat matrix $\mathbf{H}$ for the simple regression in Exercise 1. Verify that $\mathbf{H}$ is idempotent ($\mathbf{H}^2 = \mathbf{H}$) and that the diagonal elements (leverages) sum to $p + 1 = 2$.

??? success "Solution to Exercise 2"

        import numpy as np

        x = np.array([1, 2, 3, 4, 5], dtype=float)
        X = np.column_stack([np.ones_like(x), x])
        H = X @ np.linalg.solve(X.T @ X, X.T)
        print(f"H^2 == H: {np.allclose(H @ H, H)}")
        print(f"Sum of leverages: {np.trace(H):.1f} (expected 2)")

---

**Exercise 3.**
Generate 50 samples from $Y = 5 + 3X + \varepsilon$ and compute $\hat{\sigma}^2 = \text{RSS}/(n-2)$. Compare it with the true $\sigma^2 = 4$ (assuming $\varepsilon \sim N(0, 2)$). Verify unbiasedness by averaging over 1000 simulations.

??? success "Solution to Exercise 3"

        import numpy as np

        np.random.seed(42)
        sigma2_estimates = []
        for _ in range(1000):
            x = np.random.uniform(0, 10, 50)
            y = 5 + 3*x + np.random.normal(0, 2, 50)
            X = np.column_stack([np.ones_like(x), x])
            beta = np.linalg.lstsq(X, y, rcond=None)[0]
            resid = y - X @ beta
            sigma2_hat = np.sum(resid**2) / (50 - 2)
            sigma2_estimates.append(sigma2_hat)
        print(f"Mean sigma^2 estimate: {np.mean(sigma2_estimates):.4f} (true: 4)")
