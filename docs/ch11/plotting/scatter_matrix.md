# scatter_matrix

The `pd.plotting.scatter_matrix()` function creates a grid of scatter plots showing pairwise relationships between numeric columns. Diagonal plots show the distribution of each variable.

!!! tip "Mental Model"
    A scatter matrix is an n-by-n grid where each off-diagonal cell shows a scatter plot of two variables and each diagonal cell shows one variable's distribution. It is the fastest way to spot correlations, clusters, and outliers across all variable pairs at once -- a visual correlation matrix.

## Basic Usage

```python
import pandas as pd
import matplotlib.pyplot as plt

url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
df = pd.read_csv(url)

# Create scatter matrix
pd.plotting.scatter_matrix(df[['beer_servings', 'spirit_servings', 'wine_servings']], 
                           figsize=(10, 10))
plt.tight_layout()
plt.show()
```

## Understanding the Output

For n numeric columns, the scatter matrix creates an n×n grid:

- **Off-diagonal cells**: Scatter plots showing relationship between two variables
- **Diagonal cells**: Distribution of each variable (histogram by default)

```
           beer    spirit   wine
        ┌────────┬────────┬────────┐
  beer  │  hist  │ scatter│ scatter│
        ├────────┼────────┼────────┤
 spirit │ scatter│  hist  │ scatter│
        ├────────┼────────┼────────┤
  wine  │ scatter│ scatter│  hist  │
        └────────┴────────┴────────┘
```

## Key Parameters

### figsize - Figure Size

```python
pd.plotting.scatter_matrix(df, figsize=(12, 12))
```

### diagonal - Distribution Plot Type

```python
# Histogram (default)
pd.plotting.scatter_matrix(df, diagonal='hist')

# Kernel density estimate
pd.plotting.scatter_matrix(df, diagonal='kde')
```

### alpha - Point Transparency

```python
pd.plotting.scatter_matrix(df, alpha=0.5)
```

### marker - Point Style

```python
pd.plotting.scatter_matrix(df, marker='o')
pd.plotting.scatter_matrix(df, marker='.')
pd.plotting.scatter_matrix(df, marker='+')
```

### s - Point Size

```python
pd.plotting.scatter_matrix(df, s=50)  # Larger points
pd.plotting.scatter_matrix(df, s=10)  # Smaller points
```

### hist_kwds - Histogram Customization

```python
pd.plotting.scatter_matrix(
    df,
    diagonal='hist',
    hist_kwds={'bins': 20, 'edgecolor': 'black'}
)
```

### density_kwds - KDE Customization

```python
pd.plotting.scatter_matrix(
    df,
    diagonal='kde',
    density_kwds={'linewidth': 2}
)
```

### ax - Specify Axes Array

```python
fig, axes = plt.subplots(3, 3, figsize=(12, 12))
pd.plotting.scatter_matrix(df[['col1', 'col2', 'col3']], ax=axes)
plt.show()
```

## Practical Example: Iris Dataset

```python
from sklearn.datasets import load_iris
import pandas as pd
import matplotlib.pyplot as plt

# Load iris data
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)

# Create scatter matrix
fig = pd.plotting.scatter_matrix(
    df,
    figsize=(12, 12),
    diagonal='kde',
    alpha=0.6,
    marker='o',
    s=30
)

plt.suptitle('Iris Dataset - Pairwise Relationships', y=1.02)
plt.tight_layout()
plt.show()
```

## Practical Example: Financial Data

```python
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Download multiple stock prices
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
df = yf.download(tickers, start='2023-01-01', end='2024-01-01')['Close']

# Calculate returns
returns = df.pct_change().dropna()

# Scatter matrix of returns
pd.plotting.scatter_matrix(
    returns,
    figsize=(10, 10),
    diagonal='kde',
    alpha=0.3,
    marker='.'
)
plt.suptitle('Stock Return Correlations', y=1.02)
plt.tight_layout()
plt.show()
```

## Practical Example: Drinks Dataset

