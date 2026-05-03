# Power Analysis

Before collecting data, a researcher needs to know how many observations are required to detect an effect of practical interest. An underpowered study wastes resources because it is unlikely to find a real effect even if one exists, while an overpowered study collects more data than necessary. Power analysis answers this question by quantifying the relationship between four interrelated quantities: significance level, effect size, sample size, and statistical power.

!!! tip "Mental Model"
    Power analysis is the study design equation: significance level, effect size, sample size, and power are four knobs connected by one constraint. Fix any three and the fourth is determined. In practice, you fix $\alpha = 0.05$, target power $= 0.80$, estimate the effect size from prior work, and solve for the sample size you need.

---

## Statistical Power

The **power** of a test is the probability of correctly rejecting $H_0$ when $H_1$ is true:

$$
\text{Power} = 1 - \beta = P(\text{reject } H_0 \mid H_1 \text{ true})
$$

where $\beta$ is the Type II error rate (probability of failing to reject a false $H_0$). A conventional target is power $\ge 0.80$, meaning the study has at least an 80% chance of detecting the effect if it exists.

---

## The Four-Way Relationship

Power analysis connects four quantities, any one of which can be solved from the other three:

| Quantity | Symbol | Typical Value |
|---|---|---|
| Significance level | $\alpha$ | 0.05 |
| Power | $1 - \beta$ | 0.80 |
| Effect size | $d$, $f$, $r$, etc. | Varies by context |
| Sample size | $n$ | Solved for |

```python
from statsmodels.stats.power import tt_solve_power, TTestIndPower

# Solve for sample size given the other three
n = tt_solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                   alternative='two-sided')
print(f"Required n per group (d=0.5): {n:.0f}")

# Solve for power given sample size
power = tt_solve_power(effect_size=0.5, alpha=0.05, nobs=30,
                       alternative='two-sided')
print(f"Power with n=30 (d=0.5): {power:.3f}")

# Solve for detectable effect size
d = tt_solve_power(nobs=30, alpha=0.05, power=0.80,
                   alternative='two-sided')
print(f"Detectable effect size (n=30): {d:.3f}")
```

---

## Effect Size Conventions

Cohen's $d$ provides standardized benchmarks for the magnitude of a mean difference:

| Size | $d$ | Example |
|---|---|---|
| Small | 0.2 | Subtle difference, requires large $n$ to detect |
| Medium | 0.5 | Visible to careful observation |
| Large | 0.8 | Obvious difference, detectable with small $n$ |

Cohen's $d$ is defined as

$$
d = \frac{\mu_1 - \mu_2}{\sigma}
$$

where $\sigma$ is the common population standard deviation.

```python
import numpy as np

# Cohen's d from raw data
def cohens_d(group1, group2):
    """Compute Cohen's d for independent samples."""
    n1, n2 = len(group1), len(group2)
    s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
    s_pooled = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
    return (np.mean(group1) - np.mean(group2)) / s_pooled

np.random.seed(42)
g1 = np.random.normal(100, 15, 30)
g2 = np.random.normal(108, 15, 30)
d = cohens_d(g1, g2)
print(f"Cohen's d: {d:.3f}")
```

---

## Sample Size Determination

The required sample size for a two-sample $t$-test grows as the effect size shrinks. For a two-sided test at level $\alpha$ with power $1 - \beta$, the approximate sample size per group is

$$
n \approx \frac{2(z_{\alpha/2} + z_\beta)^2}{d^2}
$$

where $z_{\alpha/2}$ and $z_\beta$ are the standard normal quantiles corresponding to $\alpha/2$ and $\beta$.

```python
from scipy import stats

# Approximate formula
alpha = 0.05
power_target = 0.80
d = 0.5

z_alpha = stats.norm.ppf(1 - alpha / 2)
z_beta = stats.norm.ppf(power_target)
n_approx = 2 * (z_alpha + z_beta)**2 / d**2
print(f"Approximate n per group: {n_approx:.0f}")

# Exact calculation via statsmodels
n_exact = tt_solve_power(effect_size=d, alpha=alpha, power=power_target,
                         alternative='two-sided')
print(f"Exact n per group: {n_exact:.0f}")
```

---

## Power Curves

A power curve shows how power changes as a function of one parameter while holding the others fixed. This visualization helps researchers understand the trade-offs in study design.

```python
import numpy as np
from statsmodels.stats.power import TTestIndPower

analysis = TTestIndPower()

# Power as a function of sample size for different effect sizes
sample_sizes = np.arange(10, 201, 5)
effect_sizes = [0.2, 0.5, 0.8]

for d in effect_sizes:
    powers = [analysis.power(d, n, 0.05) for n in sample_sizes]
    print(f"d={d}: n=20 → power={analysis.power(d, 20, 0.05):.2f}, "
          f"n=100 → power={analysis.power(d, 100, 0.05):.2f}")
```

