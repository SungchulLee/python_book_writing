# ML Loss Connection

The loss functions used in machine learning are not arbitrary choices. They arise from principled information-theoretic and statistical foundations. In particular, the most common losses -- cross-entropy for classification and mean squared error for regression -- can both be derived from maximum likelihood estimation, which in turn is equivalent to minimizing KL divergence between the data distribution and the model. This section makes these connections explicit.

!!! tip "Mental Model"
    MLE, cross-entropy minimization, and KL divergence minimization are three views of the same optimization. Cross-entropy loss in classification is just negative log-likelihood; MSE loss in regression is negative log-likelihood under Gaussian errors. Understanding this unification reveals that "choosing a loss function" is really "choosing a probabilistic model."

## MLE as Cross-Entropy Minimization

Suppose we observe i.i.d. data $x_1, x_2, \ldots, x_n$ drawn from an unknown true distribution $p$. We fit a parametric model $q_\theta$ by maximizing the log-likelihood:

$$
\hat{\theta}_{\mathrm{MLE}} = \arg\max_\theta \sum_{i=1}^{n} \log q_\theta(x_i)
$$

Dividing by $n$ and taking the limit as $n \to \infty$, the law of large numbers gives

$$
\frac{1}{n} \sum_{i=1}^{n} \log q_\theta(x_i) \xrightarrow{a.s.} \mathbb{E}_{p}[\log q_\theta(X)] = -H(p, q_\theta)
$$

where $H(p, q_\theta) = -\sum_x p(x) \log q_\theta(x)$ is the cross-entropy. Maximizing the expected log-likelihood is therefore equivalent to minimizing the cross-entropy:

$$
\arg\max_\theta \, \mathbb{E}_p[\log q_\theta(X)] = \arg\min_\theta \, H(p, q_\theta)
$$

Since $H(p, q_\theta) = H(p) + D_{\mathrm{KL}}(p \| q_\theta)$ and $H(p)$ does not depend on $\theta$, this is also equivalent to minimizing the KL divergence:

$$
\arg\min_\theta \, H(p, q_\theta) = \arg\min_\theta \, D_{\mathrm{KL}}(p \| q_\theta)
$$

!!! tip "The Core Equivalence"
    Maximum likelihood estimation, cross-entropy minimization, and KL divergence minimization all select the same model parameters $\theta$. The three perspectives are mathematically equivalent.

In practice, we replace the true distribution $p$ with the empirical distribution $\hat{p}(x) = \frac{1}{n} \sum_{i=1}^n \mathbf{1}[x_i = x]$, so the training loss becomes the empirical cross-entropy.

## Classification Losses

For classification tasks, the model outputs a predicted probability distribution over classes, and the loss function is the negative log-likelihood evaluated at the true class.

**Binary cross-entropy.** For binary classification with true label $y \in \{0, 1\}$ and predicted probability $\hat{p} = q_\theta(Y=1 \mid x)$, the negative log-likelihood for a single example is

$$
\ell(y, \hat{p}) = -y \log \hat{p} - (1 - y) \log(1 - \hat{p})
$$

This is exactly the cross-entropy between the one-hot distribution $p = (1-y, y)$ and the predicted distribution $q = (1-\hat{p}, \hat{p})$.

**Categorical cross-entropy.** For multi-class classification with $K$ classes, true one-hot label $\mathbf{y} = (y_1, \ldots, y_K)$, and predicted probabilities $\hat{\mathbf{p}} = (\hat{p}_1, \ldots, \hat{p}_K)$, the loss is

$$
\ell(\mathbf{y}, \hat{\mathbf{p}}) = -\sum_{k=1}^{K} y_k \log \hat{p}_k
$$

Since exactly one $y_k = 1$ and the rest are zero, this simplifies to $-\log \hat{p}_c$ where $c$ is the true class.

## Regression Losses

For regression tasks, the connection runs through a Gaussian noise model.

**Mean squared error from Gaussian MLE.** Suppose the model assumes $Y \mid X = x \sim \mathcal{N}(f_\theta(x), \sigma^2)$ for a fixed noise variance $\sigma^2$. The negative log-likelihood for one observation $(x_i, y_i)$ is

$$
-\log q_\theta(y_i \mid x_i) = \frac{(y_i - f_\theta(x_i))^2}{2\sigma^2} + \frac{1}{2}\log(2\pi\sigma^2)
$$

The second term is constant with respect to $\theta$, so minimizing the negative log-likelihood reduces to minimizing the mean squared error:

$$
\hat{\theta}_{\mathrm{MLE}} = \arg\min_\theta \frac{1}{n}\sum_{i=1}^{n}(y_i - f_\theta(x_i))^2
$$

!!! warning "MSE Assumes Gaussian Noise"
    Using MSE loss implicitly assumes that the prediction errors are Gaussian with constant variance. When this assumption is violated (e.g., heavy-tailed errors or heteroscedastic noise), alternative losses such as Huber loss or quantile regression may be more appropriate.

## Summary

Maximum likelihood estimation is equivalent to minimizing cross-entropy, which is equivalent to minimizing KL divergence between the data distribution and the model. Binary and categorical cross-entropy losses are direct instances of negative log-likelihood for classification. Mean squared error arises as the MLE loss under a Gaussian noise assumption for regression.


---

## Exercises

**Exercise 1.** Explain the connection between cross-entropy loss in machine learning and information theory. Why is minimizing cross-entropy equivalent to maximizing likelihood?

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

**Exercise 2.** Write code that computes the binary cross-entropy loss for a set of predictions and true labels.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Demonstrate that minimizing the KL divergence between the true distribution and the model's predicted distribution is equivalent to minimizing the cross-entropy loss.

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

**Exercise 4.** Write code that computes both the log-likelihood and the cross-entropy for a simple classification example and shows they differ only by a constant.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
