# Kernel Density Estimation with imshow

Kernel Density Estimation (KDE) provides a smooth estimate of the probability density function from sample data. This document covers how to visualize 2D KDE using `imshow`.

!!! tip "Mental Model"
    KDE turns scattered data points into a smooth density surface by placing a bell curve (kernel) at each point and summing them up. The result is like a soft-focus photograph of your scatter plot -- dense clusters glow brightly while sparse regions fade. Visualize the 2D density with `imshow` to reveal the underlying probability landscape.

    In the [density estimation spectrum](hist2d.md), KDE is the **continuous**
    end: where `hist2d` and `hexbin` produce piecewise-constant approximations,
    KDE produces a smooth function that can be evaluated at any point and
    integrated analytically. The cost is computation — KDE scales with the number
    of data points, while binning methods scale with the number of bins.

## What is KDE?

KDE estimates the probability density function by placing a kernel (typically Gaussian) at each data point and summing them:

$$\hat{f}(x) = \frac{1}{nh} \sum_{i=1}^{n} K\left(\frac{x - x_i}{h}\right)$$

where:
- $K$ is the kernel function
- $h$ is the bandwidth (smoothing parameter)
- $n$ is the number of data points

## Setup

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

np.random.seed(42)
```

---

## Basic 2D KDE

### 1. Generate Sample Data

```python
# Generate bivariate data
n = 500
mean = [0, 0]
cov = [[1, 0.5], [0.5, 1]]
data = np.random.multivariate_normal(mean, cov, n)

x = data[:, 0]
y = data[:, 1]

fig, ax = plt.subplots()
ax.scatter(x, y, alpha=0.5, s=10)
ax.set_title('Raw Data Points')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()
```

### 2. Compute KDE

```python
# Create grid
xmin, xmax = x.min() - 1, x.max() + 1
ymin, ymax = y.min() - 1, y.max() + 1
xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([xx.ravel(), yy.ravel()])

# Compute KDE
kernel = stats.gaussian_kde(np.vstack([x, y]))
density = kernel(positions).reshape(xx.shape)
```

### 3. Visualize with imshow

```python
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='viridis',
    aspect='auto'
)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('2D Kernel Density Estimation')
plt.colorbar(im, ax=ax, label='Density')
plt.show()
```

---

## KDE with Data Points Overlay

### 1. Basic Overlay

```python
fig, ax = plt.subplots(figsize=(8, 6))

# KDE background
im = ax.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='Blues',
    aspect='auto'
)

# Scatter points
ax.scatter(x, y, c='red', s=5, alpha=0.3)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('KDE with Data Points')
plt.colorbar(im, ax=ax, label='Density')
plt.show()
```

### 2. Transparent KDE

```python
fig, ax = plt.subplots(figsize=(8, 6))

ax.scatter(x, y, c='black', s=10, alpha=0.5, label='Data')
im = ax.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='Reds',
    aspect='auto',
    alpha=0.6
)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Transparent KDE Overlay')
plt.colorbar(im, ax=ax, label='Density')
plt.show()
```

---

## Bandwidth Selection

The bandwidth parameter controls smoothing. Larger values = smoother estimates.

### 1. Bandwidth Comparison

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

bandwidths = [0.1, 0.3, 0.8]

for ax, bw in zip(axes, bandwidths):
    kernel = stats.gaussian_kde(np.vstack([x, y]), bw_method=bw)
    density = kernel(positions).reshape(xx.shape)
    
    im = ax.imshow(
        density.T,
        extent=[xmin, xmax, ymin, ymax],
        origin='lower',
        cmap='viridis',
        aspect='auto'
    )
    ax.set_title(f'Bandwidth = {bw}')
    plt.colorbar(im, ax=ax)

plt.suptitle('Effect of Bandwidth on KDE', fontsize=14)
plt.tight_layout()
plt.show()
```

### 2. Scott's Rule vs Silverman's Rule

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

methods = ['scott', 'silverman', 0.3]
titles = ["Scott's Rule", "Silverman's Rule", "Manual (0.3)"]

for ax, method, title in zip(axes, methods, titles):
    kernel = stats.gaussian_kde(np.vstack([x, y]), bw_method=method)
    density = kernel(positions).reshape(xx.shape)
    
    im = ax.imshow(
        density.T,
        extent=[xmin, xmax, ymin, ymax],
        origin='lower',
        cmap='viridis',
        aspect='auto'
    )
    ax.set_title(title)
    plt.colorbar(im, ax=ax)

plt.tight_layout()
plt.show()
```

---

## Different Distributions

### 1. Clustered Data

```python
# Generate clustered data
np.random.seed(42)
n1 = 300
n2 = 200

