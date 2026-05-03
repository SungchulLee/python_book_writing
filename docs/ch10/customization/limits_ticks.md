# Limits and Ticks

Control the visible range and tick positions on your axes.

!!! tip "Mental Model"
    Limits define the viewport window (what range of data is visible) and ticks define the ruler marks within that window. `set_xlim`/`set_ylim` zoom or pan the view, while `set_xticks`/`set_yticks` place marks at specific values. Matplotlib auto-picks reasonable defaults, but manual control is essential for publication-quality figures.

!!! note "The Axes System (applies to all customization pages)"

    Every plot answers six questions. Each customization page in this section addresses one:

    | Question | Control | Page |
    |---|---|---|
    | What is visible? | `set_xlim`, `set_ylim` | This page |
    | How is it measured? | `set_xticks`, `set_yticks` | This page |
    | How is it labeled? | `set_xticklabels`, rotation | [Tick Labels](tick_labels.md) |
    | How is it guided? | `ax.grid()` | [Grid](grid_axis.md) |
    | How is it scaled? | `set_xscale('log')` | [Log Scales](log_scales.md) |
    | What does it mean? | `set_title`, `set_xlabel` | [Title & Labels](title_labels.md) |

---

## Setting Axis Limits

Use `set_xlim` and `set_ylim`:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.set_xlim((-3*np.pi, 3*np.pi))
ax.set_ylim((-2, 2))
plt.show()
```

---

## Getting Current Limits

```python
print(ax.get_xlim())  # Returns tuple: (-9.42..., 9.42...)
print(ax.get_ylim())  # Returns tuple: (-2.0, 2.0)
```

---

## Setting Ticks

Use `set_xticks` and `set_yticks`:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.set_yticks(ticks=[-1, 0, 1])
ax.set_xticks(ticks=[-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
plt.show()
```

---

## Removing Ticks

Pass an empty tuple to remove all ticks:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.set_xticks(())
ax.set_yticks(())
plt.show()
```

---

## Tick Labels

Set custom labels with the `labels` parameter:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.set_yticks(ticks=[-1, 0, 1])
ax.set_xticks(
    ticks=[-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
    labels=["$-2\\pi$", "$-\\pi$", "0", "$\\pi$", "$2\\pi$"]
)
plt.show()
```

---

## Minor Ticks

Add minor ticks with `minor=True`:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)

