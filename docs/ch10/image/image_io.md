# Image I/O

This document covers reading, loading, and displaying images in matplotlib.

!!! tip "Mental Model"
    Image I/O is about converting between file formats and NumPy arrays. `plt.imread()` reads a file into an array, PIL/Pillow reads from URLs or does format conversion, and `ax.imshow()` displays the array. Once an image is a NumPy array, you can inspect its shape (height, width, channels) and manipulate it with standard array operations.

!!! warning "dtype Pitfalls"
    Image arrays come in two common dtypes that behave very differently:

    - `uint8` — values 0–255 (most file formats, PIL). This is what `imshow()` expects for RGB images.
    - `float64` or `float32` — values 0.0–1.0 (after normalization, or from `plt.imread` on PNGs). `imshow()` clips float values to [0, 1].

    Mixing these silently produces wrong results: multiplying a `uint8` image by 2.0 converts to float but gives values up to 510, which `imshow` clips to 1.0 (nearly black). Always check `img.dtype` after loading and normalize explicitly when needed: `img_float = img.astype(np.float32) / 255.0`. For large images, be mindful of memory: a 4000x3000 RGB `float64` image uses ~288 MB versus ~36 MB for `uint8`.

## Reading Web Images

Load images from URLs directly into NumPy arrays for visualization and manipulation.

### PIL and urllib Approach

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
    print(f"{type(img) = }, {img.shape = }, {img.dtype = }")

    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
```

### Understanding Image Arrays

```python
import numpy as np
import PIL
import urllib

url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

print(f"Shape: {img.shape}")      # (height, width, channels)
print(f"Dtype: {img.dtype}")      # uint8 (0-255)
print(f"Min value: {img.min()}")  # 0
print(f"Max value: {img.max()}")  # 255
```

### Channel Interpretation

| Channels | Format | Description |
|----------|--------|-------------|
| 1 | Grayscale | Single intensity value |
| 3 | RGB | Red, Green, Blue |
| 4 | RGBA | RGB + Alpha (transparency) |

### Alternative: requests Library

```python
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import requests
from io import BytesIO

