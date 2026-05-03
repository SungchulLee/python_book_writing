# Convolution and Filtering with scipy.ndimage

Convolution is one of the most fundamental operations in image processing and scientific computing. It allows us to compute weighted sums over neighborhoods in arrays, enabling edge detection, smoothing, and feature extraction.

!!! tip "Mental Model"
    Convolution slides a small kernel across an array and computes a weighted sum at every position. A uniform kernel blurs (averaging), a derivative kernel detects edges, and a Gaussian kernel smooths while preserving locality. `scipy.ndimage` handles boundary conditions and multi-dimensional arrays, making it the go-to for array-based spatial filtering.

    Mathematically, convolution is a **linear operator** — it satisfies
    $\text{conv}(\alpha x + \beta y) = \alpha\,\text{conv}(x) + \beta\,\text{conv}(y)$.
    This linearity is what makes convolution composable (applying two kernels in
    sequence is the same as convolving with their combined kernel) and analyzable
    via the Fourier transform.

!!! note "Unified Neighborhood Operator Framework"
    All spatial operations in this section follow the same pattern:

    1. **Define a neighborhood** (kernel, structure element, or footprint)
    2. **Extract values** around each point
    3. **Apply a function** to that neighborhood
    4. **Write the result** to the output array

    This gives three major operator classes:

    | Class | Neighborhood function | Example |
    |-------|----------------------|---------|
    | **Convolution** | Weighted sum (linear) | Gaussian blur, Sobel edges |
    | **Morphology** | Shape-based set rules (geometric) | Erosion, dilation, opening |
    | **Generic filter** | Arbitrary Python function (nonlinear) | Median, percentile, Game of Life |

    The difference is only in step 3. Once you see this, the three topics become
    variations on a single idea: *point → neighborhood → transformation*.

    The deeper insight: these are **local computations that produce global
    structure**. Each element sees only its neighbors, applies a rule, and writes
    one output value — yet the aggregate effect creates smoothing, edge detection,
    segmentation, and even dynamic systems like cellular automata. The same
    pattern underlies convolutional neural networks (CNNs), PDE solvers (finite
    differences), and reaction-diffusion simulations.

## What is Convolution?

Convolution combines two functions to produce a third function that expresses how one function modifies the other. In discrete form, for a 1D signal, convolution is defined as:

$$s'(t) = \sum_{j=t-\tau}^{t} s(j) f(t-j)$$

where $s(t)$ is the input signal, $f$ is the filter kernel, and $s'(t)$ is the output. The kernel is typically small and is "flipped" as it slides across the signal.

For 2D images, this generalizes naturally:

$$I'(x,y) = \sum_{i,j} I(x+i, y+j) \cdot K(i, j)$$

where $K$ is a 2D kernel and $I$ is the image.

!!! note "Why Convolution Matters"
    Convolution is the mathematical foundation for:
    - **Blurring and smoothing** - Averaging neighboring values
    - **Edge detection** - Finding boundaries where intensity changes
    - **Feature extraction** - Highlighting patterns in images
    - **Denoising** - Removing noise while preserving structure

## 1D Convolution Example

Let's start with a simple 1D example to understand how `ndi.convolve()` works:

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create a simple 1D signal with a spike
signal = np.array([0, 0, 0, 1, 0, 0, 0])

# Define a simple averaging kernel
kernel = np.array([0.25, 0.5, 0.25])

# Apply convolution
result = ndi.convolve(signal, kernel)
print("Signal:", signal)
print("Kernel:", kernel)
print("Result:", result)
```

The `convolve()` function slides the kernel across the signal, computing weighted sums at each position. At boundaries, it uses a default boundary handling mode (we'll discuss these next).

## 2D Convolution and Boundary Modes

When working with 2D images, boundary handling becomes important—what happens at the edges where the kernel extends beyond the image? `scipy.ndimage` provides several boundary modes:

```python
import numpy as np
from scipy import ndimage as ndi

# Create a small test image
image = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]], dtype=float)

# Define a simple kernel
kernel = np.array([[1, 0, -1],
                   [2, 0, -2],
                   [1, 0, -1]]) / 8.0

# Different boundary modes
modes = ['nearest', 'constant', 'wrap', 'reflect']

for mode in modes:
    result = ndi.convolve(image, kernel, mode=mode)
    print(f"Mode: {mode}")
    print(result)
    print()
```

### Boundary Modes Explained

- **`nearest`**: Repeat the edge pixel values (default)
- **`constant`**: Pad with a constant value (default 0)
- **`wrap`**: Wrap around as if the array is periodic
- **`reflect`**: Mirror values at the boundary

!!! tip "Choosing the Right Mode"
    - Use **`reflect`** for natural images where boundaries shouldn't repeat
    - Use **`wrap`** for periodic data (e.g., spherical coordinates)
    - Use **`nearest`** when edge pixels matter
    - Use **`constant`** (with `cval` parameter) for synthetic backgrounds

## Difference Filters for Edge Detection

Difference filters compute local variations in intensity, revealing edges and boundaries. The simplest is the first-order difference:

```python
import numpy as np
from scipy import ndimage as ndi
from PIL import Image

