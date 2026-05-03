# One-Sided vs Two-Sided Tests

The choice between a one-sided and two-sided test determines how the rejection region is allocated and directly affects the p-value. A two-sided test checks whether the parameter differs from the null value in either direction, while a one-sided test concentrates all rejection probability in one tail. This choice must be made before looking at the data, based on the research question.

!!! tip "Mental Model"
    A two-sided test guards against surprises in either direction (the parameter could be higher or lower); a one-sided test bets everything on one direction and gains statistical power in exchange. The rule is simple: choose one-sided only when the opposite direction is scientifically meaningless, and always decide before looking at the data.

---

## Two-Sided Tests

A two-sided (two-tailed) test uses the hypotheses

$$
H_0: \mu = \mu_0 \quad \text{vs} \quad H_1: \mu \neq \mu_0
$$

The rejection region splits $\alpha$ equally between both tails. For a $t$-test, reject $H_0$ when

$$
|t| > t_{\alpha/2,\, n-1}
$$

The two-sided p-value is

$$
p = 2 \cdot P(T \ge |t_{\text{obs}}|)
$$

where $T$ follows the $t$-distribution with $n - 1$ degrees of freedom under $H_0$.

```python
import numpy as np
from scipy import stats

np.random.seed(42)
data = np.random.normal(loc=52, scale=10, size=30)

# Two-sided test: H0: mu = 50 vs H1: mu != 50
t_stat, p_two = stats.ttest_1samp(data, 50)
print(f"t = {t_stat:.3f}")
print(f"Two-sided p-value: {p_two:.4f}")
```

---

## One-Sided Tests

### Right-Tailed (Greater Than)

A right-tailed test checks whether the parameter exceeds the null value:

$$
H_0: \mu \le \mu_0 \quad \text{vs} \quad H_1: \mu > \mu_0
$$

The rejection region places all $\alpha$ in the right tail. Reject $H_0$ when

$$
t > t_{\alpha,\, n-1}
$$

The one-sided p-value is

$$
p = P(T \ge t_{\text{obs}})
$$

```python
# Right-tailed: H0: mu <= 50 vs H1: mu > 50
t_stat, p_two = stats.ttest_1samp(data, 50)

# Convert two-sided to one-sided (right tail)
if t_stat > 0:
    p_right = p_two / 2
else:
    p_right = 1 - p_two / 2

print(f"t = {t_stat:.3f}")
print(f"Right-tailed p-value: {p_right:.4f}")
```

### Left-Tailed (Less Than)

A left-tailed test checks whether the parameter is below the null value:

$$
H_0: \mu \ge \mu_0 \quad \text{vs} \quad H_1: \mu < \mu_0
$$

Reject $H_0$ when $t < -t_{\alpha,\, n-1}$. The one-sided p-value is

$$
p = P(T \le t_{\text{obs}})
$$

```python
# Left-tailed: H0: mu >= 50 vs H1: mu < 50
if t_stat < 0:
    p_left = p_two / 2
else:
    p_left = 1 - p_two / 2

print(f"Left-tailed p-value: {p_left:.4f}")
```

!!! tip "Using the alternative Parameter"
    Several scipy.stats test functions accept an `alternative` parameter directly, avoiding manual p-value conversion:

    ```python
    # scipy >= 1.7 supports alternative for many tests
    result = stats.ttest_1samp(data, 50, alternative='greater')
    print(f"Right-tailed p-value: {result.pvalue:.4f}")

    result = stats.ttest_1samp(data, 50, alternative='less')
    print(f"Left-tailed p-value: {result.pvalue:.4f}")
    ```

---

## Comparing Rejection Regions

The key difference lies in how the significance level $\alpha$ is distributed:

| Test Type | Rejection Region | Critical Value |
|---|---|---|
| Two-sided | Both tails, $\alpha/2$ each | $\pm t_{\alpha/2,\, n-1}$ |
| Right-tailed | Right tail only, $\alpha$ | $t_{\alpha,\, n-1}$ |
| Left-tailed | Left tail only, $\alpha$ | $-t_{\alpha,\, n-1}$ |

Because a one-sided test places all $\alpha$ in one tail, its critical value is less extreme than the two-sided critical value. This makes one-sided tests more powerful for detecting effects in the specified direction.

```python
alpha = 0.05
df = len(data) - 1

t_crit_two = stats.t.ppf(1 - alpha / 2, df)
t_crit_one = stats.t.ppf(1 - alpha, df)

print(f"Two-sided critical value: ±{t_crit_two:.3f}")
print(f"One-sided critical value: {t_crit_one:.3f}")
print(f"One-sided threshold is lower by: {t_crit_two - t_crit_one:.3f}")
```

