# Contour and Surface Plots

This document covers techniques for combining 2D contour plots with 3D surface visualizations to provide complementary views of the same data.

!!! tip "Mental Model"
    A surface plot shows the full 3D shape while a contour plot shows the same data as a flat map with level curves. Placing them side by side (or projecting contours onto the base of a 3D plot) gives readers two complementary viewpoints: the surface reveals peaks and valleys, while contours reveal precise level sets and gradients.

!!! tip "Choosing the Right Representation"
    All four visualizations show the same scalar field $z = f(x, y)$ from different perspectives:

    | Representation | Best for | Perspective |
    |---|---|---|
    | `contour` (lines) | Precision reading of exact values | Top-down |
    | `contourf` (filled) | Pattern recognition, regional trends | Top-down |
    | Surface plot | Geometric intuition (peaks, valleys, saddles) | 3D |
    | Projection (contour on 3D base) | Connecting 2D level sets to 3D shape | Hybrid |

    Use `contour` + `contourf` together for the most readable 2D map. Use surface + projected contour for the most complete 3D view.

## Setup

```python
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))
```

---

## Side-by-Side Visualization

### 1. Basic Comparison

```python
fig = plt.figure(figsize=(14, 5))

# 2D Contour
ax1 = fig.add_subplot(1, 2, 1)
cf = ax1.contourf(X, Y, Z, levels=20, cmap='viridis')
ax1.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title('2D Contour Plot')
ax1.set_aspect('equal')
plt.colorbar(cf, ax=ax1)

# 3D Surface
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(X, Y, Z, cmap='viridis', linewidth=0)
ax2.set_xlabel('x')
ax2.set_ylabel('y')
ax2.set_zlabel('z')
ax2.set_title('3D Surface Plot')

plt.tight_layout()
plt.show()
```

### 2. Multiple View Angles

```python
fig = plt.figure(figsize=(15, 10))

# Contour plot
ax1 = fig.add_subplot(2, 2, 1)
cf = ax1.contourf(X, Y, Z, levels=15, cmap='viridis')
cs = ax1.contour(X, Y, Z, levels=8, colors='white', linewidths=0.5)
ax1.clabel(cs, inline=True, fontsize=8)
ax1.set_title('Contour (Top View)')
ax1.set_aspect('equal')
plt.colorbar(cf, ax=ax1)

# 3D views
views = [(30, -60), (60, -60), (30, 45)]
titles = ['Standard View', 'High Angle', 'Rotated View']

for idx, ((elev, azim), title) in enumerate(zip(views, titles)):
    ax = fig.add_subplot(2, 2, idx + 2, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0)
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(f'3D Surface: {title}')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

plt.tight_layout()
plt.show()
```

---

## Contour Projection on 3D Plot

Project contours onto the base plane of a 3D surface plot.

### 1. Basic Projection

```python
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})

# Surface plot
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)

# Contour projection on z=0 plane
ax.contour(X, Y, Z, zdir='z', offset=0, cmap='viridis', levels=10)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_title('Surface with Contour Projection')
plt.show()
```

### 2. Filled Contour Projection

```python
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})

# Surface plot
ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)

# Filled contour projection
ax.contourf(X, Y, Z, zdir='z', offset=-0.2, cmap='viridis', levels=15, alpha=0.8)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_zlim(-0.2, 1.1)
ax.set_title('Surface with Filled Contour Projection')
plt.show()
```

### 3. Multiple Projections

```python
fig, ax = plt.subplots(figsize=(12, 10), subplot_kw={'projection': '3d'})

# Surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.6)

# XY plane projection (bottom)
ax.contourf(X, Y, Z, zdir='z', offset=-0.1, cmap='viridis', levels=10, alpha=0.7)

# XZ plane projection (back)
ax.contourf(X, Y, Z, zdir='y', offset=3.5, cmap='viridis', levels=10, alpha=0.5)

# YZ plane projection (side)
ax.contourf(X, Y, Z, zdir='x', offset=-3.5, cmap='viridis', levels=10, alpha=0.5)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.set_xlim(-3.5, 3)
ax.set_ylim(-3, 3.5)
ax.set_zlim(-0.1, 1.1)
ax.set_title('Surface with Multiple Contour Projections')
plt.show()
```

---

## Wireframe with Contours

### 1. Wireframe Surface

```python
fig = plt.figure(figsize=(14, 5))

# Filled contour
ax1 = fig.add_subplot(1, 2, 1)
cf = ax1.contourf(X, Y, Z, levels=20, cmap='coolwarm')
ax1.set_title('Filled Contour')
ax1.set_aspect('equal')
plt.colorbar(cf, ax=ax1)

# Wireframe
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_wireframe(X, Y, Z, rstride=5, cstride=5, color='blue', linewidth=0.5)
ax2.set_title('Wireframe')

plt.tight_layout()
plt.show()
```

