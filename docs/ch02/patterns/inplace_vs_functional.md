
# In-Place vs Functional Style

Imagine two ways to rearrange books on a shelf. You could physically move the books where they stand, swapping and shifting until they are in order---that is **in-place modification**. Or you could take the books off the shelf, arrange them on a table, and place the sorted stack on a new shelf, leaving the original shelf untouched---that is the **functional style**. Both achieve the same goal, but they differ in what happens to the original data.

This distinction runs through all of Python. Understanding when to mutate existing data and when to produce new data is fundamental to writing correct, maintainable programs.

!!! tip "Mental Model"
    In-place style changes existing data where it lives; functional style builds new data and leaves the original untouched. Choose in-place when performance matters and you own the data, and functional style when you need safety, clarity, or must preserve the original for other consumers.

## Two Philosophies

**In-place modification** (mutation) changes the existing object. The object's identity stays the same, but its contents change.

```python
numbers = [3, 1, 4, 1, 5]
numbers.sort()
print(numbers)  # [1, 1, 3, 4, 5]
```

After `sort()`, the list `numbers` refers to the same object in memory, but its elements have been rearranged.

**Functional style** produces a new object and leaves the original unchanged.

```python
numbers = [3, 1, 4, 1, 5]
sorted_numbers = sorted(numbers)
print(sorted_numbers)  # [1, 1, 3, 4, 5]
print(numbers)          # [3, 1, 4, 1, 5]
```

`sorted()` returns a brand-new list. The original `numbers` list is untouched.

## Sorting: sort() vs sorted()

This pair is the clearest illustration of the two styles.

```python
data = [5, 2, 8, 1, 9]

# In-place: modifies data, returns None
result = data.sort()
print(result)  # None
print(data)    # [1, 2, 5, 8, 9]
```

```python
data = [5, 2, 8, 1, 9]

# Functional: returns new list, data unchanged
result = sorted(data)
print(result)  # [1, 2, 5, 8, 9]
print(data)    # [5, 2, 8, 1, 9]
```

A common mistake is writing `data = data.sort()`, which sets `data` to `None` because `sort()` returns `None`. Methods that modify in place typically return `None` to signal that mutation occurred---this is a Python convention.

## Appending vs Concatenation

Building up a list shows the same two-path choice.

### In-place: append() and extend()

```python
fruits = ["apple", "banana"]
fruits.append("cherry")
print(fruits)  # ['apple', 'banana', 'cherry']

fruits.extend(["date", "elderberry"])
print(fruits)  # ['apple', 'banana', 'cherry', 'date', 'elderberry']
```

Both `append()` and `extend()` modify the existing list and return `None`.

### Functional: concatenation

```python
fruits = ["apple", "banana"]
more_fruits = fruits + ["cherry"]
print(more_fruits)  # ['apple', 'banana', 'cherry']
print(fruits)       # ['apple', 'banana']
```

The `+` operator creates a new list. The original is unchanged.

## Reversing: reverse() vs reversed()

```python
items = [1, 2, 3, 4, 5]

# In-place
items.reverse()
print(items)  # [5, 4, 3, 2, 1]
```

```python
items = [1, 2, 3, 4, 5]

# Functional
backward = list(reversed(items))
print(backward)  # [5, 4, 3, 2, 1]
print(items)     # [1, 2, 3, 4, 5]
```

The pattern is consistent: the method mutates, the built-in function returns a new object.

## Dictionary and Set Operations

Mutable containers follow the same divide.

```python
# In-place: update modifies the dict
config = {"host": "localhost", "port": 8080}
config.update({"port": 9090, "debug": True})
print(config)  # {'host': 'localhost', 'port': 9090, 'debug': True}
```

```python
# Functional: unpacking creates a new dict
config = {"host": "localhost", "port": 8080}
new_config = {**config, "port": 9090, "debug": True}
print(new_config)  # {'host': 'localhost', 'port': 9090, 'debug': True}
print(config)      # {'host': 'localhost', 'port': 8080}
```

## Pros and Cons

### In-place modification

| Advantage | Disadvantage |
|---|---|
| Memory efficient---no copy needed | Original data is destroyed |
| Faster for large collections | Hard to debug if multiple references exist |
| Familiar imperative style | Caller may not expect mutation |

### Functional style

| Advantage | Disadvantage |
|---|---|
| Original data preserved | Uses more memory (creates copies) |
| Easier to reason about | Slower for very large data |
| Safe when multiple references exist | More objects for garbage collector |
| Enables method chaining | |

## When to Use Which

**Prefer in-place modification when:**

- You own the data and no other code holds a reference to it
- Memory is a concern and the collection is large
- You are building up a result incrementally (e.g., `append()` in a loop)

```python
# Building a list incrementally: in-place is natural
results = []
for i in range(1000):
    results.append(i ** 2)
```

**Prefer functional style when:**

- The data was passed in by a caller (do not surprise them by mutating their data)
- You need both the original and the transformed version
- You want to chain operations together
- You are working with shared or global data

```python
# Caller passes data in: do not mutate it
def top_three(scores):
    return sorted(scores, reverse=True)[:3]

original = [72, 95, 88, 61, 90]
best = top_three(original)
print(best)      # [95, 90, 88]
print(original)  # [72, 95, 88, 61, 90]  <-- still intact
```

