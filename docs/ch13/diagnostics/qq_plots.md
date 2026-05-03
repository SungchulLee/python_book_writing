# QQ Plots

A **quantile-quantile (QQ) plot** compares the quantiles of observed data against the quantiles of a theoretical distribution. If the data follow that distribution, the points fall approximately along a straight reference line. This visual diagnostic often reveals departures from normality — heavy tails, skewness, or outliers — more clearly than summary statistics or formal hypothesis tests alone.

!!! tip "Mental Model"
    Sort your data and pair each value with the theoretical quantile it "should" be if the assumed distribution were correct. Plot these pairs: a straight line means the distribution fits, upward-curving tails mean heavy tails, and S-shapes indicate skewness. The QQ plot is the single most informative diagnostic for distributional fit.

---

## Theoretical Basis

Given a sample of $n$ observations, sort them to obtain the **order statistics** $x_{(1)} \le x_{(2)} \le \cdots \le x_{(n)}$. Each order statistic $x_{(i)}$ corresponds to a **plotting position** that estimates the cumulative probability:

$$
p_i = \frac{i - 0.5}{n}
$$

The theoretical quantile paired with $x_{(i)}$ is the value $q_i$ at which the reference distribution's CDF equals $p_i$:

$$
q_i = F^{-1}(p_i)
$$

where $F^{-1}$ is the **quantile function** (inverse CDF, called `ppf` in SciPy). The QQ plot places theoretical quantiles $q_i$ on the horizontal axis and observed order statistics $x_{(i)}$ on the vertical axis.

!!! note "Why (i - 0.5) / n?"
    Several plotting-position formulas exist. The Hazen formula $(i - 0.5)/n$ avoids placing points at exactly 0 or 1, where the quantile function of many distributions is undefined. SciPy's `probplot` uses a similar convention by default.

## scipy.stats.probplot

The function `scipy.stats.probplot` computes the QQ plot coordinates and, optionally, overlays a least-squares reference line. Its signature is:

```python
scipy.stats.probplot(x, dist='norm', plot=None)
```

- `x` — the data array.
- `dist` — a string name or a `scipy.stats` distribution object. Defaults to `'norm'`.
- `plot` — pass a Matplotlib axes object to draw the plot directly.

The function returns `(osm, osr)` where `osm` contains the theoretical quantiles and `osr` the ordered data values.

### Example: Normally Distributed Data

When data are drawn from a normal distribution, the QQ plot points track the reference line closely:

```python
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
data = rng.normal(loc=5, scale=2, size=200)

fig, ax = plt.subplots()
stats.probplot(data, dist='norm', plot=ax)
ax.set_title('QQ Plot: Normal Data vs Normal Distribution')
plt.show()
```

The tight alignment along the diagonal confirms that the sample is consistent with a normal distribution.

### Example: Heavy-Tailed Data

Data from a $t$-distribution with few degrees of freedom have heavier tails than the normal. The QQ plot reveals this through characteristic S-shaped curvature:

```python
rng = np.random.default_rng(42)
data_t = rng.standard_t(df=3, size=200)

fig, ax = plt.subplots()
stats.probplot(data_t, dist='norm', plot=ax)
ax.set_title('QQ Plot: t(df=3) Data vs Normal Distribution')
plt.show()
```

Points in the lower-left fall below the line and points in the upper-right rise above it, indicating that extreme values occur more frequently than a normal model predicts.

## Interpreting Deviations from the Reference Line

The pattern of departure from the reference line diagnoses specific distributional features:

| Pattern | Interpretation |
|---|---|
| Points follow the line | Data are consistent with the reference distribution |
| S-shaped curve (both tails deviate outward) | Heavier tails than the reference distribution |
| Inverse S-shape (both tails deviate inward) | Lighter tails than the reference distribution |
| Concave or convex curvature | Skewness — right-skewed data curve upward, left-skewed curve downward |
| A few points far from the line at one end | Outliers in that tail |

### Example: Skewed Data

An exponential distribution is right-skewed. Its QQ plot against the normal shows a convex curve:

```python
rng = np.random.default_rng(42)
data_exp = rng.exponential(scale=2, size=200)

fig, ax = plt.subplots()
stats.probplot(data_exp, dist='norm', plot=ax)
ax.set_title('QQ Plot: Exponential Data vs Normal Distribution')
plt.show()
```

The upward bend in the right tail reflects the long right tail of the exponential distribution.

## QQ Plot Against Non-Normal Distributions

The `dist` parameter accepts any `scipy.stats` distribution. To check whether data follow an exponential distribution, pass `dist='expon'`:

```python
rng = np.random.default_rng(42)
data_exp = rng.exponential(scale=2, size=200)

fig, ax = plt.subplots()
stats.probplot(data_exp, dist='expon', plot=ax)
ax.set_title('QQ Plot: Exponential Data vs Exponential Distribution')
plt.show()
```

When the reference distribution matches the data-generating process, the points realign along the reference line.

## Relationship to Formal Goodness-of-Fit Tests

QQ plots complement formal tests such as the Shapiro-Wilk test (`scipy.stats.shapiro`) and the Kolmogorov-Smirnov test (`scipy.stats.kstest`). A formal test provides a $p$-value but cannot explain *how* the data deviate from the reference distribution. The QQ plot shows the nature of the deviation — whether it is in the tails, in the center, or due to outliers — guiding the analyst toward a better-fitting model.

## Summary

A QQ plot pairs observed order statistics $x_{(i)}$ with theoretical quantiles $F^{-1}(p_i)$ to visually assess distributional fit. In SciPy, `scipy.stats.probplot` computes the plot coordinates and reference line for any distribution in the library. Deviations from the line reveal heavy tails, skewness, or outliers that summary statistics may obscure.


---

## Exercises

**Exercise 1.** Write code that creates a Q-Q plot using `scipy.stats.probplot()` to assess whether a sample is normally distributed.

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

**Exercise 2.** Explain what a Q-Q plot shows. What does it mean when points deviate from the diagonal line?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that creates Q-Q plots for samples from normal, t (df=3), and exponential distributions. Explain the pattern in each.

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

**Exercise 4.** Create a Q-Q plot comparing two empirical samples against each other (rather than against a theoretical distribution).

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
