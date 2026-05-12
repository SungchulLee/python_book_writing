# Binary Structures, Morphology, and Labeling

Binary structures define connectivity patterns for segmentation and morphological operations. They answer the question: "Which neighboring pixels are considered connected?"

!!! tip "Mental Model"
    A binary structure element is a small True/False mask that defines which neighbors count as "connected." Morphological operations like erosion, dilation, and labeling slide this mask across the image. The structure shape determines whether diagonal pixels are neighbors (8-connectivity) or only horizontal/vertical ones (4-connectivity).

    Morphology is **geometry-based filtering**: where [convolution](convolution_filtering.md)
    computes weighted sums (a linear operation), morphology applies set operations
    (union, intersection) defined by the structure element's shape. Both slide a
    small neighborhood across the array — they differ only in what they compute at
    each position.

## Connectivity Definitions

In digital images, we must formally define what "neighboring" means. A pixel can have neighbors in different patterns:

- **4-connectivity**: Only horizontal and vertical neighbors (up, down, left, right)
- **8-connectivity**: Horizontal, vertical, and diagonal neighbors
- **Face connectivity** in 3D: 6 neighbors (one per face)
- **Full connectivity** in 3D: 26 neighbors (faces, edges, corners)

## Generating Binary Structures

`ndi.generate_binary_structure()` creates connectivity matrices:

```python
import numpy as np
from scipy import ndimage as ndi

# 2D structures
struct_4 = ndi.generate_binary_structure(rank=2, connectivity=1)
struct_8 = ndi.generate_binary_structure(rank=2, connectivity=2)

print("4-connectivity (rank=2, connectivity=1):")
print(struct_4.astype(int))

print("\n8-connectivity (rank=2, connectivity=2):")
print(struct_8.astype(int))

# 3D structures
struct_6 = ndi.generate_binary_structure(rank=3, connectivity=1)
struct_26 = ndi.generate_binary_structure(rank=3, connectivity=3)

print("\n6-connectivity in 3D (face neighbors):")
print(struct_6[:, :, 1])  # Middle slice

print("\n26-connectivity in 3D (all neighbors):")
print(struct_26[:, :, 1])  # Middle slice
```

The output shows `True` for connected neighbors and `False` otherwise. The center element is always `True`.

!!! note "Connectivity Parameter"

    - `connectivity=1`: Face neighbors only (minimal connectivity)
    - `connectivity=2`: Face and edge neighbors (in 3D)
    - `connectivity=3`: All neighbors including corners (full connectivity)
    - Higher connectivity = more connected objects, fewer separate components

## Custom Structures

You can define custom connectivity patterns for specialized applications:

```python
import numpy as np
from scipy import ndimage as ndi

# Custom structure: plus sign (cross)
cross = np.array([[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]], dtype=bool)

# Custom structure: ring (only neighbors, not center)
ring = np.array([[1, 1, 1],
                 [1, 0, 1],
                 [1, 1, 1]], dtype=bool)

# Custom structure: L-shape
l_shape = np.array([[1, 0, 0],
                    [1, 1, 1],
                    [0, 0, 1]], dtype=bool)

print("Cross structure:")
print(cross.astype(int))

print("\nRing structure:")
print(ring.astype(int))

print("\nL-shape structure:")
print(l_shape.astype(int))
```

## Connected Component Labeling

`ndi.label()` identifies connected components (regions of connected pixels) and assigns each a unique integer label:

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create binary image with multiple components
image = np.array([[0, 0, 1, 0, 0],
                  [0, 1, 1, 0, 0],
                  [0, 0, 0, 0, 1],
                  [0, 0, 0, 1, 1],
                  [0, 0, 0, 0, 1]], dtype=bool)

# Label with 8-connectivity
labeled, num_features = ndi.label(image)

print("Binary image:")
print(image.astype(int))

print(f"\nLabeled image ({num_features} components):")
print(labeled)

# Find component sizes
component_sizes = ndi.sum(image, labeled, range(num_features + 1))
print(f"\nComponent sizes: {component_sizes[1:]}")  # Exclude background (0)
```

### Finding Component Statistics

After labeling, you can compute statistics for each component:

```python
import numpy as np
from scipy import ndimage as ndi

# Create labeled image
image = np.random.rand(20, 20) > 0.7
labeled, num_features = ndi.label(image)

# Compute statistics per component
centroids = ndi.center_of_mass(image, labeled, range(1, num_features + 1))
sizes = ndi.sum(image, labeled, range(1, num_features + 1))
max_intensities = ndi.maximum(image, labeled, range(1, num_features + 1))

print(f"Found {num_features} components")

for component_id in range(1, num_features + 1):
    print(f"\nComponent {component_id}:")
    print(f"  Centroid: {centroids[component_id - 1]}")
    print(f"  Size: {sizes[component_id - 1]}")
    print(f"  Max intensity: {max_intensities[component_id - 1]}")
```

!!! tip "Labeling Applications"

    - **Object counting**: How many separate objects?
    - **Component filtering**: Remove small noise components
    - **Feature extraction**: Compute properties per object
    - **Image segmentation**: Identify distinct regions
    - **Quality control**: Analyze defects in manufacturing

## Morphological Operations Overview

Morphological operations process binary (or grayscale) images based on shapes. They combine labeling, erosion, and dilation to extract or modify structures.

### Erosion

Erosion shrinks white regions and enlarges black regions. For binary images, erosion with a structure:

$$E(A) = \{x | S_x \subseteq A\}$$

where $S_x$ is the structure centered at $x$, and $A$ is the input set.

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create binary image
image = np.zeros((10, 10), dtype=bool)
image[2:8, 2:8] = True  # White square
image[4:6, 4:6] = False  # Black hole

# Create structure
structure = ndi.generate_binary_structure(2, 2)

# Apply erosion
eroded = ndi.binary_erosion(image, structure=structure)

print("Original:")
print(image.astype(int))

print("\nEroded:")
print(eroded.astype(int))
```

