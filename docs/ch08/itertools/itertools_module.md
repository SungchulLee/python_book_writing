# itertools Module

The `itertools` module provides a collection of fast, memory-efficient tools for working with iterators. These functions create iterators for efficient looping, combining, and filtering data.

!!! tip "Mental Model"
    `itertools` is a LEGO set for iterators — each function is a small, composable brick (chain, filter, group, slice, combine) that snaps together with others to build sophisticated data pipelines. Because every tool yields items lazily, you can process millions of elements without loading them all into memory at once.

```python
import itertools
```

---

## Why itertools?

- **Memory efficient**: Generates items on-demand (lazy evaluation)
- **Fast**: Implemented in C for performance
- **Composable**: Functions can be combined to build complex pipelines
- **Pythonic**: Replaces verbose loops with expressive one-liners

---

## Infinite Iterators

These iterators run forever unless stopped.

### count(start=0, step=1)

Generates consecutive numbers indefinitely:

```python
from itertools import count

# Count from 0
for i in count():
    if i >= 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# Count from 10 with step 2
for i in count(10, 2):
    if i >= 20:
        break
    print(i)  # 10, 12, 14, 16, 18

# Useful with zip
names = ['Alice', 'Bob', 'Charlie']
for i, name in zip(count(1), names):
    print(f"{i}. {name}")
# 1. Alice
# 2. Bob
# 3. Charlie
```

### cycle(iterable)

Repeats an iterable indefinitely:

```python
from itertools import cycle

colors = cycle(['red', 'green', 'blue'])
for i, color in zip(range(7), colors):
    print(f"Item {i}: {color}")
# Item 0: red
# Item 1: green
# Item 2: blue
# Item 3: red
# Item 4: green
# Item 5: blue
# Item 6: red

# Practical: alternating row colors
rows = ['Row A', 'Row B', 'Row C', 'Row D', 'Row E']
bg_colors = cycle(['white', 'gray'])
for row, bg in zip(rows, bg_colors):
    print(f"{row} -> {bg}")
```

### repeat(elem, n=None)

Repeats an element n times (or forever if n is None):

```python
from itertools import repeat

# Repeat 5 times
list(repeat('hello', 5))  # ['hello', 'hello', 'hello', 'hello', 'hello']

# Useful with map
import operator
list(map(operator.mul, range(5), repeat(3)))  # [0, 3, 6, 9, 12]

# Forever (be careful!)
for i, x in zip(range(3), repeat('*')):
    print(x)  # *, *, *
```

---

## Combinatoric Iterators

Generate combinations and permutations.

### product(*iterables, repeat=1)

Cartesian product (like nested for loops):

```python
from itertools import product

# Two iterables
list(product('AB', '12'))
# [('A', '1'), ('A', '2'), ('B', '1'), ('B', '2')]

# Three iterables
list(product([0, 1], [0, 1], [0, 1]))
# [(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)]

# With repeat
list(product('AB', repeat=2))
# [('A', 'A'), ('A', 'B'), ('B', 'A'), ('B', 'B')]

# Practical: generate all possible configurations
sizes = ['S', 'M', 'L']
colors = ['red', 'blue']
for size, color in product(sizes, colors):
    print(f"{size}-{color}")
```

### permutations(iterable, r=None)

All possible orderings of length r:

```python
from itertools import permutations

# All permutations
list(permutations('ABC'))
# [('A','B','C'), ('A','C','B'), ('B','A','C'), 
#  ('B','C','A'), ('C','A','B'), ('C','B','A')]

# Permutations of length 2
list(permutations('ABC', 2))
# [('A','B'), ('A','C'), ('B','A'), ('B','C'), ('C','A'), ('C','B')]

# Count permutations: n! / (n-r)!
# permutations('ABCD', 2) -> 4! / 2! = 12 items
```

### combinations(iterable, r)

