# F-Distribution

The F-distribution arises naturally when comparing the variances of two independent normal populations. It is the sampling distribution of the ratio of two scaled chi-square random variables and serves as the foundation for analysis of variance (ANOVA) and F-tests in regression analysis.

!!! tip "Mental Model"
    The F-distribution is the ratio of two variance estimates. If both estimates measure the same underlying variance, their ratio clusters near 1. A large F-value means the numerator variance is much bigger than the denominator -- in ANOVA, this signals that group means differ more than random noise would predict.

---

## Mathematical Definition

If $X_1 \sim \chi^2(d_1)$ and $X_2 \sim \chi^2(d_2)$ are independent chi-square random variables, then the ratio

$$
F = \frac{X_1 / d_1}{X_2 / d_2}
$$

follows an F-distribution with $d_1$ (numerator) and $d_2$ (denominator) degrees of freedom, written $F \sim F(d_1, d_2)$.

The probability density function is:

$$
f(x) = \frac{1}{B\!\left(\frac{d_1}{2},\, \frac{d_2}{2}\right)} \left(\frac{d_1}{d_2}\right)^{d_1/2} \frac{x^{\,d_1/2 - 1}}{\left(1 + \frac{d_1}{d_2}\,x\right)^{(d_1 + d_2)/2}}, \quad x \ge 0
$$

where $B(\cdot,\cdot)$ is the beta function.

## Usage in scipy.stats

The `scipy.stats.f` distribution object takes the numerator degrees of freedom `dfn` ($d_1$) and denominator degrees of freedom `dfd` ($d_2$):

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

dfn, dfd = 5, 20
a = stats.f(dfn, dfd)

print(f"Mean: {a.mean():.4f}")        # d2/(d2-2) = 20/18
print(f"Variance: {a.var():.4f}")

x = np.linspace(0, 5, 200)
y_pdf = a.pdf(x)
y_cdf = a.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend()
plt.title(f'F-Distribution (d₁={dfn}, d₂={dfd})')
plt.xlabel('x')
plt.ylabel('Density / Probability')
plt.show()
```

The PDF is right-skewed with support on $[0, \infty)$. The CDF rises from 0 and approaches 1 as $x$ increases.

## Effect of Degrees of Freedom

As the degrees of freedom increase, the F-distribution becomes more concentrated around its mean and more symmetric:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 5, 200)
params = [(2, 5), (5, 10), (10, 20), (20, 40), (50, 100)]
for (d1, d2) in params:
    plt.plot(x, stats.f(d1, d2).pdf(x), label=f'd₁={d1}, d₂={d2}')

plt.legend()
plt.title('F-Distribution PDFs for Various Degrees of Freedom')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()
```

## Key Properties

- **Mean**: $E[F] = \dfrac{d_2}{d_2 - 2}$ for $d_2 > 2$
- **Variance**: $\text{Var}(F) = \dfrac{2\,d_2^2\,(d_1 + d_2 - 2)}{d_1\,(d_2 - 2)^2\,(d_2 - 4)}$ for $d_2 > 4$
- **Reciprocal property**: If $F \sim F(d_1, d_2)$, then $1/F \sim F(d_2, d_1)$
- **Relation to t-distribution**: If $T \sim t(d)$, then $T^2 \sim F(1, d)$

### Parameters in scipy.stats

| Parameter | Symbol | `scipy.stats` keyword | Default |
|-----------|--------|-----------------------|---------|
| Numerator df  | $d_1$ | `dfn`            | (required) |
| Denominator df | $d_2$ | `dfd`           | (required) |
| Location  | —       | `loc`            | 0       |
| Scale     | —       | `scale`          | 1       |

## Applications in Hypothesis Testing

The F-distribution is the basis for several important tests:

- **ANOVA**: The F-statistic compares between-group variance to within-group variance. Under the null hypothesis that all group means are equal, the test statistic follows $F(k-1, n-k)$ where $k$ is the number of groups and $n$ is the total sample size.
- **Regression F-test**: Tests whether a set of regression coefficients are jointly zero.
- **Variance ratio test**: Tests $H_0\colon \sigma_1^2 = \sigma_2^2$ for two independent normal populations.

Critical values are obtained using the PPF:

```python
alpha = 0.05
dfn, dfd = 3, 20
critical_value = stats.f(dfn, dfd).ppf(1 - alpha)
print(f"Critical value: {critical_value:.4f}")
# Reject H₀ if F-statistic > critical_value
```

## Financial Applications

In finance, the F-distribution appears in testing whether portfolio risk models with different numbers of factors provide significantly different fits, in comparing the variances of returns across different market regimes, and in multivariate regression tests for asset pricing models such as the Fama-French framework.

## Summary

The F-distribution is the sampling distribution of the ratio of two independent chi-square variables scaled by their degrees of freedom. In `scipy.stats`, use `stats.f(dfn, dfd)` to create a frozen distribution for computing PDFs, CDFs, critical values, and generating random samples.

---

## Exercises

**Exercise 1.**
Compute the 95th percentile of the $F$-distribution with $d_1 = 3$ and $d_2 = 20$. This is the critical value for an ANOVA F-test with 3 groups and 20 residual degrees of freedom.

??? success "Solution to Exercise 1"

        from scipy import stats

        crit = stats.f.ppf(0.95, dfn=3, dfd=20)
        print(f"F(3,20) 95th percentile: {crit:.4f}")

---

**Exercise 2.**
Generate 10,000 samples from an $F(5, 30)$ distribution. Compute the sample mean and verify it is close to the theoretical value $d_2 / (d_2 - 2)$.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        samples = stats.f.rvs(dfn=5, dfd=30, size=10000, random_state=42)
        theo_mean = 30 / (30 - 2)
        print(f"Sample mean: {np.mean(samples):.4f}")
        print(f"Theoretical mean: {theo_mean:.4f}")

---

**Exercise 3.**
Demonstrate the relationship between $F$ and $t$: generate 10,000 samples from $t(10)$, square them, and show the resulting distribution matches $F(1, 10)$ by comparing means and variances.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        t_samples = stats.t.rvs(df=10, size=10000, random_state=42)
        f_samples = t_samples ** 2

        f_rv = stats.f(dfn=1, dfd=10)
        print(f"t^2 mean: {np.mean(f_samples):.4f}, F(1,10) mean: {f_rv.mean():.4f}")
        print(f"t^2 var:  {np.var(f_samples, ddof=1):.4f}, F(1,10) var:  {f_rv.var():.4f}")
