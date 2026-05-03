# fillna Method

The `fillna()` method replaces missing values with specified values. It is one of the most common approaches to handling missing data.

!!! tip "Mental Model"
    `fillna()` is the "plug the hole" strategy: every NaN is replaced with a value you specify. Pass a scalar to fill all gaps with the same number, a dict to fill each column differently, or a Series/DataFrame to fill position-by-position. The choice of fill value encodes your assumption about what the missing data would have been.

## Single Value Fill

Replace all NaN values with a single value.

### 1. Constant Value

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'temperature': [21, np.nan, 25, np.nan],
    'humidity': [65, 68, np.nan, 75]
})

dg = df.fillna(0)
print(dg)
```

```
   temperature  humidity
0         21.0      65.0
1          0.0      68.0
2         25.0       0.0
3          0.0      75.0
```

### 2. Mean Fill

```python
df['temperature'].fillna(df['temperature'].mean())
```

### 3. Median Fill

```python
df['temperature'].fillna(df['temperature'].median())
```

## Column-specific Fill

Use a dictionary to specify different fill values per column.

### 1. Dictionary Mapping

```python
url = "https://raw.githubusercontent.com/codebasics/py/master/pandas/5_handling_missing_data_fillna_dropna_interpolate/weather_data.csv"
df = pd.read_csv(url, index_col='day', parse_dates=True)

dg = df.fillna({
    "temperature": 30,
    "windspeed": df.windspeed.mean(),
    "event": "No Event",
})
print(dg)
```

### 2. Computed Values

```python
fill_values = {
    'temperature': df['temperature'].mean(),
    'humidity': df['humidity'].median()
}
df.fillna(fill_values)
```

### 3. Conditional Fill

```python
df['temperature'] = df['temperature'].fillna(
    df.groupby('region')['temperature'].transform('mean')
)
```

## inplace Parameter

Modify the DataFrame directly without creating a copy.

### 1. Without inplace

```python
dg = df.fillna(0)  # Returns new DataFrame
# df is unchanged
```

### 2. With inplace

```python
df.fillna(0, inplace=True)  # Modifies df directly
```

### 3. Modern Practice

Prefer reassignment over `inplace=True`:

```python
df = df.fillna(0)  # More explicit
```

## LeetCode Example

Fill referee_id with 0 for customers without referrer.

### 1. Problem Context

```python
customer = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],
    'referee_id': [1.0, 2.0, np.nan, 3.0, np.nan]
})
```

### 2. Fill NaN Values

```python
customer["referee_id"].fillna(0)
```

### 3. Result

```
0    1.0
1    2.0
2    0.0
3    3.0
4    0.0
Name: referee_id, dtype: float64
```

## Dictionary Fill Example

Fill missing prices with 0.0 in sales data.

### 1. Sample Data

```python
sold_with_prices = pd.DataFrame({
    'product_id': [1, 1, 2],
    'purchase_date': ['2024-01-15', '2024-05-10', '2024-07-01'],
    'units': [10, 5, 8],
    'price': [100, None, 180]
})
```

### 2. Fill with Dictionary

```python
sold_with_prices.fillna({'price': 0.0}, inplace=True)
```

### 3. Resulting DataFrame

```
   product_id purchase_date  units  price
0           1    2024-01-15     10  100.0
1           1    2024-05-10      5    0.0
2           2    2024-07-01      8  180.0
```

---

## Runnable Example: `data_preprocessing_workflow.py`

```python
"""
Data Preprocessing Workflow: Cleaning Real-World Data

A practical workflow demonstrating common data cleaning operations
that are needed before analysis or machine learning.

Steps covered:
1. Handling missing values (detect, fill, drop)
2. Removing duplicates
3. String column splitting and extraction
4. Value replacement and mapping
5. Normalization (min-max scaling, z-score standardization)
6. Binning continuous variables

Based on Python-100-Days Day66-80 day04.ipynb data cleaning examples.
"""

import numpy as np
import pandas as pd


# =============================================================================
# Step 1: Create Sample Messy Data
# =============================================================================

def create_sample_data() -> pd.DataFrame:
    """Create a messy DataFrame that needs preprocessing."""
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'Alice', 'Diana',
                 'Eve', 'Frank', None, 'Grace', 'Bob'],
        'age': [28, 35, None, 28, 42, 31, None, 29, 38, 35],
        'salary_range': ['50K-70K', '80K-100K', '60K-80K', '50K-70K',
                         '90K-120K', '70K-90K', '55K-75K', '65K-85K',
                         '100K-130K', '80K-100K'],
        'department': ['Engineering', 'Marketing', 'Engineering', 'Engineering',
                       'Management', 'marketing', 'engineering', 'Sales',
                       'Management', 'Marketing'],
        'score': [85, 92, 78, 85, 95, 88, 73, None, 91, 92],
        'join_date': ['2020-03-15', '2019-07-22', '2021-01-10', '2020-03-15',
                      '2018-11-05', '2020-08-17', '2022-02-28', '2021-06-12',
                      '2019-03-08', '2019-07-22'],
    }
    return pd.DataFrame(data)


# =============================================================================
# Step 2: Inspect and Report Issues
# =============================================================================

