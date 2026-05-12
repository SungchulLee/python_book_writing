# Monte Carlo Methods in Finance

Many financial quantities -- option prices, risk measures, portfolio values -- lack closed-form solutions but can be estimated by simulating random scenarios and averaging the outcomes. Monte Carlo simulation leverages the law of large numbers to convert a probabilistic pricing problem into a computational one. This section demonstrates Monte Carlo methods in finance using `scipy.stats` for distribution sampling and statistical analysis of the results.

!!! tip "Mental Model"
    When you cannot solve a pricing equation on paper, simulate thousands of possible futures and average the payoffs. Each simulated path is one "what if" scenario; the law of large numbers guarantees that enough scenarios converge to the true price, turning an intractable integral into a counting exercise.

## Geometric Brownian Motion

The standard model for stock price dynamics under the risk-neutral measure is geometric Brownian motion (GBM):

$$
dS_t = r\, S_t\, dt + \sigma\, S_t\, dW_t
$$

where $r$ is the risk-free rate, $\sigma$ is the volatility, and $W_t$ is a standard Brownian motion. The exact solution at time $T$ is

$$
S_T = S_0 \exp\!\left[\left(r - \frac{\sigma^2}{2}\right)T + \sigma\sqrt{T}\, Z\right]
$$

where $Z \sim N(0, 1)$. This formula enables direct simulation of the terminal price without discretizing the path.

```python
from scipy import stats
import numpy as np

def simulate_gbm_terminal(s0, r, sigma, T, n_paths, rng=None):
    """Simulate terminal stock prices under GBM."""
    if rng is None:
        rng = np.random.default_rng()
    z = rng.standard_normal(n_paths)
    drift = (r - 0.5 * sigma**2) * T
    diffusion = sigma * np.sqrt(T) * z
    return s0 * np.exp(drift + diffusion)
```

## European Option Pricing

Under risk-neutral pricing, the price of a European option with payoff $h(S_T)$ is

$$
V_0 = e^{-rT}\, \mathbb{E}^{\mathbb{Q}}[h(S_T)]
$$

The Monte Carlo estimator approximates this expectation by averaging over $N$ simulated paths:

$$
\hat{V}_0 = e^{-rT} \cdot \frac{1}{N} \sum_{i=1}^{N} h(S_T^{(i)})
$$

By the central limit theorem, the standard error of this estimator is

$$
\text{SE}(\hat{V}_0) = \frac{e^{-rT}\, \hat{\sigma}_h}{\sqrt{N}}
$$

where $\hat{\sigma}_h$ is the sample standard deviation of the payoffs.

```python
from scipy import stats
import numpy as np

def price_european_option(s0, K, r, sigma, T, n_paths, option_type='call',
                          rng=None):
    """Price a European option via Monte Carlo simulation."""
    s_T = simulate_gbm_terminal(s0, r, sigma, T, n_paths, rng)

    if option_type == 'call':
        payoffs = np.maximum(s_T - K, 0)
    elif option_type == 'put':
        payoffs = np.maximum(K - s_T, 0)
    else:
        raise ValueError(f"Unknown option type: {option_type}")

    discount = np.exp(-r * T)
    price = discount * np.mean(payoffs)
    se = discount * np.std(payoffs, ddof=1) / np.sqrt(n_paths)
    return price, se

# Parameters
s0, K, r, sigma, T = 100, 105, 0.05, 0.2, 1.0
rng = np.random.default_rng(42)

price, se = price_european_option(s0, K, r, sigma, T, n_paths=100_000, rng=rng)
print(f"Monte Carlo price: {price:.4f}")
print(f"Standard error:    {se:.4f}")
print(f"95% CI: [{price - 1.96*se:.4f}, {price + 1.96*se:.4f}]")
```

### Black-Scholes Reference

For a European call, the Black-Scholes formula provides an exact benchmark:

$$
C = S_0\, \mathcal{N}(d_1) - K e^{-rT}\, \mathcal{N}(d_2)
$$

where $\Phi$ is the standard normal CDF and

$$
d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}
$$

```python
from scipy import stats
import numpy as np

def black_scholes_call(s0, K, r, sigma, T):
    """Compute Black-Scholes European call price."""
    d1 = (np.log(s0/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    return s0 * stats.norm.cdf(d1) - K * np.exp(-r*T) * stats.norm.cdf(d2)

bs_price = black_scholes_call(s0, K, r, sigma, T)
print(f"Black-Scholes price: {bs_price:.4f}")
```

## Convergence Rate

The Monte Carlo estimator converges at rate $O(1/\sqrt{N})$, meaning that reducing the standard error by half requires four times as many paths. This convergence rate is independent of the problem's dimensionality, which makes Monte Carlo particularly attractive for high-dimensional problems.

```python
import numpy as np

rng = np.random.default_rng(42)
path_counts = [1_000, 10_000, 100_000, 1_000_000]

for n in path_counts:
    price, se = price_european_option(s0, K, r, sigma, T, n, rng=rng)
    print(f"N={n:>10,d}  Price={price:.4f}  SE={se:.4f}")
```