### 2. Wireframe with Contour Projection

```python
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})

# Wireframe
ax.plot_wireframe(X, Y, Z, rstride=5, cstride=5, color='navy', linewidth=0.5, alpha=0.7)

# Contour projection
ax.contour(X, Y, Z, zdir='z', offset=0, cmap='Blues', levels=10)

ax.set_zlim(0, 1.1)
ax.set_title('Wireframe with Contour Projection')
plt.show()
```

---

## Mathematical Functions Gallery

### 1. Gaussian Function

```python
Z_gauss = np.exp(-(X**2 + Y**2))

fig = plt.figure(figsize=(14, 5))

ax1 = fig.add_subplot(1, 2, 1)
cf = ax1.contourf(X, Y, Z_gauss, levels=20, cmap='viridis')
ax1.contour(X, Y, Z_gauss, levels=10, colors='white', linewidths=0.5)
ax1.set_title('Gaussian: $e^{-(x^2+y^2)}$')
ax1.set_aspect('equal')
plt.colorbar(cf, ax=ax1)

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(X, Y, Z_gauss, cmap='viridis')
ax2.set_title('Gaussian Surface')

plt.tight_layout()
plt.show()
```

### 2. Saddle Function

```python
Z_saddle = X**2 - Y**2

fig = plt.figure(figsize=(14, 5))

ax1 = fig.add_subplot(1, 2, 1)
cf = ax1.contourf(X, Y, Z_saddle, levels=20, cmap='coolwarm')
ax1.contour(X, Y, Z_saddle, levels=[0], colors='black', linewidths=2)  # Zero contour
ax1.set_title('Saddle: $x^2 - y^2$')
ax1.set_aspect('equal')
plt.colorbar(cf, ax=ax1)

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(X, Y, Z_saddle, cmap='coolwarm')
ax2.set_title('Saddle Surface')

plt.tight_layout()
plt.show()
```

### 3. Sinusoidal Function

```python
Z_sin = np.sin(X) * np.cos(Y)

fig = plt.figure(figsize=(14, 5))

ax1 = fig.add_subplot(1, 2, 1)
cf = ax1.contourf(X, Y, Z_sin, levels=20, cmap='RdBu')
ax1.contour(X, Y, Z_sin, levels=[0], colors='black', linewidths=1)
ax1.set_title('$\\sin(x)\\cos(y)$')
ax1.set_aspect('equal')
plt.colorbar(cf, ax=ax1)

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(X, Y, Z_sin, cmap='RdBu')
ax2.set_title('Sinusoidal Surface')

plt.tight_layout()
plt.show()
```

### 4. Function Gallery

```python
functions = [
    (np.exp(-(X**2 + Y**2)), 'Gaussian', 'viridis'),
    (X**2 - Y**2, 'Saddle', 'coolwarm'),
    (np.sin(X) * np.cos(Y), 'sin(x)cos(y)', 'RdBu'),
    (np.sin(np.sqrt(X**2 + Y**2)), 'Ripple', 'plasma')
]

fig = plt.figure(figsize=(16, 12))

for idx, (Z_func, title, cmap) in enumerate(functions):
    # Contour
    ax1 = fig.add_subplot(4, 2, 2*idx + 1)
    cf = ax1.contourf(X, Y, Z_func, levels=15, cmap=cmap)
    ax1.contour(X, Y, Z_func, levels=8, colors='black', linewidths=0.3)
    ax1.set_title(f'{title} (Contour)')
    ax1.set_aspect('equal')
    plt.colorbar(cf, ax=ax1)
    
    # Surface
    ax2 = fig.add_subplot(4, 2, 2*idx + 2, projection='3d')
    ax2.plot_surface(X, Y, Z_func, cmap=cmap, linewidth=0)
    ax2.set_title(f'{title} (Surface)')

plt.tight_layout()
plt.show()
```

---

## Bivariate Normal Distribution

### 1. Standard Normal

```python
from scipy import stats

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))

rv = stats.multivariate_normal([0, 0], [[1, 0], [0, 1]])
Z = rv.pdf(pos)

fig = plt.figure(figsize=(14, 5))

ax1 = fig.add_subplot(1, 2, 1)
cf = ax1.contourf(X, Y, Z, levels=20, cmap='Blues')
ax1.contour(X, Y, Z, levels=10, colors='navy', linewidths=0.5)
ax1.set_title('Standard Bivariate Normal')
ax1.set_aspect('equal')
plt.colorbar(cf, ax=ax1, label='Density')

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.plot_surface(X, Y, Z, cmap='Blues')
ax2.set_title('PDF Surface')
ax2.set_zlabel('Density')

plt.tight_layout()
plt.show()
```

