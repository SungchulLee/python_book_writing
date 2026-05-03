# Logistic Regression Preview

Linear regression models a continuous response, but many problems involve binary
outcomes: pass or fail, default or repay, click or ignore. Fitting a straight line
to binary data produces predictions outside the $[0, 1]$ range and violates the
constant-variance assumption. Logistic regression resolves these issues by modeling
the probability of the positive class through the sigmoid function.

This page introduces the core ideas of logistic regression as a preview. Full
treatment with regularization and multiclass extensions belongs to dedicated
machine learning resources.

!!! tip "Mental Model"
    Logistic regression wraps a linear model inside a sigmoid function to squeeze predictions into the $(0, 1)$ probability range. The linear combination $\beta_0 + \beta_1 x$ controls the log-odds; the sigmoid converts log-odds into a probability. The result is a classification boundary that is linear in the feature space but nonlinear in probability.

---

## The Sigmoid Function

The sigmoid (logistic) function maps any real number to the interval $(0, 1)$:

$$
\sigma(z) = \frac{1}{1 + e^{-z}}
$$

Key properties of the sigmoid include:

- $\sigma(0) = 0.5$
- $\lim_{z \to \infty} \sigma(z) = 1$ and $\lim_{z \to -\infty} \sigma(z) = 0$
- Symmetry: $\sigma(-z) = 1 - \sigma(z)$
- Derivative: $\sigma'(z) = \sigma(z)(1 - \sigma(z))$

## The Logistic Model

For a single predictor $x$, logistic regression models the probability that $Y = 1$ as

$$
P(Y = 1 \mid x) = \sigma(\beta_0 + \beta_1 x) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x)}}
$$

where $\beta_0$ is the intercept and $\beta_1$ is the slope parameter. Unlike
linear regression, the parameters do not directly give the change in the response
per unit change in $x$.

## Log-Odds Interpretation

Applying the logit transform (the inverse of the sigmoid) to both sides yields
a linear model in the log-odds:

$$
\log \frac{P(Y=1 \mid x)}{1 - P(Y=1 \mid x)} = \beta_0 + \beta_1 x
$$

The left side is the logarithm of the odds ratio. This shows that logistic
regression is a linear model in log-odds space. The coefficient $\beta_1$
represents the change in log-odds per unit increase in $x$, and $e^{\beta_1}$
gives the multiplicative change in the odds.

## Maximum Likelihood Estimation

Unlike OLS in linear regression, logistic regression estimates parameters by
maximizing the likelihood function. For independent observations
$\{(x_i, y_i)\}_{i=1}^n$ with $y_i \in \{0, 1\}$, the log-likelihood is

$$
\ell(\beta_0, \beta_1) = \sum_{i=1}^{n} \left[ y_i \log p_i + (1 - y_i) \log(1 - p_i) \right]
$$

where $p_i = \sigma(\beta_0 + \beta_1 x_i)$. There is no closed-form solution,
so numerical optimization methods (Newton-Raphson, gradient descent) are required.

## Fitting with SciPy

While dedicated libraries like `statsmodels` and `scikit-learn` provide
full-featured logistic regression, the core optimization can be performed
with `scipy.optimize.minimize`.

```python
import numpy as np
from scipy.optimize import minimize
from scipy.special import expit  # sigmoid function

# Example: study hours vs pass/fail
hours = np.array([1, 2, 3, 4, 5, 6, 7, 8])
passed = np.array([0, 0, 0, 0, 1, 1, 1, 1])

def neg_log_likelihood(params, x, y):
    b0, b1 = params
    p = expit(b0 + b1 * x)
    # Clip to avoid log(0)
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return -np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))

result = minimize(neg_log_likelihood, x0=[0, 0], args=(hours, passed))
b0_hat, b1_hat = result.x

print(f"Intercept: {b0_hat:.4f}")
print(f"Slope:     {b1_hat:.4f}")
```

