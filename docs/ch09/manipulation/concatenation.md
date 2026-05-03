# Concatenation

NumPy provides several functions to join arrays together. Concatenation is part of a broader system of **structure operations** — ways to rearrange data without changing the values themselves:

| Category | Operations | What it does |
|---|---|---|
| Combine | `concatenate`, `stack` | Join arrays along an axis |
| Divide | `split`, `array_split` | Partition an array into pieces |
| Reorder | `transpose`, `swapaxes`, `moveaxis` | Permute axis order |
| Shift | `roll` | Circular element shift |
| Traverse | iteration (`nditer`, `ndenumerate`) | Walk elements (last resort) |

!!! tip "Mental Model"
    `np.concatenate` glues arrays end-to-end along an existing axis, while `np.stack` creates a new axis and stacks arrays along it. The key rule: all arrays must have matching shapes on every axis except the one being joined. Think of concatenation as appending rows or columns, and stacking as adding a new "batch" dimension.

!!! note "Function Hierarchy"
    NumPy's joining functions form three layers:

    - **Core** — `np.concatenate` (existing axis) and `np.stack` (new axis)
    - **Convenience** — `np.vstack`, `np.hstack`, `np.dstack` (axis-specific shortcuts)
    - **Syntactic sugar** — `np.r_`, `np.c_` (index-expression shorthand)

    Start with core, reach for convenience when the axis is obvious, use sugar in interactive work.

## np.concatenate

### 1. Along axis=0

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    c = np.concatenate([a, b], axis=0)
    
    print("a =")
    print(a)
    print()
    print("b =")
    print(b)
    print()
    print("np.concatenate([a, b], axis=0) =")
    print(c)

if __name__ == "__main__":
    main()
```

**Output:**

```
np.concatenate([a, b], axis=0) =
[[1 2]
 [3 4]
 [5 6]
 [7 8]]
```

### 2. Along axis=1

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    c = np.concatenate([a, b], axis=1)
    
    print("np.concatenate([a, b], axis=1) =")
    print(c)

if __name__ == "__main__":
    main()
```

### 3. Multiple Arrays

```python
import numpy as np

def main():
    a = np.zeros((2, 3, 4))
    b = np.zeros((2, 3, 4))
    c = np.zeros((2, 3, 4))
    
    # Concatenate along different axes
    d0 = np.concatenate([a, b, c], axis=0)
    d1 = np.concatenate([a, b, c], axis=1)
    d2 = np.concatenate([a, b, c], axis=-1)
    
    print(f"Original shape: {a.shape}")
    print(f"axis=0 shape: {d0.shape}")
    print(f"axis=1 shape: {d1.shape}")
    print(f"axis=-1 shape: {d2.shape}")

if __name__ == "__main__":
    main()
```

### 4. axis=None (Flatten)

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    # Flatten and concatenate
    c = np.concatenate([a, b], axis=None)
    
    print(f"Result: {c}")
    print(f"Shape: {c.shape}")

if __name__ == "__main__":
    main()
```

## np.vstack

### 1. Vertical Stack

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    c = np.vstack([a, b])
    
    print(f"a = {a}")
    print(f"b = {b}")
    print()
    print("np.vstack([a, b]) =")
    print(c)

if __name__ == "__main__":
    main()
```

### 2. Equivalent to concatenate axis=0

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    c1 = np.vstack([a, b])
    c2 = np.concatenate([a, b], axis=0)
    
    print(f"vstack shape: {c1.shape}")
    print(f"concatenate axis=0 shape: {c2.shape}")
    print(f"Equal: {np.array_equal(c1, c2)}")

if __name__ == "__main__":
    main()
```

### 3. 1D to 2D

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # vstack converts 1D to row vectors
    c = np.vstack([a, b])
    
    print(f"a shape: {a.shape}")
    print(f"Result shape: {c.shape}")
    print(c)

if __name__ == "__main__":
    main()
```

## np.hstack

### 1. Horizontal Stack

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    c = np.hstack([a, b])
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"np.hstack([a, b]) = {c}")

if __name__ == "__main__":
    main()
```

### 2. 2D Arrays

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    c = np.hstack([a, b])
    
    print("np.hstack([a, b]) =")
    print(c)

if __name__ == "__main__":
    main()
```

### 3. Equivalent to concatenate axis=1

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    c1 = np.hstack([a, b])
    c2 = np.concatenate([a, b], axis=1)
    
    print(f"hstack shape: {c1.shape}")
    print(f"concatenate axis=1 shape: {c2.shape}")
    print(f"Equal: {np.array_equal(c1, c2)}")

if __name__ == "__main__":
    main()
```

## np.dstack

### 1. Depth Stack

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    c = np.dstack([a, b])
    
    print(f"a shape: {a.shape}")
    print(f"b shape: {b.shape}")
    print(f"dstack shape: {c.shape}")
    print()
    print("np.dstack([a, b]) =")
    print(c)

if __name__ == "__main__":
    main()
```

### 2. Stack Along axis=2

```python
import numpy as np

def main():
    a = np.ones((2, 3))
    b = np.zeros((2, 3))
    
    c = np.dstack([a, b])
    
    print(f"Result shape: {c.shape}")
    print(f"c[:,:,0] (from a):")
    print(c[:, :, 0])
    print(f"c[:,:,1] (from b):")
    print(c[:, :, 1])

if __name__ == "__main__":
    main()
```

## np.stack

### 1. Stack Along New Axis

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # Stack creates new axis
    c0 = np.stack([a, b], axis=0)
    c1 = np.stack([a, b], axis=1)
    
    print(f"a shape: {a.shape}")
    print(f"stack axis=0 shape: {c0.shape}")
    print(f"stack axis=1 shape: {c1.shape}")

