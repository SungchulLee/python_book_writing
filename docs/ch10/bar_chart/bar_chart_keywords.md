# Bar Chart Keywords

The `ax.bar()` and `ax.barh()` methods accept numerous keyword arguments to control bar appearance and behavior.

!!! tip "Mental Model"
    Bar chart keywords control the geometry and look of each rectangle: `width` sets thickness, `color` fills the bar, `edgecolor` outlines it, `align` shifts its position, and `bottom` offsets its base (used for stacking). Like scatter keywords, each can be a scalar for uniform styling or an array for per-bar control.

## Width and Height

The `width` parameter controls bar thickness for vertical bars; `height` for horizontal bars.

### 1. Default Width

```python
import matplotlib.pyplot as plt
import numpy as np

categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]

fig, ax = plt.subplots()
ax.bar(categories, values)  # Default width = 0.8
plt.show()
```

### 2. Custom Width

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, width in zip(axes, [0.3, 0.6, 0.9]):
    ax.bar(categories, values, width=width)
    ax.set_title(f'width = {width}')

plt.tight_layout()
plt.show()
```

### 3. Variable Widths

```python
widths = [0.5, 0.7, 0.9, 0.6, 0.4]

fig, ax = plt.subplots()
ax.bar(categories, values, width=widths)
plt.show()
```

## Color

The `color` parameter sets bar fill color.

### 1. Single Color

```python
fig, ax = plt.subplots()
ax.bar(categories, values, color='steelblue')
plt.show()
```

### 2. Named Colors

```python
ax.bar(categories, values, color='coral')
ax.bar(categories, values, color='forestgreen')
ax.bar(categories, values, color='goldenrod')
```

### 3. Individual Colors

```python
colors = ['red', 'green', 'blue', 'orange', 'purple']

fig, ax = plt.subplots()
ax.bar(categories, values, color=colors)
plt.show()
```

## Edge Properties

Control bar border appearance.

### 1. Edge Color

```python
fig, ax = plt.subplots()
ax.bar(categories, values, color='lightblue', edgecolor='navy')
plt.show()
```

### 2. Edge Width

```python
ax.bar(categories, values, color='lightblue', edgecolor='navy', linewidth=2)
```

### 3. No Edge

```python
ax.bar(categories, values, edgecolor='none')
```

## Alpha (Transparency)

The `alpha` parameter sets bar transparency.

### 1. Uniform Alpha

```python
fig, ax = plt.subplots()
ax.bar(categories, values, alpha=0.7)
plt.show()
```

### 2. Overlapping Bars

```python
x = np.arange(5)
values1 = [23, 45, 56, 78, 32]
values2 = [30, 40, 50, 60, 40]

fig, ax = plt.subplots()
ax.bar(x, values1, alpha=0.7, label='Series 1')
ax.bar(x, values2, alpha=0.7, label='Series 2')
ax.legend()
plt.show()
```

### 3. Highlight Effect

```python
alphas = [0.3, 0.3, 1.0, 0.3, 0.3]  # Highlight third bar

fig, ax = plt.subplots()
for i, (cat, val, a) in enumerate(zip(categories, values, alphas)):
    ax.bar(cat, val, alpha=a, color='steelblue')
plt.show()
```

## Alignment

The `align` parameter controls bar position relative to x coordinate.

### 1. Center Alignment (Default)

```python
x = np.arange(5)

fig, ax = plt.subplots()
ax.bar(x, values, align='center')
ax.set_xticks(x)
plt.show()
```

### 2. Edge Alignment

```python
fig, ax = plt.subplots()
ax.bar(x, values, align='edge')
ax.set_xticks(x)
plt.show()
```

### 3. Comparison

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

axes[0].bar(x, values, align='center', width=0.8)
axes[0].set_title("align='center'")
axes[0].axvline(x=2, color='red', linestyle='--')

axes[1].bar(x, values, align='edge', width=0.8)
axes[1].set_title("align='edge'")
axes[1].axvline(x=2, color='red', linestyle='--')

plt.tight_layout()
plt.show()
```

## Bottom and Left

Offset bar base from zero.

### 1. Bottom Offset (Vertical)

```python
fig, ax = plt.subplots()
ax.bar(categories, values, bottom=10)
ax.axhline(y=10, color='red', linestyle='--')
plt.show()
```

### 2. Left Offset (Horizontal)

```python
fig, ax = plt.subplots()
ax.barh(categories, values, left=10)
ax.axvline(x=10, color='red', linestyle='--')
plt.show()
```

### 3. Building Stacked Bars

```python
values1 = [23, 45, 56, 78, 32]
values2 = [15, 25, 20, 30, 18]

fig, ax = plt.subplots()
ax.bar(categories, values1, label='Base')
ax.bar(categories, values2, bottom=values1, label='Addition')
ax.legend()
plt.show()
```

## Error Bars

Add error bars with `yerr` and `xerr`.

### 1. Symmetric Error

```python
errors = [3, 5, 4, 6, 3]

fig, ax = plt.subplots()
ax.bar(categories, values, yerr=errors, capsize=5)
plt.show()
```

### 2. Asymmetric Error

```python
lower_errors = [2, 3, 2, 4, 2]
upper_errors = [4, 6, 5, 8, 4]

fig, ax = plt.subplots()
ax.bar(categories, values, yerr=[lower_errors, upper_errors], capsize=5)
plt.show()
```

