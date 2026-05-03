# Saving DataFrames

Export DataFrames to various file formats for storage and sharing.

!!! tip "Mental Model"
    Every `to_*` method is the mirror of a `read_*` function. `to_csv` serializes to text, `to_parquet` serializes to efficient binary, `to_excel` writes spreadsheets. The key decision is whether you need human-readable output (CSV) or fast, type-preserving storage (Parquet). Always check `index=False` if you do not want the index written as a column.

## to_csv

Save DataFrame to CSV file.

### 1. Basic Save

```python
import pandas as pd

df.to_csv('output.csv')
```

### 2. Without Index

```python
df.to_csv('output.csv', index=False)
```

### 3. Custom Separator

```python
df.to_csv('output.tsv', sep='\t')
```

## to_csv Keywords

Customize CSV output.

### 1. Select Columns

```python
df.to_csv('output.csv', columns=['Name', 'Age'])
```

### 2. Handle Missing

```python
df.to_csv('output.csv', na_rep='NULL')
```

### 3. Float Format

```python
df.to_csv('output.csv', float_format='%.2f')
```

## to_excel

Save DataFrame to Excel file.

### 1. Basic Save

```python
df.to_excel('output.xlsx')
```

### 2. Specify Sheet Name

```python
df.to_excel('output.xlsx', sheet_name='Data')
```

### 3. Without Index

```python
df.to_excel('output.xlsx', index=False)
```

## Multiple Sheets

Save multiple DataFrames to one Excel file.

### 1. ExcelWriter

```python
with pd.ExcelWriter('output.xlsx') as writer:
    df1.to_excel(writer, sheet_name='Sheet1')
    df2.to_excel(writer, sheet_name='Sheet2')
    df3.to_excel(writer, sheet_name='Sheet3')
```

### 2. Append Mode

```python
with pd.ExcelWriter('output.xlsx', mode='a') as writer:
    df_new.to_excel(writer, sheet_name='NewSheet')
```

### 3. Engine Selection

```python
# openpyxl for .xlsx, xlsxwriter for formatting
with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer)
```

## to_json

Save DataFrame to JSON file.

### 1. Basic Save

```python
df.to_json('output.json')
```

### 2. Orient Options

```python
df.to_json('output.json', orient='records')  # List of dicts
df.to_json('output.json', orient='columns')  # Dict of lists
df.to_json('output.json', orient='index')    # Dict of dicts
```

### 3. Indent for Readability

```python
df.to_json('output.json', orient='records', indent=2)
```

## to_pickle

Save DataFrame in pickle format.

### 1. Save Pickle

```python
df.to_pickle('output.pkl')
```

### 2. Load Pickle

```python
df = pd.read_pickle('output.pkl')
```

### 3. Compression

```python
df.to_pickle('output.pkl.gz', compression='gzip')
```

## to_parquet

Save in Parquet format (efficient columnar storage).

### 1. Basic Save

```python
df.to_parquet('output.parquet')
```

### 2. Compression

```python
df.to_parquet('output.parquet', compression='snappy')
```

### 3. Read Back

```python
df = pd.read_parquet('output.parquet')
```

## Financial Example

Save stock data workflow.

### 1. Download and Save

```python
import yfinance as yf

ticker = 'WMT'
df = yf.Ticker(ticker).history(start='2020-01-01', end='2020-12-31')

# Save to CSV
df.to_csv(f'{ticker}.csv')

# Save to Excel
df.to_excel(f'{ticker}.xlsx', sheet_name='stocks')
```

### 2. Multiple Tickers

```python
tickers = ['AAPL', 'MSFT', 'GOOGL']

with pd.ExcelWriter('portfolio.xlsx') as writer:
    for ticker in tickers:
        df = yf.Ticker(ticker).history(period='1y')
        df.to_excel(writer, sheet_name=ticker)
```

### 3. Pickle for Speed

```python
# Faster save/load for large DataFrames
df.to_pickle('large_data.pkl')
df = pd.read_pickle('large_data.pkl')
```

## Format Comparison

Choose the right format.

### 1. CSV

- Pros: Universal, human-readable
- Cons: No type preservation, slow for large data

### 2. Excel

- Pros: Business-friendly, multiple sheets
- Cons: Slower, file size limits

### 3. Pickle

- Pros: Fast, preserves types
- Cons: Python-only, security concerns

### 4. Parquet

- Pros: Fast, compressed, columnar
- Cons: Less universal

---

## Exercises

**Exercise 1.**
Create a DataFrame with columns `'ticker'`, `'date'`, and `'close'` containing three rows of sample stock data. Save it to a CSV file without the index, then read it back and verify the data matches the original.

??? success "Solution to Exercise 1"
    Save with `index=False` and read back with `pd.read_csv`.

        import pandas as pd

        df = pd.DataFrame({
            'ticker': ['AAPL', 'MSFT', 'GOOGL'],
            'date': ['2024-01-01', '2024-01-01', '2024-01-01'],
            'close': [150.0, 350.0, 140.0]
        })
        df.to_csv('stocks.csv', index=False)
        df_loaded = pd.read_csv('stocks.csv')
        print(df_loaded)
        print(df.equals(df_loaded))  # True

---

**Exercise 2.**
Given a dictionary of three DataFrames (one per ticker), write them to a single Excel file where each ticker has its own sheet. Use `pd.ExcelWriter` as a context manager.

??? success "Solution to Exercise 2"
    Use `pd.ExcelWriter` with each DataFrame written to a named sheet.

        import pandas as pd
        import numpy as np

        dfs = {
            'AAPL': pd.DataFrame({'close': np.random.uniform(140, 160, 5)}),
            'MSFT': pd.DataFrame({'close': np.random.uniform(340, 360, 5)}),
            'GOOGL': pd.DataFrame({'close': np.random.uniform(130, 150, 5)}),
        }

        with pd.ExcelWriter('portfolio.xlsx') as writer:
            for ticker, df in dfs.items():
                df.to_excel(writer, sheet_name=ticker, index=False)

---

**Exercise 3.**
Create a DataFrame with 1000 rows and columns `'id'` (int), `'value'` (float), and `'category'` (string). Save it as both CSV and Parquet. Compare the file sizes and explain why Parquet is typically smaller.

??? success "Solution to Exercise 3"
    Create sample data, save in both formats, and compare sizes.

        import pandas as pd
        import numpy as np
        import os

        np.random.seed(42)
        df = pd.DataFrame({
            'id': range(1000),
            'value': np.random.randn(1000),
            'category': np.random.choice(['A', 'B', 'C'], 1000)
        })

        df.to_csv('data.csv', index=False)
        df.to_parquet('data.parquet')

        csv_size = os.path.getsize('data.csv')
        parquet_size = os.path.getsize('data.parquet')
        print(f"CSV size: {csv_size / 1e3:.1f} KB")
        print(f"Parquet size: {parquet_size / 1e3:.1f} KB")
        # Parquet is smaller because it uses columnar storage
        # with built-in compression and schema encoding.
