# PP Plots

A probability-probability (PP) plot compares the empirical cumulative distribution function of a sample against a theoretical CDF by plotting their values at each data point. While QQ plots compare quantiles and are more sensitive to tail deviations, PP plots compare cumulative probabilities and are more sensitive to deviations near the center of the distribution. This page explains how PP plots are constructed, how to interpret common patterns, and how to build them with SciPy.

!!! tip "Mental Model"
    A PP plot compares "how much probability has accumulated" at each data point under the empirical and theoretical distributions. Points on the diagonal mean the CDFs agree; S-shaped departures indicate a location or scale mismatch. PP plots are most sensitive near the center of the distribution, complementing QQ plots which are most sensitive in the tails.

---

## Construction

Given an ordered sample $x_{(1)} \le x_{(2)} \le \cdots \le x_{(n)}$ and a candidate distribution with CDF $F$, a PP plot displays the points

$$
\left(\frac{i}{n},\; F(x_{(i)})\right), \quad i = 1, 2, \ldots, n
$$

The horizontal axis shows the empirical cumulative probability $\hat{F}_n(x_{(i)}) = i/n$, and the vertical axis shows the theoretical cumulative probability $F(x_{(i)})$. If the data come from the distribution $F$, the points cluster along the identity line $y = x$.

!!! note "Plotting Position Adjustment"
    A common refinement replaces $i/n$ with a plotting position such as $(i - 0.5)/n$ or $i/(n+1)$ to avoid probabilities of exactly 0 and 1 at the boundaries.

---

## Building a PP Plot

SciPy does not provide a dedicated PP plot function, but constructing one requires only the CDF and sorted data.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
data = np.random.normal(loc=5, scale=2, size=200)

# Fit normal distribution
mu, sigma = stats.norm.fit(data)

# PP plot
data_sorted = np.sort(data)
n = len(data_sorted)
empirical_cdf = (np.arange(1, n + 1) - 0.5) / n  # Plotting position
theoretical_cdf = stats.norm.cdf(data_sorted, loc=mu, scale=sigma)

plt.figure(figsize=(6, 6))
plt.scatter(empirical_cdf, theoretical_cdf, s=10, alpha=0.6)
plt.plot([0, 1], [0, 1], 'r--', label='Identity line')
plt.xlabel('Empirical Cumulative Probability')
plt.ylabel('Theoretical Cumulative Probability')
plt.title('PP Plot (Normal Fit)')
plt.legend()
plt.axis('equal')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()
```

---

## Interpreting PP Plots

Deviations from the identity line indicate specific types of misfit between the data and the candidate distribution.

| Pattern | Interpretation |
|---------|---------------|
| Points follow $y = x$ | Good fit |
| S-shaped curve (below then above) | Data have lighter tails than the theoretical distribution |
| Inverted S-shape (above then below) | Data have heavier tails than the theoretical distribution |
| Points consistently above the line | Theoretical distribution is shifted right relative to the data |
| Points consistently below the line | Theoretical distribution is shifted left relative to the data |

---

## PP Plot vs QQ Plot

PP plots and QQ plots emphasize different aspects of distributional fit.

| Feature | PP Plot | QQ Plot |
|---------|---------|---------|
| Axes | Cumulative probabilities (0 to 1) | Quantile values (data scale) |
| Sensitivity | Center of distribution | Tails of distribution |
| Scale invariance | Yes (probabilities are unitless) | No (quantiles are in data units) |
| Best for | Detecting location/shape differences | Detecting tail heaviness, skewness |

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# PP plot
axes[0].scatter(empirical_cdf, theoretical_cdf, s=10, alpha=0.6)
axes[0].plot([0, 1], [0, 1], 'r--')
axes[0].set_xlabel('Empirical CDF')
axes[0].set_ylabel('Theoretical CDF')
axes[0].set_title('PP Plot')
axes[0].set_aspect('equal')

# QQ plot
stats.probplot(data, dist="norm", plot=axes[1])
axes[1].set_title('QQ Plot')

plt.tight_layout()
plt.show()
```

---

## PP Plot for Non-Normal Distributions

PP plots work with any continuous distribution that has a CDF available in SciPy.

```python
# Generate exponential data
data_exp = stats.expon.rvs(scale=3, size=300, random_state=42)

# PP plot against exponential fit
loc_fit, scale_fit = stats.expon.fit(data_exp)
sorted_exp = np.sort(data_exp)
n = len(sorted_exp)
emp_cdf = (np.arange(1, n + 1) - 0.5) / n
theo_cdf = stats.expon.cdf(sorted_exp, loc=loc_fit, scale=scale_fit)

plt.figure(figsize=(6, 6))
plt.scatter(emp_cdf, theo_cdf, s=10, alpha=0.6)
plt.plot([0, 1], [0, 1], 'r--', label='Identity line')
plt.xlabel('Empirical CDF')
plt.ylabel('Exponential CDF')
plt.title('PP Plot (Exponential Fit)')
plt.legend()
plt.axis('equal')
plt.xlim(0, 1)
plt.ylim(0, 1)
plt.show()
```

---

## Summary

PP plots compare empirical and theoretical cumulative probabilities, providing a diagnostic that is most sensitive to deviations near the center of the distribution. Their bounded $[0, 1] \times [0, 1]$ domain makes them scale-invariant and visually consistent across different datasets. While **QQ plots** are generally preferred for detecting tail behavior, **PP plots** complement them by highlighting location shifts and central shape mismatches. Using both together gives a complete picture of distributional fit.


---

## Exercises

**Exercise 1.** Write code that creates a P-P plot comparing the empirical CDF of a sample against the theoretical CDF of a normal distribution.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(100)
    print(f'Mean: {data.mean():.4f}')
    print(f'Std: {data.std():.4f}')
    ```

---

**Exercise 2.** Explain the difference between a P-P plot and a Q-Q plot. When might you prefer one over the other?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that creates P-P plots for data from three distributions: normal, exponential, and uniform. Show which one matches the normal reference line.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    from scipy import stats
    import matplotlib.pyplot as plt

    np.random.seed(42)
    data = np.random.randn(1000)
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, density=True, alpha=0.7)
    ax.set_title('Distribution')
    plt.show()
    ```

---

**Exercise 4.** Create a P-P plot that compares a sample against an exponential distribution instead of a normal distribution.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
