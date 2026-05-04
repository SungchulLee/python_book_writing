# add_subplot vs subplots

!!! tip "Mental Model"
    `fig.add_subplot()` builds a grid one cell at a time -- useful when subplots are added conditionally or in a loop. `plt.subplots()` builds the entire grid in one call and returns all Axes at once -- simpler for fixed layouts.

    **Default choice: `plt.subplots()`.** Switch to `add_subplot` only when the
    layout is built dynamically (e.g., number of panels determined at runtime) or
    when panels have irregular sizes that require GridSpec.

## Overview

Matplotlib provides two main ways to create axes within a figure:

| Method | Style | Returns |
|--------|-------|---------|
| `fig.add_subplot()` | OOP, incremental | Single Axes |
| `plt.subplots()` | Convenience function | Figure + Axes array |

---

## plt.subplots()

### Basic Usage

Creates figure and all axes at once:

```python
import matplotlib.pyplot as plt

# Single axes
fig, ax = plt.subplots()
ax.plot([1, 2, 3])

# Multiple axes (2 rows, 3 cols)
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
```

### Return Value

```python
# 1x1: ax is single Axes object
fig, ax = plt.subplots()

# 1xN or Nx1: axes is 1D array
fig, axes = plt.subplots(1, 3)  # shape: (3,)
fig, axes = plt.subplots(3, 1)  # shape: (3,)

# NxM: axes is 2D array
fig, axes = plt.subplots(2, 3)  # shape: (2, 3)
```

### Accessing Axes

```python
fig, axes = plt.subplots(2, 3)

# 2D indexing
axes[0, 0].plot(...)  # Top-left
axes[1, 2].plot(...)  # Bottom-right

# Flatten for iteration
for ax in axes.flat:
    ax.grid(True)

# Unpack if known size
fig, (ax1, ax2) = plt.subplots(1, 2)
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
```

### Common Parameters

```python
fig, axes = plt.subplots(
    nrows=2, 
    ncols=3,
    figsize=(12, 8),
    sharex=True,      # Share x-axis
    sharey=True,      # Share y-axis
    squeeze=False,    # Always return 2D array
    gridspec_kw={'hspace': 0.3, 'wspace': 0.2}
)
```

---

## fig.add_subplot()

### Basic Usage

Adds one axes at a time to an existing figure:

```python
fig = plt.figure(figsize=(12, 8))

# Add subplot at position (row, col, index) - 1-indexed
ax1 = fig.add_subplot(2, 3, 1)  # Row 1, Col 1
ax2 = fig.add_subplot(2, 3, 2)  # Row 1, Col 2
ax3 = fig.add_subplot(2, 3, 4)  # Row 2, Col 1
```

### Compact Notation

```python
# Three-digit shorthand (only for grids < 10x10)
ax1 = fig.add_subplot(231)  # Same as (2, 3, 1)
ax2 = fig.add_subplot(232)  # Same as (2, 3, 2)
```

### Non-Uniform Grids

```python
fig = plt.figure(figsize=(10, 8))

# Large subplot spanning multiple positions
ax1 = fig.add_subplot(2, 2, 1)  # Top-left quarter
ax2 = fig.add_subplot(2, 2, 2)  # Top-right quarter
ax3 = fig.add_subplot(2, 1, 2)  # Bottom half (spans both columns)
```

### With GridSpec

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 8))
gs = GridSpec(3, 3, figure=fig)

ax1 = fig.add_subplot(gs[0, :])    # Top row, all columns
ax2 = fig.add_subplot(gs[1:, 0])   # Left column, rows 1-2
ax3 = fig.add_subplot(gs[1:, 1:])  # Bottom-right 2x2
```

---

## Comparison

### When to Use plt.subplots()

✅ **Use when**:
- Creating regular grid of subplots
- All subplots needed at once
- Want shared axes
- Simple layouts

```python
# Perfect for regular grids
fig, axes = plt.subplots(2, 3)
for ax, data in zip(axes.flat, datasets):
    ax.plot(data)
```

### When to Use fig.add_subplot()

✅ **Use when**:
- Non-uniform subplot sizes
- Adding subplots incrementally
- Complex layouts with GridSpec
- Mixing different subplot sizes

```python
# Perfect for irregular layouts
fig = plt.figure()
ax_main = fig.add_subplot(2, 2, (1, 2))  # Top half
ax_left = fig.add_subplot(2, 2, 3)        # Bottom-left
ax_right = fig.add_subplot(2, 2, 4)       # Bottom-right
```

---

## Side-by-Side Examples

### Regular 2x2 Grid

```python
# plt.subplots (preferred)
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].plot(x, y1)
axes[0, 1].plot(x, y2)
axes[1, 0].plot(x, y3)
axes[1, 1].plot(x, y4)

