# Comparison Operators

NumPy supports element-wise comparison operations that return boolean arrays.

!!! tip "Mental Model"
    Comparing two arrays with `<`, `>`, `==`, etc. produces a boolean array of the same shape, where each element records whether that position's comparison was True or False. These boolean arrays are the masks you feed into boolean indexing, `np.where`, and logical combinators (`&`, `|`, `~`).

    The deeper role: **comparison = data selection mechanism.** The boolean mask
    produced by a comparison is the bridge between "which elements satisfy a
    condition?" and "operate only on those elements" — the `mask → indexing →
    transformation` pipeline that underlies filtering, validation, and conditional
    assignment throughout NumPy.

## Basic Comparisons

### 1. Less Than

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 7, 2])
    
    result = a < 5
    
    print(f"a = {a}")
    print(f"a < 5 = {result}")

if __name__ == "__main__":
    main()
```

**Output:**

```
a = [1 5 3 7 2]
a < 5 = [ True False  True False  True]
```

### 2. Greater Than

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 7, 2])
    
    print(f"a = {a}")
    print(f"a > 3 = {a > 3}")
    print(f"a >= 3 = {a >= 3}")

if __name__ == "__main__":
    main()
```

### 3. Equality

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 5, 2])
    
    print(f"a = {a}")
    print(f"a == 5 = {a == 5}")
    print(f"a != 5 = {a != 5}")

if __name__ == "__main__":
    main()
```

## Array vs Array

### 1. Element-wise Comparison

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    b = np.array([5, 4, 3, 2, 1])
    
    print(f"a = {a}")
    print(f"b = {b}")
    print()
    print(f"a < b  = {a < b}")
    print(f"a == b = {a == b}")
    print(f"a > b  = {a > b}")

if __name__ == "__main__":
    main()
```

### 2. 2D Arrays

```python
import numpy as np

def main():
    a = np.array([[1, 2], [3, 4]])
    b = np.array([[2, 2], [2, 2]])
    
    print("a =")
    print(a)
    print()
    print("b =")
    print(b)
    print()
    print("a > b =")
    print(a > b)

if __name__ == "__main__":
    main()
```

## Function Equivalents

### 1. np.less and np.greater

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    
    print(f"a = {a}")
    print()
    print(f"np.less(a, 3) = {np.less(a, 3)}")
    print(f"np.greater(a, 3) = {np.greater(a, 3)}")
    print(f"np.less_equal(a, 3) = {np.less_equal(a, 3)}")
    print(f"np.greater_equal(a, 3) = {np.greater_equal(a, 3)}")

if __name__ == "__main__":
    main()
```

### 2. np.equal and np.not_equal

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 2, 1])
    
    print(f"a = {a}")
    print(f"np.equal(a, 2) = {np.equal(a, 2)}")
    print(f"np.not_equal(a, 2) = {np.not_equal(a, 2)}")

if __name__ == "__main__":
    main()
```

### 3. Using out Parameter

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    result = np.empty(5, dtype=bool)
    
    np.greater(a, 3, out=result)
    
    print(f"a = {a}")
    print(f"result = {result}")

if __name__ == "__main__":
    main()
```

## Floating Point Comparison

### 1. Exact Equality Issues

```python
import numpy as np

def main():
    a = 0.1 + 0.2
    b = 0.3
    
    print(f"0.1 + 0.2 = {a}")
    print(f"0.3 = {b}")
    print(f"0.1 + 0.2 == 0.3: {a == b}")  # False!

if __name__ == "__main__":
    main()
```

### 2. np.isclose

```python
import numpy as np

def main():
    a = np.array([0.1 + 0.2, 1.0, 2.0])
    b = np.array([0.3, 1.0, 2.0001])
    
    print(f"a = {a}")
    print(f"b = {b}")
    print()
    print(f"a == b: {a == b}")
    print(f"np.isclose(a, b): {np.isclose(a, b)}")

if __name__ == "__main__":
    main()
```

