# Confidence Intervals

A point estimate like a sample mean gives a single best guess for a population parameter, but it says nothing about how precise that guess is. Confidence intervals address this gap by providing a range of plausible values for the parameter, together with a stated level of confidence. They are the natural complement to hypothesis tests: a 95% confidence interval contains exactly those parameter values that a two-sided test at the 5% level would fail to reject.

!!! tip "Mental Model"
    A confidence interval is a net, not a bullseye. The 95% in "95% confidence" means that if you cast this net repeatedly across many samples, 95% of the nets would catch the true parameter. Any single net either caught it or missed -- you just do not know which. Wider intervals reflect more uncertainty; narrower intervals reflect more data or less variability.

---

## Definition and Interpretation

A **confidence interval** at level $1 - \alpha$ for a parameter $\theta$ is a random interval $[L, U]$ computed from sample data such that

$$
P(L \le \theta \le U) = 1 - \alpha
$$

The confidence level $1 - \alpha$ refers to the long-run coverage rate of the procedure, not to the probability that a specific realized interval contains $\theta$. Once the data are observed and the interval is computed, $\theta$ is either inside or outside — the interval is no longer random.

!!! warning "Common Misinterpretation"
    A 95% confidence interval does **not** mean "there is a 95% probability that $\theta$ lies in this interval." It means that if we repeated the sampling procedure many times, 95% of the resulting intervals would contain $\theta$.

---

## Confidence Interval for a Mean

### Known Variance (z-interval)

When the population variance $\sigma^2$ is known and the data are normally distributed (or $n$ is large enough for the CLT to apply), the confidence interval for the population mean $\mu$ is

$$
\bar{X} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}
$$

where $z_{\alpha/2}$ is the upper $\alpha/2$ quantile of the standard normal distribution.

```python
import numpy as np
from scipy import stats

# Simulated data with known population std
np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=30)
sigma = 10  # Known population std

# 95% z-interval
alpha = 0.05
z_crit = stats.norm.ppf(1 - alpha / 2)
margin = z_crit * sigma / np.sqrt(len(data))
ci = (np.mean(data) - margin, np.mean(data) + margin)
print(f"Sample mean: {np.mean(data):.2f}")
print(f"95% CI (z): ({ci[0]:.2f}, {ci[1]:.2f})")
```

### Unknown Variance (t-interval)

When $\sigma$ is unknown and estimated by the sample standard deviation $s$, the interval uses the $t$-distribution with $n - 1$ degrees of freedom:

$$
\bar{X} \pm t_{\alpha/2,\, n-1} \cdot \frac{s}{\sqrt{n}}
$$

```python
# t-interval (unknown variance) using scipy
mean = np.mean(data)
se = stats.sem(data)  # Standard error of the mean
ci_t = stats.t.interval(0.95, df=len(data) - 1, loc=mean, scale=se)
print(f"95% CI (t): ({ci_t[0]:.2f}, {ci_t[1]:.2f})")
```

The $t$-interval is wider than the $z$-interval because the extra uncertainty from estimating $\sigma$ inflates the critical value. As $n \to \infty$, $t_{\alpha/2,\, n-1} \to z_{\alpha/2}$.

---

## Confidence Interval for a Proportion

For a population proportion $p$ estimated by the sample proportion $\hat{p} = X / n$, the Wald interval is

$$
\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1 - \hat{p})}{n}}
$$

This approximation relies on the normal approximation to the binomial and works well when $n\hat{p}$ and $n(1 - \hat{p})$ are both at least 10.

```python
# Proportion confidence interval
n_trials = 200
n_successes = 130
p_hat = n_successes / n_trials

z_crit = stats.norm.ppf(0.975)
margin = z_crit * np.sqrt(p_hat * (1 - p_hat) / n_trials)
ci_prop = (p_hat - margin, p_hat + margin)
print(f"Sample proportion: {p_hat:.3f}")
print(f"95% CI: ({ci_prop[0]:.3f}, {ci_prop[1]:.3f})")
```

!!! tip "Wilson Interval for Small Samples"
    The Wald interval can have poor coverage when $n$ is small or $p$ is near 0 or 1. The Wilson score interval provides better coverage in these cases:

    ```python
    from statsmodels.stats.proportion import proportion_confint
    ci_wilson = proportion_confint(n_successes, n_trials, method='wilson')
    print(f"Wilson CI: ({ci_wilson[0]:.3f}, {ci_wilson[1]:.3f})")
    ```

---

## Confidence Interval Width

The half-width (margin of error) of a confidence interval depends on three factors:

1. **Confidence level** $1 - \alpha$: higher confidence requires a larger critical value, producing a wider interval
2. **Sample size** $n$: larger samples reduce the standard error $\sigma / \sqrt{n}$, producing a narrower interval
3. **Variability** $\sigma$: more variable populations produce wider intervals

The required sample size for a desired margin of error $E$ in a z-interval is

$$
n = \left\lceil \left( \frac{z_{\alpha/2} \cdot \sigma}{E} \right)^2 \right\rceil
$$

