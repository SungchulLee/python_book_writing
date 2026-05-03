# Outlier Detection

A single anomalous observation can shift the sample mean by several standard deviations, inflate variance estimates, and distort regression coefficients. Identifying such outliers before analysis protects downstream inferences. This page covers the main statistical methods for detecting outliers using `scipy.stats` and NumPy, progressing from simple threshold rules to formal hypothesis tests.

!!! tip "Mental Model"
    An outlier is a data point that does not belong to the same generating process as the rest. Detection methods ask "how surprising is this point under the assumed model?" The catch is that outliers contaminate the very statistics (mean, standard deviation) used to detect them, so robust methods like the MAD-based Z-score break this circular dependency.

---

## Z-Score Method

The Z-score measures how many standard deviations an observation lies from the sample mean. For a dataset $x_1, x_2, \ldots, x_n$ with sample mean $\bar{x}$ and sample standard deviation $s$, the Z-score of observation $x_i$ is

$$
z_i = \frac{x_i - \bar{x}}{s}
$$

Observations with $|z_i| > 3$ are commonly flagged as outliers under the assumption of approximate normality.

```python
import numpy as np
from scipy import stats

data = np.array([12, 14, 13, 15, 14, 100, 13, 14, 12, 15])

z_scores = stats.zscore(data)
print("Z-scores:", np.round(z_scores, 2))

# Flag observations beyond 3 standard deviations
outliers = data[np.abs(z_scores) > 3]
print(f"Outliers (|z| > 3): {outliers}")
```

!!! warning "Sensitivity to Masking"
    The Z-score method uses the mean and standard deviation, both of which are themselves affected by outliers. A single extreme value inflates $s$, which can mask other outliers by shrinking their Z-scores. For datasets with multiple outliers, consider the modified Z-score method below.

---

## Modified Z-Score (MAD-Based)

The modified Z-score replaces the mean with the median and the standard deviation with the median absolute deviation (MAD), producing a robust alternative. For observation $x_i$, the modified Z-score is

$$
M_i = \frac{0.6745 \,(x_i - \tilde{x})}{\text{MAD}}
$$

where $\tilde{x}$ is the sample median and

$$
\text{MAD} = \text{median}(|x_i - \tilde{x}|)
$$

The constant $0.6745$ is the 75th percentile of the standard normal distribution, chosen so that MAD estimates the standard deviation consistently under normality. Observations with $|M_i| > 3.5$ are flagged as outliers.

```python
median = np.median(data)
mad = stats.median_abs_deviation(data)

modified_z = 0.6745 * (data - median) / mad
print("Modified Z-scores:", np.round(modified_z, 2))

outliers_mad = data[np.abs(modified_z) > 3.5]
print(f"Outliers (|M| > 3.5): {outliers_mad}")
```

---

## IQR Method

The interquartile range (IQR) method defines outlier boundaries using the first quartile $Q_1$ and third quartile $Q_3$. The IQR is

$$
\text{IQR} = Q_3 - Q_1
$$

An observation $x_i$ is classified as an outlier if

$$
x_i < Q_1 - 1.5 \times \text{IQR} \quad \text{or} \quad x_i > Q_3 + 1.5 \times \text{IQR}
$$

The multiplier $1.5$ identifies mild outliers. Replacing it with $3.0$ targets extreme outliers only.

```python
q1, q3 = np.percentile(data, [25, 75])
iqr = stats.iqr(data)

lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

outliers_iqr = data[(data < lower_fence) | (data > upper_fence)]
print(f"Q1: {q1}, Q3: {q3}, IQR: {iqr}")
print(f"Fences: [{lower_fence:.1f}, {upper_fence:.1f}]")
print(f"Outliers (IQR): {outliers_iqr}")
```

!!! tip "Why 1.5 Times the IQR"
    For a normal distribution, the interval $[Q_1 - 1.5 \times \text{IQR},\; Q_3 + 1.5 \times \text{IQR}]$ captures approximately 99.3% of the data. The 1.5 multiplier therefore flags roughly the most extreme 0.7% of observations under normality.

---

## Grubbs' Test

Grubbs' test is a formal hypothesis test for detecting a single outlier in a univariate dataset assumed to come from a normal distribution. The test statistic is

$$
G = \frac{\max_i |x_i - \bar{x}|}{s}
$$

