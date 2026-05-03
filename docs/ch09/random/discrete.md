# Discrete Distributions

NumPy provides functions for **sampling from probability mass functions** — distributions where outcomes are countable (integers, categories, labels) rather than continuous.

!!! tip "Mental Model"
    Discrete random generators produce integer-valued samples. `randint` draws from a uniform range (like rolling a die), while `choice` draws from an arbitrary set with optional probability weights. Both support the `size` parameter to generate arrays of samples in one fast call.

    The unifying concept: every discrete distribution assigns a **probability to
    each possible outcome** (a probability mass function). `randint` assumes equal
    probabilities; `choice` with `p=` lets you specify arbitrary weights;
    `multinomial` draws counts from multiple categories simultaneously.

## np.random.randint

Generates random integers from a discrete uniform distribution.

### 1. Basic Usage

```python
import numpy as np

def main():
    np.random.seed(0)
    
    # Random integers from 0 to 9
    samples = np.random.randint(0, 10, size=10)
    print(f"Samples: {samples}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Samples: [5 0 3 3 7 9 3 5 2 4]
```

### 2. Half-Open Interval

`randint(low, high)` samples from $[\text{low}, \text{high})$ — high is excluded.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Integers from 1 to 6 (inclusive)
    # Use high=7 to include 6
    dice = np.random.randint(1, 7, size=10)
    print(f"Dice rolls: {dice}")

if __name__ == "__main__":
    main()
```

### 3. Fair Dice Histogram

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    np.random.seed(0)
    
    data = np.random.randint(low=1, high=7, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("Fair Dice Rolls", fontsize=15)
    bins = np.arange(1, 8) - 0.5
    ax.hist(data, bins=bins, density=True, alpha=0.4, rwidth=0.9)
    ax.axhline(1/6, color='r', linestyle='--', label='Expected: 1/6')
    ax.set_xticks(np.arange(1, 7))
    ax.set_xlabel('Face')
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.show()

if __name__ == "__main__":
    main()
```

## np.random.choice

Samples from a custom discrete distribution or array.

### 1. Uniform Sampling

```python
import numpy as np

def main():
    np.random.seed(42)
    
    Omega = ['A', 'B', 'C', 'D', 'E']
    samples = np.random.choice(Omega, size=10)
    print(f"Samples: {samples}")

if __name__ == "__main__":
    main()
```

