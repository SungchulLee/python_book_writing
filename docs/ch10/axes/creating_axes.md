# Creating Axes

There are multiple ways to create Axes objects in Matplotlib, each suited for different use cases.

!!! tip "Mental Model"
    Creating an Axes means carving out a rectangular region on the Figure for plotting. `plt.subplots()` carves a regular grid, `fig.add_axes()` places a rectangle at exact coordinates, and `GridSpec` offers the most flexible partitioning. Every approach ultimately produces the same Axes object -- they differ only in how they specify position and size.

    **In practice, the methods are not equally common:**

    - **~90% of plots** → `plt.subplots()` (regular grid, covers most use cases)
    - **~9%** → `fig.add_subplot()` (build incrementally, mixed layouts)
    - **~1%** → `fig.add_axes()` / `GridSpec` (pixel-precise or irregular layouts)

    Start with `subplots()` and reach for the others only when it cannot express
    your layout.

---

## plt.subplots

The most common method for creating figures with axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
```

With multiple subplots:

```python
fig, axes = plt.subplots(2, 2, figsize=(8, 6))
```

---

## plt.axes

Create axes on the current figure:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.exp(x)

fig = plt.figure()
ax = plt.axes()
ax.plot(x, y)
plt.show()
```

With scale options:

```python
fig = plt.figure()
ax = plt.axes(yscale='log')  # Logarithmic y-axis
ax.plot(x, y)
plt.show()
```

---

## fig.add_axes

For precise positioning using normalized coordinates:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 3, 50)
y1 = x ** 2
y2 = np.sqrt(x)

fig = plt.figure()

# [left, bottom, width, height] - values from 0 to 1
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.plot(x, y1)

plt.show()
```

---

## fig.add_subplot

Add subplots one at a time:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 50)

fig = plt.figure(figsize=(12, 6))

for s in range(12):
    ax = fig.add_subplot(3, 4, s + 1)
    ax.plot(x ** (s + 1))
    ax.set_title(f"x^{s+1}")

plt.tight_layout()
plt.show()
```

---

## plt.subplot2grid

Create subplots with varying sizes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 3, 50)
y1 = x ** 2
y2 = np.sqrt(x)

fig = plt.figure()

ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
ax3 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
ax4 = plt.subplot2grid((3, 3), (2, 0))
ax5 = plt.subplot2grid((3, 3), (2, 1))

ax1.plot(x, y1)
ax2.plot(y1, x)
ax3.plot(x, y1)
ax4.plot(x, y2)
ax5.plot(y2, x)

fig.tight_layout()
plt.show()
```

Parameters:

- First tuple: grid shape `(nrows, ncols)`
- Second tuple: starting position `(row, col)`
- `colspan`: columns to span
- `rowspan`: rows to span

---

## GridSpec

For maximum control over subplot layout:

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

x = np.linspace(0, 3, 50)
y1 = x ** 2
y2 = np.sqrt(x)

fig = plt.figure()
gs = gridspec.GridSpec(2, 3, height_ratios=[2, 1], width_ratios=[1, 2, 1])

for i, g in enumerate(gs):
    ax = fig.add_subplot(g)
    if i % 2 == 0:
        ax.plot(x, y1)
    else:
        ax.plot(x, y2)

fig.tight_layout()
plt.show()
```

---

## Inset Axes

Create axes within axes for detail views:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 3, 50)
y1 = x ** 2
y2 = np.sqrt(x)

fig = plt.figure()

ax0 = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # Main axes
ax1 = fig.add_axes([0.2, 0.5, 0.4, 0.3])  # Inset axes

ax0.plot(x, y1)
ax1.plot(y1, x)

plt.show()
```

---

## Pandas Integration

Pandas can plot directly to a specified axes:

```python
import matplotlib.pyplot as plt
import yfinance as yf

ticker = 'AAPL'
df = yf.Ticker(ticker).history(start='2020-01-01', end='2020-12-31')

fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

df.Close.plot(ax=axes[0])
df.Volume.plot(ax=axes[1])

plt.show()
```

---

## Comparison Summary

| Method | Best For |
|--------|----------|
| `plt.subplots` | Regular grids, most common |
| `plt.axes` | Quick single axes |
| `fig.add_axes` | Precise positioning |
| `fig.add_subplot` | Adding axes dynamically |
| `plt.subplot2grid` | Spanning rows/columns |
| `GridSpec` | Complex custom layouts |

---

## Key Takeaways

- `plt.subplots` is the workhorse for most plots
- Use `fig.add_axes` for precise control
- `subplot2grid` and `GridSpec` handle complex layouts
- Inset axes are created with multiple `add_axes` calls
- Pandas plotting integrates via the `ax` parameter

---

## Exercises

**Exercise 1.**
Create a figure and add three axes using three different methods: `fig.add_subplot(1, 3, 1)`, `fig.add_axes([0.4, 0.15, 0.25, 0.7])` for the second, and `plt.subplots` for the third. Plot a different function on each.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig = plt.figure(figsize=(12, 4))

        ax1 = fig.add_subplot(1, 3, 1)
        ax1.plot(x, np.sin(x))
        ax1.set_title('add_subplot')

        ax2 = fig.add_axes([0.4, 0.15, 0.25, 0.7])
        ax2.plot(x, np.cos(x), color='red')
        ax2.set_title('add_axes')

        ax3 = fig.add_subplot(1, 3, 3)
        ax3.plot(x, np.tan(x), color='green')
        ax3.set_ylim(-5, 5)
        ax3.set_title('add_subplot again')

        plt.show()

---

**Exercise 2.**
Create an inset axes inside a main plot. Plot `y = sin(x)` on the main axes over $[0, 4\pi]$, and add a small inset axes using `fig.add_axes([0.55, 0.55, 0.3, 0.3])` that zooms into the region $[0, \pi]$.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 4 * np.pi, 500)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, np.sin(x), color='steelblue')
        ax.set_title('sin(x) with Inset Zoom')
        ax.set_xlabel('x')
        ax.set_ylabel('y')

        ax_inset = fig.add_axes([0.55, 0.55, 0.3, 0.3])
        x_zoom = np.linspace(0, np.pi, 200)
        ax_inset.plot(x_zoom, np.sin(x_zoom), color='red')
        ax_inset.set_title('Zoom: [0, π]', fontsize=9)
        ax_inset.set_xlim(0, np.pi)

        plt.show()

---

**Exercise 3.**
Use `fig.add_subplot` to create an irregular layout: one tall subplot on the left spanning 2 rows (`fig.add_subplot(1, 2, 1)`) and two small subplots stacked on the right (`fig.add_subplot(2, 2, 2)` and `fig.add_subplot(2, 2, 4)`). Plot different data in each.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig = plt.figure(figsize=(10, 6))

        ax_left = fig.add_subplot(1, 2, 1)
        ax_left.plot(x, np.sin(x), color='blue', linewidth=2)
        ax_left.set_title('Tall Left Subplot')

        ax_top_right = fig.add_subplot(2, 2, 2)
        ax_top_right.bar(['A', 'B', 'C'], [3, 7, 5], color='coral')
        ax_top_right.set_title('Top Right')

        ax_bottom_right = fig.add_subplot(2, 2, 4)
        ax_bottom_right.scatter(np.random.rand(20), np.random.rand(20), color='green')
        ax_bottom_right.set_title('Bottom Right')

        plt.tight_layout()
        plt.show()
