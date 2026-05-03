# Element-wise Min Max

!!! tip "Mental Model"
    `np.minimum` and `np.maximum` compare two arrays position by position and return the smaller or larger value at each slot. Unlike `np.min`/`np.max` which reduce an array to a single value, these are element-wise ufuncs that produce an output the same shape as the inputs — perfect for clamping values or building piecewise functions.

    **Deeper insight:** these functions are **vectorized conditionals** — each element independently picks one of two values based on a comparison. This makes them the building blocks for **piecewise function construction**: ReLU (`np.maximum(x, 0)`), clipping (`np.clip` = minimum + maximum), and any function defined differently in different regions.

## np.minimum

### 1. Basic Usage

`np.minimum` compares two arrays element-wise and returns the smaller value at each position.

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 7])
    b = np.array([2, 3, 4, 6])
    
    c = np.minimum(a, b)
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"np.minimum(a, b) = {c}")

if __name__ == "__main__":
    main()
```

**Output:**

```
a = [1 5 3 7]
b = [2 3 4 6]
np.minimum(a, b) = [1 3 3 6]
```

### 2. With Scalar

Broadcasting allows comparing with a scalar.

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 7, 2])
    threshold = 4
    
    c = np.minimum(a, threshold)
    
    print(f"a = {a}")
    print(f"threshold = {threshold}")
    print(f"np.minimum(a, threshold) = {c}")

if __name__ == "__main__":
    main()
```

**Output:**

```
a = [1 5 3 7 2]
threshold = 4
np.minimum(a, threshold) = [1 4 3 4 2]
```

### 3. Clamp Upper Bound

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    a = np.linspace(-2, 2, 11)
    b = np.zeros_like(a)
    c = np.minimum(a, b)
    
    fig, ax = plt.subplots(figsize=(6.5, 4))
    
    ax.plot(a, c, 'b-', linewidth=2)
    
    ax.spines['left'].set_position("zero")
    ax.spines['bottom'].set_position("zero")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    ax.set_xticks((-2, -1, 0, 1, 2))
    ax.set_yticks((0, -1, -2))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 0.1)
    ax.set_title('np.minimum(x, 0)')
    
    plt.show()

if __name__ == "__main__":
    main()
```

## np.maximum

### 1. Basic Usage

`np.maximum` compares two arrays element-wise and returns the larger value at each position.

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 7])
    b = np.array([2, 3, 4, 6])
    
    c = np.maximum(a, b)
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"np.maximum(a, b) = {c}")

if __name__ == "__main__":
    main()
```

**Output:**

```
a = [1 5 3 7]
b = [2 3 4 6]
np.maximum(a, b) = [2 5 4 7]
```

### 2. With Scalar

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 7, 2])
    threshold = 4
    
    c = np.maximum(a, threshold)
    
    print(f"a = {a}")
    print(f"threshold = {threshold}")
    print(f"np.maximum(a, threshold) = {c}")

if __name__ == "__main__":
    main()
```

**Output:**

```
a = [1 5 3 7 2]
threshold = 4
np.maximum(a, threshold) = [4 5 4 7 4]
```

### 3. ReLU Activation

The ReLU (Rectified Linear Unit) function is `max(0, x)`.

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    a = np.linspace(-2, 2, 11)
    b = np.zeros_like(a)
    c = np.maximum(a, b)
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    ax.plot(a, c, label='ReLU')
    ax.legend(fontsize=15)
    
    ax.spines['left'].set_position("zero")
    ax.spines['bottom'].set_position("zero")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    ax.set_xticks((-2, -1, 0, 1, 2))
    ax.set_yticks((0, 1, 2))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-0.1, 2)
    
    plt.show()

if __name__ == "__main__":
    main()
```

## Broadcasting

### 1. Scalar Broadcast

