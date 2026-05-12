# Moments and Skewness

Moments describe the shape of a distribution, with mean (1st moment), variance (2nd), skewness (3rd), and kurtosis (4th) quantifying center, spread, asymmetry, and tail heaviness respectively.

!!! tip "Mental Model"
    Each successive moment peels back another layer of a distribution's shape. The mean tells you where it sits, the variance how wide it spreads, the skewness which direction it leans, and the kurtosis how heavy its tails are. Together, these four numbers sketch a surprisingly complete portrait of any distribution.

---

## Moments Definition

### 1. Raw Moments

**E[X^n]:**

```python
from scipy import stats
import numpy as np

data = np.random.normal(0, 1, 1000)

# First raw moment = mean
m1 = np.mean(data)
print(f"1st moment (mean): {m1:.3f}")

# Second raw moment
m2 = np.mean(data**2)
print(f"2nd moment: {m2:.3f}")

# Third raw moment
m3 = np.mean(data**3)
print(f"3rd moment: {m3:.3f}")
```

### 2. Central Moments

**E[(X - μ)^n]:**

```python
mean = np.mean(data)

# Second central moment = variance
c2 = np.mean((data - mean)**2)
print(f"Variance: {c2:.3f}")

# Third central moment
c3 = np.mean((data - mean)**3)
print(f"3rd central moment: {c3:.3f}")

# Using scipy
print(stats.moment(data, moment=2))  # Variance
print(stats.moment(data, moment=3))  # 3rd central
```

### 3. Standardized Moments

**E[(X - μ)^n / σ^n]:**

```python
std = np.std(data, ddof=1)

# Skewness (3rd standardized moment)
skew = np.mean(((data - mean) / std)**3)
print(f"Skewness: {skew:.3f}")

# Using scipy
print(stats.skew(data, bias=False))
```

### 4. Relationship

```python
# Raw → Central
# μ₂' = E[X²] = Var(X) + (E[X])²
# μ₃' = E[X³] = μ₃ + 3μ(Var) + μ³

# Central → Standardized
# γ₃ = μ₃ / σ³ (skewness)
# γ₄ = μ₄ / σ⁴ - 3 (excess kurtosis)
```

### 5. Moment Generating Function

```python
# MGF: M(t) = E[e^(tX)]
# Derivatives at t=0 give moments

# For normal distribution
t = 0.5
norm_mgf = np.exp(mean * t + 0.5 * std**2 * t**2)
print(f"Normal MGF at t={t}: {norm_mgf:.3f}")
```

### 6. Cumulants

```python
# Cumulant generating function
# K(t) = log(M(t))

# First cumulant = mean
# Second cumulant = variance
# Third cumulant = third central moment
```

### 7. Sample vs Population

```python
# Sample moments (unbiased)
sample_var = np.var(data, ddof=1)  # Divide by n-1

# Population moments (biased)
pop_var = np.var(data, ddof=0)     # Divide by n

print(f"Sample variance: {sample_var:.3f}")
print(f"Population variance: {pop_var:.3f}")
```

---

## Skewness

### 1. Definition

**Measure of asymmetry:**

```python
# Skewness = E[(X - μ)³] / σ³
skewness = stats.skew(data, bias=False)
print(f"Skewness: {skewness:.3f}")

# Interpretation:
# 0: Symmetric (normal)
# >0: Right-skewed (positive, long right tail)
# <0: Left-skewed (negative, long left tail)
```

### 2. Positive Skew

```python
# Generate right-skewed data
right_skew = np.random.exponential(scale=1, size=1000)
print(f"Skewness: {stats.skew(right_skew):.3f}")  # ~2.0

# Visualization
plt.hist(right_skew, bins=50, density=True, alpha=0.7)
plt.axvline(np.mean(right_skew), color='r', label='Mean')
plt.axvline(np.median(right_skew), color='g', label='Median')
plt.legend()
plt.title('Positive Skew: Mean > Median')
plt.show()

# Mean pulled toward tail
print(f"Mean: {np.mean(right_skew):.3f}")
print(f"Median: {np.median(right_skew):.3f}")  # Mean > Median
```

### 3. Negative Skew

```python
# Generate left-skewed data
left_skew = -np.random.exponential(scale=1, size=1000)
print(f"Skewness: {stats.skew(left_skew):.3f}")  # ~-2.0

# Mean < Median for left skew
```

### 4. Skewness Test

```python
# Test if skewness significantly differs from 0
skewtest_stat, p_value = stats.skewtest(data)
print(f"Skew test: statistic={skewtest_stat:.3f}, p={p_value:.4f}")

# p < 0.05: Significant skewness (reject symmetry)
```

### 5. Pearson Skewness Coefficients

```python
# Mode skewness
mean = np.mean(data)
mode = stats.mode(data, keepdims=True).mode[0]
std = np.std(data, ddof=1)
pearson_mode = (mean - mode) / std

# Median skewness (more robust)
median = np.median(data)
pearson_median = 3 * (mean - median) / std

print(f"Pearson mode skewness: {pearson_mode:.3f}")
print(f"Pearson median skewness: {pearson_median:.3f}")
```

