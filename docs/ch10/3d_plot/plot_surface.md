# Axes Method - plot_surface

The `plot_surface` method creates a 3D surface plot from grid data. It requires 2D arrays for X, Y coordinates and corresponding Z values.

!!! tip "Mental Model"
    `plot_surface(X, Y, Z)` renders a 3D terrain from three 2D arrays: X and Y define a coordinate grid (built with `np.meshgrid`), and Z holds the height at each grid point. Think of it as draping a colored sheet over a landscape. Use `cmap` to color the surface by height and `view_init` to rotate the camera for the best viewing angle.

## Understanding meshgrid

Before using `plot_surface`, understand how `np.meshgrid` creates coordinate grids.

### 1. Basic meshgrid

```python
import numpy as np

x = np.array([0, 1, 2])      # (3,)
y = np.array([-2, -1, 0, 1, 2])  # (5,)
X, Y = np.meshgrid(x, y)
print(X)  # (5, 3)
print(Y)  # (5, 3)
```

Output:
```
X:
[[0 1 2]
 [0 1 2]
 [0 1 2]
 [0 1 2]
 [0 1 2]]

Y:
[[-2 -2 -2]
 [-1 -1 -1]
 [ 0  0  0]
 [ 1  1  1]
 [ 2  2  2]]
```

### 2. meshgrid for Surface Plots

```python
import numpy as np

n = 40
x = np.linspace(-3.0, 3.0, n)  # (40,)
y = np.linspace(-3.0, 3.0, n)  # (40,)
X, Y = np.meshgrid(x, y)       # (40, 40), (40, 40)
```

## Basic Usage

Create 3D surface plots with the `projection='3d'` subplot keyword.

### 1. Simple Surface

```python
import matplotlib.pyplot as plt
import numpy as np

def f(X, Y):
    return X**2 + Y**2

x = np.linspace(-2, 2, 30)
y = np.linspace(-2, 2, 30)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z)
plt.show()
```

### 2. With Colormap

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
plt.show()
```

### 3. With Labels

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()
```

## Standard Normal PDF

Plot the standard bivariate normal probability density function.

### 1. Basic Normal PDF

```python
import matplotlib.pyplot as plt
import numpy as np

def f(X, Y):
    return np.exp(-X**2 / 2 - Y**2 / 2) / (2 * np.pi)

x = np.linspace(-4, 4, 100)
y = np.linspace(-4, 4, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, ax = plt.subplots(figsize=(8, 6), subplot_kw={'projection': '3d'})
ax.set_title("Standard Normal PDF", fontsize=15)
ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
plt.show()
```

### 2. With Custom Z-ticks

```python
fig, ax = plt.subplots(figsize=(5 * 1.61803398875, 5), subplot_kw={'projection': '3d'})
ax.set_title("Standard Normal PDF", fontsize=15)
ax.plot_surface(
    X, Y, Z,
    rstride=2,
    cstride=2,
    cmap=plt.cm.coolwarm,
    linewidth=0.5,
    antialiased=True
)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
ax.set_zticks((0.05, 0.10, 0.15))
plt.show()
```

## Multivariate Normal with Correlation

Plot bivariate normal distributions with different correlation coefficients.

### 1. Setup Function

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def create_bivariate_normal(mu_1, mu_2, sigma_1, sigma_2, rho):
    return stats.multivariate_normal(
        [mu_1, mu_2],
        [[sigma_1, rho * sigma_1 * sigma_2],
         [rho * sigma_1 * sigma_2, sigma_2]]
    )
```

### 2. Single Correlation

```python
n = 40
mu_1, mu_2 = 0, 0
sigma_1, sigma_2 = 1, 0.5
rho = 0.0

x = np.linspace(-3.0, 3.0, n)
y = np.linspace(-3.0, 3.0, n)
X, Y = np.meshgrid(x, y)
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X
pos[:, :, 1] = Y

Z = create_bivariate_normal(mu_1, mu_2, sigma_1, sigma_2, rho)

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z.pdf(pos), cmap='viridis', linewidth=0)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
plt.show()
```

### 3. Comparing Correlations

```python
n = 40
mu_1, mu_2 = 0, 0
sigma_1, sigma_2 = 1, 0.5
rho1, rho2, rho3 = 0.0, -0.8, 0.8

x = np.linspace(-3.0, 3.0, n)
y = np.linspace(-3.0, 3.0, n)
X, Y = np.meshgrid(x, y)
pos = np.empty(X.shape + (2,))
pos[:, :, 0] = X
pos[:, :, 1] = Y

Z = lambda rho: stats.multivariate_normal(
    [mu_1, mu_2],
    [[sigma_1, rho * sigma_1 * sigma_2],
     [rho * sigma_1 * sigma_2, sigma_2]]
)

fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

ax0.plot_surface(X, Y, Z(rho1).pdf(pos), cmap='Oranges', linewidth=0)
ax0.set_xlabel('X axis')
ax0.set_ylabel('Y axis')
ax0.set_title(f'ρ = {rho1}')

