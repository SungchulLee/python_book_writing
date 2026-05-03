# Percentiles and Quantiles

Describing a dataset by its mean and standard deviation captures only the center and spread. Percentiles and quantiles reveal the full shape of a distribution by specifying the value below which a given fraction of observations falls. These measures underpin box plots, confidence intervals, and many nonparametric methods. This page defines percentiles and quantiles formally, explains the interpolation methods used to compute them, and demonstrates their use with NumPy and SciPy.

!!! tip "Mental Model"
    A percentile answers the question "what value separates the bottom $k$% from the top?" Sort your data, walk $k$% of the way through, and read off the value. The median is the 50th percentile, quartiles split the data into fourths, and together these landmarks sketch the distribution's shape without any normality assumption.

---

## Definitions

### Quantile Function

For a random variable $X$ with cumulative distribution function $F(x) = P(X \le x)$, the quantile function is the generalized inverse

$$
Q(p) = \inf\{x \in \mathbb{R} : F(x) \ge p\}, \quad 0 < p < 1
$$

The value $Q(p)$ is called the $p$-th quantile (or $100p$-th percentile) of the distribution.

### Percentile

A percentile is a quantile expressed on a 0-to-100 scale. The $k$-th percentile is the value below which $k\%$ of the observations fall:

$$
P_k = Q\!\left(\frac{k}{100}\right), \quad 0 \le k \le 100
$$

### Common Named Quantiles

| Name | Quantile | Percentile |
|------|----------|------------|
| Median | $Q(0.5)$ | 50th |
| Quartiles | $Q(0.25),\; Q(0.5),\; Q(0.75)$ | 25th, 50th, 75th |
| Deciles | $Q(0.1),\; Q(0.2),\; \ldots,\; Q(0.9)$ | 10th, 20th, ..., 90th |

---

## Computing Quantiles from a Sample

Given an ordered sample $x_{(1)} \le x_{(2)} \le \cdots \le x_{(n)}$, the empirical quantile at probability $p$ typically requires interpolation because $np$ is not always an integer.

### Linear Interpolation (Default)

NumPy and SciPy use the following linear interpolation by default. For a desired probability $p$, compute the virtual index

$$
h = (n - 1)\,p + 1
$$

and interpolate between adjacent order statistics:

$$
\hat{Q}(p) = x_{(\lfloor h \rfloor)} + (h - \lfloor h \rfloor)\bigl(x_{(\lceil h \rceil)} - x_{(\lfloor h \rfloor)}\bigr)
$$

```python
import numpy as np
from scipy import stats

data = np.array([7, 15, 36, 39, 40, 41, 42, 43, 47, 49])

# Quartiles using default linear interpolation
q1, q2, q3 = np.percentile(data, [25, 50, 75])
print(f"Q1 = {q1}, Median = {q2}, Q3 = {q3}")

# Equivalent using np.quantile with fractions
print(np.quantile(data, [0.25, 0.50, 0.75]))
```

### Interpolation Methods

NumPy supports several interpolation strategies through the `method` parameter:

```python
p = 0.25

methods = ['linear', 'lower', 'higher', 'midpoint', 'nearest']
for m in methods:
    val = np.percentile(data, 25, method=m)
    print(f"  {m:10s}: Q1 = {val}")
```

| Method | Rule |
|--------|------|
| `linear` | Linear interpolation between adjacent order statistics |
| `lower` | Take the lower of the two bracketing values |
| `higher` | Take the higher of the two bracketing values |
| `midpoint` | Average of the lower and higher values |
| `nearest` | Take the nearest order statistic |

---

## Five-Number Summary

The five-number summary consists of the minimum, $Q_1$, median, $Q_3$, and maximum. Together with the interquartile range $\text{IQR} = Q_3 - Q_1$, these values provide a robust sketch of the data distribution.

```python
summary = np.percentile(data, [0, 25, 50, 75, 100])
labels = ['Min', 'Q1', 'Median', 'Q3', 'Max']
for label, val in zip(labels, summary):
    print(f"  {label:7s}: {val}")

# IQR
iqr = stats.iqr(data)
print(f"  IQR    : {iqr}")
```

---

## SciPy Quantile Functions

### scipy.stats.mstats.mquantiles