### 6. Quantile Skewness

```python
# Based on quartiles (very robust)
q1, q2, q3 = np.percentile(data, [25, 50, 75])
bowley_skew = (q3 + q1 - 2*q2) / (q3 - q1)
print(f"Bowley skewness: {bowley_skew:.3f}")

# Ranges from -1 to +1
```

### 7. Transformations

```python
# Box-Cox transformation to reduce skewness
from scipy import stats

data_positive = np.abs(data) + 1  # Must be positive
transformed, lambda_param = stats.boxcox(data_positive)

print(f"Original skewness: {stats.skew(data_positive):.3f}")
print(f"Transformed skewness: {stats.skew(transformed):.3f}")
print(f"Lambda parameter: {lambda_param:.3f}")
```

---

## Kurtosis

### 1. Definition

**Measure of tail heaviness:**

```python
# Excess kurtosis = E[(X - μ)⁴] / σ⁴ - 3
kurtosis = stats.kurtosis(data, bias=False)
print(f"Excess kurtosis: {kurtosis:.3f}")

# Interpretation:
# 0: Normal (mesokurtic)
# >0: Heavy tails (leptokurtic)
# <0: Light tails (platykurtic)
```

### 2. Leptokurtic (Heavy Tails)

```python
# t-distribution has heavy tails
heavy_tail = stats.t.rvs(df=5, size=1000)
print(f"Kurtosis: {stats.kurtosis(heavy_tail):.3f}")  # Positive

# More extreme values than normal
```

### 3. Platykurtic (Light Tails)

```python
# Uniform distribution has light tails
light_tail = np.random.uniform(-1, 1, 1000)
print(f"Kurtosis: {stats.kurtosis(light_tail):.3f}")  # ~-1.2

# Fewer extreme values than normal
```

### 4. Kurtosis Test

```python
# Test if kurtosis significantly differs from 0 (normal)
kurttest_stat, p_value = stats.kurtosistest(data)
print(f"Kurt test: statistic={kurttest_stat:.3f}, p={p_value:.4f}")

# p < 0.05: Significant deviation from normal kurtosis
```

### 5. Sample Kurtosis Bias

```python
# Unbiased vs biased estimator
kurt_unbiased = stats.kurtosis(data, bias=False)  # Recommended
kurt_biased = stats.kurtosis(data, bias=True)

print(f"Unbiased: {kurt_unbiased:.3f}")
print(f"Biased: {kurt_biased:.3f}")
```

### 6. Outlier Sensitivity

```python
# Kurtosis very sensitive to outliers
data_clean = np.random.normal(0, 1, 100)
data_outlier = np.concatenate([data_clean, [10, -10]])

print(f"Clean kurtosis: {stats.kurtosis(data_clean):.3f}")
print(f"With outliers: {stats.kurtosis(data_outlier):.3f}")  # Much higher
```

### 7. Robust Alternatives

```python
# L-kurtosis (based on L-moments, more robust)
# Not in scipy, but conceptually important

# Or use quantile-based measure
q = np.percentile(data, [10, 25, 75, 90])
robust_kurt = (q[3] - q[0]) / (q[2] - q[1])
print(f"Robust kurtosis proxy: {robust_kurt:.3f}")
```

---

## Normal Test

### 1. Jarque-Bera Test

```python
# Tests both skewness and kurtosis
jb_stat, p_value = stats.jarque_bera(data)
print(f"Jarque-Bera: statistic={jb_stat:.3f}, p={p_value:.4f}")

# H0: Data is normally distributed
# p < 0.05: Reject normality
```

### 2. Anderson-Darling Test

```python
# More powerful than Jarque-Bera
result = stats.anderson(data, dist='norm')
print(f"A-D statistic: {result.statistic:.3f}")

# Compare to critical values
for i, sl in enumerate(result.significance_level):
    print(f"{sl}%: {result.critical_values[i]:.3f}")
```

### 3. Shapiro-Wilk Test

```python
# Most powerful test for normality (small samples)
sw_stat, p_value = stats.shapiro(data)
print(f"Shapiro-Wilk: statistic={sw_stat:.4f}, p={p_value:.4f}")

# W close to 1 indicates normality
```

### 4. Kolmogorov-Smirnov Test

```python
# General distribution test
ks_stat, p_value = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data)))
print(f"K-S test: statistic={ks_stat:.4f}, p={p_value:.4f}")
```

### 5. D'Agostino-Pearson Test

```python
# Combines skew and kurtosis tests
k2, p_value = stats.normaltest(data)
print(f"D'Agostino: statistic={k2:.3f}, p={p_value:.4f}")

# Equivalent to combining skewtest and kurtosistest
```

### 6. Q-Q Plot

```python
# Visual normality check
stats.probplot(data, dist="norm", plot=plt)
plt.title("Q-Q Plot")
plt.show()

# Points on line → Normal
# S-curve → Heavy tails
# Reverse S → Light tails
```

### 7. Omnibus Test

