# dict Internals (Hash Tables)

Python dictionaries are implemented as hash tables, using hash functions to map keys to values with O(1) average lookup time. Understanding dict internals explains performance characteristics and behavioral quirks.

!!! tip "Mental Model"
    A dict is an array of slots indexed by hash values. To look up a key, Python computes its hash, jumps straight to the corresponding slot, and checks for a match. This is why lookups are O(1) on average and why keys must be hashable -- the hash is the address in the internal array.

---

## Hash Functions

### How Hashing Works

```python
# Hash of objects
print(f"Hash of 'key': {hash('key')}")
print(f"Hash of 42: {hash(42)}")
print(f"Hash of (1,2): {hash((1, 2))}")

# Lists can't be hashed (mutable)
try:
    hash([1, 2, 3])
except TypeError as e:
    print(f"Error: {e}")
```

Output:
```
Hash of 'key': 4567822475321
Hash of 42: 42
Hash of (1,2): 3713081631934410656
Error: unhashable type: 'list'
```

### Hash Collisions

```python
# Multiple keys can hash to same bucket
d = {}
d['a'] = 1
d['b'] = 2
d['c'] = 3

print(f"Dict size: {d}")
```

Output:
```
Dict size: {'a': 1, 'b': 2, 'c': 3}
```

## Dictionary Growth

### Dynamic Resizing

```python
d = {}
print(f"Initial capacity hint")

for i in range(10):
    d[f'key_{i}'] = i

print(f"Keys: {len(d)}")
print(f"Dict: {d}")
```

Output:
```
Initial capacity hint
Keys: 10
Dict: {'key_0': 0, 'key_1': 1, 'key_2': 2, 'key_3': 3, 'key_4': 4, 'key_5': 5, 'key_6': 6, 'key_7': 7, 'key_8': 8, 'key_9': 9}
```

## Performance Characteristics

### O(1) Lookup

```python
import time

d = {i: i**2 for i in range(100000)}

# Fast lookup
start = time.time()
for _ in range(1000):
    value = d[50000]
lookup_time = time.time() - start

print(f"Lookup time: {lookup_time:.6f}s")
```

Output:
```
Lookup time: 0.000045s
```

## Key Behavior

### Keys Must Be Hashable

```python
d = {(1, 2): "tuple_key"}
print(d[(1, 2)])

# This fails - lists aren't hashable
try:
    d[[1, 2]] = "list_key"
except TypeError:
    print("Lists cannot be dict keys")
```

Output:
```
tuple_key
Lists cannot be dict keys
```

---

## Exercises


**Exercise 1.**
Create a dictionary with keys `1`, `1.0`, and `True`. How many entries does the dictionary have? Explain why.

??? success "Solution to Exercise 1"

        ```python
        d = {1: "int", 1.0: "float", True: "bool"}
        print(d)       # {1: 'bool'}
        print(len(d))  # 1
        ```

    The dictionary has only 1 entry because `1 == 1.0 == True` and `hash(1) == hash(1.0) == hash(True)`. Python treats them as the same key, and each subsequent assignment overwrites the value.

---

**Exercise 2.**
Write a function `find_hash_collision()` that finds two different strings (among the first 100000 integers converted to strings) that have the same hash modulo 1000. Print both strings and their hash values.

??? success "Solution to Exercise 2"

        ```python
        def find_hash_collision():
            seen = {}
            for i in range(100000):
                s = str(i)
                h = hash(s) % 1000
                if h in seen:
                    print(f"'{seen[h]}' and '{s}' both hash to {h}")
                    return
                seen[h] = s

        find_hash_collision()
        ```

    Hash collisions are common when mapping to a small range. The function finds two strings whose hashes collide modulo 1000.

---

**Exercise 3.**
Demonstrate that looking up a key in a dictionary is O(1) by timing lookups in dictionaries of size 1000 and 1000000 and showing that the times are approximately equal.

??? success "Solution to Exercise 3"

        ```python
        import timeit

        setup_small = "d = {i: i for i in range(1_000)}"
        setup_large = "d = {i: i for i in range(1_000_000)}"

        t_small = timeit.timeit("999 in d", setup=setup_small, number=100000)
        t_large = timeit.timeit("999999 in d", setup=setup_large, number=100000)

        print(f"Small dict: {t_small:.4f}s")
        print(f"Large dict: {t_large:.4f}s")
        ```

    Both times should be approximately equal because dictionary lookup is O(1) regardless of size.
