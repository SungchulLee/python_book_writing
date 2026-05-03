# map Method

The `map()` method applies a function or mapping to each element of a Series. It is useful for element-wise transformations and value substitutions.

!!! tip "Mental Model"
    `map()` is a lookup table applied to every element: pass a dict and each value is replaced by its corresponding entry, pass a function and it runs on each element. Unlike `apply`, `map` is strictly element-wise and works only on Series. It is the fastest way to do value substitution or simple per-element transforms.

## Basic Mapping

Map values using a function.

### 1. Lambda Function

```python
import pandas as pd

df = pd.DataFrame({
    'Age': [25, 30, 35, 40]
})

df['Age Group'] = df['Age'].map(lambda x: 'Young' if x < 30 else 'Old')
print(df)
```

```
   Age Age Group
0   25     Young
1   30       Old
2   35       Old
3   40       Old
```

### 2. Named Function

```python
def categorize_age(age):
    if age < 30:
        return 'Young'
    elif age < 50:
        return 'Middle'
    else:
        return 'Senior'

df['Category'] = df['Age'].map(categorize_age)
```

### 3. Built-in Functions

```python
df['Name'] = df['Name'].map(str.upper)
df['Value'] = df['Value'].map(abs)
```

## Dictionary Mapping

Map values using a dictionary.

### 1. Value Substitution

```python
df = pd.DataFrame({
    'grade': ['A', 'B', 'C', 'A', 'B']
})

grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0}
df['points'] = df['grade'].map(grade_points)
print(df)
```

```
  grade  points
0     A     4.0
1     B     3.0
2     C     2.0
3     A     4.0
4     B     3.0
```

### 2. Missing Keys

```python
# Keys not in dictionary become NaN
status_map = {'active': 1, 'inactive': 0}
df['status'].map(status_map)  # Unknown status → NaN
```

### 3. Complete Mapping

```python
# Provide all possible values
df['status'].map({'active': 1, 'inactive': 0, 'pending': -1})
```

## Series Mapping

Map using another Series.

### 1. Index-based Mapping

```python
mapping_series = pd.Series({
    'A': 'Excellent',
    'B': 'Good',
    'C': 'Average'
})

df['description'] = df['grade'].map(mapping_series)
```

### 2. From External Data

```python
# Map product IDs to names
product_names = products.set_index('id')['name']
orders['product_name'] = orders['product_id'].map(product_names)
```

### 3. Alignment by Index

The mapping Series is aligned by its index to the values in the source Series.

## map vs apply

Understanding when to use each method.

### 1. map for Series Only

```python
# map works on Series, not DataFrame
df['col'].map(func)  # OK
# df.map(func)       # Not available in older pandas
```

### 2. apply for Both

```python
df['col'].apply(func)    # Series
df.apply(func, axis=0)   # DataFrame columns
df.apply(func, axis=1)   # DataFrame rows
```

### 3. Performance

```python
# map is generally faster for simple mappings
# apply is more flexible for complex operations
```

## Practical Examples

Common mapping scenarios.

### 1. Boolean to String

```python
df['is_active'] = df['is_active'].map({True: 'Yes', False: 'No'})
```

### 2. Code to Description

```python
country_codes = {'US': 'United States', 'UK': 'United Kingdom', 'CA': 'Canada'}
df['country_name'] = df['country_code'].map(country_codes)
```

### 3. Numeric Binning

```python
def bin_value(x):
    if x < 0:
        return 'negative'
    elif x == 0:
        return 'zero'
    else:
        return 'positive'

df['category'] = df['value'].map(bin_value)
```

## Handling Missing Results

Deal with unmapped values.

### 1. fillna After Map

```python
df['mapped'] = df['col'].map(mapping_dict).fillna('Unknown')
```

### 2. Default with get

```python
df['mapped'] = df['col'].map(
    lambda x: mapping_dict.get(x, 'Default')
)
```

### 3. na_action Parameter

```python
# Skip NaN values during mapping
df['col'].map(func, na_action='ignore')
```

---

## Exercises

**Exercise 1.**
Create a Series of country codes like `['US', 'UK', 'JP', 'DE']`. Use `.map()` with a dictionary to convert them to full country names (e.g., `{'US': 'United States', 'UK': 'United Kingdom', ...}`).

??? success "Solution to Exercise 1"
    Map codes to names using a dictionary.

        import pandas as pd

        codes = pd.Series(['US', 'UK', 'JP', 'DE'])
        mapping = {'US': 'United States', 'UK': 'United Kingdom', 'JP': 'Japan', 'DE': 'Germany'}
        names = codes.map(mapping)
        print(names)

---

**Exercise 2.**
Create a numeric Series. Use `.map()` with a lambda to classify each value as `'positive'`, `'negative'`, or `'zero'`. Compare the result with using `.apply()` -- both should be identical.

??? success "Solution to Exercise 2"
    Compare map and apply with a lambda.

        import pandas as pd

        s = pd.Series([-3, 0, 5, -1, 0, 8])
        result_map = s.map(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'zero'))
        result_apply = s.apply(lambda x: 'positive' if x > 0 else ('negative' if x < 0 else 'zero'))
        print(result_map)
        assert (result_map == result_apply).all()
        print("map and apply produce identical results.")

---

**Exercise 3.**
Create a Series with values that partially match a mapping dictionary (some values have no mapping). Use `.map()` and observe which values become `NaN`. Then use `.map()` followed by `.fillna()` to provide a default for unmapped values.

??? success "Solution to Exercise 3"
    Handle unmapped values with fillna.

        import pandas as pd

        s = pd.Series(['a', 'b', 'c', 'd'])
        mapping = {'a': 'alpha', 'b': 'beta'}
        mapped = s.map(mapping)
        print("With NaN:\n", mapped)
        filled = mapped.fillna('unknown')
        print("With default:\n", filled)
