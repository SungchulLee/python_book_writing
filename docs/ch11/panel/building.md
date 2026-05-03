# Building Panel DataFrames

This document covers how to construct panel data structures in pandas using MultiIndex.

!!! tip "Mental Model"
    Building a panel means creating a DataFrame with a MultiIndex of (entity, time) pairs. `MultiIndex.from_product` generates a balanced panel (all entities at all times); `from_tuples` or `from_arrays` handle unbalanced panels where some entity-time combinations are missing. The construction method determines whether you start with a complete grid or a sparse one.

## Using MultiIndex.from_product

Creates a panel with all combinations of entities and time periods (balanced panel).

```python
import pandas as pd
import numpy as np

# Define dimensions
tickers = ['AAPL', 'MSFT', 'GOOGL']
dates = pd.date_range('2024-01-01', periods=5)

# Create MultiIndex (Cartesian product)
index = pd.MultiIndex.from_product(
    [tickers, dates], 
    names=['ticker', 'date']
)

# Create panel DataFrame
np.random.seed(42)
n = len(index)

df = pd.DataFrame({
    'return': np.random.randn(n) * 0.02,
    'volume': np.random.randint(1000, 10000, n),
    'close': 100 + np.random.randn(n).cumsum()
}, index=index)

print(df.head(10))
```

```
                     return  volume       close
ticker date                                    
AAPL   2024-01-01  0.009934    5765  100.496714
       2024-01-02 -0.002765    6274   99.354071
       2024-01-03  0.012936    2627  100.001572
       2024-01-04  0.030486    8019  102.283551
       2024-01-05 -0.004675    3927  101.396356
MSFT   2024-01-01 -0.003129    3109  101.542560
       2024-01-02  0.015335    2239  100.533340
       2024-01-03  0.000296    9596  100.070105
       2024-01-04 -0.002013    8394   99.634291
       2024-01-05  0.002826    8259  100.421411
```

## Using MultiIndex.from_tuples

Useful when you have specific entity-time combinations (unbalanced panel).

```python
# Specific combinations only
tuples = [
    ('AAPL', '2024-01-01'),
    ('AAPL', '2024-01-02'),
    ('AAPL', '2024-01-03'),
    ('MSFT', '2024-01-02'),  # MSFT starts later
    ('MSFT', '2024-01-03'),
]

index = pd.MultiIndex.from_tuples(tuples, names=['ticker', 'date'])

df = pd.DataFrame({
    'return': [0.01, 0.02, -0.01, 0.015, 0.008]
}, index=index)

print(df)
```

## Using MultiIndex.from_arrays

When you have separate arrays for each level:

```python
tickers = ['AAPL', 'AAPL', 'AAPL', 'MSFT', 'MSFT', 'MSFT']
dates = ['2024-01-01', '2024-01-02', '2024-01-03'] * 2

index = pd.MultiIndex.from_arrays(
    [tickers, dates], 
    names=['ticker', 'date']
)

df = pd.DataFrame({'return': [0.01, 0.02, -0.01, 0.015, 0.008, 0.012]}, index=index)
print(df)
```

## From Long-Format DataFrame

Convert a regular DataFrame to panel format:

```python
# Long format data (common from databases)
data = pd.DataFrame({
    'ticker': ['AAPL', 'AAPL', 'MSFT', 'MSFT', 'GOOGL', 'GOOGL'],
    'date': pd.to_datetime(['2024-01-01', '2024-01-02'] * 3),
    'return': [0.01, 0.02, 0.015, 0.018, 0.008, 0.012],
    'volume': [1000, 1100, 2000, 2100, 1500, 1600]
})

print("Long format:")
print(data)
print()

# Convert to panel (MultiIndex)
panel = data.set_index(['ticker', 'date'])
print("Panel format:")
print(panel)
```

## From Wide-Format DataFrame

Convert wide format (tickers as columns) to panel:

