# Statistical Distributions Visualization

This document provides practical examples for visualizing probability distributions, including PDFs, CDFs, and comparisons across distribution families.

!!! tip "Mental Model"
    Visualizing distributions means plotting their PDF (bell curve shape), CDF (cumulative probability from 0 to 1), or both. Use `scipy.stats` to compute the theoretical curves and Matplotlib to draw them. Overlaying multiple distributions on one Axes with `ax.plot()` and a legend makes parameter effects (e.g., changing mean or variance) immediately visible.

!!! note "When to Use Which Distribution"
    The shape of a distribution encodes its generating mechanism:

    | Distribution | Shape | Use when |
    |-------------|-------|----------|
    | Normal | Symmetric bell | Sums of many small effects (CLT) |
    | Exponential | Decaying right tail | Waiting times between events |
    | Uniform | Flat | No prior information, equal likelihood |
    | Poisson | Discrete, right-skewed | Counting rare events in fixed intervals |
    | Binomial | Discrete, symmetric for large $n$ | Fixed number of yes/no trials |
    | Gamma | Flexible right-skewed | Sum of exponential waiting times |

    Many distributions are related: Gamma generalizes Exponential ($k=1$),
    Chi-squared is Gamma with specific parameters, and Poisson approximates
    Binomial for large $n$ and small $p$. Overlaying related distributions on
    one plot makes these connections visible.

!!! note "Unifying Idea: Everything Is Density"
    All continuous distributions define a density function $f(x)$ — the same
    concept that appears throughout this book:

    - **Histograms** → empirical density (counting)
    - **KDE** → smoothed density (estimation)
    - **2D density plots** → density in two dimensions
    - **Distributions on this page** → theoretical density (closed-form)

    Visualizing distributions is visualizing density from the theoretical side,
    just as histograms and KDE visualize it from the data side.

## Setup

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
```

---

## Normal Distribution

### 1. Standard Normal

```python
x = np.linspace(-4, 4, 200)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# PDF
axes[0].plot(x, stats.norm.pdf(x), 'b-', linewidth=2)
axes[0].fill_between(x, stats.norm.pdf(x), alpha=0.3)
axes[0].set_title('Standard Normal PDF')
axes[0].set_xlabel('x')
axes[0].set_ylabel('f(x)')
axes[0].grid(alpha=0.3)

# CDF
axes[1].plot(x, stats.norm.cdf(x), 'r-', linewidth=2)
axes[1].set_title('Standard Normal CDF')
axes[1].set_xlabel('x')
axes[1].set_ylabel('F(x)')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

### 2. Varying Parameters

```python
x = np.linspace(-10, 10, 200)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Varying mean
for mu in [-2, 0, 2]:
    axes[0].plot(x, stats.norm(mu, 1).pdf(x), label=f'μ={mu}')
axes[0].set_title('Effect of Mean (σ=1)')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Varying std
for sigma in [0.5, 1, 2]:
    axes[1].plot(x, stats.norm(0, sigma).pdf(x), label=f'σ={sigma}')
axes[1].set_title('Effect of Std Dev (μ=0)')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

### 3. Normal Distribution Dashboard

```python
mu, sigma = 2, 1.5
x = np.linspace(-4, 8, 200)
rv = stats.norm(mu, sigma)

fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# PDF
axes[0, 0].plot(x, rv.pdf(x), 'b-', linewidth=2)
axes[0, 0].fill_between(x, rv.pdf(x), alpha=0.3)
axes[0, 0].axvline(mu, color='red', linestyle='--', label=f'μ={mu}')
axes[0, 0].set_title('Probability Density Function')
axes[0, 0].legend()
axes[0, 0].grid(alpha=0.3)

# CDF
axes[0, 1].plot(x, rv.cdf(x), 'g-', linewidth=2)
axes[0, 1].axhline(0.5, color='gray', linestyle=':', alpha=0.7)
axes[0, 1].axvline(mu, color='red', linestyle='--')
axes[0, 1].set_title('Cumulative Distribution Function')
axes[0, 1].grid(alpha=0.3)

# Histogram + PDF
np.random.seed(42)
samples = rv.rvs(1000)
axes[1, 0].hist(samples, bins=30, density=True, alpha=0.7, label='Samples')
axes[1, 0].plot(x, rv.pdf(x), 'r-', linewidth=2, label='PDF')
axes[1, 0].set_title('Sample Histogram vs PDF')
axes[1, 0].legend()
axes[1, 0].grid(alpha=0.3)

