# sorted() and Sorting

The `sorted()` function returns a new sorted list from any iterable. Understanding sorting keys and custom comparisons is essential for data manipulation.

!!! tip "Mental Model"
    `sorted()` never touches the original data -- it always hands you a brand-new list in order. The `key` parameter is a lens: it tells `sorted()` what aspect of each element to compare, without changing the elements themselves. Master `key` and you can sort anything by any criterion in a single call.

---

## Basic Usage

### sorted() Returns New List

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]
result = sorted(numbers)

print(result)   # [1, 1, 2, 3, 4, 5, 6, 9]
print(numbers)  # [3, 1, 4, 1, 5, 9, 2, 6] (unchanged)
```

### Works on Any Iterable

```python
# Strings
sorted("python")           # ['h', 'n', 'o', 'p', 't', 'y']

# Tuples
sorted((3, 1, 2))          # [1, 2, 3]

# Sets
sorted({3, 1, 2})          # [1, 2, 3]

# Dictionaries (sorts keys)
sorted({'c': 3, 'a': 1})   # ['a', 'c']

# Generators
sorted(x**2 for x in [3, 1, 2])  # [1, 4, 9]
```

---

## sorted() vs list.sort()

| Feature | `sorted()` | `list.sort()` |
|---------|-----------|---------------|
| Returns | New list | `None` (in-place) |
| Works on | Any iterable | Lists only |
| Original | Unchanged | Modified |
| Memory | Creates copy | No extra memory |

```python
# sorted() - creates new list
original = [3, 1, 2]
new_list = sorted(original)
print(original)  # [3, 1, 2] (unchanged)

# list.sort() - modifies in place
original = [3, 1, 2]
result = original.sort()
print(result)    # None
print(original)  # [1, 2, 3] (modified)
```

---

## Reverse Sorting

```python
numbers = [3, 1, 4, 1, 5]

# Descending order
sorted(numbers, reverse=True)  # [5, 4, 3, 1, 1]

# Also works with list.sort()
numbers.sort(reverse=True)
```

---

## The key Parameter

The `key` parameter specifies a function to extract a comparison key from each element.

### Sort by Length

```python
words = ['banana', 'pie', 'apple', 'fig']

sorted(words, key=len)
# ['pie', 'fig', 'apple', 'banana']
```

### Sort Case-Insensitive

```python
names = ['Bob', 'alice', 'Charlie', 'david']

# Default: uppercase before lowercase
sorted(names)              # ['Bob', 'Charlie', 'alice', 'david']

# Case-insensitive
sorted(names, key=str.lower)  # ['alice', 'Bob', 'Charlie', 'david']
```

### Sort by Absolute Value

```python
numbers = [-5, 2, -1, 4, -3]

sorted(numbers, key=abs)   # [-1, 2, -3, 4, -5]
```

### Sort with Lambda

```python
pairs = [(1, 'b'), (3, 'a'), (2, 'c')]

# Sort by second element
sorted(pairs, key=lambda x: x[1])
# [(3, 'a'), (1, 'b'), (2, 'c')]

# Sort by first element (default behavior)
sorted(pairs, key=lambda x: x[0])
# [(1, 'b'), (2, 'c'), (3, 'a')]
```

---

## Sorting Dictionaries

### Sort by Keys

```python
scores = {'Bob': 85, 'Alice': 92, 'Charlie': 78}

# Sorted keys
sorted(scores)                    # ['Alice', 'Bob', 'Charlie']

# Sorted items by key
sorted(scores.items())            # [('Alice', 92), ('Bob', 85), ('Charlie', 78)]
```

### Sort by Values

```python
scores = {'Bob': 85, 'Alice': 92, 'Charlie': 78}

# Sort by value (ascending)
sorted(scores.items(), key=lambda x: x[1])
# [('Charlie', 78), ('Bob', 85), ('Alice', 92)]

# Sort by value (descending)
sorted(scores.items(), key=lambda x: x[1], reverse=True)
# [('Alice', 92), ('Bob', 85), ('Charlie', 78)]
```

### Create Sorted Dictionary (Python 3.7+)

```python
scores = {'Bob': 85, 'Alice': 92, 'Charlie': 78}

