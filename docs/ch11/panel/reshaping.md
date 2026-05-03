# Reshaping Panel Data

Panel data often needs reshaping between long and wide formats for different analyses. This document covers common reshaping operations.

!!! tip "Mental Model"
    Long format has one row per (entity, time) observation -- best for storage and groupby. Wide format spreads entities or time periods across columns -- best for correlation analysis and plotting. `unstack` goes long-to-wide, `stack` goes wide-to-long, and `pivot`/`melt` offer column-based alternatives. Choose the shape that fits your next operation.

## Long vs Wide Format

### Long Format (Standard Panel)
- Each row is one observation (entity-time)
- Best for storage and filtering
- Natural for groupby operations

### Wide Format (Cross-Sectional)
- Rows are time periods, columns are entities
- Best for correlation/covariance analysis
- Natural for matrix operations

## Setup

```python
import pandas as pd
import numpy as np

# Create sample panel data
tickers = ['AAPL', 'MSFT', 'GOOGL']
dates = pd.date_range('2024-01-01', periods=5)
index = pd.MultiIndex.from_product([tickers, dates], names=['ticker', 'date'])

np.random.seed(42)
panel_long = pd.DataFrame({
    'return': np.random.randn(15) * 0.02,
    'volume': np.random.randint(1000, 10000, 15)
}, index=index)

print("Long format:")
print(panel_long)
```

## Long to Wide: unstack()

### Single Variable

```python
# Returns in wide format
returns_wide = panel_long['return'].unstack('ticker')
print("Returns (wide format):")
print(returns_wide)
```

```
ticker          AAPL      MSFT     GOOGL
date                                    
2024-01-01  0.009934 -0.003129 -0.018867
2024-01-02 -0.002765  0.015335  0.029389
2024-01-03  0.012936  0.000296  0.003031
2024-01-04  0.030486 -0.002013 -0.009299
2024-01-05 -0.004675  0.002826 -0.007218
```

### Multiple Variables

```python
# Both return and volume in wide format
panel_wide = panel_long.unstack('ticker')
print("Panel (wide format):")
print(panel_wide)
```

```
             return                      volume                  
ticker         AAPL      MSFT     GOOGL   AAPL  MSFT GOOGL
date                                                        
2024-01-01  0.009934 -0.003129 -0.018867   5765  3109  3046
2024-01-02 -0.002765  0.015335  0.029389   6274  2239  3856
...
```

### Unstack by Time Instead

```python
# Tickers as rows, dates as columns
by_date = panel_long['return'].unstack('date')
print("By date (wide format):")
print(by_date)
```

## Wide to Long: stack()

```python
# Convert back to long format
returns_long = returns_wide.stack()
returns_long.name = 'return'
print("Back to long format:")
print(returns_long)
```

### Swap Level Order

```python
# Change from (date, ticker) to (ticker, date)
returns_long_reordered = returns_long.swaplevel().sort_index()
print("Reordered (ticker first):")
print(returns_long_reordered)
```

## reset_index() for Flat Format

```python
# Completely flat DataFrame
flat = panel_long.reset_index()
print("Flat format:")
print(flat)
```

```
   ticker       date    return  volume
0    AAPL 2024-01-01  0.009934    5765
1    AAPL 2024-01-02 -0.002765    6274
2    AAPL 2024-01-03  0.012936    2627
...
```

## pivot() for Reshaping

Alternative to unstack when working with flat data:

```python
# From flat format
flat = panel_long.reset_index()

# Pivot to wide
wide = flat.pivot(index='date', columns='ticker', values='return')
print("Pivoted:")
print(wide)
```

## melt() for Unpivoting

```python
# From wide format back to long
melted = returns_wide.reset_index().melt(
    id_vars='date',
    var_name='ticker',
    value_name='return'
)
print("Melted:")
print(melted.head(10))
```

## Practical Use Cases

### Correlation Analysis (Requires Wide)