### 3. np.allclose

```python
import numpy as np

def main():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([1.0, 2.0, 3.0 + 1e-10])
    
    print(f"a = {a}")
    print(f"b = {b}")
    print()
    print(f"a == b (all): {np.all(a == b)}")
    print(f"np.allclose(a, b): {np.allclose(a, b)}")

if __name__ == "__main__":
    main()
```

## Tolerance Parameters

### 1. rtol and atol

```python
import numpy as np

def main():
    a = np.array([1.0, 100.0])
    b = np.array([1.001, 100.1])
    
    # Default: rtol=1e-5, atol=1e-8
    # |a - b| <= atol + rtol * |b|
    
    print(f"a = {a}")
    print(f"b = {b}")
    print()
    print(f"isclose (default): {np.isclose(a, b)}")
    print(f"isclose (rtol=0.01): {np.isclose(a, b, rtol=0.01)}")
    print(f"isclose (atol=0.1): {np.isclose(a, b, atol=0.1)}")

if __name__ == "__main__":
    main()
```

### 2. Practical Example

```python
import numpy as np

def main():
    # Verify matrix inverse
    A = np.array([[1, 2], [3, 4]], dtype=float)
    A_inv = np.linalg.inv(A)
    
    product = A @ A_inv
    identity = np.eye(2)
    
    print("A @ A_inv =")
    print(product)
    print()
    print(f"Exactly equal to I: {np.all(product == identity)}")
    print(f"Close to I: {np.allclose(product, identity)}")

if __name__ == "__main__":
    main()
```

## Combining Comparisons

### 1. Logical AND

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5, 6, 7])
    
    # Values between 3 and 6
    mask = (a >= 3) & (a <= 6)
    
    print(f"a = {a}")
    print(f"3 <= a <= 6: {mask}")
    print(f"Filtered: {a[mask]}")

if __name__ == "__main__":
    main()
```

### 2. Logical OR

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5, 6, 7])
    
    # Values less than 3 or greater than 5
    mask = (a < 3) | (a > 5)
    
    print(f"a = {a}")
    print(f"a < 3 or a > 5: {mask}")
    print(f"Filtered: {a[mask]}")

if __name__ == "__main__":
    main()
```

### 3. Logical NOT

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    
    mask = a > 3
    
    print(f"a = {a}")
    print(f"a > 3: {mask}")
    print(f"~(a > 3): {~mask}")

if __name__ == "__main__":
    main()
```

## Aggregation

### 1. np.any and np.all

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    
    print(f"a = {a}")
    print()
    print(f"Any element > 4: {np.any(a > 4)}")
    print(f"All elements > 0: {np.all(a > 0)}")
    print(f"All elements > 2: {np.all(a > 2)}")

if __name__ == "__main__":
    main()
```

### 2. Count True Values

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    
    mask = a > 5
    
    print(f"a = {a}")
    print(f"a > 5: {mask}")
    print(f"Count (sum): {np.sum(mask)}")
    print(f"Count (count_nonzero): {np.count_nonzero(mask)}")

if __name__ == "__main__":
    main()
```

### 3. With axis

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])
    
    print("a =")
    print(a)
    print()
    print(f"Any > 5 per column: {np.any(a > 5, axis=0)}")
    print(f"Any > 5 per row: {np.any(a > 5, axis=1)}")
    print(f"All > 0 per column: {np.all(a > 0, axis=0)}")

if __name__ == "__main__":
    main()
```

## np.array_equal

### 1. Array Equality

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([1, 2, 3])
    c = np.array([1, 2, 4])
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"c = {c}")
    print()
    print(f"np.array_equal(a, b): {np.array_equal(a, b)}")
    print(f"np.array_equal(a, c): {np.array_equal(a, c)}")

if __name__ == "__main__":
    main()