### 2. Custom Weights

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    np.random.seed(0)
    
    Omega = [-3, -1, 1, 2, 5]
    pmf = [0.1, 0.1, 0.1, 0.5, 0.2]
    
    sample = np.random.choice(Omega, p=pmf, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_title("Custom Discrete Distribution", fontsize=15)
    bins = np.array([-4, -2, 0, 1.5, 3.5, 6])
    ax.hist(sample, bins=bins, density=True, alpha=0.4, rwidth=0.8)
    
    # Mark theoretical probabilities
    for val, prob in zip(Omega, pmf):
        ax.plot(val, prob, 'ro', markersize=10)
    
    ax.set_xlabel('Value')
    ax.set_ylabel('Probability')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Without Replacement

```python
import numpy as np

def main():
    np.random.seed(42)
    
    Omega = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Sample 5 unique elements
    sample = np.random.choice(Omega, size=5, replace=False)
    print(f"Without replacement: {sample}")
    
    # With replacement allows duplicates
    sample_wr = np.random.choice(Omega, size=5, replace=True)
    print(f"With replacement:    {sample_wr}")

if __name__ == "__main__":
    main()
```

## np.random.geometric

Generates samples from the geometric distribution.

### 1. Basic Usage

```python
import numpy as np

def main():
    np.random.seed(42)
    
    p = 0.3  # probability of success
    samples = np.random.geometric(p, size=10)
    print(f"Samples: {samples}")

if __name__ == "__main__":
    main()
```

### 2. Waiting Time

Number of trials until the first success.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    p = 0.3
    data = np.random.geometric(p, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.set_title(f"Geometric(p={p})", fontsize=15)
    max_x = 20
    bins = np.arange(1, max_x + 1) - 0.5
    ax.hist(data[data < max_x], bins=bins, density=True, alpha=0.4, label='Samples')
    
    # Theoretical PMF
    x = np.arange(1, max_x)
    pmf = stats.geom(p).pmf(x)
    ax.stem(x, pmf, linefmt='r-', markerfmt='ro', basefmt=' ', label='PMF')
    
    ax.set_xlabel('Number of Trials')
    ax.set_ylabel('Probability')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Mean and Variance

$$E[X] = \frac{1}{p}, \quad \text{Var}(X) = \frac{1-p}{p^2}$$

```python
import numpy as np

def main():
    p = 0.3
    samples = np.random.geometric(p, size=100_000)
    
    print(f"Theoretical mean: {1/p:.4f}")
    print(f"Sample mean:      {samples.mean():.4f}")
    print()
    print(f"Theoretical var:  {(1-p)/p**2:.4f}")
    print(f"Sample var:       {samples.var():.4f}")

if __name__ == "__main__":
    main()
```

## Categorical Sampling

### 1. Multinomial

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Roll a biased die 100 times
    probs = [0.1, 0.1, 0.2, 0.2, 0.2, 0.2]  # sum to 1
    n_trials = 100
    
    counts = np.random.multinomial(n_trials, probs)
    print(f"Face counts: {counts}")
    print(f"Total: {counts.sum()}")

if __name__ == "__main__":
    main()
```

### 2. Multiple Experiments

```python
import numpy as np

def main():
    np.random.seed(42)
    
    probs = [0.2, 0.3, 0.5]
    n_trials = 10
    n_experiments = 5
    
    results = np.random.multinomial(n_trials, probs, size=n_experiments)
    print("Results (rows=experiments, cols=categories):")
    print(results)

if __name__ == "__main__":
    main()
```

### 3. Simulation Use Case

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Customer segments: [Budget, Standard, Premium]
    segment_probs = [0.5, 0.35, 0.15]
    
    # Simulate 1000 customers
    n_customers = 1000
    segment_counts = np.random.multinomial(n_customers, segment_probs)
    
    labels = ['Budget', 'Standard', 'Premium']
    for label, count in zip(labels, segment_counts):
        print(f"{label:10}: {count} ({count/n_customers:.1%})")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Bootstrap Sampling

```python
import numpy as np

def main():
    np.random.seed(42)
    
    data = np.array([2.3, 3.1, 4.5, 2.8, 3.9, 4.2, 3.5])
    
    # Bootstrap: sample with replacement
    n_bootstrap = 1000
    means = []
    
    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=len(data), replace=True)
        means.append(sample.mean())
    
    means = np.array(means)
    print(f"Original mean: {data.mean():.3f}")
    print(f"Bootstrap mean: {means.mean():.3f}")
    print(f"95% CI: [{np.percentile(means, 2.5):.3f}, {np.percentile(means, 97.5):.3f}]")

if __name__ == "__main__":
    main()
```

### 2. Random Index Selection

```python
import numpy as np

def main():
    np.random.seed(42)
    
    n_samples = 1000
    n_select = 100
    
    # Random indices for train/test split
    indices = np.arange(n_samples)
    test_idx = np.random.choice(indices, size=n_select, replace=False)
    train_idx = np.setdiff1d(indices, test_idx)
    
    print(f"Train size: {len(train_idx)}")
    print(f"Test size:  {len(test_idx)}")

if __name__ == "__main__":
    main()
```

### 3. Weighted Random Selection

```python
import numpy as np

def main():
    np.random.seed(42)
    
    items = ['Apple', 'Banana', 'Cherry', 'Date']
    weights = [10, 5, 3, 2]  # relative weights
    
    # Normalize to probabilities
    probs = np.array(weights) / sum(weights)
    
    # Sample 20 items
    samples = np.random.choice(items, size=20, p=probs)
    
    print("Samples:", samples)
    print()
    for item in items:
        count = (samples == item).sum()
        print(f"{item}: {count}")

if __name__ == "__main__":
    main()
```

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
