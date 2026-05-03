# Min Max Argmin Argmax

!!! tip "Mental Model"
    `min`/`max` tell you the extreme values; `argmin`/`argmax` tell you where those extremes live. Both accept an `axis` parameter to reduce along a specific dimension. Remember that `argmin`/`argmax` return flat indices by default -- use `np.unravel_index` to convert back to multi-dimensional coordinates.

## min and max

### 1. Basic Usage

Find minimum and maximum values across the entire array or along an axis.

```python
import numpy as np

def main():
    a = np.array([[5, 2],
                  [3, 5],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print(f"{a.min() = }")
    print(f"{a.max() = }")

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[5 2]
 [3 5]
 [2 3]]

a.min() = 2
a.max() = 5
```

### 2. With axis Parameter

```python
import numpy as np

def main():
    a = np.array([[5, 2],
                  [3, 5],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    # axis=0: min/max down columns
    print(f"{a.min(axis=0) = }")
    print(f"{a.max(axis=0) = }")
    print()
    
    # axis=1: min/max across rows
    print(f"{a.min(axis=1) = }")
    print(f"{a.max(axis=1) = }")

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[5 2]
 [3 5]
 [2 3]]

a.min(axis=0) = array([2, 2])
a.max(axis=0) = array([5, 5])

a.min(axis=1) = array([2, 3, 2])
a.max(axis=1) = array([5, 5, 3])
```

### 3. Function Syntax

```python
import numpy as np

def main():
    a = np.array([[5, 2],
                  [3, 5],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print(f"{np.min(a) = }")
    print(f"{np.min(a, axis=0) = }")
    print(f"{np.min(a, axis=1) = }")
    print()
    print(f"{np.max(a) = }")
    print(f"{np.max(a, axis=0) = }")
    print(f"{np.max(a, axis=1) = }")

if __name__ == "__main__":
    main()
```

## argmin and argmax

### 1. Basic Usage

Find the index (position) of minimum and maximum values.

```python
import numpy as np

def main():
    a = np.array([[5, 2],
                  [3, 5],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    # Flattened index
    print(f"{a.argmin() = }")  # index in flattened array
    print(f"{a.argmax() = }")

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[5 2]
 [3 5]
 [2 3]]

a.argmin() = 1
a.argmax() = 0
```

### 2. With axis Parameter

```python
import numpy as np

def main():
    a = np.array([[5, 2],
                  [3, 5],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    # axis=0: index of min/max in each column
    print(f"{a.argmin(axis=0) = }")
    print(f"{a.argmax(axis=0) = }")
    print()
    
    # axis=1: index of min/max in each row
    print(f"{a.argmin(axis=1) = }")
    print(f"{a.argmax(axis=1) = }")

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[5 2]
 [3 5]
 [2 3]]

a.argmin(axis=0) = array([2, 0])
a.argmax(axis=0) = array([0, 1])

a.argmin(axis=1) = array([1, 0, 0])
a.argmax(axis=1) = array([0, 1, 1])
```

### 3. Function Syntax

```python
import numpy as np

def main():
    a = np.array([[5, 2],
                  [3, 5],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print(f"{np.argmin(a) = }")
    print(f"{np.argmin(a, axis=0) = }")
    print(f"{np.argmin(a, axis=1) = }")
    print()
    print(f"{np.argmax(a) = }")
    print(f"{np.argmax(a, axis=0) = }")
    print(f"{np.argmax(a, axis=1) = }")

if __name__ == "__main__":
    main()
```

## Flat Index Convert

### 1. unravel_index

Convert flat index to multi-dimensional index.

```python
import numpy as np

def main():
    a = np.array([[5, 2],
                  [3, 5],
                  [2, 3]])
    
    flat_idx = a.argmin()
    print(f"Flat index of min: {flat_idx}")
    
    # Convert to 2D index
    idx_2d = np.unravel_index(flat_idx, a.shape)
    print(f"2D index: {idx_2d}")
    print(f"Value at index: {a[idx_2d]}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Flat index of min: 1
2D index: (0, 1)
Value at index: 2
```

### 2. Find Max Location

```python
import numpy as np

def main():
    a = np.array([[1, 5, 3],
                  [9, 2, 4],
                  [6, 8, 7]])
    
    print("a =")
    print(a)
    print()
    
    # Find location of maximum
    flat_idx = a.argmax()
    row, col = np.unravel_index(flat_idx, a.shape)
    
    print(f"Maximum value: {a.max()}")
    print(f"Location: row={row}, col={col}")
    print(f"Verify: a[{row}, {col}] = {a[row, col]}")

if __name__ == "__main__":
    main()
```

### 3. Multiple Maxima

`argmax` returns only the first occurrence.

```python
import numpy as np

def main():
    a = np.array([[5, 2, 5],
                  [3, 5, 1]])
    
    print("a =")
    print(a)
    print()
    
    # argmax returns first occurrence
    print(f"argmax(): {a.argmax()}")
    print(f"Location: {np.unravel_index(a.argmax(), a.shape)}")
    print()
    
    # Find all maxima
    max_val = a.max()
    all_max = np.argwhere(a == max_val)
    print(f"All locations of max ({max_val}):")
    print(all_max)

if __name__ == "__main__":
    main()
```

