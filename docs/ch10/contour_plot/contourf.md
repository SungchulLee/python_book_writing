# Axes Method - contourf

The `contourf` method creates filled contour plots, where regions between contour levels are filled with colors. This is in contrast to `contour` which only draws contour lines.

!!! tip "Mental Model"
    `contourf()` is `contour()` with the regions between lines filled in with color, like a heat map with smooth boundaries. It bridges the gap between contour lines (precise but sparse) and full heatmaps (dense but pixelated). Add `contour()` lines on top of `contourf()` fills for the most readable combination.

## Basic Usage

Create filled contour plots from meshgrid data.

### 1. Simple Filled Contour

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))

fig, ax = plt.subplots()
ax.contourf(X, Y, Z)
plt.show()
```

### 2. With Colorbar

```python
fig, ax = plt.subplots()
cf = ax.contourf(X, Y, Z)
plt.colorbar(cf, ax=ax)
plt.show()
```

### 3. With Labels

```python
fig, ax = plt.subplots()
cf = ax.contourf(X, Y, Z)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Gaussian: $e^{-(x^2+y^2)}$')
plt.colorbar(cf, ax=ax, label='Value')
plt.show()
```

## contour vs contourf

Compare line contours with filled contours.

### Side-by-Side Comparison

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Line contours
axes[0].contour(X, Y, Z)
axes[0].set_title('contour (lines only)')

# Filled contours
cf = axes[1].contourf(X, Y, Z)
axes[1].set_title('contourf (filled)')
plt.colorbar(cf, ax=axes[1])

plt.tight_layout()
plt.show()
```

### Combined contour and contourf

```python
fig, ax = plt.subplots(figsize=(8, 6))

# Filled contours as background
cf = ax.contourf(X, Y, Z, cmap='Blues')

# Line contours on top
cs = ax.contour(X, Y, Z, colors='black', linewidths=0.5)
ax.clabel(cs, inline=True, fontsize=8)

plt.colorbar(cf, ax=ax)
ax.set_title('Filled Contours with Line Overlay')
plt.show()
```

## Number of Levels

Control the number of contour levels.

### 1. Default Levels

```python
fig, ax = plt.subplots()
cf = ax.contourf(X, Y, Z)
ax.set_title('Default Levels')
plt.colorbar(cf, ax=ax)
plt.show()
```

### 2. Specify Number of Levels

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

levels_list = [5, 10, 20]

for ax, n in zip(axes, levels_list):
    cf = ax.contourf(X, Y, Z, levels=n)
    ax.set_title(f'levels={n}')
    plt.colorbar(cf, ax=ax)

plt.tight_layout()
plt.show()
```

### 3. Explicit Level Values

```python
fig, ax = plt.subplots()
levels = [0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]
cf = ax.contourf(X, Y, Z, levels=levels)
ax.set_title('Custom Level Values')
plt.colorbar(cf, ax=ax, ticks=levels)
plt.show()
```

### 4. Non-Uniform Levels

```python
fig, ax = plt.subplots()
# More resolution at higher values
levels = [0, 0.05, 0.1, 0.2, 0.5, 0.7, 0.9, 1.0]
cf = ax.contourf(X, Y, Z, levels=levels)
ax.set_title('Non-Uniform Levels')
plt.colorbar(cf, ax=ax)
plt.show()
```

## Colormap Options

Apply different colormaps to filled contours.

### 1. Sequential Colormaps

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

cmaps = ['viridis', 'plasma', 'inferno']

for ax, cmap in zip(axes, cmaps):
    cf = ax.contourf(X, Y, Z, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")
    plt.colorbar(cf, ax=ax)

plt.tight_layout()
plt.show()
```

### 2. Diverging Colormaps

```python
Z_div = np.sin(X) * np.cos(Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

cmaps = ['coolwarm', 'RdBu', 'seismic']

for ax, cmap in zip(axes, cmaps):
    cf = ax.contourf(X, Y, Z_div, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")
    plt.colorbar(cf, ax=ax)

plt.tight_layout()
plt.show()
```

### 3. Perceptually Uniform

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

cmaps = ['cividis', 'magma', 'YlOrRd']

