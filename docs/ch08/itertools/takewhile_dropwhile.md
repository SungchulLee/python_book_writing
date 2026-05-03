# takewhile and dropwhile

`takewhile()` returns elements while a condition is True, while `dropwhile()` skips elements while a condition is True, then yields all remaining elements. These functions operate on the leading portion of a sequence based on a predicate, making them especially useful for sorted or ordered data and for lazy evaluation over potentially infinite iterators.

!!! tip "Mental Model"
    Think of `takewhile` as reading lines until you hit a blank — it consumes from the front while the predicate holds, then stops forever. `dropwhile` is the opposite: it skips the leading run of matching elements and then yields everything remaining, regardless of whether later elements match. Together they split a sequence at the first boundary where the predicate changes.

## takewhile() - Take While Condition is True

`takewhile()` yields elements from the start of the iterable as long as the predicate returns `True`. It stops permanently at the first element that fails the predicate, even if later elements would pass.

```python
from itertools import takewhile

numbers = [1, 2, 3, 4, 5, 3, 2, 1]

# Take while less than 4
result = list(takewhile(lambda x: x < 4, numbers))
print(result)
```

```
[1, 2, 3]
```

## dropwhile() - Drop While Condition is True

`dropwhile()` discards elements from the start of the iterable as long as the predicate returns `True`. Once the predicate returns `False` for the first time, it yields that element and all subsequent elements unconditionally.

```python
from itertools import dropwhile

numbers = [1, 2, 3, 4, 5, 3, 2, 1]

# Drop while less than 4
result = list(dropwhile(lambda x: x < 4, numbers))
print(result)

# Practical: skip whitespace at start
lines = ['  ', '  ', 'content', 'more']
content = list(dropwhile(str.isspace, lines))
print(content)
```

```
[4, 5, 3, 2, 1]
['content', 'more']
```

---

## Exercises

**Exercise 1.**
Use `takewhile` to extract the leading digits from a string. For example, `leading_digits("123abc456")` should return `"123"`. Hint: use `str.isdigit` as the predicate.

??? success "Solution to Exercise 1"

    ```python
    from itertools import takewhile

    def leading_digits(s):
        return "".join(takewhile(str.isdigit, s))

    # Test
    print(leading_digits("123abc456"))  # 123
    print(leading_digits("abc123"))     # (empty string)
    print(leading_digits("42"))         # 42
    ```

---

**Exercise 2.**
Use `dropwhile` to skip all the header lines (lines starting with `#`) from a list of text lines and return the remaining content lines. For example, given `["# header", "# comment", "data1", "data2"]`, return `["data1", "data2"]`.

??? success "Solution to Exercise 2"

    ```python
    from itertools import dropwhile

    lines = ["# header", "# comment", "data1", "data2"]
    content = list(dropwhile(lambda line: line.startswith("#"), lines))
    print(content)  # ['data1', 'data2']
    ```

---

**Exercise 3.**
Write a function `between_markers` that takes a list and two predicates, and returns the elements between the first element that fails predicate1 (using `dropwhile`) and up to (but not including) the first element in the remaining that fails predicate2 (using `takewhile`). For example, `between_markers([0, 0, 5, 3, 8, 0, 0], lambda x: x == 0, lambda x: x != 0)` should return `[5, 3, 8]`.

??? success "Solution to Exercise 3"

    ```python
    from itertools import dropwhile, takewhile

    def between_markers(items, pred_drop, pred_take):
        after_drop = dropwhile(pred_drop, items)
        return list(takewhile(pred_take, after_drop))

    # Test
    result = between_markers(
        [0, 0, 5, 3, 8, 0, 0],
        lambda x: x == 0,
        lambda x: x != 0,
    )
    print(result)  # [5, 3, 8]
    ```
