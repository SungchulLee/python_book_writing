# Covariance Correlation

!!! tip "Mental Model"
    Covariance measures how two variables move together (positive = same direction, negative = opposite), while correlation normalizes covariance to the $[-1, 1]$ range for easy comparison. `np.cov` returns a matrix where entry $(i,j)$ is the covariance between variables $i$ and $j$; `np.corrcoef` does the same but normalized.

## np.cov

### 1. Basic Usage

`np.cov` computes the covariance matrix. Note: it's a function only, not a method.

```python
import numpy as np

def main():
    a = np.random.normal(size=(2, 5))
    
    print("a =")
    print(a)
    print()
    
    # np.cov is a function, not a method
    try:
        print(a.cov())
    except AttributeError as e:
        print(f"Error: {e}")
    
    print()
    print("np.cov(a) =")
    print(np.cov(a))

if __name__ == "__main__":
    main()
```

### 2. Row Convention

By default, each row is a variable and each column is an observation.

```python
import numpy as np

def main():
    # 2 variables, 5 observations each
    np.random.seed(42)
    x = np.random.randn(5)
    y = 2 * x + np.random.randn(5) * 0.5  # correlated with x
    
    data = np.vstack([x, y])  # shape (2, 5)
    
    print(f"data.shape = {data.shape}")
    print("data =")
    print(data)
    print()
    
    cov_matrix = np.cov(data)
    print("Covariance matrix:")
    print(cov_matrix)
    print()
    print(f"Var(x) = {cov_matrix[0, 0]:.4f}")
    print(f"Var(y) = {cov_matrix[1, 1]:.4f}")
    print(f"Cov(x, y) = {cov_matrix[0, 1]:.4f}")

if __name__ == "__main__":
    main()
```

### 3. Single Variable

For a 1D array, `np.cov` returns the variance as a 0D array.

```python
import numpy as np

def main():
    x = np.array([1, 2, 3, 4, 5])
    
    # Covariance of single variable = variance
    cov_result = np.cov(x)
    var_result = np.var(x, ddof=1)  # ddof=1 for sample variance
    
    print(f"x = {x}")
    print(f"np.cov(x) = {cov_result}")
    print(f"np.var(x, ddof=1) = {var_result}")

if __name__ == "__main__":
    main()
```

## np.corrcoef

### 1. Basic Usage

`np.corrcoef` computes the correlation coefficient matrix.

```python
import numpy as np

def main():
    a = np.random.normal(size=(2, 5))
    
    print("a =")
    print(a)
    print()
    
    # np.corrcoef is a function, not a method
    try:
        print(a.corrcoef())
    except AttributeError as e:
        print(f"Error: {e}")
    
    print()
    print("np.corrcoef(a) =")
    print(np.corrcoef(a))

if __name__ == "__main__":
    main()
```

### 2. Interpretation

Correlation coefficients range from -1 to 1.

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Create correlated variables
    x = np.random.randn(100)
    y_pos = 0.8 * x + 0.2 * np.random.randn(100)  # positive correlation
    y_neg = -0.8 * x + 0.2 * np.random.randn(100)  # negative correlation
    y_none = np.random.randn(100)  # no correlation
    
    print(f"Corr(x, y_pos):  {np.corrcoef(x, y_pos)[0, 1]:+.4f}")
    print(f"Corr(x, y_neg):  {np.corrcoef(x, y_neg)[0, 1]:+.4f}")
    print(f"Corr(x, y_none): {np.corrcoef(x, y_none)[0, 1]:+.4f}")

if __name__ == "__main__":
    main()
```

### 3. Multiple Variables

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # 3 variables, 100 observations
    x1 = np.random.randn(100)
    x2 = 0.5 * x1 + np.random.randn(100)
    x3 = -0.3 * x1 + 0.4 * x2 + np.random.randn(100)
    
    data = np.vstack([x1, x2, x3])
    corr_matrix = np.corrcoef(data)
    
    print("Correlation matrix:")
    print(np.round(corr_matrix, 3))
    print()
    print("Interpretation:")
    print(f"  x1-x2: {corr_matrix[0, 1]:+.3f}")
    print(f"  x1-x3: {corr_matrix[0, 2]:+.3f}")
    print(f"  x2-x3: {corr_matrix[1, 2]:+.3f}")

if __name__ == "__main__":
    main()
```

## cov vs corrcoef

### 1. Key Difference

Correlation is normalized covariance (scale-independent).

