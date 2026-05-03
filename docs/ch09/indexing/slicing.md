# Slicing Arrays

Slicing extracts contiguous subsequences from arrays using `start:stop:step` syntax.

!!! tip "Mental Model"
    A slice is a window into the original array's memory -- it selects a contiguous range without copying data. The `start:stop:step` syntax works the same as Python lists, but NumPy slices extend to multiple dimensions with comma-separated ranges. Because slices return views, modifying a slice modifies the original.


## 1D Array Slicing

Basic slicing works identically for lists and NumPy arrays.

### 1. Range Slice

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = np.array(a)
    print(f"{a = }")
    print(f"{b = }", end="\n\n")

    print(f"{a[1:2] = }")
    print(f"{b[1:2] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1:2] = [1]
b[1:2] = array([1])
```

### 2. From Start

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = np.array(a)

    print(f"{a[:5] = }")
    print(f"{b[:5] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[:5] = [0, 1, 2, 3, 4]
b[:5] = array([0, 1, 2, 3, 4])
```

### 3. To End

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = np.array(a)

    print(f"{a[1:] = }")
    print(f"{b[1:] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1:] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b[1:] = array([1, 2, 3, 4, 5, 6, 7, 8, 9])
```


## Step Slicing

The third parameter specifies the step size.

### 1. Step from Start

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = np.array(a)

    print(f"{a[:5:2] = }")
    print(f"{b[:5:2] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[:5:2] = [0, 2, 4]
b[:5:2] = array([0, 2, 4])
```

### 2. Step to End

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = np.array(a)

    print(f"{a[1::2] = }")
    print(f"{b[1::2] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1::2] = [1, 3, 5, 7, 9]
b[1::2] = array([1, 3, 5, 7, 9])
```

### 3. Reverse Array

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = np.array(a)

    print(f"{a[::-1] = }")
    print(f"{b[::-1] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[::-1] = [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
b[::-1] = array([9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
```


## 2D Array Slicing

Slicing 2D arrays operates on rows by default.

### 1. Row Range

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)

    print("a[:3]")
    print(a[:3], end="\n\n")
    print("b[:3]")
    print(b[:3])

if __name__ == "__main__":
    main()
```

### 2. Row with Step

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)

    print("a[:4:2]")
    print(a[:4:2], end="\n\n")
    print("b[:4:2]")
    print(b[:4:2])

if __name__ == "__main__":
    main()
```

### 3. Reverse Rows

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)

    print("a[::-1]")
    print(a[::-1], end="\n\n")
    print("b[::-1]")
    print(b[::-1])

if __name__ == "__main__":
    main()
```


## Multi-Axis Slicing

NumPy allows simultaneous slicing across multiple axes.

### 1. Row Slice Only

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)

    try:
        print(a[1, :])
    except TypeError as e:
        print(f"List error: {e}")
    print("b[1, :]")
    print(b[1, :])

if __name__ == "__main__":
    main()
```

Output:

```
List error: list indices must be integers or slices, not tuple
b[1, :]
[1 2 3]
```

### 2. Column Slice Only

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    b = np.array(a)

    try:
        print(a[:, 1])
    except TypeError as e:
        print(f"List error: {e}")
    print("b[:, 1]")
    print(b[:, 1])

if __name__ == "__main__":
    main()
```

Output:

```
List error: list indices must be integers or slices, not tuple
b[:, 1]
[1 2 3 4 5]
```

### 3. Both Axes

```python
import numpy as np

mat = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(mat[0:2, 1:])
```

Output:

```
[[2 3]
 [5 6]]
```

!!! warning "Views Are Fast but Dangerous"

    Slices return **views** (no data copy), which makes them fast and memory-efficient. But modifying a view modifies the original array:

    ```python
    a = np.arange(10)
    view = a[2:5]
    view[0] = 999
    print(a[2])  # 999 — original changed!
    ```

    Use `.copy()` when you need an independent copy: `safe = a[2:5].copy()`.

---

## Exercises

**Exercise 1.**
Given `a = np.arange(20)`, use slicing to extract every third element starting from index 2. Also extract the last 5 elements in reverse order using a single slice.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(20)
        every_third = a[2::3]
        print(f"Every third from index 2: {every_third}")

        last_five_reversed = a[-1:-6:-1]
        print(f"Last 5 reversed: {last_five_reversed}")

---

**Exercise 2.**
Create a 5x6 matrix `M = np.arange(30).reshape(5, 6)`. Use multi-axis slicing to extract the 3x2 submatrix consisting of rows 1--3 and columns 4--5. Also extract every other row and every other column.

??? success "Solution to Exercise 2"

        import numpy as np

        M = np.arange(30).reshape(5, 6)
        submatrix = M[1:4, 4:6]
        print(f"Submatrix (rows 1-3, cols 4-5):\n{submatrix}")

        every_other = M[::2, ::2]
        print(f"Every other row and col:\n{every_other}")

---

**Exercise 3.**
Given a 2D array, demonstrate that a NumPy slice returns a view by modifying a sliced subarray and checking that the original is also modified. Then repeat with `.copy()` and show the original is not modified.

??? success "Solution to Exercise 3"

        import numpy as np

        original = np.arange(12).reshape(3, 4)
        view = original[0:2, 0:2]
        view[0, 0] = 999
        print(f"Original after view modification:\n{original}")
        # original[0, 0] is now 999

        original2 = np.arange(12).reshape(3, 4)
        copy = original2[0:2, 0:2].copy()
        copy[0, 0] = 888
        print(f"Original after copy modification:\n{original2}")
        # original2[0, 0] is still 0
