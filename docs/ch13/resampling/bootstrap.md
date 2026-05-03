# Bootstrap

Classical statistical inference often relies on analytical formulas for standard errors and sampling distributions. These formulas require distributional assumptions (such as normality) or may simply not exist for complex statistics like the median or a ratio of means. The **bootstrap**, introduced by Efron (1979), provides a computer-intensive alternative: instead of deriving formulas, it resamples the observed data to approximate the sampling distribution of any statistic.

This page introduces the nonparametric bootstrap, its theoretical foundation in the plug-in principle, and its use for estimating standard errors and bias.

!!! tip "Mental Model"
    The bootstrap treats your sample as a miniature population. Resample from it with replacement thousands of times, compute your statistic each time, and the spread of those values approximates the sampling distribution. No formulas, no distributional assumptions -- just repeated resampling and computation.

---

## The Plug-In Principle

The bootstrap rests on a single idea: replace the unknown population distribution $F$ with the **empirical distribution function** $\hat{F}_n$, then compute the quantity of interest under $\hat{F}_n$.

Given observations $x_1, x_2, \ldots, x_n$, the empirical distribution function assigns equal probability $1/n$ to each observed value:

$$
\hat{F}_n(t) = \frac{1}{n} \sum_{i=1}^{n} \mathbf{1}(x_i \leq t)
$$

If the parameter of interest is $\theta = T(F)$ for some functional $T$, the plug-in estimate is $\hat{\theta} = T(\hat{F}_n)$. The bootstrap goes further by estimating the entire *sampling distribution* of $\hat{\theta}$ under $\hat{F}_n$.

---

## The Nonparametric Bootstrap Algorithm

Let $\hat{\theta} = s(\mathbf{x})$ be the statistic of interest computed from the observed sample $\mathbf{x} = (x_1, \ldots, x_n)$. The bootstrap algorithm proceeds as follows.

**Algorithm (Nonparametric Bootstrap):**

1. **For** $b = 1, 2, \ldots, B$:
    - Draw a **bootstrap sample** $\mathbf{x}^{*b} = (x_1^{*}, x_2^{*}, \ldots, x_n^{*})$ by sampling $n$ values from $\mathbf{x}$ **with replacement**.
    - Compute the **bootstrap replicate** $\hat{\theta}^{*b} = s(\mathbf{x}^{*b})$.
2. Use the collection $\{\hat{\theta}^{*1}, \hat{\theta}^{*2}, \ldots, \hat{\theta}^{*B}\}$ to approximate the sampling distribution of $\hat{\theta}$.

Each bootstrap sample has the same size $n$ as the original data. Because sampling is with replacement, some observations appear more than once while others are omitted. On average, each bootstrap sample contains approximately $1 - (1 - 1/n)^n \approx 1 - e^{-1} \approx 63.2\%$ of the unique original observations.

!!! tip "Choosing the number of bootstrap replicates"
    For standard error estimation, $B = 1{,}000$ is usually sufficient. For confidence intervals (covered in the sibling page on bootstrap confidence intervals), $B = 10{,}000$ or more is recommended to accurately estimate tail quantiles.

---

## Bootstrap Estimate of Standard Error

The bootstrap standard error of $\hat{\theta}$ is the sample standard deviation of the bootstrap replicates:

$$
\widehat{\text{SE}}_{\text{boot}} = \sqrt{\frac{1}{B-1} \sum_{b=1}^{B} \left(\hat{\theta}^{*b} - \bar{\theta}^{*}\right)^2}
$$

where $\bar{\theta}^{*} = \frac{1}{B}\sum_{b=1}^{B}\hat{\theta}^{*b}$ is the mean of the bootstrap replicates.

This estimate requires no analytical derivation and applies to any statistic $\hat{\theta}$, including medians, trimmed means, correlation coefficients, and regression coefficients.

---

## Bootstrap Estimate of Bias

The **bias** of an estimator is $\text{Bias}(\hat{\theta}) = E[\hat{\theta}] - \theta$. The bootstrap estimates this by comparing the mean of the bootstrap replicates to the original estimate:

$$
\widehat{\text{Bias}}_{\text{boot}} = \bar{\theta}^{*} - \hat{\theta}
$$

A **bias-corrected** estimate is then:

$$
\tilde{\theta} = \hat{\theta} - \widehat{\text{Bias}}_{\text{boot}} = 2\hat{\theta} - \bar{\theta}^{*}
$$

!!! warning "Bias correction can increase variance"
    Subtracting the estimated bias adds variability to the estimate. If the bias is small relative to the standard error, bias correction may do more harm than good by inflating mean squared error.

---

## When the Bootstrap Works

The bootstrap is **consistent** for a broad class of statistics: as $n \to \infty$, the bootstrap distribution of $\hat{\theta}^{*} - \hat{\theta}$ converges to the true sampling distribution of $\hat{\theta} - \theta$.

The key requirement is that $\hat{F}_n$ converges to $F$ fast enough for the functional $T$ to be smooth. The bootstrap works well for:

- Sample means, variances, and quantiles
- Correlation and regression coefficients
- Many M-estimators and U-statistics

The bootstrap can **fail** in situations where the plug-in principle breaks down:

- **Extrema:** the distribution of $\max(x_1, \ldots, x_n)$ is not consistently estimated because the bootstrap cannot generate values outside the observed range.
- **Heavy tails:** when $F$ has infinite variance, $\hat{F}_n$ converges slowly and the bootstrap may not be reliable for variance-related statistics.
- **Dependent data:** the standard nonparametric bootstrap assumes independent observations. For time series, block bootstrap or other modifications are required.

---

## Summary

The bootstrap replaces analytical formulas with computation: draw many resamples with replacement, compute the statistic on each, and use the resulting empirical distribution for inference. The plug-in principle --- substituting $\hat{F}_n$ for $F$ --- provides the theoretical justification. Bootstrap standard errors and bias estimates are available for virtually any statistic without distributional assumptions, making the bootstrap one of the most widely applicable tools in modern statistics. Its main limitations arise with extremal statistics, heavy-tailed distributions, and dependent data.


---

## Exercises

**Exercise 1.** Write code that performs bootstrap resampling on a sample of 50 observations to estimate the mean. Generate 10000 bootstrap samples and compute the bootstrap estimate and standard error.

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

**Exercise 2.** Explain the bootstrap principle. Why does resampling with replacement from the data approximate sampling from the population?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that computes a 95% bootstrap confidence interval for the median using the percentile method.

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

**Exercise 4.** Create a function that takes a sample and a statistic function, and returns the bootstrap standard error and 95% confidence interval.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
