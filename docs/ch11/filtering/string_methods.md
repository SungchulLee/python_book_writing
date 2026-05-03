# String Methods

The `.str` accessor provides string operations for filtering and transforming text data.

!!! tip "Mental Model"
    String filtering combines two ideas: the `.str` accessor exposes vectorized string methods, and each method returns a boolean mask or transformed Series. Chain `.str.contains()` or `.str.startswith()` inside `[]` to filter rows by text patterns, just as you would chain comparison operators for numeric filtering.

## str.contains

Check if string contains a pattern.

### 1. Basic Contains

```python
import pandas as pd

df = pd.DataFrame({
    'description': ['thrilling adventure', 'boring documentary', 
                   'exciting drama', 'slow and boring', 'great comedy']
})

# Filter containing 'boring'
result = df[df['description'].str.contains('boring')]
print(result)
```

```
         description
1  boring documentary
3     slow and boring
```

### 2. Case Insensitive

```python
result = df[df['description'].str.contains('boring', case=False)]
# Matches 'boring', 'Boring', 'BORING'
```

### 3. NOT Contains

```python
result = df[~df['description'].str.contains('boring', case=False)]
```

## str.startswith

Check if string starts with pattern.

### 1. Basic startswith

```python
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Mike', 'Molly', 'Eve']
})

# Names starting with 'M'
result = df[df['name'].str.startswith('M')]
print(result)
```

```
    name
2   Mike
3  Molly
```

### 2. NOT startswith

```python
result = df[~df['name'].str.startswith('M')]
```

### 3. Multiple Prefixes

```python
# Use regex with str.contains
result = df[df['name'].str.contains('^[AM]', regex=True)]
# Names starting with A or M
```

## str.endswith

Check if string ends with pattern.

### 1. Basic endswith

```python
df = pd.DataFrame({
    'email': ['user@gmail.com', 'admin@yahoo.com', 'test@gmail.com']
})

result = df[df['email'].str.endswith('@gmail.com')]
```

### 2. File Extensions

```python
df = pd.DataFrame({'filename': ['report.pdf', 'data.csv', 'image.png']})
pdf_files = df[df['filename'].str.endswith('.pdf')]
```

### 3. Multiple Suffixes

```python
# Use tuple (pandas >= 1.0)
result = df[df['email'].str.endswith(('.com', '.org'))]
```

## LeetCode Example: Not Boring Movies

Filter by description content.

### 1. Sample Data

```python
cinema = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'description': ['thrilling', 'boring', 'exciting', 'boring doc', 'great']
})
```

### 2. Combined Filter

```python
# Odd ID AND not boring
result = cinema[
    (cinema['id'] % 2 != 0) & 
    (~cinema['description'].str.contains('boring', case=False))
]
```

### 3. Result

```python
print(result)
```

## LeetCode Example: Special Bonus

Filter by name prefix.

### 1. Sample Data

```python
employees = pd.DataFrame({
    'employee_id': [1, 2, 3, 4, 5],
    'name': ['Alice', 'Bob', 'Mike', 'Molly', 'Eve'],
    'salary': [50000, 60000, 70000, 80000, 90000]
})
```

### 2. Filter Condition

```python
# Odd ID and name doesn't start with 'M'
eligible = (employees['employee_id'] % 2 != 0) & (~employees['name'].str.startswith('M'))
```

### 3. Apply Bonus

```python
employees['bonus'] = 0
employees.loc[eligible, 'bonus'] = employees.loc[eligible, 'salary']
```

## str.match

Match regular expression at start.

### 1. Regex Match

```python
df = pd.DataFrame({'code': ['ABC123', 'XYZ456', 'ABC789']})
result = df[df['code'].str.match('^ABC')]
```

### 2. Pattern Groups

```python
# Extract matched groups
df['code'].str.extract(r'([A-Z]+)(\d+)')
```

### 3. Full Match

```python
result = df[df['code'].str.fullmatch(r'[A-Z]{3}\d{3}')]
```

## str.len

Filter by string length.

### 1. Length Filter

```python
df = pd.DataFrame({'name': ['Al', 'Bob', 'Charlie', 'Ed']})
result = df[df['name'].str.len() > 2]
```

### 2. Exact Length

```python
result = df[df['name'].str.len() == 3]
```

### 3. Range

```python
result = df[df['name'].str.len().between(3, 5)]
```

## String Transformation

Transform before filtering.

### 1. Lower/Upper

```python
df['name_lower'] = df['name'].str.lower()
result = df[df['name_lower'] == 'alice']
```

### 2. Strip Whitespace

```python
df['name_clean'] = df['name'].str.strip()
```

### 3. Replace

```python
df['name_clean'] = df['name'].str.replace('-', '')
```

## Handling NaN

String methods and missing values.

### 1. na Parameter

```python
# Default: NaN returns NaN
df['name'].str.contains('A')  # NaN for missing

# Treat NaN as False
df['name'].str.contains('A', na=False)
```

### 2. fillna First

```python
df['name'].fillna('').str.contains('A')
```

### 3. Check First

```python
mask = df['name'].notna() & df['name'].str.contains('A')
```

## Common Patterns

Frequently used string filters.

### 1. Email Domain

```python
gmail_users = df[df['email'].str.contains('@gmail.com')]
```

### 2. Phone Format

```python
valid_phone = df[df['phone'].str.match(r'^\d{3}-\d{3}-\d{4}$')]
```

### 3. Name Pattern

```python
# Names with Jr. or Sr.
suffix = df[df['name'].str.contains(r'\b(Jr\.|Sr\.)\b', regex=True)]
```

---

## Exercises

**Exercise 1.**
Given a DataFrame with a `'name'` column, use `.str.contains()` to find all names that contain the substring `'son'` (case-insensitive). Print the matching rows.

??? success "Solution to Exercise 1"
    Use `case=False` for case-insensitive search.

        import pandas as pd

        df = pd.DataFrame({
            'name': ['Johnson', 'Smith', 'Jackson', 'Wilson', 'Lee']
        })
        result = df[df['name'].str.contains('son', case=False)]
        print(result)

---

**Exercise 2.**
Use `.str.startswith()` and `.str.endswith()` together to filter product codes that start with `'PRD'` and end with a digit. Use a regex pattern with `.str.match()` as an alternative.

??? success "Solution to Exercise 2"
    Combine `startswith` and regex matching.

        import pandas as pd

        df = pd.DataFrame({
            'code': ['PRD001', 'PRD002', 'SKU-10', 'PRD-AB', 'PRD999']
        })
        # Method 1: startswith + regex endswith
        mask = df['code'].str.startswith('PRD') & df['code'].str.match(r'.*\d$')
        print(df[mask])

---

**Exercise 3.**
Use `.str.len()` to filter a DataFrame of descriptions, keeping only rows where the description is between 10 and 100 characters long. Print the count of rows before and after filtering.

??? success "Solution to Exercise 3"
    Use `.str.len()` with `.between()` for length filtering.

        import pandas as pd

        df = pd.DataFrame({
            'description': ['Short', 'A medium-length description here',
                          'X' * 150, 'Another valid description']
        })
        print(f"Before: {len(df)} rows")
        mask = df['description'].str.len().between(10, 100)
        result = df[mask]
        print(f"After: {len(result)} rows")
        print(result)
