# Sparse Matrix Applications

Beyond linear algebra, sparse matrices unlock elegant solutions to real-world problems. This section explores practical applications where the structure and efficiency of sparse formats shine.

!!! tip "Mental Model"
    Sparse matrices are not just a storage optimization -- they are a computational paradigm. Whenever a problem involves pairwise relationships over a large set (confusion matrices, co-occurrence counts, graph Laplacians), the underlying matrix is almost always sparse. Recognizing this pattern lets you replace slow Python loops with fast vectorized sparse operations.

## Contingency Tables via COO Format

### The Problem: Counting Co-occurrences

Many machine learning and data analysis tasks require counting how often pairs of events occur together. Examples include:

- **Confusion matrices**: how often the classifier predicts class A when ground truth is B
- **Co-occurrence matrices**: how often word pairs appear together in documents
- **Cross-tabulation**: frequency counts across two categorical variables

The naive approach uses nested loops with multiple passes through the data. The elegant solution: exploit the COO format's automatic duplicate coordinate summing.

### Naive Approach

```python
import numpy as np

def confusion_matrix_naive(predictions, ground_truth):
    """Compute confusion matrix the inefficient way."""
    n_classes = max(predictions.max(), ground_truth.max()) + 1
    cm = np.zeros((n_classes, n_classes))

    # Multiple passes: slow!
    for i in range(len(predictions)):
        cm[predictions[i], ground_truth[i]] += 1

    return cm
```

This approach:
- Requires loop iteration
- Allocates dense storage (wasteful for sparse data)
- Poor cache locality

### Elegant COO Solution

```python
import numpy as np
from scipy import sparse

def confusion_matrix(predictions, ground_truth):
    """Compute confusion matrix via COO format."""
    # COO constructor automatically sums duplicate coordinates!
    cont = sparse.coo_matrix(
        (np.ones(predictions.size), (predictions, ground_truth))
    )
    return cont.toarray()

# Example
pred = np.array([0, 1, 1, 2, 2, 0])
gt = np.array([0, 1, 2, 2, 1, 0])

cm = confusion_matrix(pred, gt)
print("Confusion matrix:")
print(cm)
```

**Output:**
```
Confusion matrix:
[[2. 0. 0.]
 [0. 1. 1.]
 [0. 1. 1.]]
```

!!! note
    The COO format constructor accepts triplets `(data, (row, col))`. If multiple entries share the same `(row, col)` coordinates, they are **automatically summed**. This is the key insight: we don't need explicit loops—just provide the count of 1 for each sample.

### Memory Optimization with Virtual Arrays

For multi-class problems with millions of samples, even `np.ones(n)` wastes memory. Use `np.broadcast_to()` to create a virtual array with zero copy:

```python
import numpy as np
from scipy import sparse

def confusion_matrix_optimized(predictions, ground_truth):
    """Compute confusion matrix with minimal memory."""
    # Virtual array: same as np.ones(n) but without allocation
    ones = np.broadcast_to(1., predictions.shape)

    cont = sparse.coo_matrix(
        (ones, (predictions, ground_truth))
    )
    return cont.toarray()

# Works with large arrays efficiently
n_samples = 10_000_000
predictions = np.random.randint(0, 1000, n_samples)
ground_truth = np.random.randint(0, 1000, n_samples)

cm = confusion_matrix_optimized(predictions, ground_truth)
print(f"Confusion matrix shape: {cm.shape}")
print(f"Nonzero entries: {cm.count_nonzero()}")
```

### Scaling to Multi-class Problems

```python
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from scipy import sparse
import numpy as np

# Generate synthetic classification data
X, y = make_classification(n_samples=1000, n_features=20, n_classes=5,
                           n_informative=15, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train classifier
clf = RandomForestClassifier(n_estimators=10, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Compute confusion matrix via sparse format
n_classes = len(np.unique(y_test))
cm = sparse.coo_matrix(
    (np.ones(y_test.size), (y_pred, y_test)),
    shape=(n_classes, n_classes)
)

# Convert to dense for display
print("Confusion matrix (sparse → dense):")
print(cm.toarray().astype(int))
```

