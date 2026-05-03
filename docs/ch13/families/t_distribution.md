# t-Distribution

The t-distribution (Student's t-distribution) arises when estimating the mean of a normally distributed population using a small sample with unknown variance. It has heavier tails than the standard normal distribution, which accounts for the additional uncertainty introduced by estimating the variance from the data. The t-distribution is the basis for t-tests and confidence intervals in classical statistics.

!!! tip "Mental Model"
    The t-distribution is a "cautious normal." When you estimate variance from a small sample, there is extra uncertainty, so the distribution has heavier tails -- extreme values are more probable than a normal would predict. As the sample size (degrees of freedom) grows, this extra uncertainty vanishes and the t-distribution converges to the standard normal.

---

## Mathematical Definition

If $Z \sim N(0, 1)$ and $V \sim \chi^2(\nu)$ are independent, then the random variable

$$
T = \frac{Z}{\sqrt{V/\nu}}
$$

follows a t-distribution with $\nu$ degrees of freedom, written $T \sim t(\nu)$.

The probability density function is:

$$
f(x) = \frac{\Gamma\!\left(\frac{\nu + 1}{2}\right)}{\sqrt{\nu\pi}\;\Gamma\!\left(\frac{\nu}{2}\right)} \left(1 + \frac{x^2}{\nu}\right)^{-(\nu + 1)/2}
$$

where $\Gamma(\cdot)$ is the gamma function and $\nu > 0$ is the degrees of freedom parameter.

## Usage in scipy.stats

The `scipy.stats.t` distribution object takes the degrees of freedom `df` ($\nu$):

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

df = 5
a = stats.t(df)

print(f"Mean: {a.mean():.4f}")        # 0 (for ν > 1)
print(f"Variance: {a.var():.4f}")      # ν/(ν-2) = 5/3

x = np.linspace(-5, 5, 200)
y_pdf = a.pdf(x)
y_cdf = a.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend()
plt.title(f't-Distribution (ν={df})')
plt.xlabel('x')
plt.ylabel('Density / Probability')
plt.show()
```

## Comparison with the Normal Distribution

The t-distribution is symmetric about zero like the standard normal, but it has heavier tails. As $\nu$ increases, the t-distribution converges to the standard normal:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-5, 5, 200)
plt.plot(x, stats.norm.pdf(x), 'k--', linewidth=2, label='N(0,1)')
for df in [1, 3, 5, 10, 30]:
    plt.plot(x, stats.t(df).pdf(x), label=f'ν={df}')

plt.legend()
plt.title('t-Distribution PDFs vs Standard Normal')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()
```

The case $\nu = 1$ is the Cauchy distribution, which has such heavy tails that neither the mean nor the variance exists.

## Key Properties

- **Mean**: $E[T] = 0$ for $\nu > 1$ (undefined for $\nu \le 1$)
- **Variance**: $\text{Var}(T) = \dfrac{\nu}{\nu - 2}$ for $\nu > 2$ (infinite for $1 < \nu \le 2$)
- **Symmetry**: The distribution is symmetric about 0
- **Heavy tails**: For any finite $\nu$, the tails decay as a power law $|x|^{-(\nu+1)}$, slower than the exponential decay of the normal
- **Convergence**: As $\nu \to \infty$, $t(\nu) \to N(0, 1)$

### Special Cases

- $\nu = 1$: Cauchy distribution (no finite moments)
- $\nu = \infty$: standard normal distribution

### Parameters in scipy.stats

| Parameter | Symbol | `scipy.stats` keyword | Default |
|-----------|--------|-----------------------|---------|
| Degrees of freedom | $\nu$ | `df`        | (required) |
| Location  | —       | `loc`                | 0       |
| Scale     | —       | `scale`              | 1       |

## Applications in Hypothesis Testing

The t-distribution is used whenever a test statistic involves an estimated standard deviation:

- **One-sample t-test**: Testing $H_0\colon \mu = \mu_0$ using $T = (\bar{X} - \mu_0)/(S/\sqrt{n})$, which follows $t(n-1)$ under $H_0$
- **Two-sample t-test**: Comparing means of two independent groups
- **Confidence intervals**: A 95% confidence interval for the mean is $\bar{X} \pm t_{0.025,\,n-1} \cdot S/\sqrt{n}$

Critical values are obtained using the PPF:

```python
alpha = 0.05
df = 20
t_critical = stats.t(df).ppf(1 - alpha / 2)
print(f"Two-sided critical value: ±{t_critical:.4f}")
```

## Financial Applications

In finance, the t-distribution is used in modeling asset returns when normal tails are too thin to capture extreme events. The Student-t copula models joint tail dependence between assets. Risk measures such as Value at Risk use the t-distribution for more conservative tail estimates, and GARCH models with t-distributed innovations provide better fits to financial return series.

## Summary

The t-distribution arises from the ratio of a standard normal to a scaled chi-square variable and has heavier tails than the normal. In `scipy.stats`, use `stats.t(df)` to create a frozen distribution for computing PDFs, CDFs, critical values, and generating random samples.

---

## Exercises

**Exercise 1.**
Plot the PDF of the $t$-distribution for $\nu = 2, 5, 30$ and the standard normal on the same axes over $[-4, 4]$. Observe how the $t$-distribution approaches the normal as $\nu$ increases.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats
        import matplotlib.pyplot as plt

        x = np.linspace(-4, 4, 200)
        for df in [2, 5, 30]:
            plt.plot(x, stats.t.pdf(x, df), label=f't(df={df})')
        plt.plot(x, stats.norm.pdf(x), 'k--', label='Normal')
        plt.legend()
        plt.title('t-distribution vs Normal')
        plt.show()

---

**Exercise 2.**
For a $t$-distribution with 10 degrees of freedom, compute the probability $P(|T| > 2)$. Compare this with the corresponding probability under the standard normal.

??? success "Solution to Exercise 2"

        from scipy import stats

        p_t = 2 * stats.t.sf(2, df=10)
        p_norm = 2 * stats.norm.sf(2)
        print(f"P(|T|>2), t(10):  {p_t:.4f}")
        print(f"P(|Z|>2), Normal: {p_norm:.4f}")

---

**Exercise 3.**
Compute the 95th percentile of the $t$-distribution for $\nu = 5, 10, 30, 100$ and the standard normal. Show that the $t$ percentile converges toward the normal percentile as $\nu$ grows.

??? success "Solution to Exercise 3"

        from scipy import stats

        for df in [5, 10, 30, 100]:
            print(f"t(df={df:3d}) 95th percentile: {stats.t.ppf(0.95, df):.4f}")
        print(f"Normal 95th percentile:     {stats.norm.ppf(0.95):.4f}")
