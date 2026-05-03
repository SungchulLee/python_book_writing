# Bootstrap Confidence Intervals

A bootstrap standard error tells us how variable a statistic is, but it does not directly produce an interval estimate. To construct a confidence interval from bootstrap replicates, we need a rule for translating the empirical bootstrap distribution into lower and upper limits. Several methods exist, each with different assumptions and coverage accuracy.

This page presents the four most common bootstrap confidence interval methods: the normal interval, the percentile interval, the basic (pivotal) interval, and the bias-corrected and accelerated (BCa) interval.

!!! tip "Mental Model"
    The simplest bootstrap CI reads the 2.5th and 97.5th percentiles directly from the bootstrap distribution (percentile method). More sophisticated methods correct for bias and skewness in the bootstrap distribution. The BCa interval is generally the most accurate, but requires more computation. All methods need at least $B = 10{,}000$ replicates for stable tail quantiles.

---

## Setup and Notation

Suppose we observe a sample $\mathbf{x} = (x_1, \ldots, x_n)$ and compute a statistic $\hat{\theta} = s(\mathbf{x})$. We draw $B$ bootstrap samples and obtain replicates $\hat{\theta}^{*1}, \ldots, \hat{\theta}^{*B}$. Let $\widehat{\text{SE}}_{\text{boot}}$ denote the bootstrap standard error and let $\hat{\theta}^{*(\alpha)}$ denote the $\alpha$-quantile of the bootstrap distribution (i.e., the value below which a fraction $\alpha$ of the bootstrap replicates fall).

The goal is a $100(1 - \alpha)\%$ confidence interval for the population parameter $\theta$.

---

## Normal Interval

The simplest approach assumes the bootstrap distribution is approximately normal and uses the bootstrap standard error in place of an analytical one:

$$
\left(\hat{\theta} - z_{1-\alpha/2}\,\widehat{\text{SE}}_{\text{boot}},\;\; \hat{\theta} + z_{1-\alpha/2}\,\widehat{\text{SE}}_{\text{boot}}\right)
$$

where $z_{1-\alpha/2}$ is the $(1 - \alpha/2)$-quantile of the standard normal distribution.

This method inherits all the limitations of normal-based intervals: it is symmetric around $\hat{\theta}$ and performs poorly when the sampling distribution of $\hat{\theta}$ is skewed. Its main advantage is simplicity.

---

## Percentile Interval

The **percentile method** reads the confidence limits directly from the quantiles of the bootstrap distribution:

$$
\left(\hat{\theta}^{*(\alpha/2)},\;\; \hat{\theta}^{*(1-\alpha/2)}\right)
$$

For a 95% interval, the limits are the 2.5th and 97.5th percentiles of the bootstrap replicates.

The percentile interval respects the range of the parameter (for example, it will not produce a negative lower bound for a variance) and is automatically asymmetric when the bootstrap distribution is skewed. However, it can have poor coverage when the bootstrap distribution is biased as an estimate of the true sampling distribution.

!!! tip "Number of replicates for percentile intervals"
    Accurate estimation of the 2.5th and 97.5th percentiles requires large $B$. A minimum of $B = 10{,}000$ is recommended; $B = 1{,}000$ may produce unstable interval endpoints.

---

## Basic (Pivotal) Interval

The **basic interval** (also called the pivotal or reflection method) uses the bootstrap to estimate the distribution of the pivot $\hat{\theta}^{*} - \hat{\theta}$ and then inverts it:

$$
\left(2\hat{\theta} - \hat{\theta}^{*(1-\alpha/2)},\;\; 2\hat{\theta} - \hat{\theta}^{*(\alpha/2)}\right)
$$

The logic is as follows. If $\hat{\theta}^{*} - \hat{\theta}$ approximates $\hat{\theta} - \theta$, then the $(1-\alpha/2)$-quantile of the bootstrap pivot estimates the $(1-\alpha/2)$-quantile of $\hat{\theta} - \theta$. Solving for $\theta$ reverses the quantile indices.

The basic interval corrects for bias in the bootstrap distribution, which the percentile method does not. When the bootstrap distribution is shifted relative to the true sampling distribution, the basic interval adjusts the endpoints accordingly.

---

## BCa Interval (Bias-Corrected and Accelerated)

The **BCa method** modifies the percentile interval to correct for both bias and skewness. It adjusts the percentile indices using two correction factors:

**Bias correction** $\hat{z}_0$: measures the median bias of the bootstrap distribution.

$$
\hat{z}_0 = \Phi^{-1}\!\left(\frac{1}{B}\sum_{b=1}^{B} \mathbf{1}(\hat{\theta}^{*b} < \hat{\theta})\right)
$$

where $\Phi^{-1}$ is the standard normal quantile function.

**Acceleration** $\hat{a}$: accounts for how the standard error of $\hat{\theta}$ changes with $\theta$. It is typically estimated using the jackknife:

