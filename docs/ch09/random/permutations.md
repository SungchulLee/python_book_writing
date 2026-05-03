# Random Permutations

NumPy provides functions for randomly reordering array elements. A permutation is a **random ordering** --- it is the basis for shuffling datasets before training, bootstrap sampling, and randomized algorithms. While distributions generate *new* random values, permutations rearrange *existing* data — a distinct but equally important form of randomization in the [random computation pipeline](uniform.md).

!!! tip "Mental Model"
    `shuffle` rearranges elements in place and returns `None`; `permutation` returns a shuffled copy and leaves the original untouched. For multi-dimensional arrays, both operate only along the first axis (shuffling rows, not individual elements). Use `permutation` when you need to keep the original data intact.


## np.random.shuffle

Shuffles an array in-place, modifying the original.

### 1. Returns None

```python
import numpy as np

def main():
    x = [1, 4, 9, 12, 15]
    result = np.random.shuffle(x)
    print(result)  # None

if __name__ == "__main__":
    main()
```

The function modifies the array in-place and returns `None`.

### 2. List Shuffle

```python
import numpy as np

def main():
    x = [1, 4, 9, 12, 15]
    np.random.shuffle(x)
    print(x)  # Shuffled list

if __name__ == "__main__":
    main()
```

### 3. Array Shuffle

```python
import numpy as np

def main():
    x = np.array([1, 4, 9, 12, 15])
    np.random.shuffle(x)
    print(x)

if __name__ == "__main__":
    main()
```


## 2D Array Shuffle

For multi-dimensional arrays, shuffle operates along the first axis.

### 1. Row Shuffling

```python
import numpy as np

def main():
    x = np.arange(9).reshape((3, 3))
    print("Before shuffle:")
    print(x)
    
    np.random.shuffle(x)
    print("After shuffle:")
    print(x)

if __name__ == "__main__":
    main()
```

### 2. Only First Axis

Rows are permuted, but elements within each row maintain their order.


## np.random.permutation

Returns a permuted copy, leaving the original unchanged.

### 1. From Integer

```python
import numpy as np

def main():
    x = np.random.permutation(10)
    print(x)  # Random permutation of 0-9

if __name__ == "__main__":
    main()
```

### 2. From List

```python
import numpy as np

def main():
    x = [1, 4, 9, 12, 15]
    y = np.random.permutation(x)
    print(y)
    print(x)  # Original unchanged

if __name__ == "__main__":
    main()
```

### 3. From Array

```python
import numpy as np

def main():
    x = np.array([1, 4, 9, 12, 15])
    y = np.random.permutation(x)
    print(y)

if __name__ == "__main__":
    main()
```


## 2D Permutation

Like shuffle, permutation operates along the first axis for 2D arrays.

### 1. Row Permutation

```python
import numpy as np

def main():
    x = np.arange(9).reshape((3, 3))
    y = np.random.permutation(x)
    print(y)

if __name__ == "__main__":
    main()
```

### 2. Non-Destructive

The original array `x` remains unchanged.


## shuffle vs permutation

Choose based on whether you need the original array.

### 1. Use shuffle

When you want to modify the array in-place to save memory.

### 2. Use permutation

When you need to preserve the original array or create an index array.

### 3. Memory Trade-off

`shuffle` is memory-efficient; `permutation` creates a copy.


## Common Applications

Random permutations are essential in many algorithms.

### 1. Data Shuffling

Randomize training data order before each epoch in machine learning.

### 2. Random Sampling

Create random indices for selecting subsets of data.

### 3. A/B Testing

Randomly assign subjects to control and treatment groups.

---

## Exercises

**Exercise 1.** Generate 1,000 samples from this distribution using NumPy. Compute the sample mean and variance and compare with the theoretical values.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    # Adjust parameters based on the specific distribution
    samples = rng.standard_normal(1000)  # example
    print(f"Sample mean: {samples.mean():.4f}")
    print(f"Sample var: {samples.var():.4f}")
    ```

---

**Exercise 2.** Create a histogram of 10,000 samples from this distribution using `np.histogram`. Print the bin edges and counts for the first 5 bins.

??? success "Solution to Exercise 2"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    samples = rng.standard_normal(10000)
    counts, edges = np.histogram(samples, bins=20)
    for i in range(5):
        print(f"[{edges[i]:.2f}, {edges[i+1]:.2f}): {counts[i]}")
    ```

---

**Exercise 3.** Write a function that generates `n` samples from this distribution and returns the proportion that fall below the mean. Verify it approaches the expected proportion as `n` grows.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    for n in [100, 1000, 10000, 100000]:
        samples = rng.standard_normal(n)
        below_mean = np.mean(samples < samples.mean())
        print(f"n={n:>7d}: {below_mean:.4f}")
    ```

---

**Exercise 4.** Simulate a real-world scenario that uses this distribution. Generate data, compute summary statistics, and explain why this distribution is appropriate for the scenario.

??? success "Solution to Exercise 4"
    The specific scenario depends on the distribution. For example, a Poisson distribution models the number of events per time interval (e.g., customers arriving at a store).

    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    # Example: Poisson arrivals
    arrivals = rng.poisson(lam=5, size=365)
    print(f"Mean daily arrivals: {arrivals.mean():.2f}")
    print(f"Max in a day: {arrivals.max()}")
    ```
