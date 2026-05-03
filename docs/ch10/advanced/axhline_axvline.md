# Axhline and Axvline

Add horizontal and vertical reference lines that span the entire axes.

!!! tip "Mental Model"
    `axhline(y)` draws a horizontal line at a fixed y-value, and `axvline(x)` draws a vertical line at a fixed x-value — both stretch edge to edge regardless of axis limits. Use them to mark thresholds, means, or baselines. They are more convenient than `plot()` for reference lines because they automatically span the full plot width or height.

!!! note "Reference Lines Are Not Data"
    Unlike data lines (which come from measurements or computation), reference lines are **interpretation guides** — they add semantic meaning to the plot. A threshold line says "above here is critical," a mean line says "this is the center," and an event line says "this happened here." This distinction matters: reference lines should be styled differently (dashed, muted color, lower zorder) so readers do not confuse them with plotted data.

---

## ax.axhline()

Add a horizontal line across the axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.axhline(0, color='black', linewidth=0.5)
ax.axhline(0.5, color='red', linestyle='--', label='y=0.5')
ax.axhline(-0.5, color='blue', linestyle='--', label='y=-0.5')
ax.legend()
plt.show()
```

---

## axhline Parameters

```python
ax.axhline(
    y=0,              # Y position of the line
    xmin=0,           # Starting x position (0-1, axes fraction)
    xmax=1,           # Ending x position (0-1, axes fraction)
    color='black',    # Line color
    linestyle='-',    # Line style
    linewidth=1,      # Line width
    alpha=1.0,        # Transparency
    label='label'     # For legend
)
```

---

## ax.axvline()

Add a vertical line across the axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-np.pi, np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)
ax.axvline(0, color='black', linewidth=0.5)
ax.axvline(np.pi/2, color='red', linestyle='--', label='x=π/2')
ax.axvline(-np.pi/2, color='blue', linestyle='--', label='x=-π/2')
ax.legend()
plt.show()
```

---

## axvline Parameters

```python
ax.axvline(
    x=0,              # X position of the line
    ymin=0,           # Starting y position (0-1, axes fraction)
    ymax=1,           # Ending y position (0-1, axes fraction)
    color='black',    # Line color
    linestyle='-',    # Line style
    linewidth=1,      # Line width
    alpha=1.0,        # Transparency
    label='label'     # For legend
)
```

---

## Partial Lines

Draw lines that don't span the entire axes:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Full width horizontal line
ax.axhline(5, color='blue', label='Full width')

# Partial horizontal line (30% to 70% of axes width)
ax.axhline(3, xmin=0.3, xmax=0.7, color='red', linewidth=2, label='Partial')

plt.legend()
plt.show()
```

---

## Mean and Threshold Lines

Common use case for statistical visualization:

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
data = np.random.normal(100, 15, 200)
x = range(len(data))

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(x, data, 'b-', alpha=0.7)

# Mean line
mean = np.mean(data)
ax.axhline(mean, color='green', linestyle='-', linewidth=2, label=f'Mean: {mean:.1f}')

# Standard deviation bands
std = np.std(data)
ax.axhline(mean + std, color='orange', linestyle='--', label=f'+1σ: {mean+std:.1f}')
ax.axhline(mean - std, color='orange', linestyle='--', label=f'-1σ: {mean-std:.1f}')

ax.axhline(mean + 2*std, color='red', linestyle=':', label=f'+2σ: {mean+2*std:.1f}')
ax.axhline(mean - 2*std, color='red', linestyle=':', label=f'-2σ: {mean-2*std:.1f}')

ax.legend(loc='upper right')
ax.set_title('Process Control Chart')
plt.show()
```

---

## Event Markers

Mark specific events with vertical lines:

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Sample stock-like data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=100, freq='D')
prices = 100 + np.cumsum(np.random.randn(100))

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(dates, prices)

# Mark earnings dates
earnings_dates = [dates[25], dates[55], dates[85]]
for date in earnings_dates:
    ax.axvline(date, color='red', linestyle='--', alpha=0.7)

ax.set_title('Stock Price with Earnings Dates')
plt.show()
```

---

## ax.hlines() and ax.vlines()

For lines at specific data coordinates (not axes fractions):

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)

# Horizontal line from x=2 to x=8 at y=0.5
ax.hlines(y=0.5, xmin=2, xmax=8, color='red', linewidth=2)

# Vertical line from y=-0.5 to y=0.5 at x=5
ax.vlines(x=5, ymin=-0.5, ymax=0.5, color='green', linewidth=2)

plt.show()
```

---

## Key Takeaways

- `axhline` adds horizontal lines spanning the axes
- `axvline` adds vertical lines spanning the axes
- `xmin/xmax` and `ymin/ymax` control partial line extent (0-1 range)
- Use for reference lines, thresholds, and event markers
- `hlines` and `vlines` use data coordinates for extent

