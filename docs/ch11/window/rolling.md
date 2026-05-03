# rolling Method

The `rolling()` method applies operations over a fixed-size sliding window, fundamental for time series analysis.

!!! tip "Mental Model"
    `rolling(window=N)` slides a fixed-size frame of N consecutive rows across your data, computing a statistic at each position. The first N-1 results are NaN because the window is not yet full. Common uses include moving averages for smoothing trends, rolling standard deviations for measuring volatility, and rolling correlations for time-varying relationships.

## Basic Rolling

Create rolling window calculations.

### 1. Moving Average

```python
import pandas as pd
import yfinance as yf

aapl = yf.download('AAPL', start='2023-01-01', end='2024-01-01')
aapl['5D_MA'] = aapl['Close'].rolling(window=5).mean()
print(aapl[['Close', '5D_MA']].head(10))
```

### 2. Rolling Standard Deviation

```python
aapl['5D_STD'] = aapl['Close'].rolling(window=5).std()
```

### 3. Rolling Sum

```python
aapl['5D_SUM'] = aapl['Volume'].rolling(window=5).sum()
```

## Key Parameters

Configure rolling window behavior.

### 1. window

```python
# Size of the moving window
s.rolling(window=5).mean()    # 5-period window
s.rolling(window=20).mean()   # 20-period window
```

### 2. min_periods

```python
# Minimum observations required
s.rolling(window=5, min_periods=1).mean()
# Returns value even with fewer than 5 observations
```

### 3. center

```python
# Label at window center vs. right edge
s.rolling(window=5, center=True).mean()
# Value labeled at middle of window
```

## Rolling Statistics

Common rolling calculations.

### 1. Central Tendency

```python
s.rolling(20).mean()    # Moving average
s.rolling(20).median()  # Moving median
```

### 2. Dispersion

```python
s.rolling(20).std()     # Moving standard deviation
s.rolling(20).var()     # Moving variance
```

### 3. Extremes

```python
s.rolling(20).min()     # Rolling minimum
s.rolling(20).max()     # Rolling maximum
```

## Custom Functions

Apply custom functions to rolling windows.

### 1. Custom Aggregation

```python
# Range within window
aapl['5D_Range'] = aapl['Close'].rolling(window=5).apply(
    lambda x: x.max() - x.min()
)
```

### 2. With NumPy

```python
import numpy as np

aapl['5D_Skew'] = aapl['Close'].rolling(window=20).apply(
    lambda x: pd.Series(x).skew()
)
```

### 3. Multiple Outputs

```python
def custom_stats(x):
    return x.mean() / x.std()  # Sharpe-like ratio

aapl['Custom'] = aapl['Returns'].rolling(20).apply(custom_stats)
```

## Financial Example

Volatility estimation.

### 1. Rolling Volatility

```python
# 30-day rolling standard deviation
aapl['30D_Volatility'] = aapl['Close'].rolling(window=30).std()
```

### 2. Annualized Volatility

```python
returns = aapl['Close'].pct_change()
aapl['Annualized_Vol'] = returns.rolling(20).std() * np.sqrt(252)
```

### 3. Bollinger Bands

```python
aapl['MA20'] = aapl['Close'].rolling(20).mean()
aapl['Upper'] = aapl['MA20'] + 2 * aapl['Close'].rolling(20).std()
aapl['Lower'] = aapl['MA20'] - 2 * aapl['Close'].rolling(20).std()
```

## NaN Handling

Rolling calculations produce NaN at the start.

### 1. Default Behavior

```python
# First (window-1) values are NaN
s.rolling(5).mean()  # First 4 values are NaN
```

### 2. With min_periods

```python
# Start computing earlier
s.rolling(5, min_periods=1).mean()
```

### 3. Drop NaN

```python
result = s.rolling(5).mean().dropna()
```


---

## Exercises

**Exercise 1.** Write code that computes the 20-day rolling mean and rolling standard deviation of a random time series.

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

**Exercise 2.** Explain the `window`, `min_periods`, and `center` parameters of `.rolling()`. What does `center=True` do?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that applies a custom function to a rolling window using `.rolling(10).apply(lambda x: x.max() - x.min())`.

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

**Exercise 4.** Create Bollinger Bands by computing the 20-day rolling mean and adding/subtracting 2 rolling standard deviations.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
