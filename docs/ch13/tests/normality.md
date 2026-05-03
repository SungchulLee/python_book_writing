# Normality Tests

Many statistical methods — t-tests, ANOVA, linear regression — assume that the underlying data are normally distributed. Before applying these methods, normality tests provide a formal way to check whether this assumption is reasonable. A failed normality test signals that non-parametric alternatives or data transformations may be necessary.

!!! tip "Mental Model"
    Normality tests ask "could this data plausibly have come from a bell curve?" Shapiro-Wilk is the most powerful for small samples; D'Agostino-Pearson specifically checks skewness and kurtosis; Anderson-Darling emphasizes tail behavior. With large samples, all tests reject even tiny departures from normality, so always pair formal tests with visual diagnostics like QQ plots.

The general hypotheses for all normality tests are

$$
H_0: X \sim N(\mu, \sigma^2) \quad \text{vs} \quad H_1: X \not\sim N(\mu, \sigma^2)
$$

where $\mu$ and $\sigma^2$ are typically estimated from the data.

## Shapiro-Wilk Test

The Shapiro-Wilk test is one of the most powerful normality tests, particularly effective for small to moderate sample sizes ($n \leq 5000$). It assesses how well the order statistics of the sample match the expected order statistics of a normal distribution.

The test statistic is

$$
W = \frac{\left(\sum_{i=1}^{n} a_i X_{(i)}\right)^2}{\sum_{i=1}^{n}(X_i - \bar{X})^2}
$$

where $X_{(1)} \leq X_{(2)} \leq \cdots \leq X_{(n)}$ are the order statistics, and the weights $a_i$ are derived from the means, variances, and covariances of the order statistics of a standard normal sample of size $n$.

The statistic $W$ takes values in $(0, 1]$, where $W = 1$ indicates a perfect match with normality. Reject $H_0$ when $W$ is significantly smaller than 1.

```python
from scipy import stats
import numpy as np

np.random.seed(42)
data = np.random.normal(loc=0, scale=1, size=100)
w_stat, p_value = stats.shapiro(data)
print(f"Shapiro-Wilk statistic: {w_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Anderson-Darling Test

The Anderson-Darling test compares the empirical CDF to the normal CDF, with extra weight given to discrepancies in the tails. This makes it more sensitive than the Kolmogorov-Smirnov test to departures from normality in the extreme values.

The test statistic is

$$
A^2 = -n - \frac{1}{n}\sum_{i=1}^{n}\bigl[(2i - 1)\ln \Phi(Z_{(i)}) + (2(n - i) + 1)\ln(1 - \Phi(Z_{(i)}))\bigr]
$$

where $Z_{(i)} = (X_{(i)} - \bar{X}) / s$ are the standardized order statistics and $\Phi$ is the standard normal CDF.

The `anderson` function returns critical values at multiple significance levels rather than a single p-value:

```python
from scipy import stats
import numpy as np

np.random.seed(42)
data = np.random.normal(loc=0, scale=1, size=100)
result = stats.anderson(data, dist='norm')
print(f"Anderson-Darling statistic: {result.statistic:.4f}")
for sl, cv in zip(result.significance_level, result.critical_values):
    decision = "Reject H0" if result.statistic > cv else "Fail to reject H0"
    print(f"  {sl}% significance: critical value = {cv:.4f} -> {decision}")
```

## D'Agostino-Pearson Test

The D'Agostino-Pearson test combines two separate tests — one for skewness and one for kurtosis — into a single omnibus test. This approach detects departures from normality due to either asymmetry or heavy/light tails.

The test first computes a skewness statistic $Z_1$ based on the sample skewness $\sqrt{b_1}$ and a kurtosis statistic $Z_2$ based on the sample kurtosis $b_2$. The combined test statistic is

$$
K^2 = Z_1^2 + Z_2^2
$$

Under $H_0$, $K^2$ approximately follows a $\chi^2_2$ distribution. This test requires $n \geq 20$ to produce reliable results.

```python
from scipy import stats
import numpy as np

np.random.seed(42)
data = np.random.normal(loc=0, scale=1, size=100)
k2_stat, p_value = stats.normaltest(data)
print(f"K-squared statistic: {k2_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

!!! warning "Sample Size Sensitivity"
    Normality tests become increasingly sensitive with large sample sizes. A statistically significant departure from normality (small p-value) may be practically insignificant if the sample is large enough. Always supplement formal tests with visual diagnostics such as QQ plots.

## Comparison of Normality Tests

| Test | SciPy Function | Best For | Minimum $n$ |
|---|---|---|---|
| Shapiro-Wilk | `stats.shapiro` | Small to moderate samples | 3 |
| Anderson-Darling | `stats.anderson` | Tail departures | 8 |
| D'Agostino-Pearson | `stats.normaltest` | Skewness and kurtosis departures | 20 |

## Summary

Normality tests check whether data plausibly come from a normal distribution, which is an assumption underlying many parametric methods. The Shapiro-Wilk test offers the best overall power for small samples, the Anderson-Darling test is most sensitive to tail departures, and the D'Agostino-Pearson test specifically targets asymmetry and tail weight. In practice, combine formal tests with QQ plots for a complete assessment.

---

## Exercises

**Exercise 1.**
Generate 100 samples from a lognormal distribution. Apply the Shapiro-Wilk, Anderson-Darling, and D'Agostino-Pearson tests. Compare which tests detect the departure from normality.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = np.random.lognormal(0, 1, 100)

        w, p_sw = stats.shapiro(data)
        k2, p_dp = stats.normaltest(data)
        ad = stats.anderson(data, dist='norm')

        print(f"Shapiro-Wilk:      p={p_sw:.6f}")
        print(f"D'Agostino-Pearson: p={p_dp:.6f}")
        print(f"Anderson-Darling:  stat={ad.statistic:.4f}, 5% cv={ad.critical_values[2]:.4f}")

---

**Exercise 2.**
Investigate the effect of sample size on the Shapiro-Wilk test by generating normal data with $n = 10, 50, 200, 1000$ and running the test on each. Show that p-values remain large for truly normal data regardless of $n$.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        for n in [10, 50, 200, 1000]:
            data = np.random.normal(size=n)
            _, p = stats.shapiro(data)
            print(f"n={n:4d}: p={p:.4f}")

---

**Exercise 3.**
Apply the Shapiro-Wilk test to 100 samples from a $t$-distribution with 30 degrees of freedom. Since $t(30)$ is very close to normal, discuss whether the test rejects and what this means for practical analysis.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.t.rvs(df=30, size=100)
        w, p = stats.shapiro(data)
        print(f"Shapiro-Wilk: W={w:.4f}, p={p:.4f}")
        print("t(30) is very close to normal; test likely does not reject")
