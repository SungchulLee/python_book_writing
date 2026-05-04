# Box Plot Keywords

The `ax.boxplot()` method accepts numerous keyword arguments to control appearance and behavior.

!!! tip "Mental Model"
    Box plot keywords fall into three groups: data interpretation (`vert`, `whis`, `showfliers`), labeling (`labels`, `positions`), and styling (`patch_artist`, `boxprops`, `medianprops`). The most impactful is `patch_artist=True`, which switches boxes from outlines to filled patches, unlocking color customization.

!!! tip "Most Important Parameters"
    If you learn only four keywords, make it these:

    1. **`whis`** — controls outlier definition (default 1.5×IQR; set to `[5, 95]` for percentile-based whiskers)
    2. **`showfliers`** — toggle outlier dots on/off (hide them to reduce noise in dense data)
    3. **`notch`** — adds a confidence interval notch around the median (non-overlapping notches suggest different medians)
    4. **`patch_artist`** — switches boxes to filled patches (required for color customization)

## Labels

The `labels` keyword assigns names to each box on the x-axis.

### 1. Basic Labels

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data_a = np.random.normal(100, 10, 200)
data_b = np.random.normal(90, 20, 200)
data_c = np.random.normal(110, 15, 200)

fig, ax = plt.subplots()
ax.boxplot([data_a, data_b, data_c], labels=['Group A', 'Group B', 'Group C'])
plt.show()
```

### 2. LaTeX Labels

```python
ax.boxplot([data_a, data_b, data_c], 
           labels=[r'$10^4$', r'$5 \cdot 10^4$', r'$10^5$'])
```

### 3. Numeric Labels

```python
ax.boxplot([data_a, data_b, data_c], labels=['N=100', 'N=500', 'N=1000'])
```

## Widths

The `widths` keyword controls the width of each box.

### 1. Uniform Width

```python
ax.boxplot([data_a, data_b, data_c], widths=0.5)  # All boxes same width
```

### 2. Variable Widths

```python
ax.boxplot([data_a, data_b, data_c], widths=[0.2, 0.4, 0.6])
```

### 3. Proportional to Sample Size

```python
sizes = [100, 500, 1000]
widths = [np.sqrt(s) / np.sqrt(max(sizes)) * 0.8 for s in sizes]
ax.boxplot([data_a, data_b, data_c], widths=widths)
```

## Orientation

The `vert` keyword controls vertical or horizontal orientation.

### 1. Vertical (Default)

```python
ax.boxplot(data, vert=True)
```

### 2. Horizontal

```python
fig, ax = plt.subplots()
ax.boxplot([data_a, data_b, data_c], vert=False)
ax.set_yticklabels(['A', 'B', 'C'])
ax.set_xlabel('Value')
plt.show()
```

### 3. Use Case

Horizontal orientation works well when labels are long or when comparing many groups.

## Notch

The `notch` keyword adds confidence interval notches around the median.

### 1. Enable Notches

```python
ax.boxplot(data, notch=True)
```

### 2. Interpretation

Non-overlapping notches between two boxes suggest the medians differ significantly at approximately the 95% confidence level.

### 3. Notch Calculation

```python
# Notch extent approximation
notch_extent = 1.57 * IQR / np.sqrt(n)
```

## Patch Artist

The `patch_artist` keyword enables filled boxes for color customization.

### 1. Enable Patch Artist

```python
bp = ax.boxplot(data, patch_artist=True)
```

### 2. Access Box Patches

```python
for patch in bp['boxes']:
    patch.set_facecolor('lightblue')
```

### 3. Required for Fill Colors

Without `patch_artist=True`, boxes are drawn as lines only and cannot be filled.

## Show Statistics

Keywords control which statistical markers appear.

### 1. Show Mean

```python
ax.boxplot(data, showmeans=True)
```

### 2. Show Fliers (Outliers)

```python
ax.boxplot(data, showfliers=True)   # Default
ax.boxplot(data, showfliers=False)  # Hide outliers
```

### 3. Mean Line Instead of Point

```python
ax.boxplot(data, showmeans=True, meanline=True)
```

## Whisker Range

The `whis` keyword controls whisker extent.

### 1. Default (1.5 IQR)

```python
ax.boxplot(data, whis=1.5)
```

### 2. Custom Multiplier

```python
ax.boxplot(data, whis=2.0)  # Fewer outliers shown
```

### 3. Percentile Range

```python
ax.boxplot(data, whis=[5, 95])  # Whiskers at 5th and 95th percentiles
```

---

## Exercises

**Exercise 1.**
Create a box plot of three datasets with the following customizations: `notch=True`, `patch_artist=True`, `showmeans=True` with a diamond marker. Use different face colors for each box and set `medianprops` to display a red line.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = [np.random.randn(100) + i for i in range(3)]

        fig, ax = plt.subplots(figsize=(8, 5))
        bp = ax.boxplot(data, notch=True, patch_artist=True, showmeans=True,
                         meanprops=dict(marker='D', markerfacecolor='gold', markersize=8),
                         medianprops=dict(color='red', linewidth=2))

        colors = ['lightblue', 'lightcoral', 'lightgreen']
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)

        ax.set_xticklabels(['Group 1', 'Group 2', 'Group 3'])
        ax.set_title('Notched Box Plot with Means')
        plt.show()

---

**Exercise 2.**
Create a box plot using `showfliers=False` to hide outliers, and instead overlay individual data points using `ax.scatter` with jitter (small random horizontal offsets). Use 200 samples from a standard normal distribution across 4 groups.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = [np.random.randn(200) for _ in range(4)]

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.boxplot(data, showfliers=False, patch_artist=True,
                    boxprops=dict(facecolor='lightyellow'))

        for i, d in enumerate(data, 1):
            jitter = np.random.uniform(-0.15, 0.15, len(d))
            ax.scatter(np.full_like(d, i) + jitter, d, alpha=0.3, s=10, color='steelblue')

        ax.set_xticklabels(['A', 'B', 'C', 'D'])
        ax.set_title('Box Plot with Jittered Data Points')
        plt.show()

---

**Exercise 3.**
Create a box plot with `widths=[0.3, 0.5, 0.7, 0.9]` for four datasets to show how box width affects visual perception. Use `patch_artist=True` with graduated blue colors (light to dark). Set `whiskerprops`, `capprops`, and `flierprops` to customize every visible component.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = [np.random.randn(100) * (i + 1) for i in range(4)]

        fig, ax = plt.subplots(figsize=(8, 5))
        bp = ax.boxplot(data, widths=[0.3, 0.5, 0.7, 0.9], patch_artist=True,
                         whiskerprops=dict(color='navy', linewidth=1.5),
                         capprops=dict(color='navy', linewidth=2),
                         flierprops=dict(marker='o', markerfacecolor='red', markersize=4))

        blues = ['#c6dbef', '#6baed6', '#2171b5', '#08306b']
        for patch, color in zip(bp['boxes'], blues):
            patch.set_facecolor(color)

        ax.set_xticklabels(['Narrow', 'Medium', 'Wide', 'Widest'])
        ax.set_title('Variable Width Box Plots')
        plt.show()
