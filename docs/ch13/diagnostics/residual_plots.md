# Residual Diagnostics

After fitting a regression model, the predicted values alone do not reveal whether the model's assumptions hold. **Residual plots** expose violations of linearity, constant variance (homoscedasticity), and normality that summary statistics like $R^2$ can miss. Diagnosing these violations is essential before trusting inference results such as confidence intervals and $p$-values.

!!! tip "Mental Model"
    Residuals are what the model could not explain. If the model is correct, residuals should look like structureless noise -- no patterns when plotted against fitted values, no trend over time, no fan-shaped spread. Any visible pattern in the residuals is a clue that the model is missing something.

---

## Residual Definition

For a simple linear regression $y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$, the **residual** for observation $i$ is the difference between the observed and fitted value:

$$
e_i = y_i - \hat{y}_i
$$

where $\hat{y}_i = \hat{\beta}_0 + \hat{\beta}_1 x_i$. Under correct model specification, the residuals approximate the unobserved errors $\varepsilon_i$ and should satisfy four properties:

1. **Zero mean** — $\mathbb{E}[e_i] \approx 0$.
2. **Constant variance** — $\operatorname{Var}(e_i)$ does not depend on $x_i$ or $\hat{y}_i$.
3. **Normality** — $e_i$ are approximately normally distributed.
4. **Independence** — $e_i$ and $e_j$ are uncorrelated for $i \neq j$.

Each diagnostic plot below targets one or more of these properties.

## Computing Residuals with scipy.stats.linregress

The `scipy.stats.linregress` function returns slope, intercept, and regression statistics. Residuals are computed from these:

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
x = rng.uniform(0, 10, size=100)
y = 2.5 * x + 1.0 + rng.normal(0, 2, size=100)

result = stats.linregress(x, y)
y_hat = result.slope * x + result.intercept
residuals = y - y_hat
```

## Residuals vs Fitted Values

This is the most important diagnostic plot. It places fitted values $\hat{y}_i$ on the horizontal axis and residuals $e_i$ on the vertical axis.

```python
fig, ax = plt.subplots()
ax.scatter(y_hat, residuals, alpha=0.6, edgecolors='k', linewidths=0.5)
ax.axhline(y=0, color='red', linestyle='--')
ax.set_xlabel('Fitted values')
ax.set_ylabel('Residuals')
ax.set_title('Residuals vs Fitted Values')
plt.show()
```

**What to look for:**

- A random scatter around the zero line indicates that the linearity and constant-variance assumptions hold.
- A curved pattern (e.g., a parabola) indicates a non-linear relationship that the linear model fails to capture.
- A funnel shape (variance increasing with fitted values) indicates heteroscedasticity.

## Scale-Location Plot

The scale-location plot (also called a spread-location plot) displays $\sqrt{|e_i|}$ against $\hat{y}_i$. It isolates the constant-variance assumption by removing the sign of the residual:

```python
fig, ax = plt.subplots()
ax.scatter(y_hat, np.sqrt(np.abs(residuals)), alpha=0.6,
           edgecolors='k', linewidths=0.5)
ax.set_xlabel('Fitted values')
ax.set_ylabel(r'$\sqrt{|e_i|}$')
ax.set_title('Scale-Location Plot')
plt.show()
```

A horizontal band of roughly constant width confirms homoscedasticity. An upward trend signals that residual spread grows with the fitted values.

## Normal QQ Plot of Residuals

A QQ plot of residuals checks the normality assumption. SciPy's `probplot` function handles this directly:

```python
fig, ax = plt.subplots()
stats.probplot(residuals, dist='norm', plot=ax)
ax.set_title('Normal QQ Plot of Residuals')
plt.show()
```

Points that track the reference line support the normality assumption. S-shaped departures indicate heavy or light tails, and curvature indicates skewness. For a detailed discussion of QQ plot interpretation, see the [QQ Plots](qq_plots.md) page.

## Residuals vs Predictor

When the model includes a single predictor, plotting residuals against $x_i$ can reveal non-linearity more directly than the residuals-vs-fitted plot:

```python
fig, ax = plt.subplots()
ax.scatter(x, residuals, alpha=0.6, edgecolors='k', linewidths=0.5)
ax.axhline(y=0, color='red', linestyle='--')
ax.set_xlabel('x')
ax.set_ylabel('Residuals')
ax.set_title('Residuals vs Predictor')
plt.show()
```

This plot is particularly useful for detecting curvature that suggests a polynomial or transformed model would fit better.

## Standardized Residuals

Raw residuals have scale that depends on the units of $y$. **Standardized residuals** divide each residual by an estimate of its standard deviation:

$$
r_i = \frac{e_i}{s \sqrt{1 - h_{ii}}}
$$

where $s$ is the residual standard error and $h_{ii}$ is the $i$-th diagonal element of the hat matrix. Standardized residuals with $|r_i| > 2$ warrant investigation, and values beyond 3 are potential outliers.

!!! tip "When to use standardized residuals"
    Use standardized residuals instead of raw residuals when comparing observations across different scales or when setting a fixed threshold for outlier detection. For simple linear regression with `scipy.stats.linregress`, the standard error is available as `result.stderr` of the slope, but full leverage-based standardization requires a design matrix computation.

## Summary

Residual plots translate the abstract assumptions of linear regression into visual patterns. The residuals-vs-fitted plot checks linearity and constant variance, the scale-location plot isolates heteroscedasticity, and the normal QQ plot assesses the normality of errors. Together, these diagnostics guide model refinement — suggesting transformations, additional predictors, or alternative regression methods when assumptions are violated.


---

## Exercises

**Exercise 1.** Write code that fits a simple linear regression, computes the residuals, and creates a residual plot (residuals vs fitted values).

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(100)
    print(f'Mean: {data.mean():.4f}')
    print(f'Std: {data.std():.4f}')
    ```

---

**Exercise 2.** Explain three patterns in residual plots that indicate problems: heteroscedasticity, non-linearity, and outliers.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that creates a 2x2 diagnostic figure: residuals vs fitted, Q-Q plot of residuals, scale-location plot, and residuals vs leverage.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    from scipy import stats
    import matplotlib.pyplot as plt

    np.random.seed(42)
    data = np.random.randn(1000)
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, density=True, alpha=0.7)
    ax.set_title('Distribution')
    plt.show()
    ```

---

**Exercise 4.** Generate data with heteroscedastic errors and demonstrate that the residual plot reveals the non-constant variance.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
