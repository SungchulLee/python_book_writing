# Sampling (rvs)

The `.rvs()` method generates **random variates** (random samples) from a probability distribution. It is the primary tool for Monte Carlo simulation, bootstrapping, and any workflow that requires synthetic data from a known distribution.

!!! tip "Mental Model"
    Calling `.rvs(size=n)` is like rolling a custom die $n$ times, where the die is shaped by the distribution's parameters. The `random_state` parameter pins the sequence of rolls for reproducibility. The output is always a NumPy array, ready for vectorized computation.

---

## Basic Usage

Every frozen distribution in `scipy.stats` provides the `.rvs()` method:

```python
import scipy.stats as stats

a = stats.norm(loc=3.0)  # frozen normal distribution, mean=3, std=1
samples = a.rvs(size=(2, 3), random_state=1)
print(samples)
# [[4.62434536 2.38824359 2.47182825]
#  [1.92703138 3.86540763 0.6984613 ]]
print(type(samples))   # <class 'numpy.ndarray'>
print(samples.shape)   # (2, 3)
print(samples.dtype)   # float64
```

The output is always a NumPy array whose shape is determined by the `size` parameter. With `size=(2, 3)`, you get a 2x3 matrix of independent samples.

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `size` | int or tuple | Shape of the output array. `size=1000` gives a 1D array; `size=(100, 5)` gives a 2D array. |
| `random_state` | int, Generator, or RandomState | Seed for reproducibility. Pass an integer for deterministic results. |

## Reproducibility

The `random_state` parameter ensures that the same sequence of random numbers is generated each time:

```python
# These two calls produce identical samples
s1 = stats.norm(0, 1).rvs(size=5, random_state=42)
s2 = stats.norm(0, 1).rvs(size=5, random_state=42)
assert (s1 == s2).all()
```

For more control, pass a `numpy.random.Generator` object:

```python
import numpy as np
rng = np.random.default_rng(seed=42)
samples = stats.norm(0, 1).rvs(size=1000, random_state=rng)
```

## Verifying Samples Against Theory

A standard validation technique is to overlay a histogram of samples with the theoretical PDF (continuous) or PMF (discrete):

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

# Generate samples and overlay with theoretical PDF
a = stats.norm(loc=0, scale=1)
samples = a.rvs(size=10000, random_state=337)
x = np.linspace(-4, 4, 100)

plt.hist(samples, density=True, bins=50, alpha=0.7, label='Histogram')
plt.plot(x, a.pdf(x), 'r-', linewidth=2, label='Theoretical PDF')
plt.legend()
plt.title('Sampling Verification: Histogram vs PDF')
plt.show()
```

As the sample size increases, the histogram converges to the theoretical distribution — a visual demonstration of the law of large numbers.

## Sampling from Different Distribution Types

The `.rvs()` method works identically for continuous and discrete distributions:

```python
# Continuous distributions
stats.norm(0, 1).rvs(size=5)           # normal
stats.expon(scale=1/3).rvs(size=5)     # exponential with rate λ=3

# Discrete distributions
stats.poisson(mu=3.0).rvs(size=5)      # Poisson
stats.binom(n=100, p=0.6).rvs(size=5)  # binomial
```

For discrete distributions, `.rvs()` returns integer-valued arrays.

## Financial Applications

Random sampling is fundamental to Monte Carlo methods in finance: simulating asset price paths under geometric Brownian motion, generating scenarios for Value at Risk (VaR) estimation, pricing path-dependent options, and stress testing portfolio performance under various distributional assumptions.

## Summary

The `.rvs()` method is the gateway to simulation-based analysis. Combined with the `random_state` parameter for reproducibility and NumPy's array infrastructure, it provides an efficient and consistent interface for generating random samples from any `scipy.stats` distribution.

---

## Exercises

**Exercise 1.**
Generate 500 samples from a normal distribution with $\mu = 100$ and $\sigma = 15$ using `random_state=42`. Compute the sample mean and standard deviation. Repeat with `random_state=42` and verify you get identical results.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        samples1 = stats.norm.rvs(loc=100, scale=15, size=500, random_state=42)
        samples2 = stats.norm.rvs(loc=100, scale=15, size=500, random_state=42)

        print(f"Mean: {np.mean(samples1):.4f}, Std: {np.std(samples1, ddof=1):.4f}")
        print(f"Identical results: {np.array_equal(samples1, samples2)}")

---

**Exercise 2.**
Generate a $5 \times 4$ array of random samples from a uniform distribution on $[2, 7]$ using a single `.rvs()` call with the `size` parameter. Print the array shape and verify all values fall within $[2, 7]$.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        samples = stats.uniform.rvs(loc=2, scale=5, size=(5, 4), random_state=42)
        print(f"Shape: {samples.shape}")
        print(f"Min: {samples.min():.4f}, Max: {samples.max():.4f}")
        print(f"All in [2, 7]: {(samples >= 2).all() and (samples <= 7).all()}")

---

**Exercise 3.**
Draw 10,000 samples from both a $t$-distribution with 3 degrees of freedom and a standard normal. Compare the fraction of samples with $|x| > 3$ for each distribution to demonstrate heavier tails in the $t$-distribution.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        t_samples = stats.t.rvs(df=3, size=10000)
        norm_samples = stats.norm.rvs(size=10000)

        t_frac = np.mean(np.abs(t_samples) > 3)
        n_frac = np.mean(np.abs(norm_samples) > 3)
        print(f"Fraction |x|>3 — t(3): {t_frac:.4f}, Normal: {n_frac:.4f}")
