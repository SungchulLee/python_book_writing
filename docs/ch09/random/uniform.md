# Uniform Distributions

NumPy provides functions for generating uniformly distributed random numbers over continuous intervals. The uniform distribution is the **foundation of all randomness** in NumPy --- every other distribution can be derived from uniform samples via mathematical transformations (inverse transform sampling).

!!! tip "Mental Model"
    `np.random.rand` draws from the half-open interval $[0, 1)$; scale and shift with `low + (high - low) * rand(...)` to cover any range, or use `np.random.uniform(low, high, size)` directly. Uniform samples are the raw ingredient from which all other distributions can be generated via inverse transform sampling.


## np.random.rand

Generates samples uniformly distributed over $[0, 1)$.

### 1. Basic Usage

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    n_samples = 10_000
    data = np.random.rand(n_samples)
    
    fig, ax = plt.subplots()
    
    _, bins_, _ = ax.hist(data, bins=100, density=True)
    
    low_ = data.min()
    high_ = data.max()
    pdf_at_bins_ = stats.uniform(loc=low_, scale=high_ - low_).pdf(bins_)
    ax.plot(bins_, pdf_at_bins_, '--r', linewidth=5)
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Shape Arguments

Pass dimensions as separate arguments: `np.random.rand(3, 2)` for a 3×2 array.


## np.random.uniform

Generates samples uniformly distributed over a specified interval.

### 1. Custom Interval

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    low = -1
    high = 1
    n_samples = 10_000
    
    data = np.random.uniform(low=low, high=high, size=(n_samples,))
    
    fig, ax = plt.subplots()
    
    _, bins_, _ = ax.hist(data, bins=100, density=True)
    
    low_ = data.min()
    high_ = data.max()
    pdf_at_bins_ = stats.uniform(loc=low_, scale=high_ - low_).pdf(bins_)
    ax.plot(bins_, pdf_at_bins_, '--r', linewidth=5)
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Half-Open Interval

Samples are drawn from $[\text{low}, \text{high})$, excluding the upper bound.


## Scaling Relation

Any uniform distribution can be derived from $U(0, 1)$.

### 1. Linear Transform

$X \sim U(a, b)$ is equivalent to $X = a + (b - a) \cdot U$ where $U \sim U(0, 1)$.

### 2. Practical Choice

Use `rand` for $[0, 1)$ and `uniform` for custom intervals.


## PDF Shape

The uniform distribution has constant probability density.

### 1. Flat Histogram

A properly normalized histogram of uniform samples appears flat.

### 2. Theoretical PDF

$$f(x) = \frac{1}{b - a} \quad \text{for } x \in [a, b)$$


## Common Applications

Uniform random numbers have many practical uses.

### 1. Random Selection

Uniformly sample indices or elements from arrays.

### 2. Monte Carlo

Uniform samples over $[0, 1)$ are the basis for many simulation methods.

### 3. Initialization

Neural network weights are often initialized from uniform distributions.

---

## Exercises

**Exercise 1.** Generate 1,000 uniform random numbers between 5 and 15 using `rng.uniform(5, 15, 1000)`. Verify the mean is approximately 10.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    samples = rng.uniform(5, 15, 1000)
    print(f"Mean: {samples.mean():.2f}")  # ~10.0
    ```

---

**Exercise 2.** Simulate rolling a fair die 10,000 times using `rng.integers(1, 7, size=10000)`. Count the frequency of each outcome and verify they are approximately equal.

??? success "Solution to Exercise 2"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    rolls = rng.integers(1, 7, size=10000)
    for i in range(1, 7):
        print(f"{i}: {np.sum(rolls == i)}")  # ~1667 each
    ```

---

**Exercise 3.** Generate a 3x4 matrix of uniform random numbers in [0, 1). Print the shape and the min/max values.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    matrix = rng.random((3, 4))
    print(f"Shape: {matrix.shape}")
    print(f"Min: {matrix.min():.4f}, Max: {matrix.max():.4f}")
    ```

---

**Exercise 4.** Use uniform random numbers to estimate the area of a circle with radius 1 (Monte Carlo method). Generate points in the unit square and count how many fall inside the circle.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    n = 1_000_000
    x = rng.uniform(-1, 1, n)
    y = rng.uniform(-1, 1, n)
    inside = np.sum(x**2 + y**2 <= 1)
    pi_estimate = 4 * inside / n
    print(f"Pi estimate: {pi_estimate:.4f}")  # ~3.1416
    ```
