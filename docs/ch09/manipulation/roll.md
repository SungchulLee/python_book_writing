# np.roll

The `np.roll()` function shifts array elements along an axis with circular wrapping.

!!! tip "Mental Model"
    `np.roll` shifts every element by a fixed offset and wraps elements that fall off one end back to the other, like a circular conveyor belt. Positive shifts move elements to the right (or down), negative shifts move left (or up). No data is lost -- the array is just rotated in place along the chosen axis.

!!! note "Why Roll Exists"
    Circular shifting arises naturally in domains with **periodic boundary conditions**: FFT frequency bins wrap around, time-series data has seasonal cycles, and image processing uses circular convolution. `np.roll` provides this operation directly on arrays without manual index arithmetic. It fits into the manipulation system as the **shift** operation — alongside combine (concatenate), divide (split), and reorder (transpose).

## Basic Concept

### 1D Array Rolling

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(np.roll(arr, 2))   # [4, 5, 1, 2, 3] - shift right by 2
print(np.roll(arr, -2))  # [3, 4, 5, 1, 2] - shift left by 2
```

## Image Rolling

### Basic Example

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(12, 3))

    ax0.imshow(img)
    ax1.imshow(np.roll(img, 50, axis=0))  # Roll along rows (vertical)
    ax2.imshow(np.roll(img, 50, axis=1))  # Roll along columns (horizontal)

    for ax in (ax0, ax1, ax2):
        ax.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

## Axis Reference

### Roll Directions

| Axis | Direction | Effect |
|------|-----------|--------|
| 0 | Vertical | Rows wrap top-to-bottom |
| 1 | Horizontal | Columns wrap left-to-right |

### Positive vs Negative Shift

```python
import matplotlib.pyplot as plt
import numpy as np
import PIL
import urllib

url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
img = np.array(PIL.Image.open(urllib.request.urlopen(url)))

fig, axes = plt.subplots(2, 3, figsize=(12, 8))

# Row 1: Horizontal rolling (axis=1)
axes[0, 0].imshow(np.roll(img, -100, axis=1))
axes[0, 0].set_title('roll(img, -100, axis=1)')

axes[0, 1].imshow(img)
axes[0, 1].set_title('Original')

axes[0, 2].imshow(np.roll(img, 100, axis=1))
axes[0, 2].set_title('roll(img, 100, axis=1)')

# Row 2: Vertical rolling (axis=0)
axes[1, 0].imshow(np.roll(img, -100, axis=0))
axes[1, 0].set_title('roll(img, -100, axis=0)')

axes[1, 1].imshow(img)
axes[1, 1].set_title('Original')

axes[1, 2].imshow(np.roll(img, 100, axis=0))
axes[1, 2].set_title('roll(img, 100, axis=0)')

for ax in axes.flat:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

## Multi-Axis Rolling

### Roll Both Axes

```python
import matplotlib.pyplot as plt
import numpy as np

# Roll in both directions
rolled_both = np.roll(np.roll(img, 50, axis=0), 75, axis=1)

# Or use tuple for multi-axis roll
rolled_tuple = np.roll(img, (50, 75), axis=(0, 1))

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

axes[0].imshow(img)
axes[0].set_title('Original')

axes[1].imshow(rolled_both)
axes[1].set_title('Sequential Roll')

axes[2].imshow(rolled_tuple)
axes[2].set_title('Tuple Roll (50, 75)')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

## Animation Effect

### Creating Rolling Animation Frames

```python
import matplotlib.pyplot as plt
import numpy as np

def create_roll_frames(img, n_frames=10, axis=1):
    """Create frames for rolling animation."""
    step = img.shape[axis] // n_frames
    frames = []
    for i in range(n_frames):
        frames.append(np.roll(img, i * step, axis=axis))
    return frames

frames = create_roll_frames(img, n_frames=5, axis=1)

fig, axes = plt.subplots(1, 5, figsize=(15, 3))
for ax, frame in zip(axes, frames):
    ax.imshow(frame)
    ax.axis('off')
plt.tight_layout()
plt.show()
```

!!! info "Where Rolling Appears"
    Circular shifts are not just an image trick. They show up in **periodic boundary conditions** (physics simulations), **signal processing** (aligning waveforms), and **FFT work** (centering the zero-frequency component with `np.fft.fftshift`, which is roll under the hood).

## Practical Applications

### Seamless Texture Check

```python
import matplotlib.pyplot as plt
import numpy as np

def check_seamless(img, shift_fraction=0.5):
    """Check if texture tiles seamlessly."""
    h, w = img.shape[:2]
    
    rolled_h = np.roll(img, int(h * shift_fraction), axis=0)
    rolled_w = np.roll(img, int(w * shift_fraction), axis=1)
    rolled_both = np.roll(np.roll(img, int(h * shift_fraction), axis=0),
                          int(w * shift_fraction), axis=1)
    
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    
    axes[0, 0].imshow(img)
    axes[0, 0].set_title('Original')
    
    axes[0, 1].imshow(rolled_w)
    axes[0, 1].set_title('Horizontal Roll')
    
    axes[1, 0].imshow(rolled_h)
    axes[1, 0].set_title('Vertical Roll')
    
    axes[1, 1].imshow(rolled_both)
    axes[1, 1].set_title('Both Axes Roll')
    
    for ax in axes.flat:
        ax.axis('off')
    plt.tight_layout()
    plt.show()