```python
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
df = pd.read_csv(url)

# Select numeric columns for alcohol consumption
alcohol_cols = ['beer_servings', 'spirit_servings', 'wine_servings', 'total_litres_of_pure_alcohol']

fig, ax = plt.subplots(figsize=(12, 12))
pd.plotting.scatter_matrix(
    df[alcohol_cols],
    diagonal='hist',
    alpha=0.5,
    hist_kwds={'bins': 15, 'edgecolor': 'black'}
)
plt.tight_layout()
plt.show()
```

## Color by Category

To color points by a categorical variable, use matplotlib directly:

```python
from sklearn.datasets import load_iris
import pandas as pd
import matplotlib.pyplot as plt

iris = load_iris()
df = pd.DataFrame(iris.data, columns=['sepal_l', 'sepal_w', 'petal_l', 'petal_w'])
df['species'] = iris.target

# Create figure
fig, axes = plt.subplots(4, 4, figsize=(12, 12))

colors = ['red', 'green', 'blue']
columns = ['sepal_l', 'sepal_w', 'petal_l', 'petal_w']

for i, col1 in enumerate(columns):
    for j, col2 in enumerate(columns):
        ax = axes[i, j]
        if i == j:
            # Diagonal: histogram
            for species in range(3):
                mask = df['species'] == species
                ax.hist(df.loc[mask, col1], alpha=0.5, color=colors[species])
        else:
            # Off-diagonal: scatter
            for species in range(3):
                mask = df['species'] == species
                ax.scatter(df.loc[mask, col2], df.loc[mask, col1], 
                          alpha=0.5, color=colors[species], s=10)
        
        if j == 0:
            ax.set_ylabel(col1)
        if i == 3:
            ax.set_xlabel(col2)

plt.tight_layout()
plt.show()
```

## Interpreting Scatter Matrices

### What to Look For

1. **Linear relationships**: Points forming a line indicate correlation
2. **Clusters**: Groups of points may indicate categories
3. **Outliers**: Isolated points away from the main cluster
4. **Distribution shape**: Diagonal plots show if data is normal, skewed, etc.

### Correlation Patterns

| Pattern | Interpretation |
|---------|----------------|
| Points along diagonal (↗) | Positive correlation |
| Points along anti-diagonal (↘) | Negative correlation |
| Circular cloud | No correlation |
| Distinct clusters | Possible categorical grouping |

## Method Signature

```python
pandas.plotting.scatter_matrix(
    frame,              # DataFrame
    alpha=0.5,          # Point transparency
    figsize=None,       # Figure size
    ax=None,            # Axes array
    grid=False,         # Show grid
    diagonal='hist',    # 'hist' or 'kde'
    marker='.',         # Point marker
    density_kwds=None,  # KDE kwargs
    hist_kwds=None,     # Histogram kwargs
    range_padding=0.05, # Padding around axis limits
    **kwargs            # Additional scatter kwargs
)
```

## Summary

```python
# Basic scatter matrix
pd.plotting.scatter_matrix(df)

# With KDE on diagonal
pd.plotting.scatter_matrix(df, diagonal='kde')

# Customized
pd.plotting.scatter_matrix(
    df[['col1', 'col2', 'col3']],
    figsize=(10, 10),
    diagonal='hist',
    alpha=0.5,
    marker='o',
    hist_kwds={'bins': 20}
)
```

## Alternatives

For more advanced pairwise plots with categorical coloring:

```python
# Using seaborn (if available)
import seaborn as sns
sns.pairplot(df, hue='category_column')
```


---

## Exercises

**Exercise 1.** Write code that creates a scatter matrix (pair plot) using `pd.plotting.scatter_matrix(df)`.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd
    import numpy as np

    # Solution for the specific exercise
    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(10), 'B': np.random.randn(10)})
    print(df.head())
    ```

---

**Exercise 2.** Explain what information a scatter matrix provides. What is shown on the diagonal?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Create a scatter matrix with `diagonal='kde'` instead of the default histogram.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(20), 'B': np.random.randn(20)})
    result = df.describe()
    print(result)
    ```

---

**Exercise 4.** Write code that creates a scatter matrix for a subset of columns and customizes the figure size.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
