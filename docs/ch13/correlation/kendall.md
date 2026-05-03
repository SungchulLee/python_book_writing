# Kendall's Tau

While Pearson and Spearman correlation measure linear and monotonic association respectively, Kendall's Tau offers a different perspective: it measures association in terms of the probability that two randomly chosen observations are concordant. This pairwise comparison approach produces a statistic with attractive theoretical properties, including more reliable p-values for small samples and a natural probabilistic interpretation.

!!! tip "Mental Model"
    Pick any two data points at random. If both variables increase together (or both decrease), the pair is concordant; otherwise it is discordant. Kendall's Tau is simply the fraction of concordant pairs minus the fraction of discordant pairs -- a direct vote on whether the relationship is monotone.

## Concordant and Discordant Pairs

Given $n$ paired observations $(x_1, y_1), \ldots, (x_n, y_n)$, consider any pair of observations $(x_i, y_i)$ and $(x_j, y_j)$ with $i < j$:

- The pair is **concordant** if $(x_i - x_j)$ and $(y_i - y_j)$ have the same sign, meaning both variables move in the same direction
- The pair is **discordant** if $(x_i - x_j)$ and $(y_i - y_j)$ have opposite signs
- The pair is **tied** if $x_i = x_j$ or $y_i = y_j$

There are $\binom{n}{2} = \frac{n(n-1)}{2}$ total pairs.

## Tau-a

The simplest form, **Kendall's Tau-a**, is defined as

$$
\tau_a = \frac{C - D}{\binom{n}{2}}
$$

where $C$ is the number of concordant pairs and $D$ is the number of discordant pairs. Tau-a does not adjust for ties, so it can fail to reach $\pm 1$ even for perfectly monotonic data when ties are present.

## Tau-b

**Kendall's Tau-b** adjusts for ties and is defined as

$$
\tau_b = \frac{C - D}{\sqrt{(n_0 - n_1)(n_0 - n_2)}}
$$

where:

- $n_0 = \binom{n}{2}$ is the total number of pairs
- $n_1 = \sum_k \binom{t_k}{2}$ counts tied pairs in $X$ (with $t_k$ the size of the $k$-th group of ties)
- $n_2 = \sum_l \binom{u_l}{2}$ counts tied pairs in $Y$ (with $u_l$ the size of the $l$-th group of ties)

When there are no ties, Tau-b reduces to Tau-a.

!!! note "SciPy Default"
    The function `scipy.stats.kendalltau` computes Tau-b by default. This is the appropriate choice for most practical applications, since real data frequently contains ties.

## Properties

Kendall's Tau shares some properties with other correlation measures while having distinctive characteristics:

- **Range**: $-1 \leq \tau \leq 1$, with $\tau = 1$ indicating perfect concordance (all pairs agree) and $\tau = -1$ indicating perfect discordance
- **Probabilistic interpretation**: $\tau = P(\text{concordant}) - P(\text{discordant})$ for a randomly chosen pair
- **Relationship to Spearman**: In general $|\tau| \leq |r_s|$, so Kendall values are typically smaller in magnitude than Spearman values for the same data
- **Symmetry**: $\tau(X, Y) = \tau(Y, X)$

## Computing Kendall's Tau with SciPy

```python
import numpy as np
from scipy import stats

# Generate monotonically related data with some noise
np.random.seed(42)
n = 100
x = np.random.uniform(0, 10, n)
y = 2 * x + np.random.normal(0, 2, n)

# Compute Kendall's Tau-b
tau, p_value = stats.kendalltau(x, y)
print(f"Kendall tau-b = {tau:.4f}, p-value = {p_value:.2e}")

# Compare with Spearman
rho, _ = stats.spearmanr(x, y)
print(f"Spearman rho  = {rho:.4f}")
print(f"|tau| <= |rho|: {abs(tau) <= abs(rho)}")
```

The p-value tests the null hypothesis $H_0\!: \tau = 0$ (no association) against the two-sided alternative.

!!! tip "When to Prefer Kendall's Tau"
    Kendall's Tau is preferred over Spearman in several situations: (1) small sample sizes, where its p-values are more reliable; (2) when a probabilistic interpretation is desired; and (3) when working with ordinal data that contains many ties, since Tau-b handles ties explicitly.

## Summary

Kendall's Tau measures association by counting concordant and discordant pairs among all observation pairs. Tau-a uses the simple proportion, while Tau-b adjusts for ties in the denominator. The statistic ranges from $-1$ to $1$, has a direct probabilistic interpretation, and is available through `scipy.stats.kendalltau`, which computes Tau-b by default.

---

## Exercises

**Exercise 1.**
For the paired data $X = [1, 2, 3, 4, 5]$ and $Y = [2, 4, 1, 3, 5]$, compute Kendall's tau-b by hand (counting concordant and discordant pairs), then verify with `stats.kendalltau()`.

??? success "Solution to Exercise 1"

        from scipy import stats

        x = [1, 2, 3, 4, 5]
        y = [2, 4, 1, 3, 5]

        # Manual: count concordant/discordant pairs
        n = len(x)
        concordant = discordant = 0
        for i in range(n):
            for j in range(i+1, n):
                if (x[j]-x[i])*(y[j]-y[i]) > 0:
                    concordant += 1
                elif (x[j]-x[i])*(y[j]-y[i]) < 0:
                    discordant += 1
        tau_manual = (concordant - discordant) / (concordant + discordant)

        tau_scipy, p = stats.kendalltau(x, y)
        print(f"Manual tau: {tau_manual:.4f}")
        print(f"SciPy tau:  {tau_scipy:.4f}")

---

**Exercise 2.**
Generate 100 samples from a bivariate normal with $\rho = 0.6$. Compute Pearson, Spearman, and Kendall correlations and compare their magnitudes. Note the typical ordering $|r| > |\rho_s| > |\tau|$.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import stats

        np.random.seed(42)
        data = stats.multivariate_normal.rvs(mean=[0,0], cov=[[1,0.6],[0.6,1]], size=100)
        x, y = data[:, 0], data[:, 1]

        r, _ = stats.pearsonr(x, y)
        rho, _ = stats.spearmanr(x, y)
        tau, _ = stats.kendalltau(x, y)
        print(f"Pearson:  {r:.4f}")
        print(f"Spearman: {rho:.4f}")
        print(f"Kendall:  {tau:.4f}")

---

**Exercise 3.**
Create ranked data with many ties: $X = [1, 1, 2, 2, 3, 3, 4, 4]$, $Y = [1, 2, 1, 2, 3, 4, 3, 4]$. Compute Kendall's tau-b and verify it handles ties correctly.

??? success "Solution to Exercise 3"

        from scipy import stats

        x = [1, 1, 2, 2, 3, 3, 4, 4]
        y = [1, 2, 1, 2, 3, 4, 3, 4]
        tau, p = stats.kendalltau(x, y)
        print(f"Kendall tau-b (with ties): {tau:.4f}, p={p:.4f}")
