# Normal Distributions

NumPy provides multiple functions for generating samples from normal (Gaussian) distributions.

!!! tip "Mental Model"
    `np.random.randn` draws from the standard normal $\mathcal{N}(0,1)$; scale and shift with `sigma * randn(...) + mu` to get any normal distribution. Alternatively, `np.random.normal(mu, sigma, size)` does it in one call. The normal distribution appears everywhere because the Central Limit Theorem guarantees that sums of many independent variables converge to it.

## np.random.randn

Generates samples from the standard normal distribution $\mathcal{N}(0, 1)$.

### 1. Basic Usage

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    n_samples = 10_000
    data = np.random.randn(n_samples)
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    _, bins, _ = ax.hist(data, bins=100, density=True, alpha=0.3, label='Histogram')
    
    pdf = stats.norm().pdf(bins)
    ax.plot(bins, pdf, '--r', linewidth=2, label='Standard Normal PDF')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Shape Argument

Pass dimensions as separate arguments.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # 1D array
    a = np.random.randn(5)
    print(f"1D: {a.shape}")
    
    # 2D array
    b = np.random.randn(3, 4)
    print(f"2D: {b.shape}")
    
    # 3D array
    c = np.random.randn(2, 3, 4)
    print(f"3D: {c.shape}")

if __name__ == "__main__":
    main()
```

### 3. Quick Sampling

Use `randn` for quick standard normal samples with positional shape.

## np.random.standard_normal

Alternative syntax for standard normal samples using `size` keyword.

### 1. Size Keyword

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    n_samples = 10_000
    data = np.random.standard_normal(size=(n_samples,))
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    _, bins, _ = ax.hist(data, bins=100, density=True, alpha=0.3, label='Histogram')
    
    pdf = stats.norm().pdf(bins)
    ax.plot(bins, pdf, '--r', linewidth=2, label='Standard Normal PDF')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Difference from randn

Uses `size` keyword tuple instead of positional dimension arguments.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # randn: positional arguments
    a = np.random.randn(3, 4)
    
    # standard_normal: size keyword
    b = np.random.standard_normal(size=(3, 4))
    
    print(f"randn shape: {a.shape}")
    print(f"standard_normal shape: {b.shape}")

if __name__ == "__main__":
    main()
```

### 3. Equivalent Results

Both produce standard normal samples; choice is stylistic.

## np.random.normal

Generates samples from a general normal distribution $\mathcal{N}(\mu, \sigma^2)$.

### 1. Parameters

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    loc = 5      # mean (μ)
    scale = 2    # standard deviation (σ)
    n_samples = 10_000
    
    data = np.random.normal(loc=loc, scale=scale, size=(n_samples,))
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    _, bins, _ = ax.hist(data, bins=100, density=True, alpha=0.3, label='Histogram')
    
    pdf = stats.norm(loc=loc, scale=scale).pdf(bins)
    ax.plot(bins, pdf, '--r', linewidth=2, label=f'N({loc}, {scale}²) PDF')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Scaling Relation

$X \sim \mathcal{N}(\mu, \sigma^2)$ is equivalent to $X = \mu + \sigma Z$ where $Z \sim \mathcal{N}(0, 1)$.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    mu, sigma = 5, 2
    n = 10_000
    
    # Method 1: np.random.normal
    x1 = np.random.normal(loc=mu, scale=sigma, size=n)
    
    # Method 2: transform standard normal
    np.random.seed(42)
    z = np.random.randn(n)
    x2 = mu + sigma * z
    
    print(f"Method 1 mean: {x1.mean():.4f}")
    print(f"Method 2 mean: {x2.mean():.4f}")

if __name__ == "__main__":
    main()
```

### 3. Use for Custom Mean/Std

Use `normal` when you need to specify mean and standard deviation.

## scipy.stats.norm.rvs

The scipy.stats alternative for normal sampling.

### 1. Basic Usage

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    n_samples = 10_000
    data = stats.norm(loc=0, scale=1).rvs(n_samples)
    
    fig, ax = plt.subplots(figsize=(12, 3))
    
    _, bins, _ = ax.hist(data, bins=100, density=True, alpha=0.3, label='Histogram')
    
    pdf = stats.norm().pdf(bins)
    ax.plot(bins, pdf, '--r', linewidth=2, label='Standard Normal PDF')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Distribution Object

Create a frozen distribution for repeated use.

```python
import numpy as np
from scipy import stats

def main():
    np.random.seed(42)
    
    # Create distribution object
    dist = stats.norm(loc=10, scale=3)
    
    # Sample
    samples = dist.rvs(size=5)
    print(f"Samples: {samples}")
    
    # Also get PDF, CDF, etc.
    print(f"PDF at 10: {dist.pdf(10):.4f}")
    print(f"CDF at 10: {dist.cdf(10):.4f}")

if __name__ == "__main__":
    main()
```

### 3. When to Use

Use `stats.norm` when you also need PDF, CDF, quantiles, or other distribution methods.

## Method Comparison

### 1. All Four Methods

```python
import numpy as np
from scipy import stats

def main():
    np.random.seed(0)
    n = 5
    
    print("Standard Normal N(0,1) - 4 equivalent methods:")
    print()
    
    np.random.seed(42)
    print(f"np.random.randn({n}):")
    print(f"  {np.random.randn(n)}")
    
    np.random.seed(42)
    print(f"np.random.standard_normal(size=({n},)):")
    print(f"  {np.random.standard_normal(size=(n,))}")
    
    np.random.seed(42)
    print(f"np.random.normal(0, 1, size={n}):")
    print(f"  {np.random.normal(0, 1, size=n)}")
    
    np.random.seed(42)
    print(f"stats.norm(0, 1).rvs({n}):")
    print(f"  {stats.norm(0, 1).rvs(n)}")

