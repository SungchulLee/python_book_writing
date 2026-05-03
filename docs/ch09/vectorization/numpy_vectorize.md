# np.vectorize — Vectorizing Python Functions

`np.vectorize` converts a scalar function into a function that works element-wise on arrays. While convenient, it's **not** a performance optimization—it's primarily a convenience wrapper.

!!! tip "Mental Model"
    `np.vectorize` wraps a scalar Python function so it can accept array inputs, but under the hood it still calls your function once per element -- there is no C-level speedup. Use it for convenience (clean syntax, broadcasting support) when performance does not matter, but never as a substitute for true vectorization with NumPy ufuncs.

```python
import numpy as np
```

---

## Basic Usage

```python
# Scalar function (only works on single values)
def add_tax(price):
    if price > 100:
        return price * 1.1
    return price * 1.05

# This fails with arrays
prices = np.array([50, 100, 150])
# add_tax(prices)  # ValueError: truth value ambiguous

# Vectorize it
add_tax_vec = np.vectorize(add_tax)

# Now works with arrays
result = add_tax_vec(prices)
print(result)  # [52.5 105. 165.]
```

---

## Why vectorize Exists

`np.vectorize` is useful when:

1. You have an existing scalar function
2. The function has complex logic (if/else, loops)
3. You want array broadcasting behavior
4. Quick prototyping before optimization

```python
# Complex logic that's hard to vectorize manually
def categorize(value):
    if value < 0:
        return 'negative'
    elif value == 0:
        return 'zero'
    elif value < 10:
        return 'small'
    elif value < 100:
        return 'medium'
    else:
        return 'large'

categorize_vec = np.vectorize(categorize)
values = np.array([-5, 0, 5, 50, 500])
print(categorize_vec(values))
# ['negative' 'zero' 'small' 'medium' 'large']
```

---

## Important: Not a Performance Tool!

**`np.vectorize` does NOT make your code faster.** It simply loops over elements internally—there's no actual vectorization at the C level.

```python
import time

def slow_func(x):
    return x ** 2 + 2 * x + 1

slow_func_vec = np.vectorize(slow_func)

arr = np.arange(1_000_000)

# Vectorized function (NOT faster)
start = time.time()
result1 = slow_func_vec(arr)
print(f"np.vectorize: {time.time() - start:.3f}s")

# True NumPy vectorization (MUCH faster)
start = time.time()
result2 = arr ** 2 + 2 * arr + 1
print(f"True NumPy: {time.time() - start:.3f}s")

# np.vectorize: ~0.5s
# True NumPy: ~0.01s (50x faster!)
```

---

## Specifying Output Type

By default, `vectorize` infers the output type from the first element. Specify `otypes` to ensure correct type:

```python
# Without otypes: may guess wrong type
def to_string(x):
    return f"value: {x}"

vec_func = np.vectorize(to_string)
print(vec_func([1, 2, 3]).dtype)  # <U8 (may truncate!)

# With otypes: correct type
vec_func = np.vectorize(to_string, otypes=[object])
# or
vec_func = np.vectorize(to_string, otypes=['U50'])
```

### Common otypes

```python
# Numeric outputs
np.vectorize(func, otypes=[float])
np.vectorize(func, otypes=[int])
np.vectorize(func, otypes=[np.float64])

# String outputs
np.vectorize(func, otypes=['U100'])  # Unicode, max 100 chars
np.vectorize(func, otypes=[object])  # Python objects

# Multiple outputs
np.vectorize(func, otypes=[float, float])
```

---

## Multiple Inputs and Outputs

### Multiple Inputs

```python
def power_diff(base, exp1, exp2):
    return base ** exp1 - base ** exp2

power_diff_vec = np.vectorize(power_diff)

bases = np.array([2, 3, 4])
exp1 = np.array([2, 2, 2])
exp2 = np.array([1, 1, 1])

result = power_diff_vec(bases, exp1, exp2)
print(result)  # [2 6 12]
```

### Multiple Outputs

```python
def div_mod(a, b):
    return a // b, a % b

div_mod_vec = np.vectorize(div_mod)

a = np.array([10, 20, 30])
b = np.array([3, 7, 4])

quotients, remainders = div_mod_vec(a, b)
print(quotients)   # [3 2 7]
print(remainders)  # [1 6 2]
```

---

## Excluded Arguments

Exclude arguments from vectorization (passed as-is):

```python
def lookup(x, table):
    """Look up x in a dictionary."""
    return table.get(x, 'unknown')

# Without excluded: tries to iterate over table
lookup_vec = np.vectorize(lookup, excluded=['table'])

table = {1: 'one', 2: 'two', 3: 'three'}
values = np.array([1, 2, 3, 4])

result = lookup_vec(values, table)
print(result)  # ['one' 'two' 'three' 'unknown']
```

---

## Signature for Generalized ufuncs

For functions that operate on subarrays rather than scalars:

```python
# Function that takes a 1D array and returns a scalar
def array_sum(arr):
    return arr.sum()

# signature: input is (n,), output is scalar ()
array_sum_vec = np.vectorize(array_sum, signature='(n)->()')

# Apply to 2D array (operates on each row)
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

result = array_sum_vec(matrix)
print(result)  # [6 15 24]
```

### Signature Examples

```python
# Dot product of vectors
def dot(a, b):
    return np.sum(a * b)

dot_vec = np.vectorize(dot, signature='(n),(n)->()')

# Matrix-vector multiplication
def matvec(M, v):
    return M @ v

matvec_vec = np.vectorize(matvec, signature='(m,n),(n)->(m)')
```

