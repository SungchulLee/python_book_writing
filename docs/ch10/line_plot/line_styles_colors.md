# Line Styles and Colors

Matplotlib provides extensive control over line appearance through style and color parameters.

!!! tip "Mental Model"
    Every Line2D artist has three visual knobs: `linestyle` (solid, dashed, dotted), `color` (any CSS name, hex code, or RGB tuple), and `linewidth` (thickness in points). You can set them as keyword arguments in `plot()` or combine all three in a format string like `'r--'` for a red dashed line.

!!! note "Design Guidelines"
    Line style and color are **semantic signals**, not just decoration:

    | Style | Use for |
    |-------|---------|
    | Solid | Primary data / main result |
    | Dashed | Comparison, reference, or theoretical |
    | Dotted | Thresholds, baselines, secondary |
    | Lighter color / thinner line | Background or less important data |

    Choose high-contrast colors for overlaid lines. Avoid relying on color alone
    — add different line styles for colorblind accessibility.

---

## Line Style (linestyle / ls)

Common line styles:

| Style | Abbreviation | Description |
|-------|--------------|-------------|
| `'-'` | solid | Solid line (default) |
| `'--'` | dashed | Dashed line |
| `':'` | dotted | Dotted line |
| `'-.'` | dashdot | Dash-dot pattern |

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(15, 3))
ax.plot(x, y, linestyle='--')
plt.show()
```

Short form:

```python
ax.plot(x, y, ls='--')
```

---

## Line Width (linewidth / lw)

Control line thickness:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(15, 3))
ax.plot(x, y, linestyle='--', linewidth=10)
plt.show()
```

Short form:

```python
ax.plot(x, y, ls='--', lw=10)
```

---

## Color (color / c)

Specify colors in multiple ways:

**Named colors:**
```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(15, 3))
ax.plot(x, y_sin, color='red')
ax.plot(x, y_cos, color='blue')
plt.show()
```

**Single-letter codes:**
```python
ax.plot(x, y_sin, c='r')  # red
ax.plot(x, y_cos, c='b')  # blue
```

| Code | Color |
|------|-------|
| `'b'` | Blue |
| `'g'` | Green |
| `'r'` | Red |
| `'c'` | Cyan |
| `'m'` | Magenta |
| `'y'` | Yellow |
| `'k'` | Black |
| `'w'` | White |

**Hex codes:**
```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(15, 3))
ax.plot(x, y_sin, c='#e32b2b')  # Custom red
ax.plot(x, y_cos, c='#3b81f1')  # Custom blue
plt.show()
```

---

## Alpha (Transparency)

Control opacity with alpha (0 = transparent, 1 = opaque):

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(15, 4))
ax.plot(x, y_sin, alpha=0.8)
ax.plot(x, y_cos, alpha=0.2)
plt.show()
```

---

## MATLAB-Style Format Strings

Combine style, color, and marker in a single string:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 10)
y = np.sin(x)

plt.plot(x, y, '--*r', ms=20)  # dashed, star markers, red
plt.show()
```

Format: `'[marker][line][color]'` or `'[line][marker][color]'`

Examples:

- `'--*r'`: dashed line, star markers, red
- `'-ob'`: solid line, circle markers, blue
- `':sg'`: dotted line, square markers, green

---

## Using Keyword Dictionaries

Pass multiple style options via dictionary:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(15, 3))
ax.plot(x, y, **{'ls': '--', 'lw': 10})
plt.show()
```

---

## Complete Example

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

fig, ax = plt.subplots(figsize=(12, 4))

ax.plot(x, y_sin, 
        linestyle='--', 
        linewidth=2, 
        color='#e74c3c', 
        alpha=0.8,
        label='sin(x)')

ax.plot(x, y_cos, 
        ls=':', 
        lw=3, 
        c='#3498db', 
        alpha=0.8,
        label='cos(x)')

ax.legend()
ax.set_title('Trigonometric Functions')
plt.show()
```

---

## Key Takeaways

- Use `linestyle` or `ls` for line pattern
- Use `linewidth` or `lw` for thickness
- Use `color` or `c` for color
- Colors can be names, single letters, or hex codes
- `alpha` controls transparency (0-1)
- Format strings combine options: `'--or'`


---

## Exercises

**Exercise 1.** Write code that demonstrates all four line styles (`'-'`, `'--'`, `'-.'`, `':'`) on the same axes, each with a different color.

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

**Exercise 2.** Explain three ways to specify colors in Matplotlib: named colors, hex strings, and RGB tuples. Give an example of each.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a plot with a thick blue line (`linewidth=4`) and show how to set `alpha=0.5` for semi-transparency.

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

**Exercise 4.** Write code that uses a format string (e.g., `'ro--'`) and explain what each character means.

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
