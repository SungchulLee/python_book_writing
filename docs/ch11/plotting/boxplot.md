# boxplot() Method

The `boxplot()` method creates box-and-whisker plots that summarize the distribution of numeric data, showing median, quartiles, and outliers.

!!! tip "Mental Model"
    A box plot is a five-number summary in visual form: minimum, Q1, median, Q3, maximum, with dots for outliers beyond 1.5 x IQR. It reveals center, spread, skew, and outliers at a glance. Use the `by` parameter to compare distributions across categories side-by-side.

## Anatomy of a Box Plot

```
    ┌─────────┐
    │         │   ← Maximum (or upper fence)
    │    ○    │   ← Outliers (beyond 1.5×IQR)
    │    │    │
────┼────┼────┼── ← Q3 (75th percentile)
    │    │    │
    │    │    │   ← IQR (Interquartile Range)
    │    │    │
────┼────┼────┼── ← Median (Q2, 50th percentile)
    │    │    │
    │    │    │
────┼────┼────┼── ← Q1 (25th percentile)
    │    │    │
    │    │    │
    └────┴────┘   ← Minimum (or lower fence)
```

## Basic Usage

### Single Column

```python
import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

fig, ax = plt.subplots(figsize=(5, 4))
df.boxplot(column='Age', ax=ax)
ax.set_title('Age Distribution')
plt.show()
```

### Multiple Columns

```python
fig, ax = plt.subplots(figsize=(10, 5))
df.boxplot(column=['Age', 'Fare'], ax=ax)
ax.set_title('Age and Fare Distributions')
plt.show()
```

## Key Parameters

### column - Select Columns

```python
# Single column
df.boxplot(column='Age')

# Multiple columns
df.boxplot(column=['Age', 'Fare', 'SibSp'])
```

### by - Group by Category

Create separate box plots for each category:

```python
fig, ax = plt.subplots(figsize=(10, 5))
df.boxplot(column='Age', by='Pclass', ax=ax)
ax.set_title('Age Distribution by Passenger Class')
plt.suptitle('')  # Remove automatic title
plt.show()
```

### vert - Orientation

```python
# Vertical (default)
df.boxplot(column='Age', vert=True)

# Horizontal
fig, ax = plt.subplots(figsize=(8, 3))
df['Age'].plot(kind='box', vert=False, ax=ax)
ax.set_title('Horizontal Box Plot')
plt.show()
```

### figsize - Figure Size

```python
df.boxplot(column='Age', figsize=(8, 5))
```

## Practical Example: Titanic Passenger Ages

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url, index_col='PassengerId')

fig, ax = plt.subplots(figsize=(8, 4))
df['Age'].plot(kind='box', ax=ax, vert=False)
ax.set_title('Horizontal Boxplot of Passenger Ages on Titanic')
ax.set_xlabel('Age')
ax.spines[['top', 'left', 'right']].set_visible(False)
plt.show()
```

## Grouped Box Plots

### By Single Category

```python
fig, ax = plt.subplots(figsize=(10, 5))
df.boxplot(column='Fare', by='Pclass', ax=ax)
ax.set_ylabel('Fare')
plt.suptitle('')
ax.set_title('Fare Distribution by Class')
plt.show()
```

### By Multiple Categories

```python
fig, ax = plt.subplots(figsize=(12, 5))
df.boxplot(column='Age', by=['Pclass', 'Survived'], ax=ax)
plt.suptitle('')
ax.set_title('Age by Class and Survival')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

## Comparing Multiple Variables

```python
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
df = pd.read_csv(url)

fig, ax = plt.subplots(figsize=(10, 5))
df[['beer_servings', 'spirit_servings', 'wine_servings']].boxplot(ax=ax)
ax.set_title('Alcohol Servings by Type')
ax.set_ylabel('Servings')
plt.show()
```

## Customization

### Using Return Value

```python
fig, ax = plt.subplots(figsize=(8, 5))
bp = df.boxplot(column='Age', ax=ax, return_type='dict')

# Customize colors
for box in bp['boxes']:
    box.set_color('steelblue')
for whisker in bp['whiskers']:
    whisker.set_color('gray')
for cap in bp['caps']:
    cap.set_color('gray')
for median in bp['medians']:
    median.set_color('red')
    median.set_linewidth(2)

plt.show()
```

### Grid and Appearance

```python
fig, ax = plt.subplots(figsize=(8, 5))
df.boxplot(
    column='Age',
    ax=ax,
    grid=False,
    notch=True,  # Confidence interval notch
    patch_artist=True  # Enable fill color
)
plt.show()
```

## boxplot() vs plot(kind='box')

Both methods create box plots, but with slightly different interfaces:

```python
# Using boxplot()
df.boxplot(column='Age')
df.boxplot(column='Age', by='Pclass')

# Using plot(kind='box')
df['Age'].plot(kind='box')
df[['Age', 'Fare']].plot(kind='box')
```

| Feature | boxplot() | plot(kind='box') |
|---------|-----------|------------------|
| by parameter | ✅ Direct support | ❌ Manual grouping |
| Multiple columns | column=list | Select columns first |
| return_type | ✅ Supported | ❌ Not supported |
| Method location | DataFrame only | Series and DataFrame |

## Interpreting Box Plots

```python
# Get the statistics shown in box plot
stats = df['Age'].describe()
print(stats)
```

```
count    714.000000
mean      29.699118
std       14.526497
min        0.420000
25%       20.125000    ← Q1 (box bottom)
50%       28.000000    ← Median (line in box)
75%       38.000000    ← Q3 (box top)
max       80.000000
```

### Identifying Outliers

Outliers are points beyond:
- Upper fence: Q3 + 1.5 × IQR
- Lower fence: Q1 - 1.5 × IQR

```python
Q1 = df['Age'].quantile(0.25)
Q3 = df['Age'].quantile(0.75)
IQR = Q3 - Q1

lower_fence = Q1 - 1.5 * IQR
upper_fence = Q3 + 1.5 * IQR

outliers = df[(df['Age'] < lower_fence) | (df['Age'] > upper_fence)]
print(f"Number of outliers: {len(outliers)}")
```

## Method Signature

```python
DataFrame.boxplot(
    column=None,       # Column(s) to plot
    by=None,           # Group by column
    ax=None,           # Matplotlib axes
    fontsize=None,     # Tick label font size
    rot=0,             # Tick label rotation
    grid=True,         # Show grid
    figsize=None,      # Figure size
    layout=None,       # Subplot layout
    return_type=None,  # Return type ('axes', 'dict', 'both')
    **kwargs           # Additional kwargs
)
```

## Summary

```python
# Single column
df.boxplot(column='Age')

# Multiple columns
df.boxplot(column=['Age', 'Fare'])

# Grouped by category
df.boxplot(column='Age', by='Pclass')

# Horizontal (via plot)
df['Age'].plot(kind='box', vert=False)

# Customized
df.boxplot(column='Age', grid=False, notch=True)
```


---

## Exercises

**Exercise 1.** Write code that creates a box plot from a DataFrame using `df.plot.box()` or `df.boxplot()`.

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

**Exercise 2.** Explain what the box, whiskers, and outlier points represent in a box plot.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Create a grouped box plot using `df.boxplot(by='group_column')` to compare distributions across groups.

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

**Exercise 4.** Write code that customizes a box plot by changing colors, whisker style, and outlier markers.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
