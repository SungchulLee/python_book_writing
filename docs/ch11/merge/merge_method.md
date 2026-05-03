# merge Method

The `merge()` function combines DataFrames based on column values, similar to SQL joins. It is the most flexible method for combining datasets.

!!! tip "Mental Model"
    `merge()` is SQL JOIN for DataFrames. You specify which columns to match on (`on`, `left_on`, `right_on`), how to handle mismatches (`how`), and what to do with name collisions (`suffixes`). It defaults to an inner join on all shared column names -- always set `on` explicitly to avoid surprises.

## Basic Syntax

Merge two DataFrames on a common column.

### 1. Simple Merge

```python
import pandas as pd

df1 = pd.DataFrame({
    'city': ['NY', 'SF', 'LA'],
    'temperature': [21, 14, 35]
})

df2 = pd.DataFrame({
    'city': ['SF', 'NY', 'ICN'],
    'humidity': [65, 68, 75]
})

df = pd.merge(df1, df2, on='city')
print(df)
```

```
  city  temperature  humidity
0   NY           21        68
1   SF           14        65
```

### 2. Default Inner Join

By default, merge performs an inner join, keeping only matching rows.

### 3. Method Syntax

```python
# Function syntax
pd.merge(df1, df2, on='key')

# Method syntax (equivalent)
df1.merge(df2, on='key')
```

## LeetCode Example: Person and Address

Combine person information with address.

### 1. Sample Data

```python
person = pd.DataFrame({
    'personId': [1, 2, 3],
    'firstName': ['John', 'Jane', 'Jake'],
    'lastName': ['Doe', 'Smith', 'Brown']
})

address = pd.DataFrame({
    'personId': [1, 3],
    'city': ['New York', 'Los Angeles'],
    'state': ['NY', 'CA']
})
```

### 2. Left Merge

```python
merged_df = person.merge(address, on='personId', how='left')
print(merged_df)
```

### 3. Result

```
   personId firstName lastName         city state
0         1      John      Doe     New York    NY
1         2      Jane    Smith          NaN   NaN
2         3      Jake    Brown  Los Angeles    CA
```

## LeetCode Example: Project Employees

Join projects with employee experience.

### 1. Sample Data

```python
project = pd.DataFrame({
    'project_id': [101, 102, 103],
    'project_name': ['Project A', 'Project B', 'Project C']
})

employee = pd.DataFrame({
    'employee_id': [1, 2, 3, 4, 5],
    'project_id': [101, 101, 102, 102, 103],
    'experience_years': [5, 7, 3, 4, 6]
})
```

### 2. Merge with Default

```python
merged_df = pd.merge(project, employee, how='left')
print(merged_df)
```

### 3. Auto-detected Key

When `on=None`, merge uses common column names automatically.

## Common Column Detection

Merge automatically finds common columns when `on` is not specified.

### 1. Auto Detection

```python
# Both DataFrames have 'project_id' column
pd.merge(project, employee)  # on='project_id' inferred
```

### 2. Multiple Common Columns

```python
# If both have ['key1', 'key2'], merges on both
pd.merge(df1, df2)
```

### 3. No Common Columns

```python
# Raises ValueError if no common columns exist
# Must specify left_on and right_on
```

## Merge Result Structure

Understanding the output DataFrame.

### 1. Column Order

```python
# Left DataFrame columns first, then right
# Common column appears once (unless using suffixes)
```

### 2. Row Order

```python
# Order depends on join type and matching
```

### 3. Index Reset

```python
# Merge resets index to RangeIndex
# Original indices are discarded
```

---

## Runnable Example: `merge_join_tutorial.py`

