# Heatmaps with imshow

The `ax.imshow()` method displays 2D data as a color-coded image, ideal for matrices, correlation tables, and gridded data.

!!! tip "Mental Model"
    `imshow()` treats a 2D array as a grid of pixels, coloring each cell by its value. Row 0 is at the top (image convention), and cells are equally sized. It is the simplest way to visualize matrices and correlation tables. For non-uniform grids or coordinate-based data, use `pcolormesh()` instead.

!!! warning "Coordinate Convention"
    `imshow()` uses **image coordinates** by default: row 0 is at the **top** (`origin='upper'`). This matches image/pixel convention but is upside-down relative to mathematical plots. Set `origin='lower'` when your y-axis represents a quantity that increases upward (e.g., frequency, temperature). Forgetting this is one of the most common heatmap bugs.

    For data on non-uniform or real-valued grids, use [`pcolormesh()`](pcolormesh_heatmap.md) instead — it accepts explicit coordinate arrays. For colormap guidance, see [Colormap Selection](colormap_selection.md).

## Basic Heatmap

Create a simple heatmap from a 2D array.

### 1. Import and Setup

```python
import matplotlib.pyplot as plt
import numpy as np
```

### 2. Create 2D Data

```python
np.random.seed(42)
data = np.random.rand(10, 10)
```

### 3. Display with imshow

```python
fig, ax = plt.subplots()
im = ax.imshow(data)
plt.colorbar(im)
plt.show()
```

## Colormap Selection

The `cmap` keyword controls the color scheme.

### 1. Sequential Colormaps

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

for ax, cmap in zip(axes, ['viridis', 'plasma', 'Blues']):
    im = ax.imshow(data, cmap=cmap)
    ax.set_title(cmap)
    plt.colorbar(im, ax=ax)

plt.tight_layout()
plt.show()
```

### 2. Diverging Colormaps

```python
data_centered = np.random.randn(10, 10)

fig, ax = plt.subplots()
im = ax.imshow(data_centered, cmap='RdBu', vmin=-2, vmax=2)
plt.colorbar(im)
plt.show()
```

### 3. Common Colormaps

```python
# Sequential: 'viridis', 'plasma', 'inferno', 'magma', 'Blues', 'Greens'
# Diverging: 'RdBu', 'coolwarm', 'seismic', 'PiYG'
# Qualitative: 'Set1', 'Set2', 'tab10', 'tab20'
```

## Value Range

Control the mapping between data values and colors.

### 1. Auto Range (Default)

```python
ax.imshow(data)  # Maps min to bottom, max to top of colormap
```

### 2. Fixed Range

```python
ax.imshow(data, vmin=0, vmax=1)
```

### 3. Centered at Zero

```python
max_abs = np.abs(data_centered).max()
ax.imshow(data_centered, cmap='RdBu', vmin=-max_abs, vmax=max_abs)
```

## Aspect Ratio

The `aspect` keyword controls pixel shape.

### 1. Equal Aspect (Default)

```python
ax.imshow(data, aspect='equal')  # Square pixels
```

### 2. Auto Aspect

```python
ax.imshow(data, aspect='auto')  # Fills axes, may stretch
```

### 3. Numeric Aspect

```python
ax.imshow(data, aspect=2)  # Height = 2 × width per pixel
```

## Axis Labels and Ticks

Customize tick positions and labels for matrix visualization.

### 1. Set Tick Positions

```python
fig, ax = plt.subplots()
im = ax.imshow(data)

ax.set_xticks(np.arange(10))
ax.set_yticks(np.arange(10))
plt.show()
```

### 2. Custom Labels

```python
row_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
col_labels = [f'Col {i}' for i in range(10)]

ax.set_xticks(np.arange(10))
ax.set_yticks(np.arange(10))
ax.set_xticklabels(col_labels, rotation=45, ha='right')
ax.set_yticklabels(row_labels)
```

### 3. Move X Labels to Top

```python
ax.xaxis.set_ticks_position('top')
ax.xaxis.set_label_position('top')
```

## Annotating Cells

Add text values to each cell.

!!! warning "Scalability"
    The nested-loop annotation pattern below works well for small matrices (up to ~20×20). For larger matrices, annotations become unreadable and the loop becomes slow. For large data, rely on the colorbar and skip cell labels.

### 1. Basic Annotation

```python
fig, ax = plt.subplots()
im = ax.imshow(data, cmap='Blues')

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        ax.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center', fontsize=8)

plt.show()
```

### 2. Contrast Text Color

```python
threshold = data.max() / 2

for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        color = 'white' if data[i, j] > threshold else 'black'
        ax.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center', 
                color=color, fontsize=8)
```

### 3. Integer Annotation

```python
int_data = np.random.randint(0, 100, (5, 5))

for i in range(int_data.shape[0]):
    for j in range(int_data.shape[1]):
        ax.text(j, i, int_data[i, j], ha='center', va='center')