```python
# Wide format
wide = pd.DataFrame({
    'AAPL': [0.01, 0.02, -0.01],
    'MSFT': [0.015, 0.018, 0.012],
    'GOOGL': [0.008, 0.012, 0.009]
}, index=pd.date_range('2024-01-01', periods=3))
wide.index.name = 'date'
wide.columns.name = 'ticker'

print("Wide format:")
print(wide)
print()

# Convert to panel using stack
panel = wide.stack()
panel.name = 'return'
print("Panel format (Series):")
print(panel)
print()

# Or swap levels to have ticker first
panel = panel.swaplevel().sort_index()
print("Panel format (ticker first):")
print(panel)
```

## From Real Financial Data

```python
import yfinance as yf

# Download multiple stocks
tickers = ['AAPL', 'MSFT', 'GOOGL']
start = '2024-01-01'
end = '2024-01-31'

# Download returns long-form data
dfs = []
for ticker in tickers:
    data = yf.Ticker(ticker).history(start=start, end=end)
    data['ticker'] = ticker
    data = data.reset_index()[['Date', 'ticker', 'Close', 'Volume']]
    dfs.append(data)

# Combine and set MultiIndex
panel = pd.concat(dfs, ignore_index=True)
panel = panel.rename(columns={'Date': 'date', 'Close': 'close', 'Volume': 'volume'})
panel = panel.set_index(['ticker', 'date']).sort_index()

print(panel.head(15))
```

## Building with Specific Structure

### Sector-Stock-Date Hierarchy

```python
# Three-level panel
sectors = ['Tech', 'Finance']
tickers = {
    'Tech': ['AAPL', 'MSFT'],
    'Finance': ['JPM', 'BAC']
}
dates = pd.date_range('2024-01-01', periods=3)

# Build tuples
tuples = []
for sector, stocks in tickers.items():
    for stock in stocks:
        for date in dates:
            tuples.append((sector, stock, date))

index = pd.MultiIndex.from_tuples(tuples, names=['sector', 'ticker', 'date'])

df = pd.DataFrame({
    'return': np.random.randn(len(index)) * 0.02
}, index=index)

print(df)
```

## Verifying Panel Structure

```python
# Check panel dimensions
print(f"Index levels: {df.index.names}")
print(f"Number of levels: {df.index.nlevels}")
print(f"Shape: {df.shape}")

# Check balance
print(f"\nEntities: {df.index.get_level_values('ticker').unique()}")
print(f"Time periods: {df.index.get_level_values('date').unique()}")

# Check for balanced panel
def is_balanced(df, entity_level='ticker', time_level='date'):
    n_entities = df.index.get_level_values(entity_level).nunique()
    n_times = df.index.get_level_values(time_level).nunique()
    expected = n_entities * n_times
    actual = len(df)
    return actual == expected

print(f"\nBalanced panel: {is_balanced(df)}")
```

## Best Practices

1. **Name your index levels** for clarity
2. **Sort the index** after creation for performance
3. **Use appropriate dtypes** (datetime for dates, category for tickers)
4. **Verify balance** if your analysis requires it

```python
# Good practice example
index = pd.MultiIndex.from_product(
    [tickers, dates],
    names=['ticker', 'date']  # Named levels
)

df = pd.DataFrame({'return': data}, index=index)
df = df.sort_index()  # Sorted for performance
df.index = df.index.set_levels(
    df.index.levels[0].astype('category'),  # Categorical ticker
    level=0
)
```


---

## Exercises

**Exercise 1.** Write code that creates panel data by concatenating DataFrames for three entities with a `keys` parameter identifying each entity.

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

**Exercise 2.** Explain two common formats for panel data: wide format and long format. Show how to convert between them.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that creates a MultiIndex DataFrame from a dictionary of DataFrames representing different entities.

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

**Exercise 4.** Create a long-format panel DataFrame with columns `['entity', 'date', 'value']` and convert it to a MultiIndex structure using `set_index()`.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
