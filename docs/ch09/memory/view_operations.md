# View Operations

These operations return views that share memory with the original array.

!!! tip "Mental Model"
    View operations -- slicing, reshape, transpose -- give you a new array object that points to the same underlying data. They are O(1) in time and use zero extra memory, but any mutation through the view changes the original. Recognizing which operations return views is essential for writing both fast and correct NumPy code.

!!! note "View Operations at a Glance"
    All view operations share one property: they return a new array object with different shape or strides but pointing to the **same data buffer**. No data is copied.

    | Operation | What changes | Data copied? |
    |---|---|---|
    | Slicing (`a[1:5]`) | Shape, offset | No |
    | Reshape (`a.reshape(...)`) | Shape, strides | No (if contiguous) |
    | Transpose (`a.T`) | Strides, axis order | No |
    | Ravel (`a.ravel()`) | Shape | No (if contiguous) |


## Slicing

Array slices return views by default.

### 1. Basic Slice

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(f"{x = }")

    y = x[1:4]  # returns view
    y[0] = -1
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
x = array([ 0, -1,  2,  3,  4,  5,  6,  7,  8,  9])
```

### 2. Mutation Propagates

Modifying the slice modifies the original array.


## Method reshape

The `reshape` method returns a view when possible.

### 1. reshape View

```python
import numpy as np

def main():
    x = np.arange(6)
    print(f"{x = }")

    y = x.reshape((3, 2))  # returns view
    y[0, 0] = 6
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([0, 1, 2, 3, 4, 5])
x = array([6, 1, 2, 3, 4, 5])
```

### 2. Same Memory

The reshaped array shares the underlying data buffer.


## Function np.reshape

The `np.reshape` function also returns a view.

### 1. np.reshape View

```python
import numpy as np

def main():
    x = np.arange(6)
    print(f"{x = }")

    y = np.reshape(x, (3, 2))  # returns view
    y[0, 0] = 6
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([0, 1, 2, 3, 4, 5])
x = array([6, 1, 2, 3, 4, 5])
```

### 2. Equivalent Behavior

Method and function behave identically.


## Attribute T

The transpose attribute `.T` returns a view.

### 1. Transpose View

```python
import numpy as np

def main():
    x = np.array([[1, 2], [3, 4]])
    print(f"{x = }")

    y = x.T  # returns view
    y[0, 0] = 6
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([[1, 2],
           [3, 4]])
x = array([[6, 2],
           [3, 4]])
```

### 2. Shared Data

Transposed array shares memory with original.


## Function np.transpose

The `np.transpose` function returns a view.

### 1. np.transpose View

```python
import numpy as np

def main():
    x = np.array([[1, 2], [3, 4]])
    print(f"{x = }")

    y = np.transpose(x)  # returns view
    y[0, 0] = 6
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([[1, 2],
           [3, 4]])
x = array([[6, 2],
           [3, 4]])
```

### 2. Same as .T

Function and attribute produce equivalent views.


## View Summary

Common operations returning views.

### 1. List of Operations

- Slicing: `arr[1:4]`
- Reshape: `arr.reshape(shape)`
- Transpose: `arr.T`
- Ravel: `arr.ravel()`
- Squeeze: `np.squeeze(arr)`
- Expand dims: `arr[np.newaxis]`

### 2. General Rule

Operations that reinterpret existing data return views.

---

## Exercises

**Exercise 1.**
List three NumPy operations that return views and three that return copies. Create an array and test each, verifying with `np.shares_memory`.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(12).reshape(3, 4)

        # Views: reshape, slice, transpose
        print(f"Reshape is view: {np.shares_memory(a, a.reshape(4, 3))}")
        print(f"Slice is view: {np.shares_memory(a, a[1:3])}")
        print(f"Transpose is view: {np.shares_memory(a, a.T)}")

        # Copies: copy, fancy indexing, boolean indexing
        print(f"Copy shares: {np.shares_memory(a, a.copy())}")
        print(f"Fancy shares: {np.shares_memory(a, a[[0, 2]])}")
        print(f"Bool shares: {np.shares_memory(a, a[a > 5])}")

---

**Exercise 2.**
Create `a = np.arange(12)`. Reshape it to `(3, 4)` and verify the reshape is a view. Then transpose it and check if the transpose is a view. Finally, flatten the transpose and check if the result is a view or copy.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(12)
        b = a.reshape(3, 4)
        print(f"Reshape is view: {np.shares_memory(a, b)}")  # True

        c = b.T
        print(f"Transpose is view: {np.shares_memory(a, c)}")  # True

        d = c.flatten()
        print(f"Flatten is view: {np.shares_memory(a, d)}")  # False

---

**Exercise 3.**
Create a 2D array and extract a column using `a[:, 0]`. Determine whether this is a view or a copy. Then modify the extracted column and observe whether the original changes. Repeat with a row `a[0, :]` and compare the behavior.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.arange(12).reshape(3, 4)
        col = a[:, 0]
        print(f"Column is view: {np.shares_memory(a, col)}")  # True
        col[0] = 99
        print(f"a[0, 0] after col mod: {a[0, 0]}")  # 99

        row = a[0, :]
        print(f"Row is view: {np.shares_memory(a, row)}")  # True
