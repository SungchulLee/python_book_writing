# collections Overview

The `collections` module provides specialized container types that extend Python's built-in `list`, `dict`, `tuple`, and `set`.

!!! tip "Mental Model"
    Think of `collections` as Python's toolbox of purpose-built containers. Just as a carpenter reaches for a chisel instead of a screwdriver when carving wood, you reach for `Counter`, `defaultdict`, or `deque` when the built-in types make a task awkward. Each type removes a specific category of boilerplate so your code reads closer to your intent.

---

## Why Use collections?

Built-in types are versatile, but specialized containers offer:

- **Cleaner code**: Less boilerplate for common patterns
- **Better performance**: Optimized for specific use cases
- **Safer defaults**: Avoid common pitfalls (e.g., KeyError)

---

## Available Types

| Type | Description | Replaces |
|------|-------------|----------|
| `namedtuple` | Tuple with named fields | Plain tuple, simple class |
| `defaultdict` | Dict with default factory | Dict + `setdefault()` |
| `Counter` | Dict for counting | Dict + manual counting |
| `deque` | Double-ended queue | List (for queue operations) |
| `OrderedDict` | Dict with ordering features | Dict (mostly) |
| `ChainMap` | Multiple dicts as one view | Manual dict merging |

---

## Quick Comparison

### Without collections

```python
# Counting
counts = {}
for item in items:
    if item not in counts:
        counts[item] = 0
    counts[item] += 1

# Grouping
groups = {}
for item in items:
    key = get_key(item)
    if key not in groups:
        groups[key] = []
    groups[key].append(item)

# Queue operations (slow!)
queue = []
queue.append(item)      # O(1)
queue.pop(0)            # O(n) - shifts all elements
```

### With collections

```python
from collections import Counter, defaultdict, deque

# Counting
counts = Counter(items)

# Grouping
groups = defaultdict(list)
for item in items:
    groups[get_key(item)].append(item)

# Queue operations (fast!)
queue = deque()
queue.append(item)      # O(1)
queue.popleft()         # O(1)
```

---

## Import Patterns

```python
# Import specific types
from collections import namedtuple, defaultdict, Counter, deque

# Or import module
import collections
d = collections.defaultdict(list)
```

---

## When to Use Each

| Use Case | Type |
|----------|------|
| Lightweight record/struct | `namedtuple` |
| Grouping items by key | `defaultdict(list)` |
| Counting occurrences | `Counter` |
| Queue / BFS / sliding window | `deque` |
| LRU cache implementation | `OrderedDict` |
| Config layering | `ChainMap` |

---

## Summary

The `collections` module is essential for writing clean, efficient Python code. Master these types to avoid reinventing common patterns.

---

## Exercises

**Exercise 1.**
Write a function `count_word_lengths` that takes a list of words and returns a `defaultdict(list)` mapping each word length (int) to the list of words with that length. For example, `count_word_lengths(["hi", "hey", "hello", "go"])` should return `{2: ["hi", "go"], 3: ["hey"], 5: ["hello"]}`.

??? success "Solution to Exercise 1"

    ```python
    from collections import defaultdict

    def count_word_lengths(words):
        result = defaultdict(list)
        for word in words:
            result[len(word)].append(word)
        return result

    # Test
    words = ["hi", "hey", "hello", "go"]
    result = count_word_lengths(words)
    for length, word_list in sorted(result.items()):
        print(f"Length {length}: {word_list}")
    # Length 2: ['hi', 'go']
    # Length 3: ['hey']
    # Length 5: ['hello']
    ```

---

**Exercise 2.**
Using `Counter`, write a function `top_n_chars` that takes a string and an integer `n`, and returns the `n` most common characters (excluding spaces) as a list of `(char, count)` tuples. For example, `top_n_chars("banana split", 2)` should return `[('a', 3), ('n', 2)]`.

??? success "Solution to Exercise 2"

    ```python
    from collections import Counter

    def top_n_chars(text, n):
        cleaned = text.replace(" ", "")
        counter = Counter(cleaned)
        return counter.most_common(n)

    # Test
    print(top_n_chars("banana split", 2))
    # [('a', 3), ('n', 2)]
    print(top_n_chars("mississippi", 3))
    # [('s', 4), ('i', 4), ('p', 2)]
    ```

---

**Exercise 3.**
Write a function `recent_commands` that simulates a command history using a `deque` with `maxlen=5`. The function takes a list of command strings and returns the deque after all commands have been appended. For example, `recent_commands(["ls", "cd", "pwd", "cat", "echo", "grep"])` should return a deque containing `["cd", "pwd", "cat", "echo", "grep"]`.

??? success "Solution to Exercise 3"

    ```python
    from collections import deque

    def recent_commands(commands):
        history = deque(maxlen=5)
        for cmd in commands:
            history.append(cmd)
        return history

    # Test
    cmds = ["ls", "cd", "pwd", "cat", "echo", "grep"]
    result = recent_commands(cmds)
    print(result)
    # deque(['cd', 'pwd', 'cat', 'echo', 'grep'], maxlen=5)
    print(len(result))  # 5
    ```
