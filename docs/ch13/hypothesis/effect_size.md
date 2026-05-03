# Effect Size

A p-value tells you whether an observed effect is statistically significant, but it says nothing about how large or practically important that effect is. Effect size measures fill this gap by quantifying the magnitude of a difference or relationship on a standardized scale. Reporting effect sizes alongside p-values is now required by most major journals and is essential for power analysis and meta-analysis.

!!! tip "Mental Model"
    A p-value answers "is there an effect?" while effect size answers "how big is it?" With enough data, even a trivially small difference becomes statistically significant. Effect size strips away sample size to reveal the practical magnitude -- Cohen's $d = 0.2$ is a small nudge, $d = 0.8$ is a large shift.

---

## Cohen's d

Cohen's $d$ measures the standardized difference between two group means. For independent samples with equal variances, it is defined as

$$
d = \frac{\bar{X}_1 - \bar{X}_2}{s_p}
$$

where $s_p$ is the pooled standard deviation:

$$
s_p = \sqrt{\frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}}
$$

Cohen's conventional benchmarks for interpreting $d$:

| Effect Size | $d$ Value |
|---|---|
| Small | 0.2 |
| Medium | 0.5 |
| Large | 0.8 |

```python
import numpy as np
from scipy import stats

# Two groups
np.random.seed(42)
group1 = np.random.normal(loc=100, scale=15, size=50)
group2 = np.random.normal(loc=108, scale=15, size=50)

# Cohen's d (pooled std)
n1, n2 = len(group1), len(group2)
s1, s2 = np.std(group1, ddof=1), np.std(group2, ddof=1)
s_pooled = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
d = (np.mean(group1) - np.mean(group2)) / s_pooled
print(f"Cohen's d: {d:.3f}")
```

---

## Hedges' g

For small samples ($n < 20$), Cohen's $d$ overestimates the population effect size. Hedges' $g$ applies a correction factor:

$$
g = d \cdot \left(1 - \frac{3}{4(n_1 + n_2) - 9}\right)
$$

The correction factor approaches 1 as the total sample size grows, so $g \approx d$ for large samples.

```python
# Hedges' g correction
n_total = n1 + n2
correction = 1 - 3 / (4 * n_total - 9)
g = d * correction
print(f"Hedges' g: {g:.3f}")
print(f"Correction factor: {correction:.4f}")
```

---

## Glass's Delta

When the two groups have unequal variances, Glass's $\Delta$ uses only the control group's standard deviation as the denominator:

$$
\Delta = \frac{\bar{X}_1 - \bar{X}_2}{s_{\text{control}}}
$$

This is appropriate when the treatment is expected to change both the mean and the variance.

```python
# Glass's delta (using group2 as control)
delta = (np.mean(group1) - np.mean(group2)) / np.std(group2, ddof=1)
print(f"Glass's delta: {delta:.3f}")
```

---

## Effect Size for Paired Samples

For paired designs, Cohen's $d_z$ uses the standard deviation of the difference scores:

$$
d_z = \frac{\bar{D}}{s_D}
$$

where $\bar{D}$ is the mean of the paired differences and $s_D$ is their standard deviation.

```python
# Paired effect size
np.random.seed(42)
pre = np.random.normal(loc=100, scale=15, size=30)
post = pre + np.random.normal(loc=5, scale=8, size=30)  # Treatment adds ~5

diff = post - pre
d_z = np.mean(diff) / np.std(diff, ddof=1)
print(f"Cohen's d_z (paired): {d_z:.3f}")
```

---

## Eta-Squared and Partial Eta-Squared

For ANOVA designs, $\eta^2$ (eta-squared) quantifies the proportion of total variance explained by the factor:

$$
\eta^2 = \frac{SS_{\text{between}}}{SS_{\text{total}}}
$$

Partial eta-squared isolates the effect of one factor by removing the variance due to other factors:

$$
\eta_p^2 = \frac{SS_{\text{effect}}}{SS_{\text{effect}} + SS_{\text{error}}}
$$

| Effect Size | $\eta^2$ Value |
|---|---|
| Small | 0.01 |
| Medium | 0.06 |
| Large | 0.14 |

```python
# Eta-squared from one-way ANOVA
np.random.seed(42)
g1 = np.random.normal(50, 10, 30)
g2 = np.random.normal(55, 10, 30)
g3 = np.random.normal(60, 10, 30)

f_stat, p_val = stats.f_oneway(g1, g2, g3)

# Compute SS_between and SS_total
grand_mean = np.mean(np.concatenate([g1, g2, g3]))
ss_between = sum(len(g) * (np.mean(g) - grand_mean)**2 for g in [g1, g2, g3])
ss_total = np.sum((np.concatenate([g1, g2, g3]) - grand_mean)**2)
eta_sq = ss_between / ss_total

print(f"F = {f_stat:.2f}, p = {p_val:.4f}")
print(f"Eta-squared: {eta_sq:.3f}")
```

---

## Point-Biserial Correlation

When comparing two groups, the point-biserial correlation $r_{pb}$ is another effect size measure. It equals the Pearson correlation between the group membership variable (coded 0/1) and the outcome:

