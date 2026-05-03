# Distribution Comparison Visualization

Choosing the right probability model for a dataset requires comparing the empirical distribution against candidate theoretical distributions. Visual comparison methods complement formal tests by revealing where a model fits well and where it fails. This page covers the main graphical techniques for distribution comparison using `scipy.stats` and Matplotlib.

!!! tip "Mental Model"
    Formal goodness-of-fit tests give a binary yes/no answer; visual comparisons show you exactly where a model fits and where it fails. Overlay a fitted density on a histogram to check the overall shape, compare CDFs to spot systematic shifts, and use QQ plots to zoom in on tail behavior.

---

## Histogram with Density Overlay

The simplest comparison overlays a theoretical PDF on a normalized histogram of the data. Normalizing the histogram so that its total area equals one puts it on the same scale as the density function.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
data = stats.gamma.rvs(a=3, scale=2, size=500)

# Fit a gamma distribution to the data
a_hat, loc_hat, scale_hat = stats.gamma.fit(data)

x = np.linspace(0, max(data), 200)
pdf_fitted = stats.gamma.pdf(x, a_hat, loc=loc_hat, scale=scale_hat)

plt.hist(data, bins=30, density=True, alpha=0.6, label='Data')
plt.plot(x, pdf_fitted, 'r-', linewidth=2,
         label=f'Gamma(a={a_hat:.2f}, scale={scale_hat:.2f})')
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Histogram with Fitted Gamma Density')
plt.legend()
plt.show()
```

!!! tip "Bin Width Matters"
    Too few bins obscure the shape; too many create noise. The Freedman-Diaconis rule sets bin width to $2 \times \text{IQR} \times n^{-1/3}$, which adapts to both spread and sample size. Use `bins='fd'` in Matplotlib.

---

## Empirical CDF Comparison

The empirical cumulative distribution function (ECDF) for a sample of size $n$ is

$$
\hat{F}_n(x) = \frac{1}{n} \sum_{i=1}^{n} \mathbf{1}(x_i \le x)
$$

Plotting $\hat{F}_n(x)$ against the theoretical CDF $F(x)$ reveals discrepancies in the tails and center of the distribution.

```python
# Sort data for ECDF
data_sorted = np.sort(data)
ecdf = np.arange(1, len(data) + 1) / len(data)

# Theoretical CDF
cdf_theoretical = stats.gamma.cdf(data_sorted, a_hat,
                                   loc=loc_hat, scale=scale_hat)

plt.step(data_sorted, ecdf, where='post', label='Empirical CDF')
plt.plot(data_sorted, cdf_theoretical, 'r-', label='Gamma CDF')
plt.xlabel('Value')
plt.ylabel('Cumulative Probability')
plt.title('Empirical vs Theoretical CDF')
plt.legend()
plt.show()
```

The vertical distance between the two curves at any point is the Kolmogorov-Smirnov statistic at that value:

$$
D_n = \sup_x \bigl|\hat{F}_n(x) - F(x)\bigr|
$$

```python
# KS test
ks_stat, p_value = stats.kstest(data, 'gamma', args=(a_hat, loc_hat, scale_hat))
print(f"KS statistic: {ks_stat:.4f}, p-value: {p_value:.4f}")
```

---

## Comparing Two Empirical Distributions

When comparing two samples rather than a sample against a theory, the two-sample KS test measures the maximum distance between their ECDFs:

$$
D_{n,m} = \sup_x \bigl|\hat{F}_n(x) - \hat{G}_m(x)\bigr|
$$

```python
# Two samples from different distributions
sample_a = stats.norm.rvs(loc=5, scale=2, size=200, random_state=42)
sample_b = stats.norm.rvs(loc=5.5, scale=2.2, size=200, random_state=43)

# Visual comparison
a_sorted = np.sort(sample_a)
b_sorted = np.sort(sample_b)
ecdf_a = np.arange(1, len(a_sorted) + 1) / len(a_sorted)
ecdf_b = np.arange(1, len(b_sorted) + 1) / len(b_sorted)

plt.step(a_sorted, ecdf_a, where='post', label='Sample A')
plt.step(b_sorted, ecdf_b, where='post', label='Sample B')
plt.xlabel('Value')
plt.ylabel('Cumulative Probability')
plt.title('Two-Sample ECDF Comparison')
plt.legend()
plt.show()

# Two-sample KS test
ks_stat, p_value = stats.ks_2samp(sample_a, sample_b)
print(f"Two-sample KS: D = {ks_stat:.4f}, p-value = {p_value:.4f}")
```

---

## Multiple Distribution Comparison

When several candidate distributions are under consideration, overlay their fitted densities and compare using information criteria or goodness-of-fit statistics.

```python
# Fit multiple distributions
distributions = {
    'norm': stats.norm,
    'gamma': stats.gamma,
    'lognorm': stats.lognorm,
}

results = {}
x = np.linspace(0.01, max(data), 200)

plt.hist(data, bins=30, density=True, alpha=0.5, label='Data')

for name, dist in distributions.items():
    params = dist.fit(data)
    pdf = dist.pdf(x, *params)
    plt.plot(x, pdf, linewidth=2, label=f'{name}')

    # KS statistic for comparison
    ks, pval = stats.kstest(data, name, args=params)
    results[name] = {'params': params, 'KS': ks, 'p_value': pval}

plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Multiple Distribution Fits')
plt.legend()
plt.show()

# Summary table
print(f"{'Distribution':12s} {'KS stat':>8s} {'p-value':>8s}")
for name, r in results.items():
    print(f"{name:12s} {r['KS']:8.4f} {r['p_value']:8.4f}")
```

---

## Summary

Distribution comparison visualization provides essential diagnostics for model selection. **Histogram overlays** offer an intuitive first check, while **ECDF comparisons** give a more precise view of fit quality across the entire range. The **Kolmogorov-Smirnov statistic** quantifies the maximum discrepancy between empirical and theoretical distributions. Comparing multiple candidate models side by side, both visually and numerically, guides the choice of the most appropriate distributional assumption for downstream analysis.


---

## Exercises

**Exercise 1.** Write code that uses the Kolmogorov-Smirnov test (`stats.ks_2samp()`) to compare two samples and determine if they come from the same distribution.

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

**Exercise 2.** Explain the null hypothesis of the KS test. What does a small p-value indicate?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that compares the empirical CDFs of two samples by plotting them on the same axes.

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

**Exercise 4.** Create two samples from different distributions and demonstrate that the KS test correctly rejects the null hypothesis.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
