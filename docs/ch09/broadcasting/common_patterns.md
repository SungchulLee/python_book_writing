# Common Broadcasting Patterns

Once the broadcasting rules are understood, a small set of recurring patterns covers most practical use cases. These patterns eliminate explicit loops and temporary arrays, making numerical code both faster and more readable. This page collects the patterns that appear most frequently in data analysis and scientific computing.

!!! tip "Mental Model"
    Most broadcasting use cases fall into a handful of recipes: subtract a row mean, divide by a column norm, or add a bias vector. Learn these few patterns and you will recognize them everywhere -- centering, normalizing, and outer-product-style operations are the building blocks of nearly all vectorized NumPy code.

---

## Centering Data

Subtract the column mean from every row to produce zero-mean columns.

### 1. Column-wise Centering

```python
import numpy as np

def main():
    X = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0],
                  [7.0, 8.0, 9.0]])  # (3, 3)

    col_means = X.mean(axis=0)       # (3,)
    X_centered = X - col_means       # (3, 3) - (3,) broadcasts
    print("Column means:", col_means)
    print("Centered:\n", X_centered)
    print("New column means:", X_centered.mean(axis=0))

if __name__ == "__main__":
    main()
```

Output:

```
Column means: [4. 5. 6.]
Centered:
 [[-3. -3. -3.]
 [ 0.  0.  0.]
 [ 3.  3.  3.]]
New column means: [0. 0. 0.]
```

### 2. Row-wise Centering

```python
import numpy as np

def main():
    X = np.array([[1.0, 2.0, 3.0],
                  [4.0, 5.0, 6.0]])  # (2, 3)

    row_means = X.mean(axis=1, keepdims=True)  # (2, 1)
    X_centered = X - row_means                  # (2, 3) - (2, 1) broadcasts
    print("Row means:\n", row_means)
    print("Centered:\n", X_centered)

if __name__ == "__main__":
    main()
```

Output:

```
Row means:
 [[2.]
 [5.]]
Centered:
 [[-1.  0.  1.]
 [-1.  0.  1.]]
```

### 3. keepdims is Essential

Without `keepdims=True`, `X.mean(axis=1)` returns shape `(2,)` instead of `(2, 1)`, and the subtraction broadcasts incorrectly along the wrong axis.


## Standardization

Centering and scaling to unit variance in a single broadcasting expression.

### 1. Z-score Normalization

```python
import numpy as np

def main():
    X = np.random.randn(100, 5)          # (100, 5)
    mu = X.mean(axis=0)                   # (5,)
    sigma = X.std(axis=0)                 # (5,)
    Z = (X - mu) / sigma                  # each column: mean 0, std 1
    print("Column means after:", np.round(Z.mean(axis=0), 10))
    print("Column stds after: ", np.round(Z.std(axis=0), 10))

if __name__ == "__main__":
    main()
```

Output:

```
Column means after: [-0. -0.  0. -0.  0.]
Column stds after:  [1. 1. 1. 1. 1.]
```

### 2. Min-Max Scaling

```python
import numpy as np

def main():
    X = np.random.randn(100, 5)
    X_min = X.min(axis=0)                         # (5,)
    X_max = X.max(axis=0)                         # (5,)
    X_scaled = (X - X_min) / (X_max - X_min)      # all values in [0, 1]
    print("Min per column:", X_scaled.min(axis=0))
    print("Max per column:", X_scaled.max(axis=0))

if __name__ == "__main__":
    main()
```

### 3. Two Broadcasts in One Line

The expression `(X - mu) / sigma` performs two broadcasts: subtraction of `mu` with shape `(5,)` from `X` with shape `(100, 5)`, then division by `sigma` with the same shapes.


## Outer Products

Combine a column vector and a row vector to produce a 2D result.

### 1. Addition Table

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])[:, np.newaxis]  # (3, 1)
    b = np.array([10, 20, 30])[np.newaxis, :]  # (1, 3)
    table = a + b                              # (3, 3)
    print(table)

if __name__ == "__main__":
    main()
```

Output:

```
[[11 21 31]
 [12 22 32]
 [13 23 33]]
```

### 2. Multiplication Table

```python
import numpy as np

def main():
    a = np.arange(1, 10)[:, np.newaxis]  # (9, 1)
    b = np.arange(1, 10)[np.newaxis, :]  # (1, 9)
    table = a * b                         # (9, 9)
    print(table)

if __name__ == "__main__":
    main()
