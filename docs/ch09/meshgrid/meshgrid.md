# np.meshgrid

!!! tip "Mental Model"
    `meshgrid` takes two 1D vectors of x and y coordinates and returns two 2D matrices where every (x, y) pair on the grid has a home. One matrix holds the x-values repeated across rows, the other holds y-values repeated down columns. This lets you evaluate $f(x, y)$ for every grid point in a single vectorized call.

## Overview

`np.meshgrid` creates coordinate matrices from 1D coordinate vectors. Given two 1D arrays representing x and y coordinates, it returns two 2D arrays where every combination of x and y values is represented. This is essential for evaluating functions over a grid and creating surface plots.

### 1. Basic Usage

```python
import numpy as np

def main():
    x = np.linspace(0, 2, 3)  # [0, 1, 2]
    y = np.linspace(0, 3, 4)  # [0, 1, 2, 3]
    
    print(f"{x = }")
    print(f"{y = }")
    
    X, Y = np.meshgrid(x, y)
    
    print("X :")
    print(X)
    print()
    print("Y :")
    print(Y)

if __name__ == "__main__":
    main()
```

**Output:**

```
x = array([0., 1., 2.])
y = array([0., 1., 2., 3.])

X :
[[0. 1. 2.]
 [0. 1. 2.]
 [0. 1. 2.]
 [0. 1. 2.]]

Y :
[[0. 0. 0.]
 [1. 1. 1.]
 [2. 2. 2.]
 [3. 3. 3.]]
```

### 2. Output Shape

The output arrays have shape `(len(y), len(x))`. Each position `(i, j)` in the output represents the coordinate pair `(x[j], y[i])`.

```python
import numpy as np

def main():
    x = np.linspace(0, 2, 3)  # 3 elements
    y = np.linspace(0, 3, 4)  # 4 elements
    
    X, Y = np.meshgrid(x, y)
    
    print(f"x shape: {x.shape}")
    print(f"y shape: {y.shape}")
    print(f"X shape: {X.shape}")
    print(f"Y shape: {Y.shape}")

if __name__ == "__main__":
    main()
```

**Output:**

```
x shape: (3,)
y shape: (4,)
X shape: (4, 3)
Y shape: (4, 3)
```

### 3. Coordinate Pairing

At each grid position, `X[i,j]` and `Y[i,j]` together form a coordinate pair.

```python
import numpy as np

def main():
    x = np.array([10, 20, 30])
    y = np.array([1, 2])
    
    X, Y = np.meshgrid(x, y)
    
    print("Coordinate pairs at each grid position:")
    for i in range(Y.shape[0]):
        for j in range(X.shape[1]):
            print(f"  ({X[i,j]}, {Y[i,j]})", end="")
        print()

if __name__ == "__main__":
    main()
```

**Output:**

```
Coordinate pairs at each grid position:
  (10, 1)  (20, 1)  (30, 1)
  (10, 2)  (20, 2)  (30, 2)
```

## Function Evaluation

### 1. Scalar Function

Apply element-wise operations to evaluate a function at every grid point.

```python
import numpy as np

def f(X, Y):
    return X**2 + Y**2

def main():
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 3, 4)
    
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    
    print("X :")
    print(X)
    print()
    print("Y :")
    print(Y)
    print()
    print("Z = X² + Y² :")
    print(Z)

if __name__ == "__main__":
    main()
```

**Output:**

```
X :
[[0. 1. 2.]
 [0. 1. 2.]
 [0. 1. 2.]
 [0. 1. 2.]]

Y :
[[0. 0. 0.]
 [1. 1. 1.]
 [2. 2. 2.]
 [3. 3. 3.]]

Z = X² + Y² :
[[ 0.  1.  4.]
 [ 1.  2.  5.]
 [ 4.  5.  8.]
 [ 9. 10. 13.]]
```

### 2. Mathematical Functions

Use NumPy functions for trigonometric, exponential, and other operations.

```python
import numpy as np

def main():
    x = np.linspace(-np.pi, np.pi, 5)
    y = np.linspace(-np.pi, np.pi, 5)
    
    X, Y = np.meshgrid(x, y)
    
    Z = np.sin(X) * np.cos(Y)
    
    print("sin(X) * cos(Y) :")
    print(np.round(Z, 2))

if __name__ == "__main__":
    main()
```

### 3. Conditional Logic

Boolean operations work element-wise on mesh grids.

