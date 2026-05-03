# Fill and Fill Between

Fill regions in your plots to highlight areas of interest.

!!! tip "Mental Model"
    `fill_between(x, y1, y2)` shades the vertical region between two curves, while `fill()` fills an arbitrary polygon. Use `fill_between` to highlight confidence intervals, area under a curve, or the gap between two series. The `where` parameter lets you conditionally shade only parts that meet a criterion (e.g., where y1 > y2).

---

## ax.fill()

Fill a closed polygon:

```python
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

df = 5
chi2_statistics = 12.5

fig, ax = plt.subplots()

# Area before statistic
x = np.linspace(0, chi2_statistics, 100)
y = stats.chi2(df).pdf(x)
x = np.concatenate([[0], x, [chi2_statistics], [0]])
y = np.concatenate([[0], y, [0], [0]])
ax.fill(x, y, color='b', alpha=0.3)
ax.plot(x, y, color='b', linewidth=3)

# Area after statistic (p-value region)
x = np.linspace(chi2_statistics, 20, 100)
y = stats.chi2(df).pdf(x)
x = np.concatenate([[chi2_statistics], x, [20], [chi2_statistics]])
y = np.concatenate([[0], y, [0], [0]])
ax.fill(x, y, color='r', alpha=0.3)
ax.plot(x, y, color='r', linewidth=3)

ax.annotate('p value', 
            xy=((chi2_statistics + 15.0) / 2, 0.01),
            xytext=(16.5, 0.10),
            fontsize=15,
            arrowprops=dict(color='k', width=0.2, headwidth=8))

ax.set_title(f'Chi-Square Distribution (df={df})')
plt.show()
```

---

## ax.fill_between()

Fill the area between two curves or between a curve and a baseline:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y, 'b-', linewidth=2)
ax.fill_between(x, y, alpha=0.3)
ax.axhline(0, color='black', linewidth=0.5)
plt.show()
```

---

## Filling Between Two Curves

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y1 = np.sin(x)
y2 = np.sin(x) * 0.5

fig, ax = plt.subplots()
ax.plot(x, y1, 'b-', label='sin(x)')
ax.plot(x, y2, 'r-', label='0.5*sin(x)')
ax.fill_between(x, y1, y2, alpha=0.3, color='green')
ax.legend()
plt.show()
```

---

## Conditional Filling with where

Use the `where` parameter to fill only specific regions:

```python
import matplotlib.pyplot as plt
import yfinance as yf

def download(ticker, start=None, end=None):
    if start is None:
        return yf.Ticker(ticker).history(period="max")
    else:
        return yf.Ticker(ticker).history(start=start, end=end)

def main():
    df = download('AAPL', start='2020-07-01', end='2020-12-31')
    df['M15'] = df['Close'].rolling(15).mean()
    df['M50'] = df['Close'].rolling(50).mean()

    DATE = df.index[50:]
    y = df['Close'].loc[DATE]
    y_15 = df['M15'].loc[DATE]
    y_50 = df['M50'].loc[DATE]

    fig, ax = plt.subplots(figsize=(15, 3))

    ax.plot(DATE, y, label='AAPL', color='b')
    ax.plot(DATE, y_15, label='M15', color='g')
    ax.plot(DATE, y_50, label='M50', color='r')

    # Fill where M15 > M50 (bullish)
    ax.fill_between(DATE, y_15, y_50,
                    where=(y_15 > y_50), 
                    interpolate=True, 
                    color='r',
                    alpha=0.3)
    
    # Fill where M15 <= M50 (bearish)
    ax.fill_between(DATE, y_15, y_50,
                    where=(y_15 <= y_50), 
                    interpolate=True, 
                    color='b',
                    alpha=0.3)

    ax.set_xlabel('DATE')
    ax.set_ylabel('STOCK PRICE')
    ax.set_title('AAPL - Moving Average Crossover')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

---

## fill_between Parameters

```python
ax.fill_between(
    x,                    # x coordinates
    y1,                   # First y boundary
    y2=0,                 # Second y boundary (default: 0)
    where=None,           # Boolean array for conditional filling
    interpolate=False,    # Interpolate at boundaries
    step=None,            # 'pre', 'post', 'mid' for step functions
    color='blue',         # Fill color
    alpha=0.5,            # Transparency
    label='label'         # For legend
)
```

---

## fill_betweenx()

Fill horizontally (between x values for given y):

```python
import matplotlib.pyplot as plt
import numpy as np

y = np.linspace(0, 2*np.pi, 100)
x = np.sin(y)

fig, ax = plt.subplots()
ax.plot(x, y, 'b-')
ax.fill_betweenx(y, x, alpha=0.3)
ax.axvline(0, color='black', linewidth=0.5)
plt.show()
```

---

## Confidence Intervals

Common use case for uncertainty visualization:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 50)
y = np.sin(x)
y_err = 0.2 + 0.1 * np.random.randn(50)

fig, ax = plt.subplots()
ax.plot(x, y, 'b-', label='Mean')
ax.fill_between(x, y - y_err, y + y_err, alpha=0.3, label='±1 std')
ax.legend()
ax.set_title('Confidence Interval')
plt.show()
```

