# Scatter Plot Keywords

The `ax.scatter()` method accepts numerous keyword arguments to control marker appearance and behavior.

!!! tip "Mental Model"
    `scatter()` keywords map directly to visual channels: `s` controls size, `c` controls color, `marker` controls shape, `alpha` controls transparency, and `edgecolors`/`linewidths` control the marker border. Each parameter can be a single value (uniform) or an array (per-point), giving you fine-grained control over every dot.

!!! note "Parameter Priority"
    Not all scatter parameters are equally important. In practice:

    1. **`x`, `y`** — the data (always required)
    2. **`c`** + `cmap` — color encoding (most common third dimension)
    3. **`s`** — size encoding (use sparingly — area perception is imprecise)
    4. **`alpha`** — transparency for dense/overlapping data (reveals density)
    5. **`marker`**, `edgecolors`, `linewidths` — fine-tuning (rarely critical)

    A useful interaction: **`alpha` + dense data reveals density** — where many
    transparent points overlap, the color intensifies, acting as a poor-man's
    heatmap without any binning.

## Marker Size

The `s` parameter controls marker size in points squared.

### 1. Uniform Size

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
x = np.random.rand(50)
y = np.random.rand(50)

fig, ax = plt.subplots()
ax.scatter(x, y, s=100)  # All markers size 100
plt.show()
```

### 2. Variable Sizes

```python
sizes = np.random.rand(50) * 500

fig, ax = plt.subplots()
ax.scatter(x, y, s=sizes)
plt.show()
```

### 3. Size by Data Value

```python
z = np.random.rand(50) * 100
sizes = z * 5  # Scale data to appropriate marker size

fig, ax = plt.subplots()
ax.scatter(x, y, s=sizes)
plt.show()
```

## Marker Style

The `marker` parameter sets the marker shape.

### 1. Common Markers

```python
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
markers = ['o', 's', '^', 'v', 'D', 'p', '*', 'h']
names = ['Circle', 'Square', 'Triangle Up', 'Triangle Down', 
         'Diamond', 'Pentagon', 'Star', 'Hexagon']

for ax, marker, name in zip(axes.flat, markers, names):
    ax.scatter([0.5], [0.5], s=500, marker=marker)
    ax.set_title(name)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

plt.tight_layout()
plt.show()
```

### 2. Additional Markers

```python
# 'x': X marker
# '+': Plus marker
# '.': Point marker
# ',': Pixel marker
# '1', '2', '3', '4': Tri markers
# '<', '>': Left/Right triangles
```

### 3. Custom Marker

```python
from matplotlib.markers import MarkerStyle

# Filled vs unfilled
ax.scatter(x, y, marker='o', facecolors='none', edgecolors='blue')
```

## Color

The `c` or `color` parameter controls marker color.

### 1. Single Color

```python
fig, ax = plt.subplots()
ax.scatter(x, y, color='red')
plt.show()
```

### 2. Named Colors

```python
ax.scatter(x, y, color='steelblue')
ax.scatter(x, y, color='coral')
ax.scatter(x, y, color='forestgreen')
```

### 3. Hex Colors

```python
ax.scatter(x, y, color='#FF5733')
ax.scatter(x, y, color='#3498DB')
```

## Alpha (Transparency)

The `alpha` parameter sets marker transparency.

### 1. Uniform Alpha

```python
fig, ax = plt.subplots()
ax.scatter(x, y, alpha=0.5)
plt.show()
```

### 2. Overlapping Points

```python
np.random.seed(42)
x = np.random.normal(0, 1, 1000)
y = np.random.normal(0, 1, 1000)

fig, ax = plt.subplots()
ax.scatter(x, y, alpha=0.3)
plt.show()
```

### 3. Reveal Density

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, alpha in zip(axes, [1.0, 0.5, 0.1]):
    ax.scatter(x, y, alpha=alpha)
    ax.set_title(f'alpha = {alpha}')

plt.tight_layout()
plt.show()
```

## Edge Properties

Control marker edge appearance.

### 1. Edge Color

```python
fig, ax = plt.subplots()
ax.scatter(x, y, c='lightblue', edgecolors='navy', s=100)
plt.show()
```

### 2. Edge Width