cluster1 = np.random.multivariate_normal([2, 2], [[0.5, 0], [0, 0.5]], n1)
cluster2 = np.random.multivariate_normal([-1, -1], [[0.3, 0.2], [0.2, 0.3]], n2)
data_clustered = np.vstack([cluster1, cluster2])

x_c = data_clustered[:, 0]
y_c = data_clustered[:, 1]

# Compute KDE
xmin, xmax = x_c.min() - 1, x_c.max() + 1
ymin, ymax = y_c.min() - 1, y_c.max() + 1
xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([xx.ravel(), yy.ravel()])

kernel = stats.gaussian_kde(np.vstack([x_c, y_c]))
density = kernel(positions).reshape(xx.shape)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Scatter
axes[0].scatter(x_c, y_c, alpha=0.5, s=10)
axes[0].set_title('Scatter Plot')

# KDE
im = axes[1].imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='hot',
    aspect='auto'
)
axes[1].set_title('KDE')
plt.colorbar(im, ax=axes[1])

plt.suptitle('Clustered Data', fontsize=14)
plt.tight_layout()
plt.show()
```

### 2. Ring Distribution

```python
# Generate ring-shaped data
n = 1000
theta = np.random.uniform(0, 2 * np.pi, n)
r = np.random.normal(2, 0.2, n)
x_ring = r * np.cos(theta)
y_ring = r * np.sin(theta)

# Compute KDE
xmin, xmax = -4, 4
ymin, ymax = -4, 4
xx, yy = np.mgrid[xmin:xmax:150j, ymin:ymax:150j]
positions = np.vstack([xx.ravel(), yy.ravel()])

kernel = stats.gaussian_kde(np.vstack([x_ring, y_ring]), bw_method=0.15)
density = kernel(positions).reshape(xx.shape)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(x_ring, y_ring, alpha=0.3, s=5)
axes[0].set_aspect('equal')
axes[0].set_title('Scatter Plot')

im = axes[1].imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='magma',
    aspect='equal'
)
axes[1].set_title('KDE')
plt.colorbar(im, ax=axes[1])

plt.suptitle('Ring Distribution', fontsize=14)
plt.tight_layout()
plt.show()
```

---

## Comparison Methods

### KDE vs hist2d vs hexbin

```python
np.random.seed(42)
n = 2000
x = np.random.normal(0, 1, n)
y = x + np.random.normal(0, 0.5, n)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# hist2d
h = axes[0].hist2d(x, y, bins=30, cmap='viridis')
axes[0].set_title('hist2d')
plt.colorbar(h[3], ax=axes[0])

# hexbin
hb = axes[1].hexbin(x, y, gridsize=20, cmap='viridis')
axes[1].set_title('hexbin')
plt.colorbar(hb, ax=axes[1])

# KDE
xmin, xmax = x.min() - 1, x.max() + 1
ymin, ymax = y.min() - 1, y.max() + 1
xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([xx.ravel(), yy.ravel()])
kernel = stats.gaussian_kde(np.vstack([x, y]))
density = kernel(positions).reshape(xx.shape)

im = axes[2].imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='viridis',
    aspect='auto'
)
axes[2].set_title('KDE (imshow)')
plt.colorbar(im, ax=axes[2])

plt.suptitle('Density Visualization Methods', fontsize=14)
plt.tight_layout()
plt.show()
```

### Method Comparison Table

| Method | Pros | Cons |
|--------|------|------|
| `hist2d` | Fast, simple | Bin edge artifacts |
| `hexbin` | Better packing, no axis alignment | Less familiar |
| `KDE` | Smooth, accurate | Computationally expensive |

---

## Combining KDE with Contours

### 1. KDE with Contour Lines

```python
fig, ax = plt.subplots(figsize=(8, 6))

im = ax.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='Blues',
    aspect='auto'
)

# Add contour lines
cs = ax.contour(
    xx, yy, density,
    levels=5,
    colors='darkblue',
    linewidths=0.8
)
ax.clabel(cs, inline=True, fontsize=8, fmt='%.3f')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('KDE with Contour Lines')
plt.colorbar(im, ax=ax, label='Density')
plt.show()
```

### 2. KDE with Percentile Contours

```python
# Calculate percentile levels
levels_pct = np.percentile(density.ravel(), [10, 25, 50, 75, 90])

fig, ax = plt.subplots(figsize=(8, 6))

im = ax.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='YlOrRd',
    aspect='auto'
)

cs = ax.contour(xx, yy, density, levels=levels_pct, colors='black', linewidths=0.8)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('KDE with Percentile Contours')
plt.colorbar(im, ax=ax, label='Density')
plt.show()
```

---

## Marginal Distributions

### KDE with Marginal Histograms

```python
from mpl_toolkits.axes_grid1 import make_axes_locatable

