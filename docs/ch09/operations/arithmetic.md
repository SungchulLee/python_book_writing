# Arithmetic Operations

NumPy arrays support element-wise arithmetic operations.

!!! tip "Mental Model"
    Every arithmetic operator (`+`, `-`, `*`, `/`, `**`) in NumPy works element-by-element, not as matrix algebra. `A * B` multiplies corresponding elements, not rows-by-columns. This element-wise default, combined with broadcasting, lets you write compact formulas that look like scalar math but operate on entire arrays at C speed.

    Under the hood, **all arithmetic is ufuncs**: `a + b` dispatches to `np.add(a, b)`,
    `a * b` to `np.multiply(a, b)`, and so on. This means arithmetic inherits every
    ufunc feature — broadcasting, `out=` parameter, `reduce`, `accumulate` — for free.

!!! note "Array Computation Model"
    All NumPy operations in this section follow a single pattern:

    1. Take input arrays
    2. Align shapes via **broadcasting**
    3. Apply a scalar function **element-wise** (ufunc)
    4. Produce output array

    This pattern covers arithmetic (`+`, `*`), comparisons (`<`, `==`), math
    functions (`exp`, `log`), and rounding (`floor`, `ceil`). The sections that
    follow are variations on this one mechanism.

## Addition

### 1. Array Addition

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    c = a + b
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a + b = {c}")

if __name__ == "__main__":
    main()
```

**Output:**

```
a = [1 2 3]
b = [4 5 6]
a + b = [5 7 9]
```

### 2. Scalar Addition

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = 4
    
    c = a + b
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a + b = {c}")

if __name__ == "__main__":
    main()
```

### 3. 2D Array Addition

```python
import numpy as np

def main():
    a = np.array([[1, 1], [2, 3]])
    b = np.array([[1, 1], [2, 3]])
    
    c = a + b
    
    print("a + b =")
    print(c)

if __name__ == "__main__":
    main()
```

## Subtraction

### 1. Array Subtraction

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[1, 1], [2, 2]])
    
    c = a - b
    
    print("a =")
    print(a)
    print()
    print("b =")
    print(b)
    print()
    print("a - b =")
    print(c)

if __name__ == "__main__":
    main()
```

### 2. Negation

```python
import numpy as np

def main():
    a = np.array([1, -2, 3, -4])
    
    print(f"a = {a}")
    print(f"-a = {-a}")

if __name__ == "__main__":
    main()
```

## Multiplication

### 1. Element-wise Multiply

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[2, 2], [2, 2]])
    
    # Three equivalent ways
    c1 = a * b
    c2 = np.multiply(a, b)
    c3 = a.__mul__(b)
    
    print("a * b =")
    print(c1)
    print()
    print("np.multiply(a, b) =")
    print(c2)

if __name__ == "__main__":
    main()
```

### 2. Scalar Multiply

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    scalar = 3.5
    
    print(f"a = {a}")
    print(f"{scalar} * a = {scalar * a}")

if __name__ == "__main__":
    main()
```

## Division

### 1. True Division

```python
import numpy as np

def main():
    a = np.array([10, 20, 30])
    b = np.array([3, 4, 5])
    
    c = a / b
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a / b = {c}")

if __name__ == "__main__":
    main()
```

### 2. Floor Division

```python
import numpy as np

def main():
    a = np.array([10, 20, 30])
    b = np.array([3, 4, 5])
    
    c = a // b
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"a // b = {c}")

if __name__ == "__main__":
    main()
```

### 3. Modulo

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3, 4, 5],
                  [6, 7, 8, 9, 10]])
    
    b = a % 2
    
    print("a =")
    print(a)
    print()
    print("a % 2 =")
    print(b)

if __name__ == "__main__":
    main()
```

## __add__ vs __iadd__

### 1. Regular Addition

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    original_id = id(a)
    
    a = a + 100  # __add__: creates new array
    
    print(f"ID changed: {id(a) != original_id}")
    print(a)

if __name__ == "__main__":
    main()
```

### 2. In-place Addition

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    original_id = id(a)
    
    a += 100  # __iadd__: modifies in place
    
    print(f"ID changed: {id(a) != original_id}")
    print(a)

if __name__ == "__main__":
    main()
```

### 3. Performance Difference

