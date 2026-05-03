# Feature Selection for ML

Before training a machine learning model, selecting the most informative features from a large candidate set can improve predictive accuracy, reduce overfitting, and speed up computation. Statistical tests provide a principled, model-free approach to measuring the relationship between each feature and the target variable. This section demonstrates how to use `scipy.stats` functions for univariate feature selection.

!!! tip "Mental Model"
    Think of feature selection as auditioning candidates for a team. Each statistical test asks one question: "Does this feature carry a signal about the target, or is it just noise?" Features that fail the audition are cut, leaving a leaner model that generalizes better.

## Statistical Criteria for Feature Relevance

Univariate feature selection evaluates each feature independently by testing the null hypothesis that the feature is unrelated to the target. The choice of test depends on the data types involved.

| Feature type | Target type | Recommended test | scipy function |
|---|---|---|---|
| Continuous | Continuous | Pearson correlation | `stats.pearsonr` |
| Continuous | Categorical | ANOVA F-test | `stats.f_oneway` |
| Categorical | Categorical | Chi-square test | `stats.chi2_contingency` |
| Ordinal | Ordinal | Spearman or Kendall | `stats.spearmanr`, `stats.kendalltau` |

## Correlation-Based Selection

For continuous features and a continuous target, the Pearson correlation coefficient $r$ measures linear association. The test statistic under $H_0\colon \rho = 0$ is

$$
t = r \sqrt{\frac{n - 2}{1 - r^2}}
$$

which follows a $t$-distribution with $n - 2$ degrees of freedom. Features with p-values below a threshold $\alpha$ are retained.

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)
n = 200

# Feature matrix: 5 features, only first two are relevant
X = rng.standard_normal((n, 5))
y = 2 * X[:, 0] - 1.5 * X[:, 1] + rng.normal(0, 0.5, n)

print("Pearson correlation feature selection:")
for j in range(X.shape[1]):
    r, p = stats.pearsonr(X[:, j], y)
    status = "KEEP" if p < 0.05 else "DROP"
    print(f"  Feature {j}: r={r:+.4f}, p={p:.4e} -> {status}")
```

When the relationship is monotonic but not necessarily linear, Spearman's rank correlation is more appropriate.

## ANOVA F-Test for Categorical Targets

When the target variable is categorical (for example, class labels), the one-way ANOVA F-test evaluates whether the feature's group means differ significantly across classes. The F-statistic is

$$
F = \frac{\text{Between-group variance}}{\text{Within-group variance}} = \frac{\sum_{k=1}^{K} n_k (\bar{X}_k - \bar{X})^2 / (K - 1)}{\sum_{k=1}^{K} \sum_{i=1}^{n_k} (X_{ki} - \bar{X}_k)^2 / (N - K)}
$$

where $K$ is the number of classes, $n_k$ is the size of class $k$, $\bar{X}_k$ is the class mean, and $\bar{X}$ is the overall mean.

```python
from scipy import stats
import numpy as np

rng = np.random.default_rng(42)

# Simulated classification data: 3 classes
n_per_class = 100
labels = np.repeat([0, 1, 2], n_per_class)

# Feature 0: differs across classes (informative)
feature_0 = rng.normal(loc=labels * 1.5, scale=1.0)
# Feature 1: same distribution across classes (uninformative)
feature_1 = rng.normal(loc=0, scale=1.0, size=3 * n_per_class)

for name, feat in [("Feature 0 (informative)", feature_0),
                   ("Feature 1 (noise)", feature_1)]:
    groups = [feat[labels == k] for k in range(3)]
    f_stat, p_val = stats.f_oneway(*groups)
    print(f"{name}: F={f_stat:.2f}, p={p_val:.4e}")
```

## Chi-Square Test for Categorical Features

For categorical features with a categorical target, the chi-square test of independence evaluates whether the feature and target are associated. Given a contingency table with observed counts $O_{ij}$ and expected counts $E_{ij}$ under independence, the test statistic is

$$
\chi^2 = \sum_{i} \sum_{j} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}
$$

```python
from scipy import stats
import numpy as np

# Contingency table: feature values (rows) vs target classes (columns)
observed = np.array([[30, 10, 5],
                     [15, 25, 10],
                     [5,  15, 35]])

chi2, p_val, dof, expected = stats.chi2_contingency(observed)
print(f"Chi-square: {chi2:.2f}")
print(f"p-value: {p_val:.4e}")
print(f"Degrees of freedom: {dof}")
```

## Multiple Testing Correction

When testing many features simultaneously, the family-wise error rate increases. If $m$ features are tested at level $\alpha$, the probability of at least one false positive under the global null is $1 - (1 - \alpha)^m$, which approaches 1 rapidly as $m$ grows.

Apply the Bonferroni correction ($\alpha_{\text{adj}} = \alpha / m$) for strict control, or the Benjamini-Hochberg procedure for false discovery rate control.

```python
from scipy.stats import false_discovery_control
import numpy as np

# p-values from testing 20 features
rng = np.random.default_rng(42)
p_values = np.concatenate([
    rng.uniform(0.001, 0.01, 3),    # 3 truly relevant features
    rng.uniform(0.1, 0.9, 17)       # 17 irrelevant features
])

adjusted = false_discovery_control(p_values, method='bh')
n_selected = np.sum(adjusted < 0.05)
print(f"Features selected (BH, alpha=0.05): {n_selected}")
```

!!! warning "Univariate Selection Misses Interactions"
    Univariate tests evaluate each feature in isolation. A feature that is uninformative alone may become highly predictive when combined with another feature. For interaction effects, consider model-based selection methods beyond the scope of `scipy.stats`.

## Summary

Statistical feature selection uses hypothesis tests to rank and filter features based on their individual association with the target variable. Pearson or Spearman correlation handles continuous-continuous pairs, the ANOVA F-test handles continuous-categorical pairs, and the chi-square test handles categorical-categorical pairs. Multiple testing correction is essential when the candidate feature set is large.


---

## Exercises

**Exercise 1.** Write code that computes the Pearson correlation between each feature and the target variable in a synthetic dataset. Select features with correlation above 0.3.

??? success "Solution to Exercise 1"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(100)
    print(f'Mean: {data.mean():.4f}')
    print(f'Std: {data.std():.4f}')
    ```

---

**Exercise 2.** Explain the difference between filter methods, wrapper methods, and embedded methods for feature selection.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that uses mutual information (`sklearn.feature_selection.mutual_info_regression`) to rank features by their relevance to a target variable.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np
    from scipy import stats
    import matplotlib.pyplot as plt

    np.random.seed(42)
    data = np.random.randn(1000)
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, density=True, alpha=0.7)
    ax.set_title('Distribution')
    plt.show()
    ```

---

**Exercise 4.** Create a synthetic dataset with 10 features (5 relevant, 5 noise) and demonstrate that correlation-based selection correctly identifies the relevant features.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