```

### 2. Different Shapes

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([[1, 2, 3]])
    
    print(f"a shape: {a.shape}")
    print(f"b shape: {b.shape}")
    print(f"np.array_equal(a, b): {np.array_equal(a, b)}")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Boolean Indexing

```python
import numpy as np

def main():
    scores = np.array([85, 62, 91, 45, 78, 55])
    
    passing = scores >= 60
    
    print(f"Scores: {scores}")
    print(f"Passing mask: {passing}")
    print(f"Passing scores: {scores[passing]}")
    print(f"Failing scores: {scores[~passing]}")

if __name__ == "__main__":
    main()
```

### 2. Conditional Assignment

```python
import numpy as np

def main():
    a = np.array([1, -2, 3, -4, 5])
    
    # Replace negatives with zero
    a[a < 0] = 0
    
    print(f"Result: {a}")

if __name__ == "__main__":
    main()
```

### 3. Data Validation

```python
import numpy as np

def main():
    data = np.array([1.0, 2.0, np.nan, 4.0, np.inf])
    
    valid = np.isfinite(data)
    
    print(f"Data: {data}")
    print(f"Is finite: {valid}")
    print(f"Valid data: {data[valid]}")

if __name__ == "__main__":
    main()
```

## Summary Table

### 1. Comparison Operators

| Operator | Function | Description |
|:---------|:---------|:------------|
| `<` | `np.less` | Less than |
| `<=` | `np.less_equal` | Less or equal |
| `>` | `np.greater` | Greater than |
| `>=` | `np.greater_equal` | Greater or equal |
| `==` | `np.equal` | Equal |
| `!=` | `np.not_equal` | Not equal |

### 2. Floating Point

| Function | Description |
|:---------|:------------|
| `np.isclose` | Element-wise approximate equality |
| `np.allclose` | All elements approximately equal |
| `np.array_equal` | Exact array equality |

### 3. Logical Operators

| Operator | Function | Description |
|:---------|:---------|:------------|
| `&` | `np.logical_and` | Element-wise AND |
| `\|` | `np.logical_or` | Element-wise OR |
| `~` | `np.logical_not` | Element-wise NOT |
| `^` | `np.logical_xor` | Element-wise XOR |

---

## Exercises

**Exercise 1.** Create an array of 10 random integers between 0 and 100. Use comparison operators to find which elements are greater than 50. Print both the boolean mask and the filtered values.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np

    rng = np.random.default_rng(42)
    arr = rng.integers(0, 101, size=10)
    mask = arr > 50
    print("Array:", arr)
    print("Mask:", mask)
    print("Filtered:", arr[mask])
    ```

---

**Exercise 2.** Predict the output:

```python
import numpy as np
a = np.array([1, 2, 3, 4, 5])
print(a[a > 3])
print(np.where(a > 3, a, -1))
```

??? success "Solution to Exercise 2"
    ```
    [4 5]
    [-1 -1 -1  4  5]
    ```

---

**Exercise 3.** Write a function `count_in_range(arr, lo, hi)` that counts how many elements satisfy `lo <= x <= hi` using NumPy comparison operators and `np.sum()`.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    def count_in_range(arr, lo, hi):
        return np.sum((arr >= lo) & (arr <= hi))

    data = np.array([5, 15, 25, 35, 45])
    print(count_in_range(data, 10, 30))  # 2
    ```

---

**Exercise 4.** Given an array, replace all negative values with 0 and all values greater than 100 with 100 (clamping). Use `np.clip` and also implement it manually with boolean indexing.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np

    arr = np.array([-10, 50, 120, 30, -5, 200])

    # Using np.clip
    print(np.clip(arr, 0, 100))  # [0 50 100 30 0 100]

    # Manual boolean indexing
    result = arr.copy()
    result[result < 0] = 0
    result[result > 100] = 100
    print(result)  # [0 50 100 30 0 100]
    ```
