# Multiple Testing Correction

When a single hypothesis test is conducted at significance level $\alpha = 0.05$, there is a 5% chance of a false positive. But when many tests are performed simultaneously — comparing multiple groups, scanning many features, or testing at multiple time points — the probability of at least one false positive grows rapidly. Multiple testing corrections control this inflation by adjusting either the significance threshold or the p-values themselves.

!!! tip "Mental Model"
    Running 20 tests at the 5% level is like rolling a 20-sided die and hoping for no 1s -- you will get a false positive about 64% of the time. Bonferroni divides the significance level by the number of tests (strict but safe); Benjamini-Hochberg controls the false discovery rate (more power, slightly more false positives).

---

## The Multiple Comparisons Problem

If $m$ independent tests are each conducted at level $\alpha$, the probability of at least one false positive (assuming all null hypotheses are true) is

$$
P(\text{at least one false positive}) = 1 - (1 - \alpha)^m
$$

For $m = 20$ tests at $\alpha = 0.05$, this probability is $1 - 0.95^{20} \approx 0.64$ — nearly two-thirds of the time, at least one test will be falsely significant.

```python
import numpy as np
from scipy import stats

# Demonstrate inflated false positive rate
np.random.seed(42)
n_tests = 20
alpha = 0.05

# All null hypotheses are true (both groups from same distribution)
p_values = []
for _ in range(n_tests):
    x = np.random.normal(0, 1, 30)
    y = np.random.normal(0, 1, 30)
    _, p = stats.ttest_ind(x, y)
    p_values.append(p)

n_significant = sum(p < alpha for p in p_values)
print(f"Tests: {n_tests}, Significant (uncorrected): {n_significant}")
print(f"Theoretical P(at least 1 FP): {1 - (1 - alpha)**n_tests:.3f}")
```

---

## Family-Wise Error Rate

The **family-wise error rate** (FWER) is the probability of making at least one Type I error among all tests:

$$
\text{FWER} = P\left(\bigcup_{i=1}^{m} \{\text{reject } H_{0i} \mid H_{0i} \text{ true}\}\right)
$$

FWER control ensures this probability stays at or below $\alpha$.

---

## Bonferroni Correction

The simplest FWER-controlling method divides the significance level equally among all tests. Reject $H_{0i}$ if

$$
p_i \le \frac{\alpha}{m}
$$

Equivalently, multiply each p-value by $m$ and compare to $\alpha$:

$$
p_i^{\text{adj}} = \min(m \cdot p_i,\; 1)
$$

The Bonferroni correction is valid for any dependence structure among the tests but is conservative — it becomes increasingly strict as $m$ grows.

```python
from statsmodels.stats.multitest import multipletests

p_values_arr = np.array(p_values)

# Bonferroni correction
reject_bonf, pvals_bonf, _, _ = multipletests(p_values_arr, alpha=0.05,
                                               method='bonferroni')
print(f"Bonferroni rejections: {sum(reject_bonf)}")
print(f"Adjusted p-values (first 5): {pvals_bonf[:5].round(4)}")
```

---

## Holm-Bonferroni Method

The Holm (step-down) method is uniformly more powerful than Bonferroni while still controlling FWER. The procedure is:

1. Sort the $m$ p-values in ascending order: $p_{(1)} \le p_{(2)} \le \cdots \le p_{(m)}$
2. For $k = 1, 2, \ldots, m$, reject $H_{0(k)}$ if $p_{(k)} \le \frac{\alpha}{m - k + 1}$
3. Stop at the first $k$ where the condition fails; do not reject that hypothesis or any with larger p-values

```python
# Holm correction
reject_holm, pvals_holm, _, _ = multipletests(p_values_arr, alpha=0.05,
                                               method='holm')
print(f"Holm rejections: {sum(reject_holm)}")
```

!!! tip "Holm vs Bonferroni"
    The Holm method always rejects at least as many hypotheses as Bonferroni and often more. There is no reason to prefer Bonferroni over Holm when FWER control is desired.

---

## Sidak Correction

The Sidak correction uses the exact probability for independent tests rather than the Bonferroni upper bound. Reject $H_{0i}$ if

$$
p_i \le 1 - (1 - \alpha)^{1/m}
$$

For small $\alpha$ and moderate $m$, this threshold is slightly more permissive than Bonferroni's $\alpha / m$.

```python
# Sidak correction
reject_sidak, pvals_sidak, _, _ = multipletests(p_values_arr, alpha=0.05,
                                                  method='sidak')
print(f"Sidak rejections: {sum(reject_sidak)}")
print(f"Sidak threshold: {1 - (1 - 0.05)**(1/n_tests):.6f}")
print(f"Bonferroni threshold: {0.05 / n_tests:.6f}")
```

---

## False Discovery Rate

The **false discovery rate** (FDR) is the expected proportion of rejected hypotheses that are false positives:

$$
\text{FDR} = E\left[\frac{V}{R \vee 1}\right]
$$

where $V$ is the number of false rejections and $R$ is the total number of rejections (with $R \vee 1 = \max(R, 1)$ to avoid division by zero). FDR control is less conservative than FWER and is preferred when many tests are conducted and some false positives are acceptable.