for ax, cmap in zip(axes, cmaps):
    cf = ax.contourf(X, Y, Z, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")
    plt.colorbar(cf, ax=ax)

plt.tight_layout()
plt.show()
```

## Alpha Transparency

Control the transparency of filled regions.

### 1. Opaque Fill

```python
fig, ax = plt.subplots()
cf = ax.contourf(X, Y, Z, alpha=1.0)
ax.set_title('alpha=1.0 (opaque)')
plt.colorbar(cf, ax=ax)
plt.show()
```

### 2. Semi-Transparent Fill

```python
fig, ax = plt.subplots()
cf = ax.contourf(X, Y, Z, alpha=0.7)
ax.set_title('alpha=0.7')
plt.colorbar(cf, ax=ax)
plt.show()
```

### 3. Alpha Comparison

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

alphas = [1.0, 0.6, 0.3]

for ax, alpha in zip(axes, alphas):
    cf = ax.contourf(X, Y, Z, alpha=alpha)
    ax.set_title(f'alpha={alpha}')
    plt.colorbar(cf, ax=ax)

plt.tight_layout()
plt.show()
```

## Extend Option

Handle values outside the specified level range.

### 1. extend='neither'

```python
fig, ax = plt.subplots()
levels = [0.2, 0.4, 0.6, 0.8]
cf = ax.contourf(X, Y, Z, levels=levels, extend='neither')
ax.set_title("extend='neither'")
plt.colorbar(cf, ax=ax)
plt.show()
```

### 2. extend='both'

```python
fig, ax = plt.subplots()
cf = ax.contourf(X, Y, Z, levels=levels, extend='both')
ax.set_title("extend='both'")
plt.colorbar(cf, ax=ax)
plt.show()
```

### 3. Extend Comparison

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

extends = ['neither', 'min', 'max', 'both']
levels = [0.2, 0.4, 0.6, 0.8]

for ax, extend in zip(axes.flat, extends):
    cf = ax.contourf(X, Y, Z, levels=levels, extend=extend)
    ax.set_title(f"extend='{extend}'")
    plt.colorbar(cf, ax=ax)

plt.tight_layout()
plt.show()
```

## Mathematical Functions

Visualize various mathematical functions.

### 1. Bivariate Normal PDF

```python
def bivariate_normal(X, Y, mu_x=0, mu_y=0, sigma_x=1, sigma_y=1, rho=0):
    z = ((X - mu_x) / sigma_x)**2 - 2 * rho * (X - mu_x) * (Y - mu_y) / (sigma_x * sigma_y) + ((Y - mu_y) / sigma_y)**2
    return np.exp(-z / (2 * (1 - rho**2))) / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - rho**2))

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = bivariate_normal(X, Y, rho=0.5)

fig, ax = plt.subplots(figsize=(8, 6))
cf = ax.contourf(X, Y, Z, levels=20, cmap='Blues')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Bivariate Normal (ρ=0.5)')
ax.set_aspect('equal')
plt.colorbar(cf, ax=ax, label='Density')
plt.show()
```

### 2. Saddle Function

```python
Z = X**2 - Y**2

fig, ax = plt.subplots(figsize=(8, 6))
cf = ax.contourf(X, Y, Z, levels=20, cmap='coolwarm')
cs = ax.contour(X, Y, Z, levels=20, colors='black', linewidths=0.3)
ax.set_title('Saddle: $z = x^2 - y^2$')
ax.set_aspect('equal')
plt.colorbar(cf, ax=ax)
plt.show()
```

### 3. Sinusoidal Surface

```python
Z = np.sin(X) * np.cos(Y)

fig, ax = plt.subplots(figsize=(8, 6))
cf = ax.contourf(X, Y, Z, levels=20, cmap='RdBu')
ax.set_title('$z = \\sin(x)\\cos(y)$')
ax.set_aspect('equal')
plt.colorbar(cf, ax=ax)
plt.show()
```

### 4. Function Gallery

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

functions = [
    (np.exp(-(X**2 + Y**2)), 'Gaussian', 'viridis'),
    (X**2 - Y**2, 'Saddle', 'coolwarm'),
    (np.sin(X) * np.cos(Y), 'sin(x)cos(y)', 'RdBu'),
    (np.sin(np.sqrt(X**2 + Y**2)), 'Ripple', 'plasma')
]

for ax, (Z, title, cmap) in zip(axes.flat, functions):
    cf = ax.contourf(X, Y, Z, levels=15, cmap=cmap)
    ax.set_title(title)
    ax.set_aspect('equal')
    plt.colorbar(cf, ax=ax)

plt.tight_layout()
plt.show()
```

## Correlation Comparison

Visualize bivariate normal distributions with different correlations.

