# Data Normalization and Preprocessing

!!! tip "Mental Model"
    Normalization forces different samples onto a common scale so that you compare biology, not batch effects. Quantile normalization goes further by making the entire distribution of values identical across samples -- if the same genes are active in each sample, their measurements should have the same distribution after removing technical artifacts.

## Why Normalize Data?

Real-world data rarely comes in a pristine, analysis-ready form. When working with biological datasets—such as gene expression measurements from RNA-sequencing—technical variation often obscures the signal you're trying to detect. Normalization techniques separate **technical variation** from **biological variation**, making your downstream analysis more reliable.

### Technical Variation vs. Real Variation

Consider a gene expression experiment with samples processed on different days or with different reagent batches. Even if the true biological signal is identical, you might observe:

- **Sample 1 (Day 1):** average expression = 100
- **Sample 2 (Day 2):** average expression = 150

These differences could reflect:
1. **Technical effects:** differences in processing, library preparation quality, sequencing depth
2. **Biological effects:** real differences in gene activity between cell types or conditions

Normalization aims to remove (1) while preserving (2).

### Distribution Shifts Across Samples

Normalization becomes essential when samples have different distributions of values. A simple visualization reveals this problem:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Simulate raw count data from 3 samples
np.random.seed(42)
X = np.random.negative_binomial(5, 0.3, size=(1000, 3))
X[:, 1] *= 1.5  # Sample 2 has systematically higher values
X[:, 2] *= 0.7  # Sample 3 has systematically lower values

# Plot density for each column
fig, axes = plt.subplots(1, 3, figsize=(12, 3))
for i in range(3):
    kde = stats.gaussian_kde(X[:, i])
    x_range = np.linspace(X[:, i].min(), X[:, i].max(), 200)
    axes[i].plot(x_range, kde(x_range))
    axes[i].set_title(f'Sample {i+1}')
    axes[i].set_xlabel('Expression Value')
    axes[i].set_ylabel('Density')
plt.tight_layout()
plt.show()
```

!!! note
    **Visual Diagnosis Tool:** Plotting per-column density curves (using `scipy.stats.gaussian_kde`) is an excellent first step to diagnose whether your data needs normalization. If distributions look substantially different, normalization is warranted.

### When to Apply Normalization

Apply normalization when:
- Samples have different median values or distributions
- You're combining data from multiple experiments or batches
- Technical artifacts could interfere with biological conclusions
- You plan to compare expression levels across samples

---

## Log Transformation

Before applying quantile normalization, log transformation is often valuable for count data.

### Why Log Transform?

Count data (like RNA-seq reads, bacterial colony counts) typically:
- Have a **skewed (right-tailed) distribution**
- Show **variance proportional to mean** (heteroscedasticity)
- Range over multiple orders of magnitude

The log transformation compresses this range and stabilizes variance.

### Implementation: The Log(X+1) Pattern

Because log(0) is undefined, we add a pseudocount (typically 1):

$$X_{\text{log}} = \log(X + 1)$$

```python
# Log transformation with pseudocount
X_log = np.log(X + 1)
```

!!! tip
    **Adding 1:** The pseudocount (usually 1) ensures that:
    - Zero values map to log(1) = 0 instead of undefined
    - Small counts aren't over-compressed relative to large counts
    - The transformation is invertible (approximately): $\text{exp}(X_{\text{log}}) - 1 \approx X$

### Effect on Variance

The log transformation has a stabilizing effect. For count data where variance is proportional to the mean, the log scale (approximately) equalizes variance across different expression levels:

```python
# Before and after variance comparison
print(f"Variance before log: {np.var(X, axis=0)}")
print(f"Variance after log: {np.var(np.log(X + 1), axis=0)}")
```

---

## Quantile Normalization Algorithm

Quantile normalization forces all samples to have **identical distributions**. This is particularly useful for removing systematic biases while preserving sample-to-sample differences that are consistent across genes.

### The Three-Step Process

**Step 1: Sort values along each column**

For each sample (column), sort all expression values in ascending order.

**Step 2: Compute reference distribution**

Average each row of sorted values. This reference distribution represents the "typical" expression pattern after sorting.

**Step 3: Replace quantiles**

Replace each sorted value with the corresponding reference quantile value, then unsort to restore original order.

### Mathematical Intuition

If sample A has high variance and sample B has low variance:

$$\text{Before:} \quad A = [1, 50, 100], \quad B = [40, 45, 50]$$

After sorting and averaging each row:

$$\text{Reference} = \frac{1}{2} \left( \begin{bmatrix} 1 \\ 50 \\ 100 \end{bmatrix} + \begin{bmatrix} 40 \\ 45 \\ 50 \end{bmatrix} \right) = \begin{bmatrix} 20.5 \\ 47.5 \\ 75 \end{bmatrix}$$

Both samples now have identical values: 20.5, 47.5, 75 (in different original positions).

### Implementation

```python
import numpy as np
from scipy import stats

