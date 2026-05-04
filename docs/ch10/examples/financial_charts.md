# Financial Charts

Create professional financial visualizations with Matplotlib.

!!! tip "Mental Model"
    Financial charts combine multiple plot types on shared time axes: line plots for prices, bar charts for volume, fill_between for ranges, and twin axes for overlaying different scales. The key technique is using `twinx()` to pair price and volume on the same figure without distorting either scale.

!!! warning "Visualization vs Analysis"
    This page demonstrates **plotting techniques**, not trading strategies. Moving
    average crossovers, bullish/bearish shading, and volume overlays are shown as
    Matplotlib patterns — they are not validated signals. In real finance:

    - Moving averages are **lagging indicators** — they react to past data, not future prices
    - Crossover "signals" produce many **false positives** in sideways markets
    - `twinx()` can **visually mislead** by implying correlation between differently scaled axes

    Always apply statistical rigor before interpreting any chart pattern as meaningful.

    Stock prices often resemble **random walks** (see [Brownian Motion](brownian_motion.md)).
    This means visual patterns like crossovers can appear meaningful even when they
    are mostly noise — a moving average crossover on a random walk will produce
    "signals" at exactly the same rate as on real data.

!!! tip "Offline Usage"
    Examples use `yfinance` for real data, but all techniques work equally well
    with synthetic data (`np.cumsum(np.random.randn(250))`) for offline
    development and testing.

---

## Stock Price Chart

Basic price chart with volume:

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

    fig, ax = plt.subplots(figsize=(15, 4))

    ax.plot(DATE, y_price, label='AAPL', color='b')
    ax.set_xlabel('DATE')
    ax.set_ylabel('STOCK PRICE')
    ax.set_title('AAPL')

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

## Moving Average Crossover

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

    fig, ax = plt.subplots(figsize=(15, 4))

    ax.plot(DATE, y, label='AAPL', color='b')
    ax.plot(DATE, y_15, label='MA15', color='g')
    ax.plot(DATE, y_50, label='MA50', color='r')

    ax.fill_between(DATE, y_15, y_50,
                    where=(y_15 > y_50), interpolate=True,
                    color='green', alpha=0.3, label='Bullish')
    ax.fill_between(DATE, y_15, y_50,
                    where=(y_15 <= y_50), interpolate=True,
                    color='red', alpha=0.3, label='Bearish')

    ax.set_xlabel('DATE')
    ax.set_ylabel('STOCK PRICE')
    ax.set_title('AAPL - Moving Average Crossover')
    ax.legend()

    plt.show()

if __name__ == "__main__":
    main()
```

---

## Marking Events

Highlight specific dates on a chart:

```python
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

def download_stock_prices(ticker, start, end):
    return yf.download(ticker, start=start, end=end)

def display_stock_prices(data, ticker, event_date=None):
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.plot(data['Close'], label=ticker)

    if event_date:
        date = pd.to_datetime(event_date)
        ax.plot(date, data.loc[date, 'Close'], 'ro', ms=10)
        ax.annotate(f'{event_date}',
                    xy=(date, data.loc[date, 'Close']),
                    xytext=(date, data.loc[date, 'Close'] + 5),
                    fontsize=10, ha='center',
                    arrowprops=dict(arrowstyle='->', color='red'))

    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.legend()
    plt.show()

def main():
    ticker = 'AAPL'
    data = download_stock_prices(ticker, '2023-01-01', '2024-12-31')
    display_stock_prices(data, ticker, event_date='2023-12-20')

if __name__ == "__main__":
    main()
```

---

## Multi-Asset Comparison

```python
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd

