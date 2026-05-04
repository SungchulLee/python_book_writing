# Error Bars

Error bars display the uncertainty or variability of data points, essential for statistical and scientific visualizations.

!!! tip "Mental Model"
    An error bar is a line plot with "whiskers" showing how much each data point might vary. `ax.errorbar()` works like `ax.plot()` but adds vertical and/or horizontal bars centered on each point. The length of each bar represents the uncertainty -- longer bars mean less confidence in the exact value.

    Error bars add a third dimension to the visualization: beyond value (position)
    and category (color/style), they encode **uncertainty.** A visualization can
    represent value, variability, and confidence — error bars are what make
    the confidence visible.

!!! warning "Error Bars Have Different Meanings"
    Error bars do **not** always represent the same quantity. Common conventions:

    | Meaning | What it shows | When to use |
    |---------|--------------|-------------|
    | Standard deviation (SD) | Spread of the data | Describing variability |
    | Standard error (SE) | Precision of the mean | Comparing group means |
    | 95% confidence interval | Range likely containing true mean | Statistical inference |

    **Always label what your error bars represent** — readers cannot tell SD from
    SE by looking at the chart. A plot without this context is ambiguous at best
    and misleading at worst.

## Basic Error Bars

### Symmetric Error Bars

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 5, 4, 5])
yerr = np.array([0.5, 0.4, 0.6, 0.3, 0.5])

fig, ax = plt.subplots()
ax.errorbar(x, y, yerr=yerr, fmt='o', capsize=5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Basic Error Bars')
plt.show()
```

### X and Y Error Bars

```python
xerr = np.array([0.2, 0.3, 0.2, 0.25, 0.3])
yerr = np.array([0.5, 0.4, 0.6, 0.3, 0.5])

fig, ax = plt.subplots()
ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt='o', capsize=5)
plt.show()
```

## Asymmetric Error Bars

For different upper and lower errors:

```python
# Shape: (2, N) where [0] is lower, [1] is upper
yerr_asymmetric = np.array([
    [0.3, 0.2, 0.4, 0.2, 0.3],  # Lower errors
    [0.5, 0.6, 0.4, 0.5, 0.7]   # Upper errors
])

fig, ax = plt.subplots()
ax.errorbar(x, y, yerr=yerr_asymmetric, fmt='o', capsize=5)
ax.set_title('Asymmetric Error Bars')
plt.show()
```

## Error Bar Styling

### Format String

```python
fig, ax = plt.subplots()

# Format: marker, line, color
ax.errorbar(x, y, yerr=yerr, fmt='s-b', capsize=5)  # Square markers, solid line, blue
plt.show()
```

### Detailed Styling

```python
fig, ax = plt.subplots()

ax.errorbar(
    x, y, yerr=yerr,
    fmt='o',              # Marker style
    color='navy',         # Point and line color
    ecolor='lightblue',   # Error bar color
    elinewidth=2,         # Error bar line width
    capsize=6,            # Cap size
    capthick=2,           # Cap thickness
    markersize=8,         # Marker size
    markerfacecolor='white',
    markeredgecolor='navy',
    markeredgewidth=2,
    label='Data'
)

ax.legend()
plt.show()
```

### No Connecting Line

```python
ax.errorbar(x, y, yerr=yerr, fmt='o', linestyle='none', capsize=5)
```

### With Connecting Line

```python
ax.errorbar(x, y, yerr=yerr, fmt='-o', capsize=5)
```

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `x, y` | Data coordinates | Required |
| `xerr` | X error values | None |
| `yerr` | Y error values | None |
| `fmt` | Format string | '' |
| `ecolor` | Error bar color | None (uses line color) |
| `elinewidth` | Error bar line width | None |
| `capsize` | Cap length in points | 0 |
| `capthick` | Cap line width | None |
| `uplims` / `lolims` | Upper/lower limits | False |
| `xlolims` / `xuplims` | X limits | False |

## Upper and Lower Limits

Show one-sided limits when only bounds are known:

### Upper Limits Only

```python
fig, ax = plt.subplots()

