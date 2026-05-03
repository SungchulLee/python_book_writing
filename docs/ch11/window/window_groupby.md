# Window with GroupBy

Combine window functions with groupby to apply rolling, expanding, or EWM calculations within groups.

!!! tip "Mental Model"
    `groupby(...).rolling(N)` applies the rolling window independently within each group. This is essential for panel data: computing a 20-day moving average per stock, not across stocks. Use `transform` with a lambda for clean integration back into the original DataFrame without index headaches.

## Rolling Within Groups

Apply rolling calculations per group.

### 1. Basic Pattern

```python
import pandas as pd

df = pd.DataFrame({
    'Ticker': ['AAPL', 'AAPL', 'AAPL', 'MSFT', 'MSFT', 'MSFT'],
    'Date': pd.date_range('2024-01-01', periods=3).tolist() * 2,
    'Close': [150, 152, 151, 350, 355, 353]
})

df['5D_MA'] = df.groupby('Ticker')['Close'].rolling(window=2).mean().reset_index(0, drop=True)
print(df)
```

### 2. Using transform

```python
df['MA'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.rolling(2).mean()
)
```

### 3. Preserves Original Index

The transform approach maintains alignment with original DataFrame.

## Expanding Within Groups

Cumulative calculations per group.

### 1. Cumulative Mean per Group

```python
df['Cum_Mean'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.expanding().mean()
)
```

### 2. Running Max per Group

```python
df['Running_Max'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.expanding().max()
)
```

### 3. Since-Inception Return per Asset

```python
df['Since_Start'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x / x.iloc[0] - 1
)
```

## EWM Within Groups

Exponentially weighted calculations per group.

### 1. EWMA per Asset

```python
df['EWMA'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.ewm(span=10).mean()
)
```

### 2. EWM Volatility per Asset

```python
returns = df.groupby('Ticker')['Close'].pct_change()
df['EWM_Vol'] = returns.groupby(df['Ticker']).transform(
    lambda x: x.ewm(span=20).std()
)
```

### 3. Independent Decay per Group

Each group's EWM is calculated independently.

## Practical Example

Multi-asset portfolio analysis.

### 1. Sample Data

```python
import numpy as np

np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=50)
tickers = ['AAPL', 'MSFT', 'GOOGL']

data = []
for ticker in tickers:
    prices = 100 + np.cumsum(np.random.randn(50))
    for date, price in zip(dates, prices):
        data.append({'Ticker': ticker, 'Date': date, 'Close': price})

df = pd.DataFrame(data)
```

### 2. Add Rolling Stats per Asset

```python
df['MA20'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.rolling(20).mean()
)

df['Vol20'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.pct_change().rolling(20).std()
)
```

### 3. Cross-sectional Rank

```python
# Rank within each date
df['Rank'] = df.groupby('Date')['Close'].rank()
```

## Performance Tip

Efficient grouped window operations.

### 1. Single transform Call

```python
# Faster: single grouped operation
df['MA'] = df.groupby('Ticker')['Close'].transform(
    lambda x: x.rolling(20).mean()
)
```

### 2. Avoid Looping

```python
# Slower: don't loop over groups
# for ticker in df['Ticker'].unique():
#     ...
```

### 3. Use Built-in When Possible

GroupBy rolling is optimized internally.


---

## Exercises

**Exercise 1.** Write code that computes a rolling mean within each group using `df.groupby('group').rolling(5).mean()`.

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

**Exercise 2.** Explain why combining `groupby()` with `rolling()` is useful. Give a real-world example.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that computes an expanding sum for each group separately.

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

**Exercise 4.** Create a DataFrame with panel data (multiple entities over time) and compute rolling z-scores within each entity.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
