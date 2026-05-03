# np.newaxis — Adding Dimensions

`np.newaxis` inserts a new axis (dimension) into an array, increasing its dimensionality by one. This is essential for broadcasting and reshaping operations.

!!! tip "Mental Model"
    `np.newaxis` is just `None` used inside square brackets -- it tells NumPy "insert a length-1 axis here." Picture it as stretching a 1D ruler into a 2D sheet by adding a direction. Unlike `expand_dims`, you place it directly in the indexing expression, making it concise for inline broadcasting.

```python
import numpy as np
```

---

## What is np.newaxis?

`np.newaxis` is simply an alias for `None`:

```python
print(np.newaxis is None)  # True
```

When used in array indexing, it inserts a new axis of length 1.

---

## Basic Usage

### 1D to 2D: Row Vector

```python
arr = np.array([1, 2, 3, 4])
print(arr.shape)  # (4,)

# Add axis at position 0 → row vector
row = arr[np.newaxis, :]
print(row.shape)  # (1, 4)
print(row)
# [[1 2 3 4]]
```

### 1D to 2D: Column Vector

```python
arr = np.array([1, 2, 3, 4])

# Add axis at position 1 → column vector
col = arr[:, np.newaxis]
print(col.shape)  # (4, 1)
print(col)
# [[1]
#  [2]
#  [3]
#  [4]]
```

---

## Visual Explanation

```
Original: arr = [1, 2, 3, 4]     shape: (4,)

arr[np.newaxis, :]              shape: (1, 4)
┌─────────────────┐
│ [1, 2, 3, 4]    │  ← 1 row, 4 columns
└─────────────────┘

arr[:, np.newaxis]              shape: (4, 1)
┌───┐
│ 1 │  ← 4 rows, 1 column
│ 2 │
│ 3 │
│ 4 │
└───┘
```

---

## Multiple Axes

Add multiple dimensions:

```python
arr = np.array([1, 2, 3])
print(arr.shape)  # (3,)

# Add two axes
expanded = arr[np.newaxis, :, np.newaxis]
print(expanded.shape)  # (1, 3, 1)

# Equivalent to
expanded = arr[None, :, None]
```

---

## Broadcasting with newaxis

The main use of `newaxis` is enabling broadcasting between arrays of different shapes.

### Outer Product

```python
a = np.array([1, 2, 3])
b = np.array([10, 20, 30, 40])

# Without newaxis: error or unexpected result
# a * b  # shapes (3,) and (4,) don't broadcast

# With newaxis: outer product
result = a[:, np.newaxis] * b[np.newaxis, :]
# Shapes: (3, 1) * (1, 4) → (3, 4)
print(result)
# [[ 10  20  30  40]
#  [ 20  40  60  80]
#  [ 30  60  90 120]]
```

### Row-wise Operations

```python
# 2D array
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])

# 1D array to subtract from each row
row_values = np.array([1, 1, 1])

# Direct subtraction works (shapes align)
print(matrix - row_values)
# [[0 1 2]
#  [3 4 5]]
```

### Column-wise Operations

```python
matrix = np.array([[1, 2, 3],
                   [4, 5, 6]])

# 1D array to subtract from each column
col_values = np.array([1, 2])

# Need newaxis to align shapes
# matrix shape: (2, 3)
# col_values shape: (2,) → need (2, 1)
print(matrix - col_values[:, np.newaxis])
# [[0 1 2]
#  [2 3 4]]
```

---

## Practical Examples

### Normalize Each Column

```python
data = np.array([[1, 100, 1000],
                 [2, 200, 2000],
                 [3, 300, 3000]])

# Compute column means and stds
col_mean = data.mean(axis=0)  # shape (3,)
col_std = data.std(axis=0)    # shape (3,)

# Normalize (broadcasting works directly)
normalized = (data - col_mean) / col_std
```

### Normalize Each Row

```python
data = np.array([[1, 2, 3],
                 [10, 20, 30],
                 [100, 200, 300]])

# Compute row means
row_mean = data.mean(axis=1)  # shape (3,)
row_std = data.std(axis=1)    # shape (3,)

# Need newaxis for broadcasting
normalized = (data - row_mean[:, np.newaxis]) / row_std[:, np.newaxis]
```

### Distance Matrix

```python
# Points in 2D
points = np.array([[0, 0],
                   [1, 0],
                   [0, 1],
                   [1, 1]])  # shape (4, 2)

# Compute pairwise distances
# Expand dimensions for broadcasting
diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
# Shape: (4, 1, 2) - (1, 4, 2) → (4, 4, 2)

distances = np.sqrt((diff ** 2).sum(axis=2))
print(distances)
# [[0.    1.    1.    1.414]
#  [1.    0.    1.414 1.   ]
#  [1.    1.414 0.    1.   ]
#  [1.414 1.    1.    0.   ]]
```

