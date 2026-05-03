# Reductions with axis

!!! tip "Mental Model"
    A reduction collapses one axis of an array into a single value by applying an aggregation (sum, mean, max, etc.). Setting `axis=0` collapses rows, `axis=1` collapses columns, and omitting `axis` collapses everything to a scalar. The output shape is the input shape with the reduced axis removed.

!!! note "Array Analysis Pipeline"
    Reductions are the first stage of a five-step analysis pattern that runs through this entire section:

    ```text
    1. AGGREGATE  — sum, mean, var, std         (this page + sum_prod + statistics)
    2. COMPARE    — min, max                     (minmax + elementwise_minmax)
    3. LOCATE     — argmin, argmax, where         (minmax + searching + where)
    4. ORDER      — sort, argsort                 (sorting)
    5. CLEAN      — unique, nan handling, diff    (utility)
    ```

    Each stage consumes arrays and produces smaller, more informative arrays. Together they form the toolkit for extracting information from numerical data.

## Concept

Reduction operations collapse one or more dimensions of an array by applying an aggregation function. The `axis` parameter specifies which dimension to reduce.

### 1. What is Reduction

A reduction takes an array and produces a smaller array (or scalar) by combining elements along specified dimensions.

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    print("Original array:")
    print(a)
    print(f"Shape: {a.shape}")
    print()
    
    # Full reduction to scalar
    total = a.sum()
    print(f"sum() = {total}")
    print(f"Shape: {np.array(total).shape}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Original array:
[[1 2 3]
 [4 5 6]]
Shape: (2, 3)

sum() = 21
Shape: ()
```

### 2. axis Parameter

The `axis` parameter specifies which dimension to collapse. The result has one fewer dimension.

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    print("a.shape:", a.shape)  # (2, 3)
    print()
    
    # axis=0: collapse rows, keep columns
    print("sum(axis=0):", a.sum(axis=0))
    print("Shape:", a.sum(axis=0).shape)  # (3,)
    print()
    
    # axis=1: collapse columns, keep rows
    print("sum(axis=1):", a.sum(axis=1))
    print("Shape:", a.sum(axis=1).shape)  # (2,)

if __name__ == "__main__":
    main()
```

**Output:**

```
a.shape: (2, 3)

sum(axis=0): [5 7 9]
Shape: (3,)

sum(axis=1): [ 6 15]
Shape: (2,)
```

### 3. Visual Intuition

Think of `axis` as the direction of collapse:

- `axis=0`: Collapse vertically (down rows)
- `axis=1`: Collapse horizontally (across columns)

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 4],
                  [5, 6]])
    
    print("Array (3 rows, 2 cols):")
    print(a)
    print()
    
    # axis=0: sum down each column
    print("axis=0 (sum down):", a.sum(axis=0))
    # [1+3+5, 2+4+6] = [9, 12]
    
    # axis=1: sum across each row
    print("axis=1 (sum across):", a.sum(axis=1))
    # [1+2, 3+4, 5+6] = [3, 7, 11]

if __name__ == "__main__":
    main()
```

## Shape Rules

### 1. Output Shape

The output shape removes the axis dimension from the input shape.

```python
import numpy as np

def main():
    a = np.zeros((2, 3, 4))
    
    print(f"Original shape: {a.shape}")
    print()
    print(f"sum(axis=0).shape: {a.sum(axis=0).shape}")  # (3, 4)
    print(f"sum(axis=1).shape: {a.sum(axis=1).shape}")  # (2, 4)
    print(f"sum(axis=2).shape: {a.sum(axis=2).shape}")  # (2, 3)
    print(f"sum().shape: {a.sum().shape}")              # ()

if __name__ == "__main__":
    main()
```

### 2. keepdims Parameter

Use `keepdims=True` to preserve the reduced dimension as size 1.

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    print(f"Original shape: {a.shape}")
    print()
    
    # Without keepdims
    s1 = a.sum(axis=1)
    print(f"sum(axis=1): {s1}")
    print(f"Shape: {s1.shape}")
    print()
    
    # With keepdims
    s2 = a.sum(axis=1, keepdims=True)
    print(f"sum(axis=1, keepdims=True):")
    print(s2)
    print(f"Shape: {s2.shape}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Original shape: (2, 3)

sum(axis=1): [ 6 15]
Shape: (2,)

sum(axis=1, keepdims=True):
[[ 6]
 [15]]
Shape: (2, 1)
```