---

## Power for Other Tests

### Paired t-test

The paired design uses the effect size $d_z = \mu_D / \sigma_D$, where $\mu_D$ and $\sigma_D$ are the mean and standard deviation of the paired differences.

```python
from statsmodels.stats.power import tt_solve_power

# Paired t-test power (uses one-sample power with d_z)
n_paired = tt_solve_power(effect_size=0.5, alpha=0.05, power=0.80,
                          alternative='two-sided')
print(f"Required n (paired, d_z=0.5): {n_paired:.0f}")
```

### ANOVA (F-test)

For one-way ANOVA comparing $k$ groups, the effect size is Cohen's $f$:

$$
f = \sqrt{\frac{\sum_{i=1}^k n_i (\mu_i - \bar{\mu})^2}{k \cdot \sigma^2}}
$$

```python
from statsmodels.stats.power import FTestAnovaPower

anova_power = FTestAnovaPower()
n_anova = anova_power.solve_power(effect_size=0.25, alpha=0.05, power=0.80,
                                   k_groups=3)
print(f"Required n per group (ANOVA, f=0.25, k=3): {n_anova:.0f}")
```

### Chi-Square Test

For chi-square tests, the effect size is Cohen's $w$:

```python
from statsmodels.stats.power import GofChisquarePower

chi2_power = GofChisquarePower()
n_chi2 = chi2_power.solve_power(effect_size=0.3, alpha=0.05, power=0.80,
                                 n_bins=4)
print(f"Required n (chi-square, w=0.3): {n_chi2:.0f}")
```

---

## Post-Hoc Power Analysis

!!! warning "Observed Power is Uninformative"
    Computing power using the observed effect size after data collection (post-hoc or retrospective power) is widely discouraged. Observed power is a monotone function of the p-value and adds no information beyond what the p-value already provides. Power analysis is meaningful only when conducted before data collection, using a clinically or practically meaningful effect size.

---

## Summary

Power analysis determines the sample size needed to detect an effect of a specified magnitude with a given probability. The four key quantities — significance level $\alpha$, power $1 - \beta$, effect size, and sample size — are interrelated so that fixing any three determines the fourth. Conventional targets are $\alpha = 0.05$ and power $= 0.80$. Power curves visualize these trade-offs and help researchers choose an appropriate design. Power analysis should always be conducted before data collection, using a scientifically meaningful effect size rather than the observed effect.

---

## Exercises

**Exercise 1.**
Using `statsmodels.stats.power.tt_solve_power`, compute the required sample size to detect an effect size of $d = 0.3$ with 80% power at $\alpha = 0.05$ for a two-sided one-sample t-test.

??? success "Solution to Exercise 1"

        from statsmodels.stats.power import tt_solve_power

        n = tt_solve_power(effect_size=0.3, alpha=0.05, power=0.8,
                           alternative='two-sided')
        print(f"Required sample size: {n:.0f}")

---

**Exercise 2.**
Plot a power curve for a one-sample t-test with $n = 30$ at $\alpha = 0.05$: compute power for effect sizes $d = 0, 0.1, 0.2, \ldots, 1.0$ and plot power vs effect size.

??? success "Solution to Exercise 2"

        import numpy as np
        import matplotlib.pyplot as plt
        from statsmodels.stats.power import tt_solve_power

        effect_sizes = np.arange(0, 1.05, 0.1)
        powers = [tt_solve_power(effect_size=d, nobs=30, alpha=0.05,
                                  alternative='two-sided') if d > 0 else 0.05
                  for d in effect_sizes]

        plt.plot(effect_sizes, powers, 'o-')
        plt.axhline(0.8, ls='--', color='r', label='80% power')
        plt.xlabel('Effect Size (d)')
        plt.ylabel('Power')
        plt.title('Power Curve (n=30)')
        plt.legend()
        plt.show()

---

**Exercise 3.**
Compare the required sample sizes for 80% power at effect sizes $d = 0.2, 0.5, 0.8$ for both one-sided and two-sided tests. Show that the one-sided test always requires fewer subjects.

??? success "Solution to Exercise 3"

        from statsmodels.stats.power import tt_solve_power

        for d in [0.2, 0.5, 0.8]:
            n_two = tt_solve_power(effect_size=d, alpha=0.05, power=0.8,
                                    alternative='two-sided')
            n_one = tt_solve_power(effect_size=d, alpha=0.05, power=0.8,
                                    alternative='larger')
            print(f"d={d}: two-sided n={n_two:.0f}, one-sided n={n_one:.0f}")