### 3. Error Bar Styling

```python
fig, ax = plt.subplots()
ax.bar(categories, values, yerr=errors, 
       capsize=5, 
       error_kw={'elinewidth': 2, 'ecolor': 'red', 'capthick': 2})
plt.show()
```

## Label

Add labels for legend display.

### 1. Label Parameter

```python
fig, ax = plt.subplots()
ax.bar(categories, values, label='2024 Sales')
ax.legend()
plt.show()
```

### 2. Multiple Series

```python
x = np.arange(5)
width = 0.35

fig, ax = plt.subplots()
ax.bar(x - width/2, values, width, label='2023')
ax.bar(x + width/2, [v * 1.1 for v in values], width, label='2024')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
plt.show()
```

### 3. Legend Location

```python
ax.legend(loc='upper left')
ax.legend(loc='upper right')
ax.legend(loc='best')
```

## Hatch Patterns

Add patterns to bars for print-friendly distinction.

### 1. Single Pattern

```python
fig, ax = plt.subplots()
ax.bar(categories, values, hatch='//')
plt.show()
```

### 2. Available Patterns

```python
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
patterns = ['/', '\\', '|', '-', '+', 'x', 'o', 'O']

for ax, pattern in zip(axes.flat, patterns):
    ax.bar(['A'], [1], hatch=pattern * 2, edgecolor='black')
    ax.set_title(f"hatch='{pattern}'")

plt.tight_layout()
plt.show()
```

### 3. Combined with Color

```python
fig, ax = plt.subplots()
ax.bar(categories, values, color='lightblue', hatch='//', edgecolor='navy')
plt.show()
```

## Combining Keywords

Create styled bar charts with multiple parameters.

### 1. Professional Style

```python
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(categories, values,
              color='steelblue',
              edgecolor='navy',
              linewidth=1.5,
              alpha=0.8,
              width=0.6)

ax.bar_label(bars, padding=3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.show()
```

### 2. Conditional Coloring

```python
colors = ['green' if v > 50 else 'red' for v in values]

fig, ax = plt.subplots()
ax.bar(categories, values, color=colors, edgecolor='black')
plt.show()
```

### 3. Gradient Effect

```python
import matplotlib.cm as cm

cmap = cm.get_cmap('Blues')
colors = [cmap(v / max(values)) for v in values]

fig, ax = plt.subplots()
ax.bar(categories, values, color=colors, edgecolor='navy')
plt.show()
```

---

## Exercises

**Exercise 1.**
Create a bar chart with five categories where bars above a threshold of 50 are colored green and bars below are colored red. Use values `[23, 65, 42, 78, 35]`. Add a horizontal dashed line at the threshold and use `edgecolor='black'` and `linewidth=1.5`.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt

        categories = ['A', 'B', 'C', 'D', 'E']
        values = [23, 65, 42, 78, 35]
        threshold = 50
        colors = ['green' if v > threshold else 'red' for v in values]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(categories, values, color=colors, edgecolor='black', linewidth=1.5)
        ax.axhline(y=threshold, color='gray', linestyle='--', label=f'Threshold = {threshold}')
        ax.legend()
        ax.set_title('Conditional Bar Coloring')
        plt.show()

---

**Exercise 2.**
Create a bar chart with error bars. Use categories `['A', 'B', 'C', 'D']`, values `[40, 55, 30, 70]`, and asymmetric errors `lower=[3, 4, 2, 5]`, `upper=[5, 7, 4, 8]`. Style the error bars with red color and cap size of 8. Use hatch pattern `'//'` on the bars.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt

        categories = ['A', 'B', 'C', 'D']
        values = [40, 55, 30, 70]
        lower = [3, 4, 2, 5]
        upper = [5, 7, 4, 8]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(categories, values, hatch='//', edgecolor='black', color='lightblue',
               yerr=[lower, upper], capsize=8,
               error_kw={'ecolor': 'red', 'elinewidth': 2, 'capthick': 2})
        ax.set_ylabel('Value')
        ax.set_title('Bar Chart with Asymmetric Error Bars')
        plt.show()

---

**Exercise 3.**
Create a grouped bar chart with three series using the `width` and positional offset technique. Categories are `['Q1', 'Q2', 'Q3', 'Q4']` with three series: `[20, 35, 30, 45]`, `[25, 32, 34, 40]`, `[15, 27, 28, 38]`. Use `width=0.25`, different colors, `alpha=0.85`, and `edgecolor='black'`. Add bar labels and a legend.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        categories = ['Q1', 'Q2', 'Q3', 'Q4']
        series1 = [20, 35, 30, 45]
        series2 = [25, 32, 34, 40]
        series3 = [15, 27, 28, 38]

        x = np.arange(len(categories))
        width = 0.25

        fig, ax = plt.subplots(figsize=(10, 6))
        b1 = ax.bar(x - width, series1, width, label='Product A', alpha=0.85, edgecolor='black')
        b2 = ax.bar(x, series2, width, label='Product B', alpha=0.85, edgecolor='black')
        b3 = ax.bar(x + width, series3, width, label='Product C', alpha=0.85, edgecolor='black')

        ax.bar_label(b1, padding=2, fontsize=8)
        ax.bar_label(b2, padding=2, fontsize=8)
        ax.bar_label(b3, padding=2, fontsize=8)

        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.set_title('Grouped Bar Chart')
        plt.tight_layout()
        plt.show()
