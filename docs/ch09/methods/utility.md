# Utility Functions

!!! tip "Mental Model"
    Utility functions like `np.round`, `np.clip`, `np.unique`, and `np.diff` handle the small but essential data-wrangling steps that sit between major computations. They are all vectorized, so there is no need to loop. Think of them as the **data cleaning and preprocessing layer** — the stage that converts raw arrays into analysis-ready form by enforcing bounds, removing duplicates, and detecting changes.

## np.round

### 1. Basic Usage

Round to specified decimal places.

```python
import numpy as np

def main():
    x = np.round(3.146592, 2)
    print(f"np.round(3.146592, 2) = {x}")
    
    y = np.round(-3.146592, 2)
    print(f"np.round(-3.146592, 2) = {y}")

if __name__ == "__main__":
    main()
```

**Output:**

```
np.round(3.146592, 2) = 3.15
np.round(-3.146592, 2) = -3.15
```

### 2. Array Rounding

```python
import numpy as np

def main():
    x = np.array([93.324, 84.237, -73.237, 68.342])
    
    print("Original:")
    print(x)
    print()
    
    rounded = np.round(x, 2)
    print("Rounded to 2 decimals:")
    print(rounded)

if __name__ == "__main__":
    main()
```

### 3. 2D Array

```python
import numpy as np

def main():
    x = np.array([
        [93.324, 84.237, -73.237, 68.342],
        [97.234, 67.236, -57.236, 23.567],
        [87.243, 87.423, -38.253, 77.342]
    ])
    
    print("Original:")
    print(x)
    print()
    
    rounded = np.round(x, 2)
    print("Rounded:")
    print(rounded)

if __name__ == "__main__":
    main()
```

## np.isnan

### 1. Basic Usage

Check for NaN (Not a Number) values.

```python
import numpy as np

def main():
    x = np.array([1.0, np.nan, 3.0, np.nan, 5.0])
    
    print(f"Array: {x}")
    print(f"isnan: {np.isnan(x)}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Array: [ 1. nan  3. nan  5.]
isnan: [False  True False  True False]
```

### 2. 2D Array

```python
import numpy as np

def main():
    x = np.array([
        [93., 84., 73., 68.],
        [97., 67., 57., np.nan],
        [87., 87., np.nan, 77.]
    ])
    
    print("Array:")
    print(x)
    print()
    
    bool_nan = np.isnan(x)
    print("isnan result:")
    print(bool_nan)

if __name__ == "__main__":
    main()
```

### 3. With np.round

NaN values pass through rounding unchanged.

```python
import numpy as np

def main():
    x = np.array([
        [93.324, 84.237, -73.237, 68.342],
        [97.234, 67.236, -57.236, np.nan],
        [87.243, np.nan, -38.253, 77.342]
    ])
    
    print("Original:")
    print(x)
    print()
    
    rounded = np.round(x, 2)
    print("Rounded (NaN preserved):")
    print(rounded)

if __name__ == "__main__":
    main()
```

## np.nonzero

### 1. Basic Usage

Return indices of non-zero elements.

```python
import numpy as np

def main():
    a = np.array([0, 1, 0, 2, 0, 3])
    
    indices = np.nonzero(a)
    
    print(f"Array: {a}")
    print(f"Nonzero indices: {indices}")
    print(f"Nonzero values: {a[indices]}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Array: [0 1 0 2 0 3]
Nonzero indices: (array([1, 3, 5]),)
Nonzero values: [1 2 3]
```

### 2. With Boolean Condition

```python
import numpy as np

def main():
    np.random.seed(80085)
    scores = np.round(np.random.uniform(low=30, high=100, size=10))
    
    print(f"Scores: {scores}")
    print()
    
    # Boolean mask
    failing = scores < 60
    print(f"Failing mask: {failing}")
    
    # Indices of failing scores
    fail_indices = np.nonzero(failing)
    print(f"Failing indices: {fail_indices}")
    print(f"Failing indices [0]: {fail_indices[0]}")

if __name__ == "__main__":
    main()
```

### 3. Modify Subset

```python
import numpy as np

def main():
    np.random.seed(80085)
    scores = np.round(np.random.uniform(low=30, high=100, size=10))
    
    print(f"Original: {scores}")
    
    # Find first 3 failing indices
    fail_idx = np.nonzero(scores < 60)[0][:3]
    print(f"First 3 failing indices: {fail_idx}")
    
    # Zero them out
    scores[fail_idx] = 0.
    print(f"Modified: {scores}")

if __name__ == "__main__":
    main()
```

## np.nan Functions

### 1. np.nansum

Sum ignoring NaN values.

```python
import numpy as np

def main():
    a = np.array([1, 2, np.nan, 4, 5])
    
    print(f"Array: {a}")
    print(f"np.sum(a):    {np.sum(a)}")      # NaN propagates
    print(f"np.nansum(a): {np.nansum(a)}")   # Ignores NaN

if __name__ == "__main__":
    main()
```

### 2. np.nanmean

Mean ignoring NaN values.

