# rv_continuous and rv_discrete

All probability distributions in `scipy.stats` inherit from one of two base classes: `rv_continuous` for continuous distributions and `rv_discrete` for discrete distributions. Understanding these base classes reveals the unified design behind the entire `scipy.stats` distribution system.

!!! tip "Mental Model"
    Every distribution in `scipy.stats` is a specialized version of the same blueprint. `rv_continuous` provides `.pdf()`, `.cdf()`, `.ppf()`, `.rvs()`, and `.fit()` for any continuous distribution; `rv_discrete` provides the analogous `.pmf()` interface. Once you learn one distribution's API, you know them all.

---

## The Distribution Class Hierarchy

Every distribution in `scipy.stats` is an instance of either `rv_continuous` or `rv_discrete`, both of which inherit from `rv_generic`:

```
rv_generic
├── rv_continuous  →  norm, expon, gamma, chi2, t, f, beta, ...
└── rv_discrete    →  binom, poisson, geom, hypergeom, nbinom, ...
```

When you write `stats.norm(loc=3.0)`, you are calling `rv_continuous.__call__()` which returns a **frozen distribution** — an object with fixed parameters.

## rv_continuous

Continuous distributions are defined on intervals of the real line and provide the `.pdf()` method for the probability density function:

```python
import scipy.stats as stats
import numpy as np

# stats.norm is an instance of rv_continuous
a = stats.norm(loc=3.0)        # frozen: mean=3, std=1
samples = a.rvs(size=(2, 3), random_state=1)
print(samples)
print(type(samples))   # <class 'numpy.ndarray'>
print(samples.shape)   # (2, 3)
print(samples.dtype)   # float64

# Key methods: pdf, cdf, sf, ppf, isf, rvs, fit, mean, var, std, entropy
```

## rv_discrete

Discrete distributions are defined on countable sets (typically non-negative integers) and provide the `.pmf()` method for the probability mass function:

```python
# stats.poisson is an instance of rv_discrete
b = stats.poisson(mu=3.0)      # frozen: mean=3
print(b.pmf(3))                # P(X = 3) — exact probability
print(b.cdf(5))                # P(X ≤ 5)
```

The key difference: discrete distributions use `.pmf(k)` where continuous distributions use `.pdf(x)`. All other methods (`.cdf()`, `.sf()`, `.ppf()`, `.rvs()`, etc.) work identically.

## Common Interface

Both `rv_continuous` and `rv_discrete` share a consistent interface through `rv_generic`:

| Method | Continuous | Discrete | Description |
|--------|-----------|----------|-------------|
| Density/Mass | `.pdf(x)` | `.pmf(k)` | Density or mass at a point |
| Log density | `.logpdf(x)` | `.logpmf(k)` | Log of density/mass (numerically stable) |
| CDF | `.cdf(x)` | `.cdf(k)` | $P(X \le x)$ |
| Survival | `.sf(x)` | `.sf(k)` | $P(X > x)$ |
| Quantile | `.ppf(q)` | `.ppf(q)` | Inverse CDF |
| Sampling | `.rvs(size)` | `.rvs(size)` | Random variates |
| Moments | `.mean()`, `.var()` | `.mean()`, `.var()` | Theoretical moments |
| Fit | `.fit(data)` | — | MLE parameter estimation |

## Frozen vs Unfrozen

The base classes support two usage patterns. In the unfrozen pattern, parameters are passed to each method call: `stats.norm.pdf(0, loc=3, scale=1)`. In the frozen pattern, a distribution object is created once and methods are called without parameters: `a = stats.norm(loc=3, scale=1); a.pdf(0)`. The frozen pattern is preferred for clarity and efficiency.

## Summary

The `rv_continuous` and `rv_discrete` base classes define the unified API that makes `scipy.stats` distributions interchangeable. By understanding this class hierarchy, you can write generic code that works with any distribution and leverage the full suite of methods consistently.

---

## Runnable Example: `basics_distributions.py`

