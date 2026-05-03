# Lognormal and Weibull

The lognormal and Weibull distributions are both continuous distributions on $(0, \infty)$ commonly used for modeling positive, right-skewed data. The lognormal distribution arises from multiplicative processes and is central to financial asset price modeling. The Weibull distribution is the standard model for reliability analysis and survival times, with a shape parameter that controls whether the failure rate increases, decreases, or remains constant over time.

!!! tip "Mental Model"
    If additive effects produce normality (Central Limit Theorem), multiplicative effects produce lognormality -- take the log of a lognormal variable and you get a normal. The Weibull, by contrast, is the "reliability distribution": its shape parameter controls whether failure rate increases (aging), decreases (infant mortality), or stays constant (random failure) over time.

---

## Lognormal Distribution

A random variable $Y$ follows a lognormal distribution if $\ln Y$ is normally distributed. Formally, if $X \sim N(\mu, \sigma^2)$, then $Y = e^X \sim \text{Lognormal}(\mu, \sigma^2)$.

### PDF

The probability density function is:

$$
f(y) = \frac{1}{y\,\sigma\sqrt{2\pi}} \exp\!\left(-\frac{(\ln y - \mu)^2}{2\sigma^2}\right), \quad y > 0
$$

where $\mu$ and $\sigma$ are the mean and standard deviation of the underlying normal distribution $\ln Y$, not of $Y$ itself.

### Parametrization in scipy.stats

An important detail: `scipy.stats.lognorm` uses the parameter `s` for $\sigma$ and `scale` for $e^\mu$. To create a lognormal distribution with parameters $\mu$ and $\sigma$, pass `s=σ` and `scale=exp(μ)`:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mu, sigma = 0.5, 0.8
a = stats.lognorm(s=sigma, scale=np.exp(mu))

print(f"Mean: {a.mean():.4f}")        # exp(μ + σ²/2)
print(f"Variance: {a.var():.4f}")

x = np.linspace(0, 10, 200)
y_pdf = a.pdf(x)
y_cdf = a.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend()
plt.title(f'Lognormal Distribution (μ={mu}, σ={sigma})')
plt.xlabel('y')
plt.ylabel('Density / Probability')
plt.show()
```

The PDF is right-skewed with a peak below the mean, reflecting the asymmetry inherent in the exponential transformation.

### Key Properties

- **Mean**: $E[Y] = e^{\mu + \sigma^2/2}$
- **Variance**: $\text{Var}(Y) = (e^{\sigma^2} - 1)\,e^{2\mu + \sigma^2}$
- **Median**: $e^\mu$ (the median equals the scale parameter in scipy)
- **Mode**: $e^{\mu - \sigma^2}$

### Financial Applications

The lognormal distribution is central to quantitative finance. The Black-Scholes model assumes that stock prices follow a geometric Brownian motion, which implies that prices at any future time are lognormally distributed. It is also used for modeling income distributions, insurance claim sizes, and asset values in credit risk models.

## Weibull Distribution

The Weibull distribution is a flexible model for lifetime data and reliability analysis. Its PDF is:

$$
f(x) = \frac{k}{\lambda}\left(\frac{x}{\lambda}\right)^{k-1} \exp\!\left(-\left(\frac{x}{\lambda}\right)^k\right), \quad x \ge 0
$$

where $k > 0$ is the **shape parameter** and $\lambda > 0$ is the **scale parameter**.

### Parametrization in scipy.stats

The `scipy.stats.weibull_min` function uses `c` for the shape parameter $k$ and `scale` for $\lambda$:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

k, lam = 2.0, 5.0
a = stats.weibull_min(c=k, scale=lam)

print(f"Mean: {a.mean():.4f}")
print(f"Variance: {a.var():.4f}")

x = np.linspace(0, 15, 200)
y_pdf = a.pdf(x)
y_cdf = a.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend()
plt.title(f'Weibull Distribution (k={k}, λ={lam})')
plt.xlabel('x')
plt.ylabel('Density / Probability')
plt.show()
```

