# Searching Arrays

!!! tip "Mental Model"
    `np.searchsorted` performs binary search on a sorted array, returning the index where a value would be inserted to keep the array sorted. It runs in O(log n) time and is the NumPy equivalent of Python's `bisect` module. Use `np.where` and `np.nonzero` for general-purpose element searching in unsorted arrays.

    The unifying idea: **search = mapping values to positions in a structure.**
    `searchsorted` maps values to indices in a sorted array; `np.where` maps a
    boolean condition to the positions where it holds. Both convert "what" questions
    into "where" answers — the bridge between values and their locations.

## np.searchsorted

### 1. Basic Usage

`np.searchsorted` finds insertion points to maintain sorted order.

```python
import numpy as np

def main():
    a = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    v = 3.14
    
    idx = np.searchsorted(a, v)
    
    print(f"Array: {a}")
    print(f"Value: {v}")
    print(f"Insert at index: {idx}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Array: [0 1 2 3 4 5 6 7 8 9]
Value: 3.14
Insert at index: 4
```

### 2. Left vs Right

`side` parameter controls behavior for equal values.

```python
import numpy as np

def main():
    a = np.array([1, 2, 2, 2, 3, 4, 5])
    v = 2
    
    left_idx = np.searchsorted(a, v, side='left')
    right_idx = np.searchsorted(a, v, side='right')
    
    print(f"Array: {a}")
    print(f"Value: {v}")
    print(f"Left index:  {left_idx}")
    print(f"Right index: {right_idx}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Array: [1 2 2 2 3 4 5]
Value: 2
Left index:  1
Right index: 4
```

### 3. Multiple Values

```python
import numpy as np

def main():
    a = np.array([0, 10, 20, 30, 40, 50])
    values = np.array([5, 15, 25, 35])
    
    indices = np.searchsorted(a, values)
    
    print(f"Array:   {a}")
    print(f"Values:  {values}")
    print(f"Indices: {indices}")

if __name__ == "__main__":
    main()
```

## Practical Uses

### 1. Binning Data

Assign values to bins.

```python
import numpy as np

def main():
    bins = np.array([0, 10, 20, 30, 40, 50])
    data = np.array([5, 15, 25, 35, 45, 55, -5])
    
    bin_indices = np.searchsorted(bins, data)
    
    print(f"Bins: {bins}")
    print(f"Data: {data}")
    print(f"Bin indices: {bin_indices}")
    print()
    
    for d, idx in zip(data, bin_indices):
        if idx == 0:
            print(f"  {d}: below first bin")
        elif idx == len(bins):
            print(f"  {d}: above last bin")
        else:
            print(f"  {d}: bin [{bins[idx-1]}, {bins[idx]})")

if __name__ == "__main__":
    main()
```

### 2. Interpolation Lookup

Find surrounding values for interpolation.

```python
import numpy as np

def main():
    # Known data points
    x_known = np.array([0, 1, 2, 3, 4, 5])
    y_known = np.array([0, 1, 4, 9, 16, 25])  # y = x^2
    
    # Query point
    x_query = 2.5
    
    # Find position
    idx = np.searchsorted(x_known, x_query)
    
    # Linear interpolation
    x0, x1 = x_known[idx-1], x_known[idx]
    y0, y1 = y_known[idx-1], y_known[idx]
    
    t = (x_query - x0) / (x1 - x0)
    y_interp = y0 + t * (y1 - y0)
    
    print(f"Query x: {x_query}")
    print(f"Between x[{idx-1}]={x0} and x[{idx}]={x1}")
    print(f"Interpolated y: {y_interp}")
    print(f"Actual x^2: {x_query**2}")

if __name__ == "__main__":
    main()
```

### 3. Histogram Counts

```python
import numpy as np

def main():
    np.random.seed(42)
    data = np.random.randn(1000)
    
    bin_edges = np.array([-3, -2, -1, 0, 1, 2, 3])
    
    # Find bin for each data point
    bin_idx = np.searchsorted(bin_edges, data)
    
    # Count per bin (excluding out of range)
    counts = np.bincount(bin_idx, minlength=len(bin_edges)+1)
    
    print("Bin edges:", bin_edges)
    print("Counts:", counts[1:-1])  # exclude under/over
    print()
    
    # Verify with np.histogram
    hist_counts, _ = np.histogram(data, bins=bin_edges)
    print("np.histogram:", hist_counts)

if __name__ == "__main__":
    main()
```

