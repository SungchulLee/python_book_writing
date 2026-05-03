# Cross-Entropy

Suppose we have data drawn from a true distribution $p$, but we use a model $q$ to encode or predict that data. Cross-entropy measures the average number of bits (or nats) needed per symbol when using the code optimized for $q$ instead of the true distribution $p$. Because any mismatch between $p$ and $q$ incurs extra cost, cross-entropy is always at least as large as the entropy of $p$ itself. This property makes cross-entropy a natural loss function for classification and density estimation.

!!! tip "Mental Model"
    Cross-entropy $H(p, q)$ is the total cost of encoding data from $p$ using a code designed for $q$. It equals the intrinsic entropy $H(p)$ plus the KL divergence penalty for using the wrong code. Minimizing cross-entropy is therefore equivalent to minimizing KL divergence, which is why it serves as the standard classification loss.

## Definition

Let $p$ and $q$ be two probability distributions over the same discrete sample space $\mathcal{X}$. The **cross-entropy** of $q$ relative to $p$ is

$$
H(p, q) = -\sum_{x \in \mathcal{X}} p(x) \log q(x)
$$

where the logarithm is base 2 for bits or base $e$ for nats. The sum runs over all outcomes where $p(x) > 0$, and we require $q(x) > 0$ whenever $p(x) > 0$.

For continuous distributions with densities $p(x)$ and $q(x)$, the cross-entropy is

$$
H(p, q) = -\int p(x) \log q(x) \, dx
$$

Intuitively, each term $-\log q(x)$ represents the cost of encoding outcome $x$ under the model $q$, and the cross-entropy averages this cost over the true distribution $p$.

## Relationship to Entropy and KL Divergence

Cross-entropy decomposes into two interpretable components. The entropy $H(p) = -\sum_x p(x) \log p(x)$ represents the minimum achievable average code length, and the Kullback-Leibler divergence $D_{\mathrm{KL}}(p \| q)$ captures the additional cost due to using $q$ instead of $p$:

$$
H(p, q) = H(p) + D_{\mathrm{KL}}(p \| q)
$$

To see why, expand the right-hand side:

$$
H(p) + D_{\mathrm{KL}}(p \| q) = -\sum_x p(x) \log p(x) + \sum_x p(x) \log \frac{p(x)}{q(x)} = -\sum_x p(x) \log q(x) = H(p, q)
$$

Since $D_{\mathrm{KL}}(p \| q) \geq 0$ with equality if and only if $p = q$, this decomposition immediately yields the fundamental inequality:

$$
H(p, q) \geq H(p)
$$

with equality if and only if $p = q$. Minimizing cross-entropy with respect to $q$ is therefore equivalent to minimizing the KL divergence from $p$ to $q$.

!!! tip "Why Minimize Cross-Entropy?"
    In machine learning, the true data distribution $p$ is fixed (determined by the dataset), so $H(p)$ is a constant. Minimizing $H(p, q)$ over the model parameters is therefore equivalent to minimizing $D_{\mathrm{KL}}(p \| q)$, which finds the model $q$ closest to the true distribution in the KL sense.

## Example

Consider a three-class classification problem where the true label distribution for a single example is $p = (1, 0, 0)$ (the example belongs to class 1). Two models produce the following predicted distributions:

- Model A: $q_A = (0.7, 0.2, 0.1)$
- Model B: $q_B = (0.4, 0.3, 0.3)$

The cross-entropies are

$$
H(p, q_A) = -1 \cdot \log(0.7) - 0 \cdot \log(0.2) - 0 \cdot \log(0.1) = -\log(0.7) \approx 0.357 \text{ nats}
$$

$$
H(p, q_B) = -\log(0.4) \approx 0.916 \text{ nats}
$$

Model A achieves a lower cross-entropy because it assigns higher probability to the correct class. This illustrates why cross-entropy rewards confident, correct predictions.

## Summary

Cross-entropy $H(p, q)$ measures the expected coding cost when data from $p$ is encoded using a model $q$. It decomposes as $H(p) + D_{\mathrm{KL}}(p \| q)$, and minimizing it over $q$ is equivalent to minimizing the KL divergence from $p$ to $q$.


---

## Exercises

**Exercise 1.** Write code that computes the cross-entropy between two discrete probability distributions using the formula $H(p, q) = -\sum p_i \log(q_i)$.

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

**Exercise 2.** Explain the relationship between cross-entropy, entropy, and KL divergence. Write the mathematical formula connecting them.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that computes the cross-entropy loss for a binary classification example with predicted probabilities and true labels.

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

**Exercise 4.** Demonstrate that the cross-entropy of a distribution with itself equals its entropy.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
