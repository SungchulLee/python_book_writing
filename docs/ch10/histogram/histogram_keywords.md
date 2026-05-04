# Histogram Keywords

The `ax.hist()` method accepts various keyword arguments to customize histogram appearance and behavior.

!!! tip "Mental Model"
    The three most important histogram keywords are `bins` (how many divisions), `density` (counts vs. probability density), and `histtype` (bar style). `bins` controls resolution, `density=True` normalizes area to 1 for comparison with PDFs, and `histtype='step'` draws outlines instead of filled bars for overlaying multiple distributions.

!!! note "Parameter Priority"
    Not all histogram parameters are equally important:

    1. **`bins`** → controls structure (most important — few bins = smooth, many = noisy)
    2. **`density`** → controls interpretation (counts vs probability density)
    3. **`histtype` / styling** → controls visual presentation (least important)

    **Bins = resolution of the distribution.** This is the same resolution
    tradeoff that appears in 2D density plots (gridsize, bandwidth): too few
    bins hides real structure, too many creates noise.

!!! note "Decision Guide — When to Use Which Option"
    | Situation | Parameter | Setting |
    |-----------|-----------|---------|
    | Comparing distributions with different sample sizes | `density` | `True` |
    | Overlaying multiple histograms | `histtype` | `'step'` or `'stepfilled'` with `alpha` |
    | Skewed data with long tails | `bins` | Custom edges (e.g., log-spaced) |
    | Side-by-side group comparison | `multiple datasets` | Pass list to `ax.hist()` |
    | Need exact bin boundaries | `bins` | Explicit sequence `[0, 10, 20, ...]` |
    | Want to see cumulative distribution | `cumulative` | `True` |

## bins

The `bins` parameter controls how data is grouped. It accepts either an integer (number of bins) or a sequence (explicit bin edges).

### bins as int

When `bins` is an integer, matplotlib automatically calculates bin edges spanning the data range.

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    # data generation
    n_samples = 10_000
    data = np.random.randn(n_samples)

    # plot histogram with integer bins
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.hist(data, bins=100, alpha=0.2)  # <--- int used
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

### bins as sequence

When `bins` is a sequence, it defines the exact positions of bin edges, providing precise control over binning.

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    # data generation
    n_samples = 10_000
    data = np.random.randn(n_samples)

    # plot histogram with sequence bins
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.hist(data, bins=np.linspace(-4, 4, 100), alpha=0.2)  # <--- sequence used
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
```

## density

The `density` parameter controls whether the histogram shows counts or probability density.

- `density=False` (default): y-axis shows raw counts
- `density=True`: y-axis shows probability density (area under histogram equals 1)

```python
import matplotlib.pyplot as plt
import numpy as np

def main():
    # data generation
    n_samples = 10_000
    data = np.random.randn(n_samples)

    # plot histogram in density scale
    fig, ax = plt.subplots()
    ax.hist(data, bins=100, density=True, alpha=0.2)  # <--- density=True
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.show()

if __name__ == "__main__":
    main()
```

## histtype

The `histtype` parameter controls the visual style of the histogram.

| Value | Description |
|-------|-------------|
| `'bar'` | Traditional bar-style histogram (default) |
| `'barstacked'` | Bar-style with stacked data |
| `'step'` | Unfilled line histogram |
| `'stepfilled'` | Filled line histogram |

### Example: step histogram with PMF overlay

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Set the seed for reproducibility
np.random.seed(42)

# Parameters for the binomial distribution
num_trials = 10
success_probability = 0.6

# Number of random samples to generate
num_samples = 100

# Generate random samples from the binomial distribution
samples = stats.binom(num_trials, success_probability).rvs(num_samples)

# Possible outcomes from 0 successes to 'num_trials' successes
outcomes = np.arange(num_trials + 1)

# Probability mass function values for each outcome
pmf_values = stats.binom(num_trials, success_probability).pmf(outcomes)

# Set up the plot
fig, ax = plt.subplots(figsize=(12, 3))

# Bar plot to show the probability mass function
ax.bar(outcomes, pmf_values, alpha=0.2, color='red', label='Binomial PMF')

# Histogram of the sampled data with step style
ax.hist(samples, bins=np.arange(num_trials + 2) - 0.5, 
        density=True, histtype='step', label='Sampled Data Histogram')

# Adding labels and legend
ax.set_xlabel('Number of Successes')
ax.set_ylabel('Probability')
ax.legend()

plt.show()
```

## Documentation

- [matplotlib.axes.Axes.hist](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html)


---

## Exercises

**Exercise 1.** Write code demonstrating the `histtype` parameter by creating a 2x2 subplot grid showing the same data with `histtype='bar'`, `'barstacked'`, `'step'`, and `'stepfilled'`.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data = np.random.normal(5, 2, 1000)

    fig, ax = plt.subplots()
    ax.hist(data, bins=30, density=True, alpha=0.7, color='steelblue',
            edgecolor='black')
    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.set_title('Histogram')
    plt.show()
    ```

---

**Exercise 2.** Explain the difference between `bins=30` (integer) and `bins='auto'` in `ax.hist()`. What algorithm does `'auto'` use?

??? success "Solution to Exercise 2"
    `ax.hist()` returns `(n, bins, patches)` where `n` has shape `(20,)` containing the count or density in each bin, `bins` has shape `(21,)` containing the bin edges (one more than the number of bins), and `patches` is a list of 20 Rectangle objects.

---

**Exercise 3.** Create a histogram with custom bin edges using `bins=[0, 1, 2, 5, 10, 20]` (non-uniform spacing). Explain when non-uniform bins are useful.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    normal_data = np.random.normal(0, 1, 1000)
    exp_data = np.random.exponential(1, 1000)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.hist(normal_data, bins=30, density=True, alpha=0.7, color='steelblue')
    ax1.set_title('Normal Distribution')

    ax2.hist(exp_data, bins=30, density=True, alpha=0.7, color='coral')
    ax2.set_title('Exponential Distribution')

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 4.** Write code that creates a cumulative histogram using `cumulative=True` and overlays the theoretical CDF for the same distribution.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    data1 = np.random.normal(0, 1, 1000)
    data2 = np.random.normal(3, 1, 1000)

    fig, ax = plt.subplots()
    ax.hist(data1, bins=30, alpha=0.5, label='N(0, 1)', color='blue')
    ax.hist(data2, bins=30, alpha=0.5, label='N(3, 1)', color='red')
    ax.legend()
    ax.set_title('Overlaid Histograms')
    plt.show()
    ```