The `mquantiles` function supports multiple quantile estimation methods parametrized by plotting positions:

```python
from scipy.stats.mstats import mquantiles

# Default (Cunnane method, alphap=0.4, betap=0.4)
q = mquantiles(data, prob=[0.25, 0.5, 0.75])
print("Cunnane quartiles:", q)

# Hazen method (alphap=0.5, betap=0.5)
q_hazen = mquantiles(data, prob=[0.25, 0.5, 0.75],
                      alphap=0.5, betap=0.5)
print("Hazen quartiles:  ", q_hazen)
```

### scipy.stats.scoreatpercentile

```python
# Percentile score (older API, still available)
p90 = stats.scoreatpercentile(data, 90)
print(f"90th percentile: {p90}")

# Inverse: what percentile does a given value correspond to?
pct = stats.percentileofscore(data, 40)
print(f"Score 40 is at the {pct:.1f}th percentile")
```

---

## Percentile Ranks

The percentile rank of a value $v$ in a dataset is the percentage of observations that are less than or equal to $v$:

$$
R(v) = \frac{|\{i : x_i \le v\}|}{n} \times 100
$$

```python
# Percentile rank of specific values
for value in [30, 40, 50]:
    rank = stats.percentileofscore(data, value, kind='weak')
    print(f"  Value {value}: {rank:.1f}th percentile")
```

---

## Quantiles of Standard Distributions

For parametric distributions, the quantile function (percent point function) is available directly through the `.ppf()` method:

```python
# Normal distribution quantiles
z_90 = stats.norm.ppf(0.90)
z_95 = stats.norm.ppf(0.95)
z_975 = stats.norm.ppf(0.975)
print(f"Normal z-values: z_90={z_90:.4f}, z_95={z_95:.4f}, z_975={z_975:.4f}")

# t-distribution quantile (used in confidence intervals)
t_crit = stats.t.ppf(0.975, df=9)
print(f"t critical (df=9, 97.5%): {t_crit:.4f}")
```

---

## Summary

Percentiles and quantiles characterize how data values distribute across the range of observations. The **quantile function** $Q(p)$ generalizes the median to arbitrary probability levels, while **percentile ranks** perform the inverse mapping from values to probabilities. NumPy provides flexible computation with multiple interpolation methods, and SciPy extends this with `mquantiles` for alternative estimation approaches and `.ppf()` for theoretical distribution quantiles. These tools form the foundation for box plots, outlier fences, confidence intervals, and distribution diagnostics throughout statistical analysis.

---

## Exercises

**Exercise 1.**
Generate 200 samples from an exponential distribution with $\lambda = 0.5$. Compute the 10th, 25th, 50th, 75th, and 90th percentiles. Compare the 50th percentile with `np.median()`.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.expon.rvs(scale=2, size=200)
        percs = np.percentile(data, [10, 25, 50, 75, 90])
        print(f"Percentiles: {percs.round(4)}")
        print(f"Median (np.median): {np.median(data):.4f}")
        print(f"50th percentile:    {percs[2]:.4f}")

---

**Exercise 2.**
Compute the five-number summary (min, Q1, median, Q3, max) for 300 samples from a $t$-distribution with 5 degrees of freedom. Compute the IQR and identify the lower and upper fence values for outlier detection.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.t.rvs(df=5, size=300)
        q1, median, q3 = np.percentile(data, [25, 50, 75])
        iqr = q3 - q1
        lower_fence = q1 - 1.5 * iqr
        upper_fence = q3 + 1.5 * iqr
        print(f"Five-number: {data.min():.3f}, {q1:.3f}, {median:.3f}, {q3:.3f}, {data.max():.3f}")
        print(f"IQR: {iqr:.3f}, Fences: [{lower_fence:.3f}, {upper_fence:.3f}]")

---

**Exercise 3.**
Compare the `linear` and `lower` interpolation methods in `np.percentile()` for a small dataset of 10 values. Show that the methods produce different results for quantiles that fall between observed values.

??? success "Solution to Exercise 3"

        import numpy as np

        data = np.array([2, 5, 7, 8, 12, 15, 18, 22, 25, 30])
        for method in ['linear', 'lower']:
            p = np.percentile(data, 37, interpolation=method)
            print(f"37th percentile ({method}): {p}")
