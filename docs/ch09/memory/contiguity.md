# Memory Contiguity

Memory layout affects whether operations return views or copies.

!!! tip "Mental Model"
    C-contiguous means elements in the last axis are adjacent in memory (row-major), while Fortran-contiguous means elements in the first axis are adjacent (column-major). Operations that traverse memory in order are fast; operations that jump around cause cache misses and slow down. Transpose flips contiguity without moving data.

!!! warning "Why Contiguity Matters for Performance"
    Contiguity determines whether an operation can return a **view** (O(1), no copy) or must create a **copy** (O(n), new allocation). For example, `reshape` on a C-contiguous array is free (just change shape/strides), but on a non-contiguous array it forces a copy. Contiguous memory also enables CPU cache-line prefetching, making element-wise operations significantly faster. When performance matters, check `a.flags['C_CONTIGUOUS']` and call `np.ascontiguousarray(a)` if needed.


## C Contiguous

C-style row-major memory layout.

### 1. Row-Major Order

```
Array: [[0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11]]

Memory: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
```

Elements are stored row by row.

### 2. NumPy Default

NumPy arrays are C-contiguous by default.


## Fortran Contiguous

Fortran-style column-major memory layout.

### 1. Column-Major Order

```
Array: [[0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11]]

Memory: [0, 4, 8, 1, 5, 9, 2, 6, 10, 3, 7, 11]
```

Elements are stored column by column.

### 2. Transpose Effect

Transposing a C-contiguous array makes it Fortran-contiguous.


## View Chain Example

Track memory sharing through operations.

### 1. Initial Array

```python
import numpy as np

def main():
    x = np.arange(12)
    print(f"{id(x) = }")

if __name__ == "__main__":
    main()
```

### 2. Reshape (View)

```python
import numpy as np

def main():
    x = np.arange(12)
    print(f"{id(x) = }")

    y = x.reshape(3, 4)  # view
    print(f"{id(y) = }")

    y[-1, -1] = -11
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

`x` and `y` share the same memory block.

### 3. Transpose (View)

```python
import numpy as np

def main():
    x = np.arange(12)
    print(f"{id(x) = }")

    y = x.reshape(3, 4)  # view
    print(f"{id(y) = }")

    z = y.T  # still a view
    print(f"{id(z) = }")

    z[-1, -1] = -11
    print(f"{x = }")

if __name__ == "__main__":
    main()
```

`z` still shares memory but interprets it column-wise.


## Forced Copy

Non-contiguous arrays force copies when reshaped.

### 1. Copy Scenario

```python
import numpy as np

def main():
    x = np.arange(12)
    print(f"{id(x) = }")

    y = x.reshape(3, 4)  # view
    print(f"{id(y) = }")

    z = y.T  # view (Fortran contiguous)
    print(f"{id(z) = }")

    w = z.reshape((-1,))  # COPY (must reorder data)
    print(f"{id(w) = }")

    w[-1] = -11
    print(f"{x = }")
    print(f"{y = }")
    print(f"{z = }")
    print(f"{w = }")

if __name__ == "__main__":
    main()
```

### 2. Why Copy Needed

`z` is Fortran-contiguous `[0,4,8,1,5,9,2,6,10,3,7,11]` in memory.
Flattening to C-order requires reordering, forcing a copy.

### 3. Memory Independence

`w` has different `id()` and modifications don't affect `x`, `y`, `z`.


## Checking Contiguity

Inspect array memory layout flags.

### 1. Flags Attribute

```python
import numpy as np

x = np.arange(12).reshape(3, 4)
print(x.flags)
```

Output:

```
  C_CONTIGUOUS : True
  F_CONTIGUOUS : False
  ...
```

### 2. After Transpose

```python
import numpy as np

x = np.arange(12).reshape(3, 4)
y = x.T
print(y.flags)
```

Output:

```
  C_CONTIGUOUS : False
  F_CONTIGUOUS : True
  ...
```


## Best Practices

Guidelines for working with memory layout.

### 1. Be Aware

Know when operations return views vs copies.

### 2. Use id()

Track object identity to verify memory sharing.

### 3. Explicit Copy

When data integrity is critical, call `.copy()` explicitly.

### 4. Check flags

Use `.flags` to inspect contiguity when debugging.

---

## Exercises

**Exercise 1.**
Create a C-contiguous array `a = np.arange(12).reshape(3, 4)` and a Fortran-contiguous array `b = np.asfortranarray(a)`. Check `flags['C_CONTIGUOUS']` and `flags['F_CONTIGUOUS']` for both. Print the strides of each and explain the difference.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(12).reshape(3, 4)
        b = np.asfortranarray(a)

        print(f"a C_CONTIGUOUS: {a.flags['C_CONTIGUOUS']}")  # True
        print(f"a F_CONTIGUOUS: {a.flags['F_CONTIGUOUS']}")  # False
        print(f"a strides: {a.strides}")  # (32, 8)

        print(f"b C_CONTIGUOUS: {b.flags['C_CONTIGUOUS']}")  # False
        print(f"b F_CONTIGUOUS: {b.flags['F_CONTIGUOUS']}")  # True
        print(f"b strides: {b.strides}")  # (8, 24)

---

**Exercise 2.**
Starting from `a = np.arange(20).reshape(4, 5)`, create a slice `b = a[:, ::2]`. Check whether `b` is C-contiguous or F-contiguous. Explain why slicing with a step can break contiguity.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(20).reshape(4, 5)
        b = a[:, ::2]
        print(f"b C_CONTIGUOUS: {b.flags['C_CONTIGUOUS']}")  # False
        print(f"b F_CONTIGUOUS: {b.flags['F_CONTIGUOUS']}")  # False
        print(f"b strides: {b.strides}")
        # Step slicing skips elements, so the stride on axis 1
        # is doubled, breaking the contiguous memory pattern.

---

**Exercise 3.**
Use `np.ascontiguousarray` to convert a non-contiguous slice back to a C-contiguous array. Verify the conversion by checking the flags before and after. Measure the memory addresses to confirm a copy was made.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.arange(20).reshape(4, 5)
        b = a[:, ::2]  # non-contiguous
        c = np.ascontiguousarray(b)

        print(f"Before: C_CONTIGUOUS={b.flags['C_CONTIGUOUS']}")
        print(f"After:  C_CONTIGUOUS={c.flags['C_CONTIGUOUS']}")
        print(f"Copy made: {c.base is not b}")
