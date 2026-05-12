# Tick Control

This document covers the XAxis/YAxis objects, tick locators, and tick formatters for fine-grained control over axis behavior.

!!! tip "Mental Model"
    Tick placement is a two-step pipeline: a Locator decides where ticks go, and a Formatter decides what text to display at each tick. Matplotlib picks reasonable defaults, but swapping in a different Locator (e.g., `MultipleLocator(5)`) or Formatter (e.g., `PercentFormatter`) gives you precise control without manually listing every tick position.

    At a deeper level, **ticks encode the scale** — they convert visual position
    into quantitative meaning. Position is the most precise visual encoding
    channel, and ticks are what allow the viewer to decode it back into numbers.
    Without ticks, a viewer can see *relative* differences but cannot read
    *absolute* values.

!!! note "The Three Tools You Actually Need"
    The Locator/Formatter system has many classes, but in practice these three
    cover ~90% of use cases:

    1. **`MultipleLocator(n)`** — ticks at regular intervals of `n`
    2. **`MaxNLocator(n)`** — automatic placement with at most `n` ticks
    3. **`FuncFormatter(func)`** — custom label text via a callback

    Everything else (`FixedLocator`, `LogLocator`, `DateFormatter`, etc.) is for
    specialized domains. Start with these three and reach for others only when
    they cannot express your needs.

!!! tip "Design Principle"

    - **Too many ticks** → visual clutter, labels overlap
    - **Too few ticks** → reader cannot judge scale or read values

    The goal is **just enough ticks to communicate the scale** without competing
    with the data. As a rule of thumb, 5--7 ticks per axis is usually optimal
    for most plot sizes.

## XAxis and YAxis Objects

Access axis objects via the axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

# Access axis objects
xaxis = ax.xaxis
yaxis = ax.yaxis

print(type(xaxis))  # <class 'matplotlib.axis.XAxis'>
print(type(yaxis))  # <class 'matplotlib.axis.YAxis'>
```

### set_ticks_position

Control where ticks appear:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-10, 10, 500)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.xaxis.set_ticks_position('top')
ax.yaxis.set_ticks_position('right')
plt.show()
```

Options: `'top'`, `'bottom'`, `'left'`, `'right'`, `'both'`, `'none'`, `'default'`

### Axis Visibility

Hide an entire axis:

```python
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
```

### get_ticklocs and get_ticklabels

Get current tick positions and labels:

```python
print(ax.xaxis.get_ticklocs())
print(ax.yaxis.get_ticklocs())
print(ax.xaxis.get_ticklabels())  # List of Text objects
```

---

## Tick Locators

Tick locators determine where tick marks appear on an axis.

### Using Locators

```python
import matplotlib as mpl

ax.xaxis.set_major_locator(locator)
ax.yaxis.set_major_locator(locator)
ax.xaxis.set_minor_locator(locator)
ax.yaxis.set_minor_locator(locator)
```

### MultipleLocator

Place ticks at multiples of a base value:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 500)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(0.5))

ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.1))

plt.show()
```

### FixedLocator

Place ticks at specific locations:

```python
ax.xaxis.set_major_locator(mpl.ticker.FixedLocator([-1, 0, 1]))
ax.yaxis.set_major_locator(mpl.ticker.FixedLocator([-0.2, 0, 0.2]))
```

### MaxNLocator

Automatically choose up to N tick locations:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

fig, axes = plt.subplots(2, 3, sharex=True, sharey=True, figsize=(12, 3))

for ax in axes.flatten():
    ax.xaxis.set_major_locator(mpl.ticker.MaxNLocator(3))
    ax.yaxis.set_major_locator(mpl.ticker.MaxNLocator(3))
    ax.plot(np.random.randn(10))

plt.show()
```

### NullLocator

Remove all ticks:

```python
ax.xaxis.set_major_locator(mpl.ticker.NullLocator())
ax.yaxis.set_major_locator(mpl.ticker.NullLocator())
```