```python
import numpy as np
import time

def main():
    n = 10_000
    
    # __add__ (creates copy)
    a = np.random.randn(n, n)
    start = time.perf_counter()
    a = a + 100
    add_time = time.perf_counter() - start
    
    # __iadd__ (in-place)
    b = np.random.randn(n, n)
    start = time.perf_counter()
    b += 100
    iadd_time = time.perf_counter() - start
    
    print(f"a = a + 100: {add_time:.4f} sec")
    print(f"a += 100:    {iadd_time:.4f} sec")
    print(f"Speedup:     {add_time/iadd_time:.2f}x")

if __name__ == "__main__":
    main()
```

## In-place Operators

### 1. All In-place Operators

```python
import numpy as np

def main():
    a = np.array([10, 20, 30], dtype=float)
    
    print(f"Original: {a}")
    
    a += 5
    print(f"a += 5:   {a}")
    
    a -= 5
    print(f"a -= 5:   {a}")
    
    a *= 2
    print(f"a *= 2:   {a}")
    
    a /= 2
    print(f"a /= 2:   {a}")
    
    a //= 3
    print(f"a //= 3:  {a}")
    
    a %= 2
    print(f"a %= 2:   {a}")

if __name__ == "__main__":
    main()
```

### 2. When to Use In-place

- Large arrays where memory matters
- Repeated operations in loops
- When original data is no longer needed

### 3. Caveats

```python
import numpy as np

def main():
    # In-place cannot change dtype
    a = np.array([1, 2, 3], dtype=int)
    
    # This works (result fits in int)
    a *= 2
    print(f"a *= 2: {a}, dtype: {a.dtype}")
    
    # This may truncate (float -> int)
    a = np.array([1, 2, 3], dtype=int)
    a /= 2  # Becomes float division, but stored as int
    print(f"a /= 2: {a}, dtype: {a.dtype}")

if __name__ == "__main__":
    main()
```

## Broadcasting in Arithmetic

### 1. Different Shapes

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])  # (3,)
    b = np.array([[1], [2], [3], [4]])  # (4, 1)
    
    c = a + b  # (4, 3)
    
    print(f"a shape: {a.shape}")
    print(f"b shape: {b.shape}")
    print(f"a + b shape: {c.shape}")
    print()
    print("a + b =")
    print(c)

if __name__ == "__main__":
    main()
```

### 2. Incompatible Shapes

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])  # (3,)
    b = np.array([4, 5, 6, 7])  # (4,)
    
    try:
        c = a + b
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### 3. Shape Requirements

Arrays broadcast when trailing dimensions match or one is 1.

## Function Equivalents

### 1. np.add and np.subtract

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    print(f"np.add(a, b) = {np.add(a, b)}")
    print(f"np.subtract(a, b) = {np.subtract(a, b)}")

if __name__ == "__main__":
    main()
```

### 2. np.multiply and np.divide

```python
import numpy as np

def main():
    a = np.array([10, 20, 30])
    b = np.array([2, 4, 5])
    
    print(f"np.multiply(a, b) = {np.multiply(a, b)}")
    print(f"np.divide(a, b) = {np.divide(a, b)}")
    print(f"np.floor_divide(a, b) = {np.floor_divide(a, b)}")
    print(f"np.mod(a, b) = {np.mod(a, b)}")

if __name__ == "__main__":
    main()
```

### 3. Using out Parameter

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    result = np.empty(3)
    
    np.add(a, b, out=result)
    
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

---

## Runnable Example: `basic_operations_tutorial.py`

