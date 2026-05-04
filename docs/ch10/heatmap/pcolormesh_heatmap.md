# Heatmaps with pcolormesh

The `ax.pcolormesh()` method creates pseudocolor plots with quadrilateral cells, offering more flexibility than `imshow` for non-uniform grids and coordinate-based data.

!!! tip "Mental Model"
    `pcolormesh()` is like `imshow()` but with explicit coordinates. Instead of assuming a uniform pixel grid, you supply X and Y coordinate arrays that define each cell's corners. This makes it ideal for data on non-uniform grids, curvilinear coordinates, or when axes must reflect real-world units.

    The key distinction: **`imshow` = image representation** (uniform pixel grid,
    implicit coordinates), **`pcolormesh` = geometric representation** (explicit
    coordinates, preserves the domain's geometry). Use `imshow` for matrices and
    images; use `pcolormesh` when the x/y axes represent real-world quantities
    with potentially non-uniform spacing.

## Basic pcolormesh

Create a heatmap using pcolormesh.

### 1. Simple Usage

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.rand(10, 10)

fig, ax = plt.subplots()
pc = ax.pcolormesh(data)
plt.colorbar(pc)
plt.show()
```

### 2. With Coordinates

```python
x = np.arange(11)  # 11 edges for 10 cells
y = np.arange(11)
X, Y = np.meshgrid(x, y)

fig, ax = plt.subplots()
pc = ax.pcolormesh(X, Y, data)
plt.colorbar(pc)
plt.show()
```

### 3. Cell Centers vs Edges

```python
# pcolormesh uses edges: N+1 coordinates for N cells
# Data shape (10, 10) needs X, Y shape (11, 11)
```

## imshow vs pcolormesh

Understanding when to use each method.

### 1. Key Differences

```python
# imshow:
#   - Pixels are uniformly sized
#   - Origin at top-left by default
#   - Aspect ratio preserved
#   - Faster for large uniform grids

# pcolormesh:
#   - Cells can be non-uniform
#   - Origin at bottom-left by default
#   - Aspect ratio follows data coordinates
#   - Supports curvilinear grids
```

### 2. Origin Behavior

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

ax1.imshow(data)
ax1.set_title('imshow (origin=upper)')

ax2.pcolormesh(data)
ax2.set_title('pcolormesh (origin=lower)')

plt.tight_layout()
plt.show()
```

### 3. Matching Origins

```python
# Make imshow match pcolormesh
ax.imshow(data, origin='lower')

# Or flip data for pcolormesh to match imshow
ax.pcolormesh(data[::-1])
```

## Non-Uniform Grids

pcolormesh excels with irregularly spaced data.

### 1. Logarithmic Spacing

```python
x = np.logspace(0, 2, 11)  # 1 to 100, log-spaced
y = np.linspace(0, 10, 11)
X, Y = np.meshgrid(x, y)

data = np.random.rand(10, 10)

fig, ax = plt.subplots()
pc = ax.pcolormesh(X, Y, data)
ax.set_xscale('log')
plt.colorbar(pc)
plt.show()
```

### 2. Variable Cell Sizes

```python
x = np.array([0, 1, 2, 4, 8, 16])  # Non-uniform spacing
y = np.array([0, 1, 3, 6, 10])
X, Y = np.meshgrid(x, y)

data = np.random.rand(4, 5)

fig, ax = plt.subplots()
pc = ax.pcolormesh(X, Y, data)
plt.colorbar(pc)
plt.show()
```

### 3. Time Series Data

```python
import datetime

dates = [datetime.datetime(2024, 1, i) for i in range(1, 12)]
hours = np.arange(25)
data = np.random.rand(24, 10)

fig, ax = plt.subplots(figsize=(10, 5))
pc = ax.pcolormesh(dates, hours, data)
ax.set_ylabel('Hour')
plt.colorbar(pc)
plt.show()
```

## Shading Options

The `shading` keyword controls cell rendering.

!!! info "Shading Explained"
    **`flat`** — each cell is a single solid color. Coordinates define cell **edges**, so X and Y must have one more element per dimension than the data array (e.g., data is 10×10, coordinates are 11×11).

    **`auto`** — matplotlib infers whether coordinates are edges or centers and adjusts automatically. This is the safest default when you are unsure about shape matching.

    **`gouraud`** — colors are interpolated smoothly between vertices, producing gradient fills. Coordinates must be the **same shape** as the data (one value per data point, not per edge).

    Most shape-mismatch errors come from confusing edge coordinates (`flat`) with center coordinates (`gouraud`). Use `shading='auto'` until you need explicit control.

### 1. Flat Shading (Default)

```python
ax.pcolormesh(X, Y, data, shading='flat')
# Requires X, Y one larger than data in each dimension
```

### 2. Auto Shading

```python
# Automatically handles coordinate/data size mismatch
ax.pcolormesh(X, Y, data, shading='auto')
```

### 3. Gouraud Shading

```python
# Interpolated colors at vertices
# Requires X, Y same shape as data
x = np.arange(10)
y = np.arange(10)
X, Y = np.meshgrid(x, y)

ax.pcolormesh(X, Y, data, shading='gouraud')
```

## Edge Colors

Add grid lines between cells.

### 1. Black Edges

```python
fig, ax = plt.subplots()
pc = ax.pcolormesh(data, edgecolors='black', linewidth=0.5)
plt.colorbar(pc)
plt.show()
```

### 2. White Edges

```python
pc = ax.pcolormesh(data, edgecolors='white', linewidth=1)
```

### 3. Face Color Only

```python
pc = ax.pcolormesh(data, edgecolors='face')  # Edges match cell color
```

## Colormap and Range

Control color mapping identical to imshow.

### 1. Colormap Selection

```python
pc = ax.pcolormesh(data, cmap='viridis')
pc = ax.pcolormesh(data, cmap='coolwarm')
```

### 2. Value Range

```python
pc = ax.pcolormesh(data, vmin=0, vmax=1)
```

### 3. Centered Diverging

```python
data_centered = np.random.randn(10, 10)
max_abs = np.abs(data_centered).max()
pc = ax.pcolormesh(data_centered, cmap='RdBu', vmin=-max_abs, vmax=max_abs)
```

## Masked Data

Handle missing or invalid values.

### 1. Create Masked Array

```python
data = np.random.rand(10, 10)
mask = data < 0.2
masked_data = np.ma.masked_array(data, mask)

fig, ax = plt.subplots()
pc = ax.pcolormesh(masked_data)
plt.colorbar(pc)
plt.show()
```

### 2. Set Bad Color

```python
cmap = plt.cm.viridis.copy()
cmap.set_bad('gray')

pc = ax.pcolormesh(masked_data, cmap=cmap)
```

### 3. NaN Values

```python
data_with_nan = data.copy()
data_with_nan[data < 0.2] = np.nan

pc = ax.pcolormesh(data_with_nan, cmap=cmap)
```

## Practical Example

Create a complete heatmap with pcolormesh.

### 1. Generate Structured Data

```python
x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)
```

### 2. Create Visualization

```python
fig, ax = plt.subplots(figsize=(8, 6))

pc = ax.pcolormesh(X, Y, Z, cmap='RdBu', shading='auto')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('sin(x) × cos(y)')
ax.set_aspect('equal')

plt.colorbar(pc, label='Value')
plt.tight_layout()
plt.show()
```

### 3. Add Contour Overlay

```python
fig, ax = plt.subplots(figsize=(8, 6))

pc = ax.pcolormesh(X, Y, Z, cmap='RdBu', shading='auto', alpha=0.8)
ax.contour(X, Y, Z, colors='black', linewidths=0.5, levels=10)

plt.colorbar(pc)
plt.show()
```


---

## Exercises

**Exercise 1.** Write code that creates a 2D array and displays it using `ax.pcolormesh()`. Add a colorbar and labels.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.linspace(0, 5, 30)
    y = np.linspace(0, 3, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)

    fig, ax = plt.subplots(figsize=(8, 5))
    pc = ax.pcolormesh(X, Y, Z, cmap='RdBu', shading='auto')
    fig.colorbar(pc, ax=ax, label='Value')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('pcolormesh Heatmap')
    plt.show()
    ```

---

**Exercise 2.** Explain the key difference between `ax.imshow()` and `ax.pcolormesh()`. When would you prefer `pcolormesh`?

??? success "Solution to Exercise 2"
    `ax.imshow()` assumes a regular (equally-spaced) grid and treats the data as an image. `ax.pcolormesh()` accepts explicit x and y coordinate arrays, so it can handle **non-uniform** (irregularly spaced) grids.

    Prefer `pcolormesh` when your data is on an irregular grid, when you need precise control over cell edges, or when you are plotting geospatial/scientific data with non-uniform coordinates. Use `imshow` for simple, regularly-spaced data or actual images.

---

**Exercise 3.** Write code using `pcolormesh` with non-uniform grid spacing (e.g., logarithmically spaced x-coordinates).

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.logspace(0, 2, 30)  # Non-uniform: 1 to 100
    y = np.linspace(0, 5, 20)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.log(X)) * np.cos(Y)

    fig, ax = plt.subplots(figsize=(8, 5))
    pc = ax.pcolormesh(X, Y, Z, cmap='viridis', shading='auto')
    fig.colorbar(pc, ax=ax, label='Value')
    ax.set_xlabel('X (log scale)')
    ax.set_ylabel('Y')
    ax.set_title('pcolormesh with Non-Uniform Grid')
    plt.show()
    ```

---

**Exercise 4.** Create a side-by-side comparison of the same data displayed with `imshow` and `pcolormesh`, showing that `pcolormesh` handles non-uniform grids correctly.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    x = np.logspace(0, 1, 20)
    y = np.linspace(0, 3, 15)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.imshow(Z, cmap='RdBu', aspect='auto', origin='lower')
    ax1.set_title('imshow (ignores non-uniform grid)')

    pc = ax2.pcolormesh(X, Y, Z, cmap='RdBu', shading='auto')
    fig.colorbar(pc, ax=ax2)
    ax2.set_title('pcolormesh (respects non-uniform grid)')

    plt.tight_layout()
    plt.show()
    ```
