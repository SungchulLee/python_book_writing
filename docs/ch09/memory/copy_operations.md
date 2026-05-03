# Copy Operations

These operations create independent copies with separate memory.

!!! tip "Mental Model"
    A copy is an entirely new array with its own memory -- modifying the copy never affects the original. Use `.copy()` when you need to detach from shared memory, especially after slicing. The cost is double the memory and an O(n) data transfer, so copy only when you truly need independence.

!!! note "Copy = New Buffer (O(n))"
    Every copy operation allocates a **new data buffer** and transfers all elements — an O(n) operation in both time and memory. This is the fundamental cost: views are O(1) because they reuse the existing buffer; copies are O(n) because they duplicate it. Knowing which operations trigger copies lets you avoid unnecessary allocations in performance-sensitive code.


## Method copy

The `.copy()` method creates an explicit copy.

### 1. Slice then Copy

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(f"{x = }")

    y = x[1:4].copy()  # returns copy
    y[0] = -1
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
x = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
```

### 2. Original Unchanged

The copy is independent; mutations don't propagate.


## Function np.copy

The `np.copy()` function creates a copy.

### 1. np.copy Usage

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    print(f"{x = }")

    y = np.copy(x[1:4])  # returns copy
    y[0] = -1
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
x = array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
```

### 2. Equivalent to Method

Both approaches produce identical results.


## Fancy Indexing

Fancy indexing always returns a copy.

### 1. Index Array

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4, 5])
    y = x[[0, 2, 4]]  # fancy indexing returns copy
    y[0] = -1
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([0, 1, 2, 3, 4, 5])
```

### 2. Boolean Indexing

```python
import numpy as np

def main():
    x = np.array([0, 1, 2, 3, 4, 5])
    y = x[x > 2]  # boolean indexing returns copy
    y[0] = -1
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

Output:

```
x = array([0, 1, 2, 3, 4, 5])
```


## Arithmetic Operations

Most arithmetic creates new arrays.

### 1. Addition

```python
import numpy as np

x = np.array([1, 2, 3])
y = x + 1  # creates new array
y[0] = -1
print(f"{x = }")  # x = array([1, 2, 3])
```

### 2. Multiplication

```python
import numpy as np

x = np.array([1, 2, 3])
y = x * 2  # creates new array
```

### 3. In-place Operations

Use `+=`, `*=` to modify in-place without creating copies.


## Copy Summary

Operations that create copies.

### 1. Explicit Copies

- `.copy()` method
- `np.copy()` function

### 2. Implicit Copies

- Fancy indexing: `arr[[0, 2, 4]]`
- Boolean indexing: `arr[arr > 0]`
- Arithmetic: `arr + 1`, `arr * 2`
- Some reshapes (non-contiguous)

### 3. Best Practice

When in doubt, use `.copy()` explicitly for clarity.

---

## Exercises

**Exercise 1.**
Create an array `a = np.arange(10)`. Make a copy using `b = a.copy()`. Modify `b[0] = 999` and verify that `a` is unchanged. Check that `b.base is None` (confirming it owns its data).

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(10)
        b = a.copy()
        b[0] = 999
        print(f"a[0] = {a[0]}")  # 0 (unchanged)
        print(f"b.base is None: {b.base is None}")  # True

---

**Exercise 2.**
Given `a = np.arange(12).reshape(3, 4)`, create three copies using `a.copy()`, `np.array(a, copy=True)`, and `np.copy(a)`. Modify each copy and verify all are independent from `a`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(12).reshape(3, 4)
        c1 = a.copy()
        c2 = np.array(a, copy=True)
        c3 = np.copy(a)

        c1[0, 0] = 100
        c2[0, 0] = 200
        c3[0, 0] = 300

        print(f"a[0, 0] = {a[0, 0]}")  # 0 (unchanged)

---

**Exercise 3.**
Demonstrate that boolean indexing always returns a copy: create `a = np.arange(10)`, extract `b = a[a > 5]`, modify `b`, and show `a` is not affected. Contrast this with slice indexing which returns a view.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.arange(10)
        b = a[a > 5]  # boolean indexing -> copy
        b[0] = 999
        print(f"a after boolean mod: {a}")  # unchanged

        c = a[2:5]  # slice -> view
        c[0] = 888
        print(f"a after slice mod: {a}")  # a[2] changed to 888
