# Axes Method - hexbin

The `ax.hexbin()` method creates hexagonal binning plots for 2D data density visualization.

!!! tip "Mental Model"
    `hexbin()` is a 2D histogram with hexagonal bins instead of squares. Hexagons tile the plane more naturally -- each bin has six equidistant neighbors, reducing visual artifacts. Color intensity shows how many points fall in each hexagon. Use it when scatter plots become too crowded to reveal density patterns.

    In the [density estimation spectrum](hist2d.md), hexbin occupies the middle
    ground: it is still a discrete binning method (like `hist2d`), but with
    better spatial geometry — hexagons minimize the maximum distance from any
    point to the nearest bin center, producing smoother-looking results without
    the computational cost of KDE.

[Official Documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.hexbin.html)

## Basic Usage

### Hexbin with Colorbar

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    mean = [0, 0]
    cov = [[1, 1], [1, 2]]
    x = np.random.multivariate_normal(mean, cov, 10000)
    print(f"{x.shape = }")
    
    fig, ax = plt.subplots()
    a = ax.hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues')  # type(a) PolyCollection
    plt.colorbar(a, label="density")
    plt.show()

if __name__ == "__main__":
    main()
```

## Understanding Hexbin

### Why Hexagons?

| Shape | Advantages |
|-------|------------|
| Hexagon | Equal distance to neighbors, better visual perception |
| Square | Simpler but diagonal neighbors are farther |

### Data Structure

```python
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

print(f"Shape: {x.shape}")        # (10000, 2)
print(f"X range: [{x[:,0].min():.2f}, {x[:,0].max():.2f}]")
print(f"Y range: [{x[:,1].min():.2f}, {x[:,1].max():.2f}]")
```

## gridsize Parameter

### Different Grid Sizes

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
gridsizes = [10, 20, 30, 50]

for ax, gs in zip(axes, gridsizes):
    hb = ax.hexbin(x[:, 0], x[:, 1], gridsize=gs, cmap='Blues')
    ax.set_title(f'gridsize={gs}')
    fig.colorbar(hb, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

### Asymmetric Gridsize

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Symmetric
hb1 = axes[0].hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues')
axes[0].set_title('gridsize=30')
fig.colorbar(hb1, ax=axes[0])

# Asymmetric (x, y)
hb2 = axes[1].hexbin(x[:, 0], x[:, 1], gridsize=(40, 20), cmap='Blues')
axes[1].set_title('gridsize=(40, 20)')
fig.colorbar(hb2, ax=axes[1])

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
cmaps = ['Blues', 'Reds', 'Greens', 'viridis', 'plasma', 'hot']

for ax, cmap in zip(axes.flat, cmaps):
    hb = ax.hexbin(x[:, 0], x[:, 1], gridsize=30, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")
    fig.colorbar(hb, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

## Reduce Functions

### C Parameter and reduce_C_function

```python
import matplotlib.pyplot as plt
import numpy as np

# Data with associated values
n = 10000
x = np.random.randn(n)
y = np.random.randn(n)
z = x**2 + y**2  # Value at each point

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Count (default)
hb1 = axes[0].hexbin(x, y, gridsize=20, cmap='Blues')
axes[0].set_title('Count (default)')
fig.colorbar(hb1, ax=axes[0])

# Mean of z values
hb2 = axes[1].hexbin(x, y, C=z, gridsize=20, cmap='Blues', reduce_C_function=np.mean)
axes[1].set_title('Mean of z')
fig.colorbar(hb2, ax=axes[1])

# Max of z values
hb3 = axes[2].hexbin(x, y, C=z, gridsize=20, cmap='Blues', reduce_C_function=np.max)
axes[2].set_title('Max of z')
fig.colorbar(hb3, ax=axes[2])

plt.tight_layout()
plt.show()
```

## Minimum Count

### mincnt Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
mincnts = [None, 5, 20]

for ax, mc in zip(axes, mincnts):
    hb = ax.hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues', mincnt=mc)
    ax.set_title(f'mincnt={mc}')
    fig.colorbar(hb, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

## Extent and Limits

### Setting Data Range

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Auto extent
hb1 = axes[0].hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues')
axes[0].set_title('Auto extent')
fig.colorbar(hb1, ax=axes[0])

# Custom extent
hb2 = axes[1].hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues',
                     extent=[-4, 4, -6, 6])
axes[1].set_title('extent=[-4, 4, -6, 6]')
fig.colorbar(hb2, ax=axes[1])

plt.tight_layout()
plt.show()
```

## Logarithmic Scale

### bins='log'

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Linear scale
hb1 = axes[0].hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues')
axes[0].set_title('Linear scale')
fig.colorbar(hb1, ax=axes[0])

# Log scale
hb2 = axes[1].hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues', bins='log')
axes[1].set_title("bins='log'")
fig.colorbar(hb2, ax=axes[1])

