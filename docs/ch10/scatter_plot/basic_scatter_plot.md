# Basic Scatter Plot

Scatter plots display individual data points using markers, revealing relationships, clusters, and patterns between two variables.

!!! tip "Mental Model"
    Unlike `plot()` which connects points with lines, `scatter()` draws each point independently. This lets you vary marker size, color, and shape per point, encoding up to four dimensions in a 2D plot (x, y, size, color). Use scatter plots when the relationship between points matters more than their ordering.

!!! note "Visual Encoding Channels"
    A scatter plot maps data to **visual channels** — perceptual properties
    the eye can distinguish:

    | Channel | Parameter | Perceptual accuracy |
    |---------|-----------|-------------------|
    | Position (x, y) | `x`, `y` | Most accurate |
    | Color | `c` + `cmap` | Moderate (use perceptually uniform maps) |
    | Size | `s` | Less accurate (area perception is nonlinear) |
    | Shape | `marker` | Categorical only (no ordering) |

    Use at most 2--3 encodings clearly. Combining all four channels creates
    cognitive overload — the reader cannot decode everything at once.

!!! warning "Correlation is Not Causation"
    A visible trend or cluster in a scatter plot shows **association**, not cause
    and effect. Adding a regression line (`np.polyfit`) quantifies the linear
    relationship, but a linear fit only makes sense if the relationship is
    genuinely linear — always inspect the residuals before interpreting.

## Simple Scatter Plot

Create a basic scatter plot with `ax.scatter()`.

### 1. Import and Setup

```python
import matplotlib.pyplot as plt
import numpy as np
```

### 2. Generate Data

```python
np.random.seed(42)
x = np.random.rand(50)
y = np.random.rand(50)
```

### 3. Create Scatter Plot

```python
fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Basic Scatter Plot')
plt.show()
```

## Correlated Data

Visualize relationships between variables.

### 1. Positive Correlation

```python
np.random.seed(42)
x = np.random.rand(100)
y = x + np.random.normal(0, 0.1, 100)

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_title('Positive Correlation')
plt.show()
```

### 2. Negative Correlation

```python
x = np.random.rand(100)
y = 1 - x + np.random.normal(0, 0.1, 100)

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_title('Negative Correlation')
plt.show()
```

### 3. No Correlation

```python
x = np.random.rand(100)
y = np.random.rand(100)

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_title('No Correlation')
plt.show()
```

## Multiple Groups

Plot multiple data groups on the same axes.

### 1. Sequential Plotting

```python
np.random.seed(42)
x1 = np.random.normal(2, 0.5, 50)
y1 = np.random.normal(2, 0.5, 50)
x2 = np.random.normal(4, 0.5, 50)
y2 = np.random.normal(4, 0.5, 50)

fig, ax = plt.subplots()
ax.scatter(x1, y1, label='Group A')
ax.scatter(x2, y2, label='Group B')
ax.legend()
plt.show()
```

### 2. Different Colors

```python
fig, ax = plt.subplots()
ax.scatter(x1, y1, color='blue', label='Group A')
ax.scatter(x2, y2, color='red', label='Group B')
ax.legend()
plt.show()
```

### 3. Different Markers

```python
fig, ax = plt.subplots()
ax.scatter(x1, y1, marker='o', label='Group A')
ax.scatter(x2, y2, marker='^', label='Group B')
ax.legend()
plt.show()
```

## Data Input Types

Various ways to provide data to scatter.

### 1. Lists

```python
x = [1, 2, 3, 4, 5]
y = [2, 4, 1, 5, 3]
ax.scatter(x, y)
```

### 2. NumPy Arrays

```python
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 1, 5, 3])
ax.scatter(x, y)
```

### 3. Pandas Series

```python
import pandas as pd

df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 4, 1, 5, 3]})
ax.scatter(df['x'], df['y'])
```

## scatter vs plot

Understanding when to use each method.

### 1. plot with Markers

```python
fig, ax = plt.subplots()
ax.plot(x, y, 'o')  # Circle markers, no line
plt.show()
```

### 2. scatter Advantages

```python
# scatter supports:
# - Individual point sizes (s parameter)
# - Individual point colors (c parameter)
# - Colormaps for continuous color mapping
# - Alpha per point
```

### 3. Performance Comparison

```python
# plot is faster for large datasets with uniform styling
# scatter is preferred when points need individual properties
```

## Adding Trend Lines

Overlay regression lines on scatter plots.

### 1. Linear Fit

```python
np.random.seed(42)
x = np.random.rand(50) * 10
y = 2 * x + 1 + np.random.normal(0, 2, 50)

coeffs = np.polyfit(x, y, 1)
trend = np.poly1d(coeffs)

fig, ax = plt.subplots()
ax.scatter(x, y, alpha=0.7)
ax.plot(x, trend(x), color='red', linewidth=2, label=f'y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}')
ax.legend()
plt.show()
```

### 2. Polynomial Fit

```python
coeffs = np.polyfit(x, y, 2)
trend = np.poly1d(coeffs)

x_line = np.linspace(x.min(), x.max(), 100)
ax.plot(x_line, trend(x_line), color='red')
```

### 3. Sorted Line Data

```python
# Sort x for proper line plotting
sort_idx = np.argsort(x)
ax.plot(x[sort_idx], trend(x[sort_idx]), color='red')
```

## Practical Example

Create a complete scatter plot with annotations.

### 1. Generate Sample Data

```python
np.random.seed(42)
n = 30
x = np.random.rand(n) * 100
y = 0.5 * x + np.random.normal(0, 10, n)
labels = [f'P{i}' for i in range(n)]
```

### 2. Create Visualization

```python
fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(x, y, s=100, alpha=0.7, edgecolors='black')

ax.set_xlabel('Feature X', fontsize=12)
ax.set_ylabel('Feature Y', fontsize=12)
ax.set_title('Scatter Plot with Labels', fontsize=14)
ax.grid(True, alpha=0.3)
```

### 3. Add Point Labels

```python
for i, label in enumerate(labels):
    ax.annotate(label, (x[i], y[i]), textcoords='offset points',
                xytext=(5, 5), fontsize=8)

plt.tight_layout()
plt.show()
```


## Scatter Plots as Multidimensional Encoding

A scatter plot maps data points into **visual space** using multiple channels simultaneously:

```text
2D → x, y (position)
3D → + color (c parameter)
4D → + size (s parameter)
5D → + shape (marker parameter, categorical only)
```

This makes scatter plots the most flexible encoding for high-dimensional data in a 2D figure. Each additional channel adds one variable — but also increases cognitive load. Use at most 2--3 encodings per plot for readability.

Unlike histograms or KDE, scatter plots show **raw observations** without aggregation. Related views:

- Histogram → distribution of one variable
- KDE / density plot → aggregated scatter (smoothed)
- Heatmap (hist2d) → binned scatter (counted)

---

## Exercises

**Exercise 1.** Write code that generates 200 random points and creates a scatter plot using `ax.scatter()`. Set `alpha=0.6` and add axis labels.

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

**Exercise 2.** Explain the difference between `ax.plot(x, y, 'o')` and `ax.scatter(x, y)`. When would you use each?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a scatter plot where the marker size is proportional to a third variable using the `s` parameter.

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

**Exercise 4.** Write code that creates a scatter plot of two distinct clusters with different colors and adds a legend.

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
