# Non-Parametric Tests

Parametric tests such as the t-test and ANOVA assume that data follow a specific distribution, typically normal. When these assumptions are violated — due to heavy tails, skewness, or small sample sizes — non-parametric tests provide valid alternatives. These tests make minimal distributional assumptions, often relying on ranks rather than raw values, which makes them robust to outliers and applicable to ordinal data.

!!! tip "Mental Model"
    Non-parametric tests replace raw values with ranks, making them immune to outliers and valid for any continuous distribution. The Mann-Whitney U test is the rank-based counterpart of the two-sample t-test; the Wilcoxon signed-rank test replaces the paired t-test; and the Kruskal-Wallis test replaces one-way ANOVA. The trade-off is slightly less power when the parametric assumptions actually hold.

## Mann-Whitney U Test

The Mann-Whitney U test is the non-parametric counterpart of the independent two-sample t-test. It compares two independent groups to determine whether one tends to produce larger values than the other.

The null and alternative hypotheses are

$$
H_0: P(X > Y) = 0.5 \quad \text{vs} \quad H_1: P(X > Y) \neq 0.5
$$

where $X$ and $Y$ are observations from the two groups. Equivalently, $H_0$ states that the two distributions are identical.

To compute the test statistic, combine both samples and rank all $N = n_1 + n_2$ observations. Let $R_1$ be the sum of ranks assigned to group 1. The U-statistic for group 1 is

$$
U_1 = R_1 - \frac{n_1(n_1 + 1)}{2}
$$

$U_1$ counts the number of times an observation from group 1 precedes an observation from group 2. For large samples, $U_1$ is approximately normal under $H_0$.

**Assumptions**: independent samples, at least ordinal measurement scale, and similar distribution shapes (if testing for a location shift).

```python
from scipy import stats

group1 = [23, 25, 28, 30, 35]
group2 = [18, 20, 22, 24, 27]
u_stat, p_value = stats.mannwhitneyu(group1, group2, alternative='two-sided')
print(f"U-statistic: {u_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Wilcoxon Signed-Rank Test

The Wilcoxon signed-rank test is the non-parametric counterpart of the paired t-test. It tests whether the median of paired differences is zero.

Given paired observations $(X_i, Y_i)$, compute the differences $D_i = X_i - Y_i$. The hypotheses are

$$
H_0: \text{median}(D) = 0 \quad \text{vs} \quad H_1: \text{median}(D) \neq 0
$$

The procedure ranks the absolute differences $|D_i|$ (discarding zeros), then sums the ranks of positive and negative differences separately:

$$
W^+ = \sum_{D_i > 0} R_i, \qquad W^- = \sum_{D_i < 0} R_i
$$

The test statistic is $W = \min(W^+, W^-)$. Small values of $W$ indicate that the differences are systematically positive or negative.

**Assumptions**: paired samples, the distribution of differences is symmetric about the median, and at least ordinal measurement scale.

```python
from scipy import stats

before = [68, 72, 65, 70, 74, 69, 71]
after = [64, 69, 60, 66, 70, 65, 67]
w_stat, p_value = stats.wilcoxon(before, after)
print(f"W-statistic: {w_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Kruskal-Wallis Test

The Kruskal-Wallis test extends the Mann-Whitney U test to $k \geq 2$ independent groups, serving as the non-parametric alternative to one-way ANOVA. It tests whether all groups share the same distribution.

The hypotheses are

$$
H_0: F_1 = F_2 = \cdots = F_k \quad \text{vs} \quad H_1: F_i \neq F_j \text{ for some } i \neq j
$$

Rank all $N$ observations across groups. Let $\bar{R}_i$ be the mean rank for group $i$ and $\bar{R} = (N+1)/2$ the overall mean rank. The test statistic is

$$
H = \frac{12}{N(N+1)} \sum_{i=1}^{k} n_i (\bar{R}_i - \bar{R})^2
$$

Under $H_0$ and for sufficiently large group sizes, $H$ approximately follows a $\chi^2_{k-1}$ distribution.

**Assumptions**: independent samples, at least ordinal measurement scale, and similar distribution shapes across groups.

!!! warning "Post-Hoc Comparisons"
    A significant Kruskal-Wallis result indicates that at least one group differs, but does not identify which pairs differ. Use Dunn's test with a multiple comparison correction (e.g., Bonferroni) for pairwise follow-up.

```python
from scipy import stats

g1 = [23, 25, 28, 30, 35]
g2 = [18, 20, 22, 24, 27]
g3 = [30, 33, 36, 39, 42]
h_stat, p_value = stats.kruskal(g1, g2, g3)
print(f"H-statistic: {h_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Comparison with Parametric Tests

| Non-Parametric Test | Parametric Counterpart | Use Case |
|---|---|---|
| Mann-Whitney U | Independent two-sample t-test | Comparing two independent groups |
| Wilcoxon signed-rank | Paired t-test | Comparing paired observations |
| Kruskal-Wallis | One-way ANOVA | Comparing three or more groups |

Non-parametric tests are less powerful than their parametric counterparts when the parametric assumptions hold, particularly for large samples from normal distributions. However, when those assumptions are violated, non-parametric tests can be more powerful because they are not distorted by the violation.

## Summary

Non-parametric tests provide distribution-free alternatives to common parametric tests. The Mann-Whitney U, Wilcoxon signed-rank, and Kruskal-Wallis tests handle two-sample, paired, and multi-group comparisons respectively, using ranks rather than raw values. They are the preferred choice when normality assumptions are questionable, when working with ordinal data, or when samples are too small for the central limit theorem to provide adequate approximation.

---

## Exercises

**Exercise 1.**
Two groups of pain ratings (ordinal 1-10): Group A = [3, 5, 4, 6, 3, 5], Group B = [7, 8, 6, 9, 7, 8]. Perform a Mann-Whitney U test and interpret the result.

??? success "Solution to Exercise 1"

        from scipy import stats

        a = [3, 5, 4, 6, 3, 5]
        b = [7, 8, 6, 9, 7, 8]
        u_stat, p = stats.mannwhitneyu(a, b, alternative='two-sided')
        print(f"U={u_stat:.4f}, p={p:.4f}")
        print(f"{'Significant' if p < 0.05 else 'Not significant'} difference")

---

**Exercise 2.**
Before and after treatment ratings: before = [8, 7, 9, 6, 8, 7], after = [5, 6, 7, 4, 5, 5]. Perform both a Wilcoxon signed-rank test and a paired t-test. Compare the p-values.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        before = [8, 7, 9, 6, 8, 7]
        after = [5, 6, 7, 4, 5, 5]

        w_stat, p_wilcox = stats.wilcoxon(before, after)
        t_stat, p_ttest = stats.ttest_rel(before, after)

        print(f"Wilcoxon: W={w_stat:.4f}, p={p_wilcox:.4f}")
        print(f"Paired t: t={t_stat:.4f}, p={p_ttest:.4f}")

---

**Exercise 3.**
Three groups of customer satisfaction scores: Store A = [4, 5, 3, 4, 5], Store B = [7, 8, 6, 7, 8], Store C = [5, 6, 5, 4, 6]. Perform a Kruskal-Wallis test and, if significant, explain what follow-up analysis is needed.

??? success "Solution to Exercise 3"

        from scipy import stats

        a = [4, 5, 3, 4, 5]
        b = [7, 8, 6, 7, 8]
        c = [5, 6, 5, 4, 6]
        h_stat, p = stats.kruskal(a, b, c)
        print(f"H={h_stat:.4f}, p={p:.4f}")
        if p < 0.05:
            print("Significant — follow up with Dunn's test for pairwise comparisons")
