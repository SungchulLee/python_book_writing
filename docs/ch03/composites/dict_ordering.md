# dict Ordering Guarantees

Since Python 3.7, dictionaries guarantee insertion order preservation as a language feature (not just implementation detail). This makes dicts suitable for ordered key-value collections and simplifies many programming patterns.

!!! tip "Mental Model"
    A Python dict remembers the order in which you inserted keys, much like a guest book that records arrivals in sequence. Updating an existing key changes its value but keeps its position; only deleting and re-inserting moves a key to the end. Since Python 3.7, this order guarantee is part of the language specification.

---

## Insertion Order Preservation

### Order is Guaranteed

```python
d = {}
d['z'] = 1
d['a'] = 2
d['m'] = 3

for key in d:
    print(key)
```

Output:
```
z
a
m
```

### Items Maintain Order

```python
d = {'zebra': 1, 'apple': 2, 'mango': 3}

print("Keys:", list(d.keys()))
print("Values:", list(d.values()))
print("Items:", list(d.items()))
```

Output:
```
Keys: ['zebra', 'apple', 'mango']
Values: [1, 2, 3]
Items: [('zebra', 1), ('apple', 2), ('mango', 3)]
```

## Practical Benefits

### Iteration Order is Predictable

```python
config = {
    'host': 'localhost',
    'port': 8000,
    'debug': True,
    'timeout': 30
}

for setting, value in config.items():
    print(f"{setting}: {value}")
```

Output:
```
host: localhost
port: 8000
debug: True
timeout: 30
```

### First/Last Access

```python
d = {'first': 1, 'second': 2, 'third': 3}

first_key = next(iter(d))
last_key = next(reversed(d))

print(f"First: {first_key}")
print(f"Last: {last_key}")
```

Output:
```
First: first
Last: third
```

## Update Behavior

### Order After Updates

```python
d = {'a': 1, 'b': 2}
d['c'] = 3
d['a'] = 10  # Update doesn't change position

print(list(d.keys()))
```

Output:
```
['a', 'b', 'c']
```

### Deletion and Reinsertion

```python
d = {'a': 1, 'b': 2, 'c': 3}
del d['b']
d['b'] = 20

print(list(d.keys()))
```

Output:
```
['a', 'c', 'b']
```

---

## Exercises


**Exercise 1.**
Create a dictionary with keys inserted in the order `"z"`, `"a"`, `"m"`. Verify that iterating over the dictionary yields the keys in insertion order. Then delete `"a"` and re-insert it. What order do the keys appear in now?

??? success "Solution to Exercise 1"

        ```python
        d = {}
        d["z"] = 1
        d["a"] = 2
        d["m"] = 3
        print(list(d.keys()))  # ['z', 'a', 'm']

        del d["a"]
        d["a"] = 2
        print(list(d.keys()))  # ['z', 'm', 'a']
        ```

    Deleting and re-inserting a key places it at the end. Updating an existing key's value does not change its position.

---

**Exercise 2.**
Write a function `move_to_front(d, key)` that takes a dictionary and a key, and returns a new dictionary with that key moved to the front (first position), preserving the relative order of all other keys.

??? success "Solution to Exercise 2"

        ```python
        def move_to_front(d, key):
            if key not in d:
                return dict(d)
            return {key: d[key], **{k: v for k, v in d.items() if k != key}}

        d = {"a": 1, "b": 2, "c": 3}
        print(move_to_front(d, "c"))  # {'c': 3, 'a': 1, 'b': 2}
        ```

    The function creates a new dict with `key` first, followed by all other items in their original order.

---

**Exercise 3.**
Using `next(iter(d))` and `next(reversed(d))`, write a function `first_and_last(d)` that returns a tuple of the first and last key-value pairs of a dictionary.

??? success "Solution to Exercise 3"

        ```python
        def first_and_last(d):
            first_key = next(iter(d))
            last_key = next(reversed(d))
            return (first_key, d[first_key]), (last_key, d[last_key])

        d = {"x": 10, "y": 20, "z": 30}
        first, last = first_and_last(d)
        print(f"First: {first}")  # First: ('x', 10)
        print(f"Last: {last}")    # Last: ('z', 30)
        ```

    `iter(d)` starts from the first key, `reversed(d)` starts from the last. Both are O(1) operations.
