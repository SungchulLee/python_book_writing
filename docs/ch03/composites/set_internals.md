# set Internals

Sets are implemented similarly to dictionaries—as hash tables—enabling O(1) average membership testing and set operations. Understanding set internals explains their performance characteristics and implementation constraints.

!!! tip "Mental Model"
    A set is a dict that stores only keys with no values. Like dicts, sets use hash tables for O(1) membership testing and require elements to be hashable. This shared foundation is why sets and dicts have the same performance profile and the same restrictions on what they can contain.

---

## Hash-Based Implementation

### Membership Testing is Fast

```python
s = {i for i in range(100000)}

# O(1) average case
print(50000 in s)
print(99999 in s)
print(100000 in s)
```

Output:
```
True
True
False
```

### Elements Must Be Hashable

```python
s = {1, 2.5, "three", (4, 5)}
print(s)

# Unhashable types fail
try:
    s.add([6, 7])
except TypeError as e:
    print(f"Error: {e}")
```

Output:
```
{1, 2.5, 'three', (4, 5)}
Error: unhashable type: 'list'
```

## Set Operations as Hash Operations

### Union, Intersection, Difference

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(f"Union: {a | b}")
print(f"Intersection: {a & b}")
print(f"Difference: {a - b}")
print(f"Symmetric difference: {a ^ b}")
```

Output:
```
Union: {1, 2, 3, 4, 5, 6}
Intersection: {3, 4}
Difference: {1, 2}
Symmetric difference: {1, 2, 5, 6}
```

## Set vs List Performance

### Membership Testing

```python
import time

# Using list
lst = list(range(100000))
set_time = time.time()
for _ in range(1000):
    50000 in lst
list_duration = time.time() - set_time

# Using set
s = set(range(100000))
start = time.time()
for _ in range(1000):
    50000 in s
set_duration = time.time() - start

print(f"List: {list_duration:.4f}s")
print(f"Set: {set_duration:.6f}s")
```

Output:
```
List: 0.0234s
Set: 0.000024s
```

## Practical Uses

### Deduplication

```python
data = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = set(data)
print(unique)
```

Output:
```
{1, 2, 3, 4}
```

### Finding Common Elements

```python
students_morning = {'Alice', 'Bob', 'Charlie'}
students_afternoon = {'Bob', 'Charlie', 'David'}

both_shifts = students_morning & students_afternoon
print(f"Both shifts: {both_shifts}")
```

Output:
```
Both shifts: {'Charlie', 'Bob'}
```

---

## Runnable Example: `set_vs_list_performance.py`

```python
"""
TUTORIAL: Sets vs Lists for Membership Testing - O(1) vs O(n)

Why this matters:
  When you need to check "is this item in my collection?", the data structure
  you choose determines speed. Lists require scanning every item (O(n) time).
  Sets use hashing to find items instantly (O(1) time).

  For small lists, the difference is negligible. But with hundreds or thousands
  of items, using a list instead of a set can cost you seconds per second of work.

Core lesson:
  If you're doing membership testing on a large collection, USE A SET.
  If you need order or duplicates, use a list and accept the O(n) cost.
  But whenever you can, choose the faster structure.
"""

import random
import string
import timeit


# ============ Example 1: List-based uniqueness ============
# This function finds unique first names by using a nested loop.
# For each name, it searches through the unique list (O(n) per name).
# Total time: O(n^2) - quadratic, gets slow fast!

def list_unique_names(phonebook):
    """Find unique first names using a list. O(n^2) due to nested search."""
    unique_names = []
    for name, phonenumber in phonebook:
        first_name, last_name = name.split(" ", 1)

        # Check if first_name already in unique_names list
        # This is O(n) - must scan list each time
        for unique in unique_names:
            if unique == first_name:
                break  # Found it, don't add
        else:
            # Only reached if loop completed without break
            unique_names.append(first_name)

    return len(unique_names)


# ============ Example 2: Set-based uniqueness ============
# This function uses a set. Membership test is O(1) using hash lookup.
# For each name, we just add to set (duplicates automatically ignored).
# Total time: O(n) - linear, much faster!

def set_unique_names(phonebook):
    """Find unique first names using a set. O(n) due to O(1) lookups."""
    unique_names = set()
    for name, phonenumber in phonebook:
        first_name, last_name = name.split(" ", 1)

        # Add to set. Duplicates automatically ignored (O(1) time).
        unique_names.add(first_name)

    return len(unique_names)


