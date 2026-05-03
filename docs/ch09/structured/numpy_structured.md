# Structured Arrays

Structured arrays (also called record arrays) allow you to store heterogeneous data types in a single array, similar to a database table or spreadsheet row.

!!! tip "Mental Model"
    A structured array is NumPy's version of a database table: each element is a "row" containing named fields of potentially different types (e.g., a string name, an int age, a float score). Access a column by field name (`arr['age']`), a row by index (`arr[0]`). For most tabular data work, Pandas is more convenient, but structured arrays shine when you need tight memory control or C-level interop.

    At the memory level, a structured array stores different fields in a **single
    contiguous memory block** with byte offsets — the dtype acts as a schema that
    tells NumPy where each field starts within each record.

!!! warning "Array of Structs vs Struct of Arrays"
    There are two ways to store tabular data in memory, and the choice has real
    performance consequences:

    **Array of Structs (AoS)** — what structured arrays use:
    ```text
    [row1: name, age, score] [row2: name, age, score] ...
    ```
    Each record's fields are contiguous. Good for record-at-a-time access and
    C struct interop, but column operations (e.g., `arr['score'].mean()`) must
    skip over interleaved fields, reducing cache efficiency.

    **Struct of Arrays (SoA)** — what separate NumPy arrays / Pandas use:
    ```text
    names:  [name1, name2, ...]
    ages:   [age1,  age2,  ...]
    scores: [score1, score2, ...]
    ```
    Each column is contiguous. Vectorized column operations are cache-friendly
    and fast, but accessing a full record requires gathering from multiple arrays.

    | Concern | AoS (structured) | SoA (separate arrays) |
    |---------|------------------|----------------------|
    | Record access | Fast (contiguous) | Slow (scattered) |
    | Column vectorization | Slower (interleaved) | Fast (contiguous) |
    | C interop | Natural (`memcpy` a struct) | Requires packing |
    | Cache locality | Per-record | Per-column |

    **Rule of thumb:** use structured arrays (AoS) for binary I/O and C interop;
    use separate arrays or Pandas (SoA) for analytical computation.

!!! note "Structured Data Model"
    ```text
    A structured array is:
      - a contiguous block of memory
      - interpreted as records with named fields
      - defined by a dtype schema (field names + types + offsets)

    It allows:
      - heterogeneous data in a single array
      - vectorized operations across fields
      - memory-efficient tabular storage
      - direct interop with C structs and binary formats
    ```

!!! tip "Decision Guide"
    | Use case | Tool |
    |----------|------|
    | Memory-critical tabular data | **Structured arrays** |
    | Binary file formats / C interop | **Structured arrays** |
    | Data analysis (groupby, joins, missing values) | **Pandas** |
    | Heavy analytics / exploratory work | **Pandas** |

    Avoid structured arrays for operations that Pandas handles natively (groupby,
    pivot, merge) — the ergonomic cost is not worth the memory savings.

```python
import numpy as np
```

---

## What are Structured Arrays?

Regular NumPy arrays hold homogeneous data (all same type). Structured arrays hold **records** with multiple named fields of different types:

```python
# Regular array: all floats
regular = np.array([1.0, 2.0, 3.0])

# Structured array: mixed types
dt = np.dtype([('name', 'U10'), ('age', 'i4'), ('score', 'f8')])
structured = np.array([
    ('Alice', 25, 95.5),
    ('Bob', 30, 87.3),
    ('Charlie', 22, 91.0)
], dtype=dt)
```

---

## Creating Structured Arrays

The dtype is the **schema definition** for your structured array — it specifies
field names, types, and (implicitly) byte offsets, just as a `CREATE TABLE`
statement defines column names and types in SQL.

### Method 1: dtype with List of Tuples

