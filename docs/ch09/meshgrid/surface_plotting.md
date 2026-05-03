# Surface Plotting

!!! tip "Mental Model"
    A surface plot visualizes $z = f(x, y)$ by evaluating the function on a meshgrid and passing the three same-shaped arrays (X, Y, Z) to Matplotlib's `plot_surface`. The meshgrid provides the coordinates; the function evaluation provides the heights. Contour plots are the 2D projection of the same data.

## 3D Surface Basics

Mesh grids are essential for creating 3D surface plots with Matplotlib. The `plot_surface` method requires X, Y, and Z arrays of the same shape.

### 1. Simple Surface

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.plot_surface(X, Y, Z)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('Paraboloid')
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Figure Sizing

Use the golden ratio for aesthetically pleasing proportions.

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    phi = 1.61803398875  # golden ratio
    
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    
    fig, ax = plt.subplots(
        figsize=(5 * phi, 5),
        subplot_kw={'projection': '3d'}
    )
    ax.plot_surface(X, Y, Z)
    ax.set_title('Ripple')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Subplot Projection

The `projection='3d'` must be specified in `subplot_kw`.

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-3, 3, 60)
    y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, y)
    
    fig, axes = plt.subplots(
        1, 2,
        figsize=(12, 5),
        subplot_kw={'projection': '3d'}
    )
    
    # First surface
    Z1 = X**2 - Y**2
    axes[0].plot_surface(X, Y, Z1)
    axes[0].set_title('Saddle')
    
    # Second surface
    Z2 = np.sin(X) * np.cos(Y)
    axes[1].plot_surface(X, Y, Z2)
    axes[1].set_title('Wave')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

## Surface Appearance

### 1. Colormaps

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    
    fig, ax = plt.subplots(
        figsize=(8, 6),
        subplot_kw={'projection': '3d'}
    )
    
    surf = ax.plot_surface(
        X, Y, Z,
        cmap=plt.cm.coolwarm,
        linewidth=0,
        antialiased=True
    )
    
    fig.colorbar(surf, shrink=0.5, aspect=10)
    ax.set_title('Colormap: coolwarm')
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Stride and Wireframe

Control mesh density with `rstride` and `cstride`.

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2) / 4)
    
    phi = 1.61803398875
    fig, ax = plt.subplots(
        figsize=(5 * phi, 5),
        subplot_kw={'projection': '3d'}
    )
    
    ax.plot_surface(
        X, Y, Z,
        rstride=2,        # row stride
        cstride=2,        # column stride
        cmap=plt.cm.viridis,
        linewidth=0.5,
        antialiased=True
    )
    
    ax.set_title('Surface with Stride')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Edge Colors

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-2, 2, 30)
    y = np.linspace(-2, 2, 30)
    X, Y = np.meshgrid(x, y)
    Z = X * np.exp(-X**2 - Y**2)
    
    fig, ax = plt.subplots(
        figsize=(8, 6),
        subplot_kw={'projection': '3d'}
    )
    
    ax.plot_surface(
        X, Y, Z,
        cmap='plasma',
        edgecolor='black',
        linewidth=0.3,
        alpha=0.8
    )
    
    ax.set_title('Surface with Edges')
    plt.show()

if __name__ == "__main__":
    main()
```

## PDF Surfaces

### 1. Standard Normal

```python
import numpy as np
import matplotlib.pyplot as plt

def bivariate_normal(X, Y, mu_x=0, mu_y=0, sigma=1):
    """Standard bivariate normal PDF."""
    coef = 1 / (2 * np.pi * sigma**2)
    exp_term = np.exp(-(X**2 + Y**2) / (2 * sigma**2))
    return coef * exp_term

def main():
    x = np.linspace(-4, 4, 100)
    y = np.linspace(-4, 4, 100)
    X, Y = np.meshgrid(x, y)
    Z = bivariate_normal(X, Y)
    
    phi = 1.61803398875
    fig, ax = plt.subplots(
        figsize=(5 * phi, 5),
        subplot_kw={'projection': '3d'}
    )
    
    ax.plot_surface(
        X, Y, Z,
        rstride=2,
        cstride=2,
        cmap=plt.cm.coolwarm,
        linewidth=0.5,
        antialiased=True
    )
    
    ax.set_title('Standard Normal PDF', fontsize=15)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x, y)')
    ax.set_zticks([0.05, 0.10, 0.15])
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Correlated Normal

