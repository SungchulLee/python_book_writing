# list Copying

Understanding copy semantics is essential when working with mutable lists.

!!! tip "Mental Model"
    Assignment (`b = a`) creates a second label on the same box -- both names see the same list. A shallow copy (`a[:]`, `list(a)`) creates a new box but fills it with references to the same inner objects. A deep copy (`copy.deepcopy`) clones the box and recursively clones everything inside it. Choose the right level based on whether your list contains mutable elements.

---

## The Aliasing Problem

Assignment creates a reference, not a copy:

```python
a = [1, 2, 3]
b = a           # b points to same object
a.append(4)
print(b)        # [1, 2, 3, 4]
```

```
a ─┬──► [1, 2, 3, 4]
   │
b ─┘
```

---

## Creating Copies

### Method 1: Slicing

```python
a = [1, 2, 3]
b = a[:]        # Shallow copy
a.append(4)
print(b)        # [1, 2, 3]
```

### Method 2: `copy()` method

```python
a = [1, 2, 3]
b = a.copy()    # Shallow copy
```

### Method 3: `list()` constructor

```python
a = [1, 2, 3]
b = list(a)     # Shallow copy
```

---

## Shallow vs Deep Copy

### Shallow Copy

Copies the list structure, but nested objects are still shared:

```python
a = [[1, 2], [3, 4]]
b = a.copy()          # Shallow copy

a[0][0] = 'X'
print(b)              # [['X', 2], [3, 4]]  (affected!)

a[0] = [9, 9]
print(b)              # [['X', 2], [3, 4]]  (not affected)
```

```
a ──► [ ref1, ref2 ]
         │      │
b ──► [ ref1, ref2 ]   (same inner refs)
         │      │
         ▼      ▼
      [1,2]  [3,4]
```

### Deep Copy

Recursively copies all nested objects:

```python
import copy

a = [[1, 2], [3, 4]]
b = copy.deepcopy(a)  # Deep copy

a[0][0] = 'X'
print(b)              # [[1, 2], [3, 4]]  (unchanged)
```

---

## `+` vs `+=` Behavior

### `+` Creates New Object

```python
a = [1, 2, 3]
print(id(a))          # e.g., 140234567890

a = a + [4]
print(id(a))          # Different id (new object)
```

### `+=` Modifies In-Place

```python
a = [1, 2, 3]
print(id(a))          # e.g., 140234567890

a += [4]
print(id(a))          # Same id (same object)
```

This matters when other names reference the same list:

```python
a = [1, 2, 3]
b = a

a = a + [4]           # a is new object
print(b)              # [1, 2, 3] (b unchanged)

a = [1, 2, 3]
b = a

a += [4]              # a modified in-place
print(b)              # [1, 2, 3, 4] (b affected!)
```

---

## When to Use Which

| Scenario | Method |
|----------|--------|
| Simple list of immutables | `a[:]` or `a.copy()` |
| Nested lists/objects | `copy.deepcopy(a)` |
| Independent modification | Always copy first |

---

## Common Pitfall: Iterating While Modifying

```python
# Bug: skips elements
a = [1, 2, 3, 4]
for x in a:
    if x % 2 == 0:
        a.remove(x)
print(a)  # [1, 3] — but 4 was skipped!

# Fix: iterate over a copy
a = [1, 2, 3, 4]
for x in a[:]:        # a[:] is a copy
    if x % 2 == 0:
        a.remove(x)
print(a)  # [1, 3]

# Better: use list comprehension
a = [x for x in a if x % 2 != 0]
```

---

## Summary

| Method | Shallow | Deep | New Object |
|--------|---------|------|------------|
| `b = a` | ❌ | ❌ | ❌ (alias) |
| `b = a[:]` | ✅ | ❌ | ✅ |
| `b = a.copy()` | ✅ | ❌ | ✅ |
| `b = list(a)` | ✅ | ❌ | ✅ |
| `b = copy.deepcopy(a)` | ✅ | ✅ | ✅ |

---

## Exercises


**Exercise 1.**
Demonstrate the aliasing problem by creating a list `a`, assigning `b = a`, appending to `b`, and showing that `a` is also affected. Then fix it using a shallow copy.

??? success "Solution to Exercise 1"

        ```python
        a = [1, 2, 3]
        b = a
        b.append(4)
        print(a)  # [1, 2, 3, 4] (affected!)

        # Fix with shallow copy
        a = [1, 2, 3]
        b = a.copy()
        b.append(4)
        print(a)  # [1, 2, 3] (unchanged)
        print(b)  # [1, 2, 3, 4]
        ```

    `b = a` creates an alias. `b = a.copy()` creates an independent shallow copy.

---

**Exercise 2.**
Given the nested list `matrix = [[1, 2], [3, 4]]`, create both a shallow copy and a deep copy. Modify `matrix[0][0] = 99` and show which copy is affected and which is not.

??? success "Solution to Exercise 2"

        ```python
        import copy

        matrix = [[1, 2], [3, 4]]
        shallow = matrix.copy()
        deep = copy.deepcopy(matrix)

        matrix[0][0] = 99

        print(matrix)  # [[99, 2], [3, 4]]
        print(shallow) # [[99, 2], [3, 4]] (affected!)
        print(deep)    # [[1, 2], [3, 4]]  (unchanged)
        ```

    Shallow copy shares nested objects. Deep copy recursively copies everything, creating fully independent structures.

---

**Exercise 3.**
Write a function `safe_remove_evens(lst)` that returns a new list with all even numbers removed, without modifying the original list. Demonstrate that the original list is unchanged.

??? success "Solution to Exercise 3"

        ```python
        def safe_remove_evens(lst):
            return [x for x in lst if x % 2 != 0]

        original = [1, 2, 3, 4, 5, 6]
        filtered = safe_remove_evens(original)

        print(original)  # [1, 2, 3, 4, 5, 6] (unchanged)
        print(filtered)  # [1, 3, 5]
        ```

    List comprehension creates a new list, leaving the original intact.
