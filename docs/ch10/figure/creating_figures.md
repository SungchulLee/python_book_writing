# Creating Figures

The Figure object is the top-level container for all plot elements in Matplotlib.

!!! tip "Mental Model"
    A Figure is a blank sheet of paper. It has a size (`figsize`), a resolution (`dpi`), and a background color, but no data until you add Axes to it. You can create Figures explicitly with `plt.figure()` or implicitly when `plt.subplots()` builds one for you.

!!! note "The Matplotlib Hierarchy"
    ```text
    Figure  →  the whole canvas (size, background, export)
      └── Axes  →  a single plot area (data, labels, limits)
            └── Artists  →  individual visual elements (lines, text, patches)
    ```
    Every plotting command operates at one of these levels. `fig.suptitle()` is Figure-level; `ax.plot()` is Axes-level; `line.set_color()` is Artist-level. Confusing which level you need is the #1 beginner mistake.

!!! tip "Which Method to Use"
    | Need | Use | Why |
    |---|---|---|
    | Standard grid of subplots | `plt.subplots(nrows, ncols)` | Default — simplest, returns fig + axes |
    | Axes at arbitrary positions | `fig.add_axes([l, b, w, h])` | Normalized coordinates for custom layouts |
    | Inset or overlay plot | `ax.inset_axes([l, b, w, h])` | Axes within axes |
    | Legacy / incremental | `plt.subplot(nrows, ncols, idx)` | Avoid in new code; less flexible |

---

## Using plt.figure

Create an empty figure:

```python
import matplotlib.pyplot as plt

fig = plt.figure()
plt.show()
```

With size specification:

```python
fig = plt.figure(figsize=(10, 4))
```

The `figsize` parameter takes `(width, height)` in inches.

---

## Using plt.subplots

The most common way to create a figure with axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
plt.show()
```

---

## Adding Axes with fig.add_axes

For precise axes positioning, use `fig.add_axes`:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 2, 1000)
y1 = np.cos(40 * x)
y2 = np.exp(-x**2)

fig = plt.figure()

# Axes coordinates: [left, bottom, width, height] (0 to 1)
left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
ax = fig.add_axes((left, bottom, width, height))

ax.plot(x, y1 * y2)
ax.plot(x, y2, 'g')
ax.plot(x, -y2, 'g')
ax.set_xlabel("x")
ax.set_ylabel("y")

plt.show()
```

---

## Adding Axes with fig.add_subplot

Add subplots one at a time:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 50)
y1 = x ** 2
y2 = np.sqrt(x)

fig = plt.figure(figsize=(12, 6))

for s in range(11):
    ax = fig.add_subplot(3, 4, s + 1)
    if s % 2 == 0:
        ax.plot(y1, label=f"state {s}")
    else:
        ax.plot(y2, label=f"state {s}")

plt.show()
```

---

## Creating Inset Axes

Use multiple `add_axes` calls for inset plots:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 3, 50)
y1 = x ** 2
y2 = np.sqrt(x)

fig = plt.figure()

ax0 = fig.add_axes([0.1, 0.1, 0.8, 0.8])  # Main axes
ax1 = fig.add_axes([0.2, 0.5, 0.4, 0.3])  # Inset axes

ax0.plot(x, y1)  # Main figure
ax1.plot(y1, x)  # Inset

plt.show()
```

---

## Figure Keywords

Common `plt.figure` parameters:

```python
fig = plt.figure(
    figsize=(8, 6),        # Size in inches
    dpi=100,               # Dots per inch
    facecolor='#f1f1f1',   # Background color
    edgecolor='black',     # Border color
    linewidth=2            # Border width
)
```

---

## Figure Title

Add a title to the entire figure (spanning all subplots):

```python
import matplotlib.pyplot as plt

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 3))
fig.suptitle("My Figure Title", fontsize=20)

ax0.plot([1, 2, 3])
ax1.plot([3, 2, 1])

plt.show()
```

---

## Key Takeaways

- `plt.figure()` creates an empty figure
- `plt.subplots()` creates figure and axes together
- `fig.add_axes()` gives precise position control
- `fig.add_subplot()` adds subplots one at a time
- `figsize=(width, height)` sets size in inches


