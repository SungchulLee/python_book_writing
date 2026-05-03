# Axes Method - clabel

The `plt.clabel()` or `ax.clabel()` method adds labels to contour lines.

!!! tip "Mental Model"
    Contour lines without labels are like elevation lines on a map with no numbers -- you can see the shape but not the values. `clabel()` stamps numeric values directly onto the contour lines, turning your plot into a self-documenting map. Pass the contour set returned by `contour()` and Matplotlib places labels at readable positions automatically.

## Basic Usage

### Adding Labels to Contours

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
    
    # Plot contour
    contours = ax.contour(X, Y, Z, levels=3, colors='black')
    
    # Put labels to the contour lines
    plt.clabel(contours, inline=True, fontsize=20)
    plt.show()

if __name__ == "__main__":
    main()
```

## Key Parameters

### inline Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# inline=True (default) - line is broken at label
contours1 = axes[0].contour(X, Y, Z, levels=5, colors='black')
axes[0].clabel(contours1, inline=True, fontsize=12)
axes[0].set_title('inline=True (breaks line)')

# inline=False - label placed on top of line
contours2 = axes[1].contour(X, Y, Z, levels=5, colors='black')
axes[1].clabel(contours2, inline=False, fontsize=12)
axes[1].set_title('inline=False (overlaps line)')

for ax in axes:
    ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

### fontsize Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
fontsizes = [8, 14, 20]

for ax, fs in zip(axes, fontsizes):
    contours = ax.contour(X, Y, Z, levels=5, colors='black')
    ax.clabel(contours, inline=True, fontsize=fs)
    ax.set_title(f'fontsize={fs}')
    ax.set_aspect('equal')

plt.tight_layout()
plt.show()
```

## Format Control

### fmt Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Default format
contours1 = axes[0].contour(X, Y, Z, levels=[1, 2, 4, 6, 8])
axes[0].clabel(contours1, inline=True, fontsize=10)
axes[0].set_title('Default format')

# Decimal places
contours2 = axes[1].contour(X, Y, Z, levels=[1, 2, 4, 6, 8])
axes[1].clabel(contours2, inline=True, fontsize=10, fmt='%.2f')
axes[1].set_title("fmt='%.2f'")

# Integer format
contours3 = axes[2].contour(X, Y, Z, levels=[1, 2, 4, 6, 8])
axes[2].clabel(contours3, inline=True, fontsize=10, fmt='%d')
axes[2].set_title("fmt='%d'")

for ax in axes:
    ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

### Custom Format Function

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

# Custom format function
def fmt_func(x):
    return f'r={np.sqrt(x):.1f}'

fig, ax = plt.subplots(figsize=(8, 6))
contours = ax.contour(X, Y, Z, levels=[1, 4, 9, 16])
ax.clabel(contours, inline=True, fontsize=10, fmt=fmt_func)
ax.set_title('Custom format: radius values')
ax.set_aspect('equal')
plt.show()
```

### Dictionary Format

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

# Format dictionary for specific levels
fmt_dict = {
    1: 'Low',
    4: 'Medium',
    9: 'High'
}

fig, ax = plt.subplots(figsize=(8, 6))
contours = ax.contour(X, Y, Z, levels=[1, 4, 9])
ax.clabel(contours, inline=True, fontsize=12, fmt=fmt_dict)
ax.set_title('Dictionary format: custom labels')
ax.set_aspect('equal')
plt.show()
```

## Styling Labels

### colors Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Default (matches contour color)
contours1 = axes[0].contour(X, Y, Z, levels=5, colors='blue')
axes[0].clabel(contours1, inline=True, fontsize=10)
axes[0].set_title('Default label color')

# Explicit color
contours2 = axes[1].contour(X, Y, Z, levels=5, colors='blue')
axes[1].clabel(contours2, inline=True, fontsize=10, colors='red')
axes[1].set_title("colors='red'")

# With colormap
contours3 = axes[2].contour(X, Y, Z, levels=5, cmap='viridis')
axes[2].clabel(contours3, inline=True, fontsize=10, colors='black')
axes[2].set_title("colors='black' on colormap")

for ax in axes:
    ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

## Selective Labeling

### levels Parameter in clabel

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Label all levels
contours1 = axes[0].contour(X, Y, Z, levels=[1, 2, 3, 4, 5, 6, 7, 8])
axes[0].clabel(contours1, inline=True, fontsize=10)
axes[0].set_title('All levels labeled')

# Label only specific levels
contours2 = axes[1].contour(X, Y, Z, levels=[1, 2, 3, 4, 5, 6, 7, 8])
axes[1].clabel(contours2, levels=[2, 4, 6, 8], inline=True, fontsize=10)
axes[1].set_title('Only even levels labeled')

for ax in axes:
    ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

## Manual Placement

### manual Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = X**2 + Y**2

fig, ax = plt.subplots(figsize=(8, 6))
contours = ax.contour(X, Y, Z, levels=[1, 4, 9])

# Specify label positions manually
manual_locations = [(0.5, 0.5), (1.5, 1.0), (2.5, 1.5)]
ax.clabel(contours, inline=True, fontsize=12, manual=manual_locations)