---

## Power Implications

A one-sided test has greater power than a two-sided test for detecting effects in the specified direction, because the one-sided critical value is less extreme. However, it has zero power for detecting effects in the opposite direction.

```python
from statsmodels.stats.power import tt_solve_power

# Power comparison for same effect size
effect_size = 0.5
n = 30

# Two-sided power
power_two = tt_solve_power(effect_size=effect_size, nobs=n,
                           alpha=0.05, alternative='two-sided')
# One-sided power (correct direction)
power_one = tt_solve_power(effect_size=effect_size, nobs=n,
                           alpha=0.05, alternative='larger')

print(f"Two-sided power: {power_two:.3f}")
print(f"One-sided power: {power_one:.3f}")
print(f"Power gain: {power_one - power_two:.3f}")
```

---

## When to Use Each

!!! warning "Pre-Registration Requirement"
    The choice between one-sided and two-sided must be made before examining the data. Choosing a one-sided test after seeing the data direction is a form of p-hacking that inflates the false positive rate.

**Use a two-sided test when:**

- You do not have a strong directional prediction before data collection
- Effects in either direction would be scientifically interesting
- You are conducting exploratory research

**Use a one-sided test when:**

- Prior theory or evidence strongly predicts the direction of the effect
- Only one direction is practically meaningful (e.g., a drug cannot make patients worse)
- You need maximum power to detect an effect in a specific direction

```python
# Example: testing whether a new drug increases blood pressure
# Strong prior: the drug class is known to raise BP
np.random.seed(42)
bp_change = np.random.normal(loc=3, scale=8, size=25)  # Mean increase of 3

# One-sided is appropriate here (prior expectation of increase)
result = stats.ttest_1samp(bp_change, 0, alternative='greater')
print(f"One-sided test (increase): p = {result.pvalue:.4f}")

# Two-sided for comparison
result_two = stats.ttest_1samp(bp_change, 0)
print(f"Two-sided test: p = {result_two.pvalue:.4f}")
```

---

## Summary

Two-sided tests distribute the rejection probability equally in both tails and are appropriate when effects in either direction are of interest. One-sided tests concentrate all rejection probability in one tail, providing greater power for detecting effects in the pre-specified direction at the cost of being unable to detect effects in the opposite direction. The one-sided p-value is exactly half the two-sided p-value when the observed effect is in the hypothesized direction. The choice must always be justified by the research question and made before analyzing the data.

---

## Exercises

**Exercise 1.**
Generate 25 samples from $N(52, 10^2)$ and test $H_0: \mu = 50$ using both a two-sided test and a right-tailed test via the `alternative` parameter of `ttest_1samp`. Compare the p-values and explain the relationship.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = np.random.normal(52, 10, 25)
        result_two = stats.ttest_1samp(data, 50)
        result_right = stats.ttest_1samp(data, 50, alternative='greater')
        print(f"Two-sided p-value:   {result_two.pvalue:.4f}")
        print(f"Right-tailed p-value:{result_right.pvalue:.4f}")
        print("Right-tailed p = two-sided p / 2 (when t > 0)")

---

**Exercise 2.**
Compute the critical values for a two-sided and a one-sided (right-tailed) $t$-test at $\alpha = 0.05$ with 20 degrees of freedom. Show that the one-sided critical value is less extreme.

??? success "Solution to Exercise 2"

        from scipy import stats

        df = 20
        t_two = stats.t.ppf(1 - 0.05/2, df)
        t_one = stats.t.ppf(1 - 0.05, df)
        print(f"Two-sided critical value:  +/- {t_two:.4f}")
        print(f"One-sided critical value:  {t_one:.4f}")
        print(f"Difference: {t_two - t_one:.4f}")

---

**Exercise 3.**
Using `statsmodels.stats.power.tt_solve_power`, compute the power of a one-sample t-test with $n = 20$ and effect size $d = 0.5$ for both one-sided (`'larger'`) and two-sided alternatives. Confirm that the one-sided test is more powerful.

??? success "Solution to Exercise 3"

        from statsmodels.stats.power import tt_solve_power

        power_two = tt_solve_power(effect_size=0.5, nobs=20, alpha=0.05,
                                    alternative='two-sided')
        power_one = tt_solve_power(effect_size=0.5, nobs=20, alpha=0.05,
                                    alternative='larger')
        print(f"Two-sided power: {power_two:.4f}")
        print(f"One-sided power: {power_one:.4f}")