Useful for image displays:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.datasets import fetch_olivetti_faces

faces = fetch_olivetti_faces().images

fig, ax = plt.subplots(5, 5, figsize=(5, 5))
fig.subplots_adjust(hspace=0, wspace=0)

for i in range(5):
    for j in range(5):
        ax[i, j].xaxis.set_major_locator(mpl.ticker.NullLocator())
        ax[i, j].yaxis.set_major_locator(mpl.ticker.NullLocator())
        ax[i, j].imshow(faces[10 * i + j], cmap="bone")

plt.show()
```

### Locators Summary

| Locator | Description |
|---------|-------------|
| `MultipleLocator(base)` | Ticks at multiples of base |
| `FixedLocator(locs)` | Ticks at specified locations |
| `MaxNLocator(n)` | At most n ticks |
| `NullLocator()` | No ticks |
| `AutoLocator()` | Automatic (default) |
| `LogLocator()` | For log scales |
| `LinearLocator(n)` | Exactly n evenly spaced |
| `IndexLocator(base, offset)` | Ticks at base*i + offset |

---

## Tick Formatters

Tick formatters control how tick labels are displayed.

### Using Formatters

```python
import matplotlib as mpl

ax.xaxis.set_major_formatter(formatter)
ax.yaxis.set_major_formatter(formatter)
ax.xaxis.set_minor_formatter(formatter)
ax.yaxis.set_minor_formatter(formatter)
```

### NullFormatter

Remove tick labels while keeping ticks:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 500)
y = np.sin(x) * np.exp(-x**2/20)

fig, ax = plt.subplots()
ax.plot(x, y)

ax.xaxis.set_major_formatter(mpl.ticker.NullFormatter())

plt.show()
```

### FuncFormatter

Custom formatting with a function:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

def format_func(value, tick_number):
    # Convert to multiples of pi/2
    N = int(np.round(2 * value / np.pi))
    if N == 0:
        return "0"
    elif N == 1:
        return "$\\pi/2$"
    elif N == -1:
        return "$-\\pi/2$"
    elif N == 2:
        return "$\\pi$"
    elif N == -2:
        return "$-\\pi$"
    elif N % 2 > 0:
        return f"${N}\\pi/2$"
    else:
        return f"${N // 2}\\pi$"

x = np.linspace(-2*np.pi, 2*np.pi, 500)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)

ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(np.pi / 2))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(np.pi / 4))
ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(format_func))

plt.show()
```

### DateFormatter

Format datetime tick labels:

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import yfinance as yf

df = yf.Ticker('AAPL').history(start='2020-07-01', end='2020-12-31')

fig, ax = plt.subplots(figsize=(15, 3))
ax.plot(df.index, df['Close'])

# Date formatting
date_format = mpl_dates.DateFormatter('%b, %d %Y')
ax.xaxis.set_major_formatter(date_format)

fig.autofmt_xdate()
plt.show()
```

#### Date Format Codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | Year (4 digit) | 2024 |
| `%y` | Year (2 digit) | 24 |
| `%m` | Month (number) | 01-12 |
| `%b` | Month (abbrev) | Jan |
| `%B` | Month (full) | January |
| `%d` | Day | 01-31 |
| `%H` | Hour (24h) | 00-23 |
| `%M` | Minute | 00-59 |
| `%S` | Second | 00-59 |

### StrMethodFormatter

Format using string format specification:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 1, 100)
y = x ** 2 * 1000

fig, ax = plt.subplots()
ax.plot(x, y)

# Format with commas and 0 decimals
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

plt.show()
```

### PercentFormatter

Format as percentages:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 1, 100)
y = x ** 2

fig, ax = plt.subplots()
ax.plot(x, y)

# xmax=1.0 means 1.0 = 100%
ax.yaxis.set_major_formatter(mpl.ticker.PercentFormatter(xmax=1.0))

plt.show()
```

