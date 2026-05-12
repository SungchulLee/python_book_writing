# Generic Filter Operations with scipy.ndimage

While convolution applies a fixed kernel operation, `generic_filter()` allows you to apply arbitrary Python functions over neighborhoods. This enables complex, stateful, and custom operations on array data.

!!! tip "Mental Model"
    `generic_filter` is like convolution but with a custom function instead of a fixed kernel: at each position, it collects the neighborhood values into a flat array and passes them to your callback. This unlimited flexibility comes at a cost -- the callback runs in Python, not C -- so use it only when no built-in filter can express your operation.

    Where convolution is restricted to **linear** operators (weighted sums) and
    morphology to **set-based** operators (min, max, connectivity),
    `generic_filter` handles **nonlinear** operators — median, percentile,
    variance, entropy, or any arbitrary computation. It completes the trio:
    linear (convolution) → geometric (morphology) → fully general (generic filter).

## Introduction to Generic Filters

`ndi.generic_filter()` slides a neighborhood window over an array and applies a user-defined function to each neighborhood. The signature is:

```python
result = ndi.generic_filter(input, function, size=None, footprint=None,
                            mode='reflect', cval=0.0, extra_arguments=())
```

The function receives a flattened array of all values in the neighborhood and should return a scalar (or array of scalars for multiple outputs).

!!! note "When to Use Generic Filters"
    Use `generic_filter()` when:

    - Your operation cannot be expressed as a linear convolution
    - You need to apply statistics (median, percentile, min, max)
    - You want to implement custom neighborhood logic
    - You need to track state during filtering

## Footprint vs Size Parameters

You can define neighborhoods in two ways:

**Size parameter**: Creates a rectangular neighborhood
```python
import numpy as np
from scipy import ndimage as ndi

image = np.arange(25).reshape(5, 5)

# Size parameter: 3x3 neighborhood
result = ndi.generic_filter(image, np.min, size=3)
print("Using size=3 (3x3 neighborhood):")
print(result)
```

**Footprint parameter**: Custom neighborhood shape
```python
import numpy as np
from scipy import ndimage as ndi

image = np.arange(25).reshape(5, 5)

# Cross-shaped footprint (diamond)
footprint = np.array([[0, 1, 0],
                      [1, 1, 1],
                      [0, 1, 0]], dtype=bool)

result = ndi.generic_filter(image, np.sum, footprint=footprint)
print("Using cross-shaped footprint:")
print(result)
```

Footprints give fine control over which neighbors participate in the operation. This is essential for defining connectivity in segmentation and morphological operations.

!!! tip "Footprint Choice"

    - **Size**: Simple, rectangular, efficient
    - **Footprint**: Custom shapes, connectivity control, more flexible

## Percentile-Based Neighborhood Operations

A practical application is computing percentiles within neighborhoods, useful for adaptive filtering:

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create a noisy image
np.random.seed(42)
image = np.zeros((100, 100))
image[25:75, 25:75] = 100
image += 30 * np.random.randn(100, 100)

# Function to compute 75th percentile
def percentile_75(neighborhood):
    return np.percentile(neighborhood, 75)

# Apply generic filter
result = ndi.generic_filter(image, percentile_75, size=5)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].imshow(image, cmap='gray')
axes[0].set_title('Noisy Image')

axes[1].imshow(result, cmap='gray')
axes[1].set_title('75th Percentile Filter')

plt.tight_layout()
plt.show()

# Compare with standard filters
median_result = ndi.median_filter(image, size=5)
print("Percentile filter range:", result.min(), "-", result.max())
print("Median filter range:", median_result.min(), "-", median_result.max())
```

!!! note "Why Percentile Filters?"

    - **Median (50th percentile)**: Removes outliers, preserves edges
    - **Higher percentiles**: Remove dark noise, preserve bright features
    - **Lower percentiles**: Remove bright noise
    - Adaptive to local image statistics

## Conway's Game of Life

A classic example of custom neighborhood logic is Conway's Game of Life. Each cell's next state depends on its current state and its 8 neighbors:

```python
import numpy as np
from scipy import ndimage as ndi

