# ndarray Object Model

!!! tip "Mental Model"
    An `ndarray` is a thin Python wrapper around a contiguous C buffer plus metadata (dtype, shape, strides). The data lives in a flat byte array; the metadata tells NumPy how to interpret those bytes as a multi-dimensional grid. This separation is why reshaping and transposing are nearly free -- only the metadata changes, not the data.

!!! note "The NumPy Core Model"
    ```text
    An array is:
      - a contiguous block of memory  (data buffer)
      - interpreted by               dtype
      - structured by                shape
      - accessed via                 strides

    Computation happens through:
      - ufuncs        (elementwise C loops)
      - broadcasting  (shape alignment)
    ```
    Every other NumPy feature — views, reshaping, fancy indexing, linear algebra —
    builds on these six concepts. This model explains three things:

    - **Performance**: contiguous memory + compiled C loops = near-C speed
    - **Flexibility**: changing dtype or shape reinterprets existing bytes without copying
    - **Behavior**: views share the data buffer, so mutations propagate; copies don't

## Core Architecture

### 1. C-Contiguous Memory

The `ndarray` is NumPy's fundamental data structure, built around a contiguous block of memory with metadata:

```python
import numpy as np

arr = np.arange(12).reshape(3, 4)
print(type(arr))  # <class 'numpy.ndarray'>
print(arr.flags)  # Shows C_CONTIGUOUS, OWNDATA, etc.
```

**Key properties:**
- **Data buffer**: Raw memory block holding elements
- **Metadata**: Shape, strides, dtype, flags
- **C-contiguous layout**: Row-major ordering (default)

### 2. Memory Layout

NumPy stores arrays in **row-major (C)** or **column-major (Fortran)** order:

```python
# C-contiguous (row-major)
arr_c = np.array([[1, 2, 3], [4, 5, 6]], order='C')
print(arr_c.flags['C_CONTIGUOUS'])  # True

# Fortran-contiguous (column-major)
arr_f = np.array([[1, 2, 3], [4, 5, 6]], order='F')
print(arr_f.flags['F_CONTIGUOUS'])  # True
```

**Why it matters:**
- Cache locality affects performance
- Interoperability with C/Fortran libraries
- Stride calculations for slicing

### 3. Object Attributes

The `ndarray` exposes rich metadata:

```python
arr = np.arange(24).reshape(2, 3, 4)

print(arr.shape)    # (2, 3, 4) - dimensions
print(arr.ndim)     # 3 - number of axes
print(arr.size)     # 24 - total elements
print(arr.dtype)    # dtype('int64') - element type
print(arr.itemsize) # 8 - bytes per element
print(arr.nbytes)   # 192 - total bytes
print(arr.strides)  # (96, 32, 8) - byte jumps per axis
```

## Buffer Protocol

### 1. Memory Views

NumPy implements Python's buffer protocol for zero-copy data sharing:

```python
arr = np.array([1, 2, 3, 4, 5])
mv = memoryview(arr)

print(mv.format)    # 'l' - long integer
print(mv.itemsize)  # 8
print(mv.ndim)      # 1
print(mv.shape)     # (5,)
```

### 2. Interoperability

Direct memory access enables interaction with compiled code:

```python
import ctypes

arr = np.array([1, 2, 3], dtype=np.int32)
ptr = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

# Can pass to C functions
print(ptr[0])  # 1
```

### 3. Zero-Copy Sharing

Multiple objects can reference the same data:

```python
arr1 = np.arange(10)
arr2 = arr1  # Reference, not copy
arr2[0] = 999
print(arr1[0])  # 999 - shared memory
```

## Construction Methods

### 1. From Sequences

```python
# From list
arr = np.array([1, 2, 3])

# From nested list
arr2d = np.array([[1, 2], [3, 4]])

# With explicit dtype
arr_float = np.array([1, 2, 3], dtype=np.float64)
```

### 2. Factory Functions

```python
# Zeros
zeros = np.zeros((3, 4))

# Ones
ones = np.ones((2, 3))

# Empty (uninitialized)
empty = np.empty((5,))

# Identity
identity = np.eye(3)

# Range
arange = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]

# Linspace
linspace = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1]
```

### 3. From Functions

```python
# Using fromfunction
def f(i, j):
    return i + j

arr = np.fromfunction(f, (3, 3))
# [[0, 1, 2],
#  [1, 2, 3],
#  [2, 3, 4]]
```

