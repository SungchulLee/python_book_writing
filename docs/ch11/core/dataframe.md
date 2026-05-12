# DataFrame

A **DataFrame** is a two-dimensional labeled data structure with columns of potentially different types. It is the primary pandas data structure for tabular data, analogous to a spreadsheet or SQL table.

!!! tip "Mental Model"
    A DataFrame is a dictionary of Series that share the same index. Each column can have its own dtype (int, float, string), but all columns are aligned by a common set of row labels. Think of it as a spreadsheet where the row numbers are replaced by meaningful labels and each column is a typed array.

## Conceptual Overview

A DataFrame can be thought of as:

- A dictionary of Series objects sharing the same index
- A 2D NumPy array with row and column labels
- An Excel spreadsheet with named columns

```python
import pandas as pd

df = pd.DataFrame({
    "price": [100, 101, 102],
    "volume": [10, 12, 9],
})
print(df)
```

```
   price  volume
0    100      10
1    101      12
2    102       9
```

## Creating a DataFrame

### From a Dictionary of Lists

The most common creation method. Keys become column names, values become column data.

```python
df = pd.DataFrame({
    "city": ["mumbai", "delhi"],
    "temperature": [32, 45],
    "humidity": [70, 60],
})
print(df)
```

```
     city  temperature  humidity
0  mumbai           32        70
1   delhi           45        60
```

### From a List of Dictionaries

Each dictionary represents a row. Keys become column names.

```python
df = pd.DataFrame([
    {'name': 'Alice', 'age': 25, 'city': 'NYC'},
    {'name': 'Bob', 'age': 30, 'city': 'LA'},
    {'name': 'Charlie', 'age': 35}  # Missing 'city' becomes NaN
])
print(df)
```

```
      name  age city
0    Alice   25  NYC
1      Bob   30   LA
2  Charlie   35  NaN
```

### With Custom Index

```python
df = pd.DataFrame(
    {"price": [100, 101, 102]},
    index=["day1", "day2", "day3"]
)
print(df)
```

```
      price
day1    100
day2    101
day3    102
```

### From NumPy Array

```python
import numpy as np

data = np.array([[1, 2], [3, 4], [5, 6]])
df = pd.DataFrame(data, columns=['A', 'B'], index=['x', 'y', 'z'])
print(df)
```

```
   A  B
x  1  2
y  3  4
z  5  6
```

## DataFrame Attributes

### shape

Returns the dimensionality as (rows, columns).

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)
print(df.shape)  # (891, 12)
```

### columns

The column labels as an Index object.

```python
print(df.columns)
# Index(['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', ...])
```

### index

The row labels.

```python
print(df.index)
# RangeIndex(start=0, stop=891, step=1)
```

### dtypes

Data types of each column.

```python
print(df.dtypes)
```

```
PassengerId      int64
Survived         int64
Pclass           int64
Name            object
Sex             object
Age            float64
...
```

### values

The underlying data as a NumPy array.

```python
print(type(df.values))  # <class 'numpy.ndarray'>
print(df.values.shape)  # (891, 12)
```

## Column Access

### Bracket Notation (Recommended)

```python
# Single column -> returns Series
price_series = df["price"]
print(type(price_series))  # <class 'pandas.core.series.Series'>

# Multiple columns -> returns DataFrame
subset = df[["price", "volume"]]
print(type(subset))  # <class 'pandas.core.frame.DataFrame'>
```

### Attribute Access (Use Cautiously)

```python
# Works for simple column names
df.price

# Fails if column name:
# - Contains spaces
# - Starts with a number
# - Conflicts with DataFrame methods (e.g., 'count', 'mean')
```

### Adding New Columns

```python
# Direct assignment
df["return"] = df["price"].pct_change()

# Using assign() for method chaining
df = df.assign(
    return_pct=lambda x: x["price"].pct_change(),
    volume_ma=lambda x: x["volume"].rolling(3).mean()
)
```

## Row Access

### Using loc (Label-based)

```python
df = pd.DataFrame(
    {"price": [100, 101, 102]},
    index=["day1", "day2", "day3"]
)

