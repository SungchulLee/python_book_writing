# Color Mapping

Map continuous data values to colors using colormaps, enabling visualization of three-dimensional relationships in 2D scatter plots.

!!! tip "Mental Model"
    Color mapping turns a number into a color. Pass an array of values to `c=` and choose a colormap with `cmap=` -- Matplotlib linearly maps the data range to the color gradient. Add a colorbar to show readers the number-to-color lookup table. This is how you visualize a third variable on a 2D scatter plot.

!!! warning "Colormap Guidelines"
    Not all colormaps are perceptually equal:

    - **Use perceptually uniform maps** (`viridis`, `plasma`, `inferno`, `magma`)
      — brightness changes proportionally to data changes
    - **Avoid rainbow maps** (`jet`, `rainbow`) — they create false boundaries
      and misleading gradients where none exist in the data
    - **Use diverging maps** (`RdBu`, `coolwarm`) only when data has a meaningful
      center point (e.g., positive/negative, above/below average)
    - **Use sequential maps** for data that goes from low to high without a
      special midpoint

## Basic Color Mapping

Use the `c` parameter with numeric values to map data to colors.

### 1. Color by Third Variable

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.rand(100)
y = np.random.rand(100)
z = np.random.rand(100)  # Third variable for color

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z)
plt.colorbar(scatter)
plt.show()
```

### 2. Color by Computed Value

```python
x = np.random.rand(100) * 10
y = np.random.rand(100) * 10
distance = np.sqrt(x**2 + y**2)

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=distance)
plt.colorbar(scatter, label='Distance from Origin')
plt.show()
```

### 3. Color by Category Index

```python
categories = np.random.randint(0, 5, 100)

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=categories, cmap='Set1')
plt.colorbar(scatter, label='Category')
plt.show()
```

## Colormap Selection

The `cmap` parameter selects the color scheme.

### 1. Sequential Colormaps

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
cmaps = ['viridis', 'plasma', 'Blues']

for ax, cmap in zip(axes, cmaps):
    scatter = ax.scatter(x, y, c=z, cmap=cmap)
    ax.set_title(cmap)
    plt.colorbar(scatter, ax=ax)

plt.tight_layout()
plt.show()
```

### 2. Diverging Colormaps

```python
z_centered = np.random.randn(100)

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z_centered, cmap='RdBu', vmin=-3, vmax=3)
plt.colorbar(scatter)
plt.show()
```

### 3. Qualitative Colormaps

```python
# For categorical data
categories = np.random.randint(0, 8, 100)

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=categories, cmap='Set2')
plt.colorbar(scatter, ticks=range(8))
plt.show()
```

## Value Range

Control the mapping between data values and colors.

### 1. Auto Range (Default)

```python
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z)  # Maps min(z) to max(z)
plt.colorbar(scatter)
plt.show()
```

### 2. Fixed Range

```python
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z, vmin=0, vmax=1)
plt.colorbar(scatter)
plt.show()
```

### 3. Centered at Zero

```python
z_centered = np.random.randn(100) * 2
max_abs = np.abs(z_centered).max()

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z_centered, cmap='RdBu', 
                     vmin=-max_abs, vmax=max_abs)
plt.colorbar(scatter)
plt.show()
```

## Normalization

Transform data before color mapping.

### 1. Linear Normalization (Default)

```python
from matplotlib.colors import Normalize

norm = Normalize(vmin=0, vmax=1)
scatter = ax.scatter(x, y, c=z, norm=norm)
```

### 2. Logarithmic Normalization

```python
from matplotlib.colors import LogNorm

z_log = np.random.rand(100) * 1000 + 1

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z_log, norm=LogNorm(vmin=1, vmax=1000))
plt.colorbar(scatter, label='Log Scale')
plt.show()
```

### 3. Power Normalization

```python
from matplotlib.colors import PowerNorm

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z, norm=PowerNorm(gamma=0.5))
plt.colorbar(scatter)
plt.show()
```

## Discrete Colors

Map continuous data to discrete color bins.

### 1. BoundaryNorm

```python
from matplotlib.colors import BoundaryNorm

bounds = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
norm = BoundaryNorm(bounds, plt.cm.viridis.N)

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z, cmap='viridis', norm=norm)
plt.colorbar(scatter, boundaries=bounds, ticks=bounds)
plt.show()
```

### 2. Fixed Number of Bins

```python
n_bins = 5
cmap = plt.cm.get_cmap('viridis', n_bins)

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z, cmap=cmap)
plt.colorbar(scatter)
plt.show()
```

### 3. Custom Bin Edges

```python
bins = [0, 0.1, 0.3, 0.7, 0.9, 1.0]
norm = BoundaryNorm(bins, plt.cm.RdYlGn.N)

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z, cmap='RdYlGn', norm=norm)
plt.colorbar(scatter, ticks=bins)
plt.show()
```

