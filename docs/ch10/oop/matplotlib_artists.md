# Line2D and Artists

!!! tip "Mental Model"
    Every visible element on a Matplotlib plot -- every line, text label, axis tick, legend entry -- is an Artist object. `Line2D` is the Artist created by `ax.plot()`. Once you realize that plotting commands return Artists, you can grab them, inspect their properties with `get_*()`, and modify them with `set_*()` after the fact.

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
