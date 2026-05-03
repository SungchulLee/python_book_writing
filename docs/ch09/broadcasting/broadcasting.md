# Broadcasting Rules

Broadcasting allows NumPy to perform elementwise operations on arrays of different shapes without explicit loops.

!!! tip "Mental Model"
    Broadcasting is NumPy's rule for stretching smaller arrays to match larger ones during element-wise operations -- without actually copying data. Imagine tiling a single row across all rows of a matrix: NumPy does this virtually, comparing shapes right-to-left and requiring each axis to be equal or one.


## Motivation

Broadcasting eliminates common inefficiencies in numerical code.

### 1. No Manual Reshaping

Arrays of compatible shapes work directly without explicit dimension manipulation.

### 2. No Explicit Loops

Vectorized operations replace slow Python for-loops.

### 3. No Memory Copies

NumPy virtually expands dimensions without duplicating data in memory.


## Core Rules

NumPy compares shapes from the trailing (rightmost) dimensions.

### 1. Right-to-Left

Dimensions are aligned starting from the last axis and moving left.

### 2. Compatible Sizes

Two dimensions are compatible if they are equal or one of them is 1.

### 3. Expansion Rule

Size-1 dimensions are virtually stretched to match the other array.


## Formal Rule

The compatibility rules expressed mathematically.

### 1. Rule Summary

$$\begin{array}{lll}
s_1=s_2&\Rightarrow&\text{OK}\\
s_1\neq s_2,\ \text{but one of them is 1}&\Rightarrow&\text{OK}\\
\text{one of them does not exist}&\Rightarrow&\text{OK}\\
s_1\neq s_2,\ s_1\neq 1, s_2\neq 1&\Rightarrow&\text{NOT OK}\\
\end{array}$$

### 2. Result Shape

The resultant shape is the element-wise maximum of input shapes across each dimension.


## The Complete Algorithm

!!! tip "Broadcasting in Five Steps"
    ```text
    1. PAD — prepend 1s to the shorter shape until both have the same ndim
    2. ALIGN — compare shapes right-to-left, axis by axis
    3. CHECK — each pair must be equal or one must be 1
    4. EXPAND — size-1 axes are virtually stretched to match
    5. RESULT — the output shape is the element-wise maximum
    ```

    **Under the hood:** NumPy does not copy data to expand size-1 axes. Instead, it sets the **stride to 0** along that axis — the same memory is read repeatedly. This is why broadcasting is both fast and memory-efficient: the "stretched" array exists only as a view with modified strides.

## Visual Alignment

Understanding how shapes align is key to mastering broadcasting.

### 1. Scalar + Vector

```
Array A:         5        shape: ()
Array B:     [1, 2, 3]    shape: (3,)
─────────────────────────────────────
Aligned:         5        shape: (1,) → (3,)
             [1, 2, 3]    shape: (3,)
─────────────────────────────────────
Result:      [6, 7, 8]    shape: (3,)
```

```python
import numpy as np

a = 5
b = np.array([1, 2, 3])
print(a + b)  # [6 7 8]
```

### 2. Vector + Matrix

```
Array A:     [[1, 2, 3],      shape: (2, 3)
              [4, 5, 6]]

Array B:     [10, 20, 30]     shape: (3,)
─────────────────────────────────────────────
Aligned:     [[1, 2, 3],      shape: (2, 3)
              [4, 5, 6]]

             [10, 20, 30]     shape: (1, 3) → (2, 3)
─────────────────────────────────────────────
Result:      [[11, 22, 33],   shape: (2, 3)
              [14, 25, 36]]
```

```python
import numpy as np

M = np.array([[1, 2, 3],
              [4, 5, 6]])
v = np.array([10, 20, 30])
print(M + v)
```

### 3. Column + Row

