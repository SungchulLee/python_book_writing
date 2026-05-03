# Ordered Categoricals

Ordered categoricals allow logical comparisons between categories. This is essential when categories have a natural hierarchy, such as ratings, sizes, or priority levels.

!!! tip "Mental Model"
    An unordered categorical is like a set of labels with no ranking -- "red" is not greater than "blue." Setting `ordered=True` and specifying an order turns the labels into a ranked scale, so comparisons like `"medium" < "large"` become meaningful. This is essential for any column that represents a natural hierarchy.

## Why Ordered Matters

Without ordering, comparisons between categories are meaningless:

```python
import pandas as pd

# Unordered categorical
sizes = pd.Series(['medium', 'small', 'large'], dtype='category')

# This comparison doesn't make sense
try:
    result = sizes > 'small'
    print(result)  # May work but results are arbitrary
except TypeError as e:
    print(f"Error: {e}")
```

With ordering, comparisons reflect the logical hierarchy:

```python
# Ordered categorical
sizes = pd.Categorical(
    ['medium', 'small', 'large'],
    categories=['small', 'medium', 'large'],
    ordered=True
)
sizes = pd.Series(sizes)

# Now comparison is meaningful
print(sizes > 'small')
```

```
0     True   # medium > small
1    False   # small > small (False)
2     True   # large > small
dtype: bool
```

## Creating Ordered Categoricals

### Method 1: pd.Categorical with ordered=True

```python
cat = pd.Categorical(
    ['low', 'medium', 'high', 'low'],
    categories=['low', 'medium', 'high'],
    ordered=True
)
s = pd.Series(cat)
print(s)
```

```
0       low
1    medium
2      high
3       low
dtype: category
Categories (3, object): ['low' < 'medium' < 'high']
```

The `<` symbols indicate the order.

### Method 2: CategoricalDtype with ordered=True

```python
rating_dtype = pd.CategoricalDtype(
    categories=['D', 'C', 'B', 'A', 'S'],
    ordered=True
)

grades = pd.Series(['B', 'A', 'C', 'S', 'A']).astype(rating_dtype)
print(grades)
```

### Method 3: Using cat.as_ordered()

Convert an existing unordered categorical to ordered:

```python
s = pd.Series(['a', 'b', 'c'], dtype='category')
print(f"Before: ordered={s.cat.ordered}")

# First set category order, then make ordered
s = s.cat.reorder_categories(['a', 'b', 'c'], ordered=True)
print(f"After: ordered={s.cat.ordered}")
```

## Comparison Operations

### Basic Comparisons

```python
priorities = pd.Categorical(
    ['medium', 'high', 'low', 'critical', 'medium'],
    categories=['low', 'medium', 'high', 'critical'],
    ordered=True
)
priorities = pd.Series(priorities, name='priority')

# Greater than
print(priorities > 'medium')
# False, True, False, True, False

# Greater than or equal
print(priorities >= 'high')
# False, True, False, True, False

# Equal
print(priorities == 'medium')
# True, False, False, False, True

# Not equal
print(priorities != 'low')
# True, True, False, True, True
```

### Filtering with Comparisons

```python
df = pd.DataFrame({
    'task': ['Task A', 'Task B', 'Task C', 'Task D', 'Task E'],
    'priority': pd.Categorical(
        ['medium', 'high', 'low', 'critical', 'medium'],
        categories=['low', 'medium', 'high', 'critical'],
        ordered=True
    )
})

# High priority and above
urgent = df[df['priority'] >= 'high']
print(urgent)
```

```
     task  priority
1  Task B      high
3  Task D  critical
```

### Min, Max on Ordered Categoricals

```python
print(f"Minimum: {df['priority'].min()}")  # low
print(f"Maximum: {df['priority'].max()}")  # critical
```

## Practical Examples

### Credit Ratings

```python
# Credit rating scale (best to worst)
rating_categories = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B', 'CCC', 'CC', 'C', 'D']

# Note: reverse order so AAA is "greater than" lower ratings
rating_dtype = pd.CategoricalDtype(
    categories=rating_categories,
    ordered=True
)

bonds = pd.DataFrame({
    'issuer': ['Company A', 'Company B', 'Company C', 'Company D', 'Company E'],
    'rating': ['AA', 'BBB', 'A', 'BB', 'AAA']
})

bonds['rating'] = bonds['rating'].astype(rating_dtype)

# Investment grade: BBB and above
investment_grade = bonds[bonds['rating'] >= 'BBB']
print("Investment Grade Bonds:")
print(investment_grade)

# High yield (junk): below BBB
high_yield = bonds[bonds['rating'] < 'BBB']
print("\nHigh Yield Bonds:")
print(high_yield)
```

### Survey Likert Scale

```python
likert_categories = [
    'Strongly Disagree',
    'Disagree',
    'Neutral',
    'Agree',
    'Strongly Agree'
]

survey = pd.DataFrame({
    'respondent': [1, 2, 3, 4, 5, 6, 7, 8],
    'satisfaction': pd.Categorical(
        ['Agree', 'Neutral', 'Strongly Agree', 'Disagree',
         'Agree', 'Strongly Disagree', 'Neutral', 'Agree'],
        categories=likert_categories,
        ordered=True
    )
})

# Positive responses (Agree and above)
positive = survey[survey['satisfaction'] >= 'Agree']
print(f"Positive responses: {len(positive)} ({len(positive)/len(survey)*100:.0f}%)")

# Negative responses (Disagree and below)
negative = survey[survey['satisfaction'] <= 'Disagree']
print(f"Negative responses: {len(negative)} ({len(negative)/len(survey)*100:.0f}%)")
```

