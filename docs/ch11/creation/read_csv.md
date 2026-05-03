# Loading CSV Files

The `pd.read_csv()` function loads comma-separated values files into DataFrames with extensive customization options.

!!! tip "Mental Model"
    `read_csv` is a parser with dozens of knobs. At its core it splits each line by a delimiter, uses the first row as column names, and infers dtypes. Most real-world CSV quirks -- wrong delimiters, missing headers, date columns stored as strings -- are handled by a single keyword argument rather than post-load cleanup.

## Basic Usage

Load a CSV file with default settings.

### 1. Simple Load

```python
import pandas as pd

df = pd.read_csv('data.csv')
print(df.head())
```

### 2. From URL

```python
url = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'
df = pd.read_csv(url)
print(df.head())
```

### 3. Check Shape

```python
print(df.shape)  # (rows, columns)
```

## Keyword - index_col

Set a column as the DataFrame index.

### 1. First Column as Index

```python
df = pd.read_csv('data.csv', index_col=0)
```

### 2. Named Column as Index

```python
df = pd.read_csv('data.csv', index_col='Date')
```

### 3. Multiple Index Columns

```python
df = pd.read_csv('data.csv', index_col=[0, 1])  # MultiIndex
```

## Keyword - sep

Specify the delimiter character.

### 1. Semicolon Delimiter

```python
df = pd.read_csv('data.csv', sep=';')
```

### 2. Tab Delimiter

```python
df = pd.read_csv('data.tsv', sep='\t')
```

### 3. Custom Delimiter

```python
df = pd.read_csv('data.txt', sep='|')
```

## Keyword - header

Control which row becomes column names.

### 1. Default (Infer)

```python
df = pd.read_csv('data.csv')  # header='infer'
# First row becomes column names
```

### 2. No Header

```python
df = pd.read_csv('data.csv', header=None)
# Columns named 0, 1, 2, ...
```

### 3. Specific Row

```python
df = pd.read_csv('data.csv', header=2)
# Row 2 becomes header, rows 0-1 skipped
```

## Keyword - names

Provide custom column names.

### 1. Override Columns

```python
names = ['A', 'B', 'C', 'D']
df = pd.read_csv('data.csv', names=names, header=0)
```

### 2. With No Header

```python
df = pd.read_csv('data.csv', names=names, header=None)
```

### 3. Partial Names

```python
# Must provide names for all columns
```

## Keyword - skiprows

Skip rows at the beginning.

### 1. Skip N Rows

```python
df = pd.read_csv('data.csv', skiprows=3)
# Skips first 3 rows
```

### 2. Skip Specific Rows

```python
df = pd.read_csv('data.csv', skiprows=[0, 2, 4])
# Skips rows 0, 2, and 4
```

### 3. Skip with Function

```python
df = pd.read_csv('data.csv', skiprows=lambda x: x in [0, 1, 2])
```

## Keyword - usecols

Select specific columns to load.

### 1. By Name

```python
df = pd.read_csv('data.csv', usecols=['Name', 'Age', 'City'])
```

### 2. By Index

```python
df = pd.read_csv('data.csv', usecols=[0, 2, 4])
```

### 3. Memory Efficiency

```python
# Loading only needed columns saves memory
```

## Keyword - parse_dates

Parse columns as datetime.

### 1. Single Column

```python
df = pd.read_csv('data.csv', parse_dates=['Date'])
```

### 2. Multiple Columns

```python
df = pd.read_csv('data.csv', parse_dates=['Start', 'End'])
```

### 3. With Index

```python
df = pd.read_csv('data.csv', index_col='Date', parse_dates=True)
```

## Keyword - dayfirst

European date format (day before month).

### 1. Enable dayfirst

```python
# For dates like 31/12/2024 (day/month/year)
df = pd.read_csv('data.csv', parse_dates=['Date'], dayfirst=True)
```

### 2. Default (Month First)

```python
# For dates like 12/31/2024 (month/day/year)
df = pd.read_csv('data.csv', parse_dates=['Date'])
```

### 3. Combined Usage

```python
df = pd.read_csv(
    'data.csv',
    index_col=0,
    parse_dates=True,
    dayfirst=True
)
```

## Real-World Example

Load financial data with multiple options.

### 1. Stock Data

```python
url = 'http://www.stoxx.com/download/historical_values/hbrbcpe.txt'
names = ['SX5P', 'SX5E', 'SXXP', 'SXXE', 'SXXF', 'SXXA', 'DK5F', 'DKXF']

df = pd.read_csv(
    url,
    index_col=0,
    parse_dates=True,
    dayfirst=True,
    sep=';',
    header=None,
    skiprows=4,
    names=names
)
```

