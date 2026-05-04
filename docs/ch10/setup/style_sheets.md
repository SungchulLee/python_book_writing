# Style Sheets

!!! tip "Mental Model"
    Style sheets are like CSS for Matplotlib. A single `plt.style.use('ggplot')` call changes dozens of defaults -- colors, fonts, backgrounds, line widths -- so your plots look polished without setting each property by hand. Think of them as preset themes you can swap in one line.

    The deeper role: **styles influence perception, not just appearance.** Contrast
    affects visibility, gridlines affect readability, and color choices affect
    interpretation. Styles modify how visual encodings are perceived, but do not
    change the underlying data mapping — they define the **visual language** of
    your plots.

!!! note "Design Principles"
    Style matters, but **clarity beats decoration**. A few rules:

    - **Consistency** matters more than which style you pick — use one style throughout a project
    - **Avoid overly dark or light extremes** unless the context demands it (e.g., dark mode for presentations)
    - **Data ink ratio** — maximize the ink spent on data, minimize decorative elements
    - When in doubt, use `seaborn-v0_8-whitegrid` for clean, professional output

## What are Style Sheets?

Style sheets are predefined sets of rcParams that control the appearance of Matplotlib figures. They provide a quick way to change the overall look of your plots.

```python
import matplotlib.pyplot as plt

# Apply a style
plt.style.use('seaborn-v0_8')
```

---

## Available Styles

### List All Styles

```python
print(plt.style.available)
```

Common styles:
- `'default'` — Matplotlib default
- `'seaborn-v0_8'` — Seaborn-inspired (clean, modern)
- `'ggplot'` — R's ggplot2 style
- `'fivethirtyeight'` — FiveThirtyEight blog style
- `'bmh'` — Bayesian Methods for Hackers
- `'dark_background'` — White on dark
- `'grayscale'` — Black and white
- `'classic'` — Old Matplotlib style

---

## Using Styles

### Global Style

```python
# Apply to all subsequent plots
plt.style.use('ggplot')

# Create plots with ggplot style
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
```

### Temporary Style (Context Manager)

```python
# Use style only within this block
with plt.style.context('dark_background'):
    plt.plot([1, 2, 3], [1, 4, 9])
    plt.show()

# Back to default style here
```

### Combining Styles

```python
# Apply multiple styles (later overrides earlier)
plt.style.use(['seaborn-v0_8', 'seaborn-v0_8-talk'])
```

---

## Style Comparison

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
styles = ['default', 'seaborn-v0_8', 'ggplot', 'fivethirtyeight']

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for ax, style in zip(axes.flat, styles):
    with plt.style.context(style):
        ax.plot(x, np.sin(x), label='sin')
        ax.plot(x, np.cos(x), label='cos')
        ax.set_title(f"Style: '{style}'")
        ax.legend()

plt.tight_layout()
plt.show()
```

---

## Seaborn Styles

Seaborn-based styles (prefix `seaborn-v0_8`):

| Style | Description |
|-------|-------------|
| `seaborn-v0_8` | Base seaborn style |
| `seaborn-v0_8-whitegrid` | White background with grid |
| `seaborn-v0_8-darkgrid` | Gray background with grid |
| `seaborn-v0_8-white` | White background, no grid |
| `seaborn-v0_8-dark` | Gray background, no grid |
| `seaborn-v0_8-talk` | Larger fonts for presentations |
| `seaborn-v0_8-poster` | Even larger for posters |
| `seaborn-v0_8-paper` | Smaller for publications |

```python
# Combine base style with size variant
plt.style.use(['seaborn-v0_8-whitegrid', 'seaborn-v0_8-talk'])
```

---

## Custom Style Files

### Create a Style File

Create `my_style.mplstyle`:

```ini
# Figure
figure.figsize: 10, 6
figure.facecolor: white

# Axes
axes.facecolor: f5f5f5
axes.edgecolor: cccccc
axes.labelsize: 12
axes.titlesize: 14
axes.grid: True

# Grid
grid.color: white
grid.linestyle: -
grid.linewidth: 1

# Lines
lines.linewidth: 2
lines.markersize: 8

# Font
font.family: sans-serif
font.size: 11

# Legend
legend.frameon: False
legend.fontsize: 10
```

### Use Custom Style

```python
# From file path
plt.style.use('./my_style.mplstyle')

