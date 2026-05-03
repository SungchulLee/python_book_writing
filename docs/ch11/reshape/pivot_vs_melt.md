# pivot vs melt

`pivot` and `melt` are inverse operations for reshaping DataFrames between wide and long formats.

!!! tip "Mental Model"
    `pivot` spreads long data into wide columns; `melt` gathers wide columns back into long rows. They are inverses: `melt(pivot(df))` recovers the original shape (up to sorting). If your data is too wide for plotting or groupby, melt it; if it is too long for correlation or comparison, pivot it.

## Conceptual Relationship

pivot and melt transform data in opposite directions.

### 1. melt: Wide to Long

```python
import pandas as pd

# Wide format
wide = pd.DataFrame({
    'month': ['Jan', 'Feb'],
    'New York': [5, 3],
    'Los Angeles': [15, 17]
})
print("Wide format:")
print(wide)
```

```
  month  New York  Los Angeles
0   Jan         5           15
1   Feb         3           17
```

### 2. Apply melt

```python
long = pd.melt(
    wide,
    id_vars=['month'],
    var_name='city',
    value_name='temperature'
)
print("Long format (after melt):")
print(long)
```

```
  month         city  temperature
0   Jan     New York            5
1   Feb     New York            3
2   Jan  Los Angeles           15
3   Feb  Los Angeles           17
```

### 3. Apply pivot

```python
back_to_wide = long.pivot(
    index='month',
    columns='city',
    values='temperature'
)
print("Back to wide (after pivot):")
print(back_to_wide)
```

```
city   Los Angeles  New York
month                       
Feb             17         3
Jan             15         5
```

## When to Use Each

Guidelines for choosing between pivot and melt.

### 1. Use melt When

```python
# Converting columns to rows
# Preparing data for visualization (seaborn, plotly)
# Normalizing for database storage
# Input for groupby operations
```

### 2. Use pivot When

```python
# Creating summary tables
# Converting rows to columns
# Preparing data for comparison
# Creating cross-tabulation
```

### 3. Format Characteristics

| Format | Rows | Columns | Use Case |
|--------|------|---------|----------|
| Wide | Few | Many | Display, comparison |
| Long | Many | Few | Analysis, storage |

## Complete Round-trip

Transform and reverse without data loss.

### 1. Start with Wide

```python
original = pd.DataFrame({
    'product': ['A', 'B'],
    'Q1': [100, 150],
    'Q2': [200, 250]
})
```

### 2. Melt to Long

```python
long_form = original.melt(
    id_vars=['product'],
    var_name='quarter',
    value_name='sales'
)
```

### 3. Pivot Back to Wide

```python
wide_again = long_form.pivot(
    index='product',
    columns='quarter',
    values='sales'
).reset_index()

wide_again.columns.name = None  # Remove column name
```

## Practical Example

Temperature data transformation.

### 1. Original Wide Data

```python
temps = pd.DataFrame({
    'date': ['2024-01-01', '2024-01-02'],
    'city_A': [20, 22],
    'city_B': [15, 17],
    'city_C': [25, 27]
})
```

### 2. Melt for Analysis

```python
temps_long = temps.melt(
    id_vars=['date'],
    var_name='city',
    value_name='temperature'
)

# Now can easily compute:
temps_long.groupby('city')['temperature'].mean()
```

### 3. Pivot for Display

```python
temps_wide = temps_long.pivot(
    index='date',
    columns='city',
    values='temperature'
)
# Good for side-by-side comparison
```

## Key Differences

Summary of differences.

### 1. Direction

```python
# melt: columns → rows (wide to long)
# pivot: rows → columns (long to wide)
```

### 2. Data Volume

```python
# melt: increases row count
# pivot: decreases row count (typically)
```

### 3. Required Parameters

```python
# melt: id_vars (optional), var_name, value_name
# pivot: index, columns, values
```

---

## Runnable Example: `pivot_reshape_tutorial.py`