## Requirements

### 1. Sorted Input

`np.searchsorted` requires the input array to be sorted.

```python
import numpy as np

def main():
    # Correct: sorted array
    a_sorted = np.array([1, 3, 5, 7, 9])
    idx = np.searchsorted(a_sorted, 4)
    print(f"Sorted array: {a_sorted}")
    print(f"Index for 4: {idx}")
    print()
    
    # Incorrect: unsorted array gives wrong results
    a_unsorted = np.array([5, 1, 9, 3, 7])
    idx_wrong = np.searchsorted(a_unsorted, 4)
    print(f"Unsorted array: {a_unsorted}")
    print(f"Index for 4: {idx_wrong} (incorrect!)")

if __name__ == "__main__":
    main()
```

### 2. Sort First

```python
import numpy as np

def main():
    data = np.array([5, 1, 9, 3, 7])
    
    # Sort first
    sorted_data = np.sort(data)
    
    # Now searchsorted works correctly
    idx = np.searchsorted(sorted_data, 4)
    
    print(f"Original: {data}")
    print(f"Sorted:   {sorted_data}")
    print(f"Index for 4: {idx}")

if __name__ == "__main__":
    main()
```

### 3. Binary Search

`np.searchsorted` uses binary search, so it's O(log n).

```python
import numpy as np

def main():
    # Even with large arrays, searchsorted is fast
    large_array = np.arange(1_000_000)
    
    # Find insertion point for many values
    queries = np.array([100, 50000, 999999])
    
    indices = np.searchsorted(large_array, queries)
    
    print(f"Array size: {len(large_array):,}")
    print(f"Queries: {queries}")
    print(f"Indices: {indices}")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Create a sorted array `a = np.array([1, 3, 5, 7, 9, 11])`. Use `np.searchsorted` to find the insertion indices for values `[2, 6, 11]` using both `side='left'` and `side='right'`.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([1, 3, 5, 7, 9, 11])
        vals = np.array([2, 6, 11])
        left = np.searchsorted(a, vals, side='left')
        right = np.searchsorted(a, vals, side='right')
        print(f"Left:  {left}")
        print(f"Right: {right}")

---

**Exercise 2.**
Use `np.argwhere` to find all positions where a 4x4 matrix has values greater than 0.5. Print the indices and the corresponding values.

??? success "Solution to Exercise 2"

        import numpy as np

        np.random.seed(42)
        M = np.random.rand(4, 4)
        indices = np.argwhere(M > 0.5)
        print(f"Positions where > 0.5:\n{indices}")
        for idx in indices:
            print(f"  M{tuple(idx)} = {M[tuple(idx)]:.4f}")

---

**Exercise 3.**
Use `np.nonzero` to find all non-zero elements in a sparse array created by `a = np.zeros(20); a[[3, 7, 12, 18]] = [1, 2, 3, 4]`. Print the non-zero indices and values.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.zeros(20)
        a[[3, 7, 12, 18]] = [1, 2, 3, 4]
        nz = np.nonzero(a)
        print(f"Non-zero indices: {nz[0]}")
        print(f"Non-zero values: {a[nz]}")

---

**Exercise 4.**
Use `np.searchsorted` to bin 1000 random values into bins defined by edges `[0, 0.25, 0.5, 0.75, 1.0]`. Count how many values fall into each bin and verify the counts sum to 1000.

??? success "Solution to Exercise 4"

        import numpy as np

        values = np.random.rand(1000)
        edges = np.array([0, 0.25, 0.5, 0.75, 1.0])
        bins = np.searchsorted(edges, values, side='right') - 1
        counts = np.bincount(bins, minlength=4)

        for i in range(4):
            print(f"Bin [{edges[i]:.2f}, {edges[i+1]:.2f}): {counts[i]}")
        print(f"Total: {counts.sum()}")  # 1000

---

**Exercise 5.**
Use `np.argwhere` to find all positions in a 2D boolean mask where the value is `True`. Given `M = np.random.randn(5, 5)`, create a mask `M > 1.0` and print the coordinates and values of all elements exceeding 1.0.

??? success "Solution to Exercise 5"

        import numpy as np

        np.random.seed(42)
        M = np.random.randn(5, 5)
        mask = M > 1.0
        positions = np.argwhere(mask)

        print(f"Elements > 1.0:")
        for pos in positions:
            r, c = pos
            print(f"  M[{r}, {c}] = {M[r, c]:.4f}")