---

## Key Takeaways

- `ax.fill()` fills closed polygons
- `ax.fill_between()` fills between curves
- Use `where` for conditional filling
- Set `interpolate=True` for smooth boundaries
- `fill_betweenx()` fills horizontally
- Great for confidence intervals and crossover signals

!!! info "In Statistics and ML"

    `fill_between` is the standard tool for **confidence intervals** and **uncertainty bands**. Plot the mean prediction as a line and shade ±1 or ±2 standard deviations around it. In Bayesian models and ensemble methods, this visualizes prediction uncertainty — wider bands mean the model is less certain.

---

## Exercises

**Exercise 1.**
Plot the function `y = sin(x)` for `x` in $[0, 2\pi]$ and use `fill_between` to shade the area where `sin(x) > 0` in green and the area where `sin(x) < 0` in red. Use the `where` parameter and set `alpha=0.3` for both fills.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 2 * np.pi, 500)
        y = np.sin(x)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, color='black')
        ax.fill_between(x, y, 0, where=(y > 0), color='green', alpha=0.3, label='Positive')
        ax.fill_between(x, y, 0, where=(y < 0), color='red', alpha=0.3, label='Negative')
        ax.axhline(0, color='gray', linestyle='--', linewidth=0.5)
        ax.legend()
        ax.set_title('sin(x) with Positive/Negative Regions')
        plt.show()

---

**Exercise 2.**
Generate two curves `y1 = x^2` and `y2 = 2*x + 1` over `x` in $[-1, 3]$. Fill the region between them where `y2 > y1` in light blue and where `y1 > y2` in light coral. Use `interpolate=True` for smooth boundaries at the intersection points.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-1, 3, 500)
        y1 = x ** 2
        y2 = 2 * x + 1

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y1, label=r'$y = x^2$', color='blue')
        ax.plot(x, y2, label=r'$y = 2x + 1$', color='red')

        ax.fill_between(x, y1, y2, where=(y2 > y1), interpolate=True,
                         color='lightblue', alpha=0.5, label=r'$2x+1 > x^2$')
        ax.fill_between(x, y1, y2, where=(y1 > y2), interpolate=True,
                         color='lightcoral', alpha=0.5, label=r'$x^2 > 2x+1$')

        ax.legend()
        ax.set_title('Fill Between Two Curves')
        plt.show()

---

**Exercise 3.**
Simulate a random walk of 200 steps and compute a rolling mean and rolling standard deviation with a window of 20. Plot the rolling mean as a solid line and use `fill_between` to show a band at mean plus/minus one standard deviation. Label the band "1 SD Band" and add a legend.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np
        import pandas as pd

        np.random.seed(42)
        steps = np.random.randn(200)
        walk = np.cumsum(steps)

        s = pd.Series(walk)
        rolling_mean = s.rolling(20).mean()
        rolling_std = s.rolling(20).std()

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(walk, color='gray', alpha=0.5, label='Random Walk')
        ax.plot(rolling_mean, color='blue', linewidth=2, label='Rolling Mean')
        ax.fill_between(range(200),
                         rolling_mean - rolling_std,
                         rolling_mean + rolling_std,
                         color='blue', alpha=0.2, label='1 SD Band')
        ax.legend()
        ax.set_title('Random Walk with Rolling Mean and SD Band')
        plt.show()

---

**Exercise 4.**
Use `fill_between` with the `where` parameter to shade only the regions where a sinusoid is positive (green) and negative (red) separately. Plot `y = sin(x)` for `x` in `[0, 4π]`.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 4 * np.pi, 500)
        y = np.sin(x)

        fig, ax = plt.subplots()
        ax.plot(x, y, 'k-', linewidth=1)
        ax.axhline(0, color='gray', linewidth=0.5)
        ax.fill_between(x, y, 0, where=(y > 0), color='green', alpha=0.3, label='Positive')
        ax.fill_between(x, y, 0, where=(y < 0), color='red', alpha=0.3, label='Negative')
        ax.legend()
        ax.set_title('sin(x): Positive vs Negative Regions')
        plt.show()

---

**Exercise 5.**
Create a confidence band: plot `y = x^2` and shade the region between `y - 0.5|x|` and `y + 0.5|x|`. Explain how this visual communicates uncertainty without cluttering the plot.

??? success "Solution to Exercise 5"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 100)
        y = x ** 2
        unc = 0.5 * np.abs(x)

        fig, ax = plt.subplots()
        ax.plot(x, y, 'b-', linewidth=2, label='$y = x^2$')
        ax.fill_between(x, y - unc, y + unc, alpha=0.2, color='blue', label='Uncertainty')
        ax.legend()
        ax.set_title('Function with Confidence Band')
        plt.show()

        # The band shows where the true value might lie. Wide band = high
        # uncertainty, narrow band = precise. This is cleaner than individual
        # error bars and more informative than just the line alone.
        ax.set_title('Random Walk with Rolling Mean and SD Band')
        plt.show()
