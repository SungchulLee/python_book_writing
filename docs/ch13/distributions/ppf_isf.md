# Quantile Function

The CDF answers "what is the probability that $X \le x$?" The **quantile function** inverts that question: "at what value $x$ does the cumulative probability reach $q$?" This inverse operation is central to statistical practice — it determines critical values for hypothesis tests, endpoints of confidence intervals, and the theoretical quantiles used in QQ plots. In `scipy.stats`, the quantile function is called `ppf` (percent point function) and its survival-function counterpart is `isf` (inverse survival function).

!!! tip "Mental Model"
    The CDF maps values to probabilities; the PPF (quantile function) maps probabilities back to values. It is the CDF run in reverse. Whenever you need a critical value or a confidence interval endpoint, you are using the PPF -- for example, `ppf(0.975)` for the standard normal gives the familiar 1.96.

---

## Quantile Function (ppf)

For a continuous random variable $X$ with CDF $F$, the **quantile function** at probability level $q \in (0, 1)$ is:

$$
F^{-1}(q) = \inf\{x \in \mathbb{R} : F(x) \ge q\}
$$

When $F$ is strictly increasing and continuous, this reduces to the ordinary inverse: $F^{-1}(q)$ is the unique $x$ satisfying $F(x) = q$. In `scipy.stats`, this is the `.ppf(q)` method.

### Example: Standard Normal Quantiles

The most commonly used quantiles of the standard normal distribution:

```python
import scipy.stats as stats

dist = stats.norm(loc=0, scale=1)

# Median
print(f"ppf(0.50) = {dist.ppf(0.50):.4f}")   # 0.0000

# 95th percentile
print(f"ppf(0.95) = {dist.ppf(0.95):.4f}")   # 1.6449

# 97.5th percentile (used for two-sided 95% CI)
print(f"ppf(0.975) = {dist.ppf(0.975):.4f}") # 1.9600
```

The value 1.96 is the critical value that places 2.5% probability in each tail, forming the basis of the 95% confidence interval for normally distributed data.

### Example: Student's t-Distribution

For the $t$-distribution, quantiles depend on the degrees of freedom. With fewer degrees of freedom, the tails are heavier and critical values are larger:

```python
for df in [5, 10, 30, 100]:
    critical = stats.t.ppf(0.975, df=df)
    print(f"df={df:3d}: t_0.975 = {critical:.4f}")
```

As $\text{df} \to \infty$, the $t$-quantiles converge to the normal quantiles.

## Inverse Survival Function (isf)

The **survival function** is $S(x) = 1 - F(x) = P(X > x)$. Its inverse, the **inverse survival function**, returns the value $x$ at which the upper-tail probability equals $q$:

$$
S^{-1}(q) = F^{-1}(1 - q)
$$

In `scipy.stats`, this is the `.isf(q)` method.

```python
dist = stats.norm(loc=0, scale=1)

# isf(0.05) = ppf(0.95)
print(f"isf(0.05) = {dist.isf(0.05):.4f}")   # 1.6449
print(f"ppf(0.95) = {dist.ppf(0.95):.4f}")   # 1.6449
```

!!! tip "When to use isf instead of ppf"
    Use `.isf()` when working with upper-tail probabilities (e.g., "find the value exceeded with probability 0.01"). It avoids the subtraction `ppf(1 - q)`, which can lose numerical precision when $q$ is very small. For example, `isf(1e-15)` is more accurate than `ppf(1 - 1e-15)`.

## Relationship Between ppf, isf, cdf, and sf

The four functions form two inverse pairs:

| Function | Inverse |
|---|---|
| `.cdf(x)` returns $q$ | `.ppf(q)` returns $x$ |
| `.sf(x)` returns $q$ | `.isf(q)` returns $x$ |

Verifying the inverse relationship:

