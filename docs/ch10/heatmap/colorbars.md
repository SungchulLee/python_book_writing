# Colorbars

Colorbars provide a visual legend mapping colors to data values, essential for interpreting heatmaps and other color-coded visualizations.

!!! tip "Mental Model"
    A colorbar is a legend for continuous color scales. It shows the mapping from data values to colors so readers can decode heatmaps, scatter plots, and contour fills. Always add a colorbar when using `imshow`, `pcolormesh`, `contourf`, or `scatter` with color mapping -- without it, the colors are meaningless.

!!! info "The Key Idea: Normalization"
    A colorbar visualizes a **normalization** — the function that maps data values to colors. By default, matplotlib uses linear normalization between `vmin` and `vmax`. Changing the normalization (e.g., `LogNorm`, `TwoSlopeNorm`) changes what colors mean. This is why `vmin`/`vmax` matter so much: they define the mapping, and shared subplots must share the same normalization or the colors become incomparable.

!!! danger "Misleading Scales"
    Changing `vmin`/`vmax` between subplots makes identical colors represent different values. When comparing multiple heatmaps, always use the **same normalization** — pass the same `vmin`, `vmax`, and `norm` to each plot, and share a single colorbar. Otherwise, readers will misinterpret differences.

## Basic Colorbar

Add a colorbar to a plot.

### 1. Simple Addition

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.rand(10, 10)

fig, ax = plt.subplots()
im = ax.imshow(data)
plt.colorbar(im)
plt.show()
```

### 2. Specify Axes

```python
fig, ax = plt.subplots()
im = ax.imshow(data)
plt.colorbar(im, ax=ax)
```

### 3. Using Figure Method

```python
fig, ax = plt.subplots()
im = ax.imshow(data)
fig.colorbar(im, ax=ax)
```

## Colorbar Label

Add descriptive labels to the colorbar.

### 1. Label Parameter

```python
fig, ax = plt.subplots()
im = ax.imshow(data, cmap='viridis')
plt.colorbar(im, label='Intensity')
plt.show()
```

### 2. LaTeX Label

```python
plt.colorbar(im, label=r'Temperature ($^\circ$C)')
```

### 3. Set Label After Creation

```python
cbar = plt.colorbar(im)
cbar.set_label('Value', fontsize=12, rotation=270, labelpad=15)
```

## Colorbar Position

Control where the colorbar appears.

### 1. Location Parameter

```python
fig, ax = plt.subplots()
im = ax.imshow(data)

# Options: 'right', 'left', 'top', 'bottom'
plt.colorbar(im, location='right')
plt.show()
```

### 2. Horizontal Colorbar

```python
fig, ax = plt.subplots()
im = ax.imshow(data)
plt.colorbar(im, orientation='horizontal')
plt.show()
```

### 3. Custom Position with cax

```python
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, ax = plt.subplots()
im = ax.imshow(data)

divider = make_axes_locatable(ax)
cax = divider.append_axes('right', size='5%', pad=0.1)
plt.colorbar(im, cax=cax)
plt.show()
```

## Colorbar Size

Adjust colorbar dimensions.

### 1. Shrink Parameter

```python
fig, ax = plt.subplots()
im = ax.imshow(data)
plt.colorbar(im, shrink=0.8)  # 80% of default height
plt.show()
```

### 2. Aspect Ratio

```python
plt.colorbar(im, aspect=30)  # Length / width ratio
```

### 3. Fraction and Pad

```python
plt.colorbar(im, fraction=0.046, pad=0.04)
```

## Tick Customization

Control colorbar tick positions and labels.

### 1. Set Ticks

```python
fig, ax = plt.subplots()
im = ax.imshow(data, vmin=0, vmax=1)
cbar = plt.colorbar(im, ticks=[0, 0.25, 0.5, 0.75, 1])
plt.show()
```

### 2. Custom Labels

```python
cbar = plt.colorbar(im, ticks=[0, 0.5, 1])
cbar.ax.set_yticklabels(['Low', 'Medium', 'High'])
```

### 3. Tick Parameters

```python
cbar = plt.colorbar(im)
cbar.ax.tick_params(labelsize=10, length=5, width=1)
```

## Discrete Colorbars

Create colorbars for categorical or binned data.

### 1. Boundaries and Values

```python
import matplotlib.colors as mcolors

bounds = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
norm = mcolors.BoundaryNorm(bounds, plt.cm.viridis.N)

fig, ax = plt.subplots()
im = ax.imshow(data, cmap='viridis', norm=norm)
plt.colorbar(im, boundaries=bounds, ticks=bounds)
plt.show()
```

### 2. Fixed Number of Colors

```python
from matplotlib.colors import BoundaryNorm

n_colors = 5
cmap = plt.cm.get_cmap('viridis', n_colors)
bounds = np.linspace(0, 1, n_colors + 1)
norm = BoundaryNorm(bounds, cmap.N)

fig, ax = plt.subplots()
im = ax.imshow(data, cmap=cmap, norm=norm)
plt.colorbar(im, ticks=bounds[:-1] + 0.1)
plt.show()
```

### 3. Categorical Colorbar

```python
categories = ['A', 'B', 'C', 'D']
cat_data = np.random.randint(0, 4, (10, 10))

cmap = plt.cm.get_cmap('Set1', len(categories))

