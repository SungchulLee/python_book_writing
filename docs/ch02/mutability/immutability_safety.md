
# Why Immutability Is Useful

Immutability might seem like a limitation---why would you want objects that cannot change? In
practice, immutability is a powerful tool. It provides guarantees that make code safer, more
predictable, and easier to reason about.

The mental model: mutable objects are like shared whiteboards in a busy office. Anyone can walk
up and erase or rewrite content, and everyone else sees the change immediately. Immutable objects
are like laminated reference cards. They cannot be altered, so you can hand them out freely
without worrying that someone will modify your copy.

!!! tip "Mental Model"
    Immutability is a guarantee that an object will never change once created. This guarantee unlocks hashability for dict keys and sets, eliminates surprise mutations from aliasing, and makes code easier to reason about because you never have to ask "could something else have changed this?"

---

## 1. Hashability: Dict Keys and Set Elements

Python dictionaries and sets rely on hash tables internally. A hash table computes a numeric
fingerprint (hash) of each key and uses it to find the right storage slot. If a key could change
after insertion, its hash would no longer match its slot, and lookups would silently fail.

For this reason, Python requires that dictionary keys and set elements be **hashable**, and
mutable objects are generally not hashable.

```python
d = {}
d["name"] = "Alice"       # str is immutable and hashable
d[(1, 2)] = "coordinates" # tuple of ints is hashable

print(d)
```

Output:

```text
{'name': 'Alice', (1, 2): 'coordinates'}
```

Attempting to use a mutable object as a key fails.

```python
d = {}
d[[1, 2]] = "coordinates"
```

Output:

```text
TypeError: unhashable type: 'list'
```

The same rule applies to set elements.

```python
s = {1, "hello", (2, 3)}  # all hashable
print(s)
```

Output:

```text
{1, (2, 3), 'hello'}
```

```python
s = {[1, 2]}
```

Output:

```text
TypeError: unhashable type: 'list'
```

---

## 2. Tuples as Dictionary Keys

Tuples are immutable, so they can serve as dictionary keys---provided all their elements are
also hashable. This is useful for composite keys.

```python
distances = {}
distances[("New York", "Boston")] = 306
distances[("Boston", "Chicago")] = 1366

print(distances[("New York", "Boston")])
```

Output:

```text
306
```

A tuple containing a mutable element is **not** hashable.

```python
d = {}
d[([1, 2], "a")] = "value"
```

Output:

```text
TypeError: unhashable type: 'list'
```

The tuple itself is immutable, but because it contains a list, its hash cannot be reliably
computed. Python rejects it.

---

## 3. Frozenset: The Immutable Set

A `frozenset` is an immutable version of `set`. It supports the same lookup and set-algebra
operations but cannot be modified after creation.

```python
fs = frozenset([1, 2, 3])
print(fs)
print(3 in fs)
```

Output:

```text
frozenset({1, 2, 3})
True
```

Because `frozenset` is immutable, it is hashable and can be used as a dictionary key or a
member of another set.

```python
# frozenset as a dict key
groups = {}
groups[frozenset(["Alice", "Bob"])] = "Team A"
print(groups)

# frozenset as a set element
collection = {frozenset([1, 2]), frozenset([3, 4])}
print(collection)
```

Output:

```text
{frozenset({'Alice', 'Bob'}): 'Team A'}
{frozenset({1, 2}), frozenset({3, 4})}
```

Attempting to modify a `frozenset` raises an error.

```python
fs = frozenset([1, 2, 3])
fs.add(4)
```

Output:

```text
AttributeError: 'frozenset' object has no attribute 'add'
```

---

## 4. Preventing Accidental Changes

When you pass a mutable object to a function, the function receives a reference to the **same**
object. If the function modifies it, the caller sees the change. This can cause hard-to-find
bugs.

```python
def process(items):
    items.sort()
    return items[:3]

original = [5, 3, 8, 1, 9, 2]
top_three = process(original)

print(top_three)
print(original)
```

Output:

```text
[1, 2, 3]
[1, 2, 3, 5, 8, 9]
```

The caller's `original` list was sorted as a side effect. The function did not intend to modify
it, but `sort()` acts in place. Using an immutable type (or a copy) prevents this.

---

## 5. Defensive Copying

When you need to protect a mutable object from unintended modification, create a copy before
passing it around.

### Using list() or slicing

```python
def process(items):
    working = list(items)  # or items[:]
    working.sort()
    return working[:3]

original = [5, 3, 8, 1, 9, 2]
top_three = process(original)

print(top_three)
print(original)
```

Output:

```text
[1, 2, 3]
[5, 3, 8, 1, 9, 2]
```

Now `original` is untouched because the function works on an independent copy.

### Using copy()

The `copy` module provides `copy()` for shallow copies and `deepcopy()` for nested structures.

```python
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

original[0].append(99)

print(shallow)
print(deep)
```

Output:

```text
[[1, 2, 99], [3, 4]]
[[1, 2], [3, 4]]
```

The shallow copy shares the inner lists with the original. The deep copy is fully independent.

### Using dict() for dictionaries

```python
def add_defaults(config):
    safe = dict(config)
    safe.setdefault("timeout", 30)
    safe.setdefault("retries", 3)
    return safe

original = {"host": "localhost", "port": 8080}
full = add_defaults(original)

print(original)
print(full)
```

Output:

```text
{'host': 'localhost', 'port': 8080}
{'host': 'localhost', 'port': 8080, 'timeout': 30, 'retries': 3}
```

