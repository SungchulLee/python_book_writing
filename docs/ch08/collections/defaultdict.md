# defaultdict

A `defaultdict` is a dict subclass that automatically creates missing keys using a factory function.

!!! tip "Mental Model"
    A `defaultdict` is a dictionary that never says "key not found." When you access a missing key, it silently creates a default value (an empty list, zero, a new set — whatever factory you specified) and inserts it before returning. This eliminates the "check-then-initialize" pattern that clutters grouping and counting loops.

---

## The Problem

Regular dicts raise `KeyError` for missing keys:

```python
# Regular dict: must check or use setdefault
groups = {}
for name, category in data:
    if category not in groups:
        groups[category] = []
    groups[category].append(name)

# Or using setdefault (verbose)
groups = {}
for name, category in data:
    groups.setdefault(category, []).append(name)
```

---

## The Solution

```python
from collections import defaultdict

groups = defaultdict(list)
for name, category in data:
    groups[category].append(name)  # Auto-creates empty list!
```

---

## How It Works

```python
from collections import defaultdict

d = defaultdict(list)   # Factory function: list

# Accessing missing key:
# 1. Calls list() to create []
# 2. Assigns d['new_key'] = []
# 3. Returns the empty list

d['fruits'].append('apple')
print(d)  # defaultdict(<class 'list'>, {'fruits': ['apple']})
```

---

## Common Factory Functions

### `list` — Grouping

```python
from collections import defaultdict

data = [('apple', 'fruit'), ('carrot', 'vegetable'), 
        ('banana', 'fruit'), ('broccoli', 'vegetable')]

groups = defaultdict(list)
for item, category in data:
    groups[category].append(item)

print(dict(groups))
# {'fruit': ['apple', 'banana'], 'vegetable': ['carrot', 'broccoli']}
```

### `int` — Counting

```python
counts = defaultdict(int)  # int() returns 0

for char in 'mississippi':
    counts[char] += 1

print(dict(counts))
# {'m': 1, 'i': 4, 's': 4, 'p': 2}
```

### `set` — Unique Grouping

```python
tags = defaultdict(set)

data = [('doc1', 'python'), ('doc1', 'tutorial'), 
        ('doc2', 'python'), ('doc1', 'python')]  # duplicate

for doc, tag in data:
    tags[doc].add(tag)

print(dict(tags))
# {'doc1': {'python', 'tutorial'}, 'doc2': {'python'}}
```

### `lambda` — Custom Default

```python
# Default value 'N/A'
d = defaultdict(lambda: 'N/A')
d['name'] = 'Alice'
print(d['name'])    # Alice
print(d['age'])     # N/A

# Default value 0.0
prices = defaultdict(lambda: 0.0)
prices['apple'] = 1.50
print(prices['banana'])  # 0.0
```

---

## Nested defaultdict

### Two Levels

```python
# year -> month -> count
stats = defaultdict(lambda: defaultdict(int))

stats['2024']['Jan'] += 100
stats['2024']['Feb'] += 200
stats['2025']['Jan'] += 150

print(stats['2024']['Jan'])  # 100
print(stats['2024']['Mar'])  # 0 (auto-created)
```

### Three Levels

```python
# country -> city -> category -> count
data = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

data['USA']['NYC']['sales'] += 1000
data['USA']['NYC']['returns'] += 50
data['USA']['LA']['sales'] += 800
```

---

## Converting to Regular Dict

```python
d = defaultdict(list)
d['a'].append(1)
d['b'].append(2)

# Convert to regular dict
regular = dict(d)
print(regular)  # {'a': [1], 'b': [2]}

# Nested conversion
import json
print(json.dumps(dict(d)))  # Works after conversion
```

---

## defaultdict vs setdefault

| Aspect | `defaultdict` | `setdefault` |
|--------|---------------|--------------|
| Syntax | `d[key].append(x)` | `d.setdefault(key, []).append(x)` |
| Readability | ✅ Clean | ❌ Verbose |
| Creates on read | ✅ Yes | ❌ No |
| Regular dict | ❌ No | ✅ Yes |

