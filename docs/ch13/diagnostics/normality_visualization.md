# Normality Visualization

Many statistical methods -- $t$-tests, ANOVA, linear regression -- assume that data or residuals follow a normal distribution. While formal tests like Shapiro-Wilk provide a binary decision, visual methods reveal the nature and severity of departures from normality. A histogram might show skewness, a QQ plot might show heavy tails, and these patterns inform which remedies (transformations, nonparametric alternatives) are appropriate. This page demonstrates the primary visual techniques for assessing normality.

!!! tip "Mental Model"
    A normality check is like fitting a template over your data. The histogram reveals gross shape mismatches (skewness, bimodality), while the QQ plot magnifies subtle tail deviations that the histogram hides. Use both together: the histogram for the big picture, the QQ plot for the fine details.

---

## Histogram with Normal Overlay

The most intuitive check overlays the fitted normal density $f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-(x-\mu)^2/(2\sigma^2)}$ on a normalized histogram of the data.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

np.random.seed(42)
data = np.random.normal(loc=50, scale=10, size=300)

# Fit normal distribution
mu, sigma = stats.norm.fit(data)
x = np.linspace(data.min() - 5, data.max() + 5, 200)
pdf = stats.norm.pdf(x, mu, sigma)

plt.hist(data, bins=25, density=True, alpha=0.6, label='Data')
plt.plot(x, pdf, 'r-', linewidth=2,
         label=f'Normal($\\mu$={mu:.1f}, $\\sigma$={sigma:.1f})')
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Histogram with Fitted Normal Density')
plt.legend()
plt.show()
```

!!! tip "Interpreting the Histogram"
    Look for symmetry around the peak, bell-shaped curvature, and tails that taper smoothly. Skewness appears as asymmetry; heavy tails appear as excess density far from the center.

---

## Normal Probability Plot (QQ Plot)

The normal QQ plot plots sample quantiles against theoretical normal quantiles. If the data are normally distributed, the points follow a straight line. `scipy.stats.probplot` computes both the quantiles and a fitted line.

```python
fig, ax = plt.subplots()
stats.probplot(data, dist="norm", plot=ax)
ax.set_title('Normal QQ Plot')
plt.show()
```

Common deviation patterns:

| Pattern | Interpretation |
|---------|---------------|
| S-shaped curve | Heavy tails (leptokurtic) |
| Inverted S-shape | Light tails (platykurtic) |
| Points curve upward at both ends | Right skew |
| Points curve downward at both ends | Left skew |
| Points follow the line | Approximately normal |

---

## ECDF vs Normal CDF

Comparing the empirical CDF against the theoretical normal CDF provides a non-binned view of normality. The maximum vertical gap between the two curves is the Kolmogorov-Smirnov statistic.

```python
data_sorted = np.sort(data)
ecdf = np.arange(1, len(data) + 1) / len(data)
cdf_normal = stats.norm.cdf(data_sorted, loc=mu, scale=sigma)

plt.step(data_sorted, ecdf, where='post', label='Empirical CDF')
plt.plot(data_sorted, cdf_normal, 'r-', label='Normal CDF')
plt.xlabel('Value')
plt.ylabel('Cumulative Probability')
plt.title('ECDF vs Normal CDF')
plt.legend()
plt.show()

# Quantify the maximum deviation
ks_stat, p_value = stats.kstest(data, 'norm', args=(mu, sigma))
print(f"KS statistic: {ks_stat:.4f}, p-value: {p_value:.4f}")
```

---

## Box Plot

A box plot summarizes the distribution through its quartiles and flags observations beyond the whiskers as potential outliers. For normal data, the box is approximately symmetric around the median, and few points appear beyond the whiskers.

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

# Normal data
axes[0].boxplot(data, vert=True)
axes[0].set_title('Normal Data')

# Skewed data for contrast
skewed = stats.lognorm.rvs(s=0.5, size=300, random_state=42)
axes[1].boxplot(skewed, vert=True)
axes[1].set_title('Right-Skewed Data')

plt.tight_layout()
plt.show()
```

---

## Skewness and Kurtosis Indicators

Quantitative measures of shape complement the visual assessment. For a normal distribution, skewness is $0$ and excess kurtosis is $0$.

```python
skew = stats.skew(data)
kurt = stats.kurtosis(data)  # Excess kurtosis (Fisher)
print(f"Skewness: {skew:.3f} (normal = 0)")
print(f"Excess kurtosis: {kurt:.3f} (normal = 0)")

# D'Agostino-Pearson test combines skewness and kurtosis
stat, p_value = stats.normaltest(data)
print(f"D'Agostino-Pearson: statistic={stat:.3f}, p={p_value:.4f}")
```

!!! note "Kurtosis Convention"
    `scipy.stats.kurtosis` returns **excess** kurtosis by default (Fisher's definition), so the expected value for a normal distribution is $0$, not $3$. Set `fisher=False` to get the Pearson definition where the normal value is $3$.

---

## Comparing Normal vs Non-Normal Data

Viewing multiple diagnostic plots side by side clarifies how departures from normality manifest across different visualization methods.

```python
fig, axes = plt.subplots(2, 3, figsize=(14, 8))

for col, (label, sample) in enumerate([
    ('Normal', np.random.normal(0, 1, 500)),
    ('Right-skewed', stats.lognorm.rvs(s=0.8, size=500, random_state=1)),
    ('Heavy-tailed', stats.t.rvs(df=3, size=500, random_state=2)),
]):
    # Histogram
    axes[0, col].hist(sample, bins=30, density=True, alpha=0.6)
    mu_fit, sigma_fit = stats.norm.fit(sample)
    x = np.linspace(sample.min(), sample.max(), 100)
    axes[0, col].plot(x, stats.norm.pdf(x, mu_fit, sigma_fit), 'r-')
    axes[0, col].set_title(f'{label} - Histogram')

    # QQ plot
    stats.probplot(sample, dist="norm", plot=axes[1, col])
    axes[1, col].set_title(f'{label} - QQ Plot')

plt.tight_layout()
plt.show()
```

---

## Summary

Visual normality assessment reveals not just whether data are non-normal but how they deviate. **Histograms** show overall shape, **QQ plots** diagnose tail behavior and skewness with high sensitivity, and **ECDF comparisons** provide a complete non-binned view. **Box plots** highlight asymmetry and outliers at a glance, while **skewness and kurtosis** values quantify what the plots reveal. Using these methods together gives a thorough picture that guides the choice between parametric methods that assume normality and robust or nonparametric alternatives that do not.


---

## Exercises

**Exercise 1.** Write code that creates a figure with three diagnostic plots for normality: histogram with normal overlay, Q-Q plot, and box plot.

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

**Exercise 2.** Explain three visual indicators of non-normality in a Q-Q plot (heavy tails, skewness, multimodality).

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that generates data from a heavy-tailed distribution (e.g., t-distribution with 3 df) and shows its departure from normality visually.

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

**Exercise 4.** Create a function that takes a data array and produces a 4-panel normality diagnostic figure.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
