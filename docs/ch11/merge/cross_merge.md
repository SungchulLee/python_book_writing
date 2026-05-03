# Cross Merge

A cross merge produces the Cartesian product of two DataFrames, pairing every row from the left with every row from the right.

!!! tip "Mental Model"
    A cross merge is "every possible combination." If the left has M rows and the right has N rows, the result has M x N rows. It is SQL's `CROSS JOIN` -- useful for generating all pairings (e.g., students x exams) but dangerous on large tables because the output size explodes multiplicatively.

## Basic Concept

Create all possible combinations of rows.

### 1. Cross Join

```python
import pandas as pd

students = pd.DataFrame({
    'student_id': [1, 2],
    'student_name': ['Alice', 'Bob']
})

subjects = pd.DataFrame({
    'subject_name': ['Math', 'Science']
})

result = pd.merge(students, subjects, how='cross')
print(result)
```

```
   student_id student_name subject_name
0           1        Alice         Math
1           1        Alice      Science
2           2          Bob         Math
3           2          Bob      Science
```

### 2. Result Size

Cross merge produces `len(left) × len(right)` rows.

### 3. No Join Key

Cross merge does not use `on` parameter.

## LeetCode Example: Student Examinations

Create all student-subject combinations.

### 1. Sample Data

```python
students = pd.DataFrame({
    'student_id': [1, 2],
    'student_name': ['Alice', 'Bob']
})

subjects = pd.DataFrame({
    'subject_name': ['Math', 'Science']
})
```

### 2. Cross Merge

```python
student_subject = pd.merge(students, subjects, how='cross')
print(student_subject)
```

### 3. Use with Left Join

```python
# After creating all combinations, left join with actual data
examination_count = pd.DataFrame({
    'student_id': [1, 1, 2],
    'subject_name': ['Math', 'Science', 'Math'],
    'attended_exams': [2, 1, 3]
})

result = pd.merge(
    student_subject,
    examination_count,
    on=['student_id', 'subject_name'],
    how='left'
)
```

## Practical Applications

When to use cross merge.

### 1. Generate All Combinations

```python
# All product-store combinations
products = pd.DataFrame({'product': ['A', 'B', 'C']})
stores = pd.DataFrame({'store': ['X', 'Y']})

all_combos = pd.merge(products, stores, how='cross')
```

### 2. Time Period Analysis

```python
# All month-category combinations
months = pd.DataFrame({'month': ['Jan', 'Feb', 'Mar']})
categories = pd.DataFrame({'category': ['Food', 'Drinks']})

template = pd.merge(months, categories, how='cross')
```

### 3. Fill Missing Combinations

```python
# Create complete grid, then merge with actual data
template = pd.merge(dates_df, products_df, how='cross')
result = pd.merge(template, sales_data, how='left').fillna(0)
```

## Performance Warning

Cross merge can create very large DataFrames.

### 1. Size Calculation

```python
left_size = len(df1)
right_size = len(df2)
result_size = left_size * right_size

print(f"Result will have {result_size} rows")
```

### 2. Memory Considerations

```python
# 1000 × 1000 = 1,000,000 rows
# Be cautious with large DataFrames
```

### 3. Filter After Merge

```python
# Consider filtering immediately after cross merge
cross_result = pd.merge(df1, df2, how='cross')
filtered = cross_result[cross_result['condition']]
```

## Alternative Methods

Other ways to create Cartesian products.

### 1. itertools.product

```python
from itertools import product

combos = list(product(df1['col'], df2['col']))
```

### 2. MultiIndex.from_product

```python
idx = pd.MultiIndex.from_product([
    df1['col'].unique(),
    df2['col'].unique()
])
```

### 3. Comparison

```python
# pd.merge(how='cross') is most readable
# itertools.product for non-DataFrame use
```

## Complete Example

Build examination matrix with cross merge.

### 1. Create Template

```python
students = pd.DataFrame({
    'student_id': [1, 2, 3],
    'student_name': ['Alice', 'Bob', 'Carol']
})

subjects = pd.DataFrame({
    'subject_name': ['Math', 'Science', 'History']
})

template = pd.merge(students, subjects, how='cross')
```

### 2. Merge with Data

```python
exam_data = pd.DataFrame({
    'student_id': [1, 1, 2, 3],
    'subject_name': ['Math', 'Science', 'Math', 'History'],
    'score': [85, 90, 78, 92]
})

result = pd.merge(
    template,
    exam_data,
    on=['student_id', 'subject_name'],
    how='left'
)
```

### 3. Fill Missing

```python
result['score'] = result['score'].fillna(0)
```

---

## Exercises

**Exercise 1.**
Create a `colors` DataFrame (`['red', 'blue']`) and a `sizes` DataFrame (`['S', 'M', 'L']`). Use a cross merge to generate all 6 possible color-size combinations.

??? success "Solution to Exercise 1"
    Generate all color-size combinations.

        import pandas as pd

        colors = pd.DataFrame({'color': ['red', 'blue']})
        sizes = pd.DataFrame({'size': ['S', 'M', 'L']})
        result = pd.merge(colors, sizes, how='cross')
        print(result)
        assert len(result) == 6

---

**Exercise 2.**
Create a `students` DataFrame and an `exams` DataFrame. Use a cross merge to create a row for every student-exam combination, then verify the result has `len(students) * len(exams)` rows.

??? success "Solution to Exercise 2"
    Create all student-exam combinations.

        import pandas as pd

        students = pd.DataFrame({'student': ['Alice', 'Bob', 'Carol']})
        exams = pd.DataFrame({'exam': ['Midterm', 'Final']})
        result = pd.merge(students, exams, how='cross')
        print(result)
        assert len(result) == len(students) * len(exams)

---

**Exercise 3.**
Use a cross merge to create a multiplication table: merge a DataFrame of numbers 1-5 with itself to get all 25 pairs, then compute the product for each pair.

??? success "Solution to Exercise 3"
    Build a multiplication table using cross merge.

        import pandas as pd

        nums = pd.DataFrame({'a': range(1, 6)})
        result = pd.merge(nums, nums.rename(columns={'a': 'b'}), how='cross')
        result['product'] = result['a'] * result['b']
        print(result)
        assert len(result) == 25
