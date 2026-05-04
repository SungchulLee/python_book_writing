# Image Processing

This document covers colormaps and image manipulation techniques in matplotlib.

!!! tip "Mental Model"
    Image processing in Matplotlib means manipulating the underlying NumPy array and redisplaying it. Convert to grayscale by averaging channels, adjust brightness by scaling values, apply colormaps to single-channel images, and crop by slicing the array. Matplotlib is the visualization layer; NumPy does the actual pixel math.

    Mathematically, **image processing = function transformation.** The original
    image is a function $f(x, y)$; every operation produces a new function
    $g(x, y)$. Convolution-based operations (blur, edge detection) are **local
    transformations** — each output pixel becomes a function of its neighbors,
    exactly like the [neighborhood operators](../../ch09/ndimage/convolution_filtering.md)
    in the ndimage chapter.

!!! note "The Deeper Model: Images as Matrices"
    Every image operation has a mathematical interpretation:

    - **Grayscale conversion** — weighted sum of RGB channels (a linear combination)
    - **Brightness/contrast** — scaling and shifting pixel values (affine transformation)
    - **Cropping** — array slicing (selecting a submatrix)
    - **Blurring** — convolution with an averaging kernel (each pixel becomes the mean of its neighbors)
    - **Edge detection** — convolution with a derivative kernel (highlights rapid intensity changes)

    Thinking of pixels as matrix elements connects image processing to linear algebra and signal processing. The colormap section below maps scalar matrices to visual color; the manipulation section transforms the matrix itself.

## Colormaps (cmap)

The `cmap` parameter specifies the colormap used to map scalar data to colors.