# ============ Example 3: Helper function ============

def random_name():
    """Generate a random first and last name."""
    first_name = "".join(random.sample(string.ascii_letters, 8))
    last_name = "".join(random.sample(string.ascii_letters, 8))
    return f"{first_name} {last_name}"


def demo_small_data():
    """Show both methods on small data where difference is small."""
    print("\n" + "=" * 70)
    print("Example 1: Small Phonebook (few entries)")
    print("=" * 70)

    small_phonebook = [
        ("John Doe", "555-555-5555"),
        ("Jane Smith", "555-555-5556"),
        ("John Davis", "555-555-5557"),
        ("Albert Einstein", "212-555-5555"),
    ]

    print(f"Phonebook size: {len(small_phonebook)}")
    print()

    unique_from_list = list_unique_names(small_phonebook)
    unique_from_set = set_unique_names(small_phonebook)

    print(f"Unique first names (list method): {unique_from_list}")
    print(f"Unique first names (set method):  {unique_from_set}")
    print()
    print("Both give correct answers. On small data, speed difference is tiny.")


def demo_large_data():
    """Show performance difference on large data."""
    print("\n" + "=" * 70)
    print("Example 2: Large Phonebook (1000 entries)")
    print("=" * 70)

    random.seed(42)  # Reproducible results
    large_phonebook = [(random_name(), "555-5555") for i in range(1000)]

    print(f"Phonebook size: {len(large_phonebook)}")
    print(f"Running 50 iterations to measure time accurately...")
    print()

    # Time the list method
    setup_list = """
from __main__ import large_phonebook, list_unique_names
"""
    t_list = timeit.timeit(
        stmt="list_unique_names(large_phonebook)",
        setup=setup_list,
        number=50
    )

    # Time the set method
    setup_set = """
from __main__ import large_phonebook, set_unique_names
"""
    t_set = timeit.timeit(
        stmt="set_unique_names(large_phonebook)",
        setup=setup_set,
        number=50
    )

    time_per_call_list = t_list / 50
    time_per_call_set = t_set / 50
    speedup = time_per_call_list / time_per_call_set

    print(f"List method time:  {time_per_call_list:2e} seconds per call")
    print(f"Set method time:   {time_per_call_set:2e} seconds per call")
    print()
    print(f"SET is {speedup:.1f}x FASTER than list!")
    print()
    print("""
    WHY such a big difference:

    List approach (O(n^2)):
    - Check item 1 against 0 items: 1 comparison
    - Check item 2 against 1 item: 1 comparison
    - Check item 3 against 2 items: 2 comparisons
    - ...
    - Check item 1000 against ~500 items: 500 comparisons
    - Total: 1 + 1 + 2 + 3 + ... + 500 ≈ 125,000 comparisons

    Set approach (O(n)):
    - Add item 1: 1 operation
    - Add item 2: 1 operation
    - Add item 3: 1 operation
    - ...
    - Add item 1000: 1 operation
    - Total: 1000 operations
    - 125x fewer operations!
    """)


def demo_complexity_comparison():
    """Show how complexity grows with data size."""
    print("\n" + "=" * 70)
    print("Example 3: How Complexity Grows with Data Size")
    print("=" * 70)

    print("""
    For checking membership in N items:

    Data Size    List Method      Set Method      Speedup
    ---------    -----------      ----------      -------
    10 items     ~50 comparisons  10 ops          5x
    100 items    ~5,000 comps     100 ops         50x
    1,000 items  ~500,000 comps   1,000 ops       500x
    10,000 items ~50M comps       10,000 ops      5,000x

    Notice: As data grows, list method gets exponentially slower!
            Set method grows linearly (much more reasonable).

    For real-world phonebooks:
    - 1,000 entries: Set is 500x faster
    - 10,000 entries: Set is 5,000x faster
    - 1,000,000 entries: Set is 500,000x faster

    That's not theoretical - that's real wall-clock time!
    """)