# Major ticks
ax.set_yticks(ticks=[-1, 0, 1])
ax.set_xticks(
    ticks=[-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
    labels=["$-2\\pi$", "$-\\pi$", "0", "$\\pi$", "$2\\pi$"]
)

# Minor ticks (no labels)
ax.set_xticks(
    ticks=np.linspace(-2*np.pi, 2*np.pi, 17),
    labels=[],
    minor=True
)

plt.show()
```

---

## Getting Current Ticks

```python
print(ax.get_xticks())
print(ax.get_yticks())
```

---

## Complete Example with Spines

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)

# Set ticks and labels
ax.set_yticks(ticks=[-1, 0, 1])
ax.set_xticks(
    ticks=[-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
    labels=["$-2\\pi$", "$-\\pi$", "0", "$\\pi$", "$2\\pi$"]
)
ax.set_xticks(
    ticks=np.linspace(-2*np.pi, 2*np.pi, 17),
    labels=[],
    minor=True
)

# Move spines to origin
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')

plt.show()
```

---

## tick_params

Fine-tune tick appearance:

```python
ax.tick_params(
    axis='both',      # 'x', 'y', or 'both'
    which='major',    # 'major', 'minor', or 'both'
    direction='out',  # 'in', 'out', or 'inout'
    length=6,         # Tick length
    width=2,          # Tick width
    labelsize=10,     # Label font size
    rotation=45,      # Label rotation
    colors='blue'     # Tick and label color
)
```

---

## Key Takeaways

- `set_xlim()` and `set_ylim()` control visible range
- `set_xticks()` and `set_yticks()` set tick positions
- Use `labels` parameter for custom tick labels
- Use `minor=True` for minor ticks
- `tick_params()` provides fine-grained control
- Empty tuple `()` removes all ticks

---

## Runnable Example: `advanced_customization_tutorial.py`

```python
"""
Matplotlib Tutorial - Intermediate Level
========================================
Topic: Advanced Plot Customization and Styling
Author: Educational Python Course
Level: Intermediate

Learning Objectives:
-------------------
1. Master axes limits and ticks customization
2. Understand different coordinate systems
3. Add annotations and text
4. Customize grids and spines
5. Control legend appearance and positioning
6. Use colormaps effectively
7. Create publication-quality figures

Prerequisites:
-------------
- Completion of beginner tutorials
- Completion of plot() and hist() guides
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# SECTION 1: Customizing Axes Limits
# ============================================================================

if __name__ == "__main__":

    """
    Controlling what portion of data is visible
    """

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Default limits (automatic)
    axes[0, 0].plot(x, y)
    axes[0, 0].set_title('Default limits (automatic)')
    axes[0, 0].grid(True, alpha=0.3)

    # Custom x-limits only
    axes[0, 1].plot(x, y)
    axes[0, 1].set_xlim(2, 8)  # Show only x from 2 to 8
    axes[0, 1].set_title('Custom xlim(2, 8)')
    axes[0, 1].grid(True, alpha=0.3)

    # Custom y-limits only
    axes[1, 0].plot(x, y)
    axes[1, 0].set_ylim(-2, 2)  # Extend y-axis range
    axes[1, 0].set_title('Custom ylim(-2, 2)')
    axes[1, 0].grid(True, alpha=0.3)

    # Both custom limits
    axes[1, 1].plot(x, y)
    axes[1, 1].set_xlim(3, 7)
    axes[1, 1].set_ylim(-0.5, 0.5)
    axes[1, 1].set_title('Custom xlim and ylim')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 2: Customizing Ticks and Tick Labels
    # ============================================================================

    """
    Ticks are the marks on the axes.
    Tick labels are the text at each tick.
    """

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Default ticks
    axes[0, 0].plot(x, y)
    axes[0, 0].set_title('Default ticks')
    axes[0, 0].grid(True, alpha=0.3)

    # Custom tick positions
    axes[0, 1].plot(x, y)
    axes[0, 1].set_xticks([0, 2, 4, 6, 8, 10])  # Specific positions
    axes[0, 1].set_yticks([-1, -0.5, 0, 0.5, 1])
    axes[0, 1].set_title('Custom tick positions')
    axes[0, 1].grid(True, alpha=0.3)

    # Custom tick labels (different from positions)
    axes[1, 0].plot(x, y)
    axes[1, 0].set_xticks([0, np.pi, 2*np.pi, 3*np.pi])
    axes[1, 0].set_xticklabels(['0', 'π', '2π', '3π'])
    axes[1, 0].set_title('Custom tick labels')
    axes[1, 0].grid(True, alpha=0.3)

    # Rotated and formatted labels
    axes[1, 1].plot(x, y)
    axes[1, 1].set_xticks(np.arange(0, 11, 1))
    axes[1, 1].set_xticklabels([f'x={i}' for i in range(11)], rotation=45, ha='right')
    axes[1, 1].set_title('Rotated tick labels')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 3: Grid Customization
    # ============================================================================

    """
    Grids help read values from plots
    """

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    # No grid
    axes[0, 0].plot(x, y)
    axes[0, 0].set_title('No grid')

    # Basic grid
    axes[0, 1].plot(x, y)
    axes[0, 1].grid(True)
    axes[0, 1].set_title('Basic grid')

    # Customized grid (color, style, width)
    axes[0, 2].plot(x, y)
    axes[0, 2].grid(True, color='red', linestyle='--', linewidth=0.5, alpha=0.7)
    axes[0, 2].set_title('Customized grid')

    # Grid only on y-axis
    axes[1, 0].plot(x, y)
    axes[1, 0].grid(True, axis='y', alpha=0.5)
    axes[1, 0].set_title('Grid on y-axis only')

    # Grid with minor ticks
    axes[1, 1].plot(x, y)
    axes[1, 1].minorticks_on()
    axes[1, 1].grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.7)
    axes[1, 1].grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.4)
    axes[1, 1].set_title('Major and minor grids')

    # Grid behind plot
    axes[1, 2].plot(x, y, linewidth=3, zorder=3)  # zorder=3 brings line to front
    axes[1, 2].grid(True, zorder=0, alpha=0.5)  # zorder=0 puts grid in back
    axes[1, 2].set_title('Grid behind line (zorder)')

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 4: Spine Customization
    # ============================================================================

    """
    Spines are the lines connecting the axis tick marks and noting the boundaries of the data area.
    There are 4 spines: 'left', 'right', 'top', 'bottom'
    """

    x = np.linspace(-5, 5, 100)
    y = x ** 2

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # All spines visible (default)
    axes[0, 0].plot(x, y)
    axes[0, 0].set_title('All spines (default)')

    # Hide top and right spines (common for scientific plots)
    axes[0, 1].plot(x, y)
    axes[0, 1].spines['top'].set_visible(False)
    axes[0, 1].spines['right'].set_visible(False)
    axes[0, 1].set_title('Top and right spines hidden')

    # Customize spine position (centered at zero)
    axes[1, 0].plot(x, y)
    axes[1, 0].spines['left'].set_position('zero')  # Move left spine to x=0
    axes[1, 0].spines['bottom'].set_position('zero')  # Move bottom spine to y=0
    axes[1, 0].spines['top'].set_visible(False)
    axes[1, 0].spines['right'].set_visible(False)
    axes[1, 0].set_title('Spines at zero (classic math axes)')

    # Customize spine colors and linewidth
    axes[1, 1].plot(x, y)
    for spine in axes[1, 1].spines.values():
        spine.set_edgecolor('red')
        spine.set_linewidth(2)
    axes[1, 1].set_title('Custom spine color and width')

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 5: Adding Text and Annotations
    # ============================================================================

    """
    Text and annotations help explain features in plots
    """

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(x, y, 'b-', linewidth=2)

    # Simple text at data coordinates
    ax.text(5, 0.5, 'Simple text', fontsize=14)

    # Text with background box
    ax.text(8, -0.5, 'Text with box', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Annotation with arrow pointing to data
    ax.annotate('Local maximum', 
                xy=(np.pi/2, 1),  # Point to annotate
                xytext=(2, 1.3),  # Text position
                fontsize=12,
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

    # Another annotation
    ax.annotate('Zero crossing',
                xy=(np.pi, 0),
                xytext=(4, -0.5),
                fontsize=12,
                arrowprops=dict(arrowstyle='->', color='green', lw=2))

    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('sin(x)', fontsize=14)
    ax.set_title('Adding Text and Annotations', fontsize=16)
    ax.grid(True, alpha=0.3)

    plt.show()

    # ============================================================================
    # SECTION 6: Advanced Legend Customization
    # ============================================================================

    """
    Legends explain what each line/marker represents
    """

    x = np.linspace(0, 10, 100)

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Different legend locations
    for i, loc in enumerate(['upper right', 'upper left', 'lower left', 'best']):
        ax = axes[i // 2, i % 2]
        ax.plot(x, np.sin(x), 'r-', label='sin(x)')
        ax.plot(x, np.cos(x), 'b--', label='cos(x)')
        ax.plot(x, np.sin(2*x), 'g:', label='sin(2x)')
        ax.legend(loc=loc)
        ax.set_title(f"loc='{loc}'")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Highly customized legend
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
    ax.plot(x, np.cos(x), 'b--', linewidth=2, label='cos(x)')
    ax.plot(x, np.tan(x), 'g:', linewidth=2, label='tan(x)')

    ax.legend(
        loc='upper right',
        fontsize=12,
        frameon=True,          # Draw frame
        framealpha=0.9,        # Frame transparency
        shadow=True,           # Add shadow
        fancybox=True,         # Rounded corners
        title='Functions',     # Legend title
        title_fontsize=14
    )

    ax.set_ylim(-3, 3)
    ax.set_title('Customized Legend', fontsize=16)
    ax.grid(True, alpha=0.3)

    plt.show()

    # ============================================================================
    # SECTION 7: Colormaps for Multiple Lines
    # ============================================================================

    """
    When plotting many lines, colormaps provide systematic colors
    """

    x = np.linspace(0, 10, 100)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Manual colors (tedious for many lines)
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for i, color in enumerate(colors):
        axes[0].plot(x, np.sin(x + i*0.5), color=color, label=f'Line {i}')
    axes[0].set_title('Manual colors')
    axes[0].legend()

    # Using colormap (systematic and scalable)
    n_lines = 10
    colormap = plt.cm.viridis  # Choose a colormap
    colors = [colormap(i / n_lines) for i in range(n_lines)]

    for i, color in enumerate(colors):
        axes[1].plot(x, np.sin(x + i*0.3), color=color, label=f'Line {i}')

    axes[1].set_title('Using colormap (viridis)')
    axes[1].legend()

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 8: Figure Size and DPI
    # ============================================================================

    """
    Control figure dimensions and resolution
    """

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Small figure, low DPI
    fig1, ax1 = plt.subplots(figsize=(4, 3), dpi=50)
    ax1.plot(x, y)
    ax1.set_title('4"×3", 50 DPI (looks pixelated)')
    plt.show()

    # Large figure, high DPI
    fig2, ax2 = plt.subplots(figsize=(10, 6), dpi=150)
    ax2.plot(x, y, linewidth=2)
    ax2.set_xlabel('x', fontsize=14)
    ax2.set_ylabel('sin(x)', fontsize=14)
    ax2.set_title('10"×6", 150 DPI (sharp and clear)', fontsize=16)
    ax2.grid(True, alpha=0.3)
    plt.show()

    print("Figure size = (width, height) in inches")
    print("DPI = dots per inch (resolution)")
    print("Pixel dimensions = (width × DPI, height × DPI)")
    print("Example: (10, 6) at 150 DPI = 1500×900 pixels")

    # ============================================================================
    # SECTION 9: Publication-Quality Figure Example
    # ============================================================================

    """
    Combining everything for a professional-looking plot
    """

    # Generate data
    x = np.linspace(0, 10, 200)
    y1 = np.sin(x)
    y2 = np.sin(x) * np.exp(-x/5)
    y3 = np.cos(x) * np.exp(-x/5)

    # Create figure with specific size and DPI
    fig, ax = plt.subplots(figsize=(10, 6), dpi=120)

    # Plot with careful styling
    line1, = ax.plot(x, y1, color='#1f77b4', linestyle='-', linewidth=2.5, 
                     label='sin(x)', alpha=0.9)
    line2, = ax.plot(x, y2, color='#ff7f0e', linestyle='--', linewidth=2.5,
                     label='sin(x)·exp(-x/5)', alpha=0.9)
    line3, = ax.plot(x, y3, color='#2ca02c', linestyle='-.', linewidth=2.5,
                     label='cos(x)·exp(-x/5)', alpha=0.9)

    # Customize axes
    ax.set_xlabel('x', fontsize=14, fontweight='bold')
    ax.set_ylabel('y', fontsize=14, fontweight='bold')
    ax.set_title('Damped Oscillations', fontsize=16, fontweight='bold', pad=20)

    # Set limits
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.2, 1.2)

    # Customize ticks
    ax.tick_params(axis='both', which='major', labelsize=12, length=6, width=1.5)
    ax.minorticks_on()
    ax.tick_params(axis='both', which='minor', length=3, width=1)

    # Grid
    ax.grid(True, which='major', linestyle='-', linewidth=0.8, alpha=0.3)
    ax.grid(True, which='minor', linestyle=':', linewidth=0.5, alpha=0.2)

    # Customize spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)

    # Legend
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9, 
              shadow=True, fancybox=True)

    # Tight layout to prevent label cutoff
    plt.tight_layout()

    plt.show()

    # ============================================================================
    # KEY TAKEAWAYS
    # ============================================================================

    """
    1. Axes limits: set_xlim(), set_ylim()
    2. Ticks: set_xticks(), set_yticks(), set_xticklabels(), set_yticklabels()
    3. Grid: grid(True/False), customize with color, linestyle, linewidth, alpha
    4. Spines: 4 spines (top, bottom, left, right), can hide or reposition
    5. Text: text() for simple text, annotate() for text with arrows
    6. Legend: customize location, frame, font, shadow
    7. Colormaps: systematic colors for many lines
    8. Figure size: figsize=(width, height) in inches
    9. DPI: resolution (dots per inch), higher = sharper
    10. Publication quality: careful attention to all visual elements

    Common Customization Workflow:
    -----------------------------
    1. Plot data with clear line styles
    2. Add labels (xlabel, ylabel, title) with appropriate font sizes
    3. Set limits if needed
    4. Add grid with alpha < 0.5 for subtlety
    5. Hide top/right spines for cleaner look
    6. Add legend with framealpha and shadow
    7. Set figure size and DPI for intended output
    8. Use tight_layout() to prevent cutoff
    9. Save with savefig() before show()
    """
```

---

## Exercises

**Exercise 1.**
Plot `y = sin(x)` over $[0, 4\pi]$. Set the x-axis ticks at multiples of $\pi$ (0, $\pi$, $2\pi$, $3\pi$, $4\pi$) with labels showing the $\pi$ symbol. Set the y-axis limits to $[-1.5, 1.5]$ with ticks at $[-1, -0.5, 0, 0.5, 1]$.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 4 * np.pi, 500)
        y = np.sin(x)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y)

        ax.set_xticks([0, np.pi, 2*np.pi, 3*np.pi, 4*np.pi])
        ax.set_xticklabels([r'$0$', r'$\pi$', r'$2\pi$', r'$3\pi$', r'$4\pi$'])
        ax.set_ylim(-1.5, 1.5)
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])

        ax.set_title(r'$y = \sin(x)$ with $\pi$ Tick Labels')
        plt.show()