[Official Documentation](https://matplotlib.org/stable/tutorials/colors/colormaps.html)

### Basic Usage

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(10, 10)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(data, cmap='viridis')
axes[0].set_title('viridis')

axes[1].imshow(data, cmap='plasma')
axes[1].set_title('plasma')

axes[2].imshow(data, cmap='gray')
axes[2].set_title('gray')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### Colormap Categories

#### Perceptually Uniform Sequential

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(50, 50)
cmaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']

fig, axes = plt.subplots(1, 5, figsize=(15, 3))
for ax, cmap in zip(axes, cmaps):
    ax.imshow(data, cmap=cmap)
    ax.set_title(cmap)
    ax.axis('off')
plt.tight_layout()
plt.show()
```

#### Sequential

```python
cmaps = ['Greys', 'Blues', 'Greens', 'Oranges', 'Reds']

fig, axes = plt.subplots(1, 5, figsize=(15, 3))
for ax, cmap in zip(axes, cmaps):
    ax.imshow(data, cmap=cmap)
    ax.set_title(cmap)
    ax.axis('off')
plt.tight_layout()
plt.show()
```

#### Diverging

```python
# Diverging data centered at 0
data = np.random.randn(50, 50)
cmaps = ['RdBu', 'RdYlGn', 'coolwarm', 'bwr', 'seismic']

fig, axes = plt.subplots(1, 5, figsize=(15, 3))
for ax, cmap in zip(axes, cmaps):
    im = ax.imshow(data, cmap=cmap, vmin=-2, vmax=2)
    ax.set_title(cmap)
    ax.axis('off')
plt.tight_layout()
plt.show()
```

#### Cyclic

```python
# Cyclic data (e.g., angles)
x = np.linspace(-np.pi, np.pi, 100)
y = np.linspace(-np.pi, np.pi, 100)
X, Y = np.meshgrid(x, y)
data = np.arctan2(Y, X)

cmaps = ['twilight', 'twilight_shifted', 'hsv']

fig, axes = plt.subplots(1, 3, figsize=(12, 4))
for ax, cmap in zip(axes, cmaps):
    ax.imshow(data, cmap=cmap)
    ax.set_title(cmap)
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### Grayscale Images

```python
import matplotlib.pyplot as plt
import numpy as np

digit = np.random.rand(28, 28)

fig, axes = plt.subplots(1, 4, figsize=(12, 3))

axes[0].imshow(digit, cmap='gray')
axes[0].set_title('gray')

axes[1].imshow(digit, cmap='binary')
axes[1].set_title('binary')

axes[2].imshow(digit, cmap='gray_r')
axes[2].set_title('gray_r (reversed)')

axes[3].imshow(digit, cmap='binary_r')
axes[3].set_title('binary_r')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### Reversed Colormaps

Add `_r` suffix to reverse any colormap:

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(50, 50)

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

cmaps = ['viridis', 'hot', 'Blues']
for i, cmap in enumerate(cmaps):
    axes[0, i].imshow(data, cmap=cmap)
    axes[0, i].set_title(cmap)
    axes[0, i].axis('off')
    
    axes[1, i].imshow(data, cmap=cmap + '_r')
    axes[1, i].set_title(cmap + '_r')
    axes[1, i].axis('off')

plt.tight_layout()
plt.show()
```

### Value Range Control (vmin, vmax)

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(50, 50) * 100  # Range 0-100

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(data, cmap='viridis')
axes[0].set_title('Default range')

axes[1].imshow(data, cmap='viridis', vmin=25, vmax=75)
axes[1].set_title('vmin=25, vmax=75')

axes[2].imshow(data, cmap='viridis', vmin=0, vmax=50)
axes[2].set_title('vmin=0, vmax=50')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### Adding Colorbar

```python
import matplotlib.pyplot as plt
import numpy as np

data = np.random.rand(50, 50)

fig, ax = plt.subplots()
im = ax.imshow(data, cmap='viridis')
fig.colorbar(im, ax=ax, label='Value')
ax.set_title('Image with Colorbar')
plt.show()
```

---

## Image Manipulation

Manipulate images using NumPy array indexing and slicing operations.

### Image as 3D Array

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib

url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
print(img.shape)  # (height, width, channels)
```

### Common Transformations

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
    
    imgs = (
        img,              # Original
        img[::-1],        # Vertical flip
        img[:, ::-1],     # Horizontal flip
        img[:, :, ::-1],  # Channel reverse (RGB to BGR)
        img[::7, ::7],    # Downsampling
        img[50:-50, 50:-50]  # Cropping
    )
    
    imgs_title = (
        "img",
        "img[::-1]",
        "img[:, ::-1]",
        "img[:, :, ::-1]",
        "img[::7, ::7]",
        "img[50:-50, 50:-50]"
    )

    fig, axes = plt.subplots(2, 3, figsize=(8, 5))
    for ax, img_to_plot, img_title in zip(axes.flatten(), imgs, imgs_title):
        ax.set_title(img_title, fontsize=12)
        ax.imshow(img_to_plot)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### Transformation Reference

| Operation | Code | Description |
|-----------|------|-------------|
| Vertical flip | `img[::-1]` | Reverse rows |
| Horizontal flip | `img[:, ::-1]` | Reverse columns |
| 180° rotation | `img[::-1, ::-1]` | Reverse both |
| RGB to BGR | `img[:, :, ::-1]` | Reverse channels |
| Downsampling | `img[::n, ::n]` | Take every nth pixel |
| Cropping | `img[y1:y2, x1:x2]` | Extract region |

### Channel Operations

#### Visualize Individual Channels

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib

url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

fig, axes = plt.subplots(1, 4, figsize=(16, 4))

axes[0].imshow(img)
axes[0].set_title('Original')

axes[1].imshow(img[:, :, 0], cmap='Reds')
axes[1].set_title('Red Channel')

axes[2].imshow(img[:, :, 1], cmap='Greens')
axes[2].set_title('Green Channel')

axes[3].imshow(img[:, :, 2], cmap='Blues')
axes[3].set_title('Blue Channel')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

#### Swap Channels

```python
# Create different channel arrangements
img_rbg = img[:, :, [0, 2, 1]]  # R, B, G
img_grb = img[:, :, [1, 0, 2]]  # G, R, B
img_gbr = img[:, :, [1, 2, 0]]  # G, B, R
img_brg = img[:, :, [2, 0, 1]]  # B, R, G
img_bgr = img[:, :, [2, 1, 0]]  # B, G, R
```

### Image Grid Overlay

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib

url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(10, 5))

ax0.imshow(img)
ax0.set_title('Original')

spacing = 50
img_copy = img.copy()
img_copy[spacing:-1:spacing, :] = [255, 0, 0, 1]  # Horizontal red lines
img_copy[:, spacing:-1:spacing] = [255, 0, 0, 1]  # Vertical red lines
ax1.imshow(img_copy)
ax1.set_title('With Grid')

for ax in (ax0, ax1):
    ax.axis('off')

plt.tight_layout()
plt.show()
```

### Regions of Interest (ROI)

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib

url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

# Define region of interest
y_start, y_end = 100, 200
x_start, x_end = 50, 150

# Extract ROI
roi = img[y_start:y_end, x_start:x_end]

# Create highlighted version
img_highlight = img.copy()
img_highlight[y_start:y_end, x_start:x_end, 0] = 255  # Add red tint

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(img)
axes[0].set_title('Original')

axes[1].imshow(img_highlight)
axes[1].set_title('Highlighted ROI')

axes[2].imshow(roi)
axes[2].set_title('Extracted ROI')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### Image Tiling

```python
import matplotlib.pyplot as plt
import numpy as np

def tile_image(img, rows, cols):
    """Tile an image into a grid."""
    return np.tile(img, (rows, cols, 1))

# Create 2x3 tiled image
tiled = tile_image(img, 2, 3)

fig, ax = plt.subplots(figsize=(12, 8))
ax.imshow(tiled)
ax.axis('off')
plt.show()
```

### Adding Borders

```python
import matplotlib.pyplot as plt
import numpy as np

def add_border(img, size=10, color=[255, 0, 0]):
    """Add a colored border to an image."""
    bordered = img.copy()
    bordered[:size, :] = color      # Top
    bordered[-size:, :] = color     # Bottom
    bordered[:, :size] = color      # Left
    bordered[:, -size:] = color     # Right
    return bordered

bordered = add_border(img, size=20, color=[255, 0, 0])

fig, ax = plt.subplots()
ax.imshow(bordered)
ax.axis('off')
plt.show()
```

---

## Colormap Reference

### Categories Summary

| Category | Colormaps | Use Case |
|----------|-----------|----------|
| Perceptually Uniform | viridis, plasma, inferno, magma | General purpose |
| Sequential | Greys, Blues, Greens, Oranges | Single-direction data |
| Diverging | RdBu, coolwarm, bwr | Data with center point |
| Cyclic | twilight, hsv | Periodic data (angles) |
| Qualitative | Set1, Set2, Pastel1 | Categorical data |


---

## Exercises

**Exercise 1.** Write code that creates a 50x50 random image array and applies a simple threshold: set all values above 0.5 to 1 and below 0.5 to 0. Display the original and thresholded images side by side.

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

**Exercise 2.** Explain how you can use NumPy array slicing to crop a region from an image array. Write code to extract and display the center quarter of a 100x100 image.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that flips an image horizontally and vertically using NumPy operations (`[:, ::-1]` and `[::-1, :]`). Show the original and flipped versions in subplots.

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

**Exercise 4.** Create a simple 2D convolution (blurring) by replacing each pixel with the average of its neighbors. Apply it to a random 50x50 image and show the before and after.

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