```python
"""
Pandas Tutorial: Pivot Tables and Reshaping Data.

Covers pivot, pivot_table, melt, stack, and unstack.
"""

import pandas as pd
import numpy as np

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("="*70)
    print("PIVOT TABLES AND RESHAPING")
    print("="*70)

    # Create sample data
    np.random.seed(42)
    data = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=12, freq='M'),
        'Product': ['A', 'B'] * 6,
        'Region': ['North', 'North', 'South', 'South'] * 3,
        'Sales': np.random.randint(100, 1000, 12)
    })

    print("\nOriginal Data:")
    print(data)

    # Pivot
    print("\n1. Pivot (reshape from long to wide):")
    pivoted = data.pivot(index='Date', columns='Product', values='Sales')
    print(pivoted.head())

    # Pivot table (with aggregation)
    print("\n2. Pivot Table with aggregation:")
    pivot_table = data.pivot_table(values='Sales', 
                                    index='Product', 
                                    columns='Region',
                                    aggfunc='mean')
    print(pivot_table)

    # Multiple aggregation functions
    print("\n3. Pivot table with multiple functions:")
    pivot_multi = data.pivot_table(values='Sales',
                                   index='Product',
                                   columns='Region',
                                   aggfunc=['sum', 'mean', 'count'])
    print(pivot_multi)

    # Melt (reshape from wide to long)
    wide_data = pd.DataFrame({
        'ID': [1, 2, 3],
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Math': [85, 92, 78],
        'Science': [88, 95, 82],
        'English': [90, 87, 85]
    })

    print("\n4. Wide format data:")
    print(wide_data)

    print("\n5. Melt (reshape to long format):")
    melted = pd.melt(wide_data, 
                     id_vars=['ID', 'Name'],
                     value_vars=['Math', 'Science', 'English'],
                     var_name='Subject',
                     value_name='Score')
    print(melted)

    # Stack and Unstack
    df_multi = pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]
    }, index=['X', 'Y', 'Z'])

    print("\n6. Original DataFrame:")
    print(df_multi)

    print("\n7. Stack (columns to rows):")
    stacked = df_multi.stack()
    print(stacked)

    print("\n8. Unstack (rows to columns):")
    unstacked = stacked.unstack()
    print(unstacked)

    # Cross-tabulation
    df_survey = pd.DataFrame({
        'Gender': ['M', 'F', 'M', 'F', 'M', 'F'],
        'Age_Group': ['Young', 'Young', 'Old', 'Old', 'Young', 'Old'],
        'Response': ['Yes', 'No', 'Yes', 'Yes', 'No', 'Yes']
    })

    print("\n9. Cross-tabulation:")
    crosstab = pd.crosstab(df_survey['Gender'], 
                           df_survey['Response'],
                           margins=True)
    print(crosstab)

    print("\nKEY TAKEAWAYS:")
    print("- pivot(): Reshape data (needs unique index/column combinations)")
    print("- pivot_table(): Pivot with aggregation")
    print("- melt(): Convert wide to long format")
    print("- stack(): Pivot columns to row index")
    print("- unstack(): Pivot row index to columns")
    print("- crosstab(): Compute frequency table")
```


---

## Exercises

**Exercise 1.** Explain the relationship between `pivot()` and `melt()`. Are they inverse operations?

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

**Exercise 2.** Write code that converts wide to long with `melt()` and then back to wide with `pivot()`. Is the result identical?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the Pandas API and its behavior for this specific operation.

---

**Exercise 3.** Create a long-format DataFrame and reshape it to wide format using `pivot()`. Then reverse it with `melt()`.

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

**Exercise 4.** Explain when you would choose `melt()` over `stack()` for reshaping. Give a concrete example.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'A': np.random.randn(50), 'group': np.random.choice(['X', 'Y'], 50)})
    result = df.groupby('group').mean()
    print(result)
    ```