---

## Exercises

**Exercise 1.**
Plot the function `y = sin(x)` for `x` in $[0, 4\pi]$, then add a horizontal dashed line at `y = 0` in gray and two horizontal lines at `y = 0.5` (green) and `y = -0.5` (red). These represent upper and lower thresholds. Add a legend identifying each line.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 4 * np.pi, 500)
        y = np.sin(x)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, label='sin(x)')
        ax.axhline(y=0, color='gray', linestyle='--', label='y = 0')
        ax.axhline(y=0.5, color='green', linestyle='-', label='Upper threshold')
        ax.axhline(y=-0.5, color='red', linestyle='-', label='Lower threshold')
        ax.legend()
        ax.set_title('Sine Wave with Thresholds')
        plt.show()

---

**Exercise 2.**
Generate 100 random samples from a standard normal distribution and plot them as a line. Add a vertical line at the index of the maximum value (red) and the minimum value (blue). Also add a horizontal line at the mean value (green, dashed). Use `ax.text` to label the max and min values near their respective vertical lines.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        data = np.random.randn(100)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(data, color='steelblue')

        max_idx = np.argmax(data)
        min_idx = np.argmin(data)
        mean_val = data.mean()

        ax.axvline(x=max_idx, color='red', linestyle='-', label='Max')
        ax.axvline(x=min_idx, color='blue', linestyle='-', label='Min')
        ax.axhline(y=mean_val, color='green', linestyle='--', label='Mean')

        ax.text(max_idx + 1, data[max_idx], f'{data[max_idx]:.2f}', color='red')
        ax.text(min_idx + 1, data[min_idx], f'{data[min_idx]:.2f}', color='blue')

        ax.legend()
        ax.set_title('Random Data with Max, Min, and Mean')
        plt.show()

---

**Exercise 3.**
Create a plot of `y = x^2` for `x` in $[-3, 3]$. Use `axvspan` to shade the region between `x = -1` and `x = 1` in light yellow, and use `axhline` to mark the minimum value at `y = 0`. Add `axvline` at `x = -1` and `x = 1` with dashed linestyle to show the boundaries of the shaded region.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-3, 3, 200)
        y = x ** 2

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.plot(x, y, color='navy', linewidth=2)

        ax.axvspan(-1, 1, color='lightyellow', alpha=0.8, label='Region [-1, 1]')
        ax.axhline(y=0, color='green', linestyle='-', linewidth=1)
        ax.axvline(x=-1, color='gray', linestyle='--')
        ax.axvline(x=1, color='gray', linestyle='--')

        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_title(r'$y = x^2$ with Highlighted Region')
        ax.legend()
        plt.show()

---

**Exercise 4.**
Plot a time series of 100 random values simulating daily temperatures. Add `axhline` for the mean (solid green) and mean ± 1 standard deviation (dashed red). Use `axhspan` to shade the region between the two SD lines in light red. Explain how these reference elements help a reader interpret the data without reading values.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        temps = np.random.randn(100) * 5 + 20

        fig, ax = plt.subplots()
        ax.plot(temps, color='black', alpha=0.7)

        mu, sigma = temps.mean(), temps.std()
        ax.axhline(mu, color='green', linestyle='-', label=f'Mean ({mu:.1f})')
        ax.axhline(mu + sigma, color='red', linestyle='--', label=f'+1 SD')
        ax.axhline(mu - sigma, color='red', linestyle='--', label=f'-1 SD')
        ax.axhspan(mu - sigma, mu + sigma, alpha=0.1, color='red')

        ax.legend()
        ax.set_title('Daily Temperature with Reference Lines')
        plt.show()

        # The reference lines act as semantic anchors: the green line says
        # "this is normal," the red band says "68% of data falls here,"
        # and points outside the band are unusual — readable at a glance.

---

**Exercise 5.**
A colleague marks an event time on a plot using `ax.plot([5, 5], [-1, 1], 'r--')`. Explain why `axvline(5)` is better. Demonstrate the problem: change `ylim` after plotting and show the manual line no longer spans the full height.

??? success "Solution to Exercise 5"

        import matplotlib.pyplot as plt
        import numpy as np

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        x = np.linspace(0, 10, 100)
        y = np.sin(x)

        ax1.plot(x, y)
        ax1.plot([5, 5], [-1, 1], 'r--', label='manual line')
        ax1.set_ylim(-2, 2)
        ax1.set_title('Manual line (broken on resize)')
        ax1.legend()

        ax2.plot(x, y)
        ax2.axvline(5, color='r', linestyle='--', label='axvline')
        ax2.set_ylim(-2, 2)
        ax2.set_title('axvline (always spans full height)')
        ax2.legend()

        plt.tight_layout()
        plt.show()
        # axvline uses axes-relative coordinates (0 to 1) for vertical span