```python
import numpy as np

def main():
    x = np.linspace(-2, 2, 5)
    y = np.linspace(-2, 2, 5)
    
    X, Y = np.meshgrid(x, y)
    
    # Points inside unit circle
    inside_circle = X**2 + Y**2 <= 1
    
    print("Inside unit circle:")
    print(inside_circle.astype(int))

if __name__ == "__main__":
    main()
```

## Indexing Options

### 1. Default (xy indexing)

By default, `meshgrid` uses Cartesian (xy) indexing where the first dimension corresponds to rows (y) and the second to columns (x).

```python
import numpy as np

def main():
    x = np.array([1, 2, 3])
    y = np.array([4, 5])
    
    X, Y = np.meshgrid(x, y, indexing='xy')  # default
    
    print(f"X shape: {X.shape}")  # (2, 3) = (len(y), len(x))
    print("X :")
    print(X)

if __name__ == "__main__":
    main()
```

### 2. Matrix (ij indexing)

Matrix indexing swaps the convention: first dimension is rows (first input), second is columns (second input).

```python
import numpy as np

def main():
    x = np.array([1, 2, 3])
    y = np.array([4, 5])
    
    X_xy, Y_xy = np.meshgrid(x, y, indexing='xy')
    X_ij, Y_ij = np.meshgrid(x, y, indexing='ij')
    
    print("xy indexing (default):")
    print(f"  X shape: {X_xy.shape}")
    print()
    print("ij indexing:")
    print(f"  X shape: {X_ij.shape}")

if __name__ == "__main__":
    main()
```

**Output:**

```
xy indexing (default):
  X shape: (2, 3)

ij indexing:
  X shape: (3, 2)
```

### 3. When to Use ij

Use `indexing='ij'` when working with matrix conventions or when you want the output shape to match `(len(x), len(y))` instead of `(len(y), len(x))`.

```python
import numpy as np

def main():
    rows = np.arange(3)
    cols = np.arange(4)
    
    R, C = np.meshgrid(rows, cols, indexing='ij')
    
    print(f"Shape: {R.shape}")  # (3, 4) matches (len(rows), len(cols))
    print("Row indices:")
    print(R)

if __name__ == "__main__":
    main()
```

## Memory Efficiency

### 1. Sparse Option

The `sparse=True` option returns arrays that broadcast to the full grid without allocating full memory.

```python
import numpy as np

def main():
    x = np.linspace(0, 1, 1000)
    y = np.linspace(0, 1, 1000)
    
    # Dense: full memory allocation
    X_dense, Y_dense = np.meshgrid(x, y, sparse=False)
    
    # Sparse: broadcast-compatible shapes
    X_sparse, Y_sparse = np.meshgrid(x, y, sparse=True)
    
    print("Dense arrays:")
    print(f"  X shape: {X_dense.shape}, size: {X_dense.nbytes:,} bytes")
    print()
    print("Sparse arrays:")
    print(f"  X shape: {X_sparse.shape}, size: {X_sparse.nbytes:,} bytes")

if __name__ == "__main__":
    main()
```

**Output:**

```
Dense arrays:
  X shape: (1000, 1000), size: 8,000,000 bytes

Sparse arrays:
  X shape: (1, 1000), size: 8,000 bytes
```

### 2. Sparse Broadcasting

Sparse grids rely on broadcasting for computation.

```python
import numpy as np

def main():
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 3, 4)
    
    X_sparse, Y_sparse = np.meshgrid(x, y, sparse=True)
    
    print(f"X_sparse shape: {X_sparse.shape}")
    print(f"Y_sparse shape: {Y_sparse.shape}")
    
    # Broadcasting produces full result
    Z = X_sparse**2 + Y_sparse**2
    print(f"Z shape: {Z.shape}")

if __name__ == "__main__":
    main()
```

**Output:**

```
X_sparse shape: (1, 3)
Y_sparse shape: (4, 1)
Z shape: (4, 3)
```

### 3. Copy vs View

The `copy` parameter controls whether output arrays share memory with inputs.

```python
import numpy as np

def main():
    x = np.array([1.0, 2.0, 3.0])
    y = np.array([4.0, 5.0])
    
    # copy=False (default): may share memory
    X, Y = np.meshgrid(x, y, copy=False)
    
    # Modifying x affects X
    x[0] = 999
    print("After modifying x[0] = 999:")
    print(X)

if __name__ == "__main__":
    main()
```

## Common Patterns

### 1. Image Coordinates

Create pixel coordinate grids for image processing.