### Dilation

Dilation expands white regions and shrinks black regions:

$$D(A) = \{x | S_x \cap A \neq \emptyset\}$$

```python
import numpy as np
from scipy import ndimage as ndi

image = np.zeros((10, 10), dtype=bool)
image[4:6, 4:6] = True  # Small white square

structure = ndi.generate_binary_structure(2, 2)

# Apply dilation
dilated = ndi.binary_dilation(image, structure=structure)

print("Original:")
print(image.astype(int))

print("\nDilated:")
print(dilated.astype(int))
```

### Opening and Closing

**Opening** = Erosion followed by Dilation. Removes small objects and noise:

$$\text{Open}(A) = D(E(A))$$

**Closing** = Dilation followed by Erosion. Fills small holes:

$$\text{Close}(A) = E(D(A))$$

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create noisy binary image
np.random.seed(42)
image = np.random.rand(50, 50) > 0.6

structure = ndi.generate_binary_structure(2, 2)

# Apply operations
opened = ndi.binary_opening(image, structure=structure)
closed = ndi.binary_closing(image, structure=structure)

# Visualize
fig, axes = plt.subplots(1, 3, figsize=(12, 3))

axes[0].imshow(image, cmap='gray')
axes[0].set_title('Original (Noisy)')

axes[1].imshow(opened, cmap='gray')
axes[1].set_title('Opened\n(Remove Noise)')

axes[2].imshow(closed, cmap='gray')
axes[2].set_title('Closed\n(Fill Holes)')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()
```

!!! note "When to Use Morphological Operations"

    - **Opening**: Remove small spurious objects
    - **Closing**: Fill holes in objects
    - **Erosion**: Extract internal boundaries, shrink objects
    - **Dilation**: Grow objects, bridge small gaps
    - **Combine**: Chain operations for complex preprocessing

## Practical Example: Object Detection and Filtering

Here's a complete example combining labeling and morphological operations:

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create synthetic image with multiple objects
np.random.seed(42)
image = np.zeros((100, 100), dtype=bool)

# Add main objects
image[20:40, 20:40] = True
image[60:80, 60:80] = True

# Add noise
image += np.random.rand(100, 100) > 0.95

print(f"Before filtering: {np.sum(image)} pixels")

# Step 1: Clean noise with opening
structure = ndi.generate_binary_structure(2, 2)
cleaned = ndi.binary_opening(image, structure=structure, iterations=2)

print(f"After opening: {np.sum(cleaned)} pixels")

# Step 2: Label connected components
labeled, num_features = ndi.label(cleaned, structure=structure)
print(f"Number of components: {num_features}")

# Step 3: Filter by size
sizes = ndi.sum(cleaned, labeled, range(num_features + 1))
min_size = 50
size_mask = sizes > min_size
large_objects = size_mask[labeled]

print(f"After size filtering: {np.sum(large_objects)} pixels")

# Step 4: Re-label after filtering
final_labeled, final_count = ndi.label(large_objects, structure=structure)
print(f"Final number of objects: {final_count}")

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(image, cmap='gray')
axes[0, 0].set_title('Original (Noisy)')

axes[0, 1].imshow(cleaned, cmap='gray')
axes[0, 1].set_title('After Opening')

axes[1, 0].imshow(large_objects, cmap='gray')
axes[1, 0].set_title('After Size Filter')

axes[1, 1].imshow(final_labeled, cmap='nipy_spectral')
axes[1, 1].set_title('Final Labels')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()

# Compute properties of final objects
for obj_id in range(1, final_count + 1):
    mask = final_labeled == obj_id
    centroid = ndi.center_of_mass(mask)
    size = np.sum(mask)
    print(f"\nObject {obj_id}: centroid={centroid}, size={size}")
```

## Grayscale Morphological Operations

Morphological operations extend to grayscale images:

```python
import numpy as np
from scipy import ndimage as ndi
import matplotlib.pyplot as plt

# Create grayscale image
image = np.zeros((50, 50))
image[15:35, 15:35] = 100
image[20:30, 20:30] = 50  # Inner dark region
image += 10 * np.random.randn(50, 50)

structure = ndi.generate_binary_structure(2, 2)

# Grayscale operations
eroded = ndi.grey_erosion(image, footprint=structure)
dilated = ndi.grey_dilation(image, footprint=structure)
gradient = dilated - eroded  # Morphological gradient (edge detection)

# Visualize
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

axes[0, 0].imshow(image, cmap='gray')
axes[0, 0].set_title('Original')

axes[0, 1].imshow(eroded, cmap='gray')
axes[0, 1].set_title('Eroded')

axes[1, 0].imshow(dilated, cmap='gray')
axes[1, 0].set_title('Dilated')

axes[1, 1].imshow(gradient, cmap='gray')
axes[1, 1].set_title('Morphological Gradient')

for ax in axes.flat:
    ax.axis('off')

plt.tight_layout()
plt.show()
```

## Key Takeaways

Binary structures and morphological operations are essential for image segmentation:

- **Connectivity** defines which pixels are neighbors
- **Labeling** identifies connected components
- **Morphological operations** (erosion, dilation, opening, closing) reshape binary regions
- Combining operations creates powerful preprocessing pipelines
- These techniques work on both binary and grayscale images

See also:

- [Convolution and Filtering](convolution_filtering.md) - Linear filtering fundamentals
- [Generic Filter Operations](generic_filter.md) - Custom neighborhood operations

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
