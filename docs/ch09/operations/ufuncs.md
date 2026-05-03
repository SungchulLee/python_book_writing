# Universal Functions

Universal functions (ufuncs) operate element-wise on arrays with broadcasting support.

!!! tip "Mental Model"
    Ufuncs are the engine behind NumPy's speed: each one is a compiled C loop that takes array inputs, applies a scalar operation element-by-element, and handles broadcasting, type promotion, and output allocation automatically. When you write `a + b` on arrays, Python dispatches to `np.add`, which is a ufunc -- no Python loop ever runs.

    The key elevation: **ufuncs are the abstraction layer for ALL array computation.**
    Arithmetic, comparisons, math functions, and rounding are all ufuncs. Their
    methods unify many seemingly different operations:

    | Concept | UFunc expression |
    |---------|-----------------|
    | `np.sum(a)` | `np.add.reduce(a)` |
    | `np.cumsum(a)` | `np.add.accumulate(a)` |
    | Outer product | `np.multiply.outer(a, b)` |
    | In-place update | `np.add.at(a, idx, val)` |

## What are Ufuncs

### 1. Definition

A ufunc operates on ndarrays element-by-element, supporting broadcasting and type casting.

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # np.add is a ufunc
    c = np.add(a, b)
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"np.add(a, b) = {c}")
    print(f"Type: {type(np.add)}")

if __name__ == "__main__":
    main()
```

### 2. Without Ufuncs

```python
import numpy as np

def main():
    a = [1, 2, 3]
    b = [4, 5, 6]
    
    # Without ufuncs: manual loop
    c = []
    for i, j in zip(a, b):
        c.append(i + j)
    
    print(f"Result: {c}")

if __name__ == "__main__":
    main()
```

### 3. With Ufuncs

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    # With ufuncs: single expression
    c = a + b
    
    print(f"Result: {c}")

if __name__ == "__main__":
    main()
```

## Built-in Ufuncs

### 1. Math Ufuncs

```python
import numpy as np

def main():
    x = np.array([1, 4, 9, 16])
    
    print(f"x = {x}")
    print(f"np.sqrt(x) = {np.sqrt(x)}")
    print(f"np.square(x) = {np.square(x)}")
    print(f"np.abs(x) = {np.abs(x)}")

if __name__ == "__main__":
    main()
```

### 2. Trigonometric Ufuncs

```python
import numpy as np

def main():
    x = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
    
    print(f"x (radians) = {x}")
    print(f"np.sin(x) = {np.sin(x).round(4)}")
    print(f"np.cos(x) = {np.cos(x).round(4)}")

if __name__ == "__main__":
    main()
```

### 3. Comparison Ufuncs

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([3, 2, 1])
    
    print(f"np.greater(a, b) = {np.greater(a, b)}")
    print(f"np.maximum(a, b) = {np.maximum(a, b)}")
    print(f"np.minimum(a, b) = {np.minimum(a, b)}")

if __name__ == "__main__":
    main()
```

## np.frompyfunc

### 1. Create Custom Ufunc

```python
import numpy as np

def main():
    # Python function
    def my_func(x):
        return x ** 2 + 1
    
    # Convert to ufunc
    my_ufunc = np.frompyfunc(my_func, 1, 1)
    
    a = np.array([1, 2, 3, 4])
    result = my_ufunc(a)
    
    print(f"a = {a}")
    print(f"my_ufunc(a) = {result}")
    print(f"Result dtype: {result.dtype}")

if __name__ == "__main__":
    main()
```

### 2. Signature

```python
import numpy as np

def main():
    # np.frompyfunc(func, nin, nout)
    # nin: number of input arguments
    # nout: number of output values
    
    # Example: function with 2 inputs, 1 output
    def combine(x, y):
        return x * 10 + y
    
    combine_ufunc = np.frompyfunc(combine, 2, 1)
    
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    
    result = combine_ufunc(a, b)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

### 3. String Conversion

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    
    # str() on array gives string representation of whole array
    print(f"str(a) = {str(a)}")
    
    # frompyfunc applies str to each element
    str_ufunc = np.frompyfunc(str, 1, 1)
    print(f"str_ufunc(a) = {str_ufunc(a)}")

if __name__ == "__main__":
    main()
```

## np.vectorize

### 1. Basic Usage

```python
import numpy as np

def main():
    def my_func(x):
        if x < 0:
            return 0
        elif x > 10:
            return 10
        else:
            return x
    
    # Vectorize the function
    vec_func = np.vectorize(my_func)
    
    a = np.array([-5, 3, 8, 15, 2])
    result = vec_func(a)
    
    print(f"a = {a}")
    print(f"vec_func(a) = {result}")

if __name__ == "__main__":
    main()
```

### 2. Specify Output Type

```python
import numpy as np

def main():
    def classify(x):
        if x < 0:
            return "negative"
        elif x == 0:
            return "zero"
        else:
            return "positive"
    
    vec_classify = np.vectorize(classify, otypes=[object])
    
    a = np.array([-2, 0, 3])
    result = vec_classify(a)
    
    print(f"a = {a}")
    print(f"Classification: {result}")

if __name__ == "__main__":
    main()
```

### 3. Excluded Arguments

```python
import numpy as np

def main():
    def power_with_offset(x, n, offset):
        return x ** n + offset
    
    # Exclude 'offset' from vectorization
    vec_func = np.vectorize(power_with_offset, excluded=['offset'])
    
    a = np.array([1, 2, 3, 4])
    result = vec_func(a, 2, offset=10)
    
    print(f"a = {a}")
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

## Performance Note

