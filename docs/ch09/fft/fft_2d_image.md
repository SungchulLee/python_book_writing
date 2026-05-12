# 2D FFT for Image Processing

!!! tip "Mental Model"
    A 2D FFT decomposes an image into spatial frequencies along rows and columns simultaneously. Low frequencies near the center capture smooth gradients; high frequencies at the edges capture sharp details and noise. Filtering in the frequency domain is just multiplying by a mask, making operations like blurring or edge detection fast and elegant.

!!! note "Visual Cheat Sheet"
    ```text
    Center of shifted FFT   →  low frequencies  →  smooth gradients
    Edges of shifted FFT    →  high frequencies →  sharp details / noise
    Bright isolated spikes  →  periodic noise   →  remove with notch filter
    ```

## Why 2D FFT for Images?

A digital image is a 2D signal: a matrix of pixel intensities. Just as 1D FFT decomposes signals into frequency components, **2D FFT** decomposes images into frequency components in both spatial dimensions.

**Key insight:**

- **Low frequencies** in an image represent smooth regions (large color/brightness areas)
- **High frequencies** represent edges, textures, and fine details
- **Periodic patterns** (like striped noise) show up as concentrated peaks in frequency space

This opens possibilities:

- **Denoising**: Suppress high-frequency noise while preserving edges
- **Blur detection**: Analyze frequency content
- **Remove periodic noise**: Identify and eliminate repeating patterns
- **Image restoration**: Reverse certain degradations
- **Efficient convolution**: For large kernels, FFT-based convolution is faster than spatial convolution

## 2D FFT Fundamentals

### Mathematical Definition

The 2D DFT is:

$$X(u, v) = \sum_{m=0}^{M-1} \sum_{n=0}^{N-1} x(m, n) \cdot e^{-j2\pi(um/M + vn/N)}$$

where:

- $x(m, n)$ is the pixel intensity at row $m$, column $n$
- $X(u, v)$ is the frequency component at frequency $(u, v)$
- $M, N$ are image dimensions

**In practice:** Use `np.fft.fft2()` or `scipy.fftpack.fftn()` instead of implementing manually.

### Computing 2D FFT

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage

# Load or create an image
# For this example, create a simple geometric image
image = np.zeros((256, 256))
image[50:150, 50:150] = 1  # white square

# Compute 2D FFT
X = np.fft.fft2(image)

# Magnitude spectrum
X_mag = np.abs(X)

# Log scale for better visualization
X_mag_log = np.log1p(X_mag)

print(f"Image shape: {image.shape}")
print(f"FFT shape: {X.shape}")
print(f"FFT dtype: {X.dtype}")  # complex128
```

### Interpreting Frequency Components

The output `X` is a 2D array of complex numbers:

- **Real part**: Cosine components
- **Imaginary part**: Sine components
- **Magnitude** $|X(u, v)|$: Amplitude at frequency $(u, v)$
- **Phase** $\angle X(u, v)$: Phase shift

**Frequency layout (without fftshift):**

- Origin $(0, 0)$ is at top-left
- Positive frequencies in top-right and bottom-left
- Negative frequencies in bottom-right (due to complex conjugate symmetry)

## Using `fftshift()` to Center Zero Frequency

By default, the zero frequency (DC component) is at the top-left corner. To visualize conveniently, center it:

```python
# Shift zero frequency to center
X_shifted = np.fft.fftshift(X)

# Now:
# - Center of image: low frequencies (DC)
# - Edges of image: high frequencies
```

**Complete example:**

```python
import numpy as np
import matplotlib.pyplot as plt

# Simple test image: white square on black background
image = np.zeros((128, 128))
image[40:88, 40:88] = 255

# Compute FFT
X = np.fft.fft2(image)

# Magnitude and log scale
X_mag = np.abs(X)
X_mag_log = np.log1p(X_mag)

# Shift for visualization
X_shifted = np.fft.fftshift(X_mag_log)

# Plot
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Original image
ax = axes[0]
ax.imshow(image, cmap='gray')
ax.set_title('Original Image')
ax.axis('off')

# FFT magnitude (unshifted)
ax = axes[1]
ax.imshow(X_mag_log, cmap='hot')
ax.set_title('FFT Magnitude (log) - Unshifted')
ax.axis('off')

