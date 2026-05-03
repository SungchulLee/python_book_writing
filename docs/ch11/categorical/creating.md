# Creating Categoricals

There are several ways to create categorical data in pandas, from simple type conversion to explicit construction with custom categories and ordering.

!!! tip "Mental Model"
    Creating a categorical is like defining an enum: you declare the allowed values (categories) and then each element is just a pointer into that list. The simplest path is `astype('category')` which infers the categories from the data, but `CategoricalDtype` gives you full control over which values are allowed and their order.

## Method 1: Using astype('category')

The simplest way to convert existing data to categorical.

```python
import pandas as pd

# From a Series
s = pd.Series(['apple', 'banana', 'apple', 'cherry'])
s_cat = s.astype('category')
print(s_cat)
```

```
0     apple
1    banana
2     apple
3    cherry
dtype: category
Categories (3, object): ['apple', 'banana', 'cherry']
```

```python
# From a DataFrame column
df = pd.DataFrame({
    'product': ['A', 'B', 'A', 'C', 'B'],
    'price': [100, 200, 100, 300, 200]
})

df['product'] = df['product'].astype('category')
print(df['product'].dtype)  # category
```

### Categories are Automatically Inferred

When using `astype('category')`, pandas automatically:
- Identifies unique values
- Creates categories in sorted order (alphabetical for strings)
- Assigns integer codes to each value

```python
s = pd.Series(['zebra', 'apple', 'mango', 'apple'])
s_cat = s.astype('category')
print(s_cat.cat.categories)  # ['apple', 'mango', 'zebra'] (sorted)
```

## Method 2: Using pd.Categorical()

For explicit control over categories and ordering.

### Basic Construction

```python
cat = pd.Categorical(['a', 'b', 'c', 'a', 'b'])
print(cat)
```

```
['a', 'b', 'c', 'a', 'b']
Categories (3, object): ['a', 'b', 'c']
```

### Specifying Categories

Define the allowed categories explicitly:

```python
# Only these categories are valid
cat = pd.Categorical(
    ['small', 'medium', 'large', 'small'],
    categories=['small', 'medium', 'large', 'extra-large']
)
print(cat)
```

```
['small', 'medium', 'large', 'small']
Categories (4, object): ['small', 'medium', 'large', 'extra-large']
```

Note: 'extra-large' is a valid category even though it doesn't appear in the data.

### Ordered Categories

Create categories with logical ordering:

```python
cat = pd.Categorical(
    ['medium', 'small', 'large', 'small'],
    categories=['small', 'medium', 'large'],
    ordered=True
)
print(cat)
```

```
['medium', 'small', 'large', 'small']
Categories (3, object): ['small' < 'medium' < 'large']
```

The `<` symbols indicate ordering.

### Handling Invalid Values

Values not in categories become NaN:

```python
cat = pd.Categorical(
    ['a', 'b', 'c', 'd'],  # 'd' not in categories
    categories=['a', 'b', 'c']
)
print(cat)
```

```
['a', 'b', 'c', NaN]
Categories (3, object): ['a', 'b', 'c']
```

## Method 3: Using pd.CategoricalDtype

Define a categorical type for reuse across multiple columns.

```python
# Define the dtype once
size_dtype = pd.CategoricalDtype(
    categories=['S', 'M', 'L', 'XL'],
    ordered=True
)

# Apply to multiple columns
df = pd.DataFrame({
    'shirt_size': ['M', 'L', 'S', 'XL'],
    'pants_size': ['L', 'M', 'M', 'L']
})

df['shirt_size'] = df['shirt_size'].astype(size_dtype)
df['pants_size'] = df['pants_size'].astype(size_dtype)

print(df.dtypes)
```

```
shirt_size    category
pants_size    category
dtype: object
```

### CategoricalDtype with read_csv

```python
# Define dtype before reading
rating_dtype = pd.CategoricalDtype(
    categories=['AAA', 'AA', 'A', 'BBB', 'BB', 'B'],
    ordered=True
)

# Apply during read
df = pd.read_csv('bonds.csv', dtype={'rating': rating_dtype})
```

## Method 4: During DataFrame Creation

Specify categorical dtype when creating a DataFrame:

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'grade': pd.Categorical(['A', 'B', 'A'], ordered=True)
})

print(df['grade'].dtype)  # category
```

## Method 5: Using Series Constructor

```python
s = pd.Series(
    pd.Categorical(['low', 'medium', 'high', 'low']),
    name='priority'
)
print(s)
```

## Practical Examples

### Stock Sectors

```python
import numpy as np

