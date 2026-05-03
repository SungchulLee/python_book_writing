# Counter

A `Counter` is a dict subclass designed for counting hashable objects. It's the Pythonic way to do frequency analysis.

!!! tip "Mental Model"
    A `Counter` is a bag (multiset) that remembers how many of each item you dropped in. You toss items in, and it keeps a running tally — then you can ask questions like "what are the 3 most common?" or combine two bags with arithmetic. Wherever you would write a loop that increments a dictionary value, a `Counter` does it in one call.

---

## Creating Counters

```python
from collections import Counter

# From string
c = Counter('mississippi')
# Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# From list
c = Counter(['red', 'blue', 'red', 'green', 'blue', 'blue'])
# Counter({'blue': 3, 'red': 2, 'green': 1})

# From dict
c = Counter({'a': 4, 'b': 2})

# From keyword arguments
c = Counter(cats=4, dogs=2)
```

---

## Accessing Counts

```python
c = Counter('mississippi')

c['i']              # 4
c['s']              # 4
c['x']              # 0 (no KeyError!)
```

**Key difference from dict**: Missing keys return `0`, not `KeyError`.

---

## most_common()

Get elements sorted by frequency:

```python
c = Counter('mississippi')

c.most_common()     # [('i', 4), ('s', 4), ('p', 2), ('m', 1)]
c.most_common(2)    # [('i', 4), ('s', 4)] (top 2)
c.most_common()[:-3:-1]  # [('m', 1), ('p', 2)] (bottom 2)
```

---

## Updating Counts

### Add Counts

```python
c = Counter(a=3, b=1)
c.update({'a': 1, 'c': 2})
print(c)  # Counter({'a': 4, 'c': 2, 'b': 1})

c.update('aaa')  # From iterable
print(c)  # Counter({'a': 7, 'c': 2, 'b': 1})
```

### Subtract Counts

```python
c = Counter(a=4, b=2, c=0)
c.subtract({'a': 1, 'b': 3})
print(c)  # Counter({'a': 3, 'c': 0, 'b': -1})
```

**Note**: `subtract()` can result in negative counts.

---

## Counter Arithmetic

```python
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)

# Addition
c1 + c2             # Counter({'a': 4, 'b': 3})

# Subtraction (keeps positive only)
c1 - c2             # Counter({'a': 2})

# Intersection (min of each)
c1 & c2             # Counter({'a': 1, 'b': 1})

# Union (max of each)
c1 | c2             # Counter({'a': 3, 'b': 2})
```

---

## elements()

Returns an iterator over elements, repeating each by its count:

```python
c = Counter(a=3, b=2, c=1)
list(c.elements())  # ['a', 'a', 'a', 'b', 'b', 'c']

# Negative counts are ignored
c = Counter(a=2, b=-1)
list(c.elements())  # ['a', 'a']
```

---

## total() (Python 3.10+)

Sum of all counts:

```python
c = Counter(a=3, b=2, c=1)
c.total()           # 6
```

For earlier Python versions:

```python
sum(c.values())     # 6
```

---

## Practical Examples

### Word Frequency

```python
from collections import Counter

text = "the quick brown fox jumps over the lazy dog the fox"
words = text.lower().split()
word_counts = Counter(words)

print(word_counts.most_common(3))
# [('the', 3), ('fox', 2), ('quick', 1)]
```

### Character Frequency

```python
text = "Hello World"
char_counts = Counter(text.lower())
print(char_counts)
# Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})
```

### Finding Duplicates

```python
items = ['apple', 'banana', 'apple', 'cherry', 'banana', 'apple']
counts = Counter(items)

duplicates = [item for item, count in counts.items() if count > 1]
print(duplicates)  # ['apple', 'banana']
```

### Anagram Check

```python
def is_anagram(s1, s2):
    return Counter(s1.lower().replace(' ', '')) == Counter(s2.lower().replace(' ', ''))

print(is_anagram('listen', 'silent'))  # True
print(is_anagram('hello', 'world'))    # False
```

