# Series

A **Series** is a one-dimensional labeled array capable of holding any data type. It is the fundamental building block of pandas, representing a single column of data with an associated index.

!!! tip "Mental Model"
    A Series is a NumPy array with a label taped to each element. The labels (index) let you look up values by name instead of position, and they automatically align when you combine two Series. Every DataFrame column is secretly a Series.

## Conceptual Overview

```
2D NumPy Array    Matrix-like data structure with a single dtype
DataFrame         Excel-like data structure where each column may have different dtype
Series            One column of Excel-like data structure with a single dtype
```

A Series combines the power of NumPy arrays with labeled indexing, making it ideal for time-series data and tabular column operations.

## Creating a Series

### From a List

```python
import pandas as pd

# Basic creation with default integer index
s = pd.Series([3, 9, 1])
print(s)
```

```
0    3
1    9
2    1
dtype: int64
```

### With Custom Index and Name

```python
data = [3, 9, 1]
name = "data"
index = pd.date_range(start='2019-09-01', end='2019-09-03')

s = pd.Series(data, name=name, index=index)
print(s)
```

```
2019-09-01    3
2019-09-02    9
2019-09-03    1
Freq: D, Name: data, dtype: int64
```

### From a Dictionary

When creating from a dictionary, keys become the index labels.

```python
data_dict = {
    '2019-09-01': 3,
    '2019-09-02': 9,
    '2019-09-03': 1
}
s = pd.Series(data_dict, name="data")
print(s)
```

```
2019-09-01    3
2019-09-02    9
2019-09-03    1
Name: data, dtype: int64
```

### From a DataFrame Column

Extracting a column from a DataFrame returns a Series.

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Bracket notation (preferred)
survived_series = df["Survived"]

# Dot notation (use cautiously)
survived_series = df.Survived

print(type(survived_series))  # <class 'pandas.core.series.Series'>
```

## Series Attributes

### dtype

The data type of the Series elements. Pandas performs automatic type inference and upcasting.

```python
# String data -> object dtype
s = pd.Series(['Boat', 'Car', 'Bike'])
print(f"{s.dtype = }")  # s.dtype = dtype('O')

# Integer data -> int64 dtype
s = pd.Series([1, 55, 99])
print(f"{s.dtype = }")  # s.dtype = dtype('int64')

# Float data -> float64 dtype
s = pd.Series([1., 55., 99.])
print(f"{s.dtype = }")  # s.dtype = dtype('float64')

# Mixed int/float -> upcasted to float64
s = pd.Series([1., 55, 99])
print(f"{s.dtype = }")  # s.dtype = dtype('float64')
```

### index

The labels associated with each element.

```python
s = pd.Series([3, 9, 1], index=pd.date_range(start='2019-09-01', end='2019-09-03'))
print(f"{s.index = }")
# s.index = DatetimeIndex(['2019-09-01', '2019-09-02', '2019-09-03'], dtype='datetime64[ns]', freq='D')
```

### name

An optional name for the Series, useful when converting to DataFrame.

```python
s = pd.Series([3, 9, 1], name="data")
print(f"{s.name = }")  # s.name = 'data'
```

### shape

The dimensionality of the Series as a tuple.

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

print(df.shape)              # (891, 12) - DataFrame
print(df[["Survived"]].shape)  # (891, 1) - DataFrame with one column
print(df["Survived"].shape)    # (891,) - Series
```

### values

The underlying NumPy array.

```python
import yfinance as yf

df = yf.Ticker('WMT').history(start='2020-01-01', end='2020-12-31')
print(f"{type(df.Close.values) = }")  # <class 'numpy.ndarray'>
print(f"{df.Close.values.shape = }")  # (252,)
print(f"{df.Close.values.dtype = }")  # dtype('float64')
```

## Accessing Series Elements

### Label-based Access

```python
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])

s["a"]           # Single label -> 10
s[["a", "c"]]    # Multiple labels -> Series
s.loc["a"]       # Explicit label-based access
```