---

## Exercises

**Exercise 1.** Write code that creates a figure using `plt.subplots()` with `figsize=(10, 4)`, plots $y = \sin(x)$ on it, and adds a title and axis labels.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 2 * np.pi, 200)
    y = np.sin(x)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(x, y, 'b-', lw=2)
    ax.set_title(r'$y = \sin(x)$')
    ax.set_xlabel('$x$')
    ax.set_ylabel('$y$')
    plt.show()
    ```

---

**Exercise 2.** Predict the difference between `plt.figure()` followed by `fig.add_subplot(1, 1, 1)` versus using `plt.subplots()`. Which approach is more concise for creating a single plot?

??? success "Solution to Exercise 2"
    Both approaches create a figure with a single Axes object. However, `plt.subplots()` is more concise because it creates both the Figure and Axes in one call and returns them as a tuple:

    ```python
    # Approach 1: Two steps
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Approach 2: One step (more concise)
    fig, ax = plt.subplots()
    ```

    `plt.subplots()` is the recommended approach for most use cases because it is more readable and returns both objects directly.

---

**Exercise 3.** Create a figure with an inset plot using `fig.add_axes()`. The main plot should show $y = x^2$ for $x \in [0, 5]$, and the inset (positioned in the upper-left corner) should show a zoomed-in view of the same function for $x \in [0, 1]$.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 5, 200)
    y = x ** 2

    fig = plt.figure(figsize=(8, 6))
    ax_main = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    ax_main.plot(x, y, 'b-', lw=2)
    ax_main.set_xlabel('$x$')
    ax_main.set_ylabel('$y$')
    ax_main.set_title('$y = x^2$ with Inset')

    ax_inset = fig.add_axes([0.2, 0.55, 0.3, 0.3])
    x_zoom = np.linspace(0, 1, 100)
    ax_inset.plot(x_zoom, x_zoom ** 2, 'r-', lw=2)
    ax_inset.set_title('Zoom: $x \in [0, 1]$', fontsize=9)

    plt.show()
    ```

---

**Exercise 4.** Write code that creates a 3x4 grid of subplots using `fig.add_subplot()` in a loop. In each subplot, plot either $y = x^2$ or $y = \sqrt{x}$ alternating, and set the title to the subplot index.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 1, 50)

    fig = plt.figure(figsize=(14, 8))
    for i in range(12):
        ax = fig.add_subplot(3, 4, i + 1)
        if i % 2 == 0:
            ax.plot(x, x ** 2, 'b-')
            ax.set_title(f'#{i}: $x^2$', fontsize=9)
        else:
            ax.plot(x, np.sqrt(x), 'r-')
            ax.set_title(f'#{i}: $\sqrt{{x}}$', fontsize=9)

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 5.** Explain the difference between `fig.add_axes([0.1, 0.1, 0.8, 0.4])` and `fig.add_subplot(2, 1, 1)`. What coordinate system does `add_axes` use? Create a figure with one main axes and one small overlay axes using `add_axes`, positioning the overlay in the bottom-left corner at 20% width and 20% height.

??? success "Solution to Exercise 5"

    `add_axes([left, bottom, width, height])` uses **normalized figure coordinates** — each value is a fraction of the figure's total width/height (0 to 1). `[0.1, 0.1, 0.8, 0.4]` means: start at 10% from the left edge, 10% from the bottom, span 80% of the width and 40% of the height.

    `add_subplot(nrows, ncols, index)` uses a grid-based system that automatically computes the position.

    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure(figsize=(8, 6))

    # Main axes: most of the figure
    ax_main = fig.add_axes([0.1, 0.3, 0.85, 0.6])
    x = np.linspace(0, 10, 100)
    ax_main.plot(x, np.sin(x))
    ax_main.set_title('Main Plot')

    # Overlay: bottom-left, 20% width and height
    ax_small = fig.add_axes([0.15, 0.05, 0.2, 0.2])
    ax_small.plot(x, np.cos(x), 'r-')
    ax_small.set_title('Overlay', fontsize=8)

    plt.show()
    ```