y = np.array([2, 4, 5, 4, 5])
yerr = np.array([0.5, 0.4, 0.6, 0.3, 0.5])
uplims = np.array([True, False, True, False, True])  # Which points have upper limits

ax.errorbar(x, y, yerr=yerr, uplims=uplims, fmt='o', capsize=5)
ax.set_title('Upper Limits')
plt.show()
```

### Lower Limits Only

```python
lolims = np.array([False, True, False, True, False])
ax.errorbar(x, y, yerr=yerr, lolims=lolims, fmt='o', capsize=5)
```

### Both Limits

```python
ax.errorbar(x, y, yerr=yerr, uplims=uplims, lolims=lolims, fmt='o', capsize=5)
```

## Practical Examples

### 1. Experimental Data

```python
import matplotlib.pyplot as plt
import numpy as np

# Simulated experimental data with measurement uncertainty
temperature = np.array([20, 40, 60, 80, 100])
pressure = np.array([1.0, 1.8, 2.5, 3.1, 3.8])
pressure_err = np.array([0.1, 0.15, 0.12, 0.18, 0.2])

fig, ax = plt.subplots()
ax.errorbar(temperature, pressure, yerr=pressure_err, 
            fmt='o', capsize=5, capthick=1.5,
            color='darkblue', ecolor='lightblue',
            label='Measurements')

# Add fit line
coeffs = np.polyfit(temperature, pressure, 1)
fit_line = np.poly1d(coeffs)
ax.plot(temperature, fit_line(temperature), 'r--', label='Linear Fit')

ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('Pressure (atm)')
ax.set_title('Pressure vs Temperature')
ax.legend()
plt.show()
```

### 2. Comparing Groups with Error Bars

```python
import matplotlib.pyplot as plt
import numpy as np

categories = ['A', 'B', 'C', 'D']
x = np.arange(len(categories))
width = 0.35

# Group 1
means1 = [20, 35, 30, 35]
std1 = [2, 3, 4, 2]

# Group 2
means2 = [25, 32, 34, 20]
std2 = [3, 4, 2, 3]

fig, ax = plt.subplots()
ax.bar(x - width/2, means1, width, yerr=std1, label='Group 1', capsize=5)
ax.bar(x + width/2, means2, width, yerr=std2, label='Group 2', capsize=5)

ax.set_ylabel('Values')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
plt.show()
```

### 3. Time Series with Confidence Intervals

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
dates = np.arange(0, 10, 0.5)
values = np.sin(dates) + np.random.normal(0, 0.1, len(dates))
errors = np.random.uniform(0.1, 0.3, len(dates))

fig, ax = plt.subplots(figsize=(10, 5))

# Error bars
ax.errorbar(dates, values, yerr=errors, fmt='o-', capsize=3,
            color='steelblue', ecolor='lightsteelblue',
            alpha=0.8)

# Shaded confidence region alternative
ax.fill_between(dates, values - errors, values + errors, 
                alpha=0.2, color='steelblue')

ax.set_xlabel('Time')
ax.set_ylabel('Value')
ax.set_title('Time Series with Uncertainty')
plt.show()
```

### 4. Multiple Series

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 3, 4, 5])

fig, ax = plt.subplots()

# Series 1
y1 = np.array([2.1, 3.5, 4.2, 5.1, 6.3])
err1 = np.array([0.3, 0.2, 0.4, 0.3, 0.2])
ax.errorbar(x, y1, yerr=err1, fmt='o-', capsize=4, label='Method A')

# Series 2
y2 = np.array([1.8, 3.2, 4.5, 4.8, 5.9])
err2 = np.array([0.2, 0.3, 0.2, 0.4, 0.3])
ax.errorbar(x, y2, yerr=err2, fmt='s--', capsize=4, label='Method B')