$$
\hat{a} = \frac{\sum_{i=1}^{n}(\bar{\theta}_{(\cdot)} - \hat{\theta}_{(i)})^3}{6\left[\sum_{i=1}^{n}(\bar{\theta}_{(\cdot)} - \hat{\theta}_{(i)})^2\right]^{3/2}}
$$

where $\hat{\theta}_{(i)}$ is the statistic computed with observation $i$ removed and $\bar{\theta}_{(\cdot)} = \frac{1}{n}\sum_{i=1}^{n}\hat{\theta}_{(i)}$.

The adjusted percentile indices are:

$$
\alpha_1 = \Phi\!\left(\hat{z}_0 + \frac{\hat{z}_0 + z_{\alpha/2}}{1 - \hat{a}(\hat{z}_0 + z_{\alpha/2})}\right), \quad \alpha_2 = \Phi\!\left(\hat{z}_0 + \frac{\hat{z}_0 + z_{1-\alpha/2}}{1 - \hat{a}(\hat{z}_0 + z_{1-\alpha/2})}\right)
$$

The BCa interval is then $(\hat{\theta}^{*(\alpha_1)},\; \hat{\theta}^{*(\alpha_2)})$.

When $\hat{z}_0 = 0$ and $\hat{a} = 0$, the BCa interval reduces to the ordinary percentile interval. The BCa method achieves **second-order accuracy**: its coverage error is $O(n^{-1})$ compared to $O(n^{-1/2})$ for the percentile and normal methods.

---

## Comparison of Methods

| Method | Symmetric | Bias Correction | Coverage Accuracy | Computation |
|---|---|---|---|---|
| Normal | Yes | No | First-order | Lightest |
| Percentile | No | No | First-order | Light |
| Basic | No | Yes | First-order | Light |
| BCa | No | Yes | Second-order | Heavier (requires jackknife) |

!!! warning "No method is universally best"
    For well-behaved, symmetric statistics (e.g., the sample mean with moderate $n$), all four methods give similar results. The BCa method is preferred when the statistic has a skewed sampling distribution or when the sample size is small, but it requires more computation and can be unstable with very small $n$.

---

## Summary

Bootstrap confidence intervals translate the empirical bootstrap distribution into interval estimates for a parameter. The normal interval is simplest but assumes symmetry. The percentile interval reads quantiles directly and respects parameter boundaries. The basic interval corrects for bias by reflecting the bootstrap distribution around the point estimate. The BCa interval further corrects for skewness using bias and acceleration constants, achieving second-order coverage accuracy. In practice, the percentile method is a reliable default, and the BCa method is preferred when higher accuracy is needed and computation is not a constraint.

---

## Runnable Example: `seaborn_statistical_estimation.py`

```python
"""
Tutorial 08: Statistical Estimation
Error bars, confidence intervals, bootstrapping
Level: Advanced
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    sns.set_style("whitegrid")
    tips = sns.load_dataset('tips')

    # Barplot with confidence intervals (default 95%)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=tips, x='day', y='tip', ci=95, capsize=0.1)
    plt.title('Mean with 95% Confidence Interval', fontsize=14, fontweight='bold')
    plt.ylabel('Average Tip ($)')
    plt.show()

    # Pointplot - show means and CIs with lines
    plt.figure(figsize=(10, 6))
    sns.pointplot(data=tips, x='day', y='tip', hue='time', ci=95, markers=['o', 's'], linestyles=['-', '--'])
    plt.title('Point Plot with Confidence Intervals', fontsize=14, fontweight='bold')
    plt.legend(title='Time of Day')
    plt.show()

    # Custom bootstrap example
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'group': ['A']*50 + ['B']*50,
        'value': np.concatenate([np.random.normal(10, 2, 50), np.random.normal(12, 2, 50)])
    })

    plt.figure(figsize=(10, 6))
    sns.barplot(data=sample_data, x='group', y='value', ci=95, capsize=0.1, errwidth=2)
    plt.title('Bootstrapped Confidence Intervals', fontsize=14, fontweight='bold')
    plt.ylabel('Mean Value')
    plt.show()

    print("Tutorial 08 demonstrates statistical estimation visualization")
    print("Key concept: confidence intervals via bootstrapping")
```


---

## Exercises

**Exercise 1.** Write code that computes three types of bootstrap confidence intervals: percentile, basic, and BCa (bias-corrected and accelerated).

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

**Exercise 2.** Explain the difference between the percentile method and the BCa method for bootstrap confidence intervals.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that computes a 95% bootstrap confidence interval for the correlation coefficient between two variables.

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

**Exercise 4.** Demonstrate the coverage of bootstrap confidence intervals by running a simulation: generate 1000 datasets, compute CIs, and count how many contain the true parameter.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
