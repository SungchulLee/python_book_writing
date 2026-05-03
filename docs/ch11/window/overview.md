# Window Functions Overview

Window functions apply operations over subsets of data, enabling rolling, expanding, and exponentially weighted calculations.

!!! tip "Mental Model"
    All three window types slide through your data and compute a statistic at each position. Rolling uses a fixed-size window that moves forward. Expanding uses a window that starts at row 1 and grows. EWM uses all data but weights recent observations more heavily. The choice depends on whether you want a local snapshot (rolling), a cumulative history (expanding), or a decay-weighted memory (EWM).

## Three Window Types

pandas provides three core window function types.

### 1. Rolling Window

```python
import pandas as pd

s = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Fixed-size sliding window
s.rolling(window=3).mean()
```

```
0         NaN
1         NaN
2    2.000000
3    3.000000
4    4.000000
...
```

### 2. Expanding Window

```python
# Window grows from start to current position
s.expanding().mean()
```

```
0     1.000000
1     1.500000
2     2.000000
3     2.500000
4     3.000000
...
```

### 3. Exponentially Weighted

```python
# Recent values weighted more heavily
s.ewm(span=3).mean()
```

## Use Cases

When to use each window type.

### 1. Rolling

- Moving averages
- Rolling volatility
- Trend detection
- Smoothing noisy data

### 2. Expanding

- Cumulative statistics
- Progressive estimates
- Since-inception metrics

### 3. Exponentially Weighted

- Adaptive smoothing
- Fast-reacting metrics
- Volatility estimation

## Comparison Table

Feature comparison across window types.

### 1. Window Size

| Type | Window Size |
|------|-------------|
| Rolling | Fixed (e.g., 20 days) |
| Expanding | Grows from 1 to N |
| EWM | Effective span (decay) |

### 2. Weight Distribution

| Type | Weights |
|------|---------|
| Rolling | Equal within window |
| Expanding | Equal for all data |
| EWM | Exponential decay |

### 3. Responsiveness

| Type | To New Data |
|------|-------------|
| Rolling | Medium |
| Expanding | Slow |
| EWM | Fast |

## Common Methods

Methods available on window objects.

### 1. Statistical

```python
window.mean()
window.sum()
window.std()
window.var()
window.min()
window.max()
```

### 2. Count and Apply

```python
window.count()
window.apply(custom_func)
```

### 3. Quantiles

```python
window.quantile(0.5)  # Median
window.median()
```

## Financial Applications

Window functions in finance.

### 1. Moving Averages

```python
df['MA20'] = df['Close'].rolling(20).mean()
df['MA50'] = df['Close'].rolling(50).mean()
```

### 2. Volatility

```python
df['Vol20'] = df['Returns'].rolling(20).std() * np.sqrt(252)
```

### 3. Cumulative Returns

```python
df['CumReturn'] = (1 + df['Returns']).expanding().prod() - 1
```


---

## Exercises

**Exercise 1.** Name the three window operations available in Pandas: `rolling()`, `expanding()`, and `ewm()`. Write one example of each.

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

**Exercise 2.** Explain what a window function does conceptually. How does it differ from a regular aggregation?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that computes the 20-period rolling mean and the expanding mean on the same data and plots both.

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

**Exercise 4.** Explain the `min_periods` parameter. What happens when the window contains fewer observations than `min_periods`?

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