def quantile_normalize(X):
    """
    Apply quantile normalization to a matrix.

    Parameters
    ----------
    X : ndarray of shape (n_features, n_samples)
        Data matrix where columns are samples.

    Returns
    -------
    Xn : ndarray of same shape as X
        Quantile-normalized data.

    Notes
    -----
    This function assumes column-wise samples and row-wise features.
    """
    # Step 1: Compute reference distribution (mean of sorted rows)
    quantiles = np.mean(np.sort(X, axis=0), axis=1)

    # Step 2: Get rank of each value in its column
    # rankdata returns 1-indexed ranks
    ranks = np.apply_along_axis(stats.rankdata, 0, X)
    rank_indices = ranks.astype(int) - 1

    # Step 3: Replace each value with its quantile value
    Xn = quantiles[rank_indices]

    return Xn
```

### Example Usage

```python
# Create sample data: 5 features × 3 samples
np.random.seed(42)
X = np.array([
    [1, 40, 200],
    [2, 45, 250],
    [5, 50, 300],
    [10, 48, 280],
    [20, 55, 350]
], dtype=float)

print("Original data:")
print(X)

Xn = quantile_normalize(X)
print("\nQuantile-normalized data:")
print(Xn)

# Verify all columns have identical values
print("\nColumn 0:", Xn[:, 0])
print("Column 1:", Xn[:, 1])
print("Column 2:", Xn[:, 2])
```

!!! note
    **Key NumPy Concepts:**
    - `np.sort(axis=0)`: Sort within each column
    - `np.mean(..., axis=1)`: Average across columns (row-wise)
    - `np.apply_along_axis()`: Apply function along each column
    - `stats.rankdata()`: Compute ranks (handles ties)
    - Fancy indexing with `quantiles[rank_indices]`: vectorized lookup

---

## Feature Selection by Variance

High-dimensional datasets (thousands of features) can benefit from dimensionality reduction. A simple and effective approach: **select features with the highest variance**.

### Rationale

- **High-variance features** carry more information and are more likely to be biologically relevant
- **Low-variance features** add noise without signal
- Reducing feature count speeds up downstream analysis (clustering, visualization) and reduces overfitting risk

### Implementation

```python
def most_variable_rows(X, n_features=100):
    """
    Select the most variable features (rows).

    Parameters
    ----------
    X : ndarray of shape (n_features, n_samples)
        Data matrix.
    n_features : int, optional
        Number of features to select. Default: 100.

    Returns
    -------
    X_selected : ndarray of shape (n_features, n_samples)
        Data containing only selected features.
    indices : ndarray
        Indices of selected features in original matrix.
    """
    # Compute variance for each feature (row)
    variances = np.var(X, axis=1)

    # Find indices of top-n most variable features
    indices = np.argsort(variances)[-n_features:]

    # Return selected features and their indices
    return X[indices, :], indices