def load_image_requests(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return np.array(img)

url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
img = load_image_requests(url)

fig, ax = plt.subplots()
ax.imshow(img)
ax.axis('off')
plt.show()
```

### Error Handling

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib
from urllib.error import URLError, HTTPError

def safe_load_image(url):
    try:
        img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
        return img
    except HTTPError as e:
        print(f"HTTP Error: {e.code}")
        return None
    except URLError as e:
        print(f"URL Error: {e.reason}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
img = safe_load_image(url)

if img is not None:
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.axis('off')
    plt.show()
```

---

## imread - Reading Local Images

The `plt.imread()` function reads image files from disk into NumPy arrays.

### Basic Usage

```python
import matplotlib.pyplot as plt

def main():
    img = plt.imread('img/mewtwo.jpg')
    
    fig, ax = plt.subplots()
    ax.imshow(img)
    plt.show()

if __name__ == "__main__":
    main()
```

### Supported Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PNG | .png | Lossless, supports transparency |
| JPEG | .jpg, .jpeg | Lossy compression |
| GIF | .gif | Limited colors |
| TIFF | .tiff, .tif | High quality |
| BMP | .bmp | Uncompressed |

### Format-Specific Behavior

```python
import matplotlib.pyplot as plt

# PNG: Returns float32 (0.0-1.0) or uint8 (0-255)
img_png = plt.imread('image.png')
print(f"PNG dtype: {img_png.dtype}")

# JPEG: Returns uint8 (0-255)
img_jpg = plt.imread('image.jpg')
print(f"JPEG dtype: {img_jpg.dtype}")
```

### Batch Loading from Directory

```python
import matplotlib.pyplot as plt
import os
import glob

def load_images_from_directory(directory, extension='*.jpg'):
    images = []
    filenames = []
    for filepath in glob.glob(os.path.join(directory, extension)):
        img = plt.imread(filepath)
        images.append(img)
        filenames.append(os.path.basename(filepath))
    return images, filenames

images, names = load_images_from_directory('img/')
print(f"Loaded {len(images)} images")
```

### Comparison: imread vs PIL

```python
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

filepath = 'img/mewtwo.jpg'

# Using plt.imread
img_mpl = plt.imread(filepath)

# Using PIL
img_pil = np.array(Image.open(filepath))

print(f"plt.imread shape: {img_mpl.shape}, dtype: {img_mpl.dtype}")
print(f"PIL shape: {img_pil.shape}, dtype: {img_pil.dtype}")
```

---

## imshow - Displaying Images

The `ax.imshow()` method displays image data on an Axes.

### Basic Usage

```python
import matplotlib.pyplot as plt
import numpy as np

img = np.random.rand(100, 100, 3)

fig, ax = plt.subplots()
ax.imshow(img)
plt.show()
```

### Image Data Types

```python
import matplotlib.pyplot as plt
import numpy as np

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Float array (0-1)
img_float = np.random.rand(50, 50, 3)
axes[0].imshow(img_float)
axes[0].set_title('Float [0, 1]')

# Uint8 array (0-255)
img_uint8 = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
axes[1].imshow(img_uint8)
axes[1].set_title('Uint8 [0, 255]')

# Grayscale (2D array)
img_gray = np.random.rand(50, 50)
axes[2].imshow(img_gray, cmap='gray')
axes[2].set_title('Grayscale')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `X` | Image data (array-like) | Required |
| `cmap` | Colormap | None |
| `aspect` | Aspect ratio | 'equal' |
| `interpolation` | Interpolation method | 'antialiased' |
| `alpha` | Transparency | None |
| `vmin`, `vmax` | Value range | Data min/max |
| `origin` | Origin position | 'upper' |

### Aspect Ratio

```python
import matplotlib.pyplot as plt
import numpy as np

img = np.random.rand(50, 100)

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(img, aspect='equal')
axes[0].set_title("aspect='equal'")

axes[1].imshow(img, aspect='auto')
axes[1].set_title("aspect='auto'")

axes[2].imshow(img, aspect=0.5)
axes[2].set_title("aspect=0.5")

plt.tight_layout()
plt.show()
```

### Interpolation Methods

```python
import matplotlib.pyplot as plt
import numpy as np

img = np.random.rand(10, 10)
methods = ['nearest', 'bilinear', 'bicubic', 'spline16']

fig, axes = plt.subplots(1, 4, figsize=(12, 3))

for ax, method in zip(axes, methods):
    ax.imshow(img, interpolation=method, cmap='viridis')
    ax.set_title(method)
    ax.axis('off')

plt.tight_layout()
plt.show()
```

### Origin Position

```python
import matplotlib.pyplot as plt
import numpy as np

img = np.arange(25).reshape(5, 5)

fig, axes = plt.subplots(1, 2, figsize=(8, 4))

axes[0].imshow(img, origin='upper')
axes[0].set_title("origin='upper' (default)")

axes[1].imshow(img, origin='lower')
axes[1].set_title("origin='lower'")

plt.tight_layout()
plt.show()
```

### Adding Colorbar

```python
import matplotlib.pyplot as plt
import numpy as np

img = np.random.rand(50, 50)

fig, ax = plt.subplots()
im = ax.imshow(img, cmap='viridis')
fig.colorbar(im, ax=ax)
plt.show()
```

---

## Deep Learning Examples

### FashionMNIST (PyTorch)

```python
import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

def main():
    training_data = datasets.FashionMNIST(
        root="data", train=True, download=True, transform=ToTensor()
    )

    labels_map = {
        0: "T-Shirt", 1: "Trouser", 2: "Pullover", 3: "Dress", 4: "Coat",
        5: "Sandal", 6: "Shirt", 7: "Sneaker", 8: "Bag", 9: "Ankle Boot",
    }

    train_dataloader = DataLoader(training_data, batch_size=64, shuffle=True)

    fig, axes = plt.subplots(1, 10, figsize=(15, 5))

    for imgs, labels in train_dataloader:
        for i, (img, label) in enumerate(zip(imgs, labels)):
            axes[i].imshow(img.squeeze(), cmap='binary')
            axes[i].set_title(labels_map[label.item()])
            axes[i].axis('off')
            if i == 9:
                break
        break

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### MNIST (TensorFlow)

```python
import matplotlib.pyplot as plt
import tensorflow as tf

def main():
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    fig, axes = plt.subplots(nrows=2, ncols=10, figsize=(10, 2))
    for i in range(2):
        for j in range(10):
            axes[i, j].imshow(x_train[i*10+j], cmap=plt.cm.gray)
            axes[i, j].set_title(f'Label {y_train[i*10+j]}')
            axes[i, j].axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### PyTorch Tensor Handling

```python
import matplotlib.pyplot as plt
import torch

# PyTorch: (C, H, W) -> (H, W, C)
tensor = torch.rand(3, 64, 64)
img = tensor.permute(1, 2, 0).numpy()

fig, ax = plt.subplots()
ax.imshow(img)
ax.axis('off')
plt.show()
```

---

## Practical Example: Image Gallery

```python
import matplotlib.pyplot as plt
import os

def create_image_gallery(image_dir, ncols=4):
    files = [f for f in os.listdir(image_dir) 
             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    nrows = (len(files) + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(3*ncols, 3*nrows))
    axes = axes.flatten() if nrows > 1 else [axes] if ncols == 1 else axes
    
    for ax, filename in zip(axes, files):
        img = plt.imread(os.path.join(image_dir, filename))
        ax.imshow(img)
        ax.set_title(filename, fontsize=8)
        ax.axis('off')
    
    # Hide empty subplots
    for ax in axes[len(files):]:
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

create_image_gallery('img/')
```


---

## Exercises

**Exercise 1.** Write code that creates a simple plot, saves it with `fig.savefig('test.png')`, then reads and displays the saved image using `plt.imread()` and `ax.imshow()`.

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

**Exercise 2.** Explain what `plt.imread()` returns for a PNG file. What data type and shape does the array have for an RGB image?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that creates a NumPy array representing a grayscale image (e.g., a gradient) and saves it using `plt.imsave()`. Then read it back and display it.

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

**Exercise 4.** Create code that reads an image, converts it to grayscale by averaging the RGB channels, and displays the original alongside the grayscale version in a 1x2 subplot.

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
