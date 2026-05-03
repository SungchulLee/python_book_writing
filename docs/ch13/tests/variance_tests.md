# Variance Tests

Many parametric procedures — the pooled t-test, one-way ANOVA, and linear regression — assume that the groups being compared share the same variance (homoscedasticity). Before running these tests, variance tests verify whether this assumption is reasonable. When it fails, alternatives such as Welch's t-test or robust standard errors should be used instead.

!!! tip "Mental Model"
    Variance tests check whether groups have the same spread before you compare their centers. Bartlett's test is the most powerful but breaks down if data are not normal; Levene's test is robust to non-normality because it works with absolute deviations from the group medians instead of squared deviations from the mean.

## Hypotheses

Variance tests share the same hypothesis structure. Given $k$ groups with variances $\sigma_1^2, \sigma_2^2, \ldots, \sigma_k^2$, the hypotheses are

$$
H_0: \sigma_1^2 = \sigma_2^2 = \cdots = \sigma_k^2 \quad \text{vs} \quad H_1: \sigma_i^2 \neq \sigma_j^2 \text{ for some } i \neq j
$$

## Bartlett's Test

Bartlett's test is the most powerful test for equal variances when the data are normally distributed. It is based on a likelihood ratio approach.

For $k$ groups with sample sizes $n_i$ and sample variances $s_i^2$, define the pooled variance

$$
s_p^2 = \frac{\sum_{i=1}^{k}(n_i - 1)s_i^2}{\sum_{i=1}^{k}(n_i - 1)}
$$

The Bartlett test statistic is

$$
B = \frac{(N - k)\ln s_p^2 - \sum_{i=1}^{k}(n_i - 1)\ln s_i^2}{1 + \frac{1}{3(k-1)}\left(\sum_{i=1}^{k}\frac{1}{n_i - 1} - \frac{1}{N - k}\right)}
$$

where $N = \sum_{i=1}^{k} n_i$ is the total sample size. Under $H_0$, $B$ approximately follows a chi-square distribution:

$$
B \sim \chi^2_{k-1}
$$

!!! warning "Sensitivity to Non-Normality"
    Bartlett's test is highly sensitive to departures from normality. Even mild skewness or heavy tails can inflate the test statistic, leading to false rejections of $H_0$. Always verify normality before using Bartlett's test. If normality is questionable, use Levene's test instead.

```python
from scipy import stats

group_a = [23.1, 25.3, 24.8, 22.9, 26.1, 24.5]
group_b = [28.4, 30.1, 27.6, 29.8, 31.2, 28.9]
group_c = [33.5, 35.2, 34.1, 32.8, 36.0, 34.7]

b_stat, p_value = stats.bartlett(group_a, group_b, group_c)
print(f"Bartlett statistic: {b_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Levene's Test

Levene's test is a robust alternative to Bartlett's test that does not require normality. Instead of comparing variances directly, it performs an ANOVA on the transformed values $Z_{ij} = |X_{ij} - \hat{\mu}_i|$, where $\hat{\mu}_i$ is a location estimate for group $i$.

The test statistic is

$$
W = \frac{(N - k)}{(k - 1)} \cdot \frac{\sum_{i=1}^{k} n_i (\bar{Z}_i - \bar{Z})^2}{\sum_{i=1}^{k}\sum_{j=1}^{n_i}(Z_{ij} - \bar{Z}_i)^2}
$$

where $\bar{Z}_i$ is the mean of $Z_{ij}$ within group $i$ and $\bar{Z}$ is the overall mean. Under $H_0$, $W$ approximately follows:

$$
W \sim F_{k-1, \, N-k}
$$

The choice of location estimate $\hat{\mu}_i$ affects the test's properties:

| Center | `center` parameter | Properties |
|---|---|---|
| Mean | `'mean'` | Most powerful for symmetric, moderate-tailed distributions |
| Median | `'median'` | Most robust to skewness and heavy tails (default) |
| Trimmed mean | `'trimmed'` | Compromise between power and robustness |

```python
from scipy import stats

