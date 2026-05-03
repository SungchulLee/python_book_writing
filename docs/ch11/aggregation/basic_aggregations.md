# Basic Aggregations

Aggregation functions summarize data by computing statistics like sum, mean, and count. They reduce multiple values to a single result.

!!! tip "Mental Model"
    An aggregation collapses many values into one -- a column of 1000 numbers becomes a single mean, sum, or count. Picture a funnel: data flows in at the top, and a single summary number comes out at the bottom. Every built-in aggregation method (`mean`, `sum`, `std`, ...) is just a different funnel shape.

## Column Aggregations

Apply aggregations to DataFrame columns.

### 1. Single Column Mean

```python
import pandas as pd

df = pd.DataFrame({
    'Age': [25, 30, 35, 40],
    'Salary': [50000, 60000, 70000, 80000]
})

print(df['Age'].mean())  # 32.5
```

### 2. Single Column Sum

```python
print(df['Salary'].sum())  # 260000
```

### 3. Multiple Aggregations

```python
print(df['Age'].min())    # 25
print(df['Age'].max())    # 40
print(df['Age'].std())    # 6.45
print(df['Age'].count())  # 4
```

## DataFrame Aggregations

Apply aggregations across the entire DataFrame.

### 1. All Columns Mean

```python
print(df.mean())
```

```
Age          32.5
Salary    65000.0
dtype: float64
```

### 2. All Columns Sum

```python
print(df.sum())
```

### 3. Summary Statistics

```python
print(df.describe())
```

```
             Age        Salary
count   4.000000      4.000000
mean   32.500000  65000.000000
std     6.454972  12909.944487
min    25.000000  50000.000000
25%    28.750000  57500.000000
50%    32.500000  65000.000000
75%    36.250000  72500.000000
max    40.000000  80000.000000
```

## Common Aggregation Methods

Methods available on Series and DataFrame.

### 1. Central Tendency

```python
df['Age'].mean()    # Arithmetic mean
df['Age'].median()  # Middle value
df['Age'].mode()    # Most frequent value
```

### 2. Dispersion

```python
df['Age'].std()     # Standard deviation
df['Age'].var()     # Variance
df['Age'].sem()     # Standard error of mean
```

### 3. Quantiles

```python
df['Age'].quantile(0.25)       # First quartile
df['Age'].quantile([0.25, 0.75])  # Multiple quantiles
```

## Numeric Only Aggregations

Handle mixed data types.

### 1. numeric_only Parameter

```python
df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30],
    'Salary': [50000, 60000]
})

df.mean(numeric_only=True)  # Exclude 'Name'
```

### 2. Select Numeric Columns

```python
df.select_dtypes(include='number').mean()
```

### 3. Specific Columns

```python
df[['Age', 'Salary']].mean()
```

## Axis Parameter

Aggregate along rows or columns.

### 1. axis=0 (Default)

```python
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': [4, 5, 6]
})

df.sum(axis=0)  # Sum each column
```

```
A     6
B    15
dtype: int64
```

### 2. axis=1

```python
df.sum(axis=1)  # Sum each row
```

```
0    5
1    7
2    9
dtype: int64
```

### 3. Row Mean

```python
df['RowMean'] = df.mean(axis=1)
```

## Handling Missing Values

Aggregation methods handle NaN by default.

### 1. skipna=True (Default)

```python
import numpy as np

s = pd.Series([1, 2, np.nan, 4])
s.mean()  # 2.333... (ignores NaN)
```

### 2. skipna=False

```python
s.mean(skipna=False)  # NaN (includes NaN)
```

### 3. Count Non-NaN

```python
s.count()  # 3 (only non-NaN values)
len(s)     # 4 (all values including NaN)
```

---

## Exercises

**Exercise 1.**
Create a DataFrame with columns `'math'`, `'science'`, and `'english'` containing scores for five students. Use `.mean()` to compute the average score for each subject (column-wise) and for each student (row-wise with `axis=1`).

??? success "Solution to Exercise 1"
    Use `.mean()` with different axis values.

        import pandas as pd

        df = pd.DataFrame({
            'math': [85, 90, 78, 92, 88],
            'science': [80, 85, 82, 95, 90],
            'english': [75, 88, 91, 84, 79]
        })
        print("Average per subject:\n", df.mean())
        print("\nAverage per student:\n", df.mean(axis=1))

---

**Exercise 2.**
Given a DataFrame of daily stock prices for three tickers, compute the `describe()` statistics. Then extract only the `'mean'` and `'std'` rows from the result using `.loc`.

??? success "Solution to Exercise 2"
    Use `describe()` and extract specific rows with `.loc`.

        import pandas as pd
        import numpy as np

        np.random.seed(42)
        df = pd.DataFrame({
            'AAPL': np.random.uniform(140, 160, 20),
            'MSFT': np.random.uniform(340, 360, 20),
            'GOOGL': np.random.uniform(130, 150, 20)
        })
        stats = df.describe()
        print(stats.loc[['mean', 'std']])

---

**Exercise 3.**
Create a Series with some `NaN` values. Demonstrate the difference between `.count()` and `len()` by printing both. Then compute the `.sum()` and show that NaN values are skipped by default but can be included by setting `min_count`.

??? success "Solution to Exercise 3"
    Show the difference between `count()` and `len()`.

        import pandas as pd
        import numpy as np

        s = pd.Series([10, 20, np.nan, 40, np.nan])
        print(f"count(): {s.count()}")  # 3
        print(f"len(): {len(s)}")       # 5
        print(f"sum(): {s.sum()}")      # 70 (NaN skipped)