```python
# Define dtype: (field_name, data_type)
dt = np.dtype([
    ('name', 'U20'),    # Unicode string, max 20 chars
    ('age', 'i4'),      # 32-bit integer
    ('salary', 'f8'),   # 64-bit float
    ('active', '?')     # Boolean
])

# Create array
employees = np.array([
    ('Alice', 30, 75000.0, True),
    ('Bob', 25, 65000.0, True),
    ('Charlie', 35, 85000.0, False)
], dtype=dt)
```

### Method 2: Dictionary Format

```python
dt = np.dtype({
    'names': ['x', 'y', 'z'],
    'formats': ['f8', 'f8', 'f8']
})

points = np.array([(1.0, 2.0, 3.0), (4.0, 5.0, 6.0)], dtype=dt)
```

### Method 3: String Format

```python
# Comma-separated type strings
dt = np.dtype('U10, i4, f8')  # Unnamed fields: f0, f1, f2

data = np.array([('Alice', 25, 95.5)], dtype=dt)
print(data['f0'])  # 'Alice'
```

---

## Data Type Codes

| Code | Type | Example |
|------|------|---------|
| `'i4'` | 32-bit int | `np.int32` |
| `'i8'` | 64-bit int | `np.int64` |
| `'f4'` | 32-bit float | `np.float32` |
| `'f8'` | 64-bit float | `np.float64` |
| `'U10'` | Unicode string (10 chars) | |
| `'S10'` | Byte string (10 bytes) | |
| `'?'` | Boolean | `np.bool_` |
| `'c16'` | Complex 128 | `np.complex128` |

---

## Accessing Data

### By Field Name

```python
dt = np.dtype([('name', 'U10'), ('age', 'i4'), ('score', 'f8')])
students = np.array([
    ('Alice', 20, 95.5),
    ('Bob', 22, 87.3),
    ('Charlie', 21, 91.0)
], dtype=dt)

# Access entire column
print(students['name'])   # ['Alice' 'Bob' 'Charlie']
print(students['age'])    # [20 22 21]
print(students['score'])  # [95.5 87.3 91. ]

# Access single record
print(students[0])        # ('Alice', 20, 95.5)
print(students[0]['name'])  # 'Alice'
```

### By Index

```python
# First record
print(students[0])  # ('Alice', 20, 95.5)

# Slice
print(students[:2])  # First two records

# Boolean indexing
adults = students[students['age'] >= 21]
print(adults['name'])  # ['Bob' 'Charlie']
```

### Multiple Fields

```python
# Select multiple fields (returns structured array)
subset = students[['name', 'score']]
print(subset.dtype)  # [('name', '<U10'), ('score', '<f8')]
```

---

## Modifying Data

```python
# Modify single field
students['score'][0] = 98.0

# Modify entire record
students[1] = ('Robert', 23, 90.0)

# Modify column
students['age'] = students['age'] + 1  # Everyone ages by 1
```

---

## Nested Structures

```python
# Nested dtype
address_dt = np.dtype([('city', 'U20'), ('zip', 'U10')])
person_dt = np.dtype([
    ('name', 'U20'),
    ('address', address_dt)
])

people = np.array([
    ('Alice', ('New York', '10001')),
    ('Bob', ('Los Angeles', '90001'))
], dtype=person_dt)

# Access nested fields
print(people['address']['city'])  # ['New York' 'Los Angeles']
```

---

## Array Fields

```python
# Field that is itself an array
dt = np.dtype([
    ('name', 'U10'),
    ('grades', 'f8', (3,))  # Array of 3 floats
])

students = np.array([
    ('Alice', [95, 87, 92]),
    ('Bob', [88, 91, 85])
], dtype=dt)

print(students['grades'])
# [[95. 87. 92.]
#  [88. 91. 85.]]

print(students[0]['grades'].mean())  # 91.33
```

---

## Record Arrays (recarray)

A `recarray` is **syntactic sugar** over a structured array — the underlying data
and dtype are identical, but you can write `rec.name` instead of `rec['name']`.
The convenience comes at a small performance cost (attribute access is slower than
item access), so use recarrays for interactive exploration and structured arrays
for production code.

Record arrays allow attribute-style access:

