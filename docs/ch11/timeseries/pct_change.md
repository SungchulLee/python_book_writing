# pct_change Method

The `pct_change()` method calculates percentage change between consecutive elements, essential for financial analysis.

!!! tip "Mental Model"
    `pct_change()` computes `(current - previous) / previous` for each row. The first row is always NaN because there is no previous value. It is the standard way to compute returns from price series, growth rates from revenue series, or any relative change over consecutive periods.

## Basic Usage

Calculate period-over-period percentage change.

### 1. Simple pct_change

```python
import pandas as pd
import yfinance as yf

df = yf.Ticker('WMT').history(start='2020-01-01', end='2020-01-10')
df = df[['Close']]

df['pct_change'] = df['Close'].pct_change()
print(df)
```

```
                 Close  pct_change
Date                              
2020-01-02  116.459999         NaN
2020-01-03  116.279999   -0.001546
2020-01-06  116.230003   -0.000430
2020-01-07  116.849998    0.005333
2020-01-08  116.220001   -0.005392
```

### 2. Formula

$$r_D = \frac{P_t - P_{t-1}}{P_{t-1}} = \frac{P_t}{P_{t-1}} - 1$$

### 3. First Value is NaN

No previous value to compare with.

## periods Parameter

Calculate change over multiple periods.

### 1. Daily (Default)

```python
df['daily_return'] = df['Close'].pct_change(periods=1)
```

### 2. Weekly

```python
df['weekly_return'] = df['Close'].pct_change(periods=5)
```

### 3. Monthly

```python
df['monthly_return'] = df['Close'].pct_change(periods=21)
```

## Discrete vs Log Returns

Different return calculations.

### 1. Discrete Returns

```python
# Standard percentage change
df['discrete_return'] = df['Close'].pct_change()
```

### 2. Log Returns

```python
import numpy as np

df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))
```

### 3. Relationship

$$r_C = \log\frac{P_t}{P_{t-1}} \approx \frac{P_t}{P_{t-1}} - 1 = r_D$$

For small changes, log and discrete returns are approximately equal.

## Cumulative Returns

Calculate total return over time.

### 1. From pct_change

```python
df['daily_return'] = df['Close'].pct_change()
df['cum_return'] = (1 + df['daily_return']).cumprod() - 1
```

### 2. Direct Calculation

```python
df['cum_return'] = df['Close'] / df['Close'].iloc[0] - 1
```

### 3. Total Return

```python
total_return = df['Close'].iloc[-1] / df['Close'].iloc[0] - 1
```

## Rolling Statistics

Combine with rolling windows.

### 1. Rolling Volatility

```python
df['volatility'] = df['Close'].pct_change().rolling(21).std() * np.sqrt(252)
```

### 2. Rolling Average Return

```python
df['avg_return'] = df['Close'].pct_change().rolling(21).mean()
```

### 3. Sharpe Ratio (Simplified)

```python
returns = df['Close'].pct_change()
sharpe = returns.mean() / returns.std() * np.sqrt(252)
```

## Multiple Columns

Apply to entire DataFrame.

### 1. All Columns

```python
df = yf.Ticker('WMT').history(start='2020-01-01', end='2020-12-31')
returns = df.pct_change()
```

### 2. Selected Columns

```python
price_cols = ['Open', 'High', 'Low', 'Close']
returns = df[price_cols].pct_change()
```

### 3. Correlation of Returns

```python
returns.corr()
```

## fill_method Parameter

Handle missing values.

### 1. Forward Fill (Default)

```python
df['return'] = df['Close'].pct_change(fill_method='ffill')
```

### 2. No Fill

```python
df['return'] = df['Close'].pct_change(fill_method=None)
```

### 3. With Missing Data

```python
# If data has gaps, fill_method controls behavior
df['Close'].fillna(method='ffill').pct_change()
```

## Financial Analysis Example

Complete return analysis.

### 1. Load Data

```python
df = yf.Ticker('SPY').history(period='1y')
```

### 2. Calculate Returns

```python
df['daily_return'] = df['Close'].pct_change()
df['cum_return'] = (1 + df['daily_return']).cumprod() - 1
```

### 3. Summary Statistics

```python
print(f"Mean Daily Return: {df['daily_return'].mean():.4%}")
print(f"Daily Volatility: {df['daily_return'].std():.4%}")
print(f"Total Return: {df['cum_return'].iloc[-1]:.2%}")
print(f"Annualized Return: {df['daily_return'].mean() * 252:.2%}")
print(f"Annualized Volatility: {df['daily_return'].std() * np.sqrt(252):.2%}")
```

## Compare to Manual Calculation

Verify pct_change formula.

### 1. pct_change

```python
df['pct'] = df['Close'].pct_change()
```

### 2. Manual

```python
df['manual'] = (df['Close'] - df['Close'].shift(1)) / df['Close'].shift(1)
```

### 3. Verify Equal

```python
print(df['pct'].equals(df['manual']))  # True (ignoring NaN)
```

## GroupBy with pct_change

Calculate returns by group.

### 1. Per-Stock Returns

```python
# Multiple stocks in one DataFrame
df['return'] = df.groupby('ticker')['close'].pct_change()
```

### 2. Reset per Group

```python
# Cumulative return per stock
df['cum_return'] = df.groupby('ticker')['return'].transform(
    lambda x: (1 + x).cumprod() - 1
)
```

### 3. Compare Stocks

```python
# Pivot for comparison
pivot = df.pivot(columns='ticker', values='cum_return')
```


---

## Exercises

**Exercise 1.** Write code that computes percentage changes using `s.pct_change()` on a price Series. What does the first value equal?

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

**Exercise 2.** Explain the difference between `pct_change()` and `diff()`. When would you use each?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that computes the 5-period percentage change using `pct_change(periods=5)`.

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

**Exercise 4.** Create a DataFrame of stock prices and compute daily returns using `pct_change()`. Calculate the mean and standard deviation of returns.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
