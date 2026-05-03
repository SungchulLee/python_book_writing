# Shape After Indexing

Indexing and slicing affect array dimensions differently.

!!! tip "Mental Model"
    A single integer index collapses that axis (the dimension disappears), while a slice preserves it -- even if the slice selects only one element. This is the most common source of "unexpected shape" bugs: `a[0]` drops a dimension, but `a[0:1]` keeps it.


## Index vs Slice

Single index reduces dimensions; slice preserves them.

### 1. Single Index

```python
import numpy as np

def main():
    a = np.zeros((8, 8, 8, 8))
    print(f"{a[1].shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1].shape = (8, 8, 8)
```

### 2. Slice of One

```python
import numpy as np

def main():
    a = np.zeros((8, 8, 8, 8))
    print(f"{a[1:2].shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1:2].shape = (1, 8, 8, 8)
```

### 3. Key Difference

`a[1]` removes a dimension; `a[1:2]` keeps it with size 1.


## Mixed Operations

Combining indices and slices on different axes.

### 1. Index Two Axes

```python
import numpy as np

def main():
    a = np.zeros((8, 8, 8, 8))
    print(f"{a[1, :, 3, :].shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1, :, 3, :].shape = (8, 8)
```

### 2. Index and Slice

```python
import numpy as np

def main():
    a = np.zeros((8, 8, 8, 8))
    print(f"{a[1:2, :, 3, :].shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1:2, :, 3, :].shape = (1, 8, 8)
```

### 3. All Slices

```python
import numpy as np

def main():
    a = np.zeros((8, 8, 8, 8))
    print(f"{a[1:2, :, 3:4, :].shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1:2, :, 3:4, :].shape = (1, 8, 1, 8)
```


## Complete Comparison

Side-by-side comparison of all cases.

### 1. Summary Table

```python
import numpy as np

def main():
    a = np.zeros((8, 8, 8, 8))
    print(f"{a[1].shape = }")
    print(f"{a[1:2].shape = }")
    print(f"{a[1, :, 3, :].shape = }")
    print(f"{a[1:2, :, 3, :].shape = }")
    print(f"{a[1:2, :, 3:4, :].shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1].shape = (8, 8, 8)
a[1:2].shape = (1, 8, 8, 8)
a[1, :, 3, :].shape = (8, 8)
a[1:2, :, 3, :].shape = (1, 8, 8)
a[1:2, :, 3:4, :].shape = (1, 8, 1, 8)
```

### 2. Dimension Rule

Each integer index removes one dimension; each slice keeps it.


!!! danger "Silent Bug: Shape Collapse"
    Shape collapse from accidental integer indexing is one of the most common sources of downstream errors. A function expecting a 2D array receives 1D because somewhere upstream `a[0]` was used instead of `a[0:1]`. The error message appears far from the actual cause. **When in doubt, use slices to preserve dimensions.**

## Practical Impact

Understanding shape changes is crucial for array operations.

### 1. Broadcasting

Shape mismatches cause broadcasting errors; use slices to preserve dimensions.

### 2. Neural Networks

Batch dimensions must be preserved; use `[0:1]` instead of `[0]`.

### 3. Matrix Operations

Some operations require 2D arrays; slicing maintains dimensionality.

---

## Exercises

**Exercise 1.**
Given `a = np.zeros((6, 5, 4, 3))`, predict the shape of each expression without running the code, then verify:

- `a[0]`
- `a[0:1]`
- `a[2, :, 1]`
- `a[2:3, :, 1:2]`

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.zeros((6, 5, 4, 3))
        print(a[0].shape)          # (5, 4, 3)
        print(a[0:1].shape)        # (1, 5, 4, 3)
        print(a[2, :, 1].shape)    # (5, 3)
        print(a[2:3, :, 1:2].shape)# (1, 5, 1, 3)

---

**Exercise 2.**
Create a 3D array `a = np.zeros((4, 3, 2))`. Extract a single row from the middle axis using an integer index (`a[:, 1, :]`) and using a slice (`a[:, 1:2, :]`). Print both shapes and explain why one has 2 dimensions and the other has 3.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.zeros((4, 3, 2))
        with_index = a[:, 1, :]     # integer index removes axis 1
        with_slice = a[:, 1:2, :]   # slice preserves axis 1

        print(f"Integer index shape: {with_index.shape}")  # (4, 2)
        print(f"Slice shape: {with_slice.shape}")          # (4, 1, 2)
        # The integer index removes the dimension entirely,
        # while the slice keeps it with size 1.

---

**Exercise 3.**
Given `images = np.random.randn(32, 3, 64, 64)` (a batch of 32 RGB images), extract the first image preserving all 4 dimensions (shape `(1, 3, 64, 64)`) using a slice. Then extract it with an integer index and verify the shape is `(3, 64, 64)`. Show how to restore the batch dimension using `np.expand_dims`.

??? success "Solution to Exercise 3"

        import numpy as np

        images = np.random.randn(32, 3, 64, 64)

        first_slice = images[0:1]
        print(f"With slice: {first_slice.shape}")  # (1, 3, 64, 64)

        first_index = images[0]
        print(f"With index: {first_index.shape}")  # (3, 64, 64)

        restored = np.expand_dims(first_index, axis=0)
        print(f"Restored: {restored.shape}")  # (1, 3, 64, 64)