# Define valid sectors
sector_dtype = pd.CategoricalDtype(categories=[
    'Technology', 'Healthcare', 'Finance', 'Energy',
    'Consumer Discretionary', 'Consumer Staples',
    'Industrials', 'Materials', 'Utilities',
    'Real Estate', 'Communication Services'
])

# Create stock data
stocks = pd.DataFrame({
    'ticker': ['AAPL', 'JNJ', 'JPM', 'XOM', 'AMZN'],
    'sector': ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer Discretionary']
})

stocks['sector'] = stocks['sector'].astype(sector_dtype)
print(stocks['sector'].cat.categories)
```

### Credit Ratings

```python
# Ratings with natural order (AAA is best)
rating_dtype = pd.CategoricalDtype(
    categories=['D', 'C', 'CC', 'CCC', 'B', 'BB', 'BBB', 'A', 'AA', 'AAA'],
    ordered=True
)

bonds = pd.DataFrame({
    'issuer': ['Company A', 'Company B', 'Company C'],
    'rating': ['AA', 'BBB', 'A']
})

bonds['rating'] = bonds['rating'].astype(rating_dtype)

# Now we can compare ratings
print(bonds[bonds['rating'] >= 'A'])  # Investment grade
```

### Survey Responses

```python
# Likert scale with order
likert_dtype = pd.CategoricalDtype(
    categories=[
        'Strongly Disagree',
        'Disagree', 
        'Neutral',
        'Agree',
        'Strongly Agree'
    ],
    ordered=True
)

survey = pd.DataFrame({
    'respondent_id': [1, 2, 3, 4, 5],
    'satisfaction': ['Agree', 'Neutral', 'Strongly Agree', 'Disagree', 'Agree']
})

survey['satisfaction'] = survey['satisfaction'].astype(likert_dtype)

# Find positive responses
positive = survey[survey['satisfaction'] > 'Neutral']
print(positive)
```

## Summary of Creation Methods

| Method | Use Case | Example |
|--------|----------|---------|
| `astype('category')` | Quick conversion | `s.astype('category')` |
| `pd.Categorical()` | Custom categories/order | `pd.Categorical(data, categories=[...])` |
| `pd.CategoricalDtype` | Reusable type definition | `dtype = pd.CategoricalDtype(...)` |
| In DataFrame creation | Direct specification | `pd.DataFrame({'col': pd.Categorical(...)})` |

## Best Practices

1. **Define categories explicitly** when you know the valid values
2. **Use ordered=True** when categories have logical order
3. **Use CategoricalDtype** for consistency across multiple columns
4. **Specify dtype in read_csv** to save memory on large files
5. **Handle invalid values** - they become NaN silently


---

## Exercises

**Exercise 1.** Write code that creates a Pandas Categorical from the list `['low', 'medium', 'high', 'medium', 'low']` with categories `['low', 'medium', 'high']` and `ordered=True`.

??? success "Solution to Exercise 1"
    ```python
    import pandas as pd

    cat = pd.Categorical(
        ['low', 'medium', 'high', 'medium', 'low'],
        categories=['low', 'medium', 'high'],
        ordered=True
    )
    print(cat)
    print(f'Ordered: {cat.ordered}')
    ```

---

**Exercise 2.** Explain the difference between `pd.Categorical()` and `astype('category')`. When would you use each?

??? success "Solution to Exercise 2"
    `pd.Categorical()` creates a standalone categorical array where you can specify the categories and ordering explicitly at creation time. `.astype('category')` converts an existing Series to a categorical dtype, inferring the categories from the data. Use `pd.Categorical()` when you need to set custom categories or ordering upfront. Use `.astype('category')` for quick conversion of an existing column.

---

**Exercise 3.** Create a DataFrame with a string column and convert it to categorical using `.astype('category')`. Print the category codes and the memory usage before and after conversion.

??? success "Solution to Exercise 3"
    ```python
    import pandas as pd

    df = pd.DataFrame({'color': ['red', 'blue', 'green', 'red', 'blue'] * 100})
    print(f'Before: {df["color"].memory_usage()} bytes')
    df['color'] = df['color'].astype('category')
    print(f'After:  {df["color"].memory_usage()} bytes')
    print(df['color'].cat.codes[:5])
    ```

---

**Exercise 4.** Write code that creates a categorical with custom categories that include a category not present in the data (e.g., `'very_high'`). Show that this category appears in `.cat.categories`.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    cat = pd.Categorical(
        ['low', 'medium', 'high'],
        categories=['low', 'medium', 'high', 'very_high']
    )
    print(cat)
    print(f'Categories: {cat.categories.tolist()}')
    ```
