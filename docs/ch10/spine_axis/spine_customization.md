# Spine Customization

Spines are the lines that form the borders of the plotting area. This document covers spine basics, visibility control, and positioning.

!!! tip "Mental Model"
    Spines are the four border lines of the plot rectangle. By default all four are visible, but hiding the top and right spines instantly gives your plots a cleaner, more modern look. You can also reposition spines -- moving the bottom spine to `y=0` creates a traditional math-textbook axis through the origin.

    Spines, [ticks](tick_control.md), and labels together form the **axis system**
    — the visual frame that gives meaning to the data region. Customizing this
    frame is the **refinement layer** of the visualization pipeline (after data,
    plot type, and layout are decided).

!!! note "Axis System Theory"
    The axis system connects visual position to data values:

    - **Spines** → define the coordinate boundaries (reference lines)
    - **Ticks** → encode the scale (position → number)
    - **Tick labels** → provide numerical meaning

    Together, they implement the transformation: **data space → visual space.**
    Without the axis system, a plot is just colored shapes — the axis system is
    what makes it a quantitative representation. Moving or removing spines changes
    how the data is framed and interpreted.

!!! note "When to Customize Spines"
    | Goal | Technique |
    |------|-----------|
    | Cleaner modern look | Remove top + right spines |
    | Mathematical axes through origin | Position bottom/left at `'zero'` |
    | Image / heatmap display | Remove all spines |
    | Bounded axis range | Set spine bounds to data range |

    The design principle: **remove unnecessary visual elements to emphasize the
    data, not the frame.** Every spine, tick, or gridline that doesn't aid
    interpretation is clutter.

## What are Spines?

A plot has four spines:

- `'top'`: Upper border
- `'bottom'`: Lower border (x-axis line)
- `'left'`: Left border (y-axis line)
- `'right'`: Right border

Access spines through the `ax.spines` dictionary:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)

print(type(ax.spines['top']))  # <class 'matplotlib.spines.Spine'>
print(ax.spines.keys())        # ['left', 'right', 'bottom', 'top']

plt.show()
```

Each spine is a `Spine` object with methods for customization:

```python
spine = ax.spines['bottom']
# Available methods: set_visible, set_color, set_position, set_linewidth, etc.
```

---

## Spine Visibility

### set_visible

Hide or show individual spines:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()
```

### set_color to 'none'

An alternative way to hide spines:

```python
ax.spines['top'].set_color('none')
ax.spines['right'].set_color('none')
```

### Common Visibility Patterns

**Clean two-spine (L-shape):**
```python
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

**Bottom only:**
```python
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
```

**No spines:**
```python
for spine in ax.spines.values():
    spine.set_visible(False)
```

### set_linewidth

Control spine thickness:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()
```

### set_color

Change spine colors:

```python
ax.spines['bottom'].set_color('blue')
ax.spines['left'].set_color('blue')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
```

### Iterating Over Spines

Apply changes to all spines:

```python
for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_color('gray')
```

---

## Spine Position

### set_position

Move a spine to a specific location:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')
plt.show()
```

### Position Types

| Position Type | Description | Example |
|--------------|-------------|---------|
| `'zero'` | At data coordinate 0 | `set_position('zero')` |
| `'center'` | At axes center | `set_position('center')` |
| `('data', value)` | At specific data coordinate | `set_position(('data', -15))` |
| `('axes', fraction)` | Fraction of axes (0 to 1) | `set_position(('axes', 0.5))` |
| `('outward', points)` | Outward from data area | `set_position(('outward', 10))` |

### Centered Axes (Math Style)

Create a coordinate system centered at the origin:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)

# Hide top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Move bottom and left to zero
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')

plt.show()
```

### set_bounds

Limit the extent of a spine:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-5, 2, 100)
y1 = x**3 + 5*x**2 + 10
y2 = 3*x**2 + 10*x
y3 = 6*x + 10

fig, ax = plt.subplots()
ax.plot(x, y1, color="blue", label="y(x)", lw=2)
ax.plot(x, y2, color="red", label="y'(x)", lw=2)
ax.plot(x, y3, color="green", label='y"(x)', lw=2)

ax.axhline(0, color='k', lw=1)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_xticks([-4, -2, 0, 2])
ax.set_yticks([-10, 0, 10, 20, 30])

# Position and bound spines
ax.spines['bottom'].set_position(('data', -15))
ax.spines['left'].set_bounds(low=-15, high=41)
ax.spines['right'].set_bounds(low=-15, high=41)

ax.legend(ncol=3, loc=2, bbox_to_anchor=(0, 1), frameon=False)
plt.show()
```

### Arrow-Style Axis

Create arrows at the end of axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 100)
y = x ** 2

fig, ax = plt.subplots()
ax.plot(x, y)

# Position spines at zero
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Add arrows
ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

plt.show()
```

---

## Complete Example: Mathematical Function Plot

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y, 'b-', lw=2)

# Set up ticks
ax.set_yticks([-1, 0, 1])
ax.set_xticks([-2*np.pi, -np.pi, 0, np.pi, 2*np.pi])
ax.set_xticklabels(['$-2\\pi$', '$-\\pi$', '0', '$\\pi$', '$2\\pi$'])

# Minor ticks
ax.set_xticks(np.linspace(-2*np.pi, 2*np.pi, 17), minor=True)

# Configure spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_position('zero')
ax.spines['left'].set_position('zero')

ax.set_title('$y = \\sin(x)$', pad=20)
plt.show()
```

---

## Common Spine Configurations

| Configuration | Code | Use Case |
|--------------|------|----------|
| Two-spine (clean) | Hide top/right | Most plots |
| Centered axes | Position at 'zero' | Math functions |
| No spines | Hide all | Heatmaps, images |
| Bottom only | Hide top/right/left | Bar charts |

---

## Images with No Spines

For images, hide all spines and ticks:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.datasets import fetch_olivetti_faces

faces = fetch_olivetti_faces().images

fig, ax = plt.subplots(5, 5, figsize=(5, 5))
fig.subplots_adjust(hspace=0, wspace=0)

for i in range(5):
    for j in range(5):
        ax[i, j].xaxis.set_major_locator(mpl.ticker.NullLocator())
        ax[i, j].yaxis.set_major_locator(mpl.ticker.NullLocator())
        ax[i, j].imshow(faces[10 * i + j], cmap="bone")

plt.show()
```

---

## Key Takeaways

- Four spines: top, bottom, left, right
- Access via `ax.spines['name']` or `ax.spines.values()`
- `set_visible(False)` hides a spine
- `set_position('zero')` moves spine to data coordinate 0
- `set_bounds(low, high)` limits spine extent
- Removing top/right spines is a common clean style


---

## Exercises

**Exercise 1.** Write code that hides the top and right spines of a plot, creating a clean L-shaped axes frame. Plot $y = \sin(x)$.

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

**Exercise 2.** Explain what a spine is in Matplotlib. How many spines does a standard Axes have and what are their names?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that moves the bottom spine to `y=0` and the left spine to `x=0`, creating a centered coordinate system.

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

**Exercise 4.** Create a plot where only the bottom spine is visible, all other spines are hidden, and the remaining spine has a custom color and line width.

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
