# Axes Method - hist2d

The `ax.hist2d()` method creates 2D histograms with rectangular bins.

!!! tip "Mental Model"
    `hist2d()` divides the x-y plane into a grid of rectangular cells and colors each cell by how many data points fall inside it. It is the 2D extension of a 1D histogram -- instead of binning along one axis, you bin along two simultaneously. The result is a heatmap of point density.

!!! note "2D Density Visualization Model"
    When scatter plots break down due to overplotting, you need **density estimation**.
    All three methods in this section approximate the same underlying density
    $f(x, y)$ — they differ in how they discretize and smooth:

    | Method | Approximation | Resolution parameter | Tradeoff |
    |--------|--------------|---------------------|----------|
    | `hist2d` | Piecewise constant (rectangles) | `bins` | Fast + simple, but blocky |
    | `hexbin` | Piecewise constant (hexagons) | `gridsize` | Better tiling geometry |
    | KDE | Smooth continuous function | `bandwidth` | Smooth + analytical, but expensive |

    The resolution parameter (bins / gridsize / bandwidth) controls the same
    tradeoff in all three: **too small → noisy, too large → oversmoothed.**

    **Decision guide:**

    - Fast exploration → `hist2d`
    - Publication-quality density → `hexbin`
    - Smooth probability surface / contour integration → KDE

[Official Documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist2d.html)

## Basic Usage

### 2D Histogram with Colorbar

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    mean = [0, 0]
    cov = [[1, 1], [1, 2]]
    x = np.random.multivariate_normal(mean, cov, 10000)
    print(f"{x.shape = }")
    
    fig, ax = plt.subplots()
    _, _, _, a = ax.hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues')  # type(a) QuadMesh
    plt.colorbar(a, label='counts in bin')
    plt.show()

if __name__ == "__main__":
    main()
```

## Return Values

### Understanding the Return Tuple

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, ax = plt.subplots()
h, xedges, yedges, image = ax.hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues')

print(f"h (counts): {h.shape}")           # (30, 30) - bin counts
print(f"xedges: {xedges.shape}")          # (31,) - x bin edges
print(f"yedges: {yedges.shape}")          # (31,) - y bin edges
print(f"image type: {type(image)}")       # QuadMesh

plt.colorbar(image, label='counts')
plt.show()
```

## bins Parameter

### Number of Bins

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
bin_counts = [10, 20, 30, 50]

for ax, bins in zip(axes, bin_counts):
    _, _, _, im = ax.hist2d(x[:, 0], x[:, 1], bins=bins, cmap='Blues')
    ax.set_title(f'bins={bins}')
    fig.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

### Asymmetric Bins

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Symmetric bins
_, _, _, im1 = axes[0].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues')
axes[0].set_title('bins=30')
fig.colorbar(im1, ax=axes[0])

# Asymmetric bins
_, _, _, im2 = axes[1].hist2d(x[:, 0], x[:, 1], bins=[40, 20], cmap='Blues')
axes[1].set_title('bins=[40, 20]')
fig.colorbar(im2, ax=axes[1])

plt.tight_layout()
plt.show()
```

### Custom Bin Edges

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

# Custom bin edges
xbins = np.linspace(-4, 4, 41)
ybins = np.linspace(-6, 6, 31)

fig, ax = plt.subplots(figsize=(8, 6))
_, _, _, im = ax.hist2d(x[:, 0], x[:, 1], bins=[xbins, ybins], cmap='Blues')
ax.set_title('Custom bin edges')
fig.colorbar(im, label='counts')
plt.show()
```

## Range Parameter

### Limiting Data Range

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Full range
_, _, _, im1 = axes[0].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues')
axes[0].set_title('Full range')
fig.colorbar(im1, ax=axes[0])

# Limited range
_, _, _, im2 = axes[1].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues',
                              range=[[-2, 2], [-3, 3]])
axes[1].set_title('range=[[-2, 2], [-3, 3]]')
fig.colorbar(im2, ax=axes[1])

plt.tight_layout()
plt.show()
```

## Colormaps

### Different Colormaps

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
cmaps = ['Blues', 'Reds', 'viridis', 'plasma', 'hot', 'YlOrRd']

for ax, cmap in zip(axes.flat, cmaps):
    _, _, _, im = ax.hist2d(x[:, 0], x[:, 1], bins=30, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")
    fig.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

## Normalization

### norm Parameter

```python
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Linear (default)
_, _, _, im1 = axes[0].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues')
axes[0].set_title('Linear (default)')
fig.colorbar(im1, ax=axes[0])

# Log scale
_, _, _, im2 = axes[1].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues',
                              norm=colors.LogNorm())
axes[1].set_title('LogNorm')
fig.colorbar(im2, ax=axes[1])

# Power norm
_, _, _, im3 = axes[2].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues',
                              norm=colors.PowerNorm(gamma=0.5))
axes[2].set_title('PowerNorm(gamma=0.5)')
fig.colorbar(im3, ax=axes[2])

plt.tight_layout()
plt.show()
```

## Value Limits

### vmin and vmax

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Auto limits
_, _, _, im1 = axes[0].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues')
axes[0].set_title('Auto limits')
fig.colorbar(im1, ax=axes[0])

# Custom vmax
_, _, _, im2 = axes[1].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues', vmax=50)
axes[1].set_title('vmax=50')
fig.colorbar(im2, ax=axes[1])

# Custom vmin and vmax
_, _, _, im3 = axes[2].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues',
                              vmin=10, vmax=80)
axes[2].set_title('vmin=10, vmax=80')
fig.colorbar(im3, ax=axes[2])

plt.tight_layout()
plt.show()
```

