# In-Place Operations

In-place operations modify arrays without creating new memory allocations.

!!! tip "Mental Model"
    `a += b` modifies `a` in place, reusing its memory, while `a = a + b` allocates a new array and rebinds the name. In-place operations cut memory usage in half for large arrays and improve cache performance. The trade-off is that views sharing the same buffer see the changes immediately, which can cause bugs if you are not careful.


## Core Concept

In-place operations reduce memory footprint and improve cache efficiency.

### 1. Standard Operation

```python
import numpy as np

arr = np.array([1, 2, 3, 4])
arr = arr * 2  # Creates new array, rebinds name
```

### 2. In-Place Operation

```python
import numpy as np

arr = np.array([1, 2, 3, 4])
arr *= 2  # Modifies array in place
```

### 3. Memory Difference

Standard creates temporary; in-place modifies existing memory.


## Augmented Assignment

Python's augmented assignment operators perform in-place operations.

### 1. Arithmetic In-Place

```python
import numpy as np

arr = np.array([1, 2, 3, 4], dtype=float)

arr += 10    # Add
arr -= 5     # Subtract
arr *= 2     # Multiply
arr /= 4     # Divide
arr **= 2    # Power
arr //= 3    # Floor divide
arr %= 2     # Modulo

print(arr)
```

### 2. Bitwise In-Place

```python
import numpy as np

arr = np.array([1, 2, 3, 4], dtype=int)

arr &= 3     # AND
arr |= 8     # OR
arr ^= 1     # XOR
```


## Memory Verification

Verify that in-place operations don't create new arrays.

### 1. id() Check

```python
import numpy as np

def main():
    arr = np.array([1, 2, 3, 4])
    original_id = id(arr)
    
    arr *= 2
    
    print(f"ID unchanged: {id(arr) == original_id}")

if __name__ == "__main__":
    main()
```

Output:

```
ID unchanged: True
```

### 2. Standard Creates New

```python
import numpy as np

def main():
    arr = np.array([1, 2, 3, 4])
    original_id = id(arr)
    
    arr = arr * 2
    
    print(f"ID unchanged: {id(arr) == original_id}")

if __name__ == "__main__":
    main()
```

Output:

```
ID unchanged: False
```


## out Parameter

Many NumPy functions support an `out` parameter for in-place results.

### 1. Using out

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4])
    result = np.empty_like(a)
    
    np.multiply(a, 2, out=result)
    print(result)

if __name__ == "__main__":
    main()
```

### 2. Same Array out

```python
import numpy as np

def main():
    arr = np.array([1, 2, 3, 4])
    np.multiply(arr, 2, out=arr)
    print(arr)

if __name__ == "__main__":
    main()
```

Output:

```
[2 4 6 8]
```

### 3. Chained Operations

```python
import numpy as np

def main():
    arr = np.array([1.0, 2.0, 3.0, 4.0])
    np.sqrt(arr, out=arr)
    np.multiply(arr, 10, out=arr)
    print(arr)

if __name__ == "__main__":
    main()
```


## Performance Benefit

In-place operations improve performance for large arrays.

### 1. Timing Comparison

```python
import numpy as np
import time

def main():
    n = 10_000_000
    
    # Standard operation
    arr1 = np.random.randn(n)
    start = time.perf_counter()
    arr1 = arr1 * 2
    standard_time = time.perf_counter() - start
    
    # In-place operation
    arr2 = np.random.randn(n)
    start = time.perf_counter()
    arr2 *= 2
    inplace_time = time.perf_counter() - start
    
    print(f"Standard time: {standard_time:.4f} sec")
    print(f"In-place time: {inplace_time:.4f} sec")

if __name__ == "__main__":
    main()
```

### 2. Cache Efficiency

In-place avoids cache eviction from temporary allocations.


## Caveats

Be aware of in-place operation limitations.

### 1. View Side Effects

```python
import numpy as np

arr = np.array([1, 2, 3, 4])
view = arr[1:3]
view *= 10
print(arr)  # [1 20 30 4]
```

### 2. dtype Constraints

In-place operations cannot change dtype.

### 3. Broadcasting Limit

In-place requires compatible shapes without expansion.

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
