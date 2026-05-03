# Expanding Dimensions

Adding new axes to arrays is essential for broadcasting and batch operations.

!!! tip "Mental Model"
    `expand_dims` inserts a size-1 axis at the position you specify, like sliding an empty shelf into a bookcase. The data doesn't change -- only the shape gains a new dimension. This is the standard way to promote an array so that broadcasting aligns axes correctly.


## np.expand_dims

The `np.expand_dims` function inserts a new axis at the specified position.

### 1. Axis Parameter

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    print(f"{x.shape = }", end="\n\n")

    y0 = np.expand_dims(x, axis=0)
    y1 = np.expand_dims(x, axis=1)
    y2 = np.expand_dims(x, axis=2)
    y3 = np.expand_dims(x, axis=3)
    print(f"{y0.shape = }")
    print(f"{y1.shape = }")
    print(f"{y2.shape = }")
    print(f"{y3.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (2, 3, 4)

y0.shape = (1, 2, 3, 4)
y1.shape = (2, 1, 3, 4)
y2.shape = (2, 3, 1, 4)
y3.shape = (2, 3, 4, 1)
```

### 2. Axis Meaning

The axis specifies where the new size-1 dimension is inserted.


## Using np.newaxis

The `np.newaxis` constant adds dimensions via indexing syntax.

### 1. Explicit Slicing

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    print(f"{x.shape = }", end="\n\n")

    y1 = x[np.newaxis, :]
    y2 = x[:, np.newaxis]
    y3 = x[:, :, np.newaxis]
    y4 = x[:, :, :, np.newaxis]
    print(f"{y1.shape = }")
    print(f"{y2.shape = }")
    print(f"{y3.shape = }")
    print(f"{y4.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (2, 3, 4)

y1.shape = (1, 2, 3, 4)
y2.shape = (2, 1, 3, 4)
y3.shape = (2, 3, 1, 4)
y4.shape = (2, 3, 4, 1)
```

### 2. With Ellipsis

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    print(f"{x.shape = }", end="\n\n")

    z1 = x[np.newaxis, ...]
    z2 = x[..., np.newaxis]
    print(f"{z1.shape = }")
    print(f"{z2.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (2, 3, 4)

z1.shape = (1, 2, 3, 4)
z2.shape = (2, 3, 4, 1)
```


## Using None

`None` is an alias for `np.newaxis` in indexing.

### 1. Explicit Slicing

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    print(f"{x.shape = }", end="\n\n")

    y1 = x[None, :]
    y2 = x[:, None]
    y3 = x[:, :, None]
    y4 = x[:, :, :, None]
    print(f"{y1.shape = }")
    print(f"{y2.shape = }")
    print(f"{y3.shape = }")
    print(f"{y4.shape = }")

if __name__ == "__main__":
    main()
```

### 2. With Ellipsis

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    print(f"{x.shape = }", end="\n\n")

    z1 = x[None, ...]
    z2 = x[..., None]
    print(f"{z1.shape = }")
    print(f"{z2.shape = }")

if __name__ == "__main__":
    main()
```


## Method Comparison

Three equivalent ways to add dimensions.

### 1. np.expand_dims

Most explicit and readable for complex insertions.

### 2. np.newaxis

Standard NumPy idiom, clear intent.

### 3. None Shorthand

Shortest syntax, common in concise code.

## When Broadcasting Fails Without expand_dims

A common error: trying to operate on arrays whose shapes don't align.

```python
import numpy as np

a = np.array([1, 2, 3])          # shape (3,)
b = np.array([[10], [20], [30]])  # shape (3, 1)

# This works — broadcasting aligns (3,) to (1, 3) automatically
print((a + b).shape)  # (3, 3)

# But this fails:
row_means = np.mean(b, axis=1)   # shape (3,)
# b - row_means                  # shape (3, 1) - (3,) → works by accident
# For clarity, expand_dims makes intent explicit:
b - np.expand_dims(row_means, axis=1)  # shape (3, 1) - (3, 1) → clear
```

When shapes are ambiguous, `expand_dims` makes the broadcasting intent explicit and prevents subtle bugs.

---

## Exercises

**Exercise 1.**
Given `a = np.array([10, 20, 30])` (shape `(3,)`), use `np.expand_dims` to create a row vector of shape `(1, 3)` and a column vector of shape `(3, 1)`. Verify the shapes by printing them.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([10, 20, 30])

        row = np.expand_dims(a, axis=0)
        col = np.expand_dims(a, axis=1)

        print(row.shape)  # (1, 3)
        print(col.shape)  # (3, 1)

---

**Exercise 2.**
Create a 2D array `a = np.arange(12).reshape(3, 4)`. Use `np.expand_dims` to add a new axis at position 0, producing shape `(1, 3, 4)`. Then add another axis at position 2 to the original array, producing shape `(3, 1, 4)`. Print both shapes.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(12).reshape(3, 4)

        b = np.expand_dims(a, axis=0)
        print(b.shape)  # (1, 3, 4)

        c = np.expand_dims(a, axis=1)  # axis=1 inserts between dim 0 and dim 1
        # For the original (3, 4), inserting at position 2 means after dim 1
        d = np.expand_dims(a, axis=2)
        print(d.shape)  # (3, 4, 1)
        # Inserting at axis=1 gives (3, 1, 4)
        print(c.shape)  # (3, 1, 4)

---

**Exercise 3.**
Given `a = np.array([1, 2, 3])` and `b = np.array([10, 20])`, use `np.expand_dims` (or `np.newaxis`) on both arrays so that you can broadcast them into an outer-sum of shape `(3, 2)`. Print the resulting array.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.array([1, 2, 3])      # shape (3,)
        b = np.array([10, 20])        # shape (2,)

        # Make a into (3, 1) and b into (1, 2) for broadcasting
        a_col = np.expand_dims(a, axis=1)  # (3, 1)
        b_row = np.expand_dims(b, axis=0)  # (1, 2)

        result = a_col + b_row
        print(result)
        # [[11 21]
        #  [12 22]
        #  [13 23]]
        print(result.shape)  # (3, 2)