### 2. Correlation Comparison

```python
rhos = [-0.7, 0, 0.7]

fig = plt.figure(figsize=(15, 8))

for idx, rho in enumerate(rhos):
    rv = stats.multivariate_normal([0, 0], [[1, rho], [rho, 1]])
    Z = rv.pdf(pos)
    
    # Contour
    ax1 = fig.add_subplot(2, 3, idx + 1)
    cf = ax1.contourf(X, Y, Z, levels=15, cmap='Blues')
    ax1.set_title(f'ρ = {rho}')
    ax1.set_aspect('equal')
    plt.colorbar(cf, ax=ax1)
    
    # Surface
    ax2 = fig.add_subplot(2, 3, idx + 4, projection='3d')
    ax2.plot_surface(X, Y, Z, cmap='Blues')
    ax2.set_title(f'Surface (ρ = {rho})')
    ax2.view_init(30, -60)

plt.tight_layout()
plt.show()
```

---

## Interactive-Style Dashboard

```python
Z = np.exp(-(X**2 + Y**2) / 2) / (2 * np.pi)

fig = plt.figure(figsize=(16, 10))

# Main 3D surface (large)
ax_3d = fig.add_subplot(2, 2, 1, projection='3d')
surf = ax_3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9)
ax_3d.contourf(X, Y, Z, zdir='z', offset=0, cmap='viridis', levels=10, alpha=0.5)
ax_3d.set_xlabel('x')
ax_3d.set_ylabel('y')
ax_3d.set_zlabel('f(x,y)')
ax_3d.set_title('3D Surface with Contour Projection', fontsize=12)
ax_3d.view_init(30, -60)

# Top-down contour view
ax_top = fig.add_subplot(2, 2, 2)
cf = ax_top.contourf(X, Y, Z, levels=20, cmap='viridis')
cs = ax_top.contour(X, Y, Z, levels=10, colors='white', linewidths=0.5)
ax_top.clabel(cs, inline=True, fontsize=7, fmt='%.3f')
ax_top.set_xlabel('x')
ax_top.set_ylabel('y')
ax_top.set_title('Contour Plot (Top View)', fontsize=12)
ax_top.set_aspect('equal')
plt.colorbar(cf, ax=ax_top)

# X cross-section
ax_xsec = fig.add_subplot(2, 2, 3)
mid_idx = len(y) // 2
ax_xsec.plot(x, Z[mid_idx, :], 'b-', linewidth=2)
ax_xsec.fill_between(x, Z[mid_idx, :], alpha=0.3)
ax_xsec.set_xlabel('x')
ax_xsec.set_ylabel('f(x, 0)')
ax_xsec.set_title('Cross-Section at y = 0', fontsize=12)
ax_xsec.grid(alpha=0.3)

# Y cross-section
ax_ysec = fig.add_subplot(2, 2, 4)
ax_ysec.plot(y, Z[:, mid_idx], 'r-', linewidth=2)
ax_ysec.fill_between(y, Z[:, mid_idx], alpha=0.3, color='red')
ax_ysec.set_xlabel('y')
ax_ysec.set_ylabel('f(0, y)')
ax_ysec.set_title('Cross-Section at x = 0', fontsize=12)
ax_ysec.grid(alpha=0.3)

plt.suptitle('Standard Bivariate Normal Distribution Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## Publication-Quality Figure

```python
from scipy import stats

# Setup
x = np.linspace(-3, 3, 150)
y = np.linspace(-3, 3, 150)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))

rho = 0.6
rv = stats.multivariate_normal([0, 0], [[1, rho], [rho, 1]])
Z = rv.pdf(pos)

fig = plt.figure(figsize=(14, 5))

# Contour plot
ax1 = fig.add_subplot(1, 2, 1)
cf = ax1.contourf(X, Y, Z, levels=15, cmap='Blues')
cs = ax1.contour(X, Y, Z, levels=8, colors='navy', linewidths=0.6, alpha=0.8)
ax1.clabel(cs, inline=True, fontsize=8, fmt='%.3f')
ax1.set_xlabel('$X$', fontsize=12)
ax1.set_ylabel('$Y$', fontsize=12)
ax1.set_title('Contour Plot', fontsize=13)
ax1.set_aspect('equal')
ax1.tick_params(labelsize=10)
cbar1 = plt.colorbar(cf, ax=ax1)
cbar1.set_label('Probability Density', fontsize=11)