```python
"""
Tutorial 01: Introduction to scipy.stats - Basics and Probability Distributions
===============================================================================
Level: Beginner
Topics: Installing scipy, basic imports, understanding distributions,
        probability density functions (PDF), cumulative distribution functions (CDF)

This module introduces the scipy.stats package and fundamental concepts
of working with probability distributions in Python.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# =============================================================================
# SECTION 1: Introduction to scipy.stats
# =============================================================================

if __name__ == "__main__":
    """
    scipy.stats is a sub-package of SciPy that provides:
    - A large collection of probability distributions
    - Statistical functions for descriptive statistics
    - Statistical tests (hypothesis testing)
    - Correlation and regression analysis

    The package contains two main types of distribution objects:
    1. Continuous distributions (e.g., normal, exponential, uniform)
    2. Discrete distributions (e.g., binomial, Poisson, geometric)
    """

    # =============================================================================
    # SECTION 2: Understanding Distribution Objects
    # =============================================================================

    # Creating a normal distribution object
    # ---------------------------------------
    # The normal distribution is characterized by two parameters:
    # - loc: mean (μ) - center of the distribution
    # - scale: standard deviation (σ) - spread of the distribution

    # Standard normal distribution (mean=0, std=1)
    standard_normal = stats.norm(loc=0, scale=1)
    print("Standard Normal Distribution:")
    print(f"  Mean: {standard_normal.mean()}")  # Expected value
    print(f"  Variance: {standard_normal.var()}")  # Variance
    print(f"  Standard Deviation: {standard_normal.std()}")  # Standard deviation
    print()

    # Custom normal distribution (mean=10, std=2)
    custom_normal = stats.norm(loc=10, scale=2)
    print("Custom Normal Distribution (μ=10, σ=2):")
    print(f"  Mean: {custom_normal.mean()}")
    print(f"  Variance: {custom_normal.var()}")
    print(f"  Standard Deviation: {custom_normal.std()}")
    print()

    # =============================================================================
    # SECTION 3: Probability Density Function (PDF)
    # =============================================================================
    """
    The PDF gives the relative likelihood of a continuous random variable
    taking on a specific value. For a normal distribution, the PDF is:

        f(x) = (1 / (σ√(2π))) * exp(-(x-μ)²/(2σ²))

    Key point: PDF values are NOT probabilities (they can exceed 1)!
    Probabilities for continuous distributions are computed over intervals.
    """

    # Evaluate PDF at specific points
    x_value = 0.0
    pdf_value = standard_normal.pdf(x_value)
    print(f"PDF of standard normal at x={x_value}: {pdf_value:.4f}")
    # This tells us the height of the distribution curve at x=0

    # Evaluate PDF at multiple points
    x_values = np.array([-2, -1, 0, 1, 2])
    pdf_values = standard_normal.pdf(x_values)
    print(f"PDF values at x={x_values}: {pdf_values}")
    print()

    # Visualizing the PDF
    # --------------------
    # Generate 1000 points between -4 and 4
    x_range = np.linspace(-4, 4, 1000)
    # Calculate PDF for each point
    pdf_standard = standard_normal.pdf(x_range)
    pdf_custom = custom_normal.pdf(x_range)

    # Create visualization
    plt.figure(figsize=(12, 5))

    # Plot 1: Standard Normal PDF
    plt.subplot(1, 2, 1)
    plt.plot(x_range, pdf_standard, 'b-', linewidth=2, label='N(0,1)')
    plt.fill_between(x_range, pdf_standard, alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Standard Normal Distribution PDF')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Plot 2: Comparing PDFs
    plt.subplot(1, 2, 2)
    x_range2 = np.linspace(0, 20, 1000)
    plt.plot(x_range, pdf_standard, 'b-', linewidth=2, label='N(0,1)')
    plt.plot(x_range2, custom_normal.pdf(x_range2), 'r-', linewidth=2, label='N(10,2)')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Comparing Normal Distribution PDFs')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/01_pdf_visualization.png', dpi=300, bbox_inches='tight')
    print("Saved: 01_pdf_visualization.png")
    plt.close()

    # =============================================================================
    # SECTION 4: Cumulative Distribution Function (CDF)
    # =============================================================================
    """
    The CDF gives the probability that a random variable X is less than or
    equal to a value x:

        F(x) = P(X ≤ x)

    Properties of CDF:
    - Always increases (non-decreasing)
    - Ranges from 0 to 1
    - F(-∞) = 0 and F(∞) = 1
    """

    # Calculate CDF values
    x_test = 0.0
    cdf_value = standard_normal.cdf(x_test)
    print(f"CDF of standard normal at x={x_test}: {cdf_value:.4f}")
    # This means P(X ≤ 0) = 0.5 (50% of values are below 0)

    # CDF at multiple points
    x_test_values = np.array([-2, -1, 0, 1, 2])
    cdf_values = standard_normal.cdf(x_test_values)
    print(f"CDF values at x={x_test_values}:")
    for x, cdf in zip(x_test_values, cdf_values):
        print(f"  P(X ≤ {x:2.0f}) = {cdf:.4f} ({cdf*100:.2f}%)")
    print()

    # Visualizing the CDF
    # --------------------
    cdf_standard = standard_normal.cdf(x_range)
    cdf_custom = custom_normal.cdf(x_range2)

    plt.figure(figsize=(12, 5))

    # Plot 1: Standard Normal CDF
    plt.subplot(1, 2, 1)
    plt.plot(x_range, cdf_standard, 'b-', linewidth=2)
    plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.5, label='Median (CDF=0.5)')
    plt.axvline(x=0, color='r', linestyle='--', alpha=0.5)
    plt.xlabel('x')
    plt.ylabel('Cumulative Probability')
    plt.title('Standard Normal Distribution CDF')
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Plot 2: Comparing CDFs
    plt.subplot(1, 2, 2)
    plt.plot(x_range, cdf_standard, 'b-', linewidth=2, label='N(0,1)')
    plt.plot(x_range2, cdf_custom, 'r-', linewidth=2, label='N(10,2)')
    plt.xlabel('x')
    plt.ylabel('Cumulative Probability')
    plt.title('Comparing Normal Distribution CDFs')
    plt.grid(True, alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/01_cdf_visualization.png', dpi=300, bbox_inches='tight')
    print("Saved: 01_cdf_visualization.png")
    plt.close()

    # =============================================================================
    # SECTION 5: Computing Probabilities Over Intervals
    # =============================================================================
    """
    For continuous distributions, we compute probabilities over intervals:
    P(a < X ≤ b) = F(b) - F(a) = CDF(b) - CDF(a)
    """

    # Example: P(-1 < X ≤ 1) for standard normal
    a, b = -1, 1
    prob_interval = standard_normal.cdf(b) - standard_normal.cdf(a)
    print(f"P({a} < X ≤ {b}) = {prob_interval:.4f} ({prob_interval*100:.2f}%)")

    # This is approximately 68% (the 68-95-99.7 rule!)
    # About 68% of data falls within 1 standard deviation of the mean

    # Example: P(X > 2) for standard normal
    x_threshold = 2
    prob_above = 1 - standard_normal.cdf(x_threshold)
    print(f"P(X > {x_threshold}) = {prob_above:.4f} ({prob_above*100:.2f}%)")

    # Alternative using survival function (sf)
    # The survival function is defined as sf(x) = 1 - cdf(x) = P(X > x)
    prob_above_sf = standard_normal.sf(x_threshold)
    print(f"P(X > {x_threshold}) using sf = {prob_above_sf:.4f}")
    print()

    # =============================================================================
    # SECTION 6: Percent Point Function (Inverse CDF/Quantiles)
    # =============================================================================
    """
    The percent point function (PPF) is the inverse of the CDF.
    Given a probability p, it returns the value x such that P(X ≤ x) = p

    ppf(p) = CDF^(-1)(p)

    This is used to find quantiles and percentiles.
    """

    # Find the median (50th percentile)
    median = standard_normal.ppf(0.5)
    print(f"Median (50th percentile): {median:.4f}")

    # Find the 95th percentile
    percentile_95 = standard_normal.ppf(0.95)
    print(f"95th percentile: {percentile_95:.4f}")
    # This means 95% of values are below this value

    # Find the quartiles
    q1 = standard_normal.ppf(0.25)  # 25th percentile
    q2 = standard_normal.ppf(0.50)  # 50th percentile (median)
    q3 = standard_normal.ppf(0.75)  # 75th percentile
    print(f"Quartiles: Q1={q1:.4f}, Q2={q2:.4f}, Q3={q3:.4f}")

    # Verify: CDF and PPF are inverses
    p_test = 0.75
    x_from_ppf = standard_normal.ppf(p_test)
    p_from_cdf = standard_normal.cdf(x_from_ppf)
    print(f"\nVerification: ppf({p_test}) = {x_from_ppf:.4f}")
    print(f"              cdf({x_from_ppf:.4f}) = {p_from_cdf:.4f}")
    print()

    # =============================================================================
    # SECTION 7: Random Variate Generation
    # =============================================================================
    """
    Generate random samples from a distribution using the rvs() method.
    This is useful for simulations and Monte Carlo methods.
    """

    # Generate random samples
    np.random.seed(42)  # Set seed for reproducibility
    samples = standard_normal.rvs(size=1000)  # Generate 1000 random samples

    print(f"Generated {len(samples)} samples from N(0,1)")
    print(f"Sample mean: {np.mean(samples):.4f} (theoretical: 0.0)")
    print(f"Sample std: {np.std(samples, ddof=1):.4f} (theoretical: 1.0)")
    print()

    # Visualize the samples
    plt.figure(figsize=(14, 5))

    # Plot 1: Histogram of samples vs. theoretical PDF
    plt.subplot(1, 3, 1)
    plt.hist(samples, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black')
    plt.plot(x_range, pdf_standard, 'r-', linewidth=2, label='Theoretical PDF')
    plt.xlabel('x')
    plt.ylabel('Density')
    plt.title('Histogram vs. Theoretical PDF')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Empirical CDF vs. Theoretical CDF
    plt.subplot(1, 3, 2)
    sorted_samples = np.sort(samples)
    empirical_cdf = np.arange(1, len(sorted_samples) + 1) / len(sorted_samples)
    plt.plot(sorted_samples, empirical_cdf, 'b-', linewidth=1, alpha=0.7, label='Empirical CDF')
    plt.plot(x_range, cdf_standard, 'r-', linewidth=2, label='Theoretical CDF')
    plt.xlabel('x')
    plt.ylabel('Cumulative Probability')
    plt.title('Empirical vs. Theoretical CDF')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 3: Q-Q plot (Quantile-Quantile plot)
    plt.subplot(1, 3, 3)
    stats.probplot(samples, dist="norm", plot=plt)
    plt.title('Q-Q Plot (Normal)')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/01_random_samples.png', dpi=300, bbox_inches='tight')
    print("Saved: 01_random_samples.png")
    plt.close()

    # =============================================================================
    # SECTION 8: Other Common Continuous Distributions
    # =============================================================================

    # Uniform Distribution
    # ---------------------
    # All values in [a, b] are equally likely
    # Parameters: loc=a, scale=(b-a)
    uniform = stats.uniform(loc=0, scale=10)  # Uniform on [0, 10]
    print("Uniform Distribution [0, 10]:")
    print(f"  Mean: {uniform.mean():.4f}")
    print(f"  Variance: {uniform.var():.4f}")
    print(f"  P(3 < X ≤ 7) = {uniform.cdf(7) - uniform.cdf(3):.4f}")
    print()

    # Exponential Distribution
    # -------------------------
    # Models time between events in a Poisson process
    # Parameter: scale = 1/λ (where λ is the rate parameter)
    exponential = stats.expon(scale=2)  # Mean time = 2
    print("Exponential Distribution (λ=0.5):")
    print(f"  Mean: {exponential.mean():.4f}")
    print(f"  Variance: {exponential.var():.4f}")
    print(f"  P(X > 3) = {exponential.sf(3):.4f}")
    print()

    # Student's t-Distribution
    # --------------------------
    # Similar to normal but with heavier tails
    # Parameter: df (degrees of freedom)
    t_dist = stats.t(df=5)  # 5 degrees of freedom
    print("Student's t-Distribution (df=5):")
    print(f"  Mean: {t_dist.mean():.4f}")
    print(f"  Variance: {t_dist.var():.4f}")
    print()

    # Visualize various distributions
    plt.figure(figsize=(14, 5))

    x_unif = np.linspace(-1, 11, 1000)
    x_exp = np.linspace(0, 10, 1000)
    x_t = np.linspace(-4, 4, 1000)

    plt.subplot(1, 3, 1)
    plt.plot(x_unif, uniform.pdf(x_unif), 'b-', linewidth=2)
    plt.fill_between(x_unif, uniform.pdf(x_unif), alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Uniform Distribution [0, 10]')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 3, 2)
    plt.plot(x_exp, exponential.pdf(x_exp), 'r-', linewidth=2)
    plt.fill_between(x_exp, exponential.pdf(x_exp), alpha=0.3)
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Exponential Distribution (scale=2)')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 3, 3)
    plt.plot(x_t, t_dist.pdf(x_t), 'g-', linewidth=2, label='t(df=5)')
    plt.plot(x_range, standard_normal.pdf(x_range), 'b--', linewidth=2, label='N(0,1)')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title("Student's t vs. Normal")
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/01_various_distributions.png', dpi=300, bbox_inches='tight')
    print("Saved: 01_various_distributions.png")
    plt.close()

    # =============================================================================
    # SECTION 9: Summary Statistics from Distributions
    # =============================================================================
    """
    Distribution objects provide methods to compute theoretical moments
    and statistics without needing to generate samples.
    """

    print("Summary Statistics:")
    print("-" * 50)
    distributions = [
        ("Normal(0,1)", standard_normal),
        ("Normal(10,2)", custom_normal),
        ("Uniform[0,10]", uniform),
        ("Exponential(scale=2)", exponential),
    ]

    for name, dist in distributions:
        print(f"\n{name}:")
        print(f"  Mean:     {dist.mean():.4f}")
        print(f"  Variance: {dist.var():.4f}")
        print(f"  Std Dev:  {dist.std():.4f}")
        # Some distributions have median and entropy methods
        if hasattr(dist, 'median'):
            print(f"  Median:   {dist.median():.4f}")
        if hasattr(dist, 'entropy'):
            print(f"  Entropy:  {dist.entropy():.4f}")

    print("\n" + "="*80)
    print("Tutorial 01 Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("1. scipy.stats provides distribution objects with consistent interfaces")
    print("2. PDF shows the shape of the distribution (not probability values)")
    print("3. CDF gives cumulative probabilities: P(X ≤ x)")
    print("4. PPF is the inverse of CDF, used for finding quantiles")
    print("5. rvs() generates random samples from the distribution")
    print("6. Distribution objects have methods for mean, variance, and other statistics")
```

