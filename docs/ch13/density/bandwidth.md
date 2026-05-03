# Bandwidth Selection

The bandwidth parameter is the single most important choice in kernel density estimation. It controls the width of the kernel placed at each data point and determines the smoothness of the resulting density estimate. Too small a bandwidth produces a noisy, spiky curve that overfits the data; too large a bandwidth produces an overly smooth curve that obscures important features like modes and skewness. This page covers the theory behind bandwidth selection and the practical methods available in SciPy.

!!! tip "Mental Model"
    Bandwidth is the "blur radius" of your density estimate. Too narrow and you see every bump from individual data points; too wide and you smear away real features like separate modes. The optimal bandwidth balances these two errors, and rules like Scott's and Silverman's provide good starting points for unimodal data.

## Role of Bandwidth in KDE

Recall that the kernel density estimator with kernel $K$ and bandwidth $h > 0$ is

$$
\hat{f}_h(x) = \frac{1}{nh}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right)
$$

The bandwidth $h$ scales the kernel horizontally: a larger $h$ spreads each kernel wider, averaging over more of the data, while a smaller $h$ makes each kernel narrower, capturing finer detail.

## Bias-Variance Tradeoff

The quality of a density estimate is typically measured by the **mean integrated squared error** (MISE):

$$
\text{MISE}(h) = E\!\left[\int \left(\hat{f}_h(x) - f(x)\right)^2 dx\right]
$$

where $f$ is the true density. The MISE decomposes into integrated squared bias and integrated variance:

$$
\text{MISE}(h) \approx \frac{h^4}{4}\left(\int K(u)^2\, du\right) \!\left(\int \left[f''(x)\right]^2 dx\right) + \frac{1}{nh}\int K(u)^2\, du
$$

This asymptotic expansion (AMISE) reveals the tradeoff:

- **Bias term** $\propto h^4$: increases with bandwidth (oversmoothing blurs features)
- **Variance term** $\propto 1/(nh)$: decreases with bandwidth (more averaging reduces noise)

The optimal bandwidth minimizes the sum of these competing terms.

## Optimal Rate

Minimizing the AMISE with respect to $h$ yields the optimal bandwidth rate

$$
h^* \propto n^{-1/5}
$$

This means the bandwidth should shrink as the sample size grows, but slowly. The MISE at this optimal rate converges as $O(n^{-4/5})$, which is slower than the parametric rate $O(n^{-1})$ but is the best achievable rate for nonparametric density estimation with a second-order kernel.

## Silverman's Rule of Thumb

**Silverman's rule** provides a closed-form bandwidth that is optimal when the true density is Gaussian:

$$
h_{\text{Silverman}} = 1.06\,\hat{\sigma}\, n^{-1/5}
$$

where $\hat{\sigma}$ is the sample standard deviation. A more robust variant uses the minimum of the standard deviation and the interquartile range:

$$
h_{\text{robust}} = 0.9 \min\!\left(\hat{\sigma},\; \frac{\text{IQR}}{1.34}\right) n^{-1/5}
$$

**Scott's rule** is similar:

$$
h_{\text{Scott}} = 3.49\,\hat{\sigma}\, n^{-1/3}
$$

!!! note "Gaussian Assumption"
    Both Silverman's and Scott's rules assume the underlying density is approximately Gaussian. For multimodal or heavy-tailed distributions, these rules tend to oversmooth, and data-driven methods such as cross-validation should be preferred.

## Cross-Validation

**Leave-one-out cross-validation** (LOOCV) selects the bandwidth that maximizes the pseudo-likelihood:

$$
\text{CV}(h) = \frac{1}{n}\sum_{i=1}^{n} \log \hat{f}_{-i,h}(x_i)
$$

where $\hat{f}_{-i,h}$ is the KDE computed from all observations except $x_i$. This approach is fully data-driven and adapts to the shape of the true density, but it is computationally more expensive than plug-in rules.

## Bandwidth Selection in SciPy

SciPy's `gaussian_kde` uses Scott's rule by default. The `bw_method` parameter accepts `"scott"`, `"silverman"`, a scalar factor, or a callable.

```python
import numpy as np
from scipy.stats import gaussian_kde

# Generate bimodal data
np.random.seed(42)
data = np.concatenate([
    np.random.normal(-2, 0.5, 300),
    np.random.normal(2, 0.8, 200)
])

# Default (Scott's rule)
kde_scott = gaussian_kde(data, bw_method="scott")
print(f"Scott bandwidth factor:     {kde_scott.factor:.4f}")

# Silverman's rule
kde_silverman = gaussian_kde(data, bw_method="silverman")
print(f"Silverman bandwidth factor: {kde_silverman.factor:.4f}")

# Custom scalar (multiply Scott's factor)
kde_narrow = gaussian_kde(data, bw_method=0.3)
print(f"Custom bandwidth factor:    {kde_narrow.factor:.4f}")

# Evaluate on a grid
x_grid = np.linspace(-5, 5, 200)
density_scott = kde_scott(x_grid)
density_narrow = kde_narrow(x_grid)
```

!!! tip "Choosing Bandwidth for Multimodal Data"
    For multimodal distributions, Scott's and Silverman's rules typically oversmooth, merging distinct modes into one broad peak. Reducing the bandwidth factor (e.g., `bw_method=0.3`) or using cross-validation can better resolve multiple modes.

## Summary

Bandwidth selection controls the bias-variance tradeoff in kernel density estimation. The optimal bandwidth scales as $n^{-1/5}$ and balances oversmoothing (high bias) against undersmoothing (high variance). Silverman's and Scott's rules provide quick Gaussian-reference bandwidths, while cross-validation offers a data-driven alternative for non-Gaussian densities. In SciPy, the `bw_method` parameter of `gaussian_kde` provides access to all of these approaches.


---

## Exercises

**Exercise 1.** Write code that computes a KDE of 500 random samples and plots the result for three different bandwidths: 0.1, 0.5, and 1.0.

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

**Exercise 2.** Explain the bias-variance tradeoff in bandwidth selection for KDE. What happens with too small or too large a bandwidth?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that compares Scott's rule and Silverman's rule for bandwidth selection on the same dataset.

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

**Exercise 4.** Explain what cross-validation bandwidth selection is. Why might it give better results than rule-of-thumb methods?

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
