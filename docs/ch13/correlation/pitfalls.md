# Correlation Pitfalls

Correlation coefficients are among the most frequently computed and most frequently misinterpreted statistics. A single number summarizing the relationship between two variables inevitably discards information, and users who rely on that number without checking the underlying assumptions risk drawing seriously wrong conclusions. This page catalogs the most common pitfalls and shows how to recognize and avoid each one.

!!! tip "Mental Model"
    A correlation coefficient is a lossy compression of a scatter plot into a single number. It can miss nonlinear patterns, be hijacked by outliers, or reflect a confounding variable rather than a real relationship. Always plot the data first -- Anscombe's quartet is the classic reminder that very different datasets can share the same $r$.

## Correlation Does Not Imply Causation

The most fundamental pitfall is interpreting a correlation as evidence of a causal relationship. Two variables $X$ and $Y$ can be highly correlated for several reasons that have nothing to do with $X$ causing $Y$:

- **Confounding**: A third variable $Z$ drives both $X$ and $Y$. For example, ice cream sales and drowning rates are positively correlated because both increase with temperature.
- **Reverse causation**: $Y$ causes $X$ rather than the other way around.
- **Coincidence**: With enough variables, some pairs will be correlated by chance (spurious correlation).

!!! warning "Causal Claims Require More Than Correlation"
    Establishing causation requires controlled experiments, natural experiments, or formal causal inference frameworks (e.g., instrumental variables, difference-in-differences). A high correlation value alone, regardless of sample size, never establishes causation.

## Sensitivity to Outliers

Pearson correlation has a **breakdown point of zero**, meaning a single extreme observation can make $r$ arbitrarily close to $\pm 1$ or $0$ regardless of the pattern in the remaining data.

```python
import numpy as np
from scipy import stats

# Strong positive trend in 99 points
np.random.seed(42)
x = np.random.normal(0, 1, 99)
y = 0.9 * x + np.random.normal(0, 0.3, 99)
r_clean, _ = stats.pearsonr(x, y)
print(f"Without outlier: r = {r_clean:.4f}")

# Add one extreme outlier
x_outlier = np.append(x, 10.0)
y_outlier = np.append(y, -10.0)
r_dirty, _ = stats.pearsonr(x_outlier, y_outlier)
print(f"With outlier:    r = {r_dirty:.4f}")

# Spearman is more robust
rho_clean, _ = stats.spearmanr(x, y)
rho_dirty, _ = stats.spearmanr(x_outlier, y_outlier)
print(f"Spearman without outlier: rho = {rho_clean:.4f}")
print(f"Spearman with outlier:    rho = {rho_dirty:.4f}")
```

!!! tip "Mitigation"
    Always visualize data with a scatter plot before computing correlations. Use Spearman or Kendall's Tau when outliers are present or suspected, as rank-based measures are far more robust.

## Nonlinearity

Pearson correlation measures only **linear** association. A strong nonlinear relationship can produce $r \approx 0$.

Consider $X \sim \text{Uniform}(-1, 1)$ and $Y = X^2$. Here $Y$ is a deterministic function of $X$, yet

$$
\text{Cov}(X, X^2) = E[X^3] - E[X] E[X^2] = 0
$$

because $X^3$ is an odd function integrated over a symmetric interval. Thus $r = 0$ despite perfect dependence.

!!! warning "Zero Correlation Does Not Mean Independence"
    The statement $r = 0$ means no **linear** association. The variables may still have a strong nonlinear or non-monotonic relationship. Always check scatter plots and consider nonparametric measures like Spearman or mutual information.

## Anscombe's Quartet

Anscombe's quartet consists of four datasets that share nearly identical summary statistics (mean, variance, correlation, and regression line) yet have strikingly different patterns when plotted:

1. A standard linear relationship with normal scatter
2. A clear nonlinear (parabolic) relationship
3. A perfect linear relationship disrupted by a single outlier
4. No relationship except through one extreme leverage point

All four have $r \approx 0.816$, demonstrating that the correlation coefficient alone is insufficient to characterize a relationship. This motivates the practice of **always visualizing data** alongside computing summary statistics.

## Restriction of Range

When the range of one or both variables is artificially restricted (e.g., by selection or truncation), the observed correlation is **attenuated** compared to the correlation in the full population.

For example, if test scores range from 0 to 100 in the population but only students scoring above 70 are observed, the within-sample correlation between test score and performance will be lower than the true population correlation. This effect occurs because truncation reduces variability, and less variability leaves less room for covariation.

