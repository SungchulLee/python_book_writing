# Residual Analysis

After fitting a regression model, the natural question is: how well does the model describe the data? Raw goodness-of-fit statistics such as $R^2$ summarize overall fit, but they can hide systematic problems. Residual analysis examines the discrepancies between observed and predicted values to detect violations of model assumptions and guide model improvement.

This page defines residuals, introduces their key properties, and shows how standard diagnostic plots reveal common regression pathologies.

!!! tip "Mental Model"
    Residuals are the model's mistakes. If the model is correct, these mistakes should be random -- no patterns, no trends, no funneling. Plotting residuals against fitted values, predictors, or observation order reveals specific violations: curves mean missing nonlinearity, fans mean non-constant variance, and clusters mean missing variables.

---

## Definition of Residuals

In a regression model with $n$ observations, the **residual** for observation $i$ is the difference between the observed response $y_i$ and the fitted value $\hat{y}_i$:

$$
e_i = y_i - \hat{y}_i, \quad i = 1, 2, \ldots, n
$$

The fitted values come from the model $\hat{y}_i = \mathbf{x}_i^\top \hat{\boldsymbol{\beta}}$, where $\hat{\boldsymbol{\beta}}$ is the OLS estimate and $\mathbf{x}_i$ is the vector of predictors for observation $i$.

!!! warning "Residuals versus errors"
    The true **error** $\varepsilon_i = y_i - \mathbf{x}_i^\top \boldsymbol{\beta}$ involves the unknown population parameter $\boldsymbol{\beta}$, which is never observed. Residuals $e_i$ are the observable counterparts obtained by replacing $\boldsymbol{\beta}$ with $\hat{\boldsymbol{\beta}}$. Residual analysis uses $e_i$ as a proxy for the unobservable $\varepsilon_i$.

---

## Properties of OLS Residuals

Under the standard linear model $\mathbf{y} = \mathbf{X}\boldsymbol{\beta} + \boldsymbol{\varepsilon}$, the residual vector $\mathbf{e} = \mathbf{y} - \hat{\mathbf{y}}$ satisfies several useful properties.

**Zero mean.** The sum (and therefore the mean) of the OLS residuals is exactly zero whenever the model includes an intercept:

$$
\sum_{i=1}^{n} e_i = 0
$$

**Orthogonality.** The residual vector is orthogonal to every column of the design matrix $\mathbf{X}$:

$$
\mathbf{X}^\top \mathbf{e} = \mathbf{0}
$$

This follows directly from the OLS normal equations. As a consequence, the residuals are uncorrelated with the fitted values.

**Hat matrix representation.** Define the hat matrix $\mathbf{H} = \mathbf{X}(\mathbf{X}^\top \mathbf{X})^{-1}\mathbf{X}^\top$. Then the residuals can be written as:

$$
\mathbf{e} = (\mathbf{I} - \mathbf{H})\mathbf{y}
$$

The diagonal elements $h_{ii}$ of $\mathbf{H}$ are called **leverages** and measure how far each observation's predictor values lie from the center of the predictor space. High-leverage points have an outsized influence on the fitted model.

---

## Types of Residuals

Raw residuals $e_i$ are not directly comparable across observations because their variance depends on leverage. Several standardized forms address this.

### Standardized Residuals

Divide each residual by the estimated standard deviation of the residuals:

$$
r_i^{\text{std}} = \frac{e_i}{\hat{\sigma}}
$$

where $\hat{\sigma} = \sqrt{\text{RSS} / (n - p)}$ is the residual standard error, RSS is the residual sum of squares, and $p$ is the number of estimated parameters (including the intercept).

### Studentized Residuals (Internally Studentized)

Account for the fact that $\operatorname{Var}(e_i) = \sigma^2(1 - h_{ii})$ under the model assumptions:

$$
r_i = \frac{e_i}{\hat{\sigma}\sqrt{1 - h_{ii}}}
$$

These have approximately unit variance under the null hypothesis that the model is correct.

### Externally Studentized Residuals (Studentized Deleted Residuals)

Use a leave-one-out estimate $\hat{\sigma}_{(i)}$ that excludes observation $i$:

$$
t_i = \frac{e_i}{\hat{\sigma}_{(i)}\sqrt{1 - h_{ii}}}
$$

Under the model assumptions, $t_i$ follows a $t$-distribution with $n - p - 1$ degrees of freedom. This makes externally studentized residuals particularly useful for outlier detection because the test statistic is independent of the observation being tested.

---

## Diagnostic Plots

Residual plots translate abstract assumption checks into visual patterns. The four most common diagnostics are described below.

### Residuals versus Fitted Values

Plot $e_i$ (or $r_i$) on the vertical axis against $\hat{y}_i$ on the horizontal axis.

- **Ideal pattern:** a random scatter of points centered around zero with constant vertical spread.
- **Funnel shape** (spread increasing with $\hat{y}_i$): indicates **heteroscedasticity** (non-constant variance).
- **Curved pattern:** indicates a **non-linear relationship** that the model has not captured.

