# Axes Method - contour

The `ax.contour()` method draws contour lines for scalar fields.

!!! tip "Mental Model"
    `contour()` draws lines of constant value through a 2D scalar field, like elevation contours on a topographic map. You provide X, Y grids and a Z value at each point; Matplotlib interpolates to find where Z equals each contour level. Close-together lines mean steep gradients; widely spaced lines mean flat regions.

!!! note "Contour = Horizontal Slice of a Surface"
    A contour line at level $c$ is the set of all points where $f(x, y) = c$ — geometrically, it is a **horizontal slice** through the 3D surface $z = f(x, y)$. This is the bridge between 2D and 3D: every contour plot is a top-down view of level slices through the surface. The **spacing** between contour lines encodes the gradient: closely spaced lines mean the function is changing rapidly (steep slope), widely spaced lines mean it is nearly flat.

[Official Documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.contour.html)

## Basic Usage

### Simple Contour Plot

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
    x = np.linspace(0, 5, 50)
    y = np.linspace(0, 5, 40)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.contour(X, Y, Z, levels=3, colors='black')
    plt.show()

if __name__ == "__main__":
    main()
```

## Creating Meshgrid

### Understanding np.meshgrid

```python
import numpy as np

x = np.linspace(0, 5, 50)  # 50 points from 0 to 5
y = np.linspace(0, 5, 40)  # 40 points from 0 to 5
X, Y = np.meshgrid(x, y)

print(f"x shape: {x.shape}")      # (50,)
print(f"y shape: {y.shape}")      # (40,)
print(f"X shape: {X.shape}")      # (40, 50)
print(f"Y shape: {Y.shape}")      # (40, 50)
```

### Computing Z Values

```python
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

print(f"Z shape: {Z.shape}")      # (40, 50)
print(f"Z min: {Z.min():.3f}")
print(f"Z max: {Z.max():.3f}")
```

## Levels Parameter

### Number of Levels

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
level_counts = [3, 7, 15, 30]

for ax, n_levels in zip(axes, level_counts):
    ax.contour(X, Y, Z, levels=n_levels, colors='black')
    ax.set_title(f'levels={n_levels}')
    ax.set_aspect('equal')

plt.tight_layout()
plt.show()
```

### Specific Level Values

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Evenly spaced levels
axes[0].contour(X, Y, Z, levels=np.linspace(-1, 1, 11), colors='black')
axes[0].set_title('levels=np.linspace(-1, 1, 11)')

# Custom specific levels
axes[1].contour(X, Y, Z, levels=[-0.5, 0, 0.5], colors='black')
axes[1].set_title('levels=[-0.5, 0, 0.5]')

for ax in axes:
    ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

## Colors and Colormaps

### Single Color

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
colors_list = ['black', 'blue', 'red']

for ax, color in zip(axes, colors_list):
    ax.contour(X, Y, Z, levels=10, colors=color)
    ax.set_title(f"colors='{color}'")
    ax.set_aspect('equal')

plt.tight_layout()
plt.show()
```

### Using Colormaps

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
cmaps = ['viridis', 'plasma', 'coolwarm']

for ax, cmap in zip(axes, cmaps):
    cs = ax.contour(X, Y, Z, levels=15, cmap=cmap)
    ax.set_title(f"cmap='{cmap}'")
    ax.set_aspect('equal')
    fig.colorbar(cs, ax=ax, shrink=0.8)

plt.tight_layout()
plt.show()
```

## Line Styles

### Linewidths

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
linewidths = [0.5, 1.5, 3]

for ax, lw in zip(axes, linewidths):
    ax.contour(X, Y, Z, levels=10, colors='black', linewidths=lw)
    ax.set_title(f'linewidths={lw}')
    ax.set_aspect('equal')

plt.tight_layout()
plt.show()
```

### Linestyles

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
linestyles = ['solid', 'dashed', 'dotted']

for ax, ls in zip(axes, linestyles):
    ax.contour(X, Y, Z, levels=10, colors='black', linestyles=ls)
    ax.set_title(f"linestyles='{ls}'")
    ax.set_aspect('equal')

plt.tight_layout()
plt.show()
```

## Filled Contours

### contourf

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Line contour
axes[0].contour(X, Y, Z, levels=15, cmap='viridis')
axes[0].set_title('contour (lines)')

# Filled contour
cs = axes[1].contourf(X, Y, Z, levels=15, cmap='viridis')
axes[1].set_title('contourf (filled)')
fig.colorbar(cs, ax=axes[1], shrink=0.8)

for ax in axes:
    ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

### Combined Lines and Fill

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, ax = plt.subplots(figsize=(10, 6))

# Filled contours
cf = ax.contourf(X, Y, Z, levels=15, cmap='viridis', alpha=0.8)

# Line contours on top
cs = ax.contour(X, Y, Z, levels=15, colors='black', linewidths=0.5)

fig.colorbar(cf, ax=ax)
ax.set_title('Filled Contours with Lines')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

## Common Functions

### Circle/Ellipse

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2  # Circle

