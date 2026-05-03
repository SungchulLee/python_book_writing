# Time Complexity of Operations

Python data structures have different time complexity characteristics for common operations. Understanding these complexities is crucial for writing efficient code and choosing the right data structure.

!!! tip "Mental Model"
    Lists are fast at the end (append/pop are O(1)) but slow at the front (insert/delete are O(n) because everything shifts). Dicts and sets are fast everywhere for lookup, insert, and delete (O(1) average) but use more memory. Choosing the right container is choosing the right trade-off between access pattern and memory cost.

---

## List Operations

### Common Operations

```python
lst = [1, 2, 3, 4, 5]

# O(1) - Index access
print(lst[2])

# O(n) - Search
print(3 in lst)

# O(1) amortized - Append
lst.append(6)

# O(n) - Insert at beginning
lst.insert(0, 0)
```

Output:
```
3
True
```

## Dictionary Operations

### Hash Table Performance

```python
d = {'a': 1, 'b': 2, 'c': 3}

# O(1) - Key lookup
print(d['a'])

# O(1) - Insert/Update
d['d'] = 4

# O(1) - Delete
del d['a']

print(d)
```

Output:
```
1
{'b': 2, 'c': 3, 'd': 4}
```

## Set Operations

### Hash Set Performance

```python
s = {1, 2, 3, 4, 5}

# O(1) - Membership test
print(2 in s)

# O(1) - Add
s.add(6)

# O(n) - Union
s2 = {4, 5, 6, 7}
union = s | s2
print(union)
```

Output:
```
True
{1, 2, 3, 4, 5, 6, 7}
```

## Comparison Table

### Big-O Complexity Summary

```python
import sys

# Complexity examples
operations = {
    'list': {
        'index': 'O(1)',
        'search': 'O(n)',
        'append': 'O(1)',
        'insert': 'O(n)',
        'delete': 'O(n)'
    },
    'dict': {
        'lookup': 'O(1)',
        'insert': 'O(1)',
        'delete': 'O(1)'
    },
    'set': {
        'search': 'O(1)',
        'add': 'O(1)',
        'delete': 'O(1)'
    }
}

for ds, ops in operations.items():
    print(f"\n{ds.upper()}:")
    for op, complexity in ops.items():
        print(f"  {op}: {complexity}")
```

Output:
```
LIST:
  index: O(1)
  search: O(n)
  append: O(1)
  insert: O(n)
  delete: O(n)

DICT:
  lookup: O(1)
  insert: O(1)
  delete: O(1)

SET:
  search: O(1)
  add: O(1)
  delete: O(1)
```

---

## Runnable Example: `bisect_module_tutorial.py`

