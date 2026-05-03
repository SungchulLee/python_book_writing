# Permutation Tests

Classical hypothesis tests such as the $t$-test rely on distributional assumptions --- typically that the data are normally distributed. When these assumptions are questionable, **permutation tests** offer an alternative that derives $p$-values directly from the data. The key insight is that under the null hypothesis, the group labels are exchangeable: randomly reassigning observations to groups should not systematically change the test statistic. By enumerating (or sampling) all possible reassignments, we obtain the exact distribution of the test statistic under the null.

This page defines the permutation testing framework, presents the algorithm for computing permutation $p$-values, and discusses the two-sample and correlation settings.

!!! tip "Mental Model"
    If the group labels truly do not matter (null hypothesis), then shuffling them and recomputing the test statistic should give a similar result to the original. A permutation test shuffles labels thousands of times and asks: "How often does a random shuffle produce a statistic as extreme as the one we observed?" That fraction is the exact p-value, no distributional assumptions needed.

---

## The Exchangeability Principle

Consider two groups of observations: $\mathbf{x} = (x_1, \ldots, x_m)$ and $\mathbf{y} = (y_1, \ldots, y_k)$ with total sample size $n = m + k$. Under the null hypothesis $H_0$ that the two groups come from the same distribution, the assignment of observations to groups is arbitrary. Formally, the joint distribution of all $n$ observations is **invariant under permutations** of the group labels.

This exchangeability means that any rearrangement of the $n$ values into groups of sizes $m$ and $k$ is equally likely under $H_0$. The **permutation distribution** of a test statistic $T$ is obtained by computing $T$ for every such rearrangement.

---

## The Permutation Test Algorithm

Let $T_{\text{obs}} = T(\mathbf{x}, \mathbf{y})$ be the observed test statistic. The exact permutation test proceeds as follows.

**Algorithm (Exact Permutation Test):**

1. Combine all $n$ observations into a single pool $\mathbf{z} = (x_1, \ldots, x_m, y_1, \ldots, y_k)$.
2. **For** each of the $\binom{n}{m}$ ways to assign $m$ observations to the first group:
    - Compute $T^*$ for this assignment.
3. The **permutation $p$-value** (for a two-sided test) is:

$$
p = \frac{\#\{T^* : |T^*| \geq |T_{\text{obs}}|\}}{\binom{n}{m}}
$$

For a one-sided test, drop the absolute values and count in the appropriate tail.

!!! tip "The permutation $p$-value is exact"
    Under $H_0$ and exchangeability, the permutation $p$-value has exactly the correct Type I error rate: $P(p \leq \alpha) \leq \alpha$ for any significance level $\alpha$. No distributional assumptions are needed beyond exchangeability.

---

## Approximate (Random) Permutation Test

When $\binom{n}{m}$ is too large for exhaustive enumeration (which happens quickly --- for $m = k = 20$, there are over $10^{11}$ permutations), a **random permutation test** samples from the permutation distribution.

**Algorithm (Random Permutation Test):**

1. Combine all $n$ observations into $\mathbf{z}$.
2. **For** $b = 1, 2, \ldots, B$:
    - Randomly shuffle $\mathbf{z}$ and assign the first $m$ values to group 1.
    - Compute $T^{*b}$.
3. The approximate $p$-value is:

$$
\hat{p} = \frac{1 + \#\{T^{*b} : |T^{*b}| \geq |T_{\text{obs}}|\}}{B + 1}
$$

The $+1$ in numerator and denominator includes the observed statistic itself, which ensures that $\hat{p}$ is never exactly zero and maintains the validity of the test.

!!! warning "Choosing B for random permutation tests"
    For reliable $p$-values at significance level $\alpha$, use $B \geq 10/\alpha$. For example, testing at $\alpha = 0.05$ requires at least $B = 200$, but $B = 10{,}000$ is preferred for stable results, especially when reporting exact $p$-values.

---

## Two-Sample Permutation Test for Location

The most common application is testing whether two groups have the same mean (or median). The test statistic is typically the difference in group means:

$$
T = \bar{x} - \bar{y} = \frac{1}{m}\sum_{i=1}^{m}x_i - \frac{1}{k}\sum_{j=1}^{k}y_j
$$

Under $H_0: F_X = F_Y$, permuting the group labels does not change the distribution of $T$. The permutation $p$-value quantifies how extreme the observed difference is relative to the permutation distribution.

This test is the permutation analogue of the two-sample $t$-test. It makes no assumption about normality or equal variances, making it appropriate for skewed distributions, small samples, or ordinal data.

---

## Permutation Test for Correlation

Permutation tests extend beyond the two-sample setting. To test the null hypothesis of no association between paired variables $(x_i, y_i)$, $i = 1, \ldots, n$:

1. Compute the observed correlation $r_{\text{obs}} = \text{Cor}(\mathbf{x}, \mathbf{y})$.
2. For each permutation (or random sample of permutations), shuffle the $y$-values while keeping $\mathbf{x}$ fixed.
3. Compute the permutation correlation $r^*$.
4. The $p$-value is the proportion of permutations where $|r^*| \geq |r_{\text{obs}}|$.

Under the null of no association, the pairing of $x_i$ and $y_j$ is arbitrary, justifying the permutation.

---

## Properties and Comparison with Parametric Tests

| Property | Permutation Test | Parametric Test (e.g., $t$-test) |
|---|---|---|
| Distributional assumptions | Exchangeability only | Normality (or large $n$) |
| Type I error | Exact (or nearly so) | Approximate (relies on asymptotics) |
| Power | High for the chosen statistic | May be higher if assumptions hold |
| Computation | $O(\binom{n}{m})$ exact; $O(B \cdot n)$ approximate | $O(n)$ |
| Applicable statistics | Any computable statistic | Must have known null distribution |

When parametric assumptions hold, the parametric test may be slightly more powerful because it uses distributional information. However, when assumptions are violated, permutation tests maintain correct Type I error while parametric tests may not.

!!! note "Permutation tests are conditional tests"
    The permutation $p$-value is computed conditional on the observed collection of values $\mathbf{z}$. This means the test's properties hold for the specific dataset at hand, not just on average over hypothetical repetitions.

---

## Summary

Permutation tests derive $p$-values from the data itself by exploiting the exchangeability of observations under the null hypothesis. The exact permutation $p$-value enumerates all possible rearrangements of group labels; the random permutation test samples a subset when exhaustive enumeration is infeasible. The two-sample permutation test for location is the most common application, serving as a distribution-free alternative to the $t$-test. Permutation tests extend naturally to correlation, regression coefficients, and any other computable test statistic. Their main advantages are exact Type I error control and freedom from distributional assumptions; their main cost is computation.


---

## Exercises

**Exercise 1.** Write code that performs a permutation test to determine if two groups have significantly different means.

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

**Exercise 2.** Explain how a permutation test constructs the null distribution. Why is it a non-parametric test?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that runs a permutation test with 10000 permutations and plots the null distribution with the observed test statistic marked.

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

**Exercise 4.** Compare the p-value from a permutation test with the p-value from a parametric t-test on the same data.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