### 3. Broadcasting Use

`keepdims=True` is useful for broadcasting operations.

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    # Normalize each row to sum to 1
    row_sums = a.sum(axis=1, keepdims=True)
    normalized = a / row_sums
    
    print("Original:")
    print(a)
    print()
    print("Row sums (keepdims=True):")
    print(row_sums)
    print()
    print("Normalized rows:")
    print(normalized)
    print()
    print("Verify row sums:", normalized.sum(axis=1))

if __name__ == "__main__":
    main()
```

## Method vs Function

### 1. Two Syntaxes

Most reductions can be called as methods or functions.

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    
    # Method syntax
    print(f"a.sum() = {a.sum()}")
    print(f"a.sum(axis=0) = {a.sum(axis=0)}")
    
    # Function syntax
    print(f"np.sum(a) = {np.sum(a)}")
    print(f"np.sum(a, axis=0) = {np.sum(a, axis=0)}")

if __name__ == "__main__":
    main()
```

### 2. When to Use Each

```python
import numpy as np

def main():
    """
    Method syntax: a.sum()
    - More concise
    - Object-oriented style
    - Only works on ndarray
    
    Function syntax: np.sum(a)
    - Works on lists and array-like
    - Consistent with other np functions
    - Preferred in functional pipelines
    """
    
    # Function works on lists
    result = np.sum([1, 2, 3])
    print(f"np.sum([1, 2, 3]) = {result}")
    
    # Method requires array
    a = np.array([1, 2, 3])
    print(f"a.sum() = {a.sum()}")

if __name__ == "__main__":
    main()
```

### 3. Common Reductions

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    reductions = [
        ("sum", a.sum()),
        ("prod", a.prod()),
        ("min", a.min()),
        ("max", a.max()),
        ("mean", a.mean()),
        ("std", a.std()),
        ("var", a.var()),
    ]
    
    for name, result in reductions:
        print(f"{name:6}: {result}")

if __name__ == "__main__":
    main()
```

## Mathematical Form

### 1. Sum Notation

For a 2D array $a = (a_{ij})$:

$$
\begin{aligned}
\texttt{a.sum()} &= \sum_i \sum_j a_{ij} \\
\texttt{a.sum(axis=0)[j]} &= \sum_i a_{ij} \\
\texttt{a.sum(axis=1)[i]} &= \sum_j a_{ij}
\end{aligned}
$$

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    print(f"sum over all: {a.sum()}")
    print(f"sum over axis=0 (columns): {a.sum(axis=0)}")
    print(f"sum over axis=1 (rows): {a.sum(axis=1)}")

if __name__ == "__main__":
    main()
```

### 2. Index Interpretation

The axis being summed disappears from the output indices.

```python
import numpy as np

def main():
    # 3D array: shape (2, 3, 4)
    a = np.arange(24).reshape(2, 3, 4)
    
    print(f"a.shape = {a.shape}")
    print()
    
    # axis=0: sum over first index
    # a.sum(axis=0)[j,k] = sum over i of a[i,j,k]
    print(f"sum(axis=0).shape = {a.sum(axis=0).shape}")
    
    # axis=1: sum over second index
    # a.sum(axis=1)[i,k] = sum over j of a[i,j,k]
    print(f"sum(axis=1).shape = {a.sum(axis=1).shape}")
    
    # axis=2: sum over third index
    # a.sum(axis=2)[i,j] = sum over k of a[i,j,k]
    print(f"sum(axis=2).shape = {a.sum(axis=2).shape}")

if __name__ == "__main__":
    main()
```

### 3. Multiple Axes

Reduce over multiple axes simultaneously with a tuple.

