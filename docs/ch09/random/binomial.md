# Binomial Distribution

The binomial distribution models the number of successes in a fixed number of independent trials.

!!! note "Random Computation Model (applies to all distributions in this section)"

    Every distribution in NumPy follows the same four-step pattern:

    1. **Choose a distribution** — uniform, normal, binomial, Poisson, etc.
    2. **Generate many samples** — vectorized, in a single call
    3. **Treat samples as an array** — apply NumPy operations
    4. **Compute statistics or simulate** — mean, histogram, Monte Carlo

    This turns probability theory into array computation. Each distribution page that follows uses this same pipeline.

!!! tip "Mental Model"
    The binomial distribution answers "out of $n$ coin flips with probability $p$ of heads, how many heads do I get?" Each call to `np.random.binomial(n, p)` simulates that experiment once. Pass a `size` argument to run thousands of experiments in a single vectorized call, which is far faster than a Python loop.

## np.random.binomial

### 1. Basic Usage

```python
import numpy as np

def main():
    np.random.seed(42)
    
    n = 10   # number of trials
    p = 0.5  # probability of success
    
    samples = np.random.binomial(n, p, size=5)
    print(f"Samples: {samples}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Samples: [4 8 6 5 4]
```

### 2. Parameters

- `n`: Number of trials (positive integer)
- `p`: Probability of success in each trial (0 ≤ p ≤ 1)
- `size`: Output shape

### 3. Mathematical Form

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}$$

## Coin Flip Model

### 1. Fair Coin

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    n = 10
    p = 0.5
    data = np.random.binomial(n, p, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.set_title(f"Binomial(n={n}, p={p})", fontsize=15)
    bins = np.arange(n + 2) - 0.5
    ax.hist(data, bins=bins, density=True, alpha=0.4, label='Samples')
    
    # Theoretical PMF
    x = np.arange(n + 1)
    pmf = stats.binom(n, p).pmf(x)
    ax.stem(x, pmf, linefmt='r-', markerfmt='ro', basefmt=' ', label='PMF')
    
    ax.set_xlabel('Number of Successes')
    ax.set_ylabel('Probability')
    ax.set_xticks(np.arange(n + 1))
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Biased Coin

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    n = 10
    p = 0.3  # biased toward tails
    data = np.random.binomial(n, p, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.set_title(f"Binomial(n={n}, p={p})", fontsize=15)
    bins = np.arange(n + 2) - 0.5
    ax.hist(data, bins=bins, density=True, alpha=0.4, label='Samples')
    
    x = np.arange(n + 1)
    pmf = stats.binom(n, p).pmf(x)
    ax.stem(x, pmf, linefmt='r-', markerfmt='ro', basefmt=' ', label='PMF')
    
    ax.set_xlabel('Number of Successes')
    ax.set_ylabel('Probability')
    ax.set_xticks(np.arange(n + 1))
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Interpretation

Each sample counts successes in `n` independent Bernoulli trials with probability `p`.

## Varying Parameters

### 1. Effect of n

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    p = 0.5
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for ax, n in zip(axes, [5, 20, 50]):
        data = np.random.binomial(n, p, size=10_000)
        
        bins = np.arange(n + 2) - 0.5
        ax.hist(data, bins=bins, density=True, alpha=0.4)
        
        x = np.arange(n + 1)
        pmf = stats.binom(n, p).pmf(x)
        ax.stem(x, pmf, linefmt='r-', markerfmt='ro', basefmt=' ')
        
        ax.set_title(f"n={n}, p={p}")
        ax.set_xlabel('Successes')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Effect of p

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    n = 20
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for ax, p in zip(axes, [0.2, 0.5, 0.8]):
        data = np.random.binomial(n, p, size=10_000)
        
        bins = np.arange(n + 2) - 0.5
        ax.hist(data, bins=bins, density=True, alpha=0.4)
        
        x = np.arange(n + 1)
        pmf = stats.binom(n, p).pmf(x)
        ax.stem(x, pmf, linefmt='r-', markerfmt='ro', basefmt=' ')
        
        ax.set_title(f"n={n}, p={p}")
        ax.set_xlabel('Successes')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Mean and Variance

$$E[X] = np, \quad \text{Var}(X) = np(1-p)$$

```python
import numpy as np

def main():
    n, p = 100, 0.3
    samples = np.random.binomial(n, p, size=100_000)
    
    print(f"Theoretical mean: {n * p}")
    print(f"Sample mean:      {samples.mean():.2f}")
    print()
    print(f"Theoretical var:  {n * p * (1 - p)}")
    print(f"Sample var:       {samples.var():.2f}")

if __name__ == "__main__":
    main()
```

## scipy.stats Alternative

### 1. Using rvs

```python
import numpy as np
from scipy import stats

def main():
    np.random.seed(42)
    
    n, p = 10, 0.5
    
    # NumPy
    samples_np = np.random.binomial(n, p, size=5)
    
    # scipy.stats
    samples_scipy = stats.binom(n, p).rvs(size=5)
    
    print(f"NumPy:  {samples_np}")
    print(f"SciPy:  {samples_scipy}")

if __name__ == "__main__":
    main()
```

### 2. PMF and CDF

```python
import numpy as np
from scipy import stats

def main():
    n, p = 10, 0.5
    dist = stats.binom(n, p)
    
    # Probability of exactly 5 successes
    print(f"P(X = 5) = {dist.pmf(5):.4f}")
    
    # Probability of at most 5 successes
    print(f"P(X ≤ 5) = {dist.cdf(5):.4f}")

if __name__ == "__main__":
    main()
```

### 3. When to Use Each

- `np.random.binomial`: Fast sampling, simple interface
- `stats.binom`: Full distribution object with PMF, CDF, quantiles

## Applications

### 1. Quality Control

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Defect rate 2%, sample 100 items
    n_items = 100
    defect_rate = 0.02
    
    # Simulate 1000 inspections
    defects = np.random.binomial(n_items, defect_rate, size=1000)
    
    print(f"Mean defects per batch: {defects.mean():.2f}")
    print(f"Max defects observed:   {defects.max()}")
    print(f"Batches with 0 defects: {(defects == 0).sum()}")

if __name__ == "__main__":
    main()
```

### 2. A/B Testing

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Conversion rates
    p_control = 0.10
    p_treatment = 0.12
    n_users = 1000
    
    # Simulate experiments
    control = np.random.binomial(n_users, p_control, size=1000)
    treatment = np.random.binomial(n_users, p_treatment, size=1000)
    
    # How often does treatment beat control?
    wins = (treatment > control).mean()
    print(f"Treatment wins: {wins:.1%}")

if __name__ == "__main__":
    main()
```

### 3. Election Polling

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # True support 52%, poll 1000 voters
    true_support = 0.52
    n_polled = 1000
    
    # Simulate 1000 polls
    polls = np.random.binomial(n_polled, true_support, size=1000) / n_polled
    
    print(f"Mean poll result: {polls.mean():.3f}")
    print(f"Std of polls:     {polls.std():.3f}")
    print(f"Polls showing <50%: {(polls < 0.5).mean():.1%}")

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