fig, ax = plt.subplots()
im = ax.imshow(cat_data, cmap=cmap, vmin=-0.5, vmax=len(categories)-0.5)
cbar = plt.colorbar(im, ticks=range(len(categories)))
cbar.ax.set_yticklabels(categories)
plt.show()
```

## Colorbar with Subplots

Handle colorbars in multi-plot layouts.

### 1. Individual Colorbars

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax in axes:
    data = np.random.rand(10, 10)
    im = ax.imshow(data)
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

### 2. Shared Colorbar

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

vmin, vmax = 0, 1
for ax in axes:
    data = np.random.rand(10, 10)
    im = ax.imshow(data, vmin=vmin, vmax=vmax)

fig.colorbar(im, ax=axes, shrink=0.8, label='Shared Scale')
plt.tight_layout()
plt.show()
```

### 3. Colorbar Axes List

```python
fig, axes = plt.subplots(2, 2, figsize=(8, 8))

for ax in axes.flat:
    data = np.random.rand(10, 10)
    im = ax.imshow(data, vmin=0, vmax=1)

fig.colorbar(im, ax=axes.ravel().tolist(), shrink=0.6)
plt.tight_layout()
plt.show()
```

## Logarithmic Colorbar

Display data with logarithmic color scaling.

### 1. LogNorm

```python
from matplotlib.colors import LogNorm

data_log = np.random.rand(10, 10) * 1000 + 1

fig, ax = plt.subplots()
im = ax.imshow(data_log, norm=LogNorm(vmin=1, vmax=1000))
plt.colorbar(im, label='Log Scale')
plt.show()
```

### 2. SymLogNorm for Negative Values

```python
from matplotlib.colors import SymLogNorm

data_sym = np.random.randn(10, 10) * 100

fig, ax = plt.subplots()
im = ax.imshow(data_sym, cmap='RdBu', 
               norm=SymLogNorm(linthresh=1, vmin=-100, vmax=100))
plt.colorbar(im)
plt.show()
```

### 3. PowerNorm

```python
from matplotlib.colors import PowerNorm

fig, ax = plt.subplots()
im = ax.imshow(data, norm=PowerNorm(gamma=0.5))
plt.colorbar(im)
plt.show()
```

## Colorbar Styling

Customize colorbar appearance.

### 1. Outline

```python
cbar = plt.colorbar(im)
cbar.outline.set_edgecolor('black')
cbar.outline.set_linewidth(2)
```

### 2. Extension Arrows

```python
# Show arrows when data exceeds vmin/vmax
plt.colorbar(im, extend='both')  # 'min', 'max', 'both', 'neither'
```

### 3. Draw Edges

```python
cbar = plt.colorbar(im, drawedges=True)
```

## Complete Example

Create a polished heatmap with customized colorbar.

### 1. Setup Data

```python
np.random.seed(42)
data = np.random.randn(12, 12)
```

### 2. Create Figure

```python
fig, ax = plt.subplots(figsize=(8, 6))

im = ax.imshow(data, cmap='RdBu', vmin=-3, vmax=3)

ax.set_xticks(np.arange(12))
ax.set_yticks(np.arange(12))
ax.set_xticklabels([f'C{i}' for i in range(12)], rotation=45, ha='right')
ax.set_yticklabels([f'R{i}' for i in range(12)])
ax.set_title('Heatmap with Custom Colorbar')
```

### 3. Add Colorbar

```python
cbar = plt.colorbar(im, shrink=0.8, aspect=30, pad=0.02)
cbar.set_label('Z-Score', fontsize=12)
cbar.set_ticks([-3, -2, -1, 0, 1, 2, 3])
cbar.ax.tick_params(labelsize=10)

plt.tight_layout()
plt.show()
```


---

## Exercises

**Exercise 1.** Write code that creates a heatmap from a 10x10 random array and adds a colorbar with a custom label. Use the `'viridis'` colormap.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.rand(10, 10)

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='viridis')
    cbar = fig.colorbar(im, ax=ax, label='Random Values')
    ax.set_title('Heatmap with Colorbar')
    plt.show()
    ```

---

**Exercise 2.** Explain the difference between `fig.colorbar()` and `plt.colorbar()`. When would you use each?

??? success "Solution to Exercise 2"
    `fig.colorbar(mappable, ax=ax)` adds a colorbar to a specific axes within the figure. `plt.colorbar()` adds a colorbar to the current axes using the pyplot state machine. Use `fig.colorbar()` when working with the OOP style (explicit Figure and Axes objects), and `plt.colorbar()` only when using the pyplot style. The OOP version is preferred for multi-subplot figures because you can control exactly which axes the colorbar is associated with.

---

**Exercise 3.** Create a figure with two heatmaps side by side, each with its own colorbar. Use `shrink=0.8` to reduce the colorbar height.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data1 = np.random.rand(8, 8)
    data2 = np.random.randn(8, 8)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    im1 = ax1.imshow(data1, cmap='hot')
    fig.colorbar(im1, ax=ax1, shrink=0.8, label='Values')
    ax1.set_title('Uniform Random')

    im2 = ax2.imshow(data2, cmap='coolwarm')
    fig.colorbar(im2, ax=ax2, shrink=0.8, label='Values')
    ax2.set_title('Normal Random')

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 4.** Write code that creates a heatmap and customizes the colorbar with discrete tick values using `cbar.set_ticks()` and `cbar.set_ticklabels()`.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.rand(10, 10) * 100

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='YlOrRd')
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_ticks([0, 25, 50, 75, 100])
    cbar.set_ticklabels(['Low', '25%', 'Mid', '75%', 'High'])
    cbar.set_label('Custom Scale')
    ax.set_title('Heatmap with Custom Colorbar Ticks')
    plt.show()
    ```
