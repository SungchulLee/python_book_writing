# np.array Basics

The `np.array` function converts Python sequences into NumPy arrays. Understanding array dimensions is fundamental to working with NumPy.

!!! tip "Mental Model"
    `np.array` is the front door to NumPy: hand it a Python list and it gives back a typed, contiguous block of memory that supports fast vectorized operations. The nesting depth of your input list determines the number of dimensions -- a flat list becomes 1D, a list of lists becomes 2D, and so on.

    Every array is fully described by three things: **data** (the values),
    **dtype** (how bytes are interpreted), and **shape** (how the flat buffer is
    folded into dimensions). `np.array` infers all three from your input, but you
    can override dtype explicitly.

!!! note "Array Creation System"
    NumPy arrays enter the system through four creation patterns:

    ```text
    1. From data       → np.array          (convert existing values)
    2. From constants  → zeros, ones, full, empty  (initialize to a value)
    3. From structure  → diag, eye, identity       (mathematical matrices)
    4. From intervals  → arange, linspace          (sampling grids)
    ```

    Each pattern serves a different computational intent: data import, buffer
    allocation, linear algebra setup, or domain discretization.

!!! note "Why Arrays Matter"
    NumPy arrays are the foundation for everything that follows in scientific Python:

    - **Vectorized operations** — element-wise math runs in compiled C, not Python loops, giving 10–100x speedups.
    - **Memory efficiency** — arrays store data in a contiguous typed block, not as scattered Python objects.
    - **Broadcasting** — arrays of different shapes can be combined without explicit loops or copies.
    - **Ecosystem integration** — pandas, scikit-learn, matplotlib, and SciPy all build on NumPy arrays.

    Every topic in later chapters — broadcasting, FFT, linear algebra, machine learning — starts with array creation.


## Dimension Concepts

NumPy arrays generalize scalars, vectors, and matrices into n-dimensional structures.

$$\begin{array}{lll}
\text{0D Array}&=&\text{Scalar}\\
\text{1D Array}&=&\text{Vector}\\
\text{2D Array}&=&\text{Matrix}\\
\text{3D Array}&=&\text{Color Image}\\
\text{4D Array}&=&\text{Batch of Images}\\
\end{array}$$

Each dimension adds another axis of indexing.


## Creating 0D Arrays

A 0D array holds a single scalar value with no axes.

### 1. Scalar Creation

```python
import numpy as np

def main():
    a = np.array(21)
    print(f'{a = }')
    print(f'{type(a) = }')
    print(f'{a.ndim = }')
    print(f'{a.shape = }')
    print(f'{a.dtype = }')

if __name__ == "__main__":
    main()
```

Output:

```
a = array(21)
type(a) = <class 'numpy.ndarray'>
a.ndim = 0
a.shape = ()
a.dtype = dtype('int64')
```

### 2. Scalar vs Tuple

```python
a = 3
print(a)      # 3

b = 3,
print(b)      # (3,)
```

A trailing comma creates a tuple, not a scalar.


## Creating 1D Arrays

A 1D array represents a vector with a single axis.

### 1. From Python List

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    print(f'{a = }')
    print(f'{type(a) = }')
    print(f'{a.ndim = }')
    print(f'{a.shape = }')
    print(f'{a.dtype = }')

if __name__ == "__main__":
    main()
```

Output:

```
a = array([1, 2, 3])
type(a) = <class 'numpy.ndarray'>
a.ndim = 1
a.shape = (3,)
a.dtype = dtype('int64')
```

### 2. Specifying dtype

```python
import numpy as np

def main():
    a = np.array([1, 2, 3], dtype=np.uint8)
    print(f'{a = }')
    print(f'{type(a) = }')
    print(f'{a.ndim = }')
    print(f'{a.shape = }')
    print(f'{a.dtype = }')

if __name__ == "__main__":
    main()
```

Output:

```
a = array([1, 2, 3], dtype=uint8)
a.dtype = dtype('uint8')
```


## Creating 2D Arrays

A 2D array represents a matrix with rows and columns.

### 1. Nested Lists

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    print(f'{a = }')
    print(f'{type(a) = }')
    print(f'{a.ndim = }')
    print(f'{a.shape = }')
    print(f'{a.dtype = }')

if __name__ == "__main__":
    main()
```

