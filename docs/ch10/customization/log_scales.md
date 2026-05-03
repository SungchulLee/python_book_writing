# Logarithmic Scales

Logarithmic scales compress large ranges of data, making patterns visible across multiple orders of magnitude.

!!! tip "Mental Model"
    A log scale replaces equal spacing with equal ratios: each tick mark is 10x (or 2x, etc.) the previous one. This turns exponential growth into straight lines and makes patterns across orders of magnitude visible. Use `ax.set_yscale('log')` when your data spans several powers of ten and small values are getting crushed against zero.

## Setting Log Scale

### Using set_xscale / set_yscale

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 100, 100)
y = x ** 2

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_yscale('log')  # Log scale on y-axis
ax.set_xlabel('x')
ax.set_ylabel('y (log scale)')
plt.show()
```

### Log-Log Plot

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_title('Log-Log Plot')
plt.show()
```

### Semi-Log Plots

```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

# Semilog-y: log y-axis, linear x-axis
ax1.semilogy(x, y)
ax1.set_title('semilogy')

# Semilog-x: log x-axis, linear y-axis  
ax2.semilogx(x, y)
ax2.set_title('semilogx')

plt.tight_layout()
plt.show()
```

### Using loglog

```python
fig, ax = plt.subplots()
ax.loglog(x, y)  # Both axes logarithmic
ax.set_title('loglog')
plt.show()
```

## Comparison: Linear vs Log Scale

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0.1, 100, 200)
y = np.exp(x / 10)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Linear scale
ax1.plot(x, y)
ax1.set_title('Linear Scale')
ax1.set_xlabel('x')
ax1.set_ylabel('exp(x/10)')

# Log scale
ax2.plot(x, y)
ax2.set_yscale('log')
ax2.set_title('Logarithmic Y Scale')
ax2.set_xlabel('x')
ax2.set_ylabel('exp(x/10) - log scale')

plt.tight_layout()
plt.show()
```

## Log Scale Bases

### Default Base 10

```python
ax.set_yscale('log')  # Base 10
```

### Base 2 (Binary)

```python
ax.set_yscale('log', base=2)
```

### Natural Log (Base e)

```python
ax.set_yscale('log', base=np.e)
```

### Custom Base

```python
ax.set_yscale('log', base=5)
```

## Handling Negative and Zero Values

Log scales cannot display zero or negative values directly.

### Symmetric Log (symlog)

For data that spans positive and negative values:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-100, 100, 500)
y = x ** 3

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

# Linear (for comparison)
ax1.plot(x, y)
ax1.set_title('Linear Scale')

# Symmetric log
ax2.plot(x, y)
ax2.set_yscale('symlog', linthresh=100)  # Linear within ±linthresh
ax2.set_title('Symmetric Log Scale')

plt.tight_layout()
plt.show()
```

### symlog Parameters

```python
ax.set_yscale('symlog', 
              linthresh=1,    # Range around zero treated as linear
              linscale=0.5,   # Stretch factor for linear region
              base=10)        # Log base
```

### Using logit for Probabilities

For data between 0 and 1:

```python
x = np.linspace(0.01, 0.99, 100)
y = x  # Identity for demonstration

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xscale('logit')
ax.set_title('Logit Scale (for probabilities)')
plt.show()
```

## Tick Formatting

### Default Log Ticks

```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_yscale('log')
# Shows: 10^0, 10^1, 10^2, etc.
```

### Custom Tick Locations

```python
from matplotlib.ticker import LogLocator

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_yscale('log')

# Major ticks at powers of 10
ax.yaxis.set_major_locator(LogLocator(base=10, numticks=10))

plt.show()
```

### Scientific Notation

```python
from matplotlib.ticker import LogFormatterSciNotation

ax.yaxis.set_major_formatter(LogFormatterSciNotation())
```

### Custom Format

```python
from matplotlib.ticker import FuncFormatter

def log_format(x, pos):
    if x >= 1e6:
        return f'{x/1e6:.0f}M'
    elif x >= 1e3:
        return f'{x/1e3:.0f}K'
    else:
        return f'{x:.0f}'

ax.yaxis.set_major_formatter(FuncFormatter(log_format))
```

## Practical Examples

### 1. Exponential Growth

