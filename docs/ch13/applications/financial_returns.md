# Financial Returns Analysis

Financial asset prices change over time, and the statistical properties of their returns determine risk, inform portfolio construction, and underpin derivative pricing models. This section applies `scipy.stats` tools to analyze return distributions, test for normality, and fit parametric models to return data.

!!! tip "Mental Model"
    Financial returns are the language of risk. Converting raw prices to returns reveals the statistical fingerprint of an asset -- its volatility, skewness, and tail behavior. The key insight is that real returns are not normal: they have fat tails and occasional extreme moves that simple Gaussian models dangerously underestimate.

## Return Definitions

Let $P_t$ denote the price of an asset at time $t$. Two common return measures are:

**Simple return** over one period:

$$
R_t = \frac{P_t - P_{t-1}}{P_{t-1}} = \frac{P_t}{P_{t-1}} - 1
$$

**Log return** (continuously compounded return):

$$
r_t = \ln\!\left(\frac{P_t}{P_{t-1}}\right) = \ln P_t - \ln P_{t-1}
$$

Log returns have the advantage of being additive over time: the multi-period log return is $r_{t_1, t_2} = \sum_{s=t_1+1}^{t_2} r_s$.

```python
import numpy as np

# Simulated daily prices
rng = np.random.default_rng(42)
prices = 100 * np.exp(np.cumsum(rng.normal(0.0005, 0.02, 252)))

# Compute returns
simple_returns = np.diff(prices) / prices[:-1]
log_returns = np.diff(np.log(prices))

print(f"Mean daily simple return: {simple_returns.mean():.6f}")
print(f"Mean daily log return:    {log_returns.mean():.6f}")
print(f"Annualized volatility:    {log_returns.std() * np.sqrt(252):.4f}")
```

## Stylized Facts of Return Distributions

Empirical return distributions consistently exhibit several properties that deviate from normality:

1. **Fat tails (leptokurtosis)**: Extreme returns occur more frequently than a normal distribution predicts. The excess kurtosis $\kappa - 3$ is typically positive.

2. **Slight negative skewness**: Large negative returns tend to be more extreme than large positive returns, especially for equity indices.

3. **Volatility clustering**: Periods of high volatility tend to be followed by high volatility, and similarly for calm periods. This manifests as autocorrelation in squared returns.

4. **Approximate symmetry at short horizons**: Daily log returns are roughly symmetric around zero.

## Descriptive Statistics

The first four moments characterize the shape of the return distribution. For a sample $r_1, \ldots, r_n$, the sample skewness and kurtosis are

$$
\hat{S} = \frac{1}{n} \sum_{i=1}^n \left(\frac{r_i - \bar{r}}{s}\right)^3, \qquad \hat{K} = \frac{1}{n} \sum_{i=1}^n \left(\frac{r_i - \bar{r}}{s}\right)^4
$$

where $\bar{r}$ is the sample mean and $s$ is the sample standard deviation.

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)
log_returns = rng.standard_t(df=5, size=1000) * 0.01

print(f"Mean:     {np.mean(log_returns):.6f}")
print(f"Std dev:  {np.std(log_returns, ddof=1):.6f}")
print(f"Skewness: {stats.skew(log_returns):.4f}")
print(f"Kurtosis: {stats.kurtosis(log_returns):.4f}")  # excess kurtosis
```

## Normality Testing

The assumption that returns follow a normal distribution is central to many financial models. Several tests evaluate this assumption.

### Jarque-Bera Test

The Jarque-Bera test combines skewness and kurtosis into a single test statistic:

$$
JB = \frac{n}{6}\left(\hat{S}^2 + \frac{(\hat{K} - 3)^2}{4}\right)
$$

Under $H_0$ (normality), $JB \sim \chi^2(2)$ asymptotically.

```python
from scipy import stats

jb_stat, jb_p = stats.jarque_bera(log_returns)
print(f"Jarque-Bera statistic: {jb_stat:.2f}")
print(f"p-value: {jb_p:.4e}")
```

### Shapiro-Wilk and Anderson-Darling Tests

```python
from scipy import stats