```python
import numpy as np

def main():
    np.random.seed(42)
    
    x = np.random.randn(100)
    y = 2 * x + np.random.randn(100)
    
    # Scale y by 100
    y_scaled = y * 100
    
    print("Covariance (scale-dependent):")
    print(f"  Cov(x, y):        {np.cov(x, y)[0, 1]:.4f}")
    print(f"  Cov(x, y_scaled): {np.cov(x, y_scaled)[0, 1]:.4f}")
    print()
    
    print("Correlation (scale-independent):")
    print(f"  Corr(x, y):        {np.corrcoef(x, y)[0, 1]:.4f}")
    print(f"  Corr(x, y_scaled): {np.corrcoef(x, y_scaled)[0, 1]:.4f}")

if __name__ == "__main__":
    main()
```

### 2. Formula Relation

$$\text{Corr}(X, Y) = \frac{\text{Cov}(X, Y)}{\sigma_X \cdot \sigma_Y}$$

```python
import numpy as np

def main():
    np.random.seed(42)
    
    x = np.random.randn(100)
    y = 0.8 * x + np.random.randn(100) * 0.5
    
    # Manual correlation calculation
    cov_xy = np.cov(x, y)[0, 1]
    std_x = np.std(x, ddof=1)
    std_y = np.std(y, ddof=1)
    
    manual_corr = cov_xy / (std_x * std_y)
    numpy_corr = np.corrcoef(x, y)[0, 1]
    
    print(f"Cov(x, y):     {cov_xy:.4f}")
    print(f"Std(x):        {std_x:.4f}")
    print(f"Std(y):        {std_y:.4f}")
    print()
    print(f"Manual corr:   {manual_corr:.4f}")
    print(f"np.corrcoef:   {numpy_corr:.4f}")

if __name__ == "__main__":
    main()
```

### 3. Diagonal Elements

```python
import numpy as np

def main():
    np.random.seed(42)
    
    x = np.random.randn(100) * 5  # std ≈ 5
    y = np.random.randn(100) * 2  # std ≈ 2
    
    data = np.vstack([x, y])
    
    print("Covariance matrix diagonal (variances):")
    cov = np.cov(data)
    print(f"  Var(x): {cov[0, 0]:.4f}")
    print(f"  Var(y): {cov[1, 1]:.4f}")
    print()
    
    print("Correlation matrix diagonal (always 1):")
    corr = np.corrcoef(data)
    print(f"  Corr(x, x): {corr[0, 0]:.4f}")
    print(f"  Corr(y, y): {corr[1, 1]:.4f}")

if __name__ == "__main__":
    main()
```

## Practical Examples

### 1. Stock Returns

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Simulated daily returns for 3 stocks
    market = np.random.randn(252) * 0.01
    
    stock_a = 1.2 * market + np.random.randn(252) * 0.005
    stock_b = 0.8 * market + np.random.randn(252) * 0.008
    stock_c = -0.5 * market + np.random.randn(252) * 0.01
    
    returns = np.vstack([stock_a, stock_b, stock_c])
    
    print("Correlation matrix of returns:")
    corr = np.corrcoef(returns)
    labels = ['A', 'B', 'C']
    
    print("     A      B      C")
    for i, label in enumerate(labels):
        row = "  ".join(f"{corr[i, j]:+.3f}" for j in range(3))
        print(f"{label}  {row}")

if __name__ == "__main__":
    main()
```

### 2. Portfolio Variance

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Annual returns for 2 assets
    returns = np.random.randn(2, 100) * 0.1  # 10% volatility
    
    # Portfolio weights
    weights = np.array([0.6, 0.4])
    
    # Covariance matrix
    cov = np.cov(returns)
    
    # Portfolio variance: w' * Cov * w
    portfolio_var = weights @ cov @ weights
    portfolio_std = np.sqrt(portfolio_var)
    
    print("Covariance matrix:")
    print(np.round(cov, 4))
    print()
    print(f"Weights: {weights}")
    print(f"Portfolio variance: {portfolio_var:.4f}")
    print(f"Portfolio std dev: {portfolio_std:.4f}")

if __name__ == "__main__":
    main()
```

### 3. Feature Selection

```python
import numpy as np

def main():
    np.random.seed(42)
    
    # Features and target
    n = 1000
    x1 = np.random.randn(n)
    x2 = 0.9 * x1 + np.random.randn(n) * 0.1  # highly correlated with x1
    x3 = np.random.randn(n)  # independent
    target = 2 * x1 + 0.5 * x3 + np.random.randn(n) * 0.5
    
    features = np.vstack([x1, x2, x3])
    
    # Correlation with target
    corr_with_target = [np.corrcoef(f, target)[0, 1] for f in features]
    
    print("Correlation with target:")
    for i, corr in enumerate(corr_with_target, 1):
        print(f"  x{i}: {corr:+.4f}")
    
    # Feature correlation matrix
    print()
    print("Feature correlation matrix:")
    print(np.round(np.corrcoef(features), 3))

if __name__ == "__main__":
    main()
```

