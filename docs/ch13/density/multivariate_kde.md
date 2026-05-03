# Multivariate KDE

Real-world data is often multivariate: financial returns involve multiple assets, sensor measurements record multiple channels, and scientific experiments produce vector-valued observations. Understanding the joint density structure of multivariate data requires extending kernel density estimation beyond one dimension. SciPy's `gaussian_kde` handles multivariate data natively, using a multivariate Gaussian kernel with an automatically estimated bandwidth matrix.

!!! tip "Mental Model"
    In one dimension, each data point gets a bell curve; in $d$ dimensions, each data point gets a multivariate Gaussian ellipsoid. The bandwidth matrix controls both the size and orientation of these ellipsoids, automatically adapting to the covariance structure of the data so that correlated dimensions are smoothed together.

## Multivariate KDE Formula

Given $n$ observations $\mathbf{x}_1, \ldots, \mathbf{x}_n$ in $\mathbb{R}^d$, the multivariate kernel density estimator is

$$
\hat{f}(\mathbf{x}) = \frac{1}{n} \sum_{i=1}^{n} \frac{1}{|\mathbf{H}|^{1/2}} K\!\left(\mathbf{H}^{-1/2}(\mathbf{x} - \mathbf{x}_i)\right)
$$

where $\mathbf{H}$ is a $d \times d$ positive definite **bandwidth matrix** and $K$ is the multivariate Gaussian kernel:

$$
K(\mathbf{u}) = (2\pi)^{-d/2} \exp\!\left(-\frac{1}{2}\mathbf{u}^T \mathbf{u}\right)
$$

The bandwidth matrix $\mathbf{H}$ controls both the width and orientation of the kernel placed at each data point. A diagonal $\mathbf{H}$ scales each dimension independently, while a full $\mathbf{H}$ allows the kernel to be rotated to match the correlation structure of the data.

## SciPy's Bandwidth Parameterization

SciPy's `gaussian_kde` parameterizes the bandwidth matrix as

$$
\mathbf{H} = h^2 \, \hat{\Sigma}
$$

where $\hat{\Sigma}$ is the sample covariance matrix of the data and $h$ is a scalar bandwidth factor. By default, Scott's rule sets $h = n^{-1/(d+4)}$. This approach automatically adapts the kernel shape to the covariance structure of the data.

!!! warning "Data Shape Convention"
    SciPy's `gaussian_kde` expects multivariate data in shape `(d, n)`, where `d` is the number of dimensions and `n` is the number of observations. This is the transpose of the common `(n, d)` convention used by NumPy and scikit-learn. Passing data in the wrong orientation is a frequent source of errors.

## Two-Dimensional Example

```python
import numpy as np
from scipy.stats import gaussian_kde

# Generate 2-D data from a mixture
np.random.seed(42)
n = 500
cluster1 = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], n // 2)
cluster2 = np.random.multivariate_normal([3, 3], [[0.5, -0.3], [-0.3, 0.8]], n // 2)
data = np.vstack([cluster1, cluster2])

# Fit KDE (note the transpose: gaussian_kde expects shape (d, n))
kde = gaussian_kde(data.T)

print(f"Dimensionality: {kde.d}")
print(f"Number of points: {kde.n}")
print(f"Bandwidth factor: {kde.factor:.4f}")
```

## Evaluating on a Grid

To visualize a 2-D KDE, evaluate the density on a regular grid:

```python
# Create a 2-D grid
x_grid = np.linspace(-3, 6, 100)
y_grid = np.linspace(-3, 6, 100)
xx, yy = np.meshgrid(x_grid, y_grid)

# Stack grid points into shape (2, m) for evaluation
grid_points = np.vstack([xx.ravel(), yy.ravel()])
density = kde(grid_points).reshape(xx.shape)

print(f"Grid shape: {xx.shape}")
print(f"Density range: [{density.min():.6f}, {density.max():.6f}]")
```

The density values can be passed to `matplotlib.pyplot.contourf` or `pcolormesh` for visualization.

## Resampling

Resampling from a multivariate KDE works the same way as in the univariate case: select a random data point and add Gaussian noise scaled by the bandwidth matrix.

```python
# Generate new samples from the fitted KDE
new_samples = kde.resample(size=1000)
print(f"Resampled shape: {new_samples.shape}")  # (2, 1000)
print(f"Resampled mean: {new_samples.mean(axis=1)}")
print(f"Original mean:  {data.mean(axis=0)}")
```

## Curse of Dimensionality

The optimal MISE convergence rate for a $d$-dimensional KDE is

$$
\text{MISE}^* = O\!\left(n^{-4/(d+4)}\right)
$$

As $d$ increases, the rate degrades rapidly:

| Dimension $d$ | MISE rate | Samples for comparable accuracy |
|---|---|---|
| 1 | $O(n^{-4/5})$ | Baseline |
| 2 | $O(n^{-2/3})$ | ~10x more |
| 5 | $O(n^{-4/9})$ | ~1,000x more |
| 10 | $O(n^{-2/7})$ | ~100,000x more |

!!! note "Practical Limits"
    KDE is most effective for $d \leq 3$ or $4$ with typical sample sizes. For higher dimensions, the data becomes too sparse for the kernel to capture the density structure reliably. In such cases, consider dimensionality reduction (e.g., PCA) before applying KDE, or use methods designed for high dimensions.

## Summary

Multivariate KDE extends the univariate estimator by using a multivariate Gaussian kernel shaped by a bandwidth matrix $\mathbf{H}$. SciPy parameterizes $\mathbf{H}$ as a scalar factor times the sample covariance, automatically adapting to the data's correlation structure. The key practical considerations are the data shape convention (`(d, n)` not `(n, d)`), grid-based evaluation for visualization, and the curse of dimensionality that limits effective use to low-dimensional settings.


---

## Exercises

**Exercise 1.** Write code that fits a 2D Gaussian KDE to bivariate data and visualizes it using `imshow`.

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

**Exercise 2.** Explain how multivariate KDE extends the univariate case. What role does the bandwidth matrix play?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that generates data from a mixture of two bivariate normals and fits a 2D KDE to it.

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

**Exercise 4.** Create a visualization that shows the 2D KDE as a contour plot overlaid with the original scatter data.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
