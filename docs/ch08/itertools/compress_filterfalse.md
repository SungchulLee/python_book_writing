# compress and filterfalse

`compress()` filters based on a selector iterable, while `filterfalse()` keeps elements where the predicate is False. Use `compress()` when you have a precomputed boolean mask from a separate computation, and `filterfalse()` when you need the complement of the built-in `filter()` — that is, the elements that fail a predicate test.

!!! tip "Mental Model"
    `compress` is a stencil: lay a boolean mask over your data and only the items under `True` holes pass through. `filterfalse` is the inverse of `filter` — it keeps what `filter` would discard. Together they let you partition data by any criterion without writing conditional loops.

## compress() - Filter with Selectors

`compress()` pairs each element in a data iterable with a corresponding value in a selector iterable and yields only those elements whose selector is truthy. This is similar to applying a boolean mask to a sequence.

```python
from itertools import compress

data = ['a', 'b', 'c', 'd', 'e']
selectors = [1, 0, 1, 0, 1]

result = list(compress(data, selectors))
print(result)
```

```
['a', 'c', 'e']
```

## filterfalse() - Inverse Filter

`filterfalse()` is the complement of the built-in `filter()`. While `filter()` keeps elements for which the predicate returns `True`, `filterfalse()` keeps elements for which it returns `False`.

```python
from itertools import filterfalse

numbers = [1, 2, 3, 4, 5, 6, 7, 8]

# Keep even numbers using filterfalse
evens = list(filterfalse(lambda x: x % 2, numbers))
print("Evens:", evens)

# Keep short words
words = ['cat', 'elephant', 'dog', 'bird', 'butterfly']
short = list(filterfalse(lambda w: len(w) > 4, words))
print("Short words:", short)
```

```
Evens: [2, 4, 6, 8]
Short words: ['cat', 'dog', 'bird']
```

---

## Exercises

**Exercise 1.**
Use `compress` to select elements from a list of names based on a corresponding list of boolean values indicating whether each person passed an exam. For example, given `names = ["Alice", "Bob", "Carol", "Dave"]` and `passed = [True, False, True, False]`, return `["Alice", "Carol"]`.

??? success "Solution to Exercise 1"

    ```python
    from itertools import compress

    names = ["Alice", "Bob", "Carol", "Dave"]
    passed = [True, False, True, False]
    result = list(compress(names, passed))
    print(result)  # ['Alice', 'Carol']
    ```

---

**Exercise 2.**
Use `filterfalse` to extract all non-numeric strings from a mixed list. Write a function `non_numeric` that takes a list of strings and returns only those that cannot be converted to a float. For example, `non_numeric(["3.14", "hello", "42", "world"])` should return `["hello", "world"]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import filterfalse

    def is_numeric(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def non_numeric(items):
        return list(filterfalse(is_numeric, items))

    # Test
    print(non_numeric(["3.14", "hello", "42", "world"]))
    # ['hello', 'world']
    ```

---

**Exercise 3.**
Write a function `split_by_predicate` that takes a list and a predicate function, and returns two lists: one with items where the predicate is True (using `filter`) and one where it is False (using `filterfalse`). For example, `split_by_predicate([1, 2, 3, 4, 5, 6], lambda x: x % 2 == 0)` should return `([2, 4, 6], [1, 3, 5])`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import filterfalse

    def split_by_predicate(items, predicate):
        truthy = list(filter(predicate, items))
        falsy = list(filterfalse(predicate, items))
        return truthy, falsy

    # Test
    evens, odds = split_by_predicate(
        [1, 2, 3, 4, 5, 6], lambda x: x % 2 == 0
    )
    print(evens)  # [2, 4, 6]
    print(odds)   # [1, 3, 5]
    ```