```python
import numpy as np
import matplotlib.pyplot as plt

def correlated_normal(X, Y, rho=0.5):
    """Bivariate normal with correlation."""
    coef = 1 / (2 * np.pi * np.sqrt(1 - rho**2))
    quad = (X**2 - 2*rho*X*Y + Y**2) / (2 * (1 - rho**2))
    return coef * np.exp(-quad)

def main():
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)
    
    fig, axes = plt.subplots(
        1, 3,
        figsize=(15, 5),
        subplot_kw={'projection': '3d'}
    )
    
    correlations = [-0.7, 0, 0.7]
    
    for ax, rho in zip(axes, correlations):
        Z = correlated_normal(X, Y, rho)
        ax.plot_surface(X, Y, Z, cmap='viridis', linewidth=0)
        ax.set_title(f'ρ = {rho}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Mixture of Gaussians

```python
import numpy as np
import matplotlib.pyplot as plt

def gaussian_2d(X, Y, mu_x, mu_y, sigma):
    """Single 2D Gaussian."""
    return np.exp(-((X - mu_x)**2 + (Y - mu_y)**2) / (2 * sigma**2))

def main():
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    
    # Mixture of three Gaussians
    Z = (0.5 * gaussian_2d(X, Y, -2, 0, 1) +
         0.3 * gaussian_2d(X, Y, 2, 1, 0.8) +
         0.2 * gaussian_2d(X, Y, 0, -2, 1.2))
    
    phi = 1.61803398875
    fig, ax = plt.subplots(
        figsize=(5 * phi, 5),
        subplot_kw={'projection': '3d'}
    )
    
    ax.plot_surface(
        X, Y, Z,
        cmap='magma',
        linewidth=0,
        antialiased=True
    )
    
    ax.set_title('Gaussian Mixture')
    plt.show()

if __name__ == "__main__":
    main()
```

## Contour Integration

### 1. Surface with Contours

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))
    
    fig, ax = plt.subplots(
        figsize=(10, 8),
        subplot_kw={'projection': '3d'}
    )
    
    # Surface
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    
    # Contours on z = -1.5 plane
    ax.contour(X, Y, Z, zdir='z', offset=-1.5, cmap='viridis')
    
    ax.set_zlim(-1.5, 1)
    ax.set_title('Surface with Floor Contours')
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Side Projections

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-2, 2, 60)
    y = np.linspace(-2, 2, 60)
    X, Y = np.meshgrid(x, y)
    Z = X**2 - Y**2
    
    fig, ax = plt.subplots(
        figsize=(10, 8),
        subplot_kw={'projection': '3d'}
    )
    
    ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.7)
    
    # Project onto walls
    ax.contour(X, Y, Z, zdir='x', offset=-2.5, cmap='coolwarm')
    ax.contour(X, Y, Z, zdir='y', offset=2.5, cmap='coolwarm')
    
    ax.set_xlim(-2.5, 2)
    ax.set_ylim(-2, 2.5)
    ax.set_title('Saddle with Projections')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. 2D Contour Alone

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2) / 2) / (2 * np.pi)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Contour lines
    cs1 = axes[0].contour(X, Y, Z, levels=10)
    axes[0].clabel(cs1, inline=True, fontsize=8)
    axes[0].set_title('Contour Lines')
    axes[0].set_aspect('equal')
    
    # Filled contours
    cs2 = axes[1].contourf(X, Y, Z, levels=20, cmap='Blues')
    fig.colorbar(cs2, ax=axes[1])
    axes[1].set_title('Filled Contours')
    axes[1].set_aspect('equal')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

## View and Animation

### 1. View Angles

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)
    
    fig, axes = plt.subplots(
        1, 3,
        figsize=(15, 5),
        subplot_kw={'projection': '3d'}
    )
    
    views = [(30, 45), (60, 30), (90, 0)]
    titles = ['Default', 'High Angle', 'Top View']
    
    for ax, (elev, azim), title in zip(axes, views, titles):
        ax.plot_surface(X, Y, Z, cmap='viridis')
        ax.view_init(elev=elev, azim=azim)
        ax.set_title(f'{title}\nelev={elev}, azim={azim}')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Interactive Rotation

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    """
    Interactive plots allow rotation with mouse drag.
    Use plt.show() without saving for interaction.
    """
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2) / 4)
    
    fig, ax = plt.subplots(
        figsize=(8, 6),
        subplot_kw={'projection': '3d'}
    )
    
    ax.plot_surface(X, Y, Z, cmap='plasma')
    ax.set_title('Drag to Rotate')
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Saving Views

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-2, 2, 60)
    y = np.linspace(-2, 2, 60)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    
    fig, ax = plt.subplots(
        figsize=(8, 6),
        subplot_kw={'projection': '3d'}
    )
    
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.view_init(elev=25, azim=45)
    ax.set_title('Paraboloid')
    
    # Save with specific resolution
    plt.savefig('surface.png', dpi=150, bbox_inches='tight')
    plt.close()
    
    print("Saved: surface.png")

if __name__ == "__main__":
    main()
```