All unique subsets of length r (order doesn't matter):

```python
from itertools import combinations

# Choose 2 from 4
list(combinations('ABCD', 2))
# [('A','B'), ('A','C'), ('A','D'), ('B','C'), ('B','D'), ('C','D')]

# Choose 3 from 4
list(combinations('ABCD', 3))
# [('A','B','C'), ('A','B','D'), ('A','C','D'), ('B','C','D')]

# Practical: all pairs from a list
people = ['Alice', 'Bob', 'Charlie', 'Diana']
for p1, p2 in combinations(people, 2):
    print(f"{p1} meets {p2}")
```

### combinations_with_replacement(iterable, r)

Combinations where elements can repeat:

```python
from itertools import combinations_with_replacement

list(combinations_with_replacement('ABC', 2))
# [('A','A'), ('A','B'), ('A','C'), ('B','B'), ('B','C'), ('C','C')]

# Practical: dice combinations
dice_sums = {}
for d1, d2 in combinations_with_replacement(range(1, 7), 2):
    total = d1 + d2
    dice_sums[total] = dice_sums.get(total, 0) + 1
```

### Comparison

| Function | Order Matters? | Repeats Allowed? | Example (ABC, r=2) |
|----------|---------------|------------------|-------------------|
| `permutations` | Yes | No | AB, BA, AC, CA, BC, CB |
| `combinations` | No | No | AB, AC, BC |
| `combinations_with_replacement` | No | Yes | AA, AB, AC, BB, BC, CC |
| `product` | Yes | Yes | AA, AB, AC, BA, BB, BC, CA, CB, CC |

---

## Terminating Iterators

These consume input iterables and produce output.

### chain(*iterables)

Concatenates multiple iterables into one:

```python
from itertools import chain

# Chain lists
list(chain([1, 2], [3, 4], [5, 6]))  # [1, 2, 3, 4, 5, 6]

# Chain different types
list(chain('ABC', [1, 2, 3]))  # ['A', 'B', 'C', 1, 2, 3]

# Flatten one level of nesting
nested = [[1, 2], [3, 4], [5, 6]]
list(chain.from_iterable(nested))  # [1, 2, 3, 4, 5, 6]

# Practical: process multiple files
def read_lines(filename):
    with open(filename) as f:
        yield from f

all_lines = chain.from_iterable(
    read_lines(f) for f in ['file1.txt', 'file2.txt']
)
```

### islice(iterable, stop) or islice(iterable, start, stop, step)

Slice an iterator (like list slicing but for iterators):

```python
from itertools import islice

# First 5 elements
list(islice(range(100), 5))  # [0, 1, 2, 3, 4]

# Elements 2-5
list(islice(range(100), 2, 6))  # [2, 3, 4, 5]

# Every other element, first 10
list(islice(range(100), 0, 10, 2))  # [0, 2, 4, 6, 8]

# Practical: preview large iterator
large_data = range(1_000_000)
preview = list(islice(large_data, 5))
print(f"First 5: {preview}")
```

### takewhile(predicate, iterable)

Takes elements while predicate is True:

```python
from itertools import takewhile

# Take while less than 5
list(takewhile(lambda x: x < 5, [1, 3, 5, 2, 4]))
# [1, 3] — stops at 5, doesn't see 2, 4

# Practical: read until blank line
lines = ['hello', 'world', '', 'ignored']
content = list(takewhile(lambda x: x != '', lines))
# ['hello', 'world']
```

### dropwhile(predicate, iterable)

Drops elements while predicate is True, then yields the rest:

```python
from itertools import dropwhile

# Drop while less than 5
list(dropwhile(lambda x: x < 5, [1, 3, 5, 2, 4]))
# [5, 2, 4] — starts yielding at 5

# Practical: skip header lines
lines = ['# comment', '# another', 'data1', 'data2']
data = list(dropwhile(lambda x: x.startswith('#'), lines))
# ['data1', 'data2']
```

### filterfalse(predicate, iterable)

Opposite of filter() — keeps elements where predicate is False:

```python
from itertools import filterfalse

# Keep odd numbers (where "is even" is False)
list(filterfalse(lambda x: x % 2 == 0, range(10)))
# [1, 3, 5, 7, 9]

# Compare with filter
list(filter(lambda x: x % 2 == 0, range(10)))
# [0, 2, 4, 6, 8]
```

### compress(data, selectors)

Filters data based on boolean selectors:

```python
from itertools import compress

data = ['A', 'B', 'C', 'D', 'E']
selectors = [True, False, True, False, True]
list(compress(data, selectors))  # ['A', 'C', 'E']

# Practical: filter based on condition list
names = ['Alice', 'Bob', 'Charlie', 'Diana']
is_active = [True, False, True, True]
active_users = list(compress(names, is_active))
# ['Alice', 'Charlie', 'Diana']
```

### groupby(iterable, key=None)

Groups consecutive elements by key:

```python
from itertools import groupby

# Group by first letter (data must be sorted!)
data = ['apple', 'ant', 'banana', 'bear', 'cherry']
for key, group in groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# a: ['apple', 'ant']
# b: ['banana', 'bear']
# c: ['cherry']

# Group consecutive equal elements
data = [1, 1, 1, 2, 2, 3, 3, 3, 3]
for key, group in groupby(data):
    print(f"{key}: {list(group)}")
# 1: [1, 1, 1]
# 2: [2, 2]
# 3: [3, 3, 3, 3]

# Important: data must be sorted by key!
data = ['apple', 'banana', 'ant']  # Not sorted
for key, group in groupby(data, key=lambda x: x[0]):
    print(f"{key}: {list(group)}")
# a: ['apple']
# b: ['banana']
# a: ['ant']  — 'ant' is separate because data wasn't sorted!
```

### accumulate(iterable, func=operator.add, initial=None)

Running accumulation (like cumulative sum):

```python
from itertools import accumulate
import operator

# Cumulative sum
list(accumulate([1, 2, 3, 4, 5]))  # [1, 3, 6, 10, 15]

# Cumulative product
list(accumulate([1, 2, 3, 4, 5], operator.mul))  # [1, 2, 6, 24, 120]

# Running maximum
list(accumulate([3, 1, 4, 1, 5, 9], max))  # [3, 3, 4, 4, 5, 9]

# With initial value
list(accumulate([1, 2, 3], initial=10))  # [10, 11, 13, 16]
```

### zip_longest(*iterables, fillvalue=None)

Like zip(), but continues until longest iterable is exhausted:

```python
from itertools import zip_longest

# Regular zip stops at shortest
list(zip([1, 2, 3], ['a', 'b']))  # [(1, 'a'), (2, 'b')]

# zip_longest continues
list(zip_longest([1, 2, 3], ['a', 'b']))
# [(1, 'a'), (2, 'b'), (3, None)]

# Custom fill value
list(zip_longest([1, 2, 3], ['a', 'b'], fillvalue='?'))
# [(1, 'a'), (2, 'b'), (3, '?')]
```

### tee(iterable, n=2)

Create n independent iterators from one:

```python
from itertools import tee

# Create two independent iterators
iter1, iter2 = tee(range(5))
list(iter1)  # [0, 1, 2, 3, 4]
list(iter2)  # [0, 1, 2, 3, 4]

# Useful for pairwise iteration
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)  # Advance second iterator
    return zip(a, b)

list(pairwise([1, 2, 3, 4]))  # [(1, 2), (2, 3), (3, 4)]
```

**Note**: Python 3.10+ has `itertools.pairwise()` built-in.

---

## Practical Examples

### Flatten Nested Lists

```python
from itertools import chain

nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flat = list(chain.from_iterable(nested))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

### Batch Processing

```python
from itertools import islice

def batched(iterable, n):
    """Yield successive n-sized chunks."""
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch

list(batched(range(10), 3))
# [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
```

**Note**: Python 3.12+ has `itertools.batched()` built-in.

### Round-Robin

```python
from itertools import cycle, islice

def roundrobin(*iterables):
    """Visit each iterable in turn."""
    iterators = cycle(iter(it) for it in iterables)
    # ... (simplified version)

# Example usage
list(islice(cycle([1, 2, 3]), 10))
# [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
```

### Generate Test Data

```python
from itertools import product

# All possible boolean combinations
test_cases = list(product([True, False], repeat=3))
# 8 test cases with all True/False combinations
```

---

## Summary

| Category | Functions |
|----------|-----------|
| Infinite | `count`, `cycle`, `repeat` |
| Combinatoric | `product`, `permutations`, `combinations`, `combinations_with_replacement` |
| Terminating | `chain`, `islice`, `takewhile`, `dropwhile`, `filterfalse`, `compress`, `groupby`, `accumulate`, `zip_longest`, `tee` |

**Key Points**:

- All itertools functions return **iterators** (lazy evaluation)
- Wrap in `list()` to see results
- Combine functions for powerful data pipelines
- Memory efficient for large datasets
- `groupby` requires sorted input
- Use `chain.from_iterable` to flatten nested structures

---

## Exercises

**Exercise 1.**
Write a function `powerset` that takes a list and returns a list of all subsets (the power set) using `chain.from_iterable` and `combinations`. For example, `powerset([1, 2, 3])` should return `[(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import chain, combinations

    def powerset(items):
        return list(chain.from_iterable(
            combinations(items, r) for r in range(len(items) + 1)
        ))

    # Test
    print(powerset([1, 2, 3]))
    # [(), (1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    ```

---

**Exercise 2.**
Write a function `sliding_pairs` that takes an iterable and returns a list of consecutive pairs using `tee` and `islice` (or `zip`). For example, `sliding_pairs([1, 2, 3, 4])` should return `[(1, 2), (2, 3), (3, 4)]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import tee

    def sliding_pairs(iterable):
        a, b = tee(iterable)
        next(b, None)
        return list(zip(a, b))

    # Test
    print(sliding_pairs([1, 2, 3, 4]))
    # [(1, 2), (2, 3), (3, 4)]
    ```

---

**Exercise 3.**
Write a function `batched_accumulate` that takes a list of numbers and a batch size, groups the numbers into batches using `islice`, sums each batch, and returns a list of the cumulative batch sums using `accumulate`. For example, `batched_accumulate([1, 2, 3, 4, 5, 6], 2)` should group as `[3, 7, 11]` (sums of `[1,2]`, `[3,4]`, `[5,6]`) then accumulate to `[3, 10, 21]`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import accumulate, islice

    def batched_accumulate(numbers, batch_size):
        it = iter(numbers)
        batch_sums = []
        while True:
            batch = list(islice(it, batch_size))
            if not batch:
                break
            batch_sums.append(sum(batch))
        return list(accumulate(batch_sums))

    # Test
    print(batched_accumulate([1, 2, 3, 4, 5, 6], 2))
    # [3, 10, 21]
    ```