Output:

```
a = array([[1, 2, 3],
           [4, 5, 6]])
a.ndim = 2
a.shape = (2, 3)
```

### 2. Shape Interpretation

The shape `(2, 3)` means 2 rows and 3 columns.


## Creating 3D Arrays

A 3D array adds depth, commonly used for color images.

### 1. Triple Nesting

```python
import numpy as np

def main():
    a = np.array([[[1, 2, 3], [4, 5, 6]],
                  [[1, 4, 2], [5, 7, 3]]])
    print(f'{a = }')
    print(f'{type(a) = }')
    print(f'{a.ndim = }')
    print(f'{a.shape = }')
    print(f'{a.dtype = }')

if __name__ == "__main__":
    main()
```

Output:

```
a.ndim = 3
a.shape = (2, 2, 3)
```

### 2. Image Interpretation

For images, shape `(H, W, C)` represents height, width, and color channels.


## Key Attributes

Every ndarray has essential attributes for inspection.

### 1. ndim Attribute

The `ndim` attribute returns the number of dimensions.

### 2. shape Attribute

The `shape` attribute returns a tuple of dimension sizes.

### 3. dtype Attribute

The `dtype` attribute indicates the data type of elements.

---

## Runnable Example: `array_creation_tutorial.py`

```python
"""
02_array_creation.py - Creating NumPy Arrays

🔗 Connects to Topic #24: dtype controls memory usage!
"""

import numpy as np

if __name__ == "__main__":

    print("="*80)
    print("CREATING NUMPY ARRAYS")
    print("="*80)

    # ============================================================================
    # Method 1: From Python sequences
    # ============================================================================

    print("\nMethod 1: From Lists/Tuples")
    arr_from_list = np.array([1, 2, 3, 4, 5])
    arr_from_tuple = np.array((10, 20, 30))
    print(f"From list: {arr_from_list}")
    print(f"From tuple: {arr_from_tuple}")

    # Multi-dimensional
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"\n2D array:\n{matrix}")
    print(f"Shape: {matrix.shape}")  # (rows, columns)

    # ============================================================================
    # Method 2: Zeros, Ones, Empty
    # ============================================================================

    print("\n" + "="*80)
    print("Method 2: Special Arrays")
    print("="*80)

    zeros = np.zeros(5)  # All zeros
    print(f"Zeros: {zeros}")

    ones = np.ones((3, 3))  # 3x3 matrix of ones
    print(f"\nOnes:\n{ones}")

    # Empty (uninitialized - fastest but random values!)
    empty = np.empty(3)  # Memory not cleared (Topic #24!)
    print(f"\nEmpty (uninitialized): {empty}")
    print("  Warning: Contains whatever was in memory!")

    # ============================================================================
    # Method 3: Arange and Linspace
    # ============================================================================

    print("\n" + "="*80)
    print("Method 3: Number Sequences")
    print("="*80)

    # arange: Like Python range()
    arr_range = np.arange(10)  # 0 to 9
    print(f"arange(10): {arr_range}")

    arr_range2 = np.arange(5, 15, 2)  # start, stop, step
    print(f"arange(5, 15, 2): {arr_range2}")

    # linspace: Evenly spaced over interval
    arr_lin = np.linspace(0, 1, 5)  # 5 points from 0 to 1
    print(f"\nlinspace(0, 1, 5): {arr_lin}")
    print("  Includes both endpoints!")

    # ============================================================================
    # Method 4: Random Arrays
    # ============================================================================

    print("\n" + "="*80)
    print("Method 4: Random Arrays")
    print("="*80)

    # Uniform random [0, 1)
    random_uniform = np.random.rand(5)
    print(f"Random uniform: {random_uniform}")

    # Normal distribution (mean=0, std=1)
    random_normal = np.random.randn(5)
    print(f"Random normal: {random_normal}")

    # Random integers
    random_ints = np.random.randint(0, 100, size=5)  # 5 ints in [0,100)
    print(f"Random integers: {random_ints}")

    # ============================================================================
    # CRITICAL: dtype Parameter (Topic #24 - Memory Control!)
    # ============================================================================

    print("\n" + "="*80)
    print("CRITICAL: dtype Parameter (Memory Control!)")
    print("="*80)

    print("\n🔗 Connects to Topic #24: Choose dtype to control memory!\n")

    arr_default = np.array([1, 2, 3])  # Default: int64 or int32
    arr_int8 = np.array([1, 2, 3], dtype=np.int8)
    arr_int32 = np.array([1, 2, 3], dtype=np.int32)
    arr_float32 = np.array([1, 2, 3], dtype=np.float32)
    arr_float64 = np.array([1, 2, 3], dtype=np.float64)

    print("Same data [1, 2, 3], different dtypes:")
    print(f"  default:  dtype={arr_default.dtype:8}, size={arr_default.nbytes} bytes")
    print(f"  int8:     dtype={arr_int8.dtype:8}, size={arr_int8.nbytes} bytes")
    print(f"  int32:    dtype={arr_int32.dtype:8}, size={arr_int32.nbytes} bytes")
    print(f"  float32:  dtype={arr_float32.dtype:8}, size={arr_float32.nbytes} bytes")
    print(f"  float64:  dtype={arr_float64.dtype:8}, size={arr_float64.nbytes} bytes")

    print("""
    \nChoosing dtype wisely:
    - int8: Values -128 to 127 (1 byte)
    - int16: Values -32,768 to 32,767 (2 bytes)
    - int32: Values ±2 billion (4 bytes)
    - int64: Larger values (8 bytes)
    - float32: ~7 decimal digits precision (4 bytes)
    - float64: ~15 decimal digits precision (8 bytes)

    For 1 million numbers:
      int8: 1 MB
      int64: 8 MB
      float64: 8 MB

    Memory matters at scale! (Topic #24)
    """)

    # ============================================================================
    # Array Properties
    # ============================================================================

    print("="*80)
    print("Array Properties")
    print("="*80)

    arr = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"\nArray:\n{arr}")
    print(f"  .shape: {arr.shape} ← (rows, cols)")
    print(f"  .ndim: {arr.ndim} ← Number of dimensions")
    print(f"  .size: {arr.size} ← Total elements")
    print(f"  .dtype: {arr.dtype} ← Data type")
    print(f"  .nbytes: {arr.nbytes} ← Memory in bytes")
    print(f"  .itemsize: {arr.itemsize} ← Bytes per element")

    print("""
    \n🎯 KEY TAKEAWAYS:
    1. Many ways to create arrays
    2. dtype controls memory (Topic #24!)
    3. Use appropriate dtype for your data range
    4. Array properties tell you size and memory usage

    🔜 NEXT: 03_array_indexing.py
    """)
```

