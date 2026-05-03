# Normal Distribution

The normal (Gaussian) distribution is the most fundamental continuous probability distribution in statistics and financial mathematics. It arises naturally from the Central Limit Theorem and underpins much of quantitative finance, from asset return modeling to option pricing.

!!! tip "Mental Model"
    The normal distribution is the "default" bell curve that emerges whenever many small, independent effects add up (the Central Limit Theorem). Two parameters tell the whole story: $\mu$ shifts the center and $\sigma$ controls the width. Roughly 68% of values fall within one $\sigma$ of the mean, 95% within two, and 99.7% within three.

---

## Mathematical Definition

The probability density function (PDF) of a normal distribution with mean $\mu$ and standard deviation $\sigma$ is:

$$f(x) = \frac{1}{\sigma\sqrt{2\pi}} \exp\left(-\frac{(x - \mu)^2}{2\sigma^2}\right)$$

When $\mu = 0$ and $\sigma = 1$, this is the **standard normal distribution**.

## Manual PDF Computation

Before using `scipy.stats`, it is instructive to compute the normal PDF directly from the formula. This builds intuition about how the bell curve arises from the exponential of a squared deviation:

```python
import numpy as np
import matplotlib.pyplot as plt

mu = 3.0
x = np.linspace(mu - 3, mu + 3, num=100)
y = np.exp(-(x - mu)**2 / 2) / np.sqrt(2 * np.pi)

plt.plot(x, y)
plt.title(f'Normal PDF (μ={mu}, σ=1) — Manual Computation')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()
```

Here the formula is implemented element-wise using NumPy vectorization. The denominator $\sigma\sqrt{2\pi}$ normalizes the area under the curve to 1, and the exponent $-(x-\mu)^2 / (2\sigma^2)$ controls the bell shape centered at $\mu$.

## Using scipy.stats.norm

The `scipy.stats.norm` distribution object provides a consistent interface for all distribution computations:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mu = 3.0
a = stats.norm(loc=mu)  # Frozen distribution with mean=3, std=1

