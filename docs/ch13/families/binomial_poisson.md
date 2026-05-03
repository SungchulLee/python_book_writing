# Binomial and Poisson

The binomial and Poisson distributions are the two most important discrete distributions in statistics and financial mathematics. The binomial counts successes in a fixed number of trials, while the Poisson counts events occurring at a constant average rate.

!!! tip "Mental Model"
    The binomial counts successes in a fixed number of coin flips; the Poisson counts events arriving randomly over time. When the number of trials $n$ is large and the success probability $p$ is small, the binomial converges to the Poisson with rate $\lambda = np$ -- this is the "rare events" approximation.

---

## Binomial Distribution

The binomial distribution models the number of successes in $n$ independent Bernoulli trials, each with success probability $p$:

$$P(X = k) = \binom{n}{k} p^k (1-p)^{n-k}, \quad k = 0, 1, \ldots, n$$

### Usage in scipy.stats

```python
import scipy.stats as stats

# 100 trials with 60% success probability
n, p = 100, 0.6
binom_dist = stats.binom(n, p)

print(f"Mean: {binom_dist.mean():.2f}")       # np = 60
print(f"Variance: {binom_dist.var():.2f}")     # np(1-p) = 24
print(f"P(X = 60): {binom_dist.pmf(60):.4f}")
print(f"P(X ≤ 55): {binom_dist.cdf(55):.4f}")
```

### Visualizing Samples vs Theory

A powerful way to verify understanding is to overlay a histogram of random samples with the theoretical PMF:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

n_, p_ = 100, 0.6
a = stats.binom(n_, p_)
x_samples = a.rvs(size=10000, random_state=337)
x_theory = np.arange(101)
y_theory = a.pmf(x_theory)

plt.plot(x_theory, y_theory, color='r', label='Theoretical PMF')
plt.hist(x_samples, density=True, bins=20, alpha=0.7, label='Sampled histogram')
plt.legend()
plt.title(f'Binomial(n={n_}, p={p_}): Samples vs Theory')
plt.xlabel('k')
plt.ylabel('Probability')
plt.show()
```

## Poisson Distribution

The Poisson distribution models the number of events occurring in a fixed interval when events happen at a constant average rate $\mu$:

$$P(X = k) = \frac{\mu^k e^{-\mu}}{k!}, \quad k = 0, 1, 2, \ldots$$

A distinctive property is that the mean equals the variance: $E[X] = \text{Var}(X) = \mu$.

### Usage in scipy.stats

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mu = 3.0
a = stats.poisson(mu)
x = np.arange(0, 11)
y_pmf = a.pmf(x)
y_cdf = a.cdf(x)

plt.bar(x, y_cdf, label='CDF', alpha=0.5)
plt.bar(x, y_pmf, label='PMF', alpha=0.5)
plt.legend()
plt.title(f'Poisson Distribution (μ={mu})')
plt.xlabel('k')
plt.show()
```

The PMF bars show the probability of each count $k$, while the CDF bars show the cumulative probability $P(X \le k)$. For $\mu = 3$, the mode is at $k = 2$ and $k = 3$, and the distribution is slightly right-skewed.

## Relationship: Poisson as Limit of Binomial

When $n$ is large and $p$ is small, the binomial distribution is well-approximated by the Poisson distribution with $\mu = np$:

$$\text{Binom}(n, p) \approx \text{Poisson}(np), \quad \text{for large } n, \text{ small } p$$

This is useful in practice because the Poisson distribution has a simpler form and only one parameter.

## Financial Applications

The binomial distribution appears in the binomial option pricing model (Cox-Ross-Rubinstein), where asset prices move up or down at each step. It also models the number of defaults in a credit portfolio when default events are independent. The Poisson distribution models the number of trades in a time interval, insurance claim counts, and jump events in jump-diffusion models for asset prices.

## Summary

The binomial and Poisson distributions are workhorses of discrete probability. In `scipy.stats`, use `stats.binom(n, p)` and `stats.poisson(mu)` to create frozen distributions, then call `.pmf()`, `.cdf()`, `.rvs()`, and other methods as needed.

---

## Runnable Example: `discrete_distributions.py`

