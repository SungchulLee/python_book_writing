# np.mgrid and np.ogrid

!!! tip "Mental Model"
    `mgrid` builds full coordinate grids using slice syntax (like `meshgrid` but more compact), while `ogrid` returns open grids -- just the 1D vectors with shapes set up for broadcasting. Use `ogrid` when you want memory efficiency and `mgrid` when you need the fully materialized grid.

## np.mgrid Basics

`np.mgrid` is an index trick that creates dense multi-dimensional mesh grids using slice notation. Unlike `np.meshgrid`, which takes arrays as arguments, `np.mgrid` uses Python's slice syntax directly.

### 1. Basic Syntax

```python
import numpy as np

def main():
    # np.mgrid[start:stop:step, start:stop:step]
    X, Y = np.mgrid[0:3, 0:4]
    
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
X :
[[0 0 0 0]
 [1 1 1 1]
 [2 2 2 2]]

Y :
[[0 1 2 3]
 [0 1 2 3]
 [0 1 2 3]]
```

### 2. Integer Step

With integer step, `np.mgrid` works like `np.arange` for each dimension.

```python
import numpy as np

def main():
    # Step of 2
    X, Y = np.mgrid[0:6:2, 0:9:3]
    
    print("X (step=2) :")
    print(X)
    print()
    print("Y (step=3) :")
    print(Y)

if __name__ == "__main__":
    main()
```

**Output:**

```
X (step=2) :
[[0 0 0]
 [2 2 2]
 [4 4 4]]

Y (step=3) :
[[0 3 6]
 [0 3 6]
 [0 3 6]]
```

### 3. Complex Step

When the step is a complex number (e.g., `5j`), the integer part specifies the number of points, and the stop value is included.

```python
import numpy as np

def main():
    # 5j means 5 points from start to stop (inclusive)
    X, Y = np.mgrid[0:4:5j, 0:2:3j]
    
    print("X (5 points from 0 to 4) :")
    print(X)
    print()
    print("Y (3 points from 0 to 2) :")
    print(Y)

if __name__ == "__main__":
    main()
```

**Output:**

```
X (5 points from 0 to 4) :
[[0. 0. 0.]
 [1. 1. 1.]
 [2. 2. 2.]
 [3. 3. 3.]
 [4. 4. 4.]]

Y (3 points from 0 to 2) :
[[0. 1. 2.]
 [0. 1. 2.]
 [0. 1. 2.]
 [0. 1. 2.]
 [0. 1. 2.]]
```

## mgrid vs meshgrid

### 1. Equivalent Results

`np.mgrid` with complex step produces the same result as `np.meshgrid` with `indexing='ij'`.

```python
import numpy as np

def main():
    # Using np.meshgrid
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 3, 4)
    X1, Y1 = np.meshgrid(x, y, indexing='ij')
    
    # Using np.mgrid
    X2, Y2 = np.mgrid[0:2:3j, 0:3:4j]
    
    print("meshgrid X shape:", X1.shape)
    print("mgrid X shape:", X2.shape)
    print()
    print("Arrays equal:", np.allclose(X1, X2) and np.allclose(Y1, Y2))

if __name__ == "__main__":
    main()
```

**Output:**

```
meshgrid X shape: (3, 4)
mgrid X shape: (3, 4)

Arrays equal: True
```

### 2. Indexing Convention

`np.mgrid` uses matrix (`ij`) indexing by default, while `np.meshgrid` uses Cartesian (`xy`) indexing.

```python
import numpy as np

def main():
    # mgrid: first index varies along first axis
    X_mgrid, Y_mgrid = np.mgrid[0:2:3j, 0:3:4j]
    
    # meshgrid xy: first input varies along second axis
    x = np.linspace(0, 2, 3)
    y = np.linspace(0, 3, 4)
    X_xy, Y_xy = np.meshgrid(x, y, indexing='xy')
    
    print(f"mgrid shape: {X_mgrid.shape}")      # (3, 4)
    print(f"meshgrid xy shape: {X_xy.shape}")   # (4, 3)

if __name__ == "__main__":
    main()
```

### 3. Syntax Comparison

```python
import numpy as np

def main():
    # meshgrid approach
    x = np.linspace(-1, 1, 50)
    y = np.linspace(-1, 1, 50)
    X1, Y1 = np.meshgrid(x, y)
    
    # mgrid approach (more concise)
    Y2, X2 = np.mgrid[-1:1:50j, -1:1:50j]
    
    # Note: mgrid order is reversed for xy convention
    print("Both create 50x50 grids")
    print(f"meshgrid shape: {X1.shape}")
    print(f"mgrid shape: {X2.shape}")

if __name__ == "__main__":
    main()
```

## np.ogrid Basics