```python
# defaultdict: creates key even on read
d = defaultdict(list)
_ = d['key']          # Creates empty list
print('key' in d)     # True

# setdefault: only creates on explicit call
d = {}
_ = d.get('key', [])  # Does NOT create
print('key' in d)     # False
```

---

## Practical Examples

### Word Index

```python
from collections import defaultdict

text = "the quick brown fox jumps over the lazy dog"
index = defaultdict(list)

for pos, word in enumerate(text.split()):
    index[word].append(pos)

print(dict(index))
# {'the': [0, 6], 'quick': [1], 'brown': [2], ...}
```

### Graph Adjacency List

```python
graph = defaultdict(list)

edges = [('A', 'B'), ('A', 'C'), ('B', 'C'), ('C', 'D')]
for src, dst in edges:
    graph[src].append(dst)
    graph[dst].append(src)  # Undirected

print(dict(graph))
# {'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['A', 'B', 'D'], 'D': ['C']}
```

### Frequency Table

```python
from collections import defaultdict

scores = [85, 90, 85, 78, 90, 90, 85]
freq = defaultdict(int)

for score in scores:
    freq[score] += 1

print(dict(freq))  # {85: 3, 90: 3, 78: 1}
```

---

## Key Takeaways

- `defaultdict(factory)` auto-creates missing keys
- Common factories: `list`, `int`, `set`, `lambda`
- Cleaner than `setdefault()` for grouping/counting
- Use `dict(d)` to convert to regular dict
- Accessing missing key creates it (unlike regular dict)

---

## Exercises

**Exercise 1.**
Write a function `invert_dict` that takes a regular dictionary and returns a `defaultdict(list)` where each value from the original dict becomes a key, and each key from the original dict is appended to the corresponding list. For example, `invert_dict({"a": 1, "b": 2, "c": 1})` should return `{1: ["a", "c"], 2: ["b"]}`.

??? success "Solution to Exercise 1"

    ```python
    from collections import defaultdict

    def invert_dict(d):
        result = defaultdict(list)
        for key, value in d.items():
            result[value].append(key)
        return result

    # Test
    original = {"a": 1, "b": 2, "c": 1}
    inverted = invert_dict(original)
    print(dict(inverted))
    # {1: ['a', 'c'], 2: ['b']}
    ```

---

**Exercise 2.**
Write a function `nested_group` that takes a list of `(department, team, employee)` tuples and returns a nested `defaultdict` structure where you can access employees as `result[department][team]` (a list). For example, given `[("eng", "backend", "Alice"), ("eng", "backend", "Bob"), ("eng", "frontend", "Carol")]`, `result["eng"]["backend"]` should return `["Alice", "Bob"]`.

??? success "Solution to Exercise 2"

    ```python
    from collections import defaultdict

    def nested_group(records):
        result = defaultdict(lambda: defaultdict(list))
        for department, team, employee in records:
            result[department][team].append(employee)
        return result

    # Test
    data = [
        ("eng", "backend", "Alice"),
        ("eng", "backend", "Bob"),
        ("eng", "frontend", "Carol"),
        ("sales", "west", "Dave"),
    ]
    groups = nested_group(data)
    print(groups["eng"]["backend"])   # ['Alice', 'Bob']
    print(groups["eng"]["frontend"])  # ['Carol']
    print(groups["sales"]["west"])    # ['Dave']
    ```

---

**Exercise 3.**
Write a function `word_positions` that takes a sentence string and returns a `defaultdict(list)` mapping each lowercase word to a list of its 0-based positions in the sentence. For example, `word_positions("the cat and the dog")` should return `{"the": [0, 3], "cat": [1], "and": [2], "dog": [4]}`.

??? success "Solution to Exercise 3"

    ```python
    from collections import defaultdict

    def word_positions(sentence):
        result = defaultdict(list)
        for pos, word in enumerate(sentence.lower().split()):
            result[word].append(pos)
        return result

    # Test
    positions = word_positions("the cat and the dog")
    print(dict(positions))
    # {'the': [0, 3], 'cat': [1], 'and': [2], 'dog': [4]}
    ```