!!! tip
    **When to use this pattern**: Always use COO for constructing contingency tables from raw data. Convert to CSR only if you need repeated matrix operations afterward. The automatic summing of duplicate coordinates is COO's killer feature.

---

## Image Transformations via Sparse Operators

### The Problem: Applying Transformations at Scale

Imagine applying the same geometric transformation (rotation, scaling, warping) to millions of images. Naive per-image computation is slow because each transformation recalculates weights.

**Key insight**: The transformation operator (which pixels map to which) is sparse. Build it once, apply repeatedly via matrix multiplication.

### How Transformations Become Sparse Matrices

A geometric transformation maps input pixel coordinates to output coordinates. Each output pixel depends on only **~4 input pixels** (via bilinear interpolation):

```
Output(x, y) = w₁·Input(x₁, y₁) + w₂·Input(x₂, y₂) +
                w₃·Input(x₃, y₃) + w₄·Input(x₄, y₄)
```

This is a sparse linear operation! We can build a matrix T where:
- Each row represents one output pixel
- Each column represents one input pixel
- Entry T[i,j] = interpolation weight (0 if unrelated)

### Building a Sparse Rotation Operator

```python
import numpy as np
from scipy import sparse
from scipy.ndimage import affine_transform
import matplotlib.pyplot as plt

def build_rotation_matrix(image_shape, angle_deg):
    """Build sparse rotation operator for images."""
    h, w = image_shape
    n_pixels = h * w

    # Rotation matrix
    angle_rad = np.radians(angle_deg)
    cos_a, sin_a = np.cos(angle_rad), np.sin(angle_rad)

    # Center of image
    cy, cx = h / 2, w / 2

    # Build sparse matrix
    rows, cols, data = [], [], []

    for out_y in range(h):
        for out_x in range(w):
            # Transform output coordinates to input
            dy, dx = out_y - cy, out_x - cx
            in_y = cos_a * dy - sin_a * dx + cy
            in_x = sin_a * dy + cos_a * dx + cx

            # Bilinear interpolation: 4 neighboring pixels
            for di in range(2):
                for dj in range(2):
                    i = int(np.floor(in_y)) + di
                    j = int(np.floor(in_x)) + dj

                    if 0 <= i < h and 0 <= j < w:
                        # Interpolation weight
                        wi = 1 - abs(in_y - (int(np.floor(in_y)) + di))
                        wj = 1 - abs(in_x - (int(np.floor(in_x)) + dj))
                        w = wi * wj

                        if w > 1e-6:  # Only store nonzero
                            rows.append(out_y * w + out_x)
                            cols.append(i * w + j)
                            data.append(w)

    # Create sparse matrix
    T = sparse.coo_matrix(
        (data, (rows, cols)), shape=(n_pixels, n_pixels)
    )
    return T.tocsr()

# Create synthetic image
image = np.random.rand(32, 32)
img_flat = image.flatten()

# Build rotation operator once
T = build_rotation_matrix((32, 32), 15)  # 15 degree rotation

# Apply to many images efficiently
rotated_flat = T @ img_flat
rotated = rotated_flat.reshape(32, 32)

print(f"Rotation matrix shape: {T.shape}")
print(f"Nonzero entries: {T.nnz}")
print(f"Density: {T.nnz / (T.shape[0] * T.shape[1]) * 100:.2f}%")
```

!!! note
    For a 32×32 image (1,024 pixels), the rotation matrix has ~4,096 nonzeros (4 per output pixel) in ~1 million entries—clearly sparse! Building this once and reusing it 1,000 times saves enormous computation.

### Performance Advantage