# Create a simple synthetic image with a step edge
image = np.zeros((5, 10))
image[:, 5:] = 1  # Right half is brighter

# Horizontal difference filter (detects vertical edges)
h_kernel = np.array([[-1, 1]])
h_edges = ndi.convolve(image, h_kernel)

# Vertical difference filter (detects horizontal edges)
v_kernel = np.array([[-1], [1]])
v_edges = ndi.convolve(image, v_kernel)

print("Horizontal edges:\n", h_edges)
print("Vertical edges:\n", v_edges)
```

Difference filters highlight sharp transitions in intensity, making them ideal for boundary detection in images.

## Gaussian Smoothing Kernels

Gaussian smoothing is one of the most important preprocessing steps in image analysis. It reduces noise while preserving edges (better than uniform averaging). The 2D Gaussian kernel is:

$$G(x, y) = \frac{1}{2\pi\sigma^2} e^{-\frac{x^2+y^2}{2\sigma^2}}$$

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create an image with noise
np.random.seed(42)
image = np.random.rand(50, 50)
# Add a bright spot in the center
image[20:30, 20:30] += 2

# Apply Gaussian filter with sigma=2
smoothed = ndi.gaussian_filter(image, sigma=2)

# Compare
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].imshow(image, cmap='gray')
axes[0].set_title('Noisy Image')
axes[1].imshow(smoothed, cmap='gray')
axes[1].set_title('After Gaussian Smoothing (σ=2)')
plt.tight_layout()
plt.show()
```

The `gaussian_filter()` function is optimized using separable convolution—it applies 1D Gaussian filters horizontally and vertically, which is much faster than 2D convolution.

!!! note "Why Gaussian Smoothing?"
    - Natural weighting: nearby pixels have more influence
    - Frequency response: removes high-frequency noise gradually
    - Separable: can be computed efficiently in 1D passes
    - Parameter σ controls the amount of smoothing

## Sobel Edge Detection

The Sobel operator combines horizontal and vertical difference filters to detect edges while reducing noise:

$$S_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}, \quad S_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$

The edge magnitude at each point is $|S| = \sqrt{S_x^2 + S_y^2}$, and the edge direction is $\theta = \arctan(S_y / S_x)$.

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create a synthetic image with features
image = np.zeros((100, 100))
image[25:75, 25:75] = 1  # White square
image[40:60, 40:60] = 0.5  # Gray inner square

# Compute Sobel edges
sx = ndi.sobel(image, axis=0)  # Horizontal edges
sy = ndi.sobel(image, axis=1)  # Vertical edges
magnitude = np.sqrt(sx**2 + sy**2)
direction = np.arctan2(sy, sx)

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(image, cmap='gray')
axes[0, 0].set_title('Original Image')

axes[0, 1].imshow(sx, cmap='RdBu_r')
axes[0, 1].set_title('Sobel-X (Horizontal Edges)')

axes[1, 0].imshow(sy, cmap='RdBu_r')
axes[1, 0].set_title('Sobel-Y (Vertical Edges)')

axes[1, 1].imshow(magnitude, cmap='gray')
axes[1, 1].set_title('Edge Magnitude')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()

# Find strong edges
threshold = 0.1
strong_edges = magnitude > threshold
print(f"Pixels with strong edges: {strong_edges.sum()}")
```

### Understanding the Sobel Kernel

The Sobel kernel weights the central row/column more heavily (coefficient 2 instead of 1) because the center pixel is closer and more reliable. The operator combines:

1. **Smoothing** in one direction (reduces noise)
2. **Differencing** in the perpendicular direction (detects edges)

This combination makes Sobel more robust to noise than simple difference filters.

!!! tip "Key Takeaway"
    Sobel edge detection is a practical tool that:
    - Combines smoothing and differencing for noise robustness
    - Provides both magnitude (edge strength) and direction
    - Forms the basis for more advanced edge detection (Canny, etc.)
    - Runs efficiently on modern hardware

## Advanced: Custom Kernels

You can create custom kernels for specialized applications:

```python
import numpy as np
from scipy import ndimage as ndi

# Laplacian kernel (detects both edges and blobs)
laplacian_kernel = np.array([[0, -1, 0],
                             [-1, 4, -1],
                             [0, -1, 0]])

