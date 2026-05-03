# Transpose and Swapaxes

NumPy provides several ways to rearrange array axes.

!!! tip "Mental Model"
    Transposing swaps the axes of an array -- rows become columns and vice versa. For 2D arrays, `.T` is all you need. For higher dimensions, `np.transpose` with an axis order or `np.swapaxes` gives precise control over which axes are exchanged. Transposing returns a view, so no data is copied.

## .T Attribute

### 1. Basic Transpose

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    print("a =")
    print(a)
    print(f"Shape: {a.shape}")
    print()
    print("a.T =")
    print(a.T)
    print(f"Shape: {a.T.shape}")

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[1 2 3]
 [4 5 6]]
Shape: (2, 3)

a.T =
[[1 4]
 [2 5]
 [3 6]]
Shape: (3, 2)
```

### 2. 1D Array

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    
    print(f"a = {a}")
    print(f"a.shape = {a.shape}")
    print(f"a.T = {a.T}")
    print(f"a.T.shape = {a.T.shape}")
    # Note: .T has no effect on 1D arrays

if __name__ == "__main__":
    main()
```

### 3. Returns View

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = a.T
    
    print("Original a:")
    print(a)
    
    # Modify b
    b[0, 0] = 99
    
    print()
    print("After modifying b[0,0]:")
    print("a =")
    print(a)  # a is also modified!

if __name__ == "__main__":
    main()
```

## np.transpose

### 1. Basic Usage

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    b = np.transpose(a)
    
    print("a =")
    print(a)
    print()
    print("np.transpose(a) =")
    print(b)

if __name__ == "__main__":
    main()
```

### 2. Specify Axes Order

```python
import numpy as np

def main():
    a = np.arange(24).reshape(2, 3, 4)
    
    print(f"Original shape: {a.shape}")
    
    # Reverse all axes
    b = np.transpose(a, (2, 1, 0))
    print(f"transpose(a, (2,1,0)) shape: {b.shape}")
    
    # Swap first and last
    c = np.transpose(a, (2, 0, 1))
    print(f"transpose(a, (2,0,1)) shape: {c.shape}")

if __name__ == "__main__":
    main()
```

### 3. 3D Example

```python
import numpy as np

def main():
    # Image batch: (batch, height, width)
    images = np.arange(24).reshape(2, 3, 4)
    
    print("Original shape (batch, height, width):", images.shape)
    print(images)
    print()
    
    # Transpose to (height, width, batch)
    transposed = np.transpose(images, (1, 2, 0))
    print("Transposed shape (height, width, batch):", transposed.shape)

if __name__ == "__main__":
    main()
```

## np.swapaxes

### 1. Swap Two Axes

```python
import numpy as np

def main():
    a = np.arange(24).reshape(2, 3, 4)
    
    print(f"Original shape: {a.shape}")
    
    # Swap axis 0 and 2
    b = np.swapaxes(a, 0, 2)
    print(f"swapaxes(a, 0, 2) shape: {b.shape}")
    
    # Swap axis 1 and 2
    c = np.swapaxes(a, 1, 2)
    print(f"swapaxes(a, 1, 2) shape: {c.shape}")

if __name__ == "__main__":
    main()
```

### 2. Equivalent Operations

```python
import numpy as np

def main():
    a = np.arange(24).reshape(2, 3, 4)
    
    # These are equivalent for 2D
    b = np.array([[1, 2, 3], [4, 5, 6]])
    
    print(f"b.T shape: {b.T.shape}")
    print(f"np.transpose(b) shape: {np.transpose(b).shape}")
    print(f"np.swapaxes(b, 0, 1) shape: {np.swapaxes(b, 0, 1).shape}")

if __name__ == "__main__":
    main()
```

### 3. Image Channel Swap

```python
import numpy as np

def main():
    # Image: (height, width, channels)
    image = np.random.randint(0, 256, (100, 150, 3))
    
    print(f"Original (H, W, C): {image.shape}")
    
    # Convert to (channels, height, width) for PyTorch
    image_chw = np.swapaxes(np.swapaxes(image, 0, 2), 1, 2)
    print(f"CHW format: {image_chw.shape}")
    
    # Simpler with transpose
    image_chw2 = np.transpose(image, (2, 0, 1))
    print(f"Using transpose: {image_chw2.shape}")

if __name__ == "__main__":
    main()
```

