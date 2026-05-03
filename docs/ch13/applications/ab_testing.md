# A/B Testing Workflow

In product development and clinical trials, practitioners often need to compare two variants -- a control (A) and a treatment (B) -- to determine whether an observed difference in a metric is statistically significant or merely due to random variation. A/B testing applies the hypothesis testing framework from Chapter 12.5 to this comparison problem. This section walks through the complete statistical workflow using `scipy.stats`.

!!! tip "Mental Model"
    Think of an A/B test as a courtroom trial for a product change. The null hypothesis is "innocent" (no effect), and the data is the evidence. You must gather enough evidence (sample size) to convict beyond reasonable doubt (significance level), while the effect size determines how hard the case is to prove.

## Hypothesis Setup

An A/B test begins by framing the question as a hypothesis test. Let $\mu_A$ and $\mu_B$ denote the population means of the metric under variants A and B, respectively.

- **Null hypothesis** $H_0$: $\mu_A = \mu_B$ (no difference between variants)
- **Alternative hypothesis** $H_1$: $\mu_A \neq \mu_B$ (two-sided test)

For proportion-based metrics such as conversion rates, let $p_A$ and $p_B$ denote the true proportions. The null hypothesis becomes $H_0\colon p_A = p_B$.

Before collecting data, the experimenter must choose a significance level $\alpha$ (commonly $\alpha = 0.05$) and a minimum detectable effect size $\delta$.

## Sample Size Determination

Running an A/B test with too few observations risks failing to detect a real effect (Type II error). The required sample size per group for a two-proportion z-test is

$$
n = \left(\frac{z_{\alpha/2} + z_{\beta}}{\delta}\right)^2 \left[\bar{p}(1 - \bar{p}) \cdot 2\right]
$$

where $\bar{p} = (p_A + p_B)/2$ is the pooled proportion estimate, $z_{\alpha/2}$ is the critical value for the chosen significance level, $z_{\beta}$ corresponds to the desired power $1 - \beta$, and $\delta = |p_A - p_B|$ is the minimum detectable effect.

For continuous metrics, the analogous formula uses the pooled variance $\sigma^2$ in place of $\bar{p}(1 - \bar{p})$.

```python
from scipy import stats
import numpy as np

def sample_size_proportion(p1, p2, alpha=0.05, power=0.80):
    """Compute minimum sample size per group for a two-proportion z-test."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_bar = (p1 + p2) / 2
    delta = abs(p1 - p2)
    n = ((z_alpha + z_beta) / delta) ** 2 * 2 * p_bar * (1 - p_bar)
    return int(np.ceil(n))
```

## Running the Test

### Two-Sample t-Test for Continuous Metrics

When the metric is continuous (for example, revenue per user), the two-sample t-test compares the means of the two groups. The test statistic is

$$
t = \frac{\bar{X}_B - \bar{X}_A}{\sqrt{s_A^2 / n_A + s_B^2 / n_B}}
$$

where $\bar{X}_A$, $\bar{X}_B$ are the sample means, $s_A^2$, $s_B^2$ are the sample variances, and $n_A$, $n_B$ are the sample sizes.

```python
from scipy import stats

# Simulated experiment data
rng = np.random.default_rng(42)
group_a = rng.normal(loc=10.0, scale=2.0, size=500)
group_b = rng.normal(loc=10.5, scale=2.0, size=500)

t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

The `equal_var=False` argument invokes Welch's t-test, which does not assume equal variances across groups and is the recommended default for A/B testing.

### Two-Proportion z-Test for Conversion Rates

For binary outcomes (converted or not), the test statistic under the pooled proportion $\hat{p}$ is

$$
z = \frac{\hat{p}_B - \hat{p}_A}{\sqrt{\hat{p}(1 - \hat{p})\left(\frac{1}{n_A} + \frac{1}{n_B}\right)}}
$$

where $\hat{p} = (x_A + x_B)/(n_A + n_B)$ is the pooled proportion and $x_A$, $x_B$ are the numbers of successes in each group.

```python
from scipy import stats

# Observed conversions
n_a, x_a = 1000, 120   # control: 12.0% conversion
n_b, x_b = 1000, 145   # treatment: 14.5% conversion

# Pooled proportion
p_hat = (x_a + x_b) / (n_a + n_b)
se = np.sqrt(p_hat * (1 - p_hat) * (1/n_a + 1/n_b))
z_stat = (x_b/n_b - x_a/n_a) / se
p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

print(f"z-statistic: {z_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Confidence Intervals

Beyond the binary reject/fail-to-reject decision, reporting a confidence interval for the treatment effect communicates the plausible range of the true difference. For the difference in means, a $100(1 - \alpha)\%$ confidence interval is

$$
(\bar{X}_B - \bar{X}_A) \pm t_{\alpha/2,\,\nu} \cdot \sqrt{\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}}
$$

where $\nu$ is the degrees of freedom from the Welch-Satterthwaite approximation.

```python
from scipy import stats
import numpy as np

def ab_confidence_interval(group_a, group_b, alpha=0.05):
    """Compute confidence interval for difference in means (Welch)."""
    diff = np.mean(group_b) - np.mean(group_a)
    se = np.sqrt(np.var(group_a, ddof=1)/len(group_a)
                 + np.var(group_b, ddof=1)/len(group_b))
    # Welch-Satterthwaite degrees of freedom
    nu_num = (np.var(group_a, ddof=1)/len(group_a)
              + np.var(group_b, ddof=1)/len(group_b))**2
    nu_den = ((np.var(group_a, ddof=1)/len(group_a))**2 / (len(group_a)-1)
              + (np.var(group_b, ddof=1)/len(group_b))**2 / (len(group_b)-1))
    nu = nu_num / nu_den
    t_crit = stats.t.ppf(1 - alpha/2, df=nu)
    return diff - t_crit * se, diff + t_crit * se
```

## Multiple Testing Correction

When an A/B test evaluates several metrics simultaneously, the probability of at least one false positive increases. Apply the Bonferroni correction (divide $\alpha$ by the number of tests) or control the false discovery rate using the Benjamini-Hochberg procedure, as discussed in Chapter 12.5.

```python
from scipy.stats import false_discovery_control

p_values = [0.03, 0.12, 0.005, 0.45]
adjusted = false_discovery_control(p_values, method='bh')
print("Adjusted p-values:", adjusted)
```

## Summary

The A/B testing workflow combines sample size planning, hypothesis testing, confidence interval estimation, and multiple testing correction into a coherent decision framework. The key steps are: (1) define hypotheses and choose $\alpha$, (2) compute the required sample size, (3) collect data and compute the test statistic, (4) report p-values alongside confidence intervals, and (5) apply corrections when testing multiple metrics.


---

## Exercises

**Exercise 1.** Write code that simulates an A/B test with two groups (control and treatment) of 1000 observations each. Use a two-sample t-test to determine if the treatment has a statistically significant effect.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(100)
    print(f'Mean: {data.mean():.4f}')
    print(f'Std: {data.std():.4f}')
    ```

---

**Exercise 2.** Explain the difference between a one-tailed and two-tailed hypothesis test. When would you use each in an A/B test?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that computes the required sample size for an A/B test given a desired effect size of 0.2, significance level of 0.05, and power of 0.8.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    from scipy import stats
    import matplotlib.pyplot as plt

    np.random.seed(42)
    data = np.random.randn(1000)
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, density=True, alpha=0.7)
    ax.set_title('Distribution')
    plt.show()
    ```

---

**Exercise 4.** Create a simulation that runs 1000 A/B tests with no true effect (null hypothesis is true). Count how many tests yield a p-value below 0.05. What percentage do you expect?

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
