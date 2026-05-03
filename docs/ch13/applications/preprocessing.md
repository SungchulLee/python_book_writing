# Statistical Preprocessing

Many statistical methods and machine learning algorithms assume that the input data satisfies certain distributional properties -- approximate normality, constant scale, or absence of extreme outliers. When raw data violates these assumptions, statistical preprocessing transforms it into a form better suited for downstream analysis. This section covers the key transformations available in `scipy.stats`.

!!! tip "Mental Model"
    Raw data is like ingredients before cooking -- different units, different scales, different shapes. Preprocessing transforms (z-scoring, Box-Cox, rank transforms) are recipes that reshape data into a form that statistical methods can digest. The right transform depends on what your downstream method assumes about the input.

## Standardization (Z-Score)

Standardization centers data at zero and scales it to unit variance. For a sample $x_1, \ldots, x_n$, the z-score of each observation is

$$
z_i = \frac{x_i - \bar{x}}{s}
$$

where $\bar{x}$ is the sample mean and $s$ is the sample standard deviation.

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)
data = rng.exponential(scale=5.0, size=100)

z_scores = stats.zscore(data)
print(f"Original: mean={np.mean(data):.2f}, std={np.std(data, ddof=1):.2f}")
print(f"Z-scored: mean={np.mean(z_scores):.4f}, std={np.std(z_scores, ddof=1):.4f}")
```

Standardization does not change the shape of the distribution. A skewed distribution remains skewed after z-scoring.

## Box-Cox Transformation

The Box-Cox transformation maps positive data to approximate normality by applying a power transformation parameterized by $\lambda$:

$$
y_i = \begin{cases} \dfrac{x_i^\lambda - 1}{\lambda} & \text{if } \lambda \neq 0 \\[6pt] \ln x_i & \text{if } \lambda = 0 \end{cases}
$$

The optimal $\lambda$ is chosen by maximizing the log-likelihood of the resulting data under a normal model.

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)
data = rng.lognormal(mean=2, sigma=1, size=500)

# Apply Box-Cox (automatically finds optimal lambda)
transformed, lam = stats.boxcox(data)
print(f"Optimal lambda: {lam:.4f}")
print(f"Original skewness:    {stats.skew(data):.4f}")
print(f"Transformed skewness: {stats.skew(transformed):.4f}")
```

!!! warning "Box-Cox Requires Positive Data"
    The Box-Cox transformation is defined only for strictly positive values ($x_i > 0$). For data that includes zero or negative values, use the Yeo-Johnson transformation instead.

## Yeo-Johnson Transformation

The Yeo-Johnson transformation generalizes Box-Cox to handle zero and negative values. The transformation is defined piecewise:

$$
y_i = \begin{cases} \dfrac{(x_i + 1)^\lambda - 1}{\lambda} & \text{if } \lambda \neq 0,\; x_i \geq 0 \\[6pt] \ln(x_i + 1) & \text{if } \lambda = 0,\; x_i \geq 0 \\[6pt] -\dfrac{(-x_i + 1)^{2 - \lambda} - 1}{2 - \lambda} & \text{if } \lambda \neq 2,\; x_i < 0 \\[6pt] -\ln(-x_i + 1) & \text{if } \lambda = 2,\; x_i < 0 \end{cases}
$$

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)
data = rng.standard_t(df=3, size=500)  # includes negative values

transformed, lam = stats.yeojohnson(data)
print(f"Optimal lambda: {lam:.4f}")
print(f"Original kurtosis:    {stats.kurtosis(data):.4f}")
print(f"Transformed kurtosis: {stats.kurtosis(transformed):.4f}")
```

## Rank Transformation

Rank-based transformations replace each observation with its rank within the sample, removing the influence of outliers and producing a uniform marginal distribution.

For $n$ observations, the rank $R_i$ of $x_i$ ranges from 1 to $n$. The **rank-based inverse normal transformation** maps ranks to quantiles of the standard normal:

$$
z_i = \Phi^{-1}\!\left(\frac{R_i - c}{n - 2c + 1}\right)
$$

where $\Phi^{-1}$ is the standard normal quantile function and $c$ is a correction constant (commonly $c = 3/8$ for the Blom method).

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)
data = rng.exponential(scale=5.0, size=200)

# Rank transformation
ranks = stats.rankdata(data)
print(f"Min rank: {ranks.min()}, Max rank: {ranks.max()}")

# Rank-based inverse normal (Blom's method)
n = len(data)
c = 3/8
normal_scores = stats.norm.ppf((ranks - c) / (n - 2*c + 1))
print(f"Transformed skewness: {stats.skew(normal_scores):.4f}")
print(f"Transformed kurtosis: {stats.kurtosis(normal_scores):.4f}")
```

## Winsorization

Winsorization limits extreme values by replacing observations beyond specified percentiles with the boundary values. This reduces the influence of outliers without removing data points entirely.

```python
from scipy.stats import mstats
import numpy as np

rng = np.random.default_rng(42)
data = rng.standard_t(df=3, size=200)

# Winsorize at 5th and 95th percentiles
winsorized = mstats.winsorize(data, limits=[0.05, 0.05])
print(f"Original range:    [{data.min():.2f}, {data.max():.2f}]")
print(f"Winsorized range:  [{winsorized.min():.2f}, {winsorized.max():.2f}]")
print(f"Original std:      {np.std(data, ddof=1):.4f}")
print(f"Winsorized std:    {np.std(winsorized, ddof=1):.4f}")
```

## Choosing a Transformation

| Data property | Recommended transformation |
|---|---|
| Positive, right-skewed | Box-Cox or log transform |
| Includes negatives, skewed | Yeo-Johnson |
| Heavy outliers, ordinal analysis | Rank transformation |
| Extreme outliers, preserve scale | Winsorization |
| Already symmetric, different scales | Z-score standardization |

!!! tip "Test Normality After Transformation"
    After applying a transformation, verify the result with a normality test such as Shapiro-Wilk (`stats.shapiro`) or by inspecting a QQ plot (`stats.probplot`). No transformation guarantees perfect normality.

## Summary

Statistical preprocessing transforms raw data to better satisfy the assumptions of downstream methods. Z-score standardization adjusts location and scale without changing shape. Box-Cox and Yeo-Johnson power transformations reduce skewness and approximate normality. Rank transformations eliminate outlier effects entirely. The `scipy.stats` module provides efficient implementations of all these techniques through `zscore`, `boxcox`, `yeojohnson`, `rankdata`, and `mstats.winsorize`.


---

## Exercises

**Exercise 1.** Write code that standardizes a dataset (zero mean, unit variance) using `scipy.stats.zscore()` or manual computation.

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

**Exercise 2.** Explain the difference between standardization (z-score) and min-max normalization. When would you use each?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that detects outliers using the z-score method (values beyond 3 standard deviations from the mean).

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

**Exercise 4.** Create a function that takes a DataFrame, removes outliers from each numeric column using the IQR method, and returns the cleaned DataFrame.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