Under $H_0$ (no outliers), the critical value at significance level $\alpha$ for sample size $n$ is

$$
G_{\text{crit}} = \frac{n - 1}{\sqrt{n}} \sqrt{\frac{t_{\alpha/(2n),\, n-2}^2}{n - 2 + t_{\alpha/(2n),\, n-2}^2}}
$$

where $t_{\alpha/(2n),\, n-2}$ is the critical value of the $t$-distribution with $n - 2$ degrees of freedom.

```python
def grubbs_test(data, alpha=0.05):
    """Perform Grubbs' test for a single outlier."""
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)

    # Test statistic
    abs_deviations = np.abs(data - mean)
    G = np.max(abs_deviations) / std
    suspect_idx = np.argmax(abs_deviations)

    # Critical value
    t_crit = stats.t.ppf(1 - alpha / (2 * n), n - 2)
    G_crit = (n - 1) / np.sqrt(n) * np.sqrt(t_crit**2 / (n - 2 + t_crit**2))

    is_outlier = G > G_crit
    return data[suspect_idx], G, G_crit, is_outlier

value, G, G_crit, is_outlier = grubbs_test(data)
print(f"Suspect value: {value}")
print(f"G = {G:.3f}, G_crit = {G_crit:.3f}")
print(f"Outlier detected: {is_outlier}")
```

!!! warning "Single Outlier Assumption"
    Grubbs' test detects at most one outlier per application. To check for multiple outliers, apply the test iteratively: remove the detected outlier, then re-test the reduced dataset. Stop when the test no longer rejects $H_0$.

---

## Percentile-Based Clipping

Percentile-based clipping caps or removes observations beyond specified percentile thresholds. Unlike the IQR method, it does not assume symmetry and works directly with empirical quantiles.

```python
# Winsorize: cap extremes at 5th and 95th percentiles
from scipy.stats.mstats import winsorize

data_winsorized = winsorize(data, limits=[0.05, 0.05])
print("Original: ", data)
print("Winsorized:", data_winsorized)

# Trim: remove observations beyond thresholds
lower, upper = np.percentile(data, [5, 95])
data_trimmed = data[(data >= lower) & (data <= upper)]
print("Trimmed:  ", data_trimmed)
```

---

## Comparing Methods

Each method has different strengths depending on the data characteristics.

| Method | Assumes Normality | Robust to Multiple Outliers | Formal Test |
|--------|:-----------------:|:---------------------------:|:-----------:|
| Z-score | Yes | No | No |
| Modified Z-score | No | Yes | No |
| IQR | No | Yes | No |
| Grubbs' test | Yes | No | Yes |
| Percentile clipping | No | Yes | No |

```python
# Side-by-side comparison on the same dataset
data = np.array([12, 14, 13, 15, 14, 100, 13, 14, 12, 15])

# Z-score
z = stats.zscore(data)
print("Z-score outliers:     ", data[np.abs(z) > 3])

# Modified Z-score
med = np.median(data)
mad = stats.median_abs_deviation(data)
mz = 0.6745 * (data - med) / mad
print("Modified Z outliers:  ", data[np.abs(mz) > 3.5])

# IQR
q1, q3 = np.percentile(data, [25, 75])
iqr = q3 - q1
print("IQR outliers:         ",
      data[(data < q1 - 1.5*iqr) | (data > q3 + 1.5*iqr)])
```

---

## Summary

Outlier detection protects statistical analyses from the disproportionate influence of anomalous observations. The **Z-score method** offers simplicity but is sensitive to the very outliers it seeks to find. The **modified Z-score** using MAD provides robustness against masking effects. The **IQR method** is distribution-free and widely used in exploratory analysis. **Grubbs' test** provides formal hypothesis testing for a single outlier under normality. In practice, applying multiple methods and comparing their results gives the most reliable identification of genuine anomalies.

---

## Runnable Example: `outlier_detection_methods.py`