## np.moveaxis

### 1. Move Single Axis

```python
import numpy as np

def main():
    a = np.arange(24).reshape(2, 3, 4)
    
    print(f"Original shape: {a.shape}")
    
    # Move axis 0 to position 2
    b = np.moveaxis(a, 0, 2)
    print(f"moveaxis(a, 0, 2) shape: {b.shape}")
    
    # Move axis 2 to position 0
    c = np.moveaxis(a, 2, 0)
    print(f"moveaxis(a, 2, 0) shape: {c.shape}")

if __name__ == "__main__":
    main()
```

### 2. Move Multiple Axes

```python
import numpy as np

def main():
    a = np.arange(120).reshape(2, 3, 4, 5)
    
    print(f"Original shape: {a.shape}")
    
    # Move axes 0,1 to positions 2,3
    b = np.moveaxis(a, [0, 1], [2, 3])
    print(f"moveaxis(a, [0,1], [2,3]) shape: {b.shape}")

if __name__ == "__main__":
    main()
```

### 3. Channel Last to First

```python
import numpy as np

def main():
    # Batch of images: (batch, height, width, channels)
    images = np.random.randint(0, 256, (32, 64, 64, 3))
    
    print(f"Original (NHWC): {images.shape}")
    
    # Convert to (batch, channels, height, width)
    images_nchw = np.moveaxis(images, -1, 1)
    print(f"NCHW format: {images_nchw.shape}")

if __name__ == "__main__":
    main()
```

## np.rollaxis

### 1. Roll Axis to Position

```python
import numpy as np

def main():
    a = np.arange(24).reshape(2, 3, 4)
    
    print(f"Original shape: {a.shape}")
    
    # Roll axis 2 to position 0
    b = np.rollaxis(a, 2)
    print(f"rollaxis(a, 2) shape: {b.shape}")
    
    # Roll axis 2 to position 1
    c = np.rollaxis(a, 2, 1)
    print(f"rollaxis(a, 2, 1) shape: {c.shape}")

if __name__ == "__main__":
    main()
```

### 2. Prefer moveaxis

`np.moveaxis` is more intuitive than `np.rollaxis`.

## Method vs Attribute

### 1. Array Method

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    # Using method
    b = a.transpose()
    print(f"a.transpose() shape: {b.shape}")
    
    # With axes
    c = np.arange(24).reshape(2, 3, 4)
    d = c.transpose(2, 0, 1)
    print(f"c.transpose(2,0,1) shape: {d.shape}")

if __name__ == "__main__":
    main()
```

### 2. Swapaxes Method

```python
import numpy as np

def main():
    a = np.arange(24).reshape(2, 3, 4)
    
    # Using method
    b = a.swapaxes(0, 2)
    print(f"a.swapaxes(0, 2) shape: {b.shape}")

if __name__ == "__main__":
    main()
```

## Matrix Operations

### 1. Matrix Transpose

```python
import numpy as np

def main():
    A = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    print("A =")
    print(A)
    print()
    print("A^T =")
    print(A.T)
    print()
    
    # (A^T)^T = A
    print("(A^T)^T =")
    print(A.T.T)

if __name__ == "__main__":
    main()
```

### 2. Symmetric Matrix

```python
import numpy as np

def main():
    A = np.array([[1, 2, 3],
                  [2, 4, 5],
                  [3, 5, 6]])
    
    print("A =")
    print(A)
    print()
    print("A^T =")
    print(A.T)
    print()
    print(f"Is symmetric (A == A^T): {np.array_equal(A, A.T)}")

if __name__ == "__main__":
    main()
```

### 3. Transpose Properties

```python
import numpy as np

def main():
    A = np.array([[1, 2], [3, 4]])
    B = np.array([[5, 6], [7, 8]])
    
    # (AB)^T = B^T A^T
    left = (A @ B).T
    right = B.T @ A.T
    
    print("(AB)^T =")
    print(left)
    print()
    print("B^T A^T =")
    print(right)
    print()
    print(f"Equal: {np.array_equal(left, right)}")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Batch Processing