---

## Exercises

**Exercise 1.**
Use `scipy.stats` to create a frozen standard normal distribution and a frozen Poisson distribution with $\mu = 4$. For each, compute the mean and variance using the `.stats(moments='mv')` method and print the results.

??? success "Solution to Exercise 1"

        from scipy import stats

        norm_rv = stats.norm(loc=0, scale=1)
        pois_rv = stats.poisson(mu=4)

        print("Normal:", norm_rv.stats(moments='mv'))
        print("Poisson:", pois_rv.stats(moments='mv'))

---

**Exercise 2.**
Write a short script that counts how many continuous and how many discrete distributions are available in `scipy.stats` by checking which names are instances of `rv_continuous` and `rv_discrete`. Print both counts.

??? success "Solution to Exercise 2"

        from scipy import stats
        from scipy.stats import rv_continuous, rv_discrete

        n_cont = sum(1 for name in dir(stats) if isinstance(getattr(stats, name), rv_continuous))
        n_disc = sum(1 for name in dir(stats) if isinstance(getattr(stats, name), rv_discrete))
        print(f"Continuous: {n_cont}, Discrete: {n_disc}")

---

**Exercise 3.**
Create a frozen chi-square distribution with 5 degrees of freedom. Draw 1000 samples with `.rvs()`, then compare the sample mean and variance to the theoretical values from `.mean()` and `.var()`.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        chi2_rv = stats.chi2(df=5)
        samples = chi2_rv.rvs(size=1000, random_state=42)

        print(f"Theoretical mean: {chi2_rv.mean():.4f}, Sample mean: {np.mean(samples):.4f}")
        print(f"Theoretical var:  {chi2_rv.var():.4f}, Sample var:  {np.var(samples, ddof=1):.4f}")
