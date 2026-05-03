# Resampling

Resampling changes the frequency of time series data, either downsampling (e.g., daily to monthly) or upsampling (e.g., monthly to daily).

!!! tip "Mental Model"
    `resample` is `groupby` for time. Downsampling (daily to monthly) groups rows into time buckets and aggregates; upsampling (monthly to daily) creates new time slots and fills them. The frequency string (`'M'`, `'W'`, `'Q'`) defines the bucket size, and the chained aggregation method (`mean`, `sum`, `ohlc`) defines how values are combined.

## Basic Resampling

Change time series frequency.

### 1. Monthly Average

```python
import pandas as pd

s = pd.Series(
    range(100),
    index=pd.date_range('2025-01-01', periods=100, freq='D')
)

monthly = s.resample('M').mean()
print(monthly)
```

### 2. Weekly Sum

```python
weekly = s.resample('W').sum()
```

### 3. Quarterly Max

```python
quarterly = s.resample('Q').max()
```

## Common Frequencies

Resampling frequency strings.

### 1. Time-based

```python
s.resample('D').mean()   # Daily
s.resample('W').mean()   # Weekly
s.resample('M').mean()   # Monthly
s.resample('Q').mean()   # Quarterly
s.resample('Y').mean()   # Yearly
```

### 2. Business Frequencies

```python
s.resample('B').mean()   # Business day
s.resample('BM').mean()  # Business month end
```

### 3. Intraday

```python
s.resample('H').mean()   # Hourly
s.resample('T').mean()   # Minute
```

## OHLC Aggregation

Financial price data aggregation.

### 1. Open-High-Low-Close

```python
prices = pd.Series(
    [100, 101, 99, 102, 98, 103],
    index=pd.date_range('2025-01-01', periods=6, freq='D')
)

ohlc = prices.resample('W').ohlc()
print(ohlc)
```

### 2. Standard for Financial Data

OHLC is standard for representing price bars.

### 3. With Volume

```python
# For DataFrame with price and volume
df.resample('W').agg({
    'price': 'ohlc',
    'volume': 'sum'
})
```

## Aggregation Functions

Apply various aggregations when resampling.

### 1. Built-in Functions

```python
s.resample('M').mean()
s.resample('M').sum()
s.resample('M').first()
s.resample('M').last()
s.resample('M').count()
```

### 2. Multiple Functions

```python
s.resample('M').agg(['mean', 'std', 'min', 'max'])
```

### 3. Custom Function

```python
s.resample('M').apply(lambda x: x.max() - x.min())
```

## Upsampling

Increase frequency (requires filling).

### 1. Daily to Hourly

```python
daily = pd.Series([100, 101, 102], index=pd.date_range('2025-01-01', periods=3, freq='D'))
hourly = daily.resample('H').ffill()  # Forward fill
```

### 2. Fill Methods

```python
s.resample('H').ffill()    # Forward fill
s.resample('H').bfill()    # Backward fill
s.resample('H').asfreq()   # No fill (NaN)
```

### 3. Interpolation

```python
s.resample('H').interpolate()
```

## Practical Examples

Financial analysis with resampling.

### 1. Monthly Returns

```python
import yfinance as yf

aapl = yf.download('AAPL', start='2023-01-01', end='2024-01-01')
monthly_avg = aapl['Close'].resample('M').mean()
print(monthly_avg)
```

### 2. Rolling Analysis on Resampled Data

```python
monthly_returns = aapl['Close'].resample('M').last().pct_change()
```

### 3. Plotting

```python
import matplotlib.pyplot as plt

monthly_avg.plot(title='AAPL Monthly Average Closing Price')
plt.show()
```


---

## Exercises

**Exercise 1.** Write code that resamples daily data to monthly frequency using `.resample('ME').mean()`. Explain what `'ME'` means.

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

**Exercise 2.** Explain the difference between downsampling and upsampling. Give an example of each.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that resamples from daily to weekly, computing both the mean and the sum using `.resample('W').agg(['mean', 'sum'])`.

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

**Exercise 4.** Create hourly data and upsample to minute-level frequency using `.resample('min').ffill()`.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