ax1.plot_surface(X, Y, Z(rho2).pdf(pos), cmap='viridis', linewidth=0)
ax1.set_xlabel('X axis')
ax1.set_ylabel('Y axis')
ax1.set_title(f'ρ = {rho2}')

ax2.plot_surface(X, Y, Z(rho3).pdf(pos), cmap='PuBuGn', linewidth=0)
ax2.set_xlabel('X axis')
ax2.set_ylabel('Y axis')
ax2.set_title(f'ρ = {rho3}')

plt.tight_layout()
plt.show()
```

## Noisy Surface

Add random noise to surface data.

### 1. Noisy Bowl

```python
import matplotlib.pyplot as plt
import numpy as np

def f(X, Y, seed=0):
    np.random.seed(seed)
    return X**2 + Y**2 + 0.15 * np.random.normal(0., 1., X.shape)

x = np.linspace(-1.5, 1.5, 80)
y = np.linspace(-1.5, 1.5, 80)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, ax = plt.subplots(figsize=(9, 6), subplot_kw={'projection': '3d'})
ax.plot_surface(
    X, Y, Z,
    rstride=2,
    cstride=2,
    cmap=plt.cm.coolwarm,
    linewidth=0.5,
    antialiased=True
)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('f(x, y)')
plt.show()
```

### 2. Noise Level Comparison

```python
def f_noisy(X, Y, noise_level, seed=0):
    np.random.seed(seed)
    return X**2 + Y**2 + noise_level * np.random.normal(0., 1., X.shape)

x = np.linspace(-1.5, 1.5, 50)
y = np.linspace(-1.5, 1.5, 50)
X, Y = np.meshgrid(x, y)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

noise_levels = [0.0, 0.15, 0.5]
titles = ['No Noise', 'Low Noise', 'High Noise']

for ax, noise, title in zip(axes, noise_levels, titles):
    Z = f_noisy(X, Y, noise)
    ax.plot_surface(X, Y, Z, cmap=plt.cm.coolwarm, linewidth=0.5)
    ax.set_title(title)
    ax.set_xlabel('x')
    ax.set_ylabel('y')

plt.tight_layout()
plt.show()
```

## Stride Parameters

Control surface mesh density with `rstride` and `cstride`.

### 1. Default Stride

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
plt.show()
```

### 2. Custom Stride

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, rstride=2, cstride=2, cmap='viridis')
plt.show()
```

### 3. Stride Comparison

```python
x = np.linspace(-2, 2, 60)
y = np.linspace(-2, 2, 60)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

strides = [1, 3, 6]

for ax, s in zip(axes, strides):
    ax.plot_surface(X, Y, Z, rstride=s, cstride=s, cmap='viridis')
    ax.set_title(f'rstride={s}, cstride={s}')

plt.tight_layout()
plt.show()
```

## Colormap Options

Different colormaps for surface visualization.

### 1. Sequential Colormaps

```python
x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

cmaps = ['viridis', 'plasma', 'inferno']

for ax, cmap in zip(axes, cmaps):
    ax.plot_surface(X, Y, Z, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")

plt.tight_layout()
plt.show()
```

### 2. Diverging Colormaps

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

cmaps = ['coolwarm', 'RdBu', 'seismic']

for ax, cmap in zip(axes, cmaps):
    ax.plot_surface(X, Y, Z, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")

plt.tight_layout()
plt.show()
```

### 3. Qualitative Colormaps

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

cmaps = ['Oranges', 'PuBuGn', 'YlOrRd']

for ax, cmap in zip(axes, cmaps):
    ax.plot_surface(X, Y, Z, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")

plt.tight_layout()
plt.show()
```

## Linewidth and Antialiasing

Control edge appearance.

### 1. No Edge Lines

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0)
plt.show()
```

### 2. Visible Edge Lines

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0.5)
plt.show()
```

### 3. Antialiasing Comparison

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={'projection': '3d'})

axes[0].plot_surface(X, Y, Z, cmap='viridis', linewidth=0.5, antialiased=False)
axes[0].set_title('antialiased=False')

axes[1].plot_surface(X, Y, Z, cmap='viridis', linewidth=0.5, antialiased=True)
axes[1].set_title('antialiased=True')

plt.tight_layout()
plt.show()
```

## Alpha Transparency

Control surface transparency.

### 1. Opaque Surface

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=1.0)
plt.show()
```

### 2. Semi-transparent Surface

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
plt.show()
```

### 3. Alpha Comparison

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

alphas = [1.0, 0.7, 0.4]

for ax, a in zip(axes, alphas):
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=a)
    ax.set_title(f'alpha={a}')

