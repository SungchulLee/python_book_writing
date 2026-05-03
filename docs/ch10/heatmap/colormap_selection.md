# Colormap Selection

Choosing the right colormap is critical for effective data visualization. This guide covers colormap categories, selection criteria, and best practices.

!!! tip "Mental Model"
    Match your colormap to your data type: sequential (e.g., `viridis`) for ordered values like temperature, diverging (e.g., `coolwarm`) for values centered around zero like profit/loss, and qualitative (e.g., `Set1`) for unordered categories. A wrong choice can mislead readers -- the default `viridis` is perceptually uniform and colorblind-safe, making it a reliable default.

!!! tip "Default Strategy"
    **Use `viridis` unless you have a specific reason not to.** It is perceptually uniform (equal steps in data produce equal perceived color changes), prints well in grayscale, and is accessible to colorblind readers. Switch to a diverging map (`coolwarm`, `RdBu`) only when your data has a meaningful center, and to qualitative (`Set1`, `tab10`) only for unordered categories.

!!! warning "Why Jet and Rainbow Are Harmful"
    Human vision perceives brightness non-uniformly — we are far more sensitive to changes in yellow-green than in blue or red. Non-uniform colormaps like `jet` create false boundaries and hide real gradients. A smooth gradient in data can appear as sharp bands in `jet`, leading readers to see structure that does not exist. Perceptually uniform colormaps (`viridis`, `plasma`, `inferno`) eliminate this distortion.

## Colormap Categories

Matplotlib provides several categories of colormaps:

| Category | Use Case | Examples |
|----------|----------|----------|
| Sequential | Data with natural ordering (low→high) | `viridis`, `plasma`, `Blues` |
| Diverging | Data with meaningful center point | `coolwarm`, `RdBu`, `seismic` |
| Cyclic | Periodic data (angles, phases) | `twilight`, `hsv` |
| Qualitative | Categorical data | `Set1`, `tab10`, `Paired` |

## Setup

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
```

---

## Sequential Colormaps

Best for data that progresses from low to high values.

### Perceptually Uniform

These colormaps have uniform perceptual brightness changes, making them ideal for scientific visualization.

```python
Z = np.exp(-(X**2 + Y**2))

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'turbo']

for ax, cmap in zip(axes.flat, cmaps):
    im = ax.imshow(Z, cmap=cmap, origin='lower')
    ax.set_title(f"'{cmap}'")
    ax.axis('off')
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.suptitle('Perceptually Uniform Sequential Colormaps', fontsize=14)
plt.tight_layout()
plt.show()
```

### Single-Hue Sequential

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

cmaps = ['Blues', 'Greens', 'Reds', 'Purples', 'Oranges', 'Greys']

for ax, cmap in zip(axes.flat, cmaps):
    im = ax.imshow(Z, cmap=cmap, origin='lower')
    ax.set_title(f"'{cmap}'")
    ax.axis('off')
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.suptitle('Single-Hue Sequential Colormaps', fontsize=14)
plt.tight_layout()
plt.show()
```

### Multi-Hue Sequential

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

cmaps = ['YlOrRd', 'YlGnBu', 'BuPu', 'GnBu', 'PuBuGn', 'OrRd']

for ax, cmap in zip(axes.flat, cmaps):
    im = ax.imshow(Z, cmap=cmap, origin='lower')
    ax.set_title(f"'{cmap}'")
    ax.axis('off')
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.suptitle('Multi-Hue Sequential Colormaps', fontsize=14)
plt.tight_layout()
plt.show()
```

### When to Use Sequential

- Density plots
- Probability distributions
- Temperature (single direction)
- Elevation maps
- Any monotonically increasing data

```python
# Example: Probability density
from scipy import stats

rv = stats.multivariate_normal([0, 0], [[1, 0], [0, 1]])
Z_pdf = rv.pdf(np.dstack((X, Y)))

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(Z_pdf, extent=[-3, 3, -3, 3], origin='lower', cmap='viridis')
ax.set_title('Bivariate Normal PDF')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.colorbar(im, ax=ax, label='Density')
plt.show()
```

---

## Diverging Colormaps

Best for data with a meaningful center point (often zero).

### Standard Diverging

```python
Z_div = X**2 - Y**2  # Saddle function with positive and negative values

fig, axes = plt.subplots(2, 3, figsize=(15, 9))