### 2. Verify Load

```python
print(df.head())
print(df.index[:3])
print(df.columns)
```

### 3. Handle Inconsistent Data

```python
# Use skiprows with lambda for complex skip logic
df = pd.read_csv(
    url,
    skiprows=lambda x: (x in [0,1,2,3]) or (x >= 3886)
)
```

---

## Runnable Example: `reading_writing_tutorial.py`

```python
"""
Pandas Tutorial 03: Reading and Writing Data
=============================================

This tutorial covers importing and exporting data in various formats.
We'll cover:
1. Reading CSV files
2. Writing CSV files
3. Reading Excel files
4. Writing Excel files
5. Reading JSON files
6. Writing JSON files
7. Reading from SQL databases
8. Other formats (HTML, clipboard, etc.)

Prerequisites: Tutorials 01-02
Difficulty: Beginner
"""

import pandas as pd
import numpy as np
import os

# ============================================================================
# SECTION 1: READING CSV FILES
# ============================================================================

if __name__ == "__main__":

    print("=" * 70)
    print("READING CSV FILES")
    print("=" * 70)

    # Create a sample CSV file for demonstration
    sample_csv_data = """Name,Age,City,Salary
    Alice,25,New York,50000
    Bob,30,Los Angeles,60000
    Charlie,35,Chicago,75000
    David,28,Houston,55000
    Eve,32,Phoenix,65000"""

    # Write the sample data to a file
    with open('sample_data.csv', 'w') as f:
        f.write(sample_csv_data)

    # Method 1: Basic CSV reading
    print("\n1. Basic CSV reading:")
    df_csv = pd.read_csv('sample_data.csv')
    print(df_csv)
    print(f"Shape: {df_csv.shape}")

    # Method 2: Read CSV with custom delimiter
    # Create a sample with different delimiter
    sample_tsv = """Name\tAge\tScore
    Alice\t25\t85
    Bob\t30\t92"""
    with open('sample_data.tsv', 'w') as f:
        f.write(sample_tsv)

    print("\n2. Read with custom delimiter (tab-separated):")
    df_tsv = pd.read_csv('sample_data.tsv', sep='\t')
    print(df_tsv)

    # Method 3: Read CSV with custom index column
    print("\n3. Read CSV with 'Name' as index:")
    df_indexed = pd.read_csv('sample_data.csv', index_col='Name')
    print(df_indexed)

    # Method 4: Read CSV and select specific columns
    print("\n4. Read only specific columns:")
    df_selected = pd.read_csv('sample_data.csv', usecols=['Name', 'Salary'])
    print(df_selected)

    # Method 5: Read CSV and skip rows
    print("\n5. Read CSV skipping first row:")
    df_skipped = pd.read_csv('sample_data.csv', skiprows=1)
    print(df_skipped)

    # Method 6: Read CSV with specific data types
    print("\n6. Read CSV with specified data types:")
    df_types = pd.read_csv('sample_data.csv', 
                           dtype={'Age': int, 'Salary': float})
    print(df_types.dtypes)

    # Method 7: Handle missing values while reading
    sample_with_na = """Name,Age,City
    Alice,25,New York
    Bob,,Los Angeles
    Charlie,35,"""
    with open('sample_na.csv', 'w') as f:
        f.write(sample_with_na)

    print("\n7. Read CSV handling missing values:")
    df_na = pd.read_csv('sample_na.csv')
    print(df_na)
    print("\nMissing values filled with 'Unknown':")
    df_na_filled = pd.read_csv('sample_na.csv', na_values=[''], 
                               keep_default_na=True).fillna('Unknown')
    print(df_na_filled)

    # Method 8: Read large CSV in chunks (useful for big files)
    print("\n8. Read CSV in chunks:")
    chunk_size = 2
    chunks = []
    for chunk in pd.read_csv('sample_data.csv', chunksize=chunk_size):
        print(f"Processing chunk of size {len(chunk)}")
        chunks.append(chunk)
    # Combine all chunks
    df_chunked = pd.concat(chunks, ignore_index=True)
    print("Combined data:")
    print(df_chunked)

    # ============================================================================
    # SECTION 2: WRITING CSV FILES
    # ============================================================================

    print("\n" + "=" * 70)
    print("WRITING CSV FILES")
    print("=" * 70)

    # Create a sample DataFrame
    df_to_save = pd.DataFrame({
        'Product': ['A', 'B', 'C', 'D'],
        'Price': [10.5, 20.0, 15.75, 30.25],
        'Quantity': [100, 150, 200, 50]
    })

    print("DataFrame to save:")
    print(df_to_save)

    # Method 1: Basic CSV writing
    df_to_save.to_csv('output_basic.csv', index=False)
    print("\n1. Saved to 'output_basic.csv' (without index)")

    # Method 2: Save with index
    df_to_save.to_csv('output_with_index.csv', index=True)
    print("2. Saved to 'output_with_index.csv' (with index)")

    # Method 3: Save with custom delimiter
    df_to_save.to_csv('output_tsv.txt', sep='\t', index=False)
    print("3. Saved to 'output_tsv.txt' (tab-delimited)")

    # Method 4: Save specific columns only
    df_to_save.to_csv('output_selected.csv', 
                      columns=['Product', 'Price'], index=False)
    print("4. Saved to 'output_selected.csv' (Product and Price only)")

    # Method 5: Save with custom header names
    df_to_save.to_csv('output_custom_header.csv',
                      header=['Item', 'Cost', 'Stock'], index=False)
    print("5. Saved to 'output_custom_header.csv' (custom headers)")

    # Method 6: Append to existing CSV
    df_new_data = pd.DataFrame({
        'Product': ['E', 'F'],
        'Price': [25.0, 18.5],
        'Quantity': [75, 125]
    })
    df_new_data.to_csv('output_basic.csv', mode='a', header=False, index=False)
    print("6. Appended new data to 'output_basic.csv'")

    # Verify the append
    df_check = pd.read_csv('output_basic.csv')
    print("Updated file content:")
    print(df_check)

    # Method 7: Save with float formatting
    df_to_save.to_csv('output_formatted.csv', 
                      index=False, float_format='%.2f')
    print("\n7. Saved to 'output_formatted.csv' (2 decimal places)")

    # ============================================================================
    # SECTION 3: READING EXCEL FILES
    # ============================================================================

    print("\n" + "=" * 70)
    print("READING EXCEL FILES")
    print("=" * 70)

    # Create a sample Excel file first
    # Note: openpyxl is required for Excel operations
    try:
        import openpyxl
        excel_available = True
    except ImportError:
        excel_available = False
        print("Note: Install openpyxl for Excel support: pip install openpyxl")

    if excel_available:
        # Create sample data
        df_excel_sample = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May'],
            'Sales': [10000, 12000, 15000, 13000, 16000],
            'Expenses': [8000, 9000, 11000, 10000, 12000]
        })

        # Save to Excel
        df_excel_sample.to_excel('sample_data.xlsx', sheet_name='Sales', index=False)
        print("Created sample Excel file: 'sample_data.xlsx'")

        # Method 1: Read Excel file (first sheet by default)
        print("\n1. Read Excel file (default first sheet):")
        df_excel = pd.read_excel('sample_data.xlsx')
        print(df_excel)

        # Method 2: Read specific sheet by name
        print("\n2. Read specific sheet:")
        df_excel_sheet = pd.read_excel('sample_data.xlsx', sheet_name='Sales')
        print(df_excel_sheet)

        # Create a multi-sheet Excel file
        with pd.ExcelWriter('multi_sheet.xlsx') as writer:
            df_excel_sample.to_excel(writer, sheet_name='Sales', index=False)
            df_excel_sample.to_excel(writer, sheet_name='Q1', index=False)
            df_excel_sample.to_excel(writer, sheet_name='Q2', index=False)
        print("\n3. Created multi-sheet Excel file")

        # Read all sheets
        print("4. Read all sheets:")
        excel_file = pd.ExcelFile('multi_sheet.xlsx')
        print(f"Available sheets: {excel_file.sheet_names}")

        # Read all sheets into a dictionary
        all_sheets = pd.read_excel('multi_sheet.xlsx', sheet_name=None)
        for sheet_name, df in all_sheets.items():
            print(f"\nSheet: {sheet_name}")
            print(df.head(2))

        # Method 3: Read specific rows and columns
        print("\n5. Read specific range (rows 1-3):")
        df_range = pd.read_excel('sample_data.xlsx', nrows=3)
        print(df_range)

        # Method 4: Skip rows
        print("\n6. Read skipping first row:")
        df_skip = pd.read_excel('sample_data.xlsx', skiprows=1)
        print(df_skip)

    # ============================================================================
    # SECTION 4: WRITING EXCEL FILES
    # ============================================================================

    print("\n" + "=" * 70)
    print("WRITING EXCEL FILES")
    print("=" * 70)

    if excel_available:
        # Create sample data
        df_products = pd.DataFrame({
            'Product': ['Laptop', 'Mouse', 'Keyboard', 'Monitor'],
            'Price': [999.99, 29.99, 79.99, 299.99],
            'Stock': [50, 200, 150, 75]
        })

        print("DataFrame to save:")
        print(df_products)

        # Method 1: Basic Excel writing
        df_products.to_excel('products.xlsx', index=False)
        print("\n1. Saved to 'products.xlsx'")

        # Method 2: Save to specific sheet
        df_products.to_excel('products_named.xlsx', 
                            sheet_name='Inventory', index=False)
        print("2. Saved to 'products_named.xlsx' with sheet name 'Inventory'")

        # Method 3: Save multiple DataFrames to different sheets
        df_sales = pd.DataFrame({
            'Month': ['Jan', 'Feb', 'Mar'],
            'Revenue': [50000, 60000, 75000]
        })

        with pd.ExcelWriter('company_data.xlsx') as writer:
            df_products.to_excel(writer, sheet_name='Products', index=False)
            df_sales.to_excel(writer, sheet_name='Sales', index=False)
        print("3. Saved multiple sheets to 'company_data.xlsx'")

        # Method 4: Append to existing Excel file
        with pd.ExcelWriter('company_data.xlsx', mode='a', engine='openpyxl') as writer:
            df_new = pd.DataFrame({'Info': ['Additional data']})
            df_new.to_excel(writer, sheet_name='Notes', index=False)
        print("4. Appended new sheet to existing Excel file")

        # Method 5: Format while saving (requires additional packages)
        # For basic formatting, we can use ExcelWriter with engine options
        with pd.ExcelWriter('formatted.xlsx', engine='openpyxl') as writer:
            df_products.to_excel(writer, sheet_name='Products', index=False)
            # Access the worksheet
            workbook = writer.book
            worksheet = writer.sheets['Products']
            # Set column widths
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
        print("5. Saved with column width formatting")

    # ============================================================================
    # SECTION 5: READING JSON FILES
    # ============================================================================

    print("\n" + "=" * 70)
    print("READING JSON FILES")
    print("=" * 70)

    # Create sample JSON data
    import json

    sample_json_records = [
        {"name": "Alice", "age": 25, "city": "New York"},
        {"name": "Bob", "age": 30, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"}
    ]

    # Save as JSON
    with open('sample_records.json', 'w') as f:
        json.dump(sample_json_records, f)

    print("Created sample JSON file: 'sample_records.json'")

    # Method 1: Read JSON (records format)
    print("\n1. Read JSON (records format):")
    df_json = pd.read_json('sample_records.json')
    print(df_json)

    # Method 2: Different JSON formats
    # Create column-oriented JSON
    sample_json_columns = {
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["New York", "Los Angeles", "Chicago"]
    }
    with open('sample_columns.json', 'w') as f:
        json.dump(sample_json_columns, f)

    print("\n2. Read JSON (columns format):")
    df_json_cols = pd.read_json('sample_columns.json')
    print(df_json_cols)

    # Method 3: Read nested JSON
    nested_json = [
        {"name": "Alice", "address": {"city": "NYC", "zip": "10001"}},
        {"name": "Bob", "address": {"city": "LA", "zip": "90001"}}
    ]
    with open('nested.json', 'w') as f:
        json.dump(nested_json, f)

    print("\n3. Read nested JSON:")
    df_nested = pd.read_json('nested.json')
    print(df_nested)

    # To flatten nested structures, use json_normalize
    from pandas import json_normalize
    print("\n4. Flatten nested JSON:")
    df_flat = json_normalize(nested_json)
    print(df_flat)

    # ============================================================================
    # SECTION 6: WRITING JSON FILES
    # ============================================================================

    print("\n" + "=" * 70)
    print("WRITING JSON FILES")
    print("=" * 70)

    # Create sample DataFrame
    df_to_json = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Product A', 'Product B', 'Product C'],
        'price': [10.5, 20.0, 15.75]
    })

    print("DataFrame to save:")
    print(df_to_json)

    # Method 1: Save as JSON (records format)
    df_to_json.to_json('output_records.json', orient='records', indent=2)
    print("\n1. Saved as 'output_records.json' (records format)")

    # Method 2: Save as JSON (columns format)
    df_to_json.to_json('output_columns.json', orient='columns', indent=2)
    print("2. Saved as 'output_columns.json' (columns format)")

    # Method 3: Save as JSON (index format)
    df_to_json.to_json('output_index.json', orient='index', indent=2)
    print("3. Saved as 'output_index.json' (index format)")

    # Method 4: Save as JSON (split format)
    df_to_json.to_json('output_split.json', orient='split', indent=2)
    print("4. Saved as 'output_split.json' (split format)")

    # Method 5: Save as JSON (values format - just values)
    df_to_json.to_json('output_values.json', orient='values', indent=2)
    print("5. Saved as 'output_values.json' (values only)")

    # Show content of each format
    print("\n6. Comparing JSON formats:")
    with open('output_records.json', 'r') as f:
        print("Records format:")
        print(f.read())

    # ============================================================================
    # SECTION 7: OTHER DATA FORMATS
    # ============================================================================

    print("\n" + "=" * 70)
    print("OTHER DATA FORMATS")
    print("=" * 70)

    # HTML tables
    html_string = """
    <table>
        <tr><th>Name</th><th>Score</th></tr>
        <tr><td>Alice</td><td>85</td></tr>
        <tr><td>Bob</td><td>92</td></tr>
    </table>
    """

    print("\n1. Read HTML table:")
    with open('sample_table.html', 'w') as f:
        f.write(html_string)

    try:
        dfs_html = pd.read_html('sample_table.html')
        print(f"Found {len(dfs_html)} table(s)")
        print(dfs_html[0])
    except ImportError:
        print("Note: Install lxml or html5lib for HTML support")

    # Clipboard (copy/paste)
    print("\n2. Clipboard operations:")
    print("To copy DataFrame to clipboard: df.to_clipboard()")
    print("To read from clipboard: pd.read_clipboard()")

    # Pickle (Python binary format - preserves all pandas data types)
    print("\n3. Pickle format (for Python-to-Python transfer):")
    df_to_pickle = pd.DataFrame({'A': [1, 2, 3], 'B': ['x', 'y', 'z']})
    df_to_pickle.to_pickle('data.pkl')
    df_from_pickle = pd.read_pickle('data.pkl')
    print("Saved and loaded from pickle:")
    print(df_from_pickle)

    # Parquet (efficient binary format)
    print("\n4. Parquet format (efficient for large datasets):")
    try:
        df_to_pickle.to_parquet('data.parquet')
        df_from_parquet = pd.read_parquet('data.parquet')
        print("Saved and loaded from parquet:")
        print(df_from_parquet)
    except ImportError:
        print("Note: Install pyarrow or fastparquet for Parquet support")

    # ============================================================================
    # SECTION 8: READING FROM DATABASES (SQL)
    # ============================================================================

    print("\n" + "=" * 70)
    print("READING FROM DATABASES")
    print("=" * 70)

    try:
        import sqlite3

        # Create a sample database
        conn = sqlite3.connect('sample.db')

        # Create a sample table
        sample_data = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'score': [85, 92, 78, 88, 95]
        })

        # Write to database
        sample_data.to_sql('students', conn, if_exists='replace', index=False)
        print("Created sample database 'sample.db' with 'students' table")

        # Method 1: Read entire table
        print("\n1. Read entire table:")
        df_sql = pd.read_sql('SELECT * FROM students', conn)
        print(df_sql)

        # Method 2: Read with SQL query
        print("\n2. Read with WHERE clause:")
        df_sql_query = pd.read_sql('SELECT * FROM students WHERE score > 85', conn)
        print(df_sql_query)

        # Method 3: Read table by name
        print("\n3. Read table by name:")
        df_sql_table = pd.read_sql_table('students', conn)
        print(df_sql_table)

        # Close connection
        conn.close()
        print("\n4. Database connection closed")

    except ImportError:
        print("SQLite is part of Python standard library")
        print("For other databases, install sqlalchemy and appropriate drivers")

    # ============================================================================
    # SECTION 9: BEST PRACTICES AND TIPS
    # ============================================================================

    print("\n" + "=" * 70)
    print("BEST PRACTICES AND TIPS")
    print("=" * 70)

    tips = """
    1. CSV vs Excel:
       - CSV: Faster, smaller files, text-based
       - Excel: Supports multiple sheets, formatting, formulas

    2. For large files:
       - Use chunksize parameter for CSV
       - Consider Parquet for efficient storage
       - Use compression: to_csv('file.csv.gz', compression='gzip')

    3. Handling encoding issues:
       - Specify encoding: pd.read_csv('file.csv', encoding='utf-8')
       - Common encodings: 'utf-8', 'latin-1', 'cp1252'

    4. JSON formats:
       - 'records': [{col: val}, {col: val}]
       - 'columns': {col: {index: val}}
       - 'index': {index: {col: val}}
       - 'split': {columns: [], index: [], data: [[]]}

    5. Memory efficiency:
       - Specify dtypes when reading
       - Read only needed columns with usecols
       - Use categorical for repeated strings

    6. Always close database connections!

    7. Use context managers when possible:
       with pd.ExcelWriter('file.xlsx') as writer:
           df.to_excel(writer)
    """

    print(tips)

    # Clean up created files
    import glob
    files_to_remove = glob.glob('*.csv') + glob.glob('*.txt') + \
                     glob.glob('*.json') + glob.glob('*.xlsx') + \
                     glob.glob('*.html') + glob.glob('*.pkl') + \
                     glob.glob('*.parquet') + glob.glob('*.db')

    print(f"\nCreated {len(files_to_remove)} example files during this tutorial")
    print("These files are for learning purposes and can be deleted if not needed")

    # ============================================================================
    # SECTION 10: SUMMARY
    # ============================================================================

    print("\n" + "=" * 70)
    print("KEY TAKEAWAYS")
    print("=" * 70)

    summary = """
    1. Read CSV: pd.read_csv('file.csv')
    2. Write CSV: df.to_csv('file.csv', index=False)
    3. Read Excel: pd.read_excel('file.xlsx', sheet_name='Sheet1')
    4. Write Excel: df.to_excel('file.xlsx', sheet_name='Sheet1')
    5. Read JSON: pd.read_json('file.json')
    6. Write JSON: df.to_json('file.json', orient='records')
    7. Read SQL: pd.read_sql('SELECT * FROM table', connection)
    8. Write SQL: df.to_sql('table_name', connection)
    9. Use appropriate format for your needs (CSV for simple, Excel for complex)
    10. Handle large files with chunksize or Parquet format

    Next Steps:
    -----------
    - Practice reading/writing different formats
    - Try the exercise file: exercises/03_io_exercises.py
    - Move on to Tutorial 04: Data Cleaning and Preprocessing
    """

    print(summary)
```

