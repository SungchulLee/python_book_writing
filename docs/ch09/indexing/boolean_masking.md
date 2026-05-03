# Boolean Masking

Boolean masking uses logical conditions to selectively operate on array subsets.

!!! tip "Mental Model"
    A boolean mask is an array of True/False values the same shape as your data. Using it as an index selects only the True elements, like a stencil laid over the array. This is the NumPy equivalent of a SQL `WHERE` clause -- filter, replace, or count elements that satisfy any condition, all without writing a loop.


## Filtering Basics

Boolean arrays select elements satisfying a condition.

### 1. 1D with List

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = [True, False, True]
    c = a[b]
    print(f"{c = }")

if __name__ == "__main__":
    main()
```

Output:

```
c = array([1, 3])
```

### 2. 1D with Array

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = np.array([True, False, True])
    c = a[b]
    print(f"{c = }")

if __name__ == "__main__":
    main()
```

Output:

```
c = array([1, 3])
```

### 3. Condition Filter

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    b = (a % 2 == 1)
    print(f"{b = }")
    print(f"{type(b) = }")

    c = a[b]
    print(f"{c = }")

if __name__ == "__main__":
    main()
```

Output:

```
b = array([ True, False,  True])
type(b) = <class 'numpy.ndarray'>
c = array([1, 3])
```


## 2D Filtering

Multi-dimensional arrays require NumPy boolean arrays.

### 1. List Causes Error

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = [[True, False, True], [False, True, False]]
    try:
        c = a[b]
        print(f"{c = }")
    except IndexError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

### 2. Array Works

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.array([[True, False, True], [False, True, False]])
    c = a[b]
    print(f"{c = }")

if __name__ == "__main__":
    main()
```

Output:

```
c = array([1, 3, 5])
```

### 3. 2D Condition

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = (a % 2 == 1)
    print(f"{b = }")

    c = a[b]
    print(f"{c = }")

if __name__ == "__main__":
    main()
```

Output:

```
b = array([[ True, False,  True],
           [False,  True, False]])
c = array([1, 3, 5])
```


## Mask Assignment

Boolean masks can modify array elements in-place.

### 1. 1D Assignment

```python
import numpy as np

def main():
    a = np.array([1, 2, 3])
    a[a % 2 == 1] = 0
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
[0 2 0]
```

### 2. 2D Assignment

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = np.array([[True, False, True], [False, True, False]])
    a[b] = 0
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
[[0 2 0]
 [4 0 6]]
```

### 3. Condition Assignment

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    a[a % 2 == 1] = 0
    print(a)

if __name__ == "__main__":
    main()
```

Output:

```
[[0 2 0]
 [4 0 6]]
```


## Image Masking

Apply masks to image regions.

### 1. Rectangle Mask

```python
import numpy as np
import matplotlib.pyplot as plt
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
    print(f"{img.shape = }")
    print(f"{img.dtype = }")

    mask = np.zeros(shape=img.shape[:2], dtype=bool)
    mask[50:100, 50:100] = True
    img_copy = img.copy()
    img_copy[mask] = [255, 255, 255, 255]

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(6, 4))

    ax0.set_title("Original", fontsize=15)
    ax0.imshow(img)

    ax1.set_title("Masked", fontsize=15)
    ax1.imshow(img_copy)

    for ax in (ax0, ax1):
        ax.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Mask Shape

Create mask matching image height and width: `img.shape[:2]`.


## Combining Masks

Logical operators combine multiple conditions.

### 1. AND Operator

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
mask1 = arr > 2
mask2 = arr < 5
combined = mask1 & mask2
print(arr[combined])  # [3 4]
```

### 2. OR Operator

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
combined = (arr < 2) | (arr > 4)
print(arr[combined])  # [1 5]
```

### 3. NOT Operator

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
mask = arr > 2
print(arr[~mask])  # [1 2]
```


## Coin Flip Simulation

Boolean masking enables vectorized probability simulation.

### 1. Inverse Transform

```python
import numpy as np

def main():
    n = 10
    p = 0.5

    c = np.zeros(n)
    u = np.random.rand(n)
    c[u > 1 - p] = 1

    for ui, ci in zip(u, c):
        print(f"{ui = :.3f}, {ui > 1-p = }, {ci = }")

if __name__ == "__main__":
    main()
```

### 2. Vectorized Flip

```python
import numpy as np

def main():
    n = 30
    p = 0.5

    uniform = np.random.uniform(size=(n,))
    coin = np.zeros_like(uniform)
    coin[uniform > 1 - p] = 1.
    print(coin)

if __name__ == "__main__":
    main()
```

### 3. Performance Benefit

Vectorized masking is faster than loop-based coin flips.


## np.where Indices

`np.where(condition)` returns indices where condition is True.

### 1. 1D Indices

```python
import numpy as np

