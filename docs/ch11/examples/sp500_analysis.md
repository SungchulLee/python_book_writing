# SP500 Analysis

A comprehensive example demonstrating pandas operations for analyzing S&P 500 stock data.

!!! tip "Mental Model"
    This example ties together the full pandas workflow: download data, inspect it, filter and group, compute statistics, and visualize results. Think of it as a capstone that shows how individual pandas verbs chain together into a real analysis pipeline, with an OOP wrapper for reusability.

## SP500 Class Design

Build a class to download and analyze S&P 500 data.

### 1. Class Structure

```python
import pandas as pd
import yfinance as yf

class SP500:
    """
    Class to download SP500 companies' fundamental and stock price data.
    """

    def __init__(self):
        self.tickers = []
        self.data = pd.DataFrame()
        self.price_data = pd.DataFrame()
        self.fundamental_data = pd.DataFrame()
```

### 2. Fetch Tickers

```python
    def fetch_sp500_tickers(self):
        table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        self.tickers = table[0]['Symbol'].tolist()
        # Adjust ticker symbols if needed
        self.tickers = [ticker.replace('.', '-') for ticker in self.tickers]
```

### 3. Fetch Data

```python
    def fetch_data(self):
        infos = []
        closes = []

        for ticker in self.tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                df = stock.history(period='1y')
                closes.append(df[['Close']].rename(columns={'Close': ticker}))
                infos.append({
                    'Ticker': ticker,
                    'PER (Trailing)': info.get('trailingPE'),
                    'PBR': info.get('priceToBook'),
                    'Market Cap': info.get('marketCap')
                })
            except Exception as e:
                print(f"Failed to fetch {ticker}: {e}")
                continue

        self.price_data = pd.concat(closes, axis=1)
        self.fundamental_data = pd.DataFrame(infos)
```

## Data Merging

Combine price and fundamental data.

### 1. Merge Method

```python
    def merge_data(self):
        self.data = self.fundamental_data.set_index('Ticker').join(
            self.price_data.transpose(),
            how='left'
        )
```

### 2. Get Data

```python
    def get_data(self):
        return self.data
```

### 3. Usage Example

```python
# Example Usage
sp500 = SP500()
sp500.fetch_sp500_tickers()
sp500.fetch_data()
sp500.merge_data()
data = sp500.get_data()
print(data.head())
```

## Analysis Operations

Common analysis patterns with the data.

### 1. Filter by Sector

```python
# Assuming sector data is available
finance_df = data[data['Sector'] == 'Finance']
```

### 2. Group Statistics

```python
sector_stats = data.groupby('Sector').agg({
    'Market Cap': 'sum',
    'PER (Trailing)': 'mean',
    'PBR': ['mean', 'std']
})
```

### 3. Top Performers

```python
# Top 10 by market cap
top_10 = data.nlargest(10, 'Market Cap')
```

## Visualization Integration

Combine pandas with matplotlib.

### 1. Sector Distribution

```python
import matplotlib.pyplot as plt

sector_caps = data.groupby('Sector')['Market Cap'].sum()
sector_caps.plot(kind='bar', figsize=(12, 6))
plt.title('Market Cap by Sector')
plt.ylabel('Market Cap ($)')
plt.show()
```

### 2. Price Correlation

```python
# Correlation matrix of prices
price_corr = sp500.price_data.corr()
```

### 3. Returns Analysis

```python
returns = sp500.price_data.pct_change()
returns.mean().nlargest(10).plot(kind='bar')
plt.title('Top 10 Average Daily Returns')
plt.show()
```

## Best Practices

Guidelines for large-scale data analysis.

### 1. Error Handling

```python
# Always handle API errors gracefully
try:
    data = yf.download(ticker)
except Exception as e:
    print(f"Error: {e}")
```

### 2. Incremental Loading

```python
# For large datasets, process in batches
batch_size = 50
for i in range(0, len(tickers), batch_size):
    batch = tickers[i:i+batch_size]
    # Process batch
```

### 3. Caching Results

```python
# Save intermediate results
data.to_pickle('sp500_data.pkl')
# Load later
data = pd.read_pickle('sp500_data.pkl')
```


---

## Exercises

**Exercise 1.** Write code that creates a DataFrame of stock prices (date, close) and computes the 20-day and 50-day rolling means.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'salary': [70000, 80000, 60000, 90000],
        'department': ['IT', 'IT', 'HR', 'HR']
    })
    result = df.groupby('department')['salary'].max()
    print(result)
    ```

---

**Exercise 2.** Explain how to compute daily returns from a price series using `pct_change()`. Write code demonstrating this.

??? success "Solution to Exercise 2"
    See the main content for the relevant patterns and API calls. The solution involves understanding how to combine Pandas operations to solve data manipulation problems.

---

**Exercise 3.** Write code that resamples daily stock data to monthly frequency, taking the last close price of each month.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({
        'value': np.random.randint(0, 100, 20),
        'group': np.random.choice(['A', 'B'], 20)
    })
    result = df.groupby('group')['value'].transform('sum')
    print(result)
    ```

---

**Exercise 4.** Create a function that takes a price DataFrame and returns the maximum drawdown (largest peak-to-trough decline).

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    s = pd.Series(np.random.randn(100))
    s_clean = s.clip(lower=0)
    print(s_clean.describe())
    ```