```
Array A:     [[1],        shape: (3, 1)
              [2],
              [3]]

Array B:     [10, 20]     shape: (2,)
─────────────────────────────────────────────
Aligned:     [[1],        shape: (3, 1) → (3, 2)
              [2],
              [3]]

             [10, 20]     shape: (1, 2) → (3, 2)
─────────────────────────────────────────────
Result:      [[11, 21],   shape: (3, 2)
              [12, 22],
              [13, 23]]
```

```python
import numpy as np

x = np.array([[1], [2], [3]])  # shape (3, 1)
y = np.array([10, 20])          # shape (2,)
print(x + y)
```


## Basic Examples

Simple broadcasting patterns with 2D arrays.

### 1. Matrix × Row

```python
import numpy as np

def main():
    A = np.array([[0, 1], [21, 22]])  # (2, 2)
    B = np.array([[1, 2]])             # (1, 2)
    C = A * B
    print(C)

if __name__ == "__main__":
    main()
```

Output:

```
[[ 0  2]
 [21 44]]
```

### 2. Matrix + Vector

```python
import numpy as np

def main():
    A = np.array([[0, 1], [21, 22]])  # (2, 2)
    B = np.array([1, 2])               #    (2,)
    C = A + B
    print(C)

if __name__ == "__main__":
    main()
```

Output:

```
[[ 1  3]
 [22 24]]
```

### 3. Matrix + Scalar

```python
import numpy as np

def main():
    A = np.array([[1, 2], [3, 4]])  # (2, 2)
    B = 5                            #    ()
    C = A + B
    print(C)

if __name__ == "__main__":
    main()
```

Output:

```
[[6 7]
 [8 9]]
```


## Higher Dimensions

Broadcasting works with tensors of any rank.

### 1. 4D + 3D Arrays

```python
import numpy as np

def main():
    A = np.random.normal(size=(8, 1, 4, 1))
    B = np.random.normal(size=(7, 1, 5))
    C = A + B
    print(f"{A.shape = }")
    print(f"{B.shape =    }")
    print(f"{C.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
A.shape = (8, 1, 4, 1)
B.shape =    (7, 1, 5)
C.shape = (8, 7, 4, 5)
```

### 2. 2D + Singleton

```python
import numpy as np

def main():
    A = np.random.normal(size=(5, 4))
    B = np.random.normal(size=(1,))
    C = A + B
    print(f"{A.shape = }")
    print(f"{B.shape =    }")
    print(f"{C.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
A.shape = (5, 4)
B.shape =    (1,)
C.shape = (5, 4)
```

### 3. 3D + 2D Arrays

```python
import numpy as np

def main():
    A = np.random.normal(size=(15, 3, 5))
    B = np.random.normal(size=(3, 5))
    C = A + B
    print(f"{A.shape = }")
    print(f"{B.shape =     }")
    print(f"{C.shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
A.shape = (15, 3, 5)
B.shape =     (3, 5)
C.shape = (15, 3, 5)
```


## Error Cases

Incompatible shapes raise `ValueError`.

### 1. Same Rank Mismatch

```python
import numpy as np

def main():
    A = np.random.normal(size=(2, 3))
    B = np.random.normal(size=(2, 7))
    try:
        C = A + B
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

Output:

```
Error: operands could not be broadcast together with shapes (2,3) (2,7)
```

### 2. Different Rank Mismatch

```python
import numpy as np

def main():
    A = np.random.normal(size=(3, 1))
    B = np.random.normal(size=(8, 4, 3))
    try:
        C = A + B
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

Output:

```
Error: operands could not be broadcast together with shapes (3,1) (8,4,3)
```

### 3. Another Mismatch

```python
import numpy as np

def main():
    A = np.random.normal(size=(2, 1))
    B = np.random.normal(size=(8, 4, 3))
    try:
        C = A + B
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

Output:

```
Error: operands could not be broadcast together with shapes (2,1) (8,4,3)
```


## Normalization Example

A practical application of broadcasting.

### 1. Column-wise Normalize

```python
import numpy as np

