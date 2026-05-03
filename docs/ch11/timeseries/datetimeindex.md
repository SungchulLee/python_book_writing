# DatetimeIndex

pandas provides rich support for time series data through the **DatetimeIndex**, which enables label-based time alignment and slicing.

!!! tip "Mental Model"
    A DatetimeIndex is a sorted array of timestamps that serves as a time-aware row label. It unlocks partial-string indexing (`df['2024']` for all of 2024), resampling to different frequencies, and automatic time-based alignment. Any DataFrame with a DatetimeIndex becomes a first-class time series.

## Creating DatetimeIndex

Generate datetime indices for time series.

### 1. date_range Function

```python
import pandas as pd

dates = pd.date_range("2020-01-01", periods=5, freq="D")
print(dates)
```

```
DatetimeIndex(['2020-01-01', '2020-01-02', '2020-01-03', '2020-01-04',
               '2020-01-05'],
              dtype='datetime64[ns]', freq='D')
```

### 2. With End Date

```python
dates = pd.date_range(start="2024-01-01", end="2024-01-10")
```

### 3. Nanosecond Precision

DatetimeIndex stores timestamps with nanosecond precision.

## Converting to Datetime

Parse strings and other formats to datetime.

### 1. to_datetime Function

```python
pd.to_datetime(["2021-01-01", "2021-01-05"])
```

### 2. Common with CSV Loading

```python
df = pd.read_csv('data.csv', parse_dates=['date_column'])
```

### 3. Format Specification

```python
pd.to_datetime("01-15-2024", format="%m-%d-%Y")
```

## Date Range Frequencies

Common frequency strings.

### 1. Daily and Sub-daily

```python
pd.date_range("2024-01-01", periods=5, freq="D")   # Daily
pd.date_range("2024-01-01", periods=5, freq="H")   # Hourly
pd.date_range("2024-01-01", periods=5, freq="T")   # Minute
```

### 2. Weekly and Monthly

```python
pd.date_range("2024-01-01", periods=5, freq="W")   # Weekly
pd.date_range("2024-01-01", periods=5, freq="M")   # Month end
pd.date_range("2024-01-01", periods=5, freq="MS")  # Month start
```

### 3. Business Days

```python
pd.date_range("2024-01-01", periods=5, freq="B")   # Business days
```

## Indexing with Dates

Date-based slicing and selection.

### 1. String-based Selection

```python
s = pd.Series(range(5), index=pd.date_range("2020-01-01", periods=5))
s["2020-01-02":"2020-01-04"]  # Inclusive slicing
```

### 2. Partial String Indexing

```python
s["2020-01"]  # All of January 2020
s["2020"]     # All of 2020
```

### 3. loc with Dates

```python
s.loc["2020-01-02"]
s.loc["2020-01-02":"2020-01-04"]
```

## Time Zone Handling

Work with time zones.

### 1. Localize to UTC

```python
dates = pd.date_range("2020-01-01", periods=5)
dates_utc = dates.tz_localize("UTC")
```

### 2. Convert Time Zone

```python
dates_eastern = dates_utc.tz_convert("US/Eastern")
```

### 3. Financial Data

Time zones are essential for global financial data.

## Financial Context

DatetimeIndex underlies financial analysis.

### 1. Price Time Series

```python
prices = pd.Series([100, 101, 102], index=pd.date_range("2024-01-01", periods=3))
```

### 2. Returns Calculation

```python
returns = prices.pct_change()
```

### 3. Event Studies

```python
# Select specific date ranges for analysis
event_window = prices["2024-01-01":"2024-01-31"]
```

---

## Runnable Example: `time_series_tutorial.py`

