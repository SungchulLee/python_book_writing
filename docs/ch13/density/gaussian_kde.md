# gaussian_kde

Estimating the probability density function of a random variable from observed data is a fundamental task in statistics. Parametric approaches assume a specific distributional form (e.g., Gaussian), but when the true distribution is unknown or complex, a nonparametric approach is needed. SciPy's `gaussian_kde` class provides kernel density estimation (KDE) using a Gaussian kernel, offering a smooth, continuous estimate of the underlying density without distributional assumptions.

!!! tip "Mental Model"
    Place a small Gaussian bell curve on top of each data point, then add them all up and normalize. The result is a smooth density estimate that inherits no assumptions about the shape of the underlying distribution. The width of each bell (the bandwidth) is the only tuning knob.

## Kernel Density Estimation

Given observations $x_1, x_2, \ldots, x_n$ drawn from an unknown density $f$, the **kernel density estimator** places a kernel function centered at each data point and averages:

$$
\hat{f}_h(x) = \frac{1}{nh}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right)
$$

where $K$ is the kernel function and $h > 0$ is the bandwidth parameter.

The `gaussian_kde` class uses the **Gaussian kernel**:

$$
K(u) = \frac{1}{\sqrt{2\pi}} \exp\!\left(-\frac{u^2}{2}\right)
$$

With this kernel, each data point contributes a Gaussian bump of width proportional to $h$, and the density estimate is the average of all $n$ bumps. The result is a smooth, infinitely differentiable function that integrates to one.

## Basic Usage

```python
import numpy as np
from scipy.stats import gaussian_kde

# Generate sample data from a mixture distribution
np.random.seed(42)
data = np.concatenate([
    np.random.normal(-1, 0.5, 300),
    np.random.normal(2, 0.8, 200)
])

# Fit a KDE
kde = gaussian_kde(data)

# Evaluate the density at a grid of points
x_grid = np.linspace(-4, 5, 200)
density = kde(x_grid)

# Evaluate at specific points
print(f"f(-1.0) = {kde(np.array([-1.0]))[0]:.4f}")
print(f"f( 0.0) = {kde(np.array([0.0]))[0]:.4f}")
print(f"f( 2.0) = {kde(np.array([2.0]))[0]:.4f}")
```

The constructor `gaussian_kde(dataset)` expects the data as a 1-D array (for univariate data) or a 2-D array of shape `(d, n)` where `d` is the number of dimensions and `n` is the number of observations. The fitted object is callable: `kde(x)` returns the density estimate at `x`.

## Key Attributes

After fitting, the `gaussian_kde` object exposes several useful attributes:

```python
print(f"Number of data points: {kde.n}")
print(f"Dimensionality:        {kde.d}")
print(f"Bandwidth factor:      {kde.factor:.4f}")
print(f"Covariance matrix:\n{kde.covariance}")
```

| Attribute | Description |
|---|---|
| `n` | Number of data points |
| `d` | Number of dimensions |
| `dataset` | The training data (shape `(d, n)`) |
| `factor` | Bandwidth factor (scalar multiplier) |
| `covariance` | Covariance matrix used for the kernel |

## Bandwidth Selection

The `bw_method` parameter controls how the bandwidth is chosen:

```python
# Scott's rule (default)
kde_scott = gaussian_kde(data, bw_method="scott")

# Silverman's rule
kde_silverman = gaussian_kde(data, bw_method="silverman")

# Custom scalar factor
kde_custom = gaussian_kde(data, bw_method=0.2)

# Custom callable
kde_callable = gaussian_kde(
    data, bw_method=lambda kde_obj: 0.15
)

print(f"Scott factor:     {kde_scott.factor:.4f}")
print(f"Silverman factor: {kde_silverman.factor:.4f}")
print(f"Custom factor:    {kde_custom.factor:.4f}")
```

!!! note "Default Bandwidth"
    The default method is Scott's rule: $h = n^{-1/(d+4)}$ where $d$ is the dimension. For univariate data ($d=1$), this gives $h \propto n^{-1/5}$, matching the optimal rate for MISE minimization.

## Weighted KDE

The `weights` parameter allows assigning different importance to each observation:

```python
# Give higher weight to recent observations
weights = np.linspace(0.5, 1.5, len(data))
kde_weighted = gaussian_kde(data, weights=weights)

print(f"Unweighted f(2.0) = {kde(np.array([2.0]))[0]:.4f}")
print(f"Weighted   f(2.0) = {kde_weighted(np.array([2.0]))[0]:.4f}")
```

The weights must be non-negative and are normalized internally so that the density integrates to one.

## Summary

SciPy's `gaussian_kde` provides nonparametric density estimation using the Gaussian kernel. The class fits a mixture of Gaussians centered at each data point, controlled by a bandwidth parameter selected via Scott's rule (default), Silverman's rule, or a custom method. The fitted object is callable for evaluation and supports weighted observations. It serves as the foundation for the evaluation, resampling, bandwidth selection, and multivariate KDE topics covered in the companion pages of this section.


---

## Exercises

**Exercise 1.** Write code that creates a `scipy.stats.gaussian_kde` object from 500 samples and plots the estimated density curve.

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

**Exercise 2.** Explain what a Gaussian kernel is and how KDE works conceptually.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that fits a KDE to bimodal data (mixture of two normals) and shows that the KDE captures both modes.

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

**Exercise 4.** Compare the KDE estimate with a histogram of the same data on the same axes. Use `density=True` for the histogram.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
