# Fancy Indexing

Fancy indexing selects elements using arrays of indices instead of scalars or slices.

!!! tip "Mental Model"
    Fancy indexing lets you cherry-pick elements by passing an array of positions, like handing a librarian a list of shelf numbers. Unlike slicing, the positions need not be contiguous or in order, and the result is always a copy. The output shape matches the shape of your index array, not the original data.


## 1D Fancy Indexing

Select multiple elements by passing a list or array of indices.

### 1. List of Indices

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = np.array(a)
    print(f"{b[[0, 1, 3]] = }")

if __name__ == "__main__":
    main()
```

Output:

```
b[[0, 1, 3]] = array([0, 1, 3])
```

### 2. Array of Indices

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = np.array(a)
    print(f"{b[np.array([0, 1, 3])] = }")

if __name__ == "__main__":
    main()
```

Output:

```
b[np.array([0, 1, 3])] = array([0, 1, 3])
```


## 2D Fancy Indexing

Select multiple rows from a 2D array.

### 1. Row Selection

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)
    print(f"{b[[0, 1, 3]] = }")

if __name__ == "__main__":
    main()
```

Output:

```
b[[0, 1, 3]] = array([[0, 1, 2],
                      [1, 2, 3],
                      [3, 4, 5]])
```

### 2. With np.array

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)
    print(f"{b[np.array([0, 1, 3])] = }")

if __name__ == "__main__":
    main()
```

Output:

```
b[np.array([0, 1, 3])] = array([[0, 1, 2],
                                [1, 2, 3],
                                [3, 4, 5]])
```


## Multi-Axis Fancy

Index both rows and columns simultaneously.

### 1. Paired Indices

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)
    print(f"{b[[0, 1, 3], [0, 0, -1]] = }")

if __name__ == "__main__":
    main()
```

Output:

```
b[[0, 1, 3], [0, 0, -1]] = array([0, 1, 6])
```

### 2. How It Works

Pairs `(row[i], col[i])` are selected: `(0,0)`, `(1,0)`, `(3,-1)`.

### 3. With np.array

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)
    print(f"{b[np.array([0, 1, 3]), np.array([0, 0, -1])] = }")

if __name__ == "__main__":
    main()
```

Output:

```
b[np.array([0, 1, 3]), np.array([0, 0, -1])] = array([0, 1, 6])
```


## Boolean Masking

Select elements where a condition is True.

### 1. Create Mask

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])
mask = arr > 20
print(f"{mask = }")
print(f"{arr[mask] = }")
```

Output:

```
mask = array([False, False,  True,  True,  True])
arr[mask] = array([30, 40, 50])
```

### 2. Inline Condition

```python
import numpy as np

arr = np.array([10, 20, 30, 40, 50])
print(f"{arr[arr > 20] = }")
```

Output:

```
arr[arr > 20] = array([30, 40, 50])
```


## Use Cases

Fancy indexing enables expressive data selection.

### 1. Data Filtering

Select rows matching specific criteria from datasets.

### 2. Reordering

Rearrange array elements in arbitrary order.

### 3. Sampling

Select random subsets using random index arrays.

## Fancy Indexing vs Boolean Masking

Both return copies, but they serve different purposes:

```text
Fancy indexing → "give me elements at these exact positions"
Boolean masking → "give me elements that satisfy this condition"
```

| | Fancy indexing | Boolean masking |
|---|---|---|
| Input | Array of indices | Array of True/False |
| Result shape | Shape of index array | Number of True values |
| Use case | Reorder, sample, permute | Filter by condition |
| Returns | Copy | Copy |

---

## Exercises

**Exercise 1.**
Given `a = np.array([10, 20, 30, 40, 50])`, use fancy indexing to select elements at indices `[0, 3, 4]`. Then use fancy indexing to create a reversed copy: select elements at indices `[4, 3, 2, 1, 0]`.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([10, 20, 30, 40, 50])
        selected = a[[0, 3, 4]]
        print(f"Selected: {selected}")  # [10 40 50]

        reversed_a = a[[4, 3, 2, 1, 0]]
        print(f"Reversed: {reversed_a}")  # [50 40 30 20 10]

---

**Exercise 2.**
Create a 5x4 matrix `M = np.arange(20).reshape(5, 4)`. Use multi-axis fancy indexing to extract the elements at positions `(0, 0)`, `(2, 1)`, and `(4, 3)` in a single operation. The result should be a 1D array of 3 elements.

??? success "Solution to Exercise 2"

        import numpy as np

        M = np.arange(20).reshape(5, 4)
        rows = np.array([0, 2, 4])
        cols = np.array([0, 1, 3])
        result = M[rows, cols]
        print(f"Extracted: {result}")  # [ 0  9 19]

---

**Exercise 3.**
Given `a = np.random.randn(100)`, use `np.random.choice` to generate 10 random indices (without replacement) and use fancy indexing to sample 10 elements from `a`. Print the sampled values and verify the result shape is `(10,)`.

??? success "Solution to Exercise 3"

        import numpy as np

        np.random.seed(42)
        a = np.random.randn(100)
        indices = np.random.choice(100, size=10, replace=False)
        sampled = a[indices]
        print(f"Indices: {indices}")
        print(f"Sampled: {sampled}")
        print(f"Shape: {sampled.shape}")  # (10,)