```python
dist = stats.norm(loc=0, scale=1)

x = 1.5
q = dist.cdf(x)
x_back = dist.ppf(q)
print(f"cdf({x}) = {q:.6f}, ppf({q:.6f}) = {x_back:.6f}")

q_sf = dist.sf(x)
x_back_sf = dist.isf(q_sf)
print(f"sf({x}) = {q_sf:.6f}, isf({q_sf:.6f}) = {x_back_sf:.6f}")
```

For a detailed treatment of the CDF and survival function, see the [CDF and Survival Function](cdf_sf.md) page.

## Vectorized Evaluation

Both `.ppf()` and `.isf()` accept arrays for efficient computation of multiple quantiles at once:

```python
import numpy as np

dist = stats.norm(loc=0, scale=1)
probabilities = np.array([0.01, 0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99])
quantiles = dist.ppf(probabilities)

for p, q in zip(probabilities, quantiles):
    print(f"  ppf({p:.2f}) = {q:+.4f}")
```

## Applications of the Quantile Function

The quantile function underpins several common statistical operations:

- **Critical values**: Hypothesis tests compare a test statistic to $F^{-1}(1 - \alpha)$ or $F^{-1}(\alpha/2)$.
- **Confidence intervals**: The `.interval()` method is built on two calls to `.ppf()`. See the [Confidence Intervals](interval.md) page.
- **QQ plots**: Theoretical quantiles $F^{-1}(p_i)$ are plotted against observed order statistics to assess distributional fit.
- **Random variate generation**: The inverse transform method generates samples by applying $F^{-1}$ to uniform random numbers: $X = F^{-1}(U)$ where $U \sim \text{Uniform}(0,1)$.

## Summary

The quantile function $F^{-1}(q)$ and inverse survival function $S^{-1}(q) = F^{-1}(1-q)$ invert the CDF and survival function respectively. In `scipy.stats`, `.ppf()` computes quantiles from lower-tail probabilities and `.isf()` from upper-tail probabilities. These methods provide critical values, confidence interval endpoints, and the theoretical quantiles needed for probability plots.

---

## Exercises

**Exercise 1.**
Find the critical values $z_{0.025}$ and $z_{0.975}$ for the standard normal distribution using `.ppf()`. Then find the same upper-tail critical value $z_{0.025}$ using `.isf()` and verify the results match.

??? success "Solution to Exercise 1"

        from scipy import stats

        rv = stats.norm()
        z_low = rv.ppf(0.025)
        z_high = rv.ppf(0.975)
        z_isf = rv.isf(0.025)

        print(f"z_0.025 (ppf) = {z_low:.4f}")
        print(f"z_0.975 (ppf) = {z_high:.4f}")
        print(f"z_0.025 (isf) = {z_isf:.4f}")
        print(f"ppf(0.975) == isf(0.025): {abs(z_high - z_isf) < 1e-10}")

---

**Exercise 2.**
For a $t$-distribution with 10 degrees of freedom, find the critical values that enclose the middle 99% of the distribution. Compare these with the corresponding standard normal critical values.

??? success "Solution to Exercise 2"

        from scipy import stats

        t_rv = stats.t(df=10)
        t_low = t_rv.ppf(0.005)
        t_high = t_rv.ppf(0.995)

        z_low = stats.norm.ppf(0.005)
        z_high = stats.norm.ppf(0.995)

        print(f"t(10) 99% critical values: [{t_low:.4f}, {t_high:.4f}]")
        print(f"Normal 99% critical values: [{z_low:.4f}, {z_high:.4f}]")
        print(f"t critical value is wider by: {t_high - z_high:.4f}")

---

**Exercise 3.**
Generate 1000 samples from a uniform distribution on $[0, 1]$ and transform them to standard normal samples using `stats.norm.ppf()`. Verify the transformation by computing the mean and standard deviation of the resulting samples.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        u = np.random.uniform(0, 1, size=1000)
        z = stats.norm.ppf(u)

        print(f"Mean: {np.mean(z):.4f} (expected ~0)")
        print(f"Std:  {np.std(z, ddof=1):.4f} (expected ~1)")