```

### 3. np.newaxis vs reshape

`np.newaxis` (alias for `None`) inserts a size-1 dimension. These are equivalent:

```python
a[:, np.newaxis]   # (n,) → (n, 1)
a[:, None]         # same
a.reshape(-1, 1)   # same
```


## Pairwise Distances

Compute distances between all pairs of points without loops.

### 1. Euclidean Distance Matrix

```python
import numpy as np

def main():
    # 4 points in 3D space
    X = np.random.randn(4, 3)             # (4, 3)

    diff = X[:, np.newaxis, :] - X[np.newaxis, :, :]  # (4, 1, 3) - (1, 4, 3) → (4, 4, 3)
    dist = np.sqrt((diff ** 2).sum(axis=2))            # (4, 4)
    print("Distance matrix:\n", np.round(dist, 2))

if __name__ == "__main__":
    main()
```

### 2. Shape Breakdown

| Expression | Shape | Explanation |
|---|---|---|
| `X[:, np.newaxis, :]` | `(4, 1, 3)` | Each point as a row-block |
| `X[np.newaxis, :, :]` | `(1, 4, 3)` | Each point as a column-block |
| `diff` | `(4, 4, 3)` | All pairwise coordinate differences |
| `dist` | `(4, 4)` | Euclidean distances after sum and sqrt |

### 3. Symmetry Check

```python
import numpy as np

def main():
    X = np.random.randn(5, 3)
    diff = X[:, np.newaxis, :] - X[np.newaxis, :, :]
    dist = np.sqrt((diff ** 2).sum(axis=2))
    print("Symmetric:", np.allclose(dist, dist.T))
    print("Zero diagonal:", np.allclose(np.diag(dist), 0))

if __name__ == "__main__":
    main()
```


## Row or Column Scaling

Multiply each row or column by a different weight.

### 1. Scale Columns

```python
import numpy as np

def main():
    X = np.ones((3, 4))                   # (3, 4)
    weights = np.array([1, 2, 3, 4])      # (4,)
    result = X * weights                   # each column scaled
    print(result)

if __name__ == "__main__":
    main()
```

Output:

```
[[1. 2. 3. 4.]
 [1. 2. 3. 4.]
 [1. 2. 3. 4.]]
```

### 2. Scale Rows

```python
import numpy as np

def main():
    X = np.ones((3, 4))                          # (3, 4)
    weights = np.array([10, 20, 30])[:, np.newaxis]  # (3, 1)
    result = X * weights                          # each row scaled
    print(result)

if __name__ == "__main__":
    main()
```

Output:

```
[[10. 10. 10. 10.]
 [20. 20. 20. 20.]
 [30. 30. 30. 30.]]
```

### 3. Key Difference

Column scaling uses a 1D vector with shape `(n_cols,)` that aligns with the last axis. Row scaling requires a column vector with shape `(n_rows, 1)` via `np.newaxis` or `reshape`.


## Boolean Masking with Broadcasting

Combine boolean conditions across different dimensions.

### 1. Threshold per Column

```python
import numpy as np

def main():
    X = np.array([[1, 5, 3],
                  [4, 2, 6],
                  [7, 8, 1]])             # (3, 3)
    thresholds = np.array([3, 4, 5])      # (3,)
    mask = X > thresholds                  # (3, 3) > (3,) broadcasts
    print("Mask:\n", mask)
    print("Values above thresholds:", X[mask])

if __name__ == "__main__":
    main()
```

Output:

```
Mask:
 [[False  True False]
 [ True False  True]
 [ True  True False]]
Values above thresholds: [5 4 6 7 8]
```

### 2. Range Check

```python
import numpy as np

def main():
    X = np.random.randn(5, 3)
    lower = np.array([-1, -0.5, 0])       # (3,)
    upper = np.array([1, 0.5, 2])         # (3,)
    in_range = (X >= lower) & (X <= upper)
    print("In range:\n", in_range)

if __name__ == "__main__":
    main()
```

### 3. Combining Row and Column Conditions

```python
import numpy as np

def main():
    row_mask = np.array([True, False, True])[:, np.newaxis]  # (3, 1)
    col_mask = np.array([True, True, False])[np.newaxis, :]  # (1, 3)
    combined = row_mask & col_mask                            # (3, 3)
    print(combined)

if __name__ == "__main__":
    main()