sorted_dict = dict(sorted(scores.items(), key=lambda x: x[1]))
# {'Charlie': 78, 'Bob': 85, 'Alice': 92}
```

---

## Sorting Objects

### Using Attributes

```python
class Student:
    def __init__(self, name, grade, age):
        self.name = name
        self.grade = grade
        self.age = age
    
    def __repr__(self):
        return f"Student({self.name}, {self.grade})"

students = [
    Student('Alice', 85, 20),
    Student('Bob', 92, 19),
    Student('Charlie', 85, 21),
]

# Sort by grade
sorted(students, key=lambda s: s.grade)
# [Student(Alice, 85), Student(Charlie, 85), Student(Bob, 92)]

# Sort by name
sorted(students, key=lambda s: s.name)
# [Student(Alice, 85), Student(Bob, 92), Student(Charlie, 85)]
```

### Using operator.attrgetter

```python
from operator import attrgetter

# Cleaner than lambda for attribute access
sorted(students, key=attrgetter('grade'))
sorted(students, key=attrgetter('name'))

# Multiple attributes
sorted(students, key=attrgetter('grade', 'age'))
```

### Using operator.itemgetter

```python
from operator import itemgetter

# For dictionaries or tuples
records = [
    {'name': 'Alice', 'score': 85},
    {'name': 'Bob', 'score': 92},
]

sorted(records, key=itemgetter('score'))
# [{'name': 'Alice', 'score': 85}, {'name': 'Bob', 'score': 92}]

# For tuples
pairs = [(1, 'b'), (3, 'a'), (2, 'c')]
sorted(pairs, key=itemgetter(1))  # [(3, 'a'), (1, 'b'), (2, 'c')]
```

---

## Multi-Key Sorting

### Using Tuples

```python
students = [
    ('Alice', 85),
    ('Bob', 92),
    ('Charlie', 85),
]

# Sort by grade, then by name
sorted(students, key=lambda x: (x[1], x[0]))
# [('Alice', 85), ('Charlie', 85), ('Bob', 92)]

# Sort by grade descending, name ascending
sorted(students, key=lambda x: (-x[1], x[0]))
# [('Bob', 92), ('Alice', 85), ('Charlie', 85)]
```

### Multiple Sorts (Stable Sort)

Python's sort is **stable**—equal elements keep their relative order. Use this for multi-key sorting:

```python
students = [
    ('Alice', 85),
    ('Bob', 92),
    ('Charlie', 85),
]

# Sort by name first, then by grade
# (because stable sort preserves order of equal elements)
result = sorted(students, key=lambda x: x[0])  # by name
result = sorted(result, key=lambda x: x[1])    # by grade

# Result: [('Alice', 85), ('Charlie', 85), ('Bob', 92)]
```

---

## Special Cases

### Sorting None Values

```python
data = [3, None, 1, None, 2]

# This fails!
# sorted(data)  # TypeError: '<' not supported between 'int' and 'NoneType'

# Put None values at end
sorted(data, key=lambda x: (x is None, x))
# [1, 2, 3, None, None]

# Put None values at beginning
sorted(data, key=lambda x: (x is not None, x))
# [None, None, 1, 2, 3]
```

### Sorting Mixed Types (Python 3)

```python
# Python 3 doesn't allow mixed type comparison
mixed = [1, 'a', 2, 'b']
# sorted(mixed)  # TypeError

# Convert to common type
sorted(mixed, key=str)  # [1, 2, 'a', 'b']
```

### Natural Sorting (Numeric Strings)

```python
files = ['file1.txt', 'file10.txt', 'file2.txt', 'file20.txt']

# Default: lexicographic (wrong for numbers)
sorted(files)
# ['file1.txt', 'file10.txt', 'file2.txt', 'file20.txt']

# Natural sort
import re
def natural_key(s):
    return [int(c) if c.isdigit() else c.lower() 
            for c in re.split(r'(\d+)', s)]