# Mexican Hat (Ricker wavelet) - useful for blob detection
size = 7
y, x = np.ogrid[-size//2:size//2+1, -size//2:size//2+1]
sigma = 1.5
mexican_hat = -(1 - (x**2 + y**2) / (2*sigma**2)) * np.exp(-(x**2 + y**2) / (2*sigma**2))
mexican_hat /= mexican_hat.sum()  # Normalize

# Test on image
image = np.random.rand(50, 50)
image[20:30, 20:30] += 1  # Add a blob

result_laplacian = ndi.convolve(image, laplacian_kernel)
result_hat = ndi.convolve(image, mexican_hat)

print("Laplacian output range:", result_laplacian.min(), "-", result_laplacian.max())
print("Mexican Hat output range:", result_hat.min(), "-", result_hat.max())
```

## Performance Considerations

For large images, consider these optimizations:

```python
import numpy as np
from scipy import ndimage as ndi
import time

image = np.random.rand(1000, 1000)

# Gaussian filter (highly optimized)
start = time.time()
result1 = ndi.gaussian_filter(image, sigma=3)
t1 = time.time() - start

# Manual 2D convolution with same kernel
gaussian_kernel = np.exp(-(np.arange(-3, 4)**2) / 6.0)
gaussian_kernel_2d = gaussian_kernel[:, None] * gaussian_kernel[None, :]
start = time.time()
result2 = ndi.convolve(image, gaussian_kernel_2d)
t2 = time.time() - start

print(f"Gaussian filter: {t1:.4f}s")
print(f"Manual convolution: {t2:.4f}s")
print(f"Speedup: {t2/t1:.1f}x")
```

!!! tip "Performance Tips"
    - Use `gaussian_filter()` instead of `convolve()` with Gaussian kernels
    - For separable kernels, apply 1D convolutions sequentially
    - Use `order` parameter in `gaussian_filter()` for derivatives
    - Consider frequency-domain methods (FFT) for very large kernels

## Practical Example: Image Enhancement

Here's a complete example combining multiple techniques:

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create synthetic image
np.random.seed(42)
image = np.zeros((100, 100))
image[20:80, 20:80] = 1
image += 0.2 * np.random.randn(100, 100)  # Add noise

# Step 1: Denoise with Gaussian filter
denoised = ndi.gaussian_filter(image, sigma=1)

# Step 2: Detect edges with Sobel
sx = ndi.sobel(denoised, axis=0)
sy = ndi.sobel(denoised, axis=1)
edges = np.sqrt(sx**2 + sy**2)

# Step 3: Sharpen using difference of Gaussians
blurred1 = ndi.gaussian_filter(image, sigma=1)
blurred2 = ndi.gaussian_filter(image, sigma=3)
sharpened = blurred1 - 0.5 * blurred2

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(image, cmap='gray')
axes[0, 0].set_title('Noisy Original')

axes[0, 1].imshow(denoised, cmap='gray')
axes[0, 1].set_title('Denoised')

axes[1, 0].imshow(edges, cmap='gray')
axes[1, 0].set_title('Edge Detection')

axes[1, 1].imshow(sharpened, cmap='gray')
axes[1, 1].set_title('Sharpened')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()
```

## Summary

Convolution is the fundamental building block for image processing and filtering. Key points:

- Convolution applies a weighted sum over neighborhoods using a kernel
- Different boundary modes handle edges differently
- Gaussian smoothing is efficient and noise-preserving
- Sobel edge detection combines smoothing and differencing
- scipy.ndimage provides optimized implementations

See also:
- [Generic Filter Operations](generic_filter.md) - Arbitrary neighborhood computations
- [Binary Structures and Morphology](binary_structure.md) - Connected components and morphological operations

---

## Exercises

**Exercise 1.** Write a short code example that demonstrates the main concept covered on this page. Include comments explaining each step.

??? success "Solution to Exercise 1"
    Refer to the code examples in the page content above. A complete solution would recreate the key pattern with clear comments explaining the NumPy operations involved.

---

**Exercise 2.** Predict the output of a code snippet that uses the features described on this page. Explain why the output is what it is.

??? success "Solution to Exercise 2"
    The output depends on how NumPy handles the specific operation. Key factors include array shapes, dtypes, and broadcasting rules. Trace through the computation step by step.

---

**Exercise 3.** Write a practical function that applies the concepts from this page to solve a real data processing task. Test it with sample data.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    # Example: apply the page's concept to process sample data
    data = np.random.default_rng(42).random((5, 3))
    # Apply the relevant operation
    result = data  # replace with actual operation
    print(result)
    ```

---

**Exercise 4.** Identify a common mistake when using the features described on this page. Write code that demonstrates the mistake and then show the corrected version.

??? success "Solution to Exercise 4"
    A common mistake is misunderstanding array shapes or dtypes. Always check `.shape` and `.dtype` when debugging unexpected results.
