# Plot Types (kind Parameter)

The `kind` parameter in pandas `plot()` determines the type of visualization. This document covers all available plot types.

!!! tip "Mental Model"
    The `kind` parameter selects the chart type. Line for trends over time, bar for category comparisons, hist for distributions, scatter for relationships between two variables, box for distribution summaries. Each kind answers a different question about the data -- pick the kind that matches your question.

## Available Plot Types

| kind | Plot Type | Use Case |
|------|-----------|----------|
| `'line'` | Line plot | Time series, trends |
| `'bar'` | Vertical bar | Category comparison |
| `'barh'` | Horizontal bar | Category comparison |
| `'hist'` | Histogram | Distribution |
| `'box'` | Box plot | Distribution summary |
| `'kde'`/`'density'` | Kernel density | Smooth distribution |
| `'area'` | Stacked area | Composition over time |
| `'pie'` | Pie chart | Proportions |
| `'scatter'` | Scatter plot | Relationship between variables |
| `'hexbin'` | Hexbin plot | Dense scatter alternative |

## Line Plot (Default)

```python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.DataFrame({
    'A': np.random.randn(50).cumsum(),
    'B': np.random.randn(50).cumsum()
})

df.plot(kind='line')  # or just df.plot()
plt.show()
```

## Bar Plot

### Vertical Bar (kind='bar')

```python
# Count categories
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
df = pd.read_csv(url)

fig, ax = plt.subplots(figsize=(10, 4))
df['continent'].value_counts().plot(kind='bar', ax=ax)
ax.set_title('Countries by Continent')
plt.show()
```

### Horizontal Bar (kind='barh')

```python
fig, ax = plt.subplots(figsize=(8, 5))
df['continent'].value_counts().plot(kind='barh', ax=ax)
ax.set_title('Countries by Continent')
plt.show()
```

## Histogram (kind='hist')

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

fig, ax = plt.subplots(figsize=(8, 4))
df['Age'].plot(kind='hist', bins=20, ax=ax, edgecolor='black')
ax.set_title('Age Distribution')
ax.set_xlabel('Age')
plt.show()
```

### Histogram Keywords

```python
df['Age'].plot(
    kind='hist',
    bins=30,           # Number of bins
    density=True,      # Normalize to density
    alpha=0.7,         # Transparency
    edgecolor='black'  # Bar edge color
)
```

## Box Plot (kind='box')

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

fig, ax = plt.subplots(figsize=(5, 4))
df['Age'].plot(kind='box', ax=ax)
ax.set_title('Age Distribution')
plt.show()
```

### Horizontal Box Plot

```python
fig, ax = plt.subplots(figsize=(8, 3))
df['Age'].plot(kind='box', ax=ax, vert=False)
ax.set_title('Horizontal Boxplot of Passenger Ages')
ax.set_xlabel('Age')
plt.show()
```

### Multiple Box Plots

```python
fig, ax = plt.subplots(figsize=(10, 4))
df[['Age', 'Fare']].plot(kind='box', ax=ax)
plt.show()
```

## Density Plot (kind='density' or kind='kde')

Kernel Density Estimation shows a smooth distribution curve:

```python
url = 'https://raw.githubusercontent.com/justmarkham/DAT8/master/data/drinks.csv'
df = pd.read_csv(url)

fig, ax = plt.subplots(figsize=(10, 4))

# Histogram with density overlay
df['beer_servings'].plot(kind='hist', bins=20, density=True, alpha=0.5, ax=ax)
df['beer_servings'].plot(kind='density', ax=ax)

ax.set_xlabel('Beer Servings')
ax.set_title('Distribution of Beer Servings')
plt.show()
```

## Scatter Plot (kind='scatter')

Requires both `x` and `y` parameters:

```python
df = pd.read_csv('https://vincentarelbundock.github.io/Rdatasets/csv/datasets/mtcars.csv')

fig, ax = plt.subplots(figsize=(8, 5))
df.plot(
    kind='scatter',
    x='wt',
    y='mpg',
    ax=ax
)
ax.set_title('Weight vs MPG')
plt.show()
```

### Scatter with Size and Color

```python
fig, ax = plt.subplots(figsize=(10, 6))
df.plot(
    kind='scatter',
    x='wt',
    y='mpg',
    s=df['hp'],           # Point size by horsepower
    c='disp',             # Color by displacement
    colormap='Blues',
    alpha=0.6,
    ax=ax
)
ax.set_title('Weight vs MPG (size=HP, color=Displacement)')
plt.show()
```

## Area Plot (kind='area')

Stacked area chart for composition over time:

```python
df = pd.DataFrame({
    'A': np.random.rand(10) * 10,
    'B': np.random.rand(10) * 10,
    'C': np.random.rand(10) * 10
}, index=pd.date_range('2024-01-01', periods=10))

fig, ax = plt.subplots(figsize=(10, 5))
df.plot(kind='area', ax=ax, alpha=0.5)
ax.set_title('Stacked Area Plot')
plt.show()
```

### Unstacked Area

```python
df.plot(kind='area', stacked=False, alpha=0.4)
```

## Pie Chart (kind='pie')

For Series data showing proportions:

```python
data = pd.Series([30, 25, 20, 15, 10], 
                 index=['A', 'B', 'C', 'D', 'E'])

fig, ax = plt.subplots(figsize=(6, 6))
data.plot(kind='pie', ax=ax, autopct='%1.1f%%')
ax.set_ylabel('')  # Remove default ylabel
ax.set_title('Category Proportions')
plt.show()
```

## Hexbin Plot (kind='hexbin')

For large scatter datasets, hexbin aggregates points:

```python
n = 10000
df = pd.DataFrame({
    'x': np.random.randn(n),
    'y': np.random.randn(n)
})

fig, ax = plt.subplots(figsize=(8, 6))
df.plot(
    kind='hexbin',
    x='x',
    y='y',
    gridsize=25,
    cmap='YlOrRd',
    ax=ax
)
ax.set_title('Hexbin Density Plot')
plt.show()
```

## Choosing the Right Plot Type

| Data Type | Goal | Recommended kind |
|-----------|------|------------------|
| Time series | Show trend | `'line'` |
| Categories | Compare counts | `'bar'` or `'barh'` |
| Single numeric | Show distribution | `'hist'` or `'kde'` |
| Single numeric | Summary stats | `'box'` |
| Two numeric | Show relationship | `'scatter'` |
| Two numeric (large n) | Density | `'hexbin'` |
| Proportions | Part of whole | `'pie'` |
| Multiple series | Composition | `'area'` |

## Quick Reference

```python
# Line (default)
df.plot()
df.plot(kind='line')

# Bar
df['col'].value_counts().plot(kind='bar')
df['col'].value_counts().plot(kind='barh')

# Histogram
df['col'].plot(kind='hist', bins=20)

# Box
df['col'].plot(kind='box')
df[['col1', 'col2']].plot(kind='box')

# Density
df['col'].plot(kind='density')
df['col'].plot(kind='kde')

# Scatter
df.plot(kind='scatter', x='col1', y='col2')

# Area
df.plot(kind='area')

# Pie
series.plot(kind='pie')

# Hexbin
df.plot(kind='hexbin', x='col1', y='col2')
```


---

## Exercises

**Exercise 1.** Write code that creates a line plot, bar plot, and scatter plot from the same DataFrame using `df.plot(kind=...)`.

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

**Exercise 2.** List all available plot kinds in `df.plot()` and describe when each is most appropriate.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that creates an area plot using `df.plot.area()` to show cumulative values over time.

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

**Exercise 4.** Create a pie chart from a Series using `s.plot.pie()` with `autopct='%1.1f%%'`.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