---

## 6. Thread Safety

In concurrent programs, multiple threads may access the same data simultaneously. Mutable
shared state requires careful synchronization (locks, semaphores) to prevent race conditions.
Immutable objects sidestep this problem entirely: since they cannot change, concurrent reads
are always safe.

```python
# Immutable data shared between threads needs no lock
SETTINGS = ("localhost", 8080, "/api")

# Mutable data shared between threads requires synchronization
import threading
lock = threading.Lock()
shared_list = []

def worker(value):
    with lock:
        shared_list.append(value)
```

Preferring immutable data structures reduces the surface area for concurrency bugs.

---

## 7. When to Choose Immutable Over Mutable

| Situation | Prefer |
| --------- | ------ |
| Need a dictionary key or set element | Immutable (`tuple`, `frozenset`, `str`) |
| Data should not change after creation | Immutable |
| Sharing data across functions or threads | Immutable (or defensive copy) |
| Building up a collection incrementally | Mutable (`list`, `dict`, `set`) |
| Frequent additions/removals | Mutable |
| Performance-sensitive tight loops | Profile both; neither is universally faster |

The general principle: **start with immutable unless you have a specific reason to mutate**.
This makes your code's intent clearer and prevents accidental modification.

---

## 8. Summary

Key ideas:

- Immutable objects are hashable (assuming all contents are also hashable), making them valid
  as dictionary keys and set elements.
- Tuples and frozensets provide immutable alternatives to lists and sets.
- Passing mutable objects to functions risks accidental modification. Defensive copying with
  `list()`, `dict()`, slicing, or `copy.deepcopy()` protects the original.
- Immutable objects are inherently thread-safe because concurrent reads cannot conflict.
- Default to immutable types when the data does not need to change. Use mutable types when
  you genuinely need in-place modification.

---

## Exercises

**Exercise 1.**
A programmer wants to use a list of coordinates as a dictionary key:

```python
route = [[0, 0], [1, 2], [3, 4]]
distances = {}
distances[route] = 42
```

This fails. Explain why. Rewrite the code so that `route` can be used as a dictionary key,
preserving the data. What types must you convert the inner elements to?

??? success "Solution to Exercise 1"
    The code raises:

    ```text
    TypeError: unhashable type: 'list'
    ```

    Lists are mutable and therefore not hashable. Dictionary keys must be hashable. To fix this,
    convert the outer list to a **tuple** and each inner list to a **tuple** as well:

    ```python
    route = tuple(tuple(point) for point in [[0, 0], [1, 2], [3, 4]])
    distances = {}
    distances[route] = 42

    print(distances)
    # {((0, 0), (1, 2), (3, 4)): 42}
    ```

    Both levels must be converted. A tuple of lists would still fail because the inner lists
    are unhashable. The entire structure must consist of immutable, hashable types all the way
    down.

---

**Exercise 2.**
Consider this function that is supposed to collect unique groups of students:

```python
def add_group(registry, members):
    registry.add(set(members))

registry = set()
add_group(registry, ["Alice", "Bob"])
```

Explain why this fails and fix it using an appropriate immutable type.

??? success "Solution to Exercise 2"
    The code raises:

    ```text
    TypeError: unhashable type: 'set'
    ```

    A `set` is mutable and therefore not hashable. You cannot add a set to another set. The
    fix is to use `frozenset`, which is the immutable, hashable counterpart of `set`:

    ```python
    def add_group(registry, members):
        registry.add(frozenset(members))

    registry = set()
    add_group(registry, ["Alice", "Bob"])
    add_group(registry, ["Charlie", "Diana"])

    print(registry)
    # {frozenset({'Alice', 'Bob'}), frozenset({'Charlie', 'Diana'})}
    ```

    `frozenset` is immutable, so it is hashable and can be stored inside a set or used as a
    dictionary key.

---

**Exercise 3.**
A function is supposed to add a default value to a configuration dictionary without modifying
the original:

```python
def with_defaults(config):
    config["debug"] = False
    config["verbose"] = False
    return config

original = {"host": "localhost", "port": 8080}
full = with_defaults(original)

print(original)
print(full)
print(original is full)
```

Predict the output. The programmer expects `original` to be unchanged. Why is it modified?
Rewrite `with_defaults` so that `original` is not affected.

??? success "Solution to Exercise 3"
    Output:

    ```text
    {'host': 'localhost', 'port': 8080, 'debug': False, 'verbose': False}
    {'host': 'localhost', 'port': 8080, 'debug': False, 'verbose': False}
    True
    ```

    `original` is modified because `config` and `original` refer to the **same dictionary
    object**. The function mutates that shared object directly. `original is full` is `True`
    because no new dictionary was ever created.

    The fix is to make a **defensive copy** at the start of the function:

    ```python
    def with_defaults(config):
        result = dict(config)     # shallow copy
        result["debug"] = False
        result["verbose"] = False
        return result

    original = {"host": "localhost", "port": 8080}
    full = with_defaults(original)

    print(original)
    # {'host': 'localhost', 'port': 8080}
    print(full)
    # {'host': 'localhost', 'port': 8080, 'debug': False, 'verbose': False}
    print(original is full)
    # False
    ```

    Alternatively, in Python 3.9+, you can use the merge operator:

    ```python
    def with_defaults(config):
        return config | {"debug": False, "verbose": False}
    ```

    The `|` operator returns a **new** dictionary, leaving the original untouched.