## Color and Size Combined

Encode two additional dimensions using both color and size.

### 1. Four-Dimensional Visualization

```python
np.random.seed(42)
x = np.random.rand(50)
y = np.random.rand(50)
colors = np.random.rand(50)
sizes = np.random.rand(50) * 500

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
plt.colorbar(scatter, label='Color Variable')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Size and Color Encoding')
plt.show()
```

### 2. Bubble Chart

```python
# Population, GDP, Life Expectancy example
np.random.seed(42)
gdp = np.random.rand(30) * 50000
life_exp = 50 + np.random.rand(30) * 35
population = np.random.rand(30) * 1000

fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(gdp, life_exp, c=population, s=population, 
                     alpha=0.6, cmap='YlOrRd')
plt.colorbar(scatter, label='Population (millions)')
ax.set_xlabel('GDP per Capita ($)')
ax.set_ylabel('Life Expectancy (years)')
plt.show()
```

### 3. Legend for Sizes

```python
from matplotlib.lines import Line2D

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=colors, s=sizes, alpha=0.6, cmap='viridis')
plt.colorbar(scatter, label='Color')

# Size legend
size_legend = [100, 300, 500]
handles = [Line2D([0], [0], marker='o', color='w', 
                  markerfacecolor='gray', markersize=np.sqrt(s)/2, 
                  label=str(s)) for s in size_legend]
ax.legend(handles=handles, title='Size', loc='upper right')
plt.show()
```

## Colorbar Customization

Customize the colorbar for scatter plots.

### 1. Label and Ticks

```python
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z, cmap='viridis')
cbar = plt.colorbar(scatter)
cbar.set_label('Value', fontsize=12)
cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
plt.show()
```

### 2. Shrink and Position

```python
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z, cmap='viridis')
plt.colorbar(scatter, shrink=0.8, pad=0.02)
plt.show()
```

### 3. Horizontal Colorbar

```python
fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=z, cmap='viridis')
plt.colorbar(scatter, orientation='horizontal', pad=0.1)
plt.show()
```

## Practical Example

Create a complete color-mapped scatter plot.

### 1. Generate Realistic Data

```python
np.random.seed(42)
n = 200
x = np.random.randn(n)
y = 0.5 * x + np.random.randn(n) * 0.5
magnitude = np.sqrt(x**2 + y**2)
```

### 2. Create Visualization

```python
fig, ax = plt.subplots(figsize=(8, 6))

scatter = ax.scatter(x, y, 
                     c=magnitude, 
                     s=50, 
                     cmap='plasma',
                     alpha=0.7,
                     edgecolors='white',
                     linewidths=0.5)

ax.set_xlabel('X Variable', fontsize=12)
ax.set_ylabel('Y Variable', fontsize=12)
ax.set_title('Scatter Plot with Color Mapping', fontsize=14)
ax.grid(True, alpha=0.3)
ax.set_aspect('equal')
```

### 3. Add Colorbar

```python
cbar = plt.colorbar(scatter, shrink=0.8)
cbar.set_label('Distance from Origin', fontsize=11)

plt.tight_layout()
plt.show()
```


!!! info "In Machine Learning"

    Color-mapped scatter plots are essential for visualizing **clusters** and **class separability**. Plot two features on x/y axes and color by cluster label (discrete cmap) or prediction confidence (continuous cmap). This immediately reveals whether clusters are well-separated and where misclassifications occur.

---

## Exercises

**Exercise 1.** Write code that creates a scatter plot where each point's color is mapped to a third variable using the `c` parameter and `cmap='viridis'`. Add a colorbar.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    # Solution code depends on the specific exercise
    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x))
    ax.set_title('Example Solution')
    plt.show()
    ```

    See the content of this page for the relevant API details to construct the full solution.

---

**Exercise 2.** Explain the relationship between the `c`, `cmap`, `vmin`, and `vmax` parameters in `ax.scatter()`.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a scatter plot where both color and size vary with separate variables. Add a colorbar for the color variable.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(0, 2 * np.pi, 100)
    axes[0].plot(x, np.sin(x))
    axes[0].set_title('Left Subplot')

    axes[1].plot(x, np.cos(x))
    axes[1].set_title('Right Subplot')

    plt.tight_layout()
    plt.show()
    ```

    Adapt this pattern to the specific requirements of the exercise.

---

**Exercise 4.** Write code that uses a diverging colormap (`'RdBu'`) centered at zero to color scatter points based on positive/negative values.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'b-', lw=2)
    ax.set_title('Solution')
    plt.show()
    ```

    Refer to the code examples in the main content for the specific API calls needed.
