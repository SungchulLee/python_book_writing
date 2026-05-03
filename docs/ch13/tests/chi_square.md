# Chi-Square Tests

Chi-square tests evaluate whether observed frequencies in categorical data differ significantly from expected frequencies. These tests are among the most widely used tools for analyzing count data, enabling researchers to assess goodness of fit to a theoretical distribution and to test for independence between two categorical variables.

!!! tip "Mental Model"
    The chi-square statistic sums up $(O - E)^2 / E$ across all categories -- each term measures how far an observed count deviates from what the null hypothesis predicted, scaled by the expected count. Large values mean the data do not match the expected pattern. The test works for both goodness-of-fit (one variable) and independence (two variables in a contingency table).

## Chi-Square Test Statistic

The chi-square test statistic measures the discrepancy between observed counts $O_i$ and expected counts $E_i$ across $k$ categories:

$$
\chi^2 = \sum_{i=1}^{k} \frac{(O_i - E_i)^2}{E_i}
$$

Under the null hypothesis, this statistic follows a chi-square distribution with degrees of freedom that depend on the specific test context. Large values of $\chi^2$ indicate that the observed data deviate substantially from the expected pattern.

!!! warning "Expected Count Requirement"
    The chi-square approximation is reliable when all expected counts satisfy $E_i \geq 5$. When this condition fails, consider combining categories or using Fisher's exact test for $2 \times 2$ tables.

## Goodness-of-Fit Test

The goodness-of-fit test checks whether a sample of categorical observations matches a hypothesized distribution. Given $k$ categories with observed counts $O_1, \ldots, O_k$ and expected counts $E_1, \ldots, E_k$ (where $\sum E_i = \sum O_i = n$), the hypotheses are

$$
H_0: p_i = p_{i,0} \text{ for all } i \quad \text{vs} \quad H_1: p_i \neq p_{i,0} \text{ for some } i
$$

where $p_{i,0}$ are the hypothesized proportions and $E_i = n \cdot p_{i,0}$.

The degrees of freedom are $k - 1$ (or $k - 1 - m$ if $m$ parameters were estimated from the data):

$$
\chi^2 \sim \chi^2_{k-1}
$$

### SciPy Implementation

The `scipy.stats.chisquare` function performs the one-sample chi-square goodness-of-fit test:

```python
from scipy import stats

# Observed counts from a die-rolling experiment
observed = [18, 22, 16, 21, 13, 10]

# Test against uniform distribution (equal expected frequencies)
chi2_stat, p_value = stats.chisquare(observed)
print(f"Chi-square statistic: {chi2_stat:.4f}")
print(f"p-value: {p_value:.4f}")

# Test against custom expected frequencies
expected = [16.67, 16.67, 16.67, 16.67, 16.67, 16.67]
chi2_stat, p_value = stats.chisquare(observed, f_exp=expected)
print(f"Chi-square statistic: {chi2_stat:.4f}")
print(f"p-value: {p_value:.4f}")
```

When `f_exp` is omitted, the function assumes a uniform distribution across all categories.

## Test of Independence

The test of independence determines whether two categorical variables are associated. Given an $r \times c$ contingency table with observed counts $O_{ij}$, the expected counts under independence are

$$
E_{ij} = \frac{R_i \cdot C_j}{n}
$$

where $R_i = \sum_{j} O_{ij}$ is the $i$-th row total, $C_j = \sum_{i} O_{ij}$ is the $j$-th column total, and $n$ is the grand total.

The hypotheses are

$$
H_0: p_{ij} = p_{i \cdot} \cdot p_{\cdot j} \text{ for all } i, j \quad \text{vs} \quad H_1: \text{variables are associated}
$$

The test statistic uses the same formula with degrees of freedom $(r - 1)(c - 1)$:

$$
\chi^2 \sim \chi^2_{(r-1)(c-1)}
$$

### SciPy Implementation

The `scipy.stats.chi2_contingency` function handles contingency table analysis:

```python
import numpy as np
from scipy import stats

# Contingency table: treatment outcome by group
#            Success  Failure
# Drug A       45       15
# Drug B       30       30
# Placebo      20       40
observed_table = np.array([[45, 15],
                           [30, 30],
                           [20, 40]])

chi2_stat, p_value, dof, expected = stats.chi2_contingency(observed_table)
print(f"Chi-square statistic: {chi2_stat:.4f}")
print(f"Degrees of freedom: {dof}")
print(f"p-value: {p_value:.6f}")
print(f"Expected frequencies:\n{expected}")
```

The function returns the test statistic, p-value, degrees of freedom, and the matrix of expected frequencies under $H_0$.

## Effect Size

The chi-square statistic depends on sample size, so a significant result does not necessarily indicate a strong association. Cramer's $V$ provides a normalized measure of effect size for contingency tables:

$$
V = \sqrt{\frac{\chi^2}{n \cdot (\min(r, c) - 1)}}
$$

where $V \in [0, 1]$, with $V = 0$ indicating no association and $V = 1$ indicating perfect association.

## Summary

Chi-square tests assess categorical data through goodness-of-fit (`scipy.stats.chisquare`) and independence testing (`scipy.stats.chi2_contingency`). Both tests compare observed and expected frequencies using the same $\chi^2$ statistic but differ in how expected counts and degrees of freedom are computed. The chi-square approximation requires sufficiently large expected counts, and effect sizes like Cramer's $V$ should supplement p-values for practical interpretation.

---

## Exercises

**Exercise 1.**
A die is rolled 120 times with outcomes: {1: 25, 2: 17, 3: 15, 4: 23, 5: 22, 6: 18}. Test whether the die is fair using a chi-square goodness-of-fit test at $\alpha = 0.05$.

??? success "Solution to Exercise 1"

        from scipy import stats

        observed = [25, 17, 15, 23, 22, 18]
        expected = [20, 20, 20, 20, 20, 20]
        chi2, p = stats.chisquare(observed, expected)
        print(f"Chi-square: {chi2:.4f}, p: {p:.4f}")
        print(f"Decision: {'Reject H0 (unfair)' if p < 0.05 else 'Fail to reject H0 (fair)'}")

---

**Exercise 2.**
A contingency table records preferences: Men: [45 coffee, 30 tea, 25 juice], Women: [35 coffee, 40 tea, 45 juice]. Test for independence between gender and beverage preference. Compute Cramer's V.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        table = np.array([[45, 30, 25], [35, 40, 45]])
        chi2, p, dof, expected = stats.chi2_contingency(table)
        n = table.sum()
        v = np.sqrt(chi2 / (n * (min(table.shape) - 1)))

        print(f"Chi-square: {chi2:.4f}, p: {p:.4f}, dof: {dof}")
        print(f"Cramer's V: {v:.4f}")

---

**Exercise 3.**
Generate a $3 \times 3$ contingency table under perfect independence (expected = observed). Verify that the chi-square statistic is 0 and the p-value is 1.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        table = np.array([[30, 30, 30], [30, 30, 30], [30, 30, 30]])
        chi2, p, dof, expected = stats.chi2_contingency(table)
        print(f"Chi-square: {chi2:.6f}, p: {p:.4f}")
