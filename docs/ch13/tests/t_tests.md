# t-Tests

The t-test is the fundamental tool for comparing means when the population standard deviation is unknown. Unlike the z-test, which requires known variance, the t-test estimates variance from the sample and uses the heavier-tailed t-distribution to account for this additional uncertainty. SciPy provides three variants: one-sample, independent two-sample, and paired.

!!! tip "Mental Model"
    The t-test standardizes a difference in means by dividing by the estimated standard error, producing a signal-to-noise ratio. A large $|t|$ means the observed difference is many standard errors away from zero -- unlikely under the null. SciPy's three functions map to three scenarios: one sample vs. a known value, two independent groups, and two paired measurements.

## One-Sample t-Test

The one-sample t-test determines whether a sample mean differs significantly from a hypothesized population mean $\mu_0$.

The hypotheses are

$$
H_0: \mu = \mu_0 \quad \text{vs} \quad H_1: \mu \neq \mu_0
$$

The test statistic is

$$
t = \frac{\bar{X} - \mu_0}{s / \sqrt{n}}
$$

where $\bar{X}$ is the sample mean, $s$ is the sample standard deviation, and $n$ is the sample size. Under $H_0$, the statistic follows a t-distribution with $n - 1$ degrees of freedom:

$$
t \sim t_{n-1}
$$

**Assumptions**: the data are independent and approximately normally distributed (the test is robust to moderate non-normality for $n \geq 30$).

```python
from scipy import stats

# Test whether the mean differs from 50
data = [52.1, 48.3, 51.7, 49.8, 53.2, 50.5, 47.9, 51.0]
t_stat, p_value = stats.ttest_1samp(data, popmean=50)
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

## Independent Two-Sample t-Test

The independent two-sample t-test compares the means of two unrelated groups. This is the most commonly used t-test variant.

The hypotheses are

$$
H_0: \mu_1 = \mu_2 \quad \text{vs} \quad H_1: \mu_1 \neq \mu_2
$$

When the two groups have equal variances (the pooled t-test), the test statistic is

$$
t = \frac{\bar{X}_1 - \bar{X}_2}{s_p \sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}
$$

where $s_p$ is the pooled standard deviation:

$$
s_p = \sqrt{\frac{(n_1 - 1)s_1^2 + (n_2 - 1)s_2^2}{n_1 + n_2 - 2}}
$$

Under $H_0$, the statistic follows $t_{n_1 + n_2 - 2}$.

### Welch's t-Test

When the equal-variance assumption is questionable, Welch's t-test provides a more reliable alternative. The test statistic uses separate variance estimates:

$$
t = \frac{\bar{X}_1 - \bar{X}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}
$$

The degrees of freedom are approximated by the Welch-Satterthwaite equation:

$$
\nu = \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1 - 1} + \frac{(s_2^2/n_2)^2}{n_2 - 1}}
$$

!!! tip "Default to Welch's Test"
    Welch's t-test performs well even when variances are equal, with minimal power loss. Many statisticians recommend using it by default. In SciPy, set `equal_var=False` to use Welch's version.

**Assumptions**: independent samples, each group is approximately normally distributed.

```python
from scipy import stats

group_a = [23.1, 25.3, 24.8, 22.9, 26.1, 24.5]
group_b = [28.4, 30.1, 27.6, 29.8, 31.2, 28.9]

# Pooled t-test (assumes equal variances)
t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=True)
print(f"Pooled t-test: t = {t_stat:.4f}, p = {p_value:.6f}")

# Welch's t-test (does not assume equal variances)
t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
print(f"Welch's t-test: t = {t_stat:.4f}, p = {p_value:.6f}")
```

## Paired t-Test

The paired t-test compares means from the same subjects measured under two conditions (e.g., before and after a treatment). By analyzing within-subject differences, it controls for individual variability.

Given paired observations $(X_{1i}, X_{2i})$, define the differences $D_i = X_{1i} - X_{2i}$. The test reduces to a one-sample t-test on the differences:

$$
H_0: \mu_D = 0 \quad \text{vs} \quad H_1: \mu_D \neq 0
$$

$$
t = \frac{\bar{D}}{s_D / \sqrt{n}}
$$

where $\bar{D}$ and $s_D$ are the mean and standard deviation of the differences, and $n$ is the number of pairs. Under $H_0$, the statistic follows $t_{n-1}$.

**Assumptions**: the differences $D_i$ are independent and approximately normally distributed. The original measurements need not be normal — only the differences must be.

```python
from scipy import stats