### Inventory Management

```python
inventory = Counter(apples=10, oranges=5, bananas=8)

# Sell items
sold = Counter(apples=3, oranges=2)
inventory.subtract(sold)
print(inventory)  # Counter({'bananas': 8, 'apples': 7, 'oranges': 3})

# Restock
restock = Counter(apples=5, grapes=10)
inventory.update(restock)
print(inventory)
# Counter({'apples': 12, 'grapes': 10, 'bananas': 8, 'oranges': 3})
```

### Vote Counting

```python
votes = ['Alice', 'Bob', 'Alice', 'Charlie', 'Alice', 'Bob']
results = Counter(votes)

winner = results.most_common(1)[0]
print(f"Winner: {winner[0]} with {winner[1]} votes")
# Winner: Alice with 3 votes
```

---

## Counter vs defaultdict(int)

| Feature | `Counter` | `defaultdict(int)` |
|---------|-----------|-------------------|
| Missing key | Returns 0 | Returns 0 |
| `most_common()` | ✅ Yes | ❌ No |
| Arithmetic (`+`, `-`) | ✅ Yes | ❌ No |
| `elements()` | ✅ Yes | ❌ No |
| `subtract()` | ✅ Yes | ❌ No |

**Use `Counter`** for counting tasks. Use `defaultdict(int)` only if you need dict-specific behavior.

---

## Key Takeaways

- `Counter` is optimized for counting hashable objects
- Missing keys return `0` (no KeyError)
- `most_common(n)` returns top n elements
- Supports arithmetic: `+`, `-`, `&`, `|`
- `elements()` iterates with repetition
- Perfect for frequency analysis, anagrams, voting, inventory

---

## Exercises

**Exercise 1.**
Write a function `common_elements` that takes two lists and returns a `Counter` containing only the elements common to both lists, with counts equal to the minimum count in either list. For example, `common_elements([1, 1, 2, 3], [1, 1, 1, 3, 3])` should return `Counter({1: 2, 3: 1})`. Hint: use Counter intersection.

??? success "Solution to Exercise 1"

    ```python
    from collections import Counter

    def common_elements(list1, list2):
        return Counter(list1) & Counter(list2)

    # Test
    result = common_elements([1, 1, 2, 3], [1, 1, 1, 3, 3])
    print(result)  # Counter({1: 2, 3: 1})

    result2 = common_elements(['a', 'b', 'b'], ['b', 'b', 'c'])
    print(result2)  # Counter({'b': 2})
    ```

---

**Exercise 2.**
Write a function `remove_duplicates_preserve_order` that takes a string and returns a new string with duplicate characters removed, keeping only the first occurrence of each character. Use `Counter` to identify which characters appear, but preserve the original order. For example, `remove_duplicates_preserve_order("abracadabra")` should return `"abrcd"`.

??? success "Solution to Exercise 2"

    ```python
    def remove_duplicates_preserve_order(text):
        seen = set()
        result = []
        for char in text:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return ''.join(result)

    # Test
    print(remove_duplicates_preserve_order("abracadabra"))  # "abrcd"
    print(remove_duplicates_preserve_order("mississippi"))   # "misp"
    ```

---

**Exercise 3.**
Write a function `can_construct` that takes two strings, `message` and `source`, and returns `True` if the `message` can be constructed using the characters from `source` (each character used at most as many times as it appears in `source`). For example, `can_construct("hello", "hellllooo")` returns `True`, but `can_construct("hello", "world")` returns `False`.

??? success "Solution to Exercise 3"

    ```python
    from collections import Counter

    def can_construct(message, source):
        message_counts = Counter(message)
        source_counts = Counter(source)
        # Check every character in message has enough in source
        return all(
            source_counts[char] >= count
            for char, count in message_counts.items()
        )

    # Test
    print(can_construct("hello", "hellllooo"))  # True
    print(can_construct("hello", "world"))       # False
    print(can_construct("aab", "aab"))           # True
    print(can_construct("aab", "ab"))            # False
    ```