```python
import numpy as np

def main():
    height, width = 480, 640
    
    x = np.arange(width)
    y = np.arange(height)
    
    X, Y = np.meshgrid(x, y)
    
    # Distance from center
    cx, cy = width // 2, height // 2
    distance = np.sqrt((X - cx)**2 + (Y - cy)**2)
    
    print(f"Distance grid shape: {distance.shape}")
    print(f"Center distance: {distance[cy, cx]}")
    print(f"Corner distance: {distance[0, 0]:.1f}")

if __name__ == "__main__":
    main()
```

### 2. Parameter Sweep

Evaluate a function across all parameter combinations.

```python
import numpy as np

def model(learning_rate, momentum):
    # Simplified model performance function
    return -((learning_rate - 0.01)**2 + (momentum - 0.9)**2)

def main():
    lr_values = np.linspace(0.001, 0.1, 50)
    mom_values = np.linspace(0.5, 0.99, 50)
    
    LR, MOM = np.meshgrid(lr_values, mom_values)
    performance = model(LR, MOM)
    
    # Find best parameters
    best_idx = np.unravel_index(np.argmax(performance), performance.shape)
    print(f"Best LR: {LR[best_idx]:.4f}")
    print(f"Best Momentum: {MOM[best_idx]:.4f}")

if __name__ == "__main__":
    main()
```

### 3. Contour Data

Prepare data for contour plots.

```python
import numpy as np

def main():
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    
    X, Y = np.meshgrid(x, y)
    
    # Multivariate Gaussian
    Z = np.exp(-(X**2 + Y**2) / 2)
    
    print(f"Ready for plt.contour(X, Y, Z)")
    print(f"Grid dimensions: {X.shape}")

if __name__ == "__main__":
    main()
```

## The Grid Computation Pipeline

A grid is a **discrete sampling of continuous space**. All grid-based computation follows the same four steps:

```text
1. Define 1D vectors     →  x = np.linspace(-5, 5, 100)
2. Expand to grid        →  X, Y = np.meshgrid(x, y)
3. Evaluate function     →  Z = f(X, Y)
4. Visualize or analyze  →  ax.plot_surface(X, Y, Z)
```

This pipeline turns vectors into surfaces — and applies to function plotting, parameter sweeps, PDFs, and any computation over a 2D (or higher) domain. See also [mgrid / ogrid](mgrid_ogrid.md) for alternative grid creation and [Surface Plotting](surface_plotting.md) for visualization.

---

## Exercises

**Exercise 1.**
Create 1D arrays `x = np.linspace(-2, 2, 5)` and `y = np.linspace(-1, 1, 3)`. Use `np.meshgrid` to create 2D grids `X` and `Y`. Print their shapes and verify that `X[0, :]` equals `x` and `Y[:, 0]` equals `y`.

??? success "Solution to Exercise 1"

        import numpy as np

        x = np.linspace(-2, 2, 5)
        y = np.linspace(-1, 1, 3)
        X, Y = np.meshgrid(x, y)

        print(f"X shape: {X.shape}")  # (3, 5)
        print(f"Y shape: {Y.shape}")  # (3, 5)
        print(f"X[0,:] == x: {np.array_equal(X[0, :], x)}")
        print(f"Y[:,0] == y: {np.array_equal(Y[:, 0], y)}")

---

**Exercise 2.**
Using meshgrid, evaluate the function `f(x, y) = x^2 + y^2` on a grid from -3 to 3 in both dimensions with 100 points each. Find the minimum value and its grid location.

??? success "Solution to Exercise 2"

        import numpy as np

        x = np.linspace(-3, 3, 100)
        y = np.linspace(-3, 3, 100)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2

        min_val = Z.min()
        min_idx = np.unravel_index(Z.argmin(), Z.shape)
        print(f"Min value: {min_val:.6f}")
        print(f"At grid position: ({X[min_idx]:.3f}, {Y[min_idx]:.3f})")

---

**Exercise 3.**
Use `np.meshgrid` with `indexing='ij'` (matrix indexing) and compare with the default `indexing='xy'`. Create grids from `x = [1, 2, 3]` and `y = [4, 5]`. Print `X` and `Y` for both indexing modes and explain the difference.

??? success "Solution to Exercise 3"

        import numpy as np

        x = np.array([1, 2, 3])
        y = np.array([4, 5])

        X_xy, Y_xy = np.meshgrid(x, y, indexing='xy')
        X_ij, Y_ij = np.meshgrid(x, y, indexing='ij')

        print(f"xy: X shape {X_xy.shape}, Y shape {Y_xy.shape}")
        print(f"ij: X shape {X_ij.shape}, Y shape {Y_ij.shape}")
        # 'xy': X has shape (len(y), len(x))
        # 'ij': X has shape (len(x), len(y)) — matrix convention
