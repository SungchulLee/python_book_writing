# Value Counts and Unique

Methods for counting and identifying unique values are essential for data exploration and analysis. This document covers `value_counts()`, `nunique()`, and related methods.

!!! tip "Mental Model"
    `value_counts()` is a frequency table: it counts how many times each unique value appears and sorts by frequency. `nunique()` returns just the count of distinct values. Together they answer the two most basic questions about a categorical column: "what values exist?" and "how often does each appear?"

## value_counts()

Returns a Series containing counts of unique values, sorted by frequency.

### Basic Usage

```python
import pandas as pd

s = pd.Series(['a', 'b', 'a', 'c', 'a', 'b'])
print(s.value_counts())
```

```
a    3
b    2
c    1
Name: count, dtype: int64
```

### On DataFrame Columns

```python
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# Count passengers by class
print(df['Pclass'].value_counts())
```

```
3    491
1    216
2    184
Name: count, dtype: int64
```

### Parameters

#### normalize

Return proportions instead of counts.

```python
print(df['Pclass'].value_counts(normalize=True))
```

```
3    0.551066
1    0.242424
2    0.206510
Name: proportion, dtype: float64
```

#### sort

Control sorting behavior.

```python
# Sort by index instead of count
print(df['Pclass'].value_counts(sort=False))
```

```
1    216
2    184
3    491
Name: count, dtype: int64
```

#### ascending

```python
# Least frequent first
print(df['Pclass'].value_counts(ascending=True))
```

```
2    184
1    216
3    491
Name: count, dtype: int64
```

#### bins

Group numeric data into bins.

```python
# Bin ages into groups
print(df['Age'].value_counts(bins=5))
```

```
(16.336, 32.252]    346
(32.252, 48.168]    188
(0.339, 16.336]     100
(48.168, 64.084]     69
(64.084, 80.0]       11
Name: count, dtype: int64
```

#### dropna

Control whether to count NaN values.

```python
s = pd.Series([1, 2, 2, None, None, None])

# Default: exclude NaN
print(s.value_counts())
```

```
2.0    2
1.0    1
Name: count, dtype: int64
```

```python
# Include NaN in counts
print(s.value_counts(dropna=False))
```

```
NaN    3
2.0    2
1.0    1
Name: count, dtype: int64
```

## Practical Example: Manager Direct Reports

From LeetCode 570: Find managers with at least 5 direct reports.

```python
employee = pd.DataFrame({
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
    'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Helen', 'Ian'],
    'managerId': [2, None, 2, 2, 3, 2, 2, 2, 2]
})

# Count direct reports per manager
manager_counts = employee['managerId'].value_counts()
print(manager_counts)
```

```
2.0    7
3.0    1
Name: count, dtype: int64
```

```python
# Find managers with >= 5 direct reports
managers_with_5_plus = manager_counts[manager_counts >= 5].index
print(managers_with_5_plus)  # Index([2.0], dtype='float64')
```

## nunique()

Returns the number of unique values, excluding NaN by default.

### Basic Usage

```python
s = pd.Series([1, 2, 2, 3, 3, 3])
print(s.nunique())  # 3
```

### On DataFrame

```python
# Unique values per column
print(df.nunique())
```

```
PassengerId    891
Survived         2
Pclass           3
Name           891
Sex              2
Age             88
...
```

### Including NaN

```python
s = pd.Series([1, 2, None, None])

print(s.nunique())              # 2 (excludes NaN)
print(s.nunique(dropna=False))  # 3 (includes NaN as unique)
```

## Practical Example: Counting Unique Players

From LeetCode 550: Count unique players in activity data.

```python
activity = pd.DataFrame({
    'player_id': [1, 2, 1, 3, 2],
    'event_date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05']
})

# Count unique players
total_players = activity['player_id'].nunique()
print(f"Total unique players: {total_players}")  # 3
```

## unique()

Returns an array of unique values (not counts).

```python
s = pd.Series([3, 1, 2, 3, 1])
print(s.unique())  # array([3, 1, 2])
```

Note: Unlike `value_counts()`, `unique()` returns values in order of first appearance, not sorted.

### Sorted Unique Values

```python
# For sorted unique values
print(sorted(s.unique()))  # [1, 2, 3]

# Or use numpy
import numpy as np
print(np.sort(s.unique()))  # array([1, 2, 3])
```

## duplicated()

Returns a boolean Series indicating duplicate rows.

```python
s = pd.Series([1, 2, 2, 3, 3, 3])
print(s.duplicated())
```

```
0    False
1    False
2     True
3    False
4     True
5     True
dtype: bool
```

### Parameters

#### keep