```python
# Convert structured array to recarray
rec = students.view(np.recarray)

# Attribute access (instead of indexing)
print(rec.name)   # ['Alice' 'Bob']
print(rec.age)    # [20 22]
print(rec[0].name)  # 'Alice'

# Create recarray directly
rec = np.rec.array([
    ('Alice', 25, 95.5),
    ('Bob', 30, 87.3)
], dtype=[('name', 'U10'), ('age', 'i4'), ('score', 'f8')])
```

---

## Practical Examples

### CSV-like Data

```python
# Load CSV-like data
dt = np.dtype([
    ('id', 'i4'),
    ('product', 'U30'),
    ('price', 'f8'),
    ('quantity', 'i4')
])

inventory = np.array([
    (1, 'Widget', 9.99, 100),
    (2, 'Gadget', 24.99, 50),
    (3, 'Gizmo', 14.99, 75)
], dtype=dt)

# Calculate total value
total_value = (inventory['price'] * inventory['quantity']).sum()
print(f"Total inventory value: ${total_value:.2f}")
```

### Sorting Structured Arrays

```python
# Sort by single field
sorted_by_score = np.sort(students, order='score')

# Sort by multiple fields
sorted_multi = np.sort(students, order=['age', 'score'])
```

### Filtering

```python
# Boolean filtering
high_scorers = students[students['score'] > 90]
young_students = students[students['age'] < 22]

# Combined conditions
filtered = students[(students['age'] >= 20) & (students['score'] > 85)]
```

---

## When to Use Structured Arrays

### Use Structured Arrays When:

- Working with large datasets in pure NumPy
- Need memory-efficient storage
- Interfacing with C/binary data formats
- Simple tabular operations without pandas overhead

### Use Pandas Instead When:

- Need advanced data manipulation
- Working with time series
- Need missing value handling (NaN)
- Complex groupby/merge operations

---

## Summary

| Task | Code |
|------|------|
| Create dtype | `np.dtype([('name', 'U10'), ('age', 'i4')])` |
| Create array | `np.array([('Alice', 25)], dtype=dt)` |
| Access field | `arr['name']` |
| Access record | `arr[0]` |
| Access nested | `arr['address']['city']` |
| Sort by field | `np.sort(arr, order='age')` |
| Filter | `arr[arr['age'] > 20]` |
| To recarray | `arr.view(np.recarray)` |

**Key Takeaways**:

- Structured arrays store heterogeneous data with named fields
- Access fields by name: `arr['fieldname']`
- Use dtype codes: `'i4'` (int32), `'f8'` (float64), `'U10'` (string)
- Record arrays add attribute-style access: `arr.name`
- Can nest structures and include array fields
- Good for memory-efficient tabular data without pandas
- Use `order` parameter for sorting by fields

---

## Exercises

**Exercise 1.** Write a short code example that demonstrates the main concept covered on this page. Include comments explaining each step.

??? success "Solution to Exercise 1"
    Refer to the code examples in the page content above. A complete solution would recreate the key pattern with clear comments explaining the NumPy operations involved.

---

**Exercise 2.** Predict the output of a code snippet that uses the features described on this page. Explain why the output is what it is.

??? success "Solution to Exercise 2"
    The output depends on how NumPy handles the specific operation. Key factors include array shapes, dtypes, and broadcasting rules. Trace through the computation step by step.

---

**Exercise 3.** Write a practical function that applies the concepts from this page to solve a real data processing task. Test it with sample data.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    # Example: apply the page's concept to process sample data
    data = np.random.default_rng(42).random((5, 3))
    # Apply the relevant operation
    result = data  # replace with actual operation
    print(result)
    ```

---

**Exercise 4.** Identify a common mistake when using the features described on this page. Write code that demonstrates the mistake and then show the corrected version.

??? success "Solution to Exercise 4"
    A common mistake is misunderstanding array shapes or dtypes. Always check `.shape` and `.dtype` when debugging unexpected results.
