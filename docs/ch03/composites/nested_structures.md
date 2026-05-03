# Nested Structures

Composite data types can contain other composite types, creating hierarchical data structures. Understanding nested structures is essential for working with real-world data.

!!! tip "Mental Model"
    Nested structures are containers inside containers, like folders inside folders. Each level of nesting requires an additional index to reach (`matrix[row][col]`). The critical pitfall is shared references: `[[0]*3]*3` creates three references to the same inner list, while `[[0]*3 for _ in range(3)]` creates three independent lists.

## Nested Lists

Lists containing other lists form multi-dimensional structures.

### 1. Creating 2D Lists

Build matrices and grids using nested lists.

```python
# Direct creation
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Using comprehension
rows, cols = 3, 4
grid = [[0 for _ in range(cols)] for _ in range(rows)]
print(grid)
# [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
```

### 2. Accessing Elements

Use multiple indices to access nested elements.

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Single element
print(matrix[0][0])    # 1
print(matrix[1][2])    # 6

# Entire row
print(matrix[0])       # [1, 2, 3]

# Column (requires iteration)
col = [row[1] for row in matrix]
print(col)             # [2, 5, 8]
```

### 3. Common Pitfall

Avoid creating shared references when initializing.

```python
# Wrong: all rows share same list
bad_grid = [[0] * 3] * 3
bad_grid[0][0] = 1
print(bad_grid)
# [[1, 0, 0], [1, 0, 0], [1, 0, 0]]  # All changed!

# Correct: independent lists
good_grid = [[0] * 3 for _ in range(3)]
good_grid[0][0] = 1
print(good_grid)
# [[1, 0, 0], [0, 0, 0], [0, 0, 0]]  # Only first changed
```

## Nested Dicts

Dictionaries containing dictionaries model hierarchical data.

### 1. Creating Hierarchy

Build tree-like structures with nested dicts.

```python
# User profile
user = {
    "name": "Alice",
    "contact": {
        "email": "alice@example.com",
        "phone": "123-456-7890"
    },
    "address": {
        "city": "Seoul",
        "country": "Korea"
    }
}
```

### 2. Accessing Nested Values

Chain keys to access deeply nested data.

```python
user = {
    "name": "Bob",
    "settings": {
        "theme": "dark",
        "notifications": {
            "email": True,
            "sms": False
        }
    }
}

# Direct access
print(user["settings"]["theme"])              # dark
print(user["settings"]["notifications"]["email"])  # True

# Safe access with get()
print(user.get("settings", {}).get("language", "en"))  # en
```

### 3. Modifying Nested Data

Update values at any level of nesting.

```python
config = {
    "database": {
        "host": "localhost",
        "port": 5432
    }
}

# Update existing
config["database"]["port"] = 3306

# Add new nested key
config["database"]["user"] = "admin"

# Add new section
config["logging"] = {"level": "INFO"}

print(config)
# {'database': {'host': 'localhost', 'port': 3306, 'user': 'admin'},
#  'logging': {'level': 'INFO'}}
```

## Mixed Structures

Combine lists and dicts for flexible data modeling.

### 1. List of Dicts

Common pattern for collections of records.

```python
students = [
    {"name": "Alice", "score": 95},
    {"name": "Bob", "score": 87},
    {"name": "Carol", "score": 92}
]

# Access by index then key
print(students[0]["name"])  # Alice

# Iterate records
for s in students:
    print(f"{s['name']}: {s['score']}")
```

### 2. Dict of Lists

Store multiple values per key.

```python
grades = {
    "Alice": [95, 88, 92],
    "Bob": [87, 91, 85],
    "Carol": [92, 94, 90]
}

# Access all grades for one student
print(grades["Alice"])         # [95, 88, 92]

# Calculate averages
averages = {name: sum(g)/len(g) for name, g in grades.items()}
print(averages)
# {'Alice': 91.67, 'Bob': 87.67, 'Carol': 92.0}
```

### 3. Complex Hierarchies

Model real-world hierarchical data.

```python
company = {
    "name": "TechCorp",
    "departments": [
        {
            "name": "Engineering",
            "employees": [
                {"name": "Alice", "role": "Lead"},
                {"name": "Bob", "role": "Developer"}
            ]
        },
        {
            "name": "Sales",
            "employees": [
                {"name": "Carol", "role": "Manager"}
            ]
        }
    ]
}

# Navigate the hierarchy
eng = company["departments"][0]
lead = eng["employees"][0]["name"]
print(lead)  # Alice
```

## Iteration Patterns

Common patterns for traversing nested structures.

### 1. Nested Loops

Use nested loops for multi-level iteration.

```python
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Iterate all elements
for row in matrix:
    for val in row:
        print(val, end=" ")
    print()
# 1 2 3
# 4 5 6
# 7 8 9

# With indices
for i, row in enumerate(matrix):
    for j, val in enumerate(row):
        print(f"[{i},{j}]={val}", end=" ")
