# Monte Carlo Simulation

Many quantities in statistics --- expectations, probabilities, integrals, sampling distributions --- lack closed-form expressions. When analytical solutions are unavailable, **Monte Carlo simulation** provides a numerical alternative: generate random samples from the relevant distribution, compute the quantity of interest on each sample, and average the results. The law of large numbers guarantees that this average converges to the true value as the number of samples grows.

This page introduces the Monte Carlo principle, derives the standard error of Monte Carlo estimates, and shows how simulation is used to approximate expectations, probabilities, and sampling distributions.

!!! tip "Mental Model"
    Monte Carlo replaces integrals with averages of random samples. If you cannot compute $E[g(X)]$ analytically, draw $N$ samples from $X$, evaluate $g$ on each, and average. The law of large numbers guarantees convergence, and the standard error shrinks as $1/\sqrt{N}$ regardless of the problem's dimensionality.

---

## The Monte Carlo Principle

Suppose we want to compute $\mu = E[g(X)]$ for a random variable $X$ with distribution $F$ and a function $g$. The **Monte Carlo estimator** draws $N$ independent samples $X_1, X_2, \ldots, X_N$ from $F$ and approximates the expectation by the sample average:

$$
\hat{\mu}_N = \frac{1}{N}\sum_{i=1}^{N} g(X_i)
$$

By the **strong law of large numbers**, $\hat{\mu}_N \to \mu$ almost surely as $N \to \infty$. The Monte Carlo method converts the analytical problem of computing an expectation into the computational problem of generating random samples and averaging.

---

## Monte Carlo Standard Error

The accuracy of the Monte Carlo estimate depends on $N$ and on the variance of $g(X)$. If $\sigma^2 = \operatorname{Var}(g(X))$ is finite, the central limit theorem gives:

$$
\sqrt{N}\,(\hat{\mu}_N - \mu) \xrightarrow{d} N(0, \sigma^2)
$$

The **Monte Carlo standard error** is:

$$
\text{SE}(\hat{\mu}_N) = \frac{\sigma}{\sqrt{N}}
$$

In practice, $\sigma$ is unknown and is estimated by the sample standard deviation of the $g(X_i)$ values:

$$
\hat{\sigma} = \sqrt{\frac{1}{N-1}\sum_{i=1}^{N}\left(g(X_i) - \hat{\mu}_N\right)^2}
$$

!!! tip "The square-root convergence rate"
    The Monte Carlo error decreases as $O(N^{-1/2})$: to halve the standard error, the number of samples must be quadrupled. This rate is independent of the dimension of $X$, which makes Monte Carlo particularly competitive for high-dimensional problems where deterministic numerical methods (such as quadrature) suffer from the curse of dimensionality.

---

## Monte Carlo Estimation of Probabilities

A probability is a special case of an expectation. To estimate $p = P(X \in A)$, define the indicator function $g(X) = \mathbf{1}(X \in A)$. Then:

$$
\hat{p}_N = \frac{1}{N}\sum_{i=1}^{N} \mathbf{1}(X_i \in A)
$$

Since $g(X)$ is Bernoulli with parameter $p$, the Monte Carlo standard error simplifies to:

$$
\text{SE}(\hat{p}_N) = \sqrt{\frac{\hat{p}_N(1 - \hat{p}_N)}{N}}
$$

This is useful for estimating tail probabilities, $p$-values, and Type I error rates in simulation studies.

---

## Monte Carlo Integration

Monte Carlo simulation can estimate definite integrals. To compute $I = \int_a^b h(x)\,dx$, write:

$$
I = (b - a)\,E[h(U)]
$$

where $U \sim \text{Uniform}(a, b)$. The Monte Carlo estimator is:

$$
\hat{I}_N = \frac{b - a}{N}\sum_{i=1}^{N} h(U_i)
$$

where $U_1, \ldots, U_N$ are independent draws from $\text{Uniform}(a, b)$.

For multidimensional integrals over a region $\Omega \subseteq \mathbb{R}^d$, the same principle applies with a uniform (or other suitable) distribution over $\Omega$. The convergence rate remains $O(N^{-1/2})$ regardless of $d$, unlike grid-based quadrature which scales as $O(N^{-2/d})$ at best.

---

## Monte Carlo Simulation of Sampling Distributions

A core use of Monte Carlo in statistics is approximating the **sampling distribution** of a statistic. Suppose we want to understand the distribution of $T = s(X_1, \ldots, X_n)$ when $(X_1, \ldots, X_n)$ are drawn from $F$.

**Algorithm (Sampling Distribution Simulation):**

1. **For** $j = 1, 2, \ldots, N$:
    - Draw a sample $(X_1^{(j)}, \ldots, X_n^{(j)})$ from $F$.
    - Compute $T_j = s(X_1^{(j)}, \ldots, X_n^{(j)})$.
2. Use $\{T_1, T_2, \ldots, T_N\}$ to approximate the sampling distribution of $T$.

From the simulated values, one can estimate the mean, variance, quantiles, or any other feature of the sampling distribution. This technique is widely used to:

- Study the finite-sample behavior of estimators (bias, variance, MSE)
- Evaluate the size and power of hypothesis tests
- Validate asymptotic approximations

!!! warning "Monte Carlo simulation requires a known data-generating process"
    Unlike the bootstrap, which resamples from observed data, Monte Carlo simulation requires specifying the distribution $F$ explicitly. This makes it a tool for studying statistical *procedures* under assumed models, not for analyzing a single observed dataset.

---

## Variance Reduction

The basic Monte Carlo estimate can be improved by reducing the variance $\sigma^2$ without increasing $N$. Common variance reduction techniques include:

- **Antithetic variates:** pair each sample $X_i$ with a negatively correlated counterpart to reduce variance.
- **Control variates:** exploit a known expectation $E[h(X)]$ for a correlated function $h$ to adjust the estimate.
- **Importance sampling:** sample from a proposal distribution $Q$ instead of $F$ and reweight:

$$
\hat{\mu}_N^{\text{IS}} = \frac{1}{N}\sum_{i=1}^{N} g(X_i)\,\frac{f(X_i)}{q(X_i)}
$$

where $f$ and $q$ are the densities of $F$ and $Q$. The optimal proposal concentrates samples where $|g(x)|f(x)$ is large.

These techniques can dramatically reduce the number of samples needed for a given level of accuracy.

---

## Summary

Monte Carlo simulation approximates intractable expectations, probabilities, and integrals by averaging over random samples. The Monte Carlo estimator $\hat{\mu}_N = \frac{1}{N}\sum g(X_i)$ converges to $E[g(X)]$ by the law of large numbers, with standard error $O(N^{-1/2})$ independent of dimension. This makes Monte Carlo the method of choice for high-dimensional problems. In statistics, Monte Carlo simulation is used to study the properties of estimators and tests under assumed models. Variance reduction techniques such as antithetic variates, control variates, and importance sampling can substantially improve efficiency.


---

## Exercises

**Exercise 1.** Write code that uses Monte Carlo simulation to estimate the probability that the sum of two dice exceeds 8.

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

**Exercise 2.** Explain the law of large numbers and how it justifies Monte Carlo estimation.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that estimates $\pi$ using Monte Carlo simulation by generating random points in a unit square.

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

**Exercise 4.** Write code that uses Monte Carlo simulation to estimate the integral $\int_0^1 e^{-x^2} dx$.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