cmaps = ['coolwarm', 'RdBu', 'seismic', 'bwr', 'RdYlBu', 'PiYG']

for ax, cmap in zip(axes.flat, cmaps):
    im = ax.imshow(Z_div, cmap=cmap, origin='lower')
    ax.set_title(f"'{cmap}'")
    ax.axis('off')
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.suptitle('Diverging Colormaps', fontsize=14)
plt.tight_layout()
plt.show()
```

### Centered Normalization

For diverging data, center the colormap at zero:

```python
from matplotlib.colors import TwoSlopeNorm

Z_asym = X**2 - Y**2 + 2  # Asymmetric around zero

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Without centering
im1 = axes[0].imshow(Z_asym, cmap='RdBu', origin='lower')
axes[0].set_title('Default Normalization')
plt.colorbar(im1, ax=axes[0])

# With centering at zero
norm = TwoSlopeNorm(vmin=Z_asym.min(), vcenter=0, vmax=Z_asym.max())
im2 = axes[1].imshow(Z_asym, cmap='RdBu', norm=norm, origin='lower')
axes[1].set_title('Centered at Zero (TwoSlopeNorm)')
plt.colorbar(im2, ax=axes[1])

plt.tight_layout()
plt.show()
```

### When to Use Diverging

- Correlation matrices
- Temperature anomalies
- Profit/loss data
- Deviations from mean
- Any data with positive and negative values around a center

```python
# Example: Correlation matrix
np.random.seed(42)
data = np.random.randn(5, 100)
corr = np.corrcoef(data)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(corr, cmap='RdBu', vmin=-1, vmax=1)
ax.set_title('Correlation Matrix')
ax.set_xticks(range(5))
ax.set_yticks(range(5))
plt.colorbar(im, ax=ax, label='Correlation')
plt.show()
```

---

## Cyclic Colormaps

Best for periodic data like angles or phases.

### Available Cyclic Colormaps

```python
theta = np.arctan2(Y, X)  # Angle in radians

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

cmaps = ['twilight', 'twilight_shifted', 'hsv']

for ax, cmap in zip(axes, cmaps):
    im = ax.imshow(theta, cmap=cmap, origin='lower')
    ax.set_title(f"'{cmap}'")
    ax.axis('off')
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.suptitle('Cyclic Colormaps', fontsize=14)
plt.tight_layout()
plt.show()
```

### When to Use Cyclic

- Angular data (directions, phases)
- Time of day (circular)
- Hue values
- Any data that wraps around

```python
# Example: Phase angle
Z_complex = X + 1j * Y
phase = np.angle(Z_complex)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(phase, extent=[-3, 3, -3, 3], origin='lower', cmap='twilight')
ax.set_title('Complex Phase Angle')
ax.set_xlabel('Re(z)')
ax.set_ylabel('Im(z)')
plt.colorbar(im, ax=ax, label='Phase (radians)')
plt.show()
```

---

## Qualitative Colormaps

Best for categorical data with no natural ordering.

### Available Qualitative Colormaps

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

cmaps = ['Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'Paired']

# Create categorical-like data
np.random.seed(42)
Z_cat = np.random.randint(0, 8, (20, 20))

for ax, cmap in zip(axes.flat, cmaps):
    im = ax.imshow(Z_cat, cmap=cmap, origin='lower')
    ax.set_title(f"'{cmap}'")
    ax.axis('off')
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.suptitle('Qualitative Colormaps', fontsize=14)
plt.tight_layout()
plt.show()
```

### When to Use Qualitative

- Segmentation maps
- Cluster labels
- Land use categories
- Any discrete, unordered categories

```python
# Example: Cluster visualization
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

X_data, _ = make_blobs(n_samples=300, centers=4, random_state=42)
kmeans = KMeans(n_clusters=4, random_state=42).fit(X_data)

fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(X_data[:, 0], X_data[:, 1], c=kmeans.labels_, cmap='Set1')
ax.set_title('K-Means Clustering')
plt.colorbar(scatter, ax=ax, label='Cluster')
plt.show()
```

---

## Reversed Colormaps

Add `_r` suffix to reverse any colormap.

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

Z = np.exp(-(X**2 + Y**2))

pairs = [
    ('viridis', 'viridis_r'),
    ('Blues', 'Blues_r'),
    ('coolwarm', 'coolwarm_r')
]