`np.ogrid` creates open (sparse) grids that broadcast to the full grid shape without allocating full memory.

### 1. Basic Syntax

```python
import numpy as np

def main():
    # ogrid returns 1D arrays shaped for broadcasting
    X, Y = np.ogrid[0:3, 0:4]
    
    print("X shape:", X.shape)
    print("Y shape:", Y.shape)
    print()
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
X shape: (3, 1)
Y shape: (1, 4)

X :
[[0]
 [1]
 [2]]

Y :
[[0 1 2 3]]
```

### 2. Broadcasting Behavior

Operations on ogrid arrays broadcast to the full grid.

```python
import numpy as np

def main():
    X, Y = np.ogrid[0:3, 0:4]
    
    # Broadcasting creates full grid
    Z = X + Y
    
    print(f"X shape: {X.shape}")
    print(f"Y shape: {Y.shape}")
    print(f"Z shape: {Z.shape}")
    print()
    print("Z = X + Y :")
    print(Z)

if __name__ == "__main__":
    main()
```

**Output:**

```
X shape: (3, 1)
Y shape: (1, 4)
Z shape: (3, 4)

Z = X + Y :
[[0 1 2 3]
 [1 2 3 4]
 [2 3 4 5]]
```

### 3. Complex Step

Like `mgrid`, `ogrid` supports complex step for `linspace`-like behavior.

```python
import numpy as np

def main():
    X, Y = np.ogrid[0:1:5j, 0:2:3j]
    
    print("X (5 points, 0 to 1):")
    print(X)
    print()
    print("Y (3 points, 0 to 2):")
    print(Y)

if __name__ == "__main__":
    main()
```

**Output:**

```
X (5 points, 0 to 1):
[[0.  ]
 [0.25]
 [0.5 ]
 [0.75]
 [1.  ]]

Y (3 points, 0 to 2):
[[0. 1. 2.]]
```

## Memory Comparison

### 1. Dense vs Sparse

```python
import numpy as np

def main():
    n = 1000
    
    # Dense grid (mgrid)
    X_dense, Y_dense = np.mgrid[0:1:n*1j, 0:1:n*1j]
    
    # Sparse grid (ogrid)
    X_sparse, Y_sparse = np.ogrid[0:1:n*1j, 0:1:n*1j]
    
    dense_bytes = X_dense.nbytes + Y_dense.nbytes
    sparse_bytes = X_sparse.nbytes + Y_sparse.nbytes
    
    print(f"Dense (mgrid): {dense_bytes:,} bytes")
    print(f"Sparse (ogrid): {sparse_bytes:,} bytes")
    print(f"Ratio: {dense_bytes / sparse_bytes:.0f}x")

if __name__ == "__main__":
    main()
```

**Output:**

```
Dense (mgrid): 16,000,000 bytes
Sparse (ogrid): 16,000 bytes
Ratio: 1000x
```

### 2. Equivalent Computation

Both produce identical results when used in computations.

```python
import numpy as np

def f(X, Y):
    return np.sin(X) * np.cos(Y)

def main():
    # Dense
    X_d, Y_d = np.mgrid[-np.pi:np.pi:100j, -np.pi:np.pi:100j]
    Z_dense = f(X_d, Y_d)
    
    # Sparse
    X_s, Y_s = np.ogrid[-np.pi:np.pi:100j, -np.pi:np.pi:100j]
    Z_sparse = f(X_s, Y_s)
    
    print(f"Results equal: {np.allclose(Z_dense, Z_sparse)}")
    print(f"Output shape: {Z_sparse.shape}")

if __name__ == "__main__":
    main()
```

### 3. When to Use Each

```python
import numpy as np

def main():
    """
    Use mgrid when:
    - You need the full coordinate arrays
    - Memory is not a concern
    - Working with small grids
    
    Use ogrid when:
    - Memory efficiency matters
    - Working with large grids
    - Only computing derived values (not storing coordinates)
    """
    
    # ogrid for large computation
    X, Y = np.ogrid[-10:10:1000j, -10:10:1000j]
    Z = np.exp(-(X**2 + Y**2) / 10)
    
    print(f"Computed {Z.size:,} values")
    print(f"Coordinate memory: {X.nbytes + Y.nbytes:,} bytes")

if __name__ == "__main__":
    main()
```

## Practical Examples

### 1. Distance Matrix

```python
import numpy as np

def main():
    # Points in 1D
    points = np.array([0, 1, 4, 7, 10])
    n = len(points)
    
    # Use ogrid for indices
    i, j = np.ogrid[0:n, 0:n]
    
    # Pairwise distances
    distances = np.abs(points[i] - points[j])
    
    print("Points:", points)
    print()
    print("Distance matrix:")
    print(distances)

if __name__ == "__main__":
    main()
```