plt.tight_layout()
plt.show()
```

## Styling

### Edge Colors and Linewidths

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Default
hb1 = axes[0].hexbin(x[:, 0], x[:, 1], gridsize=20, cmap='Blues')
axes[0].set_title('Default')

# With edges
hb2 = axes[1].hexbin(x[:, 0], x[:, 1], gridsize=20, cmap='Blues',
                     edgecolors='black', linewidths=0.5)
axes[1].set_title('With black edges')

# White edges
hb3 = axes[2].hexbin(x[:, 0], x[:, 1], gridsize=20, cmap='Blues',
                     edgecolors='white', linewidths=1)
axes[2].set_title('With white edges')

for ax in axes:
    fig.colorbar(ax.collections[0], ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

## Return Value

### PolyCollection Object

```python
import matplotlib.pyplot as plt
import numpy as np

mean = [0, 0]
cov = [[1, 1], [1, 2]]
x = np.random.multivariate_normal(mean, cov, 10000)

fig, ax = plt.subplots()
hb = ax.hexbin(x[:, 0], x[:, 1], gridsize=30, cmap='Blues')

print(f"Type: {type(hb)}")  # PolyCollection
print(f"Array shape: {hb.get_array().shape}")  # Counts per hexagon

plt.colorbar(hb, label='counts')
plt.show()
```

## Practical Example

### Density Analysis

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate bimodal data
np.random.seed(42)
n = 5000
x1 = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], n)
x2 = np.random.multivariate_normal([3, 3], [[1, -0.5], [-0.5, 1]], n)
x = np.vstack([x1, x2])

fig, ax = plt.subplots(figsize=(10, 8))

hb = ax.hexbin(x[:, 0], x[:, 1], gridsize=35, cmap='YlOrRd', 
               edgecolors='white', linewidths=0.2)

ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_title('Bimodal Distribution Density', fontsize=14)

cbar = fig.colorbar(hb, ax=ax, label='Point Count')
plt.tight_layout()
plt.show()
```


---

## Exercises

**Exercise 1.** Write code that generates 5000 random points from a bivariate normal distribution with mean `[1, 2]` and covariance `[[2, 0.5], [0.5, 1]]`, then creates a hexbin plot with `gridsize=25`, the `'viridis'` colormap, and a colorbar.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    mean = [1, 2]
    cov = [[2, 0.5], [0.5, 1]]
    data = np.random.multivariate_normal(mean, cov, 5000)

    fig, ax = plt.subplots(figsize=(8, 6))
    hb = ax.hexbin(data[:, 0], data[:, 1], gridsize=25, cmap='viridis')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Hexbin Plot of Bivariate Normal Data')
    fig.colorbar(hb, ax=ax, label='Count')
    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 2.** Predict what happens when you pass `bins='log'` to `ax.hexbin()`. What does the colorbar represent in this case compared to the default?

??? success "Solution to Exercise 2"
    When `bins='log'` is passed to `ax.hexbin()`, the color mapping uses a logarithmic scale instead of a linear scale. The colorbar represents `log10(count)` rather than the raw count in each hexagonal bin. This is useful when the distribution of counts spans several orders of magnitude, as it prevents high-density bins from dominating the color range and makes lower-density regions more visible.

---

**Exercise 3.** Create a 1x3 subplot figure that shows the same dataset with three different `gridsize` values: 10, 25, and 50. Add a colorbar and title to each subplot. Explain how gridsize affects the visualization.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 5000)

    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    gridsizes = [10, 25, 50]

    for ax, gs in zip(axes, gridsizes):
        hb = ax.hexbin(data[:, 0], data[:, 1], gridsize=gs, cmap='Blues')
        ax.set_title(f'gridsize={gs}')
        fig.colorbar(hb, ax=ax, shrink=0.8)

    plt.tight_layout()
    plt.show()
    ```

    A smaller `gridsize` produces fewer, larger hexagons that aggregate more points per bin, giving a coarser view. A larger `gridsize` produces many smaller hexagons that reveal finer spatial detail but may have noisier counts per bin.

---

**Exercise 4.** Write code that uses the `C` parameter and `reduce_C_function=np.mean` to visualize the average value of a third variable `z = np.sin(x) + np.cos(y)` across hexagonal bins. Use `gridsize=20` and add a colorbar with an appropriate label.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    n = 10000
    x = np.random.randn(n)
    y = np.random.randn(n)
    z = np.sin(x) + np.cos(y)

    fig, ax = plt.subplots(figsize=(8, 6))
    hb = ax.hexbin(x, y, C=z, gridsize=20, cmap='coolwarm',
                   reduce_C_function=np.mean)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Mean of sin(x) + cos(y) per Hexagonal Bin')
    fig.colorbar(hb, ax=ax, label='Mean value of z')
    plt.tight_layout()
    plt.show()
    ```