# FFT magnitude (shifted)
ax = axes[2]
ax.imshow(X_shifted, cmap='hot')
ax.set_title('FFT Magnitude (log) - Shifted')
ax.axis('off')

plt.tight_layout()
plt.show()
```

!!! note "Symmetry in Real Images"
    For real-valued images (typical case), the FFT has Hermitian symmetry:

    $$X(-u, -v) = X^*(u, v)$$

    This means the negative frequencies contain redundant information (they're complex conjugates of positive frequencies). In some applications, you only need half the FFT output.

## Application: Removing Periodic Noise

Periodic patterns (like scan lines or striped artifacts) create concentrated peaks in frequency space. You can remove them by suppressing those peaks.

### Workflow

1. **Compute FFT** of the noisy image
2. **Identify noise peaks** visually or algorithmically
3. **Create a notch filter** (suppress specific frequencies)
4. **Apply the filter** in frequency domain
5. **Inverse FFT** to get the cleaned image

### Example: Removing Periodic Noise

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from scipy.ndimage import gaussian_filter

# Create a clean image (sample)
image_clean = np.zeros((256, 256))
image_clean = ndimage.binary_dilation(
    image_clean,
    iterations=0
).astype(float)

# Add realistic content: a circle
y, x = np.ogrid[:256, :256]
mask = (x - 128)**2 + (y - 128)**2 <= 60**2
image_clean[mask] = 200

# Add periodic stripe noise (horizontal)
stripe_period = 16
image_noisy = image_clean.copy()
for i in range(0, 256, stripe_period):
    image_noisy[i:i+2, :] += 50

image_noisy = np.clip(image_noisy, 0, 255)

# Compute FFT
X = np.fft.fft2(image_noisy)
X_shifted = np.fft.fftshift(X)

# Visualize FFT to identify noise peaks
X_mag = np.log1p(np.abs(X_shifted))

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Row 1: Original and FFT
ax = axes[0, 0]
ax.imshow(image_noisy, cmap='gray')
ax.set_title('Noisy Image (stripe pattern)')

ax = axes[0, 1]
ax.imshow(X_mag, cmap='hot')
ax.set_title('FFT Magnitude (log)')

# Create notch filter to suppress stripe noise
# Stripes repeat every 16 pixels → peak at frequency 256/16 = 16
notch_filter = np.ones_like(X_shifted)

# Suppress the vertical stripe peaks (horizontal frequency)
# These appear at (center_y, center_x ± stripe_freq)
freq_stripe = 256 // stripe_period
center = 128

# Create Gaussian notch at the noise frequency
for dy in [-freq_stripe, freq_stripe]:
    y_notch = center + dy
    for x_idx in range(256):
        dist = (x_idx - center)**2 + (y_notch - center)**2
        notch_filter[y_notch, x_idx] *= np.exp(-dist / 1000)

ax = axes[0, 2]
ax.imshow(notch_filter, cmap='gray')
ax.set_title('Notch Filter (suppresses peaks)')

# Apply filter in frequency domain
X_filtered = X_shifted * notch_filter

# Inverse FFT
X_filtered_unshifted = np.fft.ifftshift(X_filtered)
image_restored = np.fft.ifft2(X_filtered_unshifted).real

# Clip to valid range
image_restored = np.clip(image_restored, 0, 255)

# Visualize results
ax = axes[1, 0]
ax.imshow(image_restored, cmap='gray')
ax.set_title('Restored Image')

ax = axes[1, 1]
ax.imshow(np.abs(X_shifted * notch_filter), cmap='hot')
ax.set_title('Filtered FFT')

# Difference
ax = axes[1, 2]
diff = np.abs(image_noisy - image_restored)
ax.imshow(diff, cmap='hot')
ax.set_title('Removed Noise (difference)')

for ax in axes.flat:
    ax.axis('off')

plt.suptitle('Periodic Noise Removal via Frequency Domain')
plt.tight_layout()
plt.show()

# Quantify improvement
noise_original = np.mean((image_noisy - image_clean)**2)
noise_restored = np.mean((image_restored - image_clean)**2)

print(f"Original MSE: {noise_original:.1f}")
print(f"Restored MSE: {noise_restored:.1f}")
print(f"Improvement: {noise_original / noise_restored:.1f}x")
```

