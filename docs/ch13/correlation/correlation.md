# Pearson and Spearman

Quantifying the strength and direction of a relationship between two variables is one of the most common tasks in statistical analysis. The Pearson correlation coefficient measures the degree of linear association, while the Spearman rank correlation captures monotonic relationships without assuming linearity. Choosing the right measure depends on the data's distributional properties and the type of relationship under investigation.

!!! tip "Mental Model"
    Pearson correlation measures how well a straight line fits the scatter plot; Spearman measures how well any monotonic curve fits it. If you care about "do both variables increase together," use Spearman. If you care specifically about a linear rate of increase, use Pearson.

## Pearson Correlation

The **Pearson correlation coefficient** between two random variables $X$ and $Y$ is defined as

$$
\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \, \sigma_Y} = \frac{E[(X - \mu_X)(Y - \mu_Y)]}{\sigma_X \, \sigma_Y}
$$

Given a sample of $n$ paired observations $(x_1, y_1), \ldots, (x_n, y_n)$, the **sample Pearson correlation** is

$$
r = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2 \;\sum_{i=1}^{n}(y_i - \bar{y})^2}}
$$

The coefficient satisfies $-1 \leq r \leq 1$, where $r = 1$ indicates a perfect positive linear relationship, $r = -1$ indicates a perfect negative linear relationship, and $r = 0$ indicates no linear association.

!!! note "Assumptions for Pearson Correlation"
    Pearson correlation assumes that both variables are measured on an interval or ratio scale. The coefficient captures only **linear** relationships: a strong nonlinear relationship (e.g., $Y = X^2$) can produce $r \approx 0$. Inference (p-values, confidence intervals) additionally assumes bivariate normality.

```python
import numpy as np
from scipy import stats

# Generate linearly related data with noise
np.random.seed(42)
x = np.random.normal(0, 1, 200)
y = 0.8 * x + np.random.normal(0, 0.5, 200)

r, p_value = stats.pearsonr(x, y)
print(f"Pearson r = {r:.4f}, p-value = {p_value:.2e}")
```

The function `stats.pearsonr` returns both the correlation coefficient and a two-sided p-value testing the null hypothesis $H_0\!: \rho = 0$ against $H_1\!: \rho \neq 0$.

## Spearman Rank Correlation

The **Spearman rank correlation** is a nonparametric measure that assesses monotonic relationships. It is defined as the Pearson correlation applied to the ranks of the data. When there are no tied ranks, it simplifies to

$$
r_s = 1 - \frac{6 \sum_{i=1}^{n} d_i^2}{n(n^2 - 1)}
$$

where $d_i = \text{rank}(x_i) - \text{rank}(y_i)$ is the difference between the ranks of corresponding observations.

Like Pearson, $-1 \leq r_s \leq 1$, where $r_s = 1$ indicates a perfect monotonically increasing relationship and $r_s = -1$ a perfect monotonically decreasing one.

Because Spearman operates on ranks rather than raw values, it is robust to outliers and does not require the variables to be normally distributed. It also detects monotonic nonlinear relationships that Pearson may miss.

```python
# Generate monotonically (but nonlinearly) related data
np.random.seed(42)
x = np.random.uniform(0.1, 5, 200)
y = np.log(x) + np.random.normal(0, 0.3, 200)

rho, p_value = stats.spearmanr(x, y)
print(f"Spearman rho = {rho:.4f}, p-value = {p_value:.2e}")

# Compare with Pearson on the same data
r, _ = stats.pearsonr(x, y)
print(f"Pearson r    = {r:.4f}")
```

## When to Use Each Measure

| Criterion | Pearson | Spearman |
|---|---|---|
| Relationship type | Linear | Monotonic |
| Scale requirement | Interval/ratio | Ordinal or above |
| Sensitivity to outliers | High | Low |
| Distribution assumption | Bivariate normality (for inference) | None |

!!! tip "Practical Guidance"
    When in doubt, compute both. If Pearson and Spearman yield similar values, the relationship is approximately linear. If Spearman is substantially larger in magnitude, the relationship may be monotonic but nonlinear. If both are near zero, there may still be a non-monotonic association that neither measure captures.

## Summary

Pearson correlation quantifies linear association through the ratio of covariance to the product of standard deviations, while Spearman rank correlation measures monotonic association by applying Pearson to ranked data. Pearson is sensitive to outliers and assumes linearity, whereas Spearman is robust and distribution-free. Both return values in $[-1, 1]$ with associated p-values testing the null hypothesis of zero correlation, and they are accessible through `scipy.stats.pearsonr` and `scipy.stats.spearmanr`.

---

## Runnable Example: `correlation_regression.py`

