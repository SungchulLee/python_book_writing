# Goodness of Fit

Many statistical procedures assume that data follows a specific probability distribution. Before relying on these assumptions, a goodness-of-fit test quantifies whether the observed data are consistent with a hypothesized distribution. These tests formalize the question: does my sample plausibly come from distribution $F_0$?

!!! tip "Mental Model"
    A goodness-of-fit test compares the shape of your data to a candidate distribution. The KS test measures the maximum gap between the empirical and theoretical CDFs; the Anderson-Darling test does the same but weights the tails more heavily; the chi-square test bins the data and compares observed to expected counts. Each emphasizes different types of departures.

The general hypotheses are

$$
H_0: F = F_0 \quad \text{vs} \quad H_1: F \neq F_0
$$

where $F$ is the true cumulative distribution function (CDF) of the data and $F_0$ is the hypothesized CDF.

## Chi-Square Goodness-of-Fit Test

The chi-square test partitions the sample space into $k$ bins and compares observed counts $O_i$ to expected counts $E_i = n \cdot p_{i,0}$ under the null distribution. The test statistic is

$$
\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}
$$

Under $H_0$, this statistic follows $\chi^2_{k-1-m}$, where $m$ is the number of parameters estimated from the data.

The chi-square test applies to both discrete and continuous distributions (after binning), but requires all expected counts to satisfy $E_i \geq 5$ for the approximation to be reliable.

```python
from scipy import stats

observed = [18, 22, 16, 21, 13, 10]
chi2_stat, p_value = stats.chisquare(observed)
print(f"Chi-square statistic: {chi2_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Kolmogorov-Smirnov Test

The Kolmogorov-Smirnov (KS) test compares the empirical CDF $F_n(x) = \frac{1}{n}\sum_{i=1}^{n} \mathbf{1}(X_i \leq x)$ to the hypothesized CDF $F_0(x)$. The test statistic is the supremum of the absolute difference:

$$
D_n = \sup_{x} |F_n(x) - F_0(x)|
$$

Under $H_0$, the scaled statistic $\sqrt{n}\, D_n$ converges to the Kolmogorov distribution. The KS test is most sensitive to differences near the center of the distribution and less sensitive to deviations in the tails.

!!! warning "Fully Specified Distribution Required"
    The KS test requires that $F_0$ is completely specified — all parameters must be fixed before testing. If parameters are estimated from the same data, the test becomes conservative (p-values are too large). Use the Lilliefors correction for the special case of testing normality with estimated mean and variance.

```python
from scipy import stats
import numpy as np

np.random.seed(42)
data = np.random.normal(loc=0, scale=1, size=100)
ks_stat, p_value = stats.kstest(data, 'norm')
print(f"KS statistic: {ks_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Anderson-Darling Test

The Anderson-Darling test modifies the KS approach by weighting discrepancies in the tails more heavily. The test statistic is

$$
A^2 = -n - \frac{1}{n}\sum_{i=1}^{n}\bigl[(2i - 1)\ln F_0(X_{(i)}) + (2(n - i) + 1)\ln(1 - F_0(X_{(i)}))\bigr]
$$

where $X_{(1)} \leq X_{(2)} \leq \cdots \leq X_{(n)}$ are the order statistics. The Anderson-Darling test is generally more powerful than the KS test for detecting tail deviations, and SciPy provides critical values for several common distributions.

```python
from scipy import stats
import numpy as np

np.random.seed(42)
data = np.random.normal(loc=0, scale=1, size=100)
result = stats.anderson(data, dist='norm')
print(f"Anderson-Darling statistic: {result.statistic:.4f}")
for sl, cv in zip(result.significance_level, result.critical_values):
    print(f"  {sl}% significance: critical value = {cv:.4f}")
```

The `anderson` function returns critical values at multiple significance levels rather than a single p-value.

## Comparison of Tests

| Property | Chi-Square | KS | Anderson-Darling |
|---|---|---|---|
| Data type | Discrete or binned continuous | Continuous only | Continuous only |
| Sensitivity | Depends on binning | Center of distribution | Tails of distribution |
| Parameters | Can estimate from data (adjust df) | Must be fully specified | Built-in for common distributions |
| Sample size | Needs $E_i \geq 5$ | Any | Any |

## Summary

Goodness-of-fit tests assess whether observed data match a theoretical distribution. The chi-square test works with categorical or binned data, the Kolmogorov-Smirnov test measures the maximum CDF deviation for continuous data, and the Anderson-Darling test provides greater sensitivity in the tails. In SciPy, these are available through `chisquare`, `kstest`, and `anderson` respectively. The Shapiro-Wilk test, which specializes in normality testing, is covered in the normality tests page.

---

## Exercises

**Exercise 1.**
Generate 200 samples from an exponential distribution with $\lambda = 2$. Use the KS test (`stats.kstest`) to test the null hypothesis that the data come from $\text{Exp}(\lambda = 2)$ (i.e., `scale=0.5`). Then test against $\text{Exp}(\lambda = 1)$ and compare p-values.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.expon.rvs(scale=0.5, size=200)

        ks_correct, p_correct = stats.kstest(data, 'expon', args=(0, 0.5))
        ks_wrong, p_wrong = stats.kstest(data, 'expon', args=(0, 1.0))

        print(f"Correct model: KS={ks_correct:.4f}, p={p_correct:.4f}")
        print(f"Wrong model:   KS={ks_wrong:.4f}, p={p_wrong:.4f}")

---

**Exercise 2.**
Generate 150 samples from a $t$-distribution with 5 df and apply the Anderson-Darling normality test. Interpret the result by comparing the test statistic with the critical values.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.t.rvs(df=5, size=150)
        result = stats.anderson(data, dist='norm')
        print(f"A-D statistic: {result.statistic:.4f}")
        for sl, cv in zip(result.significance_level, result.critical_values):
            decision = "Reject" if result.statistic > cv else "Fail to reject"
            print(f"  {sl}%: critical={cv:.4f} -> {decision}")

---

**Exercise 3.**
Compare the KS and Anderson-Darling tests on data from a mixture of two normals: $0.7 \cdot N(0,1) + 0.3 \cdot N(3,1)$. Test against a standard normal and see which test produces a smaller p-value (greater power).

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        n = 200
        idx = np.random.choice([0, 1], size=n, p=[0.7, 0.3])
        data = np.where(idx == 0, np.random.normal(0, 1, n), np.random.normal(3, 1, n))

        ks_stat, ks_p = stats.kstest(data, 'norm', args=(0, 1))
        ad_result = stats.anderson(data, dist='norm')

        print(f"KS test: stat={ks_stat:.4f}, p={ks_p:.4f}")
        print(f"A-D test: stat={ad_result.statistic:.4f}")