### Size/Tier Classification

```python
# Customer tiers
tier_dtype = pd.CategoricalDtype(
    categories=['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond'],
    ordered=True
)

customers = pd.DataFrame({
    'customer_id': [1, 2, 3, 4, 5],
    'tier': ['Gold', 'Bronze', 'Platinum', 'Silver', 'Gold'],
    'spend': [5000, 500, 15000, 2000, 4500]
})

customers['tier'] = customers['tier'].astype(tier_dtype)

# Premium customers (Gold and above)
premium = customers[customers['tier'] >= 'Gold']
print("Premium customers:")
print(premium)

# Potential upgrades (Silver - one tier below Gold)
potential_upgrades = customers[customers['tier'] == 'Silver']
print("\nPotential upgrade candidates:")
print(potential_upgrades)
```

### Risk Levels

```python
risk_dtype = pd.CategoricalDtype(
    categories=['Minimal', 'Low', 'Medium', 'High', 'Critical'],
    ordered=True
)

incidents = pd.DataFrame({
    'incident_id': [1, 2, 3, 4, 5],
    'risk_level': ['Medium', 'Critical', 'Low', 'High', 'Medium'],
    'description': ['Issue A', 'Issue B', 'Issue C', 'Issue D', 'Issue E']
})

incidents['risk_level'] = incidents['risk_level'].astype(risk_dtype)

# Escalation required (High and above)
escalate = incidents[incidents['risk_level'] >= 'High']
print("Requires escalation:")
print(escalate)
```

## Sorting with Ordered Categoricals

Ordered categoricals sort according to category order, not alphabetically:

```python
sizes = pd.Categorical(
    ['medium', 'small', 'large', 'medium', 'small'],
    categories=['small', 'medium', 'large'],
    ordered=True
)
df = pd.DataFrame({'size': sizes, 'value': [1, 2, 3, 4, 5]})

# Sort by size (logical order, not alphabetical)
df_sorted = df.sort_values('size')
print(df_sorted)
```

```
     size  value
1   small      2
4   small      5
0  medium      1
3  medium      4
2   large      3
```

## Changing Order

### reorder_categories()

```python
s = pd.Series(['a', 'b', 'c'], dtype='category')

# Set new order
s = s.cat.reorder_categories(['c', 'b', 'a'], ordered=True)
print(s.cat.categories)  # Index(['c', 'b', 'a'], dtype='object')

# Now 'c' < 'b' < 'a'
print(s > 'b')  # False, False, True
```

### Reversing Order

```python
# Original: small < medium < large
sizes = pd.Categorical(
    ['small', 'medium', 'large'],
    categories=['small', 'medium', 'large'],
    ordered=True
)

# Reverse: large < medium < small
sizes_reversed = sizes.reorder_categories(
    sizes.categories[::-1]
)
print(sizes_reversed.categories)  # ['large', 'medium', 'small']
```

## Caveats

### Cannot Compare Different Category Orders

```python
cat1 = pd.Categorical(['a', 'b'], categories=['a', 'b', 'c'], ordered=True)
cat2 = pd.Categorical(['a', 'b'], categories=['c', 'b', 'a'], ordered=True)

# cat1 == cat2  # ValueError: Categoricals can only be compared if categories are the same
```

### Unordered to Ordered Requires Explicit Ordering

```python
s = pd.Series(['a', 'b', 'c'], dtype='category')
# s > 'a'  # TypeError for unordered

# Must set order first
s = s.cat.reorder_categories(['a', 'b', 'c'], ordered=True)
# Now comparisons work
```

## Summary

| Operation | Requires Ordered |
|-----------|------------------|
| `==`, `!=` | No |
| `<`, `>`, `<=`, `>=` | Yes |
| `min()`, `max()` | Yes (for meaningful results) |
| `sort_values()` | No (but uses category order if ordered) |
| Filtering with comparison | Yes |


---

## Exercises

**Exercise 1.** Create an ordered categorical with levels `['small', 'medium', 'large']` and demonstrate that comparison operators (`<`, `>`) work correctly.

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

**Exercise 2.** Explain the difference between ordered and unordered categoricals. What operations are only available for ordered categoricals?

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page. The key concept involves understanding the categorical data type and its internal representation in Pandas.

---

**Exercise 3.** Write code that creates a Series of t-shirt sizes, converts it to an ordered categorical, and filters for all sizes greater than `'medium'`.

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

**Exercise 4.** Create an ordered categorical and use `.cat.set_categories()` to reorder the levels. Show that the comparison behavior changes accordingly.

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    s = pd.Categorical(['low', 'medium', 'high', 'low'],
                        categories=['low', 'medium', 'high'],
                        ordered=True)
    print(s)
    print(s > 'low')
    ```
