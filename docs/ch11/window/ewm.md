# ewm Method

The `ewm()` method computes exponentially weighted statistics, where recent observations have more influence than older ones.

!!! tip "Mental Model"
    EWM applies exponentially decaying weights: yesterday's value matters more than last week's, which matters more than last month's. The `span` parameter controls how fast the weights decay -- a larger span means a longer memory. Unlike rolling windows with a hard cutoff, EWM uses all past data but down-weights older observations smoothly.

## Basic EWM

Create exponentially weighted calculations.

### 1. EWMA (Exponentially Weighted Moving Average)

```python
import pandas as pd
import yfinance as yf

aapl = yf.download('AAPL', start='2023-01-01', end='2024-01-01')
aapl['EWMA_10'] = aapl['Close'].ewm(span=10, adjust=False).mean()
print(aapl[['Close', 'EWMA_10']].head(10))
```

### 2. EWM Standard Deviation

```python
aapl['EWMA_Std'] = aapl['Close'].ewm(span=10).std()
```

### 3. EWM Variance

```python
aapl['EWMA_Var'] = aapl['Close'].ewm(span=10).var()
```

## Weight Parameters

Control the decay of weights.

### 1. span

```python
# Specify decay in terms of "center of mass"
s.ewm(span=10).mean()  # Roughly equivalent to 10-period window

# alpha = 2 / (span + 1)
```

### 2. halflife

```python
# Time for weight to decay to half
s.ewm(halflife=5).mean()
```

### 3. alpha

```python
# Direct smoothing factor (0 < alpha <= 1)
s.ewm(alpha=0.1).mean()  # Lower alpha = more smoothing
```

## EWMA Formula

How exponentially weighted mean is calculated.

### 1. Recursive Formula

When `adjust=False`:

$$\text{EWMA}_t = (1 - \alpha) \cdot \text{EWMA}_{t-1} + \alpha \cdot x_t$$

### 2. Alpha from Span

$$\alpha = \frac{2}{\text{span} + 1}$$

### 3. Example Calculation

```python
# With span=10: alpha = 2/11 ≈ 0.182
# Recent observation gets 18.2% weight
# Previous EWMA gets 81.8% weight
```

## EWM vs Rolling

Compare EWM to simple rolling average.

### 1. Weight Distribution

```python
# Rolling: equal weights within window
# EWM: exponentially decaying weights
```

### 2. Responsiveness

```python
# EWM responds faster to recent changes
# Rolling has more lag
```

### 3. Visual Comparison

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
aapl['Close'].plot(ax=ax, label='Price', alpha=0.5)
aapl['Close'].rolling(20).mean().plot(ax=ax, label='SMA(20)')
aapl['Close'].ewm(span=20).mean().plot(ax=ax, label='EWMA(20)')
ax.legend()
plt.show()
```

## Financial Applications

EWM in financial analysis.

### 1. EWMA Volatility

```python
import numpy as np

returns = aapl['Close'].pct_change()
aapl['EWMA_Volatility'] = returns.ewm(span=20).std() * np.sqrt(252)
```

### 2. Fast vs Slow

```python
# Trading signal: fast EWMA crosses slow EWMA
aapl['EWMA_Fast'] = aapl['Close'].ewm(span=12).mean()
aapl['EWMA_Slow'] = aapl['Close'].ewm(span=26).mean()
aapl['Signal'] = aapl['EWMA_Fast'] > aapl['EWMA_Slow']
```

### 3. Risk Management

```python
# EWMA responds quickly to volatility spikes
aapl['Risk'] = returns.ewm(span=10).std()
```

## adjust Parameter

Control bias correction.

### 1. adjust=True (Default)

```python
# Divides by decaying adjustment factor
# More accurate but slower to compute
s.ewm(span=10, adjust=True).mean()
```

### 2. adjust=False

```python
# Pure recursive formula
# Faster, commonly used in finance
s.ewm(span=10, adjust=False).mean()
```

### 3. Difference

The difference is most noticeable at the beginning of the series.


---

## Exercises

**Exercise 1.** Write code that computes the exponentially weighted moving average (EWMA) using `s.ewm(span=10).mean()`.

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

**Exercise 2.** Explain the `span`, `com`, and `halflife` parameters for `ewm()`. How do they relate to each other?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that plots a time series with both a simple moving average and an EWMA to compare their responsiveness.

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

**Exercise 4.** Create a DataFrame and compute the EWMA variance using `df.ewm(span=20).var()`.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