**Output:**

```
Points: [ 0  1  4  7 10]

Distance matrix:
[[ 0  1  4  7 10]
 [ 1  0  3  6  9]
 [ 4  3  0  3  6]
 [ 7  6  3  0  3]
 [10  9  6  3  0]]
```

### 2. Circular Mask

```python
import numpy as np

def main():
    size = 11
    radius = 4
    
    # Center coordinates
    Y, X = np.ogrid[0:size, 0:size]
    center = size // 2
    
    # Distance from center
    dist = np.sqrt((X - center)**2 + (Y - center)**2)
    
    # Circular mask
    mask = dist <= radius
    
    print("Circular mask:")
    print(mask.astype(int))

if __name__ == "__main__":
    main()
```

### 3. 2D Gaussian

```python
import numpy as np

def main():
    # Parameters
    mu_x, mu_y = 0, 0
    sigma = 1
    
    # Sparse grid
    Y, X = np.ogrid[-3:3:100j, -3:3:100j]
    
    # 2D Gaussian (unnormalized)
    Z = np.exp(-((X - mu_x)**2 + (Y - mu_y)**2) / (2 * sigma**2))
    
    print(f"Shape: {Z.shape}")
    print(f"Max value: {Z.max():.4f}")
    print(f"Value at (0,0): {Z[50, 50]:.4f}")

if __name__ == "__main__":
    main()
```

## When to Use Which

```text
meshgrid  →  explicit grids, visualization, when you have pre-built 1D arrays
mgrid     →  concise syntax, small-to-medium grids, quick prototyping
ogrid     →  large grids, memory efficiency, broadcasting-aware computation
```

In practice: start with `meshgrid` for clarity. Switch to `ogrid` when memory matters (large grids). Use `mgrid` when you want compact slice syntax without worrying about memory.

## Summary Table

| Feature | np.meshgrid | np.mgrid | np.ogrid |
|---------|-------------|----------|----------|
| Input | Arrays | Slice notation | Slice notation |
| Default indexing | xy (Cartesian) | ij (matrix) | ij (matrix) |
| Output | Dense arrays | Dense arrays | Sparse arrays |
| Memory | Full allocation | Full allocation | Minimal |
| Complex step | No | Yes | Yes |
| Stop inclusive | Depends on input | With complex step | With complex step |

### Quick Reference

```python
import numpy as np

def main():
    # All create equivalent grids for computation
    
    # Method 1: meshgrid with arrays
    x = np.linspace(0, 1, 5)
    y = np.linspace(0, 1, 5)
    X1, Y1 = np.meshgrid(x, y)
    
    # Method 2: mgrid with complex step
    X2, Y2 = np.mgrid[0:1:5j, 0:1:5j]
    
    # Method 3: ogrid (memory efficient)
    X3, Y3 = np.ogrid[0:1:5j, 0:1:5j]
    
    # All produce same Z
    Z1 = X1**2 + Y1.T**2  # Note: transpose for xy indexing
    Z2 = X2**2 + Y2**2
    Z3 = X3**2 + Y3**2
    
    print("All methods work for grid computation")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Use `np.mgrid` to create a 2D integer grid from 0 to 3 in both dimensions. Print the two resulting arrays and their shapes.

??? success "Solution to Exercise 1"

        import numpy as np

        Y, X = np.mgrid[0:4, 0:4]
        print(f"Y shape: {Y.shape}")
        print(f"X shape: {X.shape}")
        print(f"Y:\n{Y}")
        print(f"X:\n{X}")

---

**Exercise 2.**
Use `np.ogrid` to create open grids for `x` in [0, 4] and `y` in [0, 3] (integer steps). Compute `x + y` using broadcasting and verify the result matches the equivalent `np.mgrid` computation.

??? success "Solution to Exercise 2"

        import numpy as np

        y_o, x_o = np.ogrid[0:4, 0:4]
        result_ogrid = y_o + x_o

        Y, X = np.mgrid[0:4, 0:4]
        result_mgrid = Y + X

        print(f"ogrid result:\n{result_ogrid}")
        print(f"Match: {np.array_equal(result_ogrid, result_mgrid)}")

---

**Exercise 3.**
Use `np.mgrid` with complex step notation to create a float grid: `np.mgrid[0:1:5j, 0:2:3j]` (5 points from 0 to 1, 3 points from 0 to 2). Print the resulting shapes and values.

??? success "Solution to Exercise 3"

        import numpy as np

        Y, X = np.mgrid[0:1:5j, 0:2:3j]
        print(f"Y shape: {Y.shape}")  # (5, 3)
        print(f"X shape: {X.shape}")  # (5, 3)
        print(f"Y:\n{Y}")
        print(f"X:\n{X}")
