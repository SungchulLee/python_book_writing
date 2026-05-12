# UFuncs and Vectorization

!!! tip "Mental Model"
    A ufunc is a C-compiled function that operates element-by-element on arrays with automatic broadcasting, type casting, and output allocation. Every arithmetic operator (`+`, `*`, `**`) and math function (`np.sin`, `np.exp`) in NumPy is a ufunc. Understanding ufuncs means understanding why NumPy code runs at near-C speed without explicit loops.

    The one-line abstraction: **ufunc = elementwise operator on arrays**. It takes
    one or more arrays, applies a scalar operation to each corresponding element
    (in compiled C, not Python), and returns a new array. Broadcasting extends this
    to arrays of different shapes by aligning dimensions automatically.

## Universal Functions

### 1. Definition

UFuncs are vectorized wrappers around C-implemented operations:

```python
import numpy as np

x = np.array([0, np.pi/2, np.pi])
y = np.sin(x)  # UFuncs operates element-wise
print(y)  # [0. 1. 0.]
```

**Characteristics:**

- Implemented in C for speed
- Operate element-wise
- Support broadcasting
- Type-flexible with automatic promotion

### 2. Performance

```python
import time

# Python loop (slow)
x_list = [i * 0.001 for i in range(1000000)]
start = time.time()
y_list = [np.sin(xi) for xi in x_list]
print(f"List: {time.time() - start:.3f}s")

# NumPy ufunc (fast)
x_array = np.linspace(0, 1000, 1000000)
start = time.time()
y_array = np.sin(x_array)
print(f"UFuncs: {time.time() - start:.3f}s")
```

UFuncs are typically **100x faster** than Python loops.

### 3. Type Detection

```python
print(isinstance(np.sin, np.ufunc))  # True
print(isinstance(np.add, np.ufunc))  # True
```

## Common UFuncs

### 1. Arithmetic

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.add(a, b))       # [5 7 9]
print(np.subtract(a, b))  # [-3 -3 -3]
print(np.multiply(a, b))  # [4 10 18]
print(np.divide(a, b))    # [0.25 0.4 0.5]
print(np.power(a, 2))     # [1 4 9]
```

### 2. Trigonometric

```python
x = np.array([0, np.pi/4, np.pi/2])

print(np.sin(x))      # [0. 0.707 1.]
print(np.cos(x))      # [1. 0.707 0.]
print(np.tan(x))      # [0. 1. inf]
print(np.arctan2(1, 1))  # 0.785 (π/4)
```

### 3. Exponential and Logarithmic

```python
x = np.array([1, 2, 3])

print(np.exp(x))      # [2.718 7.389 20.086]
print(np.log(x))      # [0. 0.693 1.099]
print(np.log10(x))    # [0. 0.301 0.477]
print(np.sqrt(x))     # [1. 1.414 1.732]
```

## Broadcasting with UFuncs

### 1. Scalar and Array

```python
arr = np.array([1, 2, 3])
result = arr + 10  # Broadcasts scalar
print(result)  # [11 12 13]
```

### 2. Array and Array

```python
arr1 = np.array([[1], [2], [3]])  # (3, 1)
arr2 = np.array([10, 20, 30])     # (3,)
result = arr1 + arr2              # (3, 3)
# [[11 21 31]
#  [12 22 32]
#  [13 23 33]]
```

### 3. Multi-dimensional

```python
a = np.ones((3, 1, 4))
b = np.ones((1, 2, 4))
c = a + b  # Broadcasts to (3, 2, 4)
print(c.shape)  # (3, 2, 4)
```

## Advanced UFuncs Features

### 1. Output Arrays

```python
x = np.array([1.0, 2.0, 3.0])
out = np.empty_like(x)
np.sin(x, out=out)  # Writes result to out, avoids allocation
print(out)
```

### 2. Reduction Methods

```python
arr = np.array([1, 2, 3, 4, 5])

# UFuncs have reduce methods
print(np.add.reduce(arr))      # 15 (sum)
print(np.multiply.reduce(arr)) # 120 (product)
```

### 3. Accumulate

```python
arr = np.array([1, 2, 3, 4, 5])
print(np.add.accumulate(arr))  # [1 3 6 10 15] (cumulative sum)
```

## Comparison UFuncs

### 1. Element-wise Comparison

```python
a = np.array([1, 2, 3])
b = np.array([1, 3, 2])

print(np.greater(a, b))      # [False False True]
print(np.less_equal(a, b))   # [True True False]
print(np.equal(a, b))        # [True False False]
print(np.not_equal(a, b))    # [False True True]
```

### 2. Maximum and Minimum

```python
a = np.array([1, 5, 3])
b = np.array([4, 2, 6])

print(np.maximum(a, b))  # [4 5 6] element-wise max
print(np.minimum(a, b))  # [1 2 3] element-wise min
```

### 3. Logical Operations

```python
a = np.array([True, False, True])
b = np.array([True, True, False])

print(np.logical_and(a, b))  # [True False False]
print(np.logical_or(a, b))   # [True True True]
print(np.logical_not(a))     # [False True False]
```

## Custom UFuncs

### 1. Using frompyfunc

```python
def custom_func(x, y):
    return x**2 + y**2

ufunc = np.frompyfunc(custom_func, 2, 1)  # 2 inputs, 1 output

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
result = ufunc(a, b)
print(result)  # [17 29 45]
```

### 2. Numba Vectorize

```python
from numba import vectorize

@vectorize
def fast_func(x, y):
    return x**2 + y**2

result = fast_func(np.array([1, 2, 3]), np.array([4, 5, 6]))
```

### 3. Performance Comparison

Custom UFuncs via Numba can match C-level performance while being pure Python.

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