def main():
    num_paths, num_steps = 10, 100
    Z = np.random.standard_normal((num_paths, num_steps))
    print(f"{Z.shape              = }")
    print(f"{Z.mean(axis=0).shape =     }")
    print(f"{Z.std(axis=0).shape  =     }")

    Z = (Z - Z.mean(axis=0)) / Z.std(axis=0)
    print(f"{Z.shape              = }")

if __name__ == "__main__":
    main()
```

Output:

```
Z.shape              = (10, 100)
Z.mean(axis=0).shape =     (100,)
Z.std(axis=0).shape  =     (100,)
Z.shape              = (10, 100)
```

### 2. How It Works

`Z.mean(axis=0)` has shape `(100,)` which broadcasts against `Z` with shape `(10, 100)`.


## Performance Compare

Broadcasting dramatically outperforms explicit Python loops.

### 1. Loop Approach

```python
import numpy as np
import time

def add_with_loops(M, v):
    result = np.empty_like(M)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            result[i, j] = M[i, j] + v[j]
    return result

M = np.random.randn(1000, 1000)
v = np.random.randn(1000)

start = time.perf_counter()
result_loop = add_with_loops(M, v)
loop_time = time.perf_counter() - start
print(f"Loop time: {loop_time:.4f} sec")
```

### 2. Broadcast Approach

```python
import numpy as np
import time

M = np.random.randn(1000, 1000)
v = np.random.randn(1000)

start = time.perf_counter()
result_broadcast = M + v
broadcast_time = time.perf_counter() - start
print(f"Broadcast time: {broadcast_time:.6f} sec")
```

### 3. Speedup Factor

```python
import numpy as np
import time

def add_with_loops(M, v):
    result = np.empty_like(M)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            result[i, j] = M[i, j] + v[j]
    return result

def main():
    np.random.seed(42)
    M = np.random.randn(1000, 1000)
    v = np.random.randn(1000)

    start = time.perf_counter()
    result_loop = add_with_loops(M, v)
    loop_time = time.perf_counter() - start

    start = time.perf_counter()
    result_broadcast = M + v
    broadcast_time = time.perf_counter() - start

    assert np.allclose(result_loop, result_broadcast)

    print(f"Loop time:      {loop_time:.4f} sec")
    print(f"Broadcast time: {broadcast_time:.6f} sec")
    print(f"Speedup:        {loop_time / broadcast_time:.0f}x")

if __name__ == "__main__":
    main()
```

Typical output:

```
Loop time:      0.3521 sec
Broadcast time: 0.001243 sec
Speedup:        283x
```


## Memory Efficiency

Broadcasting avoids unnecessary memory allocation.

### 1. No Data Copy

```python
import numpy as np

v = np.array([1, 2, 3])
M = np.zeros((1000, 3))
result = M + v  # v is virtually expanded
```

### 2. Virtual Expansion

NumPy's stride mechanism allows size-1 dimensions to be reused without copying.

### 3. Large Array Savings

For a `(10000, 10000)` matrix plus a `(10000,)` vector, broadcasting saves ~800 MB of memory.


## Common Pitfalls

Avoid these broadcasting mistakes.

### 1. Dimension Assumptions

Erroneous assumptions regarding implicit dimension expansion.

### 2. Missing Reshapes

Failure to use `np.reshape` or `np.newaxis` when necessary.

### 3. Memory Amplification

Unintended memory growth in operations involving large singleton expansions.


## Key Takeaways

Essential points for effective broadcasting.

### 1. Align Right

Shapes are compared from the trailing dimension leftward.

### 2. Size-1 Expands

Dimensions of size 1 stretch to match the corresponding dimension.

### 3. Use for Speed

Broadcasting is 100-1000x faster than Python loops.

---

## Runnable Example: `broadcasting_tutorial.py`

```python
"""
01_broadcasting.py - NumPy's Most Powerful Feature!

Broadcasting allows arrays of different shapes to work together.
This is what makes NumPy code so elegant and fast!
"""

import numpy as np

