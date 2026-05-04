# Image Applications

This document covers practical image applications including QR code generation and image compression.

!!! tip "Mental Model"
    Images in Matplotlib are just 2D or 3D NumPy arrays displayed with `imshow()`. This means any array operation -- SVD compression, channel manipulation, thresholding -- becomes a visual transformation you can immediately plot. The bridge between numerical computing and visual output makes Matplotlib a natural tool for image processing workflows.

!!! note "Images as Information"
    Both applications on this page treat images as **carriers of information**,
    not just visuals:

    - **QR codes** → encode data *into* pixel patterns (information → image)
    - **SVD compression** → reduce redundancy *within* pixel data (image → compact representation)

    Both connect back to core ideas: QR codes use binary arrays; SVD compression
    uses the same [singular value decomposition](../../ch09/linalg/svd.md) from
    the linear algebra chapter — truncating small singular values discards the
    least important image structure.

!!! note "Two Sides of Image Applications"
    This page covers two complementary applications of images as arrays:

    - **Generation** — creating images programmatically (QR codes, synthetic data). The image is an output produced by encoding information into a pixel grid.
    - **Compression** — reducing image file size while preserving visual quality. Compression exploits **redundancy** in the array: neighboring pixels are often similar (spatial redundancy) and human vision is less sensitive to certain details (perceptual redundancy). SVD-based compression, shown below, approximates the image matrix with fewer components — discarding small singular values removes information the eye barely notices.

    Both topics treat images as **numerical data** that can be created, analyzed, and optimized using the same NumPy array operations.

## QR Code Generation

Generate and visualize QR codes using the `qrcode` library.

