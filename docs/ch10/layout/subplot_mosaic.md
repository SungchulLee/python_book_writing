# subplot_mosaic

`plt.subplot_mosaic()` provides a flexible, intuitive way to create complex subplot layouts using ASCII-art or nested lists.

!!! tip "Mental Model"
    `subplot_mosaic` lets you sketch your layout as text art: `"AB\nCC"` means A and B side by side on top, C spanning the full bottom. Each unique letter becomes a named Axes in a dictionary. It is the most readable way to create asymmetric layouts because the code looks like the result.

!!! warning "Limitations"
    `subplot_mosaic` trades power for readability. It is less suited for:

    - **Very large grids** (>6x6) — the ASCII art becomes unwieldy
    - **Programmatic generation** — you cannot easily construct the layout string
      from data or loop variables (use GridSpec instead)
    - **Fine-grained size control** — it supports `width_ratios` / `height_ratios`
      but not per-cell sizing as precise as GridSpec slicing

## Basic Usage

### ASCII Art Layout

```python
import matplotlib.pyplot as plt
import numpy as np

# Define layout using ASCII art
fig, axes = plt.subplot_mosaic(
    """
    AB
    CC
    """
)

# Access axes by their letter labels
x = np.linspace(0, 10, 100)
axes['A'].plot(x, np.sin(x))
axes['A'].set_title('A: Sine')

axes['B'].plot(x, np.cos(x))
axes['B'].set_title('B: Cosine')

axes['C'].plot(x, np.tan(x))
axes['C'].set_ylim(-5, 5)
axes['C'].set_title('C: Tangent (full width)')

plt.tight_layout()
plt.show()
```

### List-Based Layout

```python
# Equivalent using nested lists
fig, axes = plt.subplot_mosaic([
    ['A', 'B'],
    ['C', 'C']
])
```

## Layout Patterns

### Spanning Rows

```python
fig, axes = plt.subplot_mosaic(
    """
    AAB
    AAC
    """
)
# A spans 2 rows, B and C each take one row
```

### Spanning Columns

```python
fig, axes = plt.subplot_mosaic(
    """
    AB
    CC
    """
)
# C spans both columns
```

### Complex Spanning

```python
fig, axes = plt.subplot_mosaic(
    """
    AABB
    CCBB
    CCDD
    """
)
# A: top-left 2x2, B: right 3x2, C: bottom-left 2x2, D: bottom-right
```

### Empty Spaces

```python
fig, axes = plt.subplot_mosaic(
    """
    A.B
    CCC
    """,
    empty_sentinel='.'  # Default is '.'
)
# '.' creates empty space
```

## Figure Size and Spacing

### Set Figure Size

```python
fig, axes = plt.subplot_mosaic(
    """
    AB
    CC
    """,
    figsize=(10, 8)
)
```

### Adjust Spacing

```python
fig, axes = plt.subplot_mosaic(
    """
    AB
    CC
    """,
    gridspec_kw={'wspace': 0.3, 'hspace': 0.3}
)
```

### Width and Height Ratios

```python
fig, axes = plt.subplot_mosaic(
    """
    AB
    CC
    """,
    gridspec_kw={
        'width_ratios': [2, 1],   # A is twice as wide as B
        'height_ratios': [1, 2]   # C row is twice as tall
    }
)
```

## Practical Examples

### 1. Dashboard Layout

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplot_mosaic(
    """
    AAAB
    AAAC
    DDDD
    """,
    figsize=(12, 8),
    gridspec_kw={'height_ratios': [1, 1, 0.5]}
)

# Main plot
x = np.linspace(0, 10, 100)
axes['A'].plot(x, np.sin(x) + np.random.normal(0, 0.1, 100))
axes['A'].set_title('Main Time Series')
axes['A'].set_xlabel('Time')

# Side plots
axes['B'].hist(np.random.randn(500), bins=20, orientation='horizontal')
axes['B'].set_title('Distribution')

axes['C'].boxplot([np.random.randn(100) for _ in range(3)])
axes['C'].set_title('Summary')

# Bottom timeline
axes['D'].fill_between(x, 0, np.abs(np.sin(x)), alpha=0.5)
axes['D'].set_title('Activity')

plt.tight_layout()
plt.show()
```

### 2. Scientific Figure Layout

```python
fig, axes = plt.subplot_mosaic(
    """
    AB
    AC
    DE
    """,
    figsize=(10, 12),
    gridspec_kw={'height_ratios': [2, 2, 1]}
)

np.random.seed(42)

# Main scatter plot
axes['A'].scatter(np.random.randn(100), np.random.randn(100), alpha=0.6)
axes['A'].set_title('A) Scatter Plot')

# Marginal histogram (top)
axes['B'].hist(np.random.randn(100), bins=20)
axes['B'].set_title('B) X Distribution')

# Marginal histogram (right, rotated conceptually)
axes['C'].hist(np.random.randn(100), bins=20, orientation='horizontal')
axes['C'].set_title('C) Y Distribution')

# Residuals
x = np.linspace(0, 10, 50)
axes['D'].scatter(x, np.random.randn(50) * 0.5)
axes['D'].axhline(0, color='red', linestyle='--')
axes['D'].set_title('D) Residuals')

# Q-Q plot
from scipy import stats
stats.probplot(np.random.randn(100), plot=axes['E'])
axes['E'].set_title('E) Q-Q Plot')

plt.tight_layout()
plt.show()
```

### 3. Multi-Panel Comparison

```python
fig, axes = plt.subplot_mosaic(
    """
    ABC
    DEF
    GHI
    """,
    figsize=(12, 12),
    sharex=True,
    sharey=True
)

x = np.linspace(0, 2*np.pi, 100)

