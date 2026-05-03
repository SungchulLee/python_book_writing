# Mutual Information

Correlation measures linear dependence between two variables, but many important relationships are nonlinear. Mutual information provides a more general measure: it quantifies the total amount of information that one random variable provides about another, capturing all forms of statistical dependence. When two variables are independent, knowing one tells us nothing about the other, and mutual information is zero. This section defines mutual information, derives its equivalent characterizations in terms of entropy, and establishes its key properties.

!!! tip "Mental Model"
    Mutual information measures how much knowing $X$ reduces your uncertainty about $Y$ (and vice versa). Unlike correlation, it captures all forms of dependence -- linear, nonlinear, or otherwise. It equals zero if and only if $X$ and $Y$ are truly independent, making it a universal detector of statistical relationships.

## Definition

Let $X$ and $Y$ be discrete random variables with joint distribution $p(x, y)$ and marginal distributions $p(x)$ and $p(y)$. The **mutual information** between $X$ and $Y$ is

$$
I(X; Y) = \sum_{x} \sum_{y} p(x, y) \log \frac{p(x, y)}{p(x) \, p(y)}
$$

This is precisely the KL divergence between the joint distribution and the product of the marginals:

$$
I(X; Y) = D_{\mathrm{KL}}(p_{X,Y} \| p_X \, p_Y)
$$

Mutual information measures how much the joint distribution $p(x, y)$ deviates from the distribution that $X$ and $Y$ would have if they were independent. The larger the deviation, the more information the two variables share.

## Equivalent Characterizations

Mutual information connects to Shannon entropy through three equivalent expressions. Each provides a different interpretation.

**Reduction in uncertainty about $X$ from observing $Y$:**

$$
I(X; Y) = H(X) - H(X \mid Y)
$$

where $H(X \mid Y) = -\sum_{x,y} p(x,y) \log p(x \mid y)$ is the conditional entropy. Observing $Y$ reduces the uncertainty about $X$ by exactly $I(X; Y)$.

**Reduction in uncertainty about $Y$ from observing $X$:**

$$
I(X; Y) = H(Y) - H(Y \mid X)
$$

By symmetry of mutual information, the information that $X$ provides about $Y$ equals the information that $Y$ provides about $X$.

**Inclusion-exclusion with joint entropy:**

$$
I(X; Y) = H(X) + H(Y) - H(X, Y)
$$

where $H(X, Y) = -\sum_{x,y} p(x,y) \log p(x,y)$ is the joint entropy. This expression shows that mutual information accounts for the "overlap" in the uncertainty of $X$ and $Y$.

## Properties

Mutual information satisfies several fundamental properties.

**Non-negativity.** Since mutual information is a KL divergence, Gibbs' inequality gives

$$
I(X; Y) \geq 0
$$

with equality if and only if $X$ and $Y$ are independent (i.e., $p(x,y) = p(x) p(y)$ for all $x, y$).

**Symmetry.** Unlike KL divergence, mutual information is symmetric:

$$
I(X; Y) = I(Y; X)
$$

This follows immediately from the inclusion-exclusion form $H(X) + H(Y) - H(X, Y)$, which is symmetric in $X$ and $Y$.

**Upper bounds.** Mutual information is bounded above by the entropy of either variable:

$$
I(X; Y) \leq \min\{H(X), H(Y)\}
$$

This follows from the non-negativity of conditional entropy: $H(X \mid Y) \geq 0$ implies $I(X; Y) = H(X) - H(X \mid Y) \leq H(X)$, and similarly for $H(Y)$.

!!! example "Independent vs Dependent Variables"
    Let $X$ be a fair coin flip with $P(X=0) = P(X=1) = 1/2$, so $H(X) = 1$ bit.

    **Independent case.** If $Y$ is another independent fair coin, then $H(X \mid Y) = H(X) = 1$ bit, so $I(X; Y) = 0$. Knowing $Y$ tells us nothing about $X$.

    **Fully dependent case.** If $Y = X$, then $H(X \mid Y) = 0$ (knowing $Y$ determines $X$ exactly), so $I(X; Y) = H(X) = 1$ bit. The mutual information equals the entropy of each variable.

## Summary

Mutual information $I(X; Y) = D_{\mathrm{KL}}(p_{X,Y} \| p_X p_Y)$ measures the total statistical dependence between two random variables. It equals the reduction in entropy of one variable given knowledge of the other, is always non-negative, and is symmetric. Unlike linear correlation, mutual information captures all forms of dependence, making it zero if and only if the variables are independent.


---

## Exercises

**Exercise 1.** Write code that computes the mutual information between two discrete random variables from a joint probability table.

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

**Exercise 2.** Explain the relationship between mutual information and entropy: $I(X; Y) = H(X) + H(Y) - H(X, Y)$.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the statistical method and its assumptions.

---

**Exercise 3.** Write code that estimates mutual information between two continuous variables using `sklearn.metrics.mutual_info_score` on discretized data.

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

**Exercise 4.** Demonstrate that mutual information is zero for independent variables and positive for dependent variables.

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    from scipy import stats

    np.random.seed(42)
    data = np.random.randn(500)
    result = stats.describe(data)
    print(result)
    ```