### Image Channel Operations

```python
# Grayscale image: (height, width)
gray = np.random.rand(100, 100)

# Convert to RGB by repeating across new channel axis
rgb = gray[:, :, np.newaxis] * np.array([1, 0.5, 0.5])
# Shape: (100, 100, 1) * (3,) → (100, 100, 3)
```

---

## newaxis vs reshape vs expand_dims

Three ways to add dimensions:

```python
arr = np.array([1, 2, 3, 4])

# Method 1: newaxis
result1 = arr[:, np.newaxis]

# Method 2: reshape
result2 = arr.reshape(-1, 1)

# Method 3: expand_dims
result3 = np.expand_dims(arr, axis=1)

# All produce shape (4, 1)
print(result1.shape, result2.shape, result3.shape)
```

### When to Use Each

| Method | Best For |
|--------|----------|
| `np.newaxis` | Inline broadcasting, clear axis position |
| `reshape()` | Complex shape changes |
| `expand_dims()` | Programmatic axis insertion |

```python
# newaxis: clear where axis is added
col = arr[:, np.newaxis]  # Obviously adds axis at end

# expand_dims: when axis position is variable
axis = 1
col = np.expand_dims(arr, axis=axis)

# reshape: multiple changes at once
reshaped = arr.reshape(2, 2)
```

---

## Using None Instead

Since `np.newaxis is None`, you can use `None` directly:

```python
arr = np.array([1, 2, 3])

# These are equivalent:
arr[np.newaxis, :]
arr[None, :]

arr[:, np.newaxis]
arr[:, None]
```

`np.newaxis` is more readable and explicit; `None` is shorter.

---

## Common Patterns

```python
arr = np.array([1, 2, 3, 4])

# Row vector (1, n)
arr[np.newaxis, :]
arr[None, :]
arr.reshape(1, -1)

# Column vector (n, 1)
arr[:, np.newaxis]
arr[:, None]
arr.reshape(-1, 1)

# Add axis at beginning
arr[np.newaxis, ...]  # ... means "all other axes"

# Add axis at end
arr[..., np.newaxis]
```

---

## Summary

| Expression | Input Shape | Output Shape |
|------------|-------------|--------------|
| `arr[np.newaxis, :]` | `(n,)` | `(1, n)` |
| `arr[:, np.newaxis]` | `(n,)` | `(n, 1)` |
| `arr[np.newaxis, :, np.newaxis]` | `(n,)` | `(1, n, 1)` |
| `arr[:, np.newaxis, :]` | `(m, n)` | `(m, 1, n)` |

**Key Takeaways**:

- `np.newaxis` (or `None`) inserts a new axis of length 1
- Essential for broadcasting between arrays of different dimensions
- Use for outer products, row/column operations, distance matrices
- Position in index determines where axis is inserted
- Equivalent to `np.expand_dims()` but more concise inline


---

## Exercises

**Exercise 1.**
Given `a = np.array([2, 4, 6])`, use `np.newaxis` to reshape it into a column vector of shape `(3, 1)`. Then multiply it with `b = np.array([1, 10, 100])` (shape `(3,)`) using broadcasting to produce a `(3, 3)` outer product. Print the result.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([2, 4, 6])
        b = np.array([1, 10, 100])

        col = a[:, np.newaxis]  # shape (3, 1)
        result = col * b        # broadcasting: (3, 1) * (3,) -> (3, 3)
        print(result)
        # [[  2  20 200]
        #  [  4  40 400]
        #  [  6  60 600]]

---

**Exercise 2.**
Create a 1D array `x = np.linspace(0, 1, 5)`. Use `None` (equivalent to `np.newaxis`) to compute the pairwise absolute difference matrix `|x_i - x_j|` for all pairs `(i, j)`. The result should have shape `(5, 5)`.

??? success "Solution to Exercise 2"

        import numpy as np

        x = np.linspace(0, 1, 5)

        # x[:, None] has shape (5, 1), x[None, :] has shape (1, 5)
        diff_matrix = np.abs(x[:, None] - x[None, :])
        print(diff_matrix.shape)  # (5, 5)
        print(diff_matrix)

---

**Exercise 3.**
Given a 2D array `a = np.arange(6).reshape(2, 3)`, add a new axis using `np.newaxis` so that the result has shape `(2, 1, 3)`. Then broadcast-add this with `b = np.ones((4, 3))` to produce a result of shape `(2, 4, 3)`. Print the shape of the result.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.arange(6).reshape(2, 3)
        a_expanded = a[:, np.newaxis, :]  # shape (2, 1, 3)

        b = np.ones((4, 3))
        result = a_expanded + b  # (2, 1, 3) + (4, 3) -> (2, 4, 3)
        print(result.shape)  # (2, 4, 3)