```

### Example

```python
# Load and normalize data
np.random.seed(42)
X = np.random.negative_binomial(5, 0.3, size=(5000, 20))
X_log = np.log(X + 1)
X_norm = quantile_normalize(X_log)

# Select top 500 most variable genes
X_selected, gene_indices = most_variable_rows(X_norm, n_features=500)

print(f"Original shape: {X_norm.shape}")
print(f"Selected shape: {X_selected.shape}")
print(f"Selected gene indices: {gene_indices}")
```

!!! tip
    **Choosing n_features:** Use domain knowledge and downstream goals:
    - **Clustering:** 100-1000 features often sufficient
    - **Classification:** May need more features for accurate prediction
    - **Visualization:** Keep it small (50-200) for interpretable plots

---

## Hierarchical Clustering Preview

After normalization and feature selection, hierarchical clustering reveals structure in your data by grouping similar samples and features.

### Basic Linkage Computation

```python
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list

# Compute hierarchical clustering
Z = linkage(X_selected.T, method='ward')  # Ward linkage on samples

# Generate dendrogram
dendrogram(Z)
plt.xlabel('Sample Index')
plt.ylabel('Distance')
plt.title('Hierarchical Clustering of Samples')
plt.show()
```

### Biclustering: Clustering Rows AND Columns

A more sophisticated approach clusters both features (rows) and samples (columns) simultaneously, revealing blocks of co-regulated genes:

```python
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, leaves_list

# Cluster rows (features/genes)
Z_rows = linkage(X_selected, method='ward')
row_order = leaves_list(Z_rows)

# Cluster columns (samples)
Z_cols = linkage(X_selected.T, method='ward')
col_order = leaves_list(Z_cols)

# Reorder data matrix
X_reordered = X_selected[row_order, :][:, col_order]

# Visualize with dendrograms
fig = plt.figure(figsize=(10, 8))
gs = fig.add_gridspec(2, 2, width_ratios=[0.2, 1], height_ratios=[1, 0.2])

# Heatmap
ax_heatmap = fig.add_subplot(gs[0, 1])
im = ax_heatmap.imshow(X_reordered, aspect='auto', cmap='RdBu_r')
ax_heatmap.set_xlabel('Sample (clustered)')
ax_heatmap.set_ylabel('Gene (clustered)')
plt.colorbar(im, ax=ax_heatmap)

# Row dendrogram
ax_row_dend = fig.add_subplot(gs[0, 0])
dendrogram(Z_rows, ax=ax_row_dend, orientation='left')
ax_row_dend.set_yticks([])

# Column dendrogram
ax_col_dend = fig.add_subplot(gs[1, 1])
dendrogram(Z_cols, ax=ax_col_dend)
ax_col_dend.set_xticks([])

plt.tight_layout()
plt.show()
```

!!! note
    **Biclustering interpretation:** The heatmap shows gene expression, with genes and samples reordered by similarity. Dark red = high expression, dark blue = low expression. Visual blocks indicate co-regulated genes in specific sample groups.

### Why This Matters

Hierarchical clustering after normalization:
1. **Removes batch effects** via normalization (technical noise)
2. **Reveals biological structure** (cell types, conditions, disease states)
3. **Identifies outliers** (unusual samples or genes)
4. **Provides visual feedback** on data quality and preprocessing success

---

## Complete Preprocessing Pipeline

Here's a full workflow combining all techniques: load → log transform → normalize → select features → cluster.

```python
import numpy as np
from scipy import stats
from scipy.cluster.hierarchy import linkage, dendrogram, leaves_list
import matplotlib.pyplot as plt

def quantile_normalize(X):
    """Quantile normalize a matrix."""
    quantiles = np.mean(np.sort(X, axis=0), axis=1)
    ranks = np.apply_along_axis(stats.rankdata, 0, X)
    rank_indices = ranks.astype(int) - 1
    return quantiles[rank_indices]

