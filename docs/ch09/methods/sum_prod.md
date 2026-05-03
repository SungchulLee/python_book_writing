# Sum Prod Cumsum

!!! tip "Mental Model"
    `sum` adds elements, `prod` multiplies them, and `cumsum`/`cumprod` do the same but keep all intermediate results. The cumulative variants are especially useful for running totals, CDFs, and prefix-sum algorithms. All accept `axis` to operate along a specific dimension and `keepdims` to preserve the reduced axis as size 1.

    **Key insight:** `cumsum` is **discrete integration** — it converts rates into totals, just as integration sums up infinitesimal slices. Similarly, `np.diff` (in the [utility](utility.md) page) is **discrete differentiation**. Together they form a discrete calculus pair.

## sum and np.sum

### 1. Basic Usage

Sum all elements or along an axis.

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print(f"{a.sum() = }")
    print(f"{a.sum(axis=0) = }")
    print(f"{a.sum(axis=1) = }")

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[1 2]
 [3 1]
 [2 3]]

a.sum() = 12
a.sum(axis=0) = array([6, 6])
a.sum(axis=1) = array([3, 4, 5])
```

### 2. Function Syntax

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print(f"{np.sum(a) = }")
    print(f"{np.sum(a, axis=0) = }")
    print(f"{np.sum(a, axis=1) = }")

if __name__ == "__main__":
    main()
```

### 3. Row and Column Sum

```python
import numpy as np

def main():
    a = np.array([
        [8, 3, 9, 0, 10],
        [3, 5, 17, 1, 1],
        [2, 8, 6, 23, 1],
        [15, 7, 3, 2, 9],
        [6, 14, 2, 6, 0],
    ])
    
    print("Matrix:")
    print(a)
    print()
    
    print(f"Total Sum  : {a.sum()}")
    print(f"Column Sum : {a.sum(axis=0)}")
    print(f"Row Sum    : {a.sum(axis=1)}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Matrix:
[[ 8  3  9  0 10]
 [ 3  5 17  1  1]
 [ 2  8  6 23  1]
 [15  7  3  2  9]
 [ 6 14  2  6  0]]

Total Sum  : 150
Column Sum : [34 37 37 32 21]
Row Sum    : [30 27 40 36 28]
```

## cumsum and np.cumsum

### 1. Basic Usage

Cumulative sum returns running totals.

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    
    print(f"a = {a}")
    print(f"cumsum = {a.cumsum()}")
    # [1, 1+2, 1+2+3, 1+2+3+4, 1+2+3+4+5]
    # [1, 3, 6, 10, 15]

if __name__ == "__main__":
    main()
```

### 2. With axis Parameter

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print("a.cumsum() (flattened):")
    print(a.cumsum())
    print()
    
    print("a.cumsum(axis=0) (down columns):")
    print(a.cumsum(axis=0))
    print()
    
    print("a.cumsum(axis=1) (across rows):")
    print(a.cumsum(axis=1))

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[1 2]
 [3 1]
 [2 3]]

a.cumsum() (flattened):
[ 1  3  6  7  9 12]

a.cumsum(axis=0) (down columns):
[[1 2]
 [4 3]
 [6 6]]

a.cumsum(axis=1) (across rows):
[[1 3]
 [3 4]
 [2 5]]
```

### 3. Function Syntax

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print("np.cumsum(a):")
    print(np.cumsum(a))
    print()
    
    print("np.cumsum(a, axis=0):")
    print(np.cumsum(a, axis=0))
    print()
    
    print("np.cumsum(a, axis=1):")
    print(np.cumsum(a, axis=1))

if __name__ == "__main__":
    main()
```

## prod and np.prod

### 1. Basic Usage

Product of all elements or along an axis.

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print(f"{a.prod() = }")
    print(f"{a.prod(axis=0) = }")
    print(f"{a.prod(axis=1) = }")

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[1 2]
 [3 1]
 [2 3]]

a.prod() = 36
a.prod(axis=0) = array([6, 6])
a.prod(axis=1) = array([2, 3, 6])
```

### 2. Function Syntax

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print(f"{np.prod(a) = }")
    print(f"{np.prod(a, axis=0) = }")
    print(f"{np.prod(a, axis=1) = }")

if __name__ == "__main__":
    main()
```

### 3. Factorial Example

```python
import numpy as np

def main():
    # Compute 5! = 1 * 2 * 3 * 4 * 5
    n = 5
    factorial = np.arange(1, n + 1).prod()
    
    print(f"{n}! = {factorial}")
    
    # Multiple factorials
    for n in range(1, 8):
        fact = np.arange(1, n + 1).prod()
        print(f"{n}! = {fact}")

if __name__ == "__main__":
    main()
```

## cumprod and np.cumprod

### 1. Basic Usage

Cumulative product returns running products.

```python
import numpy as np

def main():
    a = np.array([1, 2, 3, 4, 5])
    
    print(f"a = {a}")
    print(f"cumprod = {a.cumprod()}")
    # [1, 1*2, 1*2*3, 1*2*3*4, 1*2*3*4*5]
    # [1, 2, 6, 24, 120]

if __name__ == "__main__":
    main()
```

### 2. With axis Parameter

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print("a.cumprod() (flattened):")
    print(a.cumprod())
    print()
    
    print("a.cumprod(axis=0) (down columns):")
    print(a.cumprod(axis=0))
    print()
    
    print("a.cumprod(axis=1) (across rows):")
    print(a.cumprod(axis=1))

if __name__ == "__main__":
    main()
```

**Output:**