```python
import numpy as np
from scipy import sparse
import time
from scipy.ndimage import rotate

# Setup
n_images = 100
image_shape = (128, 128)
n_pixels = image_shape[0] * image_shape[1]

# Generate test images
images = np.random.rand(n_images, *image_shape)

# Method 1: Per-image rotation (naive)
start = time.perf_counter()
rotated_naive = np.array([
    rotate(img, 15, reshape=False) for img in images
])
time_naive = time.perf_counter() - start

# Method 2: Build operator once, apply via sparse matrix-vector
# (Simplified example—production code would batch as matrix multiplication)
T = build_rotation_matrix(image_shape, 15)
start = time.perf_counter()
rotated_sparse = np.array([
    (T @ img.flatten()).reshape(image_shape) for img in images
])
time_sparse = time.perf_counter() - start

print(f"Per-image scipy.ndimage: {time_naive:.3f}s")
print(f"Sparse matrix operator:  {time_sparse:.3f}s")
print(f"Speedup: {time_naive / time_sparse:.1f}x")
```

!!! tip
    **Production use**: Libraries like `scikit-image` internally use sparse matrices for geometric transforms. The elegance is in decoupling the operator construction (expensive) from its application (cheap).

---

## Information Theory with Sparse Matrices

### Entropy from Joint Probability Matrices

**Entropy** measures the uncertainty in a probability distribution:

$$H(X) = -\sum_x p_x \log_2(p_x)$$

When X and Y are discrete random variables with joint distribution P(X=i, Y=j), we can compute conditional entropies efficiently using sparse matrices.

### Building Joint Probability Matrices

```python
import numpy as np
from scipy import sparse

def entropy(probabilities):
    """Compute entropy of a probability distribution."""
    # Remove zeros to avoid log(0)
    p = probabilities[probabilities > 0]
    return -np.sum(p * np.log2(p))

def conditional_entropy(joint_prob):
    """Compute H(Y|X) from joint probability matrix.

    joint_prob: sparse matrix where entry [i,j] = P(X=i, Y=j)
    """
    # Marginal: P(X=i) = sum over j
    if not sparse.issparse(joint_prob):
        joint_prob = sparse.csr_matrix(joint_prob)

    p_x = np.asarray(joint_prob.sum(axis=1)).flatten()  # P(X)

    # H(Y|X) = sum_x P(X=x) * H(Y|X=x)
    h_conditional = 0
    for i in range(joint_prob.shape[0]):
        p_x_i = p_x[i]
        if p_x_i > 0:
            # P(Y|X=i) = P(X=i, Y) / P(X=i)
            row = joint_prob[i].data / p_x_i
            h_conditional += p_x_i * entropy(row)

    return h_conditional

# Example: Two classification results
# cluster_labels: predicted clusters
# true_labels: ground truth
cluster_labels = np.array([0, 0, 1, 1, 2, 2, 0, 1])
true_labels = np.array([0, 0, 1, 0, 2, 2, 0, 1])

# Build joint probability matrix (contingency table)
n = len(cluster_labels)
joint_coo = sparse.coo_matrix(
    (np.ones(n) / n, (cluster_labels, true_labels))
)
joint_prob = joint_coo.tocsr()

print("Joint probability matrix:")
print(joint_prob.toarray())
print(f"\nH(Y|clusters) = {conditional_entropy(joint_prob):.3f}")
```

### Variation of Information

**Variation of Information** measures clustering quality—how much information is lost/gained when switching between two partitions:

$$VI(A, B) = H(A|B) + H(B|A)$$

Lower VI means better clustering consistency.

