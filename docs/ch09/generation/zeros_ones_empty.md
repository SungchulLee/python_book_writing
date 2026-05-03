# Zeros, Ones, Empty

NumPy provides efficient functions for creating arrays initialized with specific values or uninitialized memory.

!!! tip "Mental Model"
    `zeros` and `ones` give you a clean slate filled with a known value; `empty` skips initialization entirely for speed, leaving whatever garbage was in memory. Use `zeros`/`ones` when correctness matters and `empty` only when you are certain every element will be overwritten before it is read.

!!! note "Common Use Patterns"
    Each function has a natural role:

    - `zeros` — accumulators, result buffers, zero-initialized state (e.g., confusion matrices, gradient accumulators in ML)
    - `ones` — scaling factors, masks, initial weights, bias terms
    - `empty` — performance-critical inner loops where every element will be written before it is read (e.g., simulation buffers)

    If in doubt, use `zeros`. The initialization cost is negligible for most workloads, and uninitialized memory from `empty` is a common source of silent bugs.


## np.zeros Function

Creates an array filled entirely with zeros.

### 1. Basic Usage

```python
import numpy as np

def main():
    a = np.zeros((1, 2, 3))
    print(a)
    print(f'shape: {a.shape}')
    print(f'dtype: {a.dtype}')

if __name__ == "__main__":
    main()
```

Output:

```
[[[0. 0. 0.]
  [0. 0. 0.]]]
shape: (1, 2, 3)
dtype: float64
```

### 2. Default dtype

The default dtype is `float64`. Specify `dtype=np.int64` for integers.


## np.ones Function

Creates an array filled entirely with ones.

### 1. Basic Usage

```python
import numpy as np

def main():
    a = np.ones((1, 2, 3))
    print(a)
    print(f'shape: {a.shape}')
    print(f'dtype: {a.dtype}')

if __name__ == "__main__":
    main()
```

Output:

```
[[[1. 1. 1.]
  [1. 1. 1.]]]
shape: (1, 2, 3)
dtype: float64
```

### 2. Scaling Pattern

Multiply `np.ones` by a constant to create uniform arrays of any value.


## np.empty Function

Allocates memory without initialization for maximum speed.

### 1. Basic Usage

```python
import numpy as np

def main():
    a = np.empty((1, 2, 3))
    print(a)
    print(f'shape: {a.shape}')
    print(f'dtype: {a.dtype}')

if __name__ == "__main__":
    main()
```

### 2. Caution Required

The values are arbitrary memory contents. Always fill before reading.


## Like Variants

Create arrays matching another array's shape and dtype.

### 1. np.zeros_like

```python
import numpy as np

def main():
    x = np.zeros((1, 2, 3))
    
    a = np.zeros_like(x)
    print(f'shape: {a.shape}')
    print(f'dtype: {a.dtype}')

if __name__ == "__main__":
    main()
```

### 2. np.ones_like

```python
import numpy as np

def main():
    x = np.zeros((1, 2, 3))
    
    a = np.ones_like(x)
    print(f'shape: {a.shape}')
    print(f'dtype: {a.dtype}')

if __name__ == "__main__":
    main()
```

### 3. np.empty_like

```python
import numpy as np

def main():
    x = np.zeros((1, 2, 3))
    
    a = np.empty_like(x)
    print(f'shape: {a.shape}')
    print(f'dtype: {a.dtype}')

if __name__ == "__main__":
    main()
```


## Practical Example

Zero-one encoding for detecting repetitive digits in an integer.

### 1. Problem Statement

Check whether a given integer contains any digit more than once.

### 2. Algorithm Design

```python
import numpy as np

def check_repetitive_digits(n):
    seen = np.zeros(10, dtype=np.uint8)
    quotient = n
    while quotient > 0:
        quotient, remainder = quotient // 10, quotient % 10
        if seen[remainder] == 1:
            print(f"{remainder} appears more than once in {n}.")
            break
        else:
            seen[remainder] += 1
    else:
        print(f"{n} has no repetitive digits.")
```

### 3. Example Output

```python
>>> check_repetitive_digits(67827)
7 appears more than once in 67827.

>>> check_repetitive_digits(12345)
12345 has no repetitive digits.
```


## When to Use Each

Choose the right function based on your initialization needs.

### 1. Use np.zeros

When you need guaranteed zero initialization, such as accumulators or counters.

### 2. Use np.ones

When building arrays that will be scaled or used as multiplicative identities.

### 3. Use np.empty

When you will immediately overwrite all values and need maximum allocation speed.

---

## Exercises

**Exercise 1.**
Create a 3x4 array of zeros with `dtype=int`, then a 3x4 array of ones with `dtype=float64`. Add them together and print the resulting dtype (should be `float64` due to type promotion).

??? success "Solution to Exercise 1"

        import numpy as np

        z = np.zeros((3, 4), dtype=int)
        o = np.ones((3, 4), dtype=np.float64)
        result = z + o
        print(f"Result dtype: {result.dtype}")  # float64

---

**Exercise 2.**
Given `x = np.array([1.5, 2.5, 3.5])`, use `np.zeros_like` and `np.ones_like` to create arrays that match `x`'s shape and dtype. Verify that the dtype of both matches `x.dtype`.

??? success "Solution to Exercise 2"

        import numpy as np

        x = np.array([1.5, 2.5, 3.5])
        z = np.zeros_like(x)
        o = np.ones_like(x)
        print(f"x dtype: {x.dtype}")
        print(f"zeros_like dtype: {z.dtype}")
        print(f"ones_like dtype: {o.dtype}")
        print(f"All match: {z.dtype == x.dtype == o.dtype}")

---

**Exercise 3.**
Create a `(1000, 1000)` array using `np.empty` and then fill it with the value 7.0 using slice assignment (`a[:] = 7.0`). Verify that every element equals 7.0. Explain why using `np.empty` followed by a fill can be faster than `np.full` for very large arrays.

??? success "Solution to Exercise 3"

        import numpy as np
        import time

        a = np.empty((1000, 1000))
        a[:] = 7.0
        print(f"All 7.0: {np.all(a == 7.0)}")

        # np.empty does not initialize memory, so the allocation
        # step is faster. The subsequent fill writes once.
        # np.full also allocates and fills, but in some cases
        # the two-step approach can be faster when combined
        # with other initialization logic.
