# Exponential Distribution

The exponential distribution models waiting times between events in a Poisson process.

!!! tip "Mental Model"
    The exponential distribution answers "how long until the next event?" when events occur at a constant average rate. It is the continuous counterpart of the geometric distribution and the inter-arrival time of a Poisson process. The single parameter `scale` is the average waiting time (the inverse of the rate).

## np.random.exponential

### 1. Basic Usage

```python
import numpy as np

def main():
    np.random.seed(42)
    
    scale = 2.0  # mean (1/λ)
    
    samples = np.random.exponential(scale, size=5)
    print(f"Samples: {samples}")

if __name__ == "__main__":
    main()
```

**Output:**

```
Samples: [0.74972129 1.90023865 2.42491801 0.31287245 2.82538488]
```

### 2. Parameters

- `scale`: Mean of distribution (β = 1/λ)
- `size`: Output shape

### 3. Mathematical Form

$$f(x) = \frac{1}{\beta} e^{-x/\beta} = \lambda e^{-\lambda x}$$

where β = scale = 1/λ.

## Histogram with PDF

### 1. Basic Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    scale = 2.0
    data = np.random.exponential(scale, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.set_title(f"Exponential(scale={scale})", fontsize=15)
    _, bins, _ = ax.hist(data, bins=100, density=True, alpha=0.4, label='Samples')
    
    # Theoretical PDF
    pdf = stats.expon(scale=scale).pdf(bins)
    ax.plot(bins, pdf, 'r-', linewidth=2, label='PDF')
    
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Rate Parameterization

Some contexts use rate λ = 1/scale.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    rate = 0.5  # λ
    scale = 1 / rate  # β = 1/λ
    
    data = np.random.exponential(scale, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    ax.set_title(f"Exponential(λ={rate})", fontsize=15)
    _, bins, _ = ax.hist(data, bins=100, density=True, alpha=0.4)
    
    pdf = stats.expon(scale=scale).pdf(bins)
    ax.plot(bins, pdf, 'r-', linewidth=2)
    
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Mean and Variance

$$E[X] = \beta = \frac{1}{\lambda}, \quad \text{Var}(X) = \beta^2 = \frac{1}{\lambda^2}$$

```python
import numpy as np

def main():
    scale = 2.0
    samples = np.random.exponential(scale, size=100_000)
    
    print(f"Theoretical mean: {scale}")
    print(f"Sample mean:      {samples.mean():.4f}")
    print()
    print(f"Theoretical var:  {scale**2}")
    print(f"Sample var:       {samples.var():.4f}")

if __name__ == "__main__":
    main()
```

## Varying Scale

### 1. Different Scales

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    for scale in [0.5, 1.0, 2.0, 4.0]:
        data = np.random.exponential(scale, size=10_000)
        ax.hist(data, bins=50, density=True, alpha=0.3, label=f'scale={scale}')
    
    ax.set_xlim(0, 15)
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.set_title('Exponential Distributions with Different Scales')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. PDF Comparison

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    x = np.linspace(0, 10, 200)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    for scale in [0.5, 1.0, 2.0, 4.0]:
        pdf = stats.expon(scale=scale).pdf(x)
        ax.plot(x, pdf, linewidth=2, label=f'scale={scale}')
    
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Exponential PDF')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Memoryless Property

$$P(X > s + t | X > s) = P(X > t)$$

```python
import numpy as np

def main():
    np.random.seed(42)
    
    scale = 2.0
    samples = np.random.exponential(scale, size=100_000)
    
    s, t = 1.0, 2.0
    
    # P(X > s + t | X > s)
    conditional = ((samples > s + t) & (samples > s)).sum() / (samples > s).sum()
    
    # P(X > t)
    marginal = (samples > t).mean()
    
    print(f"P(X > {s+t} | X > {s}) = {conditional:.4f}")
    print(f"P(X > {t})            = {marginal:.4f}")
    print("These should be approximately equal (memoryless property)")

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
    
    scale = 2.0
    
    # NumPy
    samples_np = np.random.exponential(scale, size=5)
    
    # scipy.stats
    samples_scipy = stats.expon(scale=scale).rvs(size=5)
    
    print(f"NumPy:  {samples_np}")
    print(f"SciPy:  {samples_scipy}")

if __name__ == "__main__":
    main()
```

### 2. PDF and CDF

```python
import numpy as np
from scipy import stats

def main():
    scale = 2.0
    dist = stats.expon(scale=scale)
    
    x = 3.0
    
    print(f"f({x}) = {dist.pdf(x):.4f}")
    print(f"P(X ≤ {x}) = {dist.cdf(x):.4f}")
    print(f"P(X > {x}) = {dist.sf(x):.4f}")  # survival function

if __name__ == "__main__":
    main()
```

### 3. Quantiles

```python
from scipy import stats

def main():
    scale = 2.0
    dist = stats.expon(scale=scale)
    
    # Median
    median = dist.ppf(0.5)
    print(f"Median: {median:.4f}")
    print(f"Theoretical: {scale * np.log(2):.4f}")
    
    # 95th percentile
    p95 = dist.ppf(0.95)
    print(f"95th percentile: {p95:.4f}")

if __name__ == "__main__":
    import numpy as np
    main()
```

## Poisson Connection

### 1. Inter-Arrival Times

Time between events in a Poisson process is exponential.

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    np.random.seed(42)
    
    rate = 5  # events per unit time
    scale = 1 / rate
    
    # Simulate inter-arrival times
    inter_arrivals = np.random.exponential(scale, size=100)
    
    # Event times
    event_times = np.cumsum(inter_arrivals)
    
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.eventplot([event_times[:50]], lineoffsets=0, linelengths=0.5)
    ax.set_xlabel('Time')
    ax.set_title('Poisson Process Events (first 50)')
    ax.set_xlim(0, event_times[49] + 0.5)
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Counting Events

```python
import numpy as np

def main():
    np.random.seed(42)
    
    rate = 5  # λ = 5 events per unit time
    scale = 1 / rate
    
    # Count events in [0, 1] via exponential inter-arrivals
    counts = []
    for _ in range(10_000):
        t = 0
        count = 0
        while True:
            t += np.random.exponential(scale)
            if t > 1:
                break
            count += 1
        counts.append(count)
    
    counts = np.array(counts)
    
    print(f"Expected (Poisson λ=5): mean=5, var=5")
    print(f"Simulated: mean={counts.mean():.2f}, var={counts.var():.2f}")

if __name__ == "__main__":
    main()
```

### 3. Sum of Exponentials

Sum of n exponentials is Gamma distributed.

```python
import numpy as np
from scipy import stats

def main():
    np.random.seed(42)
    
    scale = 2.0
    n = 5
    
    # Sum of n exponentials
    sums = np.array([
        np.random.exponential(scale, size=n).sum()
        for _ in range(10_000)
    ])
    
    # Should be Gamma(n, scale)
    print(f"Expected mean (n * scale): {n * scale}")
    print(f"Simulated mean: {sums.mean():.2f}")
    print()
    print(f"Expected var (n * scale²): {n * scale**2}")
    print(f"Simulated var: {sums.var():.2f}")

if __name__ == "__main__":
    main()
```

## Applications

### 1. Service Times

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Average service time 5 minutes
    avg_service = 5.0
    
    # Simulate 100 customers
    service_times = np.random.exponential(avg_service, size=100)
    
    print(f"Mean service time: {service_times.mean():.2f} min")
    print(f"Max service time:  {service_times.max():.2f} min")
    print(f"Total time:        {service_times.sum():.2f} min")

if __name__ == "__main__":
    main()
```

### 2. Component Lifetime

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Mean lifetime 1000 hours
    mean_life = 1000
    
    # Simulate 50 components
    lifetimes = np.random.exponential(mean_life, size=50)
    
    print(f"Mean lifetime:   {lifetimes.mean():.0f} hours")
    print(f"Median lifetime: {np.median(lifetimes):.0f} hours")
    print(f"Failed by 500h:  {(lifetimes < 500).sum()} components")

if __name__ == "__main__":
    main()
```

### 3. Radioactive Decay

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    np.random.seed(42)
    
    half_life = 5.0  # arbitrary units
    decay_rate = np.log(2) / half_life
    mean_lifetime = 1 / decay_rate
    
    # Simulate decay times for 1000 atoms
    decay_times = np.random.exponential(mean_lifetime, size=1000)
    
    # Count remaining atoms over time
    times = np.linspace(0, 30, 100)
    remaining = [(decay_times > t).sum() for t in times]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(times, remaining, label='Simulated')
    ax.plot(times, 1000 * np.exp(-decay_rate * times), 'r--', label='Theoretical')
    ax.set_xlabel('Time')
    ax.set_ylabel('Atoms Remaining')
    ax.set_title(f'Radioactive Decay (half-life = {half_life})')
    ax.legend()
    plt.show()

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