---

## Decorator Syntax

```python
@np.vectorize
def celsius_to_fahrenheit(c):
    return c * 9/5 + 32

temps_c = np.array([0, 20, 37, 100])
temps_f = celsius_to_fahrenheit(temps_c)
print(temps_f)  # [32. 68. 98.6 212.]
```

With options:

```python
@np.vectorize(otypes=[float], excluded=['unit'])
def convert_temp(value, unit):
    if unit == 'C':
        return value * 9/5 + 32
    return value
```

---

## Better Alternatives

### Use np.where for Conditionals

```python
# Instead of vectorize with if/else
def categorize(x):
    if x > 0:
        return 'positive'
    return 'non-positive'

# Use np.where (much faster)
arr = np.array([-1, 0, 1, 2])
result = np.where(arr > 0, 'positive', 'non-positive')
```

### Use np.select for Multiple Conditions

```python
arr = np.array([-5, 0, 5, 50, 500])

conditions = [
    arr < 0,
    arr == 0,
    arr < 10,
    arr < 100,
]
choices = ['negative', 'zero', 'small', 'medium']
default = 'large'

result = np.select(conditions, choices, default)
# ['negative' 'zero' 'small' 'medium' 'large']
```

### Use np.piecewise for Numeric Results

```python
arr = np.array([-2, -1, 0, 1, 2], dtype=float)

result = np.piecewise(
    arr,
    [arr < 0, arr >= 0],
    [lambda x: x ** 2, lambda x: x ** 3]
)
print(result)  # [4. 1. 0. 1. 8.]
```

---

## When to Use vectorize

| Scenario | Use vectorize? | Better Alternative |
|----------|----------------|-------------------|
| Quick prototype | ✅ Yes | - |
| Complex string logic | ✅ Yes | - |
| External library calls | ✅ Yes | - |
| Simple math | ❌ No | NumPy operations |
| Conditionals | ❌ No | `np.where`, `np.select` |
| Performance critical | ❌ No | Numba, Cython |

---

## Summary

| Feature | Usage |
|---------|-------|
| Basic | `np.vectorize(func)` |
| Output type | `np.vectorize(func, otypes=[float])` |
| Exclude args | `np.vectorize(func, excluded=['param'])` |
| Subarray ops | `np.vectorize(func, signature='(n)->()')` |
| Decorator | `@np.vectorize` |

**Key Takeaways**:

- `np.vectorize` is a **convenience function**, not performance optimization
- It wraps a Python loop—not true vectorization
- Use `otypes` to specify output dtypes explicitly
- Use `excluded` for arguments that shouldn't be iterated
- Use `signature` for functions on subarrays
- Prefer `np.where`, `np.select`, or true NumPy operations for speed
- Good for prototyping and complex logic, not production performance

---

## Exercises

**Exercise 1.** Write a vectorized NumPy solution and a pure Python loop solution for the same computation. Measure and compare their performance using `time.perf_counter()`.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    data = np.random.default_rng(42).random(n)

    # Python loop
    start = time.perf_counter()
    result_py = [x ** 2 for x in data]
    py_time = time.perf_counter() - start

    # NumPy vectorized
    start = time.perf_counter()
    result_np = data ** 2
    np_time = time.perf_counter() - start

    print(f"Python: {py_time:.4f}s, NumPy: {np_time:.6f}s")
    print(f"Speedup: {py_time / np_time:.0f}x")
    ```

---

**Exercise 2.** Identify a potential performance pitfall in the following code and rewrite it using NumPy vectorization:

```python
result = []
for i in range(len(data)):
    result.append(data[i] ** 2 + 2 * data[i] + 1)
```

??? success "Solution to Exercise 2"
    ```python
    import numpy as np

    data = np.random.default_rng(42).random(100000)

    # Vectorized (fast)
    result = data ** 2 + 2 * data + 1
    ```

    The loop version creates Python objects for each element and calls `append` repeatedly. The vectorized version computes everything in compiled C code on contiguous memory.

---

**Exercise 3.** Explain why NumPy vectorized operations are faster than Python loops. Reference memory layout, type checking overhead, and SIMD instructions in your answer.

??? success "Solution to Exercise 3"
    NumPy vectorized operations are faster because:

    1. **Contiguous memory**: NumPy arrays store elements in a contiguous block, enabling efficient CPU cache usage.
    2. **No type checking**: Python loops check types at each iteration; NumPy knows the dtype in advance.
    3. **Compiled C loops**: The actual computation runs in compiled C/Fortran code, not interpreted Python.
    4. **SIMD instructions**: Modern CPUs can process multiple array elements simultaneously using SIMD (Single Instruction, Multiple Data).

---

**Exercise 4.** Apply the concepts from this page to a practical problem: given a large array of temperatures in Celsius, convert them all to Fahrenheit and find the maximum. Compare vectorized and loop approaches.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    rng = np.random.default_rng(42)
    celsius = rng.uniform(-40, 50, 1_000_000)

    # Vectorized
    start = time.perf_counter()
    fahrenheit = celsius * 9/5 + 32
    max_f = fahrenheit.max()
    vec_time = time.perf_counter() - start

    # Loop
    start = time.perf_counter()
    max_f_loop = max(c * 9/5 + 32 for c in celsius)
    loop_time = time.perf_counter() - start

    print(f"Vectorized: {vec_time:.6f}s, max={max_f:.1f}F")
    print(f"Loop: {loop_time:.4f}s, max={max_f_loop:.1f}F")
    ```
