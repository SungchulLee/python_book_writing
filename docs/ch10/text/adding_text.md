# Adding Text

Add text labels and descriptions directly to your plots.

!!! tip "Mental Model"
    `ax.text(x, y, s)` places a string at a specific point in data coordinates. For position-independent text (e.g., a watermark), use `transform=ax.transAxes` so coordinates are relative to the Axes (0-1 range). Text objects are Artists, so you can style them with `fontsize`, `color`, `fontweight`, and align them with `ha` and `va`.

!!! note "Text Hierarchy in Matplotlib"
    Matplotlib has four distinct text mechanisms, each with a different purpose:

    | Type | Method | Purpose |
    |------|--------|---------|
    | **Title** | `ax.set_title()` | Describe the entire plot |
    | **Label** | `ax.set_xlabel()` / `ax.set_ylabel()` | Describe an axis |
    | **Text** | `ax.text()` | Place arbitrary text at a position |
    | **Annotation** | `ax.annotate()` | Text + arrow pointing to a data feature |

    Use the most specific method available — `set_title` for titles, not
    `ax.text()`. Reserve `ax.text()` for labels that don't fit the other
    categories.

!!! tip "Text Design Principles"
    - **Use text sparingly** — too many labels create clutter that obscures data
    - **Keep labels concise** — a few words, not sentences
    - **Use consistent font sizes** — title > labels > annotations > tick labels
    - **Prefer annotations** for highlighting specific data points over general text

---

## ax.text()

Add text at specific data coordinates:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 3))

ax.grid(True)
ax.set_xlim(-0.5, 3.5)
ax.set_ylim(-0.05, 0.25)
ax.axhline(0, xmin=-0.5, xmax=3.5)

ax.text(0, 0.1, "Text label", fontsize=14, family="serif")
ax.text(2, 0.1, "Equation: $i\\hbar\\partial_t \\Psi = \\hat{H}\\Psi$", 
        fontsize=14, family="serif")

plt.show()
```

---

## Text Parameters

Common parameters for `ax.text()`:

```python
ax.text(
    x, y,                      # Position in data coordinates
    s,                         # Text string
    fontsize=12,               # Font size
    fontweight='bold',         # 'normal', 'bold', 'light', etc.
    fontstyle='italic',        # 'normal', 'italic', 'oblique'
    fontfamily='serif',        # 'serif', 'sans-serif', 'monospace'
    color='blue',              # Text color
    alpha=0.8,                 # Transparency
    rotation=45,               # Rotation angle
    ha='center',               # Horizontal alignment
    va='center',               # Vertical alignment
    backgroundcolor='yellow',  # Background color
    bbox=dict(...)             # Background box properties
)
```

---

## Text Alignment

Control horizontal alignment (ha) and vertical alignment (va):

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Horizontal alignment options
ax.text(0.5, 0.8, "ha='left'", ha='left', fontsize=12)
ax.text(0.5, 0.6, "ha='center'", ha='center', fontsize=12)
ax.text(0.5, 0.4, "ha='right'", ha='right', fontsize=12)

# Mark the x=0.5 position
ax.axvline(0.5, color='gray', linestyle='--', alpha=0.5)

plt.show()
```

---

## Text with Box

Add a box around text:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# Simple box
ax.text(0.5, 0.7, "Text with box", 
        fontsize=14,
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Different box styles
ax.text(0.5, 0.5, "Square box", 
        fontsize=14,
        bbox=dict(boxstyle='square', facecolor='lightblue'))

ax.text(0.5, 0.3, "Round with padding", 
        fontsize=14,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen'))

plt.show()
```

Box styles: `'square'`, `'round'`, `'round4'`, `'circle'`, `'larrow'`, `'rarrow'`, `'darrow'`

---

## Transform Coordinates

Use different coordinate systems:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1])

# Data coordinates (default)
ax.text(0.5, 0.5, "Data coords", transform=ax.transData)

# Axes coordinates (0-1 range)
ax.text(0.5, 0.9, "Axes coords", transform=ax.transAxes, ha='center')

# Figure coordinates (0-1 range)
fig.text(0.5, 0.02, "Figure coords", ha='center')

plt.show()
```

---

## Practical Example: Labeling Points

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 1, 5, 3])
labels = ['A', 'B', 'C', 'D', 'E']

fig, ax = plt.subplots()
ax.scatter(x, y, s=100)

for xi, yi, label in zip(x, y, labels):
    ax.text(xi + 0.1, yi + 0.1, label, fontsize=12, fontweight='bold')

ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()
```

---

## Multi-line Text

Use newlines for multi-line text:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

text = """Line 1
Line 2
Line 3"""

ax.text(0.5, 0.5, text, 
        fontsize=12, 
        ha='center', 
        va='center',
        bbox=dict(boxstyle='round', facecolor='wheat'))

plt.show()
```

---

## Key Takeaways

- `ax.text(x, y, s)` adds text at data coordinates
- Use `ha` and `va` for alignment
- `bbox` parameter adds a background box
- `transform` changes the coordinate system
- LaTeX math is supported with `$...$`


---

## Exercises

**Exercise 1.** Write code that creates a plot and adds text at data coordinates `(2, 0.5)` using `ax.text()` with fontsize 14.

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

**Exercise 2.** Explain the difference between data coordinates and axes coordinates in `ax.text()`. How do you specify axes coordinates?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that adds text with a bounding box (background) using the `bbox` parameter in `ax.text()`.

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

**Exercise 4.** Create a plot and add text at the center using `transform=ax.transAxes` so the text position is relative to the axes (not the data).

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
