# Confidence Intervals

In statistical inference, a point estimate like the sample mean provides a single best guess for a parameter, but it says nothing about the uncertainty of that guess. A **confidence interval** gives a range of plausible values, and the `.interval()` method on `scipy.stats` distributions computes the equal-tails interval directly from the quantile function. This page explains the mathematical basis and demonstrates the method across several distributions.

!!! tip "Mental Model"
    The `.interval()` method chops off equal probability from both tails and returns the central region. For a 95% interval, it finds the values at the 2.5th and 97.5th percentiles. This is the distribution-level building block that confidence intervals for parameters are constructed from.

---

## Equal-Tails Interval

For a continuous random variable $X$ with CDF $F$ and quantile function $F^{-1}$, the **equal-tails interval** at confidence level $\alpha$ is the pair $(a, b)$ satisfying:

$$
P(a < X < b) = \alpha
$$

with equal probability in each tail:

$$
P(X < a) = \frac{1 - \alpha}{2}, \qquad P(X > b) = \frac{1 - \alpha}{2}
$$

The endpoints are therefore:

$$
a = F^{-1}\!\left(\frac{1 - \alpha}{2}\right), \qquad b = F^{-1}\!\left(\frac{1 + \alpha}{2}\right)
$$

This is the interval that `.interval()` returns.

## The .interval() Method

Every `scipy.stats` continuous distribution provides `.interval(confidence, *args, **kwds)`:

```python
import scipy.stats as stats

# 95% interval for the standard normal
a, b = stats.norm.interval(0.95, loc=0, scale=1)
print(f"[{a:.4f}, {b:.4f}]")
# [-1.9600, 1.9600]
```

The method accepts the same shape, `loc`, and `scale` parameters as other distribution methods. The return value is a tuple `(a, b)`.

### Example: Normal Distribution

For a normal distribution with mean $\mu$ and standard deviation $\sigma$, the 95% interval spans approximately $\mu \pm 1.96\sigma$:

```python
mu, sigma = 100, 15
a, b = stats.norm.interval(0.95, loc=mu, scale=sigma)
print(f"95% interval: [{a:.2f}, {b:.2f}]")
# 95% interval: [70.60, 129.40]
```

### Example: Student's t-Distribution

The $t$-distribution has heavier tails than the normal, so its intervals are wider for the same confidence level. This is the distribution used when constructing confidence intervals for the mean with unknown population variance:

```python
df = 10
a, b = stats.t.interval(0.95, df=df, loc=0, scale=1)
print(f"95% t-interval (df={df}): [{a:.4f}, {b:.4f}]")
# Wider than [-1.96, 1.96]
```

As $\text{df} \to \infty$, the $t$-interval converges to the normal interval.

### Example: Chi-Square Distribution

The chi-square distribution is not symmetric, so the equal-tails interval is not centered at the mean:

```python
df = 10
a, b = stats.chi2.interval(0.95, df=df)
print(f"95% chi2-interval (df={df}): [{a:.4f}, {b:.4f}]")
```

This asymmetry is visible in the unequal distances from $a$ and $b$ to the distribution's mean $\text{df} = 10$.

## Connection to Confidence Intervals for the Mean

The most common application of `.interval()` is constructing a confidence interval for a population mean $\mu$ from sample data. Given a sample of size $n$ with sample mean $\bar{x}$ and sample standard deviation $s$, the $100\alpha\%$ confidence interval is:

$$
\bar{x} \pm t_{\alpha, n-1} \cdot \frac{s}{\sqrt{n}}
$$

where $t_{\alpha, n-1}$ is the critical value from the $t$-distribution. Using `.interval()`:

```python
import numpy as np

rng = np.random.default_rng(42)
data = rng.normal(loc=50, scale=10, size=30)

x_bar = np.mean(data)
se = stats.sem(data)  # standard error = s / sqrt(n)

a, b = stats.t.interval(0.95, df=len(data) - 1, loc=x_bar, scale=se)
print(f"95% CI for the mean: [{a:.2f}, {b:.2f}]")
```

Here `loc=x_bar` centers the interval at the sample mean and `scale=se` scales it by the standard error.

## .interval() vs Manual ppf Computation

The `.interval()` method is a convenience wrapper around two calls to `.ppf()`. The following are equivalent:

```python
# Using .interval()
a1, b1 = stats.norm.interval(0.95, loc=0, scale=1)

# Using .ppf() directly
a2 = stats.norm.ppf(0.025, loc=0, scale=1)
b2 = stats.norm.ppf(0.975, loc=0, scale=1)

# a1 == a2 and b1 == b2
```

For a detailed discussion of the quantile function, see the [Quantile Function (ppf, isf)](ppf_isf.md) page.

!!! note "Equal-tails vs shortest interval"
    The `.interval()` method always returns the equal-tails interval, which places the same probability in each tail. For symmetric distributions (normal, $t$), this is also the shortest interval. For skewed distributions (chi-square, gamma), the shortest interval has unequal tail probabilities and must be computed separately.

## Summary

The `.interval()` method computes the equal-tails probability interval $[F^{-1}((1-\alpha)/2),\; F^{-1}((1+\alpha)/2)]$ for any `scipy.stats` distribution. Combined with sample statistics for `loc` and `scale`, it provides a direct route to confidence intervals for population parameters. For non-symmetric distributions, the equal-tails interval differs from the shortest-length interval.

---

## Exercises

**Exercise 1.**
Use `stats.norm.interval(0.95, loc=0, scale=1)` to compute the 95% equal-tails interval for the standard normal. Verify that the endpoints match $\pm z_{0.025}$ from `.ppf()`.

??? success "Solution to Exercise 1"

        from scipy import stats

        lo, hi = stats.norm.interval(0.95, loc=0, scale=1)
        z_low = stats.norm.ppf(0.025)
        z_high = stats.norm.ppf(0.975)

        print(f"interval(): [{lo:.4f}, {hi:.4f}]")
        print(f"ppf():      [{z_low:.4f}, {z_high:.4f}]")

---

**Exercise 2.**
A sample of 25 observations has mean 80 and standard deviation 12. Use `stats.t.interval()` to construct a 95% confidence interval for the population mean. Compare the width with the corresponding z-interval.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        n, xbar, s = 25, 80, 12
        se = s / np.sqrt(n)

        ci_t = stats.t.interval(0.95, df=n-1, loc=xbar, scale=se)
        ci_z = stats.norm.interval(0.95, loc=xbar, scale=se)

        print(f"t-interval:  [{ci_t[0]:.2f}, {ci_t[1]:.2f}], width={ci_t[1]-ci_t[0]:.2f}")
        print(f"z-interval:  [{ci_z[0]:.2f}, {ci_z[1]:.2f}], width={ci_z[1]-ci_z[0]:.2f}")

---

**Exercise 3.**
Compute the 90%, 95%, and 99% equal-tails intervals for a chi-square distribution with 10 degrees of freedom. Print each interval and show how the interval width increases with confidence level.

??? success "Solution to Exercise 3"

        from scipy import stats

        rv = stats.chi2(df=10)
        for conf in [0.90, 0.95, 0.99]:
            lo, hi = rv.interval(conf)
            print(f"{conf*100:.0f}% CI: [{lo:.4f}, {hi:.4f}], width={hi-lo:.4f}")
