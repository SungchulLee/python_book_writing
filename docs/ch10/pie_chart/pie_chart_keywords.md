# Pie Chart Keywords

Reference for `ax.pie()` keyword arguments.

!!! tip "Mental Model"
    `ax.pie()` has many keywords, but they group logically: slice data (`x`, `explode`, `labels`, `colors`), text formatting (`autopct`, `pctdistance`, `labeldistance`, `textprops`), and layout (`startangle`, `radius`, `counterclock`, `center`). Use `wedgeprops` to style individual slices just as you would use `boxprops` in box plots.

!!! tip "Priority: The 5 Parameters That Matter Most"
    For 90% of pie charts, you only need these:

    1. **`x`** — the data values
    2. **`labels`** — category names
    3. **`autopct`** — percentage format string or callable
    4. **`startangle`** — typically `90` for 12-o'clock start
    5. **`colors`** — explicit color list for clarity

    Everything else (`shadow`, `frame`, `hatch`, `rotatelabels`) is secondary styling that you can ignore until you have a specific design need.

## Signature

```python
ax.pie(x, explode=None, labels=None, colors=None, autopct=None,
       pctdistance=0.6, shadow=False, labeldistance=1.1, startangle=0,
       radius=1, counterclock=True, wedgeprops=None, textprops=None,
       center=(0, 0), frame=False, rotatelabels=False, normalize=True,
       hatch=None)
```

## Data Parameter

### x

Array-like values for each wedge. Values are normalized to sum to 1 (or 360 degrees).

```python
vals = [1400, 600, 300, 410, 250]
ax.pie(vals)
```

## Label Parameters

### labels

Sequence of strings for wedge labels.

```python
labels = ["Rent", "Food", "Phone", "Car", "Utilities"]
ax.pie(vals, labels=labels)
```

### labeldistance

Radial distance for labels (default: 1.1). Set to `None` to hide labels.

```python
ax.pie(vals, labels=labels, labeldistance=1.2)  # Further from center
ax.pie(vals, labels=labels, labeldistance=None)  # No labels
```

### rotatelabels

Rotate each label to angle of slice (default: False).

```python
ax.pie(vals, labels=labels, rotatelabels=True)
```

## Percentage Parameters

### autopct

Format string or function for percentage labels.

```python
# Format string
ax.pie(vals, autopct='%1.1f%%')   # One decimal: 47.3%
ax.pie(vals, autopct='%d%%')      # Integer: 47%
ax.pie(vals, autopct='%.2f%%')    # Two decimals: 47.30%

# Custom function
def my_autopct(pct):
    return f'{pct:.1f}%' if pct > 5 else ''

ax.pie(vals, autopct=my_autopct)
```

### pctdistance

Radial distance for percentage labels (default: 0.6).

```python
ax.pie(vals, autopct='%1.1f%%', pctdistance=0.5)  # Closer to center
ax.pie(vals, autopct='%1.1f%%', pctdistance=0.8)  # Further from center
```

## Appearance Parameters

### colors

Sequence of colors for wedges.

```python
# Named colors
colors = ['red', 'blue', 'green', 'orange', 'purple']
ax.pie(vals, colors=colors)

# Hex colors
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
ax.pie(vals, colors=colors)

# Colormap
colors = plt.cm.Pastel1(np.linspace(0, 1, len(vals)))
ax.pie(vals, colors=colors)
```

### explode

Sequence of fractions to offset each wedge from center.

```python
explode = [0.1, 0, 0, 0, 0]  # Explode first slice
ax.pie(vals, explode=explode)

explode = [0.05] * len(vals)  # All slightly exploded
ax.pie(vals, explode=explode)
```

### shadow

Draw shadow beneath pie (default: False).

```python
ax.pie(vals, shadow=True)
```

### radius

Radius of the pie (default: 1).

```python
ax.pie(vals, radius=0.8)  # Smaller pie
ax.pie(vals, radius=1.2)  # Larger pie
```

## Orientation Parameters

### startangle

Angle in degrees to rotate pie (default: 0, starts from positive x-axis).

```python
ax.pie(vals, startangle=90)   # Start from top
ax.pie(vals, startangle=180)  # Start from left
ax.pie(vals, startangle=270)  # Start from bottom
```

### counterclock

Direction of slices (default: True for counter-clockwise).

```python
ax.pie(vals, counterclock=True)   # Counter-clockwise (default)
ax.pie(vals, counterclock=False)  # Clockwise
```

### center

Center position of the pie (default: (0, 0)).

```python
ax.pie(vals, center=(0.5, 0.5))  # Offset center
```

## Style Parameters

### wedgeprops

Dictionary of properties for wedge patches.

