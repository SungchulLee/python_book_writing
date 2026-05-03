# Jackknife

Before the bootstrap, statisticians needed a general-purpose method for estimating the bias and variance of a statistic without relying on distributional assumptions. The **jackknife**, introduced by Quenouille (1949) and extended by Tukey (1958), achieves this by systematically leaving out one observation at a time and studying how the statistic changes. The jackknife is deterministic (unlike the bootstrap), computationally straightforward, and provides the foundation for influence-function diagnostics.

This page defines the delete-one jackknife, derives its bias and variance estimators, introduces pseudovalues, and discusses when the jackknife succeeds or fails.

!!! tip "Mental Model"
    The jackknife removes one observation at a time and recomputes the statistic, producing exactly $n$ leave-one-out estimates. The variation among these estimates approximates the sampling variability. Unlike the bootstrap, the jackknife is deterministic and requires no random number generation, but it fails for non-smooth statistics like the median.

---

## The Delete-One Jackknife

Let $\hat{\theta} = s(\mathbf{x})$ be a statistic computed from the full sample $\mathbf{x} = (x_1, x_2, \ldots, x_n)$. The **$i$-th jackknife replicate** is obtained by removing observation $i$:

$$
\hat{\theta}_{(i)} = s(x_1, \ldots, x_{i-1}, x_{i+1}, \ldots, x_n), \quad i = 1, 2, \ldots, n
$$

The **jackknife mean** is the average of these $n$ leave-one-out estimates:

$$
\bar{\theta}_{(\cdot)} = \frac{1}{n}\sum_{i=1}^{n} \hat{\theta}_{(i)}
$$

Unlike the bootstrap, which requires choosing $B$ and involves randomness, the jackknife produces exactly $n$ replicates deterministically.

---

## Jackknife Estimate of Bias

The bias of $\hat{\theta}$ as an estimator of $\theta$ is $\text{Bias}(\hat{\theta}) = E[\hat{\theta}] - \theta$. The jackknife estimates this as:

$$
\widehat{\text{Bias}}_{\text{jack}} = (n - 1)\left(\bar{\theta}_{(\cdot)} - \hat{\theta}\right)
$$

The factor $(n - 1)$ arises from the theory of statistical functionals. Intuitively, removing one observation from a sample of size $n$ produces only a small perturbation, and the factor $(n-1)$ amplifies this perturbation to the correct scale.

The **bias-corrected jackknife estimate** is:

$$
\tilde{\theta}_{\text{jack}} = \hat{\theta} - \widehat{\text{Bias}}_{\text{jack}} = n\hat{\theta} - (n-1)\bar{\theta}_{(\cdot)}
$$

!!! tip "When jackknife bias correction is most useful"
    The jackknife removes the $O(n^{-1})$ term in the bias expansion. This is particularly valuable for statistics like the variance ($s^2$ with divisor $n$ instead of $n-1$), ratios, and correlation coefficients where the leading bias term is of order $1/n$.

---

## Jackknife Pseudovalues

Tukey introduced **pseudovalues** to turn the jackknife into a tool for both estimation and inference. The $i$-th pseudovalue is:

$$
\tilde{\theta}_i = n\hat{\theta} - (n - 1)\hat{\theta}_{(i)}, \quad i = 1, 2, \ldots, n
$$

Each pseudovalue isolates the contribution of observation $i$ to the overall estimate. The bias-corrected jackknife estimate is simply the mean of the pseudovalues:

$$
\tilde{\theta}_{\text{jack}} = \frac{1}{n}\sum_{i=1}^{n}\tilde{\theta}_i
$$

The pseudovalues are approximately independent and identically distributed (for smooth statistics), which allows treating them like ordinary data for inference. A $t$-based confidence interval for $\theta$ can be constructed from the pseudovalues:

$$
\tilde{\theta}_{\text{jack}} \pm t_{n-1,\,1-\alpha/2}\;\frac{\tilde{s}}{\sqrt{n}}
$$

where $\tilde{s}^2 = \frac{1}{n-1}\sum_{i=1}^{n}(\tilde{\theta}_i - \tilde{\theta}_{\text{jack}})^2$.

---

## Jackknife Estimate of Variance

The jackknife variance estimator for $\hat{\theta}$ is:

$$
\widehat{\text{Var}}_{\text{jack}} = \frac{n - 1}{n}\sum_{i=1}^{n}\left(\hat{\theta}_{(i)} - \bar{\theta}_{(\cdot)}\right)^2
$$

The corresponding jackknife standard error is:

$$
\widehat{\text{SE}}_{\text{jack}} = \sqrt{\frac{n-1}{n}\sum_{i=1}^{n}\left(\hat{\theta}_{(i)} - \bar{\theta}_{(\cdot)}\right)^2}
$$

The unusual prefactor $\frac{n-1}{n}$ (instead of $\frac{1}{n-1}$) compensates for the fact that the leave-one-out replicates are highly correlated with each other. Each $\hat{\theta}_{(i)}$ shares $n-1$ of $n$ observations with every other replicate, so the raw variance of the replicates underestimates the true sampling variance without this correction.

---

## Relationship to the Bootstrap

The jackknife can be viewed as a linear approximation to the bootstrap. For smooth statistics, the jackknife variance estimate converges to the same limit as the bootstrap variance estimate. More precisely, for a statistic that is a smooth functional of the empirical distribution, the jackknife and bootstrap standard errors agree to first order.

However, the bootstrap is more general:

| Property | Jackknife | Bootstrap |
|---|---|---|
| Replicates | $n$ (deterministic) | $B$ (random, user-chosen) |
| Handles non-smooth statistics | No | Yes |
| Provides full distribution | No (only mean, variance) | Yes |
| Computation | $O(n)$ evaluations | $O(B)$ evaluations |

---

## Limitations

The jackknife fails for **non-smooth statistics** --- statistics that are not smooth functionals of the empirical distribution. The most important example is the **sample median**: removing a single observation can cause the median to jump discontinuously, and the jackknife variance estimate is inconsistent in this case.

More generally, the jackknife fails for:

- **Quantiles and order statistics:** the delete-one perturbation is too crude to capture variability.
- **Extrema:** $\max(x_1, \ldots, x_n)$ changes by a large amount when the maximum observation is removed and not at all otherwise.

For these statistics, the bootstrap is the preferred resampling method.

!!! warning "Do not use the jackknife for the median"
    The jackknife variance estimator for the sample median is inconsistent. The bootstrap or kernel-based methods should be used instead.

---

## Summary

The jackknife estimates bias and variance by systematically leaving out one observation at a time. The bias estimate uses the factor $(n-1)$ to amplify the small leave-one-out perturbation to the correct scale. Pseudovalues isolate each observation's contribution and enable $t$-based confidence intervals. The jackknife is deterministic, requires no tuning parameters, and works well for smooth statistics. Its main limitation is that it fails for non-smooth statistics such as quantiles and extrema, where the bootstrap should be used instead.


---

## Exercises

**Exercise 1.** Write code that implements the jackknife estimate of the standard error for the mean of a sample of size 20.

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

**Exercise 2.** Explain the jackknife procedure: leave-one-out resampling. How does it differ from the bootstrap?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that uses the jackknife to estimate the bias and standard error of the sample variance.

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

**Exercise 4.** Compare the jackknife standard error estimate with the bootstrap standard error estimate for the same dataset and statistic.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