df.loc["day1"]           # Single row as Series
df.loc[["day1", "day3"]] # Multiple rows as DataFrame
df.loc["day1", "price"]  # Specific cell
```

### Using iloc (Position-based)

```python
df.iloc[0]        # First row as Series
df.iloc[0:2]      # First two rows as DataFrame
df.iloc[0, 0]     # First cell
df.iloc[-1]       # Last row
```

### Slicing Rows

```python
df[0:2]           # First two rows (position-based slicing)
df["day1":"day2"] # Label-based slicing (inclusive)
```

## DataFrame Operations

### Arithmetic Operations

Operations align by index and column labels.

```python
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [10, 20], 'B': [30, 40]})

print(df1 + df2)
```

```
    A   B
0  11  33
1  22  44
```

### Broadcasting with Series

```python
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
s = pd.Series([10, 100], index=['A', 'B'])

print(df * s)  # Multiplies each column by corresponding Series value
```

```
    A    B
0  10  400
1  20  500
2  30  600
```

## Financial Context

DataFrames are the standard structure for financial data analysis.

### Price Histories

```python
import pandas as pd

prices = pd.DataFrame({
    "AAPL": [150, 151, 152, 153, 154],
    "MSFT": [300, 301, 302, 303, 304],
    "GOOGL": [140, 141, 142, 143, 144]
}, index=pd.date_range("2024-01-01", periods=5))

print(prices)
```

```
            AAPL  MSFT  GOOGL
2024-01-01   150   300    140
2024-01-02   151   301    141
2024-01-03   152   302    142
2024-01-04   153   303    143
2024-01-05   154   304    144
```

### Returns Calculation

```python
# Daily returns
returns = prices.pct_change()

# Cumulative returns
cumulative_returns = (1 + returns).cumprod() - 1
```

### Risk Metrics

```python
import numpy as np

# Annualized volatility
volatility = returns.std() * np.sqrt(252)

# Correlation matrix
correlation = returns.corr()

# Covariance matrix
covariance = returns.cov() * 252  # Annualized
```

### Portfolio Analysis

```python
# Portfolio weights
weights = pd.Series({'AAPL': 0.4, 'MSFT': 0.35, 'GOOGL': 0.25})

# Portfolio return
portfolio_return = (returns * weights).sum(axis=1)

# Portfolio volatility
portfolio_vol = np.sqrt(weights @ covariance @ weights)
```

## DataFrame vs Series

| Aspect | Series | DataFrame |
|--------|--------|-----------|
| Dimensions | 1D | 2D |
| Access single item | `s['label']` | `df.loc[row, col]` |
| Selecting subset | Returns Series | Returns Series or DataFrame |
| Typical use | Single variable | Multiple variables |
| Column relationship | N/A | Each column is a Series |

---

## Runnable Example: `dataframe_tutorial.py`

```python
"""
Pandas Tutorial 02: Introduction to DataFrames
===============================================

This tutorial introduces DataFrames, the most important data structure in pandas.
We'll cover:
1. What is a DataFrame
2. Creating DataFrames from various sources
3. DataFrame attributes and methods
4. Selecting columns and rows
5. Adding and removing columns/rows
6. Basic DataFrame operations

Prerequisites: Tutorial 01 - Series
Difficulty: Beginner
"""

import pandas as pd
import numpy as np

# ============================================================================
# SECTION 1: WHAT IS A DATAFRAME?
# ============================================================================

