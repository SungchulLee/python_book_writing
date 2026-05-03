# Multivariate Normal

The multivariate normal (Gaussian) distribution extends the univariate normal distribution to multiple correlated dimensions. It is the foundation of modern portfolio theory, multivariate statistical analysis, and Gaussian process models. Understanding its properties is essential because many results in statistics and finance — from mean-variance optimization to principal component analysis — rely on the assumption of joint normality.

!!! tip "Mental Model"
    A multivariate normal is fully described by its mean vector (where the cloud of points is centered) and its covariance matrix (the shape, size, and orientation of the ellipsoidal cloud). Every marginal and every conditional distribution is also normal, and uncorrelated components are genuinely independent -- properties that make multivariate normals uniquely tractable.

---

## Mathematical Definition

A random vector $\mathbf{X} = (X_1, X_2, \ldots, X_p)^T$ follows a $p$-dimensional multivariate normal distribution, written $\mathbf{X} \sim N_p(\boldsymbol{\mu}, \boldsymbol{\Sigma})$, if its probability density function is:

$$
f(\mathbf{x}) = \frac{1}{(2\pi)^{p/2}\,|\boldsymbol{\Sigma}|^{1/2}} \exp\!\left(-\frac{1}{2}(\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})\right)
$$

where:

- $\boldsymbol{\mu} \in \mathbb{R}^p$ is the **mean vector**
- $\boldsymbol{\Sigma} \in \mathbb{R}^{p \times p}$ is the **covariance matrix**, which must be symmetric and positive definite
- $|\boldsymbol{\Sigma}|$ denotes the determinant of $\boldsymbol{\Sigma}$

The exponent $(\mathbf{x} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1} (\mathbf{x} - \boldsymbol{\mu})$ is the squared **Mahalanobis distance** from $\mathbf{x}$ to the mean $\boldsymbol{\mu}$.

## Usage in scipy.stats

The `scipy.stats.multivariate_normal` distribution takes `mean` and `cov` as parameters:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mean = [1.0, 2.0]
cov = [[1.0, 0.6],
       [0.6, 1.0]]

rv = stats.multivariate_normal(mean=mean, cov=cov)

# Evaluate PDF at a point
print(f"PDF at mean: {rv.pdf(mean):.6f}")

# Generate random samples
samples = rv.rvs(size=1000, random_state=42)
print(f"Sample mean: {samples.mean(axis=0)}")
print(f"Sample cov:\n{np.cov(samples.T)}")
```

## Visualizing the Bivariate Case

The bivariate normal ($p = 2$) can be visualized using contour plots, where each contour represents a level set of constant density:

```python
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt

mean = [0, 0]
cov = [[1.0, 0.7],
       [0.7, 1.0]]

rv = stats.multivariate_normal(mean=mean, cov=cov)

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
pos = np.dstack((X, Y))
Z = rv.pdf(pos)

plt.contourf(X, Y, Z, levels=20, cmap='Blues')
plt.colorbar(label='Density')
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.title('Bivariate Normal Density (ρ=0.7)')
plt.axis('equal')
plt.show()
```

The elliptical contours are tilted in the direction of positive correlation. When $\rho = 0$, the contours are axis-aligned circles (for equal variances) or ellipses.

## Key Properties

The multivariate normal distribution has several fundamental properties:

- **Marginals are normal**: Each component $X_i$ is marginally $N(\mu_i, \Sigma_{ii})$
- **Conditionals are normal**: The conditional distribution of any subset of components given the others is also multivariate normal
- **Affine transformation**: If $\mathbf{X} \sim N_p(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ and $\mathbf{Y} = A\mathbf{X} + \mathbf{b}$, then $\mathbf{Y} \sim N_q(A\boldsymbol{\mu} + \mathbf{b},\; A\boldsymbol{\Sigma}A^T)$
- **Uncorrelated implies independent**: For jointly normal random variables, zero covariance implies independence (this is not true in general)
- **Mahalanobis distance**: $(\mathbf{X} - \boldsymbol{\mu})^T \boldsymbol{\Sigma}^{-1}(\mathbf{X} - \boldsymbol{\mu}) \sim \chi^2(p)$

## Parameters in scipy.stats

| Parameter | Symbol | `scipy.stats` keyword | Type |
|-----------|--------|-----------------------|------|
| Mean vector | $\boldsymbol{\mu}$ | `mean` | array of length $p$ |
| Covariance matrix | $\boldsymbol{\Sigma}$ | `cov` | $p \times p$ positive definite matrix |

## Financial Applications

The multivariate normal distribution is pervasive in quantitative finance. Markowitz mean-variance portfolio optimization assumes asset returns are jointly normal, using $\boldsymbol{\mu}$ for expected returns and $\boldsymbol{\Sigma}$ for the covariance structure. Risk measures such as portfolio Value at Risk rely on the multivariate normal assumption. Factor models (CAPM, Fama-French) assume normal residuals across assets. Copula models often use the multivariate normal copula to model dependence structures.

## Summary

The multivariate normal distribution generalizes the univariate normal to $p$ dimensions via a mean vector and a covariance matrix. In `scipy.stats`, use `stats.multivariate_normal(mean, cov)` to create a frozen distribution for computing densities, generating samples, and evaluating log-likelihoods.

---

## Exercises

**Exercise 1.**
Create a bivariate normal distribution with $\boldsymbol{\mu} = [0, 0]$ and covariance matrix $\Sigma = \begin{pmatrix} 1 & 0.7 \\ 0.7 & 1 \end{pmatrix}$. Generate 1000 samples and compute the sample correlation coefficient. Verify it is close to 0.7.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import stats

        mu = [0, 0]
        cov = [[1, 0.7], [0.7, 1]]
        rv = stats.multivariate_normal(mean=mu, cov=cov)
        samples = rv.rvs(size=1000, random_state=42)
        r = np.corrcoef(samples[:, 0], samples[:, 1])[0, 1]
        print(f"Sample correlation: {r:.4f} (expected ~0.7)")

---

**Exercise 2.**
For the same bivariate normal, evaluate the PDF at the point $(1, 1)$ using `stats.multivariate_normal.pdf()`. Compare with the PDF at the mean $(0, 0)$.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        mu = [0, 0]
        cov = [[1, 0.7], [0.7, 1]]
        rv = stats.multivariate_normal(mean=mu, cov=cov)
        print(f"PDF at (1,1): {rv.pdf([1, 1]):.6f}")
        print(f"PDF at (0,0): {rv.pdf([0, 0]):.6f}")

---

**Exercise 3.**
Generate 5000 samples from a 3-dimensional multivariate normal with identity covariance. Compute the sample covariance matrix using `np.cov()` and verify it is close to the identity matrix.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy import stats

        rv = stats.multivariate_normal(mean=[0, 0, 0], cov=np.eye(3))
        samples = rv.rvs(size=5000, random_state=42)
        sample_cov = np.cov(samples, rowvar=False)
        print("Sample covariance matrix:")
        print(np.round(sample_cov, 3))
