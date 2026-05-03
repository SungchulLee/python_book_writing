# Stride Tricks

Strides control how NumPy traverses memory to access array elements.

!!! tip "Mental Model"
    Strides are the byte-level recipe for navigating an array: each axis has a stride telling NumPy how many bytes to jump to reach the next element along that axis. By manipulating strides (via `np.lib.stride_tricks`), you can create sliding windows, tiled views, or even circular buffers -- all without copying a single byte.

!!! note "Who Needs This?"
    Most NumPy users never manipulate strides directly — slicing, reshape, and transpose handle strides automatically. But understanding strides explains **why** certain operations are free (views) while others cost memory (copies), why transpose doesn't move data, and why contiguity affects performance. Strides are the mechanism behind the abstraction.


## Stride Fundamentals

A stride is the number of bytes between consecutive elements along an axis.

### 1. Definition

```python
import numpy as np

def main():
    x = np.arange(12).reshape(3, 4)
    print(f"{x.strides = }")
    print(f"{x.dtype.itemsize = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.strides = (32, 8)
x.dtype.itemsize = 8
```

### 2. Interpretation

- `32` bytes to move to the next row (4 elements × 8 bytes)
- `8` bytes to move to the next column (1 element × 8 bytes)

### 3. Memory Layout

Strides define how logical indices map to physical memory addresses.


## Viewing Strides

Different array operations produce different strides.

### 1. 1D Array Strides

```python
import numpy as np

def main():
    x = np.arange(10)
    print(f"{x.shape = }")
    print(f"{x.strides = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (10,)
x.strides = (8,)
```

### 2. Transposed Strides

```python
import numpy as np

def main():
    x = np.arange(12).reshape(3, 4)
    y = x.T
    print(f"{x.strides = }")
    print(f"{y.strides = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.strides = (32, 8)
y.strides = (8, 32)
```

### 3. Stride Swap

Transpose swaps strides without copying data.


## Sliding Windows

Create overlapping views efficiently using stride tricks.

### 1. Basic Window View

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def main():
    arr = np.arange(10)
    windowed = sliding_window_view(arr, window_shape=3)
    print(windowed)

if __name__ == "__main__":
    main()
```

Output:

```
[[0 1 2]
 [1 2 3]
 [2 3 4]
 [3 4 5]
 [4 5 6]
 [5 6 7]
 [6 7 8]
 [7 8 9]]
```

### 2. No Data Copy

Each row is a view into the original array, not a copy.

### 3. Memory Efficient

Only stores original data; windows share memory.


## Time Series Use

Sliding windows are essential for rolling computations.

### 1. Rolling Mean

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def main():
    data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    windows = sliding_window_view(data, window_shape=3)
    rolling_mean = windows.mean(axis=1)
    print(f"{rolling_mean = }")

if __name__ == "__main__":
    main()
```

Output:

```
rolling_mean = array([2., 3., 4., 5., 6., 7., 8., 9.])
```

### 2. Rolling Std

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def main():
    data = np.arange(10, dtype=float)
    windows = sliding_window_view(data, window_shape=3)
    rolling_std = windows.std(axis=1)
    print(f"{rolling_std = }")

if __name__ == "__main__":
    main()
```

### 3. Signal Processing

Sliding windows enable convolution, filtering, and feature extraction.


## 2D Sliding Windows

Apply sliding windows to matrices and images.

### 1. 2D Window Example

```python
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def main():
    arr = np.arange(16).reshape(4, 4)
    print("Original:")
    print(arr)
    
    windows = sliding_window_view(arr, window_shape=(2, 2))
    print(f"\nWindow shape: {windows.shape}")

if __name__ == "__main__":
    main()
```

Output:

```
Original:
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]
 [12 13 14 15]]

Window shape: (3, 3, 2, 2)
```

### 2. Image Patches

Extract overlapping patches for image processing or neural networks.


## Important Caveats

Stride manipulation requires careful handling.

### 1. Aliasing Risk

Multiple views share memory; modifying one affects others.

### 2. Read-Only Views

`sliding_window_view` returns read-only views by default for safety.

### 3. Undefined Behavior

Low-level stride manipulation via `as_strided` can cause segmentation faults if misused.


## Best Practices

Guidelines for safe stride manipulation.

### 1. Use High-Level API

Prefer `sliding_window_view` over manual `as_strided`.

### 2. Copy When Needed

If you must modify window data, copy first.

### 3. Validate Shapes

Always verify output shapes match expectations.

---

## Exercises

**Exercise 1.**
Create `a = np.arange(12).reshape(3, 4)`. Print its strides and explain what each stride value means in terms of bytes. Then create a Fortran-order version and compare strides.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(12).reshape(3, 4)
        print(f"C-order strides: {a.strides}")  # (32, 8)
        # 32 bytes to move one row (4 elements * 8 bytes)
        # 8 bytes to move one column (1 element * 8 bytes)

        b = np.asfortranarray(a)
        print(f"F-order strides: {b.strides}")  # (8, 24)

---

**Exercise 2.**
Create `a = np.arange(24, dtype=np.float32).reshape(2, 3, 4)`. Print the strides and manually compute the byte offset to access element `a[1, 2, 3]`. Verify by comparing with `a[1, 2, 3]`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(24, dtype=np.float32).reshape(2, 3, 4)
        print(f"Strides: {a.strides}")  # (48, 16, 4) for float32
        # Offset for [1, 2, 3] = 1*48 + 2*16 + 3*4 = 48+32+12 = 92
        print(f"a[1, 2, 3] = {a[1, 2, 3]}")  # 23.0

---

**Exercise 3.**
Use `np.lib.stride_tricks.as_strided` to create a sliding window view of `a = np.arange(10)` with window size 3 and step 1 (resulting shape `(8, 3)`). Print the result and verify no data was copied by checking that the result shares memory with `a`.

??? success "Solution to Exercise 3"

        import numpy as np
        from numpy.lib.stride_tricks import as_strided

        a = np.arange(10)
        window_size = 3
        shape = (len(a) - window_size + 1, window_size)
        strides = (a.strides[0], a.strides[0])
        windows = as_strided(a, shape=shape, strides=strides)

        print(windows)
        print(f"Shares memory: {np.shares_memory(a, windows)}")
