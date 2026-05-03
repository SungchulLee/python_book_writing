# Broadcasting with Different ndims

!!! note "Advanced: Dimension Alignment"
    This page is a deep dive into Step 1 of the [broadcasting algorithm](broadcasting.md#the-complete-algorithm): left-padding with ones. If you are comfortable with same-rank broadcasting, this page explains the additional mechanics that kick in when arrays have different numbers of dimensions.

When two arrays have a different number of dimensions, NumPy automatically prepends size-1 dimensions to the smaller array until both shapes have the same length. This implicit alignment is the key mechanism that allows scalars, vectors, and matrices to interact seamlessly. Understanding exactly how this prepending works prevents shape-mismatch errors and clarifies which axis gets expanded.

!!! tip "Mental Model"
    When array dimensions don't match, NumPy pads the shorter shape with ones on the left until both shapes are the same length. A vector of shape `(4,)` paired with a matrix of shape `(3, 4)` becomes `(1, 4)` first, then broadcasts row-wise. The padding is always on the left -- if you need it on the right, you must add the axis yourself.

---

## Dimension Prepending Rule

NumPy pads the shorter shape on the left with ones.

### 1. How Alignment Works

```
Array A shape: (3, 4)      →  (3, 4)    already 2D
Array B shape: (4,)         →  (1, 4)    prepend 1 to match ndim
────────────────────────────────────────
Result shape:  (3, 4)       max along each axis
```

### 2. General Rule

If array A has `k` dimensions and array B has `m` dimensions with `k > m`, NumPy treats B as if it had shape `(1, 1, ..., 1, *B.shape)` with `k - m` ones prepended.

### 3. Code Verification

```python
import numpy as np

def main():
    A = np.ones((3, 4))       # 2D
    B = np.array([1, 2, 3, 4])  # 1D, shape (4,)
    C = A + B
    print(f"A.shape = {A.shape}")
    print(f"B.shape = {B.shape}")
    print(f"C.shape = {C.shape}")

if __name__ == "__main__":
    main()
```

Output:

```
A.shape = (3, 4)
B.shape = (4,)
C.shape = (3, 4)
```


## 1D + 2D

A 1D array broadcasts against a 2D array along the last axis.

### 1. Vector + Matrix

```python
import numpy as np

def main():
    M = np.array([[10, 20, 30],
                  [40, 50, 60]])   # (2, 3)
    v = np.array([1, 2, 3])        # (3,) → treated as (1, 3)
    result = M + v
    print(result)

if __name__ == "__main__":
    main()
```

Output:

```
[[11 22 33]
 [41 52 63]]
```

### 2. Shape Alignment Diagram

```
M:      (2, 3)
v:         (3,)   →   (1, 3)
─────────────────
result: (2, 3)
```

### 3. Adding Along Rows Instead

To add a vector along rows (axis 0), reshape it to a column vector first:

```python
import numpy as np

def main():
    M = np.array([[10, 20, 30],
                  [40, 50, 60]])   # (2, 3)
    v = np.array([100, 200])        # (2,) → need (2, 1)
    result = M + v[:, np.newaxis]
    print(result)

if __name__ == "__main__":
    main()
```

Output:

```
[[110 120 130]
 [240 250 260]]
```


## Scalar + Any Array

A scalar has shape `()` and broadcasts against any shape.

### 1. Scalar + 1D

```python
import numpy as np

def main():
    v = np.array([1, 2, 3])   # (3,)
    result = v + 10            # () → (1,) → (3,)
    print(result)              # [11 12 13]

if __name__ == "__main__":
    main()
```

### 2. Scalar + 3D

```python
import numpy as np

def main():
    A = np.ones((2, 3, 4))    # (2, 3, 4)
    result = A * 5             # () → (1, 1, 1) → (2, 3, 4)
    print(f"A.shape      = {A.shape}")
    print(f"result.shape = {result.shape}")

if __name__ == "__main__":
    main()
```

### 3. Shape Progression

```
Scalar shape: ()
  → prepend to match 3D: (1, 1, 1)
  → expand to match:     (2, 3, 4)
```


## 1D + 3D

A 1D array aligns with the last axis of a 3D array.

### 1. Example

```python
import numpy as np

def main():
    A = np.ones((2, 3, 4))       # (2, 3, 4)
    v = np.array([1, 2, 3, 4])   # (4,)
    result = A + v
    print(f"A.shape      = {A.shape}")
    print(f"v.shape      = {v.shape}")
    print(f"result.shape = {result.shape}")
    print("Last slice:\n", result[0, 0, :])

if __name__ == "__main__":
    main()
```

Output:

```
A.shape      = (2, 3, 4)
v.shape      = (4,)
result.shape = (2, 3, 4)
Last slice:
 [2. 3. 4. 5.]
```

### 2. Shape Alignment

```
A: (2, 3, 4)
v:       (4,)  →  (1, 1, 4)
──────────────
result: (2, 3, 4)
```

### 3. Aligning Along Middle Axis

To broadcast along axis 1 instead, reshape the vector:

```python
import numpy as np

def main():
    A = np.ones((2, 3, 4))
    v = np.array([10, 20, 30])              # (3,)
    v_reshaped = v[np.newaxis, :, np.newaxis]  # (1, 3, 1)
    result = A + v_reshaped
    print(f"v_reshaped.shape = {v_reshaped.shape}")
    print(f"result.shape     = {result.shape}")

if __name__ == "__main__":
    main()
```


## 2D + 3D

A 2D array broadcasts against a 3D array by prepending one size-1 dimension.

### 1. Example

```python
import numpy as np

def main():
    A = np.random.randn(5, 3, 4)  # (5, 3, 4)
    B = np.ones((3, 4))            # (3, 4) → (1, 3, 4)
    result = A + B
    print(f"A.shape      = {A.shape}")
    print(f"B.shape      = {B.shape}")
    print(f"result.shape = {result.shape}")

if __name__ == "__main__":
    main()
```

Output:

```
A.shape      = (5, 3, 4)
B.shape      = (3, 4)
result.shape = (5, 3, 4)
```

### 2. Shape Alignment

```
A: (5, 3, 4)
B:    (3, 4)  →  (1, 3, 4)
──────────────
result: (5, 3, 4)
```

### 3. Practical Use Case

Batch normalization: subtract the mean image from a batch of images.

```python
import numpy as np

def main():
    # Batch of 8 images, each 32x32
    batch = np.random.randn(8, 32, 32)    # (8, 32, 32)
    mean_image = batch.mean(axis=0)        # (32, 32)
    centered = batch - mean_image          # (8, 32, 32) - (32, 32)
    print(f"batch.shape      = {batch.shape}")
    print(f"mean_image.shape = {mean_image.shape}")
    print(f"centered.shape   = {centered.shape}")

if __name__ == "__main__":
    main()
```


## 4D + Lower Dimensions

Broadcasting scales to any number of dimensions.

### 1. 4D + 1D

```python
import numpy as np

def main():
    A = np.ones((2, 3, 4, 5))
    v = np.array([1, 2, 3, 4, 5])     # (5,) → (1, 1, 1, 5)
    result = A + v
    print(f"A.shape      = {A.shape}")
    print(f"v.shape      = {v.shape}")
    print(f"result.shape = {result.shape}")

if __name__ == "__main__":
    main()
```

### 2. 4D + 2D

```python
import numpy as np

def main():
    A = np.ones((2, 3, 4, 5))
    B = np.ones((4, 5))               # (4, 5) → (1, 1, 4, 5)
    result = A + B
    print(f"A.shape      = {A.shape}")
    print(f"B.shape      = {B.shape}")
    print(f"result.shape = {result.shape}")

if __name__ == "__main__":
    main()
```

### 3. 4D + 3D

```python
import numpy as np

def main():
    A = np.ones((2, 3, 4, 5))
    B = np.ones((3, 1, 5))            # (3, 1, 5) → (1, 3, 1, 5)
    result = A + B
    print(f"A.shape      = {A.shape}")
    print(f"B.shape      = {B.shape}")
    print(f"result.shape = {result.shape}")

if __name__ == "__main__":
    main()
```

Output:

```
A.shape      = (2, 3, 4, 5)
B.shape      = (3, 1, 5)
result.shape = (2, 3, 4, 5)
```


## Common Mistakes

Errors that arise from misunderstanding dimension prepending.

### 1. Wrong Axis Assumption

```python
import numpy as np

def main():
    M = np.ones((3, 4))
    v = np.array([1, 2, 3])  # (3,) — does NOT align with axis 0

    try:
        result = M + v  # Fails: (3, 4) vs (3,) — trailing dims 4 != 3
    except ValueError as e:
        print(f"Error: {e}")

    # Fix: reshape to (3, 1)
    result = M + v[:, np.newaxis]
    print(f"result.shape = {result.shape}")

if __name__ == "__main__":
    main()
```

### 2. Forgetting That Prepending is Left-Only

NumPy never appends dimensions on the right. A shape `(3,)` becomes `(1, 1, 3)` in a 3D context, never `(3, 1, 1)`. To align along a non-trailing axis, explicit reshaping is required.

### 3. Debugging with Shape Prints

When a broadcast fails, print both shapes and align them right to see where the mismatch occurs:

```python
import numpy as np

def main():
    A = np.ones((8, 3, 5))
    B = np.ones((3,))
    print(f"A: {A.shape}")      # (8, 3, 5)
    print(f"B: {B.shape}")      #       (3,) → trailing dim 3 != 5
    # Fix: B needs shape (3, 1) to align with axis 1
    B_fixed = B[:, np.newaxis]  # (3, 1)
    result = A + B_fixed
    print(f"result: {result.shape}")  # (8, 3, 5)

if __name__ == "__main__":
    main()
```


## Summary

When arrays have different numbers of dimensions, NumPy prepends size-1 dimensions to the shorter shape until both have the same ndim. The expanded dimensions then follow the standard broadcasting rule: size-1 stretches to match the other array.

| Scenario | Shapes | Prepended Shape | Result |
|---|---|---|---|
| Scalar + 2D | `() + (3, 4)` | `(1, 1)` | `(3, 4)` |
| 1D + 2D | `(4,) + (3, 4)` | `(1, 4)` | `(3, 4)` |
| 1D + 3D | `(4,) + (2, 3, 4)` | `(1, 1, 4)` | `(2, 3, 4)` |
| 2D + 3D | `(3, 4) + (5, 3, 4)` | `(1, 3, 4)` | `(5, 3, 4)` |
| 2D + 4D | `(4, 5) + (2, 3, 4, 5)` | `(1, 1, 4, 5)` | `(2, 3, 4, 5)` |

---

## Exercises

**Exercise 1.**
Given a 3D array `A` of shape `(4, 3, 5)` and a 1D array `v` of shape `(3,)`, reshape `v` so that it broadcasts along axis 1 of `A`. Compute `A + v_reshaped` and verify the result shape is `(4, 3, 5)`.

??? success "Solution to Exercise 1"

        import numpy as np

        A = np.random.randn(4, 3, 5)
        v = np.array([10, 20, 30])
        v_reshaped = v[np.newaxis, :, np.newaxis]  # (1, 3, 1)
        result = A + v_reshaped
        print(result.shape)  # (4, 3, 5)

---

**Exercise 2.**
Explain, without running the code, why `np.ones((3, 4)) + np.ones((4, 3))` raises a `ValueError`. Then fix it by reshaping one of the arrays so the addition succeeds and produces a shape `(3, 4)` result.

??? success "Solution to Exercise 2"

        import numpy as np

        # np.ones((3, 4)) + np.ones((4, 3)) fails because:
        # Right-aligned: (3, 4) vs (4, 3)
        # axis 1: 4 != 3, neither is 1 -> failure

        # Fix: transpose one array so shapes match
        A = np.ones((3, 4))
        B = np.ones((4, 3))
        result = A + B.T  # (3, 4) + (3, 4)
        print(result.shape)  # (3, 4)

---

**Exercise 3.**
A batch of 16 RGB images is stored as a 4D array of shape `(16, 3, 32, 32)` (batch, channels, height, width). Given per-channel means `mu = np.array([0.485, 0.456, 0.406])` of shape `(3,)`, subtract `mu` from each image by reshaping `mu` to align with the channels dimension. Verify that the result shape is `(16, 3, 32, 32)`.

??? success "Solution to Exercise 3"

        import numpy as np

        images = np.random.randn(16, 3, 32, 32)
        mu = np.array([0.485, 0.456, 0.406])
        mu_reshaped = mu[np.newaxis, :, np.newaxis, np.newaxis]  # (1, 3, 1, 1)
        result = images - mu_reshaped
        print(result.shape)  # (16, 3, 32, 32)

---

**Exercise 4.**
A 3D array `A` has shape `(batch, rows, cols) = (8, 5, 10)`. You want to add a bias vector `b` of shape `(5,)` to each row of each batch (axis 1). Show that `A + b` fails, explain why, and fix it by reshaping `b`. Verify the result shape.

??? success "Solution to Exercise 4"

        import numpy as np

        A = np.ones((8, 5, 10))
        b = np.array([1, 2, 3, 4, 5])  # (5,)

        # A + b fails because:
        # A: (8, 5, 10)
        # b:       (5,) → padded to (1, 1, 5)
        # axis 2: 10 vs 5 → FAIL (neither is 1)

        try:
            A + b
        except ValueError as e:
            print(f"Error: {e}")

        # Fix: reshape b to align with axis 1
        b_fixed = b[np.newaxis, :, np.newaxis]  # (1, 5, 1)
        result = A + b_fixed
        print(result.shape)  # (8, 5, 10)

        # Verification: each "row" (axis 1) gets a different bias
        print(result[0, :, 0])  # [2. 3. 4. 5. 6.]

---

**Exercise 5.**
Explain the difference between `v[:, np.newaxis]` and `v[np.newaxis, :]` for a 1D array `v` of shape `(4,)`. Show how each produces a different result when added to a `(3, 4)` matrix. Connect this to the "prepending is left-only" rule.

??? success "Solution to Exercise 5"

        import numpy as np

        v = np.array([10, 20, 30, 40])  # (4,)
        M = np.zeros((3, 4))

        # v[:, np.newaxis] → (4, 1): column vector
        # M + v[:, np.newaxis] → (3, 4) + (4, 1) → axis 0: 3 vs 4 → FAIL
        try:
            M + v[:, np.newaxis]
        except ValueError as e:
            print(f"Column vector fails: {e}")

        # v[np.newaxis, :] → (1, 4): row vector
        # M + v[np.newaxis, :] → (3, 4) + (1, 4) → (3, 4) ✓
        result = M + v[np.newaxis, :]
        print(f"Row vector works: {result.shape}")  # (3, 4)

        # But actually v alone (shape (4,)) also works:
        result2 = M + v  # (3, 4) + (4,) → pad to (1, 4) → (3, 4) ✓
        print(np.array_equal(result, result2))  # True

        # The "left-only" rule: NumPy pads (4,) to (1, 4), never to (4, 1).
        # If you WANT (4, 1) behavior, you must add the axis yourself.
        # This is why np.newaxis placement matters.