# fig.add_subplot
fig = plt.figure(figsize=(10, 8))
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
ax1.plot(x, y1)
ax2.plot(x, y2)
ax3.plot(x, y3)
ax4.plot(x, y4)
```

### Main Plot with Side Plots

```python
# Using add_subplot with GridSpec
fig = plt.figure(figsize=(10, 8))
gs = GridSpec(2, 2, width_ratios=[3, 1], height_ratios=[1, 3])

ax_main = fig.add_subplot(gs[1, 0])    # Main scatter plot
ax_top = fig.add_subplot(gs[0, 0])     # Top histogram
ax_right = fig.add_subplot(gs[1, 1])   # Right histogram

ax_main.scatter(x, y)
ax_top.hist(x, bins=30)
ax_right.hist(y, bins=30, orientation='horizontal')
```

---

## Common Patterns

### Iterate Over Subplots

```python
# With subplots
fig, axes = plt.subplots(2, 3)
for ax, (title, data) in zip(axes.flat, datasets.items()):
    ax.plot(data)
    ax.set_title(title)

# With add_subplot
fig = plt.figure()
for i, (title, data) in enumerate(datasets.items(), 1):
    ax = fig.add_subplot(2, 3, i)
    ax.plot(data)
    ax.set_title(title)
```

### Shared Axes

```python
# Easy with subplots
fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)

# Manual with add_subplot
fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222, sharex=ax1, sharey=ax1)
ax3 = fig.add_subplot(223, sharex=ax1, sharey=ax1)
ax4 = fig.add_subplot(224, sharex=ax1, sharey=ax1)
```

---

## Summary

| Feature | `plt.subplots()` | `fig.add_subplot()` |
|---------|------------------|---------------------|
| Create multiple at once | ✅ Yes | ❌ One at a time |
| Regular grids | ✅ Ideal | Works |
| Irregular layouts | Limited | ✅ Ideal |
| Shared axes | ✅ Easy (`sharex`, `sharey`) | Manual |
| Return value | Figure + Axes array | Single Axes |
| GridSpec integration | Via `gridspec_kw` | ✅ Direct |

**Recommendation**:

- Start with `plt.subplots()` for most cases
- Use `fig.add_subplot()` + GridSpec for complex layouts

---

## Exercises

**Exercise 1.**
Create a figure using `fig.add_subplot()` to add three subplots in a single row (1x3 layout). In each subplot, plot a different trigonometric function (`sin`, `cos`, `tan`) over $[0, 2\pi]$. Add titles to each subplot.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig = plt.figure(figsize=(12, 4))

        ax1 = fig.add_subplot(1, 3, 1)
        ax1.plot(x, np.sin(x))
        ax1.set_title('sin(x)')

        ax2 = fig.add_subplot(1, 3, 2)
        ax2.plot(x, np.cos(x))
        ax2.set_title('cos(x)')

        ax3 = fig.add_subplot(1, 3, 3)
        ax3.plot(x, np.tan(x))
        ax3.set_ylim(-5, 5)
        ax3.set_title('tan(x)')

        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Recreate the same 1x3 layout from Exercise 1 using `plt.subplots(1, 3)` instead. Compare how you access the axes objects versus the `add_subplot` approach. Add a shared y-label using `fig.supylabel()`.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig, axes = plt.subplots(1, 3, figsize=(12, 4))

        axes[0].plot(x, np.sin(x))
        axes[0].set_title('sin(x)')

        axes[1].plot(x, np.cos(x))
        axes[1].set_title('cos(x)')

        axes[2].plot(x, np.tan(x))
        axes[2].set_ylim(-5, 5)
        axes[2].set_title('tan(x)')

        fig.supylabel('y')
        plt.tight_layout()
        plt.show()

---

**Exercise 3.**
Create a figure where you mix both approaches: use `plt.subplots(2, 2)` for a 2x2 grid, remove the bottom-right subplot with `fig.delaxes()`, and then use `fig.add_subplot()` to add a wide subplot spanning the entire bottom row using `fig.add_subplot(2, 1, 2)`. Plot different data in each subplot.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        axes[0, 0].plot(x, np.sin(x), color='blue')
        axes[0, 0].set_title('sin(x)')

        axes[0, 1].plot(x, np.cos(x), color='red')
        axes[0, 1].set_title('cos(x)')

        axes[1, 0].plot(x, np.exp(-x), color='green')
        axes[1, 0].set_title('exp(-x)')

        fig.delaxes(axes[1, 1])

        ax_bottom = fig.add_subplot(2, 1, 2)
        ax_bottom.plot(x, np.sin(x) * np.cos(x), color='purple', linewidth=2)
        ax_bottom.set_title('sin(x) * cos(x)')

        plt.tight_layout()
        plt.show()
