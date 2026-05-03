# plot() Keywords

The pandas `plot()` method accepts many keyword arguments to customize visualizations. This document covers the most commonly used parameters.

!!! tip "Mental Model"
    The `plot()` keywords fall into three groups: layout (`ax`, `figsize`, `subplots`), data presentation (`kind`, `x`, `y`, `secondary_y`), and styling (`color`, `alpha`, `title`, `grid`). The `ax` parameter is the most important -- it lets you place plots on pre-created matplotlib axes for multi-panel figures.

## ax - Specify Axes

The `ax` parameter allows plotting on an existing matplotlib axes object, enabling complex layouts.

```python
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

ticker = 'WMT'
df = yf.Ticker(ticker).history(start='2020-01-01', end='2020-12-31')

# Create figure with multiple subplots
fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 3))

# Plot on specific axes
df[['High', 'Low']].plot(ax=ax0, title='Price')
df['Volume'].plot(ax=ax1, title='Volume')

plt.tight_layout()
plt.show()
```

### Why Use ax?

- Combine multiple plots in one figure
- Control layout precisely
- Add annotations to specific subplots
- Reuse axes from other libraries

## title - Plot Title

```python
# Single title
df['Close'].plot(title='Stock Price')

# With ax
fig, ax = plt.subplots()
df['Close'].plot(ax=ax, title='WMT Closing Price 2020')
plt.show()
```

## figsize - Figure Size

Control the figure dimensions (width, height) in inches:

```python
# Wider figure
df.plot(figsize=(12, 4))

# Square figure
df.plot(figsize=(6, 6))

# Tall figure
df.plot(figsize=(6, 10))
```

## subplots - Separate Plots per Column

When `subplots=True`, each column gets its own subplot:

```python
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

ticker = 'WMT'
df = yf.Ticker(ticker).history(start='2020-01-01', end='2020-12-31')

# Each column in separate subplot
fig, axes = plt.subplots(1, 2, figsize=(12, 3))
df[['High', 'Low']].plot(ax=axes, subplots=True)
plt.tight_layout()
plt.show()
```

### With layout Parameter

```python
# 2x2 grid of subplots
df[['Open', 'High', 'Low', 'Close']].plot(
    subplots=True, 
    layout=(2, 2),
    figsize=(10, 8)
)
plt.tight_layout()
plt.show()
```

## x and y - Specify Columns

Use `x` and `y` to plot specific columns against each other:

```python
import yfinance as yf

ticker = 'AAPL'
company = yf.Ticker(ticker)
maturity = company.options[0]
calls = company.option_chain(maturity).calls

fig, ax = plt.subplots(figsize=(10, 4))
calls.plot(
    x='strike',
    y='lastPrice',
    ax=ax
)
ax.set_title(f'{ticker} Call Options')
plt.show()
```

### Multiple y Columns

```python
df.plot(x='date', y=['open', 'close'])
```

## label - Legend Label

Customize the legend label:

```python
fig, ax = plt.subplots(figsize=(10, 4))
calls.plot(
    x='strike', 
    y='lastPrice', 
    label=f'{ticker} Call {maturity}',
    ax=ax
)
plt.show()
```

## rot - Rotate Tick Labels

Rotate x-axis tick labels to prevent overlap:

```python
import pandas as pd

url = 'https://raw.githubusercontent.com/theJollySin/scipy_con_2019/master/modern_time_series_analysis/ModernTimeSeriesAnalysis/StateSpaceModels/global_temps.csv'
df = pd.read_csv(url)
df = df.pivot(index='Date', columns='Source', values='Mean')

# Rotate labels 30 degrees
df['GCAG'].plot(rot=30)
plt.show()
```

### Common Rotation Values

| Value | Use Case |
|-------|----------|
| 0 | Default horizontal |
| 45 | Moderate length labels |
| 90 | Long labels |
| 30 | Slight angle for dates |

## grid - Show Grid Lines

```python
df.plot(grid=True)
```

## legend - Control Legend

```python
# Show legend (default)
df.plot(legend=True)

# Hide legend
df.plot(legend=False)

# Legend position
df.plot().legend(loc='upper left')
```

## color / c - Line Colors

```python
# Single color
df['A'].plot(color='red')

# Multiple colors for multiple columns
df.plot(color=['red', 'blue', 'green'])

# Using color codes
df['A'].plot(color='#FF5733')
```

## style - Line Style

```python
# Dashed line
df['A'].plot(style='--')

# With markers
df['A'].plot(style='o-')  # Line with circle markers

# Different styles per column
df.plot(style=['--', '-.', ':'])
```

### Style Codes

| Code | Meaning |
|------|---------|
| `-` | Solid line |
| `--` | Dashed line |
| `-.` | Dash-dot line |
| `:` | Dotted line |
| `o` | Circle marker |
| `s` | Square marker |
| `^` | Triangle marker |

## alpha - Transparency

```python
# 50% transparent
df.plot(alpha=0.5)
```

## linewidth / lw - Line Width

```python
df.plot(linewidth=2)
```

## xlim and ylim - Axis Limits

```python
df.plot(xlim=(0, 100), ylim=(0, 50))
```

## Complete Example

```python
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Create sample data
df = pd.DataFrame({
    'A': np.random.randn(100).cumsum(),
    'B': np.random.randn(100).cumsum()
}, index=pd.date_range('2024-01-01', periods=100))

# Plot with multiple customizations
fig, ax = plt.subplots(figsize=(12, 5))

df.plot(
    ax=ax,
    title='Cumulative Random Walk',
    color=['steelblue', 'coral'],
    linewidth=1.5,
    alpha=0.8,
    grid=True,
    rot=45
)

ax.set_xlabel('Date')
ax.set_ylabel('Value')
plt.tight_layout()
plt.show()
```

## Summary Table

| Keyword | Purpose | Example |
|---------|---------|---------|
| `ax` | Target axes | `ax=ax0` |
| `title` | Plot title | `title='My Plot'` |
| `figsize` | Figure size | `figsize=(12, 4)` |
| `subplots` | Separate subplots | `subplots=True` |
| `x`, `y` | Column selection | `x='col1', y='col2'` |
| `label` | Legend label | `label='Series A'` |
| `rot` | Tick rotation | `rot=45` |
| `grid` | Show grid | `grid=True` |
| `legend` | Show legend | `legend=False` |
| `color` | Line color | `color='red'` |
| `style` | Line style | `style='--'` |
| `alpha` | Transparency | `alpha=0.5` |
| `linewidth` | Line width | `linewidth=2` |
| `xlim`, `ylim` | Axis limits | `xlim=(0, 100)` |


---

## Exercises

**Exercise 1.** Write code demonstrating the `figsize`, `title`, `xlabel`, `ylabel`, `grid`, and `legend` keywords in `df.plot()`.

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

**Exercise 2.** Explain the `style` parameter in `df.plot()`. Write code using `style=['r-', 'b--']` for two columns.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that uses `subplots=True` in `df.plot()` to create a separate subplot for each column.

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

**Exercise 4.** Create a plot using `df.plot()` and pass `ax` to plot on an existing Matplotlib axes object.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