Both `np.minimum` and `np.maximum` support broadcasting with scalars.

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    # ReLU with broadcasting (no zeros_like needed)
    a = np.linspace(-2, 2, 11)
    c = np.maximum(a, 0)  # scalar broadcasts
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    ax.plot(a, c, label='ReLU')
    ax.legend(fontsize=15)
    
    ax.spines['left'].set_position("zero")
    ax.spines['bottom'].set_position("zero")
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    ax.set_xticks((-2, -1, 0, 1, 2))
    ax.set_yticks((0, 1, 2))
    ax.set_xlim(-2, 2)
    ax.set_ylim(-0.1, 2)
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Array Broadcast

```python
import numpy as np

def main():
    # 2D array vs 1D array
    a = np.array([[1, 5, 3],
                  [4, 2, 6]])
    
    b = np.array([2, 3, 4])  # broadcasts to each row
    
    print("a =")
    print(a)
    print()
    print(f"b = {b}")
    print()
    print("np.maximum(a, b) =")
    print(np.maximum(a, b))

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[1 5 3]
 [4 2 6]]

b = [2 3 4]

np.maximum(a, b) =
[[2 5 4]
 [4 3 6]]
```

### 3. Different Shapes

```python
import numpy as np

def main():
    # Column vector vs row vector
    a = np.array([[1], [2], [3]])  # (3, 1)
    b = np.array([10, 20])         # (2,)
    
    print(f"a.shape = {a.shape}")
    print(f"b.shape = {b.shape}")
    print()
    
    result = np.maximum(a, b)
    print(f"np.maximum(a, b).shape = {result.shape}")
    print(result)

if __name__ == "__main__":
    main()
```

## min vs minimum

### 1. Key Difference

- `np.min` / `a.min()`: Reduction (finds minimum in array)
- `np.minimum`: Element-wise comparison of two arrays

```python
import numpy as np

def main():
    a = np.array([1, 5, 3])
    b = np.array([2, 3, 4])
    
    print("Reduction (single array):")
    print(f"  np.min(a) = {np.min(a)}")
    print(f"  a.min() = {a.min()}")
    print()
    
    print("Element-wise (two arrays):")
    print(f"  np.minimum(a, b) = {np.minimum(a, b)}")

if __name__ == "__main__":
    main()
```

### 2. Similar Pattern

```python
import numpy as np

def main():
    a = np.array([1, 5, 3])
    b = np.array([2, 3, 4])
    
    print("Reduction functions:")
    print(f"  np.min(a) = {np.min(a)}")
    print(f"  np.max(a) = {np.max(a)}")
    print()
    
    print("Element-wise functions:")
    print(f"  np.minimum(a, b) = {np.minimum(a, b)}")
    print(f"  np.maximum(a, b) = {np.maximum(a, b)}")

if __name__ == "__main__":
    main()
```

### 3. Use Case Summary

```python
import numpy as np

def main():
    """
    Use np.min/np.max when:
    - Finding the smallest/largest value in one array
    - Reducing along an axis
    
    Use np.minimum/np.maximum when:
    - Comparing two arrays element by element
    - Clamping values (with scalar broadcast)
    - Implementing functions like ReLU
    """
    
    data = np.array([[-1, 2], [3, -4]])
    
    # Find global minimum
    print(f"Global min: {np.min(data)}")
    
    # Clamp negative values to 0
    print(f"ReLU result:\n{np.maximum(data, 0)}")

if __name__ == "__main__":
    main()
```

## Practical Examples

### 1. Clip Values

```python
import numpy as np

def main():
    data = np.array([0.1, 0.5, 1.2, -0.3, 0.8])
    
    # Clip to [0, 1] range
    clipped = np.minimum(np.maximum(data, 0), 1)
    
    print(f"Original: {data}")
    print(f"Clipped:  {clipped}")
    
    # Equivalent using np.clip
    clipped2 = np.clip(data, 0, 1)
    print(f"np.clip:  {clipped2}")

if __name__ == "__main__":
    main()
```

### 2. Leaky ReLU

