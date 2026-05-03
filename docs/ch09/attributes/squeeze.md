# Squeezing Dimensions

The `np.squeeze` function removes all size-1 dimensions from an array.

!!! tip "Mental Model"
    `squeeze` is the inverse of `expand_dims` -- it strips away every axis that has only one element, collapsing unnecessary packaging around your data. Think of it like removing single-item wrappers: a shape `(1, 3, 1, 5)` becomes `(3, 5)` because those length-1 dimensions carry no information.


## np.squeeze Function

Removes axes of length one from the array shape.

### 1. Basic Usage

```python
import numpy as np

def main():
    x = np.random.normal(size=(1, 3, 1, 2, 1, 5, 1))
    y = np.squeeze(x)
    print(f"{x.shape = }")
    print(f"{y.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (1, 3, 1, 2, 1, 5, 1)
y.shape = (3, 2, 5)
```

### 2. All Size-1 Removed

Every dimension with size 1 is eliminated from the result.


## Selective Squeeze

Remove only specific size-1 axes using the `axis` parameter.

### 1. Single Axis

```python
import numpy as np

def main():
    x = np.zeros((1, 3, 1, 4))
    y = np.squeeze(x, axis=0)
    print(f"{x.shape = }")
    print(f"{y.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (1, 3, 1, 4)
y.shape = (3, 1, 4)
```

### 2. Multiple Axes

```python
import numpy as np

def main():
    x = np.zeros((1, 3, 1, 4))
    y = np.squeeze(x, axis=(0, 2))
    print(f"{x.shape = }")
    print(f"{y.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (1, 3, 1, 4)
y.shape = (3, 4)
```


## Error Handling

Squeezing non-singleton dimensions raises an error.

### 1. ValueError Example

```python
import numpy as np

def main():
    x = np.zeros((1, 3, 1, 4))
    try:
        y = np.squeeze(x, axis=1)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### 2. Safe Practice

Only squeeze axes you know have size 1.


## Common Use Cases

Squeeze is frequently needed after certain operations.

### 1. After Slicing

Slicing with a single index reduces dimensionality; squeeze cleans up.

### 2. Model Outputs

Neural network outputs often have extra batch or channel dimensions.

### 3. Broadcasting Result

Broadcasting may introduce size-1 dimensions that need removal.

!!! danger "Batch Size 1 Trap"

    The most common `squeeze` bug in ML: a model output has shape `(1, 10)` (batch size 1, 10 classes). Calling `np.squeeze` removes the batch dimension, producing shape `(10,)`. Later code that expects a 2D batch array breaks silently.

    ```python
    output = model.predict(single_image)  # shape (1, 10)
    squeezed = np.squeeze(output)          # shape (10,) — batch dim gone!
    ```

    **Fix**: use selective squeeze (`axis=`) to remove only the dimensions you intend, never blindly squeeze all size-1 axes.

---

## Exercises

**Exercise 1.**
Create an array `a = np.zeros((1, 5, 1, 3, 1))`. Use `np.squeeze` to remove all size-1 dimensions and print the resulting shape. Then use selective squeeze to remove only the dimension at axis 0, and print that shape.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.zeros((1, 5, 1, 3, 1))
        b = np.squeeze(a)
        print(b.shape)  # (5, 3)

        c = np.squeeze(a, axis=0)
        print(c.shape)  # (5, 1, 3, 1)

---

**Exercise 2.**
Compute the sum of rows of `a = np.array([[1, 2, 3], [4, 5, 6]])` using `a.sum(axis=1, keepdims=True)`. Print the shape of the result. Then squeeze it and verify the shape becomes `(2,)`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([[1, 2, 3], [4, 5, 6]])
        row_sums = a.sum(axis=1, keepdims=True)
        print(row_sums.shape)  # (2, 1)

        squeezed = row_sums.squeeze()
        print(squeezed.shape)  # (2,)
        print(squeezed)         # [ 6 15]

---

**Exercise 3.**
Create `a = np.array([[42]])` (shape `(1, 1)`). Squeeze it completely and check the resulting `ndim`. Then extract the Python scalar using `.item()` and verify its type is `int`.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.array([[42]])
        b = a.squeeze()
        print(b.ndim)   # 0 (scalar array)
        print(b.shape)  # ()

        val = b.item()
        print(val)           # 42
        print(type(val))     # <class 'int'>