---

## Benjamini-Hochberg Procedure

The Benjamini-Hochberg (BH) procedure controls FDR at level $\alpha$:

1. Sort the $m$ p-values in ascending order: $p_{(1)} \le p_{(2)} \le \cdots \le p_{(m)}$
2. Find the largest $k$ such that $p_{(k)} \le \frac{k}{m} \alpha$
3. Reject all $H_{0(i)}$ for $i = 1, 2, \ldots, k$

The adjusted p-values (q-values) are

$$
q_{(i)} = \min\left(\frac{m}{i} \cdot p_{(i)},\; 1\right)
$$

enforced to be monotonically non-decreasing.

```python
# Benjamini-Hochberg (FDR)
reject_bh, pvals_bh, _, _ = multipletests(p_values_arr, alpha=0.05,
                                           method='fdr_bh')
print(f"BH rejections: {sum(reject_bh)}")
print(f"BH adjusted p-values (first 5): {pvals_bh[:5].round(4)}")
```

---

## Comparison of Methods

```python
# Compare all methods side by side
np.random.seed(42)

# 50 tests: 40 true nulls, 10 with real effects
m = 50
p_vals = []
true_null = []
for i in range(m):
    x = np.random.normal(0, 1, 30)
    if i < 10:
        y = np.random.normal(0.8, 1, 30)  # Real effect
        true_null.append(False)
    else:
        y = np.random.normal(0, 1, 30)    # No effect
        true_null.append(True)
    _, p = stats.ttest_ind(x, y)
    p_vals.append(p)

p_vals = np.array(p_vals)
true_null = np.array(true_null)

methods = ['bonferroni', 'holm', 'sidak', 'fdr_bh']
for method in methods:
    reject, _, _, _ = multipletests(p_vals, alpha=0.05, method=method)
    tp = sum(reject & ~true_null)  # True positives
    fp = sum(reject & true_null)   # False positives
    print(f"{method:12s}: rejected={sum(reject):2d}, TP={tp}, FP={fp}")
```

---

## Summary

Multiple testing corrections prevent the inflation of false positive rates when many hypotheses are tested simultaneously. FWER-controlling methods (Bonferroni, Holm, Sidak) ensure the probability of any false positive stays below $\alpha$, while FDR-controlling methods (Benjamini-Hochberg) allow a controlled proportion of false positives among rejections. The Holm method dominates Bonferroni for FWER control, and the BH procedure is the standard choice for FDR control in high-dimensional settings.

---

## Exercises

**Exercise 1.**
Generate 20 p-values from t-tests where all null hypotheses are true ($H_0$ is true for all). Apply the Bonferroni correction using `multipletests` and verify that no tests are rejected.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats
        from statsmodels.stats.multitest import multipletests

        np.random.seed(42)
        p_values = []
        for _ in range(20):
            x = np.random.normal(0, 1, 30)
            y = np.random.normal(0, 1, 30)
            _, p = stats.ttest_ind(x, y)
            p_values.append(p)

        reject, pvals_adj, _, _ = multipletests(p_values, alpha=0.05, method='bonferroni')
        print(f"Rejections (Bonferroni): {sum(reject)}")

---

**Exercise 2.**
Create 50 p-values: 10 from tests with real effects ($N(0, 1)$ vs $N(1, 1)$) and 40 from null tests. Apply both Bonferroni and Benjamini-Hochberg corrections. Compare the number of true positives and false positives for each.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats
        from statsmodels.stats.multitest import multipletests

        np.random.seed(42)
        p_vals, true_null = [], []
        for i in range(50):
            x = np.random.normal(0, 1, 30)
            if i < 10:
                y = np.random.normal(1, 1, 30)
                true_null.append(False)
            else:
                y = np.random.normal(0, 1, 30)
                true_null.append(True)
            _, p = stats.ttest_ind(x, y)
            p_vals.append(p)

        p_vals = np.array(p_vals)
        true_null = np.array(true_null)

        for method in ['bonferroni', 'fdr_bh']:
            reject, _, _, _ = multipletests(p_vals, alpha=0.05, method=method)
            tp = sum(reject & ~true_null)
            fp = sum(reject & true_null)
            print(f"{method:12s}: TP={tp}, FP={fp}, Total rejected={sum(reject)}")

---

**Exercise 3.**
For the same 50 p-values from Exercise 2, apply the Holm correction. Compare its rejections with Bonferroni and verify that Holm rejects at least as many hypotheses as Bonferroni.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats
        from statsmodels.stats.multitest import multipletests

        np.random.seed(42)
        p_vals, true_null = [], []
        for i in range(50):
            x = np.random.normal(0, 1, 30)
            y = np.random.normal(1 if i < 10 else 0, 1, 30)
            true_null.append(i >= 10)
            _, p = stats.ttest_ind(x, y)
            p_vals.append(p)

        p_vals = np.array(p_vals)
        for method in ['bonferroni', 'holm']:
            reject, _, _, _ = multipletests(p_vals, alpha=0.05, method=method)
            print(f"{method:12s}: rejections={sum(reject)}")
        print("Holm always rejects >= Bonferroni")