```


## Summary

The most common broadcasting patterns share the same underlying mechanism: aligning a smaller array against a larger one along a specific axis.

| Pattern | Typical Shapes | Why It Works (Rule) | Key Technique |
|---|---|---|---|
| Column centering | `(m, n) - (n,)` | `(n,)` pads to `(1, n)`, axis 0: `1→m` | `mean(axis=0)` |
| Row centering | `(m, n) - (m, 1)` | axis 1: `1→n` | `mean(axis=1, keepdims=True)` |
| Standardization | `(m, n) - (n,)` then `/ (n,)` | Same rule, applied twice | Two broadcasts in sequence |
| Outer product | `(m, 1) * (1, n)` | axis 0: `1→m`, axis 1: `1→n` | `np.newaxis` |
| Pairwise distance | `(m, 1, d) - (1, n, d)` | axes 0-1: `1→m` and `1→n`, axis 2: `d==d` | 3D broadcasting |
| Row/column scaling | `(m, n) * (n,)` or `(m, 1)` | Same as centering | Weight vector alignment |
| Boolean masking | `(m, n) > (n,)` | `(n,)` pads to `(1, n)`, axis 0: `1→m` | Threshold per column |

---

## Exercises

**Exercise 1.**
Given a matrix `X` of shape `(50, 4)`, write a single expression that performs min-max scaling on each column so that every column's values lie in `[0, 1]`. Use `keepdims` where appropriate.

??? success "Solution to Exercise 1"

        import numpy as np

        X = np.random.randn(50, 4)
        X_min = X.min(axis=0, keepdims=True)   # (1, 4)
        X_max = X.max(axis=0, keepdims=True)   # (1, 4)
        X_scaled = (X - X_min) / (X_max - X_min)
        print(X_scaled.min(axis=0))  # [0. 0. 0. 0.]
        print(X_scaled.max(axis=0))  # [1. 1. 1. 1.]

---

**Exercise 2.**
Using only broadcasting (no `np.outer`), compute the outer product of two 1D arrays `u = np.array([1, 2, 3, 4])` and `v = np.array([10, 20, 30])` to produce a `(4, 3)` result.

??? success "Solution to Exercise 2"

        import numpy as np

        u = np.array([1, 2, 3, 4])
        v = np.array([10, 20, 30])
        outer = u[:, np.newaxis] * v[np.newaxis, :]
        print(outer)
        # [[10 20 30]
        #  [20 40 60]
        #  [30 60 90]
        #  [40 80 120]]
        print(outer.shape)  # (4, 3)

---

**Exercise 3.**
Given a set of 6 points in 2D stored as `points = np.random.randn(6, 2)`, compute the full `(6, 6)` pairwise Euclidean distance matrix using broadcasting. Verify that the diagonal is all zeros and the matrix is symmetric.

??? success "Solution to Exercise 3"

        import numpy as np

        points = np.random.randn(6, 2)
        diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]  # (6, 6, 2)
        dist = np.sqrt((diff ** 2).sum(axis=2))                     # (6, 6)
        print("Diagonal all zero:", np.allclose(np.diag(dist), 0))
        print("Symmetric:", np.allclose(dist, dist.T))

---

**Exercise 4.**
Given a matrix `X` of shape `(1000, 10)`, compute the L2 norm of each row and then normalize each row to unit length using broadcasting. Verify by checking that each row's norm is approximately 1.0 after normalization.

??? success "Solution to Exercise 4"

        import numpy as np

        X = np.random.randn(1000, 10)
        norms = np.sqrt((X ** 2).sum(axis=1, keepdims=True))  # (1000, 1)
        X_normalized = X / norms  # (1000, 10) / (1000, 1)

        # Verify: each row should have norm ~1.0
        row_norms = np.sqrt((X_normalized ** 2).sum(axis=1))
        print(np.allclose(row_norms, 1.0))  # True

---

**Exercise 5.**
Create a boolean mask of shape `(5, 5)` that is `True` for elements below the diagonal, using only broadcasting. Hint: compare a column vector `np.arange(5)[:, None]` with a row vector `np.arange(5)[None, :]`. Explain which broadcasting rule makes this work.

??? success "Solution to Exercise 5"

        import numpy as np

        rows = np.arange(5)[:, np.newaxis]  # (5, 1)
        cols = np.arange(5)[np.newaxis, :]  # (1, 5)
        below_diagonal = rows > cols         # (5, 5)
        print(below_diagonal)
        # [[False False False False False]
        #  [ True False False False False]
        #  [ True  True False False False]
        #  [ True  True  True False False]
        #  [ True  True  True  True False]]

        # This works because:
        # rows: (5, 1) — axis 1 is 1, expands to 5
        # cols: (1, 5) — axis 0 is 1, expands to 5
        # Both axes have size 1 vs 5 → expand → (5, 5)
        # This is the outer-product broadcasting pattern applied
        # to a comparison operator instead of arithmetic.