# Conway's Game of Life rules:
# 1. A live cell with 2-3 neighbors survives
# 2. A dead cell with exactly 3 neighbors becomes alive
# 3. All other cells die or stay dead

def conway_step(neighborhood):
    """
    Compute next generation of Conway's Game of Life.

    neighborhood: flattened 3x3 array with center cell as neighborhood[4]
    Returns: 1 if cell is alive, 0 if dead
    """
    center = neighborhood[4]
    neighbors_alive = np.sum(neighborhood) - center  # Don't count center

    if center == 1:  # Cell is alive
        return 1 if 2 <= neighbors_alive <= 3 else 0
    else:  # Cell is dead
        return 1 if neighbors_alive == 3 else 0

# Initialize a simple pattern (blinker - period 2)
board = np.zeros((10, 10), dtype=int)
board[5, 4:7] = 1  # Three cells in a row

print("Generation 0:")
print(board)

# Define cross-shaped footprint (8 neighbors + center)
footprint = np.ones((3, 3), dtype=bool)

# Simulate generations
for gen in range(1, 5):
    # Use mode='wrap' for toroidal topology (wraparound edges)
    board = ndi.generic_filter(board, conway_step, footprint=footprint,
                                mode='wrap', cval=0)
    print(f"\nGeneration {gen}:")
    print(board)
```

This example demonstrates several key features:

- **Custom logic**: Pure Python function defining complex rules
- **Neighborhood access**: Function receives all neighbors at once
- **Boundary handling**: `mode='wrap'` creates a toroidal board (edges wrap around)
- **State persistence**: Simple state management during filtering

!!! tip "Why Game of Life?"
    This demonstrates that `generic_filter()` can:

    - Express complex conditional logic
    - Handle non-linear operations
    - Work with custom neighborhood topologies
    - Model cellular automata and pattern propagation

## Efficient Multi-Output Generic Filter

You can return multiple values per neighborhood using a structured array:

```python
import numpy as np
from scipy import ndimage as ndi

image = np.arange(25).reshape(5, 5).astype(float)

# Function returning multiple statistics
def neighborhood_stats(neighborhood):
    """Return min, max, and median"""
    # Note: generic_filter expects scalar output
    # For multiple outputs, use structured approach
    return np.median(neighborhood)

# Better approach: compute separately or use map_array with custom logic
min_filter = ndi.minimum_filter(image, size=3)
max_filter = ndi.maximum_filter(image, size=3)
median_filter = ndi.median_filter(image, size=3)

print("Min values:", min_filter.sum())
print("Max values:", max_filter.sum())
print("Median values:", median_filter.sum())
```

## Advanced: Sobel Magnitude in Single Pass

While convolution-based approaches are typical, generic filters can compute edge magnitude directly:

```python
import numpy as np
from scipy import ndimage as ndi

# Create simple test image
image = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]], dtype=float)

def sobel_magnitude(neighborhood):
    """
    Compute Sobel magnitude from 3x3 neighborhood.
    neighborhood layout:
      [0] [1] [2]
      [3] [4] [5]
      [6] [7] [8]
    """
    # Sobel kernels
    sx = -neighborhood[0] + neighborhood[2] \
         -2*neighborhood[3] + 2*neighborhood[5] \
         -neighborhood[6] + neighborhood[8]

    sy = -neighborhood[0] - 2*neighborhood[1] - neighborhood[2] \
         +neighborhood[6] + 2*neighborhood[7] + neighborhood[8]

    return np.sqrt(sx**2 + sy**2)

result = ndi.generic_filter(image, sobel_magnitude, size=3)
print("Sobel magnitude (single pass):")
print(result)