```

### 2. Recursive Traversal

Handle arbitrary nesting depth with recursion.

```python
def flatten(nested):
    """Flatten arbitrarily nested lists."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

data = [1, [2, 3], [4, [5, 6]], 7]
print(flatten(data))  # [1, 2, 3, 4, 5, 6, 7]
```

### 3. Dict Traversal

Recursively process nested dictionaries.

```python
def find_all_values(d, target_key):
    """Find all values for a key at any nesting level."""
    results = []
    for key, value in d.items():
        if key == target_key:
            results.append(value)
        if isinstance(value, dict):
            results.extend(find_all_values(value, target_key))
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    results.extend(find_all_values(item, target_key))
    return results

data = {
    "name": "Root",
    "children": [
        {"name": "Child1"},
        {"name": "Child2", "children": [{"name": "Grandchild"}]}
    ]
}
print(find_all_values(data, "name"))
# ['Root', 'Child1', 'Child2', 'Grandchild']
```

## Safe Access

Handle missing keys and indices gracefully.

### 1. Using get() Method

Provide defaults for missing dictionary keys.

```python
data = {"user": {"name": "Alice"}}

# Unsafe - raises KeyError
# print(data["user"]["email"])

# Safe with get()
email = data.get("user", {}).get("email", "N/A")
print(email)  # N/A

# Nested get pattern
def safe_get(d, *keys, default=None):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

print(safe_get(data, "user", "name"))     # Alice
print(safe_get(data, "user", "email"))    # None
```

### 2. Try-Except Pattern

Catch access errors for mixed structures.

```python
def safe_access(data, path):
    """Safely access nested data using path list."""
    try:
        result = data
        for key in path:
            result = result[key]
        return result
    except (KeyError, IndexError, TypeError):
        return None

data = {"items": [{"id": 1}, {"id": 2}]}

print(safe_access(data, ["items", 0, "id"]))   # 1
print(safe_access(data, ["items", 5, "id"]))   # None
print(safe_access(data, ["missing", "key"]))   # None
```

### 3. Default Factories

Use `defaultdict` for auto-creating nested levels.

```python
from collections import defaultdict

# Auto-create nested dicts
def nested_dict():
    return defaultdict(nested_dict)

data = nested_dict()
data["a"]["b"]["c"] = 1
print(data["a"]["b"]["c"])  # 1

# Auto-create lists
groups = defaultdict(list)
items = [("a", 1), ("b", 2), ("a", 3)]
for key, val in items:
    groups[key].append(val)
print(dict(groups))  # {'a': [1, 3], 'b': [2]}
```

## Copy Strategies

Create independent copies of nested structures.

### 1. Shallow vs Deep

Understand the difference between copy types.

```python
import copy

original = [[1, 2], [3, 4]]

# Shallow copy - nested lists are shared
shallow = original.copy()
shallow[0][0] = 99
print(original[0][0])  # 99 (changed!)

# Deep copy - fully independent
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 99
print(original[0][0])  # 1 (unchanged)
```

### 2. When to Use Each

Choose copy strategy based on mutation needs.

```python
import copy

# Shallow: when nested data won't be modified
config_template = {"name": "default", "options": [1, 2, 3]}
config = config_template.copy()
config["name"] = "custom"  # Safe, strings are immutable

# Deep: when nested data will be modified
config = copy.deepcopy(config_template)
config["options"].append(4)  # Safe, independent list
```

### 3. JSON Round-Trip

Alternative deep copy for JSON-serializable data.

```python
import json

original = {"nested": {"value": [1, 2, 3]}}

# JSON serialization creates deep copy
copied = json.loads(json.dumps(original))
copied["nested"]["value"].append(4)

print(original["nested"]["value"])  # [1, 2, 3]
print(copied["nested"]["value"])    # [1, 2, 3, 4]
```

---

## Exercises


**Exercise 1.**
Write a function `flatten(nested)` that takes an arbitrarily nested list and returns a flat list of all non-list elements. For example, `flatten([1, [2, [3, 4]], 5])` should return `[1, 2, 3, 4, 5]`.

??? success "Solution to Exercise 1"

        ```python
        def flatten(nested):
            result = []
            for item in nested:
                if isinstance(item, list):
                    result.extend(flatten(item))
                else:
                    result.append(item)
            return result

        print(flatten([1, [2, [3, 4]], 5]))  # [1, 2, 3, 4, 5]
        print(flatten([[1, 2], [3, [4, [5]]]]))  # [1, 2, 3, 4, 5]
        ```

    The function uses recursion to handle arbitrary nesting depth.

---

**Exercise 2.**
Given the nested dictionary below, write a function `safe_get(d, *keys, default=None)` that navigates the nested structure safely. It should return the value if all keys exist, or `default` otherwise.

```python
data = {"user": {"address": {"city": "Seoul"}}}
```

??? success "Solution to Exercise 2"

        ```python
        def safe_get(d, *keys, default=None):
            for key in keys:
                if isinstance(d, dict):
                    d = d.get(key, default)
                else:
                    return default
            return d

        data = {"user": {"address": {"city": "Seoul"}}}

        print(safe_get(data, "user", "address", "city"))     # Seoul
        print(safe_get(data, "user", "phone"))                # None
        print(safe_get(data, "missing", "key", default="N/A"))  # N/A
        ```

    The function chains `.get()` calls, returning the default if any key is missing.

---

**Exercise 3.**
Explain the common pitfall of `grid = [[0] * 3] * 3`. What happens when you set `grid[0][0] = 1`? Write the correct way to create a 3x3 grid of zeros.

??? success "Solution to Exercise 3"

    `[[0] * 3] * 3` creates three references to the same inner list. Modifying one row affects all rows:

        ```python
        bad_grid = [[0] * 3] * 3
        bad_grid[0][0] = 1
        print(bad_grid)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]

        # Correct way
        good_grid = [[0] * 3 for _ in range(3)]
        good_grid[0][0] = 1
        print(good_grid)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
        ```

    The list comprehension creates independent inner lists for each row.
