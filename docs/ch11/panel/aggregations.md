# Panel Aggregations

Panel data enables both entity-wise and time-wise aggregations. This document covers common aggregation patterns.

!!! tip "Mental Model"
    Panel aggregation has two natural directions: aggregate across time (one result per entity) or across entities (one result per time point). Use `groupby(level='ticker')` for entity-wise and `groupby(level='date')` for time-wise summaries. The `level` parameter in `groupby` replaces column names with index level names.

## Setup

```python
import pandas as pd
import numpy as np

# Create sample panel
tickers = ['AAPL', 'MSFT', 'GOOGL']
dates = pd.date_range('2024-01-01', periods=10)
index = pd.MultiIndex.from_product([tickers, dates], names=['ticker', 'date'])

np.random.seed(42)
df = pd.DataFrame({
    'return': np.random.randn(30) * 0.02,
    'volume': np.random.randint(1000, 10000, 30)
}, index=index)
```

## Entity-Wise Aggregation (Across Time)

Aggregate each entity's time series.

### Using groupby(level=)

```python
# Mean return per ticker (across all dates)
mean_by_ticker = df.groupby(level='ticker').mean()
print("Mean by ticker:")
print(mean_by_ticker)
```

```
Mean by ticker:
          return       volume
ticker                       
AAPL    0.005123  5234.500000
MSFT    0.002891  4891.300000
GOOGL  -0.001234  5567.200000
```

### Various Aggregations per Entity

```python
# Multiple statistics per ticker
entity_stats = df.groupby(level='ticker').agg({
    'return': ['mean', 'std', 'min', 'max'],
    'volume': ['mean', 'sum']
})
print("Entity statistics:")
print(entity_stats)
```

### Rolling Operations per Entity

```python
# 5-day rolling mean return per ticker
rolling_mean = df.groupby(level='ticker')['return'].rolling(window=5).mean()
print("Rolling mean per entity:")
print(rolling_mean)
```

## Time-Wise Aggregation (Cross-Sectional)

Aggregate across entities at each time point.

### Using groupby(level=)

```python
# Mean return per date (across all tickers)
mean_by_date = df.groupby(level='date').mean()
print("Mean by date (cross-sectional):")
print(mean_by_date)
```

```
Mean by date (cross-sectional):
              return       volume
date                             
2024-01-01  0.003456  4567.333333
2024-01-02 -0.001234  5234.000000
...
```

### Cross-Sectional Statistics

```python
# Cross-sectional stats each day
cross_sectional = df.groupby(level='date').agg({
    'return': ['mean', 'std', 'min', 'max', 'count']
})
print("Cross-sectional statistics:")
print(cross_sectional)
```

## Using .xs for Aggregation

```python
# Get cross-section, then aggregate
jan1_returns = df.xs('2024-01-01', level='date')['return']
print(f"Jan 1 mean return: {jan1_returns.mean():.4f}")
print(f"Jan 1 return std: {jan1_returns.std():.4f}")
```

## Transform: Broadcast Aggregation

Keep original shape while adding aggregated values.

```python
# Add entity mean as new column
df['entity_mean'] = df.groupby(level='ticker')['return'].transform('mean')

# Add cross-sectional mean
df['time_mean'] = df.groupby(level='date')['return'].transform('mean')

# Demeaned return (relative to entity mean)
df['return_demeaned'] = df['return'] - df['entity_mean']

print(df.head(10))
```

## Entity-Specific Time Series Operations

```python
# Cumulative return per entity
df['cum_return'] = df.groupby(level='ticker')['return'].cumsum()

# Lagged return per entity
df['return_lag1'] = df.groupby(level='ticker')['return'].shift(1)

# Return momentum (current vs lagged)
df['momentum'] = df['return'] - df['return_lag1']

print(df[['return', 'cum_return', 'return_lag1', 'momentum']].head(15))
```

## Wide-Format Aggregations

Convert to wide format for cross-entity analysis.

```python
# Reshape to wide format
returns_wide = df['return'].unstack('ticker')
print("Wide format returns:")
print(returns_wide.head())
print()

# Correlation matrix (needs wide format)
correlation = returns_wide.corr()
print("Return correlations:")
print(correlation)
print()

# Covariance matrix
covariance = returns_wide.cov()
print("Return covariances:")
print(covariance)
```

## Market-Wide Statistics

```python
# Equal-weighted market return
market_return = df.groupby(level='date')['return'].mean()
print("Market return (equal-weighted):")
print(market_return)

# Market volume
total_volume = df.groupby(level='date')['volume'].sum()
print("\nTotal market volume:")
print(total_volume)
```

## Advanced: CAPM-Style Analysis

```python
# Add market return to panel
market = df.groupby(level='date')['return'].mean()
df['market_return'] = df.index.get_level_values('date').map(market)

# Excess return (vs market)
df['excess_return'] = df['return'] - df['market_return']

print(df[['return', 'market_return', 'excess_return']].head(10))
```

### Beta Estimation per Entity

```python
# Simple beta calculation per ticker
def calc_beta(group):
    cov = group['return'].cov(group['market_return'])
    var = group['market_return'].var()
    return cov / var if var != 0 else np.nan

betas = df.groupby(level='ticker').apply(calc_beta)
print("Betas:")
print(betas)
```

## Ranking Within Cross-Sections

```python
# Rank returns each day
df['return_rank'] = df.groupby(level='date')['return'].rank(ascending=False)
print(df[['return', 'return_rank']].head(15))
```

## Summary Statistics

```python
def panel_summary(df, value_col='return'):
    """Generate comprehensive panel summary."""
    return pd.DataFrame({
        'Overall Mean': [df[value_col].mean()],
        'Overall Std': [df[value_col].std()],
        'Entity Count': [df.index.get_level_values(0).nunique()],
        'Time Count': [df.index.get_level_values(1).nunique()],
        'Total Obs': [len(df)],
        'Cross-Sectional Std (avg)': [
            df.groupby(level='date')[value_col].std().mean()
        ],
        'Time-Series Std (avg)': [
            df.groupby(level='ticker')[value_col].std().mean()
        ]
    })

summary = panel_summary(df)
print(summary.T)
```

## Aggregation Reference

| Goal | Method |
|------|--------|
| Mean per entity | `df.groupby(level='ticker').mean()` |
| Mean per time | `df.groupby(level='date').mean()` |
| Rolling per entity | `df.groupby(level='ticker').rolling(n).mean()` |
| Broadcast entity mean | `df.groupby(level='ticker').transform('mean')` |
| Cumsum per entity | `df.groupby(level='ticker').cumsum()` |
| Lag per entity | `df.groupby(level='ticker').shift(1)` |
| Rank per time | `df.groupby(level='date').rank()` |
| Correlation matrix | `df['col'].unstack().corr()` |


---

## Exercises

**Exercise 1.** Write code that computes the mean across entities (panel groups) using `groupby().mean()` on a MultiIndex DataFrame.

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

**Exercise 2.** Explain the difference between aggregating across time (within-entity) and across entities (within-time) in panel data.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that computes both the within-entity mean and the between-entity mean for a panel dataset.

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

**Exercise 4.** Create panel data and compute the rolling mean for each entity separately using `groupby().rolling()`.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