!!! note "Range Restriction in Practice"
    This pitfall is common in educational testing (only admitted students are observed), employment studies (only hired applicants), and financial analysis (only traded assets). When possible, use correction formulas that estimate the unrestricted correlation from the restricted sample.

## Simpson's Paradox

A correlation observed in the aggregate data can reverse direction within every subgroup. This is known as **Simpson's paradox** (or the ecological fallacy when applied to group-level vs. individual-level analysis).

```python
# Simpson's paradox example
np.random.seed(42)

# Group A: negative slope within group
x_a = np.random.uniform(1, 3, 50)
y_a = -0.5 * x_a + 5 + np.random.normal(0, 0.3, 50)

# Group B: negative slope within group, shifted up and right
x_b = np.random.uniform(4, 6, 50)
y_b = -0.5 * x_b + 9 + np.random.normal(0, 0.3, 50)

# Within each group: negative correlation
r_a, _ = stats.pearsonr(x_a, y_a)
r_b, _ = stats.pearsonr(x_b, y_b)
print(f"Group A: r = {r_a:.4f}")
print(f"Group B: r = {r_b:.4f}")

# Combined: positive correlation (Simpson's paradox)
x_all = np.concatenate([x_a, x_b])
y_all = np.concatenate([y_a, y_b])
r_all, _ = stats.pearsonr(x_all, y_all)
print(f"Combined: r = {r_all:.4f}")
```

The combined positive correlation arises because group membership acts as a confounder. Aggregating heterogeneous groups without accounting for group structure can produce misleading correlations.

## Summary

Correlation coefficients are powerful summary measures, but they can mislead when used without care. The key pitfalls are: (1) confusing correlation with causation, (2) ignoring sensitivity to outliers, (3) assuming $r = 0$ means independence, (4) trusting a single number without visualization, (5) ignoring range restriction, and (6) aggregating over heterogeneous subgroups. Guarding against these errors requires combining correlation measures with scatter plots, robust alternatives, and domain knowledge.

---

## Exercises

**Exercise 1.**
Create Anscombe-like data: generate 50 points where $X$ and $Y$ have a perfect Pearson $r \approx 0$ but a clear nonlinear (quadratic) relationship. Compute Pearson's $r$ and Spearman's $\rho$ and explain the discrepancy.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        x = np.linspace(-3, 3, 50)
        y = x**2 + np.random.normal(0, 0.5, 50)
        r_p, _ = stats.pearsonr(x, y)
        r_s, _ = stats.spearmanr(x, y)
        print(f"Pearson:  {r_p:.4f} (misses U-shape)")
        print(f"Spearman: {r_s:.4f}")

---

**Exercise 2.**
Demonstrate Simpson's paradox: create two subgroups where within each group $X$ and $Y$ are positively correlated, but in the combined data the correlation is negative. Compute correlations for each subgroup and the combined data.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        # Group 1: low x range
        x1 = np.random.normal(2, 0.5, 50)
        y1 = 0.5 * x1 + np.random.normal(8, 0.3, 50)
        # Group 2: high x range
        x2 = np.random.normal(6, 0.5, 50)
        y2 = 0.5 * x2 + np.random.normal(2, 0.3, 50)

        r1, _ = stats.pearsonr(x1, y1)
        r2, _ = stats.pearsonr(x2, y2)
        r_all, _ = stats.pearsonr(np.concatenate([x1,x2]), np.concatenate([y1,y2]))

        print(f"Group 1 r: {r1:.4f}")
        print(f"Group 2 r: {r2:.4f}")
        print(f"Combined r: {r_all:.4f} (Simpson's paradox)")

---

**Exercise 3.**
Show how restriction of range reduces correlation: generate 500 samples from a bivariate normal with $\rho = 0.8$. Compute Pearson's $r$ on the full data, then restrict to samples where $X > 0$ and compute $r$ again. Show the restricted correlation is lower.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.multivariate_normal.rvs(mean=[0,0], cov=[[1,0.8],[0.8,1]], size=500)
        r_full, _ = stats.pearsonr(data[:, 0], data[:, 1])
        mask = data[:, 0] > 0
        r_restricted, _ = stats.pearsonr(data[mask, 0], data[mask, 1])
        print(f"Full data r:       {r_full:.4f}")
        print(f"Restricted (X>0) r:{r_restricted:.4f}")