def demo_when_to_use_each():
    """Explain when to use list vs set."""
    print("\n" + "=" * 70)
    print("Example 4: When to Use List vs Set")
    print("=" * 70)

    print("""
    USE A LIST when:
    - You need to preserve order
    - You need to access items by position (index)
    - You need to store duplicates
    - Data is small (< 100 items typically)
    - You rarely check membership
    - You need custom ordering

    USE A SET when:
    - You frequently check membership ("is X in collection?")
    - You need fast add/remove operations
    - Duplicates don't make sense for your data
    - You have large collections (> 100 items)
    - You need O(1) membership testing

    HYBRID APPROACH:
    - Store data as list (ordered, duplicates preserved)
    - Create set for membership testing
    - Cost: Extra memory, but gains speed on lookups

    EXAMPLE:
    names = [...]  # List for iteration and order
    name_set = set(names)  # Set for fast checking
    if "John" in name_set: ...  # O(1) instead of O(n)
    """)


if __name__ == "__main__":
    print("=" * 70)
    print("TUTORIAL: Sets vs Lists - Membership Testing Performance")
    print("=" * 70)

    demo_small_data()
    demo_large_data()
    demo_complexity_comparison()
    demo_when_to_use_each()

    # -------- KEY INSIGHTS --------
    print("\n" + "=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print("""
1. LIST membership is O(n):
   - Must scan every item to check membership
   - Slow for large collections
   - Quadratic complexity for checking all items

2. SET membership is O(1):
   - Hash lookup finds item instantly
   - Constant time regardless of collection size
   - Linear complexity for checking all items

3. COMPLEXITY MATTERS at SCALE:
   - Small differences (< 100 items): negligible
   - Medium differences (100-1,000): noticeable
   - Large differences (1,000+ items): critical

4. REAL-WORLD IMPACT:
   - List on 1,000 items: seconds
   - Set on 1,000 items: milliseconds
   - Difference is user-visible

5. MEMORY TRADEOFF:
   - Set uses ~1.5x more memory than list (for hashing)
   - But gains 500x+ speed on membership testing
   - Usually worthwhile for frequently-tested collections

6. BEST PRACTICE:
   - Default to set for membership testing
   - Only use list if you need order or duplicates
   - If uncertain, profile and measure
   - The overhead of set is minimal if you need speed
    """)
```

---

## Exercises


**Exercise 1.**
Write a function `find_duplicates(lst)` that uses a set to find and return all duplicate elements in a list. For example, `find_duplicates([1, 2, 2, 3, 3, 3, 4])` should return `{2, 3}`.

??? success "Solution to Exercise 1"

        ```python
        def find_duplicates(lst):
            seen = set()
            duplicates = set()
            for item in lst:
                if item in seen:
                    duplicates.add(item)
                seen.add(item)
            return duplicates

        print(find_duplicates([1, 2, 2, 3, 3, 3, 4]))  # {2, 3}
        ```

    Using two sets gives O(n) performance. `seen` tracks all encountered elements and `duplicates` collects those seen more than once.

---

**Exercise 2.**
Demonstrate that set elements must be hashable by attempting to add a list to a set. Then show how to add the same data by converting it to a tuple.

??? success "Solution to Exercise 2"

        ```python
        s = set()

        try:
            s.add([1, 2, 3])
        except TypeError as e:
            print(f"Error: {e}")  # unhashable type: 'list'

        s.add((1, 2, 3))
        print(s)  # {(1, 2, 3)}
        ```

    Lists are mutable and unhashable. Tuples are immutable and hashable, making them valid set elements.

---

**Exercise 3.**
Given two sets `a = {1, 2, 3, 4, 5}` and `b = {4, 5, 6, 7, 8}`, compute and print the union, intersection, difference (a - b), and symmetric difference using both operator syntax and method syntax.

??? success "Solution to Exercise 3"

        ```python
        a = {1, 2, 3, 4, 5}
        b = {4, 5, 6, 7, 8}

        # Operator syntax
        print(a | b)   # {1, 2, 3, 4, 5, 6, 7, 8}
        print(a & b)   # {4, 5}
        print(a - b)   # {1, 2, 3}
        print(a ^ b)   # {1, 2, 3, 6, 7, 8}

        # Method syntax
        print(a.union(b))                # {1, 2, 3, 4, 5, 6, 7, 8}
        print(a.intersection(b))         # {4, 5}
        print(a.difference(b))           # {1, 2, 3}
        print(a.symmetric_difference(b)) # {1, 2, 3, 6, 7, 8}
        ```

    Both syntaxes produce identical results. The method syntax is more explicit and can accept any iterable, while operators require both operands to be sets.
