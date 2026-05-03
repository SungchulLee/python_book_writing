# Splitting Arrays

NumPy provides functions to split arrays into multiple sub-arrays.

!!! tip "Mental Model"
    Splitting is the reverse of concatenation: it divides one array into a list of smaller arrays along a specified axis. `np.split` requires equal-sized chunks (or explicit cut points), while `np.array_split` handles remainders gracefully by distributing extra elements across the first few chunks.

!!! info "Core Concept"
    Splitting is **partitioning data along an axis** — the inverse of concatenation. If you concatenated arrays A, B, C along axis 0, splitting the result along axis 0 gives you A, B, C back.

## np.split

### 1. Equal Parts

```python
import numpy as np

def main():
    a = np.arange(12)
    
    # Split into 3 equal parts
    parts = np.split(a, 3)
    
    print(f"Original: {a}")
    print(f"Number of parts: {len(parts)}")
    for i, part in enumerate(parts):
        print(f"Part {i}: {part}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Original: [ 0  1  2  3  4  5  6  7  8  9 10 11]
Number of parts: 3
Part 0: [0 1 2 3]
Part 1: [4 5 6 7]
Part 2: [ 8  9 10 11]
```

### 2. Split at Indices

```python
import numpy as np

def main():
    a = np.arange(10)
    
    # Split at indices 3 and 7
    parts = np.split(a, [3, 7])
    
    print(f"Original: {a}")
    print(f"Split at [3, 7]:")
    for i, part in enumerate(parts):
        print(f"  Part {i}: {part}")

if __name__ == "__main__":
    main()
```

### 3. 2D Array Split

```python
import numpy as np

def main():
    a = np.arange(12).reshape(3, 4)
    
    print("Original:")
    print(a)
    print()
    
    # Split along axis=0 (rows)
    parts = np.split(a, 3, axis=0)
    print("Split along axis=0:")
    for i, part in enumerate(parts):
        print(f"Part {i}: {part}")

if __name__ == "__main__":
    main()
```

## np.array_split

### 1. Unequal Splits

```python
import numpy as np

def main():
    a = np.arange(10)
    
    # np.split would fail (10 not divisible by 3)
    # np.array_split handles unequal splits
    parts = np.array_split(a, 3)
    
    print(f"Original: {a}")
    print(f"Split into 3 parts:")
    for i, part in enumerate(parts):
        print(f"  Part {i}: {part} (length {len(part)})")

if __name__ == "__main__":
    main()
```

### 2. Comparison with split

```python
import numpy as np

def main():
    a = np.arange(10)
    
    # np.split requires equal division
    try:
        parts = np.split(a, 3)
    except ValueError as e:
        print(f"np.split error: {e}")
    
    # np.array_split allows unequal
    parts = np.array_split(a, 3)
    print(f"np.array_split works: {[len(p) for p in parts]}")

if __name__ == "__main__":
    main()
```

### 3. Distribution of Elements

```python
import numpy as np

def main():
    a = np.arange(17)
    
    for n in [2, 3, 4, 5]:
        parts = np.array_split(a, n)
        sizes = [len(p) for p in parts]
        print(f"Split 17 into {n}: sizes = {sizes}")

if __name__ == "__main__":
    main()
```

## np.hsplit

### 1. Horizontal Split

```python
import numpy as np

def main():
    a = np.arange(12).reshape(3, 4)
    
    print("Original:")
    print(a)
    print()
    
    # Split into 2 parts horizontally
    left, right = np.hsplit(a, 2)
    
    print("Left:")
    print(left)
    print()
    print("Right:")
    print(right)

if __name__ == "__main__":
    main()
```

### 2. Split at Column Indices

```python
import numpy as np

def main():
    a = np.arange(20).reshape(4, 5)
    
    print("Original:")
    print(a)
    print()
    
    # Split at columns 1 and 3
    parts = np.hsplit(a, [1, 3])
    
    for i, part in enumerate(parts):
        print(f"Part {i}:")
        print(part)
        print()

if __name__ == "__main__":
    main()
```

### 3. Equivalent to split axis=1

```python
import numpy as np

def main():
    a = np.arange(12).reshape(3, 4)
    
    parts1 = np.hsplit(a, 2)
    parts2 = np.split(a, 2, axis=1)
    
    print(f"hsplit equal to split axis=1: {np.array_equal(parts1[0], parts2[0])}")

if __name__ == "__main__":
    main()
```

## np.vsplit

### 1. Vertical Split

```python
import numpy as np

def main():
    a = np.arange(12).reshape(4, 3)
    
    print("Original:")
    print(a)
    print()
    
    # Split into 2 parts vertically
    top, bottom = np.vsplit(a, 2)
    
    print("Top:")
    print(top)
    print()
    print("Bottom:")
    print(bottom)

if __name__ == "__main__":
    main()
```

### 2. Split at Row Indices