np.random.seed(42)
n = 500
data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], n)
x, y = data[:, 0], data[:, 1]

# Compute KDE
xmin, xmax = x.min() - 0.5, x.max() + 0.5
ymin, ymax = y.min() - 0.5, y.max() + 0.5
xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
positions = np.vstack([xx.ravel(), yy.ravel()])
kernel = stats.gaussian_kde(np.vstack([x, y]))
density = kernel(positions).reshape(xx.shape)

# Create figure with marginals
fig, ax_main = plt.subplots(figsize=(8, 8))

divider = make_axes_locatable(ax_main)
ax_top = divider.append_axes("top", 1.2, pad=0.1, sharex=ax_main)
ax_right = divider.append_axes("right", 1.2, pad=0.1, sharey=ax_main)

# Main KDE plot
im = ax_main.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='Blues',
    aspect='auto'
)
ax_main.set_xlabel('x')
ax_main.set_ylabel('y')

# Top marginal
ax_top.hist(x, bins=30, density=True, alpha=0.7, color='steelblue')
x_kde = np.linspace(xmin, xmax, 200)
ax_top.plot(x_kde, stats.gaussian_kde(x)(x_kde), 'darkblue', linewidth=2)
ax_top.set_ylabel('Density')
plt.setp(ax_top.get_xticklabels(), visible=False)

# Right marginal
ax_right.hist(y, bins=30, density=True, alpha=0.7, color='steelblue', orientation='horizontal')
y_kde = np.linspace(ymin, ymax, 200)
ax_right.plot(stats.gaussian_kde(y)(y_kde), y_kde, 'darkblue', linewidth=2)
ax_right.set_xlabel('Density')
plt.setp(ax_right.get_yticklabels(), visible=False)

plt.suptitle('2D KDE with Marginal Distributions', fontsize=14, y=1.02)
plt.show()
```

---

## Colorbar Customization

### 1. Discrete Colorbar

```python
fig, ax = plt.subplots(figsize=(8, 6))

levels = np.linspace(density.min(), density.max(), 10)
im = ax.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='viridis',
    aspect='auto'
)

cbar = plt.colorbar(im, ax=ax, ticks=levels[::2])
cbar.set_label('Density')

ax.set_title('KDE with Custom Colorbar')
plt.show()
```

### 2. Logarithmic Scale

```python
from matplotlib.colors import LogNorm

# Ensure positive values
density_pos = np.maximum(density, 1e-10)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Linear scale
im1 = axes[0].imshow(
    density_pos.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='viridis',
    aspect='auto'
)
axes[0].set_title('Linear Scale')
plt.colorbar(im1, ax=axes[0])

# Log scale
im2 = axes[1].imshow(
    density_pos.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='viridis',
    aspect='auto',
    norm=LogNorm()
)
axes[1].set_title('Logarithmic Scale')
plt.colorbar(im2, ax=axes[1])

plt.tight_layout()
plt.show()
```

---

## Full Example: Publication Quality

```python
np.random.seed(42)

# Generate data with correlation
n = 1000
rho = 0.7
mean = [0, 0]
cov = [[1, rho], [rho, 1]]
data = np.random.multivariate_normal(mean, cov, n)
x, y = data[:, 0], data[:, 1]

# Compute KDE
xmin, xmax = -4, 4
ymin, ymax = -4, 4
xx, yy = np.mgrid[xmin:xmax:150j, ymin:ymax:150j]
positions = np.vstack([xx.ravel(), yy.ravel()])
kernel = stats.gaussian_kde(np.vstack([x, y]))
density = kernel(positions).reshape(xx.shape)

# Create figure
fig, ax = plt.subplots(figsize=(9, 7))

# KDE heatmap
im = ax.imshow(
    density.T,
    extent=[xmin, xmax, ymin, ymax],
    origin='lower',
    cmap='Blues',
    aspect='equal'
)

# Contour lines
levels = np.percentile(density.ravel(), [20, 40, 60, 80, 95])
cs = ax.contour(xx, yy, density, levels=levels, colors='navy', linewidths=0.8, alpha=0.7)

# Scatter subset
idx = np.random.choice(n, 100, replace=False)
ax.scatter(x[idx], y[idx], c='darkred', s=10, alpha=0.5, zorder=5)

# Labels and title
ax.set_xlabel('$X$', fontsize=12)
ax.set_ylabel('$Y$', fontsize=12)
ax.set_title(f'Bivariate Normal Distribution ($\\rho = {rho}$)', fontsize=14, fontweight='bold')

# Colorbar
cbar = plt.colorbar(im, ax=ax, shrink=0.85)
cbar.set_label('Estimated Density', fontsize=11)

