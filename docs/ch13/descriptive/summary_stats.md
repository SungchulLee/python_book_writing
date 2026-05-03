# Summary Statistics

Summary statistics provide concise descriptions of data distributions using measures of central tendency, spread, and shape computed efficiently with scipy.stats functions.

!!! tip "Mental Model"
    Summary statistics compress an entire dataset into a handful of numbers. The mean, median, and mode tell you where the data clusters; the variance and IQR tell you how far it spreads; and skewness and kurtosis tell you how its shape deviates from a symmetric bell curve.

---

## Central Tendency

### 1. Mean

```python
import numpy as np
from scipy import stats

data = [23, 25, 27, 24, 26, 22, 28, 25, 24, 26]

# Arithmetic mean
print(np.mean(data))  # 25.0
print(stats.tmean(data))  # Same, but can trim

# Trimmed mean (exclude outliers)
print(stats.tmean(data, limits=(23, 27)))  # Exclude <23 or >27
```

### 2. Median

```python
# 50th percentile
print(np.median(data))  # 25.0

# More robust than mean to outliers
data_with_outlier = data + [100]
print(np.mean(data_with_outlier))    # 31.82 (pulled up)
print(np.median(data_with_outlier))  # 25.0 (stable)
```

### 3. Mode

```python
# Most frequent value
mode_result = stats.mode(data, keepdims=True)
print(f"Mode: {mode_result.mode[0]}, Count: {mode_result.count[0]}")

# For continuous data, use binning
continuous_data = np.random.normal(0, 1, 1000)
hist, bin_edges = np.histogram(continuous_data, bins=30)
mode_bin = bin_edges[np.argmax(hist)]
```

### 4. Geometric Mean

```python
# Useful for growth rates, ratios
returns = [1.1, 1.05, 0.95, 1.08, 1.12]  # Return factors
geom_mean = stats.gmean(returns)
print(f"Geometric mean: {geom_mean:.4f}")  # 1.0582

# Equivalent to
print(np.prod(returns)**(1/len(returns)))
```

### 5. Harmonic Mean

```python
# Useful for rates, speeds
speeds = [60, 40, 50]  # km/h for equal distances
harm_mean = stats.hmean(speeds)
print(f"Harmonic mean: {harm_mean:.2f}")  # 48.65 km/h average
```

### 6. Trimmed Mean

```python
# Exclude extreme values
data = np.array([1, 2, 3, 4, 5, 100])  # Outlier at 100

# Trim 20% from each tail
trimmed = stats.trim_mean(data, proportiontocut=0.2)
print(f"Trimmed mean: {trimmed:.2f}")  # More robust
```

### 7. Weighted Mean

```python
# Different weights for observations
values = [10, 20, 30, 40]
weights = [1, 2, 3, 4]  # Last observation more important

weighted_mean = np.average(values, weights=weights)
print(f"Weighted mean: {weighted_mean}")  # 30.0
```

---

## Measures of Spread

### 1. Variance

```python
# Sample variance (Bessel correction)
print(np.var(data, ddof=1))  # Unbiased estimator
print(stats.tvar(data))      # Same

# Population variance
print(np.var(data, ddof=0))
```

### 2. Standard Deviation

```python
print(np.std(data, ddof=1))  # Sample std

# Interpretation: ~68% within 1σ, ~95% within 2σ
```

### 3. Range

```python
data_range = np.ptp(data)  # Peak-to-peak
print(f"Range: {data_range}")

# Or manually
print(f"Range: {np.max(data) - np.min(data)}")
```

### 4. Interquartile Range (IQR)

```python
q75, q25 = np.percentile(data, [75, 25])
iqr = q75 - q25
print(f"IQR: {iqr}")

# Using scipy
print(stats.iqr(data))

# Outlier detection: values beyond 1.5*IQR from quartiles
lower_fence = q25 - 1.5 * iqr
upper_fence = q75 + 1.5 * iqr
outliers = [x for x in data if x < lower_fence or x > upper_fence]
```

### 5. Mean Absolute Deviation

```python
# Average absolute deviation from mean
mad_mean = np.mean(np.abs(data - np.mean(data)))
print(f"MAD (from mean): {mad_mean:.2f}")

# From median (more robust)
mad_median = stats.median_abs_deviation(data)
print(f"MAD (from median): {mad_median:.2f}")
```

### 6. Standard Error

