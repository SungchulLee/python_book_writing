# Poisson Distribution

The Poisson distribution models the number of events occurring in a fixed interval of time or space.

!!! tip "Mental Model"
    The Poisson distribution answers "how many events happen in a fixed window?" when events occur independently at a constant average rate $\lambda$. Its single parameter $\lambda$ is both the mean and the variance. For large $\lambda$, the Poisson approaches a normal distribution, which is why count data often looks bell-shaped.

## np.random.poisson

### 1. Basic Usage

```python
import numpy as np

def main():
    np.random.seed(42)
    
    lam = 5  # average rate (λ)
    
    samples = np.random.poisson(lam, size=10)
    print(f"Samples: {samples}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Samples: [4 7 4 8 3 6 3 3 3 6]
```

### 2. Parameters

- `lam`: Expected number of events (λ ≥ 0)
- `size`: Output shape

### 3. Mathematical Form

$$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$$

## Event Count Model

### 1. Histogram with PMF

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    lam = 10
    data = np.random.poisson(lam, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.set_title(f"Poisson(λ={lam})", fontsize=15)
    bins = np.arange(30) - 0.5
    ax.hist(data, bins=bins, density=True, alpha=0.4, label='Samples')
    
    # Theoretical PMF
    x = np.arange(30)
    pmf = stats.poisson(lam).pmf(x)
    ax.stem(x, pmf, linefmt='r-', markerfmt='ro', basefmt=' ', label='PMF')
    
    ax.set_xlabel('Number of Events')
    ax.set_ylabel('Probability')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Interpretation

Counts rare events over fixed intervals with average rate λ.

### 3. Key Property

$$E[X] = \text{Var}(X) = \lambda$$

```python
import numpy as np

def main():
    lam = 10
    samples = np.random.poisson(lam, size=100_000)
    
    print(f"Theoretical mean: {lam}")
    print(f"Sample mean:      {samples.mean():.2f}")
    print()
    print(f"Theoretical var:  {lam}")
    print(f"Sample var:       {samples.var():.2f}")

if __name__ == "__main__":
    main()
```

## Varying Lambda

### 1. Small Lambda

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    for ax, lam in zip(axes, [1, 5, 20]):
        data = np.random.poisson(lam, size=10_000)
        
        max_x = max(30, int(lam * 2.5))
        bins = np.arange(max_x) - 0.5
        ax.hist(data, bins=bins, density=True, alpha=0.4)
        
        x = np.arange(max_x)
        pmf = stats.poisson(lam).pmf(x)
        ax.stem(x, pmf, linefmt='r-', markerfmt='ro', basefmt=' ')
        
        ax.set_title(f"λ={lam}")
        ax.set_xlabel('Events')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Normal Approximation

For large λ, Poisson approaches normal distribution.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    lam = 50
    data = np.random.poisson(lam, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.hist(data, bins=50, density=True, alpha=0.4, label='Poisson samples')
    
    # Normal approximation
    x = np.linspace(data.min(), data.max(), 100)
    pdf = stats.norm(loc=lam, scale=np.sqrt(lam)).pdf(x)
    ax.plot(x, pdf, 'r-', linewidth=2, label=f'Normal(μ={lam}, σ²={lam})')
    
    ax.set_title(f"Poisson(λ={lam}) ≈ Normal for large λ")
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Skewness

Small λ produces right-skewed distributions; large λ becomes symmetric.

## scipy.stats Alternative

### 1. Using rvs

```python
import numpy as np
from scipy import stats

def main():
    np.random.seed(42)
    
    lam = 5
    
    # NumPy
    samples_np = np.random.poisson(lam, size=5)
    
    # scipy.stats
    samples_scipy = stats.poisson(lam).rvs(size=5)
    
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
    lam = 5
    dist = stats.poisson(lam)
    
    # Probability of exactly 5 events
    print(f"P(X = 5) = {dist.pmf(5):.4f}")
    
    # Probability of at most 5 events
    print(f"P(X ≤ 5) = {dist.cdf(5):.4f}")
    
    # Probability of more than 5 events
    print(f"P(X > 5) = {1 - dist.cdf(5):.4f}")

if __name__ == "__main__":
    main()
```

### 3. Quantiles

```python
from scipy import stats

def main():
    lam = 10
    dist = stats.poisson(lam)
    
    # Find k such that P(X ≤ k) ≈ 0.95
    k = dist.ppf(0.95)
    print(f"95th percentile: {k}")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Website Traffic

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Average 100 visits per hour
    avg_visits = 100
    
    # Simulate 24 hours
    hourly_visits = np.random.poisson(avg_visits, size=24)
    
    print(f"Hourly visits: {hourly_visits}")
    print(f"Total daily:   {hourly_visits.sum()}")
    print(f"Peak hour:     {hourly_visits.max()} visits")

if __name__ == "__main__":
    main()
```

### 2. Call Center

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    np.random.seed(42)
    
    # 30 calls per hour average
    lam = 30
    
    # Simulate 1000 hours
    calls = np.random.poisson(lam, size=1000)
    
    # Staffing: need capacity for 95th percentile
    capacity_needed = np.percentile(calls, 95)
    
    print(f"Average calls:    {calls.mean():.1f}")
    print(f"95th percentile:  {capacity_needed}")
    print(f"Max observed:     {calls.max()}")

if __name__ == "__main__":
    main()
```

### 3. Defect Detection

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # 2 defects per 100 meters average
    defect_rate = 2
    
    # Inspect 50 sections of 100m each
    defects = np.random.poisson(defect_rate, size=50)
    
    print(f"Defects per section: {defects}")
    print(f"Total defects:       {defects.sum()}")
    print(f"Sections with 0:     {(defects == 0).sum()}")

if __name__ == "__main__":
    main()
```

## Poisson Process

### 1. Connection to Exponential

Inter-arrival times in a Poisson process follow exponential distribution.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    lam = 5  # events per unit time
    
    # Simulate via Poisson
    n_events = np.random.poisson(lam, size=1000)
    
    # Simulate via exponential inter-arrivals
    # (count events in unit time)
    inter_arrivals = np.random.exponential(1/lam, size=(1000, 20))
    cumsum = inter_arrivals.cumsum(axis=1)
    n_events_exp = (cumsum < 1).sum(axis=1)
    
    print(f"Poisson mean:     {n_events.mean():.2f}")
    print(f"Exponential mean: {n_events_exp.mean():.2f}")

if __name__ == "__main__":
    main()
```

### 2. Superposition

Sum of independent Poisson RVs is Poisson.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    lam1, lam2 = 3, 7
    
    X1 = np.random.poisson(lam1, size=10_000)
    X2 = np.random.poisson(lam2, size=10_000)
    
    Y = X1 + X2  # Should be Poisson(lam1 + lam2)
    
    print(f"λ1 + λ2 = {lam1 + lam2}")
    print(f"Mean of X1 + X2: {Y.mean():.2f}")
    print(f"Var of X1 + X2:  {Y.var():.2f}")

if __name__ == "__main__":
    main()
```

### 3. Thinning

Randomly selecting from Poisson gives Poisson.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    lam = 10
    p = 0.3  # selection probability
    
    # Generate Poisson(10)
    N = np.random.poisson(lam, size=10_000)
    
    # Thin each sample
    thinned = np.array([np.random.binomial(n, p) for n in N])
    
    print(f"Expected: Poisson({lam * p})")
    print(f"Mean:     {thinned.mean():.2f}")
    print(f"Var:      {thinned.var():.2f}")

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
