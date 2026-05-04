# Combined Visualizations

Combine box plots with other chart types for comprehensive data analysis and presentation.

!!! tip "Mental Model"
    Box plots summarize but hide detail; histograms reveal shape but are hard to compare across groups. Combining them -- a box plot beside a histogram, or overlaid with a strip plot -- gives readers both the quick summary and the full picture. Use subplots side by side or overlay techniques to get the best of both worlds.

    The core principle: **different plots reveal different aspects of the same
    distribution.** A box plot shows center and spread; a histogram shows shape;
    a scatter/strip shows individual points. Combining them is not decoration — it
    is choosing the right **resolution** for each aspect of the data:

    Combine at most **2–3 layers**. Too many overlays reduce clarity — each additional layer should add information the reader cannot get from the existing ones.

    | Combination | What you gain |
    |-------------|--------------|
    | Box + histogram | Summary + shape |
    | Box + scatter/strip | Summary + raw data |
    | Violin + box | Density shape + quartile markers |

## Box Plot with Histogram

Pair box plots with histograms to show both summary statistics and distributional shape.

### 1. Side by Side Layout

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.normal(100, 15, 500)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.hist(data, bins=25, edgecolor='black', alpha=0.7)
ax1.axvline(np.mean(data), color='red', linestyle='--', label='Mean')
ax1.axvline(np.median(data), color='blue', linestyle='--', label='Median')
ax1.legend()
ax1.set_title('Histogram')

ax2.boxplot(data)
ax2.set_title('Box Plot')

plt.tight_layout()
plt.show()
```

### 2. Stacked Vertically

```python
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), 
                               gridspec_kw={'height_ratios': [3, 1]})

ax1.hist(data, bins=25, edgecolor='black', alpha=0.7)
ax1.set_ylabel('Frequency')

ax2.boxplot(data, vert=False)
ax2.set_xlabel('Value')

plt.tight_layout()
plt.show()
```

### 3. Reusable Function

```python
def plot_distribution(data, title='Distribution Analysis', bins=20):
    mean = np.mean(data)
    median = np.median(data)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(title, fontsize=14)

    ax1.hist(data, bins=bins, density=True, alpha=0.7, edgecolor='black')
    ax1.axvline(mean, color='blue', linestyle='--', label=f'Mean: {mean:.1f}')
    ax1.axvline(median, color='red', linestyle='--', label=f'Median: {median:.1f}')
    ax1.legend()
    ax1.set_title('Histogram')

    ax2.boxplot(data)
    ax2.set_title('Box Plot')

    plt.tight_layout()
    plt.show()
```

## Box Plot with Reference Lines

Add horizontal reference lines to compare distributions against benchmarks.

### 1. Single Reference Line

```python
fig, ax = plt.subplots()

data = [np.random.normal(100, 15, 100) for _ in range(4)]
ax.boxplot(data, labels=['Q1', 'Q2', 'Q3', 'Q4'])
ax.axhline(y=100, color='red', linestyle='--', label='Target', alpha=0.7)
ax.legend()
ax.set_ylabel('Performance')

plt.show()
```

### 2. Multiple Reference Lines

```python
fig, ax = plt.subplots()

ax.boxplot(data, labels=['Q1', 'Q2', 'Q3', 'Q4'])
ax.axhline(y=90, color='red', linestyle='--', label='Minimum', alpha=0.7)
ax.axhline(y=100, color='green', linestyle='--', label='Target', alpha=0.7)
ax.axhline(y=110, color='blue', linestyle='--', label='Stretch', alpha=0.7)
ax.legend()

plt.show()
```

### 3. Shaded Region

```python
fig, ax = plt.subplots()

ax.boxplot(data, labels=['Q1', 'Q2', 'Q3', 'Q4'])
ax.axhspan(95, 105, color='green', alpha=0.2, label='Acceptable Range')
ax.legend()

plt.show()
```

## Box Plot with Scatter Overlay

Show individual data points alongside the box plot summary.

### 1. Jittered Points

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = [np.random.normal(0, std, 50) for std in range(1, 5)]

fig, ax = plt.subplots()

bp = ax.boxplot(data, patch_artist=True, showfliers=False)
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
    patch.set_alpha(0.5)

for i, d in enumerate(data, 1):
    jitter = np.random.normal(0, 0.04, len(d))
    ax.scatter(np.full_like(d, i) + jitter, d, alpha=0.5, s=20, c='steelblue')

plt.show()
```

### 2. Swarm-Like Layout

```python
def add_points(ax, data, positions, width=0.2):
    for pos, d in zip(positions, data):
        n = len(d)
        offsets = np.linspace(-width/2, width/2, n)
        ax.scatter(np.full(n, pos) + offsets, np.sort(d), 
                   alpha=0.4, s=15, c='darkblue')

fig, ax = plt.subplots()
bp = ax.boxplot(data, showfliers=False)
add_points(ax, data, range(1, len(data) + 1))
plt.show()
```

### 3. Strip Plot Style

```python
fig, ax = plt.subplots()

ax.boxplot(data, showfliers=False, widths=0.3)

for i, d in enumerate(data, 1):
    y = d
    x = np.random.uniform(i - 0.15, i + 0.15, len(d))
    ax.scatter(x, y, alpha=0.3, s=10, c='black')

plt.show()
```

## Grouped Box Plots

Compare multiple categories across groups.

### 1. Manual Positioning

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

group1_a = np.random.normal(100, 10, 50)
group1_b = np.random.normal(110, 15, 50)
group2_a = np.random.normal(90, 12, 50)
group2_b = np.random.normal(95, 18, 50)

fig, ax = plt.subplots()

positions_a = [1, 3]
positions_b = [1.6, 3.6]