# Shapiro-Wilk (best for n < 5000)
sw_stat, sw_p = stats.shapiro(log_returns[:500])
print(f"Shapiro-Wilk p-value: {sw_p:.4e}")

# Anderson-Darling
ad_result = stats.anderson(log_returns, dist='norm')
print(f"Anderson-Darling statistic: {ad_result.statistic:.4f}")
print(f"Critical values (5%): {ad_result.critical_values[2]:.4f}")
```

## Distribution Fitting

When returns deviate from normality, alternative distributions provide better fits. Common choices include the Student's $t$-distribution (captures fat tails) and the skew-normal distribution.

### Fitting a Student's t-Distribution

The Student's $t$-distribution with $\nu$ degrees of freedom has probability density

$$
f(x; \nu, \mu, \sigma) = \frac{\Gamma\!\left(\frac{\nu+1}{2}\right)}{\sigma\sqrt{\nu\pi}\;\Gamma\!\left(\frac{\nu}{2}\right)} \left(1 + \frac{1}{\nu}\left(\frac{x - \mu}{\sigma}\right)^2\right)^{-(\nu+1)/2}
$$

Smaller $\nu$ produces heavier tails. As $\nu \to \infty$, the distribution converges to the normal.

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)
log_returns = rng.standard_t(df=5, size=1000) * 0.01

# Fit t-distribution
df_fit, loc_fit, scale_fit = stats.t.fit(log_returns)
print(f"Fitted degrees of freedom: {df_fit:.2f}")
print(f"Fitted location: {loc_fit:.6f}")
print(f"Fitted scale: {scale_fit:.6f}")

# Goodness of fit: KS test
ks_stat, ks_p = stats.kstest(log_returns, 't', args=(df_fit, loc_fit, scale_fit))
print(f"KS test p-value (t-fit): {ks_p:.4f}")

# Compare with normal fit
loc_n, scale_n = stats.norm.fit(log_returns)
ks_stat_n, ks_p_n = stats.kstest(log_returns, 'norm', args=(loc_n, scale_n))
print(f"KS test p-value (normal-fit): {ks_p_n:.4f}")
```

## Value at Risk

Value at Risk (VaR) estimates the maximum expected loss at a given confidence level over a specified time horizon. At confidence level $1 - \alpha$, the parametric VaR under a fitted distribution $F$ is

$$
\text{VaR}_\alpha = -F^{-1}(\alpha)
$$

where $F^{-1}$ is the quantile function (percent point function).

```python
from scipy import stats
import numpy as np

# Using the fitted t-distribution
alpha = 0.05
var_t = -stats.t.ppf(alpha, df=df_fit, loc=loc_fit, scale=scale_fit)
var_norm = -stats.norm.ppf(alpha, loc=loc_n, scale=scale_n)

print(f"VaR (5%, t-distribution): {var_t:.6f}")
print(f"VaR (5%, normal):         {var_norm:.6f}")
```

!!! warning "Parametric VaR Assumptions"
    Parametric VaR relies on the chosen distribution accurately modeling the tail behavior. If the fitted distribution underestimates tail risk, VaR will understate potential losses. Historical simulation and Monte Carlo methods provide non-parametric alternatives.

## Summary

Financial returns analysis applies descriptive statistics, normality tests, and distribution fitting from `scipy.stats` to characterize asset return behavior. The key findings across most asset classes are fat tails, slight negative skewness, and rejection of normality. The Student's $t$-distribution provides a better parametric fit than the normal, and quantile-based risk measures like VaR directly leverage fitted distribution objects.


---

## Exercises

**Exercise 1.** Write code that generates a synthetic daily return series and computes the annualized mean return and volatility.

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

**Exercise 2.** Explain the difference between arithmetic and geometric (log) returns. When should you use each?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that computes the Sharpe ratio for a return series with a risk-free rate of 2% per year.

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

**Exercise 4.** Generate 10000 simulated daily returns from a normal distribution and test whether they are truly normally distributed using the Shapiro-Wilk test.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
