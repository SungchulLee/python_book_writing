# Seed and Reproduce

Setting a random seed ensures reproducible results in simulations and scientific computing.

!!! tip "Mental Model"
    A seed is the starting state of a pseudorandom number generator -- same seed, same sequence, every time. Set it once at the start of a script for reproducible experiments. Prefer the modern `np.random.default_rng(seed)` over the legacy `np.random.seed()` because the new API provides independent generators that do not share global state.


## Why Seeds Matter

Random number generators produce deterministic sequences from an initial state.

### 1. Pseudorandomness

NumPy uses pseudorandom number generators that are deterministic given the same seed.

### 2. Reproducibility

Scientific research requires reproducible results for validation and peer review.


## np.random.seed

Sets the global random state for the legacy random API.

### 1. Basic Usage

```python
import numpy as np

def main():
    np.random.seed(0)
    
    data = np.random.randn(5)
    print(data)

if __name__ == "__main__":
    main()
```

### 2. Consistent Results

Running the same seed produces identical sequences every time.


## Seed with Histogram

Visualize that seeded random samples follow expected distributions.

### 1. Normal Distribution

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def main():
    np.random.seed(0)
    
    n_samples = 10_000
    data = np.random.randn(n_samples)
    
    fig, ax = plt.subplots()
    
    _, bins_, _ = ax.hist(data, bins=100, density=True)
    
    mu = data.mean()
    sigma = data.std()
    pdf_at_bins_ = stats.norm(loc=mu, scale=sigma).pdf(bins_)
    ax.plot(bins_, pdf_at_bins_, '--r', linewidth=5)
    
    plt.show()

if __name__ == "__main__":
    main()
```

### 2. Histogram Fit

The red dashed line shows the theoretical PDF matching the sample histogram.


## Modern Generator API

The recommended approach uses explicit generator objects.

### 1. default_rng

```python
import numpy as np

rng = np.random.default_rng(seed=42)
data = rng.standard_normal(1000)
```

### 2. Advantages

Explicit generators avoid global state and enable parallel random streams.


## Best Practices

Follow these guidelines for reproducible random experiments.

### 1. Set Early

Set the seed at the beginning of your script or notebook.

### 2. Document Seeds

Record seed values in logs or comments for future reproduction.

### 3. Avoid Resetting

Resetting seeds mid-experiment can cause subtle statistical biases.

---

## Exercises

**Exercise 1.** Create two random number generators with the same seed. Verify they produce identical sequences.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)
    print(rng1.random(5))
    print(rng2.random(5))
    # Both produce identical arrays
    ```

---

**Exercise 2.** Explain why `np.random.seed(42)` is considered legacy. What is the modern alternative?

??? success "Solution to Exercise 2"
    `np.random.seed()` sets global state, which can cause subtle bugs in multithreaded code or when different parts of a program need independent random streams. The modern alternative is `np.random.default_rng(seed)`, which creates an independent generator instance.

---

**Exercise 3.** Generate 5 random floats using a seeded `default_rng`, save the seed, then reproduce the exact same sequence.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    seed = 12345
    rng = np.random.default_rng(seed)
    first_run = rng.random(5)
    rng = np.random.default_rng(seed)
    second_run = rng.random(5)
    print(np.array_equal(first_run, second_run))  # True
    ```

---

**Exercise 4.** Write a function `reproducible_sample(seed, n)` that always returns the same `n` random numbers for a given seed.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    def reproducible_sample(seed, n):
        rng = np.random.default_rng(seed)
        return rng.random(n)

    print(reproducible_sample(42, 5))
    print(reproducible_sample(42, 5))  # same output
    ```