```python
import numpy as np

def main():
    a = np.array([[1, 2, np.nan],
                  [4, np.nan, 6]])
    
    print("Array:")
    print(a)
    print()
    
    print(f"np.mean(a):    {np.mean(a)}")
    print(f"np.nanmean(a): {np.nanmean(a)}")
    print()
    
    print(f"np.nanmean(a, axis=0): {np.nanmean(a, axis=0)}")
    print(f"np.nanmean(a, axis=1): {np.nanmean(a, axis=1)}")

if __name__ == "__main__":
    main()
```

### 3. Complete nan Family

```python
import numpy as np

def main():
    a = np.array([1, 2, np.nan, 4, np.nan, 6])
    
    print(f"Array: {a}")
    print()
    
    funcs = [
        ("nansum", np.nansum),
        ("nanmean", np.nanmean),
        ("nanstd", np.nanstd),
        ("nanvar", np.nanvar),
        ("nanmin", np.nanmin),
        ("nanmax", np.nanmax),
        ("nanmedian", np.nanmedian),
    ]
    
    for name, func in funcs:
        print(f"np.{name:10}(a) = {func(a):.4f}")

if __name__ == "__main__":
    main()
```

## np.unique

### 1. Basic Usage

Extract unique elements from an array.

```python
import numpy as np

def main():
    a = np.array([3, 1, 2, 1, 3, 2, 1, 4, 3])
    
    unique_vals = np.unique(a)
    
    print(f"Original: {a}")
    print(f"Unique:   {unique_vals}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Original: [3 1 2 1 3 2 1 4 3]
Unique:   [1 2 3 4]
```

### 2. Return Indices

```python
import numpy as np

def main():
    a = np.array([3, 1, 2, 1, 3, 2, 1, 4, 3])
    
    # return_index: first occurrence of each unique value
    unique_vals, first_idx = np.unique(a, return_index=True)
    
    print(f"Original: {a}")
    print(f"Unique values: {unique_vals}")
    print(f"First indices: {first_idx}")
    print(f"Verify: a[first_idx] = {a[first_idx]}")

if __name__ == "__main__":
    main()
```

### 3. Return Inverse

```python
import numpy as np

def main():
    a = np.array([3, 1, 2, 1, 3, 2, 1, 4, 3])
    
    # return_inverse: indices to reconstruct original
    unique_vals, inverse = np.unique(a, return_inverse=True)
    
    print(f"Original: {a}")
    print(f"Unique: {unique_vals}")
    print(f"Inverse: {inverse}")
    print(f"Reconstruct: {unique_vals[inverse]}")

if __name__ == "__main__":
    main()
```

## np.unique Counts

### 1. Return Counts

```python
import numpy as np

def main():
    a = np.array([3, 1, 2, 1, 3, 2, 1, 4, 3])
    
    unique_vals, counts = np.unique(a, return_counts=True)
    
    print(f"Original: {a}")
    print(f"Unique: {unique_vals}")
    print(f"Counts: {counts}")
    
    # Most frequent
    most_freq_idx = np.argmax(counts)
    print(f"Most frequent: {unique_vals[most_freq_idx]} ({counts[most_freq_idx]} times)")

if __name__ == "__main__":
    main()
```

### 2. All Returns

```python
import numpy as np

def main():
    a = np.array([3, 1, 2, 1, 3, 2, 1, 4, 3])
    
    unique_vals, first_idx, inverse, counts = np.unique(
        a, return_index=True, return_inverse=True, return_counts=True
    )
    
    print(f"Unique values: {unique_vals}")
    print(f"First indices: {first_idx}")
    print(f"Inverse:       {inverse}")
    print(f"Counts:        {counts}")

if __name__ == "__main__":
    main()
```

### 3. 2D Arrays

```python
import numpy as np

def main():
    a = np.array([[1, 2, 1],
                  [3, 2, 1],
                  [1, 2, 1]])
    
    # Unique elements (flattened by default)
    print(f"Unique elements: {np.unique(a)}")
    
    # Unique rows
    unique_rows = np.unique(a, axis=0)
    print(f"Unique rows:\n{unique_rows}")

if __name__ == "__main__":
    main()
```

## np.unique Applications

### 1. Category Encoding

```python
import numpy as np

def main():
    labels = np.array(['cat', 'dog', 'cat', 'bird', 'dog', 'cat'])
    
    unique_labels, encoded = np.unique(labels, return_inverse=True)
    
    print(f"Original: {labels}")
    print(f"Categories: {unique_labels}")
    print(f"Encoded: {encoded}")

if __name__ == "__main__":
    main()
```

### 2. Value Counts

```python
import numpy as np

def main():
    data = np.array([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
    
    values, counts = np.unique(data, return_counts=True)
    
    # Sort by count (descending)
    sort_idx = np.argsort(counts)[::-1]
    
    print("Value counts (sorted):")
    for v, c in zip(values[sort_idx], counts[sort_idx]):
        print(f"  {v}: {c}")

if __name__ == "__main__":
    main()
```

### 3. Set Operations

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([4, 5, 6, 7, 8])
    
    print(f"a = {a}")
    print(f"b = {b}")
    print()
    
    # Union
    print(f"Union: {np.union1d(a, b)}")
    
    # Intersection
    print(f"Intersection: {np.intersect1d(a, b)}")
    
    # Difference (in a but not b)
    print(f"Difference (a-b): {np.setdiff1d(a, b)}")