bp1 = ax.boxplot([group1_a, group2_a], positions=positions_a, 
                  widths=0.5, patch_artist=True)
bp2 = ax.boxplot([group1_b, group2_b], positions=positions_b, 
                  widths=0.5, patch_artist=True)

for patch in bp1['boxes']:
    patch.set_facecolor('lightblue')
for patch in bp2['boxes']:
    patch.set_facecolor('lightcoral')

ax.set_xticks([1.3, 3.3])
ax.set_xticklabels(['Group 1', 'Group 2'])
ax.legend([bp1['boxes'][0], bp2['boxes'][0]], ['Method A', 'Method B'])

plt.show()
```

### 2. Color by Category

```python
fig, ax = plt.subplots(figsize=(10, 5))

data_dict = {
    'Control': [np.random.normal(100, 10, 50) for _ in range(3)],
    'Treatment': [np.random.normal(110, 12, 50) for _ in range(3)]
}

colors = {'Control': 'lightblue', 'Treatment': 'lightcoral'}
positions = {'Control': [1, 4, 7], 'Treatment': [2, 5, 8]}

for label, datasets in data_dict.items():
    bp = ax.boxplot(datasets, positions=positions[label], 
                    widths=0.8, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor(colors[label])

ax.set_xticks([1.5, 4.5, 7.5])
ax.set_xticklabels(['Week 1', 'Week 2', 'Week 3'])

plt.show()
```

### 3. Legend for Groups

```python
from matplotlib.patches import Patch

legend_elements = [Patch(facecolor='lightblue', label='Control'),
                   Patch(facecolor='lightcoral', label='Treatment')]
ax.legend(handles=legend_elements, loc='upper right')
```

## Box Plot with Violin Overlay

Combine box plots with violin plots for complete distribution visualization.

### 1. Overlay Approach

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = [np.random.normal(0, std, 200) for std in range(1, 5)]

fig, ax = plt.subplots()

vp = ax.violinplot(data, showextrema=False)
for body in vp['bodies']:
    body.set_alpha(0.3)

ax.boxplot(data, widths=0.1)

plt.show()
```

### 2. Side by Side

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5), sharey=True)

ax1.violinplot(data)
ax1.set_title('Violin Plot')

ax2.boxplot(data)
ax2.set_title('Box Plot')

plt.tight_layout()
plt.show()
```

### 3. Hybrid Visualization

```python
fig, ax = plt.subplots()

vp = ax.violinplot(data, showmedians=False, showextrema=False)
for body in vp['bodies']:
    body.set_facecolor('lightblue')
    body.set_alpha(0.5)

bp = ax.boxplot(data, widths=0.15, patch_artist=True,
                boxprops=dict(facecolor='white', edgecolor='black'),
                medianprops=dict(color='red', linewidth=2))

plt.show()
```

---

## Exercises

**Exercise 1.**
Create a figure with a box plot on the left and a histogram on the right showing the same dataset (500 samples from a skewed distribution using `np.random.exponential`). Use the box plot to identify the median and quartiles, then mark those same values on the histogram with vertical lines.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = np.random.exponential(2, 500)

        q1, median, q3 = np.percentile(data, [25, 50, 75])

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        ax1.boxplot(data, vert=True)
        ax1.set_title('Box Plot')

        ax2.hist(data, bins=30, color='steelblue', edgecolor='white', alpha=0.7)
        ax2.axvline(q1, color='orange', linestyle='--', label=f'Q1={q1:.2f}')
        ax2.axvline(median, color='red', linestyle='-', linewidth=2, label=f'Median={median:.2f}')
        ax2.axvline(q3, color='orange', linestyle='--', label=f'Q3={q3:.2f}')
        ax2.legend()
        ax2.set_title('Histogram with Quartile Lines')

        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Overlay a strip plot (individual points with jitter) on top of a box plot. Generate 4 groups of 50 samples from normal distributions with different means. Show the box plot with `patch_artist=True` and `alpha=0.5`, then scatter the actual points on top.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = [np.random.normal(loc=m, scale=1, size=50) for m in [2, 4, 6, 8]]

        fig, ax = plt.subplots(figsize=(8, 5))
        bp = ax.boxplot(data, patch_artist=True, showfliers=False)

        colors = ['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.5)

        for i, d in enumerate(data, 1):
            jitter = np.random.uniform(-0.15, 0.15, len(d))
            ax.scatter(np.full_like(d, i) + jitter, d, alpha=0.6, s=20, color='black', zorder=3)

        ax.set_xticklabels(['Group 1', 'Group 2', 'Group 3', 'Group 4'])
        ax.set_title('Box Plot with Strip Plot Overlay')
        plt.show()

---

**Exercise 3.**
Create a combined visualization with three panels stacked vertically: a box plot at the top showing distribution summary, a histogram in the middle showing frequency, and a rug plot (short vertical lines at each data point) at the bottom. Use 300 samples from a bimodal distribution (mix of two normals).

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = np.concatenate([np.random.normal(-2, 0.8, 150),
                                np.random.normal(2, 0.8, 150)])

        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8),
                                              gridspec_kw={'height_ratios': [1, 3, 0.5]},
                                              sharex=True)

        ax1.boxplot(data, vert=False, widths=0.6)
        ax1.set_yticks([])
        ax1.set_title('Distribution Summary')

        ax2.hist(data, bins=40, color='steelblue', edgecolor='white')
        ax2.set_ylabel('Frequency')

        ax3.eventplot(data, orientation='horizontal', lineoffsets=0.5,
                       linelengths=0.8, color='black', linewidths=0.5)
        ax3.set_yticks([])
        ax3.set_xlabel('Value')
        ax3.set_ylabel('Rug')

        plt.tight_layout()
        plt.show()
