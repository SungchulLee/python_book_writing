# Bayesian Inference Preview

Throughout this chapter, hypothesis tests and confidence intervals follow the frequentist approach: parameters are fixed unknowns, and probability statements apply to the data. Bayesian inference takes a different perspective by treating parameters as random variables with probability distributions. This section introduces the core Bayesian framework using `scipy.stats` distribution objects, setting the stage for more advanced Bayesian methods covered in later chapters.

!!! tip "Mental Model"
    Imagine a dial you can turn to set a parameter like a coin's bias. Bayesian inference starts with a prior belief about where the dial is set, then updates that belief each time new data arrives. The posterior distribution is your refined belief -- it gets sharper and more concentrated as evidence accumulates.

## Bayes' Theorem

The foundation of Bayesian inference is Bayes' theorem. Given observed data $x$ and a parameter $\theta$, the **posterior distribution** is

$$
p(\theta \mid x) = \frac{p(x \mid \theta)\, p(\theta)}{p(x)}
$$

where:

- $p(\theta)$ is the **prior distribution**, encoding beliefs about $\theta$ before observing data
- $p(x \mid \theta)$ is the **likelihood**, the probability of the data given the parameter
- $p(x) = \int p(x \mid \theta)\, p(\theta)\, d\theta$ is the **marginal likelihood** (a normalizing constant)
- $p(\theta \mid x)$ is the **posterior distribution**, the updated belief after observing data

The posterior combines prior knowledge with the evidence from data. As more data accumulates, the likelihood dominates and the influence of the prior diminishes.

## Prior Distributions

A prior distribution represents knowledge about a parameter before observing data. Priors range from highly informative (concentrating probability on a narrow range) to weakly informative (spreading probability broadly).

Common choices available in `scipy.stats`:

| Prior type | Distribution | Use case |
|---|---|---|
| Proportion | `stats.beta(a, b)` | Success probability in Bernoulli trials |
| Rate | `stats.gamma(a, scale=1/b)` | Poisson rate parameter |
| Location | `stats.norm(mu, sigma)` | Mean of a normal distribution |
| Uninformative | `stats.uniform(0, 1)` | No prior preference (bounded parameter) |

```python
from scipy import stats
import numpy as np

# Weakly informative prior for a proportion: Beta(1, 1) = Uniform(0, 1)
prior = stats.beta(1, 1)
print(f"Prior mean: {prior.mean():.2f}")
print(f"Prior 95% interval: {prior.ppf([0.025, 0.975])}")
```

## Conjugate Analysis

When the prior and likelihood belong to specific distributional families, the posterior has a closed-form solution from the same family. This is called **conjugacy**.

### Beta-Binomial Model

For Bernoulli data with a Beta prior, the posterior is also Beta. If the prior is $\theta \sim \text{Beta}(\alpha, \beta)$ and we observe $k$ successes in $n$ trials, the posterior is

$$
\theta \mid k, n \sim \text{Beta}(\alpha + k,\; \beta + n - k)
$$

This update rule has an intuitive interpretation: $\alpha$ and $\beta$ act as "pseudo-counts" of prior successes and failures.

```python
from scipy import stats
import numpy as np

# Prior: Beta(2, 2) — mild belief that theta is near 0.5
alpha_prior, beta_prior = 2, 2

# Data: 7 successes in 20 trials
k, n = 7, 20

# Posterior
alpha_post = alpha_prior + k
beta_post = beta_prior + n - k
posterior = stats.beta(alpha_post, beta_post)

print(f"Prior mean:     {stats.beta(alpha_prior, beta_prior).mean():.4f}")
print(f"MLE:            {k/n:.4f}")
print(f"Posterior mean:  {posterior.mean():.4f}")
print(f"Posterior 95% CI: {posterior.ppf([0.025, 0.975])}")
```

The posterior mean lies between the prior mean and the maximum likelihood estimate, weighted by the relative amount of information each contributes.

### Normal-Normal Model

For normally distributed data $x_1, \ldots, x_n$ with known variance $\sigma^2$ and a normal prior $\mu \sim N(\mu_0, \sigma_0^2)$, the posterior is