```python
# Required sample size for margin of error = 2 with sigma = 10
desired_margin = 2.0
sigma = 10.0
z_crit = stats.norm.ppf(0.975)
n_required = np.ceil((z_crit * sigma / desired_margin) ** 2)
print(f"Required n for margin = {desired_margin}: {n_required:.0f}")
```

---

## Relationship to Hypothesis Testing

A two-sided hypothesis test at significance level $\alpha$ and a $(1 - \alpha)$ confidence interval are equivalent:

- Reject $H_0: \mu = \mu_0$ if and only if $\mu_0$ falls outside the $(1 - \alpha)$ confidence interval
- Fail to reject $H_0$ if and only if $\mu_0$ falls inside the interval

```python
# Equivalence demonstration
np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=30)

# Hypothesis test: H0: mu = 48
mu_0 = 48
t_stat, p_value = stats.ttest_1samp(data, mu_0)
print(f"t-test p-value: {p_value:.4f}")

# Confidence interval
mean = np.mean(data)
se = stats.sem(data)
ci = stats.t.interval(0.95, df=len(data) - 1, loc=mean, scale=se)
print(f"95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")
print(f"mu_0 = {mu_0} in CI: {ci[0] <= mu_0 <= ci[1]}")
print(f"Reject H0: {p_value < 0.05}")
```

---

## Bootstrap Confidence Intervals

When the sampling distribution of the estimator is unknown or difficult to derive analytically, bootstrap methods construct confidence intervals by resampling from the observed data.

```python
from scipy.stats import bootstrap

# Bootstrap CI for the mean
np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=30)

# scipy.stats.bootstrap requires a tuple of arrays
result = bootstrap(
    (data,),
    statistic=np.mean,
    n_resamples=9999,
    confidence_level=0.95,
    method='percentile'
)
print(f"Bootstrap 95% CI: ({result.confidence_interval.low:.2f}, "
      f"{result.confidence_interval.high:.2f})")
```

The `method` parameter controls which bootstrap interval is computed:

- `'percentile'`: uses quantiles of the bootstrap distribution directly
- `'basic'`: reflects the bootstrap distribution around the sample estimate
- `'bca'`: bias-corrected and accelerated — adjusts for bias and skewness

---

## Summary

Confidence intervals quantify the precision of point estimates by providing a range of plausible values for the population parameter. The key formulas are the z-interval (known variance) and t-interval (unknown variance) for means, and the Wald or Wilson interval for proportions. The interval width shrinks with larger sample sizes and lower confidence levels. A $(1 - \alpha)$ confidence interval is equivalent to the set of parameter values not rejected by a two-sided test at level $\alpha$. When analytical formulas are unavailable, bootstrap methods provide a flexible nonparametric alternative.

---

## Exercises

**Exercise 1.**
Generate 40 samples from $N(75, 8^2)$. Compute both the z-interval (assuming $\sigma = 8$ is known) and the t-interval for a 95% confidence interval. Compare the widths and explain why the t-interval is wider.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = np.random.normal(75, 8, 40)
        xbar = np.mean(data)
        n = len(data)

        z_margin = stats.norm.ppf(0.975) * 8 / np.sqrt(n)
        ci_z = (xbar - z_margin, xbar + z_margin)

        se = stats.sem(data)
        ci_t = stats.t.interval(0.95, df=n-1, loc=xbar, scale=se)

        print(f"z-interval: ({ci_z[0]:.2f}, {ci_z[1]:.2f}), width={2*z_margin:.2f}")
        print(f"t-interval: ({ci_t[0]:.2f}, {ci_t[1]:.2f}), width={ci_t[1]-ci_t[0]:.2f}")

---

**Exercise 2.**
In a survey, 180 out of 300 respondents favor a policy. Compute the 95% Wald confidence interval and the Wilson confidence interval (using `statsmodels.stats.proportion.proportion_confint`) for the population proportion.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats
        from statsmodels.stats.proportion import proportion_confint

        n, x = 300, 180
        p_hat = x / n
        z = stats.norm.ppf(0.975)
        margin = z * np.sqrt(p_hat * (1 - p_hat) / n)
        ci_wald = (p_hat - margin, p_hat + margin)
        ci_wilson = proportion_confint(x, n, method='wilson')

        print(f"Wald CI:   ({ci_wald[0]:.4f}, {ci_wald[1]:.4f})")
        print(f"Wilson CI: ({ci_wilson[0]:.4f}, {ci_wilson[1]:.4f})")

---

**Exercise 3.**
Use `scipy.stats.bootstrap` to compute a 95% bootstrap confidence interval for the median of 50 samples drawn from an exponential distribution with $\lambda = 1$. Compare the bootstrap CI with the theoretical median $\ln 2 \approx 0.693$.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy.stats import bootstrap

        np.random.seed(42)
        data = np.random.exponential(1, size=50)
        result = bootstrap((data,), statistic=np.median,
                           n_resamples=9999, confidence_level=0.95,
                           random_state=42)
        print(f"Bootstrap 95% CI for median: "
              f"({result.confidence_interval.low:.3f}, "
              f"{result.confidence_interval.high:.3f})")
        print(f"Theoretical median: {np.log(2):.3f}")