```python
import numpy as np
import matplotlib.pyplot as plt

def leaky_relu(x, alpha=0.1):
    return np.maximum(x, alpha * x)

def main():
    x = np.linspace(-2, 2, 100)
    y = leaky_relu(x, alpha=0.1)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    ax.plot(x, y, label='Leaky ReLU (α=0.1)')
    ax.plot(x, np.maximum(x, 0), '--', label='ReLU')
    ax.legend()
    
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Leaky ReLU vs ReLU')
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Soft Maximum

```python
import numpy as np

def main():
    # Element-wise max of multiple arrays
    a = np.array([1, 4, 2])
    b = np.array([3, 2, 5])
    c = np.array([2, 3, 1])
    
    # Chain maximum calls
    result = np.maximum(np.maximum(a, b), c)
    
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"c = {c}")
    print(f"Element-wise max = {result}")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Given `a = np.array([1, 5, 3, 8, 2])` and `b = np.array([3, 2, 7, 4, 6])`, compute the element-wise minimum and maximum using `np.minimum` and `np.maximum`. Verify the results manually.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([1, 5, 3, 8, 2])
        b = np.array([3, 2, 7, 4, 6])
        print(f"min: {np.minimum(a, b)}")  # [1 2 3 4 2]
        print(f"max: {np.maximum(a, b)}")  # [3 5 7 8 6]

---

**Exercise 2.**
Use `np.clip` (which combines minimum and maximum) to clamp all values in `a = np.array([-5, 3, 12, -1, 7, 20])` to the range `[0, 10]`. Implement the same operation using `np.maximum(np.minimum(a, 10), 0)`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([-5, 3, 12, -1, 7, 20])
        clipped = np.clip(a, 0, 10)
        manual = np.maximum(np.minimum(a, 10), 0)
        print(f"Clipped: {clipped}")
        print(f"Manual:  {manual}")
        print(f"Match: {np.array_equal(clipped, manual)}")

---

**Exercise 3.**
Given a 2D array of random values, use `np.minimum` with broadcasting to clamp each column to a different maximum value. Specifically, clamp columns of a `(5, 3)` array to max values `[1.0, 2.0, 3.0]`.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.random.randn(5, 3) * 5
        max_vals = np.array([1.0, 2.0, 3.0])
        result = np.minimum(a, max_vals)  # broadcasts (5,3) with (3,)
        print(f"Max per column: {result.max(axis=0)}")

---

**Exercise 4.**
Implement a ReLU function `relu(x)` and a Leaky ReLU `leaky_relu(x, alpha=0.01)` using only `np.maximum`. Apply both to `x = np.linspace(-3, 3, 7)` and print the results. Explain why these are piecewise functions.

??? success "Solution to Exercise 4"

        import numpy as np

        def relu(x):
            return np.maximum(x, 0)

        def leaky_relu(x, alpha=0.01):
            return np.maximum(x, alpha * x)

        x = np.linspace(-3, 3, 7)
        print(f"x:          {x}")
        print(f"ReLU:       {relu(x)}")
        print(f"Leaky ReLU: {leaky_relu(x)}")

        # These are piecewise because:
        # ReLU(x) = x if x > 0, else 0       (two pieces)
        # Leaky(x) = x if x > 0, else 0.01*x (two pieces)
        # np.maximum selects the larger of two values at each point,
        # effectively choosing which "piece" of the function to use.

---

**Exercise 5.**
Use `np.clip` (which combines `np.minimum` and `np.maximum`) to normalize pixel values in an image array from arbitrary range to `[0, 255]`. Given `pixels = np.random.randn(100, 100) * 100 + 128`, clip to `[0, 255]` and convert to `uint8`. Verify no values are outside the range.

??? success "Solution to Exercise 5"

        import numpy as np

        pixels = np.random.randn(100, 100) * 100 + 128
        clipped = np.clip(pixels, 0, 255).astype(np.uint8)
        print(f"Min: {clipped.min()}, Max: {clipped.max()}")
        print(f"All in [0, 255]: {clipped.min() >= 0 and clipped.max() <= 255}")
        print(f"Dtype: {clipped.dtype}")  # uint8
