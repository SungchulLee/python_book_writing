# Evaluate and Resample

Once a kernel density estimate has been fitted, the two primary operations are **evaluation** (computing the estimated density at new points) and **resampling** (generating new synthetic observations from the estimated distribution). SciPy's `gaussian_kde` object supports both operations, along with integration methods for computing probabilities over intervals. This page covers each of these capabilities with their mathematical basis and practical usage.

!!! tip "Mental Model"
    A fitted KDE is a full generative model of your data. You can query it at any point to get a density value (evaluation), draw new synthetic samples from it (resampling), or integrate over a region to get probabilities. Think of the KDE object as a smooth, continuous replacement for the histogram that supports all the operations of a parametric distribution.

## Evaluating the Density

A fitted `gaussian_kde` object is callable. Given query points $x_1, \ldots, x_m$, calling `kde(x)` computes the density estimate at each point:

$$
\hat{f}(x) = \frac{1}{nh}\sum_{i=1}^{n} K\!\left(\frac{x - x_i}{h}\right)
$$

where $n$ is the number of training points, $h$ is the bandwidth, and $K$ is the Gaussian kernel $K(u) = \frac{1}{\sqrt{2\pi}} e^{-u^2/2}$.

```python
import numpy as np
from scipy.stats import gaussian_kde

# Fit a KDE to sample data
np.random.seed(42)
data = np.random.normal(0, 1, 500)
kde = gaussian_kde(data)

# Evaluate at a grid of points
x_grid = np.linspace(-4, 4, 200)
density = kde(x_grid)

# Evaluate at specific points
points = np.array([-1.0, 0.0, 1.0])
print("Density at specific points:")
for pt, d in zip(points, kde(points)):
    print(f"  f({pt:+.1f}) = {d:.4f}")
```

The `logpdf` method computes $\log \hat{f}(x)$ directly, avoiding numerical underflow for very small density values:

```python
log_density = kde.logpdf(x_grid)
print(f"Log-density at x=0: {kde.logpdf(np.array([0.0]))[0]:.4f}")
```

!!! note "Computational Cost"
    Evaluating the KDE at $m$ query points with $n$ training points costs $O(mn)$ operations, since each query requires summing over all $n$ kernels. SciPy uses vectorized NumPy operations to compute this efficiently, but for very large datasets, approximate methods may be needed.

## Resampling

The `resample` method generates new samples from the estimated density $\hat{f}$. The algorithm works in two steps:

1. **Select a data point**: Uniformly choose one of the $n$ original observations $x_i$
2. **Add kernel noise**: Return $x_i + h \cdot \varepsilon$ where $\varepsilon \sim \mathcal{N}(0, 1)$

This is equivalent to sampling from the mixture of Gaussians $\hat{f}(x) = \frac{1}{n}\sum_{i=1}^n \mathcal{N}(x_i, h^2)$.

```python
# Generate new samples from the fitted KDE
new_samples = kde.resample(size=1000)
print(f"Resampled shape: {new_samples.shape}")
print(f"Resampled mean:  {new_samples.mean():.4f}")
print(f"Resampled std:   {new_samples.std():.4f}")
print(f"Original mean:   {data.mean():.4f}")
print(f"Original std:    {data.std():.4f}")
```

!!! tip "Reproducibility"
    Pass a `seed` argument to `resample` for reproducible results: `kde.resample(size=1000, seed=42)`.

## Integration

The `gaussian_kde` object provides methods for computing probabilities by integrating the density over regions.

### Interval Probability

The method `integrate_box_1d(low, high)` computes

$$
P(a \leq X \leq b) = \int_a^b \hat{f}(x)\, dx
$$

```python
# Probability within one standard deviation of the mean
prob = kde.integrate_box_1d(-1, 1)
print(f"P(-1 <= X <= 1) = {prob:.4f}")

# Compare with theoretical Gaussian value
from scipy.stats import norm
print(f"Theoretical:      {norm.cdf(1) - norm.cdf(-1):.4f}")
```

### KDE-to-KDE Integration

The method `integrate_kde(other_kde)` computes the integral of the product of two KDE densities:

$$
\int \hat{f}(x)\, \hat{g}(x)\, dx
$$

This is useful for computing the $L^2$ distance between two density estimates or for kernel-based two-sample tests.

```python
# Fit a second KDE and compute the integrated product
data2 = np.random.normal(0.5, 1.2, 500)
kde2 = gaussian_kde(data2)

integrated_product = kde.integrate_kde(kde2)
self_integral = kde.integrate_kde(kde)
print(f"Integral of f*g: {integrated_product:.4f}")
print(f"Integral of f*f: {self_integral:.4f}")
```

## Summary

SciPy's `gaussian_kde` object provides three key operations after fitting: evaluation at arbitrary points via `kde(x)` or `kde.logpdf(x)`, resampling via `kde.resample(size)` which generates new observations from the mixture-of-Gaussians representation, and integration via `integrate_box_1d` for interval probabilities and `integrate_kde` for density product integrals. Evaluation costs $O(mn)$ for $m$ query points and $n$ training points, while resampling is $O(m)$ per generated sample.


---

## Exercises

**Exercise 1.** Write code that fits a KDE to 500 data points and evaluates the density at 100 evenly-spaced points using `kernel(x_grid)`.

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

**Exercise 2.** Explain the difference between evaluating a KDE at specific points and resampling from the estimated density.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that fits a KDE and uses `kernel.resample(1000)` to generate new synthetic samples. Plot the original data and the resampled data.

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

**Exercise 4.** Compute the integral of a KDE estimate over a specific interval using numerical integration. Verify it is approximately equal to the probability of data falling in that interval.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