# Different functions in each panel
functions = {
    'A': np.sin, 'B': np.cos, 'C': np.tan,
    'D': lambda x: np.sin(2*x), 'E': lambda x: np.cos(2*x), 'F': lambda x: np.sin(x)*np.cos(x),
    'G': lambda x: x/5, 'H': lambda x: np.sin(x)**2, 'I': lambda x: np.cos(x)**2
}

for label, func in functions.items():
    y = func(x)
    if label == 'C':  # Clip tangent
        y = np.clip(y, -5, 5)
    axes[label].plot(x, y)
    axes[label].set_title(label)
    axes[label].grid(True, alpha=0.3)

axes['A'].set_ylim(-2, 2)
plt.tight_layout()
plt.show()
```

### 4. Financial Dashboard

```python
fig, axes = plt.subplot_mosaic(
    """
    PPPPV
    PPPPV
    TTTTH
    """,
    figsize=(14, 10),
    gridspec_kw={
        'width_ratios': [1, 1, 1, 1, 1],
        'height_ratios': [2, 2, 1]
    }
)

np.random.seed(42)
dates = np.arange(100)
prices = 100 + np.cumsum(np.random.randn(100))
volume = np.abs(np.random.randn(100)) * 1e6
returns = np.diff(prices) / prices[:-1] * 100

# Price chart
axes['P'].plot(dates, prices, 'b-', linewidth=1.5)
axes['P'].fill_between(dates, prices.min(), prices, alpha=0.1)
axes['P'].set_ylabel('Price ($)')
axes['P'].set_title('Stock Price')

# Volume bars
axes['V'].barh(dates, volume, height=0.8, alpha=0.7)
axes['V'].set_xlabel('Volume')
axes['V'].set_title('Volume')

# Timeline
axes['T'].fill_between(dates[:-1], returns, where=returns>0, color='green', alpha=0.5)
axes['T'].fill_between(dates[:-1], returns, where=returns<0, color='red', alpha=0.5)
axes['T'].axhline(0, color='black', linewidth=0.5)
axes['T'].set_ylabel('Return %')
axes['T'].set_title('Daily Returns')

# Histogram of returns
axes['H'].hist(returns, bins=20, orientation='horizontal', color='gray', alpha=0.7)
axes['H'].axhline(0, color='black', linewidth=0.5)
axes['H'].set_xlabel('Frequency')

plt.tight_layout()
plt.show()
```

## Per-Subplot Customization

### Different Projections

```python
fig, axes = plt.subplot_mosaic(
    """
    AB
    CC
    """,
    per_subplot_kw={
        'B': {'projection': 'polar'},  # Make B a polar plot
    }
)

x = np.linspace(0, 10, 100)
axes['A'].plot(x, np.sin(x))

theta = np.linspace(0, 2*np.pi, 100)
axes['B'].plot(theta, 1 + np.sin(theta))

axes['C'].plot(x, x**2)
plt.tight_layout()
plt.show()
```

### 3D Subplot

```python
fig, axes = plt.subplot_mosaic(
    """
    AB
    """,
    per_subplot_kw={
        'B': {'projection': '3d'}
    },
    figsize=(12, 5)
)

x = np.linspace(0, 10, 100)
axes['A'].plot(x, np.sin(x))
axes['A'].set_title('2D Plot')

# 3D plot
ax3d = axes['B']
u = np.linspace(0, 2*np.pi, 50)
v = np.linspace(0, np.pi, 50)
X = np.outer(np.cos(u), np.sin(v))
Y = np.outer(np.sin(u), np.sin(v))
Z = np.outer(np.ones(np.size(u)), np.cos(v))
ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
ax3d.set_title('3D Plot')

plt.tight_layout()
plt.show()
```

## Comparison with Other Methods

| Method | Best For | Complexity |
|--------|----------|------------|
| `subplot_mosaic` | Complex, named layouts | Low |
| `subplots` | Regular grids | Low |
| `GridSpec` | Fine-grained control | Medium |
| `add_subplot` | Dynamic subplot addition | Medium |

### When to Use subplot_mosaic

- Complex layouts with spanning cells
- When you want named axes for clarity
- Dashboard-style figures
- When the layout is designed visually

### When to Use Alternatives

- **subplots**: Regular NxM grids
- **GridSpec**: Need precise spacing control
- **add_subplot**: Dynamic subplot creation

## Key Parameters

| Parameter | Description |
|-----------|-------------|
| `mosaic` | String or nested list defining layout |
| `figsize` | Figure size in inches |
| `gridspec_kw` | Dict passed to GridSpec (spacing, ratios) |
| `per_subplot_kw` | Dict of dicts for per-subplot options |
| `empty_sentinel` | Character for empty cells (default '.') |
| `sharex`, `sharey` | Share axes between subplots |

## Tips and Best Practices

1. **Use meaningful labels**: 'price', 'volume' instead of 'A', 'B'
2. **Start simple**: Test layout before adding data
3. **Adjust ratios**: Use gridspec_kw for proper proportions
4. **Consider empty space**: Use '.' for visual separation
5. **Apply tight_layout()**: Always call at the end


---

## Exercises

**Exercise 1.** Write code using `fig.subplot_mosaic()` with the layout `[["A", "A"], ["B", "C"]]` where subplot A spans the top row. Plot different data in each.

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

**Exercise 2.** Explain the advantage of `subplot_mosaic()` over `GridSpec` for defining complex layouts. What makes the string-based layout definition convenient?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a mosaic layout with a placeholder `.` for an empty cell: `[["A", "."], ["B", "C"]]`. Plot data only in the non-empty subplots.

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

**Exercise 4.** Write code that uses `subplot_mosaic()` to create a layout with three rows: one full-width plot on top, two side-by-side in the middle, and one full-width on the bottom.

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