```python
from scipy import stats

rhos = [-0.8, 0, 0.8]

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))

for ax, rho in zip(axes, rhos):
    rv = stats.multivariate_normal([0, 0], [[1, rho], [rho, 1]])
    Z = rv.pdf(pos)
    cf = ax.contourf(X, Y, Z, levels=15, cmap='Blues')
    ax.set_title(f'ρ = {rho}')
    ax.set_aspect('equal')
    plt.colorbar(cf, ax=ax)

plt.tight_layout()
plt.show()
```

## Hatching Patterns

Add hatching patterns to filled regions.

### 1. Basic Hatching

```python
fig, ax = plt.subplots()
cf = ax.contourf(X, Y, Z, levels=5, hatches=['', '/', '\\', '//', '\\\\'])
ax.set_title('Contourf with Hatching')
plt.colorbar(cf, ax=ax)
plt.show()
```

### 2. Hatching Styles

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

hatch_patterns = [
    ['', '/', '//', '///', '////'],
    ['', '.', '..', 'o', 'O'],
    ['', '-', '--', '+', 'x']
]

for ax, hatches in zip(axes, hatch_patterns):
    cf = ax.contourf(X, Y, Z, levels=5, hatches=hatches, cmap='Greys', alpha=0.5)
    ax.set_title(f'hatches={hatches}')

plt.tight_layout()
plt.show()
```

## Colorbar Customization

### 1. Horizontal Colorbar

```python
fig, ax = plt.subplots()
cf = ax.contourf(X, Y, Z, levels=10, cmap='viridis')
plt.colorbar(cf, ax=ax, orientation='horizontal', label='Value')
plt.show()
```

### 2. Custom Ticks

```python
fig, ax = plt.subplots()
levels = np.linspace(0, 1, 11)
cf = ax.contourf(X, Y, Z, levels=levels, cmap='viridis')
cbar = plt.colorbar(cf, ax=ax, ticks=[0, 0.25, 0.5, 0.75, 1.0])
cbar.set_label('Intensity')
plt.show()
```

### 3. Discrete Colorbar

```python
fig, ax = plt.subplots()
levels = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
cf = ax.contourf(X, Y, Z, levels=levels, cmap='RdYlGn')
cbar = plt.colorbar(cf, ax=ax, ticks=levels)
cbar.set_ticklabels(['Very Low', 'Low', 'Medium', 'High', 'Very High', ''])
plt.show()
```

## Full Customization

### 1. Complete Example

```python
x = np.linspace(-4, 4, 150)
y = np.linspace(-4, 4, 150)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2) / 2) / (2 * np.pi)

fig, ax = plt.subplots(figsize=(9, 7))

cf = ax.contourf(X, Y, Z, levels=20, cmap='Blues')
cs = ax.contour(X, Y, Z, levels=10, colors='navy', linewidths=0.5, alpha=0.7)
ax.clabel(cs, inline=True, fontsize=8, fmt='%.3f')

ax.set_xlabel('$x$', fontsize=12)
ax.set_ylabel('$y$', fontsize=12)
ax.set_title('Standard Bivariate Normal PDF', fontsize=14)
ax.set_aspect('equal')

cbar = plt.colorbar(cf, ax=ax)
cbar.set_label('Probability Density', fontsize=11)

plt.tight_layout()
plt.show()
```

### 2. Publication-Quality Figure

```python
from scipy import stats

x = np.linspace(-3, 3, 150)
y = np.linspace(-3, 3, 150)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))

rv = stats.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]])
Z = rv.pdf(pos)

fig, ax = plt.subplots(figsize=(9, 7))

cf = ax.contourf(X, Y, Z, levels=15, cmap='viridis')
cs = ax.contour(X, Y, Z, levels=8, colors='white', linewidths=0.5, alpha=0.8)

ax.set_xlabel('$X$', fontsize=13)
ax.set_ylabel('$Y$', fontsize=13)
ax.set_title('Bivariate Normal Distribution ($\\rho = 0.6$)', fontsize=14, fontweight='bold')
ax.set_aspect('equal')
ax.tick_params(labelsize=11)

cbar = plt.colorbar(cf, ax=ax, shrink=0.85)
cbar.set_label('Probability Density', fontsize=12)

plt.tight_layout()
plt.show()
```

## Practical Applications

### 1. Terrain Map

```python
np.random.seed(42)
from scipy.ndimage import gaussian_filter

# Generate terrain-like data
Z_terrain = np.random.rand(100, 100)
Z_terrain = gaussian_filter(Z_terrain, sigma=10) * 1000

