# Shape and ndim

Every NumPy array has `shape` and `ndim` attributes that describe its structure.

!!! tip "Mental Model"
    `shape` is the blueprint of an array's geometry -- a tuple like `(3, 4)` means 3 rows and 4 columns, while `ndim` simply counts how many axes that tuple has. Knowing the shape is the first step in debugging any NumPy operation, because most errors trace back to mismatched shapes.


## The shape Attribute

The `shape` attribute returns a tuple indicating the size along each dimension.

### 1. 1D Array Shape

```python
import numpy as np

def main():
    x = np.array([7, 2, 9, 10])
    print(f"{x.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (4,)
```

### 2. 2D Array Shape

```python
import numpy as np

def main():
    y = np.array([[5.2, 3.0, 4.5], [9.1, 0.1, 0.3]])
    print(f"{y.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
y.shape = (2, 3)
```

### 3. 3D Array Shape

```python
import numpy as np

def main():
    z = np.zeros((4, 3, 2))
    print(f"{z.shape = }, {z.dtype = }")

if __name__ == "__main__":
    main()
```

Output:

```
z.shape = (4, 3, 2), z.dtype = dtype('float64')
```


## The ndim Attribute

The `ndim` attribute returns the number of dimensions (axes) of the array.

### 1. 1D Array ndim

```python
import numpy as np

def main():
    x = np.array([7, 2, 9, 10])
    print(f"{x.ndim = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.ndim = 1
```

### 2. 2D Array ndim

```python
import numpy as np

def main():
    y = np.array([[5.2, 3.0, 4.5], [9.1, 0.1, 0.3]])
    print(f"{y.ndim = }")

if __name__ == "__main__":
    main()
```

Output:

```
y.ndim = 2
```

### 3. 3D Array ndim

```python
import numpy as np

def main():
    z = np.zeros((4, 3, 2))
    print(f"{z.ndim = }")

if __name__ == "__main__":
    main()
```

Output:

```
z.ndim = 3
```


## Relationship

The `ndim` equals the length of the `shape` tuple.

### 1. Mathematical Link

```python
import numpy as np

x = np.zeros((4, 3, 2))
assert x.ndim == len(x.shape)
```

### 2. Practical Use

Use `ndim` to check dimensionality before operations that require specific dimensions.

## Shape Debugging Checklist

When an operation fails with a shape mismatch:

1. **Print shapes**: `print(a.shape, b.shape)` — the single most useful debugging step.
2. **Check ndim**: is one array 1D when it should be 2D? Use `np.expand_dims` or `reshape`.
3. **Check broadcasting**: shapes must be equal or one must be 1 in each trailing dimension.
4. **Check after slicing**: indexing with a scalar reduces ndim by 1 (e.g., `a[0]` turns `(3, 4)` into `(4,)`). Use `a[0:1]` to keep the dimension.

```python
import numpy as np

a = np.zeros((3, 4))
print(a[0].shape)    # (4,) — scalar index drops dimension
print(a[0:1].shape)  # (1, 4) — slice preserves dimension
```

---

## Exercises

**Exercise 1.**
Create arrays with 0, 1, 2, and 3 dimensions: a scalar `np.array(42)`, a 1D array `np.array([1, 2, 3])`, a 2D array `np.zeros((2, 3))`, and a 3D array `np.ones((2, 3, 4))`. Print the `ndim` and `shape` of each. Verify that `ndim` equals `len(shape)` for every array.

??? success "Solution to Exercise 1"

        import numpy as np

        arrays = [
            np.array(42),
            np.array([1, 2, 3]),
            np.zeros((2, 3)),
            np.ones((2, 3, 4)),
        ]

        for arr in arrays:
            print(f"ndim={arr.ndim}, shape={arr.shape}, len(shape)={len(arr.shape)}")
            assert arr.ndim == len(arr.shape)

---

**Exercise 2.**
Given `a = np.arange(60).reshape(3, 4, 5)`, print its shape and use the shape tuple to compute the total number of elements. Verify your answer against `a.size`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(60).reshape(3, 4, 5)
        print(a.shape)  # (3, 4, 5)

        total = 1
        for dim in a.shape:
            total *= dim
        print(f"Computed total: {total}")  # 60
        print(f"a.size: {a.size}")          # 60
        print(total == a.size)              # True

---

**Exercise 3.**
Create a 1D array `a = np.array([10, 20, 30])` and check its `ndim`. Then use `a.reshape(1, -1)` and `a.reshape(-1, 1)` to produce 2D arrays. Print the `ndim` and `shape` of each reshaped array.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.array([10, 20, 30])
        print(f"Original: ndim={a.ndim}, shape={a.shape}")  # ndim=1, shape=(3,)

        row = a.reshape(1, -1)
        print(f"Row vector: ndim={row.ndim}, shape={row.shape}")  # ndim=2, shape=(1, 3)

        col = a.reshape(-1, 1)
        print(f"Col vector: ndim={col.ndim}, shape={col.shape}")  # ndim=2, shape=(3, 1)