```python
"""
Data Cleaning & Preprocessing - Tutorial 04
Topic: Outlier Detection and Treatment (Intermediate)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    np.random.seed(42)

    print("="*80)
    print("TUTORIAL 04: OUTLIER DETECTION AND TREATMENT")
    print("="*80)

    # Generate data with outliers
    data = np.concatenate([np.random.normal(50, 10, 95), [150, 160, 155, -20, -15]])
    df = pd.DataFrame({'value': data})

    print("\nDataset statistics:")
    print(df.describe())

    # Method 1: Z-score
    print("\n--- Z-Score Method ---")
    z_scores = np.abs((df['value'] - df['value'].mean()) / df['value'].std())
    outliers_z = df[z_scores > 3]
    print(f"Outliers (|z| > 3): {len(outliers_z)} found")
    print(outliers_z)

    # Method 2: IQR
    print("\n--- IQR Method ---")
    Q1 = df['value'].quantile(0.25)
    Q3 = df['value'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers_iqr = df[(df['value'] < lower_bound) | (df['value'] > upper_bound)]
    print(f"IQR bounds: [{lower_bound:.2f}, {upper_bound:.2f}]")
    print(f"Outliers: {len(outliers_iqr)} found")
    print(outliers_iqr)

    # Method 3: Modified Z-score (MAD)
    print("\n--- Modified Z-Score (MAD) ---")
    median = df['value'].median()
    mad = np.median(np.abs(df['value'] - median))
    modified_z = 0.6745 * (df['value'] - median) / mad
    outliers_mad = df[np.abs(modified_z) > 3.5]
    print(f"Outliers (robust method): {len(outliers_mad)} found")

    # Treatment strategies
    print("\n--- Treatment Strategies ---")

    # Strategy 1: Remove outliers
    df_removed = df[z_scores <= 3]
    print(f"1. Removal: {len(df)} → {len(df_removed)} rows")

    # Strategy 2: Cap/Winsorize
    df_capped = df.copy()
    df_capped['value'] = df_capped['value'].clip(lower=lower_bound, upper=upper_bound)
    print(f"2. Capping: outliers clipped to [{lower_bound:.2f}, {upper_bound:.2f}]")

    # Strategy 3: Log transformation
    df_log = df[df['value'] > 0].copy()  # Only positive values
    df_log['value_log'] = np.log1p(df_log['value'])
    print(f"3. Log transform applied to {len(df_log)} positive values")

    print("\nKEY TAKEAWAYS:")
    print("- Z-score: assumes normal distribution, sensitive to extreme outliers")
    print("- IQR: robust, works for any distribution")
    print("- MAD: most robust, resistant to outliers")
    print("- Always investigate outliers before removing!")
    print("\nNEXT: 05_intermediate_encoding.py")
    print("="*80)
```

---

## Exercises

**Exercise 1.**
Generate 100 standard normal samples and insert one outlier at value 10. Apply the z-score method ($|z| > 3$) and the IQR method ($1.5 \times$ IQR) to detect the outlier. Compare which method finds it.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = np.append(np.random.normal(size=100), 10.0)

        z_scores = np.abs(stats.zscore(data))
        z_outliers = np.where(z_scores > 3)[0]

        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        iqr_outliers = np.where((data < q1 - 1.5*iqr) | (data > q3 + 1.5*iqr))[0]

        print(f"Z-score outliers: {z_outliers}")
        print(f"IQR outliers:     {iqr_outliers}")

---

**Exercise 2.**
Compute the modified z-score (using MAD) for the same dataset from Exercise 1. Use the threshold $|M_i| > 3.5$ to flag outliers. Compare the result with the standard z-score method.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = np.append(np.random.normal(size=100), 10.0)

        mad = stats.median_abs_deviation(data)
        median = np.median(data)
        modified_z = 0.6745 * (data - median) / mad
        mod_outliers = np.where(np.abs(modified_z) > 3.5)[0]

        z_outliers = np.where(np.abs(stats.zscore(data)) > 3)[0]

        print(f"Modified z-score outliers: {mod_outliers}")
        print(f"Standard z-score outliers: {z_outliers}")

---

**Exercise 3.**
Generate 200 samples from a $t$-distribution with 3 degrees of freedom (heavy tails). Apply the IQR outlier method and count how many values are flagged as outliers. Discuss whether these are true outliers or simply heavy-tailed behavior.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.t.rvs(df=3, size=200)

        q1, q3 = np.percentile(data, [25, 75])
        iqr = q3 - q1
        outliers = np.where((data < q1 - 1.5*iqr) | (data > q3 + 1.5*iqr))[0]
        print(f"Flagged outliers: {len(outliers)} out of 200")
        print("Note: heavy-tailed distributions produce many IQR 'outliers'")
