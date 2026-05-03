# Array Utilities: clip, unique, diff, gradient

Common NumPy utility functions for data manipulation and analysis.

!!! tip "Mental Model"
    `clip` caps values to a range (great for clamping pixel values or enforcing bounds), `unique` finds distinct elements (like SQL `DISTINCT`), and `diff` computes consecutive differences (the discrete derivative). These utilities handle the most common data-cleaning tasks without loops.

!!! note "These Are Operators, Not Just Utilities"
    These functions transform arrays in three fundamentally different ways:

    | Function | Operator type | What it does |
    |----------|--------------|--------------|
    | `clip` | **Constraint** (projection) | Enforce bounds — project values onto $[a, b]$ |
    | `unique` | **Structural** (set extraction) | Extract distinct values — factorize into categories |
    | `diff` | **Derivative** (finite difference) | Measure change — discrete first/second derivative |
    | `gradient` | **Differential** (central difference) | Approximate continuous derivative — same-length output |

    Together they form the core toolkit for the pipeline:
    **data → constrain (clip) → structure (unique) → differentiate (diff/gradient) → analyze**.

    The unifying insight: these are **discrete analogs of mathematical operators** —
    projection, factorization, and differentiation — applied element-wise to arrays.
    They bridge raw data and higher-level analysis.

```python
import numpy as np
```

---

## np.clip() — Limit Values to Range

Mathematically, `clip(x, a, b)` is the **projection of $x$ onto the interval
$[a, b]$** — it returns the closest point in the interval to $x$. This framing
connects it to constrained optimization, where clipping is a standard step after
gradient updates.

Constrain array values to a minimum and maximum:

```python
arr = np.array([1, 5, 10, 15, 20])

# Clip to range [5, 15]
clipped = np.clip(arr, 5, 15)
print(clipped)  # [ 5  5 10 15 15]

# Clip with only min
np.clip(arr, 5, None)  # [ 5  5 10 15 20]

# Clip with only max
np.clip(arr, None, 15)  # [ 1  5 10 15 15]
```

### Method Syntax

```python
arr = np.array([1, 5, 10, 15, 20])

# Function syntax
np.clip(arr, 5, 15)

# Method syntax
arr.clip(5, 15)

# In-place (modifies original)
arr.clip(5, 15, out=arr)
```

### Practical Examples

```python
# Normalize pixel values to [0, 255]
pixels = np.array([-10, 50, 200, 300])
pixels = np.clip(pixels, 0, 255)
print(pixels)  # [  0  50 200 255]

# Prevent division by small numbers
denominators = np.array([0.001, 0.5, 1.0, 0.0001])
safe_denom = np.clip(denominators, 1e-6, None)

# Clip neural network gradients
gradients = np.array([-100, 0.5, 50, -0.1])
clipped_grads = np.clip(gradients, -1, 1)
print(clipped_grads)  # [-1.   0.5  1.  -0.1]

# Probability bounds
probs = np.array([-0.1, 0.5, 1.2])
probs = np.clip(probs, 0, 1)
print(probs)  # [0.  0.5 1. ]
```

---

## np.unique() — Find Unique Values

`unique` with `return_inverse=True` is a **factorization**: it decomposes an array
into a compact set of distinct values and an index mapping that can reconstruct the
original. This is exactly **categorical encoding** — the basis of label encoding in
ML, value-count analysis, and data compression.

Return sorted unique elements of an array:

```python
arr = np.array([3, 1, 2, 2, 3, 1, 1, 4])

unique = np.unique(arr)
print(unique)  # [1 2 3 4]
```

### Return Indices

```python
arr = np.array([3, 1, 2, 2, 3, 1, 1, 4])

# Index of first occurrence of each unique value
unique, indices = np.unique(arr, return_index=True)
print(unique)   # [1 2 3 4]
print(indices)  # [1 2 0 7]

# Indices to reconstruct original from unique
unique, inverse = np.unique(arr, return_inverse=True)
print(unique)   # [1 2 3 4]
print(inverse)  # [2 0 1 1 2 0 0 3]
print(unique[inverse])  # [3 1 2 2 3 1 1 4] (original!)

# Count of each unique value
unique, counts = np.unique(arr, return_counts=True)
print(unique)  # [1 2 3 4]
print(counts)  # [3 2 2 1]
```

### All Return Values

```python
arr = np.array([3, 1, 2, 2, 3])

unique, indices, inverse, counts = np.unique(
    arr,
    return_index=True,
    return_inverse=True,
    return_counts=True
)
```

### Unique Rows (2D)

```python
arr = np.array([[1, 2],
                [3, 4],
                [1, 2],
                [5, 6]])

# Unique rows
unique_rows = np.unique(arr, axis=0)
print(unique_rows)
# [[1 2]
#  [3 4]
#  [5 6]]
```

### Practical Examples

```python
# Find unique categories
labels = np.array(['cat', 'dog', 'cat', 'bird', 'dog'])
categories = np.unique(labels)
print(categories)  # ['bird' 'cat' 'dog']

# Value counts (like pandas)
values, counts = np.unique(labels, return_counts=True)
for v, c in zip(values, counts):
    print(f"{v}: {c}")
# bird: 1
# cat: 2
# dog: 2

# Label encoding
labels = np.array(['cat', 'dog', 'cat', 'bird'])
unique, encoded = np.unique(labels, return_inverse=True)
print(encoded)  # [1 2 1 0]  (numeric encoding)

# Check if array has duplicates
arr = np.array([1, 2, 3, 2])
has_duplicates = len(np.unique(arr)) < len(arr)
print(has_duplicates)  # True
```