```python
import matplotlib.pyplot as plt
import numpy as np

# Population growth
years = np.arange(1800, 2025, 25)
population = [1, 1.2, 1.4, 1.65, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0]  # billions

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.plot(years, population, 'o-')
ax1.set_title('World Population (Linear)')
ax1.set_ylabel('Population (billions)')

ax2.plot(years, population, 'o-')
ax2.set_yscale('log')
ax2.set_title('World Population (Log Scale)')
ax2.set_ylabel('Population (billions)')

for ax in [ax1, ax2]:
    ax.set_xlabel('Year')
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 2. Power Law Distributions

```python
import matplotlib.pyplot as plt
import numpy as np

# Zipf's law example (word frequencies)
rank = np.arange(1, 101)
frequency = 1000 / rank ** 1.07

fig, ax = plt.subplots()
ax.loglog(rank, frequency, 'o-', markersize=4)
ax.set_xlabel('Rank')
ax.set_ylabel('Frequency')
ax.set_title("Power Law Distribution (Zipf's Law)")
ax.grid(True, alpha=0.3)
plt.show()
```

### 3. Frequency Response

```python
import matplotlib.pyplot as plt
import numpy as np

# Bode plot style
freq = np.logspace(0, 4, 100)  # 1 Hz to 10 kHz
gain = 1 / np.sqrt(1 + (freq / 1000) ** 2)  # Low-pass filter
gain_db = 20 * np.log10(gain)

fig, ax = plt.subplots()
ax.semilogx(freq, gain_db)
ax.set_xlabel('Frequency (Hz)')
ax.set_ylabel('Gain (dB)')
ax.set_title('Frequency Response (Bode Plot)')
ax.grid(True, which='both', alpha=0.3)
ax.axhline(-3, color='red', linestyle='--', label='-3 dB cutoff')
ax.legend()
plt.show()
```

### 4. Financial Returns

```python
import matplotlib.pyplot as plt
import numpy as np

# Compound growth
years = np.arange(0, 31)
returns = {'7% Annual': 1.07 ** years * 1000,
           '10% Annual': 1.10 ** years * 1000,
           '15% Annual': 1.15 ** years * 1000}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

for label, values in returns.items():
    ax1.plot(years, values, label=label)
    ax2.plot(years, values, label=label)

ax1.set_title('Investment Growth (Linear)')
ax2.set_title('Investment Growth (Log Scale)')
ax2.set_yscale('log')

for ax in [ax1, ax2]:
    ax.set_xlabel('Years')
    ax.set_ylabel('Value ($)')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
```

### 5. Scatter Plot with Log Scales

```python
import matplotlib.pyplot as plt
import numpy as np

# Data spanning many orders of magnitude
np.random.seed(42)
x = 10 ** (np.random.rand(100) * 4)  # 1 to 10000
y = x * (0.5 + np.random.rand(100))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.scatter(x, y, alpha=0.6)
ax1.set_title('Linear Scale')
ax1.set_xlabel('x')
ax1.set_ylabel('y')

ax2.scatter(x, y, alpha=0.6)
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_title('Log-Log Scale')
ax2.set_xlabel('x (log)')
ax2.set_ylabel('y (log)')

plt.tight_layout()
plt.show()
```

### 6. Histograms with Log Scale

```python
import matplotlib.pyplot as plt
import numpy as np

# Log-normal distribution
data = np.random.lognormal(0, 1, 10000)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

ax1.hist(data, bins=50, edgecolor='black', alpha=0.7)
ax1.set_title('Linear Scale')
ax1.set_xlabel('Value')

# Log scale on x-axis
ax2.hist(data, bins=np.logspace(-2, 2, 50), edgecolor='black', alpha=0.7)
ax2.set_xscale('log')
ax2.set_title('Log Scale (X-axis)')
ax2.set_xlabel('Value (log)')

plt.tight_layout()
plt.show()
```

## Grid Lines on Log Scale

### Major and Minor Grid

```python
fig, ax = plt.subplots()
ax.loglog(x, y)

# Major grid (powers of 10)
ax.grid(True, which='major', linestyle='-', alpha=0.7)

# Minor grid (subdivisions)
ax.grid(True, which='minor', linestyle=':', alpha=0.4)

plt.show()
```

### Minor Ticks

```python
from matplotlib.ticker import LogLocator, NullFormatter

fig, ax = plt.subplots()
ax.loglog(x, y)

# Add minor ticks
ax.yaxis.set_minor_locator(LogLocator(subs=np.arange(2, 10)))
ax.xaxis.set_minor_locator(LogLocator(subs=np.arange(2, 10)))

