# Image Manipulation

NumPy indexing enables powerful image transformations.

!!! tip "Mental Model"
    An image in NumPy is just a 3D array of shape `(height, width, channels)`. Slicing along the first two axes crops the image; indexing the third axis isolates color channels. Every image operation -- flipping, rotating, channel swapping -- is an array indexing operation in disguise.


## Channel Extraction

Separate RGB and alpha channels using indexing.

### 1. RGBA Channels

```python
import numpy as np
import matplotlib.pyplot as plt
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
    print(f"{img.shape = }")

    fig, axes = plt.subplots(1, 4, figsize=(12, 3))
    for i, title in enumerate(["R Channel", "G Channel", "B Channel", "Alpha"]):
        axes[i].set_title(title, fontsize=15)
        axes[i].imshow(img[:, :, i])
        axes[i].axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Single Channel

Access one channel with `img[:, :, 0]` for red, `1` for green, `2` for blue.


## Basic Transforms

Apply geometric transformations using slicing.

### 1. Flip and Slice

```python
import numpy as np
import matplotlib.pyplot as plt
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
    
    imgs = (img, img[::-1], img[:, ::-1], 
            img[:, :, ::-1], img[::7, ::7], img[50:-50, 50:-50])
    titles = ("Original", "Flip Vertical", "Flip Horizontal",
              "Swap Channels", "Downsample", "Crop")

    fig, axes = plt.subplots(2, 3, figsize=(8, 5))
    for ax, im, title in zip(axes.flat, imgs, titles):
        ax.set_title(title, fontsize=12)
        ax.imshow(im)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Operation Summary

- `img[::-1]` — flip vertically
- `img[:, ::-1]` — flip horizontally
- `img[:, :, ::-1]` — reverse channel order (RGB→BGR)
- `img[::7, ::7]` — downsample by factor of 7
- `img[50:-50, 50:-50]` — crop 50 pixels from each edge


## Grid Overlay

Draw grid lines on an image using slice assignment.

### 1. Manual Grid

```python
import numpy as np
import matplotlib.pyplot as plt
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(6, 4))

    ax0.imshow(img)

    spacing = 50
    img_copy = img.copy()
    img_copy[spacing::spacing, :] = [0, 0, 0, 255]
    img_copy[:, spacing::spacing] = [0, 0, 0, 255]
    ax1.imshow(img_copy)

    for ax in (ax0, ax1):
        ax.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Slice Assignment

`img[::50, :] = color` sets every 50th row to the specified color.


## np.where Function

Conditional element replacement based on a condition.

### 1. Syntax Pattern

$$\begin{array}{cccccccc}
b&=&\text{np.where(}&\text{condition}&,&\text{if\_true}&,&\text{if\_false}&\text{)}
\end{array}$$

### 2. Add Noise Example

```python
import numpy as np
import matplotlib.pyplot as plt
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
    
    img_noisy = img + np.random.randint(-100, 101, size=img.shape)
    img_noisy = np.where(img_noisy >= 0, img_noisy, 0)
    img_noisy = np.where(img_noisy <= 255, img_noisy, 255)

    fig, ax = plt.subplots()
    ax.imshow(img_noisy.astype(np.uint8))
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Clipping Values

Chain `np.where` to clamp values within valid range [0, 255].


## np.transpose

Swap array axes for transposition.

### 1. Image Transpose

```python
import numpy as np
import matplotlib.pyplot as plt
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

    img_T = np.empty((img.shape[1], img.shape[0], 3), dtype=np.uint8)
    img_T[:, :, 0] = img[:, :, 0].T
    img_T[:, :, 1] = img[:, :, 1].T
    img_T[:, :, 2] = img[:, :, 2].T

    fig, ax = plt.subplots()
    ax.imshow(img_T)
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Channel-wise

Transpose each color channel separately to maintain RGB structure.


## np.roll Function

Circular shift of array elements along an axis.

### 1. Roll Example

```python
import numpy as np
import matplotlib.pyplot as plt
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(12, 3))

    ax0.imshow(img)
    ax1.imshow(np.roll(img, 50, axis=0))
    ax2.imshow(np.roll(img, 50, axis=1))

    for ax in (ax0, ax1, ax2):
        ax.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Axis Parameter

`axis=0` rolls vertically; `axis=1` rolls horizontally.

## Key Insight

All image operations reduce to array indexing:

```text
Crop       → slicing (img[y1:y2, x1:x2])
Flip       → reverse slicing (img[::-1])
Channel    → indexing (img[:, :, 0])
Overlay    → mask assignment (img[mask] = color)
```

No special image library is needed for these basic transformations --- they are just NumPy selection operations.

---

## Exercises

**Exercise 1.**
Create a synthetic 100x100x3 RGB image (random uint8 values). Flip it vertically using `img[::-1]` and horizontally using `img[:, ::-1]`. Verify that the vertically flipped image's first row matches the original's last row.

??? success "Solution to Exercise 1"

        import numpy as np

        np.random.seed(42)
        img = np.random.randint(0, 256, size=(100, 100, 3), dtype=np.uint8)
        flipped_v = img[::-1]
        flipped_h = img[:, ::-1]

        print(f"First row of flipped == last row of original: "
              f"{np.array_equal(flipped_v[0], img[-1])}")

---

**Exercise 2.**
Create a 200x200x3 image filled with zeros (black). Using slice assignment, draw a red border 5 pixels wide around the entire image (set the border pixels' red channel to 255). Print the shape and verify the corners are red.

??? success "Solution to Exercise 2"

        import numpy as np

        img = np.zeros((200, 200, 3), dtype=np.uint8)
        # Top and bottom borders
        img[:5, :, 0] = 255
        img[-5:, :, 0] = 255
        # Left and right borders
        img[:, :5, 0] = 255
        img[:, -5:, 0] = 255

        print(f"Shape: {img.shape}")
        print(f"Top-left corner red channel: {img[0, 0, 0]}")  # 255
        print(f"Bottom-right corner red channel: {img[-1, -1, 0]}")  # 255

---

**Exercise 3.**
Create a 64x64x3 random image. Downsample it by a factor of 4 using stride slicing `img[::4, ::4]` to produce a 16x16x3 image. Then crop the center 32x32 region from the original. Print the shapes of all three images.

??? success "Solution to Exercise 3"

        import numpy as np

        img = np.random.randint(0, 256, size=(64, 64, 3), dtype=np.uint8)
        downsampled = img[::4, ::4]
        h, w = img.shape[:2]
        cropped = img[h//4:3*h//4, w//4:3*w//4]

        print(f"Original: {img.shape}")        # (64, 64, 3)
        print(f"Downsampled: {downsampled.shape}") # (16, 16, 3)
        print(f"Cropped: {cropped.shape}")      # (32, 32, 3)
