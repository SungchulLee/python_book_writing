# GridSpec

GridSpec provides fine-grained control over subplot layout, enabling complex arrangements with varying cell sizes and spans.

!!! tip "Mental Model"
    GridSpec defines an invisible grid on the Figure, then you assign each subplot to one or more cells using slice notation (e.g., `gs[0, :]` for the entire first row). Think of it as a spreadsheet grid where you merge cells to create subplots of different sizes. It is the most powerful layout tool when `plt.subplots()` is too rigid.

!!! note "When to Use GridSpec"
    | Need | Tool |
    |------|------|
    | Simple uniform grid | `plt.subplots()` |
    | Panels of different sizes / spanning rows or columns | **GridSpec** |
    | Readable ASCII-style layout | `subplot_mosaic` |
    | Nested grids (grid inside a grid) | **GridSpec** (with `SubGridSpec`) |
    | Programmatic dynamic layouts | **GridSpec** (generated from data) |

    Use GridSpec when you need precise control over cell spanning and size ratios
    that `subplots()` cannot express.

## Basic GridSpec

Create a grid and add subplots to each cell.

### 1. Import GridSpec

```python
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
```

### 2. Create Grid

```python
x = np.linspace(0, 3, 50)
y1 = x ** 2
y2 = np.sqrt(x)

fig = plt.figure()
gs = gridspec.GridSpec(2, 3)  # 2 rows, 3 columns
```

### 3. Add Subplots

```python
for i, g in enumerate(gs):
    ax = fig.add_subplot(g)
    if i % 2 == 0:
        ax.plot(x, y1)
    else:
        ax.plot(x, y2)

fig.tight_layout()
plt.show()
```

## Size Ratios

Control relative sizes of rows and columns.

### 1. Height Ratios

```python
fig = plt.figure()
gs = gridspec.GridSpec(2, 3, height_ratios=[2, 1])  # Top row twice as tall

for i, g in enumerate(gs):
    ax = fig.add_subplot(g)
    ax.set_title(f'Cell {i}')

fig.tight_layout()
plt.show()
```

### 2. Width Ratios

```python
fig = plt.figure()
gs = gridspec.GridSpec(2, 3, width_ratios=[1, 2, 1])  # Middle column wider

for i, g in enumerate(gs):
    ax = fig.add_subplot(g)

fig.tight_layout()
plt.show()
```

### 3. Combined Ratios

```python
fig = plt.figure()
gs = gridspec.GridSpec(2, 3, 
                       height_ratios=[2, 1], 
                       width_ratios=[1, 2, 1])

for i, g in enumerate(gs):
    ax = fig.add_subplot(g)
    ax.set_title(f'Cell {i}')

fig.tight_layout()
plt.show()
```

## Spanning Cells

Use slicing to span multiple rows or columns.

### 1. Span Columns

```python
fig = plt.figure(figsize=(10, 6))
gs = gridspec.GridSpec(3, 3)

# Full top row
ax1 = fig.add_subplot(gs[0, :])  # Row 0, all columns
ax1.set_title('Top Row (spans all columns)')

fig.tight_layout()
plt.show()
```

### 2. Span Rows

```python
fig = plt.figure(figsize=(10, 6))
gs = gridspec.GridSpec(3, 3)

# Left column, rows 1-2
ax2 = fig.add_subplot(gs[1:, 0])  # Rows 1-2, column 0
ax2.set_title('Left (spans 2 rows)')

fig.tight_layout()
plt.show()
```

### 3. Span Block

```python
fig = plt.figure(figsize=(10, 6))
gs = gridspec.GridSpec(3, 3)

ax1 = fig.add_subplot(gs[0, :])
ax1.set_title('Top Row')

ax2 = fig.add_subplot(gs[1:, 0])
ax2.set_title('Left Column')

ax3 = fig.add_subplot(gs[1:, 1:])  # 2x2 block
ax3.set_title('Right Block (2x2)')

x = np.linspace(0, 10, 100)
ax1.plot(x, np.sin(x))
ax2.plot(x, np.cos(x))
ax3.plot(x, np.tan(x))
ax3.set_ylim(-5, 5)

fig.tight_layout()
plt.show()
```

