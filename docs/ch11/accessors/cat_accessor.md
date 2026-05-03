# Categorical Accessor (cat)

The `cat` accessor in pandas provides methods and properties for working with categorical data. It allows you to inspect, modify, and manipulate the categories of a Categorical Series.

!!! tip "Mental Model"
    Think of `.cat` as a control panel attached to any categorical Series. Just as a TV remote only works with a TV, `.cat` only activates on categorical dtype -- but once you have it, you can rename, reorder, add, or remove the category labels that define the column's vocabulary.

## Overview

```python
import pandas as pd

s = pd.Series(['low', 'medium', 'high', 'low'], dtype='category')

# Access categorical methods via .cat accessor
print(s.cat.categories)
```

```
Index(['high', 'low', 'medium'], dtype='object')
```

## Prerequisites

The `cat` accessor only works with categorical dtype:

```python
# String column - cat accessor NOT available
s = pd.Series(['a', 'b', 'c'])
# s.cat.categories  # AttributeError

# Convert to categorical first
s = s.astype('category')
print(s.cat.categories)  # Now works
```

## Properties

### categories

Returns the categories of the categorical.

```python
s = pd.Series(['apple', 'banana', 'apple', 'cherry'], dtype='category')
print(s.cat.categories)
```

```
Index(['apple', 'banana', 'cherry'], dtype='object')
```

### codes

Returns the integer codes representing each category.

```python
s = pd.Series(['apple', 'banana', 'apple', 'cherry'], dtype='category')
print(s.cat.codes)
```

```
0    0
1    1
2    0
3    2
dtype: int8
```

The codes are integers that index into the categories array. This is how categorical data achieves memory efficiency.

### ordered

Returns whether the categorical has an order.

```python
s = pd.Series(['low', 'medium', 'high'], dtype='category')
print(s.cat.ordered)  # False

# Create ordered categorical
s_ordered = pd.Categorical(['low', 'medium', 'high'], 
                           categories=['low', 'medium', 'high'],
                           ordered=True)
print(pd.Series(s_ordered).cat.ordered)  # True
```

## Category Management Methods

### add_categories()

Add new categories.

```python
s = pd.Series(['a', 'b', 'a'], dtype='category')
print(s.cat.categories)  # ['a', 'b']

s = s.cat.add_categories(['c', 'd'])
print(s.cat.categories)  # ['a', 'b', 'c', 'd']
```

Note: Adding categories doesn't add data values—it just expands the allowed categories.

### remove_categories()

Remove categories (values become NaN).

```python
s = pd.Series(['a', 'b', 'c', 'a'], dtype='category')
s = s.cat.remove_categories(['c'])
print(s)
```

```
0      a
1      b
2    NaN
3      a
dtype: category
Categories (2, object): ['a', 'b']
```

⚠️ **Warning**: Removing a category doesn't remove rows—it converts those values to NaN.

### remove_unused_categories()

Remove categories that don't appear in the data.

```python
s = pd.Series(['a', 'b', 'a'], dtype='category')
s = s.cat.add_categories(['c', 'd'])  # Add unused categories
print(s.cat.categories)  # ['a', 'b', 'c', 'd']

s = s.cat.remove_unused_categories()
print(s.cat.categories)  # ['a', 'b']
```

### set_categories()

Set categories to a new list (replaces all).

```python
s = pd.Series(['a', 'b', 'c'], dtype='category')
s = s.cat.set_categories(['a', 'b', 'c', 'd', 'e'])
print(s.cat.categories)
```

```
Index(['a', 'b', 'c', 'd', 'e'], dtype='object')
```

### rename_categories()

Rename existing categories.

```python
s = pd.Series(['a', 'b', 'c', 'a'], dtype='category')

# Using a dictionary
s = s.cat.rename_categories({'a': 'alpha', 'b': 'beta', 'c': 'gamma'})
print(s)
```

```
0    alpha
1     beta
2    gamma
3    alpha
dtype: category
Categories (3, object): ['alpha', 'beta', 'gamma']
```

```python
# Using a function
s = pd.Series(['a', 'b', 'c'], dtype='category')
s = s.cat.rename_categories(lambda x: x.upper())
print(s.cat.categories)  # ['A', 'B', 'C']
```

### reorder_categories()

Reorder categories (for ordered categoricals).

```python
s = pd.Series(['low', 'medium', 'high'], dtype='category')
s = s.cat.reorder_categories(['low', 'medium', 'high'], ordered=True)
print(s.cat.categories)
```

```
Index(['low', 'medium', 'high'], dtype='object')
```

## Ordering Methods

### as_ordered()

Make the categorical ordered.

```python
s = pd.Series(['low', 'medium', 'high'], dtype='category')
print(s.cat.ordered)  # False

s = s.cat.as_ordered()
print(s.cat.ordered)  # True
```

### as_unordered()

Make the categorical unordered.

```python
s = s.cat.as_unordered()
print(s.cat.ordered)  # False
```

## Practical Examples

### Stock Sector Analysis

