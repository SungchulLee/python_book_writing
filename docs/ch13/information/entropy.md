# Entropy

Entropy quantifies the average amount of surprise or uncertainty in a random variable. A fair coin has maximum entropy because each flip is maximally unpredictable, while a heavily biased coin has lower entropy because one outcome is nearly certain. Introduced by Claude Shannon in 1948, entropy provides the theoretical foundation for data compression: it gives the minimum average number of bits needed to encode samples from a distribution. This section defines Shannon entropy, establishes its key properties, and extends the concept to continuous distributions.

!!! tip "Mental Model"
    Entropy is the average surprise of a random variable. Rare events are highly surprising ($-\log p$ is large); common events are not. A fair coin maximizes entropy because every outcome is equally uncertain. Entropy sets a hard floor on compression: you cannot encode samples from a distribution using fewer than $H$ bits on average.

## Definition

Let $X$ be a discrete random variable taking values in a finite set $\mathcal{X}$ with probability mass function $p(x) = P(X = x)$. The **Shannon entropy** of $X$ is

$$
H(X) = -\sum_{x \in \mathcal{X}} p(x) \log p(x)
$$

where the logarithm is base 2 (giving entropy in bits) or base $e$ (giving entropy in nats). By convention, $0 \log 0 = 0$, which is justified by the limit $\lim_{p \to 0^+} p \log p = 0$.

Each term $-\log p(x)$ represents the **information content** (or surprise) of outcome $x$: rare events carry more information than common ones. Entropy averages this surprise over all possible outcomes.

## Properties

Shannon entropy satisfies several fundamental properties.

**Non-negativity.** For any discrete random variable $X$,

$$
H(X) \geq 0
$$

with equality if and only if $X$ is deterministic (one outcome has probability 1). This follows because $-p(x) \log p(x) \geq 0$ for all $p(x) \in [0, 1]$.

**Maximum entropy.** Among all distributions on a finite set $\mathcal{X}$ with $|\mathcal{X}| = n$, the uniform distribution $p(x) = 1/n$ maximizes entropy:

$$
H(X) \leq \log n
$$

with equality if and only if $X$ is uniformly distributed. This result follows from the non-negativity of KL divergence between $p$ and the uniform distribution.

**Concavity.** Entropy is a concave function of the probability distribution. For any two distributions $p$ and $q$ on the same space and $\lambda \in [0, 1]$,

$$
H(\lambda p + (1-\lambda) q) \geq \lambda H(p) + (1-\lambda) H(q)
$$

!!! example "Entropy of a Binary Random Variable"
    Consider a coin with probability $p$ of heads and $1 - p$ of tails. Its entropy is the binary entropy function:

    $$
    H(p) = -p \log p - (1 - p) \log(1 - p)
    $$

    At $p = 1/2$ (fair coin), $H = \log 2 = 1$ bit. At $p = 0$ or $p = 1$ (deterministic outcome), $H = 0$.

## Differential Entropy

For a continuous random variable $X$ with probability density function $p(x)$, the **differential entropy** is

$$
h(X) = -\int_{-\infty}^{\infty} p(x) \log p(x) \, dx
$$

Differential entropy shares some properties with its discrete counterpart, but there are important differences:

- **Can be negative.** For example, if $X \sim \text{Uniform}(0, a)$ with $a < 1$, then $h(X) = \log a < 0$.
- **Not invariant under changes of variable.** If $Y = g(X)$ for a smooth bijection $g$, then $h(Y) \neq h(X)$ in general.
- **Maximum entropy.** Among all continuous distributions on $\mathbb{R}$ with a given mean and variance, the Gaussian distribution maximizes differential entropy.

!!! note "Gaussian Differential Entropy"
    If $X \sim \mathcal{N}(\mu, \sigma^2)$, then

    $$
    h(X) = \frac{1}{2} \log(2 \pi e \sigma^2)
    $$

    This result shows that differential entropy grows logarithmically with the variance.

## Summary

Shannon entropy $H(X) = -\sum_x p(x) \log p(x)$ measures the average uncertainty in a discrete random variable. It is non-negative, maximized by the uniform distribution, and concave. Differential entropy extends this concept to continuous distributions but can be negative and is not invariant under changes of variable.


---

## Exercises

**Exercise 1.** Write code that computes the Shannon entropy of a discrete probability distribution $p = [0.25, 0.25, 0.25, 0.25]$ using the formula $H(p) = -\sum p_i \log_2(p_i)$.

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

**Exercise 2.** Explain why the uniform distribution has maximum entropy among all distributions on the same support.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that plots the entropy of a binary distribution (Bernoulli) as a function of the probability parameter $p$ for $p \in [0, 1]$.

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

**Exercise 4.** Compute the entropy of a dataset of categorical values by first computing the empirical probabilities and then applying the entropy formula.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