## Alternative Plots

### 1. Wireframe

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-2, 2, 30)
    y = np.linspace(-2, 2, 30)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X**2 + Y**2)
    
    fig, axes = plt.subplots(
        1, 2,
        figsize=(12, 5),
        subplot_kw={'projection': '3d'}
    )
    
    axes[0].plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    axes[0].set_title('Surface')
    
    axes[1].plot_wireframe(X, Y, Z, color='steelblue', linewidth=0.5)
    axes[1].set_title('Wireframe')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Scatter on Surface

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Surface
    x = np.linspace(-2, 2, 40)
    y = np.linspace(-2, 2, 40)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2))
    
    # Sample points
    np.random.seed(42)
    xs = np.random.uniform(-2, 2, 50)
    ys = np.random.uniform(-2, 2, 50)
    zs = np.exp(-(xs**2 + ys**2))
    
    fig, ax = plt.subplots(
        figsize=(8, 6),
        subplot_kw={'projection': '3d'}
    )
    
    ax.plot_surface(X, Y, Z, cmap='Blues', alpha=0.6)
    ax.scatter(xs, ys, zs, c='red', s=30)
    ax.set_title('Surface with Samples')
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Heatmap Alternative

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2) / 2)
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Heatmap (imshow)
    im = axes[0].imshow(
        Z,
        extent=[-3, 3, -3, 3],
        origin='lower',
        cmap='hot',
        aspect='equal'
    )
    fig.colorbar(im, ax=axes[0])
    axes[0].set_title('Heatmap (imshow)')
    
    # Pseudocolor (pcolormesh)
    pc = axes[1].pcolormesh(X, Y, Z, cmap='hot', shading='auto')
    fig.colorbar(pc, ax=axes[1])
    axes[1].set_title('Pseudocolor (pcolormesh)')
    axes[1].set_aspect('equal')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

## Core Pipeline Summary

Every surface plot follows three steps:

```text
1. meshgrid  →  X, Y = np.meshgrid(x, y)
2. compute   →  Z = f(X, Y)
3. visualize →  ax.plot_surface(X, Y, Z)
```

All variations (colormaps, contours, wireframes, projections) are styling on top of this same pipeline. The meshgrid provides coordinates; the function evaluation provides heights; the plotting call renders the result.

---

## Exercises

**Exercise 1.**
Create a meshgrid for `x` and `y` both ranging from -5 to 5 with 50 points. Compute `Z = np.sin(np.sqrt(X**2 + Y**2))` and print the shape of `Z`. Describe what this surface looks like geometrically.

??? success "Solution to Exercise 1"

        import numpy as np

        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(np.sqrt(X**2 + Y**2))
        print(f"Z shape: {Z.shape}")  # (50, 50)
        # This is a circular ripple pattern centered at the origin.

---

**Exercise 2.**
Using meshgrid, evaluate and print the minimum and maximum of the function `f(x, y) = x * exp(-(x^2 + y^2))` on the grid `[-3, 3] x [-3, 3]` with 200 points per axis.

??? success "Solution to Exercise 2"

        import numpy as np

        x = np.linspace(-3, 3, 200)
        y = np.linspace(-3, 3, 200)
        X, Y = np.meshgrid(x, y)
        Z = X * np.exp(-(X**2 + Y**2))
        print(f"Min: {Z.min():.6f}")
        print(f"Max: {Z.max():.6f}")

---

**Exercise 3.**
Create meshgrid coordinates for a parametric surface: a hemisphere defined by `Z = sqrt(max(0, 1 - X^2 - Y^2))` on the grid `[-1, 1] x [-1, 1]`. Use `np.where` or `np.clip` to handle the square root of negative values. Print the shape of `Z` and its maximum value.

??? success "Solution to Exercise 3"

        import numpy as np

        x = np.linspace(-1, 1, 100)
        y = np.linspace(-1, 1, 100)
        X, Y = np.meshgrid(x, y)
        R2 = X**2 + Y**2
        Z = np.sqrt(np.clip(1 - R2, 0, None))
        print(f"Z shape: {Z.shape}")  # (100, 100)
        print(f"Z max: {Z.max():.4f}")  # 1.0