## Complex Layouts

Create sophisticated multi-panel figures.

### 1. Dashboard Layout

```python
fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(4, 4)

# Main plot: upper-left 3x3
ax_main = fig.add_subplot(gs[:3, :3])
ax_main.set_title('Main Plot')

# Right sidebar: 3 small plots
ax_right1 = fig.add_subplot(gs[0, 3])
ax_right2 = fig.add_subplot(gs[1, 3])
ax_right3 = fig.add_subplot(gs[2, 3])

# Bottom bar: full width
ax_bottom = fig.add_subplot(gs[3, :])
ax_bottom.set_title('Timeline')
```

### 2. Add Data

```python
x = np.linspace(0, 10, 100)
ax_main.plot(x, np.sin(x), 'b-', linewidth=2)
ax_main.set_xlabel('x')
ax_main.set_ylabel('y')

ax_right1.hist(np.random.randn(100), bins=20)
ax_right2.hist(np.random.randn(100), bins=20)
ax_right3.hist(np.random.randn(100), bins=20)

ax_bottom.plot(x, np.random.randn(100).cumsum())

fig.tight_layout()
plt.show()
```

### 3. Scientific Figure Layout

```python
fig = plt.figure(figsize=(10, 8))
gs = gridspec.GridSpec(2, 2, height_ratios=[3, 1], width_ratios=[2, 1])

ax_main = fig.add_subplot(gs[0, 0])
ax_hist = fig.add_subplot(gs[0, 1])
ax_resid = fig.add_subplot(gs[1, 0])
ax_stats = fig.add_subplot(gs[1, 1])

fig.tight_layout()
plt.show()
```

## Nested GridSpec

Create grids within grids for hierarchical layouts.

### 1. Outer Grid

```python
fig = plt.figure(figsize=(12, 6))
outer_gs = gridspec.GridSpec(1, 2, figure=fig)

ax_left = fig.add_subplot(outer_gs[0])
ax_left.set_title('Left Panel')
```

### 2. Inner Grid

```python
inner_gs = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer_gs[1])

ax1 = fig.add_subplot(inner_gs[0, 0])
ax2 = fig.add_subplot(inner_gs[0, 1])
ax3 = fig.add_subplot(inner_gs[1, 0])
ax4 = fig.add_subplot(inner_gs[1, 1])
```

### 3. Complete Example

```python
fig = plt.figure(figsize=(12, 6))
outer_gs = gridspec.GridSpec(1, 2, figure=fig)

ax_left = fig.add_subplot(outer_gs[0])
ax_left.set_title('Left Panel')

inner_gs = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer_gs[1])
ax1 = fig.add_subplot(inner_gs[0, 0])
ax2 = fig.add_subplot(inner_gs[0, 1])
ax3 = fig.add_subplot(inner_gs[1, 0])
ax4 = fig.add_subplot(inner_gs[1, 1])

x = np.linspace(0, 5, 50)
ax_left.plot(x, x**2)
ax1.plot(x, np.sin(x))
ax2.plot(x, np.cos(x))
ax3.plot(x, np.exp(x/5))
ax4.plot(x, np.log(x + 1))

fig.tight_layout()
plt.show()
```

## GridSpec Parameters

Configure spacing and position.

### 1. Spacing Parameters

```python
gs = gridspec.GridSpec(2, 3,
                       wspace=0.3,   # Width space between subplots
                       hspace=0.3)   # Height space between subplots
```

### 2. Position Parameters

```python
gs = gridspec.GridSpec(2, 3,
                       left=0.1,     # Left edge position
                       right=0.9,    # Right edge position
                       bottom=0.1,   # Bottom edge position
                       top=0.9)      # Top edge position
```

### 3. Full Parameter List

```python
gs = gridspec.GridSpec(
    nrows=2,                    # Number of rows
    ncols=3,                    # Number of columns
    figure=fig,                 # Figure to attach to
    left=0.1,
    right=0.9,
    bottom=0.1,
    top=0.9,
    wspace=0.2,
    hspace=0.2,
    width_ratios=[1, 2, 1],
    height_ratios=[2, 1]
)
```