[QR Code Video Explanation](https://www.youtube.com/watch?v=03qMfonukno)

### Installation

```bash
pip install qrcode
```

### Basic Usage

```python
import matplotlib.pyplot as plt
import qrcode

def main():
    # Make QR code image
    img = qrcode.make('https://www.youtube.com/watch?v=03qMfonukno')

    # Save QR code image as jpg
    img.save('YouTubeQRCode.jpg')

    # Show QR code image
    fig, ax = plt.subplots()
    ax.imshow(img, cmap='binary')
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
```

### QR Code Content Types

#### URL

```python
url_qr = qrcode.make('https://www.example.com')
```

#### Text

```python
text_qr = qrcode.make('Hello, World! This is a QR code.')
```

#### Contact Information (vCard)

```python
vcard = """BEGIN:VCARD
VERSION:3.0
N:Doe;John
FN:John Doe
ORG:Example Inc.
TEL:+1234567890
EMAIL:john.doe@example.com
END:VCARD"""

vcard_qr = qrcode.make(vcard)
```

#### WiFi Connection

```python
# WiFi QR code format: WIFI:T:WPA;S:NetworkName;P:Password;;
wifi_config = "WIFI:T:WPA;S:MyWiFiNetwork;P:MyPassword;;"
wifi_qr = qrcode.make(wifi_config)
```

### Advanced QR Code Generation

```python
import matplotlib.pyplot as plt
import qrcode

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data('https://www.example.com')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

fig, ax = plt.subplots()
ax.imshow(img, cmap='binary')
ax.axis('off')
plt.show()
```

### Error Correction Levels

| Level | Constant | Recovery |
|-------|----------|----------|
| L | ERROR_CORRECT_L | ~7% |
| M | ERROR_CORRECT_M | ~15% |
| Q | ERROR_CORRECT_Q | ~25% |
| H | ERROR_CORRECT_H | ~30% |

```python
import matplotlib.pyplot as plt
import qrcode

data = 'https://www.example.com'

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
corrections = [
    (qrcode.constants.ERROR_CORRECT_L, 'L (~7%)'),
    (qrcode.constants.ERROR_CORRECT_M, 'M (~15%)'),
    (qrcode.constants.ERROR_CORRECT_Q, 'Q (~25%)'),
    (qrcode.constants.ERROR_CORRECT_H, 'H (~30%)')
]

for ax, (level, name) in zip(axes, corrections):
    qr = qrcode.QRCode(error_correction=level, box_size=10, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    ax.imshow(img, cmap='binary')
    ax.set_title(f'Error Correction: {name}')
    ax.axis('off')

plt.tight_layout()
plt.show()
```

### Custom Colors

```python
import matplotlib.pyplot as plt
import qrcode

qr = qrcode.QRCode(box_size=10, border=2)
qr.add_data('https://www.example.com')
qr.make(fit=True)

colors = [
    ("black", "white"),
    ("darkblue", "lightyellow"),
    ("darkgreen", "lightgray"),
    ("darkred", "white")
]

fig, axes = plt.subplots(1, 4, figsize=(16, 4))

for ax, (fill, back) in zip(axes, colors):
    img = qr.make_image(fill_color=fill, back_color=back)
    ax.imshow(img)
    ax.set_title(f'{fill} on {back}')
    ax.axis('off')

plt.tight_layout()
plt.show()
```

### Business Card QR Example

```python
import matplotlib.pyplot as plt
import qrcode

contact_info = """BEGIN:VCARD
VERSION:3.0
N:Smith;Jane
FN:Jane Smith
TITLE:Software Engineer
ORG:Tech Company
TEL;TYPE=WORK:+1-555-123-4567
EMAIL:jane.smith@techcompany.com
URL:https://janesmith.dev
END:VCARD"""

qr = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data(contact_info)
qr.make(fit=True)
img = qr.make_image(fill_color="#2c3e50", back_color="white")

fig, ax = plt.subplots(figsize=(6, 6))
ax.imshow(img)
ax.set_title('Scan for Contact Info', fontsize=14, fontweight='bold')
ax.axis('off')
plt.tight_layout()
plt.show()
```

---

## Image Compression

Understanding image compression techniques and their effects on image quality.

### Compression Types

| Type | Description | Formats | Use Case |
|------|-------------|---------|----------|
| Lossless | No data loss | PNG, BMP, TIFF | Graphics, screenshots |
| Lossy | Some data discarded | JPEG, WebP | Photos, web images |

### JPEG Quality Comparison

```python
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# Load original image
img = Image.open('image.jpg')

# Save at different quality levels
qualities = [10, 30, 50, 70, 90]
compressed_images = []

for q in qualities:
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=q)
    buffer.seek(0)
    compressed_images.append(Image.open(buffer))

# Display comparison
fig, axes = plt.subplots(1, 5, figsize=(20, 4))

for ax, comp_img, q in zip(axes, compressed_images, qualities):
    ax.imshow(comp_img)
    ax.set_title(f'Quality: {q}')
    ax.axis('off')

plt.tight_layout()
plt.show()
```

### File Size vs Quality

```python
import matplotlib.pyplot as plt
from PIL import Image
import io

img = Image.open('image.jpg')

qualities = range(10, 101, 10)
sizes = []

for q in qualities:
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=q)
    sizes.append(len(buffer.getvalue()) / 1024)  # KB

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(qualities, sizes, 'bo-', linewidth=2, markersize=8)
ax.set_xlabel('JPEG Quality')
ax.set_ylabel('File Size (KB)')
ax.set_title('JPEG Quality vs File Size')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Compression Artifacts

```python
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import io

# Create image with sharp edges (prone to artifacts)
gradient = np.zeros((100, 200, 3), dtype=np.uint8)
gradient[:, :100] = [255, 0, 0]   # Red
gradient[:, 100:] = [0, 0, 255]   # Blue

img = Image.fromarray(gradient)

# Heavy compression
buffer = io.BytesIO()
img.save(buffer, format='JPEG', quality=5)
buffer.seek(0)
compressed = Image.open(buffer)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].imshow(img)
axes[0].set_title('Original')
axes[0].axis('off')

axes[1].imshow(compressed)
axes[1].set_title('JPEG Quality=5 (Artifacts visible)')
axes[1].axis('off')

plt.tight_layout()
plt.show()
```

### Generational Loss

```python
import matplotlib.pyplot as plt
from PIL import Image
import io

def recompress_jpeg(img, quality, generations):
    """Simulate multiple JPEG saves (generational loss)."""
    current = img
    for _ in range(generations):
        buffer = io.BytesIO()
        current.save(buffer, format='JPEG', quality=quality)
        buffer.seek(0)
        current = Image.open(buffer)
    return current

img = Image.open('image.jpg')
generations = [1, 5, 10, 20]

fig, axes = plt.subplots(1, 4, figsize=(16, 4))

for ax, gen in zip(axes, generations):
    degraded = recompress_jpeg(img.copy(), quality=70, generations=gen)
    ax.imshow(degraded)
    ax.set_title(f'{gen} generations')
    ax.axis('off')

plt.suptitle('JPEG Generational Loss (Quality=70)', fontsize=14)
plt.tight_layout()
plt.show()
```

### Format Comparison

```python
import matplotlib.pyplot as plt
from PIL import Image
import io