# Or place in matplotlib config directory
# ~/.config/matplotlib/stylelib/my_style.mplstyle
plt.style.use('my_style')
```

---

## Modifying rcParams Directly

### Temporary Changes

```python
# Change specific parameters
plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['font.size'] = 12
```

### Reset to Defaults

```python
# Reset all to defaults
plt.rcdefaults()

# Or reset to a specific style
plt.style.use('default')
```

### Context Manager for rcParams

```python
with plt.rc_context({'lines.linewidth': 3, 'font.size': 14}):
    plt.plot([1, 2, 3])
    plt.show()
# Back to original settings
```

---

## Best Practices

### For Publications

```python
plt.style.use('seaborn-v0_8-paper')
plt.rcParams.update({
    'font.size': 8,
    'axes.labelsize': 9,
    'axes.titlesize': 10,
    'figure.figsize': [3.5, 2.5],  # Single column width
    'savefig.dpi': 300
})
```

### For Presentations

```python
plt.style.use(['seaborn-v0_8', 'seaborn-v0_8-talk'])
plt.rcParams.update({
    'figure.figsize': [12, 8],
    'lines.linewidth': 3
})
```

### For Dark Mode

```python
plt.style.use('dark_background')
```

---

## Summary

| Function | Purpose |
|----------|---------|
| `plt.style.use(style)` | Apply style globally |
| `plt.style.context(style)` | Apply style temporarily |
| `plt.style.available` | List all available styles |
| `plt.rcParams[key] = value` | Modify individual setting |
| `plt.rcdefaults()` | Reset to defaults |
| `plt.rc_context(dict)` | Temporary rcParams changes |

**Key Takeaways**:

- Use style sheets for consistent, professional plots
- `seaborn-v0_8` styles are clean and modern
- Combine styles for customization
- Create custom `.mplstyle` files for reusable configurations
- Use context managers for temporary style changes


---

## Exercises

**Exercise 1.** Write code that lists all available Matplotlib style sheets using `plt.style.available` and prints how many are available.

??? success "Solution to Exercise 1"
        import matplotlib.pyplot as plt

        styles = plt.style.available
        print(f"Number of styles: {len(styles)}")
        for s in sorted(styles):
            print(f"  {s}")

---

**Exercise 2.** Explain the difference between `plt.style.use()` and `plt.style.context()`. When would you use each?

??? success "Solution to Exercise 2"
    `plt.style.use(name)` applies a style **globally** — all subsequent plots use it until you call `plt.style.use('default')` or `plt.rcdefaults()`. Use it at the top of a script or notebook when you want a consistent look throughout.

    `plt.style.context(name)` applies a style **temporarily** inside a `with` block. When the block exits, the previous style is restored. Use it when you need one-off styled plots without affecting the rest of your code:

        with plt.style.context('dark_background'):
            plt.plot([1, 2, 3])
            plt.show()
        # style reverts here

---

**Exercise 3.** Write code that creates the same sin(x) plot using three different style sheets (`'default'`, `'ggplot'`, `'dark_background'`) in three subplots, using `plt.style.context()` for each.

??? success "Solution to Exercise 3"
        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 100)
        styles = ['default', 'ggplot', 'dark_background']

        fig, axes = plt.subplots(1, 3, figsize=(15, 4))
        for ax, style in zip(axes, styles):
            with plt.style.context(style):
                ax.plot(x, np.sin(x))
                ax.set_title(f"Style: '{style}'")
        plt.tight_layout()
        plt.show()

---

**Exercise 4.** Create a custom style by modifying `plt.rcParams` to set the default font size to 14, line width to 2, and grid alpha to 0.3. Plot a simple line to verify the settings, then reset to defaults.

??? success "Solution to Exercise 4"
        import matplotlib.pyplot as plt
        import numpy as np

        # Apply custom settings
        plt.rcParams['font.size'] = 14
        plt.rcParams['lines.linewidth'] = 2
        plt.rcParams['grid.alpha'] = 0.3

        x = np.linspace(0, 10, 100)
        fig, ax = plt.subplots()
        ax.plot(x, np.sin(x))
        ax.set_title('Custom Style')
        ax.grid(True)
        plt.show()

        # Reset to defaults
        plt.rcdefaults()
