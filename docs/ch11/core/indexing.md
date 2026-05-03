# Indexing and Selection

Indexing is one of pandas' most powerful features. Understanding the difference between label-based and position-based selection is essential.

!!! tip "Mental Model"
    Pandas has two addressing systems: `loc` uses label names (like looking up a word in a dictionary), and `iloc` uses integer positions (like accessing an array by index). Mixing them up is the most common pandas mistake. When in doubt, `loc` for labels, `iloc` for integers.

## Label-based Selection

The `loc` accessor selects by labels.

### 1. Single Row by Label

```python
import pandas as pd

df = pd.DataFrame({
    "price": [100, 101, 102],
    "volume": [10, 12, 9]
}, index=['day1', 'day2', 'day3'])

print(df.loc['day1'])
```

```
price     100
volume     10
Name: day1, dtype: int64
```

### 2. Row and Column Selection

```python
df.loc['day1', 'price']       # Single value
df.loc['day1':'day2', 'price']  # Slice (inclusive)
df.loc[:, 'price']            # All rows, one column
```

### 3. Multiple Labels

```python
df.loc[['day1', 'day3'], ['price', 'volume']]
```

## Position-based Selection

The `iloc` accessor selects by integer positions.

### 1. Single Row by Position

```python
df.iloc[0]  # First row
```

### 2. Row and Column by Position

```python
df.iloc[0, 0]      # First row, first column
df.iloc[0:2, 0]    # First two rows, first column
df.iloc[:, 0]      # All rows, first column
```

### 3. Integer Slicing

```python
df.iloc[0:2]       # First two rows (exclusive end)
df.iloc[-1]        # Last row
```

## Boolean Indexing

Select rows based on conditions.

### 1. Single Condition

```python
df[df["price"] > 100]
```

### 2. Multiple Conditions

```python
df[(df["price"] > 100) & (df["volume"] > 10)]
df[(df["price"] > 102) | (df["volume"] < 10)]
```

### 3. Using Query

```python
df.query("price > 100 and volume > 10")
```

## Chained Indexing

Avoid chained indexing to prevent unexpected behavior.

### 1. Problematic Pattern

```python
# This can cause SettingWithCopyWarning
df[df["price"] > 100]["volume"] = 20
```

### 2. Correct Approach

```python
df.loc[df["price"] > 100, "volume"] = 20
```

### 3. Copy vs View

Chained indexing may return a view or copy unpredictably.

## Setting Values

Use `loc` and `iloc` for assignment.

### 1. Single Value

```python
df.loc['day1', 'price'] = 105
```

### 2. Multiple Values

```python
df.loc['day1', ['price', 'volume']] = [105, 15]
```

### 3. Conditional Assignment

```python
df.loc[df['price'] > 100, 'flag'] = True
```

## Best Practices

Follow these guidelines for clean indexing code.

### 1. Explicit Selection

Always use `loc` or `iloc` explicitly:

```python
# Preferred
df.loc[0]     # If 0 is a label
df.iloc[0]    # If 0 is a position

# Avoid
df[0]         # Ambiguous
```

### 2. Avoid Mixed Indexing

```python
# Don't mix labels and positions
# Use loc for labels, iloc for positions
```

### 3. Check Index Type

```python
print(df.index)       # Understand your index
print(type(df.index)) # Know the index type
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with a string index. Use `.loc[]` to select a single row, a range of rows (slice), and specific rows and columns simultaneously.

??? success "Solution to Exercise 1"
    Use loc for label-based selection.

        import pandas as pd

        df = pd.DataFrame(
            {'A': [10, 20, 30, 40], 'B': [50, 60, 70, 80]},
            index=['w', 'x', 'y', 'z']
        )
        print("Single row:\n", df.loc['x'])
        print("\nSlice:\n", df.loc['x':'z'])
        print("\nRows and cols:\n", df.loc[['w', 'z'], ['A']])

---

**Exercise 2.**
Create a DataFrame with a default numeric index. Use `.iloc[]` to select the first 3 rows, every other row, and the last row. Verify each result.

??? success "Solution to Exercise 2"
    Use iloc for position-based selection.

        import pandas as pd

        df = pd.DataFrame({'val': [10, 20, 30, 40, 50]})
        print("First 3:\n", df.iloc[:3])
        print("\nEvery other:\n", df.iloc[::2])
        print("\nLast row:\n", df.iloc[-1])

---

**Exercise 3.**
Create a DataFrame and demonstrate the difference between `df['col']` (column access), `df.loc[row_label]` (row by label), and `df.iloc[row_pos]` (row by position). Show that `df.loc['label', 'col']` accesses a scalar value.

??? success "Solution to Exercise 3"
    Demonstrate different selection methods.

        import pandas as pd

        df = pd.DataFrame(
            {'price': [100, 200, 300], 'qty': [5, 3, 7]},
            index=['a', 'b', 'c']
        )
        print("Column:", type(df['price']))
        print("Row by label:", type(df.loc['a']))
        print("Row by position:", type(df.iloc[0]))
        print("Scalar:", df.loc['b', 'price'])
