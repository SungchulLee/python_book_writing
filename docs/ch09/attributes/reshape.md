# Reshaping Arrays

Reshaping changes an array's dimensions while preserving its data.

!!! tip "Mental Model"
    Reshape reinterprets a flat sequence of numbers by placing new row and column boundaries. The total number of elements stays constant -- you are folding the same ribbon of data into a different grid. When possible, NumPy returns a view (no copy), so the reshaped array shares memory with the original.


## Method reshape

The `reshape` method returns a new view with the specified shape.

### 1. Basic Usage

```python
import numpy as np

def main():
    x = np.arange(6)
    print(f"{x.shape = }")
    print(x, end="\n\n")

    y = x.reshape((3, 2))
    print(f"{y.shape = }")
    print(y)

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (6,)
[0 1 2 3 4 5]

y.shape = (3, 2)
[[0 1]
 [2 3]
 [4 5]]
```

### 2. Total Size Rule

The product of new dimensions must equal the original total size.


## Function np.reshape

The `np.reshape` function provides the same functionality.

### 1. Function Syntax

```python
import numpy as np

def main():
    x = np.arange(6)
    print(f"{x.shape = }")
    print(x, end="\n\n")

    y = np.reshape(x, (3, 2))
    print(f"{y.shape = }")
    print(y)

if __name__ == "__main__":
    main()
```

### 2. Method vs Function

Both are equivalent; the method syntax is more common.


## The -1 Wildcard

Using `-1` lets NumPy infer one dimension automatically.

### 1. Flatten to 1D

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    y = x.reshape((-1,))
    print(f"{x.shape = }")
    print(f"{y.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (2, 3, 4)
y.shape = (24,)
```

### 2. Keep First Axis

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    z = x.reshape((2, -1))
    print(f"{x.shape = }")
    print(f"{z.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (2, 3, 4)
z.shape = (2, 12)
```

### 3. Keep Last Axis

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    w = x.reshape((-1, 4))
    print(f"{x.shape = }")
    print(f"{w.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
x.shape = (2, 3, 4)
w.shape = (6, 4)
```


## Multiple Examples

Combining all `-1` examples in one block.

### 1. All Together

```python
import numpy as np

def main():
    x = np.zeros((2, 3, 4))
    y = x.reshape((-1,))
    z = x.reshape((2, -1))
    w = x.reshape((-1, 4))
    print(f"{x.shape = }")
    print(f"{y.shape = }")
    print(f"{z.shape = }")
    print(f"{w.shape = }")

if __name__ == "__main__":
    main()
```

### 2. Only One -1

You can only use `-1` for a single dimension per reshape call.

---

## Runnable Example: `shape_manipulation_tutorial.py`

```python
"""
02_shape_manipulation.py - Reshaping and Transforming

🔗 Topic #24: Most operations return VIEWS (no memory copy)!
"""

import numpy as np

if __name__ == "__main__":

    print("="*80)
    print("SHAPE MANIPULATION")
    print("="*80)
    print("\n🔗 Remember: Most operations return VIEWS (Topic #24)!")

    # ============================================================================
    # Reshape
    # ============================================================================

    print("\n" + "="*80)
    print("Reshape - Change Dimensions")
    print("="*80)

    arr = np.arange(12)
    print(f"Original: {arr}")
    print(f"Shape: {arr.shape}")

    matrix = arr.reshape(3, 4)
    print(f"\nReshaped to (3, 4):\n{matrix}")

    # CRITICAL: Reshape returns a VIEW!
    print(f"\nIs it a view? {matrix.base is arr}")
    matrix[0, 0] = 999
    print(f"After matrix[0,0]=999: original arr[0]={arr[0]}")
    print("They share memory! (Topic #24)")

    # ============================================================================
    # Transpose
    # ============================================================================

    print("\n" + "="*80)
    print("Transpose - Flip Dimensions")
    print("="*80)

    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"Original (2,3):\n{matrix}")
    transposed = matrix.T
    print(f"\nTransposed (3,2):\n{transposed}")
    print(f"Is view? {transposed.base is matrix}")

    # ============================================================================
    # Ravel and Flatten
    # ============================================================================

    print("\n" + "="*80)
    print("Ravel vs Flatten")
    print("="*80)

    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"Matrix:\n{matrix}")

    ravel = matrix.ravel()  # Returns view if possible
    flatten = matrix.flatten()  # Always returns copy

    print(f"\nravel(): {ravel}")
    print(f"Is view? {ravel.base is matrix}")

    print(f"\nflatten(): {flatten}")
    print(f"Is view? {flatten.base is matrix}")

    print("""
    \nravel(): Fast (view if possible)
    flatten(): Slower (always copies)
    """)

    print("""
    \n🎯 KEY TAKEAWAYS:
    1. reshape() returns views (fast!)
    2. .T (transpose) returns views
    3. ravel() tries to return view
    4. flatten() always copies
    5. Check .base to verify view vs copy

    🔜 NEXT: 03_mathematical_ops.py
    """)
```


## Contiguity and Reshape Pitfalls

!!! warning "Non-Contiguous Arrays"

    After slicing, an array may become **non-contiguous** in memory. Reshaping a non-contiguous array forces a **copy** instead of returning a view:

    ```python
    import numpy as np

    a = np.arange(12).reshape(3, 4)
    sliced = a[:, ::2]  # every other column — non-contiguous
    print(sliced.flags['C_CONTIGUOUS'])  # False

    reshaped = sliced.reshape(-1)  # works, but creates a COPY
    reshaped[0] = 999
    print(sliced[0, 0])  # unchanged — it's a copy, not a view
    ```

    Check `arr.flags['C_CONTIGUOUS']` before relying on reshape returning a view. If contiguity matters, call `np.ascontiguousarray(arr)` first.

---

## Exercises

**Exercise 1.**
Create a 1D array of 24 elements using `np.arange(24)`. Reshape it into a 3D array of shape `(2, 3, 4)`. Then reshape the 3D array back to a 1D array using `-1` as the dimension argument. Verify that the values are unchanged.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(24)
        b = a.reshape(2, 3, 4)
        print(b.shape)  # (2, 3, 4)

        c = b.reshape(-1)
        print(c.shape)  # (24,)
        print(np.array_equal(a, c))  # True

---

**Exercise 2.**
Given `a = np.arange(12)`, reshape it into shape `(3, -1)` and print the result. Then reshape the original array into shape `(-1, 2)` and print the result. Explain what `-1` does in each case.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(12)

        b = a.reshape(3, -1)
        print(b.shape)  # (3, 4) — NumPy infers 12/3 = 4
        print(b)

        c = a.reshape(-1, 2)
        print(c.shape)  # (6, 2) — NumPy infers 12/2 = 6
        print(c)
        # -1 tells NumPy to compute that dimension automatically
        # so that the total number of elements is preserved.

---

**Exercise 3.**
Create a 2D array `a = np.arange(6).reshape(2, 3)`. Attempt to reshape it into shape `(4, 2)` and catch the `ValueError`. Print the error message and explain why the reshape fails.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.arange(6).reshape(2, 3)
        try:
            b = a.reshape(4, 2)
        except ValueError as e:
            print(f"Error: {e}")
        # Error: cannot reshape array of size 6 into shape (4,2)
        # 4 * 2 = 8 != 6, so the reshape is impossible.