```python
# Not directly in scipy, but can be constructed
skew = stats.skew(data)
kurt = stats.kurtosis(data)
n = len(data)

# Jarque-Bera statistic
jb = n/6 * (skew**2 + kurt**2/4)
p_value = 1 - stats.chi2.cdf(jb, df=2)
print(f"Omnibus: JB={jb:.3f}, p={p_value:.4f}")
```

---

## Practical Applications

### 1. Financial Returns

```python
# Stock returns often have fat tails
returns = np.random.standard_t(df=5, size=1000) * 0.02  # 2% daily vol

print(f"Skewness: {stats.skew(returns):.3f}")
print(f"Kurtosis: {stats.kurtosis(returns):.3f}")  # Positive → Fat tails

# Implications: Normal models underestimate risk
```

### 2. Income Distribution

```python
# Income typically right-skewed
income = np.random.lognormal(mean=10.5, sigma=0.5, size=1000)

print(f"Skewness: {stats.skew(income):.3f}")  # Strongly positive
print(f"Mean: ${np.mean(income):.0f}")
print(f"Median: ${np.median(income):.0f}")  # Median < Mean
```

### 3. Outlier Detection

```python
# High kurtosis suggests outliers
if stats.kurtosis(data) > 3:
    print("Warning: Heavy tails detected")
    # Consider robust statistics or outlier removal
```

### 4. Transformation Selection

```python
# Choose transformation based on skewness
if stats.skew(data) > 1:
    # Strong right skew → log transform
    transformed = np.log(data + 1)
elif stats.skew(data) < -1:
    # Strong left skew → exponential transform
    transformed = np.exp(data)
else:
    # Mild skew → square root or Box-Cox
    transformed, _ = stats.boxcox(data + abs(data.min()) + 1)
```

### 5. Model Selection

```python
# Normal vs t-distribution based on kurtosis
if abs(stats.kurtosis(data)) < 1:
    model = stats.norm
    print("Using normal distribution")
else:
    # Fit t-distribution for heavy tails
    df, loc, scale = stats.t.fit(data)
    model = stats.t(df=df, loc=loc, scale=scale)
    print(f"Using t-distribution (df={df:.1f})")
```

### 6. Risk Measures

```python
# VaR underestimated if kurtosis ignored
mean, std = np.mean(returns), np.std(returns)

# Normal assumption
var_normal = stats.norm.ppf(0.05, loc=mean, scale=std)

# Empirical (accounts for actual distribution)
var_empirical = np.percentile(returns, 5)

print(f"VaR (normal): {var_normal:.4f}")
print(f"VaR (empirical): {var_empirical:.4f}")
```

### 7. Power Analysis

```python
# Sample size for detecting skewness/kurtosis
from statsmodels.stats.power import normal_power_het

# Example: Detect skewness of 0.5 with power 0.8
# Requires large sample size
```

---

## Summary

**Moments:**

- 1st: Mean (location)
- 2nd: Variance (spread)
- 3rd: Skewness (asymmetry)
- 4th: Kurtosis (tail heaviness)

**Skewness:**

- 0: Symmetric
- >0: Right-skewed (mean > median)
- <0: Left-skewed (mean < median)

**Kurtosis (excess):**

- 0: Normal tails
- >0: Heavy tails (more extremes)
- <0: Light tails (fewer extremes)

**Key insight:** Higher moments reveal distribution shape beyond mean and variance, with skewness indicating asymmetry (important for risk assessment) and kurtosis measuring tail thickness (critical for extreme event modeling).

---

## Exercises

**Exercise 1.**
Compute the skewness and excess kurtosis of 1000 samples from (a) a standard normal, (b) an exponential with $\lambda = 1$, and (c) a uniform on $[0, 1]$. Use `scipy.stats.skew()` and `scipy.stats.kurtosis()`.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        for name, data in [("Normal", np.random.normal(size=1000)),
                           ("Exponential", np.random.exponential(size=1000)),
                           ("Uniform", np.random.uniform(size=1000))]:
            print(f"{name:12s}: skew={stats.skew(data):.4f}, kurtosis={stats.kurtosis(data):.4f}")

---

**Exercise 2.**
For 500 samples from a $\chi^2(5)$ distribution, compute the first four raw moments using `scipy.stats.moment()` (for central moments) and manual computation. Compare with theoretical moments.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats as st

        np.random.seed(42)
        data = st.chi2.rvs(df=5, size=500)
        for k in range(1, 5):
            cm = st.moment(data, moment=k)
            print(f"Central moment {k}: {cm:.4f}")

---

**Exercise 3.**
Apply the Jarque-Bera test (`scipy.stats.jarque_bera()`) to samples from a normal and a lognormal distribution (500 samples each). Print the test statistics and p-values to demonstrate which sample departs from normality.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        normal_data = np.random.normal(size=500)
        lognormal_data = np.random.lognormal(size=500)

        for name, data in [("Normal", normal_data), ("Lognormal", lognormal_data)]:
            jb_stat, p_val = stats.jarque_bera(data)
            print(f"{name:10s}: JB={jb_stat:.4f}, p={p_val:.4f}")