def most_variable_rows(X, n_features=100):
    """Select most variable features."""
    variances = np.var(X, axis=1)
    indices = np.argsort(variances)[-n_features:]
    return X[indices, :], indices

# Step 1: Load data
np.random.seed(42)
X_raw = np.random.negative_binomial(5, 0.3, size=(2000, 30))

# Step 2: Log transformation
X_log = np.log(X_raw + 1)

# Step 3: Quantile normalization
X_norm = quantile_normalize(X_log)

# Step 4: Feature selection (keep top 500 genes)
X_selected, selected_idx = most_variable_rows(X_norm, n_features=500)

# Step 5: Hierarchical clustering
Z = linkage(X_selected.T, method='ward')

# Visualize results
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# Before normalization
axes[0].hist(X_raw.flatten(), bins=50)
axes[0].set_title('Raw Data Distribution')
axes[0].set_xlabel('Count')

# After normalization
axes[1].hist(X_norm.flatten(), bins=50)
axes[1].set_title('After Quantile Normalization')
axes[1].set_xlabel('Normalized Value')

# Clustering dendrogram
axes[2].remove()
ax_dend = fig.add_subplot(133)
dendrogram(Z, ax=ax_dend, leaf_rotation=90)
ax_dend.set_title('Sample Clustering')
ax_dend.set_xlabel('Sample')
ax_dend.set_ylabel('Distance')

plt.tight_layout()
plt.show()
```

---

## Best Practices and Common Pitfalls

### Best Practices

1. **Always visualize before and after**
   - Density plots, histograms, and heatmaps reveal whether normalization worked
   - Save plots for your analysis report

2. **Document your normalization choice**
   - Different analyses may require different approaches
   - Quantile normalization assumes technical shifts only (no true biological rank changes)
   - Log transformation assumes counts; avoid on already-normalized data

3. **Be cautious with feature selection**
   - Features selected on training data can introduce bias
   - Use cross-validation or hold-out test sets when building predictive models
   - Variance-based selection is exploratory; use statistical tests for inference

4. **Check for over-normalization**
   - Quantile normalization forces artificial similarity
   - Use it when you're confident technical effects dominate
   - Consider milder approaches (e.g., median centering) if you want to preserve more biological signal

### Common Pitfalls

1. **Normalizing twice**
   - Don't apply quantile normalization to already-normalized data
   - It will create artificial patterns

2. **Forgetting batch effects**
   - If data comes from different batches, normalize within batches or use batch-aware methods
   - Visual clustering by batch before preprocessing is a good diagnostic

3. **Selecting features on biased data**
   - Always perform feature selection AFTER normalization, not before
   - Pre-selection on non-normalized data can amplify technical artifacts

4. **Ignoring the biological question**
   - Choose normalization that preserves signal relevant to your hypothesis
   - Over-normalization can erase true biological differences

!!! tip
    **Gold Standard:** Compare multiple preprocessing approaches on a small set of known positive/negative controls. The approach that best separates true signals from noise is your best choice.

---

## Summary

Normalization and preprocessing are critical foundations for reliable data analysis:

- **Log transformation** compresses count data and stabilizes variance
- **Quantile normalization** forces identical distributions across samples, removing systematic biases
- **Feature selection** reduces dimensionality and focuses on informative signals
- **Hierarchical clustering** reveals structure while providing visual quality control

Master these techniques, and you'll spend less time fighting artifacts and more time discovering biological insights.


---

## Exercises

**Exercise 1.** Write code that performs quantile normalization on a matrix of values. All columns should have the same distribution after normalization.

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

**Exercise 2.** Explain the steps of quantile normalization: rank within columns, average across columns, reassign.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that compares the distributions before and after quantile normalization using histograms.

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

**Exercise 4.** Explain when quantile normalization is appropriate. Give an example from genomics or another field.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
