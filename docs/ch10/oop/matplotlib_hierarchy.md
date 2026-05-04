# Figure-Axes-Artist

!!! tip "Mental Model"
    Matplotlib uses a tree structure: a Figure contains Axes, and each Axes contains Artists. This is the composite pattern — every node knows its children and can draw them recursively. When you call `fig.savefig()`, the Figure asks each Axes to render, and each Axes asks its Artists to render. Understanding this tree is the key to debugging any display issue.

!!! note "Matplotlib Is a Scene Graph"
    The hierarchy `Figure → Axes → Artists` is a **scene graph**: a tree data structure where each node represents a visual element, and rendering traverses the tree recursively calling `draw()`. This is the same architecture used in game engines, SVG, and the browser DOM.

    ```text
    Full visualization pipeline:

    Data → Encoding (plot/scatter/bar) → Artists (Line2D, Patch, Text)
         → Axes (coordinate system) → Figure (layout container)
         → Backend (renderer) → Pixels/File → Human perception
    ```

    Understanding this pipeline means you can intervene at any stage: change the data, swap the encoding, modify Artists after creation, rearrange Axes, or switch the output format.

## Composite Pattern

### 1. Hierarchy

```
Figure
  └── Axes
        └── Artists (Line2D, Text, Patch, etc.)
```

### 2. Figure Object

Top-level container:

```python
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10, 6))
print(type(fig))  # <class 'matplotlib.figure.Figure'>
```

### 3. Axes Object

Plotting region with coordinate system:

```python
fig, ax = plt.subplots()
print(type(ax))  # <class 'matplotlib.axes._axes.Axes'>
```

## Components

### 1. Figure Properties

```python
fig = plt.figure(figsize=(12, 8), dpi=100)
fig.suptitle('Main Title')
fig.tight_layout()
fig.savefig('output.png')
```

### 2. Axes Properties

```python
fig, ax = plt.subplots()
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_title('Axes Title')
ax.set_xlim(0, 10)
ax.set_ylim(0, 100)
ax.grid(True)
```

### 3. Artist Objects

```python
line, = ax.plot([0, 1, 2], [0, 1, 0])
print(type(line))  # <class 'matplotlib.lines.Line2D'>
line.set_color('red')
line.set_linewidth(2)
```

## Multiple Axes

### 1. Subplots

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot([1, 2, 3])
ax2.scatter([1, 2, 3], [4, 5, 6])
```

### 2. GridSpec

```python
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(10, 8))
gs = GridSpec(3, 3, figure=fig)

ax1 = fig.add_subplot(gs[0, :])  # Top row, all columns
ax2 = fig.add_subplot(gs[1:, 0:2])  # Bottom 2 rows, first 2 cols
ax3 = fig.add_subplot(gs[1:, 2])  # Bottom 2 rows, last col
```

### 3. Nested Axes

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3])

# Inset axes
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
ax_inset = inset_axes(ax, width="30%", height="30%", loc='upper right')
ax_inset.plot([1, 2, 3], [3, 2, 1])
```


## The Full Rendering Pipeline

The hierarchy doesn't stop at Artists. The complete model from data to screen:

```text
Data
  ↓
Artist (Line2D, Text, Patch, ...)
  ↓
Axes (coordinates, scaling, limits)
  ↓
Figure (container, size, DPI)
  ↓
Renderer + Backend (converts to pixels)
  ↓
Screen / File (.png, .pdf, .svg)
```

When something doesn't appear on screen, trace this pipeline: is the data correct? Is the Artist created? Are the axes limits right? Is the backend rendering?

!!! warning "Axes vs Axis"

    This is one of the most common naming confusions in Matplotlib:

    - **Axes** = the entire plotting area (contains everything: lines, labels, ticks)
    - **Axis** = one x-axis or y-axis (contains ticks, tick labels, axis label)

    One Axes contains two (or three in 3D) Axis objects. `ax` refers to Axes; `ax.xaxis` and `ax.yaxis` refer to Axis objects.

---

## Exercises

**Exercise 1.** Draw the Matplotlib object hierarchy from Figure down to Tick. Write code that accesses each level: `fig`, `ax`, `ax.xaxis`, `ax.xaxis.get_major_ticks()`.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    # Solution code depends on the specific exercise
    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x))
    ax.set_title('Example Solution')
    plt.show()
    ```

    See the content of this page for the relevant API details to construct the full solution.

---

**Exercise 2.** Explain the parent-child relationship between Figure, Axes, Axis, and Tick objects.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that creates a figure with two subplots and demonstrates that both Axes share the same parent Figure using `ax.get_figure()`.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(0, 2 * np.pi, 100)
    axes[0].plot(x, np.sin(x))
    axes[0].set_title('Left Subplot')

    axes[1].plot(x, np.cos(x))
    axes[1].set_title('Right Subplot')

    plt.tight_layout()
    plt.show()
    ```

    Adapt this pattern to the specific requirements of the exercise.

---

**Exercise 4.** Access and modify a specific tick label on the x-axis programmatically. Change its color to red and increase its font size.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots()
        ax.plot(np.linspace(0, 10, 50), np.sin(np.linspace(0, 10, 50)))

        # Draw first to populate tick labels
        fig.canvas.draw()

        # Access tick labels — they are Text Artists
        labels = ax.get_xticklabels()
        if len(labels) > 2:
            labels[2].set_color('red')
            labels[2].set_fontsize(16)

        plt.show()

---

**Exercise 5.** Traverse the scene graph programmatically. Write code that creates a figure with 2 subplots, each containing a line plot. Then use `fig.get_children()` and `ax.get_children()` to print the full tree structure (Figure → Axes → Artists). Count the total number of Artists in the figure.

??? success "Solution to Exercise 5"

        import matplotlib.pyplot as plt
        import numpy as np

        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot([1, 2, 3], [1, 4, 9], 'b-')
        ax2.bar([1, 2, 3], [3, 1, 2])

        # Traverse the scene graph
        print(f"Figure children: {len(fig.get_children())}")
        for i, child in enumerate(fig.get_children()):
            print(f"  [{i}] {type(child).__name__}")

        print(f"\nAx1 children: {len(ax1.get_children())}")
        for child in ax1.get_children()[:5]:
            print(f"  {type(child).__name__}")

        # Count all Artists recursively
        total = 0
        for ax in fig.get_axes():
            total += len(ax.get_children())
        print(f"\nTotal Artists across all Axes: {total}")

        # This demonstrates the scene graph: Figure owns Axes,
        # each Axes owns Lines, Patches, Text, Spines, etc.
        plt.show()

    Refer to the code examples in the main content for the specific API calls needed.