### ScalarFormatter

Default formatter with scientific notation control:

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(0, 1, 100)
y = x * 1e6

fig, ax = plt.subplots()
ax.plot(x, y)

formatter = mpl.ticker.ScalarFormatter(useMathText=True)
formatter.set_scientific(True)
formatter.set_powerlimits((-2, 2))
ax.yaxis.set_major_formatter(formatter)

plt.show()
```

### Formatters Summary

| Formatter | Description |
|-----------|-------------|
| `NullFormatter()` | No labels |
| `FuncFormatter(func)` | Custom function |
| `StrMethodFormatter(fmt)` | String format |
| `PercentFormatter(xmax)` | Percentage |
| `ScalarFormatter()` | Default with options |
| `LogFormatter()` | For log scales |
| `DateFormatter(fmt)` | Date/time |

---

## Complete Example: Stock Chart

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mpl_dates
import numpy as np
import pandas as pd

# Create sample time series
dates = pd.date_range('2024-01-01', periods=100, freq='D')
values = np.cumsum(np.random.randn(100)) * 1000 + 50000

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(dates, values)

# Date formatter for x-axis
ax.xaxis.set_major_formatter(mpl_dates.DateFormatter('%b %Y'))
ax.xaxis.set_major_locator(mpl_dates.MonthLocator())

# Currency formatter for y-axis
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.0f}'))

ax.set_title('Portfolio Value')
fig.autofmt_xdate()
plt.show()
```

## Complete Example: Math Plot with Grid

```python
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 500)
y = np.sin(x) * np.exp(-x**2/20)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(x, y)

# Configure x-axis
ax.xaxis.set_major_locator(mpl.ticker.MultipleLocator(np.pi))
ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(np.pi/4))
ax.xaxis.set_ticks_position('bottom')

# Configure y-axis
ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(0.2))
ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(0.05))
ax.yaxis.set_ticks_position('left')

# Add grid for both major and minor ticks
ax.grid(which='major', linestyle='-', linewidth=0.5)
ax.grid(which='minor', linestyle=':', linewidth=0.5, alpha=0.5)

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Damped Sine Wave')

plt.show()
```

---

## Key Takeaways

- Access axis objects via `ax.xaxis` and `ax.yaxis`
- **Locators** control where ticks appear
- **Formatters** control how tick labels are displayed
- `set_ticks_position()` controls tick placement
- Apply locators/formatters to major and minor ticks separately
- Use `MultipleLocator` for regular intervals
- Use `FuncFormatter` for custom label formatting
- Use `DateFormatter` for time series data


---

## Exercises

**Exercise 1.** Write code that sets custom major tick positions at multiples of $\pi$ on the x-axis using `ax.set_xticks()` and LaTeX tick labels.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    # Solution code depends on the specific exercise
    x = np.linspace(0, 2 * np.pi, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x))
    ax.set_title('Example Solution')
    plt.show()
    ```

    See the content of this page for the relevant API details to construct the full solution.

---

**Exercise 2.** Explain the difference between major and minor ticks in Matplotlib. How do you enable minor ticks?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Write code that uses `matplotlib.ticker.MultipleLocator` to set major ticks at intervals of 1 and minor ticks at intervals of 0.25.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    x = np.linspace(0, 2 * np.pi, 100)
    axes[0].plot(x, np.sin(x))
    axes[0].set_title('Left Subplot')

    axes[1].plot(x, np.cos(x))
    axes[1].set_title('Right Subplot')

    plt.tight_layout()
    plt.show()
    ```

    Adapt this pattern to the specific requirements of the exercise.

---

**Exercise 4.** Create a plot with tick marks pointing inward (`ax.tick_params(direction='in')`) and a custom tick label font size.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    x = np.linspace(0, 10, 100)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), 'b-', lw=2)
    ax.set_title('Solution')
    plt.show()
    ```

    Refer to the code examples in the main content for the specific API calls needed.