```python
"""
Tutorial 03: Discrete Probability Distributions
===============================================
Level: Beginner-Intermediate
Topics: Bernoulli, binomial, geometric, negative binomial, Poisson,
        hypergeometric, and multinomial distributions

This module explores discrete probability distributions in scipy.stats
and their applications in counting, probability, and statistical modeling.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.special import comb

# =============================================================================
# SECTION 1: Discrete vs. Continuous Distributions
# =============================================================================

if __name__ == "__main__":
    """
    Key Differences:
    ----------------
    Continuous Distributions:
    - PDF (Probability Density Function): f(x)
    - CDF: P(X ≤ x)
    - Defined on intervals (e.g., all real numbers, [0, ∞))

    Discrete Distributions:
    - PMF (Probability Mass Function): P(X = k)
    - CDF: P(X ≤ k)
    - Defined on countable values (e.g., {0, 1, 2, 3, ...})

    In scipy.stats, discrete distributions use .pmf() instead of .pdf()
    """

    print("="*80)
    print("DISCRETE PROBABILITY DISTRIBUTIONS")
    print("="*80)
    print()

    # =============================================================================
    # SECTION 2: Bernoulli Distribution
    # =============================================================================
    """
    The simplest discrete distribution: models a single trial with two outcomes.

    PMF: P(X = k) = p^k * (1-p)^(1-k) for k ∈ {0, 1}

    Parameter:
    - p: probability of success (0 ≤ p ≤ 1)

    Properties:
    - Mean: E[X] = p
    - Variance: Var(X) = p(1-p)

    Applications:
    - Coin flip (fair: p=0.5, biased: p≠0.5)
    - Success/failure of a single trial
    - Binary classification outcomes
    """

    # Create Bernoulli distributions
    bernoulli_fair = stats.bernoulli(p=0.5)  # Fair coin
    bernoulli_biased = stats.bernoulli(p=0.7)  # Biased coin (70% heads)

    print("BERNOULLI DISTRIBUTION")
    print("-" * 40)
    print("Fair coin (p=0.5):")
    print(f"  P(X=0) = {bernoulli_fair.pmf(0):.4f}")
    print(f"  P(X=1) = {bernoulli_fair.pmf(1):.4f}")
    print(f"  Mean: {bernoulli_fair.mean():.4f}")
    print(f"  Variance: {bernoulli_fair.var():.4f}")
    print()

    print("Biased coin (p=0.7):")
    print(f"  P(X=0) = {bernoulli_biased.pmf(0):.4f}")
    print(f"  P(X=1) = {bernoulli_biased.pmf(1):.4f}")
    print(f"  Mean: {bernoulli_biased.mean():.4f}")
    print(f"  Variance: {bernoulli_biased.var():.4f}")
    print()

    # Visualize Bernoulli distributions
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for ax, (dist, p, title) in zip(axes, 
                                     [(bernoulli_fair, 0.5, "Fair Coin (p=0.5)"),
                                      (bernoulli_biased, 0.7, "Biased Coin (p=0.7)")]):
        x = [0, 1]
        pmf_values = [dist.pmf(k) for k in x]
        ax.bar(x, pmf_values, width=0.4, alpha=0.7, edgecolor='black')
        ax.set_xlabel('Outcome')
        ax.set_ylabel('Probability')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(['Failure (0)', 'Success (1)'])
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/03_bernoulli.png', dpi=300, bbox_inches='tight')
    print("Saved: 03_bernoulli.png\n")
    plt.close()

    # =============================================================================
    # SECTION 3: Binomial Distribution
    # =============================================================================
    """
    Models the number of successes in n independent Bernoulli trials.

    PMF: P(X = k) = C(n,k) * p^k * (1-p)^(n-k)
         where C(n,k) = n! / (k!(n-k)!) is the binomial coefficient

    Parameters:
    - n: number of trials
    - p: probability of success in each trial

    Properties:
    - Mean: E[X] = np
    - Variance: Var(X) = np(1-p)
    - Sum of n independent Bernoulli(p) ~ Binomial(n, p)

    Applications:
    - Number of heads in n coin flips
    - Number of defective items in a batch
    - Number of successful conversions in marketing
    - Quality control sampling
    """

    print("BINOMIAL DISTRIBUTION")
    print("-" * 40)

    # Example: Flipping a fair coin 10 times
    n = 10  # Number of trials
    p = 0.5  # Probability of success (heads)
    binomial = stats.binom(n, p)

    print(f"Binomial({n}, {p}) - Coin flips:")
    print(f"  Mean: {binomial.mean():.2f} (expected number of heads)")
    print(f"  Variance: {binomial.var():.2f}")
    print(f"  Std Dev: {binomial.std():.2f}")
    print()

    # Probability calculations
    print("Probability calculations:")
    print(f"  P(X = 5) = {binomial.pmf(5):.4f} (exactly 5 heads)")
    print(f"  P(X ≤ 3) = {binomial.cdf(3):.4f} (at most 3 heads)")
    print(f"  P(X ≥ 7) = {binomial.sf(6):.4f} (at least 7 heads)")
    print(f"  P(3 ≤ X ≤ 7) = {binomial.cdf(7) - binomial.cdf(2):.4f}")
    print()

    # Visualize binomial distribution
    x = np.arange(0, n+1)
    pmf_values = binomial.pmf(x)
    cdf_values = binomial.cdf(x)

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: PMF
    axes[0, 0].bar(x, pmf_values, alpha=0.7, edgecolor='black')
    axes[0, 0].set_xlabel('Number of Heads (k)')
    axes[0, 0].set_ylabel('Probability P(X = k)')
    axes[0, 0].set_title(f'Binomial({n}, {p}) - PMF')
    axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: CDF
    axes[0, 1].step(x, cdf_values, where='post', linewidth=2)
    axes[0, 1].scatter(x, cdf_values, color='red', zorder=3)
    axes[0, 1].set_xlabel('k')
    axes[0, 1].set_ylabel('Cumulative Probability P(X ≤ k)')
    axes[0, 1].set_title(f'Binomial({n}, {p}) - CDF')
    axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: Effect of p (n fixed)
    n_fixed = 20
    for p_val in [0.2, 0.5, 0.8]:
        binom_temp = stats.binom(n_fixed, p_val)
        x_temp = np.arange(0, n_fixed+1)
        axes[1, 0].plot(x_temp, binom_temp.pmf(x_temp), marker='o', 
                        label=f'p={p_val}', linewidth=2)

    axes[1, 0].set_xlabel('k')
    axes[1, 0].set_ylabel('Probability')
    axes[1, 0].set_title(f'Effect of p (n={n_fixed} fixed)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Effect of n (p fixed)
    p_fixed = 0.5
    for n_val in [10, 20, 50]:
        binom_temp = stats.binom(n_val, p_fixed)
        x_temp = np.arange(0, n_val+1)
        axes[1, 1].plot(x_temp, binom_temp.pmf(x_temp), marker='o', 
                        label=f'n={n_val}', linewidth=2, alpha=0.7)

    axes[1, 1].set_xlabel('k')
    axes[1, 1].set_ylabel('Probability')
    axes[1, 1].set_title(f'Effect of n (p={p_fixed} fixed)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/03_binomial.png', dpi=300, bbox_inches='tight')
    print("Saved: 03_binomial.png\n")
    plt.close()

    # Real-world application: Quality control
    print("Application: Quality Control")
    print("-" * 40)
    n_products = 100
    defect_rate = 0.05  # 5% defect rate
    qc_binom = stats.binom(n_products, defect_rate)

    print(f"Inspecting {n_products} products with {defect_rate*100:.0f}% defect rate:")
    print(f"  Expected defects: {qc_binom.mean():.2f}")
    print(f"  P(≤ 3 defects) = {qc_binom.cdf(3):.4f}")
    print(f"  P(> 10 defects) = {qc_binom.sf(10):.4f} (unusual, may indicate problem)")
    print()

    # =============================================================================
    # SECTION 4: Geometric Distribution
    # =============================================================================
    """
    Models the number of trials needed to get the first success.

    PMF: P(X = k) = (1-p)^(k-1) * p for k = 1, 2, 3, ...

    Parameter:
    - p: probability of success

    Properties:
    - Mean: E[X] = 1/p
    - Variance: Var(X) = (1-p)/p²
    - Memoryless property (like exponential)

    Applications:
    - Number of attempts until first success
    - Number of job interviews until getting hired
    - Number of at-bats until first hit
    """

    print("GEOMETRIC DISTRIBUTION")
    print("-" * 40)

    p_success = 0.3  # 30% success rate
    geometric = stats.geom(p_success)

    print(f"Geometric({p_success}):")
    print(f"  Mean trials to success: {geometric.mean():.2f}")
    print(f"  Variance: {geometric.var():.2f}")
    print()

    print("Probability calculations:")
    print(f"  P(1st success on trial 1) = {geometric.pmf(1):.4f}")
    print(f"  P(1st success on trial 3) = {geometric.pmf(3):.4f}")
    print(f"  P(1st success within 5 trials) = {geometric.cdf(5):.4f}")
    print(f"  P(need more than 10 trials) = {geometric.sf(10):.4f}")
    print()

    # Memoryless property
    # If we've already failed k times, the distribution of additional trials
    # is the same as starting fresh
    k = 3
    prob_succeed_within_5 = geometric.cdf(5)
    prob_succeed_within_8_given_failed_3 = (geometric.cdf(8) - geometric.cdf(3)) / geometric.sf(3)
    print("Memoryless Property:")
    print(f"  P(X ≤ 5) = {prob_succeed_within_5:.4f}")
    print(f"  P(X ≤ 8 | X > 3) = {prob_succeed_within_8_given_failed_3:.4f}")
    print(f"  These should be equal (both = P(X ≤ 5)): approximately satisfied")
    print()

    # Visualize geometric distribution
    x_geom = np.arange(1, 21)
    pmf_geom = geometric.pmf(x_geom)
    cdf_geom = geometric.cdf(x_geom)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # PMF
    axes[0].bar(x_geom, pmf_geom, alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Trial of First Success')
    axes[0].set_ylabel('Probability')
    axes[0].set_title(f'Geometric({p_success}) - PMF')
    axes[0].grid(True, alpha=0.3)

    # CDF
    axes[1].step(x_geom, cdf_geom, where='post', linewidth=2)
    axes[1].scatter(x_geom, cdf_geom, color='red', zorder=3)
    axes[1].set_xlabel('k')
    axes[1].set_ylabel('Cumulative Probability')
    axes[1].set_title(f'Geometric({p_success}) - CDF')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/03_geometric.png', dpi=300, bbox_inches='tight')
    print("Saved: 03_geometric.png\n")
    plt.close()

    # =============================================================================
    # SECTION 5: Negative Binomial Distribution
    # =============================================================================
    """
    Models the number of failures before the r-th success.

    PMF: P(X = k) = C(k+r-1, k) * p^r * (1-p)^k

    Parameters:
    - n (or r): number of successes
    - p: probability of success

    Properties:
    - Mean: E[X] = r(1-p)/p (number of failures)
    - Variance: Var(X) = r(1-p)/p²
    - Sum of r independent Geometric(p) ~ NegativeBinomial(r, p)

    Applications:
    - Number of failures before r successes
    - Over-dispersed count data (variance > mean)
    - Modeling heterogeneity in Poisson processes
    """

    print("NEGATIVE BINOMIAL DISTRIBUTION")
    print("-" * 40)

    r = 5  # Number of successes desired
    p_nb = 0.3  # Probability of success
    negbinom = stats.nbinom(r, p_nb)

    print(f"NegativeBinomial({r}, {p_nb}):")
    print(f"  Mean failures before {r} successes: {negbinom.mean():.2f}")
    print(f"  Variance: {negbinom.var():.2f}")
    print()

    print("Probability calculations:")
    print(f"  P(10 failures before {r} successes) = {negbinom.pmf(10):.4f}")
    print(f"  P(≤ 15 failures) = {negbinom.cdf(15):.4f}")
    print()

    # Visualize negative binomial
    x_nb = np.arange(0, 40)
    pmf_nb = negbinom.pmf(x_nb)

    plt.figure(figsize=(10, 6))
    plt.bar(x_nb, pmf_nb, alpha=0.7, edgecolor='black')
    plt.xlabel('Number of Failures (k)')
    plt.ylabel('Probability')
    plt.title(f'Negative Binomial({r}, {p_nb}) - PMF')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/03_negative_binomial.png', dpi=300, bbox_inches='tight')
    print("Saved: 03_negative_binomial.png\n")
    plt.close()

    # =============================================================================
    # SECTION 6: Poisson Distribution
    # =============================================================================
    """
    Models the number of events occurring in a fixed interval of time or space.

    PMF: P(X = k) = (λ^k * e^(-λ)) / k!

    Parameter:
    - λ (mu): average rate (mean number of events)

    Properties:
    - Mean: E[X] = λ
    - Variance: Var(X) = λ (mean = variance!)
    - Sum of independent Poisson(λ₁) and Poisson(λ₂) ~ Poisson(λ₁ + λ₂)

    Applications:
    - Number of customers arriving per hour
    - Number of emails received per day
    - Number of accidents per month
    - Number of mutations in a DNA sequence
    - Rare events with constant average rate
    """

    print("POISSON DISTRIBUTION")
    print("-" * 40)

    lambda_val = 5  # Average number of events
    poisson = stats.poisson(lambda_val)

    print(f"Poisson({lambda_val}):")
    print(f"  Mean: {poisson.mean():.2f}")
    print(f"  Variance: {poisson.var():.2f}")
    print(f"  Std Dev: {poisson.std():.2f}")
    print()

    print("Probability calculations:")
    print(f"  P(X = 5) = {poisson.pmf(5):.4f}")
    print(f"  P(X ≤ 3) = {poisson.cdf(3):.4f}")
    print(f"  P(X ≥ 8) = {poisson.sf(7):.4f}")
    print(f"  P(3 ≤ X ≤ 7) = {poisson.cdf(7) - poisson.cdf(2):.4f}")
    print()

    # Application: Website traffic
    print("Application: Website Traffic")
    print("-" * 40)
    avg_visitors_per_hour = 50
    traffic = stats.poisson(avg_visitors_per_hour)

    print(f"Average visitors per hour: {avg_visitors_per_hour}")
    print(f"  P(< 40 visitors) = {traffic.cdf(39):.4f} (unusually low)")
    print(f"  P(40-60 visitors) = {traffic.cdf(60) - traffic.cdf(39):.4f} (typical)")
    print(f"  P(> 70 visitors) = {traffic.sf(70):.4f} (unusually high)")
    print()

    # Visualize Poisson distributions with different λ
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Single Poisson PMF
    x_pois = np.arange(0, 20)
    axes[0, 0].bar(x_pois, poisson.pmf(x_pois), alpha=0.7, edgecolor='black')
    axes[0, 0].axvline(lambda_val, color='red', linestyle='--', linewidth=2, label=f'λ={lambda_val}')
    axes[0, 0].set_xlabel('k')
    axes[0, 0].set_ylabel('Probability')
    axes[0, 0].set_title(f'Poisson({lambda_val}) - PMF')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Effect of λ
    for lam in [1, 5, 10, 20]:
        pois_temp = stats.poisson(lam)
        x_temp = np.arange(0, 40)
        axes[0, 1].plot(x_temp, pois_temp.pmf(x_temp), marker='o', 
                        label=f'λ={lam}', linewidth=2, alpha=0.7)

    axes[0, 1].set_xlabel('k')
    axes[0, 1].set_ylabel('Probability')
    axes[0, 1].set_title('Effect of λ')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: Poisson approximation to Binomial
    # When n is large and p is small, Binomial(n,p) ≈ Poisson(np)
    n_large = 100
    p_small = 0.05
    binom_approx = stats.binom(n_large, p_small)
    pois_approx = stats.poisson(n_large * p_small)
    x_approx = np.arange(0, 15)

    axes[1, 0].bar(x_approx - 0.2, binom_approx.pmf(x_approx), width=0.4, 
                   alpha=0.7, label='Binomial(100, 0.05)', edgecolor='black')
    axes[1, 0].bar(x_approx + 0.2, pois_approx.pmf(x_approx), width=0.4, 
                   alpha=0.7, label='Poisson(5)', edgecolor='black')
    axes[1, 0].set_xlabel('k')
    axes[1, 0].set_ylabel('Probability')
    axes[1, 0].set_title('Poisson Approximation to Binomial')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Normal approximation to Poisson (large λ)
    # When λ is large, Poisson(λ) ≈ Normal(λ, λ)
    lambda_large = 50
    pois_large = stats.poisson(lambda_large)
    norm_approx = stats.norm(lambda_large, np.sqrt(lambda_large))
    x_large = np.arange(30, 70)

    axes[1, 1].bar(x_large, pois_large.pmf(x_large), alpha=0.7, 
                   label='Poisson(50)', edgecolor='black')
    axes[1, 1].plot(x_large, norm_approx.pdf(x_large), 'r-', linewidth=3, 
                    label='Normal(50, √50)')
    axes[1, 1].set_xlabel('k')
    axes[1, 1].set_ylabel('Probability/Density')
    axes[1, 1].set_title('Normal Approximation to Poisson (large λ)')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/03_poisson.png', dpi=300, bbox_inches='tight')
    print("Saved: 03_poisson.png\n")
    plt.close()

    # =============================================================================
    # SECTION 7: Hypergeometric Distribution
    # =============================================================================
    """
    Models sampling WITHOUT replacement from a finite population.

    PMF: P(X = k) = C(K,k) * C(N-K,n-k) / C(N,n)

    Parameters:
    - M (N): total population size
    - n: number of success states in population (K)
    - N (n): number of draws (sample size)

    Properties:
    - Mean: E[X] = n * K/N
    - Variance: Var(X) = n * (K/N) * (1 - K/N) * (N-n)/(N-1)
    - When N is large, Hypergeometric ≈ Binomial

    Applications:
    - Quality control (sampling without replacement)
    - Card games (drawing cards from a deck)
    - Capture-recapture studies in ecology
    """

    print("HYPERGEOMETRIC DISTRIBUTION")
    print("-" * 40)

    # Example: Drawing cards from a deck
    M = 52  # Total cards
    n = 13  # Hearts in deck
    N = 5   # Cards drawn
    hypergeom = stats.hypergeom(M, n, N)

    print(f"Drawing {N} cards from a deck of {M} cards ({n} hearts):")
    print(f"  Mean hearts drawn: {hypergeom.mean():.2f}")
    print(f"  Variance: {hypergeom.var():.2f}")
    print()

    print("Probability of drawing k hearts:")
    for k in range(N+1):
        prob = hypergeom.pmf(k)
        print(f"  P(X = {k}) = {prob:.4f}")
    print()

    # Comparison with Binomial (with replacement)
    p_hearts = n / M
    binom_comparison = stats.binom(N, p_hearts)

    print("Comparison: Hypergeometric vs. Binomial")
    print("(Hypergeometric: without replacement, Binomial: with replacement)")
    print(f"{'k':<5} {'Hypergeometric':<20} {'Binomial':<20} {'Difference':<15}")
    print("-" * 60)
    for k in range(N+1):
        hyper_prob = hypergeom.pmf(k)
        binom_prob = binom_comparison.pmf(k)
        diff = abs(hyper_prob - binom_prob)
        print(f"{k:<5} {hyper_prob:<20.6f} {binom_prob:<20.6f} {diff:<15.6f}")
    print()

    # Visualize hypergeometric vs binomial
    x_hyper = np.arange(0, N+1)
    pmf_hyper = hypergeom.pmf(x_hyper)
    pmf_binom = binom_comparison.pmf(x_hyper)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Hypergeometric PMF
    axes[0].bar(x_hyper, pmf_hyper, alpha=0.7, edgecolor='black')
    axes[0].set_xlabel('Number of Hearts')
    axes[0].set_ylabel('Probability')
    axes[0].set_title(f'Hypergeometric({M}, {n}, {N}) - PMF')
    axes[0].grid(True, alpha=0.3)

    # Plot 2: Comparison
    x_pos = np.arange(len(x_hyper))
    width = 0.35
    axes[1].bar(x_pos - width/2, pmf_hyper, width, alpha=0.7, 
                label='Hypergeometric', edgecolor='black')
    axes[1].bar(x_pos + width/2, pmf_binom, width, alpha=0.7, 
                label='Binomial', edgecolor='black')
    axes[1].set_xlabel('k')
    axes[1].set_ylabel('Probability')
    axes[1].set_title('Hypergeometric vs. Binomial')
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(x_hyper)
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/03_hypergeometric.png', dpi=300, bbox_inches='tight')
    print("Saved: 03_hypergeometric.png\n")
    plt.close()

    # =============================================================================
    # SECTION 8: Summary and Comparison
    # =============================================================================

    print("="*80)
    print("SUMMARY: Discrete Distribution Characteristics")
    print("="*80)

    comparison_data = [
        ("Bernoulli", "Single trial, two outcomes", "p", "p", "p(1-p)"),
        ("Binomial", "# successes in n trials", "n, p", "np", "np(1-p)"),
        ("Geometric", "# trials to 1st success", "p", "1/p", "(1-p)/p²"),
        ("Negative Binomial", "# failures before r successes", "r, p", "r(1-p)/p", "r(1-p)/p²"),
        ("Poisson", "# events in fixed interval", "λ", "λ", "λ"),
        ("Hypergeometric", "# successes without replacement", "M, n, N", "nK/M", "complex"),
    ]

    print(f"\n{'Distribution':<20} {'Description':<40} {'Parameters':<15} {'Mean':<15} {'Variance':<15}")
    print("-" * 105)
    for name, desc, params, mean, var in comparison_data:
        print(f"{name:<20} {desc:<40} {params:<15} {mean:<15} {var:<15}")

    print("\n" + "="*80)
    print("Relationships Between Distributions:")
    print("="*80)
    print("1. Sum of n Bernoulli(p) = Binomial(n, p)")
    print("2. Sum of r Geometric(p) = Negative Binomial(r, p)")
    print("3. Binomial(n, p) ≈ Poisson(np) when n large, p small")
    print("4. Poisson(λ) ≈ Normal(λ, √λ) when λ large")
    print("5. Hypergeometric ≈ Binomial when population >> sample")
    print()

    print("="*80)
    print("Tutorial 03 Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("1. Discrete distributions use PMF (not PDF) to give exact probabilities")
    print("2. Bernoulli: single trial with success/failure")
    print("3. Binomial: number of successes in fixed number of trials")
    print("4. Geometric: number of trials until first success (memoryless)")
    print("5. Negative Binomial: number of failures before r successes")
    print("6. Poisson: number of events in fixed time/space interval (mean = variance)")
    print("7. Hypergeometric: sampling without replacement from finite population")
    print("8. Many distributions are related through limiting cases and special relationships")
```