for i, (cmap1, cmap2) in enumerate(pairs):
    im1 = axes[0, i].imshow(Z, cmap=cmap1, origin='lower')
    axes[0, i].set_title(f"'{cmap1}'")
    axes[0, i].axis('off')
    plt.colorbar(im1, ax=axes[0, i], shrink=0.8)
    
    im2 = axes[1, i].imshow(Z, cmap=cmap2, origin='lower')
    axes[1, i].set_title(f"'{cmap2}'")
    axes[1, i].axis('off')
    plt.colorbar(im2, ax=axes[1, i], shrink=0.8)

plt.suptitle('Original vs Reversed Colormaps', fontsize=14)
plt.tight_layout()
plt.show()
```

---

## Color Vision Deficiency

Consider colorblind-friendly options.

### Colorblind-Safe Colormaps

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

# Colorblind-friendly options
cmaps = ['viridis', 'plasma', 'cividis', 'inferno', 'magma', 'YlOrBr']

for ax, cmap in zip(axes.flat, cmaps):
    im = ax.imshow(Z, cmap=cmap, origin='lower')
    ax.set_title(f"'{cmap}' (colorblind-safe)")
    ax.axis('off')
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.suptitle('Colorblind-Friendly Colormaps', fontsize=14)
plt.tight_layout()
plt.show()
```

### Avoid These for Colorblind Users

- `jet` (rainbow) - poor perceptual uniformity
- `hsv` - hard to distinguish regions
- `rainbow` - misleading intensity perception

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Problematic colormaps
cmaps = ['jet', 'rainbow', 'hsv']

for ax, cmap in zip(axes, cmaps):
    im = ax.imshow(Z, cmap=cmap, origin='lower')
    ax.set_title(f"'{cmap}' (avoid for scientific use)")
    ax.axis('off')
    plt.colorbar(im, ax=ax, shrink=0.8)

plt.suptitle('Colormaps to Avoid', fontsize=14)
plt.tight_layout()
plt.show()
```

---

## Custom Colormaps

Create custom colormaps for specific needs.

### From Listed Colors

```python
from matplotlib.colors import ListedColormap

colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12']
custom_cmap = ListedColormap(colors)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(np.random.randint(0, 5, (20, 20)), cmap=custom_cmap)
ax.set_title('Custom ListedColormap')
plt.colorbar(im, ax=ax)
plt.show()
```

### Linear Segmented

```python
from matplotlib.colors import LinearSegmentedColormap

# White to blue gradient
colors = ['white', 'lightblue', 'blue', 'darkblue']
custom_cmap = LinearSegmentedColormap.from_list('custom_blues', colors, N=256)

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(Z, cmap=custom_cmap, origin='lower')
ax.set_title('Custom LinearSegmentedColormap')
plt.colorbar(im, ax=ax)
plt.show()
```

### Truncated Colormap

```python
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=256):
    new_cmap = LinearSegmentedColormap.from_list(
        f'trunc({cmap.name},{minval:.2f},{maxval:.2f})',
        cmap(np.linspace(minval, maxval, n))
    )
    return new_cmap

# Use only middle portion of viridis
cmap_full = plt.cm.viridis
cmap_trunc = truncate_colormap(cmap_full, 0.2, 0.8)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

im1 = axes[0].imshow(Z, cmap=cmap_full, origin='lower')
axes[0].set_title('Full viridis')
plt.colorbar(im1, ax=axes[0])

im2 = axes[1].imshow(Z, cmap=cmap_trunc, origin='lower')
axes[1].set_title('Truncated viridis (0.2-0.8)')
plt.colorbar(im2, ax=axes[1])

plt.tight_layout()
plt.show()
```

---

## Selection Decision Tree

```
Is your data...
│
├── Ordered/Sequential (low → high)?
│   ├── Need colorblind-safe? → viridis, cividis, plasma
│   ├── Single hue preferred? → Blues, Greens, Greys
│   └── Multi-hue preferred? → YlOrRd, YlGnBu
│
├── Diverging (center is meaningful)?
│   ├── Center at zero? → coolwarm, RdBu, seismic
│   └── Asymmetric data? → Use TwoSlopeNorm
│
├── Cyclic (wraps around)?
│   └── Use twilight or twilight_shifted
│
└── Categorical (no order)?
    ├── Few categories (<10)? → Set1, tab10
    └── Many categories? → tab20, Set3
