# ravel vs flatten

Both methods flatten arrays to 1D, but differ in memory behavior.

!!! tip "Mental Model"
    `ravel` returns a view when the array is already contiguous (free), but falls back to a copy when it must rearrange data. `flatten` always returns a copy, guaranteeing independence. Choose `ravel` for speed when you just need a flat view, and `flatten` when you need a safe, modifiable 1D copy.

!!! tip "Decision Rule"

    | Need | Use | Why |
    |---|---|---|
    | Speed, read-only flat view | `ravel()` | Returns a view when contiguous — O(1) |
    | Safe, independent 1D copy | `flatten()` | Always copies — O(n) but mutation-safe |
    | Flat view, guaranteed no copy | `a.reshape(-1)` | Raises error if copy needed (unlike ravel, which silently copies) |

    If you are unsure whether `ravel` returned a view or a copy, check `result.base is a`.


## Method ravel

The `ravel()` method returns a view when possible.

### 1. Basic Usage

```python
import numpy as np

def main():
    x = np.arange(6).reshape((3, 2))
    print(f"{x.shape = }")

    y = x.ravel()  # returns view
    print(f"{y.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (3, 2)
y.shape = (6,)
```

### 2. Memory Sharing

```python
import numpy as np

def main():
    x = np.arange(6).reshape((3, 2))
    y = x.ravel()
    y[0] = -1
    print(f"{x[0, 0] = }")  # -1

if __name__ == "__main__":
    main()
```

### 3. View Behavior

Modifying the raveled array modifies the original.


## Method flatten

The `flatten()` method always returns a copy.

### 1. Basic Usage

```python
import numpy as np

def main():
    x = np.arange(6).reshape((3, 2))
    print(f"{x.shape = }")

    y = x.flatten()  # returns copy
    print(f"{y.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (3, 2)
y.shape = (6,)
```

### 2. Memory Independence

```python
import numpy as np

def main():
    x = np.arange(6).reshape((3, 2))
    y = x.flatten()
    y[0] = -1
    print(f"{x[0, 0] = }")  # 0

if __name__ == "__main__":
    main()
```

### 3. Copy Behavior

Modifying the flattened array does not affect the original.


## Side-by-Side Compare

Direct comparison of the two methods.

### 1. Comparison Code

```python
import numpy as np

def main():
    x = np.arange(6).reshape((3, 2))
    
    # ravel returns view
    r = x.ravel()
    r[0] = 99
    print(f"After ravel modification: x[0,0] = {x[0, 0]}")
    
    # Reset
    x = np.arange(6).reshape((3, 2))
    
    # flatten returns copy
    f = x.flatten()
    f[0] = 99
    print(f"After flatten modification: x[0,0] = {x[0, 0]}")

if __name__ == "__main__":
    main()
```

Output:

```
After ravel modification: x[0,0] = 99
After flatten modification: x[0,0] = 0
```

### 2. Key Difference

`ravel` shares memory; `flatten` does not.


## When to Use Each

Choose based on your memory requirements.

### 1. Use ravel When

- Memory efficiency matters
- You want changes to reflect in original
- Working with large arrays

### 2. Use flatten When

- You need data isolation
- Original must remain unchanged
- Returning from functions

### 3. Performance Note

`ravel` is faster because it avoids memory allocation.


## Order Parameter

Both methods support different flattening orders.

### 1. C Order (Default)

```python
import numpy as np

x = np.array([[1, 2], [3, 4]])
print(x.ravel(order='C'))  # [1 2 3 4]
```

Row-major order (C-style).

### 2. Fortran Order

```python
import numpy as np

x = np.array([[1, 2], [3, 4]])
print(x.ravel(order='F'))  # [1 3 2 4]
```

Column-major order (Fortran-style).

---

## Exercises

**Exercise 1.**
Create `a = np.arange(12).reshape(3, 4)`. Flatten it using both `a.ravel()` and `a.flatten()`. Modify the first element of each result and check which modification affects the original array `a`.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(12).reshape(3, 4)
        r = a.ravel()
        f = a.flatten()

        r[0] = 99
        print(f"After ravel mod: a[0,0] = {a[0, 0]}")  # 99 (view)

        a2 = np.arange(12).reshape(3, 4)
        f = a2.flatten()
        f[0] = 88
        print(f"After flatten mod: a2[0,0] = {a2[0, 0]}")  # 0 (copy)

---

**Exercise 2.**
Test `np.ravel` with both `order='C'` (row-major) and `order='F'` (column-major) on a 2x3 matrix. Print both results and explain why the element order differs.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([[1, 2, 3], [4, 5, 6]])
        print(f"C order: {np.ravel(a, order='C')}")  # [1 2 3 4 5 6]
        print(f"F order: {np.ravel(a, order='F')}")  # [1 4 2 5 3 6]
        # C order reads row by row, F order reads column by column.

---

**Exercise 3.**
Create a non-contiguous array `b = np.arange(20).reshape(4, 5)[:, ::2]`. Show that `b.ravel()` returns a copy (not a view) by checking `b.ravel().base`. Explain why `ravel` cannot return a view for non-contiguous arrays.

??? success "Solution to Exercise 3"

        import numpy as np

        b = np.arange(20).reshape(4, 5)[:, ::2]
        r = b.ravel()
        print(f"Is view: {r.base is b}")  # False (copy)
        # ravel cannot return a view for non-contiguous arrays
        # because the elements are not in a single contiguous
        # memory block.
