# Line2D and Artists

!!! tip "Mental Model"
    Every visible element on a Matplotlib plot — every line, text label, axis tick, legend entry — is an Artist object. `Line2D` is the Artist created by `ax.plot()`. Once you realize that plotting commands return Artists, you can grab them, inspect their properties with `get_*()`, and modify them with `set_*()` after the fact.

!!! note "Artists = Visual Encoding"
    Artists are the concrete implementation of visual variables. Each plot command creates a specific Artist type:

    | Plot command | Artist created | Visual variable |
    |---|---|---|
    | `ax.plot()` | `Line2D` | Position, color, linestyle |
    | `ax.scatter()` | `PathCollection` | Position, size, color |
    | `ax.bar()` | `Rectangle` (Patch) | Height, color |
    | `ax.text()` | `Text` | Position, content, font |
    | `ax.imshow()` | `AxesImage` | Color map of 2D data |

    Understanding this mapping means you can modify any aspect of a plot after creation by accessing the returned Artist and calling its `set_*()` methods.

## Artist Base Class

### 1. Hierarchy

All plot elements inherit from Artist:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
line, = ax.plot([1, 2, 3])
print(isinstance(line, plt.Artist))  # True
```

### 2. Properties

```python
line.set_color('red')
line.set_linewidth(2)
line.set_linestyle('--')
line.set_marker('o')
line.set_markersize(8)
```

### 3. Visibility

```python
line.set_visible(False)
line.set_alpha(0.5)  # Transparency
```

## Line2D

### 1. Creation

```python
from matplotlib.lines import Line2D

line = Line2D([0, 1, 2], [0, 1, 0], color='blue', linewidth=2)
ax.add_line(line)
```

### 2. Properties

```python
line.set_xdata([0, 1, 2, 3])
line.set_ydata([0, 1, 0, 1])
line.set_label('Custom Line')
```

### 3. Markers

```python
line.set_marker('o')
line.set_markerfacecolor('yellow')
line.set_markeredgecolor('black')
line.set_markeredgewidth(1)
```

## Other Artists

### 1. Text

```python
text = ax.text(0.5, 0.5, 'Hello', fontsize=14)
text.set_color('red')
text.set_rotation(45)
```

### 2. Patch

```python
from matplotlib.patches import Rectangle

rect = Rectangle((0, 0), 1, 1, facecolor='lightblue', edgecolor='blue')
ax.add_patch(rect)
```

### 3. Collection

```python
from matplotlib.collections import LineCollection

segments = [[(0, 0), (1, 1)], [(1, 0), (0, 1)]]
lc = LineCollection(segments, colors='red', linewidths=2)
ax.add_collection(lc)
```


## The One Abstraction

Every Artist is a **stateful object with properties and a `draw()` method**. That's it. Lines, text, patches, ticks, legends --- they all follow the same pattern:

```python
artist.set_color('red')     # change a property
artist.get_linewidth()       # read a property
artist.set_visible(False)    # hide it
```

## Debugging with Artists

When a plot looks wrong, inspect the Artist tree:

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])

# List all artists on the axes
for child in ax.get_children():
    print(type(child).__name__, getattr(child, 'get_label', lambda: '')())

# Inspect a specific line
lines = ax.get_lines()
for line in lines:
    print(f"color={line.get_color()}, lw={line.get_linewidth()}, visible={line.get_visible()}")
```

Common issues:

- **Plot not showing?** → Check `artist.get_visible()` and axis limits
- **Wrong z-order?** → Check `artist.get_zorder()` --- higher values draw on top
- **Plot not updating?** → Call `fig.canvas.draw()` after modifying Artists

---

## Exercises

**Exercise 1.** Write code that creates a plot and uses `ax.get_children()` to list all Artist objects. Print the type of each child.

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

**Exercise 2.** Explain the Matplotlib Artist hierarchy. What is the base class for all drawable objects in Matplotlib?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that creates a Line2D object with `ax.plot()`, then modifies its properties using setter methods (e.g., `line.set_color()`).

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

**Exercise 4.** Create a plot and manually add a `matplotlib.patches.Rectangle` to the axes using `ax.add_patch()`.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
        import numpy as np

        fig, ax = plt.subplots()
        x = np.linspace(0, 10, 100)
        ax.plot(x, np.sin(x), 'b-')

        # Manually create and add a Rectangle Artist
        rect = mpatches.Rectangle((2, -0.5), 3, 1,
                                   linewidth=2, edgecolor='red',
                                   facecolor='yellow', alpha=0.3)
        ax.add_patch(rect)

        ax.set_title('Line2D + manually added Rectangle')
        plt.show()

        # The Rectangle is a Patch Artist — same base class as bars in bar charts.
        # add_patch() inserts it into the Axes' artist list for rendering.

---

**Exercise 5.** Demonstrate the `set_*()` / `get_*()` pattern. Create a line plot and then modify it after creation: change the line color, width, linestyle, and marker using only `set_*()` methods on the returned `Line2D` object. Print the properties before and after using `get_color()`, `get_linewidth()`, etc.

??? success "Solution to Exercise 5"

        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots()
        x = np.linspace(0, 5, 30)
        line, = ax.plot(x, np.cos(x))

        # Before modification
        print(f"Color:     {line.get_color()}")
        print(f"Linewidth: {line.get_linewidth()}")
        print(f"Linestyle: {line.get_linestyle()}")

        # Modify via set_*() — no need to replot
        line.set_color('red')
        line.set_linewidth(3)
        line.set_linestyle('--')
        line.set_marker('o')
        line.set_markersize(6)

        # After modification
        print(f"\nAfter set_*():")
        print(f"Color:     {line.get_color()}")
        print(f"Linewidth: {line.get_linewidth()}")
        print(f"Linestyle: {line.get_linestyle()}")

        ax.set_title('Modified Line2D (red, dashed, markers)')
        plt.show()

        # This is the Artist mutation model: create once, modify freely.
        # The plot updates when drawn — no need to recreate the figure.

    Refer to the code examples in the main content for the specific API calls needed.
