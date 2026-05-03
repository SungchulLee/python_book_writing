# Binning with cut and qcut

Binning (discretization) converts continuous data into discrete categories. pandas provides two primary functions: `pd.cut()` for equal-width bins and `pd.qcut()` for equal-frequency bins.

!!! tip "Mental Model"
    Imagine a number line chopped into buckets. `cut` chops by equal width (every bucket spans the same range), while `qcut` chops by equal count (every bucket holds roughly the same number of data points). Choose `cut` when the bin boundaries matter, and `qcut` when balanced group sizes matter.

## pd.cut - Equal-Width Bins

Divides data into bins of equal width (range).

### Basic Usage

```python
import pandas as pd
import numpy as np

ages = pd.Series([22, 35, 45, 28, 65, 52, 19, 38, 72, 33])

# Create 3 equal-width bins
binned = pd.cut(ages, bins=3)
print(binned)
```

```
0    (18.947, 36.667]
1    (18.947, 36.667]
2     (36.667, 54.333]
3    (18.947, 36.667]
4      (54.333, 72.0]
5     (36.667, 54.333]
6    (18.947, 36.667]
7     (36.667, 54.333]
8      (54.333, 72.0]
9    (18.947, 36.667]
dtype: category
Categories (3, interval[float64, right]): [(18.947, 36.667] < (36.667, 54.333] < (54.333, 72.0]]
```

### Custom Bin Edges

```python
# Define explicit bin boundaries
bins = [0, 18, 35, 50, 65, 100]
labels = ['Child', 'Young Adult', 'Middle Age', 'Senior', 'Elderly']

age_groups = pd.cut(ages, bins=bins, labels=labels)
print(age_groups)
```

```
0    Young Adult
1    Young Adult
2     Middle Age
3    Young Adult
4         Senior
5     Middle Age
6          Child
7     Middle Age
8        Elderly
9    Young Adult
dtype: category
Categories (5, object): ['Child' < 'Young Adult' < 'Middle Age' < 'Senior' < 'Elderly']
```

### Include Lowest Value

By default, the leftmost bin edge is exclusive. Use `include_lowest=True` to include it.

```python
values = pd.Series([0, 10, 20, 30])
bins = [0, 10, 20, 30]

# Without include_lowest: 0 becomes NaN
print(pd.cut(values, bins=bins))

# With include_lowest: 0 is included
print(pd.cut(values, bins=bins, include_lowest=True))
```

### Right vs Left Closed

```python
values = pd.Series([1, 5, 10, 15, 20])
bins = [0, 10, 20]

# right=True (default): intervals are (a, b]
print(pd.cut(values, bins=bins, right=True))
# 10 goes into (0, 10], 20 goes into (10, 20]

# right=False: intervals are [a, b)
print(pd.cut(values, bins=bins, right=False))
# 10 goes into [10, 20), 20 becomes NaN
```

### Return Bin Information

```python
ages = pd.Series([22, 35, 45, 28, 65, 52])

# Get bins and bin edges
binned, bin_edges = pd.cut(ages, bins=3, retbins=True)
print(f"Bin edges: {bin_edges}")
```

```
Bin edges: [21.957 36.333 50.667 65.   ]
```

## pd.qcut - Quantile-Based Bins

Divides data into bins with approximately equal numbers of observations.

### Basic Usage

```python
# Highly skewed data
salaries = pd.Series([30000, 35000, 40000, 45000, 50000, 
                      100000, 150000, 200000, 500000, 1000000])

# Equal-width bins (pd.cut) - most values in one bin
print("cut (equal-width):")
print(pd.cut(salaries, bins=4).value_counts())

# Equal-frequency bins (pd.qcut) - same count per bin
print("\nqcut (equal-frequency):")
print(pd.qcut(salaries, q=4).value_counts())
```

