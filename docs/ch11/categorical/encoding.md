# One-Hot Encoding with get_dummies

One-hot encoding converts categorical variables into binary columns, enabling their use in machine learning models that require numerical input.

!!! tip "Mental Model"
    One-hot encoding replaces a single column of labels with a row of binary flags -- one flag per unique label. If a column has values `[red, blue, green]`, it becomes three columns where exactly one is 1 and the rest are 0. This trades a compact representation for one that linear models can consume directly.

## pd.get_dummies Basics

### Basic Usage

```python
import pandas as pd

df = pd.DataFrame({
    'color': ['red', 'blue', 'green', 'red', 'blue'],
    'size': ['S', 'M', 'L', 'M', 'S'],
    'price': [10, 20, 30, 15, 25]
})

# Encode categorical columns
encoded = pd.get_dummies(df)
print(encoded)
```

```
   price  color_blue  color_green  color_red  size_L  size_M  size_S
0     10       False        False       True   False   False    True
1     20        True        False      False   False    True   False
2     30       False         True      False    True   False   False
3     15       False        False       True   False    True   False
4     25        True        False      False   False   False    True
```

### Encode Specific Columns

```python
# Only encode 'color' column
encoded = pd.get_dummies(df, columns=['color'])
print(encoded)
```

```
  size  price  color_blue  color_green  color_red
0    S     10       False        False       True
1    M     20        True        False      False
2    L     30       False         True      False
3    M     15       False        False       True
4    S     25        True        False      False
```

### Custom Prefix

```python
# Add custom prefix to encoded columns
encoded = pd.get_dummies(df, columns=['color'], prefix='c')
print(encoded.columns)
# Index(['size', 'price', 'c_blue', 'c_green', 'c_red'], dtype='object')

# Multiple columns with different prefixes
encoded = pd.get_dummies(
    df, 
    columns=['color', 'size'],
    prefix={'color': 'col', 'size': 'sz'}
)
print(encoded.columns)
```

## Handling Data Types

### dtype Parameter

```python
# Default: bool dtype (memory efficient)
encoded = pd.get_dummies(df['color'])
print(encoded.dtypes)

# Integer dtype for ML compatibility
encoded = pd.get_dummies(df['color'], dtype=int)
print(encoded.dtypes)

# Float dtype
encoded = pd.get_dummies(df['color'], dtype=float)
```

## Drop First (Dummy Variable Trap)

In regression models, including all dummy variables creates multicollinearity. Use `drop_first=True` to avoid this.

### The Problem

```python
# Full encoding: 3 columns for 3 colors
# red + blue + green always sums to 1 (perfect collinearity)
full = pd.get_dummies(df['color'])
print(full)
```

```
    blue  green   red
0  False  False  True
1   True  False  False
2  False   True  False
3  False  False  True
4   True  False  False
```

### The Solution

```python
# Drop first category: 2 columns sufficient
# If blue=0 and green=0, it's red
reduced = pd.get_dummies(df['color'], drop_first=True)
print(reduced)
```

```
   green   red
0  False  True
1  False  False
2   True  False
3  False  True
4  False  False
```

## Handling Missing Values

### Default Behavior

```python
df_missing = pd.DataFrame({
    'color': ['red', 'blue', None, 'red', pd.NA]
})

# NaN is not encoded by default
encoded = pd.get_dummies(df_missing['color'])
print(encoded)
```

```
    blue   red
0  False  True
1   True  False
2  False  False  # NaN row: all False
3  False  True
4  False  False  # NA row: all False
```

### Create NaN Indicator Column

```python
# Create column for missing values
encoded = pd.get_dummies(df_missing['color'], dummy_na=True)
print(encoded)
```

```
    blue   red   NaN
0  False  True  False
1   True  False  False
2  False  False  True
3  False  True  False
4  False  False  True
```

## Encoding Series vs DataFrame

### Series Encoding

```python
s = pd.Series(['A', 'B', 'A', 'C'])
encoded = pd.get_dummies(s)
print(encoded)
```

```
       A      B      C
0   True  False  False
1  False   True  False
2   True  False  False
3  False  False   True
```

### DataFrame Encoding

```python
# Encodes ALL object/category columns automatically
df = pd.DataFrame({
    'cat1': ['A', 'B', 'A'],
    'cat2': ['X', 'Y', 'X'],
    'num': [1, 2, 3]
})

encoded = pd.get_dummies(df)
print(encoded)
```

## Sparse Output

For datasets with many categories, use sparse matrices to save memory.

```python
# Dense (default)
encoded_dense = pd.get_dummies(df['color'])
print(f"Dense memory: {encoded_dense.memory_usage(deep=True).sum()} bytes")

# Sparse
encoded_sparse = pd.get_dummies(df['color'], sparse=True)
print(f"Sparse memory: {encoded_sparse.memory_usage(deep=True).sum()} bytes")
```

## Practical Examples

### 1. Preparing Data for Machine Learning

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Sample dataset
df = pd.DataFrame({
    'age': [25, 35, 45, 30, 50],
    'education': ['High School', 'Bachelor', 'Master', 'Bachelor', 'PhD'],
    'income_level': ['Low', 'Medium', 'High', 'Medium', 'High'],
    'purchased': [0, 1, 1, 0, 1]
})

# Encode categorical variables
X = pd.get_dummies(
    df[['age', 'education', 'income_level']], 
    drop_first=True,
    dtype=int
)
y = df['purchased']

