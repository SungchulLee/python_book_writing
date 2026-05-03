# dict Merge Operators

Python 3.9+ introduced the | and |= operators for merging dictionaries, providing a cleaner syntax than update() and providing merge semantics. This is part of PEP 584 and improves dict manipulation.

!!! tip "Mental Model"
    Think of `|` as layering two transparencies: the left dict goes down first, then the right dict goes on top. Where keys overlap, the right side wins. `|` produces a new dict (like `+` for lists), while `|=` updates the left dict in place (like `+=` for lists).

---

## The | Operator (Merge)

### Basic Dict Merging

```python
d1 = {'a': 1, 'b': 2}
d2 = {'c': 3, 'd': 4}

merged = d1 | d2
print(merged)
```

Output:
```
{'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

### Right Side Overwrites

```python
d1 = {'a': 1, 'b': 2}
d2 = {'b': 20, 'c': 3}

merged = d1 | d2
print(merged)
```

Output:
```
{'a': 1, 'b': 20, 'c': 3}
```

## The |= Operator (In-Place Merge)

### Updating a Dictionary

```python
d = {'a': 1, 'b': 2}
d |= {'c': 3, 'd': 4}
print(d)
```

Output:
```
{'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

### Overwriting Values

```python
d = {'a': 1, 'b': 2}
d |= {'b': 20, 'c': 3}
print(d)
```

Output:
```
{'a': 1, 'b': 20, 'c': 3}
```

## Practical Applications

### Configuration Merging

```python
defaults = {'host': 'localhost', 'port': 8000, 'debug': False}
custom = {'port': 5000, 'debug': True}

config = defaults | custom
print(config)
```

Output:
```
{'host': 'localhost', 'port': 5000, 'debug': True}
```

### Layered Configuration

```python
system = {'theme': 'dark', 'language': 'en'}
user = {'theme': 'light'}
session = {'theme': 'auto'}

final = system | user | session
print(final)
```

Output:
```
{'theme': 'auto', 'language': 'en'}
```

## Comparison with update()

### | Creates New Dict

```python
d1 = {'a': 1, 'b': 2}
d2 = {'c': 3}

d3 = d1 | d2
print(f"d1: {d1}")
print(f"d3: {d3}")
print(f"d1 unchanged: {d1 is not d3}")
```

Output:
```
d1: {'a': 1, 'b': 2}
d3: {'a': 1, 'b': 2, 'c': 3}
d1 unchanged: True
```

---

## Exercises


**Exercise 1.**
Given two dictionaries `defaults = {"color": "red", "size": 10}` and `custom = {"size": 20, "font": "Arial"}`, merge them so that `custom` values take priority. Show two approaches: one using `|` and one using `{**d1, **d2}`.

??? success "Solution to Exercise 1"

        ```python
        defaults = {"color": "red", "size": 10}
        custom = {"size": 20, "font": "Arial"}

        # Using | (Python 3.9+)
        merged1 = defaults | custom
        print(merged1)  # {'color': 'red', 'size': 20, 'font': 'Arial'}

        # Using ** unpacking
        merged2 = {**defaults, **custom}
        print(merged2)  # {'color': 'red', 'size': 20, 'font': 'Arial'}
        ```

    Both approaches give `custom` priority. The rightmost dictionary's values win for duplicate keys.

---

**Exercise 2.**
Write a function `deep_merge(d1, d2)` that merges two dictionaries recursively. If both values for a key are dictionaries, merge them recursively. Otherwise, `d2`'s value wins.

??? success "Solution to Exercise 2"

        ```python
        def deep_merge(d1, d2):
            result = d1.copy()
            for key, value in d2.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        a = {"db": {"host": "localhost", "port": 5432}, "debug": True}
        b = {"db": {"port": 3306, "user": "admin"}, "debug": False}

        print(deep_merge(a, b))
        # {'db': {'host': 'localhost', 'port': 3306, 'user': 'admin'}, 'debug': False}
        ```

    The recursive approach preserves nested keys from both dictionaries while letting `d2` values take priority.

---

**Exercise 3.**
Demonstrate the difference between `d1 | d2` (creates new dict) and `d1 |= d2` (updates in place) by showing that one changes the original dictionary and the other does not.

??? success "Solution to Exercise 3"

        ```python
        d1 = {"a": 1, "b": 2}
        d2 = {"b": 3, "c": 4}

        # | creates a new dict
        d3 = d1 | d2
        print(d1)  # {'a': 1, 'b': 2} (unchanged)
        print(d3)  # {'a': 1, 'b': 3, 'c': 4}

        # |= updates in place
        original_id = id(d1)
        d1 |= d2
        print(d1)  # {'a': 1, 'b': 3, 'c': 4} (modified)
        print(id(d1) == original_id)  # True (same object)
        ```

    `|` returns a new dictionary, leaving originals intact. `|=` modifies the left-hand dictionary in place.