if __name__ == "__main__":
    main()
```

### 2. Summary Table

| Function | Standard Normal | General Normal | Shape Syntax |
|----------|----------------|----------------|--------------|
| `randn` | ✓ | ✗ | Positional args |
| `standard_normal` | ✓ | ✗ | `size=` keyword |
| `normal` | ✓ | ✓ | `size=` keyword |
| `stats.norm.rvs` | ✓ | ✓ | Positional or `size=` |

### 3. Recommendations

- Quick standard normal: `randn`
- Custom mean/std: `normal`
- Need PDF/CDF too: `stats.norm`

## Multivariate Normal

Generates samples from a multivariate normal distribution.

### 1. Covariance Matrix

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(42)
    
    mean = [0, 0]
    cov = [[1, 0.8], [0.8, 1]]
    
    x = np.random.multivariate_normal(mean, cov, size=1000)
    print(f"Shape: {x.shape}")
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x[:, 0], x[:, 1], alpha=0.3)
    ax.set_xlabel('X1')
    ax.set_ylabel('X2')
    ax.set_title('Bivariate Normal (ρ=0.8)')
    ax.set_aspect('equal')
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Correlation Structure

The covariance matrix determines the shape and orientation.

```python
import numpy as np
import matplotlib.pyplot as plt

def main():
    np.random.seed(42)
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    correlations = [-0.8, 0, 0.8]
    
    for ax, rho in zip(axes, correlations):
        cov = [[1, rho], [rho, 1]]
        x = np.random.multivariate_normal([0, 0], cov, size=500)
        ax.scatter(x[:, 0], x[:, 1], alpha=0.3)
        ax.set_title(f'ρ = {rho}')
        ax.set_xlim(-4, 4)
        ax.set_ylim(-4, 4)
        ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### 3. Higher Dimensions

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # 4D multivariate normal
    mean = [0, 0, 0, 0]
    cov = np.eye(4)  # independent components
    
    samples = np.random.multivariate_normal(mean, cov, size=1000)
    print(f"Shape: {samples.shape}")
    print(f"Sample mean: {samples.mean(axis=0)}")

if __name__ == "__main__":
    main()
```

## Chi-Square Distribution

A distribution derived from squared normal random variables.

### 1. Degrees of Freedom

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    df = 5
    data = np.random.chisquare(df=df, size=10_000)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    _, bins, _ = ax.hist(data, bins=100, density=True, alpha=0.3)
    
    pdf = stats.chi2(df).pdf(bins)
    ax.plot(bins, pdf, 'r-', linewidth=2, label=f'χ²({df}) PDF')
    
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Relation to Normal

$$\chi^2_k = \sum_{i=1}^{k} Z_i^2$$ where $Z_i \sim \mathcal{N}(0, 1)$.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    k = 5
    n_samples = 10_000
    
    # Method 1: np.random.chisquare
    chi2_direct = np.random.chisquare(df=k, size=n_samples)
    
    # Method 2: sum of squared normals
    z = np.random.randn(n_samples, k)
    chi2_manual = (z ** 2).sum(axis=1)
    
    print(f"Direct mean: {chi2_direct.mean():.2f} (expected: {k})")
    print(f"Manual mean: {chi2_manual.mean():.2f} (expected: {k})")

if __name__ == "__main__":
    main()
```

### 3. Varying df

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    x = np.linspace(0, 30, 200)
    
    fig, ax = plt.subplots(figsize=(10, 4))
    
    for df in [2, 5, 10, 15]:
        pdf = stats.chi2(df).pdf(x)
        ax.plot(x, pdf, linewidth=2, label=f'df={df}')
    
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title('Chi-Square Distributions')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.** Generate 10,000 samples from a normal distribution with mean 100 and standard deviation 15. Verify the sample mean and std are close to the true parameters.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    samples = rng.normal(100, 15, 10000)
    print(f"Mean: {samples.mean():.1f}")  # ~100
    print(f"Std: {samples.std():.1f}")    # ~15
    ```

---

**Exercise 2.** Generate standard normal samples and verify that approximately 68% fall within one standard deviation of the mean.

??? success "Solution to Exercise 2"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    samples = rng.standard_normal(10000)
    within_1std = np.sum(np.abs(samples) <= 1) / len(samples)
    print(f"Within 1 std: {within_1std:.2%}")  # ~68%
    ```

---

**Exercise 3.** Generate a 2D array of shape (1000, 3) from a standard normal. Compute the mean and std of each column.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    data = rng.standard_normal((1000, 3))
    print("Means:", data.mean(axis=0))
    print("Stds:", data.std(axis=0))
    ```

---

**Exercise 4.** Use the Box-Muller transform to generate normal samples from uniform samples: $Z = \sqrt{-2\ln U_1}\cos(2\pi U_2)$. Compare with `rng.standard_normal`.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    rng = np.random.default_rng(42)
    n = 10000
    u1 = rng.uniform(0, 1, n)
    u2 = rng.uniform(0, 1, n)
    z = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
    print(f"Box-Muller mean: {z.mean():.3f}, std: {z.std():.3f}")
    ```