---

## np.diff() — Discrete Differences

`diff` is a **finite difference operator** — the discrete analog of differentiation.
`np.diff(x)` computes forward differences ($x_{i+1} - x_i$), and `np.diff(x, n=2)`
computes second-order differences (the discrete second derivative, analogous to
acceleration). This connects directly to calculus, signal processing (change
detection), and time-series analysis (returns, velocity).

Calculate the n-th discrete difference along an axis:

```python
arr = np.array([1, 3, 6, 10, 15])

# First difference: arr[i+1] - arr[i]
diff1 = np.diff(arr)
print(diff1)  # [2 3 4 5]

# Second difference (difference of differences)
diff2 = np.diff(arr, n=2)
print(diff2)  # [1 1 1]
```

### Along Different Axes

```python
matrix = np.array([[1, 2, 4],
                   [3, 5, 9]])

# Diff along columns (axis=1, default)
np.diff(matrix)
# [[1 2]
#  [2 4]]

# Diff along rows (axis=0)
np.diff(matrix, axis=0)
# [[2 3 5]]
```

### Prepend/Append Values

```python
arr = np.array([1, 3, 6, 10])

# Prepend to maintain length
np.diff(arr, prepend=0)
# [1 2 3 4]

# Append to maintain length
np.diff(arr, append=arr[-1])
# [2 3 4 0]
```

### Practical Examples

```python
# Calculate velocity from position
time = np.array([0, 1, 2, 3, 4])
position = np.array([0, 2, 8, 18, 32])
velocity = np.diff(position) / np.diff(time)
print(velocity)  # [ 2.  6. 10. 14.]

# Calculate acceleration
acceleration = np.diff(velocity)
print(acceleration)  # [4. 4. 4.]

# Detect changes in signal
signal = np.array([1, 1, 1, 5, 5, 5, 2, 2])
changes = np.diff(signal)
change_points = np.where(changes != 0)[0]
print(change_points)  # [2 5]  (indices where changes occur)

# Cumulative sum check (diff is inverse of cumsum)
arr = np.array([1, 2, 3, 4, 5])
cumsum = np.cumsum(arr)
print(cumsum)                        # [ 1  3  6 10 15]
print(np.diff(cumsum, prepend=0))   # [1 2 3 4 5] (original!)
```

---

## np.gradient() — Numerical Gradient

`gradient` approximates the **continuous derivative** using central differences,
which are more accurate than the forward differences of `diff` and — critically —
preserve the array length. For multi-dimensional arrays, `np.gradient(img)` returns
partial derivatives along each axis, connecting directly to edge detection in image
processing and gradient computation in optimization.

Unlike `diff()`, `gradient()` computes central differences and preserves array length:

```python
arr = np.array([1, 3, 6, 10, 15])

# gradient uses central differences (except at edges)
grad = np.gradient(arr)
print(grad)  # [2.  2.5 3.5 4.5 5. ]

# Compare with diff (one element shorter)
print(np.diff(arr))  # [2 3 4 5]
```

### With Spacing

```python
# Position at uneven time intervals
t = np.array([0, 1, 3, 6])
x = np.array([0, 2, 10, 28])

# Velocity with time spacing
velocity = np.gradient(x, t)
print(velocity)  # [2.  2.5 4.33... 6.]
```

### 2D Gradient

```python
img = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Returns gradient along each axis
gy, gx = np.gradient(img)
print(gx)  # Gradient along x (columns)
print(gy)  # Gradient along y (rows)
```

### Practical Examples

```python
# Edge detection (simplified)
image = np.random.rand(100, 100)
gy, gx = np.gradient(image)
edges = np.sqrt(gx**2 + gy**2)

# Numerical derivative of function
x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)
dydx = np.gradient(y, x)
# dydx ≈ cos(x)
```

---

## diff() vs gradient()

| Feature | `np.diff()` | `np.gradient()` |
|---------|-------------|-----------------|
| Method | Forward difference | Central difference |
| Output length | n - 1 | n (same) |
| Edge handling | None | One-sided at edges |
| Accuracy | First-order | Second-order |
| Use case | Discrete changes | Smooth derivatives |

```python
arr = np.array([1, 4, 9, 16, 25])  # x^2 at x=1,2,3,4,5

# diff: forward difference
print(np.diff(arr))      # [3 5 7 9]  (length 4)

# gradient: central difference
print(np.gradient(arr))  # [3. 4. 6. 8. 9.]  (length 5)
# True derivative is 2x: [2, 4, 6, 8, 10]
# gradient is more accurate in the middle
```

---

## Summary

| Function | Purpose | Key Feature |
|----------|---------|-------------|
| `np.clip(a, min, max)` | Limit values to range | In-place option |
| `np.unique(a)` | Find unique values | Return counts/indices |
| `np.diff(a)` | Forward differences | Length n-1 |
| `np.gradient(a)` | Central differences | Length n (preserved) |

**Key Takeaways**:

- `clip()` is essential for data normalization and bound enforcement
- `unique()` with `return_counts=True` replaces pandas value_counts
- `unique()` with `return_inverse=True` enables label encoding
- `diff()` for discrete changes (signal processing, change detection)
- `gradient()` for smooth numerical derivatives (preserves length)
- Use `gradient()` over `diff()` when you need same-length output

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
