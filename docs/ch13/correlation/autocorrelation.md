# Autocorrelation

When analyzing time series data, a natural question arises: does the value at one time point predict values at future time points? For example, stock returns today may influence returns tomorrow, and temperature measurements exhibit seasonal patterns. Autocorrelation quantifies this self-similarity by measuring the correlation of a signal with a delayed copy of itself, providing essential tools for detecting temporal dependencies in data.

!!! tip "Mental Model"
    Autocorrelation asks: "Does a time series remember its past?" Slide a copy of the signal forward by lag $k$ and correlate the original with the shifted version. High autocorrelation at lag $k$ means today's value is a useful predictor of the value $k$ steps ahead.

## Definition

For a stationary stochastic process $\{X_t\}$ with mean $\mu$ and variance $\sigma^2$, the **autocorrelation function** (ACF) at lag $\tau$ is defined as

$$
R(\tau) = \frac{\text{Cov}(X_t, X_{t+\tau})}{\text{Var}(X_t)} = \frac{E[(X_t - \mu)(X_{t+\tau} - \mu)]}{\sigma^2}
$$

The related **autocovariance function** is

$$
\gamma(\tau) = \text{Cov}(X_t, X_{t+\tau}) = E[(X_t - \mu)(X_{t+\tau} - \mu)]
$$

so that $R(\tau) = \gamma(\tau) / \gamma(0)$.

Given a sample $x_1, x_2, \ldots, x_n$, the **sample autocorrelation** at lag $k$ is

$$
\hat{r}_k = \frac{\sum_{t=1}^{n-k}(x_t - \bar{x})(x_{t+k} - \bar{x})}{\sum_{t=1}^{n}(x_t - \bar{x})^2}
$$

where $\bar{x} = \frac{1}{n}\sum_{t=1}^n x_t$ is the sample mean.

## Properties

The autocorrelation function has several important properties:

- **Normalization**: $R(0) = 1$ (a signal is perfectly correlated with itself at zero lag)
- **Symmetry**: $R(\tau) = R(-\tau)$ (correlation depends on the magnitude of the lag, not its direction)
- **Boundedness**: $|R(\tau)| \leq 1$ for all $\tau$
- **Positive semi-definiteness**: The autocovariance matrix formed from $\gamma(\tau)$ is positive semi-definite, which ensures that no linear combination of the process values can have negative variance

!!! note "Stationarity Requirement"
    The autocorrelation function is well-defined in this form only for **stationary** processes, where the mean and variance do not change over time and the covariance between $X_t$ and $X_{t+\tau}$ depends only on the lag $\tau$, not on $t$ itself.

## Partial Autocorrelation

While the ACF at lag $k$ captures the total correlation between $X_t$ and $X_{t+k}$, the **partial autocorrelation function** (PACF) isolates the direct relationship at lag $k$ after removing the linear influence of the intermediate lags $1, 2, \ldots, k-1$.

The PACF at lag $k$, denoted $\phi_{kk}$, is the last coefficient in the autoregression

$$
X_t = \phi_{k1} X_{t-1} + \phi_{k2} X_{t-2} + \cdots + \phi_{kk} X_{t-k} + \varepsilon_t
$$

The PACF is particularly useful for identifying the order of autoregressive (AR) models: an AR($p$) process has $\phi_{kk} = 0$ for all $k > p$.

## Computing Autocorrelation with SciPy

SciPy provides `scipy.signal.correlate` for computing raw cross-correlation, which can be normalized to obtain the autocorrelation.

```python
import numpy as np
from scipy import signal

# Generate a simple AR(1) process
np.random.seed(42)
n = 500
phi = 0.7
x = np.zeros(n)
for t in range(1, n):
    x[t] = phi * x[t - 1] + np.random.normal()

# Compute autocorrelation via scipy.signal.correlate
autocorr_full = signal.correlate(x - x.mean(), x - x.mean(), mode="full")
autocorr_full /= autocorr_full[len(autocorr_full) // 2]  # normalize by zero-lag
lags = np.arange(-n + 1, n)

# Extract non-negative lags
mid = len(autocorr_full) // 2
acf_values = autocorr_full[mid:mid + 20]  # first 20 lags
print("ACF at lags 0-4:", np.round(acf_values[:5], 4))
```

