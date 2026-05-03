# Basic Indexing

NumPy arrays support flexible indexing to access individual elements. This is the first of four selection methods that together form NumPy's selection system:

| Method | What it selects | View or Copy | Dimension effect |
|---|---|---|---|
| **Indexing** (this page) | Single elements | View | Reduces dimension |
| [Slicing](slicing.md) | Contiguous ranges | **View** | Preserves dimension |
| [Boolean masking](boolean_masking.md) | Condition-based | **Copy** | Flattens |
| [Fancy indexing](fancy_indexing.md) | Arbitrary positions | **Copy** | Shape = index shape |

!!! tip "Mental Model"
    NumPy indexing works like Python list indexing extended to multiple dimensions. Supply one index per axis, separated by commas, to pinpoint a single element. Negative indices count from the end, and each index reduces the result by one dimension.


## Positive Indexing

Access elements using zero-based positive indices.

### 1. 1D Array Access

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"{a[1] = }")

    b = np.array(a)
    print(f"{b[1] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1] = 1
b[1] = 1
```

### 2. 2D Array Access

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    print(f"{a[1] = }")

    b = np.array(a)
    print(f"{b[1] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1] = [1, 2, 3]
b[1] = array([1, 2, 3])
```


## Negative Indexing

Access elements from the end using negative indices.

### 1. 1D Negative Index

```python
import numpy as np

def main():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"{a[-2] = }")

    b = np.array(a)
    print(f"{b[-2] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[-2] = 8
b[-2] = 8
```

### 2. 2D Negative Index

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    print(f"{a[-2] = }")

    b = np.array(a)
    print(f"{b[-2] = }, {b[-2].shape = }")
    print(f"{b[-2:-1] = }, {b[-2:-1].shape = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[-2] = [3, 4, 5]
b[-2] = array([3, 4, 5]), b[-2].shape = (3,)
b[-2:-1] = array([[3, 4, 5]]), b[-2:-1].shape = (1, 3)
```


## List-like Indexing

Chain indices with multiple brackets, works for both lists and arrays.

### 1. Positive Chaining

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    print(f"{a[1][1] = }")

    b = np.array(a)
    print(f"{b[1][1] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[1][1] = 2
b[1][1] = 2
```

### 2. Negative Chaining

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    print(f"{a[-2][-2] = }")

    b = np.array(a)
    print(f"{b[-2][-2] = }")

if __name__ == "__main__":
    main()
```

Output:

```
a[-2][-2] = 4
b[-2][-2] = 4
```


## NumPy-Only Indexing

Use comma-separated indices inside single brackets (NumPy exclusive).

### 1. Tuple Syntax

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    try:
        print(f"{a[1, 1] = }")
    except TypeError as e:
        print(f"List error: {e}")

    b = np.array(a)
    print(f"{b[1, 1] = }")

if __name__ == "__main__":
    main()
```

Output:

```
List error: list indices must be integers or slices, not tuple
b[1, 1] = 2
```

### 2. Negative Tuple

```python
import numpy as np

def main():
    a = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6]]
    try:
        print(f"{a[-2, -2] = }")
    except TypeError as e:
        print(f"List error: {e}")

    b = np.array(a)
    print(f"{b[-2, -2] = }")

if __name__ == "__main__":
    main()
```

Output:

```
List error: list indices must be integers or slices, not tuple
b[-2, -2] = 4
```


## Iteration Example

Print all elements of a 2D array using indexing.

### 1. Nested Loop

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3], [4, 5, 6]])
    rows, cols = a.shape

    for i in range(rows):
        for j in range(cols):
            element = a[i, j]
            if j != cols - 1:
                print(element, end=' ')
            else:
                print(element)

if __name__ == "__main__":
    main()
```

Output:

```
1 2 3
4 5 6
```

### 2. Shape Unpacking

Use `a.shape` to get dimensions for iteration bounds.

---

## Runnable Example: `array_indexing_tutorial.py`

```python
"""
03_array_indexing.py - Indexing and Slicing

🔗 CRITICAL: Slices return VIEWS not COPIES! (Topic #24)
"""

import numpy as np

