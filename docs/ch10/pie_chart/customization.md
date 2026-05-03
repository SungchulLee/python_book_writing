# Pie Chart Customization

This document consolidates the key customization parameters for pie charts: `startangle`, `shadow`, `counterclock`, `explode`, `radius`, and `autopct`.

!!! tip "Mental Model"
    Pie chart customization controls two things: geometry (where slices start, which direction they go, how far they explode outward) and labeling (percentage format via `autopct`, label distance via `labeldistance`). The `startangle=90` convention puts the first slice at 12 o'clock, which is the most natural orientation for Western readers.

!!! note "Design Principles: Clarity Over Decoration"
    ```text
    Visualization priority order:
    1. Accuracy — correct data mapping
    2. Clarity — easy to read
    3. Efficiency — fast to interpret
    4. Aesthetics — last priority
    ```

    Guidelines for professional pie charts:

    - **Explode sparingly** — offset 1–2 key slices at most. Exploding everything defeats the purpose.
    - **Avoid shadow** in publication-quality figures — shadows distort perceived slice sizes.
    - **Prefer clean color palettes** — high-contrast, colorblind-friendly, no gradients.
    - **Use labels or legend, not both** — redundant labeling clutters.

## Parameter Overview

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `startangle` | float | 0 | Rotation angle in degrees (counterclockwise from 3 o'clock) |
| `shadow` | bool | False | Draw shadow beneath pie |
| `counterclock` | bool | True | Wedge direction (True=CCW, False=CW) |
| `explode` | array-like | None | Offset distance for each wedge |
| `radius` | float | 1 | Pie chart radius |
| `autopct` | str or callable | None | Format string for percentage labels |

## Setup

```python
import matplotlib.pyplot as plt
import numpy as np

vals = [1400, 600, 300, 410, 250]
labels = ["Home Rent", "Food", "Phone/Internet", "Car", "Utilities"]
colors = ['#e74c3c', '#3498db', '#9b59b6', '#f39c12', '#2ecc71']
```

---

## startangle

Controls the starting position of the first wedge. The angle is measured counterclockwise from the positive x-axis (3 o'clock position).

### Basic Usage

```python
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

angles = [0, 45, 90, 180]

for ax, angle in zip(axes, angles):
    ax.pie(vals, labels=labels, startangle=angle)
    ax.set_title(f'startangle={angle}°')

plt.tight_layout()
plt.show()
```

### Common Patterns

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Default: starts at 3 o'clock
axes[0].pie(vals, labels=labels, startangle=0)
axes[0].set_title('startangle=0° (3 o\'clock)')

# Top start: common for presentations
axes[1].pie(vals, labels=labels, startangle=90)
axes[1].set_title('startangle=90° (12 o\'clock)')

# Custom positioning
axes[2].pie(vals, labels=labels, startangle=140)
axes[2].set_title('startangle=140°')

plt.tight_layout()
plt.show()
```

---

## shadow

Adds a shadow effect beneath the pie chart for visual depth.

### Basic Usage

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].pie(vals, labels=labels, shadow=False)
axes[0].set_title('shadow=False')

axes[1].pie(vals, labels=labels, shadow=True)
axes[1].set_title('shadow=True')

plt.tight_layout()
plt.show()
```

### Shadow with Other Parameters

```python
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(
    vals,
    labels=labels,
    colors=colors,
    shadow=True,
    startangle=90,
    autopct='%1.1f%%'
)
ax.set_title('Shadow with Styling')
plt.show()
```

---

## counterclock

Controls the direction in which wedges are drawn.

### Basic Usage

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].pie(vals, labels=labels, counterclock=True, startangle=90)
axes[0].set_title('counterclock=True (default)')

axes[1].pie(vals, labels=labels, counterclock=False, startangle=90)
axes[1].set_title('counterclock=False')

plt.tight_layout()
plt.show()
```

### Direction Comparison

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

configs = [
    {'startangle': 90, 'counterclock': True},
    {'startangle': 90, 'counterclock': False},
    {'startangle': 0, 'counterclock': True},
    {'startangle': 0, 'counterclock': False},
]

for ax, config in zip(axes.flat, configs):
    ax.pie(vals, labels=labels, **config)
    ax.set_title(f"startangle={config['startangle']}°, counterclock={config['counterclock']}")

plt.tight_layout()
plt.show()
```

---

## explode

Offsets wedges from the center to emphasize specific slices.

### Explode Syntax

```python
# Array of offset distances, one per wedge
# 0 = no offset, 0.1 = slight offset, 0.3 = large offset
explode = [0.1, 0, 0, 0, 0]  # Explode first slice only
```

### Basic Usage

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Single slice
axes[0].pie(vals, labels=labels, explode=[0.1, 0, 0, 0, 0])
axes[0].set_title('Explode First Slice')

# Multiple slices
axes[1].pie(vals, labels=labels, explode=[0.1, 0, 0.15, 0, 0.1])
axes[1].set_title('Explode Multiple')

# All slices
axes[2].pie(vals, labels=labels, explode=[0.05, 0.05, 0.05, 0.05, 0.05])
axes[2].set_title('Explode All')

plt.tight_layout()
plt.show()
```

### Dynamic Explode

```python
# Explode the largest slice
max_idx = vals.index(max(vals))
explode = [0.1 if i == max_idx else 0 for i in range(len(vals))]

fig, ax = plt.subplots()
ax.pie(vals, labels=labels, explode=explode, autopct='%1.1f%%')
ax.set_title('Highlight Maximum Value')
plt.show()
```

### Explode Values Comparison

```python
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

offsets = [0.05, 0.1, 0.2, 0.3]

for ax, offset in zip(axes, offsets):
    ax.pie(vals, labels=labels, explode=[offset, 0, 0, 0, 0])
    ax.set_title(f'explode={offset}')

plt.tight_layout()
plt.show()
```

---

## radius

Controls the size of the pie chart.

### Basic Usage

```python
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

radii = [0.5, 0.8, 1.0, 1.3]

for ax, r in zip(axes, radii):
    ax.pie(vals, labels=labels, radius=r)
    ax.set_title(f'radius={r}')

plt.tight_layout()
plt.show()
```

### Donut Charts

Use `radius` with `wedgeprops` to create donut charts.

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Basic donut
axes[0].pie(vals, radius=1.2, wedgeprops=dict(width=0.4))
axes[0].set_title('Basic Donut')

# Thin donut
axes[1].pie(vals, radius=1.2, wedgeprops=dict(width=0.2))
axes[1].set_title('Thin Donut')

# Thick donut
axes[2].pie(vals, radius=1.2, wedgeprops=dict(width=0.6))
axes[2].set_title('Thick Donut')

plt.tight_layout()
plt.show()
```

### Nested Donut Chart

```python
outer_vals = [1400, 600, 300, 410, 250]
inner_vals = [800, 600, 500, 400, 660]

fig, ax = plt.subplots(figsize=(9, 9))

ax.pie(outer_vals, radius=1.3, wedgeprops=dict(width=0.3),
       autopct='%1.0f%%', pctdistance=0.85)
ax.pie(inner_vals, radius=1.0, wedgeprops=dict(width=0.3),
       autopct='%1.0f%%', pctdistance=0.75)

ax.set_title('Nested Donut Chart')
plt.show()
```

---

## autopct

Automatically calculates and displays percentage values on each wedge.

### Format String Syntax

```
autopct = '%[width].[precision]f%%'
```

| Component | Description | Example |
|-----------|-------------|---------|
| `%` | Format initiator | Required |
| `width` | Minimum total characters | `4` |
| `.precision` | Decimal places | `.1` |
| `f` | Float type | Required |
| `%%` | Literal % symbol | `%%` |

### Basic Usage

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

formats = ['%.0f%%', '%.1f%%', '%.2f%%']
titles = ['No Decimal', 'One Decimal', 'Two Decimals']

for ax, fmt, title in zip(axes, formats, titles):
    ax.pie(vals, labels=labels, autopct=fmt)
    ax.set_title(f"{title}: autopct='{fmt}'")

plt.tight_layout()
plt.show()
```

### Custom Format Strings

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Parentheses
axes[0].pie(vals, labels=labels, autopct='(%.1f%%)')
axes[0].set_title('Parentheses')

# Brackets
axes[1].pie(vals, labels=labels, autopct='[%.0f%%]')
axes[1].set_title('Brackets')

# Custom text
axes[2].pie(vals, labels=labels, autopct='%.1f pct')
axes[2].set_title('Custom Text')

plt.tight_layout()
plt.show()
```

### Callable Function

Use a function for complete control over formatting.

```python
def make_autopct(values):
    def autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n(${val:,})'
    return autopct

fig, ax = plt.subplots(figsize=(10, 8))
ax.pie(vals, labels=labels, autopct=make_autopct(vals))
ax.set_title('Percentage with Absolute Values')
plt.show()
```

### Conditional Display

```python
def threshold_autopct(pct, threshold=10):
    return f'{pct:.1f}%' if pct >= threshold else ''

fig, ax = plt.subplots()
ax.pie(vals, labels=labels, autopct=lambda p: threshold_autopct(p, 15))
ax.set_title('Show Only Values ≥ 15%')
plt.show()
```

---

## Styling Percentage Labels

Access returned text objects for custom styling.

```python
fig, ax = plt.subplots(figsize=(10, 8))
wedges, texts, autotexts = ax.pie(
    vals,
    labels=labels,
    colors=colors,
    autopct='%1.1f%%'
)

for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_color('white')
    autotext.set_fontsize(11)

plt.show()
```

---

## Combined Customization

### Full Example

```python
fig, ax = plt.subplots(figsize=(10, 8))

wedges, texts, autotexts = ax.pie(
    vals,
    labels=labels,
    colors=colors,
    startangle=90,
    counterclock=False,
    shadow=True,
    explode=[0.05, 0, 0, 0.1, 0.15],
    radius=1.2,
    autopct='%1.1f%%',
    pctdistance=0.6,
    labeldistance=1.15
)

for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_color('white')

ax.set_title('Monthly Budget Distribution', fontsize=14, fontweight='bold')
plt.show()
```

### Professional Dashboard

```python
fig = plt.figure(figsize=(14, 6))

# Main pie chart
ax1 = fig.add_subplot(121)
wedges, texts, autotexts = ax1.pie(
    vals,
    labels=labels,
    colors=colors,
    startangle=90,
    counterclock=False,
    shadow=True,
    explode=[0.03, 0, 0, 0, 0],
    autopct='%1.1f%%',
    pctdistance=0.6
)
for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_color('white')
ax1.set_title('Budget Breakdown', fontsize=13)

# Donut chart
ax2 = fig.add_subplot(122)
ax2.pie(
    vals,
    colors=colors,
    startangle=90,
    counterclock=False,
    radius=1.2,
    wedgeprops=dict(width=0.4),
    autopct='%1.0f%%',
    pctdistance=0.8
)
ax2.set_title('Donut Visualization', fontsize=13)

plt.suptitle('Monthly Expenses Analysis', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## Parameter Quick Reference

```python
ax.pie(
    data,                    # Values
    labels=labels,           # Wedge labels
    colors=colors,           # Wedge colors
    startangle=90,           # Start at 12 o'clock
    counterclock=False,      # Clockwise direction
    shadow=True,             # Add shadow
    explode=[0.1, 0, 0, 0],  # Offset slices
    radius=1.2,              # Chart size
    autopct='%1.1f%%',       # Percentage format
    pctdistance=0.6,         # % label position
    labeldistance=1.1,       # Label position
    wedgeprops=dict(         # Wedge styling
        width=0.4,           # For donut charts
        edgecolor='white'
    ),
    textprops=dict(          # Text styling
        fontsize=11,
        fontweight='bold'
    )
)
```


---

## Exercises

**Exercise 1.** Write code that creates a pie chart with custom colors using a list of hex codes and the `explode` parameter to offset the largest slice.

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

**Exercise 2.** Explain the `shadow` parameter in `ax.pie()`. Write code demonstrating a pie chart with and without shadow.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a pie chart with custom text properties: bold percentage labels and italic category labels.

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

**Exercise 4.** Write code that creates a nested pie chart (ring chart) by calling `ax.pie()` twice with different `radius` and `width` values.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt

        outer_sizes = [40, 30, 30]
        outer_labels = ['Product', 'Service', 'Other']
        outer_colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']

        inner_sizes = [20, 20, 15, 15, 10, 20]
        inner_colors = ['#ff8a8a', '#ff4d4d', '#6fd6c8', '#3dbfa7',
                        '#5cc4d4', '#3aabc0']

        fig, ax = plt.subplots()
        ax.pie(outer_sizes, labels=outer_labels, colors=outer_colors,
               radius=1.0, wedgeprops=dict(width=0.3), autopct='%1.0f%%',
               pctdistance=0.85)
        ax.pie(inner_sizes, colors=inner_colors,
               radius=0.7, wedgeprops=dict(width=0.3))
        ax.set_title('Nested Pie (Ring Chart)')
        plt.show()

---

**Exercise 5.** Create a pie chart with 5 slices of sizes 22%, 21%, 20%, 19%, 18%. Then create a bar chart of the same data side-by-side. Explain the perceptual problem: why are differences invisible in the pie but obvious in the bar chart?

??? success "Solution to Exercise 5"

        import matplotlib.pyplot as plt

        labels = ['A', 'B', 'C', 'D', 'E']
        sizes = [22, 21, 20, 19, 18]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.pie(sizes, labels=labels, autopct='%1.0f%%', startangle=90)
        ax1.set_title('Pie: Can you rank these?')

        ax2.bar(labels, sizes, color='steelblue')
        ax2.set_ylabel('Percentage')
        ax2.set_ylim(0, 30)
        ax2.set_title('Bar: Ranking is immediate')

        plt.tight_layout()
        plt.show()

        # The pie slices look nearly identical because angles that differ
        # by only 1-2 degrees are below human perceptual threshold.
        # The bar chart encodes the same data as length — a channel that
        # humans compare with much higher precision.
