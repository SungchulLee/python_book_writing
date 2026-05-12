# Axes Method - view_init

The `view_init` method sets the elevation and azimuth angles for viewing a 3D plot. It controls the camera position relative to the plotted surface.

!!! tip "Mental Model"
    `view_init(elev, azim)` positions the camera orbiting your 3D plot. Elevation tilts up/down (0 degrees is eye-level, 90 degrees is bird's-eye view), and azimuth rotates left/right around the z-axis. Experiment with different angles to find the view that best reveals your data's structure -- a single surface can look completely different from two viewpoints.

## Understanding View Angles

The view is defined by two angles:

- **Elevation (elev)**: Angle above the xy-plane in degrees. 0° is edge-on, 90° is directly above.
- **Azimuth (azim)**: Rotation around the z-axis in degrees. Determines horizontal viewing direction.

## Basic Usage

Set viewing angles after creating a 3D plot.

### 1. Default View

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 2, 30)
y = np.linspace(-2, 2, 30)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
plt.show()
```

### 2. Custom View

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=30, azim=45)
plt.show()
```

### 3. Top-Down View

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=90, azim=0)
plt.show()
```

## Elevation Angle

Control the vertical viewing angle.

### 1. Low Elevation

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=10, azim=-60)
plt.show()
```

### 2. Medium Elevation

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=30, azim=-60)
plt.show()
```

### 3. High Elevation

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=60, azim=-60)
plt.show()
```

### 4. Elevation Comparison

```python
fig, axes = plt.subplots(1, 4, figsize=(16, 4), subplot_kw={'projection': '3d'})

elevations = [0, 30, 60, 90]

for ax, elev in zip(axes, elevations):
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.view_init(elev=elev, azim=-60)
    ax.set_title(f'elev={elev}°')

plt.tight_layout()
plt.show()
```

## Azimuth Angle

Control the horizontal rotation.

### 1. Front View

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=30, azim=0)
plt.show()
```

### 2. Side View

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=30, azim=90)
plt.show()
```

### 3. Azimuth Comparison

```python
fig, axes = plt.subplots(1, 4, figsize=(16, 4), subplot_kw={'projection': '3d'})

azimuths = [0, 45, 90, 135]

for ax, azim in zip(axes, azimuths):
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.view_init(elev=30, azim=azim)
    ax.set_title(f'azim={azim}°')

plt.tight_layout()
plt.show()
```

### 4. Full Rotation

```python
fig, axes = plt.subplots(2, 4, figsize=(16, 8), subplot_kw={'projection': '3d'})

azimuths = [0, 45, 90, 135, 180, 225, 270, 315]

for ax, azim in zip(axes.flat, azimuths):
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.view_init(elev=30, azim=azim)
    ax.set_title(f'azim={azim}°')

plt.tight_layout()
plt.show()
```

## Standard Views

Common viewing angles for specific perspectives.

### 1. Isometric View

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=35, azim=45)
ax.set_title('Isometric View')
plt.show()
```

### 2. Top-Down View

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=90, azim=0)
ax.set_title('Top-Down View')
plt.show()
```

### 3. Side Profile

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=0, azim=0)
ax.set_title('Side Profile')
plt.show()
```

### 4. Standard Views Gallery

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 10), subplot_kw={'projection': '3d'})

views = [
    (30, -60, 'Default'),
    (90, 0, 'Top-Down'),
    (0, 0, 'Front'),
    (0, 90, 'Side'),
    (35, 45, 'Isometric'),
    (60, -45, 'High Angle')
]

for ax, (elev, azim, title) in zip(axes.flat, views):
    ax.plot_surface(X, Y, Z, cmap='viridis')
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(f'{title}\n(elev={elev}°, azim={azim}°)')

plt.tight_layout()
plt.show()
```

## Bivariate Normal Distribution Views

Apply view_init to statistical distributions.

### 1. Correlation Comparison with Consistent View

```python
from scipy import stats

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

ax0.plot_surface(X, Y, Z(rho1).pdf(pos), cmap='viridis', linewidth=0)
ax0.set_xlabel('X axis')
ax0.set_ylabel('Y axis')
ax0.view_init(80, -90)
ax0.set_title(f'ρ = {rho1}')

ax1.plot_surface(X, Y, Z(rho2).pdf(pos), cmap='viridis', linewidth=0)
ax1.set_xlabel('X axis')
ax1.set_ylabel('Y axis')
ax1.view_init(80, -90)
ax1.set_title(f'ρ = {rho2}')

ax2.plot_surface(X, Y, Z(rho3).pdf(pos), cmap='viridis', linewidth=0)
ax2.set_xlabel('X axis')
ax2.set_ylabel('Y axis')
ax2.view_init(80, -90)
ax2.set_title(f'ρ = {rho3}')

plt.tight_layout()
plt.show()
```

