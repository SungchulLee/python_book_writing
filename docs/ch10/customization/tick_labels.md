# Tick Labels

Customize how tick labels appear on your axes.

!!! tip "Mental Model"
    Tick labels are the text strings displayed at each tick mark. By default, Matplotlib formats numbers automatically, but you can override them with custom strings (e.g., month names), rotate them for readability, or use `FuncFormatter` for computed labels. Always set tick positions with `set_xticks` before setting tick labels with `set_xticklabels` to keep them aligned.

---

## set_xticklabels and set_yticklabels

Set custom text for tick labels:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 100)
y = np.sin(x)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(x, y)

ax.set_xticks((-2*np.pi, -np.pi, 0, np.pi, 2*np.pi))
ax.set_yticks((-1, 0, 1))
ax.set_xticklabels(("-2$\\pi$", "-$\\pi$", "0", "$\\pi$", "2$\\pi$"))
ax.set_yticklabels(("-1", "0", "1"))

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_position("zero")
ax.spines["left"].set_position("zero")

plt.show()
```

---

## Getting Current Labels

```python
print(ax.get_xticklabels())
print(ax.get_yticklabels())
```

Returns a list of `Text` objects.

---

## Rotating Labels

Rotate labels to prevent overlap:

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Generate time series data
np.random.seed(0)
error = np.random.normal(size=(400,))
index = pd.date_range(start='2019-09-01', end='2020-01-01', freq='D')

mu = 50
data = [mu + 0.4*error[t-1] + 0.3*error[t-2] + error[t] 
        for t in range(2, len(index)+2)]
s = pd.Series(data, index)

fig, ax = plt.subplots(figsize=(12, 3))
ax.plot(s)
ax.axhline(mu, linestyle='--', color='grey')

# Rotate and align labels
for label in ax.get_xticklabels():
    label.set_horizontalalignment("right")
    label.set_rotation(45)

plt.show()
```

---

## Text Object Properties

Each tick label is a `Text` object with many properties:

```python
for label in ax.get_xticklabels():
    print(type(label))  # <class 'matplotlib.text.Text'>
```

Common Text methods:

- `set_rotation(angle)`: Rotate the text
- `set_horizontalalignment(align)`: 'left', 'center', 'right'
- `set_verticalalignment(align)`: 'top', 'center', 'bottom', 'baseline'
- `set_fontsize(size)`: Set font size
- `set_color(color)`: Set text color
- `set_bbox(dict)`: Add background box

---

## Adding Background to Labels

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-10, 10, 500)
y = np.sin(x) / x

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, linewidth=2)

# Move spines to origin
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.spines['bottom'].set_position(('data', 0))
ax.spines['left'].set_position(('data', 0))

ax.set_xticks([-10, -5, 5, 10])
ax.set_yticks([0.5, 1])

# Add white background to labels
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_bbox({'facecolor': 'white', 'edgecolor': 'white'})

plt.show()
```

---

## Using tick_params for Styling

Bulk styling of tick labels:

```python
ax.tick_params(
    axis='x',
    labelsize=12,
    labelrotation=45,
    labelcolor='blue'
)

ax.tick_params(
    axis='y', 
    labelsize=10,
    labelcolor='green'
)
```

---

## Categorical Labels

For bar charts or categorical data:

```python
import matplotlib.pyplot as plt

categories = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
values = [10, 25, 15, 30, 20]

fig, ax = plt.subplots()
ax.bar(range(len(categories)), values)
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories)
plt.show()
```

---

## Hiding Tick Labels

Keep ticks but hide labels:

```python
ax.tick_params(labelbottom=False)  # Hide x-axis labels
ax.tick_params(labelleft=False)    # Hide y-axis labels
```

Or set empty labels:

```python
ax.set_xticklabels([])
```

---

## Key Takeaways

- `set_xticklabels()` and `set_yticklabels()` set custom label text
- Each label is a `Text` object with full formatting control
- Use `set_rotation()` and `set_horizontalalignment()` for angled labels
- `set_bbox()` adds a background to labels
- `tick_params()` provides bulk styling options

---

## Exercises

**Exercise 1.**
Plot monthly revenue data and format the y-axis tick labels as currency (e.g., "\$10K", "\$20K") using `FuncFormatter`. Use months `['Jan', 'Feb', ..., 'Dec']` as x-tick labels rotated 45 degrees, and values in thousands like `[12, 15, 18, 22, 19, 25, 28, 30, 27, 24, 20, 35]`.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        revenue = [12, 15, 18, 22, 19, 25, 28, 30, 27, 24, 20, 35]

        def currency_fmt(x, pos):
            return f'${x:.0f}K'

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(months, revenue, color='steelblue')
        ax.yaxis.set_major_formatter(FuncFormatter(currency_fmt))
        ax.tick_params(axis='x', rotation=45)
        ax.set_title('Monthly Revenue')
        plt.tight_layout()
        plt.show()

---

**Exercise 2.**
Create a plot of `y = sin(x)` for `x` in $[0, 2\pi]$ and use `FixedLocator` to place x-ticks at `[0, pi/4, pi/2, 3pi/4, pi, 5pi/4, 3pi/2, 7pi/4, 2pi]`. Format the labels as fractions of $\pi$ (e.g., "$\pi/4$", "$\pi/2$", "$3\pi/4$").

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np
        from matplotlib.ticker import FixedLocator

        x = np.linspace(0, 2 * np.pi, 500)
        y = np.sin(x)

        tick_positions = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi,
                          5*np.pi/4, 3*np.pi/2, 7*np.pi/4, 2*np.pi]
        tick_labels = [r'$0$', r'$\pi/4$', r'$\pi/2$', r'$3\pi/4$', r'$\pi$',
                       r'$5\pi/4$', r'$3\pi/2$', r'$7\pi/4$', r'$2\pi$']

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y)
        ax.xaxis.set_major_locator(FixedLocator(tick_positions))
        ax.set_xticklabels(tick_labels)
        ax.set_title(r'$\sin(x)$ with Fractional $\pi$ Labels')
        ax.grid(True, alpha=0.3)
        plt.show()

---

**Exercise 3.**
Generate a time series of 365 daily data points and format the x-axis using `mdates.DateFormatter('%b %Y')` for month-year labels and `mdates.MonthLocator()` for monthly ticks. Rotate labels 30 degrees and add minor ticks at weekly intervals.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        import numpy as np
        import pandas as pd

        np.random.seed(42)
        dates = pd.date_range('2024-01-01', periods=365, freq='D')
        values = np.cumsum(np.random.randn(365)) + 100

        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(dates, values, color='steelblue', linewidth=1)

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_minor_locator(mdates.WeekdayLocator())

        ax.tick_params(axis='x', rotation=30)
        ax.set_title('Daily Time Series')
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