```python
import numpy as np
from scipy import sparse

def variation_of_information(labels1, labels2):
    """Compute VI distance between two clusterings."""
    n = len(labels1)

    # Joint probability matrix
    joint_coo = sparse.coo_matrix(
        (np.ones(n) / n, (labels1, labels2))
    )
    joint_prob = joint_coo.tocsr()

    # Marginals
    p_i = np.asarray(joint_prob.sum(axis=1)).flatten()
    p_j = np.asarray(joint_prob.sum(axis=0)).flatten()

    # H(i), H(j)
    h_i = entropy(p_i[p_i > 0])
    h_j = entropy(p_j[p_j > 0])

    # H(i|j) = H(i,j) - H(j)
    h_joint = entropy(joint_prob.data)
    h_i_given_j = h_joint - h_j
    h_j_given_i = h_joint - h_i

    vi = h_i_given_j + h_j_given_i
    return vi

# Example: comparing clustering algorithms
labels_kmeans = np.array([0, 0, 1, 1, 0, 1, 0, 1])
labels_hierarchical = np.array([0, 0, 1, 1, 0, 1, 0, 2])

vi = variation_of_information(labels_kmeans, labels_hierarchical)
print(f"Variation of Information: {vi:.3f}")
```

### Efficient Normalization with Sparse Diagonal Matrices

Computing probabilities from counts often requires dividing each row by its sum. With sparse matrices, use `sparse.diags()` to build a diagonal scaling matrix:

```python
import numpy as np
from scipy import sparse

def normalize_rows_sparse(mat):
    """Normalize sparse matrix rows to sum to 1."""
    if not sparse.issparse(mat):
        mat = sparse.csr_matrix(mat)

    # Row sums
    row_sums = np.asarray(mat.sum(axis=1)).flatten()

    # Inverse diagonal: 1/row_sum for each row
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    inv_row_sums = 1.0 / row_sums

    # D_inv @ A: multiply each row i by inv_row_sums[i]
    D_inv = sparse.diags(inv_row_sums)
    normalized = D_inv @ mat

    return normalized

# Example: normalized confusion matrix
cm = sparse.csr_matrix(np.array([
    [50, 5, 0],
    [3, 45, 2],
    [1, 2, 47]
]))

cm_normalized = normalize_rows_sparse(cm)
print("Row-normalized confusion matrix:")
print(cm_normalized.toarray())
```

!!! tip
    **Sparse linear algebra for broadcasting**: Instead of using numpy broadcasting operations (which create dense intermediates), express them as sparse matrix operations. `sparse.diags()` @ matrix is memory-efficient even for huge matrices.

---

## When to Use Sparse Applications

### Guidelines for Sparse Adoption

Use sparse matrix applications when:

| Criterion | Recommendation |
|:----------|:--------------|
| **Data sparsity** | >90% zeros |
| **Matrix size** | >1,000 × 1,000 |
| **Operation pattern** | Repeated (build once, use many times) |
| **Update frequency** | Infrequent modifications |

### Format Selection Strategy

```python
import numpy as np
from scipy import sparse

# 1. Construction: Use COO (automatic duplicate summing)
rows = np.array([0, 0, 1, 2])
cols = np.array([1, 1, 2, 0])
data = np.array([1, 2, 3, 4])
A = sparse.coo_matrix((data, (rows, cols)))

# 2. Single operation: Convert to appropriate format
#    - Row access: CSR
#    - Column access: CSC
#    - Matrix multiplication: CSR
A_csr = A.tocsr()

# 3. Computation: Use the @ operator for clean expressions
x = np.random.randn(A.shape[1])
y = A_csr @ x

# 4. Result handling: Convert back to dense only if needed
result_dense = y.toarray() if sparse.issparse(y) else y
```

### Decision Tree

```
Is matrix >90% zeros?
├─ Yes: Consider sparse
│   └─ Will you repeat operations?
│       ├─ Yes: Invest in sparse (build once, reuse)
│       └─ No: Dense might be simpler
└─ No: Use dense (overhead not justified)
```

### Anti-patterns to Avoid