### Normal Q-Q Plot

Plot the ordered studentized residuals against the theoretical quantiles of the standard normal distribution.

- **Ideal pattern:** points fall approximately along the diagonal reference line.
- **Heavy tails** (S-shape deviating at both ends): the error distribution has heavier tails than normal.
- **Skewness** (systematic departure on one side): the error distribution is asymmetric.

### Scale-Location Plot

Plot $\sqrt{|r_i|}$ against $\hat{y}_i$.

- **Ideal pattern:** a flat band of points with no trend.
- **Upward trend:** variance increases with the fitted value, confirming heteroscedasticity.

### Residuals versus Leverage

Plot studentized residuals against leverages $h_{ii}$, often with contour lines for **Cook's distance**.

- Points with both high leverage and large residual magnitude are **influential observations** that can substantially change the fitted model.
- **Cook's distance** for observation $i$ combines leverage and residual size:

$$
D_i = \frac{r_i^2}{p} \cdot \frac{h_{ii}}{1 - h_{ii}}
$$

A common rule of thumb flags observations with $D_i > 4/n$ or $D_i > 1$ for further investigation.

---

## Assumption Checking Summary

The following table connects each regression assumption to the diagnostic that reveals its violation.

| Assumption | Diagnostic Plot | Violation Pattern |
|---|---|---|
| Linearity | Residuals vs Fitted | Curved pattern |
| Constant variance | Residuals vs Fitted, Scale-Location | Funnel or trend |
| Normality of errors | Normal Q-Q | Deviations from diagonal |
| Independence | Residuals vs Order (index plot) | Autocorrelation pattern |
| No undue influence | Residuals vs Leverage | Points beyond Cook's distance threshold |

!!! tip "Formal tests complement visual diagnostics"
    The Breusch-Pagan test checks for heteroscedasticity, the Durbin-Watson test checks for autocorrelation, and the Shapiro-Wilk test checks for non-normality. These tests provide $p$-values, but visual inspection of residual plots often reveals the *nature* of the problem more clearly than a test statistic alone.

---

## Summary

Residuals $e_i = y_i - \hat{y}_i$ are the primary tool for evaluating whether a fitted regression model meets its assumptions. OLS residuals have zero mean and are orthogonal to the predictor space. Standardized and studentized forms make residuals comparable across observations with different leverages. Four standard diagnostic plots -- residuals versus fitted values, the Q-Q plot, the scale-location plot, and the residuals-versus-leverage plot -- each target a specific assumption. When violations are found, they guide the modeler toward corrective actions such as variance-stabilizing transformations, non-linear terms, or the removal of influential outliers.

---

## Exercises

**Exercise 1.**
Fit a linear regression to 50 samples from $Y = 2X + \varepsilon$ where $\varepsilon \sim N(0, 1)$. Compute the raw residuals and verify they sum to zero and are orthogonal to $X$.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        x = np.random.uniform(0, 10, 50)
        y = 2*x + np.random.normal(0, 1, 50)
        result = stats.linregress(x, y)
        residuals = y - (result.intercept + result.slope * x)

        print(f"Sum of residuals: {np.sum(residuals):.10f}")
        print(f"Dot product with x: {np.dot(residuals, x):.10f}")

---

**Exercise 2.**
Generate data with heteroscedasticity: $Y = 3X + X \cdot \varepsilon$ where $\varepsilon \sim N(0, 1)$ (variance increases with $X$). Fit a linear model and plot residuals vs fitted values to visualize the funnel shape.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats
        import matplotlib.pyplot as plt

        np.random.seed(42)
        x = np.random.uniform(1, 10, 100)
        y = 3*x + x * np.random.normal(0, 1, 100)
        result = stats.linregress(x, y)
        fitted = result.intercept + result.slope * x
        resid = y - fitted

        plt.scatter(fitted, resid, alpha=0.5)
        plt.axhline(0, color='r', ls='--')
        plt.xlabel('Fitted values')
        plt.ylabel('Residuals')
        plt.title('Heteroscedasticity: Funnel Pattern')
        plt.show()

---

**Exercise 3.**
Fit a linear model to quadratic data ($Y = X^2$) and compute standardized residuals. Plot the residuals vs fitted values and the Q-Q plot to show both non-linearity and non-normality of residuals.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats
        import matplotlib.pyplot as plt

        x = np.linspace(1, 10, 50)
        y = x**2
        result = stats.linregress(x, y)
        fitted = result.intercept + result.slope * x
        resid = y - fitted
        std_resid = resid / np.std(resid, ddof=2)

        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        axes[0].scatter(fitted, std_resid)
        axes[0].axhline(0, color='r', ls='--')
        axes[0].set_title('Residuals vs Fitted')
        stats.probplot(std_resid, plot=axes[1])
        axes[1].set_title('Q-Q Plot of Residuals')
        plt.tight_layout()
        plt.show()