group_a = [23.1, 25.3, 24.8, 22.9, 26.1, 24.5]
group_b = [28.4, 30.1, 27.6, 29.8, 31.2, 28.9]
group_c = [33.5, 35.2, 34.1, 32.8, 36.0, 34.7]

# Default: median-based (most robust)
w_stat, p_value = stats.levene(group_a, group_b, group_c)
print(f"Levene (median): W = {w_stat:.4f}, p = {p_value:.4f}")

# Mean-based (more powerful for normal data)
w_stat, p_value = stats.levene(group_a, group_b, group_c, center='mean')
print(f"Levene (mean):   W = {w_stat:.4f}, p = {p_value:.4f}")
```

## Choosing Between Bartlett and Levene

| Property | Bartlett's Test | Levene's Test |
|---|---|---|
| Requires normality | Yes | No |
| Power under normality | Higher | Lower |
| Robustness to non-normality | Poor | Good |
| Recommended when | Normality is confirmed | Normality is uncertain or violated |

!!! tip "Practical Recommendation"
    In most applied settings, Levene's test with the median center is the safer default choice. Reserve Bartlett's test for situations where normality has been verified by a formal test (e.g., Shapiro-Wilk).

## Summary

Variance tests check the equal-variance assumption required by parametric procedures like the pooled t-test and ANOVA. Bartlett's test offers the highest power under normality but is unreliable when the normality assumption itself is violated. Levene's test provides a robust alternative that works well regardless of the underlying distribution shape. In SciPy, these are available through `scipy.stats.bartlett` and `scipy.stats.levene` respectively.

---

## Exercises

**Exercise 1.**
Three groups of measurements: A = [10.2, 10.5, 9.8, 10.1], B = [10.0, 11.5, 8.5, 12.0], C = [10.1, 10.0, 10.3, 9.9]. Apply both Bartlett's and Levene's tests. Which group has noticeably different variance?

??? success "Solution to Exercise 1"

        from scipy import stats

        a = [10.2, 10.5, 9.8, 10.1]
        b = [10.0, 11.5, 8.5, 12.0]
        c = [10.1, 10.0, 10.3, 9.9]

        b_stat, p_bart = stats.bartlett(a, b, c)
        w_stat, p_lev = stats.levene(a, b, c)

        print(f"Bartlett: stat={b_stat:.4f}, p={p_bart:.4f}")
        print(f"Levene:   stat={w_stat:.4f}, p={p_lev:.4f}")
        import numpy as np
        for name, g in [("A", a), ("B", b), ("C", c)]:
            print(f"  Group {name} variance: {np.var(g, ddof=1):.4f}")

---

**Exercise 2.**
Generate two groups from $N(0, 1)$ and $N(0, 3)$ (50 samples each). Apply Levene's test with `center='median'` and `center='mean'`. Compare the p-values.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        g1 = np.random.normal(0, 1, 50)
        g2 = np.random.normal(0, 3, 50)

        _, p_median = stats.levene(g1, g2, center='median')
        _, p_mean = stats.levene(g1, g2, center='mean')
        print(f"Levene (median): p={p_median:.6f}")
        print(f"Levene (mean):   p={p_mean:.6f}")

---

**Exercise 3.**
Simulate 1000 Levene's tests on groups from the same distribution ($N(0, 1)$, three groups of 30). Compute the false positive rate at $\alpha = 0.05$ and verify it is close to the nominal level.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        rejections = 0
        for _ in range(1000):
            g1 = np.random.normal(0, 1, 30)
            g2 = np.random.normal(0, 1, 30)
            g3 = np.random.normal(0, 1, 30)
            _, p = stats.levene(g1, g2, g3)
            if p < 0.05:
                rejections += 1
        print(f"False positive rate: {rejections/1000:.3f} (expected ~0.05)")