```python
# WRONG: Convert to dense for every operation
A_sparse = sparse.csr_matrix(...)
for i in range(1000):
    A_dense = A_sparse.toarray()  # Memory spike!
    result = dense_computation(A_dense)

# CORRECT: Keep sparse, convert once at end
A_sparse = sparse.csr_matrix(...)
for i in range(1000):
    result = sparse_computation(A_sparse)
final_result = result.toarray()
```

---

## Summary

Sparse matrix applications excel when:

1. **Data naturally has structure** (contingency tables, co-occurrence counts)
2. **Operators are reusable** (image transforms, information metrics)
3. **Operations are algebraic** (matrix-vector products, linear combinations)

### Key Takeaways

- **COO format** for construction (automatic duplicate summing)
- **CSR format** for computation (row access, matrix multiplication)
- **Diagonal matrices** via `sparse.diags()` for scaling operations
- **@ operator** for clean, readable sparse linear algebra

The elegance of sparse matrices lies in separating construction from computation, letting you build once and apply efficiently many times.

---

## Exercises

**Exercise 1.**
Given prediction and ground truth arrays `pred = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])` and `gt = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])`, build a $3 \times 3$ confusion matrix using the COO sparse format (exploit duplicate coordinate summing). Convert to dense and print it. Compute the overall accuracy (sum of diagonal / total).

??? success "Solution to Exercise 1"
        import numpy as np
        from scipy import sparse

        pred = np.array([0, 1, 2, 0, 1, 2, 0, 1, 2])
        gt = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2])

        cm = sparse.coo_matrix(
            (np.ones(len(pred)), (pred, gt)),
            shape=(3, 3)
        ).toarray()

        print("Confusion matrix:")
        print(cm.astype(int))

        accuracy = np.trace(cm) / cm.sum()
        print(f"Accuracy: {accuracy:.4f}")

---

**Exercise 2.**
Create a row-stochastic matrix from a sparse count matrix: start with the sparse matrix `C = sparse.csr_matrix([[10, 5, 0], [3, 20, 2], [0, 1, 15]])`. Normalize each row to sum to 1 using `sparse.diags` to build the inverse row-sum diagonal matrix, then multiply. Print the normalized matrix and verify each row sums to 1.

??? success "Solution to Exercise 2"
        import numpy as np
        from scipy import sparse

        C = sparse.csr_matrix([[10, 5, 0],
                                [3, 20, 2],
                                [0, 1, 15]])

        row_sums = np.array(C.sum(axis=1)).flatten()
        row_sums[row_sums == 0] = 1
        D_inv = sparse.diags(1.0 / row_sums)
        normalized = D_inv @ C

        print("Normalized matrix:")
        print(normalized.toarray())
        print("Row sums:", np.array(normalized.sum(axis=1)).flatten())

---

**Exercise 3.**
Build a sparse co-occurrence matrix from two categorical arrays: `words = np.array([0, 1, 2, 0, 1, 0, 2, 1])` and `docs = np.array([0, 0, 0, 1, 1, 2, 2, 2])`, where each pair (word, doc) indicates that the word appeared in that document. Use COO format to count occurrences, convert to CSR, and print the dense matrix. Then compute the TF normalization (divide each column by its sum).

??? success "Solution to Exercise 3"
        import numpy as np
        from scipy import sparse

        words = np.array([0, 1, 2, 0, 1, 0, 2, 1])
        docs = np.array([0, 0, 0, 1, 1, 2, 2, 2])

        co_occur = sparse.coo_matrix(
            (np.ones(len(words)), (words, docs))
        ).tocsr()

        print("Co-occurrence matrix (words x docs):")
        print(co_occur.toarray().astype(int))

        # TF normalization: divide each column by its sum
        col_sums = np.array(co_occur.sum(axis=0)).flatten()
        col_sums[col_sums == 0] = 1
        D_inv_col = sparse.diags(1.0 / col_sums)
        tf_normalized = co_occur @ D_inv_col

        print("\nTF-normalized matrix:")
        print(tf_normalized.toarray().round(4))