For time series analysis workflows, `statsmodels` provides dedicated ACF and PACF functions with confidence intervals.

```python
from statsmodels.tsa.stattools import acf, pacf

# Compute ACF and PACF with confidence bands
acf_vals, acf_confint = acf(x, nlags=20, alpha=0.05)
pacf_vals, pacf_confint = pacf(x, nlags=20, alpha=0.05)

print("Sample ACF  at lag 1:", round(acf_vals[1], 4))
print("Sample PACF at lag 1:", round(pacf_vals[1], 4))
print("Sample PACF at lag 2:", round(pacf_vals[2], 4))
```

!!! tip "Choosing Between ACF and PACF"
    Use the ACF to identify the order of moving average (MA) models: an MA($q$) process has $R(\tau) = 0$ for $|\tau| > q$. Use the PACF to identify the order of autoregressive (AR) models: an AR($p$) process has $\phi_{kk} = 0$ for $k > p$.

## Applications

Autocorrelation analysis serves several practical purposes in data analysis:

- **Model identification**: ACF and PACF plots guide selection of ARIMA model orders $(p, d, q)$
- **Residual diagnostics**: After fitting a model, the residual autocorrelations should be close to zero; significant residual autocorrelation indicates model inadequacy
- **Signal processing**: Autocorrelation detects periodicity in signals, even when obscured by noise
- **Independence testing**: The Ljung-Box test uses sample autocorrelations to test whether a time series is independently distributed

## Summary

Autocorrelation measures the linear dependence between values of a time series at different lags. The ACF captures total correlation at each lag, while the PACF isolates direct effects by removing intermediate dependencies. Together, they provide the primary diagnostic tools for time series model identification and residual analysis, with efficient implementations available through SciPy and statsmodels.

---

## Exercises

**Exercise 1.**
Generate an AR(1) process $x_t = 0.8 x_{t-1} + \varepsilon_t$ with $\varepsilon_t \sim N(0, 1)$ for 500 time steps. Plot the autocorrelation function (ACF) for lags 0 to 20 using `statsmodels.tsa.stattools.acf`.

??? success "Solution to Exercise 1"

        import numpy as np
        import matplotlib.pyplot as plt
        from statsmodels.tsa.stattools import acf

        np.random.seed(42)
        n = 500
        x = np.zeros(n)
        for t in range(1, n):
            x[t] = 0.8 * x[t-1] + np.random.normal()

        acf_vals = acf(x, nlags=20)
        plt.bar(range(21), acf_vals)
        plt.xlabel('Lag')
        plt.ylabel('ACF')
        plt.title('ACF of AR(1) with phi=0.8')
        plt.show()

---

**Exercise 2.**
For the same AR(1) process, compute the partial autocorrelation function (PACF) using `statsmodels.tsa.stattools.pacf`. Verify that only the first lag has a significant PACF value (close to 0.8).

??? success "Solution to Exercise 2"

        import numpy as np
        from statsmodels.tsa.stattools import pacf

        np.random.seed(42)
        n = 500
        x = np.zeros(n)
        for t in range(1, n):
            x[t] = 0.8 * x[t-1] + np.random.normal()

        pacf_vals = pacf(x, nlags=10)
        for lag, val in enumerate(pacf_vals):
            print(f"Lag {lag}: PACF = {val:.4f}")

---

**Exercise 3.**
Generate white noise (iid $N(0, 1)$, 200 samples) and compute the ACF for lags 1-15. Verify that all autocorrelations fall within the 95% confidence band $\pm 1.96/\sqrt{n}$.

??? success "Solution to Exercise 3"

        import numpy as np
        from statsmodels.tsa.stattools import acf

        np.random.seed(42)
        noise = np.random.normal(size=200)
        acf_vals = acf(noise, nlags=15)
        band = 1.96 / np.sqrt(200)
        all_inside = all(abs(acf_vals[k]) < band for k in range(1, 16))
        print(f"95% band: +/- {band:.4f}")
        print(f"All lags within band: {all_inside}")
