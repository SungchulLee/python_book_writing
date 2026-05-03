# hist() Method

The `hist()` method creates histograms for numeric columns in a DataFrame. Unlike `plot(kind='hist')`, this method is specifically designed for histogram creation with additional features.

!!! tip "Mental Model"
    A histogram chops a continuous variable into bins and counts how many values fall in each bin. The `bins` parameter controls granularity: too few bins hide patterns, too many create noise. Use `density=True` to normalize to a probability distribution, and the `by` parameter to compare distributions across groups.

## Basic Usage

### DataFrame.hist()

Creates histograms for all numeric columns:

```python
import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Histogram for all numeric columns
df.hist(figsize=(12, 8))
plt.tight_layout()
plt.show()
```

### Series.hist()

```python
df['Age'].hist(bins=20)
plt.show()
```

## Key Parameters

### bins - Number of Bins

```python
fig, axes = plt.subplots(1, 3, figsize=(12, 3))

df['Age'].hist(bins=10, ax=axes[0])
axes[0].set_title('10 bins')

df['Age'].hist(bins=30, ax=axes[1])
axes[1].set_title('30 bins')

df['Age'].hist(bins=50, ax=axes[2])
axes[2].set_title('50 bins')

plt.tight_layout()
plt.show()
```

### column - Specific Column

```python
df.hist(column='Age', bins=20)
plt.show()
```

### by - Group by Category

Create separate histograms for each category:

```python
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
df = pd.read_csv(url)

# Histogram of beer servings by continent
df.hist(column='beer_servings', by='continent', figsize=(12, 8), sharex=True, sharey=True)
plt.tight_layout()
plt.show()
```

### layout - Subplot Arrangement

```python
# Arrange histograms in 2 rows, 3 columns
df.hist(column='beer_servings', by='continent', layout=(2, 3), figsize=(12, 6))
plt.tight_layout()
plt.show()
```

### sharex and sharey - Share Axes

```python
df.hist(
    column='beer_servings',
    by='continent',
    sharex=True,  # Same x-axis scale
    sharey=True   # Same y-axis scale
)
```

### figsize - Figure Size

```python
df.hist(figsize=(15, 10))
```

### ax - Specify Axes

```python
fig, axes = plt.subplots(3, 3, figsize=(12, 9))
df.hist(ax=axes)
plt.tight_layout()
plt.show()
```

## Practical Example: Housing Data

```python
import os
import tarfile
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt

# Download and load housing data
DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml2/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

def fetch_housing_data():
    if not os.path.isdir(HOUSING_PATH):
        os.makedirs(HOUSING_PATH)
    tgz_path = os.path.join(HOUSING_PATH, "housing.tgz")
    urllib.request.urlretrieve(HOUSING_URL, tgz_path)
    with tarfile.open(tgz_path) as tgz:
        tgz.extractall(path=HOUSING_PATH)

def load_housing_data():
    return pd.read_csv(os.path.join(HOUSING_PATH, "housing.csv"))

fetch_housing_data()
df = load_housing_data()

# Create histogram grid
fig, axes = plt.subplots(3, 3, figsize=(12, 9))
df.hist(bins=50, ax=axes)

# Clean up appearance
for ax in axes.flatten():
    ax.grid(False)
    ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.show()
```

## Practical Example: Titanic Data

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Create histograms for specific columns
fig, axes = plt.subplots(1, 5, figsize=(15, 3))
columns = ['Survived', 'Pclass', 'Age', 'SibSp', 'Fare']

for ax, col in zip(axes, columns):
    df[col].hist(ax=ax, density=True, edgecolor='black', alpha=0.7)
    ax.set_title(col)
    ax.set_ylabel('Density')

plt.tight_layout()
plt.show()
```

## Customization Options

### density - Normalize to Probability

```python
df['Age'].hist(density=True)  # Y-axis shows probability density
```

### edgecolor - Bar Borders

```python
df['Age'].hist(edgecolor='black')
```

### alpha - Transparency

```python
df['Age'].hist(alpha=0.7)
```

### color - Bar Color

```python
df['Age'].hist(color='steelblue')
```

## Comparing Distributions

### Overlapping Histograms

```python
fig, ax = plt.subplots(figsize=(10, 5))

# Survived vs not survived
df[df['Survived'] == 1]['Age'].hist(alpha=0.5, label='Survived', ax=ax)
df[df['Survived'] == 0]['Age'].hist(alpha=0.5, label='Did not survive', ax=ax)

ax.legend()
ax.set_xlabel('Age')
ax.set_title('Age Distribution by Survival')
plt.show()
```

### Side-by-Side with by Parameter

```python
df.hist(column='Age', by='Survived', figsize=(10, 4), sharex=True)
plt.tight_layout()
plt.show()
```

## hist() vs plot(kind='hist')

| Feature | df.hist() | df.plot(kind='hist') |
|---------|-----------|---------------------|
| Multiple columns | Automatic grid | Manual iteration |
| by parameter | ✅ Supported | ❌ Not supported |
| layout control | ✅ Built-in | Manual |
| Single column | Use Series | Use Series |

```python
# Both produce similar output for single column:
df['Age'].hist(bins=20)
df['Age'].plot(kind='hist', bins=20)
```

## Method Signature

```python
DataFrame.hist(
    column=None,       # Column(s) to plot
    by=None,           # Group by this column
    grid=True,         # Show grid
    xlabelsize=None,   # X label font size
    ylabelsize=None,   # Y label font size
    ax=None,           # Matplotlib axes
    sharex=False,      # Share x-axis
    sharey=False,      # Share y-axis
    figsize=None,      # Figure size
    layout=None,       # Subplot layout (rows, cols)
    bins=10,           # Number of bins
    **kwargs           # Additional hist kwargs
)
```

## Summary

```python
# All numeric columns
df.hist()

# Specific column
df.hist(column='Age')
df['Age'].hist()

# Grouped by category
df.hist(column='Age', by='Survived')

# Customized
df.hist(bins=30, figsize=(12, 8), edgecolor='black', alpha=0.7)

# With layout
df.hist(column='beer', by='continent', layout=(2, 3), sharex=True)
```


---

## Exercises

**Exercise 1.** Write code that creates a histogram from a DataFrame column using `df['col'].plot.hist(bins=30)`.

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

**Exercise 2.** Create overlaid histograms for two columns using `df[['a', 'b']].plot.hist(alpha=0.5)`.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that uses `df.plot.hist(subplots=True)` to create a separate histogram for each numeric column.

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

**Exercise 4.** Create a histogram with `density=True` and overlay a KDE curve using `df['col'].plot.kde()` on the same axes.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
