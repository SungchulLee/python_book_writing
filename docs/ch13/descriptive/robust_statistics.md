# Robust Statistics

Classical estimators like the sample mean and variance are optimal when data follow an exact parametric model, but even a single outlier can render them misleading. Robust statistics provides estimators that remain reliable under contamination, trading a small amount of efficiency under ideal conditions for stability when the data deviate from assumptions. This page covers the key robust estimators available in `scipy.stats`, including the median absolute deviation, trimmed and winsorized statistics, and the concept of breakdown point.

!!! tip "Mental Model"
    Robust estimators are built to survive contamination. The breakdown point tells you how many data points an adversary can corrupt before the estimator gives nonsense. The mean breaks after a single bad point (0% breakdown), while the median survives up to 50% corruption -- the price is a small loss of precision on clean data.

---

## Breakdown Point

The breakdown point of an estimator is the largest fraction of contaminated observations the estimator can tolerate before producing arbitrarily incorrect results. It formalizes the intuition of "how many bad data points can the estimator handle."

| Estimator | Breakdown Point |
|-----------|:--------------:|
| Sample mean | $0\%$ (a single outlier can shift it arbitrarily) |
| Sample median | $50\%$ |
| Trimmed mean ($\alpha$) | $\alpha$ |
| MAD | $50\%$ |
| Sample standard deviation | $0\%$ |

A higher breakdown point means greater robustness, but typically at the cost of statistical efficiency when the data are clean.

---

## Median Absolute Deviation (MAD)

The MAD is a robust measure of scale defined as the median of the absolute deviations from the median:

$$
\text{MAD} = \text{median}\bigl(|x_i - \tilde{x}|\bigr)
$$

where $\tilde{x} = \text{median}(x_1, \ldots, x_n)$.

To use MAD as an estimator of the standard deviation under normality, multiply by the consistency constant $1/\Phi^{-1}(3/4) \approx 1.4826$:

$$
\hat{\sigma}_{\text{MAD}} = 1.4826 \times \text{MAD}
$$

```python
import numpy as np
from scipy import stats

data = np.array([1.2, 1.5, 1.3, 1.4, 1.6, 1.3, 1.5, 10.0])  # 10.0 is an outlier

# MAD
mad = stats.median_abs_deviation(data)
print(f"MAD: {mad:.4f}")

# MAD-based sigma estimate (scale='normal' applies the 1.4826 factor)
mad_sigma = stats.median_abs_deviation(data, scale='normal')
print(f"MAD sigma estimate: {mad_sigma:.4f}")

# Compare with classical standard deviation
print(f"Sample std: {np.std(data, ddof=1):.4f}")
```

The classical standard deviation is heavily inflated by the outlier, while the MAD-based estimate remains stable.

---

## Trimmed Mean

The trimmed mean removes a fixed fraction $\alpha$ of observations from each tail before computing the mean. For a sample of size $n$ with $k = \lfloor \alpha n \rfloor$ observations trimmed from each end:

$$
\bar{x}_{\text{trim}} = \frac{1}{n - 2k} \sum_{i=k+1}^{n-k} x_{(i)}
$$

where $x_{(1)} \le x_{(2)} \le \cdots \le x_{(n)}$ are the order statistics. Setting $\alpha = 0$ recovers the ordinary mean; setting $\alpha = 0.5$ yields the median.

```python
# Trimmed mean with 10% cut from each tail
trimmed = stats.trim_mean(data, proportiontocut=0.1)
print(f"Trimmed mean (10%): {trimmed:.4f}")

# Compare
print(f"Ordinary mean: {np.mean(data):.4f}")
print(f"Median: {np.median(data):.4f}")
```

!!! tip "Choosing the Trimming Proportion"
    A common default is $\alpha = 0.1$ (10% from each tail), which protects against moderate contamination. For heavier contamination, $\alpha = 0.2$ or higher may be appropriate. The choice balances robustness against efficiency loss.

---

## Winsorized Statistics

Winsorization replaces extreme values with the nearest non-extreme value rather than removing them. This preserves the sample size. For a winsorization level $\alpha$, the $k = \lfloor \alpha n \rfloor$ smallest values are set to $x_{(k+1)}$ and the $k$ largest to $x_{(n-k)}$:

$$
x_i^{(W)} = \begin{cases}
x_{(k+1)} & \text{if } x_i \le x_{(k)} \\
x_i & \text{if } x_{(k)} < x_i < x_{(n-k+1)} \\
x_{(n-k)} & \text{if } x_i \ge x_{(n-k+1)}
\end{cases}
$$

