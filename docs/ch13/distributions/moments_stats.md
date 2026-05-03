# Moments and Stats

The **moments** of a probability distribution encode its shape: the mean locates the center, the variance measures spread, skewness quantifies asymmetry, and kurtosis captures tail weight. Rather than estimating these from samples, `scipy.stats` distribution objects compute them analytically from the distribution's parameters, giving exact values with no sampling error. This page defines each moment and demonstrates the corresponding `scipy.stats` methods.

!!! tip "Mental Model"
    Distribution objects know their own moments exactly -- no sampling needed. Calling `.mean()` or `.var()` on a frozen distribution returns the theoretical value derived from the parameters, not an estimate. This is useful for verifying simulation results or computing quantities like the coefficient of variation without generating any data.

---

## Mean and Variance

The **mean** (first moment about the origin) of a continuous random variable $X$ with PDF $f$ is:

$$
\mu = \mathbb{E}[X] = \int_{-\infty}^{\infty} x \, f(x) \, dx
$$

The **variance** (second central moment) measures the expected squared deviation from the mean:

$$
\sigma^2 = \operatorname{Var}(X) = \mathbb{E}\!\left[(X - \mu)^2\right] = \int_{-\infty}^{\infty} (x - \mu)^2 \, f(x) \, dx
$$

The **standard deviation** is $\sigma = \sqrt{\sigma^2}$.

### Computing Mean, Variance, and Standard Deviation

```python
import scipy.stats as stats

# Normal distribution with μ=5, σ=2
dist = stats.norm(loc=5, scale=2)

print(f"Mean:     {dist.mean():.4f}")       # 5.0
print(f"Variance: {dist.var():.4f}")         # 4.0
print(f"Std dev:  {dist.std():.4f}")         # 2.0
```

These methods return exact analytical values. For the normal distribution, `.mean()` returns `loc`, `.var()` returns `scale**2`, and `.std()` returns `scale`.

### Example: Gamma Distribution

The gamma distribution with shape $a$ and scale $\theta$ has mean $a\theta$ and variance $a\theta^2$:

```python
dist = stats.gamma(a=3, scale=2)
print(f"Mean:     {dist.mean():.4f}")       # 6.0  (3 * 2)
print(f"Variance: {dist.var():.4f}")         # 12.0 (3 * 4)
```

## Skewness and Kurtosis

The **skewness** measures asymmetry of the distribution about its mean:

$$
\gamma_1 = \mathbb{E}\!\left[\left(\frac{X - \mu}{\sigma}\right)^{\!3}\right]
$$

A positive value indicates a right tail longer than the left; a negative value indicates the opposite. A symmetric distribution has $\gamma_1 = 0$.

The **excess kurtosis** measures the heaviness of the tails relative to the normal distribution:

$$
\gamma_2 = \mathbb{E}\!\left[\left(\frac{X - \mu}{\sigma}\right)^{\!4}\right] - 3
$$

The subtraction of 3 makes the normal distribution the reference point with $\gamma_2 = 0$. Positive excess kurtosis (leptokurtic) indicates heavier tails; negative (platykurtic) indicates lighter tails.

!!! note "Excess vs raw kurtosis"
    SciPy reports **excess kurtosis** (subtracting 3). Some other software reports raw kurtosis without the subtraction. Always check the convention before comparing values.

## The .stats() Method

The `.stats()` method returns multiple moments in a single call. The `moments` keyword controls which are computed, using a string of characters:

| Character | Moment |
|---|---|
| `m` | Mean |
| `v` | Variance |
| `s` | Skewness |
| `k` | Excess kurtosis |

```python
dist = stats.norm(loc=0, scale=1)
mean, var, skew, kurt = dist.stats(moments='mvsk')
print(f"Mean={mean:.2f}, Var={var:.2f}, Skew={skew:.2f}, Kurt={kurt:.2f}")
# Mean=0.00, Var=1.00, Skew=0.00, Kurt=0.00
```

### Example: Exponential Distribution

The exponential distribution with rate $\lambda$ (scale $= 1/\lambda$) is right-skewed:

```python
dist = stats.expon(scale=1.0)
mean, var, skew, kurt = dist.stats(moments='mvsk')
print(f"Mean={mean:.2f}, Var={var:.2f}, Skew={skew:.2f}, Kurt={kurt:.2f}")
# Mean=1.00, Var=1.00, Skew=2.00, Kurt=6.00
```