```python
import numpy as np

def main():
    a = np.arange(24).reshape(2, 3, 4)
    
    print(f"Original shape: {a.shape}")
    print()
    
    # Sum over axes 0 and 1
    print(f"sum(axis=(0,1)).shape: {a.sum(axis=(0,1)).shape}")
    
    # Sum over axes 1 and 2
    print(f"sum(axis=(1,2)).shape: {a.sum(axis=(1,2)).shape}")
    
    # Sum over all axes (equivalent to sum())
    print(f"sum(axis=(0,1,2)): {a.sum(axis=(0,1,2))}")
    print(f"sum(): {a.sum()}")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Create a 3D array of shape `(2, 3, 4)`. Compute `np.sum` along axis 0, axis 1, and axis 2. Print the resulting shape for each and verify they are `(3, 4)`, `(2, 4)`, and `(2, 3)` respectively.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(24).reshape(2, 3, 4)
        print(f"sum axis=0 shape: {np.sum(a, axis=0).shape}")  # (3, 4)
        print(f"sum axis=1 shape: {np.sum(a, axis=1).shape}")  # (2, 4)
        print(f"sum axis=2 shape: {np.sum(a, axis=2).shape}")  # (2, 3)

---

**Exercise 2.**
Compute the column means of a `(100, 5)` matrix using `np.mean(axis=0)`. Then use `keepdims=True` and verify the result has shape `(1, 5)` so it can be subtracted from the original matrix via broadcasting.

??? success "Solution to Exercise 2"

        import numpy as np

        M = np.random.randn(100, 5)
        means = np.mean(M, axis=0, keepdims=True)
        print(f"means shape: {means.shape}")  # (1, 5)
        centered = M - means
        print(f"Column means after centering: {centered.mean(axis=0).round(10)}")

---

**Exercise 3.**
Use `np.prod(axis=1)` to compute the row-wise product of a 4x3 matrix. Then use `np.cumsum(axis=0)` to compute the cumulative sum along columns. Print both results.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        row_prod = np.prod(a, axis=1)
        print(f"Row products: {row_prod}")

        col_cumsum = np.cumsum(a, axis=0)
        print(f"Column cumsum:\n{col_cumsum}")

---

**Exercise 4.**
Given a 3D array of shape `(4, 3, 5)`, predict the output shape of `a.sum(axis=1)` and `a.sum(axis=1, keepdims=True)`. Verify with NumPy. Explain why `keepdims=True` is essential when the result will be broadcast back against the original array.

??? success "Solution to Exercise 4"

        import numpy as np

        a = np.random.randn(4, 3, 5)
        r1 = a.sum(axis=1)
        r2 = a.sum(axis=1, keepdims=True)
        print(f"Without keepdims: {r1.shape}")  # (4, 5) — axis 1 removed
        print(f"With keepdims:    {r2.shape}")  # (4, 1, 5) — axis 1 kept as 1

        # Why keepdims matters: subtracting the sum from the original
        # a - r1  → (4, 3, 5) - (4, 5) → broadcasts along axis 1? No:
        #   (4, 3, 5) vs (4, 5) → right-align: 5==5, 3 vs 4 → FAIL
        # a - r2  → (4, 3, 5) - (4, 1, 5) → axis 1: 3 vs 1 → OK
        centered = a - r2
        print(f"Centered shape: {centered.shape}")  # (4, 3, 5)

---

**Exercise 5.**
Use `np.all` and `np.any` as reductions to check properties of a matrix. Given `M = np.random.randn(100, 5)`, verify (a) that at least one element per row is positive (`np.any(M > 0, axis=1)`), and (b) that no row has all negative values. Explain why these are reductions.

??? success "Solution to Exercise 5"

        import numpy as np

        M = np.random.randn(100, 5)

        # (a) At least one positive per row
        any_positive = np.any(M > 0, axis=1)  # (100,) boolean
        print(f"All rows have a positive: {np.all(any_positive)}")

        # (b) No row is all-negative
        all_negative = np.all(M < 0, axis=1)  # (100,) boolean
        print(f"Any all-negative row: {np.any(all_negative)}")

        # These are reductions because:
        # np.any(axis=1) collapses 5 columns into 1 boolean per row
        # np.all(axis=1) does the same — both remove axis 1
        # Input: (100, 5) → Output: (100,)
        # The "aggregation" is logical OR (any) or logical AND (all)
