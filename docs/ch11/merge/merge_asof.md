# merge_asof Method

The `merge_asof()` function performs an approximate merge, matching on the nearest key rather than exact equality. It is designed for ordered data like time series.

!!! tip "Mental Model"
    `merge_asof` is a "closest match" join. For each row in the left table, it finds the nearest preceding (or nearest overall) key in the right table. This is essential for time series: if you have trades at irregular timestamps and quotes at different timestamps, `merge_asof` pairs each trade with the most recent quote.

## Basic Concept

Match to the nearest preceding value.

### 1. Time-based Matching

```python
import pandas as pd

# Sales data
units_sold = pd.DataFrame({
    'product_id': [1, 2, 3],
    'purchase_date': pd.to_datetime(['2022-01-01', '2022-01-02', '2022-01-03'])
})

# Price data
prices = pd.DataFrame({
    'product_id': [1, 2],
    'start_date': pd.to_datetime(['2022-01-01', '2022-01-02']),
    'price': [100, 200]
})
```

### 2. merge_asof vs merge

```python
# Regular merge requires exact match
pd.merge(units_sold, prices, 
         left_on='purchase_date', right_on='start_date')

# merge_asof finds nearest preceding match
pd.merge_asof(
    units_sold.sort_values('purchase_date'),
    prices.sort_values('start_date'),
    left_on='purchase_date',
    right_on='start_date'
)
```

### 3. Requires Sorted Data

Both DataFrames must be sorted by the merge key.

## Practical Example

Match sales to applicable prices.

### 1. Sample Data

```python
units_sold = pd.DataFrame({
    'product_id': [1, 1, 2, 2],
    'purchase_date': pd.to_datetime([
        '2022-01-15', '2022-05-10', '2022-03-01', '2022-07-01'
    ]),
    'units': [10, 5, 8, 12]
})

prices = pd.DataFrame({
    'product_id': [1, 1, 2, 2],
    'start_date': pd.to_datetime([
        '2022-01-01', '2022-04-01', '2022-01-01', '2022-06-01'
    ]),
    'price': [100, 120, 200, 180]
})
```

### 2. Sort Before Merge

```python
units_sold = units_sold.sort_values('purchase_date')
prices = prices.sort_values('start_date')
```

### 3. merge_asof with by

```python
result = pd.merge_asof(
    units_sold,
    prices,
    left_on='purchase_date',
    right_on='start_date',
    by='product_id'
)
print(result)
```

## Key Parameters

Configure merge_asof behavior.

### 1. by Parameter

```python
# Match exactly on 'by' columns, approximately on merge key
pd.merge_asof(
    left, right,
    on='timestamp',
    by='product_id'  # Exact match required
)
```

### 2. direction Parameter

```python
# 'backward' (default): match to previous value
# 'forward': match to next value
# 'nearest': match to closest value

pd.merge_asof(left, right, on='time', direction='backward')
pd.merge_asof(left, right, on='time', direction='forward')
pd.merge_asof(left, right, on='time', direction='nearest')
```

### 3. tolerance Parameter

```python
# Maximum distance for match
pd.merge_asof(
    left, right,
    on='timestamp',
    tolerance=pd.Timedelta('1 day')  # Max 1 day gap
)
```

## Financial Application

Match trades to quotes.

### 1. Trade Data

```python
trades = pd.DataFrame({
    'timestamp': pd.to_datetime([
        '2024-01-01 10:00:05',
        '2024-01-01 10:00:15',
        '2024-01-01 10:00:25'
    ]),
    'quantity': [100, 50, 75]
})
```

### 2. Quote Data

```python
quotes = pd.DataFrame({
    'timestamp': pd.to_datetime([
        '2024-01-01 10:00:00',
        '2024-01-01 10:00:10',
        '2024-01-01 10:00:20'
    ]),
    'bid': [99.0, 99.5, 99.8],
    'ask': [100.0, 100.5, 100.8]
})
```

### 3. Match Trades to Quotes

```python
result = pd.merge_asof(
    trades.sort_values('timestamp'),
    quotes.sort_values('timestamp'),
    on='timestamp',
    direction='backward'
)
# Each trade gets the most recent quote
```

## Comparison with Regular Merge

When to use each method.

### 1. Exact Match (merge)

```python
# Use when keys must match exactly
# Foreign key relationships
# Categorical data
```

### 2. Approximate Match (merge_asof)

```python
# Use for time-based data
# Price lookups with effective dates
# Event matching within tolerance
```

### 3. Performance

```python
# merge_asof is optimized for sorted data
# Faster than alternatives for time series
```

---

## Exercises

**Exercise 1.**
Create a `trades` DataFrame with timestamps and a `quotes` DataFrame with slightly earlier timestamps. Use `pd.merge_asof()` to match each trade with the most recent quote that occurred at or before the trade time.

??? success "Solution to Exercise 1"
    Match trades to the most recent preceding quote.

        import pandas as pd

        trades = pd.DataFrame({
            'time': pd.to_datetime(['10:00:01', '10:00:03', '10:00:05']),
            'price': [100, 102, 101]
        })
        quotes = pd.DataFrame({
            'time': pd.to_datetime(['10:00:00', '10:00:02', '10:00:04']),
            'bid': [99, 101, 100]
        })
        result = pd.merge_asof(trades, quotes, on='time')
        print(result)

---

**Exercise 2.**
Use `pd.merge_asof()` with the `tolerance` parameter to match only if the time difference is within a specified window (e.g., 2 seconds). Verify that trades without a quote within the tolerance get `NaN`.

??? success "Solution to Exercise 2"
    Use tolerance to limit the match window.

        import pandas as pd

        trades = pd.DataFrame({
            'time': pd.to_datetime(['10:00:01', '10:00:10']),
            'price': [100, 102]
        })
        quotes = pd.DataFrame({
            'time': pd.to_datetime(['10:00:00', '10:00:02']),
            'bid': [99, 101]
        })
        result = pd.merge_asof(trades, quotes, on='time', tolerance=pd.Timedelta('2s'))
        print(result)
        # Second trade has no quote within 2 seconds -> NaN

---

**Exercise 3.**
Use `pd.merge_asof()` with a `by` parameter to perform the approximate match within groups (e.g., match each trade to the latest quote for the same stock ticker).

??? success "Solution to Exercise 3"
    Use the by parameter for grouped asof merge.

        import pandas as pd

        trades = pd.DataFrame({
            'time': pd.to_datetime(['10:00:01', '10:00:01', '10:00:03']),
            'ticker': ['AAPL', 'MSFT', 'AAPL'],
            'price': [150, 250, 152]
        })
        quotes = pd.DataFrame({
            'time': pd.to_datetime(['10:00:00', '10:00:00', '10:00:02']),
            'ticker': ['AAPL', 'MSFT', 'AAPL'],
            'bid': [149, 249, 151]
        })
        result = pd.merge_asof(trades, quotes, on='time', by='ticker')
        print(result)