!!! tip "More Sophisticated Filters"

    - **Butterworth filter**: Smooth roll-off (avoids sharp artifacts)
    - **Morphological operations**: Enhance specific frequency bands
    - **Wiener filter**: Optimal restoration for known noise statistics
    - **For real applications**: Use scikit-image (restoration module)

## FFT-Based Convolution

The **convolution theorem** is the bridge between spatial and frequency domains: convolution in the spatial domain is equivalent to pointwise multiplication in the frequency domain (and vice versa). This means a filter that would require expensive sliding-window operations in spatial space becomes a single element-wise multiply after an FFT:

$$y = \text{IFFT}(\text{FFT}(x) \cdot \text{FFT}(h))$$

### When to Use FFT Convolution

- **Kernel size** > ~10×10 pixels: FFT is faster
- **Small kernels** (3×3, 5×5): Spatial convolution is faster
- **Repetitive convolution**: Amortize FFT computation cost

### Example: Blur with FFT

```python
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

# Create test image (checkerboard)
image = np.zeros((256, 256))
image[::8, ::8] = 1
image[1::8, 1::8] = 1
image[::8, 1::8] = 1
image[1::8, ::8] = 1

# Define blur kernel (Gaussian)
kernel_size = 31
kernel = ndimage.gaussian_filter(
    np.ones((kernel_size, kernel_size)),
    sigma=5
)
kernel /= kernel.sum()

print(f"Image shape: {image.shape}")
print(f"Kernel shape: {kernel.shape}")

# Method 1: Spatial convolution
result_spatial = ndimage.convolve(image, kernel)

# Method 2: FFT convolution
# Need to zero-pad to avoid circular convolution
M, N = image.shape
Mk, Nk = kernel.shape

# Pad to M + Mk - 1, N + Nk - 1
output_shape = (M + Mk - 1, N + Nk - 1)

# Pad image and kernel
image_padded = np.pad(image, ((0, Mk-1), (0, Nk-1)), mode='constant')
kernel_padded = np.pad(kernel, ((0, M-1), (0, N-1)), mode='constant')

# FFT-based convolution
X = np.fft.fft2(image_padded)
H = np.fft.fft2(kernel_padded)
Y = X * H
result_fft = np.fft.ifft2(Y).real

# Crop to original size
result_fft = result_fft[:M, :N]

# Compare
fig, axes = plt.subplots(2, 2, figsize=(12, 12))

ax = axes[0, 0]
ax.imshow(image, cmap='gray')
ax.set_title('Original Image')
ax.axis('off')

ax = axes[0, 1]
ax.imshow(kernel, cmap='gray')
ax.set_title('Blur Kernel')
ax.axis('off')

ax = axes[1, 0]
ax.imshow(result_spatial, cmap='gray')
ax.set_title('Spatial Convolution')
ax.axis('off')

ax = axes[1, 1]
ax.imshow(result_fft, cmap='gray')
ax.set_title('FFT Convolution')
ax.axis('off')

plt.tight_layout()
plt.show()

# Verify they produce the same result
difference = np.max(np.abs(result_spatial - result_fft))
print(f"Max difference: {difference:.2e} (should be ~0)")
print(f"Results match: {np.allclose(result_spatial, result_fft, atol=1e-10)}")
```

### Performance Comparison

```python
import time
import numpy as np
from scipy import ndimage

# Benchmark
image = np.random.rand(512, 512)
kernel = np.random.rand(64, 64)
kernel /= kernel.sum()

# Time spatial convolution
start = time.perf_counter()
for _ in range(10):
    _ = ndimage.convolve(image, kernel)
time_spatial = time.perf_counter() - start

# Time FFT convolution
start = time.perf_counter()
for _ in range(10):
    M, N = image.shape
    Mk, Nk = kernel.shape
    image_padded = np.pad(image, ((0, Mk-1), (0, Nk-1)))
    kernel_padded = np.pad(kernel, ((0, M-1), (0, N-1)))
    X = np.fft.fft2(image_padded)
    H = np.fft.fft2(kernel_padded)
    Y = X * H
    _ = np.fft.ifft2(Y).real[:M, :N]
time_fft = time.perf_counter() - start

print(f"Spatial convolution: {time_spatial:.3f} sec")
print(f"FFT convolution: {time_fft:.3f} sec")
print(f"Speedup: {time_spatial / time_fft:.1f}x")
```

