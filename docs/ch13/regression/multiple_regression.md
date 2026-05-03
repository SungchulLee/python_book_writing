# Multiple Regression Concepts

Simple linear regression uses a single predictor to explain a response variable.
In practice, outcomes depend on several factors simultaneously. Multiple regression
extends the linear framework to $p$ predictors, allowing us to estimate the effect
of each predictor while controlling for the others. This page presents the matrix
formulation, the OLS solution, and the key diagnostics that arise when moving
beyond a single predictor.

!!! tip "Mental Model"
    Multiple regression is simple regression scaled up: instead of one slope, you have $p$ slopes -- one per predictor. Each coefficient measures the effect of its predictor while holding all others constant. The matrix formulation $\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top \mathbf{y}$ is the universal OLS formula that works regardless of how many predictors you have.

---

## The Matrix Model

With $n$ observations and $p$ predictors, the multiple regression model is

$$
\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}
$$

where

- $\mathbf{y}$ is the $n \times 1$ response vector
- $\mathbf{X}$ is the $n \times (p+1)$ design matrix (including a column of ones for the intercept)
- $\boldsymbol{\beta} = (\beta_0, \beta_1, \dots, \beta_p)^\top$ is the $(p+1) \times 1$ parameter vector
- $\boldsymbol{\varepsilon}$ is the $n \times 1$ error vector with $\mathbb{E}[\boldsymbol{\varepsilon}] = \mathbf{0}$ and $\operatorname{Cov}(\boldsymbol{\varepsilon}) = \sigma^2 \mathbf{I}_n$

Each row of $\mathbf{X}$ has the form $(1, x_{i1}, x_{i2}, \dots, x_{ip})$, so the
model for the $i$-th observation reads

$$
y_i = \beta_0 + \beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_p x_{ip} + \varepsilon_i
$$

## Normal Equations and OLS Estimator

The OLS estimator minimizes $\|\mathbf{y} - \mathbf{X}\boldsymbol{\beta}\|^2$. Setting
the gradient to zero produces the normal equations

$$
\mathbf{X}^\top \mathbf{X} \hat{\boldsymbol{\beta}} = \mathbf{X}^\top \mathbf{y}
$$

When $\mathbf{X}^\top \mathbf{X}$ is invertible (full column rank), the unique solution is

$$
\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top \mathbf{X})^{-1} \mathbf{X}^\top \mathbf{y}
$$

The fitted values and residuals are

$$
\hat{\mathbf{y}} = \mathbf{X}\hat{\boldsymbol{\beta}} = \mathbf{H}\mathbf{y}, \quad \hat{\boldsymbol{\varepsilon}} = \mathbf{y} - \hat{\mathbf{y}} = (\mathbf{I} - \mathbf{H})\mathbf{y}
$$