def main():
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    start = '2023-01-01'
    end = '2024-01-01'

    fig, ax = plt.subplots(figsize=(12, 4))

    for ticker in tickers:
        data = yf.download(ticker, start=start, end=end)
        # Normalize to starting price
        normalized = data['Close'] / data['Close'].iloc[0] * 100
        ax.plot(normalized, label=ticker)

    ax.set_xlabel('Date')
    ax.set_ylabel('Normalized Price (Base=100)')
    ax.set_title('Tech Stock Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.show()

if __name__ == "__main__":
    main()
```

---

## Price with Date Formatting

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
import yfinance as yf

def main():
    df = yf.Ticker('AAPL').history(start='2020-07-01', end='2020-12-31')

    fig, ax = plt.subplots(figsize=(15, 4))
    ax.plot(df.index, df['Close'])

    ax.set_xlabel('Date')
    ax.set_ylabel('Close Price')
    ax.set_title('AAPL Stock Price')

    # Format dates
    date_format = mpl_dates.DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(date_format)
    ax.xaxis.set_major_locator(mpl_dates.MonthLocator())

    fig.autofmt_xdate()
    plt.show()

if __name__ == "__main__":
    main()
```

---

## Key Takeaways

- Use `twinx()` for price and volume on same chart
- `fill_between()` visualizes moving average crossovers
- Mark events with `annotate()`
- Normalize prices for multi-asset comparison
- Use `DateFormatter` for proper date display
- `autofmt_xdate()` prevents label overlap


---

## Exercises

**Exercise 1.** Write code that creates a stock price chart with a secondary y-axis for volume using `ax.twinx()`. Use synthetic data: generate 100 dates, a random-walk price series starting at 100, and random volume data.

??? success "Solution to Exercise 1"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    n = 100
    dates = np.arange(n)
    price = 100 + np.cumsum(np.random.randn(n) * 0.5)
    volume = np.random.randint(1000, 5000, n)

    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(dates, price, 'b-', label='Price')
    ax1.set_xlabel('Day')
    ax1.set_ylabel('Price', color='blue')

    ax2 = ax1.twinx()
    ax2.fill_between(dates, volume, color='gray', alpha=0.3, label='Volume')
    ax2.set_ylabel('Volume', color='gray')

    ax1.set_title('Price and Volume Chart')
    ax1.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 2.** Explain the purpose of `fill_between()` in a moving average crossover chart. When is the filled region green versus red?

??? success "Solution to Exercise 2"
    `fill_between()` fills the area between two moving average lines (e.g., a short-term MA and a long-term MA). The filled region is **green** when the short-term MA is above the long-term MA, signaling a **bullish** (upward) trend. The filled region is **red** when the short-term MA is below the long-term MA, signaling a **bearish** (downward) trend. The `where` parameter controls which condition determines the fill, and `interpolate=True` ensures smooth transitions at crossover points.

---

**Exercise 3.** Create a figure that plots three synthetic "stock" series (random walks), normalizes each to start at 100, and plots them on the same axes with a legend. Add appropriate labels and title.

??? success "Solution to Exercise 3"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    n = 200
    days = np.arange(n)

    stocks = {}
    for name in ['Stock A', 'Stock B', 'Stock C']:
        raw = 100 + np.cumsum(np.random.randn(n) * 1.5)
        normalized = raw / raw[0] * 100
        stocks[name] = normalized

    fig, ax = plt.subplots(figsize=(12, 5))
    for name, values in stocks.items():
        ax.plot(days, values, label=name)

    ax.set_xlabel('Day')
    ax.set_ylabel('Normalized Price (Base=100)')
    ax.set_title('Multi-Asset Comparison')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    ```

---

**Exercise 4.** Write code that plots a synthetic price series and marks a specific point on the chart using `ax.annotate()` with an arrow. Add a title and axis labels.

??? success "Solution to Exercise 4"
    ```python
    import matplotlib.pyplot as plt
    import numpy as np

    np.random.seed(42)
    n = 100
    days = np.arange(n)
    price = 100 + np.cumsum(np.random.randn(n) * 0.8)

    event_day = 60
    event_price = price[event_day]

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(days, price, 'b-')

    ax.plot(event_day, event_price, 'ro', markersize=10)
    ax.annotate(f'Event at day {event_day}',
                xy=(event_day, event_price),
                xytext=(event_day + 10, event_price + 3),
                fontsize=10, ha='left',
                arrowprops=dict(arrowstyle='->', color='red'))

    ax.set_xlabel('Day')
    ax.set_ylabel('Price')
    ax.set_title('Price Chart with Annotated Event')
    plt.tight_layout()
    plt.show()
    ```