## Density Mode

### density Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Counts (default)
_, _, _, im1 = axes[0].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues')
axes[0].set_title('Counts (default)')
fig.colorbar(im1, ax=axes[0], label='counts')

# Density
_, _, _, im2 = axes[1].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues', density=True)
axes[1].set_title('density=True')
fig.colorbar(im2, ax=axes[1], label='density')

plt.tight_layout()
plt.show()
```

## Minimum Count

### cmin Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
cmins = [None, 5, 20]

for ax, cmin in zip(axes, cmins):
    _, _, _, im = ax.hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues', cmin=cmin)
    ax.set_title(f'cmin={cmin}')
    fig.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

## Comparison: hist2d vs hexbin vs KDE

### Side by Side

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# hist2d
_, _, _, im1 = axes[0].hist2d(x[:, 0], x[:, 1], bins=30, cmap='Blues')
axes[0].set_title('hist2d')
fig.colorbar(im1, ax=axes[0])

# hexbin
im2 = axes[1].hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues')
axes[1].set_title('hexbin')
fig.colorbar(im2, ax=axes[1])

# KDE with imshow
kde = stats.gaussian_kde(x.T)
x_ = np.linspace(-4, 4, 80)
y_ = np.linspace(-6, 6, 80)
X, Y = np.meshgrid(x_, y_)
Z = kde.evaluate(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
im3 = axes[2].imshow(Z, origin='lower', aspect='auto',
                     extent=[-4, 4, -6, 6], cmap='Blues')
axes[2].set_title('KDE (imshow)')
fig.colorbar(im3, ax=axes[2])

plt.tight_layout()
plt.show()
```

## Practical Example

### Distribution Analysis

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate bimodal data
np.random.seed(42)
n = 5000
x1 = np.random.multivariate_normal([-1, -1], [[0.5, 0.2], [0.2, 0.5]], n)
x2 = np.random.multivariate_normal([2, 2], [[0.8, -0.3], [-0.3, 0.8]], n)
x = np.vstack([x1, x2])

fig, ax = plt.subplots(figsize=(10, 8))

h, xedges, yedges, im = ax.hist2d(
    x[:, 0], x[:, 1], 
    bins=40, 
    cmap='YlOrRd',
    cmin=1
)

ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_title('2D Histogram: Bimodal Distribution', fontsize=14)

cbar = fig.colorbar(im, ax=ax, label='Counts per bin')

# Add statistics
total_points = len(x)
ax.text(0.02, 0.98, f'Total points: {total_points}',
        transform=ax.transAxes, fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()
```


---

## Exercises

**Exercise 1.** Write code that creates a 2D histogram of 8000 points drawn from a bivariate normal distribution. Use `bins=40`, the `'plasma'` colormap, and add a colorbar. Print the shape of the returned count array `h`.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    mean = [0, 0]
    cov = [[1, 0.5], [0.5, 1]]
    data = np.random.multivariate_normal(mean, cov, 8000)

    fig, ax = plt.subplots(figsize=(8, 6))
    h, xedges, yedges, im = ax.hist2d(
        data[:, 0], data[:, 1], bins=40, cmap='plasma'
    )
    fig.colorbar(im, ax=ax, label='Counts')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('2D Histogram')
    print(f"h.shape = {h.shape}")  # (40, 40)
    plt.show()
    ```

---

**Exercise 2.** Predict the output of the following code:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(1000)
y = np.random.randn(1000)

fig, ax = plt.subplots()
h, xedges, yedges, im = ax.hist2d(x, y, bins=20)
print(h.shape)
print(xedges.shape)
print(yedges.shape)
```

??? success "Solution to Exercise 2"
    The output is:

    ```
    (20, 20)
    (21,)
    (21,)
    ```

    The count array `h` has shape `(bins, bins)` = `(20, 20)`. The edge arrays have shape `(bins + 1,)` = `(21,)` because they define the boundaries of each bin (one more edge than the number of bins).

---

**Exercise 3.** Create a 1x2 subplot figure comparing `hist2d` with `density=False` (left) and `density=True` (right) for the same dataset. Add colorbars with labels `'Counts'` and `'Density'` respectively.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 5000)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    _, _, _, im1 = axes[0].hist2d(data[:, 0], data[:, 1], bins=30, cmap='Blues')
    axes[0].set_title('density=False (default)')
    fig.colorbar(im1, ax=axes[0], label='Counts')

    _, _, _, im2 = axes[1].hist2d(data[:, 0], data[:, 1], bins=30, cmap='Blues',
                                   density=True)
    axes[1].set_title('density=True')
    fig.colorbar(im2, ax=axes[1], label='Density')

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 4.** Write code that uses the `cmin` parameter to hide bins with fewer than 10 counts. Generate bimodal data by combining two clusters, use `bins=30`, and add a colorbar.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    c1 = np.random.multivariate_normal([-2, -2], [[0.5, 0], [0, 0.5]], 3000)
    c2 = np.random.multivariate_normal([2, 2], [[0.5, 0], [0, 0.5]], 3000)
    data = np.vstack([c1, c2])

    fig, ax = plt.subplots(figsize=(8, 6))
    _, _, _, im = ax.hist2d(data[:, 0], data[:, 1], bins=30, cmap='YlOrRd',
                            cmin=10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('2D Histogram with cmin=10')
    fig.colorbar(im, ax=ax, label='Counts (bins < 10 hidden)')
    plt.tight_layout()
    plt.show()
    ```