!!! tip "scipy.special.expit"
    SciPy provides `expit` as a numerically stable implementation of the
    sigmoid function. Use it instead of writing `1 / (1 + np.exp(-z))`
    to avoid overflow warnings for large negative values of $z$.

## Decision Boundary

The model predicts $Y = 1$ when $P(Y = 1 \mid x) > 0.5$, which occurs when
$\beta_0 + \beta_1 x > 0$. The decision boundary is the value of $x$ where
the predicted probability equals 0.5:

$$
x^* = -\frac{\beta_0}{\beta_1}
$$

For the multivariate case with predictor vector $\mathbf{x}$, the decision
boundary becomes a hyperplane in feature space.

## Comparison with Linear Regression

| Aspect                | Linear Regression            | Logistic Regression             |
|-----------------------|------------------------------|---------------------------------|
| Response type         | Continuous                   | Binary (0 or 1)                 |
| Model output          | Predicted value $\hat{y}$    | Predicted probability $\hat{p}$ |
| Link function         | Identity                     | Logit (log-odds)                |
| Estimation method     | OLS (closed-form)            | MLE (iterative)                 |
| Loss function         | Sum of squared residuals     | Negative log-likelihood         |

## Summary

Logistic regression extends the linear modeling framework to binary outcomes
by applying the sigmoid function to a linear predictor. The parameters are
estimated by maximum likelihood rather than least squares, and the coefficients
are interpreted in terms of log-odds rather than direct changes in the response.
SciPy's `scipy.special.expit` and `scipy.optimize.minimize` provide the
building blocks for fitting the model from scratch.

---

## Exercises

**Exercise 1.**
Implement the sigmoid function and evaluate it at $z = -5, -2, 0, 2, 5$. Verify the symmetry property $\sigma(-z) = 1 - \sigma(z)$.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy.special import expit

        for z in [-5, -2, 0, 2, 5]:
            s = expit(z)
            s_neg = expit(-z)
            print(f"sigma({z:2d})={s:.4f}, sigma({-z:2d})={s_neg:.4f}, sum={s+s_neg:.4f}")

---

**Exercise 2.**
Fit a logistic regression using `scipy.optimize.minimize` on the data: hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], passed = [0, 0, 0, 0, 1, 0, 1, 1, 1, 1]. Find the decision boundary (the number of hours where $P(\text{pass}) = 0.5$).

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy.optimize import minimize
        from scipy.special import expit

        hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        passed = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])

        def neg_ll(params, x, y):
            p = expit(params[0] + params[1] * x)
            p = np.clip(p, 1e-12, 1 - 1e-12)
            return -np.sum(y * np.log(p) + (1-y) * np.log(1-p))

        result = minimize(neg_ll, x0=[0, 0], args=(hours, passed))
        b0, b1 = result.x
        boundary = -b0 / b1
        print(f"b0={b0:.4f}, b1={b1:.4f}")
        print(f"Decision boundary: {boundary:.2f} hours")

---

**Exercise 3.**
Plot the fitted logistic curve from Exercise 2 alongside the data points. Mark the decision boundary on the plot.

??? success "Solution to Exercise 3"

        import numpy as np
        import matplotlib.pyplot as plt
        from scipy.optimize import minimize
        from scipy.special import expit

        hours = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        passed = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])

        def neg_ll(params, x, y):
            p = np.clip(expit(params[0] + params[1]*x), 1e-12, 1-1e-12)
            return -np.sum(y*np.log(p) + (1-y)*np.log(1-p))

        res = minimize(neg_ll, x0=[0, 0], args=(hours, passed))
        b0, b1 = res.x
        x_plot = np.linspace(0, 11, 200)
        plt.plot(x_plot, expit(b0 + b1*x_plot), 'b-', label='Logistic curve')
        plt.scatter(hours, passed, c='red', zorder=5, label='Data')
        plt.axvline(-b0/b1, ls='--', color='gray', label=f'Boundary={-b0/b1:.1f}')
        plt.xlabel('Hours')
        plt.ylabel('P(Pass)')
        plt.legend()
        plt.show()