```python
import pandas as pd
import numpy as np

# Create stock data
np.random.seed(42)
sectors = ['Technology', 'Finance', 'Healthcare', 'Energy', 'Consumer']
df = pd.DataFrame({
    'ticker': [f'STOCK_{i}' for i in range(1000)],
    'sector': np.random.choice(sectors, 1000),
    'returns': np.random.randn(1000) * 0.02
})

# Convert to categorical
df['sector'] = df['sector'].astype('category')

# Check categories
print(df['sector'].cat.categories)

# Reorder for logical grouping
df['sector'] = df['sector'].cat.reorder_categories(
    ['Technology', 'Healthcare', 'Finance', 'Consumer', 'Energy']
)

# Group analysis is now faster
sector_returns = df.groupby('sector')['returns'].mean()
print(sector_returns)
```

### Credit Rating Analysis

```python
# Credit ratings have natural order
ratings = pd.Series(['BBB', 'AA', 'AAA', 'BB', 'A', 'BBB', 'AA'])

# Convert to ordered categorical
rating_order = ['BB', 'BBB', 'A', 'AA', 'AAA']
ratings = pd.Categorical(ratings, categories=rating_order, ordered=True)
ratings = pd.Series(ratings)

# Now comparisons work
print(ratings > 'BBB')
```

```
0    False
1     True
2     True
3    False
4     True
5    False
6     True
dtype: bool
```

```python
# Filter investment grade (BBB and above)
investment_grade = ratings[ratings >= 'BBB']
print(investment_grade)
```

### Survey Response Analysis

```python
# Survey responses with natural order
responses = pd.Series([
    'Strongly Disagree', 'Disagree', 'Neutral', 
    'Agree', 'Strongly Agree', 'Agree', 'Neutral'
])

# Define order
response_order = [
    'Strongly Disagree', 'Disagree', 'Neutral', 
    'Agree', 'Strongly Agree'
]

responses = pd.Categorical(responses, categories=response_order, ordered=True)
responses = pd.Series(responses)

# Find positive responses
positive = responses[responses > 'Neutral']
print(positive)
```

## Memory Comparison

```python
import pandas as pd
import numpy as np

# Create large dataset
n = 1_000_000
categories = ['Cat_A', 'Cat_B', 'Cat_C', 'Cat_D', 'Cat_E']
data = np.random.choice(categories, n)

# As string (object)
s_string = pd.Series(data)
print(f"String memory: {s_string.memory_usage(deep=True) / 1e6:.2f} MB")

# As categorical
s_cat = pd.Series(data, dtype='category')
print(f"Categorical memory: {s_cat.memory_usage(deep=True) / 1e6:.2f} MB")

# Ratio
ratio = s_string.memory_usage(deep=True) / s_cat.memory_usage(deep=True)
print(f"Memory reduction: {ratio:.1f}x")
```

```
String memory: 57.00 MB
Categorical memory: 1.00 MB
Memory reduction: 57.0x
```

## Summary of cat Methods

| Method/Property | Description |
|----------------|-------------|
| `cat.categories` | Get/set categories |
| `cat.codes` | Integer codes for values |
| `cat.ordered` | Check if ordered |
| `cat.add_categories()` | Add new categories |
| `cat.remove_categories()` | Remove categories |
| `cat.remove_unused_categories()` | Remove unused categories |
| `cat.set_categories()` | Replace all categories |
| `cat.rename_categories()` | Rename categories |
| `cat.reorder_categories()` | Reorder categories |
| `cat.as_ordered()` | Make ordered |
| `cat.as_unordered()` | Make unordered |

---

## Exercises

**Exercise 1.**
Create a Series with values `['small', 'medium', 'large', 'medium', 'small']` and convert it to a categorical type. Use `.cat.codes` to print the integer codes and `.cat.categories` to print the category labels.

??? success "Solution to Exercise 1"
    Convert to categorical and inspect codes and categories.

        import pandas as pd

        s = pd.Series(['small', 'medium', 'large', 'medium', 'small'], dtype='category')
        print("Codes:", s.cat.codes.tolist())
        print("Categories:", s.cat.categories.tolist())

---

**Exercise 2.**
Create an ordered categorical Series with the custom order `['bronze', 'silver', 'gold']`. Add a new category `'platinum'` using `.cat.add_categories()`. Then verify that `'platinum'` appears in the categories even though no element has that value.

??? success "Solution to Exercise 2"
    Create ordered categorical and add a new category.

        import pandas as pd
        from pandas.api.types import CategoricalDtype

        cat_type = CategoricalDtype(
            categories=['bronze', 'silver', 'gold'],
            ordered=True
        )
        s = pd.Series(['bronze', 'silver', 'gold', 'silver'], dtype=cat_type)
        s = s.cat.add_categories('platinum')
        print(s.cat.categories)  # ['bronze', 'silver', 'gold', 'platinum']
        print('platinum' in s.cat.categories)  # True

---

**Exercise 3.**
Given a categorical Series with categories `['A', 'B', 'C', 'D']` where category `'D'` is never used, use `.cat.remove_unused_categories()` to clean it up. Then rename the remaining categories to `['Alpha', 'Beta', 'Gamma']` using `.cat.rename_categories()`.

??? success "Solution to Exercise 3"
    Remove unused categories and rename the rest.

        import pandas as pd

        s = pd.Series(
            pd.Categorical(['A', 'B', 'C', 'A', 'B'],
                           categories=['A', 'B', 'C', 'D'])
        )
        s = s.cat.remove_unused_categories()
        print("After removing unused:", s.cat.categories.tolist())  # ['A', 'B', 'C']
        s = s.cat.rename_categories({'A': 'Alpha', 'B': 'Beta', 'C': 'Gamma'})
        print(s)