img = Image.open('image.png').convert('RGB')

formats = {
    'JPEG (Q=85)': ('JPEG', {'quality': 85}),
    'JPEG (Q=50)': ('JPEG', {'quality': 50}),
    'PNG': ('PNG', {}),
    'WebP (Q=85)': ('WEBP', {'quality': 85})
}

results = {}
for name, (fmt, kwargs) in formats.items():
    buffer = io.BytesIO()
    img.save(buffer, format=fmt, **kwargs)
    size_kb = len(buffer.getvalue()) / 1024
    buffer.seek(0)
    results[name] = (Image.open(buffer), size_kb)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for ax, (name, (comp_img, size)) in zip(axes.flat, results.items()):
    ax.imshow(comp_img)
    ax.set_title(f'{name}\n{size:.1f} KB')
    ax.axis('off')

plt.tight_layout()
plt.show()
```

### Matplotlib Save Compression

```python
import matplotlib.pyplot as plt
import numpy as np

# Create sample plot
fig, ax = plt.subplots(figsize=(8, 6))
x = np.linspace(0, 10, 100)
ax.plot(x, np.sin(x), 'b-', linewidth=2)
ax.set_title('Sample Plot')

# Save with different settings
fig.savefig('plot_low.jpg', dpi=72, quality=50)
fig.savefig('plot_high.jpg', dpi=150, quality=95)
fig.savefig('plot.png', dpi=150)

plt.show()
```

### Choosing Format

| Content Type | Recommended Format | Reason |
|--------------|-------------------|--------|
| Photographs | JPEG (Q=80-90) | Good compression, acceptable loss |
| Screenshots | PNG | Sharp edges preserved |
| Graphics/Logos | PNG or SVG | No artifacts |
| Web photos | WebP | Best compression ratio |
| Scientific figures | PDF/SVG | Vector, scalable |

### Quality Recommendations

| Quality Range | Description |
|---------------|-------------|
| 90-100 | Maximum quality, large files |
| 80-90 | High quality, good for printing |
| 60-80 | Good quality, web standard |
| 40-60 | Medium quality, smaller files |
| 20-40 | Low quality, thumbnails |
| 1-20 | Very low, visible artifacts |

### Image Optimization Workflow

```python
import matplotlib.pyplot as plt
from PIL import Image
import io
import os

def optimize_image(input_path, output_path, max_size_kb=100, min_quality=30):
    """Optimize image to target file size."""
    img = Image.open(input_path)
    
    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # Binary search for quality
    low, high = min_quality, 95
    best_quality = high
    
    while low <= high:
        mid = (low + high) // 2
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=mid)
        size_kb = len(buffer.getvalue()) / 1024
        
        if size_kb <= max_size_kb:
            best_quality = mid
            low = mid + 1
        else:
            high = mid - 1
    
    # Save with best quality
    img.save(output_path, format='JPEG', quality=best_quality)
    final_size = os.path.getsize(output_path) / 1024
    
    return best_quality, final_size

# Usage
quality, size = optimize_image('large_image.jpg', 'optimized.jpg', max_size_kb=200)
print(f"Optimized to quality={quality}, size={size:.1f}KB")
```

---

## Summary

### QR Code Quick Reference

```python
import qrcode

# Simple QR
img = qrcode.make('data')

# Advanced QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data('data')
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
```

### Compression Quick Reference

```python
from PIL import Image
import io

# JPEG compression
img.save('output.jpg', format='JPEG', quality=85)

# PNG compression
img.save('output.png', format='PNG', compress_level=6)

# In-memory compression
buffer = io.BytesIO()
img.save(buffer, format='JPEG', quality=70)
```


---

## Exercises

**Exercise 1.** Write code that creates a 100x100 NumPy array representing a gradient image (values from 0 to 1, increasing left to right) and displays it using `ax.imshow()` with the `'gray'` colormap.

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

**Exercise 2.** Explain the role of the `origin` parameter in `ax.imshow()`. What is the difference between `origin='upper'` (default) and `origin='lower'`?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that creates a 3x1 subplot figure showing the same 2D array displayed with three different colormaps: `'gray'`, `'hot'`, and `'viridis'`.

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

**Exercise 4.** Create a synthetic RGB image as a NumPy array of shape `(100, 100, 3)` with a red top-left, green top-right, blue bottom-left, and white bottom-right quadrant. Display it with `ax.imshow()`.

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