check_seamless(img)
```

### Centering Object

```python
import matplotlib.pyplot as plt
import numpy as np

def center_object(img, current_center, target_center=None):
    """Roll image to center an object."""
    h, w = img.shape[:2]
    if target_center is None:
        target_center = (h // 2, w // 2)
    
    shift_y = target_center[0] - current_center[0]
    shift_x = target_center[1] - current_center[1]
    
    return np.roll(np.roll(img, shift_y, axis=0), shift_x, axis=1)

# Example: move object from (100, 150) to center
centered = center_object(img, current_center=(100, 150))

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(img)
axes[0].set_title('Original')
axes[1].imshow(centered)
axes[1].set_title('Centered')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

### Panorama Creation

```python
import matplotlib.pyplot as plt
import numpy as np

def create_panorama_effect(img, repetitions=3):
    """Create a panorama by tiling and rolling."""
    # Tile horizontally
    tiled = np.tile(img, (1, repetitions, 1))
    
    # Show different roll positions
    fig, axes = plt.subplots(3, 1, figsize=(15, 9))
    
    for i, ax in enumerate(axes):
        shift = i * img.shape[1] // 2
        rolled = np.roll(tiled, shift, axis=1)
        # Crop to original width
        cropped = rolled[:, :img.shape[1]*2]
        ax.imshow(cropped)
        ax.set_title(f'Pan position {i+1}')
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

create_panorama_effect(img)
```

## Comparison with Other Operations

### Roll vs Slice

```python
import matplotlib.pyplot as plt
import numpy as np

shift = 100

fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Original
axes[0].imshow(img)
axes[0].set_title('Original')

# Roll (circular - wraps around)
axes[1].imshow(np.roll(img, shift, axis=1))
axes[1].set_title('Roll (circular)')

# Slice (non-circular - loses data)
sliced = np.concatenate([img[:, shift:], np.zeros_like(img[:, :shift])], axis=1)
axes[2].imshow(sliced.astype(np.uint8))
axes[2].set_title('Slice (loses data)')

for ax in axes:
    ax.axis('off')
plt.tight_layout()
plt.show()
```

## Grid of Roll Amounts

### Various Shift Values

```python
import matplotlib.pyplot as plt
import numpy as np

shifts = [0, 50, 100, 150, 200]

fig, axes = plt.subplots(2, 5, figsize=(15, 6))

# Horizontal rolls
for ax, shift in zip(axes[0], shifts):
    ax.imshow(np.roll(img, shift, axis=1))
    ax.set_title(f'axis=1, shift={shift}')
    ax.axis('off')

# Vertical rolls
for ax, shift in zip(axes[1], shifts):
    ax.imshow(np.roll(img, shift, axis=0))
    ax.set_title(f'axis=0, shift={shift}')
    ax.axis('off')

plt.tight_layout()
plt.show()
```

---

## Exercises

**Exercise 1.**
Create `a = np.arange(10)`. Roll it by 3 positions and by -2 positions. Verify that rolling by `n` then by `-n` returns the original array.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(10)
        rolled = np.roll(a, 3)
        unrolled = np.roll(rolled, -3)
        print(f"Original: {a}")
        print(f"Rolled +3: {rolled}")
        print(f"Rolled back: {unrolled}")
        print(f"Match: {np.array_equal(a, unrolled)}")

---

**Exercise 2.**
Create a 4x4 matrix and roll it by 1 along axis 0 (shift rows down) and by -1 along axis 1 (shift columns left). Print the results.

??? success "Solution to Exercise 2"

        import numpy as np

        M = np.arange(16).reshape(4, 4)
        print(f"Original:\n{M}")
        print(f"Roll rows +1:\n{np.roll(M, 1, axis=0)}")
        print(f"Roll cols -1:\n{np.roll(M, -1, axis=1)}")

---

**Exercise 3.**
Implement a circular convolution of two 1D arrays using `np.roll`: given `a = np.array([1, 2, 3, 0, 0])` and `b = np.array([1, 1, 0, 0, 0])`, compute the circular convolution by summing `a * np.roll(b, k)` for each shift `k`. Compare with `np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real`.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.array([1, 2, 3, 0, 0], dtype=float)
        b = np.array([1, 1, 0, 0, 0], dtype=float)

        # Circular convolution via roll
        result = np.zeros(len(a))
        for k in range(len(a)):
            result += a[k] * np.roll(b, k)

        # FFT-based circular convolution
        result_fft = np.fft.ifft(np.fft.fft(a) * np.fft.fft(b)).real

        print(f"Roll method: {result}")
        print(f"FFT method:  {result_fft}")
        print(f"Match: {np.allclose(result, result_fft)}")