# Q-Q Plot
stats.probplot(samples, dist="norm", plot=axes[1, 1])
axes[1, 1].set_title('Q-Q Plot')
axes[1, 1].grid(alpha=0.3)

plt.suptitle(f'Normal Distribution (μ={mu}, σ={sigma})', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## Exponential Distribution

### 1. Basic Visualization

```python
x = np.linspace(0, 8, 200)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for lam in [0.5, 1, 2]:
    rv = stats.expon(scale=1/lam)
    axes[0].plot(x, rv.pdf(x), label=f'λ={lam}')
    axes[1].plot(x, rv.cdf(x), label=f'λ={lam}')

axes[0].set_title('Exponential PDF')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].set_title('Exponential CDF')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Gamma Distribution

```python
x = np.linspace(0, 20, 200)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Varying shape (k)
for k in [1, 2, 5, 9]:
    rv = stats.gamma(a=k, scale=1)
    axes[0].plot(x, rv.pdf(x), label=f'k={k}, θ=1')

axes[0].set_title('Gamma PDF: Varying Shape')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Varying scale (θ)
for theta in [0.5, 1, 2]:
    rv = stats.gamma(a=3, scale=theta)
    axes[1].plot(x, rv.pdf(x), label=f'k=3, θ={theta}')

axes[1].set_title('Gamma PDF: Varying Scale')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## Beta Distribution

```python
x = np.linspace(0, 1, 200)

fig, ax = plt.subplots(figsize=(10, 6))

params = [(0.5, 0.5), (2, 2), (2, 5), (5, 2), (1, 3)]
colors = plt.cm.viridis(np.linspace(0, 1, len(params)))

for (a, b), color in zip(params, colors):
    rv = stats.beta(a, b)
    ax.plot(x, rv.pdf(x), color=color, linewidth=2, label=f'α={a}, β={b}')

ax.set_title('Beta Distribution')
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.legend()
ax.grid(alpha=0.3)
plt.show()
```

---

## Student's t-Distribution

```python
x = np.linspace(-5, 5, 200)

fig, ax = plt.subplots(figsize=(10, 6))

# Normal for reference
ax.plot(x, stats.norm.pdf(x), 'k--', linewidth=2, label='Normal')

# t-distributions with various df
for df in [1, 2, 5, 30]:
    ax.plot(x, stats.t(df).pdf(x), linewidth=2, label=f't (df={df})')

ax.set_title("Student's t-Distribution")
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.legend()
ax.grid(alpha=0.3)
plt.show()
```

---

## Chi-Square Distribution

```python
x = np.linspace(0, 30, 200)

fig, ax = plt.subplots(figsize=(10, 6))

for df in [1, 2, 3, 5, 10]:
    ax.plot(x, stats.chi2(df).pdf(x), linewidth=2, label=f'df={df}')

ax.set_title('Chi-Square Distribution')
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.legend()
ax.grid(alpha=0.3)
ax.set_ylim(0, 0.5)
plt.show()
```

---

## Discrete Distributions

### 1. Binomial Distribution

```python
n = 20
x = np.arange(0, n + 1)

fig, ax = plt.subplots(figsize=(10, 6))

for p in [0.2, 0.5, 0.7]:
    pmf = stats.binom(n, p).pmf(x)
    ax.bar(x + (p - 0.5) * 0.25, pmf, width=0.25, alpha=0.7, label=f'p={p}')

ax.set_title(f'Binomial Distribution (n={n})')
ax.set_xlabel('k')
ax.set_ylabel('P(X = k)')
ax.legend()
ax.grid(alpha=0.3, axis='y')
plt.show()
```

### 2. Poisson Distribution

```python
x = np.arange(0, 20)

fig, ax = plt.subplots(figsize=(10, 6))

for lam in [1, 4, 10]:
    pmf = stats.poisson(lam).pmf(x)
    ax.plot(x, pmf, 'o-', linewidth=2, markersize=6, label=f'λ={lam}')

ax.set_title('Poisson Distribution')
ax.set_xlabel('k')
ax.set_ylabel('P(X = k)')
ax.legend()
ax.grid(alpha=0.3)
plt.show()
```

### 3. Geometric Distribution

```python
x = np.arange(1, 15)

fig, ax = plt.subplots(figsize=(10, 6))

for p in [0.2, 0.5, 0.8]:
    pmf = stats.geom(p).pmf(x)
    ax.bar(x + (p - 0.5) * 0.25, pmf, width=0.25, alpha=0.7, label=f'p={p}')

ax.set_title('Geometric Distribution')
ax.set_xlabel('k (number of trials)')
ax.set_ylabel('P(X = k)')
ax.legend()
ax.grid(alpha=0.3, axis='y')
plt.show()
```

---

## Distribution Comparisons

### 1. Normal vs t-Distribution

```python
x = np.linspace(-5, 5, 200)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# PDF comparison
axes[0].plot(x, stats.norm.pdf(x), 'b-', linewidth=2, label='Normal')
axes[0].plot(x, stats.t(5).pdf(x), 'r-', linewidth=2, label='t (df=5)')
axes[0].fill_between(x, stats.norm.pdf(x), stats.t(5).pdf(x), alpha=0.3)
axes[0].set_title('PDF Comparison')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Tail comparison
x_tail = np.linspace(2, 5, 100)
axes[1].plot(x_tail, stats.norm.pdf(x_tail), 'b-', linewidth=2, label='Normal')
axes[1].plot(x_tail, stats.t(5).pdf(x_tail), 'r-', linewidth=2, label='t (df=5)')
axes[1].set_title('Right Tail Comparison')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.suptitle('Normal vs t-Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### 2. Exponential Family

```python
x = np.linspace(0, 10, 200)

fig, ax = plt.subplots(figsize=(10, 6))

# Exponential
ax.plot(x, stats.expon(scale=2).pdf(x), label='Exponential (λ=0.5)')

# Gamma
ax.plot(x, stats.gamma(a=2, scale=1).pdf(x), label='Gamma (k=2, θ=1)')

# Chi-square
ax.plot(x, stats.chi2(4).pdf(x), label='Chi-square (df=4)')

ax.set_title('Exponential Family Distributions')
ax.set_xlabel('x')
ax.set_ylabel('Density')
ax.legend()
ax.grid(alpha=0.3)
plt.show()
```

---

## Bivariate Distributions

### 1. Bivariate Normal

```python
from scipy import stats

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

rhos = [-0.7, 0, 0.7]

for ax, rho in zip(axes, rhos):
    rv = stats.multivariate_normal([0, 0], [[1, rho], [rho, 1]])
    Z = rv.pdf(pos)
    cf = ax.contourf(X, Y, Z, levels=15, cmap='Blues')
    ax.contour(X, Y, Z, levels=8, colors='navy', linewidths=0.5)
    ax.set_title(f'ρ = {rho}')
    ax.set_aspect('equal')
    plt.colorbar(cf, ax=ax)

plt.suptitle('Bivariate Normal Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

### 2. Bivariate Normal with Marginals

```python
from mpl_toolkits.axes_grid1 import make_axes_locatable

np.random.seed(42)
rho = 0.6
mean = [0, 0]
cov = [[1, rho], [rho, 1]]
data = np.random.multivariate_normal(mean, cov, 500)

fig, ax_main = plt.subplots(figsize=(8, 8))
divider = make_axes_locatable(ax_main)
ax_top = divider.append_axes("top", 1.2, pad=0.1, sharex=ax_main)
ax_right = divider.append_axes("right", 1.2, pad=0.1, sharey=ax_main)

# Main scatter
ax_main.scatter(data[:, 0], data[:, 1], alpha=0.5, s=20)
ax_main.set_xlabel('X')
ax_main.set_ylabel('Y')

# Marginals
ax_top.hist(data[:, 0], bins=30, density=True, alpha=0.7)
x_range = np.linspace(-4, 4, 100)
ax_top.plot(x_range, stats.norm.pdf(x_range), 'r-', linewidth=2)
plt.setp(ax_top.get_xticklabels(), visible=False)

ax_right.hist(data[:, 1], bins=30, density=True, alpha=0.7, orientation='horizontal')
ax_right.plot(stats.norm.pdf(x_range), x_range, 'r-', linewidth=2)
plt.setp(ax_right.get_yticklabels(), visible=False)

plt.suptitle(f'Bivariate Normal (ρ={rho}) with Marginals', fontsize=13, y=1.02)
plt.show()
```

---

## Distribution Gallery

### Complete Overview

```python
fig, axes = plt.subplots(3, 3, figsize=(15, 12))

# Normal
x = np.linspace(-4, 4, 200)
axes[0, 0].plot(x, stats.norm.pdf(x), 'b-', linewidth=2)
axes[0, 0].fill_between(x, stats.norm.pdf(x), alpha=0.3)
axes[0, 0].set_title('Normal')

# Exponential
x = np.linspace(0, 6, 200)
axes[0, 1].plot(x, stats.expon.pdf(x), 'g-', linewidth=2)
axes[0, 1].fill_between(x, stats.expon.pdf(x), alpha=0.3)
axes[0, 1].set_title('Exponential')

# Uniform
x = np.linspace(-0.5, 1.5, 200)
axes[0, 2].plot(x, stats.uniform.pdf(x), 'r-', linewidth=2)
axes[0, 2].fill_between(x, stats.uniform.pdf(x), alpha=0.3)
axes[0, 2].set_title('Uniform')

# Gamma
x = np.linspace(0, 15, 200)
axes[1, 0].plot(x, stats.gamma(a=3).pdf(x), 'purple', linewidth=2)
axes[1, 0].fill_between(x, stats.gamma(a=3).pdf(x), alpha=0.3, color='purple')
axes[1, 0].set_title('Gamma (k=3)')

# Beta
x = np.linspace(0, 1, 200)
axes[1, 1].plot(x, stats.beta(2, 5).pdf(x), 'orange', linewidth=2)
axes[1, 1].fill_between(x, stats.beta(2, 5).pdf(x), alpha=0.3, color='orange')
axes[1, 1].set_title('Beta (α=2, β=5)')

# Chi-square
x = np.linspace(0, 20, 200)
axes[1, 2].plot(x, stats.chi2(5).pdf(x), 'brown', linewidth=2)
axes[1, 2].fill_between(x, stats.chi2(5).pdf(x), alpha=0.3, color='brown')
axes[1, 2].set_title('Chi-square (df=5)')

# Binomial
x = np.arange(0, 21)
axes[2, 0].bar(x, stats.binom(20, 0.5).pmf(x), color='steelblue', alpha=0.7)
axes[2, 0].set_title('Binomial (n=20, p=0.5)')

# Poisson
x = np.arange(0, 15)
axes[2, 1].bar(x, stats.poisson(5).pmf(x), color='seagreen', alpha=0.7)
axes[2, 1].set_title('Poisson (λ=5)')

# Geometric
x = np.arange(1, 12)
axes[2, 2].bar(x, stats.geom(0.3).pmf(x), color='coral', alpha=0.7)
axes[2, 2].set_title('Geometric (p=0.3)')

for ax in axes.flat:
    ax.grid(alpha=0.3)

plt.suptitle('Common Probability Distributions', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## Publication-Quality Figure

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Normal with shaded regions
x = np.linspace(-4, 4, 200)
rv = stats.norm()
axes[0, 0].plot(x, rv.pdf(x), 'steelblue', linewidth=2)
axes[0, 0].fill_between(x, rv.pdf(x), where=(x >= -1) & (x <= 1), alpha=0.4, color='steelblue')
axes[0, 0].fill_between(x, rv.pdf(x), where=(x >= -2) & (x <= 2), alpha=0.2, color='steelblue')
axes[0, 0].axvline(-1, color='gray', linestyle=':', alpha=0.7)
axes[0, 0].axvline(1, color='gray', linestyle=':', alpha=0.7)
axes[0, 0].set_title('Standard Normal with σ Regions', fontsize=12)
axes[0, 0].set_xlabel('$x$')
axes[0, 0].set_ylabel('$f(x)$')

# t-distribution comparison
axes[0, 1].plot(x, rv.pdf(x), 'b-', linewidth=2, label='Normal')
for df, color in [(3, 'orange'), (10, 'green')]:
    axes[0, 1].plot(x, stats.t(df).pdf(x), color=color, linewidth=2, label=f't (df={df})')
axes[0, 1].set_title('Normal vs t-Distribution', fontsize=12)
axes[0, 1].legend()
axes[0, 1].set_xlabel('$x$')
axes[0, 1].set_ylabel('$f(x)$')

# Gamma family
x = np.linspace(0, 15, 200)
for k, color in [(1, 'red'), (2, 'green'), (5, 'blue')]:
    axes[1, 0].plot(x, stats.gamma(a=k).pdf(x), color=color, linewidth=2, label=f'k={k}')
axes[1, 0].set_title('Gamma Distribution Family', fontsize=12)
axes[1, 0].legend()
axes[1, 0].set_xlabel('$x$')
axes[1, 0].set_ylabel('$f(x)$')

# Beta distribution
x = np.linspace(0, 1, 200)
params = [(2, 2), (2, 5), (5, 2)]
colors = ['blue', 'green', 'red']
for (a, b), color in zip(params, colors):
    axes[1, 1].plot(x, stats.beta(a, b).pdf(x), color=color, linewidth=2, label=f'α={a}, β={b}')
axes[1, 1].set_title('Beta Distribution', fontsize=12)
axes[1, 1].legend()
axes[1, 1].set_xlabel('$x$')
axes[1, 1].set_ylabel('$f(x)$')

for ax in axes.flat:
    ax.grid(alpha=0.3)
    ax.tick_params(labelsize=10)

plt.suptitle('Probability Distribution Examples', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
```

---

## Summary Table

| Distribution | scipy.stats | Parameters | Support |
|--------------|-------------|------------|---------|
| Normal | `norm(loc, scale)` | μ, σ | (-∞, ∞) |
| Exponential | `expon(scale=1/λ)` | λ | [0, ∞) |
| Gamma | `gamma(a, scale)` | k, θ | [0, ∞) |
| Beta | `beta(a, b)` | α, β | [0, 1] |
| t | `t(df)` | df | (-∞, ∞) |
| Chi-square | `chi2(df)` | df | [0, ∞) |
| Binomial | `binom(n, p)` | n, p | {0,...,n} |
| Poisson | `poisson(mu)` | λ | {0,1,2,...} |
| Geometric | `geom(p)` | p | {1,2,3,...} |


---

## Exercises

**Exercise 1.** Write code that plots the probability density function (PDF) of a standard normal distribution $N(0, 1)$ and shades the area for $|x| > 1.96$ (the 95% confidence region tails).

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    x = np.linspace(-4, 4, 500)
    y = stats.norm.pdf(x)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, y, 'b-', lw=2)

    x_left = x[x < -1.96]
    x_right = x[x > 1.96]
    ax.fill_between(x_left, stats.norm.pdf(x_left), alpha=0.4, color='red')
    ax.fill_between(x_right, stats.norm.pdf(x_right), alpha=0.4, color='red')

    ax.set_xlabel('$x$')
    ax.set_ylabel('Density')
    ax.set_title('Standard Normal PDF with 95% Confidence Tails')
    plt.show()
    ```

---

**Exercise 2.** Create a figure with 2x2 subplots showing the PDFs of four distributions: Normal(0, 1), Exponential(1), Uniform(0, 1), and Chi-squared(3). Label each subplot with the distribution name.

??? success "Solution to Exercise 2"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    x1 = np.linspace(-4, 4, 200)
    axes[0, 0].plot(x1, stats.norm.pdf(x1), 'b-', lw=2)
    axes[0, 0].set_title('Normal(0, 1)')
    axes[0, 0].grid(True, alpha=0.3)

    x2 = np.linspace(0, 6, 200)
    axes[0, 1].plot(x2, stats.expon.pdf(x2), 'r-', lw=2)
    axes[0, 1].set_title('Exponential(1)')
    axes[0, 1].grid(True, alpha=0.3)

    x3 = np.linspace(-0.5, 1.5, 200)
    axes[1, 0].plot(x3, stats.uniform.pdf(x3), 'g-', lw=2)
    axes[1, 0].set_title('Uniform(0, 1)')
    axes[1, 0].grid(True, alpha=0.3)

    x4 = np.linspace(0, 12, 200)
    axes[1, 1].plot(x4, stats.chi2.pdf(x4, df=3), 'm-', lw=2)
    axes[1, 1].set_title('Chi-squared(df=3)')
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 3.** Write code that generates 10000 samples from a normal distribution, plots a histogram with `density=True`, and overlays the theoretical PDF curve. Include a legend distinguishing the histogram from the theoretical curve.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    samples = np.random.randn(10000)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(samples, bins=50, density=True, alpha=0.7, label='Histogram')

    x = np.linspace(-4, 4, 200)
    ax.plot(x, stats.norm.pdf(x), 'r-', lw=2, label='Theoretical PDF')

    ax.set_xlabel('$x$')
    ax.set_ylabel('Density')
    ax.set_title('Histogram vs Theoretical Normal PDF')
    ax.legend()
    plt.show()
    ```

---

**Exercise 4.** Create a plot comparing three normal distributions with different parameters: $N(0, 1)$, $N(0, 2)$, and $N(2, 1)$. Use different colors and line styles for each, and add a legend.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy import stats

    x = np.linspace(-6, 8, 500)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, stats.norm(0, 1).pdf(x), 'b-', lw=2, label='$N(0, 1)$')
    ax.plot(x, stats.norm(0, 2).pdf(x), 'r--', lw=2, label='$N(0, 2)$')
    ax.plot(x, stats.norm(2, 1).pdf(x), 'g-.', lw=2, label='$N(2, 1)$')

    ax.set_xlabel('$x$')
    ax.set_ylabel('Density')
    ax.set_title('Comparison of Normal Distributions')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()
    ```