## Strides and Layout

### 1. Stride Calculation

Strides define byte jumps between elements:

```python
arr = np.arange(24).reshape(2, 3, 4)
print(arr.strides)  # (96, 32, 8)

# Element at [i, j, k] is at:
# base_address + i*96 + j*32 + k*8
```

### 2. Transposition Effects

```python
arr = np.arange(6).reshape(2, 3)
print(arr.strides)  # (24, 8) - C-contiguous

arr_t = arr.T
print(arr_t.strides)  # (8, 24) - not C-contiguous
print(arr_t.flags['C_CONTIGUOUS'])  # False
```

### 3. Reshape vs Ravel

```python
arr = np.arange(12).reshape(3, 4)

# Ravel returns view if possible
flat = arr.ravel()
flat[0] = 999
print(arr[0, 0])  # 999 - view

# Flatten always copies
flat_copy = arr.flatten()
flat_copy[0] = -1
print(arr[0, 0])  # 999 - no change
```

## Ownership and Flags

### 1. Data Ownership

```python
arr = np.arange(10)
print(arr.flags['OWNDATA'])  # True

view = arr[::2]
print(view.flags['OWNDATA'])  # False - references arr's data
```

### 2. Writability

```python
arr = np.arange(5)
print(arr.flags['WRITEABLE'])  # True

arr.flags.writeable = False
# arr[0] = 999  # ValueError: assignment destination is read-only
```

### 3. Alignment

```python
arr = np.arange(10)
print(arr.flags['ALIGNED'])  # True

# Properly aligned for CPU SIMD operations
```

## Performance Implications

### 1. Contiguous Access

```python
import time

# C-contiguous access (fast)
arr = np.arange(10000000).reshape(10000, 1000)
start = time.time()
for i in range(arr.shape[0]):
    _ = arr[i, :].sum()
print(f"Row-wise: {time.time() - start:.3f}s")

# Column access (slower on C-contiguous)
start = time.time()
for j in range(arr.shape[1]):
    _ = arr[:, j].sum()
print(f"Column-wise: {time.time() - start:.3f}s")
```

### 2. View Semantics

```python
# Views avoid copies
arr = np.arange(1000000)
view = arr[::2]  # No copy, instant

# But operations may need temporaries
result = view + 1  # Creates new array
```

### 3. SIMD Vectorization

Contiguous aligned arrays enable CPU SIMD:

```python
arr = np.arange(1000000, dtype=np.float64)
# Operations vectorized across multiple elements simultaneously
result = arr * 2.0 + 1.0  # Single instruction, multiple data
```

## Best Practices

### 1. Prefer Views

```python
# ✅ GOOD - Use views
arr = np.arange(100)
subset = arr[10:20]  # View

# ❌ BAD - Unnecessary copy
subset = arr[10:20].copy()  # Only copy if needed
```

### 2. Check Contiguity

```python
def ensure_contiguous(arr):
    if not arr.flags['C_CONTIGUOUS']:
        return np.ascontiguousarray(arr)
    return arr
```

### 3. Understand Ownership

```python
arr = np.arange(10)
view = arr[::2]

# Modifying view affects original
view[0] = 999
assert arr[0] == 999

# Copy if independence needed
independent = arr[::2].copy()
```

---

## Exercises

**Exercise 1.** Write a short code example that demonstrates the main concept covered on this page. Include comments explaining each step.

??? success "Solution to Exercise 1"
    Refer to the code examples in the page content above. A complete solution would recreate the key pattern with clear comments explaining the NumPy operations involved.

---

**Exercise 2.** Predict the output of a code snippet that uses the features described on this page. Explain why the output is what it is.

??? success "Solution to Exercise 2"
    The output depends on how NumPy handles the specific operation. Key factors include array shapes, dtypes, and broadcasting rules. Trace through the computation step by step.

---

**Exercise 3.** Write a practical function that applies the concepts from this page to solve a real data processing task. Test it with sample data.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    # Example: apply the page's concept to process sample data
    data = np.random.default_rng(42).random((5, 3))
    # Apply the relevant operation
    result = data  # replace with actual operation
    print(result)
    ```

---

**Exercise 4.** Identify a common mistake when using the features described on this page. Write code that demonstrates the mistake and then show the corrected version.

??? success "Solution to Exercise 4"
    A common mistake is misunderstanding array shapes or dtypes. Always check `.shape` and `.dtype` when debugging unexpected results.
