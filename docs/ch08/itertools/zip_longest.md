# zip_longest

When combining iterables of unequal length, Python's built-in `zip()` silently truncates to the shortest input — which can cause data loss. `zip_longest()` from the `itertools` module solves this by continuing until every iterable is exhausted, filling in a default value for the shorter ones.

!!! tip "Mental Model"
    `zip` stops at the shortest input like a zipper that runs out of teeth on one side. `zip_longest` pads the short side with a fill value and keeps going until every iterable is exhausted. Reach for it whenever losing trailing elements would silently corrupt your data — for example, when aligning columns of unequal length.

## Zipping Different Length Iterables

The following example pairs a 3-element list with a 5-element list. The `fillvalue` parameter specifies what to substitute for the missing entries in the shorter iterable.

```python
from itertools import zip_longest

list1 = [1, 2, 3]
list2 = ['a', 'b', 'c', 'd', 'e']

result = list(zip_longest(list1, list2, fillvalue='*'))
print(result)
```

```text
[(1, 'a'), (2, 'b'), (3, 'c'), ('*', 'd'), ('*', 'e')]
```

## Custom Fill Value

The default fill value is `None`, but you can pass any object via the `fillvalue` parameter. This is especially useful when the fill value must be meaningful in downstream processing — for example, using `'N/A'` for missing names.

```python
from itertools import zip_longest

names = ['Alice', 'Bob']
scores = [95, 87, 92, 88]

result = list(zip_longest(names, scores, fillvalue='N/A'))
for name, score in result:
    print(f"{name}: {score}")
```

```text
Alice: 95
Bob: 87
N/A: 92
N/A: 88
```

---

## Exercises

**Exercise 1.**
Use `zip_longest` to merge two lists of different lengths into a list of tuples, using `0` as the fill value. For example, `merge_with_zeros([1, 2, 3], [10, 20])` should return `[(1, 10), (2, 20), (3, 0)]`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import zip_longest

    def merge_with_zeros(list1, list2):
        return list(zip_longest(list1, list2, fillvalue=0))

    # Test
    print(merge_with_zeros([1, 2, 3], [10, 20]))
    # [(1, 10), (2, 20), (3, 0)]
    ```

---

**Exercise 2.**
Write a function `transpose_ragged` that takes a list of lists of different lengths and transposes them using `zip_longest`, filling missing values with `None`. For example, `transpose_ragged([[1, 2, 3], [4, 5], [6]])` should return `[(1, 4, 6), (2, 5, None), (3, None, None)]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import zip_longest

    def transpose_ragged(matrix):
        return list(zip_longest(*matrix, fillvalue=None))

    # Test
    result = transpose_ragged([[1, 2, 3], [4, 5], [6]])
    print(result)
    # [(1, 4, 6), (2, 5, None), (3, None, None)]
    ```

---

**Exercise 3.**
Write a function `interleave_longest` that takes multiple iterables and interleaves their elements one at a time, padding shorter ones with a sentinel value. Use `zip_longest` and `chain`. For example, `interleave_longest("AB", "CDEF", "GH", fillvalue="-")` should return `['A', 'C', 'G', 'B', 'D', 'H', '-', 'E', '-', '-', 'F', '-']`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import zip_longest, chain

    def interleave_longest(*iterables, fillvalue="-"):
        return list(chain.from_iterable(
            zip_longest(*iterables, fillvalue=fillvalue)
        ))

    # Test
    result = interleave_longest("AB", "CDEF", "GH", fillvalue="-")
    print(result)
    # ['A', 'C', 'G', 'B', 'D', 'H', '-', 'E', '-', '-', 'F', '-']
    ```