**Typical speedup:** 5-10x for 64×64 kernels, even more for larger kernels.

!!! note "Real-World FFT Convolution"
    SciPy provides optimized versions:
    ```python
    from scipy.signal import fftconvolve
    result = fftconvolve(image, kernel, mode='same')
    ```
    This handles padding and edge modes automatically.

## Zero-Padding Considerations

Zero-padding affects FFT behavior in important ways:

### 1. Avoiding Circular Convolution

By default, FFT assumes **circular convolution** (the signal wraps around). To get **linear convolution**, pad with zeros:

```python
# Without padding: circular convolution
X = np.fft.fft2(image)
H = np.fft.fft2(kernel)
Y = X * H
result_circular = np.fft.ifft2(Y).real

# With padding: linear convolution
M, N = image.shape
Mk, Nk = kernel.shape
image_padded = np.pad(image, ((0, Mk-1), (0, Nk-1)))
kernel_padded = np.pad(kernel, ((0, M-1), (0, N-1)))
X = np.fft.fft2(image_padded)
H = np.fft.fft2(kernel_padded)
Y = X * H
result_linear = np.fft.ifft2(Y).real[:M, :N]
```

### 2. Frequency Resolution

More zero-padding increases frequency resolution but doesn't improve the actual information content:

```python
# Image: 128×128 pixels
image = np.random.rand(128, 128)

# No padding
X1 = np.fft.fft2(image)
freqs1 = np.fft.fftfreq(128, 1.0)

# 2x padding (256×256)
image_padded = np.pad(image, ((0, 128), (0, 128)))
X2 = np.fft.fft2(image_padded)
freqs2 = np.fft.fftfreq(256, 1.0)

print(f"Frequency resolution without padding: {1.0/128:.4f}")
print(f"Frequency resolution with 2x padding: {1.0/256:.4f}")
print(f"More padding = finer frequency grid (interpolation, not more info)")
```

### 3. Edge Effects

Abrupt image boundaries create high-frequency artifacts. Options:

- **Zero-padding**: Simple but introduces discontinuity
- **Mirroring**: Reflects image edges
- **Periodic extension**: Assumes the image repeats (FFT default)

```python
image = np.random.rand(64, 64)

# Pad with different modes
padded_zeros = np.pad(image, 32, mode='constant', constant_values=0)
padded_reflect = np.pad(image, 32, mode='reflect')
padded_wrap = np.pad(image, 32, mode='wrap')

# Compare frequency content
X_zeros = np.log1p(np.abs(np.fft.fft2(padded_zeros)))
X_reflect = np.log1p(np.abs(np.fft.fft2(padded_reflect)))

# Reflection typically gives lower high-frequency artifacts
```

## Complete Image Denoising Pipeline

```python
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

def denoise_fft(image, threshold_percentile=90):
    """Denoise image by suppressing low-magnitude frequency components."""

    # Compute FFT
    X = np.fft.fft2(image)

    # Magnitude spectrum
    X_mag = np.abs(X)

    # Threshold: keep top X% of frequencies
    threshold = np.percentile(X_mag, threshold_percentile)

    # Create binary mask
    mask = X_mag > threshold

    # Apply mask
    X_filtered = X * mask

    # Inverse FFT
    image_denoised = np.fft.ifft2(X_filtered).real

    return image_denoised, X, mask

# Test
image = ndimage.gaussian_filter(np.random.rand(128, 128), sigma=2)
image_noisy = image + 0.3 * np.random.randn(128, 128)

image_denoised, X, mask = denoise_fft(image_noisy, threshold_percentile=85)

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].imshow(image_noisy, cmap='gray')
axes[0].set_title('Noisy Image')

axes[1].imshow(np.log1p(np.abs(X)), cmap='hot')
axes[1].set_title('FFT Magnitude')

axes[2].imshow(image_denoised, cmap='gray')
axes[2].set_title('Denoised (FFT threshold)')

for ax in axes:
    ax.axis('off')

plt.tight_layout()
plt.show()
```

!!! tip "Why 2D FFT Is Separable"
    The 2D DFT can be computed as a sequence of 1D DFTs: first along rows, then
    along columns (or vice versa). This **separability** is why `np.fft.fft2` is
    efficient — it applies the 1D FFT algorithm twice rather than computing the full
    2D sum directly. It also means that intuition from 1D FFT (frequency bins,
    symmetry, leakage) transfers directly to each axis of the 2D case.

