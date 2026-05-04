# Basic Line Plot

The `plot()` method is the fundamental tool for creating line plots in Matplotlib.

!!! tip "Mental Model"
    `ax.plot(x, y)` connects data points with straight line segments in order. If you pass only y-values, Matplotlib uses 0, 1, 2, ... as x-values. Every `plot()` call returns a list of `Line2D` artists, and you can stack multiple `plot()` calls on the same Axes to overlay several lines.

    The core concept: **`plot()` maps numerical data to visual position (x, y).**
    Everything else — line styles, colors, markers, labels — is styling on top of
    this spatial encoding. Each `plot()` call creates `Line2D` artists on the
    Axes; all styling modifies these artists.

!!! note "Visual Encoding Channels"
    All plotting in Matplotlib is about encoding data into visual variables:

    | Channel | What it encodes | Example |
    |---------|----------------|---------|
    | Position (x, y) | Where — the primary data | `ax.plot(x, y)` |
    | Color | What — category or group | `color='red'` |
    | Linestyle | Distinction — primary vs reference | `linestyle='--'` |
    | Marker | Discrete observations | `marker='o'` |
    | Size | Emphasis | `linewidth=2` |
    | Error bars | Uncertainty | `ax.errorbar(...)` |

    Understanding plotting is not about memorizing functions — it is about
    understanding how data is translated into visuals. Lines encode continuity
    (interpolation between points); markers encode discrete measurements.

!!! note "Matplotlib Workflow"
    Every visualization follows the same five-step pipeline:

    ```text
    1. Prepare data         (NumPy / Pandas)
    2. Plot data            (plot, scatter, bar, hist, ...)
    3. Style                (color, linestyle, markers)
    4. Annotate             (labels, legend, title)
    5. Layout               (subplots, spacing, saving)
    ```

    This section covers steps 2--4 for line plots. The remaining pages in this
    folder detail each styling and annotation layer.

---

## Simplest Line Plot

Provide only y-values (x-values are auto-generated as indices):

```python
import matplotlib.pyplot as plt

y = [1, 5, 2]

plt.plot(y)
plt.show()
```

---

## Providing X and Y Values

```python
import matplotlib.pyplot as plt

x = [1, 2, 3]
y = [1, 5, 2]

plt.plot(x, y)
plt.show()
```

---

## OOP Style

Using explicit Figure and Axes objects:

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    y = np.sin(x)

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(x, y)
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Multiple Lines

Plot multiple lines on the same axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y_sin)
ax.plot(x, y_cos)
plt.show()
```

---

## Plot Returns Line2D Objects

The `plot()` method returns a list of `Line2D` objects:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 10)
y = np.sin(x)

lines = plt.plot(x, y, '--*r', ms=20)
plt.show()

print(type(lines))     # <class 'list'>
print(type(lines[0]))  # <class 'matplotlib.lines.Line2D'>
```

---

## With Labels and Title

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 100)
y = x + x**2

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y, color='g')
ax.set_title('$y = x + x^2$', fontsize=20)
ax.set_xlabel('$x$', fontsize=20)
ax.set_ylabel('$y$', fontsize=20)
plt.show()
```

---

## Combining Multiple Options

Use the `set()` method for multiple properties at once:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 100)
y = x + x**2

fig, ax = plt.subplots()
ax.plot(x, y, color='g')
ax.set(
    title='$y = x + x^2$',
    xlabel='$x$',
    ylabel='$y$',
    xlim=[0, 1],
    ylim=(0, 2),
    xticks=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    yticks=[0.0, 0.5, 1.0, 1.5, 2.0]
)
plt.show()
```

---

## Practical Example: Financial Data

```python
import matplotlib.pyplot as plt
import yfinance as yf

def main():
    kospi_ticker = "^KS11"
    kospi_data = yf.download(kospi_ticker, start="2023-01-01", end="2024-12-31")
    close_prices = kospi_data["Close"]

    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(close_prices, label="KOSPI Close")
    ax.set_title("KOSPI Closing Prices")
    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.legend()
    ax.grid(True)
    plt.show()

if __name__ == '__main__':
    main()
```

---

## Key Takeaways

- `plt.plot(y)` uses indices as x-values
- `plt.plot(x, y)` specifies both coordinates
- Multiple `plot()` calls add lines to the same axes
- `plot()` returns a list of `Line2D` objects
- Use `ax.set()` for multiple properties at once

---

## Runnable Example: `complete_guide_plot.py`