### Position-based Access

```python
s.iloc[0]        # First element -> 10
s.iloc[0:2]      # First two elements -> Series
s.iloc[-1]       # Last element -> 30
```

### Boolean Indexing

```python
s[s > 15]        # Elements greater than 15
```

## Common Series Methods

### Statistical Methods

```python
s = pd.Series([3, 9, 1, 5, 7])

s.mean()     # 5.0
s.median()   # 5.0
s.sum()      # 25
s.std()      # Standard deviation
s.min()      # 1
s.max()      # 9
```

### Conversion Methods

```python
s = pd.Series([1, 2, 3], index=['a', 'b', 'c'])

s.tolist()       # [1, 2, 3] - Convert to Python list
s.to_frame()     # Convert to DataFrame
s.to_numpy()     # Convert to NumPy array
```

### Value Inspection

```python
s = pd.Series([1, 2, 2, 3, 3, 3])

s.value_counts()  # Count occurrences of each value
s.nunique()       # Number of unique values -> 3
s.unique()        # Array of unique values -> [1, 2, 3]
```

## Financial Example

```python
import pandas as pd
import yfinance as yf

# Download stock data
ticker = 'AAPL'
df = yf.Ticker(ticker).history(start='2024-01-01', end='2024-06-30')

# Close prices as Series
close_prices = df['Close']

print(f"Mean price: ${close_prices.mean():.2f}")
print(f"Max price: ${close_prices.max():.2f}")
print(f"Min price: ${close_prices.min():.2f}")
print(f"Volatility: {close_prices.pct_change().std() * (252**0.5):.2%}")
```

## Series vs NumPy Array

| Feature | NumPy Array | pandas Series |
|---------|-------------|---------------|
| Indexing | Integer only | Label or integer |
| Alignment | Manual | Automatic by index |
| Missing data | No native support | Native NaN handling |
| Metadata | None | name, index attributes |
| Operations | Element-wise | Index-aligned |

---

## Runnable Example: `series_tutorial.py`