```python
import numpy as np

def main():
    a = np.arange(20).reshape(5, 4)
    
    print("Original:")
    print(a)
    print()
    
    # Split at rows 1 and 3
    parts = np.vsplit(a, [1, 3])
    
    for i, part in enumerate(parts):
        print(f"Part {i} (shape {part.shape}):")
        print(part)
        print()

if __name__ == "__main__":
    main()
```

### 3. Equivalent to split axis=0

```python
import numpy as np

def main():
    a = np.arange(12).reshape(4, 3)
    
    parts1 = np.vsplit(a, 2)
    parts2 = np.split(a, 2, axis=0)
    
    print(f"vsplit equal to split axis=0: {np.array_equal(parts1[0], parts2[0])}")

if __name__ == "__main__":
    main()
```

## np.dsplit

### 1. Depth Split

```python
import numpy as np

def main():
    a = np.arange(24).reshape(2, 3, 4)
    
    print(f"Original shape: {a.shape}")
    
    # Split along axis=2
    parts = np.dsplit(a, 2)
    
    print(f"Number of parts: {len(parts)}")
    for i, part in enumerate(parts):
        print(f"Part {i} shape: {part.shape}")

if __name__ == "__main__":
    main()
```

### 2. Split RGB Channels

```python
import numpy as np

def main():
    # Simulated RGB image
    image = np.random.randint(0, 256, (100, 100, 3))
    
    print(f"Image shape: {image.shape}")
    
    # Split into channels
    r, g, b = np.dsplit(image, 3)
    
    print(f"Red channel shape: {r.shape}")
    
    # Squeeze to get 2D
    r_2d = r.squeeze()
    print(f"Squeezed shape: {r_2d.shape}")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Train/Test Split

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Dataset
    X = np.random.randn(100, 5)
    y = np.random.randint(0, 2, 100)
    
    # 80/20 split
    split_idx = int(0.8 * len(X))
    
    X_train, X_test = np.split(X, [split_idx])
    y_train, y_test = np.split(y, [split_idx])
    
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")

if __name__ == "__main__":
    main()
```

### 2. Batch Processing

```python
import numpy as np

def main():
    data = np.arange(1000)
    batch_size = 32
    
    n_batches = len(data) // batch_size
    batches = np.split(data[:n_batches * batch_size], n_batches)
    
    print(f"Number of batches: {len(batches)}")
    print(f"Batch shape: {batches[0].shape}")

if __name__ == "__main__":
    main()
```

### 3. K-Fold Cross-Validation

```python
import numpy as np

def main():
    data = np.arange(100)
    n_folds = 5
    
    folds = np.array_split(data, n_folds)
    
    for i in range(n_folds):
        test = folds[i]
        train = np.concatenate([folds[j] for j in range(n_folds) if j != i])
        print(f"Fold {i}: train={len(train)}, test={len(test)}")

if __name__ == "__main__":
    main()
```

## Summary Table

### 1. Split Functions

| Function | Description |
|:---------|:------------|
| `np.split(a, n)` | Split into n equal parts |
| `np.split(a, [i,j])` | Split at indices i, j |
| `np.array_split(a, n)` | Split into n parts (unequal OK) |
| `np.hsplit(a, n)` | Split horizontally (axis=1) |
| `np.vsplit(a, n)` | Split vertically (axis=0) |
| `np.dsplit(a, n)` | Split depth-wise (axis=2) |

### 2. Equivalences

| Function | Equivalent |
|:---------|:-----------|
| `np.hsplit(a, n)` | `np.split(a, n, axis=1)` |
| `np.vsplit(a, n)` | `np.split(a, n, axis=0)` |
| `np.dsplit(a, n)` | `np.split(a, n, axis=2)` |

---

## Exercises

**Exercise 1.**
Create `a = np.arange(12)`. Split it into 3 equal parts using `np.split` and into parts of sizes 2, 5, 5 using `np.split` with explicit indices.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(12)
        parts_equal = np.split(a, 3)
        for i, p in enumerate(parts_equal):
            print(f"Part {i}: {p}")

        parts_custom = np.split(a, [2, 7])
        for i, p in enumerate(parts_custom):
            print(f"Custom part {i}: {p}")

---

**Exercise 2.**
Create a 4x6 matrix. Use `np.hsplit` to split it into 3 equal column blocks and `np.vsplit` to split it into 2 equal row blocks. Print the shapes of each resulting block.

??? success "Solution to Exercise 2"

        import numpy as np

        M = np.arange(24).reshape(4, 6)
        col_blocks = np.hsplit(M, 3)
        for i, b in enumerate(col_blocks):
            print(f"Col block {i}: shape {b.shape}")

        row_blocks = np.vsplit(M, 2)
        for i, b in enumerate(row_blocks):
            print(f"Row block {i}: shape {b.shape}")

---

**Exercise 3.**
Create `a = np.arange(10)`. Use `np.array_split` to split it into 3 parts (which handles uneven division). Print the lengths of each part and verify they sum to 10.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.arange(10)
        parts = np.array_split(a, 3)
        lengths = [len(p) for p in parts]
        print(f"Lengths: {lengths}")  # [4, 3, 3]
        print(f"Sum: {sum(lengths)}")  # 10
