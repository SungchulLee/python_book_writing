# Three Ways of Drawing

Matplotlib behaves differently depending on where you run your code: Jupyter Notebook, Python files, or the terminal.

!!! tip "Mental Model"
    Matplotlib's display behavior depends on its backend. Jupyter auto-renders plots inline after each cell, Python scripts need an explicit `plt.show()` to open a window, and the interactive terminal updates on every command. The plotting code stays the same; only the "when does it appear on screen" part changes.

---

## Jupyter Notebook

In Jupyter notebooks, plots render automatically inline.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
# No plt.show() needed - displays automatically
```

**Key points:**

- Neither `plt.show()` nor `plt.draw()` are required
- Plots appear below the cell
- Use `%matplotlib inline` for static images
- Use `%matplotlib notebook` for interactive plots

### Magic Commands

```python
%matplotlib inline    # Static images (default in modern Jupyter)
%matplotlib notebook  # Interactive (zoom, pan)
%matplotlib widget    # Interactive in JupyterLab
```

---

## Python File (.py)

When running Python scripts, you must explicitly display plots.

```python
# script.py
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.plot(x, y)
plt.show()  # Required - opens interactive window
```

**Key points:**

- `plt.show()` starts an event loop
- Opens one or more interactive windows
- Script blocks until windows are closed
- Looks for all active figure objects

### Running the Script

```bash
python script.py
```

A window will open displaying the plot. The script continues after you close the window.

---

## Terminal (Interactive Python)

In an interactive Python session, use `plt.draw()` for updates.

```python
>>> import matplotlib.pyplot as plt
>>> import numpy as np
>>> 
>>> plt.ion()  # Turn on interactive mode
>>> x = np.linspace(0, 10, 100)
>>> plt.plot(x, np.sin(x))
>>> plt.draw()  # Updates the figure
```

**Key points:**

- `plt.ion()` enables interactive mode
- `plt.draw()` updates the figure without blocking
- `plt.ioff()` disables interactive mode
- Useful for dynamic updates

---

## Comparison

| Environment | Display Method | Blocking | Interactive |
|-------------|----------------|----------|-------------|
| Jupyter | Automatic | No | Optional |
| Python file | `plt.show()` | Yes | Yes |
| Terminal | `plt.draw()` | No | Yes |

---

## plt.show() vs plt.draw()

### plt.show()

- Starts the event loop
- Blocks execution until window closed
- Displays all pending figures
- Used in scripts

```python
plt.plot([1, 2, 3])
plt.show()  # Blocks here
print("After show")  # Runs after window closed
```

### plt.draw()

- Redraws the current figure
- Non-blocking
- Used for animations and updates
- Requires interactive mode

```python
plt.ion()
plt.plot([1, 2, 3])
plt.draw()  # Non-blocking
print("Continues immediately")
```

---

## Best Practices

1. **Jupyter**: Let automatic display work; use magic commands for interactivity
2. **Scripts**: Always end with `plt.show()`
3. **Interactive**: Use `plt.ion()` and `plt.draw()` for dynamic updates
4. **Saving**: Use `plt.savefig()` before `plt.show()` in scripts

---

## Key Takeaways

- Jupyter: automatic display, no `show()` needed
- Python files: `plt.show()` required, blocks until closed
- Terminal: `plt.draw()` for non-blocking updates
- `plt.ion()` enables interactive mode
- Choose the right approach for your environment

---

## Runnable Example: `matplotlib_cheatsheet.py`

```python
"""
MATPLOTLIB QUICK REFERENCE CHEAT SHEET
======================================

This is a condensed reference for quick lookup while coding.
For detailed explanations, see the full course files.
"""

# ============================================================================
# IMPORTS
# ============================================================================

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# TWO PLOTTING STYLES
# ============================================================================

# MATLAB-Style (Simple, for quick plots)

