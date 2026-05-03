# Uniform Distribution

The uniform distribution is the simplest continuous probability distribution, assigning equal probability density to every point in an interval $[a, b]$. Despite its simplicity, it plays a foundational role in probability theory and computational statistics. The probability integral transform states that applying the CDF of any continuous distribution to a random variable from that distribution yields a uniform random variable, making the uniform distribution the starting point for all random variate generation methods.

!!! tip "Mental Model"
    The uniform distribution is "maximum ignorance" on an interval -- every value is equally likely. Its deeper importance is the probability integral transform: feed any continuous random variable through its own CDF and the result is $U(0,1)$. This transform is why computers can generate samples from any distribution starting from uniform random numbers.

---

## Mathematical Definition

A random variable $X$ follows a continuous uniform distribution on $[a, b]$, written $X \sim U(a, b)$, if its probability density function is:

$$
f(x) = \frac{1}{b - a}, \quad a \le x \le b
$$

The cumulative distribution function is:

$$
F(x) = \frac{x - a}{b - a}, \quad a \le x \le b
$$

with $F(x) = 0$ for $x < a$ and $F(x) = 1$ for $x > b$.

## Parametrization in scipy.stats

An important detail: `scipy.stats.uniform` uses `loc` and `scale` rather than $a$ and $b$ directly. The support is $[\text{loc},\; \text{loc} + \text{scale}]$, so to represent $U(a, b)$ you pass `loc=a` and `scale=b-a`:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

a, b = 2.0, 7.0
dist = stats.uniform(loc=a, scale=b - a)

print(f"Mean: {dist.mean():.4f}")        # (a+b)/2 = 4.5
print(f"Variance: {dist.var():.4f}")      # (b-a)²/12

x = np.linspace(0, 9, 200)
y_pdf = dist.pdf(x)
y_cdf = dist.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend()
plt.title(f'Uniform Distribution U({a}, {b})')
plt.xlabel('x')
plt.ylabel('Density / Probability')
plt.show()
```

The PDF is a flat rectangle of height $1/(b-a)$ between $a$ and $b$, and the CDF is a straight line rising from 0 to 1 over that interval.

## Standard Uniform U(0, 1)

The standard uniform distribution $U(0, 1)$ is the default when no parameters are specified:

```python
import scipy.stats as stats

u = stats.uniform()  # U(0, 1) by default
print(f"Mean: {u.mean():.4f}")        # 0.5
print(f"Variance: {u.var():.4f}")      # 1/12 ≈ 0.0833
print(f"P(X ≤ 0.3): {u.cdf(0.3):.4f}")  # 0.3
```

## Key Properties

- **Mean**: $E[X] = \dfrac{a + b}{2}$
- **Variance**: $\text{Var}(X) = \dfrac{(b - a)^2}{12}$
- **Symmetry**: The distribution is symmetric about the midpoint $(a + b)/2$
- **Maximum entropy**: Among all continuous distributions on $[a, b]$, the uniform distribution has the maximum entropy (it encodes the least information)

### Parameters in scipy.stats

| Parameter | Symbol | `scipy.stats` keyword | Default |
|-----------|--------|-----------------------|---------|
| Left endpoint  | $a$ | `loc`            | 0 |
| Interval length | $b - a$ | `scale`      | 1 |

## Probability Integral Transform

The probability integral transform is a fundamental result connecting any continuous distribution to the uniform. If $X$ is a continuous random variable with CDF $F$, then:

$$
F(X) \sim U(0, 1)
$$

Conversely, if $U \sim U(0, 1)$ and $F$ is any continuous CDF, then $X = F^{-1}(U)$ has CDF $F$. This is called **inverse transform sampling** and is the basis for generating random variates from any distribution:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

# Generate exponential(λ=2) samples via inverse transform
u = stats.uniform.rvs(size=5000, random_state=42)
lam = 2.0
x_inv = -np.log(1 - u) / lam  # F⁻¹(u) for exponential

# Compare with direct sampling
x_direct = stats.expon(scale=1/lam).rvs(size=5000, random_state=43)

plt.hist(x_inv, bins=40, density=True, alpha=0.5, label='Inverse transform')
plt.hist(x_direct, bins=40, density=True, alpha=0.5, label='Direct sampling')
plt.legend()
plt.title('Exponential Samples via Inverse Transform vs Direct')
plt.xlabel('x')
plt.ylabel('Density')
plt.show()
```

## Financial Applications

In quantitative finance, the uniform distribution appears in Monte Carlo simulation (all pseudorandom number generators start by producing uniform variates). Copula models use the probability integral transform to convert marginal distributions to uniform margins before applying a dependence structure. Quasi-random sequences (Sobol, Halton) generate low-discrepancy uniform samples for variance reduction in pricing.

## Summary

The uniform distribution assigns equal density across an interval and serves as the foundation for random variate generation through the probability integral transform. In `scipy.stats`, use `stats.uniform(loc=a, scale=b-a)` to represent $U(a, b)$, noting the loc-scale parametrization rather than the endpoint parametrization.

---

## Exercises

**Exercise 1.**
Create a uniform distribution on $[3, 8]$ using `scipy.stats.uniform`. Compute $P(4 \le X \le 6)$ using the CDF and verify it equals $(6 - 4) / (8 - 3)$.

??? success "Solution to Exercise 1"

        from scipy import stats

        rv = stats.uniform(loc=3, scale=5)
        prob = rv.cdf(6) - rv.cdf(4)
        expected = (6 - 4) / (8 - 3)
        print(f"P(4 <= X <= 6) = {prob:.4f}, expected = {expected:.4f}")

---

**Exercise 2.**
Generate 10,000 uniform samples on $[0, 1]$ and apply the CDF of an exponential distribution with $\lambda = 2$ (the probability integral transform in reverse) to produce exponential samples. Verify by comparing the sample mean to $1/\lambda$.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        u = np.random.uniform(0, 1, size=10000)
        exp_samples = stats.expon.ppf(u, scale=0.5)
        print(f"Sample mean: {np.mean(exp_samples):.4f} (expected 0.5)")

---

**Exercise 3.**
Compute the entropy of uniform distributions on $[0, 1]$, $[0, 10]$, and $[0, 100]$. Verify that the entropy equals $\ln(b - a)$.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        for width in [1, 10, 100]:
            rv = stats.uniform(loc=0, scale=width)
            print(f"U[0,{width:3d}]: entropy={rv.entropy():.4f}, ln({width})={np.log(width):.4f}")
