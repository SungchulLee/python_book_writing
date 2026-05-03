# Return Values

The `ax.hist()` method returns three objects that provide information about the created histogram.

!!! tip "Mental Model"
    `n, bins, patches = ax.hist(data)` gives you three things: `n` is the count (or density) per bin, `bins` is the array of bin edges (one longer than `n`), and `patches` is the list of Rectangle artists. Capture these return values when you need to post-process bin counts or individually style each bar after creation.

    The deeper connection: `n` and `bins` together define an **empirical
    distribution** — you can compute probabilities from them
    (`P(a < X < b) ≈ sum of density × bin_width` for bins in `[a, b]`), making
    the histogram a bridge between raw data and probability theory.

## Return Signature

```python
n, bins, patches = ax.hist(data, ...)
```

| Return | Type | Description |
|--------|------|-------------|
| `n` | array or list of arrays | Values of the histogram bins (counts or density) |
| `bins` | array | Edges of the bins (length = number of bins + 1) |
| `patches` | BarContainer or list | Container of individual bar artists |

## Using Return Values

The returned `bins` array is particularly useful for overlaying fitted distributions, as it provides the exact x-coordinates used by the histogram.

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def main():
    # data generation
    n_samples = 10_000
    data = np.random.randn(n_samples)

    # parameter estimation
    mu = data.mean()
    sigma = data.std()

    # plot histogram and capture return values
    fig, ax = plt.subplots()
    _, x, _ = ax.hist(data, bins=100, density=True, alpha=0.2)
    
    # use bins (x) to compute and plot pdf
    pdf = stats.norm(loc=mu, scale=sigma).pdf(x)
    ax.plot(x, pdf, '--r')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.show()

if __name__ == "__main__":
    main()
```

## Practical Applications

### Accessing bin counts

```python
n, bins, patches = ax.hist(data, bins=50)
print(f"Total count: {n.sum()}")
print(f"Max bin count: {n.max()}")
print(f"Bin with max count: {bins[n.argmax()]:.2f} to {bins[n.argmax()+1]:.2f}")
```

### Customizing individual bars

```python
n, bins, patches = ax.hist(data, bins=50)

# Color bars based on height
for count, patch in zip(n, patches):
    patch.set_facecolor(plt.cm.viridis(count / n.max()))
```

## Documentation

- [matplotlib.axes.Axes.hist](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html)


---

## Exercises

**Exercise 1.** Write code that captures the return values `(n, bins, patches)` from `ax.hist()` and prints the count in each bin and the bin edges.

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

**Exercise 2.** Explain what each element of the tuple `(n, bins, patches)` returned by `ax.hist()` represents. What is the relationship between the shapes of `n` and `bins`?

??? success "Solution to Exercise 2"
    `ax.hist()` returns `(n, bins, patches)` where `n` has shape `(20,)` containing the count or density in each bin, `bins` has shape `(21,)` containing the bin edges (one more than the number of bins), and `patches` is a list of 20 Rectangle objects.

---

**Exercise 3.** Write code that uses the `patches` return value to color each bar of a histogram based on its height (e.g., taller bars in darker colors).

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

**Exercise 4.** Create a histogram and use the returned `n` and `bins` arrays to compute and print the total area under the histogram when `density=True`. What should it equal?

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