before = [120, 135, 128, 142, 130, 125, 138]
after = [115, 128, 122, 138, 125, 118, 132]
t_stat, p_value = stats.ttest_rel(before, after)
print(f"Paired t-test: t = {t_stat:.4f}, p = {p_value:.4f}")
```

## Summary of t-Test Variants

| Variant | SciPy Function | Use Case | Degrees of Freedom |
|---|---|---|---|
| One-sample | `ttest_1samp` | Sample mean vs known value | $n - 1$ |
| Independent (pooled) | `ttest_ind(equal_var=True)` | Two independent groups, equal variance | $n_1 + n_2 - 2$ |
| Independent (Welch) | `ttest_ind(equal_var=False)` | Two independent groups, unequal variance | Welch-Satterthwaite $\nu$ |
| Paired | `ttest_rel` | Same subjects, two conditions | $n - 1$ (number of pairs) |

## Summary

The three t-test variants address distinct experimental designs: one-sample tests compare a single group to a reference value, independent tests compare two separate groups, and paired tests compare two measurements on the same subjects. All three share the same core structure of forming a t-ratio (signal divided by estimated noise) and comparing it to the t-distribution, differing only in how the signal, noise, and degrees of freedom are computed.

---

## Runnable Example: `statistical_tests.py`

```python
"""
Tutorial 04: Statistical Tests in scipy.stats
=============================================
Level: Intermediate
Topics: t-tests, chi-square tests, ANOVA, normality tests, Mann-Whitney U,
        Wilcoxon, Kruskal-Wallis, and other hypothesis tests

This module covers the most common statistical hypothesis tests available
in scipy.stats for comparing means, distributions, and relationships.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings

if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    # Set random seed for reproducibility
    np.random.seed(42)

    # =============================================================================
    # SECTION 1: Introduction to Hypothesis Testing
    # =============================================================================
    """
    Hypothesis Testing Framework:
    ------------------------------
    1. State null hypothesis (H₀) and alternative hypothesis (H₁)
    2. Choose significance level (α), typically 0.05
    3. Calculate test statistic from sample data
    4. Determine p-value: probability of observing data as extreme as ours, assuming H₀ is true
    5. Decision:
       - If p-value ≤ α: Reject H₀ (result is "statistically significant")
       - If p-value > α: Fail to reject H₀ (insufficient evidence)

    Types of Errors:
    - Type I Error (α): Rejecting H₀ when it's true (false positive)
    - Type II Error (β): Failing to reject H₀ when it's false (false negative)
    - Power = 1 - β: Probability of correctly rejecting false H₀
    """

    print("="*80)
    print("STATISTICAL HYPOTHESIS TESTS")
    print("="*80)
    print()

    # =============================================================================
    # SECTION 2: One-Sample t-Test
    # =============================================================================
    """
    Tests if the mean of a single sample differs from a hypothesized value.

    H₀: μ = μ₀ (population mean equals hypothesized value)
    H₁: μ ≠ μ₀ (two-tailed) or μ > μ₀ or μ < μ₀ (one-tailed)

    Test statistic: t = (x̄ - μ₀) / (s / √n)
    where x̄ is sample mean, s is sample std dev, n is sample size

    Assumptions:
    - Data is approximately normally distributed (or n ≥ 30 by CLT)
    - Random sample
    """

    print("ONE-SAMPLE t-TEST")
    print("-" * 40)

    # Example: Testing if average student test score differs from 75
    scores = np.array([78, 82, 75, 88, 72, 90, 85, 77, 83, 79, 
                       81, 76, 84, 80, 86, 74, 89, 73, 87, 91])
    hypothesized_mean = 75

    # Perform one-sample t-test
    t_statistic, p_value = stats.ttest_1samp(scores, hypothesized_mean)

    print(f"Sample data: n={len(scores)}, mean={np.mean(scores):.2f}, std={np.std(scores, ddof=1):.2f}")
    print(f"Hypothesized mean: μ₀ = {hypothesized_mean}")
    print(f"Test statistic: t = {t_statistic:.4f}")
    print(f"P-value (two-tailed): {p_value:.4f}")
    print()

    alpha = 0.05
    if p_value < alpha:
        print(f"Decision: Reject H₀ (p={p_value:.4f} < α={alpha})")
        print(f"Conclusion: Sample mean ({np.mean(scores):.2f}) significantly differs from {hypothesized_mean}")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_value:.4f} ≥ α={alpha})")
        print(f"Conclusion: Insufficient evidence that mean differs from {hypothesized_mean}")
    print()

    # Confidence interval for the mean
    confidence_level = 0.95
    df = len(scores) - 1
    t_critical = stats.t.ppf((1 + confidence_level) / 2, df)
    margin_of_error = t_critical * (np.std(scores, ddof=1) / np.sqrt(len(scores)))
    ci_lower = np.mean(scores) - margin_of_error
    ci_upper = np.mean(scores) + margin_of_error

    print(f"{confidence_level*100:.0f}% Confidence Interval for mean: [{ci_lower:.2f}, {ci_upper:.2f}]")
    print()

    # =============================================================================
    # SECTION 3: Two-Sample t-Test (Independent Samples)
    # =============================================================================
    """
    Tests if the means of two independent samples differ.

    H₀: μ₁ = μ₂ (population means are equal)
    H₁: μ₁ ≠ μ₂ (two-tailed) or μ₁ > μ₂ or μ₁ < μ₂ (one-tailed)

    Two versions:
    1. Student's t-test: assumes equal variances
    2. Welch's t-test: does not assume equal variances (default in scipy)

    Assumptions:
    - Both samples are approximately normally distributed
    - Random and independent samples
    """

    print("TWO-SAMPLE t-TEST (Independent)")
    print("-" * 40)

    # Example: Comparing test scores between two teaching methods
    method_A = np.array([78, 82, 75, 88, 72, 90, 85, 77, 83, 79])
    method_B = np.array([85, 88, 91, 84, 89, 92, 87, 90, 86, 93, 88, 85])

    print(f"Method A: n={len(method_A)}, mean={np.mean(method_A):.2f}, std={np.std(method_A, ddof=1):.2f}")
    print(f"Method B: n={len(method_B)}, mean={np.mean(method_B):.2f}, std={np.std(method_B, ddof=1):.2f}")
    print()

    # Test for equal variances (Levene's test)
    levene_stat, levene_p = stats.levene(method_A, method_B)
    print(f"Levene's test for equal variances: p={levene_p:.4f}")
    if levene_p > 0.05:
        print("  → Variances are approximately equal")
        equal_var = True
    else:
        print("  → Variances are significantly different")
        equal_var = False
    print()

    # Perform two-sample t-test
    t_stat, p_val = stats.ttest_ind(method_A, method_B, equal_var=equal_var)

    print(f"Test statistic: t = {t_stat:.4f}")
    print(f"P-value (two-tailed): {p_val:.4f}")
    print()

    if p_val < alpha:
        print(f"Decision: Reject H₀ (p={p_val:.4f} < α={alpha})")
        print("Conclusion: Teaching methods produce significantly different results")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_val:.4f} ≥ α={alpha})")
        print("Conclusion: No significant difference between teaching methods")
    print()

    # Effect size: Cohen's d
    pooled_std = np.sqrt(((len(method_A)-1)*np.var(method_A, ddof=1) + 
                          (len(method_B)-1)*np.var(method_B, ddof=1)) / 
                         (len(method_A) + len(method_B) - 2))
    cohens_d = (np.mean(method_B) - np.mean(method_A)) / pooled_std
    print(f"Effect size (Cohen's d): {cohens_d:.4f}")
    print("  Interpretation: |d| < 0.2 (small), 0.2-0.8 (medium), > 0.8 (large)")
    print()

    # =============================================================================
    # SECTION 4: Paired t-Test (Dependent Samples)
    # =============================================================================
    """
    Tests if the mean difference between paired observations is zero.

    H₀: μ_d = 0 (mean difference is zero)
    H₁: μ_d ≠ 0 (mean difference is non-zero)

    Used for:
    - Before-after measurements
    - Matched pairs
    - Repeated measures

    Test statistic: t = d̄ / (s_d / √n)
    where d̄ is mean of differences, s_d is std dev of differences
    """

    print("PAIRED t-TEST (Dependent Samples)")
    print("-" * 40)

    # Example: Weight before and after diet program
    before = np.array([85, 92, 78, 88, 95, 82, 90, 87, 93, 80])
    after = np.array([82, 89, 76, 85, 91, 80, 87, 84, 90, 78])

    differences = after - before
    mean_diff = np.mean(differences)
    print(f"Before: mean={np.mean(before):.2f}, std={np.std(before, ddof=1):.2f}")
    print(f"After:  mean={np.mean(after):.2f}, std={np.std(after, ddof=1):.2f}")
    print(f"Mean difference: {mean_diff:.2f} kg")
    print()

    # Perform paired t-test
    t_paired, p_paired = stats.ttest_rel(before, after)

    print(f"Test statistic: t = {t_paired:.4f}")
    print(f"P-value (two-tailed): {p_paired:.4f}")
    print()

    if p_paired < alpha:
        print(f"Decision: Reject H₀ (p={p_paired:.4f} < α={alpha})")
        print("Conclusion: Diet program has significant effect on weight")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_paired:.4f} ≥ α={alpha})")
        print("Conclusion: No significant effect of diet program")
    print()

    # Visualize paired data
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    x = np.arange(len(before))
    plt.plot(x, before, 'o-', label='Before', markersize=8)
    plt.plot(x, after, 's-', label='After', markersize=8)
    for i in range(len(before)):
        plt.plot([i, i], [before[i], after[i]], 'k-', alpha=0.3)
    plt.xlabel('Subject')
    plt.ylabel('Weight (kg)')
    plt.title('Paired Measurements: Before vs After')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.hist(differences, bins=7, edgecolor='black', alpha=0.7)
    plt.axvline(0, color='red', linestyle='--', linewidth=2, label='No change')
    plt.axvline(mean_diff, color='blue', linestyle='-', linewidth=2, label=f'Mean diff = {mean_diff:.2f}')
    plt.xlabel('Weight Change (kg)')
    plt.ylabel('Frequency')
    plt.title('Distribution of Weight Changes')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/04_paired_test.png', dpi=300, bbox_inches='tight')
    print("Saved: 04_paired_test.png\n")
    plt.close()

    # =============================================================================
    # SECTION 5: Chi-Square Test for Independence
    # =============================================================================
    """
    Tests if two categorical variables are independent.

    H₀: Variables are independent
    H₁: Variables are associated (dependent)

    Test statistic: χ² = Σ [(O - E)² / E]
    where O is observed frequency, E is expected frequency

    Assumptions:
    - Expected frequency ≥ 5 in at least 80% of cells
    - Expected frequency ≥ 1 in all cells
    """

    print("CHI-SQUARE TEST FOR INDEPENDENCE")
    print("-" * 40)

    # Example: Relationship between smoking and lung disease
    # Rows: Smoker/Non-smoker, Columns: Disease/No Disease
    observed = np.array([[45, 65],   # Smokers: Disease, No Disease
                         [15, 95]])   # Non-smokers: Disease, No Disease

    print("Contingency Table:")
    print("                  Disease    No Disease")
    print(f"Smokers            {observed[0,0]:3d}        {observed[0,1]:3d}")
    print(f"Non-smokers        {observed[1,0]:3d}        {observed[1,1]:3d}")
    print()

    # Perform chi-square test
    chi2_stat, p_chi, dof, expected = stats.chi2_contingency(observed)

    print(f"Chi-square statistic: χ² = {chi2_stat:.4f}")
    print(f"Degrees of freedom: {dof}")
    print(f"P-value: {p_chi:.4f}")
    print()

    print("Expected frequencies (under independence):")
    print("                  Disease    No Disease")
    print(f"Smokers          {expected[0,0]:6.2f}     {expected[0,1]:6.2f}")
    print(f"Non-smokers      {expected[1,0]:6.2f}     {expected[1,1]:6.2f}")
    print()

    if p_chi < alpha:
        print(f"Decision: Reject H₀ (p={p_chi:.4f} < α={alpha})")
        print("Conclusion: Smoking and lung disease are associated")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_chi:.4f} ≥ α={alpha})")
        print("Conclusion: No significant association found")
    print()

    # Cramér's V (effect size for chi-square)
    n = np.sum(observed)
    min_dim = min(observed.shape[0], observed.shape[1]) - 1
    cramers_v = np.sqrt(chi2_stat / (n * min_dim))
    print(f"Cramér's V (effect size): {cramers_v:.4f}")
    print("  Interpretation: V < 0.1 (small), 0.1-0.3 (medium), > 0.3 (large)")
    print()

    # =============================================================================
    # SECTION 6: Chi-Square Goodness-of-Fit Test
    # =============================================================================
    """
    Tests if observed frequencies match expected frequencies.

    H₀: Data follows the specified distribution
    H₁: Data does not follow the specified distribution
    """

    print("CHI-SQUARE GOODNESS-OF-FIT TEST")
    print("-" * 40)

    # Example: Testing if a die is fair
    rolls = np.array([12, 18, 15, 14, 16, 13])  # Observed frequencies
    expected_freq = np.array([15, 15, 15, 15, 15, 15])  # Expected if fair (88 total rolls)

    print(f"Die rolls observed: {rolls}")
    print(f"Expected (fair die): {expected_freq}")
    print()

    # Perform goodness-of-fit test
    chi2_gof, p_gof = stats.chisquare(rolls, expected_freq)

    print(f"Chi-square statistic: χ² = {chi2_gof:.4f}")
    print(f"P-value: {p_gof:.4f}")
    print()

    if p_gof < alpha:
        print(f"Decision: Reject H₀ (p={p_gof:.4f} < α={alpha})")
        print("Conclusion: Die is likely not fair")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_gof:.4f} ≥ α={alpha})")
        print("Conclusion: Data consistent with fair die")
    print()

    # =============================================================================
    # SECTION 7: One-Way ANOVA (Analysis of Variance)
    # =============================================================================
    """
    Tests if means of three or more groups are equal.

    H₀: μ₁ = μ₂ = μ₃ = ... (all group means are equal)
    H₁: At least one mean differs

    F-statistic: F = (Between-group variance) / (Within-group variance)

    Assumptions:
    - Normal distribution within each group
    - Equal variances across groups (homoscedasticity)
    - Independent observations
    """

    print("ONE-WAY ANOVA")
    print("-" * 40)

    # Example: Comparing productivity across three work schedules
    schedule_A = np.array([82, 85, 88, 84, 86, 83, 87, 85, 89, 84])
    schedule_B = np.array([90, 92, 88, 91, 93, 89, 92, 90, 94, 91])
    schedule_C = np.array([85, 87, 86, 88, 84, 86, 87, 85, 89, 86])

    print(f"Schedule A: mean={np.mean(schedule_A):.2f}, std={np.std(schedule_A, ddof=1):.2f}")
    print(f"Schedule B: mean={np.mean(schedule_B):.2f}, std={np.std(schedule_B, ddof=1):.2f}")
    print(f"Schedule C: mean={np.mean(schedule_C):.2f}, std={np.std(schedule_C, ddof=1):.2f}")
    print()

    # Test for equal variances across groups
    bartlett_stat, bartlett_p = stats.bartlett(schedule_A, schedule_B, schedule_C)
    print(f"Bartlett's test for equal variances: p={bartlett_p:.4f}")
    print()

    # Perform one-way ANOVA
    f_stat, p_anova = stats.f_oneway(schedule_A, schedule_B, schedule_C)

    print(f"F-statistic: F = {f_stat:.4f}")
    print(f"P-value: {p_anova:.4f}")
    print()

    if p_anova < alpha:
        print(f"Decision: Reject H₀ (p={p_anova:.4f} < α={alpha})")
        print("Conclusion: At least one schedule produces different results")
        print("  → Follow up with post-hoc tests (e.g., Tukey HSD) to identify which groups differ")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_anova:.4f} ≥ α={alpha})")
        print("Conclusion: No significant difference among schedules")
    print()

    # Visualize ANOVA
    plt.figure(figsize=(10, 6))
    data_anova = [schedule_A, schedule_B, schedule_C]
    positions = [1, 2, 3]
    bp = plt.boxplot(data_anova, positions=positions, widths=0.6, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    plt.xticks(positions, ['Schedule A', 'Schedule B', 'Schedule C'])
    plt.ylabel('Productivity Score')
    plt.title('One-Way ANOVA: Productivity by Work Schedule')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/04_anova.png', dpi=300, bbox_inches='tight')
    print("Saved: 04_anova.png\n")
    plt.close()

    # =============================================================================
    # SECTION 8: Mann-Whitney U Test (Non-parametric Alternative to t-test)
    # =============================================================================
    """
    Tests if two independent samples come from the same distribution.
    Non-parametric alternative to independent t-test.

    H₀: Distributions are equal
    H₁: Distributions differ

    Advantages:
    - Does not assume normality
    - Robust to outliers
    - Works with ordinal data

    Use when:
    - Data is not normally distributed
    - Small sample sizes
    - Presence of outliers
    """

    print("MANN-WHITNEY U TEST (Non-parametric)")
    print("-" * 40)

    # Example: Comparing reaction times (may not be normal due to outliers)
    group1 = np.array([12, 15, 13, 18, 14, 16, 15, 40])  # Note outlier: 40
    group2 = np.array([20, 22, 21, 24, 19, 23, 22, 21])

    print(f"Group 1: median={np.median(group1):.1f}, IQR={np.percentile(group1, 75)-np.percentile(group1, 25):.1f}")
    print(f"Group 2: median={np.median(group2):.1f}, IQR={np.percentile(group2, 75)-np.percentile(group2, 25):.1f}")
    print()

    # Perform Mann-Whitney U test
    u_stat, p_mann = stats.mannwhitneyu(group1, group2, alternative='two-sided')

    print(f"U-statistic: U = {u_stat:.4f}")
    print(f"P-value: {p_mann:.4f}")
    print()

    if p_mann < alpha:
        print(f"Decision: Reject H₀ (p={p_mann:.4f} < α={alpha})")
        print("Conclusion: Groups have significantly different distributions")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_mann:.4f} ≥ α={alpha})")
        print("Conclusion: No significant difference in distributions")
    print()

    # Compare with t-test (for illustration)
    t_with_outlier, p_t = stats.ttest_ind(group1, group2)
    print(f"For comparison, t-test p-value: {p_t:.4f}")
    print("  (t-test is affected by the outlier in group1)")
    print()

    # =============================================================================
    # SECTION 9: Wilcoxon Signed-Rank Test (Non-parametric Paired Test)
    # =============================================================================
    """
    Non-parametric alternative to paired t-test.
    Tests if median difference between paired samples is zero.

    H₀: Median difference is zero
    H₁: Median difference is non-zero

    Use when:
    - Paired data is not normally distributed
    - Small sample sizes
    - Ordinal data
    """

    print("WILCOXON SIGNED-RANK TEST (Non-parametric Paired)")
    print("-" * 40)

    # Example: Pain scores before and after treatment (ordinal scale 1-10)
    pain_before = np.array([8, 7, 9, 6, 8, 7, 9, 8, 7, 6])
    pain_after = np.array([5, 6, 7, 5, 6, 4, 6, 5, 5, 4])

    print(f"Before: median={np.median(pain_before):.1f}")
    print(f"After:  median={np.median(pain_after):.1f}")
    print()

    # Perform Wilcoxon signed-rank test
    w_stat, p_wilcoxon = stats.wilcoxon(pain_before, pain_after)

    print(f"W-statistic: W = {w_stat:.4f}")
    print(f"P-value: {p_wilcoxon:.4f}")
    print()

    if p_wilcoxon < alpha:
        print(f"Decision: Reject H₀ (p={p_wilcoxon:.4f} < α={alpha})")
        print("Conclusion: Treatment significantly reduces pain")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_wilcoxon:.4f} ≥ α={alpha})")
        print("Conclusion: No significant effect of treatment")
    print()

    # =============================================================================
    # SECTION 10: Kruskal-Wallis H Test (Non-parametric Alternative to ANOVA)
    # =============================================================================
    """
    Tests if three or more groups come from the same distribution.
    Non-parametric alternative to one-way ANOVA.

    H₀: All groups have the same distribution
    H₁: At least one group differs

    Use when:
    - Data is not normally distributed
    - Ordinal data
    - Presence of outliers
    """

    print("KRUSKAL-WALLIS H TEST (Non-parametric ANOVA)")
    print("-" * 40)

    # Example: Customer satisfaction scores (ordinal scale) across three stores
    store1 = np.array([3, 4, 3, 5, 4, 3, 4, 5, 3, 4])
    store2 = np.array([4, 5, 5, 5, 4, 5, 5, 4, 5, 5])
    store3 = np.array([3, 3, 4, 3, 2, 3, 4, 3, 3, 4])

    print(f"Store 1: median={np.median(store1):.1f}")
    print(f"Store 2: median={np.median(store2):.1f}")
    print(f"Store 3: median={np.median(store3):.1f}")
    print()

    # Perform Kruskal-Wallis H test
    h_stat, p_kruskal = stats.kruskal(store1, store2, store3)

    print(f"H-statistic: H = {h_stat:.4f}")
    print(f"P-value: {p_kruskal:.4f}")
    print()

    if p_kruskal < alpha:
        print(f"Decision: Reject H₀ (p={p_kruskal:.4f} < α={alpha})")
        print("Conclusion: At least one store has different satisfaction distribution")
    else:
        print(f"Decision: Fail to reject H₀ (p={p_kruskal:.4f} ≥ α={alpha})")
        print("Conclusion: No significant difference among stores")
    print()

    # =============================================================================
    # SECTION 11: Tests for Normality
    # =============================================================================
    """
    Several tests to check if data is normally distributed.

    Common tests:
    1. Shapiro-Wilk: Good for small to medium samples (n < 5000)
    2. Kolmogorov-Smirnov: Compares with reference distribution
    3. Anderson-Darling: More weight to tail values
    4. D'Agostino-Pearson: Based on skewness and kurtosis
    """

    print("NORMALITY TESTS")
    print("-" * 40)

    # Generate test data
    normal_data = np.random.normal(0, 1, 100)
    uniform_data = np.random.uniform(-2, 2, 100)
    exponential_data = np.random.exponential(2, 100)

    datasets = [
        ("Normal", normal_data),
        ("Uniform", uniform_data),
        ("Exponential", exponential_data)
    ]

    for name, data in datasets:
        print(f"\n{name} data:")

        # Shapiro-Wilk test
        shapiro_stat, shapiro_p = stats.shapiro(data)
        print(f"  Shapiro-Wilk: W={shapiro_stat:.4f}, p={shapiro_p:.4f}", end="")
        print(f" → {'Normal' if shapiro_p > alpha else 'Not normal'}")

        # Kolmogorov-Smirnov test
        ks_stat, ks_p = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data, ddof=1)))
        print(f"  Kolmogorov-Smirnov: D={ks_stat:.4f}, p={ks_p:.4f}", end="")
        print(f" → {'Normal' if ks_p > alpha else 'Not normal'}")

        # Anderson-Darling test
        anderson_result = stats.anderson(data, dist='norm')
        print(f"  Anderson-Darling: A²={anderson_result.statistic:.4f}")
        print(f"    Critical values: {anderson_result.critical_values}")
        print(f"    Significance levels: {anderson_result.significance_level}")

    print()

    # Visualize normality
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    for i, (name, data) in enumerate(datasets):
        # Histogram with normal curve overlay
        axes[0, i].hist(data, bins=20, density=True, alpha=0.7, edgecolor='black')
        x_range = np.linspace(data.min(), data.max(), 100)
        axes[0, i].plot(x_range, stats.norm.pdf(x_range, np.mean(data), np.std(data, ddof=1)), 
                        'r-', linewidth=2, label='Normal fit')
        axes[0, i].set_title(f'{name} Data - Histogram')
        axes[0, i].legend()
        axes[0, i].grid(True, alpha=0.3)

        # Q-Q plot
        stats.probplot(data, dist="norm", plot=axes[1, i])
        axes[1, i].set_title(f'{name} Data - Q-Q Plot')
        axes[1, i].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/04_normality_tests.png', dpi=300, bbox_inches='tight')
    print("Saved: 04_normality_tests.png\n")
    plt.close()

    # =============================================================================
    # SECTION 12: Summary Table
    # =============================================================================

    print("="*80)
    print("SUMMARY: When to Use Each Test")
    print("="*80)

    test_guide = """
    Test Type               Use When                              Assumptions
    --------------------------------------------------------------------------------
    One-sample t-test       Compare sample mean to value         Normal or n≥30
    Two-sample t-test       Compare two independent means        Normal, independent
    Paired t-test           Compare paired measurements          Normal differences
    Chi-square test         Test categorical associations        Expected freq ≥ 5
    Goodness-of-fit         Test distribution fit                Expected freq ≥ 5
    One-way ANOVA           Compare 3+ independent means         Normal, equal var
    Mann-Whitney U          Compare 2 independent (non-param)    None (ordinal OK)
    Wilcoxon signed-rank    Compare paired (non-parametric)      None (ordinal OK)
    Kruskal-Wallis          Compare 3+ groups (non-parametric)   None (ordinal OK)
    Shapiro-Wilk            Test normality                       n < 5000
    """

    print(test_guide)

    print("\n" + "="*80)
    print("Tutorial 04 Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("1. Choose parametric tests (t-tests, ANOVA) when assumptions are met")
    print("2. Use non-parametric tests when data is not normal or has outliers")
    print("3. Always check test assumptions before proceeding")
    print("4. P-value indicates strength of evidence against null hypothesis")
    print("5. Statistical significance (p<0.05) doesn't always mean practical importance")
    print("6. Report effect sizes along with p-values for complete picture")
    print("7. Multiple comparisons require adjustment (e.g., Bonferroni correction)")
```

---

## Exercises

**Exercise 1.**
A sample of 15 light bulbs has lifetimes (in hours): 1020, 980, 1050, 990, 1010, 1030, 960, 1040, 1000, 1020, 970, 1060, 1010, 985, 1025. Test whether the mean lifetime differs from 1000 hours at $\alpha = 0.05$.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        data = [1020, 980, 1050, 990, 1010, 1030, 960, 1040, 1000, 1020, 970, 1060, 1010, 985, 1025]
        t_stat, p_val = stats.ttest_1samp(data, 1000)
        print(f"t = {t_stat:.4f}, p = {p_val:.4f}")
        print(f"Decision: {'Reject H0' if p_val < 0.05 else 'Fail to reject H0'}")

---

**Exercise 2.**
Two groups of students took different prep courses. Group A scores: 78, 85, 90, 72, 88. Group B scores: 82, 91, 95, 88, 93. Perform both a pooled t-test and Welch's t-test. Compare the results.

??? success "Solution to Exercise 2"

        from scipy import stats

        a = [78, 85, 90, 72, 88]
        b = [82, 91, 95, 88, 93]

        t_pooled, p_pooled = stats.ttest_ind(a, b, equal_var=True)
        t_welch, p_welch = stats.ttest_ind(a, b, equal_var=False)

        print(f"Pooled: t={t_pooled:.4f}, p={p_pooled:.4f}")
        print(f"Welch:  t={t_welch:.4f}, p={p_welch:.4f}")

---

**Exercise 3.**
Blood pressure was measured before and after a medication for 8 patients: before = [140, 135, 150, 145, 138, 142, 148, 136], after = [132, 130, 145, 140, 135, 138, 142, 130]. Perform a paired t-test and compute Cohen's $d_z$ for the paired differences.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        before = np.array([140, 135, 150, 145, 138, 142, 148, 136])
        after = np.array([132, 130, 145, 140, 135, 138, 142, 130])

        t_stat, p_val = stats.ttest_rel(before, after)
        diff = after - before
        d_z = np.mean(diff) / np.std(diff, ddof=1)

        print(f"Paired t-test: t={t_stat:.4f}, p={p_val:.4f}")
        print(f"Cohen's d_z: {d_z:.4f}")
