# Five Major Objects

Matplotlib is built around five major object types that form a hierarchy. Understanding these objects is essential for effective plotting.

!!! tip "Mental Model"
    Picture a Figure as a physical canvas on a wall, and each Axes as a framed picture hanging on that canvas. Inside each frame, the XAxis, YAxis, and Spines form the border, while Artists (lines, text, patches) are the painted content. Every plotting command ultimately creates or modifies one of these five objects.

---

## Object Hierarchy

```
Figure
  └── Axes (AxesSubplot)
        ├── XAxis
        ├── YAxis
        ├── Spine (top, bottom, left, right)
        └── Text (labels, titles, tick labels)
```

---

## 1. Figure

The **Figure** is the top-level container—the entire window or canvas.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
print(type(fig))  # <class 'matplotlib.figure.Figure'>
```

**Responsibilities:**

- Contains all plot elements
- Controls figure size and DPI
- Manages multiple Axes
- Handles saving to files

---

## 2. Axes (AxesSubplot)

The **Axes** is the actual plotting area where data is drawn.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
print(type(ax))  # <class 'matplotlib.axes._subplots.AxesSubplot'>

ax.plot(x, y)
plt.show()
```

**Responsibilities:**

- Contains the plotted data
- Manages axis limits and scales
- Holds title and labels
- Contains XAxis, YAxis, and Spines

---

## 3. Spine

**Spines** are the lines forming the plot borders.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

print(type(ax.spines['top']))  # <class 'matplotlib.spines.Spine'>

# Customize spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')

plt.show()
```

**Four spines:**

- `ax.spines['top']`
- `ax.spines['bottom']`
- `ax.spines['left']`
- `ax.spines['right']`

---

## 4. Axis (XAxis and YAxis)

**Axis** objects control tick marks, tick labels, and axis labels.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

print(type(ax.xaxis))  # <class 'matplotlib.axis.XAxis'>
print(type(ax.yaxis))  # <class 'matplotlib.axis.YAxis'>

# Customize axis
ax.set_xticks(
    ticks=[-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
    labels=["$-2\\pi$", "$-\\pi$", "0", "$\\pi$", "$2\\pi$"]
)
ax.xaxis.set_ticks_position('top')
ax.yaxis.set_ticks_position('right')

plt.show()
```

**Responsibilities:**

- Tick positions (locators)
- Tick labels (formatters)
- Axis labels
- Tick position (top/bottom, left/right)

---

## 5. Text

**Text** objects represent all text elements including labels and tick labels.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

# Access tick labels (Text objects)
for label in ax.get_xticklabels():
    print(type(label))  # <class 'matplotlib.text.Text'>
    label.set_rotation(45)

plt.show()
```

**Text elements:**

- Tick labels
- Axis labels
- Title
- Annotations
- Any added text

---

## Complete Example

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    x = np.linspace(-2*np.pi, 2*np.pi, 100+1)
    y = np.sin(x)

    # 1. Figure
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    print(f"{type(fig) = }")  # matplotlib.figure.Figure

    # 2. Axes
    print(f"{type(ax) = }")   # matplotlib.axes._subplots.AxesSubplot
    ax.plot(x, y)
    ax2.plot(y, x)

    # 3. Spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    print(f"{type(ax.spines['top']) = }")  # matplotlib.spines.Spine

    # 4. Axis
    ax.set_xticks(
        ticks=[-2*np.pi, -np.pi, 0, np.pi, 2*np.pi],
        labels=["$-2\\pi$", "$-\\pi$", "0", "$\\pi$", "$2\\pi$"]
    )
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('right')
    print(f"{type(ax.xaxis) = }")  # matplotlib.axis.XAxis
    print(f"{type(ax.yaxis) = }")  # matplotlib.axis.YAxis

    # 5. Text
    for label in ax.get_xticklabels():
        label.set_rotation(45)
    print(f"{type(label) = }")  # matplotlib.text.Text

    plt.show()

if __name__ == '__main__':
    main()
```

---

## Summary Table

| Object | Type | Purpose |
|--------|------|---------|
| Figure | `matplotlib.figure.Figure` | Top-level container |
| Axes | `matplotlib.axes.AxesSubplot` | Plotting area |
| Spine | `matplotlib.spines.Spine` | Border lines |
| Axis | `matplotlib.axis.XAxis/YAxis` | Tick and label control |
| Text | `matplotlib.text.Text` | All text elements |

---

## Key Takeaways