where $\mathbf{H} = \mathbf{X}(\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top$ is
the hat matrix.

## Computing OLS with NumPy

The normal equation approach can be implemented directly, but using `numpy.linalg.lstsq`
is numerically more stable because it avoids forming $\mathbf{X}^\top\mathbf{X}$ explicitly.

```python
import numpy as np

# Design matrix: 3 predictors + intercept column
X = np.array([
    [1, 2.0, 3.0, 1.5],
    [1, 4.0, 1.0, 2.3],
    [1, 3.0, 5.0, 3.1],
    [1, 5.0, 2.0, 4.0],
    [1, 1.0, 4.0, 2.8],
])
y = np.array([10.2, 12.1, 14.5, 15.8, 11.0])

# Solve via lstsq (preferred for numerical stability)
beta_hat, residuals, rank, sv = np.linalg.lstsq(X, y, rcond=None)

print("Estimated coefficients:", beta_hat)
```

!!! warning "Multicollinearity"
    When predictors are highly correlated, $\mathbf{X}^\top\mathbf{X}$ becomes
    nearly singular and the OLS estimates become unstable with large standard
    errors. Variance inflation factors (VIF) and condition numbers diagnose
    this problem. Regularization methods (Ridge, Lasso) provide remedies.

## Adjusted R-Squared

Adding more predictors to a model never decreases $R^2$, even if the new
predictors are irrelevant. The adjusted $R^2$ penalizes model complexity:

$$
R^2_{\text{adj}} = 1 - \frac{n - 1}{n - p - 1}(1 - R^2)
$$

where $n$ is the number of observations and $p$ is the number of predictors
(excluding the intercept). Unlike $R^2$, the adjusted version can decrease
when an uninformative predictor is added, making it more suitable for
comparing models with different numbers of predictors.

## Coefficient Interpretation

In multiple regression, each coefficient $\hat{\beta}_j$ represents the expected
change in $y$ for a one-unit increase in $x_j$, holding all other predictors
constant. This "all else equal" interpretation distinguishes multiple regression
from running separate simple regressions.

The standard error of each coefficient is

$$
\text{SE}(\hat{\beta}_j) = \hat{\sigma} \sqrt{[(\mathbf{X}^\top \mathbf{X})^{-1}]_{jj}}
$$

where $\hat{\sigma}^2 = \frac{1}{n - p - 1}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2$.
Individual $t$-tests for $H_0: \beta_j = 0$ use the statistic
$t_j = \hat{\beta}_j / \text{SE}(\hat{\beta}_j)$ with $n - p - 1$ degrees
of freedom.

## F-Test for Overall Significance

The $F$-test assesses whether the model as a whole explains significant
variation in $y$:

$$
H_0: \beta_1 = \beta_2 = \cdots = \beta_p = 0
$$

The test statistic is

$$
F = \frac{(\text{SS}_{\text{tot}} - \text{SS}_{\text{res}}) / p}{\text{SS}_{\text{res}} / (n - p - 1)}
$$

Under $H_0$, $F$ follows an $F$-distribution with $p$ and $n - p - 1$ degrees
of freedom.

## Assumptions

Multiple regression inherits the assumptions of simple linear regression,
extended to the multivariate setting:

1. **Linearity** -- $\mathbb{E}[y_i \mid \mathbf{x}_i]$ is linear in the parameters
2. **Independence** -- observations are independent
3. **Homoscedasticity** -- $\operatorname{Var}(\varepsilon_i) = \sigma^2$ for all $i$
4. **Normality** -- $\boldsymbol{\varepsilon} \sim \mathcal{N}(\mathbf{0}, \sigma^2\mathbf{I})$ (for exact inference)
5. **No perfect multicollinearity** -- $\mathbf{X}$ has full column rank

Violation of these assumptions affects the validity of standard errors, $t$-tests,
and $F$-tests. Residual analysis and diagnostic plots help assess these conditions.

## Summary

Multiple regression extends simple linear regression to $p$ predictors using the
matrix formulation $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$.
The OLS estimator $\hat{\boldsymbol{\beta}} = (\mathbf{X}^\top\mathbf{X})^{-1}\mathbf{X}^\top\mathbf{y}$
provides the best linear unbiased estimates under the Gauss-Markov conditions. Adjusted
$R^2$ and the $F$-test offer tools for model comparison and overall significance testing.

---

## Exercises

**Exercise 1.**
Create a design matrix with 3 predictors and 50 observations. Generate $Y = 2 + 3X_1 - X_2 + 0.5X_3 + \varepsilon$. Estimate the coefficients using `np.linalg.lstsq` and compare with the true values.

??? success "Solution to Exercise 1"

        import numpy as np

        np.random.seed(42)
        n = 50
        X123 = np.random.normal(size=(n, 3))
        y = 2 + 3*X123[:,0] - X123[:,1] + 0.5*X123[:,2] + np.random.normal(0, 1, n)
        X = np.column_stack([np.ones(n), X123])
        beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        print("Estimated:", np.round(beta, 3))
        print("True:      [2.000, 3.000, -1.000, 0.500]")

---

**Exercise 2.**
For the model in Exercise 1, compute $R^2$ and adjusted $R^2$. Add a fourth random (noise) predictor and show that $R^2$ increases but adjusted $R^2$ may decrease.

??? success "Solution to Exercise 2"

        import numpy as np

        np.random.seed(42)
        n = 50
        X123 = np.random.normal(size=(n, 3))
        y = 2 + 3*X123[:,0] - X123[:,1] + 0.5*X123[:,2] + np.random.normal(0, 1, n)

        def r2_adj(y, X_design):
            beta = np.linalg.lstsq(X_design, y, rcond=None)[0]
            yhat = X_design @ beta
            ss_res = np.sum((y - yhat)**2)
            ss_tot = np.sum((y - y.mean())**2)
            r2 = 1 - ss_res / ss_tot
            n, p = X_design.shape[0], X_design.shape[1] - 1
            adj = 1 - (n-1)/(n-p-1)*(1-r2)
            return r2, adj

        X3 = np.column_stack([np.ones(n), X123])
        r2_3, adj_3 = r2_adj(y, X3)

        noise = np.random.normal(size=(n, 1))
        X4 = np.column_stack([X3, noise])
        r2_4, adj_4 = r2_adj(y, X4)

        print(f"3 predictors: R2={r2_3:.4f}, Adj R2={adj_3:.4f}")
        print(f"4 predictors: R2={r2_4:.4f}, Adj R2={adj_4:.4f}")

---

**Exercise 3.**
Construct the F-statistic for overall significance of the model from Exercise 1. Compare with the critical value from `stats.f.ppf(0.95, p, n-p-1)` and verify using the p-value.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        n, p = 50, 3
        X123 = np.random.normal(size=(n, p))
        y = 2 + 3*X123[:,0] - X123[:,1] + 0.5*X123[:,2] + np.random.normal(0, 1, n)
        X = np.column_stack([np.ones(n), X123])
        beta = np.linalg.lstsq(X, y, rcond=None)[0]
        yhat = X @ beta
        ss_res = np.sum((y - yhat)**2)
        ss_tot = np.sum((y - y.mean())**2)
        F = ((ss_tot - ss_res)/p) / (ss_res/(n-p-1))
        p_val = 1 - stats.f.cdf(F, p, n-p-1)
        print(f"F = {F:.4f}, p = {p_val:.6f}")