---

**Exercise 2.**
Create a scatter plot of 200 random points. Set the x-limits to `[0, 1]` and y-limits to `[0, 1]` regardless of the data range. Add ticks at every 0.1 increment and rotate the x-tick labels by 45 degrees. Also set minor ticks at every 0.05 increment.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.ticker import MultipleLocator

        np.random.seed(42)
        x = np.random.rand(200)
        y = np.random.rand(200)

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.scatter(x, y, alpha=0.5, s=20)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        ax.xaxis.set_major_locator(MultipleLocator(0.1))
        ax.yaxis.set_major_locator(MultipleLocator(0.1))
        ax.xaxis.set_minor_locator(MultipleLocator(0.05))
        ax.yaxis.set_minor_locator(MultipleLocator(0.05))

        ax.tick_params(axis='x', rotation=45)
        ax.set_title('Scatter with Fine Ticks')
        plt.show()

---

**Exercise 3.**
Plot three subplots (1x3) of the same data `y = x^3 - 3*x` over $[-3, 3]$: the first with default limits, the second zoomed into the region $[-1, 1] \times [-2, 2]$, and the third zoomed into $[1, 3] \times [0, 20]$. Add titles indicating the zoom region for each.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 500)
        y = x**3 - 3*x

        fig, axes = plt.subplots(1, 3, figsize=(15, 4))

        axes[0].plot(x, y, color='navy')
        axes[0].set_title('Full View (default)')

        axes[1].plot(x, y, color='navy')
        axes[1].set_xlim(-1, 1)
        axes[1].set_ylim(-2, 2)
        axes[1].set_title('Zoom: [-1,1] x [-2,2]')

        axes[2].plot(x, y, color='navy')
        axes[2].set_xlim(1, 3)
        axes[2].set_ylim(0, 20)
        axes[2].set_title('Zoom: [1,3] x [0,20]')

        for ax in axes:
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()