## Practical Examples

### 1. Best Parameters

```python
import numpy as np

def main():
    # Grid search results: rows=learning_rate, cols=momentum
    results = np.array([[0.85, 0.87, 0.86],
                        [0.88, 0.92, 0.89],
                        [0.84, 0.86, 0.85]])
    
    lr_values = [0.001, 0.01, 0.1]
    mom_values = [0.8, 0.9, 0.99]
    
    # Find best combination
    best_idx = np.unravel_index(results.argmax(), results.shape)
    best_lr = lr_values[best_idx[0]]
    best_mom = mom_values[best_idx[1]]
    
    print("Results grid:")
    print(results)
    print()
    print(f"Best accuracy: {results.max():.2f}")
    print(f"Best LR: {best_lr}")
    print(f"Best Momentum: {best_mom}")

if __name__ == "__main__":
    main()
```

### 2. Column-wise Best

```python
import numpy as np

def main():
    # Scores for 4 students on 3 tests
    scores = np.array([[85, 90, 78],
                       [92, 88, 95],
                       [78, 85, 82],
                       [88, 92, 90]])
    
    students = ["Alice", "Bob", "Carol", "David"]
    tests = ["Test1", "Test2", "Test3"]
    
    # Best student per test
    best_per_test = scores.argmax(axis=0)
    
    print("Scores:")
    print(scores)
    print()
    
    for i, test in enumerate(tests):
        best = students[best_per_test[i]]
        score = scores[best_per_test[i], i]
        print(f"{test}: {best} ({score})")

if __name__ == "__main__":
    main()
```

### 3. Row-wise Best

```python
import numpy as np

def main():
    # Prices from 3 vendors for 4 products
    prices = np.array([[10.5, 9.8, 10.2],
                       [25.0, 24.5, 26.0],
                       [5.5, 5.8, 5.2],
                       [15.0, 14.8, 15.5]])
    
    vendors = ["VendorA", "VendorB", "VendorC"]
    products = ["Widget", "Gadget", "Gizmo", "Doohickey"]
    
    # Cheapest vendor per product
    cheapest = prices.argmin(axis=1)
    
    print("Prices:")
    print(prices)
    print()
    
    for i, product in enumerate(products):
        vendor = vendors[cheapest[i]]
        price = prices[i, cheapest[i]]
        print(f"{product}: {vendor} (${price:.2f})")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Create a 2D array `a = np.random.randn(4, 5)`. Find the global min and max, then find the min and max along each axis (rows and columns).

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.random.randn(4, 5)
        print(f"Global min: {a.min():.4f}, max: {a.max():.4f}")
        print(f"Column min: {a.min(axis=0)}")
        print(f"Row max: {a.max(axis=1)}")

---

**Exercise 2.**
Use `np.argmin` and `np.argmax` to find the indices of the minimum and maximum elements in a 1D array. Then use `np.unravel_index` to find the 2D indices of the min/max in a 3x4 matrix.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.random.randn(12)
        print(f"argmin: {np.argmin(a)}, argmax: {np.argmax(a)}")

        M = np.random.randn(3, 4)
        flat_idx = np.argmin(M)
        idx_2d = np.unravel_index(flat_idx, M.shape)
        print(f"2D argmin: {idx_2d}, value: {M[idx_2d]:.4f}")

---

**Exercise 3.**
Compute the range (max - min) of each row in a `(100, 5)` array using `axis=1` in a single expression. Verify by computing manually with a loop.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.random.randn(100, 5)
        ranges = a.max(axis=1) - a.min(axis=1)
        ranges_manual = np.array([row.max() - row.min() for row in a])
        print(f"Match: {np.allclose(ranges, ranges_manual)}")

---

**Exercise 4.**
Use `np.argmax` with `np.unravel_index` to find the location of the maximum value in a 3D array of shape `(4, 5, 6)`. Print the flat index, the 3D index, and the value at that location.

??? success "Solution to Exercise 4"

        import numpy as np

        a = np.random.randn(4, 5, 6)
        flat_idx = np.argmax(a)
        idx_3d = np.unravel_index(flat_idx, a.shape)
        print(f"Flat index: {flat_idx}")
        print(f"3D index:   {idx_3d}")
        print(f"Value:      {a[idx_3d]}")
        print(f"Matches max: {a[idx_3d] == a.max()}")  # True

---

**Exercise 5.**
Given a matrix of exam scores `scores` with shape `(30, 4)` (30 students, 4 exams), use `argmax(axis=1)` to find which exam each student scored highest on. Then count how many students scored highest on each exam using `np.bincount`.

??? success "Solution to Exercise 5"

        import numpy as np

        scores = np.random.randint(50, 100, size=(30, 4))
        best_exam = np.argmax(scores, axis=1)  # (30,)
        counts = np.bincount(best_exam, minlength=4)

        for exam in range(4):
            print(f"Exam {exam}: {counts[exam]} students scored highest")
        print(f"Total: {counts.sum()}")  # 30