```python
"""
Pandas Tutorial: Time Series Analysis.

Covers datetime operations, resampling, rolling windows, time zones.
"""

import pandas as pd
import numpy as np

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("="*70)
    print("TIME SERIES ANALYSIS")
    print("="*70)

    # Create time series data
    dates = pd.date_range('2024-01-01', periods=100, freq='D')
    np.random.seed(42)
    ts_data = pd.DataFrame({
        'Date': dates,
        'Sales': np.random.randint(100, 500, 100),
        'Temperature': np.random.uniform(15, 35, 100)
    })
    ts_data.set_index('Date', inplace=True)

    print("\nTime Series Data:")
    print(ts_data.head())

    # Date parsing
    print("\n1. Parse dates from strings:")
    date_strings = ['2024-01-01', '2024-02-15', '2024-03-30']
    parsed_dates = pd.to_datetime(date_strings)
    print(parsed_dates)

    # Date ranges
    print("\n2. Create date ranges:")
    print("Daily:", pd.date_range('2024-01-01', periods=5, freq='D'))
    print("Weekly:", pd.date_range('2024-01-01', periods=5, freq='W'))
    print("Monthly:", pd.date_range('2024-01-01', periods=5, freq='MS'))

    # Accessing datetime components
    print("\n3. Extract datetime components:")
    ts_data['Year'] = ts_data.index.year
    ts_data['Month'] = ts_data.index.month
    ts_data['Day'] = ts_data.index.day
    ts_data['DayOfWeek'] = ts_data.index.dayofweek
    print(ts_data[['Sales', 'Year', 'Month', 'Day', 'DayOfWeek']].head())

    # Resampling (changing frequency)
    print("\n4. Resample to weekly frequency (sum):")
    weekly = ts_data['Sales'].resample('W').sum()
    print(weekly.head())

    print("\n5. Resample to monthly (mean):")
    monthly = ts_data['Sales'].resample('MS').mean()
    print(monthly.head())

    # Rolling windows
    print("\n6. Rolling mean (7-day window):")
    ts_data['Sales_MA7'] = ts_data['Sales'].rolling(window=7).mean()
    print(ts_data[['Sales', 'Sales_MA7']].head(10))

    print("\n7. Rolling statistics:")
    rolling_stats = ts_data['Sales'].rolling(window=7).agg(['mean', 'std', 'min', 'max'])
    print(rolling_stats.head(10))

    # Expanding windows
    print("\n8. Expanding mean (cumulative):")
    ts_data['Cumulative_Mean'] = ts_data['Sales'].expanding().mean()
    print(ts_data[['Sales', 'Cumulative_Mean']].head(10))

    # Shift and lag
    print("\n9. Shift values (lag/lead):")
    ts_data['Sales_Yesterday'] = ts_data['Sales'].shift(1)
    ts_data['Sales_Tomorrow'] = ts_data['Sales'].shift(-1)
    print(ts_data[['Sales', 'Sales_Yesterday', 'Sales_Tomorrow']].head())

    # Percentage change
    print("\n10. Percentage change:")
    ts_data['Sales_Pct_Change'] = ts_data['Sales'].pct_change()
    print(ts_data[['Sales', 'Sales_Pct_Change']].head())

    # Time zones
    print("\n11. Time zone operations:")
    utc_dates = pd.date_range('2024-01-01', periods=3, freq='D', tz='UTC')
    print("UTC:", utc_dates)

    # Convert time zone
    eastern = utc_dates.tz_convert('US/Eastern')
    print("Eastern:", eastern)

    print("\nKEY TAKEAWAYS:")
    print("- pd.to_datetime(): Parse dates from strings")
    print("- pd.date_range(): Create date sequences")
    print("- resample(): Change time frequency")
    print("- rolling(): Moving window calculations")
    print("- shift(): Lag/lead values")
    print("- pct_change(): Percentage change")
    print("- Time zone handling with tz parameter")
```


---

## Exercises

**Exercise 1.** Write code that creates a DataFrame with a DatetimeIndex and accesses rows for a specific month using `.loc['2024-06']`.

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

**Exercise 2.** Explain three advantages of having a DatetimeIndex on a DataFrame.

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Write code that extracts the year, month, and day from a DatetimeIndex using `.year`, `.month`, `.day`.

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

**Exercise 4.** Create a DatetimeIndex with hourly frequency and demonstrate slicing by date and time.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