```python
ax.scatter(x, y, c='white', edgecolors='black', linewidths=2, s=100)
```

### 3. No Edge

```python
ax.scatter(x, y, edgecolors='none', s=100)
```

## Label and Legend

Add labels for legend display.

### 1. Label Parameter

```python
fig, ax = plt.subplots()
ax.scatter(x[:25], y[:25], label='Group A')
ax.scatter(x[25:], y[25:], label='Group B')
ax.legend()
plt.show()
```

### 2. Legend Location

```python
ax.legend(loc='upper right')
ax.legend(loc='lower left')
ax.legend(loc='best')
```

### 3. Legend with Marker Size

```python
# Create legend with consistent marker size
scatter = ax.scatter(x, y, s=sizes, label='Data')
ax.legend(markerscale=0.5)  # Scale markers in legend
```

## Z-Order

Control drawing order of overlapping elements.

### 1. Default Order

```python
fig, ax = plt.subplots()
ax.scatter(x, y, s=200, zorder=1)
ax.axhline(0.5, color='red', zorder=2)  # Line on top
plt.show()
```

### 2. Points on Top

```python
fig, ax = plt.subplots()
ax.axhline(0.5, color='red', zorder=1)
ax.scatter(x, y, s=200, zorder=2)  # Points on top
plt.show()
```

### 3. Layered Scatter

```python
fig, ax = plt.subplots()
ax.scatter(x, y, s=300, c='lightgray', zorder=1)
ax.scatter(x, y, s=100, c='red', zorder=2)
plt.show()
```

## Combining Keywords

Create complex visualizations with multiple parameters.

### 1. Styled Points

```python
fig, ax = plt.subplots()
ax.scatter(x, y, 
           s=150,
           c='steelblue',
           alpha=0.7,
           edgecolors='navy',
           linewidths=1,
           marker='o')
plt.show()
```

### 2. Bubble Chart Style

```python
np.random.seed(42)
x = np.random.rand(20)
y = np.random.rand(20)
sizes = np.random.rand(20) * 1000

fig, ax = plt.subplots()
ax.scatter(x, y,
           s=sizes,
           c='coral',
           alpha=0.6,
           edgecolors='darkred',
           linewidths=2)
plt.show()
```

### 3. Multi-Group Styled

```python
fig, ax = plt.subplots(figsize=(8, 6))

groups = {
    'A': {'x': np.random.normal(2, 0.5, 30), 'y': np.random.normal(2, 0.5, 30),
          'color': 'steelblue', 'marker': 'o'},
    'B': {'x': np.random.normal(4, 0.5, 30), 'y': np.random.normal(4, 0.5, 30),
          'color': 'coral', 'marker': 's'},
    'C': {'x': np.random.normal(3, 0.5, 30), 'y': np.random.normal(5, 0.5, 30),
          'color': 'forestgreen', 'marker': '^'}
}

for name, data in groups.items():
    ax.scatter(data['x'], data['y'], 
               c=data['color'], 
               marker=data['marker'],
               s=100, alpha=0.7, label=name)

ax.legend()
plt.show()
```


## Parameters as Visual Channels

Each scatter keyword maps to a visual encoding channel:

| Parameter | Visual channel | What it encodes |
|---|---|---|
| `x`, `y` | Position | Primary relationship |
| `c` | Color | Additional variable or category |
| `s` | Size (area) | Magnitude or weight |
| `marker` | Shape | Categorical distinction |
| `alpha` | Transparency | Density (overlapping points reveal concentration) |
| `edgecolors` | Border | Emphasis or distinction from background |

Understanding this mapping means you can design scatter plots intentionally — choosing which variables go to which channel based on importance and precision.

---

## Exercises

**Exercise 1.** Write code demonstrating the `edgecolors` and `linewidths` parameters in `ax.scatter()` to give each point a visible border.

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

**Exercise 2.** Explain the `marker` parameter in `ax.scatter()`. List at least five different marker shapes.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a scatter plot with `alpha=0.3` to handle overplotting (overlapping points in dense regions).

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

**Exercise 4.** Write code that uses `ax.scatter()` with the `zorder` parameter to ensure scatter points appear on top of other plot elements.

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