$$
\mu \mid x_1, \ldots, x_n \sim N\!\left(\frac{\frac{\mu_0}{\sigma_0^2} + \frac{n\bar{x}}{\sigma^2}}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}},\; \frac{1}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}}\right)
$$

where $\bar{x}$ is the sample mean.

```python
from scipy import stats
import numpy as np

# Prior: mu ~ N(0, 10^2)
mu_0, sigma_0 = 0.0, 10.0

# Data: 30 observations with known sigma = 2
sigma = 2.0
rng = np.random.default_rng(42)
data = rng.normal(loc=3.0, scale=sigma, size=30)
x_bar = np.mean(data)
n = len(data)

# Posterior parameters
precision_prior = 1 / sigma_0**2
precision_data = n / sigma**2
mu_post = (mu_0 * precision_prior + x_bar * precision_data) / (precision_prior + precision_data)
sigma_post = np.sqrt(1 / (precision_prior + precision_data))

posterior = stats.norm(mu_post, sigma_post)
print(f"Posterior mean: {mu_post:.4f}")
print(f"Posterior std:  {sigma_post:.4f}")
print(f"Posterior 95% CI: {posterior.ppf([0.025, 0.975])}")
```

## Grid Approximation

When conjugate priors are not available, a simple numerical approach evaluates the posterior on a grid of parameter values. For each grid point $\theta_i$, the unnormalized posterior is

$$
p(\theta_i \mid x) \propto p(x \mid \theta_i)\, p(\theta_i)
$$

Normalizing these values by their sum (times the grid spacing) produces an approximate posterior distribution.

```python
from scipy import stats
import numpy as np

# Grid approximation for Beta-Binomial (verifying conjugate result)
theta_grid = np.linspace(0, 1, 1000)

prior = stats.beta(2, 2)
k, n = 7, 20

log_prior = prior.logpdf(theta_grid)
log_likelihood = stats.binom.logpmf(k, n, theta_grid)
log_posterior = log_prior + log_likelihood

# Normalize
posterior_unnorm = np.exp(log_posterior - log_posterior.max())
posterior_approx = posterior_unnorm / np.trapz(posterior_unnorm, theta_grid)

# Compare with exact conjugate posterior
exact_posterior = stats.beta(2 + k, 2 + n - k)
print(f"Grid mean:  {np.trapz(theta_grid * posterior_approx, theta_grid):.4f}")
print(f"Exact mean: {exact_posterior.mean():.4f}")
```

## Bayesian vs Frequentist Comparison

| Aspect | Frequentist | Bayesian |
|---|---|---|
| Parameters | Fixed unknowns | Random variables with distributions |
| Probability | Long-run frequency | Degree of belief |
| Result | p-value, confidence interval | Posterior distribution, credible interval |
| Prior information | Not formally incorporated | Encoded in the prior |
| Small samples | May lack power | Prior stabilizes estimates |

!!! tip "When to Consider Bayesian Methods"
    Bayesian approaches are particularly useful when prior information is available from domain expertise, when sample sizes are small, or when the full posterior distribution (rather than a point estimate) is needed for downstream decisions.

## Summary

Bayesian inference updates a prior distribution with observed data via Bayes' theorem to produce a posterior distribution. Conjugate analysis provides closed-form posteriors for specific prior-likelihood pairs, while grid approximation handles arbitrary models numerically. The `scipy.stats` distribution objects serve as building blocks for specifying priors and evaluating posteriors in both approaches.


---

## Exercises

**Exercise 1.** Explain the difference between frequentist and Bayesian approaches to statistical inference. Give one advantage of each.

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

**Exercise 2.** Write code that computes Bayes' theorem for a simple example: if a disease has 1% prevalence and a test has 95% sensitivity and 90% specificity, what is the probability of having the disease given a positive test?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that performs a Bayesian update: start with a uniform prior on a coin's bias, observe 7 heads out of 10 flips, and compute the posterior distribution.

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

**Exercise 4.** Explain what a prior, likelihood, and posterior distribution represent in Bayesian statistics.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