```python
"""
TUTORIAL: Using bisect for Efficient Sorted List Operations

Why this matters:
  Finding items in a sorted list is a classic problem. If you use a simple
  loop (O(n) time), you check every item. But BINARY SEARCH (O(log n) time)
  cuts the work in half with each comparison.

  The bisect module implements binary search in Python. It's:
  - Much faster for large sorted lists
  - Optimal for finding insertion points
  - Perfect for "closest value" problems

Core lesson:
  When you have sorted data, leverage binary search via bisect. For a list of
  1,000 items, bisect needs ~10 comparisons. Linear search needs ~500 on average.
"""

import bisect
import random


# ============ Example 1: Inserting in sorted order ============
# bisect.insort() maintains sorted order automatically. Each new number
# is placed in its correct position using binary search (~log n operations).
# This is much better than append + sort repeatedly.

def demo_insort():
    """Show how bisect.insort keeps a list sorted."""
    print("\n" + "=" * 70)
    print("Example 1: Inserting items while maintaining sorted order")
    print("=" * 70)

    important_numbers = []
    random.seed(42)  # For reproducible results

    for i in range(10):
        new_number = random.randint(0, 1000)
        print(f"Inserting {new_number}...", end=" -> ")
        bisect.insort(important_numbers, new_number)
        print(f"List is now: {important_numbers}")

    print(f"\nFinal sorted list: {important_numbers}")
    print("WHY: bisect.insort finds the right position (O(log n)) then inserts.")
    print("List remains sorted without calling sort() repeatedly.")


# ============ Example 2: Finding closest values ============
# bisect_left() tells us where a value WOULD go if inserted.
# We can use this to find the closest value, both higher and lower.

def find_closest(haystack, needle):
    """
    Find the value in haystack that's closest to needle.

    Algorithm:
    1. Use bisect_left to find where needle would be inserted
    2. Check three candidates: at position i, at i-1, and at i+1
    3. Return the closest one
    """

    # bisect_left returns the insertion position
    i = bisect.bisect_left(haystack, needle)

    # Boundary case: needle is larger than everything in the list
    if i == len(haystack):
        return i - 1  # Return the last item (largest)

    # Boundary case: needle matches an item exactly
    elif haystack[i] == needle:
        return i  # Perfect match!

    # General case: needle is between two items
    # Compare haystack[i] (the next item) with haystack[i-1] (previous item)
    elif i > 0:
        next_item = haystack[i]
        prev_item = haystack[i - 1]

        # Which is closer: next or previous?
        distance_to_next = next_item - needle
        distance_to_prev = needle - prev_item

        if distance_to_next > distance_to_prev:
            return i - 1  # Previous is closer

    return i  # Next is closer (or no previous item exists)


def demo_find_closest():
    """Show finding closest values using binary search."""
    print("\n" + "=" * 70)
    print("Example 2: Finding closest value in sorted list")
    print("=" * 70)

    important_numbers = [14, 265, 496, 661, 683, 734, 881, 892, 973, 992]
    print(f"Working with sorted list: {important_numbers}\n")

    # Test case 1: needle far below the list
    needle = -250
    closest_idx = find_closest(important_numbers, needle)
    closest_val = important_numbers[closest_idx]
    print(f"Closest value to {needle:5}: {closest_val:5}")
    print(f"  (distance = {closest_val - needle})")

    # Test case 2: needle in the middle of the list
    needle = 500
    closest_idx = find_closest(important_numbers, needle)
    closest_val = important_numbers[closest_idx]
    print(f"Closest value to {needle:5}: {closest_val:5}")
    print(f"  (distance = {abs(closest_val - needle)})")

    # Test case 3: needle far above the list
    needle = 1100
    closest_idx = find_closest(important_numbers, needle)
    closest_val = important_numbers[closest_idx]
    print(f"Closest value to {needle:5}: {closest_val:5}")
    print(f"  (distance = {needle - closest_val})")

    # Test case 4: exact match
    needle = 661
    closest_idx = find_closest(important_numbers, needle)
    closest_val = important_numbers[closest_idx]
    print(f"Closest value to {needle:5}: {closest_val:5}")
    print(f"  (exact match!)")


# ============ Example 3: bisect_left vs bisect_right ============
# These functions differ when the needle exists in the list.

def demo_bisect_variants():
    """Show the difference between bisect_left and bisect_right."""
    print("\n" + "=" * 70)
    print("Example 3: bisect_left vs bisect_right for duplicates")
    print("=" * 70)

    data = [10, 20, 20, 20, 30, 40]
    needle = 20

    left_pos = bisect.bisect_left(data, needle)
    right_pos = bisect.bisect_right(data, needle)

    print(f"Data: {data}")
    print(f"Looking for: {needle}\n")
    print(f"bisect_left({needle}):   position {left_pos}  (first occurrence)")
    print(f"bisect_right({needle}):  position {right_pos} (after last occurrence)")

    print("\nWHY: When duplicates exist:")
    print("  - bisect_left: insert BEFORE duplicates")
    print("  - bisect_right: insert AFTER duplicates")


if __name__ == "__main__":
    print("=" * 70)
    print("TUTORIAL: Binary Search with bisect Module")
    print("=" * 70)

    demo_insort()
    demo_find_closest()
    demo_bisect_variants()

    # -------- KEY INSIGHTS --------
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. BISECT.INSORT maintains sorted order:
   - Insert item in O(log n) time to find position
   - Then O(n) to shift items for insertion
   - Better than append-then-sort when doing many inserts

2. BINARY SEARCH efficiency:
   - List of 1,000 items: ~10 comparisons (vs 500 for linear search)
   - List of 1,000,000 items: ~20 comparisons (vs 500,000)
   - Difference grows with list size!

3. BISECT.BISECT_LEFT vs BISECT_RIGHT:
   - Use bisect_left to find first occurrence
   - Use bisect_right to find insertion point after duplicates
   - Use bisect_right (default) for most insertion tasks

4. PERFECT for "closest value" problems:
   - Find insertion position with bisect_left
   - Check items before/after that position
   - Comparison costs much less than linear scan

5. REQUIREMENT: List MUST be sorted:
   - bisect doesn't check if list is sorted
   - If unsorted, results are undefined
   - Always sort first if data order is uncertain
    """)
```

---

## Exercises


**Exercise 1.**
Write a benchmark that compares the time to check membership (`x in collection`) for a list, set, and dictionary, each with 100000 elements. Which is fastest and why?

??? success "Solution to Exercise 1"

        ```python
        import timeit

        n = 100_000
        setup_list = f"c = list(range({n}))"
        setup_set = f"c = set(range({n}))"
        setup_dict = f"c = {{i: None for i in range({n})}}"

        t_list = timeit.timeit(f"{n-1} in c", setup=setup_list, number=1000)
        t_set = timeit.timeit(f"{n-1} in c", setup=setup_set, number=1000)
        t_dict = timeit.timeit(f"{n-1} in c", setup=setup_dict, number=1000)

        print(f"List: {t_list:.4f}s")
        print(f"Set:  {t_set:.6f}s")
        print(f"Dict: {t_dict:.6f}s")
        ```

    Sets and dicts use hash-based lookup (O(1) average), while lists require linear scan (O(n)). Sets and dicts are orders of magnitude faster for membership testing.

---

**Exercise 2.**
Explain why `list.insert(0, x)` is O(n) while `list.append(x)` is O(1). Write a timing experiment that demonstrates this difference with a list of 100000 elements.

??? success "Solution to Exercise 2"

        ```python
        import timeit

        n = 100_000
        t_append = timeit.timeit(
            "lst.append(0)",
            setup=f"lst = list(range({n}))",
            number=1000
        )
        t_insert = timeit.timeit(
            "lst.insert(0, 0)",
            setup=f"lst = list(range({n}))",
            number=1000
        )

        print(f"append: {t_append:.4f}s")
        print(f"insert(0): {t_insert:.4f}s")
        ```

    `append` adds to the end in O(1) amortized time. `insert(0, x)` must shift all existing elements one position to the right, requiring O(n) time.

---

**Exercise 3.**
A developer has written the following code. Identify the performance problem and suggest a fix that improves the time complexity.

```python
def remove_duplicates(lst):
    result = []
    for item in lst:
        if item not in result:
            result.append(item)
    return result
```

??? success "Solution to Exercise 3"

    The problem is that `item not in result` performs a linear scan of `result` for each element, giving O(n^2) overall complexity. Fix by using a set for fast membership testing:

        ```python
        def remove_duplicates(lst):
            seen = set()
            result = []
            for item in lst:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            return result
        ```

    The improved version is O(n) because set membership testing is O(1).