if __name__ == "__main__":

    print("="*80)
    print("BROADCASTING - NumPy's Superpower!")
    print("="*80)

    # ============================================================================
    # What is Broadcasting?
    # ============================================================================

    print("\nBroadcasting: Operating on arrays of different shapes")
    print("="*80)

    # Simple example
    arr = np.array([1, 2, 3])
    print(f"arr = {arr}  (shape: {arr.shape})")
    print(f"arr + 10 = {arr + 10}")
    print("\nWhat happened? 10 was 'broadcast' to [10, 10, 10]!")

    # ============================================================================
    # Broadcasting Rules
    # ============================================================================

    print("\n" + "="*80)
    print("The Three Broadcasting Rules")
    print("="*80)

    print("""
    Rule 1: If arrays have different ndim, pad smaller with 1s on LEFT
      arr1.shape = (3, 4, 5)
      arr2.shape = (5,)      → becomes (1, 1, 5)

    Rule 2: Dimensions with size 1 are stretched
      arr1.shape = (3, 1, 5)
      arr2.shape = (1, 4, 5) → both become (3, 4, 5)

    Rule 3: Dimensions must match or be 1, else ERROR
      arr1.shape = (3, 4)
      arr2.shape = (3, 5)  ← ERROR! 4 != 5 and neither is 1
    """)

    # ============================================================================
    # Common Patterns
    # ============================================================================

    print("="*80)
    print("Common Broadcasting Patterns")
    print("="*80)

    # Pattern 1: Add row vector to matrix
    print("\nPattern 1: Add vector to each row")
    matrix = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [7, 8, 9]])
    row_vec = np.array([10, 20, 30])

    print(f"Matrix (3,3):\n{matrix}")
    print(f"Vector (3,): {row_vec}")
    result = matrix + row_vec
    print(f"Result:\n{result}")
    print("Each row gets the vector added!")

    # Pattern 2: Add column vector to matrix
    print("\nPattern 2: Add vector to each column")
    col_vec = np.array([[100], [200], [300]])  # Shape (3, 1)
    print(f"Column vector (3,1):\n{col_vec}")
    result = matrix + col_vec
    print(f"Result:\n{result}")
    print("Each column gets the vector added!")

    # Pattern 3: Outer product
    print("\nPattern 3: Multiplication table (outer product)")
    x = np.arange(1, 6).reshape(5, 1)  # (5, 1)
    y = np.arange(1, 6).reshape(1, 5)  # (1, 5)
    table = x * y
    print(f"x (column):\n{x}")
    print(f"y (row): {y}")
    print(f"\nMultiplication table:\n{table}")

    # ============================================================================
    # Practical Example: Normalizing data
    # ============================================================================

    print("\n" + "="*80)
    print("Practical: Normalizing Each Column")
    print("="*80)

    # Data: 5 samples, 3 features
    data = np.random.randint(0, 100, (5, 3)).astype(float)
    print(f"Data (5 samples, 3 features):\n{data}\n")

    # Calculate mean of each column
    means = data.mean(axis=0)  # Shape (3,)
    print(f"Column means: {means}  (shape: {means.shape})")

    # Subtract mean (broadcasting!)
    centered = data - means  # (5,3) - (3,) broadcasts!
    print(f"\nCentered data:\n{centered}")
    print(f"\nNew column means: {centered.mean(axis=0)}")
    print("  (Should be ~0 for each column)")

    print("""
    \nWhat happened?
      data.shape = (5, 3)
      means.shape = (3,)

    Broadcasting:
      means is treated as shape (1, 3)
      Then stretched to (5, 3)
      So each row gets the same means subtracted!
    """)

    print("""
    \n🎯 KEY TAKEAWAYS:
    1. Broadcasting eliminates explicit loops
    2. Works with arrays of different shapes
    3. Memory efficient (no actual copying)
    4. Master this for elegant NumPy code!

    🔜 NEXT: 02_shape_manipulation.py
    """)