if __name__ == "__main__":

    """
    What is a DataFrame?
    --------------------
    A DataFrame is a 2-dimensional labeled data structure with columns that can be 
    of different types. You can think of it as:
    - A spreadsheet or SQL table
    - A dictionary of Series objects (each column is a Series)
    - A 2D NumPy array with row and column labels

    Key characteristics:
    - Rows and columns have labels (index and columns)
    - Columns can have different data types
    - Size-mutable: can add/delete columns and rows
    - Automatic data alignment
    - Powerful data manipulation capabilities
    """

    # ============================================================================
    # SECTION 2: CREATING DATAFRAMES
    # ============================================================================

    print("=" * 70)
    print("CREATING DATAFRAMES")
    print("=" * 70)

    # Method 1: From a dictionary of lists
    # Keys become column names, lists become column data
    print("\n1. DataFrame from dictionary of lists:")
    data_dict = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'Age': [25, 30, 35, 28, 32],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
        'Salary': [50000, 60000, 75000, 55000, 65000]
    }
    df1 = pd.DataFrame(data_dict)
    print(df1)
    print(f"\nType: {type(df1)}")

    # Method 2: From a list of dictionaries
    # Each dictionary is a row
    print("\n2. DataFrame from list of dictionaries:")
    data_list = [
        {'Name': 'Alice', 'Age': 25, 'Score': 85},
        {'Name': 'Bob', 'Age': 30, 'Score': 92},
        {'Name': 'Charlie', 'Age': 35, 'Score': 78},
    ]
    df2 = pd.DataFrame(data_list)
    print(df2)

    # Method 3: From a 2D NumPy array
    # Need to specify column names and index
    print("\n3. DataFrame from NumPy array:")
    numpy_data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    df3 = pd.DataFrame(numpy_data,
                       columns=['Column A', 'Column B', 'Column C'],
                       index=['Row 1', 'Row 2', 'Row 3'])
    print(df3)

    # Method 4: From a dictionary of Series
    # Useful when you already have Series objects
    print("\n4. DataFrame from dictionary of Series:")
    series_x = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
    series_y = pd.Series([100, 200, 300], index=['a', 'b', 'c'])
    series_z = pd.Series([1000, 2000, 3000], index=['a', 'b', 'c'])
    df4 = pd.DataFrame({'X': series_x, 'Y': series_y, 'Z': series_z})
    print(df4)

    # Method 5: From a list of lists with column names
    print("\n5. DataFrame from list of lists:")
    data_lists = [
        ['Product A', 100, 10.5],
        ['Product B', 150, 12.0],
        ['Product C', 200, 9.5]
    ]
    df5 = pd.DataFrame(data_lists, columns=['Product', 'Quantity', 'Price'])
    print(df5)

    # Method 6: Empty DataFrame (then fill it later)
    print("\n6. Empty DataFrame:")
    df6 = pd.DataFrame()
    print(f"Empty DataFrame:\n{df6}")
    print(f"Shape: {df6.shape}")

    # ============================================================================
    # SECTION 3: DATAFRAME ATTRIBUTES
    # ============================================================================

    print("\n" + "=" * 70)
    print("DATAFRAME ATTRIBUTES")
    print("=" * 70)

    # Let's work with df1 (employee data)
    print("\nWorking with this DataFrame:")
    print(df1)

    # Shape: (rows, columns)
    print(f"\nShape (rows, columns): {df1.shape}")

    # Dimensions
    print(f"Number of dimensions: {df1.ndim}")

    # Size: total number of elements (rows × columns)
    print(f"Size (total elements): {df1.size}")

    # Column names
    print(f"\nColumn names: {df1.columns.tolist()}")

    # Index (row labels)
    print(f"Index (row labels): {df1.index.tolist()}")

    # Data types of each column
    print("\nData types of columns:")
    print(df1.dtypes)

    # Values as a NumPy array
    print("\nValues (as 2D NumPy array):")
    print(df1.values)

    # Information about the DataFrame
    print("\nDataFrame info:")
    df1.info()

    # Memory usage
    print(f"\nMemory usage:\n{df1.memory_usage()}")

    # ============================================================================
    # SECTION 4: VIEWING DATA
    # ============================================================================

    print("\n" + "=" * 70)
    print("VIEWING DATA")
    print("=" * 70)

    # Create a larger DataFrame for demonstration
    np.random.seed(42)  # For reproducibility
    large_df = pd.DataFrame({
        'A': np.random.randint(1, 100, 20),
        'B': np.random.randint(1, 100, 20),
        'C': np.random.randint(1, 100, 20),
        'D': np.random.randint(1, 100, 20)
    })

    print("Full DataFrame (20 rows):")
    print(large_df)

    # View first n rows (default: 5)
    print("\nFirst 5 rows (head):")
    print(large_df.head())

    print("\nFirst 3 rows:")
    print(large_df.head(3))

    # View last n rows (default: 5)
    print("\nLast 5 rows (tail):")
    print(large_df.tail())

    print("\nLast 2 rows:")
    print(large_df.tail(2))

    # Random sample of rows
    print("\nRandom sample of 3 rows:")
    print(large_df.sample(3))

    # ============================================================================
    # SECTION 5: SELECTING COLUMNS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SELECTING COLUMNS")
    print("=" * 70)

    print("Original DataFrame:")
    print(df1)

    # Method 1: Select a single column (returns a Series)
    print("\n1. Select 'Name' column (returns Series):")
    name_column = df1['Name']
    print(name_column)
    print(f"Type: {type(name_column)}")

    # Alternative: using dot notation (only if column name is valid Python identifier)
    print("\n2. Select 'Age' using dot notation:")
    age_column = df1.Age
    print(age_column)

    # Method 2: Select multiple columns (returns a DataFrame)
    print("\n3. Select multiple columns ['Name', 'Salary']:")
    subset = df1[['Name', 'Salary']]
    print(subset)
    print(f"Type: {type(subset)}")

    # Change column order while selecting
    print("\n4. Select columns in different order:")
    reordered = df1[['Salary', 'Name', 'City']]
    print(reordered)

    # ============================================================================
    # SECTION 6: SELECTING ROWS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SELECTING ROWS")
    print("=" * 70)

    print("Original DataFrame:")
    print(df1)

    # Method 1: Select by integer position using iloc
    # iloc[row, column] - both are integer positions
    # Remember: Python uses 0-based indexing

    print("\n1. Select first row using iloc[0]:")
    first_row = df1.iloc[0]
    print(first_row)
    print(f"Type: {type(first_row)}")  # Returns a Series

    print("\n2. Select first 3 rows using iloc[0:3]:")
    first_three = df1.iloc[0:3]
    print(first_three)

    print("\n3. Select specific rows using iloc[[0, 2, 4]]:")
    specific_rows = df1.iloc[[0, 2, 4]]
    print(specific_rows)

    # Method 2: Select by label using loc
    # loc[row_label, column_label]
    # First, let's set custom index
    df1_custom = df1.copy()
    df1_custom.index = ['emp1', 'emp2', 'emp3', 'emp4', 'emp5']
    print("\n4. DataFrame with custom index:")
    print(df1_custom)

    print("\n5. Select row by label using loc['emp2']:")
    row_emp2 = df1_custom.loc['emp2']
    print(row_emp2)

    print("\n6. Select multiple rows using loc[['emp1', 'emp3', 'emp5']]:")
    selected_emps = df1_custom.loc[['emp1', 'emp3', 'emp5']]
    print(selected_emps)

    # Method 3: Boolean indexing (very powerful!)
    print("\n7. Boolean indexing - employees with Age > 28:")
    condition = df1['Age'] > 28
    print(f"Condition: {condition.tolist()}")
    filtered = df1[condition]
    print(filtered)

    # Multiple conditions using & (and) or | (or)
    # Important: Each condition must be in parentheses!
    print("\n8. Multiple conditions - Age > 28 AND Salary > 60000:")
    filtered2 = df1[(df1['Age'] > 28) & (df1['Salary'] > 60000)]
    print(filtered2)

    print("\n9. Multiple conditions - Age < 30 OR Salary > 65000:")
    filtered3 = df1[(df1['Age'] < 30) | (df1['Salary'] > 65000)]
    print(filtered3)

    # String conditions
    print("\n10. Filter by string - City contains 'New':")
    filtered4 = df1[df1['City'].str.contains('New')]
    print(filtered4)

    # ============================================================================
    # SECTION 7: SELECTING BOTH ROWS AND COLUMNS
    # ============================================================================

    print("\n" + "=" * 70)
    print("SELECTING ROWS AND COLUMNS TOGETHER")
    print("=" * 70)

    print("Original DataFrame:")
    print(df1)

    # Using iloc[rows, columns] - integer positions
    print("\n1. iloc[0:3, 0:2] - first 3 rows, first 2 columns:")
    subset1 = df1.iloc[0:3, 0:2]
    print(subset1)

    print("\n2. iloc[[0, 2], [0, 3]] - specific rows and columns:")
    subset2 = df1.iloc[[0, 2], [0, 3]]
    print(subset2)

    # Using loc[rows, columns] - labels
    print("\n3. loc[0:2, ['Name', 'Salary']] - rows 0-2, specific columns:")
    subset3 = df1.loc[0:2, ['Name', 'Salary']]
    print(subset3)

    # Select all rows, specific columns
    print("\n4. All rows, columns 'Name' and 'Age':")
    subset4 = df1.loc[:, ['Name', 'Age']]
    print(subset4)

    # Combine boolean indexing with column selection
    print("\n5. Age > 28, show Name and Salary only:")
    subset5 = df1.loc[df1['Age'] > 28, ['Name', 'Salary']]
    print(subset5)

    # ============================================================================
    # SECTION 8: ADDING AND MODIFYING COLUMNS
    # ============================================================================

    print("\n" + "=" * 70)
    print("ADDING AND MODIFYING COLUMNS")
    print("=" * 70)

    # Create a working copy
    df_work = df1.copy()
    print("Original DataFrame:")
    print(df_work)

    # Add a new column with a constant value
    df_work['Country'] = 'USA'
    print("\n1. Added 'Country' column with constant value:")
    print(df_work)

    # Add a new column based on calculation
    df_work['Annual Bonus'] = df_work['Salary'] * 0.1
    print("\n2. Added 'Annual Bonus' (10% of Salary):")
    print(df_work)

    # Add a column based on conditions
    df_work['Category'] = df_work['Age'].apply(
        lambda x: 'Young' if x < 30 else 'Experienced'
    )
    print("\n3. Added 'Category' based on Age:")
    print(df_work)

    # Modify existing column
    df_work['Salary'] = df_work['Salary'] * 1.05  # 5% raise
    print("\n4. Modified 'Salary' (5% increase):")
    print(df_work)

    # Add column using assign() method (doesn't modify original)
    df_assigned = df_work.assign(Tax=lambda x: x['Salary'] * 0.2)
    print("\n5. Added 'Tax' column using assign():")
    print(df_assigned)

    # ============================================================================
    # SECTION 9: ADDING AND REMOVING ROWS
    # ============================================================================

    print("\n" + "=" * 70)
    print("ADDING AND REMOVING ROWS")
    print("=" * 70)

    # Create a working copy
    df_rows = df1.copy()
    print("Original DataFrame:")
    print(df_rows)

    # Add a new row using loc (with specific index)
    df_rows.loc[len(df_rows)] = ['Frank', 40, 'Seattle', 70000]
    print("\n1. Added new row:")
    print(df_rows)

    # Add row using dictionary
    new_row_dict = {'Name': 'Grace', 'Age': 27, 'City': 'Boston', 'Salary': 58000}
    df_rows = pd.concat([df_rows, pd.DataFrame([new_row_dict])], ignore_index=True)
    print("\n2. Added row from dictionary:")
    print(df_rows)

    # Remove row by index position
    df_dropped = df_rows.drop(0)  # Drops row with index 0
    print("\n3. Removed first row (index 0):")
    print(df_dropped)

    # Remove multiple rows
    df_dropped_multiple = df_rows.drop([0, 2, 4])
    print("\n4. Removed rows at indices 0, 2, 4:")
    print(df_dropped_multiple)

    # Remove rows based on condition
    df_filtered = df_rows[df_rows['Age'] < 35]
    print("\n5. Kept only rows where Age < 35:")
    print(df_filtered)

    # ============================================================================
    # SECTION 10: BASIC DATAFRAME OPERATIONS
    # ============================================================================

    print("\n" + "=" * 70)
    print("BASIC DATAFRAME OPERATIONS")
    print("=" * 70)

    print("Original DataFrame:")
    print(df1)

    # Statistical summary
    print("\n1. Statistical summary (describe):")
    print(df1.describe())

    # Summary including non-numeric columns
    print("\n2. Summary including all columns:")
    print(df1.describe(include='all'))

    # Mean of numeric columns
    print("\n3. Mean of numeric columns:")
    print(df1.mean(numeric_only=True))

    # Sum of numeric columns
    print("\n4. Sum of numeric columns:")
    print(df1.sum(numeric_only=True))

    # Count non-null values in each column
    print("\n5. Count of non-null values:")
    print(df1.count())

    # Unique values in a column
    print("\n6. Unique cities:")
    print(df1['City'].unique())
    print(f"Number of unique cities: {df1['City'].nunique()}")

    # Value counts
    print("\n7. Value counts for 'City':")
    print(df1['City'].value_counts())

    # ============================================================================
    # SECTION 11: SORTING
    # ============================================================================

    print("\n" + "=" * 70)
    print("SORTING")
    print("=" * 70)

    print("Original DataFrame:")
    print(df1)

    # Sort by a single column
    print("\n1. Sort by Age (ascending):")
    sorted_age = df1.sort_values('Age')
    print(sorted_age)

    print("\n2. Sort by Age (descending):")
    sorted_age_desc = df1.sort_values('Age', ascending=False)
    print(sorted_age_desc)

    # Sort by multiple columns
    print("\n3. Sort by Salary (desc), then by Name (asc):")
    sorted_multi = df1.sort_values(['Salary', 'Name'], ascending=[False, True])
    print(sorted_multi)

    # Sort by index
    print("\n4. Sort by index:")
    df_index_sorted = df1.sort_index()
    print(df_index_sorted)

    # ============================================================================
    # SECTION 12: RENAMING COLUMNS AND INDEX
    # ============================================================================

    print("\n" + "=" * 70)
    print("RENAMING")
    print("=" * 70)

    print("Original DataFrame:")
    print(df1)

    # Rename columns using a dictionary
    df_renamed = df1.rename(columns={'Name': 'Employee Name', 'Salary': 'Annual Salary'})
    print("\n1. Renamed columns:")
    print(df_renamed)

    # Rename all columns at once
    df_renamed_all = df1.copy()
    df_renamed_all.columns = ['emp_name', 'emp_age', 'emp_city', 'emp_salary']
    print("\n2. Renamed all columns:")
    print(df_renamed_all)

    # Rename index
    df_renamed_index = df1.rename(index={0: 'first', 1: 'second', 2: 'third'})
    print("\n3. Renamed index:")
    print(df_renamed_index)

    # ============================================================================
    # SECTION 13: HANDLING MISSING DATA
    # ============================================================================

    print("\n" + "=" * 70)
    print("HANDLING MISSING DATA")
    print("=" * 70)

    # Create DataFrame with missing values
    data_missing = {
        'A': [1, 2, np.nan, 4, 5],
        'B': [np.nan, 2, 3, np.nan, 5],
        'C': [1, 2, 3, 4, 5],
        'D': [np.nan, np.nan, np.nan, np.nan, np.nan]
    }
    df_missing = pd.DataFrame(data_missing)
    print("DataFrame with missing values:")
    print(df_missing)

    # Check for missing values
    print("\n1. Is null? (True for NaN values):")
    print(df_missing.isnull())

    # Count missing values per column
    print("\n2. Count of missing values per column:")
    print(df_missing.isnull().sum())

    # Total missing values
    print(f"\n3. Total missing values: {df_missing.isnull().sum().sum()}")

    # Drop rows with any missing values
    print("\n4. Drop rows with ANY missing values:")
    df_dropped_rows = df_missing.dropna()
    print(df_dropped_rows)

    # Drop columns with any missing values
    print("\n5. Drop columns with ANY missing values:")
    df_dropped_cols = df_missing.dropna(axis=1)
    print(df_dropped_cols)

    # Drop rows where ALL values are missing
    print("\n6. Drop rows where ALL values are missing:")
    df_dropped_all = df_missing.dropna(how='all')
    print(df_dropped_all)

    # Drop columns where ALL values are missing
    print("\n7. Drop columns where ALL values are missing:")
    df_dropped_all_cols = df_missing.dropna(axis=1, how='all')
    print(df_dropped_all_cols)

    # Fill missing values with 0
    print("\n8. Fill missing values with 0:")
    df_filled_zero = df_missing.fillna(0)
    print(df_filled_zero)

    # Fill missing values with mean of each column
    print("\n9. Fill missing values with column mean:")
    df_filled_mean = df_missing.fillna(df_missing.mean())
    print(df_filled_mean)

    # Fill missing values with different values for each column
    print("\n10. Fill with different values per column:")
    df_filled_dict = df_missing.fillna({'A': 0, 'B': 999, 'D': -1})
    print(df_filled_dict)

    # Forward fill
    print("\n11. Forward fill (use previous row's value):")
    df_ffill = df_missing.fillna(method='ffill')
    print(df_ffill)

    # Backward fill
    print("\n12. Backward fill (use next row's value):")
    df_bfill = df_missing.fillna(method='bfill')
    print(df_bfill)

    # ============================================================================
    # SECTION 14: SUMMARY AND KEY TAKEAWAYS
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    summary = """
    1. DataFrame is a 2D labeled data structure (like a table)
    2. Create DataFrames from dicts, lists, arrays, or Series
    3. Use head(), tail(), and sample() to view data
    4. Select columns with [] or dot notation
    5. Select rows with iloc (position) or loc (label)
    6. Boolean indexing is powerful for filtering
    7. Add columns by assignment or assign() method
    8. Add rows with loc or concat()
    9. Remove rows/columns with drop()
    10. Sort with sort_values() or sort_index()
    11. Rename with rename() or direct assignment to .columns
    12. Handle missing data with dropna() or fillna()

    Next Steps:
    -----------
    - Practice DataFrame operations
    - Try the exercise file: exercises/02_dataframe_exercises.py
    - Move on to Tutorial 03: Reading and Writing Data
    """

    print(summary)