```

## Correlation Matrix

A common use case for imshow heatmaps.

### 1. Compute Correlation

```python
np.random.seed(42)
df_data = np.random.randn(100, 5)
corr_matrix = np.corrcoef(df_data.T)
```

### 2. Display Correlation Heatmap

```python
fig, ax = plt.subplots(figsize=(6, 5))

im = ax.imshow(corr_matrix, cmap='RdBu', vmin=-1, vmax=1)

labels = ['Var A', 'Var B', 'Var C', 'Var D', 'Var E']
ax.set_xticks(np.arange(5))
ax.set_yticks(np.arange(5))
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_yticklabels(labels)

for i in range(5):
    for j in range(5):
        color = 'white' if abs(corr_matrix[i, j]) > 0.5 else 'black'
        ax.text(j, i, f'{corr_matrix[i, j]:.2f}', ha='center', va='center', color=color)

plt.colorbar(im, label='Correlation')
plt.tight_layout()
plt.show()
```

### 3. Mask Upper Triangle

```python
mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
masked_corr = np.ma.masked_array(corr_matrix, mask)

ax.imshow(masked_corr, cmap='RdBu', vmin=-1, vmax=1)
```

## Interpolation

Control how pixel boundaries are rendered.

### 1. No Interpolation (Default for Small Data)

```python
ax.imshow(data, interpolation='nearest')
```

### 2. Smooth Interpolation

```python
ax.imshow(data, interpolation='bilinear')
```

### 3. Common Options

```python
# 'nearest': Sharp pixel boundaries
# 'bilinear': Smooth linear interpolation
# 'bicubic': Smoother cubic interpolation
# 'gaussian': Gaussian smoothing
```

---

## Runnable Example: `seaborn_matrix_plots.py`

```python
"""
Tutorial 06: Matrix Plots
Heatmaps, cluster maps, correlation matrices
Level: Intermediate
"""
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    sns.set_style("white")
    tips = sns.load_dataset('tips')

    # Correlation heatmap
    plt.figure(figsize=(8, 6))
    numeric_cols = tips.select_dtypes(include=[np.number])
    corr = numeric_cols.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, square=True, linewidths=1)
    plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Pivot table heatmap
    pivot_data = tips.pivot_table(values='tip', index='day', columns='time', aggfunc='mean')
    plt.figure(figsize=(8, 6))
    sns.heatmap(pivot_data, annot=True, fmt='.2f', cmap='YlOrRd')
    plt.title('Average Tip: Day vs Time', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Clustermap - with hierarchical clustering
    plt.figure(figsize=(10, 8))
    sns.clustermap(corr, cmap='coolwarm', center=0, linewidths=1, annot=True)
    plt.show()

    print("Tutorial 06 demonstrates matrix visualizations")
    print("Key functions: heatmap(), clustermap()")
```


!!! info "In Machine Learning"

    Heatmaps are used for **confusion matrices** (predicted vs actual class, with cell values = counts) and **correlation matrices** (feature-to-feature Pearson correlations). Annotating cells with `ax.text()` and choosing a diverging colormap (`'RdBu'` centered at 0 for correlations, sequential for counts) makes these instantly readable.

---

## Exercises

**Exercise 1.** Write code that creates a 5x5 NumPy array of random values and displays it as a heatmap using `ax.imshow()`. Add a colorbar and set the colormap to `'viridis'`.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.rand(5, 5)

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='viridis')
    fig.colorbar(im, ax=ax)
    ax.set_title('5x5 Random Heatmap')
    plt.show()
    ```

---

**Exercise 2.** Explain the role of `origin='lower'` vs `origin='upper'` in `ax.imshow()`. When should you use each?

??? success "Solution to Exercise 2"
    `origin='upper'` (default) places row 0 at the **top** of the image, matching how matrices and digital images are conventionally displayed. `origin='lower'` places row 0 at the **bottom**, matching mathematical coordinate systems where the y-axis increases upward.

    Use `'upper'` for actual image data and matrices. Use `'lower'` for scientific data like KDE, contour-like heatmaps, or any data where the y-axis should increase upward.

---

**Exercise 3.** Write code that creates a heatmap of a 10x10 array and adds text annotations showing the value in each cell using a loop with `ax.text()`.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.rand(10, 10)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(data, cmap='Blues')
    fig.colorbar(im, ax=ax)

    for i in range(10):
        for j in range(10):
            ax.text(j, i, f'{data[i, j]:.2f}', ha='center', va='center', fontsize=7)

    ax.set_title('Annotated Heatmap')
    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 4.** Create a heatmap with a custom `extent` parameter to set meaningful x and y axis ranges instead of pixel indices.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.rand(20, 30)

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(data, cmap='hot', extent=[0, 6, 0, 4], aspect='auto')
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_title('Heatmap with Custom Extent')
    fig.colorbar(im, ax=ax, label='Intensity')
    plt.show()
    ```