```

---

## Quick Reference Table

| Data Type | Recommended | Avoid |
|-----------|-------------|-------|
| Density/PDF | `viridis`, `plasma` | `jet`, `rainbow` |
| Elevation | `terrain`, `gist_earth` | `hsv` |
| Temperature | `coolwarm`, `RdBu` | `jet` |
| Correlation | `RdBu`, `coolwarm` | sequential |
| Binary | `Greys`, `binary` | diverging |
| Categories | `Set1`, `tab10` | sequential |
| Phase/Angle | `twilight`, `hsv` | sequential |
| Heatmap | `viridis`, `YlOrRd` | `jet` |

---

## List All Available Colormaps

```python
import matplotlib.pyplot as plt

cmaps = plt.colormaps()
print(f"Total colormaps: {len(cmaps)}")
print("\nFirst 20:", cmaps[:20])
```

### Visual Catalog

```python
import matplotlib.pyplot as plt
import numpy as np

gradient = np.linspace(0, 1, 256).reshape(1, -1)

categories = {
    'Perceptually Uniform': ['viridis', 'plasma', 'inferno', 'magma', 'cividis'],
    'Sequential': ['Blues', 'Greens', 'Reds', 'YlOrRd', 'PuBuGn'],
    'Diverging': ['coolwarm', 'RdBu', 'seismic', 'bwr', 'RdYlBu'],
    'Cyclic': ['twilight', 'twilight_shifted', 'hsv'],
}

for category, cmap_list in categories.items():
    fig, axes = plt.subplots(len(cmap_list), 1, figsize=(8, len(cmap_list) * 0.4))
    fig.suptitle(category, fontsize=12, fontweight='bold')
    
    for ax, cmap in zip(axes, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=cmap)
        ax.set_ylabel(cmap, rotation=0, ha='right', va='center', fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    
    plt.tight_layout()
    plt.show()
```


---

## Exercises

**Exercise 1.** Write code that displays the same 8x8 random data array using four different colormaps in a 2x2 subplot grid. Add the colormap name as the title of each subplot.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.randn(8, 8)

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    cmaps = ['viridis', 'plasma', 'coolwarm', 'gray']

    for ax, cmap in zip(axes.flat, cmaps):
        im = ax.imshow(data, cmap=cmap)
        ax.set_title(f"cmap='{cmap}'")
        fig.colorbar(im, ax=ax, shrink=0.8)

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 2.** Explain the difference between sequential, diverging, and qualitative colormaps. Give one example of each and when to use it.

??? success "Solution to Exercise 2"
    - **Sequential colormaps** (e.g., `'viridis'`, `'Blues'`) map low-to-high values with a single color gradient. Use for data that goes in one direction (counts, temperatures, concentrations).
    - **Diverging colormaps** (e.g., `'coolwarm'`, `'RdBu'`) have two contrasting colors meeting at a midpoint. Use for data with a meaningful center point (e.g., deviations from zero, anomalies).
    - **Qualitative colormaps** (e.g., `'Set1'`, `'tab10'`) use distinct colors without implied ordering. Use for categorical data or distinguishing groups.

---

**Exercise 3.** Write code that creates a custom diverging colormap centered at zero using `matplotlib.colors.TwoSlopeNorm`. Apply it to data that ranges from -5 to 10.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import numpy as np

    np.random.seed(42)
    data = np.random.uniform(-5, 10, (10, 10))

    norm = mcolors.TwoSlopeNorm(vmin=-5, vcenter=0, vmax=10)

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='RdBu_r', norm=norm)
    fig.colorbar(im, ax=ax, label='Value')
    ax.set_title('Diverging Colormap Centered at Zero')
    plt.show()
    ```

---

**Exercise 4.** Create a figure showing how `vmin` and `vmax` affect the colormap mapping. Show the same data with default limits and with `vmin=-2, vmax=2`.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.randn(8, 8) * 3

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    im1 = ax1.imshow(data, cmap='RdBu')
    ax1.set_title('Default vmin/vmax')
    fig.colorbar(im1, ax=ax1)

    im2 = ax2.imshow(data, cmap='RdBu', vmin=-2, vmax=2)
    ax2.set_title('vmin=-2, vmax=2')
    fig.colorbar(im2, ax=ax2)

    plt.tight_layout()
    plt.show()
    ```