```python
"""
Pandas Tutorial 01: Introduction to Pandas and Series
======================================================

This tutorial introduces pandas, a powerful data manipulation library in Python.

🔗 CRITICAL CONNECTIONS TO PREVIOUS TOPICS:
- Topic #24: Memory Deep Dive (dtype selection, memory efficiency)
- Topics #26-36: Object-Oriented Programming (Series/DataFrame are classes!)
- Topic #27: Methods and Attributes (understanding .head(), .shape, etc.)
- Topic #37: NumPy (Pandas is built on NumPy arrays!)

We'll cover:
1. What is pandas and why use it
2. Installing and importing pandas
3. Creating pandas Series (objects!)
4. Basic Series operations
5. Indexing and slicing Series
6. Common Series methods

Prerequisites: Topics #24, #26-36, #37
Difficulty: Beginner
"""

import pandas as pd
import numpy as np

# ============================================================================
# SECTION 1: INTRODUCTION TO PANDAS
# ============================================================================

if __name__ == "__main__":

    """
    What is Pandas?
    ---------------
    Pandas is a fast, powerful, flexible and easy-to-use open-source data analysis 
    and manipulation library built on top of Python. It provides two primary data 
    structures:

    1. Series: 1-dimensional labeled array (A CLASS - OOP!)
    2. DataFrame: 2-dimensional labeled data structure (A CLASS - OOP!)

    🔗 CONNECTION TO TOPIC #37 (NumPy):
    Pandas is BUILT ON NumPy! Under the hood:
    - Series uses NumPy arrays for data storage
    - DataFrame is a collection of NumPy arrays (one per column)
    - Inherits NumPy's speed and memory efficiency

    🔗 CONNECTION TO TOPICS #26-36 (OOP):
    Series and DataFrame are CLASSES (not just data structures):
    - They have METHODS: .head(), .describe(), .mean()
    - They have ATTRIBUTES: .shape, .dtypes, .index
    - They use ENCAPSULATION: Internal optimizations hidden
    - They support METHOD CHAINING: df.sort().groupby().mean()

    Why use Pandas?
    ---------------
    - Handles missing data elegantly
    - Easy data alignment and indexing
    - Powerful groupby functionality (Topic #27: method chaining!)
    - Flexible reshaping and pivoting
    - Time series functionality
    - Integration with NumPy (Topic #37), Matplotlib, etc.
    - Object-oriented design makes code readable (Topics #26-36!)
    """

    # ============================================================================
    # SECTION 1.5: Pandas as Object-Oriented Programming (Topics #26-36)
    # ============================================================================

    print("=" * 70)
    print("UNDERSTANDING PANDAS AS OOP (Topics #26-36)")
    print("=" * 70)

    print("""
    🔗 CONNECTION TO OBJECT-ORIENTED PROGRAMMING:

    Pandas uses CLASSES and OBJECTS:
    --------------------------------
    1. Series is a CLASS (like classes you learned in Topic #26)
    2. When you create a Series, you create an OBJECT (instance)
    3. Objects have METHODS (functions) and ATTRIBUTES (data)

    Example from OOP:
      class Car:                    # Define a class
          def __init__(self, brand): 
              self.brand = brand    # Attribute
          def honk(self):           # Method
              print("Beep!")

      my_car = Car("Toyota")        # Create object
      print(my_car.brand)           # Access attribute
      my_car.honk()                 # Call method

    Similarly in Pandas:
      series = pd.Series([1, 2, 3])  # Create Series OBJECT
      print(series.shape)             # Access ATTRIBUTE (no parentheses!)
      series.mean()                   # Call METHOD (with parentheses!)

    Understanding this OOP structure helps you know:
    - When to use () for methods
    - When not to use () for attributes
    - How method chaining works (Topic #27!)
    """)

    # ============================================================================
    # SECTION 2: CREATING A SERIES (It's Creating an Object!)
    # ============================================================================

    print("\n" + "=" * 70)
    print("CREATING PANDAS SERIES (Creating Objects!)")
    print("=" * 70)

    # Method 1: Create a Series from a Python list
    # A Series is like a column in a spreadsheet with labels (index)
    data_list = [10, 20, 30, 40, 50]
    series1 = pd.Series(data_list)  # Creating a Series OBJECT
    print("\n1. Series from list:")
    print(series1)
    print(f"Type: {type(series1)}")  # <class 'pandas.core.series.Series'>
    print(f"Is it an object? Yes! (Topic #26)")

    # Method 2: Create a Series with custom index
    # By default, pandas uses 0, 1, 2, ... as index
    # We can provide our own labels
    series2 = pd.Series([10, 20, 30, 40, 50], 
                        index=['a', 'b', 'c', 'd', 'e'])
    print("\n2. Series with custom index:")
    print(series2)

    # Method 3: Create a Series from a dictionary
    # Dictionary keys become the index, values become the data
    data_dict = {'Monday': 100, 'Tuesday': 150, 'Wednesday': 120, 
                 'Thursday': 180, 'Friday': 200}
    series3 = pd.Series(data_dict)
    print("\n3. Series from dictionary:")
    print(series3)

    # Method 4: Create a Series from a NumPy array
    # Pandas works seamlessly with NumPy
    numpy_array = np.array([1.5, 2.7, 3.9, 4.1, 5.3])
    series4 = pd.Series(numpy_array, index=['first', 'second', 'third', 'fourth', 'fifth'])
    print("\n4. Series from NumPy array:")
    print(series4)

    # Method 5: Create a Series with a scalar value
    # The scalar value is repeated for all indices
    series5 = pd.Series(100, index=['a', 'b', 'c', 'd'])
    print("\n5. Series from scalar value:")
    print(series5)

    # ============================================================================
    # SECTION 3: SERIES ATTRIBUTES
    # ============================================================================

    print("\n" + "=" * 70)
    print("SERIES ATTRIBUTES")
    print("=" * 70)

    # Let's work with series3 (days of the week)
    print("\nWorking with series:", series3.name if series3.name else "Unnamed")
    print(series3)

    # Get the values as a NumPy array
    print("\nValues (as NumPy array):")
    print(series3.values)
    print(f"Type: {type(series3.values)}")

    # Get the index (labels)
    print("\nIndex:")
    print(series3.index)
    print(f"Type: {type(series3.index)}")

    # Get the data type of elements
    print(f"\nData type of elements: {series3.dtype}")

    # Get the shape (number of elements)
    print(f"Shape: {series3.shape}")

    # Get the size (number of elements)
    print(f"Size: {series3.size}")

    # Give the Series a name (useful for DataFrames later)
    series3.name = "Daily Sales"
    print(f"\nSeries name: {series3.name}")
    print(series3)

    # ============================================================================
    # SECTION 3.5: METHODS vs ATTRIBUTES & METHOD CHAINING (Topics #27, #26-36)
    # ============================================================================

    print("\n" + "=" * 70)
    print("METHODS vs ATTRIBUTES (Topic #27)")
    print("=" * 70)

    print("""
    🔗 CONNECTION TO TOPIC #27 (Methods and Attributes):

    ATTRIBUTES: Data about the object (NO parentheses!)
    - .shape      ← Shape of the Series
    - .size       ← Number of elements
    - .dtype      ← Data type
    - .index      ← Index labels
    - .values     ← Underlying NumPy array

    METHODS: Actions/operations on the object (WITH parentheses!)
    - .mean()     ← Calculate mean
    - .sum()      ← Calculate sum
    - .head()     ← Get first n elements
    - .describe() ← Statistical summary
    """)

    # Demonstrate attributes (no parentheses!)
    print(f"\nATTRIBUTES (no parentheses):")
    print(f"  series3.shape = {series3.shape}  ← Attribute")
    print(f"  series3.size = {series3.size}    ← Attribute")
    print(f"  series3.dtype = {series3.dtype}  ← Attribute")

    # Demonstrate methods (with parentheses!)
    print(f"\nMETHODS (with parentheses):")
    print(f"  series3.mean() = {series3.mean():.1f}  ← Method call")
    print(f"  series3.sum() = {series3.sum()}    ← Method call")
    print(f"  series3.max() = {series3.max()}    ← Method call")

    print("""
    Common Mistake for Beginners:
      series.shape() ← ERROR! shape is an attribute, not a method
      series.mean   ← This works but returns a function, not the result!
      series.mean() ← Correct! Calls the method
    """)

    # ============================================================================
    # SECTION 3.6: METHOD CHAINING (Topic #27 - Fluent Interfaces)
    # ============================================================================

    print("\n" + "=" * 70)
    print("METHOD CHAINING (Topic #27)")
    print("=" * 70)

    print("""
    🔗 CONNECTION TO TOPIC #27 (Fluent Interfaces):

    Many Pandas methods return NEW Series/DataFrame objects.
    This allows METHOD CHAINING - calling methods one after another!

    Example: obj.method1().method2().method3()
    """)

    # Create sample data
    values = pd.Series([100, 150, 120, 180, 200, 95, 175])
    print(f"Original series:\n{values}\n")

    # Method chaining example
    result = values.sort_values().head(3)
    print(f"Method chain: values.sort_values().head(3)")
    print(f"Result:\n{result}\n")

    # Longer chain
    result = (series3
        .sort_values(ascending=False)  # Sort descending
        .head(3)                        # Get top 3
        .mean())                        # Calculate mean

    print(f"Complex chain:")
    print(f"  series3.sort_values(ascending=False).head(3).mean()")
    print(f"  Result: {result:.1f}\n")

    print("""
    Method chaining makes code:
    1. More readable (reads like a sentence)
    2. Easier to debug (one operation per line)
    3. More Pythonic (elegant and concise)

    This is OBJECT-ORIENTED design (Topics #26-36)!
    Each method returns an object you can call more methods on.
    """)

    # ============================================================================
    # SECTION 3.7: MEMORY CONSIDERATIONS (Topic #24)
    # ============================================================================

    print("\n" + "=" * 70)
    print("MEMORY CONSIDERATIONS (Topic #24)")
    print("=" * 70)

    print("""
    🔗 CONNECTION TO TOPIC #24 (Memory Deep Dive):

    Pandas leverages NumPy's memory efficiency, but you can optimize further!
    """)

    # Create different dtype Series
    import sys

    series_int64 = pd.Series(range(10000))  # Default: int64
    series_int32 = pd.Series(range(10000), dtype='int32')
    series_int16 = pd.Series(range(10000), dtype='int16')
    series_int8 = pd.Series(range(10000), dtype='int8')

    print(f"\nMemory usage for 10,000 integers:")
    print(f"  int64 (default): {series_int64.memory_usage(deep=True):,} bytes")
    print(f"  int32:           {series_int32.memory_usage(deep=True):,} bytes")
    print(f"  int16:           {series_int16.memory_usage(deep=True):,} bytes")
    print(f"  int8:            {series_int8.memory_usage(deep=True):,} bytes")

    savings = 100 * (1 - series_int8.memory_usage(deep=True) / series_int64.memory_usage(deep=True))
    print(f"\n  Savings: {savings:.0f}% by choosing appropriate dtype!")

    print("""
    Best Practice (Topic #24):
    - Choose smallest dtype that fits your data
    - int8: -128 to 127
    - int16: -32,768 to 32,767
    - int32: ±2 billion
    - int64: Very large numbers (default)

    For large datasets, dtype choice matters! (Topic #24)
    """)

    # ============================================================================
    # SECTION 4: INDEXING AND SELECTION
    # ============================================================================

    print("\n" + "=" * 70)
    print("INDEXING AND SELECTION")
    print("=" * 70)

    # Create a sample Series for demonstration
    temperatures = pd.Series([22.5, 24.1, 23.7, 25.3, 26.8, 24.9, 23.2],
                            index=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                            name='Temperature (°C)')
    print("\nSample Series - Weekly Temperatures:")
    print(temperatures)

    # Method 1: Access by label using square brackets
    print(f"\nTemperature on Monday: {temperatures['Mon']}°C")

    # Method 2: Access by integer position
    print(f"First temperature: {temperatures[0]}°C")
    print(f"Last temperature: {temperatures[-1]}°C")

    # Method 3: Access using .loc (label-based)
    # .loc is INCLUSIVE on both ends
    print(f"\nUsing .loc['Mon']: {temperatures.loc['Mon']}°C")
    print("\nUsing .loc['Mon':'Wed'] (inclusive):")
    print(temperatures.loc['Mon':'Wed'])

    # Method 4: Access using .iloc (integer position-based)
    # .iloc is EXCLUSIVE on the right end (like Python slicing)
    print(f"\nUsing .iloc[0]: {temperatures.iloc[0]}°C")
    print("\nUsing .iloc[0:3] (exclusive right):")
    print(temperatures.iloc[0:3])

    # Select multiple elements by labels
    print("\nSelect multiple days:")
    print(temperatures[['Mon', 'Wed', 'Fri']])

    # Select using boolean indexing
    # This is very powerful for filtering data
    print("\nDays with temperature > 24°C:")
    hot_days = temperatures[temperatures > 24]
    print(hot_days)

    # ============================================================================
    # SECTION 5: BASIC OPERATIONS
    # ============================================================================

    print("\n" + "=" * 70)
    print("BASIC OPERATIONS")
    print("=" * 70)

    # Arithmetic operations work element-wise
    print("\nOriginal temperatures:")
    print(temperatures)

    # Convert Celsius to Fahrenheit: F = C * 9/5 + 32
    temps_fahrenheit = temperatures * 9/5 + 32
    temps_fahrenheit.name = 'Temperature (°F)'
    print("\nTemperatures in Fahrenheit:")
    print(temps_fahrenheit)

    # Add a constant to all elements
    adjusted_temps = temperatures + 2
    print("\nAdjusted temperatures (+2°C):")
    print(adjusted_temps)

    # Operations between two Series
    # Pandas automatically aligns by index!
    series_a = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
    series_b = pd.Series([10, 20, 30], index=['a', 'b', 'c'])
    print("\nSeries A:")
    print(series_a)
    print("\nSeries B:")
    print(series_b)
    print("\nA + B (element-wise addition with index alignment):")
    print(series_a + series_b)

    # What happens with misaligned indices?
    series_c = pd.Series([100, 200, 300], index=['a', 'c', 'd'])
    print("\nSeries C (different indices):")
    print(series_c)
    print("\nA + C (NaN appears for non-matching indices):")
    print(series_a + series_c)

    # ============================================================================
    # SECTION 6: COMMON SERIES METHODS
    # ============================================================================

    print("\n" + "=" * 70)
    print("COMMON SERIES METHODS")
    print("=" * 70)

    # Create a sample Series with various values
    data = pd.Series([23, 45, 12, 67, 34, 89, 23, 56, 45, 12],
                     name='Sample Data')
    print("\nSample data:")
    print(data)

    # Statistical methods
    print("\n--- Statistical Summary ---")
    print(f"Mean (average): {data.mean():.2f}")
    print(f"Median (middle value): {data.median():.2f}")
    print(f"Standard deviation: {data.std():.2f}")
    print(f"Minimum value: {data.min()}")
    print(f"Maximum value: {data.max()}")
    print(f"Sum of all values: {data.sum()}")

    # Get a statistical summary at once
    print("\nComplete statistical summary:")
    print(data.describe())

    # Count occurrences
    print("\n--- Value Counts ---")
    print("Frequency of each value:")
    print(data.value_counts())

    # Sorting
    print("\n--- Sorting ---")
    print("Sort by values (ascending):")
    print(data.sort_values())

    print("\nSort by values (descending):")
    print(data.sort_values(ascending=False))

    print("\nSort by index:")
    sorted_by_index = data.sort_index()
    print(sorted_by_index)

    # Unique values
    print("\n--- Unique Values ---")
    print(f"Unique values: {data.unique()}")
    print(f"Number of unique values: {data.nunique()}")

    # Check for duplicates
    print("\n--- Duplicates ---")
    print("Is duplicated? (True if value appears more than once)")
    print(data.duplicated())

    # Drop duplicates (keep first occurrence)
    print("\nData after dropping duplicates:")
    print(data.drop_duplicates())

    # Apply a function to all elements
    print("\n--- Applying Functions ---")
    print("Square all values:")
    squared = data.apply(lambda x: x ** 2)
    print(squared)

    # Custom function application
    def categorize(value):
        """Categorize values as low, medium, or high"""
        if value < 30:
            return "Low"
        elif value < 60:
            return "Medium"
        else:
            return "High"

    print("\nCategorize values:")
    categories = data.apply(categorize)
    print(categories)

    # ============================================================================
    # SECTION 7: HANDLING MISSING DATA
    # ============================================================================

    print("\n" + "=" * 70)
    print("HANDLING MISSING DATA")
    print("=" * 70)

    # Create a Series with missing data (NaN = Not a Number)
    data_with_nan = pd.Series([1, 2, np.nan, 4, 5, np.nan, 7, 8],
                              index=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    print("\nSeries with missing values:")
    print(data_with_nan)

    # Check for missing values
    print("\nIs null? (True for missing values):")
    print(data_with_nan.isnull())

    print("\nIs not null? (True for non-missing values):")
    print(data_with_nan.notnull())

    # Count missing values
    print(f"\nNumber of missing values: {data_with_nan.isnull().sum()}")
    print(f"Number of non-missing values: {data_with_nan.notnull().sum()}")

    # Drop missing values
    print("\nDrop missing values:")
    cleaned = data_with_nan.dropna()
    print(cleaned)

    # Fill missing values with a constant
    print("\nFill missing values with 0:")
    filled_zero = data_with_nan.fillna(0)
    print(filled_zero)

    # Fill missing values with mean
    print("\nFill missing values with mean:")
    filled_mean = data_with_nan.fillna(data_with_nan.mean())
    print(filled_mean)

    # Forward fill: use previous valid value
    print("\nForward fill (use previous value):")
    forward_filled = data_with_nan.fillna(method='ffill')
    print(forward_filled)

    # Backward fill: use next valid value
    print("\nBackward fill (use next value):")
    backward_filled = data_with_nan.fillna(method='bfill')
    print(backward_filled)

    # ============================================================================
    # SECTION 8: SUMMARY AND KEY TAKEAWAYS
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    summary = """
    1. Series is a 1-dimensional labeled array
    2. Create Series from lists, dicts, arrays, or scalars
    3. Series have both values and index (labels)
    4. Use [] for basic indexing, .loc for label-based, .iloc for position-based
    5. Operations are element-wise and align by index
    6. Many statistical methods available (mean, median, std, etc.)
    7. Handle missing data with dropna() or fillna()
    8. Apply functions with .apply()
    9. Sort with sort_values() or sort_index()
    10. Get value counts with value_counts()

    Next Steps:
    -----------
    - Practice creating and manipulating Series
    - Try the exercise file: exercises/01_series_exercises.py
    - Move on to Tutorial 02: Introduction to DataFrames
    """

    print(summary)

    # ============================================================================
    # PRACTICE EXERCISES (Try these yourself!)
    # ============================================================================

    print("\n" + "=" * 70)
    print("PRACTICE EXERCISES")
    print("=" * 70)

    exercises = """
    1. Create a Series of your favorite 5 movies with ratings (1-10)
    2. Calculate the average rating
    3. Find movies with rating > 7
    4. Add 0.5 to all ratings
    5. Create a Series of temperatures for a week and convert to Fahrenheit
    6. Create a Series with some NaN values and fill them with the mean
    7. Sort a Series by values in descending order
    8. Find duplicate values in a Series
    9. Apply a custom function to categorize values
    10. Combine two Series with different indices

    See exercises/01_series_exercises.py for detailed exercises!
    """

    print(exercises)
```