# Train model
model = LogisticRegression()
model.fit(X, y)
print(f"Features: {list(X.columns)}")
```

### 2. Handling New Categories in Test Data

```python
# Training data
train = pd.DataFrame({'color': ['red', 'blue', 'green']})
train_encoded = pd.get_dummies(train['color'])

# Test data has new category 'yellow'
test = pd.DataFrame({'color': ['red', 'yellow', 'blue']})
test_encoded = pd.get_dummies(test['color'])

# Problem: different columns!
print(f"Train columns: {list(train_encoded.columns)}")
print(f"Test columns: {list(test_encoded.columns)}")

# Solution: reindex to match training columns
test_aligned = test_encoded.reindex(columns=train_encoded.columns, fill_value=0)
print(test_aligned)
```

### 3. Financial Sector Analysis

```python
import yfinance as yf

# Get S&P 500 sector data (simplified example)
portfolio = pd.DataFrame({
    'ticker': ['AAPL', 'JPM', 'JNJ', 'XOM', 'GOOGL'],
    'sector': ['Technology', 'Financial', 'Healthcare', 'Energy', 'Technology'],
    'weight': [0.25, 0.20, 0.20, 0.15, 0.20]
})

# Create sector exposure matrix
sector_exposure = pd.get_dummies(portfolio['sector'], dtype=float)

# Weight by portfolio allocation
weighted_exposure = sector_exposure.multiply(portfolio['weight'], axis=0)
print("Sector Exposure:")
print(weighted_exposure)
print("\nTotal Sector Allocation:")
print(weighted_exposure.sum())
```

### 4. Time-Based Categorical Features

```python
# Create time-based features
dates = pd.date_range('2024-01-01', periods=10, freq='D')
df = pd.DataFrame({'date': dates, 'value': range(10)})

df['day_of_week'] = df['date'].dt.day_name()
df['is_weekend'] = df['date'].dt.dayofweek >= 5

# Encode day of week
encoded = pd.get_dummies(df[['value', 'day_of_week', 'is_weekend']], 
                          columns=['day_of_week'],
                          drop_first=True)
print(encoded.head())
```

## Comparison: get_dummies vs sklearn

```python
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

df = pd.DataFrame({'color': ['red', 'blue', 'green', 'red']})

# pandas get_dummies
pd_encoded = pd.get_dummies(df['color'], dtype=int)

# sklearn OneHotEncoder
encoder = OneHotEncoder(sparse_output=False)
sk_encoded = encoder.fit_transform(df[['color']])
sk_df = pd.DataFrame(sk_encoded, columns=encoder.get_feature_names_out())
```

| Feature | pd.get_dummies | sklearn OneHotEncoder |
|---------|----------------|----------------------|
| Returns | DataFrame | NumPy array (default) |
| Handles new categories | No (must reindex) | Yes (with handle_unknown) |
| Fit/transform pattern | No | Yes |
| Column names | Automatic | Via get_feature_names_out() |
| Best for | Quick exploration | Production ML pipelines |

## Key Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `data` | Input DataFrame or Series | Required |
| `columns` | Columns to encode (DataFrame only) | None (all object/category) |
| `prefix` | String prefix for column names | None |
| `prefix_sep` | Separator between prefix and value | '_' |
| `drop_first` | Drop first category | False |
| `dummy_na` | Add NaN indicator column | False |
| `dtype` | Data type for encoded columns | bool |
| `sparse` | Return sparse DataFrame | False |

## Common Pitfalls

### 1. Not Handling Unseen Categories

```python
# Training
train_encoded = pd.get_dummies(train_df['category'])

# Test has new category - causes mismatch
test_encoded = pd.get_dummies(test_df['category'])

# Fix: align columns
test_aligned = test_encoded.reindex(columns=train_encoded.columns, fill_value=0)
```

### 2. Forgetting drop_first for Regression

```python
# For linear regression, ALWAYS use drop_first=True
X = pd.get_dummies(df[categorical_cols], drop_first=True)
```

### 3. Memory Issues with High Cardinality

```python
# Column with 10,000 unique values creates 10,000 columns!
# Consider: grouping rare categories, target encoding, or embeddings
df['category_grouped'] = df['category'].apply(
    lambda x: x if df['category'].value_counts()[x] > 100 else 'Other'
)
```


---

## Exercises

**Exercise 1.** Write code that converts a categorical column to dummy variables using `pd.get_dummies()`. Show the resulting DataFrame.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    # See page content for relevant API details
    s = pd.Series(['a', 'b', 'c', 'a', 'b'], dtype='category')
    print(s)
    print(s.cat.categories)
    print(s.cat.codes)
    ```

---

**Exercise 2.** Explain the difference between one-hot encoding and label encoding. Give an example of when each is appropriate.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page. The key concept involves understanding the categorical data type and its internal representation in Pandas.

---

**Exercise 3.** Write code that performs label encoding by using `.cat.codes` on a categorical Series. Print the codes alongside the original values.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd
    import numpy as np

    np.random.seed(42)
    df = pd.DataFrame({'col': np.random.choice(['A', 'B', 'C'], 1000)})
    df['col'] = df['col'].astype('category')
    print(df.dtypes)
    print(df['col'].value_counts())
    ```

---

**Exercise 4.** Create a DataFrame with a categorical column and use `pd.get_dummies(drop_first=True)` to avoid the dummy variable trap. Explain why `drop_first` is useful.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    s = pd.Categorical(['low', 'medium', 'high', 'low'],
                        categories=['low', 'medium', 'high'],
                        ordered=True)
    print(s)
    print(s > 'low')
    ```