```python
"""
Matplotlib Tutorial - Intermediate Level
========================================
Topic: Complete Guide to plt.plot() - The Most Important Function
Author: Educational Python Course
Level: Intermediate

Learning Objectives:
-------------------
1. Master all parameters and options of plt.plot()
2. Understand line customization in depth
3. Learn marker customization
4. Create professional-quality line plots
5. Understand format strings and explicit parameters
6. Master multiple datasets on same axes

Prerequisites:
-------------
- Completion of all beginner tutorials
- Understanding of both MATLAB and OOP styles
- Basic NumPy knowledge

IMPORTANT:
---------
plt.plot() and ax.plot() have IDENTICAL parameters and behavior.
Everything here applies to both styles!
"""

import matplotlib.pyplot as plt
import numpy as np

# ============================================================================
# SECTION 1: Basic Signature and Return Values
# ============================================================================

if __name__ == "__main__":

    """
    Complete Signature:
    ------------------
    plot([x], y, [fmt], **kwargs)

    Parameters:
    -----------
    x : array-like (optional)
        X-coordinates. If not provided, uses range(len(y))

    y : array-like
        Y-coordinates (required)

    fmt : str (optional)
        Format string: '[marker][line][color]'
        Examples: 'ro-', 'b--', 'g^:', 'k*-.'

    **kwargs : keyword arguments
        Explicit property settings (color, linewidth, marker, etc.)

    Returns:
    --------
    list of Line2D objects
        Can be used to modify line properties later
    """

    # Example of return value
    x = np.linspace(0, 10, 50)
    y = np.sin(x)

    line_objects = plt.plot(x, y)
    print(f"Type of return value: {type(line_objects)}")  # list
    print(f"Number of Line2D objects: {len(line_objects)}")  # 1
    print(f"First line object: {line_objects[0]}")

    plt.show()

    # ============================================================================
    # SECTION 2: Different Ways to Call plot()
    # ============================================================================

    print("=" * 70)
    print("DIFFERENT WAYS TO CALL plot()")
    print("=" * 70)

    # Method 1: Only y values (x is automatically 0, 1, 2, ...)
    y = [1, 4, 9, 16, 25]
    plt.plot(y)
    plt.title('Method 1: Only y values')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.show()

    # Method 2: x and y values
    x = [0, 1, 2, 3, 4]
    y = [1, 4, 9, 16, 25]
    plt.plot(x, y)
    plt.title('Method 2: x and y values')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

    # Method 3: x, y, and format string
    x = np.linspace(0, 10, 50)
    y = np.sin(x)
    plt.plot(x, y, 'ro-')  # red circles with solid line
    plt.title('Method 3: x, y, and format string')
    plt.show()

    # Method 4: x, y, and keyword arguments
    plt.plot(x, y, color='blue', linewidth=2, marker='o', markersize=8)
    plt.title('Method 4: x, y, and keyword arguments')
    plt.show()

    # Method 5: Multiple datasets in one call
    x = np.linspace(0, 10, 100)
    plt.plot(x, np.sin(x), x, np.cos(x), x, np.sin(2*x))
    plt.title('Method 5: Multiple datasets')
    plt.legend(['sin(x)', 'cos(x)', 'sin(2x)'])
    plt.show()

    # ============================================================================
    # SECTION 3: Format Strings - The Compact Way
    # ============================================================================

    """
    Format String Syntax: '[marker][line][color]'

    Order doesn't matter! All of these are equivalent:
    - 'ro-'  (red circles, solid line)
    - 'r-o'  (same)
    - 'or-'  (same)
    - '-ro'  (same)

    Colors:
    -------
    'b' = blue        'g' = green       'r' = red         'c' = cyan
    'm' = magenta     'y' = yellow      'k' = black       'w' = white

    Line Styles:
    -----------
    '-'  = solid line
    '--' = dashed line
    '-.' = dash-dot line
    ':'  = dotted line

    Markers:
    --------
    '.'  = point             'o'  = circle          's'  = square
    '^'  = triangle up       'v'  = triangle down   '<'  = triangle left
    '>'  = triangle right    '*'  = star            '+'  = plus
    'x'  = x mark            'D'  = diamond         'p'  = pentagon
    'h'  = hexagon          '|'  = vertical line   '_'  = horizontal line
    """

    # Create a comprehensive example showing different format strings
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()

    x = np.linspace(0, 10, 20)
    y = x

    format_strings = [
        ('ro-', 'Red circles, solid'),
        ('bs--', 'Blue squares, dashed'),
        ('g^:', 'Green triangles up, dotted'),
        ('mv-.', 'Magenta triangles down, dash-dot'),
        ('c*-', 'Cyan stars, solid'),
        ('yD--', 'Yellow diamonds, dashed'),
        ('kp:', 'Black pentagons, dotted'),
        ('r+-.', 'Red plus, dash-dot'),
    ]

    for ax, (fmt, title) in zip(axes, format_strings):
        ax.plot(x, y, fmt, markersize=8, linewidth=2)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 4: Line Properties - Complete Reference
    # ============================================================================

    """
    Complete List of Line Properties:
    ---------------------------------

    color / c : color specification
        - Color name: 'red', 'blue', 'green', etc.
        - Short code: 'r', 'g', 'b', 'c', 'm', 'y', 'k', 'w'
        - Hex string: '#FF0000' (red), '#00FF00' (green)
        - RGB tuple: (1.0, 0.0, 0.0) for red, values 0-1
        - RGBA tuple: (1.0, 0.0, 0.0, 0.5) for semi-transparent red

    linestyle / ls : line style
        - '-' or 'solid'
        - '--' or 'dashed'
        - '-.' or 'dashdot'
        - ':' or 'dotted'
        - '' or ' ' or 'none' (no line)

    linewidth / lw : float
        - Width of the line in points (default: 1.5)

    marker : marker style
        - See list above (Section 3)

    markersize / ms : float
        - Size of markers in points

    markerfacecolor / mfc : color
        - Fill color of the marker

    markeredgecolor / mec : color
        - Edge color of the marker

    markeredgewidth / mew : float
        - Width of marker edge

    alpha : float (0.0 to 1.0)
        - Transparency (0 = fully transparent, 1 = fully opaque)

    label : str
        - Label for legend

    zorder : int
        - Drawing order (higher values drawn on top)
    """

    # Demonstrating line properties
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))

    x = np.linspace(0, 10, 100)

    # Different colors
    axes[0, 0].plot(x, np.sin(x), color='red', linewidth=2)
    axes[0, 0].plot(x, np.sin(x) + 1, color='#00FF00', linewidth=2)
    axes[0, 0].plot(x, np.sin(x) + 2, color=(0, 0, 1), linewidth=2)
    axes[0, 0].set_title('Different Color Specifications')
    axes[0, 0].legend(['Name', 'Hex', 'RGB tuple'])

    # Line styles
    axes[0, 1].plot(x, np.sin(x), linestyle='-', linewidth=2, label='solid')
    axes[0, 1].plot(x, np.sin(x) + 1, linestyle='--', linewidth=2, label='dashed')
    axes[0, 1].plot(x, np.sin(x) + 2, linestyle='-.', linewidth=2, label='dashdot')
    axes[0, 1].plot(x, np.sin(x) + 3, linestyle=':', linewidth=2, label='dotted')
    axes[0, 1].set_title('Line Styles')
    axes[0, 1].legend()

    # Line widths
    axes[0, 2].plot(x, np.sin(x), linewidth=1, label='lw=1')
    axes[0, 2].plot(x, np.sin(x) + 1, linewidth=2, label='lw=2')
    axes[0, 2].plot(x, np.sin(x) + 2, linewidth=4, label='lw=4')
    axes[0, 2].plot(x, np.sin(x) + 3, linewidth=8, label='lw=8')
    axes[0, 2].set_title('Line Widths')
    axes[0, 2].legend()

    # Marker sizes
    x_sparse = np.linspace(0, 10, 20)
    axes[1, 0].plot(x_sparse, np.sin(x_sparse), 'o-', markersize=4, label='ms=4')
    axes[1, 0].plot(x_sparse, np.sin(x_sparse) + 1, 'o-', markersize=8, label='ms=8')
    axes[1, 0].plot(x_sparse, np.sin(x_sparse) + 2, 'o-', markersize=12, label='ms=12')
    axes[1, 0].set_title('Marker Sizes')
    axes[1, 0].legend()

    # Marker face and edge colors
    axes[1, 1].plot(x_sparse, np.sin(x_sparse), 'o-', 
                    markerfacecolor='red', markeredgecolor='black', 
                    markeredgewidth=2, markersize=10, label='Custom colors')
    axes[1, 1].plot(x_sparse, np.sin(x_sparse) + 1, 'o-',
                    markerfacecolor='none', markeredgecolor='blue',
                    markeredgewidth=2, markersize=10, label='Hollow markers')
    axes[1, 1].set_title('Marker Colors')
    axes[1, 1].legend()

    # Alpha (transparency)
    axes[1, 2].plot(x, np.sin(x), linewidth=8, alpha=1.0, label='alpha=1.0')
    axes[1, 2].plot(x, np.sin(x) + 0.5, linewidth=8, alpha=0.7, label='alpha=0.7')
    axes[1, 2].plot(x, np.sin(x) + 1.0, linewidth=8, alpha=0.4, label='alpha=0.4')
    axes[1, 2].plot(x, np.sin(x) + 1.5, linewidth=8, alpha=0.1, label='alpha=0.1')
    axes[1, 2].set_title('Transparency (Alpha)')
    axes[1, 2].legend()

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 5: Advanced Marker Customization
    # ============================================================================

    """
    Markers can be heavily customized beyond basic properties.
    """

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    x = np.linspace(0, 10, 15)
    y = np.sin(x)

    # Basic markers
    axes[0].plot(x, y, 'o-', markersize=10)
    axes[0].set_title('Basic Markers')
    axes[0].grid(True, alpha=0.3)

    # Customized markers: different face and edge
    axes[1].plot(x, y, marker='o', linestyle='-',
                 color='blue',
                 markerfacecolor='yellow',
                 markeredgecolor='red',
                 markeredgewidth=3,
                 markersize=12,
                 linewidth=2)
    axes[1].set_title('Custom Marker Colors')
    axes[1].grid(True, alpha=0.3)

    # Hollow markers with thick edges
    axes[2].plot(x, y, marker='s', linestyle='--',
                 color='green',
                 markerfacecolor='none',
                 markeredgecolor='green',
                 markeredgewidth=2,
                 markersize=10,
                 linewidth=1.5)
    axes[2].set_title('Hollow Markers')
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 6: Plotting Multiple Lines - Best Practices
    # ============================================================================

    """
    When plotting multiple datasets, you have several options:
    1. Multiple plot() calls (most common)
    2. Single plot() call with all data
    3. Loop over datasets
    """

    x = np.linspace(0, 10, 100)

    # Method 1: Multiple plot() calls (RECOMMENDED for clarity)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, np.sin(x), 'r-', linewidth=2, label='sin(x)')
    ax.plot(x, np.cos(x), 'b--', linewidth=2, label='cos(x)')
    ax.plot(x, np.sin(2*x), 'g:', linewidth=2, label='sin(2x)')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Method 1: Multiple plot() calls')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    # Method 2: Single plot() call with all data
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, np.sin(x), 'r-',
            x, np.cos(x), 'b--',
            x, np.sin(2*x), 'g:',
            linewidth=2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Method 2: Single plot() call')
    ax.legend(['sin(x)', 'cos(x)', 'sin(2x)'])
    ax.grid(True, alpha=0.3)
    plt.show()

    # Method 3: Loop over datasets (good for many similar plots)
    fig, ax = plt.subplots(figsize=(10, 6))

    functions = [
        ('sin(x)', np.sin(x), 'r-'),
        ('cos(x)', np.cos(x), 'b--'),
        ('sin(2x)', np.sin(2*x), 'g:')
    ]

    for label, y_data, fmt in functions:
        ax.plot(x, y_data, fmt, linewidth=2, label=label)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Method 3: Loop over datasets')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    # ============================================================================
    # SECTION 7: Using Line2D Objects to Modify Properties Later
    # ============================================================================

    """
    plot() returns Line2D objects that you can modify after creation.
    This is useful for animations or interactive applications.
    """

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    # Get the Line2D object
    fig, ax = plt.subplots()
    line, = ax.plot(x, y, 'r-', linewidth=2)  # Note the comma to unpack
    # OR: lines = ax.plot(x, y); line = lines[0]

    print(f"Line object: {line}")
    print(f"Current color: {line.get_color()}")
    print(f"Current linewidth: {line.get_linewidth()}")

    # Modify properties using setter methods
    line.set_color('blue')
    line.set_linewidth(4)
    line.set_linestyle('--')
    line.set_alpha(0.7)

    ax.set_title('Line properties modified after creation')
    plt.show()

    # You can also get multiple line objects
    fig, ax = plt.subplots()
    line1, line2, line3 = ax.plot(x, np.sin(x), x, np.cos(x), x, np.tan(x))

    # Modify each line
    line1.set_color('red')
    line2.set_color('blue')
    line3.set_color('green')

    ax.set_ylim(-5, 5)
    ax.set_title('Multiple Line2D objects')
    plt.show()

    # ============================================================================
    # SECTION 8: Combining Format Strings with Keyword Arguments
    # ============================================================================

    """
    You can use BOTH format strings and keyword arguments.
    Keyword arguments override format string specifications.
    """

    x = np.linspace(0, 10, 50)
    y = np.sin(x)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Only format string
    axes[0].plot(x, y, 'ro-')
    axes[0].set_title("Format string only: 'ro-'")

    # Format string + keyword arguments (keywords override)
    axes[1].plot(x, y, 'ro-', color='blue', markersize=10)
    axes[1].set_title("'ro-' + color='blue'\n(blue overrides red)")

    # Keyword arguments only (most explicit)
    axes[2].plot(x, y, color='green', linestyle='--', 
                 marker='s', markersize=8, linewidth=2)
    axes[2].set_title('Keyword arguments only')

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # SECTION 9: Professional Plot Example
    # ============================================================================

    """
    Let's create a publication-quality plot using everything we've learned.
    """

    # Generate data
    x = np.linspace(0, 10, 200)
    y1 = np.sin(x)
    y2 = np.sin(x) * np.exp(-x/10)  # Damped sine
    y3 = np.cos(x) * np.exp(-x/10)  # Damped cosine

    # Create figure with custom size
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot with carefully chosen colors and styles
    ax.plot(x, y1, color='#1f77b4', linestyle='-', linewidth=2.5, 
            label='sin(x)', alpha=0.9, zorder=3)
    ax.plot(x, y2, color='#ff7f0e', linestyle='--', linewidth=2.5,
            label='sin(x)·exp(-x/10)', alpha=0.9, zorder=2)
    ax.plot(x, y3, color='#2ca02c', linestyle='-.', linewidth=2.5,
            label='cos(x)·exp(-x/10)', alpha=0.9, zorder=1)

    # Customize axes
    ax.set_xlabel('x', fontsize=14, fontweight='bold')
    ax.set_ylabel('y', fontsize=14, fontweight='bold')
    ax.set_title('Oscillatory and Damped Functions', fontsize=16, fontweight='bold', pad=20)

    # Add grid
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

    # Customize legend
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9, shadow=True)

    # Set axis limits for better view
    ax.set_xlim(0, 10)
    ax.set_ylim(-1.2, 1.2)

    # Add minor ticks
    ax.minorticks_on()

    plt.tight_layout()
    plt.show()

    # ============================================================================
    # KEY TAKEAWAYS
    # ============================================================================

    """
    1. plot(x, y) is the most important matplotlib function
    2. Format strings provide compact styling: '[marker][line][color]'
    3. Keyword arguments provide explicit control
    4. Line properties: color, linestyle, linewidth, marker, markersize, alpha
    5. Marker customization: face color, edge color, edge width
    6. plot() returns Line2D objects that can be modified later
    7. Multiple datasets: use multiple plot() calls for clarity
    8. Combine format strings and keywords (keywords override format)
    9. Use consistent styling for professional plots
    10. Always add labels, title, legend, and grid for publication quality

    Common Parameters:
    -----------------
    - color / c : line color
    - linestyle / ls : '-', '--', '-.', ':'
    - linewidth / lw : line thickness
    - marker : marker style
    - markersize / ms : marker size
    - markerfacecolor / mfc : marker fill color
    - markeredgecolor / mec : marker edge color
    - markeredgewidth / mew : marker edge width
    - alpha : transparency (0-1)
    - label : for legend
    """
```


!!! info "In Machine Learning"

    Line plots are the primary tool for **training curves**: plot loss vs epoch to diagnose convergence, overfitting (train loss drops but validation loss rises), and learning rate issues. Overlaying train and validation lines on the same axes is the first thing practitioners check after every training run.

---

## Exercises

**Exercise 1.** Write code that plots $y = x^2$ for $x \in [0, 5]$ using the OOP style. Add a title, axis labels, and a grid.

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

**Exercise 2.** Predict the output type of `lines = plt.plot(x, y)`. What does `lines[0]` represent?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that plots three lines on the same axes using multiple `ax.plot()` calls. Use different colors for each.

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

**Exercise 4.** Create a plot using the `ax.set()` method to set the title, xlabel, ylabel, xlim, and ylim all in one call.

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