The skewness of 2 confirms the strong right skew, and the excess kurtosis of 6 indicates substantially heavier tails than the normal.

## The .moment() Method

The `.moment(n)` method computes the $n$-th **non-central moment** $\mathbb{E}[X^n]$:

```python
dist = stats.norm(loc=0, scale=1)

# First non-central moment = mean
print(f"E[X]   = {dist.moment(1):.4f}")    # 0.0

# Second non-central moment = E[X^2] = Var + mean^2
print(f"E[X^2] = {dist.moment(2):.4f}")    # 1.0

# Fourth non-central moment
print(f"E[X^4] = {dist.moment(4):.4f}")    # 3.0
```

!!! tip "Non-central vs central moments"
    The `.moment(n)` method returns $\mathbb{E}[X^n]$, not $\mathbb{E}[(X-\mu)^n]$. To get the $n$-th central moment, compute it from non-central moments. For example, $\operatorname{Var}(X) = \mathbb{E}[X^2] - (\mathbb{E}[X])^2$.

## The .entropy() Method

The **differential entropy** of a continuous distribution measures its uncertainty:

$$
h(X) = -\int_{-\infty}^{\infty} f(x) \ln f(x) \, dx
$$

```python
# Normal distribution: entropy = 0.5 * ln(2πeσ²)
dist = stats.norm(loc=0, scale=1)
print(f"Entropy: {dist.entropy():.4f}")     # 1.4189
```

Higher entropy indicates greater spread or uncertainty in the distribution.

## Method Summary

| Method | Returns | Notes |
|---|---|---|
| `.mean()` | $\mathbb{E}[X]$ | First moment about the origin |
| `.var()` | $\operatorname{Var}(X)$ | Second central moment |
| `.std()` | $\sigma$ | Square root of variance |
| `.stats(moments='mvsk')` | Tuple of selected moments | Any subset of `m`, `v`, `s`, `k` |
| `.moment(n)` | $\mathbb{E}[X^n]$ | $n$-th non-central moment |
| `.entropy()` | $h(X)$ | Differential entropy (nats) |

## Summary

The moments of a distribution — mean, variance, skewness, and kurtosis — summarize its center, spread, asymmetry, and tail behavior. In `scipy.stats`, the `.mean()`, `.var()`, `.std()`, and `.stats()` methods compute these analytically from the distribution parameters, while `.moment(n)` provides arbitrary non-central moments. These exact values serve as benchmarks when comparing against sample estimates computed from data.

---

## Exercises

**Exercise 1.**
For an exponential distribution with $\lambda = 0.5$ (i.e., `scale=2`), compute the mean, variance, skewness, and kurtosis using `.stats(moments='mvsk')`. Verify the mean equals $1/\lambda$.

??? success "Solution to Exercise 1"

        from scipy import stats

        rv = stats.expon(scale=2)
        m, v, s, k = rv.stats(moments='mvsk')
        print(f"Mean: {float(m):.4f} (expected {1/0.5:.4f})")
        print(f"Variance: {float(v):.4f}")
        print(f"Skewness: {float(s):.4f}")
        print(f"Kurtosis: {float(k):.4f}")

---

**Exercise 2.**
Compute the differential entropy of a normal distribution for $\sigma = 1, 2, 5$ using the `.entropy()` method. Verify that the entropy of $N(0, \sigma^2)$ equals $\frac{1}{2}\ln(2\pi e \sigma^2)$.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        for sigma in [1, 2, 5]:
            rv = stats.norm(scale=sigma)
            entropy = rv.entropy()
            expected = 0.5 * np.log(2 * np.pi * np.e * sigma**2)
            print(f"sigma={sigma}: entropy={entropy:.4f}, expected={expected:.4f}, "
                  f"match={np.isclose(entropy, expected)}")

---

**Exercise 3.**
Use `.moment(n)` to compute the 1st through 4th non-central moments of a standard normal distribution. Verify that odd moments are zero and the 2nd moment equals 1.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        rv = stats.norm()
        for n in range(1, 5):
            moment_val = rv.moment(n)
            print(f"E[X^{n}] = {moment_val:.4f}")