```
cut (equal-width):
(29030.0, 272500.0]      8
(272500.0, 515000.0]     1
(515000.0, 757500.0]     0
(757500.0, 1000000.0]    1
dtype: int64

qcut (equal-frequency):
(29999.999, 42500.0]     3
(42500.0, 75000.0]       2
(75000.0, 175000.0]      3
(175000.0, 1000000.0]    2
dtype: int64
```

### Custom Quantiles

```python
# Create quartiles
quartiles = pd.qcut(salaries, q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
print(quartiles)

# Custom percentiles
percentiles = pd.qcut(salaries, q=[0, 0.25, 0.5, 0.75, 0.9, 1.0],
                      labels=['Bottom 25%', '25-50%', '50-75%', '75-90%', 'Top 10%'])
print(percentiles)
```

### Handling Duplicates

When data has many duplicate values, qcut may fail because it can't create distinct bins.

```python
# Data with many duplicates
values = pd.Series([1, 1, 1, 2, 2, 2, 3, 3, 3])

# This will raise an error
# pd.qcut(values, q=4)  # ValueError: Bin edges must be unique

# Solution 1: Use duplicates='drop'
print(pd.qcut(values, q=4, duplicates='drop'))

# Solution 2: Use pd.cut instead
print(pd.cut(values, bins=4))
```

## cut vs qcut Comparison

```python
# Normally distributed data
np.random.seed(42)
normal_data = pd.Series(np.random.randn(1000) * 10 + 50)

# Skewed data
skewed_data = pd.Series(np.random.exponential(scale=10, size=1000))

print("=== Normal Data ===")
print("cut bins:", pd.cut(normal_data, bins=5).value_counts().sort_index())
print("qcut bins:", pd.qcut(normal_data, q=5).value_counts().sort_index())

print("\n=== Skewed Data ===")
print("cut bins:", pd.cut(skewed_data, bins=5).value_counts().sort_index())
print("qcut bins:", pd.qcut(skewed_data, q=5).value_counts().sort_index())
```

| Scenario | Use `cut` | Use `qcut` |
|----------|-----------|------------|
| Equal-width ranges needed | ✅ | |
| Equal sample sizes per bin | | ✅ |
| Predefined boundaries | ✅ | |
| Percentile-based analysis | | ✅ |
| Skewed distributions | | ✅ (usually) |
| Custom business rules | ✅ | |

## Practical Examples

### 1. Customer Segmentation by Spending

```python
# Customer purchase data
customers = pd.DataFrame({
    'customer_id': range(1, 101),
    'total_spend': np.random.exponential(scale=500, size=100)
})

# Segment into spending tiers using qcut (equal customer count)
customers['spend_tier'] = pd.qcut(
    customers['total_spend'], 
    q=4, 
    labels=['Bronze', 'Silver', 'Gold', 'Platinum']
)

# Check distribution
print(customers['spend_tier'].value_counts())
print(customers.groupby('spend_tier')['total_spend'].agg(['min', 'max', 'mean']))
```

### 2. Grade Assignment

```python
# Student scores
scores = pd.Series([95, 87, 76, 65, 58, 92, 73, 81, 45, 88])

# Fixed grade boundaries
bins = [0, 60, 70, 80, 90, 100]
labels = ['F', 'D', 'C', 'B', 'A']

grades = pd.cut(scores, bins=bins, labels=labels, right=False)
print(grades)
```

### 3. Age Groups for Analysis

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Carol', 'David', 'Eve'],
    'age': [25, 35, 45, 55, 65],
    'income': [50000, 75000, 90000, 120000, 80000]
})

# Create age groups
df['age_group'] = pd.cut(
    df['age'], 
    bins=[18, 30, 45, 60, 100],
    labels=['Young', 'Middle', 'Senior', 'Retired']
)

# Analyze income by age group
print(df.groupby('age_group')['income'].mean())
```

### 4. Stock Price Volatility Buckets

```python
import yfinance as yf

