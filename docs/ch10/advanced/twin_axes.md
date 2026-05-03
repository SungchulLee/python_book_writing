# Twin Axes

Twin axes allow plotting data with different scales on the same figure.

!!! tip "Mental Model"
    `ax.twinx()` creates a second invisible Axes layered on top of the first, sharing the same x-axis but with its own independent y-axis on the right. Each Axes has its own scale, so you can plot temperature on the left and precipitation on the right. Color-code the lines to match their respective y-axis labels for clarity.

!!! warning "Twin Axes Can Mislead"
    Twin axes are powerful but dangerous. Because the two y-scales are independent, it is easy to choose scales that make unrelated variables appear correlated (or mask a real correlation). Always ask: would a reader misinterpret the crossing point of two lines that are on completely different scales? If the answer is yes, consider using two separate subplots instead. Twin axes work best when the two variables have a genuine relationship (e.g., temperature and energy consumption) and the scales are chosen honestly.

---

## twinx()

Create a second y-axis sharing the same x-axis:

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

    DATE = df.index[50:]
    y_price = df['Close'].loc[DATE]
    y_volume = df['Volume'].loc[DATE]

    fig, ax = plt.subplots(figsize=(15, 3))

    # Primary axis: price
    ax.plot(DATE, y_price, label='AAPL', color='b')
    ax.set_ylim([90, 140])
    ax.set_xlabel('DATE')
    ax.set_ylabel('STOCK PRICE')
    ax.set_title('AAPL')

    # Secondary axis: volume
    ax2 = ax.twinx()
    ax2.fill_between(DATE, y_volume, color='gray', alpha=0.3)
    ax2.set_ylim([0.0, 1e9])
    ax2.set_ylabel('VOLUME')

    ax.legend()
    plt.show()

if __name__ == "__main__":
    main()
```

---

## twiny()

Create a second x-axis sharing the same y-axis:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()

ax.plot(x, y, 'b-')
ax.set_xlabel('Radians', color='blue')
ax.tick_params(axis='x', labelcolor='blue')

# Create twin axis for degrees
ax2 = ax.twiny()
ax2.plot(np.degrees(x), y, 'r-', alpha=0)  # Invisible line to set range
ax2.set_xlabel('Degrees', color='red')
ax2.tick_params(axis='x', labelcolor='red')

plt.show()
```

---

## Synchronizing Axes

When using twin axes, ensure they align logically:

```python
import matplotlib.pyplot as plt
import numpy as np

# Temperature conversion example
x = np.linspace(0, 100, 50)
celsius = x
fahrenheit = celsius * 9/5 + 32

fig, ax1 = plt.subplots()

# Celsius axis
ax1.plot(x, celsius, 'b-', label='Celsius')
ax1.set_xlabel('Sample')
ax1.set_ylabel('Temperature (°C)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Fahrenheit axis
ax2 = ax1.twinx()
ax2.plot(x, fahrenheit, 'r-', label='Fahrenheit')
ax2.set_ylabel('Temperature (°F)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

fig.tight_layout()
plt.show()
```

---

## Legend with Twin Axes

Combine legends from both axes:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, ax1 = plt.subplots()

line1, = ax1.plot(x, np.sin(x), 'b-', label='sin(x)')
ax1.set_ylabel('sin(x)', color='blue')

ax2 = ax1.twinx()
line2, = ax2.plot(x, np.exp(x/10), 'r-', label='exp(x/10)')
ax2.set_ylabel('exp(x/10)', color='red')

# Combine legends
lines = [line1, line2]
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left')

plt.show()
```

---

## Three Axes Example

Add a third axis using spine manipulation:

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, ax1 = plt.subplots()
fig.subplots_adjust(right=0.75)

# First y-axis
ax1.plot(x, np.sin(x), 'b-')
ax1.set_ylabel('sin(x)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Second y-axis
ax2 = ax1.twinx()
ax2.plot(x, np.cos(x), 'r-')
ax2.set_ylabel('cos(x)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Third y-axis
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(x, np.tan(x), 'g-')
ax3.set_ylabel('tan(x)', color='green')
ax3.tick_params(axis='y', labelcolor='green')
ax3.set_ylim(-10, 10)

plt.show()
```

---

## Key Takeaways

- `ax.twinx()` creates a second y-axis
- `ax.twiny()` creates a second x-axis
- Color-code axes and labels for clarity
- Combine legends manually when using twin axes
- Adjust spine positions for additional axes

---

## Exercises

**Exercise 1.**
Plot monthly rainfall (in mm) and average temperature (in Celsius) on the same figure using `twinx`. Use bar chart for rainfall on the left y-axis and a line plot for temperature on the right y-axis. Color-code the axes and labels to match each dataset.