```python
"""
Pandas Tutorial: Merging, Joining, and Concatenating DataFrames.

Covers different ways to combine DataFrames.
"""

import pandas as pd
import numpy as np

# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":

    print("="*70)
    print("MERGING, JOINING, AND CONCATENATING")
    print("="*70)

    # Create sample DataFrames
    df1 = pd.DataFrame({
        'ID': [1, 2, 3, 4],
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 28]
    })

    df2 = pd.DataFrame({
        'ID': [1, 2, 3, 5],
        'Department': ['HR', 'IT', 'Finance', 'Marketing'],
        'Salary': [50000, 60000, 75000, 55000]
    })

    print("\nDataFrame 1 (Employees):")
    print(df1)
    print("\nDataFrame 2 (Departments):")
    print(df2)

    # Inner join (default)
    print("\n1. Inner Join (intersection):")
    inner_merged = pd.merge(df1, df2, on='ID', how='inner')
    print(inner_merged)

    # Left join
    print("\n2. Left Join (keep all from left):")
    left_merged = pd.merge(df1, df2, on='ID', how='left')
    print(left_merged)

    # Right join
    print("\n3. Right Join (keep all from right):")
    right_merged = pd.merge(df1, df2, on='ID', how='right')
    print(right_merged)

    # Outer join
    print("\n4. Outer Join (keep all from both):")
    outer_merged = pd.merge(df1, df2, on='ID', how='outer')
    print(outer_merged)

    # Merge on different column names
    df3 = pd.DataFrame({
        'EmpID': [1, 2, 3],
        'Project': ['A', 'B', 'C']
    })

    print("\n5. Merge on different column names:")
    merged_diff = pd.merge(df1, df3, left_on='ID', right_on='EmpID')
    print(merged_diff)

    # Concatenate DataFrames vertically
    df_top = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df_bottom = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

    print("\n6. Concatenate vertically (stack rows):")
    print("Top:")
    print(df_top)
    print("Bottom:")
    print(df_bottom)
    print("Result:")
    vertical_concat = pd.concat([df_top, df_bottom], ignore_index=True)
    print(vertical_concat)

    # Concatenate horizontally
    df_left = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    df_right = pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})

    print("\n7. Concatenate horizontally (add columns):")
    horizontal_concat = pd.concat([df_left, df_right], axis=1)
    print(horizontal_concat)

    # Join (using index)
    df_indexed1 = df1.set_index('ID')
    df_indexed2 = df2.set_index('ID')

    print("\n8. Join using index:")
    joined = df_indexed1.join(df_indexed2, how='inner')
    print(joined)

    print("\nKEY TAKEAWAYS:")
    print("- merge(): SQL-style joins on columns")
    print("- concat(): Stack DataFrames vertically or horizontally")
    print("- join(): Merge on index")
    print("- Join types: inner, left, right, outer")
    print("- Use on= for same column names, left_on=/right_on= for different names")
```

---

## Exercises

**Exercise 1.**
Create two DataFrames sharing a `'key'` column with partial overlap. Perform a default merge (inner join) and count the resulting rows. Then perform an outer merge and compare.

??? success "Solution to Exercise 1"
    Compare inner and outer merge row counts.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b', 'c'], 'val1': [1, 2, 3]})
        df2 = pd.DataFrame({'key': ['b', 'c', 'd'], 'val2': [4, 5, 6]})
        inner = pd.merge(df1, df2, on='key')
        outer = pd.merge(df1, df2, on='key', how='outer')
        print(f"Inner: {len(inner)} rows")
        print(f"Outer: {len(outer)} rows")

---

**Exercise 2.**
Create an `orders` DataFrame with a `'product_id'` column and a `products` DataFrame with a `'product_id'` and `'product_name'` column. Use `pd.merge()` to look up the product name for each order.

??? success "Solution to Exercise 2"
    Look up product names for orders.

        import pandas as pd

        orders = pd.DataFrame({'order_id': [1, 2, 3], 'product_id': [101, 102, 101]})
        products = pd.DataFrame({'product_id': [101, 102, 103], 'product_name': ['Widget', 'Gadget', 'Doohickey']})
        result = pd.merge(orders, products, on='product_id')
        print(result)

---

**Exercise 3.**
Create two DataFrames and merge them using both the function syntax `pd.merge(df1, df2)` and the method syntax `df1.merge(df2)`. Verify both produce identical results.

??? success "Solution to Exercise 3"
    Verify function syntax and method syntax produce the same result.

        import pandas as pd

        df1 = pd.DataFrame({'key': ['a', 'b'], 'x': [1, 2]})
        df2 = pd.DataFrame({'key': ['a', 'b'], 'y': [3, 4]})
        result_func = pd.merge(df1, df2, on='key')
        result_method = df1.merge(df2, on='key')
        assert result_func.equals(result_method)
        print("Both approaches produce identical results.")