if __name__ == "__main__":

    print("="*80)
    print("ARRAY INDEXING AND SLICING")
    print("="*80)
    print("\n🔗 Views vs Copies - Critical concept from Topic #24!")

    # ============================================================================
    # 1D Indexing (like Python lists)
    # ============================================================================

    print("\n" + "="*80)
    print("1D Indexing")
    print("="*80)

    arr = np.array([10, 20, 30, 40, 50])
    print(f"Array: {arr}")
    print(f"  arr[0] = {arr[0]}")  # First element
    print(f"  arr[-1] = {arr[-1]}")  # Last element
    print(f"  arr[1:4] = {arr[1:4]}")  # Slicing

    # ============================================================================
    # CRITICAL: Slices are VIEWS! (Topic #24)
    # ============================================================================

    print("\n" + "="*80)
    print("CRITICAL: Slices Return VIEWS (Topic #24)")
    print("="*80)

    arr = np.array([1, 2, 3, 4, 5])
    view = arr[1:4]  # Elements at index 1, 2, 3

    print(f"Original: {arr}")
    print(f"View: {view}")
    print(f"\nview.base is arr: {view.base is arr} ← It's a VIEW!")

    # Modify the view
    view[0] = 999
    print(f"\nAfter view[0] = 999:")
    print(f"  Original: {arr} ← CHANGED!")
    print(f"  View: {view}")

    print("""
    This is DIFFERENT from Python lists!
    Python: slice_copy = my_list[1:4]  # Creates COPY
    NumPy:  view = arr[1:4]            # Creates VIEW

    Why? Memory efficiency (Topic #24)!
    Views share memory, no copying needed.
    """)

    # Want an independent copy? Use .copy()
    arr = np.array([1, 2, 3, 4, 5])
    independent = arr[1:4].copy()
    independent[0] = 888

    print(f"\nUsing .copy():")
    print(f"  Original: {arr} ← Unchanged")
    print(f"  Copy: {independent}")

    # ============================================================================
    # Multi-dimensional Indexing
    # ============================================================================

    print("\n" + "="*80)
    print("2D Indexing")
    print("="*80)

    matrix = np.array([[10, 20, 30],
                       [40, 50, 60],
                       [70, 80, 90]])
    print(f"Matrix:\n{matrix}\n")

    print(f"matrix[0, 0] = {matrix[0, 0]}  ← Row 0, Col 0")
    print(f"matrix[1, 2] = {matrix[1, 2]}  ← Row 1, Col 2")
    print(f"matrix[-1, -1] = {matrix[-1, -1]}  ← Last row, last col")

    # Slicing rows and columns
    print(f"\nmatrix[0, :] = {matrix[0, :]}  ← First row (all cols)")
    print(f"matrix[:, 0] = {matrix[:, 0]}  ← First column (all rows)")
    print(f"matrix[1:, 1:] = \n{matrix[1:, 1:]}  ← Bottom-right 2x2")

    # ============================================================================
    # Boolean Indexing (returns COPY!)
    # ============================================================================

    print("\n" + "="*80)
    print("Boolean Indexing")
    print("="*80)

    arr = np.array([10, 15, 20, 25, 30])
    mask = arr > 18  # Boolean array
    print(f"Array: {arr}")
    print(f"Mask (arr > 18): {mask}")
    print(f"arr[mask] = {arr[mask]}  ← Elements where mask is True")

    print("""
    \nNote: Boolean indexing creates a COPY, not a view!
    Why? Selected elements may not be contiguous in memory.
    """)

    print("""
    \n🎯 KEY TAKEAWAYS:
    1. Slicing returns VIEWS (shares memory!)
    2. Use .copy() for independent arrays
    3. Boolean indexing returns COPIES
    4. .base attribute checks if it's a view

    🔜 NEXT: 04_basic_operations.py
    """)
```

---

## Exercises

**Exercise 1.**
Create a 2D array of shape `(5, 4)` with values from 0 to 19. Access the element at row 3, column 2 using both `a[3][2]` (chained indexing) and `a[3, 2]` (tuple indexing). Verify both return the same value.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(20).reshape(5, 4)
        val1 = a[3][2]
        val2 = a[3, 2]
        print(f"a[3][2] = {val1}")
        print(f"a[3, 2] = {val2}")
        print(f"Equal: {val1 == val2}")

---

**Exercise 2.**
Given `a = np.arange(10)`, use negative indexing to extract the last three elements. Then use negative indexing on a 2D array `b = np.arange(20).reshape(4, 5)` to access the element in the second-to-last row and last column.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.arange(10)
        last_three = a[-3:]
        print(f"Last three: {last_three}")  # [7 8 9]

        b = np.arange(20).reshape(4, 5)
        val = b[-2, -1]
        print(f"b[-2, -1] = {val}")

---

**Exercise 3.**
Create a 3D array of shape `(2, 3, 4)` with `np.arange(24).reshape(2, 3, 4)`. Print the element at position `[1, 2, 3]` using tuple indexing. Then iterate over all elements using three nested loops and verify the sum equals `np.sum(a)`.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.arange(24).reshape(2, 3, 4)
        print(f"a[1, 2, 3] = {a[1, 2, 3]}")

        total = 0
        for i in range(a.shape[0]):
            for j in range(a.shape[1]):
                for k in range(a.shape[2]):
                    total += a[i, j, k]
        print(f"Loop sum: {total}")
        print(f"np.sum: {np.sum(a)}")
        print(f"Match: {total == np.sum(a)}")