ax.tick_params(labelsize=10)
plt.tight_layout()
plt.show()
```

---

## Summary

| Step | Code |
|------|------|
| Create grid | `xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]` |
| Stack positions | `positions = np.vstack([xx.ravel(), yy.ravel()])` |
| Compute KDE | `kernel = stats.gaussian_kde(np.vstack([x, y]))` |
| Evaluate | `density = kernel(positions).reshape(xx.shape)` |
| Display | `ax.imshow(density.T, extent=[...], origin='lower')` |


---

## Exercises

**Exercise 1.** Write code that generates 500 points from a bivariate normal distribution, computes a 2D KDE using `scipy.stats.gaussian_kde`, and visualizes it with `ax.imshow()`. Include `origin='lower'`, an appropriate `extent`, and a colorbar.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 500)
    x, y = data[:, 0], data[:, 1]

    xmin, xmax = x.min() - 1, x.max() + 1
    ymin, ymax = y.min() - 1, y.max() + 1
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])

    kernel = stats.gaussian_kde(np.vstack([x, y]))
    density = kernel(positions).reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(density.T, extent=[xmin, xmax, ymin, ymax],
                   origin='lower', cmap='viridis', aspect='auto')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('2D KDE Visualization')
    plt.colorbar(im, ax=ax, label='Density')
    plt.show()
    ```

---

**Exercise 2.** Explain the role of the `bw_method` parameter in `scipy.stats.gaussian_kde`. What happens visually when you use a very small bandwidth (e.g., 0.05) versus a very large bandwidth (e.g., 1.0)?

??? success "Solution to Exercise 2"
    The `bw_method` parameter controls the bandwidth (smoothing) of the kernel density estimate. It determines how wide each Gaussian kernel is around each data point.

    - **Very small bandwidth (e.g., 0.05)**: Each data point contributes a very narrow Gaussian. The result is a spiky, noisy density estimate that closely follows individual data points. This is called **underfitting** (high variance, low bias).
    - **Very large bandwidth (e.g., 1.0)**: Each data point contributes a very wide Gaussian. The result is an overly smooth density estimate that blurs out important features like clusters or modes. This is called **oversmoothing** (low variance, high bias).

    The default methods (`'scott'` and `'silverman'`) attempt to find a balanced bandwidth that captures the true density structure without excessive noise.

---

**Exercise 3.** Create a figure that overlays scatter points on top of a KDE heatmap. Use `alpha=0.3` for the scatter points and the `'Blues'` colormap for the KDE. Demonstrate this with bimodal data (two clusters).

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    c1 = np.random.multivariate_normal([2, 2], [[0.5, 0], [0, 0.5]], 300)
    c2 = np.random.multivariate_normal([-1, -1], [[0.3, 0.2], [0.2, 0.3]], 200)
    data = np.vstack([c1, c2])
    x, y = data[:, 0], data[:, 1]

    xmin, xmax = x.min() - 1, x.max() + 1
    ymin, ymax = y.min() - 1, y.max() + 1
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])

    kernel = stats.gaussian_kde(np.vstack([x, y]))
    density = kernel(positions).reshape(xx.shape)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(density.T, extent=[xmin, xmax, ymin, ymax],
                   origin='lower', cmap='Blues', aspect='auto')
    ax.scatter(x, y, c='red', s=10, alpha=0.3)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('KDE with Scatter Overlay (Bimodal Data)')
    plt.colorbar(im, ax=ax, label='Density')
    plt.show()
    ```

---

**Exercise 4.** Write code that creates a 1x3 subplot figure comparing `hist2d`, `hexbin`, and KDE (via `imshow`) side by side for the same dataset of 2000 points. Add a colorbar and title to each subplot.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 2000)
    x, y = data[:, 0], data[:, 1]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # hist2d
    _, _, _, im1 = axes[0].hist2d(x, y, bins=30, cmap='viridis')
    axes[0].set_title('hist2d')
    fig.colorbar(im1, ax=axes[0])

    # hexbin
    hb = axes[1].hexbin(x, y, gridsize=20, cmap='viridis')
    axes[1].set_title('hexbin')
    fig.colorbar(hb, ax=axes[1])

    # KDE
    xmin, xmax = x.min() - 1, x.max() + 1
    ymin, ymax = y.min() - 1, y.max() + 1
    xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([xx.ravel(), yy.ravel()])
    kernel = stats.gaussian_kde(np.vstack([x, y]))
    density = kernel(positions).reshape(xx.shape)

    im3 = axes[2].imshow(density.T, extent=[xmin, xmax, ymin, ymax],
                         origin='lower', cmap='viridis', aspect='auto')
    axes[2].set_title('KDE (imshow)')
    fig.colorbar(im3, ax=axes[2])

    plt.tight_layout()
    plt.show()
    ```
