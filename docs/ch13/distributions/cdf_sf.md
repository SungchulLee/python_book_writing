# CDF and Survival Function

The **cumulative distribution function** (CDF) and **survival function** (SF) are complementary functions that describe the probability of a random variable falling below or above a threshold.

!!! tip "Mental Model"
    The CDF answers "what is the probability of being at or below $x$?" and the survival function answers "what is the probability of exceeding $x$?" They always sum to 1. Use the CDF for left-tail probabilities and the SF for right-tail probabilities -- the SF avoids catastrophic floating-point cancellation when the probability is very close to 1.

---

## Cumulative Distribution Function (CDF)

The CDF gives the probability that a random variable $X$ is less than or equal to a value $x$:

$$F(x) = P(X \le x)$$

For continuous distributions this is the integral of the PDF from $-\infty$ to $x$. For discrete distributions it is the sum of the PMF up to $k$.

### Properties of the CDF

The CDF is non-decreasing, right-continuous, and satisfies $\lim_{x \to -\infty} F(x) = 0$ and $\lim_{x \to \infty} F(x) = 1$.

### Continuous Example: Normal Distribution CDF

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mu = 3.0
a = stats.norm(loc=mu)
x = np.linspace(mu - 3, mu + 3, 100)
y_pdf = a.pdf(x)
y_cdf = a.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend(loc='lower left')
plt.title(f'Normal Distribution (μ={mu}, σ=1)')
plt.xlabel('x')
plt.show()
```

The CDF rises from 0 to 1 in an S-shaped (sigmoid) curve. At the mean $\mu$, the CDF equals 0.5.

### Continuous Example: Exponential Distribution CDF

The exponential distribution models waiting times and inter-arrival times. Its CDF rises quickly for high rate parameters:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

la = 3.0  # rate parameter λ
a = stats.expon(scale=1/la)  # scale = 1/λ
x = np.linspace(0, 3, 100)
y_pdf = a.pdf(x)
y_cdf = a.cdf(x)

plt.plot(x, y_pdf, label='PDF')
plt.plot(x, y_cdf, label='CDF')
plt.legend(loc='lower left')
plt.title(f'Exponential Distribution (λ={la})')
plt.xlabel('x')
plt.show()
```

Note the important parametrization detail: `scipy.stats.expon` uses `scale = 1/λ`, so when the rate is $\lambda = 3$, you pass `scale=1/3`.

### Discrete Example: Poisson Distribution CDF

For discrete distributions, the CDF is a step function. A bar chart effectively shows both the PMF and CDF together:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mu = 3.0
a = stats.poisson(mu)
x = np.arange(0, 11)
y_cdf = a.cdf(x)
y_pmf = a.pmf(x)

plt.bar(x, y_cdf, label='CDF', alpha=0.5)
plt.bar(x, y_pmf, label='PMF', alpha=0.5)
plt.legend()
plt.title(f'Poisson Distribution (μ={mu})')
plt.xlabel('k')
plt.show()
```

The CDF bars show the cumulative probability up to each value $k$, while the PMF bars show the individual probability at each $k$.

## Survival Function (SF)

The survival function is the complement of the CDF:

$$S(x) = 1 - F(x) = P(X > x)$$

In `scipy.stats`, use `.sf(x)` instead of computing `1 - .cdf(x)`. The dedicated method is numerically more accurate in the tails where CDF values are very close to 1:

```python
a = stats.norm(loc=0, scale=1)

# These are mathematically equivalent, but sf is more accurate in the tails
p1 = 1 - a.cdf(5)      # may lose precision
p2 = a.sf(5)            # numerically stable
```

## Computing Probabilities Over Intervals

The CDF enables computation of interval probabilities:

$$P(a < X \le b) = F(b) - F(a)$$

```python
a = stats.norm(loc=0, scale=1)
prob = a.cdf(1) - a.cdf(-1)  # P(-1 < X ≤ 1) ≈ 0.6827
```

## Summary

The CDF and survival function are essential tools for probability computation. In `scipy.stats`, `.cdf()` gives $P(X \le x)$ and `.sf()` gives $P(X > x)$ with numerical stability. Together with the PDF/PMF and quantile functions, they form the complete interface for working with probability distributions.

---

## Exercises

**Exercise 1.**
For a standard normal distribution, compute $P(X \le 1.96)$ using `.cdf()` and $P(X > 1.96)$ using `.sf()`. Verify that they sum to 1.

??? success "Solution to Exercise 1"

        from scipy import stats

        rv = stats.norm()
        cdf_val = rv.cdf(1.96)
        sf_val = rv.sf(1.96)
        print(f"P(X <= 1.96) = {cdf_val:.6f}")
        print(f"P(X > 1.96)  = {sf_val:.6f}")
        print(f"Sum = {cdf_val + sf_val:.6f}")

---

**Exercise 2.**
A light bulb lifetime follows an exponential distribution with mean 1000 hours. Compute the probability that a bulb lasts more than 1500 hours using the survival function. Then compute $P(500 \le X \le 1500)$ using the CDF.

??? success "Solution to Exercise 2"

        from scipy import stats

        rv = stats.expon(scale=1000)
        p_gt_1500 = rv.sf(1500)
        p_interval = rv.cdf(1500) - rv.cdf(500)
        print(f"P(X > 1500) = {p_gt_1500:.4f}")
        print(f"P(500 <= X <= 1500) = {p_interval:.4f}")

---

**Exercise 3.**
For a Poisson distribution with $\lambda = 7$, compute $P(X \le 5)$ and $P(X > 10)$ using `.cdf()` and `.sf()` respectively. Verify the SF result by computing $1 - P(X \le 10)$.

??? success "Solution to Exercise 3"

        from scipy import stats

        rv = stats.poisson(mu=7)
        p_le_5 = rv.cdf(5)
        p_gt_10 = rv.sf(10)
        p_gt_10_check = 1 - rv.cdf(10)

        print(f"P(X <= 5)  = {p_le_5:.4f}")
        print(f"P(X > 10)  = {p_gt_10:.6f}")
        print(f"1 - P(X<=10) = {p_gt_10_check:.6f}")
        print(f"Match: {abs(p_gt_10 - p_gt_10_check) < 1e-10}")
