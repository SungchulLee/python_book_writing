# Introduction to Categoricals

In real-world datasets, many columns take on only a limited number of unique values, even if stored as strings or numbers. Such columns are ideal candidates for **categorical encoding**.

!!! tip "Mental Model"
    A categorical column is like a dropdown menu: the data can only take values from a fixed list. Pandas stores an integer code for each row and a separate table of unique labels, so repeated strings are stored once instead of millions of times. This insight drives both memory savings and faster groupby operations.

## What is Categorical Data?

Categorical data represents variables that can take on a limited, fixed number of possible values. Examples include:

| Domain | Example | Possible Values |
|--------|---------|-----------------|
| Finance | Stock sector | Technology, Finance, Healthcare, Energy, ... |
| Surveys | Agreement scale | Strongly Disagree, Disagree, Neutral, Agree, Strongly Agree |
| Credit | Rating | AAA, AA, A, BBB, BB, B, CCC, ... |
| Retail | Size | Small, Medium, Large, XL |
| Demographics | Education | High School, Bachelor's, Master's, PhD |

## How Pandas Stores Categoricals

A **Categorical** column in pandas is:

1. **Internally stored as integers** pointing to a category lookup table
2. **Memory efficient**, especially for repeated values
3. **Faster** for comparisons, groupby, and filtering operations

```
┌─────────────────────────────────────────────────────────┐
│                    String Storage                        │
├─────────────────────────────────────────────────────────┤
│ Row 0: "Technology"  (10 bytes)                         │
│ Row 1: "Finance"     (7 bytes)                          │
│ Row 2: "Technology"  (10 bytes)  ← Duplicate stored     │
│ Row 3: "Healthcare"  (10 bytes)                         │
│ Row 4: "Technology"  (10 bytes)  ← Duplicate stored     │
│ ...                                                      │
│ Total: N × avg_string_length bytes                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                  Categorical Storage                     │
├─────────────────────────────────────────────────────────┤
│ Categories: ["Technology", "Finance", "Healthcare"]     │
│             (stored once)                                │
├─────────────────────────────────────────────────────────┤
│ Codes (integers):                                        │
│ Row 0: 0  (1 byte)  → "Technology"                      │
│ Row 1: 1  (1 byte)  → "Finance"                         │
│ Row 2: 0  (1 byte)  → "Technology"                      │
│ Row 3: 2  (1 byte)  → "Healthcare"                      │
│ Row 4: 0  (1 byte)  → "Technology"                      │
│ ...                                                      │
│ Total: N bytes + category_table                         │
└─────────────────────────────────────────────────────────┘
```

## Quick Example

```python
import pandas as pd

# Regular string column
s_string = pd.Series(['apple', 'banana', 'apple', 'cherry', 'apple'])
print(f"String dtype: {s_string.dtype}")  # object

# Categorical column
s_cat = s_string.astype('category')
print(f"Categorical dtype: {s_cat.dtype}")  # category

# View internal structure
print(f"Categories: {s_cat.cat.categories.tolist()}")
print(f"Codes: {s_cat.cat.codes.tolist()}")
```

```
String dtype: object
Categorical dtype: category
Categories: ['apple', 'banana', 'cherry']
Codes: [0, 1, 0, 2, 0]
```

## Benefits of Categorical Data

### 1. Memory Efficiency

Categorical data uses dramatically less memory for columns with repeated values.

```python
import numpy as np

# 1 million rows with 10 sectors
sectors = ['Tech', 'Finance', 'Healthcare', 'Retail', 'Energy', 
           'Utilities', 'Media', 'Aerospace', 'Banks', 'Insurance']
data = np.random.choice(sectors, size=1_000_000)

df = pd.DataFrame({'Sector': data})

# Before: string storage
print(f"String: {df['Sector'].memory_usage(deep=True) / 1e6:.1f} MB")

# After: categorical storage
df['Sector'] = df['Sector'].astype('category')
print(f"Categorical: {df['Sector'].memory_usage(deep=True) / 1e6:.1f} MB")
```