- `'first'` (default): Mark duplicates except for the first occurrence
- `'last'`: Mark duplicates except for the last occurrence
- `False`: Mark all duplicates as True

```python
s = pd.Series([1, 2, 2, 3])

print(s.duplicated(keep='first'))  # [False, False, True, False]
print(s.duplicated(keep='last'))   # [False, True, False, False]
print(s.duplicated(keep=False))    # [False, True, True, False]
```

## DataFrame value_counts()

Count unique combinations of values across multiple columns.

```python
df = pd.DataFrame({
    'A': ['foo', 'foo', 'foo', 'bar', 'bar'],
    'B': ['one', 'one', 'two', 'two', 'one']
})

print(df.value_counts())
```

```
A    B  
foo  one    2
     two    1
bar  two    1
     one    1
Name: count, dtype: int64
```

### Reset Index for DataFrame Output

```python
# Convert to DataFrame
counts_df = df.value_counts().reset_index()
print(counts_df)
```

```
     A    B  count
0  foo  one      2
1  foo  two      1
2  bar  two      1
3  bar  one      1
```

## Practical Example: Finding Duplicate Emails

From LeetCode 182: Find duplicate emails.

```python
person = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'email': ['a@example.com', 'b@example.com', 'a@example.com', 
              'b@example.com', 'c@example.com']
})

# Method 1: Using value_counts
email_counts = person['email'].value_counts()
duplicates = email_counts[email_counts > 1].index.tolist()
print(duplicates)  # ['a@example.com', 'b@example.com']

# Method 2: Using groupby and count
email_counts = person.groupby('email')['id'].count().reset_index(name='count')
duplicates = email_counts[email_counts['count'] > 1]['email']
print(duplicates.tolist())  # ['a@example.com', 'b@example.com']
```

## Comparison Summary

| Method | Returns | Purpose |
|--------|---------|---------|
| `value_counts()` | Series | Count occurrences of each unique value |
| `nunique()` | int | Count of unique values |
| `unique()` | ndarray | Array of unique values |
| `duplicated()` | bool Series | Mark duplicate values |

## Financial Example: Sector Distribution

```python
# Portfolio holdings by sector
holdings = pd.DataFrame({
    'ticker': ['AAPL', 'MSFT', 'GOOGL', 'JPM', 'BAC', 'XOM', 'CVX'],
    'sector': ['Tech', 'Tech', 'Tech', 'Finance', 'Finance', 'Energy', 'Energy'],
    'weight': [0.20, 0.18, 0.15, 0.12, 0.10, 0.13, 0.12]
})

# Count holdings per sector
print(holdings['sector'].value_counts())
```

```
Tech       3
Finance    2
Energy     2
Name: count, dtype: int64
```

```python
# Sector concentration
print(holdings['sector'].value_counts(normalize=True))
```

```
Tech       0.428571
Finance    0.285714
Energy     0.285714
Name: proportion, dtype: float64
```

```python
# Number of sectors
print(f"Number of sectors: {holdings['sector'].nunique()}")  # 3
```

---

## Exercises

**Exercise 1.**
Create a Series of 50 random choices from `['red', 'blue', 'green']`. Use `.value_counts()` to count occurrences and `.value_counts(normalize=True)` to get the proportion of each color.

??? success "Solution to Exercise 1"
    Use value_counts with and without normalize.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        colors = pd.Series(np.random.choice(['red', 'blue', 'green'], 50))
        print("Counts:")
        print(colors.value_counts())
        print("\nProportions:")
        print(colors.value_counts(normalize=True))

---

**Exercise 2.**
Given a DataFrame with a numeric `'score'` column, use `.value_counts(bins=5)` to group scores into 5 bins. Then use `.nunique()` to count the number of distinct scores.

??? success "Solution to Exercise 2"
    Use bins parameter and nunique.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        df = pd.DataFrame({'score': np.random.randint(0, 101, 100)})
        print("Binned counts:")
        print(df['score'].value_counts(bins=5))
        print(f"\nUnique scores: {df['score'].nunique()}")

---

**Exercise 3.**
Create a DataFrame with duplicate rows. Use `.duplicated()` to identify them, `.duplicated(keep=False)` to mark all duplicates, and then use `value_counts()` on a column to find which values appear more than once.

??? success "Solution to Exercise 3"
    Identify duplicates using duplicated and value_counts.

        import pandas as pd

        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Alice', 'Carol', 'Bob'],
            'dept': ['HR', 'IT', 'HR', 'IT', 'IT']
        })
        print("Duplicated (keep first):")
        print(df.duplicated())
        print("\nAll duplicates:")
        print(df.duplicated(keep=False))
        print("\nValues appearing more than once:")
        counts = df['name'].value_counts()
        print(counts[counts > 1])