# Surface plot
ax2 = fig.add_subplot(1, 2, 2, projection='3d')
surf = ax2.plot_surface(X, Y, Z, cmap='Blues', linewidth=0, antialiased=True)
ax2.contourf(X, Y, Z, zdir='z', offset=0, cmap='Blues', levels=10, alpha=0.5)
ax2.set_xlabel('$X$', fontsize=11, labelpad=10)
ax2.set_ylabel('$Y$', fontsize=11, labelpad=10)
ax2.set_zlabel('Density', fontsize=11, labelpad=10)
ax2.set_title('Surface Plot', fontsize=13)
ax2.view_init(25, -50)
ax2.tick_params(labelsize=9)

# White panes
ax2.w_xaxis.set_pane_color((0.98, 0.98, 0.98, 1.0))
ax2.w_yaxis.set_pane_color((0.98, 0.98, 0.98, 1.0))
ax2.w_zaxis.set_pane_color((0.98, 0.98, 0.98, 1.0))

plt.suptitle(f'Bivariate Normal Distribution ($\\rho = {rho}$)', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
```

---

## Summary

| Visualization | Best For |
|---------------|----------|
| Contour only | 2D view, precise level reading |
| Surface only | Overall shape understanding |
| Contour + Surface side-by-side | Comprehensive analysis |
| Surface + Contour projection | 3D context with 2D precision |
| Wireframe + Contour | Structure visualization |
| Dashboard (multiple views) | Complete exploration |

---

## Exercises

**Exercise 1.**
Create a side-by-side figure (1x2) showing a filled contour plot on the left and a 3D surface plot on the right for the function $z = \cos(\sqrt{x^2 + y^2})$ over $[-5, 5] \times [-5, 5]$. Use the same colormap for both.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-5, 5, 200)
        y = np.linspace(-5, 5, 200)
        X, Y = np.meshgrid(x, y)
        Z = np.cos(np.sqrt(X**2 + Y**2))

        fig = plt.figure(figsize=(14, 5))

        ax1 = fig.add_subplot(1, 2, 1)
        cf = ax1.contourf(X, Y, Z, levels=20, cmap='viridis')
        plt.colorbar(cf, ax=ax1)
        ax1.set_title('Filled Contour')
        ax1.set_aspect('equal')

        ax2 = fig.add_subplot(1, 2, 2, projection='3d')
        ax2.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9)
        ax2.set_title('3D Surface')

        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Create a 3D surface plot of $z = \sin(x) \cdot \cos(y)$ and project contour lines onto the z-axis floor of the 3D axes using `ax.contour` with the `zdir='z'` and `offset` parameters. Set the offset to the minimum z value.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-np.pi, np.pi, 100)
        y = np.linspace(-np.pi, np.pi, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.8)
        ax.contour(X, Y, Z, zdir='z', offset=Z.min(), cmap='coolwarm', levels=15)

        ax.set_zlim(Z.min() - 0.3, Z.max())
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Surface with Projected Contours')
        plt.show()

---

**Exercise 3.**
Build a three-panel figure: top-left shows `contour` (line), top-right shows `contourf` (filled), and bottom (spanning full width) shows the 3D `plot_surface`. Use the function $z = x^2 - y^2$ over $[-2, 2] \times [-2, 2]$. Use `gridspec` for the layout.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import matplotlib.gridspec as gridspec
        import numpy as np

        x = np.linspace(-2, 2, 100)
        y = np.linspace(-2, 2, 100)
        X, Y = np.meshgrid(x, y)
        Z = X**2 - Y**2

        fig = plt.figure(figsize=(12, 10))
        gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1.2])

        ax1 = fig.add_subplot(gs[0, 0])
        cs = ax1.contour(X, Y, Z, levels=15, cmap='RdBu')
        ax1.clabel(cs, inline=True, fontsize=8)
        ax1.set_title('Contour Lines')
        ax1.set_aspect('equal')

        ax2 = fig.add_subplot(gs[0, 1])
        cf = ax2.contourf(X, Y, Z, levels=15, cmap='RdBu')
        plt.colorbar(cf, ax=ax2)
        ax2.set_title('Filled Contour')
        ax2.set_aspect('equal')

        ax3 = fig.add_subplot(gs[1, :], projection='3d')
        ax3.plot_surface(X, Y, Z, cmap='RdBu', alpha=0.9)
        ax3.set_title('3D Surface')

        plt.tight_layout()
        plt.show()