plt.tight_layout()
plt.show()
```

## Common Mathematical Surfaces

### 1. Paraboloid

```python
x = np.linspace(-2, 2, 50)
y = np.linspace(-2, 2, 50)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.set_title('Paraboloid: $z = x^2 + y^2$')
plt.show()
```

### 2. Saddle Point

```python
Z = X**2 - Y**2

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='coolwarm')
ax.set_title('Saddle: $z = x^2 - y^2$')
plt.show()
```

### 3. Sinusoidal Surface

```python
Z = np.sin(np.sqrt(X**2 + Y**2))

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='plasma')
ax.set_title('Sinusoidal: $z = sin(\\sqrt{x^2 + y^2})$')
plt.show()
```

### 4. Surface Gallery

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10), subplot_kw={'projection': '3d'})

# Paraboloid
axes[0, 0].plot_surface(X, Y, X**2 + Y**2, cmap='viridis')
axes[0, 0].set_title('Paraboloid')

# Saddle
axes[0, 1].plot_surface(X, Y, X**2 - Y**2, cmap='coolwarm')
axes[0, 1].set_title('Saddle')

# Sinusoidal
axes[1, 0].plot_surface(X, Y, np.sin(X) * np.cos(Y), cmap='plasma')
axes[1, 0].set_title('sin(x)cos(y)')

# Gaussian
axes[1, 1].plot_surface(X, Y, np.exp(-(X**2 + Y**2)), cmap='inferno')
axes[1, 1].set_title('Gaussian')

plt.tight_layout()
plt.show()
```

## Full Customization

### 1. Complete Example

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 80)
y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2) / 2) / (2 * np.pi)

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
surf = ax.plot_surface(
    X, Y, Z,
    rstride=2,
    cstride=2,
    cmap=plt.cm.coolwarm,
    linewidth=0.3,
    antialiased=True,
    alpha=0.9
)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Bivariate Normal Distribution', fontsize=14)
fig.colorbar(surf, shrink=0.5, aspect=10)
plt.show()
```

### 2. Professional Presentation

```python
from scipy import stats

n = 50
x = np.linspace(-3, 3, n)
y = np.linspace(-3, 3, n)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))

rv = stats.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]])
Z = rv.pdf(pos)

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
surf = ax.plot_surface(
    X, Y, Z,
    cmap='viridis',
    linewidth=0,
    antialiased=True
)
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Density', fontsize=12)
ax.set_title('Bivariate Normal (ρ = 0.5)', fontsize=14, fontweight='bold')
fig.colorbar(surf, shrink=0.6, aspect=15, label='Probability Density')
plt.tight_layout()
plt.show()
```

!!! info "In Machine Learning"

    Surface plots visualize **loss landscapes** — plot the loss function over two weight dimensions to see minima, saddle points, and the terrain that gradient descent navigates. This is a key tool for understanding optimization behavior, especially when comparing different architectures or learning rates.

## Choosing the Right 3D Representation

| Data type | Method | When to use |
|---|---|---|
| 1D parametric: x(t), y(t), z(t) | `ax.plot(x, y, z)` | Trajectories, helices, orbits |
| 2D scalar field: z = f(x, y) | `ax.plot_surface(X, Y, Z)` | Landscapes, PDFs, potential fields |
| Complex function: f(t) = u(t) + iv(t) | `ax.plot(t, Re, Im)` | Characteristic functions, Euler's formula |
| Contour projection | `ax.contour(X, Y, Z)` | Isolines, level sets |

Use parametric curves when data flows along a single parameter; use surfaces when data covers a 2D domain.

---

## Exercises

**Exercise 1.**
Create a 3D surface plot of the function $z = \cos(x) \cdot \sin(y)$ over the domain $[-\pi, \pi] \times [-\pi, \pi]$ using `meshgrid`. Apply the `coolwarm` colormap, add a colorbar with label "Value", and set axis labels.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-np.pi, np.pi, 100)
        y = np.linspace(-np.pi, np.pi, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.cos(X) * np.sin(Y)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='coolwarm')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(r'$z = \cos(x) \cdot \sin(y)$')
        fig.colorbar(surf, shrink=0.6, label='Value')
        plt.show()

---

**Exercise 2.**
Plot two surfaces on the same 3D axes: $z_1 = x^2 + y^2$ (a paraboloid) and $z_2 = 8 - x^2 - y^2$ (an inverted paraboloid) over $[-2, 2] \times [-2, 2]$. Use different colormaps for each surface and set `alpha=0.7` so both are visible. Add a title describing the intersection.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-2, 2, 100)
        y = np.linspace(-2, 2, 100)
        X, Y = np.meshgrid(x, y)
        Z1 = X**2 + Y**2
        Z2 = 8 - X**2 - Y**2

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(X, Y, Z1, cmap='viridis', alpha=0.7)
        ax.plot_surface(X, Y, Z2, cmap='plasma', alpha=0.7)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Paraboloid and Inverted Paraboloid')
        plt.show()

---

**Exercise 3.**
Create a surface plot of the 2D Gaussian $z = e^{-(x^2 + y^2)}$ over $[-3, 3] \times [-3, 3]$. Customize the plot with `rstride=2`, `cstride=2`, `edgecolor='black'`, `linewidth=0.3`, and the `viridis` colormap. Add a colorbar and adjust the view angle to `elev=35, azim=225`.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 + Y**2))

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', rstride=2, cstride=2,
                               edgecolor='black', linewidth=0.3)
        ax.view_init(elev=35, azim=225)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(r'$z = e^{-(x^2 + y^2)}$')
        fig.colorbar(surf, shrink=0.6)
        plt.show()