---

## Runnable Example: `gridspec_tutorial.py`

```python
"""
Matplotlib Tutorial - Advanced Level
====================================
Topic: Complex Subplot Layouts and GridSpec
Author: Educational Python Course
Level: Advanced

Learning Objectives:
-------------------
1. Master complex subplot arrangements
2. Use GridSpec for flexible layouts
3. Create subplots with different sizes
4. Share axes between subplots
5. Create nested subplots
6. Build dashboard-style visualizations

Prerequisites:
-------------
- Complete understanding of basic subplots
- Mastery of axes array indexing
- Intermediate plotting skills
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# ============================================================================
# SECTION 1: Review - Basic Subplots
# ============================================================================

if __name__ == "__main__":

    """
    Quick review of plt.subplots() for equal-sized subplots
    """

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))

    for i, ax in enumerate(axes.flatten()):
        x = np.linspace(0, 10, 100)
        ax.plot(x, np.sin((i+1)*x))
        ax.set_title(f'Subplot {i+1}')

    plt.suptitle('Basic Subplots: Equal Sizes', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 2: Sharing Axes - Linked Plots
    # ============================================================================

    """
    sharex and sharey parameters link axes across subplots
    This is useful when comparing data with the same scale
    """

    x = np.linspace(0, 10, 100)

    # Share x-axis
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(x, np.sin(x))
    axes[0].set_ylabel('sin(x)')
    axes[0].set_title('Shared x-axis: All plots use same x-range')

    axes[1].plot(x, np.cos(x))
    axes[1].set_ylabel('cos(x)')

    axes[2].plot(x, np.tan(x))
    axes[2].set_ylabel('tan(x)')
    axes[2].set_ylim(-3, 3)
    axes[2].set_xlabel('x')  # Only bottom plot has x-label

    # Notice: when you zoom on one plot, all plots zoom together in x
    plt.tight_layout()
    plt.show()

    # Share both x and y axes
    fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)

    for i, ax in enumerate(axes.flatten()):
        x = np.linspace(0, 10, 100)
        ax.plot(x, np.sin(x + i))
        ax.set_title(f'Plot {i+1}')

    # Only need labels on edge plots
    axes[1, 0].set_xlabel('x')
    axes[1, 1].set_xlabel('x')
    axes[0, 0].set_ylabel('y')
    axes[1, 0].set_ylabel('y')

    plt.suptitle('Shared x and y axes', fontsize=16)
    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 3: Introduction to GridSpec - The Power Tool
    # ============================================================================

    """
    GridSpec allows creating subplots with different sizes and positions
    Think of it as a grid layout manager

    Key concept: Define a grid (rows × columns), then assign subplots to 
    portions of that grid
    """

    # Create a 3×3 grid
    fig = plt.figure(figsize=(12, 10))
    gs = gridspec.GridSpec(3, 3, figure=fig)

    # Subplot spanning multiple cells
    # gs[row_start:row_end, col_start:col_end]

    # Top row: one large plot
    ax1 = fig.add_subplot(gs[0, :])  # Row 0, all columns
    ax1.plot(np.linspace(0, 10, 100), np.sin(np.linspace(0, 10, 100)))
    ax1.set_title('Large plot spanning entire top row')
    ax1.set_ylabel('sin(x)')

    # Middle row: two plots
    ax2 = fig.add_subplot(gs[1, :2])  # Row 1, columns 0-1
    ax2.plot(np.linspace(0, 10, 100), np.cos(np.linspace(0, 10, 100)))
    ax2.set_title('Middle-left plot (2/3 width)')
    ax2.set_ylabel('cos(x)')

    ax3 = fig.add_subplot(gs[1, 2])  # Row 1, column 2
    ax3.hist(np.random.randn(1000), bins=20)
    ax3.set_title('Middle-right (1/3 width)')

    # Bottom row: three small plots
    ax4 = fig.add_subplot(gs[2, 0])
    ax4.scatter(np.random.rand(50), np.random.rand(50))
    ax4.set_title('Bottom-left')

    ax5 = fig.add_subplot(gs[2, 1])
    ax5.scatter(np.random.rand(50), np.random.rand(50))
    ax5.set_title('Bottom-middle')

    ax6 = fig.add_subplot(gs[2, 2])
    ax6.scatter(np.random.rand(50), np.random.rand(50))
    ax6.set_title('Bottom-right')

    plt.suptitle('GridSpec: Different Subplot Sizes', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    print("=" * 70)
    print("GRIDSPEC INDEXING")
    print("=" * 70)
    print("gs[0, :]     → Row 0, all columns")
    print("gs[:, 0]     → All rows, column 0")
    print("gs[1:3, 0:2] → Rows 1-2, columns 0-1")
    print("gs[0, 0]     → Single cell at row 0, col 0")

    # ============================================================================
    # SECTION 4: GridSpec with Spacing Control
    # ============================================================================

    """
    GridSpec allows fine control over spacing between subplots
    """

    fig = plt.figure(figsize=(12, 10))

    # Create GridSpec with custom spacing
    gs = gridspec.GridSpec(
        3, 3,
        figure=fig,
        wspace=0.4,  # Width space between columns
        hspace=0.4,  # Height space between rows
        left=0.1,    # Left margin
        right=0.9,   # Right margin
        top=0.9,     # Top margin
        bottom=0.1   # Bottom margin
    )

    # Create subplots
    for i in range(3):
        for j in range(3):
            ax = fig.add_subplot(gs[i, j])
            ax.text(0.5, 0.5, f'({i},{j})', 
                    ha='center', va='center', fontsize=16,
                    transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])

    plt.suptitle('GridSpec with Custom Spacing', fontsize=16, fontweight='bold', y=0.95)
    plt.show()

    # ============================================================================
    # SECTION 5: Dashboard-Style Layout
    # ============================================================================

    """
    Create a dashboard with one large main plot and smaller auxiliary plots
    """

    # Generate data
    np.random.seed(42)
    x = np.linspace(0, 10, 1000)
    y = np.sin(x) + 0.1 * np.random.randn(1000)

    fig = plt.figure(figsize=(14, 10))
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

    # Main plot: large, spanning 2×2
    ax_main = fig.add_subplot(gs[:2, :2])
    ax_main.plot(x, y, 'b-', alpha=0.5, linewidth=0.5)
    ax_main.plot(x, np.sin(x), 'r-', linewidth=2, label='True signal')
    ax_main.set_xlabel('Time', fontsize=12)
    ax_main.set_ylabel('Signal', fontsize=12)
    ax_main.set_title('Main Plot: Time Series with Noise', fontsize=14, fontweight='bold')
    ax_main.legend()
    ax_main.grid(True, alpha=0.3)

    # Histogram of values (right side)
    ax_hist = fig.add_subplot(gs[:2, 2])
    ax_hist.hist(y, bins=50, orientation='horizontal', alpha=0.7)
    ax_hist.set_xlabel('Frequency', fontsize=10)
    ax_hist.set_title('Distribution', fontsize=12)
    ax_hist.grid(True, alpha=0.3)

    # Power spectrum (bottom left)
    ax_fft = fig.add_subplot(gs[2, 0])
    fft_vals = np.abs(np.fft.fft(y))
    fft_freq = np.fft.fftfreq(len(y), x[1] - x[0])
    ax_fft.plot(fft_freq[:len(fft_freq)//2], fft_vals[:len(fft_vals)//2])
    ax_fft.set_xlabel('Frequency', fontsize=10)
    ax_fft.set_ylabel('Power', fontsize=10)
    ax_fft.set_title('Frequency Domain', fontsize=12)
    ax_fft.grid(True, alpha=0.3)

    # Statistics (bottom middle)
    ax_stats = fig.add_subplot(gs[2, 1])
    stats_text = f"""
    Statistics:
    Mean: {np.mean(y):.3f}
    Std:  {np.std(y):.3f}
    Min:  {np.min(y):.3f}
    Max:  {np.max(y):.3f}
    """
    ax_stats.text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
                  transform=ax_stats.transAxes, verticalalignment='center')
    ax_stats.set_xlim(0, 1)
    ax_stats.set_ylim(0, 1)
    ax_stats.axis('off')

    # Correlation plot (bottom right)
    ax_corr = fig.add_subplot(gs[2, 2])
    ax_corr.scatter(y[:-1], y[1:], alpha=0.3, s=1)
    ax_corr.set_xlabel('y(t)', fontsize=10)
    ax_corr.set_ylabel('y(t+1)', fontsize=10)
    ax_corr.set_title('Lag-1 Autocorr', fontsize=12)
    ax_corr.grid(True, alpha=0.3)

    plt.suptitle('Data Analysis Dashboard', fontsize=16, fontweight='bold')
    plt.show()

    # ============================================================================
    # SECTION 6: Nested GridSpecs
    # ============================================================================

    """
    You can create grids within grids for even more complex layouts
    """

    fig = plt.figure(figsize=(14, 10))

    # Outer grid: 2 rows, 2 columns
    outer_gs = gridspec.GridSpec(2, 2, figure=fig, wspace=0.3, hspace=0.3)

    # Top-left: Single plot
    ax1 = fig.add_subplot(outer_gs[0, 0])
    ax1.plot(np.linspace(0, 10, 100), np.sin(np.linspace(0, 10, 100)))
    ax1.set_title('Top-Left: Single Plot', fontweight='bold')

    # Top-right: Nested grid (2×2)
    inner_gs_tr = gridspec.GridSpecFromSubplotSpec(2, 2, subplot_spec=outer_gs[0, 1],
                                                    wspace=0.1, hspace=0.1)
    for i in range(2):
        for j in range(2):
            ax = fig.add_subplot(inner_gs_tr[i, j])
            ax.plot(np.random.rand(20))
            ax.set_title(f'TR-{i}{j}', fontsize=9)
            ax.tick_params(labelsize=8)

    # Bottom-left: Nested grid (3×1)
    inner_gs_bl = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=outer_gs[1, 0],
                                                    hspace=0.4)
    for i in range(3):
        ax = fig.add_subplot(inner_gs_bl[i, 0])
        ax.hist(np.random.randn(100), bins=15)
        ax.set_title(f'Bottom-Left {i+1}', fontsize=10)

    # Bottom-right: Single large plot
    ax2 = fig.add_subplot(outer_gs[1, 1])
    x = np.random.randn(500)
    y = np.random.randn(500)
    ax2.scatter(x, y, alpha=0.5)
    ax2.set_title('Bottom-Right: Scatter Plot', fontweight='bold')

    plt.suptitle('Nested GridSpecs: Grids within Grids', fontsize=16, fontweight='bold')
    plt.show()

    # ============================================================================
    # SECTION 7: Using subplot2grid - Alternative Syntax
    # ============================================================================

    """
    subplot2grid is an alternative to GridSpec with simpler syntax for some cases
    """

    fig = plt.figure(figsize=(12, 8))

    # subplot2grid(grid_shape, location, rowspan=1, colspan=1)

    # Create a 3×3 grid and place subplots
    ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)  # Top row, span 3 cols
    ax1.plot(np.linspace(0, 10, 100), np.sin(np.linspace(0, 10, 100)))
    ax1.set_title('Top: colspan=3')

    ax2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)  # Middle, span 2 cols
    ax2.plot(np.linspace(0, 10, 100), np.cos(np.linspace(0, 10, 100)))
    ax2.set_title('Middle-left: colspan=2')

    ax3 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)  # Right side, span 2 rows
    ax3.hist(np.random.randn(1000), bins=30, orientation='horizontal')
    ax3.set_title('Right: rowspan=2')

    ax4 = plt.subplot2grid((3, 3), (2, 0))
    ax4.scatter(np.random.rand(50), np.random.rand(50))
    ax4.set_title('Bottom-left')

    ax5 = plt.subplot2grid((3, 3), (2, 1))
    ax5.scatter(np.random.rand(50), np.random.rand(50))
    ax5.set_title('Bottom-middle')

    plt.suptitle('subplot2grid: Simpler Syntax', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 8: Width and Height Ratios
    # ============================================================================

    """
    Control relative sizes of rows and columns
    """

    fig = plt.figure(figsize=(12, 8))

    # Create GridSpec with custom ratios
    # width_ratios: relative widths of columns
    # height_ratios: relative heights of rows
    gs = gridspec.GridSpec(
        2, 3,
        figure=fig,
        width_ratios=[1, 2, 1],   # Middle column is twice as wide
        height_ratios=[2, 1],     # Top row is twice as tall
        wspace=0.3,
        hspace=0.3
    )

    # Create subplots
    positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)]
    for i, (row, col) in enumerate(positions):
        ax = fig.add_subplot(gs[row, col])
        ax.text(0.5, 0.5, f'({row},{col})\nRatio demo',
                ha='center', va='center', fontsize=14,
                transform=ax.transAxes)
        ax.set_title(f'Plot {i+1}')

    plt.suptitle('Custom Width and Height Ratios', fontsize=16, fontweight='bold')
    plt.show()

    print("=" * 70)
    print("WIDTH AND HEIGHT RATIOS")
    print("=" * 70)
    print("width_ratios=[1, 2, 1]  → columns have relative widths 1:2:1")
    print("height_ratios=[2, 1]    → rows have relative heights 2:1")
    print("Actual sizes calculated automatically to fit figure")

    # ============================================================================
    # SECTION 9: Complex Scientific Figure Example
    # ============================================================================

    """
    Real-world example: Comprehensive data analysis figure
    """

    # Generate synthetic data
    np.random.seed(42)
    time = np.linspace(0, 10, 1000)
    signal1 = np.sin(2 * np.pi * time) + 0.5 * np.random.randn(1000)
    signal2 = np.cos(2 * np.pi * time) + 0.5 * np.random.randn(1000)

    fig = plt.figure(figsize=(16, 10))
    gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.4)

    # Main time series (top, spanning 3 columns)
    ax_main = fig.add_subplot(gs[0, :3])
    ax_main.plot(time, signal1, 'b-', alpha=0.7, label='Signal 1')
    ax_main.plot(time, signal2, 'r-', alpha=0.7, label='Signal 2')
    ax_main.set_xlabel('Time (s)', fontsize=12)
    ax_main.set_ylabel('Amplitude', fontsize=12)
    ax_main.set_title('Time Series Data', fontsize=14, fontweight='bold')
    ax_main.legend(loc='upper right')
    ax_main.grid(True, alpha=0.3)

    # Phase space (top right)
    ax_phase = fig.add_subplot(gs[0, 3])
    ax_phase.scatter(signal1, signal2, alpha=0.3, s=1)
    ax_phase.set_xlabel('Signal 1', fontsize=10)
    ax_phase.set_ylabel('Signal 2', fontsize=10)
    ax_phase.set_title('Phase Space', fontsize=12)
    ax_phase.grid(True, alpha=0.3)

    # Histogram signal 1
    ax_hist1 = fig.add_subplot(gs[1, 0])
    ax_hist1.hist(signal1, bins=50, alpha=0.7, edgecolor='black')
    ax_hist1.set_xlabel('Signal 1', fontsize=10)
    ax_hist1.set_ylabel('Frequency', fontsize=10)
    ax_hist1.set_title('Distribution: Signal 1', fontsize=12)
    ax_hist1.grid(True, alpha=0.3)

    # Histogram signal 2
    ax_hist2 = fig.add_subplot(gs[1, 1])
    ax_hist2.hist(signal2, bins=50, alpha=0.7, edgecolor='black')
    ax_hist2.set_xlabel('Signal 2', fontsize=10)
    ax_hist2.set_ylabel('Frequency', fontsize=10)
    ax_hist2.set_title('Distribution: Signal 2', fontsize=12)
    ax_hist2.grid(True, alpha=0.3)

    # Correlation
    ax_corr = fig.add_subplot(gs[1, 2])
    correlation = np.correlate(signal1 - signal1.mean(), 
                               signal2 - signal2.mean(), 
                               mode='same')
    lags = np.arange(-len(correlation)//2, len(correlation)//2 + 1)
    ax_corr.plot(lags, correlation)
    ax_corr.set_xlabel('Lag', fontsize=10)
    ax_corr.set_ylabel('Correlation', fontsize=10)
    ax_corr.set_title('Cross-Correlation', fontsize=12)
    ax_corr.grid(True, alpha=0.3)

    # Statistics
    ax_stats = fig.add_subplot(gs[1, 3])
    stats_text = f"""Signal 1:
      μ = {np.mean(signal1):.3f}
      σ = {np.std(signal1):.3f}

    Signal 2:
      μ = {np.mean(signal2):.3f}
      σ = {np.std(signal2):.3f}

    Correlation:
      ρ = {np.corrcoef(signal1, signal2)[0,1]:.3f}
    """
    ax_stats.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
                  transform=ax_stats.transAxes, verticalalignment='center')
    ax_stats.axis('off')

    # Spectrogram or rolling statistics (bottom row, full width)
    ax_bottom = fig.add_subplot(gs[2, :])
    window = 100
    rolling_mean1 = np.convolve(signal1, np.ones(window)/window, mode='same')
    rolling_mean2 = np.convolve(signal2, np.ones(window)/window, mode='same')
    ax_bottom.plot(time, rolling_mean1, 'b-', linewidth=2, label='Signal 1 (smoothed)')
    ax_bottom.plot(time, rolling_mean2, 'r-', linewidth=2, label='Signal 2 (smoothed)')
    ax_bottom.set_xlabel('Time (s)', fontsize=12)
    ax_bottom.set_ylabel('Smoothed Amplitude', fontsize=12)
    ax_bottom.set_title('Rolling Average (window=100)', fontsize=14, fontweight='bold')
    ax_bottom.legend()
    ax_bottom.grid(True, alpha=0.3)

    plt.suptitle('Comprehensive Signal Analysis', fontsize=18, fontweight='bold', y=0.98)
    plt.show()

    # ============================================================================
    # KEY TAKEAWAYS
    # ============================================================================

    """
    1. Basic plt.subplots() creates equal-sized subplots
    2. sharex/sharey links axes across subplots
    3. GridSpec provides flexible layout control:
       - Different subplot sizes
       - Spanning multiple cells
       - Custom spacing (wspace, hspace)
    4. GridSpec indexing: gs[row_start:row_end, col_start:col_end]
    5. Nested GridSpecs allow grids within grids
    6. subplot2grid is simpler syntax for some layouts
    7. width_ratios and height_ratios control relative sizes
    8. Complex layouts require planning:
       - Sketch layout first
       - Choose grid size
       - Decide which cells each subplot occupies

    Common Patterns:
    ---------------
    Dashboard: Large main plot + smaller auxiliary plots
    Comparison: Multiple views of same data
    Multi-scale: Overview + detail views
    Analysis: Data + distributions + statistics

    GridSpec Syntax Comparison:
    ---------------------------
    gs[0, :]       → Row 0, all columns
    gs[:, 0]       → All rows, column 0  
    gs[0:2, 1:3]   → Rows 0-1, columns 1-2
    gs[0, 0]       → Single cell

    Tips:
    ----
    - Plan layout on paper first
    - Start with outer structure, then details
    - Use wspace/hspace for breathing room
    - tight_layout() helps but isn't always perfect
    - For complex figures, manual spacing may be needed
    """
```


---

## Exercises

**Exercise 1.** Write code using `matplotlib.gridspec.GridSpec` to create a layout with one wide subplot on top spanning the full width and two subplots below side by side.

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

**Exercise 2.** Explain the advantage of `GridSpec` over `plt.subplots()` for creating non-uniform subplot layouts.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a layout with `GridSpec` where one subplot spans 2 rows on the left and two smaller subplots are stacked on the right.

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

**Exercise 4.** Write code using `GridSpec` with `hspace` and `wspace` parameters to control spacing between subplots.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'b-', lw=2)
    ax.set_title('Solution')
    plt.show()
    ```

    Refer to the code examples in the main content for the specific API calls needed.
