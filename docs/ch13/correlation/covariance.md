# Covariance and Covariance Matrix

Covariance is the foundational measure of how two random variables change together. It underpins correlation, portfolio variance in finance, principal component analysis, and nearly all of multivariate statistics. Unlike correlation, covariance retains the original scale of the variables, making it essential when absolute magnitudes matter but less suitable for comparing relationships across different measurement units.

!!! tip "Mental Model"
    Covariance is the "raw" version of correlation -- it tells you whether two variables move together and by how much in their original units. Dividing by both standard deviations normalizes this to the $[-1, 1]$ scale of correlation, but covariance itself is what appears in portfolio variance formulas and PCA because the actual magnitudes matter there.

## Definition

The **covariance** of two random variables $X$ and $Y$ with means $\mu_X$ and $\mu_Y$ is

$$
\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - \mu_X \mu_Y
$$

A positive covariance indicates that $X$ and $Y$ tend to increase together, while a negative covariance indicates that one tends to increase as the other decreases.

Given a sample of $n$ paired observations $(x_1, y_1), \ldots, (x_n, y_n)$, the **sample covariance** is

$$
s_{XY} = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})
$$

The denominator $n-1$ (Bessel's correction) yields an unbiased estimator of the population covariance.

## Properties

Covariance satisfies several important algebraic properties:

- **Symmetry**: $\text{Cov}(X, Y) = \text{Cov}(Y, X)$
- **Variance as self-covariance**: $\text{Cov}(X, X) = \text{Var}(X)$
- **Bilinearity**: $\text{Cov}(aX + b, \, cY + d) = ac \, \text{Cov}(X, Y)$ for constants $a, b, c, d$
- **Variance of sums**: $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y)$
- **Independence implies zero covariance**: If $X$ and $Y$ are independent, then $\text{Cov}(X, Y) = 0$ (the converse is not true in general)

!!! warning "Zero Covariance Does Not Imply Independence"
    Two variables can have $\text{Cov}(X, Y) = 0$ yet be strongly dependent. For example, if $X \sim \text{Uniform}(-1, 1)$ and $Y = X^2$, then $\text{Cov}(X, Y) = 0$ despite $Y$ being a deterministic function of $X$. Covariance detects only linear dependence.

## Covariance Matrix

For a random vector $\mathbf{X} = (X_1, X_2, \ldots, X_p)^T$, the **covariance matrix** $\Sigma$ is the $p \times p$ matrix with entries

$$
\Sigma_{ij} = \text{Cov}(X_i, X_j)
$$

The diagonal entries $\Sigma_{ii} = \text{Var}(X_i)$ are the variances, and the off-diagonal entries are the pairwise covariances. The covariance matrix is always **symmetric** and **positive semi-definite**.

```python
import numpy as np

# Generate three correlated variables
np.random.seed(42)
n = 500
x1 = np.random.normal(0, 1, n)
x2 = 0.6 * x1 + np.random.normal(0, 0.8, n)
x3 = -0.3 * x1 + 0.5 * x2 + np.random.normal(0, 0.7, n)
data = np.column_stack([x1, x2, x3])

# Compute the sample covariance matrix
cov_matrix = np.cov(data, rowvar=False)
print("Covariance matrix:")
print(np.round(cov_matrix, 4))
```

The function `np.cov` computes the sample covariance matrix using $n - 1$ in the denominator by default. The parameter `rowvar=False` indicates that each column is a variable and each row is an observation.

## Relationship to Correlation

Covariance and correlation are related through standardization. The Pearson correlation is obtained by dividing the covariance by the product of the standard deviations:

$$
\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \, \sigma_Y}
$$

Equivalently, the **correlation matrix** $R$ is obtained from the covariance matrix by

$$
R_{ij} = \frac{\Sigma_{ij}}{\sqrt{\Sigma_{ii} \, \Sigma_{jj}}}
$$

```python
from scipy import stats

# Compute pairwise covariance and correlation for two variables
cov_xy = np.cov(data[:, 0], data[:, 1])[0, 1]
r, p_value = stats.pearsonr(data[:, 0], data[:, 1])
print(f"Covariance:  {cov_xy:.4f}")
print(f"Correlation: {r:.4f}")

# Full correlation matrix from covariance matrix
std_devs = np.sqrt(np.diag(cov_matrix))
corr_matrix = cov_matrix / np.outer(std_devs, std_devs)
print("\nCorrelation matrix:")
print(np.round(corr_matrix, 4))
```

## Summary

Covariance measures the joint variability of two random variables in their original scale, with positive values indicating co-movement and negative values indicating inverse movement. The covariance matrix generalizes this to $p$ variables, encoding all pairwise covariances in a symmetric positive semi-definite matrix. Because covariance is scale-dependent, standardizing by the standard deviations yields the Pearson correlation, which is bounded to $[-1, 1]$ and more suitable for comparing relationships across different units.

---

## Exercises

**Exercise 1.**
Generate 200 samples from a bivariate normal with $\mu = [0, 0]$ and $\Sigma = \begin{pmatrix} 4 & 3 \\ 3 & 9 \end{pmatrix}$. Compute the sample covariance matrix using `np.cov()` and verify it is close to $\Sigma$.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        cov_true = [[4, 3], [3, 9]]
        data = stats.multivariate_normal.rvs(mean=[0, 0], cov=cov_true, size=200)
        sample_cov = np.cov(data, rowvar=False)
        print("Sample covariance:")
        print(np.round(sample_cov, 2))

---

**Exercise 2.**
Compute the covariance and correlation between $X$ and $Y$ for 100 samples where $Y = 2X + \varepsilon$, $X \sim N(0, 1)$, and $\varepsilon \sim N(0, 0.5^2)$. Verify that $r = \text{Cov}(X,Y) / (s_X s_Y)$.

??? success "Solution to Exercise 2"

        import numpy as np

        np.random.seed(42)
        x = np.random.normal(0, 1, 100)
        eps = np.random.normal(0, 0.5, 100)
        y = 2 * x + eps

        cov_xy = np.cov(x, y)[0, 1]
        r = cov_xy / (np.std(x, ddof=1) * np.std(y, ddof=1))
        r_check = np.corrcoef(x, y)[0, 1]
        print(f"Cov(X,Y): {cov_xy:.4f}")
        print(f"r (manual): {r:.4f}, r (corrcoef): {r_check:.4f}")

---

**Exercise 3.**
Show that covariance depends on scale: compute $\text{Cov}(X, Y)$ and $\text{Cov}(10X, Y)$ for 200 standard normal pairs with correlation 0.6. Verify that multiplying $X$ by 10 multiplies the covariance by 10 while the correlation remains unchanged.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.multivariate_normal.rvs(mean=[0,0], cov=[[1,0.6],[0.6,1]], size=200)
        x, y = data[:, 0], data[:, 1]

        cov1 = np.cov(x, y)[0, 1]
        cov2 = np.cov(10*x, y)[0, 1]
        r1 = np.corrcoef(x, y)[0, 1]
        r2 = np.corrcoef(10*x, y)[0, 1]

        print(f"Cov(X,Y):    {cov1:.4f}, Cov(10X,Y): {cov2:.4f}, ratio: {cov2/cov1:.1f}")
        print(f"Corr(X,Y):   {r1:.4f}, Corr(10X,Y): {r2:.4f}")