---

## Exercises

**Exercise 1.**
For a $\text{Binomial}(n=100, p=0.03)$, compute $P(X = 3)$ using both the binomial PMF and the Poisson approximation with $\lambda = np = 3$. Compare the two values.

??? success "Solution to Exercise 1"

        from scipy import stats

        p_binom = stats.binom.pmf(3, n=100, p=0.03)
        p_poisson = stats.poisson.pmf(3, mu=3)
        print(f"Binomial:  P(X=3) = {p_binom:.6f}")
        print(f"Poisson:   P(X=3) = {p_poisson:.6f}")
        print(f"Difference: {abs(p_binom - p_poisson):.6f}")

---

**Exercise 2.**
A call center receives an average of 8 calls per hour (Poisson). Compute the probability of receiving more than 12 calls in one hour and the probability of receiving exactly 0 calls using the survival function and PMF respectively.

??? success "Solution to Exercise 2"

        from scipy import stats

        rv = stats.poisson(mu=8)
        p_gt_12 = rv.sf(12)
        p_eq_0 = rv.pmf(0)
        print(f"P(X > 12) = {p_gt_12:.4f}")
        print(f"P(X = 0)  = {p_eq_0:.6f}")

---

**Exercise 3.**
Generate 10,000 binomial samples with $n = 20$ and $p = 0.4$. Compute the sample mean and variance and compare them with the theoretical values $np$ and $np(1-p)$.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        samples = stats.binom.rvs(n=20, p=0.4, size=10000, random_state=42)
        print(f"Sample mean: {np.mean(samples):.4f} (expected {20*0.4})")
        print(f"Sample var:  {np.var(samples, ddof=1):.4f} (expected {20*0.4*0.6})")