sorted(files, key=natural_key)
# ['file1.txt', 'file2.txt', 'file10.txt', 'file20.txt']
```

---

## Performance

### Time Complexity

- **Best case**: O(n) — already sorted
- **Average/Worst case**: O(n log n)
- **Space**: O(n) for `sorted()`, O(1) for `list.sort()`

### Tips

```python
# Avoid sorting repeatedly
data = [...]
sorted_data = sorted(data)  # Sort once, use many times

# Use key functions efficiently
# Good: simple attribute access
sorted(items, key=lambda x: x.value)

# Bad: expensive computation in key
sorted(items, key=lambda x: expensive_function(x))

# Better: precompute if sorting repeatedly
decorated = [(expensive_function(x), x) for x in items]
decorated.sort()
result = [x for _, x in decorated]
```

---

## Summary

| Task | Code |
|------|------|
| Basic sort | `sorted(items)` |
| Reverse | `sorted(items, reverse=True)` |
| By length | `sorted(items, key=len)` |
| Case-insensitive | `sorted(items, key=str.lower)` |
| By attribute | `sorted(items, key=attrgetter('attr'))` |
| By dict key | `sorted(items, key=itemgetter('key'))` |
| Multi-key | `sorted(items, key=lambda x: (x.a, x.b))` |
| Descending + ascending | `sorted(items, key=lambda x: (-x.a, x.b))` |

**Key Takeaways**:

- `sorted()` returns a new list; `list.sort()` modifies in place
- Use `key` parameter for custom sort orders
- `operator.attrgetter` and `itemgetter` are cleaner than lambdas
- Python's sort is stable—use for multi-key sorting
- Use tuple keys for multiple sort criteria
- Negate numeric values for mixed ascending/descending sorts

---

## Exercises


**Exercise 1.**
Given a list of tuples representing students and their scores, sort them by score in descending order. If two students have the same score, sort them alphabetically by name.

```python
students = [("Alice", 88), ("Bob", 95), ("Carol", 88), ("Dave", 95)]
```

??? success "Solution to Exercise 1"

        ```python
        students = [("Alice", 88), ("Bob", 95), ("Carol", 88), ("Dave", 95)]

        result = sorted(students, key=lambda s: (-s[1], s[0]))
        print(result)
        # [('Bob', 95), ('Dave', 95), ('Alice', 88), ('Carol', 88)]
        ```

    Negating the score (`-s[1]`) sorts scores in descending order. The name `s[0]` serves as the tiebreaker and sorts alphabetically in ascending order.

---

**Exercise 2.**
Write a function `sort_by_last_word(sentences)` that takes a list of strings and returns them sorted by their last word (case-insensitive). For example, `["Hello World", "Foo Bar", "Python Alpha"]` should be sorted by `"World"`, `"Bar"`, `"Alpha"`.

??? success "Solution to Exercise 2"

        ```python
        def sort_by_last_word(sentences):
            return sorted(sentences, key=lambda s: s.split()[-1].lower())

        result = sort_by_last_word(["Hello World", "Foo Bar", "Python Alpha"])
        print(result)
        # ['Python Alpha', 'Foo Bar', 'Hello World']
        ```

    `s.split()[-1]` extracts the last word, and `.lower()` makes the comparison case-insensitive.

---

**Exercise 3.**
Explain the difference between `sorted()` and `list.sort()`. Write a code example that demonstrates that `sorted()` returns a new list while `list.sort()` modifies the list in place and returns `None`.

??? success "Solution to Exercise 3"

        ```python
        original = [3, 1, 2]

        # sorted() returns a new list
        new_list = sorted(original)
        print(new_list)    # [1, 2, 3]
        print(original)    # [3, 1, 2] (unchanged)

        # list.sort() modifies in place and returns None
        result = original.sort()
        print(result)      # None
        print(original)    # [1, 2, 3] (modified)
        ```

    `sorted()` creates and returns a new list, leaving the original unchanged. `list.sort()` sorts the list in place and returns `None` -- a common source of bugs when developers write `x = my_list.sort()` expecting to get the sorted list.