```python
# Standard error of mean
se = stats.sem(data)
print(f"SE: {se:.3f}")

# Equivalent to
print(np.std(data, ddof=1) / np.sqrt(len(data)))

# Used for confidence intervals
```

### 7. Coefficient of Variation

```python
# Relative variability (std/mean)
cv = stats.variation(data)
print(f"CV: {cv:.3f}")

# Equivalent to
print(np.std(data, ddof=1) / np.mean(data))

# Useful for comparing variability across different scales
```

---

## Quantiles

### 1. Percentiles

```python
# Specific percentiles
print(np.percentile(data, 25))   # Q1
print(np.percentile(data, 50))   # Median
print(np.percentile(data, 75))   # Q3

# Multiple at once
percentiles = np.percentile(data, [25, 50, 75])
```

### 2. Quartiles

```python
# Using mquantiles
quartiles = stats.mstats.mquantiles(data, prob=[0.25, 0.5, 0.75])
print(f"Q1: {quartiles[0]}, Q2: {quartiles[1]}, Q3: {quartiles[2]}")
```

### 3. Deciles

```python
# 10 equal groups
deciles = np.percentile(data, np.arange(10, 100, 10))
print("Deciles:", deciles)
```

### 4. Quantile Function

```python
# Custom quantiles
quantiles = np.quantile(data, [0.1, 0.9])  # 10th and 90th
print(f"80% central range: [{quantiles[0]}, {quantiles[1]}]")
```

### 5. Five-Number Summary

```python
# Min, Q1, Median, Q3, Max
summary = [np.min(data), *np.percentile(data, [25, 50, 75]), np.max(data)]
print(f"Five-number summary: {summary}")

# Or use describe
print(stats.describe(data))
```

### 6. Confidence Intervals

```python
# CI for mean
mean = np.mean(data)
se = stats.sem(data)
ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=se)
print(f"95% CI: [{ci[0]:.2f}, {ci[1]:.2f}]")
```

### 7. Bootstrap Percentiles

```python
# Bootstrap confidence intervals
n_boot = 1000
boot_means = []

for _ in range(n_boot):
    sample = np.random.choice(data, size=len(data), replace=True)
    boot_means.append(np.mean(sample))

ci_boot = np.percentile(boot_means, [2.5, 97.5])
print(f"Bootstrap 95% CI: {ci_boot}")
```

---

## Describe Functions

### 1. describe()

```python
# Comprehensive summary
desc = stats.describe(data)
print(f"n: {desc.nobs}")
print(f"Min/Max: ({desc.minmax[0]}, {desc.minmax[1]})")
print(f"Mean: {desc.mean:.2f}")
print(f"Variance: {desc.variance:.2f}")
print(f"Skewness: {desc.skewness:.2f}")
print(f"Kurtosis: {desc.kurtosis:.2f}")
```

### 2. describe with NaN

```python
# Handle missing values
data_with_nan = np.array([1, 2, np.nan, 4, 5])
desc = stats.describe(data_with_nan, nan_policy='omit')
print(desc)
```

### 3. Pandas describe()

```python
import pandas as pd

df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [10, 20, 30, 40, 50]
})

print(df.describe())
# Shows count, mean, std, min, 25%, 50%, 75%, max
```

### 4. describeby()

```python
# Not in scipy, but useful pattern
groups = np.array([0, 0, 1, 1, 1])
data_arr = np.array([10, 15, 20, 25, 30])

for g in [0, 1]:
    group_data = data_arr[groups == g]
    print(f"Group {g}: mean={np.mean(group_data):.1f}")
```

### 5. Summary Statistics Table

```python
# Create summary table
summary_stats = {
    'Mean': np.mean(data),
    'Median': np.median(data),
    'Std': np.std(data, ddof=1),
    'Min': np.min(data),
    'Max': np.max(data),
    'Q1': np.percentile(data, 25),
    'Q3': np.percentile(data, 75),
    'IQR': stats.iqr(data)
}

for stat, value in summary_stats.items():
    print(f"{stat:10s}: {value:.2f}")
```

### 6. Binned Statistics

```python
# Statistics within bins
x = np.random.randn(1000)
y = x**2 + np.random.randn(1000) * 0.5

# Mean y within x bins
bin_means, bin_edges, binnumber = stats.binned_statistic(
    x, y, statistic='mean', bins=10
)
print("Bin means:", bin_means)
```

### 7. Multi-dimensional Statistics