## Summary

- **2D FFT** decomposes images into frequency components
- **Low frequencies** = smooth regions; **high frequencies** = edges and noise
- **`fftshift()`** centers zero frequency for intuitive visualization
- **Frequency domain filtering** can remove periodic noise effectively
- **FFT convolution** is faster for large kernels (>10×10)
- **Zero-padding** avoids circular convolution and can reduce edge artifacts
- **Real-world applications** use SciPy (`fftconvolve`, `ndimage`) for reliability

**Next steps:**

- Explore **convolution theorem** for deeper frequency domain theory
- Study **image restoration** techniques (Wiener filtering, etc.)
- Apply to **computer vision** tasks: edge detection, blur analysis, feature extraction

---

## Exercises

**Exercise 1.**
Create a 128x128 image with a single white horizontal stripe (row 64, all columns set to 255). Compute its 2D FFT, shift it with `fftshift`, and display the log-magnitude spectrum. Explain why the energy concentrates along the vertical axis in the frequency domain.

??? success "Solution to Exercise 1"

        import numpy as np
        import matplotlib.pyplot as plt

        image = np.zeros((128, 128))
        image[64, :] = 255

        X = np.fft.fft2(image)
        X_shifted = np.fft.fftshift(X)
        mag = np.log1p(np.abs(X_shifted))

        # The horizontal stripe has variation only along the vertical
        # direction, so its frequency content lies along the vertical
        # axis (u-axis) in the 2D frequency domain.
        print(f"Spectrum shape: {mag.shape}")
        print("Energy is along vertical axis because the stripe is horizontal.")

---

**Exercise 2.**
Implement a simple low-pass filter in the frequency domain: create a circular mask of radius 20 centered in the shifted FFT, multiply the shifted FFT by this mask, then invert the FFT. Apply this to a noisy checkerboard image (8x8 pattern with Gaussian noise `sigma=50`) and compare the denoised result with the original clean image.

??? success "Solution to Exercise 2"

        import numpy as np

        # Create clean checkerboard
        image = np.zeros((128, 128))
        for i in range(0, 128, 16):
            for j in range(0, 128, 16):
                image[i:i+8, j:j+8] = 255
                image[i+8:i+16, j+8:j+16] = 255

        # Add noise
        np.random.seed(42)
        noisy = image + np.random.randn(128, 128) * 50
        noisy = np.clip(noisy, 0, 255)

        # Low-pass filter
        X = np.fft.fft2(noisy)
        X_shifted = np.fft.fftshift(X)

        # Circular mask of radius 20
        cy, cx = 64, 64
        Y, XC = np.ogrid[:128, :128]
        mask = ((Y - cy)**2 + (XC - cx)**2) <= 20**2

        X_filtered = X_shifted * mask
        denoised = np.fft.ifft2(np.fft.ifftshift(X_filtered)).real

        mse = np.mean((denoised - image)**2)
        print(f"MSE after low-pass: {mse:.1f}")

---

**Exercise 3.**
Given two images of the same size, implement FFT-based convolution using `np.fft.fft2` without relying on `scipy.signal.fftconvolve`. Apply a 15x15 averaging kernel to a 256x256 random image, remembering to zero-pad both the image and kernel to avoid circular convolution artifacts. Verify your result matches `scipy.ndimage.convolve` within a tolerance of `1e-10`.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import ndimage

        image = np.random.rand(256, 256)
        kernel = np.ones((15, 15)) / (15 * 15)

        # Zero-pad
        M, N = image.shape
        Mk, Nk = kernel.shape
        image_padded = np.pad(image, ((0, Mk - 1), (0, Nk - 1)))
        kernel_padded = np.pad(kernel, ((0, M - 1), (0, N - 1)))

        # FFT-based convolution
        X = np.fft.fft2(image_padded)
        H = np.fft.fft2(kernel_padded)
        result_fft = np.fft.ifft2(X * H).real[:M, :N]

        # Reference
        result_ref = ndimage.convolve(image, kernel)

        print(f"Max difference: {np.max(np.abs(result_fft - result_ref)):.2e}")
        print(f"Match: {np.allclose(result_fft, result_ref, atol=1e-10)}")
