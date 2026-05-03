# Filtering with where

!!! tip "Mental Model"
    `np.where` has two modes: with one argument it returns the indices where a condition is True (like `np.nonzero`); with three arguments it acts as a vectorized if-else, choosing from two arrays element-by-element. The three-argument form is the NumPy replacement for `[a if c else b for c, a, b in zip(...)]`.

## np.where Basics

### 1. Find Indices

`np.where(condition)` returns indices where condition is True.

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 8, 2, 9, 4])
    
    # Find where values > 4
    indices = np.where(a > 4)
    
    print(f"Array: {a}")
    print(f"Indices where > 4: {indices}")
    print(f"Values at indices: {a[indices]}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Array: [1 5 3 8 2 9 4]
Indices where > 4: (array([1, 3, 5]),)
Values at indices: [5 8 9]
```

### 2. Tuple Return

`np.where` returns a tuple of arrays, one per dimension.

```python
import numpy as np

def main():
    a = np.array([[1, 5, 3],
                  [8, 2, 9]])
    
    # Find where values > 4
    rows, cols = np.where(a > 4)
    
    print("Array:")
    print(a)
    print()
    print(f"Row indices: {rows}")
    print(f"Col indices: {cols}")
    print()
    
    for r, c in zip(rows, cols):
        print(f"  a[{r}, {c}] = {a[r, c]}")

if __name__ == "__main__":
    main()
```

### 3. Extract First Match

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 8, 2, 9, 4])
    
    indices = np.where(a > 4)[0]
    
    print(f"Array: {a}")
    print(f"All indices > 4: {indices}")
    
    if len(indices) > 0:
        first_idx = indices[0]
        print(f"First index: {first_idx}")
        print(f"First value: {a[first_idx]}")

if __name__ == "__main__":
    main()
```

## Conditional Select

### 1. Three-Argument Form

`np.where(condition, x, y)` returns x where True, y where False.

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 8, 2, 9, 4])
    
    # Replace values: keep if > 4, else 0
    result = np.where(a > 4, a, 0)
    
    print(f"Original: {a}")
    print(f"Filtered: {result}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Original: [1 5 3 8 2 9 4]
Filtered: [0 5 0 8 0 9 0]
```

### 2. Conditional Replace

```python
import numpy as np

def main():
    a = np.array([-2, -1, 0, 1, 2])
    
    # Replace negative values with 0
    result = np.where(a < 0, 0, a)
    
    print(f"Original: {a}")
    print(f"Clipped:  {result}")

if __name__ == "__main__":
    main()
```

### 3. Choose Between Arrays

```python
import numpy as np

def main():
    condition = np.array([True, False, True, False])
    x = np.array([1, 2, 3, 4])
    y = np.array([10, 20, 30, 40])
    
    result = np.where(condition, x, y)
    
    print(f"Condition: {condition}")
    print(f"x: {x}")
    print(f"y: {y}")
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
```

## CDF Example

### 1. Find Threshold

Find smallest index where CDF exceeds a threshold.

```python
import numpy as np
from scipy import stats

def main():
    # Binomial distribution parameters
    n = 10
    p = 0.4
    
    # Values and CDF
    i = np.arange(0, n + 1)
    pmf = stats.binom.pmf(i, n, p)
    cdf = np.cumsum(pmf)
    
    # Find smallest t0 where P(X <= t0) >= 1/3
    threshold = 1/3
    t0 = np.where(cdf >= threshold)[0][0]
    
    print(f"Distribution: Binomial(n={n}, p={p})")
    print(f"Threshold: {threshold:.4f}")
    print(f"First i where CDF >= threshold: {t0}")
    print(f"CDF at t0: {cdf[t0]:.4f}")

if __name__ == "__main__":
    main()
```

### 2. Visualize CDF

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    n = 10
    p = 0.4
    
    i = np.arange(0, n + 1)
    pmf = stats.binom.pmf(i, n, p)
    cdf = np.cumsum(pmf)
    
    # Find threshold crossing
    t0 = np.where(cdf >= 1/3)[0][0]
    
    fig, ax = plt.subplots()
    
    ax.bar(i, cdf, color='lightblue', label='CDF')
    ax.axhline(y=1/3, color='b', ls='--', label='Threshold 1/3')
    
    # Mark t0
    ax.plot([t0, t0], [0, cdf[t0]], 'r--')
    ax.axhline(y=cdf[t0], xmax=t0/(n+1), color='r', ls='--')
    ax.scatter([t0], [cdf[t0]], color='red', s=50, zorder=5)
    
    ax.set_xlabel('Daily Demand')
    ax.set_ylabel('CDF')
    ax.set_title('CDF with Threshold')
    ax.legend()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Multiple Thresholds

```python
import numpy as np
from scipy import stats

def main():
    n = 20
    p = 0.3
    
    i = np.arange(0, n + 1)
    cdf = stats.binom.cdf(i, n, p)
    
    thresholds = [0.25, 0.50, 0.75, 0.90]
    
    print(f"Binomial(n={n}, p={p})")
    print()
    
    for thresh in thresholds:
        idx = np.where(cdf >= thresh)[0][0]
        print(f"P(X <= {idx}) = {cdf[idx]:.4f} >= {thresh}")

if __name__ == "__main__":
    main()
```

## vs Boolean Indexing

### 1. Comparison

```python
import numpy as np

def main():
    a = np.array([1, 5, 3, 8, 2, 9, 4])
    
    # Boolean indexing: direct values
    values = a[a > 4]
    
    # np.where: indices
    indices = np.where(a > 4)[0]
    values_via_where = a[indices]
    
    print(f"Array: {a}")
    print()
    print(f"Boolean indexing: {values}")
    print(f"np.where indices: {indices}")
    print(f"Values via where: {values_via_where}")

if __name__ == "__main__":
    main()
```

### 2. When to Use Each

```python
import numpy as np

def main():
    """
    Use boolean indexing when:
    - You only need the values
    - Simple filtering
    
    Use np.where when:
    - You need the indices/positions
    - Conditional replacement (3-arg form)
    - Working with multiple arrays
    """
    
    scores = np.array([85, 72, 90, 68, 95])
    names = np.array(['A', 'B', 'C', 'D', 'E'])
    
    # Boolean: just get passing scores
    passing_scores = scores[scores >= 70]
    print(f"Passing scores: {passing_scores}")
    
    # np.where: get names of passing students
    passing_idx = np.where(scores >= 70)[0]
    passing_names = names[passing_idx]
    print(f"Passing names: {passing_names}")

if __name__ == "__main__":
    main()
```

### 3. Combined Use

```python
import numpy as np

def main():
    np.random.seed(42)
    scores = np.round(np.random.uniform(30, 100, size=10))
    
    print(f"Scores: {scores}")
    print()
    
    # Find failing scores
    fail_mask = scores < 60
    fail_idx = np.where(fail_mask)[0]
    
    print(f"Failing indices: {fail_idx}")
    print(f"Failing scores: {scores[fail_idx]}")
    print()
    
    # Zero out first 3 failing scores
    if len(fail_idx) >= 3:
        scores[fail_idx[:3]] = 0
        print(f"After zeroing first 3 failures: {scores}")

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Use `np.where(condition)` (single argument) to find the indices of all elements greater than 0 in `a = np.array([-2, 3, -1, 5, 0, -4, 7])`.

??? success "Solution to Exercise 1"

        import numpy as np

        a = np.array([-2, 3, -1, 5, 0, -4, 7])
        indices = np.where(a > 0)
        print(f"Indices where > 0: {indices[0]}")
        print(f"Values: {a[indices]}")

---

**Exercise 2.**
Use `np.where(condition, x, y)` (three arguments) to replace all negative values in `a = np.array([-3, 2, -1, 5, -4])` with 0 while keeping positive values unchanged.

??? success "Solution to Exercise 2"

        import numpy as np

        a = np.array([-3, 2, -1, 5, -4])
        result = np.where(a < 0, 0, a)
        print(f"Original: {a}")
        print(f"Replaced: {result}")

---

**Exercise 3.**
Create a 4x4 matrix of random integers from 0 to 9. Use `np.where` to create a new matrix where even values are replaced by -1 and odd values remain. Print both the original and result.

??? success "Solution to Exercise 3"

        import numpy as np

        np.random.seed(42)
        M = np.random.randint(0, 10, size=(4, 4))
        result = np.where(M % 2 == 0, -1, M)
        print(f"Original:\n{M}")
        print(f"Evens replaced:\n{result}")

---

**Exercise 4.**
Use `np.where` as a vectorized if-else to implement a piecewise function: `f(x) = x^2` for `x >= 0` and `f(x) = -x` for `x < 0`. Apply it to `x = np.linspace(-3, 3, 7)` and print the result.

??? success "Solution to Exercise 4"

        import numpy as np

        x = np.linspace(-3, 3, 7)
        result = np.where(x >= 0, x ** 2, -x)
        print(f"x:    {x}")
        print(f"f(x): {result}")
        # x < 0: f(x) = -x → [3, 2, 1]
        # x ≥ 0: f(x) = x² → [0, 1, 4, 9]

---

**Exercise 5.**
Use `np.select` (which generalizes `np.where` to multiple conditions) to classify array values into categories: "negative" for `x < 0`, "small" for `0 <= x < 1`, and "large" for `x >= 1`. Apply to `x = np.array([-2, 0.5, 3, -0.1, 1.5, 0])`.

??? success "Solution to Exercise 5"

        import numpy as np

        x = np.array([-2, 0.5, 3, -0.1, 1.5, 0])
        conditions = [x < 0, (x >= 0) & (x < 1), x >= 1]
        choices = ["negative", "small", "large"]
        result = np.select(conditions, choices, default="unknown")
        print(f"x:      {x}")
        print(f"labels: {result}")
        # ['negative' 'small' 'large' 'negative' 'large' 'small']