if __name__ == "__main__":
    main()
```

## Practical Examples

### 1. Clean Data

```python
import numpy as np

def main():
    # Data with missing values
    data = np.array([10, 20, np.nan, 40, np.nan, 60])
    
    print(f"Original: {data}")
    
    # Count NaN
    nan_count = np.sum(np.isnan(data))
    print(f"NaN count: {nan_count}")
    
    # Remove NaN
    clean = data[~np.isnan(data)]
    print(f"Cleaned: {clean}")
    
    # Replace NaN with mean
    filled = data.copy()
    filled[np.isnan(filled)] = np.nanmean(data)
    print(f"Filled: {filled}")

if __name__ == "__main__":
    main()
```

### 2. Format Output

```python
import numpy as np

def main():
    # Simulation results
    np.random.seed(42)
    results = np.random.randn(3, 4) * 100
    
    print("Raw results:")
    print(results)
    print()
    
    print("Rounded to 1 decimal:")
    print(np.round(results, 1))

if __name__ == "__main__":
    main()
```

### 3. Find Outliers

```python
import numpy as np

def main():
    np.random.seed(42)
    data = np.random.randn(100)
    
    # Add outliers
    data[10] = 10
    data[50] = -8
    
    # Find outliers (|z| > 3)
    z_scores = np.abs((data - np.mean(data)) / np.std(data))
    outlier_idx = np.nonzero(z_scores > 3)[0]
    
    print(f"Data shape: {data.shape}")
    print(f"Outlier indices: {outlier_idx}")
    print(f"Outlier values: {data[outlier_idx]}")
    print(f"Outlier z-scores: {np.round(z_scores[outlier_idx], 2)}")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Create `a = np.array([1.234, 2.567, 3.891])`. Round to 1 decimal place with `np.round`, apply `np.floor` and `np.ceil`. Print all three results and explain the difference.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([1.234, 2.567, 3.891])
        print(f"Round: {np.round(a, 1)}")  # [1.2 2.6 3.9]
        print(f"Floor: {np.floor(a)}")      # [1. 2. 3.]
        print(f"Ceil:  {np.ceil(a)}")       # [2. 3. 4.]

---

**Exercise 2.**
Use `np.unique` to find the unique elements and their counts in `a = np.array([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])`. Print both the unique values and their counts.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([1, 2, 2, 3, 3, 3, 4, 4, 4, 4])
        vals, counts = np.unique(a, return_counts=True)
        print(f"Unique: {vals}")
        print(f"Counts: {counts}")

---

**Exercise 3.**
Use `np.diff` to compute the first and second differences of `a = np.array([1, 4, 9, 16, 25])` (perfect squares). Verify that the first differences are odd numbers and the second differences are all 2.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.array([1, 4, 9, 16, 25])
        d1 = np.diff(a)
        d2 = np.diff(a, n=2)
        print(f"First differences: {d1}")   # [3 5 7 9]
        print(f"Second differences: {d2}")  # [2 2 2]
        print(f"All second diffs are 2: {np.all(d2 == 2)}")

---

**Exercise 4.**
Use `np.unique` with `return_inverse=True` to encode categorical labels. Given `labels = np.array(["cat", "dog", "cat", "bird", "dog", "cat"])`, get the unique categories and the integer encoding. Then reconstruct the original labels from the encoding.

??? success "Solution to Exercise 4"

        import numpy as np

        labels = np.array(["cat", "dog", "cat", "bird", "dog", "cat"])
        categories, encoded = np.unique(labels, return_inverse=True)

        print(f"Categories: {categories}")  # ['bird' 'cat' 'dog']
        print(f"Encoded:    {encoded}")     # [1 2 1 0 2 1]

        # Reconstruct
        reconstructed = categories[encoded]
        print(f"Reconstructed: {reconstructed}")
        print(f"Match: {np.array_equal(labels, reconstructed)}")  # True

---

**Exercise 5.**
Use `np.nan`-safe functions to compute summary statistics of an array with missing values. Given `a = np.array([1, np.nan, 3, np.nan, 5, 6, np.nan, 8])`, compute the mean, max, and count of non-NaN values using `np.nanmean`, `np.nanmax`, and `np.count_nonzero(~np.isnan(a))`.

??? success "Solution to Exercise 5"

        import numpy as np

        a = np.array([1, np.nan, 3, np.nan, 5, 6, np.nan, 8])

        print(f"nanmean: {np.nanmean(a):.2f}")     # 4.60
        print(f"nanmax:  {np.nanmax(a):.2f}")       # 8.00
        print(f"nanmin:  {np.nanmin(a):.2f}")       # 1.00

        n_valid = np.count_nonzero(~np.isnan(a))
        print(f"Valid count: {n_valid}")             # 5
        print(f"NaN count:   {np.isnan(a).sum()}")  # 3

        # Compare with non-nan-safe versions
        print(f"np.mean(a): {np.mean(a)}")  # nan — NaN propagates!