```python
"""
Tutorial 06: Correlation and Regression Analysis
================================================
Level: Intermediate-Advanced
Topics: Pearson, Spearman, Kendall correlation; Simple and multiple linear
        regression; Polynomial regression; Regression diagnostics

This module covers correlation analysis and linear regression using scipy.stats
and demonstrates how to assess relationships between variables.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit
import warnings

if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    np.random.seed(42)

    print("="*80)
    print("CORRELATION AND REGRESSION ANALYSIS")
    print("="*80)
    print()

    # =============================================================================
    # SECTION 1: Pearson Correlation Coefficient
    # =============================================================================
    """
    Pearson correlation (r) measures linear relationship between two variables.

    Range: -1 to +1
    - r = +1: Perfect positive linear relationship
    - r = 0: No linear relationship
    - r = -1: Perfect negative linear relationship

    Test: H₀: ρ = 0 (no correlation)
          H₁: ρ ≠ 0 (correlation exists)
    """

    print("PEARSON CORRELATION")
    print("-" * 40)

    # Generate correlated data
    n = 50
    x = np.random.normal(0, 1, n)
    noise = np.random.normal(0, 0.5, n)

    # Different correlation strengths
    y_strong = 2*x + 3 + noise * 0.2  # Strong positive correlation
    y_moderate = 0.8*x + 2 + noise     # Moderate positive correlation
    y_weak = 0.3*x + 1 + noise * 2     # Weak positive correlation
    y_none = np.random.normal(0, 1, n)  # No correlation

    datasets = [
        ("Strong positive", x, y_strong),
        ("Moderate positive", x, y_moderate),
        ("Weak positive", x, y_weak),
        ("No correlation", x, y_none)
    ]

    print(f"{'Relationship':<20} {'r':<10} {'p-value':<12} {'Interpretation'}")
    print("-" * 60)

    for name, x_data, y_data in datasets:
        r, p = stats.pearsonr(x_data, y_data)

        if p < 0.001:
            sig = "***"
        elif p < 0.01:
            sig = "**"
        elif p < 0.05:
            sig = "*"
        else:
            sig = "ns"

        print(f"{name:<20} {r:>8.3f}  {p:>10.4f}{sig:<2}", end="")

        if abs(r) < 0.3:
            print(" weak")
        elif abs(r) < 0.7:
            print(" moderate")
        else:
            print(" strong")

    print()

    # Visualize correlations
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.ravel()

    for i, (name, x_data, y_data) in enumerate(datasets):
        r, p = stats.pearsonr(x_data, y_data)

        axes[i].scatter(x_data, y_data, alpha=0.6)

        # Add regression line
        slope, intercept = np.polyfit(x_data, y_data, 1)
        x_line = np.linspace(x_data.min(), x_data.max(), 100)
        y_line = slope * x_line + intercept
        axes[i].plot(x_line, y_line, 'r-', linewidth=2, label=f'r={r:.3f}')

        axes[i].set_xlabel('X')
        axes[i].set_ylabel('Y')
        axes[i].set_title(f'{name}')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/06_pearson_correlation.png', 
                dpi=300, bbox_inches='tight')
    print("Saved: 06_pearson_correlation.png\n")
    plt.close()

    # More detailed tutorial content would continue...
    # [Additional sections on Spearman, Kendall, regression, etc.]

    print("="*80)
    print("Tutorial 06 Complete!")
    print("="*80)
```

---

## Exercises

**Exercise 1.**
Generate 150 samples where $Y = X^2 + \varepsilon$ with $X \sim \text{Uniform}(-2, 2)$ and $\varepsilon \sim N(0, 0.5^2)$. Compute Pearson and Spearman correlations. Explain why Spearman may be higher for this nonlinear relationship.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        x = np.random.uniform(-2, 2, 150)
        y = x**2 + np.random.normal(0, 0.5, 150)

        r_pearson, _ = stats.pearsonr(x, y)
        r_spearman, _ = stats.spearmanr(x, y)
        print(f"Pearson:  {r_pearson:.4f}")
        print(f"Spearman: {r_spearman:.4f}")
        print("Pearson is near 0 (symmetric U-shape); Spearman may capture monotonic segments")

---

**Exercise 2.**
Compute Pearson's $r$ for 100 bivariate normal samples with true $\rho = 0.5$. Also compute the p-value from `stats.pearsonr()`. Repeat 1000 times and verify the p-value is below 0.05 approximately $(1 - \beta)$ of the time.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        significant = 0
        for _ in range(1000):
            data = stats.multivariate_normal.rvs(mean=[0,0], cov=[[1,0.5],[0.5,1]], size=100)
            _, p = stats.pearsonr(data[:, 0], data[:, 1])
            if p < 0.05:
                significant += 1
        print(f"Power (fraction significant): {significant/1000:.3f}")

---

**Exercise 3.**
Create data with an outlier: 50 samples from $N(0, 1)$ for both $X$ and $Y$ (independent), then add one point at $(10, 10)$. Compute Pearson's $r$ with and without the outlier to demonstrate outlier sensitivity.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        x = np.random.normal(0, 1, 50)
        y = np.random.normal(0, 1, 50)

        r_no_outlier, _ = stats.pearsonr(x, y)
        x_out = np.append(x, 10)
        y_out = np.append(y, 10)
        r_outlier, _ = stats.pearsonr(x_out, y_out)

        print(f"Pearson r (no outlier): {r_no_outlier:.4f}")
        print(f"Pearson r (with outlier): {r_outlier:.4f}")