---

## Exercises

**Exercise 1.**
Using `pd.read_csv` with `io.StringIO`, read the following CSV string and set the `'date'` column as the index while parsing it as a datetime: `"date,value\n2024-01-01,10\n2024-01-02,20\n2024-01-03,30"`. Print the resulting DataFrame and confirm the index dtype is `datetime64`.

??? success "Solution to Exercise 1"
    Use `index_col` and `parse_dates` together.

        import pandas as pd
        import io

        csv_data = "date,value\n2024-01-01,10\n2024-01-02,20\n2024-01-03,30"
        df = pd.read_csv(
            io.StringIO(csv_data),
            index_col='date',
            parse_dates=True
        )
        print(df)
        print(f"Index dtype: {df.index.dtype}")  # datetime64[ns]

---

**Exercise 2.**
Read a CSV string with columns `'name'`, `'age'`, `'salary'`, `'department'` but only load the `'name'` and `'salary'` columns using the `usecols` parameter. Also skip the first data row using `skiprows`.

??? success "Solution to Exercise 2"
    Combine `usecols` and `skiprows` to selectively load data.

        import pandas as pd
        import io

        csv_data = "name,age,salary,department\nAlice,30,70000,HR\nBob,25,60000,IT\nCarol,35,80000,Finance"
        df = pd.read_csv(
            io.StringIO(csv_data),
            usecols=['name', 'salary'],
            skiprows=[1]  # Skip the first data row (Alice)
        )
        print(df)

---

**Exercise 3.**
Read a CSV string that uses `';'` as the separator and `','` as the decimal separator (European format): `"item;price\nWidget;12,50\nGadget;25,99"`. Use the `sep` and `decimal` parameters to load the prices as proper floats.

??? success "Solution to Exercise 3"
    Handle European CSV format with semicolon separator and comma decimal.

        import pandas as pd
        import io

        csv_data = "item;price\nWidget;12,50\nGadget;25,99"
        df = pd.read_csv(
            io.StringIO(csv_data),
            sep=';',
            decimal=','
        )
        print(df)
        print(f"price dtype: {df['price'].dtype}")  # float64
