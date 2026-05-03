# Chi-Square Distribution

The chi-square ($\chi^2$) distribution arises as the sum of squared standard normal random variables. It plays a central role in hypothesis testing, confidence interval construction, and goodness-of-fit tests.

!!! tip "Mental Model"
    Square a standard normal variable and you get a chi-square with 1 degree of freedom. Add $k$ such squared normals and you get $\chi^2(k)$. This is why the chi-square appears whenever you measure squared deviations from expected values -- goodness-of-fit tests, variance estimation, and contingency tables all reduce to sums of squared standardized differences.

---

## Mathematical Definition

If $Z_1, Z_2, \ldots, Z_k$ are independent standard normal random variables, then:

$$X = Z_1^2 + Z_2^2 + \cdots + Z_k^2 \sim \chi^2(k)$$

The PDF is:

$$f(x) = \frac{x^{k/2 - 1} e^{-x/2}}{2^{k/2} \Gamma(k/2)}, \quad x \ge 0$$

where $k$ is the **degrees of freedom** (df).

## Usage in scipy.stats

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

df = 10
a = stats.chi2(df)

print(f"Mean: {a.mean():.2f}")      # = df = 10
print(f"Variance: {a.var():.2f}")    # = 2*df = 20

# Visualize: samples vs theoretical PDF
x_samples = a.rvs(size=10000, random_state=337)
x_theory = np.linspace(0, 40, 100)
y_theory = a.pdf(x_theory)

plt.plot(x_theory, y_theory, color='r', label='Theoretical PDF')
plt.hist(x_samples, density=True, bins=30, alpha=0.7, label='Sampled histogram')
plt.legend()
plt.title(f'Chi-Square Distribution (df={df})')
plt.xlabel('x')
plt.ylabel('Density')
plt.show()
```

## Key Properties

The chi-square distribution has mean $E[X] = k$, variance $\text{Var}(X) = 2k$, and is always right-skewed (though it becomes more symmetric as $k$ increases). It is a special case of the gamma distribution: $\chi^2(k) = \text{Gamma}(k/2, 2)$.

## Effect of Degrees of Freedom

As the degrees of freedom increase, the chi-square distribution shifts to the right and becomes more symmetric, approaching a normal distribution by the Central Limit Theorem:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 40, 200)
for df in [1, 2, 5, 10, 20]:
    plt.plot(x, stats.chi2(df).pdf(x), label=f'df={df}')

plt.legend()
plt.title('Chi-Square PDFs for Various Degrees of Freedom')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()
```

## Applications in Hypothesis Testing

The chi-square distribution is used for chi-square tests of independence (testing association between categorical variables), goodness-of-fit tests (testing if data follows a hypothesized distribution), and confidence intervals for population variance ($\sigma^2$).

Critical values are obtained using the PPF:

```python
alpha = 0.05
df = 10
critical_value = stats.chi2(df).ppf(1 - alpha)
# Reject H₀ if test statistic > critical_value
```

## Financial Applications

In finance, the chi-square distribution appears in variance ratio tests for market efficiency, likelihood ratio tests in maximum likelihood estimation, and portfolio variance testing under normality assumptions.

## Summary

The chi-square distribution is fundamental to statistical inference. In `scipy.stats`, use `stats.chi2(df)` to create a frozen distribution for computing PDFs, CDFs, critical values, and generating random samples.

---

## Exercises

**Exercise 1.**
Generate 5000 standard normal samples, square each one, and show that the resulting distribution matches a $\chi^2(1)$ distribution by comparing sample quantiles to theoretical quantiles from `stats.chi2(df=1).ppf()`.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        z = np.random.normal(size=5000)
        chi2_samples = z ** 2

        theoretical_q = stats.chi2.ppf([0.25, 0.50, 0.75], df=1)
        sample_q = np.quantile(chi2_samples, [0.25, 0.50, 0.75])
        for p, tq, sq in zip([0.25, 0.50, 0.75], theoretical_q, sample_q):
            print(f"Quantile {p}: theoretical={tq:.4f}, sample={sq:.4f}")

---

**Exercise 2.**
Compute the mean and variance of $\chi^2$ distributions for $k = 1, 5, 10, 30$. Verify that the mean equals $k$ and the variance equals $2k$ for each.

??? success "Solution to Exercise 2"

        from scipy import stats

        for k in [1, 5, 10, 30]:
            rv = stats.chi2(df=k)
            print(f"k={k:2d}: mean={rv.mean():.1f} (exp {k}), var={rv.var():.1f} (exp {2*k})")

---

**Exercise 3.**
For a $\chi^2$ distribution with 15 degrees of freedom, find the critical value $c$ such that $P(\chi^2 > c) = 0.05$. Verify using the survival function.

??? success "Solution to Exercise 3"

        from scipy import stats

        rv = stats.chi2(df=15)
        c = rv.isf(0.05)
        print(f"Critical value: {c:.4f}")
        print(f"Verification: P(X > {c:.4f}) = {rv.sf(c):.4f}")