def main():
    a = np.array([1, 2, 2, 3, 2, 4, 4, 2])
    b = np.where(a == 2)
    print(f"{b = }")

if __name__ == "__main__":
    main()
```

Output:

```
b = (array([1, 2, 4, 7]),)
```

### 2. 2D Indices

```python
import numpy as np

def main():
    a = np.array([[1, 2], [2, 3], [2, 4], [4, 2]])
    b = np.where(a == 2)
    print(f"{b = }")

if __name__ == "__main__":
    main()
```

Output:

```
b = (array([0, 1, 2, 3]), array([1, 0, 0, 1]))
```

### 3. 3D Indices

```python
import numpy as np

def main():
    a = np.array([[1, 2], [2, 3], [2, 4], [4, 2]])
    a = np.array([a, a])
    b = np.where(a == 2)
    print(f"{b = }")

if __name__ == "__main__":
    main()
```


## np.where Conditional

`np.where(condition, x, y)` selects from x or y based on condition.

### 1. Syntax Pattern

$$\begin{array}{ccccccc}
\text{c}&=&\text{np.where(}&\text{condition}&,&\text{if\_true}&,&\text{if\_false}&\text{)}
\end{array}$$

### 2. 1D Example

```python
import numpy as np

def main():
    a = np.array([1, 2, 2, 3, 2, 4, 4, 2])
    b = a * 10
    c = np.where(a == 2, a, b)
    print(f"{c = }")

if __name__ == "__main__":
    main()
```

Output:

```
c = array([10,  2,  2, 30,  2, 40, 40,  2])
```

### 3. 2D Example

```python
import numpy as np

def main():
    a = np.array([[1, 2], [2, 3], [2, 4], [4, 2]])
    b = a * 10
    c = np.where(a == 2, a, b)
    print(f"{c = }")

if __name__ == "__main__":
    main()
```

Output:

```
c = array([[10,  2],
           [ 2, 30],
           [ 2, 40],
           [40,  2]])
```


## Image Clamping

Use `np.where` to clamp pixel values to valid range.

### 1. Noise and Clamp

```python
import numpy as np
import matplotlib.pyplot as plt
import PIL
import urllib

def main():
    url = "https://upload.wikimedia.org/wikipedia/en/4/43/Pok%C3%A9mon_Mewtwo_art.png"
    img = np.array(PIL.Image.open(urllib.request.urlopen(url)))
    
    img_noisy = img + np.random.randint(-100, 101, size=img.shape)
    img_noisy = np.where(img_noisy >= 0, img_noisy, 0)
    img_noisy = np.where(img_noisy <= 255, img_noisy, 255)

    fig, ax = plt.subplots()
    ax.imshow(img_noisy.astype(np.uint8))
    ax.axis('off')
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Chained np.where

Apply multiple conditions sequentially to enforce bounds.

!!! warning "Boolean Masking Always Returns a Copy"

    Unlike slicing (which returns a view), boolean masking **always returns a copy**. Modifying the result does not modify the original array:

    ```python
    a = np.arange(10)
    result = a[a > 5]   # copy, not a view
    result[0] = 999
    print(a)  # unchanged
    ```

    To modify the original, use mask assignment directly: `a[a > 5] = 0`.

---

## Exercises

**Exercise 1.**
Create an array `a = np.arange(1, 21)`. Use boolean masking to extract all elements divisible by 3. Then use mask assignment to replace all elements greater than 15 with -1. Print the modified array.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(1, 21)
        divisible_by_3 = a[a % 3 == 0]
        print(f"Divisible by 3: {divisible_by_3}")

        a[a > 15] = -1
        print(f"After replacement: {a}")

---

**Exercise 2.**
Given a 2D array `M = np.random.randint(0, 100, size=(5, 5))`, create a combined mask that selects elements that are both greater than 25 AND less than 75. Count how many elements satisfy this condition using `np.sum` on the mask.

??? success "Solution to Exercise 2"

        import numpy as np

        np.random.seed(42)
        M = np.random.randint(0, 100, size=(5, 5))
        mask = (M > 25) & (M < 75)
        count = np.sum(mask)
        print(f"Elements in (25, 75): {count}")
        print(f"Values: {M[mask]}")

---

**Exercise 3.**
Simulate 1000 coin flips with probability `p = 0.7` using `np.random.rand` and boolean masking (set values where `rand < p` to 1, else 0). Print the empirical probability (mean of the result) and verify it is close to 0.7.

??? success "Solution to Exercise 3"

        import numpy as np

        np.random.seed(42)
        p = 0.7
        flips = np.zeros(1000)
        flips[np.random.rand(1000) < p] = 1
        empirical_p = flips.mean()
        print(f"Empirical probability: {empirical_p:.3f}")
        print(f"Close to 0.7: {abs(empirical_p - 0.7) < 0.05}")