fig, ax = plt.subplots(figsize=(6, 6))
cs = ax.contour(X, Y, Z, levels=[1, 2, 4, 6, 8], colors='black')
ax.clabel(cs, inline=True, fontsize=10)
ax.set_title('Circles: $x^2 + y^2 = c$')
ax.set_aspect('equal')
plt.show()
```

### Saddle Point

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 - Y**2  # Hyperbolic paraboloid

fig, ax = plt.subplots(figsize=(8, 6))
cs = ax.contour(X, Y, Z, levels=15, cmap='RdBu')
fig.colorbar(cs, ax=ax)
ax.set_title('Saddle: $z = x^2 - y^2$')
ax.set_aspect('equal')
plt.show()
```

### Gaussian

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))  # Gaussian

fig, ax = plt.subplots(figsize=(8, 6))
cs = ax.contourf(X, Y, Z, levels=20, cmap='hot')
ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5)
fig.colorbar(cs, ax=ax)
ax.set_title('Gaussian: $z = e^{-(x^2 + y^2)}$')
ax.set_aspect('equal')
plt.show()
```

## Practical Example

### Topographic Map Style

```python
import matplotlib.pyplot as plt
import numpy as np

# Create terrain-like surface
np.random.seed(42)
x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)

Z = (np.sin(X) * np.cos(Y) + 
     0.5 * np.sin(2*X) * np.cos(2*Y) +
     0.25 * np.sin(4*X) * np.cos(4*Y))

fig, ax = plt.subplots(figsize=(10, 8))

# Filled contours for elevation colors
cf = ax.contourf(X, Y, Z, levels=20, cmap='terrain')

# Contour lines
cs = ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5)
ax.clabel(cs, inline=True, fontsize=8, fmt='%.1f')

fig.colorbar(cf, ax=ax, label='Elevation')
ax.set_title('Topographic Contour Map')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

## Reading Contour Shapes

Contours reveal the **geometry** of a function. Learn to recognize common patterns:

| Contour shape | What it means | Example function |
|---|---|---|
| Concentric circles | Radial symmetry | Gaussian, $x^2 + y^2$ |
| Ellipses | Stretched/scaled axes | $ax^2 + by^2$ |
| Hyperbolas (X-shaped) | Saddle point | $x^2 - y^2$ |
| Parallel lines | Linear function | $ax + by$ |
| Wavy lines | Sinusoidal behavior | $\sin(x) + \cos(y)$ |

Close contour lines = steep gradient. Wide spacing = flat region. This is why contour plots are sometimes called "topographic maps" of functions.

---

## Exercises

**Exercise 1.**
Create contour plots of $z = \sin(x) + \cos(y)$ over $[-2\pi, 2\pi] \times [-2\pi, 2\pi]$ with 15 levels. Use the `coolwarm` colormap and add a colorbar. Set equal aspect ratio.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-2 * np.pi, 2 * np.pi, 200)
        y = np.linspace(-2 * np.pi, 2 * np.pi, 200)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) + np.cos(Y)

        fig, ax = plt.subplots(figsize=(8, 6))
        cs = ax.contour(X, Y, Z, levels=15, cmap='coolwarm')
        plt.colorbar(cs, ax=ax)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(r'$z = \sin(x) + \cos(y)$')
        ax.set_aspect('equal')
        plt.show()

---

**Exercise 2.**
Plot contour lines for the function $z = x \cdot e^{-x^2 - y^2}$ over $[-2, 2] \times [-2, 2]$ using both positive and negative levels. Use solid lines for positive contours and dashed lines for negative contours by plotting two separate `contour` calls with different `linestyles`.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-2, 2, 200)
        y = np.linspace(-2, 2, 200)
        X, Y = np.meshgrid(x, y)
        Z = X * np.exp(-X**2 - Y**2)

        fig, ax = plt.subplots(figsize=(8, 6))

        pos_levels = np.linspace(0.01, Z.max(), 8)
        neg_levels = np.linspace(Z.min(), -0.01, 8)

        ax.contour(X, Y, Z, levels=pos_levels, colors='blue', linestyles='solid')
        ax.contour(X, Y, Z, levels=neg_levels, colors='red', linestyles='dashed')
        ax.contour(X, Y, Z, levels=[0], colors='black', linewidths=2)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(r'$z = x \cdot e^{-x^2 - y^2}$')
        ax.set_aspect('equal')
        plt.show()

---

**Exercise 3.**
Overlay contour lines on a scatter plot. Generate 500 random (x, y) points from a bivariate normal distribution and plot them as a scatter. Then compute the theoretical density on a grid using `scipy.stats.multivariate_normal` and overlay contour lines showing the density levels.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.stats import multivariate_normal

        np.random.seed(42)
        mean = [0, 0]
        cov = [[1, 0.5], [0.5, 1]]
        points = np.random.multivariate_normal(mean, cov, 500)

        x = np.linspace(-4, 4, 200)
        y = np.linspace(-4, 4, 200)
        X, Y = np.meshgrid(x, y)
        pos = np.dstack((X, Y))
        rv = multivariate_normal(mean, cov)
        Z = rv.pdf(pos)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(points[:, 0], points[:, 1], alpha=0.3, s=10, color='steelblue')
        cs = ax.contour(X, Y, Z, levels=6, colors='red', linewidths=1.5)
        ax.clabel(cs, inline=True, fontsize=8, fmt='%.3f')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Scatter with Density Contours')
        ax.set_aspect('equal')
        plt.show()
