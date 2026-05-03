# ANOVA

When comparing means across more than two groups, running multiple pairwise t-tests inflates the overall Type I error rate. For example, with five groups there are ten pairwise comparisons, and even at $\alpha = 0.05$ per test the probability of at least one false rejection grows substantially. Analysis of Variance (ANOVA) solves this by testing all group means simultaneously in a single F-test, controlling the family-wise error rate.

!!! tip "Mental Model"
    ANOVA compares the variance between group means to the variance within groups. If the groups truly share the same mean, between-group variance should be similar to within-group variance and the F-ratio clusters near 1. A large F-ratio means the group means are more spread out than random noise would explain -- evidence that at least one group differs.

## One-Way ANOVA Model

The one-way ANOVA model assumes $k$ independent groups, where observations in group $i$ follow

$$
X_{ij} = \mu_i + \varepsilon_{ij}, \quad j = 1, \ldots, n_i
$$

with $\varepsilon_{ij} \overset{\text{iid}}{\sim} N(0, \sigma^2)$. The total sample size is $N = \sum_{i=1}^{k} n_i$.

The hypotheses are

$$
H_0: \mu_1 = \mu_2 = \cdots = \mu_k \quad \text{vs} \quad H_1: \mu_i \neq \mu_j \text{ for some } i \neq j
$$

## Sum of Squares Decomposition

ANOVA partitions the total variability into between-group and within-group components. Define the grand mean $\bar{X} = \frac{1}{N}\sum_{i=1}^{k}\sum_{j=1}^{n_i} X_{ij}$ and each group mean $\bar{X}_i = \frac{1}{n_i}\sum_{j=1}^{n_i} X_{ij}$. The decomposition is

$$
\underbrace{\sum_{i=1}^{k}\sum_{j=1}^{n_i}(X_{ij} - \bar{X})^2}_{\text{SST}} = \underbrace{\sum_{i=1}^{k} n_i (\bar{X}_i - \bar{X})^2}_{\text{SSB}} + \underbrace{\sum_{i=1}^{k}\sum_{j=1}^{n_i}(X_{ij} - \bar{X}_i)^2}_{\text{SSW}}
$$

where SST is the total sum of squares, SSB is the between-group sum of squares, and SSW is the within-group sum of squares.

## F-Statistic

The mean squares are

$$
\text{MSB} = \frac{\text{SSB}}{k - 1}, \qquad \text{MSW} = \frac{\text{SSW}}{N - k}
$$

The F-statistic is the ratio of between-group variance to within-group variance:

$$
F = \frac{\text{MSB}}{\text{MSW}}
$$

Under $H_0$, this statistic follows an $F$-distribution with degrees of freedom $k - 1$ and $N - k$:

$$
F \sim F_{k-1,\, N-k}
$$

Large values of $F$ indicate that the between-group variability is large relative to the within-group variability, providing evidence against $H_0$.

## Assumptions

One-way ANOVA requires three assumptions:

1. **Independence**: observations are independent both within and across groups.
2. **Normality**: each group is drawn from a normal distribution. ANOVA is moderately robust to departures from normality, especially with large sample sizes.
3. **Homoscedasticity**: all groups share the same variance $\sigma^2$. Use the Levene or Bartlett test to verify this assumption before running ANOVA.

!!! warning "Violation of Equal Variances"
    When the equal-variance assumption fails, the standard F-test can produce misleading p-values. Use Welch's ANOVA (`scipy.stats.alexandergovern`) or a non-parametric alternative such as the Kruskal-Wallis test.

## SciPy Implementation

The `scipy.stats.f_oneway` function computes the one-way ANOVA F-test:

```python
from scipy import stats

# Three treatment groups
group_a = [23.1, 25.3, 24.8, 22.9, 26.1]
group_b = [28.4, 30.1, 27.6, 29.8, 31.2]
group_c = [33.5, 35.2, 34.1, 32.8, 36.0]

f_stat, p_value = stats.f_oneway(group_a, group_b, group_c)
print(f"F-statistic: {f_stat:.4f}")
print(f"p-value: {p_value:.6f}")
```

The function returns the F-statistic and the corresponding p-value. Reject $H_0$ when the p-value is below the chosen significance level $\alpha$.

## ANOVA Table

Results are typically organized in an ANOVA table:

| Source | SS | df | MS | F |
|---|---|---|---|---|
| Between groups | SSB | $k - 1$ | MSB | $F = \text{MSB}/\text{MSW}$ |
| Within groups | SSW | $N - k$ | MSW | |
| Total | SST | $N - 1$ | | |

## Summary

ANOVA tests whether the means of multiple groups are equal by comparing between-group and within-group variability through the F-statistic. The key requirements are independence, normality, and equal variances across groups. In SciPy, `scipy.stats.f_oneway` provides a direct implementation for the one-way case.

---

## Exercises

**Exercise 1.**
Three fertilizers are tested on plant growth (cm): A = [20, 22, 19, 24, 21], B = [28, 30, 27, 29, 31], C = [25, 23, 26, 24, 27]. Perform a one-way ANOVA and compute eta-squared as the effect size.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        a = [20, 22, 19, 24, 21]
        b = [28, 30, 27, 29, 31]
        c = [25, 23, 26, 24, 27]

        f_stat, p_val = stats.f_oneway(a, b, c)
        all_data = np.concatenate([a, b, c])
        grand_mean = np.mean(all_data)
        ss_b = sum(len(g)*(np.mean(g)-grand_mean)**2 for g in [a,b,c])
        ss_t = np.sum((all_data - grand_mean)**2)
        eta_sq = ss_b / ss_t

        print(f"F={f_stat:.4f}, p={p_val:.6f}")
        print(f"Eta-squared: {eta_sq:.4f}")

---

**Exercise 2.**
Verify the equal-variance assumption for the three groups in Exercise 1 using Levene's test before running ANOVA. If the assumption fails, suggest an alternative.

??? success "Solution to Exercise 2"

        from scipy import stats

        a = [20, 22, 19, 24, 21]
        b = [28, 30, 27, 29, 31]
        c = [25, 23, 26, 24, 27]

        w_stat, p_val = stats.levene(a, b, c)
        print(f"Levene's test: W={w_stat:.4f}, p={p_val:.4f}")
        if p_val < 0.05:
            print("Unequal variances — use Kruskal-Wallis instead")
        else:
            print("Equal variances — ANOVA is appropriate")

---

**Exercise 3.**
Generate three groups from $N(50, 10^2)$ with $n = 30$ each (all null hypotheses true). Run ANOVA 1000 times and verify the false positive rate is approximately 5% at $\alpha = 0.05$.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        rejections = 0
        for _ in range(1000):
            g1 = np.random.normal(50, 10, 30)
            g2 = np.random.normal(50, 10, 30)
            g3 = np.random.normal(50, 10, 30)
            _, p = stats.f_oneway(g1, g2, g3)
            if p < 0.05:
                rejections += 1
        print(f"False positive rate: {rejections/1000:.3f} (expected ~0.05)")