## The Aliasing Trap

In-place modification is especially dangerous when multiple variables reference the same object.

```python
a = [1, 2, 3]
b = a          # b is an alias, not a copy
a.sort()
print(b)       # [1, 2, 3]?  No: [1, 2, 3] -> [1, 2, 3]
```

```python
a = [3, 1, 2]
b = a
a.sort()
print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3]  <-- b changed too!
```

Because `b` and `a` point to the same list, sorting `a` also sorts `b`. The functional approach avoids this entirely.

```python
a = [3, 1, 2]
b = a
c = sorted(a)
print(a)  # [3, 1, 2]  <-- unchanged
print(b)  # [3, 1, 2]  <-- unchanged
print(c)  # [1, 2, 3]  <-- new list
```

## Summary Table

| Operation | In-place (mutates) | Functional (new object) |
|---|---|---|
| Sort | `list.sort()` | `sorted(list)` |
| Reverse | `list.reverse()` | `list(reversed(list))` |
| Add element | `list.append(x)` | `list + [x]` |
| Add elements | `list.extend(other)` | `list + other` |
| Remove element | `list.remove(x)` | `[i for i in list if i != x]` |
| Update dict | `dict.update(other)` | `{**dict, **other}` |

---

## Exercises

**Exercise 1.**
Predict the output of this code. Pay careful attention to which operations mutate and which create new objects.

```python
original = [4, 2, 7, 1, 9]
backup = original

result_sort = original.sort()
print(result_sort)
print(original)
print(backup)
print(original is backup)
```

Why does `sort()` return `None`? What does the `is` check tell you about the relationship between `original` and `backup`?

??? success "Solution to Exercise 1"
    Output:

    ```text
    None
    [1, 2, 4, 7, 9]
    [1, 2, 4, 7, 9]
    True
    ```

    `sort()` returns `None` by Python convention: methods that mutate an object in place return `None` to make it clear that no new object was created. This prevents the common mistake of chaining off a mutation (e.g., `data.sort().reverse()` would fail because `None` has no `reverse` method).

    `original is backup` is `True` because `backup = original` creates an alias, not a copy. Both variables point to the exact same list object in memory. When `sort()` rearranges the elements of that object, both names see the change. This is the aliasing trap---if you needed `backup` to remain unsorted, you should have written `backup = original.copy()` or `backup = sorted(original)`.

---

**Exercise 2.**
Write a function `safe_sort` that returns a sorted version of the input list without modifying the original. Then write a function `sort_in_place` that sorts the list in place and returns `None`. Demonstrate that each behaves correctly.

```python
def safe_sort(data):
    # your code here
    pass

def sort_in_place(data):
    # your code here
    pass

nums = [5, 3, 8, 1]

result = safe_sort(nums)
print(result)        # should be sorted
print(nums)          # should be unchanged

sort_in_place(nums)
print(nums)          # should now be sorted
```

??? success "Solution to Exercise 2"
    ```python
    def safe_sort(data):
        return sorted(data)

    def sort_in_place(data):
        data.sort()

    nums = [5, 3, 8, 1]

    result = safe_sort(nums)
    print(result)   # [1, 3, 5, 8]
    print(nums)     # [5, 3, 8, 1]

    sort_in_place(nums)
    print(nums)     # [1, 3, 5, 8]
    ```

    Output:

    ```text
    [1, 3, 5, 8]
    [5, 3, 8, 1]
    [1, 3, 5, 8]
    ```

    `safe_sort` uses `sorted()`, which creates a new list and leaves the original untouched. `sort_in_place` calls `data.sort()`, which mutates the list that was passed in. Since lists are mutable and passed by reference, the caller sees the change. The function implicitly returns `None`, matching the convention of in-place operations.

---

**Exercise 3.**
Predict the output of this code that mixes in-place and functional operations.

```python
data = [3, 1, 4, 1, 5]

a = sorted(data)
b = data + [9]
data.append(2)
data.sort()

print(a)
print(b)
print(data)
print(a is data)
print(b is data)
```

How many distinct list objects exist after all operations complete? Trace which operations create new lists and which modify existing ones.

??? success "Solution to Exercise 3"
    Output:

    ```text
    [1, 1, 3, 4, 5]
    [3, 1, 4, 1, 5, 9]
    [1, 1, 2, 3, 4, 5]
    False
    False
    ```

    Three distinct list objects exist:

    1. `a` -- created by `sorted(data)`, a new list `[1, 1, 3, 4, 5]`. It is a snapshot of `data` at the time `sorted()` was called. Later changes to `data` do not affect it.
    2. `b` -- created by `data + [9]`, a new list `[3, 1, 4, 1, 5, 9]`. The `+` operator always creates a new list. It captures `data` before `append(2)` and `sort()`.
    3. `data` -- the original list, mutated in place by `append(2)` (adds `2` to the end) and then `sort()` (rearranges to `[1, 1, 2, 3, 4, 5]`).

    `a is data` and `b is data` are both `False` because `sorted()` and `+` each create new list objects. The key lesson: functional operations (`sorted`, `+`) create independent copies, while in-place operations (`append`, `sort`) modify the original. Once a copy is made, it is completely independent of the source.