```

---

## Exercises

**Exercise 1.**
Create a DataFrame from a dictionary with 3 columns and 5 rows. Select a single column (returns a Series) and then select two columns (returns a DataFrame). Print the type of each result.

??? success "Solution to Exercise 1"
    Select single and multiple columns and check types.

        import pandas as pd

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Carol', 'Dave', 'Eve'],
            'age': [25, 30, 35, 40, 45],
            'score': [85, 90, 78, 92, 88]
        })
        single = df['name']
        multi = df[['name', 'age']]
        print(type(single))   # Series
        print(type(multi))    # DataFrame

---

**Exercise 2.**
Create a DataFrame and add a new column computed from existing columns (e.g., `'total' = 'price' * 'quantity'`). Then delete a column using `del df['column']` or `df.drop(columns=...)`.

??? success "Solution to Exercise 2"
    Add and remove columns.

        import pandas as pd

        df = pd.DataFrame({'price': [10, 20, 30], 'quantity': [2, 3, 1]})
        df['total'] = df['price'] * df['quantity']
        print(df)
        df = df.drop(columns=['quantity'])
        print(df)

---

**Exercise 3.**
Create a DataFrame with a custom index (not the default RangeIndex). Use `.loc[]` to select a row by label and `.iloc[]` to select a row by position. Verify both return the same row.

??? success "Solution to Exercise 3"
    Compare loc and iloc access.

        import pandas as pd

        df = pd.DataFrame(
            {'val': [100, 200, 300]},
            index=['first', 'second', 'third']
        )
        by_label = df.loc['second']
        by_position = df.iloc[1]
        print(by_label)
        assert (by_label == by_position).all()