---

## Exercises

**Exercise 1.**
Generate two correlated random variables: `x = np.random.randn(1000)` and `y = 0.8 * x + 0.2 * np.random.randn(1000)`. Compute the covariance matrix using `np.cov(x, y)` and the correlation matrix using `np.corrcoef(x, y)`. Verify that the correlation is close to the expected value.

??? success "Solution to Exercise 1"

        import numpy as np

        np.random.seed(42)
        x = np.random.randn(1000)
        y = 0.8 * x + 0.2 * np.random.randn(1000)

        cov = np.cov(x, y)
        corr = np.corrcoef(x, y)
        print(f"Covariance matrix:\n{cov.round(3)}")
        print(f"Correlation: {corr[0, 1]:.4f}")

---

**Exercise 2.**
Create a 3-variable dataset `X = np.random.randn(3, 100)` and compute the 3x3 covariance matrix. Verify that it is symmetric and that the diagonal elements equal the variances of each variable.

??? success "Solution to Exercise 2"

        import numpy as np

        X = np.random.randn(3, 100)
        cov = np.cov(X)
        print(f"Symmetric: {np.allclose(cov, cov.T)}")
        for i in range(3):
            print(f"Var(X[{i}]) = {X[i].var(ddof=1):.4f}, cov[{i},{i}] = {cov[i,i]:.4f}")

---

**Exercise 3.**
Generate two uncorrelated variables `x` and `y` (independent standard normals, 500 samples). Compute their correlation coefficient and verify it is close to 0. Then transform `y_corr = x + y` and verify the correlation between `x` and `y_corr` is close to `1/sqrt(2)`.

??? success "Solution to Exercise 3"

        import numpy as np

        np.random.seed(42)
        x = np.random.randn(500)
        y = np.random.randn(500)
        print(f"corr(x, y): {np.corrcoef(x, y)[0, 1]:.4f}")  # ~0

        y_corr = x + y
        print(f"corr(x, x+y): {np.corrcoef(x, y_corr)[0, 1]:.4f}")  # ~0.707

---

**Exercise 4.**
Given a `(1000, 3)` data matrix representing three stock returns, compute the full `3x3` correlation matrix using `np.corrcoef`. Identify the most and least correlated pair of stocks by finding the off-diagonal maximum and minimum.

??? success "Solution to Exercise 4"

        import numpy as np

        np.random.seed(42)
        base = np.random.randn(1000)
        returns = np.column_stack([
            base + np.random.randn(1000) * 0.5,
            base + np.random.randn(1000) * 2,
            np.random.randn(1000)
        ])

        corr = np.corrcoef(returns.T)
        print(f"Correlation matrix:\n{np.round(corr, 3)}")

        # Mask diagonal for off-diagonal search
        np.fill_diagonal(corr, np.nan)
        max_idx = np.unravel_index(np.nanargmax(corr), corr.shape)
        min_idx = np.unravel_index(np.nanargmin(corr), corr.shape)
        print(f"Most correlated pair:  stocks {max_idx}")
        print(f"Least correlated pair: stocks {min_idx}")

---

**Exercise 5.**
Demonstrate that correlation is scale-invariant but covariance is not. Compute `np.cov` and `np.corrcoef` for two variables `x` and `y`, then for `10*x` and `y`. Show that covariance changes by a factor of 10 but correlation stays the same.

??? success "Solution to Exercise 5"

        import numpy as np

        np.random.seed(0)
        x = np.random.randn(500)
        y = 2 * x + np.random.randn(500)

        cov_orig = np.cov(x, y)[0, 1]
        corr_orig = np.corrcoef(x, y)[0, 1]

        cov_scaled = np.cov(10 * x, y)[0, 1]
        corr_scaled = np.corrcoef(10 * x, y)[0, 1]

        print(f"Cov(x, y):      {cov_orig:.4f}")
        print(f"Cov(10x, y):    {cov_scaled:.4f}")  # ~10x larger
        print(f"Ratio:          {cov_scaled / cov_orig:.1f}")  # ~10

        print(f"Corr(x, y):     {corr_orig:.4f}")
        print(f"Corr(10x, y):   {corr_scaled:.4f}")  # Same!
        print(f"Same: {np.allclose(corr_orig, corr_scaled)}")  # True