if __name__ == "__main__":
    main()
```

### 2. Difference from concatenate

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[5, 6], [7, 8]])
    
    # concatenate joins along existing axis
    c_concat = np.concatenate([a, b], axis=0)
    
    # stack creates new axis
    c_stack = np.stack([a, b], axis=0)
    
    print(f"concatenate shape: {c_concat.shape}")
    print(f"stack shape: {c_stack.shape}")

if __name__ == "__main__":
    main()
```

### 3. Batch Creation

```python
import numpy as np

def main():
    # Create batch from individual samples
    samples = [np.random.randn(28, 28) for _ in range(32)]
    
    batch = np.stack(samples, axis=0)
    
    print(f"Number of samples: {len(samples)}")
    print(f"Sample shape: {samples[0].shape}")
    print(f"Batch shape: {batch.shape}")

if __name__ == "__main__":
    main()
```

## np.r_ and np.c_

### 1. np.r_ (Row-wise)

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # Same as hstack for 1D
    c = np.r_[a, b]
    
    print(f"np.r_[a, b] = {c}")

if __name__ == "__main__":
    main()
```

### 2. np.c_ (Column-wise)

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # Creates column vectors and stacks horizontally
    c = np.c_[a, b]
    
    print("np.c_[a, b] =")
    print(c)

if __name__ == "__main__":
    main()
```

### 3. Convenience Syntax

```python
import numpy as np

def main():
    # Range syntax
    print(f"np.r_[1:5] = {np.r_[1:5]}")
    print(f"np.r_[1:5, 10:15] = {np.r_[1:5, 10:15]}")
    
    # Mix arrays and ranges
    a = np.array([100, 200])
    print(f"np.r_[a, 1:4] = {np.r_[a, 1:4]}")

if __name__ == "__main__":
    main()
```

## Summary Table

### 1. Concatenation Equivalences

| Long Form | Short Form |
|:----------|:-----------|
| `np.concatenate([a,b], axis=0)` | `np.vstack([a,b])` |
| `np.concatenate([a,b], axis=1)` | `np.hstack([a,b])` |
| `np.concatenate([a,b], axis=2)` | `np.dstack([a,b])` |

### 2. Stack vs Concatenate

| Function | Behavior |
|:---------|:---------|
| `concatenate` | Joins along existing axis |
| `stack` | Creates new axis, then joins |
| `vstack` | Vertical (axis=0) |
| `hstack` | Horizontal (axis=1 for 2D) |
| `dstack` | Depth (axis=2) |

### 3. Quick Reference

| Function | Shorthand |
|:---------|:----------|
| `np.concatenate([a, b], axis=0)` | `np.r_[a, b]` |
| `np.column_stack([a, b])` | `np.c_[a, b]` |

## Applications

### 1. Feature Engineering

```python
import numpy as np

def main():
    # Original features
    X = np.array([[1, 2], [3, 4], [5, 6]])
    
    # Add polynomial features
    X_squared = X ** 2
    
    # Combine features
    X_enhanced = np.hstack([X, X_squared])
    
    print(f"Original shape: {X.shape}")
    print(f"Enhanced shape: {X_enhanced.shape}")
    print()
    print("Enhanced features:")
    print(X_enhanced)

if __name__ == "__main__":
    main()
```

### 2. Data Augmentation

```python
import numpy as np

def main():
    # Original data
    data = np.array([[1, 2, 3],
                     [4, 5, 6]])
    
    # Create augmented versions
    flipped = data[:, ::-1]
    
    # Combine original and augmented
    augmented = np.vstack([data, flipped])
    
    print("Original:")
    print(data)
    print()
    print("Augmented dataset:")
    print(augmented)

if __name__ == "__main__":
    main()
```

### 3. One-Hot Encoding

```python
import numpy as np

def main():
    labels = np.array([0, 1, 2, 0, 1])
    n_classes = 3
    
    # Create one-hot encoding
    one_hot = np.eye(n_classes)[labels]
    
    print(f"Labels: {labels}")
    print()
    print("One-hot encoding:")
    print(one_hot)

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Concatenate two 1D arrays `a = np.array([1, 2, 3])` and `b = np.array([4, 5, 6])` using `np.concatenate`. Then create 2D row vectors from each and stack them vertically using `np.vstack`.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([1, 2, 3])
        b = np.array([4, 5, 6])
        c = np.concatenate([a, b])
        print(f"Concatenated: {c}")

        stacked = np.vstack([a, b])
        print(f"Stacked shape: {stacked.shape}")  # (2, 3)

---

**Exercise 2.**
Given two matrices `A` of shape `(3, 2)` and `B` of shape `(3, 4)`, concatenate them horizontally along axis 1 to form a `(3, 6)` matrix. Verify the result shape.

??? success "Solution to Exercise 2"

        import numpy as np

        A = np.ones((3, 2))
        B = np.zeros((3, 4))
        result = np.concatenate([A, B], axis=1)
        print(f"Shape: {result.shape}")  # (3, 6)

---

**Exercise 3.**
Use `np.hstack`, `np.vstack`, and `np.concatenate` to build a 4x4 block matrix from four 2x2 blocks: `A = np.ones((2,2))`, `B = np.zeros((2,2))`, `C = np.full((2,2), 2)`, `D = np.eye(2)`. The result should have `A` and `B` on the top row and `C` and `D` on the bottom.

??? success "Solution to Exercise 3"

        import numpy as np

        A = np.ones((2, 2))
        B = np.zeros((2, 2))
        C = np.full((2, 2), 2)
        D = np.eye(2)

        top = np.hstack([A, B])
        bottom = np.hstack([C, D])
        block = np.vstack([top, bottom])
        print(f"Shape: {block.shape}")  # (4, 4)
        print(block)