x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)

fig, ax = plt.subplots(figsize=(10, 8))
cf = ax.contourf(X, Y, Z_terrain, levels=20, cmap='terrain')
cs = ax.contour(X, Y, Z_terrain, levels=10, colors='black', linewidths=0.3)
ax.clabel(cs, inline=True, fontsize=7, fmt='%.0f m')
ax.set_title('Topographic Map')
ax.set_xlabel('Distance (km)')
ax.set_ylabel('Distance (km)')
plt.colorbar(cf, ax=ax, label='Elevation (m)')
plt.show()
```

### 2. Temperature Field

```python
# Simulated temperature field
Z_temp = 20 + 10 * np.exp(-((X - 1)**2 + Y**2) / 2) - 5 * np.exp(-((X + 1)**2 + (Y - 1)**2) / 1)

fig, ax = plt.subplots(figsize=(10, 8))
cf = ax.contourf(X, Y, Z_temp, levels=20, cmap='coolwarm')
cs = ax.contour(X, Y, Z_temp, levels=10, colors='black', linewidths=0.3)
ax.clabel(cs, inline=True, fontsize=8, fmt='%.1f°C')
ax.set_title('Temperature Distribution')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.colorbar(cf, ax=ax, label='Temperature (°C)')
plt.show()
```

!!! info "In Machine Learning"

    Filled contour plots are the standard way to visualize **decision boundaries** in classification. Train a classifier on 2D features, evaluate it on a meshgrid, and `contourf` the predictions — each colored region shows where the model assigns a different class. Overlaying the training points as a scatter plot reveals how well the boundary fits the data.

---

## Exercises

**Exercise 1.**
Create a filled contour plot of the Rosenbrock function $z = (1 - x)^2 + 100(y - x^2)^2$ over $[-2, 2] \times [-1, 3]$. Use `np.log10` of the values for better visualization (since the range is huge). Use 20 levels and the `hot` colormap. Add a colorbar with label "log10(z)".

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-2, 2, 300)
        y = np.linspace(-1, 3, 300)
        X, Y = np.meshgrid(x, y)
        Z = (1 - X)**2 + 100 * (Y - X**2)**2
        Z_log = np.log10(Z + 1)

        fig, ax = plt.subplots(figsize=(8, 6))
        cf = ax.contourf(X, Y, Z_log, levels=20, cmap='hot')
        plt.colorbar(cf, ax=ax, label='log10(z)')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Rosenbrock Function (log scale)')
        plt.show()

---

**Exercise 2.**
Compare `contour` and `contourf` side by side for the function $z = \sin(x^2 + y^2)$ over $[-3, 3] \times [-3, 3]$. Create a 1x2 subplot layout with contour lines on the left (with labels) and filled contour on the right. Use the same 15 levels and `coolwarm` colormap for both.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 200)
        y = np.linspace(-3, 3, 200)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X**2 + Y**2)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        cs = ax1.contour(X, Y, Z, levels=15, cmap='coolwarm')
        ax1.clabel(cs, inline=True, fontsize=8)
        ax1.set_title('contour (lines)')
        ax1.set_aspect('equal')

        cf = ax2.contourf(X, Y, Z, levels=15, cmap='coolwarm')
        plt.colorbar(cf, ax=ax2)
        ax2.set_title('contourf (filled)')
        ax2.set_aspect('equal')

        plt.tight_layout()
        plt.show()

---

**Exercise 3.**
Create a filled contour plot with a custom discrete colormap using `BoundaryNorm`. Plot $z = x^2 + y^2$ over $[-3, 3] \times [-3, 3]$ with boundaries at `[0, 2, 4, 6, 8, 10, 15, 20]`. Use the `RdYlGn_r` colormap and add a colorbar showing the discrete boundaries.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.colors import BoundaryNorm

        x = np.linspace(-3, 3, 200)
        y = np.linspace(-3, 3, 200)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2

        bounds = [0, 2, 4, 6, 8, 10, 15, 20]
        cmap = plt.cm.RdYlGn_r
        norm = BoundaryNorm(bounds, cmap.N)

        fig, ax = plt.subplots(figsize=(8, 6))
        cf = ax.contourf(X, Y, Z, levels=bounds, cmap=cmap, norm=norm)
        plt.colorbar(cf, ax=ax, label='Value', ticks=bounds)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(r'$z = x^2 + y^2$ with Discrete Colormap')
        ax.set_aspect('equal')
        plt.show()