```python
from scipy.stats.mstats import winsorize

# Winsorize 10% from each tail
data_wins = winsorize(data, limits=[0.1, 0.1])
print("Original:   ", data)
print("Winsorized: ", np.array(data_wins))
print(f"Winsorized mean: {np.mean(data_wins):.4f}")
```

---

## Trimmed Variance

The trimmed variance complements the trimmed mean by providing a robust measure of spread. SciPy provides `tvar` for computing variance within specified limits:

```python
# Variance computed only on the middle portion of data
lower, upper = np.percentile(data, [10, 90])
trimmed_var = stats.tvar(data, limits=(lower, upper))
print(f"Trimmed variance: {trimmed_var:.4f}")
print(f"Ordinary variance: {np.var(data, ddof=1):.4f}")
```

---

## Robust vs Classical Estimators

The following comparison illustrates the effect of outlier contamination on classical versus robust estimators:

```python
# Clean data from a normal distribution
np.random.seed(42)
clean = np.random.normal(loc=5.0, scale=1.0, size=100)

# Contaminated: replace 5% of values with outliers
contaminated = clean.copy()
contaminated[:5] = [50, -40, 60, -30, 45]

print("               Clean     Contaminated")
print(f"  Mean:       {np.mean(clean):8.3f}    {np.mean(contaminated):8.3f}")
print(f"  Median:     {np.median(clean):8.3f}    {np.median(contaminated):8.3f}")
print(f"  Std:        {np.std(clean, ddof=1):8.3f}    {np.std(contaminated, ddof=1):8.3f}")
print(f"  MAD sigma:  {stats.median_abs_deviation(clean, scale='normal'):8.3f}    "
      f"{stats.median_abs_deviation(contaminated, scale='normal'):8.3f}")
print(f"  Trim mean:  {stats.trim_mean(clean, 0.1):8.3f}    "
      f"{stats.trim_mean(contaminated, 0.1):8.3f}")
```

---

## Summary

Robust statistics provides estimators that resist the influence of outliers and model violations. The **median** and **MAD** achieve the maximum 50% breakdown point for location and scale estimation. **Trimmed means** offer a tunable compromise between robustness and efficiency through the trimming proportion $\alpha$. **Winsorization** caps extremes rather than removing them, preserving sample size. When data quality is uncertain, using robust estimators alongside classical ones reveals whether conclusions depend on a few influential observations.

---

## Exercises

**Exercise 1.**
Generate 100 normal samples ($\mu = 50$, $\sigma = 5$) and add 5 extreme outliers at value 200. Compare the mean vs trimmed mean (10% trim) and standard deviation vs MAD to show robustness.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = np.concatenate([np.random.normal(50, 5, 100), [200]*5])
        print(f"Mean:         {np.mean(data):.4f}")
        print(f"Trimmed mean: {stats.trim_mean(data, 0.1):.4f}")
        print(f"Std:          {np.std(data, ddof=1):.4f}")
        print(f"MAD:          {stats.median_abs_deviation(data):.4f}")

---

**Exercise 2.**
Compute the Winsorized mean and Winsorized variance of 200 samples from a $t$-distribution with 3 degrees of freedom using `scipy.stats.mstats.winsorize()`. Compare with the ordinary mean and variance.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats
        from scipy.stats.mstats import winsorize

        np.random.seed(42)
        data = stats.t.rvs(df=3, size=200)
        winsorized = winsorize(data, limits=[0.05, 0.05])
        print(f"Mean:           {np.mean(data):.4f}")
        print(f"Winsorized mean:{np.mean(winsorized):.4f}")
        print(f"Var:            {np.var(data, ddof=1):.4f}")
        print(f"Winsorized var: {np.var(winsorized, ddof=1):.4f}")

---

**Exercise 3.**
Using `scipy.stats.trim_mean()`, compute the trimmed mean at trim proportions 0%, 5%, 10%, 25%, and 50% (the median) for a dataset with heavy outliers. Show how the estimate becomes more stable as the trim proportion increases.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = np.concatenate([np.random.normal(10, 2, 90), [100, -80, 150, 200, -100]])
        for prop in [0.0, 0.05, 0.10, 0.25, 0.50]:
            tm = stats.trim_mean(data, prop)
            print(f"Trim {prop:.0%}: {tm:.4f}")