```python
# For 2D data
data_2d = np.random.randn(100, 5)

# Column-wise statistics
print("Means:", np.mean(data_2d, axis=0))
print("Stds:", np.std(data_2d, axis=0, ddof=1))

# Row-wise
print("Row means:", np.mean(data_2d, axis=1))
```

---

## Robust Statistics

### 1. Median Absolute Deviation

```python
# Robust measure of spread
mad = stats.median_abs_deviation(data)
print(f"MAD: {mad:.2f}")

# Scaling factor for normal consistency
mad_scaled = mad * 1.4826  # Estimates σ
print(f"MAD (σ estimate): {mad_scaled:.2f}")
```

### 2. Trimmed Statistics

```python
# Trim proportion from each tail
trimmed_mean = stats.trim_mean(data, 0.1)  # Remove 10% from each tail
trimmed_var = stats.tvar(data, limits=(np.percentile(data, 10),
                                        np.percentile(data, 90)))
```

### 3. Winsorized Statistics

```python
# Cap extreme values instead of removing
from scipy.stats.mstats import winsorize

data_wins = winsorize(data, limits=[0.1, 0.1])  # Cap at 10th/90th percentiles
print("Winsorized mean:", np.mean(data_wins))
```

### 4. Biweight Midvariance

```python
# Robust variance estimator (less sensitive to outliers)
# Not directly in scipy, but conceptually important
```

### 5. Hodges-Lehmann Estimator

```python
# Median of pairwise averages (robust location)
from itertools import combinations

pairwise_avgs = [(a + b) / 2 for a, b in combinations(data, 2)]
hl_estimator = np.median(pairwise_avgs)
print(f"Hodges-Lehmann estimator: {hl_estimator:.2f}")
```

### 6. Q-Q Plot

```python
# Visual check for normality
stats.probplot(data, dist="norm", plot=plt)
plt.title("Q-Q Plot")
plt.show()
```

### 7. Outlier Detection

```python
# Z-score method
z_scores = np.abs(stats.zscore(data))
outliers_zscore = data[z_scores > 3]

# IQR method
q1, q3 = np.percentile(data, [25, 75])
iqr = q3 - q1
outliers_iqr = data[(data < q1 - 1.5*iqr) | (data > q3 + 1.5*iqr)]

print(f"Outliers (Z-score): {outliers_zscore}")
print(f"Outliers (IQR): {outliers_iqr}")
```

---

## Summary

**Central tendency:**
- Mean: Average value (sensitive to outliers)
- Median: Middle value (robust)
- Mode: Most frequent (for categorical/discrete)

**Spread:**
- Std: Average deviation from mean
- IQR: Range of middle 50% (robust)
- MAD: Median absolute deviation (very robust)

**Key insight:** Summary statistics reduce data to key numerical values, with robust measures (median, MAD, IQR) preferred when outliers are present, while classical measures (mean, std) are more efficient for clean, normally-distributed data.

---

## Exercises

**Exercise 1.**
Generate 200 samples from a gamma distribution with shape 3 and scale 2. Compute the mean, median, standard deviation, and IQR using NumPy and SciPy functions.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.gamma.rvs(a=3, scale=2, size=200)
        print(f"Mean:   {np.mean(data):.4f}")
        print(f"Median: {np.median(data):.4f}")
        print(f"Std:    {np.std(data, ddof=1):.4f}")
        print(f"IQR:    {np.percentile(data, 75) - np.percentile(data, 25):.4f}")

---

**Exercise 2.**
Use `scipy.stats.describe()` on an array of 500 standard normal samples. Print all returned fields (nobs, minmax, mean, variance, skewness, kurtosis) and interpret each.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = np.random.normal(size=500)
        result = stats.describe(data)
        print(f"nobs:     {result.nobs}")
        print(f"minmax:   {result.minmax}")
        print(f"mean:     {result.mean:.4f}")
        print(f"variance: {result.variance:.4f}")
        print(f"skewness: {result.skewness:.4f}")
        print(f"kurtosis: {result.kurtosis:.4f}")

---

**Exercise 3.**
Create two datasets: one from a normal distribution and one from an exponential distribution (both with 300 samples). Compare their `describe()` outputs and identify which statistics reveal the difference in distribution shape.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        normal_data = np.random.normal(5, 2, size=300)
        exp_data = np.random.exponential(5, size=300)

        for name, data in [("Normal", normal_data), ("Exponential", exp_data)]:
            d = stats.describe(data)
            print(f"{name}: skew={d.skewness:.3f}, kurt={d.kurtosis:.3f}")