# Compare with standard approach
sx = ndi.sobel(image, axis=0)
sy = ndi.sobel(image, axis=1)
magnitude_standard = np.sqrt(sx**2 + sy**2)
print("\nStandard Sobel magnitude:")
print(magnitude_standard)
```

## Side-Effect Programming Pattern

Generic filters can accumulate state during execution, useful for building data structures:

```python
import numpy as np
from scipy import ndimage as ndi

image = np.array([[1, 0, 2],
                  [0, 3, 0],
                  [4, 0, 5]], dtype=int)

# Global accumulator (use with caution!)
detected_neighbors = {}

def find_local_max(neighborhood):
    """Find local maxima and track their neighbors"""
    center_val = neighborhood[4]
    max_neighbor = np.max(neighborhood)

    # Simple detection: center equals neighborhood max
    if center_val == max_neighbor and center_val > 0:
        detected_neighbors[len(detected_neighbors)] = {
            'value': center_val,
            'neighbors': neighborhood.tolist()
        }
        return 1.0
    return 0.0

result = ndi.generic_filter(image, find_local_max, size=3)

print("Local maxima found:")
print(result)
print("\nDetected structure:")
for idx, data in detected_neighbors.items():
    print(f"  Maxima {idx}: value={data['value']}")
```

!!! warning "State Accumulation Caution"
    Global state during filtering is useful for analysis but:

    - Can produce unexpected results with boundary modes
    - Makes debugging harder
    - Doesn't parallelize well
    - Use only when truly necessary

## Performance Comparison

Generic filters are more flexible but slower than specialized operations:

```python
import numpy as np
from scipy import ndimage as ndi
import time

image = np.random.rand(500, 500)

# Method 1: Generic filter (flexible, slower)
def custom_median(neighborhood):
    return np.median(neighborhood)

start = time.time()
result1 = ndi.generic_filter(image, custom_median, size=5)
t1 = time.time() - start

# Method 2: Optimized median filter
start = time.time()
result2 = ndi.median_filter(image, size=5)
t2 = time.time() - start

print(f"Generic filter: {t1:.4f}s")
print(f"Optimized median: {t2:.4f}s")
print(f"Slowdown: {t1/t2:.1f}x")
print(f"Results match: {np.allclose(result1, result2)}")
```

## Practical Example: Adaptive Local Contrast

Here's a practical application that enhances local contrast:

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create synthetic image
np.random.seed(42)
image = np.zeros((100, 100))
image[20:80, 20:80] = 0.7
image[40:60, 40:60] = 0.3
image += 0.05 * np.random.randn(100, 100)

def local_contrast(neighborhood):
    """
    Normalize neighborhood values to enhance local contrast.
    Returns normalized center value.
    """
    center = neighborhood[4]
    local_mean = np.mean(neighborhood)
    local_std = np.std(neighborhood)

    if local_std < 1e-6:  # Avoid division by zero
        return 0.5

    # Normalize to [0, 1]
    normalized = (center - local_mean) / (3 * local_std) + 0.5
    return np.clip(normalized, 0, 1)

# Apply adaptive contrast enhancement
enhanced = ndi.generic_filter(image, local_contrast, size=7)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].imshow(image, cmap='gray')
axes[0].set_title('Original Image')

axes[1].imshow(enhanced, cmap='gray')
axes[1].set_title('Adaptive Contrast Enhancement')

plt.tight_layout()
plt.show()
```

## Key Takeaways

`generic_filter()` is a powerful tool for custom neighborhood operations:

- Applies arbitrary Python functions to neighborhoods
- Supports custom footprints for flexible connectivity
- Enables complex logic like cellular automata
- Slower than specialized filters but more flexible
- Useful for percentiles, statistics, and adaptive operations

See also:

- [Convolution and Filtering](convolution_filtering.md) - Linear filtering operations
- [Binary Structures and Morphology](binary_structure.md) - Connectivity and labeling

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