---

## Exercises

**Exercise 1.**
Create a Series from a dictionary with 5 key-value pairs. Access a value by its label. Then use `.index` and `.values` to inspect the index and underlying data separately.

??? success "Solution to Exercise 1"
    Create a Series from a dictionary and inspect its components.

        import pandas as pd

        s = pd.Series({'a': 10, 'b': 20, 'c': 30, 'd': 40, 'e': 50})
        print("Value at 'c':", s['c'])
        print("Index:", s.index.tolist())
        print("Values:", s.values)

---

**Exercise 2.**
Create two numeric Series with partially overlapping indices. Add them together and observe how pandas aligns by index, producing `NaN` where indices do not match.

??? success "Solution to Exercise 2"
    Add two Series with different indices.

        import pandas as pd

        s1 = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
        s2 = pd.Series([4, 5, 6], index=['b', 'c', 'd'])
        result = s1 + s2
        print(result)
        # 'a' and 'd' will have NaN

---

**Exercise 3.**
Create a Series of 10 random floats. Use boolean indexing to select only values greater than 0. Then use `.sort_values()` to sort the result in descending order.

??? success "Solution to Exercise 3"
    Filter and sort a random Series.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        s = pd.Series(np.random.randn(10))
        positive = s[s > 0]
        sorted_desc = positive.sort_values(ascending=False)
        print(sorted_desc)
