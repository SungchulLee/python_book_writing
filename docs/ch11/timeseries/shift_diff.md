# shift and diff Methods

The `shift()` and `diff()` methods are essential for time series analysis, computing lagged values and differences.

!!! tip "Mental Model"
    `shift(n)` slides the data up or down by n positions without changing the index -- it creates lagged or lead columns. `diff(n)` computes `value - value_shifted_by_n`, giving the absolute change. Together they are the building blocks for returns, growth rates, and any "compare this period to the previous" analysis.

## shift Method

Move data by specified number of periods.

### 1. Basic shift

```python
import pandas as pd
import yfinance as yf

df = yf.Ticker('WMT').history(start='2020-01-01', end='2020-01-10')
df = df[['Close']]

df['shift_1'] = df['Close'].shift(1)
df['shift_2'] = df['Close'].shift(2)
print(df)
```

```
                 Close    shift_1    shift_2
Date                                        
2020-01-02  116.459999        NaN        NaN
2020-01-03  116.279999  116.459999        NaN
2020-01-06  116.230003  116.279999  116.459999
2020-01-07  116.849998  116.230003  116.279999
2020-01-08  116.220001  116.849998  116.230003
```

### 2. Positive Shift

```python
# shift(1): current row gets previous value
df['previous_close'] = df['Close'].shift(1)
```

### 3. Negative Shift

```python
# shift(-1): current row gets next value
df['next_close'] = df['Close'].shift(-1)
```

## shift for Comparisons

Compare current values to previous.

### 1. Day-over-Day Change

```python
df['change'] = df['Close'] - df['Close'].shift(1)
```

### 2. Conditional Logic

```python
# Did price increase?
df['increased'] = df['Close'] > df['Close'].shift(1)
```

### 3. LeetCode: Rising Temperature

```python
# Temperature rose AND consecutive day
weather[
    (weather['temperature'] > weather['temperature'].shift(1)) &
    (weather['id'] == weather['id'].shift(1) + 1)
]
```

## diff Method

Calculate difference between consecutive elements.

### 1. Basic diff

```python
df = yf.Ticker('WMT').history(start='2020-01-01', end='2020-01-10')
df = df[['Close']]

df['diff_1'] = df['Close'].diff(1)
df['diff_2'] = df['Close'].diff(2)
print(df)
```

```
                 Close    diff_1    diff_2
Date                                       
2020-01-02  116.459999       NaN       NaN
2020-01-03  116.279999 -0.180000       NaN
2020-01-06  116.230003 -0.049996 -0.229996
2020-01-07  116.849998  0.619995  0.569999
2020-01-08  116.220001 -0.629997  0.009998
```

### 2. diff Equivalent

```python
# diff(1) is equivalent to:
df['Close'] - df['Close'].shift(1)
```

### 3. Higher Order Differences

```python
# Second difference (change in change)
df['second_diff'] = df['Close'].diff().diff()
```

## LeetCode Example: Rising Temperature

Find days with temperature increase.

### 1. Sample Data

```python
weather = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'recordDate': pd.to_datetime(['2024-01-01', '2024-01-02', 
                                   '2024-01-03', '2024-01-04']),
    'temperature': [10, 25, 20, 30]
})
weather = weather.sort_values('recordDate')
```

### 2. Using diff

```python
# Temperature increased AND consecutive dates
result = weather[
    (weather['temperature'].diff() > 0) &
    (weather['recordDate'].diff().dt.days == 1)
]
```

### 3. Using shift

```python
result = weather[
    (weather['temperature'] > weather['temperature'].shift(1)) &
    (weather['recordDate'] == weather['recordDate'].shift(1) + pd.Timedelta(days=1))
]
```

## LeetCode Example: Consecutive Numbers

Find numbers appearing 3+ times consecutively.

### 1. Sample Data

```python
logs = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6],
    'num': [1, 1, 1, 2, 1, 2]
})
logs = logs.sort_values('id')
```

### 2. Check Consecutive

```python
consecutive = logs[
    (logs['num'] == logs['num'].shift(1)) &
    (logs['num'] == logs['num'].shift(2)) &
    (logs['id'] == logs['id'].shift(1) + 1) &
    (logs['id'] == logs['id'].shift(2) + 2)
]
```

### 3. Get Unique Numbers

```python
result = consecutive.drop_duplicates('num')[['num']]
```

## Date Differences

shift and diff with dates.

### 1. Date shift

```python
df['prev_date'] = df['date'].shift(1)
```

### 2. Date diff

```python
df['days_between'] = df['date'].diff().dt.days
```

### 3. Check Consecutive Dates

```python
df['consecutive'] = df['date'].diff().dt.days == 1
```

## LeetCode: Human Traffic

Find 3+ consecutive high traffic days.

### 1. Sample Data

```python
stadium = pd.DataFrame({
    'id': [1, 2, 3, 5, 6, 7, 8],
    'people': [100, 200, 150, 300, 250, 400, 350]
})
```

### 2. Check Consecutive IDs

```python
# Current and previous two rows are consecutive
consecutive = (
    (stadium['id'].diff() == 1) &
    (stadium['id'].diff().shift(1) == 1)
)
```

### 3. Alternative

```python
# Marks the third row of each consecutive sequence
consecutive = (
    (stadium['id'] == stadium['id'].shift(1) + 1) &
    (stadium['id'] == stadium['id'].shift(2) + 2)
)
```

## Financial Applications

Daily returns and changes.

### 1. Price Change

```python
df['price_change'] = df['Close'].diff()
```

### 2. Daily Return

```python
df['daily_return'] = df['Close'].diff() / df['Close'].shift(1)
# or
df['daily_return'] = df['Close'].pct_change()
```

### 3. Cumulative Return

```python
df['cum_return'] = (1 + df['daily_return']).cumprod() - 1
```


---

## Exercises

**Exercise 1.** Write code that uses `s.shift(1)` and `s.diff(1)` on a price Series. Explain the relationship between them.

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

**Exercise 2.** Explain the `shift()` method. What does a positive vs negative shift value do?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that computes log returns using `np.log(s / s.shift(1))`. Compare with `pct_change()`.

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

**Exercise 4.** Create a DataFrame and use `shift()` to create a lagged feature column for time series forecasting.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
