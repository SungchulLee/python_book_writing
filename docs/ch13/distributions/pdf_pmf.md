# PDF and PMF

The **probability density function** (PDF) and **probability mass function** (PMF) describe how probability is distributed across the values a random variable can take. The PDF applies to continuous distributions, while the PMF applies to discrete distributions.

!!! tip "Mental Model"
    The PMF gives the actual probability of each discrete outcome, while the PDF gives the probability density -- a relative likelihood that must be integrated over an interval to yield a probability. A PDF value above 1 is perfectly valid; what matters is that the total area under the curve equals 1.

---

## Probability Density Function (PDF)

For a continuous random variable $X$, the PDF $f(x)$ gives the **relative likelihood** of $X$ taking a value near $x$. Crucially, $f(x)$ is not itself a probability — it can exceed 1. Probabilities are obtained by integrating the PDF over an interval:

$$P(a < X \le b) = \int_a^b f(x)\, dx$$

### Example: Normal Distribution PDF

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mu = 3.0
a = stats.norm(loc=mu)
x = np.linspace(mu - 3, mu + 3, 100)
y = a.pdf(x)

plt.plot(x, y, label='PDF')
plt.fill_between(x, y, alpha=0.3)
plt.title(f'Normal PDF (μ={mu}, σ=1)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.show()
```

The PDF peaks at the mean and decays symmetrically. The total area under the curve equals 1.

## Probability Mass Function (PMF)

For a discrete random variable $X$, the PMF $P(X = k)$ gives the **exact probability** that $X$ equals $k$. Unlike the PDF, PMF values are true probabilities and must satisfy:

$$\sum_k P(X = k) = 1$$

### Example: Poisson Distribution PMF

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mu = 3.0
a = stats.poisson(mu)
x = np.arange(0, 11)
y = a.pmf(x)

plt.bar(x, y, alpha=0.7, label='PMF')
plt.title(f'Poisson PMF (μ={mu})')
plt.xlabel('k')
plt.ylabel('P(X = k)')
plt.legend()
plt.show()
```

Each bar represents the exact probability of observing that count. The distribution is right-skewed for small $\mu$ and becomes more symmetric as $\mu$ increases.

## PDF vs PMF: Key Differences

| Property | PDF (Continuous) | PMF (Discrete) |
|----------|-----------------|-----------------|
| Method in `scipy.stats` | `.pdf(x)` | `.pmf(k)` |
| Values represent | Density (not probability) | Exact probability |
| Can exceed 1? | Yes | No |
| Sums/integrates to | $\int f(x)\,dx = 1$ | $\sum P(X=k) = 1$ |
| Plotting | Line plot | Bar chart |

## Evaluating PDF and PMF

Both `.pdf()` and `.pmf()` accept arrays for vectorized computation:

```python
# Continuous: evaluate PDF at multiple points
normal = stats.norm(loc=0, scale=1)
x_values = np.array([-2, -1, 0, 1, 2])
pdf_values = normal.pdf(x_values)
# [0.0540, 0.2420, 0.3989, 0.2420, 0.0540]

# Discrete: evaluate PMF at multiple points
poisson = stats.poisson(mu=5)
k_values = np.array([0, 3, 5, 7, 10])
pmf_values = poisson.pmf(k_values)
```

## Financial Context

In financial mathematics, the PDF is used extensively: the normal PDF models log-return densities, risk-neutral densities are extracted from option prices, and kernel density estimation (KDE) uses PDF evaluation to construct smooth empirical distributions from sample data.

## Summary

The PDF and PMF are the fundamental functions that characterize probability distributions. In `scipy.stats`, continuous distributions provide `.pdf()` and discrete distributions provide `.pmf()`, both accepting scalar or array inputs for efficient vectorized evaluation.

---

## Runnable Example: `solutions_basics.py`

```python
"""
Solutions 01: Basics of scipy.stats and Probability Distributions
=================================================================
Detailed solutions with explanations for all exercises.
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("="*80)
    print("SOLUTIONS: BASICS AND DISTRIBUTIONS")
    print("="*80)
    print()

    # Solution 1: Working with Normal Distribution
    print("Solution 1: Normal Distribution")
    print("-" * 40)
    print("Given: μ=10.0 cm, σ=0.5 cm")
    print()

    # Create the distribution
    normal_dist = stats.norm(loc=10.0, scale=0.5)

    # Part a
    prob_a = normal_dist.cdf(10.5) - normal_dist.cdf(9.5)
    print(f"a) P(9.5 < X < 10.5) = {prob_a:.4f} = {prob_a*100:.2f}%")
    print(f"   This is approximately 68% (μ ± σ rule)\n")

    # Part b
    percentile_95 = normal_dist.ppf(0.95)
    print(f"b) 95th percentile = {percentile_95:.4f} cm")
    print(f"   95% of parts are below this length\n")

    # Part c - Using Central Limit Theorem
    # Sample mean distribution: N(μ, σ²/n)
    n = 100
    mean_dist = stats.norm(loc=10.0, scale=0.5/np.sqrt(n))
    prob_c = mean_dist.cdf(10.1) - mean_dist.cdf(9.9)
    print(f"c) P(9.9 < X̄ < 10.1) = {prob_c:.4f}")
    print(f"   Sample mean has smaller variance: σ/√n = {0.5/np.sqrt(n):.4f}\n")

    print()

    # Solution 2: Binomial Distribution
    print("Solution 2: Binomial Distribution")
    print("-" * 40)
    print("Given: n=20 questions, p=0.25 (1 in 4 chance)")
    print()

    # Create the distribution
    binom_dist = stats.binom(n=20, p=0.25)

    # Part a
    expected = binom_dist.mean()
    print(f"a) Expected correct answers = np = {expected:.1f}")
    print()

    # Part b
    prob_8 = binom_dist.pmf(8)
    print(f"b) P(X = 8) = {prob_8:.4f}")
    print()

    # Part c
    prob_pass = binom_dist.sf(11)  # P(X >= 12) = P(X > 11)
    print(f"c) P(X ≥ 12) = {prob_pass:.4f}")
    print(f"   Very low probability of passing by guessing!\n")

    # Detailed explanation continues...
    print("="*80)
```

---

## Exercises

**Exercise 1.**
Evaluate the PDF of a normal distribution with $\mu = 10$ and $\sigma = 3$ at the points $x = 7, 10, 13$. Verify that the PDF at the mean is $1/(\sigma\sqrt{2\pi})$.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        rv = stats.norm(loc=10, scale=3)
        for x in [7, 10, 13]:
            print(f"PDF at x={x}: {rv.pdf(x):.6f}")

        expected_peak = 1 / (3 * np.sqrt(2 * np.pi))
        print(f"1/(sigma*sqrt(2pi)) = {expected_peak:.6f}")
        print(f"Match: {np.isclose(rv.pdf(10), expected_peak)}")

---

**Exercise 2.**
Compute the PMF of a Poisson distribution with $\lambda = 5$ for $k = 0, 1, \ldots, 15$. Find the value of $k$ that maximizes the PMF and verify that the PMF values sum to approximately 1.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        rv = stats.poisson(mu=5)
        k_vals = np.arange(0, 16)
        pmf_vals = rv.pmf(k_vals)

        print(f"k with max PMF: {k_vals[np.argmax(pmf_vals)]}")
        print(f"Sum of PMF (k=0..15): {pmf_vals.sum():.6f}")

---

**Exercise 3.**
Generate 10,000 samples from a standard normal distribution with `.rvs()`. Plot a normalized histogram of the samples and overlay the theoretical PDF using `.pdf()`. Visually confirm that they match.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats
        import matplotlib.pyplot as plt

        rv = stats.norm()
        samples = rv.rvs(size=10000, random_state=42)
        x = np.linspace(-4, 4, 200)

        plt.hist(samples, bins=50, density=True, alpha=0.6, label='Histogram')
        plt.plot(x, rv.pdf(x), 'r-', lw=2, label='PDF')
        plt.legend()
        plt.title('Standard Normal: Histogram vs PDF')
        plt.show()