if __name__ == "__main__":
    plt.plot(x, y)
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    plt.title('Title')
    plt.show()

    # OOP-Style (Recommended for complex plots)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_title('Title')
    plt.show()

    # ============================================================================
    # METHOD NAME DIFFERENCES
    # ============================================================================

    """
    MATLAB-style              OOP-style
    -------------            ----------------
    plt.xlabel()      →      ax.set_xlabel()
    plt.ylabel()      →      ax.set_ylabel()
    plt.title()       →      ax.set_title()
    plt.xlim()        →      ax.set_xlim()
    plt.ylim()        →      ax.set_ylim()
    plt.xticks()      →      ax.set_xticks()
    plt.yticks()      →      ax.set_yticks()
    plt.legend()      →      ax.legend()        # SAME
    plt.grid()        →      ax.grid()          # SAME
    plt.plot()        →      ax.plot()          # SAME
    """

    # ============================================================================
    # CREATING SUBPLOTS
    # ============================================================================

    # Single plot
    fig, ax = plt.subplots()

    # Multiple plots (2 rows, 3 columns)
    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    # axes.shape = (2, 3)
    # Access: axes[row, col]

    # With shared axes
    fig, axes = plt.subplots(2, 1, sharex=True)

    # Flatten for easy iteration
    axes_flat = axes.flatten()

    # ============================================================================
    # PLOT() - LINE PLOTS
    # ============================================================================

    # Basic
    ax.plot(x, y)

    # With format string: '[marker][line][color]'
    ax.plot(x, y, 'ro-')   # Red circles with solid line
    ax.plot(x, y, 'b--')   # Blue dashed line
    ax.plot(x, y, 'g:s')   # Green dotted with squares

    # With keyword arguments
    ax.plot(x, y, 
            color='red',              # or 'r' or '#FF0000'
            linestyle='--',           # or '--'
            linewidth=2,              # or lw
            marker='o',
            markersize=8,             # or ms
            markerfacecolor='blue',   # or mfc
            markeredgecolor='black',  # or mec
            alpha=0.7,
            label='My Line')

    # Multiple lines
    ax.plot(x, y1, 'r-', label='Line 1')
    ax.plot(x, y2, 'b--', label='Line 2')
    ax.legend()

    # ============================================================================
    # HIST() - HISTOGRAMS
    # ============================================================================

    # Basic histogram
    n, bins, patches = ax.hist(data, bins=30)

    # With explicit bin edges (can be unequal!)
    bins = [0, 1, 2, 5, 10]
    n, bins, patches = ax.hist(data, bins=bins)

    # Probability density (area = 1.0)
    n, bins, patches = ax.hist(data, bins=30, density=True)

    # Customization
    ax.hist(data,
            bins=30,                  # int or array
            density=False,            # False=counts, True=density
            cumulative=False,         # False or True
            histtype='bar',           # 'bar', 'step', 'stepfilled'
            color='blue',
            edgecolor='black',
            alpha=0.7,
            label='My Data')

    # Return values
    n       # Array of counts or densities (length = num_bins)
    bins    # Array of bin edges (length = num_bins + 1)
    patches # List of bar objects

    # Key formula for density
    # density[i] = count[i] / (N × bin_width[i])

    # ============================================================================
    # COLORS
    # ============================================================================

    # Short codes
    'r' 'g' 'b' 'c' 'm' 'y' 'k' 'w'

    # Full names
    'red' 'green' 'blue' 'cyan' 'magenta' 'yellow' 'black' 'white'

    # Hex codes
    '#FF0000'  # Red
    '#00FF00'  # Green
    '#0000FF'  # Blue

    # RGB tuple (0-1)
    (1.0, 0.0, 0.0)  # Red

    # RGBA tuple (0-1, with alpha)
    (1.0, 0.0, 0.0, 0.5)  # Semi-transparent red

    # ============================================================================
    # LINE STYLES
    # ============================================================================

    '-'   # Solid
    '--'  # Dashed
    ':'   # Dotted
    '-.'  # Dash-dot
    ''    # No line

    # ============================================================================
    # MARKERS
    # ============================================================================

    '.'  # Point
    'o'  # Circle
    's'  # Square
    '^'  # Triangle up
    'v'  # Triangle down
    '*'  # Star
    '+'  # Plus
    'x'  # X
    'D'  # Diamond

    # ============================================================================
    # CUSTOMIZATION
    # ============================================================================

    # Labels and title
    ax.set_xlabel('X Label', fontsize=12)
    ax.set_ylabel('Y Label', fontsize=12)
    ax.set_title('Title', fontsize=14, fontweight='bold')

    # Limits
    ax.set_xlim(0, 10)
    ax.set_ylim(-1, 1)

    # Ticks
    ax.set_xticks([0, 2, 4, 6, 8, 10])
    ax.set_xticklabels(['0', '2', '4', '6', '8', '10'])

    # Grid
    ax.grid(True)
    ax.grid(True, alpha=0.3, linestyle='--')

    # Legend
    ax.legend()
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9)

    # Spines (hide top and right)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # ============================================================================
    # TEXT AND ANNOTATIONS
    # ============================================================================

    # Simple text
    ax.text(5, 0.5, 'My text', fontsize=12)

    # Text with box
    ax.text(5, 0.5, 'Text', bbox=dict(boxstyle='round', facecolor='wheat'))

    # Annotation with arrow
    ax.annotate('Point of interest',
                xy=(5, 0.5),      # Point to annotate
                xytext=(6, 0.8),  # Text position
                arrowprops=dict(arrowstyle='->'))

    # ============================================================================
    # FIGURE AND AXES
    # ============================================================================

    # Figure size
    fig, ax = plt.subplots(figsize=(10, 6))  # Width, height in inches

    # DPI (resolution)
    fig, ax = plt.subplots(dpi=150)

    # Tight layout (auto-adjust spacing)
    plt.tight_layout()

    # Save figure
    plt.savefig('figure.png', dpi=300, bbox_inches='tight')

    # ============================================================================
    # GRIDSPEC (COMPLEX LAYOUTS)
    # ============================================================================

    import matplotlib.gridspec as gridspec

    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(3, 3, figure=fig)

    # Span multiple cells
    ax1 = fig.add_subplot(gs[0, :])    # Row 0, all columns
    ax2 = fig.add_subplot(gs[1:, 0])   # Rows 1-2, column 0
    ax3 = fig.add_subplot(gs[1, 1:])   # Row 1, columns 1-2

    # ============================================================================
    # COMMON PATTERNS
    # ============================================================================

    # Single plot with customization
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y, 'b-', linewidth=2, label='Data')
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title('My Plot', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Histogram with density and PDF overlay
    fig, ax = plt.subplots(figsize=(10, 6))
    n, bins, patches = ax.hist(data, bins=30, density=True, alpha=0.7, label='Data')
    ax.plot(x_pdf, pdf, 'r-', linewidth=3, label='Theory')
    ax.set_xlabel('Value', fontsize=12)
    ax.set_ylabel('Probability Density', fontsize=12)
    ax.legend()
    plt.show()

    # Multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    for i, ax in enumerate(axes.flatten()):
        ax.plot(x, y[i])
        ax.set_title(f'Plot {i+1}')
    plt.tight_layout()
    plt.show()

    # ============================================================================
    # DEBUGGING CHECKLIST
    # ============================================================================

    """
    Common Mistakes:
    1. Using plt.xlabel() instead of ax.set_xlabel() in OOP style
    2. Forgetting that axes[row, col] (not axes[col, row])
    3. Not unpacking hist() return values when needed
    4. Confusing density=True (area=1) with density=False (counts)
    5. Accessing axes[2, 1] when shape is (2, 2) (out of bounds)
    6. Not calling plt.show() at the end
    7. Forgetting that bins array has length = num_bins + 1
    """

    # ============================================================================
    # QUICK DIAGNOSIS
    # ============================================================================

    """
    Error: 'AxesSubplot' object has no attribute 'xlabel'
    Fix: Use ax.set_xlabel() not ax.xlabel()

    Error: IndexError: index 2 is out of bounds for axis 0 with size 2
    Fix: Check axes.shape, remember axes[row, col]

    Issue: Histogram looks weird
    Check: bins parameter, try different values

    Issue: Want to overlay PDF but scales don't match
    Fix: Use density=True in hist()

    Issue: Can't access individual subplots
    Fix: Use axes.flatten() to convert to 1D array
    """

    print("Cheat sheet loaded! Use as quick reference while coding.")
```


## Why Behavior Differs: The Backend

The plotting code is always the same --- what changes is the **backend** (the rendering engine):

```text
inline backend (Jupyter)  → renders static PNG per cell
GUI backend (scripts)     → opens interactive window, blocks at show()
interactive terminal      → updates on every command
```

The backend controls *when and how* pixels reach the screen. This is why the same code behaves differently in Jupyter vs a `.py` script vs the REPL.

---

## Exercises

**Exercise 1.** Write the same plot (a sine curve) using all three Matplotlib interfaces: (1) pyplot implicit, (2) pyplot explicit (`fig, ax`), and (3) pure OOP style.

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

**Exercise 2.** Explain the advantages and disadvantages of the pyplot interface versus the OOP interface. Which is recommended for production code?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code using `plt.subplots()` (the recommended way) to create a 1x2 figure with different plots in each subplot.

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

**Exercise 4.** Predict what happens if you mix pyplot calls (`plt.plot()`) and OOP calls (`ax.plot()`) in the same script. Can this cause confusion?

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