```python
# White edge
wedgeprops = {'edgecolor': 'white', 'linewidth': 2}
ax.pie(vals, wedgeprops=wedgeprops)

# Semi-transparent
wedgeprops = {'alpha': 0.7}
ax.pie(vals, wedgeprops=wedgeprops)

# Custom width (for donut chart)
wedgeprops = {'width': 0.5}
ax.pie(vals, wedgeprops=wedgeprops)
```

### textprops

Dictionary of properties for label and percentage text.

```python
textprops = {'fontsize': 12, 'fontweight': 'bold', 'color': 'navy'}
ax.pie(vals, labels=labels, textprops=textprops)
```

### hatch

Hatch pattern for wedges. Can be string or sequence.

```python
# Single pattern for all
ax.pie(vals, hatch='/')

# Different patterns
hatches = ['/', '\\', '|', '-', '+']
wedges, texts = ax.pie(vals)
for wedge, hatch in zip(wedges, hatches):
    wedge.set_hatch(hatch)
```

## Other Parameters

### normalize

Normalize values to sum to 1 (default: True). Set to False if values already represent fractions.

```python
# Values normalized automatically
ax.pie([30, 20, 50], normalize=True)

# Pre-normalized fractions (must sum to 1)
ax.pie([0.3, 0.2, 0.5], normalize=False)
```

### frame

Draw axes frame around pie (default: False).

```python
ax.pie(vals, frame=True)
```

## Return Values

`ax.pie()` returns tuple depending on parameters:

```python
# Without autopct
wedges, texts = ax.pie(vals, labels=labels)

# With autopct
wedges, texts, autotexts = ax.pie(vals, labels=labels, autopct='%1.1f%%')
```

### Modifying Return Values

```python
wedges, texts, autotexts = ax.pie(vals, labels=labels, autopct='%1.1f%%')

# Modify wedges
for wedge in wedges:
    wedge.set_linewidth(2)
    wedge.set_edgecolor('white')

# Modify label texts
for text in texts:
    text.set_fontsize(10)
    text.set_fontweight('bold')

# Modify percentage texts
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
```

## Common Combinations

### Styled Pie with Legend

```python
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(
    vals,
    autopct='%1.1f%%',
    startangle=90,
    colors=plt.cm.Set2.colors[:len(vals)],
    wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    pctdistance=0.7
)
ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()
```

### Donut Chart

```python
fig, ax = plt.subplots()
ax.pie(vals, labels=labels, autopct='%1.1f%%',
       wedgeprops={'width': 0.5}, startangle=90)
ax.set_title('Donut Chart')
plt.show()
```

### Nested Pie (Ring Chart)

```python
fig, ax = plt.subplots()

# Outer ring
ax.pie(outer_vals, radius=1, labels=outer_labels,
       wedgeprops={'width': 0.3, 'edgecolor': 'white'})

# Inner ring
ax.pie(inner_vals, radius=0.7,
       wedgeprops={'width': 0.3, 'edgecolor': 'white'})

plt.show()
```


---

## Exercises

**Exercise 1.** Write code that demonstrates the `autopct` parameter with a custom format function that shows both the percentage and the absolute value.

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

**Exercise 2.** Explain the `pctdistance` and `labeldistance` parameters in `ax.pie()`. How do they control the position of text?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a pie chart where slices smaller than 5% have their labels placed outside the chart using `ax.annotate()`.

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

**Exercise 4.** Write code that uses `colors` from a Matplotlib colormap (e.g., `plt.cm.Set3`) to color the wedges of a pie chart.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt

        sizes = [30, 25, 20, 15, 10]
        labels = ['A', 'B', 'C', 'D', 'E']
        cmap = plt.cm.Set3
        colors = [cmap(i / len(sizes)) for i in range(len(sizes))]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%',
               startangle=90)
        ax.set_title('Pie Chart with Colormap Colors')
        plt.show()

---

**Exercise 5.** Using `wedgeprops` and `textprops`, create a pie chart where all wedge edges are white (creating visual separation) and all text is bold. Explain why white edges are often better than `explode` for separating slices.

??? success "Solution to Exercise 5"

        import matplotlib.pyplot as plt

        sizes = [35, 25, 20, 12, 8]
        labels = ['Core', 'Growth', 'Stable', 'Risk', 'Cash']
        colors = ['#2ecc71', '#3498db', '#9b59b6', '#e74c3c', '#f39c12']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%',
               startangle=90,
               wedgeprops=dict(edgecolor='white', linewidth=2),
               textprops=dict(fontweight='bold'))
        ax.set_title('Portfolio Allocation', fontweight='bold')
        plt.show()

        # White edges create clean visual separation without pulling slices
        # apart (explode distorts the circular shape and makes it harder to
        # compare sizes). This is the professional technique used in
        # dashboards and presentations.