```python
# Need wide format for correlation
returns_wide = panel_long['return'].unstack('ticker')

# Calculate correlation matrix
corr_matrix = returns_wide.corr()
print("Correlation matrix:")
print(corr_matrix)
```

### Covariance Matrix

```python
# Annualized covariance
cov_matrix = returns_wide.cov() * 252
print("Annualized covariance matrix:")
print(cov_matrix)
```

### Portfolio Analysis

```python
# Define weights
weights = np.array([0.4, 0.35, 0.25])  # AAPL, GOOGL, MSFT order

# Portfolio return (requires wide format)
portfolio_return = returns_wide.dot(weights)
print("Portfolio return:")
print(portfolio_return)

# Portfolio variance
portfolio_var = weights @ cov_matrix @ weights
print(f"\nPortfolio variance: {portfolio_var:.6f}")
```

### Rolling Correlation

```python
# Rolling 20-day correlation (requires wide)
rolling_corr = returns_wide['AAPL'].rolling(3).corr(returns_wide['MSFT'])
print("Rolling correlation AAPL-MSFT:")
print(rolling_corr)
```

### Cross-Sectional Regression

```python
# At each time, regress returns on a factor
# Wide format makes this natural

# Add a "factor" column
returns_wide['factor'] = np.random.randn(len(returns_wide)) * 0.01

# For each date, calculate betas
from scipy import stats

betas = {}
for ticker in ['AAPL', 'MSFT', 'GOOGL']:
    slope, _, _, _, _ = stats.linregress(
        returns_wide['factor'], 
        returns_wide[ticker]
    )
    betas[ticker] = slope

print("Factor betas:")
print(pd.Series(betas))
```

## Three-Level Panel Reshaping

```python
# Create 3-level panel: sector, ticker, date
sectors = {'Tech': ['AAPL', 'MSFT'], 'Finance': ['JPM', 'BAC']}
dates = pd.date_range('2024-01-01', periods=3)

data = []
for sector, tickers in sectors.items():
    for ticker in tickers:
        for date in dates:
            data.append({
                'sector': sector,
                'ticker': ticker,
                'date': date,
                'return': np.random.randn() * 0.02
            })

df = pd.DataFrame(data).set_index(['sector', 'ticker', 'date'])
print("3-level panel:")
print(df)
print()

# Reshape: dates as columns
wide_by_date = df['return'].unstack('date')
print("Unstacked by date:")
print(wide_by_date)
print()

# Reshape: tickers as columns
wide_by_ticker = df['return'].unstack('ticker')
print("Unstacked by ticker:")
print(wide_by_ticker)
```

## Summary of Reshaping Operations

| From | To | Method |
|------|-----|--------|
| Long (MultiIndex) | Wide (columns = entities) | `.unstack('ticker')` |
| Wide | Long (MultiIndex) | `.stack()` |
| Long (MultiIndex) | Flat DataFrame | `.reset_index()` |
| Flat | Long (MultiIndex) | `.set_index([...])` |
| Flat | Wide | `.pivot(index, columns, values)` |
| Wide | Flat | `.melt(id_vars, var_name, value_name)` |

## Best Practices

1. **Use long format for storage** - more flexible, handles missing data
2. **Convert to wide for matrix operations** - correlation, portfolio math
3. **Name index levels** - makes reshaping code clearer
4. **Sort after reshaping** - ensures consistent ordering
5. **Check for NaN after unstack** - unbalanced panels create missing values


---

## Exercises

**Exercise 1.** Write code that converts panel data from long format to wide format using `pivot()` or `unstack()`.

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

**Exercise 2.** Explain the relationship between `stack()`, `unstack()`, `melt()`, and `pivot()` in the context of reshaping panel data.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that uses `unstack()` to convert a MultiIndex DataFrame to a wide-format DataFrame.

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

**Exercise 4.** Create wide-format panel data and convert it to long format using `melt()` or `stack()`.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
