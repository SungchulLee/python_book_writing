# Exponential and Gamma

The exponential and gamma distributions are closely related continuous distributions that model waiting times and event durations. The exponential distribution models the time until a single event, while the gamma distribution generalizes this to the time until multiple events.

!!! tip "Mental Model"
    The exponential distribution is the "waiting time for one event" in a Poisson process; the gamma distribution is the "waiting time for $k$ events." The exponential's memoryless property means the remaining wait time does not depend on how long you have already waited -- the only continuous distribution with this property.

---

## Exponential Distribution

The exponential distribution models the time between events in a Poisson process. Its PDF is:

$$f(x) = \lambda e^{-\lambda x}, \quad x \ge 0$$

where $\lambda$ is the **rate parameter** (average number of events per unit time).

### Parametrization in scipy.stats

An important detail: `scipy.stats.expon` uses the **scale** parameter, which is the reciprocal of the rate: $\text{scale} = 1/\lambda$. When working with a rate $\lambda$, you must pass `scale=1/λ`:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

la = 3.0  # rate parameter λ
a = stats.expon(scale=1/la)  # scale = 1/λ

x = np.linspace(0, 3, 100)
y_pdf = a.pdf(x)
y_cdf = a.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend(loc='lower left')
plt.title(f'Exponential Distribution (λ={la})')
plt.xlabel('x')
plt.show()
```

The PDF starts at its maximum value $\lambda$ at $x=0$ and decays exponentially. The CDF $F(x) = 1 - e^{-\lambda x}$ rises from 0 toward 1.

### Key Properties

The exponential distribution has mean $E[X] = 1/\lambda$, variance $\text{Var}(X) = 1/\lambda^2$, and the unique **memoryless property**: $P(X > s + t \mid X > s) = P(X > t)$. This means that knowing the process has already lasted $s$ time units provides no information about the remaining time.

### Financial Applications

In finance, the exponential distribution models inter-arrival times of trades, time between defaults in credit risk, and duration analysis in survival models for corporate defaults.

## Gamma Distribution

The gamma distribution is a generalization of the exponential. If $X_1, \ldots, X_k$ are independent $\text{Exp}(\lambda)$ random variables, then their sum follows a $\text{Gamma}(k, 1/\lambda)$ distribution.

$$f(x) = \frac{\lambda^k x^{k-1} e^{-\lambda x}}{\Gamma(k)}, \quad x \ge 0$$

### Parameters

| Parameter | Symbol | `scipy.stats` keyword | Description |
|-----------|--------|----------------------|-------------|
| Shape     | $k$ (or $\alpha$) | `a` | Number of events |
| Scale     | $\theta = 1/\lambda$ | `scale` | Mean time between events |

```python
import scipy.stats as stats

# Gamma with shape=5, scale=2 (waiting for 5 events, mean inter-event time=2)
gamma_dist = stats.gamma(a=5, scale=2)
print(f"Mean: {gamma_dist.mean():.2f}")      # k * θ = 10
print(f"Variance: {gamma_dist.var():.2f}")    # k * θ² = 20
```

### Special Cases

The gamma family includes several important special cases: $\text{Gamma}(1, \theta) = \text{Exponential}(\text{scale}=\theta)$ and $\text{Gamma}(k/2, 2) = \chi^2(k)$ (chi-square with $k$ degrees of freedom).

### Financial Applications

In finance, the gamma distribution is used in insurance claim modeling (aggregate loss distributions), Bayesian conjugate priors for Poisson rate estimation, and stochastic volatility models where variance follows a gamma process.

## Summary

The exponential and gamma distributions form a natural family for modeling durations and waiting times. The key practical point when using `scipy.stats` is the scale parametrization: always pass `scale=1/λ` when working with rate parameters.

---

## Exercises

**Exercise 1.**
Verify the memoryless property of the exponential distribution numerically. For $X \sim \text{Exp}(\lambda=1)$, compute $P(X > 3 \mid X > 1)$ using the survival function and compare it to $P(X > 2)$.

??? success "Solution to Exercise 1"

        from scipy import stats

        rv = stats.expon(scale=1)
        p_conditional = rv.sf(3) / rv.sf(1)
        p_direct = rv.sf(2)
        print(f"P(X>3 | X>1) = {p_conditional:.6f}")
        print(f"P(X>2)       = {p_direct:.6f}")
        print(f"Equal: {abs(p_conditional - p_direct) < 1e-10}")

---

**Exercise 2.**
Show that the sum of $n$ independent $\text{Exp}(\lambda)$ random variables follows a $\text{Gamma}(n, 1/\lambda)$ distribution. Generate 10,000 sums of 5 exponential samples with $\lambda = 2$ and compare the sample mean/variance with $\text{Gamma}(5, 0.5)$ theoretical values.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        exp_samples = stats.expon.rvs(scale=0.5, size=(10000, 5))
        sums = exp_samples.sum(axis=1)

        gamma_rv = stats.gamma(a=5, scale=0.5)
        print(f"Sample mean: {np.mean(sums):.4f}, Theoretical: {gamma_rv.mean():.4f}")
        print(f"Sample var:  {np.var(sums, ddof=1):.4f}, Theoretical: {gamma_rv.var():.4f}")

---

**Exercise 3.**
Fit a gamma distribution to 500 samples generated from $\text{Gamma}(a=4, \text{scale}=3)$. Use `stats.gamma.fit()` with `floc=0` and compare the estimated parameters with the true values.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.gamma.rvs(a=4, scale=3, size=500)
        a_hat, loc_hat, scale_hat = stats.gamma.fit(data, floc=0)
        print(f"Estimated a={a_hat:.4f} (true 4), scale={scale_hat:.4f} (true 3)")