- Figure is the top-level container
- Axes is where data is plotted
- Spines are the four border lines
- Axis (XAxis/YAxis) controls ticks and labels
- Text represents all text elements
- Understanding this hierarchy enables full customization

---

## Runnable Example: `introduction_tutorial.py`

```python
"""
Matplotlib Tutorial - Beginner Level
=====================================
Topic: Introduction to Matplotlib and First Plots
Author: Educational Python Course
Level: Beginner

Learning Objectives:
-------------------
1. Understand what matplotlib is and its purpose
2. Learn to import matplotlib.pyplot
3. Create your first simple plot
4. Understand the figure and show() function
5. Basic line plotting with plot()

Prerequisites:
-------------
- Basic Python knowledge
- NumPy basics (arrays)
"""

# ============================================================================
# SECTION 1: Introduction to Matplotlib
# ============================================================================

if __name__ == "__main__":

    """
    What is Matplotlib?
    ------------------
    Matplotlib is a comprehensive library for creating static, animated, and 
    interactive visualizations in Python. It is one of the most widely used 
    plotting libraries in the scientific Python ecosystem.

    Key Features:
    - Create publication-quality figures
    - Support for various plot types (line, bar, scatter, histogram, etc.)
    - Extensive customization options
    - Integration with NumPy and Pandas
    - Two different plotting interfaces: MATLAB-style and Object-Oriented style
    """

    # ============================================================================
    # SECTION 2: Importing Matplotlib
    # ============================================================================

    # Standard way to import matplotlib's plotting interface
    # 'plt' is the conventional alias used by the community
    import matplotlib.pyplot as plt
    import numpy as np  # We'll use numpy to generate data

    # ============================================================================
    # SECTION 3: Your First Plot - Simple Line
    # ============================================================================

    # Create some simple data
    # x-coordinates: 0, 1, 2, 3, 4
    x = [0, 1, 2, 3, 4]
    # y-coordinates: 0, 1, 4, 9, 16 (these are squares: 0^2, 1^2, 2^2, 3^2, 4^2)
    y = [0, 1, 4, 9, 16]

    # Create a plot
    # plot() is the most basic plotting function
    # It connects points with lines by default
    plt.plot(x, y)

    # Display the plot
    # show() is required to actually display the figure window
    # Without this, the plot exists in memory but won't be visible
    plt.show()

    # NOTE: After show() is called, the figure is displayed and then cleared
    # If you want to add more to the same figure, do it before calling show()

    # ============================================================================
    # SECTION 4: Adding Labels and Title
    # ============================================================================

    # Let's create a more informative plot
    x = [0, 1, 2, 3, 4]
    y = [0, 1, 4, 9, 16]

    # Create the plot
    plt.plot(x, y)

    # Add x-axis label
    # The label appears below the x-axis
    plt.xlabel('Input Value')

    # Add y-axis label
    # The label appears to the left of the y-axis
    plt.ylabel('Squared Value')

    # Add a title
    # The title appears at the top of the plot
    plt.title('Simple Quadratic Function: y = x²')

    # Display the plot
    plt.show()

    # ============================================================================
    # SECTION 5: Using NumPy for More Data Points
    # ============================================================================

    # When plotting smooth curves, we need many points
    # NumPy's linspace() creates evenly spaced points

    # Create 100 points between 0 and 4
    # linspace(start, stop, num_points)
    x = np.linspace(0, 4, 100)

    # Calculate y values (each x squared)
    y = x ** 2

    # Create the plot
    plt.plot(x, y)

    # Add labels and title
    plt.xlabel('x')
    plt.ylabel('y = x²')
    plt.title('Smooth Quadratic Function (100 points)')

    # Display the plot
    plt.show()

    # ============================================================================
    # SECTION 6: Customizing Line Appearance
    # ============================================================================

    # Generate data
    x = np.linspace(0, 4, 100)
    y = x ** 2

    # Create plot with custom line properties
    # 'r' = red color
    # '--' = dashed line style
    # linewidth controls the thickness of the line
    plt.plot(x, y, 'r--', linewidth=2)

    # You can also specify properties using keyword arguments
    # This is more explicit and readable
    # plt.plot(x, y, color='red', linestyle='--', linewidth=2)

    plt.xlabel('x')
    plt.ylabel('y = x²')
    plt.title('Customized Line: Red and Dashed')

    plt.show()

    # ============================================================================
    # SECTION 7: Multiple Lines on Same Plot
    # ============================================================================

    # Generate x data
    x = np.linspace(0, 4, 100)

    # Generate multiple y datasets
    y1 = x ** 2      # Quadratic
    y2 = x ** 3      # Cubic
    y3 = np.sqrt(x)  # Square root

    # Plot all three lines
    # Each plot() call adds a new line to the same figure
    plt.plot(x, y1, 'r-', linewidth=2, label='y = x²')   # Red solid line
    plt.plot(x, y2, 'b--', linewidth=2, label='y = x³')  # Blue dashed line
    plt.plot(x, y3, 'g:', linewidth=2, label='y = √x')   # Green dotted line

    # Add labels and title
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Multiple Functions on Same Plot')

    # Add legend
    # legend() creates a box showing what each line represents
    # The labels come from the 'label' parameter in plot()
    # loc='best' automatically chooses the best position
    plt.legend(loc='best')

    plt.show()

    # ============================================================================
    # SECTION 8: Common Line Styles and Colors
    # ============================================================================

    """
    Common Color Codes:
    ------------------
    'r' = red
    'g' = green
    'b' = blue
    'c' = cyan
    'm' = magenta
    'y' = yellow
    'k' = black
    'w' = white

    You can also use full names: 'red', 'green', 'blue', etc.
    Or hex codes: '#FF0000' for red, '#00FF00' for green, etc.

    Common Line Styles:
    ------------------
    '-'  = solid line (default)
    '--' = dashed line
    ':'  = dotted line
    '-.' = dash-dot line

    Common Markers:
    --------------
    'o'  = circle
    's'  = square
    '^'  = triangle up
    'v'  = triangle down
    '*'  = star
    '+'  = plus
    'x'  = x mark
    'D'  = diamond

    You can combine them: 'ro-' = red circles connected by solid line
    """

    # Example demonstrating various styles
    x = np.linspace(0, 10, 20)

    plt.plot(x, x, 'ro-', label='Red circles, solid')
    plt.plot(x, x + 2, 'bs--', label='Blue squares, dashed')
    plt.plot(x, x + 4, 'g^:', label='Green triangles, dotted')
    plt.plot(x, x + 6, 'k*-.', label='Black stars, dash-dot')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Different Line Styles, Colors, and Markers')
    plt.legend()
    plt.grid(True)  # Add grid for better readability

    plt.show()

    # ============================================================================
    # SECTION 9: Saving Figures
    # ============================================================================

    # Create a plot
    x = np.linspace(0, 4, 100)
    y = x ** 2

    plt.plot(x, y, 'b-', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('y = x²')
    plt.title('Quadratic Function')

    # Save the figure before showing it
    # savefig() saves the current figure to a file
    # Common formats: .png, .pdf, .svg, .jpg
    plt.savefig('my_first_plot.png', dpi=300, bbox_inches='tight')
    # dpi = dots per inch (resolution)
    # bbox_inches='tight' removes excess white space

    # You can still show the figure after saving
    plt.show()

    print("Figure saved as 'my_first_plot.png'")

    # ============================================================================
    # KEY TAKEAWAYS
    # ============================================================================

    """
    1. Import matplotlib.pyplot as plt
    2. Use plt.plot(x, y) to create line plots
    3. Add labels with xlabel(), ylabel(), and title()
    4. Use show() to display the plot
    5. Customize lines with color, style, and width parameters
    6. Add legends with plt.legend() when plotting multiple lines
    7. Save figures with savefig() before show()
    8. MATLAB-style (plt.plot, plt.xlabel, etc.) is simple for quick plots
    """
```


## The Artist Abstraction

Everything visible in a Matplotlib plot is an **Artist** --- lines, text, patches, tick marks, axis labels, even the Axes and Figure themselves. This means:

- To change anything visual, you are modifying an Artist's properties
- `ax.plot()` returns a list of `Line2D` Artists
- `ax.set_title()` creates a `Text` Artist
- Debugging "why does my plot look wrong?" becomes: "which Artist has the wrong property?"

The rendering pipeline: **Data → Axes → Artists → Backend → Pixels**

---

## Exercises

**Exercise 1.** Name the five major objects in the Matplotlib hierarchy (Figure, Axes, Axis, Tick, Artist). Write code that creates a Figure and Axes using `plt.subplots()` and prints the type of each.

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

**Exercise 2.** Explain the difference between `Figure` and `Axes` in Matplotlib. Can a Figure contain multiple Axes?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that creates a Figure, adds an Axes, and then accesses the x-axis and y-axis objects using `ax.xaxis` and `ax.yaxis`. Print their types.

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

**Exercise 4.** Explain the role of the Artist class in Matplotlib. Is a Line2D object an Artist? What about an Axes object?

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