### 2. Top View for Contour Effect

```python
rv = stats.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]])
Z_norm = rv.pdf(pos)

fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={'projection': '3d'})

axes[0].plot_surface(X, Y, Z_norm, cmap='viridis')
axes[0].view_init(elev=30, azim=-60)
axes[0].set_title('3D Perspective')

axes[1].plot_surface(X, Y, Z_norm, cmap='viridis')
axes[1].view_init(elev=90, azim=0)
axes[1].set_title('Top View (Contour-like)')

plt.tight_layout()
plt.show()
```

## Multiple Angles of Same Surface

### 1. Four-View Layout

```python
Z = np.sin(np.sqrt(X**2 + Y**2))

fig, axes = plt.subplots(2, 2, figsize=(12, 10), subplot_kw={'projection': '3d'})

views = [(30, -60), (30, 60), (60, -60), (60, 60)]
labels = ['Front-Left', 'Front-Right', 'High-Left', 'High-Right']

for ax, (elev, azim), label in zip(axes.flat, views, labels):
    ax.plot_surface(X, Y, Z, cmap='plasma')
    ax.view_init(elev=elev, azim=azim)
    ax.set_title(f'{label}\n(elev={elev}°, azim={azim}°)')

plt.tight_layout()
plt.show()
```

### 2. Rotating Views

```python
fig, axes = plt.subplots(2, 3, figsize=(15, 10), subplot_kw={'projection': '3d'})

angles = range(0, 360, 60)

for ax, azim in zip(axes.flat, angles):
    ax.plot_surface(X, Y, Z, cmap='coolwarm')
    ax.view_init(elev=30, azim=azim)
    ax.set_title(f'azim={azim}°')

plt.tight_layout()
plt.show()
```

## Combined with Other 3D Settings

### 1. With Axis Labels

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=25, azim=45)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()
```

### 2. With Title

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=35, azim=-45)
ax.set_title('Surface Plot with Custom View', fontsize=14)
plt.show()
```

### 3. With Colorbar

```python
fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
surf = ax.plot_surface(X, Y, Z, cmap='coolwarm')
ax.view_init(elev=30, azim=45)
fig.colorbar(surf, shrink=0.5, aspect=10)
plt.show()
```

## Negative Elevation

View from below the surface.

### 1. Below Surface View

```python
fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
ax.plot_surface(X, Y, Z, cmap='viridis')
ax.view_init(elev=-30, azim=45)
ax.set_title('View from Below (elev=-30°)')
plt.show()
```

### 2. Above vs Below Comparison

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5), subplot_kw={'projection': '3d'})

axes[0].plot_surface(X, Y, Z, cmap='viridis')
axes[0].view_init(elev=30, azim=45)
axes[0].set_title('Above (elev=30°)')

axes[1].plot_surface(X, Y, Z, cmap='viridis')
axes[1].view_init(elev=-30, azim=45)
axes[1].set_title('Below (elev=-30°)')

plt.tight_layout()
plt.show()
```

## Practical Applications

### 1. Best View for Data Understanding

```python
def f(X, Y):
    return np.exp(-(X**2 + Y**2) / 2) / (2 * np.pi)

x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': '3d'})

# 3D perspective
axes[0].plot_surface(X, Y, Z, cmap='viridis')
axes[0].view_init(elev=30, azim=-60)
axes[0].set_title('3D Shape')

# Top view for distribution spread
axes[1].plot_surface(X, Y, Z, cmap='viridis')
axes[1].view_init(elev=90, azim=0)
axes[1].set_title('Distribution Spread')

# Side view for peak height
axes[2].plot_surface(X, Y, Z, cmap='viridis')
axes[2].view_init(elev=0, azim=0)
axes[2].set_title('Peak Height')

plt.tight_layout()
plt.show()
```

### 2. Publication-Quality Figure

```python
from scipy import stats

n = 60
x = np.linspace(-3, 3, n)
y = np.linspace(-3, 3, n)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))

rv = stats.multivariate_normal([0, 0], [[1, 0.6], [0.6, 1]])
Z = rv.pdf(pos)

fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': '3d'})
surf = ax.plot_surface(
    X, Y, Z,
    cmap='viridis',
    linewidth=0,
    antialiased=True
)
ax.view_init(elev=25, azim=-50)
ax.set_xlabel('X', fontsize=12)
ax.set_ylabel('Y', fontsize=12)
ax.set_zlabel('Density', fontsize=12)
ax.set_title('Bivariate Normal Distribution (ρ = 0.6)', fontsize=14, fontweight='bold')
fig.colorbar(surf, shrink=0.6, aspect=15, label='Probability Density')
plt.tight_layout()
plt.show()
```

### 3. Comparison Dashboard

```python
Z1 = X**2 + Y**2
Z2 = X**2 - Y**2
Z3 = np.sin(X) * np.cos(Y)
Z4 = np.exp(-(X**2 + Y**2))

surfaces = [(Z1, 'Paraboloid'), (Z2, 'Saddle'), (Z3, 'Wave'), (Z4, 'Gaussian')]

fig, axes = plt.subplots(2, 2, figsize=(14, 12), subplot_kw={'projection': '3d'})

for ax, (Z, title) in zip(axes.flat, surfaces):
    ax.plot_surface(X, Y, Z, cmap='coolwarm', linewidth=0)
    ax.view_init(elev=30, azim=-45)
    ax.set_title(title, fontsize=12)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

plt.tight_layout()
plt.show()
```

## What Each View Reveals

`view_init` is not just a camera --- it is a tool to extract structure. Different angles reveal different features of the same surface:

| View | `view_init` | What it reveals |
|---|---|---|
| Top-down | `(90, 0)` | Contour structure, symmetry |
| Side view | `(0, 0)` | Amplitude / cross-section along one axis |
| Diagonal | `(30, 45)` | Overall 3D shape (default) |
| Rotated side | `(0, 90)` | Cross-section along the other axis |

**Workflow for choosing the best view:**

1. Start at default `(30, -60)` --- get overall shape
2. Rotate to top-down `(90, 0)` --- check symmetry and contour structure
3. Rotate to side `(0, 0)` and `(0, 90)` --- check amplitude profiles along each axis
4. Choose the angle that reveals the most structure with least occlusion

---

## Exercises

**Exercise 1.**
Create a surface plot of $z = \sin(x) \cdot \cos(y)$ and display it in a 2x2 grid of subplots, each with a different combination of elevation and azimuth: (10, 0), (30, 45), (60, 120), and (90, 0). Title each subplot with the angles used.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-np.pi, np.pi, 100)
        y = np.linspace(-np.pi, np.pi, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)

        angles = [(10, 0), (30, 45), (60, 120), (90, 0)]

        fig = plt.figure(figsize=(12, 10))
        for i, (elev, azim) in enumerate(angles, 1):
            ax = fig.add_subplot(2, 2, i, projection='3d')
            ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9)
            ax.view_init(elev=elev, azim=azim)
            ax.set_title(f'elev={elev}, azim={azim}')

        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Plot the surface $z = x^2 - y^2$ (a saddle) and create three views: a front view (`elev=0, azim=0`), a top-down view (`elev=90, azim=0`), and an isometric view (`elev=35, azim=225`). Arrange the views side by side using `plt.subplots(1, 3)`.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        Z = X**2 - Y**2

        views = [
            (0, 0, 'Front View'),
            (90, 0, 'Top-Down View'),
            (35, 225, 'Isometric View'),
        ]

        fig, axes = plt.subplots(1, 3, figsize=(15, 5),
                                  subplot_kw={'projection': '3d'})

        for ax, (elev, azim, title) in zip(axes, views):
            ax.plot_surface(X, Y, Z, cmap='coolwarm', alpha=0.9)
            ax.view_init(elev=elev, azim=azim)
            ax.set_title(title)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')

        plt.tight_layout()
        plt.show()

---

**Exercise 3.**
Create a surface plot of $z = e^{-(x^2 + y^2)}$ and use `view_init` with `roll=30` in addition to `elev=30, azim=45` to tilt the camera. Compare this tilted view with the non-tilted version (`roll=0`) side by side.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 + Y**2))

        fig, axes = plt.subplots(1, 2, figsize=(14, 6),
                                  subplot_kw={'projection': '3d'})

        axes[0].plot_surface(X, Y, Z, cmap='plasma', alpha=0.9)
        axes[0].view_init(elev=30, azim=45, roll=0)
        axes[0].set_title('roll=0 (default)')

        axes[1].plot_surface(X, Y, Z, cmap='plasma', alpha=0.9)
        axes[1].view_init(elev=30, azim=45, roll=30)
        axes[1].set_title('roll=30')

        plt.tight_layout()
        plt.show()
