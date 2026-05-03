# Regularization Preview (Ridge, Lasso)

When a linear model has many predictors or correlated features, OLS estimates
can become unstable and overfit the training data. Regularization addresses this
by adding a penalty term to the OLS objective, shrinking coefficients toward
zero. This controlled shrinkage introduces a small bias but can substantially
reduce variance, often improving prediction on new data.

This page introduces the two most common regularization methods -- Ridge and
Lasso -- as a preview. Full treatment with cross-validation tuning and elastic
net belongs to dedicated machine learning resources.

!!! tip "Mental Model"
    Regularization adds a "penalty for complexity" to the OLS objective: Ridge penalizes large coefficients with $\lambda \sum \beta_j^2$ (shrinks toward zero but never to zero), while Lasso uses $\lambda \sum |\beta_j|$ (can shrink coefficients exactly to zero, performing feature selection). The tuning parameter $\lambda$ controls how much you trade fit for simplicity.

---

## The Overfitting Problem

Recall the OLS objective for $p$ predictors:

$$
\hat{\boldsymbol{\beta}}_{\text{OLS}} = \arg\min_{\boldsymbol{\beta}} \sum_{i=1}^{n}(y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2
$$

When $p$ is large relative to $n$, or when predictors are highly correlated,
OLS produces coefficients with large magnitudes that cancel each other. The
fitted model captures noise rather than signal, and predictions on new data
deteriorate.

## Ridge Regression (L2 Penalty)

Ridge regression adds the squared $L^2$ norm of the coefficient vector as a
penalty:

$$
\hat{\boldsymbol{\beta}}_{\text{Ridge}} = \arg\min_{\boldsymbol{\beta}} \left\{ \sum_{i=1}^{n}(y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2 + \lambda \sum_{j=1}^{p} \beta_j^2 \right\}
$$

where $\lambda \geq 0$ is the regularization parameter. The closed-form solution is

$$
\hat{\boldsymbol{\beta}}_{\text{Ridge}} = (\mathbf{X}^\top \mathbf{X} + \lambda \mathbf{I})^{-1}\mathbf{X}^\top \mathbf{y}
$$

The addition of $\lambda \mathbf{I}$ to $\mathbf{X}^\top\mathbf{X}$ ensures the
matrix is invertible even when $\mathbf{X}$ does not have full column rank. As
$\lambda$ increases, the coefficients shrink toward zero but never reach exactly
zero.

!!! note "Intercept is not penalized"
    Standard practice excludes the intercept $\beta_0$ from the penalty.
    Predictors should be centered (and often standardized) before applying
    Ridge regression so that the penalty treats all coefficients equally.

## Lasso Regression (L1 Penalty)

Lasso regression replaces the squared penalty with the $L^1$ norm:

$$
\hat{\boldsymbol{\beta}}_{\text{Lasso}} = \arg\min_{\boldsymbol{\beta}} \left\{ \sum_{i=1}^{n}(y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2 + \lambda \sum_{j=1}^{p} |\beta_j| \right\}
$$

The $L^1$ penalty has a distinctive property: for sufficiently large $\lambda$,
some coefficients are driven exactly to zero. This makes Lasso a simultaneous
estimation and variable selection method.

Unlike Ridge, there is no closed-form solution for Lasso. The optimization
requires iterative algorithms such as coordinate descent.

## Comparing Ridge and Lasso

| Aspect                  | Ridge ($L^2$)                        | Lasso ($L^1$)                        |
|-------------------------|--------------------------------------|--------------------------------------|
| Penalty                 | $\lambda \sum \beta_j^2$             | $\lambda \sum \lvert\beta_j\rvert$   |
| Closed-form solution    | Yes                                  | No (iterative)                       |
| Feature selection       | No (coefficients shrink but remain nonzero) | Yes (some coefficients become exactly zero) |
| Correlated predictors   | Retains all, shares weight           | Tends to select one, drop the rest   |
| Geometric view          | Constraint region is a sphere        | Constraint region is a diamond       |

## The Role of Lambda

The regularization parameter $\lambda$ controls the bias-variance trade-off:

- $\lambda = 0$: no penalty, solution equals OLS
- $\lambda \to \infty$: all coefficients shrink to zero (intercept-only model)
- Optimal $\lambda$: balances fit quality against model complexity

Cross-validation is the standard method for choosing $\lambda$: fit the model
for a grid of $\lambda$ values and select the one that minimizes prediction
error on held-out folds.

## Computing Ridge with NumPy

The Ridge closed-form solution is straightforward to implement:

```python
import numpy as np

# Design matrix (centered, without intercept column for simplicity)
X = np.array([[1.0, 2.0], [3.0, 1.0], [2.0, 4.0],
              [5.0, 3.0], [4.0, 5.0]])
y = np.array([3.0, 5.0, 7.0, 10.0, 11.0])

lam = 1.0  # regularization parameter
p = X.shape[1]

beta_ridge = np.linalg.solve(X.T @ X + lam * np.eye(p), X.T @ y)
print(f"Ridge coefficients: {beta_ridge}")

# Compare with OLS
beta_ols = np.linalg.solve(X.T @ X, X.T @ y)
print(f"OLS coefficients:   {beta_ols}")
```

!!! warning "Standardize predictors"
    The penalty $\lambda \sum \beta_j^2$ depends on the scale of each
    predictor. If predictors are on different scales, Ridge and Lasso
    penalize them unequally. Always standardize predictors to zero mean
    and unit variance before applying regularization.

## Elastic Net

The elastic net combines both penalties:

$$
\hat{\boldsymbol{\beta}}_{\text{EN}} = \arg\min_{\boldsymbol{\beta}} \left\{ \sum_{i=1}^{n}(y_i - \mathbf{x}_i^\top \boldsymbol{\beta})^2 + \lambda_1 \sum_{j=1}^{p} |\beta_j| + \lambda_2 \sum_{j=1}^{p} \beta_j^2 \right\}
$$

This hybrid approach retains Lasso's variable selection ability while
handling correlated predictors more gracefully than Lasso alone.

## Summary

Regularization combats overfitting by penalizing large coefficients. Ridge
regression adds an $L^2$ penalty and shrinks coefficients smoothly toward
zero, while Lasso uses an $L^1$ penalty that can drive coefficients to
exactly zero, performing variable selection. The regularization parameter
$\lambda$ balances bias and variance, and is typically chosen by
cross-validation.

---

## Exercises

**Exercise 1.**
Generate a dataset with 20 observations and 15 predictors (more features than useful). Fit OLS and Ridge ($\lambda = 1$) using the closed-form solution. Compare the coefficient magnitudes (L2 norms).

??? success "Solution to Exercise 1"

        import numpy as np

        np.random.seed(42)
        n, p = 20, 15
        X = np.random.normal(size=(n, p))
        y = X[:, 0] + 0.5*X[:, 1] + np.random.normal(0, 1, n)

        beta_ols = np.linalg.lstsq(X, y, rcond=None)[0]
        lam = 1.0
        beta_ridge = np.linalg.solve(X.T @ X + lam * np.eye(p), X.T @ y)

        print(f"OLS L2 norm:   {np.linalg.norm(beta_ols):.4f}")
        print(f"Ridge L2 norm: {np.linalg.norm(beta_ridge):.4f}")

---

**Exercise 2.**
Vary $\lambda$ from 0.001 to 100 (logarithmic grid) for Ridge regression on the dataset from Exercise 1. Plot the L2 norm of the coefficient vector vs $\lambda$ to show the shrinkage path.

??? success "Solution to Exercise 2"

        import numpy as np
        import matplotlib.pyplot as plt

        np.random.seed(42)
        n, p = 20, 15
        X = np.random.normal(size=(n, p))
        y = X[:, 0] + 0.5*X[:, 1] + np.random.normal(0, 1, n)

        lambdas = np.logspace(-3, 2, 50)
        norms = []
        for lam in lambdas:
            beta = np.linalg.solve(X.T @ X + lam * np.eye(p), X.T @ y)
            norms.append(np.linalg.norm(beta))

        plt.semilogx(lambdas, norms)
        plt.xlabel('Lambda')
        plt.ylabel('L2 Norm of Coefficients')
        plt.title('Ridge Shrinkage Path')
        plt.show()

---

**Exercise 3.**
For a simple 2-predictor model with correlated features ($\rho = 0.95$), fit OLS and Ridge ($\lambda = 0.5$). Show that Ridge produces more stable (smaller magnitude) coefficients.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        n = 50
        data = stats.multivariate_normal.rvs(mean=[0,0], cov=[[1,0.95],[0.95,1]], size=n)
        X = data
        y = 2*X[:,0] + 3*X[:,1] + np.random.normal(0, 1, n)

        beta_ols = np.linalg.lstsq(X, y, rcond=None)[0]
        beta_ridge = np.linalg.solve(X.T @ X + 0.5*np.eye(2), X.T @ y)

        print(f"OLS:   {np.round(beta_ols, 3)}")
        print(f"Ridge: {np.round(beta_ridge, 3)}")