??? success "Solution to Exercise 1"

        import matplotlib.pyplot as plt
        import numpy as np

        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        rainfall = [78, 52, 65, 45, 30, 15, 10, 12, 35, 60, 80, 90]
        temperature = [5, 7, 12, 18, 23, 28, 31, 30, 25, 18, 11, 6]

        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.bar(months, rainfall, color='steelblue', alpha=0.7, label='Rainfall')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Rainfall (mm)', color='steelblue')
        ax1.tick_params(axis='y', labelcolor='steelblue')

        ax2 = ax1.twinx()
        ax2.plot(months, temperature, 'o-', color='red', linewidth=2, label='Temperature')
        ax2.set_ylabel('Temperature (°C)', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        ax1.set_title('Monthly Rainfall and Temperature')
        fig.tight_layout()
        plt.show()

---

**Exercise 2.**
Create a figure showing a stock price on the left y-axis and its daily trading volume on the right y-axis using `twinx`. Generate synthetic data: 100 days of prices starting at 100 with random walk increments, and volumes as random integers between 1M and 10M. Combine legends from both axes into a single legend.

??? success "Solution to Exercise 2"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        days = np.arange(100)
        prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
        volumes = np.random.randint(1_000_000, 10_000_000, 100)

        fig, ax1 = plt.subplots(figsize=(12, 6))

        line1, = ax1.plot(days, prices, color='navy', linewidth=1.5, label='Price')
        ax1.set_xlabel('Day')
        ax1.set_ylabel('Price ($)', color='navy')
        ax1.tick_params(axis='y', labelcolor='navy')

        ax2 = ax1.twinx()
        bar1 = ax2.bar(days, volumes, color='lightcoral', alpha=0.4, label='Volume')
        ax2.set_ylabel('Volume', color='lightcoral')
        ax2.tick_params(axis='y', labelcolor='lightcoral')

        lines = [line1, bar1]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left')
        ax1.set_title('Stock Price and Volume')
        fig.tight_layout()
        plt.show()

---

**Exercise 3.**
Use `twiny` to show two different x-axis scales. Plot a function `y = sin(x)` where the bottom x-axis shows `x` in radians ($[0, 2\pi]$) and the top x-axis shows the same range in degrees ($[0, 360]$). Synchronize the two axes so they correspond correctly.

??? success "Solution to Exercise 3"

        import matplotlib.pyplot as plt
        import numpy as np

        x_rad = np.linspace(0, 2 * np.pi, 500)
        y = np.sin(x_rad)

        fig, ax1 = plt.subplots(figsize=(10, 5))
        ax1.plot(x_rad, y, color='purple', linewidth=2)
        ax1.set_xlabel('x (radians)')
        ax1.set_ylabel('sin(x)')
        ax1.set_xlim(0, 2 * np.pi)

        ax2 = ax1.twiny()
        ax2.set_xlim(0, 360)
        ax2.set_xlabel('x (degrees)')

        ax1.set_title('sin(x) with Radian and Degree Axes', pad=30)
        plt.show()

---

**Exercise 4.**
Create a twin-axis plot showing monthly sales revenue (left y-axis, in thousands) and customer count (right y-axis). Use bar chart for revenue and line plot for customers. Color-code each y-axis label to match its data. Add a combined legend.

??? success "Solution to Exercise 4"

        import matplotlib.pyplot as plt
        import numpy as np

        months = np.arange(1, 13)
        revenue = np.array([45, 52, 48, 61, 55, 68, 72, 78, 65, 59, 70, 85])
        customers = np.array([120, 135, 128, 150, 142, 165, 180, 195, 170, 155, 175, 210])

        fig, ax1 = plt.subplots(figsize=(10, 5))

        bars = ax1.bar(months, revenue, color='steelblue', alpha=0.7, label='Revenue ($K)')
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Revenue ($K)', color='steelblue')
        ax1.tick_params(axis='y', labelcolor='steelblue')

        ax2 = ax1.twinx()
        line = ax2.plot(months, customers, 'r-o', linewidth=2, label='Customers')
        ax2.set_ylabel('Customers', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        # Combined legend
        lines = [bars, line[0]]
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left')
        ax1.set_title('Monthly Revenue and Customer Growth')
        fig.tight_layout()
        plt.show()

---

**Exercise 5.**
Demonstrate how twin axes can mislead. Plot two unrelated random walks on twin axes and show that their apparent "correlation" is entirely an artifact of scale choice. Then change the y-limits on one axis to make the correlation disappear. Explain the lesson.

??? success "Solution to Exercise 5"

        import matplotlib.pyplot as plt
        import numpy as np

        np.random.seed(42)
        x = np.arange(100)
        series_a = np.cumsum(np.random.randn(100))  # Random walk
        series_b = np.cumsum(np.random.randn(100))  # Independent random walk

        fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(14, 5))

        # Left: misleading — scales chosen to make them look correlated
        ax1.plot(x, series_a, 'b-', label='Series A')
        ax1.set_ylabel('Series A', color='blue')
        ax2 = ax1.twinx()
        ax2.plot(x, series_b, 'r-', label='Series B')
        ax2.set_ylabel('Series B', color='red')
        ax1.set_title('Misleading: looks correlated')

        # Right: honest — same data, wider scale reveals independence
        ax3.plot(x, series_a, 'b-', label='Series A')
        ax3.set_ylabel('Series A', color='blue')
        ax4 = ax3.twinx()
        ax4.plot(x, series_b, 'r-', label='Series B')
        ax4.set_ylabel('Series B', color='red')
        ax4.set_ylim(-30, 30)  # Honest scale
        ax3.set_title('Honest: independence visible')

        plt.tight_layout()
        plt.show()

        # Lesson: twin axes with auto-scaled y-limits will stretch any two
        # time series to fill the same visual space, making them appear
        # correlated regardless of actual relationship. Always ask: "would
        # two subplots tell a different story?" If yes, use subplots.
