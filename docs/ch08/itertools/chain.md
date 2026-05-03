# chain and chain.from_iterable

The `chain()` function concatenates multiple iterables into a single iterator, while `chain.from_iterable()` accepts an iterable of iterables. These tools let you process items from several sources as a single stream without copying them into a new collection, preserving memory efficiency and keeping code concise.

!!! tip "Mental Model"
    `chain` is like laying train tracks end-to-end — items come from the first iterable, then seamlessly from the second, and so on, without ever building a combined list in memory. Use `chain()` when you have a known set of iterables and `chain.from_iterable()` when the iterables themselves come from a generator or lazy source.

## chain() - Concatenate Iterables

Pass any number of iterables as separate arguments to `chain()`. It yields elements from the first iterable until it is exhausted, then proceeds to the next, and so on.

```python
from itertools import chain

list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
list3 = [10, 20]

result = list(chain(list1, list2, list3))
print(result)
```

```
[1, 2, 3, 'a', 'b', 'c', 10, 20]
```

## chain.from_iterable() - Flatten Iterables

Unlike `chain()`, which requires each iterable as a separate argument, `chain.from_iterable()` accepts a single iterable of iterables. This is essential when the sub-iterables come from a generator or when their count is not known in advance.

```python
from itertools import chain

lists = [[1, 2], [3, 4], [5, 6]]
result = list(chain.from_iterable(lists))
print(result)

# Flatten a generator expression
nested = ([i, i+10] for i in range(3))
flattened = list(chain.from_iterable(nested))
print(flattened)
```

```
[1, 2, 3, 4, 5, 6]
[0, 10, 1, 11, 2, 12]
```

---

## Exercises

**Exercise 1.**
Write a function `flatten_one_level` that takes a list of lists and returns a single flat list using `chain.from_iterable`. For example, `flatten_one_level([[1, 2], [3], [4, 5, 6]])` should return `[1, 2, 3, 4, 5, 6]`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import chain

    def flatten_one_level(nested):
        return list(chain.from_iterable(nested))

    # Test
    print(flatten_one_level([[1, 2], [3], [4, 5, 6]]))
    # [1, 2, 3, 4, 5, 6]
    ```

---

**Exercise 2.**
Write a function `merge_sorted_iterators` that takes multiple sorted lists and returns a single sorted list by chaining them together and then sorting. For example, `merge_sorted_iterators([1, 4, 7], [2, 5, 8], [3, 6, 9])` should return `[1, 2, 3, 4, 5, 6, 7, 8, 9]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import chain

    def merge_sorted_iterators(*iterables):
        return sorted(chain(*iterables))

    # Test
    print(merge_sorted_iterators([1, 4, 7], [2, 5, 8], [3, 6, 9]))
    # [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ```

---

**Exercise 3.**
Write a function `unique_items` that takes multiple iterables and returns a list of unique items (preserving first-seen order) using `chain`. For example, `unique_items([1, 2, 3], [2, 3, 4], [4, 5])` should return `[1, 2, 3, 4, 5]`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import chain

    def unique_items(*iterables):
        seen = set()
        result = []
        for item in chain(*iterables):
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result

    # Test
    print(unique_items([1, 2, 3], [2, 3, 4], [4, 5]))
    # [1, 2, 3, 4, 5]
    ```