```python
import numpy as np

def main():
    # Data: (samples, features)
    data = np.array([[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]])
    
    # Weights: (features, outputs)
    weights = np.array([[0.1, 0.2],
                        [0.3, 0.4],
                        [0.5, 0.6]])
    
    # Forward pass
    output = data @ weights
    
    print(f"Data shape: {data.shape}")
    print(f"Weights shape: {weights.shape}")
    print(f"Output shape: {output.shape}")

if __name__ == "__main__":
    main()
```

### 2. Covariance Matrix

```python
import numpy as np

def main():
    # Data: (samples, features)
    X = np.random.randn(100, 3)
    X_centered = X - X.mean(axis=0)
    
    # Covariance: X^T X / (n-1)
    cov = X_centered.T @ X_centered / (len(X) - 1)
    
    print("Covariance matrix:")
    print(cov.round(3))
    print()
    print("Using np.cov:")
    print(np.cov(X.T).round(3))

if __name__ == "__main__":
    main()
```

### 3. Gram Matrix

```python
import numpy as np

def main():
    # Feature matrix
    F = np.random.randn(4, 6)
    
    # Gram matrix: F @ F^T
    gram = F @ F.T
    
    print(f"F shape: {F.shape}")
    print(f"Gram matrix shape: {gram.shape}")
    print()
    print("Gram matrix:")
    print(gram.round(3))

if __name__ == "__main__":
    main()
```

!!! tip "Unifying Idea"
    All axis operations — `.T`, `transpose`, `swapaxes`, `moveaxis` — are **permutations of dimensions**. They rearrange which axis is which without touching the underlying data (they return views). Once you see axis manipulation as dimension permutation, the entire API collapses to one concept.

## Summary Table

### 1. Transpose Functions

| Method | Description |
|:-------|:------------|
| `a.T` | Transpose (attribute) |
| `np.transpose(a)` | Transpose (function) |
| `np.transpose(a, axes)` | Permute axes |
| `a.transpose(axes)` | Permute axes (method) |

### 2. Axis Manipulation

| Function | Description |
|:---------|:------------|
| `np.swapaxes(a, ax1, ax2)` | Swap two axes |
| `np.moveaxis(a, src, dst)` | Move axis to new position |
| `np.rollaxis(a, axis, start)` | Roll axis (legacy) |

### 3. Key Points

- `.T` and `transpose()` return views, not copies
- For 1D arrays, `.T` has no effect
- Use `np.moveaxis` for clarity over `np.rollaxis`

---

## Exercises

**Exercise 1.**
Create a 3x5 matrix `A`. Compute its transpose using both `A.T` and `np.transpose(A)`. Verify both produce the same `(5, 3)` result and that `(A.T).T` returns the original shape.

??? success "Solution to Exercise 1"

        import numpy as np

        A = np.random.randn(3, 5)
        T1 = A.T
        T2 = np.transpose(A)
        print(f"A.T shape: {T1.shape}")  # (5, 3)
        print(f"Same: {np.array_equal(T1, T2)}")
        print(f"(A.T).T shape: {T1.T.shape}")  # (3, 5)

---

**Exercise 2.**
Create a 3D array of shape `(2, 3, 4)`. Use `np.transpose(a, axes=(1, 0, 2))` to swap the first two axes. Print the resulting shape and verify it is `(3, 2, 4)`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(24).reshape(2, 3, 4)
        b = np.transpose(a, axes=(1, 0, 2))
        print(f"Original shape: {a.shape}")    # (2, 3, 4)
        print(f"Transposed shape: {b.shape}")  # (3, 2, 4)

---

**Exercise 3.**
Verify the matrix identity $(AB)^T = B^T A^T$ for random matrices `A` of shape `(3, 4)` and `B` of shape `(4, 2)`.

??? success "Solution to Exercise 3"

        import numpy as np

        A = np.random.randn(3, 4)
        B = np.random.randn(4, 2)
        lhs = (A @ B).T
        rhs = B.T @ A.T
        print(f"(AB)^T == B^T A^T: {np.allclose(lhs, rhs)}")