# Hide minor tick labels
ax.yaxis.set_minor_formatter(NullFormatter())
ax.xaxis.set_minor_formatter(NullFormatter())

ax.grid(True, which='both', alpha=0.3)
plt.show()
```

## Scale Types Summary

| Scale | Function | Use Case |
|-------|----------|----------|
| `'linear'` | Default | Normal data |
| `'log'` | Logarithmic | Exponential growth, wide range |
| `'symlog'` | Symmetric log | Data with positive and negative |
| `'logit'` | Logit | Probabilities (0 to 1) |
| `'asinh'` | Inverse hyperbolic sine | Like symlog, smoother |

## Common Pitfalls

### 1. Zero or Negative Values

```python
# This will cause issues:
y = np.array([0, 1, 10, 100])
ax.set_yscale('log')  # Warning: zero cannot be displayed

# Solution: filter or offset
y = np.array([0.1, 1, 10, 100])  # Replace 0 with small value
```

### 2. Axis Limits with Log Scale

```python
# Must set positive limits
ax.set_ylim(0.1, 1000)  # Correct
# ax.set_ylim(0, 1000)  # Wrong: 0 is invalid
```

### 3. Log Bins for Histograms

```python
# Use logarithmically spaced bins
bins = np.logspace(np.log10(data.min()), np.log10(data.max()), 50)
ax.hist(data, bins=bins)
ax.set_xscale('log')
```

## The Deeper Meaning of Scale Choice

Changing the scale is not just a visual preference --- it changes the **geometry** of your data:

```text
Linear scale → equal spacing = equal differences (additive structure)
Log scale    → equal spacing = equal ratios     (multiplicative structure)
```

This is why exponential growth becomes a straight line on a log scale: growth by a constant *factor* (multiplicative) maps to growth by a constant *step* (additive) in log space. Choosing the right scale reveals the natural structure of your data.

---

## Exercises

**Exercise 1.**
Plot the function $y = x^3$ for `x` in $[1, 1000]$ using four scale combinations in a 2x2 grid: linear-linear, log-linear (log x, linear y), linear-log (linear x, log y), and log-log. Title each subplot with its scale type.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(1, 1000, 500)
        y = x ** 3

        fig, axes = plt.subplots(2, 2, figsize=(10, 8))

        axes[0, 0].plot(x, y)
        axes[0, 0].set_title('Linear-Linear')

        axes[0, 1].plot(x, y)
        axes[0, 1].set_xscale('log')
        axes[0, 1].set_title('Log-Linear')

        axes[1, 0].plot(x, y)
        axes[1, 0].set_yscale('log')
        axes[1, 0].set_title('Linear-Log')

        axes[1, 1].plot(x, y)
        axes[1, 1].set_xscale('log')
        axes[1, 1].set_yscale('log')
        axes[1, 1].set_title('Log-Log')

        for ax in axes.flat:
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Create a semilogy plot of three exponential decays: $y = e^{-x}$, $y = e^{-2x}$, and $y = e^{-3x}$ for `x` in $[0, 5]$. On a log scale y-axis, these should appear as straight lines. Add a legend and grid.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(0, 5, 200)

        fig, ax = plt.subplots(figsize=(8, 5))
        for k in [1, 2, 3]:
            ax.semilogy(x, np.exp(-k * x), label=f'exp(-{k}x)')

        ax.set_xlabel('x')
        ax.set_ylabel('y (log scale)')
        ax.set_title('Exponential Decays on Semilogy')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.show()

---

**Exercise 3.**
Use `ax.set_xscale('symlog', linthresh=1)` to plot the function $y = x^3$ over $[-100, 100]$. The symmetric log scale handles both positive and negative values. Compare this with a standard linear plot side by side, and shade the linear region $[-1, 1]$ with `axvspan`.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x = np.linspace(-100, 100, 1000)
        y = x ** 3

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        ax1.plot(x, y, color='navy')
        ax1.set_title('Linear Scale')
        ax1.set_xlabel('x')
        ax1.set_ylabel(r'$x^3$')
        ax1.grid(True, alpha=0.3)

        ax2.plot(x, y, color='navy')
        ax2.set_xscale('symlog', linthresh=1)
        ax2.set_title('Symmetric Log Scale (linthresh=1)')
        ax2.set_xlabel('x (symlog)')
        ax2.set_ylabel(r'$x^3$')
        ax2.axvspan(-1, 1, color='yellow', alpha=0.3, label='Linear region')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()
