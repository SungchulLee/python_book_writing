# Grid and Axis

Configure grid lines and axis behavior for clearer visualizations.

!!! tip "Mental Model"
    Grid lines are faint reference lines aligned with tick marks that help readers trace values from data points back to the axes. `ax.grid(True)` adds them, and the `which`, `axis`, and `linestyle` parameters let you control major vs. minor grids, x vs. y, and their visual weight. Subtle grids improve readability; heavy grids create clutter.

---

## Basic Grid

Enable grid lines:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.grid()
plt.show()
```

Disable grid:

```python
ax.grid(visible=False)
```

---

## Grid Styling

Customize grid appearance:

```python
ax.grid(True, linestyle='--', alpha=0.7)
```

Full customization:

```python
ax.grid(
    visible=True,
    which='major',      # 'major', 'minor', or 'both'
    axis='both',        # 'x', 'y', or 'both'
    color='gray',
    linestyle='-',
    linewidth=0.5,
    alpha=0.7
)
```

---

## Major and Minor Grids

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

# Enable minor ticks
ax.minorticks_on()

# Style grids separately
ax.grid(which='major', color='gray', linestyle='-')
ax.grid(which='minor', color='lightgray', linestyle=':')

plt.show()
```

---

## Axis Scaling

Set axis scale type:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 100, 100)
y = x ** 2

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xscale('log')
ax.set_yscale('linear')  # Options: 'linear', 'log', 'symlog', 'logit'
plt.show()
```

Or use `plt.axes()` with scale:

```python
fig = plt.figure()
ax = plt.axes(yscale='log')
ax.plot(x, y)
```

---

## axis() Method

Control multiple axis properties:

**Tight bounds:**
```python
import matplotlib.pyplot as plt
import numpy as np

i = complex(0, 1)
theta = np.linspace(0, 2*np.pi, 100)
z = np.exp(i * theta)
x = np.real(z)
y = np.imag(z)

fig, ax = plt.subplots(figsize=(3, 3))
ax.plot(x, y)
ax.axis('tight')  # Tight bounds around data
plt.show()
```

**Equal aspect ratio:**
```python
fig, ax = plt.subplots(figsize=(3, 3))
ax.plot(x, y)
ax.axis('equal')  # Equal scaling for x and y
plt.show()
```

**Turn off axis:**
```python
fig, ax = plt.subplots(figsize=(3, 3))
ax.plot(x, y)
ax.axis('equal')
ax.axis('off')  # Hide all axis elements
plt.show()
```

---

## axis() Options Summary

| Option | Description |
|--------|-------------|
| `'on'` | Turn axis lines and labels on |
| `'off'` | Turn axis lines and labels off |
| `'equal'` | Equal scaling on both axes |
| `'scaled'` | Equal scaling, adjust limits |
| `'tight'` | Tight limits around data |
| `'auto'` | Automatic limits |
| `'square'` | Square aspect ratio |
| `'image'` | Equal with tight limits |

You can also set limits directly:

```python
ax.axis([xmin, xmax, ymin, ymax])
```

---

## Aspect Ratio

Control the aspect ratio directly:

```python
ax.set_aspect('equal')    # Equal scaling
ax.set_aspect(2.0)        # y-axis is 2x scale of x-axis
ax.set_aspect('auto')     # Automatic (default)
```

---

## Box Aspect

Set the physical box aspect ratio:

```python
ax.set_box_aspect(1)      # Square box
ax.set_box_aspect(0.5)    # Wide box
```

---

## Complete Example

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(x, y)

# Grid
ax.minorticks_on()
ax.grid(which='major', color='#666666', linestyle='-', linewidth=0.8)
ax.grid(which='minor', color='#999999', linestyle=':', linewidth=0.5, alpha=0.5)

# Set limits
ax.set_xlim(-2.5*np.pi, 2.5*np.pi)
ax.set_ylim(-1.5, 1.5)

# Labels
ax.set_xlabel('x')
ax.set_ylabel('sin(x)')
ax.set_title('Sine Wave with Grid')

plt.show()
```

---

## Key Takeaways

- `ax.grid()` enables/disables grid lines
- Use `which='major'` or `which='minor'` for different grid levels
- `ax.minorticks_on()` enables minor ticks
- `ax.set_xscale()` and `ax.set_yscale()` set axis scaling
- `ax.axis()` provides quick access to common configurations
- `ax.set_aspect()` controls the aspect ratio

---

## Exercises

**Exercise 1.**
Create a plot of `y = sin(x)` and configure the grid with major grid lines (solid, alpha=0.5) and minor grid lines (dashed, alpha=0.2). Enable minor ticks using `ax.minorticks_on()` and apply grid to both major and minor ticks.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 4 * np.pi, 500)
        y = np.sin(x)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, color='steelblue', linewidth=2)

        ax.minorticks_on()
        ax.grid(which='major', linestyle='-', alpha=0.5)
        ax.grid(which='minor', linestyle='--', alpha=0.2)

        ax.set_title('Major and Minor Grid Lines')
        plt.show()

---

**Exercise 2.**
Create a 2x2 subplot grid demonstrating four different grid configurations: (1) no grid, (2) only x-axis grid, (3) only y-axis grid, (4) both axes with different styles. Plot the same sine wave in each.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)
        y = np.sin(x)

        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        axes[0, 0].plot(x, y)
        axes[0, 0].set_title('No Grid')

        axes[0, 1].plot(x, y)
        axes[0, 1].grid(axis='x', alpha=0.5)
        axes[0, 1].set_title('X Grid Only')

        axes[1, 0].plot(x, y)
        axes[1, 0].grid(axis='y', alpha=0.5)
        axes[1, 0].set_title('Y Grid Only')

        axes[1, 1].plot(x, y)
        axes[1, 1].grid(axis='x', color='blue', linestyle='--', alpha=0.3)
        axes[1, 1].grid(axis='y', color='red', linestyle=':', alpha=0.3)
        axes[1, 1].set_title('Both Axes, Different Styles')

        plt.tight_layout()
        plt.show()

---

**Exercise 3.**
Plot `y = exp(x)` for `x` in $[0, 5]$ and turn off the top and right axis lines using `ax.spines`. Show grid lines only on the y-axis with a log scale. Customize the grid color to light blue and set `ax.set_axisbelow(True)` so grid lines appear behind the data.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 5, 200)
        y = np.exp(x)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x, y, color='darkred', linewidth=2)
        ax.set_yscale('log')

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        ax.grid(axis='y', color='lightblue', linestyle='-', alpha=0.7)
        ax.set_axisbelow(True)

        ax.set_xlabel('x')
        ax.set_ylabel('exp(x)')
        ax.set_title('Exponential with Log Scale Grid')
        plt.show()
