# Axes Basics

The Axes object is the core component for plotting in Matplotlib. It contains most plot elements including the data, axes, ticks, labels, and title.

!!! tip "Mental Model"
    An Axes is a single coordinate system -- the rectangle where data gets drawn. Every call like `ax.plot()`, `ax.set_title()`, or `ax.set_xlim()` targets one specific Axes. A Figure can hold many Axes, but each Axes is self-contained with its own ticks, labels, and data.

!!! note "Matplotlib Layout Model"
    All visualization in Matplotlib follows a five-layer system:

    ```text
    1. Figure       → the canvas (one per image/window)
    2. Axes         → independent coordinate systems (one per subplot)
    3. Layout       → how Axes are arranged (grid, freeform, flexible)
    4. Access       → how you reference each Axes (index, unpack, name)
    5. Encoding     → how data maps to visual elements (lines, bars, color)
    ```

    This section covers layers 1--4. The key insight: **layout is a semantic
    decision, not a cosmetic one** — the number and arrangement of Axes
    determines how many perspectives on the data the reader sees:

    | Layout | Meaning |
    |--------|---------|
    | 1 Axes | Single perspective |
    | 2 Axes side-by-side | Comparison |
    | Grid of Axes | Multiple scenarios / variables |
    | Inset Axes | Detail zoom |
    | Twin Axes | Same data, different units |

---

## What is an Axes Object

An Axes object encapsulates all elements of an individual (sub-)plot:

- X-axis and Y-axis (`Axis` objects)
- Ticks and tick labels
- Plot elements (`Line2D`, `Text`, `Polygon`, etc.)
- Coordinate system

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()

print(type(ax))  # <class 'matplotlib.axes._subplots.AxesSubplot'>
```

---

## Axes vs Figure

| Figure | Axes |
|--------|------|
| The whole canvas | A single plot area |
| Can contain multiple Axes | Contains one coordinate system |
| Top-level container | Where data is plotted |

```python
import matplotlib.pyplot as plt

# One figure, one axes
fig, ax = plt.subplots()

# One figure, four axes
fig, axes = plt.subplots(2, 2)
```

---

## Axes is a NumPy Array

When creating multiple subplots, `plt.subplots` returns a NumPy array of Axes:

```python
import matplotlib.pyplot as plt

fig, axes = plt.subplots(2, 2)

print(type(axes))   # <class 'numpy.ndarray'>
print(axes.shape)   # (2, 2)
print(axes.dtype)   # object
print(type(axes[0, 0]))  # AxesSubplot
```

---

## Accessing Individual Axes

Access axes using NumPy indexing:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)

fig, axes = plt.subplots(2, 2)

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title("sin")

axes[0, 1].plot(x, np.cos(x))
axes[0, 1].set_title("cos")

axes[1, 0].plot(x, np.sinh(x))
axes[1, 0].set_title("sinh")

axes[1, 1].plot(x, np.cosh(x))
axes[1, 1].set_title("cosh")

plt.tight_layout()
plt.show()
```

---

## Key Axes Properties

Important attributes of an Axes object:

```python
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
x = np.linspace(0, 1, 10)
ax.plot(x, x**2)

# Access components
print(ax.xaxis)      # XAxis object
print(ax.yaxis)      # YAxis object
print(ax.spines)     # Dictionary of Spine objects
print(ax.lines)      # List of Line2D objects
print(ax.patches)    # List of Patch objects
print(ax.texts)      # List of Text objects

plt.show()
```

---

## OOP Style Benefits

Using explicit Axes objects provides:

1. **Clear references**: Know exactly which plot you're modifying
2. **Flexibility**: Modify any axes at any time
3. **Reusability**: Pass axes to functions
4. **Complex layouts**: Handle multi-panel figures easily

```python
import matplotlib.pyplot as plt
import numpy as np

def plot_sine(ax, frequency=1):
    """Reusable plotting function that takes an axes."""
    x = np.linspace(0, 2*np.pi, 100)
    ax.plot(x, np.sin(frequency * x))
    ax.set_title(f"sin({frequency}x)")

fig, axes = plt.subplots(1, 3, figsize=(12, 3))

for i, ax in enumerate(axes):
    plot_sine(ax, frequency=i+1)

plt.tight_layout()
plt.show()
```

---

## Key Takeaways

- Axes is the main plotting area within a Figure
- `plt.subplots` returns a NumPy array of Axes objects
- Use NumPy indexing to access individual Axes
- OOP style with explicit Axes provides more control
- Each Axes contains its own coordinate system

---

## Exercises

**Exercise 1.**
Create a single Axes and plot both `y = x^2` and `y = x^3` for `x` in $[-2, 2]$. Customize the axes by setting x and y labels, a title, grid lines, and a legend. Also set the y-axis limits to $[-10, 10]$.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-2, 2, 200)

        fig, ax = plt.subplots()
        ax.plot(x, x**2, label=r'$y = x^2$')
        ax.plot(x, x**3, label=r'$y = x^3$')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title('Polynomial Functions')
        ax.set_ylim(-10, 10)
        ax.grid(True)
        ax.legend()
        plt.show()

---

**Exercise 2.**
Create a figure with one Axes. Plot random data (50 points) as a scatter plot. Then use the axes object to access and print: the x-axis limits (`get_xlim`), the y-axis limits (`get_ylim`), and the number of lines/collections in the axes (`len(ax.collections)`).

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        x = np.random.rand(50) * 10
        y = np.random.rand(50) * 10

        fig, ax = plt.subplots()
        ax.scatter(x, y, color='steelblue')

        print(f"X limits: {ax.get_xlim()}")
        print(f"Y limits: {ax.get_ylim()}")
        print(f"Number of collections: {len(ax.collections)}")

        plt.show()

---

**Exercise 3.**
Create an Axes and plot `y = sin(x)`. Then use the Axes methods to: set the background color to light gray (`set_facecolor`), remove the top and right spines, and set major grid lines with `alpha=0.3`. Show that the Axes is the central object controlling all visual elements.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 200)

        fig, ax = plt.subplots()
        ax.plot(x, np.sin(x), color='navy')

        ax.set_facecolor('#f0f0f0')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('x')
        ax.set_ylabel('sin(x)')
        ax.set_title('Customized Axes')
        plt.show()