```
String: 57.0 MB
Categorical: 1.0 MB
```

### 2. Faster Operations

GroupBy and other operations are significantly faster on categorical columns.

```python
import time

df['Returns'] = np.random.randn(1_000_000)

# Time groupby with string column
df_string = df.copy()
df_string['Sector'] = df_string['Sector'].astype(str)

start = time.time()
_ = df_string.groupby('Sector')['Returns'].mean()
string_time = time.time() - start

# Time groupby with categorical column
start = time.time()
_ = df.groupby('Sector')['Returns'].mean()
cat_time = time.time() - start

print(f"String groupby: {string_time:.3f}s")
print(f"Categorical groupby: {cat_time:.3f}s")
print(f"Speedup: {string_time/cat_time:.1f}x")
```

### 3. Logical Ordering

Ordered categoricals enable meaningful comparisons.

```python
# Without order: comparison fails
sizes = pd.Series(['medium', 'small', 'large'])
# sizes > 'small'  # TypeError or meaningless result

# With order: comparison works
sizes = pd.Categorical(
    ['medium', 'small', 'large'],
    categories=['small', 'medium', 'large'],
    ordered=True
)
sizes = pd.Series(sizes)

print(sizes > 'small')  # False, False, True
```

### 4. Data Validation

Categories enforce valid values—invalid data is caught early.

```python
valid_ratings = ['AAA', 'AA', 'A', 'BBB', 'BB', 'B']
ratings = pd.Categorical(['AA', 'BBB', 'A'], categories=valid_ratings)

# Adding invalid value raises error or becomes NaN
# ratings = pd.Categorical(['AA', 'INVALID'], categories=valid_ratings)
# ValueError or NaN depending on method
```

## When to Use Categorical

| Scenario | Use Categorical? | Reason |
|----------|------------------|--------|
| Limited unique values (< 50% of rows) | ✅ Yes | Memory savings |
| Frequent repeated values | ✅ Yes | Memory + speed |
| Natural order exists | ✅ Yes | Enable comparisons |
| Heavy groupby/filtering | ✅ Yes | Performance boost |
| All unique values | ❌ No | No benefit |
| Need string operations | ⚠️ Maybe | Convert back if needed |

## Categorical vs Other Types

| Type | Use Case | Memory | Ordered Comparison |
|------|----------|--------|-------------------|
| `object` (string) | Free-form text | High | No |
| `category` | Fixed set of values | Low | Optional |
| `int` / `float` | Numeric codes | Medium | Yes (numeric) |

## Real-World Applications

1. **Stock Sectors**: Technology, Healthcare, Finance, ...
2. **Credit Ratings**: AAA, AA, A, BBB, BB, B, ...
3. **Survey Responses**: Strongly Agree, Agree, Neutral, ...
4. **Product Categories**: Electronics, Clothing, Food, ...
5. **Geographic Regions**: North, South, East, West
6. **Time Periods**: Q1, Q2, Q3, Q4
7. **Risk Levels**: Low, Medium, High, Critical


---

## Exercises

**Exercise 1.** Create a Series with categorical dtype and print its `dtype`, `cat.categories`, and `cat.codes`.

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

**Exercise 2.** Explain why categorical data types are useful in Pandas. Name two benefits.

??? success "Solution to Exercise 2"
    See the explanation in the main content of this page. The key concept involves understanding the categorical data type and its internal representation in Pandas.

---

**Exercise 3.** Write code that creates a DataFrame with 10000 rows of a column with only 3 unique values. Compare the memory usage before and after converting to categorical.

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

**Exercise 4.** Convert a column of repeated strings to categorical type and demonstrate that comparisons still work correctly (e.g., filtering with `==`).

??? success "Solution to Exercise 4"
    ```python
    import pandas as pd

    s = pd.Categorical(['low', 'medium', 'high', 'low'],
                        categories=['low', 'medium', 'high'],
                        ordered=True)
    print(s)
    print(s > 'low')
    ```