---

## Exercises

**Exercise 1.**
Create a 0D array containing the value 42. Print its `ndim`, `shape`, and `size`. Then create a 1D array containing just `[42]` and compare all three attributes with the 0D version.

??? success "Solution to Exercise 1"

        import numpy as np

        a_0d = np.array(42)
        a_1d = np.array([42])

        print(f"0D: ndim={a_0d.ndim}, shape={a_0d.shape}, size={a_0d.size}")
        print(f"1D: ndim={a_1d.ndim}, shape={a_1d.shape}, size={a_1d.size}")

---

**Exercise 2.**
Create a 3D array from nested lists representing a 2x3x4 block (2 layers, 3 rows, 4 columns). Verify its shape is `(2, 3, 4)` and print the total number of elements using `a.size`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([[[1,  2,  3,  4],
                        [5,  6,  7,  8],
                        [9, 10, 11, 12]],
                       [[13, 14, 15, 16],
                        [17, 18, 19, 20],
                        [21, 22, 23, 24]]])
        print(f"Shape: {a.shape}")  # (2, 3, 4)
        print(f"Total elements: {a.size}")  # 24

---

**Exercise 3.**
Create two arrays from the same list `[1, 2, 3]`: one with `dtype=np.float32` and one with `dtype=np.int8`. Print the `nbytes` of each and compute the memory savings ratio.

??? success "Solution to Exercise 3"

        import numpy as np

        data = [1, 2, 3]
        a_f32 = np.array(data, dtype=np.float32)
        a_i8 = np.array(data, dtype=np.int8)

        print(f"float32 nbytes: {a_f32.nbytes}")  # 12
        print(f"int8 nbytes:    {a_i8.nbytes}")    # 3
        print(f"Memory ratio: {a_f32.nbytes / a_i8.nbytes:.1f}x")