$$
r_{pb} = \frac{\bar{X}_1 - \bar{X}_2}{s_{\text{total}}} \sqrt{\frac{n_1 n_2}{n^2}}
$$

Cohen's $d$ and $r_{pb}$ are related by

$$
d = \frac{2r_{pb}}{\sqrt{1 - r_{pb}^2}}
$$

```python
# Point-biserial correlation
outcome = np.concatenate([group1, group2])
group_label = np.array([0] * len(group1) + [1] * len(group2))

r_pb, p_val = stats.pointbiserialr(group_label, outcome)
print(f"Point-biserial r: {r_pb:.3f}")

# Convert to Cohen's d
d_from_r = 2 * r_pb / np.sqrt(1 - r_pb**2)
print(f"Cohen's d from r: {d_from_r:.3f}")
```

---

## Confidence Intervals for Effect Sizes

Effect size estimates are themselves subject to sampling variability. A confidence interval for Cohen's $d$ can be obtained using the noncentral $t$-distribution. The noncentrality parameter is

$$
\lambda = d \sqrt{\frac{n_1 n_2}{n_1 + n_2}}
$$

```python
# CI for Cohen's d via noncentral t
from scipy.stats import nct

def cohens_d_ci(d, n1, n2, alpha=0.05):
    """Compute CI for Cohen's d using noncentral t."""
    df = n1 + n2 - 2
    ncp = d * np.sqrt(n1 * n2 / (n1 + n2))
    t_low = nct.ppf(alpha / 2, df, ncp)
    t_high = nct.ppf(1 - alpha / 2, df, ncp)
    d_low = t_low / np.sqrt(n1 * n2 / (n1 + n2))
    d_high = t_high / np.sqrt(n1 * n2 / (n1 + n2))
    return d_low, d_high

ci = cohens_d_ci(d, n1, n2)
print(f"95% CI for d: ({ci[0]:.3f}, {ci[1]:.3f})")
```

---

## Summary

Effect sizes quantify the magnitude of an observed effect on a standardized scale, complementing the binary significant/not-significant verdict of hypothesis tests. Cohen's $d$ and Hedges' $g$ measure standardized mean differences, $\eta^2$ captures variance explained in ANOVA, and the point-biserial $r$ expresses group differences as a correlation. Always report effect sizes with confidence intervals to communicate both the estimated magnitude and its precision.

---

## Exercises

**Exercise 1.**
Generate two groups of 40 samples each from $N(100, 15^2)$ and $N(108, 15^2)$. Compute Cohen's $d$ and Hedges' $g$. Classify the effect size using Cohen's benchmarks.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        g1 = np.random.normal(100, 15, 40)
        g2 = np.random.normal(108, 15, 40)

        n1, n2 = len(g1), len(g2)
        s_pooled = np.sqrt(((n1-1)*np.var(g1,ddof=1) + (n2-1)*np.var(g2,ddof=1)) / (n1+n2-2))
        d = (np.mean(g2) - np.mean(g1)) / s_pooled
        g = d * (1 - 3 / (4*(n1+n2) - 9))

        print(f"Cohen's d: {d:.3f}")
        print(f"Hedges' g: {g:.3f}")
        print(f"Classification: {'Large' if abs(d)>0.8 else 'Medium' if abs(d)>0.5 else 'Small'}")

---

**Exercise 2.**
Compute eta-squared ($\eta^2$) for a one-way ANOVA with three groups: $N(50, 10^2)$, $N(55, 10^2)$, and $N(65, 10^2)$ (30 samples each). Classify the effect size as small, medium, or large.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        g1 = np.random.normal(50, 10, 30)
        g2 = np.random.normal(55, 10, 30)
        g3 = np.random.normal(65, 10, 30)

        all_data = np.concatenate([g1, g2, g3])
        grand_mean = np.mean(all_data)
        ss_between = sum(len(g)*(np.mean(g)-grand_mean)**2 for g in [g1,g2,g3])
        ss_total = np.sum((all_data - grand_mean)**2)
        eta_sq = ss_between / ss_total

        print(f"Eta-squared: {eta_sq:.3f}")
        print(f"Classification: {'Large' if eta_sq>0.14 else 'Medium' if eta_sq>0.06 else 'Small'}")

---

**Exercise 3.**
For two groups of size 30 from $N(0, 1)$ and $N(0.5, 1)$, compute both the point-biserial correlation $r_{pb}$ (using `stats.pointbiserialr`) and Cohen's $d$. Convert $d$ to $r$ using the formula $r = d / \sqrt{d^2 + 4}$ and verify it matches.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        g1 = np.random.normal(0, 1, 30)
        g2 = np.random.normal(0.5, 1, 30)

        outcome = np.concatenate([g1, g2])
        labels = np.array([0]*30 + [1]*30)
        r_pb, _ = stats.pointbiserialr(labels, outcome)

        s_p = np.sqrt(((29)*np.var(g1,ddof=1)+(29)*np.var(g2,ddof=1))/58)
        d = (np.mean(g2) - np.mean(g1)) / s_p
        r_from_d = d / np.sqrt(d**2 + 4)

        print(f"Point-biserial r: {r_pb:.4f}")
        print(f"Cohen's d: {d:.4f}")
        print(f"r from d formula: {r_from_d:.4f}")