# Evaluate PDF and CDF over a range
x = np.linspace(mu - 3, mu + 3, 100)
y_pdf = a.pdf(x)
y_cdf = a.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend(loc='lower left')
plt.title(f'Normal Distribution (μ={mu}, σ=1)')
plt.xlabel('x')
plt.ylabel('Density / Probability')
plt.show()
```

The PDF curve shows the relative likelihood of each value (its height at the mean is the maximum), while the CDF is the S-shaped curve that gives $P(X \le x)$, rising from 0 to 1.

## Key Properties

The normal distribution has several important properties:

- **Symmetry**: The distribution is symmetric about the mean, so $\text{mean} = \text{median} = \text{mode} = \mu$.
- **68-95-99.7 Rule**: Approximately 68% of values fall within $\mu \pm \sigma$, 95% within $\mu \pm 2\sigma$, and 99.7% within $\mu \pm 3\sigma$.
- **Additivity**: If $X \sim N(\mu_1, \sigma_1^2)$ and $Y \sim N(\mu_2, \sigma_2^2)$ are independent, then $X + Y \sim N(\mu_1 + \mu_2, \sigma_1^2 + \sigma_2^2)$.
- **Central Limit Theorem**: The sum (or mean) of a large number of independent random variables tends toward a normal distribution, regardless of the original distribution.

## Parameters in scipy.stats

| Parameter | Symbol | `scipy.stats` keyword | Default |
|-----------|--------|----------------------|---------|
| Mean      | $\mu$  | `loc`                | 0       |
| Std Dev   | $\sigma$| `scale`             | 1       |

## Financial Applications

The normal distribution is central to quantitative finance. Log-returns of assets are often modeled as normally distributed, which leads to the lognormal model for prices. The Black-Scholes option pricing model assumes that log-returns follow a normal distribution. Value at Risk (VaR) calculations frequently use the normal quantile function (`ppf`). Portfolio theory relies on the normal distribution for computing efficient frontiers under mean-variance optimization.

## Summary

The normal distribution serves as the foundation for much of statistics and financial mathematics. Understanding both its manual derivation and its `scipy.stats` interface is essential for any quantitative analysis workflow.

---

## Runnable Example: `continuous_distributions.py`

```python
"""
Tutorial 02: Continuous Distributions in Depth
===============================================
Level: Beginner-Intermediate
Topics: Normal, lognormal, exponential, gamma, beta, chi-square, F, Weibull,
        Cauchy, and other continuous distributions with practical applications

This module explores various continuous probability distributions available
in scipy.stats and their real-world applications.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings

if __name__ == "__main__":
    warnings.filterwarnings('ignore')

    # =============================================================================
    # SECTION 1: Normal (Gaussian) Distribution - Deep Dive
    # =============================================================================
    """
    The normal distribution is the most important distribution in statistics.

    PDF: f(x) = (1/(σ√(2π))) * exp(-(x-μ)²/(2σ²))

    Parameters:
    - μ (loc): mean, median, and mode
    - σ (scale): standard deviation

    Properties:
    - Symmetric around the mean
    - 68-95-99.7 rule (empirical rule)
    - Central Limit Theorem: sums of independent random variables → normal
    """

    # The 68-95-99.7 Rule (Empirical Rule)
    # -------------------------------------
    normal = stats.norm(loc=100, scale=15)  # IQ scores: mean=100, std=15

    print("="*80)
    print("NORMAL DISTRIBUTION - The 68-95-99.7 Rule")
    print("="*80)

    # Within 1 standard deviation (μ ± σ)
    prob_1std = normal.cdf(115) - normal.cdf(85)  # P(85 < X < 115)
    print(f"P(μ-σ < X < μ+σ) = P(85 < X < 115) = {prob_1std:.4f} ≈ 68%")

    # Within 2 standard deviations (μ ± 2σ)
    prob_2std = normal.cdf(130) - normal.cdf(70)  # P(70 < X < 130)
    print(f"P(μ-2σ < X < μ+2σ) = P(70 < X < 130) = {prob_2std:.4f} ≈ 95%")

    # Within 3 standard deviations (μ ± 3σ)
    prob_3std = normal.cdf(145) - normal.cdf(55)  # P(55 < X < 145)
    print(f"P(μ-3σ < X < μ+3σ) = P(55 < X < 145) = {prob_3std:.4f} ≈ 99.7%")
    print()

    # Standardization (Z-scores)
    # ---------------------------
    # Convert any normal distribution to standard normal: Z = (X - μ) / σ
    raw_score = 115  # IQ score
    z_score = (raw_score - normal.mean()) / normal.std()
    print(f"IQ score {raw_score} corresponds to z-score: {z_score:.2f}")
    print(f"This is at the {normal.cdf(raw_score)*100:.1f}th percentile")
    print()

    # =============================================================================
    # SECTION 2: Lognormal Distribution
    # =============================================================================
    """
    If X ~ Lognormal, then ln(X) ~ Normal
    Used for modeling variables that are products of many small factors.

    Applications:
    - Income distributions
    - Stock prices
    - Particle sizes
    - File sizes on the internet

    Parameters:
    - s: shape parameter (σ of the underlying normal)
    - scale: exp(μ) where μ is the mean of the underlying normal
    """

    # Creating lognormal distributions
    lognormal = stats.lognorm(s=0.5, scale=np.exp(2))  # σ=0.5, μ=2

    print("="*80)
    print("LOGNORMAL DISTRIBUTION")
    print("="*80)
    print(f"Mean: {lognormal.mean():.4f}")
    print(f"Median: {lognormal.median():.4f}")  # Median = exp(μ)
    print(f"Mode: {np.exp(2 - 0.5**2):.4f}")  # Mode = exp(μ - σ²)
    print(f"Variance: {lognormal.var():.4f}")
    print()

    # Note: Lognormal is right-skewed (mean > median > mode)
    print(f"Skewness: mean ({lognormal.mean():.2f}) > "
          f"median ({lognormal.median():.2f}) > "
          f"mode ({np.exp(2 - 0.5**2):.2f})")
    print()

    # Application: Stock price model
    # -------------------------------
    # If daily returns are normal, prices follow lognormal
    initial_price = 100
    daily_return_mean = 0.001  # 0.1% daily return
    daily_return_std = 0.02   # 2% daily volatility
    days = 252  # Trading days in a year

    # Price after 1 year follows lognormal
    mu = daily_return_mean * days
    sigma = daily_return_std * np.sqrt(days)
    final_price_dist = stats.lognorm(s=sigma, scale=initial_price * np.exp(mu))

    print(f"Stock Price Prediction (1 year):")
    print(f"  Expected price: ${final_price_dist.mean():.2f}")
    print(f"  Median price: ${final_price_dist.median():.2f}")
    print(f"  95% confidence interval: ${final_price_dist.ppf(0.025):.2f} - ${final_price_dist.ppf(0.975):.2f}")
    print()

    # =============================================================================
    # SECTION 3: Exponential Distribution
    # =============================================================================
    """
    Models the time between events in a Poisson process.

    PDF: f(x) = λ * exp(-λx) for x ≥ 0

    Parameter:
    - scale = 1/λ (mean time between events)

    Properties:
    - Memoryless property: P(X > s+t | X > s) = P(X > t)
    - Mean = Variance = 1/λ

    Applications:
    - Time between arrivals
    - Lifetime of electronic components
    - Time to decay of radioactive particles
    """

    # Example: Customer service waiting times
    mean_wait_time = 5  # minutes
    exponential = stats.expon(scale=mean_wait_time)

    print("="*80)
    print("EXPONENTIAL DISTRIBUTION - Customer Wait Times")
    print("="*80)
    print(f"Mean wait time: {exponential.mean():.2f} minutes")
    print(f"Median wait time: {exponential.median():.2f} minutes")
    print()

    # Probability questions
    prob_less_than_3 = exponential.cdf(3)
    print(f"P(wait < 3 min) = {prob_less_than_3:.4f} ({prob_less_than_3*100:.1f}%)")

    prob_more_than_10 = exponential.sf(10)
    print(f"P(wait > 10 min) = {prob_more_than_10:.4f} ({prob_more_than_10*100:.1f}%)")

    prob_between_5_10 = exponential.cdf(10) - exponential.cdf(5)
    print(f"P(5 < wait < 10 min) = {prob_between_5_10:.4f} ({prob_between_5_10*100:.1f}%)")
    print()

    # Memoryless property demonstration
    # If you've already waited 5 minutes, the probability of waiting
    # another 5 minutes is the same as waiting 5 minutes from the start
    prob_wait_5 = exponential.sf(5)
    prob_wait_10_given_5 = exponential.sf(10) / exponential.sf(5)
    print("Memoryless Property:")
    print(f"  P(X > 5) = {prob_wait_5:.4f}")
    print(f"  P(X > 10 | X > 5) = P(X > 10) / P(X > 5) = {prob_wait_10_given_5:.4f}")
    print(f"  P(X > 5) = P(X > 10 | X > 5) ✓ (Memoryless)")
    print()

    # =============================================================================
    # SECTION 4: Gamma Distribution
    # =============================================================================
    """
    Generalization of the exponential distribution.
    Sum of k independent exponential random variables ~ Gamma(k, λ)

    PDF: f(x) = (λ^k * x^(k-1) * exp(-λx)) / Γ(k)

    Parameters:
    - a (shape): k
    - scale: 1/λ (or loc: θ)

    Applications:
    - Waiting time for k events in a Poisson process
    - Bayesian statistics (conjugate prior for Poisson)
    - Insurance claim amounts
    """

    # Example: Time until 5 customers arrive (if arrivals ~ Poisson)
    k = 5  # Shape parameter (number of events)
    theta = 3  # Scale parameter (mean time between events)
    gamma_dist = stats.gamma(a=k, scale=theta)

    print("="*80)
    print("GAMMA DISTRIBUTION - Time for Multiple Events")
    print("="*80)
    print(f"Waiting time for {k} customers (mean wait per customer = {theta} min):")
    print(f"  Mean total wait: {gamma_dist.mean():.2f} minutes")
    print(f"  Std deviation: {gamma_dist.std():.2f} minutes")
    print(f"  Median: {gamma_dist.median():.2f} minutes")
    print()

    # Special cases
    print("Special Cases of Gamma Distribution:")
    print(f"  Gamma(1, θ) = Exponential(scale=θ)")
    print(f"  Gamma(k/2, 2) = Chi-square(k)")
    print()

    # =============================================================================
    # SECTION 5: Beta Distribution
    # =============================================================================
    """
    Continuous distribution on the interval [0, 1].
    Very flexible shape based on two parameters.

    PDF: f(x) = (x^(α-1) * (1-x)^(β-1)) / B(α, β)

    Parameters:
    - a (α): first shape parameter
    - b (β): second shape parameter

    Applications:
    - Modeling probabilities and proportions
    - Bayesian statistics (conjugate prior for binomial)
    - Project completion time (PERT distribution)
    - Order statistics
    """

    print("="*80)
    print("BETA DISTRIBUTION - Flexible Shapes")
    print("="*80)

    # Different shapes of beta distribution
    beta_params = [
        (0.5, 0.5, "U-shaped"),
        (1, 1, "Uniform"),
        (2, 2, "Symmetric, peaked"),
        (2, 5, "Right-skewed"),
        (5, 2, "Left-skewed"),
        (8, 4, "Narrow, left-skewed")
    ]

    x_beta = np.linspace(0, 1, 1000)
    plt.figure(figsize=(12, 8))

    for i, (a, b, desc) in enumerate(beta_params, 1):
        beta = stats.beta(a, b)
        plt.subplot(2, 3, i)
        plt.plot(x_beta, beta.pdf(x_beta), linewidth=2)
        plt.fill_between(x_beta, beta.pdf(x_beta), alpha=0.3)
        plt.title(f'Beta({a}, {b}) - {desc}')
        plt.xlabel('x')
        plt.ylabel('Density')
        plt.grid(True, alpha=0.3)
        plt.xlim(0, 1)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/02_beta_shapes.png', dpi=300, bbox_inches='tight')
    print("Saved: 02_beta_shapes.png")
    plt.close()

    # Application: Estimating success probability
    # ----------------------------------------------
    # After observing 7 successes in 10 trials, what's the probability distribution?
    # Using Bayesian inference with uniform prior: Beta(1,1)
    successes = 7
    failures = 3
    posterior = stats.beta(successes + 1, failures + 1)

    print(f"\nBayesian Estimation of Success Probability:")
    print(f"  Observed: {successes} successes, {failures} failures")
    print(f"  Mean estimate: {posterior.mean():.4f}")
    print(f"  Median estimate: {posterior.median():.4f}")
    print(f"  95% credible interval: [{posterior.ppf(0.025):.4f}, {posterior.ppf(0.975):.4f}]")
    print()

    # =============================================================================
    # SECTION 6: Chi-Square Distribution
    # =============================================================================
    """
    Sum of k independent squared standard normal random variables.
    If Z₁, ..., Zₖ ~ N(0,1), then Z₁² + ... + Zₖ² ~ χ²(k)

    Parameter:
    - df: degrees of freedom (k)

    Applications:
    - Chi-square test for independence
    - Goodness-of-fit tests
    - Confidence intervals for variance
    - Distribution of sample variance
    """

    # Chi-square with different degrees of freedom
    df_values = [1, 2, 3, 5, 10, 20]
    x_chi = np.linspace(0, 40, 1000)

    plt.figure(figsize=(14, 6))

    # Plot 1: PDF for different df
    plt.subplot(1, 2, 1)
    for df in df_values:
        chi2 = stats.chi2(df)
        plt.plot(x_chi, chi2.pdf(x_chi), label=f'df={df}', linewidth=2)

    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Chi-Square Distribution PDFs')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 30)

    # Plot 2: Mean and variance vs. df
    plt.subplot(1, 2, 2)
    df_range = np.arange(1, 31)
    means = [stats.chi2(df).mean() for df in df_range]
    variances = [stats.chi2(df).var() for df in df_range]

    plt.plot(df_range, means, 'b-', linewidth=2, label='Mean = df', marker='o')
    plt.plot(df_range, variances, 'r-', linewidth=2, label='Variance = 2*df', marker='s')
    plt.xlabel('Degrees of Freedom')
    plt.ylabel('Value')
    plt.title('Chi-Square: Mean and Variance vs. df')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/02_chi_square.png', dpi=300, bbox_inches='tight')
    print("Saved: 02_chi_square.png")
    plt.close()

    print("="*80)
    print("CHI-SQUARE DISTRIBUTION")
    print("="*80)
    chi2_10 = stats.chi2(df=10)
    print(f"Chi-square(df=10):")
    print(f"  Mean: {chi2_10.mean():.2f} (= df)")
    print(f"  Variance: {chi2_10.var():.2f} (= 2*df)")
    print(f"  Std Dev: {chi2_10.std():.2f}")
    print()

    # Critical values for hypothesis testing
    alpha = 0.05
    critical_value = chi2_10.ppf(1 - alpha)
    print(f"Critical value at α={alpha}: {critical_value:.4f}")
    print(f"Used in hypothesis testing: reject H₀ if test statistic > {critical_value:.4f}")
    print()

    # =============================================================================
    # SECTION 7: F-Distribution
    # =============================================================================
    """
    Ratio of two independent chi-square random variables (each divided by its df).
    If X ~ χ²(d₁) and Y ~ χ²(d₂), then (X/d₁)/(Y/d₂) ~ F(d₁, d₂)

    Parameters:
    - dfn: numerator degrees of freedom
    - dfd: denominator degrees of freedom

    Applications:
    - ANOVA (Analysis of Variance)
    - Testing equality of variances
    - Regression analysis (F-test for overall significance)
    """

    # F-distribution with different df combinations
    f_dist = stats.f(dfn=5, dfd=20)

    print("="*80)
    print("F-DISTRIBUTION")
    print("="*80)
    print(f"F(5, 20) Distribution:")
    print(f"  Mean: {f_dist.mean():.4f}")
    print(f"  Variance: {f_dist.var():.4f}")
    print()

    # Critical values for ANOVA
    alpha_levels = [0.10, 0.05, 0.01]
    print("Critical values for ANOVA (α levels):")
    for alpha in alpha_levels:
        critical_f = f_dist.ppf(1 - alpha)
        print(f"  α = {alpha:.2f}: F_critical = {critical_f:.4f}")
    print()

    # Visualize F-distributions
    x_f = np.linspace(0, 5, 1000)
    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    f_configs = [(2, 10), (5, 20), (10, 10), (20, 20)]
    for dfn, dfd in f_configs:
        f_temp = stats.f(dfn, dfd)
        plt.plot(x_f, f_temp.pdf(x_f), label=f'F({dfn}, {dfd})', linewidth=2)

    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('F-Distribution PDFs')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Critical region
    plt.subplot(1, 2, 2)
    f_test = stats.f(dfn=5, dfd=20)
    x_range = np.linspace(0, 5, 1000)
    pdf_values = f_test.pdf(x_range)
    critical = f_test.ppf(0.95)

    plt.plot(x_range, pdf_values, 'b-', linewidth=2, label='F(5, 20)')
    plt.fill_between(x_range[x_range >= critical], pdf_values[x_range >= critical],
                     alpha=0.3, color='red', label=f'Critical region (α=0.05)')
    plt.axvline(critical, color='red', linestyle='--', linewidth=2)
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('F-Distribution: Critical Region for α=0.05')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/02_f_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: 02_f_distribution.png")
    plt.close()

    # =============================================================================
    # SECTION 8: Student's t-Distribution
    # =============================================================================
    """
    Similar to normal distribution but with heavier tails.
    Used when estimating the mean with small sample sizes.

    If X̄ ~ N(μ, σ²/n) and S² is the sample variance,
    then (X̄ - μ)/(S/√n) ~ t(n-1)

    Parameter:
    - df: degrees of freedom (typically n-1 for sample size n)

    As df → ∞, t-distribution → Normal distribution
    """

    print("="*80)
    print("STUDENT'S t-DISTRIBUTION")
    print("="*80)

    # Compare t-distributions with different df to normal
    x_t = np.linspace(-4, 4, 1000)
    normal = stats.norm()

    plt.figure(figsize=(14, 6))

    # Plot 1: PDFs
    plt.subplot(1, 2, 1)
    plt.plot(x_t, normal.pdf(x_t), 'k-', linewidth=2, label='Normal')
    for df in [1, 3, 10, 30]:
        t_temp = stats.t(df)
        plt.plot(x_t, t_temp.pdf(x_t), label=f't(df={df})', linewidth=2)

    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('t-Distribution vs. Normal: PDFs')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Tail probabilities
    plt.subplot(1, 2, 2)
    df_range = np.arange(1, 51)
    tail_probs_normal = [2 * (1 - normal.cdf(2)) for _ in df_range]
    tail_probs_t = [2 * (1 - stats.t(df).cdf(2)) for df in df_range]

    plt.plot(df_range, tail_probs_normal, 'k--', linewidth=2, label='Normal')
    plt.plot(df_range, tail_probs_t, 'r-', linewidth=2, label='t-distribution', marker='o')
    plt.xlabel('Degrees of Freedom')
    plt.ylabel('P(|X| > 2)')
    plt.title('Tail Probability: t converges to Normal as df increases')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/02_t_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: 02_t_distribution.png")
    plt.close()

    # Critical values for confidence intervals
    sample_sizes = [5, 10, 20, 50, 100]
    confidence = 0.95
    alpha = 1 - confidence

    print(f"\nCritical values for {confidence*100:.0f}% confidence intervals:")
    print(f"{'Sample Size':<15} {'df':<10} {'t-critical':<15} {'z-critical':<15}")
    print("-" * 55)
    for n in sample_sizes:
        df = n - 1
        t_crit = stats.t(df).ppf(1 - alpha/2)
        z_crit = normal.ppf(1 - alpha/2)
        print(f"{n:<15} {df:<10} {t_crit:<15.4f} {z_crit:<15.4f}")

    print(f"\nAs sample size increases, t-critical → z-critical")
    print()

    # =============================================================================
    # SECTION 9: Weibull Distribution
    # =============================================================================
    """
    Flexible distribution used in reliability analysis and survival analysis.

    PDF: f(x) = (k/λ) * (x/λ)^(k-1) * exp(-(x/λ)^k)

    Parameters:
    - c: shape parameter (k)
    - scale: scale parameter (λ)

    Special cases:
    - k = 1: Exponential distribution
    - k = 2: Rayleigh distribution
    - k = 3.4: Approximates normal

    Applications:
    - Lifetime and failure time analysis
    - Wind speed modeling
    - Time to failure of electronic components
    """

    print("="*80)
    print("WEIBULL DISTRIBUTION - Reliability Analysis")
    print("="*80)

    # Different shape parameters
    x_weibull = np.linspace(0, 3, 1000)
    plt.figure(figsize=(14, 6))

    # Plot 1: Effect of shape parameter
    plt.subplot(1, 2, 1)
    for k in [0.5, 1, 1.5, 2, 3]:
        weibull = stats.weibull_min(c=k, scale=1)
        plt.plot(x_weibull, weibull.pdf(x_weibull), label=f'k={k}', linewidth=2)

    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Weibull: Effect of Shape Parameter (λ=1)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 2: Hazard function
    plt.subplot(1, 2, 2)
    for k in [0.5, 1, 1.5, 2, 3]:
        weibull = stats.weibull_min(c=k, scale=1)
        # Hazard function: h(x) = f(x) / (1 - F(x))
        hazard = weibull.pdf(x_weibull) / weibull.sf(x_weibull)
        plt.plot(x_weibull, hazard, label=f'k={k}', linewidth=2)

    plt.xlabel('x')
    plt.ylabel('Hazard Rate')
    plt.title('Weibull: Hazard Function')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/02_weibull.png', dpi=300, bbox_inches='tight')
    print("Saved: 02_weibull.png")
    plt.close()

    # Interpretation of shape parameter
    print("Shape parameter interpretation:")
    print("  k < 1: Decreasing failure rate (infant mortality)")
    print("  k = 1: Constant failure rate (random failures) - Exponential")
    print("  k > 1: Increasing failure rate (wear-out failures)")
    print()

    # Application: Component lifetime
    component_life = stats.weibull_min(c=2.5, scale=1000)  # hours
    print("Component Lifetime Analysis:")
    print(f"  Mean lifetime: {component_life.mean():.1f} hours")
    print(f"  Median lifetime: {component_life.median():.1f} hours")
    print(f"  Probability of failure before 500 hours: {component_life.cdf(500):.4f}")
    print(f"  Reliability at 1000 hours: {component_life.sf(1000):.4f}")
    print()

    # =============================================================================
    # SECTION 10: Cauchy Distribution
    # =============================================================================
    """
    Heavy-tailed distribution with no defined mean or variance!

    PDF: f(x) = 1 / (π γ (1 + ((x-x₀)/γ)²))

    Parameters:
    - loc: location parameter (x₀)
    - scale: scale parameter (γ)

    Properties:
    - Symmetric around loc
    - Mean and variance are undefined
    - Sample mean does NOT converge to population mean
    - Ratio of two independent standard normals ~ Cauchy
    """

    print("="*80)
    print("CAUCHY DISTRIBUTION - No Mean or Variance!")
    print("="*80)

    cauchy = stats.cauchy(loc=0, scale=1)

    # The mean() and var() methods exist but don't represent true moments
    print("Note: Cauchy distribution has undefined mean and variance")
    print("The .mean() and .var() methods return values, but these are NOT")
    print("the true population parameters (which don't exist).")
    print()

    # Demonstrate with simulation
    np.random.seed(42)
    sample_sizes = [10, 100, 1000, 10000]
    print("Sample means for different sample sizes:")
    for n in sample_sizes:
        sample = cauchy.rvs(size=n)
        print(f"  n={n:5d}: sample mean = {np.mean(sample):8.2f} (unstable!)")

    print("\nThe sample mean does NOT converge as n increases!")
    print()

    # Visualize Cauchy vs. Normal
    x_cauchy = np.linspace(-10, 10, 1000)
    normal = stats.norm()

    plt.figure(figsize=(14, 6))

    # Plot 1: Linear scale
    plt.subplot(1, 2, 1)
    plt.plot(x_cauchy, normal.pdf(x_cauchy), 'b-', linewidth=2, label='Normal(0,1)')
    plt.plot(x_cauchy, cauchy.pdf(x_cauchy), 'r-', linewidth=2, label='Cauchy(0,1)')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.title('Cauchy vs. Normal: Linear Scale')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 0.5)

    # Plot 2: Log scale shows heavier tails
    plt.subplot(1, 2, 2)
    plt.semilogy(x_cauchy, normal.pdf(x_cauchy), 'b-', linewidth=2, label='Normal(0,1)')
    plt.semilogy(x_cauchy, cauchy.pdf(x_cauchy), 'r-', linewidth=2, label='Cauchy(0,1)')
    plt.xlabel('x')
    plt.ylabel('Probability Density (log scale)')
    plt.title('Cauchy vs. Normal: Log Scale (Heavy Tails)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('/home/claude/scipy_stats_course/02_cauchy.png', dpi=300, bbox_inches='tight')
    print("Saved: 02_cauchy.png")
    plt.close()

    # =============================================================================
    # SECTION 11: Comparing All Distributions
    # =============================================================================

    print("="*80)
    print("SUMMARY: Continuous Distribution Characteristics")
    print("="*80)

    distributions = [
        ("Normal", stats.norm(0, 1), "Symmetric, light tails"),
        ("Lognormal", stats.lognorm(s=0.5), "Right-skewed, positive values"),
        ("Exponential", stats.expon(scale=1), "Right-skewed, memoryless"),
        ("Gamma", stats.gamma(a=2, scale=1), "Right-skewed, sum of exponentials"),
        ("Beta", stats.beta(2, 5), "Bounded [0,1], flexible shape"),
        ("Chi-square", stats.chi2(df=10), "Right-skewed, sum of squared normals"),
        ("F", stats.f(dfn=5, dfd=20), "Right-skewed, ratio of chi-squares"),
        ("t", stats.t(df=5), "Symmetric, heavy tails"),
        ("Weibull", stats.weibull_min(c=2, scale=1), "Flexible, reliability analysis"),
        ("Cauchy", stats.cauchy(0, 1), "Symmetric, very heavy tails"),
    ]

    print(f"\n{'Distribution':<15} {'Support':<20} {'Characteristics':<40}")
    print("-" * 75)

    for name, dist, chars in distributions:
        # Determine support
        lower = dist.ppf(0.001)
        upper = dist.ppf(0.999)
        if lower < 0 and upper > 10:
            support = "(-∞, ∞)"
        elif lower < 0.01:
            support = "[0, ∞)"
        else:
            support = f"[{lower:.1f}, {upper:.1f}]"

        print(f"{name:<15} {support:<20} {chars:<40}")

    print("\n" + "="*80)
    print("Tutorial 02 Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("1. Different distributions model different real-world phenomena")
    print("2. Normal: symmetric, Central Limit Theorem, 68-95-99.7 rule")
    print("3. Lognormal: right-skewed, for positive multiplicative processes")
    print("4. Exponential: memoryless, time between events")
    print("5. Gamma: sum of exponentials, waiting times")
    print("6. Beta: bounded [0,1], modeling probabilities")
    print("7. Chi-square, F, t: derived distributions used in statistical tests")
    print("8. Weibull: flexible, reliability and survival analysis")
    print("9. Cauchy: heavy tails, no defined mean or variance")
    print("10. Choose distribution based on data characteristics and domain knowledge")
```

---

## Exercises

**Exercise 1.**
Using `scipy.stats.norm`, compute the probability that a normally distributed variable with $\mu = 100$ and $\sigma = 15$ falls between 85 and 115 (i.e., within one standard deviation of the mean). Verify the result is approximately 0.6827.

??? success "Solution to Exercise 1"

        from scipy import stats

        rv = stats.norm(loc=100, scale=15)
        prob = rv.cdf(115) - rv.cdf(85)
        print(f"P(85 <= X <= 115) = {prob:.4f}")

---

**Exercise 2.**
Find the value $x$ such that $P(X \le x) = 0.90$ for a normal distribution with $\mu = 50$ and $\sigma = 10$. Then verify by computing `.cdf(x)` and confirming it returns 0.90.

??? success "Solution to Exercise 2"

        from scipy import stats

        rv = stats.norm(loc=50, scale=10)
        x = rv.ppf(0.90)
        print(f"x = {x:.4f}")
        print(f"Verification: CDF(x) = {rv.cdf(x):.4f}")

---

**Exercise 3.**
The 68-95-99.7 rule states that approximately 68%, 95%, and 99.7% of data fall within 1, 2, and 3 standard deviations of the mean. Verify this numerically using `.cdf()` for the standard normal distribution.

??? success "Solution to Exercise 3"

        from scipy import stats

        rv = stats.norm()
        for k in [1, 2, 3]:
            prob = rv.cdf(k) - rv.cdf(-k)
            print(f"P(-{k} < Z < {k}) = {prob:.4f}")
