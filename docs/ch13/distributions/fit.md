# Fitting Distributions to Data

Given a sample of observations, a natural question is: which parametric distribution best describes the data, and what are its parameters? The `.fit()` method on `scipy.stats` continuous distributions answers the second part by finding the **maximum likelihood estimates** (MLEs) of the distribution's parameters. This page covers the statistical principle behind `.fit()`, its usage, and practical considerations for reliable fitting.

!!! tip "Mental Model"
    Fitting a distribution asks: "Which parameter values make the observed data most probable?" The `.fit()` method searches the parameter space to maximize this likelihood. The result is the parametric model that best explains your sample, but always verify the fit visually -- MLE finds the best parameters for a given family, even if that family is wrong for your data.

---

## Maximum Likelihood Estimation

Suppose $x_1, x_2, \ldots, x_n$ are independent observations from a distribution with PDF $f(x; \theta)$, where $\theta$ collects all unknown parameters. The **likelihood function** is the joint density evaluated at the observed data, treated as a function of $\theta$:

$$
L(\theta) = \prod_{i=1}^{n} f(x_i; \theta)
$$

Because products of many small numbers are numerically unstable, optimization works with the **log-likelihood**:

$$
\ell(\theta) = \sum_{i=1}^{n} \ln f(x_i; \theta)
$$

The **maximum likelihood estimator** $\hat{\theta}$ is the value of $\theta$ that maximizes $\ell(\theta)$. MLE has desirable asymptotic properties: as $n \to \infty$, the estimator is consistent, asymptotically normal, and asymptotically efficient.

## The .fit() Method

Every `scipy.stats` continuous distribution provides a `.fit(data)` method that computes MLE for all parameters (shape, loc, scale):

```python
import numpy as np
import scipy.stats as stats

rng = np.random.default_rng(42)
data = rng.normal(loc=5.0, scale=2.0, size=500)

params = stats.norm.fit(data)
print(f"Estimated loc={params[0]:.3f}, scale={params[1]:.3f}")
```

The return value is a tuple whose length depends on the distribution. For distributions with shape parameters (e.g., gamma, beta), the shape parameters come first, followed by `loc` and `scale`.

### Return Value Structure

| Distribution | `.fit()` returns |
|---|---|
| `norm` | `(loc, scale)` |
| `expon` | `(loc, scale)` |
| `gamma` | `(a, loc, scale)` |
| `beta` | `(a, b, loc, scale)` |
| `t` | `(df, loc, scale)` |

### Example: Fitting a Gamma Distribution

The gamma distribution has a shape parameter $a$. Fitting recovers all three parameters:

```python
rng = np.random.default_rng(42)
data_gamma = rng.gamma(shape=2.0, scale=3.0, size=500)

a_hat, loc_hat, scale_hat = stats.gamma.fit(data_gamma)
print(f"shape={a_hat:.3f}, loc={loc_hat:.3f}, scale={scale_hat:.3f}")
```

The estimated shape should be close to 2.0 and the scale close to 3.0, with `loc` near 0.

## Fixing Parameters

Sometimes one or more parameters are known in advance. Pass them as keyword arguments to hold them fixed during optimization:

```python
# Fix loc=0 (data are strictly positive)
a_hat, loc_hat, scale_hat = stats.gamma.fit(data_gamma, floc=0)
print(f"shape={a_hat:.3f}, loc={loc_hat:.3f}, scale={scale_hat:.3f}")
```

The `floc` and `fscale` keywords fix `loc` and `scale` respectively. For shape parameters, use `f0` for the first shape parameter, `f1` for the second, and so on.

!!! tip "Fix loc=0 for positive distributions"
    Distributions like gamma, exponential, and lognormal have support on $[0, \infty)$. Leaving `loc` free lets the optimizer shift the distribution left, which can produce a negative `loc` and a misleading fit. Fix `loc=0` when the data are known to be non-negative.

## Visualizing the Fit

Overlaying the fitted PDF on a histogram of the data provides a quick visual check:

```python
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
data_gamma = rng.gamma(shape=2.0, scale=3.0, size=500)
a_hat, loc_hat, scale_hat = stats.gamma.fit(data_gamma, floc=0)

x = np.linspace(0, 20, 200)
pdf_fitted = stats.gamma.pdf(x, a_hat, loc=loc_hat, scale=scale_hat)

fig, ax = plt.subplots()
ax.hist(data_gamma, bins=30, density=True, alpha=0.6, label='Data')
ax.plot(x, pdf_fitted, 'r-', linewidth=2, label='Fitted gamma PDF')
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.set_title('Gamma Distribution Fit')
ax.legend()
plt.show()
```

## Goodness of Fit After Fitting

After fitting, use the Kolmogorov-Smirnov test to assess how well the fitted distribution matches the data:

```python
ks_stat, p_value = stats.kstest(data_gamma, 'gamma', args=(a_hat, loc_hat, scale_hat))
print(f"KS statistic={ks_stat:.4f}, p-value={p_value:.4f}")
```

!!! warning "KS test after fitting"
    When the distribution parameters are estimated from the same data used in the test, the $p$-value from `kstest` is conservative (biased toward not rejecting). The Lilliefors test or parametric bootstrap provides a more accurate $p$-value in this setting.

## Summary

The `.fit()` method on `scipy.stats` distributions finds maximum likelihood estimates of shape, location, and scale parameters. MLE maximizes the log-likelihood $\ell(\theta) = \sum \ln f(x_i; \theta)$, yielding estimators with strong asymptotic properties. Fixing known parameters with `floc` or `fscale` improves reliability, and overlaying the fitted PDF on a histogram provides an immediate visual diagnostic.

---

## Exercises

**Exercise 1.**
Generate 500 samples from a normal distribution with $\mu = 50$ and $\sigma = 8$. Use `stats.norm.fit()` to estimate the parameters. Print the estimated values and compare to the true parameters.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.norm.rvs(loc=50, scale=8, size=500)
        mu_hat, sigma_hat = stats.norm.fit(data)
        print(f"Estimated mu: {mu_hat:.4f} (true: 50)")
        print(f"Estimated sigma: {sigma_hat:.4f} (true: 8)")

---

**Exercise 2.**
Generate 1000 samples from a gamma distribution with shape $a = 3$ and scale $\theta = 2$. Fit a gamma distribution using `.fit()` with `floc=0` (fixing the location). Print the estimated shape and scale, then overlay the fitted PDF on a histogram.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats
        import matplotlib.pyplot as plt

        np.random.seed(42)
        data = stats.gamma.rvs(a=3, scale=2, size=1000)
        a_hat, loc_hat, scale_hat = stats.gamma.fit(data, floc=0)

        print(f"Estimated shape: {a_hat:.4f} (true: 3)")
        print(f"Estimated scale: {scale_hat:.4f} (true: 2)")

        x = np.linspace(0, data.max(), 200)
        plt.hist(data, bins=40, density=True, alpha=0.6)
        plt.plot(x, stats.gamma.pdf(x, a_hat, loc=0, scale=scale_hat), 'r-', lw=2)
        plt.title('Gamma Fit')
        plt.show()

---

**Exercise 3.**
Generate 500 samples from an exponential distribution with $\lambda = 0.5$. Fit both an exponential and a normal distribution to the data. Use the Kolmogorov-Smirnov test (`stats.kstest`) to determine which fit is better by comparing p-values.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.expon.rvs(scale=2, size=500)

        # Fit exponential
        loc_e, scale_e = stats.expon.fit(data, floc=0)
        ks_exp, p_exp = stats.kstest(data, 'expon', args=(0, scale_e))

        # Fit normal
        mu_n, sigma_n = stats.norm.fit(data)
        ks_norm, p_norm = stats.kstest(data, 'norm', args=(mu_n, sigma_n))

        print(f"Exponential fit — KS: {ks_exp:.4f}, p: {p_exp:.4f}")
        print(f"Normal fit     — KS: {ks_norm:.4f}, p: {p_norm:.4f}")
        print(f"Better fit: {'Exponential' if p_exp > p_norm else 'Normal'}")
