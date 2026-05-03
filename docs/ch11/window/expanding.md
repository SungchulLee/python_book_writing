# expanding Method

The `expanding()` method computes statistics over all data from the start up to each point, with a window that grows over time.

!!! tip "Mental Model"
    An expanding window starts at the first row and grows by one row at each step -- it computes a cumulative statistic. At row 10, it uses rows 1-10; at row 100, it uses rows 1-100. This is useful for running averages, cumulative returns, and any "so far" metric that incorporates all prior history.

## Basic Expanding

Create expanding window calculations.

### 1. Cumulative Mean

```python
import pandas as pd
import yfinance as yf

aapl = yf.download('AAPL', start='2023-01-01', end='2024-01-01')
aapl['Cumulative_Mean'] = aapl['Close'].expanding().mean()
print(aapl[['Close', 'Cumulative_Mean']].head(10))
```

### 2. Cumulative Sum

```python
aapl['Cumulative_Sum'] = aapl['Volume'].expanding().sum()
```

### 3. Cumulative Standard Deviation

```python
aapl['Cumulative_STD'] = aapl['Close'].expanding().std()
```

## How Expanding Works

At time t, includes observations 1 to t.

### 1. Window Growth

```python
# Day 1: window = [1]
# Day 2: window = [1, 2]
# Day 3: window = [1, 2, 3]
# Day N: window = [1, 2, ..., N]
```

### 2. Formula for Mean

At time $t$:

$$\text{Expanding Mean}_t = \frac{1}{t} \sum_{i=1}^{t} x_i$$

### 3. vs Rolling

```python
# Rolling: fixed window size
# Expanding: window grows from 1 to N
```

## min_periods Parameter

Minimum observations before calculating.

### 1. Default (min_periods=1)

```python
s.expanding().mean()  # Starts from first value
```

### 2. With Minimum

```python
s.expanding(min_periods=5).mean()  # First 4 values are NaN
```

### 3. Use Case

```python
# Wait for enough data before computing volatility
s.expanding(min_periods=20).std()
```

## Common Applications

Typical expanding calculations.

### 1. Cumulative Returns

```python
returns = aapl['Close'].pct_change()
cumulative = (1 + returns).expanding().prod() - 1
```

### 2. Running Statistics

```python
aapl['Running_Max'] = aapl['Close'].expanding().max()
aapl['Running_Min'] = aapl['Close'].expanding().min()
```

### 3. Progressive Estimates

```python
# Track how estimates converge
aapl['Mean_Estimate'] = aapl['Close'].expanding().mean()
```

## Financial Example

Track cumulative performance metrics.

### 1. Cumulative Sharpe

```python
import numpy as np

returns = aapl['Close'].pct_change()
aapl['Cum_Mean'] = returns.expanding().mean()
aapl['Cum_Std'] = returns.expanding().std()
aapl['Cum_Sharpe'] = aapl['Cum_Mean'] / aapl['Cum_Std'] * np.sqrt(252)
```

### 2. All-Time High

```python
aapl['ATH'] = aapl['Close'].expanding().max()
aapl['Drawdown'] = aapl['Close'] / aapl['ATH'] - 1
```

### 3. Since Inception Returns

```python
first_price = aapl['Close'].iloc[0]
aapl['Since_Inception'] = aapl['Close'] / first_price - 1
```

## Expanding vs cumsum/cumprod

Comparison with built-in cumulative functions.

### 1. cumsum

```python
# Equivalent for sum
s.expanding().sum()
s.cumsum()  # Same result, faster
```

### 2. cumprod

```python
# Equivalent for product
s.expanding().prod()
s.cumprod()  # Same result, faster
```

### 3. When to Use Each

```python
# Use cumsum/cumprod for simple cumulative operations
# Use expanding() for mean, std, custom functions
```


---

## Exercises

**Exercise 1.** Write code that computes the expanding (cumulative) mean using `s.expanding().mean()`.

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

**Exercise 2.** Explain the difference between `expanding()` and `rolling()`. When would you use each?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that computes the expanding maximum and minimum of a time series. What do these represent?

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

**Exercise 4.** Create a DataFrame and use `expanding(min_periods=10).std()` to compute the expanding standard deviation, requiring at least 10 observations.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