```
a =
[[1 2]
 [3 1]
 [2 3]]

a.cumprod() (flattened):
[ 1  2  6  6 12 36]

a.cumprod(axis=0) (down columns):
[[1 2]
 [3 2]
 [6 6]]

a.cumprod(axis=1) (across rows):
[[1 2]
 [3 3]
 [2 6]]
```

### 3. Function Syntax

```python
import numpy as np

def main():
    a = np.array([[1, 2],
                  [3, 1],
                  [2, 3]])
    
    print("a =")
    print(a)
    print()
    
    print("np.cumprod(a):")
    print(np.cumprod(a))
    print()
    
    print("np.cumprod(a, axis=0):")
    print(np.cumprod(a, axis=0))
    print()
    
    print("np.cumprod(a, axis=1):")
    print(np.cumprod(a, axis=1))

if __name__ == "__main__":
    main()
```

## np.squeeze

### 1. Remove Size-1 Dims

`np.squeeze` removes dimensions of size 1.

```python
import numpy as np

def main():
    A = np.zeros((1, 3, 1))
    B = A.squeeze()
    C = A.squeeze(axis=2)
    
    print(f"{A.shape = }")
    print(f"{B.shape = }")
    print(f"{C.shape = }")

if __name__ == "__main__":
    main()
```

**Output:**

```
A.shape = (1, 3, 1)
B.shape = (3,)
C.shape = (1, 3)
```

### 2. Selective Squeeze

```python
import numpy as np

def main():
    a = np.zeros((1, 4, 1, 5, 1))
    
    print(f"Original: {a.shape}")
    print()
    
    # Squeeze all size-1 dimensions
    print(f"squeeze(): {a.squeeze().shape}")
    
    # Squeeze specific axis
    print(f"squeeze(axis=0): {a.squeeze(axis=0).shape}")
    print(f"squeeze(axis=2): {a.squeeze(axis=2).shape}")
    print(f"squeeze(axis=4): {a.squeeze(axis=4).shape}")

if __name__ == "__main__":
    main()
```

### 3. After Reduction

```python
import numpy as np

def main():
    a = np.array([[1, 2, 3],
                  [4, 5, 6]])
    
    # keepdims creates size-1 dimension
    row_sum = a.sum(axis=1, keepdims=True)
    print(f"With keepdims: {row_sum.shape}")
    print(row_sum)
    print()
    
    # Squeeze removes it
    squeezed = row_sum.squeeze()
    print(f"After squeeze: {squeezed.shape}")
    print(squeezed)

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Create a 3x4 matrix and compute the sum along both axes as well as the global sum. Verify that `np.sum(a)` equals `np.sum(np.sum(a, axis=0))`.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.arange(12).reshape(3, 4)
        print(f"Global sum: {np.sum(a)}")
        print(f"Sum of column sums: {np.sum(np.sum(a, axis=0))}")
        print(f"Match: {np.sum(a) == np.sum(np.sum(a, axis=0))}")

---

**Exercise 2.**
Use `np.cumsum` on a 1D array `[1, 2, 3, 4, 5]` and verify the last element of the cumulative sum equals the total sum. Then apply `np.cumprod` to the same array and verify the last element equals `np.prod(a)`.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([1, 2, 3, 4, 5])
        cs = np.cumsum(a)
        print(f"cumsum: {cs}, last == sum: {cs[-1] == np.sum(a)}")
        cp = np.cumprod(a)
        print(f"cumprod: {cp}, last == prod: {cp[-1] == np.prod(a)}")

---

**Exercise 3.**
Use `np.nansum` and `np.nanmean` to compute the sum and mean of an array that contains `np.nan` values: `a = np.array([1, 2, np.nan, 4, np.nan, 6])`. Compare with `np.sum(a)` and `np.mean(a)` which propagate NaN.

??? success "Solution to Exercise 3"

        import numpy as np

        a = np.array([1, 2, np.nan, 4, np.nan, 6])
        print(f"np.sum:    {np.sum(a)}")      # nan
        print(f"np.nansum: {np.nansum(a)}")    # 13.0
        print(f"np.mean:    {np.mean(a)}")     # nan
        print(f"np.nanmean: {np.nanmean(a)}")  # 3.25

---

**Exercise 4.**
Demonstrate that `cumsum` is discrete integration and `np.diff` is discrete differentiation. Starting with `velocities = np.array([0, 2, 5, 3, 1])`, compute positions via `cumsum`. Then recover the original velocities by applying `np.diff` to the positions (prepend 0). Verify the round-trip.

??? success "Solution to Exercise 4"

        import numpy as np

        velocities = np.array([0, 2, 5, 3, 1])

        # Integration: velocity → position
        positions = np.cumsum(velocities)
        print(f"Velocities: {velocities}")
        print(f"Positions:  {positions}")  # [0 2 7 10 11]

        # Differentiation: position → velocity
        recovered = np.diff(positions, prepend=0)
        print(f"Recovered:  {recovered}")  # [0 2 5 3 1]

        print(f"Round-trip: {np.array_equal(velocities, recovered)}")  # True

---

**Exercise 5.**
Use `np.cumprod` to compute the growth of a \$1000 investment given daily returns `r = np.array([0.01, -0.005, 0.02, -0.01, 0.015])`. The portfolio value after day `k` is `1000 * cumprod(1 + r)[:k+1]`. Print the portfolio value after each day.

??? success "Solution to Exercise 5"

        import numpy as np

        initial = 1000
        r = np.array([0.01, -0.005, 0.02, -0.01, 0.015])
        growth = np.cumprod(1 + r)
        portfolio = initial * growth
        print(f"Daily returns: {r}")
        print(f"Portfolio:     {np.round(portfolio, 2)}")
        # [1010.0, 1004.95, 1025.05, 1014.80, 1030.02]
