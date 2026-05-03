# Styling and Colors

Customize box plot appearance through color schemes, line styles, and component-specific properties.

!!! tip "Mental Model"
    By default, `boxplot()` draws unfilled outlines. Set `patch_artist=True` to get filled rectangles, then use `boxprops`, `medianprops`, `whiskerprops`, `capprops`, and `flierprops` dictionaries to style each component independently. Think of each dictionary as a CSS rule targeting one part of the box plot anatomy.

## Box Colors

Use `patch_artist=True` to enable box filling with colors.

### 1. Single Color

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in range(1, 5)]

fig, ax = plt.subplots()
bp = ax.boxplot(data, patch_artist=True)

for patch in bp['boxes']:
    patch.set_facecolor('lightblue')

plt.show()
```

### 2. Multiple Colors

```python
colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink']

bp = ax.boxplot(data, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
```

### 3. Colormap Colors

```python
import matplotlib.cm as cm

cmap = cm.get_cmap('viridis')
colors = [cmap(i / len(data)) for i in range(len(data))]

bp = ax.boxplot(data, patch_artist=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
```

## Component Properties

Each box plot component can be styled individually using property dictionaries.

### 1. Box Properties

```python
boxprops = dict(facecolor='lightblue', edgecolor='navy', linewidth=2)
ax.boxplot(data, patch_artist=True, boxprops=boxprops)
```

### 2. Whisker Properties

```python
whiskerprops = dict(color='gray', linewidth=1.5, linestyle='--')
ax.boxplot(data, whiskerprops=whiskerprops)
```

### 3. Cap Properties

```python
capprops = dict(color='black', linewidth=2)
ax.boxplot(data, capprops=capprops)
```

## Median Styling

Customize the median line appearance.

### 1. Color and Width

```python
medianprops = dict(color='red', linewidth=2)
ax.boxplot(data, medianprops=medianprops)
```

### 2. Line Style

```python
medianprops = dict(color='darkred', linewidth=2, linestyle='-')
ax.boxplot(data, medianprops=medianprops)
```

### 3. Full Example

```python
fig, ax = plt.subplots()
bp = ax.boxplot(data, 
                patch_artist=True,
                medianprops=dict(color='white', linewidth=2))

for patch in bp['boxes']:
    patch.set_facecolor('steelblue')

plt.show()
```

## Mean Marker Styling

Customize the mean indicator appearance.

### 1. Mean Properties

```python
meanprops = dict(marker='D', 
                 markerfacecolor='red', 
                 markeredgecolor='darkred',
                 markersize=8)

ax.boxplot(data, showmeans=True, meanprops=meanprops)
```

### 2. Mean as Line

```python
meanprops = dict(color='green', linewidth=2, linestyle='--')
ax.boxplot(data, showmeans=True, meanline=True, meanprops=meanprops)
```

### 3. Diamond vs Triangle

```python
# Diamond marker
meanprops = dict(marker='D', markerfacecolor='red')

# Triangle marker
meanprops = dict(marker='^', markerfacecolor='green')
```

## Outlier Styling

Customize flier (outlier) point appearance.

### 1. Basic Flier Properties

```python
flierprops = dict(marker='o',
                  markerfacecolor='red',
                  markersize=8,
                  markeredgecolor='darkred')

ax.boxplot(data, flierprops=flierprops)
```

### 2. Different Marker Shapes

```python
# Circle
flierprops = dict(marker='o', markerfacecolor='red')

# Star
flierprops = dict(marker='*', markerfacecolor='gold', markersize=10)

# Diamond
flierprops = dict(marker='D', markerfacecolor='purple')
```

### 3. Transparent Outliers

```python
flierprops = dict(marker='o', 
                  markerfacecolor='none',
                  markeredgecolor='gray',
                  alpha=0.5)
```

## Complete Styled Example

Combine all styling options for a polished visualization.

### 1. Professional Style

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = [np.random.normal(0, std, 100) for std in range(1, 5)]

fig, ax = plt.subplots(figsize=(8, 5))

bp = ax.boxplot(data,
                patch_artist=True,
                notch=True,
                widths=0.6,
                boxprops=dict(facecolor='steelblue', edgecolor='navy'),
                whiskerprops=dict(color='navy', linewidth=1.5),
                capprops=dict(color='navy', linewidth=1.5),
                medianprops=dict(color='white', linewidth=2),
                flierprops=dict(marker='o', markerfacecolor='coral', 
                               markeredgecolor='darkred', markersize=6))

ax.set_xticklabels([r'$\sigma=1$', r'$\sigma=2$', r'$\sigma=3$', r'$\sigma=4$'])
ax.set_ylabel('Value')
ax.set_title('Customized Box Plot')
ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()
```

### 2. Return Value Dictionary

```python
# bp dictionary contains all artists
print(bp.keys())
# dict_keys(['whiskers', 'caps', 'boxes', 'medians', 'fliers', 'means'])
```

### 3. Post-Creation Modification

```python
bp = ax.boxplot(data, patch_artist=True)

# Modify after creation
bp['boxes'][0].set_facecolor('red')
bp['medians'][0].set_color('white')
bp['whiskers'][0].set_linestyle('--')
```

---

## Exercises

**Exercise 1.**
Create a box plot for five groups using `patch_artist=True` where each box is filled with a color from the `tab10` colormap. Set the median line to white with `linewidth=2` and the whiskers to match the box face color.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = [np.random.randn(100) + i for i in range(5)]

        fig, ax = plt.subplots(figsize=(8, 5))
        bp = ax.boxplot(data, patch_artist=True,
                         medianprops=dict(color='white', linewidth=2))

        cmap = plt.cm.tab10
        for i, (patch, whisker_pair) in enumerate(zip(bp['boxes'],
                zip(bp['whiskers'][::2], bp['whiskers'][1::2]))):
            color = cmap(i / 5)
            patch.set_facecolor(color)
            for w in whisker_pair:
                w.set_color(color)

        ax.set_xticklabels([f'Group {i+1}' for i in range(5)])
        ax.set_title('Colormap-Styled Box Plot')
        plt.show()

---

**Exercise 2.**
Create a dark-themed box plot by setting `plt.style.use('dark_background')`. Plot four datasets with neon-colored boxes (bright green, cyan, magenta, yellow). Set edge colors to white and flier markers to star shape with white color.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = [np.random.randn(100) + i for i in range(4)]

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(8, 5))

        bp = ax.boxplot(data, patch_artist=True,
                         flierprops=dict(marker='*', markerfacecolor='white', markersize=6))

        neon_colors = ['#39ff14', '#00ffff', '#ff00ff', '#ffff00']
        for patch, color in zip(bp['boxes'], neon_colors):
            patch.set_facecolor(color)
            patch.set_edgecolor('white')
            patch.set_alpha(0.7)

        ax.set_xticklabels(['A', 'B', 'C', 'D'])
        ax.set_title('Dark Theme Box Plot')
        plt.show()
        plt.style.use('default')

---

**Exercise 3.**
Create a box plot where the box color reflects the median value using a colormap. Generate 6 datasets with medians ranging from low to high. Map each median to a color using `plt.cm.RdYlGn` (red for low, green for high). Add a colorbar to show the mapping.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.colors import Normalize

        np.random.seed(42)
        medians_target = [1, 3, 5, 7, 9, 11]
        data = [np.random.randn(100) + m for m in medians_target]
        actual_medians = [np.median(d) for d in data]

        norm = Normalize(vmin=min(actual_medians), vmax=max(actual_medians))
        cmap = plt.cm.RdYlGn

        fig, ax = plt.subplots(figsize=(10, 5))
        bp = ax.boxplot(data, patch_artist=True)

        for patch, med in zip(bp['boxes'], actual_medians):
            patch.set_facecolor(cmap(norm(med)))

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        plt.colorbar(sm, ax=ax, label='Median Value')
        ax.set_xticklabels([f'Set {i+1}' for i in range(6)])
        ax.set_title('Box Colors Mapped to Median Value')
        plt.show()