def inspect_data(df: pd.DataFrame) -> None:
    """Report data quality issues."""
    print("=== Data Inspection ===")
    print(f"Shape: {df.shape}")
    print(f"\nMissing values:\n{df.isnull().sum()}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"\nData types:\n{df.dtypes}")
    print()


# =============================================================================
# Step 3: Clean the Data
# =============================================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply a sequence of cleaning operations."""
    df = df.copy()

    # --- Remove duplicates ---
    print("--- Removing Duplicates ---")
    before = len(df)
    df = df.drop_duplicates()
    print(f"  Removed {before - len(df)} duplicate rows")

    # --- Handle missing values ---
    print("\n--- Handling Missing Values ---")

    # Drop rows where name is missing (can't identify)
    df = df.dropna(subset=['name'])
    print(f"  Dropped rows with missing name")

    # Fill numeric missing values with median
    for col in ['age', 'score']:
        median_val = df[col].median()
        filled = df[col].isnull().sum()
        df[col] = df[col].fillna(median_val)
        print(f"  Filled {filled} missing {col} with median ({median_val})")

    # --- Standardize text columns ---
    print("\n--- Standardizing Text ---")
    df['department'] = df['department'].str.strip().str.title()
    print(f"  Departments: {df['department'].unique().tolist()}")

    # --- Parse dates ---
    print("\n--- Parsing Dates ---")
    df['join_date'] = pd.to_datetime(df['join_date'])
    print(f"  Converted join_date to datetime")

    # --- Extract salary range into min/max columns ---
    print("\n--- Extracting Salary Range ---")
    salary_split = df['salary_range'].str.replace('K', '').str.split('-', expand=True)
    df['salary_min'] = salary_split[0].astype(float) * 1000
    df['salary_max'] = salary_split[1].astype(float) * 1000
    df['salary_mid'] = (df['salary_min'] + df['salary_max']) / 2
    print(f"  Created salary_min, salary_max, salary_mid columns")

    return df


# =============================================================================
# Step 4: Normalize Numeric Columns
# =============================================================================

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply normalization techniques."""
    df = df.copy()

    print("\n--- Normalization ---")

    # Min-Max Scaling: scales to [0, 1]
    # formula: (x - min) / (max - min)
    col = 'score'
    min_val, max_val = df[col].min(), df[col].max()
    df['score_minmax'] = (df[col] - min_val) / (max_val - min_val)
    print(f"  Min-Max scaled '{col}': [{df['score_minmax'].min():.2f}, "
          f"{df['score_minmax'].max():.2f}]")

    # Z-Score Standardization: mean=0, std=1
    # formula: (x - mean) / std
    df['score_zscore'] = (df[col] - df[col].mean()) / df[col].std()
    print(f"  Z-Score '{col}': mean={df['score_zscore'].mean():.4f}, "
          f"std={df['score_zscore'].std():.4f}")

    return df


# =============================================================================
# Step 5: Bin Continuous Variables
# =============================================================================

def bin_data(df: pd.DataFrame) -> pd.DataFrame:
    """Create categorical bins from continuous variables."""
    df = df.copy()

    print("\n--- Binning ---")

    # Age bins
    bins = [0, 25, 35, 45, 100]
    labels = ['Junior', 'Mid-Level', 'Senior', 'Executive']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
    print(f"  Age groups:\n{df['age_group'].value_counts().to_string()}")

    # Salary quantile bins
    df['salary_quartile'] = pd.qcut(df['salary_mid'], q=4,
                                     labels=['Q1', 'Q2', 'Q3', 'Q4'])
    print(f"\n  Salary quartiles:\n{df['salary_quartile'].value_counts().to_string()}")

    return df


# =============================================================================
# Step 6: Final Report
# =============================================================================

def final_report(original: pd.DataFrame, cleaned: pd.DataFrame) -> None:
    """Show before/after comparison."""
    print("\n=== Final Report ===")
    print(f"Original: {original.shape[0]} rows, {original.shape[1]} columns")
    print(f"Cleaned:  {cleaned.shape[0]} rows, {cleaned.shape[1]} columns")
    print(f"\nMissing values remaining: {cleaned.isnull().sum().sum()}")
    print(f"\nCleaned columns: {cleaned.columns.tolist()}")
    print(f"\nSample (first 3 rows):")
    print(cleaned.head(3).to_string())


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    # Create and inspect
    raw_df = create_sample_data()
    print("=== Raw Data ===")
    print(raw_df.to_string())
    print()
    inspect_data(raw_df)

    # Clean
    cleaned_df = clean_data(raw_df)

    # Normalize
    cleaned_df = normalize_data(cleaned_df)

    # Bin
    cleaned_df = bin_data(cleaned_df)

    # Report
    final_report(raw_df, cleaned_df)
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with `NaN` values. Use `.fillna(0)` to replace all missing values with 0. Then use `.fillna()` with a dictionary to fill different columns with different values.

??? success "Solution to Exercise 1"
    Fill with a constant and with per-column values.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({
            'temp': [21, np.nan, 25, np.nan],
            'humidity': [65, 68, np.nan, 75]
        })
        print("Fill with 0:\n", df.fillna(0))
        print("\nFill per column:\n", df.fillna({'temp': 20, 'humidity': 70}))

---

**Exercise 2.**
Create a DataFrame with a numeric column containing `NaN`. Use `.fillna()` with the column's mean to impute missing values. Compare the mean before and after imputation.

??? success "Solution to Exercise 2"
    Impute missing values with the column mean.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({'score': [85, np.nan, 90, np.nan, 78]})
        mean_val = df['score'].mean()
        print(f"Mean before: {mean_val:.2f}")
        df['score'] = df['score'].fillna(mean_val)
        print(f"Mean after: {df['score'].mean():.2f}")
        print(df)

---

**Exercise 3.**
Create a DataFrame and use `.fillna(method='ffill')` (forward fill) to propagate the last valid value forward. Then use `.fillna(method='bfill')` (backward fill) and compare the two results.

??? success "Solution to Exercise 3"
    Compare forward fill and backward fill.

        import pandas as pd
        import numpy as np

        df = pd.DataFrame({'val': [1, np.nan, np.nan, 4, np.nan]})
        print("Forward fill:\n", df.fillna(method='ffill'))
        print("\nBackward fill:\n", df.fillna(method='bfill'))