```

---

## Exercises

**Exercise 1.**
Predict the result shape of each operation without running the code, then verify with NumPy:

- `np.ones((5, 3)) + np.ones((3,))`
- `np.ones((4, 1)) * np.ones((1, 6))`
- `np.ones((2, 1, 4)) + np.ones((3, 1))`

??? success "Solution to Exercise 1"

        import numpy as np

        # Predict then verify
        r1 = np.ones((5, 3)) + np.ones((3,))
        print(r1.shape)  # (5, 3)

        r2 = np.ones((4, 1)) * np.ones((1, 6))
        print(r2.shape)  # (4, 6)

        r3 = np.ones((2, 1, 4)) + np.ones((3, 1))
        print(r3.shape)  # (2, 3, 4)

---

**Exercise 2.**
Given a 2D array `data` of shape `(100, 5)`, use broadcasting to subtract the row-wise minimum from every element in each row so that each row's smallest value becomes zero. Do not use any explicit Python loop.

??? success "Solution to Exercise 2"

        import numpy as np

        data = np.random.randn(100, 5)
        row_min = data.min(axis=1, keepdims=True)  # shape (100, 1)
        result = data - row_min                     # broadcasts (100, 5) - (100, 1)
        print(result.min(axis=1))  # all zeros

---

**Exercise 3.**
Write a function that takes two 1D arrays `a` of shape `(m,)` and `b` of shape `(n,)` and returns a 2D boolean array of shape `(m, n)` where entry `(i, j)` is `True` if `a[i] > b[j]`, using only broadcasting (no loops).

??? success "Solution to Exercise 3"

        import numpy as np

        def pairwise_greater(a, b):
            return a[:, np.newaxis] > b[np.newaxis, :]

        a = np.array([3, 1, 4])
        b = np.array([2, 5])
        result = pairwise_greater(a, b)
        print(result)
        # [[ True False]
        #  [False False]
        #  [ True False]]
        print(result.shape)  # (3, 2)

---

**Exercise 4.**
Use `np.broadcast_to` to inspect what a scalar `5` looks like when broadcast to shape `(3, 4)`. Print the result, its shape, and its strides. Explain why the stride is `(0, 0)` and what this means for memory usage.

??? success "Solution to Exercise 4"

        import numpy as np

        scalar = np.array(5)
        expanded = np.broadcast_to(scalar, (3, 4))
        print(expanded)
        print(f"Shape:   {expanded.shape}")    # (3, 4)
        print(f"Strides: {expanded.strides}")  # (0, 0)
        print(f"Memory:  {scalar.nbytes} bytes (actual)")

        # Strides (0, 0) means: moving along any axis reads the
        # same memory location. The value 5 is stored once (8 bytes)
        # but appears as a 3×4 array. No data is copied — NumPy
        # reuses the single value by setting both strides to zero.
        # This is how broadcasting achieves zero-copy expansion.

---

**Exercise 5.**
Walk through the broadcasting algorithm step by step for shapes `(8, 1, 4, 1)` and `(7, 1, 5)`. Show the padding, alignment, compatibility check for each axis, and the final result shape. Verify with `np.broadcast_shapes`.

??? success "Solution to Exercise 5"

        import numpy as np

        # Step 1: PAD — shorter shape gets 1s prepended
        # A: (8, 1, 4, 1)   — already 4D
        # B:    (7, 1, 5)   → (1, 7, 1, 5)

        # Step 2: ALIGN right-to-left
        # axis:  0  1  2  3
        # A:     8  1  4  1
        # B:     1  7  1  5

        # Step 3: CHECK each axis
        # axis 0: 8 vs 1 → OK (1 expands)
        # axis 1: 1 vs 7 → OK (1 expands)
        # axis 2: 4 vs 1 → OK (1 expands)
        # axis 3: 1 vs 5 → OK (1 expands)

        # Step 4: EXPAND 1s → max per axis
        # Step 5: RESULT = (8, 7, 4, 5)

        result = np.broadcast_shapes((8, 1, 4, 1), (7, 1, 5))
        print(result)  # (8, 7, 4, 5)