ax.set_title('Manual label placement')
ax.set_aspect('equal')
plt.show()
```

## Inline Spacing

### inline_spacing Parameter

```python
import matplotlib.pyplot as plt
import numpy as np

f = lambda x, y: np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)
x = np.linspace(0, 5, 50)
y = np.linspace(0, 5, 40)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
spacings = [2, 5, 10]

for ax, spacing in zip(axes, spacings):
    contours = ax.contour(X, Y, Z, levels=5, colors='black')
    ax.clabel(contours, inline=True, fontsize=10, inline_spacing=spacing)
    ax.set_title(f'inline_spacing={spacing}')
    ax.set_aspect('equal')

plt.tight_layout()
plt.show()
```

## With Filled Contours

### Labels on contourf

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

# Line contours for labels
cs = ax.contour(X, Y, Z, levels=7, colors='black', linewidths=0.5)
ax.clabel(cs, inline=True, fontsize=10, fmt='%.2f')

fig.colorbar(cf, ax=ax)
ax.set_title('Labels on Filled Contours')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

## Practical Example

### Topographic Map with Elevation Labels

```python
import matplotlib.pyplot as plt
import numpy as np

# Create terrain
x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)
Z = (2 * np.sin(X) * np.cos(Y) + 
     np.sin(2*X) * np.cos(2*Y) +
     0.5 * np.sin(4*X) * np.cos(4*Y) + 3)  # Add offset for positive values

fig, ax = plt.subplots(figsize=(10, 8))

# Filled contours
cf = ax.contourf(X, Y, Z, levels=20, cmap='terrain')

# Labeled contours
cs = ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.7)
ax.clabel(cs, inline=True, fontsize=9, fmt='%1.1f m')

fig.colorbar(cf, ax=ax, label='Elevation (m)')
ax.set_title('Topographic Map with Elevation Labels', fontsize=14)
ax.set_xlabel('Distance (km)')
ax.set_ylabel('Distance (km)')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

### Temperature Distribution

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = 20 + 10 * np.exp(-(X**2 + Y**2) / 10)  # Temperature distribution

fig, ax = plt.subplots(figsize=(10, 8))

cf = ax.contourf(X, Y, Z, levels=15, cmap='coolwarm')
cs = ax.contour(X, Y, Z, levels=10, colors='black', linewidths=0.5)
ax.clabel(cs, inline=True, fontsize=10, fmt='%.1f°C')

fig.colorbar(cf, ax=ax, label='Temperature (°C)')
ax.set_title('Temperature Distribution', fontsize=14)
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()
```

---

## Exercises

**Exercise 1.**
Create a contour plot of $z = x^2 + y^2$ over $[-3, 3] \times [-3, 3]$ with 10 levels. Add contour labels using `ax.clabel` with `inline=True` and `fontsize=10`. Format the labels to show one decimal place using `fmt='%.1f'`.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2

        fig, ax = plt.subplots(figsize=(8, 6))
        cs = ax.contour(X, Y, Z, levels=10)
        ax.clabel(cs, inline=True, fontsize=10, fmt='%.1f')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(r'Contour Plot of $z = x^2 + y^2$')
        ax.set_aspect('equal')
        plt.show()

---

**Exercise 2.**
Plot contour lines for $z = \sin(x) \cdot \cos(y)$ and add labels only to specific levels $[-0.5, 0, 0.5]$ by passing the `levels` parameter to `contour` and then labeling. Style the labels with `fontsize=12`, a white background (`colors='white'`), and `inline_spacing=5`.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-np.pi, np.pi, 200)
        y = np.linspace(-np.pi, np.pi, 200)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)

        fig, ax = plt.subplots(figsize=(8, 6))
        cs = ax.contour(X, Y, Z, levels=[-0.5, 0, 0.5])
        ax.clabel(cs, inline=True, fontsize=12, inline_spacing=5)
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(r'Contour Labels at Selected Levels')
        ax.set_aspect('equal')
        plt.show()

---

**Exercise 3.**
Create a contour plot of the 2D Gaussian $z = e^{-(x^2 + y^2)/2}$ with manually chosen levels `[0.1, 0.3, 0.5, 0.7, 0.9]`. Add labels with a custom format function that displays each level as a percentage (e.g., "10%", "30%"). Use `manual` label placement by specifying explicit (x, y) positions for each label.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 200)
        y = np.linspace(-3, 3, 200)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 + Y**2) / 2)

        levels = [0.1, 0.3, 0.5, 0.7, 0.9]

        fig, ax = plt.subplots(figsize=(8, 6))
        cs = ax.contour(X, Y, Z, levels=levels)

        fmt = {lev: f'{lev*100:.0f}%' for lev in levels}
        manual_positions = [(2.0, 0), (1.3, 0), (0.9, 0), (0.5, 0), (0.2, 0)]
        ax.clabel(cs, inline=True, fontsize=11, fmt=fmt, manual=manual_positions)

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('2D Gaussian with Percentage Labels')
        ax.set_aspect('equal')
        plt.show()