```python
"""
04_basic_operations.py - Vectorized Operations

Key concept: Eliminate Python loops with vectorization!
"""

import numpy as np

if __name__ == "__main__":

    print("="*80)
    print("VECTORIZED OPERATIONS - No Loops Needed!")
    print("="*80)

    # ============================================================================
    # Element-wise Arithmetic
    # ============================================================================

    print("\nElement-wise Arithmetic (Vectorization)")
    print("="*80)

    arr = np.array([1, 2, 3, 4, 5])
    print(f"Array: {arr}")
    print(f"  arr + 10 = {arr + 10}  ← Add to all")
    print(f"  arr * 2 = {arr * 2}   ← Multiply all")
    print(f"  arr ** 2 = {arr ** 2}  ← Square all")
    print(f"  1 / arr = {1 / arr}  ← Reciprocal")

    print("""
    \nCompare to Python lists:
      # Python (SLOW - explicit loop):
      result = [x * 2 for x in my_list]

      # NumPy (FAST - vectorized):
      result = arr * 2

    Vectorization = C-speed loop hidden from Python!
    """)

    # Two arrays
    arr1 = np.array([1, 2, 3])
    arr2 = np.array([10, 20, 30])
    print(f"\narr1 = {arr1}")
    print(f"arr2 = {arr2}")
    print(f"  arr1 + arr2 = {arr1 + arr2}  ← Element-wise")
    print(f"  arr1 * arr2 = {arr1 * arr2}  ← Element-wise")

    # ============================================================================
    # Universal Functions (ufuncs)
    # ============================================================================

    print("\n" + "="*80)
    print("Universal Functions (ufuncs)")
    print("="*80)

    arr = np.array([1, 2, 3, 4])
    print(f"Array: {arr}")
    print(f"  np.sqrt(arr) = {np.sqrt(arr)}")
    print(f"  np.exp(arr) = {np.exp(arr)}")
    print(f"  np.log(arr) = {np.log(arr)}")
    print(f"  np.sin(arr) = {np.sin(arr)}")

    # ============================================================================
    # Comparison Operations
    # ============================================================================

    print("\n" + "="*80)
    print("Comparison Operations")
    print("="*80)

    arr = np.array([10, 15, 20, 25, 30])
    print(f"Array: {arr}")
    print(f"  arr > 18 = {arr > 18}  ← Boolean array")
    print(f"  arr == 20 = {arr == 20}")
    print(f"  (arr >= 15) & (arr <= 25) = {(arr >= 15) & (arr <= 25)}")

    # ============================================================================
    # Aggregation Functions
    # ============================================================================

    print("\n" + "="*80)
    print("Aggregation Functions")
    print("="*80)

    arr = np.array([10, 20, 30, 40, 50])
    print(f"Array: {arr}")
    print(f"  arr.sum() = {arr.sum()}")
    print(f"  arr.mean() = {arr.mean()}")
    print(f"  arr.std() = {arr.std():.2f}")
    print(f"  arr.min() = {arr.min()}")
    print(f"  arr.max() = {arr.max()}")
    print(f"  arr.argmin() = {arr.argmin()} ← Index of min")
    print(f"  arr.argmax() = {arr.argmax()} ← Index of max")

    # 2D aggregations
    matrix = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"\nMatrix:\n{matrix}")
    print(f"  matrix.sum() = {matrix.sum()} ← Total sum")
    print(f"  matrix.sum(axis=0) = {matrix.sum(axis=0)} ← Sum columns")
    print(f"  matrix.sum(axis=1) = {matrix.sum(axis=1)} ← Sum rows")

    print("""
    \n🎯 KEY TAKEAWAYS:
    1. Vectorization eliminates loops (50-200x faster!)
    2. Arithmetic works element-wise
    3. Universal functions (ufuncs) for math
    4. Aggregations: sum, mean, std, min, max
    5. axis parameter: 0=columns, 1=rows

    🔜 NEXT: Intermediate tutorials on broadcasting!
    """)
```

---

## Exercises

**Exercise 1.** Create two NumPy arrays `a = [10, 20, 30]` and `b = [3, 5, 7]`. Compute element-wise addition, subtraction, multiplication, division, and integer division. Print all results.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np

    a = np.array([10, 20, 30])
    b = np.array([3, 5, 7])

    print("Add:", a + b)       # [13 25 37]
    print("Sub:", a - b)       # [ 7 15 23]
    print("Mul:", a * b)       # [ 30 100 210]
    print("Div:", a / b)       # [3.333 4.0 4.286]
    print("IntDiv:", a // b)   # [3 4 4]
    ```

---

**Exercise 2.** Predict the output:

```python
import numpy as np
a = np.array([1, 2, 3])
b = np.array([10])
print(a + b)
print(a * b)
```

??? success "Solution to Exercise 2"
    ```
    [11 12 13]
    [10 20 30]
    ```

    Broadcasting: the scalar array `[10]` is broadcast to match the shape of `a`.

---

**Exercise 3.** Create a 3x3 matrix of ones and add a 1D array `[1, 2, 3]` to each row using broadcasting. Explain why this works.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    matrix = np.ones((3, 3))
    row = np.array([1, 2, 3])
    result = matrix + row
    print(result)
    # [[2. 3. 4.]
    #  [2. 3. 4.]
    #  [2. 3. 4.]]
    ```

    Broadcasting adds the 1D array to each row of the 2D matrix because their trailing dimensions match.

---

**Exercise 4.** Write a function `normalize(arr)` that subtracts the mean and divides by the standard deviation using only NumPy arithmetic operations. Test it and verify the result has mean approximately 0 and std approximately 1.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np

    def normalize(arr):
        return (arr - np.mean(arr)) / np.std(arr)

    data = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
    result = normalize(data)
    print(f"Mean: {np.mean(result):.10f}")  # ~0
    print(f"Std:  {np.std(result):.10f}")   # ~1
    ```