# Get stock data
stock = yf.Ticker('AAPL').history(period='1y')
stock['daily_return'] = stock['Close'].pct_change()

# Bin returns into volatility categories
stock['return_category'] = pd.cut(
    stock['daily_return'],
    bins=[-np.inf, -0.02, -0.01, 0, 0.01, 0.02, np.inf],
    labels=['Large Loss', 'Loss', 'Slight Loss', 'Slight Gain', 'Gain', 'Large Gain']
)

print(stock['return_category'].value_counts())
```

## Key Parameters Summary

### pd.cut Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `x` | Input array to bin | Required |
| `bins` | Number of bins or bin edges | Required |
| `labels` | Labels for bins | None (interval notation) |
| `right` | Include right edge | True |
| `include_lowest` | Include lowest edge | False |
| `retbins` | Return bin edges | False |
| `precision` | Decimal precision | 3 |

### pd.qcut Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `x` | Input array to bin | Required |
| `q` | Number of quantiles or quantile edges | Required |
| `labels` | Labels for bins | None |
| `retbins` | Return bin edges | False |
| `precision` | Decimal precision | 3 |
| `duplicates` | Handle duplicate edges | 'raise' |

## Common Pitfalls

### 1. NaN Values in Input

```python
values = pd.Series([1, 2, np.nan, 4, 5])
binned = pd.cut(values, bins=3)
print(binned)  # NaN remains NaN
```

### 2. Out-of-Range Values

```python
values = pd.Series([5, 15, 25, 35])
bins = [10, 20, 30]

result = pd.cut(values, bins=bins)
print(result)
# 5 and 35 become NaN (outside bin range)
```

### 3. Too Few Unique Values for qcut

```python
# When data has fewer unique values than requested quantiles
values = pd.Series([1, 1, 2, 2])
# pd.qcut(values, q=4)  # Error!
pd.qcut(values, q=4, duplicates='drop')  # Works
```


---

## Exercises

**Exercise 1.** Write code that uses `pd.cut()` to bin a list of ages `[5, 15, 25, 35, 45, 55, 65, 75]` into categories: `'Child'`, `'Young Adult'`, `'Adult'`, `'Senior'` with boundaries `[0, 18, 35, 60, 100]`.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    ages = [5, 15, 25, 35, 45, 55, 65, 75]
    bins = [0, 18, 35, 60, 100]
    labels = ['Child', 'Young Adult', 'Adult', 'Senior']
    categories = pd.cut(ages, bins=bins, labels=labels)
    print(categories)
    print(categories.value_counts())
    ```

---

**Exercise 2.** Explain the difference between `pd.cut()` and `pd.qcut()`. When would you use each?

??? success "Solution to Exercise 2"
    `pd.cut()` bins data into intervals of equal **width** (or custom boundaries). `pd.qcut()` bins data into intervals of equal **frequency** (each bin has approximately the same number of observations). Use `cut()` when you have meaningful boundary values (e.g., age groups). Use `qcut()` when you want to split data into quantiles (e.g., quartiles, deciles).

---

**Exercise 3.** Write code that uses `pd.qcut()` to divide 100 random values into 4 equal-frequency bins. Print the value counts of each bin.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    values = np.random.randn(100)
    quartiles = pd.qcut(values, q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    print(quartiles.value_counts())
    ```

---

**Exercise 4.** Create a DataFrame with a `'score'` column of random integers from 0 to 100. Use `pd.cut()` to add a `'grade'` column with categories A (90-100), B (80-89), C (70-79), D (60-69), F (0-59).

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'score': np.random.randint(0, 101, 50)})
    bins = [0, 60, 70, 80, 90, 101]
    labels = ['F', 'D', 'C', 'B', 'A']
    df['grade'] = pd.cut(df['score'], bins=bins, labels=labels, right=False)
    print(df.head(10))
    print(df['grade'].value_counts())
    ```