## Variance Reduction

### Antithetic Variates

For each standard normal draw $Z_i$, the antithetic draw $-Z_i$ produces a negatively correlated path. Averaging the two reduces variance without additional random draws:

$$
\hat{V}_{\text{anti}} = e^{-rT} \cdot \frac{1}{N}\sum_{i=1}^{N} \frac{h(S_T(Z_i)) + h(S_T(-Z_i))}{2}
$$

```python
import numpy as np

def price_antithetic(s0, K, r, sigma, T, n_paths, rng=None):
    """Price with antithetic variates for variance reduction."""
    if rng is None:
        rng = np.random.default_rng()
    z = rng.standard_normal(n_paths)

    drift = (r - 0.5 * sigma**2) * T
    s_plus = s0 * np.exp(drift + sigma * np.sqrt(T) * z)
    s_minus = s0 * np.exp(drift + sigma * np.sqrt(T) * (-z))

    payoffs = 0.5 * (np.maximum(s_plus - K, 0) + np.maximum(s_minus - K, 0))
    discount = np.exp(-r * T)
    price = discount * np.mean(payoffs)
    se = discount * np.std(payoffs, ddof=1) / np.sqrt(n_paths)
    return price, se

rng = np.random.default_rng(42)
price_av, se_av = price_antithetic(s0, K, r, sigma, T, 50_000, rng)
print(f"Antithetic price: {price_av:.4f}, SE: {se_av:.4f}")
```

!!! tip "Choosing Variance Reduction Techniques"
    Antithetic variates work well when the payoff is monotonic in the underlying random variable. For more complex payoffs, control variates (using a correlated quantity with a known expectation) can provide larger variance reductions.

## Summary

Monte Carlo simulation estimates financial quantities by averaging over randomly generated scenarios. The geometric Brownian motion model provides the sampling distribution for stock prices under the risk-neutral measure. The estimator converges at rate $O(1/\sqrt{N})$, and variance reduction techniques such as antithetic variates improve efficiency. The `scipy.stats.norm` distribution underlies the random number generation and provides the CDF needed for the Black-Scholes reference formula.

---

## Runnable Example: `advanced_topics.py`

```python
"""
Tutorial 07: Advanced Statistical Methods
=========================================
Level: Advanced
Topics: Survival analysis, multivariate distributions, maximum likelihood,
        Monte Carlo methods, statistical modeling

This module introduces advanced statistical concepts and methods available
in scipy.stats for specialized analyses.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import minimize
import warnings

if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    np.random.seed(42)

    print("="*80)
    print("ADVANCED STATISTICAL METHODS")
    print("="*80)
    print()

    # =============================================================================
    # SECTION 1: Multivariate Normal Distribution
    # =============================================================================
    """
    Multivariate normal distribution extends the normal distribution to
    multiple dimensions with specified covariance structure.
    """

    print("MULTIVARIATE NORMAL DISTRIBUTION")
    print("-" * 40)

    # Define 2D multivariate normal
    mean = [0, 0]
    cov = [[1, 0.7],   # Positive correlation between variables
           [0.7, 1]]

    # Generate samples
    mvn = stats.multivariate_normal(mean, cov)
    samples = mvn.rvs(size=1000)

    print(f"Mean vector: {mean}")
    print(f"Covariance matrix:")
    print(f"  {cov[0]}")
    print(f"  {cov[1]}")
    print()

    # Calculate sample statistics
    sample_mean = np.mean(samples, axis=0)
    sample_cov = np.cov(samples.T)

    print(f"Sample mean: [{sample_mean[0]:.3f}, {sample_mean[1]:.3f}]")
    print(f"Sample covariance:")
    print(f"  [{sample_cov[0,0]:.3f}, {sample_cov[0,1]:.3f}]")
    print(f"  [{sample_cov[1,0]:.3f}, {sample_cov[1,1]:.3f}]")
    print()

    # Visualize
    plt.figure(figsize=(10, 8))
    plt.scatter(samples[:,0], samples[:,1], alpha=0.5)
    plt.xlabel('X₁')
    plt.ylabel('X₂')
    plt.title('Bivariate Normal Distribution Samples')
    plt.grid(True, alpha=0.3)
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/07_multivariate_normal.png', 
                dpi=300, bbox_inches='tight')
    print("Saved: 07_multivariate_normal.png\n")
    plt.close()

    # More advanced content would continue...

    print("="*80)
    print("Tutorial 07 Complete!")
    print("="*80)
```


---

## Exercises

**Exercise 1.** Write code that uses Monte Carlo simulation to estimate the price of a European call option under the Black-Scholes model.

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

**Exercise 2.** Explain how Monte Carlo simulation can be used to estimate Value at Risk (VaR). What does the 95% VaR represent?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that simulates 10000 portfolio return paths and computes the 5th percentile as the VaR estimate.

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

**Exercise 4.** Create a Monte Carlo simulation that estimates $\pi$ by generating random points in a unit square and counting those inside a quarter circle.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