### 1. vectorize is Not Fast

```python
import numpy as np
import time

def main():
    def square(x):
        return x ** 2
    
    vec_square = np.vectorize(square)
    
    a = np.random.randn(1_000_000)
    
    # Vectorized (slow)
    start = time.perf_counter()
    result1 = vec_square(a)
    vec_time = time.perf_counter() - start
    
    # Native ufunc (fast)
    start = time.perf_counter()
    result2 = np.square(a)
    native_time = time.perf_counter() - start
    
    print(f"np.vectorize: {vec_time:.4f} sec")
    print(f"np.square:    {native_time:.6f} sec")
    print(f"Speedup:      {vec_time/native_time:.0f}x")

if __name__ == "__main__":
    main()
```

### 2. When to Use

- `np.vectorize`: Convenience, not performance
- Use native ufuncs when available
- For performance: use NumPy operations or Numba

### 3. Documentation Quote

> The `vectorize` function is provided primarily for convenience, not for performance. The implementation is essentially a for loop.

## Ufunc Attributes

### 1. nin and nout

```python
import numpy as np

def main():
    print(f"np.add.nin = {np.add.nin}")    # 2 inputs
    print(f"np.add.nout = {np.add.nout}")  # 1 output
    print()
    print(f"np.sqrt.nin = {np.sqrt.nin}")  # 1 input
    print(f"np.sqrt.nout = {np.sqrt.nout}")  # 1 output
    print()
    print(f"np.divmod.nin = {np.divmod.nin}")  # 2 inputs
    print(f"np.divmod.nout = {np.divmod.nout}")  # 2 outputs

if __name__ == "__main__":
    main()
```

### 2. ntypes

```python
import numpy as np

def main():
    print(f"np.add.ntypes = {np.add.ntypes}")
    print()
    print("Supported type signatures:")
    for sig in np.add.types[:5]:
        print(f"  {sig}")
    print("  ...")

if __name__ == "__main__":
    main()
```

## Ufunc Methods

### 1. reduce

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    
    # Reduce applies operation cumulatively
    result = np.add.reduce(a)  # Same as np.sum
    
    print(f"a = {a}")
    print(f"np.add.reduce(a) = {result}")
    print(f"np.sum(a) = {np.sum(a)}")

if __name__ == "__main__":
    main()
```

### 2. accumulate

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    
    # Accumulate keeps intermediate results
    result = np.add.accumulate(a)  # Same as np.cumsum
    
    print(f"a = {a}")
    print(f"np.add.accumulate(a) = {result}")
    print(f"np.cumsum(a) = {np.cumsum(a)}")

if __name__ == "__main__":
    main()
```

### 3. outer

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([10, 20])
    
    # Outer applies operation to all pairs
    result = np.multiply.outer(a, b)
    
    print(f"a = {a}")
    print(f"b = {b}")
    print("np.multiply.outer(a, b) =")
    print(result)

if __name__ == "__main__":
    main()
```

### 4. at

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    indices = np.array([0, 2, 2])  # Note: index 2 appears twice
    
    # Add 10 at specified indices (in-place)
    np.add.at(a, indices, 10)
    
    print(f"Result: {a}")
    # Index 2 was incremented twice!

if __name__ == "__main__":
    main()
```

## Common Ufuncs

### 1. Math Operations

| Ufunc | Description |
|:------|:------------|
| `np.add` | Addition |
| `np.subtract` | Subtraction |
| `np.multiply` | Multiplication |
| `np.divide` | Division |
| `np.power` | Power |
| `np.sqrt` | Square root |
| `np.abs` | Absolute value |

### 2. Trigonometric

| Ufunc | Description |
|:------|:------------|
| `np.sin` | Sine |
| `np.cos` | Cosine |
| `np.tan` | Tangent |
| `np.arcsin` | Inverse sine |
| `np.arctan2` | Two-argument arctangent |

### 3. Comparison

| Ufunc | Description |
|:------|:------------|
| `np.greater` | Greater than |
| `np.less` | Less than |
| `np.equal` | Equal |
| `np.maximum` | Element-wise maximum |
| `np.minimum` | Element-wise minimum |

---

## Exercises

**Exercise 1.** Use `np.add.reduce` to compute the sum of `[1, 2, 3, 4, 5]`. Compare with `np.sum`.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np

    arr = np.array([1, 2, 3, 4, 5])
    print(np.add.reduce(arr))  # 15
    print(np.sum(arr))         # 15
    ```

---

**Exercise 2.** Use `np.add.accumulate` to compute the cumulative sum of `[1, 2, 3, 4, 5]`. Compare with `np.cumsum`.

??? success "Solution to Exercise 2"
    ```python
    import numpy as np

    arr = np.array([1, 2, 3, 4, 5])
    print(np.add.accumulate(arr))  # [ 1  3  6 10 15]
    print(np.cumsum(arr))          # [ 1  3  6 10 15]
    ```

---

**Exercise 3.** Use `np.add.outer` to create an addition table for digits 1 through 5. Print the 5x5 result.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    digits = np.arange(1, 6)
    table = np.add.outer(digits, digits)
    print(table)
    ```

---

**Exercise 4.** Write a custom ufunc using `np.frompyfunc` that converts Celsius to Fahrenheit. Apply it to an array of temperatures.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np

    celsius_to_fahrenheit = np.frompyfunc(lambda c: c * 9/5 + 32, 1, 1)
    temps_c = np.array([0, 20, 37, 100])
    temps_f = celsius_to_fahrenheit(temps_c)
    print(temps_f)  # [32.0, 68.0, 98.6, 212.0]
    ```