### Effect of the Shape Parameter

The shape parameter $k$ controls the failure rate behavior, making the Weibull distribution versatile for reliability modeling:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 3, 200)
for k in [0.5, 1.0, 1.5, 2.0, 3.0]:
    plt.plot(x, stats.weibull_min(c=k, scale=1).pdf(x), label=f'k={k}')

plt.legend()
plt.title('Weibull PDFs for Various Shape Parameters (λ=1)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()
```

### Key Properties

- **Mean**: $E[X] = \lambda\,\Gamma(1 + 1/k)$
- **Variance**: $\text{Var}(X) = \lambda^2\left[\Gamma(1 + 2/k) - \Gamma(1 + 1/k)^2\right]$

### Special Cases and Failure Rate

- $k = 1$: reduces to the exponential distribution with rate $1/\lambda$ (constant failure rate)
- $k < 1$: decreasing failure rate (infant mortality or burn-in phase)
- $k > 1$: increasing failure rate (aging or wear-out phase)
- $k = 2$: the Rayleigh distribution (after appropriate scaling)

### Parameters in scipy.stats

| Parameter | Symbol | `scipy.stats` keyword | Default |
|-----------|--------|-----------------------|---------|
| Shape     | $k$    | `c`                  | (required) |
| Scale     | $\lambda$ | `scale`           | 1       |
| Location  | —      | `loc`                | 0       |

### Financial Applications

In finance, the Weibull distribution models time-to-default for bonds, operational risk event durations, and equipment failure in physical asset valuation. It is also used in insurance for modeling claim development periods and policy lapse rates.

## Summary

The lognormal and Weibull distributions are both flexible models for positive, right-skewed data. The key practical point for `scipy.stats` is the parametrization: use `stats.lognorm(s=σ, scale=exp(μ))` for lognormal and `stats.weibull_min(c=k, scale=λ)` for Weibull.

---

## Exercises

**Exercise 1.**
Generate 5000 samples from a lognormal distribution with $\mu = 0$ and $\sigma = 0.5$ (in log-space). Compute the sample mean and compare with the theoretical mean $e^{\mu + \sigma^2/2}$.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        rv = stats.lognorm(s=0.5, scale=np.exp(0))
        samples = rv.rvs(size=5000, random_state=42)
        theo_mean = np.exp(0 + 0.5**2 / 2)
        print(f"Sample mean: {np.mean(samples):.4f}")
        print(f"Theoretical mean: {theo_mean:.4f}")

---

**Exercise 2.**
Plot the Weibull PDF for shape parameters $c = 0.5, 1.0, 2.0, 5.0$ on the same axes. Identify which shapes correspond to decreasing, constant, and increasing hazard rates.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats
        import matplotlib.pyplot as plt

        x = np.linspace(0.01, 3, 200)
        for c in [0.5, 1.0, 2.0, 5.0]:
            plt.plot(x, stats.weibull_min.pdf(x, c), label=f'c={c}')
        plt.legend()
        plt.title('Weibull PDF for Various Shape Parameters')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.ylim(0, 3)
        plt.show()
        # c < 1: decreasing hazard, c = 1: constant, c > 1: increasing

---

**Exercise 3.**
Fit a lognormal distribution to the following data: take 1000 samples from $\text{Lognormal}(\mu=2, \sigma=0.8)$, use `stats.lognorm.fit()`, and recover the underlying $\mu$ and $\sigma$ parameters. Recall that `scipy` parametrizes lognormal with shape $s = \sigma$, `scale` $= e^\mu$.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.lognorm.rvs(s=0.8, scale=np.exp(2), size=1000)
        s_hat, loc_hat, scale_hat = stats.lognorm.fit(data, floc=0)
        mu_hat = np.log(scale_hat)
        print(f"Estimated sigma (s): {s_hat:.4f} (true: 0.8)")
        print(f"Estimated mu: {mu_hat:.4f} (true: 2.0)")