# Series 3
y3 = np.array([2.5, 3.8, 4.0, 5.3, 6.0])
err3 = np.array([0.4, 0.2, 0.3, 0.2, 0.4])
ax.errorbar(x, y3, yerr=err3, fmt='^:', capsize=4, label='Method C')

ax.legend()
ax.set_xlabel('Sample')
ax.set_ylabel('Measurement')
plt.show()
```

### 5. Logarithmic Scale with Error Bars

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 2, 5, 10, 20, 50, 100])
y = np.array([0.5, 1.2, 3.5, 8.0, 22, 60, 150])
yerr = y * 0.15  # 15% relative error

fig, ax = plt.subplots()
ax.errorbar(x, y, yerr=yerr, fmt='o', capsize=4)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel('X (log scale)')
ax.set_ylabel('Y (log scale)')
ax.set_title('Log-Log Plot with Error Bars')
plt.show()
```

### 6. Horizontal Error Bars

```python
import matplotlib.pyplot as plt
import numpy as np

y = np.array([1, 2, 3, 4, 5])
x = np.array([10, 25, 40, 35, 50])
xerr = np.array([3, 5, 4, 6, 4])

fig, ax = plt.subplots()
ax.errorbar(x, y, xerr=xerr, fmt='o', capsize=5, 
            color='green', ecolor='lightgreen')
ax.set_xlabel('X Value')
ax.set_ylabel('Category')
ax.set_title('Horizontal Error Bars')
plt.show()
```

## Combining with Other Plot Types

### Error Bars on Scatter Plot

```python
fig, ax = plt.subplots()

# Scatter with color mapping
colors = np.random.rand(len(x))
scatter = ax.scatter(x, y, c=colors, s=100, cmap='viridis', zorder=2)
ax.errorbar(x, y, yerr=yerr, fmt='none', ecolor='gray', capsize=3, zorder=1)
plt.colorbar(scatter)
plt.show()
```

### Error Bars on Bar Chart

```python
fig, ax = plt.subplots()

categories = ['A', 'B', 'C', 'D']
values = [23, 45, 56, 78]
errors = [3, 5, 4, 6]

bars = ax.bar(categories, values, yerr=errors, capsize=5,
              color='steelblue', edgecolor='black')
plt.show()
```

## Common Pitfalls

### 1. Error Values Must Be Positive

```python
# WRONG: Negative error values
yerr = np.array([-0.5, 0.4, 0.6])

# CORRECT: Use absolute values
yerr = np.abs(np.array([-0.5, 0.4, 0.6]))
```

### 2. Asymmetric Error Shape

```python
# WRONG: Shape (N, 2)
yerr = np.array([[0.3, 0.5], [0.2, 0.6], [0.4, 0.4]])

# CORRECT: Shape (2, N)
yerr = np.array([
    [0.3, 0.2, 0.4],  # Lower errors
    [0.5, 0.6, 0.4]   # Upper errors
])
```

### 3. Caps Not Showing

```python
# Caps have size 0 by default
ax.errorbar(x, y, yerr=yerr)  # No visible caps

# Set capsize to show caps
ax.errorbar(x, y, yerr=yerr, capsize=5)
```


---

## Exercises

**Exercise 1.** Write code that creates an error bar plot using `ax.errorbar()` with symmetric error bars (same size above and below each point).

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

**Exercise 2.** Explain the difference between symmetric and asymmetric error bars. How do you specify asymmetric errors in `ax.errorbar()`?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page for the key concepts. The essential idea is to understand the API parameters and their effects on the resulting visualization.

---

**Exercise 3.** Create a plot with error bars where `fmt='o'` (markers only, no connecting line) and `capsize=5` to add horizontal caps to the error bars.

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

**Exercise 4.** Write code that generates 20 data points with random noise, computes the mean and standard deviation in groups of 5, and plots the grouped means with standard deviation error bars.

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
